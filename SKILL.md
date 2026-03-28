---
name: darren-notebooklm-workflow
description: "Run Darren's staged NotebookLM reading workflow: inspect the registered NotebookLM library or ask for a notebook URL, ask Darren how he wants to read a paper/article, then use NotebookLM to run an adaptive question funnel grounded in first principles and, when relevant, Aristotelian four causes or potentiality/actuality. Record under every question what it establishes and why it matters, synthesize the answers, write the result to an Obsidian Markdown note, archive it in DARREN THE NOTES, and update the current daily note with double links. Use when Darren asks to deeply read a paper, article, or notebook through NotebookLM and wants the full process saved in Obsidian."
---

# Darren NotebookLM Workflow

Use this skill as an orchestration layer around the existing NotebookLM, Obsidian, and archive skills. Reuse those skills instead of rebuilding their capabilities here. For all notebook access, treat `$notebooklm` as the single NotebookLM execution path.

## Companion Skills

- Use `$brainstorming` at `/Users/camellionkid/.agents/skills/brainstorming/SKILL.md` at the very beginning to clarify the reading goal, success criteria, funnel intensity, and expected output before asking NotebookLM anything.
- Use `$superpowers` at `/Users/camellionkid/.openclaw/workspace/skills/superpowers/SKILL.md` immediately after the reading goal is clarified to frame the session as exploratory research, implementation preparation, or debugging preparation. Reuse its systematic pipeline when the reading will feed a build or a fix.
- Use `$notebooklm` at `/Users/camellionkid/.agents/skills/notebooklm-skill/SKILL.md` for authentication, notebook listing, notebook registration, smart add, follow-up handling, and each source-grounded query. Do not duplicate or replace its NotebookLM workflow in this skill.
- Use `$obsidian-cli` at `/Users/camellionkid/.codex/skills/obsidian-cli/SKILL.md` to create the Markdown note, inspect the daily note path, and append the backlink.
- Use `$darren-archive` at `/Users/camellionkid/Desktop/01-10 系统储存（System）/02 AI/02.01 Skills/darren-archive/SKILL.md` to archive the finished note into DARREN THE NOTES.

## Session Setup

1. Ensure Obsidian is open and the CLI is available.
2. Prepare the workflow directory:

```bash
WORKFLOW_DIR="/Users/camellionkid/.codex/skills/darren-notebooklm-workflow"
```

3. For NotebookLM work, switch to the NotebookLM skill directory and follow `$notebooklm` exactly as written:

```bash
cd /Users/camellionkid/.agents/skills/notebooklm-skill
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
```

4. If the library is empty, ask Darren for a NotebookLM URL. If Darren gives a URL without metadata, use `$notebooklm`'s smart add workflow instead of inventing metadata.

## Workflow

### 0. Front-Load Brainstorming and Superpowers

1. Invoke `$brainstorming` first.
2. Use it to pin down:
   - what Darren wants from this reading
   - whether the goal is overview, critique, concept analysis, writing support, implementation support, or debugging support
   - whether the funnel should stay adaptive or switch to heavy mode
   - what counts as done for this session
3. After the reading goal is stable, invoke `$superpowers`.
4. Use `$superpowers` to classify the downstream context:
   - pure research note
   - pre-build specification input
   - pre-debug root-cause input
5. If the session will later feed implementation or debugging, let `$superpowers` set the execution frame before NotebookLM questioning starts.

### 1. Resolve the Notebook and the Target Source

1. Show Darren the registered notebook list when available.
2. Ask which notebook to use, or ask for a NotebookLM URL if the target notebook is not registered yet.
3. If the notebook contains multiple source documents and Darren did not name the target article, ask NotebookLM to enumerate the sources before asking Darren to choose one article or theme.
4. Keep the user-side prompt minimal. Ask one concise question, not a full questionnaire.

Recommended discovery question when the notebook contents are unclear:

```bash
cd /Users/camellionkid/.agents/skills/notebooklm-skill
python scripts/run.py ask_question.py \
  --notebook-id NOTEBOOK_ID \
  --question "这个 notebook 里有哪些文章、论文或资料？请按标题列出，并各用一句话说明主题。"
```

### 2. Ask Darren How He Wants to Read the Article

Ask one concise question with a short menu. Capture Darren's wording and keep it in the final note. If `$brainstorming` already clarified this, reuse that result instead of asking again.

Also choose the funnel intensity:

- `自适应精读（默认）`：默认用 `10→6→4→3→1`，当信息已充分时提前收束
- `重度精读`：只有 Darren 明确要求时才用 `20→10→5→3→1`

Suggested options:

- `总览`：快速看主题、结构、结论
- `论证结构`：拆核心论点、证据与推理链
- `概念辨析`：梳理关键术语、概念关系、作者定义
- `批判性阅读`：找最强反对意见、盲点、遗漏前提
- `研究转化`：把内容转化成论文、研究问题或写作提纲
- `自定义`：直接使用 Darren 的原话

If Darren specifies a philosophical lens, HR lens, or writing goal, carry it through every later phase.

### 3. Run the Adaptive Ladder

Use `references/question-ladder.md` to choose the question goals for each phase.

Rules:

- All NotebookLM calls in this section must go through `$notebooklm` and its `run.py` wrapper.
- Ask NotebookLM one question at a time. Do not batch multiple questions into one prompt.
- Because `$notebooklm` is stateless across questions, include enough carry-over context in each new question.
- Honor `$notebooklm`'s follow-up mechanism: after every answer, compare it with the current phase goal and decide what the next question must resolve.
- Default to first-principles decomposition: separate claim, evidence, concept, cause, structure, and end before moving into critique.
- When the article is metaphysical, ethical, explanatory, or process-oriented, explicitly test whether Aristotle's four causes or potentiality/actuality give a better reading lens.
- After every answer, save three fields:
  - `question`
  - `why`
  - `answer`
- The `why` field must explain both:
  - `知其然`：这道题要先确定什么事实、结构或判断
  - `知其所以然`：这道题要追到什么原因、根据、机制、目的或生成条件
- Add an optional `lens` field when useful, such as `first-principles`, `four-causes`, or `potentiality-actuality`.
- Every question must stay grounded in the chosen notebook source. If the notebook does not answer it, record `NotebookLM 未明确提到`, never invent an answer.
- The later phases must be based on the earlier answers, not written in advance.
- Stop a phase early when new questions no longer materially reduce uncertainty. Never ask filler questions just to hit a quota.

Use this phase sequence:

1. `默认自适应模式`
   - `10 questions`: 建立全景，抓 thesis、结构、概念、证据、假设、方法、结论
   - `6 questions`: 深挖隐含前提、歧义、跳步、证据薄弱处
   - `4 questions`: 施压核心论证，逼出最强 objection 与最脆弱前提
   - `3 questions`: 转化到 Darren 的论文、HR 场景、伦理分析或概念系统
   - `1 total question`: 压成最终综合判断
2. `重度精读模式`
   - 只有 Darren 明确指定时才运行 `20→10→5→3→1`
3. `阶段退出标准`
   - 第一阶段结束：已经可以复述全文结构
   - 第二阶段结束：已经知道争议与薄弱点在哪里
   - 第三阶段结束：已经知道最强 objection 与残存成立部分
   - 第四阶段结束：已经知道这篇材料对 Darren 有何具体用途

### 4. Synthesize Before Writing

After the ladder is complete, write a concise synthesis in your own words:

- `概要`
- `核心论证`
- `第一性原理拆解`
- `四因分析` 或 `潜能/现实分析`（按文本适配，不必两者都强行使用）
- `最强反对意见`
- `对 Darren 的启发`
- `仍待追问`

Keep the synthesis grounded in the NotebookLM answers. Mark inference as inference. Do not stop at what the text says; also recover why the text says it, what generates it, and what purpose or realization structure the argument implies.

If `$superpowers` framed the session as implementation or debugging preparation, end the synthesis with explicit handoff material:

- what the later plan should build or fix
- which uncertainty has already been resolved by reading
- which uncertainty still blocks execution

### 5. Create the Obsidian Markdown Note

1. Read today's daily note path and extract the daily note name:

```bash
TODAY_PATH="$(obsidian daily:path)"
TODAY_NAME="$(basename "$TODAY_PATH" .md)"
```

2. Build a JSON payload that matches `references/obsidian-note-schema.md`.
3. Render the note content with the helper script:

```bash
python3 "$WORKFLOW_DIR/scripts/build_reading_note.py" \
  --input /tmp/notebooklm-reading.json \
  --format obsidian-content
```

4. Create the note in the pending folder first:

```bash
NOTE_PATH="81-90 待阅读&分类（Pending）/90 一切待分类/YYYY-MM-DD Title - NotebookLM 阅读.md"
NOTE_CONTENT="$(python3 "$WORKFLOW_DIR/scripts/build_reading_note.py" --input /tmp/notebooklm-reading.json --format obsidian-content)"
obsidian create path="$NOTE_PATH" content="$NOTE_CONTENT" silent overwrite
```

5. Use `references/obsidian-note-schema.md` for the section order and metadata fields.

### 6. Archive the Note and Update the Daily Note

1. Invoke `$darren-archive` on the note you just created. Archive one note only.
2. After the archive step, confirm the final path.
3. Append the double-link entry to today's daily note:

```bash
obsidian daily:append content="- [[NOTE_TITLE]]"
```

4. Make sure the generated note itself contains `关联日志：[[TODAY_NAME]]`. That creates the backlink pair.

### 7. Report Back

Tell Darren:

- which notebook was used
- which reading mode was chosen
- whether the notebook had enough information
- where the final note ended up after archiving
- what remained unresolved

## Output Requirements

- Follow `references/obsidian-note-schema.md` for the note structure.
- Keep the phase history visible. Darren asked to preserve the process, not just the summary.
- Under every question include `为什么问这个问题（知其然 / 知其所以然）`.
- Default to first-principles reading. Do not merely record conclusions; track grounds, causes, structure, and ends.
- When the text supports it, use Aristotle's four causes or potentiality/actuality to make the note more explanatory, not more ornamental.
- Use Chinese by default unless Darren explicitly asks for English.
- Prefer short structured prose over tables unless the content is genuinely tabular.

## Failure Handling

- If NotebookLM auth fails, stop and hand the session back to `$notebooklm`'s re-authentication flow.
- If the library is empty, do not guess; ask for a notebook URL or notebook name.
- If the notebook contains multiple sources and the target article is still ambiguous after one discovery pass, stop and ask Darren to choose.
- If Obsidian CLI is unavailable, stop and report that the note could not be written.
- If the archive destination is low-confidence, let `$darren-archive` ask Darren instead of guessing.

## References

- Read `references/question-ladder.md` before writing the ladder prompts.
- Read `references/obsidian-note-schema.md` before generating the JSON payload for the note.
