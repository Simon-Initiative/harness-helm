# Testing

## Test Types

- Unit tests for markdown and YAML parsing.
- Unit tests for derived state, including requirement validation summaries and plan phase extraction.
- Integration tests for refreshing state when source files change.
- UI tests for core Textual screens and keyboard navigation where practical.

## Required Gates

- Parser and model changes require automated tests.
- Regressions in work-item loading should be covered with fixture directories that resemble real `docs/exec-plans/current/<feature-slug>` content.
- Polling behavior should be tested with controlled file updates rather than manual verification alone.

## Notes

- Most behavioral risk is in parsing and state refresh, so those layers should be tested before optimizing widget behavior.
- Raw markdown rendering can be smoke-tested with representative PRD, FDD, and plan fixtures.
