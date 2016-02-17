#!/usr/bin/env python3

import math

def z(x, y):
    return (math.sin(x**2 + 3*y**2) / (0.1 + (x**2 + y**2))) \
            + ((x**2 + 5*y**2) * math.exp(1 - (x**2) + (y**2)) / 2)

def hill_climb(f, step, start_point=(0, 0), maxfunc=min):
    x, y = start_point

    # Loop until break.
    while True:
        # Store the current point to compare to the next selected point.
        old_x, old_y = x, y
        # Select the new best by taking the minimum new value of the function
        # from the surrounding points.
        x, y = maxfunc(
                [(x - step, y + step), (x, y + step), (x + step, y + step),
                 (x - step, y),        (x, y)       , (x + step, y),
                 (x - step, y - step), (x, y - step), (x + step, y - step)],
                key=lambda coord: f(*coord))

        # If the point we're already on is the minimum, break from the loop,
        # because we have found a local minimum.
        if (x, y) == (old_x, old_y):
            return x, y

def hill_climb_random_restart(f, step, restarts):
    pass

def simulated_annealing(f, step, max_temp):
    pass
