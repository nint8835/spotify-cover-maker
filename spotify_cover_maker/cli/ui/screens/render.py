import asyncio
from pathlib import Path

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import TextLog

from spotify_cover_maker.rendering import PlanMode, RenderPlan


class RenderScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield TextLog()

    def render_covers(self, log: TextLog) -> None:
        log.write("Generating render plan...")
        log.refresh()
        # TODO: Take in paths from command line
        plan = RenderPlan(
            PlanMode.changed, Path("covers.yaml"), Path(".scm_state.yaml")
        )

        log.write(f"\nRender plan - {len(plan.covers)} covers")
        for cover in plan.covers:
            log.write(f" - {cover.name}")

        log.write("\nRendering covers...")
        plan.render()

        log.write("\nDone! Press Esc to exit.")

    async def on_mount(self) -> None:
        log = self.query_one(TextLog)
        asyncio.create_task(asyncio.to_thread(self.render_covers, log))
