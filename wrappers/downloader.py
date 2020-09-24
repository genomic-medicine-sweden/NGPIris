#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import glob
import argparse
import os
import schema
import json
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcp.hcp import HCPManager
from hci import hci

##############################################
def check(hcpm, args, pretty):
    if args.query:
        f = pretty
        results= (f["results"])
        for item in results:
            itm = (item["metadata"])
            meta = itm["HCI_displayName"]
            samples = (itm["hcp_fastqpaths"])
            string = "".join(samples).strip("[]").strip("{]}'")
            lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").split(",")
        print(f"Metadata file: {meta}")
        for i in lst:
            if args.query in os.path.basename(i) or args.query in i:
                print("check:",i)
                name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 

    else:
        obj = hcpm.get_object(args.key) # Get object with key.

# Download files using query, e.g. runid or sample name.
def download(hcpm, args, pretty):
    if args.query:
        f = pretty
        results= (f["results"])
        for item in results:
            itm = (item["metadata"])
            samples = (itm["hcp_fastqpaths"])
            string = "".join(samples).strip("[]").strip("{]}'")
            lst = string.replace('"','').replace("\\","").replace("[","").replace("]","").split(",")

        for i in lst:
            if args.query in os.path.basename(i) or args.query in i:
                print("downloading:",i.replace(".fastq.gz", ".fasterq").strip())
                name = i.replace(".fastq.gz", ".fasterq").strip() # Replace suffix. 
                obj = hcpm.get_object(name) # Get object with json.
                hcpm.download_file(obj, f"{args.output}/"+os.path.basename(name)) # Downloads file.

    else:
        obj = hcpm.get_object(args.key) # Get object with key.
        hcpm.download_file(obj, args.output) # Downloads file.


# Delete file on HCP using a key (path to object)
def delete(hcpm, args):
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
