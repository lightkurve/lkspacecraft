"""Not sure what this is yet"""
from . import PACKAGEDIR
import spiceypy

class Ephemeris(object):
    def __init__(self):
        spiceypy.kclear()
        spiceypy.furnsh(PACKAGEDIR + '/data/Meta.txt')

    def __repr__(self):
        # Get the total number of loaded kernels
        return "lkspice Ephemeris"
        # num_kernels = spiceypy.ktotal("ALL")
        # return f"{num_kernels} Kernels Loaded:" + '\t\n'.join([spiceypy.kdata(i, "ALL")[0] for i in range(num_kernels)])
