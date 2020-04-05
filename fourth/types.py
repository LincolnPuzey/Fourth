from datetime import datetime


__all__ = ("LocalDatetime", "SpanningDatetime", "UtcDatetime")


class NoTimezoneDatetime(datetime):
    """
    A subclass of `datetime.datetime` that does it's best to pretend that it
    doesn't have a `tzinfo` attribute.
    """

    __slots__ = ()

    def __new__(
        cls,
        year,
        month=None,
        day=None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
        *,
        fold=0,
    ):
        if tzinfo is not None:
            raise ValueError(f"'tzinfo' kwarg must be None.")
        return super().__new__(
            cls, year, month, day, hour, minute, second, microsecond, fold=fold
        )

    def __getattribute__(self, name):
        if name in {
            "tzinfo",
            "timetz",
            "astimezone",
            "utcoffset",
            "dst",
            "tzname",
            "utctimetuple",
        }:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )
        return super().__getattribute__(name)

    def __setattr__(self, key, value):
        if key == "tzinfo":
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute 'tzinfo'"
            )
        return super().__setattr__(key, value)

    def __str__(self):
        return self.isoformat(sep="T")

    @classmethod
    def now(cls):
        return super().now()

    @classmethod
    def fromtimestamp(cls, timestamp):
        return super().fromtimestamp(timestamp)

    @classmethod
    def combine(cls, date, time):
        if time.tzinfo is not None:
            raise ValueError("time must have 'tzinfo' as None")
        return super().combine(date, time)

    @classmethod
    def fromisoformat(cls, date_string: str):
        return super().fromisoformat(date_string).replace(tzinfo=None)

    @classmethod
    def strptime(cls, date_string, format):
        return super().strptime(date_string, format).replace(tzinfo=None)

    def replace(
        self,
        *,
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
        microsecond: int = None,
        fold: int = None,
    ):
        return super().replace(
            year, month, day, hour, minute, second, microsecond, fold=fold,
        )

    def isoformat(self, *, sep: str = "T", timespec: str = "microseconds"):
        return super().isoformat(sep=sep, timespec=timespec)

    def strftime(self, fmt: str, tzinfo=None) -> str:
        return datetime(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
            tzinfo=tzinfo,
            fold=self.fold,
        ).strftime(fmt)


class LocalDatetime(NoTimezoneDatetime):
    """
    A datetime with no timezone.
    """

    __slots__ = ()


class SpanningDatetime(NoTimezoneDatetime):
    """
    A datetime that "spans" across multiple timezones.
    """

    __slots__ = ()


class UtcDatetime(datetime):
    """
    A datetime in the UTC timezone.
    """

    __slots__ = ()

    # TODO
