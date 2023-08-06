JIC Geometry
============

.. image:: https://badge.fury.io/py/jicgeometry.svg
   :target: http://badge.fury.io/py/jicgeometry
   :alt: PyPi package

.. image:: https://travis-ci.org/JIC-CSB/jicgeometry.svg?branch=master
   :target: https://travis-ci.org/JIC-CSB/jicgeometry
   :alt: Travis CI build status (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/skvp3sa9f5htpnkf?svg=true
   :target: https://ci.appveyor.com/project/tjelvar-olsson/jicgeometry
   :alt: AppVeyor CI build status (Windows)

.. image:: http://codecov.io/github/JIC-CSB/jicgeometry/coverage.svg?branch=master
   :target: http://codecov.io/github/JIC-CSB/jicgeometry?branch=master
   :alt: Code Coverage

.. image:: https://readthedocs.org/projects/jicgeometry/badge/?version=latest
   :target: https://readthedocs.org/projects/jicgeometry?badge=latest
   :alt: Documentation Status

Python package for basic geometry operations.

- Documentation: http://jicgeometry.readthedocs.org/en/latest/
- GitHub: https://github.com/JIC-CSB/jicgeometry
- PyPI: https://pypi.python.org/pypi/jicgeometry
- Free software: MIT License

Features
--------

- Lightweight: no dependencies outside Python's standard library
- Cross-platform: Linux, Mac and Windows are all supported
- Works with with Python 2.7, 3.2, 3.3, and 3.4


Quick Guide
-----------

To install ``jicgeometry``::

    sudo pip install jicgeometry

Create some points::

    >>> from jicgeometry import Point2D
    >>> p1 = Point2D(6, 1)
    >>> p2 = Point2D(3, 5)

Find the distances between two points::

    >>> p1.distance(p2)
    5.0

Add/subtract points from each other::

    >>> p1 + p2
    <Point2D(x=9, y=6, dtype=int)>

Scale points using multiplication/division::

    >>> p1 / 2.0
    <Point2D(x=3.00, y=0.50, dtype=float)>

Treat points as vectors::

    >>> p1.unit_vector
    <Point2D(x=0.99, y=0.16, dtype=float)>
    >>> round(p1.magnitude, 4)
    6.0828


History
-------

0.6.0
^^^^^

- Added Point3D class


0.5.0
^^^^^

- Initial upload to PyPi
