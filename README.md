# Artifact Registry tools for PyPI
This repository contains an alternate [keyring](https://pypi.python.org/pypi/keyring) backend implementation to help with interacting with PyPI Repositories hosted on Artifact Registry.

## Authentication
artifactregistry-gauth is a python package which allows you to configure keyring to interact with PyPI repositories stored in Artifact Registry.

The backend automatically searches for credentials from the environment and authenticates to Artifact Registry. It looks for credentials in the following order:

1. [Google Application Default Credentials](https://developers.google.com/accounts/docs/application-default-credentials).
2. From the `gcloud` SDK. (i.e., the access token printed via `gcloud config config-helper --format='value(credential.access_token)'`)
    * Hint: You can see which account is active with the command `gcloud config config-helper --format='value(configuration.properties.core.account)'`
3. If neither of them exist, an error occurs.

To use the keyring backend:

1. Log in

	Option 1: log in as a service account:

	(1). Using a JSON file that contains a service account key:

		`$ export GOOGLE_APPLICATION_CREDENTIALS=[path/to/key.json]`

	(2). Or using gcloud:

		`$ gcloud auth application-default login`

	Option 2: log in as an end user via gcloud:

		`$ gcloud auth login`

2. Configure twine (.pypirc) and pip (pip.conf) tools to connect to the repository. Use the output from the following command:

	`gcloud alpha artifacts print-settings pypi`

	In your `.pypirc` file add:

	```
	[disutils]
	index-servers =
		REPOSITORY_ID

	[REPOSITORY_ID]
	repository: https://LOCATION-pypi.pkg.dev/PROJECT_ID/REPOSITORY_ID/
	```

	In your `pip.conf` file add:

	```
	[global]
	index-url = https://LOCATION-pypi.pkg.dev/PROJECT_ID/REPOSITORY_ID/simple/
	```
3. Install the artifactregistry-gauth package

	`pip install artifactregistry-gauth`

  List backends to confirm the installation.

  	`keyring --list-backends`

  The list should include

  	-`ChainerBackend(priority:10)`
  	-`GooglePyPIAuth(priority:9)`
