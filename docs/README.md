# lkspice

This package provides a way to access the orbital parameters for the Kepler and TESS spacecrafts. This will enable you to access

1. Spacecraft position at any given time with respect to the solar system barycenter, the earth, or the moon
2. Spacecraft velocity at any given time with respect to the solar system barycenter, the earth, or the moon
3. The baycentric time correction for any target RA/Dec at any time
4. The velocity aberration  for any target RA/Dec at any time

## Requirements

This package relies heavily on [`spiceypy`](https://github.com/AndrewAnnex/SpiceyPy) which wraps [SPICE](https://naif.jpl.nasa.gov/naif/toolkit.html). It also relies on [astropy](https://www.astropy.org/).

## Installation

You can install this package with `pip` using

```
pip install lkspice --upgrade
```

You can also install this package by cloning the repo and then installing via poetry

```
git clone https://github.com/lightkurve/lkspice.git
cd lkspice
pip install --upgrade poetry
poetry install .
```

## Usage

`lkspice` provides `Spacecraft` object which will enable you to access the orbital parameters of either the Kepler or TESS spacecraft. `lkspice` will obtain the relevant SPICE kernels to calculate the spacecraft position and velocity. To get the orbital elements you will need to pick a time that is within the relevant window of those SPICE kernels (i.e. when the mission was operational).

You can find the start and end times of the kernels using the following

```python
from lkspice import KeplerSpacecraft

ks = KeplerSpacecraft()
ks.start_time, ks.end_time
```

All times in `lkspice` use `astropy.time.Time` objects. Using the `get_spacecraft_position` or `get_spacecraft_velocity` functions will provide you with the position or velocity in cartesian coordinates, for example

```python
from lkspice import KeplerSpacecraft
from astropy.time import Time

ks = KeplerSpacecraft()
t = Time("2009-04-06 06:22:56.000025")
ks.get_spacecraft_velocity(t)
```

will result in

```
array([[  6.94188023, -26.24714425, -11.16828662]])
```

This will give the velocity with respect to the solar system barycenter by default, but you can specify the earth or moon using

```python
from lkspice import KeplerSpacecraft
from astropy.time import Time

ks = KeplerSpacecraft()
t = Time("2009-04-06 06:22:56.000025")
ks.get_spacecraft_velocity(time=t, observer="earth")
```

You are able to calculate the light arrival time of observations of a source at a given RA/Dec using `lkspice`'s `get_barycentric_time_correction` function. This will give you the time delay in seconds from spacecraft time to time at the barycenter.

```python
from lkspice import KeplerSpacecraft
from astropy.time import Time

ks = KeplerSpacecraft()
t = Time("2009-04-06 06:22:56.000025")
ks.get_barycentric_time_correction(time=t, ra=290.666, dec=44.5)
```

Finally you can calculate velocity aberration using

```python
from lkspice import KeplerSpacecraft
from astropy.time import Time

ks = KeplerSpacecraft()
t = Time("2009-04-06 06:22:56.000025")
ks.get_velocity_aberrated_positions(time=t, ra=290.666, dec=44.5)
```

### Units

In `lkspice`, just as in `SPICE`, units are `km` and `s`, unless otherwise specified.

## Kernels

`lkspice` will obtain the SPICE kernels for Kepler and TESS for you store them within the packages `src/lkspice/data/kernels` directory. It will then munge them into a meta kernel on import.

The generic kernels can be obtained from NAIF generic kernels:
    <https://naif.jpl.nasa.gov/pub/naif/generic_kernels/>
The Kepler kernels can be obtained from MAST:
    <https://archive.stsci.edu/missions/kepler/spice/>
The K2 kernels can be obtained from MAST:
    <https://archive.stsci.edu/missions/k2/spice/>
The TESS kernels can be obtained from MAST:
    <https://archive.stsci.edu/missions/tess/engineering/>
    <https://archive.stsci.edu/missions/tess/models/>

### Extending `lkspice`

If you wanted to extend `lkspice` to include more spacecraft you would need to include more kernels in the kernel directory and ensure they are added to the meta kernel. You can then create a new class in the `spacecraft.py` module with the correct NAIF code.

## Caveats

### Velocity Aberration vs. Differential Velocity Aberration

This package will provide you **velocity aberration**. However, each of these spacecrafts repoint during observations to account for the bulk offset of velocity aberration. If you are interested in where stars will fall on pixels, you should consider calculating the **differential velocity aberration**.

### Spacecraft Time

This package assumes you will provide time as the time **at the spacecraft**. For SPOC products, this is the time in the `'TIME'` column of any fits file, with the time corrections from `TIME_CORR` subtracted. i.e.

```python
    t = np.asarray(hdulist[1].data['TIME'], dtype=float)
    tcorr = np.asarray(hdulist[1].data['TIMECORR'], dtype=float)
    # Spacecraft time:
    t -= tcorr
```

If you are trying to accurately calculate time corrections, it is important you use the spacecraft time in all functions.

# Contributing

Contributions are welcome! If you find bugs or have feature requests, please submit an issue or a pull request.

# License

This project is licensed under the MIT License. See the LICENSE file for details.
