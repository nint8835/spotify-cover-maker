from cairosvg import svg2png
from jinja2 import Environment, PackageLoader

from .template_data import TemplateData


def render(cover: TemplateData) -> str:
    return (
        Environment(loader=PackageLoader("spotify_cover_maker", "templates"))
        .get_template(cover.template + ".svg")
        .render(
            **cover.get_template_data(),
        )
    )


def to_png(
    svg_data: str, png_filename: str, *, width: int = 1000, height: int = 1000
) -> None:
    svg2png(
        bytestring=svg_data.encode(),
        write_to=png_filename,
        output_width=width,
        output_height=height,
    )
