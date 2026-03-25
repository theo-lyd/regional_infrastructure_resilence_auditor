# Pipeline SLA Report

Generated at (UTC): 2026-03-25T14:46:26.098617+00:00
Overall status: PASS

| Check | Status | Observed | Threshold | Detail |
| --- | --- | --- | --- | --- |
| data_freshness | PASS | 0 | <= 30 | Latest forecast generated at 2026-03-25T13:21:05.352883 |
| minimum_completeness | PASS | 1.0000 | >= 0.85 | Latest completeness from year 2020 |
| failed_refresh_alerts | PASS | 0 | 0 missing | All required refresh outputs present |
| row_count_anomaly | PASS | 0.0000 | <= 0.25 | Row count comparison 2020 vs previous year |

## Alert Routing Note

Use this lightweight routing rule to close the loop when SLA fails.

- No freshness/completeness failure in this run. Keep default daily monitoring.