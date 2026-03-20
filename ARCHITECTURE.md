# Architecture

## System Map

`helm` is a local Python application with three major layers:

1. CLI entrypoint and app bootstrapping.
2. Work-item ingestion and state derivation.
3. Textual-based terminal rendering.

The core runtime flow is:

1. The user runs `helm docs/exec-plans/current/<feature-slug>`.
2. The CLI resolves the target work-item directory and validates that the expected harness files exist.
3. Parsers read `prd.md`, `fdd.md`, `plan.md`, and `requirements.yml` into a normalized in-memory model.
4. A polling loop checks those files for timestamp or content changes.
5. When a change is detected, the model is rebuilt and the Textual app refreshes the affected views.

## Primary Components

### CLI Layer

- Resolves input paths.
- Handles startup errors early.
- Launches the Textual application with an initial snapshot of the work item.

### Domain Layer

- Defines the normalized representation of phases, requirements, validation state, and source documents.
- Keeps parsing logic separate from Textual widgets.
- Computes derived state, such as which requirements are validated and which plan phases are complete or in progress.

### File Observation Layer

- Starts with polling because it is simple, portable, and matches the product requirement.
- Tracks source file metadata and reloads only when inputs change.
- Emits explicit refresh events into the UI layer.

### UI Layer

- Renders multiple views over the same work-item state.
- Supports quick navigation between plan phases, requirements, and raw document views.
- Updates incrementally when snapshots change to avoid full-screen flicker.

## Key Data Sources

- `plan.md`: phase structure, titles, and progress narrative.
- `requirements.yml`: requirements, acceptance criteria, traceability, and validation state.
- `prd.md`: product context and intent.
- `fdd.md`: implementation design and boundaries.

## Architectural Boundaries

- Parsing code should not depend on Textual widgets.
- Rendering code should consume a stable view model, not raw markdown or YAML.
- Polling and refresh scheduling should be isolated from business logic so it can be tested without a running UI loop.

## Assumptions

- This repository is intentionally local-first and does not require a backend service.
- The first implementation targets polling rather than filesystem event subscriptions.
- Markdown rendering inside the terminal should favor correctness and clarity over pixel-perfect parity with web markdown renderers.
