#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

try:
    ver = __import__('HCPInterface').version
except ImportError:
    ver = '1.0.0'

setup(
    name="HCPInterface",
    version=ver,
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/genomic-medicine-sweden/HCPInterface",
    author="Isak Sylvin",
    author_email="isak.sylvin@gu.se",
    project_urls={
        "Bug Tracker": "https://github.com/genomic-medicine-sweden/HCPInterface/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["hcpi=HCPInterface.cli.base:root"],
    },
)
