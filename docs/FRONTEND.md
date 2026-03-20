# Frontend

## UI Rules

- The UI is a terminal UI, not a web frontend.
- Textual widgets should present a stable multi-pane browsing experience for phases, requirements, and source documents.
- Keyboard-first navigation is required.
- Live refresh must preserve context when possible so the user does not lose their current selection during file updates.

## Primary Views

- A plan view that exposes phases and titles from `plan.md`.
- A requirements view that lists requirements and their validation state from `requirements.yml`.
- Rendered document views for `prd.md`, `fdd.md`, and `plan.md`.
- A status area that shows refresh timing, parse health, and file-change detection.

## Rendering Principles

- Prefer legibility over decorative styling.
- Use consistent visual language for status states such as valid, stale, missing, and failed-to-parse.
- Keep long markdown documents browsable with clear section hierarchy and predictable scrolling behavior.
