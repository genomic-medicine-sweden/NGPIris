from NGPIris import HCPHandler


class HCPStatistics(HCPHandler):
    """
    Class for handling HCP statistics requests. Subclass of `HCPHandler`.
    """

    def __init__(
        self,
        credentials_path: str,
        use_ssl: bool = False,
        custom_config_path: str = "",
    ) -> None:
        """
        Constructor for the `HCPStatistics` class. Identical to the constructor
        of `HCPHandler`.
        """
        super().__init__(credentials_path, use_ssl, custom_config_path)

    def get_namespace_settings(self) -> dict:
        """
        Get namespace/bucket settings.

        :return: Namespace/bucket settings as a dictionary.
        """
        return self.get_response("/namespaces/" + self._get_mounted_bucket())  # pyright: ignore[reportOperatorIssue, reportAttributeAccessIssue]

    def get_namespace_statistics(self) -> dict:
        """
        Get namespace/bucket statistics.

        :return: Namespace/bucket statistics as a dictionary.
        """
        return self.get_response(  # pyright: ignore[reportAttributeAccessIssue]
            "/namespaces/" + self._get_mounted_bucket() + "/statistics",  # pyright: ignore[reportOperatorIssue]
        )

    def get_namespace_permissions(self) -> dict:
        """
        Get namespace/bucket permissions.

        :return: Namespace/bucket permissions as a dictionary.
        """
        return self.get_response(  # pyright: ignore[reportAttributeAccessIssue]
            "/namespaces/" + self._get_mounted_bucket() + "/permissions",  # pyright: ignore[reportOperatorIssue]
        )
