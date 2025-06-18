# Standard library
import os  # noqa

PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))
TEST_MODE = False


def enable_test_mode():
    global TEST_MODE
    TEST_MODE = True


def disable_test_mode():
    global TEST_MODE
    TEST_MODE = False


def is_test_mode():
    return TEST_MODE


from importlib.metadata import PackageNotFoundError, version  # noqa


def get_version():
    try:
        return version("lkspacecraft")
    except PackageNotFoundError:
        return "unknown"


__version__ = get_version()

import logging  # noqa: E402
import os  # noqa
from glob import glob  # noqa

log = logging.getLogger("lkspacecraft")

PACKAGEDIR = os.path.abspath(os.path.dirname(__file__))
KERNELDIR = f"{PACKAGEDIR}/data/kernels/"

# from .io import update_kernels
from .utils import create_meta_test_kernel  # noqa

create_meta_test_kernel()

from .spacecraft import KeplerSpacecraft, TESSSpacecraft  # noqa
