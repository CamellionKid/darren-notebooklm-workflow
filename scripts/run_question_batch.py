#!/usr/bin/env python3
"""Run a batch of stateless NotebookLM questions through the notebooklm skill wrapper."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


FOLLOW_UP_REMINDER = "EXTREMELY IMPORTANT: Is that ALL you need to know?"
DEFAULT_SKILL_DIR = Path("/Users/camellionkid/.agents/skills/notebooklm-skill")


def load_questions(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Questions JSON must be a list")
    return data


def extract_answer(output: str) -> str:
    match = re.search(r"={60}\nQuestion:.*?\n={60}\n\n(.*)\n\n={60}", output, re.S)
    if not match:
        raise RuntimeError("Could not parse NotebookLM answer block")
    answer = match.group(1).strip()
    if FOLLOW_UP_REMINDER in answer:
        answer = answer.split(FOLLOW_UP_REMINDER, 1)[0].rstrip()
    return answer.strip()


def build_prompt(context: str, question: str) -> str:
    context = context.strip()
    question = question.strip()
    if not context:
        return question
    return f"{context}\n当前问题：{question}"


def run_question(skill_dir: Path, notebook_url: str, prompt: str, show_browser: bool) -> str:
    env = dict(os.environ)
    env["NOTEBOOKLM_USE_TEMP_PROFILE"] = "1"
    cmd = [
        "python3",
        "scripts/run.py",
        "ask_question.py",
        "--notebook-url",
        notebook_url,
        "--question",
        prompt,
    ]
    if show_browser:
        cmd.append("--show-browser")

    proc = subprocess.run(
        cmd,
        cwd=skill_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "NotebookLM question failed.\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}"
        )
    return extract_answer(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions-json", required=True, help="Path to a JSON list of question objects")
    parser.add_argument("--output-json", required=True, help="Where to write the answered question list")
    parser.add_argument("--notebook-url", required=True, help="NotebookLM URL to query")
    parser.add_argument("--context", default="", help="Shared context prefix for every question")
    parser.add_argument("--skill-dir", default=str(DEFAULT_SKILL_DIR), help="Path to the notebooklm skill root")
    parser.add_argument("--show-browser", action="store_true", help="Show the browser during each question")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    questions = load_questions(Path(args.questions_json))
    output_path = Path(args.output_json).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, Any]] = []
    for index, item in enumerate(questions, start=1):
        question = str(item.get("question", "")).strip()
        if not question:
            raise ValueError(f"Question #{index} is missing 'question'")

        started = time.time()
        answer = run_question(
            skill_dir=skill_dir,
            notebook_url=args.notebook_url,
            prompt=build_prompt(args.context, question),
            show_browser=args.show_browser,
        )

        result = dict(item)
        result["answer"] = answer
        result["elapsed_seconds"] = round(time.time() - started, 2)
        results.append(result)
        output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Q{index:02d} ok ({result['elapsed_seconds']}s)", flush=True)

    print(f"saved={output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
