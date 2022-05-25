import logging
import os
import urllib3

from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warnings about missing SLL certificate.

logformat =  logging.Formatter("[%(asctime)s] - %(levelname)s: %(message)s")

# File work directory
WD = os.path.dirname(os.path.realpath(__file__))
TIMESTAMP = datetime.now().strftime("%y%m%d-%H%M%S")

# Initialize log
log = logging.getLogger("main_log")
log.setLevel(logging.DEBUG)
#Streamlog
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logformat)
log.addHandler(ch)
