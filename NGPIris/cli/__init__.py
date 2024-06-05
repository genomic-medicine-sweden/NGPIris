
import click
from click.core import Context
from json import dumps, dump
from os import path

from NGPIris.hcp import HCPHandler

def get_HCPHandler(context : Context)-> HCPHandler:
    return context.obj["hcph"]

def format_list(list_of_things : list) -> str:
    list_of_buckets = list(map(lambda s : s + "\n", list_of_things))
    return "".join(list_of_buckets).strip("\n")

@click.group()
@click.argument("credentials")
@click.version_option(package_name = "NGPIris")
@click.pass_context
def cli(context : Context, credentials : str):
    """
    NGP Intelligence and Repository Interface Software, IRIS. 
    
    CREDENTIALS refers to the path to the JSON credentials file.
    """
    context.ensure_object(dict)
    context.obj["hcph"] = HCPHandler(credentials)

@cli.command()
@click.argument("file-or-folder")
@click.argument("bucket")
@click.pass_context
def upload(context : Context, file_or_folder : str, bucket : str):
    """
    Upload files to an HCP bucket/namespace. 
    
    FILE-OR-FOLDER is the path to the file or folder of files to be uploaded.

    BUCKET is the name of the upload destination bucket.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    if path.isdir(file_or_folder):
        hcph.upload_folder(file_or_folder)
    else:
        hcph.upload_file(file_or_folder)

@cli.command()
@click.argument("object")
@click.argument("bucket")
@click.argument("local_path")
@click.pass_context
def download(context : Context, object : str, bucket : str, local_path : str):
    """
    Download files from an HCP bucket/namespace.

    OBJECT is the name of the object to be downloaded.

    BUCKET is the name of the upload destination bucket.

    LOCAL_PATH is the path to where the downloaded objects are to be stored locally.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.download_file(object, local_path)

@cli.command()
@click.argument("object")
@click.argument("bucket")
@click.pass_context
def delete_object(context : Context, object : str, bucket : str):
    """
    Delete an object from an HCP bucket/namespace. 

    OBJECT is the name of the object to be deleted.

    BUCKET is the name of the bucket where the object to be deleted exist.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.delete_object(object)

@cli.command()
@click.argument("folder")
@click.argument("bucket")
@click.pass_context
def delete_folder(context : Context, folder : str, bucket : str):
    """
    Delete a folder from an HCP bucket/namespace. 

    FOLDER is the name of the folder to be deleted.

    BUCKET is the name of the bucket where the folder to be deleted exist.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    hcph.delete_folder(folder)

@cli.command()
@click.pass_context
def list_buckets(context : Context):
    """
    List the available buckets/namespaces on the HCP.
    """
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
    """
    List the objects in a certain bucket/namespace on the HCP.

    BUCKET is the name of the bucket in which to list its objects.
    """
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

@cli.command()
@click.argument("bucket")
@click.argument("search_string")
@click.option(
    "-cs", 
    "--case_sensitive", 
    help = "Use case sensitivity?", 
    default = False
)
@click.pass_context
def simple_search(context : Context, bucket : str, search_string : str, case_sensitive : bool):
    """
    Make simple search using substrings in a bucket/namespace on the HCP.

    BUCKET is the name of the bucket in which to make the search.

    SEARCH_STRING is any string that is to be used for the search.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    hcph.mount_bucket(bucket)
    list_of_results = hcph.search_objects_in_bucket(search_string, case_sensitive)
    click.echo("Search results:")
    for result in list_of_results:
        click.echo("- " + result)

@cli.command()
@click.argument("bucket")
@click.pass_context
def test_connection(context : Context, bucket : str):
    """
    Test the connection to a bucket/namespace.

    BUCKET is the name of the bucket for which a connection test should be made.
    """
    hcph : HCPHandler = get_HCPHandler(context)
    click.echo(hcph.test_connection(bucket))

@click.command()
@click.option(
    "--path",
    help = "Path for where to put the new credentials file",
    default = ""
)
@click.option(
    "--name",
    help = "Custom name for the credentials file",
    default = "credentials"
)
def iris_generate_credentials_file(path : str, name : str):
    """
    Generate blank credentials file for the HCI and HCP. 

    WARNING: This file will store sensitive information (such as passwords) in plaintext.
    """
    credentials_dict = {
        "hcp" : {
            "endpoint" : "",
            "aws_access_key_id" : "",
            "aws_secret_access_key" : ""
        },
        "hci" : {
            "username" : "",
            "password" : "",
            "address" : "",
            "auth_port" : "",
            "api_port" : ""
        }
    }
    file_path = path + name + ".json"
    with open(file_path, "w") as f:
        dump(credentials_dict, f, indent = 4)

    