import logging
import yupi

try:
    import traja
except (ModuleNotFoundError, ImportError):
    logging.error(f'''Fail at importing 'traja' library

You can refer to https://github.com/traja-team/traja#installation-and-setup''')


def yupi2traja(yupi_trajectory: yupi.Trajectory) -> traja.TrajaDataFrame:
    """Converts a yupi trajectory to a traja dataframe.

    Parameters
    ----------
    yupi_trajectory : yupi.Trajectory
        Yupi trajectory input.

    Returns
    -------
    traja.TrajaDataFrame
        Resulting traja dataframe.

    Raises
    ------
    ValueError
        If the yupi trajectory dimension is not equal 2.
    """

    if yupi_trajectory.dim != 2:
        raise ValueError("Trajectory object has incompatible dimensions with traja")
    
    x = yupi_trajectory.r.x
    y = yupi_trajectory.r.y
    t = yupi_trajectory.t
    return traja.TrajaDataFrame({"x": x, "y": y, "time": t})

def traja2yupi(traja_trajectory: traja.TrajaDataFrame) -> yupi.Trajectory:
    """Converts a traja dataframe to a yupi trajectory.

    Parameters
    ----------
    traja_trajectory : traja.TrajaDataFrame
        Traja dataframe input.

    Returns
    -------
    yupi.Trajectory
        Resulting yupi trajectory.
    """

    x = traja_trajectory.x.to_numpy()
    y = traja_trajectory.y.to_numpy()
    t = traja_trajectory.time.to_numpy()
    return yupi.Trajectory(x=x, y=y, t=t)