from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

from pantrydb.database import PantryDatabase

mcp = FastMCP("Demo")


@dataclass
class AppContext:
    db: PantryDatabase


# TODO replace these tools with database tools
# TODO test local db with inspector
# TODO test local db in claude desktop
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
