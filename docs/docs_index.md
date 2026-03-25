# Documentation Index

This folder is the project control center for technical and non-technical stakeholders.

## Core Governance

- `project_brief.md`: project objective, users, public value, and success criteria.
- `scope.md`: in-scope and out-of-scope boundaries.
- `methodology.md`: KPI design, model layers, and technical principles.
- `environment_setup.md`: reproducible environment instructions for Codespaces/local.
- `metabase_setup.md`: Metabase JAR + DuckDB plugin setup (non-Docker).

## Phase-by-Phase Guides

- `phase_0_governance.md`
- `phase_1_repository_setup.md`
- `phase_2_environment_configuration.md`

## Technical Implementation Records

- `phase_0_technical_implementation.md`
- `phase_1_technical_implementation.md`
- `phase_2_technical_implementation.md`
- `phase_3_technical_implementation.md`
- `phase_4_technical_implementation.md`
- `phase_5_technical_implementation.md`
- `phase_6_technical_implementation.md`
- `phase_7_technical_implementation.md`
- `phase_8_technical_implementation.md`
- `phase_9_technical_implementation.md`
- `phase_10_technical_implementation.md`
- `phase_11_technical_implementation.md`
- `phase_12_roadmap.md`

Each phase guide contains:
- what was implemented
- how it was implemented
- why it matters for public-sector analytics
- often-overlooked details and review checklist

## Data and Modeling Design

- `source_inventory.md`: source dataset inventory and ingestion notes.
- `standardization_business_rules.md`: normalization and business rule decisions.
- `grain_definition.md`: table grain definitions and anti-pattern warnings.
- `join_strategy.md`: join keys, cardinality assumptions, and safeguards.
- `formula_to_model_mapping.md`: KPI formulas mapped to dbt marts/facts.
- `dbt_scaffold.md`: dbt project architecture and model contracts.
- `data_dictionary.md`: canonical field glossary and business meaning.
- `predictive_assumptions.md`: forecasting target, feature logic, evaluation assumptions, and risk band policy.
- `sla_monitoring.md`: SLA thresholds, monitoring logic, and alert interpretation.
- `current_state_capabilities_and_gaps.md`: explicit implemented/not-implemented status, SCD position, alerting model, and data robustness boundaries.
- `release_governance.md`: release versioning policy, checklist, approvals, and traceability requirements.

## Stakeholder Delivery

- `dashboard_question_bank.md`: decision questions mapped to dashboard pages and batches.
- `thesis_report_outline.md`: defense-ready long-form report structure.
- `final_handoff.md`: operations handoff checklist and support model.
- `thesis_methodology_chapter.md`: thesis-ready methodology chapter draft.
- `final_presentation_deck.md`: final presentation deck draft (slide-by-slide).
- `architecture_diagrams.md`: architecture, KPI composition, lineage, and orchestration diagrams.
- `defense_qa_and_lessons.md`: stakeholder Q&A, interview prompts, and lessons learned.
- `interview_question_bank_with_answers.md`: business, theoretical, and technical interview questions with suggested answers.
- `git_commands_reference.md`: detailed explanation of Git commands used across project phases.
- `shell_commands_reference.md`: command-by-command explanation for runtime, pipeline, monitoring, and launcher operations.
- `system_launch_modes.md`: one-command and clickable launch options for technical and non-technical users.
- `releases/`: versioned release notes for feature and governance changes.

## Reading Order (Novice Friendly)

1. `project_brief.md`
2. `scope.md`
3. `phase_0_governance.md`
4. `phase_1_repository_setup.md`
5. `phase_2_environment_configuration.md`
6. `methodology.md`
7. `standardization_business_rules.md`
8. `dashboard_question_bank.md`
9. `final_handoff.md`
