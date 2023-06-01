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
        hcpi = ctx['hcpi']

        hcpi.create_template(index, query)
        token = hcpi.generate_token()

        #if verbose:
        #    resp = hcpi.query(token)
        #    pretty = json.loads(resp)
        #    click.secho(json.dumps(pretty, indent=4))

        results = hcpi.pretty_query(token)
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
@click.argument('file_paths', nargs=-1, type=click.Path(exists=True))
@click.option('--prefix', default='', help='Prefix path added to file basename in final remote key')
@click.option('--skip-error', is_flag=True, help='Skip exception raise and continue with next file')
@click.option('--result-json', default='', help='Local path to which json result summary is written')
@click.pass_obj
def quick_upload(ctx, file_paths, prefix, skip_error, result_json):
    """Upload local files to the HCP in a quick and dirty fashion.

    Usage:
        quick_upload <file_paths>... [options]
    """
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
        hcpi = ctx['hcpi']
        hcpi.create_template(index, query)
        token = hcpi.generate_token()
        results = hcpi.pretty_query(token)

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

@click.command()
@click.argument("keywords", nargs=-1)
@click.option('--output-path', default=os.getcwd(), type=click.Path(exists=True), help='Output directory to download to')
@click.option('--absolute-key', is_flag=True, help='Process input key_pattern as absolute path')
@click.option('--skip-prompt', is_flag=True, help='Skip prompt for verifying number of files to download')
@click.option('--skip-error', is_flag=True, help='Skip exception raise and continue with next file')
@click.option('--result-json', default='', help='Local path to which json result summary is written')
@click.option('--force', is_flag=True, help='Force overwrite of existing files')
@click.pass_obj
def quick_download(ctx, keywords, output_path, absolute_key, skip_prompt, skip_error, result_json, force):
    """Download remote keys from the HCP in a quick and dirty fashion.

    Usage:
        quick_download <keywords>... [options]
    """
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
