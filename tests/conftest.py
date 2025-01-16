
from pytest import Config, fixture, UsageError
from configparser import ConfigParser
from typing import Any, Generator
from shutil import rmtree

from NGPIris.hcp import HCPHandler

class CustomConfig:
    """A typed wrapper around pytest.Config for dynamic attributes."""
    def __init__(self, pytest_config : Config):
        self._config = pytest_config

    @property
    def hcp_h(self) -> HCPHandler:
        """Access the HCPHandler instance."""
        return getattr(self._config, "hcp_h")

    def __getattr__(self, name : str) -> Any:
        """Dynamically get attributes set during pytest configuration."""
        return getattr(self._config, name)

def set_section(config : Config, parser : ConfigParser, section : str) -> None:
    parse_dict = dict(parser.items(section))
    for k, v in parse_dict.items():
        setattr(config, k, v)  # Adds attributes dynamically to pytest.Config

def pytest_addoption(parser) -> None:
    parser.addoption(
        "--config",
        action="store",
        default=None,
        help="Path to the configuration file (e.g., path/to/config.ini)",
    )

def pytest_configure(config : Config) -> None:
    config_path = config.getoption("--config")
    if not config_path:
        raise UsageError("--config argument is required.")
    else:
        parser = ConfigParser()
        parser.read(str(config_path))

        # Add the INI parser to config
        setattr(config, "parser", parser)

        # Dynamically add an HCPHandler instance to config
        setattr(config, "hcp_h", HCPHandler(parser.get("General", "credentials_path")))

        # Dynamically add all key-value pairs from "HCP_tests" section
        set_section(config, parser, "HCP_tests")

@fixture(scope = "session")
def hcp_result_path(pytestconfig : Config) -> str:
    return pytestconfig.parser.get("HCP_tests", "result_path") # type: ignore

@fixture(scope = "session", autouse = True)
def clean_up_after_tests(hcp_result_path : str) -> Generator[None, Any, None]:
    # Setup code can go here if needed
    yield
    # Teardown code
    rmtree(hcp_result_path)

@fixture
def custom_config(pytestconfig : Config) -> CustomConfig:
    """Provide the typed wrapper for pytest.Config."""
    return CustomConfig(pytestconfig)
