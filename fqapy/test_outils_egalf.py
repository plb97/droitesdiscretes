import unittest

from . import outils


class Tegalf:
    """Classe pour tester egalf"""

    def __init__(self, a_=0.0, b_=0.0, ok_=True):
        self.a, self.b, self.ok = a_, b_, ok_

    def __str__(self):
        return "a={}, b={}, ok={}".format(self.a, self.b, self.ok)


class OutilsEgalfTestCase(unittest.TestCase):
    def test_egalf(self):
        tt = [
            Tegalf(a_=1.2, b_=1.2, ok_=True),
            Tegalf(a_=1.2, b_=1.2 + 1e-15, ok_=False),
            Tegalf(a_=1.2, b_=1.2 + 0.9e-15, ok_=True),
            Tegalf(a_=1.0, b_=1, ok_=True),
            Tegalf(a_=1, b_=1.0, ok_=True),
            Tegalf(a_=1, b_=1, ok_=True),
        ]
        # print()
        # print("test_egalf")
        for v_ in tt:
            ok_ = outils.egalf(v_.a, v_.b)
            # print("v", v_, "obtenu: ", "ok", ok_)
            self.assertEqual(v_.ok, ok_)

        with self.assertRaises(AssertionError):
            outils.egalf(1.2, 1.2, prec=0.0)
            outils.egalf(1.2, 1.2, prec=-1e-15)


if __name__ == '__main__':
    unittest.main()
