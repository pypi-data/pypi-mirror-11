import unittest
import types
from StringIO import StringIO
from math import exp, sqrt

from numpy import pi, random
import progressbar

from sapphire import utils


class PbarTests(unittest.TestCase):

    def setUp(self):
        self.iterable = range(10)
        self.output = StringIO()

    def test_pbar_iterable(self):
        pb = utils.pbar(self.iterable, fd=self.output)
        self.assertIsInstance(pb, progressbar.ProgressBar)
        self.assertEqual(list(pb), self.iterable)

    def test_pbar_generator(self):
        """Return original generator, not a progressbar"""

        generator = (x for x in self.iterable)
        pb = utils.pbar(generator)
        self.assertIsInstance(pb, types.GeneratorType)
        self.assertEqual(list(pb), self.iterable)

    def test_pbar_generator_known_length(self):
        """Return progressbar for generator with known length"""

        generator = (y for y in self.iterable)
        pb = utils.pbar(generator, length=len(self.iterable), fd=self.output)
        self.assertIsInstance(pb, progressbar.ProgressBar)
        self.assertEqual(list(pb), self.iterable)

    def test_pbar_generator_wrong_length(self):
        """Raise exception for generator with wrong length"""

        generator = (y for y in self.iterable)
        pb = utils.pbar(generator, length=len(self.iterable) - 5, fd=self.output)
        self.assertRaises(ValueError, list, pb)

    def test_pbar_hide_output(self):
        """Empty output when not showing progressbar"""

        pb = utils.pbar(self.iterable, show=False, fd=self.output)
        self.assertEqual(list(pb), self.iterable)
        self.assertEqual(self.output.getvalue(), '')

        pb = utils.pbar(self.iterable, show=True, fd=self.output)
        self.assertEqual(list(pb), self.iterable)
        self.assertNotEqual(self.output.getvalue(), '')


class InBaseTests(unittest.TestCase):

    def test_ceil(self):
        self.assertEqual(utils.ceil_in_base(2.4, 2.5), 2.5)
        self.assertEqual(utils.ceil_in_base(0.1, 2.5), 2.5)

    def test_floor(self):
        self.assertEqual(utils.floor_in_base(2.4, 2.5), 0)
        self.assertEqual(utils.floor_in_base(0.1, 2.5), 0)

    def test_round(self):
        self.assertEqual(utils.round_in_base(2.4, 2.5), 2.5)
        self.assertEqual(utils.round_in_base(0.1, 2.5), 0)

    def test_zero_base(self):
        self.assertRaises(ZeroDivisionError, utils.ceil_in_base, 0.1, 0)
        self.assertRaises(ZeroDivisionError, utils.floor_in_base, 0.1, 0)
        self.assertRaises(ZeroDivisionError, utils.round_in_base, 0.1, 0)

    def test_integers(self):
        self.assertEqual(utils.ceil_in_base(3, 4), 4)
        self.assertEqual(utils.floor_in_base(3, 4), 0)
        self.assertEqual(utils.round_in_base(3, 4), 4)


class ActiveIndexTests(unittest.TestCase):

    def test_get_active_index(self):
        """Test if the bisection returns the correct index

        - If timestamp is before the first timestamp return index for
          first item
        - If timestamp is after last timestamp return index for last item
        - If timestamp is in the range return index of rightmost value
          equal or less than the timestamp

        """
        timestamps = [1., 2., 3., 4.]

        for idx, ts in [(0, 0.), (0, 1.), (0, 1.5), (1, 2.), (1, 2.1), (3, 4.),
                        (3, 5.)]:
            self.assertEqual(utils.get_active_index(timestamps, ts), idx)


class GaussTests(unittest.TestCase):
    """Test against explicit Gaussian"""

    def gaussian(self, x, N, mu, sigma):
        return N * exp(-(x - mu) ** 2. / (2. * sigma ** 2)) / (sigma * sqrt(2 * pi))

    def test_gauss(self):
        x, N, mu, sigma = (1., 1., 0., 1.)
        self.assertEqual(utils.gauss(x, N, mu, sigma), self.gaussian(x, N, mu, sigma))
        N = 2.
        self.assertEqual(utils.gauss(x, N, mu, sigma), self.gaussian(x, N, mu, sigma))
        sigma = 2.
        self.assertEqual(utils.gauss(x, N, mu, sigma), self.gaussian(x, N, mu, sigma))
        x = 1e5
        self.assertEqual(utils.gauss(x, N, mu, sigma), 0.)


class AngleBetweenTests(unittest.TestCase):

    def test_zeniths(self):
        for zenith in random.uniform(0, pi / 2, 10):
            self.assertAlmostEqual(utils.angle_between(zenith, 0, 0, 0), zenith)
            self.assertAlmostEqual(utils.angle_between(0, 0, zenith, 0), zenith)

    def test_azimuths(self):
        # Set both zeniths to pi/2 to give azimuth full effect.
        z = pi / 2
        for azimuth in random.uniform(-pi, pi, 20):
            self.assertAlmostEqual(utils.angle_between(z, azimuth, z, 0), abs(azimuth))
            self.assertAlmostEqual(utils.angle_between(z, 0, z, azimuth), abs(azimuth))

    def test_no_zenith(self):
        for azimuth in random.uniform(-pi, pi, 20):
            self.assertAlmostEqual(utils.angle_between(0, azimuth, 0, 0), 0)
            self.assertAlmostEqual(utils.angle_between(0, 0, 0, azimuth), 0)


if __name__ == '__main__':
    unittest.main()
