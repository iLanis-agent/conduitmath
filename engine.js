// Conduit Math engine: how much of a conduit's cross section wires take, how many more fit under a fill you choose, and the smallest conduit for that fill. Areas are compared by the squares of the diameters, so the circle factor cancels exactly. Exact integers on tenths of a mm, results rounded half up.
function _t(t, err, lo, hi) { // decimal text with at most one place -> tenths
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,4})(?:\.([0-9]))?$/.exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * 10 + (m[2] ? parseInt(m[2], 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _w(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _DIA = "each wire diameter must be from 0.5 to 50 mm with at most one decimal place";
var _N = "each wire count must be a whole number from 0 to 50";
var _COND = "the conduit inner diameter must be from 1 to 200 mm with at most one decimal place";
var _FILL = "the fill limit must be a whole percent from 1 to 100";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _wires(c, d) { return c + (c === 1 ? " wire" : " wires") + " of " + _dec(d, 1) + " mm"; }
function _list(a) { return a.length === 1 ? a[0] : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]; }
function _isqrt(n) { var r = Math.floor(Math.sqrt(n)); while (r * r > n) r--; while ((r + 1) * (r + 1) <= n) r++; return r; }
function _in(c1, d1, c2, d2, c3, d3) {
  var c = [_w(c1, _N, 0, 50), _w(c2, _N, 0, 50), _w(c3, _N, 0, 50)];
  var d = [_t(d1, _DIA, 5, 500), _t(d2, _DIA, 5, 500), _t(d3, _DIA, 5, 500)];
  var S = 0;
  for (var i = 0; i < 3; i++) S += c[i] * d[i] * d[i];   // diameter squared, tenths squared
  return { c: c, d: d, S: S };
}
function _desc(p) {
  var a = [];
  for (var i = 0; i < 3; i++) if (p.c[i] > 0) a.push(_wires(p.c[i], p.d[i]));
  return a.length ? _list(a) : "no wires";
}

function fillTruth(c1, d1, c2, d2, c3, d3, cond) {
  var p = _in(c1, d1, c2, d2, c3, d3), D = _t(cond, _COND, 10, 2000);
  return "In a " + _dec(D, 1) + " mm conduit, " + _desc(p) + (p.c[0] + p.c[1] + p.c[2] === 1 ? " takes " : " take ") + _dec(_hu(1000 * p.S, D * D), 1) + "% of the cross section.";
}
function headroomTruth(c1, d1, c2, d2, c3, d3, cond, fill) {
  var p = _in(c1, d1, c2, d2, c3, d3), D = _t(cond, _COND, 10, 2000), f = _w(fill, _FILL, 1, 100);
  var N = f * D * D - 100 * p.S;
  if (N < 0) return "At a fill limit of " + f + "% the wires are already over it by " + _dec(_hu(-1000 * N, 100 * D * D), 1) + " points.";
  var extra = Math.floor(N / (100 * p.d[0] * p.d[0]));
  return "At a fill limit of " + f + "% that leaves room for " + extra + " more " + (extra === 1 ? "wire" : "wires") + " of " + _dec(p.d[0], 1) + " mm.";
}
function sizeTruth(c1, d1, c2, d2, c3, d3, fill) {
  var p = _in(c1, d1, c2, d2, c3, d3), f = _w(fill, _FILL, 1, 100);
  if (p.S === 0) return "With no wires there is no conduit to size.";
  var r = _isqrt(Math.ceil(100 * p.S / f));               // tenths, then adjust to the smallest that holds the fill
  while (r * r * f < 100 * p.S) r++;
  while (r > 1 && (r - 1) * (r - 1) * f >= 100 * p.S) r--;
  return "To keep " + _desc(p) + " at or under a " + f + "% fill, the conduit needs an inner diameter of at least " + _dec(r, 1) + " mm.";
}
