
from typing import Callable

from pytest import Config
from configparser import ConfigParser
from pathlib import Path
from shutil import rmtree
from filecmp import cmp

from conftest import DynamicConfig

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

def test_list_buckets(dynamic_config : DynamicConfig) -> None:
    assert dynamic_config.hcp_h.list_buckets() 

def test_mount_bucket(dynamic_config : DynamicConfig) -> None:
    dynamic_config.hcp_h.mount_bucket(dynamic_config.test_bucket) 

def test_mount_nonexisting_bucket(dynamic_config : DynamicConfig) -> None:
    try:
        dynamic_config.hcp_h.mount_bucket("aBucketThatDoesNotExist") 
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_test_connection(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.test_connection() 

def test_test_connection_with_bucket_name(dynamic_config : DynamicConfig) -> None:
    dynamic_config.hcp_h.test_connection(bucket_name = dynamic_config.test_bucket) 

def test_test_connection_without_mounting_bucket(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    try:
        _hcp_h.test_connection()
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_list_objects(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    assert type(list(dynamic_config.hcp_h.list_objects())) == list 

def test_list_objects_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.list_objects)

def test_upload_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.upload_file(dynamic_config.test_file_path) 

def test_upload_file_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.upload_file)

def test_upload_file_in_sub_directory(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.upload_file(dynamic_config.test_file_path, "a_sub_directory/a_file") 

def test_upload_nonexistent_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    try: 
        dynamic_config.hcp_h.upload_file("tests/data/aTestFileThatDoesNotExist") 
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_upload_folder(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.upload_folder("tests/data/a folder of data/", "a folder of data/") 

def test_upload_folder_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.upload_folder)

def test_upload_nonexisting_folder(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    try: 
        dynamic_config.hcp_h.upload_folder("tests/data/aFolderOfFilesThatDoesNotExist") 
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_get_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    assert dynamic_config.hcp_h.object_exists("a_sub_directory/a_file") 
    assert dynamic_config.hcp_h.get_object("a_sub_directory/a_file") 

def test_get_folder_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.object_exists)
    _without_mounting(_hcp_h.get_object)

def test_get_file_in_sub_directory(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    test_file = Path(dynamic_config.test_file_path).name 
    assert dynamic_config.hcp_h.object_exists(test_file) 
    assert dynamic_config.hcp_h.get_object(test_file) 

def test_download_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    Path(dynamic_config.result_path).mkdir() 
    test_file = Path(dynamic_config.test_file_path).name 
    dynamic_config.hcp_h.download_file(test_file, dynamic_config.result_path + test_file) 
    assert cmp(dynamic_config.result_path + test_file, dynamic_config.test_file_path) 

def test_download_file_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.download_file)

def test_download_nonexistent_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    try:
        dynamic_config.hcp_h.download_file("aFileThatDoesNotExist", dynamic_config.result_path + "aFileThatDoesNotExist") 
    except:
        assert True
    else: # pragma: no cover
        assert False

def test_download_folder(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.download_folder("a folder of data/", dynamic_config.result_path) 

def test_search_objects_in_bucket(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    test_file = Path(dynamic_config.test_file_path).name 
    dynamic_config.hcp_h.search_objects_in_bucket(test_file) 

def test_search_objects_in_bucket_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.search_objects_in_bucket)

def test_get_object_acl(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    test_file = Path(dynamic_config.test_file_path).name 
    dynamic_config.hcp_h.get_object_acl(test_file) 

def test_get_object_acl_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.get_object_acl)

def test_get_bucket_acl(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.get_bucket_acl() 

def test_get_bucket_acl_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.get_bucket_acl)

#def test_modify_single_object_acl(dynamic_config : DynamicConfig) -> None:
#    test_mount_bucket(dynamic_config)
#    dynamic_config.hcp_h.modify_single_object_acl()
#
#def test_modify_single_bucket_acl(dynamic_config : DynamicConfig) -> None:
#    test_mount_bucket(dynamic_config)
#    dynamic_config.hcp_h.modify_single_bucket_acl()
#
#def test_modify_object_acl(dynamic_config : DynamicConfig) -> None:
#    test_mount_bucket(dynamic_config)
#    dynamic_config.hcp_h.modify_object_acl()
#
#def test_modify_bucket_acl(dynamic_config : DynamicConfig) -> None:
#    test_mount_bucket(dynamic_config)
#    dynamic_config.hcp_h.modify_bucket_acl()

def test_delete_file(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    test_file = Path(dynamic_config.test_file_path).name 
    dynamic_config.hcp_h.delete_object(test_file) 
    dynamic_config.hcp_h.delete_object("a_sub_directory/a_file") 
    dynamic_config.hcp_h.delete_object("a_sub_directory") 

def test_delete_file_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.delete_object)

def test_delete_folder_with_sub_directory(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.upload_file(dynamic_config.test_file_path, "a folder of data/a sub dir/a file") 
    try:
        dynamic_config.hcp_h.delete_folder("a folder of data/") 
    except: 
        assert True
    else: # pragma: no cover 
        assert False
    dynamic_config.hcp_h.delete_folder("a folder of data/a sub dir/") 

def test_delete_folder(dynamic_config : DynamicConfig) -> None:
    test_mount_bucket(dynamic_config)
    dynamic_config.hcp_h.delete_folder("a folder of data/") 

def test_delete_folder_without_mounting(dynamic_config : DynamicConfig) -> None:
    _hcp_h = dynamic_config.hcp_h 
    _without_mounting(_hcp_h.delete_folder)

def test_delete_nonexistent_files(dynamic_config : DynamicConfig) -> None:
    dynamic_config.hcp_h.delete_objects(["some", "files", "that", "does", "not", "exist"]) 

def test_clean_up(dynamic_config : DynamicConfig) -> None:
    rmtree(dynamic_config.result_path) 