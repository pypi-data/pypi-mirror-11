"""
    muffin description.

"""

# Package information
# ===================

__version__ = "0.1.2"
__project__ = "muffin"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"

from aiohttp.web import *                           # noqa

CONFIGURATION_ENVIRON_VARIABLE = 'MUFFIN_CONFIG'

from .app import Application, Handler                   # noqa
from .urls import sre                                   # noqa
from .utils import to_coroutine, MuffinException, local # noqa
