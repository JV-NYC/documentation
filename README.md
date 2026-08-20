# Portfolio Documentation

This repository contains the durable documentation and supporting tooling for the Portfolio project. It is primarily a **documentation repository**, not the source code for the portfolio website itself. The repository preserves project thinking, production history, and structured ideation in plain Markdown while providing tooling that can validate and transform selected documentation for downstream use.

The current automated pipeline turns the Portfolio Ideation Log into structured data and synchronizes that data into Notion; type content into the log, run the script, populate your Notion page.  

## Core principle

The repository follows a strict source-of-truth hierarchy:

```text
Project work and conversation
        ↓
Local Markdown
        ↓
Git
        ↓
Derived systems
```

Git contains the canonical committed state.

Derived systems such as Notion are downstream representations of that state.

They are not alternate authoring environments.

For the ideation system specifically:

```text
portfolio-ideation-log.md
        ↓
parser + validator
        ↓
generated/portfolio-ideation.json
        ↓
Notion sync
        ↓
Portfolio Ideation database
```

Changes to an idea are made in the Markdown source and committed to Git.

They are not made directly in Notion.

---

# Repository Structure

## `AGENTS.md`

Project-level operating instructions for AI agents and other automated collaborators working in this repository. This file defines relevant conventions, constraints, and expectations for automated work. Agents should read and follow it before changing repository content.

---

## `portfolio-ideation-log.md`

The canonical Portfolio Ideation Log.

This is an ongoing chronological record of:

- ideas
- references
- experiments
- questions
- principles
- emerging directions

The log preserves the evolution of the project rather than rewriting history to match later decisions.

Entries are organized as:

```text
Date
    Theme
        Idea ID
        Status — Title
        Body
```

Example:

```markdown
## Wednesday, August 19, 2026

### Motion

<!-- idea-id: 20260819-000001 -->

**Principle — Alive, not animated**

Alive, not animated. Stillness should be the default state...
```

The Markdown file remains the authored source even though its contents are also represented in Notion.

---

# Permanent Idea IDs

Every atomic ideation entry has a permanent identifier:

```text
YYYYMMDD-NNNNNN
```

Example:

```text
20260819-000001
```

The date represents the historical date of the idea.

The six-digit suffix is a globally unique sequence number.

## ID rules

- The global sequence never resets.
- A sequence number is never reused.
- Existing IDs never change.
- Deleted or retired IDs remain retired.
- Historical backfill receives the next available global sequence number.
- An ID does not change if the title, body, status, theme, or date is later revised.

The permanent `idea-id` is the sole synchronization key used to match Git records with Notion records.

Titles and other mutable content are never used as identity.

---

# Normalized Ideation Themes

The ideation log currently recognizes these themes:

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

Unknown theme values cause validation failure rather than being silently normalized.

---

# Normalized Ideation Statuses

The ideation lifecycle vocabulary is:

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

Not every status must be represented in the current dataset.

---

## `portfolio-production-log.md`

The production record for meaningful work performed while building the Portfolio project. It is intended to document production decisions, experiments, failures, revisions, and milestones. It is not a task manager or a transcript.

The intended case-study structure is:

```text
Problem / Goal
    ↓
Constraint
    ↓
What I did
    ↓
Outcome
    ↓
What I learned
```

---

## `portfolio-production-log-instructions.md`

The authoritative formatting and maintenance instructions for the production log.

Automated collaborators should consult this file before adding or modifying production-log entries.

---

## `portfolio-change-log.md`

Reserved for changes to the live Portfolio site after the site is in production.

It is distinct from the production log.

Production work performed while the site is being built belongs in the production log rather than the change log.

---

# Ideation Tooling

## `tools/ideation_log.py`

Deterministic parser, validator, and JSON generator for `portfolio-ideation-log.md`.

It reads the canonical Markdown structure and produces normalized structured records.

Each record has the shape:

```json
{
  "id": "20260819-000001",
  "date": "2026-08-19",
  "theme": "Motion",
  "status": "Principle",
  "title": "Alive, not animated",
  "body": "..."
}
```

The parser validates source invariants including:

- valid permanent IDs
- unique IDs
- unique global sequence numbers
- date-prefix consistency
- valid date headings
- normalized themes
- normalized statuses
- correctly formed Status / Title lines
- required IDs

The parser does not rewrite or repair source content.

Invalid source data causes validation failure.

### Validate the ideation log

From the repository root:

```powershell
python .\tools\ideation_log.py validate
```

### Generate normalized JSON

```powershell
python .\tools\ideation_log.py generate
```

Repeated generation against unchanged Markdown should produce deterministic output.

---

## `generated/portfolio-ideation.json`

Generated structured representation of the canonical ideation log.

This file is produced by `tools/ideation_log.py`.

It is **derived data**.

Do not edit it manually.

If its contents need to change, modify `portfolio-ideation-log.md` and regenerate the JSON.

The Markdown source remains authoritative.

---

# Notion Synchronization

## `tools/notion_ideation_sync.py`

One-way synchronization client for the Portfolio Ideation Notion database.

The sync reads the generated ideation records and compares them with existing Notion records using permanent `Idea ID`.

The synchronization model is:

```text
Git-derived ideation records
        ↓
match by Idea ID
        ↓
Notion
```

It does not synchronize changes from Notion back into Git.

## Matching

Records are matched only by permanent `Idea ID`.

Example:

```text
20260819-000001
```

If the title or body changes but the ID remains the same, the existing Notion record can be updated rather than duplicated.

---

# Sync Safety

The synchronization client is intentionally conservative.

## Dry run is the default

The sync defaults to planning changes without writing them.

```powershell
python .\tools\notion_ideation_sync.py --dry-run
```

A dry run reports expected:

- creates
- updates
- unchanged records
- duplicates
- errors

It also generates a local diagnostic report.

A typical clean initial import might report:

```text
creates=47
updates=0
unchanged=0
duplicates=0
errors=0
```

After a successful synchronization, a subsequent run against unchanged data should report:

```text
creates=0
updates=0
unchanged=47
duplicates=0
errors=0
```

## Apply changes explicitly

Actual Notion writes require:

```powershell
python .\tools\notion_ideation_sync.py --apply
```

The explicit `--apply` requirement prevents an accidental command invocation from modifying the Notion database.

## No automatic deletion

The V1 sync does not delete Notion-only records.

Git remains authoritative, but destructive reconciliation has intentionally not been implemented.

---

# Notion Configuration

The sync uses local environment configuration.

A template is provided in:

```text
.env.example
```

Copy the template to:

```text
.env
```

and supply the required local Notion values.

The real `.env` file contains secrets and must never be committed.

Do not place credentials directly in:

- Python files
- Markdown files
- JSON
- Git configuration committed to this repository

---

## `.env.example`

Safe template showing the environment variables required by the Notion synchronization tooling.

This file may be committed.

It must contain variable names or safe example values only.

It must never contain the real integration secret.

---

## `.env`

Local credential file.

This file is intentionally ignored by Git.

Never commit it.

---

# Tests

## `tests/test_ideation_log.py`

Automated tests for the Markdown parser and validator.

Coverage includes valid parsing and failure conditions such as:

- malformed IDs
- missing IDs
- duplicate IDs
- duplicate global sequences
- date mismatches
- unknown themes
- unknown statuses
- malformed entry headings
- historical backfill
- valid sequence gaps
- body preservation

---

## `tests/test_notion_ideation_sync.py`

Automated tests for the Notion synchronization client.

Tests cover synchronization planning, matching, API behavior, and safe error handling.

The test suite does not require modifying the canonical ideation log.

---

# Generated and Local Diagnostic Files

The synchronization tooling may create diagnostic output such as:

```text
generated/portfolio-ideation-notion-dry-run.json
```

These files are intended for local inspection and debugging.

They are not canonical project artifacts and are intentionally excluded from Git.

Likewise, temporary error logs and Python-generated files such as:

```text
__pycache__/
*.pyc
```

are not repository content.

---

# Repository Security Model

This repository uses a **deny-by-default Git allowlist**.

The root `.gitignore` begins by ignoring repository contents generally and then explicitly allows only approved files and directories.

The principle is:

> If a file has not been deliberately approved for Git, Git should ignore it.

This differs from the more common approach of tracking everything by default and trying to remember every file that should be excluded.

The allowlist helps prevent accidental commits of:

- credentials
- private working documents
- temporary files
- local diagnostics
- unrelated material
- generated development artifacts

## Important limitation

`.gitignore` only prevents untracked files from being added.

It does not remove files that are already tracked, and it does not erase files from Git history.

Before making this repository public, its complete Git history should be audited for anything that should never have been committed.

---

## `.gitignore`

Defines the repository's deny-by-default tracking policy.

Approved paths are explicitly allowlisted.

Local secrets and transient development files remain ignored.

When adding a new legitimate repository file, remember that it may also need to be explicitly added to the allowlist.

---

## `.gitattributes`

Defines repository text and line-ending behavior.

Text-based project files use normalized LF line endings so the repository behaves consistently across Windows, Codex, GitHub, and other environments.

This prevents environment-specific line-ending behavior from producing unnecessary changes or warnings.

---

# Adding a New Repository File

Because the repository is deny-by-default, creating a file locally does not necessarily make it visible to Git.

When adding a legitimate repository artifact:

1. Create the file.
2. Add an explicit allow rule to `.gitignore` if necessary.
3. Inspect what Git sees.

Use:

```powershell
git status --short
```

Before staging everything, inspect what would be added:

```powershell
git add -n .
```

The `-n` option performs a dry run.

Review this output carefully.

Only then stage the approved files.

---

# Typical Ideation Workflow

## Add or revise ideas

Edit:

```text
portfolio-ideation-log.md
```

Every new atomic idea must receive the next unused permanent global sequence number.

Existing IDs must never be changed.

## Validate

```powershell
python .\tools\ideation_log.py validate
```

## Generate structured records

```powershell
python .\tools\ideation_log.py generate
```

## Inspect Notion changes

```powershell
python .\tools\notion_ideation_sync.py --dry-run
```

## Apply when satisfied

```powershell
python .\tools\notion_ideation_sync.py --apply
```

## Commit and push the canonical state

Git remains the authoritative committed record.

---

# What Notion Is For

Notion provides an exploratory interface over the ideation dataset.

It allows the same records to be viewed through:

- chronological lists
- tables
- status boards
- theme-oriented views
- filtered subsets

The current conceptual visual model is:

```text
Board position / grouping = Status
Card color = Theme
```

This makes it possible to inspect the development of the Portfolio's thinking without sacrificing the durable chronological Markdown record. Notion is a view over the work; it is not the work itself.

---

# Current Status

The current implementation includes:

- canonical Markdown ideation log
- permanent globally unique idea IDs
- deterministic parser
- validation
- normalized JSON generation
- automated parser tests
- one-way Notion synchronization
- dry-run synchronization
- explicit apply mode
- automated sync tests
- deny-by-default Git tracking
- local secret protection
- normalized repository line endings

The synchronization process is currently validated as a manual workflow.

Future work may automate synchronization from the canonical Git state after the manual pipeline and safety rules are considered sufficiently stable.