# Mforce

A record keeping utility for user data


## Prerequisites

* Python 3.10.0
* Pipenv

If you don't have Pipenv, you can use your preferred tool. The `requirements.txt` file is generated by running `pipenv run pip freeze > requirements.txt` and should have a list of all required dependencies.

## Testing

Clone the project, navigate into the directory and run the commands below

```
# Install all dependencies (or via requirements.txt)
$ pipenv install

# Run tests via unittest module
$ python -m unittest tests/* -v
```

## Pre-commit hooks

The project uses a few pre-commit hooks to ensure proper code formatting, type hints and that methods a called with expected data types.

Enable this by running

```commandline
pre-commit install
```

You can also run this manually with

```commandline
pre-commit run --all-files
```

For more information on the various hooks, please check `.pre-commit-config.yaml`
