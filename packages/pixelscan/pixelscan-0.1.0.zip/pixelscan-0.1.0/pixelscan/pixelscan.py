#!/usr/bin/python

# AUTHOR
#   Daniel Pulido <dpmcmlxxvi@gmail.com>
# COPYRIGHT
#   Copyright (c) 2015 Daniel Pulido <dpmcmlxxvi@gmail.com>
# LICENSE
#   MIT License (http://opensource.org/licenses/MIT)

"""
Various patterns to scan pixels on a grid. Rectangular patterns are scanned
first along the x-coordinate then the y-coordinate. Radial patterns are
scanned counter-clockwise. Transformation filters are available to apply
standard transformations (e.g., rotation, scale, translation) on the
coordinates.
"""

import math
import random
import sys

# ======================================================================
# Distance metrics
# ----------------------------------------------------------------------

def chebyshev(point1, point2):
    """
    Computes distance between points using chebyshev metric
    :param point1: 1st point
    :param point2: 2nd point
    :returns: Distance between point1 and point2
    """

    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def manhattan(point1, point2):
    """
    Computes distance between points using manhattan metric
    :param point1: 1st point
    :param point2: 2nd point
    :returns: Distance between point1 and point2
    """

    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# ======================================================================
# Scan transformations
# ----------------------------------------------------------------------

class reflection:
    """
    Reflect coordinates about x and y axes
    """
    def __init__(self, scan, rx=False, ry=False):
        """
        :param scan: Pixel scan generator
        :param rx: True if x coordinate should be reflected (default=False)
        :param ry: True if y coordinate should be reflected (default=False)
        """
        self.scan = scan
        self.rx = rx
        self.ry = ry

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        return -x if self.rx else x, -y if self.ry else y

class rotation:
    """
    Rotate coordinates by given angle
    """

    def __init__(self, scan, angle=0):
        """
        :param scan: Pixel scan generator
        :param angle: Counter-clockwise angle in degrees (default=0)
        :warning: If the final transformation axes do not align with the x
                  and y axes then it may yield duplicate coordinates during
                  scanning.
        """
        self.scan = scan
        self.angle = angle * (math.pi / 180.0)

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        ca, sa = math.cos(self.angle), math.sin(self.angle)
        xr = ca * x - sa * y
        yr = sa * x + ca * y
        return xr, yr

class sample:
    """
    Randomly sample points at the given probability.
    """
    def __init__(self, scan, probability=1):
        """
        :param scan: Pixel scan generator
        :param step: Sampling probability in interval [0,1] (default=1)
        :warning: Will sample an unknown number of points unless set to 1.
        """
        if probability < 0 or probability > 1:
            raise ValueError("Sampling probability must be in range [0,1]")
        self.scan = scan
        self.probability = probability

    def __iter__(self):
        return self

    def next(self):
        if self.probability == 1:
            x, y = next(self.scan)
        else:
            while True:
                x, y = next(self.scan)
                if random.random() <= self.probability: break
        return x, y

class scale:
    """
    Scale coordinates by given factor
    """

    def __init__(self, scan, sx=1, sy=1):
        """
        :param scan: Pixel scan generator
        :param sx: X-coordinate scale factor (default=1)
        :param sy: Y-coordinate scale factor (default=1)
        """
        if sx <= 0: raise ValueError("X-scale must be positive")
        if sy <= 0: raise ValueError("Y-scale must be positive")
        self.scan = scan
        self.sx = sx
        self.sy = sy

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        xr = self.sx * x
        yr = self.sy * y
        return xr, yr

class skip:
    """
    Skip points at the given step size
    """
    def __init__(self, scan, start=0, stop=sys.maxint, step=1):
        """
        :param scan: Pixel scan generator
        :param start: Iteration starting 0-based index (default = 0)
        :param stop: Iteration stopping 0-based index (default = sys.maxint)
        :param step: Iteration step size (default = 1)
        """
        if start < 0: raise ValueError("Start must be non-negative")
        if stop < 0: raise ValueError("Stop must be non-negative")
        if step <= 0: raise ValueError("Step must be positive")
        self.scan = scan
        self.start = start
        self.stop = stop
        self.step = step
        self.index = -1

    def __iter__(self):
        return self

    def next(self):
        while True:
            x, y = next(self.scan)
            self.index += 1
            if (self.index < self.start): continue
            if (self.index > self.stop): continue
            if ((self.index-self.start) % self.step != 0): continue
            return x, y

class snap:
    """
    Snap x and y coordinates to a grid point
    """
    def __init__(self, scan):
        """
        :param scan: Pixel scan generator
        """
        self.scan = scan

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        xs = int(round(x))
        ys = int(round(y))
        return xs, ys

class swap:
    """
    Swap x and y coordinates
    """
    def __init__(self, scan):
        """
        :param scan: Pixel scan generator
        """
        self.scan = scan

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        return y, x

class translation:
    """
    Translate coordinates by given offset
    """

    def __init__(self, scan, tx=0, ty=0):
        """
        :param scan: Pixel scan generator
        :param sx: X-coordinate translation offset (default = 0)
        :param sy: Y-coordinate translaation offset (default = 0)
        """
        self.scan = scan
        self.tx = tx
        self.ty = ty

    def __iter__(self):
        return self

    def next(self):
        x, y = next(self.scan)
        xr = x + self.tx
        yr = y + self.ty
        return xr, yr

# ======================================================================
# Scan patterns
# ----------------------------------------------------------------------

def circlescan(x0, y0, r1, r2):
    """
    Scan pixels in a circle pattern around a center point
    :param x0: Center x-coordinate
    :param y0: Center y-coordinate
    :param r1: Initial radius
    :param r2: Final radius
    :returns: Coordinate generator
    """

    # Validate inputs
    if r1 < 0: raise ValueError("Initial radius must be non-negative")
    if r2 < 0: raise ValueError("Final radius must be non-negative")

    # List of pixels visited in previous diameter
    previous = []
    
    # Scan distances outward (1) or inward (-1)
    rstep = 1 if r2 >= r1 else -1
    for distance in range(r1, r2 + rstep, rstep):

        if distance == 0:

            yield x0, y0

        else:

            # Computes points for first octant and the rotate by multiples of
            # 45 degrees to compute the other octants
            a = 0.707107
            rotations = {0: [[ 1, 0], [ 0, 1]],
                         1: [[ a, a], [-a, a]],
                         2: [[ 0, 1], [-1, 0]],
                         3: [[-a, a], [-a,-a]],
                         4: [[-1, 0], [ 0,-1]],
                         5: [[-a,-a], [ a,-a]],
                         6: [[ 0,-1], [ 1, 0]],
                         7: [[ a,-a], [ a, a]]}
            nangles = len(rotations)

            # List of pixels visited in current diameter
            current = []

            for angle in range(nangles):
                x = 0
                y = distance
                d = 1 - distance
                while x < y:
                    xr = rotations[angle][0][0] * x + rotations[angle][0][1] * y
                    yr = rotations[angle][1][0] * x + rotations[angle][1][1] * y
                    xr = x0 + xr
                    yr = y0 + yr
                    
                    # First check  if point was in previous diameter
                    # since our scan pattern can lead to duplicates in
                    # neighboring diameters
                    point = (int(round(xr)), int(round(yr)))
                    if point not in previous:
                        yield xr, yr
                        current.append(point)

                    # Move pixel according to circle constraint
                    if (d < 0):
                        d += 3 + 2 * x
                    else:
                        d += 5 - 2 * (y-x)
                        y -= 1
                    x += 1

            previous = current

def gridscan(xi, yi, xf, yf, stepx=1, stepy=1):
    """
    Scan pixels in a grid pattern along the x-coordinate then y-coordinate
    :param xi: Initial x coordinate
    :param yi: Initial y coordinate
    :param xf: Final x coordinate
    :param yf: Final y coordinate
    :param stepx: Number of pixel to skip during scan in x-coordinate
    :param stepy: Number of pixel to skip during scan in y-coordinate
    :returns: Coordinate generator
    """

    if stepx <= 0: raise ValueError("X-step must be positive")
    if stepy <= 0: raise ValueError("Y-step must be positive")

    # Determine direction to move
    dx = stepx if xf >= xi else -stepx
    dy = stepy if yf >= yi else -stepy

    for y in range(yi, yf + dy, dy):
        for x in range(xi, xf + dx, dx):
            yield x, y

def randomscan(xi, yi, xf, yf, npoints):
    """
    Scan pixels in a region in a random pattern. This is only useful if you
    need exactly 'npoints' sampled. Otherwise use the 'sample'
    transformation to randomly sample at a given rate.
    :param xi: Initial x coordinate
    :param yi: Initial y coordinate
    :param xf: Final x coordinate
    :param yf: Final y coordinate
    :param npoints: Sample size
    :returns: Coordinate generator
    """

    # Validate inputs
    if npoints <= 0: raise ValueError("Sample size must be positive")

    # Partition then entire range of unwrapped indexes into bins and then
    # pick a random pixel in each bin
    nx = xf - xi + 1
    ny = yf - yi + 1
    npixels = nx * ny
    binsize = min(npixels, max(1, int(npixels / npoints)))

    for point in range(0, npoints):

        # Wrap index if oversampling pixels
        point = point % npixels

        # Compute random index
        pi = point * binsize
        pf = (point + 1) * binsize - 1 if point < npoints-1 else npixels-1
        index = random.randint(pi, pf)

        # Convert point from unwrapped index to x-y coordinate
        x = xi + index % nx
        y = yi + index / nx
        yield x, y

def ringscan(x0, y0, r1, r2, metric=chebyshev):
    """
    Scan pixels in a ring pattern around a center point counter-clockwise
    :param x0: Center x-coordinate
    :param y0: Center y-coordinate
    :param r1: Initial radius
    :param r2: Final radius
    :param metric: Distance metric
    :returns: Coordinate generator
    """

    # Validate inputs
    if r1 < 0: raise ValueError("Initial radius must be non-negative")
    if r2 < 0: raise ValueError("Final radius must be non-negative")
    if not hasattr(metric, "__call__"): raise TypeError("Metric is not callable")

    # Define counter-clockwise step directions
    direction = 0
    steps = {0: [ 1, 0],
             1: [ 1,-1],
             2: [ 0,-1],
             3: [-1,-1],
             4: [-1, 0],
             5: [-1, 1],
             6: [ 0, 1],
             7: [ 1, 1]}
    nsteps = len(steps)

    center = [x0, y0]
    
    # Scan distances outward (1) or inward (-1)
    rstep = 1 if r2 >= r1 else -1
    for distance in range(r1, r2 + rstep, rstep):

        initial = [x0, y0 + distance]
        current = initial

        # Number of tries to find a valid neighrbor
        ntrys = 0

        while True:

            # Short-circuit special case
            if distance == 0:
                yield current[0], current[1]
                break

            # Try and take a step and check if still within distance
            next = [current[i] + steps[direction][i] for i in range(2)]
            if metric(center, next) != distance:

                # Check if we tried all step directions and failed
                ntrys += 1
                if ntrys == nsteps:
                    break
                
                # Try the next direction
                direction = (direction + 1) % nsteps
                continue

            ntrys = 0
            yield current[0], current[1]

            # Check if we have come all the way around
            current = next
            if current == initial:
                break

        # Check if we tried all step directions and failed
        if ntrys == nsteps:
            break

def snakescan(xi, yi, xf, yf):
    """
    Scan pixels in a snake pattern along the x-coordinate then y-coordinate
    :param xi: Initial x coordinate
    :param yi: Initial y coordinate
    :param xf: Final x coordinate
    :param yf: Final y coordinate
    :returns: Coordinate generator
    """

    # Determine direction to move
    dx = 1 if xf >= xi else -1
    dy = 1 if yf >= yi else -1

    # Scan pixels first along x-coordinate then y-coordinate and flip
    # x-direction when the end of the line is reached
    x, xa, xb = xi, xi, xf
    for y in range(yi, yf + dy, dy):
        for x in range(xa, xb + dx, dx):
            yield x, y

        # Swap x-direction
        if x == xa or x == xb:
            dx *= -1
            xa, xb = xb, xa
