#!/usr/bin/env python
"""
Module for interactive usage.

"""
import os
import sys
import time

from pathlib import Path

from NGPIris import log, TIMESTAMP
from NGPIris.preproc import preproc

class HCPInteracter:
    def __init__(self, hcpmanager):
        self.hcpm = hcpmanager

    def delete_interactive(self,query,force=False):
        objs = self.hcpm.search_objects(query) # Get object with query
        if len(objs) < 1:
            log.info(f"File: {query} does not exist on {self.hcpm.bucket.name}")
        else:
            hits = list()
            for obj in objs:
                hits.append(obj.key)
            log.info(f"Found {len(objs)} entries matching query '{query}':")
            log.info(f"{hits}")
            for obj in objs:
                if not force:
                    sys.stdout.write(f"You are about to delete the file {obj.key} " \
                                     f"on {self.hcpm.bucket.name}, are you sure? [Y/N/Q]?\n")
                    sys.stdout.flush()
                    answer = sys.stdin.readline()
                    if answer[0].lower() == "y":
                        self.hcpm.delete_object(obj) # Delete file.
                        time.sleep(2)
                        log.info(f"Deleted file {obj.key} ")
                    elif answer[0].lower() == "q":
                        break
                    else:
                        log.info(f"Skipped deleting {obj.key} ")
                elif force:
                        self.hcpm.delete_object(obj) # Delete file.
                        time.sleep(2)
                        log.info(f"Deleted file {obj.key} ")


    def download_interactive(self, query, destination="", force=False, silent=False):
        found_objs = self.hcpm.search_objects(query)

        #Defaults destination to input name
        if destination == "":
            destination = os.path.basename(query)
        #If destination is folder. Default file name to input name
        elif destination[-1] in ["/","\\"]:
            destination = os.path.join(destination, os.path.basename(query))


        if found_objs is None or len(found_objs) == 0:
            log.info(f"File: {query} does not exist on {self.hcpm.bucket.name}")

        elif len(found_objs) == 1:
            obj = self.hcpm.get_object(query) # Get object with key.
            self.hcpm.download_file(obj, destination, force=force, callback=(not silent)) # Downloads file.

        elif len(found_objs) > 1:
            for obj in found_objs:
                log.info(f"Found {len(found_objs)} files matching query")
                log.info(f"Download {obj}? [Y/N]")
                sys.stdout.write(f"[--] Do you wish to download {obj.key} on {self.hcpm.bucket.name}? [Y/N]?\n")
                sys.stdout.flush()
                answer = sys.stdin.readline()
                if answer[0].lower() == "y":
                    obj = self.hcpm.get_object(query) # Get object with key.
                    #Default destination name to key
                    if destination == "":
                        destination = obj.key
                    #If destination is folder. Default file name to obj.key
                    elif destination[-1] in ["/","\\"]:
                        destination = os.path.join(destination, obj.key)

                    self.hcpm.download_file(obj, destination, force=force, callback=(not silent)) # Downloads file.
                    #log.info(f"Downloaded {obj.key}"

    def upload_interactive(self, source, destination="", fastq_only=False, metadata="", force=False, silent=False):
        """ Uploads a file/folder-of-files and verifies its content """
        file_lst = []
        ###Sets destinations
        #Defaults destination to source name
        if destination == "":
            destination = os.path.basename(source)
        #If destination is folder. Default file name to source name
        elif destination[-1] in ["/","\\"]:
            destination = os.path.join(destination, os.path.basename(source))

        ###Verify fastq contents and metadata existence
        if os.path.isdir(source) and fastq_only:
            [file_lst, mdfile]=preproc.verify_upload_folder(source, metadata=metadata)
        elif os.path.isdir(source):
            [file_lst, mdfile]=preproc.folder_to_list(source, metadata=metadata)
        elif fastq_only:
            [file_lst, mdfile]=preproc.verify_upload_file(source, metadata=metadata)
        if fastq_only and file_lst == []:
            log.error(f"{source} could not be uploaded to NGPr. Try using an atypical (-a) upload")

        if os.path.isdir(source):
            pass
            #for file_pg in file_lst:
            #    self.hcpm.upload_file(file_pg, destination, force=force, callback=(not silent))
            #    #time.sleep(2)
            #    log.info(f"Uploaded: {file_pg}")
        else:
            self.hcpm.upload_file(source, destination, force=force, callback=(not silent))
            #time.sleep(2)
            log.info(f"Uploaded: {destination}")

        #Upload metadata
        #dstfld = Path(destination)
        #dstfld = dstfld.parent
        #if dstfld.parts == ():
        #    dstfld = ""
        #meta_fn = Path(mdfile).name
        #ctx['hcpm'].upload_file(mdfile, os.path.join(dstfld, meta_fn), callback=(not silent))
