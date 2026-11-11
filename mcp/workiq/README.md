# Work IQ

Microsoft 365 for your agents: mail, calendar, Teams chats and channels, OneDrive and SharePoint
files, people, Planner and more, through Microsoft's hosted Work IQ server. Agents can find and
summarize what's there, and act on it: draft and send mail, create meetings, post in Teams. The
agents ask before each tool call unless you mark the server trusted in Girard.

**Remote server:** `https://workiq.svc.cloud.microsoft/mcp`

## Needs

- A Microsoft 365 work account with a **Microsoft 365 Copilot** licence.
- **Tenant admin consent** for Work IQ. If signing in stops at *Need admin approval*, ask your
  tenant administrator to follow Microsoft's
  [Tenant Administrator Enablement Guide](https://github.com/microsoft/work-iq-mcp/blob/main/ADMIN-INSTRUCTIONS.md),
  which starts with the one-click consent URL
  `https://login.microsoftonline.com/<tenant>/adminconsent?client_id=ba081686-5d24-4bc6-a0d6-d034ecffed87`.
- A Girard version that signs in with pre-registered OAuth clients (`oauth_client`). Older
  versions report that the server doesn't let apps register themselves.

## Notes

Girard signs in with OAuth in your browser after you add it: open **Settings → MCP servers** and
click **Sign in**, then sign in with your work account. Microsoft Entra ID doesn't let apps register
themselves, so Girard signs in as Work IQ's own public client (`ba081686-…`), the one its Copilot
CLI plugin uses, and catches the redirect on `http://localhost:12798/`. Close other Work IQ sign-ins
(such as Copilot CLI's) while you sign in, since they use the same port. Girard keeps the tokens in
the system keychain and refreshes them; the agents never see them.

Work IQ is in public preview; its tools may change.

Upstream: <https://github.com/microsoft/work-iq-mcp>
