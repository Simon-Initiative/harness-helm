# Code Review

## Policy

- Prioritize correctness of parsing, refresh behavior, and state derivation over cosmetic UI feedback.
- Require tests for parser changes and bug fixes in the observation loop.
- Reject changes that mix Textual widget code with raw file parsing unless there is a clear boundary reason.

## Review Guides

- Verify that malformed or partial work-item files fail visibly and safely.
- Verify that refreshes do not lose the user’s place unnecessarily.
- Verify that requirements and plan phases shown in the UI match the source artifacts.
