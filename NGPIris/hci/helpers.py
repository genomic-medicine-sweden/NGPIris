from json import dumps, loads
from typing import TYPE_CHECKING, Any, Literal, overload

from requests import HTTPError, Response, get, post

from NGPIris.hci.exceptions import HCI_ResponseError
from NGPIris.hci.types import IndexResponse, QueryRequest, QueryResponse

if TYPE_CHECKING:
    from NGPIris.hci import HCIHandler, types

# ruff: noqa: PYI051


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


def get_response(
    hci_handler: HCIHandler,
    request_type: Literal["GET", "POST"],
    api_endpoint: Literal[
        "/auth/oauth/",
        "/api/search/indexes/",
        "/api/search/query/",
    ]
    | str,
    api_endpoint_extension: str = "",
    extra_headers: dict[str, str] | None = None,
    data: dict | types.Request | None = None,
) -> Response:
    """
    A general implementation of making requests to the HCI.

    :param hci_handler:
        The :py:class:`HCIHandler` object to be used to make the request

    :param request_type: The specified kind of request

    :param api_endpoint: The specified API endpoint to make the request at

    :param api_endpoint_extension: Optional extension of the API endpoint

    :param extra_headers: Optional additional header values to the request

    :param data: Optional data to be made

    :return: A response from the HCI
    """
    if data is None:
        data = {}
    if extra_headers is None:
        extra_headers = {}

    if not (request_type == "POST" and data):
        raise TypeError

    url: str = (
        "https://"
        + hci_handler.address
        + ":"
        + hci_handler.api_port
        + api_endpoint
        + api_endpoint_extension
    )
    headers: dict[str, str] = extra_headers | {
        "Accept": "application/json",
        "Authorization": "Bearer " + hci_handler.token,
    }

    match request_type:
        case "GET":
            response = get(
                url, headers=headers, verify=hci_handler.use_ssl, timeout=15
            )
        case "POST":
            response = post(
                url,
                data=dumps(data),
                headers=headers,
                verify=hci_handler.use_ssl,
                timeout=15,
            )

    try:
        response.raise_for_status()
    except HTTPError as http_error:
        error_content = dict(loads(http_error.response.content))
        error_msg = (
            "\nstatusCode: "
            + str(error_content.get("statusCode", ""))
            + "\nerrorMessage: "
            + str(error_content.get("errorMessage", ""))
            + "\nerrorProperties: "
            + str(error_content.get("errorProperties", ""))
        )
        raise HCI_ResponseError(error_msg) from http_error

    return response


def get_index_response(hci_handler: HCIHandler) -> Response:
    """
    Retrieve the index response given the address, API port and token.

    :param hci_handler:
        The :py:class:`HCIHandler` object to be used to make the request

    :return: A response containing information about the index
    """
    return get_response(hci_handler, "GET", "/api/search/indexes/")


def get_query_response(
    query_dict: QueryRequest, hci_handler: HCIHandler
) -> Response:
    """
    Retrieve the query response given the address, API port and token.

    :param query_dict: The query dictionary

    :param hci_handler:
        The :py:class:`HCIHandler` object to be used to make the request

    :return: A response containing information about the query
    """
    return get_response(
        hci_handler,
        "POST",
        "/api/search/query/",
        extra_headers={
            "Content-Type": "application/json",
        },
        data=query_dict,
    )
