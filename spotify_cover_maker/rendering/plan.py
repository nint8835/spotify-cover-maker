import os
from enum import Enum

from spotify_cover_maker.models import (
    Cover,
    CoverFile,
    GeneratedCoverState,
    StateFile,
    load_cover_data,
    load_state_data,
)


class PlanMode(str, Enum):
    changed = "changed"
    missing = "missing"
    all = "all"


class RenderPlan:
    covers: list[Cover]

    config: CoverFile
    state: StateFile

    state_path: str | os.PathLike[str]

    def __init__(
        self,
        mode: PlanMode,
        covers_path: str | os.PathLike[str] = "covers.yaml",
        state_path: str | os.PathLike[str] = ".scm_state.yaml",
    ) -> None:
        self.covers = []
        self.state_path = state_path
        self.config = load_cover_data(covers_path)
        self.state = load_state_data(state_path)

        for cover in self.config.covers:
            match mode:
                case PlanMode.all:
                    self.covers.append(cover)
                case PlanMode.missing:
                    if (
                        cover.name not in self.state.generated_covers
                        or not self.config.path_for(cover).exists()
                    ):
                        self.covers.append(cover)
                case PlanMode.changed:
                    if (
                        cover.name not in self.state.generated_covers
                        or self.state.generated_covers[cover.name]
                        != GeneratedCoverState.for_cover(cover)
                    ):
                        self.covers.append(cover)
