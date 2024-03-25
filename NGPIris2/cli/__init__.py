
import click
from click.core import Context, Argument, Option

from NGPIris2.hcp import HCPHandler

@click.group()
@click.argument("credentials")
@click.pass_context
def cli(context : Context, credentials : str):
    context.ensure_object(dict)
    context.obj["hcph"] = HCPHandler(credentials)

@cli.command()
def upload():
    click.echo("Test")

@cli.command()
def download():
@cli.command()
@click.pass_context
def list_buckets(context : Context):
    hcph : HCPHandler = context.obj["hcph"]
    click.echo(hcph.list_buckets())

    pass