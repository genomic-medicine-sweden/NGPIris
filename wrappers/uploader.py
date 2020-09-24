#!/usr/bin/env python3

# Wrapper that uploads FASTQ files.
# Uploads the files to selected bucket on the HCP.

import glob
import argparse
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcp.hcp import HCPManager

##############################################
# List files that will be uploaded on the HCP.
# Depending on if the files are compressed or not.
def files(args):
    if glob.glob(f"{args.path}/*.fasterq"):
        file_lst = glob.glob(f"{args.path}/*.fasterq")
    else:
        file_lst = glob.glob(f"{args.path}/*.fastq.gz") 
    return file_lst


# Upload FASTQ and json to selected bucket on HCP.
def upload_fastq(args, files_pg):
    hcpm = HCPManager(args.endpoint, args.aws_access_key_id, args.aws_secret_access_key)
    hcpm.attach_bucket(args.bucket)

    # List and upload files provided bu path flag.
    for file_pg in files_pg:
        hcpm.upload_file(file_pg, args.run+"/"+os.path.basename(file_pg))
        print(f"uploading: {file_pg}")

    # Uploads associated json files.
    hcpm.upload_file(f"{args.jsonpath}",
                        f"{args.run}/"+os.path.basename(args.jsonpath))

    

def arg():
    parser = argparse.ArgumentParser(prog="uploader.py")
    requiredNamed = parser.add_argument_group('required arguments')
    requiredUpload = parser.add_argument_group('additional required arguments for upload')

    requiredUpload.add_argument("-ep", "--endpoint",
                            help="endpoint url")
    requiredUpload.add_argument("-aki", "--aws_access_key_id",
                            help="aws access key id")
    requiredUpload.add_argument("-sak", "--aws_secret_access_key",
                            help="aws secret access key")
    requiredUpload.add_argument("-b", "--bucket",
                            help="bucket name")
    requiredUpload.add_argument("-p", "--path",
                            help="path to directory with files for upload")
    requiredNamed.add_argument("-j", "--jsonpath",
                            required=True,
                            help="path to json file with metadata")
    requiredNamed.add_argument("-r", "--run",
                            help="run name")
    requiredNamed.add_argument("-s", "--sample",
                            required=True,
                            help="samplename")

    args = parser.parse_args()

    return args


def main():
    args = arg()
    files_pg = files(args)

    # Upload files only if validation is OK.
    upload_fastq(args, files_pg)


if __name__ == "__main__":
    main()
