# Table of Contents

* [Table of Contents](#table-of-contents)
* [\_\_init\_\_](#__init__)
* [hci](#hci)
* [hci.hci](#hcihci)
  * [HCIHandler Objects](#hcihandler-objects)
    * [\_\_init\_\_](#__init__-1)
    * [request\_token](#request_token)
    * [list\_index\_names](#list_index_names)
    * [look\_up\_index](#look_up_index)
    * [raw\_query](#raw_query)
    * [raw\_query\_from\_JSON](#raw_query_from_json)
    * [prettify\_raw\_query](#prettify_raw_query)
    * [SQL\_query](#sql_query)
* [hci.helpers](#hcihelpers)
    * [raise\_request\_error](#raise_request_error)
    * [get\_index\_response](#get_index_response)
    * [get\_query\_response](#get_query_response)
    * [process\_raw\_query](#process_raw_query)
* [utils](#utils)
* [utils.utils](#utilsutils)
* [hcp](#hcp)
* [hcp.hcp](#hcphcp)
  * [HCPHandler Objects](#hcphandler-objects)
      * [\_\_init\_\_](#__init__-2)
      * [mount\_bucket](#mount_bucket)
      * [list\_buckets](#list_buckets)
      * [list\_objects](#list_objects)
      * [get\_object](#get_object)
      * [object\_exists](#object_exists)
      * [download\_file](#download_file)
      * [upload\_file](#upload_file)
      * [upload\_folder](#upload_folder)
      * [delete\_objects](#delete_objects)
      * [delete\_object](#delete_object)
      * [search\_objects\_in\_bucket](#search_objects_in_bucket)
      * [get\_bucket\_statistics](#get_bucket_statistics)
      * [get\_object\_acl](#get_object_acl)
      * [get\_bucket\_acl](#get_bucket_acl)
      * [modify\_single\_object\_acl](#modify_single_object_acl)
      * [modify\_single\_bucket\_acl](#modify_single_bucket_acl)
      * [modify\_object\_acl](#modify_object_acl)
      * [modify\_bucket\_acl](#modify_bucket_acl)
* [hcp.helpers](#hcphelpers)
* [parse\_credentials](#parse_credentials)
* [parse\_credentials.parse\_credentials](#parse_credentialsparse_credentials)
  * [CredentialsHandler Objects](#credentialshandler-objects)
      * [\_\_init\_\_](#__init__-3)

<a id="__init__"></a>

# \_\_init\_\_

<a id="hci"></a>

# hci

<a id="hci.hci"></a>

# hci.hci

<a id="hci.hci.HCIHandler"></a>

## HCIHandler Objects

```python
class HCIHandler()
```

<a id="hci.hci.HCIHandler.__init__"></a>

### \_\_init\_\_

```python
def __init__(credentials_path: str, use_ssl: bool = False) -> None
```

Class for handling HCI requests.

**Arguments**:

- `credentials_path` (`str`): Path to the JSON credentials file
- `use_ssl` (`bool, optional`): Boolean choice between using SSL, defaults to False

<a id="hci.hci.HCIHandler.request_token"></a>

### request\_token

```python
def request_token() -> None
```

Request a token from the HCI, which is stored in the HCIHandler object. 

The token is used for every operation that needs to send a request to 
HCI.

**Raises**:

- `RuntimeError`: If there was a problem when requesting a token, a 
runtime error will be raised

<a id="hci.hci.HCIHandler.list_index_names"></a>

### list\_index\_names

```python
def list_index_names() -> list[str]
```

Retrieve a list of all index names.

**Returns**:

`list[str]`: A list of index names

<a id="hci.hci.HCIHandler.look_up_index"></a>

### look\_up\_index

```python
def look_up_index(index_name: str) -> dict
```

Look up index information in the form of a dictionary by submitting 

the index name. Will return an empty dictionary if no index was found.

**Arguments**:

- `index_name` (`str`): The index name

**Returns**:

`dict`: A dictionary containing information about an index

<a id="hci.hci.HCIHandler.raw_query"></a>

### raw\_query

```python
def raw_query(query_dict: dict[str, str]) -> dict
```

Make query to an HCI index, with a dictionary

**Arguments**:

- `query_dict` (`dict[str, str]`): Dictionary consisting of the query

**Returns**:

`dict`: Dictionary containing the raw query

<a id="hci.hci.HCIHandler.raw_query_from_JSON"></a>

### raw\_query\_from\_JSON

```python
def raw_query_from_JSON(query_path: str) -> dict
```

Make query to an HCI index, with prewritten query in a JSON file

**Arguments**:

- `query_path` (`str`): Path to the JSON file

**Returns**:

`dict`: Dictionary containing the raw query

<a id="hci.hci.HCIHandler.prettify_raw_query"></a>

### prettify\_raw\_query

```python
def prettify_raw_query(raw_query: dict,
                       only_metadata: bool = True) -> DataFrame
```

Prettify a query in the shape of a DataFrame.

**Arguments**:

- `query_path` (`dict`): The raw query to be prettified
- `only_metadata` (`bool, optional`): Boolean choice between only returning the metadata. 
Defaults to True

**Returns**:

`DataFrame`: A DataFrame of the query

<a id="hci.hci.HCIHandler.SQL_query"></a>

### SQL\_query

```python
def SQL_query(query_path: str) -> DataFrame
```

Perform an SQL query given a path to a JSON file containing the 

query. Returns a DataFrame containing the result of the query.

**Arguments**:

- `query_path` (`str`): Path to the query JSON file

**Raises**:

- `RuntimeError`: Will raise a runtime error if an error was found 
with the SQL query

**Returns**:

`DataFrame`: A DataFrame containing the result of the SQL query

<a id="hci.exceptions"></a>

# hci.exceptions

<a id="hci.helpers"></a>

# hci.helpers

<a id="hci.helpers.raise_request_error"></a>

### raise\_request\_error

```python
def raise_request_error(response: Response, url: str) -> None
```

Raise a request error.

**Arguments**:

- `response` (`requests.Response`): The response containing the error to be raised
- `url` (`str`): The URL where the request was made

**Raises**:

- `RuntimeError`: Will raise a runtime error for a request

<a id="hci.helpers.get_index_response"></a>

### get\_index\_response

```python
def get_index_response(address: str, api_port: str, token: str,
                       use_ssl: bool) -> Response
```

Retrieve the index response given the address, API port and token.

**Arguments**:

- `address` (`str`): The address where request is to be made
- `api_port` (`str`): The API port at the given address
- `token` (`str`): The HCI token
- `use_ssl` (`bool`): Boolean choice of using SSL

**Returns**:

`requests.Response`: A response containing information about the index

<a id="hci.helpers.get_query_response"></a>

### get\_query\_response

```python
def get_query_response(query_dict: dict[str, str],
                       address: str,
                       api_port: str,
                       token: str,
                       use_ssl: bool,
                       path_extension: str = "") -> Response
```

Retrieve the query response given the address, API port and token.

**Arguments**:

- `query_dict` (`dict[str, str]`): The query dictionary
- `address` (`str`): The address where request is to be made
- `api_port` (`str`): The API port at the given address
- `token` (`str`): The HCI token
- `use_ssl` (`bool`): Boolean choice of using SSL
- `path_extension` (`str, optional`): possibly extend the request URL. Used for example 
when making SQL requests. Defaults to ""

**Returns**:

`requests.Response`: A response containing information about the query

<a id="hci.helpers.process_raw_query"></a>

### process\_raw\_query

```python
def process_raw_query(raw_query: dict, only_metadata: bool) -> list
```

Take a raw query dictionary and turn it into a list of datapoints

**Arguments**:

- `raw_query` (`dict`): Raw query to be processed
- `only_metadata` (`bool`): Boolean choice between only returning the metadata

**Returns**:

`list`: List of datapoints from the response

<a id="utils"></a>

# utils

<a id="utils.utils"></a>

# utils.utils

<a id="cli"></a>

# cli

<a id="cli.cli"></a>

#### cli

```python
@click.group()
@click.argument("credentials")
@click.version_option(package_name="NGPIris2")
@click.pass_context
def cli(context: Context, credentials: str)
```

NGP Intelligence and Repository Interface Software, IRIS. 

CREDENTIALS refers to the path to the JSON credentials file.

<a id="cli.upload"></a>

#### upload

```python
@cli.command()
@click.argument("file-or-folder")
@click.argument("bucket")
@click.pass_context
def upload(context: Context, file_or_folder: str, bucket: str)
```

Upload files to an HCP bucket/namespace. 

FILE-OR-FOLDER is the path to the file or folder of files to be uploaded.

BUCKET is the name of the upload destination bucket.

<a id="cli.download"></a>

#### download

```python
@cli.command()
@click.argument("object")
@click.argument("bucket")
@click.argument("local_path")
@click.pass_context
def download(context: Context, object: str, bucket: str, local_path: str)
```

Download files from an HCP bucket/namespace.

OBJECT is the name of the object to be downloaded.

BUCKET is the name of the upload destination bucket.

LOCAL_PATH is the path to where the downloaded objects are to be stored locally.

<a id="cli.delete"></a>

#### delete

```python
@cli.command()
@click.argument("object")
@click.argument("bucket")
@click.pass_context
def delete(context: Context, object: str, bucket: str)
```

Delete an object from an HCP bucket/namespace. 

OBJECT is the name of the object to be deleted.

BUCKET is the name of the bucket where the object to be deleted exist.

<a id="cli.list_buckets"></a>

#### list\_buckets

```python
@cli.command()
@click.pass_context
def list_buckets(context: Context)
```

List the available buckets/namespaces on the HCP.

<a id="cli.list_objects"></a>

#### list\_objects

```python
@cli.command()
@click.argument("bucket")
@click.option(
    "-no",
    "--name-only",
    help=
    "Output only the name of the objects instead of all the associated metadata",
    default=False)
@click.pass_context
def list_objects(context: Context, bucket: str, name_only: bool)
```

List the objects in a certain bucket/namespace on the HCP.

BUCKET is the name of the bucket in which to list its objects.

<a id="cli.iris2_generate_credentials_file"></a>

#### iris2\_generate\_credentials\_file

```python
@click.command()
@click.option("--path",
              help="Path for where to put the new credentials file",
              default="")
@click.option("--name",
              help="Custom name for the credentials file",
              default="credentials")
def iris2_generate_credentials_file(path: str, name: str)
```

Generate blank credentials file for the HCI and HCP. 

WARNING: This file will store sensisitve information (such as passwords) in plaintext.

<a id="hcp"></a>

# hcp

<a id="hcp.hcp"></a>

# hcp.hcp

<a id="hcp.hcp.HCPHandler"></a>

## HCPHandler Objects

```python
class HCPHandler()
```

<a id="hcp.hcp.HCPHandler.__init__"></a>

#### \_\_init\_\_

```python
def __init__(credentials_path: str,
             use_ssl: bool = False,
             proxy_path: str = "",
             custom_config_path: str = "") -> None
```

Class for handling HCP requests.

**Arguments**:

- `credentials_path` (`str`): Path to the JSON credentials file
- `use_ssl` (`bool, optional`): Boolean choice between using SSL, defaults to False
- `custom_config_path` (`str, optional`): Path to a .ini file for customs settings regarding download and upload

<a id="hcp.hcp.HCPHandler.mount_bucket"></a>

#### mount\_bucket

```python
def mount_bucket(bucket_name: str) -> None
```

Mount bucket that is to be used. This method needs to executed in order 

for most of the other methods to work. It mainly concerns operations with 
download and upload.

**Arguments**:

- `bucket_name` (`str`): The name of the bucket to be mounted

**Raises**:

- `VPNConnectionError`: If there is no VPN connection
- `BucketNotFound`: If no bucket of that name was found
- `Exception`: Other exceptions

<a id="hcp.hcp.HCPHandler.list_buckets"></a>

#### list\_buckets

```python
def list_buckets() -> list[str]
```

List all available buckets at endpoint.

**Returns**:

`list[str]`: A list of buckets

<a id="hcp.hcp.HCPHandler.list_objects"></a>

#### list\_objects

```python
def list_objects(name_only=False) -> list
```

List all objects in the mounted bucket

**Arguments**:

- `name_only` (`bool, optional`): If True, return only a list of the object names. 
If False, return the full metadata about each object. Defaults to False.

**Returns**:

`list`: A list of of either strings or a list of object metadata (the form of a dictionary)

<a id="hcp.hcp.HCPHandler.get_object"></a>

#### get\_object

```python
def get_object(key: str) -> dict
```

Retrieve object metadata

**Arguments**:

- `key` (`str`): The object name

**Returns**:

`dict`: A dictionary containing the object metadata

<a id="hcp.hcp.HCPHandler.object_exists"></a>

#### object\_exists

```python
def object_exists(key: str) -> bool
```

Check if a given object is in the mounted bucket

**Arguments**:

- `key` (`str`): The object name

**Returns**:

`bool`: True if the object exist, otherwise False

<a id="hcp.hcp.HCPHandler.download_file"></a>

#### download\_file

```python
def download_file(key: str, local_file_path: str) -> None
```

Download one object file from the mounted bucket

**Arguments**:

- `key` (`str`): Name of the object
- `local_file_path` (`str`): Path to a file on your local system where the 
contents of the object file can be put.

<a id="hcp.hcp.HCPHandler.upload_file"></a>

#### upload\_file

```python
def upload_file(local_file_path: str, key: str = "") -> None
```

Upload one file to the mounted bucket

**Arguments**:

- `local_file_path` (`str`): Path to the file to be uploaded
- `key` (`str, optional`): An optional new name for the file object on the bucket. 
Defaults to the same name as the file

<a id="hcp.hcp.HCPHandler.upload_folder"></a>

#### upload\_folder

```python
def upload_folder(local_folder_path: str) -> None
```

Upload the contents of a folder to the mounted bucket

**Arguments**:

- `local_folder_path` (`str`): Path to the folder to be uploaded

<a id="hcp.hcp.HCPHandler.delete_objects"></a>

#### delete\_objects

```python
def delete_objects(keys: list[str], verbose=True) -> None
```

Delete a list of objects on the mounted bucket

**Arguments**:

- `keys` (`list[str]`): List of object names to be deleted
- `verbose` (`bool, optional`): Print the result of the deletion. Defaults to True

<a id="hcp.hcp.HCPHandler.delete_object"></a>

#### delete\_object

```python
def delete_object(key: str, verbose=True) -> None
```

Delete a single object in the mounted bucket

**Arguments**:

- `key` (`str`): The object to be deleted
- `verbose` (`bool, optional`): Print the result of the deletion. Defaults to True

<a id="hcp.hcp.HCPHandler.search_objects_in_bucket"></a>

#### search\_objects\_in\_bucket

```python
def search_objects_in_bucket(search_string: str,
                             case_sensitive=False) -> list[str]
```

Simple search method using substrings in order to find certain objects. 

Case insensitive by default.

**Arguments**:

- `search_string` (`str`): Substring to be used in the search
- `case_sensitive` (`bool, optional`): Case sensitivity. Defaults to False

**Returns**:

`list[str]`: List of object names that match the in some way to the 
object names

<a id="hcp.hcp.HCPHandler.get_bucket_statistics"></a>

#### get\_bucket\_statistics

```python
def get_bucket_statistics() -> dict
```

Retrieve a dictionary containing information about the mounted bucket

**Raises**:

- `RuntimeError`: Raises an error if there was a problem with parsing the endpoint URL

**Returns**:

`dict`: A dictionary containing the information about the mounted bucket

<a id="hcp.hcp.HCPHandler.get_object_acl"></a>

#### get\_object\_acl

```python
def get_object_acl(key: str) -> dict
```

Get the object Access Control List (ACL)

**Arguments**:

- `key` (`str`): The name of the object

**Returns**:

`dict`: Return the ACL in the shape of a dictionary

<a id="hcp.hcp.HCPHandler.get_bucket_acl"></a>

#### get\_bucket\_acl

```python
def get_bucket_acl() -> dict
```

Get the bucket Access Control List (ACL)

**Returns**:

`dict`: Return the ACL in the shape of a dictionary

<a id="hcp.hcp.HCPHandler.modify_single_object_acl"></a>

#### modify\_single\_object\_acl

```python
def modify_single_object_acl(key: str, user_ID: str, permission: str) -> None
```

Modify permissions for a user in the Access Control List (ACL) for one object

**Arguments**:

- `key` (`str`): The name of the object
- `user_ID` (`str`): The user name. Can either be the DisplayName or user_ID
- `permission` (`str`): What permission to be set. Valid options are:
- FULL_CONTROL 
- WRITE 
- WRITE_ACP 
- READ 
- READ_ACP

<a id="hcp.hcp.HCPHandler.modify_single_bucket_acl"></a>

#### modify\_single\_bucket\_acl

```python
def modify_single_bucket_acl(user_ID: str, permission: str) -> None
```

Modify permissions for a user in the Access Control List (ACL) for the 

mounted bucket

**Arguments**:

- `user_ID` (`str`): The user name. Can either be the DisplayName or user_ID
- `permission` (`str`): What permission to be set. Valid options are:
- FULL_CONTROL 
- WRITE 
- WRITE_ACP 
- READ 
- READ_ACP

<a id="hcp.hcp.HCPHandler.modify_object_acl"></a>

#### modify\_object\_acl

```python
def modify_object_acl(
        key_user_ID_permissions: dict[str, dict[str, str]]) -> None
```

Modifies  permissions to multiple objects, see below.

In order to add permissions for multiple objects, we make use of a 
dictionary of a dictionary:

**Arguments**:

- `key_user_ID_permissions` (`dict[str, dict[str, str]]`): The dictionary containing object name 
and user_id-permission dictionary

<a id="hcp.hcp.HCPHandler.modify_bucket_acl"></a>

#### modify\_bucket\_acl

```python
def modify_bucket_acl(user_ID_permissions: dict[str, str]) -> None
```

Modify permissions for multiple users for the mounted bucket

**Arguments**:

- `user_ID_permissions` (`dict[str, str]`): The dictionary containing the user name and 
the corresponding permission to be set to that user

<a id="hcp.exceptions"></a>

# hcp.exceptions

<a id="hcp.helpers"></a>

# hcp.helpers

<a id="parse_credentials"></a>

# parse\_credentials

<a id="parse_credentials.parse_credentials"></a>

# parse\_credentials.parse\_credentials

<a id="parse_credentials.parse_credentials.CredentialsHandler"></a>

## CredentialsHandler Objects

```python
class CredentialsHandler()
```

<a id="parse_credentials.parse_credentials.CredentialsHandler.__init__"></a>

#### \_\_init\_\_

```python
def __init__(credentials_path: str) -> None
```

Class for handling credentials to HCP and HCI

**Arguments**:

- `credentials_path` (`str`): Path to the credentials JSON file

