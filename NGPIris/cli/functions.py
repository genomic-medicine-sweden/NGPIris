#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from pathlib import Path

from NGPIris import log, TIMESTAMP
from NGPIris.hcp import HCPManager
from NGPIris.preproc import preproc

##############################################

@click.command()
@click.argument("query")
@click.option("-f", "--file",help="The path to the file containing a list of queries",default="")
@click.pass_obj
def search(ctx, query, file):
    """List all file hits for a given query"""
    if query != "":
        found_objs = ctx['hcpm'].search_objects(query)
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
        objects = ctx['hcpm'].get_objects()
        
        #Search for each item in query file
        qdict = {}
        for line in lines:
            log.info(f"[-- query: {line} --]")
            found_objs = ctx['hcpm'].search_objects(line)
            if len(found_objs) > 0:
                for obj in found_objs:
                    log.info(obj)
            else:
                log.info('Nothing found')
    else:
        log.info('A query or file needs to be specified if you are using the "search" option')

@click.command()
@click.argument("query")
@click.option('-f',"--force",is_flag=True,default=False)
@click.pass_obj
def delete(ctx,query,force):
    """Delete a file on the HCP"""

    objs = ctx['hcpm'].search_objects(query) # Get object with query
    if len(objs) < 1:
        log.info(f"File: {query} does not exist on {ctx['hcpm'].bucket.name}")
    else:
        hits = list()
        for obj in objs:
            hits.append(obj.key)
        log.info(f"Found {len(objs)} entries matching query '{query}':")
        log.info(f"{hits}")
        for obj in objs: 
            if not force: 
                sys.stdout.write(f"You are about to delete the file {obj.key} " \
                                 f"on {ctx['hcpm'].bucket.name}, are you sure? [Y/N/Q]?\n")
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    ctx['hcpm'].delete_object(obj) # Delete file.
                    time.sleep(2)
                    log.info(f"Deleted file {obj.key} ")
                elif answer[0].lower() == "q":
                    break
                else:
                    log.info(f"Skipped deleting {obj.key} ")
            elif force:
                    ctx['hcpm'].delete_object(obj) # Delete file.
                    time.sleep(2)
                    log.info(f"Deleted file {obj.key} ")


@click.command()
@click.argument("input")
@click.option('-o',"--output",help="Destination file name on HCP", default="")
@click.option('-t',"--tag", default="None", help="Tag for downstream pipeline execution")
@click.option('-m',"--meta",help="Local path for generated metadata file",default=f"")
@click.option('-s',"--silent",help="Suppresses file progress output",is_flag=True,default=False)
@click.option('-a',"--atypical",help="Allows upload of non-fastq file", is_flag=True,default=False)
@click.pass_obj
def upload(ctx, input, output, tag, meta,silent,atypical):
    """Upload fastq files / fastq folder structure"""
    file_lst = []

    #Workaround
    if output == "":
        output = os.path.basename(input)

    dstfld = Path(output)
    dstfld = dstfld.parent
    if dstfld.parts == ():
        dstfld = ""

    if os.path.isdir(input):
        #Recursively loop over all folders
        for root, dirs, files in os.walk(folder):
            for f in files:
                try:
                    if not atypical:
                        preproc.verify_fq_suffix(os.path.join(root,f))
                        preproc.verify_fq_content(os.path.join(root,f))
                    if meta != "":
                        preproc.generate_tagmap(os.path.join(root,f), tag, meta)
                    file_lst.append(os.path.join(root,f))
                except Exception as e:
                    log.debug(f"{f} is not a valid upload file: {e}")
    else:
        input = os.path.abspath(input)
        try:
            if not atypical: 
                preproc.verify_fq_suffix(input)
                preproc.verify_fq_content(input)
            if meta != "":
                preproc.generate_tagmap(input, tag, meta)
            file_lst.append(input)
        except Exception as e:
            log.debug(f"{input} is not a valid upload file: {e}")
            sys.exit(-1)


    for file_pg in file_lst:
        if silent:
            ctx['hcpm'].upload_file(file_pg, output, callback="")
        else:
            ctx['hcpm'].upload_file(file_pg, output)
        #time.sleep(2)
        log.info(f"Uploaded: {file_pg}")

    if meta != "":
        meta_fn = Path(meta).name
        # Uploads associated json files.
        if silent:
            ctx['hcpm'].upload_file(meta, os.path.join(dstfld, meta_fn), callback="")
        else:
            ctx['hcpm'].upload_file(meta, os.path.join(dstfld, meta_fn))

@click.command()
@click.argument("query")
@click.option('-o',"--output",help="Specify output file to write to",required=True)
@click.option('-f',"--fast",help="Downloads without searching (Faster)", is_flag=True,default=False)
@click.option('-s',"--silent",help="Suppresses file progress output",is_flag=True,default=False)
@click.pass_obj
def download(ctx, query, output,fast, silent):
    """Download files using a given query"""
    if not fast:
        found_objs = ctx['hcpm'].search_objects(query)
        if len(found_objs) == 0:
            log.info(f"File: {query} does not exist on {ctx['hcpm'].bucket.name}")
        elif len(found_objs) > 1:
            for obj in found_objs:
                log.info(f"Found {len(found_obj)} files matching query")
                log.info(f"Download {obj}? [Y/N]")
                sys.stdout.write(f"[--] Do you wish to download {obj.key} on {ctx['hcpm'].bucket.name}? [Y/N]?\n")
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    obj = ctx['hcpm'].get_object(query) # Get object with key.
                    if silent:
                        ctx['hcpm'].download_file(obj, output, force=True,callback="") # Downloads file.
                    else:
                        ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.
                    #log.info(f"Downloaded {obj.key}"

        elif len(found_objs) == 1:
            obj = ctx['hcpm'].get_object(query) # Get object with key.
            if silent:
                ctx['hcpm'].download_file(obj, output, force=True,callback="") # Downloads file.
            else:
                ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.
 
    elif fast:
        obj = ctx['hcpm'].get_object(query) # Get object with key.
        if silent:
            ctx['hcpm'].download_file(obj, output, force=True,callback="") # Downloads file.
        else:
            ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.

def main():
    pass

if __name__ == "__main__":
    main()
