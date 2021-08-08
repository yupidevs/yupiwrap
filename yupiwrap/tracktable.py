from datetime import datetime
import logging
import numpy as np
from typing import Callable, Iterable, Union
from yupiwrap.utils import seconds2datetime
import yupi

try:
    import tracktable.domain.terrestrial as tdt_ter
    import tracktable.domain.cartesian2d as tdt_2d
    import tracktable.domain.cartesian3d as tdt_3d
except (ModuleNotFoundError, ImportError):
    logging.error(f'''Fail at importing 'tracktable' library

You can refer to https://github.com/sandialabs/tracktable#getting-tracktable''')

TracktableTrajectory = Union[
    tdt_ter.Trajectory,
    tdt_2d.Trajectory,
    tdt_3d.Trajectory
]

def yupi2tracktable(yupi_trajectory: yupi.Trajectory,
                    time_conv: Callable[[np.ndarray], Iterable] = seconds2datetime,
                    init_datetime: datetime = None,
                    is_terrestrial = False) -> TracktableTrajectory:
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

    dates = time_conv(yupi_trajectory.t, init_datetime)
    track_points = []
    if yupi_trajectory.dim == 2:
        for tp, date in zip(yupi_trajectory, dates):
            if is_terrestrial:
                point = tdt_ter.TrajectoryPoint(tp.r[0], tp.r[1])
            else:
                point = tdt_2d.TrajectoryPoint(tp.r[0], tp.r[1])
            point.object_id = yupi_trajectory.id
            point.timestamp = date
            track_points.append(point)
        if is_terrestrial:
            return tdt_ter.Trajectory.from_position_list(track_points)
        else:
            return tdt_2d.Trajectory.from_position_list(track_points)
    elif yupi_trajectory.dim == 3:
        for tp, date in zip(yupi_trajectory, dates):
            if is_terrestrial:
                point = tdt_ter.TrajectoryPoint(tp.r[0], tp.r[1])
                point.properties['altitude'] = tp.r[2]
            else:
                point = tdt_3d.TrajectoryPoint(tp.r[0], tp.r[1], tp.r[2])
            point.object_id = yupi_trajectory.id
            point.timestamp = date
            track_points.append(point)
        if is_terrestrial:
            return tdt_ter.Trajectory.from_position_list(track_points)
        else:
            return tdt_3d.Trajectory.from_position_list(track_points)
    else:
        raise ValueError("Trajectory object has incompatible dimensions with tracktable")

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
        raise ValueError('Invalid tracktable trajectory')

    points, t = [], []
    init_date = None
    for i, point in enumerate(tracktable_trajectory):
        if i == 0:
            init_date: datetime = point.timestamp
        current_date: datetime = point.timestamp
        if is_ter:
            points.append([point[1], point[0]])
        elif is_2d:
            points.append([point[0], point[1]])
        else:
            points.append([point[0], point[1], point[2]])
        t.append((current_date - init_date).seconds)
    return yupi.Trajectory(points=points, t=t)
