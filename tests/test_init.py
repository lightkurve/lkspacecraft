import os

def test_init():
    import lkspice
    os.path.isfile(lkspice.PACKAGEDIR + '/data/Meta.txt')
    lkspice.Ephemeris()
