# HCP interfacing tool
Tools for interfacing with the HCP

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

## Introduction
Interfacing with the HCP is done through the HCPManager class. It makes the connection to the specified endpoint with the provided access keys and manages the upload, download, and querying against the contents of the available buckets.

The connection is made on the higher-level resource level rather than client level. This may change in the future when more advanced features are desired.

### Usage

#### Connect to the HCP
Be careful not to list your access keys publically!

```python
from hcp import HCPManager

endpoint = <>
aws_access_key_id = <>
aws_secret_access_key = <>

hcpm = HCPManager(endpoint, aws_access_key_id, aws_secret_access_key)
```

#### Attach bucket and get all contents
The class at present time only manages one bucket connection at a time.
To work with multiple buckets at once, make two separate HCPManager instantiations and connect to the different buckets.

```python
# Attach a bucket
hcpm.attach_bucket(<bucket_name>)

# Attaching to new bucket with already attached bucket
# This flushes the previous buckets object listing
hcpm.attach_bucket(<bucket_name_1)
hcpm.attach_bucket(<bucket_name_2)

# Grab all object summaries in the attached bucket
objects = hcpm.get_objects()
```

#### Getting, searching, and downloading objects/files
```python
# Get an object with a known remote key and download it
obj = hcpm.get_object(<remote_key>)
hcpm.download_file(obj, <local_file_path>)

# Download object directly from the known remote key
hcpm.download_file(<remote_key>, <local_file_path>)  # Runs get_object() internally

# Search for objects with keys containing query string and download them
found_objs = hcpm.search_objects(<query_string>)
for obj in found_objs:
    local_file_name = os.path.basename(obj.key)
    hcpm.download_file(obj, <local_file_path>)
```

#### Uploading a file
```python

# Upload a file
hcpm.upload_file(<local_file_path>, <remote_key>)

# Upload a file with metadata
# Note that the maximum metadata size is rather small (2KB).
hcpm.upload_file(<local_file_path>, <remote_key>, metadata={'key': value})
```
