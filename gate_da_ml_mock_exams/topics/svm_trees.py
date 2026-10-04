"""SVM & Decision Trees (with a few ensemble templates) for the GATE DA ML mock-exam generator."""
import math
from fractions import Fraction
from itertools import combinations

import numpy as np

from core import (Q, Figure, Table, fmt, frac, mcq, mcq_numeric, msq_from_statements, nat_hint, nat_range,
                  template, vec)

TOPIC = "SVM & Decision Trees"
S_MARGIN = "SVM: margin & geometry"
S_DUAL = "SVM: dual & support vectors"
S_SOFT = "SVM: soft margin & hinge loss"
S_KER = "SVM: kernels"
S_PERC = "Perceptron (linear separators)"
S_IMP = "Decision trees: impurity measures"
S_SPLIT = "Decision trees: split selection"
S_STRUCT = "Decision trees: structure & traversal"
S_PRUNE = "Decision trees: overfitting & pruning"
S_REG = "Regression trees"
S_BAG = "Ensembles: bagging & random forests"
S_BOOST = "Ensembles: boosting"

INK = "#222222"
GREY = "#777777"


# =============================================================================
# Generic helpers
# =============================================================================
def _pick(rng, seq):
    return seq[int(rng.integers(len(seq)))]


def _q(x, maxden=400):
    """Exact-looking rational display of a float that is (close to) a simple fraction."""
    return frac(Fraction(float(x)).limit_denominator(maxden))


def _H(c):
    c = np.asarray(c, float)
    p = c[c > 0] / c.sum()
    return float(-(p * np.log2(p)).sum())


def _G(c):
    c = np.asarray(c, float)
    p = c / c.sum()
    return float(1 - (p ** 2).sum())


def _ME(c):
    c = np.asarray(c, float)
    return float(1 - c.max() / c.sum())


def _H_expr(c):
    n = sum(c)
    terms = [f"({k}/{n})log<sub>2</sub>({k}/{n})" for k in c if k > 0]
    if len(terms) <= 1:
        return "0 (pure node)"
    return "−" + " − ".join(terms)


def _G_expr(c):
    n = sum(c)
    return "1 − [" + " + ".join(f"({k}/{n})²" for k in c) + "]"


def _cstr(c):
    if len(c) == 2:
        return f"[{c[0]}+, {c[1]}−]"
    return "[" + ", ".join(str(k) for k in c) + "]"


def _sub(name, i):
    return f"{name}<sub>{i}</sub>"


def _lin_str(w, b, var="x"):
    """String for w1 x1 + w2 x2 + b (markup)."""
    parts = []
    for j, wj in enumerate(w, 1):
        if abs(wj) < 1e-12:
            continue
        mag = abs(wj)
        coef = "" if abs(mag - 1) < 1e-12 else fmt(mag, 3)
        sign = "−" if wj < 0 else "+"
        term = f"{coef}{var}<sub>{j}</sub>"
        if not parts:
            parts.append(("−" if wj < 0 else "") + term)
        else:
            parts.append(f" {sign} {term}")
    if abs(b) > 1e-12 or not parts:
        if parts:
            parts.append(f" {'−' if b < 0 else '+'} {fmt(abs(b), 3)}")
        else:
            parts.append(fmt(b, 3))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Tree drawing
# ---------------------------------------------------------------------------
def _node(text, children=None):
    return {"text": text, "children": children or []}


def _tree_positions(root):
    pos = {}
    nxt = [0]

    def rec(n, d):
        if not n["children"]:
            x = nxt[0]
            nxt[0] += 1
        else:
            xs = [rec(c, d + 1) for _, c in n["children"]]
            x = sum(xs) / len(xs)
        pos[id(n)] = (x, -d)
        return x

    rec(root, 0)
    return pos, nxt[0]


def _draw_tree(ax, root, fs=7.0, leaf_fc="#e6e6e6"):
    pos, nleaves = _tree_positions(root)

    def rec(n):
        x, y = pos[id(n)]
        for lab, c in n["children"]:
            cx, cy = pos[id(c)]
            ax.annotate("", xy=(cx, cy), xytext=(x, y),
                        arrowprops=dict(arrowstyle="-|>", color="#333333", lw=0.8, shrinkA=7, shrinkB=9),
                        zorder=1)
            if lab:
                ax.text(x + 0.6 * (cx - x), y + 0.6 * (cy - y), lab, fontsize=fs - 0.6, ha="center", va="center",
                        color="#111111", zorder=4,
                        bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
            rec(c)
        leaf = not n["children"]
        ax.text(x, y, n["text"], ha="center", va="center", fontsize=fs, zorder=5,
                bbox=dict(boxstyle="square,pad=0.3" if leaf else "round,pad=0.35",
                          fc=leaf_fc if leaf else "white", ec=INK, lw=0.8))
        return None

    rec(root)
    depth = max(-p[1] for p in pos.values())
    ax.set_xlim(-0.75, nleaves - 0.25)
    ax.set_ylim(-depth - 0.5, 0.5)
    ax.axis("off")


# ---------------------------------------------------------------------------
# SVM helpers
# ---------------------------------------------------------------------------
_DIRS = [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (2, 1), (1, -2), (2, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]


def _hard_svm(X, y):
    """Exact hard-margin SVM in 2-D for small data sets.

    The optimum is defined by 2 support vectors (one per class) or 3 (two of one class on a
    margin line + one of the other class).  We enumerate all such candidates, keep the
    feasible ones and return the one with the largest margin."""
    P = [i for i in range(len(y)) if y[i] > 0]
    N = [i for i in range(len(y)) if y[i] < 0]
    cands = []
    for i in P:
        for j in N:
            d = X[i] - X[j]
            dd = d @ d
            w = 2 * d / dd
            cands.append((w, -w @ (X[i] + X[j]) / 2))
    for cls, other in ((P, N), (N, P)):
        if not cls:
            continue
        s = y[cls[0]]
        for a, b in combinations(cls, 2):
            e = X[b] - X[a]
            nv = np.array([-e[1], e[0]])
            for c in other:
                den = s * (nv @ (X[a] - X[c]))
                if abs(den) < 1e-12:
                    continue
                w = 2 / den * nv
                cands.append((w, s - w @ X[a]))
    best = None
    for w, b in cands:
        if (y * (X @ w + b)).min() >= 1 - 1e-9:
            m = 2 / np.linalg.norm(w)
            if best is None or m > best[2] + 1e-9:
                best = (w, b, m)
    if best is None:
        return None
    w, b, m = best
    sv = np.where(np.abs(y * (X @ w + b) - 1) < 1e-9)[0]
    return w, b, m, sv


def _alphas(X, y, w, sv):
    if len(sv) < 2 or len(sv) > 3:
        return None
    A = np.vstack([(y[sv][:, None] * X[sv]).T, y[sv][None, :]])
    rhs = np.array([w[0], w[1], 0.0])
    a, *_ = np.linalg.lstsq(A, rhs, rcond=None)
    if np.abs(A @ a - rhs).max() > 1e-8 or (a <= 1e-7).any():
        return None
    return a


def _gen_svm(rng, npos, nneg, hi=6, nice_alpha=False):
    grid = np.array([(i, j) for i in range(hi + 1) for j in range(hi + 1)], float)
    for _ in range(5000):
        nvec = np.array(_pick(rng, _DIRS), float)
        s = grid @ nvec
        lo, up = int(s.min()) + 2, int(s.max()) - 2
        if lo > up:
            continue
        c = int(rng.integers(lo, up + 1))
        g = int(rng.integers(1, 3))
        posc = np.where(s >= c + g)[0]
        negc = np.where(s <= c - g)[0]
        if len(posc) < npos + 1 or len(negc) < nneg + 1:
            continue
        wp = np.exp(-(s[posc] - c) / 1.5)
        wn = np.exp(-(c - s[negc]) / 1.5)
        ip = rng.choice(posc, npos, replace=False, p=wp / wp.sum())
        ineg = rng.choice(negc, nneg, replace=False, p=wn / wn.sum())
        X = np.vstack([grid[ip], grid[ineg]])
        y = np.array([1.0] * npos + [-1.0] * nneg)
        perm = rng.permutation(len(y))
        X, y = X[perm], y[perm]
        res = _hard_svm(X, y)
        if res is None:
            continue
        w, b, m, sv = res
        a = _alphas(X, y, w, sv)
        if a is None:
            continue
        if nice_alpha and not all(abs(round(v, 3) - v) < 1e-9 and v >= 0.05 for v in a):
            continue
        return X, y, w, b, m, sv, a
    raise RuntimeError("could not generate SVM data")


def _svm_axes(ax, X, y, hi=6, lines=None, labels=True, test=None):
    pos = y > 0
    ax.scatter(X[pos, 0], X[pos, 1], marker="o", s=34, c=INK, label="y = +1", zorder=3)
    ax.scatter(X[~pos, 0], X[~pos, 1], marker="s", s=34, facecolors="white", edgecolors=INK, linewidths=1.1,
               label="y = −1", zorder=3)
    if labels:
        for i, (a, b) in enumerate(X):
            ax.annotate(f"P{i + 1}", (a, b), textcoords="offset points", xytext=(4, 4), fontsize=6.5)
    if test is not None:
        ax.scatter([test[0]], [test[1]], marker="x", s=40, c=INK, zorder=3, label="test point")
    if lines:
        xs = np.linspace(-0.8, hi + 0.8, 50)
        for (w, b, c, style) in lines:
            if abs(w[1]) > 1e-12:
                ax.plot(xs, (c - b - w[0] * xs) / w[1], style, color=GREY, lw=1)
            else:
                ax.axvline((c - b) / w[0], ls=style, color=GREY, lw=1)
    ax.set_xlim(-0.8, hi + 0.8)
    ax.set_ylim(-0.8, hi + 0.8)
    ax.set_xticks(range(0, hi + 1))
    ax.set_yticks(range(0, hi + 1))
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False)


def _eval_str(w, t, b):
    """'w1·t1 + w2·t2 + b' with exact fractions and proper signs."""
    s = f"({_q(w[0])})({fmt(t[0])}) + ({_q(w[1])})({fmt(t[1])})"
    s += (" − " if b < 0 else " + ") + _q(abs(b))
    return s


def _pts_table(X, y, extra=None, extra_head=None):
    head = ["Point", "x₁", "x₂", "y"] + ([extra_head] if extra_head else [])
    rows = [head]
    for i in range(len(y)):
        r = [f"P{i + 1}", fmt(X[i, 0]), fmt(X[i, 1]), "+1" if y[i] > 0 else "−1"]
        if extra is not None:
            r.append(extra[i])
        rows.append(r)
    return Table(rows, header=True)


# =============================================================================
# SVM — 1 mark
# =============================================================================
_PYTH = [(3, 4), (6, 8), (5, 12), (1, 2, 2), (2, 3, 6), (1, 4, 8), (4, 4, 7), (2, 6, 9), (8, 15), (2, 1), (1, 1),
         (1, 3), (2, 2, 1), (3, 0, 4)]


@template(TOPIC, S_MARGIN, marks=1, qtype="NAT")
def svm_margin_width(rng):
    v = int(rng.integers(3))
    if v == 0:
        w = np.array(_pick(rng, _PYTH), float) * _pick(rng, [1, 1, 0.5])
        b = int(rng.integers(-5, 6))
        nw = np.linalg.norm(w)
        ans = 2 / nw
        d = 2 if ans >= 0.1 else 3
        text = (f"A hard-margin linear SVM trained on a separable data set returns the canonical solution "
                f"w = {vec(w)}, b = {fmt(b)} (so that min<sub>i</sub> y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1). "
                f"The width of the margin, i.e. the distance between the hyperplanes wᵀx + b = +1 and "
                f"wᵀx + b = −1, is ______")
        sol = [f"Margin width = 2/‖w‖.  ‖w‖ = √({' + '.join(fmt(x * x) for x in w)}) = {fmt(nw, 4)}.",
               f"Width = 2/{fmt(nw, 4)} = <b>{fmt(ans, d)}</b>.",
               "Common mistakes: 1/‖w‖ (that is the distance from the boundary to one margin hyperplane) "
               "or 2/‖w‖² — the bias b plays no role."]
    elif v == 1:
        m = _pick(rng, [0.5, 0.8, 1, 1.25, 2, 2.5, 4, 0.4])
        ans = (2 / m) ** 2
        d = 2
        text = (f"For a canonical hard-margin SVM (support vectors satisfy y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1), "
                f"the distance between the two margin hyperplanes is found to be {fmt(m)}. "
                f"The value of ‖w‖² is ______")
        sol = [f"Margin width 2/‖w‖ = {fmt(m)} ⇒ ‖w‖ = 2/{fmt(m)} = {fmt(2 / m, 4)}.",
               f"‖w‖² = <b>{fmt(ans, d)}</b>."]
    else:
        base = np.array(_pick(rng, [(1, 0), (0, 1), (1, 1), (1, 2), (2, 1), (3, 4), (1, -1), (2, -1)]), float)
        k = _pick(rng, [1, 2, 3])
        xn = rng.integers(-3, 4, size=2).astype(float)
        xp = xn + k * base
        dist = np.linalg.norm(xp - xn)
        ans = 2 / dist
        d = 3 if ans < 0.1 else 2
        text = (f"For a hard-margin linear SVM, the support vectors x<sub>+</sub> = {vec(xp)} (class +1) and "
                f"x<sub>−</sub> = {vec(xn)} (class −1) lie on the hyperplanes wᵀx + b = +1 and wᵀx + b = −1 "
                f"respectively, and the segment joining them is perpendicular to the decision boundary. "
                f"The value of ‖w‖ is ______")
        sol = [f"Since x<sub>+</sub> − x<sub>−</sub> = {vec(xp - xn)} is parallel to w, the margin width equals "
               f"‖x<sub>+</sub> − x<sub>−</sub>‖ = {fmt(dist, 4)}.",
               f"Margin = 2/‖w‖ ⇒ ‖w‖ = 2/{fmt(dist, 4)} = <b>{fmt(ans, d)}</b>.",
               "(Check: wᵀ(x<sub>+</sub> − x<sub>−</sub>) = 2 and w ∥ (x<sub>+</sub> − x<sub>−</sub>) give the same "
               "result.)"]
    return Q(text=text + " " + nat_hint(d), qtype="NAT", marks=1, answer=nat_range(ans, d), nat_hint=nat_hint(d),
             solution=sol)


@template(TOPIC, S_MARGIN, marks=1, qtype="NAT")
def svm_point_distance(rng):
    v = int(rng.integers(4))
    w = np.array(_pick(rng, _PYTH), float)
    p = len(w)
    nw = np.linalg.norm(w)
    b = int(rng.integers(-9, 10))
    hyp = _lin_str(w, b) + " = 0"
    if v == 0:
        while True:
            x = rng.integers(-4, 5, size=p).astype(float)
            fx = w @ x + b
            if abs(fx) > 0.5:
                break
        ans = abs(fx) / nw
        text = f"The perpendicular distance of the point x = {vec(x)} from the hyperplane {hyp} is ______"
        sol = [f"Distance = |wᵀx + b| / ‖w‖, with w = {vec(w)}, b = {fmt(b)}.",
               f"wᵀx + b = {fmt(fx)}, ‖w‖ = {fmt(nw, 4)}.",
               f"Distance = {fmt(abs(fx))}/{fmt(nw, 4)} = <b>{fmt(ans, 2)}</b>."]
    elif v == 1:
        while b == 0:
            b = int(rng.integers(-9, 10))
        hyp = _lin_str(w, b) + " = 0"
        ans = abs(b) / nw
        text = f"The distance of the hyperplane {hyp} from the origin is ______"
        sol = [f"Distance of origin = |wᵀ0 + b|/‖w‖ = |b|/‖w‖ = {abs(b)}/{fmt(nw, 4)} = <b>{fmt(ans, 2)}</b>."]
    elif v == 2:
        b2 = b + int(rng.choice([-1, 1])) * int(rng.integers(2, 9))
        ans = abs(b - b2) / nw
        text = (f"The distance between the parallel hyperplanes {_lin_str(w, b)} = 0 and "
                f"{_lin_str(w, b2)} = 0 is ______")
        sol = [f"For wᵀx + b<sub>1</sub> = 0 and wᵀx + b<sub>2</sub> = 0, distance = |b<sub>1</sub> − "
               f"b<sub>2</sub>|/‖w‖.",
               f"= |{fmt(b)} − ({fmt(b2)})|/{fmt(nw, 4)} = {abs(b - b2)}/{fmt(nw, 4)} = <b>{fmt(ans, 2)}</b>."]
    else:
        while True:
            x = rng.integers(-4, 5, size=p).astype(float)
            fx = w @ x + b
            if abs(fx) > 0.5:
                break
        yv = int(rng.choice([-1, 1]))
        ans = yv * fx / nw
        text = (f"A linear classifier has decision boundary {hyp} (predict +1 when the left side is positive). "
                f"The <i>signed geometric margin</i> γ = y(wᵀx + b)/‖w‖ of the labelled example x = {vec(x)}, "
                f"y = {'+1' if yv > 0 else '−1'} is ______")
        sol = [f"Functional margin y(wᵀx + b) = ({'+1' if yv > 0 else '−1'})({fmt(fx)}) = {fmt(yv * fx)}.",
               f"‖w‖ = {fmt(nw, 4)}, so γ = {fmt(yv * fx)}/{fmt(nw, 4)} = <b>{fmt(ans, 2)}</b>.",
               "A negative value means the example is on the wrong side of the boundary (misclassified)."]
    return Q(text=text + " " + nat_hint(2), qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             solution=sol)


_STATUS = ["Correctly classified, on or outside the margin (ξ = 0)",
           "Correctly classified but strictly inside the margin (0 &lt; ξ &lt; 1)",
           "Exactly on the decision boundary (ξ = 1)",
           "Misclassified (ξ &gt; 1)"]


def _status_of(m):
    if m >= 1 - 1e-12:
        return 0
    if m > 1e-12:
        return 1
    if abs(m) <= 1e-12:
        return 2
    return 3


@template(TOPIC, S_SOFT, marks=1, qtype="MCQ")
def svm_point_status(rng):
    target = int(rng.choice(4, p=[0.25, 0.3, 0.15, 0.3]))
    while True:
        w = np.array(_pick(rng, [(1, 1), (2, 1), (1, -1), (0.5, 1), (1, 2), (2, -1), (0.5, 0.5), (1, 0.5)]))
        b = float(rng.integers(-4, 5))
        x = rng.integers(-3, 5, size=2).astype(float)
        yv = float(rng.choice([-1, 1]))
        m = yv * (w @ x + b)
        if _status_of(m) == target and abs(m) <= 4:
            break
    opts, a = mcq(rng, _STATUS[target], [s for s in _STATUS if s != _STATUS[target]])
    xi = max(0.0, 1 - m)
    return Q(text=f"A soft-margin linear SVM has learned f(x) = {_lin_str(w, b)}. For the training example "
                  f"x = {vec(x)} with label y = {'+1' if yv > 0 else '−1'}, which statement is CORRECT?",
             qtype="MCQ", marks=1, options=opts, answer=a,
             solution=[f"y·f(x) = ({'+1' if yv > 0 else '−1'})·({fmt(w @ x + b)}) = {fmt(m)}.",
                       f"Slack ξ = max(0, 1 − y f(x)) = {fmt(xi)}.",
                       "Rules: y f ≥ 1 ⇒ ξ = 0 (on/outside margin); 0 &lt; y f &lt; 1 ⇒ inside margin, still correct; "
                       "y f = 0 ⇒ on the boundary (ξ = 1); y f &lt; 0 ⇒ misclassified (ξ &gt; 1).",
                       f"Hence: <b>{_STATUS[target]}</b>."])


@template(TOPIC, S_DUAL, marks=1, qtype="NAT")
def svm_dual_constraint(rng):
    v = int(rng.integers(2))
    if v == 0:
        k = int(rng.integers(4, 6))
        while True:
            y = rng.choice([-1, 1], size=k)
            if len(set(y)) < 2:
                continue
            al = rng.integers(1, 16, size=k) / 10
            miss = int(rng.integers(k))
            val = -y[miss] * sum(al[i] * y[i] for i in range(k) if i != miss)
            if val > 0.05:
                break
        rows = [["i"] + [str(i + 1) for i in range(k)],
                ["y<sub>i</sub>"] + ["+1" if t > 0 else "−1" for t in y],
                ["α<sub>i</sub>"] + ["?" if i == miss else fmt(al[i]) for i in range(k)]]
        return Q(text=f"In the dual solution of a linear SVM, the non-zero Lagrange multipliers α<sub>i</sub> and "
                      f"labels y<sub>i</sub> of the support vectors are given below (all other α<sub>i</sub> = 0). "
                      f"The value of α<sub>{miss + 1}</sub> is ______ {nat_hint(1)}",
                 qtype="NAT", marks=1, answer=nat_range(val, 1, tol=0.01), nat_hint=nat_hint(1),
                 blocks=[Table(rows, header=False)],
                 solution=["Stationarity w.r.t. b gives the dual constraint Σ<sub>i</sub> α<sub>i</sub>y<sub>i</sub> = 0.",
                           "Σ<sub>i≠" + str(miss + 1) + "</sub> α<sub>i</sub>y<sub>i</sub> = "
                           + " ".join(("+ " if t > 0 else "− ") + fmt(al[i]) for i, t in enumerate(y) if i != miss)
                           + f" = {fmt(-y[miss] * val)}.",
                           f"So α<sub>{miss + 1}</sub>({'+1' if y[miss] > 0 else '−1'}) = {fmt(y[miss] * val)} ⇒ "
                           f"α<sub>{miss + 1}</sub> = <b>{fmt(val)}</b> (it must be ≥ 0)."])
    # w component
    while True:
        X = rng.integers(-2, 5, size=(3, 2)).astype(float)
        if len({tuple(r) for r in X}) < 3:
            continue
        y = np.array([1, 1, -1]) if rng.random() < 0.5 else np.array([1, -1, -1])
        y = y[rng.permutation(3)]
        al = rng.integers(1, 9, size=3) / 4
        al[2] = -y[2] * sum(al[i] * y[i] for i in range(2))  # enforce Σ α_i y_i = 0
        if al[2] <= 0:
            continue
        w = (al * y) @ X
        comp = int(rng.integers(2))
        if abs(w[comp]) > 0.2:
            break
    rows = [["i", "x<sub>i</sub>", "y<sub>i</sub>", "α<sub>i</sub>"]] + \
           [[str(i + 1), vec(X[i]), "+1" if y[i] > 0 else "−1", fmt(al[i])] for i in range(3)]
    terms = " + ".join(f"({fmt(al[i])})({'+1' if y[i] > 0 else '−1'})({fmt(X[i, comp])})" for i in range(3))
    return Q(text=f"A hard-margin SVM has exactly three support vectors with the optimal dual variables shown. "
                  f"The component w<sub>{comp + 1}</sub> of the optimal weight vector is ______ {nat_hint(2)}",
             qtype="NAT", marks=1, answer=nat_range(w[comp], 2), nat_hint=nat_hint(2),
             blocks=[Table(rows)],
             solution=["w = Σ<sub>i</sub> α<sub>i</sub> y<sub>i</sub> x<sub>i</sub> (sum over support vectors).",
                       f"w<sub>{comp + 1}</sub> = {terms} = <b>{fmt(w[comp], 2)}</b>.",
                       f"(Full vector w = {vec(w)}; note Σα<sub>i</sub>y<sub>i</sub> = 0 holds.)"])


@template(TOPIC, S_KER, marks=1, qtype="NAT")
def kernel_poly_value(rng):
    while True:
        p = int(rng.integers(2, 4))
        x = rng.integers(-2, 4, size=p)
        z = rng.integers(-2, 4, size=p)
        c = int(_pick(rng, [0, 1, 1, 2]))
        d = int(_pick(rng, [2, 2, 3]))
        v = int(rng.integers(3))
        if v == 2:
            z = x
        base = int(x @ z) + c
        val = base ** d
        if 0 < abs(val) <= 3000 and base != 0 and int(x @ z) != 0:
            break
    kstr = f"(xᵀz + {c})<super>{d}</super>" if c else f"(xᵀz)<super>{d}</super>"
    what = "K(x, x)" if v == 2 else "K(x, z)"
    return Q(text=f"Consider the polynomial kernel K(x, z) = {kstr} with x = {vec(x)} and z = {vec(z)}. "
                  f"The value of {what} is ______ {nat_hint(0)}",
             qtype="NAT", marks=1, answer=(val, val), nat_hint=nat_hint(0),
             solution=[("xᵀx = " if v == 2 else "xᵀz = ") + " + ".join(
                 f"({a})({bb})" for a, bb in zip(x, z)) + f" = {int(x @ z)}.",
                       f"{what} = ({int(x @ z)} + {c})<super>{d}</super> = {base}<super>{d}</super> = <b>{val}</b>.",
                       "The kernel equals the inner product φ(x)ᵀφ(z) of the explicit (all-monomials-up-to-degree-d) "
                       "feature maps, without forming φ."])


@template(TOPIC, S_KER, marks=1, qtype="NAT")
def kernel_rbf_value(rng):
    v = int(rng.integers(3))
    while True:
        p = int(rng.integers(2, 4))
        x = rng.integers(-2, 3, size=p).astype(float)
        z = x + rng.integers(-2, 3, size=p)
        d2 = float(((x - z) ** 2).sum())
        if d2 > 0:
            break
    if v == 0:
        while True:
            g = _pick(rng, [0.05, 0.1, 0.2, 0.25, 0.5, 1.0])
            ans = math.exp(-g * d2)
            if ans > 0.01:
                break
        text = (f"The RBF (Gaussian) kernel is K(x, z) = exp(−γ‖x − z‖²) with γ = {fmt(g)}. For x = {vec(x)} and "
                f"z = {vec(z)}, the value of K(x, z) is ______ {nat_hint(3)}")
        sol = [f"‖x − z‖² = {' + '.join(fmt(t * t) for t in (x - z))} = {fmt(d2)}.",
               f"K = exp(−{fmt(g)} × {fmt(d2)}) = exp(−{fmt(g * d2, 3)}) = <b>{fmt(ans, 3)}</b>."]
        d = 3
    elif v == 1:
        while True:
            sg = _pick(rng, [1, 1.5, 2, 3])
            ans = math.exp(-d2 / (2 * sg * sg))
            if ans > 0.01:
                break
        text = (f"The Gaussian kernel is K(x, z) = exp(−‖x − z‖²/(2σ²)) with σ = {fmt(sg)}. For x = {vec(x)} and "
                f"z = {vec(z)}, the value of K(x, z) is ______ {nat_hint(3)}")
        sol = [f"‖x − z‖² = {fmt(d2)};  2σ² = {fmt(2 * sg * sg)}.",
               f"K = exp(−{fmt(d2)}/{fmt(2 * sg * sg)}) = <b>{fmt(ans, 3)}</b>."]
        d = 3
    else:
        target = _pick(rng, [0.5, 0.25, 0.1, 0.8])
        ans = -math.log(target) / d2
        d = 3
        text = (f"For the RBF kernel K(x, z) = exp(−γ‖x − z‖²), with x = {vec(x)} and z = {vec(z)}, the value of γ "
                f"for which K(x, z) = {fmt(target)} is ______ {nat_hint(3)}")
        sol = [f"‖x − z‖² = {fmt(d2)}.",
               f"exp(−γ·{fmt(d2)}) = {fmt(target)} ⇒ γ = −ln({fmt(target)})/{fmt(d2)} = {fmt(-math.log(target), 4)}/"
               f"{fmt(d2)} = <b>{fmt(ans, 3)}</b>."]
    sol.append("Note: K ∈ (0, 1], K(x, x) = 1, and K decreases as the points move apart or as γ grows.")
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, d, tol=0.002), nat_hint=nat_hint(d), solution=sol)


@template(TOPIC, S_KER, marks=1, qtype="NAT")
def kernel_poly_dimension(rng):
    v = int(rng.integers(3))
    p = int(rng.integers(2, 7))
    d = int(rng.integers(2, 5))
    if v == 0:
        ans = math.comb(p + d, d)
        text = (f"The inhomogeneous polynomial kernel K(x, z) = (xᵀz + 1)<super>{d}</super> on x ∈ ℝ<super>{p}</super> "
                f"corresponds to an explicit feature map containing all monomials of degree at most {d}. "
                f"The dimension of this feature space is ______")
        sol = [f"Number of monomials of degree ≤ d in p variables = C(p + d, d).",
               f"C({p} + {d}, {d}) = C({p + d}, {d}) = <b>{ans}</b>."]
    elif v == 1:
        ans = math.comb(p + d - 1, d)
        text = (f"The homogeneous polynomial kernel K(x, z) = (xᵀz)<super>{d}</super> on x ∈ ℝ<super>{p}</super> "
                f"corresponds to a feature map of all (scaled) monomials of degree exactly {d}. "
                f"The number of distinct such features is ______")
        sol = [f"Monomials of degree exactly d in p variables = C(p + d − 1, d) (stars and bars).",
               f"C({p + d - 1}, {d}) = <b>{ans}</b>.",
               f"(Including all lower degrees, as for (xᵀz + 1)<super>{d}</super>, would give C({p + d}, {d}) = "
               f"{math.comb(p + d, d)}.)"]
    else:
        p = int(rng.integers(2, 6))
        ans = math.comb(p + 2, 2)
        text = (f"For x ∈ ℝ<super>{p}</super>, the quadratic kernel K(x, z) = (1 + xᵀz)² equals φ(x)ᵀφ(z) for a "
                f"feature map φ containing a constant, the linear terms, the squares and the pairwise cross terms "
                f"(with √2 scaling). The length of φ(x) is ______")
        sol = [f"Constant: 1; linear: {p}; squares: {p}; cross terms: C({p}, 2) = {math.comb(p, 2)}.",
               f"Total = 1 + {p} + {p} + {math.comb(p, 2)} = <b>{ans}</b> = C({p} + 2, 2)."]
    return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(ans, ans), nat_hint=nat_hint(0),
             solution=sol)


# --- statement pools ---------------------------------------------------------
_SVM_T = [
    ("For a canonical hard-margin SVM (min<sub>i</sub> y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1), the margin width is 2/‖w‖.",
     "Each margin hyperplane is at distance 1/‖w‖ from the boundary."),
    ("Removing a training point that is not a support vector does not change the hard-margin SVM solution.",
     "Non-support vectors have α<sub>i</sub> = 0 and inactive constraints."),
    ("In the hard-margin SVM, α<sub>i</sub> &gt; 0 only for points lying on the hyperplanes wᵀx + b = ±1.",
     "Complementary slackness: α<sub>i</sub>[y<sub>i</sub>(wᵀx<sub>i</sub>+b) − 1] = 0."),
    ("The optimal weight vector of an SVM can be written as w = Σ α<sub>i</sub> y<sub>i</sub> x<sub>i</sub>.",
     "From ∂L/∂w = 0 in the Lagrangian."),
    ("The dual variables of the SVM satisfy Σ α<sub>i</sub> y<sub>i</sub> = 0.", "From ∂L/∂b = 0."),
    ("The XOR data set in ℝ² is not linearly separable, but becomes separable after adding the feature x₁x₂.",
     "The sign of x₁x₂ is exactly the XOR label (with ±1 coding)."),
    ("The hard-margin SVM primal is a convex quadratic program, so its optimal w is unique.",
     "Strictly convex objective ½‖w‖² over a convex feasible set."),
    ("Scaling (w, b) by a positive constant does not change the decision boundary.",
     "{x : wᵀx + b = 0} is unchanged by positive scaling."),
    ("The hinge loss max(0, 1 − y f(x)) is a convex upper bound on the 0–1 loss.",
     "It is ≥ 1 whenever y f(x) ≤ 0 and is a maximum of affine functions."),
    ("The logistic loss log(1 + e<super>−y f(x)</super>) is strictly positive for every finite f(x).",
     "Unlike hinge loss, it never becomes exactly zero."),
    ("A standard SVM does not directly output calibrated class probabilities, unlike logistic regression.",
     "SVM outputs a score; probabilities need extra calibration (e.g. Platt scaling)."),
    ("In the SVM dual, the training data enter only through inner products x<sub>i</sub>ᵀx<sub>j</sub>.",
     "This is what makes the kernel trick possible."),
    ("The kernel trick computes inner products in a feature space without explicitly constructing φ(x).",
     "K(x, z) = φ(x)ᵀφ(z) is evaluated directly."),
    ("A kernel SVM predicts with f(x) = Σ α<sub>i</sub> y<sub>i</sub> K(x<sub>i</sub>, x) + b, where only support "
     "vectors contribute.", "α<sub>i</sub> = 0 for all other points."),
    ("A hard-margin linear SVM has a feasible solution only if the training data are linearly separable.",
     "Otherwise the constraints y<sub>i</sub>(wᵀx<sub>i</sub>+b) ≥ 1 cannot all hold."),
    ("The functional margin y<sub>i</sub>(wᵀx<sub>i</sub> + b) is positive if and only if point i is correctly "
     "classified.", "Its sign compares the prediction with the label."),
    ("The geometric margin of a point equals its functional margin divided by ‖w‖.",
     "That normalisation makes it invariant to scaling (w, b)."),
    ("The RBF kernel corresponds to an infinite-dimensional feature space.",
     "Its Taylor expansion contains monomials of every degree."),
    ("Without kernels, both the SVM and logistic regression produce linear (hyperplane) decision boundaries.",
     "Both threshold an affine score wᵀx + b."),
    ("For separable data the hard-margin SVM boundary is equidistant from the nearest positive and the nearest "
     "negative training points.", "Both classes' support vectors are at distance 1/‖w‖."),
    ("Hinge loss is zero for a correctly classified point with y f(x) ≥ 1, so such points do not affect the SVM "
     "solution.", "They contribute neither loss nor gradient."),
    ("Logistic regression is influenced by all training points, while the SVM solution depends only on support "
     "vectors.", "Log-loss gradient is non-zero for every point."),
]
_SVM_F = [
    ("Every training point contributes a non-zero term to w in the SVM solution.",
     "Only support vectors have α<sub>i</sub> &gt; 0."),
    ("The margin width of the canonical hard-margin SVM is 1/‖w‖².", "It is 2/‖w‖."),
    ("Moving a non-support-vector point (keeping it strictly outside the margin) changes the SVM boundary.",
     "Its constraint stays inactive, so the solution is unchanged."),
    ("The XOR problem can be solved by a hard-margin linear SVM in the original 2-D input space.",
     "XOR is not linearly separable; a kernel/feature map is needed."),
    ("The SVM dual requires Σ α<sub>i</sub> = 0.", "The constraint is Σ α<sub>i</sub>y<sub>i</sub> = 0, with α<sub>i</sub> ≥ 0."),
    ("In the hard-margin SVM dual, some α<sub>i</sub> may be negative at the optimum.",
     "Lagrange multipliers of inequality constraints satisfy α<sub>i</sub> ≥ 0."),
    ("Logistic-regression loss becomes exactly zero for every point with y f(x) ≥ 1.",
     "That property belongs to the hinge loss."),
    ("SVM training maximises the likelihood of the training labels.",
     "SVM maximises the margin (minimises regularised hinge loss); it is not a likelihood method."),
    ("Doubling both w and b doubles the geometric margin of every point.",
     "Functional margin doubles; geometric margin is unchanged."),
    ("The hinge loss is differentiable everywhere.", "It has a kink at y f(x) = 1."),
    ("A kernel SVM must explicitly compute φ(x) for every training point.", "The kernel trick avoids this."),
    ("The number of support vectors of a hard-margin SVM always equals the input dimension plus one.",
     "It depends on the data (it can be as few as 2)."),
    ("Support vectors are the training points farthest from the decision boundary.", "They are the closest ones."),
    ("The SVM primal objective is non-convex, so different initialisations give different solutions.",
     "It is a convex QP."),
    ("The hard-margin SVM attains zero training error even on non-separable data.",
     "On non-separable data the hard-margin problem is infeasible."),
    ("A point with functional margin y(wᵀx + b) = 0.5 is misclassified.",
     "It is on the correct side (positive), only inside the margin."),
    ("The bias b of a hard-margin SVM can be computed as b = y<sub>i</sub> − wᵀx<sub>i</sub> from any training point.",
     "Only valid for support vectors (points on the margin)."),
    ("Maximising the SVM margin is equivalent to maximising ‖w‖.", "The margin 2/‖w‖ is maximised by minimising ‖w‖."),
    ("Logistic regression can never produce a linear decision boundary.",
     "Its boundary wᵀx + b = 0 is linear."),
    ("Adding a polynomial kernel can never make a non-separable data set separable.",
     "Mapping to higher dimensions (e.g. XOR with x₁x₂) can make it separable."),
]

_SOFT_T = [
    ("Increasing C penalises slack more heavily and typically gives a narrower margin with fewer margin violations.",
     "Large C trades margin width for training fit."),
    ("As C → ∞, the soft-margin SVM approaches the hard-margin SVM on separable data.",
     "Any slack becomes infinitely costly."),
    ("A small C allows more margin violations and typically yields a wider margin.",
     "Small C ⇒ stronger regularisation."),
    ("At the optimum, ξ<sub>i</sub> = max(0, 1 − y<sub>i</sub>(wᵀx<sub>i</sub> + b)).",
     "Slack equals the hinge loss of the point."),
    ("A point with 0 &lt; ξ<sub>i</sub> &lt; 1 is correctly classified but lies inside the margin.",
     "0 &lt; y f &lt; 1."),
    ("A point with ξ<sub>i</sub> &gt; 1 is misclassified.", "y f = 1 − ξ &lt; 0."),
    ("A point with ξ<sub>i</sub> = 1 lies exactly on the decision boundary.", "y f(x) = 0."),
    ("Σ ξ<sub>i</sub> is an upper bound on the number of misclassified training points.",
     "Each misclassified point has ξ<sub>i</sub> &gt; 1."),
    ("In the soft-margin dual the multipliers satisfy the box constraint 0 ≤ α<sub>i</sub> ≤ C.",
     "C caps the influence of any single point."),
    ("Points with 0 &lt; α<sub>i</sub> &lt; C lie exactly on the margin (ξ<sub>i</sub> = 0).",
     "KKT: α<sub>i</sub> &lt; C ⇒ ξ<sub>i</sub> = 0, and α<sub>i</sub> &gt; 0 ⇒ y f = 1 − ξ."),
    ("Points with α<sub>i</sub> = C may lie inside the margin or be misclassified.", "Bound support vectors."),
    ("Soft-margin SVM is equivalent to minimising Σ max(0, 1 − y<sub>i</sub>f(x<sub>i</sub>)) + λ‖w‖² with λ = 1/(2C).",
     "Divide ½‖w‖² + CΣξ by C."),
    ("Small C corresponds to higher bias/lower variance; large C to lower bias/higher variance.",
     "C acts like an inverse regularisation strength."),
    ("Points correctly classified and strictly outside the margin have α<sub>i</sub> = 0.",
     "Complementary slackness."),
    ("The hyper-parameter C is usually chosen by cross-validation.", "It controls the bias–variance trade-off."),
    ("The soft-margin SVM has a solution even when the data are not linearly separable.",
     "Slack variables make the problem always feasible."),
    ("A point lying exactly on the margin (y f(x) = 1) incurs zero hinge loss.", "max(0, 1 − 1) = 0."),
]
_SOFT_F = [
    ("Increasing C always widens the margin.", "Increasing C typically narrows it."),
    ("A point with ξ<sub>i</sub> = 0.5 is misclassified.", "It has y f = 0.5 &gt; 0 — correct but inside the margin."),
    ("Slack variables ξ<sub>i</sub> can be negative for points far from the boundary.", "ξ<sub>i</sub> ≥ 0 by definition."),
    ("With C = 0 the soft-margin SVM coincides with the hard-margin SVM.",
     "C = 0 ignores the data entirely (w = 0); hard margin is C → ∞."),
    ("In the soft-margin dual, α<sub>i</sub> is unbounded above as in the hard-margin case.", "0 ≤ α<sub>i</sub> ≤ C."),
    ("Σ ξ<sub>i</sub> equals the number of misclassified training points.", "It is only an upper bound."),
    ("A small C makes the SVM more prone to overfitting than a large C.", "It is the other way round."),
    ("Points with α<sub>i</sub> = 0 are support vectors.", "Support vectors are those with α<sub>i</sub> &gt; 0."),
    ("A point lying exactly on the margin (y f(x) = 1) incurs a positive hinge loss.", "Hinge loss is 0 there."),
    ("The hinge loss of every correctly classified point is zero.",
     "Correct points inside the margin (0 &lt; y f &lt; 1) have positive loss."),
    ("The soft-margin SVM is infeasible if the data are not linearly separable.", "Slack makes it always feasible."),
    ("The slack of a misclassified point is less than 1.", "Misclassified ⇒ y f &lt; 0 ⇒ ξ &gt; 1."),
    ("In the primal ½‖w‖² + C Σξ<sub>i</sub>, the constant C multiplies ‖w‖².", "C multiplies the total slack."),
    ("Increasing C increases the regularisation strength.", "Larger C means weaker regularisation."),
    ("Every point strictly inside the margin has α<sub>i</sub> = 0.", "Such points have α<sub>i</sub> = C."),
    ("The soft-margin SVM objective is non-convex because of the slack variables.",
     "Objective and constraints remain convex (a QP)."),
]

_KER_T = [
    ("If k₁ and k₂ are valid kernels, k₁ + k₂ is a valid kernel.", "Sum of PSD Gram matrices is PSD."),
    ("If k₁ and k₂ are valid kernels, the product k₁·k₂ is a valid kernel.", "Schur product theorem."),
    ("If k is valid and c &gt; 0, then c·k is valid.", "Positive scaling preserves PSD."),
    ("If k is valid, f(x)k(x, z)f(z) is valid for any real function f.", "Gram matrix D K D with D diagonal."),
    ("If k is valid, exp(k(x, z)) is valid.", "Limit of polynomials with non-negative coefficients."),
    ("(xᵀz + c)<super>d</super> with c ≥ 0 and positive integer d is a valid kernel.", "Products and sums of valid kernels."),
    ("exp(−γ‖x − z‖²) with γ &gt; 0 is a valid kernel.", "The Gaussian/RBF kernel."),
    ("k(x, z) = xᵀAz is a valid kernel when A is symmetric positive semidefinite.", "φ(x) = A<super>1/2</super>x."),
    ("Every valid kernel yields a symmetric PSD Gram matrix for any finite set of points.", "Mercer's condition."),
    ("k(x, x) ≥ 0 for every valid kernel.", "k(x, x) = ‖φ(x)‖²."),
    ("|k(x, z)| ≤ √(k(x, x)·k(z, z)) for every valid kernel.", "Cauchy–Schwarz in feature space."),
    ("For the RBF kernel, k(x, x) = 1 for every x.", "exp(0) = 1."),
    ("Any function of the form k(x, z) = φ(x)ᵀφ(z) is a valid kernel.", "Gram matrix = ΦΦᵀ is PSD."),
    ("k(x, z) = f(x)f(z) is valid for any real-valued f.", "Rank-one PSD Gram matrix."),
    ("The linear kernel k(x, z) = xᵀz is valid.", "φ(x) = x."),
    ("k(x, z) = xᵀz + c with c ≥ 0 is a valid kernel.", "Sum of the linear kernel and a constant kernel."),
    ("p(k(x, z)) is valid for any polynomial p with non-negative coefficients when k is valid.",
     "Sums, products and positive scalings."),
]
_KER_F = [
    ("If k₁ and k₂ are valid kernels, k₁ − k₂ is always a valid kernel.", "The difference may have negative eigenvalues."),
    ("If k is a valid (non-zero) kernel, −k is also valid.", "−K has a negative diagonal entry somewhere."),
    ("k(x, z) = ‖x − z‖² is a valid kernel.", "Its Gram matrix has zero diagonal and positive off-diagonal ⇒ det &lt; 0."),
    ("The Gram matrix of a valid kernel can have a negative eigenvalue.", "It must be PSD."),
    ("If k is valid, c·k is valid for every c &lt; 0.", "Negative scaling breaks PSD."),
    ("k(x, z) = xᵀAz is a valid kernel for every square matrix A.", "A must be symmetric PSD."),
    ("Mercer's condition requires every entry of the Gram matrix to be positive.",
     "It requires PSD; entries may be negative (e.g. linear kernel)."),
    ("The Gram matrix of an RBF kernel can have diagonal entries larger than 1.", "All diagonal entries equal 1."),
    ("k(x, z) = (xz − 1)² is a valid kernel on ℝ.",
     "For points 0 and 1 the Gram matrix [[1, 1], [1, 0]] has determinant −1."),
    ("A valid kernel must satisfy k(x, z) ≥ 0 for all x, z.", "The linear kernel takes negative values."),
    ("The polynomial kernel (xᵀz + 1)<super>d</super> corresponds to an infinite-dimensional feature space.",
     "Its feature space has dimension C(p + d, d)."),
    ("The RBF kernel corresponds to a finite-dimensional feature map.", "It is infinite-dimensional."),
    ("k(x, z) = −xᵀz is a valid kernel.", "k(x, x) = −‖x‖² &lt; 0."),
    ("k(x, z) = exp(+γ‖x − z‖²) with γ &gt; 0 is a valid kernel.",
     "For two distinct points det [[1, e<super>γd²</super>], [e<super>γd²</super>, 1]] &lt; 0."),
    ("Any symmetric function whose Gram matrices have positive diagonals is a valid kernel.",
     "Positive diagonal is necessary, not sufficient (need PSD)."),
]


@template(TOPIC, S_DUAL, marks=1, qtype="MSQ")
def svm_concepts_msq(rng):
    opts, ans, expl = msq_from_statements(rng, _SVM_T, _SVM_F)
    return Q(text="Which of the following statements about support vector machines is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_SOFT, marks=1, qtype="MSQ")
def svm_soft_margin_msq(rng):
    opts, ans, expl = msq_from_statements(rng, _SOFT_T, _SOFT_F)
    return Q(text="Consider the soft-margin SVM: minimise ½‖w‖² + C Σ<sub>i</sub> ξ<sub>i</sub> subject to "
                  "y<sub>i</sub>(wᵀx<sub>i</sub> + b) ≥ 1 − ξ<sub>i</sub>, ξ<sub>i</sub> ≥ 0. "
                  "Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_KER, marks=1, qtype="MSQ")
def kernel_validity_msq(rng):
    opts, ans, expl = msq_from_statements(rng, _KER_T, _KER_F)
    return Q(text="Which of the following statements about kernel functions (Mercer kernels) is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# =============================================================================
# SVM — 2 marks
# =============================================================================
def _svm_geom_solution(X, y, w, b, m, sv):
    names = ", ".join(f"P{i + 1}" for i in sv)
    out = []
    if len(sv) == 2:
        i, j = sv
        out.append(f"The closest pair of opposite-class points is P{i + 1} = {vec(X[i])} and P{j + 1} = {vec(X[j])}, "
                   f"Their perpendicular bisector separates the classes and no other point comes closer to it, so "
                   f"Hence w ∥ (x<sub>+</sub> − x<sub>−</sub>) and the support vectors are {names}.")
    else:
        cls = [i for i in sv if sum(1 for j in sv if y[j] == y[i]) == 2]
        oth = [i for i in sv if i not in cls]
        out.append(f"P{cls[0] + 1} and P{cls[1] + 1} (same class) lie on one margin line and P{oth[0] + 1} on the "
                   f"other; the optimal boundary is parallel to the line through P{cls[0] + 1}, P{cls[1] + 1}, "
                   f"midway to P{oth[0] + 1}. Support vectors: {names}.")
    out.append(f"Scaling so that y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1 at the support vectors gives "
               f"w = ({_q(w[0])}, {_q(w[1])}), b = {_q(b)}; ‖w‖ = {fmt(np.linalg.norm(w), 4)}, margin 2/‖w‖ = "
               f"{fmt(m, 4)}.")
    return out


def _margins_table(X, y, w, b):
    vals = y * (X @ w + b)
    return Table([["Point"] + [f"P{i + 1}" for i in range(len(y))],
                  ["y(wᵀx + b)"] + [fmt(v, 3) for v in vals]], header=True)


@template(TOPIC, S_MARGIN, marks=2, qtype="NAT")
def svm_max_margin(rng):
    npos, nneg = int(rng.integers(3, 5)), int(rng.integers(3, 5))
    X, y, w, b, m, sv, a = _gen_svm(rng, npos, nneg)
    v = int(rng.integers(3))
    while True:
        t = rng.integers(0, 7, size=2).astype(float)
        if not any((X == t).all(1)):
            break
    ft = w @ t + b
    if v == 0:
        ask, ans = "the width of the margin (distance between the two margin hyperplanes)", m
    elif v == 1:
        ask, ans = "‖w‖ for the canonical solution (support vectors satisfy y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1)", \
            float(np.linalg.norm(w))
    else:
        ask, ans = (f"the value of the canonical decision function f(x) = wᵀx + b (support vectors satisfy "
                    f"y<sub>i</sub>f(x<sub>i</sub>) = 1) at the test point x = {vec(t)}"), float(ft)

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y)

    sol = _svm_geom_solution(X, y, w, b, m, sv)
    sol.append(_margins_table(X, y, w, b))
    sol.append("All values are ≥ 1 (feasible), with equality exactly at the support vectors.")
    if v == 0:
        sol.append(f"Margin width = 2/‖w‖ = <b>{fmt(ans, 2)}</b>.")
    elif v == 1:
        sol.append(f"‖w‖ = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"f({vec(t)}) = {_eval_str(w, t, b)} = <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"The labelled training points shown below are linearly separable. A hard-margin linear SVM is "
                  f"trained on them. Compute {ask}. {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_pts_table(X, y), Figure(draw, 8.5, 6)], solution=sol)


@template(TOPIC, S_DUAL, marks=2, qtype="MSQ")
def svm_support_vectors(rng):
    npos, nneg = int(rng.integers(3, 5)), int(rng.integers(3, 5))
    X, y, w, b, m, sv, a = _gen_svm(rng, npos, nneg)
    n = len(y)
    marg = y * (X @ w + b)
    non = [i for i in np.argsort(marg) if i not in sv]
    k_non = 4 - len(sv)
    chosen = sorted(list(sv) + non[:k_non])
    opts = [f"P{i + 1}" for i in chosen]
    ans = [j for j, i in enumerate(chosen) if i in sv]

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y)

    sol = _svm_geom_solution(X, y, w, b, m, sv)
    sol.append(_margins_table(X, y, w, b))
    sol.append("Support vectors are exactly the points with y<sub>i</sub>(wᵀx<sub>i</sub> + b) = 1 "
               "(α<sub>i</sub> &gt; 0): " + ", ".join(f"<b>P{i + 1}</b>" for i in sv) + ".")
    sol.append("Dual check: α = (" + ", ".join(f"α<sub>{i + 1}</sub> = {_q(v)}" for i, v in zip(sv, a)) +
               ") satisfy Σα<sub>i</sub>y<sub>i</sub> = 0 and Σα<sub>i</sub>y<sub>i</sub>x<sub>i</sub> = w.")
    return Q(text=f"A hard-margin linear SVM is trained on the {n} labelled points shown. Which of the following "
                  f"points is/are support vectors of the resulting maximum-margin classifier?",
             qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[_pts_table(X, y), Figure(draw, 8.5, 6)],
             solution=sol)


@template(TOPIC, S_DUAL, marks=2, qtype="NAT")
def svm_dual_to_primal(rng):
    npos, nneg = int(rng.integers(2, 4)), int(rng.integers(2, 4))
    X, y, w, b, m, sv, a = _gen_svm(rng, npos, nneg, nice_alpha=True)
    alpha = np.zeros(len(y))
    alpha[sv] = a
    v = int(rng.integers(4))
    while True:
        t = rng.integers(0, 7, size=2).astype(float)
        if not any((X == t).all(1)):
            break
    ft = float(w @ t + b)
    if v == 0:
        ask, ans = f"the bias b", float(b)
    elif v == 1:
        ask, ans = f"the decision value f(x) = wᵀx + b at x = {vec(t)}", ft
    elif v == 2:
        ask, ans = "the margin width 2/‖w‖", float(m)
    else:
        c = int(rng.integers(2))
        ask, ans = f"the weight component w<sub>{c + 1}</sub>", float(w[c])
    s0 = sv[0]
    terms1 = " + ".join(f"({fmt(alpha[i], 3)})({'+1' if y[i] > 0 else '−1'}){vec(X[i])}" for i in sv)
    sol = ["w = Σ α<sub>i</sub>y<sub>i</sub>x<sub>i</sub> over points with α<sub>i</sub> &gt; 0:",
           f"w = {terms1} = ({_q(w[0])}, {_q(w[1])}).",
           f"b from any support vector, e.g. P{s0 + 1}: y = wᵀx + b ⇒ b = {'+1' if y[s0] > 0 else '−1'} − "
           f"({fmt(w @ X[s0], 3)}) = {_q(b)}.",
           f"Check: Σα<sub>i</sub>y<sub>i</sub> = {fmt(float(alpha @ y), 3)} (= 0, as required)."]
    if v == 1:
        sol.append(f"f({vec(t)}) = {_eval_str(w, t, b)} = <b>{fmt(ans, 2)}</b>.")
    elif v == 2:
        sol.append(f"‖w‖ = {fmt(np.linalg.norm(w), 4)} ⇒ margin = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y, test=t if v == 1 else None)

    return Q(text=f"A hard-margin linear SVM is trained on the points below. Solving the dual problem gives the "
                  f"Lagrange multipliers α<sub>i</sub> listed in the table. Using the KKT conditions, compute {ask}. "
                  f"{nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_pts_table(X, y, [fmt(v_, 3) for v_ in alpha], "α<sub>i</sub>"), Figure(draw, 8, 5.6)],
             solution=sol)


def _gen_soft(rng, n=5):
    while True:
        w = np.array(_pick(rng, [(1, 1), (1, -1), (2, 1), (1, 2), (0.5, 1), (1, 0.5), (2, -1), (1, 0), (0, 1)]),
                     float)
        b = float(rng.integers(-6, 1)) if w.sum() > 0 else float(rng.integers(-3, 4))
        X = rng.integers(0, 6, size=(n, 2)).astype(float)
        if len({tuple(r) for r in X}) < n:
            continue
        f = X @ w + b
        y = np.sign(f)
        flip = rng.random(n) < 0.3
        y[flip] *= -1
        if (f == 0).any():
            continue
        m = y * f
        cats = [_status_of(v) for v in m]
        if 0 in cats and 1 in cats and 3 in cats and (np.abs(m) <= 4).all():
            return X, y, w, b, m


@template(TOPIC, S_SOFT, marks=2, qtype="NAT")
def svm_hinge_objective(rng):
    X, y, w, b, m = _gen_soft(rng, int(rng.integers(5, 7)))
    xi = np.maximum(0, 1 - m)
    v = int(rng.integers(3))
    if v == 0:
        ans = float(xi.sum())
        ask = "the total hinge loss Σ<sub>i</sub> max(0, 1 − y<sub>i</sub>f(x<sub>i</sub>))"
        last = f"Σξ<sub>i</sub> = <b>{fmt(ans, 2)}</b>."
    elif v == 1:
        C = _pick(rng, [0.5, 1, 2, 5, 10])
        ans = 0.5 * float(w @ w) + C * float(xi.sum())
        ask = f"the value of the soft-margin primal objective ½‖w‖² + C Σ<sub>i</sub> ξ<sub>i</sub> with C = {fmt(C)} " \
              f"(using the optimal slacks for this (w, b))"
        last = f"½‖w‖² = {fmt(0.5 * w @ w, 3)}; objective = {fmt(0.5 * w @ w, 3)} + {fmt(C)} × {fmt(xi.sum(), 3)} = " \
               f"<b>{fmt(ans, 2)}</b>."
    else:
        ans = float(xi.mean())
        ask = "the average hinge loss (1/n) Σ<sub>i</sub> max(0, 1 − y<sub>i</sub>f(x<sub>i</sub>))"
        last = f"Average = {fmt(xi.sum(), 3)}/{len(y)} = <b>{fmt(ans, 2)}</b>."

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y, hi=5, lines=[(w, b, 0, "-"), (w, b, 1, "--"), (w, b, -1, "--")])

    rows = [["Point", "x", "y", "f(x)", "y f(x)", "ξ = max(0, 1 − y f)"]]
    for i in range(len(y)):
        rows.append([f"P{i + 1}", vec(X[i]), "+1" if y[i] > 0 else "−1", fmt(X[i] @ w + b, 3), fmt(m[i], 3),
                     fmt(xi[i], 3)])
    return Q(text=f"A linear SVM with f(x) = {_lin_str(w, b)} is evaluated on the training points in the table "
                  f"(also plotted, with the boundary f = 0 solid and f = ±1 dashed). Compute {ask}. {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_pts_table(X, y), Figure(draw, 8.5, 6)],
             solution=["Compute f(x<sub>i</sub>), the functional margin y<sub>i</sub>f(x<sub>i</sub>) and the "
                       "slack/hinge loss for each point:", Table(rows), last,
                       "Points with y f ≥ 1 contribute 0; points inside the margin contribute between 0 and 1; "
                       "misclassified points contribute more than 1."])


@template(TOPIC, S_SOFT, marks=2, qtype="MSQ")
def svm_slack_msq(rng):
    X, y, w, b, m = _gen_soft(rng, int(rng.integers(5, 7)))
    xi = np.maximum(0, 1 - m)
    T, F = [], []
    for i in range(len(y)):
        cat = _status_of(m[i])
        ex = f"y f = {fmt(m[i], 3)} ⇒ ξ = {fmt(xi[i], 3)}."
        s_on = (f"P{i + 1} has slack ξ<sub>{i + 1}</sub> = 0.", ex)
        s_in = (f"P{i + 1} is correctly classified but lies strictly inside the margin.", ex)
        s_mis = (f"P{i + 1} is misclassified (ξ<sub>{i + 1}</sub> &gt; 1).", ex)
        (T if cat == 0 else F).append(s_on)
        (T if cat == 1 else F).append(s_in)
        (T if cat == 3 else F).append(s_mis)
    npos = int((xi > 0).sum())
    T.append((f"Exactly {npos} of the points have ξ<sub>i</sub> &gt; 0.", "Count of points with y f &lt; 1."))
    F.append((f"Exactly {npos + 1} of the points have ξ<sub>i</sub> &gt; 0.", f"The correct count is {npos}."))
    tot = xi.sum()
    T.append((f"Σ ξ<sub>i</sub> = {fmt(tot, 2)}.", "Sum of the individual slacks."))
    F.append((f"Σ ξ<sub>i</sub> = {fmt(tot + _pick(rng, [-1, 1, 0.5]), 2)}.", f"Σ ξ<sub>i</sub> = {fmt(tot, 2)}."))
    opts, ans, expl = msq_from_statements(rng, T, F)

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y, hi=5, lines=[(w, b, 0, "-"), (w, b, 1, "--"), (w, b, -1, "--")])

    rows = [["Point", "y f(x)", "ξ"]] + [[f"P{i + 1}", fmt(m[i], 3), fmt(xi[i], 3)] for i in range(len(y))]
    return Q(text=f"A soft-margin linear SVM has learned f(x) = {_lin_str(w, b)}. The training points are listed "
                  f"below and plotted (boundary solid, margins f = ±1 dashed). With ξ<sub>i</sub> the optimal slack "
                  f"of point i, which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[_pts_table(X, y), Figure(draw, 8.5, 6)],
             solution=["ξ<sub>i</sub> = max(0, 1 − y<sub>i</sub>f(x<sub>i</sub>)).", Table(rows)] + expl)


@template(TOPIC, S_KER, marks=2, qtype="NAT")
def kernel_feature_space(rng):
    v = int(rng.integers(3))
    while True:
        x = rng.integers(-2, 3, size=2).astype(float)
        z = rng.integers(-2, 3, size=2).astype(float)
        if not (x == z).all() and np.abs(x).sum() > 0 and np.abs(z).sum() > 0:
            break
    if v == 0:
        c = _pick(rng, [0, 1])
        K = lambda a, bb: (a @ bb + c) ** 2  # noqa: E731
        kxx, kzz, kxz = K(x, x), K(z, z), K(x, z)
        ans = kxx + kzz - 2 * kxz
        ks = f"(xᵀz + {c})²" if c else "(xᵀz)²"
        text = (f"Let φ be the feature map of the kernel K(x, z) = {ks} on ℝ², so that K(x, z) = φ(x)ᵀφ(z). "
                f"For x = {vec(x)} and z = {vec(z)}, the squared distance ‖φ(x) − φ(z)‖² in feature space is ______")
        sol = ["‖φ(x) − φ(z)‖² = K(x, x) + K(z, z) − 2K(x, z).",
               f"K(x, x) = ({fmt(x @ x)} + {c})² = {fmt(kxx)}, K(z, z) = ({fmt(z @ z)} + {c})² = {fmt(kzz)}, "
               f"K(x, z) = ({fmt(x @ z)} + {c})² = {fmt(kxz)}.",
               f"Squared distance = {fmt(kxx)} + {fmt(kzz)} − 2({fmt(kxz)}) = <b>{fmt(ans)}</b>."]
        d = 0
    elif v == 1:
        g = _pick(rng, [0.1, 0.2, 0.25, 0.5, 1])
        d2 = float(((x - z) ** 2).sum())
        k = math.exp(-g * d2)
        ans = math.sqrt(2 - 2 * k)
        text = (f"For the RBF kernel K(x, z) = exp(−γ‖x − z‖²) with γ = {fmt(g)}, let φ be its (infinite-"
                f"dimensional) feature map. For x = {vec(x)} and z = {vec(z)}, the Euclidean distance "
                f"‖φ(x) − φ(z)‖ in feature space is ______")
        sol = ["‖φ(x) − φ(z)‖² = K(x, x) + K(z, z) − 2K(x, z) = 2 − 2K(x, z) for the RBF kernel.",
               f"‖x − z‖² = {fmt(d2)}, K(x, z) = exp(−{fmt(g * d2, 3)}) = {fmt(k, 4)}.",
               f"Distance = √(2 − 2 × {fmt(k, 4)}) = <b>{fmt(ans, 2)}</b> (always below √2 ≈ 1.414)."]
        d = 2
    else:
        c = 1
        kxx, kzz, kxz = (x @ x + c) ** 2, (z @ z + c) ** 2, (x @ z + c) ** 2
        ans = kxz / math.sqrt(kxx * kzz)
        text = (f"For the kernel K(x, z) = (xᵀz + 1)² on ℝ² with feature map φ, compute the cosine of the angle between "
                f"φ(x) and φ(z), where x = {vec(x)} and z = {vec(z)}.")
        sol = ["cos θ = φ(x)ᵀφ(z)/(‖φ(x)‖‖φ(z)‖) = K(x, z)/√(K(x, x)K(z, z)).",
               f"K(x, z) = {fmt(kxz)}, K(x, x) = {fmt(kxx)}, K(z, z) = {fmt(kzz)}.",
               f"cos θ = {fmt(kxz)}/√({fmt(kxx)} × {fmt(kzz)}) = <b>{fmt(ans, 2)}</b>."]
        d = 2
    ansr = (ans, ans) if d == 0 else nat_range(ans, d)
    return Q(text=text + " " + nat_hint(d), qtype="NAT", marks=2, answer=ansr, nat_hint=nat_hint(d), solution=sol)


def _mat2(a, b, c, d):
    return f'<font face="Mono">[[{fmt(a)}, {fmt(b)}], [{fmt(c)}, {fmt(d)}]]</font>'


@template(TOPIC, S_KER, marks=2, qtype="MSQ")
def kernel_gram_psd(rng):
    kinds_t = ["pd", "psd0", "pd", "neg_off"]
    kinds_f = ["detneg", "negdiag", "asym", "detneg"]
    n_true = int(rng.integers(1, 4))
    kinds = list(rng.choice(kinds_t, n_true, replace=True)) + list(rng.choice(kinds_f, 4 - n_true, replace=True))
    kinds = [kinds[i] for i in rng.permutation(4)]
    opts, ans, expl = [], [], []
    for j, kd in enumerate(kinds):
        while True:
            a = int(rng.integers(1, 10))
            c = int(rng.integers(1, 10))
            if kd == "pd":
                lim = math.isqrt(a * c - 1) if a * c > 1 else 0
                bb = int(rng.integers(0, lim + 1)) if lim >= 0 else 0
                M = (a, bb, bb, c)
            elif kd == "neg_off":
                lim = math.isqrt(a * c - 1) if a * c > 1 else 0
                if lim < 1:
                    continue
                bb = -int(rng.integers(1, lim + 1))
                M = (a, bb, bb, c)
            elif kd == "psd0":
                r = math.isqrt(a * c)
                if r * r != a * c:
                    continue
                M = (a, r * int(rng.choice([-1, 1])), 0, c)
                M = (a, M[1], M[1], c)
            elif kd == "detneg":
                bb = math.isqrt(a * c) + int(rng.integers(1, 4))
                bb *= int(rng.choice([-1, 1]))
                M = (a, bb, bb, c)
            elif kd == "negdiag":
                M = (-a, 0 if rng.random() < 0.5 else 1, 0, c)
                M = (M[0], M[1], M[1], c)
            else:
                bb = int(rng.integers(0, 3))
                M = (a + 2, bb, bb + int(rng.integers(1, 3)), c + 2)
            s = _mat2(*M)
            if s not in opts:
                break
        opts.append(s)
        a_, b_, c_, d_ = M
        det = a_ * d_ - b_ * c_
        ok = kd in ("pd", "psd0", "neg_off")
        if ok:
            ans.append(j)
        why = {"pd": f"symmetric, diagonal entries ≥ 0 and det = {det} &gt; 0 ⇒ positive definite.",
               "neg_off": f"symmetric, diagonal ≥ 0, det = {det} &gt; 0 ⇒ PD (negative off-diagonal entries are fine).",
               "psd0": "symmetric, diagonal ≥ 0, det = 0 ⇒ PSD (singular) — still a valid Gram matrix.",
               "detneg": f"det = {det} &lt; 0 ⇒ one negative eigenvalue, not PSD.",
               "negdiag": "a diagonal entry K(x, x) = ‖φ(x)‖² is negative — impossible.",
               "asym": "not symmetric, but K(x, z) = K(z, x) for every kernel."}[kd]
        expl.append(f"<b>({'ABCD'[j]}) {'TRUE' if ok else 'FALSE'}.</b> {why}")
    return Q(text="Each option shows a 2 × 2 matrix [[K(x<sub>1</sub>,x<sub>1</sub>), K(x<sub>1</sub>,x<sub>2</sub>)], "
                  "[K(x<sub>2</sub>,x<sub>1</sub>), K(x<sub>2</sub>,x<sub>2</sub>)]]. Which of them can be the Gram "
                  "matrix of some valid (Mercer) kernel K on two points x<sub>1</sub>, x<sub>2</sub>?",
             qtype="MSQ", marks=2, options=opts, answer=ans,
             solution=["A Gram matrix of a valid kernel must be symmetric and positive semidefinite. For a symmetric "
                       "2 × 2 matrix this is equivalent to: both diagonal entries ≥ 0 and determinant ≥ 0."] + expl)


@template(TOPIC, S_PERC, marks=2, qtype="NAT")
def perceptron_epoch(rng):
    while True:
        n = int(rng.integers(4, 6))
        X = rng.integers(-3, 4, size=(n, 2)).astype(float)
        if len({tuple(r) for r in X}) < n or (np.abs(X).sum(1) == 0).any():
            continue
        u = np.array(_pick(rng, [(1, 1), (1, -1), (2, -1), (1, 2), (-1, 2)]), float)
        c = float(rng.integers(-1, 2))
        s = X @ u + c
        if (s == 0).any():
            continue
        y = np.sign(s)
        if len(set(y)) < 2:
            continue
        eta = _pick(rng, [1, 1, 0.5])
        w = np.zeros(3) if rng.random() < 0.6 else rng.integers(-1, 2, size=3).astype(float)
        w0 = w.copy()
        steps = []
        upd = 0
        for i in range(n):
            xt = np.array([1, X[i, 0], X[i, 1]])
            act = w @ xt
            mis = y[i] * act <= 0
            old = w.copy()
            if mis:
                w = w + eta * y[i] * xt
                upd += 1
            steps.append((i, act, mis, old, w.copy()))
        if 2 <= upd <= n - 1:
            break
    v = int(rng.integers(4))
    names = ["w<sub>0</sub> (bias)", "w<sub>1</sub>", "w<sub>2</sub>"]
    if v < 3:
        ask, ans = f"the value of {names[v]} after this epoch", float(w[v])
    else:
        ask, ans = "the number of weight updates made during this epoch", float(upd)
    rows = [["Step", "x̃ = (1, x₁, x₂)", "y", "wᵀx̃", "y·wᵀx̃ ≤ 0 ?", "w after step"]]
    for i, act, mis, old, new in steps:
        rows.append([str(i + 1), vec([1, X[i, 0], X[i, 1]]), "+1" if y[i] > 0 else "−1", fmt(act), "yes → update" if mis
                     else "no", vec(new)])

    def draw(fig):
        ax = fig.add_subplot(111)
        pos = y > 0
        ax.scatter(X[pos, 0], X[pos, 1], marker="o", s=34, c=INK, label="y = +1", zorder=3)
        ax.scatter(X[~pos, 0], X[~pos, 1], marker="s", s=34, facecolors="white", edgecolors=INK, label="y = −1",
                   zorder=3)
        for i, (a, b) in enumerate(X):
            ax.annotate(f"P{i + 1}", (a, b), textcoords="offset points", xytext=(4, 4), fontsize=6.5)
        ax.set_xlim(-3.7, 3.7)
        ax.set_ylim(-3.7, 3.7)
        ax.axhline(0, color=GREY, lw=0.6)
        ax.axvline(0, color=GREY, lw=0.6)
        ax.set_aspect("equal")
        ax.grid(alpha=0.3)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), frameon=False)

    d = 0 if eta == 1 or v == 3 else 1
    ansr = (ans, ans) if d == 0 else nat_range(ans, 1, tol=0.01)
    return Q(text=f"A perceptron with augmented weight vector w = (w<sub>0</sub>, w<sub>1</sub>, w<sub>2</sub>) "
                  f"(w<sub>0</sub> is the bias, x̃ = (1, x<sub>1</sub>, x<sub>2</sub>)) starts from w = {vec(w0)} and "
                  f"uses learning rate η = {fmt(eta)}. The points P1, P2, … are presented once, in order; whenever "
                  f"y·wᵀx̃ ≤ 0 the update w ← w + η y x̃ is applied. Find {ask}. {nat_hint(d)}",
             qtype="NAT", marks=2, answer=ansr, nat_hint=nat_hint(d),
             blocks=[_pts_table(X, y), Figure(draw, 8, 5.5)],
             solution=["Trace the epoch (a point with y·wᵀx̃ ≤ 0, including 0, triggers an update):", Table(rows),
                       f"Final w = {vec(w)}, number of updates = {upd}.  Answer: <b>{fmt(ans)}</b>."])


@template(TOPIC, S_MARGIN, marks=2, qtype="MCQ")
def svm_best_hyperplane(rng):
    for _ in range(4000):
        X, y, *_ = _gen_svm(rng, int(rng.integers(3, 5)), int(rng.integers(3, 5)))
        cands = {}
        for dvec in _DIRS[:8]:
            nv = np.array(dvec, float)
            s = X @ nv
            for c2 in range(int(2 * s.min()) - 2, int(2 * s.max()) + 3):
                c = c2 / 2
                g = (y * (s - c)).min() / np.linalg.norm(nv)
                g2 = (-y * (s - c)).min() / np.linalg.norm(nv)
                cands[(dvec, c)] = max(g, g2)
        good = [k for k, g in cands.items() if g > 0.05]
        bad = [k for k, g in cands.items() if g < -0.05]
        if len(good) < 3:
            continue
        idx = rng.choice(len(good), 3, replace=False)
        chosen = [good[i] for i in idx]
        if rng.random() < 0.4 and bad:
            chosen.append(bad[int(rng.integers(len(bad)))])
        else:
            rest = [k for k in good if k not in chosen]
            if not rest:
                continue
            chosen.append(rest[int(rng.integers(len(rest)))])
        gs = [cands[k] for k in chosen]
        order = np.argsort(gs)[::-1]
        if gs[order[0]] - gs[order[1]] < 0.08:
            continue
        strs = [_lin_str(k[0], -k[1]) + " = 0" for k in chosen]
        if len(set(strs)) < 4:
            continue
        break
    best = int(order[0])
    opts = strs
    rows = [["Hyperplane", "‖n‖", "min<sub>i</sub> distance (signed, best orientation)"]]
    for k, g, s_ in zip(chosen, gs, strs):
        rows.append([s_, fmt(np.linalg.norm(k[0]), 3), fmt(g, 3) + ("  (does not separate)" if g < 0 else "")])

    def draw(fig):
        ax = fig.add_subplot(111)
        _svm_axes(ax, X, y)

    return Q(text="Four candidate linear decision boundaries are proposed for the labelled training points shown. "
                  "Which boundary separates the two classes with the LARGEST geometric margin "
                  "(minimum distance from the boundary to any training point, all points correctly classified)?",
             qtype="MCQ", marks=2, options=opts, answer=best, blocks=[_pts_table(X, y), Figure(draw, 8.5, 6)],
             solution=["For nᵀx − c = 0, the geometric margin is min<sub>i</sub> y<sub>i</sub>s(nᵀx<sub>i</sub> − c)/‖n‖ "
                       "with orientation s = ±1 chosen so that the positive class is on the positive side; "
                       "a negative value means some point is misclassified.", Table(rows),
                       f"The largest margin is {fmt(gs[best], 3)}, for <b>{strs[best]}</b>. Note that a boundary "
                       f"can separate the data perfectly yet pass close to some point — only the minimum distance "
                       f"matters."])


# =============================================================================
# Decision trees — 1 mark
# =============================================================================
@template(TOPIC, S_IMP, marks=1, qtype="NAT")
def tree_node_impurity(rng):
    while True:
        K = int(_pick(rng, [2, 2, 3]))
        c = [int(v) for v in rng.integers(0, 13, size=K)]
        if sum(c) >= 4 and max(c) < sum(c) and sum(1 for v in c if v > 0) >= 2:
            break
    v = int(rng.choice(3, p=[0.45, 0.4, 0.15]))
    cls = ", ".join(f"{k} of class C<sub>{i + 1}</sub>" for i, k in enumerate(c))
    if v == 0:
        ans, d = _H(c), 3
        what = "entropy (in bits)"
        sol = [f"H = −Σ p<sub>k</sub> log<sub>2</sub> p<sub>k</sub> = {_H_expr(c)} = <b>{fmt(ans, 3)}</b> bits.",
               f"(Maximum possible with {K} classes: log<sub>2</sub>{K} = {fmt(math.log2(K), 3)}.)"]
    elif v == 1:
        ans, d = _G(c), 3
        what = "Gini index"
        sol = [f"Gini = 1 − Σ p<sub>k</sub>² = {_G_expr(c)} = <b>{fmt(ans, 3)}</b>.",
               f"(Maximum possible with {K} classes: 1 − 1/{K} = {fmt(1 - 1 / K, 3)}.)"]
    else:
        ans, d = _ME(c), 3
        what = "misclassification error"
        sol = [f"Error = 1 − max<sub>k</sub> p<sub>k</sub> = 1 − {max(c)}/{sum(c)} = <b>{fmt(ans, 3)}</b>."]
    return Q(text=f"A node of a classification tree contains {sum(c)} training records: {cls}. The {what} of this "
                  f"node is ______ {nat_hint(2)}",
             qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


@template(TOPIC, S_IMP, marks=1, qtype="NAT")
def tree_max_impurity(rng):
    v = int(rng.integers(4))
    if v == 0:
        K = int(_pick(rng, [3, 5, 6, 7, 10, 12, 20]))
        ans = math.log2(K)
        text = f"The maximum possible entropy (in bits) of a decision-tree node for a {K}-class problem is ______"
        sol = [f"Entropy is maximised by the uniform distribution p<sub>k</sub> = 1/{K}: H<sub>max</sub> = "
               f"log<sub>2</sub>{K} = <b>{fmt(ans, 2)}</b> bits."]
    elif v == 1:
        K = int(_pick(rng, [3, 4, 5, 6, 8, 10]))
        ans = 1 - 1 / K
        text = f"The maximum possible Gini index of a node in a {K}-class classification problem is ______"
        sol = [f"Gini = 1 − Σp<sub>k</sub>² is maximised at p<sub>k</sub> = 1/{K}: 1 − {K}·(1/{K})² = 1 − 1/{K} = "
               f"<b>{fmt(ans, 2)}</b>."]
    elif v == 2:
        p = _pick(rng, [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
        g = 2 * p * (1 - p)
        ans = p
        text = (f"In a binary-class node, the fraction of the minority class is p (≤ 0.5). If the Gini index of the "
                f"node is {fmt(g, 4)}, then p is ______")
        sol = [f"Binary Gini = 1 − p² − (1 − p)² = 2p(1 − p) = {fmt(g, 4)}.",
               f"p² − p + {fmt(g / 2, 4)} = 0 ⇒ p = [1 − √(1 − 2×{fmt(g, 4)})]/2 = [1 − {fmt(math.sqrt(1 - 2 * g), 4)}]/2 "
               f"= <b>{fmt(ans, 2)}</b> (taking the root ≤ 0.5)."]
    else:
        K = int(_pick(rng, [2, 4, 8, 16, 32]))
        ans = math.log2(K)
        m = int(_pick(rng, [2, 3, 4]))
        tot = K * m
        text = (f"A node contains {tot} records spread equally over {K} classes ({m} records per class). Its entropy "
                f"(in bits) is ______")
        sol = [f"p<sub>k</sub> = {m}/{tot} = 1/{K} for every class ⇒ H = −{K}·(1/{K})log<sub>2</sub>(1/{K}) = "
               f"log<sub>2</sub>{K} = <b>{fmt(ans, 2)}</b> — the maximum possible for {K} classes."]
    return Q(text=text + " " + nat_hint(2), qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             solution=sol)


_DOMAINS = [
    {"classes": ["Low", "Medium", "High", "Critical"], "noun": "risk level of a loan applicant",
     "num": [("Age", 22, 65, "yr"), ("Income", 20, 95, "k"), ("Debt", 1, 40, "k")],
     "cat": ("Credit", ["Good", "Fair", "Poor"])},
    {"classes": ["Tennis", "Swim", "Golf", "Stay in"], "noun": "activity for the day",
     "num": [("Temp", 5, 40, "°C"), ("Humidity", 30, 95, "%"), ("Wind", 2, 40, "km/h")],
     "cat": ("Outlook", ["Sunny", "Overcast", "Rain"])},
    {"classes": ["Basic", "Silver", "Gold", "Platinum"], "noun": "membership tier offered to a customer",
     "num": [("Visits", 1, 50, ""), ("Spend", 5, 120, "k"), ("Tenure", 1, 15, "yr")],
     "cat": ("Region", ["North", "South", "East"])},
    {"classes": ["Normal", "Mild", "Moderate", "Severe"], "noun": "diagnosis category of a patient",
     "num": [("BP", 90, 180, ""), ("Sugar", 70, 250, ""), ("BMI", 16, 40, "")],
     "cat": ("Smoker", ["Never", "Former", "Current"])},
]


def _rand_tree_mixed(rng):
    dom = _pick(rng, _DOMAINS)
    nums = [dom["num"][i] for i in rng.permutation(3)]
    thr = []
    for (nm, lo, hi, _) in nums:
        thr.append(int(rng.integers(lo + (hi - lo) // 4, hi - (hi - lo) // 4)))
    cat, vals = dom["cat"]
    labels = list(rng.permutation(dom["classes"])) + [_pick(rng, dom["classes"])]
    labels = [labels[i] for i in rng.permutation(5)]
    shape = int(rng.integers(2))
    if shape == 0:
        # numeric root -> (numeric -> 2 leaves) | (categorical -> 3 leaves)
        def classify(r):
            if r[nums[0][0]] <= thr[0]:
                return labels[0] if r[nums[1][0]] <= thr[1] else labels[1]
            return labels[2 + vals.index(r[cat])]
        root = _node(f"{nums[0][0]} ≤ {thr[0]}?", [
            ("Yes", _node(f"{nums[1][0]} ≤ {thr[1]}?", [("Yes", _node(labels[0])), ("No", _node(labels[1]))])),
            ("No", _node(cat, [(vals[0], _node(labels[2])), (vals[1], _node(labels[3])), (vals[2], _node(labels[4]))]))])
    else:
        # categorical root -> leaf | numeric(2 leaves) | numeric(2 leaves)
        def classify(r):
            k = vals.index(r[cat])
            if k == 0:
                return labels[0]
            if k == 1:
                return labels[1] if r[nums[0][0]] <= thr[0] else labels[2]
            return labels[3] if r[nums[1][0]] <= thr[1] else labels[4]
        root = _node(cat, [(vals[0], _node(labels[0])),
                           (vals[1], _node(f"{nums[0][0]} ≤ {thr[0]}?", [("Yes", _node(labels[1])),
                                                                         ("No", _node(labels[2]))])),
                           (vals[2], _node(f"{nums[1][0]} ≤ {thr[1]}?", [("Yes", _node(labels[3])),
                                                                         ("No", _node(labels[4]))]))])
    return dom, nums, thr, cat, vals, root, classify


@template(TOPIC, S_STRUCT, marks=1, qtype="MCQ")
def tree_traverse(rng):
    dom, nums, thr, cat, vals, root, classify = _rand_tree_mixed(rng)
    rec = {nm: int(rng.integers(lo, hi + 1)) for (nm, lo, hi, _) in nums}
    # bias numeric values to be near thresholds sometimes (careful reading)
    for (nm, lo, hi, _), t in zip(nums, thr):
        if rng.random() < 0.35:
            rec[nm] = t + int(rng.choice([0, 1, -1]))
    rec[cat] = _pick(rng, vals)
    pred = classify(rec)
    opts, a = mcq(rng, pred, [c for c in dom["classes"] if c != pred])
    head = [nm for (nm, *_r) in nums] + [cat]
    tbl = Table([head, [str(rec[h]) for h in head]], header=True)

    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_tree(ax, root)

    path = []
    if root["text"] == cat:
        path.append(f"Root tests {cat} = {rec[cat]}.")
    else:
        path.append(f"Root: {nums[0][0]} = {rec[nums[0][0]]} ≤ {thr[0]}? "
                    f"{'Yes' if rec[nums[0][0]] <= thr[0] else 'No'}.")
    for (nm, *_r), t in zip(nums[:2], thr[:2]):
        path.append(f"{nm} = {rec[nm]} vs threshold {t}: {'≤' if rec[nm] <= t else '&gt;'}.")
    return Q(text=f"The decision tree below predicts the {dom['noun']}. Edges labelled Yes/No answer the test in the "
                  f"node. What is the prediction for the record shown in the table?",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 10, 6.2), tbl],
             solution=["Follow the record from the root, taking the branch that matches each test:"] + path +
                      [f"(Only the tests on the actual path matter.) The record reaches the leaf <b>{pred}</b>.",
                       "Note: “≤” includes equality, so a value equal to the threshold goes to the Yes branch."])


@template(TOPIC, S_STRUCT, marks=1, qtype="NAT")
def tree_depth_leaves(rng):
    v = int(rng.integers(6))
    if v == 0:
        d = int(rng.integers(3, 9))
        ans = 2 ** d
        text = f"The maximum number of leaf nodes in a binary decision tree of depth {d} (root at depth 0) is ______"
        sol = [f"Each level at most doubles the nodes: leaves ≤ 2<super>d</super> = 2<super>{d}</super> = <b>{ans}</b>."]
    elif v == 1:
        d = int(rng.integers(3, 8))
        ans = 2 ** (d + 1) - 1
        text = f"The maximum total number of nodes (internal + leaves) in a binary decision tree of depth {d} " \
               f"(root at depth 0) is ______"
        sol = [f"1 + 2 + … + 2<super>{d}</super> = 2<super>{d + 1}</super> − 1 = <b>{ans}</b>."]
    elif v == 2:
        L = int(rng.integers(5, 60))
        ans = L - 1
        text = f"A binary decision tree in which every internal node has exactly two children has {L} leaves. The " \
               f"number of internal (decision) nodes is ______"
        sol = [f"In a full binary tree, #internal = #leaves − 1 = {L} − 1 = <b>{ans}</b>."]
    elif v == 3:
        L = int(rng.integers(5, 200))
        ans = math.ceil(math.log2(L))
        if 2 ** ans == L:
            L += 1
            ans = math.ceil(math.log2(L))
        text = f"A binary decision tree must have at least {L} leaves to separate {L} distinct classes. The minimum " \
               f"possible depth of such a tree is ______"
        sol = [f"Depth d allows at most 2<super>d</super> leaves, so we need 2<super>d</super> ≥ {L} ⇒ "
               f"d ≥ log<sub>2</sub>{L} = {fmt(math.log2(L), 3)} ⇒ d = <b>{ans}</b>."]
    elif v == 4:
        n = int(rng.integers(2, 5))
        ans = 2 ** (2 ** n)
        text = f"The number of distinct Boolean functions of {n} Boolean attributes (each of which can be represented " \
               f"by some decision tree) is ______"
        sol = [f"There are 2<super>{n}</super> = {2 ** n} input rows, each mapped to 0/1: 2<super>{2 ** n}</super> = "
               f"<b>{ans}</b> functions."]
    else:
        n = int(rng.integers(3, 9))
        ans = 2 ** n
        text = f"A decision tree is built over {n} Boolean attributes, testing each attribute at most once on any " \
               f"root-to-leaf path. The maximum possible number of leaves is ______"
        sol = [f"Depth is at most {n} (one test per attribute), so leaves ≤ 2<super>{n}</super> = <b>{ans}</b>."]
    return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(ans, ans), nat_hint=nat_hint(0),
             solution=sol)


@template(TOPIC, S_PRUNE, marks=1, qtype="MCQ")
def tree_ccp_select(rng):
    while True:
        L = sorted(rng.choice(np.arange(2, 16), 4, replace=False))[::-1]
        R = sorted(rng.choice(np.arange(2, 40), 4, replace=False) / 200)
        alpha = _pick(rng, [0.002, 0.005, 0.008, 0.01, 0.015, 0.02, 0.03])
        cost = [R[i] + alpha * L[i] for i in range(4)]
        o = np.argsort(cost)
        if cost[o[1]] - cost[o[0]] >= 0.004:
            break
    best = int(o[0])
    rows = [["Subtree", "T1", "T2", "T3", "T4"],
            ["Leaves |T|"] + [str(v) for v in L],
            ["Training error R(T)"] + [fmt(v, 3) for v in R]]
    sol_rows = [["Subtree", "R(T) + α|T|"]] + [[f"T{i + 1}", f"{fmt(R[i], 3)} + {fmt(alpha, 3)}×{L[i]} = "
                                                               f"{fmt(cost[i], 4)}"] for i in range(4)]
    return Q(text=f"Cost-complexity pruning of a classification tree produced the nested subtrees T1 ⊃ T2 ⊃ T3 ⊃ T4 "
                  f"below. For complexity parameter α = {fmt(alpha, 3)}, which subtree minimises "
                  f"R<sub>α</sub>(T) = R(T) + α|T| ?",
             qtype="MCQ", marks=1, options=["T1", "T2", "T3", "T4"], answer=best, blocks=[Table(rows)],
             solution=[Table(sol_rows), f"Minimum at <b>T{best + 1}</b>. Larger α penalises leaves more and favours "
                                        f"smaller trees; α = 0 would pick the largest tree T1."])


_TREE_T = [
    ("The entropy of a node in a K-class problem is at most log<sub>2</sub>K bits.", "Attained by the uniform distribution."),
    ("The Gini index of a pure node is 0.", "1 − 1² = 0."),
    ("A decision tree's training predictions are unchanged by a strictly increasing transformation of a feature "
     "(e.g. x → log x).", "Splits depend only on the ordering of values."),
    ("ID3 chooses splits greedily by information gain and never backtracks.", "Hill-climbing without backtracking."),
    ("Information gain is biased towards attributes with many distinct values; C4.5's gain ratio corrects for this.",
     "Split information penalises many-way splits."),
    ("CART builds binary trees and typically uses the Gini index for classification.", "Standard CART design."),
    ("A tree grown until every leaf is pure usually has low bias and high variance.", "It fits noise."),
    ("Pre-pruning stops tree growth early, e.g. via a maximum depth or minimum samples per leaf.", "Early stopping."),
    ("Post-pruning grows a full tree and then removes subtrees that do not help validation performance.",
     "E.g. reduced-error or cost-complexity pruning."),
    ("Cost-complexity pruning minimises R(T) + α|T|, where |T| is the number of leaves.", "CART pruning criterion."),
    ("A larger α in cost-complexity pruning yields a smaller (or equal-size) tree.", "Each leaf costs more."),
    ("A binary tree of depth d has at most 2<super>d</super> leaves.", "Doubling per level."),
    ("Decision trees do not require feature standardisation.", "Threshold splits are scale-invariant."),
    ("A tree with axis-parallel splits predicts a constant within each axis-aligned rectangular region.",
     "Each leaf corresponds to a hyper-rectangle."),
    ("The information gain of any split is non-negative.", "Conditioning cannot increase entropy on average."),
    ("For a continuous attribute it suffices to consider thresholds at midpoints between consecutive distinct sorted "
     "values.", "Any threshold between two such values gives the same partition."),
    ("Regression trees choose splits that minimise the total within-node sum of squared errors.", "Variance reduction."),
    ("With squared-error loss, a regression-tree leaf predicts the mean response of its training samples.",
     "The mean minimises SSE."),
    ("Any Boolean function of n Boolean attributes can be represented by a decision tree.", "Up to 2<super>n</super> leaves."),
    ("Greedy top-down induction is not guaranteed to find the smallest tree consistent with the data.",
     "Finding the minimal tree is NP-hard."),
    ("Small changes in the training data can produce a very different tree.", "Trees are high-variance learners."),
    ("For a binary node with class fraction p, the Gini index 2p(1 − p) is maximised at p = 0.5 with value 0.5.",
     "Derivative 2 − 4p = 0."),
    ("Misclassification error is less sensitive to changes in class proportions than entropy or Gini, so the latter "
     "are preferred for growing trees.", "Entropy/Gini are strictly concave."),
    ("Pruning a subtree can increase the training error of the tree.", "Pruning trades training fit for simplicity."),
]
_TREE_F = [
    ("The entropy of a node in a K-class problem can exceed log<sub>2</sub>K bits.", "log<sub>2</sub>K is the maximum."),
    ("The maximum Gini index for a binary classification node is 1.", "It is 0.5."),
    ("Rescaling a feature as x → 10x changes the training predictions of a decision tree.",
     "Ordering is preserved, so the same partition results."),
    ("ID3 backtracks to reconsider earlier splits when a later split is poor.", "ID3 is purely greedy."),
    ("Information gain is biased towards attributes with few distinct values.", "It favours many-valued attributes."),
    ("Growing a tree until all leaves are pure typically reduces variance.", "It increases variance (overfits)."),
    ("Increasing α in cost-complexity pruning produces larger trees.", "Larger α gives smaller trees."),
    ("A binary tree of depth d can have up to 2<super>d+1</super> leaves.", "At most 2<super>d</super>."),
    ("Decision trees require features standardised to zero mean and unit variance.", "Not needed."),
    ("Decision trees can handle only categorical attributes.", "Continuous attributes are split by thresholds."),
    ("The information gain of a poorly chosen split can be negative.", "IG ≥ 0 always."),
    ("Greedy ID3 always finds the smallest tree consistent with the training data.", "Greedy ≠ optimal."),
    ("Post-pruning is performed before the tree is fully grown.", "That is pre-pruning."),
    ("The Gini index of a pure node is 1.", "It is 0."),
    ("A tree with finitely many axis-parallel splits can represent the diagonal boundary x₁ = x₂ exactly on "
     "continuous inputs.", "Only a staircase approximation is possible."),
    ("With squared-error loss, a regression-tree leaf predicts the median of its training responses.",
     "The mean minimises SSE (median minimises absolute error)."),
    ("Pruning a subtree can never increase the training error.", "Pruning usually increases (or keeps) training error."),
    ("Testing each of n Boolean attributes at most once per path, a tree can have depth greater than n.",
     "Depth ≤ n."),
    ("Gain ratio equals information gain multiplied by split information.", "It is IG divided by split information."),
    ("A decision tree is a linear classifier.", "Its boundary is piecewise axis-parallel, generally non-linear."),
    ("Information gain and Gini gain always select the same attribute.", "They usually agree but can differ."),
    ("Deeper trees always generalise better because they have lower training error.", "They tend to overfit."),
]


@template(TOPIC, S_PRUNE, marks=1, qtype="MSQ")
def tree_concepts_msq(rng):
    opts, ans, expl = msq_from_statements(rng, _TREE_T, _TREE_F)
    return Q(text="Which of the following statements about decision-tree learning is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# =============================================================================
# Decision trees — 2 marks
# =============================================================================
_ATTRS = [("Outlook", ["Sunny", "Overcast", "Rain"]), ("Humidity", ["High", "Normal"]), ("Wind", ["Weak", "Strong"]),
          ("Temp", ["Hot", "Mild", "Cool"]), ("Student", ["Yes", "No"]), ("Income", ["Low", "Medium", "High"]),
          ("Credit", ["Fair", "Excellent"]), ("Colour", ["Red", "Green", "Blue"]), ("Size", ["Small", "Large"]),
          ("Age", ["Young", "Middle", "Senior"]), ("Shape", ["Round", "Square", "Oval"]), ("Weekend", ["Yes", "No"])]


def _rand_split(rng, k, K=2, minIG=0.05, crit=_H):
    for _ in range(10000):
        counts = [[int(v) for v in rng.integers(0, 9, size=K)] for _ in range(k)]
        if any(sum(c) < 2 for c in counts):
            continue
        par = [sum(c[j] for c in counts) for j in range(K)]
        if min(par) == 0:
            continue
        N = sum(par)
        gain = crit(par) - sum(sum(c) / N * crit(c) for c in counts)
        if gain >= minIG and N <= 30:
            return par, counts, gain
    raise RuntimeError


def _split_fig(attr, vals, par, counts):
    root = _node(f"{attr}\n{_cstr(par)}", [(v, _node(_cstr(c))) for v, c in zip(vals, counts)])

    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_tree(ax, root, fs=7.5, leaf_fc="#f2f2f2")
    return Figure(draw, 8 if len(vals) <= 2 else 9.5, 4.2)


@template(TOPIC, S_SPLIT, marks=2, qtype="NAT")
def tree_info_gain(rng):
    attr, vals = _pick(rng, _ATTRS)
    k = len(vals)
    par, counts, ig = _rand_split(rng, k)
    N = sum(par)
    v = int(rng.choice(2, p=[0.7, 0.3]))
    hc = [_H(c) for c in counts]
    wsum = sum(sum(c) / N * h for c, h in zip(counts, hc))
    if v == 0:
        ask, ans = "the information gain (in bits) of splitting on " + attr, ig
    elif v == 1:
        ask, ans = f"the weighted average entropy (in bits) of the children after splitting on {attr}", wsum
    sol = [f"Parent {_cstr(par)}: H = {_H_expr(par)} = {fmt(_H(par), 4)}."]
    for vv, c, h in zip(vals, counts, hc):
        sol.append(f"{attr} = {vv}: {_cstr(c)}, H = {_H_expr(c)} = {fmt(h, 4)}.")
    sol.append("Weighted child entropy = " + " + ".join(f"({sum(c)}/{N})({fmt(h, 4)})" for c, h in zip(counts, hc))
               + f" = {fmt(wsum, 4)}.")
    sol.append(f"IG = {fmt(_H(par), 4)} − {fmt(wsum, 4)} = {fmt(ig, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"A node with {N} training records (class counts [positive+, negative−]) is split on the attribute "
                  f"{attr} as shown. Compute {ask}. {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_split_fig(attr, vals, par, counts)], solution=sol)


@template(TOPIC, S_SPLIT, marks=2, qtype="NAT")
def tree_gini_gain(rng):
    attr, vals = _pick(rng, _ATTRS)
    k = len(vals)
    K = int(_pick(rng, [2, 2, 3]))
    par, counts, gg = _rand_split(rng, k, K=K, minIG=0.03, crit=_G)
    N = sum(par)
    gc = [_G(c) for c in counts]
    wsum = sum(sum(c) / N * g for c, g in zip(counts, gc))
    v = int(rng.integers(2))
    if v == 0:
        ask, ans = f"the reduction in Gini index (Gini gain) obtained by splitting on {attr}", gg
    else:
        ask, ans = f"the weighted Gini index of the split on {attr}", wsum
    lab = "class counts [positive+, negative−]" if K == 2 else "class counts [C1, C2, C3]"
    sol = [f"Parent {_cstr(par)}: Gini = {_G_expr(par)} = {fmt(_G(par), 4)}."]
    for vv, c, g in zip(vals, counts, gc):
        sol.append(f"{attr} = {vv}: {_cstr(c)}, Gini = {_G_expr(c)} = {fmt(g, 4)}.")
    sol.append("Weighted Gini = " + " + ".join(f"({sum(c)}/{N})({fmt(g, 4)})" for c, g in zip(counts, gc)) +
               f" = {fmt(wsum, 4)}.")
    sol.append(f"Gini gain = {fmt(_G(par), 4)} − {fmt(wsum, 4)} = {fmt(gg, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"A CART node with {N} training records ({lab}) is split on {attr} as shown. "
                  f"Compute {ask}. {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_split_fig(attr, vals, par, counts)], solution=sol)


@template(TOPIC, S_SPLIT, marks=2, qtype="NAT")
def tree_gain_ratio(rng):
    k = int(rng.integers(2, 5))
    attr = _pick(rng, ["Customer-type", "Region", "Day", "Product", "Branch", "Channel"])
    vals = [f"v{i + 1}" for i in range(k)]
    par, counts, ig = _rand_split(rng, k, minIG=0.08)
    N = sum(par)
    sizes = [sum(c) for c in counts]
    si = _H(sizes)
    gr = ig / si
    v = int(rng.choice(2, p=[0.65, 0.35]))
    ask, ans = ("the gain ratio", gr) if v == 0 else ("the split information", si)
    rows = [[attr, "#Yes", "#No"]] + [[vv, str(c[0]), str(c[1])] for vv, c in zip(vals, counts)]
    sol = [f"Parent [{par[0]} Yes, {par[1]} No]: H = {fmt(_H(par), 4)}.",
           "Child entropies: " + ", ".join(f"{vv}: {fmt(_H(c), 4)}" for vv, c in zip(vals, counts)) + ".",
           f"IG = {fmt(_H(par), 4)} − Σ(n<sub>v</sub>/{N})H<sub>v</sub> = {fmt(ig, 4)}.",
           f"SplitInfo = −Σ (n<sub>v</sub>/N) log<sub>2</sub>(n<sub>v</sub>/N) = {_H_expr(sizes)} = {fmt(si, 4)}."]
    if v == 0:
        sol.append(f"Gain ratio = IG / SplitInfo = {fmt(ig, 4)}/{fmt(si, 4)} = <b>{fmt(gr, 2)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(si, 2)}</b>.")
    sol.append("C4.5 uses the gain ratio to penalise attributes that split the data into many small branches.")
    return Q(text=f"In C4.5, the attribute {attr} splits a node of {N} records as tabulated (class Yes/No counts in "
                  f"each branch). Compute {ask} of {attr} (all logarithms base 2). {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2), blocks=[Table(rows)],
             solution=sol)


@template(TOPIC, S_SPLIT, marks=2, qtype="MCQ")
def tree_best_attribute(rng):
    crit_name = _pick(rng, ["information gain", "information gain", "Gini gain"])
    crit = _H if crit_name == "information gain" else _G
    for _ in range(5000):
        idx = rng.choice(len(_ATTRS), 4, replace=False)
        attrs = [_ATTRS[i] for i in idx]
        n = int(rng.integers(10, 13))
        data = [[_pick(rng, vals) for (_, vals) in attrs] for _ in range(n)]
        key = int(rng.integers(4))
        good = set(rng.choice(attrs[key][1], max(1, len(attrs[key][1]) // 2), replace=False))
        lab = ["Yes" if (r[key] in good) != (rng.random() < 0.2) else "No" for r in data]
        par = [lab.count("Yes"), lab.count("No")]
        if min(par) < 3:
            continue
        gains, splits = [], []
        for j, (nm, vals) in enumerate(attrs):
            cs = []
            for vv in vals:
                ls = [lab[i] for i in range(n) if data[i][j] == vv]
                if ls:
                    cs.append((vv, [ls.count("Yes"), ls.count("No")]))
            g = crit(par) - sum(sum(c) / n * crit(c) for _, c in cs)
            gains.append(g)
            splits.append(cs)
        o = np.argsort(gains)[::-1]
        if gains[o[0]] - gains[o[1]] >= 0.03 and gains[o[0]] >= 0.1:
            break
    best = int(o[0])
    names = [a[0] for a in attrs]
    rows = [["#"] + names + ["Class"]] + [[str(i + 1)] + data[i] + [lab[i]] for i in range(n)]
    sol = [f"Parent: {par[0]} Yes, {par[1]} No ⇒ {'H' if crit is _H else 'Gini'} = {fmt(crit(par), 4)}."]
    for j, nm in enumerate(names):
        parts = ", ".join(f"{vv}: {_cstr(c)}" for vv, c in splits[j])
        sol.append(f"<b>{nm}</b> — {parts}; gain = {fmt(gains[j], 4)}.")
    sol.append(f"The largest {crit_name} is for <b>{names[best]}</b>, so it is chosen at the root.")
    return Q(text=f"A decision tree is to be grown on the {n} training records below using {crit_name} as the "
                  f"splitting criterion (multi-way split on each categorical attribute). Which attribute is chosen "
                  f"at the root?",
             qtype="MCQ", marks=2, options=names, answer=best, blocks=[Table(rows)], solution=sol)


@template(TOPIC, S_SPLIT, marks=2, qtype="NAT")
def tree_continuous_threshold(rng):
    nm, lo, hi = _pick(rng, [("Temperature", 50, 95), ("Age", 18, 70), ("Income", 10, 90), ("Score", 30, 100),
                             ("Glucose", 70, 160)])
    for _ in range(5000):
        n = int(rng.integers(8, 11))
        x = np.sort(rng.choice(np.arange(lo, hi + 1), n, replace=False))
        t0 = rng.integers(2, n - 2)
        lab = np.array([1 if i >= t0 else 0 for i in range(n)])
        if rng.random() < 0.5:
            lab = 1 - lab
        flip = rng.choice(n, int(rng.integers(1, 3)), replace=False)
        lab[flip] = 1 - lab[flip]
        cands = []
        for i in range(n - 1):
            if lab[i] != lab[i + 1]:
                t = (x[i] + x[i + 1]) / 2
                L, R = lab[:i + 1], lab[i + 1:]
                cl = [int(L.sum()), int(len(L) - L.sum())]
                cr = [int(R.sum()), int(len(R) - R.sum())]
                par = [int(lab.sum()), int(n - lab.sum())]
                g = _H(par) - len(L) / n * _H(cl) - len(R) / n * _H(cr)
                cands.append((t, g, cl, cr))
        if len(cands) < 3:
            continue
        gs = sorted([c[1] for c in cands])[::-1]
        if gs[0] - gs[1] >= 0.02:
            break
    par = [int(lab.sum()), int(n - lab.sum())]
    bi = int(np.argmax([c[1] for c in cands]))
    bt, bg = cands[bi][0], cands[bi][1]
    v = int(rng.choice(3, p=[0.5, 0.3, 0.2]))
    if v == 0:
        ask, ans, d, ansr = "the threshold value t chosen for the split “" + nm + " ≤ t”", bt, 1, \
            nat_range(bt, 1, tol=0.01)
    elif v == 1:
        ask, ans, d = "the information gain (in bits) of the best threshold split", bg, 2
        ansr = nat_range(bg, 2)
    else:
        ask, ans, d = "the number of candidate thresholds that need to be evaluated (midpoints between consecutive " \
                      "sorted values at which the class label changes)", len(cands), 0
        ansr = (ans, ans)
    perm = rng.permutation(n)
    labs = ["Yes" if v_ else "No" for v_ in lab]
    tbl = Table([[nm] + [str(int(x[i])) for i in perm], ["Class"] + [labs[i] for i in perm]], header=False)
    rows = [["Threshold", "Left (≤ t) [Yes, No]", "Right [Yes, No]", "IG"]] + \
           [[fmt(t, 1), str(cl), str(cr), fmt(g, 4)] for t, g, cl, cr in cands]

    def draw(fig):
        ax = fig.add_subplot(111)
        yes = lab == 1
        ax.scatter(x[yes], np.zeros(yes.sum()), marker="o", s=40, c=INK, label="Yes", zorder=3)
        ax.scatter(x[~yes], np.zeros((~yes).sum()), marker="s", s=40, facecolors="white", edgecolors=INK,
                   label="No", zorder=3)
        ax.axhline(0, color=GREY, lw=0.8, zorder=1)
        for k_, xi in enumerate(x):
            ax.annotate(str(int(xi)), (xi, 0), textcoords="offset points", xytext=(0, -13 if k_ % 2 == 0 else 7),
                        ha="center", fontsize=6.5)
        ax.set_yticks([])
        ax.set_ylim(-1, 1)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.set_xticks([])
        ax.set_xlabel(nm)
        ax.legend(loc="upper center", ncol=2, frameon=False)

    return Q(text=f"The continuous attribute {nm} and the class label of {n} training records are given below "
                  f"(unsorted). A binary split “{nm} ≤ t” is chosen to maximise information gain, with t restricted "
                  f"to midpoints between consecutive sorted values. Find {ask}. {nat_hint(d)}",
             qtype="NAT", marks=2, answer=ansr, nat_hint=nat_hint(d), blocks=[tbl, Figure(draw, 10, 3.0)],
             solution=["Sort the values: " + ", ".join(f"{int(a)}({'Y' if b_ else 'N'})" for a, b_ in zip(x, lab)) + ".",
                       f"Parent [{par[0]} Yes, {par[1]} No], H = {fmt(_H(par), 4)}. The optimal threshold always lies "
                       f"where the class changes between neighbours (Fayyad–Irani), giving {len(cands)} candidates:",
                       Table(rows),
                       f"Best: t = {fmt(bt, 1)} with IG = {fmt(bg, 4)}. Answer: <b>{fmt(ans, d)}</b>."])


def _ccp_tree(rng):
    for _ in range(5000):
        e = {}
        e[4], e[5], e[6], e[8], e[9] = [int(v) for v in rng.integers(0, 8, size=5)]
        e[7] = e[8] + e[9] + int(rng.integers(1, 9))
        e[2] = e[4] + e[5] + int(rng.integers(1, 12))
        e[3] = max(e[6] + e[7] + int(rng.integers(1, 12)), e[6] + e[8] + e[9] + 2)
        e[1] = e[2] + e[3] + int(rng.integers(-3, 15))
        leaves_err = e[4] + e[5] + e[6] + e[8] + e[9]
        if e[1] <= leaves_err + 4 or e[1] > 60:
            continue
        N = 100
        g = {1: (e[1] - leaves_err) / (N * 4), 2: (e[2] - e[4] - e[5]) / N,
             3: (e[3] - e[6] - e[8] - e[9]) / (N * 2), 7: (e[7] - e[8] - e[9]) / N}
        gs = sorted(g.values())
        if gs[1] - gs[0] >= 0.004:
            return e, g, N
    raise RuntimeError


@template(TOPIC, S_PRUNE, marks=2, qtype="NAT")
def tree_ccp_alpha(rng):
    e, g, N = _ccp_tree(rng)
    root = _node(f"t1\ne={e[1]}", [
        ("", _node(f"t2\ne={e[2]}", [("", _node(f"t4\ne={e[4]}")), ("", _node(f"t5\ne={e[5]}"))])),
        ("", _node(f"t3\ne={e[3]}", [("", _node(f"t6\ne={e[6]}")),
                                     ("", _node(f"t7\ne={e[7]}", [("", _node(f"t8\ne={e[8]}")),
                                                                  ("", _node(f"t9\ne={e[9]}"))]))]))])

    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_tree(ax, root, fs=7)

    weakest = min(g, key=g.get)
    leaves_err = e[4] + e[5] + e[6] + e[8] + e[9]
    v = int(rng.integers(2))
    sol = ["R(t) = e(t)/N with N = 100. For an internal node t with subtree T<sub>t</sub>: "
           "g(t) = [R(t) − R(T<sub>t</sub>)]/(|T<sub>t</sub>| − 1), where |T<sub>t</sub>| = number of leaves.",
           Table([["Node", "R(t)", "R(T<sub>t</sub>)", "|T<sub>t</sub>|", "g(t)"],
                  ["t1", fmt(e[1] / N, 2), fmt(leaves_err / N, 2), "5", fmt(g[1], 4)],
                  ["t2", fmt(e[2] / N, 2), fmt((e[4] + e[5]) / N, 2), "2", fmt(g[2], 4)],
                  ["t3", fmt(e[3] / N, 2), fmt((e[6] + e[8] + e[9]) / N, 2), "3", fmt(g[3], 4)],
                  ["t7", fmt(e[7] / N, 2), fmt((e[8] + e[9]) / N, 2), "2", fmt(g[7], 4)]])]
    if v == 0:
        ans = g[weakest]
        text = ("The smallest value of α at which cost-complexity pruning first prunes the tree (the weakest link) "
                "is ______")
        sol.append(f"The weakest link is t{weakest} with the minimum g = <b>{fmt(ans, 3)}</b>; for α ≥ this value, "
                   f"collapsing t{weakest} into a leaf does not increase R<sub>α</sub>.")
        d = 3
    else:
        alpha = _pick(rng, [0.005, 0.01, 0.02, 0.025])
        ans = leaves_err / N + alpha * 5
        text = f"For α = {fmt(alpha, 3)}, the cost-complexity R<sub>α</sub>(T) = R(T) + α|T| of the full tree T is ______"
        sol = [f"R(T) = sum of leaf errors / N = ({e[4]} + {e[5]} + {e[6]} + {e[8]} + {e[9]})/100 = "
               f"{fmt(leaves_err / N, 2)}; |T| = 5 leaves.",
               f"R<sub>α</sub>(T) = {fmt(leaves_err / N, 2)} + {fmt(alpha, 3)} × 5 = <b>{fmt(ans, 3)}</b>."]
        d = 3
    return Q(text=f"A classification tree was grown on N = 100 training records. Each node shows e(t), the number of "
                  f"training records that would be misclassified if t were a leaf; R(t) = e(t)/N. " + text + " " +
                  nat_hint(d),
             qtype="NAT", marks=2, answer=nat_range(ans, d, tol=0.0015), nat_hint=nat_hint(d),
             blocks=[Figure(draw, 9, 6.8)], solution=sol)


@template(TOPIC, S_REG, marks=2, qtype="NAT")
def regression_tree_split(rng):
    for _ in range(5000):
        n = int(rng.integers(6, 9))
        x = np.sort(rng.choice(np.arange(1, 16), n, replace=False)).astype(float)
        k = int(rng.integers(2, n - 1))
        lvl = rng.integers(1, 10, size=2)
        y = np.array([lvl[0] if i < k else lvl[1] for i in range(n)], float) + rng.integers(-2, 3, size=n)
        sse0 = ((y - y.mean()) ** 2).sum()
        res = []
        for i in range(1, n):
            L, R = y[:i], y[i:]
            s = ((L - L.mean()) ** 2).sum() + ((R - R.mean()) ** 2).sum()
            res.append(((x[i - 1] + x[i]) / 2, s, L.mean(), R.mean()))
        ss = sorted(r[1] for r in res)
        if ss[1] - ss[0] >= 1.0 and sse0 - ss[0] >= 3:
            break
    bi = int(np.argmin([r[1] for r in res]))
    t, sb, mL, mR = res[bi]
    v = int(rng.integers(4))
    if v == 0:
        ask, ans, d = "the threshold t of the best split “x ≤ t”", t, 1
        ansr = nat_range(t, 1, tol=0.01)
    elif v == 1:
        ask, ans, d = "the reduction in SSE (sum of squared errors) achieved by the best split", sse0 - sb, 2
        ansr = nat_range(ans, 2)
    elif v == 2:
        x0 = float(_pick(rng, [v_ for v_ in range(1, 16) if v_ not in x]))
        pred = mL if x0 <= t else mR
        ask, ans, d = f"the prediction of the resulting depth-1 regression tree (stump) at x = {fmt(x0)}", pred, 2
        ansr = nat_range(pred, 2)
    else:
        ask, ans, d = "the total SSE of the two child nodes after the best split", sb, 2
        ansr = nat_range(sb, 2)
    rows = [["Split t", "Left mean", "Right mean", "SSE<sub>L</sub> + SSE<sub>R</sub>"]] + \
           [[fmt(r[0], 1), fmt(r[2], 3), fmt(r[3], 3), fmt(r[1], 3)] for r in res]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(x, y, c=INK, s=22, zorder=3)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_xticks(x)
        ax.grid(alpha=0.3)

    return Q(text=f"A regression tree (squared-error criterion) is fitted to the {n} points below. The root split "
                  f"“x ≤ t” is chosen among midpoints of consecutive x values to minimise the total SSE of the two "
                  f"children (each child predicts its mean). Find {ask}. {nat_hint(d)}",
             qtype="NAT", marks=2, answer=ansr, nat_hint=nat_hint(d),
             blocks=[Table([["x"] + [fmt(v_) for v_ in x], ["y"] + [fmt(v_) for v_ in y]], header=False),
                     Figure(draw, 7.5, 4.5)],
             solution=[f"Parent mean ȳ = {fmt(y.mean(), 3)}, SSE<sub>0</sub> = Σ(y − ȳ)² = {fmt(sse0, 3)}.",
                       "Evaluate every split:", Table(rows),
                       f"Best split t = {fmt(t, 1)}: left mean {fmt(mL, 3)}, right mean {fmt(mR, 3)}, "
                       f"SSE = {fmt(sb, 3)}, reduction = {fmt(sse0 - sb, 3)}.",
                       f"Answer: <b>{fmt(ans, d)}</b>."])


def _rand_tree_cat(rng):
    idx = rng.choice(len(_ATTRS), 3, replace=False)
    A = [_ATTRS[i] for i in idx]
    if len(A[0][1]) == 2:
        # ensure 3-valued root for variety
        for i in range(len(_ATTRS)):
            if len(_ATTRS[i][1]) == 3 and _ATTRS[i] not in A:
                A[0] = _ATTRS[i]
                break
    rootn, rv = A[0]
    leafbranch = int(rng.integers(3))
    sub = {}
    for j, vv in enumerate(rv):
        if j == leafbranch:
            sub[vv] = ("leaf", _pick(rng, ["Yes", "No"]))
        else:
            an, av = A[1] if j == (leafbranch + 1) % 3 else A[2]
            l1 = _pick(rng, ["Yes", "No"])
            labs = {av[0]: l1, av[1] if len(av) > 1 else av[0]: "No" if l1 == "Yes" else "Yes"}
            for extra in av[2:]:
                labs[extra] = _pick(rng, ["Yes", "No"])
            sub[vv] = ("split", an, av, labs)
    children = []
    for vv in rv:
        s = sub[vv]
        if s[0] == "leaf":
            children.append((vv, _node(s[1])))
        else:
            children.append((vv, _node(s[1], [(a_, _node(s[3][a_])) for a_ in s[2]])))
    root = _node(rootn, children)
    attrs_used = [A[0], A[1], A[2]]

    def classify(r):
        s = sub[r[rootn]]
        if s[0] == "leaf":
            return s[1]
        return s[3][r[s[1]]]
    return root, attrs_used, classify


@template(TOPIC, S_STRUCT, marks=2, qtype="NAT")
def tree_training_errors(rng):
    for _ in range(1000):
        root, attrs, classify = _rand_tree_cat(rng)
        n = int(rng.integers(8, 11))
        recs = [{nm: _pick(rng, vals) for nm, vals in attrs} for _ in range(n)]
        preds = [classify(r) for r in recs]
        actual = [p if rng.random() > 0.3 else ("No" if p == "Yes" else "Yes") for p in preds]
        wrong = sum(p != a for p, a in zip(preds, actual))
        if 1 <= wrong <= n - 3:
            break
    v = int(rng.integers(3))
    if v == 0:
        ask, ans, d = "the number of records misclassified by the tree", wrong, 0
    elif v == 1:
        ask, ans, d = "the training accuracy of the tree (as a percentage)", 100 * (n - wrong) / n, 1
    else:
        tp = sum(p == "Yes" and a == "Yes" for p, a in zip(preds, actual))
        fp = sum(p == "Yes" and a == "No" for p, a in zip(preds, actual))
        if tp + fp == 0:
            ask, ans, d = "the number of records misclassified by the tree", wrong, 0
        else:
            ask, ans, d = "the precision of the tree for the class “Yes”", tp / (tp + fp), 2
    names = [a[0] for a in attrs]
    rows = [["#"] + names + ["Actual"]] + [[str(i + 1)] + [r[nm] for nm in names] + [actual[i]]
                                           for i, r in enumerate(recs)]
    srows = [["#", "Predicted", "Actual", "Correct?"]] + [[str(i + 1), preds[i], actual[i],
                                                          "yes" if preds[i] == actual[i] else "<b>no</b>"] for i in range(n)]

    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_tree(ax, root, fs=7)

    ansr = (ans, ans) if d == 0 else nat_range(ans, d, tol=0.05 if d == 1 else 0.01)
    return Q(text=f"The decision tree shown is applied to the {n} labelled records in the table (attributes not "
                  f"tested on a path are ignored). Find {ask}. {nat_hint(d)}",
             qtype="NAT", marks=2, answer=ansr, nat_hint=nat_hint(d), blocks=[Figure(draw, 10, 6.0), Table(rows)],
             solution=["Route each record from the root to a leaf:", Table(srows),
                       f"Misclassified: {wrong} of {n} (accuracy {fmt(100 * (n - wrong) / n, 2)}%). "
                       f"Answer: <b>{fmt(ans, d)}</b>."])


@template(TOPIC, S_IMP, marks=2, qtype="MSQ")
def tree_criteria_compare(rng):
    for _ in range(10000):
        P = int(_pick(rng, [20, 30, 40, 50, 60]))
        Nn = int(_pick(rng, [20, 30, 40, 50, 60]))
        par = [P, Nn]
        sp = []
        for _s in range(2):
            a = int(rng.integers(1, P))
            b = int(rng.integers(1, Nn))
            sp.append(([a, b], [P - a, Nn - b]))
        tot = P + Nn

        def gain(cr, s):
            return cr(par) - sum(sum(c) / tot * cr(c) for c in s)
        gH = [gain(_H, s) for s in sp]
        gG = [gain(_G, s) for s in sp]
        gM = [Fraction(max(par), 1) - 0 for s in sp]  # placeholder
        # exact misclassification gain using integer counts
        gM = [Fraction(tot - max(par), tot) - sum(Fraction(sum(c) - max(c), tot) for c in s) for s in sp]
        if abs(gH[0] - gH[1]) < 0.01 or abs(gG[0] - gG[1]) < 0.005:
            continue
        if min(gH) < 0.01:
            continue
        # make ties in misclassification gain more likely to appear (classic case)
        if gM[0] != gM[1] and rng.random() < 0.5:
            continue
        break
    crits = [("information gain (entropy)", gH, False), ("Gini gain", gG, False), ("misclassification-error reduction",
                                                                                    gM, True)]
    T, F = [], []
    for nm, g, exact in crits:
        a, b = g
        eq = (a == b) if exact else False
        vals = f"S1: {fmt(float(a), 4)}, S2: {fmt(float(b), 4)}."
        s1 = (f"{nm[0].upper() + nm[1:]} prefers S1 over S2.", vals)
        s2 = (f"{nm[0].upper() + nm[1:]} prefers S2 over S1.", vals)
        se = (f"{nm[0].upper() + nm[1:]} is the same for S1 and S2.", vals)
        (T if (not eq and a > b) else F).append(s1)
        (T if (not eq and b > a) else F).append(s2)
        if exact:
            (T if eq else F).append(se)
    best = 0 if gH[0] > gH[1] else 1
    T.append((f"The information gain of S{best + 1} is {fmt(gH[best], 2)} bits (to two decimals).",
              f"IG(S{best + 1}) = {fmt(gH[best], 4)}."))
    F.append((f"The information gain of S{best + 1} is {fmt(gH[best] + _pick(rng, [0.05, -0.05, 0.1]), 2)} bits "
              f"(to two decimals).", f"IG(S{best + 1}) = {fmt(gH[best], 4)}."))
    opts, ans, expl = msq_from_statements(rng, T, F)
    rows = [["Split", "Left child [+, −]", "Right child [+, −]"]] + \
           [[f"S{i + 1}", _cstr(s[0]), _cstr(s[1])] for i, s in enumerate(sp)]
    sol = [f"Parent {_cstr(par)}: H = {fmt(_H(par), 4)}, Gini = {fmt(_G(par), 4)}, error = "
           f"{fmt(_ME(par), 4)}."]
    for i, s in enumerate(sp):
        sol.append(f"S{i + 1}: children H = {fmt(_H(s[0]), 4)}, {fmt(_H(s[1]), 4)}; Gini = {fmt(_G(s[0]), 4)}, "
                   f"{fmt(_G(s[1]), 4)}; error = {fmt(_ME(s[0]), 4)}, {fmt(_ME(s[1]), 4)}. Gains: IG = {fmt(gH[i], 4)}, "
                   f"Gini = {fmt(gG[i], 4)}, error = {fmt(float(gM[i]), 4)}.")
    return Q(text=f"A node with class counts {_cstr(par)} can be split by either of two binary splits S1 or S2 "
                  f"(table). For each impurity measure, the “gain” is the parent impurity minus the weighted child "
                  f"impurity. Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[Table(rows)], solution=sol + expl)


# =============================================================================
# Ensembles
# =============================================================================
@template(TOPIC, S_BOOST, marks=1, qtype="NAT")
def adaboost_alpha(rng):
    v = int(rng.integers(3))
    if v == 0:
        eps = _pick(rng, [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.12, 0.18, 0.22])
        ans = 0.5 * math.log((1 - eps) / eps)
        text = (f"In AdaBoost, a weak learner has weighted training error ε = {fmt(eps)}. Its vote weight "
                f"α = ½ ln((1 − ε)/ε) is ______")
        sol = [f"α = ½ ln({fmt(1 - eps)}/{fmt(eps)}) = ½ ln({fmt((1 - eps) / eps, 4)}) = <b>{fmt(ans, 2)}</b>."]
    elif v == 1:
        al = _pick(rng, [0.2, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2])
        ans = 1 / (1 + math.exp(2 * al))
        text = (f"In AdaBoost (α<sub>t</sub> = ½ ln((1 − ε<sub>t</sub>)/ε<sub>t</sub>)), a weak learner received "
                f"weight α<sub>t</sub> = {fmt(al)}. Its weighted error ε<sub>t</sub> was ______")
        sol = [f"(1 − ε)/ε = e<super>2α</super> = e<super>{fmt(2 * al)}</super> = {fmt(math.exp(2 * al), 4)} ⇒ "
               f"ε = 1/(1 + e<super>2α</super>) = <b>{fmt(ans, 2)}</b>."]
    else:
        eps = _pick(rng, [0.1, 0.2, 0.25, 0.3, 0.4, 0.125])
        ans = math.sqrt((1 - eps) / eps)
        text = (f"In AdaBoost with ε<sub>t</sub> = {fmt(eps, 3)}, before normalisation each misclassified example's "
                f"weight is multiplied by e<super>α<sub>t</sub></super>, where α<sub>t</sub> = ½ ln((1 − ε<sub>t</sub>)/"
                f"ε<sub>t</sub>). This multiplying factor is ______")
        sol = [f"e<super>α</super> = e<super>½ ln((1−ε)/ε)</super> = √((1 − ε)/ε) = √({fmt((1 - eps) / eps, 4)}) "
               f"= <b>{fmt(ans, 2)}</b>.",
               "Correctly classified examples are multiplied by e<super>−α</super> = √(ε/(1 − ε))."]
    return Q(text=text + " " + nat_hint(2), qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             solution=sol + ["ε &lt; 0.5 ⇒ α &gt; 0; ε = 0.5 ⇒ α = 0 (no better than chance)."])


@template(TOPIC, S_BOOST, marks=2, qtype="NAT")
def adaboost_reweight(rng):
    v = int(rng.integers(4))
    if v == 3:
        T = 3
        eps = [_pick(rng, [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]) for _ in range(T)]
        al = [0.5 * math.log((1 - e) / e) for e in eps]
        while True:
            h = [int(rng.choice([-1, 1])) for _ in range(T)]
            s = sum(a * hh for a, hh in zip(al, h))
            if len(set(h)) == 2 and abs(s) > 0.02:
                break
        rows = [["Round t", "ε<sub>t</sub>", "h<sub>t</sub>(x)"]] + [[str(i + 1), fmt(eps[i]), "+1" if h[i] > 0 else "−1"]
                                                                  for i in range(T)]
        return Q(text=f"An AdaBoost ensemble has three weak classifiers with the weighted errors below, and their "
                      f"predictions on a test point x are listed. The ensemble score F(x) = Σ α<sub>t</sub> "
                      f"h<sub>t</sub>(x), with α<sub>t</sub> = ½ ln((1 − ε<sub>t</sub>)/ε<sub>t</sub>), is ______ "
                      f"{nat_hint(2)}",
                 qtype="NAT", marks=2, answer=nat_range(s, 2), nat_hint=nat_hint(2), blocks=[Table(rows)],
                 solution=["α<sub>t</sub>: " + ", ".join(f"α<sub>{i + 1}</sub> = {fmt(a, 4)}" for i, a in enumerate(al)) + ".",
                           "F(x) = " + " ".join(("+ " if hh > 0 else "− ") + fmt(a, 4) for a, hh in zip(al, h)) +
                           f" = <b>{fmt(s, 2)}</b>; prediction sign(F) = {'+1' if s > 0 else '−1'}.",
                           "Note that a majority of weak votes need not win: a low-error learner carries a larger α."])
    while True:
        n = int(rng.integers(5, 9))
        uniform = rng.random() < 0.4
        if uniform:
            w = np.full(n, 1 / n)
        else:
            raw = rng.integers(1, 6, size=n).astype(float)
            w = raw / raw.sum()
        mis = np.zeros(n, bool)
        m = int(rng.integers(1, max(2, n // 2)))
        mis[rng.choice(n, m, replace=False)] = True
        eps = float(w[mis].sum())
        if 0.05 < eps < 0.45:
            break
    al = 0.5 * math.log((1 - eps) / eps)
    wn = w * np.exp(np.where(mis, al, -al))
    Z = wn.sum()
    wn /= Z
    j_mis = int(np.where(mis)[0][0])
    j_cor = int(np.where(~mis)[0][0])
    if v == 0:
        j = j_mis
        ask, ans = f"the normalised weight of example {j + 1} for the next round", float(wn[j])
    elif v == 1:
        j = j_cor
        ask, ans = f"the normalised weight of example {j + 1} for the next round", float(wn[j])
    else:
        ask, ans = "the normalisation constant Z = Σ<sub>i</sub> w<sub>i</sub>·exp(−α y<sub>i</sub>h(x<sub>i</sub>))", \
            float(Z)
    wshow = [_q(x_, 100) for x_ in w]
    rows = [["Example i"] + [str(i + 1) for i in range(n)],
            ["Weight w<sub>i</sub>"] + wshow,
            ["h(x<sub>i</sub>) correct?"] + ["No" if mm else "Yes" for mm in mis]]
    return Q(text=f"In one AdaBoost round the current example weights and whether the chosen weak classifier h "
                  f"classifies each example correctly are given. Using α = ½ ln((1 − ε)/ε) and the update "
                  f"w<sub>i</sub> ← w<sub>i</sub>·exp(−α y<sub>i</sub>h(x<sub>i</sub>))/Z, find {ask}. "
                  f"{nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, tol=0.002), nat_hint=nat_hint(3), blocks=[Table(rows)],
             solution=[f"ε = Σ<sub>misclassified</sub> w<sub>i</sub> = {fmt(eps, 4)}; α = ½ ln({fmt(1 - eps, 4)}/"
                       f"{fmt(eps, 4)}) = {fmt(al, 4)}.",
                       f"Misclassified weights × e<super>α</super> = {fmt(math.exp(al), 4)}; correct weights × "
                       f"e<super>−α</super> = {fmt(math.exp(-al), 4)}.",
                       f"Z = ε e<super>α</super> + (1 − ε) e<super>−α</super> = 2√(ε(1 − ε)) = {fmt(Z, 4)}.",
                       "New weights: " + ", ".join(fmt(x_, 4) for x_ in wn) + ".",
                       "Shortcut: after normalisation the misclassified set has total weight exactly ½: "
                       "w<sub>i</sub>' = w<sub>i</sub>/(2ε) if misclassified, w<sub>i</sub>/(2(1 − ε)) otherwise.",
                       f"Answer: <b>{fmt(ans, 3)}</b>."])


@template(TOPIC, S_BAG, marks=1, qtype="NAT")
def bagging_oob(rng):
    v = int(rng.integers(4))
    if v == 0:
        n = int(_pick(rng, [3, 4, 5, 6, 8, 10]))
        ans = (1 - 1 / n) ** n
        text = (f"A bootstrap sample of size n = {n} is drawn with replacement from a training set of {n} distinct "
                f"points. The probability that a particular point is NOT in the sample (i.e. is out-of-bag) is ______")
        sol = [f"Each draw misses the point with probability 1 − 1/{n}; {n} independent draws: "
               f"(1 − 1/{n})<super>{n}</super> = <b>{fmt(ans, 3)}</b> (→ 1/e ≈ 0.368 as n → ∞)."]
        d = 3
    elif v == 1:
        n = int(_pick(rng, [4, 5, 6, 10]))
        ans = n * (1 - (1 - 1 / n) ** n)
        text = (f"A bootstrap sample of size {n} is drawn with replacement from {n} distinct training points. The "
                f"expected number of distinct points appearing in the sample is ______")
        sol = [f"By linearity: n·P(point appears) = {n}·[1 − (1 − 1/{n})<super>{n}</super>] = <b>{fmt(ans, 3)}</b>."]
        d = 2
    elif v == 2:
        p = int(_pick(rng, [16, 25, 36, 49, 50, 64, 80, 100, 120]))
        m = int(math.floor(math.sqrt(p)))
        ans = m / p
        text = (f"A random forest for classification on p = {p} features uses the common default of m = ⌊√p⌋ "
                f"candidate features (sampled uniformly without replacement) at each split. The probability that a "
                f"particular feature is among the candidates at a given split is ______")
        sol = [f"m = ⌊√{p}⌋ = {m}. P(feature selected) = m/p = {m}/{p} = <b>{fmt(ans, 3)}</b>."]
        d = 3
    else:
        N = int(_pick(rng, [500, 1000, 2000, 5000, 10000]))
        ans = N * math.exp(-1)
        text = (f"A bagged ensemble is trained on N = {N} points. Using the large-N approximation, the expected "
                f"number of training points that are out-of-bag for a single bootstrap sample of size N is ______")
        sol = [f"P(out-of-bag) = (1 − 1/N)<super>N</super> ≈ e<super>−1</super> ≈ 0.3679; expected count ≈ "
               f"{N} × 0.3679 = <b>{fmt(ans, 0)}</b>."]
        d = 0
        return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1,
                 answer=(math.floor(ans) - 1, math.ceil(ans) + 1), nat_hint=nat_hint(0), solution=sol)
    tol = 10 ** (-d) * (2 if d == 3 else 1)
    return Q(text=text + " " + nat_hint(d), qtype="NAT", marks=1, answer=nat_range(ans, d, tol=tol),
             nat_hint=nat_hint(d), solution=sol)


_ENS_T = [
    ("Bagging mainly reduces the variance of the base learner.", "Averaging bootstrap models smooths fluctuations."),
    ("For large n, a bootstrap sample omits about 36.8% of the training points.", "(1 − 1/n)<super>n</super> → 1/e."),
    ("Out-of-bag error gives an estimate of test error without a separate validation set.",
     "Each point is predicted by trees that did not see it."),
    ("Random forests decorrelate trees by considering a random subset of features at each split.",
     "Feature subsampling reduces correlation between trees."),
    ("A common default for random-forest classification is m ≈ √p features per split.", "Breiman's recommendation."),
    ("Boosting fits base learners sequentially, each focusing on examples the previous ones handled poorly.",
     "Via reweighting (AdaBoost) or residual fitting."),
    ("AdaBoost gives weak learner t the weight α<sub>t</sub> = ½ ln((1 − ε<sub>t</sub>)/ε<sub>t</sub>).",
     "Standard binary AdaBoost."),
    ("In AdaBoost, the weights of misclassified examples increase for the next round.", "Multiplied by e<super>α</super>."),
    ("Boosting with weak learners such as stumps primarily reduces bias.", "It builds a strong additive model."),
    ("AdaBoost can be viewed as stagewise minimisation of the exponential loss.", "Friedman, Hastie &amp; Tibshirani."),
    ("A weak learner with weighted error ε<sub>t</sub> = 0.5 receives α<sub>t</sub> = 0.", "ln(1) = 0."),
    ("Bagged trees can be trained in parallel, whereas boosting is inherently sequential.",
     "Boosting needs the previous round's weights."),
    ("A random forest with m = p (all features considered at each split) is equivalent to bagged trees.",
     "No feature subsampling."),
    ("Averaging B independent predictors, each with variance σ², gives variance σ²/B.", "Variance of a mean."),
    ("AdaBoost is sensitive to label noise because the weights of persistently misclassified points grow "
     "exponentially.", "Outliers get dominant weight."),
    ("After an AdaBoost reweighting step, the misclassified examples carry exactly half of the total weight.",
     "w' = w/(2ε) for misclassified points."),
]
_ENS_F = [
    ("Bagging is mainly used to reduce the bias of high-bias learners such as decision stumps.",
     "Bagging reduces variance; boosting reduces bias."),
    ("Every bootstrap sample contains each training point exactly once.", "Sampling is with replacement."),
    ("About 63.2% of the training points are out-of-bag for a given bootstrap sample.",
     "≈ 63.2% are in-bag; ≈ 36.8% are out-of-bag."),
    ("A random forest considers all features at every split.", "It samples m &lt; p features."),
    ("In AdaBoost, the weights of correctly classified examples increase.", "They decrease (× e<super>−α</super>)."),
    ("AdaBoost trains its weak learners independently and in parallel.", "It is sequential."),
    ("A weak learner with weighted error 0.3 receives a negative α in AdaBoost.",
     "α = ½ ln(0.7/0.3) &gt; 0."),
    ("Boosting can never overfit, however many rounds are used.", "It can overfit, especially with noisy labels."),
    ("Averaging B identically distributed predictors with pairwise correlation ρ &gt; 0 gives variance σ²/B.",
     "Variance is ρσ² + (1 − ρ)σ²/B."),
    ("Out-of-bag error estimation requires a held-out test set.", "It uses the out-of-bag points themselves."),
    ("Bagging helps most for stable, low-variance learners such as linear regression.",
     "It helps most for unstable learners like deep trees."),
    ("Random forests reduce variance by making the individual trees more correlated.", "They de-correlate them."),
    ("In AdaBoost, α<sub>t</sub> increases as ε<sub>t</sub> increases (for ε<sub>t</sub> &lt; 0.5).",
     "α decreases as ε increases."),
    ("Bagging draws bootstrap samples of size n without replacement.", "Without replacement it would reproduce the data."),
    ("AdaBoost requires weak learners whose error is strictly greater than 0.5.", "It needs error below 0.5."),
]


@template(TOPIC, S_BAG, marks=1, qtype="MSQ")
def ensemble_concepts_msq(rng):
    opts, ans, expl = msq_from_statements(rng, _ENS_T, _ENS_F)
    return Q(text="Which of the following statements about bagging, random forests and boosting is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_BAG, marks=2, qtype="NAT")
def ensemble_majority_vote(rng):
    v = int(rng.integers(3))
    m = int(_pick(rng, [3, 5, 7]))
    p = _pick(rng, [0.6, 0.65, 0.7, 0.75, 0.8])
    k0 = m // 2 + 1
    acc = sum(math.comb(m, k) * p ** k * (1 - p) ** (m - k) for k in range(k0, m + 1))
    terms = " + ".join(f"C({m},{k})({fmt(p)})<super>{k}</super>({fmt(1 - p)})<super>{m - k}</super>"
                       for k in range(k0, m + 1))
    if v == 0:
        ask, ans = "the probability that the majority vote is correct", acc
    elif v == 1:
        ask, ans = "the error rate of the majority-vote ensemble", 1 - acc
    else:
        rho = _pick(rng, [0.2, 0.3, 0.5])
        B = int(_pick(rng, [5, 10, 20, 50]))
        s2 = _pick(rng, [1, 2, 4])
        ans = rho * s2 + (1 - rho) * s2 / B
        return Q(text=f"B = {B} regression trees are averaged. Each tree's prediction has variance σ² = {fmt(s2)}, "
                      f"and every pair of trees has correlation ρ = {fmt(rho)}. The variance of the averaged "
                      f"prediction is ______ {nat_hint(2)}",
                 qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
                 solution=["Var((1/B)Σf<sub>b</sub>) = (1/B²)[Bσ² + B(B − 1)ρσ²] = ρσ² + (1 − ρ)σ²/B.",
                           f"= {fmt(rho)}×{fmt(s2)} + {fmt(1 - rho)}×{fmt(s2)}/{B} = {fmt(rho * s2, 4)} + "
                           f"{fmt((1 - rho) * s2 / B, 4)} = <b>{fmt(ans, 2)}</b>.",
                           f"Even with B → ∞ the variance cannot fall below ρσ² = {fmt(rho * s2, 3)} — which is why "
                           f"random forests try to reduce ρ by feature subsampling."])
    return Q(text=f"An ensemble combines {m} binary classifiers by majority vote. Each classifier is correct with "
                  f"probability {fmt(p)}, independently of the others. Compute {ask}. {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, tol=0.002), nat_hint=nat_hint(3),
             solution=[f"The vote is correct when at least {k0} of {m} classifiers are correct (Binomial({m}, {fmt(p)})).",
                       f"P(correct) = {terms} = {fmt(acc, 4)}.",
                       f"Answer: <b>{fmt(ans, 3)}</b>. Independence is crucial — correlated classifiers gain much less."])
