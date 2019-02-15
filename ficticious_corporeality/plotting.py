# Plotting/GUI
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np

def plot(manager):
    #Plot setup
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    subsystems = manager.now.subsystems

    #Values of x, y, and z for all particle values
    xs = []
    ys = []
    zs = []

    #Iterates through every particle in the first subsystem.
    #TODO: Expand to multi-colored and multi-subsystem plotting. (Multi-subsystem is available, however there is only one sub-system being received at the moment.)
    for i in range(len(subsystems)):
        for j in range(subsystems[i].get_particles().size):
            xs.append(subsystems[i].get_particles()[j].loc[0])
            ys.append(subsystems[i].get_particles()[j].loc[1])
            zs.append(subsystems[i].get_particles()[j].loc[2])

    #Scatter plot subsystem particles.
    axes.scatter(xs, ys, zs, s = 20, c='blue', depthshade = True)
    plt.show()
