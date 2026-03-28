# Obsidian Note Schema

Use this schema when building the JSON payload for `scripts/build_reading_note.py`.

## Recommended Note Location

Create the draft note here first:

`81-90 待阅读&分类（Pending）/90 一切待分类/`

After creation, hand the note to `$darren-archive`.

## Recommended Filename

`YYYY-MM-DD {source_title} - NotebookLM 阅读.md`

Keep the visible title aligned with the filename unless Darren asks otherwise.

## JSON Shape

```json
{
  "title": "Virtue Ethics and Emotional Agency - NotebookLM 阅读",
  "created": "2026-03-28",
  "source_title": "Virtue Ethics and Emotional Agency",
  "source_kind": "paper",
  "notebook_name": "Virtue Ethics Papers",
  "notebook_id": "virtue-ethics-papers",
  "notebook_url": "https://notebooklm.google.com/notebook/...",
  "reading_mode": "批判性阅读",
  "funnel_mode": "自适应精读（10→6→4→3→1）",
  "reading_request": "重点看核心论证、概念界定和最强反对意见",
  "reasoning_frameworks": [
    "first-principles",
    "four-causes"
  ],
  "daily_note_name": "2026-03-28",
  "summary": "这里写整体概要。",
  "core_argument": "这里写核心论证。",
  "first_principles_summary": "这里写第一性原理拆解。",
  "four_causes": {
    "material": "这里写质料因。",
    "formal": "这里写形式因。",
    "efficient": "这里写动力因。",
    "final": "这里写目的因。"
  },
  "potentiality_actuality": {
    "potentiality": "这里写潜能。",
    "actuality": "这里写现实。",
    "transition": "这里写潜能走向现实的条件或机制。"
  },
  "strongest_objection": "这里写最强反对意见。",
  "darren_takeaways": [
    "启发 1",
    "启发 2"
  ],
  "open_questions": [
    "待追问 1"
  ],
  "phases": [
    {
      "label": "第一轮（10问）",
      "purpose": "先建立全景图。",
      "questions": [
        {
          "question": "作者的核心论点是什么？",
          "why": "知其然：先锁定全文中心。知其所以然：确认后续所有分析围绕同一个支点展开。",
          "lens": "first-principles",
          "answer": "NotebookLM 的回答……"
        }
      ]
    }
  ],
  "final_question": {
    "question": "综合前面所有回答，这篇文章最值得保留的一条判断是什么？",
    "why": "知其然：压缩出总判断。知其所以然：把前面分散的原因、结构与目的收束成一个可复用结论。",
    "answer": "NotebookLM 的最终综合回答……"
  }
}
```

## Rendered Note Sections

The rendered Markdown should contain these sections in order:

1. YAML frontmatter
2. `# 概要`
3. `# 阅读设定`
4. `# 原理透视`
5. `# 分阶段问答`
6. `# 总问题`
7. `# 综合判断`
8. `# 仍待追问`
9. `# 链接`

## Backlink Rule

The final note must contain:

`关联日志：[[{daily_note_name}]]`

After the note is archived, append this to today's daily note:

`- [[{title}]]`

That gives Darren the double link he asked for.
