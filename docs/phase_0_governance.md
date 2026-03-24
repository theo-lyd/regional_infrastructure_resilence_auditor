# Phase 0: Project Framing and Governance

## Purpose

Phase 0 defines project truth before any heavy coding starts.
In public-sector work, this is essential because unclear scope and undefined KPIs often create policy risk later.

## What Was Implemented

- project objective and positioning
- target user definition
- policy-relevant research questions
- explicit in-scope/out-of-scope boundaries
- KPI framework across childcare, youth welfare, and hospital infrastructure
- technical principles for reproducibility and traceability

## How It Was Implemented

Documentation artifacts:
- `project_brief.md`
- `scope.md`
- `methodology.md`

Process used:
1. Convert high-level problem statement into measurable research questions.
2. Convert research questions into KPI categories.
3. Define technical principles that later phases must obey.
4. Record exclusions to prevent scope creep and non-defensible claims.

## Why It Matters

- protects against ambiguous policy interpretation
- creates a defensible boundary for stakeholder expectation management
- ensures engineering outputs map to business questions
- provides a stable baseline for CI tests and dashboard acceptance criteria

## Often-Overlooked Details

- Out-of-scope items are not optional; they are risk controls.
- KPI names should be stable early to avoid dashboard and dbt churn.
- "Predictive" in public sector should default to transparent methods, not black-box complexity.
- Governance docs should be updated with every major metric logic change.

## Evidence Checklist (Defense Ready)

- Can a reviewer identify exactly what the project does not claim?
- Are KPI categories mapped to real policy questions?
- Is there a documented success criterion per major output area?
- Are reproducibility principles explicit and testable?

## Exit Criteria for Phase Completion

- governance docs present in version control
- scope boundaries accepted and explicit
- baseline KPI framework documented
- technical principles documented and referenced by later phases
