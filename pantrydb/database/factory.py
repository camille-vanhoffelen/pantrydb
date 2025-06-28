# Factory module for creating database instances
import os
from typing import Union

from pantrydb.database.local import LocalPantryDatabase
from pantrydb.database.rds import RDSPantryDatabase


def create_database_from_env_vars() -> Union[LocalPantryDatabase, RDSPantryDatabase]:
    """
    Create a database instance based on the DATABASE_TYPE environment variable.
    
    Returns:
        LocalPantryDatabase if DATABASE_TYPE=local
        RDSPantryDatabase if DATABASE_TYPE=rds
        
    Raises:
        ValueError: If DATABASE_TYPE is not set or has an invalid value
    """
    database_type = os.getenv("DATABASE_TYPE", "").lower()
    
    if database_type == "local":
        return LocalPantryDatabase.from_env_vars()
    elif database_type == "rds":
        return RDSPantryDatabase.from_env_vars()
    else:
        raise ValueError(
            f"Invalid DATABASE_TYPE: '{database_type}'. "
            "Must be either 'local' or 'rds'"
        )
