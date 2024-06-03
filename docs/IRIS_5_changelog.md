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
* `delete-folder`: Deletes a folder on the HCP
* `delete-object`: Deletes an object on the HCP
* `list-buckets`: Lists all buckets that the user is allowed to see
* `list-objects`: Lists all objects that the user is allowed to see
* `simple-search`: Performs a simple search using a substring in order to find matching objects in a bucket/namespace

#### Removed features
* `delete`: Replaced by `delete-folder` and `delete-object`
* `search`: Replaced by `simple-search`
* `utils`: Removed since it didn't contain anything particularly useful that can be moved to being separate subcommands in the future

#### Modified features
* `download`:
  * Does pretty much the same thing as previous versions in terms of CLI
  * `iris path/to/credentials.json download --help`:
    * ```cmd
      Usage: iris CREDENTIALS download [OPTIONS] OBJECT BUCKET LOCAL_PATH

        Download files from an HCP bucket/namespace.

        OBJECT is the name of the object to be downloaded.

        BUCKET is the name of the upload destination bucket.

        LOCAL_PATH is the path to where the downloaded objects are to be stored
        locally.

      Options:
        --help  Show this message and exit.
      ```
* `upload`:
  * Does pretty much the same thing as previous versions in terms of CLI
  * `iris path/to/credentials.json upload --help`:
    * ```cmd
      Usage: iris CREDENTIALS upload [OPTIONS] FILE_OR_FOLDER BUCKET

        Upload files to an HCP bucket/namespace.

        FILE-OR-FOLDER is the path to the file or folder of files to be uploaded.

        BUCKET is the name of the upload destination bucket.

      Options:
        --help  Show this message and exit.
      ```

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
The updated codebase for IRIS 5 contains some major changes to use of the package, but should still be familiar. The use cases of IRIS 5 is sill intended to be the same as in previous versions. The difference between IRIS 5 and previous versions is the new syntax and names of classes, methods and functions. Everything in IRIS 5 was inspired by the previous implementations of the `boto3` library, which means that most functionality should still exist, but in a different form; methods and functions may have new names, and they might be combined or separated. A good starting point for how to use IRIS 5 is the README and the technical documentation of the package. Below is a summary of the alterations made to IRIS 5. In order to avoid confusion, IRIS 5 content is marked in <span style="color:green">green</span> and old content is marked in <span style="color:red">red</span>.

### The `HCPHandler` class and its methods
The <span style="color:green">`HCPHandler`</span> class is the replacement for <span style="color:red">`HCPManager`</span>. Their class parameters are the following:
```python
HCPHandler(self, 
  credentials_path : str, 
  use_ssl : bool = False, 
  proxy_path : str = "", 
  custom_config_path : str = ""
)
```
```python
HCPManager(self, 
  endpoint = "", 
  aws_access_key_id = "", 
  aws_secret_access_key = "", 
  bucket = None, 
  credentials_path = "", 
  debug = False
)
```
As you can see, the differences between the two in terms of parameters are significant. Most of the information going into <span style="color:red">`HCPManager`</span> is moved to the credentials file, where the <span style="color:green">`credentials_path`</span> parameter in the <span style="color:green">`HCPHandler`</span> class parsed. The rest of the parameters are optional and more information about them can be found in the technical documentation. 

In order to connect to a bucket in IRIS 5, you need to use the method <span style="color:green">`mount_bucket`</span>. This method effectively replaces <span style="color:red">`set_bucket`</span> and <span style="color:red">`attach_bucket`</span>. <span style="color:green">`mount_bucket`</span> only performs side-effects, so nothing is returned (just like <span style="color:red">`set_bucket`</span> and <span style="color:red">`attach_bucket`</span>). 

Listing buckets in IRIS 5 yields the same result as in the previous versions. However, you can also list all objects in the bucket/namespace with <span style="color:green">`list_objects`</span>. By default, all metadata for each object is included, but this can be changed with the `name_only` parameter. If you need to search for an object however, we recommend using the <span style="color:green">`search_objects_in_bucket`</span> method (until sufficiently good HCI index searches can be made).

Downloading files from a mounted bucket is done with <span style="color:green">`download_file`</span>. It outputs a progress bar and ETAs for files. Similarly, <span style="color:green">`upload_file`</span> uploads files to the mounted bucket with an associated progress bar and ETA. You can also upload a folder of files with <span style="color:green">`upload_folder`</span>. 

Deletion on the mounted bucket is made via the <span style="color:green">`delete_object`</span>, <span style="color:green">`delete_objects`</span> and <span style="color:green">`delete_folder`</span> methods.

### The `HCIHandler` class and its methods
The <span style="color:green">`HCIHandler`</span> class is the replacement for <span style="color:red">`HCIManager`</span>. Their class parameters are the following:
```python
HCIHandler(self, 
  credentials_path : str, 
  use_ssl : bool = False
)
```

```python
HCIManager(self,
  password = "", 
  credentials_path = ""
)
```

In terms of parameters, the `password` input is moved to the credentials file instead of being a separate parameter. Also note that the `credentials_path` parameter is now required, as opposed to in previous versions. 

In order to perform any operations on the HCI, we first need to request a token. We do this by calling <span style="color:green">`request_token`</span>. This method only performs side-effects. 

We can list the index names by using <span style="color:green">`list_index_names`</span> and then pick out some metadata about any of those indices that came from that list with <span style="color:green">`look_up_index`</span>. 

We can also make queries to the HCI via the <span style="color:green">`raw_query`</span> and <span style="color:green">`raw_query_from_JSON`</span> methods. The queries themselves have the following structure:
