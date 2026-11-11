from typing_extensions import Literal, TypedDict


class Credentials(TypedDict, total=False):
    hcp: CredentialsHCP
    hci: CredentialsHCI


class CredentialsHCP(Credentials):
    endpoint: str
    username: str
    password: str


class CredentialsHCI(Credentials):
    address: str
    username: str
    password: str
    realm: Literal["HCI", "LOCAL"]
