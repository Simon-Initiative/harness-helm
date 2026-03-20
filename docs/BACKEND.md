# Backend

## Service Architecture

- No network service is required for the first version.
- The backend responsibility in this repository is a local parsing and state engine embedded in the CLI app.
- That engine should convert filesystem inputs into a stable work-item model that the Textual UI can consume.

## Backend Boundaries

- Path resolution and input validation belong near the CLI boundary.
- Markdown and YAML parsers belong in the domain ingestion layer.
- Requirement-state derivation belongs in pure business logic.
- Polling, snapshot comparison, and refresh scheduling belong in an observation layer that is independent from rendering.
