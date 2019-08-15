import unittest

from . import outils


class Tent:
    """Classe pour tester la partie entière"""

    def __init__(self, f_=0.0, q=0, r=0.0, sup=False):
        self.f, self.q, self.r, self.sup = f_, q, r, sup

    def __str__(self):
        return "f={}, q={}, r={}".format(self.f, self.q, self.r)


class OutilsEntTestCase(unittest.TestCase):
    def test_ent(self):
        """Test de la partie entière."""
        tt = [
            Tent(f_=1.2, q=1, r=0.2),
            Tent(f_=-1.2, q=-2, r=0.8),
            Tent(f_=1.0, q=1, r=0.0),
            Tent(f_=-1.0, q=-1, r=0.0),
            Tent(f_=1.2, q=2, r=-0.8, sup=True),
            Tent(f_=-1.2, q=-1, r=-0.2, sup=True),
            Tent(f_=1.0, q=1, r=0.0, sup=True),
            Tent(f_=-1.0, q=-1, r=0.0, sup=True),
        ]
        # print()
        # print("test_ent")
        for v_ in tt:
            q_, r_ = outils.ent(v_.f, v_.sup)
            # print("v", v_, "obtenu :", "q", q_, "r", r_)
            if not v_.sup:
                self.assertTrue(0.0 <= r_ < 1.0)
            else:
                self.assertTrue(0.0 >= r_ > -1.0)
            self.assertTrue(outils.egalf(v_.f, q_ + r_))
            self.assertEqual(v_.q, q_)
            self.assertTrue(outils.egalf(v_.r, r_))


if __name__ == '__main__':
    unittest.main()
