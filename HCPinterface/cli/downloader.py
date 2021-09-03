#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcp.hcp import HCPManager
from hci import hci

##############################################

@click.group()
@click.options('-q',"--query",help="Specific search query")
@click.options("-k", "--key",help="The path to the key-file on the HCP you want to download")
@click.options("--no-hci", default=False, help="Avoid using HCI")
@click.options("-i", "--index", type=str,default="" help="Specify index from HCI to parse")
def download(ctx, query, key, no_hci,index):
    """Downloads or deletes files from the selected bucket on the HCP"""
    hcpm = HCPManager(endpoint, access_key_id, secret_access_key)
    hcpm.attach_bucket(bucket)

    if no_hcp and index == "":
        log.error("Avoiding HCI requires use of --index flag")

    #Skip the HCI stuff if requested
    if not no_hci:
        hci.create_template(args)    
        token = hci.generate_token(args) 
        pretty = json.loads(hci.query(token, args.index))
    return

@download.command()
@click.pass_obj
def check(ctx, hcpm, pretty):
    """Checks for file existence"""
    if args.query:
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
                if args.query in i or args.query in os.path.basename(i):
                    print("check:",i)
                    name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 

        except:
            print(f"File(s) does not exists: {args.query}")

    else:
        obj = hcpm.get_object(args.key) # Get object with key.

@download.command()
@click.option('-o',"--output",help="Specify output file to write to",required=True)
@click.pass_obj
def download_files(ctx, output hcpm, pretty):
    """Download files using query, e.g. runid or sample name."""
    if args.query:
        f = pretty
        results= f["results"]
        for item in results:
            itm = item["metadata"]
            samples = itm["samples_Fastq_paths"]
            string = "".join(samples).strip("[]").strip("{]}'")
            lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").replace(";",",").split(",")

        for i in lst:
            if args.query in os.path.basename(i) or args.query in i:
                s = os.path.basename(i)
                print("downloading:",s.replace(".fastq.gz", ".fasterq").strip())
                name = s.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 
                obj = hcpm.get_object(name) # Get object with json.
                if obj is not None:
                    hcpm.download_file(obj, f"{args.output}/"+os.path.basename(name)) # Downloads file.
                else:
                    print(f"File: '{name}' does not exist in bucket '{args.bucket}' on the HCP")

    else:
        obj = hcpm.get_object(args.key) # Get object with key.
        hcpm.download_file(obj, args.output) # Downloads file.

@download.command()
@click.option('-o',"--output",help="Specify output file to write to",required=True)
@click.pass_obj
def download_legacy(ctx, output, hcpm, pretty):
    """Downloads files on the old NGS buckets"""
    if args.query:
        f = pretty
        results= f["results"]
        for item in results:
            itm = item["metadata"]
            samples = itm["samples_Fastq_paths"]
        for i in samples:
            obj = hcpm.get_object(i) # Get object with json.
            if obj is not None:
                hcpm.download_file(obj, f"{args.output}/"+os.path.basename(i)) # Downloads file.
            else:
                print(f"File: '{s}' does not exist in bucket '{args.bucket}' on the HCP")

    else:
        obj = hcpm.get_object(args.key) # Get object with key.
        hcpm.download_file(obj, args.output) # Downloads file.

@download.command()
@click.pass_obj
def delete(ctx, hcpm):
    """Delete file on HCP using a key (path to object)"""

    obj = hcpm.get_object(args.key) # Get object with key.
    if obj is not None:
        sys.stdout.write(f"[--] You are about to delete a file in a bucket on HCP\"{args.key}\", are you sure? [Y/N]?\n")
        sys.stdout.flush()
        answer = sys.stdin.readline()
        if answer[0].lower() == "y":
            hcpm.delete_object(obj) # Delete file.
            time.sleep(2)
            print(f"[--] Deleting file \"{args.key}\" \n")
        else:
            sys.exit(f"[Error] Exiting... Did not delete the file \"{args.key}\"\n")
    else:
        print(f"File: {args.key} does not exist in the HCP")

@download.command()
@click.pass_obj
@click.options('-qf','--query-file',help="File listing queries")
def search(ctx, query_file, hcpm):
    """Search for file"""
    if args.query:
        found_objs = hcpm.search_objects(args.query)
        if len(found_objs) > 0:
            for obj in found_objs:
                print(obj)
        else:
            print(f'No results found for: {args.query}')
                
    elif args.qfile:
        #Read the query file line by line and store in list
        infile = open(args.qfile, 'r')
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

def main():
    pass

if __name__ == "__main__":
    main()
