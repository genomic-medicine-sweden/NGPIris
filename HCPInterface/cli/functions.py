#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from HCPInterface.hcp import HCPManager
from HCPInterface.hci import hci

##############################################

@click.command()
@click.pass_obj
@click.option('-t',"--type",required=True,help="Method to identify file",type=click.Choice(['query','key'],case_sensitive=False))
def check(ctx, type, hcpm, pretty):
    """Checks for file existence"""
    if type=="query":
        try:
            f = pretty
            results= f["results"]
            for item in results:
                itm = item["metadata"]
                meta = itm["HCI_displayName"]
                samples = itm["samples_Fastq_paths"]
                string = "".join(samples).strip("[]").strip("{]}'")
                lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")
            print(f"Metadata file: {meta}")
            for i in lst:
                if query in i or query in os.path.basename(i):
                    print("check:",i)
                    name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 

        except:
            print("File(s) does not exists: {}".format(query))

    elif type=="key":
        obj = hcpm.get_object(key) # Get object with key.

@click.command()
@click.option('-o',"--output",help="Specify output file to write to",required=True)
@click.option('-t',"--type",required=True,help="Method to identify file",type=click.Choice(['query','key'],case_sensitive=False))
@click.option('-l'"--legacy",help="Legacy mode to download files on the old NGS buckets",default=False,is_flag=True)
@click.pass_obj
def download_files(ctx, output, hcpm, pretty):
    """Download files using query, e.g. runid or sample name."""
    if type=="query":
        f = pretty
        results= f["results"]

        if legacy:
            for item in results:
                itm = item["metadata"]
                samples = itm["samples_Fastq_paths"]
            for i in samples:
                obj = hcpm.get_object(i) # Get object with json.
                if obj is not None:
                    hcpm.download_file(obj, "{0}/{1}".format(output,os.path.basename(i))) # Downloads file.
                else:
                    print("File: '{0}' does not exist in bucket '{1}' on the HCP".format(s,bucket))

        elif not legacy:
            for item in results:
                itm = item["metadata"]
                samples = itm["samples_Fastq_paths"]
                string = "".join(samples).strip("[]").strip("{]}'")
                lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")

            for i in lst:
                if query in os.path.basename(i) or query in i:
                    s = os.path.basename(i)
                    print("downloading:",s.replace(".fastq.gz", ".fasterq").strip())
                    name = s.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 
                    obj = hcpm.get_object(name) # Get object with json.
                    if obj is not None:
                        hcpm.download_file(obj, "{0}/{1}".format(output,os.path.basename(name))) # Downloads file.
                    else:
                        print("File: '{0}' does not exist in bucket '{1}' on the HCP".format(name, bucket))

    elif type=="key":
        obj = hcpm.get_object(key) # Get object with key.
        hcpm.download_file(obj, output) # Downloads file.

@click.command()
@click.pass_obj
def delete(ctx, hcpm):
    """Delete file on HCP using a key (path to object)"""

    obj = hcpm.get_object(key) # Get object with key.
    if obj is not None:
        sys.stdout.write(f"[--] You are about to delete a file in a bucket on HCP\"{key}\", are you sure? [Y/N]?\n")
        sys.stdout.flush()
        answer = sys.stdin.readline()
        if answer[0].lower() == "y":
            hcpm.delete_object(obj) # Delete file.
            time.sleep(2)
            print(f"[--] Deleting file \"{key}\" \n")
        else:
            sys.exit(f"[Error] Exiting... Did not delete the file \"{key}\"\n")
    else:
        print(f"File: {key} does not exist in the HCP")

@click.command()
@click.pass_obj
@click.option('-qf','--query-file',help="File listing queries")
def search(ctx, query_file, hcpm):
    """Search for file"""
    if query:
        found_objs = hcpm.search_objects(query)
        if len(found_objs) > 0:
            for obj in found_objs:
                print(obj)
        else:
            print(f'No results found for: {query}')
                
    elif query_file:
        #Read the query file line by line and store in list
        infile = open(query_file, 'r')
        lines = infile.readlines()
        #Remove newlines
        lines = map(lambda s: s.strip(), lines)
        
        #Load in all data on HCP
        objects = hcpm.get_objects()
        
        #Search for each item in query file
        qdict = {}
        for line in lines:
            print(f'[-- query: {line} --]')
            found_objs = hcpm.search_objects(line)
            if len(found_objs) > 0:
                for obj in found_objs:
                    print(obj)
            else:
                print('Nothing found')
    else:
        print(f'A query or query file needs to be specified if you are using the "search" option')

@click.command()
@click.option('-i',"--input",help="Item to upload", type=click.Path())
@click.option('-d',"--destination",help="Target directory to put files on HCP")
@click.pass_obj
def upload_fastq(files_pg, hcpm, input):
    """Upload fastq to HCP"""

    # List and upload files provided bu path flag.
    if os.path.isdir(input):
        if glob.glob("{}/*.fasterq".format(input)):
            file_lst = glob.glob("{}/*.fasterq".format(input))
        else:
            file_lst = glob.glob("{}/*.fastq.gz".format(input)) 

        for file_pg in files_lst:
            hcpm.upload_file(file_pg, os.path.join(destination,os.path.basename(file_pg)))
            print(f"uploading: {file_pg}")
    else:
        # Uploads associated json files.
        hcpm.upload_file(input,  os.path.join(destination,os.path.basename(file_pg)))
 

def main():
    pass

if __name__ == "__main__":
    main()
