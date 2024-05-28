
from NGPIris.hci import HCIHandler
from random import randint
from json import load, dump

hci_h = HCIHandler("credentials/testCredentials.json")
hci_h.request_token()

def test_list_index_names_type() -> None:
    list_of_indexes = hci_h.list_index_names()
    assert type(list_of_indexes) is list

def test_look_up_all_indexes() -> None:
    list_of_indexes = hci_h.list_index_names()
    for index in list_of_indexes:
        assert hci_h.look_up_index(index)

def test_fail_index_look_up() -> None:
    assert not hci_h.look_up_index("anIndexThatDoesNotExist")
    
def test_make_simple_raw_query() -> None:
    list_of_indexes = hci_h.list_index_names()
    arbitrary_index = list_of_indexes[randint(0, len(list_of_indexes) - 1)]
    query = {
        "indexName" : arbitrary_index
    }
    result = hci_h.raw_query(query)
    assert result["indexName"] == arbitrary_index

def test_make_simple_raw_query_from_JSON() -> None:
    list_of_indexes = hci_h.list_index_names()
    arbitrary_index = list_of_indexes[randint(0, len(list_of_indexes) - 1)]
    path = "tests/data/json_test_query.json"
    with open(path, "r") as f1:
        query : dict = load(f1)
        query["indexName"] = arbitrary_index
        with open(path, "w") as f2:
            dump(query, f2, indent = 4)
    result = hci_h.raw_query_from_JSON(path)
    assert result["indexName"] == arbitrary_index

def test_prettify_raw_query() -> None:
    list_of_indexes = hci_h.list_index_names()
    arbitrary_index = list_of_indexes[randint(0, len(list_of_indexes) - 1)]
    query = {
        "indexName" : arbitrary_index
    }
    result = hci_h.raw_query(query)
    df = hci_h.prettify_raw_query(result)
    assert type(df.to_dict("list")) == dict