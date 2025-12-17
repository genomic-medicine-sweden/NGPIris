from collections.abc import Callable
from filecmp import cmp
from pathlib import Path
from typing import Any

from conftest import CustomConfig
from icecream import ic
from pytest import fail

from NGPIris import HCPHandler

# ruff: noqa: S101, D103, E722, PT013, INP001

# --------------------------- Constants ---------------------------

SUBDIR = "a_sub_directory"

# --------------------------- Helper functions ---------------------------------


def _without_mounting(
    hcp_h: HCPHandler,
    hcp_h_method: Callable[..., Any],
) -> None:
    hcp_h.bucket_name = None
    try:
        hcp_h_method(hcp_h)
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")


# --------------------------- Test suite ---------------------------------------


# ---------------------------- User methods tests ----------------------------
# get_users
def test_get_users(custom_config: CustomConfig) -> None:
    assert isinstance(custom_config.hcp_h.get_users(), list)


# get_user_roles
def test_get_user_roles(custom_config: CustomConfig) -> None:
    user = custom_config.hcp_h.get_users()[0]
    assert isinstance(custom_config.hcp_h.get_user_roles(user), list)


# is_user_admin
def test_is_user_admin(custom_config: CustomConfig) -> None:
    user = custom_config.hcp_h.get_users()[0]
    is_admin = custom_config.hcp_h.is_user_admin(user)
    is_not_admin = not is_admin

    # This assertion might look silly, but the point of the test is to retrieve
    # the information about admin status itself not what status the user has
    assert is_admin or is_not_admin


# ---------------------------- Util methods tests ----------------------------
# test_connection
def test_test_connection(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    assert custom_config.hcp_h.test_connection(
        bucket_name=custom_config.test_bucket
    )


def test_test_connection_without_mounting_bucket(
    custom_config: CustomConfig,
) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.test_connection)


# ---------------------------- Bucket methods tests ----------------------------
# mount_bucket
def test_mount_bucket(custom_config: CustomConfig) -> None:
    custom_config.hcp_h.mount_bucket(custom_config.test_bucket)


def test_mount_nonexisting_bucket(custom_config: CustomConfig) -> None:
    try:
        custom_config.hcp_h.mount_bucket("aBucketThatDoesNotExist")
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")


# create_bucket
def test_create_bucket(custom_config: CustomConfig) -> None:
    custom_config.hcp_h.create_bucket(custom_config.test_bucket + "2")


# delete_bucket
def test_delete_bucket(custom_config: CustomConfig) -> None:
    custom_config.hcp_h.delete_bucket(custom_config.test_bucket + "2")


# list_buckets
def test_list_buckets(custom_config: CustomConfig) -> None:
    assert custom_config.hcp_h.list_buckets()


# ---------------------------- Object methods tests ----------------------------
# list_objects
def test_list_objects(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    assert isinstance(list(custom_config.hcp_h.list_objects()), list)


def test_list_objects_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.list_objects)


# upload_file
def test_upload_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)

    # With progress bar
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.delete_object(custom_config.test_file_path)

    # Without progress bar
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path + "_no_progress_bar",
        show_progress_bar=False,
    )

    custom_config.hcp_h.delete_object(
        custom_config.test_file_path + "_no_progress_bar"
    )

    # Test every upload mode
    for mode in HCPHandler.UploadMode:
        key = custom_config.test_file_path + "_" + str(mode).replace(".", "_")
        ic(
            mode,
            key,
        )
        custom_config.hcp_h.upload_file(
            custom_config.test_file_path,
            key,
            upload_mode=mode,
        )
        custom_config.hcp_h.delete_object(key)


def test_upload_file_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.upload_file)


def test_upload_file_in_sub_directory(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        SUBDIR + "/a_file",
    )
    custom_config.hcp_h.delete_object(SUBDIR + "/a_file")


def test_upload_nonexistent_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    try:
        custom_config.hcp_h.upload_file("tests/data/aTestFileThatDoesNotExist")
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")


# upload_folder
def test_upload_folder(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_folder(
        custom_config.test_folder_path,
        custom_config.test_folder_path,
    )
    custom_config.hcp_h.delete_folder(custom_config.test_folder_path)


def test_upload_folder_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.upload_folder)


def test_upload_nonexisting_folder(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    try:
        custom_config.hcp_h.upload_folder(
            "tests/data/aFolderOfFilesThatDoesNotExist",
        )
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")


# get_object
def test_get_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )
    assert custom_config.hcp_h.get_object(custom_config.test_file_path)
    custom_config.hcp_h.delete_object(custom_config.test_file_path)


def test_get_file_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.get_object)


# object_exists
def test_object_exists(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )
    assert custom_config.hcp_h.object_exists(custom_config.test_file_path)
    custom_config.hcp_h.delete_object(custom_config.test_file_path)


def test_object_exists_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.object_exists)


# download_file
def test_download_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)

    # With progress bar
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.download_file(
        custom_config.test_file_path,
        custom_config.result_path + custom_config.test_file_path,
    )
    assert cmp(
        custom_config.result_path + custom_config.test_file_path,
        custom_config.test_file_path,
    )

    # Without progress bar
    custom_config.hcp_h.download_file(
        custom_config.test_file_path + "_no_progress_bar",
        custom_config.result_path
        + custom_config.test_file_path
        + "_no_progress_bar",
        show_progress_bar=False,
    )
    assert cmp(
        custom_config.result_path + custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.delete_object(custom_config.test_file_path)


def test_download_file_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.download_file)


def test_download_nonexistent_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    try:
        custom_config.hcp_h.download_file(
            "aFileThatDoesNotExist",
            custom_config.result_path + "aFileThatDoesNotExist",
        )
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")


# download_folder
def test_download_folder(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_folder(
        custom_config.test_folder_path,
        custom_config.test_folder_path,
    )
    custom_config.hcp_h.download_folder(
        custom_config.test_folder_path,
        custom_config.result_path,
    )
    custom_config.hcp_h.delete_folder(custom_config.test_folder_path)


# delete_objects
def test_delete_nonexistent_files(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.delete_objects(
        ["some", "files", "that", "does", "not", "exist"],
    )


# delete_object
def test_delete_object(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )
    custom_config.hcp_h.delete_object(custom_config.test_file_path)


def test_delete_object_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.delete_object)


# delete_folder
def test_delete_folder(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_folder(
        custom_config.test_folder_path,
        custom_config.test_folder_path,
    )
    custom_config.hcp_h.delete_folder(custom_config.test_folder_path)


def test_delete_folder_with_sub_directory(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        SUBDIR + "/another_dir/a_new_file",
    )
    try:
        custom_config.hcp_h.delete_folder(SUBDIR)
    except:
        assert True
    else:  # pragma: no cover
        fail("Test failed")
    custom_config.hcp_h.delete_folder(SUBDIR + "/another_dir/a_new_file")
    custom_config.hcp_h.delete_folder(SUBDIR)


def test_delete_folder_without_mounting(custom_config: CustomConfig) -> None:
    _hcp_h = custom_config.hcp_h
    _without_mounting(_hcp_h, HCPHandler.delete_folder)


# copy_file
def test_copy_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )
    custom_config.hcp_h.copy_file(
        custom_config.test_file_path, custom_config.test_file_path + "_copy"
    )
    custom_config.hcp_h.delete_object(custom_config.test_file_path)


def test_copy_file_to_other_bucket(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.create_bucket("TempBucket")
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.copy_file(
        custom_config.test_file_path,
        custom_config.test_file_path + "_copy",
        "TempBucket",
    )
    custom_config.hcp_h.delete_object(custom_config.test_file_path)

    custom_config.hcp_h.mount_bucket("TempBucket")
    custom_config.hcp_h.delete_object(custom_config.test_file_path + "_copy")
    custom_config.hcp_h.delete_bucket("TempBucket")


# move_file
def test_move_file(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.move_file(
        custom_config.test_file_path, custom_config.test_file_path + "_moved"
    )

    custom_config.hcp_h.delete_object(custom_config.test_file_path + "_moved")


def test_move_file_to_other_bucket(custom_config: CustomConfig) -> None:
    test_mount_bucket(custom_config)
    custom_config.hcp_h.create_bucket("TempBucket")
    custom_config.hcp_h.upload_file(
        custom_config.test_file_path,
        custom_config.test_file_path,
    )

    custom_config.hcp_h.move_file(
        custom_config.test_file_path,
        custom_config.test_file_path + "_moved",
        "TempBucket",
    )

    custom_config.hcp_h.mount_bucket("TempBucket")
    custom_config.hcp_h.delete_object(custom_config.test_file_path + "_moved")
    custom_config.hcp_h.delete_bucket("TempBucket")


# ---------------------------- Search methods tests ----------------------------
# N/A
