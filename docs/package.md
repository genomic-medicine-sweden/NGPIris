### As a package
Listed below are some of the more common use cases.

For more use cases, check out [the CLI file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/cli/functions.py)

For an index of all HCPManager functionality, check out [the HCPManager source file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/hcp/hcp.py)

#### Connect to the HCP
```python
from NGPIris.hcp import HCPManager

endpoint = <>
aws_access_key_id = <>
aws_secret_access_key = <>

hcpm = HCPManager(endpoint, aws_access_key_id, aws_secret_access_key)
```

or more effectively

```python
from NGPIris.hcp import HCPManager

hcpm = HCPManager(credentials_path="./credentials.json",bucket="ngs-test")
hcpm.test_connection()
```

#### Attach a bucket and get all contents
```python
# Attach a bucket
hcpm.attach_bucket(<bucket_name>)

# Attaching to new bucket with already attached bucket
# This flushes the previous buckets object listing
hcpm.set_bucket("bucket_name_1")
hcpm.attach_bucket(bucket_instance_1)

# Grab all object summaries in the attached bucket
objects = hcpm.get_objects()
```
#### Mundane operations
##### Use a search string to find files and download them
```
# Search for objects with keys containing query string and download them
found_objs = hcpm.search_objects(<query_string>)
for obj in found_objs:
    local_file_name = os.path.basename(obj.key)
    hcpm.download_file(obj, <local_file_path>,force=False)
```
##### Perform preliminary checks before uploading a fastq file
```python
from  NGPIris.io  import  io

io.verify_fq_suffix(<local_file_path>)
io.verify_fq_content(<local_file_path>)
io.generate_tagmap(<local_file_path>, "microbial", <output_file_path>) #Generates a json file that describes what pipeline to use on the NGPr
```
##### Uploading a local file
```python

# Upload a file
hcpm.upload_file(<local_file_path>, <remote_key>)

# Upload a file with metadata
# Note that the maximum metadata size is rather small (2KB).

hcpm.upload_file(<local_file_path>, <remote_key>, metadata={'key': value})

```
##### Disable upload/download callback
Upload and download of files per default utilize a progress tracker. This can be disabled by passing `callback=False` to `upload_file()` or `download_file()`.
```python

# Disable progress tracking
hcpm.upload_file(<local_file_path>, <remote_key>, callback=False)
hcpm.download_file(obj, <local_file_path>, callback=False)
```
