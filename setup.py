from setuptools import setup
from make_icons import make_iconset

VERSION = '0.1.0'
APP = ['blinkblink.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'iconfile': make_iconset('icon.png', 'blinkblink.iconset')
}

setup(
    name='blinkblink',
    description='macOS app reminding to take breaks from the screen',
    version=VERSION,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
