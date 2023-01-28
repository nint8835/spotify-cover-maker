import typer
from rich.console import Console
from rich.progress import track

from spotify_cover_maker.models import (
    Cover,
    GeneratedCoverState,
    load_cover_data,
    load_state_data,
    save_state_data,
)
from spotify_cover_maker.render import render, to_png

generate_app = typer.Typer(help="Generate covers.")
console = Console()


@generate_app.command()
def changed() -> None:
    """Generate all covers from covers.yaml which have changed since last run."""
    cover_data = load_cover_data()
    state_data = load_state_data()

    target_covers: list[Cover] = []

    for cover in cover_data.covers:
        if cover.name not in state_data.generated_covers or state_data.generated_covers[
            cover.name
        ].should_render(cover):
            target_covers.append(cover)

    if len(target_covers) == 0:
        console.print("No covers have changed.", style="green")
        return

    for cover in track(target_covers, description="Generating covers..."):
        png_filename = "covers/" + cover.name + ".png"

        svg_data = render(cover)
        to_png(svg_data, png_filename)

        state_data.generated_covers[cover.name] = GeneratedCoverState.generate_state(
            cover
        )

    save_state_data(state_data)
