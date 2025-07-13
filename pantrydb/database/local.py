from typing import Dict, List

from pantrydb.database.abstract import PantryDatabase
from pantrydb.items import PantryItem


class LocalPantryDatabase(PantryDatabase):
    """Local in-memory implementation of PantryDatabase."""

    @classmethod
    def from_env_vars(cls) -> "LocalPantryDatabase":
        """Create a LocalPantryDatabase instance from environment variables."""
        return cls()

    def __init__(self):
        self._items: Dict[str, PantryItem] = {}

    def list_items(self) -> List[PantryItem]:
        """List all items in the database."""
        return list(self._items.values())

    def add_item(self, item: PantryItem) -> bool:
        """Add an item to the database."""
        try:
            if item.name not in self._items:
                self._items[item.name] = item
                return True
            else:
                current_item = self._items[item.name]
                new_amount = current_item.amount + item.amount

                updated_item = PantryItem(name=current_item.name, amount=new_amount)
                self._items[item.name] = updated_item
                return True

        except Exception:
            return False

    def remove_item(self, item: PantryItem) -> bool:
        try:
            if item.name not in self._items:
                return False

            current_item = self._items[item.name]

            remaining_amount = current_item.amount - item.amount

            # If consuming more than available, fail
            if item.amount > current_item.amount:
                return False

            # If consuming all, remove item entirely
            if remaining_amount == 0:
                del self._items[item.name]
                return True

            # If consuming some, update item amount
            updated_item = PantryItem(name=current_item.name, amount=remaining_amount)
            self._items[item.name] = updated_item
            return True

        except Exception:
            return False
