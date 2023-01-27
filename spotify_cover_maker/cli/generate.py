import typer
from rich.progress import track

from spotify_cover_maker.models import load_cover_data
from spotify_cover_maker.render import render, to_png

generate_app = typer.Typer(help="Generate covers.")


@generate_app.command()
def legacy() -> None:
    """Generate covers using the legacy generation code."""
    cover_data = load_cover_data()

    for cover in track(cover_data.covers, description="Generating covers..."):
        png_filename = "covers/" + cover.name + ".png"

        svg_data = render(cover)
        to_png(svg_data, png_filename)
