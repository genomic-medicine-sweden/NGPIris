#!/usr/bin/env python
from HCPinterface import version
from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

setup(
    name="HCPinterface",
    version=version,
    long_description=__doc__,
    url="https://github.com/genomic-medicine-sweden/HCPinterface",
    author="Isak Sylvin",
    author_email="isak.sylvin@gu.se",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["hcpi=HCPinterface.cli.base:root"],
    },
)
