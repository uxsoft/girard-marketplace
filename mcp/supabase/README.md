# Supabase

Manage Supabase projects: tables, SQL, migrations, edge functions and logs.

**Remote server:** `https://mcp.supabase.com/mcp`

## Notes

Wisp signs in with OAuth in your browser after you add it: open **Settings → MCP servers** and click **Sign in**. Wisp keeps the tokens in the system keychain and refreshes them; the agents never see them.

To limit it to one project or to read-only queries, edit the URL in Settings: add `?project_ref=<id>` and/or `read_only=true`.

Upstream: <https://supabase.com/docs/guides/getting-started/mcp>
