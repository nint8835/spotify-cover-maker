import os
from enum import Enum

from rich.console import Console
from rich.progress import Progress

from spotify_cover_maker.models import (
    Cover,
    CoverFile,
    GeneratedCoverState,
    StateFile,
    load_cover_data,
    load_state_data,
    save_state_data,
)

from .render import render, to_png


class PlanMode(str, Enum):
    changed = "changed"
    missing = "missing"
    all = "all"


class RenderPlan:
    covers: list[Cover]

    config: CoverFile
    state: StateFile

    state_path: os.PathLike[str]

    def __init__(
        self,
        mode: PlanMode,
        covers_path: os.PathLike[str],
        state_path: os.PathLike[str],
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

    def __len__(self) -> int:
        return len(self.covers)

    def render(self, *, progress: Progress | None = None) -> None:
        if progress is None:
            # If the caller has not provided a progress bar for us to use, create a
            # silent one to allow for progress code to continue being used without
            # outputting to the terminal
            progress = Progress(console=Console(quiet=True))

        with progress:
            task = progress.add_task("Generating covers...", total=len(self.covers))

            for cover in self.covers:
                png_filename = self.config.path_for(cover)

                svg_data = render(cover)
                to_png(svg_data, png_filename)

                self.state.generated_covers[cover.name] = GeneratedCoverState.for_cover(
                    cover
                )

                progress.update(task, advance=1)

        save_state_data(self.state, self.state_path)
