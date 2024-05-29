# NGP Iris 👀
NGP Iris is a light-weight tool for interacting with a Hitachi Content Platform (HCP) using S3 in the `boto3` package. NGP Iris is designed with two use cases in mind:
* A simple, clear, real-time interaction with NGPr file management
* Improving process flow for performing off-site data analysis by using automated transfer scripts

Both of these cases can be achieved as either a [Python package](#as-a-python-package) or as a [Command Line Interface (CLI)](#as-a-command-line-tool).

## Getting started

### Prerequisites 
* Python 3.11.5[^1]
* NGPr credentials (see ["NGPr credentials"](#ngpr-credentials))

[^1]: Most versions of Python 3 should work

### Installation
The current way to install NGP Iris is by the following steps:

1. Clone this repository
2. Open a terminal in your local copy of the repository
3. Run `pip install .`. This will install NGP Iris along with the required Python packages in your Python environment

### NGPr credentials
In order to use NGP Iris, a JSON file containing your credentials for the NGPr. The template of the JSON file can be found in [credentials/credentials_template.json](credentials/credentials_template.json). Depending on your needs, you can either enter only the credentials for the HCP, only for the HCI ***or*** both. Do note that you can't leave some parts of either the HCP or HCI credentials empty:
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
This will prompt NGP Iris to complain about incomplete credentials. Of course, the same error would occur if the reverse between the HCP and HCI fields would be true.

## Technical package documentation
A thorough package documentation can be found in the Technical documentation page.

## Basic usage
NGP Iris can be used as a Python package or by using the command line. The following sections cover examples of how NGP Iris might be used as a package and how to use its various commands.

### As a Python package
#### Connect to HCP
In order to connect to the HCP, we first need to create an `HCPHandler` object and mount it to some bucket:
```Python
import NGPIris.hcp as hcp

hcph = hcp.HCPHandler("myCredentials.json")

hcph.mount_bucket("myBucket")
```
If you are unsure which buckets you are allowed to see, you can use `hcph.list_buckets()` in order to list all available buckets to you.

When you have successfully mounted a bucket, you can then do different operations onto the bucket. Object names on the bucket can be listed by typing `print(hcph.list_objects(True))`. 

##### Upload files
```Python
# Upload a single file to HCP
hcph.upload_object_file("myFile")

# Upload folder contents to HCP
hcph.upload_object_folder("./myFiles/")
```

##### Download files
```Python
# Download a single object from HCP
hcph.download_object_file("myObject")

# Download all objects from HCP to a local folder
hcph.download_all_object_files("./myDownloadedFiles/")
```

#### Connect to HCI
In order to connect to the HCI, we first need to create an `HCIHandler` object and request an authorization token:
```Python
import NGPIris.hci as hci

hcih = hci.HCIHandler("./credentials/myCredentials.json")

hcih.request_token()
```
Note that the token is stored inside of the `HCIHandler` object called `hcih`. We can now request a list of indexes that are available by typing `print(hcih.list_index_names())`. We can also look up information about a certain index with `print(hcih.look_up_index("myIndex"))`. It is recommended to combine the use of the pretty print module `pprint` and the `json` module for this output, as it is mostly unreadable otherwise:
```Python
import NGPIris.hci as hci
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

### As a command line tool
NGP Iris comes with two commands: `iris` and `iris_generate_credentials_file`. The latter command is used solely to generate the `.json` credentials file. Running `iris_generate_credentials_file --help` we get the following:
```
Usage: iris_generate_credentials_file [OPTIONS]

  Generate blank credentials file for the HCI and HCP.

  WARNING: This file will store sensisitve information (such as passwords) in
  plaintext.

Options:
  --path TEXT  Path for where to put the new credentials file
  --name TEXT  Custom name for the credentials file
  --help       Show this message and exit.
```

The `iris` command is used for communicating with the HCP and HCI. This includes upload and download to and from the HCP/HCI. Running `iris --help` yields the following:
```
Usage: iris [OPTIONS] CREDENTIALS COMMAND [ARGS]...

  NGP Intelligence and Repository Interface Software, IRIS.

  CREDENTIALS refers to the path to the JSON credentials file.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  delete        Delete an object from an HCP bucket/namespace.
  download      Download files from an HCP bucket/namespace.
  list-buckets  List the available buckets/namespaces on the HCP.
  list-objects  List the objects in a certain bucket/namespace on the HCP.
  upload        Upload files to an HCP bucket/namespace.
```

#### The `delete` command
```
Usage: iris CREDENTIALS delete [OPTIONS] OBJECT BUCKET

  Delete an object from an HCP bucket/namespace.

  OBJECT is the name of the object to be deleted.

  BUCKET is the name of the bucket where the object to be deleted exist.

Options:
  --help  Show this message and exit.
```

#### The `download` command
```
Usage: iris CREDENTIALS download [OPTIONS] OBJECT BUCKET LOCAL_PATH

  Download files from an HCP bucket/namespace.

  OBJECT is the name of the object to be downloaded.

  BUCKET is the name of the upload destination bucket.

  LOCAL_PATH is the path to where the downloaded objects are to be stored
  locally.

Options:
  --help  Show this message and exit.
```

#### The `list-buckets` command
```
Usage: iris CREDENTIALS list-buckets [OPTIONS]

  List the available buckets/namespaces on the HCP.

Options:
  --help  Show this message and exit.
```

#### The `list-objects` command
```
Usage: iris CREDENTIALS list-objects [OPTIONS] BUCKET

  List the objects in a certain bucket/namespace on the HCP.

  BUCKET is the name of the bucket in which to list its objects.

Options:
  -no, --name-only BOOLEAN  Output only the name of the objects instead of all
                            the associated metadata
  --help                    Show this message and exit.
```

#### The `upload` command
```
Usage: iris CREDENTIALS upload [OPTIONS] FILE_OR_FOLDER BUCKET

  Upload files to an HCP bucket/namespace.

  FILE-OR-FOLDER is the path to the file or folder of files to be uploaded.

  BUCKET is the name of the upload destination bucket.

Options:
  --help  Show this message and exit.
```