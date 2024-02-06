
import parse_credentials.parse_credentials as pc
import requests
import json

class HCIHandler:
    def __init__(self, credentials_path : str) -> None:
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hci = credentials_handler.hci
        self.username = self.hci["username"]
        self.password = self.hci["password"]
        self.address = self.hci["address"]
        self.auth_port = self.hci["auth_port"]
        self.api_port = self.hci["api_port"]
        self.token = ""
    
    def request_token(self) -> None:
        url = "https://" + self.address + ":" + self.auth_port + "/auth/oauth/"
        data = {
            "grant_type": "password", 
            "username": "admin", 
            "password": self.password,
            "scope": "*",  
            "client_secret": "hci-client", 
            "client_id": "hci-client", 
            "realm": "LOCAL"
        }
        response : requests.Response = requests.post(url, data = data, verify = False)
        token : str = response.json()["access_token"]
        self.token = token

    def list_index_names(self) -> list[str]:
        url     : str            = "https://" + self.address + ":" + self.api_port + "/api/search/indexes/"
        headers : dict[str, str] = {
                "Accept": "application/json",
                "Authorization": "Bearer " + self.token
        }
        
        response : requests.Response = requests.get(
            url,
            headers = headers,
            verify = False)

        if response.status_code != 200:
            print(response.text)
        
        return [entry["name"]for entry in response.json()]

    def get_index(self, index = "all") -> None:
        pass

    def query(self, token, index_name, query_string) -> None:
        pass    def query(self, token : str, query_path : str) -> dict:
