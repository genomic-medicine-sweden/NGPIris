from HCPInterface import WD
from HCPInterface.hcp import HCPManager
import pdb

#pdb.set_trace()
print(f"WD at {WD}")
hcpm = HCPManager(credentials_path="./credentials.json",bucket="ngs-test")
hcpm.test_connection()
print("Connection is working fine!")
