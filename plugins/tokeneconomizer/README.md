# TokenEconomizer

Makes coding agents cheaper to run in the repositories you work in often, without changing the
agent. It learns from the sessions you have already run in a repository:

- **Micro-skills** (off by default): short facts about how the repository works, stated at the
  start of each session once three sessions have confirmed them.
- **Tool pruning**: tools a repository's sessions never use are left out of the next sessions,
  through the agent's own settings. One command gives them back.
- **Loop guard**: a turn stuck in a failing loop gets a short redirect. It never stops a turn.

What it learns stays on your computer, in `~/.tokeneconomizer`. Its own model calls run through
your agent's CLI, on the same sign-in.

**Plugin:** `tokeneconomizer@tokeneconomizer` from `microsoft/TokenEconomizer`, for Claude Code,
Codex and Copilot CLI.

## Needs

- **Python 3.10 or newer** on `PATH`. Without it the plugin does nothing. Sessions in a Girard
  sandbox need it in the sandbox image too.

## Notes

- Girard installs it with each CLI's own plugin manager, so it is also active when you run the CLI
  in a terminal.
- Claude Code and Copilot CLI: run `/tokeneconomizer:toolprune refresh-catalog` once, and again
  after the CLI updates.
- Codex runs plugin hooks only once they are approved. Girard offers to approve them after
  installing; otherwise start `codex` once and choose **Trust all**, or use `/hooks`.
- Before removing it, run `/tokeneconomizer:toolprune restore` in each repository where it left
  tools out. `rm -rf ~/.tokeneconomizer` deletes what it learned.

Upstream: <https://github.com/microsoft/TokenEconomizer>
