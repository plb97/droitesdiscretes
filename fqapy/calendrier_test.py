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

from . import calendrier


class Tcalend:
    def __init__(self, j_=0, t_=0., y_=0, m_=0, d_=0., c_=None, js_=0):
        self.j = j_
        self.dt = calendrier.Date(y_, m_, d_, c_)
        self.js = js_
        self.jj = calendrier.EPOQUE_JJ + j_ + t_
        # ATTENTION : La façon dont on écrit self.jd peut avoir des conséquences sur la précision.
        #             self.jd = EPOQUE_JJ + jj + t est équivalent à self.jd = (EPOQUE_JJ + jj) + t
        #             et pas à self.jd = EPOQUE_JJ + (jj + t), cette dernière façon de faire induit
        #             une perte de précision sensible (~ 5e-11).

    def __str__(self):
        # ATTENTION : Il faut forcer l'appel à str pour les jours de la semaine. Pourquoi ?
        return "j={}, dt={}, js={}, jj={}".format(self.jj, self.dt, str(self.js), self.jj)


class CalendrierTestCase(unittest.TestCase):
    """Série de tests utilisée pour valider les formes quasi affines du module """

    def test_jour_julien(self):
        """Test du jour julien (à ne pas confondre avec une date du calendrier julien)"""
        tt = [
            {"jd": 2436116.31, "jj": 2436116.81}
        ]
        print("\ntest_jour_julien")
        for v_ in tt:
            print("v", v_)

            jj = calendrier.EPOQUE_JJ + v_["jj"]
            print("jj={} {}".format(jj, jj()))
            jd = calendrier.EPOQUE_JD + v_["jd"]
            print("jd={} {}".format(jd, jd()))
            # Le nouveau jj va être un nombre
            jj = jj - calendrier.EPOQUE_JJ
            self.assertEqual(jj, v_["jj"])
            # Le nouveau jd va être un nombre
            jd = jd - calendrier.EPOQUE_JD
            self.assertEqual(jd, v_["jd"])
            jjp2 = calendrier.EPOQUE_JJ + v_["jj"] + 2
            print("jjp2", jjp2, "jj", jj)
            jjp2 = jjp2 - calendrier.EPOQUE_JJ
            self.assertTrue(calendrier.egalf(jjp2, jj + 2))
            jjm35 = (calendrier.EPOQUE_JJ + v_["jj"]) - 3.5
            print("jjm35", jjm35, "jj", jj)
            jjm35 = jjm35 - calendrier.EPOQUE_JJ
            self.assertTrue(calendrier.egalf(jjm35, jj - 3.5))
            jjp2 = calendrier.EPOQUE_JJ + v_["jj"]
            print("jjp2", jjp2, "jj", jj)
            jjp2 += 2
            print("jjp2", jjp2, "jj", jj)
            self.assertTrue(calendrier.egalf(jjp2 - calendrier.EPOQUE_JD, jd + 2))
            jjm35 = calendrier.EPOQUE_JJ + v_["jj"]
            print("jjm35", jjm35, "jj", jj)
            jjm35 -= 3.5
            print("jjm35", jjm35, "jj", jj)
            self.assertTrue(calendrier.egalf(jjm35 - calendrier.EPOQUE_JD, jd - 3.5))
            # évaluation faite de gauche à droite
            jj = calendrier.EPOQUE_JD + v_["jd"] - calendrier.EPOQUE_JJ
            # translations
            jjp5, jjm3 = jj + 5, jj - 3
            # différences
            dif = jjp5 - jjm3
            print("jj", jj, "jjp5", jjp5, "jjm3", jjm3, "jjp5-jjm3", dif)
            self.assertEqual(dif, 8.0)

    # noinspection SpellCheckingInspection
    def test_calend_gregorien(self):
        """Test du calendrier grégorien"""
        c_ = calendrier.CALENDRIER_GRE
        tt = [
            # lancement du premier Spoutnik
            Tcalend(j_=2436116, t_=0.81, y_=1957, m_=calendrier.Mois.OCTOBRE, d_=4.81, c_=c_, js_=calendrier.Jours.VENDREDI),
            Tcalend(j_=2448449, t_=0.25, y_=1991, m_=calendrier.Mois.JUILLET, d_=11.25, c_=c_, js_=calendrier.Jours.JEUDI),
            Tcalend(j_=2451545, t_=0.5, y_=2000, m_=calendrier.Mois.JANVIER, d_=1.5, c_=c_, js_=calendrier.Jours.SAMEDI),
            Tcalend(j_=2457578, t_=0.75, y_=2016, m_=calendrier.Mois.JUILLET, d_=8.75, c_=c_, js_=calendrier.Jours.VENDREDI),
            Tcalend(j_=2299161, t_=0.0, y_=1582, m_=calendrier.Mois.OCTOBRE, d_=15.0, c_=c_, js_=calendrier.Jours.VENDREDI),
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
        c_ = calendrier.CALENDRIER_JUL
        tt = [
            # Tcalend(j=1842713, t=0.75, y=333,m=Months.JANUARY,d=27.75, c=c, js=Days.SATURDAY),
            # Tcalend(j=2299160, t=0.5, y=1582,m=Months.OCTOBER,d=4.5, c=c, js=Days.THURSDAY),
            Tcalend(j_=1842713, t_=0.75, y_=333, m_=calendrier.Mois.JANVIER, d_=27.75, c_=c_, js_=calendrier.Jours.SAMEDI),
            Tcalend(j_=2299160, t_=0.5, y_=1582, m_=calendrier.Mois.OCTOBRE, d_=4.5, c_=c_, js_=calendrier.Jours.JEUDI),
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
        c_ = calendrier.CALENDRIER_ISL
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

    def test_date(self):
        """Test des dates"""
        tt = [
            {"date": calendrier.Date(2019, 6, 27, calendrier.CALENDRIER_GRE), "jj": calendrier.EPOQUE_JJ + 2458662},
        ]
        print("\ntest_date")
        for v_ in tt:
            print("v", v_)
            jj_ = v_["date"]()
            date_ = calendrier.CALENDRIER_GRE.date(jj_)
            print("jj", jj_)
            self.assertEqual(v_["jj"], jj_)
            self.assertEqual(calendrier.CALENDRIER_GRE, v_["date"].calendrier)
            self.assertEqual(v_["date"], date_)


if "__main__" == __name__:

    print("EPOQUE_JUL - EPOQUE_JJ", calendrier.EPOQUE_JUL - calendrier.EPOQUE_JJ)
    print("EPOQUE_COP - EPOQUE_JJ", calendrier.EPOQUE_COP - calendrier.EPOQUE_JJ)
    print("EPOQUE_ETH - EPOQUE_JJ", calendrier.EPOQUE_ETH - calendrier.EPOQUE_JJ)

    unittest.main()
