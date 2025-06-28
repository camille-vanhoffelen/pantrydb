# Database module for pantrydb
from abc import ABC, abstractmethod
from typing import List, Optional

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
    def delete_item(self, item_id: str) -> bool:
        """Delete an item from the database by its ID."""
        pass
    
    @abstractmethod
    def search_item(self, name: str) -> Optional[PantryItem]:
        """Find an item in the database by its name."""
        pass
    
    @abstractmethod
    def decrease_item_amount(self, item_id: str, amount: int) -> bool:
        """Decrease the amount of an item in the database."""
        pass 