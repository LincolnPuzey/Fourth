from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest import TestCase

from fourth import LocalDatetime, UTCDatetime
from fourth.types import BaseDatetime


class BaseDatetimeTests(TestCase):
    def test_cant_be_instantiated(self):
        with self.assertRaisesRegex(
            TypeError, r"^Can't instantiate abstract class BaseDatetime",
        ):
            BaseDatetime(datetime.now())

    def test_at_not_implemented(self):
        with self.assertRaisesRegex(
            NotImplementedError,
            r"^BaseDatetime does not provide an implementation of at\(\)$",
        ):
            BaseDatetime.at(year=2010, month=1, day=1)


class LocalDatetimeTests(TestCase):
    def test_class_attributes(self):
        self.assertTrue(hasattr(LocalDatetime, "min"))
        self.assertEqual(
            LocalDatetime.min, LocalDatetime.at(1, 1, 1, 0, 0, 0, 0),
        )
        self.assertTrue(hasattr(LocalDatetime, "max"))
        self.assertEqual(
            LocalDatetime.max,
            LocalDatetime.at(9999, 12, 31, 23, 59, 59, 999999),
        )

    def test_init(self):
        now = datetime.now()
        local_now = LocalDatetime(now)

        self.assertIsInstance(local_now, LocalDatetime)
        self.assertEqual(now, local_now._at)

    def test_init_exceptions(self):
        now_aware = datetime.now(timezone.utc)

        with self.assertRaisesRegex(
            ValueError,
            r"^LocalDatetime can't be initialised with an aware datetime$",
        ):
            LocalDatetime(now_aware)

    def test_setattr(self):
        foo = LocalDatetime.now()

        with self.assertRaisesRegex(
            AttributeError, "^'LocalDatetime' object has no attribute '_at'$"
        ):
            setattr(foo, "_at", 1)

    def test_delattr(self):
        foo = LocalDatetime.now()

        with self.assertRaisesRegex(
            AttributeError, "^'LocalDatetime' object has no attribute '_at'$"
        ):
            delattr(foo, "_at")

    def test_repr(self):
        foo = LocalDatetime.at(2020, 11, 12, 8, 36, 42, 433677)

        self.assertEqual(
            repr(foo), "LocalDatetime.at(2020, 11, 12, 8, 36, 42, 433677)",
        )

    def test_eval_repr(self):
        foo = LocalDatetime.at(2020, 9, 20, 4, 56, 43, 333677)

        self.assertEqual(foo, eval(repr(foo)))

    def test_str(self):
        foo = LocalDatetime.at(year=2020, month=1, day=1)

        self.assertEqual(
            str(foo), "2020-01-01T00:00:00.000000",
        )

    def test_eq(self):
        foo = LocalDatetime.at(year=2020, month=1, day=1)

        # use assertIs to check that __eq__ is returning actual True/False,
        # and not just a truthy/falsey value
        self.assertIs(False, foo == 1)
        self.assertIs(False, foo == "foo")
        self.assertIs(False, foo == datetime(2020, 1, 3))
        self.assertIs(False, foo == datetime(2020, 1, 1, tzinfo=timezone.utc))
        self.assertIs(False, foo == LocalDatetime.at(2020, 1, 2))
        self.assertIs(False, foo == UTCDatetime.at(2020, 1, 1))

        self.assertIs(True, foo == datetime(2020, 1, 1))
        self.assertIs(True, foo == LocalDatetime.at(2020, 1, 1))

    def test_at_constructor_minimal_args(self):
        foo = LocalDatetime.at(year=2020, month=1, day=2)

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2020, 1, 2))
        self.assertIsNone(foo._at.tzinfo)

    def test_at_constructor_all_args(self):
        foo = LocalDatetime.at(
            year=2020,
            month=1,
            day=2,
            hour=3,
            minute=4,
            second=5,
            microsecond=6,
        )

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2020, 1, 2, 3, 4, 5, 6))
        self.assertIsNone(foo._at.tzinfo)

    def test_at_constructor_minimal_positional_args(self):
        foo = LocalDatetime.at(2010, 3, 5)

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2010, 3, 5))
        self.assertIsNone(foo._at.tzinfo)

    def test_at_constructor_all_positional_args(self):
        foo = LocalDatetime.at(2010, 3, 5, 14, 44, 55, 123456)

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2010, 3, 5, 14, 44, 55, 123456))
        self.assertIsNone(foo._at.tzinfo)

    def test_now_constructor(self):
        now = datetime.now()
        local_now = LocalDatetime.now()

        self.assertIsInstance(local_now, LocalDatetime)
        self.assertLess(local_now._at - now, timedelta(seconds=1))

    def test_from_iso_format(self):
        foo = LocalDatetime.from_iso_format("2020-03-04T23:59:59.333444")

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2020, 3, 4, 23, 59, 59, 333444))

    def test_from_iso_format_with_tz(self):
        with self.assertRaisesRegex(
            ValueError, r"^fromisoformat: date_string contained tz info$"
        ):
            LocalDatetime.from_iso_format("2020-03-04T23:59:59.333444+00:00")

    def test_strptime(self):
        foo = LocalDatetime.strptime(
            "2020/05/22 12:02:04", "%Y/%m/%d %H:%M:%S",
        )

        self.assertIsInstance(foo, LocalDatetime)
        self.assertEqual(foo._at, datetime(2020, 5, 22, 12, 2, 4))

    def test_strptime_with_tz(self):
        with self.assertRaisesRegex(
            ValueError, r"^strptime: date_string contained tz info$"
        ):
            LocalDatetime.strptime(
                "2020/05/22 12:02:04 +1030", "%Y/%m/%d %H:%M:%S %z",
            )

    def test_properties(self):
        foo = LocalDatetime.at(2020, 2, 3, 14, 44, 33, 123)

        self.assertEqual(foo.year, 2020)
        self.assertEqual(foo.month, 2)
        self.assertEqual(foo.day, 3)
        self.assertEqual(foo.hour, 14)
        self.assertEqual(foo.minute, 44)
        self.assertEqual(foo.second, 33)
        self.assertEqual(foo.microsecond, 123)

    def test_as_datetime(self):
        foo = LocalDatetime.at(2020, 1, 1, 22, 33, 52, 333444)

        self.assertEqual(
            foo.as_datetime(), datetime(2020, 1, 1, 22, 33, 52, 333444)
        )

    def test_iso_format(self):
        foo = LocalDatetime.at(year=2020, month=1, day=1)

        self.assertEqual(
            foo.iso_format(), "2020-01-01T00:00:00.000000",
        )

    def test_iso_format_custom(self):
        foo = LocalDatetime.at(year=2020, month=1, day=1)

        self.assertEqual(
            foo.iso_format(sep=" ", timespec="auto"), "2020-01-01 00:00:00",
        )


class UTCDatetimeTests(TestCase):
    def test_class_attributes(self):
        self.assertTrue(hasattr(UTCDatetime, "min"))
        self.assertEqual(UTCDatetime.min, UTCDatetime.at(1, 1, 1, 0, 0, 0, 0))
        self.assertTrue(hasattr(UTCDatetime, "max"))
        self.assertEqual(
            UTCDatetime.max, UTCDatetime.at(9999, 12, 31, 23, 59, 59, 999999),
        )

    def test_init(self):
        now = datetime.now(timezone.utc)
        utc_now = UTCDatetime(now)

        self.assertIsInstance(utc_now, UTCDatetime)
        self.assertEqual(now, utc_now._at)

    def test_init_exceptions(self):
        now_naive = datetime.now()

        with self.assertRaisesRegex(
            ValueError,
            r"^UTCDatetime can't be initialised with a naive datetime$",
        ):
            UTCDatetime(now_naive)
