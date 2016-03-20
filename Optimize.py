#!/usr/bin/env python3

import math
import random

def z(x, y):
    return (math.sin(x**2 + 3*y**2) / (0.1 + (x**2 + y**2))) \
            + ((x**2 + 5*y**2) * math.exp(1 - (x**2 + y**2)) / 2)

class Domain():
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def random_coords(self):
        return random.uniform(self.xmin, self.xmax), \
                random.uniform(self.ymin, self.ymax)

    def __contains__(self, p):
        """Check if coordinates are in this Domain."""
        x, y = p
        return self.xmin <= x and x <= self.xmax \
                and self.ymin <= y and y <= self.ymax

def parameterized_annealing(f, step, restarts, domain, T_sched, optfunc=min,
        move_retries=18):
    """Simulated annealing is a superset of hill climbing, and hill climbing
    with restarts. By parameterizing this function in different ways, each
    desired function can be achieved.

    f:        function to be optimized.
    step:     the step size (a magnitude)
    restarts: number of times to restart from a random point (> 0)
    domain:   domain on which to optimize f: ((x_min, y_min), (x_max, y_max))
    T_sched:  the temperature, an infinite iterator; if none, accept no poor moves
    optfunc:  function to decide between two points, must support key function
    
    Returns tuple of optimal point and a list of lists of points visited on each
    restart: (best_point, [[r0p0, r0p1, ...], [r1p0, r1p1, ...], ...]).
    
    Note: if T is not an infinite iterator, then this function may fail."""
    best_point = None
    best = None
    all_visited = []

    def accept(current, new, T = None):
        if new < current:
            return True
        elif T != None:
            # If using a temperature, accept the bad move with a probability.
            return random.random() <= math.exp((new - current)/T)
        else:
            return False

    while restarts > 0:
        visited = []

        # Get a random point in the domain to visit.
        x, y = domain.random_coords()
        current = f(x, y)
        visited.append((x, y))

        move_attempts = 0

        # Get T if we are using it.
        T = next(T_sched) if T_sched else None

        # Iterate until no move seems good.
        while move_attempts < move_retries:
            # Pick a direction at random.
            direction = random.uniform(0, 2*math.pi)

            # Select another point with a distance of the step size from the
            # current point.
            next_x = x + math.cos(direction)*step
            next_y = y + math.sin(direction)*step
            new = f(next_x, next_y)

            # Check if we accept the move.
            if (x, y) in domain and accept(current, new, T):
                # Set the new point and log it.
                x, y = next_x, next_y
                current = new
                visited.append((x, y))

                # Get the next T if we are using it.
                T = next(T_sched) if T_sched else None

                # Reset the number of moves
                move_attempts = 0
            else:
                # Note that we've attempted a direction.
                move_attempts += 1

        # Record this restart attempt, and set the new best if appropriate.
        all_visited.append(visited)
        if best == None or current < best:
            best_point = (x, y)
            best = current

        # Restart and decrement the counter
        restarts -= 1

    return best_point, all_visited

def hill_climb(f, step, xmin, xmax, ymin, ymax, graph=False, **kwargs):
    """Naively hill_climb to the minimum of the function with no restarts. If
    graph is set, it will return (best_point, [visited_points])."""
    best_point, all_visited = parameterized_annealing(
            f, step, 1, Domain(xmin, xmax, ymin, ymax), None,
            **kwargs)
    if not graph:
        return best_point
    else:
        return best_point, all_visited

def hill_climb_random_restart(f, step, restarts, xmin, xmax, ymin, ymax,
        graph=False, **kwargs):
    """Naively hill_climb to the minimum of the function with restarts as given.
    Note that the number of restarts includes the first iteration. If graph is
    set, it will return (best_point, [visited_points])."""
    best_point, all_visited = parameterized_annealing(
            f, step, restarts, Domain(xmin, xmax, ymin, ymax), None,
            **kwargs)
    if not graph:
        return best_point
    else:
        return best_point, all_visited

def simulated_annealing(f, step, max_temp, xmin, xmax, ymin, ymax,
        graph=False, **kwargs):
    """Use simulated annealing to find the minimum of the function. If graph is
    set, it will return (best_point, [visited_points])."""
    
    # Define a T schedule: an infinite iterator which approaches zero but never
    # reaches it.
    def T_sched(T):
        while T > 0:
            yield T
            T -= 0.01
        # If T reaches 0 from float error, yield a small value forever.
        while True:
            yield 1e-15

    best_point, all_visited = parameterized_annealing(
            f, step, 1, Domain(xmin, xmax, ymin, ymax), T_sched(max_temp),
            **kwargs)
    if not graph:
        return best_point
    else:
        return best_point, all_visited
