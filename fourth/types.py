"""
Source code for the datetime types that Fourth provides.
"""
from __future__ import annotations

__all__ = ("BaseDatetime", "LocalDatetime", "UTCDatetime")

from abc import ABCMeta, abstractmethod
from datetime import datetime, timezone
from operator import ge, gt, le, lt
from typing import Any, Callable, ClassVar, Literal, NoReturn, Union

from ._internal import contains_timezone

TIMESPEC = Literal[
    "auto", "hours", "minutes", "seconds", "milliseconds", "microseconds"
]


class BaseDatetime(metaclass=ABCMeta):
    """
    Abstract base class for Fourth datetime types.

    Contains a single real attribute `_at` which is a datetime.datetime
    instance which the Datetime is "at".

    Implements __setattr__ and __delattr__ to make instances pseudo-immutable.
    """

    # Instance Attributes

    _at: datetime

    __slots__ = ("_at",)

    # Special Methods

    @abstractmethod
    def __init__(self, from_datetime: datetime) -> None:
        """
        Set the _at attribute to the datetime we are initialising from.

        Subclasses should implement some validation of from_datetime before
        passing it here.

        :param from_datetime: The datetime to initialise from.
        """
        # use object.__setattr__ to get around pseudo immutability.
        object.__setattr__(self, "_at", from_datetime)

    def __setattr__(self, name: str, value: Any) -> NoReturn:
        """
        Setting attributes is disallowed for pseudo-immutability.

        :param name: The name of the attribute being set.
        :param value: The value to set the attribute to.
        :raises AttributeError: Always raised.
        """
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __delattr__(self, name: str) -> NoReturn:
        """
        Deleting attributes is disallowed for pseudo-immutability.

        :param name: The name of the attribute being deleted.
        :raises AttributeError: Always raised.
        """
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def __repr__(self) -> str:
        """
        Construct a command-line representation of the Datetime.
        Should be able to eval() this and get back an identical instance.

        :return: The representation of the Datetime.
        """
        return "{}.at({}, {}, {}, {}, {}, {}, {})".format(
            self.__class__.__name__,
            self._at.year,
            self._at.month,
            self._at.day,
            self._at.hour,
            self._at.minute,
            self._at.second,
            self._at.microsecond,
        )

    def __str__(self) -> str:
        """
        Construct a string representation of the Datetime.

        :return: An ISO format string representation of the Datetime.
        """
        return self.iso_format(sep="T", timespec="microseconds")

    def __format__(self, format_spec: str) -> str:
        """
        Called by the format() built-in function to build a formatted representation.

        :param format_spec: The formatting style required.
        :return:
        """
        if format_spec == "":
            return str(self)
        else:
            return self.strftime(format_spec)

    # Constructors

    @classmethod
    @abstractmethod
    def at(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> BaseDatetime:
        """
        Return a new instance at the specified date and time.

        Subclasses must implement this method.
        """
        raise NotImplementedError(f"{cls.__name__} does not implement at()")

    # Instance Properties

    @property
    def year(self) -> int:
        return self._at.year

    @property
    def month(self) -> int:
        return self._at.month

    @property
    def day(self) -> int:
        return self._at.day

    @property
    def hour(self) -> int:
        return self._at.hour

    @property
    def minute(self) -> int:
        return self._at.minute

    @property
    def second(self) -> int:
        return self._at.second

    @property
    def microsecond(self) -> int:
        return self._at.microsecond

    # Instance Methods

    def as_datetime(self) -> datetime:
        """
        Return a python standard library datetime.datetime instance
        corresponding to this Datetime.

        :return: A datetime.datetime instance.
        """
        return self._at

    def iso_format(self, *, sep: str = "T", timespec: TIMESPEC = "microseconds") -> str:
        """
        Construct an ISO 8601 format string of the Datetime.

        :param sep: Character to separate the date and time components.
        :param timespec: How to format the time component.
            Has the same meaning and available values as datetime.isoformat().
            Defaults to `"microseconds"` since that gives the most information
            and is the most consistent.
        :return: The ISO 8601 format string representation of the Datetime.
        """
        return self._at.isoformat(sep=sep, timespec=timespec)

    @abstractmethod
    def strftime(self, format_string: str) -> str:
        """
        Return a string representation of the Datetime, controlled by the format
        string. See datetime.datetime.strftime() for a list of the formatting options.

        :param format_string: The format string the representation will match.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement strftime()"
        )


class LocalDatetime(BaseDatetime):
    """
    A local Datetime with no timezone.

    The internal datetime always has `tzinfo=None`
    """

    # Class Attributes

    min: ClassVar[LocalDatetime]
    max: ClassVar[LocalDatetime]

    # Instance Attributes

    __slots__ = ()

    # Special Methods

    def __init__(self, at: datetime) -> None:
        """
        Initialise a LocalDatetime from a naive datetime.datetime instance.

        :param at: A naive datetime.datetime instance for this LocalDatetime.
        """
        if at.tzinfo is not None:
            raise ValueError(
                "LocalDatetime can't be initialised with an aware datetime",
            )

        super().__init__(at)

    def __eq__(self, other: Any) -> Union[bool, NotImplemented]:
        """
        A LocalDateTime can be equal to other LocalDateTime instances and
        datetime.datetime instances that are naive.
        Explicitly not equal to aware datetime.datetime instances.

        :param other: The object to check if equal to.
        :return: True if equal. False if not. NotImplemented otherwise.
        """
        if isinstance(other, LocalDatetime):
            return other._at == self._at
        elif isinstance(other, datetime):
            return other.tzinfo is None and other == self._at
        else:
            return NotImplemented

    def __hash__(self) -> int:
        """
        The hash is the same as the internal datetime's hash. This satisfies the
        property that objects which compare equal have the same hash value.

        :return: The hash as an integer.
        """
        return hash(self._at)

    # Rich Comparison Methods

    def _rich_compare(
        self, other: Any, compare: Callable[[Any, Any], Union[bool, NotImplemented]]
    ) -> Union[bool, NotImplemented]:
        """
        Do a rich comparison with other. This method contains the common logic for all
        the rich comparisons.

        Instances of LocalDatetime can be compared with other LocalDatetime instances,
        and naive datetime.datetime instances.

        :param other: The other object to compare to.
        :param compare: A function to compare objects once we know we can.
        :return: True/False if determined. Otherwise NotImplemented.
        """
        if isinstance(other, LocalDatetime):
            return compare(self._at, other._at)
        elif isinstance(other, datetime) and other.tzinfo is None:
            return compare(self._at, other)
        else:
            return NotImplemented

    def __lt__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, lt)

    def __le__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, le)

    def __gt__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, gt)

    def __ge__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, ge)

    # Constructors

    @classmethod
    def at(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> LocalDatetime:
        """
        Return a new LocalDatetime at the specified time.

        The year, month and day arguments are required.
        All arguments must be integers.

        :param year:
        :param month:
        :param day:
        :param hour:
        :param minute:
        :param second:
        :param microsecond:
        :return: A LocalDatetime instance at the specified time.
        """
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
            )
        )

    @classmethod
    def now(cls) -> LocalDatetime:
        """
        Return a new LocalDatetime instance for the current date and time.

        :return: A LocalDatetime instance for the current date and time.
        """
        return cls(datetime.now())

    @classmethod
    def from_iso_format(cls, date_string: str) -> LocalDatetime:
        """
        Return a new LocalDatetime instance corresponding to the ISO 8601
        formatted datetime string.

        The datetime string must not contain timezone information.

        This is intended to be the inverse of LocalDatetime.iso_format().
        Parsing Arbitrary ISO 8601 strings is not supported.

        :param date_string: The ISO 8601 formatted datetime string.
        :return: The corresponding LocalDatetime instance.
        :raises ValueError: When the datetime string contains tz info.
        """
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("fromisoformat: date_string contained tz info")
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string: str, format_string: str) -> LocalDatetime:
        """
        Returns a new LocalDatetime instance corresponding to the datetime
        string after being parsed according to the format string.

        Uses datetime.datetime.strptime to parse the strings.

        The datetime and format strings must not have a timezone component.

        :param date_string: The datetime string.
        :param format_string: The format string.
        :return: The corresponding LocalDatetime instance.
        :raises ValueError: When the strings have a timezone component.
        """
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is not None:
            raise ValueError("strptime: date_string contained tz info")
        return cls(datetime_obj)

    # Instance Methods

    def strftime(self, format_string: str) -> str:
        """
        Return a string representation of the date and time, controlled by the format
        string. See datetime.datetime.strftime() for a list of the formatting options.

        The format string must not contain timezone directive (%z, %Z), since
        LocalDatetime has no timezone information.

        :param format_string: The format string the representation will match.
        :return: The string representation of the date and time.
        :raises ValueError: When the format string contains timezone directives.
        """
        if contains_timezone(format_string):
            raise ValueError(
                "format string for LocalDatetime.strftime() must not contain timezone "
                "directives ('%z', '%Z')"
            )

        return self._at.strftime(format_string)


LocalDatetime.min = LocalDatetime(datetime.min)
LocalDatetime.max = LocalDatetime(datetime.max)


class UTCDatetime(BaseDatetime):
    """
    A Datetime in the UTC timezone.

    The internal datetime always has `tzinfo=timezone.utc`
    """

    # Class Attributes

    min: ClassVar[UTCDatetime]
    max: ClassVar[UTCDatetime]

    # Instance Attributes

    __slots__ = ()

    # Special Methods

    def __init__(self, at: datetime) -> None:
        """
        Initialise a UTCDatetime from an aware datetime.datetime instance.

        :param at: An aware datetime.datetime instance for this UTCDatetime.
        :raises ValueError: When the `at` argument is naive.
        """
        if at.tzinfo is None:
            raise ValueError("UTCDatetime can't be initialised with a naive datetime")

        at = at.astimezone(timezone.utc)

        super().__init__(at)

    def __eq__(self, other: Any) -> Union[bool, NotImplemented]:
        """
        A UTCDateTime can be equal to other UTCDateTime instances and
        datetime.datetime instances that are aware.
        Explicitly not equal to naive datetime.datetime instances.

        :param other: The object to check if equal to.
        :return: True if equal. False if not. NotImplemented otherwise.
        """
        if isinstance(other, UTCDatetime):
            return other._at == self._at
        elif isinstance(other, datetime):
            return other.tzinfo is not None and other == self._at
        else:
            return NotImplemented

    def __hash__(self) -> int:
        """
        The hash is the same as the internal datetime's hash. This satisfies the
        property that objects which compare equal have the same hash value.

        :return: The hash as an integer.
        """
        return hash(self._at)

    # Rich Comparison Methods

    def _rich_compare(
        self, other: Any, compare: Callable[[Any, Any], Union[bool, NotImplemented]]
    ) -> Union[bool, NotImplemented]:
        """
        Do a rich comparison with other. This method contains the common logic for all
        the rich comparisons.

        Instances of UTCDatetime can be compared with other UTCDatetime instances,
        and aware datetime.datetime instances.

        :param other: The other object to compare to.
        :param compare: A function to compare objects once we know we can.
        :return: True/False if determined. Otherwise NotImplemented.
        """
        if isinstance(other, UTCDatetime):
            return compare(self._at, other._at)
        elif isinstance(other, datetime) and other.tzinfo is not None:
            return compare(self._at, other)
        else:
            return NotImplemented

    def __lt__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, lt)

    def __le__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, le)

    def __gt__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, gt)

    def __ge__(self, other: Any) -> Union[bool, NotImplemented]:
        return self._rich_compare(other, ge)

    # Constructors

    @classmethod
    def at(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> UTCDatetime:
        """
        Return a new UTCDatetime at the specified time.

        The year, month and day arguments are required.
        All arguments must be integers.

        :param year:
        :param month:
        :param day:
        :param hour:
        :param minute:
        :param second:
        :param microsecond:
        :return: A UTCDatetime instance at the specified time.
        """
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
    def now(cls) -> UTCDatetime:
        """
        Return a new UTCDatetime instance for the current UTC date and time.

        :return: A UTCDatetime instance for the current UTC date and time.
        """
        return cls(datetime.now(timezone.utc))

    @classmethod
    def from_timestamp(cls, timestamp: Union[int, float]) -> UTCDatetime:
        """
        Return a new UTCDatetime instance corresponding to the POSIX timestamp.

        This method is only available on UTCDatetime since POSIX timestamps are
        inherently 'in' the UTC timezone.
        Constructing a LocalDatetime from a POSIX timestamp would result in a
        loss of data/context.

        :param timestamp: The POSIX timestamp.
        :return: The corresponding UTCDatetime instance.
        """
        return cls(datetime.fromtimestamp(timestamp, timezone.utc))

    @classmethod
    def from_iso_format(cls, date_string: str) -> UTCDatetime:
        """
        Return a new UTCDatetime instance corresponding to the ISO 8601
        formatted datetime string.

        The datetime string must contain some timezone information, so the date
        and time can be converted to UTC.

        This is intended to be the inverse of UTCDatetime.iso_format().
        Parsing Arbitrary ISO 8601 strings is not supported.

        :param date_string: The ISO 8601 formatted datetime string.
        :return: The corresponding UTCDatetime instance.
        :raises ValueError: When the datetime string doesn't contain tz info.
        """
        datetime_obj = datetime.fromisoformat(date_string)
        if datetime_obj.tzinfo is None:
            raise ValueError("fromisoformat: date_string didn't contain tz info")
        return cls(datetime_obj)

    @classmethod
    def strptime(cls, date_string: str, format_string: str) -> UTCDatetime:
        """
        Returns a new UTCDatetime instance corresponding to the datetime string
        after being parsed according to the format string.

        Uses datetime.datetime.strptime to parse the strings.

        The datetime and format strings must have a timezone component so that
        the date and time can be converted to UTC.

        :param date_string: The datetime string.
        :param format_string: The format string.
        :return: The corresponding UTCDatetime instance.
        :raises ValueError: When the strings don't have a timezone component.
        """
        datetime_obj = datetime.strptime(date_string, format_string)
        if datetime_obj.tzinfo is None:
            raise ValueError("strptime: date_string didn't contain tz info")
        return cls(datetime_obj)

    # Instance Methods

    def strftime(self, format_string: str) -> str:
        """
        Return a string representation of the date and time, controlled by the format
        string. See datetime.datetime.strftime() for a list of the formatting options.

        :param format_string: The format string the representation will match.
        :return: The string representation of the date and time.
        """
        return self._at.strftime(format_string)


UTCDatetime.min = UTCDatetime(datetime.min.replace(tzinfo=timezone.utc))
UTCDatetime.max = UTCDatetime(datetime.max.replace(tzinfo=timezone.utc))
