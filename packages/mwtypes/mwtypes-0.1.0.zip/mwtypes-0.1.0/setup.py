from distutils.core import setup

from setuptools import find_packages

setup(
    name='mwtypes',
    version="0.1.0",
    author='Aaron Halfaker',
    author_email='aaron.halfaker@gmail.com',
    packages=find_packages(),
    url='https://github.com/halfak/mwtypes',
    license=open('LICENSE').read(),
    description='A set of types for processing MediaWiki data.',
    long_description=open('README.md').read(),
    install_requires=[],
    test_suite='nose.collector',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering"
    ],
)
