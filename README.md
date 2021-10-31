# MySQL and Python Billing 
[![Publish](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/release.yml/badge.svg)](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/release.yml)
[![Syntax Highlighting](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/main.yml/badge.svg)](https://github.com/Smilin-Dominator/mysql-and-python-billing/actions/workflows/main.yml)

# How To Use It?
***DELETE THIS FILE WHEN YOU'VE READ IT, ANYONE OTHER UNTRUSTED PARTY WHO READS THIS IS A THREAT***
### Prerequisites
- Running From Source
    - <font size="6">Download [Python 3.9.4](https://www.python.org/downloads/release/python-394/) and install it.
    - Then you're good to go! Just go to the directory where you downloaded it (via Powershell) and type
     `python -m pip install rich pyyaml` and then `python main.py`, it'll check for log.txt, if it's not present, it'll run
    the shell script related to your OS! **Do Not Delete Your log.txt, If you want you may clear it, but not delete it.**</font>
- Running The .exe
    - <font size="6">Download The Latest (main.zip) From The GitHub Page
        **(Optional: Read README.md, its the manual)**
    - You can either open Powershell and Type `./main.exe` or just click the Icon And It Should Setup Everything</font>
- Notes Common To Both
    - If you have a MySQL Server instance, don't create a docker container, but if you don't install [docker-compose](https://docs.docker.com/compose/install/) and then run the program.

# Index
- [Log](./docs/log.md)
- Function Lists
  - [main.py](./docs/functions/main.md)
  - [connector.py](./docs/functions/connector.md)
  - [verify.py](./docs/functions/verify.md)
  - [sql-client.py](./docs/functions/sql-client.md)
- Options For [config.yaml](./docs/functions/configuration_options.md)
- [Scenarios and Combating Them](./docs/scenarios.md)