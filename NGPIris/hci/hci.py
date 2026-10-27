from json import load
from pathlib import Path
from typing import Literal
from warnings import deprecated

from requests import Response, post
from urllib3 import disable_warnings

from NGPIris.hci.exceptions import IndexNotFound
from NGPIris.hci.helpers import (
    get_index_response,
    get_query_response,
    to_QueryRequest,
)
from NGPIris.hci.types import (
    FacetRequest,
    IndexResponse,
    QueryRequest,
    QueryResponse,
    SortField,
)
from NGPIris.parse_credentials import CredentialsHandler
from NGPIris.utils.deprecation import _add_deprecation_in_doc_string


class HCIHandler:
    """
    Class for handling HCI requests.
    """

    def __init__(
        self, credentials: str | dict[str, str], use_ssl: bool = False
    ) -> None:
        """
        Class for handling HCI requests.

        :param credentials:
            If ``credentials`` is a :py:type:`str`, then it will be interpreted as
            a path to the JSON credentials file. If ``credentials`` is a
            :py:type:`dict`, then a dictionary with the appropriate HCI
            credentials is expected::

                {
                    "username" : "",
                    "password" : "",
                    "address" : "",
                    "auth_port" : "",
                    "api_port" : ""
                }

        :param use_ssl: Boolean choice between using SSL
        """
        if type(credentials) is str:
            credentials_handler = CredentialsHandler(credentials)
            self.hci = credentials_handler.hci

            self.username = self.hci["username"]
            self.password = self.hci["password"]
            self.address = self.hci["address"]
            self.auth_port = self.hci["auth_port"]
            self.api_port = self.hci["api_port"]
        elif type(credentials) is dict:
            self.username = credentials["username"]
            self.password = credentials["password"]
            self.address = credentials["address"]
            self.auth_port = credentials["auth_port"]
            self.api_port = credentials["api_port"]

        self.use_ssl = use_ssl

        if not self.use_ssl:
            disable_warnings()

        self.token = self._request_token()

    _REQUEST_TOKEN_DEP_MSG = (
        ":py:func:`request_token` is depricated in favor of integrating its "  # noqa: S105
        "functionality into the :py:class:`HCIHandler` constructor"
    )

    @_add_deprecation_in_doc_string(_REQUEST_TOKEN_DEP_MSG, "v5.6.7")
    @deprecated(_REQUEST_TOKEN_DEP_MSG)
    def request_token(self) -> None:
        """
        Request a token from the HCI, which is stored in the HCIHandler object.
        The token is used for every operation that needs to send a request to
        HCI.

        :raises ConnectionError:
            If there was a problem when requesting a token
        """
        self.token = self._request_token()

    def _request_token(self) -> str:
        """
        Request a token from the HCI. The token is used for every operation
        that needs to send a request to HCI.

        :raises ConnectionError:
            If there was a problem when requesting a token
        """
        url = "https://" + self.address + ":" + self.auth_port + "/auth/oauth/"
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "*",
            "client_secret": "hci-client",
            "client_id": "hci-client",
            "realm": "LOCAL",
        }
        try:
            response: Response = post(
                url, data=data, verify=self.use_ssl, timeout=15
            )
        except:  # noqa: E722  # pragma: no cover
            error_msg: str = (
                "The token request made at "
                + url
                + " failed. Please check your connection."
            )
            raise ConnectionError(error_msg) from None

        token: str = response.json()["access_token"]
        return token

    def list_index_names(self) -> list[str]:
        """
        Retrieve a list of all index names.

        :return: A list of index names
        """
        return [entry["name"] for entry in get_index_response(self)]

    def look_up_index(self, index_name: str) -> IndexResponse:
        """
        Look up index information in the form of a dictionary by submitting
        the index name. Will return an empty dictionary if no index was found.

        :param index_name: The index name

        :return: A dictionary containing information about an index
        """
        for entry in get_index_response(self):
            if entry["name"] == index_name:
                return entry

        msg = "The index " + index_name + " could not be found"
        raise IndexNotFound(msg)

    def query(self, query_dict: QueryRequest) -> QueryResponse:
        """
        Make query to an HCI index, with a :py:class:`QueryRequest` typed
        dictionary.

        :param query_dict:
            Dictionary consisting of the query. For more information see the
            specification of :py:class:`QueryRequest`

        :return:
            :py:class:`QueryResponse` typed dictionary containing the query
            response
        """
        return get_query_response(query_dict, self)

    def query_from_JSON(self, query_path: str) -> QueryResponse:
        """
        Make query to an HCI index, with pre-written query in a JSON file.

        :param query_path: Path to the JSON file

        :return: Dictionary containing the raw query
        """
        with Path(query_path).open() as inp:
            return get_query_response(to_QueryRequest(load(inp)), self)

    def basic_query(
        self,
        index_name: str,
        query_string: str = "",
        items_to_return: int = 0,
        facets: list[str] | None = None,
        sort_fields: list[tuple[str, Literal["DESC", "ASC"]]] | None = None,
    ) -> QueryResponse:
        """
        Make a query to the HCI based on the parameters of this method.

        :param index_name: Name of the index

        :param query_string: The Solr query string.

        :param items_to_return: Number of results that should be returned

        :param facets:
            List of facets that should be returned included in the response.

        :param sort_fields:
            List of tuples of fields and sort orders

        :return: The response in the form of a dictionary
        """
        if sort_fields is None:
            sort_fields = []
        if facets is None:
            facets = []

        facetRequests = [FacetRequest({"fieldName": facet}) for facet in facets]
        sortFields = [
            SortField(sortField=sf, sortOrder=so) for sf, so in sort_fields
        ]
        query_dict: QueryRequest = {
            "indexName": index_name,
            "queryString": query_string,
            "itemsToReturn": items_to_return,
            "facetRequests": facetRequests,
            "sortFields": sortFields,
        }
        return self.query(query_dict)
