#!/usr/bin/env python

import builtins
import click
import json
import logging
import pathlib
import pdb
import pytest
import re
import mock
import os
import sys

from HCPInterface import version, log, WD
from HCPInterface.cli.base import root

from click.testing import CliRunner
from distutils.sysconfig import get_python_lib
from unittest.mock import patch, mock_open

testWD = os.path.join(WD, '..', 'tests')
credentials_path = os.path.join(testWD, 'credentials.json')
f1target =  os.path.join("unittest","test_reads_R1.fastq.gz") 


@pytest.fixture
def runner():
    runnah = CliRunner()
    return runnah

def test_version(runner):
    res = runner.invoke(root, '--version')
    assert res.exit_code == 0
    assert version in res.stdout

def test_base(runner):
    cmd = "-b ngs-test -c {0}".format(credentials_path)
    res = runner.invoke(root, cmd.split())
    #Command should complain about lack of subcommand
    assert res.exit_code == 2

def test_hci_base(runner):
    cmd = "-b ngs-test -c {0} hci".format(credentials_path)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0

def test_upload(runner):
    cmd = "-b ngs-test -c {0} upload -i {1} -d {2} -f -m /tmp/meta.json".format(credentials_path, 
          os.path.join(testWD,"data","test_reads_R1.fastq.gz"), f1target)
    log.debug(cmd)
    res = runner.invoke(root, cmd.split()) 
    assert res.exit_code == 0

#def test_search(runner):
#    cmd = "-b ngs-test -c {0} search -q {1}".format(credentials_path, f1target)
#    res = runner.invoke(root, cmd.split())
#    assert res.exit_code == 0 

def test_download(runner):
    cmd = "-b ngs-test -c {0} download -f -q {1} -d /{2}".format(credentials_path, f1target, os.path.join('tmp','tst.fq'))
    log.debug(cmd)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0

def test_delete(runner):
    cmd = "-b ngs-test -c {0} delete -q {1} -f".format(credentials_path, f1target)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0
