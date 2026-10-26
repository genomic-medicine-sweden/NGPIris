from json import dumps, loads
from typing import TYPE_CHECKING, Literal

from requests import HTTPError, Response, get, post

from NGPIris.hci.exceptions import HCI_ResponseError

if TYPE_CHECKING:
    from NGPIris.hci import HCIHandler

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
    data: dict | None = None,
) -> Response:
    """
    TBD

    :param hci_handler:

    :param api_endpoint:

    :param api_endpoint_extension:

    :param extra_headers:

    :return: A response containing information about the index
    """
    if data is None:
        data = {}
    if extra_headers is None:
        extra_headers = {}
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

    :return: A response containing information about the index
    """
    return get_response(hci_handler, "GET", "/api/search/indexes/")


def get_query_response(
    query_dict: dict[str, str | int | list | dict], hci_handler: HCIHandler
) -> Response:
    """
    Retrieve the query response given the address, API port and token.

    :param query_dict: The query dictionary

    :param hci_handler:

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
