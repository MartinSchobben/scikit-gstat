import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from skgstat import DirectionalVariogram, Variogram


class TestDirectionalVariogramInstantiation(unittest.TestCase):
    def setUp(self):
        # set up default valures, whenever c,v are not important
        np.random.seed(1306)
        self.c = np.random.gamma(11, 2, (30, 2))
        np.random.seed(1306)
        self.v = np.random.normal(5, 4, 30)

    def test_standard_settings(self):
        DV = DirectionalVariogram(self.c, self.v, normalize=True)

        for x, y in zip(DV.parameters, [407.467, 2138.098, 0]):
            self.assertAlmostEqual(x, y, places=0)

    def test_azimuth(self):
        DV = DirectionalVariogram(self.c, self.v, azimuth=-45, normalize=True)

        for x, y in zip(DV.parameters, [27.288, 131.644, 0]):
            self.assertAlmostEqual(x, y, places=3)

    def test_invalid_azimuth(self):
        with self.assertRaises(ValueError) as e:
            DirectionalVariogram(self.c, self.v, azimuth=360)
            self.assertEqual(
                str(e),
                'The azimuth is an angle in degree and has '
                'to meet -180 <= angle <= 180'
            )

    def test_tolerance(self):
        DV = DirectionalVariogram(self.c, self.v, tolerance=15, normalize=True)

        for x, y in zip(DV.parameters, [26.342, 1880.015, 0]):
            self.assertAlmostEqual(x, y, places=3)

    def test_invalid_tolerance(self):
        with self.assertRaises(ValueError) as e:
            DirectionalVariogram(self.c, self.v, tolerance=-1)
            self.assertEqual(
                str(e),
                'The tolerance is an angle in degree and has to '
                'meet 0 <= angle <= 360'
            )

    def test_bandwidth(self):
        DV = DirectionalVariogram(self.c, self.v, bandwidth=12, normalize=True)

        for x, y in zip(DV.parameters, [435.733, 2715.865, 0]):
            self.assertAlmostEqual(x, y, places=3)

    def test_invalid_model(self):
        with self.assertRaises(ValueError) as e:
            DirectionalVariogram(self.c, self.v, directional_model='NotAModel')
            self.assertEqual(
                str(e),
                'NotAModel is not a valid model.'
            )

    def test_invalid_model_type(self):
        with self.assertRaises(ValueError) as e:
            DirectionalVariogram(self.c, self.v, directional_model=5)
            self.assertEqual(
                str(e),
                'The directional model has to be identified by a '
                'model name, or it has to be the search area '
                'itself'
            )


class Mock:
    def __init__(self, c=None, v=None):
        self._X = c
        self.values = v


class TestDirectionalVariogramMethods(unittest.TestCase):
    def setUp(self):
        # set up default valures, whenever c,v are not important
        np.random.seed(11884)
        self.c = np.random.gamma(15, 3, (30, 2))
        np.random.seed(11884)
        self.v = np.random.normal(9, 2, 30)


    def test_bin_func(self):
        DV = DirectionalVariogram(self.c, self.v, n_lags=4)
        V = Variogram(self.c, self.v, n_lags=4)

        for x, y in zip (DV.bins, V.bins):
            self.assertNotEqual(x, y)

        assert_array_almost_equal(
            np.array([12.3, 24.7, 37., 49.4]), DV.bins, decimal=1
        )

    def test_directional_mask(self):
        a = np.array([[0, 0], [1, 2], [2, 1]])

        # overwrite fit method
        class Test(DirectionalVariogram):
            def fit(*args, **kwargs):
                pass

        var = Test(a, np.random.normal(0, 1, size=3))
        var._calc_directional_mask_data()

        assert_array_almost_equal(
            np.degrees(var._angles + np.pi)[:2],
            [63.4, 26.6],
            places=1
        )


if __name__ == '__main__':
    unittest.main()
