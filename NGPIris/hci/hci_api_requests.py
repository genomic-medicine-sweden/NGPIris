from json import dumps, loads
from typing import TYPE_CHECKING, Literal

from requests import HTTPError, Response, get, post

from NGPIris.hci.exceptions import (
    DataNotSuppliedToPOST,
    DataSuppliedToGET,
    HCI_ResponseError,
)

if TYPE_CHECKING:
    from NGPIris.hci import HCIHandler, types
    from NGPIris.hci.types import QueryRequest

# ruff: noqa: PYI051


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

    :raise DataNotSuppliedToPOST:
        If :py:obj:`request_type` is set to :py:obj:`"POST"` but no data is
        supplied

    :raise DataSuppliedToGET:
        If :py:obj:`request_type` is set to :py:obj:`"GET"` and data is supplied

    :return: A response from the HCI
    """
    if data is None:
        data = {}
    if extra_headers is None:
        extra_headers = {}

    if (request_type == "POST") and not data:
        msg = "Request type is set to POST, but no data was supplied"
        raise DataNotSuppliedToPOST(msg)

    if request_type == "GET" and data:
        msg = "Request type is set to POST, but data was also supplied"
        raise DataSuppliedToGET(msg)

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


def make_index_request(hci_handler: HCIHandler) -> Response:
    """
    Retrieve the index response by making a request with the address, API port
    and token.

    :param hci_handler:
        The :py:class:`HCIHandler` object to be used to make the request

    :return: A response containing information about the index
    """
    return get_response(hci_handler, "GET", "/api/search/indexes/")


def make_query_request(
    query_dict: QueryRequest, hci_handler: HCIHandler
) -> Response:
    """
    Retrieve the query response by making a request with the address, API port
    and token.

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
