import sys
from collections.abc import Callable
from pathlib import Path
from typing import ParamSpec, TypeVar

from icecream.icecream import ic

from NGPIris.hcp.exceptions import (
    MetadataCouldNotBeFoundError,
    NoBucketMountedError,
    NoStatusCodeSuppliedError,
    ObjectDoesNotExistError,
    OperationNotPermittedError,
    UnknownStatusCodeError,
)


def create_access_control_policy(user_ID_permissions: dict[str, str]) -> dict:  # noqa: D103
    access_control_policy: dict[str, list] = {
        "Grants": [],
    }
    for user_ID, permission in user_ID_permissions.items():
        if permission not in [
            "FULL_CONTROL",
            "WRITE",
            "WRITE_ACP",
            "READ",
            "READ_ACP",
        ]:
            print("Invalid permission option:", permission)
            sys.exit()
        grantee = {
            "Grantee": {
                "ID": user_ID,
                "Type": "CanonicalUser",
            },
            "Permission": permission,
        }
        access_control_policy["Grants"].append(grantee)
    return access_control_policy


def raise_path_error(path: str) -> None:
    """
    Raise FileNotFoundError if the system path does not exist.

    :param path: Local system path
    :type path: str

    :raises FileNotFoundError: If `path` does not exist
    """
    if not Path(path).exists():
        raise FileNotFoundError('"' + path + '"' + " does not exist")


P = ParamSpec("P")
T = TypeVar("T")


def check_mounted(method: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator for checking if a bucket is mounted. This is meant to be used by
    class methods, hence the possibly odd typing.

    :param method: An arbitrary class method of the `HCPHandler` class
    :type method: Callable[ParamSpec("P"), TypeVar("T")]

    :return: A decorated class method of the `HCPHandler` class
    :rtype: Callable[ParamSpec("P"), TypeVar("T")]
    """

    def check_if_mounted(*args: P.args, **kwargs: P.kwargs) -> T:
        self = args[0]
        if not self.bucket_name:  # pyright: ignore[reportAttributeAccessIssue]
            msg = "No bucket is mounted"
            raise NoBucketMountedError(msg)
        return method(*args, **kwargs)

    return check_if_mounted


def operation_response_code_handler(response: dict, operation: str) -> None:
    """
    Check for status codes from response. If it's anything but 200, raise
    errors.

    :param response: The response dictionary from an S3 operation
    :type response: dict

    :param operation:
        The type of operation that will be displayed in the error
        message.
    :type operation: str

    :rtype: None
    """
    metadata: dict = response.get("ResponseMetadata", {})
    if metadata:
        status_code: int | None = metadata.get("HTTPStatusCode")
        match status_code:
            case 200:
                pass
            case 403:
                msg = (
                    "You do not have enough permissions (status code 403) for "
                    "the followingoperation: " + operation
                )
                raise OperationNotPermittedError(msg)
            case 404:
                msg = (
                    "An object that was part of the operation could not be "
                    "found"
                )
                raise ObjectDoesNotExistError(msg)
            case None:
                msg = "No status code was supplied in the operation response"
                raise NoStatusCodeSuppliedError(msg)
            case _:
                msg = (
                    "The status code "
                    + str(status_code)
                    + " is not among known status codes. Please report this to "
                    + "the NGP development team"
                )
                raise UnknownStatusCodeError(msg)
    else:
        msg = "MetadataCouldNotBeFoundError.__doc__"
        raise MetadataCouldNotBeFoundError(msg)
