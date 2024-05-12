from pathlib import Path

import pytest
from click.testing import CliRunner

PROJECT_DIR = Path(__file__).resolve().parent
TEST_CONFIG = PROJECT_DIR / "tests" / "test_config.ini"


@pytest.fixture
def config():
    return TEST_CONFIG


@pytest.fixture(autouse=True)
def csv_teardown():
    yield
    csvfile = PROJECT_DIR / "tests" / "transactions.csv"
    csvfile.unlink(missing_ok=True)


@pytest.fixture
def cli_runner():
    return CliRunner()
