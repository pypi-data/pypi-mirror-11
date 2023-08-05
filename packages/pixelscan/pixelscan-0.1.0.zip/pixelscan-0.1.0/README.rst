=========
pixelscan
=========

The **pixelscan** library provides functions to scan pixels on a grid in a
variety of spatial patterns. The library consists of scan generators and
coordinate transformations. Scan generators are Python generators that return
pixel coordinates in a particular spatial pattern. Coordinate transformations
are iterators that apply spatial transformations to the coordinates created by
the scan generators. Transformation can be chained to yield very generic
transformations.

***************
Usage
***************

The typical calling syntax is

.. code-block:: python

   for x, y in transformation(generator(...), ...):
      foo(x,y)

For example, the following scans pixels in a counter-clockwise circular pattern
from the origin up to a radius of 1

.. code-block:: python

   for x, y in circlescan(0, 0, 0, 1):
      print x, y

and will generate the following points 

.. code-block:: python

   (0,0), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)

To skip every other pixel a skip transformation can be applied

.. code-block:: python

   for x, y in skip(circlescan(0, 0, 0, 1), step=2):
      print x, y

which will generate the following points

.. code-block:: python

   (0,0), (1,1), (1,-1), (-1,-1), (-1,1)

***************
Scan Generators
***************

The following are the currently available generators

- **circlescan**
   Generates pixels in a counter-clockwise circular pattern
- **gridscan**
   Generates pixels in rectangular grid pattern
- **randomscan**
   Generates pixels in a random pattern within a grid
- **ringscan**
   Generates pixels in a ring pattern (squares or diamonds)
- **snakescan**
   Generates pixels by in a snake pattern along the x then y axis

**************************
Coordinate Transformations
**************************

The following are the currentl available transformations

- **reflection**
   Reflects the coordinates along the x and/or y axis
- **rotation**
   Rotates the coordinates about the origin
- **sample**
   Randomly samples the pixels with a given probability
- **scale**
   Scales the coordinates with a given scale factors
- **skip**
   Skips the pixels with the given step size
- **snap**
   Snap the x and y coordinates to a grid point
- **swap**
   Swap the x and y coordinates
- **translation**
   Translates the coordinates by the given offsets

***************
Warnings
***************

Transformations such as the **rotation** can yield non-grid points.
They can be snapped to a grid point using the **snap** transformation.

***************
Changelog
***************

- v0.1.0
   Initial release
