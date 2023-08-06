# (C) British Crown Copyright 2014, Met Office
#
# This file is part of cf_units.
#
# cf_units is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cf_units is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cf_units.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the `cf_units.Unit` class."""

from __future__ import (absolute_import, division, print_function)

import unittest

import numpy as np

import cf_units
from cf_units import Unit


class Test___init__(unittest.TestCase):

    def test_capitalised_calendar(self):
        calendar = 'GrEgoRian'
        expected = cf_units.CALENDAR_GREGORIAN
        u = Unit('hours since 1970-01-01 00:00:00', calendar=calendar)
        self.assertEqual(u.calendar, expected)

    def test_not_basestring_calendar(self):
        with self.assertRaises(TypeError):
            u = Unit('hours since 1970-01-01 00:00:00', calendar=5)


class Test_convert(unittest.TestCase):

    class MyStr(str):
        pass

    def test_gregorian_calendar_conversion_setup(self):
        # Reproduces a situation where a unit's gregorian calendar would not
        # match (using the `is` operator) to the literal string 'gregorian',
        # causing an `is not` test to return a false negative.
        cal_str = cf_units.CALENDAR_GREGORIAN
        calendar = self.MyStr(cal_str)
        self.assertIsNot(calendar, cal_str)
        u1 = Unit('hours since 1970-01-01 00:00:00', calendar=calendar)
        u2 = Unit('hours since 1969-11-30 00:00:00', calendar=calendar)
        u1point = np.array([8.], dtype=np.float32)
        expected = np.array([776.], dtype=np.float32)
        result = u1.convert(u1point, u2)
        return expected, result

    def test_gregorian_calendar_conversion_array(self):
        expected, result = self.test_gregorian_calendar_conversion_setup()
        np.testing.assert_array_equal(expected, result)

    def test_gregorian_calendar_conversion_dtype(self):
        expected, result = self.test_gregorian_calendar_conversion_setup()
        self.assertEqual(expected.dtype, result.dtype)

    def test_gregorian_calendar_conversion_shape(self):
        expected, result = self.test_gregorian_calendar_conversion_setup()
        self.assertEqual(expected.shape, result.shape)

    def test_non_gregorian_calendar_conversion_dtype(self):
        data = np.arange(4, dtype=np.float32)
        u1 = Unit('hours since 2000-01-01 00:00:00', calendar='360_day')
        u2 = Unit('hours since 2000-01-02 00:00:00', calendar='360_day')
        result = u1.convert(data, u2)
        self.assertEqual(result.dtype, np.float32)


if __name__ == '__main__':
    tests.main()
