from traceback import print_tb

from click.testing import CliRunner
from conftest import CustomConfig
from icecream import ic

from NGPIris.cli import cli

# ruff: noqa: D103


def test_basic_cli(custom_config: CustomConfig) -> None:
    runner = CliRunner()
    result = runner.invoke(cli)
    ic(result.output)


def test_list_buckets(custom_config: CustomConfig) -> None:
    runner = CliRunner()
    creds = custom_config.credentials_path
    ic(creds)

    result = runner.invoke(cli, ["-c " + str(creds), "list-buckets"])
    if result.exc_info:
        tb = result.exc_info[2]
        print_tb(tb)
    ic(result.output)


def test_list_objects(custom_config: CustomConfig) -> None:
    runner = CliRunner()
    bucket = custom_config.test_bucket
    creds = custom_config.credentials_path
    result = runner.invoke(
        cli, ["-c " + str(creds), "list-objects", str(bucket)]
    )
    ic(result.output)
