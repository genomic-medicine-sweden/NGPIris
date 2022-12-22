# NGP Iris 👁
NGP Iris is a light-weight tool for interacting with a [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) backed Hitachi Content Platform. 
NGP Iris is designed with two use cases in mind:
* A simple, clear, real-time interaction with NGPr file management
* Improving process flow for performing off-site data analysis by using automated transfer scripts

## Getting started

### Easy installation
```
pip install NGPIris
```

### Requirements
* [Anaconda](https://www.anaconda.com/products/individual-d) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for conda environment
* pip installed
* NGPr credentials 

### NGPr Credentials

* Receive your NGPr credentials from your local NGP admin
* Edit NGPIris/credentials.json

```
{
"endpoint" : "https://ACCESSNODESERVERNAME:PORT",
"aws_access_key_id" : "ALONGSTRINGOFCHARSTHATSYMBOLIZEYOURID",
"aws_secret_access_key" : "ANEVENLONGERSTRINGOFCHARSTHATSYMBOLIZEYOURPASSWORD",
"ngpi_password": "p@ssw0rd"
}
```

## Introduction

NGP Iris provides two  parts. 
A command line interface for intuitive manipulation of single files.
And a python package to import easy to use file manipulation functions

Both of these modes of interaction pipe processes to the HCPManager class. This class is responsible for connecting to the specified endpoints with the provided access keys and manages the upload, download, and querying against the contents of the available buckets.

The connection is made on a higher resource level rather than client level. This will come to change in the future as more advanced features are introduced.


## Usage

### Command Line Interface
Successful installation means the command `iris --help` is active.
Iris is constructed to have additional help for each subcommand. So, e.g., run `iris -c CREDENTIALS -b BUCKET download --help` to recieve all the download information.

```iris
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

#### Search for a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE search MYDU*TESTFILE --mode ngpr`

This command will search the bucket BUCKETNAME for the object `MYDU*TESTFILE`.  
The search command supports both asterix (*) completion and most regex.  

`--mode ngpr` uses the NGPr search mode to find this file. This is the slowest mode, but also the one that has existed the longest.  

#### Download a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE download /tmp/MYDUMBTESTFILE -o ./MYLOCALTESTFILE --silent --mode ngpr -f`

This command will download your previously uploaded testfile, and put it in your current directory.  
`--mode ngpr` uses the NGPr search mode to find this file. This is the slowest mode, but also the one that has existed the longest. 
Alternatively use `--mode None` to skip searching for the file altogether. This is lightening fast. But requires the file name to be exactly correct.   
`-f` will overwrite any locally stored file with the same name  
`--silent` will remove the download progress bar. Which is sometimes useful when scripting  

#### Upload a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE upload FILE2UPLOAD -o /tmp/MYDUMBTESTFILE -a -s`

This command will upload your test file as `MYDUMBTESTFILE` on the bucket BUCKETNAME.  
`-a` allows non-fastq file formats.  
`-s` removes the transfer speed info. Which can get very spammy in scripts.  

#### Delete a file
`iris -b BUCKETNAME -c CREDENTIALS_FILE delete MYDUMBTESTFILE`

This command will delete the file MYDUMBTESTFILE.  
By default you will be prompted that you are certain that you wish to remove your file.  


#### Additional commands
`iris` contains more commands and flags for additional operations. Such as search, deleting, or doing things in a more nuanced way. The help menu packaged with the program is always kept up to date, so refer to that to easily discover more.

For more use cases, check out [the CLI file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/cli/functions.py)

## As a package
For usage of Iris as a package see the [package documentation](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/docs/package.md)

For an index of all HCPManager functionality, check out the [source file](https://github.com/genomic-medicine-sweden/NGPIris/blob/master/NGPIris/hcp/hcp.py)


## Development build
``` 
git clone git@github.com:genomic-medicine-sweden/NGPIris.git
cd NGPIris
bash setup.sh iris
source activate iris
```
