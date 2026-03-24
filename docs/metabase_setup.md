# Metabase Setup (JAR + DuckDB Plugin, No Docker)

## Decision

For this project, Metabase will run using the JAR distribution and DuckDB driver plugin.
Docker is intentionally excluded to keep operations simple in Codespaces and novice local setups.

## Why this approach

- simpler startup for beginners
- fewer container resource issues in constrained environments
- easier debugging with direct logs
- avoids container networking complexity

## Prerequisites

- Java Runtime Environment (JRE 17+)
- DuckDB file available (for example `data/processed/regional_resilience.duckdb`)

## Setup Steps

1. Download Metabase JAR from official release page.
2. Create plugin folder:

```bash
mkdir -p plugins
```

3. Download DuckDB plugin JAR into `plugins/`.
4. Run Metabase from repository root:

```bash
java -jar metabase.jar
```

5. Open Metabase UI (default `http://localhost:3000`).
6. Add database connection using DuckDB plugin and point to project DuckDB file.

## Operational Notes

- keep plugin and metabase versions documented when changed
- use read-only analytical models for dashboard exposure where feasible
- store dashboard question-to-chart mapping in `docs/dashboard_question_bank.md`

## Troubleshooting

- If DuckDB does not appear as a database option, verify plugin JAR path and restart Metabase.
- If connection fails, verify DuckDB file path and file permissions.
- If port 3000 is busy, run Metabase with custom port environment variable.
