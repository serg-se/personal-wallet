import datetime
import re


class Transaction:
    """Represents a financial transaction."""

    def __init__(
        self,
        date: datetime.datetime | None,
        amount: int,
        category: str,
        description: str | None,
    ):
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description

    def as_dict(self) -> dict:
        """Return a dictionary representation, ready to be written to csv."""
        return {
            "date": str(self.date.date()),
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
        }

    @staticmethod
    def fieldnames() -> list[str]:
        return ["date", "amount", "category", "description"]

    @classmethod
    def from_csv_row(cls, line) -> "Transaction":
        """Create transaction from csv row."""
        date = datetime.datetime.strptime(line["date"], "%Y-%m-%d")
        amount = int(line["amount"])
        category = line["category"]
        description = line["description"]
        return cls(date, amount, category, description)

    def update(
        self,
        date: datetime.datetime | None,
        amount: int | None,
        category: str | None,
        description: str | None,
    ) -> None:
        """Update transaction date, amount, category or description."""
        if date is not None:
            self.date = date
        if amount is not None:
            self.amount = amount
        if category is not None:
            self.category = category
        if description is not None:
            self.description = description

    def match_category(self, category) -> bool:
        return self.category == category

    def match_date(self, date: datetime.datetime) -> bool:
        return date == self.date

    def match_date_range(self, date_range: [datetime.datetime, datetime.datetime]) -> bool:
        return date_range[0] <= self.date <= date_range[1]

    def match_amount(self, amount: int) -> bool:
        return self.amount == amount

    def match_amount_range(self, amount_range: [int, int]) -> bool:
        return amount_range[0] <= self.amount <= amount_range[1]

    def match_description(self, description: str) -> bool:
        return self.description == description

    def match_description_pattern(self, description_pattern: re.Pattern) -> bool:
        return re.search(description_pattern, self.description) is not None
