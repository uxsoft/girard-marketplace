# GitHub

Repositories, issues, pull requests, Actions and code search on GitHub.

**Remote server:** `https://api.githubcopilot.com/mcp/`

## Secrets

Wisp keeps these in the system keychain.

- **Personal access token** (`Authorization`) — A fine-grained or classic GitHub token, sent as a Bearer token. Give it only the repositories and scopes the agents need. [Get one](https://github.com/settings/personal-access-tokens/new).

## Notes

GitHub's hosted server. It takes a personal access token; Wisp adds the `Bearer ` prefix for you.

Upstream: <https://github.com/github/github-mcp-server>
