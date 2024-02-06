
import json

class CredentialsHandler:
    def __init__(self, credentials_path : str) -> None:

        self.hcp : dict[str, str] = {}
        self.hci : dict[str, str] = {}

        credentials : dict[str, str] = parse_credentials(credentials_path)
        for key, value in credentials.items():
            setattr(self, key, value)



def parse_credentials(credentials_path : str) -> dict[str,str]:
    credentials : dict[str, str] = {}
    with open(credentials_path, 'r') as inp:
        credentials = json.load(inp)
        
        # Raise exceptions for incomplete credentials here

        return credentials