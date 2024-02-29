
import json
import requests

def raise_request_error(response : requests.Response, url : str) -> None:
    """
    Raise a request error.

    :param response: The response containing the error to be raised
    :type response: requests.Response

    :param url: The URL where the request was made
    :type url: str

    :raises RuntimeError: Will raise a runtime error for a request
    """
    error_msg : str = "The response code from the request made at " + url + " returned status code " + str(response.status_code) + ": " + str(json.loads(response.text)["errorMessage"])
    raise RuntimeError(error_msg) from None

def get_index_response(address : str, api_port : str, token : str, use_ssl : bool) -> requests.Response:
    """
    Retrieve the index response given the address, API port and token.

    :param address: The address where request is to be made
    :type address: str

    :param api_port: The API port at the given address
    :type api_port: str

    :param token: The HCI token 
    :type token: str

    :param use_ssl: Boolean choice of using SSL
    :type use_ssl: bool

    :return: A response containing information about the index
    :rtype: requests.Response
    """
    url     : str            = "https://" + address + ":" + api_port + "/api/search/indexes/"
    headers : dict[str, str] = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token
    }

    response : requests.Response = requests.get(
        url,
        headers = headers,
        verify = use_ssl
    )

    if response.status_code != 200:
        raise_request_error(response, url)

    return response

def get_query_response(
        query_dict : dict[str, str], 
        address : str, 
        api_port : str, 
        token : str, 
        use_ssl : bool, 
        path_extension : str = ""
    ) -> requests.Response:
    """
    Retrieve the query response given the address, API port and token.

    :param query_dict: The query dictionary
    :type query_dict: dict[str, str]

    :param address: The address where request is to be made
    :type address: str

    :param api_port: The API port at the given address
    :type api_port: str

    :param token: The HCI token 
    :type token: str

    :param use_ssl: Boolean choice of using SSL
    :type use_ssl: bool

    :param path_extension: possibly extend the request URL. Used for example 
    when making SQL requests. Defaults to ""
    :type path_extension: str, optional

    :return: A response containing information about the query
    :rtype: requests.Response
    """
    if not "indexName" in query_dict.keys():
        raise RuntimeError("Field indexName is missing in the query dictionary")

    url     : str            = "https://" + address + ":" + api_port + "/api/search/query/" + path_extension
    query   : dict[str, str] = query_dict
    headers : dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token
    }
    response : requests.Response = requests.post(
        url, 
        json.dumps(query), 
        headers = headers, 
        verify = use_ssl
    )

    if response.status_code != 200:
        raise_request_error(response, url)
    
    return response
    
def process_raw_query(raw_query : dict, only_metadata : bool) -> list:
    """
    Take a raw query dictionary and turn it into a list of datapoints

    :param raw_query: Raw query to be processed
    :type raw_query: dict

    :param only_metadata: Boolean choice between only returning the metadata
    :type only_metadata: bool
    
    :return: List of datapoints from the response
    :rtype: list
    """ 
    list_of_data = [] 
    if only_metadata:
        for result_dict in raw_query["results"]:
            list_of_data.append({k : "".join(v) for k, v in result_dict["metadata"].items()})
    else:
        for result_dict in raw_query["results"]:
            list_of_data.append(result_dict)
    
    return list_of_data
    