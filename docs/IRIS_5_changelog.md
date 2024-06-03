# NGP IRIS 5 changelog
IRIS 5 is a complete overhaul of the previous versions of IRIS, mainly in terms of its codebase. The general functionality like download from and upload to the HCP are still here, but might differ from previous versions from what you are used to. 

This document is meant as a semi complete changelog for IRIS, that will hopefully shed some light on what you (the user) can expect and how your workflow with IRIS might change.

## CLI 
IRIS 5 still features a Command Line Interface (CLI) like recent versions of IRIS. However, the new CLI is a bit different compared to before; the general structure of commands are totally different, but it still has the commands you would come to expect. 

### The `iris` command

Typing `iris --help` yields the following:
```cmd
Usage: iris [OPTIONS] CREDENTIALS COMMAND [ARGS]...

  NGP Intelligence and Repository Interface Software, IRIS.

  CREDENTIALS refers to the path to the JSON credentials file.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  delete-folder  Delete a folder from an HCP bucket/namespace.
  delete-object  Delete an object from an HCP bucket/namespace.
  download       Download files from an HCP bucket/namespace.
  list-buckets   List the available buckets/namespaces on the HCP.
  list-objects   List the objects in a certain bucket/namespace on the HCP.
  simple-search  Make simple search using substrings in a...
  upload         Upload files to an HCP bucket/namespace.
```
The previous version of IRIS would similarly yield the following:
```cmd
Usage: iris [OPTIONS] COMMAND [ARGS]...

  NGP intelligence and repository interface software

Options:
  -c, --credentials PATH     File containing ep, id & key  [required]
  -b, --bucket TEXT          Bucket name  [required]
  -ep, --endpoint TEXT       Endpoint URL override
  -id, --access_key_id TEXT  Amazon key identifier override
  -key, --access_key TEXT    Amazon secret access key override
  -p, --password TEXT        NGPintelligence password
  -l, --logfile PATH         Logs activity to provided file
  --version                  Show the version and exit.
  --help                     Show this message and exit.

Commands:
  delete    Delete a file on the HCP
  download  Download files using a given query
  search    List all file hits for a given query by directly calling HCP
  upload    Upload fastq files / fastq folder structure
  utils     Advanced commands for specific purposes

```
#### Added features
* `iris` commands:
  * `delete-folder`
  * `delete-object`
  * `list-buckets`
  * `list-objects`
  * `simple-search`

#### Removed features
* `iris` commands:
  * `delete`
  * `search`
  * `utils`

#### Modified features
* `iris` commands:
  * `download`
  * `upload`

### The `iris_generate_credentials_file` command

IRIS 5 comes with a new separate command for generating your NGPr credentials: `iris_generate_credentials_file`. The idea with this command is to make it easier for anyone to ensure the correct structure of their credentials file. Typing `iris_generate_credentials_file --help` yields the following:
```cmd
Usage: iris_generate_credentials_file [OPTIONS]

  Generate blank credentials file for the HCI and HCP.

  WARNING: This file will store sensitive information (such as passwords) in
  plaintext.

Options:
  --path TEXT  Path for where to put the new credentials file
  --name TEXT  Custom name for the credentials file
  --help       Show this message and exit.
```
Simply running `iris_generate_credentials_file` will generate a blank credentials file (which is just a JSON file) like the following:
```json
{
  "hcp": {
      "endpoint": "",
      "aws_access_key_id": "",
      "aws_secret_access_key": ""
  },
  "hci": {
      "username": "",
      "password": "",
      "address": "",
      "auth_port": "",
      "api_port": ""
  }
}
```

## Package
### Added features
### Removed features
### Modified features