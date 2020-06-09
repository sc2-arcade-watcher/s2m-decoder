# s2m-decoder

Supported filetypes:
* `s2mi` - StarCraft II Map Info (Base)
* `s2mh` - StarCraft II Map Header
    * incomplete: attribute definitions. several fields/sections remain unknown.

## Info

**Version number**

Conversion goes as follows:

```py
def to_sc2_ver(version):
    return {
        'majorVersion': version >> 16,
        'minorVersion': version & 0xFFFF,
    }
```
```py
>>> print(to_sc2_ver(65568))
{'majorVersion': 1, 'minorVersion': 32}
```

**Pictures**

All images across the structure are referenced from `visualFiles` array.

```json
"picture": {
    "index": 1,
    "top": 0,
    "left": 0,
    "width": 600,
    "height": 800
},
```

Above example references second element (`index = 1`) from `visualFiles`).

**Localizations**

Strings are referenced in similar way to pictures. However it's possible to have multiple files for the same localization. They're refered to as string tables in the code.

```json
"name": {
    "table": 0,
    "index": 1
},
```
String table:
```xml
<Locale region="enUS">
    <e id="1">Ice Baneling Escape - Cold Voyage</e>
    <!-- ... -->
</Locale>
```

**Depot handles**

Depot handles reference another resource from the Blizzard depot.

```json
"headerCacheHandle": {
    "type": "s2mh",
    "server": "us",
    "hash": "a1f3dfd0ceea4562e5045b6ebb0ad97f416308254c137c28455f55e6535c9f8b"
},
```

Link to the above:
`http://us.depot.battle.net:1119/a1f3dfd0ceea4562e5045b6ebb0ad97f416308254c137c28455f55e6535c9f8b.s2mh`

## Output examples

### Decode s2mi

> `$ s2mdecoder eb37f724c481a8deda5e98d989adb6bb0d46a2d80f9bab37fa0ee04367fcc435.s2mi`

```json
{
    "instance": {
        "id": 289177,
        "version": 65568
    },
    "headerCacheHandle": {
        "type": "s2mh",
        "server": "us",
        "hash": "a1f3dfd0ceea4562e5045b6ebb0ad97f416308254c137c28455f55e6535c9f8b"
    },
    "uploadTime": 1516437999,
    "isLinked": true,
    "isLocked": true,
    "isPrivate": false,
    "mapSize": 5619565,
    "name": "Ice Baneling Escape - Cold Voyage",
    "isMod": false,
    "authorToonName": {
        "regionId": 1,
        "app": "S2",
        "realmId": 1,
        "battleTag": "Chioy#812"
    },
    "isLatestVersion": true,
    "mainLocale": "enUS",
    "authorToonHandle": {
        "regionId": 1,
        "app": "S2",
        "realmId": 1,
        "profileId": 4293706
    },
    "isSkipInitialDownload": false,
    "createdTime": 0,
    "labels": [],
    "isMelee": false,
    "isCluster": false,
    "clusterParent": null,
    "clusterChildren": [],
    "isHiddenLobby": false,
    "isExtensionMod": false
}
```

### Decode s2mh

> `$ s2mdecoder a1f3dfd0ceea4562e5045b6ebb0ad97f416308254c137c28455f55e6535c9f8b.s2mh`

```json
{
    "instance": {
        "id": 289177,
        "version": 65568
    },
    "name": "ColdVoyage.SC2Map",
    "mapFile": {
        "type": "s2ma",
        "server": "us",
        "hash": "7067e8b25868263f1c2006c0722983114d026293779d60c738512308a7b4480c"
    },
    "mapNamespace": 362949,
    "mapInfo": {
        "name": {
            "table": 0,
            "index": 1
        },
        "description": {
            "table": 0,
            "index": 2
        },
        "thumbnail": {
            "index": 0,
            "top": 0,
            "left": 0,
            "width": 512,
            "height": 512
        },
        "maxPlayers": 10,
        "visualFiles": [
            {
                "type": "s2mv",
                "server": "us",
                "hash": "ab3f92a8e025b25fca4a8cc8c8736b0b3614c3dcc7875a5b6b3c94f391124a63"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "c50888599249b83e3ec4463cd8467279394839e11668f3cb28312a5545c706fd"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "b952eef72d5009bcaa153fde74511b3b4be5aff7671d03491e1f16b090b07a8f"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "47834a60f73bfaf9d857e10e9aee0596a4b90ba49a0b8b7f63e05c04b72b6d2a"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "61faf4c17b59e368b43693a218cb24af46bd6c7950d36fd1edab869a640f3283"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "d9e0f7b9756900581119faa3337563ffebc455e877c20b10ab0c8df5af14f870"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "d2e06878a567b7a4b1f6957bb75d40c6d356890fe0d498d41444da8c9dc19f4b"
            }
        ],
        "localeTable": [
            {
                "locale": "enUS",
                "stringTable": [
                    {
                        "type": "s2ml",
                        "server": "us",
                        "hash": "2177ce1bf9453f634457242b2b8758df5390e2c531732fb7e6fa027c8ba4a5c6"
                    }
                ]
            }
        ]
    },
    "definitions": [],
    "resultDefinitions": [],
    "localeTable": [
        {
            "locale": "enUS",
            "stringTable": [
                {
                    "type": "s2ml",
                    "server": "us",
                    "hash": "2177ce1bf9453f634457242b2b8758df5390e2c531732fb7e6fa027c8ba4a5c6"
                }
            ]
        }
    ],
    "mapSize": {
        "horizontal": 256,
        "vertical": 256
    },
    "tileset": {
        "table": 0,
        "index": 3
    },
    "defaultVariantIndex": 0,
    "variants": [
        {
            "categoryName": {
                "table": 0,
                "index": 4
            },
            "modeName": {
                "table": 0,
                "index": 6
            },
            "categoryDescription": {
                "table": 0,
                "index": 5
            },
            "modeDescription": {
                "table": 0,
                "index": 7
            },
            "categoryId": 10,
            "achievementTags": [],
            "maxHumanPlayers": 10,
            "maxOpenSlots": 16
        }
    ],
    "dependencies": [
        {
            "id": 288191,
            "version": 0
        },
        {
            "id": 12,
            "version": 0
        }
    ],
    "unknown_15": 1,
    "licenses": [],
    "specialTags": [],
    "arcade": {
        "gameInfoScreenshots": [
            {
                "picture": {
                    "index": 1,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": {
                    "table": 0,
                    "index": 0
                }
            },
            {
                "picture": {
                    "index": 2,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": {
                    "table": 0,
                    "index": 0
                }
            },
            {
                "picture": {
                    "index": 3,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": {
                    "table": 0,
                    "index": 0
                }
            },
            {
                "picture": {
                    "index": 4,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": {
                    "table": 0,
                    "index": 0
                }
            },
            {
                "picture": {
                    "index": 5,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": {
                    "table": 0,
                    "index": 0
                }
            }
        ],
        "howToPlayScreenshots": [],
        "howToPlaySections": {
            "headers": [
                {
                    "title": {
                        "table": 0,
                        "index": 8
                    },
                    "startOffset": 0,
                    "listType": 0,
                    "subtitle": {
                        "table": 0,
                        "index": 0
                    }
                },
                {
                    "title": {
                        "table": 0,
                        "index": 12
                    },
                    "startOffset": 3,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 0
                    }
                }
            ],
            "items": [
                {
                    "table": 0,
                    "index": 9
                },
                {
                    "table": 0,
                    "index": 10
                },
                {
                    "table": 0,
                    "index": 11
                },
                {
                    "table": 0,
                    "index": 13
                }
            ]
        },
        "patchNoteSections": {
            "headers": [
                {
                    "title": {
                        "table": 0,
                        "index": 15
                    },
                    "startOffset": 0,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 16
                    }
                },
                {
                    "title": {
                        "table": 0,
                        "index": 21
                    },
                    "startOffset": 4,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 22
                    }
                },
                {
                    "title": {
                        "table": 0,
                        "index": 25
                    },
                    "startOffset": 6,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 26
                    }
                },
                {
                    "title": {
                        "table": 0,
                        "index": 30
                    },
                    "startOffset": 9,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 31
                    }
                },
                {
                    "title": {
                        "table": 0,
                        "index": 34
                    },
                    "startOffset": 11,
                    "listType": 2,
                    "subtitle": {
                        "table": 0,
                        "index": 35
                    }
                }
            ],
            "items": [
                {
                    "table": 0,
                    "index": 17
                },
                {
                    "table": 0,
                    "index": 18
                },
                {
                    "table": 0,
                    "index": 19
                },
                {
                    "table": 0,
                    "index": 20
                },
                {
                    "table": 0,
                    "index": 23
                },
                {
                    "table": 0,
                    "index": 24
                },
                {
                    "table": 0,
                    "index": 27
                },
                {
                    "table": 0,
                    "index": 28
                },
                {
                    "table": 0,
                    "index": 29
                },
                {
                    "table": 0,
                    "index": 32
                },
                {
                    "table": 0,
                    "index": 33
                },
                {
                    "table": 0,
                    "index": 36
                },
                {
                    "table": 0,
                    "index": 37
                },
                {
                    "table": 0,
                    "index": 38
                },
                {
                    "table": 0,
                    "index": 39
                },
                {
                    "table": 0,
                    "index": 40
                },
                {
                    "table": 0,
                    "index": 41
                },
                {
                    "table": 0,
                    "index": 42
                },
                {
                    "table": 0,
                    "index": 43
                },
                {
                    "table": 0,
                    "index": 44
                }
            ]
        },
        "mapIcon": {
            "index": 6,
            "top": 0,
            "left": 0,
            "width": 150,
            "height": 225
        },
        "tutorialLink": null,
        "matchmakerTags": [],
        "website": {
            "table": 0,
            "index": 45
        }
    },
    "unknown_22": 0
}
```

### Decode s2mh and inline translation

> `$ s2mdecoder a1f3dfd0ceea4562e5045b6ebb0ad97f416308254c137c28455f55e6535c9f8b.s2mh 2177ce1bf9453f634457242b2b8758df5390e2c531732fb7e6fa027c8ba4a5c6.s2ml`

```json
{
    "instance": {
        "id": 289177,
        "version": 65568
    },
    "name": "ColdVoyage.SC2Map",
    "mapFile": {
        "type": "s2ma",
        "server": "us",
        "hash": "7067e8b25868263f1c2006c0722983114d026293779d60c738512308a7b4480c"
    },
    "mapNamespace": 362949,
    "mapInfo": {
        "name": "Ice Baneling Escape - Cold Voyage",
        "description": "Cold Voyage is a fan made map consisting of 27 new challenging levels and some new obstacles and challenges.",
        "thumbnail": {
            "index": 0,
            "top": 0,
            "left": 0,
            "width": 512,
            "height": 512
        },
        "maxPlayers": 10,
        "visualFiles": [
            {
                "type": "s2mv",
                "server": "us",
                "hash": "ab3f92a8e025b25fca4a8cc8c8736b0b3614c3dcc7875a5b6b3c94f391124a63"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "c50888599249b83e3ec4463cd8467279394839e11668f3cb28312a5545c706fd"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "b952eef72d5009bcaa153fde74511b3b4be5aff7671d03491e1f16b090b07a8f"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "47834a60f73bfaf9d857e10e9aee0596a4b90ba49a0b8b7f63e05c04b72b6d2a"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "61faf4c17b59e368b43693a218cb24af46bd6c7950d36fd1edab869a640f3283"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "d9e0f7b9756900581119faa3337563ffebc455e877c20b10ab0c8df5af14f870"
            },
            {
                "type": "s2mv",
                "server": "us",
                "hash": "d2e06878a567b7a4b1f6957bb75d40c6d356890fe0d498d41444da8c9dc19f4b"
            }
        ],
        "localeTable": [
            {
                "locale": "enUS",
                "stringTable": [
                    {
                        "type": "s2ml",
                        "server": "us",
                        "hash": "2177ce1bf9453f634457242b2b8758df5390e2c531732fb7e6fa027c8ba4a5c6"
                    }
                ]
            }
        ]
    },
    "definitions": [],
    "resultDefinitions": [],
    "localeTable": [
        {
            "locale": "enUS",
            "stringTable": [
                {
                    "type": "s2ml",
                    "server": "us",
                    "hash": "2177ce1bf9453f634457242b2b8758df5390e2c531732fb7e6fa027c8ba4a5c6"
                }
            ]
        }
    ],
    "mapSize": {
        "horizontal": 256,
        "vertical": 256
    },
    "tileset": "LIWE",
    "defaultVariantIndex": 0,
    "variants": [
        {
            "categoryName": "Other",
            "modeName": "Ice Escape",
            "categoryDescription": "Unclassified game type.",
            "modeDescription": "All settings may be customized.",
            "categoryId": 10,
            "achievementTags": [],
            "maxHumanPlayers": 10,
            "maxOpenSlots": 16
        }
    ],
    "dependencies": [
        {
            "id": 288191,
            "version": 0
        },
        {
            "id": 12,
            "version": 0
        }
    ],
    "unknown_15": 1,
    "licenses": [],
    "specialTags": [],
    "arcade": {
        "gameInfoScreenshots": [
            {
                "picture": {
                    "index": 1,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": null
            },
            {
                "picture": {
                    "index": 2,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": null
            },
            {
                "picture": {
                    "index": 3,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": null
            },
            {
                "picture": {
                    "index": 4,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": null
            },
            {
                "picture": {
                    "index": 5,
                    "top": 0,
                    "left": 0,
                    "width": 600,
                    "height": 800
                },
                "caption": null
            }
        ],
        "howToPlayScreenshots": [],
        "howToPlaySections": {
            "headers": [
                {
                    "title": "Basic Instructions",
                    "startOffset": 0,
                    "listType": 0,
                    "subtitle": null
                },
                {
                    "title": "How To Win",
                    "startOffset": 3,
                    "listType": 2,
                    "subtitle": null
                }
            ],
            "items": [
                "Learn first how to control your unit and how to make circles",
                "Click a lot for more precise control",
                "Try to save others to have more chances to beat the level",
                "Complete all levels to escape!"
            ]
        },
        "patchNoteSections": {
            "headers": [
                {
                    "title": "Version 1.25",
                    "startOffset": 0,
                    "listType": 2,
                    "subtitle": "October 16, 2017"
                },
                {
                    "title": "Version 1.26",
                    "startOffset": 4,
                    "listType": 2,
                    "subtitle": "October 27, 2017"
                },
                {
                    "title": "Version 1.31",
                    "startOffset": 6,
                    "listType": 2,
                    "subtitle": "November 9, 2017"
                },
                {
                    "title": "Version 1.32",
                    "startOffset": 9,
                    "listType": 2,
                    "subtitle": "November 12, 2017"
                },
                {
                    "title": "Version 1.34",
                    "startOffset": 11,
                    "listType": 2,
                    "subtitle": "November 22, 2017"
                }
            ],
            "items": [
                "- Skins should work now and 4 skins can be unlocked",
                "- Golden skin for beating extreme difficulty",
                "- Pink skin for beating normal mode while being the only human player in the game (A.I. allowed)",
                "- Poison skin & Flash skin in secrets",
                "- Bonus level now avainlable in normal mode",
                "- New skin avainlable for beating game with 2 players, A.I. not allowed",
                "Collect all 31 bonuses to unlock a skin!",
                null,
                "Kicking vote doesn't count the vote of the player that you are voting against.",
                "- Bonus level now available in extreme mode (skin reward)",
                "- Added portal in bonus level to make it faster to retry",
                "CV Mastery now available:",
                null,
                "    - Beat game on extreme fast difficulty ",
                "    - Have your best escape time under 15min",
                "    - Have your best time for each map total to be under 11min",
                "    - Work as a medic to collect over 2000 revives",
                "    - Collect at least 7 skins of your choice ",
                null,
                "Reward: Adaptive skin"
            ]
        },
        "mapIcon": {
            "index": 6,
            "top": 0,
            "left": 0,
            "width": 150,
            "height": 225
        },
        "tutorialLink": null,
        "matchmakerTags": [],
        "website": "http://discord.gg/cWdtANP"
    },
    "unknown_22": 0
}
```
