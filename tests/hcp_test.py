#!/usr/bin/env python3

# Test for hcp.py, run from root in project directory tests/hcp_test.py

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import unittest
from hcp import HCPManager
from hcp.helpers import calculate_etag
import sys
import os
import time
import json
import urllib3
import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog="unittest")
    parser.add_argument("--json", \
                required=True, \
                            help="json file with keys")
    ns, args = parser.parse_known_args(namespace=unittest)
    return ns, sys.argv[:1] + args


# Parse json file with passwords for HCP connection.
def setup_args(args):
#    with open(os.path.join(os.path.dirname(__file__), "keys.json") , "r") as fp:
    with open(args.json , "r") as fp:
        data = json.load(fp)
        endpoint = data["ep"]
        aws_access_key_id = data["aki"]
        aws_secret_access_key = data["sak"]

        return endpoint, aws_access_key_id, aws_secret_access_key


class TestProcess(unittest.TestCase):

    def test01_upload_file(self):
        self.assertIsNone(hcpm.upload_file("data/test_reads_R1.fasterq", "unittest/test_reads_R1.fasterq"))

    def test02_search_objects(self):
        self.assertEqual(hcpm.search_objects("unittest/test_reads_R1.fasterq")[0].key, "unittest/test_reads_R1.fasterq")

    def test03_download_file(self):
        obj = hcpm.get_object("unittest/test_reads_R1.fasterq")
        self.assertIsNone(hcpm.download_file(obj, "test_reads_R1.fasterq"))

    def test04_md5_sha256(self):
        remote_etag = hcpm.get_object("unittest/test_reads_R1.fasterq").e_tag
        calculated_etag = calculate_etag("data/test_reads_R1.fasterq")
        self.assertEqual(calculated_etag, remote_etag)

    def test05_delete_file(self):
        obj = hcpm.get_object("unittest/test_reads_R1.fasterq")
        self.assertIsNone(hcpm.delete_object(obj))
        self.assertIsNone(hcpm.get_object("unittest/test_reads_R1.fasterq")) # Verify that object was removed

    def test06_upload_error(self):
        self.assertRaises(TypeError, lambda:hcpm.upload_file())

    def test07_get_object_error(self):
        self.assertRaises(TypeError, lambda:hcpm.get_object())

    def test08_incorrect_credentials(self):
        self.assertRaises(ValueError, lambda:HCPManager("x", "x", "x"))


    @classmethod
    def tearDownClass(cls):
        # Remove the directories and files after the test is done.
        if "test_reads_R1.fasterq" in os.listdir():
            os.remove("test_reads_R1.fasterq")


if __name__ == '__main__':
    args, argv = parse_args()   # run this first
    sys.argv[:] = argv       # create cleans argv for main()
    hcpm = HCPManager(*setup_args(args))
    hcpm.attach_bucket("ngs-test")
    unittest.main()
