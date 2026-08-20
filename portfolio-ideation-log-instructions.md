# Portfolio Ideation Log Instructions

Edit `portfolio-ideation-log.md`.

The file is the canonical, chronological record of the Portfolio project's ideas, references, experiments, questions, principles, and emerging directions. It is the authored source for the generated ideation dataset and the downstream Notion database.

Before adding or revising an entry, follow this document exactly. The parser validates the file's structural conventions; an entry that reads well but breaks those conventions is not valid.

Do not edit `generated/portfolio-ideation.json` manually. Do not author or revise ideas directly in Notion. Do not use this log as a production diary, a task list, or a changelog for the live site.

## Source of truth

The source-of-truth hierarchy is:

```text
Project work and conversation
        ↓
portfolio-ideation-log.md
        ↓
Git
        ↓
generated/portfolio-ideation.json
        ↓
Notion
```

The Markdown log is canonical. JSON and Notion are derived representations.

Make substantive changes in `portfolio-ideation-log.md`, validate it, generate the JSON, inspect the proposed Notion changes, and only then apply a Notion synchronization when authorized.

## Purpose and writing standard

The log preserves how the project's thinking developed. It should retain useful uncertainty, alternatives, and discarded directions rather than rewriting the past to make later decisions seem inevitable.

Each entry is one atomic item: a single idea, direction, experiment, reference, principle, decision-state change, or question. Split independent thoughts into separate entries so each has its own permanent ID and can be retrieved, filtered, and discussed independently.

Write concisely in the designer's voice. State the idea clearly enough that it remains useful when read out of context. Preserve nuance where it matters, but do not turn the log into an exhaustive transcript of conversation or prompt history.

Prefer:

- a specific proposition, observation, or question
- an honest record of uncertainty
- a concrete reference and what it is useful for
- a short paragraph or compact list when the idea needs supporting detail

Avoid:

- task-management prose such as "to do" or "next action"
- retrospective language that treats an open question as already resolved
- duplicating an existing atomic idea instead of revising it
- vague entries such as "Explore the visuals"
- notes that are only status reports without a meaningful ideation item

## Canonical Markdown structure

Use portable standard Markdown. The parser recognizes a strict hierarchy:

```text
Date heading
    Theme heading
        Permanent idea ID comment
        Bold Status: Title line
        Body
```

Example:

```markdown
## Wednesday, August 19, 2026

### Motion

<!-- idea-id: 20260819-000001 -->

**Principle: Alive, not animated**

Stillness should be the default state. Motion should feel like an event rather than a constant demonstration that the website can move.
```

Use the hierarchy exactly:

- Date sections are level-two headings (`##`).
- Themes are level-three headings (`###`) beneath a date.
- The idea ID is an HTML comment immediately below the theme section.
- The title line is bold and uses exactly `**Status: Title**`.
- The body follows the title line and may contain standard Markdown paragraphs, lists, emphasis, links, or fenced code blocks when useful.

Do not insert another heading level or arbitrary content between a date and its theme, or between an idea ID and its title.

## Dates and chronology

Use a date heading in this exact form:

```markdown
## Wednesday, August 19, 2026
```

Requirements:

- The weekday must be correct for the calendar date.
- Use the full weekday and month names.
- Do not use ISO dates, abbreviated months, or date headings without the weekday.
- A date section may contain multiple themes and multiple ideas.
- Maintain the log in reverse chronological order: newest date first.
- Add a new idea to the section for the date when the ideation actually occurred, when that can be established with reasonable confidence.
- Do not invent exact historical dates. If a date cannot be established, resolve the uncertainty before adding the entry.

Within a date, keep related ideas together under the appropriate theme. Preserve the historical sequence of existing material; do not reorganize the whole log by topic.

## Themes

Every entry must belong to one of these normalized theme headings exactly as written:

- Accessibility
- Asset production
- Audio
- Biography
- Case studies
- Character
- Content
- Environment
- Interaction
- Motion
- Navigation
- Process
- Technology
- Visual world

Use the most specific theme that makes the entry easy to retrieve. Do not create a new theme or silently rename an existing one; unknown themes cause validation failure.

## Statuses

Every entry title starts with one normalized status, followed by a colon, one space, and a descriptive title:

```markdown
**Status: Descriptive title**
```

Use one of these statuses exactly as written:

- Idea
- Exploration
- Experiment
- Reference
- Principle
- Direction
- Promoted
- De-emphasized
- Rejected
- Open Question

Choose the status by the role the entry plays:

- **Idea** — a distinct proposal not yet developed.
- **Exploration** — a possibility being examined without a commitment.
- **Experiment** — a bounded trial intended to reveal something.
- **Reference** — an external work, pattern, or source and the relevant lesson from it.
- **Principle** — a durable guiding rule or preference.
- **Direction** — a developing creative or strategic trajectory.
- **Promoted** — an existing idea that has become more important or committed.
- **De-emphasized** — an existing idea that remains known but is less central.
- **Rejected** — an idea deliberately set aside.
- **Open Question** — an unresolved question that should remain visible.

Do not use an unrecognized status, multiple statuses, a missing title, or a colon without a single following space.

## Permanent idea IDs

Every atomic idea requires one permanent ID in this exact comment format:

```markdown
<!-- idea-id: YYYYMMDD-NNNNNN -->
```

Example:

```markdown
<!-- idea-id: 20260819-000047 -->
```

The first eight digits must match the date section (`YYYYMMDD`). The six-digit suffix is a globally unique sequence number.

ID rules:

- Assign each new idea the next unused global sequence number.
- Never reset the sequence for a new date, theme, or year.
- Never reuse a sequence number, including one from a deleted or retired idea.
- Never change an existing idea ID when revising its title, body, status, theme, or date placement.
- For historical backfill, use the next available sequence number, not a sequence number that would make the historical date appear ordered.
- A sequence gap is valid; do not renumber to close it.
- IDs are the only synchronization key between Markdown and Notion. Titles and body text are not identity.

To find the next sequence number, inspect the highest existing ID in the log or run validation and use the reported `Highest global sequence`. Increment it by one and retain leading zeroes.

## Exact entry spacing

The parser requires this spacing:

```markdown
<!-- idea-id: 20260819-000001 -->

**Principle: Entry title**
```

There must be exactly one blank line between the ID comment and its bold title line. Do not put prose, a list, another ID, or a heading between them.

Place a blank line after the title before the body. Separate entries with blank lines so the Markdown stays readable.

## Adding an entry

1. Identify the actual date, normalized theme, and appropriate status.
2. Confirm whether an existing atomic entry should be revised instead of creating a duplicate.
3. Locate the date section in reverse chronological position, or create it using the required date format.
4. Locate or create the normalized theme heading beneath that date.
5. Assign the next unused permanent global ID, with a date prefix matching the date section.
6. Add the ID comment, one blank line, the bold `Status: Title` line, and the body.
7. Keep the entry atomic and write a body that captures the meaningful thought rather than the full discussion that led to it.
8. Validate the log before treating the edit as complete.

## Revising an existing entry

Revise an existing entry when the original idea remains the same but its wording, status, emphasis, or supporting explanation has changed.

- Keep its permanent ID unchanged.
- Preserve the exact ID-comment and title-line spacing.
- Change the normalized status when the idea's state has genuinely changed.
- Do not add a second entry merely to restate the same idea in updated language.
- Add a separate entry when a new, independently useful thought, test, decision, or question emerges.

The log records an evolving process, so a later `Promoted`, `De-emphasized`, or `Rejected` entry may be appropriate when the evolution itself is worth preserving. Do not rewrite or delete meaningful history merely because the project moved on.

## Rights and reuse footer

The log ends with a `Rights And Reuse` section. It is not an ideation entry and is intentionally excluded from parsing.

Do not place new ideas after that footer. Keep the footer at the end of the document and preserve its content unless the user explicitly asks to change the rights language.

## Validation and generated data

From the repository root, validate the canonical Markdown:

```powershell
python .\tools\ideation_log.py validate
```

This validates:

- date-heading format and weekday accuracy
- date, theme, ID, title, and body hierarchy
- allowed themes and statuses
- required permanent IDs
- unique IDs and unique global sequence numbers
- date-prefix consistency between IDs and date sections
- `Status: Title` formatting
- required blank line between ID and title

When the Markdown has changed and the generated representation should be refreshed, run:

```powershell
python .\tools\ideation_log.py generate
```

This updates `generated/portfolio-ideation.json` deterministically. Never hand-edit that file; correct the Markdown and regenerate it instead.

## Notion synchronization

Notion is a one-way downstream view of the canonical Git-derived ideation records. It must not be used as a parallel authoring source.

After validation and generation, inspect the sync plan first:

```powershell
python .\tools\notion_ideation_sync.py --dry-run
```

Only perform external writes when they are explicitly intended:

```powershell
python .\tools\notion_ideation_sync.py --apply
```

The synchronization matches records solely by permanent `Idea ID`. It does not automatically delete Notion-only records. Do not include credentials in the log, generated JSON, commit messages, or source files.

## Final checklist

Before completing an ideation-log edit, confirm:

- The entry is an atomic ideation record, not a production activity or task.
- Its date heading is accurate and in the required weekday date format.
- Its theme and status use the exact normalized vocabulary.
- Its ID has the correct date prefix and the next unused global sequence.
- The ID comment has one blank line before the bold `Status: Title` line.
- Existing IDs were not changed or reused.
- No idea was placed after `Rights And Reuse`.
- `python .\tools\ideation_log.py validate` succeeds.
- Generated JSON was refreshed only through the generator, when required.
- A Notion sync is dry-run first and applied only with explicit authorization.

## Scope boundaries

Do not edit `portfolio-production-log.md` or `portfolio-change-log.md` while maintaining this file unless the requested work expressly includes them.

The production log records meaningful work performed while making the project. The change log records updates to the live site. This ideation log records the thinking that may shape that work.
