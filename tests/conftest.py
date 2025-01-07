
from pytest import FixtureRequest, fixture, UsageError, Config
from configparser import ConfigParser
from NGPIris.hcp import HCPHandler

def set_section(config : Config, parser : ConfigParser, section : str):
    parse_dict = dict(parser.items(section))
    for k, v in parse_dict.items():
        setattr(config, k, v)


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

        setattr(config, "hcp_h", HCPHandler(parser.get("General", "credentials_path")))
        set_section(config, parser, "HCP_tests")
        
@fixture(scope = "session")
def get_ini_config(request : FixtureRequest):
    config_path = request.config.getoption("--config")
    if not config_path:
        raise UsageError("--config argument is required.")
    else:
        parser = ConfigParser()
        parser.read(str(config_path))
        return parser

