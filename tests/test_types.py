from __future__ import annotations

from datetime import datetime
from unittest import TestCase

from freezegun import freeze_time


class BaseTests(TestCase):
    def test_hello(self):
        self.assertEqual(1, 1)

    @freeze_time("2020-01-01")
    def test_freeze(self):
        self.assertEqual(datetime.now().day, 1)
