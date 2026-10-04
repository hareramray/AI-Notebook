"""Unsupervised Learning: k-means, k-medoids, hierarchical clustering, distance measures,
cluster evaluation and PCA / dimensionality reduction.

All numeric answers are computed in code; random data is re-sampled whenever a tie or an
ill-conditioned situation would make the answer ambiguous.  Only numpy + matplotlib are used.
"""
import math
from itertools import combinations

import numpy as np

from core import (Figure, Matrix, Q, Table, fmt, mcq, msq_from_statements, nat_hint, nat_range,
                  template)

TOPIC = "Unsupervised Learning"

SUB_KM = "k-means"
SUB_KMED = "k-medoids"
SUB_HC = "Hierarchical clustering"
SUB_DIST = "Distance measures"
SUB_EVAL = "Cluster evaluation"
SUB_PCA = "PCA & dimensionality reduction"

MARKERS = ["o", "s", "^", "D", "v", "P"]
GREYS = ["#222222", "#777777", "#aaaaaa", "#444444", "#999999", "#555555"]


# ============================================================================
# Generic helpers (local to this module)
# ============================================================================
def _names(n, prefix="P"):
    return [f"{prefix}{i + 1}" for i in range(n)]


def _pt(p):
    return "(" + ", ".join(fmt(v, 2) for v in p) + ")"


def _sq(p, q):
    p, q = np.asarray(p, float), np.asarray(q, float)
    return float(((p - q) ** 2).sum())


def _dist(p, q, metric="euclidean"):
    p, q = np.asarray(p, float), np.asarray(q, float)
    if metric == "manhattan":
        return float(np.abs(p - q).sum())
    if metric == "chebyshev":
        return float(np.abs(p - q).max())
    return float(np.sqrt(((p - q) ** 2).sum()))


def _points_table(names, P, cols=("x₁", "x₂")):
    P = np.atleast_2d(P)
    rows = [["Point"] + list(names)]
    for j, c in enumerate(cols):
        rows.append([c] + [fmt(v, 2) for v in P[:, j]])
    return Table(rows, header=False)


def _dist_table(D, names, d=0):
    n = len(names)
    rows = [[""] + list(names)]
    for i in range(n):
        rows.append([names[i]] + [fmt(D[i][j], d) if j >= i else "" for j in range(n)])
    # show the upper triangle only (incl. diagonal zeros) – symmetric matrix
    return Table(rows, header=True)


def _scatter_labeled(ax, P, names, groups=None, offset=(0.15, 0.15), size=26):
    P = np.asarray(P, float)
    if groups is None:
        groups = [0] * len(P)
    for g in sorted(set(groups)):
        idx = [i for i in range(len(P)) if groups[i] == g]
        ax.scatter(P[idx, 0], P[idx, 1], s=size, marker=MARKERS[g % 6], color=GREYS[g % 6],
                   edgecolor="black", linewidth=0.5, zorder=3)
    for i, nm in enumerate(names):
        ax.annotate(nm, (P[i, 0], P[i, 1]), xytext=(3, 3), textcoords="offset points", fontsize=7)


def _int_grid(ax, P, pad=1):
    P = np.asarray(P, float)
    ax.set_xlim(P[:, 0].min() - pad, P[:, 0].max() + pad)
    ax.set_ylim(P[:, 1].min() - pad, P[:, 1].max() + pad)
    ax.grid(alpha=0.3)
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")


def _part_str(clusters, names):
    cl = sorted([sorted(c) for c in clusters], key=lambda c: c[0])
    return ", ".join("{" + ", ".join(names[i] for i in c) + "}" for c in cl)


def _distinct_ints(rng, lo, hi, n):
    return np.sort(rng.choice(np.arange(lo, hi + 1), n, replace=False)).astype(float)


def _strip(ax, x, names=None, marks=None, mark_label="initial centroid"):
    """1-D strip plot of points x, optionally marking special positions with triangles."""
    x = np.asarray(x, float)
    ax.axhline(0, color="#888888", lw=0.8, zorder=1)
    ax.scatter(x, np.zeros_like(x), s=28, color="#333333", zorder=3)
    if names is not None:
        for xi, nm in zip(x, names):
            ax.annotate(nm, (xi, 0), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=6.5)
    if marks is not None:
        ax.scatter(marks, np.zeros(len(marks)) - 0.35, marker="^", s=55, color="white", edgecolor="black",
                   zorder=4, label=mark_label)
        ax.legend(loc="upper right", frameon=False)
    lo, hi = x.min(), x.max()
    if marks is not None:
        lo, hi = min(lo, min(marks)), max(hi, max(marks))
    ax.set_xlim(lo - 1.5, hi + 1.5)
    ax.set_ylim(-0.8, 0.8)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    span = int(hi - lo) + 4
    step = next(st for st in (1, 2, 5, 10, 20) if span / st <= 16)
    start = math.floor(lo) - 1
    start -= start % step
    ax.set_xticks(np.arange(start, math.ceil(hi) + 2, step))
    ax.set_xlabel("x")


# ----------------------------------------------------------------------------
# Hierarchical clustering helpers
# ----------------------------------------------------------------------------
def _link(D, A, B, method):
    vals = [D[i][j] for i in A for j in B]
    if method == "single":
        return min(vals)
    if method == "complete":
        return max(vals)
    return sum(vals) / len(vals)


def _hclust(D, method, tol=1e-6):
    """Agglomerative clustering; returns list of (A, B, height) with frozensets, or None on a tie."""
    n = len(D)
    clusters = [frozenset([i]) for i in range(n)]
    merges = []
    while len(clusters) > 1:
        cand = []
        for a, b in combinations(range(len(clusters)), 2):
            cand.append((_link(D, clusters[a], clusters[b], method), a, b))
        cand.sort(key=lambda t: t[0])
        if len(cand) > 1 and cand[1][0] - cand[0][0] < tol:
            return None
        h, a, b = cand[0]
        A, B = clusters[a], clusters[b]
        merges.append((A, B, h))
        clusters = [c for k, c in enumerate(clusters) if k not in (a, b)] + [A | B]
    return merges


def _clusters_k(merges, n, k):
    clusters = [frozenset([i]) for i in range(n)]
    for A, B, h in merges[: n - k]:
        clusters = [c for c in clusters if c != A and c != B] + [A | B]
    return clusters


def _coph(merges, i, j):
    for A, B, h in merges:
        if (i in A and j in B) or (i in B and j in A):
            return h
    return None


def _draw_dendro(ax, merges, names, ylabel="height"):
    n = len(names)
    children = {A | B: (A, B, h) for A, B, h in merges}
    root = merges[-1][0] | merges[-1][1]

    def order(S):
        if len(S) == 1:
            return list(S)
        A, B, _ = children[S]
        return order(A) + order(B)

    leaves = order(root)
    pos = {frozenset([leaf]): (x, 0.0) for x, leaf in enumerate(leaves)}
    for A, B, h in merges:
        xa, ha = pos[A]
        xb, hb = pos[B]
        ax.plot([xa, xa], [ha, h], color="black", lw=1)
        ax.plot([xb, xb], [hb, h], color="black", lw=1)
        ax.plot([xa, xb], [h, h], color="black", lw=1)
        pos[A | B] = ((xa + xb) / 2, h)
    ax.set_xticks(range(n))
    ax.set_xticklabels([names[i] for i in leaves])
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(0, merges[-1][2] * 1.08)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.35)


def _manhattan_points(rng, n, lo=0, hi=10):
    while True:
        P = rng.integers(lo, hi + 1, size=(n, 2)).astype(float)
        if len({tuple(p) for p in P}) == n:
            return P


def _pairwise(P, metric):
    n = len(P)
    return [[_dist(P[i], P[j], metric) for j in range(n)] for i in range(n)]


def _merge_lines(merges, names, d=2):
    out = []
    for s, (A, B, h) in enumerate(merges, 1):
        out.append(f"Merge {s}: {{{', '.join(names[i] for i in sorted(A))}}} + "
                   f"{{{', '.join(names[i] for i in sorted(B))}}} at height <b>{fmt(h, d)}</b>")
    return out


LINK_DEF = {
    "single": "single linkage: d(A,B) = min<sub>a∈A, b∈B</sub> d(a,b)",
    "complete": "complete linkage: d(A,B) = max<sub>a∈A, b∈B</sub> d(a,b)",
    "average": "average linkage (UPGMA): d(A,B) = (1/|A||B|) Σ<sub>a∈A</sub>Σ<sub>b∈B</sub> d(a,b)",
}


def _hc_instance(rng, n, method, metric="manhattan"):
    while True:
        P = _manhattan_points(rng, n, 0, 9)
        D = _pairwise(P, metric)
        m = _hclust(D, method)
        if m is not None:
            return P, D, m


# ============================================================================
# k-MEANS
# ============================================================================
def _kmeans_assign(X, C):
    """Return labels or None if any point is (near) equidistant to two centroids."""
    labs = []
    for x in X:
        d = sorted((_sq(x, c), j) for j, c in enumerate(C))
        if len(d) > 1 and d[1][0] - d[0][0] < 1e-6:
            return None
        labs.append(d[0][1])
    return labs


@template(TOPIC, SUB_KM, marks=2, qtype="NAT")
def kmeans_iter_2d(rng):
    while True:
        n = int(rng.integers(7, 9))
        k = int(rng.choice([2, 2, 3]))
        X = _manhattan_points(rng, n, 0, 10)
        C0 = rng.integers(0, 11, size=(k, 2)).astype(float)
        if len({tuple(c) for c in C0}) < k:
            continue
        l1 = _kmeans_assign(X, C0)
        if l1 is None or len(set(l1)) < k:
            continue
        C1 = np.array([X[[i for i in range(n) if l1[i] == j]].mean(axis=0) for j in range(k)])
        l2 = _kmeans_assign(X, C1)
        if l2 is None or len(set(l2)) < k:
            continue
        C2 = np.array([X[[i for i in range(n) if l2[i] == j]].mean(axis=0) for j in range(k)])
        variant = int(rng.integers(0, 4))
        changed = sum(1 for a, b in zip(l1, l2) if a != b)
        if variant == 2 and changed == 0:
            continue
        break
    names = _names(n)
    cn = [f"C{j + 1}" for j in range(k)]
    j = int(rng.integers(0, k))
    coord = int(rng.integers(0, 2))
    sse1 = sum(_sq(X[i], C1[l1[i]]) for i in range(n))
    if variant == 0:
        val, d = C1[j, coord], 2
        ask = (f"After <b>one</b> iteration (assignment step followed by update step), the "
               f"x<sub>{coord + 1}</sub>-coordinate of the updated centroid of cluster {cn[j]} is ______")
    elif variant == 1:
        val, d = sse1, 2
        ask = ("After <b>one</b> iteration (assignment step followed by update step), the within-cluster sum of "
               "squared Euclidean distances J = Σ<sub>i</sub>‖x<sub>i</sub> − μ<sub>c(i)</sub>‖², computed with the "
               "<i>updated</i> centroids and the assignments of that iteration, is ______")
    elif variant == 2:
        val, d = changed, 0
        ask = ("The number of points whose cluster membership <b>changes</b> in the second iteration "
               "(compared with the first-iteration assignment) is ______")
    else:
        val, d = C2[j, coord], 2
        ask = (f"After <b>two</b> iterations, the x<sub>{coord + 1}</sub>-coordinate of the centroid of cluster "
               f"{cn[j]} is ______")

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, X, names)
        for jj in range(k):
            ax.scatter(C0[jj, 0], C0[jj, 1], marker="X", s=90, color="white", edgecolor="black", lw=1.2, zorder=4)
            ax.annotate(cn[jj], (C0[jj, 0], C0[jj, 1]), xytext=(4, -10), textcoords="offset points",
                        fontsize=7.5, fontweight="bold")
        _int_grid(ax, np.vstack([X, C0]))
        ax.set_title("data points (•) and initial centroids (×)")

    def assign_table(C, labs):
        rows = [["Point"] + [f"d²(·,{c})" for c in cn] + ["cluster"]]
        for i in range(n):
            rows.append([f"{names[i]} {_pt(X[i])}"] + [fmt(_sq(X[i], C[jj]), 2) for jj in range(k)] + [cn[labs[i]]])
        return Table(rows, header=True)

    sol = ["<b>Iteration 1 – assignment</b> (nearest initial centroid, squared Euclidean distance):",
           assign_table(C0, l1),
           "<b>Update</b>: each centroid becomes the mean of its assigned points: "
           + "; ".join(f"{cn[jj]} → {_pt(C1[jj])}" for jj in range(k)) + "."]
    if variant == 1:
        sol.append(f"J = Σ‖x<sub>i</sub> − μ<sub>c(i)</sub>‖² with the new centroids = <b>{fmt(sse1, 2)}</b>.")
    if variant in (2, 3):
        sol += ["<b>Iteration 2 – assignment</b> with the updated centroids:", assign_table(C1, l2)]
        if variant == 2:
            ch = [names[i] for i in range(n) if l1[i] != l2[i]]
            sol.append(f"Points that changed cluster: {', '.join(ch)} → answer <b>{changed}</b>.")
        else:
            sol.append("<b>Update</b>: " + "; ".join(f"{cn[jj]} → {_pt(C2[jj])}" for jj in range(k))
                       + f". Required coordinate = <b>{fmt(val, 2)}</b>.")
    if variant == 0:
        sol.append(f"Required coordinate = <b>{fmt(val, 2)}</b>.")
    sol.append("Note: each step of Lloyd's algorithm can only decrease (or keep) J, which is why it converges.")
    return Q(text=f"k-means (Lloyd's algorithm, Euclidean distance) with k = {k} is run on the {n} points below, "
                  f"starting from the initial centroids "
                  + ", ".join(f"{cn[jj]} = {_pt(C0[jj])}" for jj in range(k)) + ". " + ask + " " + nat_hint(d),
             qtype="NAT", marks=2, answer=nat_range(val, d) if d else (val, val), nat_hint=nat_hint(d),
             blocks=[_points_table(names, X), Figure(draw, 8.5, 6)], solution=sol)


def _lloyd_1d(x, c, max_it=30):
    """Run 1-D Lloyd; returns (history of (centroids, labels)) or None on tie / empty cluster."""
    hist = []
    c = np.array(c, float)
    for _ in range(max_it):
        labs = _kmeans_assign(x[:, None], c[:, None])
        if labs is None or len(set(labs)) < len(c):
            return None
        newc = np.array([x[[i for i in range(len(x)) if labs[i] == j]].mean() for j in range(len(c))])
        hist.append((c.copy(), labs, newc))
        if np.allclose(newc, c):
            return hist
        c = newc
    return None


@template(TOPIC, SUB_KM, marks=2, qtype="NAT")
def kmeans_converge_1d(rng):
    while True:
        n = int(rng.integers(7, 9))
        x = _distinct_ints(rng, 0, 24, n)
        c0 = np.sort(rng.choice(np.arange(0, 25), 2, replace=False)).astype(float)
        hist = _lloyd_1d(x, c0)
        if hist is None:
            continue
        moved = sum(1 for (c, l, nc) in hist if not np.allclose(c, nc))
        if moved < 2:
            continue
        break
    cf, lf, _ = hist[-1]
    sse = sum((x[i] - cf[lf[i]]) ** 2 for i in range(n))
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val, d, ask = cf[1], 2, "the <b>larger</b> of the two final centroids is ______"
    elif variant == 1:
        val, d, ask = sse, 2, "the final within-cluster sum of squared errors (SSE) is ______"
    else:
        val, d, ask = moved, 0, ("the number of iterations in which at least one centroid <b>changes</b> its value "
                                 "is ______")
    names = _names(n, "x")

    def draw(fig):
        ax = fig.add_subplot(111)
        _strip(ax, x, None, c0)

    sol = [f"Data: {{{', '.join(fmt(v) for v in x)}}}; initial centroids c₁ = {fmt(c0[0])}, c₂ = {fmt(c0[1])}."]
    rows = [["Iter", "centroids used", "cluster 1", "cluster 2", "new centroids"]]
    for t, (c, l, nc) in enumerate(hist, 1):
        g1 = [fmt(x[i]) for i in range(n) if l[i] == 0]
        g2 = [fmt(x[i]) for i in range(n) if l[i] == 1]
        rows.append([str(t), f"{fmt(c[0], 2)}, {fmt(c[1], 2)}", "{" + ", ".join(g1) + "}",
                     "{" + ", ".join(g2) + "}", f"{fmt(nc[0], 2)}, {fmt(nc[1], 2)}"])
    sol.append(Table(rows, header=True))
    sol.append(f"In the last row the centroids do not change, so the algorithm has converged: final centroids "
               f"{fmt(cf[0], 2)} and {fmt(cf[1], 2)}.")
    if variant == 1:
        terms = " + ".join(f"({fmt(x[i])} − {fmt(cf[lf[i]], 2)})²" for i in range(n))
        sol.append(f"SSE = {terms} = <b>{fmt(sse, 2)}</b>.")
    elif variant == 0:
        sol.append(f"Larger final centroid = <b>{fmt(val, 2)}</b>.")
    else:
        sol.append(f"Centroids changed in {moved} iteration(s); the final iteration only confirms convergence. "
                   f"Answer <b>{moved}</b>.")
    return Q(text=f"The 1-D dataset {{{', '.join(fmt(v) for v in x)}}} is clustered with k-means (k = 2) using "
                  f"initial centroids {fmt(c0[0])} and {fmt(c0[1])} (shown as triangles). Lloyd's iterations "
                  f"(assign to nearest centroid, then recompute means) are run until convergence. Then "
                  + ask + " " + nat_hint(d),
             qtype="NAT", marks=2, answer=nat_range(val, d) if d else (val, val), nat_hint=nat_hint(d),
             blocks=[Figure(draw, 9, 3.2)], solution=sol)


@template(TOPIC, SUB_KM, marks=1, qtype="NAT")
def kmeans_assign_sse(rng):
    while True:
        k = int(rng.choice([2, 3]))
        n = int(rng.integers(6, 8))
        x = _distinct_ints(rng, 0, 20, n)
        c = np.sort(rng.choice(np.arange(0, 21), k, replace=False)).astype(float)
        labs = _kmeans_assign(x[:, None], c[:, None])
        if labs is None or len(set(labs)) < k:
            continue
        break
    sse = sum((x[i] - c[labs[i]]) ** 2 for i in range(n))
    variant = int(rng.integers(0, 2))
    if variant == 0:
        val = sse
        ask = ("Each point is assigned to its nearest centroid (centroids are <b>not</b> updated). The resulting "
               "within-cluster sum of squared errors Σ(x<sub>i</sub> − c<sub>c(i)</sub>)² is ______")
    else:
        newc = np.array([x[[i for i in range(n) if labs[i] == j]].mean() for j in range(k)])
        val = sum((x[i] - newc[labs[i]]) ** 2 for i in range(n))
        ask = ("Each point is assigned to its nearest centroid and then each centroid is recomputed as the mean of its "
               "points. The within-cluster SSE with the <b>updated</b> centroids is ______")

    def draw(fig):
        ax = fig.add_subplot(111)
        _strip(ax, x, None, c, "centroid")

    sol = ["Assignment (nearest centroid): " + "; ".join(
        f"c = {fmt(c[j])}: {{{', '.join(fmt(x[i]) for i in range(n) if labs[i] == j)}}}" for j in range(k)) + "."]
    if variant == 0:
        sol.append("SSE = " + " + ".join(f"({fmt(x[i])}−{fmt(c[labs[i]])})²" for i in range(n))
                   + f" = <b>{fmt(val, 2)}</b>.")
    else:
        sol.append("Updated centroids (cluster means): " + ", ".join(fmt(v, 2) for v in newc) + ".")
        sol.append("SSE = " + " + ".join(f"({fmt(x[i])}−{fmt(newc[labs[i]], 2)})²" for i in range(n))
                   + f" = <b>{fmt(val, 2)}</b>.")
        sol.append(f"(With the old centroids the SSE was {fmt(sse, 2)}; the update step can only lower it.)")
    return Q(text=f"One-dimensional data {{{', '.join(fmt(v) for v in x)}}} and k = {k} centroids at "
                  f"{', '.join(fmt(v) for v in c)} are given. " + ask + " " + nat_hint(2),
             qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[Figure(draw, 9, 3)], solution=sol)


@template(TOPIC, SUB_KM, marks=2, qtype="NAT")
def kmeans_plusplus(rng):
    while True:
        n = 6
        X = _manhattan_points(rng, n, 0, 8)
        variant = int(rng.integers(0, 2))
        idx = rng.permutation(n)
        chosen = [int(idx[0])] if variant == 0 else [int(idx[0]), int(idx[1])]
        D2 = np.array([min(_sq(X[i], X[c]) for c in chosen) for i in range(n)])
        cand = [i for i in range(n) if i not in chosen]
        target = int(rng.choice(cand))
        p = D2[target] / D2.sum()
        if 0.03 < p < 0.97:
            break
    names = _names(n)
    chs = " and ".join(names[c] for c in chosen)
    which = "second" if variant == 0 else "third"

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, X, names)
        for c in chosen:
            ax.scatter(X[c, 0], X[c, 1], s=150, facecolor="none", edgecolor="black", lw=1.3, zorder=4)
        _int_grid(ax, X)
        ax.set_title("circled: centre(s) already chosen")

    rows = [["Point"] + names, ["D(x)²"] + [fmt(v, 2) for v in D2]]
    sol = ["k-means++ picks the next centre x with probability D(x)² / Σ<sub>x′</sub> D(x′)², where D(x) is the "
           "distance from x to the <b>nearest</b> centre already chosen (chosen centres have D = 0).",
           Table(rows, header=False),
           f"Σ D² = {fmt(D2.sum(), 2)}, so P({names[target]}) = {fmt(D2[target], 2)}/{fmt(D2.sum(), 2)} = "
           f"<b>{fmt(p, 3)}</b>.",
           "Common mistakes: using D instead of D² (that is not k-means++), or using the distance to the "
           "<i>farthest</i>/first centre instead of the nearest chosen centre."]
    return Q(text=f"k-means++ initialization (squared Euclidean seeding) is applied to the six points below. "
                  f"{chs} {'has' if variant == 0 else 'have'} already been chosen as centre{'s' if variant else ''}. "
                  f"The probability that {names[target]} is selected as the {which} centre is ______ " + nat_hint(3),
             qtype="NAT", marks=2, answer=nat_range(p, 3, 0.002), nat_hint=nat_hint(3),
             blocks=[_points_table(names, X), Figure(draw, 8, 5.5)], solution=sol)


@template(TOPIC, SUB_KM, marks=1, qtype="MCQ")
def kmeans_elbow(rng):
    ks = int(rng.integers(2, 6))
    K = 9
    sse = [0.0] * (K + 1)
    sse[1] = float(rng.integers(800, 1500))
    for k in range(2, K + 1):
        f = rng.uniform(0.35, 0.55) if k <= ks else rng.uniform(0.86, 0.94)
        sse[k] = sse[k - 1] * f
    vals = sse[1:]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(range(1, K + 1), vals, "-o", color="black", ms=4)
        ax.set_xlabel("number of clusters k")
        ax.set_ylabel("within-cluster SSE")
        ax.set_xticks(range(1, K + 1))
        ax.grid(alpha=0.3)

    dis = [str(ks + 1), str(ks - 1) if ks > 2 else str(ks + 2), str(K)]
    opts, a = mcq(rng, str(ks), dis)
    return Q(text="k-means is run for k = 1, 2, …, 9 on a dataset and the final within-cluster SSE is plotted below. "
                  "Using the elbow method, the most appropriate number of clusters is",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 8, 5)],
             solution=[f"The SSE drops steeply up to k = {ks} and then decreases only slowly (relative drops: "
                       + ", ".join(f"k={k}: {fmt(100 * (1 - sse[k] / sse[k - 1]), 0)}%" for k in range(2, K + 1))
                       + f"). The bend ('elbow') is at <b>k = {ks}</b>.",
                       f"k = {K} gives the lowest SSE but SSE always (weakly) decreases with k, so minimizing it would "
                       f"pick the largest k; it is not a model-selection criterion by itself."])


def _stirling2(n, k):
    S = [[0] * (k + 1) for _ in range(n + 1)]
    S[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            S[i][j] = j * S[i - 1][j] + S[i - 1][j - 1]
    return S[n][k]


@template(TOPIC, SUB_KM, marks=1, qtype="NAT")
def kmeans_partitions(rng):
    variant = int(rng.integers(0, 3))
    if variant == 0:
        n, k = [(4, 2), (5, 2), (5, 3), (6, 2), (6, 3), (7, 2), (7, 3), (6, 4), (8, 2)][int(rng.integers(0, 9))]
        val = _stirling2(n, k)
        text = (f"k-means with k = {k} searches over partitions of the data into k non-empty, unlabeled clusters. "
                f"The number of distinct such partitions of n = {n} points is ______")
        sol = [f"This is the Stirling number of the second kind S(n,k), with S(n,k) = k·S(n−1,k) + S(n−1,k−1).",
               f"S({n},{k}) = <b>{val}</b>." + (f" (For k = 2 it equals 2<super>n−1</super> − 1 = "
                                                f"{2 ** (n - 1) - 1}.)" if k == 2 else "")]
    elif variant == 1:
        n = int(rng.integers(4, 8))
        val = 2 ** (n - 1) - 1
        text = (f"A divisive (top-down) hierarchical algorithm considers <b>every</b> way of splitting a cluster of "
                f"{n} points into two non-empty sub-clusters. The number of candidate splits is ______")
        sol = [f"Each split is an unordered pair of non-empty complementary subsets: (2<super>{n}</super> − 2)/2 = "
               f"2<super>{n - 1}</super> − 1 = <b>{val}</b>.",
               "This exponential count is why divisive methods use heuristics (e.g. bisecting k-means)."]
    else:
        n, k = [(4, 3), (5, 3), (5, 4), (6, 3), (4, 4), (6, 5)][int(rng.integers(0, 6))]
        val = sum(_stirling2(n, j) for j in range(1, k + 1))
        text = (f"The number of ways to partition {n} distinct points into <b>at most</b> {k} non-empty "
                f"(unlabeled) clusters is ______")
        sol = ["Sum Stirling numbers of the second kind: " + " + ".join(
            f"S({n},{j}) = {_stirling2(n, j)}" for j in range(1, k + 1)) + f" → total <b>{val}</b>."]
    return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(val, val), nat_hint=nat_hint(0),
             solution=sol)


def _rings(rng, n=70):
    t1 = rng.uniform(0, 2 * np.pi, n // 2)
    t2 = rng.uniform(0, 2 * np.pi, n)
    a = np.c_[np.cos(t1), np.sin(t1)] * (1 + rng.normal(0, 0.05, (n // 2, 1)))
    b = np.c_[np.cos(t2), np.sin(t2)] * (3 + rng.normal(0, 0.08, (n, 1)))
    return a, b


def _moons(rng, n=60):
    t = rng.uniform(0, np.pi, n)
    a = np.c_[np.cos(t), np.sin(t)] + rng.normal(0, 0.05, (n, 2))
    t = rng.uniform(0, np.pi, n)
    b = np.c_[1 - np.cos(t), 0.45 - np.sin(t)] + rng.normal(0, 0.05, (n, 2))
    return a, b


@template(TOPIC, SUB_KM, marks=1, qtype="MCQ")
def kmeans_nonconvex(rng):
    shape = int(rng.integers(0, 2))
    a, b = _rings(rng) if shape == 0 else _moons(rng)
    sname = "two concentric rings" if shape == 0 else "two interleaving half-moons"

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(a[:, 0], a[:, 1], s=8, color="#222222")
        ax.scatter(b[:, 0], b[:, 1], s=8, color="#222222")
        ax.set_aspect("equal")
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.grid(alpha=0.25)

    variant = int(rng.integers(0, 2))
    if variant == 0:
        text = (f"The unlabeled data below visibly consists of {sname} (well separated, dense). Which method is "
                f"most likely to recover these two groups exactly?")
        correct = "Single-linkage agglomerative clustering, cut into 2 clusters"
        dis = ["k-means with k = 2 (best of many restarts)", "k-medoids (PAM) with k = 2",
               "Complete-linkage agglomerative clustering, cut into 2 clusters"]
        sol = [f"Each group is connected by chains of small gaps, while the gap between groups is larger. Single "
               f"linkage merges via nearest neighbours (MST edges) and therefore follows these chains: cutting the "
               f"largest MST edge separates the {sname}.",
               "k-means and k-medoids produce convex (Voronoi) clusters around representatives, so they split the "
               "shapes by a straight boundary. Complete linkage favours compact, small-diameter clusters and also "
               "cuts across the non-convex shapes."]
    else:
        text = (f"k-means with k = 2 fails to separate the {sname} shown below, even with many random restarts. "
                f"The main reason is that k-means")
        correct = "produces convex clusters separated by linear (Voronoi) boundaries"
        dis = ["converges only when the data are standardized",
               "cannot be applied to two-dimensional data",
               "requires class labels to place the centroids"]
        sol = ["Points are assigned to the nearest centroid, so each k-means cluster is a convex Voronoi cell and "
               "two clusters are separated by the perpendicular bisector of their centroids. Non-convex shapes "
               "such as rings or moons cannot be separated by such a boundary.",
               "k-means converges on raw data, works in any dimension, and is unsupervised (no labels)."]
    opts, ans = mcq(rng, correct, dis)
    return Q(text=text, qtype="MCQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 7, 5.5)],
             solution=sol)


@template(TOPIC, SUB_KM, marks=1, qtype="NAT")
def kmeans_complexity(rng):
    n = int(rng.choice([200, 500, 1000, 1500, 2000]))
    k = int(rng.integers(3, 9))
    d = int(rng.integers(2, 11))
    T = int(rng.integers(5, 21))
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val = n * k * T
        text = (f"Lloyd's k-means is run on n = {n} points in d = {d} dimensions with k = {k} for T = {T} "
                f"iterations. The total number of point-to-centroid distance computations in the assignment steps is ______")
        sol = [f"Each assignment step computes the distance of each of the n points to each of the k centroids: "
               f"n·k = {n * k} per iteration. Over T = {T} iterations: {n}·{k}·{T} = <b>{val}</b>. "
               f"(Each distance costs O(d), giving O(nkdT) overall; d does not affect the count of distances.)"]
        dd = 0
    elif variant == 1:
        val = n * k * d * T
        text = (f"Lloyd's k-means is run on n = {n} points in d = {d} dimensions with k = {k} for T = {T} "
                f"iterations. Counting one subtraction per coordinate per point–centroid pair in the assignment "
                f"step, the total number of such subtractions is ______")
        sol = [f"Assignment cost per iteration = n·k·d = {n}·{k}·{d} = {n * k * d}; over T iterations "
               f"<b>{val}</b>. This is the O(nkdT) complexity of k-means."]
        dd = 0
    else:
        n = int(rng.integers(20, 101))
        val = k * (n - k)
        text = (f"In one iteration of PAM (k-medoids) on n = {n} points with k = {k}, every (medoid, non-medoid) "
                f"pair is considered as a candidate swap. The number of candidate swaps is ______")
        sol = [f"There are k medoids and n − k non-medoids, so k(n − k) = {k}·{n - k} = <b>{val}</b> swaps "
               f"(each evaluated in O(n − k), giving O(k(n−k)²) per iteration, far costlier than k-means' O(nkd))."]
        dd = 0
    return Q(text=text + " " + nat_hint(dd), qtype="NAT", marks=1,
             answer=nat_range(val, dd, 10 ** (-dd) / 2) if dd else (val, val), nat_hint=nat_hint(dd), solution=sol)


KM_T = [
    ("Each iteration of Lloyd's k-means algorithm cannot increase the within-cluster sum of squares.",
     "Both the assignment step and the mean-update step minimize the objective with the other block fixed."),
    ("k-means converges in a finite number of iterations.",
     "There are finitely many partitions and the objective never increases, so no partition repeats."),
    ("The solution found by k-means can depend on the choice of initial centroids.",
     "Lloyd's algorithm converges to a local optimum determined by the initialization."),
    ("Running k-means from several random initializations and keeping the run with lowest SSE is a common remedy "
     "for poor local optima.", "Multiple restarts reduce the chance of a bad local minimum."),
    ("In the update step, a cluster's new centroid is the arithmetic mean of the points assigned to it.",
     "The mean minimizes the sum of squared Euclidean distances to the points."),
    ("k-means is sensitive to outliers.",
     "Centroids are means, and squared distances give far-away points a large influence."),
    ("The assignment step partitions the feature space into the Voronoi cells of the centroids.",
     "Each point goes to its nearest centroid."),
    ("With Euclidean distance, the boundary between two k-means clusters is the perpendicular bisector "
     "(hyperplane) of their centroids.", "Points equidistant from two centroids form that hyperplane."),
    ("k-means++ picks each new initial centre with probability proportional to D(x)², the squared distance to "
     "the nearest centre already chosen.", "This is the definition of k-means++ seeding."),
    ("The minimum achievable within-cluster SSE is a non-increasing function of k.",
     "Splitting a cluster can never increase the optimal SSE."),
    ("If k equals the number of (distinct) data points, the optimal within-cluster SSE is 0.",
     "Every point can be its own centroid."),
    ("Rescaling one feature (e.g. changing its units) can change the clusters found by k-means.",
     "Euclidean distances change non-uniformly, so assignments can change."),
    ("One iteration of Lloyd's algorithm costs O(nkd) time.", "n·k distances, each O(d)."),
    ("k-means works best when clusters are roughly spherical and of similar size.",
     "Its objective implicitly assumes isotropic, equal-variance clusters."),
    ("k-means requires the number of clusters k to be specified in advance.",
     "k is an input hyper-parameter."),
    ("The elbow method plots the within-cluster SSE against k and picks the k where the decrease levels off.",
     "That bend is the 'elbow'."),
    ("Finding the globally optimal k-means partition is NP-hard in general.",
     "Hence the use of the Lloyd heuristic."),
    ("k-means is an unsupervised method: it uses no class labels.", "Only the feature vectors are used."),
    ("Each k-means cluster region (Voronoi cell) is convex.",
     "A Voronoi cell is an intersection of half-spaces."),
    ("In standard (hard) k-means every point belongs to exactly one cluster.",
     "Assignments are one-hot; soft assignments arise in GMM/EM."),
]
KM_F = [
    ("k-means is guaranteed to find the partition with the globally minimum SSE.",
     "It only reaches a local optimum."),
    ("The within-cluster SSE can increase from one Lloyd iteration to the next.",
     "Each step minimizes the SSE over one block of variables, so it is non-increasing."),
    ("The final k-means clustering does not depend on the initial centroids.",
     "Different initializations can converge to different local optima."),
    ("k-means with k = 2 can directly separate two concentric rings.",
     "k-means clusters are convex Voronoi cells; rings are non-convex."),
    ("The k-means centroid of a cluster must be one of the data points.",
     "That is true for k-medoids; the k-means centroid is the mean."),
    ("k-means is robust to outliers because each cluster is summarized by its median.",
     "k-means uses the mean, which is sensitive to outliers."),
    ("The optimal within-cluster SSE increases as k increases.",
     "It is non-increasing in k."),
    ("k-means determines the number of clusters automatically.", "k must be supplied by the user."),
    ("k-means requires labelled training data.", "It is unsupervised."),
    ("k-means results are invariant to rescaling individual features.",
     "Rescaling changes Euclidean distances and hence assignments."),
    ("k-means++ chooses all k initial centres uniformly at random from the data.",
     "Only the first centre is uniform; later ones are drawn ∝ D(x)²."),
    ("One iteration of Lloyd's k-means costs O(n²d).",
     "It costs O(nkd); O(n²) pairwise distances are not needed."),
    ("Choosing the k that minimizes the training SSE is a sound way to select k.",
     "SSE keeps decreasing with k (to 0 at k = n)."),
    ("k-means produces a hierarchy of nested clusterings.", "That is hierarchical clustering."),
    ("k-means assigns each point to the centroid with the largest cosine similarity.",
     "Standard k-means uses Euclidean distance."),
    ("k-means is a soft clustering method that gives each point a membership probability for each cluster.",
     "That describes Gaussian mixture models fitted with EM."),
    ("k-means is well suited to clusters of very different sizes and densities.",
     "It tends to split large clusters and merge small ones."),
    ("The boundary between two k-means clusters (Euclidean) is in general a curved quadratic surface.",
     "It is a hyperplane (perpendicular bisector)."),
]


@template(TOPIC, SUB_KM, marks=1, qtype="MSQ")
def kmeans_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, KM_T, KM_F)
    return Q(text="Which of the following statements about k-means clustering is/are CORRECT?", qtype="MSQ",
             marks=1, options=opts, answer=ans, solution=expl)


KM2_T = [
    ("If the centroids do not change between two successive iterations, the assignments will not change in any "
     "later iteration either.", "Same centroids give the same assignments; the algorithm is at a fixed point."),
    ("k-means (Lloyd) is block-coordinate descent on J = Σ‖x<sub>i</sub> − μ<sub>c(i)</sub>‖²: assignments are "
     "optimal for fixed centroids and means are optimal for fixed assignments.",
     "That is exactly why J is non-increasing."),
    ("Within a cluster C, Σ<sub>x∈C</sub>‖x − μ‖² = (1/(2|C|)) Σ<sub>x∈C</sub>Σ<sub>y∈C</sub>‖x − y‖².",
     "A standard identity; the SSE can be written via pairwise distances."),
    ("k-medoids (PAM) can be run using only a pairwise dissimilarity matrix, without coordinates.",
     "Medoids are data points; no means are needed."),
    ("The medoid of a cluster is the member that minimizes the sum of dissimilarities to the other members.",
     "This is the definition."),
    ("k-medoids is generally more robust to outliers than k-means.",
     "A medoid is an actual point and uses unsquared dissimilarities, so an outlier pulls it far less."),
    ("For mean centroids, total sum of squares = within-cluster SS + between-cluster SS.",
     "The standard ANOVA decomposition; reducing WSS increases BSS."),
    ("Multiplying all coordinates by 2 multiplies the optimal k-means SSE by 4 and leaves the optimal partition "
     "unchanged.", "Uniform scaling multiplies every squared distance by 4."),
    ("k-means is a limiting case of EM for a Gaussian mixture with equal spherical covariances σ²I as σ → 0.",
     "The responsibilities become hard 0/1 assignments."),
    ("During Lloyd's iterations a cluster can become empty; implementations handle it, e.g. by re-seeding.",
     "Nothing in the algorithm prevents a centroid from losing all its points."),
    ("The number of distinct partitions of n points into k non-empty clusters is the Stirling number of the "
     "second kind S(n, k).", "Hence exhaustive search is infeasible."),
    ("For 1-D data and a single cluster, the k-medoids representative under absolute distance is a median "
     "data point.", "The median minimizes the sum of absolute deviations."),
]
KM2_F = [
    ("k-medoids requires the data to lie in a Euclidean space so that means can be computed.",
     "k-medoids never computes means; any dissimilarity works."),
    ("For a 1-D cluster with an odd number of points, the medoid under absolute distance is the mean.",
     "It is the median, which is a data point."),
    ("One PAM iteration is cheaper than one Lloyd iteration for large n.",
     "PAM costs O(k(n−k)²) per iteration versus O(nkd)."),
    ("Multiplying one feature by 10 never changes the k-means partition.",
     "Non-uniform scaling changes distances and can change the partition."),
    ("For mean centroids, total sum of squares = within-cluster SS − between-cluster SS.",
     "The decomposition is TSS = WSS + BSS."),
    ("k-means++ initialization guarantees the globally optimal clustering.",
     "It only gives an O(log k) approximation in expectation."),
    ("Lloyd's algorithm can cycle forever between two partitions with different SSE values.",
     "J strictly decreases whenever the partition changes, so it cannot return to a worse partition."),
    ("As k-means lowers the within-cluster SS, the between-cluster SS also decreases.",
     "TSS is fixed, so BSS increases."),
    ("k-medoids minimizes the sum of squared Euclidean distances to the cluster means.",
     "It minimizes the sum of dissimilarities to medoids (data points)."),
    ("The number of ways to split n points into 2 non-empty clusters is n(n−1)/2.",
     "It is 2<super>n−1</super> − 1."),
    ("Running k-means with Manhattan-distance assignments and mean updates minimizes the total L1 distance.",
     "The L1-optimal centre is the coordinate-wise median (k-medians), not the mean."),
    ("Increasing k by one changes the cluster membership of every point.",
     "Typically only some points move."),
]


@template(TOPIC, SUB_KM, marks=2, qtype="MSQ")
def kmeans_kmedoids_concepts2(rng):
    opts, ans, expl = msq_from_statements(rng, KM2_T, KM2_F)
    return Q(text="Consider k-means (Lloyd's algorithm) and k-medoids (PAM). Which of the following statements "
                  "is/are CORRECT?", qtype="MSQ", marks=2, options=opts, answer=ans, solution=expl)


# ============================================================================
# k-MEDOIDS
# ============================================================================
@template(TOPIC, SUB_KMED, marks=1, qtype="NAT")
def medoid_outlier(rng):
    while True:
        n = int(rng.choice([5, 7]))
        base = _distinct_ints(rng, 2, 16, n - 1)
        out = float(rng.integers(40, 90))
        x = np.sort(np.r_[base, out])
        mean = x.mean()
        med = float(np.median(x))
        if abs(mean - round(mean, 2)) < 1e-9:
            break
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val, ask = med, "the medoid of this cluster (absolute-difference dissimilarity) is ______"
    elif variant == 1:
        val, ask = abs(mean - med), ("the absolute difference between the k-means centroid (mean) and the k-medoids "
                                     "representative (absolute-difference dissimilarity) is ______")
    else:
        costs = [np.abs(x - c).sum() for c in x]
        val, ask = min(costs), ("the total cost Σ|x<sub>i</sub> − m| of the cluster about its medoid m is ______")

    def draw(fig):
        ax = fig.add_subplot(111)
        _strip(ax, x)

    costs = [np.abs(x - c).sum() for c in x]
    sol = [f"Mean = {fmt(x.sum())}/{n} = {fmt(mean, 2)} (pulled towards the outlier {fmt(out)}).",
           "Medoid = data point minimizing Σ|x<sub>i</sub> − m|. Costs: "
           + ", ".join(f"m={fmt(c)}: {fmt(v)}" for c, v in zip(x, costs)) + ".",
           f"The minimum is at m = {fmt(med)} (the median), cost {fmt(min(costs))}.",
           f"Answer: <b>{fmt(val, 2)}</b>. The medoid is barely affected by the outlier, unlike the mean."]
    return Q(text=f"A cluster contains the 1-D values {{{', '.join(fmt(v) for v in x)}}}. Treating them as one cluster, "
                  + ask + " " + nat_hint(2),
             qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2), blocks=[Figure(draw, 9, 2.6)],
             solution=sol)


@template(TOPIC, SUB_KMED, marks=2, qtype="NAT")
def medoid_cost(rng):
    while True:
        n = int(rng.integers(5, 7))
        X = _manhattan_points(rng, n, 0, 9)
        metric = "manhattan" if rng.random() < 0.6 else "euclidean"
        costs = np.array([sum(_dist(X[i], X[j], metric) for j in range(n)) for i in range(n)])
        o = np.sort(costs)
        if o[1] - o[0] < 0.05:
            continue
        m = int(np.argmin(costs))
        others = [i for i in range(n) if i != m]
        j = int(rng.choice(others))
        variant = int(rng.integers(0, 2))
        break
    names = _names(n)
    mname = "Manhattan (L<sub>1</sub>)" if metric == "manhattan" else "Euclidean (L<sub>2</sub>)"
    d = 0 if (metric == "manhattan") else 2
    if variant == 0:
        val = costs[m]
        ask = ("The medoid is the point that minimizes the sum of distances to all points of the cluster. The minimum "
               "total distance (cost of the medoid) is ______")
    else:
        val = costs[j] - costs[m]
        ask = (f"If {names[j]} were used as the cluster representative instead of the medoid, the total distance "
               f"(cost) would increase by ______")

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, X, names)
        _int_grid(ax, X)

    D = _pairwise(X, metric)
    rows = [[""] + names + ["Σ"]]
    for i in range(n):
        rows.append([names[i]] + [fmt(D[i][jj], 2) for jj in range(n)] + [fmt(costs[i], 2)])
    sol = [f"Compute the {mname} distance matrix and its row sums:", Table(rows, header=True),
           f"The smallest row sum is {fmt(costs[m], 2)} for {names[m]}, so the medoid is {names[m]}."]
    if variant == 1:
        sol.append(f"Cost with {names[j]}: {fmt(costs[j], 2)}; increase = {fmt(costs[j], 2)} − {fmt(costs[m], 2)} = "
                   f"<b>{fmt(val, 2)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(val, 2)}</b>.")
    sol.append("Unlike a k-means centroid, the medoid is always an actual data point.")
    return Q(text=f"A cluster contains the {n} points below. Distances are {mname}. " + ask + " " + nat_hint(d),
             qtype="NAT", marks=2, answer=nat_range(val, d) if d else (val, val), nat_hint=nat_hint(d),
             blocks=[_points_table(names, X), Figure(draw, 7.5, 5.2)], solution=sol)


@template(TOPIC, SUB_KMED, marks=2, qtype="NAT")
def pam_swap(rng):
    while True:
        n = int(rng.integers(7, 9))
        x = _distinct_ints(rng, 0, 30, n)
        mi = sorted(rng.choice(n, 2, replace=False).tolist())
        non = [i for i in range(n) if i not in mi]
        o = int(rng.choice(non))
        mo = int(rng.choice(mi))
        new = [i for i in mi if i != mo] + [o]

        def cost(meds):
            return sum(min(abs(x[i] - x[m]) for m in meds) for i in range(n))

        c_old, c_new = cost(mi), cost(new)
        if c_old != c_new:
            break
    names = _names(n, "x")
    variant = int(rng.integers(0, 2))
    delta = c_new - c_old
    if variant == 0:
        val = delta
        ask = (f"The change in total cost, (cost after swap) − (cost before swap), when medoid {fmt(x[mo])} is "
               f"swapped with non-medoid {fmt(x[o])} is ______")
    else:
        val = c_old
        ask = "The total cost Σ<sub>i</sub> min<sub>m</sub>|x<sub>i</sub> − m| of the current configuration is ______"

    def draw(fig):
        ax = fig.add_subplot(111)
        _strip(ax, x, None, [x[i] for i in mi], "current medoid")

    def detail(meds):
        return ", ".join(f"{fmt(x[i])}→{fmt(min(abs(x[i] - x[m]) for m in meds))}" for i in range(n))

    sol = ["PAM cost = Σ over all points of the absolute distance to the nearest medoid.",
           f"Current medoids {{{fmt(x[mi[0]])}, {fmt(x[mi[1]])}}}: distances {detail(mi)}; cost = <b>{fmt(c_old)}</b>."]
    if variant == 0:
        sol += [f"After swap, medoids {{{', '.join(fmt(x[i]) for i in sorted(new))}}}: distances {detail(new)}; "
                f"cost = {fmt(c_new)}.",
                f"Change = {fmt(c_new)} − {fmt(c_old)} = <b>{fmt(delta)}</b> "
                + ("(negative → PAM accepts the swap)." if delta < 0 else "(positive → PAM rejects the swap).")]
    return Q(text=f"PAM (k-medoids, k = 2, absolute-difference dissimilarity) is applied to the 1-D data "
                  f"{{{', '.join(fmt(v) for v in x)}}}. The current medoids are {fmt(x[mi[0]])} and {fmt(x[mi[1]])}. "
                  + ask + " " + nat_hint(0),
             qtype="NAT", marks=2, answer=(val, val), nat_hint=nat_hint(0), blocks=[Figure(draw, 9.5, 2.8)],
             solution=sol)


# ============================================================================
# HIERARCHICAL CLUSTERING
# ============================================================================
def _hc_solution_head(D, names, method, merges, d=2):
    sol = [f"Use {LINK_DEF[method]}. After each merge, recompute the distance of the new cluster to the others "
           f"with this rule and merge the closest pair again."]
    n = len(names)
    clusters = [frozenset([i]) for i in range(n)]

    def cname(C):
        return "{" + ", ".join(names[i] for i in sorted(C)) + "}"

    for st, (A, B, h) in enumerate(merges, 1):
        clusters = [c for c in clusters if c != A and c != B]
        N = A | B
        line = f"Merge {st}: {cname(A)} + {cname(B)} at height <b>{fmt(h, d)}</b>."
        if clusters:
            line += " Updated: " + ", ".join(f"d({cname(N)}, {cname(c)}) = {fmt(_link(D, N, c, method), d)}"
                                             for c in clusters) + "."
        clusters.append(N)
        sol.append(line)
    return sol


def _dendro_fig(merges, names):
    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_dendro(ax, merges, names)
    return Figure(draw, 8, 4.6)


@template(TOPIC, SUB_HC, marks=2, qtype="NAT")
def hc_merge_height(rng):
    method = str(rng.choice(["single", "complete", "average"]))
    n = int(rng.choice([5, 6]))
    P, D, merges = _hc_instance(rng, n, method)
    names = _names(n)
    m = int(rng.integers(2, n))  # merge number 2..n-1
    val = merges[m - 1][2]
    ordn = {2: "second", 3: "third", 4: "fourth", 5: "fifth"}[m]
    sol = _hc_solution_head(D, names, method, merges)
    sol.append(f"The {ordn} merge occurs at height <b>{fmt(val, 2)}</b>.")
    sol.append("Dendrogram:")
    sol.append(_dendro_fig(merges, names))
    return Q(text=f"Agglomerative hierarchical clustering with <b>{method} linkage</b> is applied to {n} points whose "
                  f"pairwise distance matrix is given below (upper triangle shown). The height (linkage distance) at "
                  f"which the <b>{ordn}</b> merge takes place is ______ " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[_dist_table(D, names)], solution=sol)


@template(TOPIC, SUB_HC, marks=2, qtype="NAT")
def hc_cophenetic(rng):
    while True:
        method = str(rng.choice(["single", "complete", "average"]))
        n = int(rng.choice([5, 6]))
        P, D, merges = _hc_instance(rng, n, method)
        pairs = [(i, j) for i, j in combinations(range(n), 2) if abs(_coph(merges, i, j) - D[i][j]) > 0.5]
        if pairs:
            break
    i, j = pairs[int(rng.integers(0, len(pairs)))]
    names = _names(n)
    val = _coph(merges, i, j)
    sol = _hc_solution_head(D, names, method, merges)
    sol.append(f"{names[i]} and {names[j]} first lie in the same cluster at the merge of height {fmt(val, 2)}, so "
               f"their cophenetic distance is <b>{fmt(val, 2)}</b> (their original distance was {fmt(D[i][j], 2)}).")
    sol.append(_dendro_fig(merges, names))
    return Q(text=f"Agglomerative clustering with <b>{method} linkage</b> is applied to the distance matrix below. The "
                  f"cophenetic distance between {names[i]} and {names[j]} (the dendrogram height at which they are "
                  f"first joined) is ______ " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[_dist_table(D, names)], solution=sol)


@template(TOPIC, SUB_HC, marks=2, qtype="MCQ")
def hc_cut_clusters(rng):
    for _ in range(500):
        method = str(rng.choice(["single", "complete", "average"]))
        n = 6
        k = int(rng.choice([2, 3]))
        P, D, merges = _hc_instance(rng, n, method)
        correct = _clusters_k(merges, n, k)
        others = []
        for om in ["single", "complete", "average"]:
            if om == method:
                continue
            mm = _hclust(D, om)
            if mm is not None:
                others.append((om, _clusters_k(mm, n, k)))
        diff = [(om, c) for om, c in others if set(c) != set(correct)]
        if diff:
            break
    names = _names(n)
    cs = _part_str(correct, names)
    dis = []
    dis_note = []
    for om, c in diff:
        s = _part_str(c, names)
        if s != cs and s not in dis:
            dis.append(s)
            dis_note.append(f"{s} is what <i>{om}</i> linkage would give.")
    # also the clustering at k±1 merged/split, and random partitions
    for kk in (k - 1, k + 1):
        if 2 <= kk <= n - 1:
            s = _part_str(_clusters_k(merges, n, kk), names)
            if s not in dis and s != cs:
                dis.append(s)
                dis_note.append(f"{s} has {kk} clusters (cut at the wrong level).")
    while len(dis) < 3:
        lab = rng.integers(0, k, n)
        if len(set(lab.tolist())) < k:
            continue
        c = [frozenset(int(i) for i in np.where(lab == g)[0]) for g in range(k)]
        s = _part_str(c, names)
        if s not in dis and s != cs:
            dis.append(s)
            dis_note.append("")
    dis, dis_note = dis[:3], dis_note[:3]
    opts, a = mcq(rng, cs, dis)
    sol = _hc_solution_head(D, names, method, merges)
    sol.append(f"Stopping when {k} clusters remain (i.e. after {n - k} merges): <b>{cs}</b>.")
    sol += [x for x in dis_note if x]
    sol.append(_dendro_fig(merges, names))
    return Q(text=f"Six points have the pairwise distances below. Agglomerative clustering with "
                  f"<b>{method} linkage</b> is run and the dendrogram is cut to give exactly <b>{k}</b> clusters. "
                  f"The resulting clusters are",
             qtype="MCQ", marks=2, options=opts, answer=a, blocks=[_dist_table(D, names)], solution=sol)


@template(TOPIC, SUB_HC, marks=1, qtype="NAT")
def hc_dendrogram_read(rng):
    while True:
        n = int(rng.integers(6, 9))
        P, D, merges = _hc_instance(rng, n, "average", "euclidean")
        hs = [h for _, _, h in merges]
        top = hs[-1]
        gaps = [(hs[i + 1] - hs[i], i) for i in range(n - 2)]
        good = [i for g, i in gaps if g > 0.12 * top]
        if good:
            break
    names = [chr(ord("A") + i) for i in range(n)]
    variant = int(rng.integers(0, 2))
    if variant == 0:
        i = int(rng.choice(good))
        h = round((hs[i] + hs[i + 1]) / 2, 1)
        val = n - (i + 1)
        text = (f"The dendrogram below was obtained by agglomerative clustering of {n} points A–{names[-1]}. If the "
                f"dendrogram is cut by a horizontal line at height {fmt(h, 1)}, the number of clusters obtained is ______")
        sol = [f"Merges below the cut height {fmt(h, 1)}: {i + 1} (heights "
               + ", ".join(fmt(x, 2) for x in hs[: i + 1]) + ").",
               f"Each merge reduces the number of clusters by one: {n} − {i + 1} = <b>{val}</b>. Equivalently, count "
               f"the vertical lines crossed by the horizontal cut."]
    else:
        k = int(rng.integers(2, min(4, n - 1) + 1))
        cl = _clusters_k(merges, n, k)
        leaf = int(rng.integers(0, n))
        c = [c for c in cl if leaf in c][0]
        val = len(c)
        text = (f"The dendrogram below was obtained by agglomerative clustering of {n} points A–{names[-1]}. If it is "
                f"cut to obtain exactly {k} clusters, the number of points in the cluster that contains point "
                f"{names[leaf]} is ______")
        sol = [f"Undo the top {k - 1} merge(s) (equivalently cut just below height {fmt(hs[n - k], 2)}). Clusters: "
               f"{_part_str(cl, names)}.",
               f"{names[leaf]} lies in a cluster of size <b>{val}</b>."]

    def draw(fig):
        ax = fig.add_subplot(111)
        _draw_dendro(ax, merges, names)
        step = next(st for st in (0.25, 0.5, 1, 2, 5) if top / st <= 12)
        ax.set_yticks(np.arange(0, top * 1.08, step))
        ax.set_ylim(0, top * 1.08)

    return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(val, val), nat_hint=nat_hint(0),
             blocks=[Figure(draw, 8.5, 5)], solution=sol)


def _mst(D):
    n = len(D)
    inT = [0]
    edges = []
    while len(inT) < n:
        best = min(((D[i][j], i, j) for i in inT for j in range(n) if j not in inT))
        edges.append(best)
        inT.append(best[2])
    return edges


@template(TOPIC, SUB_HC, marks=2, qtype="NAT")
def hc_single_mst(rng):
    n = 6
    metric = "manhattan" if rng.random() < 0.6 else "euclidean"
    P = _manhattan_points(rng, n, 0, 9)
    D = _pairwise(P, metric)
    edges = _mst(D)
    w = sorted(e[0] for e in edges)
    names = _names(n)
    d = 0 if metric == "manhattan" else 2
    variant = int(rng.integers(0, 3))
    if variant == 2:
        ok = [i for i in range(n - 2) if w[i + 1] - w[i] >= 0.5]
        if not ok:
            variant = 0
    if variant == 0:
        val = w[-1]
        ask = "the height at which the <b>last</b> merge (forming a single cluster) occurs is ______"
        fin = f"The last single-linkage merge happens at the largest MST edge: <b>{fmt(val, 2)}</b>."
    elif variant == 1:
        val = sum(w)
        ask = "the <b>sum of the heights</b> of all merges in the dendrogram is ______"
        fin = f"Sum of merge heights = total MST weight = {' + '.join(fmt(x, 2) for x in w)} = <b>{fmt(val, 2)}</b>."
    else:
        i = int(rng.choice(ok))
        h = round((w[i] + w[i + 1]) / 2, 2)
        val = n - (i + 1)
        d = 0
        ask = f"the number of clusters obtained by cutting the dendrogram at height {fmt(h, 2)} is ______"
        fin = (f"MST edges shorter than {fmt(h, 2)}: {i + 1}; clusters = n − (number of such edges) = {n} − {i + 1} = "
               f"<b>{val}</b>.")
    mname = "Manhattan" if metric == "manhattan" else "Euclidean"

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, P, names)
        _int_grid(ax, P)

    sol = ["Single-linkage merge heights are exactly the edge weights of a minimum spanning tree (Kruskal's "
           "algorithm adds the shortest edge joining two different components = single-linkage merge).",
           "MST edges (Prim's algorithm): " + "; ".join(f"{names[i]}–{names[j]} ({fmt(wt, 2)})" for wt, i, j in edges)
           + ".", f"Sorted merge heights: {', '.join(fmt(x, 2) for x in w)}.", fin]
    return Q(text=f"Single-linkage agglomerative clustering with {mname} distance is applied to the six points below. "
                  f"Then " + ask + " " + nat_hint(d),
             qtype="NAT", marks=2, answer=nat_range(val, d) if d else (val, val), nat_hint=nat_hint(d),
             blocks=[_points_table(names, P), Figure(draw, 7.5, 5.2)], solution=sol)


@template(TOPIC, SUB_HC, marks=1, qtype="NAT")
def hc_counts(rng):
    n = int(rng.integers(8, 61))
    variant = int(rng.integers(0, 4))
    if variant == 0:
        val = n - 1
        text = f"Agglomerative hierarchical clustering of n = {n} points (until one cluster remains) performs how many merges? "
        sol = f"Each merge reduces the number of clusters by one: from {n} to 1 needs n − 1 = <b>{val}</b> merges."
    elif variant == 1:
        k = int(rng.integers(2, 8))
        val = n - k
        text = (f"Agglomerative clustering of {n} points is stopped when {k} clusters remain. The number of merges "
                f"performed is ______")
        sol = f"{n} − {k} = <b>{val}</b> merges."
    elif variant == 2:
        val = n * (n - 1) // 2
        text = (f"The number of distinct pairwise dissimilarities that must be stored in the (symmetric, zero-diagonal) "
                f"distance matrix for agglomerative clustering of {n} points is ______")
        sol = f"n(n−1)/2 = {n}·{n - 1}/2 = <b>{val}</b>."
    else:
        val = 2 * n - 1
        text = f"A complete (binary) dendrogram over n = {n} points has how many nodes in total (leaves plus internal nodes)? "
        sol = f"n leaves + (n − 1) internal (merge) nodes = 2n − 1 = <b>{val}</b>."
    return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(val, val), nat_hint=nat_hint(0),
             solution=sol)


HC_T = [
    ("Agglomerative clustering starts with each point as its own cluster and repeatedly merges the two closest "
     "clusters.", "Bottom-up procedure."),
    ("Divisive clustering starts with all points in one cluster and recursively splits clusters.",
     "Top-down procedure."),
    ("Agglomerative clustering of n points performs exactly n − 1 merges.", "Each merge removes one cluster."),
    ("Single linkage measures cluster distance by the minimum pairwise distance between their members.",
     "Definition of single (nearest-neighbour) linkage."),
    ("Complete linkage measures cluster distance by the maximum pairwise distance between their members.",
     "Definition of complete (farthest-neighbour) linkage."),
    ("Average linkage uses the mean of all pairwise distances between members of the two clusters.",
     "Definition of UPGMA."),
    ("Single linkage is prone to the chaining effect, producing long, straggly clusters.",
     "One close pair suffices to merge two clusters."),
    ("Complete linkage tends to produce compact clusters with small diameters.",
     "It merges on the largest within-pair distance."),
    ("Single-linkage clustering is closely related to the minimum spanning tree of the data.",
     "Its merge heights are the MST edge weights."),
    ("Hierarchical clustering does not need the number of clusters in advance; it can be chosen afterwards by "
     "cutting the dendrogram.", "One run gives all levels."),
    ("Ward's method merges the pair of clusters giving the smallest increase in total within-cluster sum of "
     "squares.", "Definition of Ward's criterion."),
    ("The cophenetic distance between two points is the dendrogram height at which they are first joined.",
     "Definition."),
    ("Agglomerative clustering can be run from a pairwise dissimilarity matrix alone.",
     "Single/complete/average linkage only need pairwise dissimilarities."),
    ("For single, complete and average linkage, successive merge heights are non-decreasing.",
     "These linkages are monotone (no inversions)."),
    ("Storing the full distance matrix for agglomerative clustering needs O(n²) memory.",
     "There are n(n−1)/2 pairs."),
    ("Single linkage can recover well-separated non-convex clusters such as concentric rings.",
     "It follows chains of nearest neighbours."),
    ("For a fixed distance matrix without ties, agglomerative clustering is deterministic.",
     "No random initialization is involved."),
]
HC_F = [
    ("Agglomerative clustering of n points performs n merges.", "It performs n − 1 merges."),
    ("Single linkage uses the maximum pairwise distance between clusters.", "That is complete linkage."),
    ("Complete linkage is particularly prone to the chaining effect.", "Chaining is typical of single linkage."),
    ("Hierarchical clustering requires the number of clusters before it can be run.",
     "The dendrogram can be cut at any level afterwards."),
    ("Divisive clustering starts from singleton clusters and merges them.", "That is agglomerative clustering."),
    ("The agglomerative dendrogram depends on a random initialization.",
     "The procedure is deterministic (apart from tie-breaking)."),
    ("A merge made in agglomerative clustering can be undone in a later step.",
     "Merges are greedy and final."),
    ("Single and complete linkage always produce the same dendrogram.", "They generally differ."),
    ("Ward's method merges the two clusters whose centroids are farthest apart.",
     "It merges the pair that least increases the within-cluster SS."),
    ("Cutting a dendrogram at a greater height produces more clusters.", "Higher cuts give fewer clusters."),
    ("Average linkage defines the distance between clusters as the distance between their medoids.",
     "It averages all pairwise distances."),
    ("The cophenetic distance between two points always equals their original distance.",
     "It equals the merge height, which generally differs."),
    ("Centroid linkage always yields a monotone dendrogram (no inversions).",
     "Centroid (and median) linkage can produce inversions."),
    ("Naive agglomerative clustering runs in O(n) time.", "The naive algorithm is O(n³) (O(n² log n) with heaps)."),
]


@template(TOPIC, SUB_HC, marks=1, qtype="MSQ")
def hc_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, HC_T, HC_F)
    return Q(text="Which of the following statements about hierarchical clustering is/are CORRECT?", qtype="MSQ",
             marks=1, options=opts, answer=ans, solution=expl)


HC2_T = [
    ("The single-linkage merge heights are exactly the edge weights of a minimum spanning tree of the complete "
     "distance graph.", "Kruskal's algorithm performs the same merges in the same order."),
    ("Cutting the single-linkage dendrogram into k clusters is equivalent to deleting the k − 1 heaviest edges of "
     "an MST.", "The remaining forest's components are the clusters."),
    ("For any two points, the single-linkage cophenetic distance is ≤ their original distance.",
     "They are joined no later than when their own edge would merge them."),
    ("For any two points, the complete-linkage cophenetic distance is ≥ their original distance.",
     "The merge height is a maximum over cross pairs that includes this pair."),
    ("Cophenetic distances from single, complete or average linkage satisfy the ultrametric inequality "
     "d(x, z) ≤ max(d(x, y), d(y, z)).", "Monotone dendrograms define ultrametrics."),
    ("Replacing every dissimilarity by its square does not change the single-linkage merge order.",
     "Single (and complete) linkage depend only on the ranks of the distances."),
    ("Cutting a dendrogram (with distinct merge heights) at all possible heights gives exactly n different "
     "clusterings, with 1, 2, …, n clusters.", "One clustering per number of clusters."),
    ("Centroid linkage can produce inversions, i.e. a merge at a lower height than an earlier merge.",
     "Merging can bring a new centroid closer to another cluster."),
    ("Ward's merge cost for clusters A and B is (|A||B|/(|A|+|B|))·‖μ<sub>A</sub> − μ<sub>B</sub>‖².",
     "This is the increase in within-cluster SS when A and B merge."),
    ("The Lance–Williams formula updates inter-cluster distances after a merge without going back to the raw "
     "points.", "It covers single, complete, average, Ward and others."),
    ("Clusterings obtained by cutting one dendrogram at different heights are nested.",
     "A higher cut only merges lower-level clusters."),
]
HC2_F = [
    ("The single-linkage cophenetic distance between two points can exceed their original distance.",
     "It is always ≤ the original distance."),
    ("Complete-linkage merge heights equal the edge weights of a minimum spanning tree.",
     "That holds for single linkage."),
    ("Replacing every dissimilarity by its square never changes the average-linkage dendrogram topology.",
     "Average linkage depends on actual values, not only on ranks."),
    ("A dendrogram over n leaves has n internal nodes.", "It has n − 1 internal nodes."),
    ("Cutting a dendrogram at two different heights can give clusterings that are not nested.",
     "Hierarchical clusterings are nested by construction."),
    ("Single linkage is robust to a few noise points lying between two clusters.",
     "Such bridge points cause chaining and merge the clusters."),
    ("The naive agglomerative algorithm runs in O(n log n) time.", "It needs O(n³) (O(n² log n) with priority queues)."),
    ("Exhaustive divisive clustering of a cluster of m points needs to examine only O(m) binary splits.",
     "There are 2<super>m−1</super> − 1 splits."),
    ("Different linkages applied to the same distance matrix must yield the same 2-cluster partition.",
     "Single and complete linkage often disagree."),
    ("For any two points, the complete-linkage cophenetic distance is ≤ their original distance.",
     "It is ≥ the original distance."),
    ("Single linkage tends to produce compact, roughly spherical clusters of equal diameter.",
     "That describes complete linkage; single linkage chains."),
]


@template(TOPIC, SUB_HC, marks=2, qtype="MSQ")
def hc_concepts2(rng):
    opts, ans, expl = msq_from_statements(rng, HC2_T, HC2_F)
    return Q(text="Consider agglomerative hierarchical clustering on n points with a dissimilarity matrix (no ties). "
                  "Which of the following statements is/are CORRECT?", qtype="MSQ", marks=2, options=opts,
             answer=ans, solution=expl)


# ============================================================================
# DISTANCE MEASURES
# ============================================================================
@template(TOPIC, SUB_DIST, marks=1, qtype="NAT")
def dist_compute(rng):
    dim = int(rng.integers(3, 6))
    while True:
        x = rng.integers(-4, 8, dim).astype(float)
        y = rng.integers(-4, 8, dim).astype(float)
        if np.any(x != y) and np.linalg.norm(x) > 0 and np.linalg.norm(y) > 0:
            break
    variant = str(rng.choice(["euclid", "manhattan", "cheb", "mink3", "cos", "cosd"]))
    diff = np.abs(x - y)
    if variant == "euclid":
        val = float(np.sqrt((diff ** 2).sum()))
        name, sol = "Euclidean distance", f"√(Σ(x<sub>i</sub>−y<sub>i</sub>)²) = √({fmt((diff ** 2).sum())})"
    elif variant == "manhattan":
        val = float(diff.sum())
        name, sol = "Manhattan (L<sub>1</sub>) distance", f"Σ|x<sub>i</sub>−y<sub>i</sub>| = {' + '.join(fmt(v) for v in diff)}"
    elif variant == "cheb":
        val = float(diff.max())
        name, sol = "Chebyshev (L<sub>∞</sub>) distance", f"max|x<sub>i</sub>−y<sub>i</sub>| = max({', '.join(fmt(v) for v in diff)})"
    elif variant == "mink3":
        val = float(((diff ** 3).sum()) ** (1 / 3))
        name, sol = "Minkowski distance with p = 3", f"(Σ|x<sub>i</sub>−y<sub>i</sub>|³)<super>1/3</super> = ({fmt((diff ** 3).sum())})<super>1/3</super>"
    else:
        c = float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))
        sol = (f"x·y = {fmt(x @ y)}, ‖x‖ = √{fmt(x @ x)}, ‖y‖ = √{fmt(y @ y)}; cos θ = x·y/(‖x‖‖y‖) = {fmt(c, 4)}")
        if variant == "cos":
            val, name = c, "cosine similarity"
        else:
            val, name = 1 - c, "cosine distance (1 − cosine similarity)"
            sol += f"; distance = 1 − {fmt(c, 4)}"
    return Q(text=f"For x = {_pt(x)} and y = {_pt(y)}, the {name} between x and y is ______ " + nat_hint(2),
             qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             solution=[sol + f" = <b>{fmt(val, 2)}</b>.",
                       f"For reference: L<sub>1</sub> = {fmt(diff.sum())}, L<sub>2</sub> = "
                       f"{fmt(np.sqrt((diff ** 2).sum()), 2)}, L<sub>∞</sub> = {fmt(diff.max())} "
                       f"(always L<sub>∞</sub> ≤ L<sub>2</sub> ≤ L<sub>1</sub>)."])


@template(TOPIC, SUB_DIST, marks=1, qtype="NAT")
def dist_jaccard(rng):
    items = ["milk", "bread", "eggs", "butter", "jam", "tea", "rice", "salt", "sugar", "oil"]
    while True:
        m = int(rng.integers(7, 11))
        a = rng.integers(0, 2, m)
        b = rng.integers(0, 2, m)
        f11 = int(((a == 1) & (b == 1)).sum())
        f10 = int(((a == 1) & (b == 0)).sum())
        f01 = int(((a == 0) & (b == 1)).sum())
        f00 = int(((a == 0) & (b == 0)).sum())
        if f11 >= 1 and f10 + f01 >= 1 and f00 >= 1:
            break
    variant = int(rng.integers(0, 3))
    jac = f11 / (f11 + f10 + f01)
    smc = (f11 + f00) / m
    if variant == 0:
        val, name = jac, "Jaccard similarity"
    elif variant == 1:
        val, name = 1 - jac, "Jaccard distance"
    else:
        val, name = smc - jac, "difference (simple matching coefficient − Jaccard similarity)"
    tbl = Table([["Item"] + items[:m], ["Basket A"] + [str(v) for v in a], ["Basket B"] + [str(v) for v in b]],
                header=True)
    sol = [f"Counts: f<sub>11</sub> = {f11}, f<sub>10</sub> = {f10}, f<sub>01</sub> = {f01}, f<sub>00</sub> = {f00}.",
           f"Jaccard J = f<sub>11</sub>/(f<sub>11</sub>+f<sub>10</sub>+f<sub>01</sub>) = {f11}/{f11 + f10 + f01} = "
           f"{fmt(jac, 4)} (0–0 matches are ignored).",
           f"SMC = (f<sub>11</sub>+f<sub>00</sub>)/m = {f11 + f00}/{m} = {fmt(smc, 4)}.",
           f"Required {name} = <b>{fmt(val, 2)}</b>."]
    return Q(text=f"Two shopping baskets are encoded as binary vectors (1 = item bought). The {name} between "
                  f"basket A and basket B is ______ " + nat_hint(2),
             qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2), blocks=[tbl], solution=sol)


@template(TOPIC, SUB_DIST, marks=2, qtype="MCQ")
def dist_nearest(rng):
    metrics = ["manhattan", "euclidean", "chebyshev", "cosine"]
    label = {"manhattan": "Manhattan (L<sub>1</sub>) distance", "euclidean": "Euclidean (L<sub>2</sub>) distance",
             "chebyshev": "Chebyshev (L<sub>∞</sub>) distance", "cosine": "cosine similarity"}
    names = ["A", "B", "C", "D"]
    for _ in range(5000):
        q = rng.integers(1, 6, 2).astype(float)
        P = rng.integers(0, 10, (4, 2)).astype(float)
        if any(np.all(p == q) for p in P) or len({tuple(p) for p in P}) < 4 or np.any(P.sum(1) == 0):
            continue
        sc = {}
        for m in metrics:
            if m == "cosine":
                s = [-(p @ q) / (np.linalg.norm(p) * np.linalg.norm(q)) for p in P]
            else:
                s = [_dist(p, q, m) for p in P]
            o = np.sort(s)
            sc[m] = (int(np.argmin(s)), o[1] - o[0] > 0.04 * (1 if m == "cosine" else 0) + (0.01 if m == "cosine" else 0.2), s)
        met = str(rng.choice(metrics))
        best, clear, s = sc[met]
        if not clear:
            continue
        winners = {sc[m][0] for m in metrics if sc[m][1]}
        if len(winners) >= 3:
            break
    ask = "most similar to" if met == "cosine" else "nearest to"
    opts = [f"Point {nm}" for nm in names]
    a = best
    rows = [["Point", "coordinates"] + [label[m].split(" (")[0].replace(" distance", "") for m in metrics]]
    for i in range(4):
        r = [names[i], _pt(P[i])]
        for m in metrics:
            v = sc[m][2][i]
            r.append(fmt(-v if m == "cosine" else v, 3))
        rows.append(r)

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, P, names)
        ax.scatter([q[0]], [q[1]], marker="*", s=140, color="white", edgecolor="black", zorder=4)
        ax.annotate("q", (q[0], q[1]), xytext=(4, -10), textcoords="offset points", fontsize=8, fontweight="bold")
        ax.scatter([0], [0], marker="+", color="black", s=30)
        _int_grid(ax, np.vstack([P, q, [0, 0]]))
        ax.set_aspect("equal")

    sol = [f"Compute the measure from q = {_pt(q)} to every point (cosine column shows similarity, larger = more "
           f"similar):", Table(rows, header=True),
           f"Under {label[met]} the {ask} q is <b>point {names[best]}</b>.",
           "Note how the answer depends on the measure: "
           + "; ".join(f"{label[m]} → {names[sc[m][0]]}" for m in metrics) + ". Cosine similarity looks only at "
           "the angle from the origin, L<sub>1</sub> sums coordinate gaps, L<sub>∞</sub> takes the largest gap."]
    return Q(text=f"A query point q = {_pt(q)} and four points A–D are shown below. Using <b>{label[met]}</b>, "
                  f"which point is {ask} q?",
             qtype="MCQ", marks=2, options=opts, answer=a,
             blocks=[_points_table(names, P), Figure(draw, 7, 6)], solution=sol)


@template(TOPIC, SUB_DIST, marks=2, qtype="NAT")
def dist_scaling(rng):
    names = ["A", "B", "C"]
    for _ in range(10000):
        age = rng.integers(20, 61, 3).astype(float)
        inc = (rng.integers(2, 41, 3) * 5).astype(float)  # thousand rupees
        amin, amax = 20.0, 60.0
        imin, imax = 10.0, 210.0
        X = np.c_[age, inc]
        Z = np.c_[(age - amin) / (amax - amin), (inc - imin) / (imax - imin)]
        r = [_dist(X[0], X[i]) for i in (1, 2)]
        s = [_dist(Z[0], Z[i]) for i in (1, 2)]
        if abs(r[0] - r[1]) > 3 and abs(s[0] - s[1]) > 0.05 and (np.argmin(r) != np.argmin(s)) and min(s) > 0.05:
            break
    variant = int(rng.integers(0, 2))
    if variant == 0:
        val = min(s)
        ask = ("After min–max scaling of each feature to [0, 1] (using the stated ranges), the Euclidean distance "
               "from A to its <b>nearest</b> neighbour among B and C is ______")
    else:
        val = min(r)
        ask = ("On the <b>raw</b> (unscaled) features, the Euclidean distance from A to its nearest neighbour among B "
               "and C is ______")
    tbl = Table([["Customer", "Age (years)", "Income (₹ thousand)"]] +
                [[names[i], fmt(age[i]), fmt(inc[i])] for i in range(3)], header=True)
    sol = ["Min–max scaling: x′ = (x − min)/(max − min); age range [20, 60], income range [10, 210].",
           Table([["Customer", "age′", "income′"]] + [[names[i], fmt(Z[i, 0], 4), fmt(Z[i, 1], 4)] for i in range(3)],
                 header=True),
           f"Raw distances: d(A,B) = {fmt(r[0], 2)}, d(A,C) = {fmt(r[1], 2)} → nearest is {names[1 + int(np.argmin(r))]} "
           f"(income dominates because of its larger range).",
           f"Scaled distances: d(A,B) = {fmt(s[0], 4)}, d(A,C) = {fmt(s[1], 4)} → nearest is "
           f"{names[1 + int(np.argmin(s))]}.",
           f"Answer: <b>{fmt(val, 2)}</b>. Scaling changes which neighbour is nearest — distance-based methods "
           f"(k-means, k-NN, hierarchical clustering) should be run on standardized features."]
    return Q(text="Three customers are described by age and income. Age ranges over [20, 60] years and income over "
                  "[10, 210] thousand rupees in the full dataset. " + ask + " " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(val, 2), nat_hint=nat_hint(2), blocks=[tbl], solution=sol)


DIST_T = [
    ("Minkowski distance with p = 1 is the Manhattan distance and with p = 2 the Euclidean distance.", "Definitions."),
    ("As p → ∞ the Minkowski distance tends to the Chebyshev distance max<sub>i</sub>|x<sub>i</sub> − y<sub>i</sub>|.",
     "The largest coordinate gap dominates."),
    ("For any two vectors, L<sub>∞</sub> ≤ L<sub>2</sub> ≤ L<sub>1</sub> distance.", "Standard norm inequalities."),
    ("Cosine similarity is unchanged if one of the vectors is multiplied by a positive scalar.",
     "It depends only on the angle."),
    ("Cosine distance 1 − cos θ does not satisfy the triangle inequality in general.",
     "So it is not a true metric."),
    ("The Jaccard similarity of sets A and B is |A ∩ B| / |A ∪ B|.", "Definition."),
    ("Jaccard similarity ignores 0–0 matches, which suits sparse asymmetric binary data.",
     "Shared absences carry little information, e.g. items not bought."),
    ("Euclidean distance is invariant to rotations and translations of the coordinate system.",
     "Orthogonal transforms preserve L<sub>2</sub> norms."),
    ("Features with large numeric ranges dominate the Euclidean distance unless the data are standardized.",
     "Squared differences of a large-range feature swamp the others."),
    ("Minkowski 'distance' with 0 &lt; p &lt; 1 violates the triangle inequality.",
     "e.g. p = 0.5: d((0,0),(1,1)) = 4, which exceeds d((0,0),(1,0)) + d((1,0),(1,1)) = 2."),
    ("For unit-length vectors, squared Euclidean distance equals 2(1 − cos θ).",
     "‖x − y‖² = 2 − 2x·y."),
    ("The Hamming distance between two binary vectors equals their Manhattan distance.",
     "Each mismatched coordinate contributes 1."),
    ("Mahalanobis distance accounts for feature correlations through the inverse covariance matrix.",
     "d² = (x − y)ᵀ Σ⁻¹ (x − y)."),
    ("Manhattan distance is not invariant to rotations of the coordinate axes.",
     "e.g. (1,0) → (1/√2, 1/√2) changes L<sub>1</sub> norm from 1 to √2."),
    ("Jaccard distance 1 − J(A, B) is a metric on finite sets.", "It satisfies the triangle inequality."),
]
DIST_F = [
    ("Cosine similarity changes when both vectors are multiplied by the same positive constant.",
     "Scaling does not change the angle."),
    ("Manhattan distance is always ≤ Euclidean distance.", "It is the other way round: L<sub>2</sub> ≤ L<sub>1</sub>."),
    ("Chebyshev distance is the sum of absolute coordinate differences.", "That is Manhattan; Chebyshev is the max."),
    ("Minkowski distance with p = 0.5 is a metric.", "For p &lt; 1 the triangle inequality fails."),
    ("Euclidean distance is unaffected by changing the unit of one feature (e.g. metres to centimetres).",
     "Rescaling one coordinate changes distances."),
    ("Jaccard similarity counts 0–0 matches as agreements.", "That is the simple matching coefficient."),
    ("Cosine similarity between two vectors with non-negative entries can be negative.",
     "Their dot product is ≥ 0, so cos θ ≥ 0."),
    ("Cosine distance 1 − cos θ satisfies the triangle inequality for all vectors.", "It does not in general."),
    ("Manhattan distance is invariant to rotations of the coordinate axes.", "Only L<sub>2</sub> is rotation-invariant."),
    ("Two vectors with cosine similarity 1 must be identical.", "They need only point in the same direction."),
    ("The Jaccard similarity of two identical non-empty sets is 0.", "It is 1."),
    ("The simple matching coefficient and the Jaccard coefficient are always equal for binary vectors.",
     "They differ whenever there are 0–0 matches."),
    ("The Chebyshev distance is always ≥ the Euclidean distance.", "L<sub>∞</sub> ≤ L<sub>2</sub>."),
]


@template(TOPIC, SUB_DIST, marks=1, qtype="MSQ")
def dist_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, DIST_T, DIST_F)
    return Q(text="Which of the following statements about distance / similarity measures is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# ============================================================================
# CLUSTER EVALUATION
# ============================================================================
@template(TOPIC, SUB_EVAL, marks=2, qtype="NAT")
def silhouette_point(rng):
    while True:
        k = int(rng.choice([2, 3]))
        sizes = [int(rng.integers(2, 4)) for _ in range(k)]
        centers = rng.integers(1, 10, (k, 2)).astype(float)
        if min(_dist(centers[a], centers[b]) for a, b in combinations(range(k), 2)) < 3.5:
            continue
        X, lab = [], []
        for g in range(k):
            for _ in range(sizes[g]):
                X.append(centers[g] + rng.integers(-2, 3, 2))
                lab.append(g)
        X = np.array(X, float)
        if len({tuple(p) for p in X}) < len(X):
            continue
        metric = "euclidean" if rng.random() < 0.6 else "manhattan"
        n = len(X)
        i = int(rng.integers(0, n))
        own = [j for j in range(n) if lab[j] == lab[i] and j != i]
        a = np.mean([_dist(X[i], X[j], metric) for j in own])
        bs = {g: np.mean([_dist(X[i], X[j], metric) for j in range(n) if lab[j] == g]) for g in range(k) if g != lab[i]}
        b = min(bs.values())
        if len(bs) > 1 and sorted(bs.values())[1] - b < 0.1:
            continue
        s = (b - a) / max(a, b)
        break
    names = _names(n)
    cn = ["C1", "C2", "C3"]
    mname = "Euclidean" if metric == "euclidean" else "Manhattan"

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, X, names, lab)
        for g in range(k):
            ax.scatter([], [], marker=MARKERS[g], color=GREYS[g], edgecolor="black", label=cn[g])
        ax.legend(loc="best", frameon=False)
        _int_grid(ax, X)

    tbl = Table([["Point"] + names, ["x₁"] + [fmt(v) for v in X[:, 0]], ["x₂"] + [fmt(v) for v in X[:, 1]],
                 ["cluster"] + [cn[g] for g in lab]], header=False)
    sol = [f"a(i) = mean {mname} distance from {names[i]} to the other members of its own cluster {cn[lab[i]]}: "
           + ", ".join(f"d({names[i]},{names[j]}) = {fmt(_dist(X[i], X[j], metric), 3)}" for j in own)
           + f" → a = {fmt(a, 4)}.",
           "b(i) = smallest mean distance to the points of another cluster: "
           + "; ".join(f"{cn[g]}: {fmt(v, 4)}" for g, v in bs.items()) + f" → b = {fmt(b, 4)}.",
           f"s(i) = (b − a)/max(a, b) = ({fmt(b, 4)} − {fmt(a, 4)})/{fmt(max(a, b), 4)} = <b>{fmt(s, 2)}</b>.",
           "s ranges in [−1, 1]; values near 1 mean well clustered, negative values suggest a wrong assignment."]
    return Q(text=f"A clustering of {n} points into {k} clusters is shown below. Using {mname} distance, the "
                  f"silhouette coefficient s(i) = (b(i) − a(i))/max(a(i), b(i)) of point {names[i]} is ______ "
                  + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(s, 2), nat_hint=nat_hint(2),
             blocks=[tbl, Figure(draw, 8, 5.5)], solution=sol)


@template(TOPIC, SUB_EVAL, marks=1, qtype="NAT")
def purity(rng):
    while True:
        M = rng.integers(0, 12, (3, 3))
        for r in range(3):
            M[r, rng.integers(0, 3)] += int(rng.integers(8, 20))
        if M.sum(1).min() > 0:
            break
    N = int(M.sum())
    mx = M.max(1)
    variant = int(rng.integers(0, 2))
    if variant == 0:
        val, d = mx.sum() / N, 2
        ask = "The purity of this clustering is ______"
    else:
        val, d = N - int(mx.sum()), 0
        ask = ("If every point in a cluster is labelled with the cluster's majority class, the number of misclassified "
               "points is ______")
    classes = ["Class P", "Class Q", "Class R"]
    tbl = Table([["", *classes]] + [[f"Cluster {r + 1}"] + [str(v) for v in M[r]] for r in range(3)], header=True)
    sol = [f"Majority count in each cluster: {', '.join(str(v) for v in mx)} (sum {int(mx.sum())}); N = {N}.",
           f"Purity = (1/N) Σ<sub>k</sub> max<sub>j</sub> n<sub>kj</sub> = {int(mx.sum())}/{N} = {fmt(mx.sum() / N, 4)}.",
           f"Misclassified = N − Σ max = {N - int(mx.sum())}.", f"Answer: <b>{fmt(val, d)}</b>.",
           "Purity is an external measure (needs class labels) and is trivially 1 if each point forms its own "
           "cluster, so it cannot be used to choose k."]
    return Q(text="A clustering algorithm groups labelled data into three clusters; the contingency table of cluster "
                  "versus true class counts is given below. " + ask + " " + nat_hint(d),
             qtype="NAT", marks=1, answer=nat_range(val, d) if d else (val, val), nat_hint=nat_hint(d),
             blocks=[tbl], solution=sol)


@template(TOPIC, SUB_EVAL, marks=2, qtype="NAT")
def rand_index(rng):
    while True:
        n = int(rng.integers(6, 9))
        U = rng.integers(0, int(rng.integers(2, 4)), n)
        V = U.copy()
        flip = rng.choice(n, int(rng.integers(1, 4)), replace=False)
        V[flip] = rng.integers(0, 3, len(flip))
        if len(set(U.tolist())) >= 2 and len(set(V.tolist())) >= 2 and not np.array_equal(U, V):
            break
    a = b = c = d_ = 0
    for i, j in combinations(range(n), 2):
        su, sv = U[i] == U[j], V[i] == V[j]
        if su and sv:
            a += 1
        elif not su and not sv:
            b += 1
        elif su:
            c += 1
        else:
            d_ += 1
    tot = n * (n - 1) // 2
    ri = (a + b) / tot
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val, dd, ask = ri, 2, "the Rand index between the two clusterings is ______"
    elif variant == 1:
        val, dd, ask = a, 0, "the number of point pairs placed in the same cluster by <b>both</b> clusterings is ______"
    else:
        val, dd, ask = c + d_, 0, "the number of point pairs on which the two clusterings <b>disagree</b> is ______"
    names = _names(n)
    lu = ["α", "β", "γ"]
    tbl = Table([["Point"] + names, ["Clustering U"] + [lu[u] for u in U], ["Clustering V"] + [str(v + 1) for v in V]],
                header=True)
    sol = [f"Total pairs = C({n},2) = {tot}.",
           f"a = pairs together in both = {a}; b = pairs separated in both = {b}; pairs together in U only = {c}; "
           f"together in V only = {d_}.",
           f"Rand index = (a + b)/C(n,2) = ({a} + {b})/{tot} = {fmt(ri, 4)}.",
           f"Answer: <b>{fmt(val, dd)}</b>. (Cluster names do not matter: only whether pairs are together.)"]
    return Q(text=f"Two clusterings U and V of {n} points are given below (cluster names are arbitrary). Then "
                  + ask + " " + nat_hint(dd),
             qtype="NAT", marks=2, answer=nat_range(val, dd) if dd else (val, val), nat_hint=nat_hint(dd),
             blocks=[tbl], solution=sol)


EVAL_T = [
    ("The silhouette coefficient of a point lies in [−1, 1].", "s = (b − a)/max(a, b)."),
    ("A silhouette close to 1 means the point is much closer to its own cluster than to the nearest other cluster.",
     "a ≪ b gives s ≈ 1."),
    ("A negative silhouette suggests that the point may be assigned to the wrong cluster.",
     "It is on average closer to another cluster (b &lt; a)."),
    ("Purity is an external validation measure: it needs ground-truth class labels.", "Majority class per cluster."),
    ("Purity can be made equal to 1 by putting every point in its own cluster.",
     "Hence purity alone cannot choose k."),
    ("The Rand index is the fraction of point pairs on which two clusterings agree (both together or both apart).",
     "RI = (a + b)/C(n, 2)."),
    ("The Rand index of a clustering compared with itself is 1.", "All pairs agree."),
    ("The silhouette coefficient is an internal measure: it uses only the data and the cluster assignments.",
     "No ground-truth labels are needed."),
    ("The adjusted Rand index corrects the Rand index for chance; its expected value under random labelings is 0.",
     "That is the purpose of the adjustment."),
    ("The average silhouette width can be used to choose k by picking the k with the largest value.",
     "A common model-selection heuristic."),
    ("The Rand index is unchanged if the cluster labels are renamed (e.g. 1 ↔ 2).",
     "It depends only on pair co-membership."),
    ("The Rand index can compare two clusterings with different numbers of clusters.", "Only pairs are compared."),
]
EVAL_F = [
    ("Purity penalizes having many clusters, so maximizing it is a good way to choose k.",
     "Purity increases (weakly) with more clusters."),
    ("The silhouette coefficient always lies in [0, 1].", "It can be negative; range is [−1, 1]."),
    ("A silhouette value of −1 indicates a perfectly clustered point.", "+1 is ideal; −1 is worst."),
    ("The Rand index requires the two clusterings to have the same number of clusters.", "It compares pairs only."),
    ("Purity is an internal measure that needs no class labels.", "It needs ground-truth labels."),
    ("The (unadjusted) Rand index of two random labelings has expected value 0.",
     "It is typically well above 0; the ARI is the chance-corrected version."),
    ("The Rand index changes if the cluster labels are renamed.", "Renaming does not change co-membership."),
    ("A larger within-cluster SSE indicates more compact clusters.", "Compact clusters have smaller SSE."),
    ("In the silhouette, b(i) is the mean distance to the farthest other cluster.",
     "b(i) uses the nearest other cluster."),
    ("A silhouette of 0 means the point coincides with its cluster centroid.",
     "s = 0 means a = b: the point lies between two clusters."),
]


@template(TOPIC, SUB_EVAL, marks=1, qtype="MSQ")
def eval_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, EVAL_T, EVAL_F)
    return Q(text="Which of the following statements about clustering evaluation measures is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# ============================================================================
# PCA & DIMENSIONALITY REDUCTION
# ============================================================================
def _eig2(S):
    w, V = np.linalg.eigh(S)
    o = np.argsort(w)[::-1]
    w, V = w[o], V[:, o]
    for j in range(V.shape[1]):
        if V[0, j] < 0 or (abs(V[0, j]) < 1e-12 and V[1, j] < 0):
            V[:, j] *= -1
    return w, V


@template(TOPIC, SUB_PCA, marks=1, qtype="NAT")
def pca_covariance(rng):
    while True:
        n = int(rng.choice([4, 5]))
        X = rng.integers(-4, 5, (n, 2)).astype(float)
        X[-1] = -X[:-1].sum(0)
        if X[:, 0].std() > 0 and X[:, 1].std() > 0 and np.abs(X).max() <= 7 and abs(np.corrcoef(X.T)[0, 1]) < 0.999:
            break
    S = X.T @ X / (n - 1)
    variant = int(rng.integers(0, 4))
    if variant == 0:
        val, what = S[0, 0], "the sample variance of x₁ (divisor n − 1)"
    elif variant == 1:
        val, what = S[0, 1], "the sample covariance between x₁ and x₂ (divisor n − 1)"
    elif variant == 2:
        val, what = np.trace(S), "the total variance (trace of the sample covariance matrix, divisor n − 1)"
    else:
        val, what = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1]), "the correlation coefficient between x₁ and x₂"
    sol = ["The data are already centered (column means are 0), so S = XᵀX/(n − 1).",
           f"Σx₁² = {fmt((X[:, 0] ** 2).sum())}, Σx₂² = {fmt((X[:, 1] ** 2).sum())}, Σx₁x₂ = {fmt((X[:, 0] * X[:, 1]).sum())}.",
           f"S = [[{fmt(S[0, 0], 4)}, {fmt(S[0, 1], 4)}], [{fmt(S[1, 0], 4)}, {fmt(S[1, 1], 4)}]].",
           f"Required value = <b>{fmt(val, 2)}</b>."
           + (" (Dividing by n instead of n − 1 would give " + fmt(val * (n - 1) / n, 2) + ".)" if variant < 3 else "")]
    return Q(text=f"The {n} two-dimensional observations below have zero mean in each feature. Then {what} is ______ "
                  + nat_hint(2),
             qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[_points_table(_names(n, "x"), X, ("x₁", "x₂"))], solution=sol)


@template(TOPIC, SUB_PCA, marks=2, qtype="NAT")
def pca_eig_2x2(rng):
    while True:
        a = int(rng.integers(1, 13))
        c = int(rng.integers(1, 13))
        b = int(rng.integers(-6, 7))
        if b == 0 or a * c - b * b <= 0:
            continue
        S = np.array([[a, b], [b, c]], float)
        w, V = _eig2(S)
        if abs(V[0, 0]) < 0.05:
            continue
        break
    variant = int(rng.integers(0, 4))
    disc = math.sqrt(((a - c) / 2) ** 2 + b * b)
    if variant == 0:
        val, ask = w[0], "the variance of the data along the first principal component is ______"
    elif variant == 1:
        val, ask = 100 * w[0] / w.sum(), "the percentage of total variance explained by the first principal component is ______"
    elif variant == 2:
        val, ask = V[1, 0] / V[0, 0], ("if the first principal direction is written as (1, m) (up to scaling), the "
                                       "value of m is ______")
    else:
        val, ask = w[1], "the variance of the data along the second principal component is ______"
    sol = ["Eigenvalues of [[a, b], [b, c]]: λ = (a + c)/2 ± √(((a − c)/2)² + b²).",
           f"λ = {fmt((a + c) / 2, 2)} ± √({fmt(((a - c) / 2) ** 2, 2)} + {b * b}) = {fmt((a + c) / 2, 2)} ± {fmt(disc, 4)} "
           f"→ λ₁ = {fmt(w[0], 4)}, λ₂ = {fmt(w[1], 4)} (check: λ₁ + λ₂ = trace = {a + c}, λ₁λ₂ = det = {a * c - b * b}).",
           f"Eigenvector for λ₁: (S − λ₁I)v = 0 → ({fmt(a - w[0], 4)})v₁ + ({b})v₂ = 0 → v ∝ (1, {fmt(V[1, 0] / V[0, 0], 4)}).",
           f"PVE(PC1) = λ₁/(λ₁ + λ₂) = {fmt(100 * w[0] / w.sum(), 2)}%.",
           f"Answer: <b>{fmt(val, 2)}</b>."]
    return Q(text="The sample covariance matrix of a two-feature dataset is S given below. In principal component "
                  "analysis, " + ask + " " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[Matrix("S", S, 0)], solution=sol)


@template(TOPIC, SUB_PCA, marks=1, qtype="NAT")
def pca_scree(rng):
    while True:
        d = int(rng.integers(6, 9))
        lam = np.sort(np.round(rng.exponential(1.0, d) * 10, 1) + 0.2)[::-1]
        lam = np.round(lam, 1)
        if len(set(lam)) < d:
            continue
        cum = np.cumsum(lam) / lam.sum() * 100
        thr = int(rng.choice([70, 75, 80, 85, 90, 95]))
        kk = int(np.argmax(cum >= thr)) + 1
        if np.min(np.abs(cum - thr)) < 0.6 or kk == d or kk < 2:
            continue
        break
    variant = int(rng.integers(0, 2))
    if variant == 0:
        val, dd = kk, 0
        ask = (f"The minimum number of principal components needed to explain at least {thr}% of the total "
               f"variance is ______")
    else:
        val, dd = cum[1], 1
        ask = "The percentage of total variance explained by the first two principal components together is ______"

    def draw(fig):
        ax = fig.add_subplot(111)
        bars = ax.bar(range(1, d + 1), lam, color="#999999", edgecolor="black")
        for i, v in enumerate(lam):
            ax.text(i + 1, v + lam.max() * 0.02, fmt(v, 1), ha="center", fontsize=7)
        ax.plot(range(1, d + 1), lam, "-o", color="black", ms=3)
        ax.set_xlabel("principal component")
        ax.set_ylabel("eigenvalue (variance)")
        ax.set_xticks(range(1, d + 1))
        ax.set_ylim(0, lam.max() * 1.15)

    rows = [["k"] + [str(i + 1) for i in range(d)], ["λ<sub>k</sub>"] + [fmt(v, 1) for v in lam],
            ["cumulative %"] + [fmt(v, 2) for v in cum]]
    sol = [f"Total variance = Σλ = {fmt(lam.sum(), 1)}. Cumulative proportion of variance explained:",
           Table(rows, header=False)]
    if variant == 0:
        sol.append(f"The cumulative share first reaches {thr}% at k = <b>{kk}</b>.")
    else:
        sol.append(f"(λ₁ + λ₂)/Σλ = {fmt(lam[0] + lam[1], 1)}/{fmt(lam.sum(), 1)} = <b>{fmt(val, 1)}%</b>.")
    return Q(text=f"The scree plot below shows the eigenvalues of the covariance matrix of a {d}-dimensional dataset. "
                  + ask + " " + nat_hint(dd),
             qtype="NAT", marks=1, answer=nat_range(val, dd, 0.2) if dd else (val, val), nat_hint=nat_hint(dd),
             blocks=[Figure(draw, 8.5, 5)], solution=sol)


@template(TOPIC, SUB_PCA, marks=2, qtype="NAT")
def pca_projection(rng):
    while True:
        n = 5
        X = rng.integers(0, 10, (n, 2)).astype(float)
        mu = X.mean(0)
        Xc = X - mu
        S = Xc.T @ Xc / (n - 1)
        w, V = _eig2(S)
        if w[1] < 1e-9 or w[0] / w[1] < 2.5 or abs(V[0, 0]) < 0.15:
            continue
        i = int(rng.integers(0, n))
        z = float(V[:, 0] @ Xc[i])
        if abs(z) < 0.3:
            continue
        break
    names = _names(n)
    v = V[:, 0]
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val = z
        ask = (f"Taking the unit-length first principal direction with a <b>positive first component</b>, the score "
               f"(projection) of {names[i]} on PC1 is ______")
    elif variant == 1:
        val = float(Xc[i] @ Xc[i] - z * z)
        ask = (f"If each point is reconstructed from its PC1 score only (x̂ = x̄ + z₁v₁), the squared reconstruction "
               f"error ‖x − x̂‖² of {names[i]} is ______")
    else:
        val = w[0]
        ask = "The sample variance (divisor n − 1) of the PC1 scores of the five points is ______"

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_labeled(ax, X, names)
        ax.scatter([mu[0]], [mu[1]], marker="+", s=80, color="black")
        ax.annotate("mean", (mu[0], mu[1]), xytext=(4, -10), textcoords="offset points", fontsize=7)
        _int_grid(ax, X)
        ax.set_aspect("equal")

    sol = [f"Mean x̄ = {_pt(mu)}. Centered data rows: " + ", ".join(f"{names[j]}: {_pt(Xc[j])}" for j in range(n)) + ".",
           f"Sample covariance S = (1/(n − 1)) Σ(x − x̄)(x − x̄)ᵀ = [[{fmt(S[0, 0], 4)}, {fmt(S[0, 1], 4)}], "
           f"[{fmt(S[1, 0], 4)}, {fmt(S[1, 1], 4)}]].",
           f"Eigenvalues: λ₁ = {fmt(w[0], 4)}, λ₂ = {fmt(w[1], 4)}; unit PC1 direction v₁ = ({fmt(v[0], 4)}, {fmt(v[1], 4)}).",
           f"Score z₁ = v₁ · (x − x̄) = {fmt(v[0], 4)}·{fmt(Xc[i, 0], 2)} + {fmt(v[1], 4)}·{fmt(Xc[i, 1], 2)} = {fmt(z, 4)}."]
    if variant == 1:
        sol.append(f"‖x − x̄‖² = {fmt(Xc[i] @ Xc[i], 4)}; error = ‖x − x̄‖² − z₁² = {fmt(Xc[i] @ Xc[i], 4)} − "
                   f"{fmt(z * z, 4)} = <b>{fmt(val, 2)}</b> (Pythagoras: the residual is the PC2 component).")
    elif variant == 2:
        sol.append(f"The variance of the PC1 scores equals the top eigenvalue: <b>{fmt(val, 2)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(val, 2)}</b> (the sign depends on the orientation of v₁; with the stated "
                   f"convention it is {fmt(val, 2)}).")
    return Q(text="PCA is applied to the five 2-D points below (data are mean-centered first; sample covariance uses "
                  "divisor n − 1). " + ask + " " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             blocks=[_points_table(names, X), Figure(draw, 7, 5.5)], solution=sol)


@template(TOPIC, SUB_PCA, marks=2, qtype="NAT")
def pca_reconstruction(rng):
    while True:
        d = int(rng.integers(5, 8))
        lam = np.sort(rng.integers(1, 41, d).astype(float) / 2)[::-1]
        if len(set(lam)) < d:
            continue
        k = int(rng.integers(1, d - 1))
        n = int(rng.choice([11, 21, 51, 101]))
        break
    disc = lam[k:].sum()
    variant = int(rng.integers(0, 3))
    if variant == 0:
        val, dd = disc, 2
        ask = (f"the mean squared reconstruction error (1/(n − 1)) Σ<sub>i</sub> ‖x<sub>i</sub> − x̂<sub>i</sub>‖², "
               f"when each point is projected onto the top {k} principal components, is ______")
    elif variant == 1:
        val, dd = (n - 1) * disc, 2
        ask = (f"with n = {n} samples, the total squared reconstruction error Σ<sub>i</sub> ‖x<sub>i</sub> − "
               f"x̂<sub>i</sub>‖² when keeping the top {k} principal components is ______")
    else:
        val, dd = 100 * disc / lam.sum(), 2
        ask = f"the percentage of total variance <b>lost</b> by keeping only the top {k} principal components is ______"
    sol = ["For centered data, projecting onto the top-k PCs and reconstructing leaves the components along the "
           "discarded eigenvectors; their average squared length (divisor n − 1) is the sum of the discarded "
           "eigenvalues.",
           f"Discarded eigenvalues: {', '.join(fmt(v, 2) for v in lam[k:])}; sum = {fmt(disc, 2)}; total = {fmt(lam.sum(), 2)}."]
    if variant == 1:
        sol.append(f"Total error = (n − 1) × {fmt(disc, 2)} = {n - 1} × {fmt(disc, 2)} = <b>{fmt(val, 2)}</b>.")
    elif variant == 2:
        sol.append(f"Lost fraction = {fmt(disc, 2)}/{fmt(lam.sum(), 2)} = <b>{fmt(val, 2)}%</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(val, 2)}</b>. (A common mistake is to add the <i>retained</i> eigenvalues "
                   f"{fmt(lam[:k].sum(), 2)}.)")
    return Q(text=f"The eigenvalues of the sample covariance matrix (divisor n − 1) of a centered {d}-dimensional "
                  f"dataset are {', '.join(fmt(v, 2) for v in lam)}. Then " + ask + " " + nat_hint(dd),
             qtype="NAT", marks=2, answer=nat_range(val, dd), nat_hint=nat_hint(dd), solution=sol)


@template(TOPIC, SUB_PCA, marks=2, qtype="NAT")
def pca_svd(rng):
    while True:
        d = int(rng.integers(3, 5))
        sig = np.sort(rng.integers(2, 31, d).astype(float))[::-1]
        if len(set(sig)) < d:
            continue
        n = int(rng.choice([5, 9, 11, 17, 21, 26, 51]))
        lam = sig ** 2 / (n - 1)
        cum = np.cumsum(lam) / lam.sum() * 100
        thr = int(rng.choice([80, 90, 95]))
        if np.min(np.abs(cum - thr)) < 0.5:
            continue
        break
    variant = int(rng.integers(0, 4))
    j = int(rng.integers(0, d))
    ordn = ["first", "second", "third", "fourth"]
    if variant == 0:
        val, dd = lam[j], 2
        ask = f"the variance of the data along the {ordn[j]} principal component is ______"
    elif variant == 1:
        val, dd = cum[0], 2
        ask = "the percentage of total variance explained by the first principal component is ______"
    elif variant == 2:
        val, dd = int(np.argmax(cum >= thr)) + 1, 0
        ask = f"the minimum number of principal components needed to retain at least {thr}% of the variance is ______"
    else:
        val, dd = lam.sum(), 2
        ask = "the total variance (trace of the sample covariance matrix) is ______"
    sol = ["With X = UΣVᵀ (X centered, n × d), the sample covariance is S = XᵀX/(n − 1) = V(Σ²/(n − 1))Vᵀ, so the "
           "PC directions are the columns of V and the eigenvalues are λ<sub>j</sub> = σ<sub>j</sub>²/(n − 1).",
           "λ = " + ", ".join(f"{fmt(s)}²/{n - 1} = {fmt(l, 4)}" for s, l in zip(sig, lam)) + ".",
           "Cumulative % variance: " + ", ".join(fmt(c, 2) for c in cum) + " (note the (n − 1) factor cancels in "
           "proportions: PVE = σ<sub>j</sub>²/Σσ²).",
           f"Answer: <b>{fmt(val, dd)}</b>. (Using σ instead of σ² is the classic mistake.)"]
    return Q(text=f"A centered data matrix X with n = {n} rows (samples) and d = {d} columns has singular values "
                  f"{', '.join(fmt(s) for s in sig)}. Using the sample covariance with divisor n − 1, "
                  + ask + " " + nat_hint(dd),
             qtype="NAT", marks=2, answer=nat_range(val, dd) if dd else (val, val), nat_hint=nat_hint(dd),
             solution=sol)


@template(TOPIC, SUB_PCA, marks=1, qtype="MCQ")
def pca_direction_figure(rng):
    th = float(rng.choice([1, -1]) * rng.uniform(20, 70))
    t = np.deg2rad(th)
    u = np.array([np.cos(t), np.sin(t)])
    w = np.array([-np.sin(t), np.cos(t)])
    pts = rng.normal(0, 2.4, (60, 1)) * u + rng.normal(0, 0.6, (60, 1)) * w + np.array([5, 5])
    angles = {"PC": th, "perp": th + 90, "p45": th + 45, "m45": th - 45}
    keys = list(angles)
    perm = rng.permutation(4)
    lab = {keys[perm[i]]: "ABCD"[i] for i in range(4)}
    ask_pc2 = rng.random() < 0.35
    target = "perp" if ask_pc2 else "PC"

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(pts[:, 0], pts[:, 1], s=8, color="#555555")
        c = pts.mean(0)
        for kname, ang in angles.items():
            r = np.deg2rad(ang)
            dvec = 3.6 * np.array([np.cos(r), np.sin(r)])
            ax.annotate("", xy=c + dvec, xytext=c, arrowprops=dict(arrowstyle="->", lw=1.4, color="black"))
            ax.text(*(c + 1.15 * dvec), lab[kname], fontsize=9, fontweight="bold", ha="center", va="center")
        ax.set_aspect("equal")
        ax.set_xlim(c[0] - 6, c[0] + 6)
        ax.set_ylim(c[1] - 5.5, c[1] + 5.5)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.grid(alpha=0.25)

    opts = [f"Direction {L}" for L in "ABCD"]
    ans = "ABCD".index(lab[target])
    which = "second principal component (PC2)" if ask_pc2 else "first principal component (PC1)"
    return Q(text=f"The scatter plot shows a 2-D dataset together with four candidate directions A–D drawn from the "
                  f"data mean. Which direction best represents the {which}?",
             qtype="MCQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 7, 6.2)],
             solution=[f"PC1 is the direction of maximum variance — along the long axis of the elongated cloud "
                       f"(direction {lab['PC']}). PC2 must be orthogonal to PC1 and captures the remaining variance "
                       f"(direction {lab['perp']}).",
                       f"Answer: <b>Direction {lab[target]}</b>. Directions {lab['p45']} and {lab['m45']} are at 45° "
                       f"to the main axis and capture intermediate variance."])


@template(TOPIC, SUB_PCA, marks=1, qtype="MCQ")
def pca_vs_lda(rng):
    th = float(rng.uniform(-60, 60))
    t = np.deg2rad(th)
    u = np.array([np.cos(t), np.sin(t)])
    w = np.array([-np.sin(t), np.cos(t)])
    m = 40
    A = rng.normal(0, 2.6, (m, 1)) * u + rng.normal(0, 0.35, (m, 1)) * w + 1.1 * w
    B = rng.normal(0, 2.6, (m, 1)) * u + rng.normal(0, 0.35, (m, 1)) * w - 1.1 * w
    swap = rng.random() < 0.5
    d1, d2 = (u, w) if not swap else (w, u)

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(A[:, 0], A[:, 1], s=10, marker="o", color="#222222", label="class 1")
        ax.scatter(B[:, 0], B[:, 1], s=12, marker="^", facecolor="white", edgecolor="#444444", label="class 2")
        for vec, nm in ((d1, "d₁"), (d2, "d₂")):
            ax.annotate("", xy=4.2 * vec, xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=1.6, color="black"))
            ax.text(*(4.8 * vec), nm, fontsize=9, fontweight="bold", ha="center", va="center")
        ax.set_aspect("equal")
        ax.set_xlim(-6.5, 6.5)
        ax.set_ylim(-5.5, 5.5)
        ax.legend(loc="lower right", frameon=False, fontsize=6.5)
        ax.grid(alpha=0.25)

    pc_lab = "d₁" if not swap else "d₂"
    lda_lab = "d₂" if not swap else "d₁"
    correct = f"PCA (1st PC) chooses {pc_lab}; LDA chooses {lda_lab}"
    dis = [f"PCA (1st PC) chooses {lda_lab}; LDA chooses {pc_lab}",
           f"Both PCA and LDA choose {pc_lab}", f"Both PCA and LDA choose {lda_lab}"]
    opts, a = mcq(rng, correct, dis)
    return Q(text="Two labelled classes are shown below, together with two orthogonal directions d₁ and d₂. A single "
                  "direction is to be selected by (i) PCA (first principal component, ignoring labels) and (ii) "
                  "Fisher's LDA. Which statement is correct?",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 7, 6)],
             solution=[f"PCA is unsupervised: it picks the direction of maximum total variance, which is along the long "
                       f"axis of the clouds ({pc_lab}).",
                       f"LDA is supervised: it maximizes between-class separation relative to within-class scatter, "
                       f"so it picks the direction across which the class means differ ({lda_lab}).",
                       f"Answer: <b>{correct}</b>. Projecting on the PCA direction would mix the two classes completely."])


@template(TOPIC, SUB_PCA, marks=1, qtype="NAT")
def curse_of_dim(rng):
    variant = int(rng.integers(0, 3))
    if variant == 0:
        r = float(rng.choice([0.01, 0.05, 0.1, 0.2]))
        d = int(rng.choice([3, 5, 10, 20, 50]))
        val = r ** (1 / d)
        text = (f"Data are uniformly distributed in the d-dimensional unit hypercube with d = {d}. A sub-cube is to "
                f"capture a fraction r = {fmt(r, 2)} of the data. The required edge length of the sub-cube is ______")
        sol = [f"Volume of sub-cube = e<super>d</super> = r ⇒ e = r<super>1/d</super> = {fmt(r, 2)}<super>1/{d}</super> "
               f"= <b>{fmt(val, 2)}</b>.",
               "Even to capture a small fraction of data, the 'local' neighbourhood must span most of each "
               "feature's range — the curse of dimensionality."]
    elif variant == 1:
        eps = float(rng.choice([0.01, 0.02, 0.05, 0.1]))
        d = int(rng.choice([5, 10, 20, 50, 100]))
        val = 1 - (1 - 2 * eps) ** d
        text = (f"For points uniform in the unit hypercube [0, 1]<super>{d}</super>, the fraction of the volume lying "
                f"within distance {fmt(eps, 2)} of the boundary (i.e. outside the inner cube [{fmt(eps, 2)}, "
                f"{fmt(1 - eps, 2)}]<super>{d}</super>) is ______")
        sol = [f"Inner cube volume = (1 − 2ε)<super>d</super> = {fmt(1 - 2 * eps, 2)}<super>{d}</super> = "
               f"{fmt((1 - 2 * eps) ** d, 4)}.",
               f"Fraction near boundary = 1 − {fmt((1 - 2 * eps) ** d, 4)} = <b>{fmt(val, 2)}</b>. In high dimensions "
               f"most of the volume lies near the boundary."]
    else:
        m, d = [(5, 2), (5, 3), (5, 5), (5, 8), (10, 2), (10, 3), (10, 5), (20, 2), (20, 3), (20, 4)][
            int(rng.integers(0, 10))]
        val = m ** d
        text = (f"To keep the same sampling density as {m} points per axis in 1-D, the number of points needed in "
                f"d = {d} dimensions (a grid with {m} points per axis) is ______")
        sol = [f"A grid with {m} points per axis needs {m}<super>{d}</super> = <b>{val}</b> points — exponential "
               f"growth with d."]
        return Q(text=text + " " + nat_hint(0), qtype="NAT", marks=1, answer=(val, val), nat_hint=nat_hint(0),
                 solution=sol)
    return Q(text=text + " " + nat_hint(2), qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             solution=sol)


PCA_T = [
    ("PCA is an unsupervised, linear dimensionality-reduction technique.", "It uses no labels and linear projections."),
    ("The principal component directions are eigenvectors of the sample covariance matrix.", "Standard result."),
    ("The principal component directions are mutually orthogonal.", "Eigenvectors of a symmetric matrix."),
    ("The variance of the projected data along the j-th PC equals the j-th largest covariance eigenvalue.",
     "vᵀSv = λ for a unit eigenvector v."),
    ("The first PC is the unit direction that maximizes the variance of the projected data.",
     "Rayleigh quotient maximization."),
    ("Data are normally mean-centered before PCA.", "PCA describes variation about the mean."),
    ("When features are in different units, PCA is usually applied to standardized features (correlation matrix).",
     "Otherwise large-scale features dominate."),
    ("The proportion of variance explained by the first k PCs is (λ₁ + … + λ<sub>k</sub>)/(λ₁ + … + λ<sub>d</sub>).",
     "Eigenvalues are variances along PCs."),
    ("Scores on different principal components are uncorrelated.", "The covariance of the scores is diagonal."),
    ("Projecting onto the top-k PCs minimizes the mean squared reconstruction error over all k-dimensional linear "
     "subspaces (through the mean).", "Equivalent formulation of PCA."),
    ("For centered X = UΣVᵀ (samples as rows), the PC directions are the columns of V.", "XᵀX = VΣ²Vᵀ."),
    ("The sum of all eigenvalues of the covariance matrix equals the total variance (its trace).", "trace = Σλ."),
    ("LDA, unlike PCA, uses class labels to find discriminative directions.", "LDA is supervised."),
    ("A scree plot shows the eigenvalues (or variance explained) in decreasing order against component number.",
     "Used to choose the number of PCs."),
    ("The sample covariance matrix of n points has at most min(n − 1, d) non-zero eigenvalues.",
     "Centered data has rank ≤ n − 1."),
]
PCA_F = [
    ("PCA is a supervised method that uses class labels.", "PCA ignores labels."),
    ("The first PC is chosen to maximize class separation.", "That is LDA's goal; PCA maximizes variance."),
    ("Scores on different principal components are in general correlated.", "They are uncorrelated."),
    ("PCA results are unaffected by rescaling one of the features.", "Variances change, so PCs change."),
    ("The first PC is the eigenvector of the covariance matrix with the smallest eigenvalue.",
     "It has the largest eigenvalue."),
    ("A few linear principal components can unfold a nonlinear manifold such as a Swiss roll.",
     "PCA is linear; kernel PCA or manifold learning is needed."),
    ("For centered X = UΣVᵀ (samples as rows), the PC directions are the columns of U.",
     "They are columns of V; UΣ gives the scores."),
    ("Retaining all d principal components loses some of the variance.", "All d PCs retain 100% of the variance."),
    ("A covariance matrix can have negative eigenvalues.", "It is positive semi-definite."),
    ("PCA on the uncentered data matrix gives the same directions as PCA on centered data for every dataset.",
     "Without centering, the first direction tends to point towards the mean."),
    ("The projection on the first PC has the minimum variance among all unit directions.", "It has the maximum."),
    ("The proportion of variance explained by PC1 is λ₁/λ<sub>d</sub>.", "It is λ₁/Σλ."),
    ("The first PC is always the best single direction for classification.", "High variance ≠ discriminative."),
]


@template(TOPIC, SUB_PCA, marks=1, qtype="MSQ")
def pca_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, PCA_T, PCA_F)
    return Q(text="Which of the following statements about principal component analysis (PCA) is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


PCA2_T = [
    ("If centered X (n × d) has SVD X = UΣVᵀ, the eigenvalues of the sample covariance are σ<sub>j</sub>²/(n − 1).",
     "S = XᵀX/(n − 1) = VΣ²Vᵀ/(n − 1)."),
    ("The PC score matrix equals XV = UΣ.", "Multiply X = UΣVᵀ by V."),
    ("The mean squared reconstruction error (divisor n − 1) when keeping k PCs equals the sum of the discarded "
     "eigenvalues.", "The residual lies in the span of the discarded eigenvectors."),
    ("If two features are perfectly correlated, their 2 × 2 covariance matrix has a zero eigenvalue.",
     "The matrix is singular."),
    ("For a covariance matrix [[a, b], [b, a]] with b &gt; 0, PC1 is along (1, 1)/√2.", "Eigenvalue a + b."),
    ("PCA on standardized features is equivalent to eigen-decomposition of the correlation matrix.",
     "The covariance of z-scores is the correlation matrix."),
    ("In high dimensions, pairwise distances between random points concentrate, so nearest and farthest neighbours "
     "become similar in distance.", "A symptom of the curse of dimensionality."),
    ("To capture a fraction r of uniform data in a d-dimensional unit hypercube, a sub-cube needs edge length "
     "r<super>1/d</super>, which approaches 1 as d grows.", "Neighbourhoods stop being local."),
    ("With n samples and d ≥ n features, the centered data matrix has rank at most n − 1.",
     "Centering removes one degree of freedom."),
    ("Fisher LDA for C classes yields at most C − 1 discriminant directions.", "The between-class scatter has rank ≤ C − 1."),
    ("Kernel PCA can capture nonlinear structure by performing PCA in a feature space.", "Via the kernel trick."),
    ("Rotating the data by an orthogonal matrix rotates the PC directions but leaves the eigenvalues unchanged.",
     "S → RSRᵀ is a similarity transform."),
    ("Multiplying all features by the same non-zero constant c leaves the proportion of variance explained by each PC "
     "unchanged.", "All eigenvalues scale by c²."),
]
PCA2_F = [
    ("The eigenvalues of the sample covariance equal the singular values σ<sub>j</sub> of centered X.",
     "They are σ<sub>j</sub>²/(n − 1)."),
    ("Adding a constant to every value of one feature changes the principal components.",
     "Centering removes the shift."),
    ("If X = UΣVᵀ, the PC scores are given by VΣ.", "Scores are UΣ = XV."),
    ("PCA's first component always coincides with the LDA discriminant direction.",
     "PCA ignores labels; directions can even be orthogonal."),
    ("For a covariance matrix [[a, b], [b, a]] with b &gt; 0, PC1 is along (1, −1)/√2.",
     "(1, −1)/√2 has eigenvalue a − b, the smaller one."),
    ("Fisher LDA for C classes can give up to C + 1 discriminant directions.", "At most C − 1."),
    ("The reconstruction error when keeping k PCs equals the sum of the retained eigenvalues.",
     "It equals the sum of the discarded eigenvalues."),
    ("In high dimensions, most of the volume of a hypercube is concentrated near its centre.",
     "It concentrates near the boundary."),
    ("Multiplying all features by the same non-zero constant changes the proportion of variance explained by each PC.",
     "Every eigenvalue is scaled by c², so proportions are unchanged."),
    ("With a fixed number of samples, adding more irrelevant features always improves nearest-neighbour accuracy.",
     "Irrelevant dimensions dilute distances (curse of dimensionality)."),
    ("PCA always preserves the class separability present in the original feature space.",
     "Discarded low-variance directions may be the discriminative ones."),
    ("The sample covariance of n = 5 points in d = 10 dimensions can have 10 non-zero eigenvalues.",
     "Its rank is at most n − 1 = 4."),
]


@template(TOPIC, SUB_PCA, marks=2, qtype="MSQ")
def pca_concepts2(rng):
    opts, ans, expl = msq_from_statements(rng, PCA2_T, PCA2_F)
    return Q(text="Which of the following statements about PCA, SVD and dimensionality reduction is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, solution=expl)
