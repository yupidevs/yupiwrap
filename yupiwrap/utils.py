from typing import Iterable
import numpy as np
from typing import Iterable
from datetime import datetime, timedelta

def seconds2datetime(time: np.ndarray, init_datetime=None) -> Iterable[datetime]:
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