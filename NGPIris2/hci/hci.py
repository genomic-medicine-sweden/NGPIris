
import NGPIris2.parse_credentials.parse_credentials as pc
import requests
import json
import pandas as pd

# TO BE REMOVED LATER
import urllib3
urllib3.disable_warnings()
#####################

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
            verify = False
        )

        if response.status_code != 200:
            print(response.text)
            # To-Do: Add exception handling
        
        return [entry["name"]for entry in response.json()]

    def query(self, query_path : str) -> dict:
        with open(query_path, "r") as inp:
            url     : str            = "https://" + self.address + ":" + self.api_port + "/api/search/query/"
            query   : dict[str, str] = json.load(inp)
            headers : dict[str, str] = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + self.token
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
        
        return response.json()
    
    def SQL_query(self, query_path : str) -> pd.DataFrame:
        with open(query_path, "r") as inp:
            url     : str            = "https://" + self.address + ":" + self.api_port + "/api/search/query/sql/"
            query   : dict[str, str] = json.load(inp)
            headers : dict[str, str] = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": "Bearer " + self.token
            }
        response : requests.Response = requests.post(
            url, 
            json.dumps(query), 
            headers=headers, 
            verify = False
        )

        if response.status_code != 200:
            exit(response.text)
            # To-Do: Add exception handling

        result_list = list(response.json()["results"])
        if result_list:
            result_df : pd.DataFrame = pd.DataFrame(result_list)
            meta_df : pd.DataFrame = pd.DataFrame()

            for row in result_df["metadata"]:
                metadata_dict : dict = dict(row)
                df = pd.DataFrame(metadata_dict)
                meta_df = pd.concat([meta_df, df])

            meta_df = meta_df.reset_index(drop = True)

            for col in meta_df.columns:
                result_df.insert(len(result_df.columns), col, meta_df[col], allow_duplicates = True)

            result_df = result_df.drop("metadata", axis = 1)

            if "EXCEPTION" in meta_df.columns:
                exit(''.join(meta_df["EXCEPTION"].to_list()))
        else:
            result_df = pd.DataFrame()

        return result_df
