from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        install_requires : list[str] = [x.strip() for x in f.readlines()]
except IOError:
    install_requires : list[str] = []

setup(
    name='NGPIris2',
    version='0.0.1',
    install_requires=install_requires,
    packages = find_packages()
)