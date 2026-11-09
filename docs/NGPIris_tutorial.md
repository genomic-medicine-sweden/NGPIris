# NGPIris beginner's tutorial

```{contents} Outline of the tutorial
:depth: 3
:backlinks: none
:local:
```

---

:::{important}
This tutorial was written for version v5.7.0
:::

## Introduction

Welcome to the {py:mod}`NGPIris` beginner's tutorial! In this tutorial, we will show you how to get started with {py:mod}`NGPIris`.

We will start by discussing the terminology used and what the purpose of {py:mod}`NGPIris` is. Then we will cover how to install {py:mod}`NGPIris`, followed by an introduction on how to use the {term}`CLI` and Python package respectively.

What follows after that are some example use cases of {py:mod}`NGPIris` both in the {term}`CLI` and as the Python code counterpart.

:::{tip}
Throughout this tutorial, there will be tabs for either viewing the {term}`CLI` version or the Python version of a given example in sections like _[](#communicating-with-ngpr)_ and _[](#communicating-with-ngpi)_. This is useful for comparing how {term}`CLI` corresponds to a Python implementation.
:::

### Terminology

:::{tip}
If you stumble upon terms that are unfamiliar to you, you can most likely find a definition in the [](./glossary.rst).
:::

Within the {term}`NGP`, we have the {term}`NGPr` and the {term}`NGPi` which will be our main focus for this tutorial. For information about these services, please see the respective definitions in the [](./glossary.rst).

The most important take-away is that when we refer to the {term}`HCP` we also refer to the {term}`NGPr` and vice versa. Similarly, when we refer to the {term}`HCI` we also refer to the {term}`NGPi` and vice versa.

:::{important}

```{math}
\text{"HCP"} \Leftrightarrow \text{"NGPr"}

\text{"HCI"} \Leftrightarrow \text{"NGPi"}
```

:::

### The purpose of {py:mod}`NGPIris`

```{figure} ./_static/Iris_HCP_HCI.png
:figname: Iris_HCP_HCI
:alt: Diagram of how an end user or application, the HCP and the HCI interact with each other via NGPIris
:align: center
:scale: 10

Diagram of how an end user or application, the {term}`HCP`/{term}`NGPr` and the {term}`HCI`/{term}`NGPi` interact with each other via {py:mod}`NGPIris`.
```

{py:mod}`NGPIris` is meant to be the main way of accessing the {term}`NGPr` and {term}`NGPi` from either an end user or an application. It achieves this by either being used as a {term}`CLI` or as a Python package that can be implemented into any Python application such as a [Django](https://www.djangoproject.com/) web app for example.

The backend of {py:mod}`NGPIris` is an implementation of {term}`HCP`'s own variant of {term}`S3` and the {term}`HCI`'s own {term}`REST API` for making queries among other things. As such, {py:mod}`NGPIris` becomes one standardized collection of Python classes, methods, etc. for the specialized purposes of the {term}`NGP`.

## Installing {py:mod}`NGPIris`

The simplest way to install {py:mod}`NGPIris` is by using `pip`. You might also want to create and select a {term}`virtual environment` before installation, to avoid potential cluttering.

::::{tab-set}

:::{tab-item} pip

```{code} sh
pip install NGPIris
```

:::

:::{tab-item} uv

```{code} sh
uv add NGPIris
```

:::

:::{tab-item} git

1. Clone this repository
2. Open a terminal in your local copy of the repository
3. Run `pip install .` at the root of the repository. This will install Iris along with the required Python packages in your current Python environment

:::

::::

(prereq)=

### Prerequisites

In order to connect to the {term}`NGPr` and the {term}`NGPi`, you need to have a filled out credentials file:

```{include} ../credentials/credentials_template.json
:code: json
```

The information to be included in this credentials can be requested by your local {term}`GMC` admin.

## How to use the {term}`CLI`

:::{seealso}
See [_The NGPIris CLI_](NGPIris.cli) for more extensive information about the {term}`CLI`.
:::

The {term}`CLI` consist of one main command `iris`, which in turn consist of various sub commands. This section will focus on the `iris` command itself, while the sub commands are described in [the upcoming sections](#communicating-with-ngpr).

### Supplying credentials

When we use `iris`, we need to supply [credentials](#prereq) in some way. There are two ways to do so: Either by supplying the `-c`/`--credentials` flag or by supplying the credentials to a prompt upon running a command. The `-c` flag accepts a path to your [`credentials.json`](#prereq) file.

Let's look at an example where we attempt to [list the available buckets](#list-buckets) on the {term}`HCP`:

::::{grid}

:::{grid-item}

Running `iris` with the `-c` flag along with a path to a credentials file:

```{code} sh
iris -c path/to/credentials.json list-buckets
```

:::

:::{grid-item}
Example of running `iris` and supplying credentials with prompts:

```{code} sh
iris list-buckets
Please enter your tenant endpoint: my_example_tenant
Please enter your base64 hashed username (a.k.a aws_access_key_id): my_example_user
Please enter your md5 hashed password (a.k.a aws_secret_access_key):
Repeat for confirmation:
```

:::{danger}
Please note that the input `my_example_tenant` and `my_example_user` will be different for each each user.
:::

::::

Either input should result in a table view of all buckets that your user is allowed to see:

```{code} sh
Bucket                                Ingested volume    Storage capacity used    Hard quota    Storage capacity used (%)    Soft quota (%)    Object count    Owner     Description
------------------------------------  -----------------  -----------------------  ------------  ---------------------------  ----------------  --------------  --------  ------------
Bucket_1
Bucket_2
...
```

:::{attention}
We generally recommend the approach of using `-c` flag.
:::

### The `--debug` flag

Sometimes we stumble upon new problems that that has not been foreseen during the development of {py:mod}`NGPIris`. As such, when {py:mod}`NGPIris` misbehaves it can be useful to get the full debug log in order to figure out where the problem originates. This can be achieved by supplying the `--debug` flag:

```{code} sh
iris --debug
```

## How to use the Python package

:::{seealso}
For more extensive information about {py:mod}`NGPIris` Python package, see [_NGPIris base package_](NGPIris_base).
:::

The primary imports of interest in the {py:mod}`NGPIris` Python package is the {py:class}`~NGPIris.HCPHandler` and {py:class}`~NGPIris.HCIHandler`. They can both be found in the base package {py:mod}`NGPIris`:

```{code} python
from NGPIris import HCPHandler, HCIHandler
```

Both classes only have one required argument in their respective constructor which is `credentials`. `credentials` can either be a {py:type}`str` or {py:type}`dict[str, str]`. If it is a {py:type}`str`, then that string should be a path to a [`credentials.json`](#prereq) file:

```{code} python
from NGPIris import HCPHandler, HCIHandler

hcp_h = HCPHandler("path/to/credentials.json")

hci_h = HCIHandler("path/to/credentials.json")
```

If it is a {py:type}`dict[str, str]` then the respective credential data for either the HCP or the HCI is expected:

```{code} python
from NGPIris import HCPHandler, HCIHandler

hcp_h = HCPHandler(
    {
        "endpoint": "",
        "username": "",
        "password": "",
    }
)

hci_h = HCIHandler(
    {
        "username": "",
        "password": "",
        "address": "",
        "auth_port": "",
        "api_port": "",
    }
)
```

### An important note regarding {py:class}`~NGPIris.HCPHandler`

Most operations using the {py:class}`~NGPIris.HCPHandler` will require a bucket. To assign or "mount" a bucket do the following:

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")
```

(communicating-with-ngpr)=

## The basics of communicating with NGPr

The following sections will provide basic examples of how to use {py:mod}`NGPIris` both as a {term}`CLI` and as Python code.

:::{tip}
By using the tabs in the following subsections, you can compare the {term}`CLI` version or the Python version of a given example.
:::

(list-buckets)=

### Listing buckets

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json list-buckets
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

print(hcp_h.list_buckets())
```

:::

::::

(list-objs)=

### List objects

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json list-objects my_bucket
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

print(list(hcp_h.list_objects()))
```

:::

::::

### Upload objects

Assume that `a/local/file.txt` is a file on your local filesystem.

#### Uploading to the "root" of the bucket

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json upload my_bucket a/local/file.txt /
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

my_local_file = "a/local/file.txt"

hcp_h.upload_file(my_local_file)
```

The default value for `key` in {py:meth}`~NGPIris.HCPHandler.upload_file` is the same as `local_file_path`, which means that `hcp_h.upload_file(my_local_file)` is equivalent to `hcp_h.upload_file(my_local_file, my_local_file)`.

::::{seealso}
{py:meth}`~NGPIris.HCPHandler.upload_folder`
::::

:::

::::

#### Uploading to a "folder" in the bucket

Assume that you wish to put your object in a folder called `a/path/on/the/bucket/`.

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json upload my_bucket a/local/file.txt a/path/on/the/bucket/
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

my_local_file = "a/local/file.txt"

hcp_h.upload_file(
    my_local_file,
    "a/path/on/the/bucket/" + my_local_file,
)
```

```{seealso}
{py:meth}`~NGPIris.HCPHandler.upload_folder`
```

:::

::::

### Download objects

Assume that you wish to download an object `a/path/on/the/bucket/file.txt` to a local filesystem path `a/local/path/`.

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json download my_bucket a/path/on/the/bucket/file.txt a/local/path/
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

file_name = "file.txt"

bucket_path = "a/path/on/the/bucket/"

my_local_file_path = "a/local/path/"

hcp_h.download_file(
    bucket_path + file_name,
    my_local_file_path + file_name,
)
```

```{seealso}
{py:meth}`~NGPIris.HCPHandler.download_folder`
```

:::

::::

### Delete objects

#### Deleting one object

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json delete -m file my_bucket my/file/to/be/deleted.txt
```

```{tip}
The `-dr`/`--dry_run` flag can be used to simulate the outcome of running the command.
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

hcp_h.delete_object("my/file/to/be/deleted.txt")
```

```{seealso}
{py:meth}`~NGPIris.HCPHandler.delete_objects`
```

:::

::::

#### Deleting a "folder"

::::{tab-set}

:::{tab-item} CLI
:sync: cli

```{code} sh
iris -c path/to/credentials.json delete my_bucket my/folder/to/be/deleted/
```

```{tip}
The `-dr`/`--dry_run` flag can be used to simulate the outcome of running the command.
```

```{note}
Notice that `folder` is the default value for the `-m` flag, as such `-m folder` is not needed.
```

:::

:::{tab-item} Python
:sync: python

```{code} python
from NGPIris import HCPHandler

hcp_h = HCPHandler("path/to/credentials.json")

hcp_h.mount_bucket("my_bucket")

hcp_h.delete_folder("my/folder/to/be/deleted/")
```

:::

::::

(communicating-with-ngpi)=

## The basics of communicating with NGPi
