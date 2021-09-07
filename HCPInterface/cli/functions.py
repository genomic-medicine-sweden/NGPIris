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
@click.option("-k", "--key",help="The path to the key-file containing a list of queries",default="")
def search(ctx, query, key):
    """Search for file"""
    if query != "":
        found_objs = ctx["hcpm"].search_objects(query)
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
        objects = ctx["hcpm"].get_objects()
        
        #Search for each item in query file
        qdict = {}
        for line in lines:
            log.info('[-- query: {line} --]')
            found_objs = ctx["hcpm"].search_objects(line)
            if len(found_objs) > 0:
                for obj in found_objs:
                    log.info(obj)
            else:
                log.info('Nothing found')
    else:
        log.info('A query or key file needs to be specified if you are using the "search" option')

@click.command()
@click.option('-q',"--query",help="Specific search query", default="")
@click.option('-f',"--force",is_flag=True,default=False)
@click.pass_obj
def delete(ctx,query,force):
    """Delete file on the HCP"""

    objs = ctx["hcpm"].search_objects(query) # Get object with query
    if len(objs) < 1:
        log.info("File: {0} does not exist on {1}".format(query, ctx["hcpm"].bucket.name))
    else:
        log.info("Found {0} files matching query".format(len(objs)))
        for obj in objs: 
            if not force: 
                sys.stdout.write("[--] You are about to delete the file {0} on {1}, are you sure? [Y/N]?\n".format(obj.key, ctx["hcpm"].bucket.name))
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    ctx["hcpm"].delete_object(obj) # Delete file.
                    time.sleep(2)
                    log.info("[--] Deleting file \"{0}\" \n".format(query))
                else:
                    log.info("Skipped deleting \"{}\"\n".format(obj.key))
            elif force:
                    ctx["hcpm"].delete_object(obj) # Delete file.
                    time.sleep(2)
                    log.info("[--] Deleting file \"{0}\" \n".format(query))


@click.command()
@click.option('-i',"--input",help="Item to upload", type=click.Path())
@click.option('-d',"--destination",help="Target directory to put files on HCP")
@click.pass_obj
def upload(ctx, input, destination):
    """Upload fastq file to the HCP"""

    # List and upload files provided bu path flag.
    if os.path.isdir(input):
        if glob.glob("{}/*.fasterq".format(input)):
            file_lst = glob.glob("{}/*.fasterq".format(input))
        else:
            file_lst = glob.glob("{}/*.fastq.gz".format(input)) 

        for file_pg in files_lst:
            ctx["hcpm"].upload_file(file_pg, os.path.join(destination))
            log.info("uploading: {}".format(file_pg))
    else:
        # Uploads associated json files.
        ctx["hcpm"].upload_file(input,  os.path.join(destination))
 

def main():
    pass

if __name__ == "__main__":
    main()
