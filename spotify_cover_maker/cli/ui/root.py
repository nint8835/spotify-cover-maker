from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Tree

from spotify_cover_maker.models import Cover, load_cover_data, save_cover_data
from spotify_cover_maker.models.covers import GradientCover

from .editor import Editor
from .sidebar import Sidebar


def fetch_initial_covers() -> tuple[Cover, ...]:
    # TODO: Take in path as argument
    cover_data = load_cover_data(Path("covers.yaml"))

    return tuple(cover_data.covers)


class UIRoot(App[None]):
    TITLE = "Spotify Cover Maker"
    CSS = """
    .app {
        layout: grid;
        grid-size: 2 1;
        grid-columns: 1fr 3fr;
    }
    """
    BINDINGS = [
        Binding("ctrl+a", "add_cover", "Add Cover"),
        Binding("ctrl+s", "save", "Save"),
    ]

    covers: reactive[tuple[Cover, ...]] = reactive(fetch_initial_covers)
    selected_cover: reactive[str | None] = reactive(None)

    def action_add_cover(self) -> None:
        self.covers = self.covers + (
            GradientCover(template="gradient", name=f"Test {len(self.covers)}"),
        )

    def action_save(self) -> None:
        existing_config = load_cover_data(Path("covers.yaml"))
        existing_config.covers = list(self.covers)
        save_cover_data(existing_config, Path("covers.yaml"))

    def watch_covers(self, _: list[Cover], new: list[Cover]) -> None:
        self.query_one(Sidebar).covers = tuple(cover.name for cover in new)

    def watch_selected_cover(self, _: str | None, new: str | None) -> None:
        editor = self.query_one(Editor)
        if new is None:
            self.sub_title = "No cover selected"
            editor.cover = None
        else:
            self.sub_title = new
            editor.cover = next(cover for cover in self.covers if cover.name == new)

    def on_tree_node_selected(self, message: Tree.NodeSelected[str]) -> None:
        self.selected_cover = message.node.data

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="app"):
            yield Sidebar()
            yield Editor()
        yield Footer()
