
from typing import Callable

from pytest import Config
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree
from filecmp import cmp

# --------------------------- Helper fucntions ---------------------------------

#def _get_hcp_handler(config_parser : ConfigParser) -> HCPHandler:
#    return HCPHandler(config_parser.get("General", "credentials_path"))

def _get_all_config(config_parser : ConfigParser) -> dict:
    return dict(config_parser.items("HCP_tests"))

#def _get_test_bucket(config_parser : ConfigParser) -> str:
#    return config_parser.get("hcp_tests", "bucket")
#
#def _get_test_file_path(config_parser : ConfigParser) -> str:
#    return config_parser.get("hcp_tests","data_test_file")

def _without_mounting(test : Callable) -> None:
    try:
        test()
    except:
        assert True
    else: # pragma: no cover
        assert False

# --------------------------- Test suite ---------------------------------------

def test_list_buckets(pytestconfig : Config) -> None:
    assert pytestconfig.hcp_h.list_buckets() # type: ignore

def test_mount_bucket(pytestconfig : Config) -> None:
    pytestconfig.hcp_h.mount_bucket(pytestconfig.test_bucket) # type: ignore

def test_mount_nonexisting_bucket(pytestconfig : Config) -> None:
    try:
        pytestconfig.hcp_h.mount_bucket("aBucketThatDoesNotExist") # type: ignore
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_test_connection(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.test_connection() # type: ignore

def test_test_connection_with_bucket_name(pytestconfig : Config) -> None:
    pytestconfig.hcp_h.test_connection(bucket_name = pytestconfig.test_bucket) # type: ignore

def test_test_connection_without_mounting_bucket(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    try:
        _hcp_h.test_connection()
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_list_objects(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    assert type(list(pytestconfig.hcp_h.list_objects())) == list # type: ignore

def test_list_objects_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.list_objects)

def test_upload_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.upload_file(pytestconfig.test_file_path) # type: ignore

def test_upload_file_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.upload_file)

def test_upload_file_in_sub_directory(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.upload_file(pytestconfig.test_file_path, "a_sub_directory/a_file") # type: ignore

def test_upload_nonexistent_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    try: 
        pytestconfig.hcp_h.upload_file("tests/data/aTestFileThatDoesNotExist") # type: ignore
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_upload_folder(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.upload_folder("tests/data/a folder of data/", "a folder of data/") # type: ignore

def test_upload_folder_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.upload_folder)

def test_upload_nonexisting_folder(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    try: 
        pytestconfig.hcp_h.upload_folder("tests/data/aFolderOfFilesThatDoesNotExist") # type: ignore
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_get_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    assert pytestconfig.hcp_h.object_exists("a_sub_directory/a_file") # type: ignore
    assert pytestconfig.hcp_h.get_object("a_sub_directory/a_file") # type: ignore

def test_get_folder_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.object_exists)
    _without_mounting(_hcp_h.get_object)

def test_get_file_in_sub_directory(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    test_file = Path(pytestconfig.test_file_path).name # type: ignore
    assert pytestconfig.hcp_h.object_exists(test_file) # type: ignore
    assert pytestconfig.hcp_h.get_object(test_file) # type: ignore

def test_download_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    Path(pytestconfig.result_path).mkdir() # type: ignore
    test_file = Path(pytestconfig.test_file_path).name # type: ignore
    pytestconfig.hcp_h.download_file(test_file, pytestconfig.result_path + test_file) # type: ignore
    assert cmp(pytestconfig.result_path + test_file, pytestconfig.test_file_path) # type: ignore

def test_download_file_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.download_file)

def test_download_nonexistent_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    try:
        pytestconfig.hcp_h.download_file("aFileThatDoesNotExist", pytestconfig.result_path + "aFileThatDoesNotExist") # type: ignore
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_download_folder(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.download_folder("a folder of data/", pytestconfig.result_path) # type: ignore

def test_search_objects_in_bucket(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    test_file = Path(pytestconfig.test_file_path).name # type: ignore
    pytestconfig.hcp_h.search_objects_in_bucket(test_file) # type: ignore

def test_search_objects_in_bucket_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.search_objects_in_bucket)

def test_get_object_acl(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    test_file = Path(pytestconfig.test_file_path).name # type: ignore
    pytestconfig.hcp_h.get_object_acl(test_file) # type: ignore

def test_get_object_acl_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.get_object_acl)

def test_get_bucket_acl(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.get_bucket_acl() # type: ignore

def test_get_bucket_acl_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.get_bucket_acl)

#def test_modify_single_object_acl(pytestconfig : Config) -> None:
#    test_mount_bucket(pytestconfig)
#    pytestconfig.hcp_h.modify_single_object_acl()
#
#def test_modify_single_bucket_acl(pytestconfig : Config) -> None:
#    test_mount_bucket(pytestconfig)
#    pytestconfig.hcp_h.modify_single_bucket_acl()
#
#def test_modify_object_acl(pytestconfig : Config) -> None:
#    test_mount_bucket(pytestconfig)
#    pytestconfig.hcp_h.modify_object_acl()
#
#def test_modify_bucket_acl(pytestconfig : Config) -> None:
#    test_mount_bucket(pytestconfig)
#    pytestconfig.hcp_h.modify_bucket_acl()

def test_delete_file(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    test_file = Path(pytestconfig.test_file_path).name # type: ignore
    pytestconfig.hcp_h.delete_object(test_file) # type: ignore
    pytestconfig.hcp_h.delete_object("a_sub_directory/a_file") # type: ignore
    pytestconfig.hcp_h.delete_object("a_sub_directory") # type: ignore

def test_delete_file_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.delete_object)

def test_delete_folder_with_sub_directory(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.upload_file(pytestconfig.test_file_path, "a folder of data/a sub dir/a file") # type: ignore
    try:
        pytestconfig.hcp_h.delete_folder("a folder of data/") # type: ignore
    except: 
        assert True
    else: # pragma: no cover 
        assert False
    pytestconfig.hcp_h.delete_folder("a folder of data/a sub dir/") # type: ignore

def test_delete_folder(pytestconfig : Config) -> None:
    test_mount_bucket(pytestconfig)
    pytestconfig.hcp_h.delete_folder("a folder of data/") # type: ignore

def test_delete_folder_without_mounting(pytestconfig : Config) -> None:
    _hcp_h = pytestconfig.hcp_h # type: ignore
    _without_mounting(_hcp_h.delete_folder)

def test_delete_nonexistent_files(pytestconfig : Config) -> None:
    pytestconfig.hcp_h.delete_objects(["some", "files", "that", "does", "not", "exist"]) # type: ignore

def test_clean_up(pytestconfig : Config) -> None:
    rmtree(pytestconfig.result_path) # type: ignore