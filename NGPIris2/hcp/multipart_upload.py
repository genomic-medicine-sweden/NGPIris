
#from NGPIris2.hcp.hcp import HCPHandler
import os
import tqdm

class HCPMultipartUpload:
    def __init__(self, hcph, local_file_path : str, key : str) -> None:
        self.hcph = hcph
        self.local_file_path = local_file_path
        self.total_bytes = os.stat(local_file_path).st_size
        self.key = key

        multi_part_upload : dict = self.hcph.s3_client.create_multipart_upload(
            Bucket = self.hcph.bucket_name,
            Key = self.key
        )

        multi_part_upload_id = multi_part_upload["UploadId"]

        self.upload_id = multi_part_upload_id
        self.parts : list[dict] = [{}]

    def multipart_upload(self):
        parts : list[dict] = []
        with open(self.local_file_path, "rb") as file:
            part_number = 1
            with tqdm.tqdm(total = self.total_bytes, unit = "B", unit_scale = True, desc = self.local_file_path) as pbar:
                while (part_data := file.read(self.hcph.transfer_config.multipart_chunksize)):
                    part = self.hcph.s3_client.upload_part(
                        Body = part_data,
                        Bucket = self.hcph.bucket_name,
                        Key = self.key,
                        UploadId = self.upload_id,
                        PartNumber = part_number
                    )
                    parts.append(
                        {"PartNumber" : part_number, 
                        "ETag" : part["ETag"]
                        }
                    )
                    print(parts)
                    part_number += 1
                    pbar.update(len(part_data))
            self.parts = parts
    
    def complete_multipart_upload(self):
        self.hcph.s3_client.complete_multipart_upload(
            Bucket = self.hcph.bucket_name,
            Key = self.key,
            UploadId = self.upload_id,
            MultipartUpload = {"Parts" : self.parts}
        )
