from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Tree


class Sidebar(Widget):
    covers: reactive[tuple[str, ...]] = reactive(tuple())

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("Covers")
        tree.show_root = False

        yield tree

    def watch_covers(self, _: int, new: tuple[str]) -> None:
        tree = self.query_one(Tree)
        tree.clear()
        for cover in new:
            tree.root.add_leaf(cover, cover)
