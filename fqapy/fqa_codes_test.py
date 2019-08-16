import unittest

from . import fqa


class Tcodes:
    """Classe pour tester les codes des formes quasi affines"""

    def __init__(self, x0_=0, y0_=0, c_=None, ok=False, a_=0, b_=1, r_=0):
        self.x0, self.y0, self.c, self.ok, self.f = x0_, y0_, c_, ok, fqa.Fqa(a_, b_, r_)

    def __str__(self):
        return "x0={}, y0={}, c={}, ok={}, f={}".format(self.x0, self.y0, self.c, self.ok, self.f)


class FqaCodesTestCase(unittest.TestCase):
    def test_codes(self):
        """Test des codes."""
        tt = [
            Tcodes(x0_=0, y0_=0, c_=[2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1], ok=True, a_=12,
                   b_=7, r_=5),
            # calendrier musulman (cycle des années)
            Tcodes(x0_=0, y0_=2, c_=[3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3], ok=True, a_=30,
                   b_=11, r_=26),
            # Tcodes(x0=0, y0=0, c=[3,3,3,2,3,3,3,2,3,3,2,3,3,3,2,3,3,3,2,3,3,2], ok=True, a=30, b=11, r=0),
            # calendrier juif (années embolismiques)
            Tcodes(x0_=0, y0_=0, c_=[3, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2], ok=True, a_=19, b_=7, r_=5),
            # jours (écarts ou codes successifs entre j+1 et j)
            Tcodes(x0_=1, y0_=0, c_=[1, 1, 1, 1, 1, 1, 1, 1], ok=True, a_=1, b_=1, r_=-1),
            # mois (durée des mois de mars a février sur une année glissante)
            # remarque : le mois de février n'a pas d'effet sur le résultat
            Tcodes(x0_=3, y0_=0, c_=[31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28], ok=True, a_=153, b_=5, r_=-457),
            # calendrier julien (années)
            # (durées des annees sur 2 périodes de 4 ans)
            # (origine -4712 a minuit c-a-d jd+0.5)
            # 4712 * 365.25 = 1721058
            # le premier mars seules les années comptent
            # l'année 0 (la variable x0) est bissextile :
            # du 1 janvier 0 au 1 mars 0 = 31+29=60
            # 1721058 + 60 = 1721118 (la valeur y0)
            Tcodes(x0_=0, y0_=1721118, c_=[365, 365, 365, 366, 365, 365, 365, 366], ok=True, a_=1461, b_=4, r_=6884472),
            # Autre façon d'obtenir le même résultat
            # x0 = 1 = année 1
            # 1721424 = EPOQUE_JUL
            # 59 = nombre de jours entre le premier janvier an 1 et le premier mars an 1
            # REMARQUE : 1721424 - 1721118 = 306 = 366 - 60 = nombre de jours entre le
            #            premier mars an 0 et le premier janvier an 1 sachant que l'an 0
            #            est bissextile (de toute manière, il y a toujours 306 jours entre
            #            le premier mars d'une année et le premier janvier de la suivante).
            Tcodes(x0_=1, y0_=1721424 + 59, c_=[365, 365, 366, 365, 365, 365, 366, 365], ok=True, a_=1461, b_=4,
                   r_=6884472),
            # calendrier grégorien (siècles)
            # (durées des siècles sur deux périodes de 400 ans)
            # on fait commencer le jd a minuit et non pas a midi (jd+0.5)
            # on impose la continuité du jd :
            #   jd grégorien(15 octobre 1582) = jd julien(4 octobre 1582) + 1
            # remarque : l'année grégorienne 1582 n'a que 355 jours
            #            de meme l'annee julienne 46 avant JC eut 445 jours
            # remarque : John Herschel (1792-1871)) proposa de retirer
            #            au calendrier grégorien une année bissextile tous
            #            les 4000 ans (les annees divisibles par 4000 ne seraient
            #            plus bissextiles) mais a ce jour cela n'a pas ete retenu
            #            et heureusement car cela préparerait le "bug" de l'an 4000...
            # jd julien(4 octobre 1582) = 2299160
            # du 4 octobre 1582 au 15 octobre 1582 = 1
            # du 15 octobre au 31 decembre = 78
            # année 1583 = 365
            # du 1 janvier 1584 au 31 decembre 1599 = 5844
            # du 1 janvier 1600 au 29 fevrier 1600 = 60
            # 2299160 + 1 + 78 + 365 + 5844 + 60 = 2305508
            # le 1 mars 1600, seul le siècle s intervient dans le résultat (jd)
            # s = 1600 / 100 = 16 (variable x0)
            # jd grégorien (1 mars 1600) = 2305508 (valeur y0)
            # [(a*s + r) / b] = jj = [(a*16 + r) / b] = 2305508
            Tcodes(x0_=16, y0_=2305508, c_=[36524, 36524, 36524, 36525, 36524, 36524, 36524, 36525],
                   ok=True, a_=146097, b_=4, r_=6884480),
            # Dans une quantité de secondes
            # pour déterminer les jours
            Tcodes(x0_=0, y0_=0, c_=[86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400],
                   ok=True, a_=86400, b_=1, r_=0),
            # pour déterminer les heures
            Tcodes(x0_=0, y0_=0, c_=[3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600],
                   ok=True, a_=3600, b_=1, r_=0),
            # pour déterminer les minutes
            Tcodes(x0_=0, y0_=0, c_=[60, 60, 60, 60, 60, 60, 60, 60],
                   ok=True, a_=60, b_=1, r_=0),
            # pour déterminer les secondes
            Tcodes(x0_=0, y0_=0, c_=[1, 1, 1, 1, 1, 1, 1, 1],
                   ok=True, a_=1, b_=1, r_=0),
        ]
        # print()
        # print("test_codes")
        for v_ in tt:
            f_ = fqa.codes(x0_=v_.x0, y0_=v_.y0, liste_codes=v_.c)
            # print("v", v_, "f", f_)
            self.assertEqual(v_.f, f_)

        with self.assertRaises(AssertionError):
            fqa.codes([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])


if __name__ == '__main__':
    unittest.main()
