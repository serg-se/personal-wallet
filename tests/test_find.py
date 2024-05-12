"""
Tests for 'find' command.
"""

import pytest

from personal_wallet.cli import main


class TestFindByNone:
    def test_found_none(self, cli_runner, config):
        result = cli_runner.invoke(main, ["find", "--config", config])
        found_none(result)


class TestFindByIndex:
    def test_found_by_index(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_index(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-i", WRONG_INDEX, "--config", config])
        found_none(result)

    def test_found_by_index_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-i", INDEX_RANGE, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_index_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-i", WRONG_INDEX_RANGE, "--config", config])
        found_none(result)


class TestFindByAmount:
    def test_found_by_amount(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-a", AMOUNT, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_amount(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-a", WRONG_AMOUNT, "--config", config])
        found_none(result)

    def test_found_by_amount_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-a", AMOUNT_RANGE, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_amount_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-a", WRONG_AMOUNT_RANGE, "--config", config])
        found_none(result)


class TestFindByDate:
    def test_found_by_date(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-d", DATE, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_date(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-d", WRONG_DATE, "--config", config])
        found_none(result)

    def test_found_by_date_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-d", DATE_RANGE, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_date_range(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-d", WRONG_DATE_RANGE, "--config", config])
        found_none(result)


class TestFindByDescription:
    def test_found_by_description_prefix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-s", DESCRIPTION_PREFIX, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_description_prefix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(
            main, ["find", "-s", WRONG_DESCRIPTION_PREFIX, "--config", config]
        )
        found_none(result)

    def test_found_by_description_suffix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-s", DESCRIPTION_SUFFIX, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_description_suffix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(
            main, ["find", "-s", WRONG_DESCRIPTION_SUFFIX, "--config", config]
        )
        found_none(result)

    def test_found_by_description_prefix_suffix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(
            main, ["find", "-s", DESCRIPTION_PREFIX_SUFFIX, "--config", config]
        )
        found_matching_transaction(result)

    def test_not_found_by_description_prefix_suffix(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(
            main, ["find", "-s", WRONG_DESCRIPTION_PREFIX_SUFFIX, "--config", config]
        )
        found_none(result)


class TestFindByCategory:
    def test_found_by_category(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-c", CATEGORY, "--config", config])
        found_matching_transaction(result)

    def test_not_found_by_category(self, cli_runner, config, add_transaction):
        result = cli_runner.invoke(main, ["find", "-c", WRONG_CATEGORY, "--config", config])
        found_none(result)


INDEX = "0"
DATE = "2024-06-03"
AMOUNT = "257"
CATEGORY = "expenses"
DESCRIPTION = "Bought a book"

INDEX_RANGE = "0..10"
AMOUNT_RANGE = "100..300"
DATE_RANGE = "2024-01-01..2025-01-01"
DESCRIPTION_PREFIX = "Boug%"
DESCRIPTION_SUFFIX = "%ook"
DESCRIPTION_PREFIX_SUFFIX = "%ught a b%"

WRONG_INDEX = "2"
WRONG_DATE = "2024-06-05"
WRONG_AMOUNT = "357"
WRONG_CATEGORY = "income"
WRONG_DESCRIPTION = "Bought a book"

WRONG_INDEX_RANGE = "5..10"
WRONG_AMOUNT_RANGE = "300..350"
WRONG_DATE_RANGE = "2021-01-01..2023-01-01"
WRONG_DESCRIPTION_PREFIX = "oug%"
WRONG_DESCRIPTION_SUFFIX = "%boo"
WRONG_DESCRIPTION_PREFIX_SUFFIX = "%ughta b%"


@pytest.fixture
def add_transaction(cli_runner, config):
    cli_runner.invoke(
        main,
        ["add", "-d", DATE, "-a", AMOUNT, "-c", CATEGORY, "-s", DESCRIPTION, "--config", config],
    )


def found_matching_transaction(result):
    assert DATE in result.output
    assert AMOUNT in result.output
    assert CATEGORY in result.output
    assert DESCRIPTION in result.output


def found_none(result):
    assert result.output == "\n"
