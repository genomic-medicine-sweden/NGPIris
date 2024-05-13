
from NGPIris2.parse_credentials import CredentialsHandler
from NGPIris2.hcp import HCPHandler

from requests import (
    Response,
    get,
    post    
)

class HCPStatistics(HCPHandler):
    def __init__(self, credentials_path: str, use_ssl: bool = False, proxy_path: str = "", custom_config_path: str = "") -> None:
        super().__init__(credentials_path, use_ssl, proxy_path, custom_config_path)
        self.request_base_url = "https://" + self.endpoint + ":9090/mapi/tenants/" + self.tenant

    def get_statistics_response(self, path_extension : str = "") -> Response:
        url = self.request_base_url + path_extension
        headers = {
            "Authorization": "HCP " + self.token,
            "Cookie": "hcp-ns-auth=" + self.token,
            "Accept": "application/json"
        }
        response = get(
            url, 
            headers=headers,
            verify=self.use_ssl
        )

        return response
    
    