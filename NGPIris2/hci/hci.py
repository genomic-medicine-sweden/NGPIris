
import NGPIris2.parse_credentials.parse_credentials as pc
import NGPIris2.hci.helpers as helpers

import requests
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
        try:
            response : requests.Response = requests.post(url, data = data, verify = False)
        except: 
            error_msg : str = "The token reqeust made at " + url + " failed. Please check your connection and that you have your VPN enabled"
            raise RuntimeError(error_msg) from None

        token : str = response.json()["access_token"]
        self.token = token

    def list_index_names(self) -> list[str]:
        response : requests.Response = helpers.get_index_response(self.address, self.api_port, self.token)
        return [entry["name"]for entry in response.json()]
    
    def look_up_index(self, index_name : str) -> dict:
        response : requests.Response = helpers.get_index_response(self.address, self.api_port, self.token)

        for entry in response.json():
            if entry["name"] == index_name:
                return dict(entry)
        
        return {}
        

    def query(self, query_path : str) -> dict:
        return helpers.get_query_response(query_path, self.address, self.api_port, self.token).json()
    
    def SQL_query(self, query_path : str) -> pd.DataFrame:
        response = helpers.get_query_response(query_path, self.address, self.api_port, self.token, "sql/")

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
                raise RuntimeError(''.join(meta_df["EXCEPTION"].to_list())) from None
        else:
            result_df = pd.DataFrame()

        return result_df
