# Formes quasi affines
"""
Bibliographie.
    [1] 'La saga des calendriers' (Jean LEFORT, Pour la Science, 1998).
    [2] 'Calendrical Calculations'.
    (Nachum Dershowitz et Edward M. Reingold, Cambridge University Press, 1997).
    [3] 'Droites discrètes et calendriers'
    (Albert TROESCH, Mathématiques et sciences humaines, tome 141, 1998, p. 11-41)
        disponible sur http://www.numdam.org/article/MSH_1998__141__11_0.pdf
    [4] 'Calculs astronomiques à l'usage des amateurs'
    (Jean MEEUS, Société Astronomique de France, Paris, 2014).
    [5] "Interprétation géométrique de l'algorithme d'Euclide et reconnaissance de segments"
    (Albert TROESCH, Theoretical Computer Science 115 (1993) 291-319)
        disponible sur https://www.sciencedirect.com/science/article/pii/0304397593901219
"""

# ATTENTION : La conversion systématique (et normalement silencieuse) des paramètres des fonctions
#             au types attendus est faite par parti-pris.

import array
from . import outils


def reconnaissance(liste_codes):
    """Reconnaissance des codes.
    Entrée : Une liste d'entiers (codes).
    Sortie : Les caractéristiques a, b, r de la forme quasi affine.
    Erreur : ValueError si les codes ne sont pas ceux d'un segment de droite discrète.
    Références [3] et [5].
    """
    def reduction(lc):
        # Algorithme décrit dans [3] et [5] : reconnaissance.
        p_ = min(lc)
        # transvection
        sc = "".join(
            map(lambda c_: {True: str, False: lambda c__: "*"}[c_ in [0, 1]](c_), list(map(lambda c__: c__ - p_, lc))))
        # En cas d'erreur, le dernier code peut être ignoré si c'est le plus petit
        # REMARQUE : len(lc) >= 2 obligatoirement car il y a au minimum un "0" et une "*".
        #            On peut donc retirer sans risque un élément si nécessaire.
        if "*" in sc and lc[-1] == p_:
            p_ = min(lc[:-1])
            sc = "".join(map(lambda c_: {True: str, False: lambda c__: "*"}[c_ in [0, 1]](c_),
                             list(map(lambda c_: c_ - p_, lc[:-1]))))
        if "*" in sc:
            raise ValueError("Liste de codes invalide")
        # complémentation (si "1" n'est pas le caractère isolé)
        complement_ = "11" in sc
        # caractère isolé
        ci = {True: "0", False: "1"}[complement_]
        # le palier terminal est complet (dp=0) s'il s'achève par le caractère isolé (sc[-1] == ci)
        dp = 0 if sc[-1] == ci else 1
        # symétrie (longueurs des paliers caractère isolé inclus)
        tl_ = [len(c_) + 1 for c_ in sc[:len(sc) - 1 + dp].split(ci)]
        # plus petit palier
        # REMARQUE : si le dernier palier est complet (dp=0) il faut le prendre en considération
        if 1 + dp < len(tl_):
            # plus petit palier interne incluant éventuellement le dernier s'il est complet (dp=0)
            mini = min(tl_[1:len(tl_) - dp])
        else:
            # sinon le plus petit palier externe
            mini = min(tl_)
        # translation
        g_ = 0
        # suppression du premier palier s'il est plus petit ou égal au mini
        if 1 < len(tl_) and tl_[0] <= mini:
            g_ = tl_[0]
            del tl_[0]
        # suppression du dernier palier s'il est plus petit ou égal au mini et s'il n'est pas complet (dp=1)
        if 1 < len(tl_) and tl_[-1] <= mini and 1 == dp:
            del tl_[-1]
        return tl_, p_, g_, complement_

    def restitution(a_, b_, r_, p_, g_, complement_):
        # Algorithme décrit dans [3] et [5] : restitution à rebours des paramètres a, b et r.
        ap, bp, rp = b_, a_, b_ - r_ - 1
        # translation
        if 0 < g_:
            rp -= ap * g_ - bp
            # rp = (rp - ap * g_) % bp
        # complémentation : x' = x ; y' = x - y
        if complement_:
            ap, bp, rp = bp - ap, bp, bp - rp - 1
        # transvection : x' = x ; y' = y - px
        ap, bp, rp = ap + p_ * bp, bp, rp
        return ap, bp, rp

    assert 0 < len(liste_codes)
    tl = array.array('l', liste_codes)
    # REMARQUE : le critère d'arrêt peut être différent, par exemple 'if 1 == len(tl):', mais ne donne pas toujours les
    # mêmes résultats bien que ceux obtenus restent conforment dans la mesure où ils représentent toujours le même
    # segment de droite discrète.
    # critère d'arrêt
    if min(tl) == max(tl):
        a, b, r = tl[0], 1, 0
    else:
        tl, p, g, complement = reduction(tl)
        # appels récursifs qui se terminent ci-dessus (critère d'arrêt).
        a, b, r = reconnaissance(tl)
        # les appels récursifs sont dépilés ici.
        a, b, r = restitution(a, b, r, p, g, complement)
    return a, b, r


def codes(liste_codes, x0_=0, y0_=0):
    """Reconnaissance des codes.
    Entrée : Une liste d'entiers (codes).
           : Les valeurs initiales x0_ et y0_ nulles par défaut.
    Sortie : La forme quasi affine correspondant aux codes et aux valeurs initiales fournies.
    Erreur : ValueError si les codes ne sont pas ceux d'un segment de droite discrète.
    Références : [3] et [5] pour les détails.
    """
    a, b, r = reconnaissance(liste_codes)
    r += b * int(y0_) - a * int(x0_)
    return Fqa(a=a, b=b, r=r)


class Fqa:
    """Forme quasi affine."""

    def __init__(self, a=0, b=1, r=0):
        """Forme quasi affine : y = Fqa(a,b,r)(x) = [(a * x + r) / b]
        Entrée : les caractéristiques a, b, r de la forme quasi affine.
        Sortie : La forme quasi affine Fqa.
        """
        self.a, self.b, self.r = int(a), int(b), int(r)

    def __call__(self, n_):
        """Entrée : un entier n.
        Sortie : Fqa(a,b,r)(n) = [(a * n + r) / b]
        """
        n_ = int(n_)
        q_, _ = outils.divent(self.a * n_ + self.r, self.b)
        return q_

    def __eq__(self, autre):
        if not isinstance(autre, Fqa):
            return False
        return self.a == autre.a and self.b == autre.b and self.r == autre.r

    def __repr__(self):
        return "Fqa(a={}, b={}, r={})".format(self.a, self.b, self.r)

    def __str__(self):
        return "[a={}, b={}, r={}]".format(self.a, self.b, self.r)

    def divfqa(self, n_):
        """divfqa est l'équivalent de la division entière de n par la forme quasi affine self.
            Entrée : Un nombre entier n.
            Sortie : Le "quotient" q ~ n // self et le "reste" r ~ (n % self).
        """
        n_ = int(n_)
        # equivalent (q = n // self).
        q_, _ = outils.divent(self.b * n_ + self.b - self.r - 1, self.a)
        # equivalent (r = n % self) = n - self * (n // self).
        r_ = n_ - self(q_)
        return q_, r_

    def inv(self):
        """Forme quasi affine inverse : x = Fqa(a,b,r).inv()(y) = [(b * y + b - r - 1) / a].
        Entrée : Aucun paramètre.
        Sortie : La forme quasi affine inverse.
        """
        return Fqa(self.b, self.a, self.b - self.r - 1)


class Base:
    """Classe Base définit une base pour représenter un nombre.
    De la même manière que nombre peut être représenté en base 10 ou 2.
    """

    def __init__(self, liste_fqa):
        """Entrée : Une liste de formes quasi affines liste_fqa.
        Sortie : Une base.
        Erreur : Si le paramètre liste_fqa n'est pas une liste de formes quasi affines.
        """
        assert isinstance(liste_fqa, list)
        self.t = []
        for value in liste_fqa:
            assert isinstance(value, Fqa)
            self.t.append(value)

    def __call__(self, liste_entiers):
        """Base([n0, n1, ...]) = [t[0](n0)+t[1](n1)+...].
        Entrée : Une liste d'entiers représentant un nombre entier dans la base.
        Sortie : Le nombre entier représenté par la liste dans la base.
        Erreur : Si le paramètre liste_entiers n'est pas une liste d'entiers.
                 Ou si le paramètre liste_entiers a trop d'éléments.
        """
        assert isinstance(liste_entiers, list)
        assert len(self.t) >= len(liste_entiers)
        # REMARQUE : si la taille de la liste d'entiers est inférieure à celle de self.t,
        #            ce sont les formes les plus significatives qui sont ignorées.
        tv = array.array('l', ([0] * (len(self.t) - len(liste_entiers)) + liste_entiers))
        i, n_ = 0, 0
        for value in tv:
            n_ += self.t[i](value)
            i += 1
        return n_

    def __eq__(self, autre):
        if not isinstance(autre, Base):
            return False
        return self.t == autre.t

    def __len__(self):
        return len(self.t)

    def __getitem__(self, clef):
        return self.t[clef]

    def __setitem__(self, clef, valeur):
        """Erreur : si la valeur n'est pas une forme quasi affine."""
        assert isinstance(valeur, Fqa)
        # assert isinstance(clef, int)
        self.t[clef] = valeur

    def __delitem__(self, clef):
        # assert isinstance(clef, int)
        del self.t[clef]

    def __iter__(self):
        return iter(self.t)

    def append(self, valeur):
        assert isinstance(valeur, Fqa)
        self.t.append(valeur)

    def __repr__(self):
        return "Base({})".format(self.t)

    def __str__(self):
        return "{}".format(self.t)

    def inv(self, n_):
        """Entrée : Un nombre entier.
        Sortie : Un tableau d'entiers représentant le nombre dans la base.
        Référence : [1] pour les détails.
        """
        # Erreur : Si le paramètre n'est pas un nombre entier.
        # assert isinstance(n_, int)
        v = [0] * len(self.t)
        i, r = 0, int(n_)
        for f_ in self.t:
            v[i], r = f_.divfqa(r)
            i += 1
        return v


class Representation:
    """Representation d'une Quantite dans une Base.
       Aucun traitement ni contrôle de cohérence n'est fait.
       ATTENTION : Une Representation doit nécessairement être associée à une Base
       afin de donner un sens à la liste de nombres qui la compose.
    """

    def __init__(self, base, liste_entiers):
        """Entrée : Le paramètre Base de la Représentation.
                    Le paramètre facultatif liste d'entiers de la représentation.
        Sortie : La Representation.
        Erreur : Si le paramètres base n'est pas une Base.
                 Si le paramètre liste_entiers n'est pas une liste.
                 Si la taille de la liste d'entiers est supérieure à celle de la base.
        """
        assert isinstance(base, Base)
        assert isinstance(liste_entiers, list)
        if len(liste_entiers) > len(base.t):
            raise ValueError("La taille de la liste d'entiers est supérieure à celle de la base")
        self.base = base
        self.liste_entiers = array.array('l', [])
        for valeur in liste_entiers:
            self.liste_entiers.append(valeur)

    def __eq__(self, autre):
        if not isinstance(autre, Representation):
            return False
        return self.base == autre.base and self.liste_entiers == autre.liste_entiers

    def __call__(self):
        """Representation() retourne le nom entier représenté."""
        return self.base(self.liste_entiers.tolist())

    def __repr__(self):
        # Le format d'une date peut (doit ?) dépendre de la base.
        return "Representation({}, {})".format(self.base, self.liste_entiers)

    def __str__(self):
        return "{}".format(self.liste_entiers)


BASE_TEMPS = Base([
            Fqa(86400, 1, 0),
            Fqa(3600, 1, 0),
            Fqa(60, 1, 0),
            Fqa(1, 1, 0),
        ])

if "__main__" == __name__:

    # RAPPELS : les codes si définis par : c(x) = f(x+1) - f(x)
    print("fqa")

    # print()
    # print("les années")
    # ca =[365, 365, 366, 365, 365, 365, 366, 365, 365, 365]
    # x0, y0 = 1, 59
    # print("x0", x0, "y0", y0, "ca", ca)
    # f = codes(x0=x0, y0=y0, liste_codes=ca)
    # fqa_annees = f
    # print("*** années juliennes", "ok", ok, "f", f, f.b * 1721424 + f.r)
    # print("ca", ca[x0:x0+5])
    # print("n", [f(x0+x+1) - f(x0+x) for x in range(4)])

    # print()
    # print("les mois")
    # cm = [31,30,31,30,31,31,30,31,30,31,31,28]
    # x0, y0 = 3 , 0
    # print("x0", x0, "y0", y0, "cm", cm)
    # f = codes(x0=x0, y0=y0, liste_codes=cm)
    # fqa_mois = f
    # print("*** mois", "ok", ok, "f", f)
    # REMARQUE : f(13) - f(12) donne un mois de février de 30 jours.
    # print("cm", cm[:12])
    # print("n", [f(x0+x+1) - f(x0+x) for x in range(12)])

    # print()
    # print("les jours")
    # cj = [1,1,1,1,1,1,1,1]
    # x0, y0 = 1, 0
    # print("x0", x0, "y0", y0, "cj", cj)
    # f = codes(x0=x0, y0=y0, liste_codes=cj)
    # fqa_jours = f
    # print("*** jours", "ok", ok, "f", f)
    # print("cj", cj[:4])
    # print("n", [f(x0+x+1) - f(x0+x) for x in range(2)])
    #
    # print()
    # cs = [36524, 36524, 36524, 36525, 36524, 36524, 36524, 36525]
    # x0, y0 = 0, 0
    # print("x0", x0, "y0", y0, "cs", cs)
    # f = codes(x0=x0, y0=y0, lst=cs)
    # print("*** siècles grégoriens", "ok", ok, "f", f)
    # print("cs", cs[:4])
    # print("n", [f(x0+x+1) - f(x0+x) for x in range(4)])

    # a, m, j = 1,3,1
    # jul = lambda a, m, j : (int((365.25 * a) // 1) + int((30.6 * (m + 1)) // 1) + j + 1720994.5)
    # print(jul(a,m,j))

    # print((365.25 * a) // 1)
    # print((30.6 * (m + 1)) // 1 )
    # print(j)

    def norm(a, m, j):
        k, m = outils.divent(m - 1, 12)
        m += 1
        a += k
        if 3 > m:
            return a - 1, m + 12, j
        else:
            return a, m, j


    def dnorm(a, m, j):
        k, m = outils.divent(m - 3, 12)
        m += 3
        a += k
        if 12 < m:
            return a + 1, m - 12, j
        else:
            return a, m, j


    # base = Base([fqa_annees, fqa_mois, fqa_jours])
    #
    # j = 1
    # for i in range(5):
    #    a = i + 1
    #    print()
    #    m = 1
    #    print("+++ a m j", a, m, j)
    #    u, v, w = norm(a, m, j)
    #    print("u v w", u, v, w)
    #    #if not i:
    #    #    print("codes annees[u:u+5]", ca[u:u+5])
    #    #    print("fa(u+n+1)-fa(u+n)", [fqa_annees(u+x+1) - fqa_annees(u+x) for x in range(4)])
    #    
    #    print("fqa_annees", fqa_annees, fqa_annees(u))
    #    print("fqa_mois", fqa_mois, fqa_mois(v))
    #    print("fqa_jours", fqa_jours, fqa_jours(w))
    #    
    #    n0 = base([u, v, w])
    #    #print("n0", n0)
    #    
    #    u, v, w = base.inv(n0)
    #    print("u, v, w", u, v, w)
    #    u, v, w = dnorm(u, v, w)
    #    print("u, v, w", u, v, w)
    #    
    #    print()
    #    m = 3
    #    print("a m j", a, m, j)
    #    u, v, w = norm(a, m, j)
    #    print("u v w", u, v, w)
    #    
    #    print("fqa_annees", fqa_annees, fqa_annees(u))
    #    print("fqa_mois", fqa_mois, fqa_mois(v))
    #    print("fqa_jours", fqa_jours, fqa_jours(w))
    #    
    #    n = base([u, v, w])
    #    
    #    u, v, w = base.inv(n)
    #    print("u, v, w", u, v, w)
    #    u, v, w = dnorm(u, v, w)
    #    print("u, v, w", u, v, w)
    #    
    #    print()
    #    print("*** a", a, "n0", n0, "n", n, "n-n0", n - n0)
    #    print("***", n0+1721424, n+1721424)
    #
    #
    # print()
    # print("les années")
    # ca =[365, 365, 366, 365, 365, 365, 366, 365, 365, 365]
    # x0, y0 = 1, 1721424+59
    # print("x0", x0, "y0", y0, "ca", ca)
    # f = codes(x0=x0, y0=y0, liste_codes=ca)
    # print("f", f)
    #
    # print("***")
    # x0, y0 = 1, 1721424+59
    # l=[366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365, 366, 365, 365, 365]
    # for k in range(5):
    #    print()
    #    c = l[k:k+8]
    #    print("c", c)
    #    f = codes(x0=0, y0=0, liste_codes=c)
    #    print("f", f)
    #    n = [f(i+1) - f(i) for i in range(8)]
    #    print("n", n)

    # x0, y0, c = 0, 0, [366, 365, 365, 365, 366, 365, 365, 365, ]
    # x0, y0, c = 0, 0, [365, 366, 365, 365, 365, 366, 365, 365, ]
    # x0, y0, c = 0, 0, [365, 365, 366, 365, 365, 365, 366, 365, ]
    # x0, y0, c = 0, 0, [365, 365, 365, 366, 365, 365, 365, 366, ]
    # x0, y0, c = 0, 0, [365, 365, 365, 366, ]
    # x0, y0, c = 0, 0, [31,30,31,30,31,31,30,31,30,31,31,28, ]
    # x0, y0, c = 0, 0, [3,2,3,3,3,2,3,3,2,3,3,3,2,3,3,3,2,3,3,2,3,3,]
    # x0, y0, c = 0, 0, [3,3,2,3,3,3,2,3,3,2,3,3,3,2,]
    # x0, y0, c = 0, 0, [36524, 36524, 36524, 36525, 36524, 36524, 36524, 36525, ]
    x0, y0, c = 0, 0, [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, ]
    # x0, y0, c = 0, 0, [1,1,1,0,]

    print("c", c)
    f = codes(x0_=x0, y0_=y0, liste_codes=c)
    print("f", f, len(c))
    n = [f(i + 1) - f(i) for i in range(len(c))]
    print("n", n)
    f = Fqa(8, 25, 7)
    print("f", f, repr(f))
    f1 = eval(repr(f))
    print(f1, f == f1, f1 is f)
    n = [f(i+1) - f(i) for i in range(len(c))]
    print("n", n)

    print("BASE_TEMPS", BASE_TEMPS, repr(BASE_TEMPS), )
    bt = eval(repr(BASE_TEMPS))
    print("bt",bt, bt == BASE_TEMPS, bt is BASE_TEMPS)
    
