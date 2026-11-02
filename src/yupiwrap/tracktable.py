from collections.abc import Callable, Iterable
from datetime import datetime
from typing import Any

import numpy as np
import yupi

try:
    import tracktable.domain.cartesian2d as tdt_2d
    import tracktable.domain.cartesian3d as tdt_3d
    import tracktable.domain.terrestrial as tdt_ter
except ImportError as error:
    raise ImportError(
        "The tracktable conversions need the tracktable extra: pip install 'yupiwrap[tracktable]'"
    ) from error

from yupiwrap.utils import seconds2datetime

PLANAR = 2
SPATIAL = 3

TracktableTrajectory = Any


def yupi2tracktable(
    yupi_trajectory: yupi.Trajectory,
    time_conv: Callable[[np.ndarray, datetime | None], Iterable[datetime]] = seconds2datetime,
    init_datetime: datetime | None = None,
    is_terrestrial: bool = False,
) -> TracktableTrajectory:
    """Converts a yupi trajectory to a tracktable trajectory.

    Parameters
    ----------
    yupi_trajectory : yupi.Trajectory
        Yupi trajectory input.
    time_conv : Callable[[np.ndarray], Iterable], optional
        This function translates theyupi trajectory time array to a
        datetime iterable, by default ``yupiwrap.utils.seconds2datetime``.
    init_datetime : datetime, optional
        Initial datetime taken as reference for the construction of the
        datetime iterable, by default None.
    is_terrestrial : bool, optional
        If True the returned tracktable trajectory will be of terrestial
        type instead of the default cartesian type, by default False.

    Returns
    -------
    TracktableTrajectory
        The result tracktable trajectory.

    Raises
    ------
    ValueError
        If the yupi trajectory dimension is not 2 or 3.
    """

    if yupi_trajectory.dim not in (PLANAR, SPATIAL):
        raise ValueError("Trajectory object has incompatible dimensions with tracktable")

    domain = _domain(yupi_trajectory.dim, is_terrestrial)
    track_points = []
    dates = time_conv(yupi_trajectory.t, init_datetime)
    for tp, date in zip(yupi_trajectory, dates, strict=True):
        point = _make_point(domain, tp.r, is_terrestrial)
        point.object_id = yupi_trajectory.traj_id
        point.timestamp = date
        track_points.append(point)
    return domain.Trajectory.from_position_list(track_points)


def tracktable2yupi(tracktable_trajectory: TracktableTrajectory) -> yupi.Trajectory:
    """Converts a tracktable trajectory to a yupi trajectory

    Parameters
    ----------
    tracktable_trajectory : TracktableTrajectory
        Tracktable trajectory input.

    Returns
    -------
    yupi.Trajectory
        Resulting yupi trajectory.

    Raises
    ------
    ValueError
        If the input is not a valid tracktable trajectory
    """

    is_ter = isinstance(tracktable_trajectory, tdt_ter.Trajectory)
    is_2d = isinstance(tracktable_trajectory, tdt_2d.Trajectory)
    is_3d = isinstance(tracktable_trajectory, tdt_3d.Trajectory)

    if is_ter + is_2d + is_3d != 1:
        raise ValueError("Invalid tracktable trajectory")

    points: list[list[float]] = []
    t: list[float] = []
    timestamps = [point.timestamp for point in tracktable_trajectory]
    for point, timestamp in zip(tracktable_trajectory, timestamps, strict=True):
        if is_ter:
            points.append([point[1], point[0]])
        elif is_2d:
            points.append([point[0], point[1]])
        else:
            points.append([point[0], point[1], point[2]])
        t.append((timestamp - timestamps[0]).total_seconds())
    return yupi.Trajectory(points=points, t=t)


def _domain(dimensions: int, is_terrestrial: bool) -> Any:
    if is_terrestrial:
        return tdt_ter
    return tdt_2d if dimensions == PLANAR else tdt_3d


def _make_point(domain: Any, position: np.ndarray, is_terrestrial: bool) -> Any:
    if not is_terrestrial:
        return domain.TrajectoryPoint(*position)
    point = domain.TrajectoryPoint(position[0], position[1])
    if len(position) == SPATIAL:
        point.properties["altitude"] = position[2]
    return point
