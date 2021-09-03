import click
import sys

from HCPInterface.hcp import HCPManager
from HCPInterface.cli.functions import check, download, delete, search, upload

@click.group()
@click.option("-ep","--endpoint",help="Endpoint URL",type=str)
@click.option("-id","--access_key_id",help="Amazon key identifier",type=str)
@click.option("-key","--access_key",help="Amazon secret access key",type=str)
@click.option("-b","--bucket",help="Bucket name",type=str)
@click.option('-q',"--query",help="Specific search query")
@click.option("-k", "--key",help="The path to the key-file on the HCP you want to download")
@click.option("--no-hci", default=False, help="Avoid using HCI")
@click.option("-i", "--index", type=str,default="",help="Specify index from HCI to parse")
@click.option("-pw","--password",default="",help="File with HCI password")
@click.pass_context
def root(ctx, endpoint, access_key_id, access_key, bucket, query,key,no_hci,index,password):
    """HCP interfacing tool"""
    ctx.obj = {}
    hcpm = HCPManager(endpoint, access_key_id, access_key)
    hcpm.attach_bucket(bucket)

    if not no_hci and (index == "" or password == ""):
        log.error("HCI requires an --index and --password")
        sys.exit(-1)
    
    if no_hci:
        pass
    else:
        hci.create_template(index, query)    
        token = hci.generate_token(password) 
        pretty = json.loads(hci.query(token, index))


root.add_command(check)
root.add_command(download)
root.add_command(delete)
root.add_command(search)
root.add_command(upload)
