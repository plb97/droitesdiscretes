# Calendar
from . import outils

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

Implémentation EXPÉRIMENTALE des calendriers définis dans [2].
Aucun contrôle de type n'est fait.

REMARQUE : 'date' signifie (généralement) jour julien (c-à-d un nombre flottant).
          'fixed' désigne (généralement) ce type de date.
          Dans [2] une distinction est faite entre 'date' et 'moment', 'date' = ['moment'],
          dans ce qui suit cette distinction n'est pas explicite mais est faite systématiquement
          lorsque c'est nécessaire dans les calculs : 'date', 'time' = ent('moment').
"""


def day_of_week_from_fixed(date):
    """Jour de la semaine de la date (la semaine commence le lundi).
    Entrée : Un jour julien date.
    Sortie : Un jour de la semaine (0 = lundi).
    Référence : [2] p. 17.
    """
    return date % 7


def signum(y):
    """Signe d'un nombre.
    Entrée : Un nombre y.
    Sortie : +1 si y > 0, -1 si y < 0 et 0 sinon.
    Référence : [2] p. 15.
    """
    return -1 if 0 > y else 1 if 0 < y else 0


def amod(x, y):
    """Reste ajusté de la division de x par y.
    Entrée : Un nombre y.
    Sortie : y si x % y == 0.
             x % y sinon.
    Référence : [2] p. 15.
    """
    z = x % y
    return z if z else y


def kday_on_or_before(date, k):
    """Date du k qui précède la date ou elle-même si cette date est un k.
    Entrée : paramètre date en jour julien
             paramètre k en jour de la semaine (0 = lundi, ..., 6 = dimanche).
    Sortie : le jour julien recherché.
    Référence : [2] (1.22) p. 17.
    """
    k = int(k) % 7
    return date - (date - k) % 7


def kday_on_or_after(date, k):
    """Référence : [2] (1.27) p. 19."""
    return kday_on_or_before(date + 6, k)


def kday_nearest(date, k):
    """Référence : [2] (1.28) p. 19."""
    return kday_on_or_before(date + 3, k)


def kday_after(date, k):
    """Référence : [2] (1.29) p. 19."""
    return kday_on_or_before(date + 7, k)


def kday_before(date, k):
    """Référence : [2] (1.30) p. 19."""
    return kday_on_or_before(date - 1, k)


def label_of_day(n, c, d, gamma=0, delta=0):
    """Entrée : Le "day number" n.
                La durée du "first cycle" c.
                La durée du "second cycle" d  (c < d < 2d).
                Le label gamma du "day 0" du premier cycle (de durée c).
                Le label delta du "day 0" du second cycle (de durée d).
    Sortie : Le label (a, b) du "day n"
    Référence : [2] (1.31) p. 19.
    """
    return (n + gamma) % c, (n + delta) % d


def day_number_of_label(a, b, c, d, gamma=0, delta=0):
    """Entrée : Le label (a, b).
                La durée du "first cycle" c.
                La durée du "second cycle" d  (c < d < 2d).
                Le label gamma du "day 0" du premier cycle (de durée c).
                Le label delta du "day 0" du second cycle (de durée d).
    Sortie : Le "day number" du label (a, b).
    Référence : [2] (1.33) p. 20.
    """
    gcd, k, _ = outils.pgcd(c, d)
    lcm = c * d // gcd
    return (a - gamma + (c * (b - a + gamma - delta) % d) // gcd) % lcm


def number_of_days_in_the_year_prior_year(y, l, c, L, delta=0):
    """Entrée : Le "year number" y.
                Le "number of leap years in the cycle c" l.
                La durée du "cycle" c.
                La durée d'une année ordinaire L.
                La position dans le cycle de l'année 0 delta.
        Sortie : Le nombre de jours de l'année précédant y.
    Référence : [2] (1.39) p. 24.
    """
    return (l * y - l + (delta * l) % c) // c + L * (y - 1)


def year_at_day(n, l, c, L, delta=0):
    """Entrée : Le "day number" n.
                Le "number of leap years in the cycle c" l.
                La durée du "cycle" c.
                La durée d'une année ordinaire L.
                La position dans le cycle de l'année 0 delta.
    Sortie : l'année du "day n".
    Référence : [2] (1.43) p. 25.
    """
    return (c * n + c * L + l - 1 + c - (l * delta) % c) // (c * L + l)


# Définition des constantes compatibles avec le module .calendrier.
#
# Référence [2] (1.13-1.19) p. 17.
# ATTENTION : CONTRAIREMENT À LA REFERENCE CITÉE CI-DESSUS LA SEMAINE
# COMMENCE LE LUNDI ET NON PAS LE DIMANCHE (LE JOUR JULIEN 0 EST UN LUNDI).
_MONDAY = 0
_TUESDAY = 1
_WEDNESDAY = 2
_THURSDAY = 3
_FRIDAY = 4
_SATURDAY = 5
_SUNDAY = 6
#
# Formellement _GREGORIAN_EPOCH = .calendrier.EPOQUE_GRE - .calendrier.EPOQUE_JJ
_GREGORIAN_EPOCH = 1721426
#
# Référence : [2] (2.4-2.13) pp. 35-36.
_JANUARY = 1
_FEBRUARY = _JANUARY + 1
_MARCH = _JANUARY + 2
_APRIL = _JANUARY + 3
_MAY = _JANUARY + 4
_JUNE = _JANUARY + 5
_JULY = _JANUARY + 6
_AUGUST = _JANUARY + 7
_SEPTEMBER = _JANUARY + 8
_OCTOBER = _JANUARY + 9
_NOVEMBER = _JANUARY + 10
_DECEMBER = _JANUARY + 11
#
# Référence : [2] (2.25-2.26) p. 40.
_FIRST = 1
_LAST = -1


# GREGORIAN CALENDAR

class GDate:
    """Référence [2] pp. 33-41"""

    def __init__(self, month, day, year, time=0.0):
        self.month = int(month)
        self.day, self.time = outils.ent(float(day + time))
        self.year = int(year)

    def __eq__(self, other):
        if not isinstance(other, GDate):
            return False
        else:
            return (self.month == other.month and self.day == other.day and self.year == other.year
                    and self.time == other.time)

    def __repr__(self):
        return "GDate({}, {}, {}, {})".format(self.month, self.day, self.year, self.time)

    def __str__(self):
        return "[Gregorian: month={}, day={}, year={}, time={}]".format(self.month, self.day, self.year, self.time)


def gregorian_leap_year(g_year):
    """Détermine si l'année grégorienne g_year est bissextile.
    Entrée : Une année du calendrier grégorien.
    Sortie : True si l'année g_year est bissextile
             False sinon.
    Référence : [2] (2.16) p.36.
    """
    gym4 = g_year % 4
    return gym4 == 0 and not gym4 in [100, 200, 300]


def _gregorian_day_adjust(g_year, month):
    """Référence : [2] (2.17) p.36."""
    return 0 if month <= 2 else -1 if month > 2 and gregorian_leap_year(g_year) else -2


def fixed_from_gregorian(g_date):
    """Calcule le jour julien sous la forme d'un nombre flottant.
    Entrée : Une GDate [month, day, year].
    Sortie : Un nombre flottant représentant le jour julien de la date.
    Référence : [2] (2.17) p.36.
    REMARQUE : le jour julien est cohérent avec le Jour julien calculé avec
               le calendrier grégorien CALENDRIER_GRE.
    """
    return (_GREGORIAN_EPOCH - 1 + 365 * (g_date.year - 1)
            + (g_date.year - 1) // 4 - (g_date.year - 1) // 100 + (g_date.year - 1) // 400
            + (367 * g_date.month - 362) // 12
            + _gregorian_day_adjust(g_date.year, g_date.month) + g_date.day) + g_date.time


def gregorian_year_from_fixed(date):
    """Calcule l'année grégorienne du jour julien date.
    Entrée : Un jour julien (nombre flottant).
    Sortie : L'année grégorienne correspondant au jour julien date.
    Référence : [2] (2.18) p.37.
    """
    d0, _ = outils.ent(date - _GREGORIAN_EPOCH)
    n400, d1 = d0 // 146097, d0 % 146097
    n100, d2 = d1 // 36524, d1 % 36524
    n4, d3 = d2 // 1461, d2 % 1461
    n1, d4 = d3 // 365, d3 % 365
    return 400 * n400 + 100 * n100 + 4 * n4 + n1 + (0 if n100 == 4 or n1 == 4 else 1)


def gregorian_from_fixed(date):
    """Calcule le mois, je jour et l'année grégorienne du jour julien date.
    Entrée : Un jour julien (nombre flottant).
    Sortie : Le mois, le jour et l'année grégorienne correspondant au jour julien date.
    Référence : [2] (2.19) p.38.
    """
    date, time = outils.ent(date)
    year = gregorian_year_from_fixed(date)
    prior_days = date - fixed_from_gregorian(GDate(_JANUARY, 1, year))
    march1 = fixed_from_gregorian(GDate(_MARCH, 1, year))
    correction = (0 if date < march1 else 
                  1 if date >= march1 and gregorian_leap_year(year) else 
                  2)
    month = (12 * (prior_days + correction) + 373) // 367
    day = date - fixed_from_gregorian(GDate(month, 1, year)) + 1
    return GDate(month, day, year, time)


def gregorian_date_difference(g_date_1, g_date_2):
    """Calcule le nombre des jours entre les dates g_date_2 et g_date_1.
    Entrée : Une première date grégorienne g_date_1.
             Une deuxième date grégorienne g_date_2.
    Sortie : Le nombre de jours = g_date_2 - g_date_1.
    Référence : [2] (2.20) p.38.
    """
    return fixed_from_gregorian(g_date_2) - fixed_from_gregorian(g_date_1)


def day_number(g_date):
    """Calcule le numéro du jour de la date.
    Entrée : Une date grégorienne g_date.
    Sortie : Le numéro du jour.
    Référence : [2] (2.21) p.39.
    """
    return gregorian_date_difference(GDate(_DECEMBER, 31, g_date.year - 1), g_date)


def days_remaining(g_date):
    """Calcule le nombre de jours restant à partir de la date.
    Entrée : Une date grégorienne g_date.
    Sortie : Le nombre du jours restant.
    Référence : [2] (2.22) p.39.
    """
    return gregorian_date_difference(g_date, GDate(_DECEMBER, 31, g_date.year))


def independence_day(g_year):
    """Calcule le jour julien de l'"independence day" de l'année year.
    Entrée : Une année grégorienne.
    Sortie : Le jour julien de l'"independence day".
    Référence : [2] (2.23) p.39.
    """
    return fixed_from_gregorian(GDate(_JULY, 4, g_year))


def nth_kday(n, k, g_date):
    """Calcule le nième kday (jour de la semaine) à partir d'une date g_date.
    Entrée : Un nombre de jours de la semaine (peut être négatif pour signifier précédents).
             Un jour de la semaine.
             Une date grégorienne.
    Sortie : Le jour julien recherché.
    Référence : [2] (2.24) p.40.
    """
    return (7 * n + kday_before(fixed_from_gregorian(g_date), k) if n > 0 else 
            7 * n + kday_after(fixed_from_gregorian(g_date), k))


def labor_day(g_year):
    """Calcule le "labor day" (USA).
    Entrée : Une année grégorienne.
    Sortie : Le jour julien du "labor day" de l'année g_date.
    Référence : [2] (2.27) p. 40.
    """
    return nth_kday(_FIRST, _MONDAY, GDate(_SEPTEMBER, 1, g_year))


def memorial_day(g_year):
    """Calcule le "memorial day" (USA).
    Entrée : Une année grégorienne.
    Sortie : Le jour julien du "memorial day" de l'année g_date.
    Référence : [2] (2.28) p. 40.
    """
    return nth_kday(_LAST, _MONDAY, GDate(_MAY, 31, g_year))


def election_day(g_year):
    """Calcule l'"election day" (USA).
    Entrée : Une année grégorienne.
    Sortie : Le jour julien de l'"election day" de l'année g_date.
    Référence : [2] (2.29) p. 40.
    """
    return nth_kday(_FIRST, _TUESDAY, GDate(_NOVEMBER, 2, g_year))


def daylight_saving_start(g_year):
    """Calcule jour du début de l'heure d'été (USA).
    Entrée : Une année grégorienne.
    Sortie : Le jour julien du début de l'heure d'été de l'année g_date.
    Référence : [2] (2.30) p. 40.
    """
    return nth_kday(_FIRST, _SUNDAY, GDate(_APRIL, 1, g_year))


def daylight_saving_end(g_year):
    """Calcule jour du la fin de l'heure d'été (USA).
    Entrée : Une année grégorienne.
    Sortie : Le jour julien de la fin de l'heure d'été de l'année g_date.
    Référence : [2] (2.31) p. 40.
    """
    return nth_kday(_LAST, _SUNDAY, GDate(_OCTOBER, 31, g_year))


def christmas(g_year):
    """Entrée : Une année grégorienne.
    Sortie : Le jour julien de noël de l'année g_date.
    Référence : [2] (2.32) p. 41.
    """
    return fixed_from_gregorian(GDate(_DECEMBER, 25, g_year))


def advent(g_year):
    """Entrée : Une année grégorienne.
    Sortie : Le jour julien de l'"advent" (USA) de l'année g_date.
    Référence : [2] (2.33) p. 41.
    """
    return kday_nearest(fixed_from_gregorian(GDate(_NOVEMBER, 30, g_year)), _SUNDAY)


def epiphany(g_year):
    """Entrée : Une année grégorienne.
    Sortie : Le jour julien de l'"advent" (USA) de l'année g_date.
    Référence : [2] (2.33) p. 41.
    """
    return 12 + christmas(g_year - 1)


def assumption(g_year):
    """Entrée : Une année grégorienne.
    Sortie : Le jour julien l'"assumption" de l'année g_date.
    Référence : [2] p. 41.
    """
    return fixed_from_gregorian(GDate(_AUGUST, 15, g_year))


# ISO CALENDAR

class ISODate:
    """Référence [2] pp. 43-44"""

    def __init__(self, week, day, year, time=0.0):
        """
        Référence : [2] p. 33.
        """
        self.week = int(week)
        self.day, self.time = outils.ent(float(day + time))
        self.year = int(year)

    def __eq__(self, other):
        if not isinstance(other, ISODate):
            return False
        else:
            return (self.week == other.week and self.day == other.day and self.year == other.year
                    and self.time == other.time)

    def __repr__(self):
        return "ISODate({}, {}, {}, {})".format(self.week, self.day, self.year, self.time)

    def __str__(self):
        return "[ISO: week={}, day={}, year={}, time={}]".format(self.week, self.day, self.year, self.time)


def fixed_from_iso(iso_date):
    """Entrée : Une date ISO (week, day, year).
    Sortie : Le jour julien correspondant.
    Référence : [2] (3.1) p. 43.
    """
    return (nth_kday(iso_date.week, _SUNDAY, GDate(_DECEMBER, 28, iso_date.year - 1))
            + iso_date.day + iso_date.time)


def iso_from_fixed(date):
    """
    Entrée : Un jour julien date.
    Sortie : La date ISO correspondante.
    Référence : [2] (3.2) p. 43.
    """
    date, time = outils.ent(date)
    approx = gregorian_year_from_fixed(date - 3)
    year = approx + (1 if date >= fixed_from_iso(ISODate(1, 1, approx + 1)) else 0)
    week = (date - fixed_from_iso(ISODate(1, 1, year))) // 7 + 1
    # day = amod(date, 7)
    # Pour tenir compte que la semaine débute le lundi (et pas le dimanche comme dans [2])
    day = date % 7 + 1
    return ISODate(week, day, year, time)


# JULIAN CALENDAR
# Référence [2] pp. 47-55.
#
# Définition des constantes compatibles avec le module .calendrier
# du moins pour les années positives (année 1 -> 1CE, année 0 -> 1BCE = -1)
# Formellement _JULIAN_EPOCH = .calendrier.EPOQUE_JUL - .calendrier.EPOQUE_JJ
# Référence : [2] (4.2) p. 48.
_JULIAN_EPOCH = 1721424


#
class JDate:
    """Référence [2] pp. 47-55."""

    def __init__(self, month, day, year, time=0.0):
        self.month = int(month)
        self.day, self.time = outils.ent(float(day + time))
        self.year = int(year)

    def __eq__(self, other):
        if not isinstance(other, JDate):
            return False
        else:
            return (self.month == other.month and self.day == other.day and self.year == other.year
                    and self.time == other.time)

    def __repr__(self):
        return "JDate({}, {}, {}, {})".format(self.month, self.day, self.year, self.time)

    def __str__(self):
        if self.year < 0:
            return "[Julian: month={}, day={}, year={} B.C.E., time={}]".format(self.month, self.day, -self.year, self.time)
        else:
            return "[Julian: month={}, day={}, year={} C.E., time={}]".format(self.month, self.day, self.year, self.time)


def julian_leap_year(j_year):
    """Détermine si l'année j_year est bissextile dans le calendrier Julien.
    Entrée : Une année julienne.
    Sortie : True si l'année est bissextile dans le calendrier Julien.
             False sinon.
    Référence [2] (4.1) p. 47.
    """
    return j_year % 4 == (0 if j_year > 0 else 3)


def _julian_day_adjust(j_year, month):
    """Référence : [2] (2.17) p.36."""
    return 0 if month <= 2 else -1 if month > 2 and julian_leap_year(j_year) else -2

def fixed_from_julian(j_date):
    """Calcule le jour julien sous la forme d'un nombre flottant.
    Entrée : Une JDate [month, day, year].
    Sortie : Un nombre flottant représentant le jour julien de la date.
    Référence : [2] (4.3) p.48.
    REMARQUE : le jour julien est cohérent avec le Jour julien calculé avec
               le calendrier julien CALENDRIER_JUL.
    """
    y = j_date.year + (1 if j_date.year < 0 else 0)
    return (_JULIAN_EPOCH - 1 + 365 * (y - 1) + (y - 1) // 4
            + (367 * j_date.month - 362) // 12
            + _julian_day_adjust(j_date.year, j_date.month) + j_date.day) + j_date.time


def julian_from_fixed(date):
    """Calcule le mois, le jour et l'année Julienne du jour julien date.
    Entrée : Un jour julien (nombre flottant).
    Sortie : Le mois, le jour et l'année Julienne correspondant au jour julien date.
    Référence : [2] (4.4) p.48.
    """
    date, time = outils.ent(date)
    approx = (4 * (date - _JULIAN_EPOCH) + 1464) // 1461
    year = approx - (1 if approx <= 0 else 0)
    prior_days = date - fixed_from_julian(JDate(_JANUARY, 1, year))
    march1 = fixed_from_julian(JDate(_MARCH, 1, year))
    correction = (0 if date < march1 else 
                  1 if date >= march1 and julian_leap_year(year) else 
                  2)
    month = (12 * (prior_days + correction) + 373) // 367
    day = date - fixed_from_julian(JDate(month, 1, year)) + 1
    return JDate(month, day, year, time)


def julian_in_gregorian(j_month, j_day, g_year):
    """
    Entrée : Un mois julien.
             Un jour julien.
             Une année grégorienne.
    Sortie:  La liste des jour juliens correspondants.
             Cette liste peut contenir 0, 1 ou 2 dates.
    Référence : [2] (4.5) p. 50.
    """
    jan1 = fixed_from_gregorian(GDate(_JANUARY, 1, g_year))
    dec31 = fixed_from_gregorian(GDate(_DECEMBER, 31, g_year))
    y = julian_from_fixed(jan1).year
    date1 = fixed_from_julian(JDate(j_month, j_day, y))
    date2 = fixed_from_julian(JDate(j_month, j_day, y + 1))
    lst = [date1] if jan1 <= date1 <= dec31 else []
    lst += [date2] if jan1 <= date2 <= dec31 else []
    return lst


def eastern_orthodox_christmas(g_year):
    """
    Entrée : Une année grégorienne.
    Sortie : La liste les jour juliens des "eastern orthodox christmas" 
             de l'année grégorienne concernée.
             Cette liste peut contenir 0, 1 ou 2 dates.
    Référence : [2] (4.6) p. 50.
    """
    return julian_in_gregorian(_DECEMBER, 25, g_year)


def nicaean_rule_easter(j_year):
    """
    Entrée : Une année julienne.
    Sortie : Le jour julien correspondant à la date de Pâques dans le calendrier julien.
    Référence : [2] (4.7) p. 52.
    """
    shifted_epact = (14 + 11 * (j_year % 19)) % 30
    paschal_moon = fixed_from_julian(JDate(_APRIL, 19, j_year)) - shifted_epact
    return kday_after(paschal_moon, _SUNDAY)


def easter(g_year):
    """
    Entrée : Une année grégorienne.
    Sortie : Le jour julien  correspondant à la date de Pâques dans le calendrier grégorien.
    Référence [2] (4.8) pp. 53-54.
    """
    century = g_year // 100 + 1
    shifted_epact = (14 + 11 * (g_year % 19) - (3 * century) // 4 + (5 + 8 * century) // 25) % 30
    adjusted_epact = shifted_epact + (1 if (shifted_epact == 0 or (shifted_epact == 1 and 10 < (g_year % 19))) else 0)
    paschal_moon = fixed_from_gregorian(GDate(_APRIL, 19, g_year)) - adjusted_epact
    return kday_after(paschal_moon, _SUNDAY)


def pentecost(g_year):
    """
    Entrée : Une année grégorienne.
    Sortie : Le jour julien correspondant à la date de la Pentecôte dans le calendrier grégorien.
    Référence [2] (4.9) pp. 55.
    """
    return easter(g_year) + 49


# COPTIC CALENDAR
# Référence [2] pp. 57-58.
# Définition des constantes compatibles avec le module .calendrier
#
# Formellement _COPTIC_EPOCH = .calendrier.EPOQUE_COP - .calendrier.EPOQUE_JJ
# Référence : [2] (5.1) p. 58.
_COPTIC_EPOCH = 1825030

_TUT = 1
_BABAH = 2
_HATUR = 3
_KIYAHK = 4
_TUBAH = 5
_AMSHIR = 6
_BARAMHAT = 7
_BARAMUNDAH = 8
_BASHANS = 9
_BA_UNAH = 10
_ABIB = 11
_MISRA = 12
_AL_NASI = 13


class CDate:
    """Référence [2] pp. 37-55."""

    def __init__(self, month, day, year, time=0.0):
        self.month = int(month)
        self.day, self.time = outils.ent(float(day + time))
        self.year = int(year)

    def __eq__(self, other):
        if not isinstance(other, JDate):
            return False
        else:
            return (self.month == other.month and self.day == other.day and self.year == other.year
                    and self.time == other.time)

    def __repr__(self):
        return "CDate({}, {}, {}, {})".format(self.month, self.day, self.year, self.time)

    def __str__(self):
        return "[Coptic: month={}, day={}, year={}, time={}]".format(self.month, self.day, self.year, self.time)


def coptic_leap_year(c_year):
    """
    Référence : [2] (5.2) p. 58.
    """
    return (c_year % 4) == 3


def fixed_from_coptic(c_date):
    """Entrée : Une date du calendrier copte c_date.
    Sortie : Le jour julien correspondant.
    Référence : [2] (5.3) p. 58.
    """
    return (_COPTIC_EPOCH - 1 + 365 * (c_date.year - 1) + c_date.year // 4
            + 30 * (c_date.month - 1) + c_date.day + c_date.time)


def coptic_from_fixed(date):
    """Entrée : Un jour julien.
    Sortie : La date copte CDate correspondante.
    Référence : [2] (5.4) p. 58.
    """
    date, time = outils.ent(date)
    year = (4 * (date - _COPTIC_EPOCH) + 1463) // 1461
    month = (date - fixed_from_coptic(CDate(1, 1, year))) // 30 + 1
    day = date + 1 - fixed_from_coptic(CDate(month, 1, year))
    return CDate(month, day, year, time)


# ETHIOPIC CALENDAR
# Référence [2] pp. 59-60.
# Définition des constantes compatibles avec le module .calendrier
#
# Formellement _ETHIOPIC_EPOCH = .calendrier.EPOQUE_ETH - .calendrier.EPOQUE_JJ
# Référence : [2] (5.5) p. 59.
_ETHIOPIC_EPOCH = 1723855


#
class EDate:
    """Référence [2] pp. 59-60."""

    def __init__(self, month, day, year, time=0.0):
        self.month = int(month)
        self.day, self.time = outils.ent(float(day + time))
        self.year = int(year)

    def __eq__(self, other):
        if not isinstance(other, JDate):
            return False
        else:
            return (self.month == other.month and self.day == other.day and self.year == other.year
                    and self.time == other.time)

    def __repr__(self):
        return "EDate({}, {}, {}, {})".format(self.month, self.day, self.year, self.time)

    def __str__(self):
        return "[Ethiopic: month={}, day={}, year={}, time={}]".format(self.month, self.day, self.year, self.time)


_MASKARAM = 1
_TEQEMT = 2
_KHEDAR = 3
_TAKHSAS = 4
_TER = 5
_YAKATIT = 6
_MAGABIT = 7
_MIYAZYA = 8
_GENBOT = 9
_SANE = 10
_HAMLE = 11
_NAHASE = 12
_PAGUEMEN = 13


def fixed_from_ethiopic(e_date):
    """
    Entrée : Une date du calendrier éthiopien e_date.
    Sortie : Le jour julien correspondant.
    Référence [2] (5.6) p. 59.
    """
    # REMARQUE : transtypage pour la forme.
    c_date = CDate(e_date.month, e_date.day + e_date.time, e_date.year)
    return _ETHIOPIC_EPOCH + fixed_from_coptic(c_date) - _COPTIC_EPOCH


def ethiopic_from_fixed(date):
    """
    Entrée : Un jour julien.
    Sortie : La date du calendrier éthiopien correspondante.
    Référence [2] (5.7) p. 59.
    """
    c_date = coptic_from_fixed(date + _COPTIC_EPOCH - _ETHIOPIC_EPOCH)
    return EDate(c_date.month, c_date.day, c_date.year, c_date.time)


def coptic_in_gregorian(c_month, c_day, g_year):
    """Entrée : Un mois du calendrier copte.
                Un jour du calendrier copte.
                Une année du calendrier grégorien.
    Sortie:  La liste des jour juliens correspondants.
             Cette liste peut contenir 0, 1 ou 2 dates.
    Référence [2] (5.8) p. 60.
    """
    jan1 = fixed_from_gregorian(GDate(_JANUARY, 1, g_year))
    dec31 = fixed_from_gregorian(GDate(_DECEMBER, 31, g_year))
    y = coptic_from_fixed(jan1).year
    date1 = fixed_from_coptic(CDate(c_month, c_day, y))
    date2 = fixed_from_coptic(CDate(c_month, c_day, y + 1))
    lst = [date1] if jan1 <= date1 <= dec31 else []
    lst += [date2] if jan1 <= date2 <= dec31 else []
    return lst


def coptic_christmas(g_year):
    """
    Entrée : Une année grégorienne.
    Sortie : La liste les jour juliens des "coptic christmas" 
             de l'année grégorienne concernée.
             Cette liste peut contenir 0, 1 ou 2 dates.
    Référence [2] (5.9) p. 60.
    """
    return coptic_in_gregorian(4, 29, g_year)


def ethiopic_in_gregorian(e_month, e_day, g_year):
    """Entrée : Un mois du calendrier éthiopien.
                Un jour du calendrier éthiopien.
                Une année du calendrier grégorien.
    Sortie:  La liste des jour juliens correspondants.
             Cette liste peut contenir 0, 1 ou 2 dates.
    Référence [2] p. 60.
    """
    jan1 = fixed_from_gregorian(GDate(_JANUARY, 1, g_year))
    dec31 = fixed_from_gregorian(GDate(_DECEMBER, 31, g_year))
    y = ethiopic_from_fixed(jan1).year
    date1 = fixed_from_ethiopic(EDate(e_month, e_day, y))
    date2 = fixed_from_ethiopic(EDate(e_month, e_day, y + 1))
    lst = [date1] if jan1 <= date1 <= dec31 else []
    lst += [date2] if jan1 <= date2 <= dec31 else []
    return lst


if "__main__" == __name__:
    print("calendar")
    d0 = fixed_from_gregorian(GDate(7, 14.25, 1789))
    print(d0)
    
    g0 = gregorian_from_fixed(d0)
    print(g0, repr(g0))
    g = eval(repr(g0))
    print(g, repr(g), g == g0, g is g0)

    j0 = julian_from_fixed(d0)
    print(j0, repr(j0))
    j = eval(repr(j0))
    print(j, repr(j), j == j0, j is j0)
    
    i0 = iso_from_fixed(d0)
    print(i0, repr(i0))
    i = eval(repr(i0))
    print(i, repr(i), i == i0, i is i0)

    c0 = coptic_from_fixed(d0)
    print(c0, repr(c0))
    c = eval(repr(c0))
    print(c, repr(c), c == c0, c is c0)

    e0 =  ethiopic_from_fixed(d0)
    print(e0, repr(e0))
    e = eval(repr(e0))
    print(e, repr(e), e == e0, e is e0)

