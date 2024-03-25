
import click

@click.group()
def cli():
    pass

@cli.command()
def upload():
    click.echo("Test")

@cli.command()
def download():
    pass