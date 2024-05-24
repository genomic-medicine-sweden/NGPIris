
from NGPIris2.hci import HCIHandler
from random import randint

hci_h = HCIHandler("credentials/testCredentials.json")
hci_h.request_token()

def test_list_index_names_type() -> None:
    list_of_indexes = hci_h.list_index_names()
    assert type(list_of_indexes) is list

def test_look_up_all_indexes() -> None:
    list_of_indexes = hci_h.list_index_names()
    for index in list_of_indexes:
        assert hci_h.look_up_index(index)

def test_make_simple_raw_query() -> None:
    list_of_indexes = hci_h.list_index_names()
    arbitrary_index = list_of_indexes[randint(0, len(list_of_indexes) - 1)]
    query = {
        "indexName" : arbitrary_index
    }
    result = hci_h.raw_query(query)
    assert result["indexName"] == arbitrary_index