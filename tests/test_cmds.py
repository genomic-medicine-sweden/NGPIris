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


#    def test01_upload_file(self):
#        self.assertIsNone(hcpm.upload_file(f"{ROOT_PATH}/data/test_reads_R1.fasterq", "unittest/test_reads_R1.fasterq"))
#
#    def test02_search_objects(self):
#        self.assertEqual(hcpm.search_objects("unittest/test_reads_R1.fasterq")[0].key, "unittest/test_reads_R1.fasterq")
#
#    def test03_download_file(self):
#        obj = hcpm.get_object("unittest/test_reads_R1.fasterq")
#        self.assertIsNone(hcpm.download_file(obj, "test_reads_R1.fasterq"))
#
#    def test04_md5_sha256(self):
#        remote_etag = hcpm.get_object("unittest/test_reads_R1.fasterq").e_tag
#        calculated_etag = calculate_etag(f"{ROOT_PATH}/data/test_reads_R1.fasterq")
#        self.assertEqual(calculated_etag, remote_etag)
#
#    def test05_delete_file(self):
#        obj = hcpm.get_object("unittest/test_reads_R1.fasterq")
#        self.assertIsNone(hcpm.delete_object(obj))
#        self.assertIsNone(hcpm.get_object("unittest/test_reads_R1.fasterq")) # Verify that object was removed
#
#    def test06_upload_error(self):
#        self.assertRaises(TypeError, lambda:hcpm.upload_file())
#
#    def test07_get_object_error(self):
#        self.assertRaises(TypeError, lambda:hcpm.get_object())
#
#    def test08_incorrect_credentials(self):
#        self.assertRaises(ValueError, lambda:HCPManager("x", "x", "x"))

@pytest.fixture
def runner():
    runnah = CliRunner()
    return runnah

def test_version(runner):
    res = runner.invoke(root, '--version')
    assert res.exit_code == 0
    assert version in res.stdout

def test_base(runner):
    cmd = "-b 'ngs-test' -c {0}".format(credentials_path)
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0

def test_upload(runner):
    cmd = "-b 'ngs-test' -c {0} --skip-hci upload -i {1} -d {2}".format(credentials_path, 
          os.path.join(testWD,"data","test_reads_R1.fasterq"), os.path.join("unittest","test_reads_R1.fasterq"))
    res = runner.invoke(root, cmd.split()) 
    assert res.exit_code == 0

def test_search(runner):
    cmd = "-b 'ngs-test' -c {0} search -q {1}".format(credentials_path, os.path.join("unittest","test_reads_R1.fasterq")
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0 

def test_check(runner):
    cmd = "-b 'ngs-test' -c {0} check".format(credentials_path)
    res = runner.invoke(root, cmd.split())
    pass

def test_download(runner):
    cmd = "-b 'ngs-test' -c {0} download".format(credentials_path)
    res = runner.invoke(root, cmd.split())
    pass

def test_delete(runner):
    cmd = "-b 'ngs-test' -c {0} delete -q {1} -f".format(credentials_path, os.path.join("unittest","test_reads_R1.fasterq"))
    res = runner.invoke(root, cmd.split())
    assert res.exit_code == 0
