import hashlib
import importlib.resources
import os
from functools import lru_cache
from typing import Any

import yaml
from pydantic import BaseModel

from spotify_cover_maker import templates

from .covers import Cover


@lru_cache(maxsize=None)
def get_template_hash(template: str) -> str:
    files = importlib.resources.files(templates)
    template_file = files.joinpath(template + ".svg").read_bytes()

    return hashlib.sha512(template_file, usedforsecurity=False).hexdigest()


class GeneratedCoverState(BaseModel):
    data_hash: str
    template_hash: str

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GeneratedCoverState):
            return False

        return (
            self.template_hash == other.template_hash
            and self.data_hash == other.data_hash
        )

    @classmethod
    def for_cover(cls, cover: Cover) -> "GeneratedCoverState":
        template_hash = get_template_hash(cover.template)
        cover_data_hash = cover.get_data_hash()

        return GeneratedCoverState(
            data_hash=cover_data_hash, template_hash=template_hash
        )


class StateFile(BaseModel):
    generated_covers: dict[str, GeneratedCoverState] = {}


def load_state_data(path: os.PathLike[str]) -> StateFile:
    if not os.path.isfile(path):
        return StateFile()

    with open(path) as f:
        return StateFile.parse_obj(yaml.safe_load(f))


def save_state_data(state: StateFile, path: os.PathLike[str]) -> None:
    with open(path, "w") as f:
        yaml.dump(state.dict(), f)
