"""Module de test de calendar."""

import unittest

from . import calendrier
from . import calendar

_JULIAN_EPOCH = 1721424


class CalendarTestCase(unittest.TestCase):
    """Série de tests du module calendar."""

    def test_signum(self):
        """Référence [2] p. 15."""
        # print()
        # print("test_signum")
        tt = [
            {"y": 1.2, "s": 1, },
            {"y": -12, "s": -1, },
            {"y": 0, "s": 0, },
            {"y": 0.0, "s": 0, },
            {"y": float('NaN'), "s": 0, },
        ]
        # print()
        # print("test_signum")
        for v_ in tt:
            s = calendar.signum(v_["y"])
            # print("v", v_, "s", s)
            self.assertEqual(v_["s"], s)

        with self.assertRaises(TypeError):
            calendar.signum('NaN')

    def test_amod(self):
        """Référence [2] p. 15."""
        # print()
        # print("test_amod")
        tt = [
            {"x": 9, "y": 5, "r": 4, },
            {"x": -9, "y": 5, "r": 1, },
            {"x": 9, "y": -5, "r": -1, },
            {"x": -9, "y": -5, "r": -4, },
            {"x": 6, "y": 2, "r": 2, },
        ]
        for v_ in tt:
            r = calendar.amod(v_["x"], v_["y"])
            # print("v", v_, "r", r)
            self.assertEqual(v_["r"], r)

        with self.assertRaises(TypeError):
            calendar.amod(1, 'NaN')
            calendar.amod('NaN', 1)

        with self.assertRaises(ZeroDivisionError):
            calendar.amod(1, 0)

    def test_kday_on_or_before(self):
        """Référence [2] p. 15."""

        # print()
        # print("test_kday_on_or_before")

        def date(a_, m_, j_):
            return calendar.fixed_from_gregorian(calendar.GDate(m_, j_, a_))

        tt = [
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.LUNDI,
             "kday": date(2019, 6, 24), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.MARDI,
             "kday": date(2019, 6, 25), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.MERCREDI,
             "kday": date(2019, 6, 26), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.JEUDI,
             "kday": date(2019, 6, 27), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.VENDREDI,
             "kday": date(2019, 6, 21), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.SAMEDI,
             "kday": date(2019, 6, 22), },
            {"date": date(2019, 6, 27), "js": calendrier.Jours.JEUDI, "k": calendrier.Jours.DIMANCHE,
             "kday": date(2019, 6, 23), },
        ]
        for v_ in tt:
            kday = calendar.kday_on_or_before(v_["date"], v_["k"])
            # print("v", v_, "kday", kday)
            self.assertEqual(v_["kday"], kday)

    def test_number_of_days_in_the_year_prior_year(self):
        """Référence : [2] p. 22."""
        # print()
        # print("test_number_of_days_in_the_year_prior_year")
        tt = [
            #              c, l, delta, L
            {"cal": "Julian C.E.", "c": 4, "l": 1, "delta": 0, "L": 365, },
            # {"cal":"Julian B.C.E.","c":4, "l":1, "delta":1, "L":365,},
            {"cal": "Coptic/Ethiopic", "c": 4, "l": 1, "delta": 1, "L": 365, },
            {"cal": "Islamic", "c": 30, "l": 11, "delta": 4, "L": 354, },
            {"cal": "Islamic (variant)", "c": 30, "l": 11, "delta": 15, "L": 354, },
            {"cal": "Hebrew (month)", "c": 19, "l": 7, "delta": 11, "L": 12, },
            # {"cal":"Persian (partial)","c":2816, "l":682, "delta":38, "L":365,},
            # {"cal":"Gregorian/Julian (approximate)","c":12, "l":7, "delta":11, "L":30,},
        ]
        for v_ in tt:
            cal, c_, l, delta, L = v_["cal"], v_["c"], v_["l"], v_["delta"], v_["L"]
            # o = -delta % c + 1
            o = 1
            # print("v", v_, "cal", cal, "c", c_, "l", l, "L", L, "delta", delta, o)
            # pn = calendar.number_of_days_in_the_year_prior_year(o, l, c_, L, delta)
            for y in range(o + 1, c_ + o + 1):
                n_ = calendar.number_of_days_in_the_year_prior_year(y, l, c_, L, delta)
                a_ = calendar.year_at_day(n_, l, c_, L, delta)
                # print("y", y - 1, "a", a_ - 1, "n", n_, n_ - pn, ["", "*"][(n_ - pn) % L])
                # pn = n_
                self.assertEqual(y, a_)
            # print()
        #
        # with self.assertRaises(TypeError):
        #    pass

    def test_iso_date(self):
        """Référence : [2] p. 22."""
        # print()
        # print("test_iso_date")
        tt = [
            {"g_date": calendar.GDate(1, 1, 2006), "iso_date": calendar.ISODate(52, 7, 2005), },
            {"g_date": calendar.GDate(1, 2, 2006), "iso_date": calendar.ISODate(1, 1, 2006), },
            {"g_date": calendar.GDate(12, 31, 2006), "iso_date": calendar.ISODate(52, 7, 2006), },
            {"g_date": calendar.GDate(1, 1, 2007), "iso_date": calendar.ISODate(1, 1, 2007), },
            {"g_date": calendar.GDate(12, 30, 2007), "iso_date": calendar.ISODate(52, 7, 2007), },
            {"g_date": calendar.GDate(12, 31, 2007), "iso_date": calendar.ISODate(1, 1, 2008), },
            {"g_date": calendar.GDate(1, 1, 2008), "iso_date": calendar.ISODate(1, 2, 2008), },
            {"g_date": calendar.GDate(12, 29, 2008), "iso_date": calendar.ISODate(1, 1, 2009), },
            {"g_date": calendar.GDate(12, 31, 2008), "iso_date": calendar.ISODate(1, 3, 2009), },
            {"g_date": calendar.GDate(1, 1, 2009), "iso_date": calendar.ISODate(1, 4, 2009), },
            {"g_date": calendar.GDate(12, 31, 2009), "iso_date": calendar.ISODate(53, 4, 2009), },
            {"g_date": calendar.GDate(1, 3, 2010), "iso_date": calendar.ISODate(53, 7, 2009), },
        ]
        for v_ in tt:
            # print()
            g_date = v_["g_date"]
            iso_date = v_["iso_date"]
            # print("g_date", g_date, "iso_date", iso_date)

            fixed_g_date = calendar.fixed_from_gregorian(g_date)
            fixed_iso_date = calendar.fixed_from_iso(iso_date)
            self.assertEqual(fixed_g_date, fixed_iso_date)

            iso_g_date = calendar.iso_from_fixed(fixed_g_date)
            # print("fixed_g_date", fixed_g_date, "iso_g_date", iso_g_date)
            g_iso_date = calendar.gregorian_from_fixed(fixed_iso_date)
            # print("fixed_iso_date", fixed_iso_date, "g_iso_date", g_iso_date)
            self.assertEqual(g_date, g_iso_date)
            self.assertEqual(iso_date, iso_g_date)

    def test_julian_date(self):
        """Référence : [2] p. 14."""
        # print()
        # print("test_julian_date")
        # print(fixed_from_gregorian(GDate(12, 30, 0)), _JULIAN_EPOCH)
        tt = [
            {"g_date": calendar.GDate(11, 24.5, -4713), "j_date": calendar.JDate(1, 1.5, -4713), },
            {"g_date": calendar.GDate(9, 7, -3760), "j_date": calendar.JDate(10, 7, -3761), },
            {"g_date": calendar.GDate(8, 11, -3113), "j_date": calendar.JDate(9, 6, -3114), },
            {"g_date": calendar.GDate(1, 23, -3101), "j_date": calendar.JDate(2, 18, -3102), },
            {"g_date": calendar.GDate(2, 15, -2636), "j_date": calendar.JDate(3, 8, -2637), },
            {"g_date": calendar.GDate(12, 30, 0), "j_date": calendar.JDate(1, 1, 1), },
            {"g_date": calendar.GDate(1, 1, 1), "j_date": calendar.JDate(1, 3, 1), },
            {"g_date": calendar.GDate(8, 27, 7), "j_date": calendar.JDate(8, 29, 7), },
            {"g_date": calendar.GDate(8, 29, 284), "j_date": calendar.JDate(8, 29, 284), },
            {"g_date": calendar.GDate(3, 22, 622), "j_date": calendar.JDate(3, 19, 622), },
            {"g_date": calendar.GDate(7, 19, 622), "j_date": calendar.JDate(7, 16, 622), },
            {"g_date": calendar.GDate(9, 22, 1792), "j_date": calendar.JDate(9, 11, 1792), },
            {"g_date": calendar.GDate(3, 21, 1844), "j_date": calendar.JDate(3, 9, 1844), },
        ]
        for v_ in tt:
            # print()
            g_date = v_["g_date"]
            j_date = v_["j_date"]
            # print("g_date", g_date, "j_date", j_date)
            fixed_g_date = calendar.fixed_from_gregorian(g_date)
            fixed_j_date = calendar.fixed_from_julian(j_date)
            self.assertEqual(fixed_g_date, fixed_j_date)

            j_g_date = calendar.julian_from_fixed(fixed_g_date)
            # print("fixed_g_date", fixed_g_date, "j_g_date", j_g_date)
            g_j_date = calendar.gregorian_from_fixed(fixed_j_date)
            # print("fixed_j_date", fixed_j_date, "g_j_date", g_j_date, fixed_j_date - _JULIAN_EPOCH - 1)
            self.assertEqual(g_date, g_j_date)
            self.assertEqual(j_date, j_g_date)

        # https://www.timeanddate.com/holidays/common/orthodox-christmas-day (consulté en 2019)
        self.assertEqual(calendar.gregorian_from_fixed(calendar.eastern_orthodox_christmas(2019)[0]),
                         calendar.GDate(1, 7, 2019))
        self.assertEqual(calendar.gregorian_from_fixed(calendar.eastern_orthodox_christmas(2020)[0]),
                         calendar.GDate(1, 7, 2020))

        # print()
        # https://www.vive-paques.com/paques/date-paques.htm (consulté en 2019)
        paques = [
            {"g_paques": calendar.GDate(4, 1, 2018), "j_paques": calendar.GDate(4, 8, 2018),
             "h_paques": calendar.GDate(3, 31, 2018), },
            {"g_paques": calendar.GDate(4, 21, 2019), "j_paques": calendar.GDate(4, 28, 2019),
             "h_paques": calendar.GDate(4, 20, 2019), },
            {"g_paques": calendar.GDate(4, 12, 2020), "j_paques": calendar.GDate(4, 19, 2020),
             "h_paques": calendar.GDate(4, 9, 2020), },
            {"g_paques": calendar.GDate(4, 4, 2021), "j_paques": calendar.GDate(5, 2, 2021),
             "h_paques": calendar.GDate(3, 28, 2021), },
            {"g_paques": calendar.GDate(4, 17, 2022), "j_paques": calendar.GDate(4, 24, 2022),
             "h_paques": calendar.GDate(4, 16, 2022), },
            {"g_paques": calendar.GDate(4, 9, 2023), "j_paques": calendar.GDate(4, 16, 2023),
             "h_paques": calendar.GDate(4, 6, 2023), },
            {"g_paques": calendar.GDate(3, 31, 2024), "j_paques": calendar.GDate(5, 5, 2024),
             "h_paques": calendar.GDate(4, 23, 2024), },
            {"g_paques": calendar.GDate(4, 20, 2025), "j_paques": calendar.GDate(4, 20, 2025),
             "h_paques": calendar.GDate(4, 13, 2025), },
        ]
        for i_ in range(len(paques)):
            a_ = 2018 + i_
            g_e = calendar.gregorian_from_fixed(calendar.easter(a_))
            # print("easter({})".format(a_), g_e, paques[i_]["g_paques"])
            j_e = calendar.gregorian_from_fixed(calendar.nicaean_rule_easter(a_))
            # print("nicaean rule({})".format(a_), j_e, paques[i_]["j_paques"])
            self.assertEqual(g_e, paques[i_]["g_paques"])
            self.assertEqual(j_e, paques[i_]["j_paques"])

        # print()
        pentecotes = [calendar.GDate(6, 9, 2019), calendar.GDate(5, 31, 2020), calendar.GDate(5, 23, 2021), ]
        for i_ in range(len(pentecotes)):
            a_ = 2019 + i_
            g_p = calendar.gregorian_from_fixed(calendar.pentecost(a_))
            # print("pentecost({})".format(a_), g_p, pentecotes[i_])
            self.assertEqual(g_p, pentecotes[i_])

    def test_coptic_date(self):
        """Référence : [2] pp. 57-58."""
        # https://www.timeanddate.com/holidays/egypt/coptic-christmas-day (consulté en 2019)
        # print()
        # print("test_coptic_date")
        tt = [
            {"year": 2015, "g_date": calendar.GDate(1, 7, 2015), },
            # {"year":2016, "g_date":GDate(1, 7, 2016),},
            {"year": 2017, "g_date": calendar.GDate(1, 7, 2017), },
            {"year": 2018, "g_date": calendar.GDate(1, 7, 2018), },
            {"year": 2019, "g_date": calendar.GDate(1, 7, 2019), },
            # {"year":2020, "g_date":GDate(1, 7, 2020),},
            {"year": 2021, "g_date": calendar.GDate(1, 7, 2021), },
            {"year": 2022, "g_date": calendar.GDate(1, 7, 2022), },
            {"year": 2023, "g_date": calendar.GDate(1, 7, 2023), },
            # {"year":2024, "g_date":GDate(1, 7, 2024),},
            {"year": 2025, "g_date": calendar.GDate(1, 7, 2025), },
        ]
        for v_ in tt:
            g_date = calendar.gregorian_from_fixed(calendar.coptic_christmas(v_["year"])[0])
            # print("v", v_, "year", v_["year"], coptic_leap_year(v_["year"]), "g_date", v_["g_date"], "->", g_date)
            self.assertEqual(g_date, v_["g_date"])


if "__main__" == __name__:
    # print("calendar_test")
    # print("coptic epoch", fixed_from_julian(JDate(8, 29, 284)))
    # print("coptic_christmas(2019)", gregorian_from_fixed(coptic_christmas(2019)[0]))
    unittest.main()
