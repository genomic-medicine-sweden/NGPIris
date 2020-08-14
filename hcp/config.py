import os

from configparser import ConfigParser


def get_config():
    config = ConfigParser()
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(root_path, 'config.ini')
    config.read(config_path)

    return config
