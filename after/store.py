import datetime
from typing import List

from models import Item


class DataStore:
    """Manages the in-memory collection of items."""

    def __init__(self):
        self._items: List[Item] = []

    MAX_VALUE_LENGTH = 200

    def add_item(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Item value cannot be empty.")
        if len(value) > self.MAX_VALUE_LENGTH:
            raise ValueError(f"Item value cannot exceed {self.MAX_VALUE_LENGTH} characters.")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item = Item(id=len(self._items) + 1, value=value.strip(), created_at=timestamp)
        self._items.append(item)
        print("Added.")

    def display_items(self) -> None:
        if not self._items:
            print("No items to show.")
            return
        for item in self._items:
            print(f"Item: {item.id} - {item.value} at {item.created_at}")

    def load_items(self, items: List[Item]) -> None:
        """Populate the store from a pre-loaded list (e.g. restored from disk)."""
        self._items = list(items)

    @property
    def items(self) -> List[Item]:
        return list(self._items)
