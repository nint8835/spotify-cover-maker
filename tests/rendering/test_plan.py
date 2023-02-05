from pathlib import Path

from spotify_cover_maker.models.covers import GradientCover
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


def test_plan_mode_changed() -> None:
    plan = RenderPlan(
        PlanMode.changed, test_path / "covers.yaml", test_path / ".scm_state.yaml"
    )

    assert plan.covers == [
        GradientCover(name="new", template="gradient"),
        GradientCover(name="changed_data", template="gradient"),
        GradientCover(name="changed_template", template="gradient"),
    ]


def test_plan_mode_missing() -> None:
    plan = RenderPlan(
        PlanMode.missing, test_path / "covers.yaml", test_path / ".scm_state.yaml"
    )

    assert plan.covers == [
        GradientCover(name="new", template="gradient"),
        GradientCover(name="missing_file", template="gradient"),
    ]
