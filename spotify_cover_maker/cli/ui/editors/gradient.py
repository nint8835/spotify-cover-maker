from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Markdown

from spotify_cover_maker.models.covers import GradientCover


class GradientEditor(Widget):
    def __init__(self, cover: GradientCover):
        self.cover = cover

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Markdown(f"```json\n{self.cover.json(indent=2, sort_keys=True)}\n```")
