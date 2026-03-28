#!/usr/bin/env python3
"""Render a staged NotebookLM reading session into Obsidian Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable


def read_payload(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object")
    return data


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def join_lines(parts: Iterable[str]) -> str:
    return "\n".join(part.rstrip() for part in parts if part is not None).strip() + "\n"


def yaml_scalar(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def format_frontmatter(data: dict[str, Any]) -> str:
    title = data.get("title", "NotebookLM 阅读")
    created = data.get("created", "")
    notebook_name = data.get("notebook_name", "")
    reading_mode = data.get("reading_mode", "")
    source_kind = data.get("source_kind", "")
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"created: {yaml_scalar(created)}",
        'tags: ["notebooklm-reading"]',
        f"notebook_name: {yaml_scalar(notebook_name)}",
        f"reading_mode: {yaml_scalar(reading_mode)}",
        f"source_kind: {yaml_scalar(source_kind)}",
        "---",
    ]
    return "\n".join(lines)


def render_phase(phase: dict[str, Any]) -> str:
    label = phase.get("label", "未命名阶段")
    purpose = phase.get("purpose", "")
    blocks = [f"## {label}"]
    if purpose:
        blocks.append(f"目的：{purpose}")

    for idx, item in enumerate(ensure_list(phase.get("questions")), start=1):
        if not isinstance(item, dict):
            continue
        question = item.get("question", "").strip()
        why = item.get("why", "").strip()
        lens = item.get("lens", "").strip()
        answer = item.get("answer", "").strip()
        blocks.extend(
            [
                f"### Q{idx:02d}",
                f"问题：{question or '未记录'}",
                f"为什么问这个问题（知其然 / 知其所以然）：{why or '未记录'}",
                f"推理镜头：{lens}" if lens else None,
                "回答：",
                answer or "NotebookLM 未明确提到。",
            ]
        )

    return "\n\n".join(blocks)


def render_list(items: list[Any]) -> str:
    if not items:
        return "- 暂无"
    rendered = []
    for item in items:
        text = str(item).strip()
        rendered.append(f"- {text or '未记录'}")
    return "\n".join(rendered)


def render_mapping(mapping: Any, ordered_keys: list[tuple[str, str]]) -> str:
    if not isinstance(mapping, dict) or not mapping:
        return "- 暂无"
    rendered = []
    for key, label in ordered_keys:
        value = str(mapping.get(key, "")).strip()
        rendered.append(f"- {label}：{value or '暂无'}")
    return "\n".join(rendered)


def render_markdown(data: dict[str, Any]) -> str:
    phases = ensure_list(data.get("phases"))
    final_question = data.get("final_question", {}) or {}
    daily_note_name = data.get("daily_note_name", "")

    parts = [
        format_frontmatter(data),
        f"# {data.get('title', 'NotebookLM 阅读')}",
        "# 概要",
        data.get("summary", "待补充。"),
        "# 阅读设定",
        f"- 来源标题：{data.get('source_title', '未记录')}",
        f"- 来源类型：{data.get('source_kind', '未记录')}",
        f"- Notebook：{data.get('notebook_name', '未记录')}",
        f"- Notebook ID：{data.get('notebook_id', '未记录')}",
        f"- 阅读模式：{data.get('reading_mode', '未记录')}",
        f"- 漏斗模式：{data.get('funnel_mode', '未记录')}",
        f"- 推理框架：{', '.join(ensure_list(data.get('reasoning_frameworks'))) or '未记录'}",
        f"- 阅读要求：{data.get('reading_request', '未记录')}",
        "# 原理透视",
        "## 第一性原理拆解",
        data.get("first_principles_summary", "待补充。"),
        "## 四因分析",
        render_mapping(
            data.get("four_causes"),
            [
                ("material", "质料因"),
                ("formal", "形式因"),
                ("efficient", "动力因"),
                ("final", "目的因"),
            ],
        ),
        "## 潜能与现实",
        render_mapping(
            data.get("potentiality_actuality"),
            [
                ("potentiality", "潜能"),
                ("actuality", "现实"),
                ("transition", "转化机制"),
            ],
        ),
        "# 分阶段问答",
        "\n\n".join(render_phase(phase) for phase in phases) if phases else "暂无分阶段问答。",
        "# 总问题",
        f"问题：{final_question.get('question', '未记录')}",
        f"为什么问这个问题（知其然 / 知其所以然）：{final_question.get('why', '未记录')}",
        "回答：",
        final_question.get("answer", "NotebookLM 未明确提到。"),
        "# 综合判断",
        "## 核心论证",
        data.get("core_argument", "待补充。"),
        "## 最强反对意见",
        data.get("strongest_objection", "待补充。"),
        "## 对 Darren 的启发",
        render_list(ensure_list(data.get("darren_takeaways"))),
        "# 仍待追问",
        render_list(ensure_list(data.get("open_questions"))),
        "# 链接",
        f"关联日志：[[{daily_note_name}]]" if daily_note_name else "关联日志：待补充",
        f"Notebook URL：{data.get('notebook_url', '未记录')}",
    ]
    return join_lines(parts)


def to_obsidian_content(markdown: str) -> str:
    return markdown.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to the JSON payload")
    parser.add_argument(
        "--format",
        choices=("markdown", "obsidian-content"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument("--output", help="Optional output file path")
    args = parser.parse_args()

    payload = read_payload(Path(args.input))
    markdown = render_markdown(payload)
    output = markdown if args.format == "markdown" else to_obsidian_content(markdown)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
