#!/usr/bin/env python3
# Conduit Math oracle - mirrors engine.js with Fractions and Decimal: the cross sections are compared by the squares of the diameters (the circle factor cancels), the extra wires are added one at a time, the smallest conduit is found with a 60 digit Decimal square root, rounding is Decimal half-up.
import json, re, random
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 60

DIA = "each wire diameter must be from 0.5 to 50 mm with at most one decimal place"
N = "each wire count must be a whole number from 0 to 50"
COND = "the conduit inner diameter must be from 1 to 200 mm with at most one decimal place"
FILL = "the fill limit must be a whole percent from 1 to 100"
def dec(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,4}(\.[0-9])?", t) or not F(lo) <= F(t) <= F(hi): raise ValueError(err)
    return F(t)
def whole(t, err, lo, hi):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,3}", t) or not lo <= int(t) <= hi: raise ValueError(err)
    return int(t)
def txt(fr, places):
    v = int((Decimal(fr.numerator) / Decimal(fr.denominator) * (10 ** places)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    ip, fp = divmod(v, 10 ** places); fs = str(fp).zfill(places).rstrip("0")
    return f"{ip}.{fs}" if fs else str(ip)
def wires(c, d): return f"{c} wire{'s' if c != 1 else ''} of {txt(d,1)} mm"
def lst(a): return a[0] if len(a) == 1 else ", ".join(a[:-1]) + " and " + a[-1]
def inp(c1, d1, c2, d2, c3, d3):
    c = [whole(x, N, 0, 50) for x in (c1, c2, c3)]
    d = [dec(x, DIA, "0.5", "50") for x in (d1, d2, d3)]
    S = sum(c[i] * d[i] ** 2 for i in range(3))
    return c, d, S
def desc(c, d):
    a = [wires(c[i], d[i]) for i in range(3) if c[i] > 0]
    return lst(a) if a else "no wires"

def fill(c1, d1, c2, d2, c3, d3, cond):
    c, d, S = inp(c1, d1, c2, d2, c3, d3); D = dec(cond, COND, "1", "200"); verb = "takes" if sum(c) == 1 else "take"
    return f"In a {txt(D,1)} mm conduit, {desc(c,d)} {verb} {txt(100 * S / D ** 2,1)}% of the cross section."
def headroom(c1, d1, c2, d2, c3, d3, cond, fill_):
    c, d, S = inp(c1, d1, c2, d2, c3, d3); D = dec(cond, COND, "1", "200"); f = whole(fill_, FILL, 1, 100)
    if 100 * S > f * D ** 2:
        over = txt(F(100 * S - f * D ** 2) / (D ** 2), 1)
        return f"At a fill limit of {f}% the wires are already over it by {over} points."
    room = F(f) / 100 * D ** 2 - S
    extra = 0
    while (extra + 1) * d[0] ** 2 <= room: extra += 1
    return f"At a fill limit of {f}% that leaves room for {extra} more wire{'s' if extra != 1 else ''} of {txt(d[0],1)} mm."
def size(c1, d1, c2, d2, c3, d3, fill_):
    c, d, S = inp(c1, d1, c2, d2, c3, d3); f = whole(fill_, FILL, 1, 100)
    if S == 0: return "With no wires there is no conduit to size."
    target = Decimal(10000 * S.numerator) / Decimal(S.denominator) / Decimal(f)                # D squared, in tenths squared
    r = target.sqrt()                                     # D in tenths
    D = int(r.to_integral_value(rounding="ROUND_FLOOR"))
    while D * D * f < 10000 * S: D += 1
    while D > 1 and (D - 1) * (D - 1) * f >= 10000 * S: D -= 1
    return f"To keep {desc(c,d)} at or under a {f}% fill, the conduit needs an inner diameter of at least {txt(F(D,10),1)} mm."

FNS = {"fillTruth": fill, "headroomTruth": headroom, "sizeTruth": size}
def cases():
    c = []
    base = ["6", "5", "4", "8.5", "0", "10"]
    sets = [base, ["0", "5", "0", "8.5", "0", "10"], ["1", "50", "1", "0.5", "50", "50"], ["50", "50", "50", "50", "50", "50"],
            ["10", "12", "10", "12", "10", "12"], ["3", "2.5", "7", "4", "2", "6"], ["0", "5", "1", "1", "0", "10"], ["50", "0.5", "0", "10", "0", "50"]]
    for s in sets:
        for D in ["1", "25", "40.5", "200"]:
            c.append(("fillTruth", s + [D]))
            for f in ["1", "40", "50", "100"]:
                c.append(("headroomTruth", s + [D, f]))
        for f in ["1", "40", "50", "100"]:
            c.append(("sizeTruth", s + [f]))
    for a in [" 6 ", "06", "6.0"]:
        c += [("fillTruth", [a, " 5 ", "4", "8.5", "0", "10", " 25 "]), ("headroomTruth", [a, "5", "4", "8.5", "0", "10", "25", " 50 "])]
    bad = ["", "x", "-1", ".5", "5.", "1e2", "0.05", "1.25", "10000", "99999"]
    for v in bad:
        c += [("fillTruth", [v, "5", "4", "8.5", "0", "10", "25"]), ("fillTruth", ["6", v, "4", "8.5", "0", "10", "25"]),
              ("fillTruth", ["6", "5", "4", "8.5", "0", "10", v]), ("headroomTruth", ["6", "5", "4", "8.5", "0", "10", "25", v]),
              ("sizeTruth", ["6", "5", "4", "8.5", "0", "10", v])]
    for t in [["51", "5", "4", "8.5", "0", "10", "25"], ["6", "0.4", "4", "8.5", "0", "10", "25"], ["6", "50.1", "4", "8.5", "0", "10", "25"],
              ["6", "5", "4", "8.5", "0", "10", "0.9"], ["6", "5", "4", "8.5", "0", "10", "200.1"]]:
        c.append(("fillTruth", t))
    c += [("headroomTruth", ["6", "5", "4", "8.5", "0", "10", "25", "0"]), ("headroomTruth", ["6", "5", "4", "8.5", "0", "10", "25", "101"]),
          ("sizeTruth", ["6", "5", "4", "8.5", "0", "10", "0"]), ("sizeTruth", ["6", "5", "4", "8.5", "0", "10", "101"])]
    r = random.Random(716)
    for _ in range(8):
        s = [str(r.randint(0, 50)), f"{r.randint(0, 49)}.{r.randint(0, 9)}", str(r.randint(0, 50)), f"{r.randint(0, 49)}.{r.randint(0, 9)}", str(r.randint(0, 50)), f"{r.randint(0, 49)}.{r.randint(0, 9)}"]
        s = [s[i] if not (i % 2 == 1 and float(s[i]) < 0.5) else "0.5" for i in range(6)]
        D = f"{r.randint(1, 199)}.{r.randint(0, 9)}"; f = str(r.randint(1, 100))
        c += [("fillTruth", s + [D]), ("headroomTruth", s + [D, f]), ("sizeTruth", s + [f])]
    return c
out = []
for fn, args in cases():
    try: exp = FNS[fn](*args)
    except ValueError as e: exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    f.write("[\n" + ",\n".join(json.dumps(o, separators=(",", ":"), ensure_ascii=False) for o in out) + "\n]\n")
print(len(out), "cases written")
