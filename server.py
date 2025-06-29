from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

from pantrydb.database import PantryDatabase, create_database_from_env_vars
from pantrydb.items import PantryItem


@dataclass
class AppContext:
    db: PantryDatabase


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # TODO ?
    # db = await PantryDatabase.connect()
    db = create_database_from_env_vars()
    try:
        yield AppContext(db=db)
    finally:
        # Cleanup on shutdown
        # TODO ?
        await db.disconnect()


mcp = FastMCP("PantryDB", lifespan=app_lifespan)


@mcp.tool()
def list_items() -> list[PantryItem]:
    """Tool that uses initialized resources"""
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context.db
    return db.list_items()


@mcp.tool()
def add_item(name: str, amount: int) -> bool:
    """Add an item to the pantry database"""
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context.db
    item = PantryItem(name=name, amount=amount)
    return db.add_item(item=item)


@mcp.tool()
def remove_item(name: str, amount: int) -> bool:
    """Remove an item from pantry database"""
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context.db
    item = PantryItem(name=name, amount=amount)
    return db.remove_item(item=item)
