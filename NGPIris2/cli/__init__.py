
import click
from click.core import Context, Argument, Option
from json import dumps

from NGPIris2.hcp import HCPHandler

def get_HCPHandler(context : Context)-> HCPHandler:
    return context.obj["hcph"]

def format_list(list_of_things : list) -> str:
    list_of_buckets = list(map(lambda s : s + "\n", list_of_things))
    return "".join(list_of_buckets).strip("\n")

@click.group()
@click.argument("credentials")
@click.pass_context
def cli(context : Context, credentials : str):
    context.ensure_object(dict)
    context.obj["hcph"] = HCPHandler(credentials)

@cli.command()
@click.argument("file")
@click.argument("bucket")
@click.pass_context
def upload(context : Context, file : str, bucket : str):
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.upload_file(file)

@cli.command()
def download():
@cli.command()
@click.pass_context
def list_buckets(context : Context):
    hcph : HCPHandler = get_HCPHandler(context)
    click.echo(format_list(hcph.list_buckets()))

@cli.command()
@click.argument("bucket")
@click.option(
    "-no", 
    "--name-only", 
    help = "Output only the name of the objects instead of all the associated metadata", 
    default = False
)
@click.pass_context
def list_objects(context : Context, bucket : str, name_only : bool):
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    objects_list = hcph.list_objects(name_only)
    if name_only:
        click.echo(format_list(objects_list))
    else: 
        out = []
        for d in objects_list:
            out.append(dumps(d, indent = 4, default = str) + "\n")
        click.echo("".join(out))