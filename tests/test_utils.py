from datetime import datetime, timedelta

import numpy as np

from yupiwrap.utils import seconds2datetime


def test_offsets_are_added_to_the_initial_datetime() -> None:
    start = datetime(2021, 1, 1, 12, 0, 0)
    result = seconds2datetime(np.array([0.0, 1.5, 90000.0]), start)
    assert list(result) == [
        start,
        start + timedelta(seconds=1.5),
        start + timedelta(days=1, seconds=3600),
    ]


def test_without_an_initial_datetime_it_starts_now() -> None:
    before = datetime.now()
    first = next(iter(seconds2datetime(np.array([0.0]))))
    assert before <= first <= datetime.now()
