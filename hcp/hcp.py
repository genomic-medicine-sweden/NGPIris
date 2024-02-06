
import parse_credentials.parse_credentials as pc

class HCPHandler:

    def __init__(self, credentials_path) -> None:
        credentials_handler = pc.CredentialsHandler(credentials_path)
        self.hcp = credentials_handler.hcp
        self.endpoint = self.hcp["endpoint"]
        self.aws_access_key_id = self.hcp["aws_access_key_id"]
        self.aws_secret_access_key = self.hcp["aws_secret_access_key"]
