#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from NGPIris import log, WD
from NGPIris.hcp import HCPManager
from NGPIris.hci import hci as HCI

##############################################


def query_hci(query, index, password):
    HCI.create_template(index, query)
    token = HCI.generate_token(password)
    hci_query = HCI.pretty_query(token)

    return hci_query

@click.group()
@click.pass_context
def utils(ctx):
    """Advanced commands for specific purposes"""
    pass

@utils.command()
@click.option('-i',"--index",help="List indices present on NGPi", default="all", required=True)
@click.pass_obj
def indices(ctx, index):
    """Displays file hits for a given query"""
    hcim = ctx['hcim']
    token = hcim.generate_token()
    index_list = hcim.get_index(token, index=index)
    pretty = json.dumps(index_list)
    print(json.dumps(pretty, indent=4))


@utils.command()
@click.option('-d',"--destination",help="Specify destination file to write to",required=True)
@click.option('-l',"--legacy",help="Legacy mode to download files on the old NGS buckets",default=False,is_flag=True)
@click.option('-q',"--query",help="Specific search query", default="", required=True)
@click.pass_obj
def hci_download(ctx, destination, legacy, query):
    """Download files matching a given query"""
    results= query_hci(query, ctx["index"], ctx["password"])

    if legacy:
        for item in results:
            itm = item["metadata"]
            samples = itm["samples_Fastq_paths"]
        for i in samples:
            obj = ctx["hcpm"].get_object(i) # Get object with json.
            if obj is not None:
                ctx["hcpm"].download_file(obj, f"{destination}/{os.path.basename(i)}") # Downloads file.
            else:
                log.error(f"File: '{s}' does not exist in bucket '{bucket}' on the HCP")

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
                    ctx["hcpm"].download_file(obj, f"{destination}/{os.path.basename(name)}") # Downloads file.
                else:
                    log.error(f"File: '{name}' does not exist in bucket '{bucket}' on the HCP")

@utils.command()
@click.argument("query")
@click.option("-m", "--mode",help="Restrict search to a file type", type=click.Choice(['all','file', 'dir'], case_sensitive=False),default='all')
@click.pass_obj
def slow_search(ctx, query, mode):
    """List all file hits for a given query by directly calling HCP"""
    if query != "":
        found_objs = ctx['hcpm'].search_objects(query,mode=mode)
        if len(found_objs) > 0:
            for obj in found_objs:
                log.info(obj.key)
        else:
            log.info(f'No results found for: {query}')
    else:
        log.info('A query or file needs to be specified if you are using the "search" option')


def main():
    pass

if __name__ == "__main__":
    main()
