import unittest


from . import outils


class Tppcm:
    """Classe pour tester le ppcm"""

    def __init__(self, a_=0, b_=0, p_=0):
        self.a, self.b, self.p = a_, b_, p_

    def __str__(self):
        return "a={}, b={}, p={}".format(self.a, self.b, self.p)


class OutilsPpcmTestCase(unittest.TestCase):
    def test_ppcm(self):
        """Test du PPCM."""
        tt = [
            Tppcm(a_=15, b_=10, p_=30),
            Tppcm(a_=-15, b_=10, p_=30),
            Tppcm(a_=15, b_=-10, p_=30),
            Tppcm(a_=0, b_=10, p_=0),
            Tppcm(a_=15, b_=0, p_=0),
        ]
        # print()
        # print("test_ppcm")
        for v_ in tt:
            p_ = outils.ppcm(v_.a, v_.b)
            # print("v", v_, "obtenu :", "p", p_)
            # contrôle de la cohérence du test
            self.assertTrue(0 <= v_.p)
            if 0 != v_.a:
                self.assertTrue(0 == v_.p % v_.a)
            if 0 != v_.b:
                self.assertTrue(0 == v_.p % v_.b)
            # contrôle du résultat du test
            self.assertEqual(v_.p, p_)

        with self.assertRaises(AssertionError):
            outils.ppcm(0, 0)


if __name__ == '__main__':
    unittest.main()
