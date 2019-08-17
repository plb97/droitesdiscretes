import unittest

from . import fqa
from . import outils


class FqaBaseTestCase(unittest.TestCase):

    def test_base_temps(self):
        """Test de la base temps"""
        tt = [
            # 7 jours 3 heures 48 minutes 13 secondes
            {"jhms": [7, 3, 48, 13], "t": 618493, "inv": [7, 3, 48, 13], },
            # -7 jours 3 heures 48 minutes 13 secondes
            {"jhms": [-7, 3, 48, 13], "t": -591107, "inv": [-7, 3, 48, 13], },
            # 7 jours -3 heures 48 minutes 13 secondes
            # 6 jours 21 heures 48 minutes 13 secondes
            {"jhms": [7, -3, 48, 13], "t": 596893, "inv": [6, 21, 48, 13], },
            # 7 jours 3 heures -48 minutes 13 secondes
            # 7 jours 2 heures 12 minutes 13 secondes
            {"jhms": [7, 3, -48, 13], "t": 612733, "inv": [7, 2, 12, 13], },
            # 7 jours 3 heures 48 minutes -13 secondes
            # 7 jours 3 heures 47 minutes 47 secondes
            {"jhms": [7, 3, 48, -13], "t": 618467, "inv": [7, 3, 47, 47], },
            # 0 jours -3 heures -48 minutes -13 secondes
            # -1 jours 20 heures 11 minutes 47 secondes
            {"jhms": [0, -3, -48, -13], "t": -13693, "inv": [-1, 20, 11, 47], },
            # 3 heures 48 minutes 13 secondes
            # 0 jours 3 heures 48 minutes 13 secondes
            {"jhms": [0, 3, 48, 13], "t": 13693, "inv": [0, 3, 48, 13], },
            # 48 minutes 13 secondes
            # 0 jours 0 heures 48 minutes 13 secondes
            {"jhms": [48, 13], "t": 2893, "inv": [0, 0, 48, 13], },
        ]
        # print()
        # print("test_base_temps")
        for v_ in tt:
            u_ = ([0] * (4 - len(v_["jhms"])) + v_["jhms"])[-4:]
            # t0 = 86400 * u_[0] + 3600 * u_[1] + 60 * u_[2] + u_[3]
            # print("v", v_, "t0", t0)
            # s_ = t0
            # j_, s_ = outils.divent(s_, 86400)
            # h_, s_ = outils.divent(s_, 3600)
            # m_, s_ = outils.divent(s_, 60)
            # print("t0", t0, "->", [j_, h_, m_, s_])
            t_ = fqa.BASE_TEMPS(u_)
            # print("t", t_)
            self.assertEqual(t_, v_["t"])
            self.assertEqual(v_["inv"], fqa.BASE_TEMPS.inv(t_))


if __name__ == '__main__':
    unittest.main()
