# Reliability

## Expectations

- The TUI should keep running when a watched file becomes temporarily invalid during editing.
- Parse failures should degrade visibly rather than crashing the session.
- Refreshes should converge quickly to the latest on-disk state once edits are saved.
