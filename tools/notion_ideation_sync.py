"""Synchronize Git-derived Portfolio ideation records to Notion.

The Markdown log and its generated JSON remain authoritative. Notion is a
downstream display of that data, and matching is always by permanent Idea ID.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ideation_log import ALLOWED_STATUSES, ALLOWED_THEMES


API_BASE_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2026-03-11"
REQUIRED_FIELDS = ("id", "date", "theme", "status", "title", "body")
PROPERTY_NAMES = {
    "id": "Idea ID",
    "date": "Date",
    "theme": "Theme",
    "status": "Status",
    "title": "Title",
}
PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n")


class SyncError(Exception):
    """Raised when the source data or Notion response is unsafe to sync."""


class DuplicateIdeaIdError(SyncError):
    """Raised when more than one Notion page shares a canonical Idea ID."""

    def __init__(self, idea_ids: Iterable[str]):
        self.idea_ids = tuple(sorted(idea_ids))
        super().__init__("Duplicate Idea ID in Notion: " + ", ".join(self.idea_ids))


@dataclass(frozen=True)
class NotionPage:
    page_id: str
    title: str
    date: str | None
    theme: str | None
    status: str | None
    idea_id: str | None
    body: tuple[str, ...]


@dataclass(frozen=True)
class PlannedOperation:
    action: str
    record: dict[str, str]
    page_id: str | None = None
    changed_fields: tuple[str, ...] = ()
    body_changed: bool = False

    def as_report(self) -> dict[str, Any]:
        return {
            "id": self.record["id"],
            "action": self.action,
            "title": self.record["title"],
            "date": self.record["date"],
            "theme": self.record["theme"],
            "status": self.record["status"],
            "body_paragraphs": body_to_paragraphs(self.record["body"]),
            "changed_fields": list(self.changed_fields),
            "body_changed": self.body_changed,
        }


@dataclass(frozen=True)
class SyncPlan:
    operations: tuple[PlannedOperation, ...]
    duplicate_ids: tuple[str, ...]

    def report(self) -> dict[str, Any]:
        counts = {"creates": 0, "updates": 0, "unchanged": 0}
        for operation in self.operations:
            counts[operation.action + "s" if operation.action != "unchanged" else "unchanged"] += 1
        return {
            "summary": {
                **counts,
                "duplicates": len(self.duplicate_ids),
                "errors": len(self.duplicate_ids),
            },
            "duplicate_ids": list(self.duplicate_ids),
            "records": [operation.as_report() for operation in self.operations],
        }


class NotionClient(Protocol):
    def list_pages(self) -> list[NotionPage]: ...

    def create_page(self, record: dict[str, str]) -> None: ...

    def update_page(self, page_id: str, record: dict[str, str], replace_body: bool) -> None: ...


def body_to_paragraphs(body: str) -> list[str]:
    """Split body text at blank lines without interpreting Markdown syntax."""
    if not body.strip():
        return []
    return [paragraph.strip() for paragraph in PARAGRAPH_BREAK.split(body.strip()) if paragraph.strip()]


def load_normalized_records(path: Path) -> list[dict[str, str]]:
    """Read and validate the generated JSON before it can reach Notion."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise SyncError(f"Could not read normalized JSON {path}: {error}") from error
    except json.JSONDecodeError as error:
        raise SyncError(f"Normalized JSON {path} is invalid: {error}") from error

    if not isinstance(payload, list):
        raise SyncError("Normalized JSON must contain a list of records")

    seen_ids: set[str] = set()
    records: list[dict[str, str]] = []
    for index, raw_record in enumerate(payload, start=1):
        if not isinstance(raw_record, dict) or set(raw_record) != set(REQUIRED_FIELDS):
            raise SyncError(f"Record {index} must contain exactly: {', '.join(REQUIRED_FIELDS)}")
        if any(not isinstance(raw_record[field], str) for field in REQUIRED_FIELDS):
            raise SyncError(f"Record {index} fields must all be strings")
        record = {field: raw_record[field] for field in REQUIRED_FIELDS}
        if record["id"] in seen_ids:
            raise SyncError(f"Normalized JSON contains duplicate Idea ID {record['id']}")
        if record["theme"] not in ALLOWED_THEMES:
            raise SyncError(f"Record {record['id']} has unknown theme {record['theme']!r}")
        if record["status"] not in ALLOWED_STATUSES:
            raise SyncError(f"Record {record['id']} has unknown status {record['status']!r}")
        seen_ids.add(record["id"])
        records.append(record)
    return records


def build_sync_plan(records: Iterable[dict[str, str]], pages: Iterable[NotionPage]) -> SyncPlan:
    """Make a deterministic create, update, or unchanged decision for each record."""
    pages_by_idea_id: dict[str, list[NotionPage]] = {}
    for page in pages:
        if page.idea_id:
            pages_by_idea_id.setdefault(page.idea_id, []).append(page)

    record_list = list(records)
    canonical_ids = {record["id"] for record in record_list}
    duplicates = tuple(
        idea_id
        for idea_id, matching_pages in pages_by_idea_id.items()
        if idea_id in canonical_ids and len(matching_pages) > 1
    )
    if duplicates:
        return SyncPlan(operations=(), duplicate_ids=tuple(sorted(duplicates)))

    operations: list[PlannedOperation] = []
    for record in record_list:
        matches = pages_by_idea_id.get(record["id"], [])
        if not matches:
            operations.append(PlannedOperation("create", record))
            continue

        page = matches[0]
        changed_fields = tuple(
            field
            for field in ("title", "date", "theme", "status", "id")
            if getattr(page, "idea_id" if field == "id" else field) != record[field]
        )
        body_changed = page.body != tuple(body_to_paragraphs(record["body"]))
        action = "update" if changed_fields or body_changed else "unchanged"
        operations.append(
            PlannedOperation(
                action,
                record,
                page_id=page.page_id,
                changed_fields=changed_fields,
                body_changed=body_changed,
            )
        )
    return SyncPlan(operations=tuple(operations), duplicate_ids=())


def make_paragraph_blocks(body: str) -> list[dict[str, Any]]:
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": paragraph}}]},
        }
        for paragraph in body_to_paragraphs(body)
    ]


def notion_properties(record: dict[str, str]) -> dict[str, Any]:
    return {
        PROPERTY_NAMES["title"]: {"title": [{"type": "text", "text": {"content": record["title"]}}]},
        PROPERTY_NAMES["date"]: {"date": {"start": record["date"]}},
        PROPERTY_NAMES["theme"]: {"select": {"name": record["theme"]}},
        PROPERTY_NAMES["status"]: {"select": {"name": record["status"]}},
        PROPERTY_NAMES["id"]: {"rich_text": [{"type": "text", "text": {"content": record["id"]}}]},
    }


def synchronize(records: list[dict[str, str]], client: NotionClient, dry_run: bool) -> SyncPlan:
    """Query Notion, plan changes, and optionally apply only planned Git-derived changes."""
    plan = build_sync_plan(records, client.list_pages())
    if plan.duplicate_ids:
        raise DuplicateIdeaIdError(plan.duplicate_ids)
    if dry_run:
        return plan

    for operation in plan.operations:
        if operation.action == "create":
            client.create_page(operation.record)
        elif operation.action == "update":
            assert operation.page_id is not None
            client.update_page(operation.page_id, operation.record, operation.body_changed)
    return plan


def _plain_text(rich_text: Any) -> str:
    if not isinstance(rich_text, list):
        return ""
    return "".join(str(item.get("plain_text", "")) for item in rich_text if isinstance(item, dict))


def _notion_http_error_details(error: HTTPError) -> str:
    """Return safe, useful Notion error fields without exposing request credentials."""
    request_id: str | None = None
    headers = error.headers
    if headers is not None:
        request_id = headers.get("x-request-id") or headers.get("request-id")

    try:
        body = error.read().decode("utf-8", errors="replace")
    except OSError:
        body = ""

    try:
        payload = json.loads(body) if body else None
    except json.JSONDecodeError:
        payload = None

    details = [f"HTTP {error.code}"]
    if isinstance(payload, dict):
        code = payload.get("code")
        message = payload.get("message")
        body_request_id = payload.get("request_id")
        if isinstance(code, str) and code:
            details.append(f"code={code}")
        if isinstance(message, str) and message:
            details.append(f"message={message}")
        if isinstance(body_request_id, str) and body_request_id:
            request_id = body_request_id
    elif body:
        details.append("response body was not JSON")

    if request_id:
        details.append(f"request_id={request_id}")
    return "; ".join(details)


class HttpNotionClient:
    """Small Notion API client kept dependency-free for local use and tests."""

    def __init__(self, token: str, database_id: str) -> None:
        self.token = token
        self.database_id = database_id
        self.data_source_id: str | None = None

    def _request(self, method: str, endpoint: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            API_BASE_URL + endpoint,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(request) as response:
                response_payload = response.read().decode("utf-8")
        except HTTPError as error:
            raise SyncError(f"Notion API request failed: {_notion_http_error_details(error)}") from error
        except URLError as error:
            raise SyncError(f"Could not connect to Notion: {error.reason}") from error
        try:
            parsed = json.loads(response_payload) if response_payload else {}
        except json.JSONDecodeError as error:
            raise SyncError("Notion API returned invalid JSON") from error
        if not isinstance(parsed, dict):
            raise SyncError("Notion API returned an unexpected response")
        return parsed

    def _list_child_blocks(self, page_id: str) -> list[dict[str, Any]]:
        blocks: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            suffix = f"?page_size=100{('&start_cursor=' + cursor) if cursor else ''}"
            response = self._request("GET", f"/blocks/{page_id}/children{suffix}")
            results = response.get("results")
            if not isinstance(results, list):
                raise SyncError(f"Notion page {page_id} has an invalid blocks response")
            blocks.extend(block for block in results if isinstance(block, dict))
            if not response.get("has_more"):
                return blocks
            cursor = response.get("next_cursor")
            if not isinstance(cursor, str) or not cursor:
                raise SyncError(f"Notion page {page_id} reports more blocks without a cursor")

    def _resolve_data_source(self) -> str:
        if self.data_source_id is not None:
            return self.data_source_id
        database = self._request("GET", f"/databases/{self.database_id}")
        data_sources = database.get("data_sources")
        if not isinstance(data_sources, list) or len(data_sources) != 1:
            raise SyncError(
                "Portfolio Ideation database must contain exactly one data source for V1 synchronization"
            )
        source = data_sources[0]
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            raise SyncError("Portfolio Ideation database returned an invalid data source")
        self.data_source_id = source["id"]
        self._validate_data_source_schema()
        return self.data_source_id

    def _validate_data_source_schema(self) -> None:
        assert self.data_source_id is not None
        source = self._request("GET", f"/data_sources/{self.data_source_id}")
        properties = source.get("properties")
        if not isinstance(properties, dict):
            raise SyncError("Portfolio Ideation data source returned an invalid properties schema")
        expected_types = {
            PROPERTY_NAMES["title"]: "title",
            PROPERTY_NAMES["date"]: "date",
            PROPERTY_NAMES["theme"]: "select",
            PROPERTY_NAMES["status"]: "select",
            PROPERTY_NAMES["id"]: "rich_text",
        }
        for name, expected_type in expected_types.items():
            property_schema = properties.get(name)
            if not isinstance(property_schema, dict) or property_schema.get("type") != expected_type:
                raise SyncError(f"Portfolio Ideation data source needs a {expected_type} property named {name!r}")
        self._validate_select_options(properties, PROPERTY_NAMES["theme"], ALLOWED_THEMES)
        self._validate_select_options(properties, PROPERTY_NAMES["status"], ALLOWED_STATUSES)

    @staticmethod
    def _validate_select_options(properties: dict[str, Any], name: str, expected: Iterable[str]) -> None:
        select_schema = properties[name].get("select")
        options = select_schema.get("options") if isinstance(select_schema, dict) else None
        option_names = {
            option.get("name") for option in options if isinstance(option, dict) and isinstance(option.get("name"), str)
        } if isinstance(options, list) else set()
        missing = sorted(set(expected) - option_names)
        if missing:
            raise SyncError(f"Portfolio Ideation {name!r} select is missing canonical option(s): {', '.join(missing)}")

    def _page_from_response(self, page: dict[str, Any]) -> NotionPage:
        page_id = page.get("id")
        properties = page.get("properties")
        if not isinstance(page_id, str) or not isinstance(properties, dict):
            raise SyncError("Notion database returned a page without id or properties")

        def property_value(name: str) -> dict[str, Any]:
            value = properties.get(name)
            if not isinstance(value, dict):
                raise SyncError(f"Notion page {page_id} is missing required property {name!r}")
            return value

        title = _plain_text(property_value(PROPERTY_NAMES["title"]).get("title"))
        date_value = property_value(PROPERTY_NAMES["date"]).get("date")
        date = date_value.get("start") if isinstance(date_value, dict) else None
        theme_value = property_value(PROPERTY_NAMES["theme"]).get("select")
        status_value = property_value(PROPERTY_NAMES["status"]).get("select")
        body_blocks = self._list_child_blocks(page_id)
        body: list[str] = []
        for block in body_blocks:
            if block.get("type") != "paragraph":
                return NotionPage(page_id, title, date, _select_name(theme_value), _select_name(status_value), _plain_text(property_value(PROPERTY_NAMES["id"]).get("rich_text")), ("__NON_PARAGRAPH_BLOCK__",))
            paragraph = block.get("paragraph")
            if not isinstance(paragraph, dict):
                raise SyncError(f"Notion page {page_id} has an invalid paragraph block")
            body.append(_plain_text(paragraph.get("rich_text")))
        return NotionPage(
            page_id, title, date, _select_name(theme_value), _select_name(status_value),
            _plain_text(property_value(PROPERTY_NAMES["id"]).get("rich_text")), tuple(body),
        )

    def list_pages(self) -> list[NotionPage]:
        pages: list[NotionPage] = []
        data_source_id = self._resolve_data_source()
        cursor: str | None = None
        while True:
            request_payload: dict[str, Any] = {"page_size": 100}
            if cursor:
                request_payload["start_cursor"] = cursor
            response = self._request("POST", f"/data_sources/{data_source_id}/query", request_payload)
            results = response.get("results")
            if not isinstance(results, list):
                raise SyncError("Notion database query returned an invalid results list")
            pages.extend(self._page_from_response(page) for page in results if isinstance(page, dict))
            if not response.get("has_more"):
                return pages
            cursor = response.get("next_cursor")
            if not isinstance(cursor, str) or not cursor:
                raise SyncError("Notion database query reports more pages without a cursor")

    def create_page(self, record: dict[str, str]) -> None:
        data_source_id = self._resolve_data_source()
        self._request(
            "POST", "/pages",
            {
                "parent": {"type": "data_source_id", "data_source_id": data_source_id},
                "properties": notion_properties(record),
                "children": make_paragraph_blocks(record["body"]),
            },
        )

    def update_page(self, page_id: str, record: dict[str, str], replace_body: bool) -> None:
        update_payload: dict[str, Any] = {"properties": notion_properties(record)}
        if replace_body:
            update_payload["erase_content"] = True
        self._request("PATCH", f"/pages/{page_id}", update_payload)
        if not replace_body:
            return
        blocks = make_paragraph_blocks(record["body"])
        for start in range(0, len(blocks), 100):
            self._request("PATCH", f"/blocks/{page_id}/children", {"children": blocks[start:start + 100]})


def _select_name(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, dict) or not isinstance(value.get("name"), str):
        raise SyncError("Notion select property has an invalid value")
    return value["name"]


def _write_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_local_env(path: Path) -> None:
    """Load simple KEY=value entries without overriding explicitly set variables."""
    if not path.is_file():
        return
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise SyncError(f"Could not read local environment file {path}: {error}") from error
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise SyncError(f"Invalid .env entry on line {line_number}")
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise SyncError(f"Invalid .env entry on line {line_number}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Synchronize generated Portfolio ideation JSON to Notion.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Plan changes without writing to Notion (the default).")
    mode.add_argument("--apply", action="store_true", help="Apply planned changes to Notion.")
    parser.add_argument("--input", type=Path, default=root / "generated" / "portfolio-ideation.json")
    parser.add_argument("--report", type=Path, default=root / "generated" / "portfolio-ideation-notion-dry-run.json")
    args = parser.parse_args(argv)

    try:
        records = load_normalized_records(args.input)
        load_local_env(root / ".env")
        token = os.environ.get("NOTION_PORTFOLIO_IDEATION_TOKEN")
        database_id = os.environ.get("NOTION_PORTFOLIO_IDEATION_DATABASE_ID")
        if not token or not database_id:
            raise SyncError("Set NOTION_PORTFOLIO_IDEATION_TOKEN and NOTION_PORTFOLIO_IDEATION_DATABASE_ID before syncing")
        plan = synchronize(records, HttpNotionClient(token, database_id), dry_run=not args.apply)
        report = plan.report()
        if not args.apply:
            _write_report(args.report, report)
            print(f"Dry-run report: {args.report}")
        summary = report["summary"]
        print("Sync summary: " + ", ".join(f"{key}={value}" for key, value in summary.items()))
        return 0
    except DuplicateIdeaIdError as error:
        report = {"summary": {"creates": 0, "updates": 0, "unchanged": 0, "duplicates": len(error.idea_ids), "errors": len(error.idea_ids)}, "duplicate_ids": list(error.idea_ids), "records": []}
        if not args.apply:
            _write_report(args.report, report)
        print(str(error), file=sys.stderr)
        return 1
    except SyncError as error:
        print(f"Sync failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
