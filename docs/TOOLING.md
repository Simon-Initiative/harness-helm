# Tooling

## Commands

- `helm <work-item-dir>` launches the TUI for a work item directory.
- `pytest` runs the automated test suite.
- A formatter and linter should be part of the default local workflow once the Python project skeleton is added.

## Required Gates

- Tests must pass before merge.
- Parsing and state-derivation code should have automated coverage before UI-heavy work is accepted.
- Changes to harness document parsing should include fixture-based regression tests.

## Development Expectations

- Prefer deterministic local commands that work without network dependencies.
- Keep the app runnable from a terminal in a single command during active development.
- Avoid coupling tooling to a specific editor or IDE.
