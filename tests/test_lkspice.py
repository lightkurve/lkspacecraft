import os
import numpy as np
import lkspice
from astropy.time import Time


def test_init():
    os.path.isfile(lkspice.PACKAGEDIR + "/data/Meta.txt")
    lkspice.KeplerSpacecraft()
    lkspice.TESSSpacecraft()


def test_kepler():
    ks = lkspice.KeplerSpacecraft()
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
