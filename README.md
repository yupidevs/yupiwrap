# yupi_wrap

This repository contains functions to simplify the conversion of Trajectory data
among [yupi](https://yupi.readthedocs.io/en/latest/) and other useful software 
libraries designed for analyzing trajectories. 

Standing for *Yet Underused Path Instruments*, [yupi](https://yupi.readthedocs.io/en/latest/) is a set of tools designed 
for collecting, generating and processing trajectory data. The structure of yupi 
aims to standardize the usage and storage of general purpose trajectories 
independently of its dimensions. We believe it is useful to be able to convert, 
when possible, yupi trajectories to the data structures used by other libraries to
empower our users with the tools offered by third parties. With the same spirit, 
we offer the possibility of converting data from other libraries to yupi trajectories. 

## Installation

Current recommended installation method is via the pypi package:

```cmd
pip install yupi_wrap
```

It will install required dependencies such as [yupi package](https://pypi.org/project/yupi/) from pypi.

## Compatible libraries

### traja

The [Traja Python package](https://traja.readthedocs.io/en/latest/index.html) is a toolkit for the numerical characterization and analysis of the trajectories of moving animals. It provides several machine learning tools that are not yet implemented in yupi. Even when it is limited to two-dimensional trajectories, there are many resources that traja can offer when dealing with 2D Trajectories in [yupi](https://yupi.readthedocs.io/en/latest/). 

#### Converting a *yupi.Trajectory* into a *traja DataFrame*

Let's create a trajectory with yupi:

```python
from yupi import Trajectory

x = [0, 1.0, 0.63, -0.37, -1.24, -1.5, -1.08, -0.19, 0.82, 1.63, 1.99, 1.85]
y = [0, 0, 0.98, 1.24, 0.69, -0.3, -1.23, -1.72, -1.63, -1.01, -0.06, 0.94]

track = Trajectory(x=x, y=y, traj_id="Spiral")
```

We can convert it to a traja DataFrame simply by:

```python
from yupi_wrap import yupi2traja

traja_track = yupi2traja(track)
```

⚠️ Only *yupi.Trajectory* objects with two dimensions can be converted to *traja DataFrame* due to traja limitations.


#### Converting a *traja DataFrame* into a *yupi.Trajectory* 

If you have a *traja DataFrame* you can always convert it to a *yupi.Trajectory* by using:

```python
from yupi_wrap import traja2yupi

yupi_track = traja2yupi(traja_track)
```
