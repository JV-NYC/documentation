"""Parse and validate the Portfolio ideation log.

The Markdown file remains the source of truth. This module only reads it and
derives normalized records from its explicit structure.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable


ALLOWED_THEMES = frozenset(
    {
        "Accessibility",
        "Asset production",
        "Audio",
        "Biography",
        "Case studies",
        "Character",
        "Content",
        "Environment",
        "Interaction",
        "Motion",
        "Navigation",
        "Process",
        "Technology",
        "Visual world",
    }
)

ALLOWED_STATUSES = frozenset(
    {
        "Idea",
        "Exploration",
        "Experiment",
        "Reference",
        "Principle",
        "Direction",
        "Promoted",
        "De-emphasized",
        "Rejected",
        "Open Question",
    }
)

ID_PATTERN = re.compile(r"^(?P<date>\d{8})-(?P<sequence>\d{6})$")
ID_COMMENT_PATTERN = re.compile(r"^\s*<!--\s*idea-id:\s*(?P<id>.*?)\s*-->\s*$")
ID_COMMENT_MENTION_PATTERN = re.compile(r"idea-id:")
DATE_HEADING_PATTERN = re.compile(r"^##(?!#)\s+(?P<value>.*?)\s*$")
THEME_HEADING_PATTERN = re.compile(r"^###(?!#)\s+(?P<value>.*?)\s*$")
BOLD_LINE_PATTERN = re.compile(r"^\*\*(?P<value>.*?)\*\*\s*$")


@dataclass(frozen=True)
class Issue:
    line: int
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.message}"


class ValidationError(Exception):
    def __init__(self, issues: Iterable[Issue]):
        self.issues = tuple(issues)
        super().__init__("\n".join(str(issue) for issue in self.issues))


@dataclass
class RawIdea:
    raw_id: str | None
    id_line: int | None
    date: str | None
    date_line: int | None
    theme: str | None
    theme_line: int | None
    heading_line: int | None = None
    heading_text: str | None = None
    body_lines: list[str] = field(default_factory=list)


@dataclass
class ParsedLog:
    records: list[RawIdea]
    issues: list[Issue]


@dataclass(frozen=True)
class ValidationSummary:
    records: tuple[dict[str, str], ...]
    highest_sequence: int | None
    themes: tuple[str, ...]
    statuses: tuple[str, ...]


def parse_date_heading(value: str) -> str:
    """Convert a required weekday date heading to an ISO date."""
    try:
        parsed = datetime.strptime(value, "%A, %B %d, %Y")
    except ValueError as error:
        raise ValueError(
            f"date heading {value!r} must use 'Weekday, Month D, YYYY'"
        ) from error

    weekday = value.split(",", 1)[0]
    if parsed.strftime("%A") != weekday:
        raise ValueError(
            f"date heading {value!r} has weekday {weekday!r}, but the date is "
            f"{parsed.strftime('%A')}"
        )
    return parsed.date().isoformat()


def _trim_structural_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def _finish_record(current: RawIdea | None, records: list[RawIdea]) -> None:
    if current is None:
        return
    current.body_lines = _trim_structural_blank_lines(current.body_lines)
    records.append(current)


def _is_canonical_title_line(line: str) -> bool:
    match = BOLD_LINE_PATTERN.match(line)
    return match is not None and " — " in match.group("value")


def parse_ideation_log(text: str) -> ParsedLog:
    """Parse Markdown into raw ideas without validating their vocabulary or IDs."""
    records: list[RawIdea] = []
    issues: list[Issue] = []
    current: RawIdea | None = None
    current_date: str | None = None
    current_date_line: int | None = None
    current_theme: str | None = None
    current_theme_line: int | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        date_match = DATE_HEADING_PATTERN.match(line)
        theme_match = THEME_HEADING_PATTERN.match(line)
        id_match = ID_COMMENT_PATTERN.match(line)

        if date_match:
            _finish_record(current, records)
            current = None
            current_theme = None
            current_theme_line = None
            current_date_line = line_number
            try:
                current_date = parse_date_heading(date_match.group("value"))
            except ValueError as error:
                current_date = None
                issues.append(Issue(line_number, str(error)))
            continue

        if theme_match:
            _finish_record(current, records)
            current = None
            current_theme = theme_match.group("value")
            current_theme_line = line_number
            if current_date is None:
                issues.append(Issue(line_number, "theme heading appears before a valid date heading"))
            continue

        if id_match:
            if current is not None and current.heading_line is None:
                issues.append(
                    Issue(
                        line_number,
                        "multiple idea-id comments appear before the prior idea has a Status — Title heading",
                    )
                )
            _finish_record(current, records)
            current = RawIdea(
                raw_id=id_match.group("id"),
                id_line=line_number,
                date=current_date,
                date_line=current_date_line,
                theme=current_theme,
                theme_line=current_theme_line,
            )
            continue

        if ID_COMMENT_MENTION_PATTERN.search(line):
            issues.append(Issue(line_number, "malformed idea-id comment"))
            continue

        bold_match = BOLD_LINE_PATTERN.match(line)
        if current is not None and current.heading_line is None:
            if not line.strip():
                continue
            current.heading_line = line_number
            current.heading_text = bold_match.group("value") if bold_match else None
            if bold_match is None:
                issues.append(
                    Issue(line_number, "expected a bold Status — Title heading after idea-id")
                )
            continue

        if current is None and bold_match is not None:
            # A standalone bold line directly under a theme is an attempted idea
            # entry, even though it lacks its required permanent identity.
            current = RawIdea(
                raw_id=None,
                id_line=None,
                date=current_date,
                date_line=current_date_line,
                theme=current_theme,
                theme_line=current_theme_line,
                heading_line=line_number,
                heading_text=bold_match.group("value"),
            )
            continue

        if current is not None:
            current.body_lines.append(line)

    _finish_record(current, records)
    return ParsedLog(records=records, issues=issues)


def _parse_status_and_title(record: RawIdea, issues: list[Issue]) -> tuple[str | None, str | None]:
    if record.heading_text is None:
        return None, None
    if " — " not in record.heading_text:
        issues.append(
            Issue(
                record.heading_line or record.id_line or 1,
                "Status — Title heading must contain a ' — ' separator",
            )
        )
        return None, None
    status, title = record.heading_text.split(" — ", 1)
    if not status or not title:
        issues.append(
            Issue(
                record.heading_line or record.id_line or 1,
                "Status — Title heading must include both a status and a title",
            )
        )
        return None, None
    return status, title


def validate_parsed_log(parsed: ParsedLog) -> ValidationSummary:
    """Validate parsed records and return normalized records on success."""
    issues = list(parsed.issues)
    normalized: list[dict[str, str]] = []
    full_ids: dict[str, int] = {}
    sequences: dict[int, int] = {}

    for record in parsed.records:
        location = record.id_line or record.heading_line or record.theme_line or 1
        if record.date is None:
            issues.append(Issue(location, "idea is not contained in a valid date section"))
        if record.theme is None:
            issues.append(Issue(location, "idea is not contained in a theme section"))
        elif record.theme not in ALLOWED_THEMES:
            issues.append(Issue(record.theme_line or location, f"unknown theme {record.theme!r}"))

        if record.raw_id is None:
            issues.append(Issue(location, "idea is missing its required idea-id"))
            id_match = None
        else:
            id_match = ID_PATTERN.match(record.raw_id)
            if id_match is None:
                issues.append(Issue(record.id_line or location, f"invalid idea-id {record.raw_id!r}"))
            else:
                try:
                    id_date = datetime.strptime(id_match.group("date"), "%Y%m%d").date().isoformat()
                except ValueError:
                    id_date = None
                    issues.append(
                        Issue(record.id_line or location, f"idea-id {record.raw_id!r} has an invalid date prefix")
                    )
                if record.date is not None and id_date is not None and id_date != record.date:
                    issues.append(
                        Issue(
                            record.id_line or location,
                            f"idea-id {record.raw_id!r} has date prefix {id_date}, "
                            f"but its section date is {record.date}",
                        )
                    )
                if record.raw_id in full_ids:
                    issues.append(
                        Issue(
                            record.id_line or location,
                            f"duplicate idea-id {record.raw_id!r}; first used on line {full_ids[record.raw_id]}",
                        )
                    )
                else:
                    full_ids[record.raw_id] = record.id_line or location

                sequence = int(id_match.group("sequence"))
                if sequence in sequences:
                    issues.append(
                        Issue(
                            record.id_line or location,
                            f"duplicate global sequence {sequence:06d}; first used on line {sequences[sequence]}",
                        )
                    )
                else:
                    sequences[sequence] = record.id_line or location

        status, title = _parse_status_and_title(record, issues)
        if status is not None and status not in ALLOWED_STATUSES:
            issues.append(Issue(record.heading_line or location, f"unknown status {status!r}"))

        if (
            record.id_line is not None
            and record.heading_line is not None
            and record.heading_line - record.id_line != 2
        ):
            issues.append(
                Issue(
                    record.id_line,
                    "idea-id must be followed by one blank line and then its Status — Title heading",
                )
            )

        if (
            record.raw_id is not None
            and record.date is not None
            and record.theme is not None
            and status is not None
            and title is not None
            and id_match is not None
        ):
            normalized.append(
                {
                    "id": record.raw_id,
                    "date": record.date,
                    "theme": record.theme,
                    "status": status,
                    "title": title,
                    "body": "\n".join(record.body_lines),
                }
            )

    if issues:
        raise ValidationError(issues)

    return ValidationSummary(
        records=tuple(normalized),
        highest_sequence=max(sequences, default=None),
        themes=tuple(sorted({record["theme"] for record in normalized})),
        statuses=tuple(sorted({record["status"] for record in normalized})),
    )


def parse_and_validate(text: str) -> ValidationSummary:
    return validate_parsed_log(parse_ideation_log(text))


def _format_summary(summary: ValidationSummary) -> str:
    highest = f"{summary.highest_sequence:06d}" if summary.highest_sequence is not None else "none"
    return "\n".join(
        (
            "Validation succeeded.",
            f"Total ideas: {len(summary.records)}",
            f"Unique IDs: {len(summary.records)}",
            f"Highest global sequence: {highest}",
            f"Themes represented: {', '.join(summary.themes) or 'none'}",
            f"Statuses represented: {', '.join(summary.statuses) or 'none'}",
        )
    )


def main(argv: list[str] | None = None) -> int:
    repository_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Parse and validate the Portfolio ideation log.")
    parser.add_argument("command", choices=("validate", "generate"))
    parser.add_argument(
        "--source",
        type=Path,
        default=repository_root / "portfolio-ideation-log.md",
        help="Markdown log to read (default: portfolio-ideation-log.md)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=repository_root / "generated" / "portfolio-ideation.json",
        help="Generated JSON path for the generate command",
    )
    args = parser.parse_args(argv)

    try:
        summary = parse_and_validate(args.source.read_text(encoding="utf-8"))
    except OSError as error:
        print(f"Could not read {args.source}: {error}", file=sys.stderr)
        return 2
    except ValidationError as error:
        print("Validation failed:", file=sys.stderr)
        for issue in error.issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    if args.command == "generate":
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(summary.records, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as error:
            print(f"Could not write {args.output}: {error}", file=sys.stderr)
            return 2
        print(f"Wrote {args.output}")

    print(_format_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
