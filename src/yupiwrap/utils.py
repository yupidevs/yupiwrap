from collections.abc import Iterable
from datetime import datetime, timedelta

import numpy as np


def seconds2datetime(time: np.ndarray, init_datetime: datetime | None = None) -> Iterable[datetime]:
    """Converts a time array of seconds to a datetime iterable

    Parameters
    ----------
    time : np.ndarray
        Time array input.
    init_datetime : datetime, optional
        Initial datetime, by default None.

        If None, then the initial datetime is taken as ``datetime.now()``.

    Returns
    -------
    Iterable[datetime]
        Resulting datetime iterable.
    """

    if init_datetime is None:
        init_datetime = datetime.now()
    return [init_datetime + timedelta(seconds=s) for s in time]
