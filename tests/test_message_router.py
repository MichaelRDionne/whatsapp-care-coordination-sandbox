from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from message_router import load_messages, route_message, route_messages


class MessageRouterTests(unittest.TestCase):
    def test_worsening_clinical_message_requires_high_priority_review(self) -> None:
        routed = route_message(
            {
                "id": "MSG-001",
                "body": "Synthetic patient reports worsening symptom pattern.",
            }
        )

        self.assertEqual(routed["queue"], "clinician-review")
        self.assertEqual(routed["priority"], "high")
        self.assertIn("No outbound guidance", routed["guardrail"])

    def test_scheduling_message_routes_to_operational_queue(self) -> None:
        routed = route_message(
            {
                "id": "MSG-002",
                "body": "Synthetic message asks to reschedule appointment.",
            }
        )

        self.assertEqual(routed["queue"], "scheduling")
        self.assertEqual(routed["priority"], "medium")
        self.assertIn("Operational outreach only", routed["guardrail"])

    def test_admin_message_routes_to_routine_queue(self) -> None:
        routed = route_message(
            {
                "id": "MSG-003",
                "body": "Synthetic message asks about an insurance form.",
            }
        )

        self.assertEqual(routed["queue"], "admin")
        self.assertEqual(routed["priority"], "routine")

    def test_ambiguous_message_routes_to_human_triage(self) -> None:
        routed = route_message(
            {
                "id": "MSG-004",
                "body": "Synthetic message says please review this when available.",
            }
        )

        self.assertEqual(routed["queue"], "needs-triage")
        self.assertEqual(routed["priority"], "medium")
        self.assertIn("human triage", routed["guardrail"])

    def test_route_messages_sorts_high_before_medium_before_routine(self) -> None:
        routed = route_messages(
            [
                {"id": "MSG-003", "body": "Synthetic insurance form question."},
                {"id": "MSG-001", "body": "Synthetic safety concern."},
                {"id": "MSG-002", "body": "Synthetic missed appointment."},
            ]
        )

        self.assertEqual([item["priority"] for item in routed], ["high", "medium", "routine"])
        self.assertEqual([item["id"] for item in routed], ["MSG-001", "MSG-002", "MSG-003"])

    def test_load_messages_rejects_non_list_json(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as handle:
            json.dump({"id": "MSG-001"}, handle)
            handle.flush()

            with self.assertRaisesRegex(ValueError, "Expected a list"):
                load_messages(handle.name)


if __name__ == "__main__":
    unittest.main()
