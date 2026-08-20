import importlib.util
import io
import os
import sys
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "notion_ideation_sync.py"
SPEC = importlib.util.spec_from_file_location("notion_ideation_sync", MODULE_PATH)
notion_sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = notion_sync
SPEC.loader.exec_module(notion_sync)


def record(**changes):
    base = {
        "id": "20260819-000001",
        "date": "2026-08-19",
        "theme": "Motion",
        "status": "Principle",
        "title": "Alive, not animated",
        "body": "First paragraph.\n\nSecond paragraph.",
    }
    base.update(changes)
    return base


def page(**changes):
    base = {
        "page_id": "page-1",
        "title": "Alive, not animated",
        "date": "2026-08-19",
        "theme": "Motion",
        "status": "Principle",
        "idea_id": "20260819-000001",
        "body": ("First paragraph.", "Second paragraph."),
    }
    base.update(changes)
    return notion_sync.NotionPage(**base)


class FakeNotionClient:
    def __init__(self, pages):
        self.pages = pages
        self.creates = []
        self.updates = []

    def list_pages(self):
        return self.pages

    def create_page(self, source_record):
        self.creates.append(source_record)

    def update_page(self, page_id, source_record, replace_body):
        self.updates.append((page_id, source_record, replace_body))


class NotionIdeationSyncTests(unittest.TestCase):
    def test_json_http_error_reports_notion_details_without_credentials(self):
        headers = Message()
        headers["X-Request-Id"] = "header-request-id"
        error = HTTPError(
            "https://api.notion.com/v1/databases/database-1",
            400,
            "Bad Request",
            headers,
            io.BytesIO(
                b'{"object":"error","status":400,"code":"validation_error",'
                b'"message":"The database ID is invalid."}'
            ),
        )
        client = notion_sync.HttpNotionClient("secret-token", "database-1")

        with patch.object(notion_sync, "urlopen", side_effect=error):
            with self.assertRaises(notion_sync.SyncError) as raised:
                client._request("GET", "/databases/database-1")

        message = str(raised.exception)
        self.assertIn("HTTP 400", message)
        self.assertIn("code=validation_error", message)
        self.assertIn("message=The database ID is invalid.", message)
        self.assertIn("request_id=header-request-id", message)
        self.assertNotIn("secret-token", message)

    def test_non_json_http_error_falls_back_without_echoing_body(self):
        error = HTTPError(
            "https://api.notion.com/v1/databases/database-1",
            502,
            "Bad Gateway",
            Message(),
            io.BytesIO(b"<html>gateway error</html>"),
        )
        client = notion_sync.HttpNotionClient("secret-token", "database-1")

        with patch.object(notion_sync, "urlopen", side_effect=error):
            with self.assertRaises(notion_sync.SyncError) as raised:
                client._request("GET", "/databases/database-1")

        message = str(raised.exception)
        self.assertIn("HTTP 502", message)
        self.assertIn("response body was not JSON", message)
        self.assertNotIn("gateway error", message)
        self.assertNotIn("secret-token", message)

    def test_absent_idea_id_is_a_create(self):
        plan = notion_sync.build_sync_plan([record()], [])
        self.assertEqual(plan.operations[0].action, "create")

    def test_changed_canonical_field_is_an_update(self):
        plan = notion_sync.build_sync_plan([record(title="New title")], [page()])
        operation = plan.operations[0]
        self.assertEqual(operation.action, "update")
        self.assertEqual(operation.changed_fields, ("title",))
        self.assertFalse(operation.body_changed)

    def test_matching_page_is_unchanged(self):
        plan = notion_sync.build_sync_plan([record()], [page()])
        self.assertEqual(plan.operations[0].action, "unchanged")

    def test_duplicate_idea_id_is_detected(self):
        plan = notion_sync.build_sync_plan([record()], [page(), page(page_id="page-2")])
        self.assertEqual(plan.duplicate_ids, ("20260819-000001",))
        with self.assertRaises(notion_sync.DuplicateIdeaIdError):
            notion_sync.synchronize([record()], FakeNotionClient([page(), page(page_id="page-2")]), dry_run=True)

    def test_body_becomes_plain_ordered_paragraphs(self):
        self.assertEqual(
            notion_sync.body_to_paragraphs(" First.\n\n  Second with *Markdown*. \n\nThird. "),
            ["First.", "Second with *Markdown*.", "Third."],
        )

    def test_changed_body_requires_replacement(self):
        plan = notion_sync.build_sync_plan([record(body="Different.")], [page()])
        operation = plan.operations[0]
        self.assertEqual(operation.action, "update")
        self.assertTrue(operation.body_changed)

    def test_notion_only_page_is_not_planned_for_deletion(self):
        plan = notion_sync.build_sync_plan([record()], [page(idea_id="20260819-000999")])
        self.assertEqual([operation.action for operation in plan.operations], ["create"])

    def test_dry_run_makes_no_writes_and_is_idempotent(self):
        client = FakeNotionClient([page()])
        first = notion_sync.synchronize([record()], client, dry_run=True)
        second = notion_sync.synchronize([record()], client, dry_run=True)
        self.assertEqual(first, second)
        self.assertEqual(first.operations[0].action, "unchanged")
        self.assertEqual(client.creates, [])
        self.assertEqual(client.updates, [])

    def test_local_env_does_not_override_existing_values(self):
        previous = os.environ.get("NOTION_PORTFOLIO_IDEATION_TOKEN")
        try:
            os.environ["NOTION_PORTFOLIO_IDEATION_TOKEN"] = "existing"
            with tempfile.TemporaryDirectory() as directory:
                env_path = Path(directory) / ".env"
                env_path.write_text("NOTION_PORTFOLIO_IDEATION_TOKEN=from-file\n", encoding="utf-8")
                notion_sync.load_local_env(env_path)
            self.assertEqual(os.environ["NOTION_PORTFOLIO_IDEATION_TOKEN"], "existing")
        finally:
            if previous is None:
                os.environ.pop("NOTION_PORTFOLIO_IDEATION_TOKEN", None)
            else:
                os.environ["NOTION_PORTFOLIO_IDEATION_TOKEN"] = previous

    def test_http_client_resolves_and_queries_the_single_data_source(self):
        client = notion_sync.HttpNotionClient("test-token", "database-1")
        calls = []

        def request(method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if endpoint == "/databases/database-1":
                return {"data_sources": [{"id": "source-1"}]}
            if endpoint == "/data_sources/source-1":
                return {
                    "properties": {
                        "Title": {"type": "title"},
                        "Date": {"type": "date"},
                        "Theme": {"type": "select", "select": {"options": [{"name": value} for value in notion_sync.ALLOWED_THEMES]}},
                        "Status": {"type": "select", "select": {"options": [{"name": value} for value in notion_sync.ALLOWED_STATUSES]}},
                        "Idea ID": {"type": "rich_text"},
                    }
                }
            if endpoint == "/data_sources/source-1/query":
                return {"results": [], "has_more": False}
            self.fail(f"Unexpected request: {method} {endpoint}")

        client._request = request
        self.assertEqual(client.list_pages(), [])
        self.assertEqual(
            [endpoint for _, endpoint, _ in calls],
            ["/databases/database-1", "/data_sources/source-1", "/data_sources/source-1/query"],
        )


if __name__ == "__main__":
    unittest.main()
