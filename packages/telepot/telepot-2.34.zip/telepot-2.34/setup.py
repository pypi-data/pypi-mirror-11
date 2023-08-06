from setuptools import setup, find_packages
from os import path
import sys

PY_34 = sys.version_info >= (3,4)

install_requires = ['requests']

if PY_34:
    install_requires += ['aiohttp']


here = path.abspath(path.dirname(__file__))

try:
    with open(path.join(here, 'pypi.rst')) as f:
        long_description = f.read()
except:
    long_description = ''


setup(
    name='telepot',
    packages=['telepot'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=install_requires,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='2.34',

    description='Python wrapper for Telegram Bot API',

    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/nickoala/telepot',

    # Author details
    author='Nick Lee',
    author_email='lee1nick@yahoo.ca',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='telegram bot api python wrapper',
)
