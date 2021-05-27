import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_testenv_install_deps(venv, action):
    venv._install(venv.envconfig.config.requires, action=action)
