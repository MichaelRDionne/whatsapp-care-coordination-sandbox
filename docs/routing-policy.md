# Routing Policy

This sandbox treats message routing as a human-reviewed workflow, not autonomous clinical action.

## Queues

- `clinician-review`: medication, symptom, lab, safety, or clinical interpretation language.
- `scheduling`: missed visits, appointment coordination, transportation, or callback requests.
- `admin`: billing, forms, insurance, or non-clinical logistics.
- `needs-triage`: ambiguous messages or messages that do not match a safe operational category.

## Guardrails

- Do not send clinical advice automatically.
- Do not close a message with clinical content without clinician review.
- Do not include sensitive identifiers in public logs or demo fixtures.
- Keep examples synthetic, minimal, and easy to audit.
