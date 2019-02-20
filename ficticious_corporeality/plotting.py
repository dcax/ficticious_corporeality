# Plotting/GUI
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
import numpy as np
import pprint

def plot(manager):
    #Plot setup
    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    xs = []
    ys = []
    zs = []

    #zs = [] Default is 0

    #Iterates through every particle in the first subsystem and adds the respective x, y, z value to it's respective array.
    #TODO: Expand to multi-colored and multi-subsystem plotting
    for j in range(len(manager.now.subsystems)):
        for i in range(manager.now.subsystems[j].get_particles().size):
            xs.append(manager.now.subsystems[j].get_particles()[i].loc[0])
            ys.append(manager.now.subsystems[j].get_particles()[i].loc[1])
            zs.append(manager.now.subsystems[j].get_particles()[i].loc[2])
            print(vars(manager.now.subsystems[j]))
    axes.scatter(xs, ys, zs, s = 20, c='red', depthshade = True)
    plt.show()
