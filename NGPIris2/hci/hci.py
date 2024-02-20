
import NGPIris2.parse_credentials.parse_credentials as pc
import NGPIris2.hci.helpers as h

import requests
import pandas as pd
import urllib3

class HCIHandler:
    """Class for handling HCI requests"""
    def __init__(self, credentials_path : str, use_ssl : bool = False) -> None:
        """
        Constructor for the HCIHandler class.

        :param credentials_path: Path to the JSON credentials file
        :type credentials_path: str
        :param use_ssl: Boolean choice between using SSL, defaults to False
        :type use_ssl: bool, optional
        """
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hci = credentials_handler.hci
        self.username = self.hci["username"]
        self.password = self.hci["password"]
        self.address = self.hci["address"]
        self.auth_port = self.hci["auth_port"]
        self.api_port = self.hci["api_port"]
        self.token = ""

        self.use_ssl = use_ssl

        if not self.use_ssl:
            urllib3.disable_warnings()
    
    def request_token(self) -> None:
        """
        Request a token from the HCI, which is stored in the HCIHandler object. 
        The token is used for every operation that needs to send a request to 
        HCI.

        :raises RuntimeError: If there was a problem when requesting a token, a 
        runtime error will be raised 
        """
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
            response : requests.Response = requests.post(url, data = data, verify = self.use_ssl)
        except: 
            error_msg : str = "The token request made at " + url + " failed. Please check your connection and that you have your VPN enabled"
            raise RuntimeError(error_msg) from None

        token : str = response.json()["access_token"]
        self.token = token

    def list_index_names(self) -> list[str]:
        """
        Retrieve a list of all index names.

        :return: A list of index names
        :rtype: list[str]
        """
        response : requests.Response = h.get_index_response(self.address, self.api_port, self.token, self.use_ssl)
        return [entry["name"]for entry in response.json()]
    
    def look_up_index(self, index_name : str) -> dict:
        """
        Look up index information in the form of a dictionary by submitting 
        the index name. Will return an empty dictionary if no index was found.

        :param index_name: The index name
        :type index_name: str
        :return: A dictionary containing information about an index
        :rtype: dict
        """
        response : requests.Response = h.get_index_response(self.address, self.api_port, self.token, self.use_ssl)

        for entry in response.json():
            if entry["name"] == index_name:
                return dict(entry)
        
        return {}


    def query(self, query_path : str, only_metadata : bool = True) -> pd.DataFrame:
        """
        Make query to an HCI index. Will return a response in the shape of a 
        dictionary.

        :param query_path: Path to the query JSON file
        :type query_path: str
        :param only_metadata: Boolean choice between only returning the metadata. 
        Defaults to True
        :type only_metadata: bool, optional
        :return: A DataFrame containing the response from the query
        :rtype: pd.DataFrame
        """
        
        response_dict = dict(h.get_query_response(
            query_path, 
            self.address, 
            self.api_port, 
            self.token, 
            self.use_ssl
        ).json())
        
        list_of_data = [] 

        if only_metadata:
            for result_dict in response_dict["results"]:
                list_of_data.append(result_dict["metadata"])
        else:
            for result_dict in response_dict["results"]:
                list_of_data.append(result_dict)
        
        return pd.DataFrame(list_of_data)
    
    def SQL_query(self, query_path : str) -> pd.DataFrame:
        """
        Perform an SQL query given a path to a JSON file containing the 
        query. Returns a DataFrame containing the result of the query. 

        :param query_path: Path to the query JSON file
        :type query_path: str
        :raises RuntimeError: Will raise a runtime error if an error was found 
        with the SQL query
        :return: A DataFrame containing the result of the SQL query
        :rtype: pd.DataFrame
        """
        response = h.get_query_response(
            query_path, 
            self.address, 
            self.api_port, 
            self.token, 
            self.use_ssl, 
            "sql/"
        )

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
