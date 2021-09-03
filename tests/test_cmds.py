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

from HCPInterface import version, log
from HCPInterface.cli.base import root

from click.testing import CliRunner
from distutils.sysconfig import get_python_lib
from unittest.mock import patch, mock_open

@pytest.fixture
def runner():
    runnah = CliRunner()
    return runnah

def test_version(runner):
    res = runner.invoke(root, '--version')
    assert res.exit_code == 0
    assert version in res.stdout

def test_base(runner):
    res = runner.invoke(root)
    pass

def test_check(runner):
    res = runner.invoke(root, 'check')
    pass

def test_download(runner):
    res = runner.invoke(root, 'download')   
    pass
 
def test_upload(runner):
    res = runner.invoke(root, 'upload')
    pass

def test_delete(runner):
    res = runner.invoke(root, 'delete')
    pass

def test_search(runner):
    res = runner.invoke(root, 'search')
    pass
