
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
    
    def get_token(self, set_token_attribute = False) -> str:
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
        if set_token_attribute:
            self.token = token
        return token

    def get_index(self, token, index = "all") -> None:
        pass

    def query(self, token, index_name, query_string) -> None:
        pass    def query(self, token : str, query_path : str) -> dict:
