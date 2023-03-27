from pathlib import Path

import filetype

from spotify_cover_maker.models.covers import GradientCover
from spotify_cover_maker.rendering import render, to_png

GRADIENT_SINGLE_LINE_HEADING = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        
        <text x="104.209px" y="182.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">Testing</text>
        
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        
        <text x="69.495px" y="918.468px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:100px;fill:white;">Title</text>
        
        
        <text x="69.495px" y="1001.8px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:75px;fill:white;">Subtitle</text>
        
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:rgb(72,188,191);stop-opacity:1" />
            <stop offset="1" style="stop-color:rgb(108,68,120);stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>"""


def test_render_gradient_with_single_line_heading() -> None:
    svg_result = render(
        GradientCover(
            name="single_line_heading",
            template="gradient",
            heading_lines=["Testing"],
            title="Title",
            subtitle="Subtitle",
        )
    )

    assert svg_result == GRADIENT_SINGLE_LINE_HEADING


GRADIENT_MULTI_LINE_HEADING = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        
        <text x="104.209px" y="182.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">Testing</text>
        
        <text x="104.209px" y="307.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">2</text>
        
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        
        <text x="69.495px" y="918.468px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:100px;fill:white;">Title</text>
        
        
        <text x="69.495px" y="1001.8px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:75px;fill:white;">Subtitle</text>
        
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:rgb(0,97,74);stop-opacity:1" />
            <stop offset="1" style="stop-color:rgb(95,113,69);stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>"""


def test_render_gradient_with_multi_line_heading() -> None:
    svg_result = render(
        GradientCover(
            name="multi_line_heading",
            template="gradient",
            heading_lines=["Testing", "2"],
            title="Title",
            subtitle="Subtitle",
        )
    )

    assert svg_result == GRADIENT_MULTI_LINE_HEADING


GRADIENT_NO_SUBTITLE = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        
        <text x="104.209px" y="182.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">Testing</text>
        
        <text x="104.209px" y="307.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">2</text>
        
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        
        <text x="69.495px" y="978.7014px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:100px;fill:white;">Title</text>
        
        
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:rgb(183,83,225);stop-opacity:1" />
            <stop offset="1" style="stop-color:rgb(100,14,34);stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>"""


def test_render_gradient_with_no_subtitle() -> None:
    svg_result = render(
        GradientCover(
            name="no_subtitle",
            template="gradient",
            heading_lines=["Testing", "2"],
            title="Title",
            subtitle=None,
        )
    )

    assert svg_result == GRADIENT_NO_SUBTITLE


GRADIENT_NO_SUBTITLE_OR_TITLE = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        
        <text x="104.209px" y="182.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">Testing</text>
        
        <text x="104.209px" y="307.254px" style="font-family:'sans-serif', sans-serif;font-weight:800;font-size:125px;fill:white;">2</text>
        
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        
        
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:rgb(71,150,2);stop-opacity:1" />
            <stop offset="1" style="stop-color:rgb(162,161,88);stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>"""


def test_render_gradient_with_no_subtitle_or_title() -> None:
    svg_result = render(
        GradientCover(
            name="no_subtitle_or_title",
            template="gradient",
            heading_lines=["Testing", "2"],
            title=None,
            subtitle=None,
        )
    )

    assert svg_result == GRADIENT_NO_SUBTITLE_OR_TITLE


GRADIENT_CUSTOM_FONT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100%" height="100%" viewBox="0 0 1000 1000" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" xmlns:serif="http://www.serif.com/" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
    <g transform="matrix(1,0,0,1,-0.953232,-1.59316)">
        <rect x="0.953" y="1.593" width="1000.02" height="1000.02" style="fill:url(#_Linear1);" />
    </g>

    <g transform="matrix(1,0,0,1,-66.5839,-51.5039)">
        
        <text x="104.209px" y="182.254px" style="font-family:'PragmataPro', sans-serif;font-weight:800;font-size:125px;fill:white;">Testing</text>
        
        <text x="104.209px" y="307.254px" style="font-family:'PragmataPro', sans-serif;font-weight:800;font-size:125px;fill:white;">2</text>
        
    </g>
    <g transform="matrix(1,0,0,1,-29.3949,-42.7013)">
        
        
    </g>
    <defs>
        <linearGradient id="_Linear1" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(1000.33,719.597,-719.597,1000.33,3.43297,122.534)">
            <stop offset="0" style="stop-color:rgb(94,195,200);stop-opacity:1" />
            <stop offset="1" style="stop-color:rgb(148,184,169);stop-opacity:1" />
        </linearGradient>
    </defs>
</svg>"""


def test_render_gradient_with_custom_font() -> None:
    svg_result = render(
        GradientCover(
            name="custom_font",
            template="gradient",
            heading_lines=["Testing", "2"],
            title=None,
            subtitle=None,
            font="PragmataPro",
        )
    )

    assert svg_result == GRADIENT_CUSTOM_FONT


def test_to_png_produces_png(tmp_path: Path) -> None:
    png_path = tmp_path / "test.png"

    to_png(
        svg_data="<svg></svg>",
        png_path=png_path,
    )

    assert png_path.exists()
    assert filetype.guess(png_path).mime == "image/png"
