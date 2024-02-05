
import json

def parse_credentials(credentials_path : str) -> dict[str,str]:
    credentials : dict[str, str] = {}
    with open(credentials_path, 'r') as inp:
        credentials = json.load(inp)
        
        # Raise conditions for incomplete credentials here

        return credentials