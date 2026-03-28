# Question Ladder

Use this file to design the staged NotebookLM questioning sequence. The point is not to generate random questions; it is to reduce uncertainty in a disciplined order.

## Mode Selection

Choose the funnel mode before asking the first substantive question:

- `自适应精读（默认）`: `10→6→4→3→1`
- `重度精读`: `20→10→5→3→1`

Use the heavy mode only when Darren explicitly asks for it or when the source is unusually dense and foundational. Otherwise prefer the adaptive mode.

## Global Rules

- Ask one NotebookLM question at a time.
- Each saved question must carry a `why` field.
- Each `why` field should explicitly include both:
  - `知其然`: what fact, structure, distinction, or judgment this question needs to establish
  - `知其所以然`: what cause, ground, mechanism, or purpose this question is trying to uncover
- Prefer article-specific wording over generic academic prompts.
- If Darren gives a reading lens, propagate it throughout the ladder.
- Default to first-principles decomposition: break the text into irreducible claims, concepts, assumptions, evidence, and ends.
- When suitable, use Aristotle's explanatory lenses:
  - `质料因`: what material, evidence, textual basis, or substrate the claim depends on
  - `形式因`: what definition, structure, distinction, or organizing form makes it what it is
  - `动力因`: what process, agent, or mechanism brings the claim or change about
  - `目的因`: what end, function, or telos the argument or object is for
- When the text involves development, formation, cultivation, change, realization, or capacity, ask whether `潜能 → 现实` is the better lens:
  - what exists only as a capacity
  - what counts as its realization
  - what transition or condition moves one into the other
- Stop a phase when new questions stop materially reducing uncertainty.

## Default Funnel: 10 → 6 → 4 → 3 → 1

Use this unless Darren explicitly requests the heavy mode.

### Phase 1: 10 Questions

Goal: map the article before going deep.

Typical coverage:

1. What is the central thesis, and what problem is the author trying to solve?
2. How is the article structured from beginning to end?
3. What are the core concepts, and how are they defined?
4. Which claims are descriptive, and which are normative?
5. What evidence, textual basis, or examples carry the argument?
6. What method or argumentative strategy is doing the work?
7. What assumptions are explicit, and which ones stay implicit?
8. Where does the argument make a major transition, and where is the main internal tension?
9. What does the author reject, conclude, or leave unresolved?
10. What is the single most important thing a careful reader should not miss, especially for Darren's chosen lens?

Exit standard:

- You can restate the article's thesis, structure, core concepts, and basic support without guessing.

### Phase 2: 6 Questions

Goal: deepen the places where the first round exposed uncertainty.

Typical targets:

- hidden premises that support the thesis
- ambiguous jumps between sections
- conflict between stated goal and actual method
- thin evidence
- suspicious concept shifts
- tension between cited thinkers
- missing counterexample
- possible alternative interpretation
- dependence on historical context
- what would break if one premise failed

Exit standard:

- You can name where the argument is strongest, where it is thinnest, and which hidden premise matters most.

### Phase 3: 4 Questions

Goal: stress-test the heart of the argument.

Recommended focus:

1. What is the strongest objection?
2. What is the author's best available reply?
3. Which premise is most vulnerable?
4. After this stress test, what still stands?

When Darren is doing philosophy work, always try to surface the strongest objection explicitly.

Exit standard:

- You know what the strongest objection is, what survives it, and why.

### Phase 4: 3 Questions

Goal: translate the article into Darren's practical or scholarly use.

Recommended directions:

1. How should Darren use this in his paper, note system, or project?
2. Which concepts deserve their own follow-up notes?
3. What research question or writing move naturally follows from this reading?

If Darren specified HR, ethics, virtue ethics, AI ethics, or onboarding analysis, make that lens concrete here.

Exit standard:

- You know how Darren should use this reading next.

### Phase 5: 1 Total Question

Goal: ask for the one synthesis question that only makes sense after the whole ladder.

The total question should usually combine:

- the article's central claim
- its strongest pressure point
- its practical or scholarly significance for Darren

Example pattern:

`综合前面所有回答，如果只保留这篇文章最有价值的一条判断、最脆弱的一处前提、以及它对 [Darren's goal] 最直接的意义，分别是什么？请说明理由。`

## Heavy Funnel: 20 → 10 → 5 → 3 → 1

Use this mode only when Darren explicitly asks for full heavy reading.

### Phase 1: 20 Questions

Goal: map the article in fuller detail than the default mode.

Use the original twenty coverage slots:

1. What is the central thesis?
2. What problem is the author trying to solve?
3. How is the article structured?
4. What are the core concepts and how are they defined?
5. Which claims are descriptive, and which are normative?
6. What evidence or textual support is used?
7. What method or argumentative strategy appears?
8. Which prior thinkers, schools, or debates matter?
9. What assumptions are explicit?
10. What assumptions are implicit?
11. Where does the argument make a major transition?
12. What is the strongest internal tension in the paper?
13. What does the author reject?
14. What is the conclusion?
15. What does the author leave unresolved?
16. Which terms need sharper clarification?
17. Which paragraph or section carries the argumentative weight?
18. What does the article imply but not fully state?
19. How would the article matter to Darren's chosen lens?
20. What is the single most important thing a careful reader should not miss?

### Phase 2: 10 Questions

Use the deeper ambiguity and hidden-premise targets from the default mode, but with more room for parallel tensions.

### Phase 3: 5 Questions

Use the stress-test pattern:

1. What is the strongest objection?
2. What is the author's best available reply?
3. Which premise is most vulnerable?
4. What would a rival framework say?
5. After this stress test, what still stands?

### Phase 4: 3 Questions

Translate the reading into Darren's next concrete use.

### Phase 5: 1 Total Question

Compress everything into a final judgment.

## First-Principles and Aristotelian Prompts

Use these templates only when they fit the source:

- First principles:
  - `如果把作者的中心论点拆到不能再拆，最基础的几个前提分别是什么？`
  - `这些前提里，哪一个是支撑全文的必要条件？`
- Four causes:
  - `这篇文章讨论的对象或德性，其质料因、形式因、动力因、目的因分别是什么？`
  - `如果作者没有显式使用四因框架，哪些回答可以近似映射到四因？`
- Potentiality and actuality:
  - `作者讨论的能力、德性或主体性，哪些还处在潜能状态，哪些已被现实化？`
  - `从潜能到现实的转化机制，在文中依赖哪些条件或实践？`
