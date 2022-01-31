This project utilizes the pytest framework for automation testing.

## Prerequisites
For both test authoring and execution:

* [Python 3.9+](https://www.python.org)
* _Note: Python 3.6 is no longer available in the Optum appstore_

## Configuration

There are 2 configurations for this project:
* `config.yaml` - contains the generic configuration for the project
* `choice_dtc.yaml` - contains the specific configuration for the domain

`config.yaml`
* `browser:` General browser settings.
  * `name:` String. The name of the browser to use (e.g., `chrome`).
  * `url:` String. Base ICS URL.
  * `headless:` Boolean. Whether to run the browser in headless mode.
  * `size:` String. Window dimensions in format `width,height` (e.g., `1920,1080`).
  * `extensions:` Boolean. Whether to allow the use of installed extensions.
  * `gpu:` Boolean. Whether to enable GPU acceleration.

* `device:` String. The name of the device to use (e.g., `iPhone X`).
* `environment`: String. Test environment to use (e.g., `model`, `supp`).
* `execution_mode`: String. Execution mode to use (e.g., `local`, `remote`).
* `log_level`: String. Log level to use (e.g., `DEBUG`, `INFO`, `WARNING`, `ERROR`).

`choice_dtc.yaml`
* `choice_dtc_site:` List of strings. The list of DTC sites to test.
  * `model:` String. Model Test environment.
    * `url:` String. Required. Base url of the model environment.
  * `supp:` String. Supp Test environment.
    * `url:` String. Required. Base url of the supp environment.

You can also create a file named config.override.yaml to selectively override
a subset of the defaults without directly changing config.yaml, which is useful
when you want to avoid Git picking up those changes. Example override file:

```yaml
browser:
  headless: true
```

## Development
Prerequisites:

* [Poetry 1.0.0+](https://github.com/python-poetry/poetry)
  * Windows: `pip install poetry`

After cloning, prepare your development environment like so:

* Set up a Python virtual environment: `poetry install`
* Activate the pre-commit hooks: `poetry run pre-commit install`

[poetry](https://github.com/python-poetry/poetry) is a tool to handle dependency installation as well as building and packaging of Python packages. It only needs one file to do all of that: the new, [standardized](https://www.python.org/dev/peps/pep-0518/) `pyproject.toml`.

In other words, poetry uses pyproject.toml to replace `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in` and the newly added `Pipfile`.

After cloning this repository, prepare your development environment like so:

* Set up the Python virtual environment: `poetry install`
* Activate the pre-commit hooks: `poetry run pre-commit install`
