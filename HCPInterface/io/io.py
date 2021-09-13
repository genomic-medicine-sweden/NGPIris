#!/usr/bin/env python

"""
Module for file validation and generation
"""

import gzip
import json
import os
import re

from HCPInterface import log, WD, TIMESTAMP

def verify_fq_suffix(fn):
    """Makes sure the provided file looks like a fastq"""

    #Check suffix
    if not fn.endswith any(["fastq.gz","fq.gz","fastq","fq"]):
        raise Exception("File {0} is not a zipped fastq".format(fn))
    log.debug('Verified that {0} is a zipped fastq'.format(fn))
    #Check for unresolved symlink
    if os.path.islink(fn):
        if not os.path.exists(os.readlink(fn)):
            raise Exception("File {0} is an unresolved symlink".format(fn))


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
            raise Exception("File {0} does not look like a fastq at line {1}: {2}".format(fn, lineno, line))
    f1.close()
    
    if lineno % 4 != 0:
        raise Exception("File {0} is missing data".format(fn))
    log.debug('Verified that {0} resembles a fastq'.format(fn))

def generate_tagmap(fn, tag, out="{}/meta-{}.json".format(os.getcwd(), TIMESTAMP)):
    """Creates a json file with filenames and tags"""
    mdict = dict()
    mdict[fn] = {'tag':tag}
    md = open(out, "a")
    md.write(json.dumps(mdict, indent=4))
    md.close()
    log.debug('Generated metadata file {}'.format(out))     
