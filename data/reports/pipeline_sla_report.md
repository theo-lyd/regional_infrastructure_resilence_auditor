# Pipeline SLA Report

Generated at (UTC): 2026-03-25T16:14:26.893352+00:00
Overall status: PASS

| Check | Status | Severity | Observed | Threshold | Detail |
| --- | --- | --- | --- | --- | --- |
| data_freshness | PASS | high | 0 | <= 30 | Latest forecast generated at 2026-03-25T14:48:42.526373 |
| minimum_completeness | PASS | high | 1.0000 | >= 0.85 | Latest completeness from year 2020 |
| completeness_regression | PASS | medium | 0.0000 | drop <= 0.05 | Completeness comparison 2017->2020 |
| failed_refresh_alerts | PASS | critical | 0 | 0 missing | All required refresh outputs present |
| row_count_anomaly | PASS | medium | 0.0000 | <= 0.25 | Row count comparison 2020 vs previous year |

## Alert Decisions (Dedupe and Escalation)

| Check | Status | Severity | Decision | Consecutive Fails | Notify | Reason |
| --- | --- | --- | --- | ---: | --- | --- |
| data_freshness | PASS | high | no_alert | 0 | false | Healthy status with no active incident |
| minimum_completeness | PASS | high | no_alert | 0 | false | Healthy status with no active incident |
| completeness_regression | PASS | medium | no_alert | 0 | false | Healthy status with no active incident |
| failed_refresh_alerts | PASS | critical | no_alert | 0 | false | Healthy status with no active incident |
| row_count_anomaly | PASS | medium | no_alert | 0 | false | Healthy status with no active incident |

## Alert Routing Note

Use this lightweight routing rule to close the loop when SLA fails.

- No freshness/completeness failure in this run. Keep default daily monitoring.