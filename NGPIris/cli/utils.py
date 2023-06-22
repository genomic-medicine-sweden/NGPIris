#!/usr/bin/env python3

# Downloads or deletes files from selected bucket on the HCP.

import click
import glob
import os
import json
import sys
import time

from NGPIris import log, WD
from NGPIris.hcp import HCPManager
from NGPIris.hci import hci as HCI

##############################################


def query_hci(query, index, password):
    HCI.create_template(index, query)
    token = HCI.generate_token(password)
    hci_query = HCI.pretty_query(token)

    return hci_query

@click.group()
@click.pass_context
def utils(ctx):
    """Advanced commands for specific purposes"""
    pass

@utils.command()
@click.option('-i',"--index",help="List indices present on NGPi", default="all", required=True)
@click.pass_obj
def indices(ctx, index):
    """Displays file hits for a given query"""
    hcpi = ctx['hcpi']
    token = hcpi.generate_token()
    index_list = hcpi.get_index(token, index=index)
    pretty = json.dumps(index_list)
    print(json.dumps(pretty, indent=4))

@utils.command()
@click.pass_obj
def list_buckets(ctx):
    """Lists all administered buckets for the provided credentials"""
    hcpm = ctx['hcpm']
    ls = hcpm.list_buckets()
    log.info(f"Administrated buckets: {ls}")

@utils.command()
@click.pass_obj
def test_connection(ctx):
    """Tests credentials for validity"""
    if not (40 in log._cache or 30 in log._cache):
        log.info(f"A successful connection has been established!")

@utils.command()
@click.argument('file_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--prefix', default='', help='Prefix path added to file basename in final remote key')
@click.option('--skip-error', is_flag=True, help='Skip exception raise and continue with next file')
@click.option('--result-json', default='', help='Local path to which json result summary is written')
@click.pass_obj
def quick_upload(ctx, file_paths, prefix, skip_error, result_json):
    """Download files using a sequential list"""
    if len(file_paths) < 1:
        print('Input at least one file path')
        return

    # Normalize input paths
    file_paths = [os.path.abspath(os.path.normpath(path)) for path in file_paths]

    log.info(f'Attempting upload of {len(file_paths)} files to the HCP')

    completed = []
    existed = []
    failed = []
    for file_path in file_paths:
        file_basename = os.path.basename(file_path)
        remote_key = os.path.join(prefix, file_basename)

        if ctx['hcpm'].get_object(remote_key):
            log.info(f'{remote_key} already exists')
            existed.append(remote_key)
            continue
        try:
            ctx['hcpm'].upload_file(file_path, remote_key)
            log.info(f'Uploaded {file_path} to {remote_key}')

            # Perform a sanity check on object existance after upload
            if not ctx['hcpm'].get_object(remote_key):
                log.info(f'Failed to verify upload to {remote_key}')
                failed.append(remote_key)
                continue
            else:
                completed.append(remote_key)

        except Exception as e:
            log.info(f'Failed to upload to {remote_key}')
            failed.append(remote_key)
            if not skip_error:
                raise

    if result_json:
        log.info(f'Writing summary to {result_json}')
        with open(result_json, 'w') as file_out:
            json_info = {'completed': completed,
                         'existed': existed,
                         'failed': failed}
            json.dump(json_info, file_out, indent=4)

@utils.command()
@click.argument("keywords", nargs=-1)
@click.option('--output-path', default=os.getcwd(), type=click.Path(exists=True), help='Output directory to download to')
@click.option('--absolute-key', is_flag=True, help='Process input key_pattern as absolute path')
@click.option('--skip-prompt', is_flag=True, help='Skip prompt for verifying number of files to download')
@click.option('--skip-error', is_flag=True, help='Skip exception raise and continue with next file')
@click.option('--result-json', default='', help='Local path to which json result summary is written')
@click.option('--force', is_flag=True, help='Force overwrite of existing files')
@click.pass_obj
def quick_download(ctx, keywords, output_path, absolute_key, skip_prompt, skip_error, result_json, force):
    """Download files using a sequential list"""
    if len(keywords) < 1:
        print('Input at least one keyword to search for')
        return

    completed = []
    existed = []
    failed = []

    found_objects = []
    log.info(f'Finding objects to download...')
    for keyword in keywords:
        if absolute_key:
            log.info(f'Getting object with keyword: {keyword}')
            found = ctx['hcpm'].get_object(keyword)
            if found:
                found_objects.append(found)
            else:
                failed.append(keyword)
        else:
            log.info(f'Searching for objects containing keyword: {keyword}')
            found = ctx['hcpm'].search_objects(keyword)
            found_objects.extend(found)

    if len(found_objects) < 1:
        log.info(f'No objects found matching any keyword')
        return

    if not skip_prompt:
        input(f'Found {len(found_objects)} objects. Press enter/return to download them...')

    log.info(f'Attempting download of {len(found_objects)} files from the HCP')
    for obj in found_objects:
        object_basename = os.path.basename(obj.key)
        local_path = os.path.join(output_path, object_basename)

        if os.path.exists(local_path) and not force:
            log.info(f'{local_path} already exists')
            existed.append(local_path)
            continue

        try:
            ctx['hcpm'].download_file(obj, local_path, force=force)
            log.info(f'Downloaded {obj.key} to {local_path}')
            completed.append(local_path)

        except Exception as e:
            log.info(f'Failed to download {obj.key}')
            failed.append(local_path)
            if not skip_error:
                raise

    if result_json:
        log.info(f'Writing summary to {result_json}')
        with open(result_json, 'w') as file_out:
            json_info = {'completed': completed,
                         'existed': existed,
                         'failed': failed}
            json.dump(json_info, file_out, indent=4)

def main():
    pass

if __name__ == "__main__":
    main()
