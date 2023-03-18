from spotify_cover_maker.models.covers import GradientCover

from .gradient import GradientEditor

CoverTypeMap = {
    GradientCover: GradientEditor,
}

__all__ = ["GradientEditor", "CoverTypeMap"]
