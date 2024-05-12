"""
Tests for 'balance' command.
"""

from personal_wallet.cli import main


def test_balance_is_zero(cli_runner, config):
    balance_is_correct(cli_runner, config, 0, 0)


def test_balance_is_increased(cli_runner, config):
    total_income = 0
    total_expenses = 0
    for amount in [50, 100, 1500]:
        total_income += amount

        increase_balance(cli_runner, config, amount)
        balance_is_correct(cli_runner, config, total_income, total_expenses)


def test_balance_is_decreased(cli_runner, config):
    total_income = 0
    total_expenses = 0
    for amount in [50, 100, 1500]:
        total_expenses += amount

        decrease_balance(cli_runner, config, amount)
        balance_is_correct(cli_runner, config, total_income, total_expenses)


def test_increased_and_decreased(cli_runner, config):
    total_income = 0
    total_expenses = 0
    for income, expenses in zip([50, 100, 1500], [1500, 100, 50]):
        total_income += income
        total_expenses += expenses

        increase_balance(cli_runner, config, income)
        decrease_balance(cli_runner, config, expenses)
        balance_is_correct(cli_runner, config, total_income, total_expenses)


def increase_balance(cli_runner, config, amount):
    cli_runner.invoke(main, ["add", "-a", amount, "-c", "income", "--config", config])


def decrease_balance(cli_runner, config, amount):
    cli_runner.invoke(main, ["add", "-a", amount, "-c", "expenses", "--config", config])


def balance_is_correct(cli_runner, config, income, expenses):
    result = cli_runner.invoke(main, ["balance", "--config", config])
    assert result.exit_code == 0
    assert (
        result.output
        == f"Current balance: {income - expenses}\nIncome: {income}\nExpenses: {expenses}\n"
    )
