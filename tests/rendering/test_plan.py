from pathlib import Path

import yaml
from pytest import MonkeyPatch

from spotify_cover_maker.models.covers import CoverFile, GradientCover
from spotify_cover_maker.models.state import GeneratedCoverState, StateFile
from spotify_cover_maker.rendering import PlanMode, RenderPlan

test_path = Path(__file__).parent / "plan_test"


def test_plan_mode_all() -> None:
    plan = RenderPlan(
        PlanMode.all, test_path / "covers.yaml", test_path / ".scm_state.yaml"
    )

    assert plan.covers == [
        GradientCover(name="new", template="gradient"),
        GradientCover(name="changed_data", template="gradient"),
        GradientCover(name="changed_template", template="gradient"),
        GradientCover(name="missing_file", template="gradient"),
    ]
    assert len(plan) == 4


def test_plan_mode_changed() -> None:
    plan = RenderPlan(
        PlanMode.changed, test_path / "covers.yaml", test_path / ".scm_state.yaml"
    )

    assert plan.covers == [
        GradientCover(name="new", template="gradient"),
        GradientCover(name="changed_data", template="gradient"),
        GradientCover(name="changed_template", template="gradient"),
    ]
    assert len(plan) == 3


def test_plan_mode_missing() -> None:
    plan = RenderPlan(
        PlanMode.missing, test_path / "covers.yaml", test_path / ".scm_state.yaml"
    )

    assert plan.covers == [
        GradientCover(name="new", template="gradient"),
        GradientCover(name="missing_file", template="gradient"),
    ]
    assert len(plan) == 2


def test_plan_render(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    test_cover = GradientCover(name="test", template="gradient")

    with open("covers.yaml", "w") as f:
        yaml.safe_dump(
            CoverFile(covers=[test_cover]).dict(),
            f,
        )

    plan = RenderPlan(PlanMode.all, Path("covers.yaml"), Path(".scm_state.yaml"))

    assert plan.covers == [test_cover]
    assert len(plan) == 1

    plan.render()

    assert Path(".scm_state.yaml").exists()
    assert Path("covers").is_dir()
    assert Path("covers", "test.png").is_file()

    with open(".scm_state.yaml") as f:
        state = StateFile.parse_obj(yaml.safe_load(f))

        assert state == StateFile(
            generated_covers={"test": GeneratedCoverState.for_cover(test_cover)}
        )
