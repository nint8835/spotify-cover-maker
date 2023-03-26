from pathlib import Path

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from spotify_cover_maker.cli.ui import UIRoot
from spotify_cover_maker.rendering import PlanMode, RenderPlan

app = typer.Typer(
    help="Utility for automatically generating cover images for Spotify playlists."
)
console = Console()


@app.command(name="generate")
def generate(
    mode: PlanMode = typer.Option(
        PlanMode.changed, help="Selection of covers to generate."
    ),
    covers_path: Path = typer.Option(
        "covers.yaml", help="Path to the file containing your cover definitions."
    ),
    state_path: Path = typer.Option(
        ".scm_state.yaml", help="Path to the file that cover state should be saved in."
    ),
) -> None:
    """Generate cover images."""

    plan = RenderPlan(mode, covers_path=covers_path, state_path=state_path)

    if len(plan) == 0:
        console.print("No covers have changed.", style="green")
        return

    plan.render(
        progress=Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console,
        )
    )


@app.command(name="manage")
def manage(
    covers_path: Path = typer.Option(
        "covers.yaml", help="Path to the file containing your cover definitions."
    ),
    state_path: Path = typer.Option(
        ".scm_state.yaml", help="Path to the file that cover state should be saved in."
    ),
) -> None:
    """Open the cover management UI."""
    UIRoot.cover_path = covers_path
    UIRoot.state_path = state_path

    UIRoot().run()


@app.callback()
def callback() -> None:
    pass
