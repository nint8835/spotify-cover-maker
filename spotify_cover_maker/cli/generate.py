import typer
import yaml

from rich.progress import track

from spotify_cover_maker.template_data import parse_template_data
from spotify_cover_maker.render import render, to_png

generate_app = typer.Typer(help="Generate covers.")


@generate_app.command()
def legacy():
    """Generate covers using the legacy generation code."""
    with open("covers.yaml") as f:
        covers_yaml = yaml.safe_load(f)
        covers = parse_template_data(covers_yaml)

    for cover in track(covers, description="Generating covers..."):
        png_filename = "covers/" + cover.name + ".png"

        svg_data = render(cover)
        to_png(svg_data, png_filename)
