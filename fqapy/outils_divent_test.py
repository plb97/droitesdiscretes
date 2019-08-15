import unittest

from . import outils


class Tdivent:
    """Classe pour tester la division entière"""

    def __init__(self, n_=0, d=0, q=0, r=0):
        self.n, self.d, self.q, self.r = n_, d, q, r

    def __str__(self):
        return "n={}, d={}, q={}, r={}".format(self.n, self.d, self.q, self.r)


class OutilsDiventTestCase(unittest.TestCase):
    def test_divent(self):
        """Test de la division entière."""
        tt = [
            Tdivent(n_=3, d=2, q=1, r=1),
            Tdivent(n_=-3, d=2, q=-2, r=1),
            Tdivent(n_=3, d=-2, q=-1, r=1),
            Tdivent(n_=-3, d=-2, q=2, r=1),
            Tdivent(n_=6, d=2, q=3, r=0),
            Tdivent(n_=2, d=6, q=0, r=2),
        ]
        # print()
        # print("test_divent")
        for v_ in tt:
            q_, r_ = outils.divent(v_.n, v_.d)
            # print("v", v_, "obtenu :", "q", q_, "r", r_)
            self.assertTrue(0 <= r_ < abs(v_.d))
            self.assertEqual(v_.n, q_ * v_.d + r_)
            self.assertEqual(v_.q, q_)
            self.assertEqual(v_.r, r_)

        with self.assertRaises(AssertionError):
            outils.divent(3, 0)


if __name__ == '__main__':
    unittest.main()
