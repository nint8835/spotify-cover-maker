from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, Tree

from spotify_cover_maker.models import Cover, load_cover_data, save_cover_data
from spotify_cover_maker.models.covers import GradientCover

from .editor import Editor
from .screens import RenderScreen
from .sidebar import Sidebar


def fetch_initial_covers() -> tuple[Cover, ...]:
    cover_data = load_cover_data(UIRoot.cover_path)
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
        Binding("ctrl+d", "delete_cover", "Delete Cover"),
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+r", "render_covers", "Render Covers"),
    ]

    covers: reactive[tuple[Cover, ...]] = reactive(fetch_initial_covers)
    selected_cover: reactive[str | None] = reactive(None)

    cover_path: Path = Path("covers.yaml")
    state_path: Path = Path(".scm_state.yaml")

    def action_add_cover(self) -> None:
        self.covers = self.covers + (
            GradientCover(
                template="gradient", name=f"Unnamed Cover {len(self.covers)}"
            ),
        )

    def action_delete_cover(self) -> None:
        if self.selected_cover is not None:
            self.covers = tuple(
                cover for cover in self.covers if cover.name != self.selected_cover
            )
            self.selected_cover = None

    def action_save(self) -> None:
        existing_config = load_cover_data(UIRoot.cover_path)
        existing_config.covers = list(self.covers)
        save_cover_data(existing_config, UIRoot.cover_path)

    def action_render_covers(self) -> None:
        self.action_save()
        render_screen = RenderScreen(UIRoot.cover_path, UIRoot.state_path)
        self.push_screen(render_screen)

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

    def on_input_changed(self, message: Input.Changed) -> None:
        if message.input.id != "name":
            return

        next(
            cover for cover in self.covers if cover.name == self.selected_cover
        ).name = message.value
        self.query_one(Sidebar).covers = tuple(cover.name for cover in self.covers)
        if message.input.id == "name":
            self.selected_cover = message.value

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(classes="app"):
            yield Sidebar()
            yield Editor()
        yield Footer()
