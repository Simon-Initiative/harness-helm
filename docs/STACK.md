# Stack

## Languages

- Python is the implementation language for the CLI, parsers, and TUI.
- Markdown and YAML are the primary user-authored input formats consumed by the app.

## Frameworks

- `Textual` is the terminal UI framework.
- Standard-library file and path tooling should be preferred for initial ingestion and polling.
- A YAML parser is required for `requirements.yml`.
- A markdown-to-terminal rendering approach is required for the raw document panes.

## Storage

- The application is local-first and reads work-item state directly from the filesystem.
- No database is required for the first version.
- Derived UI state should remain in memory and be rebuilt from source files on refresh.

## Initial Version Targets

- Target modern Python 3.
- Keep packaging and environment management simple and scriptable for terminal-first contributors.
