import click

from .downloader import download
from .uploader import upload

@click.group()
@click.option("-ep","--endpoint",help="Endpoint URL",type=str)
@click.option("-id","--access_key_id",help="Amazon key identifier",type=str)
@click.option("-key","--access_key",help="Amazon secret access key",type=str)
@click.option("-b","--bucket",help="Bucket name",type=str)
@click.pass_context
def root(ctx, endpoint, access_key_id, access_key, bucket):
    """HCP interfacing tool"""
    ctx.obj = {}

root.add_command(upload)
root.add_command(download)
