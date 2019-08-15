import unittest

from . import fqa


class Tfqa:
    """Classe pour tester les formes quasi affines"""

    def __init__(self, i_=0, n_=0, a_=0, b_=1, r_=0):
        self.i, self.n, self.f = i_, n_, fqa.Fqa(a_, b_, r_)

    def __str__(self):
        return "i={}, n={}, f={}".format(self.i, self.n, self.f)


class FqaValeurTestCase(unittest.TestCase):
    def test_fqa_valeur(self):
        """Test des valeurs des formes quasi affine."""
        tt = [
            # i valeur initiale
            # n = fqa(i)
            # i, r = divfqa(n) ~ i = n // fqa et r = n % fqa
            # siècle calendrier grégorien
            Tfqa(i_=20, n_=2451605, a_=146097, b_=4, r_=6884480),
            # année calendrier grégorien
            Tfqa(i_=16, n_=5844, a_=1461, b_=4, r_=0),
            # mois calendrier grégorien
            Tfqa(i_=7, n_=122, a_=153, b_=5, r_=-457),
            # jour calendrier grégorien
            Tfqa(i_=8, n_=7, a_=1, b_=1, r_=-1),
        ]
        # print()
        # print("test_fqa_valeur")
        for v_ in tt:
            n_ = v_.f(v_.i)
            i_, r_ = v_.f.divfqa(n_)
            # print("v", v_, "obtenu :", "n", n_, "i", i_, "r", r_)
            self.assertEqual(v_.n, n_)
            self.assertEqual(v_.i, i_)
            self.assertEqual(0, r_)


if __name__ == '__main__':
    unittest.main()
