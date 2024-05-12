"""
Tests for 'update' command.
"""

from personal_wallet.cli import main


def test_update(cli_runner, config):
    add_transaction(cli_runner, config)
    result = update_transaction(cli_runner, config)
    update_is_successful(result)
    transaction_is_updated(cli_runner, config)


INDEX = "0"
DATE = "2024-06-03"
AMOUNT = "257"
CATEGORY = "expenses"
DESCRIPTION = "Bought a book"

UPDATED_DATE = "2024-08-01"
UPDATED_AMOUNT = "780"
UPDATED_CATEGORY = "income"
UPDATED_DESCRIPTION = "Sold a book"


def add_transaction(cli_runner, config):
    cli_runner.invoke(
        main,
        ["add", "-d", DATE, "-a", AMOUNT, "-c", CATEGORY, "-s", DESCRIPTION, "--config", config],
    )


def update_transaction(cli_runner, config):
    result = cli_runner.invoke(
        main,
        [
            "update",
            "-i",
            INDEX,
            "-d",
            UPDATED_DATE,
            "-a",
            UPDATED_AMOUNT,
            "-c",
            UPDATED_CATEGORY,
            "-s",
            UPDATED_DESCRIPTION,
            "--config",
            config,
        ],
    )
    return result


def update_is_successful(result):
    assert result.exit_code == 0
    assert result.output == "Updated transaction successfully!\n"


def transaction_is_updated(cli_runner, config):
    result = cli_runner.invoke(main, ["find", "--config", config])
    assert UPDATED_DATE in result.output
    assert UPDATED_AMOUNT in result.output
    assert UPDATED_CATEGORY in result.output
    assert UPDATED_DESCRIPTION in result.output
