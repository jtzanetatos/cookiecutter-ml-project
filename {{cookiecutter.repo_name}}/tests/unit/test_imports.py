import importlib


def test_import_package_root() -> None:
    mod = importlib.import_module("{{cookiecutter.project_slug}}")
    assert mod is not None
