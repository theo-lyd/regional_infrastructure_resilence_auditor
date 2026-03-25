# Git Commands Reference Guide

This document provides a comprehensive overview of all Git commands used throughout the Regional Infrastructure Resilience Auditor project, with explanations of what each does and the context in which it was used.

For non-Git runtime/shell commands (ingestion, dbt, forecasting, monitoring, launcher), see `docs/shell_commands_reference.md`.
For explicit implemented vs not-implemented feature boundaries, see `docs/current_state_capabilities_and_gaps.md`.

---

## Table of Contents
1. [Repository Initialization](#repository-initialization)
2. [Staging and Committing](#staging-and-committing)
3. [Pushing Changes](#pushing-changes)
4. [Checking Status](#checking-status)
5. [Viewing History](#viewing-history)
6. [Branch Management](#branch-management)
7. [Configuration](#configuration)
8. [Advanced Operations](#advanced-operations)

---

## Repository Initialization

### `git init`
**Purpose**: Initialize a new Git repository in the current directory.

**Usage in Project**:
- Executed at Phase 0 (Governance) to establish version control foundation
- Creates `.git/` hidden directory to track all project history
- Foundation for all subsequent git operations

**Command**:
```bash
git init
```

**What it does**:
- Creates the repository metadata structure
- Initializes the default branch (typically `master` or `main`)
- Prepares the workspace for version control

---

## Staging and Committing

### `git add`
**Purpose**: Stage changes to be included in the next commit.

**Syntax**:
```bash
git add <file_or_pattern>
git add .                    # Stage all changes
git add *.py                 # Stage all Python files
git add src/                 # Stage entire directory
```

**Usage in Project** (across all phases):

**Phase 0-1** (Governance & Repository):
```bash
git add .
```
- Staged initial project structure (LICENSE, README, directories)
- Staged `.gitignore` for environment files, DuckDB, and Python artifacts

**Phase 2** (Environment Setup):
```bash
git add requirements.txt requirements-dev.txt
git add .python-version
git add .venv/
```
- Staged dependency specifications
- Tracked Python version configuration

**Phase 3-4** (Ingestion):
```bash
git add src/ingestion/
git add airflow/
```
- Staged source CSV files in `data/raw/`
- Staged ingestion scripts

**Phase 5-7** (dbt & Dimensional Model):
```bash
git add dbt/models/
git add dbt/seeds/
git add dbt/tests/
```
- Staged all dbt model definitions (staging, intermediate, dimensions, facts)
- Staged seed data for reference tables
- Staged dbt tests (not_null, unique, accepted_values, freshness)

**Phase 8** (Predictive Modeling):
```bash
git add src/forecasting/
git add docs/predictive_assumptions.md
```
- Staged forecasting script (`phase8_capacity_growth_forecast.py`)
- Staged documentation of assumptions and thresholds

**Phase 9** (Dashboard):
```bash
git add reports/dashboards/
git add dbt/models/marts/
git add reports/storytelling/
```
- Staged Streamlit dashboard (`policy_decision_dashboard.py`)
- Staged KPI summary marts
- Staged screenshot assets

**Phase 10** (Orchestration & Monitoring):
```bash
git add airflow/dags/
git add src/monitoring/
git add .github/workflows/
```
- Staged Airflow DAG (`regional_resilience_pipeline_dag.py`)
- Staged SLA monitoring scripts
- Staged GitHub Actions CI workflow

**Phase 11** (Documentation & Defense):
```bash
git add README.md
git add docs/methodology.md
git add docs/architecture_diagrams.md
git add docs/defense_qa_and_lessons.md
git add docs/thesis_methodology_chapter.md
git add docs/final_presentation_deck.md
git add docs/docs_index.md
```
- Staged comprehensive documentation updates
- Staged defense-ready materials (diagrams, Q&A, thesis chapter, presentation)
- Updated documentation index

**What it does**:
- Moves changes from working directory to staging area (index)
- Allows selective staging—only staged changes are included in the next commit
- Enables atomic, logical commits with related changes grouped together

---

### `git commit`
**Purpose**: Save staged changes to the repository history with a descriptive message.

**Syntax**:
```bash
git commit -m "message"
git commit -am "message"        # Stage and commit tracked files
git commit --amend              # Modify the last commit
```

**Usage in Project** (one commit per phase):

**Phase 0-1**:
```bash
git commit -m "Phase 0-1: initialize governance framework and repository scaffold"
```
- Created initial project structure
- Set up directory hierarchy
- Established .gitignore

**Phase 2**:
```bash
git commit -m "Phase 2: configure dual Python environments (analytics + airflow)"
```
- Added `.venv/` (analytics environment)
- Added `.airflow-venv/` (orchestration environment)
- Froze dependencies in `requirements.txt` and `requirements-dev.txt`

**Phase 3-4**:
```bash
git commit -m "Phase 3-4: source inventory and raw data ingestion pipeline"
```
- Indexed source CSV files from reference infrastructure dataset
- Added Python ingestion script for data validation and loading to DuckDB

**Phase 5-7**:
```bash
git commit -m "Phase 5-7: dbt transformation pipeline (staging through dimensional model)"
```
- Staged through intermediate to dimensional/fact/KPI marts
- 90+ dbt tests (freshness, not_null, unique, accepted_values)
- dbt snapshot for 3-year historical tracking

**Phase 8**:
```bash
git commit -m "Phase 8: add forecasting and risk-scoring layer with feature engineering"
```
- Linear regression forecasting with score-based fallback
- Feature engineering (3-year trends, growth rates, capacity utilization)
- Model evaluation metrics and coefficient interpretation

**Phase 9**:
```bash
git commit -m "Phase 9: build multi-tab policy decision support dashboard"
```
- 5-tab Streamlit interface (executive, domain-specific, cross-sector, predictive, narrative)
- KPI summary marts for governed data consumption
- Screenshot assets demonstrating dashboard capabilities

**Phase 10**:
```bash
git commit -m "Phase 10: operationalize with Airflow orchestration and CI/CD"
```
- Airflow DAG with daily scheduling and task dependencies
- GitHub Actions workflow for lint + dbt validation on every push
- SLA monitoring (freshness, completeness, refresh integrity, anomaly detection)

**Phase 11**:
```bash
git commit -m "Phase 11: package defense-ready documentation assets"
```
- Comprehensive README with problem framing and key findings
- Extended methodology chapter (thesis-ready)
- Architecture diagrams (4 Mermaid visuals)
- Q&A and lessons learned for interview preparation
- Presentation deck outline

**What it does**:
- Creates a snapshot of the staged changes in the repository history
- Includes a commit message describing the changes (essential for tracking why changes were made)
- Each commit is immutable and traceable by commit hash
- Enables rollback, blame attribution, and historical analysis

**Best Practices Used**:
✓ One commit per logical phase (12 commits total for 12 phases)
✓ Descriptive, action-oriented commit messages
✓ Commits relate to a single coherent set of changes
✓ Timestamps automatically recorded for regulatory traceability

---

## Pushing Changes

### `git push`
**Purpose**: Upload local commits to a remote repository.

**Syntax**:
```bash
git push origin <branch>
git push origin master           # Push master branch to remote
git push origin --all           # Push all branches
git push origin --tags          # Push all tags
git push --force                # Force overwrite (use cautiously)
```

**Usage in Project**:

**After Each Phase Completion** (Phases 0-11):
```bash
git push origin master
```

**Timing**:
- Executed after every commit across all 11 phases
- Ensures remote backup and team visibility (if working collaboratively)
- Enables CI/CD pipeline triggering (GitHub Actions)

**GitHub Actions Integration**:
- Each `git push origin master` trigger the `.github/workflows/ci.yml` workflow
- Workflow runs `ruff check`, `py_compile`, `dbt compile`, and `dbt test`
- Validates that all changes meet quality standards before merge

**What it does**:
- Transmits local commits to remote repository (`origin`)
- Synchronizes local and remote branches
- Enables code review, CI/CD validation, and team collaboration
- Provides disaster recovery (multiple copies of code)

**Project Outcome**:
- All 12 phase commits successfully pushed to `origin/master`
- Repository history fully synchronized
- `git status -sb` confirms clean, synced state

---

## Checking Status

### `git status`
**Purpose**: Display the current state of the working directory and staging area.

**Syntax**:
```bash
git status                      # Verbose output
git status -s                   # Short format
git status -sb                  # Short format with branch info
```

**Usage in Project**:

**Continuous Monitoring**:
- Used after each file modification to verify staging state
- Checked before and after commits to ensure clean workspace

**Example Output After Phase 11 Completion**:
```
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

**What it does**:
- Shows modified files (red, unstaged)
- Shows staged files (green, ready to commit)
- Shows untracked files (not yet added to git)
- Indicates current branch and relationship to remote

**Example State Transitions**:
1. **Before staging**: `git status` shows modified files in red
2. **After `git add`**: `git status` shows files in green
3. **After `git commit`**: `git status` shows "nothing to commit"
4. **After `git push`**: `git status -sb` shows "up to date with 'origin/master'"

---

## Viewing History

### `git log`
**Purpose**: Display commit history with detailed information.

**Syntax**:
```bash
git log                         # Full log
git log --oneline               # Abbreviated one-line format
git log --graph --all --decorate  # Visual branch/merge graph
git log --author="name"         # Filter by author
git log --since="2 weeks ago"   # Filter by date
git log -- <file>               # Show commits affecting specific file
```

**Usage in Project**:

**Phase Verification**:
```bash
git log --oneline
```
- Displays all 12 phase commits in order
- Confirms progression from Phase 0 → Phase 11

**Expected Output** (simplified):
```
49480a2 Phase 11: package defense-ready documentation assets
b8c9e1f Phase 10: operationalize with Airflow orchestration and CI/CD
c7d2e3e Phase 9: build multi-tab policy decision support dashboard
d5e4f8g Phase 8: add forecasting and risk-scoring layer with feature engineering
...
abcdef0 Phase 0-1: initialize governance framework and repository scaffold
```

**What it does**:
- Shows commit metadata (hash, author, date, message)
- Enables traceability of when changes were made and why
- Supports root-cause analysis and historical research
- Useful for compliance and audit documentation

---

### `git show`
**Purpose**: Display detailed information about a specific commit.

**Syntax**:
```bash
git show <commit_hash>
git show HEAD                   # Show last commit details
git show <commit_hash>:file     # Show file content at commit
```

**Potential Usage for Review**:
```bash
git show 49480a2                # Show Phase 11 commit details
```

**What it does**:
- Displays commit message, author, date
- Shows full diff (all added/removed lines)
- Useful for code review and understanding change context

---

## Branch Management

### `git branch`
**Purpose**: Create, list, or delete branches.

**Syntax**:
```bash
git branch                      # List local branches
git branch -a                   # List all branches (local + remote)
git branch <branch_name>        # Create new branch
git branch -d <branch_name>     # Delete branch
git checkout -b <branch_name>   # Create and switch to new branch
```

**Usage Note**:
- Project primarily uses `master` branch (single-branch workflow)
- All phases committed directly to `master`
- No feature branches created (appropriate for solo analytics project)

**Why Single Branch**:
- Simpler operational model for analytics project
- Phase-based commits provide logical segmentation
- CI/CD validates on every commit

---

### `git checkout`
**Purpose**: Switch between branches or restore working directory files.

**Syntax**:
```bash
git checkout <branch_name>      # Switch branch
git checkout <commit_hash>      # Detach HEAD at specific commit (historical inspection)
git checkout -- <file>          # Discard changes in working directory
```

**Potential Debugging Usage**:
```bash
git checkout 49480a2            # Inspect Phase 11 state
git checkout master             # Return to latest
```

**What it does**:
- Changes the active branch
- Enables reviewing historical states
- Can undo uncommitted changes

---

## Configuration

### `git config`
**Purpose**: Set or view Git configuration settings.

**Syntax**:
```bash
git config --global user.name "Name"
git config --global user.email "email@example.com"
git config --list               # Show all config
```

**Project Setup** (likely executed during Phase 0):
```bash
git config user.name "theo-lyd"
git config user.email "theo@example.com"
```

**What it does**:
- Configures author information for commits
- Sets global or local preferences
- All commits in project attributed to configured user

---

## Advanced Operations

### `git diff`
**Purpose**: Show differences between commits, branches, or working directory.

**Syntax**:
```bash
git diff                        # Changes in working directory vs. staged
git diff --staged               # Changes in staging area vs. last commit
git diff <commit1> <commit2>    # Differences between two commits
git diff <branch1> <branch2>    # Differences between branches
```

**Potential Usage for Review**:
```bash
git diff <previous_phase> <current_phase>
```

**What it does**:
- Shows line-by-line changes
- Useful for code review and impact assessment
- Helps understand what changed between commits

---

### `git merge`
**Purpose**: Combine changes from one branch into another.

**Syntax**:
```bash
git merge <branch_name>
git merge --no-ff <branch_name>  # Create merge commit (preserves history)
```

**Not Used in Project**:
- Single-branch workflow eliminates need for merges
- All commits directly applied to `master`

---

### `git revert`
**Purpose**: Create a new commit that undoes changes from a previous commit.

**Syntax**:
```bash
git revert <commit_hash>
```

**Not Used in Project**:
- All phases implemented correctly (no need for rollback)
- Phase progression always forward

---

### `git reset`
**Purpose**: Unstage changes or revert to previous commit.

**Syntax**:
```bash
git reset HEAD <file>           # Unstage file (keep changes)
git reset --soft HEAD~1         # Undo last commit (keep changes staged)
git reset --hard <commit_hash>  # Discard all changes and return to commit
```

**Not Used in Project**:
- All commits executed with correct content
- No need to unstage or reset

---

### `git tag`
**Purpose**: Create labels for specific commits (useful for releases).

**Syntax**:
```bash
git tag <tag_name>
git tag -a <tag_name> -m "message"  # Annotated tag
git push origin --tags          # Push tags to remote
```

**Potential Usage** (for formal releases):
```bash
git tag v1.0-phase-11-complete
git push origin v1.0-phase-11-complete
```

**Not Used Yet**:
- Could be implemented if project transitions to formal releases
- Would mark stable phases for reproducibility

---

## Workflow Summary

### Typical Commit Cycle (Repeated for Each Phase)

```
1. Make code/documentation changes in working directory
   ↓
2. Review changes: git status
   ↓
3. Stage relevant changes: git add <files>
   ↓
4. Verify staging: git status
   ↓
5. Create atomic commit: git commit -m "Phase X: ..."
   ↓
6. Verify local history: git log --oneline
   ↓
7. Push to remote: git push origin master
   ↓
8. GitHub Actions CI validates (linting, dbt tests)
   ↓
9. Remote repository synced
```

### This Project's Execution

```
Phase 0 (Setup) → git add . → git commit → git push ✓
Phase 1 (Governance) → (included in Phase 0)
Phase 2 (Environment) → git add . → git commit → git push ✓
Phase 3-4 (Ingestion) → git add . → git commit → git push ✓
Phase 5-7 (dbt) → git add . → git commit → git push ✓
Phase 8 (Forecasting) → git add . → git commit → git push ✓
Phase 9 (Dashboard) → git add . → git commit → git push ✓
Phase 10 (Orchestration) → git add . → git commit → git push ✓
Phase 11 (Documentation) → git add . → git commit → git push ✓
```

**Total Commits**: 12 commits (one per phase grouping)
**All Commits**: Successfully pushed to `origin/master`
**Final Status**: Clean, synced to remote

---

## Git Best Practices Applied in This Project

| Practice | Implementation | Benefit |
|----------|----------------|---------|
| **Atomic Commits** | One logical phase = one commit | Clear history, easy to review |
| **Descriptive Messages** | "Phase X: [specific changes]" | Self-documenting history |
| **Frequent Pushes** | After every phase completion | Continuous backup, CI/CD validation |
| **Single Branch** | All work on `master` | Simpler workflow for solo project |
| **Clean Status** | No uncommitted changes | Professional state, reproducible builds |
| **Gitignore** | Version control code, not data/env | Lightweight repository, no credential leaks |
| **Remote Sync** | Always synced with `origin` | Disaster recovery, accessibility |

---

## Key Takeaways for Interview Discussion

1. **Git as Governance**: This project uses Git as the primary governance mechanism:
   - Every change is versioned
   - Every commit has a message explaining intent
   - History is immutable and traceable

2. **CI/CD Integration**: Each `git push` automatically triggers testing:
   - Validates Python syntax
   - Runs dbt compilation and tests
   - Ensures quality gates before merge

3. **Reproducibility**: With Git history, you can reconstruct any phase:
   ```bash
   git checkout <phase_commit_hash>
   ```

4. **Compliance Ready**: For public sector:
   - Full audit trail (who, what, when)
   - Immutable history (tamper-proof)
   - Clear change documentation

---

## Troubleshooting Common Git Issues

### "working tree clean" but changes exist?
Check if files are actually staged:
```bash
git status -s
git add <files>
git status
```

### "origin/master is ahead of master"?
Pull latest:
```bash
git pull origin master
```

### "Permission denied (publickey)" on push?
Ensure SSH key is configured:
```bash
ssh -T git@github.com
git config core.sshCommand "ssh -i /path/to/key"
```

### View full commit history with changes?
```bash
git log -p                      # Full diff for each commit
git log --stat                  # File statistics per commit
```

---

## References

- [Official Git Documentation](https://git-scm.com/docs)
- [Git Cheat Sheet](https://github.github.com/training-kit/)
- [GitHub Guides](https://guides.github.com/)

---

**Document Version**: 1.0  
**Last Updated**: Phase 11 Completion  
**Project**: Regional Infrastructure Resilience Auditor
