
from NGPIris.hcp import HCPHandler


class HCPStatistics(HCPHandler):
    def __init__(self, credentials_path: str, use_ssl: bool = False, proxy_path: str = "", custom_config_path: str = "") -> None:
        super().__init__(credentials_path, use_ssl, proxy_path, custom_config_path)

    def get_namespace_settings(self) -> dict:
        if self.bucket_name:
            return self.get_response("/namespaces/" + self.bucket_name)
        else:
            raise RuntimeError("No bucket has been mounted")

    def get_namespace_statistics(self) -> dict:
        if self.bucket_name:
            return self.get_response("/namespaces/" + self.bucket_name + "/statistics")
        else:
            raise RuntimeError("No bucket has been mounted")

    def get_namespace_permissions(self) -> dict:
            if self.bucket_name:
                return self.get_response("/namespaces/" + self.bucket_name + "/permissions")
            else:
                raise RuntimeError("No bucket has been mounted")
