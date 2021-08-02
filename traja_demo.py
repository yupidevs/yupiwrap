from yupiwrap import yupi2traja, traja2yupi
from yupi import Trajectory

# Create a trajectory in yupi

points = [[0, 0], [1.0, 0], [0.63, 0.98], [-0.37, 1.24], [-1.24, 0.69],
          [-1.5, -0.3], [-1.08, -1.23], [-0.19, -1.72], [0.82, -1.63],
          [1.63, -1.01], [1.99, -0.06], [1.85, 0.94]]

track = Trajectory(points=points, traj_id="Spiral")

# Converting the trajectory to traja
traja_track = yupi2traja(track)

# Converting the trajectory from traja to yupi
yupi_track = traja2yupi(traja_track)

