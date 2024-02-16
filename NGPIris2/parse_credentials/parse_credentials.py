
import json

Credentials = dict[str, dict[str, str]]
class CredentialsHandler:
    def __init__(self, credentials_path : str) -> None:

        self.hcp : dict[str, str] = {}
        self.hci : dict[str, str] = {}

        credentials : Credentials = parse_credentials(credentials_path)
        for key, value in credentials.items():
            setattr(self, key, value)

def all_fields_empty(key : str, credentials : Credentials) -> bool:
    return all([v == "" for v in credentials[key].values()])

def check_empty_field(credentials : Credentials):
    empty_fields_per_entry : dict[str, list[str]] = {}
    for k1, d in credentials.items():
        if all_fields_empty(k1, credentials):
            continue
        empty_fields : list[str] = []
        for k2, v in d.items():
            if v == "":
                empty_fields.append("\t- " + k2 + "\n")
        if empty_fields:
            empty_fields_per_entry[k1] = empty_fields

    all_empty_fields = []
    for entry, l in empty_fields_per_entry.items():
        l.insert(0, "- " + entry + ":\n")
        all_empty_fields.append("".join(l))

    if all_empty_fields:
        raise RuntimeError(
            "Missing fields for the following entries in the credentials file: \n" + 
            "".join(all_empty_fields)
        )

def parse_credentials(credentials_path : str) -> Credentials:
    credentials : Credentials = {}
    with open(credentials_path, 'r') as inp:
        credentials : Credentials = json.load(inp)
        
        check_empty_field(credentials)

        return credentials