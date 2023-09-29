def gcd(a: int, b: int) -> int:
    if a < b:
        a, b = b, a

    while b != 0:
        temp = a % b
        a, b = b, temp

    return a


def gcde(r1: int, r2: int) -> tuple[int, int, int]:
    if r1 < r2:
        r1, r2 = r2, r1

    s1, s2 = 1, 0
    t1, t2 = 0, 1

    while r2 != 0:
        q = r1 // r2
        r = r1 % r2
        r1, s1, t1 = r2, s2, t2
        r2, s2, t2 = r, s1 - s2 * q, t1 - t2 * q

    return r1, s1, t1

