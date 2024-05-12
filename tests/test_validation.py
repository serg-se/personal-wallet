"""
Tests for cli options validation.
"""

import pytest

from personal_wallet.cli import main


class TestIndexValidation:
    @pytest.mark.parametrize("command", ["find", "update", "delete"])
    @pytest.mark.parametrize("valid_index", ["0", "1"])
    def test_valid_index(self, cli_runner, config, valid_index, command):
        result = cli_runner.invoke(main, [command, "-i", valid_index, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("command", ["find", "update", "delete"])
    @pytest.mark.parametrize("invalid_index", ["1.0", "1.3", "1...3", "", ".", "..", "..."])
    def test_invalid_index(self, cli_runner, config, invalid_index, command):
        result = cli_runner.invoke(main, [command, "-i", invalid_index, "--config", config])
        value_is_invalid_int(result)

    @pytest.mark.parametrize("command", ["find", "update", "delete"])
    @pytest.mark.parametrize("negative_index", ["-1", "-15"])
    def test_negative_index(self, cli_runner, config, negative_index, command):
        result = cli_runner.invoke(main, [command, "-i", negative_index, "--config", config])
        value_is_negative(result)

    @pytest.mark.parametrize("valid_index_range", ["0..1", "1..5"])
    def test_valid_index_range(self, cli_runner, config, valid_index_range):
        result = cli_runner.invoke(main, ["find", "-i", valid_index_range, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("invalid_index_range", ["10..1", "11..10"])
    def test_invalid_index_range(self, cli_runner, config, invalid_index_range):
        result = cli_runner.invoke(main, ["find", "-i", invalid_index_range, "--config", config])
        value_is_invalid_range(result)

    @pytest.mark.parametrize("negative_index_range", ["-1..2", "-3..-1"])
    def test_negative_index_range(self, cli_runner, config, negative_index_range):
        result = cli_runner.invoke(main, ["find", "-i", negative_index_range, "--config", config])
        value_is_negative(result)


class TestDateValidation:
    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize("valid_date", ["2024-05-04", "2024-01-30"])
    def test_valid_date(self, cli_runner, config, valid_date, command):
        result = cli_runner.invoke(main, [*command, "-d", valid_date, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize(
        "invalid_date",
        [
            "2024-01",
            "2024-01-32",
            "2024/01/01",
            "2024-01-01.2024-01-01",
            "2024-01-01...2024-01-01",
            "",
            ".",
            "..",
            "...",
        ],
    )
    def test_invalid_date(self, cli_runner, config, invalid_date, command):
        result = cli_runner.invoke(main, [*command, "-d", invalid_date, "--config", config])
        value_is_invalid_date_format(result)

    @pytest.mark.parametrize("valid_date_range", ["2024-03-15..2030-01-01"])
    def test_valid_date_range(self, cli_runner, config, valid_date_range):
        result = cli_runner.invoke(main, ["find", "-d", valid_date_range, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("invalid_date_range", ["2026-01-01..2024-01-01"])
    def test_invalid_date_range(self, cli_runner, config, invalid_date_range):
        result = cli_runner.invoke(main, ["find", "-d", invalid_date_range, "--config", config])
        value_is_invalid_range(result)


class TestAmountValidation:
    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize("valid_amount", ["0", "10"])
    def test_valid_amount(self, cli_runner, config, valid_amount, command):
        result = cli_runner.invoke(main, [*command, "-a", valid_amount, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize(
        "invalid_amount",
        ["10.0", "10.3", "100.300", "100...300", "", ".", "..", "..."],
    )
    def test_invalid_amount(self, cli_runner, config, invalid_amount, command):
        result = cli_runner.invoke(main, [*command, "-a", invalid_amount, "--config", config])
        value_is_invalid_int(result)

    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize("negative_amount", ["-1", "-15"])
    def test_negative_amount(self, cli_runner, config, negative_amount, command):
        result = cli_runner.invoke(main, [*command, "-a", negative_amount, "--config", config])
        value_is_negative(result)

    @pytest.mark.parametrize("valid_amount_range", ["100..300", "0..100"])
    def test_valid_amount_range(self, cli_runner, config, valid_amount_range):
        result = cli_runner.invoke(main, ["find", "-a", valid_amount_range, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("invalid_amount_range", ["300..100", "201..200"])
    def test_invalid_amount_range(self, cli_runner, config, invalid_amount_range):
        result = cli_runner.invoke(main, ["find", "-a", invalid_amount_range, "--config", config])
        value_is_invalid_range(result)

    @pytest.mark.parametrize("negative_range", ["-100..100", "-300..-100"])
    def test_negative_amount_range(self, cli_runner, config, negative_range):
        result = cli_runner.invoke(main, ["find", "-a", negative_range, "--config", config])
        value_is_negative(result)


class TestDescriptionValidation:
    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize(
        "valid_description",
        [
            "Salary",
            "Bought a book",
            "1368",
            "Salary fr%",
            "%a book",
            "%ary fr%",
            "Bought % book",
            "%%%% % %%%%",
            "%",
        ],
    )
    def test_valid_description(self, cli_runner, config, valid_description, command):
        result = cli_runner.invoke(main, [*command, "-s", valid_description, "--config", config])
        value_is_valid(result)


class TestCategoryValidation:
    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize("valid_category", ["income", "expenses"])
    def test_valid_category(self, cli_runner, config, valid_category, command):
        result = cli_runner.invoke(main, [*command, "-c", valid_category, "--config", config])
        value_is_valid(result)

    @pytest.mark.parametrize("command", [["find"], ["add"], ["update", "-i", "0"]])
    @pytest.mark.parametrize("invalid_category", ["spending", ""])
    def test_invalid_category(self, cli_runner, config, invalid_category, command):
        result = cli_runner.invoke(main, [*command, "-c", invalid_category, "--config", config])
        value_is_not_one_of(result)


def value_is_valid(result):
    assert "Error: Invalid value" not in result.output


def value_is_invalid_int(result):
    assert "Error: Invalid value" in result.output
    assert "is not a valid integer" in result.output


def value_is_negative(result):
    assert "Error: Invalid value" in result.output
    assert "is not in the range x>=0" in result.output


def value_is_invalid_range(result):
    assert "Error: Invalid value" in result.output
    assert "is greater than end" in result.output


def value_is_invalid_date_format(result):
    assert "Error: Invalid value" in result.output
    assert "does not match the format" in result.output


def value_is_not_one_of(result):
    assert "Error: Invalid value" in result.output
    assert "is not one of" in result.output
