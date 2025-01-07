
from pytest import fixture, UsageError, Config
from configparser import ConfigParser
from NGPIris.hcp import HCPHandler
from typing import Any

def set_section(config : Config, parser : ConfigParser, section : str):
    parse_dict = dict(parser.items(section))
    for k, v in parse_dict.items():
        setattr(config, k, v)

class DynamicConfig(Config):
    def __init__(self, config: Config):
        self._config = config  # Store the original pytest Config object

    def __getattr__(self, name: str) -> Any:
        # Provide default behavior for dynamic attributes
        try:
            return super().__getattribute__(name)
        except AttributeError:
            raise AttributeError(type(self).__name__ + " object has no attribute " + name)

def pytest_addoption(parser):
    parser.addoption(
        "--config",
        action="store",
        default=None,
        help="Path to the configuration file (e.g., path/to/config.ini)"
    )

def pytest_configure(config : Config):
    config_path = config.getoption("--config")
    if not config_path:
        raise UsageError("--config argument is required.")
    else:
        parser = ConfigParser()
        parser.read(str(config_path))

        dynamic_config = DynamicConfig(config)

        setattr(dynamic_config, "hcp_h", HCPHandler(parser.get("General", "credentials_path")))
        set_section(dynamic_config, parser, "HCP_tests")
        
@fixture
def dynamic_config(pytestconfig : Config) -> DynamicConfig:
    return DynamicConfig(pytestconfig)