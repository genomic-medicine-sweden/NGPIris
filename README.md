# NGP Iris 2 👀
Rework of the original [NGP Iris](https://github.com/genomic-medicine-sweden/NGPIris). The major difference is that the previous version was based on `boto3` sessions instead of clients. By using clients we are able to do some more "low-level" operations like setting Access Control Lists (ACLs).

**Do note that we might change the name, but right now NGP Iris 2 is the WIP name.**

## Getting started

### Prerequisites 
* Python 3.11.5[^1]
* NGPr credentials (see ["NGPr credentials"](#ngpr-credentials))

[^1]: Most versions of Python 3 should work

### Installation
The current way to install NGP Iris 2 is by the following steps:

1. Clone this repository
2. Open a terminal in your local copy of the repository
3. Run `pip install .`. This will install NGP Iris 2 along with the required Python packages in your Python environment

### NGPr credentials
In order to use NGP Iris 2, a JSON file containing your credentials for the NGPr. The template of the JSON file can be found in [credentials/credentials_template.json](credentials/credentials_template.json). Depending on your needs, you can either enter only the credentials for the HCP, only for the HCI ***or*** both. Do note that you can't leave some parts of either the HCP or HCI credentials empty:
```JSON
{
    "hcp" : {
        "endpoint" : "some_endpoint",
        "aws_access_key_id" : "",        <-- Empty field!
        "aws_secret_access_key" : ""     <-- Empty field!
    },
    "hci" : {
        "username" : "some_user",
        "password" : "some_password",
        "address" : "some_address",
        "auth_port" : "some_auth_port",
        "api_port" : "some_api_port"
    }
}
```
This will prompt NGP Iris 2 to complain about incomplete credentials. Of course, the same error would occur if the reverse between the HCP and HCI fields would be true.

## Basic usage
NGP Iris 2 is to be used as a Python package. The main use consists of accessing an HCP or HCI via the AWS S3 service. This section contains examples of how NGP Iris 2 might be used to do so.

### Connect to HCP
In order to connect to the HCP, we first need to create an `HCPHandler` object and mount it to some bucket:
```Python
import NGPIris2.hcp as hcp

hcph = hcp.HCPHandler("myCredentials.json")

hcph.mount_bucket("myBucket")
```
If you are unsure which buckets you are allowed to see, you can use `hcph.list_buckets()` in order to list all available buckets to you.

When you have successfully mounted a bucket, you can then do different operations onto the bucket. Object names on the bucket can be listed by typing `print(hcph.list_objects(True))`. 

#### Upload files
```Python
# Upload a single file to HCP
hcph.upload_object_file("myFile")

# Upload folder contents to HCP
hcph.upload_object_folder("./myFiles/")
```

#### Download files
```Python
# Download a single object from HCP
hcph.download_object_file("myObject")

# Download all objects from HCP to a local folder
hcph.download_all_object_files("./myDownloadedFiles/")
```

### Connect to HCI
In order to connect to the HCI, we first need to create an `HCIHandler` object and request an authorization token:
```Python
import NGPIris2.hci as hci

hcih = hci.HCIHandler("./credentials/myCredentials.json")

hcih.request_token()
```
Note that the token is stored inside of the `HCIHandler` object called `hcih`. We can now request a list of indexes that are available by typing `print(hcih.list_index_names())`. We can also look up information about a certain index with `print(hcih.look_up_index("myIndex"))`. It is recommended to combine the use of the pretty print module `pprint` and the `json` module for this output, as it is mostly unreadable otherwise:
```Python
import NGPIris2.hci as hci
from pprint import pprint
import json

hcih = hci.HCIHandler("./credentials/myCredentials.json")

hcih.request_token()

pprint(
    json.dumps(
        hcih.look_up_index("myIndex"), 
        indent = 4
    )
)
```

### Miscellaneous utilities (`utils.py`)
The `utils` module can be contains two functions: one for converting a string to `base64` encoding and one for `MD5` encoding.

## Technical package documentation
A thorough package documentation can be found in [docs.md](docs.md).