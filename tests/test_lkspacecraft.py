import astropy.units as u
import numpy as np
import spiceypy
from astropy.time import Time

import lkspacecraft
from lkspacecraft.utils import KERNELS


def test_init():
    assert len(KERNELS) > 600
    lkspacecraft.KeplerSpacecraft()
    lkspacecraft.TESSSpacecraft()
    nkernels = spiceypy.ktotal("ALL")
    assert nkernels > 600


def test_kepler():
    ks = lkspacecraft.KeplerSpacecraft()
    assert ks.start_time > Time("2009-03-06 06:22:56.000025")
    assert ks.end_time < Time("2019-12-30 23:58:50.815000")
    t = Time("2009-04-06 06:22:56.000025")
    # Speed in km/s
    speed = np.sum(ks.get_spacecraft_velocity(t) ** 2) ** 0.5
    assert speed < 100
    dist = (np.sum(ks.get_spacecraft_position(t) ** 2) ** 0.5) * u.km.to(u.AU)
    # 1 AU from barycenter
    assert np.isclose(dist, 1, atol=0.05)

    start, end = ks.start_time, ks.end_time
    t = Time(np.linspace(start.jd + 1, end.jd - 1, 1000), format="jd")

    # Speed in km/s
    speed = np.sum(ks.get_spacecraft_velocity(t) ** 2) ** 0.5
    dist = (np.sum(ks.get_spacecraft_position(t) ** 2) ** 0.5) * u.km.to(u.AU)

    ra, dec = 285.6794224553767, +50.2413060048164
    tcorr = ks.get_barycentric_time_correction(t, ra, dec)
    assert np.isclose((tcorr.max() - tcorr.min()), 320, atol=5)
