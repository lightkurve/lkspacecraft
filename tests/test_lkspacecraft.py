import os

import astropy.units as u
import numpy as np
import pytest
from astropy.constants import c
from astropy.time import Time

import lkspacecraft


def test_tess_truncated():
    lkspacecraft.enable_test_mode()
    ts = lkspacecraft.TESSSpacecraft()
    assert ts.start_time > Time("2018-10-07 20:09:56.999998")
    assert ts.end_time < Time("2018-11-20 11:33:59.999999")
    time = Time("2018-11-01 13:00:00")
    ra = 300
    dec = 10
    velocity = ts.get_spacecraft_velocity(time, observer="EARTH")
    assert velocity.shape == (1, 3)
    position = ts.get_spacecraft_position(time, observer="EARTH")
    assert position.shape == (1, 3)
    lt = ts.get_spacecraft_light_travel_time(time)
    assert lt.shape == (1,)
    assert np.isclose(lt, 500, atol=50)
    ra_result, dec_result = ts.get_velocity_aberrated_positions(time, ra, dec)
    assert ra_result.shape == (1,)
    assert dec_result.shape == (1,)
    ra_result, dec_result = ts.get_differential_velocity_aberrated_positions(
        time, ra, dec, ra0=301, dec0=11
    )
    assert ra_result.shape == (1,)
    assert dec_result.shape == (1,)
    lkspacecraft.disable_test_mode()


def test_kepler_truncated():
    lkspacecraft.enable_test_mode()
    ks = lkspacecraft.spacecraft.KeplerSpacecraft()
    assert ks.start_time > Time("2010-07-23 20:09:56.999998")
    assert ks.end_time < Time("2010-07-27 11:33:59.999999")

    time = Time("2010-07-25 00:00:00")
    ra = 300
    dec = 10
    velocity = ks.get_spacecraft_velocity(time, observer="EARTH")
    assert velocity.shape == (1, 3)
    position = ks.get_spacecraft_position(time, observer="EARTH")
    assert position.shape == (1, 3)
    lt = ks.get_spacecraft_light_travel_time(time)
    assert lt.shape == (1,)
    assert np.isclose(lt, 500, atol=50)
    ra_result, dec_result = ks.get_velocity_aberrated_positions(time, ra, dec)
    assert ra_result.shape == (1,)
    assert dec_result.shape == (1,)
    ra_result, dec_result = ks.get_differential_velocity_aberrated_positions(
        time, ra, dec, ra0=301, dec0=11
    )
    assert ra_result.shape == (1,)
    assert dec_result.shape == (1,)
    lkspacecraft.disable_test_mode()


def test_kepler_full():
    if os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip(
            "Skipping this test on GitHub Actions this downloads a database of stellar models."
        )
    lkspacecraft.disable_test_mode()
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


def test_dva():
    lkspacecraft.enable_test_mode()
    ts = lkspacecraft.TESSSpacecraft()
    start = Time("2018-10-15T00:00:00.000", format="isot")
    t = Time(np.linspace(start.jd, start.jd + 28, 360), format="jd")

    dra, ddec = ts.get_differential_velocity_aberrated_positions(
        time=t, ra=200, dec=10, ra0=200, dec0=10
    )

    assert np.allclose(dra, 200)
    assert np.allclose(ddec, 10)
    assert dra.shape == (len(t),)
    assert dra.shape == (len(t),)

    dra, ddec = ts.get_differential_velocity_aberrated_positions(
        time=t, ra=[200], dec=[10], ra0=190, dec0=0
    )
    assert dra.shape == (len(t), 1)
    assert dra.shape == (len(t), 1)

    dra, ddec = ts.get_differential_velocity_aberrated_positions(
        time=t,
        ra=np.random.normal(size=(10)),
        dec=np.random.normal(size=(10)),
        ra0=190,
        dec0=0,
    )
    assert dra.shape == (len(t), 10)
    assert dra.shape == (len(t), 10)

    dra, ddec = ts.get_differential_velocity_aberrated_positions(
        time=t,
        ra=np.random.normal(size=(10, 11)),
        dec=np.random.normal(size=(10, 11)),
        ra0=190,
        dec0=0,
    )
    assert dra.shape == (len(t), 10, 11)
    assert dra.shape == (len(t), 10, 11)
    lkspacecraft.disable_test_mode()


def test_light_travel_time():
    lkspacecraft.enable_test_mode()
    t = Time("2010-07-25 00:00:00.0000")
    ks = lkspacecraft.KeplerSpacecraft()
    dist = ((np.sum(ks.get_spacecraft_position(t) ** 2) ** 0.5) * u.km).to(u.m)
    travel_time = ks.get_spacecraft_light_travel_time(t) * u.second
    assert np.isclose(((dist / travel_time) / c), u.Quantity(1))
    lkspacecraft.disable_test_mode()
