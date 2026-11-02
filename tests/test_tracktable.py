import importlib
import sys
from datetime import UTC, datetime, timedelta
from typing import Any

import numpy as np
import pytest
import tracktable.domain.cartesian2d as tdt_2d
import tracktable.domain.cartesian3d as tdt_3d
import tracktable.domain.terrestrial as tdt_ter
from yupi import Trajectory

from yupiwrap.tracktable import tracktable2yupi, yupi2tracktable

PLANAR = [[0.0, 0.0], [1.0, 2.0], [3.0, 4.0]]
SPATIAL = [[0.0, 0.0, 0.0], [1.0, 1.0, 3.0], [3.0, 2.0, 5.0]]


@pytest.mark.parametrize(
    ("points", "domain"), [(PLANAR, tdt_2d), (SPATIAL, tdt_3d)], ids=["planar", "spatial"]
)
def test_cartesian_conversions_use_the_right_domain(points: list[list[float]], domain: Any) -> None:
    track = yupi2tracktable(Trajectory(points=points, traj_id="a"))
    assert isinstance(track, domain.Trajectory)


@pytest.mark.parametrize("points", [PLANAR, SPATIAL], ids=["planar", "spatial"])
def test_cartesian_round_trip(points: list[list[float]]) -> None:
    original = Trajectory(points=points, t=[0.0, 1.0, 3.0], traj_id="a")
    result = tracktable2yupi(yupi2tracktable(original))
    assert np.array_equal(result.r, original.r)
    assert np.array_equal(result.t, original.t)


@pytest.mark.parametrize(
    "times", [[0.0, 1.5, 3.25], [0.0, 90000.5, 180000.0]], ids=["fractions", "days"]
)
def test_times_survive_a_round_trip(times: list[float]) -> None:
    original = Trajectory(points=PLANAR, t=times, traj_id="a")
    assert tracktable2yupi(yupi2tracktable(original)).t.tolist() == pytest.approx(times)


def test_terrestrial_conversion_uses_the_terrestrial_domain() -> None:
    track = yupi2tracktable(Trajectory(points=PLANAR, traj_id="a"), is_terrestrial=True)
    assert isinstance(track, tdt_ter.Trajectory)


def test_terrestrial_points_can_have_an_altitude() -> None:
    track = yupi2tracktable(Trajectory(points=SPATIAL, traj_id="a"), is_terrestrial=True)
    assert [point.properties["altitude"] for point in track] == [0.0, 3.0, 5.0]


def test_the_trajectory_id_becomes_the_object_id() -> None:
    track = yupi2tracktable(Trajectory(points=PLANAR, traj_id="spiral"))
    assert {point.object_id for point in track} == {"spiral"}


def test_the_initial_datetime_is_used() -> None:
    start = datetime(2021, 1, 1, 12, 0, 0, tzinfo=UTC)
    track = yupi2tracktable(Trajectory(points=PLANAR, t=[0.0, 1.0, 3.0]), init_datetime=start)
    assert [point.timestamp for point in track] == [
        start,
        start + timedelta(seconds=1),
        start + timedelta(seconds=3),
    ]


def test_a_custom_time_conversion_is_used() -> None:
    fixed = datetime(2020, 2, 2, tzinfo=UTC)

    def convert(time: np.ndarray, _: datetime | None) -> list[datetime]:
        return [fixed + timedelta(days=int(value)) for value in time]

    track = yupi2tracktable(Trajectory(points=PLANAR, t=[0.0, 1.0, 2.0]), time_conv=convert)
    assert track[2].timestamp == fixed + timedelta(days=2)


def test_other_dimensions_are_rejected() -> None:
    with pytest.raises(ValueError, match="incompatible dimensions"):
        yupi2tracktable(Trajectory(x=[0.0, 1.0]))


def test_other_objects_are_rejected() -> None:
    with pytest.raises(ValueError, match="Invalid tracktable trajectory"):
        tracktable2yupi("not a trajectory")


def test_import_without_the_extra_says_what_to_install(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "tracktable.domain.cartesian2d", None)
    monkeypatch.delitem(sys.modules, "yupiwrap.tracktable")
    with pytest.raises(ImportError, match=r"yupiwrap\[tracktable\]"):
        importlib.import_module("yupiwrap.tracktable")
