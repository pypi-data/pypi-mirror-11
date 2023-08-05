===============================
KiPart
===============================

.. image:: https://img.shields.io/pypi/v/kipart.svg
        :target: https://pypi.python.org/pypi/kipart


Part creator for KiCad.

* Free software: MIT license
* Documentation: https://kipart.readthedocs.org.

Features
--------

* Generates schematic part libraries for KiCad.
* Converts lists of pins in a CSV file into a multi-unit schematic part symbol.
* Converts multiple CSV files in .zip archives.
* Each row of the CSV file lists the number, name, type and unit of a pin.
* Pins on a unit with the same name (e.g., GND) are placed at the same location
  so they can all be tied to the same net with a single connection.
