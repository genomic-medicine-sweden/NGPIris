#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import argparse
import os
import json
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcp.hcp import HCPManager
from hci import hci

##############################################

@click.group()
def legacy_download():
    """Downloads or deletes files on the old NGS buckets on the HCP"""
    return

@legacy_download.command()
@click.pass_context
def check(ctx, hcpm, args, pretty):
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
                if args.query in i:
                    print("check:",i)

        except:
            print(f"File(s) does not exists: {args.query}")

    else:
        obj = hcpm.get_object(args.key) # Get object with key.

@legacy_download.command()
@click.pass_context
def download(ctx, hcpm, args, pretty):
    """Download files using query, e.g. runid or sample name."""

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

@legacy_download.command()
@click.pass_context
def delete(ctx, hcpm, args):
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


def arg():
    parser = argparse.ArgumentParser(prog="downloader.py")
    requiredNamed = parser.add_argument_group("required arguments")
    requiredUpload = parser.add_argument_group("additional required arguments for upload")

    requiredNamed.add_argument("-ep", "--endpoint", help="endpoint url")
    requiredNamed.add_argument("-aki", "--aws_access_key_id", help="aws access key id")
    requiredNamed.add_argument("-sak", "--aws_secret_access_key", help="aws secret access key")
    requiredNamed.add_argument("-b", "--bucket", help="bucket name")
    requiredNamed.add_argument("-p", "--password", help="file with passwords for HCI")

    parser.add_argument("-q", "--query", nargs="?", action="store", type=str, help="Specify search query, e.g. sample name")
    parser.add_argument("-i", "--index", nargs="?", action="store", type=str, help="Specify index from HCI to parse")
    parser.add_argument("-o", "--output", nargs="?", action="store", type=str, help="Specify file to store outputs")
    parser.add_argument("-k", "--key", help="The path (key) to the file on the HCP you want to download")

    parser.add_argument("--download", action="store_true", help="Use when download")
    parser.add_argument("--delete", action="store_true", help="Use when delete")
    parser.add_argument("--check", action="store_true", help="Only prints results")
    
    args = parser.parse_args()

    return args


def main():
    args = arg()
    hcpm = HCPManager(args.endpoint, args.aws_access_key_id, args.aws_secret_access_key)
    hcpm.attach_bucket(args.bucket)

    hci.create_template(args)    
    token = hci.generate_token(args) 
    pretty = json.loads(hci.query(token, args.index))

    if args.download:
        download(hcpm, args, pretty)

    elif args.delete:
        delete(hcpm, args)
    
    elif args.check:
        check(hcpm, args, pretty)

if __name__ == "__main__":
    main()
