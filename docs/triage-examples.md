# Triage Examples

This page shows how the synthetic routing logic is intended to behave.

## Scheduling Queue

Example pattern:

`I missed the appointment and need to reschedule.`

Expected handling:

- route to `scheduling`
- mark priority `medium`
- allow operational outreach only

## Admin Queue

Example pattern:

`I need help with an insurance form.`

Expected handling:

- route to `admin`
- mark priority `routine`
- allow non-clinical reply

## Clinician Review Queue

Example pattern:

`Symptoms are worsening and I have questions about medication.`

Expected handling:

- route to `clinician-review`
- raise priority
- block outbound guidance until licensed review

## Needs Triage Queue

Example pattern:

`Can someone call me back?`

Expected handling:

- route to `needs-triage`
- treat as ambiguous
- require a human to decide whether this is operational, clinical, or both

## Why This Matters

The routing boundary is the whole point of the repo. In care-team messaging, the risk is usually not that the inbox is empty. The risk is that a mixed operational-clinical message gets treated like a simple admin task.
