from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Markdown

from spotify_cover_maker.models import Cover

EMPTY_STATE = """# No cover selected
Select a cover from the sidebar to begin editing, or press `Ctrl+A` to add a new cover.
"""


class Editor(Widget):
    cover: reactive[Cover | None] = reactive(None)

    async def watch_cover(self, _: Cover | None, new: Cover | None) -> None:
        if new is None:
            await self.query_one(Markdown).update(EMPTY_STATE)
        else:
            await self.query_one(Markdown).update(
                f"# JSON representation\n"
                f"```json\n{new.json(indent=2, sort_keys=True)}\n```"
            )

    def compose(self) -> ComposeResult:
        yield Markdown(EMPTY_STATE)
