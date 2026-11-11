from json import load
from pathlib import Path
from typing import TYPE_CHECKING

from icecream import ic

from NGPIris.credentials.exceptions import (
    MissingCredentialsError,
    PartialCredentialsError,
)

if TYPE_CHECKING:
    from NGPIris.credentials.types import (
        Credentials,
        CredentialsHCI,
        CredentialsHCP,
    )


def check_if_emtpy_credentials(
    credentials: CredentialsHCP | CredentialsHCI,
) -> bool:
    d = credentials.keys()
    ic(d)
    pass


def check_if_partial_credentials(
    credentials: CredentialsHCP | CredentialsHCI,
) -> bool:
    pass


def parse_credentials(credentials_path: str) -> Credentials:
    """
    Parse credentials at the given ``credentials_path``.

    :param credentials_path: Path to credentials
    :return: Parsed credentials
    """
    with Path(credentials_path).open() as inp:
        credentials: Credentials = load(inp)
        hcp_c = credentials.get("hcp")
        hci_c = credentials.get("hci")

        hcp_c_exists = bool(hcp_c)
        hci_c_exists = bool(hci_c)

        neither_exists = not (hcp_c_exists or hci_c_exists)

        if neither_exists:
            msg = (
                "Missing `hcp` or `hci` entries in the credentials file. "
                "Please the provided credentials file template"
            )
            raise MissingCredentialsError(msg)

        empty_credential_checks = [
            check_if_emtpy_credentials(hcp_c) if hcp_c else True,
            check_if_emtpy_credentials(hci_c) if hci_c else True,
        ]

        if all(empty_credential_checks):
            msg = (
                "Missing entries in all fields in the credentials file. "
                "Please enter your credentials in either the "
                "`hcp` or `hci` fields, or both of them"
            )
            raise MissingCredentialsError(msg)

        partial_credential_checks = [
            check_if_partial_credentials(hcp_c) if hcp_c else False,
            check_if_partial_credentials(hci_c) if hci_c else False,
        ]

        either_contains_partial_credentials = any(partial_credential_checks)
        if either_contains_partial_credentials:
            msg = (
                "Partial credentials detected in the credentials file. "
                "Please enter your credentials in either the "
                "`hcp` or `hci` fields, or both of them"
            )
            raise PartialCredentialsError(msg)

        return credentials
