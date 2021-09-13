## Contents


### The What


### The Why


### The How


### This [update](https://semver.org/) is:
- [ ] **MAJOR** - when you make incompatible API changes
- [ ] **MINOR** - when you add functionality in a backwards compatible manner
- [ ] **PATCH** - when you make backwards compatible bug fixes or documentation/instructions

## Test Procedure

### Installation and initiation
* `git clone git@github.com:genomic-medicine-sweden/HCPInterface.git`
* `cd HCPInterface && git checkout <BRANCH>`
* `bash setup.sh`
* `source activate hpcenv`

### Tests
* `pytest tests/`
* Potential additional tests

### Expected outcome:
* Pytest resolves without crashes
* Potential additional results

## Confirmations:
- [ ] Code reviewed by @octocat
- [ ] Code tested by @octocat
