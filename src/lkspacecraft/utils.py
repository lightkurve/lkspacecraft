# flake8: noqa
import os
import tempfile
import warnings
from glob import glob
from pathlib import Path

import numpy as np
import pandas as pd
from astropy.utils.data import CacheMissingWarning, cache_contents
from astropy.utils.data import clear_download_cache as _astropy_clear_download_cache
from astropy.utils.data import download_file, import_file_to_cache, is_url_in_cache
from tqdm import tqdm

from . import log

KERNELS = {
    "naif0012.tls": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/",
    "de440.bsp": "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/",
    "kplr2012299191755.tsc": "https://archive.stsci.edu/missions/kepler/spice/",
    "kplr2013205175543.tsc": "https://archive.stsci.edu/missions/kepler/spice/",
    "spk_2013161000000_2013163203537_kplr.bsp": "https://archive.stsci.edu/missions/kepler/spice/",
    "spk_2013358000000_2013360154555_kplr.bsp": "https://archive.stsci.edu/missions/kepler/spice/",
    "kplr2018134232543.tsc": "https://archive.stsci.edu/missions/k2/spice/",
    "spk_2018290000000_2018306220633_kplr.bsp": "https://archive.stsci.edu/missions/k2/spice/",
    "tess2018236164754-41096_sclk.tsc": "https://archive.stsci.edu/missions/tess/engineering/",
    "tess_20_year_long_predictive.bsp": "https://archive.stsci.edu/missions/tess/models/",
}


def get_tess_bsp():
    """Get all the listings of the spice kernels for TESS, including any new files."""
    df = pd.read_csv("https://archive.stsci.edu/missions/tess/models/", header=None)
    tess_bsp = {
        l.split(">")[2].split("<")[0]: "https://archive.stsci.edu/missions/tess/models/"
        for l in df[0]
        if "TESS_EPH_DEF" in l
    }
    _ = tess_bsp.pop("TESS_EPH_DEF_2018004_01.bsp")
    _ = tess_bsp.pop("TESS_EPH_DEF_2018080_01.bsp")
    return tess_bsp


KERNELS.update(
    {
        "TESS_EPH_PRE_2018150_01.bsp": "https://archive.stsci.edu/missions/tess/models/",
        "TESS_EPH_PRE_2018186_01.bsp": "https://archive.stsci.edu/missions/tess/models/",
    }
)

KERNELS.update(get_tess_bsp())


def get_file_path(url):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", CacheMissingWarning)
        return download_file(
            url, cache=True, show_progress=False, pkgname="lkspacecraft"
        )


def get_file_paths():
    """Ensure the file is downloaded and valid using Astropy's download_file."""
    file_paths = []
    file_names = list(KERNELS.keys())
    progress_bar = None
    for idx, file_name in enumerate(file_names):
        log.debug(f"Finding {file_name}.")
        url = KERNELS[file_name]
        if is_url_in_cache(url + file_name, pkgname="lkspacecraft"):
            file_paths.append(get_file_path(url + file_name))
            log.debug(f"Found {file_name} in cache.")
            continue
        if progress_bar is None:
            progress_bar = tqdm(
                range(0, len(file_names)),
                initial=idx,
                total=len(file_names),
                desc="Downloading SPICE Kernels",
            )
        file_paths.append(get_file_path(url + file_name))
        progress_bar.n = idx
        progress_bar.refresh()
        log.debug(f"Downloaded {file_name}.")
    return file_paths


def clear_download_cache():
    _astropy_clear_download_cache(pkgname="lkspacecraft")


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


META_START = """KPL/MK

lkspacecraft meta kernel
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


def create_meta_kernel():
    """Create a meta kernel out of the cached SPICE kernels"""
    paths = get_file_paths()
    if len(paths) == 0:
        raise ValueError(
            "Can not find any SPICE kernels. Check documentation on installation."
        )
    cache_dirs = np.unique([os.path.dirname(os.path.dirname(f)) for f in paths])
    if len(cache_dirs) != 1:
        raise ValueError(
            "You have provided multiple cache directories for SPICE kernels, try reinstalling."
        )

    path_values = truncate_directory_string(cache_dirs[0])
    path_symbols = ["cache"]
    kernels_to_load = ["$cache/" + path[len(cache_dirs[0]) + 1 :] for path in paths]

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

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write(output)
        # Get the file name
        temp_file_name = temp_file.name

    import_file_to_cache(
        "https://github.com/lightkurve/lkspacecraft/src/lkspacecraft/data/Meta.txt",
        temp_file_name,
        pkgname="lkspacecraft",
    )
    return


# def create_meta_kernel():
#     """Function that makes a meta kernel text file in a directory with a reasonable order.

#     We assume that everything in KERNELDIR/generic is required, and has higher priority than the mission kernels.
#     """

#     META_START = """KPL/MK

# lkspacecraft meta kernel
# ==============

#     The generic kernels listed below can be obtained from NAIF generic kernels:
#         https://naif.jpl.nasa.gov/pub/naif/generic_kernels/
#     The Kepler kernels below can be obtained from MAST
#         https://archive.stsci.edu/missions/kepler/spice/
#     The K2 kernels below can be obtained from MAST
#         https://archive.stsci.edu/missions/k2/spice/
#     The TESS kernels below can be obtained from MAST
#         https://archive.stsci.edu/missions/tess/engineering/
#         https://archive.stsci.edu/missions/tess/models/

#     \\begindata

#     """
#     META_END = """

#     \\begintext
#     """
#     path_values = []
#     path_symbols = []
#     kernels_to_load = []
#     for dirname in glob(f"{KERNELDIR}*"):
#         for d in truncate_directory_string(dirname):
#             path_values.append(d)
#         path_symbols.append(dirname.split("/")[-1])
#         for d in np.sort(glob(dirname + "/*")):
#             kernels_to_load.append("$" + dirname.split("/")[-1] + d[len(dirname) :])

#     def format_list(l, pad=10):
#         if len(l) == 0:
#             return ""
#         if len(l) == 1:
#             return f" '{l[0]}'"
#         output = f" '{l[0]}'"
#         for i in l[1:]:
#             output += "\n" + "".join([" "] * pad) + "'" + i + "'"
#         return output

#     output = f"""{META_START}
#     \n    PATH_VALUES = ({format_list(path_values, 20)}              )
#     \n    PATH_SYMBOLS = ({format_list(path_symbols, 21)}              )
#     \n    KERNELS_TO_LOAD = ({format_list(kernels_to_load, 24)}              )
#     {META_END}
#     """
#     with open(f"{PACKAGEDIR}/data/Meta.txt", "w") as file:
#         file.write(output)
#     return
