
import NGPIris2.parse_credentials.parse_credentials as pc
import boto3
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
import configparser as cfp
from typing import Any, List
import os
import json
import parse


class HCPHandler:
    def __init__(self, credentials_path : str) -> None:
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hcp = credentials_handler.hcp
        self.endpoint = self.hcp["endpoint"]
        self.aws_access_key_id = self.hcp["aws_access_key_id"]
        self.aws_secret_access_key = self.hcp["aws_secret_access_key"]

        ini_config = cfp.ConfigParser()
        ini_config.read("config.ini")

        s3_config = Config(
            s3 = {
                'addressing_style': 'path',
                'payload_signing_enabled': True
            },
            signature_version = 's3v4'
        )

        self.s3_client = boto3.client(
            "s3", 
            aws_access_key_id = self.aws_access_key_id, 
            aws_secret_access_key = self.aws_secret_access_key,
            endpoint_url = self.endpoint,
            verify = False,
            config = s3_config
        )

        self.transfer_config = TransferConfig(
            multipart_threshold = ini_config.getint('hcp', 'size_threshold'),
            max_concurrency = ini_config.getint('hcp', 'max_concurrency'),
            multipart_chunksize = ini_config.getint('hcp', 'chunk_size')
        )
    
    def mount_bucket(self, bucket_name : str) -> None:
        # Check if bucket exist
        # Note: We could add the ExpectedBucketOwner parameter for checking user permissions
        response : dict = self.s3_client.head_bucket(Bucket = bucket_name)

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            # To-Do: Add exceptions 
            print("Error: HTTPStatusCode was " + response["ResponseMetadata"]["HTTPStatusCode"])
            exit()
    
        self.bucket_name = bucket_name
        self.bucket_objects = None

    def get_bucket_metadata(self) -> dict:

        out : dict = {}

        acl_response : dict = self.s3_client.get_bucket_acl(
            Bucket = self.bucket_name
        )

        location_response : dict = self.s3_client.get_bucket_location(
            Bucket = self.bucket_name
        )

        out.update(acl_response)
        out.update(location_response)

        return out

    def list_buckets(self) -> list[str]:
        """List all available buckets at endpoint."""
        response : dict = self.s3_client.list_buckets()
        list_of_buckets : list[dict] = response["Buckets"]
        return [bucket["Name"] for bucket in list_of_buckets]
    
    def list_objects(self, name_only = False) -> list[dict]:
        response_list_objects : dict = self.s3_client.list_objects_v2(
            Bucket = self.bucket_name
        )
        list_of_objects : list[dict] = response_list_objects["Contents"]
        if name_only:
            return [object["Key"] for object in list_of_objects]
        else:
            return list_of_objects
    
    def download_object_file(self, key : str, local_file_path : str) -> None:
        # To-Do: add exception handling
        self.s3_client.download_file(
            self.bucket_name, 
            key, 
            local_file_path, 
            Config = self.transfer_config
        )

    def download_all_object_files(self, 
                                  local_folder_path : str, 
                                  keys_exluced : list[str] = []) -> None:
        """Downloads all objects in the mounted bucket to a local folder"""
        list_of_objects : list[dict] = self.list_objects()

        if not os.path.exists(local_folder_path):
            os.makedirs(local_folder_path)

        for object in list_of_objects:
            key : str = object["Key"]
            path : str = local_folder_path + key

            if key in keys_exluced:
                continue

            self.s3_client.download_file(
                self.bucket_name,
                key,
                path,
                Config = self.transfer_config
            )

    def upload_object_file(self, local_file_path : str, key : str = "") -> None:
        if not key:
            file_name = os.path.split(local_file_path)[1]
            key = file_name
        
        self.s3_client.upload_file(
            local_file_path, 
            self.bucket_name, 
            key,
            Config = self.transfer_config
        )
        pass

    def upload_object_folder(self, local_folder_path : str) -> None:
        if not os.path.exists(local_folder_path):
            # To-Do: Raise exception
            print("Error: folder does not exist")

        filenames = os.listdir(local_folder_path)

        for filename in filenames:
            self.upload_object_file(local_folder_path + filename)

    def delete_objects(self, keys : list[str], verbose = True):
        object_list = []
        for key in keys:
            object_list.append({"Key" : key})

        deletion_dict = {"Objects": object_list}

        response : dict = self.s3_client.delete_objects(
            Bucket = self.bucket_name,
            Delete = deletion_dict
        )
        if verbose:
            print(json.dumps(response, indent=4))

    def search_objects_in_bucket(self, search_string : str, case_sensitive = False) -> list[str]:
        """
        Simple seach method using substrings in order to find certain objects. 
        
        Case insensitive by default.
        """
        search_result : list[str] = []
        p = self.s3_client.get_paginator("list_objects_v2")
        page_iterator = p.paginate(Bucket = self.bucket_name)
        for page in page_iterator:
            for object in page["Contents"]:
                parse_object = parse.search(
                    search_string, 
                    object["Key"], 
                    case_sensitive = case_sensitive
                )
                if type(parse_object) is parse.Result:
                    search_result.append(object["Key"])
        return search_result


