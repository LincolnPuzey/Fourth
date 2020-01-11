from datetime import datetime, MINYEAR


__all__ = ("LocalDatetime", "LocalDatetimeSubclass")


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


class LocalDatetimeSubclass(datetime):
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
        return super().__new__(
            cls, year, month, day, hour, minute, second, microsecond, fold=fold
        )

    @classmethod
    def now(cls):
        return super().now()

    @classmethod
    def fromtimestamp(cls, timestamp):
        return super().fromtimestamp(timestamp)

    @classmethod
    def combine(cls, date, time):
        return super().combine(date, time)

    @classmethod
    def fromisoformat(cls, date_string: str):
        return super().fromisoformat(date_string).replace(tzinfo=None)

    @classmethod
    def strptime(cls, date_string, format):
        return super().strptime(date_string, format).replace(tzinfo=None)
