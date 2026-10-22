# NGP IRIS 👀

NGP IRIS, or just Iris, is a tool for interacting with a Hitachi Content Platform (HCP) using S3 in the `boto3` package. NGP Iris is designed with two use cases in mind:

- A simple, clear, real-time interaction with NGPr file management
- Improving process flow for performing off-site data analysis by using automated transfer scripts

Both of these cases can be achieved as either a [Python package](#as-a-python-package) or as a [Command Line Interface (CLI)](#as-a-command-line-tool).

## Getting started

### Prerequisites

- Python 3.14
- Python dependencies can be found in [pyproject.toml](pyproject.toml)
- NGPr credentials (see ["NGPr credentials"](#ngpr-credentials))

### Installation

Iris can be installed via PyPi by running the following:

```bash
pip install NGPIris
```

If you wish, you can also install NGP Iris with the following steps:

1. Clone this repository
2. Open a terminal in your local copy of the repository
3. Run `pip install .` at the root of the repository. This will install Iris along with the required Python packages in your current Python environment

### NGPr credentials

In order to use Iris, a JSON file containing your credentials for NGPr is required. The template of the JSON file can be found in [credentials/credentials_template.json](credentials/credentials_template.json). Depending on your needs, you can either enter

- only the credentials for the HCP
- only for the HCI _**or**_ both.

Do note that you can't leave some parts of either the HCP or HCI credentials empty:

```JSON
{
  "hcp" : {
      "endpoint" : "some_endpoint",
      "username" : "",
      "password" : ""
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

This will prompt Iris to complain about incomplete credentials (since the entries `username` and `password` in the `hcp` section are empty). Of course, the same error would occur if the reverse between the `hcp` and `hci` sections would be true.

> [!NOTE]
> The `username` field is equivalent to `aws_access_key_id` and `password` is equivalent to `aws_secret_access_key`

> [!IMPORTANT]
> The `endpoint` field should not contain `https://` or any port number.

## Technical package documentation

A thorough package documentation can be found in the technical documentation pages. In order to compile the documentation, see [here](#compiling-the-documentation).

## Basic usage

Iris can be used as a Python package or by using the command line. The following sections cover some examples of how Iris might be used as a package and how to use its various commands. However, we highly recommend checking out the [tutorial](/docs/Tutorial.md) containing more example use cases.

### As a Python package

#### Connect to HCP

In order to connect to the HCP, we first need to create an `HCPHandler` object and mount it to some bucket:

```Python
from NGPIris import HCPHandler

hcp_h = HCPHandler("credentials.json")

hcp_h.mount_bucket("myBucket")
```

If you are unsure which buckets you are allowed to see, you can use `hcp_h.list_buckets()` in order to list all available buckets to you.

When you have successfully mounted a bucket, you can then do different operations in the bucket. Object names on the bucket can be listed by typing `print(hcp_h.list_objects())`.

##### Upload files

```Python
# Upload a single file to HCP
hcp_h.upload_file("myFile")

# Upload folder contents to HCP
hcp_h.upload_folder("myFiles/")
```

##### Download files

```Python
# Download a single object from HCP
hcp_h.download_file("myFile")

# Download folder contents from HCP
hcp_h.download_folder("myFiles/")
```

#### Connect to HCI

In order to connect to the HCI, we first need to create an `HCIHandler` object and request an authorization token:

```Python
from NGPIris import HCIHandler

hci_h = HCIHandler("credentials.json")
```

Note that the token is stored inside of the `HCIHandler` object called `hci_h`. We can now request a list of indexes that are available by typing `print(hci_h.list_index_names())`. We can also look up information about a certain index with `print(hci_h.look_up_index("myIndex"))`. It is recommended to combine the use of the pretty print module `pprint` (or similar packages) and the `json` module for this output, as it is mostly unreadable otherwise:

```Python
from NGPIris import HCIHandler
from pprint import pprint

hci_h = HCIHandler("credentials.json")

pprint(
    json.dumps(
        hci_h.look_up_index("myIndex"),
        indent = 4
    )
)
```

#### Miscellaneous utilities (`utils.py`)

The `utils` module contains two functions: one for converting a string to `base64` encoding and one for `MD5` encoding.

### As a command line tool

NGP Iris comes with two commands: `iris` and `iris_generate_credentials_file`. The latter command is used solely to generate the `.json` credentials file. The `iris` command is used for communicating with the HCP. This includes uploads to and downloads from the HCP. Running `iris --help` will yield more detailed information. Each sub-command has its own help message and is displayed by running `iris [sub-command] --help` after replacing `[sub-command]` with the command of interest.

## Testing

Assuming that the repository has been cloned, do the following:

1. Create a test config file based on [`test_conf_template.ini`](tests/test_conf_template.ini)
2. Run the following command:

```shell
pytest --config [test config file] tests/test_hcp.py -v -s
```

## Update documentation

With force flag `-f`:

```shell
cd docs/
sphinx-apidoc ../NGPIris/ -o . -F -f
```

Without force flag

```shell
cd docs/
sphinx-apidoc ../NGPIris/ -o . -F
```

## Compiling the documentation

```shell
cd docs/
make html
```
