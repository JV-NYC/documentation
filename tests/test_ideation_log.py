import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "ideation_log.py"
SPEC = importlib.util.spec_from_file_location("ideation_log", MODULE_PATH)
ideation_log = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = ideation_log
SPEC.loader.exec_module(ideation_log)


def log(*sections: str) -> str:
    return "\n".join(sections) + "\n"


def entry(identifier: str, status_title: str, body: str = "Body.") -> str:
    return f"<!-- idea-id: {identifier} -->\n\n**{status_title}**\n\n{body}"


class IdeationLogTests(unittest.TestCase):
    def assert_invalid(self, text: str, fragment: str) -> None:
        with self.assertRaises(ideation_log.ValidationError) as error:
            ideation_log.parse_and_validate(text)
        self.assertIn(fragment, str(error.exception))

    def test_parses_a_valid_entry(self) -> None:
        summary = ideation_log.parse_and_validate(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Principle — Alive, not animated"))
        )
        self.assertEqual(
            summary.records,
            (
                {
                    "id": "20260819-000001",
                    "date": "2026-08-19",
                    "theme": "Motion",
                    "status": "Principle",
                    "title": "Alive, not animated",
                    "body": "Body.",
                },
            ),
        )

    def test_multiple_entries_under_one_theme(self) -> None:
        summary = ideation_log.parse_and_validate(
            log(
                "## Wednesday, August 19, 2026", "", "### Motion", "",
                entry("20260819-000001", "Principle — First"), "",
                entry("20260819-000002", "Exploration — Second"),
            )
        )
        self.assertEqual([record["title"] for record in summary.records], ["First", "Second"])

    def test_theme_and_date_transitions(self) -> None:
        summary = ideation_log.parse_and_validate(
            log(
                "## Wednesday, August 19, 2026", "", "### Motion", "",
                entry("20260819-000001", "Principle — First"), "",
                "### Audio", "", entry("20260819-000002", "Reference — Second"), "",
                "## Tuesday, August 18, 2026", "", "### Process", "",
                entry("20260818-000003", "Idea — Third"),
            )
        )
        self.assertEqual(
            [(record["date"], record["theme"]) for record in summary.records],
            [("2026-08-19", "Motion"), ("2026-08-19", "Audio"), ("2026-08-18", "Process")],
        )

    def test_preserves_markdown_body(self) -> None:
        body = "First paragraph.\n\n- one\n- two with `code`\n\n> A quote"
        summary = ideation_log.parse_and_validate(
            log("## Wednesday, August 19, 2026", "", "### Process", "", entry("20260819-000001", "Idea — Preserve", body))
        )
        self.assertEqual(summary.records[0]["body"], body)

    def test_rejects_duplicate_full_id(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Idea — First"), "", entry("20260819-000001", "Idea — Second")),
            "duplicate idea-id",
        )

    def test_rejects_duplicate_global_sequence(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Idea — First"), "", "## Tuesday, August 18, 2026", "", "### Motion", "", entry("20260818-000001", "Idea — Second")),
            "duplicate global sequence",
        )

    def test_rejects_malformed_id(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("not-an-id", "Idea — Invalid")),
            "invalid idea-id",
        )

    def test_rejects_missing_id(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", "**Idea — Missing identity**\n\nBody."),
            "missing its required idea-id",
        )

    def test_rejects_date_prefix_mismatch(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260818-000001", "Idea — Wrong date")),
            "has date prefix 2026-08-18",
        )

    def test_rejects_unknown_theme(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Mystery", "", entry("20260819-000001", "Idea — Unknown theme")),
            "unknown theme",
        )

    def test_rejects_unknown_status(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Draft — Unknown status")),
            "unknown status",
        )

    def test_rejects_malformed_status_title_heading(self) -> None:
        self.assert_invalid(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Idea - Wrong separator")),
            "must contain a",
        )

    def test_accepts_historical_backfill_with_later_sequence(self) -> None:
        summary = ideation_log.parse_and_validate(
            log(
                "## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000002", "Idea — Newer"), "",
                "## Monday, August 17, 2026", "", "### Motion", "", entry("20260817-000003", "Idea — Historical"),
            )
        )
        self.assertEqual(summary.highest_sequence, 3)

    def test_accepts_gaps_in_global_sequences(self) -> None:
        summary = ideation_log.parse_and_validate(
            log("## Wednesday, August 19, 2026", "", "### Motion", "", entry("20260819-000001", "Idea — First"), "", entry("20260819-000003", "Idea — Third"))
        )
        self.assertEqual(summary.highest_sequence, 3)


if __name__ == "__main__":
    unittest.main()
