import importlib
import sys

import numpy as np
import pytest
import traja
from yupi import Trajectory

from yupiwrap.traja import traja2yupi, yupi2traja

X = [0.0, 1.0, 0.63, -0.37]
Y = [0.0, 0.0, 0.98, 1.24]
T = [0.0, 1.0, 2.5, 4.0]


def test_yupi_to_traja() -> None:
    frame = yupi2traja(Trajectory(x=X, y=Y, t=T))
    assert isinstance(frame, traja.TrajaDataFrame)
    assert frame.x.tolist() == X
    assert frame.y.tolist() == Y
    assert frame.time.tolist() == T


def test_traja_to_yupi() -> None:
    track = traja2yupi(traja.TrajaDataFrame({"x": X, "y": Y, "time": T}))
    assert isinstance(track, Trajectory)
    assert np.array_equal(track.r.x, X)
    assert np.array_equal(track.r.y, Y)
    assert np.array_equal(track.t, T)


def test_round_trip() -> None:
    original = Trajectory(x=X, y=Y, t=T)
    result = traja2yupi(yupi2traja(original))
    assert np.array_equal(result.r, original.r)
    assert np.array_equal(result.t, original.t)


def test_only_planar_trajectories_convert() -> None:
    with pytest.raises(ValueError, match="incompatible dimensions"):
        yupi2traja(Trajectory(x=X, y=Y, z=T))


def test_import_without_the_extra_says_what_to_install(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "traja", None)
    monkeypatch.delitem(sys.modules, "yupiwrap.traja")
    with pytest.raises(ImportError, match=r"yupiwrap\[traja\]"):
        importlib.import_module("yupiwrap.traja")
