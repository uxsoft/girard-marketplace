# Wisp Marketplace

Ready-made [MCP](https://modelcontextprotocol.io) server setups for [Wisp](https://github.com/uxsoft/wisp).
Wisp's **Settings → Marketplace** tab lists every server here. Click **Add**, fill in any keys it
asks for, and the server is given to Claude Code, Codex and Copilot CLI in your next session.

Wisp keeps a shallow clone of this repository in `~/.wisp/marketplace` and updates it when you
open the tab, so a server merged here shows up without a Wisp release.

## Servers

| | Server | Kind | Needs |
|---|---|---|---|
| <img src="mcp/github/icon.svg" width="20"> | [GitHub](mcp/github) | Remote | Personal access token |
| <img src="mcp/context7/icon.svg" width="20"> | [Context7](mcp/context7) | Remote | Optional API key |
| <img src="mcp/playwright/icon.svg" width="20"> | [Playwright](mcp/playwright) | Local | Node.js |
| <img src="mcp/sequential-thinking/icon.svg" width="20"> | [Sequential Thinking](mcp/sequential-thinking) | Local | Node.js |
| <img src="mcp/atlassian/icon.svg" width="20"> | [Atlassian](mcp/atlassian) | Remote | OAuth sign-in |
| <img src="mcp/linear/icon.svg" width="20"> | [Linear](mcp/linear) | Remote | OAuth sign-in |
| <img src="mcp/notion/icon.svg" width="20"> | [Notion](mcp/notion) | Remote | OAuth sign-in |
| <img src="mcp/sentry/icon.svg" width="20"> | [Sentry](mcp/sentry) | Remote | OAuth sign-in |
| <img src="mcp/figma/icon.svg" width="20"> | [Figma](mcp/figma) | Remote | OAuth sign-in |
| <img src="mcp/fetch/icon.svg" width="20"> | [Fetch](mcp/fetch) | Local | uv |
| <img src="mcp/brave-search/icon.svg" width="20"> | [Brave Search](mcp/brave-search) | Local | Node.js, API key |
| <img src="mcp/exa/icon.svg" width="20"> | [Exa](mcp/exa) | Remote | Optional API key |
| <img src="mcp/postgres/icon.svg" width="20"> | [Postgres](mcp/postgres) | Local | uv, connection URI |
| <img src="mcp/sqlite/icon.svg" width="20"> | [SQLite](mcp/sqlite) | Local | uv, database path |
| <img src="mcp/supabase/icon.svg" width="20"> | [Supabase](mcp/supabase) | Remote | OAuth sign-in |
| <img src="mcp/stripe/icon.svg" width="20"> | [Stripe](mcp/stripe) | Remote | OAuth sign-in |

## Adding a server

Each server is a folder under `mcp/`. The folder name is the server's id in Wisp, made of lowercase
letters, digits and `-`.

```
mcp/<id>/
  mcp.json    how Wisp starts or reaches the server
  icon.svg    a square icon, under 256 KiB, without scripts or embedded images
  README.md   what it does, what it needs, where to get keys
```

`mcp.json` follows [`schema/mcp.schema.json`](schema/mcp.schema.json):

```json
{
  "$schema": "../../schema/mcp.schema.json",
  "name": "Brave Search",
  "description": "Web, news, image and local search with the Brave Search API.",
  "homepage": "https://github.com/brave/brave-search-mcp-server",
  "kind": "stdio",
  "command": "npx",
  "args": ["-y", "@brave/brave-search-mcp-server"],
  "secrets": [
    {
      "name": "BRAVE_API_KEY",
      "label": "API key",
      "description": "A Brave Search API key.",
      "link": "https://api-dashboard.search.brave.com/app/keys"
    }
  ]
}
```

| Field | |
|---|---|
| `name`, `description` | Shown on the card. Keep the description to one sentence. |
| `homepage` | The card's **Docs** link. |
| `kind` | `stdio` runs `command` with `args` on the user's computer; `http` talks to `url` (streamable HTTP). |
| `oauth` | `http` only: the user signs in in the browser after adding it. |
| `oauth_client_name` | `http` only: the client name Wisp registers under, for servers that only accept known clients. |
| `inputs` | Plain values asked for when adding, each `{id, label, description?, placeholder?}`. `{id}` in `args` or `url` is replaced with the value. |
| `secrets` | Env vars (`stdio`) or headers (`http`), each `{name, label, description?, link?, prefix?, optional?}`. Wisp stores them in the system keychain. `prefix` goes before what the user types, e.g. `"Bearer "`. An `optional` secret left empty is left out. |

Check your entry with `python3 scripts/validate.py` before opening a pull request; CI runs it too.

Icons in the colored tiles use glyphs from [Simple Icons](https://simpleicons.org) (CC0). The brand
names and logos belong to their owners.
