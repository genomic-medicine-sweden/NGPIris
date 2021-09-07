#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from HCPInterface import log, TIMESTAMP
from HCPInterface.hcp import HCPManager
from HCPInterface.io import io

##############################################

@click.command()
@click.pass_obj
@click.option('-q',"--query",help="Specific search query", default="")
@click.option("-f", "--file",help="The path to the file containing a list of queries",default="")
def search(ctx, query, file):
    """List all file hits for a given query"""
    if query != "":
        found_objs = ctx["hcpm"].search_objects(query)
        if len(found_objs) > 0:
            for obj in found_objs:
                log.info(obj)
        else:
            log.info(f'No results found for: {query}')
                
    elif file != "":
        #Read the query file line by line and store in list
        infile = open(file, 'r')
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
        log.info('A query or file needs to be specified if you are using the "search" option')

@click.command()
@click.option('-q',"--query",help="Specific search query", default="")
@click.option('-f',"--force",is_flag=True,default=False)
@click.pass_obj
def delete(ctx,query,force):
    """Delete a file on the HCP"""

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
@click.option('-i',"input", type=click.Path(exists=True), required=True)
@click.option('-d',"--destination",help="Target directory to put files on HCP")
@click.option('-t',"--tag", default="None", help="Tag for downstream pipeline execution")
@click.option('-f',"--force",is_flag=True,default=False,help="Removes remote file in case of name collision")
@click.option('-m',"--meta",help="Local path for generated metadata file",default="{}/meta-{}.json".format(os.getcwd(), TIMESTAMP))
@click.pass_obj
def upload(ctx, input, destination, tag, force,meta):
    """Upload fastq files / fastq folder structure"""
    meta_fn = meta
    file_lst = []

    if os.path.isdir(input):
        #Recursively loop over all folders
        for root, dirs, files in os.walk(folder):
            log.debug("{} {} {}".format(root,dirs,files))
            for f in files:
                try:
                    io.verify_fq_suffix(os.path.join(root,f))
                    io.verify_fq_content(os.path.join(root,f))
                    io.generate_tagmap(os.path.join(root,f), tag, meta_fn)
                    file_lst.append(os.path.join(root,f))
                except Exception as e:
                    log.debug("{} is not a valid upload file".format(f))
    else:
        input = os.path.abspath(input)
        try:
            io.verify_fq_suffix(input)
            io.verify_fq_content(input)
            io.generate_tagmap(input, tag, meta_fn)
            file_lst.append(input)
        except Exception as e:
            log.debug("{} is not a valid upload file".format(input))


    for file_pg in file_lst:
        ctx["hcpm"].upload_file(file_pg, destination, force=force)
        log.info("Uploading: {}".format(file_pg))

    # Uploads associated json files.
    ctx["hcpm"].upload_file(meta_fn, destination, force=force)


@click.command()
@click.option('-d',"--destination",help="Specify destination file to write to",required=True)
@click.option('-q',"--query",help="Specific search query", default="", required=True)
@click.option('-f',"--fast",help="Downloads without searching (Faster)", is_flag=True,default=False)
@click.pass_obj
def download(ctx, destination, query,fast):
    """Download files using a given query"""
    if not fast:
        found_objs = ctx["hcpm"].search_objects(query)
        if len(found_objs) == 0:
            log.info("File: {} does not exist on {}".format(query, ctx["hcpm"].bucket.name))
        elif len(found_objs) > 1:
            for obj in found_objs:
                log.info("Found {} files matching query".format(len(found_obj)))
                log.info("Download {}? [Y/N]".format(obj))
                sys.stdout.write("[--] Do you wish to download {0} on {1}? [Y/N]?\n".format(obj.key, ctx["hcpm"].bucket.name))
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    obj = ctx["hcpm"].get_object(query) # Get object with key.
                    ctx["hcpm"].download_file(obj, destination, force=True) # Downloads file.
                    #log.info("Downloaded {}".format(obj.key))

        elif len(found_objs) == 1:
            obj = ctx["hcpm"].get_object(query) # Get object with key.
            ctx["hcpm"].download_file(obj, destination, force=True) # Downloads file.
            #log.info("Downloaded {}".format(obj.key))
    elif fast:
        obj = ctx["hcpm"].get_object(query) # Get object with key.
        ctx["hcpm"].download_file(obj, destination, force=True) # Downloads file.
        #log.info("Downloaded {}".format(obj.key))
        

def main():
    pass

if __name__ == "__main__":
    main()
