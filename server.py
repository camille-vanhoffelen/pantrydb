import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import structlog
from mcp.server.fastmcp import FastMCP
from structlog.contextvars import bound_contextvars

from pantrydb.database import PantryDatabase, create_database_from_env_vars
from pantrydb.items import PantryItem

# Local MCP servers should not log messages to stdout (standard out), 
# as this will interfere with protocol operation.
# TODO local vs deployed log configs, for structured logs and stdout
structlog.configure(logger_factory=structlog.PrintLoggerFactory(sys.stderr))

logger = structlog.get_logger()


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
        # await db.disconnect()
        ...


# TODO OAuth
mcp = FastMCP("PantryDB", lifespan=app_lifespan)


@mcp.tool()
def list_items() -> list[PantryItem]:
    """List items in the pantry database"""
    logger.info("list_items tool called")
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context.db
    return db.list_items()


@mcp.tool()
def add_item(item: PantryItem) -> bool:
    """Add an item to the pantry database"""
    # TODO fix
    with bound_contextvars(**item.model_dump()):
    # with bound_contextvars(name=item.name, amount=item.amount):
        logger.info("add_item tool called")
        ctx = mcp.get_context()
        db = ctx.request_context.lifespan_context.db
        return db.add_item(item=item)


@mcp.tool()
def remove_item(item: PantryItem) -> bool:
    """Remove an item from pantry database"""
    # TODO fix
    # with bound_contextvars(name=item.name, amount=item.amount):
    logger.info("remove_item tool called")
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context.db
    return db.remove_item(item=item)

if __name__ == "__main__":
    # TODO protocol
    mcp.run()