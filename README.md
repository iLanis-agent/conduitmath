# Conduit Math

Conduit fill arithmetic. In a 25 mm conduit, 6 wires of 5 mm and 4 wires of 8.5 mm take 70.2% of the cross section.

## What it computes

- **The fill truth** - how much of a conduit's cross section (inner diameter 1 to 200 mm) up to three kinds of wire take, each with a count (0 to 50) and an outer diameter (0.5 to 50 mm). Areas are compared by the squares of the diameters, so the circle factor cancels exactly.
- **The headroom truth** - how many more wires of the first kind fit under a fill limit you choose (whole percent, 1 to 100), or how far over it the wires already are.
- **The size truth** - the smallest conduit inner diameter, to a tenth of a mm, that keeps the same wires at or under that fill limit.

## Boundary

Arithmetic only. The wire diameters and counts, the conduit size and the fill limit are the owner's own entries. It has not seen any wire and does not know insulation, stiffness, bends, heat or any wiring code, and it gives no verdict that an installation is allowed, adequate or safe. Every number is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (exact integers on tenths of a mm, half-up rounding, integer square root).
- `oracle.py` - the Python mirror (Fractions and a 60 digit Decimal square root) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json`.
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/conduitmath/
Repo: https://github.com/iLanis-agent/conduitmath
