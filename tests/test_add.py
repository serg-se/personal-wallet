"""
Tests for 'add' command.
"""

import datetime

from personal_wallet.cli import main


def test_add_transaction(cli_runner, config):
    date = "2024-05-03"
    amount = "153"
    category = "income"
    description = "Sold a book"

    result = add_transaction(cli_runner, config, date, amount, category, description)
    added_successfully(result)
    transaction_is_added(cli_runner, config, date, amount, category, description)


def test_add_income(cli_runner, config):
    date = "2024-05-03"
    amount = "153"
    category = "income"
    description = "Sold a book"

    result = add_transaction(cli_runner, config, date, amount, category, description)
    added_successfully(result)
    transaction_is_added(cli_runner, config, date, amount, category, description)


def test_add_expenses(cli_runner, config):
    date = "2024-06-03"
    amount = "257"
    category = "expenses"
    description = "Bought a book"

    result = add_transaction(cli_runner, config, date, amount, category, description)
    added_successfully(result)
    transaction_is_added(cli_runner, config, date, amount, category, description)


def test_add_with_default_date(cli_runner, config):
    today = datetime.date.today().strftime("%Y-%m-%d")

    date = None
    amount = "257"
    category = "expenses"
    description = "Bought a book"

    result = add_transaction(cli_runner, config, date, amount, category, description)
    added_successfully(result)
    transaction_is_added(cli_runner, config, today, amount, category, description)


def add_transaction(cli_runner, config, date, amount, category, description):
    result = cli_runner.invoke(
        main,
        ["add", "-d", date, "-a", amount, "-c", category, "-s", description, "--config", config],
    )
    assert result.exit_code == 0
    return result


def find_all(cli_runner, config):
    result = cli_runner.invoke(main, ["find", "--config", config])
    assert result.exit_code == 0
    return result


def added_successfully(result):
    assert result.exit_code == 0
    assert result.output == "Added transaction successfully!\n"


def transaction_is_added(cli_runner, config, date, amount, category, description):
    result = cli_runner.invoke(main, ["find", "--config", config])
    assert date in result.output
    assert amount in result.output
    assert category in result.output
    assert description in result.output
