from __future__ import annotations

from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time

from fourth import LocalDatetime


class BaseTests(TestCase):
    @freeze_time("2020-01-01T14:10:20")
    def test_local_now(self):
        self.assertEqual(
            LocalDatetime.now().internal_datetime,
            datetime(2020, 1, 1, 14, 10, 20),
        )
