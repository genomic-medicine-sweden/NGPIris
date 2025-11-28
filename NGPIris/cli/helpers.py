
import os
import sys
import click
from click.core import Context
from boto3 import set_stream_logger

from NGPIris import HCPHandler

def add_trailing_slash(path: str) -> str:
    """
    Add a trailing slash ("/") to `path`.

    :param path: Arbitrary string
    :type path: str

    :return: Arbitrary string with `"/"` at the end
    :rtype: str
    """
    if not path[-1] == "/":
        path += "/"
    return path

def create_HCPHandler(context: Context) -> HCPHandler:  # noqa: N802
    """
    Returns a `HCPHandler` based on the given command `context`.

    :param context: The `click` context from the entered command
    :type context: Context

    :return: An `HCPHandler` instance based on the given command `context`
    :rtype: HCPHandler
    """
    if context.parent:
        parent_context = context.parent
    else:
        # Should never happen
        click.echo(
            """
            Something went wrong with the subcommand and parent command relation
            """,
            err=True,
        )
        sys.exit(1)

    credentials: str | None = parent_context.params.get("credentials")

    if credentials:
        hcp_credentials = credentials
    elif os.environ.get("NGPIRIS_CREDENTIALS_PATH", None):
        hcp_credentials = os.environ["NGPIRIS_CREDENTIALS_PATH"]
    else:
        endpoint: str = click.prompt(
            "Please enter your tenant endpoint",
        )

        aws_access_key_id: str = click.prompt(
            "Please enter your base64 hashed aws_access_key_id",
        )

        aws_secret_access_key: str = click.prompt(
            "Please enter your md5 hashed aws_secret_access_key",
            hide_input=True,
            confirmation_prompt=True,
        )

        hcp_credentials = {
            "endpoint": endpoint,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }

    debug: bool | None = parent_context.params.get("debug")
    transfer_config: str | None = parent_context.params.get("transfer_config")
    if transfer_config:
        hcp_h = HCPHandler(hcp_credentials, custom_config_path=transfer_config)
    else:
        hcp_h = HCPHandler(hcp_credentials)

    if debug:
        set_stream_logger(name="")
        click.echo(hcp_h.transfer_config.__dict__)

    return hcp_h