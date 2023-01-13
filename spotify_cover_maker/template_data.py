import random
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, parse_obj_as


class TemplateDataBase(BaseModel):
    name: str

    def get_template_data(self) -> dict[str, Any]:
        return {}


class GradientTemplateData(TemplateDataBase):
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


# Discriminated unions require 2 or more types, so this needs to be commented out until there's a second template type
# TemplateData = Annotated[GradientTemplateData, Field(discriminator="template")]
TemplateData = GradientTemplateData


def parse_template_data(data: list[dict[str, Any]]) -> list[TemplateData]:
    return parse_obj_as(list[TemplateData], data)
