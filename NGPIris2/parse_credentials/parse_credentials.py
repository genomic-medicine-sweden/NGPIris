
import json

Credentials = dict[str, dict[str, str]]
class CredentialsHandler:
    def __init__(self, credentials_path : str) -> None:

        self.hcp : dict[str, str] = {}
        self.hci : dict[str, str] = {}

        credentials : Credentials = parse_credentials(credentials_path)
        for key, value in credentials.items():
            setattr(self, key, value)

def check_empty_field(credentials : Credentials):
    empty_fields = []
    for k1, d in credentials.items():
        for k2, v in d.items():
            if v == "":
                empty_fields.append("- " + k1 + " : " + k2 + "\n")
    
    if empty_fields:
        raise RuntimeError("Missing entry for the following fields in the credentials file: \n" + "".join(empty_fields))

def parse_credentials(credentials_path : str) -> Credentials:
    credentials : Credentials = {}
    with open(credentials_path, 'r') as inp:
        credentials : Credentials = json.load(inp)
        
        check_empty_field(credentials)

        return credentials