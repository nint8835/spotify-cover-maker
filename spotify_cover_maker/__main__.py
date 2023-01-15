import yaml
from rich.progress import track

from .render import render, to_png
from .template_data import parse_template_data

with open("covers.yaml") as f:
    covers_yaml = yaml.safe_load(f)
    covers = parse_template_data(covers_yaml)

for cover in track(covers, description="Generating covers..."):
    png_filename = "covers/" + cover.name + ".png"

    svg_data = render(cover)
    to_png(svg_data, png_filename)
