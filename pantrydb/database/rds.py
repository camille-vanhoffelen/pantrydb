# RDS database implementation for pantrydb
from typing import List

from pantrydb.database.abstract import PantryDatabase
from pantrydb.items import PantryItem


# TODO implement RDS backend
class RDSPantryDatabase(PantryDatabase):
    """RDS implementation of the Database abstract class."""

    @classmethod
    def from_env_vars(cls) -> "RDSPantryDatabase":
        """Create a RDSPantryDatabase instance from environment variables."""
        raise NotImplementedError("RDS implementation not yet implemented")
    
    def __init__(self):
        """Initialize the RDS database connection."""
        # TODO: Implement RDS connection setup
        pass
    
    def list_items(self) -> List[PantryItem]:
        """List all items in the database."""
        raise NotImplementedError("RDS implementation not yet implemented")
    
    def add_item(self, item: PantryItem) -> bool:
        """Add an item to the database."""
        raise NotImplementedError("RDS implementation not yet implemented")
    
    def remove_item(self, item: PantryItem) -> bool:
        """Remove an item from the database."""
        raise NotImplementedError("RDS implementation not yet implemented")
