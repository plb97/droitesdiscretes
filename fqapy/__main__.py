from .fqa import *
from .calendrier import *
from .calendar import *

if "__main__" == __name__:
    fqa = Fqa()
    print(fqa)
    fqa = Fqa(b=2, r=1, a=-1)
    print(fqa)
    print('fqa(4)', fqa(4))
    n, d = 3, 2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    q, r = divmod(n, d)
    print("*divmod: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    n, d = -3, 2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    q, r = divmod(n, d)
    print("*divmod: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    n, d = 3, -2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    q, r = divmod(n, d)
    print("*divmod: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    n, d = -3, -2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    q, r = divmod(n, d)
    print("*divmod: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    n, d = 0, 2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))
    n, d = 0, -2
    q, r = divent(n, d)
    print("divent: n={}, d={} -> q={}, r={} -> q*d+r={}".format(n, d, q, r, q * d + r))

    f = 2.123
    q, r = ent(f)
    print("f={} -> q={}, r={} -> q+r={}".format(f, q, r, q + r))
    f = -2.123
    q, r = ent(f)
    print("f={} -> q={}, r={} -> q+r={}".format(f, q, r, q + r))

    # t = _TabInt(0)
    # print(t)
    # print(t._minmax())
    # t = _TabInt(5)
    # print(t)
    # print(t._minmax())
    # t = _TabInt(taille=5, lst=list(range(0,3)))
    # print(t)
    # print(t._minmax())

    print("egalf(0.1,0.09999999999999998)", egalf(0.1, 0.09999999999999998))
    print("egalf(-0.1,-0.09999999999999998)", egalf(-0.1, -0.09999999999999998))

    dt, jd = Date(1957, 10, 4.81, CALENDRIER_GRE), 2436116.31

    jj = dt()
    print("dt={} -> jj()={}, jj.jd()={}".format(dt, jd, jj(), jj - EPOQUE_JD))

    rd0 = Date(1, 1, 0, CALENDRIER_GRE)()  # veille du premier janvier
    print("rd0", rd0, "jj", rd0(), "jd", rd0 - EPOQUE_JD)

    rd0 = EPOQUE_JD + 1721424.5
    print("rd0", rd0, "jj", rd0(), "jd", rd0 - EPOQUE_JD)

    rd0 = EPOQUE_JJ + 1721425.0
    print("rd0", rd0, "jj", rd0(), "jd", rd0 - EPOQUE_JD)

    rd0p1 = rd0 + 1
    rd0m1 = rd0 - 1
    print("rd0", rd0, "rd0p1", rd0p1, "rd0m1", rd0m1, "rd0p1 - rd0m1", rd0p1 - rd0m1)

    # 3 heures 48 secondes et 18 secondes
    j, h, m, s = 7, 3, 48, 18
    t0 = j * 86400 + 3600 * h + 60 * m + s
    t = BASE_TEMPS([j, h, m, s])
    print("t0", t0, "t", t, BASE_TEMPS.inv(t))

    print("rd0", rd0)
    rd0 += 1
    print("rd0+=1", rd0)
    rd0 -= 1
    print("rd0-=1", rd0)

    print("EPOQUE_RD", EPOQUE_RD, CALENDRIER_GRE.date(EPOQUE_RD), EPOQUE_RD.jour_semaine(), "EPOQUE_RD+5",
          EPOQUE_RD + 5, "EPOQUE_RD-3.2", EPOQUE_RD - 3.2)
    print("EPOQUE_JD", EPOQUE_JD.jour_semaine(), EPOQUE_JD, CALENDRIER_GRE.date(EPOQUE_JD),
          CALENDRIER_JUL.date(EPOQUE_JD))
    j = julian_from_fixed(EPOQUE_JD - EPOQUE_JJ)
    print("***", j, EPOQUE_JD - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_HEB", EPOQUE_HEB.jour_semaine(), EPOQUE_HEB, CALENDRIER_GRE.date(EPOQUE_HEB),
          CALENDRIER_JUL.date(EPOQUE_HEB))
    j = julian_from_fixed(EPOQUE_HEB - EPOQUE_JJ)
    print("***", j, EPOQUE_HEB - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_MAY", EPOQUE_MAY.jour_semaine(), EPOQUE_MAY, CALENDRIER_GRE.date(EPOQUE_MAY),
          CALENDRIER_JUL.date(EPOQUE_MAY))
    j = julian_from_fixed(EPOQUE_MAY - EPOQUE_JJ)
    print("***", j, EPOQUE_MAY - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_HIN", EPOQUE_HIN.jour_semaine(), EPOQUE_HIN, CALENDRIER_GRE.date(EPOQUE_HIN),
          CALENDRIER_JUL.date(EPOQUE_HIN))
    j = julian_from_fixed(EPOQUE_HIN - EPOQUE_JJ)
    print("***", j, EPOQUE_HIN - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_CHI", EPOQUE_CHI.jour_semaine(), EPOQUE_CHI, CALENDRIER_GRE.date(EPOQUE_CHI),
          CALENDRIER_JUL.date(EPOQUE_CHI))
    j = julian_from_fixed(EPOQUE_CHI - EPOQUE_JJ)
    print("***", j, EPOQUE_CHI - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_JUL", EPOQUE_JUL.jour_semaine(), EPOQUE_JUL, CALENDRIER_GRE.date(EPOQUE_JUL),
          CALENDRIER_JUL.date(EPOQUE_JUL))
    j = julian_from_fixed(EPOQUE_JUL - EPOQUE_JJ)
    print("***", j, EPOQUE_JUL - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_GRE", EPOQUE_GRE.jour_semaine(), EPOQUE_GRE, CALENDRIER_GRE.date(EPOQUE_GRE),
          CALENDRIER_JUL.date(EPOQUE_GRE))
    j = julian_from_fixed(EPOQUE_GRE - EPOQUE_JJ)
    print("***", j, EPOQUE_GRE - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_ISO", EPOQUE_ISO.jour_semaine(), EPOQUE_ISO, CALENDRIER_GRE.date(EPOQUE_ISO),
          CALENDRIER_JUL.date(EPOQUE_ISO))
    j = julian_from_fixed(EPOQUE_ISO - EPOQUE_JJ)
    print("***", j, EPOQUE_ISO - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_ETH", EPOQUE_ETH.jour_semaine(), EPOQUE_ETH, CALENDRIER_GRE.date(EPOQUE_ETH),
          CALENDRIER_JUL.date(EPOQUE_ETH))
    j = julian_from_fixed(EPOQUE_ETH - EPOQUE_JJ)
    print("***", j, EPOQUE_ETH - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_COP", EPOQUE_COP.jour_semaine(), EPOQUE_COP, CALENDRIER_GRE.date(EPOQUE_COP),
          CALENDRIER_JUL.date(EPOQUE_COP))
    j = julian_from_fixed(EPOQUE_COP - EPOQUE_JJ)
    print("***", j, EPOQUE_COP - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_PER", EPOQUE_PER.jour_semaine(), EPOQUE_PER, CALENDRIER_GRE.date(EPOQUE_PER),
          CALENDRIER_JUL.date(EPOQUE_PER))
    j = julian_from_fixed(EPOQUE_PER - EPOQUE_JJ)
    print("***", j, EPOQUE_PER - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_ISL", EPOQUE_ISL.jour_semaine(), EPOQUE_ISL, CALENDRIER_GRE.date(EPOQUE_ISL),
          CALENDRIER_JUL.date(EPOQUE_ISL))
    j = julian_from_fixed(EPOQUE_ISL - EPOQUE_JJ)
    print("***", j, EPOQUE_ISL - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_RFR", EPOQUE_RFR.jour_semaine(), EPOQUE_RFR, CALENDRIER_GRE.date(EPOQUE_RFR),
          CALENDRIER_JUL.date(EPOQUE_RFR))
    j = julian_from_fixed(EPOQUE_RFR - EPOQUE_JJ)
    print("***", j, EPOQUE_RFR - EPOQUE_JJ == fixed_from_julian(j))
    print("EPOQUE_BAH", EPOQUE_BAH.jour_semaine(), EPOQUE_BAH, CALENDRIER_GRE.date(EPOQUE_BAH),
          CALENDRIER_JUL.date(EPOQUE_BAH))
    j = julian_from_fixed(EPOQUE_BAH - EPOQUE_JJ)
    print("***", j, EPOQUE_BAH - EPOQUE_JJ == fixed_from_julian(j))

    print("divmod(1.2,1)", divmod(1.2, 1), "ent(1.2)", ent(1.2))
    print("divmod(-1.2,1)", divmod(-1.2, 1), "ent(-1.2)", ent(-1.2))

    jd = 2436116.31
    jj = EPOQUE_JD + jd
    dt = CALENDRIER_GRE.date(jj)
    print("jd", jd, "jj", jj, "dt", dt)

    jd = 1842713.0
    jj = EPOQUE_JD + jd
    dt = CALENDRIER_JUL.date(jj)
    print("jd", jd, "jj", jj, "dt", dt, jj.n, jj.f)

    # jj = EPOQUE_JJ + 0.5
    # print("EPOQUE_JJ + 0.5",jj, jj.jd(), CALENDRIER_JUL.date(jj))
    # print("jj == EPOQUE_JD", jj == EPOQUE_JD)
    print("EPOQUE_JJ", EPOQUE_JJ, EPOQUE_JJ - EPOQUE_JD, "jul", CALENDRIER_JUL.date(EPOQUE_JJ),
          "gre", CALENDRIER_GRE.date(EPOQUE_JJ))
    print("EPOQUE_JD", EPOQUE_JD, EPOQUE_JD - EPOQUE_JD, "jul", CALENDRIER_JUL.date(EPOQUE_JD),
          "gre", CALENDRIER_GRE.date(EPOQUE_JD))
    print("EPOQUE_RD", EPOQUE_RD, EPOQUE_RD - EPOQUE_JD, "jul", CALENDRIER_JUL.date(EPOQUE_RD),
          "gre", CALENDRIER_GRE.date(EPOQUE_RD))
    print("EPOQUE_JUL", EPOQUE_JUL, EPOQUE_JUL - EPOQUE_JD, "jul", CALENDRIER_JUL.date(EPOQUE_JUL),
          "gre", CALENDRIER_GRE.date(EPOQUE_JUL))
    print("EPOQUE_GRE", EPOQUE_GRE, EPOQUE_GRE - EPOQUE_JD, "jul", CALENDRIER_JUL.date(EPOQUE_GRE),
          "gre", CALENDRIER_GRE.date(EPOQUE_GRE))
