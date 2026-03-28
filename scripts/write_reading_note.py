#!/usr/bin/env python3
"""Write a rendered NotebookLM reading note into the vault and back-link the daily note."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from build_reading_note import read_payload, render_markdown


def ensure_inside_vault(vault_root: Path, relative_path: str) -> Path:
    """Resolve a vault-relative path and reject path traversal."""
    full_path = (vault_root / Path(relative_path)).resolve()
    try:
        full_path.relative_to(vault_root)
    except ValueError as exc:
        raise ValueError(f"Path escapes vault root: {relative_path}") from exc
    return full_path


def write_note(vault_root: Path, note_path: str, markdown: str) -> tuple[Path, bool]:
    """Write the note markdown to the requested vault-relative path."""
    full_path = ensure_inside_vault(vault_root, note_path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    previous = full_path.read_text(encoding="utf-8") if full_path.exists() else None
    full_path.write_text(markdown, encoding="utf-8")
    return full_path, previous != markdown


def insert_link_under_heading(content: str, heading: str, link_line: str) -> tuple[str, bool]:
    """Insert the note link directly under the requested heading if absent."""
    normalized_link = link_line.strip()
    lines = content.splitlines()

    if any(line.strip() == normalized_link for line in lines):
        return content, False

    for index, line in enumerate(lines):
        if line.strip() == heading.strip():
            updated = lines[: index + 1] + [normalized_link] + lines[index + 1 :]
            return "\n".join(updated).rstrip() + "\n", True

    updated = content.rstrip() + f"\n\n{heading}\n{normalized_link}\n"
    return updated, True


def update_daily_note(vault_root: Path, daily_note_path: str, note_title: str) -> tuple[Path, bool]:
    """Append a double link entry to the daily note under the notes heading."""
    full_path = ensure_inside_vault(vault_root, daily_note_path)
    if not full_path.exists():
        raise FileNotFoundError(f"Daily note not found: {daily_note_path}")

    content = full_path.read_text(encoding="utf-8")
    link_line = f"- [[{note_title}]]"
    updated, changed = insert_link_under_heading(content, "## 3. Notes & ideas", link_line)
    if changed:
        full_path.write_text(updated, encoding="utf-8")
    return full_path, changed


def build_result(note_path: Path, daily_note_path: Path, note_written: bool, backlink_added: bool) -> dict[str, Any]:
    """Return a compact JSON result for callers."""
    return {
        "success": True,
        "note_path": str(note_path),
        "daily_note_path": str(daily_note_path),
        "note_written": note_written,
        "backlink_added": backlink_added,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-root", required=True, help="Absolute path to the Obsidian vault root")
    parser.add_argument("--input-json", required=True, help="Path to the NotebookLM reading payload JSON")
    parser.add_argument("--note-path", required=True, help="Vault-relative note path to write")
    parser.add_argument("--daily-note-path", required=True, help="Vault-relative daily note path to update")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).expanduser().resolve()
    payload = read_payload(Path(args.input_json))
    markdown = render_markdown(payload)
    note_full_path, note_written = write_note(vault_root, args.note_path, markdown)
    daily_full_path, backlink_added = update_daily_note(vault_root, args.daily_note_path, payload["title"])

    print(json.dumps(build_result(note_full_path, daily_full_path, note_written, backlink_added), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
