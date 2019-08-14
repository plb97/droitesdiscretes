""" Test des Formes Quasi Affines.
    Les formes quasi affines sont des fonctions 'f' définies par :
    
        f(x) = [(ax + r) / b]
    
    où a, b et c sont des entiers avec a > r >= 0 et [x] désigne la 
    valeur entière ('floor') de x.
    
    Entre autres, les formes quasi affines sont utilisables dans les calculs de
    calendriers.
    Dans son livre 'La saga des calendriers ou le frisson millénariste'
    (Bibliothèque pour la Science, 1998), Jean Lefort en donne une illustration 
    intéressante.
    Cette utilisation des droites discrètes a été proposée en 1992 par A. Troesch :
    
    Droites discrètes et calendriers (Albert Troesch)
    https://mathinfo.unistra.fr/websites/math-info/irem/Publications/L_Ouvert/n071/o_71_27-42.pdf
"""

import unittest

from .calendrier import *


class Tdivent:
    """Classe pour tester la division entière"""

    def __init__(self, n_=0, d=0, q=0, r=0):
        self.n, self.d, self.q, self.r = n_, d, q, r

    def __str__(self):
        return "n={}, d={}, q={}, r={}".format(self.n, self.d, self.q, self.r)


class Tent:
    """Classe pour tester la partie entière"""

    def __init__(self, f_=0.0, q=0, r=0.0, sup=False):
        self.f, self.q, self.r, self.sup = f_, q, r, sup

    def __str__(self):
        return "f={}, q={}, r={}".format(self.f, self.q, self.r)


class Tfqa:
    """Classe pour tester les formes quasi affines"""

    def __init__(self, i_=0, n_=0, a_=0, b_=1, r_=0):
        self.i, self.n, self.f = i_, n_, Fqa(a_, b_, r_)

    def __str__(self):
        return "i={}, n={}, f={}".format(self.i, self.n, self.f)


class Tcodes:
    """Classe pour tester les codes des formes quasi affines"""

    def __init__(self, x0_=0, y0_=0, c_=None, ok=False, a_=0, b_=1, r_=0):
        self.x0, self.y0, self.c, self.ok, self.f = x0_, y0_, c_, ok, Fqa(a_, b_, r_)

    def __str__(self):
        return "x0={}, y0={}, c={}, ok={}, f={}".format(self.x0, self.y0, self.c, self.ok, self.f)


class Tcalend:
    def __init__(self, j_=0, t_=0., y_=0, m_=0, d_=0., c_=None, js_=0):
        self.j = j_
        self.dt = Date(y_, m_, d_, c_)
        self.js = js_
        self.jj = EPOQUE_JJ + j_ + t_
        # ATTENTION : La façon dont on écrit self.jd peut avoir des conséquences sur la précision.
        #             self.jd = EPOQUE_JJ + jj + t est équivalent à self.jd = (EPOQUE_JJ + jj) + t
        #             et pas à self.jd = EPOQUE_JJ + (jj + t), cette dernière façon de faire induit
        #             une perte de précision sensible (~ 5e-11).

    def __str__(self):
        # ATTENTION : Il faut forcer l'appel à str pour les jours de la semaine. Pourquoi ?
        return "j={}, dt={}, js={}, jj={}".format(self.jj, self.dt, str(self.js), self.jj)


class AllTest(unittest.TestCase):
    """Série de tests utilisée pour valider les formes quasi affines du module """

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
        print("\ntest_divent")
        for v_ in tt:
            q_, r_ = divent(v_.n, v_.d)
            print("v", v_, "obtenu :", "q", q_, "r", r_)
            self.assertTrue(0 <= r_ < abs(v_.d))
            self.assertEqual(v_.n, q_ * v_.d + r_)
            self.assertEqual(v_.q, q_)
            self.assertEqual(v_.r, r_)

        with self.assertRaises(ValueError):
            divent(3, 0)

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
        print("\ntest_ent")
        for v_ in tt:
            q_, r_ = ent(v_.f, v_.sup)
            print("v", v_, "obtenu :", "q", q_, "r", r_)
            if not v_.sup:
                self.assertTrue(0.0 <= r_ < 1.0)
            else:
                self.assertTrue(0.0 >= r_ > -1.0)
            self.assertTrue(egalf(v_.f, q_ + r_))
            self.assertEqual(v_.q, q_)
            self.assertTrue(egalf(v_.r, r_))

        with self.assertRaises(TypeError):
            ent("1.2")
            egalf(1, 1.2)
            egalf(1.2, 1)
        with self.assertRaises(ValueError):
            egalf(1.2, 1.2, prec=-1.0e-10)

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
        print("\ntest_fqa_valeur")
        for v_ in tt:
            print("v", v_)
            n_ = v_.f(v_.i)
            i_, r_ = v_.f.divfqa(n_)
            print("v", v_, "obtenu :", "n", n_, "i", i_, "r", r_)
            self.assertEqual(v_.n, n_)
            self.assertEqual(v_.i, i_)
            self.assertEqual(0, r_)

    def test_codes(self):
        """Test des codes."""
        tt = [
            Tcodes(x0_=0, y0_=0, c_=[2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1], ok=True, a_=12,
                   b_=7, r_=5),
            # calendrier musulman (cycle des annees)
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
        print("\ntest_codes")
        for v_ in tt:
            print("v", v_)
            f_ = codes(x0_=v_.x0, y0_=v_.y0, liste_codes=v_.c)
            print("f", f_)
            self.assertEqual(v_.f, f_)

    def test_jour_julien(self):
        """Test du jour julien (à ne pas confondre avec une date du calendrier julien)"""
        tt = [
            {"jd": 2436116.31, "jj": 2436116.81}
        ]
        print("\ntest_jour_julien")
        for v_ in tt:
            print("v", v_)

            jj = EPOQUE_JJ + v_["jj"]
            print("jj={} {}".format(jj, jj()))
            jd = EPOQUE_JD + v_["jd"]
            print("jd={} {}".format(jd, jd()))
            # Le nouveau jj va être un nombre
            jj = jj - EPOQUE_JJ
            self.assertEqual(jj, v_["jj"])
            # Le nouveau jd va être un nombre
            jd = jd - EPOQUE_JD
            self.assertEqual(jd, v_["jd"])
            jjp2 = EPOQUE_JJ + v_["jj"] + 2
            print("jjp2", jjp2, "jj", jj)
            jjp2 = jjp2 - EPOQUE_JJ
            self.assertTrue(egalf(jjp2, jj + 2))
            jjm35 = (EPOQUE_JJ + v_["jj"]) - 3.5
            print("jjm35", jjm35, "jj", jj)
            jjm35 = jjm35 - EPOQUE_JJ
            self.assertTrue(egalf(jjm35, jj - 3.5))
            jjp2 = EPOQUE_JJ + v_["jj"]
            print("jjp2", jjp2, "jj", jj)
            jjp2 += 2
            print("jjp2", jjp2, "jj", jj)
            self.assertTrue(egalf(jjp2 - EPOQUE_JD, jd + 2))
            jjm35 = EPOQUE_JJ + v_["jj"]
            print("jjm35", jjm35, "jj", jj)
            jjm35 -= 3.5
            print("jjm35", jjm35, "jj", jj)
            self.assertTrue(egalf(jjm35 - EPOQUE_JD, jd - 3.5))
            # évaluation faite de gauche à droite
            jj = EPOQUE_JD + v_["jd"] - EPOQUE_JJ
            # translations
            jjp5, jjm3 = jj + 5, jj - 3
            # différences
            dif = jjp5 - jjm3
            print("jj", jj, "jjp5", jjp5, "jjm3", jjm3, "jjp5-jjm3", dif)
            self.assertEqual(dif, 8.0)

    # noinspection SpellCheckingInspection
    def test_calend_gregorien(self):
        """Test du calendrier grégorien"""
        c_ = CALENDRIER_GRE
        tt = [
            # lancement du premier Spoutnik
            Tcalend(j_=2436116, t_=0.81, y_=1957, m_=Mois.OCTOBRE, d_=4.81, c_=c_, js_=Jours.VENDREDI),
            Tcalend(j_=2448449, t_=0.25, y_=1991, m_=Mois.JUILLET, d_=11.25, c_=c_, js_=Jours.JEUDI),
            Tcalend(j_=2451545, t_=0.5, y_=2000, m_=Mois.JANVIER, d_=1.5, c_=c_, js_=Jours.SAMEDI),
            Tcalend(j_=2457578, t_=0.75, y_=2016, m_=Mois.JUILLET, d_=8.75, c_=c_, js_=Jours.VENDREDI),
            Tcalend(j_=2299161, t_=0.0, y_=1582, m_=Mois.OCTOBRE, d_=15.0, c_=c_, js_=Jours.VENDREDI),
        ]
        print("\ntest_calend_grégorien")
        for v_ in tt:
            print("v", v_)
            jj = v_.dt()
            js = jj.jour_semaine()
            print("jj", jj, js)
            # vp = jj.kjour_semaine_precedant(Jours.VENDREDI)
            # vpp = jj.kjour_semaine_plus_proche(Jours.VENDREDI)
            # vav = jj.kjour_semaine_avant(Jours.VENDREDI)
            # vap = jj.kjour_semaine_apres(Jours.VENDREDI)
            # print("jj",jj,js,
            #      "\n vendredi précédent", vp, vp.jour_semaine(), 
            #      "\n vendredi plus proche", vpp, vpp.jour_semaine(),
            #      "\n vendredi avant", vav, vav.jour_semaine(),
            #      "\n vendredi apres", vap, vap.jour_semaine(),
            #     )
            self.assertEqual(v_.jj, jj)
            self.assertEqual(v_.js, js)
            dt_ = c_.date(v_.jj)
            print("dt", dt_)
            self.assertEqual(v_.dt, dt_)

    def test_calend_julien(self):
        """Test du calendrier julien"""
        c_ = CALENDRIER_JUL
        tt = [
            # Tcalend(j=1842713, t=0.75, y=333,m=Months.JANUARY,d=27.75, c=c, js=Days.SATURDAY),
            # Tcalend(j=2299160, t=0.5, y=1582,m=Months.OCTOBER,d=4.5, c=c, js=Days.THURSDAY),
            Tcalend(j_=1842713, t_=0.75, y_=333, m_=Mois.JANVIER, d_=27.75, c_=c_, js_=Jours.SAMEDI),
            Tcalend(j_=2299160, t_=0.5, y_=1582, m_=Mois.OCTOBRE, d_=4.5, c_=c_, js_=Jours.JEUDI),
        ]
        print("\ntest_calend_julien")
        for v_ in tt:
            print("v", v_)
            jj = v_.dt()
            js = jj.jour_semaine()
            print("jj", jj, "js", js)
            self.assertEqual(v_.jj, jj)
            self.assertEqual(v_.js, js)
            dt_ = c_.date(v_.jj)
            print("dt", dt_)
            self.assertEqual(v_.dt, dt_)

    def test_calend_musulman(self):
        """Test du calendrier musulman"""
        c_ = CALENDRIER_ISL
        tt = [
            # samedi 1er janvier 2000
            # Tcalend(j=2451545, t=0.25, y=1420,m=Mois.RAMADAN,d=24.25, c=CALENDRIER_ISL, js=Jours.ESSABAT),
            Tcalend(j_=2451545, t_=0.25, y_=1420, m_=9, d_=24.25, c_=c_, js_=5),
            # vendredi 8 juillet 2016
            # Tcalend(j=2457578, t=0.5, y=1437,m=Mois.CHAWWAL,d=2.5, c=CALENDRIER_ISL, js=Jours.ELJOMOA),
            Tcalend(j_=2457578, t_=0.5, y_=1437, m_=10, d_=2.5, c_=c_, js_=4),
        ]
        print("\ntest_calend_musulman")
        for v_ in tt:
            print("v", v_)
            jj = v_.dt()
            js = jj.jour_semaine()
            print("jj", jj, "js", js)
            self.assertEqual(v_.jj, jj)
            self.assertEqual(v_.js, js)
            dt_ = c_.date(v_.jj)
            print("dt", dt_)
            self.assertEqual(v_.dt, dt_)

    def test_base_temps(self):
        """Test de la base temps"""
        tt = [
            {"jhms": [7, 3, 48, 13], "t": 618493, "inv": [7, 3, 48, 13], },
            {"jhms": [-7, 3, 48, 13], "t": -591107, "inv": [-7, 3, 48, 13], },
            {"jhms": [7, -3, 48, 13], "t": 596893, "inv": [6, 21, 48, 13], },
            {"jhms": [7, 3, -48, 13], "t": 612733, "inv": [7, 2, 12, 13], },
            {"jhms": [7, 3, 48, -13], "t": 618467, "inv": [7, 3, 47, 47], },
            {"jhms": [0, -3, -48, -13], "t": -13693, "inv": [-1, 20, 11, 47], },
        ]
        print("\ntest_base_temps")
        for v_ in tt:
            print("v", v_)
            t0 = 86400 * v_["jhms"][0] + 3600 * v_["jhms"][1] + 60 * v_["jhms"][2] + v_["jhms"][3]
            s_ = t0
            j_, s_ = divent(s_, 86400)
            h_, s_ = divent(s_, 3600)
            m_, s_ = divent(s_, 60)
            print("t0", t0, "->", [j_, h_, m_, s_])
            t_ = BASE_TEMPS([v_["jhms"][0], v_["jhms"][1], v_["jhms"][2], v_["jhms"][3]])
            print("t", t_)
            self.assertEqual(t_, v_["t"])
            self.assertEqual(v_["inv"], BASE_TEMPS.inv(t_))

    def test_date(self):
        """Test des dates"""
        tt = [
            {"date": Date(2019, 6, 27, CALENDRIER_GRE), "jj": EPOQUE_JJ + 2458662},
        ]
        print("\ntest_date")
        for v_ in tt:
            print("v", v_)
            jj_ = v_["date"]()
            date_ = CALENDRIER_GRE.date(jj_)
            print("jj", jj_)
            self.assertEqual(v_["jj"], jj_)
            self.assertEqual(CALENDRIER_GRE, v_["date"].calendrier)
            self.assertEqual(v_["date"], date_)


if "__main__" == __name__:

    print("EPOQUE_JUL - EPOQUE_JJ", EPOQUE_JUL - EPOQUE_JJ)
    print("EPOQUE_COP - EPOQUE_JJ", EPOQUE_COP - EPOQUE_JJ)
    print("EPOQUE_ETH - EPOQUE_JJ", EPOQUE_ETH - EPOQUE_JJ)

    unittest.main()
