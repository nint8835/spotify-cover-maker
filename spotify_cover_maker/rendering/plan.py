import os
from enum import Enum

from spotify_cover_maker.models import (
    Cover,
    StateFile,
    load_cover_data,
    load_state_data,
)


class PlanMode(Enum):
    changed = "changed"
    missing = "missing"
    all = "all"


class RenderPlan:
    covers: list[Cover]
    state: StateFile

    state_path: str | os.PathLike[str]

    def __init__(self, state_path: str | os.PathLike[str]) -> None:
        self.covers = []
        self.state_path = state_path
        self.state = load_state_data(state_path)

    @classmethod
    def plan(
        cls,
        mode: PlanMode,
        covers_path: str | os.PathLike[str] = "covers.yaml",
        state_path: str | os.PathLike[str] = ".scm_state.yaml",
    ) -> "RenderPlan":
        plan = RenderPlan(state_path)

        covers_data = load_cover_data(covers_path)

        for cover in covers_data.covers:
            match mode:
                case PlanMode.all:
                    plan.covers.append(cover)
                case PlanMode.missing:
                    # TODO: Add cover to plan if file is missing from disk or state
                    pass
                case PlanMode.changed:
                    if (
                        cover.name not in plan.state.generated_covers
                        or plan.state.generated_covers[cover.name].should_render(cover)
                    ):
                        plan.covers.append(cover)

        return plan
