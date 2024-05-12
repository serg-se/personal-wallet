import datetime
import functools
import re

import click
import tabulate

from personal_wallet.cli_types import (
    DateTimeOrDateTimeRange,
    NON_NEG_INT_OR_INT_RANGE,
    STRING_OR_PATTERN,
)
from personal_wallet.config import configure
from personal_wallet.constants import DEFAULT_CFG, PROJECT_DIR
from personal_wallet.models.transaction import Transaction
from personal_wallet.models.wallet import Wallet


def common_options(func):
    @click.option(
        "--config",
        type=click.Path(dir_okay=False),
        default=DEFAULT_CFG,
        callback=configure,
        is_eager=True,
        expose_value=False,
        help="Read option defaults from the specified INI file",
        show_default=True,
    )
    @click.option(
        "--data-path",
        default="data",
        help="Directory for storing transaction data",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.command("balance", help="Shows the current balance, income and expenses.")
@common_options
def balance(data_path: str):
    """Shows the current balance, income and expenses."""
    csvfile = PROJECT_DIR / data_path / "transactions.csv"

    wallet = Wallet(file=csvfile)
    income, expenses = wallet.get_balance()

    click.echo(f"Current balance: {income - expenses}")
    click.echo(f"Income: {income}")
    click.echo(f"Expenses: {expenses}")


@click.command("add", help="Add a new transaction to the wallet.")
@click.option(
    "-d",
    "--date",
    help="Transaction date in YYYY-MM-DD format.",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(datetime.date.today()),
)
@click.option(
    "-a",
    "--amount",
    type=click.IntRange(min=0),
    required=True,
    help="Transaction amount as non-negative integer.",
)
@click.option(
    "-c",
    "--category",
    type=click.Choice(["income", "expenses"]),
    required=True,
    help="Transaction category (income/expenses).",
)
@click.option(
    "-s",
    "--description",
    help="Transaction description.",
)
@common_options
def add(
    data_path: str,
    date: datetime.datetime,
    amount: int,
    category: str,
    description: str | None,
):
    """Add a new transaction to the wallet."""
    csvfile = PROJECT_DIR / data_path / "transactions.csv"

    wallet = Wallet(file=csvfile)
    transaction = Transaction(date=date, amount=amount, category=category, description=description)
    wallet.add_transaction(transaction)

    click.echo("Added transaction successfully!")


@click.command(name="find", help="Search transactions by date, amount, category or description.")
@click.option(
    "-i",
    "--index",
    type=NON_NEG_INT_OR_INT_RANGE,
    help="Index of transaction. Single non-negative integer or `from..to` range "
    "(e.g., `1` or `1..15`)",
)
@click.option(
    "-d",
    "--date",
    type=DateTimeOrDateTimeRange(formats=["%Y-%m-%d"]),
    help="Transaction date. Single date in YYYY-MM-DD format or `from..to` range "
    "(e.g., `2024-05-08` or `2024-05-01..2024-05-09`)",
)
@click.option(
    "-a",
    "--amount",
    type=NON_NEG_INT_OR_INT_RANGE,
    help="Transaction amount. Single non-negative integer or `from..to` range "
    "(e.g., `100` or `50..200`)",
)
@click.option(
    "-c",
    "--category",
    type=click.Choice(["income", "expenses"]),
    help="Transaction category (income/expenses).",
)
@click.option(
    "-s",
    "--description",
    type=STRING_OR_PATTERN,
    help="Transaction description. Exact description or pattern using % "
    "(e.g., `Salary` or `Sa%`). The % wildcard represents any number of characters.",
)
@common_options
def find(
    index: int,
    data_path: str,
    date: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None,
    amount: int | tuple[int, int] | None,
    category: str | None,
    description: str | re.Pattern | None,
):
    """Search transactions by date, amount, category or description."""
    csvfile = PROJECT_DIR / data_path / "transactions.csv"

    wallet = Wallet(file=csvfile)
    transactions = wallet.find_transactions(
        index=index, date=date, amount=amount, category=category, description=description
    )
    # transactions = (t.as_dict() for t in transactions)
    click.echo(tabulate.tabulate(transactions, headers="keys"))


@click.command(
    name="update", help="Update transaction date, amount, category or description by its index."
)
@click.option(
    "-i",
    "--index",
    type=click.IntRange(min=0),
    required=True,
    help="Index of transaction.",
)
@click.option(
    "-d",
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Transaction date in YYYY-MM-DD format.",
)
@click.option(
    "-a",
    "--amount",
    type=click.IntRange(min=0),
    help="Transaction amount as non-negative integer.",
)
@click.option(
    "-c",
    "--category",
    type=click.Choice(["income", "expenses"]),
    help="Transaction category (income/expenses).",
)
@click.option(
    "-s",
    "--description",
    type=click.STRING,
    help="Transaction description.",
)
@common_options
def update(
    data_path: str,
    index: int,
    date: datetime.datetime | None,
    amount: int | None,
    category: str | None,
    description: str | None,
):
    """Update transaction date, amount, category or description by its index."""
    csvfile = PROJECT_DIR / data_path / "transactions.csv"

    wallet = Wallet(file=csvfile)
    try:
        wallet.update_transaction(
            index=index, date=date, amount=amount, category=category, description=description
        )
        click.echo("Updated transaction successfully!")
    except Exception as e:
        error_message = str(e)
        click.echo(error_message)


@click.command(name="delete", help="Delete a transaction by its index.")
@click.option(
    "-i",
    "--index",
    type=click.IntRange(min=0),
    required=True,
    help="Index of transaction.",
)
@common_options
def delete(data_path: str, index: int):
    """Delete a transaction by its index."""
    csvfile = PROJECT_DIR / data_path / "transactions.csv"

    wallet = Wallet(file=csvfile)
    try:
        wallet.delete_transaction(index=index)
        click.echo("Deleted transaction successfully!")
    except Exception as e:
        error_message = str(e)
        click.echo(error_message)
