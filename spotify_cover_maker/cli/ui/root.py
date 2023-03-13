from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header, Placeholder

from .sidebar import Sidebar


class UIRoot(App[None]):
    TITLE = "Spotify Cover Maker"
    CSS = """
    .app {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 3fr;
    }
    """
    BINDINGS = [Binding("a", "add_cover", "Add Cover", priority=True)]

    def action_add_cover(self) -> None:
        self.query_one(Sidebar).covers += ("test",)

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="app"):
            yield Sidebar()
            yield Placeholder("Editor")
        yield Footer()
