
Karta - tidy package for geospatial computation
===============================================

*Karta* is a simple and fast framework for spatial analysis in Python.

Components:

- Clean geographically-aware vector and gridded data types
- Integration with pyproj to support a wide range of coordinate systems and
  transformations
- A selection of geographical analysis methods including geodetic length and
  area calculations, intersections, convex hulls, raster sampling and profiling,
  and grid warping
- IO for several common geographical formats, including GeoJSON, shapefiles
  (through pyshp), ESRI ASCII, and GeoTiff (through GDAL). Vector geometries
  implement ``__geo_interface__``.

*Karta* works with Python 2.7 and Python 3.3+.

DOCUMENTATION
-------------

See the `online manual <http://www.ironicmtn.com/kartadocs/karta-manual.html>`_,
read the tutorial_, or search the `API documentation`_.

.. _tutorial: http://www.ironicmtn.com/kartadocs/tutorial.html
.. _API documentation: http://www.ironicmtn.com/kartadocs/reference.html

The manual can also be built offline with Sphinx by running ``make`` from the
``doc/`` directory. The documentation is built from source code docstrings and
information in the `Wiki <https://github.com/njwilson23/karta/wiki/Tutorial>`_.


