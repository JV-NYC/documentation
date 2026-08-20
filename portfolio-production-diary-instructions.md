Edit `portfolio-production-diary.md`.

The file is currently intended to serve as the production diary for the Portfolio project.

Before adding any historical backfill, establish the file structure, conventions, and reusable entry template described below.

Do not add production history yet.

## Purpose

This diary is a chronological, public-readable record of how the portfolio is being made.

Treat each entry as an **abbreviated case study**.

The core structure is:

**Problem / Goal → Constraint → What I did → Outcome → What I learned**

The diary should record meaningful production work, experiments, tests, revisions, failures, decisions, and milestones.

It is not:

- a task manager
- a changelog for the live site
- a transcript of conversations
- a running list of trivial activity
- a polished retrospective pretending the process was cleaner than it was

`portfolio-change-log.md` is reserved for pushed updates after the site is live. Do not use it during this work.

## Canonical format

Use portable standard Markdown as the source of truth.

The Markdown should import cleanly into Notion and remain readable outside Notion.

Prefer:

- standard headings
- paragraphs
- bullet and numbered lists
- blockquotes
- bold and italics
- inline code
- fenced code blocks
- standard Markdown links
- horizontal rules

Avoid:

- HTML layout
- complex Markdown tables
- platform-specific Markdown extensions
- Notion-only syntax
- formatting that depends on a single application

The canonical record remains chronological. Do not reorganize entries by topic.

Notion may later provide filtered or alternate views, but the Markdown file should preserve the historical sequence of the work.

## Voice

All narrative prose must follow `voice-principles.md`.

Treat that file as the canonical writing-style specification.

In particular:

- preserve the movement of the thinking
- lead with the point
- preserve uncertainty where it existed
- use concrete examples where useful
- retain changes of mind and failed approaches
- avoid corporate or consultancy language
- avoid generic AI phrasing
- do not over-polish the process
- do not convert ordinary production work into inflated design rhetoric
- never use an em dash

The diary may eventually be public. Write clearly enough that an outside reader can understand what happened, but do not sanitize the work into a retrospective success story.

## Entry heading

Every entry begins:

```markdown
### YYYY-MM-DD | Short descriptive title
```

Use ISO dates.

For historical backfill, use the date when the work actually occurred when that can be established with reasonable confidence.

If exact dating cannot be established, do not invent precision.

Do not include times unless a time is genuinely relevant to the event.

## Required metadata

Every entry should include:

```markdown
**Item:**  
**Type:**  
```

### Item

Name the actual thing being worked on.

Examples:

- Framer CMS
- Artifact Card
- Landing page
- Design system
- Low-Tide Signal Station
- Portfolio world
- Claude design-system handoff
- Framer token ingestion

Prefer a specific item over a broad category.

### Type

Use one primary type from this stable vocabulary:

- Build
- Experiment
- Test
- Research
- Design
- Decision
- Revision
- Setup
- Review
- Debug
- Milestone

Use multiple types only when genuinely necessary.

## Optional metadata

Include these only when useful:

```markdown
**Tools:**  
**Status:**  
**Tags:**  
**Source:**  
```

### Tools

Name tools that materially participated in the work.

Examples:

`Framer, Figma, Claude, ChatGPT, Gemini`

Do not list incidental tools simply because they were open.

### Status

Use when it adds useful context:

- In progress
- Complete
- Blocked
- Abandoned
- Revisited

Do not use task-management statuses such as To Do.

### Tags

Use a small number of lowercase tags in inline code formatting.

Example:

`framer`, `cms`, `design-system`

Tags should aid retrieval, not describe every aspect of the entry.

### Source

Use when the work has a useful durable reference.

Examples:

```markdown
**Source:** `design-system.md`
```

```markdown
**Source:** Framer Lab / Artifact Card
```

```markdown
**Source:** Git commit `abc1234`
```

Do not invent source references.

## Case study structure

Use this as the default entry structure:

```markdown
### YYYY-MM-DD | Entry title

**Item:**  
**Type:**  
**Tools:**  
**Status:**  
**Tags:**  
**Source:**  

#### Problem / Goal

What was I trying to solve, make, test, understand, or decide?

#### Constraint

What materially shaped the work?

#### What I did

What approach, experiment, build, revision, or test actually occurred?

#### Outcome

What happened?

What changed as a result?

#### What I learned

What changed in my understanding because of the work?

#### Next

Only include this when there is a meaningful next move.
```

## Section rules

The structure above is the default, not an excuse to manufacture empty sections.

The abbreviated case-study spine should remain recognizable, but use judgment.

A section may be omitted when it is genuinely irrelevant.

Do not add boilerplate merely to satisfy the template.

The most important sections are:

- Problem / Goal
- Constraint
- What I did
- Outcome
- What I learned

### Problem / Goal

State the actual problem or production goal.

Avoid vague entries such as:

> Worked on the CMS.

Prefer:

> Test whether one Artifacts collection can support both case studies and essays without creating unnecessary CMS complexity.

### Constraint

Record only constraints that materially affected the work.

These might be:

- platform limitations
- Framer compatibility
- accessibility
- performance
- available time
- visual restraint
- CMS simplicity
- production effort
- authorship goals
- limits discovered in a tool
- an intentional design restriction

Do not invent constraints to make an entry sound more rigorous.

### What I did

Describe the actual approach.

This may be prose, a short list, or both.

Avoid turning the entry into exhaustive technical documentation unless the technical detail itself matters to understanding the case.

### Outcome

This section is essential.

Record the result, not merely the activity.

Examples:

- a test passed
- a test failed
- an approach was abandoned
- a workflow was simplified
- a component was built
- a design direction changed
- a limitation was discovered
- a manual step was accepted as preferable to further automation

### What I learned

Capture the meaningful lesson.

Do not force a grand lesson from routine work.

Sometimes the useful learning is small and practical.

### Next

Use only when the next move is clear and meaningful.

Do not turn every diary entry into a project-management checklist.

## AI process notes

AI provenance should be included selectively.

Do not record every AI interaction.

Include an AI process note when an AI system:

- materially shaped an idea or approach
- challenged an assumption
- generated something that was actually tested
- exposed a meaningful problem
- led to an interesting dead end
- materially helped make a decision
- played a deliberate role where model or effort choice mattered

Skip AI notes for:

- routine formatting
- simple file edits
- incidental factual help
- trivial assistance
- ordinary conversational turns that did not affect the work

When relevant, append:

```markdown
#### AI process note

**System:**  
**Role:**  

**Prompt sketch**

```text
Paraphrased structure of the prompt.
Do not reproduce the original prompt verbatim.
```
```

### System

Include the specific model and effort level when known and relevant.

Examples might include:

- ChatGPT 5.6 Sol, High
- Claude Opus, High

Do not invent a model or effort level if it is not known.

### Role

Describe what the AI was actually being used for.

Examples:

- Technical critique
- Visual ideation
- Adversarial review
- Implementation exploration
- Synthesis
- Debugging

### Prompt sketch

Summarize or paraphrase how the problem was framed.

Do not paste the verbatim prompt.

The prompt sketch should show useful structure, constraints, or intent so a reader can understand how the AI was directed.

Use a fenced `text` code block so the prompt sketch is visually distinct from the diary prose.

The useful part is not telemetry. The useful part is seeing how the human framed the problem and what happened because of that interaction.

## Authorship

Write the diary in the designer's voice.

Prefer:

> I wanted to know whether one CMS collection could carry both essays and case studies without creating a mess.

Avoid:

> The designer evaluated the feasibility of a unified CMS architecture.

Prefer:

> At some point the automation became the problem.

Avoid:

> Further automation presented diminishing operational returns.

AI involvement should remain visible when relevant, but the diary should not read as an AI observer narrating the designer's work.

## Historical record note

Add a short note near the beginning of the file:

> **Historical record note:** Entries through 2026-08-19 were reconstructed from contemporaneous Portfolio project conversations when this diary was established. Dates reflect the original work where they can be established. Later entries are recorded as the project develops.

Do not add the historical entries yet.

## Reusable template

Add a clearly marked reusable template near the top of the file:

```markdown
### YYYY-MM-DD | Entry title

**Item:**  
**Type:**  
**Tools:**  
**Status:**  
**Tags:**  
**Source:**  

#### Problem / Goal

#### Constraint

#### What I did

#### Outcome

#### What I learned

#### Next

#### AI process note

**System:**  
**Role:**  

**Prompt sketch**

```text
Paraphrased prompt structure.
```
```

Make clear in the surrounding instructions that optional metadata and optional sections should be omitted when they add no value.

## Final instruction

For this edit, establish only:

1. file title and purpose
2. historical record note
3. writing and formatting conventions
4. metadata conventions
5. abbreviated case-study structure
6. selective AI provenance rules
7. reusable entry template

Do not add historical production entries yet.

Do not edit `portfolio-ideation-log.md`.

Do not edit `portfolio-change-log.md`.