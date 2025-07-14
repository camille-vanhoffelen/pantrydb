# Item models for pantrydb
from pydantic import BaseModel, Field, field_validator


class PantryItem(BaseModel):
    """Pydantic model for pantry items."""
    
    name: str = Field(..., description="Name of the pantry item, in simple and singular form, e.g 'banana' or 'yogurt'")
    # TODO consider changing amount to units, so it's more integer like (e.g for butter?)
    amount: int = Field(..., description="Amount of the item")

    @field_validator('name')
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Normalize the name field to lowercase and stripped."""
        return v.lower().strip()
