# dbt Scaffold Guide

## Purpose

Define dbt project structure so transformations remain modular, testable, and explainable.

## Folder Design

- `models/staging/`: source cleanup and type normalization
- `models/intermediate/`: reusable transformations and harmonized domain tables
- `models/dimensions/`: conformed dimensions
- `models/facts/`: domain-level fact tables
- `models/marts/`: decision-ready policy marts
- `tests/`: generic and singular tests
- `snapshots/`: historical state tracking where needed
- `macros/`: reusable SQL logic and custom tests

## Standards

- one model purpose per file
- explicit model naming by layer and domain
- tests required on keys and critical fields
- avoid embedding policy scoring logic in staging layer

## Suggested Initial Build Order

1. source declarations
2. staging models
3. dimensions
4. fact models
5. marts
6. tests and documentation
