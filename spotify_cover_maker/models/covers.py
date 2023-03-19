import hashlib
import json
import os
import random
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel


class CoverBase(BaseModel):
    name: str

    def get_template_data(self) -> dict[str, Any]:
        return {}

    def get_data_hash(self) -> str:
        return hashlib.sha512(
            json.dumps(self.get_template_data()).encode("utf8"), usedforsecurity=False
        ).hexdigest()


class GradientCover(CoverBase):
    template: Literal["gradient"]

    heading_lines: list[str] = ["Favourite", "Songs"]
    title: str | None = None
    subtitle: str | None = None

    def get_template_data(self) -> dict[str, Any]:
        random.seed(self.name)

        r1 = random.randint(0, 225)
        r2 = random.randint(0, 225)
        g1 = random.randint(0, 225)
        g2 = random.randint(0, 225)
        b1 = random.randint(0, 225)
        b2 = random.randint(0, 225)

        return {
            **super().get_template_data(),
            "colour_1": f"rgb({r1},{g1},{b1})",
            "colour_2": f"rgb({r2},{g2},{b2})",
            "heading_lines": self.heading_lines,
            "title": self.title,
            "subtitle": self.subtitle,
        }


# Discriminated unions require 2 or more types, so this needs to be commented out until
# there's a second template type
# Cover = Annotated[GradientCover, Field(discriminator="template")]
Cover = GradientCover


class CoverFile(BaseModel):
    covers: list[Cover]
    output_path: str = "covers"

    def path_for(self, cover: Cover) -> Path:
        return Path(self.output_path) / f"{cover.name}.png"


def load_cover_data(path: os.PathLike[str]) -> CoverFile:
    try:
        with open(path) as f:
            return CoverFile.parse_obj(yaml.safe_load(f))
    except FileNotFoundError:
        return CoverFile(covers=[])


def save_cover_data(cover_data: CoverFile, path: os.PathLike[str]) -> None:
    with open(path, "w") as f:
        yaml.dump(cover_data.dict(), f)
