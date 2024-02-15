
import NGPIris2.parse_credentials.parse_credentials as pc
import NGPIris2.hcp.helpers as h

import boto3
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
import configparser as cfp

import os
import json
import parse
import urllib3

class HCPHandler:
    def __init__(self, credentials_path : str, use_ssl : bool = False) -> None:
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hcp = credentials_handler.hcp
        self.endpoint = self.hcp["endpoint"]
        self.aws_access_key_id = self.hcp["aws_access_key_id"]
        self.aws_secret_access_key = self.hcp["aws_secret_access_key"]
        self.bucket_name = None
        self.use_ssl = use_ssl

        if not self.use_ssl:
            urllib3.disable_warnings()

        s3_config = Config(
            s3 = {
                "addressing_style": "path",
                "payload_signing_enabled": True
            },
            signature_version = "s3v4"
        )

        self.s3_client = boto3.client(
            "s3", 
            aws_access_key_id = self.aws_access_key_id, 
            aws_secret_access_key = self.aws_secret_access_key,
            endpoint_url = self.endpoint,
            verify = self.use_ssl,
            config = s3_config
        )

        ini_config = cfp.ConfigParser()
        ini_config.read("config.ini")

        self.transfer_config = TransferConfig(
            multipart_threshold = ini_config.getint("hcp", "size_threshold"),
            max_concurrency = ini_config.getint("hcp", "max_concurrency"),
            multipart_chunksize = ini_config.getint("hcp", "chunk_size")
        )
    
    def mount_bucket(self, bucket_name : str) -> None:
        # Check if bucket exist
        response : dict = self.s3_client.head_bucket(Bucket = bucket_name)

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            error_msg = "The response code from the reqeust made at " + self.endpoint + " returned status code " + response["ResponseMetadata"]["HTTPStatusCode"]
            raise RuntimeError(error_msg)
    
        self.bucket_name = bucket_name

    def list_buckets(self) -> list[str]:
        """List all available buckets at endpoint."""
        response : dict = self.s3_client.list_buckets()
        list_of_buckets : list[dict] = response["Buckets"]
        return [bucket["Name"] for bucket in list_of_buckets]
    
    def list_objects(self, name_only = False) -> list:
        response_list_objects : dict = self.s3_client.list_objects_v2(
            Bucket = self.bucket_name
        )
        list_of_objects : list[dict] = response_list_objects["Contents"]
        if name_only:
            return [object["Key"] for object in list_of_objects]
        else:
            return list_of_objects
    
    def download_object_file(self, key : str, local_file_path : str) -> None:
        try:
            self.s3_client.download_file(
                self.bucket_name, 
                key, 
                local_file_path, 
                Config = self.transfer_config
            )
        except Exception as e:
            print("botocore.exceptions.ClientError: " + str(e))
            print("Could not find object", "\"" + key + "\"", "in bucket", "\"" + str(self.bucket_name) + "\"")


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
            
            self.download_object_file(key, path)


    def upload_object_file(self, local_file_path : str, key : str = "") -> None:
        h.raise_path_error(local_file_path)

        if not key:
            file_name = os.path.split(local_file_path)[1]
            key = file_name

        self.s3_client.upload_file(
            local_file_path, 
            self.bucket_name, 
            key,
            Config = self.transfer_config
        )

    def upload_object_folder(self, local_folder_path : str) -> None:
        h.raise_path_error(local_folder_path)

        filenames = os.listdir(local_folder_path)

        for filename in filenames:
            self.upload_object_file(local_folder_path + filename)

    def delete_objects(self, keys : list[str], verbose = True) -> None:
        object_list = []
        for key in keys:
            object_list.append({"Key" : key})

        deletion_dict = {"Objects": object_list}

        list_of_objects_before = self.list_objects(True)
        print("list before", list_of_objects_before)

        response : dict = self.s3_client.delete_objects(
            Bucket = self.bucket_name,
            Delete = deletion_dict
        )
        if verbose:
            print(json.dumps(response, indent=4))
        diff : set[str] = set(keys) - set(list_of_objects_before)
        if diff:
            does_not_exist = []
            for key in diff:
                does_not_exist.append("- " + key + "\n")
            print("The following could not be deleted because they didn't exist: \n" + "".join(does_not_exist))

    def search_objects_in_bucket(self, search_string : str, case_sensitive = False) -> list[str]:
        """
        Simple seach method using substrings in order to find certain objects. 
        
        Case insensitive by default.
        """
        search_result : list[str] = []
        for key in self.list_objects(True):
            parse_object = parse.search(
                search_string, 
                key, 
                case_sensitive = case_sensitive
            )
            if type(parse_object) is parse.Result:
                search_result.append(key)
        return search_result
    
    def get_object_acl(self, key : str) -> dict:
        response : dict = self.s3_client.get_object_acl(
            Bucket = self.bucket_name,
            Key = key
        )
        return response

    def get_bucket_acl(self) -> dict:
        response : dict = self.s3_client.get_bucket_acl(
            Bucket = self.bucket_name
        )
        return response

    def add_single_object_acl(self, key : str, user_ID : str, permission : str) -> None:
        self.s3_client.put_object_acl(
            Bucket = self.bucket_name,
            Key = key,
            AccessControlPolicy = h.create_access_control_policy({user_ID : permission})
        )

    def add_single_bucket_acl(self, user_ID : str, permission : str) -> None:
        self.s3_client.put_bucket_acl(
            Bucket = self.bucket_name,
            AccessControlPolicy = h.create_access_control_policy({user_ID : permission})
        )

    def add_object_acl(self, key_user_ID_permissions : dict[str, dict[str, str]]) -> None:
        """
        In order to add permissions for multiple objects, we make use of a dictionary of a dictionary:
        :py:obj:`key_user_ID_permissions = {key : {user_ID : permission}}`
        So for every obejct (key), we set the permissions for every user ID for that object. 
        """
        for key, user_ID_permissions in key_user_ID_permissions.items():
            self.s3_client.put_object_acl(
                Bucket = self.bucket_name,
                Key = key,
                AccessControlPolicy = h.create_access_control_policy(user_ID_permissions)
            )

    def add_bucket_acl(self, user_ID_permissions : dict[str, str]) -> None:
        self.s3_client.put_bucket_acl(
            Bucket = self.bucket_name,
            AccessControlPolicy = h.create_access_control_policy(user_ID_permissions)
        )
