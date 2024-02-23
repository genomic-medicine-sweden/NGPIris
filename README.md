# NGP Iris 2 👀
Rework of the original [NGP Iris](https://github.com/genomic-medicine-sweden/NGPIris). The major difference is that the previous version was based on `boto3` sessions instead of clients. By using clients we are able to do some more "low-level" operations like setting Access Control Lists (ACLs).

**Do note that we might change the name, but right now NGP Iris 2 is the WIP name.**

---

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

---

## Usage
To be added.