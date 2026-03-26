# Contributing To UncommonRoute

Thanks for helping improve UncommonRoute.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Common Commands

Run the full test suite:

```bash
pytest -q
```

Run lint:

```bash
ruff check .
```

Reproduce the offline evaluation snapshots used in the README:

```bash
python -m bench.run
python -m bench.cost_simulation
```

Build and validate the package metadata:

```bash
python -m build
python -m twine check dist/*
```

## Repo Layout

- `uncommon_route/`: shipped runtime package, proxy, router, CLI, calibration
- `bench/`: offline evaluation datasets and benchmark scripts
- `demo/`: local comparison/demo servers and utilities
- `frontend/`: dashboard and demo frontends
- `openclaw-plugin/`: OpenClaw integration assets

The root-level `api.py` is only a compatibility shim for the comparison demo.
New demo work should live under `demo/`, not in the package root.

## Pull Request Expectations

- Keep PRs focused. Small, reviewable changes land faster.
- Add or update tests for behavior changes.
- Update README benchmark numbers only when they can be reproduced from the current repo.
- Do not commit `dist/`, `build/`, `.egg-info/`, or other generated artifacts.
- If a change affects routing behavior, include the exact command you used to validate it.

## Coding Notes

- Prefer `rg` / `rg --files` for local search.
- Keep edits ASCII unless the file already uses non-ASCII text.
- Avoid adding new heuristics when a measurable offline evaluation or calibration change is a better fit.
