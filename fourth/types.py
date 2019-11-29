from datetime import datetime, MINYEAR


__all__ = ("LocalDatetime",)


class DateTimeBase:
    __slots__ = ("_date_time",)

    @property
    def year(self):
        return self._date_time.year

    @property
    def month(self):
        return self._date_time.month

    @property
    def day(self):
        return self._date_time.day

    @property
    def hour(self):
        return self._date_time.hour

    @property
    def minute(self):
        return self._date_time.minute

    @property
    def second(self):
        return self._date_time.second

    @property
    def microsecond(self):
        return self._date_time.microsecond


class LocalDatetime(DateTimeBase):
    def __init__(
        self,
        year=MINYEAR,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        *,
        date_time: datetime = None,
    ):
        if date_time is None:
            self._date_time = datetime(
                year, month, day, hour, minute, second, microsecond,
            )
        else:
            if date_time.tzinfo is not None:
                date_time.replace(tzinfo=None)
            self._date_time = date_time

    @classmethod
    def now(cls):
        return cls(date_time=datetime.now())

    @classmethod
    def now_utc(cls):
        return cls(date_time=datetime.utcnow())
