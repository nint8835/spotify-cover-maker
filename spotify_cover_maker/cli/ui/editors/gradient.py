from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Input, Label

from spotify_cover_maker.models.covers import GradientCover


class GradientEditor(Widget):
    DEFAULT_CSS = """
    .editor_container {
        padding: 1;
    }

    .input_container {
        height: 5;
        width: 100%;
        margin-bottom: 1;
    }
    """

    def __init__(self, cover: GradientCover):
        super().__init__()

        self.cover = cover

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "title":
            self.cover.title = event.value if event.value else None
        elif event.input.id == "subtitle":
            self.cover.subtitle = event.value if event.value else None

    def compose(self) -> ComposeResult:
        with Container(classes="editor_container"):
            with Container(classes="input_container"):
                yield Label("Title")
                yield Input(value=self.cover.title, id="title")
            with Container(classes="input_container"):
                yield Label("Subtitle")
                yield Input(value=self.cover.subtitle, id="subtitle")
