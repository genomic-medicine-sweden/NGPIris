import os

from configparser import ConfigParser
from HCPInterface import WD

from distutils.sysconfig import get_python_lib

def get_config():
    config = ConfigParser()

    installed = False
    for entry in os.listdir(get_python_lib()):
        if 'HCPInterface-' in entry:
             installed = True
             break

    if installed:
        #Also works but req conda
        #config_path= os.path.join(os.path.expandvars("$CONDA_PREFIX"), "config.ini")

        #pip show HCPInterface
        #Backpedals all the way to the env folder
        config_path = os.path.join(WD, '..', '..', '..', '..', 'config', 'config.ini')

    else:
        config_path = os.path.join(WD, '..', 'config.ini')
  
    config.read(config_path)

    return config
