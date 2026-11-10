# Girard Marketplace

Ready-made [MCP](https://modelcontextprotocol.io) server setups and agent CLI plugins for
[Girard](https://github.com/uxsoft/girard). Girard's **Settings → Marketplace** tab lists every
entry here, under **Servers** and **Plugins**. Click **Add**, fill in any keys a server asks for,
and the server is given to Claude Code, Codex and Copilot CLI in your next session. A plugin is
installed with each CLI's own plugin manager.

Girard keeps a shallow clone of this repository in `~/.girard/marketplace` and updates it when you
open the tab, so an entry merged here shows up without a Girard release.

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

## Plugins

| | Plugin | For | Needs |
|---|---|---|---|
| <img src="plugins/tokeneconomizer/icon.svg" width="20"> | [TokenEconomizer](plugins/tokeneconomizer) | Claude Code, Codex, Copilot CLI | Python 3.10+ |

## Adding a server

Each server is a folder under `mcp/`. The folder name is the server's id in Girard, made of lowercase
letters, digits and `-`.

```
mcp/<id>/
  mcp.json    how Girard starts or reaches the server
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
| `oauth_client_name` | `http` only: the client name Girard registers under, for servers that only accept known clients. |
| `inputs` | Plain values asked for when adding, each `{id, label, description?, placeholder?}`. `{id}` in `args` or `url` is replaced with the value. |
| `secrets` | Env vars (`stdio`) or headers (`http`), each `{name, label, description?, link?, prefix?, optional?}`. Girard stores them in the system keychain. `prefix` goes before what the user types, e.g. `"Bearer "`. An `optional` secret left empty is left out. |

## Adding a plugin

A plugin is one that Claude Code, Codex or Copilot CLI installs itself, from a plugin marketplace
(`.claude-plugin/marketplace.json`) in a Git repository. Girard runs each CLI's
`plugin marketplace add <source>` and `plugin install <plugin>@<marketplace>`, so the plugin is
installed for that CLI globally, also outside Girard. Each plugin is a folder under `plugins/`,
named like a server's:

```
plugins/<id>/
  plugin.json  where Girard installs it from, and for which CLIs
  icon.svg     as for servers
  README.md    what it does, what it needs, anything to do after installing
```

`plugin.json` follows [`schema/plugin.schema.json`](schema/plugin.schema.json):

```json
{
  "$schema": "../../schema/plugin.schema.json",
  "name": "TokenEconomizer",
  "description": "Cuts agent cost in repositories you work in often.",
  "homepage": "https://github.com/microsoft/TokenEconomizer",
  "source": "microsoft/TokenEconomizer",
  "harnesses": ["claude-code", "codex", "copilot-cli"],
  "requires": ["python3"],
  "notes": { "codex": "Approve its hooks; they run from your next session." }
}
```

| Field | |
|---|---|
| `name`, `description` | Shown on the card. Keep the description to one sentence. |
| `homepage` | The card's **Docs** link. |
| `source` | The marketplace: a GitHub `owner/repo` or an `https://` Git URL. Its default branch is installed, and **Update** follows it. |
| `marketplace` | The marketplace's `name` in the source's `marketplace.json`. Defaults to the folder name. |
| `plugin` | The plugin's name in that marketplace. Defaults to the folder name. |
| `harnesses` | The CLIs it supports: `claude-code`, `codex`, `copilot-cli`. |
| `requires` | Commands it needs on `PATH`, such as `python3`. Girard warns when one is missing. |
| `notes` | Per CLI, a sentence or two shown after installing, for steps the user has to take. |

Plugins run code on the user's computer, in hooks the CLIs start. Link the source in the README and
say what its hooks do.

## Checking an entry

Check your entry with `python3 scripts/validate.py` before opening a pull request; CI runs it too.

Icons in the colored tiles use glyphs from [Simple Icons](https://simpleicons.org) (CC0). The brand
names and logos belong to their owners.
