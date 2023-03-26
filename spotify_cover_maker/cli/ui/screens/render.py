import asyncio
from pathlib import Path

from rich.progress import Progress
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import TextLog

from spotify_cover_maker.rendering import PlanMode, RenderPlan


class RenderScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, cover_path: Path, state_path: Path):
        self.cover_path = cover_path
        self.state_path = state_path

        super().__init__()

    def compose(self) -> ComposeResult:
        yield TextLog()

    def render_covers(self, log: TextLog) -> None:
        log.write("Generating render plan...")
        plan = RenderPlan(PlanMode.changed, self.cover_path, self.state_path)

        log.write(f"\nRender plan - {len(plan.covers)} covers")
        for cover in plan.covers:
            log.write(f" - {cover.name}")

        plan.render(progress=Progress(console=self.app.console))
        self.app.console.show_cursor(False)

        log.write("\nDone! Press Esc to exit.")

    async def on_mount(self) -> None:
        log = self.query_one(TextLog)
        asyncio.create_task(asyncio.to_thread(self.render_covers, log))
