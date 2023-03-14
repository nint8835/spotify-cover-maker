from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Placeholder, Tree

from spotify_cover_maker.models import Cover
from spotify_cover_maker.models.covers import GradientCover

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

    covers: reactive[tuple[Cover, ...]] = reactive(tuple())
    selected_cover: reactive[str | None] = reactive(None)

    def action_add_cover(self) -> None:
        self.covers = self.covers + (
            GradientCover(template="gradient", name=f"Test {len(self.covers)}"),
        )

    def watch_covers(self, _: list[Cover], new: list[Cover]) -> None:
        self.query_one(Sidebar).covers = tuple(cover.name for cover in new)

    def watch_selected_cover(self, old: str | None, new: str | None) -> None:
        if new is None:
            self.sub_title = "No cover selected"
        else:
            self.sub_title = new

    def on_tree_node_selected(self, message: Tree.NodeSelected[str]) -> None:
        self.selected_cover = message.node.data

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="app"):
            yield Sidebar()
            yield Placeholder("Editor")
        yield Footer()
