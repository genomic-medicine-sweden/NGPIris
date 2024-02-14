#import NGPIris2.hci.hci as hci
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