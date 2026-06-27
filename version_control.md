# Version Control Guide

> Created: 2026-06-27
> Purpose: Master reference for all Git operations and a living changelog.

## Branching Strategy

```
main                              ← stable, always-working state
  └── codex/finetune-*            ← experimental branch per iteration
```

- `main` — only working, tested code. Never commit directly during experimentation.
- `codex/*` — WIP branches. Create one per feature or fix. Merge when stable, delete if dead-end.

## Common Commands

### Daily workflow

```powershell
# Before any experiment — branch off main
git checkout main
git checkout -b codex/finetune-<name>

# Make changes, test...
# Stage and commit frequently
git add <files>
git commit -m "descriptive message"

# When experiment succeeds — merge back
git checkout main
git merge codex/finetune-<name>
git branch -d codex/finetune-<name>

# When experiment fails — discard
git checkout main
git branch -D codex/finetune-<name>
```

### Rollback

```powershell
# Undo uncommitted changes (go back to last commit)
git checkout -- .

# Undo the last commit (keep changes unstaged)
git reset --soft HEAD~1

# Undo the last commit (discard changes entirely)
git reset --hard HEAD~1

# Revert a specific commit (safe, keeps history)
git revert <commit-hash>

# Go back to a tagged milestone
git checkout tags/v0.2-phase2-db
```

### Tags (milestones)

```powershell
# Tag current commit as a milestone
git tag -a v0.4-phase4-ui -m "Phase 4 complete — Streamlit UI working"

# List all tags
git tag -l

# Push tags to remote (if any)
git push --tags
```

### Inspection

```powershell
git log --oneline --graph --all    # Compact history
git status                          # Current state
git diff                            # Uncommitted changes
git show <commit-hash>              # Details of a commit
```

## Changelog

| # | Date | Commit | Description | Tag |
|---|---|---|---|---|
| 1 | 2026-06-27 | `Initial commit` | Phase 1-4 complete — environment setup, wealth_segment_pivot data (57,600 rows), DuckDB load, knowledge base with 20 examples, query engine (Ollama → SQL → execution → formatting), Streamlit UI | `v0.4-phase4-ui` |
