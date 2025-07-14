# 🥫 PantryDB

MCP server to keep track of what's in your pantry.

## 

## Development

local run 
```
uv run mcp install server.py --with-editable . --env-file .env

uv run mcp run server.py
uv run mcp run --transport=streamable-http server.py
uv run --with mcp[cli] --with-editable . mcp run server.py
```

local dev
```
uv run mcp dev server.py --with-editable .
```
