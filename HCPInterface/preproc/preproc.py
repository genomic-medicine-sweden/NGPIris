#!/usr/bin/env python

"""
Module for file validation and generation
"""

import csv
import gzip
import json
import os
import re

from HCPInterface import log, WD, TIMESTAMP

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
    nuc = set("ATCG\n")
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

def generate_tagmap(fn, tag, out="{}/meta-{}.json".format(os.getcwd(), TIMESTAMP)):
    """Creates a json file with filenames and tags"""
    mdict = dict()
    mdict[fn] = {'tag':tag}
    md = open(out, "a")
    md.write(json.dumps(mdict, indent=4))
    md.close()
    log.debug(f'Generated metadata file {out}')


def read_credentials(credentials_path):
    """Set endpoint, aws id and aws key using a json-file"""
    with open(credentials_path, 'r') as inp:
        c = json.load(inp)

    ep = c['endpoint']
    aid = c['aws_access_key_id']
    key = c['aws_secret_access_key']
    log.debug("Credentials file successfully utilized")

    if not all([c['endpoint'], c['aws_access_key_id'], c['aws_secret_access_key']]):
        raise MissingCredentialsError('One or more values missing from provided json.')

    return [ep,aid,key]

def verify_metadata(fn, type=""):
    """Verifies that the metadata contains expected values"""
    if type == "covid"
        verify_covidmd(fn)
    else:
        log.error("Cannot verify metadata without providing a type""")

def verify_covidmd(fn):
    """Verifies that covid metadata contains expected values"""
    j = open(fn)
    metad = json.load(j)

    #Read fields definition
    with open(f'{WD}/credentials/covidMetadataTemplate.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        fields = next(reader)
        #for row in spamreader:
        #    print(', '.join(row))

    #Check field presence
    warns = 0    
    for f in fields:
        if not f in metad.keys():
            log.warning(f"Field '{f}' not present in {fn}")
            warns = warns + 1
    if warns > 0:
        log.error(f"{warns} warnings produced when reading metadata file")

    #Read fields definition
    with open(f'{WD}/credentials/covidMetadataAllowedValues.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        fields = next(reader)
 

    ##Check field allowed values
    ##From xls template
    #n = range(1,99)
    #nums = [f'{i:02}' for i in nums] 
    #if not j['regionkod'] in nums:
    #    log.error(f"Regionkod contains invalid value {j['regionkod']")
















