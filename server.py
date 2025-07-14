import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import structlog
from mcp.server.fastmcp import FastMCP
from structlog.contextvars import bound_contextvars
import os

from pantrydb.database import create_database_from_env_vars
from pantrydb.items import PantryItem

# Local MCP servers should not log messages to stdout (standard out), 
# as this will interfere with protocol operation.
# TODO local vs deployed log configs, for structured logs and stdout
structlog.configure(logger_factory=structlog.PrintLoggerFactory(sys.stderr))

logger = structlog.get_logger()



# connection pool, re-used across calls
db = create_database_from_env_vars()
# TODO OAuth
mcp = FastMCP("PantryDB", stateless_http=True, json_response=True)
# mcp = FastMCP("PantryDB", lifespan=app_lifespan, stateless_http=True, json_response=True)


@mcp.tool()
def list_items() -> list[PantryItem]:
    """List items in the pantry database"""
    logger.info("list_items tool called")
    return db.list_items()


@mcp.tool()
def add_item(item: PantryItem) -> bool:
    """Add an item to the pantry database"""
    with bound_contextvars(**item.model_dump()):
        logger.info("add_item tool called")
        return db.add_item(item=item)


@mcp.tool()
def remove_item(item: PantryItem) -> bool:
    """Remove an item from pantry database"""
    with bound_contextvars(**item.model_dump()):
        logger.info("remove_item tool called")
        return db.remove_item(item=item)

if __name__ == "__main__":
    # TODO protocol
    # TODO better args and validation
    mcp.run(transport=os.getenv("TRANSPORT"))