import os
from difflib import SequenceMatcher
from typing import Dict, List, Optional

from pantrydb.database.abstract import PantryDatabase
from pantrydb.items import PantryItem

DEFAULT_SIMILARITY_THRESHOLD = "0.6"


class LocalPantryDatabase(PantryDatabase):
    """Local in-memory implementation of PantryDatabase."""

    @classmethod
    def from_env_vars(cls) -> "LocalPantryDatabase":
        """Create a LocalPantryDatabase instance from environment variables."""
        similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", DEFAULT_SIMILARITY_THRESHOLD))
        return cls(similarity_threshold=similarity_threshold)

    def __init__(self, similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD):
        self._items: Dict[str, PantryItem] = {}
        self.similarity_threshold = similarity_threshold

    def list_items(self) -> List[PantryItem]:
        """List all items in the database."""
        return list(self._items.values())

    def add_item(self, item: PantryItem) -> bool:
        """Add an item to the database."""
        try:
            self._items[item.uuid] = item
            return True
        except Exception:
            return False

    def delete_item(self, item_id: str) -> bool:
        """Delete an item from the database by its UUID."""
        try:
            if item_id in self._items:
                del self._items[item_id]
                return True
            return False
        except Exception:
            return False

    def search_item(self, name: str) -> Optional[PantryItem]:
        """Find an item in the database by its name using string similarity."""
        if not name or not self._items:
            return None

        search_name = name.lower()
        best_match = None
        best_ratio = 0.0

        for item in self._items.values():
            item_name = item.name.lower()

            # TODO check that this is the best way to do this
            similarity = SequenceMatcher(None, search_name, item_name).ratio()

            if similarity > best_ratio:
                best_ratio = similarity
                best_match = item

        return best_match if best_ratio >= self.similarity_threshold else None

    def decrease_item_amount(self, item_id: str, amount: int) -> bool:
        """Decrease the amount of an item in the database."""
        try:
            # Check if item exists
            if item_id not in self._items:
                return False
            
            current_item = self._items[item_id]
            remaining_amount = current_item.amount - amount
            
            # If consuming more than available, remove item entirely
            if remaining_amount <= 0:
                del self._items[item_id]
                return True
            
            # Update item with remaining amount
            updated_item = PantryItem(
                uuid=current_item.uuid,
                name=current_item.name,
                amount=remaining_amount
            )
            self._items[item_id] = updated_item
            return True
            
        except Exception:
            return False
