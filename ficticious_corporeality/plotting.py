# Plotting/GUI
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import numpy as np

def plot(manager):
    #Plot setup
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    xs = []
    ys = []
    #zs = [] Default is 0

    #Iterates through every particle in the first subsystem.
    #TODO: Expand to multi-colored and multi-subsystem plotting
    for i in range(manager.now.subsystems[0].get_particles().size):
        xs.append(manager.now.subsystems[0].get_particles()[i].loc[0])
        ys.append(manager.now.subsystems[0].get_particles()[i].loc[1])
    axes.scatter(xs, ys, zs=0, s = 20, c='red', depthshade = True)
    plt.show()
    print("test")
