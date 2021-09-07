#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from HCPInterface import log, WD
from HCPInterface.hcp import HCPManager
from HCPInterface.hci import hci as HCI

##############################################


def query_hci(query, index, password):
    HCI.create_template(index, query)
    token = HCI.generate_token(password)
    hci_query = HCI.pretty_query(token)

    return hci_query

@click.group()
@click.option("-i", "--index", type=str,default="",help="Specify index from HCI to parse",required=True)
@click.option("-p","--password",default="",help="File with HCI password",required=True)
@click.pass_context
def hci(ctx, index, password):
    """HCI dependent commands"""
    ctx.obj["index"] = index
    ctx.obj["password"] = password


@hci.command()
@click.option('-q',"--query",help="Specific search query", default="", required=True)
@click.option("-k", "--key",help="The path to the key-file of files to check for",default="")
@click.pass_obj
def check(ctx, query, key):
    """Basically a dry run download"""
    if query != "":
        try:
            results= query_hci(query, ctx["index"], ctx["password"])
            for item in results:
                itm = item["metadata"]
                meta = itm["HCI_displayName"]
                samples = itm["samples_Fastq_paths"]
                string = "".join(samples).strip("[]").strip("{]}'")
                lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")
            log.info("Metadata file: {}".format(meta))
            for i in lst:
                if query in i or query in os.path.basename(i):
                    log.info("check: ",i)
                    name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 

        except:
            log.info("File(s) does not exists: {}".format(query))

    elif key != "":
        obj = ctx["hcpm"].get_object(key) # Get object with key.

@hci.command()
@click.option('-d',"--destination",help="Specify destination file to write to",required=True)
@click.option('-l',"--legacy",help="Legacy mode to download files on the old NGS buckets",default=False,is_flag=True)
@click.option('-q',"--query",help="Specific search query", default="", required=True)
@click.option("-k", "--key",help="The path to the key-file on the HCP you want to download",default="")
@click.pass_obj
def download(ctx, destination, legacy, query, key):
    """Download files using query for RunID or Sample name."""
    if query != "":
        results= query_hci(query, ctx["index"], ctx["password"])

        if legacy:
            for item in results:
                itm = item["metadata"]
                samples = itm["samples_Fastq_paths"]
            for i in samples:
                obj = ctx["hcpm"].get_object(i) # Get object with json.
                if obj is not None:
                    ctx["hcpm"].download_file(obj, "{0}/{1}".format(destination,os.path.basename(i))) # Downloads file.
                else:
                    log.error("File: '{0}' does not exist in bucket '{1}' on the HCP".format(s,bucket))

        elif not legacy:
            for item in results:
                itm = item["metadata"]
                samples = itm["samples_Fastq_paths"]
                string = "".join(samples).strip("[]").strip("{]}'")
                lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")

            for i in lst:
                if query in os.path.basename(i) or query in i:
                    s = os.path.basename(i)
                    log.info("downloading:",s.replace(".fastq.gz", ".fasterq").strip())
                    name = s.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 
                    obj = ctx["hcpm"].get_object(name) # Get object with json.
                    if obj is not None:
                        ctx["hcpm"].download_file(obj, "{0}/{1}".format(destination,os.path.basename(name))) # Downloads file.
                    else:
                        log.error("File: '{0}' does not exist in bucket '{1}' on the HCP".format(name, bucket))

    elif key != "":
        obj = ctx["hcpm"].get_object(key) # Get object with key.
        ctx["hcpm"].download_file(obj, destination) # Downloads file.

def main():
    pass

if __name__ == "__main__":
    main()