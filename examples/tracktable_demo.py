from yupiwrap.tracktable import yupi2tracktable, tracktable2yupi
from yupi import Trajectory

# Converting the terrain trajectory to tracktable
points = [[-82.359415, 23.135012],[-82.382116, 23.136252]]
track_1 = Trajectory(points=points, traj_id="ter_track")

# Converting the 2D trajectory to tracktable
points = [[0, 0], [1.0, 0], [0.63, 0.98], [-0.37, 1.24], [-1.24, 0.69],
          [-1.5, -0.3], [-1.08, -1.23], [-0.19, -1.72], [0.82, -1.63],
          [1.63, -1.01], [1.99, -0.06], [1.85, 0.94]]
track_2 = Trajectory(points=points, traj_id="2d_track")

# Converting the 3D trajectory to tracktable
points = [[0,0,0], [1,1,3], [3,2,5]]
track_3 = Trajectory(points=points, traj_id="3d_track")


tracktable_track_1 = yupi2tracktable(track_1, is_terrestial=True)
tracktable_track_2 = yupi2tracktable(track_2)
tracktable_track_3 = yupi2tracktable(track_3)

# Converting the trajectory from tracktable to yupi
yupi_track_1 = tracktable2yupi(tracktable_track_1)
yupi_track_2 = tracktable2yupi(tracktable_track_2)
yupi_track_3 = tracktable2yupi(tracktable_track_3)

