#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='s2mdecoder',
    version='0.1.0',
    author='Talv',
    url='https://github.com/SC2-Arcade-Watcher/s2m-decoder',
    packages=['s2mdecoder'],
    entry_points={
        'console_scripts': [
            's2mdecoder=s2mdecoder.main:main',
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        'sc2reader',
    ],
)
