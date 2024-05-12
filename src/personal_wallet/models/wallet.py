import datetime
import re
from pathlib import Path

from personal_wallet.models.storage import CsvStorage
from personal_wallet.models.transaction import Transaction


class Wallet(CsvStorage):
    """Represents a wallet."""

    def __init__(self, file: Path):
        super().__init__(file)
        self.transactions = self.read_data()

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a new transaction to wallet and storage."""
        self.transactions.append(transaction)
        self.append_data(transaction)

    def get_balance(self) -> tuple[int, int]:
        """Return total income and total expenses."""
        income = 0
        expenses = 0
        for transaction in self.transactions:
            match transaction.category:
                case "income":
                    income += transaction.amount
                case "expenses":
                    expenses += transaction.amount
        return income, expenses

    def find_transactions(
        self,
        index: int | tuple[int, int] | None,
        date: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None,
        amount: int | tuple[int, int] | None,
        category: str | None,
        description: str | re.Pattern | None,
    ) -> list[dict]:
        """Filter out transactions not matching index, date, amount, category or description."""

        # Define search range.
        n = len(self.transactions)
        start, stop = 0, n
        if index is not None:
            if isinstance(index, tuple):
                start, stop = index[0], min(n, index[1] + 1)
            else:
                start, stop = index, min(n, index + 1)

        # Filtering out.
        matching_transactions = []
        for i in range(start, stop):
            transaction = self.transactions[i]
            if (
                category is not None
                and not transaction.match_category(category)
                or date is not None
                and (
                    isinstance(date, datetime.datetime)
                    and not transaction.match_date(date)
                    or isinstance(date, tuple)
                    and not transaction.match_date_range(date)
                )
                or amount is not None
                and (
                    isinstance(amount, int)
                    and not transaction.match_amount(amount)
                    or isinstance(amount, tuple)
                    and not transaction.match_amount_range(amount)
                )
                or description is not None
                and (
                    isinstance(description, str)
                    and not transaction.match_description(description)
                    or isinstance(description, re.Pattern)
                    and not transaction.match_description_pattern(description)
                )
            ):
                continue
            transaction = {"index": i, **transaction.as_dict()}
            matching_transactions.append(transaction)
        return matching_transactions

    def update_transaction(
        self,
        index: int,
        date: datetime.datetime | tuple[datetime.datetime, datetime.datetime] | None,
        amount: int | tuple[int, int] | None,
        category: str | None,
        description: str | re.Pattern | None,
    ) -> None:
        """Update transaction date, amount, category or description by its index."""
        if not self.transactions:
            raise IndexError("Wallet is empty, no transactions to update.")
        try:
            transaction = self.transactions[index]
            transaction.update(date, amount, category, description)
            self.write_data(self.transactions)
        except IndexError as e:
            raise LookupError(f"Error: Transaction with index {index} not found.") from e
        except IOError as e:
            raise IOError("Error: Error writing data after transaction deletion.") from e

    def delete_transaction(self, index: int) -> None:
        """Delete a transaction by its index"""
        if not self.transactions:
            raise IndexError("Wallet is empty, no transactions to delete.")
        try:
            self.transactions.pop(index)
            self.write_data(self.transactions)
        except IndexError as e:
            raise LookupError(f"Error: Transaction with index {index} not found.") from e
        except IOError as e:
            raise IOError("Error: Error writing data after transaction deletion.") from e
