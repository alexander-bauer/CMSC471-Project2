#!/usr/bin/env python3

import time
import numpy as np
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot

from Optimize import *

def make_plot(f, best_point, paths):
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    pyplot.hold(True)

    x = y = np.arange(-2.5, 2.5, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array([f(x, y) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    ax.plot_surface(X, Y, Z, cmap = matplotlib.cm.hot, alpha=0.25)

    for path in paths:
        length = len(path)
        path_xs = []
        path_ys = []
        path_zs = []
        for index, (x, y) in enumerate(path):
            path_xs.append(x)
            path_ys.append(y)
            path_zs.append(f(x,y) + 0.01) # We add to the dot position so it
                                          # shows above the surface.
        ax.scatter(path_xs, path_ys, path_zs, s = 25)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z(x, y)')

    return fig

start = time.clock()
best_point, all_visited = hill_climb(z, 0.05, -2.5, 2.5, -2.5, 2.5, graph=True)
end = time.clock()
print("Hill climbing: z({:f}, {:f}) = {:f}".format(*best_point, z(*best_point)))
print("In {:f} seconds".format(end - start))

f1 = make_plot(z, best_point, all_visited)
f1.savefig('hill_climb.png')

start = time.clock()
best_point, all_visited = hill_climb_random_restart(z, 0.05, 10, -2.5, 2.5, -2.5, 2.5, graph=True)
end = time.clock()
print("Hill climbing with {} restarts: z({:f}, {:f}) = {:f}".format(10, *best_point, z(*best_point)))
print("In {:f} seconds".format(end - start))

f2 = make_plot(z, best_point, all_visited)
f2.savefig('hill_climb_random_restart.png')

start = time.clock()
best_point, all_visited = simulated_annealing(z, 0.1, 200, -2.5, 2.5, -2.5, 2.5, graph=True)
end = time.clock()
print("Simulated annealing with T = {}: z({:f}, {:f}) = {:f}".format(200, *best_point, z(*best_point)))
print("In {:f} seconds".format(end - start))

f3 = make_plot(z, best_point, all_visited)
f3.savefig('simulated_annealing.png')
