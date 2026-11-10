#!/usr/bin/env python3
"""Checks every mcp/<id>/ and plugins/<id>/ entry the way Girard reads it. Standard library only.

Usage: python3 scripts/validate.py [repo root]
"""

import json
import re
import sys
from pathlib import Path

ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
INPUT_ID = re.compile(r"^[a-z][a-z0-9_]*$")
PLACEHOLDER = re.compile(r"\{([^{}]*)\}")
KNOWN = {"$schema", "name", "description", "homepage", "kind", "command", "args", "url",
         "oauth", "oauth_client_name", "inputs", "secrets"}
MAX_ICON = 256 * 1024
PLUGIN_KNOWN = {"$schema", "name", "description", "homepage", "source", "marketplace", "plugin",
                "harnesses", "requires", "notes"}
HARNESSES = ("claude-code", "codex", "copilot-cli")
SOURCE = re.compile(r"^([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+|https://\S+)$")
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
COMMAND = re.compile(r"^[A-Za-z0-9_.+-]+$")


def check(folder: Path) -> list[str]:
    errors = []
    if not ID.match(folder.name):
        errors.append("the folder name must be lowercase letters, digits and '-'")
    try:
        entry = json.loads((folder / "mcp.json").read_text())
    except FileNotFoundError:
        return errors + ["mcp.json is missing"]
    except json.JSONDecodeError as e:
        return errors + [f"mcp.json is not valid JSON: {e}"]
    if not isinstance(entry, dict):
        return errors + ["mcp.json must be an object"]

    for key in entry.keys() - KNOWN:
        errors.append(f"unknown field {key!r}")
    for key in ("name", "description"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            errors.append(f"{key!r} must be a non-empty string")
    kind = entry.get("kind")
    if kind not in ("stdio", "http"):
        errors.append("'kind' must be 'stdio' or 'http'")
    args = entry.get("args", [])
    if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
        errors.append("'args' must be a list of strings")
        args = []
    url = entry.get("url", "")
    if kind == "stdio":
        if not isinstance(entry.get("command"), str) or not entry["command"].strip():
            errors.append("a stdio server needs a 'command'")
        for key in ("url", "oauth", "oauth_client_name"):
            if entry.get(key):
                errors.append(f"{key!r} is for http servers only")
    if kind == "http":
        if not isinstance(url, str) or not re.match(r"^https?://", url):
            errors.append("an http server needs a 'url' starting with http:// or https://")
            url = ""
        if entry.get("command") or args:
            errors.append("'command' and 'args' are for stdio servers only")
    if "oauth" in entry and not isinstance(entry["oauth"], bool):
        errors.append("'oauth' must be true or false")
    if entry.get("oauth_client_name") is not None and not entry.get("oauth"):
        errors.append("'oauth_client_name' needs 'oauth': true")

    inputs = entry.get("inputs", [])
    input_ids = set()
    for i in inputs if isinstance(inputs, list) else []:
        iid = i.get("id", "") if isinstance(i, dict) else ""
        if not INPUT_ID.match(iid):
            errors.append(f"input id {iid!r} must be lowercase letters, digits and '_'")
        elif iid in input_ids:
            errors.append(f"input {iid!r} is listed twice")
        input_ids.add(iid)
        if not isinstance(i, dict) or not str(i.get("label", "")).strip():
            errors.append(f"input {iid!r} needs a 'label'")
    used = set(PLACEHOLDER.findall(" ".join([*args, url or ""])))
    for name in used - input_ids:
        errors.append(f"{{{name}}} is used but no input declares it")
    for name in input_ids - used:
        errors.append(f"input {name!r} is never used in 'args' or 'url'")

    secrets = entry.get("secrets", [])
    names = set()
    for s in secrets if isinstance(secrets, list) else []:
        name = s.get("name", "") if isinstance(s, dict) else ""
        if not name.strip():
            errors.append("every secret needs a 'name'")
        elif name.lower() in names:
            errors.append(f"secret {name!r} is listed twice")
        names.add(name.lower())
        if not isinstance(s, dict) or not str(s.get("label", "")).strip():
            errors.append(f"secret {name!r} needs a 'label'")
    if entry.get("oauth") and "authorization" in names:
        errors.append("an OAuth server can't also take an Authorization secret")

    return errors + check_files(folder)


def check_files(folder: Path) -> list[str]:
    """The icon and README every entry has."""
    errors = []
    icon = folder / "icon.svg"
    if not icon.is_file():
        errors.append("icon.svg is missing")
    else:
        data = icon.read_bytes()
        if len(data) > MAX_ICON:
            errors.append("icon.svg must be under 256 KiB")
        if b"<svg" not in data[:512]:
            errors.append("icon.svg doesn't look like an SVG")
        if re.search(rb"<(script|image|foreignObject)\b", data):
            errors.append("icon.svg must not contain scripts, images or foreign objects")
    if not (folder / "README.md").is_file():
        errors.append("README.md is missing")
    return errors


def check_plugin(folder: Path) -> list[str]:
    errors = []
    if not ID.match(folder.name):
        errors.append("the folder name must be lowercase letters, digits and '-'")
    try:
        entry = json.loads((folder / "plugin.json").read_text())
    except FileNotFoundError:
        return errors + ["plugin.json is missing"]
    except json.JSONDecodeError as e:
        return errors + [f"plugin.json is not valid JSON: {e}"]
    if not isinstance(entry, dict):
        return errors + ["plugin.json must be an object"]

    for key in entry.keys() - PLUGIN_KNOWN:
        errors.append(f"unknown field {key!r}")
    for key in ("name", "description"):
        if not isinstance(entry.get(key), str) or not entry[key].strip():
            errors.append(f"{key!r} must be a non-empty string")
    source = entry.get("source")
    if not isinstance(source, str) or not SOURCE.match(source):
        errors.append("'source' must be a GitHub owner/repo or an https:// Git URL")
    for key in ("marketplace", "plugin"):
        if key in entry and (not isinstance(entry[key], str) or not NAME.match(entry[key])):
            errors.append(f"{key!r} must be a name of letters, digits, '.', '_' and '-'")
    harnesses = entry.get("harnesses")
    if not isinstance(harnesses, list) or not harnesses:
        errors.append(f"'harnesses' must list one or more of {', '.join(HARNESSES)}")
        harnesses = []
    for h in harnesses:
        if h not in HARNESSES:
            errors.append(f"unknown harness {h!r}; use {', '.join(HARNESSES)}")
    if len(set(map(str, harnesses))) != len(harnesses):
        errors.append("a harness is listed twice")
    requires = entry.get("requires", [])
    if not isinstance(requires, list) or not all(
        isinstance(r, str) and COMMAND.match(r) for r in requires
    ):
        errors.append("'requires' must be a list of command names")
    notes = entry.get("notes", {})
    if not isinstance(notes, dict):
        errors.append("'notes' must be an object keyed by harness")
        notes = {}
    for h, note in notes.items():
        if h not in harnesses:
            errors.append(f"a note for {h!r}, which 'harnesses' doesn't list")
        if not isinstance(note, str) or not note.strip():
            errors.append(f"the note for {h!r} must be a non-empty string")
    return errors + check_files(folder)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    failed = 0
    counts = []
    for kind, check_one, noun in (("mcp", check, "servers"), ("plugins", check_plugin, "plugins")):
        top = root / kind
        folders = sorted(p for p in top.iterdir() if p.is_dir()) if top.is_dir() else []
        for folder in folders:
            for error in check_one(folder):
                print(f"{kind}/{folder.name}: {error}")
                failed += 1
        counts.append(f"{len(folders)} {noun}")
    print(f"{' and '.join(counts)} checked, {failed} problem(s).")
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
