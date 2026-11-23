import sys
from pathlib import Path
from typing import TYPE_CHECKING

from tqdm import tqdm
from types_boto3_s3.type_defs import AccessControlPolicyTypeDef

from NGPIris.hcp.exceptions import (
    MetadataCouldNotBeFoundError,
    NoStatusCodeSuppliedError,
    ObjectDoesNotExistError,
    OperationNotPermittedError,
    UnknownStatusCodeError,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from botocore.exceptions import ClientError
    from types_boto3_s3.type_defs import DeleteObjectOutputTypeDef


def create_access_control_policy(
    user_ID_permissions: dict[str, str],
) -> AccessControlPolicyTypeDef:
    grants = []
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
        grants.append(grantee)
    return AccessControlPolicyTypeDef(
        {
            "Grants": grants,
        }
    )


def raise_path_error(path: str) -> None:
    """
    Raise FileNotFoundError if the system path does not exist.

    :param path: Local system path

    :raises FileNotFoundError: If `path` does not exist
    """
    if not Path(path).exists():
        raise FileNotFoundError('"' + path + '"' + " does not exist")


def client_error_response_code_handler(
    error: ClientError,
    operation: str,
    obj: str | dict | None = None,
    bucket: str | None = None,
) -> None:
    """
    Check for status codes from response. If it's anything but 200, raise
    errors.

    :param response: The response dictionary from an S3 operation

    :param operation:
        The type of operation that will be displayed in the error
        message.
    """
    metadata = error.response.get("ResponseMetadata", {})
    if metadata:
        status_code: int | None = metadata.get("HTTPStatusCode")
        match status_code:
            case 200:
                pass
            case 403:
                msg = (
                    "You do not have enough permissions (status code 403) for "
                    "the following operation: " + operation
                )
                raise OperationNotPermittedError(msg)
            case 404:
                match obj:
                    case str():
                        bucket_str = "' in bucket '" + bucket if bucket else ""
                        msg = (
                            "The object '"
                            + obj
                            + bucket_str
                            + "' that was part of the operation could not be "
                            "found"
                        )
                    case dict():
                        msg = (
                            "The object that was part of the operation could"
                            "not be found: " + str(obj)
                        )
                    case _:
                        msg = (
                            "An object that was part of the operation could "
                            "not be found"
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
        msg = str(MetadataCouldNotBeFoundError.__doc__)
        raise MetadataCouldNotBeFoundError(msg)


def operation_response_code_handler(
    response: DeleteObjectOutputTypeDef,
    operation: str,
    obj: str | dict | None = None,
    bucket: str | None = None,
) -> None:
    """
    Check for status codes from response. If it's anything but 200, raise
    errors.

    :param response: The response dictionary from an S3 operation

    :param operation:
        The type of operation that will be displayed in the error
        message.
    """
    metadata = response.get("ResponseMetadata", {})
    if metadata:
        status_code: int | None = metadata.get("HTTPStatusCode")
        match status_code:
            case 200:
                pass
            case 403:
                msg = (
                    "You do not have enough permissions (status code 403) for "
                    "the following operation: " + operation
                )
                raise OperationNotPermittedError(msg)
            case 404:
                match obj:
                    case str():
                        bucket_str = "' in bucket '" + bucket if bucket else ""
                        msg = (
                            "The object '"
                            + obj
                            + bucket_str
                            + "' that was part of the operation could not be "
                            "found"
                        )
                    case dict():
                        msg = (
                            "The object that was part of the operation could"
                            "not be found: " + str(obj)
                        )
                    case _:
                        msg = (
                            "An object that was part of the operation could "
                            "not be found"
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
        msg = str(MetadataCouldNotBeFoundError.__doc__)
        raise MetadataCouldNotBeFoundError(msg)


def progress_bar_handler[**P, R](
    show_progress_bar: bool,
    file_size: int,
    desc: str,
    method: Callable[P, R],
    method_kwargs: dict,
) -> None:
    """
    Helper function for progressbar logic.
    """

    def _progress_bar_handler(*args: P.args, **kwargs: P.kwargs) -> None:
        if show_progress_bar:
            with tqdm(
                total=file_size,
                unit="B",
                unit_scale=True,
                desc=desc,
            ) as pbar:
                kwargs["Callback"] = lambda bytes_transferred: pbar.update(
                    bytes_transferred,
                )
                method(*args, **kwargs)
        else:
            method(*args, **kwargs)

    _progress_bar_handler(**method_kwargs)  # pyright: ignore[reportCallIssue]
