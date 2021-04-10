import unittest
import datetime
from astro import find_corresponding_night, day_to_hour_minutes_seconds, jd_to_date, jd_to_datetime_object, MJD_JD_CONVERSION_VALUE


class TestAstroMethods(unittest.TestCase):

    def setUp(self):
        # List of dates used for testing in assignment as Julian Dates
        self.JD_list = [2451552.87431, 2451552.99931, 2451553.00069, 2451553.49931, 2451553.50069]
        # List of dates used for testing in assignment as Modified Julian Dates
        self.MJD_list = [elem - MJD_JD_CONVERSION_VALUE for elem in self.JD_list]
        # Longitude for Wroclaw
        self.Lon = 17.03

        self.result = ["2000-01-08", "2000-01-09", "2000-01-09", "2000-01-09", "2000-01-09"]

    def test_find_corresponding_night(self):
        method_result = []
        for elem in self.JD_list:
            method_result.append(find_corresponding_night(elem, self.Lon))

        self.assertEqual(method_result, self.result)

    def test_find_corresponding_night_MJD_values(self):
        method_result = []
        for elem in self.MJD_list:
            method_result.append(find_corresponding_night(elem, self.Lon))
        self.assertEqual(method_result, self.result)

    def test_day_to_hour_minutes_seconds_wrong_day(self):
        with self.assertRaises(ValueError):
            day_to_hour_minutes_seconds(15.2)

    def test_day_to_hour_minutes_seconds(self):
        result = (12, 0, 0)

        self.assertEqual(day_to_hour_minutes_seconds(0.5), result)

    def test_jd_to_date_wrong_JD(self):
        with self.assertRaises(ValueError):
            jd_to_date(-30.0)

    def test_jd_to_date(self):
        result = (2021, 4, 10.5)
        self.assertEqual(jd_to_date(2459315.00000), result)

    def test_jd_to_datetime_object(self):
        result = datetime.datetime(2021, 4, 10, 12, 0, 0)
        self.assertEqual(jd_to_datetime_object(2459315.00000), result)

