
import json
import requests

def raise_request_error(response : requests.Response, url : str) -> None:
    error_msg : str = "The response code from the reqeust made at " + url + " returned status code " + str(response.status_code) + ": " + str(json.loads(response.text)["errorMessage"])
    raise RuntimeError(error_msg) from None

def get_index_response(address : str, api_port : str, token : str, use_ssl : bool) -> requests.Response:
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

def get_query_response(query_path, address : str, api_port : str, token : str, use_ssl : bool, path_extension : str = "") -> requests.Response:
    with open(query_path, "r") as inp:
        url     : str            = "https://" + address + ":" + api_port + "/api/search/query/" + path_extension
        query   : dict[str, str] = json.load(inp)
        headers : dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Bearer " + token
        }
        response : requests.Response = requests.post(
            url, 
            json.dumps(query), 
            headers=headers, 
            verify = use_ssl
        )

        if response.status_code != 200:
            raise_request_error(response, url)
        
        return response