from glob import glob
import numpy as np
from . import PACKAGEDIR, KERNELDIR

def truncate_directory_string(directory_string):
    """Turns a directory string into a SPICE compliant list of directorys..."""
    lines = []
    line = ""
    for word in directory_string.split("/"):
        if word == "":
            continue
        if len(line) < 130:
            line = f"{line}/{word}"
        else:
            line = f"{line}+"
            lines.append(line)
            line = ""
    lines.append(line)
    return lines


def create_meta_kernel():
    """Function that makes a meta kernel text file in a directory with a reasonable order.

    We assume that everything in KERNELDIR/generic is required, and has higher priority than the mission kernels. 
    """

    META_START = """KPL/MK

K2 meta kernel
==============

    The generic kernels listed below can be obtained from NAIF generic kernels:
        https://naif.jpl.nasa.gov/pub/naif/generic_kernels/
    The Kepler kernels below can be obtained from MAST
        https://archive.stsci.edu/missions/kepler/spice/
    The K2 kernels below can be obtained from MAST
        https://archive.stsci.edu/missions/k2/spice/
    The TESS kernels below can be obtained from MAST
        https://archive.stsci.edu/missions/tess/engineering/
        https://archive.stsci.edu/missions/tess/models/

    \\begindata
    
    """
    META_END = """

    \\begintext   
    """
    path_values = []
    path_symbols = []
    kernels_to_load = []
    for dirname in glob(f"{KERNELDIR}*"):
        for d in truncate_directory_string(dirname):
            path_values.append(d)
        path_symbols.append(dirname.split('/')[-1])
        for d in np.sort(glob(dirname + "/*")):
            kernels_to_load.append('$' + dirname.split('/')[-1] + d[len(dirname):])

    def format_list(l, pad=10):
        if len(l) == 0:
            return ""
        if len(l) == 1:
            return f" '{l[0]}'"
        output = f" '{l[0]}'" 
        for i in l[1:]:
            output += "\n" + "".join([" "] * pad) + "'" + i + "'"
        return output
        
    output = f"""{META_START}
    \n    PATH_VALUES = ({format_list(path_values, 20)}              )
    \n    PATH_SYMBOLS = ({format_list(path_symbols, 21)}              )
    \n    KERNELS_TO_LOAD = ({format_list(kernels_to_load, 24)}              )
    {META_END}
    """
    with open(f"{PACKAGEDIR}/data/Meta.txt", "w") as file:
        file.write(output)
    return

