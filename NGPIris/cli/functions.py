#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import os
import json

from NGPIris import log

##############################################


@click.command()
@click.argument("query")
@click.option("-i","--index",help="NGPi index name")
@click.option("-m", "--mode",help="Search mode", type=click.Choice(['ngpi','ngpr'], case_sensitive=False),default='ngpr')
@click.pass_obj
def search(ctx, query, index, mode):
    """List all file hits for a given query by directly calling HCP"""
  
    #Todo: Input search by file-with-list-of-items

    found_objs = ctx['hcpm'].search_objects(query)
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
    ctx['interactive'].delete_interactive(query, force)

@click.command()
@click.argument("input")
@click.option('-o',"--output",help="Destination file name on HCP", default="")
@click.option('-t',"--tag", default="None", help="Tag for downstream pipeline execution")
@click.option('-m',"--meta",help="Local path for metadata file",default=f"")
@click.option('-f',"--force",help="Overwrites any remote file with same name if present",is_flag=True, default=False)
@click.option('-s',"--silent",help="Suppresses file progress output",is_flag=True,default=False)
@click.option('-a',"--atypical",help="Allows upload of non-fastq file", is_flag=True,default=False)
@click.pass_obj
def upload(ctx, input, output, tag, meta, force, silent,atypical):
    """Upload fastq files / fastq folder structure"""
    ctx['interactive'].upload_interactive(input, output, fastq_only=(not atypical), force=force, metadata=meta, silent=silent)

@click.command()
@click.argument("query")
@click.option('-o',"--output",help="Specify output file to write to",default="")
@click.option("-m", "--mode",help="Search mode", type=click.Choice(['ngpi','ngpr','none','legacy-ngpi'], case_sensitive=False),default='ngpr')
@click.option('-s',"--silent",help="Suppresses file progress output",is_flag=True,default=False)
@click.option('-f',"--force",help="Overwrites any local file with same name if present",is_flag=True, default=False)
@click.pass_obj
def download(ctx, query, output,mode, silent,force):
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
        ctx['interactive'].download_interactive(query, destination=output, force=force, silent=silent)
 
    elif mode =="none":
        obj = ctx['hcpm'].get_object(query) # Get object with key.
        ctx['hcpm'].download_file(obj, output, force=force, callback=(not silent)) # Downloads file.

def main():
    pass

if __name__ == "__main__":
    main()
