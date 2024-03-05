
import NGPIris2.parse_credentials.parse_credentials as pc
import NGPIris2.hcp.helpers as h

import boto3
from botocore.client import Config
from botocore.exceptions import EndpointConnectionError, ClientError
from boto3.s3.transfer import TransferConfig
import configparser as cfp

import os
import json
import parse
import urllib3
import tqdm

KB = 1024
MB = KB * KB

class HCPHandler:
    def __init__(self, credentials_path : str, use_ssl : bool = False, custom_config_path : str = "") -> None:
        """
        Class for handling HCP requests.

        :param credentials_path: Path to the JSON credentials file
        :type credentials_path: str
        
        :param use_ssl: Boolean choice between using SSL, defaults to False
        :type use_ssl: bool, optional
        
        :param custom_config_path: Path to a .ini file for customs settings regarding download and upload
        :type custom_config_path: str, optional
        """
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hcp = credentials_handler.hcp
        self.endpoint = "https://" + self.hcp["endpoint"]
        self.aws_access_key_id = self.hcp["aws_access_key_id"]
        self.aws_secret_access_key = self.hcp["aws_secret_access_key"]
        self.token = self.aws_access_key_id + ":" + self.aws_secret_access_key
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

        if custom_config_path:
            ini_config = cfp.ConfigParser()
            ini_config.read(custom_config_path)

            self.transfer_config = TransferConfig(
                multipart_threshold = ini_config.getint("hcp", "multipart_threshold"),
                max_concurrency = ini_config.getint("hcp", "max_concurrency"),
                multipart_chunksize = ini_config.getint("hcp", "multipart_chunksize"),
                use_threads = ini_config.getboolean("hcp", "use_threads")
            )
        else:
            self.transfer_config = TransferConfig(
                multipart_threshold = 10 * MB,
                max_concurrency = 60,
                multipart_chunksize = 40 * MB,
                use_threads = True
            )
    
    def mount_bucket(self, bucket_name : str) -> None:
        """
        Mount bucket that is to be used. This method needs to executed in order 
        for most of the other methods to work. It main concerns operations with 
        download and upload. 

        :param bucket_name: The name of the bucket to be mounted
        :type bucket_name: str

        :raises RuntimeError: If there was a problem when mounting the bucket, a 
        runtime error will be raised 
        """
        
        # Check if bucket exist
        try:
            response : dict = self.s3_client.head_bucket(Bucket = bucket_name)
        except EndpointConnectionError as e:
            print(e)
            exit("Please check your connection and that you have your VPN enabled")
        except ClientError as e:
            print(e)
            exit("Bucket \"" + bucket_name + "\" was not found")
        except Exception as e:
            exit(str(e))
            
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            error_msg = "The response code from the request made at " + self.endpoint + " returned status code " + response["ResponseMetadata"]["HTTPStatusCode"]
            raise RuntimeError(error_msg)
    
        self.bucket_name = bucket_name

    def list_buckets(self) -> list[str]:
        """
        List all available buckets at endpoint.

        :return: A list of buckets
        :rtype: list[str]
        """
        tenant_parse = parse.parse("https://{}.hcp1.vgregion.se", self.endpoint)
        if type(tenant_parse) is parse.Result:
            url = ":9090/mapi/tenants/" + str(tenant_parse[0]) + "/namespaces"
            response = h.get_tenant_response(self.endpoint, self.token, self.use_ssl, url)
            list_of_buckets : list[str] = dict(response.json())["name"]
            return list_of_buckets
        else:
            raise RuntimeError("Unable to parse endpoint. Make sure that you have entered the correct endpoint in your credentials JSON file")
    
    def list_objects(self, name_only = False) -> list:
        """
        List all objects in the mounted bucket

        :param name_only: If True, return only a list of the object names. 
        If False, return the full metadata about each object. Defaults to False.
        :type name_only: bool, optional

        :return: A list of of either strings or a list of object metadata (the form of a dictionary)
        :rtype: list
        """
        response_list_objects = dict(self.s3_client.list_objects_v2(
            Bucket = self.bucket_name
        ))
        if "Contents" not in response_list_objects.keys():
            return []
        list_of_objects : list[dict] = response_list_objects["Contents"]
        if name_only:
            return [object["Key"] for object in list_of_objects]
        else:
            return list_of_objects
    
    def get_object(self, key : str) -> dict:
        """
        Retrieve object metadata

        :param key: The object name
        :type key: str

        :return: A dictionary containing the object metadata
        :rtype: dict
        """
        response = dict(self.s3_client.get_object(
            Bucket = self.bucket_name,
            Key = key
        ))
        return response

    def object_exists(self, key : str) -> bool:
        """
        Check if a given object is in the mounted bucket

        :param key: The object name
        :type key: str

        :return: True if the object exist, otherwise False
        :rtype: bool
        """
        try:
            response = self.get_object(key)
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
            else: 
                return False
        except:
            return False

    def download_file(self, key : str, local_file_path : str) -> None:
        """
        Download one object file from the mounted bucket

        :param key: Name of the object
        :type key: str

        :param local_file_path: Path to a file on your local system where the 
        contents of the object file can be put.
        :type local_file_path: str
        """
        try:
            file_size : int = self.s3_client.head_object(Bucket = self.bucket_name, Key = key)["ContentLength"]
            with tqdm.tqdm(
                total = file_size, 
                unit = "B", 
                unit_scale = True, 
                desc = key
            ) as pbar:
                self.s3_client.download_file(
                    Bucket = self.bucket_name, 
                    Key = key, 
                    Filename = local_file_path, 
                    Config = self.transfer_config,
                    Callback = lambda bytes_transferred : pbar.update(bytes_transferred)
                )
        except ClientError as e0:
            print(str(e0))
            print("Could not find object", "\"" + key + "\"", "in bucket", "\"" + str(self.bucket_name) + "\"")
        except Exception as e:
            print(str(e))

    def upload_file(self, local_file_path : str, key : str = "") -> None:
        """
        Upload one file to the mounted bucket

        :param local_file_path: Path to the file to be uploaded
        :type local_file_path: str

        :param key: An optional new name for the file object on the bucket. 
        Defaults to the same name as the file
        :type key: str, optional
        """
        h.raise_path_error(local_file_path)

        if not key:
            file_name = os.path.basename(local_file_path)
            key = file_name

        file_size : int = os.stat(local_file_path).st_size
        with tqdm.tqdm(
            total = file_size, 
            unit = "B", 
            unit_scale = True, 
            desc = local_file_path
        ) as pbar:
            self.s3_client.upload_file(
                Filename = local_file_path, 
                Bucket = self.bucket_name, 
                Key = key,
                Config = self.transfer_config,
                Callback = lambda bytes_transferred : pbar.update(bytes_transferred)
            )

    def upload_folder(self, local_folder_path : str) -> None:
        """
        Upload the contents of a folder to the mounted bucket

        :param local_folder_path: Path to the folder to be uploaded
        :type local_folder_path: str
        """
        h.raise_path_error(local_folder_path)

        filenames = os.listdir(local_folder_path)

        for filename in filenames:
            self.upload_file(local_folder_path + filename)

    def delete_objects(self, keys : list[str], verbose = True) -> None:
        """Delete a list of objects on the mounted bucket 

        :param keys: List of object names to be deleted
        :type keys: list[str]

        :param verbose: Print the result of the deletion. Defaults to True
        :type verbose: bool, optional
        """
        object_list = []
        for key in keys:
            object_list.append({"Key" : key})

        deletion_dict = {"Objects": object_list}

        list_of_objects_before = self.list_objects(True)

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
        Simple search method using substrings in order to find certain objects. 
        
        Case insensitive by default.

        :param search_string: Substring to be used in the search
        :type search_string: str

        :param case_sensitive: Case sensitivity. Defaults to False
        :type case_sensitive: bool, optional

        :return: List of object names that match the in some way to the 
        object names
        :rtype: list[str]
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
    
    def get_bucket_statistics(self) -> dict:
        """
        Retrieve a dictionary containing information about the mounted bucket

        :raises RuntimeError: Raises an error if there was a problem with parsing the endpoint URL
        :return: A dictionary containing the information about the mounted bucket
        :rtype: dict
        """
        response = h.get_bucket_response(self.endpoint, self.bucket_name, self.token, self.use_ssl, "/proc/statistics")
        dict_of_statistics = {}
        statistics_parse = parse.parse("{}<statistics{}/>", response.text)
        if type(statistics_parse) is parse.Result:
            list_of_statistics : list[str] = statistics_parse[1].replace('"', "").split()
            for statistic in list_of_statistics:
                p = parse.parse("{}={}", statistic)
                if type(p) is parse.Result: 
                    if p[1].isdigit():
                        dict_of_statistics[p[0]] = int(p[1])
                    else:
                        dict_of_statistics[p[0]] = p[1]
        return dict_of_statistics

    def get_object_acl(self, key : str) -> dict:
        """
        Get the object Access Control List (ACL)

        :param key: The name of the object
        :type key: str

        :return: Return the ACL in the shape of a dictionary
        :rtype: dict
        """
        try:
            response : dict = self.s3_client.get_object_acl(
                Bucket = self.bucket_name,
                Key = key
            )
        except Exception as e:
            exit(str(e))
        return response

    def get_bucket_acl(self) -> dict:
        """
        Get the bucket Access Control List (ACL)

        :return: Return the ACL in the shape of a dictionary
        :rtype: dict
        """
        response : dict = self.s3_client.get_bucket_acl(
            Bucket = self.bucket_name
        )
        return response

    def add_single_object_acl(self, key : str, user_ID : str, permission : str) -> None:
        """
        Add permissions for a user in the Access Control List (ACL) for one object

        :param key: The name of the object
        :type key: str

        :param user_ID: The user name. Can either be the DisplayName or user_ID
        :type user_ID: str

        :param permission: What permission to be set. Valid options are:
        - FULL_CONTROL 
        - WRITE 
        - WRITE_ACP 
        - READ 
        - READ_ACP\n
        :type permission: str
        """
        self.s3_client.put_object_acl(
            Bucket = self.bucket_name,
            Key = key,
            AccessControlPolicy = h.create_access_control_policy({user_ID : permission})
        )

    def add_single_bucket_acl(self, user_ID : str, permission : str) -> None:
        """
        Add permissions for a user in the Access Control List (ACL) for the 
        mounted bucket

        :param user_ID: The user name. Can either be the DisplayName or user_ID
        :type user_ID: str
        
        :param permission: What permission to be set. Valid options are:
        - FULL_CONTROL 
        - WRITE 
        - WRITE_ACP 
        - READ 
        - READ_ACP\n
        :type permission: str
        """
        self.s3_client.put_bucket_acl(
            Bucket = self.bucket_name,
            AccessControlPolicy = h.create_access_control_policy({user_ID : permission})
        )

    def add_object_acl(self, key_user_ID_permissions : dict[str, dict[str, str]]) -> None:
        """
        Adds permissions to multiple objects, see below.

        In order to add permissions for multiple objects, we make use of a 
        dictionary of a dictionary:
        :py:obj:`key_user_ID_permissions = {key : {user_ID : permission}}`
        So for every object (key), we set the permissions for every user ID for 
        that object. 

        :param key_user_ID_permissions: The dictionary containing object name 
        and user_id-permission dictionary
        :type key_user_ID_permissions: dict[str, dict[str, str]]
        """
        for key, user_ID_permissions in key_user_ID_permissions.items():
            self.s3_client.put_object_acl(
                Bucket = self.bucket_name,
                Key = key,
                AccessControlPolicy = h.create_access_control_policy(user_ID_permissions)
            )

    def add_bucket_acl(self, user_ID_permissions : dict[str, str]) -> None:
        """
        Add permissions for multiple users for the mounted bucket

        :param user_ID_permissions: The dictionary containing the user name and 
        the corresponding permission to be set to that user
        :type user_ID_permissions: dict[str, str]
        """
        self.s3_client.put_bucket_acl(
            Bucket = self.bucket_name,
            AccessControlPolicy = h.create_access_control_policy(user_ID_permissions)
        )
