#!/usr/bin/env python

"""
Module for file validation and generation
"""

import csv
import gzip
import json
import os
import re

from NGPIris import log, WD, TIMESTAMP

from NGPIris.hcp.errors import (UnattachedBucketError, LocalFileExistsError,
                                     UnknownSourceTypeError, MismatchChecksumError,
                                     ConnectionError, MissingCredentialsError)


def verify_fq_suffix(fn):
    """Makes sure the provided file looks like a fastq"""

    #Check suffix
    if not fn.endswith(("fastq.gz","fq.gz","fastq","fq")):
        raise Exception(f"File {fn} is not a fastq")
    log.debug(f'Verified that {fn} is a zipped fastq')
    #Check for unresolved symlink
    if os.path.islink(fn):
        if not os.path.exists(os.readlink(fn)):
            raise Exception(f"File {fn} is an unresolved symlink")


def verify_fq_content(fn):
    """Makes sure fastq file contains fastq data"""
    nuc = set("ATCGN\n")
    lineno = 0
    f1 = gzip.open(fn, "r")
    for line in f1:
        line = line.decode('UTF-8')
        lineno = lineno + 1 
        if lineno == 1:
            corr = re.match("^@",line)
        elif lineno == 2:
            corr = set(line) <= nuc
        elif lineno == 3:
            corr = re.match("^\+",line)
        elif lineno == 4:
            lineno = 0

        if not corr:
            raise Exception(f"File{fn} does not look like a fastq at line {lineno}: {line}")
    f1.close()
    
    if lineno % 4 != 0:
        raise Exception(f"File {fn} is missing data")
    log.debug(f'Verified that {fn} resembles a fastq')


def generate_tagmap(fn, tag, output_path="{}/meta-{}.json".format(os.getcwd(), TIMESTAMP)):
    """Creates a json file with filenames and tags"""
    # Check if meta exists, else make it
    if not os.path.exists(output_path):
        data = {fn: {'tag': tag}}
        with open(output_path, 'w') as out:
            json.dump(data, out, indent=4)
    else:
        # Read the current meta
        with open(output_path, 'r') as inp:
            current_data = json.load(inp)

        # New data
        new_data = {fn: {'tag': tag}}
        updated_data = {**current_data, **new_data}

        # Write updated
        with open(output_path, 'w') as out:
            json.dump(updated_data, out, indent=4)

    log.debug(f'Generated metadata file {output_path}')
    return output_path

def read_credentials(credentials_path):
    """Reads sensitive information from a json-file"""
    with open(credentials_path, 'r') as inp:
        c = json.load(inp)
    try:
        pw = c['ngpi_password']
    except Exception as e:
        pass
    log.debug("Credentials file successfully utilized")

    if c.get('endpoint') is None or c.get('aws_access_key_id') is None or c.get('aws_secret_access_key') is None:
        raise MissingCredentialsError('One or more values missing from provided json.')
        log.error('One or more critical values missing from provided json.')
        sys.exit(-1)

    if c.get('ngpi_password') is None:
        log.warning('Credentials file lack NGPi credentials')

    return c

def folder_to_list(folder, metadata=""):
    file_lst = []
    md_lst= []
    #Recursively loop over all folders
    for root, dirs, files in os.walk(folder):
        for f in files:
            try:
                #Auto-generate metadata
                #if metadata == "":
                #    metadata = preproc.generate_tagmap(os.path.join(root,f), tag,"meta-{}.json".format(TIMESTAMP))
                file_lst.append(os.path.join(root,f))
            except Exception as e:
                log.warning(f"{f} is not a valid upload file: {e}")
    return [file_lst, metadata]

def verify_upload_folder(folder, metadata=""):
    file_lst = []
    md_lst= []
    #Recursively loop over all folders
    for root, dirs, files in os.walk(folder):
        for f in files:
            try:
                verify_fq_suffix(os.path.join(root,f))
                verify_fq_content(os.path.join(root,f))
                #Auto-generate metadata
                #if metadata == "":
                #    metadata = preproc.generate_tagmap(os.path.join(root,f), tag,"meta-{}.json".format(TIMESTAMP))
                file_lst.append(os.path.join(root,f))
            except Exception as e:
                log.warning(f"{f} is not a valid upload file: {e}")
    return [file_lst, metadata]

def verify_upload_file(source, metadata=""):
    source = os.path.abspath(source)
    dst = []
    try:
        verify_fq_suffix(source)
        verify_fq_content(source)
        #Auto-generate metadata
        #if metadata == "":
        #    metadata = preproc.generate_tagmap(source, tag)
        dst = source
        file_lst.append(mdfile)
    except Exception as e:
        log.warning(f"{source} is not a valid upload file: {e}")
    return [dst, metadata]
