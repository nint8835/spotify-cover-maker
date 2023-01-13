import yaml
from cairosvg import svg2png
from jinja2 import Environment, PackageLoader
from rich.progress import track

from .template_data import parse_template_data

env = Environment(loader=PackageLoader("spotify_cover_maker", "templates"))

with open("covers.yaml") as f:
    covers_yaml = yaml.safe_load(f)
    covers = parse_template_data(covers_yaml)

for cover in track(covers, description="Generating covers..."):
    png_filename = "covers/" + cover.name + ".png"

    svg_data = env.get_template(cover.template + ".svg").render(
        **cover.get_template_data(),
    )
    svg2png(
        bytestring=svg_data.encode(),
        write_to=png_filename,
        output_width=1000,
        output_height=1000,
    )
