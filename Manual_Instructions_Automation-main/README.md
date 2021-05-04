# Manual_Instructions_Automation
All code relation to the automation of Silverback Manual Instructions process

# Manual_Instructions_Automation

## Dependencies

### Python

The solution is developed against [CPython 3.9.0](https://www.python.org/downloads/release/python-390/). Earlier runtime versions are not supported as they don't provide all the features used in the code.

Package dependencies will be maintained in [requirements.txt](requirements.txt). 

After installing Python, you should create a virtual environment and install the required packages.

It should just be a case of:

Windows:

```commandline
py -3.9 -m venv path\to\venv
path\to\venv\scripts\activate
pip install -r requirements.txt
```

*Nix:

```commandline
python3.9 -m venv path/to/venv
source path/to/venv/bin/activate
pip install -r requirements.txt
```

To install the development dependencies, the process is the same except you substitute [requirements-dev.txt](requirements-dev.txt) for [requirements.txt](requirements.txt) in the last command:

```commandline
...
pip install -r requirements-dev.txt
```

### .env file

You will need to create a file named .env under the Manual_Instructions_Automation directory.

This file will contain secrets and filepaths to be accessed by the robot.

You will need to create one for your local development environment.

The required filepaths can be inferred from [settings.py](Manual_Instructions_Automation/settings.py).

The structure of .env files is very simple - just key-value pairs.

```dotenv
some_key_name="some_super_secret_value"
my_api_key="wouldn't you like to know"
```




## Project Structure

### Source Code

All source code - the solution itself - lives under the [Manual_Instructions_Automation](Manual_Instructions_Automation) directory.

This is the directory that should be deployed onto production server.

## Deployment Checklist

- Make sure the right Python runtime is installed on the server, and that the Windows account which the robot is running as has access to it, you may need to set the Windows PATH Environment Variable.
- Deploy the [Manual_Instructions_Automation](Manual_Instructions_Automation) directory to the server, along with the [requirements.txt](requirements.txt) file. For subsequent deployments, I would suggest renaming the existing directory on the server rather than deleting it so that you can roll back easily.
- Create a virtual environment for the robot and install the packages. 
```commandline
cd path\to\Manual_Instructions_Automation
py -3.9 venv venv
venv\scripts\activate
pip install -r path\to\requirements.txt
```
Alternatively, just upgrade the packages in a pre-existing virtual environment via:
```commandline
path\to\venv\scripts\activate
pip install --upgrade -r path\to\requirements.txt
```
- Create a .env file containing the required secrets and file paths or reuse/update the one from the previous deployment.


