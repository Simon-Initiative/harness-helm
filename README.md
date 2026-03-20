# harness-helm

`harness-helm` is a local-first Python TUI for observing harness work items as they change on disk.

## What It Does

- Show plan phases and titles from `plan.md`.
- Browse requirements and their validation state from `requirements.yml`.
- Render `prd.md`, `fdd.md`, and `plan.md` in the terminal.
- Poll the work-item files and refresh the UI when they change.

The app is read-only and optimized for feature-spec situational awareness rather than editing.

## Install

### Local install with `pip`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

After install:

```bash
helm <feature-dir>
```

Example:

```bash
helm docs/exec-plans/current/<feature-slug>
```

### Development install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

### Install from a built wheel

```bash
pip install dist/harness_helm-0.1.0-py3-none-any.whl
```

## Quick Start

```bash
.venv/bin/helm tests/fixtures/sample_feature
```

## Usage

```bash
helm <feature-dir>
```

Examples:

```bash
helm tests/fixtures/sample_feature
helm ../oli-torus/docs/exec-plans/current/epics/product_overhaul/template_preview
```

Keyboard shortcuts:

- `1` Overview
- `2` PRD
- `3` FDD
- `4` Plan
- `5` Requirements
- `Tab` next view
- `Shift+Tab` previous view
- `r` refresh
- `q` quit

## Packaging And Distribution

Build a source distribution and wheel:

```bash
.venv/bin/python -m build
```

Artifacts are written to `dist/`:

- `dist/harness_helm-0.1.0.tar.gz`
- `dist/harness_helm-0.1.0-py3-none-any.whl`

To test the built package in a clean environment:

```bash
python3 -m venv /tmp/helm-test
/tmp/helm-test/bin/pip install dist/harness_helm-0.1.0-py3-none-any.whl
/tmp/helm-test/bin/helm tests/fixtures/sample_feature
```

## Developer Workflow

Run tests:

```bash
.venv/bin/python -m pytest
```

Run the app directly from source:

```bash
.venv/bin/python -m helm tests/fixtures/sample_feature
```

## Project Layout

- `src/helm/cli.py`: CLI entrypoint and argument parsing.
- `src/helm/store.py`: central app state, refresh flow, and watcher integration.
- `src/helm/watcher.py`: polling-based file observation.
- `src/helm/app.py`: Textual application shell and three-row layout.
- `src/helm/parsers/`: plan, PRD capability, and requirements parsing.
- `src/helm/views/`: overview, requirements, and markdown document views.
- `src/helm/widgets/`: top and bottom chrome widgets.
- `tests/`: loader-focused tests with fixture work items.

## Current Assumptions

- Python 3.11+ is required.
- The app targets a single feature directory containing `prd.md`, `fdd.md`, `plan.md`, and `requirements.yml`.
- File change detection currently uses polling, not OS-native file watcher events.
