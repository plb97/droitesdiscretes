import unittest

from . import outils


class Tpgcd:
    """Classe pour tester le pgcd"""

    def __init__(self, a_=0, b_=0, g_=0):
        self.a, self.b, self.g = a_, b_, g_

    def __str__(self):
        return "a={}, b={}, g={}".format(self.a, self.b, self.g)


class OutilsPgcdTestCase(unittest.TestCase):
    def test_pgcd(self):
        """Test du PGCD."""
        tt = [
            Tpgcd(a_=15, b_=10, g_=5),
            Tpgcd(a_=-15, b_=10, g_=5),
            Tpgcd(a_=15, b_=-10, g_=5),
            Tpgcd(a_=-15, b_=-10, g_=5),
            Tpgcd(a_=15, b_=0, g_=15),
            Tpgcd(a_=-15, b_=0, g_=15),
            Tpgcd(a_=0, b_=10, g_=10),
            Tpgcd(a_=0, b_=-10, g_=10),
        ]
        # print()
        # print("test_pgcd")
        for v_ in tt:
            g_ = outils.pgcd(v_.a, v_.b)
            # print("v", v_, "obtenu :", "g", g_)
            # contrôle de la cohérence du test
            self.assertTrue(1 <= v_.g)
            self.assertTrue(0 == v_.a % v_.g)
            self.assertTrue(0 == v_.b % v_.g)
            # contrôle du résultat du test
            self.assertEqual(v_.g, g_)

        with self.assertRaises(AssertionError):
            outils.pgcd(0, 0)


if __name__ == '__main__':
    unittest.main()
