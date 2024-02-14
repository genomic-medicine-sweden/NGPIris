
import json
import requests

def get_index_response(address : str, api_port : str, token : str) -> requests.Response:
    url     : str            = "https://" + address + ":" + api_port + "/api/search/indexes/"
    headers : dict[str, str] = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token
    }

    response : requests.Response = requests.get(
        url,
        headers = headers,
        verify = False
    )

    if response.status_code != 200:
        print(response.text)
        # To-Do: Add exception handling

    return response

def get_query_response(query_path, address : str, api_port : str, token : str, path_extension : str = "") -> requests.Response:
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
            verify = False
        )

        if response.status_code != 200:
            print(response.text)
            # To-Do: Add exception handling
        
        return response