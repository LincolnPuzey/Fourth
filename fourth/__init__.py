"""
The Fourth datetime library. ALl public names should be imported here and
declared in __all__.

TODO feature list:
* spanning datetime type
* setup changelog - semantic version statement
* Docs
"""
from __future__ import annotations

__version__ = "0.0.11"

__all__ = ("LocalDatetime", "UTCDatetime")

from .types import LocalDatetime, UTCDatetime
