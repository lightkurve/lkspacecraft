.. image:: https://github.com/lightkurve/lkspacecraft/actions/workflows/pytest.yml/badge.svg
    :target: https://github.com/lightkurve/lkspacecraft/actions/workflows/pytest.yml
    :alt: Test status

.. image:: https://badge.fury.io/py/lkspacecraft.svg
    :target: https://badge.fury.io/py/lkspacecraft
    :alt: PyPI version

.. image:: https://img.shields.io/badge/documentation-live-blue.svg
    :target: https://lightkurve.github.io/lkspacecraft/
    :alt: Documentation


lkspacecraft
============

.. <!-- intro content start -->

This package provides a way to access the orbital parameters for the
Kepler and TESS spacecrafts. This will enable you to access

1. Spacecraft position at any given time with respect to the solar
   system barycenter, the earth, or the moon
2. Spacecraft velocity at any given time with respect to the solar
   system barycenter, the earth, or the moon
3. The baycentric time correction for any target RA/Dec at any time
4. The velocity aberration for any target RA/Dec at any time



.. image:: https://raw.githubusercontent.com/lightkurve/lkspacecraft/main/docs/images/tess_wrt_earth.png
   :width: 400px
   :alt: TESS position with respect to the earth.

Requirements
------------

This package relies heavily on
`spiceypy <https://github.com/AndrewAnnex/SpiceyPy>`__ which wraps
`SPICE <https://naif.jpl.nasa.gov/naif/toolkit.html>`__. It also relies
on `astropy <https://www.astropy.org/>`__.

Installation
------------

You can install this package with ``pip`` using

.. code-block:: console

   pip install lkspacecraft --upgrade

You can also install this package by cloning the repo and then
installing via poetry

.. code-block:: console

   git clone https://github.com/lightkurve/lkspacecraft.git
   cd lkspacecraft
   pip install --upgrade poetry
   poetry install .


Usage
-----

``lkspacecraft`` provides ``Spacecraft`` object which will enable you to
access the orbital parameters of either the Kepler or TESS spacecraft.
``lkspacecraft`` will obtain the relevant SPICE kernels to calculate the
spacecraft position and velocity. To get the orbital elements you will
need to pick a time that is within the relevant window of those SPICE
kernels (i.e. when the mission was operational).

You can find the start and end times of the kernels using the following

.. code-block:: python

   from lkspacecraft import KeplerSpacecraft

   ks = KeplerSpacecraft()
   ks.start_time, ks.end_time

All times in ``lkspacecraft`` use ``astropy.time.Time`` objects. Using the
``get_spacecraft_position`` or ``get_spacecraft_velocity`` functions
will provide you with the position or velocity in cartesian coordinates,
for example

.. code-block:: python

   from lkspacecraft import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_spacecraft_velocity(t)

will result in

::

   array([[  6.94188023, -26.24714425, -11.16828662]])

This will give the velocity with respect to the solar system barycenter
by default, but you can specify the earth or moon using

.. code-block:: python

   from lkspacecraft import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_spacecraft_velocity(time=t, observer="earth")

You are able to calculate the light arrival time of observations of a
source at a given RA/Dec using ``lkspacecraft``\ ’s
``get_barycentric_time_correction`` function. This will give you the
time delay in seconds from spacecraft time to time at the barycenter.

.. code-block:: python

   from lkspacecraft import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_barycentric_time_correction(time=t, ra=290.666, dec=44.5)

Finally you can calculate velocity aberration using

.. code-block:: python

   from lkspacecraft import KeplerSpacecraft
   from astropy.time import Time

   ks = KeplerSpacecraft()
   t = Time("2009-04-06 06:22:56.000025")
   ks.get_velocity_aberrated_positions(time=t, ra=290.666, dec=44.5)

Units
~~~~~

In ``lkspacecraft``, just as in ``SPICE``, units are ``km`` and ``s``, unless
otherwise specified.

Kernels
-------

``lkspacecraft`` will obtain the SPICE kernels for Kepler and TESS for you
store them. Kernels can be found here:

The generic kernels can be obtained from NAIF generic kernels:
https://naif.jpl.nasa.gov/pub/naif/generic_kernels/
The Kepler kernels can be obtained from MAST:
https://archive.stsci.edu/missions/kepler/spice/ 
The K2 kernels can be obtained from MAST: 
https://archive.stsci.edu/missions/k2/spice/ The
TESS kernels can be obtained from MAST:
https://archive.stsci.edu/missions/tess/engineering/
https://archive.stsci.edu/missions/tess/models/

When you first load `lkspacecraft` into Python all the kernels will be downloaded for you. This will take approximately 5 minutes, depending on your internet connection. Once this has been done, the kernels will be cached. If there are new TESS kernels available `lkspacecraft` will retrieve them for you and update the cache. 

The total file volume for the kernels is ~1GB. These cached files are stored using `astropy`'s cache. If you want to clear the cache you can do either of the following;

.. code-block:: python

   from lkspacecraft.utils import clear_download_cache
   clear_download_cache()
   
.. code-block:: python

   from astropy.utils.data import clear_download_cache
   clear_download_cache(pkgname='lkspacecraft')



Extending ``lkspacecraft``
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you wanted to extend ``lkspacecraft`` to include more spacecraft you would
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

.. code-block:: python

       t = np.asarray(hdulist[1].data['TIME'], dtype=float)
       tcorr = np.asarray(hdulist[1].data['TIMECORR'], dtype=float)
       # Spacecraft time:
       t -= tcorr

If you are trying to accurately calculate time corrections, it is
important you use the spacecraft time in all functions.


.. <!-- intro content end -->

.. <!-- quickstart content start -->


The easiest way to install ``lkspacecraft`` and all of its dependencies is to use the ``pip`` command,
which is a standard part of all Python distributions. (upon release)

To install ``lkspacecraft``, run the following command in a terminal window:

.. code-block:: console

  $ python -m pip install lkspacecraft --upgrade

The ``--upgrade`` flag is optional, but recommended if you already
have ``lkspacecraft`` installed and want to upgrade to the latest version.

You can use `lkspacecraft` to access position and velocity information of Kepler and TESS using input times

.. code-block:: python

  from lkspacecraft import KeplerSpacecraft
  ks = KeplerSpacecraft()
  t = Time("2009-04-06 06:22:56.000025")
  ks.get_velocity_aberrated_positions(time=t, ra=290.666, dec=44.5)

.. <!-- quickstart content end -->

.. <!-- Contributing content start -->

Contributing
============

``lkspacecraft``  is an open-source, community driven package. 
We welcome users to contribute and develop new features for ``lkspacecraft``.  

For further information, please see the `Lightkurve Community guidelines <https://docs.lightkurve.org/development/contributing.html>`_.

.. <!-- Contributing content end -->

.. <!-- Citing content start -->

Citing
======

If you find ``lkspacecraft`` useful in your research, please cite it and give us a GitHub star!

If you use Lightkurve for work or research presented in a publication, we request the following acknowledgment or citation:

`This research made use of Lightkurve, a Python package for Kepler and TESS data analysis (Lightkurve Collaboration, 2018).`

See full citation instuctions, including dependencies, in the `Lightkurve documentation <https://docs.lightkurve.org/about/citing.html>`_. 

.. <!-- Citing content end -->

.. <!-- Contact content start -->

Contact
=======

``lkspacecraft`` is an open source community project created by the `TESS Science Support Center`_.  The best way to contact us is to `open an issue`_ or to e-mail tesshelp@bigbang.gsfc.nasa.gov.
 
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
v1.0.5
   - Added a function for calculating DVA
v1.0.4
   - Made Python version >=3.9 compliant
v1.0.3
   - Added ability to calculate velocity aberration on an array of RA/Decs.
   - Added ability to calculate barycentric time correction on an array of RA/Decs.
v1.0.0
   - First version

.. <!-- Changelog content end -->