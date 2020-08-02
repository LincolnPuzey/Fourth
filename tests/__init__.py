"""
Tests for Fourth.

Test helpers can go here.
"""
from __future__ import annotations

__all__ = ("FourthTestCase",)

from typing import Any
from unittest import TestCase


class FourthTestCase(TestCase):
    def assertSymmetricEqual(self, a: Any, b: Any) -> None:
        self.assertTrue(a == b)
        self.assertTrue(b == a)

    def assertSymmetricNotEqual(self, a: Any, b: Any) -> None:
        self.assertFalse(a == b)
        self.assertFalse(b == a)
