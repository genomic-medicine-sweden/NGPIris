import click
import sys

from HCPInterface import log, version
from HCPInterface.hcp import HCPManager
from HCPInterface.cli.functions import check, download, delete, search, upload

@click.group()
@click.option("-ep","--endpoint",help="Endpoint URL",type=str)
@click.option("-id","--access_key_id",help="Amazon key identifier",type=str)
@click.option("-key","--access_key",help="Amazon secret access key",type=str)
@click.option("-b","--bucket",help="Bucket name",type=str, required=True)
@click.option("--skip-hci", default=False, help="Skips calling the HCI. Requires --index & --password",is_flag=True)
@click.option("-i", "--index", type=str,default="",help="Specify index from HCI to parse")
@click.option("-pw","--password",default="",help="File with HCI password")
@click.version_option(version)
@click.pass_context
def root(ctx, endpoint, access_key_id, access_key, bucket, skip_hci, index, password):
    """HCP interfacing tool"""
    ctx.obj = {}
    hcpm = HCPManager(endpoint, access_key_id, access_key)
    hcpm.attach_bucket(bucket)

    if not skip_hci and (index == "" or password == ""):
        log.error("HCI requires an --index and --password")
        sys.exit(-1)
    
    if skip_hci:
        pass
    else:
        hci.create_template(index, query)    
        token = hci.generate_token(password) 
        pretty = json.loads(hci.query(token, index))
        ctx.obj["pretty"] = pretty

    ctx.obj["hcpm"] = hcpm


root.add_command(check)
root.add_command(download)
root.add_command(delete)
root.add_command(search)
root.add_command(upload)
