# Phase 12 Roadmap

This roadmap translates remaining engineering items into executable workstreams with effort, dependencies, and delivery order.

## 1. Planning Assumptions

1. Team: 1 to 2 analytics/data engineers.
2. Existing stack remains: DuckDB, dbt, Python, Streamlit, Airflow, GitHub Actions.
3. Effort units:
- `S`: 1 to 3 engineering days
- `M`: 4 to 10 engineering days
- `L`: 2 to 4 engineering weeks

## 2. Priority Roadmap Table

| ID | Workstream | Outcome | Effort | Dependencies | Quick Win vs Long-Term |
| --- | --- | --- | --- | --- | --- |
| P12-01 | Alert delivery channels | Send actionable alerts to email/Teams/webhook from monitoring decisions | M | Existing severity+dedupe decision table (`analytics_monitoring.pipeline_alert_events`) | Quick Win |
| P12-02 | SCD Type 2 expansion | Add snapshot coverage for remaining dimensions and define SCD policy per dimension | M | Existing snapshot baseline for region/sector | Quick Win |
| P12-03 | SCD policy and data contracts | Publish explicit Type 1/Type 2 rules and downstream impact notes | S | P12-02 design decisions | Quick Win |
| P12-04 | Semantic metric layer contracts | Canonical metric registry for KPI names, formulas, dimensions, owners | L | Stable marts, documentation baseline | Long-Term Foundation |
| P12-05 | Controlled what-if backend | Scenario runner with bounded inputs and auditable scenario metadata | L | P12-04 metric semantics, forecast assumptions | Long-Term Foundation |
| P12-06 | Streamlit what-if UI | End-user scenario form and comparison output cards | M | P12-05 backend APIs/contracts | Long-Term |
| P12-07 | Ad-hoc query guardrail service | Restricted query execution with allowlisted schemas and timeouts | L | P12-04 semantic contracts, governance approvals | Long-Term |
| P12-08 | User-defined metric workflow | Proposal->review->publish path for custom metrics | L | P12-04, release governance workflow | Long-Term |
| P12-09 | Performance profiling and tuning | Profiling report and optimization of slow models/dashboard queries | M | Current CI and dbt telemetry | Quick Win |
| P12-10 | Data drift and semantic contract checks | Add type-level and distribution-level drift checks beyond column-count checks | M | Current source registry and SLA checks | Quick Win |

## 3. Delivery Sequence

### Wave A (2 to 3 weeks): Operational hardening quick wins

1. P12-01 Alert delivery channels
2. P12-02 SCD Type 2 expansion
3. P12-03 SCD policy and contracts
4. P12-09 Performance profiling and tuning
5. P12-10 Data drift and semantic contract checks

### Wave B (3 to 5 weeks): Self-service foundations

1. P12-04 Semantic metric layer contracts
2. P12-05 Controlled what-if backend

### Wave C (3 to 6 weeks): Self-service UX and advanced capabilities

1. P12-06 Streamlit what-if UI
2. P12-07 Ad-hoc query guardrail service
3. P12-08 User-defined metric workflow

## 4. Detailed To-Do (Ready for Ticketing)

### P12-01 Alert Delivery Channels (M)

Tasks:
1. add environment variables for alert channels (email/Teams/webhook endpoints)
2. add notifier module reading `analytics_monitoring.pipeline_alert_events`
3. send notifications only when `is_notification=true`
4. add retry and backoff for network failures
5. add docs and runbook updates

Acceptance criteria:
1. critical/high alerts reach configured channel
2. duplicate suppressed events do not notify
3. escalation and recovery notifications are distinguishable in message templates

### P12-02 SCD Type 2 Expansion (M)

Tasks:
1. identify additional candidate dimensions for snapshotting
2. implement dbt snapshots with stable unique keys and check columns
3. add snapshot tests for key uniqueness and current-record assumptions
4. update docs with query examples for historical lookups

Acceptance criteria:
1. snapshots run in CI/local without errors
2. dimension-history queries are reproducible and documented

### P12-03 SCD Policy and Contracts (S)

Tasks:
1. create SCD policy matrix (dimension -> strategy -> rationale)
2. define consumer guidance for Type 1 vs Type 2 usage
3. include breaking-change guidance in release governance

Acceptance criteria:
1. policy doc is referenced in docs index and release governance
2. interview/defense artifacts align with final policy

### P12-04 Semantic Metric Layer Contracts (L)

Tasks:
1. create metric registry file/table (metric id, formula, owner, grain, dimensions)
2. map existing dashboard KPIs to registry entries
3. enforce registry checks in CI (missing metric references fail)
4. expose registry metadata in dashboard tooltips and docs

Acceptance criteria:
1. all dashboard KPIs map to registry entries
2. CI fails on undocumented metric additions

### P12-05 Controlled What-If Backend (L)

Tasks:
1. define scenario input schema with bounded ranges
2. implement scenario runner for forecast recalculation with assumptions
3. persist scenario metadata (who/when/inputs/version)
4. provide scenario result table with baseline vs scenario deltas

Acceptance criteria:
1. scenario runs are reproducible
2. invalid inputs are rejected with clear validation messages

### P12-06 Streamlit What-If UI (M)

Tasks:
1. add scenario input form and validation hints
2. show baseline vs scenario comparison cards/charts
3. allow scenario export for governance review

Acceptance criteria:
1. non-technical users can run valid scenarios without code changes
2. outputs include scenario assumptions and timestamps

### P12-07 Ad-Hoc Query Guardrail Service (L)

Tasks:
1. implement allowlisted query endpoint/runner
2. enforce query timeout and row limits
3. audit log user query text and execution metadata
4. block non-select statements and forbidden schemas

Acceptance criteria:
1. only approved read-only queries execute
2. audit logs are persisted and reviewable

### P12-08 User-Defined Metric Workflow (L)

Tasks:
1. define metric proposal schema and review states
2. implement approval workflow and publish gate
3. update dashboard to display approved custom metrics only

Acceptance criteria:
1. no custom metric appears without approval
2. published metrics are versioned and traceable

### P12-09 Performance Profiling and Tuning (M)

Tasks:
1. collect dbt model timing and dashboard query timing
2. identify top 5 bottlenecks
3. apply targeted optimizations (materialization changes, query rewrites)
4. benchmark before/after performance

Acceptance criteria:
1. measurable runtime improvement for top bottlenecks
2. benchmark report added to docs/releases

### P12-10 Data Drift and Semantic Contract Checks (M)

Tasks:
1. add type-consistency checks for raw->staging transitions
2. add distribution drift checks for critical numeric fields
3. wire drift checks into SLA/CI failure policy

Acceptance criteria:
1. drift checks produce actionable failures with source/field context
2. false positives remain within acceptable operational threshold

## 5. Risk Register

1. governance risk: metric drift if semantic contracts are delayed
2. adoption risk: self-service features before guardrails may reduce trust
3. operational risk: alert channels without routing ownership can increase noise
4. maintenance risk: large feature expansion without phased release boundaries

Mitigation:
1. enforce Wave A before Wave B and Wave C
2. require release notes for each roadmap workstream
3. keep capability register current after each delivery wave

## 6. Immediate Next Sprint Recommendation

Recommended next sprint (highest value/lowest complexity):
1. implement P12-01 alert delivery channels
2. complete P12-02 snapshot expansion
3. publish P12-03 SCD policy matrix
4. execute P12-09 profiling baseline and quick optimizations

This sprint delivers reliability and governance gains without opening high-risk self-service scope too early.
