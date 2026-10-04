"""GATE DA mock-exam templates: Neural Networks (MLP / feed-forward).

Subtopics: perceptron, activation functions, forward pass, backpropagation,
parameter counting, expressiveness, training (loss, optimisation, regularisation),
softmax + cross-entropy.
"""
import math

import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch

from core import (Figure, Matrix, Q, Table, fmt, mcq, mcq_numeric, msq_from_statements, nat_hint,
                  nat_range, template, vec)

TOPIC = "Neural Networks (MLP / Feed-forward)"

S_PER = "Perceptron"
S_ACT = "Activation functions"
S_FWD = "Forward pass"
S_BP = "Backpropagation"
S_PAR = "Parameter counting"
S_EXP = "Expressiveness"
S_TRN = "Training & regularisation"
S_SMX = "Softmax + cross-entropy"

GRAY = ["#222222", "#666666", "#999999", "#bbbbbb"]


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def _softmax(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max())
    return e / e.sum()


def _pick(rng, seq):
    return seq[int(rng.integers(len(seq)))]


def _halfgrid(rng, lo=-2.0, hi=2.0, size=None, nonzero=True):
    vals = np.arange(lo, hi + 1e-9, 0.5)
    if nonzero:
        vals = vals[np.abs(vals) > 1e-9]
    return rng.choice(vals, size=size)


def _ints(rng, lo, hi, size=None, nonzero=False):
    vals = np.arange(lo, hi + 1)
    if nonzero:
        vals = vals[vals != 0]
    return rng.choice(vals, size=size)


def _nat_auto(val):
    """NAT answer/hint with 3 decimals, or 4 decimals for small magnitudes."""
    if abs(val) >= 0.1:
        return nat_range(val, 3, 0.002), nat_hint(3), 3
    return nat_range(val, 4, max(0.0002, 0.02 * abs(val))), nat_hint(4), 4


def _M(name, M, digits=2):
    """Matrix block whose name column is wide enough not to wrap."""
    return Matrix(name + "\u2007" * 3, M, digits)


def _p(x, d=4):
    """Number formatted with parentheses when negative."""
    return f"({fmt(x, d)})" if x < 0 else fmt(x, d)


def _sub(name, i):
    return f"{name}<sub>{i}</sub>"


def _draw_net(fig, layers, node_names, edge_labels=None, biases=None, layer_titles=None, t_edge=None,
              input_values=None):
    """Draw a feed-forward network.

    layers: list of layer sizes; node_names: list of lists (mathtext ok);
    edge_labels: dict {(l, i, j): str} for edge layer l node i -> layer l+1 node j (None: no labels);
    biases: dict {(l, j): str} drawn above node; t_edge: list of label positions per layer.
    """
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.axis("off")
    ax.set_aspect("equal")
    L = len(layers)
    dx, dy, r = 3.0, 1.8, 0.36
    pos = {}
    for l, n in enumerate(layers):
        for i in range(n):
            pos[(l, i)] = (l * dx, ((n - 1) / 2 - i) * dy)
    if t_edge is None:
        t_edge = [0.3] * (L - 1)
    for l in range(L - 1):
        for i in range(layers[l]):
            for j in range(layers[l + 1]):
                (x0, y0), (x1, y1) = pos[(l, i)], pos[(l + 1, j)]
                d = math.hypot(x1 - x0, y1 - y0)
                ux, uy = (x1 - x0) / d, (y1 - y0) / d
                ax.annotate("", xy=(x1 - ux * r, y1 - uy * r), xytext=(x0 + ux * r, y0 + uy * r),
                            arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8, mutation_scale=7))
                if edge_labels and (l, i, j) in edge_labels:
                    t = t_edge[l]
                    ax.text(x0 + t * (x1 - x0), y0 + t * (y1 - y0), edge_labels[(l, i, j)], fontsize=7,
                            ha="center", va="center", color="#000000",
                            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="#cccccc", lw=0.4))
    for (l, i), (x, y) in pos.items():
        fc = "#eeeeee" if l == 0 else ("#ffffff" if l < L - 1 else "#dddddd")
        ax.add_patch(Circle((x, y), r, fc=fc, ec="#222222", lw=1.0, zorder=3))
        ax.text(x, y, node_names[l][i], ha="center", va="center", fontsize=8, zorder=4)
        if biases and (l, i) in biases:
            ax.text(x, y + r + 0.2, biases[(l, i)], ha="center", va="bottom", fontsize=6.6, color="#000000")
        if input_values and l == 0 and i < len(input_values):
            ax.text(x - r - 0.15, y, input_values[i], ha="right", va="center", fontsize=7.2)
    ymax = max((n - 1) / 2 * dy for n in layers) + r + 0.6
    ymin = -ymax + 0.15
    if layer_titles:
        for l, ttl in enumerate(layer_titles):
            ax.text(l * dx, ymin - 0.1, ttl, ha="center", va="top", fontsize=6.8, color="#333333")
        ymin -= 0.55
    xmin = -r - (1.4 if input_values else 0.4)
    ax.set_xlim(xmin, (L - 1) * dx + r + 0.4)
    ax.set_ylim(ymin, ymax)


# truth tables over (x1,x2) in order 00, 01, 10, 11
INPUTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
TT_NAME = {
    (0, 0, 0, 1): "AND", (0, 1, 1, 1): "OR", (1, 1, 1, 0): "NAND", (1, 0, 0, 0): "NOR",
    (0, 1, 1, 0): "XOR", (1, 0, 0, 1): "XNOR", (0, 0, 1, 1): "x₁ (identity of x₁)",
    (0, 1, 0, 1): "x₂ (identity of x₂)", (1, 1, 0, 0): "NOT x₁", (1, 0, 1, 0): "NOT x₂",
    (0, 0, 1, 0): "x₁ AND (NOT x₂)", (0, 1, 0, 0): "(NOT x₁) AND x₂", (1, 0, 1, 1): "x₁ OR (NOT x₂)",
    (1, 1, 0, 1): "(NOT x₁) OR x₂",
}
GATE_TT = {"AND": (0, 0, 0, 1), "OR": (0, 1, 1, 1), "NAND": (1, 1, 1, 0), "NOR": (1, 0, 0, 0),
           "A AND NOT B": (0, 0, 1, 0), "NOT A AND B": (0, 1, 0, 0)}


def _tt(w1, w2, b):
    nets = [w1 * a + w2 * c + b for a, c in INPUTS]
    return tuple(int(n > 0) for n in nets), nets


def _sample_gate(rng, target, grid=(-3, 3), step=0.5, max_tries=5000):
    vals = np.arange(grid[0], grid[1] + 1e-9, step)
    for _ in range(max_tries):
        w1, w2, b = (float(v) for v in rng.choice(vals, 3))
        tt, nets = _tt(w1, w2, b)
        if tt == target and min(abs(n) for n in nets) >= 0.5 - 1e-9:
            return w1, w2, b
    raise RuntimeError("gate sampling failed")


# ============================================================================
# PERCEPTRON
# ============================================================================
@template(TOPIC, S_PER, marks=1, qtype="MSQ")
def perc_classify(rng):
    while True:
        w = _ints(rng, -3, 3, 2, nonzero=True)
        b = int(_ints(rng, -4, 4))
        pts = [tuple(int(v) for v in _ints(rng, -3, 3, 2)) for _ in range(4)]
        if len(set(pts)) < 4:
            continue
        nets = [w[0] * p[0] + w[1] * p[1] + b for p in pts]
        if any(n == 0 for n in nets):
            continue
        pos = [n > 0 for n in nets]
        if any(pos):
            break
    labels = "PQRS"
    opts = [f"Point {labels[i]} = ({fmt(p[0])}, {fmt(p[1])})" for i, p in enumerate(pts)]
    ans = [i for i in range(4) if pos[i]]

    def draw(fig):
        ax = fig.add_subplot(111)
        for i, p in enumerate(pts):
            ax.scatter([p[0]], [p[1]], color="#333333", s=22, zorder=3)
            ax.annotate(labels[i], p, textcoords="offset points", xytext=(5, 4), fontsize=8)
        ax.set_xlim(-3.6, 3.6)
        ax.set_ylim(-3.6, 3.6)
        ax.axhline(0, color="#aaaaaa", lw=0.6)
        ax.axvline(0, color="#aaaaaa", lw=0.6)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.set_xticks(range(-3, 4))
        ax.set_yticks(range(-3, 4))
        ax.grid(alpha=0.3)

    sol = [f"Net input a = w·x + b = {fmt(w[0])}x₁ + ({fmt(w[1])})x₂ + ({fmt(b)}); output +1 iff a ≥ 0."]
    for i, p in enumerate(pts):
        sol.append(f"({labels[i]}) a = {fmt(w[0])}·{fmt(p[0])} + ({fmt(w[1])})·{fmt(p[1])} + ({fmt(b)}) = "
                   f"{fmt(nets[i])} → {'+1 (selected)' if pos[i] else '−1'}.")
    sol.append("Answer: <b>" + ", ".join(f"({'ABCD'[i]})" for i in ans) + "</b>.")
    return Q(text=f"A perceptron with weights w = ({fmt(w[0])}, {fmt(w[1])}) and bias b = {fmt(b)} outputs "
                  f"ŷ = +1 if w·x + b ≥ 0 and ŷ = −1 otherwise. Which of the points shown below are "
                  f"classified as ŷ = +1?",
             qtype="MSQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 6.5, 5.0)], solution=sol)


@template(TOPIC, S_PER, marks=2, qtype="NAT")
def perc_update(rng):
    while True:
        n = 4
        X = _ints(rng, -3, 3, (n, 2))
        if len({tuple(r) for r in X}) < n or np.any(np.all(X == 0, axis=1)):
            continue
        y = rng.choice([-1, 1], n)
        if len(set(y)) < 2:
            continue
        eta = float(_pick(rng, [1.0, 0.5, 1.0, 2.0]))
        w = np.zeros(2)
        b = 0.0
        log = []
        nupd = 0
        for i in range(n):
            a = w @ X[i] + b
            mis = y[i] * a <= 0
            if mis:
                w = w + eta * y[i] * X[i]
                b = b + eta * y[i]
                nupd += 1
            log.append((i, a, mis, w.copy(), b))
        if nupd < 2:
            continue
        xt = _ints(rng, -3, 3, 2)
        break
    variant = int(rng.integers(5))
    if variant == 0:
        target, ask = w[0], "the weight w<sub>1</sub>"
    elif variant == 1:
        target, ask = w[1], "the weight w<sub>2</sub>"
    elif variant == 2:
        target, ask = b, "the bias b"
    elif variant == 3:
        target, ask = nupd, "the number of weight updates (mistakes) made in this epoch"
    else:
        target = w @ xt + b
        ask = f"the net input w·x + b for the test point x = ({fmt(xt[0])}, {fmt(xt[1])}) using the final parameters"
    rows = [["i", "x<sub>1</sub>", "x<sub>2</sub>", "y"]] + [[str(i + 1), fmt(X[i, 0]), fmt(X[i, 1]), fmt(y[i])]
                                                             for i in range(n)]

    def draw(fig):
        ax = fig.add_subplot(111)
        for i in range(n):
            mk = "s" if y[i] > 0 else "o"
            ax.scatter([X[i, 0]], [X[i, 1]], marker=mk, s=40, facecolor="#333333" if y[i] > 0 else "white",
                       edgecolor="#000000", zorder=3)
            ax.annotate(str(i + 1), (X[i, 0], X[i, 1]), textcoords="offset points", xytext=(5, 4), fontsize=8)
        ax.set_xlim(-3.6, 3.6)
        ax.set_ylim(-3.6, 3.6)
        ax.axhline(0, color="#aaaaaa", lw=0.6)
        ax.axvline(0, color="#aaaaaa", lw=0.6)
        ax.set_xlabel("x₁")
        ax.set_ylabel("x₂")
        ax.set_title("filled square: y = +1, open circle: y = −1", fontsize=7)
        ax.grid(alpha=0.3)

    sol = [f"Rule: if y<sub>i</sub>(w·x<sub>i</sub> + b) ≤ 0, then w ← w + η y<sub>i</sub> x<sub>i</sub>, "
           f"b ← b + η y<sub>i</sub> (η = {fmt(eta)}). Start w = (0, 0), b = 0."]
    for i, a, mis, wv, bv in log:
        sol.append(f"Example {i + 1}: a = {fmt(a)}, y·a = {fmt(y[i] * a)} → "
                   + (f"<b>mistake</b>, update → w = {vec(wv)}, b = {fmt(bv)}" if mis else "correct, no change") + ".")
    if variant == 4:
        sol.append(f"Test: w·x + b = {fmt(w[0])}·{fmt(xt[0])} + {fmt(w[1])}·{fmt(xt[1])} + {fmt(b)} = <b>{fmt(target)}</b>.")
    else:
        sol.append(f"Required value = <b>{fmt(target)}</b>.")
    sol.append("Note: a point with net input exactly 0 counts as a mistake (y·a ≤ 0) – this is why the first "
               "example always triggers an update when starting from zero.")
    return Q(text=f"A perceptron with parameters w ∈ ℝ², b is trained on the data below, starting from w = (0, 0), "
                  f"b = 0, with learning rate η = {fmt(eta)}. Examples are presented once in the order 1, 2, 3, 4 "
                  f"(one epoch). An update w ← w + η y x, b ← b + η y is made whenever y(w·x + b) ≤ 0. "
                  f"After the epoch, {ask} is ______ " + nat_hint(0),
             qtype="NAT", marks=2, answer=(float(target), float(target)), nat_hint=nat_hint(0),
             blocks=[Table(rows), Figure(draw, 6.5, 5.0)], solution=sol)


@template(TOPIC, S_PER, marks=2, qtype="MSQ")
def perc_gate(rng):
    gate = _pick(rng, ["AND", "OR", "NAND", "NOR"])
    target = GATE_TT[gate]
    n_true = int(rng.integers(1, 4))
    trues, falses = [], []
    vals = np.arange(-3, 3 + 1e-9, 0.5)
    tries = 0
    while len(trues) < n_true or len(falses) < 4 - n_true:
        tries += 1
        if len(trues) < n_true and tries % 3 == 0:
            cand = _sample_gate(rng, target)
        else:
            cand = tuple(float(v) for v in rng.choice(vals, 3))
        tt, nets = _tt(*cand)
        if min(abs(v) for v in nets) < 0.5 - 1e-9 or cand in trues or cand in falses:
            continue
        if tt == target and len(trues) < n_true:
            trues.append(cand)
        elif tt != target and len(falses) < 4 - n_true:
            # prefer plausible near-misses: a separable named gate or same sign pattern of b
            if tt in TT_NAME or rng.random() < 0.3:
                falses.append(cand)
    items = [(c, True) for c in trues] + [(c, False) for c in falses]
    perm = rng.permutation(4)
    items = [items[i] for i in perm]
    opts = [f"w<sub>1</sub> = {fmt(c[0])}, w<sub>2</sub> = {fmt(c[1])}, b = {fmt(c[2])}" for c, _ in items]
    ans = [i for i, (_, ok) in enumerate(items) if ok]
    sol = [f"Target {gate} truth table for (x<sub>1</sub>, x<sub>2</sub>) = (0,0), (0,1), (1,0), (1,1): "
           f"{', '.join(map(str, target))}. For each option compute a = w<sub>1</sub>x<sub>1</sub> + "
           f"w<sub>2</sub>x<sub>2</sub> + b at the four inputs and output 1 iff a &gt; 0."]
    for i, (c, ok) in enumerate(items):
        tt, nets = _tt(*c)
        nm = TT_NAME.get(tt, "constant " + str(tt[0]) if len(set(tt)) == 1 else "")
        sol.append(f"<b>({'ABCD'[i]}) {'TRUE' if ok else 'FALSE'}.</b> a = {', '.join(fmt(v) for v in nets)} → "
                   f"outputs {', '.join(map(str, tt))}" + (f" – {nm}" if nm else "") + ".")
    return Q(text=f"A threshold unit outputs 1 if w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + b &gt; 0 "
                  f"and 0 otherwise, for binary inputs x<sub>1</sub>, x<sub>2</sub> ∈ {{0, 1}}. Which of the "
                  f"following parameter settings make the unit implement the Boolean <b>{gate}</b> function?",
             qtype="MSQ", marks=2, options=opts, answer=ans, solution=sol)


PERC_T = [
    ("If the training data are linearly separable, the perceptron learning algorithm makes only a finite number "
     "of updates.", "Perceptron convergence theorem (Novikoff): at most (R/γ)² mistakes."),
    ("A single perceptron cannot represent the XOR function of two binary inputs.",
     "The positive points (0,1),(1,0) and negative points (0,0),(1,1) are not linearly separable."),
    ("The decision boundary of a perceptron, w·x + b = 0, is a hyperplane.", "It is an affine set of dimension d−1."),
    ("The weight vector w is normal (perpendicular) to the perceptron's decision boundary.",
     "For any two points on the boundary, w·(x−x′) = 0."),
    ("In the perceptron learning rule (labels ±1), the weights change only on misclassified examples.",
     "Update w ← w + ηyx is applied only when y(w·x+b) ≤ 0."),
    ("The perceptron mistake bound (R/γ)² does not depend explicitly on the input dimension d.",
     "It depends only on the radius R of the data and the margin γ."),
    ("The perceptron mistake bound (R/γ)² does not depend on the number of training examples.",
     "Only R and γ appear in the bound."),
    ("A single perceptron can implement AND, OR and NAND on binary inputs.",
     "All three are linearly separable, e.g. AND: w = (1,1), b = −1.5."),
    ("For separable data, the separating hyperplane found by the perceptron can depend on the order in which "
     "examples are presented.", "Different orders lead to different update sequences and final weights."),
    ("When the data are not linearly separable, the basic perceptron algorithm does not settle on a fixed "
     "weight vector.", "Some example is always misclassified, so updates never stop."),
    ("XOR becomes linearly separable if the product feature x₁x₂ is added as an extra input.",
     "XOR = x₁ + x₂ − 2x₁x₂ is linear in (x₁, x₂, x₁x₂)."),
    ("Starting from w = 0, b = 0, scaling the learning rate η by a positive constant does not change the "
     "sequence of predictions made by the perceptron.", "All weights (and bias) are simply scaled by the constant."),
    ("The perceptron is not trained by gradient descent on the 0–1 loss, because that loss has zero gradient "
     "almost everywhere.", "The 0–1 loss is piecewise constant in w."),
    ("A two-layer network of threshold units can compute XOR.", "E.g. XOR = AND(OR(x₁,x₂), NAND(x₁,x₂))."),
    ("Each mistake of the perceptron increases w·w* by at least γ, where w* is a unit-norm separator with "
     "margin γ (η = 1).", "Key step of the convergence proof: w·w* grows linearly in the number of mistakes."),
]
PERC_F = [
    ("A single perceptron can represent XOR if the learning rate is chosen small enough.",
     "No choice of η helps: XOR is not linearly separable."),
    ("The perceptron algorithm converges for every training set, separable or not.",
     "Convergence is guaranteed only for linearly separable data."),
    ("The perceptron always finds the maximum-margin separating hyperplane.",
     "It stops at any separating hyperplane; max margin is the SVM objective."),
    ("The perceptron update rule changes the weights even on correctly classified examples.",
     "Correctly classified points (y·a &gt; 0) cause no update."),
    ("The perceptron mistake bound grows linearly with the input dimension d.",
     "The bound (R/γ)² has no explicit dependence on d."),
    ("A single perceptron can implement XNOR on binary inputs.", "XNOR, like XOR, is not linearly separable."),
    ("The perceptron learning rule is gradient descent on the squared error of a sigmoid output.",
     "That is the delta rule / logistic-type training, not the perceptron rule."),
    ("Multiplying all input vectors by 10 can make a non-separable dataset linearly separable.",
     "Uniform scaling preserves (non-)separability."),
    ("A perceptron with a bias term can only realise decision boundaries passing through the origin.",
     "The bias b shifts the hyperplane away from the origin."),
    ("A two-layer network of threshold units cannot represent XOR.", "Two hidden threshold units suffice."),
    ("For linearly separable data the perceptron converges in at most d + 1 updates (d = input dimension).",
     "The bound is (R/γ)², which can be much larger than d + 1."),
    ("If a perceptron classifies all training points correctly, its weight vector is unique.",
     "Any positive scaling (and many other vectors) also separates the data."),
    ("The output of a perceptron is a calibrated probability of the positive class.",
     "It outputs a hard ±1 (or 0/1) decision."),
    ("The perceptron mistake bound becomes smaller when the margin γ decreases.",
     "(R/γ)² grows as γ shrinks."),
]


@template(TOPIC, S_PER, marks=1, qtype="MSQ")
def perc_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, PERC_T, PERC_F)
    return Q(text="Which of the following statements about the perceptron is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_PER, marks=2, qtype="NAT")
def perc_bound(rng):
    dirs = [(3, 4), (4, 3), (1, 0), (0, 1), (-3, 4), (4, -3), (1, 1), (1, -1)]
    while True:
        uraw = np.array(_pick(rng, dirs), dtype=float)
        u = uraw / np.linalg.norm(uraw)
        X = _ints(rng, -4, 4, (5, 2))
        if len({tuple(r) for r in X}) < 5:
            continue
        m = X @ u
        if np.min(np.abs(m)) < 0.4:
            continue
        y = np.sign(m)
        if len(set(y)) < 2:
            continue
        gam = float(np.min(y * m))
        R = float(np.max(np.linalg.norm(X, axis=1)))
        bound = (R / gam) ** 2
        if bound > 400:
            continue
        break
    nrm = np.linalg.norm(uraw)
    if abs(nrm - 1) < 1e-9:
        ustr = f"({fmt(uraw[0])}, {fmt(uraw[1])})"
    elif abs(nrm - math.sqrt(2)) < 1e-9:
        ustr = f"({fmt(uraw[0])}, {fmt(uraw[1])})/√2"
    else:
        ustr = f"({fmt(uraw[0])}, {fmt(uraw[1])})/{fmt(nrm)}"
    rows = [["i"] + [str(i + 1) for i in range(5)],
            ["x<sub>i</sub>"] + [f"({fmt(r[0])}, {fmt(r[1])})" for r in X],
            ["y<sub>i</sub>"] + [fmt(v) for v in y]]
    sol = [f"Unit separator u = {ustr}. Margins y<sub>i</sub>(u·x<sub>i</sub>): "
           + ", ".join(fmt(v, 3) for v in y * m) + f" → γ = min = {fmt(gam, 4)}.",
           "Norms ‖x<sub>i</sub>‖: " + ", ".join(fmt(v, 3) for v in np.linalg.norm(X, axis=1))
           + f" → R = max = {fmt(R, 4)}.",
           f"Novikoff bound: number of mistakes ≤ (R/γ)² = ({fmt(R, 4)}/{fmt(gam, 4)})² = <b>{fmt(bound, 2)}</b>.",
           "Common mistakes: forgetting to normalise u (γ must be measured with ‖u‖ = 1), or using R/γ without "
           "squaring."]
    return Q(text=f"The labelled data below are linearly separable through the origin by the unit vector "
                  f"u = {ustr} (i.e. y<sub>i</sub> = sign(u·x<sub>i</sub>)). Take γ = min<sub>i</sub> "
                  f"y<sub>i</sub>(u·x<sub>i</sub>) and R = max<sub>i</sub> ‖x<sub>i</sub>‖. The perceptron "
                  f"convergence theorem (no bias, w<sub>0</sub> = 0, η = 1) bounds the number of mistakes by "
                  f"(R/γ)². The value of this bound is ______ " + nat_hint(2),
             qtype="NAT", marks=2, answer=nat_range(bound, 2, max(0.01, 0.002 * bound)), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False)], solution=sol)


@template(TOPIC, S_PER, marks=1, qtype="MCQ")
def perc_xor_panels(rng):
    sep = [k for k in TT_NAME if k not in ((0, 1, 1, 0), (1, 0, 0, 1))]
    bad = _pick(rng, [(0, 1, 1, 0), (1, 0, 0, 1)])
    idx = rng.choice(len(sep), 3, replace=False)
    funcs = [sep[i] for i in idx] + [bad]
    perm = rng.permutation(4)
    funcs = [funcs[i] for i in perm]
    names = "PQRS"
    k = funcs.index(bad)
    opts = [f"Dataset {names[i]}" for i in range(4)]

    def draw(fig):
        for p in range(4):
            ax = fig.add_subplot(1, 4, p + 1)
            for (a, c), v in zip(INPUTS, funcs[p]):
                ax.scatter([a], [c], marker="s" if v else "o", s=55, facecolor="#222222" if v else "white",
                           edgecolor="#000000", zorder=3)
            ax.set_xlim(-0.5, 1.5)
            ax.set_ylim(-0.5, 1.5)
            ax.set_xticks([0, 1])
            ax.set_yticks([0, 1])
            ax.set_aspect("equal")
            ax.set_title(names[p], fontsize=9)
            ax.set_xlabel("x₁", fontsize=7)
            if p == 0:
                ax.set_ylabel("x₂", fontsize=7)

    sol = ["A single perceptron can classify a dataset perfectly iff the two classes are linearly separable."]
    for p in range(4):
        sol.append(f"Dataset {names[p]}: labels for (0,0),(0,1),(1,0),(1,1) = {', '.join(map(str, funcs[p]))} → "
                   f"{TT_NAME[funcs[p]]} – " + ("<b>not</b> linearly separable (diagonal pattern)."
                                                if p == k else "linearly separable."))
    sol.append(f"Answer: <b>Dataset {names[k]}</b>. Of the 14 non-constant Boolean functions of two inputs, only "
               "XOR and XNOR are not linearly separable.")
    return Q(text="Each panel shows the four binary inputs (x<sub>1</sub>, x<sub>2</sub>) labelled as class 1 "
                  "(filled square) or class 0 (open circle). Which dataset can NOT be classified perfectly by a "
                  "single perceptron (one linear threshold unit)?",
             qtype="MCQ", marks=1, options=opts, answer=k, blocks=[Figure(draw, 12, 3.6)], solution=sol)


# ============================================================================
# ACTIVATION FUNCTIONS
# ============================================================================
@template(TOPIC, S_ACT, marks=1, qtype="NAT")
def act_values(rng):
    z = float(_halfgrid(rng, -3, 3))
    v = int(rng.integers(6))
    s = _sig(z)
    if v == 0:
        val = s
        q = f"σ(z) = 1/(1 + e<super>−z</super>) at z = {fmt(z)}"
        sol = [f"σ({fmt(z)}) = 1/(1 + e<super>{fmt(-z)}</super>) = 1/(1 + {fmt(math.exp(-z), 4)}) = <b>{fmt(val, 4)}</b>."]
    elif v == 1:
        val = s * (1 - s)
        q = f"the derivative σ′(z) of the logistic sigmoid at z = {fmt(z)}"
        sol = [f"σ({fmt(z)}) = {fmt(s, 4)}; σ′(z) = σ(z)(1 − σ(z)) = {fmt(s, 4)} × {fmt(1 - s, 4)} = <b>{fmt(val, 4)}</b>.",
               "Note σ′ ≤ 0.25, with equality only at z = 0."]
    elif v == 2:
        val = math.tanh(z)
        q = f"tanh(z) at z = {fmt(z)}"
        sol = [f"tanh(z) = (e<super>z</super> − e<super>−z</super>)/(e<super>z</super> + e<super>−z</super>) = "
               f"<b>{fmt(val, 4)}</b> (equivalently 2σ(2z) − 1)."]
    elif v == 3:
        t = math.tanh(z)
        val = 1 - t * t
        q = f"the derivative of tanh(z) at z = {fmt(z)}"
        sol = [f"tanh({fmt(z)}) = {fmt(t, 4)}; d/dz tanh(z) = 1 − tanh²(z) = 1 − {fmt(t * t, 4)} = <b>{fmt(val, 4)}</b>."]
    elif v == 4:
        alpha = float(_pick(rng, [0.01, 0.1, 0.2, 0.05]))
        z1 = float(_halfgrid(rng, -4, -0.5))
        z2 = float(_halfgrid(rng, 0.5, 3))
        val = alpha * z1 + z2 + max(0.0, z1)
        q = (f"LeakyReLU<sub>α</sub>(z<sub>1</sub>) + LeakyReLU<sub>α</sub>(z<sub>2</sub>) + ReLU(z<sub>1</sub>) with "
             f"α = {fmt(alpha)}, z<sub>1</sub> = {fmt(z1)}, z<sub>2</sub> = {fmt(z2)} (LeakyReLU<sub>α</sub>(z) = z for "
             f"z ≥ 0 and αz for z &lt; 0)")
        sol = [f"LeakyReLU({fmt(z1)}) = {fmt(alpha)}×{fmt(z1)} = {fmt(alpha * z1, 4)}; LeakyReLU({fmt(z2)}) = {fmt(z2)}; "
               f"ReLU({fmt(z1)}) = 0. Sum = <b>{fmt(val, 4)}</b>."]
    else:
        val = math.log1p(math.exp(z))
        q = f"the softplus function ln(1 + e<super>z</super>) at z = {fmt(z)}"
        sol = [f"ln(1 + e<super>{fmt(z)}</super>) = ln(1 + {fmt(math.exp(z), 4)}) = <b>{fmt(val, 4)}</b>. "
               f"(Its derivative is σ(z) = {fmt(s, 4)}.)"]
    ans, hint, _ = _nat_auto(val)
    return Q(text=f"The value of {q} is ______ " + hint,
             qtype="NAT", marks=1, answer=ans, nat_hint=hint, solution=sol)


@template(TOPIC, S_ACT, marks=2, qtype="NAT")
def act_chain(rng):
    act = _pick(rng, ["σ", "σ", "tanh"])
    f = _sig if act == "σ" else np.tanh
    fp = (lambda a: _sig(a) * (1 - _sig(a))) if act == "σ" else (lambda a: 1 - np.tanh(a) ** 2)
    while True:
        w = _ints(rng, -3, 3, 3, nonzero=True).astype(float)
        bb = _halfgrid(rng, -1, 1, 3, nonzero=False).astype(float)
        x = float(_halfgrid(rng, -1, 1))
        a1 = w[0] * x + bb[0]
        h1 = f(a1)
        a2 = w[1] * h1 + bb[1]
        h2 = f(a2)
        a3 = w[2] * h2 + bb[2]
        yv = f(a3)
        d1, d2, d3 = fp(a1), fp(a2), fp(a3)
        variant = int(rng.integers(2))
        dydx = d3 * w[2] * d2 * w[1] * d1 * w[0]
        val = dydx if variant == 0 else d3 * w[2] * d2 * w[1] * d1 * x
        if abs(val) > 0.003:
            break
    ask = "∂y/∂x" if variant == 0 else "∂y/∂w<sub>1</sub>"

    def draw(fig):
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("off")
        ax.set_xlim(0, 10.6)
        ax.set_ylim(0, 1.6)
        labels = ["x", f"h₁ = {act}(w₁x + b₁)", f"h₂ = {act}(w₂h₁ + b₂)", f"y = {act}(w₃h₂ + b₃)"]
        xs = [0.5, 3.0, 5.9, 8.8]
        widths = [0.7, 2.3, 2.5, 2.4]
        for xc, wd, lb in zip(xs, widths, labels):
            ax.add_patch(FancyBboxPatch((xc - wd / 2, 0.5), wd, 0.6, boxstyle="round,pad=0.05", fc="#f2f2f2",
                                        ec="#222222", lw=0.8))
            ax.text(xc, 0.8, lb, ha="center", va="center", fontsize=7.5)
        for k in range(3):
            x0 = xs[k] + widths[k] / 2 + 0.05
            x1 = xs[k + 1] - widths[k + 1] / 2 - 0.05
            ax.annotate("", xy=(x1, 0.8), xytext=(x0, 0.8), arrowprops=dict(arrowstyle="-|>", color="#444444", lw=0.9))

    sol = [f"Forward: a₁ = {fmt(w[0])}·{fmt(x)} + {fmt(bb[0])} = {fmt(a1, 4)}, h₁ = {fmt(h1, 4)}; "
           f"a₂ = {fmt(w[1])}·{fmt(h1, 4)} + {fmt(bb[1])} = {fmt(a2, 4)}, h₂ = {fmt(h2, 4)}; "
           f"a₃ = {fmt(w[2])}·{fmt(h2, 4)} + {fmt(bb[2])} = {fmt(a3, 4)}, y = {fmt(yv, 4)}.",
           f"Local derivatives {act}′(a): " + (
               "σ′(a) = σ(a)(1 − σ(a))" if act == "σ" else "tanh′(a) = 1 − tanh²(a)")
           + f": {act}′(a₁) = {fmt(d1, 4)}, {act}′(a₂) = {fmt(d2, 4)}, {act}′(a₃) = {fmt(d3, 4)}.",
           ("Chain rule: ∂y/∂x = " + f"{act}′(a₃)·w₃·{act}′(a₂)·w₂·{act}′(a₁)·w₁"
            if variant == 0 else "Chain rule: ∂y/∂w₁ = " + f"{act}′(a₃)·w₃·{act}′(a₂)·w₂·{act}′(a₁)·x")
           + f" = <b>{fmt(val, 4)}</b>.",
           "Each layer contributes a factor " + (
               "σ′ ≤ 0.25" if act == "σ" else "tanh′ ≤ 1") + " – the product shrinks with depth (vanishing gradient)."]
    return Q(text=f"Consider the scalar chain shown below with weights w₁ = {fmt(w[0])}, w₂ = {fmt(w[1])}, "
                  f"w₃ = {fmt(w[2])}, biases b₁ = {fmt(bb[0])}, b₂ = {fmt(bb[1])}, b₃ = {fmt(bb[2])} and activation "
                  f"{'the logistic sigmoid σ' if act == 'σ' else 'tanh'} at every stage. For input x = {fmt(x)}, the "
                  f"value of {ask} is ______ " + nat_hint(4),
             qtype="NAT", marks=2, answer=nat_range(val, 4, max(0.0003, 0.01 * abs(val))), nat_hint=nat_hint(4),
             blocks=[Figure(draw, 13, 2.2)], solution=sol)


ACT_FUNCS = {
    "Sigmoid σ(z) = 1/(1+e<super>−z</super>)": (lambda z: _sig(z)),
    "tanh(z)": (lambda z: np.tanh(z)),
    "ReLU: max(0, z)": (lambda z: np.maximum(0, z)),
    "Leaky ReLU with α = 0.1": (lambda z: np.where(z > 0, z, 0.1 * z)),
    "ELU with α = 1": (lambda z: np.where(z > 0, z, np.exp(z) - 1)),
    "Softplus: ln(1 + e<super>z</super>)": (lambda z: np.log1p(np.exp(z))),
    "σ′(z) = σ(z)(1 − σ(z))": (lambda z: _sig(z) * (1 - _sig(z))),
    "1 − tanh²(z)": (lambda z: 1 - np.tanh(z) ** 2),
}
ACT_NOTES = {
    "Sigmoid σ(z) = 1/(1+e<super>−z</super>)": "S-shaped, range (0, 1), value 0.5 at z = 0.",
    "tanh(z)": "S-shaped, range (−1, 1), passes through the origin.",
    "ReLU: max(0, z)": "Exactly 0 for z ≤ 0, slope 1 for z &gt; 0, kink at origin.",
    "Leaky ReLU with α = 0.1": "Small negative linear part (slope 0.1) for z &lt; 0, slope 1 for z &gt; 0.",
    "ELU with α = 1": "Smoothly saturates to −1 for z → −∞, linear for z &gt; 0, passes through origin.",
    "Softplus: ln(1 + e<super>z</super>)": "Smooth, always positive, value ln 2 ≈ 0.69 at z = 0, ~z for large z.",
    "σ′(z) = σ(z)(1 − σ(z))": "Bell-shaped with peak 0.25 at z = 0.",
    "1 − tanh²(z)": "Bell-shaped with peak 1 at z = 0.",
}


@template(TOPIC, S_ACT, marks=1, qtype="MCQ")
def act_identify(rng):
    keys = list(ACT_FUNCS)
    correct = _pick(rng, keys)
    f = ACT_FUNCS[correct]
    confusers = {
        keys[0]: [keys[1], keys[5], keys[6], keys[7]], keys[1]: [keys[0], keys[4], keys[7]],
        keys[2]: [keys[3], keys[4], keys[5]], keys[3]: [keys[2], keys[4], keys[5]],
        keys[4]: [keys[2], keys[3], keys[5], keys[1]], keys[5]: [keys[2], keys[4], keys[0]],
        keys[6]: [keys[7], keys[0], keys[1]], keys[7]: [keys[6], keys[0], keys[1]],
    }[correct]
    opts, a = mcq(rng, correct, confusers)
    zz = np.linspace(-4, 4, 400)

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(zz, f(zz), color="#111111", lw=1.6)
        ax.axhline(0, color="#999999", lw=0.6)
        ax.axvline(0, color="#999999", lw=0.6)
        ax.set_xlabel("z")
        ax.set_ylabel("g(z)")
        ax.grid(alpha=0.3)
        ax.set_xticks(range(-4, 5))

    sol = [f"Key features of the plotted curve: {ACT_NOTES[correct]}",
           f"Hence g = <b>{correct}</b>."]
    for o in opts:
        if o != correct:
            sol.append(f"{o}: {ACT_NOTES[o]} – does not match.")
    return Q(text="The figure shows the graph of a function g(z) used in neural networks. Which function is it?",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 7.5, 4.6)], solution=sol)


ACT_T = [
    ("σ′(z) = σ(z)(1 − σ(z)), whose maximum value is 0.25 (at z = 0).", "σ(1−σ) is maximised at σ = 1/2."),
    ("tanh(z) = 2σ(2z) − 1.", "Standard identity relating tanh and the logistic sigmoid."),
    ("The derivative of tanh(z) has maximum value 1, attained at z = 0.", "tanh′ = 1 − tanh², and tanh(0) = 0."),
    ("The output of ReLU lies in [0, ∞).", "max(0, z) is never negative and is unbounded above."),
    ("tanh outputs lie in (−1, 1) and are zero-centred.", "tanh is odd and bounded by ±1."),
    ("Sigmoid units saturate for large |z|, giving near-zero gradients.",
     "σ′(z) → 0 as |z| → ∞; a cause of vanishing gradients."),
    ("Leaky ReLU has a non-zero gradient for z &lt; 0, which helps avoid 'dead' units.",
     "Its gradient is α &gt; 0 for negative inputs."),
    ("Softmax outputs are strictly positive and sum to 1.", "exp(·) &gt; 0 and the outputs are normalised."),
    ("softmax(z + c·1) = softmax(z) for any real constant c.", "The factor e<super>c</super> cancels."),
    ("For two classes, the softmax probability of class 1 equals σ(z₁ − z₂).",
     "e<super>z₁</super>/(e<super>z₁</super>+e<super>z₂</super>) = 1/(1+e<super>−(z₁−z₂)</super>)."),
    ("In a deep network of sigmoid units, the backpropagated gradient contains a product of σ′ factors, each at "
     "most 0.25, which can shrink exponentially with depth.", "This is the vanishing-gradient problem."),
    ("ReLU is not differentiable at z = 0; in practice a subgradient value (0 or 1) is used there.",
     "Left and right derivatives are 0 and 1."),
    ("The derivative of the softplus ln(1 + e<super>z</super>) is σ(z).",
     "d/dz ln(1+e<super>z</super>) = e<super>z</super>/(1+e<super>z</super>)."),
    ("Sigmoid outputs are always positive, so they are not zero-centred.", "σ(z) ∈ (0, 1)."),
    ("Dividing the logits by a temperature T &gt; 1 makes the softmax distribution more uniform.",
     "Differences between logits shrink."),
    ("σ(−z) = 1 − σ(z).", "1/(1+e<super>z</super>) = e<super>−z</super>/(1+e<super>−z</super>)."),
    ("For z &gt; 0 the derivative of ReLU equals 1, so ReLU does not saturate for positive inputs.",
     "Gradient passes unchanged through active ReLUs."),
]
ACT_F = [
    ("The maximum value of σ′(z) for the logistic sigmoid is 0.5.", "The maximum is 0.25 at z = 0."),
    ("tanh outputs lie in the interval (0, 1).", "tanh ranges over (−1, 1)."),
    ("ReLU suffers from vanishing gradients for large positive inputs.", "Its gradient is exactly 1 for z &gt; 0."),
    ("For z &gt; 0, the derivative of ReLU(z) equals z.", "The derivative is 1, the value is z."),
    ("Softmax is invariant to multiplying all logits by the same positive constant.",
     "Scaling changes the sharpness (temperature); only additive shifts leave it unchanged."),
    ("The logistic sigmoid is zero-centred.", "σ(0) = 0.5 and all outputs are positive."),
    ("σ(−z) = −σ(z) for the logistic sigmoid.", "Correct identity: σ(−z) = 1 − σ(z)."),
    ("d/dz tanh(z) = 1 + tanh²(z).", "It is 1 − tanh²(z)."),
    ("The output range of Leaky ReLU is [0, ∞).", "Negative inputs give negative outputs αz."),
    ("Softmax assigns the largest probability to the smallest logit.", "It is monotone increasing in each logit."),
    ("Replacing sigmoid by tanh in the hidden layers completely removes the vanishing-gradient problem.",
     "tanh also saturates; it only helps (zero-centred, larger max slope)."),
    ("The derivative of the sigmoid is largest for large |z|.", "It is largest at z = 0 and decays for large |z|."),
    ("As the temperature T → 0⁺, softmax(z/T) approaches the uniform distribution.",
     "It approaches a one-hot vector at argmax z (uniform is the T → ∞ limit)."),
    ("σ(0) = 0 for the logistic sigmoid.", "σ(0) = 1/2."),
    ("ReLU is a bounded function.", "It is unbounded above."),
    ("tanh(z) = σ(z) − 0.5 for all z.", "The correct identity is tanh(z) = 2σ(2z) − 1."),
]


@template(TOPIC, S_ACT, marks=1, qtype="MSQ")
def act_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, ACT_T, ACT_F)
    return Q(text="Which of the following statements about activation functions is/are CORRECT? "
                  "(σ denotes the logistic sigmoid.)",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_ACT, marks=2, qtype="MSQ")
def act_compare_msq(rng):
    """Numeric MSQ: comparisons of activation values/derivatives at a random z."""
    z = float(_halfgrid(rng, -2.5, 2.5))
    s = _sig(z)
    t = math.tanh(z)
    cands = []
    # (statement, truth, explanation)
    v1 = s * (1 - s)
    v2 = 1 - t * t
    cands.append((f"σ′({fmt(z)}) &gt; tanh′({fmt(z)})", v1 > v2, f"σ′ = {fmt(v1, 4)}, tanh′ = {fmt(v2, 4)}."))
    cands.append((f"tanh({fmt(z)}) = 2σ({fmt(2 * z)}) − 1", True, f"Both equal {fmt(t, 4)}."))
    cands.append((f"σ({fmt(z)}) + σ({fmt(-z)}) = 1", True, "σ(−z) = 1 − σ(z)."))
    cands.append((f"σ′({fmt(z)}) = σ′({fmt(-z)})", True, "σ′ is an even function."))
    cands.append((f"tanh({fmt(z)}) + tanh({fmt(-z)}) = 1", False, "tanh is odd: the sum is 0."))
    cands.append((f"σ′({fmt(z)}) ≥ 0.25", False, f"σ′({fmt(z)}) = {fmt(v1, 4)} &lt; 0.25 (max only at 0)."))
    cands.append((f"ReLU′({fmt(z)}) = {'1' if z > 0 else '0'}", True, "ReLU′ = 1 for z &gt; 0 and 0 for z &lt; 0."))
    cands.append((f"ReLU′({fmt(z)}) = {'0' if z > 0 else '1'}", False, "ReLU′ = 1 for z &gt; 0 and 0 for z &lt; 0."))
    sp = math.log1p(math.exp(z))
    cands.append((f"softplus({fmt(z)}) &gt; ReLU({fmt(z)})", True,
                  f"softplus = {fmt(sp, 4)} &gt; {fmt(max(0, z))}; ln(1+e<super>z</super>) &gt; max(0, z) always."))
    cands.append((f"|tanh({fmt(z)})| &gt; |{fmt(z)}|", False, "|tanh z| &lt; |z| for z ≠ 0."))
    cands.append((f"σ({fmt(z)}) &gt; 0.5", z > 0, f"σ({fmt(z)}) = {fmt(s, 4)}."))
    cands.append((f"tanh′({fmt(z)}) = 1 − tanh²({fmt(z)}) = {fmt(v2, 3)}", True, f"tanh = {fmt(t, 4)}."))
    cands.append((f"σ′({fmt(z)}) = σ({fmt(z)})² = {fmt(s * s, 3)}", False, f"σ′ = σ(1−σ) = {fmt(v1, 4)}."))
    tr = [c for c in cands if c[1]]
    fl = [c for c in cands if not c[1]]
    opts, ans, expl = msq_from_statements(rng, [(c[0], c[2]) for c in tr], [(c[0], c[2]) for c in fl])
    return Q(text=f"Let σ be the logistic sigmoid, and ′ denote the derivative. At z = {fmt(z)} "
                  f"(and −z = {fmt(-z)}), which of the following is/are CORRECT? (softplus(z) = ln(1 + e<super>z</super>).)",
             qtype="MSQ", marks=2, options=opts, answer=ans,
             solution=[f"σ({fmt(z)}) = {fmt(s, 4)}, tanh({fmt(z)}) = {fmt(t, 4)}."] + expl)


@template(TOPIC, S_ACT, marks=1, qtype="NAT")
def softmax_prob(rng):
    K = int(rng.integers(3, 5))
    while True:
        z = _halfgrid(rng, -2, 3, K, nonzero=False).astype(float)
        if len(set(z)) == K:
            break
    k = int(rng.integers(K))
    v = int(rng.integers(3))
    T = 1.0
    if v == 1:
        T = float(_pick(rng, [2.0, 0.5]))
    zz = z / T
    p = _softmax(zz)
    zs = ", ".join(fmt(x) for x in z)
    if v == 2:
        c = float(_pick(rng, [10, -5, 100, 3]))
        txt = (f"A network produces logits z = ({zs}). A constant {fmt(c)} is added to every logit. The softmax "
               f"probability of class {k + 1} computed from the shifted logits is ______ ")
    elif v == 1:
        txt = (f"For logits z = ({zs}), the temperature-scaled softmax p<sub>k</sub> = exp(z<sub>k</sub>/T)/Σ<sub>j</sub>"
               f" exp(z<sub>j</sub>/T) with T = {fmt(T)} gives p<sub>{k + 1}</sub> = ______ ")
    else:
        txt = (f"For logits z = ({zs}), the softmax probability p<sub>{k + 1}</sub> = exp(z<sub>{k + 1}</sub>)/"
               f"Σ<sub>j</sub> exp(z<sub>j</sub>) is ______ ")
    ex = np.exp(zz)
    sol = [("Adding a constant to all logits does not change softmax (e<super>c</super> cancels). " if v == 2 else "")
           + ("Scaled logits z/T = (" + ", ".join(fmt(x, 3) for x in zz) + "). " if v == 1 else ""),
           "exp values: " + ", ".join(fmt(x, 4) for x in ex) + f"; sum = {fmt(ex.sum(), 4)}.",
           f"p<sub>{k + 1}</sub> = {fmt(ex[k], 4)}/{fmt(ex.sum(), 4)} = <b>{fmt(p[k], 4)}</b>."]
    return Q(text=txt + _nat_auto(p[k])[1], qtype="NAT", marks=1, answer=_nat_auto(p[k])[0],
             nat_hint=_nat_auto(p[k])[1], solution=sol)


# ============================================================================
# FORWARD PASS
# ============================================================================
def _act_fn(name):
    return {"ReLU": lambda a: np.maximum(0, a), "sigmoid": _sig, "tanh": np.tanh}[name]


@template(TOPIC, S_FWD, marks=2, qtype="NAT")
def fwd_221(rng):
    act = _pick(rng, ["ReLU", "sigmoid", "tanh", "ReLU"])
    out = _pick(rng, ["linear", "sigmoid"])
    f = _act_fn(act)
    while True:
        x = _halfgrid(rng, -2, 2, 2).astype(float)
        W = _halfgrid(rng, -2, 2, (2, 2)).astype(float)
        b = _halfgrid(rng, -1, 1, 2, nonzero=False).astype(float)
        v = _halfgrid(rng, -2, 2, 2).astype(float)
        c = float(_halfgrid(rng, -1, 1, nonzero=False))
        a = W @ x + b
        if np.any(np.abs(a) < 0.25):
            continue
        if act == "ReLU" and not np.any(a > 0):
            continue
        h = f(a)
        o = v @ h + c
        yv = o if out == "linear" else _sig(o)
        if abs(o) < 0.05:
            continue
        break
    ask_h = rng.random() < 0.2
    j = int(rng.integers(2))
    val = h[j] if ask_h else yv
    names = [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$"], ["$\\hat{y}$"]]
    el = {(0, i, jj): fmt(W[jj, i]) for i in range(2) for jj in range(2)}
    el.update({(1, i, 0): fmt(v[i]) for i in range(2)})
    bias = {(1, 0): f"b={fmt(b[0])}", (1, 1): f"b={fmt(b[1])}", (2, 0): f"b={fmt(c)}"}

    def draw(fig):
        _draw_net(fig, [2, 2, 1], names, el, bias, ["input", f"hidden ({act})", f"output ({out})"],
                  t_edge=[0.3, 0.45], input_values=[f"{fmt(x[0])}", f"{fmt(x[1])}"])

    actdesc = {"ReLU": "ReLU(a) = max(0, a)", "sigmoid": "σ(a) = 1/(1+e<super>−a</super>)", "tanh": "tanh(a)"}[act]
    sol = [f"Hidden pre-activations: a<sub>1</sub> = {fmt(W[0, 0])}·{fmt(x[0])} + ({fmt(W[0, 1])})·{fmt(x[1])} + "
           f"({fmt(b[0])}) = {fmt(a[0], 4)}; a<sub>2</sub> = {fmt(W[1, 0])}·{fmt(x[0])} + ({fmt(W[1, 1])})·{fmt(x[1])} "
           f"+ ({fmt(b[1])}) = {fmt(a[1], 4)}.",
           f"Hidden activations ({actdesc}): h<sub>1</sub> = {fmt(h[0], 4)}, h<sub>2</sub> = {fmt(h[1], 4)}."]
    if not ask_h:
        sol.append(f"Output pre-activation: o = {fmt(v[0])}·{fmt(h[0], 4)} + ({fmt(v[1])})·{fmt(h[1], 4)} + ({fmt(c)}) "
                   f"= {fmt(o, 4)}.")
        sol.append(f"ŷ = {'o' if out == 'linear' else 'σ(o)'} = <b>{fmt(yv, 3)}</b>.")
        q = "the network output ŷ"
    else:
        sol.append(f"Required: h<sub>{j + 1}</sub> = <b>{fmt(val, 4)}</b>.")
        q = f"the activation of hidden unit h<sub>{j + 1}</sub>"
    return Q(text=f"The feed-forward network below has {act} hidden units and a {out} output unit. The number on "
                  f"each edge is its weight and 'b' above a node is that node's bias. For input "
                  f"x = ({fmt(x[0])}, {fmt(x[1])}) (values shown left of the inputs), {q} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Figure(draw, 9, 5.6)], solution=sol)


@template(TOPIC, S_FWD, marks=1, qtype="NAT")
def fwd_int_relu(rng):
    while True:
        x = _ints(rng, -2, 3, 2).astype(float)
        W = _ints(rng, -2, 2, (2, 2), nonzero=True).astype(float)
        b = _ints(rng, -2, 2, 2).astype(float)
        v = _ints(rng, -3, 3, 2, nonzero=True).astype(float)
        c = float(_ints(rng, -2, 2))
        a = W @ x + b
        if np.any(a == 0) or not np.any(a > 0) or not np.any(a < 0) and rng.random() < 0.6:
            continue
        h = np.maximum(0, a)
        yv = v @ h + c
        break
    names = [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$"], ["$y$"]]
    el = {(0, i, jj): fmt(W[jj, i]) for i in range(2) for jj in range(2)}
    el.update({(1, i, 0): fmt(v[i]) for i in range(2)})
    bias = {(1, 0): f"b={fmt(b[0])}", (1, 1): f"b={fmt(b[1])}", (2, 0): f"b={fmt(c)}"}

    def draw(fig):
        _draw_net(fig, [2, 2, 1], names, el, bias, ["input", "hidden (ReLU)", "output (linear)"],
                  t_edge=[0.3, 0.45], input_values=[fmt(x[0]), fmt(x[1])])

    sol = [f"a = Wx + b = ({fmt(a[0])}, {fmt(a[1])}); h = ReLU(a) = ({fmt(h[0])}, {fmt(h[1])})"
           + (" – a negative pre-activation is clipped to 0." if np.any(a < 0) else "."),
           f"y = {fmt(v[0])}·{fmt(h[0])} + ({fmt(v[1])})·{fmt(h[1])} + ({fmt(c)}) = <b>{fmt(yv)}</b>.",
           "A common slip is to forget the ReLU and use the raw pre-activation "
           f"(which would give {fmt(v @ a + c)})."]
    return Q(text=f"For the ReLU network shown (edge labels are weights, 'b' denotes a bias) and input "
                  f"x = ({fmt(x[0])}, {fmt(x[1])}), the output y is ______ " + nat_hint(0),
             qtype="NAT", marks=1, answer=(float(yv), float(yv)), nat_hint=nat_hint(0),
             blocks=[Figure(draw, 8.5, 5.3)], solution=sol)


@template(TOPIC, S_FWD, marks=2, qtype="NAT")
def fwd_softmax(rng):
    act = _pick(rng, ["ReLU", "tanh"])
    f = _act_fn(act)
    while True:
        x = _ints(rng, -1, 2, 3).astype(float)
        W1 = _halfgrid(rng, -1, 1, (2, 3), nonzero=False).astype(float)
        b1 = _halfgrid(rng, -1, 1, 2, nonzero=False).astype(float)
        W2 = _ints(rng, -2, 2, (3, 2)).astype(float)
        b2 = _halfgrid(rng, -1, 1, 3, nonzero=False).astype(float)
        a = W1 @ x + b1
        if np.any(np.abs(a) < 0.25) or not np.any(a > 0):
            continue
        h = f(a)
        z = W2 @ h + b2
        if np.ptp(z) < 0.3:
            continue
        p = _softmax(z)
        break
    k = int(rng.choice(np.flatnonzero(p > 0.08)))

    def draw(fig):
        _draw_net(fig, [3, 2, 3], [["$x_1$", "$x_2$", "$x_3$"], ["$h_1$", "$h_2$"], ["$p_1$", "$p_2$", "$p_3$"]],
                  None, None, ["input", f"hidden ({act})", "softmax"])

    sol = [f"a = W<sub>1</sub>x + b<sub>1</sub> = {vec(a, 3)}; h = {act}(a) = {vec(h, 4)}.",
           f"z = W<sub>2</sub>h + b<sub>2</sub> = {vec(z, 4)}.",
           "exp(z) = " + vec(np.exp(z), 4) + f", sum = {fmt(np.exp(z).sum(), 4)}.",
           f"p<sub>{k + 1}</sub> = exp(z<sub>{k + 1}</sub>)/Σ exp(z<sub>j</sub>) = <b>{fmt(p[k], 4)}</b>. "
           f"(All probabilities: {vec(p, 3)}.)"]
    return Q(text=f"A 3-2-3 network computes h = {act}(W<sub>1</sub>x + b<sub>1</sub>), z = W<sub>2</sub>h + "
                  f"b<sub>2</sub>, p = softmax(z), with the parameters below. For x = {vec(x)}ᵀ, the predicted "
                  f"probability p<sub>{k + 1}</sub> of class {k + 1} is ______ " + _nat_auto(p[k])[1],
             qtype="NAT", marks=2, answer=_nat_auto(p[k])[0], nat_hint=_nat_auto(p[k])[1],
             blocks=[Figure(draw, 7.5, 5.2), _M("W₁", W1), _M("b₁", b1), _M("W₂", W2),
                     _M("b₂", b2)],
             solution=sol)


@template(TOPIC, S_FWD, marks=2, qtype="MCQ")
def fwd_vector_mcq(rng):
    while True:
        x = _ints(rng, -2, 2, 3).astype(float)
        W1 = _ints(rng, -2, 2, (3, 3)).astype(float)
        b1 = _ints(rng, -1, 1, 3).astype(float)
        W2 = _ints(rng, -1, 2, (2, 3)).astype(float)
        b2 = _ints(rng, -1, 1, 2).astype(float)
        a = W1 @ x + b1
        if not np.any(a < 0) or not np.any(a > 0) or np.any(a == 0):
            continue
        y = W2 @ np.maximum(0, a) + b2
        y_norelu = W2 @ a + b2
        y_T = W2 @ np.maximum(0, W1.T @ x + b1) + b2
        y_nob = W2 @ np.maximum(0, W1 @ x)
        y_abs = W2 @ np.abs(a) + b2
        cands = [y, y_norelu, y_T, y_nob, y_abs]
        strs = [vec(c, 0) for c in cands]
        if len(set(strs[:4])) < 4 and len(set(strs)) < 4:
            continue
        if strs[0] in strs[1:]:
            continue
        ds = [s for s in strs[1:] if s != strs[0]]
        if len(set(ds)) < 3:
            continue
        break
    opts, ans = mcq(rng, "ŷ = " + strs[0] + "ᵀ", ["ŷ = " + s + "ᵀ" for s in ds])
    sol = [f"a = W<sub>1</sub>x + b<sub>1</sub> = {vec(a, 0)}ᵀ; h = ReLU(a) = {vec(np.maximum(0, a), 0)}ᵀ.",
           f"ŷ = W<sub>2</sub>h + b<sub>2</sub> = <b>{strs[0]}ᵀ</b>.",
           f"Distractors: skipping the ReLU gives {strs[1]}ᵀ; using W<sub>1</sub>ᵀ instead of W<sub>1</sub> gives "
           f"{strs[2]}ᵀ; dropping the biases gives {strs[3]}ᵀ; using |a| instead of ReLU gives {strs[4]}ᵀ."]
    return Q(text=f"A network computes ŷ = W<sub>2</sub> ReLU(W<sub>1</sub>x + b<sub>1</sub>) + b<sub>2</sub> with "
                  f"the parameters below. For x = {vec(x, 0)}ᵀ, the output ŷ is",
             qtype="MCQ", marks=2, options=opts, answer=ans,
             blocks=[_M("W₁", W1, 0), _M("b₁", b1, 0), _M("W₂", W2, 0), _M("b₂", b2, 0)],
             solution=sol)


# ============================================================================
# BACKPROPAGATION
# ============================================================================
@template(TOPIC, S_BP, marks=2, qtype="NAT")
def bp_neuron_mse(rng):
    while True:
        x = _halfgrid(rng, -2, 2, 3).astype(float)
        w = _halfgrid(rng, -1.5, 1.5, 3).astype(float)
        b = float(_halfgrid(rng, -1, 1, nonzero=False))
        y = int(rng.integers(2))
        a = w @ x + b
        yh = _sig(a)
        if abs(a) > 2.5 or abs(a) < 0.1:
            continue
        break
    k = int(rng.integers(3))
    eta = float(_pick(rng, [0.1, 0.5, 1.0, 0.2]))
    delta = (yh - y) * yh * (1 - yh)
    g = delta * x[k]
    v = int(rng.integers(3))
    if v == 0:
        val, ask = g, f"∂L/∂w<sub>{k + 1}</sub>"
    elif v == 1:
        val, ask = w[k] - eta * g, f"the updated weight w<sub>{k + 1}</sub> after one gradient-descent step with η = {fmt(eta)}"
    else:
        val, ask = delta, "∂L/∂b"
    names = [["$x_1$", "$x_2$", "$x_3$"], ["$\\hat{y}$"]]
    el = {(0, i, 0): f"w{'₁₂₃'[i]}={fmt(w[i])}" for i in range(3)}

    def draw(fig):
        _draw_net(fig, [3, 1], names, el, {(1, 0): f"b={fmt(b)}"}, ["input", "sigmoid"], t_edge=[0.45],
                  input_values=[fmt(v_) for v_ in x])

    sol = [f"a = w·x + b = {fmt(a, 4)}; ŷ = σ(a) = {fmt(yh, 4)}.",
           f"L = ½(ŷ − y)² ⇒ ∂L/∂ŷ = ŷ − y = {fmt(yh - y, 4)}; ∂ŷ/∂a = ŷ(1 − ŷ) = {fmt(yh * (1 - yh), 4)}.",
           f"δ = ∂L/∂a = (ŷ − y)ŷ(1 − ŷ) = {fmt(delta, 4)} (= ∂L/∂b)."]
    if v != 2:
        sol.append(f"∂L/∂w<sub>{k + 1}</sub> = δ·x<sub>{k + 1}</sub> = {fmt(delta, 4)} × {fmt(x[k])} = {fmt(g, 4)}.")
    if v == 1:
        sol.append(f"w<sub>{k + 1}</sub> ← w<sub>{k + 1}</sub> − η ∂L/∂w<sub>{k + 1}</sub> = {fmt(w[k])} − "
                   f"{fmt(eta)}×({fmt(g, 4)}) = <b>{fmt(val, 4)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(val, 4)}</b>.")
    sol.append("Forgetting the factor ŷ(1 − ŷ) (i.e. treating the output as linear) is the most common error.")
    return Q(text=f"A single sigmoid neuron (shown below) receives x = {vec(x)} and has target y = {y}. The loss is "
                  f"L = ½(ŷ − y)². The value of {ask} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Figure(draw, 7, 4.6)], solution=sol)


@template(TOPIC, S_BP, marks=2, qtype="NAT")
def bp_two_layer(rng):
    while True:
        x = _halfgrid(rng, -1.5, 1.5, 2).astype(float)
        W = _halfgrid(rng, -1.5, 1.5, (2, 2)).astype(float)
        b = np.zeros(2)
        v = _halfgrid(rng, -2, 2, 2).astype(float)
        y = float(_halfgrid(rng, -1, 2, nonzero=False))
        a = W @ x + b
        h = _sig(a)
        yh = v @ h
        e = yh - y
        if abs(e) < 0.2:
            continue
        break
    var = int(rng.integers(3))
    j = int(rng.integers(2))
    k = int(rng.integers(2))
    if var == 0:
        val = e * h[j]
        ask = f"∂L/∂v<sub>{j + 1}</sub>"
    elif var == 1:
        val = e * v[j] * h[j] * (1 - h[j]) * x[k]
        ask = f"∂L/∂w<sub>{j + 1}{k + 1}</sub> (the weight from x<sub>{k + 1}</sub> to h<sub>{j + 1}</sub>)"
    else:
        val = e * v[j] * h[j] * (1 - h[j])
        ask = f"∂L/∂b<sub>{j + 1}</sub> (bias of hidden unit h<sub>{j + 1}</sub>, currently 0)"
    names = [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$"], ["$\\hat{y}$"]]
    el = {(0, i, jj): f"{fmt(W[jj, i])}" for i in range(2) for jj in range(2)}
    el.update({(1, i, 0): f"v{'₁₂'[i]}={fmt(v[i])}" for i in range(2)})

    def draw(fig):
        _draw_net(fig, [2, 2, 1], names, el, None, ["input", "hidden (sigmoid)", "output (linear)"],
                  t_edge=[0.3, 0.45], input_values=[fmt(x[0]), fmt(x[1])])

    dj = e * v[j] * h[j] * (1 - h[j])
    sol = [f"Forward: a = Wx = {vec(a, 4)}, h = σ(a) = {vec(h, 4)}, ŷ = v·h = {fmt(yh, 4)}.",
           f"Output error δ<sub>o</sub> = ∂L/∂ŷ = ŷ − y = {fmt(e, 4)} (linear output, L = ½(ŷ − y)²)."]
    if var == 0:
        sol.append(f"∂L/∂v<sub>{j + 1}</sub> = δ<sub>o</sub>·h<sub>{j + 1}</sub> = {fmt(e, 4)} × {fmt(h[j], 4)} "
                   f"= <b>{fmt(val, 4)}</b>.")
    else:
        sol.append(f"Hidden delta δ<sub>{j + 1}</sub> = δ<sub>o</sub>·v<sub>{j + 1}</sub>·h<sub>{j + 1}</sub>"
                   f"(1 − h<sub>{j + 1}</sub>) = {fmt(e, 4)} × {fmt(v[j])} × {fmt(h[j] * (1 - h[j]), 4)} = {fmt(dj, 4)}.")
        if var == 1:
            sol.append(f"∂L/∂w<sub>{j + 1}{k + 1}</sub> = δ<sub>{j + 1}</sub>·x<sub>{k + 1}</sub> = {fmt(dj, 4)} × "
                       f"{fmt(x[k])} = <b>{fmt(val, 4)}</b>.")
        else:
            sol.append(f"∂L/∂b<sub>{j + 1}</sub> = δ<sub>{j + 1}</sub> = <b>{fmt(val, 4)}</b>.")
    return Q(text=f"In the network below, hidden units are sigmoid, the output is linear (ŷ = v<sub>1</sub>h<sub>1</sub>"
                  f" + v<sub>2</sub>h<sub>2</sub>), all biases are 0, and the loss is L = ½(ŷ − y)². For input "
                  f"x = ({fmt(x[0])}, {fmt(x[1])}) and target y = {fmt(y)}, the value of {ask} is ______ "
                  + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Figure(draw, 9, 5.4)], solution=sol)


@template(TOPIC, S_BP, marks=2, qtype="NAT")
def bp_logistic_bce(rng):
    while True:
        w = _halfgrid(rng, -1, 1, 2, nonzero=False).astype(float)
        b = float(_halfgrid(rng, -1, 1, nonzero=False))
        X = _halfgrid(rng, -2, 2, (2, 2)).astype(float)
        y = rng.integers(0, 2, 2)
        p = _sig(X @ w + b)
        if np.any(np.abs(p - y) < 0.05):
            continue
        break
    eta = float(_pick(rng, [0.1, 0.5, 1.0]))
    batch = rng.random() < 0.5
    k = int(rng.integers(3))  # 0,1 weights, 2 bias
    feats = np.c_[X, np.ones(2)]
    if batch:
        g = ((p - y)[:, None] * feats).mean(axis=0)
    else:
        g = (p[0] - y[0]) * feats[0]
    params = np.r_[w, b]
    new = params - eta * g
    pname = ["w<sub>1</sub>", "w<sub>2</sub>", "b"][k]
    val = new[k]
    rows = [["example", "x<sub>1</sub>", "x<sub>2</sub>", "y"]] + [[str(i + 1), fmt(X[i, 0]), fmt(X[i, 1]), str(y[i])]
                                                                  for i in range(2)]
    sol = [f"For σ output with binary cross-entropy L = −[y ln p + (1 − y) ln(1 − p)], ∂L/∂a = p − y, so "
           f"∂L/∂w<sub>j</sub> = (p − y)x<sub>j</sub> and ∂L/∂b = p − y."]
    for i in range(2 if batch else 1):
        sol.append(f"Example {i + 1}: a = {fmt(X[i] @ w + b, 4)}, p = {fmt(p[i], 4)}, p − y = {fmt(p[i] - y[i], 4)}.")
    sol.append(("Mini-batch (mean) gradient" if batch else "Gradient") + f" for {pname}: {fmt(g[k], 4)}.")
    sol.append(f"{pname} ← {fmt(params[k])} − {fmt(eta)} × ({fmt(g[k], 4)}) = <b>{fmt(val, 4)}</b>.")
    sol.append("Note there is no σ′ factor: it cancels with the derivative of the log loss.")
    which = ("one gradient-descent step using the <b>average</b> loss over both examples (a mini-batch of size 2)"
             if batch else "one stochastic gradient step on <b>example 1 only</b>")
    return Q(text=f"A logistic-regression neuron p = σ(w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + b) "
                  f"has w = ({fmt(w[0])}, {fmt(w[1])}), b = {fmt(b)} and is trained with binary cross-entropy loss. "
                  f"After {which} with learning rate η = {fmt(eta)}, the new value of {pname} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Table(rows)], solution=sol)


@template(TOPIC, S_BP, marks=2, qtype="NAT")
def bp_relu(rng):
    while True:
        x = _ints(rng, -2, 2, 2, nonzero=True).astype(float)
        W = _ints(rng, -2, 2, (3, 2)).astype(float)
        b = _ints(rng, -1, 1, 3).astype(float)
        v = _ints(rng, -2, 2, 3, nonzero=True).astype(float)
        c = float(_ints(rng, -1, 1))
        a = W @ x + b
        if np.any(a == 0) or np.all(a > 0) or np.all(a < 0):
            continue
        h = np.maximum(0, a)
        yh = v @ h + c
        y = float(_ints(rng, -3, 3))
        e = yh - y
        if e == 0:
            continue
        break
    var = int(rng.integers(3))
    j = int(rng.integers(3))
    k = int(rng.integers(2))
    act = (a > 0).astype(float)
    if var == 0:
        val = e * v[j] * act[j] * x[k]
        ask = f"∂L/∂W<sub>{j + 1}{k + 1}</sub>"
    elif var == 1:
        val = e * h[j]
        ask = f"∂L/∂v<sub>{j + 1}</sub>"
    else:
        val = e * float(np.sum(v * act * W[:, k]))
        ask = f"∂L/∂x<sub>{k + 1}</sub> (gradient with respect to the input)"

    def draw(fig):
        _draw_net(fig, [2, 3, 1], [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$", "$h_3$"], ["$\\hat{y}$"]], None, None,
                  ["input", "hidden (ReLU)", "output (linear)"])

    sol = [f"a = Wx + b = {vec(a, 0)}, h = ReLU(a) = {vec(h, 0)}, ŷ = v·h + c = {fmt(yh)}; ∂L/∂ŷ = ŷ − y = {fmt(e)}.",
           f"ReLU′(a) = {vec(act, 0)} (unit j is active iff a<sub>j</sub> &gt; 0)."]
    if var == 0:
        sol.append(f"∂L/∂W<sub>{j + 1}{k + 1}</sub> = (ŷ − y)·v<sub>{j + 1}</sub>·ReLU′(a<sub>{j + 1}</sub>)·"
                   f"x<sub>{k + 1}</sub> = {fmt(e)}×{fmt(v[j])}×{fmt(act[j])}×{fmt(x[k])} = <b>{fmt(val)}</b>."
                   + (" The unit is inactive, so no gradient flows to its incoming weights." if act[j] == 0 else ""))
    elif var == 1:
        sol.append(f"∂L/∂v<sub>{j + 1}</sub> = (ŷ − y)·h<sub>{j + 1}</sub> = {fmt(e)}×{fmt(h[j])} = <b>{fmt(val)}</b>.")
    else:
        sol.append(f"∂L/∂x<sub>{k + 1}</sub> = (ŷ − y) Σ<sub>j</sub> v<sub>j</sub> ReLU′(a<sub>j</sub>) "
                   f"W<sub>j{k + 1}</sub> = {fmt(e)} × ("
                   + " + ".join(f"{fmt(v[i])}·{fmt(act[i])}·{fmt(W[i, k])}" for i in range(3))
                   + f") = <b>{fmt(val)}</b>.")
    return Q(text=f"The 2-3-1 network below computes ŷ = v·ReLU(Wx + b) + c with W, b, v given below and c = {fmt(c)}. "
                  f"With x = ({fmt(x[0])}, {fmt(x[1])}), target y = {fmt(y)} and loss L = ½(ŷ − y)², the value of "
                  f"{ask} is ______ " + nat_hint(0),
             qtype="NAT", marks=2, answer=(float(val), float(val)), nat_hint=nat_hint(0),
             blocks=[Figure(draw, 7, 5.0), _M("W", W, 0), _M("b", b, 0), _M("vᵀ", v[None, :], 0)],
             solution=sol)


BP_T = [
    ("Backpropagation computes the gradient of the loss with respect to every weight using the chain rule, at a "
     "cost of the same order as one forward pass.", "Reverse-mode differentiation reuses intermediate results."),
    ("For a sigmoid output with binary cross-entropy (or softmax with cross-entropy), the error at the output "
     "pre-activation is ŷ − y.", "The σ′ factor cancels with the log-loss derivative."),
    ("For a hidden unit j, δ<sub>j</sub> = f′(a<sub>j</sub>) Σ<sub>k</sub> w<sub>kj</sub> δ<sub>k</sub>, summing over "
     "the units k that j feeds into.", "Standard backprop recursion."),
    ("∂L/∂w<sub>ji</sub> = δ<sub>j</sub> z<sub>i</sub>, where z<sub>i</sub> is the activation flowing along the weight "
     "w<sub>ji</sub> into unit j.", "Pre-activation a<sub>j</sub> is linear in w<sub>ji</sub> with coefficient z<sub>i</sub>."),
    ("Backpropagation needs the activations computed in the forward pass (stored or recomputed).",
     "Local derivatives f′(a) and inputs z are needed."),
    ("If a ReLU unit's pre-activation is negative for an input, no gradient flows through that unit for that input.",
     "ReLU′(a) = 0 for a &lt; 0."),
    ("Backpropagation only computes gradients; the parameter update rule (SGD, momentum, Adam) is a separate choice.",
     "Backprop ≠ optimiser."),
    ("The gradient of a sum of per-example losses equals the sum of the per-example gradients.",
     "Differentiation is linear."),
    ("With L = ½(ŷ − y)² and a sigmoid output unit, δ<sub>out</sub> = (ŷ − y) ŷ (1 − ŷ).", "Chain rule through σ."),
    ("A finite-difference (central difference) check can be used to verify a backprop implementation.",
     "[L(w+ε) − L(w−ε)]/2ε ≈ ∂L/∂w."),
    ("The gradient with respect to a bias b<sub>j</sub> equals δ<sub>j</sub>.", "a<sub>j</sub> depends on b<sub>j</sub> with coefficient 1."),
    ("In backpropagation, the deltas of a layer are computed after (from) the deltas of the next layer.",
     "Errors propagate from output towards input."),
]
BP_F = [
    ("Backpropagation computes gradients only for the output-layer weights.", "It computes gradients for all layers."),
    ("Backpropagation guarantees convergence to the global minimum of the training loss.",
     "It only computes gradients; the loss is non-convex in general."),
    ("The cost of backpropagation grows exponentially with the number of layers.",
     "It is linear in the number of weights (same order as a forward pass)."),
    ("Backpropagation can only be used with sigmoid activation functions.",
     "Any (sub)differentiable activation works."),
    ("With a sigmoid output unit and squared-error loss ½(ŷ − y)², the output delta is simply ŷ − y.",
     "It is (ŷ − y)ŷ(1 − ŷ); the simple form holds for cross-entropy."),
    ("Backpropagation requires the loss function to be convex.", "Convexity is not required to compute gradients."),
    ("Gradients with respect to biases are always zero, so biases need not be trained.",
     "∂L/∂b<sub>j</sub> = δ<sub>j</sub>, generally non-zero."),
    ("Backpropagation estimates each partial derivative by finite differences.",
     "It computes exact derivatives analytically via the chain rule."),
    ("∂L/∂w<sub>ji</sub> does not depend on the value z<sub>i</sub> of the input feeding that weight.",
     "∂L/∂w<sub>ji</sub> = δ<sub>j</sub> z<sub>i</sub>."),
    ("If all weights of an MLP are initialised to the same value, backpropagation gives different gradients to "
     "the hidden units of a layer, breaking the symmetry automatically.",
     "Identical units receive identical gradients; symmetry is never broken."),
    ("Hidden-layer deltas are computed before the output-layer deltas.", "Order is output → input."),
    ("In backpropagation, ReLU units with negative pre-activation pass the gradient unchanged.",
     "Their local derivative is 0, blocking the gradient."),
]


@template(TOPIC, S_BP, marks=1, qtype="MSQ")
def bp_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, BP_T, BP_F)
    return Q(text="Which of the following statements about backpropagation is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# ============================================================================
# PARAMETER COUNTING
# ============================================================================
@template(TOPIC, S_PAR, marks=1, qtype="NAT")
def param_count(rng):
    d = int(_pick(rng, [784, 100, 64, 32, 20, 10, 3072, 50, 256, 12]))
    nh = int(rng.integers(1, 4))
    hs = [int(_pick(rng, [512, 256, 128, 100, 64, 50, 32, 16, 10, 8])) for _ in range(nh)]
    k = int(_pick(rng, [10, 1, 3, 5, 2, 100]))
    sizes = [d] + hs + [k]
    v = int(rng.integers(3))
    W = sum(sizes[i] * sizes[i + 1] for i in range(len(sizes) - 1))
    B = sum(sizes[1:])
    val = [W + B, W, B][v]
    ask = ["total number of trainable parameters (weights and biases)", "number of weights (excluding biases)",
           "number of bias parameters"][v]
    arch = "-".join(map(str, sizes))
    sol = ["Fully connected layer with n<sub>in</sub> inputs and n<sub>out</sub> outputs: n<sub>in</sub>·n<sub>out</sub> "
           "weights + n<sub>out</sub> biases."]
    for i in range(len(sizes) - 1):
        sol.append(f"Layer {i + 1}: {sizes[i]}×{sizes[i + 1]} = {sizes[i] * sizes[i + 1]} weights, {sizes[i + 1]} biases.")
    sol.append(f"Weights = {W}, biases = {B}. Required: <b>{val}</b>.")
    return Q(text=f"A fully connected MLP has layer sizes {arch} (input-…-output), every layer having a bias "
                  f"vector. The {ask} is ______ " + nat_hint(0),
             qtype="NAT", marks=1, answer=(float(val), float(val)), nat_hint=nat_hint(0), solution=sol)


@template(TOPIC, S_PAR, marks=2, qtype="NAT")
def param_advanced(rng):
    v = int(rng.integers(4))
    if v == 0:
        d = int(_pick(rng, [20, 30, 50, 64, 100, 784]))
        k = int(_pick(rng, [1, 3, 5, 10]))
        h = int(rng.integers(5, 65))
        P = (d + 1) * h + (h + 1) * k
        val = h
        text = (f"A network with one hidden layer maps {d} inputs to {k} output{'s' if k > 1 else ''}; all layers "
                f"are fully connected and have biases. It has exactly {P} trainable parameters. The number of "
                f"hidden units is ______ ")
        sol = [f"P = (d + 1)h + (h + 1)k = h(d + k + 1) + k ⇒ h = (P − k)/(d + k + 1) = ({P} − {k})/({d} + {k} + 1) "
               f"= <b>{h}</b>."]
    elif v == 1:
        sizes = [int(_pick(rng, [784, 100, 64, 32])), int(_pick(rng, [128, 64, 32, 16])),
                 int(_pick(rng, [64, 32, 16, 8])), int(_pick(rng, [10, 2, 1]))]
        Bt = int(_pick(rng, [1, 16, 32, 64, 100]))
        Wm = sum(sizes[i] * sizes[i + 1] for i in range(3))
        val = Wm * Bt
        text = (f"For the fully connected network {'-'.join(map(str, sizes))}, a forward pass on a mini-batch of "
                f"{Bt} input{'s' if Bt > 1 else ''} is computed as dense matrix products. Counting only the scalar "
                f"multiplications in the weight-matrix products (ignore biases and activations), the number of "
                f"multiplications is ______ ")
        sol = ["Each weight participates in exactly one multiplication per example."] + [
            f"Layer {i + 1}: {sizes[i]}×{sizes[i + 1]} = {sizes[i] * sizes[i + 1]}." for i in range(3)] + [
            f"Per example: {Wm}; for {Bt} examples: {Wm}×{Bt} = <b>{val}</b>."]
    elif v == 2:
        d = int(_pick(rng, [784, 100, 64, 256, 50]))
        h = int(_pick(rng, [32, 16, 10, 8, 64]))
        tied = rng.random() < 0.5
        if tied:
            val = d * h + h + d
            text = (f"An autoencoder {d}-{h}-{d} uses tied weights: the decoder weight matrix is the transpose of the "
                    f"encoder weight matrix W ∈ ℝ<super>{h}×{d}</super>, while encoder and decoder have their own bias "
                    f"vectors. The number of trainable parameters is ______ ")
            sol = [f"Shared W: {h}×{d} = {d * h}; encoder bias {h}; decoder bias {d}. Total = <b>{val}</b>.",
                   f"(Without tying it would be 2×{d * h} + {h} + {d} = {2 * d * h + h + d}.)"]
        else:
            val = 2 * d * h + h + d
            text = (f"An autoencoder with layer sizes {d}-{h}-{d} (fully connected, separate encoder and decoder "
                    f"weights, biases in both layers) has ______ trainable parameters. ")
            sol = [f"Encoder: {d}×{h} + {h} = {d * h + h}; decoder: {h}×{d} + {d} = {d * h + d}. Total = <b>{val}</b>."]
    else:
        d = int(_pick(rng, [100, 64, 50, 32]))
        h1 = int(_pick(rng, [64, 32, 20]))
        m = int(_pick(rng, [16, 10, 8, 32]))
        k = int(_pick(rng, [10, 3, 1]))
        before = (d + 1) * h1 + (h1 + 1) * k
        after = (d + 1) * h1 + (h1 + 1) * m + (m + 1) * k
        val = after - before
        text = (f"A {d}-{h1}-{k} fully connected network (with biases) is modified by inserting a new hidden layer of "
                f"{m} units between the {h1}-unit layer and the output, giving {d}-{h1}-{m}-{k}. The change in "
                f"the number of trainable parameters (new minus old) is ______ ")
        sol = [f"Old: ({d}+1)·{h1} + ({h1}+1)·{k} = {before}.",
               f"New: ({d}+1)·{h1} + ({h1}+1)·{m} + ({m}+1)·{k} = {after}.",
               f"Change = <b>{val}</b>" + (" (negative: the bottleneck reduces parameters)." if val < 0 else ".")]
    return Q(text=text + nat_hint(0), qtype="NAT", marks=2, answer=(float(val), float(val)), nat_hint=nat_hint(0),
             solution=sol)


# ============================================================================
# EXPRESSIVENESS
# ============================================================================
@template(TOPIC, S_EXP, marks=2, qtype="NAT")
def linear_collapse(rng):
    while True:
        W1 = _ints(rng, -2, 2, (2, 2)).astype(float)
        b1 = _ints(rng, -2, 2, 2).astype(float)
        W2 = _ints(rng, -2, 2, (1, 2), nonzero=True).astype(float)
        b2 = float(_ints(rng, -2, 2))
        Weff = (W2 @ W1).ravel()
        beff = float((W2 @ b1)[0] + b2)
        if np.all(Weff == 0):
            continue
        break
    v = int(rng.integers(4))
    if v in (0, 1):
        val = Weff[v]
        ask = f"the coefficient w̃<sub>{v + 1}</sub>"
    elif v == 2:
        val = beff
        ask = "the intercept b̃"
    else:
        x = _ints(rng, -3, 3, 2).astype(float)
        val = float(Weff @ x + beff)
        ask = f"the output for x = ({fmt(x[0])}, {fmt(x[1])})"
    sol = ["With identity activations, ŷ = W<sub>2</sub>(W<sub>1</sub>x + b<sub>1</sub>) + b<sub>2</sub> = "
           "(W<sub>2</sub>W<sub>1</sub>)x + (W<sub>2</sub>b<sub>1</sub> + b<sub>2</sub>): a single affine map.",
           f"w̃ᵀ = W<sub>2</sub>W<sub>1</sub> = ({fmt(Weff[0])}, {fmt(Weff[1])}); b̃ = W<sub>2</sub>b<sub>1</sub> + "
           f"b<sub>2</sub> = {fmt(beff)}."]
    if v == 3:
        sol.append(f"ŷ = {fmt(Weff[0])}·{fmt(x[0])} + ({fmt(Weff[1])})·{fmt(x[1])} + ({fmt(beff)}) = <b>{fmt(val)}</b>.")
    else:
        sol.append(f"Answer: <b>{fmt(val)}</b>.")
    sol.append("Hence stacking linear layers adds no expressive power – a non-linear activation is essential.")
    return Q(text="A 2-2-1 network uses the identity (linear) activation in its hidden layer: ŷ = W<sub>2</sub>"
                  "(W<sub>1</sub>x + b<sub>1</sub>) + b<sub>2</sub>, with the parameters below. The network is "
                  "equivalent to a single linear model ŷ = w̃<sub>1</sub>x<sub>1</sub> + w̃<sub>2</sub>x<sub>2</sub> "
                  f"+ b̃. Then {ask} is ______ " + nat_hint(0),
             qtype="NAT", marks=2, answer=(float(val), float(val)), nat_hint=nat_hint(0),
             blocks=[_M("W₁", W1, 0), _M("b₁", b1, 0), _M("W₂", W2, 0), f"b<sub>2</sub> = {fmt(b2)}"],
             solution=sol)


@template(TOPIC, S_EXP, marks=2, qtype="MCQ")
def xor_net(rng):
    gates = list(GATE_TT)
    while True:
        g1, g2, go = (gates[int(i)] for i in rng.integers(len(gates), size=3))
        if g1 == g2:
            continue
        p1 = _sample_gate(rng, GATE_TT[g1], (-2, 2))
        p2 = _sample_gate(rng, GATE_TT[g2], (-2, 2))
        po = _sample_gate(rng, GATE_TT[go], (-2, 2))
        outs = []
        for a, c in INPUTS:
            h1 = int(p1[0] * a + p1[1] * c + p1[2] > 0)
            h2 = int(p2[0] * a + p2[1] * c + p2[2] > 0)
            outs.append(int(po[0] * h1 + po[1] * h2 + po[2] > 0))
        outs = tuple(outs)
        if outs not in TT_NAME:
            continue
        if outs in ((0, 1, 1, 0), (1, 0, 0, 1)) or rng.random() < 0.15:
            break
    correct = TT_NAME[outs]
    pool = ["XOR", "XNOR", "AND", "OR", "NAND", "NOR", "x₁ AND (NOT x₂)", "(NOT x₁) AND x₂"]
    opts, ans = mcq(rng, correct, pool)
    names = [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$"], ["$y$"]]
    el = {(0, 0, 0): fmt(p1[0]), (0, 1, 0): fmt(p1[1]), (0, 0, 1): fmt(p2[0]), (0, 1, 1): fmt(p2[1]),
          (1, 0, 0): fmt(po[0]), (1, 1, 0): fmt(po[1])}
    bias = {(1, 0): f"b={fmt(p1[2])}", (1, 1): f"b={fmt(p2[2])}", (2, 0): f"b={fmt(po[2])}"}

    def draw(fig):
        _draw_net(fig, [2, 2, 1], names, el, bias, ["input", "hidden (step)", "output (step)"], t_edge=[0.3, 0.45])

    rows = [["x<sub>1</sub>", "x<sub>2</sub>", "h<sub>1</sub>", "h<sub>2</sub>", "y"]]
    for (a, c), o in zip(INPUTS, outs):
        h1 = int(p1[0] * a + p1[1] * c + p1[2] > 0)
        h2 = int(p2[0] * a + p2[1] * c + p2[2] > 0)
        rows.append([str(a), str(c), str(h1), str(h2), str(o)])
    sol = ["Each unit outputs 1 iff its net input (weighted sum + bias) is &gt; 0. Evaluate on all four inputs:",
           Table(rows),
           f"h<sub>1</sub> computes {TT_NAME[GATE_TT[g1]]}, h<sub>2</sub> computes {TT_NAME[GATE_TT[g2]]}; the output "
           f"column (0,0)→(1,1) is {', '.join(map(str, outs))}, i.e. <b>{correct}</b>."]
    if outs in ((0, 1, 1, 0), (1, 0, 0, 1)):
        sol.append("This shows that one hidden layer of two threshold units suffices for the non-linearly-separable "
                   f"{correct}, which a single perceptron cannot represent.")
    return Q(text="In the network below every unit (hidden and output) is a threshold unit that outputs 1 if its "
                  "weighted input plus bias is &gt; 0, and 0 otherwise. Edge labels are weights. For binary inputs "
                  "x<sub>1</sub>, x<sub>2</sub> ∈ {0, 1}, the network computes",
             qtype="MCQ", marks=2, options=opts, answer=ans, blocks=[Figure(draw, 8.5, 5.3)], solution=sol)


EXP_T = [
    ("An MLP of any depth with identity (linear) activations computes an affine function of its input.",
     "A composition of affine maps is affine."),
    ("Universal approximation theorem: a single hidden layer with enough units and a non-polynomial activation "
     "(e.g. sigmoid) can approximate any continuous function on a compact set to arbitrary accuracy.",
     "Cybenko (1989) / Hornik (1991) / Leshno et al. (1993)."),
    ("The universal approximation theorem is an existence result; it does not say that gradient descent will find "
     "the approximating weights.", "It says nothing about learnability or sample complexity."),
    ("XOR can be computed by an MLP with one hidden layer containing two threshold units.",
     "E.g. h₁ = OR, h₂ = NAND, y = AND(h₁, h₂)."),
    ("Every Boolean function of n binary inputs can be represented by an MLP with a single hidden layer of threshold "
     "units (possibly with exponentially many hidden units).", "One hidden unit per positive input pattern (DNF)."),
    ("A ReLU network computes a continuous piecewise-linear function of its input.",
     "Composition of affine maps and max(0, ·)."),
    ("A single sigmoid neuron (logistic regression) has a linear decision boundary.",
     "σ(w·x + b) = 0.5 ⇔ w·x + b = 0."),
    ("A one-hidden-layer network with sigmoid hidden units can produce a decision boundary that is non-linear in the "
     "input.", "The output is a non-linear combination of several sigmoids."),
    ("Some functions that a deep network represents with few units require exponentially many units in a "
     "shallow (one-hidden-layer) network.", "Depth-efficiency results (e.g. Telgarsky's sawtooth construction)."),
    ("Removing all non-linear activations from a deep MLP reduces it to the hypothesis class of linear regression "
     "(or logistic regression if the output is sigmoid).", "The pre-output computation is affine."),
    ("The universal approximation theorem also holds with ReLU activations.",
     "ReLU is non-polynomial, so the Leshno et al. theorem applies."),
]
EXP_F = [
    ("The universal approximation theorem guarantees that gradient descent will find weights approximating any "
     "continuous function.", "It is only an existence statement."),
    ("The universal approximation theorem requires at least two hidden layers.", "One hidden layer suffices."),
    ("An MLP with 10 hidden layers and identity activations can represent XOR.",
     "It is still a linear model; XOR is not linearly separable."),
    ("A single sigmoid neuron can represent XOR because the sigmoid is non-linear.",
     "Its decision boundary w·x + b = 0 is still linear."),
    ("A ReLU network with finitely many units can represent a discontinuous step function exactly.",
     "ReLU networks compute continuous functions."),
    ("Adding hidden layers with identity activations enlarges the set of functions the network can represent.",
     "The composition remains affine."),
    ("The universal approximation theorem states that the number of hidden units needed grows at most linearly "
     "with the input dimension.", "It gives no such bound; the width can be very large."),
    ("A network with a single hidden layer of two ReLU units can approximate any continuous function on [0, 1] to "
     "arbitrary accuracy.", "Width must grow with the required accuracy."),
    ("Logistic regression has a non-linear decision boundary because the sigmoid is non-linear.",
     "Thresholding σ(w·x+b) at 0.5 gives the hyperplane w·x + b = 0."),
    ("The universal approximation theorem fails for sigmoid activations; it holds only for ReLU.",
     "The original result (Cybenko) was proved for sigmoids."),
    ("A two-layer linear network ŷ = W₂W₁x can represent functions that a single linear layer ŷ = Wx cannot.",
     "Take W = W₂W₁."),
]


@template(TOPIC, S_EXP, marks=1, qtype="MSQ")
def expr_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, EXP_T, EXP_F)
    return Q(text="Which of the following statements about the representational power of feed-forward neural "
                  "networks is/are CORRECT?", qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


# ============================================================================
# TRAINING
# ============================================================================
@template(TOPIC, S_TRN, marks=1, qtype="NAT")
def epochs_iters(rng):
    N = int(_pick(rng, [1000, 1200, 2500, 5000, 60000, 50000, 10000, 3000, 1050, 999, 2020]))
    B = int(_pick(rng, [16, 32, 64, 100, 128, 50, 256]))
    E = int(rng.integers(2, 21))
    v = int(rng.integers(4))
    full, rem = divmod(N, B)
    per = full + (1 if rem else 0)
    if v == 0:
        val = per * E
        text = (f"A network is trained with mini-batch SGD on N = {N} examples with batch size B = {B} for E = {E} "
                f"epochs. The last, smaller batch of each epoch is kept (not dropped). The total number of parameter "
                f"updates is ______ ")
        sol = [f"Updates per epoch = ⌈N/B⌉ = ⌈{N}/{B}⌉ = {per}" + (f" ({full} full batches + 1 partial batch of {rem})"
                                                                 if rem else "") + ".",
               f"Total = {per} × {E} = <b>{val}</b>."]
    elif v == 1:
        val = full * E
        text = (f"Mini-batch SGD is run on N = {N} examples with batch size B = {B} for E = {E} epochs, and any "
                f"incomplete final batch in an epoch is <b>dropped</b>. The total number of parameter updates is ______ ")
        sol = [f"Updates per epoch = ⌊N/B⌋ = ⌊{N}/{B}⌋ = {full}.", f"Total = {full} × {E} = <b>{val}</b>."]
    elif v == 2:
        T = per * E
        val = E
        text = (f"A training run on N = {N} examples with batch size B = {B} (last partial batch kept) performed "
                f"{T} parameter updates in total. The number of epochs completed is ______ ")
        sol = [f"Updates per epoch = ⌈{N}/{B}⌉ = {per}; epochs = {T}/{per} = <b>{E}</b>."]
    else:
        val = N * E
        text = (f"Pure (single-example) SGD, i.e. batch size 1, is run for E = {E} epochs on N = {N} examples. "
                f"The number of parameter updates is ______ ")
        sol = [f"Batch size 1 ⇒ N updates per epoch; total = {N} × {E} = <b>{val}</b>. "
               f"(Full-batch gradient descent would make only {E}.)"]
    return Q(text=text + nat_hint(0), qtype="NAT", marks=1, answer=(float(val), float(val)), nat_hint=nat_hint(0),
             solution=sol)


@template(TOPIC, S_TRN, marks=2, qtype="NAT")
def momentum(rng):
    a = float(_pick(rng, [1, 2, 4, 0.5]))
    w0 = float(_pick(rng, [1, 2, -2, 3, 4, -1]))
    eta = float(_pick(rng, [0.1, 0.2, 0.05, 0.25]))
    beta = float(_pick(rng, [0.5, 0.9, 0.8]))
    steps = int(rng.integers(2, 4))
    ask_v = rng.random() < 0.3
    w, vv = w0, 0.0
    log = []
    for t in range(1, steps + 1):
        g = a * w
        vv = beta * vv + g
        w = w - eta * vv
        log.append((t, g, vv, w))
    val = vv if ask_v else w
    sol = [f"f(w) = ({fmt(a)}/2)w² ⇒ ∇f(w) = {fmt(a)}w. Update: v<sub>t</sub> = β v<sub>t−1</sub> + ∇f(w<sub>t−1</sub>), "
           f"w<sub>t</sub> = w<sub>t−1</sub> − η v<sub>t</sub>, with v<sub>0</sub> = 0, β = {fmt(beta)}, η = {fmt(eta)}."]
    wp, vprev = w0, 0.0
    for t, g, vt, wt in log:
        sol.append(f"t = {t}: g = {fmt(a)}×{_p(wp)} = {fmt(g, 4)}; v<sub>{t}</sub> = {fmt(beta)}×{_p(vprev)} + "
                   f"{_p(g)} = {fmt(vt, 4)}; w<sub>{t}</sub> = {fmt(wp, 4)} − {fmt(eta)}×{_p(vt)} = {fmt(wt, 4)}.")
        vprev = vt
        wp = wt
    plain = w0 * (1 - eta * a) ** steps
    sol.append(f"Answer: <b>{fmt(val, 4)}</b>." + ("" if ask_v else
               f" (Plain gradient descent without momentum would give w<sub>{steps}</sub> = {fmt(plain, 4)}.)"))
    ask = f"v<sub>{steps}</sub>" if ask_v else f"w<sub>{steps}</sub>"
    return Q(text=f"Gradient descent with (heavy-ball) momentum minimises f(w) = ({fmt(a)}/2)w² using "
                  f"v<sub>t</sub> = β v<sub>t−1</sub> + ∇f(w<sub>t−1</sub>) and w<sub>t</sub> = w<sub>t−1</sub> − η "
                  f"v<sub>t</sub>, with w<sub>0</sub> = {fmt(w0)}, v<sub>0</sub> = 0, η = {fmt(eta)}, β = {fmt(beta)}. "
                  f"The value of {ask} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1], solution=sol)


@template(TOPIC, S_TRN, marks=1, qtype="NAT")
def weight_decay(rng):
    v = int(rng.integers(3))
    eta = float(_pick(rng, [0.1, 0.01, 0.05, 0.2]))
    lam = float(_pick(rng, [0.1, 0.5, 1.0, 0.01, 2.0]))
    w = float(_halfgrid(rng, -3, 3))
    if v == 0:
        g = float(_halfgrid(rng, -2, 2, nonzero=False))
        val = w - eta * (g + lam * w)
        text = (f"A weight w = {fmt(w)} is trained on the regularised objective L(w) + (λ/2)w² with λ = {fmt(lam)}. "
                f"The data-loss gradient is ∂L/∂w = {fmt(g)}. After one gradient-descent step with η = {fmt(eta)}, "
                f"the new weight is ______ ")
        sol = [f"∇ = ∂L/∂w + λw = {fmt(g)} + {fmt(lam)}×{fmt(w)} = {fmt(g + lam * w, 4)}.",
               f"w ← {fmt(w)} − {fmt(eta)}×{fmt(g + lam * w, 4)} = <b>{fmt(val, 4)}</b>  "
               f"(equivalently (1 − ηλ)w − η∂L/∂w)."]
    elif v == 1:
        k = int(rng.integers(2, 6))
        val = w * (1 - eta * lam) ** k
        text = (f"With L2 weight decay (penalty (λ/2)w², λ = {fmt(lam)}) and learning rate η = {fmt(eta)}, a weight "
                f"w = {fmt(w)} receives zero data-loss gradient for {k} consecutive gradient-descent steps. Its value "
                f"after these {k} steps is ______ ")
        sol = [f"Each step: w ← w − ηλw = (1 − ηλ)w = {fmt(1 - eta * lam, 4)}·w.",
               f"After {k} steps: {fmt(w)} × {fmt(1 - eta * lam, 4)}<super>{k}</super> = <b>{fmt(val, 4)}</b>."]
    else:
        ws = _halfgrid(rng, -2, 2, 3).astype(float)
        val = lam / 2 * float(np.sum(ws ** 2))
        text = (f"A model has weights w = {vec(ws)}. The L2 penalty term (λ/2)‖w‖² with λ = {fmt(lam)} added to the "
                f"loss equals ______ ")
        sol = [f"‖w‖² = {' + '.join(fmt(x * x) for x in ws)} = {fmt(np.sum(ws ** 2))}; (λ/2)‖w‖² = "
               f"{fmt(lam / 2)}×{fmt(np.sum(ws ** 2))} = <b>{fmt(val, 4)}</b>."]
    return Q(text=text + _nat_auto(val)[1], qtype="NAT", marks=1, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             solution=sol)


@template(TOPIC, S_TRN, marks=1, qtype="NAT")
def dropout(rng):
    p = float(_pick(rng, [0.5, 0.8, 0.75, 0.9, 0.6]))
    v = int(rng.integers(4))
    if v == 0:
        h = float(_halfgrid(rng, 0.5, 4))
        val = h / p
        text = (f"Inverted dropout with keep probability p = {fmt(p)} is applied during training. A hidden unit with "
                f"activation h = {fmt(h)} that is <b>kept</b> passes on the value ______ ")
        sol = [f"Inverted dropout multiplies kept activations by 1/p so that E[output] = h: {fmt(h)}/{fmt(p)} = "
               f"<b>{fmt(val, 4)}</b>. No scaling is applied at test time."]
    elif v == 1:
        n = int(_pick(rng, [100, 200, 256, 512, 1000, 40]))
        val = n * (1 - p)
        text = (f"A layer of {n} units uses dropout with keep probability p = {fmt(p)}. The expected number of units "
                f"dropped (set to zero) in one forward pass during training is ______ ")
        sol = [f"Each unit is dropped independently with probability 1 − p = {fmt(1 - p)}; expected number = "
               f"{n}×{fmt(1 - p)} = <b>{fmt(val, 4)}</b>."]
    elif v == 2:
        w = _halfgrid(rng, -2, 2, 3).astype(float)
        h = _halfgrid(rng, 0.5, 3, 3).astype(float)
        val = p * float(w @ h)
        text = (f"In standard (non-inverted) dropout, each input h<sub>i</sub> of a unit is kept with probability "
                f"p = {fmt(p)} during training (and not rescaled). For h = {vec(h)} and weights w = {vec(w)}, the "
                f"expected value of the unit's pre-activation Σ w<sub>i</sub>m<sub>i</sub>h<sub>i</sub> (m<sub>i</sub> "
                f"~ Bernoulli(p)) during training is ______ ")
        sol = [f"E[m<sub>i</sub>] = p ⇒ E[Σ w<sub>i</sub>m<sub>i</sub>h<sub>i</sub>] = p Σ w<sub>i</sub>h<sub>i</sub> = "
               f"{fmt(p)} × {fmt(w @ h, 4)} = <b>{fmt(val, 4)}</b>.",
               "This is why, at test time, standard dropout scales the weights by p (inverted dropout instead scales "
               "by 1/p during training)."]
    else:
        w = float(_halfgrid(rng, -3, 3))
        val = p * w
        text = (f"A network is trained with standard (non-inverted) dropout, keep probability p = {fmt(p)}, on the "
                f"inputs of a layer. A trained outgoing weight equals {fmt(w)}. To match expected activations, the "
                f"weight used at test time is ______ ")
        sol = [f"During training each input is present with probability p, so at test time weights are scaled by p: "
               f"{fmt(p)}×{fmt(w)} = <b>{fmt(val, 4)}</b>."]
    return Q(text=text + nat_hint(2), qtype="NAT", marks=1, answer=nat_range(val, 2), nat_hint=nat_hint(2),
             solution=sol)


@template(TOPIC, S_TRN, marks=1, qtype="MCQ")
def lr_curves(rng):
    kinds = ["very_high", "high", "low", "good"]
    perm = rng.permutation(4)
    assign = [kinds[i] for i in perm]  # curve letter -> kind
    E = np.arange(0, 51)
    noise = rng.normal(0, 1, (4, len(E)))

    def curve(kind, nz):
        if kind == "very_high":
            return np.minimum(2.3 * np.exp(0.09 * E) + 0.02 * nz, 9.5)
        if kind == "high":
            return 0.9 + 1.4 * np.exp(-E / 2.0) + 0.04 * nz
        if kind == "low":
            return 2.3 - 0.022 * E + 0.015 * nz
        return 0.25 + 2.05 * np.exp(-E / 9.0) + 0.02 * nz

    curves = [curve(assign[i], noise[i]) for i in range(4)]
    target = _pick(rng, kinds)
    desc = {"very_high": "a learning rate that is far too high (training diverges)",
            "high": "a learning rate that is somewhat too high (fast initial drop, then the loss plateaus at a high "
                    "value)",
            "low": "a learning rate that is too low (very slow, almost linear decrease)",
            "good": "a well-chosen learning rate"}
    letters = "ABCD"
    k = assign.index(target)
    opts = [f"Curve {letters[i]}" for i in range(4)]
    styles = ["-", "--", "-.", ":"]

    def draw(fig):
        ax = fig.add_subplot(111)
        for i in range(4):
            ax.plot(E, curves[i], styles[i], color=GRAY[i % 3], lw=1.5, label=f"Curve {letters[i]}")
        ax.set_ylim(0, 4.5)
        ax.set_xlabel("epoch")
        ax.set_ylabel("training loss")
        ax.legend(loc="upper right", ncol=2, frameon=False)
        ax.grid(alpha=0.3)

    sol = ["Typical signatures: far-too-high η → loss blows up; somewhat-too-high η → quick drop then plateau at a "
           "high loss (bouncing around the minimum); too-low η → slow, nearly linear decrease; good η → fast "
           "decrease to the lowest loss."]
    for i in range(4):
        sol.append(f"Curve {letters[i]}: {desc[assign[i]]}.")
    sol.append(f"Hence the answer is <b>Curve {letters[k]}</b>.")
    return Q(text=f"The training-loss curves below were obtained with four different learning rates (everything else "
                  f"fixed). Which curve corresponds to {desc[target]}?",
             qtype="MCQ", marks=1, options=opts, answer=k, blocks=[Figure(draw, 8.5, 5.0)], solution=sol)


@template(TOPIC, S_TRN, marks=2, qtype="NAT")
def early_stopping(rng):
    while True:
        N = 20
        e0 = int(rng.integers(6, 13))
        ep = np.arange(1, N + 1)
        base = 0.45 + 1.2 * np.exp(-ep / 3.0) + 0.012 * np.maximum(0, ep - e0) ** 1.4
        val = np.round(base + rng.normal(0, 0.025, N), 3)
        train = np.round(0.1 + 1.5 * np.exp(-ep / 3.5) + rng.normal(0, 0.01, N), 3)
        if len(set(val)) < N:
            continue
        P = int(rng.integers(2, 6))
        best, best_e, wait, stop = np.inf, 0, 0, None
        for e, vl in zip(ep, val):
            if vl < best:
                best, best_e, wait = vl, e, 0
            else:
                wait += 1
                if wait == P:
                    stop = e
                    break
        if stop is None or stop < 6:
            continue
        break
    ask_stop = rng.random() < 0.5
    ans = stop if ask_stop else best_e
    rows1 = [["epoch"] + [str(e) for e in ep[:10]], ["val. loss"] + [f"{v:.3f}" for v in val[:10]]]
    rows2 = [["epoch"] + [str(e) for e in ep[10:]], ["val. loss"] + [f"{v:.3f}" for v in val[10:]]]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(ep, train, "o-", ms=2.5, color="#777777", lw=1.1, label="training loss")
        ax.plot(ep, val, "s-", ms=2.5, color="#111111", lw=1.3, label="validation loss")
        ax.set_xlabel("epoch")
        ax.set_ylabel("loss")
        ax.set_xticks(range(0, 21, 2))
        ax.legend(frameon=False)
        ax.grid(alpha=0.3)

    sol = [f"Rule: keep track of the best (lowest) validation loss; an epoch that does not strictly improve on it "
           f"increments a counter, which is reset on improvement; stop when the counter reaches patience P = {P}."]
    best, wait = np.inf, 0
    trace = []
    for e, vl in zip(ep, val):
        if vl < best:
            best, wait = vl, 0
            trace.append(f"{e}: {vl:.3f} (new best)")
        else:
            wait += 1
            trace.append(f"{e}: {vl:.3f} (no improvement, count = {wait})")
        if e == stop:
            break
    sol.append("Trace – " + "; ".join(trace) + ".")
    sol.append(f"Training stops after epoch {stop}; the best validation loss {val[best_e - 1]:.3f} occurred at "
               f"epoch {best_e}, whose weights are restored.")
    sol.append(f"Answer: <b>{ans}</b>. The widening train/validation gap after this point is the signature of "
               "overfitting.")
    q = ("the epoch after which training is stopped" if ask_stop
         else "the epoch whose weights are returned (restored) as the final model")
    return Q(text=f"A network is trained with early stopping on validation loss using patience P = {P}: training "
                  f"stops as soon as the validation loss has failed to improve on its best value for {P} consecutive "
                  f"epochs, and the weights from the best epoch are restored. Using the validation losses below "
                  f"(also plotted), {q} is ______ " + nat_hint(0),
             qtype="NAT", marks=2, answer=(float(ans), float(ans)), nat_hint=nat_hint(0),
             blocks=[Figure(draw, 8.5, 4.8), Table(rows1, header=False), Table(rows2, header=False)], solution=sol)


TR1_T = [
    ("Initialising all weights of an MLP to the same value makes the hidden units of a layer compute identical "
     "functions and receive identical updates, so they stay identical.", "The symmetry is never broken by GD."),
    ("Biases may be initialised to zero provided the weights are initialised randomly.",
     "Random weights already break the symmetry."),
    ("With penalty (λ/2)‖w‖² and SGD, each step first shrinks the weights by the factor (1 − ηλ) (weight decay).",
     "w ← w − η(∇L + λw) = (1 − ηλ)w − η∇L."),
    ("With inverted dropout (keep probability p), retained activations are scaled by 1/p during training, so no "
     "scaling is needed at test time.", "E[m·h/p] = h."),
    ("Early stopping acts as a regulariser.", "It limits how far the weights move from their initialisation."),
    ("Dropout is switched off at inference (test) time.", "The full network (appropriately scaled) is used."),
    ("Xavier/Glorot initialisation chooses the weight variance based on the layer's fan-in and fan-out to keep "
     "activation and gradient variances roughly constant across layers.", "Var(w) = 2/(fan_in + fan_out)."),
    ("He initialisation, with variance 2/fan_in, is designed for ReLU layers.",
     "The factor 2 compensates for ReLU zeroing half the inputs."),
    ("Increasing the L2 penalty λ generally increases bias and reduces variance.", "Stronger shrinkage."),
    ("Training loss decreasing while validation loss increases is a sign of overfitting.", "Generalisation gap grows."),
    ("Data augmentation can reduce overfitting.", "It effectively enlarges the training set."),
    ("An L1 penalty tends to drive some weights exactly to zero, unlike an L2 penalty.",
     "The L1 subgradient has constant magnitude λ."),
    ("Dropout can be interpreted as training an ensemble of exponentially many thinned sub-networks that share "
     "weights.", "Each mask defines a sub-network."),
]
TR1_F = [
    ("Initialising all weights of an MLP to zero is harmless because backpropagation breaks the symmetry.",
     "All hidden units get identical gradients; symmetry persists."),
    ("Dropout is applied at test time with freshly sampled random masks, exactly as during training.",
     "Dropout is disabled at test time (deterministic prediction)."),
    ("L2 regularisation tends to increase the magnitude of the weights.", "It shrinks weights towards 0."),
    ("Early stopping selects the epoch with the minimum training loss.", "It uses the validation loss."),
    ("Increasing the dropout rate always reduces the training error.",
     "More dropout adds noise and usually increases training error."),
    ("With inverted dropout (keep probability p), activations must additionally be multiplied by p at test time.",
     "The 1/p scaling during training already makes test-time scaling unnecessary."),
    ("Increasing the L2 penalty λ decreases the bias of the model.", "Shrinkage increases bias."),
    ("High training loss and high validation loss together indicate overfitting.", "That pattern is underfitting."),
    ("Adding more (representative) training data typically increases overfitting.", "More data reduces variance."),
    ("Initialising sigmoid networks with very large random weights helps avoid vanishing gradients.",
     "Large weights saturate the sigmoids, making gradients vanish."),
    ("A training error much lower than the validation error indicates underfitting.", "It indicates overfitting."),
    ("L2 weight decay sets many weights exactly to zero, giving sparse networks.",
     "L2 shrinks but rarely zeroes; L1 promotes sparsity."),
]


@template(TOPIC, S_TRN, marks=1, qtype="MSQ")
def train_concepts_reg(rng):
    opts, ans, expl = msq_from_statements(rng, TR1_T, TR1_F)
    return Q(text="Which of the following statements about initialisation and regularisation of neural networks "
                  "is/are CORRECT?", qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


TR2_T = [
    ("For classification with sigmoid/softmax outputs, cross-entropy loss gives the output gradient ŷ − y, avoiding "
     "the σ′ factor that slows MSE-based learning when outputs saturate.", "Gradient does not vanish when wrong and saturated."),
    ("Minimising cross-entropy loss is equivalent to maximising the log-likelihood of the labels under the model.",
     "CE = negative log-likelihood of a categorical/Bernoulli model."),
    ("Minimising the mean squared error corresponds to maximum likelihood under additive Gaussian noise with fixed "
     "variance.", "−log N(y; ŷ, σ²) ∝ (y − ŷ)²."),
    ("Too large a learning rate can make the training loss oscillate or diverge.", "Steps overshoot the minimum."),
    ("Too small a learning rate leads to very slow convergence.", "Tiny steps."),
    ("With uniformly sampled mini-batches, the mini-batch gradient is an unbiased estimate of the full-batch "
     "gradient.", "Its expectation equals the average gradient."),
    ("Momentum accumulates an exponentially decaying average of past gradients, which damps oscillations across "
     "steep directions.", "Opposite-sign components cancel."),
    ("The number of parameter updates in one epoch of mini-batch training is ⌈N/B⌉ (keeping the last partial batch).",
     "One update per mini-batch."),
    ("Increasing the batch size reduces the variance of the gradient estimate.", "Variance ∝ 1/B."),
    ("For f(w) = (a/2)w² with a &gt; 0, gradient descent converges for every starting point iff 0 &lt; η &lt; 2/a.",
     "w<sub>t</sub> = (1 − ηa)<super>t</super>w<sub>0</sub>."),
    ("With momentum β (v ← βv + g, w ← w − ηv) and a constant gradient g, the step size approaches ηg/(1 − β).",
     "Geometric series 1 + β + β² + …"),
    ("The training loss of an MLP with hidden layers is in general non-convex in its weights.",
     "E.g. permuting hidden units gives equivalent minima."),
    ("Decaying the learning rate during training can help SGD settle closer to a minimum.",
     "Reduces the noise floor of SGD."),
]
TR2_F = [
    ("For classification with a sigmoid output, MSE loss is convex in the weights and is therefore preferred over "
     "cross-entropy.", "MSE∘σ is non-convex; CE is the standard choice."),
    ("Cross-entropy loss can be negative when the predicted probabilities are valid.", "−log p ≥ 0 for p ∈ (0, 1]."),
    ("One epoch of mini-batch SGD consists of exactly one parameter update.", "It has ⌈N/B⌉ updates."),
    ("Increasing the batch size increases the number of parameter updates per epoch.", "Fewer batches → fewer updates."),
    ("Momentum guarantees convergence to the global minimum of a neural network's loss.", "No such guarantee."),
    ("Gradient descent with a fixed learning rate decreases the training loss at every step regardless of η.",
     "Large η can increase the loss."),
    ("The training loss of an MLP is convex in its weights, so every local minimum is global.",
     "It is non-convex."),
    ("Binary cross-entropy for a positive example is minimised when the predicted probability is 0.5.",
     "It is minimised as p → 1."),
    ("Doubling the learning rate always halves the number of epochs needed to converge.",
     "It may even cause divergence."),
    ("With momentum β = 0.9 and a constant gradient g, the step size eventually becomes 0.1ηg.",
     "It approaches ηg/(1 − β) = 10ηg."),
    ("Mini-batch gradient descent with batch size B = N is the same as single-example SGD.",
     "B = N is full-batch gradient descent."),
    ("Using MSE loss for a classification network makes training by backpropagation impossible.",
     "It is possible, just usually slower/worse."),
    ("For f(w) = (a/2)w², gradient descent converges for any learning rate η &lt; 4/a.",
     "It diverges for η &gt; 2/a."),
]


@template(TOPIC, S_TRN, marks=2, qtype="MSQ")
def train_concepts_opt(rng):
    opts, ans, expl = msq_from_statements(rng, TR2_T, TR2_F)
    return Q(text="Which of the following statements about loss functions and optimisation for training neural "
                  "networks is/are CORRECT?", qtype="MSQ", marks=2, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_TRN, marks=2, qtype="NAT")
def zero_init(rng):
    while True:
        c = float(_pick(rng, [0.5, 0.25, 1.0, -0.5, 0.2]))
        x = _halfgrid(rng, -2, 2, 2).astype(float)
        y = float(_halfgrid(rng, -1, 2, nonzero=False))
        eta = float(_pick(rng, [0.1, 0.5, 1.0]))
        a = c * (x[0] + x[1])
        h = _sig(a)
        yh = 2 * c * h
        e = yh - y
        if abs(e) < 0.2:
            continue
        break
    j = int(rng.integers(2))
    k = int(rng.integers(2))
    var = int(rng.integers(5))
    gW = e * c * h * (1 - h) * x[k]
    gv = e * h
    if var <= 2:
        val = c - eta * gW
        ask = f"the updated value of w<sub>{j + 1}{k + 1}</sub> (weight from x<sub>{k + 1}</sub> to h<sub>{j + 1}</sub>)"
    elif var == 3:
        val = c - eta * gv
        ask = f"the updated value of the output weight v<sub>{j + 1}</sub>"
    else:
        val = 0.0
        ask = (f"w<sub>1{k + 1}</sub> − w<sub>2{k + 1}</sub> after the update (difference between the weights from "
               f"x<sub>{k + 1}</sub> into the two hidden units)")

    def draw(fig):
        el = {(0, i, jj): fmt(c) for i in range(2) for jj in range(2)}
        el.update({(1, i, 0): fmt(c) for i in range(2)})
        _draw_net(fig, [2, 2, 1], [["$x_1$", "$x_2$"], ["$h_1$", "$h_2$"], ["$\\hat{y}$"]], el, None,
                  ["input", "hidden (sigmoid)", "output (linear)"], t_edge=[0.3, 0.45],
                  input_values=[fmt(x[0]), fmt(x[1])])

    sol = [f"All weights = {fmt(c)}, biases 0 ⇒ both hidden units get a = {fmt(c)}×({fmt(x[0])} + {fmt(x[1])}) = "
           f"{fmt(a, 4)}, h<sub>1</sub> = h<sub>2</sub> = σ(a) = {fmt(h, 4)}; ŷ = 2×{fmt(c)}×{fmt(h, 4)} = {fmt(yh, 4)}.",
           f"ŷ − y = {fmt(e, 4)}. ∂L/∂v<sub>j</sub> = (ŷ − y)h<sub>j</sub> = {fmt(gv, 4)} (same for both j).",
           f"∂L/∂w<sub>jk</sub> = (ŷ − y) v<sub>j</sub> h<sub>j</sub>(1 − h<sub>j</sub>) x<sub>k</sub> = {fmt(e, 4)}×"
           f"{fmt(c)}×{fmt(h * (1 - h), 4)}×{fmt(x[k])} = {fmt(gW, 4)} (identical for j = 1, 2)."]
    if var <= 2:
        sol.append(f"w<sub>{j + 1}{k + 1}</sub> ← {fmt(c)} − {fmt(eta)}×({fmt(gW, 4)}) = <b>{fmt(val, 4)}</b>.")
    elif var == 3:
        sol.append(f"v<sub>{j + 1}</sub> ← {fmt(c)} − {fmt(eta)}×({fmt(gv, 4)}) = <b>{fmt(val, 4)}</b>.")
    else:
        sol.append("Both hidden units receive identical gradients, so the difference stays <b>0</b>.")
    sol.append("Because the two hidden units start identical and get identical updates, they remain identical forever "
               "(symmetry problem) – hence weights must be initialised randomly.")
    return Q(text=f"In the 2-2-1 network below (sigmoid hidden units, linear output ŷ = v<sub>1</sub>h<sub>1</sub> + "
                  f"v<sub>2</sub>h<sub>2</sub>, all biases 0), <b>every</b> weight is initialised to {fmt(c)}. One "
                  f"gradient-descent step with η = {fmt(eta)} is taken on L = ½(ŷ − y)² for the input "
                  f"x = ({fmt(x[0])}, {fmt(x[1])}) with target y = {fmt(y)}. Then {ask} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Figure(draw, 8.5, 5.3)], solution=sol)


@template(TOPIC, S_TRN, marks=2, qtype="MSQ")
def lr_quadratic(rng):
    while True:
        a1 = int(_pick(rng, [1, 2, 4, 5, 8, 10]))
        a2 = int(_pick(rng, [1, 2, 4, 5, 8, 10]))
        if a1 == a2:
            continue
        amax = max(a1, a2)
        cands = sorted({round(m / amax, 4) for m in (0.3, 0.5, 0.8, 1.2, 1.5, 1.9, 2.2, 2.6, 3.0)})
        etas = list(rng.choice(cands, 4, replace=False))
        variant = int(rng.integers(2))
        rates = [max(abs(1 - e * a1), abs(1 - e * a2)) for e in etas]
        if any(abs(r - 1) < 0.05 for r in rates):
            continue
        conv = [r < 1 for r in rates]
        truth = conv if variant == 0 else [not c for c in conv]
        if any(truth):
            break
    opts = [f"η = {fmt(e, 4)}" for e in etas]
    ans = [i for i in range(4) if truth[i]]

    def draw(fig):
        ax = fig.add_subplot(111)
        g = np.linspace(-2, 2, 200)
        G1, G2 = np.meshgrid(g, g)
        F = 0.5 * (a1 * G1 ** 2 + a2 * G2 ** 2)
        cs = ax.contour(G1, G2, F, levels=6, colors="#444444", linewidths=0.8)
        ax.clabel(cs, fontsize=6, fmt="%.1f")
        ax.set_xlabel("w₁")
        ax.set_ylabel("w₂")
        ax.set_aspect("equal")
        ax.set_title("contours of f(w₁, w₂)", fontsize=7.5)

    sol = [f"∇f = ({a1}w₁, {a2}w₂) ⇒ w<sub>i</sub> ← (1 − η a<sub>i</sub>) w<sub>i</sub>. GD converges (from every "
           f"start) iff |1 − η a<sub>i</sub>| &lt; 1 for both i, i.e. 0 &lt; η &lt; 2/max(a<sub>i</sub>) = "
           f"2/{amax} = {fmt(2 / amax, 4)}. The steep direction (a = {amax}) limits the learning rate."]
    for i, e in enumerate(etas):
        sol.append(f"<b>({'ABCD'[i]}) {'TRUE' if truth[i] else 'FALSE'}.</b> η = {fmt(e, 4)}: |1 − η·{a1}| = "
                   f"{fmt(abs(1 - e * a1), 3)}, |1 − η·{a2}| = {fmt(abs(1 - e * a2), 3)} → "
                   + ("converges." if conv[i] else "diverges."))
    want = "converge to the minimum" if variant == 0 else "diverge"
    return Q(text=f"Gradient descent w ← w − η∇f(w) is applied to f(w₁, w₂) = ½({a1}w₁² + {a2}w₂²) from a generic "
                  f"starting point (both coordinates non-zero). For which of the following learning rates does GD "
                  f"<b>{want}</b>?",
             qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[Figure(draw, 6, 5)], solution=sol)


@template(TOPIC, S_TRN, marks=1, qtype="NAT")
def ce_loss_value(rng):
    v = int(rng.integers(2))
    if v == 0:
        n = 3
        P = []
        for _ in range(n):
            raw = _pick(rng, [(0.7, 0.2, 0.1), (0.5, 0.3, 0.2), (0.6, 0.3, 0.1), (0.4, 0.4, 0.2), (0.8, 0.1, 0.1),
                              (0.25, 0.25, 0.5), (0.9, 0.05, 0.05)])
            P.append(list(rng.permutation(raw)))
        P = np.array(P)
        yl = rng.integers(0, 3, n)
        ps = P[np.arange(n), yl]
        val = float(-np.mean(np.log(ps)))
        rows = [["example", "p(class 1)", "p(class 2)", "p(class 3)", "true class"]] + [
            [str(i + 1)] + [fmt(x) for x in P[i]] + [str(yl[i] + 1)] for i in range(n)]
        text = ("A 3-class softmax classifier gives the predicted probabilities below for a mini-batch of 3 examples. "
                "The mean categorical cross-entropy loss (natural log) over the mini-batch is ______ ")
        sol = ["CE for one example = −ln p<sub>true class</sub>."] + [
            f"Example {i + 1}: −ln {fmt(ps[i])} = {fmt(-np.log(ps[i]), 4)}." for i in range(n)] + [
            f"Mean = <b>{fmt(val, 4)}</b>."]
    else:
        n = 4
        p = rng.choice([0.9, 0.8, 0.7, 0.6, 0.4, 0.3, 0.2, 0.1], n)
        yl = rng.integers(0, 2, n)
        terms = -(yl * np.log(p) + (1 - yl) * np.log(1 - p))
        val = float(terms.mean())
        rows = [["example", "p = P(y = 1)", "y"]] + [[str(i + 1), fmt(p[i]), str(yl[i])] for i in range(n)]
        text = ("A sigmoid-output classifier gives the probabilities p = P(y = 1 | x) below. The mean binary "
                "cross-entropy −[y ln p + (1 − y) ln(1 − p)] over the 4 examples is ______ ")
        sol = [f"Example {i + 1}: " + (f"y = 1 → −ln {fmt(p[i])}" if yl[i] else f"y = 0 → −ln(1 − {fmt(p[i])})")
               + f" = {fmt(terms[i], 4)}." for i in range(n)] + [f"Mean = <b>{fmt(val, 4)}</b>."]
    return Q(text=text + _nat_auto(val)[1], qtype="NAT", marks=1, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[Table(rows)], solution=sol)


# ============================================================================
# SOFTMAX + CROSS-ENTROPY
# ============================================================================
@template(TOPIC, S_SMX, marks=2, qtype="NAT")
def smx_ce_grad(rng):
    K = int(rng.integers(3, 5))
    while True:
        z = _halfgrid(rng, -2, 2, K, nonzero=False).astype(float)
        if len(set(z)) >= K - 1 and np.ptp(z) > 0.5:
            break
    c = int(rng.integers(K))
    p = _softmax(z)
    yv = np.zeros(K)
    yv[c] = 1
    g = p - yv
    var = int(rng.integers(4))
    k = int(rng.integers(K))
    eta = float(_pick(rng, [0.5, 1.0, 0.1]))
    if var == 0:
        val = -math.log(p[c])
        ask = "the cross-entropy loss L = −ln p<sub>y</sub> (natural log)"
    elif var == 1:
        val = g[k]
        ask = f"∂L/∂z<sub>{k + 1}</sub>"
    elif var == 2:
        val = z[k] - eta * g[k]
        ask = f"the value of z<sub>{k + 1}</sub> after one gradient step on the logits with η = {fmt(eta)}"
    else:
        val = float(np.linalg.norm(g))
        ask = "the Euclidean norm ‖∂L/∂z‖ of the gradient with respect to the logit vector"
    zs = ", ".join(fmt(x) for x in z)
    sol = ["p = softmax(z): exp(z) = " + vec(np.exp(z), 4) + f", sum = {fmt(np.exp(z).sum(), 4)}, so p = {vec(p, 4)}.",
           f"For L = −ln p<sub>y</sub> with softmax, ∂L/∂z = p − y (y one-hot, true class {c + 1}): "
           f"∂L/∂z = {vec(g, 4)}."]
    if var == 0:
        sol.append(f"L = −ln {fmt(p[c], 4)} = <b>{fmt(val, 4)}</b>.")
    elif var == 1:
        sol.append(f"∂L/∂z<sub>{k + 1}</sub> = p<sub>{k + 1}</sub> − y<sub>{k + 1}</sub> = {fmt(p[k], 4)} − "
                   f"{int(yv[k])} = <b>{fmt(val, 4)}</b>" + (" (negative for the true class: increasing its logit "
                                                              "lowers the loss)." if k == c else "."))
    elif var == 2:
        sol.append(f"z<sub>{k + 1}</sub> ← {fmt(z[k])} − {fmt(eta)}×({fmt(g[k], 4)}) = <b>{fmt(val, 4)}</b>.")
    else:
        sol.append(f"‖p − y‖ = √({' + '.join(fmt(x * x, 4) for x in g)}) = <b>{fmt(val, 4)}</b>.")
    sol.append("Note Σ<sub>k</sub> ∂L/∂z<sub>k</sub> = Σp<sub>k</sub> − 1 = 0.")
    return Q(text=f"A {K}-class classifier outputs logits z = ({zs}) and probabilities p = softmax(z). The true class "
                  f"is {c + 1}, and the loss is the cross-entropy L = −ln p<sub>{c + 1}</sub>. Then {ask} is ______ "
                  + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1], solution=sol)


@template(TOPIC, S_SMX, marks=2, qtype="NAT")
def smx_weight_grad(rng):
    while True:
        W = _halfgrid(rng, -1, 1, (3, 2), nonzero=False).astype(float)
        b = _halfgrid(rng, -0.5, 0.5, 3, nonzero=False).astype(float)
        x = _ints(rng, -2, 2, 2, nonzero=True).astype(float)
        z = W @ x + b
        if np.ptp(z) < 0.5:
            continue
        break
    c = int(rng.integers(3))
    p = _softmax(z)
    yv = np.zeros(3)
    yv[c] = 1
    d = p - yv
    k = int(rng.integers(3))
    j = int(rng.integers(2))
    var = int(rng.integers(3))
    eta = float(_pick(rng, [0.1, 0.5, 1.0]))
    if var == 0:
        val = d[k] * x[j]
        ask = f"∂L/∂W<sub>{k + 1}{j + 1}</sub>"
    elif var == 1:
        val = d[k]
        ask = f"∂L/∂b<sub>{k + 1}</sub>"
    else:
        val = W[k, j] - eta * d[k] * x[j]
        ask = f"the updated W<sub>{k + 1}{j + 1}</sub> after one gradient-descent step with η = {fmt(eta)}"
    sol = [f"z = Wx + b = {vec(z, 4)}; p = softmax(z) = {vec(p, 4)}.",
           f"δ = ∂L/∂z = p − y = {vec(d, 4)} (true class {c + 1}).",
           "Since z<sub>k</sub> = Σ<sub>j</sub> W<sub>kj</sub>x<sub>j</sub> + b<sub>k</sub>: ∂L/∂W<sub>kj</sub> = "
           "(p<sub>k</sub> − y<sub>k</sub>) x<sub>j</sub> and ∂L/∂b<sub>k</sub> = p<sub>k</sub> − y<sub>k</sub> "
           "(gradient matrix = (p − y)xᵀ)."]
    if var == 0:
        sol.append(f"∂L/∂W<sub>{k + 1}{j + 1}</sub> = {fmt(d[k], 4)} × {fmt(x[j])} = <b>{fmt(val, 4)}</b>.")
    elif var == 1:
        sol.append(f"∂L/∂b<sub>{k + 1}</sub> = <b>{fmt(val, 4)}</b>.")
    else:
        sol.append(f"W<sub>{k + 1}{j + 1}</sub> ← {fmt(W[k, j])} − {fmt(eta)}×{fmt(d[k], 4)}×{fmt(x[j])} = "
                   f"<b>{fmt(val, 4)}</b>.")
    return Q(text=f"A softmax-regression output layer computes z = Wx + b, p = softmax(z) with W and b below, and is "
                  f"trained with cross-entropy loss L = −ln p<sub>y</sub>. For x = ({fmt(x[0])}, {fmt(x[1])})ᵀ with "
                  f"true class y = {c + 1}, {ask} is ______ " + _nat_auto(val)[1],
             qtype="NAT", marks=2, answer=_nat_auto(val)[0], nat_hint=_nat_auto(val)[1],
             blocks=[_M("W", W), _M("b", b)], solution=sol)


SMX_T = [
    ("For softmax outputs with cross-entropy loss and one-hot target y, ∂L/∂z = p − y.", "Standard result."),
    ("The components of ∂L/∂z for softmax + cross-entropy sum to zero.", "Σ(p<sub>k</sub> − y<sub>k</sub>) = 1 − 1."),
    ("For softmax + cross-entropy, the gradient with respect to the true-class logit is negative unless "
     "p<sub>y</sub> = 1.", "p<sub>y</sub> − 1 &lt; 0."),
    ("Adding the same constant to all logits leaves the softmax output and the cross-entropy loss unchanged.",
     "Shift invariance."),
    ("Cross-entropy loss −ln p<sub>y</sub> is 0 only when p<sub>y</sub> = 1.", "−ln 1 = 0."),
    ("For a confidently wrong prediction (p<sub>y</sub> → 0), the cross-entropy loss grows without bound.",
     "−ln p<sub>y</sub> → ∞."),
    ("Softmax with two classes is equivalent to a sigmoid applied to the logit difference.", "p₁ = σ(z₁ − z₂)."),
    ("Subtracting max(z) from all logits before exponentiating is a standard trick for numerical stability.",
     "Avoids overflow without changing the output."),
    ("For softmax + cross-entropy, ∂L/∂z<sub>k</sub> for a wrong class k equals p<sub>k</sub> (which is positive).",
     "y<sub>k</sub> = 0."),
    ("The Jacobian of softmax is ∂p<sub>i</sub>/∂z<sub>j</sub> = p<sub>i</sub>(δ<sub>ij</sub> − p<sub>j</sub>).",
     "Standard derivative."),
]
SMX_F = [
    ("For softmax + cross-entropy, ∂L/∂z = y − p.", "Sign is reversed: it is p − y."),
    ("Multiplying all logits by 2 leaves the softmax probabilities unchanged.", "It sharpens the distribution."),
    ("For softmax + cross-entropy, the gradient of a wrong-class logit is negative.",
     "It is p<sub>k</sub> &gt; 0, so GD lowers wrong-class logits."),
    ("The cross-entropy loss −ln p<sub>y</sub> can be negative.", "p<sub>y</sub> ≤ 1 ⇒ −ln p<sub>y</sub> ≥ 0."),
    ("Softmax outputs can be negative when logits are negative.", "exp(·) &gt; 0 always."),
    ("The softmax Jacobian is diagonal, so each p<sub>i</sub> depends only on z<sub>i</sub>.",
     "Off-diagonal terms −p<sub>i</sub>p<sub>j</sub> are non-zero."),
    ("For softmax + cross-entropy, ∂L/∂z<sub>k</sub> = (p<sub>k</sub> − y<sub>k</sub>) p<sub>k</sub>(1 − p<sub>k</sub>).",
     "The extra factor would appear only for an MSE-type loss on a sigmoid; it cancels here."),
    ("Cross-entropy loss is maximised when the model predicts the correct class with probability 1.",
     "It is minimised (= 0) there."),
    ("The sum of the softmax probabilities depends on the scale of the logits.", "It always equals 1."),
]


@template(TOPIC, S_SMX, marks=1, qtype="MSQ")
def smx_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, SMX_T, SMX_F)
    return Q(text="Let p = softmax(z) for logits z ∈ ℝ<super>K</super> and L = −ln p<sub>y</sub> the cross-entropy loss "
                  "for true class y. Which of the following is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_SMX, marks=2, qtype="MCQ")
def smx_grad_mcq(rng):
    while True:
        z = _ints(rng, -1, 2, 3).astype(float)
        if len(set(z)) == 3:
            break
    c = int(rng.integers(3))
    p = _softmax(z)
    y = np.zeros(3)
    y[c] = 1
    corr = vec(p - y, 2)
    d = [vec(y - p, 2), vec(p, 2), vec((p - y) * p * (1 - p), 2), vec(p - 1, 2), vec(-y / p, 2)]
    opts, ans = mcq(rng, corr, d)
    sol = [f"p = softmax({vec(z, 0)}) = {vec(p, 4)}; y = {vec(y, 0)}.",
           f"∂L/∂z = p − y = <b>{corr}</b>.",
           f"Distractors: y − p = {vec(y - p, 2)} (wrong sign); p alone = {vec(p, 2)} (forgot the target); "
           f"(p − y)⊙p⊙(1 − p) = {vec((p - y) * p * (1 - p), 2)} (spurious σ′-type factor, which cancels for "
           f"cross-entropy); −y/p = {vec(-y / p, 2)} is ∂L/∂p, not ∂L/∂z."]
    return Q(text=f"For logits z = {vec(z, 0)}, softmax probabilities p and true class {c + 1}, the gradient of the "
                  f"cross-entropy loss L = −ln p<sub>{c + 1}</sub> with respect to z (rounded to two decimals) is",
             qtype="MCQ", marks=2, options=opts, answer=ans, solution=sol)
