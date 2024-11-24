from setuptools import setup

APP = ['just_decrypt.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['cryptography', 'os', 'tkinter'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
