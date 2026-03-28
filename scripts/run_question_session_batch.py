#!/usr/bin/env python3
"""Run a batch of NotebookLM questions inside one persistent browser session."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_SKILL_DIR = Path("/Users/camellionkid/.agents/skills/notebooklm-skill")


def load_questions(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Questions JSON must be a list")
    return data


def build_prompt(context: str, question: str) -> str:
    context = context.strip()
    question = question.strip()
    if not context:
        return question
    return f"{context}\n当前问题：{question}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--notebook-url", required=True)
    parser.add_argument("--context", default="")
    parser.add_argument("--skill-dir", default=str(DEFAULT_SKILL_DIR))
    parser.add_argument("--show-browser", action="store_true")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    sys.path.insert(0, str((skill_dir / "scripts").resolve()))

    from patchright.sync_api import sync_playwright
    from browser_utils import BrowserFactory
    from browser_session import BrowserSession

    questions = load_questions(Path(args.questions_json))
    output_path = Path(args.output_json).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    with sync_playwright() as playwright:
        context = BrowserFactory.launch_persistent_context(
            playwright,
            headless=not args.show_browser,
        )
        session = BrowserSession(
            session_id=f"batch-{int(time.time())}",
            context=context,
            notebook_url=args.notebook_url,
        )

        try:
            for index, item in enumerate(questions, start=1):
                question = str(item.get("question", "")).strip()
                if not question:
                    raise ValueError(f"Question #{index} is missing 'question'")

                started = time.time()
                response = session.ask(build_prompt(args.context, question))
                if response.get("status") != "success":
                    raise RuntimeError(json.dumps(response, ensure_ascii=False, indent=2))

                result = dict(item)
                result["answer"] = response["answer"].strip()
                result["elapsed_seconds"] = round(time.time() - started, 2)
                results.append(result)
                output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"Q{index:02d} ok ({result['elapsed_seconds']}s)", flush=True)
        finally:
            try:
                session.close()
            finally:
                context.close()

    print(f"saved={output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
