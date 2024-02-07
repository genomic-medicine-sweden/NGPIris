
import NGPIris2.parse_credentials.parse_credentials as pc
import boto3
from botocore.client import Config
from boto3.s3.transfer import TransferConfig
import configparser as cfp


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
    
    def list_buckets(self) -> list[str]:
        """List all available buckets at endpoint."""
        response : dict = self.s3_client.list_buckets()
        list_of_buckets : list[dict] = response["Buckets"]
        return [bucket["Name"] for bucket in list_of_buckets]
    
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

    
