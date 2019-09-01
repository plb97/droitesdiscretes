import fqapy.fqa as fqa


def ddy(a_, b_, c_):
    print("ddy", a_, b_, c_)
    if 0 > b_:
        c_, b_, a_ = b_ - 1 - c_, -b_, -a_
        print("ddy2", a_, b_, c_)

    def f(x_):
        return (a_ * x_ + c_) // b_

    return f


def gen(f_, x0_=0, x1_=0):
    if not x1_ > x0_:
        raise ValueError("x1 n'est pas strictement supérieur à x0")
    ty = []
    for i in range(x1_ - x0_ + 1):
        x_ = x0_ + i
        y_ = f_(x_)
        ty.append((x_, y_))
    return ty


if "__main__" == __name__:
    tl0 = list(map(int, "00100010010010010001001001001001000100100100100"))
    print("tl0", tl0)
    print(fqa.codes(tl0))
    c = [2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1]
    print("c", c)
    print(fqa.codes(c))
    c = [2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1]
    print("c", c)
    print(fqa.codes(c))
    c = [31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 28]
    print("c", c)
    print(fqa.codes(c))
    c = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, ]
    print("c", c)
    print(fqa.codes(c))
    c = [354, 354, 355, 354, 354, 355, 354, 355, 354, 354, 355, ]
    print("c", c)
    print(fqa.codes(c))
    c = [3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3]
    print("c", c)
    print(fqa.codes(c))
    c = [3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 2]
    print("c", c)
    print(fqa.codes(c))
    c = [3, 3, 2, 3, 3, 3, 2, 3, 3, 2, 3, 3, 3, 2]
    print("c", c)
    print(fqa.codes(c))
    c = [365, 365, 365, 366, 365, 365, 365, 366]
    print("c", c)
    print(fqa.codes(c))
    c = [365, 365, 366, 365, 365, 365, 366, 365, ]
    print("c", c)
    print(fqa.codes(c))
    c = [365, 366, 365, 365, 365, 366, 365, 365, ]
    print("c", c)
    print(fqa.codes(c))
    c = [366, 365, 365, 365, 366, 365, 365, 365, ]
    print("c", c)
    print(fqa.codes(c))
    c = [36524, 36524, 36524, 36525, 36524, 36524, 36524, 36525]
    print("c", c)
    print(fqa.codes(c))
    c = [86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400]
    print("c", c)
    print(fqa.codes(c))
    c = [3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600]
    print("c", c)
    print(fqa.codes(c))
    c = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, ]
    print("c", c)
    print(fqa.codes(c))
    c = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ]
    print("c", c)
    print(fqa.codes(c))
    c = [31, 30, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    print("c", c)
    print(fqa.codes(c))

    # a, b, c = 5, 17, 4
    a, b, c = 24, 7, 10
    # a, b, c = 2, 7, 2
    x0 = 0
    x1 = x0 + abs(a) + abs(b)
    fqa1 = fqa.Fqa(a, b, c)
    print("fqa1", fqa1, "a/b", fqa1.a / fqa1.b, "r/b", fqa1.r / fqa1.b)
    txy = gen(ddy(a, b, c), x0, x1)
    x0, y0 = txy[0]
    print("x0", x0, "y0", y0)
    print("txy", txy)
    # ty = [y for _, y in txy]
    # print("ty", ty)
    # tc = list(map(lambda u, v: u - v, ty[1:], ty))
    # print("tc", tc)
    # print(codes(tc, x0, y0))
    tc = list(map(lambda u, v: u[1] - v[1], txy[1:], txy))
    print("tc", tc)
    fqa2 = fqa.codes(tc, x0, y0)
    print("fqa2", fqa2, "a/b", fqa2.a / fqa2.b, "r/b", fqa2.r / fqa2.b, fqa1 == fqa2)
    if not fqa1 == fqa2:
        for x in range(x0, x1 + 1):
            y = fqa2(x)
            print(x, y, y == txy[x - x0][1])


