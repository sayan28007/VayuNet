# VayuNet Render Backend Fix 3

## Replace
apps/backend/app/prediction/forecast.py

## Problem
Render reaches application startup, but Python stops parsing `forecast.py`
because the current code uses:

```python
for mins in horizon := horizons:
```

That is invalid Python syntax. The walrus expression cannot be used in that
`for` target form.

## Fix
Use:

```python
for mins in horizons:
```

The deterministic forecast behavior is otherwise preserved.

## After replacement
Commit:
`fix: repair forecast engine syntax for Render`

Push to `main`. Render should automatically deploy the new commit.
