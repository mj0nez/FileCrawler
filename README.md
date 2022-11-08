# FileSwitch
------------
A file router for distributed systems, which (just) handles routing logic. Like a railway switch, this tool (neither) pulls nor pushes files (yet), it simply evaluates their names, meta-data or content and provides a route to get the files to their destination.

### **Note**: 
While the core idea - providing a simple, testable and extendable logic for file routings - of this project has not changed, features to actually move files will be added from now on.

This extends the projects uses cases to the underlying problem: Connecting different file sources and destinations. By implementing both, we allow ETL-tools like [Prefect](https://www.prefect.io/) and [Airflow](https://airflow.apache.org/) to utilize their proficiency in orchestrating and executing task/flows, while centralizing or separating the underlying routing logic and services with this package.

A standalone application, overseeing the complete routing process - from source to destination, is currently out of scope but may be implemented in the future. PR are more than welcome!


## Installation
---------------
As usual, use a virtualenv, and install via pip or pipenv. Because this package is not yet published on PyPi, please install the latest stable version from GitHub or from source.

```bash
pip install git+https://github.com/mj0nez/FileSwitch.git
```

Alternatively, clone this project and install in development mode:
```bash
git clone https://github.com/mj0nez/FileSwitch.git
cd FileSwitch
pip install -e .[dev]
```

## Development
--------------
Follow the above mentioned dev-installation. Format all files with [black](https://black.readthedocs.io).

PR are more than welcome to make this library better, or to add a feature that matches your needs. Nevertheless, don't forget adding tests for every aspect you. This project uses [pytest](http://pytest.org).


## License
----------
This library is licensed under the
*MIT* license, see the
[LICENSE file](LICENSE).
