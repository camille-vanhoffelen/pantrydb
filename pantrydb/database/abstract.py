# Database module for pantrydb
from abc import ABC, abstractmethod
from typing import List

from pantrydb.items import PantryItem


class PantryDatabase(ABC):
    """Abstract base class for database operations."""

    @abstractmethod
    def list_items(self) -> List[PantryItem]:
        """List all items in the database."""
        pass

    @abstractmethod
    def add_item(self, item: PantryItem) -> bool:
        """Add an item to the database."""
        pass

    @abstractmethod
    def remove_item(self, item: PantryItem) -> bool:
        """Remove an item from the database."""
        pass
