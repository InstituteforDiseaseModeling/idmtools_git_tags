![Staging: idmtools_git_tags]

# idmtools_git_tags

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [User Installation](#user-installation)
  - [Pre-requisites](#pre-requisites)
- [Development Environment Setup](#development-environment-setup)
  - [First Time Setup](#first-time-setup)
  - [Development Tips](#development-tips)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# User Installation

```bash
pip install idmtools-git-tags --extra-index-url=https://packages.idmod.org/api/pypi/pypi-production/simple
```

## Pre-requisites
- Python 3.6-3.8 x64
- idmtools 1.6.2 or greater

# Development Environment Setup

When setting up your environment for the first time, you can use the following instructions

## First Time Setup
1) Clone the repository:
   ```bash
   > git clone https://github.com/InstituteforDiseaseModeling/idmtools_git_tags.git
   ```
2) Create a virtualenv. On Windows, please use venv to create the environment
   `python -m venv idmtools_git_tags`
   On Unix(Mac/Linux) you can use venv or virtualenv
3) Activate the virtualenv
4) Then run `python ./.dev_scripts/bootstrap.py`. This will install all the tools. 

## Development Tips

There is a Makefile file available for most common development tasks. 

To see the list of rules with descriptions, run `make help`.

Here is a list of common commands
```bash
clean       -   Clean up temproary files
lint        -   Lint package and tests
test        -   Run All tests
coverage    -   Run tests and generate coverage report that is shown in browser
docs        -   Build docs
docs-server -   Build docs and server on localthost
```
On Windows, you can use `pymake` instead of `make`
