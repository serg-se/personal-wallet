import csv
from abc import ABC, abstractmethod
from pathlib import Path

from personal_wallet.models.transaction import Transaction


class Storage(ABC):
    """Abstract base class for storage."""

    def __init__(self, file: Path):
        self.file = file

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_data(self, transactions):
        pass

    @abstractmethod
    def append_data(self, transaction):
        pass


class CsvStorage(Storage):
    """Concrete class for CSV storage."""

    def read_data(self) -> [Transaction]:
        """Read csv file and return a list of transactions."""
        try:
            with open(self.file, "r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                transactions = []
                for row in reader:
                    transaction = Transaction.from_csv_row(row)
                    transactions.append(transaction)
                return transactions
        except FileNotFoundError:
            return []

    def write_data(self, transactions: [Transaction]) -> None:
        """Write all the transactions to csv file."""

        # Get header names.
        fieldnames = Transaction.fieldnames()

        self.file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.file, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for transaction in transactions:
                writer.writerow(transaction.as_dict())

    def append_data(self, transaction: Transaction) -> None:
        """Append a new transaction to csv file."""

        # Get header names.
        fieldnames = Transaction.fieldnames()

        self.file.parent.mkdir(parents=True, exist_ok=True)

        # Create file if it's not exist and write headers.
        if not self.file.exists():
            with open(self.file, "w", encoding="utf-8", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

        # Open for appending (avoids rewriting header).
        with open(self.file, "a", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(transaction.as_dict())
