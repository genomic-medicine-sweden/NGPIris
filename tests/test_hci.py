from random import randint
from typing import TYPE_CHECKING

from pytest import fail  # noqa: PT013

if TYPE_CHECKING:
    from conftest import CustomConfig

# ruff: noqa: S101, INP001, D103, E722, PT016


def test_list_index_names_type(custom_config: CustomConfig) -> None:
    list_of_indexes = custom_config.hci_h.list_index_names()
    assert type(list_of_indexes) is list


def test_look_up_all_indexes(custom_config: CustomConfig) -> None:
    list_of_indexes = custom_config.hci_h.list_index_names()
    for index in list_of_indexes:
        assert custom_config.hci_h.look_up_index(index)


def test_fail_index_look_up(custom_config: CustomConfig) -> None:
    assert not custom_config.hci_h.look_up_index("anIndexThatDoesNotExist")


def test_make_simple_query(custom_config: CustomConfig) -> None:
    list_of_indexes = custom_config.hci_h.list_index_names()
    arbitrary_index = list_of_indexes[randint(0, len(list_of_indexes) - 1)]  # noqa: S311
    result = custom_config.hci_h.query(
        {
            "indexName": arbitrary_index,
        },
    )
    assert result["indexName"] == arbitrary_index


def test_fail_query(custom_config: CustomConfig) -> None:
    query = {}
    try:
        custom_config.hci_h.query(query)  # pyright: ignore[reportArgumentType]
    except:
        assert True
    else:  # pragma: no cover
        fail()


def test_make_query(custom_config: CustomConfig) -> None:
    custom_config.hci_h.query({"indexName": custom_config.test_index})


def test_make_query_with_query_string(custom_config: CustomConfig) -> None:
    custom_config.hci_h.query(
        {
            "indexName": custom_config.test_index,
            "queryString": custom_config.query_string,
        }
    )


# TODO(EB): Add more and better tests
