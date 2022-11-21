#!/usr/bin/env python3

# Script that uses HCI Search API.
# Get a json with information from selected index on HCI.


import argparse
import requests
import ast
import json
import os
import sys
import urllib3

from NGPIris import WD

from NGPIris.preproc import preproc

class HCIManager:
    
    def __init__(self,password="", credentials_path=""):
        if credentials_path:
            c = preproc.read_credentials(credentials_path)

        self.password = password if password else c('password','')
        self.address = "10.248.192.3"
        self.authport = "8000"
        self.apiport = "8888"

    def get_password(self):
        return self.password

    def create_template(self, index, query):
        """Reorganises query to standard format"""
        with open(f"{WD}/hci/template_query.json", "r") as sample:
            data = json.load(sample)
            data["indexName"] = index
            data["queryString"] = query

        with open(f"{WD}/hci/package.json", "w") as signal:
            json.dump(data, signal, indent=4)


    def generate_token(self):
        """Generate a security token from a password"""
        my_key = requests.post(f"https://{self.address}:{self.authport}/auth/oauth/", 
                 data={"grant_type": "password", "username": "admin", "password": f"{self.password}", "scope": "*",  
                 "client_secret": "hci-client", "client_id": "hci-client", "realm": "LOCAL"}, verify=False)
            
        return ast.literal_eval(my_key.text)["access_token"].lstrip()


    def query(self, token):
        """Queries the HCI using a token"""
        with open ("{}/hci/package.json".format(WD), "r") as signal:
            json_data = json.load(signal)
        response = requests.post(f"https://{self.address}:{self.apiport}/api/search/query", 
                   headers={"accept": "application/json", "Authorization": f"Bearer {token}"}, 
                   json=json_data, verify=False) 
        return response.text

    def pretty_query(self, token):
       """Return the result of a query in json loaded format"""
       return json.loads(self.query(token))["results"]


    # If using index, it searches through all indexes if nothing else is specified. 
    def get_index(self, token, index="all"):
        if index == "all":
            response = requests.get(f"https://{self.address}:{self.apiport}/api/search/indexes", 
                       headers={"accept": "application/json","Authorization": f"Bearer {token}"}, verify=False)
            response_string = response.text
            fixed_response = ast.literal_eval(response_string.replace("true", "True").replace("false", "False"))
            return fixed_response

        else:
            response = requests.get(f"https://{self.address}:{self.apiport}/api/search/indexes", 
                       headers={"accept": "application/json","Authorization": f"Bearer {token}"}, verify=False)
            response_string = response.text
            fixed_response = response_string.replace("true", "True").replace("false", "False")

            to_loop = ast.literal_eval(fixed_response)
            for each_dict in to_loop:
                if each_dict["name"] == index:
                    return each_dict
