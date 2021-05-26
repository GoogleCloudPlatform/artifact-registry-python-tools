import pluggy

import google_artifactregistry_auth

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_testenv_install_deps(venv, action):
    venv._install(
        [
            "keyrings.google-artifactregistry-auth=={}".format(
                google_artifactregistry_auth.__version__
            )
        ],
        action=action,
    )
