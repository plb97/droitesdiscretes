# Calendriers
"""Définition des calendriers Julien, Grégorien et musulman.
Bibliographie.
    [1] 'La saga des calendriers' (Jean LEFORT, Pour la Science, 1998).
    [2] 'Calendrical Calculations'.
    (Nachum Dershowitz et Edward M. Reingold, Cambridge University Press, 1997).
    [3] 'Droites discrètes et calendriers'
    (Albert Troesch, Mathématiques et sciences humaines, tome 141, 1998, p. 11-41)
        disponible sur http://www.numdam.org/article/MSH_1998__141__11_0.pdf
    [4] 'Calculs astronomiques à l'usage des amateurs'
    (Jean MEEUS, Société Astronomique de France, Paris, 2014).

Jours de la semaine commençant par 0 pour le lundi
ATTENTION : différent de [2] p. 17 où le dimanche débute le semaine."""

from enum import IntEnum

from .fqa import *


def _corr_am(a_=0, m_=1, o_=1):
    # Entrée : une année a et un mois m.
    # Sortie : une année ajustée a et un mois m tels que o <= m <= o+11.
    i_, m_ = divent(m_ - o_, 12)
    a_ += i_
    m_ += o_
    return a_, m_


def _norm_am(a_=0, m_=1):
    # Entrée : une année a et un mois m compris entre 1 et 12.
    # Sortie : une année ajustée a et un mois m tels que 3 <= m <= 14.
    a_, m_ = _corr_am(a_, m_)
    if 3 > m_:
        m_ += 12
        a_ -= 1
    return a_, m_


def _dnorm_am(a_=0, m_=1):
    # Entrée : une année a et un mois m compris entre 3 et 14.
    # Sortie : une année ajustée a et un mois m tels que 1 <= m <= 12.
    a_, m_ = _corr_am(a_, m_, 3)
    if 12 < m_:
        m_ -= 12
        a_ += 1
    return a_, m_


_JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class Jours(IntEnum):
    LUNDI = 0
    MARDI = 1
    MERCREDI = 2
    JEUDI = 3
    VENDREDI = 4
    SAMEDI = 5
    DIMANCHE = 6

    # https://fr.wikiversity.org/wiki/Arabe/Vocabulaire/Jours_et_mois
    # ELETHNAYN = LUNDI       ## الإثنين
    # ETHTHOLATHA = MARDI     ## الثلاثاء
    # ELARBIEAA = MERCREDI    ## الأربعاء
    # ELKHAMIIS = JEUDI       ## الخميس
    # ELJOMOA = VENDREDI      ## الجمعة
    # ESSABAT = SAMEDI        ## السبت
    # ELAHAD = DIMANCHE       ## الأحد
    def __repr__(self):
        return "Jour de la semaine : {} {}".format(self.value, _JOURS[self.value])

    def __str__(self):
        return _JOURS[self.value]


_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class Days(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __repr__(self):
        return "Day of week : {} {}".format(self.value, _DAYS[self.value])

    def __str__(self):
        return _DAYS[self.value]


"""Douze mois de l'année numérotés à partir de 1 pour janvier."""

_MOIS = ["janvier",
         "février",
         "mars",
         "avril",
         "mai",
         "juin",
         "juillet",
         "août",
         "septembre",
         "octobre",
         "novembre",
         "décembre",
         ]


class Mois(IntEnum):
    JANVIER = 1
    FEVRIER = 2
    MARS = 3
    AVRIL = 4
    MAI = 5
    JUIN = 6
    JUILLET = 7
    AOUT = 8
    SEPTEMBRE = 9
    OCTOBRE = 10
    NOVEMBRE = 11
    DECEMBRE = 12

    # https://fr.wikiversity.org/wiki/Arabe/Vocabulaire/Jours_et_mois
    # MOUHARRAM = JANVIER	        ## محرم
    # SAFAR = FEVRIER             ## صفر
    # RABI_AL_AWWAL = MARS        ## ربيع الأول
    # RABI_AL_THANI = AVRIL       ## ربيع الثاني
    # JOUMADA_AL_AWWAL = MAI      ## جمادى الأول
    # JOUMADA_AL_THANI = JUIN     ## جمادى الثاني
    # RAJAB = JUILLET             ## رجب
    # CHA_BAN = AOUT              ## شعبان
    # RAMADAN = SEPTEMBRE         ## رمضان
    # CHAWWAL = OCTOBRE           ## شوال
    # DHOUL_AL_QA_DA = NOVEMBRE   ## ذو القعدة
    # DHOUL_AL_HIJJA = DECEMBRE   ## ذو الحجة
    def __repr__(self):
        return "Mois : {} {}".format(self.value, _MOIS[self.value - 1])

    def __str__(self):
        return _MOIS[self.value - 1]


_MONTHS = ["January",
           "February",
           "March",
           "April",
           "May",
           "June",
           "July",
           "August",
           "September",
           "October",
           "November",
           "December",
           ]


class Months(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def __repr__(self):
        return "Month : {} {}".format(self.value, _MONTHS[self.value - 1])

    def __str__(self):
        return _MONTHS[self.value - 1]


class Date:
    """Date de trois nombres (deux premiers entiers et troisième flottant).
       Aucun traitement ni contrôle de cohérence n'est fait.
       ATTENTION : Une Date doit nécessairement être associée à un calendrier 
       afin de donner un sens aux trois nombres qui la représentent.
    """

    #  REMARQUE : Le choix u, v, w est arbitraire.
    #             Il est fait pour suggérer que u n'est pas forcément
    #             une année, v un mois et w un jour avec heure au sens du
    #             calendrier grégorien (ou autres) même si cela est le plus souvent
    #             le cas dans ce contexte.
    #             L'attribut t contient le temps (l'heure) extrait de w.
    #             Par exemple, pour le calendrier ISO u serait une année,
    #             v un numéro de semaine dans l'année et w un numéro de jour dans
    #             la semaine.
    def __init__(self, u_, v_, w_, calendrier):
        """Entrée : les trois paramètres u, v, w et le calendrier.
        Sortie : Le Date.
        Erreur : Si u ou v n'est pas un entier ou si w n'est pas un flottant ou un entier
                 ou si le calendrier n'est pas un Calendrier.
        """
        assert isinstance(u_, int)
        assert isinstance(v_, int)
        assert (isinstance(w_, float) or isinstance(w_, int))
        assert isinstance(calendrier, Calendrier)
        self.u, self.v = u_, v_
        self.w, self.t = ent(w_)
        self.calendrier = calendrier

    def __eq__(self, autre):
        if not isinstance(autre, Date):
            return False
        return (self.u == autre.u and self.v == autre.v and self.w == autre.w
                and egalf(self.t, autre.t)
                and self.calendrier == autre.calendrier)

    def __call__(self):
        """Date() retourne le Jour julien."""
        return self.calendrier.date_vers_jj(self)

    def __repr__(self):
        # Le format d'une peut (doit ?) dépendre du calendrier.
        return "Date : u={}, v={}, w={}, t={}".format(self.u, self.v, self.w, self.t)

    def __str__(self):
        return "({}, {}, {}, {})".format(self.u, str(self.v), self.w, self.t)


class _Quantite:
    """Une Quantite représente un "nombre" constitué d'une partie entière n et d'un faction f.
    La fraction f vérifie 0.0 <= f < 1.0
    """

    def __init__(self, n_=0, f_=0.0):
        """Entrée : Un nombre entier n et un nombre flottant f.
        Sortie : Une Quantite.
        Erreur : Si n n'est pas un entier ou si f n'est pas un entier ou un flottant.
        """
        if not isinstance(n_, int):
            raise TypeError("Le paramètre n n'est pas un entier")
        if isinstance(f_, int):
            n_ += f_
            f_ = 0.0
        if not isinstance(f_, float):
            raise TypeError("Le paramètre f n'est pas un entier ou un flottant")
        # au final f doit vérifier 0.0 <= f < 1.0.
        j_, self.f = ent(f_)
        self.n = n_ + j_

    def __add__(self, autre):
        """Entrée : un nombre entier ou flottant à ajouter.
        Sortie : Une nouvelle Quantite translatée de autre.
        Erreur : Si autre n'est pas un entier ou un flottant.
        """
        if not (isinstance(autre, float) or isinstance(autre, int)):
            raise TypeError("Le paramètre n'est pas un entier ou un flottant")
        n_, f_ = ent(autre)
        n_ += self.n
        f_ += self.f
        j_, f_ = ent(f_)
        return _Quantite(n_ + j_, f_)

    def __iadd__(self, autre):
        """Entrée : Un nombre entier ou flottant à ajouter.
        Sortie : La même Quantite translaté de autre.
        Erreur : Si autre n'est pas un entier ou un flottant.
        """
        if not (isinstance(autre, float) or isinstance(autre, int)):
            raise TypeError("Le paramètre n'est pas un entier ou un flottant")
        n_, f_ = ent(autre)
        n_ += self.n
        f_ += self.f
        j_, f_ = ent(f_)
        self.n, self.f = n_ + j_, f_
        return self

    def __sub__(self, autre):
        """Soustraire un nombre ou une Quantite.
        Entrée : Un nombre entier ou flottant ou une Quantite à soustraire.
        Sortie : Un nombre flottant si autre est une Quantite.
                 Une Quantite si autre est un nombre.
        Erreur : Si autre n'est pas un entier ou un flottant.
        REMARQUE : Par exemple dans le cas où Quantite représente des dates,
                   la différence entre deux dates à un sens intuitif
                   mais que pourrait signifier :
                   dt1 + dt2
                   dt1 -= dt2
                   dt * 3
                   ... ?
        """
        # Soustraction d'une Quantite -> un nombre
        if isinstance(autre, _Quantite):
            n_, f_ = autre.n, autre.f
            n_, f_ = self.n - n_, self.f - f_
            j_, f_ = ent(f_)
            return n_ + j_ + f_
        # Soustraction d'un nombre -> une Quantite
        elif isinstance(autre, float) or isinstance(autre, int):
            n_, f_ = ent(autre)
            n_, f_ = self.n - n_, self.f - f_
            j_, f_ = ent(f_)
            return _Quantite(n_ + j_, f_)
        else:
            raise TypeError("Le paramètre n'est pas un entier ou un flottant ou un JourJulien")

    def __isub__(self, autre):
        """Entrée : Un nombre entier ou flottant à soustraire.
        Sortie : La même Quantite "augmentée" de autre.
        Erreur : Si autre n'est pas un entier ou un flottant.
        """
        assert (isinstance(autre, float) or isinstance(autre, int))
        n_, f_ = ent(autre)
        n_, f_ = self.n - n_, self.f - f_
        j_, f_ = ent(f_)
        self.n, self.f = n_ + j_, f_
        return self

    def __eq__(self, autre):
        if not isinstance(autre, _Quantite):
            return False
        return self.n == autre.n and egalf(self.f, autre.f)

    def __call__(self):
        return self.n + self.f

    def __repr__(self):
        return "n={}, f={}".format(self.n, self.f)

    def __str__(self):
        return "(n={}, f={})".format(self.n, self.f)


class JourJulien(_Quantite):

    def __add__(self, autre):
        """Force le typage à JourJulien."""
        q = super().__add__(autre)
        return JourJulien(q.n, q.f)

    def __iadd__(self, autre):
        """Force le typage à JourJulien."""
        q = super().__iadd__(autre)
        return JourJulien(q.n, q.f)

    def __sub__(self, autre):
        """Force le typage à JourJulien si nécessaire."""
        q = super().__sub__(autre)
        if isinstance(q, _Quantite):
            return JourJulien(q.n, q.f)
        else:
            return q

    def __isub__(self, autre):
        """Force le typage à JourJulien."""
        q = super().__isub__(autre)
        return JourJulien(q.n, q.f)

    def jour_semaine(self):
        return Jours(self.n % 7)

    def kjour_semaine_precedant(self, k):
        return self - (self.n - k) % 7

    def kjour_semaine_suivant(self, k):
        return self + (6 - (self.n + 6 - k) % 7)

    def kjour_semaine_plus_proche(self, k):
        return self + (3 - (self.n + 3 - k) % 7)

    def kjour_semaine_apres(self, k):
        return self + (7 - (self.n + 7 - k) % 7)

    def kjour_semaine_avant(self, k):
        return self - (1 + (self.n - 1 - k) % 7)


# REMARQUE : Le début du jour est à minuit comme dans [2] et non pas à midi
#           comme pour le jour julien (Julian Day) en astronomie (jd = jj - 0.5).
#           De ce point de vue cela se rapproche de la notion de 
#           'Rata Die' (RD) [2] p. 9 même si l'origine n'est pas la même.
EPOQUE_JJ = JourJulien()
# Par définition
EPOQUE_JD = EPOQUE_JJ + 0.5
# Origine Rata Die : voir [2] p. 14
# EPOQUE_JD = EPOQUE_RD - 1721424.5
EPOQUE_RD = EPOQUE_JD + 1721424.5
EPOQUE_HEB = EPOQUE_RD - 1373427
EPOQUE_MAY = EPOQUE_RD - 1137142
EPOQUE_HIN = EPOQUE_RD - 1132959
EPOQUE_CHI = EPOQUE_RD - 963099
EPOQUE_JUL = EPOQUE_RD - 1
EPOQUE_GRE = EPOQUE_RD + 1
EPOQUE_ISO = EPOQUE_RD + 1
EPOQUE_ETH = EPOQUE_RD + 2430
EPOQUE_COP = EPOQUE_RD + 103605
EPOQUE_PER = EPOQUE_RD + 226896
EPOQUE_ISL = EPOQUE_RD + 227015
EPOQUE_RFR = EPOQUE_RD + 654415
EPOQUE_BAH = EPOQUE_RD + 673222


class Calendrier(Base):
    """Calendrier défini comme dans [1]."""

    def date_vers_jj(self, date: Date) -> JourJulien:
        """Entrée : Une Date(a, m, j, t) représentant la date dans le calendrier.
        Sortie : le Jour julien correspondant.
        Erreur : Si le paramètre n'est pas une date.
        """
        raise NotImplementedError("Méthode non implémentée.")

    def date(self, jj: JourJulien):
        """Entrée : Un Jour julien.
        Sortie : La Date(a, m, j, t) représentant le Jour julien dans le calendrier.
        Erreur : Si le paramètre n'est pas un Jour julien.
        """
        raise NotImplementedError("Méthode non implémentée.")

    # def format(self, jj):
    #    raise NotImplementedError("Méthode non implémentée.")


class _CalendrierGre(Calendrier):
    """Calendrier grégorien [année, mois, jour]."""

    def __init__(self):
        super().__init__([
            Fqa(146097, 4, 6884480),
            Fqa(1461, 4, 0),
            Fqa(153, 5, -457),
            Fqa(1, 1, -1),
        ])

    def date_vers_jj(self, date):
        """Entrée : Une Date(a, m, j, t) représentant la date dans le calendrier.
        Sortie : le Jour julien correspondant.
        Erreur : Si le paramètre n'est pas une date.
        """
        assert isinstance(date, Date)
        a_, m_ = _norm_am(date.u, date.v)
        d_, t = date.w, date.t
        c_, b_ = divent(a_, 100)
        n_ = super().__call__([c_, b_, m_, d_])
        jj_ = JourJulien(n_, t)
        return jj_

    def date(self, jj_):
        """Entrée : Un Jour julien.
        Sortie : La Date(a, m, j, t) représentant le Jour julien dans le calendrier.
        Erreur : Si le paramètre n'est pas un Jour julien.
        """
        assert isinstance(jj_, JourJulien)
        dt_ = super().inv(jj_.n)
        a_, m_ = _dnorm_am(100 * dt_[0] + dt_[1], dt_[2])
        j_ = dt_[3]
        return Date(a_, Mois(m_), j_ + jj_.f, self)


CALENDRIER_GRE = _CalendrierGre()


class _CalendrierJul(Calendrier):
    """Calendrier julien [année, mois, jour]."""

    def __init__(self):
        super().__init__([
            Fqa(1461, 4, 6884472),
            Fqa(153, 5, -457),
            Fqa(1, 1, -1),
        ])

    def date_vers_jj(self, date):
        """Entrée : Une Date(a, m, j, t) représentant la date dans le calendrier.
        Sortie : le Jour julien correspondant.
        Erreur : Si le paramètre n'est pas une date.
        """
        if not isinstance(date, Date):
            raise TypeError("Le paramètre n'est pas une Date")
        a_, m_ = _norm_am(date.u, date.v)
        d_, t_ = date.w, date.t
        n_ = super().__call__([a_, m_, d_])
        jj_ = JourJulien(n_, t_)
        return jj_

    def date(self, jj_):
        """Entrée : Un Jour julien.
        Sortie : La Date(a, m, j, t) représentant le Jour julien dans le calendrier.
        Erreur : Si le paramètre n'est pas un Jour julien.
        """
        assert isinstance(jj_, JourJulien)
        dt_ = super().inv(jj_.n)
        a_, m_ = _dnorm_am(dt_[0], dt_[1])
        j_ = dt_[2]
        return Date(a_, Mois(m_), j_ + jj_.f, self)


CALENDRIER_JUL = _CalendrierJul()


class _CalendrierIsl(Calendrier):
    """Calendrier musulman [année, mois, jour]."""

    def __init__(self):
        super().__init__([
            Fqa(10631, 30, 58442583),
            Fqa(325, 11, -320),
            Fqa(1, 1, -1),
        ])

    def date_vers_jj(self, date):
        """Entrée : Une Date(a, m, j, t) représentant la date dans le calendrier.
        Sortie : le Jour julien correspondant.
        Erreur : Si le paramètre n'est pas une date.
        """
        # if not isinstance(date, Date):
        #    raise TypeError("Le paramètre n'est pas une Date")
        a_, m_ = _corr_am(date.u, date.v)
        d_, t_ = date.w, date.t
        n_ = super().__call__([a_, m_, d_])
        jj_ = JourJulien(n_, t_)
        return jj_

    def date(self, jj_):
        """Entrée : Un Jour julien.
        Sortie : La Date(a, m, j, t) représentant le Jour julien dans le calendrier.
        Erreur : Si le paramètre n'est pas un Jour julien.
        """
        assert isinstance(jj_, JourJulien)
        dt_ = super().inv(jj_.n)
        a_, m_, j_ = dt_[0], dt_[1], dt_[2]
        return Date(a_, m_, j_ + jj_.f, self)


CALENDRIER_ISL = _CalendrierIsl()


class _BaseTemps(Base):
    """Base temps [jour, heures, minutes, secondes]."""

    def __init__(self):
        super().__init__([
            Fqa(86400, 1, 0),
            Fqa(3600, 1, 0),
            Fqa(60, 1, 0),
            Fqa(1, 1, 0),
        ])


BASE_TEMPS = _BaseTemps()

if "__main__" == __name__:

    # 1721424.0
    # JUL0 = EPOQUE_JUL - EPOQUE_JJ

    # a, m, j = 1,3,1

    # JUL1MARS =  Date(a, m, j, CALENDRIER_JUL)()()
    # print("JUL0", JUL0, "JUL1MARS", JUL1MARS, JUL1MARS - JUL0)

    # jul = lambda a, m, j : int((365.25 * a) // 1) + int((30.6 * (m + 1)) // 1) + j + 1720994.5

    print("EPOQUE_JUL", EPOQUE_JUL(), "EPOQUE_JUL - EPOQUE_JD", EPOQUE_JUL - EPOQUE_JD,
          1720994.5 - (EPOQUE_JUL - EPOQUE_JD))
    # print("jul", jul(a, m, j), "JUL1MARS", JUL1MARS)

    # fa, fm, fj = Fqa(1461,4,6884472), Fqa(153,5,-457), Fqa(1,1,-1),
    # print("fa(a) - EPOQUE_JUL()",fa(a) - EPOQUE_JUL(), int((365.25 * (a - 1)) // 1))
    # print("fm(m)",fm(m), int((30.6 * (m + 1)) // 1) - 122)
    # print("fj(j)",fj(j), int(j-1))

    # fm = Fqa(a=153, b=5, r=-162)
    # print("fm(m)",fm(m), int((30.6 * (m + 1)) // 1) - 122)

    # print("fa(1)",fm(1))

    print()
    j = 1
    for i in range(5):
        print()
        a = i + 1
        m = 1
        dt0 = Date(a, m, j, CALENDRIER_JUL)
        print("a m j", a, m, j)
        print("dt0", dt0, dt0())
        u, v = _norm_am(a, m)
        print("a m j", u, v, j)

        print()
        m = 3
        dt = Date(a, m, j, CALENDRIER_JUL)
        print("a m j", a, m, j)
        print("dt", dt, dt())
        u, v = _norm_am(a, m)
        print("a m j", u, v, j)
        print("*** dt-dt0", dt() - dt0())
