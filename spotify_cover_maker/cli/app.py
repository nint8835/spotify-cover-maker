from pathlib import Path

import typer
from rich.console import Console
from rich.progress import track

from spotify_cover_maker.models import GeneratedCoverState, save_state_data
from spotify_cover_maker.rendering import PlanMode, RenderPlan, render, to_png

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

    if len(plan.covers) == 0:
        console.print("No covers have changed.", style="green")
        return

    for cover in track(plan.covers, description="Generating covers..."):
        png_filename = plan.config.path_for(cover)

        svg_data = render(cover)
        to_png(svg_data, png_filename)

        plan.state.generated_covers[cover.name] = GeneratedCoverState.for_cover(cover)

    save_state_data(plan.state, state_path)


@app.callback()
def callback() -> None:
    pass
