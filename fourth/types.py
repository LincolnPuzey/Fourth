from datetime import datetime


__all__ = ("LocalDatetime",)


class LocalDatetime:
    __slots__ = ("_datetime",)

    def __init__(
        self,
        year,
        month,
        day,
        hour=None,
        minute=None,
        second=None,
        microsecond=None,
    ):
        self._datetime = datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo=None,
        )
