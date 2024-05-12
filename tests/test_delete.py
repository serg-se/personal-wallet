"""
Tests for 'delete' command.
"""

from personal_wallet.cli import main


def test_delete_existing_transaction(cli_runner, config):
    add_transaction(cli_runner, config)
    result = delete_transaction(cli_runner, config)
    deletion_is_successful(result)
    no_transactions_found(cli_runner, config)


def test_delete_existing_transaction_twice(cli_runner, config):
    add_transaction(cli_runner, config)
    delete_transaction(cli_runner, config)
    result = delete_transaction(cli_runner, config)
    no_transactions_to_delete(result)


def test_delete_on_empty_wallet(cli_runner, config):
    result = delete_transaction(cli_runner, config)
    no_transactions_to_delete(result)


INDEX = "0"
DATE = "2024-06-03"
AMOUNT = "257"
CATEGORY = "expenses"
DESCRIPTION = "Bought a book"


def add_transaction(cli_runner, config):
    cli_runner.invoke(
        main,
        ["add", "-d", DATE, "-a", AMOUNT, "-c", CATEGORY, "-s", DESCRIPTION, "--config", config],
    )


def delete_transaction(cli_runner, config):
    result = cli_runner.invoke(
        main,
        ["delete", "-i", INDEX, "--config", config],
    )
    return result


def no_transactions_found(cli_runner, config):
    result = cli_runner.invoke(main, ["find", "--config", config])
    assert result.output == "\n"


def deletion_is_successful(result):
    assert result.exit_code == 0
    assert result.output == "Deleted transaction successfully!\n"


def no_transactions_to_delete(result):
    assert result.exit_code == 0
    assert result.output == "Wallet is empty, no transactions to delete.\n"
