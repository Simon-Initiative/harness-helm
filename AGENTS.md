# AGENTS

This repository builds `helm`, a Python terminal UI for observing harness work items under `docs/exec-plans/current/`.

## How To Use This Repo Context

- Start with [ARCHITECTURE.md](/Users/darren/dev/harness-helm/ARCHITECTURE.md) for the system shape and data flow.
- Use [docs/STACK.md](/Users/darren/dev/harness-helm/docs/STACK.md) for the implementation stack and major libraries.
- Use [docs/TOOLING.md](/Users/darren/dev/harness-helm/docs/TOOLING.md) for local commands and development gates.
- Use [docs/TESTING.md](/Users/darren/dev/harness-helm/docs/TESTING.md) for the test strategy.
- Use [docs/OPERATIONS.md](/Users/darren/dev/harness-helm/docs/OPERATIONS.md) for observability, polling, and runtime expectations.
- Use [docs/FRONTEND.md](/Users/darren/dev/harness-helm/docs/FRONTEND.md) for terminal UI rules and rendering constraints.
- Use [docs/BACKEND.md](/Users/darren/dev/harness-helm/docs/BACKEND.md) for parser and state-management boundaries.
- Use [docs/PRODUCT_SENSE.md](/Users/darren/dev/harness-helm/docs/PRODUCT_SENSE.md) for user goals and product intent.
- Use [docs/PLANS.md](/Users/darren/dev/harness-helm/docs/PLANS.md) for the harness work-item model this tool must understand.

## Repository Intent

The product is a local-first observer for changing feature state. A developer runs:

```bash
helm docs/exec-plans/current/<feature-slug>
```

The TUI then parses and renders the work item, continuously polls the source files, and refreshes the visible state as `prd.md`, `fdd.md`, `plan.md`, and `requirements.yml` change.
