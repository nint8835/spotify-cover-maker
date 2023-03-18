from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Markdown

from spotify_cover_maker.models import Cover

from .editors import CoverTypeMap

EMPTY_STATE = """# No cover selected
Select a cover from the sidebar to begin editing, or press `Ctrl+A` to add a new cover.
"""


class Editor(Widget):
    cover: reactive[Cover | None] = reactive(None)

    async def watch_cover(self, _: Cover | None, new: Cover | None) -> None:
        for child in self.children:
            await child.remove()

        if new is None:
            await self.mount(Markdown(EMPTY_STATE))
        else:
            await self.mount(CoverTypeMap[type(new)](new))

    def compose(self) -> ComposeResult:
        yield Markdown(EMPTY_STATE)
