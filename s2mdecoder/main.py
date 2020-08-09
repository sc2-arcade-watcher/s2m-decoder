import os
import sys
import json
import binascii
import xml.etree.ElementTree as ET
from pprint import pprint
from sc2reader.decoders import BitPackedDecoder

def to_hex(data):
    return binascii.hexlify(data).decode('ascii')

def to_bool(data: int):
    assert 0 <= data <= 1
    return bool(data)

def read_depot_link(data):
    o = {}
    o['type'] = data[0:4].decode('ascii')
    o['server'] = data[4:8].strip(b'\x00').decode('ascii').lower()
    o['hash'] = to_hex(data[8:])
    return o

def read_localization_link(data):
    return {
        'locale': data[0].decode('ascii'),
        'stringTable': [*map(read_depot_link, data[1])],
    }

def read_instance_header(data):
    assert len(data) == 2
    return {
        'id': data[0],
        'version': data[1],
        # 'majorVersion': data[1] >> 16,
        # 'minorVersion': data[1] & 0xFFFF,
    }

def read_localization_table_key(data):
    if data is None:
        return None
    assert len(data) == 3
    return {
        'color': data[0],
        'table': data[1],
        'index': data[2],
    }

def read_picture(data):
    if data is None:
        return None
    assert len(data) == 5
    return {
        'index': data[0],
        'top': data[1],
        'left': data[2],
        'width': data[3],
        'height': data[4],
    }

def read_screenshot_entry(data):
    assert len(data) == 2
    return {
        'picture': read_picture(data[0]),
        'caption': read_localization_table_key(data[1]),
    }

def read_namespace_definition(data):
    assert len(data) == 2
    return {
        'namespace': read_attribute_link(data[0]),
        'value': read_attribute_default_value_or_values(data[1]),
    }

def read_map_info(data):
    o = {}
    ver = max(data.keys())

    assert ver in [8, 10, 11]

    o['name'] = read_localization_table_key(data[0])
    o['description'] = read_localization_table_key(data[1])
    assert data[2] == None
    o['thumbnail'] = read_picture(data[3])
    o['maxPlayers'] = data[4]
    assert data[5] == 22
    o['namespaceDefinitions'] = [*map(read_namespace_definition, data[6])]
    o['visualFiles'] = [*map(read_depot_link, data[7])]
    o['localeTable'] = [*map(read_localization_link, data[8])]

    if ver >= 10:
        assert len(data[9]) == 0
        assert len(data[10]) == 0
    if ver >= 11:
        # 11: [{0: {0: 999, 1: 3004}, 1: 1011, 2: [{0: b'\x00Lic', 1: 162}]}]}
        pass

    return o

def read_premium_info(data):
    o = {}
    ver = max(data.keys())
    assert ver in [0]
    o['license'] = data[0]
    return o

def read_attribute_visual(data):
    assert len(data) == 3
    return {
        'text': read_localization_table_key(data[0]),
        'tip': read_localization_table_key(data[1]),
        'art': read_picture(data[2]),
    }

def read_attribute_value_definition(data):
    ver = max(data.keys())
    assert ver in [1, 2]
    if ver >= 2:
        assert len(data[2]) == 0
    return {
        'value': data[0].decode('ascii'),
        'visual': read_attribute_visual(data[1])
    }

VISIBILITY_TYPE = {
    0: 'none',
    1: 'self',
    2: 'host',
    3: 'all',
}

def read_attribute_definition(data):
    o = {}
    o['namespace'] = read_attribute_link(data[0])
    o['values'] = [*map(read_attribute_value_definition, data[1])]
    o['visual'] = read_attribute_visual(data[2])
    o['requirements'] = str(data[3])
    o['arbitration'] = data[4]
    # 0x00 always
    # 0x01 first come, first serve
    o['visibility'] = VISIBILITY_TYPE[data[5]]
    o['access'] = VISIBILITY_TYPE[data[6]]
    o['options'] = data[7]
    # options flags:
    # 0x01 unknown
    # 0x02 locked when public
    # 0x04 hidden
    o['default'] = read_attribute_default_value_or_values(data[8])
    o['sortOrder'] = data[9]
    return o

def read_attribute_link(data):
    assert len(data) == 2
    return {
        'namespace': data[0],
        'id': data[1],
    }

def read_attribute_default_value(data):
    assert len(data) == 2
    return {
        'index': data[0],
        'unk_attr_val_1': data[1],
    }

def read_attribute_default_value_or_values(data):
    if isinstance(data, list):
        return [*map(read_attribute_default_value, data)]
    else:
        return read_attribute_default_value(data)

def read_variant_attribute_defaults(data):
    assert len(data) == 2
    o = {}
    o['attribute'] = read_attribute_link(data[0])
    o['value'] = read_attribute_default_value_or_values(data[1])
    return o

def read_variant_attribute_locked(data):
    assert len(data) == 2
    o = {}
    o['attribute'] = read_attribute_link(data[0])
    o['lockedScopes'] = data[1]
    return o

def read_variant_attribute_visibility(data):
    assert len(data) == 2
    o = {}
    o['attribute'] = read_attribute_link(data[0])
    o['hidden'] = data[1]
    return o

def read_variant_info(data):
    o = {}
    ver = max(data.keys())
    assert ver in [8, 11, 12, 13, 14, 15]
    assert len(data[0]) == 2
    o['categoryId'] = data[0][0]
    o['modeId'] = data[0][1]
    o['categoryName'] = read_localization_table_key(data[1])
    o['modeName'] = read_localization_table_key(data[2])
    o['categoryDescription'] = read_localization_table_key(data[3])
    o['modeDescription'] = read_localization_table_key(data[4])
    assert len(data[5]) == 3
    o['attributeDefaults'] = [*map(read_variant_attribute_defaults, data[6])]
    o['lockedAttributes'] = [*map(read_variant_attribute_locked, data[7])]
    o['maxTeamSize'] = data[8]
    if ver >= 11:
        o['attributeVisibility'] = [*map(read_variant_attribute_visibility, data[9])]
        # TODO: data[10] - attribute value restrictions?
        # 10: [{0: {0: 999, 1: 500}, 1: {0: [8, 8, 8, 8]}}],
        o['achievementTags'] = [x.strip(b'\x00').decode('ascii') for x in data[11]]
    if ver >= 12:
        o['maxHumanPlayers'] = data[12]
    if ver >= 13:
        o['maxOpenSlots'] = data[13]
    if ver >= 14:
        o['premiumInfo'] = read_premium_info(data[14]) if data[14] is not None else None
    if ver >= 15:
        o['teamNames'] = [*map(read_localization_table_key, data[15])]
    return o

LIST_TYPE = {
    0: 'bulleted',
    1: 'numbered',
    2: 'none',
}

def read_arcade_section_header(data):
    assert len(data) == 4
    o = {}
    o['title'] = read_localization_table_key(data[0])
    o['startOffset'] = data[1]
    o['listType'] = LIST_TYPE[data[2]]
    o['subtitle'] = read_localization_table_key(data[3])
    return o

def read_arcade_section_raw(data):
    assert len(data) == 2
    o = {}
    o['headers'] = [*map(read_arcade_section_header, data[0])]
    o['items'] = [*map(read_localization_table_key, data[1])]
    return o

def read_arcade_section(data):
    assert len(data) == 2
    sect_headers = [*map(read_arcade_section_header, data[0])]
    sect_items = [*map(read_localization_table_key, data[1])]
    prev = len(sect_items)
    for x in reversed(sect_headers):
        x['items'] = sect_items[x['startOffset']:prev]
        prev = x['startOffset']
        del x['startOffset']
    return sect_headers

def read_arcade_tutorial_link(data):
    assert len(data) == 3
    o = {}
    o['variantIndex'] = data[0],
    o['speed'] = data[1].decode('ascii'),
    # looks like link to map, but it's an array..
    assert len(data[2]) == 1
    o['map'] = read_instance_header(data[2][0][0])
    return o

def read_arcade_info(data):
    o = {}
    ver = max(data.keys())
    assert ver == 9

    # extra visualizationFiles ??
    assert len(data[0]) == 0
    # extra localizationFiles ??
    assert len(data[1]) == 0
    o['gameInfoScreenshots'] = [*map(read_screenshot_entry, data[2])]
    o['howToPlayScreenshots'] = [*map(read_screenshot_entry, data[3])]
    o['howToPlaySections'] = read_arcade_section(data[4])
    o['patchNoteSections'] = read_arcade_section(data[5])
    o['mapIcon'] = read_picture(data[6])
    o['tutorialLink'] = read_arcade_tutorial_link(data[7]) if data[7] is not None else None
    o['matchmakerTags'] = [x.strip(b'\x00').decode('ascii') for x in data[8]]
    o['website'] = read_localization_table_key(data[9])

    return o

KNOWN_TAGS = ['BLIZ', 'TRIL', 'FEAT', 'PRGN', 'HotS', 'LotV', 'WoL', 'WoLX', 'HoSX', 'LoVX', 'HerX', 'Desc', 'Glue', 'Blnc', 'PREM']

def read_s2mh(data):
    o = {}
    assert len(data) == 2
    data = data[0]
    ver = max(data.keys())
    assert ver in [13, 14, 18, 22, 23, 24]

    # pprint(data, width=200)

    assert len(data[0]) == 2
    o['header'] = read_instance_header(data[0])
    o['name'] = data[1].decode('utf8')
    o['mapFile'] = read_depot_link(data[2])
    o['mapNamespace'] = data[3]
    o['mapInfo'] = read_map_info(data[4])
    o['attributes'] = [*map(read_attribute_definition, data[5])]

    if 6 in data:
        o['unk6'] = '%s' % data[6]

    # TODO: 7 - score IDs and such?
    # o['resultDefinitions'] = []

    o['localeTable'] = [*map(read_localization_link, data[8])]
    o['mapSize'] = {
        'horizontal': data[9][0],
        'vertical': data[9][1],
    } if data[9] is not None else None

    if 11 in data:
        o['specialTags'] = [data[11].decode('ascii')] if data[11] is not None else []
    o['tileset'] = read_localization_table_key(data[10])
    o['defaultVariantIndex'] = data[12]
    o['variants'] = [*map(read_variant_info, data[13])]

    if ver >= 14:
        o['dependencies'] = [*map(read_instance_header, data[14])]
    if ver >= 18:
        o['addDefaultPermissions'] = to_bool(data[15])
        o['relevantPermissions'] = [*map(lambda x: {'name': x[0].strip(b'\x00').decode('ascii'), 'number': x[1]}, data[16])]
        o['specialTags'] = [x.strip(b'\x00').decode('ascii') for x in data[18]]
    if ver >= 22:
        o['arcade'] = read_arcade_info(data[19]) if data[19] else None
        o['addMultiMod'] = to_bool(data[22])
    if ver >= 23:
        # 23: [b'SC2ParkVoicePack'
        pass
    if ver >= 24:
        # array with a lot of numbers - possibly reward IDs?
        # 24: [23498
        pass

    for x in o['specialTags']:
        assert x in KNOWN_TAGS

    return o


def s2mh_apply_s2ml(data, translation, fields = None):
    def translate_prop(prop):
        if prop['index'] == 0:
            return None
        return translation[str(prop['index'])]

    if fields is None:
        fields = {
            'mapInfo': {
                'name': True,
                'description': True,
            },
            'tileset': True,
            'variants': {
                'categoryName': True,
                'modeName': True,
                'categoryDescription': True,
                'modeDescription': True,
            },
            'arcade': {
                'gameInfoScreenshots': {
                    'caption': True,
                },
                'howToPlayScreenshots': {
                    'caption': True,
                },
                'howToPlaySections': {
                    'title': True,
                    'subtitle': True,
                    'items': True,
                },
                'patchNoteSections': {
                    'title': True,
                    'subtitle': True,
                    'items': True,
                },
                'website': True,
            },
        }

    for x in fields:
        if isinstance(data[x], list):
            for y, item in enumerate(data[x]):
                if fields[x] is True:
                    data[x][y] = translate_prop(data[x][y])
                elif isinstance(fields[x], dict):
                    s2mh_apply_s2ml(data[x][y], translation, fields[x])
        else:
            if fields[x] is True and data[x] is not None:
                data[x] = translate_prop(data[x])
            elif isinstance(fields[x], dict):
                s2mh_apply_s2ml(data[x], translation, fields[x])

    return data


def read_s2mi(data):
    o = {}
    assert len(data) == 2
    data = data[0]
    ver = max(data.keys())
    assert ver in [22, 23, 26]

    o['header'] = read_instance_header(data[0])
    o['headerCacheHandle'] = read_depot_link(data[1])
    o['uploadTime'] = data[2]
    o['isLinked'] = bool(data[3])
    o['isLocked'] = bool(data[4])
    o['isPrivate'] = bool(data[5])
    o['mapSize'] = data[6]
    o['name'] = data[7].decode('utf8')
    # o['profileRecordAddress'] = data[8]
    o['isMod'] = bool(data[9])
    assert len(data[11]) == 4
    o['authorToonName'] = {
        'regionId': data[11][0],
        'app': data[11][1].strip(b'\x00').decode('ascii'),
        'realmId': data[11][2],
        'battleTag': data[11][3].decode('utf8'),
    }
    o['isLatestVersion'] = bool(data[12])
    o['mainLocale'] = data[13].decode('ascii')
    assert len(data[14]) == 4
    o['authorToonHandle'] = {
        'regionId': data[14][0],
        'app': data[14][1].strip(b'\x00').decode('ascii'),
        'realmId': data[14][2],
        'profileId': data[14][3],
    }
    o['isSkipInitialDownload'] = bool(data[15])
    o['createdTime'] = data[16]
    o['labels'] = [x.decode('ascii') for x in data[17]]
    o['isMelee'] = bool(data[18])
    o['isCluster'] = bool(data[19])
    o['clusterParent'] = data[20]
    o['clusterChildren'] = data[21]
    o['isHiddenLobby'] = bool(data[22])
    o['isExtensionMod'] = bool(data[23]) if 23 in data else False
    if ver >= 24:
        o['transitionId'] = data[24]
        o['lastPublishTime'] = data[25]
        o['firstPublicPublishTime'] = data[26]

    return o


def read_s2ml(filename):
    o = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        o[child.attrib['id']] = child.text or ''
    return o


def read_file(filename):
    with open(filename, 'rb') as f:
        ext = os.path.splitext(filename)[1][1:]
        data = BitPackedDecoder(f.read()).read_struct()
        if ext == 's2mh':
            return read_s2mh(data)
        elif ext == 's2mi':
            return read_s2mi(data)
        else:
            raise Exception(ext)
        return data


def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        data = read_file(filename)
        if len(sys.argv) >= 3:
            translation = read_s2ml(sys.argv[2])
            print(json.dumps(s2mh_apply_s2ml(data, translation), indent=4, ensure_ascii=False))
        else:
            print(json.dumps(data, indent=4, ensure_ascii=False))
            # with open(filename, 'rb') as f:
            #     data = BitPackedDecoder(f.read()).read_struct()
            #     pprint(data, width=180)


if __name__ == '__main__':
    main()
