# WhatsApp Care Coordination Sandbox

Synthetic care-team message routing demo for healthcare operations.

This project demonstrates how a lightweight AI-assisted routing layer can turn unstructured team messages into human-reviewed queues: missed visit outreach, refill routing, lab follow-up, scheduling barriers, and escalation review.

## What It Shows

- Synthetic message fixtures with no phone numbers or real identities.
- Rule-based routing that mirrors the structure an AI classifier could support.
- Human-review guardrails for clinical, urgent, or ambiguous messages.
- A simple queue output that separates operational tasks from clinician review.

## Safety Boundary

This is a synthetic demo. It contains no real messages, no patient identifiers, no phone numbers, and no production care-team data. It should not send messages, make clinical decisions, or replace clinician judgment.

## Run The Demo

```bash
python3 examples/run_demo.py
```

## Project Structure

```text
synthetic-data/messages.json  synthetic message examples
src/message_router.py         routing logic
docs/routing-policy.md        human-review policy
examples/run_demo.py          runnable demo
```
