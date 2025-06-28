# Item models for pantrydb
from uuid import uuid4

from pydantic import BaseModel, Field


class PantryItem(BaseModel):
    """Pydantic model for pantry items."""
    
    uuid: str = Field(default_factory=lambda: str(uuid4()), description="Unique identifier for the item")
    name: str = Field(..., description="Name of the pantry item")
    amount: int = Field(..., description="Amount of the item")
