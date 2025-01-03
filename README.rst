lkorbit
=======


.. <!-- intro content start -->

This package provides a way to access the orbital parameters for the
Kepler and TESS spacecrafts. This will enable you to access

1. Spacecraft position at any given time with respect to the solar
   system barycenter, the earth, or the moon
2. Spacecraft velocity at any given time with respect to the solar
   system barycenter, the earth, or the moon
3. The baycentric time correction for any target RA/Dec at any time
4. The velocity aberration for any target RA/Dec at any time

Requirements
------------

This package relies heavily on
`spiceypy <https://github.com/AndrewAnnex/SpiceyPy>`__ which wraps
`SPICE <https://naif.jpl.nasa.gov/naif/toolkit.html>`__. It also relies
on `astropy <https://www.astropy.org/>`__.

Installation
------------

You can install this package with ``pip`` using

::

   pip install lkorbit --upgrade

You can also install this package by cloning the repo and then
installing via poetry

::

   git clone https://github.com/lightkurve/lkorbit.git
   cd lkorbit
   pip install --upgrade poetry
   poetry install .

Usage
-----

``lkorbit`` provides ``Spacecraft`` object which will enable you to
access the orbital parameters of either the Kepler or TESS spacecraft.
``lkorbit`` will obtain the relevant SPICE kernels to calculate the
spacecraft position and velocity. To get the orbital elements you will
need to pick a time that is within the relevant window of those SPICE
kernels (i.e. when the mission was operational).

You can find the start and end times of the kernels using the following

.. code:: python

   from lkorbit import KeplerSpacecraft

   ks = KeplerSpacecraft()
   ks.start_time, ks.end_time

All times in ``lkorbit`` use ``astropy.time.Time`` objects. Using the
``get_spacecraft_position`` or ``get_spacecraft_velocity`` functions
will provide you with the position or velocity in cartesian coordinates,
for example

.. code:: python

   from lkorbit import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_spacecraft_velocity(t)

will result in

::

   array([[  6.94188023, -26.24714425, -11.16828662]])

This will give the velocity with respect to the solar system barycenter
by default, but you can specify the earth or moon using

.. code:: python

   from lkorbit import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_spacecraft_velocity(time=t, observer="earth")

You are able to calculate the light arrival time of observations of a
source at a given RA/Dec using ``lkorbit``\ ’s
``get_barycentric_time_correction`` function. This will give you the
time delay in seconds from spacecraft time to time at the barycenter.

.. code:: python

   from lkorbit import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_barycentric_time_correction(time=t, ra=290.666, dec=44.5)

Finally you can calculate velocity aberration using

.. code:: python

   from lkorbit import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_velocity_aberrated_positions(time=t, ra=290.666, dec=44.5)

Units
~~~~~

In ``lkorbit``, just as in ``SPICE``, units are ``km`` and ``s``, unless
otherwise specified.

Kernels
-------

``lkorbit`` will obtain the SPICE kernels for Kepler and TESS for you
store them within the packages ``src/lkorbit/data/kernels`` directory.
It will then munge them into a meta kernel on import.

The generic kernels can be obtained from NAIF generic kernels:
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/
The Kepler kernels can be obtained from MAST:
https://archive.stsci.edu/missions/kepler/spice/ 
The K2 kernels can be obtained from MAST: 
https://archive.stsci.edu/missions/k2/spice/ The
TESS kernels can be obtained from MAST:
https://archive.stsci.edu/missions/tess/engineering/
https://archive.stsci.edu/missions/tess/models/

Extending ``lkorbit``
~~~~~~~~~~~~~~~~~~~~~

If you wanted to extend ``lkorbit`` to include more spacecraft you would
need to include more kernels in the kernel directory and ensure they are
added to the meta kernel. You can then create a new class in the
``spacecraft.py`` module with the correct NAIF code.

Caveats
-------

Velocity Aberration vs. Differential Velocity Aberration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package will provide you **velocity aberration**. However, each of
these spacecrafts repoint during observations to account for the bulk
offset of velocity aberration. If you are interested in where stars will
fall on pixels, you should consider calculating the **differential
velocity aberration**.

Spacecraft Time
~~~~~~~~~~~~~~~

This package assumes you will provide time as the time **at the
spacecraft**. For SPOC products, this is the time in the ``'TIME'``
column of any fits file, with the time corrections from ``TIME_CORR``
subtracted. i.e.

.. code:: python

       t = np.asarray(hdulist[1].data['TIME'], dtype=float)
       tcorr = np.asarray(hdulist[1].data['TIMECORR'], dtype=float)
       # Spacecraft time:
       t -= tcorr

If you are trying to accurately calculate time corrections, it is
important you use the spacecraft time in all functions.


.. <!-- intro content end -->

.. <!-- quickstart content start -->


The easiest way to install ``lkorbit`` and all of its dependencies is to use the ``pip`` command,
which is a standard part of all Python distributions. (upon release)

To install ``lkorbit``, run the following command in a terminal window:

.. code-block:: console

  $ python -m pip install lkorbit --upgrade

The ``--upgrade`` flag is optional, but recommended if you already
have ``lkorbit`` installed and want to upgrade to the latest version.

Usage
-----

You can use `lkorbit` to access position and velocity information of Kepler and TESS using input times

.. code-block:: python

  from lkorbit import KeplerSpacecraft
  ks = KeplerSpacecraft()
  t = Time("2009-04-06 06:22:56.000025")
  ks.get_velocity_aberrated_positions(time=t, ra=290.666, dec=44.5)

.. <!-- quickstart content end -->

.. <!-- Contributing content start -->

Contributing
============

``lkorbit``  is an open-source, community driven package. 
We welcome users to contribute and develop new features for ``lkorbit``.  

For further information, please see the `Lightkurve Community guidelines <https://docs.lightkurve.org/development/contributing.html>`_.

.. <!-- Contributing content end -->

.. <!-- Citing content start -->

Citing
======

If you find ``lkorbit`` useful in your research, please cite it and give us a GitHub star!

If you use Lightkurve for work or research presented in a publication, we request the following acknowledgment or citation:

`This research made use of Lightkurve, a Python package for Kepler and TESS data analysis (Lightkurve Collaboration, 2018).`

See full citation instuctions, including dependencies, in the `Lightkurve documentation <https://docs.lightkurve.org/about/citing.html>`_. 

.. <!-- Citing content end -->

.. <!-- Contact content start -->

Contact
=======

``lkorbit`` is an open source community project created by the `TESS Science Support Center`_.  The best way to contact us is to `open an issue`_ or to e-mail tesshelp@bigbang.gsfc.nasa.gov.
 
  .. _`TESS Science Support Center`: https://heasarc.gsfc.nasa.gov/docs/tess/
  
  .. _`open an issue`: https://github.com/lightkurve/lksearch/issues/new

Please include a self-contained example that fully demonstrates your problem or question.


.. <!-- Contact content end -->

License
=======

This project is licensed under the MIT License. See the LICENSE file for
details.

.. <!-- Changelog content start -->

Changelog:
==========
v1.0.0
   - First version

.. <!-- Changelog content end -->