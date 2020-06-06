"""
Source code for the datetime types that Fourth provides.
"""
from __future__ import annotations

__all__ = ("LocalDatetime", "UTCDatetime")

from datetime import datetime, timezone
from typing import Literal, Union


FOLD = Literal[0, 1]


class BaseDatetime:
    """
    Base class for Fourth datetime types.
    """

    _at: datetime

    __slots__ = ("_at",)

    def __init__(self, from_datetime: datetime, /):
        # use object.__setattr__ to get around pseudo immutability.
        object.__setattr__(self, "_at", from_datetime)

    def __setattr__(self, name, value):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __delattr__(self, name):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._at)})"

    def __str__(self):
        return self.isoformat(sep="T", timespec="microseconds")

    @property
    def internal_datetime(self):
        return self._at

    def isoformat(self, *, sep: str = "T", timespec: str = "microseconds"):
        return self._at.isoformat(sep=sep, timespec=timespec)


class LocalDatetime(BaseDatetime):
    """
    A local datetime with no timezone.

    The internal datetime always has `tzinfo=None`
    """

    __slots__ = ()

    def __init__(self, at: datetime):
        if at.tzinfo is not None:
            raise ValueError(
                f"{self.__class__.__name__} can't be initialised with an "
                f"aware datetime"
            )

        super().__init__(at)

    @classmethod
    def at(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        fold: FOLD = 0,
    ):
        return cls(
            datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=microsecond,
                tzinfo=None,
                fold=fold,
            )
        )

    @classmethod
    def now(cls):
        return cls(datetime.now())

    @classmethod
    def fromisoformat(cls, date_string: str):
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("fromisoformat: date_string contained tz info")
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string, format_string):
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("strptime: date_string contained tz info")
        return cls(datetime_obj)


class UTCDatetime(BaseDatetime):
    """
    A datetime in the UTC timezone.

    The internal datetime always has `tzinfo=timezone.utc`
    """

    __slots__ = ()

    def __init__(self, at: datetime):
        if at.tzinfo is None:
            raise ValueError(
                f"{self.__class__.__name__} can't be initialised with a "
                f"naive datetime"
            )

        at = at.astimezone(timezone.utc)

        super().__init__(at)

    @classmethod
    def at(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ):
        return cls(
            datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=microsecond,
                tzinfo=timezone.utc,
            )
        )

    @classmethod
    def now(cls):
        return cls(datetime.now(timezone.utc))

    @classmethod
    def fromtimestamp(cls, timestamp: Union[int, float]):
        return cls(datetime.fromtimestamp(timestamp, timezone.utc))

    @classmethod
    def fromisoformat(cls, date_string: str):
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is None:
            raise ValueError(
                "fromisoformat: date_string didn't contain tz info"
            )
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string, format_string):
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is None:
            raise ValueError("strptime: date_string didn't contain tz info")
        return cls(datetime_obj)
