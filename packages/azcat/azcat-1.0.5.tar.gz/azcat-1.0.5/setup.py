from setuptools import setup, find_packages
import os
import sys

requires = open("requirements.txt").read().split("\n")
readme = open("README.rst").read()

setup(
    name="azcat",
    version="1.0.5",
    description="A alternative to cat(1); specialized for printing files",
    long_description=readme,
    author="Seiya Nuta",
    author_email="nuta@seiya.me",
    url="http://github.com/nuta/azcat",
    packages=find_packages(),
    scripts=["az"],
    install_requires=requires,
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: Public Domain",
        "Operating System :: POSIX",
        "Topic :: Utilities"
    ]
)
