import random

import yaml
from cairosvg import svg2png
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, parse_obj_as
from rich.progress import track


class Cover(BaseModel):
    template: str = "gradient.svg"

    heading_lines: list[str] = ["Favourite", "Songs"]

    name: str
    title: str | None = None
    subtitle: str | None = None


env = Environment(loader=FileSystemLoader("templates"))

with open("covers.yaml") as f:
    covers_yaml = yaml.safe_load(f)
    covers = parse_obj_as(list[Cover], covers_yaml)

for cover in track(covers, description="Generating covers..."):
    random.seed(cover.name)

    r1 = random.randint(0, 225)
    r2 = random.randint(0, 225)
    g1 = random.randint(0, 225)
    g2 = random.randint(0, 225)
    b1 = random.randint(0, 225)
    b2 = random.randint(0, 225)

    png_filename = "covers/" + cover.name + ".png"

    svg_data = env.get_template(cover.template).render(
        heading_lines=cover.heading_lines,
        title=cover.title,
        subtitle=cover.subtitle,
        colour_1=f"rgb({r1},{g1},{b1})",
        colour_2=f"rgb({r2},{g2},{b2})",
    )
    svg2png(
        bytestring=svg_data.encode(),
        write_to=png_filename,
        output_width=1000,
        output_height=1000,
    )
