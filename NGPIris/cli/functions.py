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
from NGPIris.preproc import preproc

##############################################


@click.command()
@click.argument("query")
@click.option("-i","--index",help="NGPi index name")
@click.option("-o","--output",help="Specify output file to write to",default="")
@click.option("-m", "--mode",help="Search mode", type=click.Choice(['ngpi','ngpr'], case_sensitive=False),default='ngpr')
@click.pass_obj
def search(ctx, query, index, output, mode):
    """List all file hits for a given query by directly calling HCP"""
  
    #Todo: Input search by file-with-list-of-items

    found_objs = ctx['hcpm'].search_objects(query,mode=mode)
    if mode == "ngpr":
        if not (found_objs is None) and len(found_objs) > 0:
            for obj in found_objs:
                log.info(obj.key)
        else:
            log.info(f'No results found for: {query}')

    elif mode == "ngpi":
        hcim = ctx['hcim']

        hcim.create_template(index, query)
        token = hcim.generate_token()

        #if verbose:
        #    resp = hcim.query(token)
        #    pretty = json.loads(resp)
        #    click.secho(json.dumps(pretty, indent=4))

        results = hcim.pretty_query(token)
        for item in results:
            md = item["metadata"]
            hci_name = md["HCI_displayName"]
            path = md["samples_Fastq_paths"]
            string = "".join(path).strip("[]").strip("{]}'")
            lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")
            log.info(f"Metadata file: {hci_name}")
        for i in lst:
            if query in i or query in os.path.basename(i):
                log.info("File: ",i)
                name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 

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

    #Defaults output to input name
    if output == "":
        output = os.path.basename(input)
    #If output is folder. Default file name to input name
    elif output[-1] in ["/","\\"]:
        output = os.path.join(output, os.path.basename(input))

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
                    log.warning(f"{f} is not a valid upload file: {e}")
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
            log.warning(f"{input} is not a valid upload file: {e}")
            sys.exit(-1)

    if file_lst == []:
        log.error(f"{input} could not be uploaded to NGPr. Try using an atypical upload")
    for file_pg in file_lst:
        if silent:
            ctx['hcpm'].upload_file(file_pg, output, callback=False)
        else:
            ctx['hcpm'].upload_file(file_pg, output)
        #time.sleep(2)
        log.info(f"Uploaded: {file_pg}")

    if meta != "":
        meta_fn = Path(meta).name
        # Uploads associated json files.
        if silent:
            ctx['hcpm'].upload_file(meta, os.path.join(dstfld, meta_fn), callback=False)
        else:
            ctx['hcpm'].upload_file(meta, os.path.join(dstfld, meta_fn))

@click.command()
@click.argument("query")
@click.option('-o',"--output",help="Specify output file to write to",default="")
@click.option("-m", "--mode",help="Search mode", type=click.Choice(['ngpi','ngpr','none','legacy-ngpi'], case_sensitive=False),default='ngpr')
@click.option('-s',"--silent",help="Suppresses file progress output",is_flag=True,default=False)
@click.pass_obj
def download(ctx, query, output,mode, silent):
    """Download files using a given query"""

    #Defaults output to input name
    if output == "":
        output = os.path.basename(query)
    #If output is folder. Default file name to input name
    elif output[-1] in ["/","\\"]:
        output = os.path.join(output, os.path.basename(query))

    if mode == "ngpi" or mode == "ngpi-legacy":
        hcim = ctx['hcim']
        hcim.create_template(index, query)
        token = hcim.generate_token()
        results = hcim.pretty_query(token)

        if mode == "ngpi-legacy":
            for item in results:
                md = item["metadata"]
                path = md["samples_Fastq_paths"]
            for i in path:
                obj = ctx["hcpm"].get_object(i) # Get object with json.
                if obj is not None:
                    ctx["hcpm"].download_file(obj, f"{destination}/{os.path.basename(i)}") # Downloads file.
                else:
                    log.error(f"File: '{s}' does not exist in bucket '{bucket}' on the HCP")

        else:
            for item in results:
                md = item["metadata"]
                path = md["samples_Fastq_paths"]
                string = "".join(path).strip("[]").strip("{]}'")
                lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")

            for i in lst:
                if query in os.path.basename(i) or query in i:
                    if not silent:
                        s = os.path.basename(i)
                        log.info("Downloading:",s.replace(".fastq.gz", ".fasterq").strip())
                    name = s.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 
                    obj = ctx["hcpm"].get_object(name) # Get object with json.
                if obj is not None:
                    ctx["hcpm"].download_file(obj, f"{destination}/{os.path.basename(name)}") # Downloads file.
                else:
                    log.error(f"File: '{name}' does not exist in bucket '{bucket}' on the HCP")

    elif mode == "ngpr":
        found_objs = ctx['hcpm'].search_objects(query)
        if len(found_objs) == 0:
            log.info(f"File: {query} does not exist on {ctx['hcpm'].bucket.name}")
        elif len(found_objs) > 1:
            for obj in found_objs:
                log.info(f"Found {len(found_objs)} files matching query")
                log.info(f"Download {obj}? [Y/N]")
                sys.stdout.write(f"[--] Do you wish to download {obj.key} on {ctx['hcpm'].bucket.name}? [Y/N]?\n")
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    obj = ctx['hcpm'].get_object(query) # Get object with key.
                    #Default output name to key
                    if output == "":
                        output = obj.key
                    #If output is folder. Default file name to obj.key
                    elif output[-1] in ["/","\\"]:
                        output = os.path.join(output, obj.key)
                    if silent:
                        ctx['hcpm'].download_file(obj, output, force=True, callback=False) # Downloads file.
                    else:
                        ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.
                    #log.info(f"Downloaded {obj.key}"

        elif len(found_objs) == 1:
            obj = ctx['hcpm'].get_object(query) # Get object with key.
            if silent:
                ctx['hcpm'].download_file(obj, output, force=True, callback=False) # Downloads file.
            else:
                ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.
 
    elif mode =="none":
        obj = ctx['hcpm'].get_object(query) # Get object with key.
        if silent:
            ctx['hcpm'].download_file(obj, output, force=True, callback=False) # Downloads file.
        else:
            ctx['hcpm'].download_file(obj, output, force=True) # Downloads file.

def main():
    pass

if __name__ == "__main__":
    main()
