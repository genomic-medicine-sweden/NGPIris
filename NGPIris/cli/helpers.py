import os
import sys
from json import load
from pathlib import Path
from typing import Any, Generator

import click
from bitmath import Byte, TiB
from boto3 import set_stream_logger
from click.core import Context
from tabulate import tabulate

from NGPIris import HCPHandler


def add_trailing_slash(path: str) -> str:
    """
    Add a trailing slash ("/") to `path`.

    :param path: Arbitrary string
    :type path: str

    :return: Arbitrary string with `"/"` at the end
    :rtype: str
    """
    if not path.endswith("/"):
        path += "/"
    return path


def create_HCPHandler(context: Context) -> HCPHandler:
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
            (
                "Something went wrong with the subcommand and parent"
                "command relation"
            ),
            err=True,
        )
        sys.exit(1)

    credentials: str | None = parent_context.params.get("credentials")
    profile: str | None = parent_context.params.get("profile")
    profile_path: str | None = parent_context.params.get("profile_path")

    if credentials:
        hcp_credentials = credentials
    elif os.environ.get("NGPIRIS_CREDENTIALS_PATH", None):
        hcp_credentials = os.environ["NGPIRIS_CREDENTIALS_PATH"]
    elif profile_path:
        if profile:
            # profile_path = os.environ.get(PROFILE_PATH_ENV_VAR)
            with Path(profile_path).open() as file:
                profiles_dict: dict = load(file)
                creds: dict | None = profiles_dict.get(profile)
                if creds:
                    hcp_credentials = creds["hcp"]
                else:
                    click.echo(
                        "No profile named" + profile + " exist", err=True
                    )
                    sys.exit(1)
        else:
            click.echo("No profile supplied with `-p`")
            sys.exit(1)
    else:
        endpoint: str = click.prompt(
            "Please enter your tenant endpoint",
        )

        aws_access_key_id: str = click.prompt(
            "Please enter your base64 hashed username (a.k.a aws_access_key_id)",
        )

        aws_secret_access_key: str = click.prompt(
            "Please enter your md5 hashed password (a.k.a aws_secret_access_key)",
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


def ensure_destination_dir(destination: str) -> Path:
    """
    Ensure that `destination` exists and return it as a `Path`.
    """
    dest_path = Path(destination)
    dest_path.mkdir(parents=True, exist_ok=True)
    return dest_path


def prompt_large_download() -> None:
    """
    Prompt for large downloads.
    """
    if not click.confirm(
        "WARNING: You are about to download more than 1 TB of data. "
        "Is this your intention?"
    ):
        sys.exit("\nAborting download")


def download_folder(
    source: str, destination_path: Path, ignore_warning: bool, hcp_h: HCPHandler
) -> None:
    """
    Helper function to `download` for downloading a folder.
    """
    prefix = "" if source == "/" else source

    cumulative_download_size = Byte(0)
    if not ignore_warning:
        click.echo("Computing download size...")
        for hcp_object in hcp_h.list_objects(prefix):
            hcp_object: dict
            cumulative_download_size += Byte(hcp_object["Size"])
            if cumulative_download_size >= TiB(1):
                prompt_large_download()

    hcp_h.download_folder(prefix, destination_path.as_posix())


def download_file(
    source: str,
    destination_path: Path,
    ignore_warning: bool,
    force: bool,
    hcp_h: HCPHandler,
) -> None:
    """
    Helper function to `download` for downloading a file.
    """
    check_size_and_ignore_warning_flag = (
        Byte(hcp_h.get_object(source)["ContentLength"]) >= TiB(1)
    ) and (not ignore_warning)
    if check_size_and_ignore_warning_flag:
        prompt_large_download()

    downloaded_source = Path(destination_path) / Path(source).name
    if downloaded_source.exists() and not force:
        sys.exit(
            "Object already exists. If you wish to overwrite the existing file,"
            " use the -f / --force option"
        )
    hcp_h.download_file(source, downloaded_source.as_posix())


def render_objects_table(
    table_data: Generator[dict[str, Any], Any, None], batch_size: int
) -> None:
    """
    Helper function for lazily displaying objects in a table with a given batch
    size.
    """
    rows = []
    positive_batch_size = batch_size > 0
    for row in table_data:
        rows.append(row)
        if positive_batch_size and (
            not len(rows) % batch_size
        ):  # Check if `len(rows)` is a mutliple of `batch_size`
            click.echo(tabulate(rows, headers="keys"))
            click.echo(
                "(Press any key to get more rows or ctrl+c to abort...)",
                nl=False,
            )
            click.getchar()
            click.clear()
    click.echo(tabulate(rows, headers="keys"))
