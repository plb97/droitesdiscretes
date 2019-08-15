import unittest

from . import outils


class Tpgcde:
    """Classe pour tester pgcde"""

    def __init__(self, a_=0, b_=0, g_=0, u_=0, v_=0):
        self.a, self.b, self.g, self.u, self.v = a_, b_, g_, u_, v_

    def __str__(self):
        return "a={}, b={}, g={}, u={}, v={}".format(self.a, self.b, self.g, self.u, self.v)


class OutilsPgcdeTestCase(unittest.TestCase):
    def test_pgcde(self):
        """Test du PGCD étendu."""
        tt = [
            Tpgcde(a_=15, b_=10, g_=5, u_=1, v_=-1),
            Tpgcde(a_=-15, b_=10, g_=5, u_=1, v_=2),
            Tpgcde(a_=15, b_=-10, g_=5, u_=-1, v_=-2),
            Tpgcde(a_=-15, b_=-10, g_=5, u_=-1, v_=1),
            Tpgcde(a_=15, b_=0, g_=15, u_=1, v_=0),
            Tpgcde(a_=-15, b_=0, g_=15, u_=-1, v_=0),
            Tpgcde(a_=0, b_=10, g_=10, u_=0, v_=1),
            Tpgcde(a_=0, b_=-10, g_=10, u_=0, v_=-1),
        ]
        # print()
        # print("test_pgcde")
        for t_ in tt:
            g_, u_, v_ = outils.pgcde(t_.a, t_.b)
            # print("v", t_, "obtenu :", "g", g_, "u", u_, "v", v_)
            # contrôle de la cohérence du test
            self.assertTrue(1 <= t_.g)
            self.assertTrue(0 == t_.a % t_.g)
            self.assertTrue(0 == t_.b % t_.g)
            self.assertEqual(t_.g, t_.a * t_.u + t_.b * t_.v)

            # contrôle du résultat du test
            self.assertEqual(t_.g, g_)
            self.assertEqual(t_.u, u_)
            self.assertEqual(t_.v, v_)

        with self.assertRaises(AssertionError):
            outils.pgcde(0, 0)


if __name__ == '__main__':
    unittest.main()
