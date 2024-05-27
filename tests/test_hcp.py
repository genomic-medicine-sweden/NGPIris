
from NGPIris2.hcp import HCPHandler
from configparser import ConfigParser

hcp_h = HCPHandler("credentials/testCredentials.json")

ini_config = ConfigParser()
ini_config.read("tests/test_conf.ini")

test_bucket = ini_config.get("hcp_tests", "bucket")

def test_list_buckets() -> None:
    assert hcp_h.list_buckets()

def test_mount_bucket() -> None:
    assert hcp_h.mount_bucket(test_bucket)

def test_upload_file():
    test_file = ini_config.get("hcp_tests","datapath")
    test_file_path = test_file.replace(".", "/")
    assert hcp_h.upload_file(test_file_path)
