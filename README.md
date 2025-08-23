![Pantry photo](resources/pantry.jpg)

# 🥫 PantryDB

Remote MCP server to keep track of what's in your pantry.

The server is remote so it can be accessed on the go (e.g on mobile).
It supports a single user authenticated through GitHub OAuth.

PantryDB uses [CloudFlare's MCP & OAuth libraries](https://developers.cloudflare.com/agents/guides/remote-mcp-server/), and deployed on [CloudFlare Workers](https://developers.cloudflare.com/workers/).

## 📋 Table of Contents

- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Local](#local)
  - [Remote](#remote)
- [🥫 Examples](#-examples)
- [😎 Credits](#-credits)
- [🤝 License](#-license)

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or higher) and **npm** - for running the project and managing dependencies
- **OpenSSL** - for generating cookie encryption keys (`openssl rand -hex 32`)
- **GitHub account** - for OAuth authentication setup
- **Cloudflare account** - for Workers deployment and D1/KV services

### Installation 

Install dependencies:

```bash
npm install
```

Login to Wrangler:

```bash
npx wrangler login
```

### Local

_Run PantryDB locally and access it with MCP clients on the same machine._

#### GitHub OAuth

Create a new OAuth App for local development.

Navigate to [github.com/settings/developers](https://github.com/settings/developers) to create a new OAuth App with the following settings:

```
Application name: PantryDB (local)
Homepage URL: http://localhost:8788
Authorization callback URL: http://localhost:8788/callback
```

Note your Client ID and generate a Client secret. Add both to a `.dev.vars` file in the root of your project, which will be used to set secrets in local development:

```bash
touch .dev.vars
echo 'GITHUB_CLIENT_ID="your-client-id"' >> .dev.vars
echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .dev.vars
```

Then, add the username of the only GitHub account which will be allowed to use your PantryDB:

```bash
echo 'ALLOWED_GITHUB_USERNAME="your-username"' >> .dev.vars
```

#### Cookie Encryption

Set a cookie encryption key. Use any random string (e.g `openssl rand -hex 32`).

```bash
echo 'COOKIE_ENCRYPTION_KEY="your-cookie-encryption-key"' >> .dev.vars
```

#### KV namespace

Create the server's OAuth KV namespace: 

```bash
npx wrangler kv:namespace create "OAUTH_KV"
```

Then, update the Wrangler file (`wrangler.jsonc`) with the KV ID.

#### D1 Database

Create and initialize local d1 database.

```bash
npx wrangler d1 create pantrydb
npx wrangler d1 execute pantrydb --local --file=db/schema.sql
```

Then, update the Wrangler file (`wrangler.jsonc`) with the D1 database ID.

#### Run

Run the MCP server locally at `http://localhost:8788/sse`:

```bash
npx wrangler dev
```

#### Usage

Then connect to your local PantryDB at `http://localhost:8788/sse` with:

* [Claude Desktop](https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp) running on the same machine
* [MCP inspector](https://modelcontextprotocol.io/docs/tools/inspector):

```bash
npx @modelcontextprotocol/inspector
```

### Remote

_Run PantryDB remote and access from any MCP client._

#### GitHub OAuth

Create a new OAuth App for the remote server:

Navigate to [github.com/settings/developers](https://github.com/settings/developers) to create a new OAuth App with the following settings:

```
Application name: PantryDB (prod)
Homepage URL: https://pantrydb.<your-subdomain>.workers.dev
Authorization callback URL: https://pantrydb.<your-subdomain>.workers.dev/callback
```

Note your Client ID and generate a Client secret. Set secrets via Wrangler:

```bash
npx wrangler secret put GITHUB_CLIENT_ID
npx wrangler secret put GITHUB_CLIENT_SECRET
```

Then, set the username of the only GitHub account which will be allowed to use your PantryDB:

```bash
npx wrangler secret put ALLOWED_GITHUB_USERNAME
```

#### Cookie Encryption

Set a cookie encryption key. Use any random string (e.g `openssl rand -hex 32`).

```bash
npx wrangler secret put COOKIE_ENCRYPTION_KEY
```

#### KV namespace

Create the server's OAuth KV namespace: 

```bash
npx wrangler kv:namespace create "OAUTH_KV"
```

Then, update the Wrangler file (`wrangler.jsonc`) with the KV ID.

#### D1 Database

Create and initialize remote d1 database.

```bash
npx wrangler d1 create pantrydb
npx wrangler d1 execute pantrydb --remote --file=db/schema.sql
```

Then, update the Wrangler file (`wrangler.jsonc`) with the D1 database ID.

#### Deploy

Deploy the MCP server to make it available on your `workers.dev` domain:

```bash
npx wrangler deploy
```

#### Usage

Then connect to your remote PantryDB at `https://pantrydb.<your-subdomain>.workers.dev/sse` with:

* [Claude Desktop or Mobile](https://support.anthropic.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)
* any other [MCP client](https://modelcontextprotocol.io/docs/tutorials/use-remote-mcp-server)
* [MCP inspector](https://modelcontextprotocol.io/docs/tools/inspector):

```bash
npx @modelcontextprotocol/inspector
```

## 🥫 Examples

## 😎 Credits

* Pantry photo by <a href="https://unsplash.com/@anniespratt?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Annie Spratt</a> on <a href="https://unsplash.com/photos/clear-glass-jars-on-white-shelf-nLHnx2-_sK4?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
* Cloudflare "Build a Remote MCP Server" [examples](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#_top) & [template](https://github.com/cloudflare/ai/blob/main/demos/remote-mcp-github-oauth/)
* Cloudflare D1 [examples](https://developers.cloudflare.com/d1/get-started/#_top)

Special thanks to:

* [Raphael Van Hoffelen](https://github.com/dskart), OAuth mentor


## 🤝 License

[MIT license](LICENSE)