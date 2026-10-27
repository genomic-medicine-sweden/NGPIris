from typing import TYPE_CHECKING, Any, overload

from NGPIris.hci.hci_api_requests import make_index_request, make_query_request
from NGPIris.hci.types import IndexResponse, QueryRequest, QueryResponse

if TYPE_CHECKING:
    from requests import Response

    from NGPIris.hci import HCIHandler


@overload
def from_response(
    response: Response, to: type[IndexResponse]
) -> list[IndexResponse]:
    pass


@overload
def from_response(response: Response, to: type[QueryResponse]) -> QueryResponse:
    pass


def from_response(
    response: Response, to: type[IndexResponse | QueryResponse]
) -> list[IndexResponse] | QueryResponse:
    """
    Helper function for turning a :py:class:`requests.Response` object into a
    IRIS :py:class:`~NGPIris.hci.types.Response`. It achieves this by a somewhat
    *unorthodox* approach.

    NOTE: The return type for when :py:obj:`to` is
    :py:class:`~NGPIris.hci.types.IndexResponse` is a
    :py:type:`list[IndexResponse]`. This is due to the fact that the response
    produced by :py:func:`get_index_response` is a list of individual index
    responses. This is how the HCI works by design.

    :param response: The incoming :py:class:`requests.Response`

    :param to:
        The expected sub type of :py:class:`~NGPIris.hci.types.Response` that
        should be returned

    :return: The response as the chosen kind based on :py:obj:`to`
    """
    if to is IndexResponse:
        list_of_index_response_dicts: list[dict[str, Any]] = response.json()
        index_responses: list[IndexResponse] = [
            IndexResponse(dict(index_response_dict))  # pyright: ignore[reportArgumentType]
            for index_response_dict in list_of_index_response_dicts
        ]
        return index_responses
    elif to is QueryResponse:  # noqa: RET505
        as_dict = dict(response.json())
        return QueryResponse(as_dict)  # pyright: ignore[reportArgumentType]

    msg = "to_type = " + str(to)
    raise RuntimeError(msg)


def get_index_response(hci_handler: HCIHandler) -> list[IndexResponse]:
    """
    A short hand function equivalent to
    ```
    from_response(make_index_request(hci_handler), IndexResponse)
    ```.
    """
    return from_response(make_index_request(hci_handler), IndexResponse)


def get_query_response(
    query_dict: QueryRequest, hci_handler: HCIHandler
) -> QueryResponse:
    """
    A short hand function equivalent to
    ```
    from_response(
        make_query_request(query_dict, hci_handler), QueryResponse
    )
    ```.
    """
    return from_response(
        make_query_request(query_dict, hci_handler), QueryResponse
    )


def to_QueryRequest(dictionary: dict[str, Any]) -> QueryRequest:
    """
    Helper function for turning a :py:type:`dict` into a
    :py:class:`QueryRequest`. It achieves this by a somewhat
    *unorthodox* approach.
    """
    return QueryRequest(dictionary)  # pyright: ignore[reportArgumentType]
