
import os
import requests
import parse

def create_access_control_policy(user_ID_permissions : dict[str, str]) -> dict:
    access_control_policy : dict[str, list] = {
        "Grants" : []
    }
    for user_ID, permission in user_ID_permissions.items():
        if not permission in ["FULL_CONTROL", "WRITE", "WRITE_ACP", "READ", "READ_ACP"]:
            print("Invalid permission option:", permission)
            exit()
        grantee = {
            "Grantee": {
                "ID": user_ID,
                "Type": "CanonicalUser"
            },
            "Permission": permission
        }
        access_control_policy["Grants"].append(grantee)
    return access_control_policy

def raise_path_error(path : str):
    if not os.path.exists(path):
        raise FileNotFoundError("\"" + path + "\"" + " does not exist")

def get_response(endpoint : str, 
                 token : str, 
                 use_ssl : bool, 
                 url_extension : str, 
                 bucket_name : str | None = "") -> requests.Response:
    url_parse = parse.parse("https://{}", endpoint)
    if type(url_parse) is parse.Result:
        if bucket_name:
            url = "https://" + bucket_name + "." + url_parse[0]
        else:
            url = "https://" + url_parse[0]
        response = requests.get(
            url + url_extension,
            verify = use_ssl,
            headers = {
                "Authorization" : "HCP " + token,
                "Cookie" : "hcp-ns-auth=" + token,
                "Accept" : "application/json"
            }
        )
    else:
        raise RuntimeError("Could not parse the endpoint URL")
    return response

def get_bucket_response(endpoint : str, 
                        bucket_name : str | None, 
                        token : str, 
                        use_ssl : bool, 
                        url_extension : str) -> requests.Response:
    return get_response(endpoint, token, use_ssl, url_extension, bucket_name=bucket_name)

def get_tenant_response(endpoint : str, 
                        token : str, 
                        use_ssl : bool, 
                        url_extension : str) -> requests.Response:
    return get_response(endpoint, token, use_ssl, url_extension)