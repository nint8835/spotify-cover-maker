import yaml
from cairosvg import svg2png
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, parse_obj_as
from rich.progress import track


class Cover(BaseModel):
    template: str = "gradient.svg"

    name: str
    title: str
    subtitle: str


env = Environment(loader=FileSystemLoader("templates"))

with open("covers.yaml") as f:
    covers_yaml = yaml.safe_load(f)
    covers = parse_obj_as(list[Cover], covers_yaml)

for cover in track(covers, description="Generating covers..."):
    png_filename = "covers/" + cover.name + ".png"

    svg_data = env.get_template(cover.template).render(
        title=cover.title, subtitle=cover.subtitle
    )
    svg2png(
        bytestring=svg_data.encode(),
        write_to=png_filename,
        output_width=1000,
        output_height=1000,
    )
