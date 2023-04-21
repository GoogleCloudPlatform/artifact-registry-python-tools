"""
Copyright 2021 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

import google
from google.auth.transport import requests
from google.auth.exceptions import DefaultCredentialsError

import keyring
from keyring import backend
from keyring import credentials
from urllib.parse import urlparse

import json
import logging
import subprocess

class GooglePythonAuth(backend.KeyringBackend):
  priority = 9

  """
  Higher priority than typical recommended backends - but one less priority than Chainer Backend.
  """

  def get_password(self,service,username):
    url = urlparse(service)
    if url.hostname is None or not url.hostname.endswith(".pkg.dev"):
      return

    #trying application default credentials otherwise fall back to gcloud credentials command
    try:
      CREDENTIAL_SCOPES =["https://www.googleapis.com/auth/cloud-platform"]
      credentials, project_id = google.auth.default(scopes=CREDENTIAL_SCOPES)
      credentials.refresh(requests.Request())
      return credentials.token
    except Exception as e:
      logging.warning("Failed to retrieve Application Default Credentials: {0}".format(e))

    try:
      credentials = get_gcloud_credential()
      return credentials
    except Exception as e:
      logging.warning("Failed to retrieve credentials from gcloud: {0}".format(e))

    logging.warning("Artifact Registry PyPI Keyring: No credentials could be found.")
    raise Exception("Failed to find credentials, Please run: `gcloud auth application-default login or export GOOGLE_APPLICATION_CREDENTIALS=<path/to/service/account/key>`")

  def set_password(self,service,username,password):
    raise NotImplementedError()

  def delete_password(self,service,username):
    raise NotImplementedError()

  def get_credential(self,service,username):
    password = self.get_password(service,username)
    if password is not None:
      return credentials.SimpleCredential("oauth2accesstoken",password)
    return None


def get_gcloud_credential():

  # check if the user has set a GOOGLE_ACCESS_TOKEN env var
  # this value can be retrieved from
  #
  #  $ gcloud auth print-access-token
  #  (or)
  #  $ GOOGLE_ACCESS_TOKEN=$(gcloud auth print-access-token) python3 ...
  #
  # we will return this token immediately.
  # developers please note that, this token is only valid for 1 hour.
  access_token = os.getenv("GOOGLE_ACCESS_TOKEN")
  if access_token is not None:
    logging.warning("Using access token from GOOGLE_ACCESS_TOKEN env var...")
    return access_token

  # check if the user has set a GOOGLE_ACCESS_TOKEN_CREDENTIALS
  # this is a json file, which can be exported like
  #
  #  $ gcloud config config-helper --format="json(credential)" > key.json
  #  $ GOOGLE_ACCESS_TOKEN_CREDENTIALS=key.json python3 some.py
  #
  access_token_credentials_file = os.getenv("GOOGLE_ACCESS_TOKEN_CREDENTIALS")
  if access_token_credentials_file is not None:
    logging.warning("Using access token from file defined in GOOGLE_ACCESS_TOKEN_CREDENTIALS env var...")
    with open(access_token_credentials_file) as fp:
      json_data = fp.read()
  else:
    # fall back to fetching credentials from gcloud if Application Default Credentials fails
    # and if other env var approaches fail
    try:
      logging.warning("Trying to retrieve credentials from gcloud...")
      command = subprocess.run(['gcloud','config','config-helper','--format=json(credential)'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
      raise Exception ("gcloud command exited with status: {0}".format(e))
    json_data = command.stdout

  result = json.loads(json_data)
  credential = result.get("credential")
  if credential is None:
    raise Exception("No credential returned from gcloud")
  if "access_token" not in credential or "token_expiry" not in credential:
    raise Exception("Malformed response from gcloud")
  return credential.get("access_token")

