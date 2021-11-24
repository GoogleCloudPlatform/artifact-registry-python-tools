# Artifact Registry tools for Python
This repository contains an alternate [keyring](https://pypi.python.org/pypi/keyring) backend implementation to help with interacting with Python repositories hosted on Artifact Registry.

## Authentication
`keyrings.google-artifactregistry-auth` is a Python package which allows you to configure keyring to interact with Python repositories stored in Artifact Registry.

The backend automatically searches for credentials from the environment and authenticates to Artifact Registry. It looks for credentials in the following order:

1. [Google Application Default Credentials](https://developers.google.com/accounts/docs/application-default-credentials).
2. From the `gcloud` SDK. (i.e., the access token printed via `gcloud config config-helper --format='value(credential.access_token)'`)
    * Hint: You can see which account is active with the command `gcloud config config-helper --format='value(configuration.properties.core.account)'`
3. If neither of them exist, an error occurs.

To use the keyring backend:

1. Log in

    Option 1: log in as a service account:

    (1). Using a JSON file that contains a service account key:

    ```
    $ export GOOGLE_APPLICATION_CREDENTIALS=[path/to/key.json]
    ```

    (2). Or using `gcloud`:

    ```
    $ gcloud auth application-default login
    ```

    Option 2: log in as an end user via `gcloud`:

    ```
    $ gcloud auth login
    ```

2. Configure twine (`.pypirc`) and pip (`pip.conf`) tools to connect to the repository. Use the output from the following command:

        $ gcloud artifacts print-settings python

    In your `.pypirc` file add:

    ```ini
    [disutils]
    index-servers =
        REPOSITORY_ID

    [REPOSITORY_ID]
    repository = https://LOCATION-python.pkg.dev/PROJECT_ID/REPOSITORY_ID/
    ```

    In your `pip.conf` file add:

    ```ini
    [global]
    extra-index-url = https://LOCATION-python.pkg.dev/PROJECT_ID/REPOSITORY_ID/simple/
    ```
3. Install the `keyrings.google-artifactregistry-auth` package

    ```
    $ pip install keyrings.google-artifactregistry-auth
    ```

    List backends to confirm the installation.

    ```
    $ keyring --list-backends
    ```

    The list should include

    * `keyrings.gauth.GooglePythonAuth (priority: 9)`
    * `keyring.backends.chainer.ChainerBackend (priority: -1)`
    * `keyring.backends.fail.Keyring (priority: 0)`

## Usage with other tools

### Usage with `tox`

The [`tox` tool](https://pypi.org/project/tox/) is a testing and automation tool.

Because the credential helper needs to be installed _before_ any private
dependencies are installed, it needs to be bootstrapped into the `tox`
environment via a plugin.

To do this, specify the `keyrings.google-artifactregistry-auth` package via the
[`requires`](https://tox.readthedocs.io/en/latest/config.html#conf-requires)
requirement in your `tox.ini` file:

```ini
[tox]
envlist = py
requires = keyrings.google-artifactregistry-auth

[testenv]
deps = -r requirements.txt
```

You can then configure your `requirement.txt` file to use the Artifact Registry repo as
an extra index, and specify both public and private dependencies:

```
--extra-index-url https://[REGION]-python.pkg.dev/[PROJECT_ID]/[REPOSITORY]/simple

# samplepackage will be installed directly from PyPI
samplepackage
# mypackage will be installed from the Artifact Registry repository
mypackage
```
