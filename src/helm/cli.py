from __future__ import annotations

import argparse

from helm.app import HelmApp
from helm.store import WorkItemStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="helm",
        description="Observe a harness work item in a Textual TUI.",
    )
    parser.add_argument("work_item_dir", help="Path to docs/exec-plans/current/<feature-slug>")
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Polling interval in seconds for checking work-item file changes.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = WorkItemStore(args.work_item_dir)
    app = HelmApp(store=store, poll_interval=max(0.2, args.poll_interval))
    app.run()
    return 0
