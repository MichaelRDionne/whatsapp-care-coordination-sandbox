from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CLINICIAN_TERMS = ("symptom", "medication", "lab", "worsening", "safety")
SCHEDULING_TERMS = ("missed", "reschedule", "appointment", "call back")
ADMIN_TERMS = ("billing", "insurance", "form")


def load_messages(path: str | Path) -> list[dict[str, Any]]:
    with Path(path).open("r", encoding="utf-8") as handle:
        messages = json.load(handle)
    if not isinstance(messages, list):
        raise ValueError("Expected a list of synthetic messages")
    return messages


def route_message(message: dict[str, str]) -> dict[str, str]:
    body = message["body"].lower()

    if any(term in body for term in CLINICIAN_TERMS):
        queue = "clinician-review"
        priority = "high" if "worsening" in body or "safety" in body else "medium"
        guardrail = "No outbound guidance until a licensed clinician reviews the message."
    elif any(term in body for term in SCHEDULING_TERMS):
        queue = "scheduling"
        priority = "medium"
        guardrail = "Operational outreach only; no clinical advice."
    elif any(term in body for term in ADMIN_TERMS):
        queue = "admin"
        priority = "routine"
        guardrail = "Administrative response allowed if no clinical content is added."
    else:
        queue = "needs-triage"
        priority = "medium"
        guardrail = "Ambiguous message requires human triage."

    return {
        "id": message["id"],
        "queue": queue,
        "priority": priority,
        "guardrail": guardrail,
    }


def route_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    order = {"high": 0, "medium": 1, "routine": 2}
    routed = [route_message(message) for message in messages]
    return sorted(routed, key=lambda item: order[item["priority"]])
