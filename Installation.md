# Installation and Configuration

- [Installation and Configuration](#installation-and-configuration)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Execution](#execution)

## Prerequisites

- If you are behind a proxy, you should set the environment variables
  ``http_proxy`` and ``https_proxy`` at the beginning of your session.
  Both the setup tools as well as the test scripts will evaluate the
  content of these variables when making HTTP requests.

  Example for Windows users:
  ```
  set http_proxy=http://localhost:3128
  set https_proxy=%http_proxy%
  ```

  Example for PowerShell
  ```powershell
  $env:http_proxy="http://localhost:3128"
  $env:https_proxy=$env:http_proxy
  ```



- Python3 should be installed on your computer. The following instructions
  will assume that the interpreter is installed under the alias ``python``.
  Users of some operating systems (e.g. Debian, Ubuntu) will have to use
  ``python3`` instead.

- for the virtual environment the pipenv package should be installed with pip. For this the command ```pip install pipenv``` can be used

- gauge should be installed in order to run the specification [gauge install instruction](https://docs.gauge.org/getting_started/installing-gauge.htm)


## Setup

In this repository

```
git clone https://github.com/eu-digital-green-certificates/dgc-api-tests.git
cd dgc-api-tests

pipenv install

pipenv shell
```

## Configuration

In order to run the tests multiple certificates are needed to create DSC certificates and to authenticate against the DGC-Gateway.

Gauge supports multiple environments in which the configuration can change. For that reason a `.gitignore` file is configured in order to use a local environment. In order to change the baseUrl a config file at `/env/local/defaupt.properties` is needed. This file can look like this:

```properties
baseurl = https://gateway.url
```

Also some Authentication/UPLOAD/CSCA certificates are needed in order to upload and delete certificates. The folder structure looks like this:

| path                                       | description                                                                             |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| /certificates/auth.pem                     | PEM encoded Authentication (NBTLS) certificate                                          |
| /certificates/key_auth.pem                 | PEM encoded private key of the Authentication (NBTLS) certificate                       |
| /certificates/csca.pem                     | PEM encoded CSCA (NBCSCA) certificate                                                   |
| /certificates/key_csca.pem                 | PEM encoded private key of CSCA (NBCSCA) certificate                                    |
| /certificates/upload.pem                   | PEM encoded Upload (NBUS) certificate                                                   |
| /certificates/key_upload.pem               | PEM encoded private key of Upload (NBUS) certificate                                    |
| /certificates/secondCountry/auth.pem       | PEM encoded Authentication (NBTLS) certificate of the second country                    |
| /certificates/secondCountry/key_auth.pem   | PEM encoded private key of the Authentication (NBTLS) certificate of the second country |
| /certificates/secondCountry/csca.pem       | PEM encoded CSCA (NBCSCA) certificate of the second country                             |
| /certificates/secondCountry/key_csca.pem   | PEM encoded private key of CSCA (NBCSCA) certificate of the second country              |
| /certificates/secondCountry/upload.pem     | PEM encoded Upload (NBUS) certificate of the second country                             |
| /certificates/secondCountry/key_upload.pem | PEM encoded private key of Upload (NBUS) certificate of the second country              |


## Execution

Gauge is used for the execution of the test cases. For this ```gauge run --env local``` is used to run the test cases against the local configuration. For more information on how the execution can be tweaked are in the [gauge documentation](https://docs.gauge.org/execution.htmlos=windows&language=python&ide=vscode#multiple-arguments-passed-to-gauge-run).
