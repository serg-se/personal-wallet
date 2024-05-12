"""
Tests for command line interface (CLI).
"""

import subprocess
from importlib import import_module
from importlib.metadata import version

from personal_wallet.cli import main


def test_main_module():
    """
    Exercise (most of) the code in the ``__main__`` module.
    """
    import_module("personal_wallet.__main__")


def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = subprocess.run(["python", "-m", "personal_wallet"], shell=True)
    assert result.returncode == 0


def test_entrypoint():
    """
    Is entrypoint script installed? (setup.py)
    """
    result = subprocess.run(["personal_wallet", "--help"], shell=True)
    assert result.returncode == 0


def test_usage(cli_runner):
    """
    Does CLI run w/o arguments, displaying usage instructions?
    """
    result = cli_runner.invoke(main)
    assert "Usage:" in result.output
    assert result.exit_code == 0


def test_version(cli_runner):
    """
    Does --version display information as expected?
    """
    expected_version = version("personal_wallet")
    result = cli_runner.invoke(main, "--version")
    assert result.output == f"personal_wallet, version {expected_version}\n"
    assert result.exit_code == 0


def test_example_command(cli_runner, config):
    """
    Is command available?
    """
    result = cli_runner.invoke(main, "balance", "--version")
    assert result.exit_code == 0
