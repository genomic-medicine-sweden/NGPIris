from tomllib import load
from packaging.version import Version
from NGPIris.cli.exceptions import TooOutdatedVersion

def checkversion():
    with open("pyproject.toml", "rb") as pyproject:
        pyproject_dict = load(pyproject)
        version = Version(pyproject_dict["project"]["version"])
        least_viable_version = Version(pyproject_dict["tool"]["NGPIris"]["least_viable_version"])
        if version < least_viable_version:
            raise TooOutdatedVersion("Your version of IRIS (" + str(version) + ") is less than the least viable version (" + str(least_viable_version) + ")")