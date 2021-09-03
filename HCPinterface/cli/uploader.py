#!/usr/bin/env python3

# Wrapper that uploads FASTQ files.
# Uploads the files to selected bucket on the HCP.

import click
import glob
import argparse
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hcp.hcp import HCPManager

##############################################
# List files that will be uploaded on the HCP.

def files(args):
    """Depending on if the files are compressed or not"""
    file_lst = glob.glob(args.path)
    return file_lst

@click.group()
def upload():
    """Uploads the files to the selected bucked on the HCP"""
    return


@upload.command()
@click.pass_context
def upload_fastq(ctx, args, files_pg, hcpm):
    """Upload FASTQ and json to selected bucket on HCP."""

    # List and upload files provided by path flag.
    for file_pg in files_pg:
        if len(hcpm.search_objects(f"{args.remotepath}/"+os.path.basename(file_pg))) < 1:
            try:
                hcpm.upload_file(file_pg, f"{args.remotepath}/"+os.path.basename(file_pg))
                print(f"uploading: {args.remotepath}/{os.path.basename(file_pg)}")
            except Exception as e:
                print(e)
                continue
        else:
            print(f"Object already exists: {args.remotepath}/{os.path.basename(file_pg)}")
            continue

    if args.filepath:
        # Uploads single file.
        hcpm.upload_file(f"{args.filepath}",
                            f"{args.remotepath}/"+os.path.basename(args.filepath))


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
    requiredUpload.add_argument("-f", "--filepath",
                            help="path to single file")
    requiredUpload.add_argument("-r", "--remotepath",
                            help="path to directory to put files on HCP")
    requiredUpload.add_argument("-q", "--query",
                            help="search for files on HCP")

    args = parser.parse_args()

    return args


def main():
    args = arg()

    # Connect to HCP
    hcpm = HCPManager(args.endpoint, args.aws_access_key_id, args.aws_secret_access_key)
    hcpm.attach_bucket(args.bucket)

    if args.path:
        files_pg = files(args)
        upload_fastq(args, files_pg, hcpm)

    if args.filepath:
        files_pg = []
        upload_fastq(args, files_pg, hcpm)

    if args.query:
        search(args,hcpm)


if __name__ == "__main__":
    main()
