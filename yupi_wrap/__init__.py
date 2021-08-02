import matplotlib.pyplot as plt
import traja
import yupi
import numpy as np

def yupi2traja(yupi_trajectory):
    if yupi_trajectory.dim != 2:
        raise ValueError("Trajectory object has incompatible dimensions with traja")
    else:
        x = yupi_trajectory.r.x
        y = yupi_trajectory.r.y
        t = yupi_trajectory.t
        print(x)
    return traja.TrajaDataFrame({"x": x, "y": y, "time": t})

def traja2yupi(traja_trajectory):
    x = np.array(traja_trajectory.x)
    y = np.array(traja_trajectory.y)
    t = np.array(traja_trajectory.time)
    print(x)
    return yupi.Trajectory(x=x, y=y, t=t)