#!/bin/bash
#
# Copyright 2021 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# A script to test Artifact Registry's Keyring library installation in the current environment.
#
# Internally this script is used to test installation on DLVM/DL Container
# images.
# - https://cloud.google.com/deep-learning-vm
# - https://cloud.google.com/ai-platform/deep-learning-containers
#
# The list of the container images can be found in:
# https://cloud.google.com/ai-platform/deep-learning-containers/docs/choosing-container

set -ex

PYTHON_BINARY=$(which python3)

${PYTHON_BINARY} -m pip install "keyrings.google-artifactregistry-auth"


if ${PYTHON_BINARY} -m pip show "keyrings.google-artifactregistry-auth"; then
      echo "Artifact Regsitry Keyring Auth is installed."
else
      echo "keyrings.google-artifactregistry-auth package is not installed"
fi
