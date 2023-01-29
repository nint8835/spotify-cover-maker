from pprint import pprint

import typer
from rich.console import Console
from rich.progress import track

from spotify_cover_maker.models import GeneratedCoverState, save_state_data
from spotify_cover_maker.rendering import PlanMode, RenderPlan, render, to_png

generate_app = typer.Typer(help="Generate covers.")
console = Console()


@generate_app.command()
def changed() -> None:
    """Generate all covers from covers.yaml which have changed since last run."""

    plan = RenderPlan.plan(PlanMode.changed)

    if len(plan.covers) == 0:
        console.print("No covers have changed.", style="green")
        return

    for cover in track(plan.covers, description="Generating covers..."):
        png_filename = "covers/" + cover.name + ".png"

        svg_data = render(cover)
        to_png(svg_data, png_filename)

        plan.state.generated_covers[cover.name] = GeneratedCoverState.for_cover(cover)

    save_state_data(plan.state)
