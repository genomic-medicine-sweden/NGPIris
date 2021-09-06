#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from HCPInterface import log
from HCPInterface.hcp import HCPManager
from HCPInterface.hci import hci

##############################################

@click.command()
@click.pass_obj
@click.option('-q',"--query",help="Specific search query", default="")
@click.option("-k", "--key",help="The path to the key-file of files to check for",default="")
def check(ctx, query, key):
    """Checks for file existence"""
    if query != "":
        try:
            f = ctx.obj["pretty"]
            results= f["results"]
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
        obj = ctx.obj["hcpm"].get_object(key) # Get object with key.

@click.command()
@click.option('-o',"--output",help="Specify output file to write to",required=True)
@click.option('-l'"--legacy",help="Legacy mode to download files on the old NGS buckets",default=False,is_flag=True)
@click.option('-q',"--query",help="Specific search query", default="")
@click.option("-k", "--key",help="The path to the key-file on the HCP you want to download",default="")
@click.pass_obj
def download(ctx, output):
    """Download files using query for RunID or Sample name."""
    if query != "":
        f = ctx.obj["pretty"]
        results= f["results"]

        if legacy:
            for item in results:
                itm = item["metadata"]
                samples = itm["samples_Fastq_paths"]
            for i in samples:
                obj = ctx.obj["hcpm"].get_object(i) # Get object with json.
                if obj is not None:
                    ctx.obj["hcpm"].download_file(obj, "{0}/{1}".format(output,os.path.basename(i))) # Downloads file.
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
                    obj = ctx.obj["hcpm"].get_object(name) # Get object with json.
                    if obj is not None:
                        ctx.obj["hcpm"].download_file(obj, "{0}/{1}".format(output,os.path.basename(name))) # Downloads file.
                    else:
                        log.error("File: '{0}' does not exist in bucket '{1}' on the HCP".format(name, bucket))

    elif key != "":
        obj = ctx.obj["hcpm"].get_object(key) # Get object with key.
        ctx.obj["hcpm"].download_file(obj, output) # Downloads file.

@click.command()
@click.pass_obj
@click.option('-q',"--query",help="Specific search query", default="")
@click.option("-k", "--key",help="The path to the key-file containing a list of queries",default="")
def search(ctx, query, key):
    """Search for file"""
    if query != "":
        found_objs = ctx.obj["hcpm"].search_objects(query)
        if len(found_objs) > 0:
            for obj in found_objs:
                log.info(obj)
        else:
            log.info(f'No results found for: {query}')
                
    elif key != "":
        #Read the query file line by line and store in list
        infile = open(key, 'r')
        lines = infile.readlines()
        #Remove newlines
        lines = map(lambda s: s.strip(), lines)
        
        #Load in all data on HCP
        objects = ctx.obj["hcpm"].get_objects()
        
        #Search for each item in query file
        qdict = {}
        for line in lines:
            log.info('[-- query: {line} --]')
            found_objs = ctx.obj["hcpm"].search_objects(line)
            if len(found_objs) > 0:
                for obj in found_objs:
                    log.info(obj)
            else:
                log.info('Nothing found')
    else:
        log.info('A query or key file needs to be specified if you are using the "search" option')

@click.command()
@click.pass_obj
def delete(ctx):
    """Delete file on the HCP"""

    obj = ctx.obj["hcpm"].get_object(key) # Get object with key.
    if obj is not None:
        sys.stdout.write(f"[--] You are about to delete a file in a bucket on HCP\"{key}\", are you sure? [Y/N]?\n")
        sys.stdout.flush()
        answer = sys.stdin.readline()
        if answer[0].lower() == "y":
            ctx.obj["hcpm"].delete_object(obj) # Delete file.
            time.sleep(2)
            log.info("[--] Deleting file \"{0}\" \n".format(key))
        else:
            log.error("[Error] Exiting... Did not delete the file \"{}\"\n".format(key))
            sys.exit(-1)
    else:
        log.info(f"File: {0} does not exist in the HCP".format(key))



@click.command()
@click.option('-i',"--input",help="Item to upload", type=click.Path())
@click.option('-d',"--destination",help="Target directory to put files on HCP")
@click.pass_obj
def upload(files_pg, input):
    """Upload fastq file to the HCP"""

    # List and upload files provided bu path flag.
    if os.path.isdir(input):
        if glob.glob("{}/*.fasterq".format(input)):
            file_lst = glob.glob("{}/*.fasterq".format(input))
        else:
            file_lst = glob.glob("{}/*.fastq.gz".format(input)) 

        for file_pg in files_lst:
            ctx.obj["hcpm"].upload_file(file_pg, os.path.join(destination,os.path.basename(file_pg)))
            log.info("uploading: {}".format(file_pg))
    else:
        # Uploads associated json files.
        ctx.obj["hcpm"].upload_file(input,  os.path.join(destination,os.path.basename(file_pg)))
 

def main():
    pass

if __name__ == "__main__":
    main()
