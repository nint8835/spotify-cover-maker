from pathlib import Path

from cairosvg import svg2png
from jinja2 import Environment, PackageLoader

from spotify_cover_maker.models import Cover


def render(cover: Cover) -> str:
    return (
        Environment(loader=PackageLoader("spotify_cover_maker", "templates"))
        .get_template(cover.template + ".svg")
        .render(
            **cover.get_template_data(),
        )
    )


def to_png(
    svg_data: str, png_path: Path, *, width: int = 1000, height: int = 1000
) -> None:
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg2png(
        bytestring=svg_data.encode(),
        write_to=str(png_path),
        output_width=width,
        output_height=height,
    )
