import tests
import unittest
from astro import find_corresponding_night

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=2).run(suite)
    longitude_warsaw = 21.01
    julian_date = 2459315.08333
    print("Longitude: " + str(longitude_warsaw))
    print("Julian date: " + str(julian_date))
    print("Night of the event: " + find_corresponding_night(julian_date, longitude_warsaw))

