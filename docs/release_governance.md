# Release Governance

This document defines release controls for analytics, modeling, and dashboard changes.

## 1. Versioning Policy

Use semantic-style release tags:
1. major: breaking KPI/model contract changes
2. minor: backward-compatible feature additions
3. patch: bug fixes and documentation-only clarifications

## 2. Release Cadence

1. operational patch releases: as needed
2. planned analytics releases: monthly
3. KPI logic review release: quarterly

## 3. Required Release Checklist

Before release:
1. pipeline run completes end to end
2. dbt tests pass
3. SLA monitor run is captured
4. docs index and capability register updated
5. release note created under `docs/releases/`

## 4. Release Notes Template

Create one markdown file per release in `docs/releases/`:

- release version
- release date
- summary of changes
- data-model impacts
- dashboard impacts
- monitoring/alerting impacts
- known limitations and follow-up actions

## 5. Breaking Change Rules

Treat as breaking changes when:
1. KPI formulas are changed
2. metric names/meanings are changed
3. dashboard interpretation guidance changes materially
4. schema contracts for downstream consumers are changed

## 6. Approval Roles

1. Data Engineer / Analytics Engineer: technical sign-off
2. Analytics Owner: metric and interpretation sign-off
3. Stakeholder Liaison: communication sign-off for policy consumers

## 7. Traceability Requirements

1. every release maps to commit hash and changelog entry
2. release note links to updated docs
3. unresolved risks are explicitly listed
