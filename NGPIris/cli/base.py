import click
import logging
import sys

from NGPIris import log, logformat
from NGPIris.hcp import HCPManager
from NGPIris.hci import HCIManager
from NGPIris.hcp.interactive import HCPInteracter
from NGPIris.preproc import preproc
from NGPIris.cli.functions import delete, search, upload, download
from NGPIris.cli.utils import utils

@click.group()
@click.option('-c',"--credentials", help="File containing ep, id & key",type=click.Path(),required=True)
@click.option("-b","--bucket",help="Bucket name",type=str,required=True)
@click.option("-ep","--endpoint",help="Endpoint URL override",type=str,default="")
@click.option("-id","--access_key_id",help="Amazon key identifier override",type=str,default="")
@click.option("-key","--access_key",help="Amazon secret access key override",type=str,default="")
@click.option("-p","--password",help="NGPintelligence password", type=str, default="")
@click.option("-l","--logfile",type=click.Path(),help="Logs activity to provided file",default="")
@click.version_option()
@click.pass_context
def root(ctx, endpoint, access_key_id, access_key, bucket, credentials, password, logfile):
    """NGP intelligence and repository interface software"""
    c = preproc.read_credentials(credentials)

    ep = endpoint if endpoint else c.get('endpoint','')
    aid = access_key_id if access_key_id else c.get('aws_access_key_id','') 
    key = access_key if access_key else c.get('aws_secret_access_key','')
    pw = password if password else c.get('ngpi_password', '')

    ctx.obj = {}
    hcpm = HCPManager(ep, aid, key, bucket=bucket)
    hcpm.attach_bucket(bucket)
    hcpm.test_connection()
    ctx.obj["hcpm"] = hcpm
    interact = HCPInteracter(hcpm)
    ctx.obj['interactive'] = interact

    if pw:
        hcim = HCIManager(pw)
        ctx.obj["hcpi"] = hcim

    if logfile != "":
        fh = logging.FileHandler(logfile)
        fh.setFormatter(logformat)
        log.addHandler(fh)


root.add_command(delete)
root.add_command(search)
root.add_command(upload)
root.add_command(download)
root.add_command(utils)


def main():
    pass

if __name__ == "__main__":
    main()
