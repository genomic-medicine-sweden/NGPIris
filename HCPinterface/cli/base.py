import click

from .downloader import download
from .uploader import upload
from .legacy_downloader import legacy_download

@click.group()
@click.pass_context
def root():
    """HCP interfacing tool"""

root.add_command(upload)
root.add_command(download)
root.add_command(legacy_download)
