# Postgres

Query a PostgreSQL database, explain query plans and check its health (read-only).

**Runs locally:** `uvx postgres-mcp --access-mode=restricted`

## Secrets

Wisp keeps these in the system keychain.

- **Connection URI** (`DATABASE_URI`) — postgresql://user:password@host:5432/dbname. Kept in the keychain since it holds the password.

## Notes

Needs [uv](https://docs.astral.sh/uv/) (`uvx`). Runs in restricted (read-only) mode; edit the server in Settings and change `--access-mode=restricted` to `--access-mode=unrestricted` to allow writes.

Upstream: <https://github.com/crystaldba/postgres-mcp>
