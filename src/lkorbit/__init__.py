# Standard library
import os  # noqa

PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))

from importlib.metadata import version, PackageNotFoundError  # noqa


def get_version():
    try:
        return version("lkorbit")
    except PackageNotFoundError:
        return "unknown"


__version__ = get_version()

import logging  # noqa: E402
import os  # noqa
from glob import glob  # noqa

log = logging.getLogger("lkorbit")

PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))
KERNELDIR = f"{PACKAGEDIR}/data/kernels/"

# from .io import update_kernels
from .utils import create_meta_kernel  # noqa

# update_kernels() # This function should grab kernels and update the kernel directory
create_meta_kernel()

from .spacecraft import KeplerSpacecraft, TESSSpacecraft  # noqa
