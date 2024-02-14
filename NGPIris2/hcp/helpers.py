
import os

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
