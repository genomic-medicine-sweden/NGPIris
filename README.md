# NGPIris-2
Rework of NGPIris. We might change the name, but right now NGPIris 2 is the WIP name

## Proposed structure

## CLI
* Which commands are needed?
  ```
  delete    Delete a file on the HCP
  download  Download files using a given query
  search    List all file hits for a given query by directly calling HCP
  upload    Upload fastq files / fastq folder structure
  ```
* Should we use Click?

## File structure of this repository
This was the structure used in the old repo:
```
.
├── NGPIris
│   ├── __init__.py
│   ├── cli
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── functions.py
│   ├── hci
│   │   ├── __init__.py
│   │   ├── hci.py
│   │   └── template_query.json
│   ├── hcp
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── hcp.py
│   │   ├── helpers.py
│   │   └── interactive.py
│   └── preproc
│       ├── __init__.py
│       └── preproc.py
├── README.md
├── config.ini
├── credentials.json
├── docs
│   └── package.md
├── pyproject.toml
├── reference
│   ├── covidMetadataAllowedValues.csv
│   └── covidMetadataTemplate.csv
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
├── setup.py
├── setup.sh
├── test.py
└── tests
    ├── __init__.py
    ├── data
    │   ├── test.json
    │   ├── test_reads_R1.fasterq
    │   └── test_reads_R1.fastq.gz
    ├── test_cmds.py
    └── test_hcp.py

```

A loose general structure could be the following:
```
.
└── NGPIris
    ├── __init__.py
    ├── cli
    │   ├── __init__.py
    │   ├── base.py
    │   ├── functions.py
    │   └── utils.py
    ├── hci
    │   ├── __init__.py
    │   ├── hci.py
    │   └── template_query.json
    ├── hcp
    │   ├── __init__.py
    │   ├── config.py
    │   ├── errors.py
    │   ├── hcp.py
    │   ├── helpers.py
    │   └── interactive.py
    └── preproc
        ├── __init__.py
        └── preproc.py
```

## Python package?
