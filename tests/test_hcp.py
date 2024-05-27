
from NGPIris2.hcp import HCPHandler
from configparser import ConfigParser
from os import mkdir, rmdir, remove
from filecmp import cmp

hcp_h = HCPHandler("credentials/testCredentials.json")

ini_config = ConfigParser()
ini_config.read("tests/test_conf.ini")

test_bucket = ini_config.get("hcp_tests", "bucket")

test_file = ini_config.get("hcp_tests","data_test_file")
test_file_path = "tests/data/" + test_file

result_path = "tests/data/results/"

def test_list_buckets() -> None:
    assert hcp_h.list_buckets()

def test_mount_bucket() -> None:
    hcp_h.mount_bucket(test_bucket)

def test_upload_file() -> None:
    test_mount_bucket()
    hcp_h.upload_file(test_file_path)

def test_get_file() -> None:
    test_mount_bucket()
    assert hcp_h.get_object(test_file)

def test_download_file() -> None:
    test_mount_bucket()
    mkdir(result_path)
    hcp_h.download_file(test_file, result_path + test_file)
    assert cmp(result_path + test_file, test_file_path)

def test_delete_file() -> None:
    test_mount_bucket()
    hcp_h.delete_object(test_file)

def test_clean_up() -> None:
    remove(result_path + test_file)
    rmdir(result_path)