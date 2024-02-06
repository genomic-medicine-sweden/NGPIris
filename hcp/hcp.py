
import parse_credentials.parse_credentials as pc
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

        session = boto3.Session(
            self.aws_access_key_id, 
            self.aws_secret_access_key
        )

        ini_config = cfp.ConfigParser()
        ini_config.read("config.ini")

        s3_config = Config(
            s3 = {
                'addressing_style': 'path',
                'payload_signing_enabled': True
            },
            signature_version = 's3v4'
        )

        self.s3 = session.resource(
            's3',
            endpoint_url = self.endpoint,
            verify = False,  # Checks for SLL certificate. Disables because of already "secure" solution.
            config = s3_config
        )

        self.transfer_config = TransferConfig(
            multipart_threshold = ini_config.getint('hcp', 'size_threshold'),
            max_concurrency = ini_config.getint('hcp', 'max_concurrency'),
            multipart_chunksize = ini_config.getint('hcp', 'chunk_size')
        )

    def list_buckets(self):
        """List all available buckets at endpoint."""
        return [bucket.name for bucket in self.s3.buckets.all()]