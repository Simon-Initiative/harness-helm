# Operations

## Observability

- Log startup failures, parse failures, and reload events to stderr or structured local logs.
- Surface reload and parse errors inside the TUI so the user can see when the displayed state is stale or incomplete.
- Track file refresh counts and reload latency as first-order runtime signals.

## Performance

- Poll only the small set of source files that define the work-item state.
- Refresh only when file content or metadata changes.
- Keep the parser fast enough that frequent refreshes do not degrade terminal responsiveness.

## Rollout

- Start with local developer use in a single terminal session.
- Favor portability across macOS and Linux terminals.
- Delay nonessential infrastructure concerns until the core work-item observation loop is stable.

## Assumptions

- The first release does not require remote telemetry or SaaS observability.
- Polling frequency should be configurable once real usage exposes the right tradeoff between responsiveness and CPU usage.
