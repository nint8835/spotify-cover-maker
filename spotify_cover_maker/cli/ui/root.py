from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.widgets import Header, Placeholder


class UIRoot(App[None]):
    TITLE = "Spotify Cover Maker"
    CSS = """
    .app {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 3fr;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Placeholder("Sidebar"),
            Placeholder("Editor"),
            classes="app"
        )
