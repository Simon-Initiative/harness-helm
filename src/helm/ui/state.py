from __future__ import annotations

from dataclasses import dataclass

VIEW_SEQUENCE = ("overview", "prd", "fdd", "plan", "requirements")


@dataclass(slots=True)
class UIState:
    active_view: str = "overview"
    selected_phase_index: int = 0
    selected_requirement_index: int = 0
    last_status_message: str = "initial load"
