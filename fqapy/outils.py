# Outils
"""Fonctions utiles."""

# Précision par défaut des comparaisons entre flottants
_PRECISION = 1e-15


def egalf(a, b, prec=_PRECISION):
    """Vérification de l'égalité de a et b à la précision prec près.
    Entrée : Deux nombres flottants a et b et facultativement la précision prec.
    Sortie : True si les deux nombres sont égaux à la précision près,
             False sinon.
    Erreur : Dès que l'un des deux nombres ou la précision n'est pas un flottant
             ou encore si la précision n'est pas strictement positive.
    """
    if not isinstance(a, float):
        raise TypeError("Le paramètre a n'est pas un flottant")
    if not isinstance(b, float):
        raise TypeError("Le paramètre b n'est pas un flottant")
    if not isinstance(prec, float):
        raise TypeError("Le paramètre prec n'est pas un flottant")
    if 0. > prec:
        raise ValueError("Précision négative ou nulle invalide")
    c = b - a
    return -prec < c < prec


def divent(n, d):
    """Division entière du numérateur n par le dénominateur d.
    Entrée : Deux nombres entiers n et d.
    Sortie : Le quotient q et le reste r tels que : n=q*d+r.
             Le reste r vérifie : 0 <= r < |d|.
    Erreur : Si le dénominateur d est nul.
    REMARQUE : La fonction standard divmod ne donne pas les mêmes 
               résultats lorsque le dénominateur est négatif 
               (le reste r est est alors négatif).
               Toutefois divmod, comme l'opérateur %, donnent des 
               résultats conforment à ceux définis dans [2] p. 15.
    ATTENTION : la fonction divmod retourne des flottants 
                dés que l'un des paramètres est un flottant.
    """
    #          divmod(9,5) = (1, 4)
    #          divmod(-9,5) = (-2, 1)
    #          divmod(9,-5) = (-2, -1)
    #          divmod(-9,-5) = (1, -4)
    #          9 % 5 = 4
    #          -9 % 5 = 1
    #          9 % -5 = -1
    #          -9 % -5 = -4
    #          9.0 % 5.0 = 4.0
    #          -9.0 % 5.0 = 1.0
    #          9.0 % -5.0 = -1.0
    #          -9.0 % -5.0 = -4.0
    #          divmod(0.9,0.5) = (1.0, 0.4)
    #          divmod(-0.9,0.5) = (-2.0, 0.09999999999999998)
    #          divmod(0.9,-0.5) = (-2.0, -0.09999999999999998)
    #          divmod(-0.9,-0.5) = (1.0, -0.4)
    #          0.9 % 0.5 = 0.4
    #          -0.9 % 0.5 = 0.09999999999999998
    #          0.9 % -0.5 = -0.09999999999999998
    #          -0.9 % -0.5 = -0.4
    # if not isinstance(n, int):
    #    raise TypeError("Le numérateur n n'est pas un entier")
    # if not isinstance(d, int):
    #    raise TypeError("Le dénominateur d n'est pas un entier")
    n, d = int(n), int(d)
    if 0 == d:
        raise ValueError("Le dénominateur d est nul")
    q, r = n // d, n % d
    # corriger le résultat si le reste r est négatif
    if 0 > r:
        if 0 < d:
            q -= 1
            r += d
        else:
            q += 1
            r -= d
    return q, r


def ent(f, sup=False):
    """Partie entière de f.
    Entrée : Un nombre flottant ou entier f.
             Si sup = False alors la partie entière est inférieure ou égale à f et 0 <= r < 1.
             Si sup = True alors la partie entière est supérieure ou égale à f et 0 >= r > -1.
    Sortie : Le plus grand entier q inférieur ou égal à f 
             et la partie fractionnaire r tels que f = q + r.
             La partie fractionnaire r vérifie : 0.0 <= r < 1.0.
    REMARQUE : Si q, r = divent(n, d) et si e, f = ent(n / d)
               alors q = e et r = int(f * d) aux erreurs d'arrondi près.
               D'autre part, ent(f) = divmod(f, 1) sauf éventuellement pour le 
               quotient retourné par divmod qui peut être un flottant 
               si f l'est, alors que ent renvoie toujours un entier.
    """
    if isinstance(f, int):
        return f, 0.0
    # if not isinstance(f, float):
    #    raise TypeError("Le paramètre f n'est pas un flottant")
    f = float(f)
    q = int(f)
    r = f - q
    # par défaut sup = False : donc partie entière <= f et r >= 0
    if 0. > r:
        q -= 1
        r += 1.0
    # corriger si sup = True : donc partie entière >= f et r <= 0
    if 0. < r and sup:
        q += 1
        r -= 1.0
    return q, r


def pgcd(a, b):
    """PGCD plus grand commun diviseur des deux nombres a et b.
    Entrée : Deux nombres entiers a et b
    Sortie : Le PGCD.
    """
    # if not isinstance(a, int):
    #    raise TypeError("Le paramètre a n'est pas un entier")
    # if not isinstance(b, int):
    #    raise TypeError("Le paramètre b n'est pas un entier")
    a, b = int(a), int(b)
    while b:
        a, b = b, a % b
    return a


def pgcde(a, b):
    """PGCD étendu des deux nombres entiers a et b.
    Entrée : Deux nombres entiers a et b.
    Sortie : Le triplet PGCD, u ,v tels que u * a + v * b = PGCD.
    Référence : https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu
    REMARQUE : Si et seulement si a et b sont premiers entre eux PGCD = 1.
               Donc u * a = (-v) * b + 1, c'est-à-dire que (u * a) % b = 1.
               u est donc l'inverse de a modulo b.
    REMARQUE : Si u * a + v * b = PGCD alors 
               u * (a // PGCD) + v * (b // PGCD) = 1
               donc (a // PGCD) et (b // PGCD) sont premiers entre eux
               et u est l'inverse de (a // PGCD) modulo (b // PGCD).
               Voir [2] pp. 20, 21.
    """
    # if not isinstance(a, int):
    #    raise TypeError("Le paramètre a n'est pas un entier")
    # if not isinstance(b, int):
    #    raise TypeError("Le paramètre b n'est pas un entier")
    a, b = int(a), int(b)
    r, u, v, rp, up, vp = a, 1, 0, b, 0, 1
    while rp:
        q = r // rp
        r, u, v, rp, up, vp = rp, up, vp, r - q * rp, u - q * up, v - q * vp
    return r, u, v


def ppcm(a, b):
    """PPCM plus petit commun multiple des deux nombres a et b.
    Entrée : Deux nombres entiers a et b.
    Sortie : Le PPCM.
    Référence : https://fr.wikipedia.org/wiki/Plus_petit_commun_multiple
    """
    # if not isinstance(a, int):
    #    raise TypeError("Le paramètre a n'est pas un entier")
    # if not isinstance(b, int):
    #    raise TypeError("Le paramètre b n'est pas un entier")
    a, b = int(a), int(b)
    if 0 == a or 0 == b:
        return 0
    else:
        return (a * b) // pgcd(a, b)
