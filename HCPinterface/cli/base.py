import click

from .functions import check, download_files, download_legacy, delete, search, upload_fastq

@click.group()
@click.option("-ep","--endpoint",help="Endpoint URL",type=str)
@click.option("-id","--access_key_id",help="Amazon key identifier",type=str)
@click.option("-key","--access_key",help="Amazon secret access key",type=str)
@click.option("-b","--bucket",help="Bucket name",type=str)
@click.option('-q',"--query",help="Specific search query")
@click.option("-k", "--key",help="The path to the key-file on the HCP you want to download")
@click.option("--no-hci", default=False, help="Avoid using HCI")
@click.option("-i", "--index", type=str,default="",help="Specify index from HCI to parse")
@click.pass_context
def root(ctx, endpoint, access_key_id, access_key, bucket, query,key,no_hci,index):
    """HCP interfacing tool"""
    ctx.obj = {}
    hcpm = HCPManager(endpoint, access_key_id, secret_access_key)
    hcpm.attach_bucket(bucket)

    if no_hcp and index == "":
        log.error("Avoiding HCI requires use of --index flag")

    #Skip the HCI stuff if requested
    if not no_hci:
        hci.create_template(args)    
        token = hci.generate_token(args) 
        pretty = json.loads(hci.query(token, args.index))
    return



root.add_command(check)
root.add_command(download_files)
root.add_command(download_legacy)
root.add_command(delete)
root.add_command(search)
root.add_command(upload_fastq)
