# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sl2gtfs',
    version='1.0.0',
    description='Converts SL stop ids to GTFS stop ids',
    long_description=long_description,
    url='https://github.com/johannilsson/sl2gtfs',
    author='Johan Nilsson',
    author_email='johan@markupartist.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    keywords='gtfs stockholm',
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'sl2gtfs=sl2gtfs:main',
        ],
    },
)