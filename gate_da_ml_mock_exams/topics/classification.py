"""Probabilistic & instance-based classifiers: logistic regression, k-NN, naive Bayes, LDA/QDA,
Bayes-optimal decisions and classification evaluation metrics."""
import math
from fractions import Fraction

import numpy as np

from core import (Figure, Matrix, Q, Table, fmt, mcq, mcq_numeric, msq_from_statements, nat_hint, nat_range,
                  template)

TOPIC = "Probabilistic & Instance-based Classifiers"
LR = "Logistic regression"
KNN = "k-nearest neighbours"
NB = "Naive Bayes"
LDA = "Linear discriminant analysis"
BAYES = "Bayes optimal classifier"
MET = "Evaluation metrics"

DARK = "#222222"
MID = "#777777"
LIGHT = "#bbbbbb"


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _sig(z):
    return 1.0 / (1.0 + math.exp(-z))


def _pick(rng, seq):
    return seq[int(rng.integers(len(seq)))]


def _msq_build(rng, items):
    """items: list of 4 (statement, truth, explanation). Shuffles; returns opts, ans, expl."""
    perm = rng.permutation(len(items))
    items = [items[i] for i in perm]
    opts, ans, expl = [], [], []
    for j, (s, ok, ex) in enumerate(items):
        opts.append(s)
        if ok:
            ans.append(j)
        expl.append(f"<b>({'ABCD'[j]}) {'TRUE' if ok else 'FALSE'}.</b> {ex}")
    return opts, ans, expl


def _dist(X, q, metric):
    D = np.asarray(X, float) - np.asarray(q, float)
    if metric == "E":
        return np.sqrt((D ** 2).sum(axis=1))
    return np.abs(D).sum(axis=1)


def _dist_str(X, q, metric, i):
    dx, dy = X[i][0] - q[0], X[i][1] - q[1]
    if metric == "E":
        s2 = dx * dx + dy * dy
        return f"√{fmt(s2, 2)} = {fmt(math.sqrt(s2), 3)}"
    return f"{fmt(abs(dx), 2)} + {fmt(abs(dy), 2)} = {fmt(abs(dx) + abs(dy), 2)}"


METRIC_NAME = {"E": "Euclidean", "M": "Manhattan (L<sub>1</sub>)"}


def _scatter_classes(ax, X, lab, names=("A", "B"), annotate=None):
    X = np.asarray(X, float)
    lab = np.asarray(lab)
    m0 = lab == 0
    ax.scatter(X[m0, 0], X[m0, 1], s=38, marker="o", color=DARK, zorder=3, label=f"class {names[0]}")
    ax.scatter(X[~m0, 0], X[~m0, 1], s=44, marker="^", facecolor="white", edgecolor=DARK, linewidth=1.2,
               zorder=3, label=f"class {names[1]}")
    if annotate is not None:
        for i, (a, b) in enumerate(X):
            ax.annotate(annotate[i], (a, b), xytext=(4, 4), textcoords="offset points", fontsize=6.5, color=MID)


def _gauss(x, mu, var):
    return math.exp(-(x - mu) ** 2 / (2 * var)) / math.sqrt(2 * math.pi * var)


# =============================================================================
# LOGISTIC REGRESSION
# =============================================================================
@template(TOPIC, LR, marks=1, qtype="NAT")
def lr_probability(rng):
    var = int(rng.integers(3))
    if var < 2:
        while True:
            w = rng.choice(np.arange(-4, 5) * 0.5, 2)
            b = float(rng.choice(np.arange(-6, 7) * 0.5))
            x = rng.integers(-3, 4, 2).astype(float)
            if w[0] == 0 or w[1] == 0:
                continue
            z = b + float(w @ x)
            if 0.2 <= abs(z) <= 3.2:
                break
        p1 = _sig(z)
        if var == 0:
            ask, ans = "P(y = 1 | <b>x</b>)", p1
            form = (f"P(y = 1 | <b>x</b>) = σ(w<sub>0</sub> + w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub>) "
                    f"with w<sub>0</sub> = {fmt(b)}, w<sub>1</sub> = {fmt(w[0])}, w<sub>2</sub> = {fmt(w[1])}, "
                    f"where σ(z) = 1/(1 + e<super>−z</super>)")
        else:
            ask, ans = "P(y = 0 | <b>x</b>)", 1 - p1
            form = (f"ln[ P(y=1|<b>x</b>) / P(y=0|<b>x</b>) ] = {fmt(b)} + ({fmt(w[0])})x<sub>1</sub> + "
                    f"({fmt(w[1])})x<sub>2</sub>")
        text = (f"A binary logistic regression model is given by {form}. For the input "
                f"<b>x</b> = (x<sub>1</sub>, x<sub>2</sub>) = ({fmt(x[0])}, {fmt(x[1])}), the value of {ask} is ______")
        sol = [f"z = w<sub>0</sub> + w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> = {fmt(b)} + "
               f"({fmt(w[0])})({fmt(x[0])}) + ({fmt(w[1])})({fmt(x[1])}) = {fmt(z, 3)} (this is the log-odds).",
               f"P(y = 1 | <b>x</b>) = σ(z) = 1/(1 + e<super>{fmt(-z, 3)}</super>) = {fmt(p1, 4)}."]
        if var == 1:
            sol.append(f"P(y = 0 | <b>x</b>) = 1 − σ(z) = σ(−z) = <b>{fmt(ans, 2)}</b>.")
        else:
            sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    else:
        p0 = float(_pick(rng, [0.2, 0.25, 0.3, 0.4, 0.6, 0.7, 0.75, 0.8]))
        w1 = float(_pick(rng, [-1.5, -1, -0.5, 0.5, 1, 1.5]))
        dlt = int(rng.integers(1, 3))
        L0 = math.log(p0 / (1 - p0))
        z = L0 + dlt * w1
        ans = _sig(z)
        text = (f"In a logistic regression model, the coefficient of feature x<sub>1</sub> is β<sub>1</sub> = {fmt(w1)}. "
                f"For a certain input the model gives P(y = 1 | <b>x</b>) = {fmt(p0)}. If x<sub>1</sub> is increased by "
                f"{dlt} unit{'s' if dlt > 1 else ''} with all other features unchanged, the new value of P(y = 1 | <b>x</b>) "
                f"is ______")
        sol = [f"Work on the log-odds scale, which is linear in x<sub>1</sub>.",
               f"Old log-odds = ln({fmt(p0)}/{fmt(1 - p0)}) = {fmt(L0, 4)}.",
               f"New log-odds = {fmt(L0, 4)} + {dlt}×({fmt(w1)}) = {fmt(z, 4)}.",
               f"New probability = σ({fmt(z, 4)}) = <b>{fmt(ans, 2)}</b>.",
               "Note: the probability does NOT change by β<sub>1</sub>×Δx; only the log-odds does."]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


FEATS_ODDS = [("hours of study", "passing the exam"), ("age (years)", "having the disease"),
              ("number of prior purchases", "buying the product"), ("credit score (in 10s)", "loan approval"),
              ("dose (mg)", "a positive response"), ("number of links in an email", "the email being spam")]


@template(TOPIC, LR, marks=1, qtype="MCQ")
def lr_odds_ratio(rng):
    feat, ev = _pick(rng, FEATS_ODDS)
    var = int(rng.integers(3))
    if var == 0:
        beta = float(_pick(rng, [0.2, 0.3, 0.4, 0.5, 0.7, -0.3, -0.5, -0.7, 0.25, 0.6]))
        dx = int(rng.integers(1, 4))
        val = math.exp(beta * dx)
        opts, a = mcq_numeric(rng, val, 2, [beta * dx, math.exp(beta), 1 + beta * dx, _sig(beta * dx),
                                            math.exp(beta) * dx])
        text = (f"In a logistic regression model for the probability of {ev}, the coefficient of <i>{feat}</i> is "
                f"β = {fmt(beta)}. Holding all other features fixed, increasing <i>{feat}</i> by {dx} "
                f"unit{'s' if dx > 1 else ''} multiplies the <b>odds</b> of {ev} by (approximately)")
        sol = [f"log-odds = β<sub>0</sub> + βx + …, so Δ(log-odds) = β·Δx = {fmt(beta)}×{dx} = {fmt(beta * dx)}.",
               f"Odds are multiplied by e<super>βΔx</super> = e<super>{fmt(beta * dx)}</super> = <b>{fmt(val, 2)}</b>.",
               "Distractors: β·Δx is the change in log-odds (not a multiplier); e<super>β</super> ignores Δx; σ(βΔx) "
               "is a probability, not an odds ratio."]
    elif var == 1:
        R = float(_pick(rng, [1.5, 2.0, 2.5, 3.0, 0.5, 0.8, 1.2, 4.0, 0.25]))
        val = math.log(R)
        opts, a = mcq_numeric(rng, val, 2, [R, math.log10(R), 1 / R, R - 1, _sig(R)])
        text = (f"A fitted logistic regression model reports that each one-unit increase in <i>{feat}</i> multiplies the "
                f"odds of {ev} by {fmt(R)} (other features fixed). The coefficient of <i>{feat}</i> in the model is")
        sol = [f"Odds ratio for a unit increase = e<super>β</super> = {fmt(R)} ⇒ β = ln {fmt(R)} = <b>{fmt(val, 2)}</b>.",
               "Distractors: the odds ratio itself, log<sub>10</sub>, or 1/R are common slips; the model is linear in "
               "the <i>natural</i> log-odds."]
    else:
        beta = float(_pick(rng, [0.1, 0.2, 0.3, 0.4, -0.2, -0.4, 0.15, -0.1, 0.5]))
        val = 100 * (math.exp(beta) - 1)
        opts, a = mcq_numeric(rng, val, 1, [100 * beta, 100 * math.exp(beta), 100 * _sig(beta),
                                            100 * (1 - math.exp(-beta))], unit="%")
        text = (f"In a logistic regression model for {ev}, the coefficient of <i>{feat}</i> is β = {fmt(beta)}. "
                f"A one-unit increase in <i>{feat}</i> (others fixed) changes the odds of {ev} by approximately")
        sol = [f"Odds multiply by e<super>β</super> = e<super>{fmt(beta)}</super> = {fmt(math.exp(beta), 4)}.",
               f"Percentage change = 100(e<super>β</super> − 1)% = <b>{fmt(val, 1)}%</b>.",
               "100β% is only a small-β approximation; 100e<super>β</super>% is the new odds as a percentage of the "
               "old odds, not the change."]
    return Q(text=text, qtype="MCQ", marks=1, options=opts, answer=a, solution=sol)


@template(TOPIC, LR, marks=1, qtype="NAT")
def lr_softmax_logits(rng):
    while True:
        K = int(rng.integers(3, 5))
        z = rng.integers(-2, 4, K).astype(float)
        if z.max() - z.min() <= 4 and len(set(z)) >= 2:
            break
    p = np.exp(z) / np.exp(z).sum()
    var = int(rng.integers(3))
    names = ", ".join(f"z<sub>{i + 1}</sub> = {fmt(v)}" for i, v in enumerate(z))
    if var < 2:
        k = int(rng.integers(K))
        ans = p[k]
        text = (f"A {K}-class softmax classifier produces the logits {names} for an input <b>x</b>. "
                f"The predicted probability of class {k + 1}, P(y = {k + 1} | <b>x</b>), is ______")
        sol = [f"softmax: P(y = k | <b>x</b>) = e<super>z<sub>k</sub></super> / Σ<sub>j</sub> e<super>z<sub>j</sub></super>.",
               "e<super>z</super> values: " + ", ".join(fmt(math.exp(v), 4) for v in z) +
               f"; sum = {fmt(np.exp(z).sum(), 4)}.",
               f"P(y = {k + 1} | <b>x</b>) = {fmt(math.exp(z[k]), 4)}/{fmt(np.exp(z).sum(), 4)} = <b>{fmt(ans, 2)}</b>."]
    else:
        i, j = rng.choice(K, 2, replace=False)
        while z[i] == z[j]:
            i, j = rng.choice(K, 2, replace=False)
        ans = math.exp(z[i] - z[j])
        text = (f"A {K}-class softmax classifier produces the logits {names} for an input <b>x</b>. "
                f"The ratio P(y = {i + 1} | <b>x</b>) / P(y = {j + 1} | <b>x</b>) is ______")
        sol = ["The normalising constant Σe<super>z<sub>j</sub></super> cancels in the ratio:",
               f"P({i + 1})/P({j + 1}) = e<super>z<sub>{i + 1}</sub> − z<sub>{j + 1}</sub></super> = "
               f"e<super>{fmt(z[i] - z[j])}</super> = <b>{fmt(ans, 2)}</b>."]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


LR_TRUE = [
    ("The sigmoid satisfies σ(−z) = 1 − σ(z).", "σ(−z) = 1/(1+e<super>z</super>) = 1 − 1/(1+e<super>−z</super>)."),
    ("The derivative of the sigmoid is σ′(z) = σ(z)(1 − σ(z)).", "Standard identity; maximal value 0.25 at z = 0."),
    ("In logistic regression, the log-odds ln[p/(1−p)] is a linear function of the input features.",
     "That is the model definition: logit(p) = wᵀx + b."),
    ("With threshold 0.5, the decision boundary of binary logistic regression is the hyperplane wᵀx + b = 0.",
     "σ(z) ≥ 0.5 ⇔ z ≥ 0."),
    ("The average cross-entropy loss of logistic regression is a convex function of (w, b).",
     "Its Hessian XᵀSX with S = diag(p<sub>i</sub>(1−p<sub>i</sub>)) is positive semidefinite."),
    ("There is no closed-form expression for the maximum-likelihood weights of logistic regression; they are "
     "found iteratively (gradient descent, Newton/IRLS).",
     "Setting the gradient Σ(σ(wᵀx<sub>i</sub>) − y<sub>i</sub>)x<sub>i</sub> = 0 gives non-linear equations."),
    ("If the training data are linearly separable, the norm of the unregularised logistic-regression weights "
     "grows without bound during gradient descent.",
     "Scaling a separating w up always lowers the loss, so the MLE does not exist (it diverges)."),
    ("Adding an L2 penalty λ‖w‖² (λ &gt; 0) keeps the logistic-regression weights finite even on separable data.",
     "The penalty grows with ‖w‖ and makes the objective strictly convex and coercive."),
    ("For one example, the gradient of the cross-entropy loss with respect to w is (σ(wᵀx + b) − y)x.",
     "dL/dz = σ(z) − y and dz/dw = x."),
    ("Increasing x<sub>j</sub> by one unit (others fixed) multiplies the odds of y = 1 by e<super>β<sub>j</sub></super>.",
     "The log-odds increase by β<sub>j</sub>."),
    ("Softmax regression with K = 2 classes is equivalent to binary logistic regression.",
     "P(1) = e<super>z<sub>1</sub></super>/(e<super>z<sub>1</sub></super>+e<super>z<sub>2</sub></super>) = σ(z<sub>1</sub>−z<sub>2</sub>)."),
    ("Softmax probabilities are unchanged if the same constant is added to every logit.",
     "e<super>c</super> cancels between numerator and denominator."),
    ("Changing the probability threshold from 0.5 to 0.8 moves the logistic-regression decision boundary to a "
     "parallel hyperplane.", "The boundary becomes wᵀx + b = ln 4, same normal vector w."),
    ("Logistic regression is a discriminative model: it models P(y | x) directly.",
     "It never models the distribution of x."),
    ("A negative coefficient β<sub>j</sub> means the predicted probability of y = 1 decreases as x<sub>j</sub> "
     "increases (others fixed).", "σ is increasing and the log-odds decrease with x<sub>j</sub>."),
    ("Minimising the cross-entropy loss is equivalent to maximising the Bernoulli log-likelihood of the labels.",
     "Cross-entropy = −(1/n) × log-likelihood."),
    ("Multiplying w and b by the same positive constant does not change the 0.5-threshold decision boundary.",
     "The set {wᵀx + b = 0} is unchanged; only the confidence (steepness) changes."),
    ("The decision boundaries between pairs of classes in softmax (multinomial logistic) regression are linear in x.",
     "Boundary between k and l: (w<sub>k</sub> − w<sub>l</sub>)ᵀx + (b<sub>k</sub> − b<sub>l</sub>) = 0."),
]
LR_FALSE = [
    ("Logistic regression weights have a closed-form solution analogous to the normal equations.",
     "The score equations are non-linear in w; iterative methods are needed."),
    ("The cross-entropy loss of logistic regression is non-convex, so gradient descent may get trapped in poor local minima.",
     "It is convex; every local minimum is global."),
    ("Without feature transformations, the decision boundary of logistic regression is quadratic in x.",
     "It is the hyperplane wᵀx + b = const (linear)."),
    ("Logistic regression assumes that the features are Gaussian within each class.",
     "That is an assumption of LDA/QDA (generative); logistic regression makes no assumption on P(x|y)."),
    ("σ(0) = 0.", "σ(0) = 1/(1+1) = 0.5."),
    ("Increasing x<sub>j</sub> by one unit increases P(y = 1 | x) by exactly β<sub>j</sub>.",
     "β<sub>j</sub> is the change in log-odds; the change in probability depends on x."),
    ("On linearly separable data, unregularised logistic regression converges to a unique finite weight vector.",
     "The weights diverge: the likelihood can be pushed arbitrarily close to 1."),
    ("The odds ratio for a one-unit increase in x<sub>j</sub> equals β<sub>j</sub>.", "It equals e<super>β<sub>j</sub></super>."),
    ("Adding the same constant to all logits changes the softmax probabilities.", "The constant cancels."),
    ("Logistic regression is a generative classifier that models P(x | y).", "It is discriminative."),
    ("For finite z, the sigmoid output σ(z) can be exactly 0 or exactly 1.", "0 &lt; σ(z) &lt; 1 for every finite z."),
    ("Multiplying all weights and the bias by 2 shifts the 0.5-threshold decision boundary.",
     "wᵀx + b = 0 ⇔ 2wᵀx + 2b = 0; the boundary is the same."),
    ("A predicted probability of 0.8 corresponds to log-odds equal to 0.8.", "log-odds = ln(0.8/0.2) = ln 4 ≈ 1.386."),
    ("The squared-error loss composed with the sigmoid is the standard convex training loss of logistic regression.",
     "The standard loss is cross-entropy; squared error with a sigmoid is non-convex in w."),
    ("Raising the classification threshold from 0.5 to 0.9 can increase recall.",
     "Fewer examples are predicted positive, so TP can only stay the same or fall."),
    ("In softmax regression with K classes, the boundary between two classes is in general a curved surface in x.",
     "It is the hyperplane (w<sub>k</sub> − w<sub>l</sub>)ᵀx + b<sub>k</sub> − b<sub>l</sub> = 0."),
    ("Logistic regression cannot be used when some input features are categorical.",
     "Categorical features are simply one-hot encoded."),
]


@template(TOPIC, LR, marks=1, qtype="MSQ")
def lr_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, LR_TRUE, LR_FALSE)
    return Q(text="Which of the following statements about logistic regression is/are CORRECT?", qtype="MSQ",
             marks=1, options=opts, answer=ans, solution=expl)


def _same_halfplane(u, v):
    u, v = np.asarray(u, float), np.asarray(v, float)
    # same if v = c u with c > 0
    c = (u @ v) / (u @ u)
    return c > 0 and np.allclose(v, c * u)


@template(TOPIC, LR, marks=2, qtype="MCQ")
def lr_boundary_figure(rng):
    while True:
        a = int(rng.choice([-4, -3, -2, 2, 3, 4]))  # x1-intercept
        c = int(rng.choice([-4, -3, -2, 2, 3, 4]))  # x2-intercept
        if abs(a) != abs(c):
            break
    s = int(rng.choice([-1, 1]))
    k = int(rng.choice([1, 1, 2]))
    g = math.gcd(abs(a), abs(c))
    base = np.array([-a * c, c, a]) // g  # w0, w1, w2 ; zero on line
    w = s * k * base
    # sample points
    pts, lab = [], []
    while len(pts) < 14:
        p = rng.uniform(-4.6, 4.6, 2)
        val = w[0] + w[1] * p[0] + w[2] * p[1]
        if abs(val) / np.linalg.norm(w[1:]) < 0.5:
            continue
        pts.append(p)
        lab.append(1 if val > 0 else 0)
    pts = np.array(pts)
    lab = np.array(lab)
    if lab.sum() in (0, len(lab)):
        pts[0] = np.array([0.0, 0.0])
    cands = [(-w[0], -w[1], -w[2]), (w[0], w[2], w[1]), (-w[0], w[1], w[2]), (w[0], -w[1], w[2]),
             (w[0], w[1], -w[2]), (-w[0], w[2], w[1]), (w[0], -w[2], -w[1])]
    dis = []
    for cnd in cands:
        if not _same_halfplane(w, cnd):
            st = f"(w<sub>0</sub>, w<sub>1</sub>, w<sub>2</sub>) = ({', '.join(fmt(v) for v in cnd)})"
            dis.append(st)
    corr = f"(w<sub>0</sub>, w<sub>1</sub>, w<sub>2</sub>) = ({', '.join(fmt(v) for v in w)})"
    opts, ans = mcq(rng, corr, dis)
    lab1 = lab.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        m1 = lab1 == 1
        ax.scatter(pts[m1, 0], pts[m1, 1], marker="o", s=30, color=DARK, label="y = 1", zorder=3)
        ax.scatter(pts[~m1, 0], pts[~m1, 1], marker="x", s=32, color=MID, label="y = 0", zorder=3)
        xx = np.linspace(-5, 5, 50)
        yy = c - c / a * xx
        ax.plot(xx, yy, color=DARK, lw=1.4)
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_xticks(range(-5, 6))
        ax.set_yticks(range(-5, 6))
        ax.axhline(0, color=LIGHT, lw=0.7)
        ax.axvline(0, color=LIGHT, lw=0.7)
        ax.grid(alpha=.3)
        ax.set_aspect("equal")
        ax.set_xlabel("x$_1$")
        ax.set_ylabel("x$_2$")
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)

    text = ("A logistic regression model P(y = 1 | <b>x</b>) = σ(w<sub>0</sub> + w<sub>1</sub>x<sub>1</sub> + "
            "w<sub>2</sub>x<sub>2</sub>) perfectly classifies the training points shown below using threshold 0.5. "
            "Its decision boundary is the solid line (it crosses the axes at grid points). Which of the following "
            "parameter vectors is consistent with the figure?")
    sol = [f"The line passes through ({a}, 0) and (0, {c}): x<sub>1</sub>/{fmt(a)} + x<sub>2</sub>/{fmt(c)} = 1, i.e. "
           f"{fmt(c)}x<sub>1</sub> + {fmt(a)}x<sub>2</sub> − {fmt(a * c)} = 0. Hence (w<sub>0</sub>, w<sub>1</sub>, "
           f"w<sub>2</sub>) must be a non-zero multiple of ({fmt(-a * c)}, {fmt(c)}, {fmt(a)}).",
           f"Orientation: the class y = 1 region must have w<sub>0</sub> + w<sub>1</sub>x<sub>1</sub> + "
           f"w<sub>2</sub>x<sub>2</sub> &gt; 0. At the origin the y = 1 side has sign "
           f"{'+' if w[0] > 0 else '−'} (w<sub>0</sub> = {fmt(w[0])}), which matches the figure "
           f"(the origin lies on the {'y = 1' if w[0] > 0 else 'y = 0'} side).",
           f"So the answer is <b>{corr}</b> (any positive multiple gives the same classifier).",
           "Other options either describe a different line (swapped/negated coefficients move the intercepts) or the "
           "same line with the sign flipped, which would label every training point incorrectly."]
    return Q(text=text, qtype="MCQ", marks=2, options=opts, answer=ans, blocks=[Figure(draw, 9.5, 6.5)],
             solution=sol)


@template(TOPIC, LR, marks=2, qtype="NAT")
def lr_boundary_threshold(rng):
    while True:
        w0 = float(rng.integers(-4, 5))
        w1, w2 = (float(v) for v in rng.choice([-3, -2, -1, 1, 2, 3], 2))
        p0 = float(_pick(rng, [0.2, 0.25, 0.75, 0.8, 0.9, 0.1, 0.5, 0.6, 0.4]))
        L = math.log(p0 / (1 - p0))
        var = int(rng.integers(3))
        if var == 0:
            x1v = float(rng.integers(-2, 3))
            ans = (L - w0 - w1 * x1v) / w2
            ask = f"the value of x<sub>2</sub> on the decision boundary at x<sub>1</sub> = {fmt(x1v)}"
            last = (f"x<sub>2</sub> = (c − w<sub>0</sub> − w<sub>1</sub>x<sub>1</sub>)/w<sub>2</sub> = "
                    f"({fmt(L, 4)} − ({fmt(w0)}) − ({fmt(w1)})({fmt(x1v)}))/({fmt(w2)})")
        elif var == 1:
            ans = (L - w0) / w1
            ask = "the x<sub>1</sub>-intercept of the decision boundary (the value of x<sub>1</sub> where it meets x<sub>2</sub> = 0)"
            last = f"x<sub>1</sub> = (c − w<sub>0</sub>)/w<sub>1</sub> = ({fmt(L, 4)} − ({fmt(w0)}))/({fmt(w1)})"
        else:
            ans = abs(L - w0) / math.hypot(w1, w2)
            ask = "the perpendicular distance of the decision boundary from the origin"
            last = (f"distance = |w<sub>0</sub> − c|/‖(w<sub>1</sub>, w<sub>2</sub>)‖ = |{fmt(w0)} − {fmt(L, 4)}|/"
                    f"√({fmt(w1 * w1 + w2 * w2)})")
        if abs(ans) <= 8 and (var != 2 or ans > 0.05):
            break
    text = (f"A logistic regression classifier has P(y = 1 | <b>x</b>) = σ({fmt(w0)} + ({fmt(w1)})x<sub>1</sub> + "
            f"({fmt(w2)})x<sub>2</sub>). An input is labelled y = 1 if and only if P(y = 1 | <b>x</b>) ≥ {fmt(p0)}. "
            f"For this rule, {ask} is ______")
    sol = [f"P(y=1|x) ≥ {fmt(p0)} ⇔ z ≥ c, where c = ln({fmt(p0)}/{fmt(1 - p0)}) = {fmt(L, 4)}.",
           f"Decision boundary: {fmt(w0)} + ({fmt(w1)})x<sub>1</sub> + ({fmt(w2)})x<sub>2</sub> = {fmt(L, 4)} "
           "(a straight line; changing the threshold only shifts it parallel to the 0.5 boundary).",
           last + f" = <b>{fmt(ans, 2)}</b>."]
    if p0 == 0.5:
        sol.insert(1, "Here c = 0 because the threshold is 0.5.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


@template(TOPIC, LR, marks=2, qtype="NAT")
def lr_cross_entropy(rng):
    var = int(rng.integers(3))
    n = int(rng.integers(4, 6))
    while True:
        y = rng.integers(0, 2, n)
        if 0 < y.sum() < n:
            break
    if var == 0:
        p = rng.choice(np.round(np.arange(0.1, 0.96, 0.05), 2), n, replace=True)
        rows = [["i"] + [str(i + 1) for i in range(n)], ["y<sub>i</sub>"] + [str(v) for v in y],
                ["p̂<sub>i</sub> = P(y<sub>i</sub>=1)"] + [fmt(v) for v in p]]
        intro = "The predicted probabilities p̂<sub>i</sub> = P(y<sub>i</sub> = 1 | x<sub>i</sub>) of a binary classifier on "
        intro += f"{n} examples, and their true labels, are given below."
        extra = []
    else:
        w = float(_pick(rng, [-1.5, -1, -0.5, 0.5, 1, 1.5, 2]))
        b = float(_pick(rng, [-1, -0.5, 0, 0.5, 1]))
        x = rng.integers(-2, 3, n).astype(float)
        p = np.array([_sig(w * xi + b) for xi in x])
        rows = [["i"] + [str(i + 1) for i in range(n)], ["x<sub>i</sub>"] + [fmt(v) for v in x],
                ["y<sub>i</sub>"] + [str(v) for v in y]]
        intro = (f"A one-feature logistic regression model P(y = 1 | x) = σ(wx + b) has w = {fmt(w)} and b = {fmt(b)}. "
                 f"It is evaluated on the {n} examples below.")
        extra = [f"z<sub>i</sub> = {fmt(w)}x<sub>i</sub> + {fmt(b)}; p̂<sub>i</sub> = σ(z<sub>i</sub>): " +
                 ", ".join(fmt(v, 4) for v in p) + "."]
    loss_i = np.where(y == 1, -np.log(p), -np.log(1 - p))
    mean_mode = var != 2
    total = loss_i.sum()
    ans = total / n if mean_mode else total
    what = "the <b>average</b> binary cross-entropy loss" if mean_mode else "the <b>total</b> (summed) binary cross-entropy loss"
    text = (intro + f" Using natural logarithms, {what} −[y ln p̂ + (1 − y) ln(1 − p̂)] over these examples is ______")
    sol = extra + ["Per-example loss L<sub>i</sub> = −ln p̂<sub>i</sub> if y<sub>i</sub> = 1 and −ln(1 − p̂<sub>i</sub>) if "
                   "y<sub>i</sub> = 0:",
                   Table([["i", "y", "p̂", "L<sub>i</sub>"]] +
                         [[str(i + 1), str(y[i]), fmt(p[i], 4), fmt(loss_i[i], 4)] for i in range(n)])]
    sol.append(f"ΣL<sub>i</sub> = {fmt(total, 4)}" + (f"; average = {fmt(total, 4)}/{n} = <b>{fmt(ans, 2)}</b>."
                                                       if mean_mode else f" = <b>{fmt(ans, 2)}</b>."))
    sol.append("Common mistakes: using ln p̂ for y = 0 examples, or log<sub>10</sub> instead of ln.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False)], solution=sol)


@template(TOPIC, LR, marks=2, qtype="NAT")
def lr_gradient_step(rng):
    n = int(rng.integers(2, 4))
    d2 = bool(rng.integers(2))
    eta = float(_pick(rng, [0.1, 0.2, 0.5, 1.0]))
    while True:
        X = rng.integers(-2, 4, (n, 2 if d2 else 1)).astype(float)
        y = rng.integers(0, 2, n)
        w = rng.choice([-0.5, 0.0, 0.5, 1.0], X.shape[1]).astype(float)
        b = float(_pick(rng, [0.0, 0.5, -0.5]))
        if not (X == 0).all(axis=0).any():
            break
    z = X @ w + b
    p = 1 / (1 + np.exp(-z))
    r = p - y
    gw = (r[:, None] * X).mean(axis=0)
    gb = r.mean()
    nw = w - eta * gw
    nb = b - eta * gb
    names = ["w<sub>1</sub>", "w<sub>2</sub>"][:X.shape[1]]
    tgt = int(rng.integers(X.shape[1] + 1))
    if tgt == X.shape[1]:
        tname, ans = "b", nb
    else:
        tname, ans = names[tgt], nw[tgt]
    if d2:
        rows = [["i", "x<sub>1</sub>", "x<sub>2</sub>", "y"]] + [[str(i + 1), fmt(X[i, 0]), fmt(X[i, 1]), str(y[i])]
                                                                  for i in range(n)]
        init = f"w<sub>1</sub> = {fmt(w[0])}, w<sub>2</sub> = {fmt(w[1])}, b = {fmt(b)}"
        model = "σ(w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + b)"
    else:
        rows = [["i", "x", "y"]] + [[str(i + 1), fmt(X[i, 0]), str(y[i])] for i in range(n)]
        init = f"w<sub>1</sub> = {fmt(w[0])}, b = {fmt(b)}"
        model = "σ(w<sub>1</sub>x + b)"
    text = (f"Logistic regression P(y = 1 | <b>x</b>) = {model} is trained by <b>batch</b> gradient descent on the "
            f"<b>average</b> cross-entropy loss over the {n} examples below, with learning rate η = {fmt(eta)}. "
            f"Starting from {init}, the value of {tname} after ONE gradient-descent update is ______")
    sol = ["For the average cross-entropy, ∂L/∂w<sub>j</sub> = (1/n)Σ(p̂<sub>i</sub> − y<sub>i</sub>)x<sub>ij</sub> and "
           "∂L/∂b = (1/n)Σ(p̂<sub>i</sub> − y<sub>i</sub>), with p̂<sub>i</sub> = σ(z<sub>i</sub>).",
           Table([["i", "z<sub>i</sub>", "p̂<sub>i</sub>", "p̂<sub>i</sub> − y<sub>i</sub>"]] +
                 [[str(i + 1), fmt(z[i], 3), fmt(p[i], 4), fmt(r[i], 4)] for i in range(n)]),
           "Gradient: " + ", ".join(f"∂L/∂{nm} = {fmt(g, 4)}" for nm, g in zip(names, gw)) + f", ∂L/∂b = {fmt(gb, 4)}.",
           f"Update θ ← θ − η∇L: " + ", ".join(f"{nm} = {fmt(wv)} − {fmt(eta)}×({fmt(g, 4)}) = {fmt(nv, 4)}"
                                               for nm, wv, g, nv in zip(names, w, gw, nw)) +
           f", b = {fmt(b)} − {fmt(eta)}×({fmt(gb, 4)}) = {fmt(nb, 4)}.",
           f"Required: {tname} = <b>{fmt(ans, 3)}</b>."]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.002), nat_hint=nat_hint(3),
             blocks=[Table(rows)], solution=sol)


@template(TOPIC, LR, marks=2, qtype="NAT")
def lr_softmax_matrix(rng):
    while True:
        W = rng.integers(-2, 3, (3, 2)).astype(float)
        bb = rng.integers(-1, 2, 3).astype(float)
        x = rng.integers(-2, 3, 2).astype(float)
        z = W @ x + bb
        if z.max() - z.min() <= 5 and len(set(z)) == 3 and not (x == 0).all():
            break
    p = np.exp(z) / np.exp(z).sum()
    var = int(rng.integers(2))
    k = int(rng.integers(3))
    if var == 0:
        ask = f"the predicted probability P(y = {k + 1} | <b>x</b>)"
        ans = p[k]
        last = f"P(y = {k + 1} | <b>x</b>) = <b>{fmt(ans, 2)}</b>."
    else:
        ask = (f"the cross-entropy loss −ln P(y = {k + 1} | <b>x</b>) incurred if the true class is {k + 1} "
               "(natural log)")
        ans = -math.log(p[k])
        last = f"Loss = −ln({fmt(p[k], 4)}) = <b>{fmt(ans, 2)}</b>."
    text = (f"A 3-class softmax (multinomial logistic) regression model computes scores <b>z</b> = W<b>x</b> + <b>b</b> and "
            f"P(y = k | <b>x</b>) = e<super>z<sub>k</sub></super>/Σ<sub>j</sub>e<super>z<sub>j</sub></super>, where row k "
            f"of W holds the weights of class k. For the parameters below and <b>x</b> = ({fmt(x[0])}, {fmt(x[1])})ᵀ, "
            f"{ask} is ______")
    sol = [f"<b>z</b> = W<b>x</b> + <b>b</b> = ({', '.join(fmt(v) for v in z)}).",
           "e<super>z</super> = (" + ", ".join(fmt(math.exp(v), 4) for v in z) + f"), sum = {fmt(np.exp(z).sum(), 4)}.",
           "Softmax probabilities = (" + ", ".join(fmt(v, 4) for v in p) + ").", last]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Matrix("W", W, 0), Matrix("b", bb, 0)], solution=sol)


# =============================================================================
# k-NN
# =============================================================================
def _knn1d_data(rng, n=7):
    while True:
        xs = np.sort(rng.choice(np.arange(0, 21), n, replace=False)).astype(float)
        ys = rng.integers(1, 30, n).astype(float)
        q = float(rng.integers(2, 19)) + float(_pick(rng, [0.5, 0.3, 0.7, 0.4]))
        d = np.abs(xs - q)
        order = np.argsort(d, kind="stable")
        ds = d[order]
        if all(ds[k - 1] < ds[k] - 1e-9 for k in (1, 2, 3, 4)) and len(set(np.round(ds, 6))) == n:
            return xs, ys, q, d, order


def _knn1d_fig(xs, ys, q):
    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(xs, ys, color=DARK, s=24, zorder=3)
        for a, b in zip(xs, ys):
            ax.annotate(fmt(b), (a, b), xytext=(3, 4), textcoords="offset points", fontsize=6.5)
        ax.axvline(q, ls="--", color=MID, lw=1)
        ax.text(q, ax.get_ylim()[0], f" query x = {fmt(q)}", fontsize=7, va="bottom", color=MID)
        ax.set_xticks(range(0, 21, 2))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(alpha=.3)
    return Figure(draw, 9, 4.8)


@template(TOPIC, KNN, marks=1, qtype="NAT")
def knn_regression(rng):
    xs, ys, q, d, order = _knn1d_data(rng)
    k = int(rng.integers(2, 5))
    nb = order[:k]
    ans = ys[nb].mean()
    text = (f"The training data for a k-NN regressor are given below (also plotted). Using k = {k} and absolute "
            f"distance |x − x<sub>i</sub>|, the predicted value (unweighted average of neighbours) at x = {fmt(q)} is ______")
    sol = ["Distances |x<sub>i</sub> − " + fmt(q) + "|: " + ", ".join(f"x={fmt(xs[i])}: {fmt(d[i])}" for i in order) + ".",
           f"The {k} nearest neighbours are x = " + ", ".join(fmt(xs[i]) for i in nb) + " with y = " +
           ", ".join(fmt(ys[i]) for i in nb) + ".",
           f"ŷ = ({' + '.join(fmt(ys[i]) for i in nb)})/{k} = <b>{fmt(ans, 2)}</b>."]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Table([["x"] + [fmt(v) for v in xs], ["y"] + [fmt(v) for v in ys]], header=False),
                     _knn1d_fig(xs, ys, q)], solution=sol)


@template(TOPIC, KNN, marks=2, qtype="NAT")
def knn_weighted(rng):
    var = int(rng.integers(2))
    if var == 0:
        xs, ys, q, d, order = _knn1d_data(rng)
        k = 3
        pw = int(rng.integers(1, 3))
        nb = order[:k]
        wts = 1 / d[nb] ** pw
        ans = (wts * ys[nb]).sum() / wts.sum()
        blocks = [Table([["x"] + [fmt(v) for v in xs], ["y"] + [fmt(v) for v in ys]], header=False),
                  _knn1d_fig(xs, ys, q)]
        qdesc = f"x = {fmt(q)}"
        dlist = [fmt(d[i], 2) for i in nb]
        nbdesc = ", ".join(f"x={fmt(xs[i])} (d={fmt(d[i])}, y={fmt(ys[i])})" for i in nb)
    else:
        while True:
            idx = rng.choice(64, 6, replace=False)
            X = np.stack([idx // 8, idx % 8], 1).astype(float)
            ys = rng.integers(1, 20, 6).astype(float)
            qv = rng.integers(1, 7, 2).astype(float)
            d = _dist(X, qv, "E")
            order = np.argsort(d, kind="stable")
            ds = d[order]
            if ds[0] > 0 and ds[2] < ds[3] - 1e-9:
                break
        k = 3
        pw = 2
        nb = order[:k]
        wts = 1 / d[nb] ** pw
        ans = (wts * ys[nb]).sum() / wts.sum()
        rows = [["Point", "x<sub>1</sub>", "x<sub>2</sub>", "y"]] + [[f"P{i + 1}", fmt(X[i, 0]), fmt(X[i, 1]), fmt(ys[i])]
                                                                       for i in range(6)]
        Xc, yc, qc = X.copy(), ys.copy(), qv.copy()

        def draw(fig):
            ax = fig.add_subplot(111)
            ax.scatter(Xc[:, 0], Xc[:, 1], color=DARK, s=24, zorder=3)
            for i, (a, b) in enumerate(Xc):
                ax.annotate(f"P{i + 1} (y={fmt(yc[i])})", (a, b), xytext=(3, 4), textcoords="offset points",
                            fontsize=6.5)
            ax.scatter([qc[0]], [qc[1]], marker="*", s=110, color=MID, zorder=4)
            ax.annotate("query", (qc[0], qc[1]), xytext=(5, -10), textcoords="offset points", fontsize=7, color=MID)
            ax.set_xlim(-0.5, 8.5)
            ax.set_ylim(-0.5, 8.5)
            ax.set_xticks(range(0, 9))
            ax.set_yticks(range(0, 9))
            ax.set_aspect("equal")
            ax.grid(alpha=.3)
            ax.set_xlabel("x$_1$")
            ax.set_ylabel("x$_2$")
        blocks = [Table(rows), Figure(draw, 8, 6.5)]
        qdesc = f"<b>x</b> = ({fmt(qv[0])}, {fmt(qv[1])}) (Euclidean distance)"
        nbdesc = ", ".join(f"P{i + 1} (d²={fmt(d[i] ** 2)}, y={fmt(ys[i])})" for i in nb)
    wname = "1/d" if pw == 1 else "1/d²"
    text = (f"A distance-weighted k-NN regressor with k = 3 predicts ŷ = Σw<sub>i</sub>y<sub>i</sub>/Σw<sub>i</sub> over "
            f"the 3 nearest neighbours, with weights w<sub>i</sub> = {wname}<sub>i</sub>. For the training data below, "
            f"the prediction at {qdesc} is ______")
    sol = [f"Three nearest neighbours: {nbdesc}.",
           "Weights " + wname + ": " + ", ".join(fmt(v, 4) for v in wts) + f"; Σw = {fmt(wts.sum(), 4)}.",
           f"Σw<sub>i</sub>y<sub>i</sub> = {fmt((wts * ys[nb]).sum(), 4)} ⇒ ŷ = {fmt((wts * ys[nb]).sum(), 4)}/"
           f"{fmt(wts.sum(), 4)} = <b>{fmt(ans, 2)}</b>.",
           f"(The unweighted 3-NN average would be {fmt(ys[nb].mean(), 2)}; weighting pulls ŷ towards the closest point.)"]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2), blocks=blocks,
             solution=sol)


@template(TOPIC, KNN, marks=2, qtype="MSQ")
def knn_classify_figure(rng):
    while True:
        n = 12
        idx = rng.choice(100, n, replace=False)
        X = np.stack([idx // 10, idx % 10], 1).astype(float)
        lab = rng.integers(0, 2, n)
        if not 4 <= lab.sum() <= 8:
            continue
        q = rng.integers(2, 8, 2).astype(float) + rng.choice([0.0, 0.5], 2)
        if (np.abs(X - q).sum(1) == 0).any():
            continue
        metric = str(rng.choice(["E", "M"]))
        d = _dist(X, q, metric)
        order = np.argsort(d, kind="stable")
        ds = d[order]
        if not all(ds[k - 1] < ds[k] - 1e-9 for k in (1, 3, 5, 7)):
            continue
        preds = {k: int(lab[order[:k]].sum() * 2 > k) for k in (1, 3, 5, 7)}
        if len(set(preds.values())) < 2:
            continue
        break
    cname = ["A", "B"]
    items = []
    truths = rng.random(4) < 0.5
    if not truths.any():
        truths[int(rng.integers(4))] = True
    for j, k in enumerate((1, 3, 5, 7)):
        stated = preds[k] if truths[j] else 1 - preds[k]
        nbl = lab[order[:k]]
        ex = (f"{k} nearest: " + ", ".join(f"#{i + 1}" for i in order[:k]) +
              f" → {int((nbl == 0).sum())} A vs {int((nbl == 1).sum())} B ⇒ class {cname[preds[k]]}.")
        items.append((f"With k = {k}, the query is classified as class {cname[stated]}.", bool(truths[j]), ex))
    opts, ans, expl = _msq_build(rng, items)
    Xc, lc, qc = X.copy(), lab.copy(), q.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_classes(ax, Xc, lc, annotate=[f"#{i + 1}" for i in range(n)])
        ax.scatter([qc[0]], [qc[1]], marker="*", s=130, color=MID, zorder=4, label="query")
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.5, 9.5)
        ax.set_xticks(range(10))
        ax.set_yticks(range(10))
        ax.set_aspect("equal")
        ax.grid(alpha=.35)
        ax.set_xlabel("x$_1$")
        ax.set_ylabel("x$_2$")
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)

    rows = [["#"] + [str(i + 1) for i in range(n)], ["x<sub>1</sub>"] + [fmt(v) for v in X[:, 0]],
            ["x<sub>2</sub>"] + [fmt(v) for v in X[:, 1]], ["class"] + [cname[v] for v in lab]]
    text = (f"The figure and table show 12 labelled training points (class A: filled circles, class B: open "
            f"triangles) and a query point (star) at ({fmt(q[0])}, {fmt(q[1])}). A k-NN classifier with "
            f"<b>{METRIC_NAME[metric]}</b> distance and majority vote is used. Which of the following statements "
            f"is/are CORRECT?")
    sol = ["Distances from the query, sorted:",
           Table([["rank", "#", "(x<sub>1</sub>, x<sub>2</sub>)", "distance", "class"]] +
                 [[str(r + 1), str(i + 1), f"({fmt(X[i, 0])}, {fmt(X[i, 1])})", _dist_str(X, q, metric, i),
                   cname[lab[i]]] for r, i in enumerate(order[:8])])] + expl
    return Q(text=text, qtype="MSQ", marks=2, options=opts, answer=ans,
             blocks=[Table(rows, header=False), Figure(draw, 9.5, 6.8)], solution=sol)


@template(TOPIC, KNN, marks=2, qtype="MCQ")
def knn_metric_compare(rng):
    want_diff = rng.random() < 0.65
    for _ in range(4000):
        n = 7
        idx = rng.choice(121, n, replace=False)
        X = np.stack([idx // 11, idx % 11], 1).astype(float)
        lab = rng.integers(0, 2, n)
        if not 2 <= lab.sum() <= 5:
            continue
        q = rng.integers(2, 9, 2).astype(float)
        if (np.abs(X - q).sum(1) == 0).any():
            continue
        res = {}
        ok = True
        for m in ("E", "M"):
            d = _dist(X, q, m)
            o = np.argsort(d, kind="stable")
            if not d[o[2]] < d[o[3]] - 1e-9:
                ok = False
                break
            res[m] = (d, o, int(lab[o[:3]].sum() >= 2))
        if not ok:
            continue
        if want_diff and res["E"][2] == res["M"][2]:
            continue
        break
    cn = ["A", "B"]
    combos = [f"Euclidean: {cn[a]}; Manhattan: {cn[b]}" for a in (0, 1) for b in (0, 1)]
    corr = f"Euclidean: {cn[res['E'][2]]}; Manhattan: {cn[res['M'][2]]}"
    opts, ans = mcq(rng, corr, combos)
    rows = [["Point", "x<sub>1</sub>", "x<sub>2</sub>", "class"]] + [[f"P{i + 1}", fmt(X[i, 0]), fmt(X[i, 1]), cn[lab[i]]]
                                                                      for i in range(n)]
    text = (f"Consider the training set below. A 3-NN classifier (majority vote) is applied to the query point "
            f"<b>q</b> = ({fmt(q[0])}, {fmt(q[1])}), once with Euclidean distance and once with Manhattan distance. "
            f"The predicted classes are")
    tab = [["Point", "class", "Euclidean d", "Manhattan d"]]
    for i in range(n):
        tab.append([f"P{i + 1}", cn[lab[i]], fmt(res["E"][0][i], 3), fmt(res["M"][0][i], 2)])
    sol = ["Distances from <b>q</b>:", Table(tab),
           "Euclidean 3 nearest: " + ", ".join(f"P{i + 1}({cn[lab[i]]})" for i in res["E"][1][:3]) +
           f" ⇒ <b>{cn[res['E'][2]]}</b>.",
           "Manhattan 3 nearest: " + ", ".join(f"P{i + 1}({cn[lab[i]]})" for i in res["M"][1][:3]) +
           f" ⇒ <b>{cn[res['M'][2]]}</b>.",
           f"Answer: <b>{corr}</b>." + (" The two metrics disagree because L<sub>1</sub> penalises diagonal "
                                         "offsets more than L<sub>2</sub>, changing the neighbour set."
                                         if res["E"][2] != res["M"][2] else
                                         " Here both metrics lead to the same vote.")]
    Xc, lc, qc = X.copy(), lab.copy(), q.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_classes(ax, Xc, lc, annotate=[f"P{i + 1}" for i in range(n)])
        ax.scatter([qc[0]], [qc[1]], marker="*", s=120, color=MID, zorder=4, label="q")
        ax.set_xlim(-0.5, 10.5)
        ax.set_ylim(-0.5, 10.5)
        ax.set_xticks(range(11))
        ax.set_yticks(range(11))
        ax.set_aspect("equal")
        ax.grid(alpha=.35)
        ax.set_xlabel("x$_1$")
        ax.set_ylabel("x$_2$")
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    return Q(text=text, qtype="MCQ", marks=2, options=opts, answer=ans, blocks=[Table(rows), Figure(draw, 8.5, 6.5)],
             solution=sol)


@template(TOPIC, KNN, marks=2, qtype="NAT")
def knn_loocv(rng):
    for _ in range(5000):
        n = int(rng.integers(8, 11))
        xs = np.sort(rng.choice(np.arange(0, 31), n, replace=False)).astype(float)
        t = rng.integers(8, 23)
        lab = (xs > t).astype(int) ^ (rng.random(n) < 0.22).astype(int)
        k = int(rng.choice([1, 3]))
        errs, ok, det = 0, True, []
        for i in range(n):
            oth = np.delete(np.arange(n), i)
            d = np.abs(xs[oth] - xs[i])
            o = np.argsort(d, kind="stable")
            if not d[o[k - 1]] < d[o[k]] - 1e-9:
                ok = False
                break
            nbr = oth[o[:k]]
            pred = int(lab[nbr].sum() * 2 > k)
            errs += int(pred != lab[i])
            det.append((i, nbr, pred))
        if ok and 0 < errs < n and 0 < lab.sum() < n:
            break
    var = int(rng.integers(2))
    if var == 0:
        ans, d_, ask = float(errs), 0, "the number of training points misclassified in leave-one-out cross-validation"
    else:
        ans, d_, ask = errs / n, 2, "the leave-one-out cross-validation error rate (as a fraction)"
    xc, lc = xs.copy(), lab.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.axhline(0, color=LIGHT, lw=1, zorder=1)
        m1 = lc == 1
        ax.scatter(xc[m1], np.zeros(m1.sum()), marker="o", s=46, color=DARK, zorder=3, label="class 1")
        ax.scatter(xc[~m1], np.zeros((~m1).sum()), marker="s", s=40, facecolor="white", edgecolor=DARK, zorder=3,
                   label="class 0")
        for v in xc:
            ax.annotate(fmt(v), (v, 0), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=7)
        ax.set_ylim(-1, 1.2)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_xlim(-1, 31)
        ax.set_xlabel("x")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.45), ncol=2, frameon=False)

    tab = [["x", "true", f"{k} nearest (excluding itself)", "LOO prediction", ""]]
    for i, nbr, pred in det:
        tab.append([fmt(xs[i]), str(lab[i]), ", ".join(f"{fmt(xs[j])}({lab[j]})" for j in nbr), str(pred),
                    "wrong" if pred != lab[i] else ""])
    text = (f"Ten or fewer one-dimensional points with binary labels are shown on the number line (filled circle = "
            f"class 1, open square = class 0). A {k}-NN classifier (absolute distance, majority vote) is evaluated by "
            f"leave-one-out cross-validation: each point is classified using all the <i>other</i> points. "
            f"{ask[0].upper() + ask[1:]} is ______")
    text = text.replace("Ten or fewer one-dimensional points", f"{n} one-dimensional points")
    sol = ["Classify each point by its nearest neighbour(s) among the remaining points:", Table(tab),
           f"Misclassified: {errs} of {n}." + (f" Error rate = {errs}/{n} = <b>{fmt(ans, 2)}</b>." if var == 1
                                               else f" Answer: <b>{errs}</b>."),
           "Note: the <i>training</i> error of 1-NN is 0, but the LOOCV error is not — a point cannot be its own neighbour."]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, d_) if d_ else (ans, ans), nat_hint=nat_hint(d_),
             blocks=[Figure(draw, 12, 3.4)], solution=sol)


@template(TOPIC, KNN, marks=2, qtype="MCQ")
def knn_scaling(rng):
    while True:
        age = rng.integers(20, 61, 4).astype(float)
        inc = rng.integers(20, 151, 4).astype(float)
        if len(set(age)) < 4 or len(set(inc)) < 4:
            continue
        qa = float(rng.integers(age.min() + 1, age.max()))
        qi = float(rng.integers(inc.min() + 1, inc.max()))
        X = np.stack([age, inc], 1)
        q = np.array([qa, qi])
        draw_ = _dist(X, q, "E")
        lo, hi = X.min(0), X.max(0)
        Xs = (X - lo) / (hi - lo)
        qs = (q - lo) / (hi - lo)
        dsc = _dist(Xs, qs, "E")
        r1, s1 = np.sort(draw_), np.sort(dsc)
        if r1[1] - r1[0] < 0.5 or s1[1] - s1[0] < 0.03:
            continue
        if int(np.argmin(draw_)) == int(np.argmin(dsc)):
            continue
        break
    raw_nn, sc_nn = int(np.argmin(draw_)), int(np.argmin(dsc))
    opts = [f"P{i + 1}" for i in range(4)]
    ans = sc_nn
    rows = [["Point", "Age (years)", "Monthly income (₹ thousand)"]] + \
           [[f"P{i + 1}", fmt(age[i]), fmt(inc[i])] for i in range(4)] + [["Query", fmt(qa), fmt(qi)]]
    text = ("A 1-NN classifier uses the two features below. Before computing Euclidean distances, each feature is "
            "min-max scaled to [0, 1] using the minimum and maximum of that feature over the four training points "
            "P1–P4 (the query is scaled with the same constants). The nearest neighbour of the query after scaling is")
    sol = [f"Ranges: age [{fmt(lo[0])}, {fmt(hi[0])}], income [{fmt(lo[1])}, {fmt(hi[1])}]. Scaled query = "
           f"({fmt(qs[0], 3)}, {fmt(qs[1], 3)}).",
           Table([["Point", "scaled age", "scaled income", "scaled distance", "raw distance"]] +
                 [[f"P{i + 1}", fmt(Xs[i, 0], 3), fmt(Xs[i, 1], 3), fmt(dsc[i], 3), fmt(draw_[i], 2)]
                  for i in range(4)]),
           f"Nearest after scaling: <b>P{sc_nn + 1}</b>.",
           f"Without scaling the nearest point would be P{raw_nn + 1}, because income differences (tens of thousands) "
           "dominate the age differences — exactly why k-NN needs feature scaling."]
    Xc, qc = X.copy(), q.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(Xc[:, 0], Xc[:, 1], color=DARK, s=26, zorder=3)
        for i, (a, b) in enumerate(Xc):
            ax.annotate(f"P{i + 1}", (a, b), xytext=(4, 3), textcoords="offset points", fontsize=7)
        ax.scatter([qc[0]], [qc[1]], marker="*", s=120, color=MID, zorder=4)
        ax.annotate("query", (qc[0], qc[1]), xytext=(5, -10), textcoords="offset points", fontsize=7, color=MID)
        ax.set_xlim(15, 65)
        ax.set_ylim(10, 160)
        ax.set_xlabel("Age (years)")
        ax.set_ylabel("Income (₹ thousand)")
        ax.grid(alpha=.3)
    return Q(text=text, qtype="MCQ", marks=2, options=opts, answer=ans, blocks=[Table(rows), Figure(draw, 8, 5)],
             solution=sol)


@template(TOPIC, KNN, marks=1, qtype="NAT")
def knn_curse_dimension(rng):
    var = int(rng.integers(2))
    if var == 0:
        while True:
            r = float(_pick(rng, [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]))
            d = int(_pick(rng, [2, 3, 5, 10, 20, 50]))
            ans = r ** (1 / d)
            if 0.08 < ans < 0.995:
                break
        text = (f"Data are uniformly distributed in the unit hypercube [0, 1]<super>{d}</super>. To capture a fraction "
                f"{fmt(r)} of the data, a k-NN method uses a sub-cube neighbourhood. The required edge length of this "
                f"sub-cube is ______")
        sol = [f"Volume of a cube with edge e is e<super>{d}</super>; set e<super>{d}</super> = {fmt(r)}.",
               f"e = {fmt(r)}<super>1/{d}</super> = <b>{fmt(ans, 2)}</b>.",
               "In high dimensions even a small fraction of data needs an edge spanning most of each coordinate's "
               "range, so 'nearest' neighbours are not local — the curse of dimensionality."]
    else:
        while True:
            eps = float(_pick(rng, [0.01, 0.02, 0.05, 0.1]))
            d = int(_pick(rng, [5, 10, 20, 50, 100]))
            ans = 1 - (1 - 2 * eps) ** d
            if 0.05 < ans < 0.995:
                break
        text = (f"Points are drawn uniformly from the unit hypercube [0, 1]<super>{d}</super>. The fraction of points "
                f"lying within distance {fmt(eps)} of the boundary (i.e. outside the inner cube "
                f"[{fmt(eps)}, {fmt(1 - eps)}]<super>{d}</super>) is ______")
        sol = [f"Inner cube volume = (1 − 2×{fmt(eps)})<super>{d}</super> = {fmt(1 - 2 * eps)}<super>{d}</super> "
               f"= {fmt((1 - 2 * eps) ** d, 4)}.",
               f"Fraction near the boundary = 1 − {fmt((1 - 2 * eps) ** d, 4)} = <b>{fmt(ans, 2)}</b>.",
               "In high dimensions most points lie near the boundary, far from each other — a symptom of the curse of "
               "dimensionality that hurts k-NN."]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


KNN_TRUE = [
    ("k-NN is a lazy (instance-based) learner: training essentially consists of storing the data.",
     "All computation is deferred to prediction time."),
    ("The training error of 1-NN is zero when no two identical inputs carry different labels.",
     "Each training point is its own nearest neighbour."),
    ("Increasing k generally increases bias and decreases variance of the k-NN classifier.",
     "Averaging more neighbours smooths the decision boundary."),
    ("The decision boundary of 1-NN is made of pieces of perpendicular bisectors between training points of "
     "different classes.", "It is the union of Voronoi-cell edges separating differently labelled points."),
    ("Rescaling one feature (e.g. metres → millimetres) can change k-NN predictions.",
     "Distances, and hence neighbour sets, depend on feature scales."),
    ("In high dimensions, distances between random points tend to concentrate, making nearest neighbours less "
     "informative.", "The ratio of farthest to nearest distance approaches 1."),
    ("The cost of a brute-force k-NN prediction grows linearly with the number of training points n.",
     "Distances to all n points are computed for each query."),
    ("For binary classification, choosing an odd k avoids ties in majority voting.", "Votes cannot split equally."),
    ("In distance-weighted k-NN, closer neighbours receive larger weights.", "Typical weights are 1/d or 1/d²."),
    ("Unweighted k-NN regression with k = n (all training points) predicts the training mean of y for every query.",
     "All points are neighbours of every query."),
    ("k-NN can produce highly non-linear decision boundaries.", "It is non-parametric."),
    ("Irrelevant (noise) features can degrade k-NN accuracy because they still contribute to distances.",
     "They add random variation to every distance."),
    ("As n → ∞, the error rate of 1-NN is at most twice the Bayes error rate (binary case).",
     "Cover–Hart bound: R* ≤ R<sub>1NN</sub> ≤ 2R*(1 − R*)."),
    ("k-NN is a non-parametric method: its effective complexity grows with the amount of training data.",
     "The whole training set is the model."),
    ("The number of neighbours k is a hyperparameter usually chosen by cross-validation.",
     "Training error cannot select k (it always favours k = 1)."),
    ("Manhattan and Euclidean distances can give different nearest neighbours for the same query.",
     "Their orderings of points differ in general."),
]
KNN_FALSE = [
    ("Increasing k always reduces the test error of k-NN.", "Too large k underfits; test error is typically U-shaped in k."),
    ("k-NN training requires solving an optimisation problem by gradient descent.", "It simply stores the data."),
    ("k-NN predictions are invariant to rescaling of individual features.", "Scaling changes distances."),
    ("1-NN has high bias and low variance.", "1-NN has low bias and high variance."),
    ("For a fixed sample size, k-NN typically becomes more accurate as the number of irrelevant dimensions grows.",
     "More irrelevant dimensions dilute distances (curse of dimensionality)."),
    ("The decision boundary of k-NN is always a straight line (hyperplane).", "It is generally piecewise and non-linear."),
    ("The training error of k-NN is zero for every value of k.", "Only 1-NN is guaranteed zero training error (without duplicates)."),
    ("k-NN is a parametric model whose number of parameters does not depend on n.", "It is non-parametric."),
    ("Prediction with brute-force k-NN takes time independent of the training-set size.", "It is O(nd) per query."),
    ("Using a larger k makes the k-NN decision boundary more jagged.", "Larger k gives smoother boundaries."),
    ("Feature scaling is unnecessary for k-NN even when features are measured in very different units.",
     "Large-range features dominate the distance."),
    ("Unweighted k-NN classification with k = n gives different predictions for different queries.",
     "Every query sees all points, so it always predicts the majority class."),
    ("The leave-one-out cross-validation error of 1-NN is always zero, since its training error is zero.",
     "In LOOCV a point cannot use itself as neighbour."),
    ("In distance-weighted k-NN with weights 1/d, farther neighbours get larger weights.", "Weights decrease with distance."),
]


@template(TOPIC, KNN, marks=1, qtype="MSQ")
def knn_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, KNN_TRUE, KNN_FALSE)
    return Q(text="Which of the following statements about the k-nearest-neighbour method is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, KNN, marks=1, qtype="MCQ")
def knn_k_panels(rng):
    kbig = int(_pick(rng, [15, 21, 25]))
    while True:
        X0 = rng.normal([0, 0], 1.15, (20, 2))
        X1 = rng.normal([1.7, 1.7], 1.15, (20, 2))
        X = np.vstack([X0, X1])
        y = np.array([0] * 20 + [1] * 20)
        D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        o = np.argsort(D, axis=1)[:, :kbig]
        pred = (y[o].sum(1) * 2 > kbig).astype(int)
        if (pred != y).sum() >= 2:
            break
    small_first = bool(rng.integers(2))
    ks = (1, kbig) if small_first else (kbig, 1)
    p1 = "P" if small_first else "Q"
    pb = "Q" if small_first else "P"
    corr = f"Panel {p1} uses k = 1; it has lower bias and higher variance"
    dis = [f"Panel {p1} uses k = 1; it has higher bias and lower variance",
           f"Panel {pb} uses k = 1; it has lower bias and higher variance",
           f"Panel {pb} uses k = 1; it has higher bias and lower variance",
           f"Panel {pb} uses k = {kbig}; it has zero training error"]
    opts, ans = mcq(rng, corr, dis)

    def draw(fig):
        gx = np.linspace(X[:, 0].min() - 0.5, X[:, 0].max() + 0.5, 110)
        gy = np.linspace(X[:, 1].min() - 0.5, X[:, 1].max() + 0.5, 110)
        GX, GY = np.meshgrid(gx, gy)
        G = np.stack([GX.ravel(), GY.ravel()], 1)
        DG = np.sqrt(((G[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        for j, k in enumerate(ks):
            ax = fig.add_subplot(1, 2, j + 1)
            oo = np.argsort(DG, axis=1)[:, :k]
            Z = (y[oo].sum(1) * 2 > k).astype(float).reshape(GX.shape)
            ax.contourf(GX, GY, Z, levels=[-0.5, 0.5, 1.5], colors=["#f2f2f2", "#c8c8c8"])
            ax.contour(GX, GY, Z, levels=[0.5], colors=DARK, linewidths=0.9)
            _scatter_classes(ax, X, y)
            ax.set_title(f"Panel {'PQ'[j]}")
            ax.set_xticks([])
            ax.set_yticks([])

    text = (f"The two panels show the decision regions of k-NN classifiers trained on the same 2-D data set, one with "
            f"k = 1 and the other with k = {kbig}. Which of the following statements is CORRECT?")
    sol = [f"The jagged boundary with small islands around individual points (Panel {p1}) is produced by k = 1, which "
           f"fits every training point (zero training error): low bias, high variance.",
           f"The smooth boundary (Panel {pb}) comes from k = {kbig}: averaging many neighbours raises bias and lowers "
           f"variance; it misclassifies some training points, so its training error is not zero.",
           f"Answer: <b>{corr}</b>."]
    return Q(text=text, qtype="MCQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 13, 5.6)], solution=sol)


# =============================================================================
# NAIVE BAYES
# =============================================================================
NB_CONTEXTS = [
    dict(feats=[("Outlook", ["Sunny", "Overcast", "Rain"]), ("Temp", ["Hot", "Mild", "Cool"]),
                ("Wind", ["Weak", "Strong"])], cls="Play", cv=["Yes", "No"]),
    dict(feats=[("Income", ["Low", "Medium", "High"]), ("Credit", ["Good", "Bad"]), ("Employed", ["Yes", "No"])],
         cls="Approve", cv=["Yes", "No"]),
    dict(feats=[("Sender", ["Known", "Unknown"]), ("Length", ["Short", "Medium", "Long"]),
                ("HasLink", ["Yes", "No"])], cls="Class", cv=["Spam", "Ham"]),
    dict(feats=[("Fever", ["High", "Mild", "None"]), ("Cough", ["Yes", "No"]), ("Fatigue", ["Yes", "No"])],
         cls="Flu", cv=["Pos", "Neg"]),
    dict(feats=[("Age", ["Young", "Middle", "Senior"]), ("Student", ["Yes", "No"]), ("Rating", ["Fair", "Excellent"])],
         cls="Buys", cv=["Yes", "No"]),
]


def _nb_data(rng, n):
    ctx = NB_CONTEXTS[int(rng.integers(len(NB_CONTEXTS)))]
    while True:
        y = (rng.random(n) < 0.5).astype(int)
        if not 3 <= y.sum() <= n - 3:
            continue
        probs = [[rng.dirichlet(np.ones(len(v)) * 1.3) for _ in range(2)] for _, v in ctx["feats"]]
        X = np.zeros((n, len(ctx["feats"])), int)
        for i in range(n):
            for j, (_, vals) in enumerate(ctx["feats"]):
                X[i, j] = rng.choice(len(vals), p=probs[j][y[i]])
        return ctx, X, y


def _nb_table(ctx, X, y):
    rows = [["#"] + [f for f, _ in ctx["feats"]] + [ctx["cls"]]]
    for i in range(len(y)):
        rows.append([str(i + 1)] + [ctx["feats"][j][1][X[i, j]] for j in range(X.shape[1])] + [ctx["cv"][y[i]]])
    return Table(rows)


def _nb_scores(ctx, X, y, xq, alpha):
    n = len(y)
    out = []
    for c in (0, 1):
        nc = int((y == c).sum())
        terms = [Fraction(nc, n)]
        desc = [f"P({ctx['cls']}={ctx['cv'][c]}) = {nc}/{n}"]
        for j, (fname, vals) in enumerate(ctx["feats"]):
            cnt = int(((X[:, j] == xq[j]) & (y == c)).sum())
            V = len(vals)
            fr = Fraction(cnt + alpha, nc + alpha * V)
            terms.append(fr)
            if alpha:
                desc.append(f"P({fname}={vals[xq[j]]}|{ctx['cv'][c]}) = ({cnt}+1)/({nc}+{V}) = {fr.numerator}/{fr.denominator}")
            else:
                desc.append(f"P({fname}={vals[xq[j]]}|{ctx['cv'][c]}) = {cnt}/{nc}")
        sc = 1.0
        for t in terms:
            sc *= float(t)
        out.append((sc, terms, desc))
    return out


@template(TOPIC, NB, marks=2, qtype="NAT")
def nb_categorical_posterior(rng):
    alpha = int(rng.integers(2))
    while True:
        n = int(rng.integers(10, 13))
        ctx, X, y = _nb_data(rng, n)
        xq = [int(rng.integers(len(v))) for _, v in ctx["feats"]]
        sc = _nb_scores(ctx, X, y, xq, alpha)
        if any(s == 0 for s, _, _ in sc):
            continue
        post = sc[0][0] / (sc[0][0] + sc[1][0])
        if 0.04 < post < 0.96:
            break
    qdesc = ", ".join(f"{f} = {vals[xq[j]]}" for j, (f, vals) in enumerate(ctx["feats"]))
    smooth = ("using <b>Laplace (add-one) smoothing</b> for the class-conditional feature probabilities (the class "
              "prior is not smoothed)") if alpha else "using maximum-likelihood estimates (no smoothing)"
    text = (f"A naive Bayes classifier is trained on the {n} examples below, {smooth}. For the new instance "
            f"({qdesc}), the posterior probability P({ctx['cls']} = {ctx['cv'][0]} | x) is ______")
    sol = ["Naive Bayes: P(c | x) ∝ P(c) Π<sub>j</sub> P(x<sub>j</sub> | c)." +
           (" With Laplace smoothing, P(x<sub>j</sub> = v | c) = (count + 1)/(n<sub>c</sub> + V<sub>j</sub>), "
            "V<sub>j</sub> = number of values of feature j." if alpha else "")]
    for c in (0, 1):
        s, terms, desc = sc[c]
        sol.append(f"<b>{ctx['cv'][c]}</b>: " + "; ".join(desc) + f". Product = {fmt(s, 5)}.")
    sol.append(f"P({ctx['cv'][0]} | x) = {fmt(sc[0][0], 5)}/({fmt(sc[0][0], 5)} + {fmt(sc[1][0], 5)}) = "
               f"<b>{fmt(post, 2)}</b>.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(post, 2), nat_hint=nat_hint(2),
             blocks=[_nb_table(ctx, X, y)], solution=sol)


@template(TOPIC, NB, marks=2, qtype="MCQ")
def nb_zero_frequency(rng):
    want_flip = rng.random() < 0.55
    for _ in range(5000):
        n = int(rng.integers(10, 13))
        ctx, X, y = _nb_data(rng, n)
        xq = [int(rng.integers(len(v))) for _, v in ctx["feats"]]
        s0 = _nb_scores(ctx, X, y, xq, 0)
        zeros = [s == 0 for s, _, _ in s0]
        if sum(zeros) != 1:
            continue
        zc = zeros.index(True)
        unsm = 1 - zc
        s1 = _nb_scores(ctx, X, y, xq, 1)
        if abs(math.log(s1[0][0] / s1[1][0])) < 0.08:
            continue
        sm = 0 if s1[0][0] > s1[1][0] else 1
        if want_flip and sm == unsm:
            continue
        break
    cv = ctx["cv"]
    combos = [f"Without smoothing: {cv[a]}; with Laplace smoothing: {cv[b]}" for a in (0, 1) for b in (0, 1)]
    corr = f"Without smoothing: {cv[unsm]}; with Laplace smoothing: {cv[sm]}"
    opts, ans = mcq(rng, corr, combos)
    qdesc = ", ".join(f"{f} = {vals[xq[j]]}" for j, (f, vals) in enumerate(ctx["feats"]))
    text = (f"A naive Bayes classifier is trained on the {n} examples below. The new instance ({qdesc}) is classified "
            f"(i) with maximum-likelihood (unsmoothed) estimates and (ii) with Laplace (add-one) smoothing of the "
            f"class-conditional probabilities (class priors unsmoothed). The predicted classes are")
    sol = ["<b>(i) No smoothing.</b>"]
    for c in (0, 1):
        sol.append(f"{cv[c]}: " + "; ".join(s0[c][2]) + f" ⇒ score = {fmt(s0[c][0], 5)}.")
    sol.append(f"A zero count makes the whole product for {cv[zc]} equal to 0 (zero-frequency problem), so the "
               f"prediction is {cv[unsm]}.")
    sol.append("<b>(ii) Laplace smoothing.</b>")
    for c in (0, 1):
        sol.append(f"{cv[c]}: " + "; ".join(s1[c][2]) + f" ⇒ score = {fmt(s1[c][0], 5)}.")
    sol.append(f"Larger score: {cv[sm]}. Answer: <b>{corr}</b>.")
    return Q(text=text, qtype="MCQ", marks=2, options=opts, answer=ans, blocks=[_nb_table(ctx, X, y)], solution=sol)


@template(TOPIC, NB, marks=1, qtype="NAT")
def nb_laplace(rng):
    ctx = NB_CONTEXTS[int(rng.integers(len(NB_CONTEXTS)))]
    feats3 = [(f, v) for f, v in ctx["feats"] if len(v) >= 3]
    fname, vals = feats3[0] if feats3 else ctx["feats"][0]
    V = len(vals)
    while True:
        cnt = rng.integers(0, 7, V)
        if (cnt == 0).sum() >= 1 and cnt.sum() >= 4:
            break
    alpha = int(_pick(rng, [1, 1, 1, 2]))
    c = int(rng.integers(2))
    v = int(np.argmin(cnt)) if rng.random() < 0.5 else int(rng.integers(V))
    N = int(cnt.sum())
    ans = (cnt[v] + alpha) / (N + alpha * V)
    rows = [[fname] + vals, [f"count in {ctx['cls']} = {ctx['cv'][c]}"] + [str(x) for x in cnt]]
    sm = "Laplace (add-one) smoothing" if alpha == 1 else "additive (add-α) smoothing with α = 2"
    text = (f"In a training set, the {N} examples of class {ctx['cls']} = {ctx['cv'][c]} have the following counts for "
            f"the feature <i>{fname}</i>. Using {sm}, the naive Bayes estimate of "
            f"P({fname} = {vals[v]} | {ctx['cls']} = {ctx['cv'][c]}) is ______")
    sol = [f"Add-α estimate: (count + α)/(N<sub>c</sub> + αV) with V = {V} possible values.",
           f"= ({cnt[v]} + {alpha})/({N} + {alpha}×{V}) = {cnt[v] + alpha}/{N + alpha * V} = <b>{fmt(ans, 3)}</b>.",
           f"(The unsmoothed estimate would be {cnt[v]}/{N}" +
           (", i.e. zero, which would wipe out the whole posterior product.)" if cnt[v] == 0 else ".)")]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 3, 0.002), nat_hint=nat_hint(3),
             blocks=[Table(rows, header=False)], solution=sol)


@template(TOPIC, NB, marks=1, qtype="NAT")
def nb_param_count(rng):
    var = int(rng.integers(4))
    d = int(rng.integers(3, 11))
    K = int(rng.integers(2, 5))
    if var == 0:
        ans = K * d + K - 1
        text = (f"A naive Bayes classifier has d = {d} binary features and K = {K} classes. The number of independent "
                f"parameters (class priors plus class-conditional feature probabilities) to be estimated is ______")
        sol = [f"Priors: K − 1 = {K - 1}. Each binary feature needs 1 parameter P(x<sub>j</sub>=1|c) per class: "
               f"Kd = {K * d}.", f"Total = {K * d} + {K - 1} = <b>{ans}</b>."]
    elif var == 1:
        d = int(rng.integers(3, 8))
        ans = K * (2 ** d - 1) + K - 1
        text = (f"For K = {K} classes and d = {d} binary features, a Bayes classifier that models the FULL joint "
                f"class-conditional distribution P(x<sub>1</sub>, …, x<sub>d</sub> | c) (no independence assumption) "
                f"needs how many independent parameters, including the class priors? ______")
        sol = [f"Each class-conditional joint over 2<super>{d}</super> = {2 ** d} configurations needs "
               f"2<super>{d}</super> − 1 = {2 ** d - 1} parameters; for K classes: {K * (2 ** d - 1)}.",
               f"Priors: K − 1 = {K - 1}. Total = <b>{ans}</b>.",
               f"Naive Bayes would need only Kd + K − 1 = {K * d + K - 1} — linear rather than exponential in d."]
    elif var == 2:
        ans = 2 * K * d + K - 1
        text = (f"A Gaussian naive Bayes classifier has d = {d} continuous features and K = {K} classes, with a separate "
                f"mean and variance for every (feature, class) pair. The number of independent parameters, including "
                f"class priors, is ______")
        sol = [f"Means: Kd = {K * d}; variances: Kd = {K * d}; priors: K − 1 = {K - 1}.",
               f"Total = 2Kd + K − 1 = <b>{ans}</b>."]
    else:
        m = int(rng.integers(3, 6))
        ans = K * d * (m - 1) + K - 1
        text = (f"A categorical naive Bayes classifier has d = {d} features, each taking m = {m} possible values, and "
                f"K = {K} classes. The number of independent parameters, including class priors, is ______")
        sol = [f"For each class and feature, a distribution over m values has m − 1 = {m - 1} free parameters: "
               f"Kd(m − 1) = {K * d * (m - 1)}.", f"Priors: K − 1 = {K - 1}. Total = <b>{ans}</b>."]
    return Q(text=text, qtype="NAT", marks=1, answer=(float(ans), float(ans)), nat_hint=nat_hint(0), solution=sol)


@template(TOPIC, NB, marks=2, qtype="NAT")
def nb_gaussian(rng):
    p = int(rng.integers(1, 3))
    while True:
        mu = rng.integers(0, 9, (2, p)).astype(float)
        var = rng.choice([1.0, 2.0, 4.0], (2, p))
        pri1 = float(_pick(rng, [0.3, 0.4, 0.5, 0.6, 0.7]))
        x = rng.integers(0, 9, p).astype(float) + float(_pick(rng, [0, 0.5]))
        if (mu[0] == mu[1]).all():
            continue
        lik = [np.prod([_gauss(x[j], mu[c, j], var[c, j]) for j in range(p)]) for c in (0, 1)]
        pri = [1 - pri1, pri1]
        s = [pri[c] * lik[c] for c in (0, 1)]
        if min(s) == 0:
            continue
        post = s[1] / (s[0] + s[1])
        if 0.05 < post < 0.95:
            break
    feats = ", ".join(f"x<sub>{j + 1}</sub>" for j in range(p))
    rows = [["class", "prior"] + sum([[f"μ (x<sub>{j + 1}</sub>)", f"σ² (x<sub>{j + 1}</sub>)"] for j in range(p)], [])]
    for c in (0, 1):
        rows.append([f"C<sub>{c}</sub>", fmt(pri[c])] + sum([[fmt(mu[c, j]), fmt(var[c, j])] for j in range(p)], []))
    xs = "(" + ", ".join(fmt(v) for v in x) + ")" if p > 1 else fmt(x[0])
    text = (f"A Gaussian naive Bayes classifier with feature{'s' if p > 1 else ''} {feats} has the class priors and "
            f"per-class Gaussian parameters below (σ² = variance). For the input x = {xs}, the posterior probability "
            f"P(C<sub>1</sub> | x) is ______")
    sol = ["N(x; μ, σ²) = exp(−(x−μ)²/(2σ²))/√(2πσ²). Naive Bayes multiplies the per-feature densities."]
    for c in (0, 1):
        parts = [f"N({fmt(x[j])}; {fmt(mu[c, j])}, {fmt(var[c, j])}) = {fmt(_gauss(x[j], mu[c, j], var[c, j]), 5)}"
                 for j in range(p)]
        sol.append(f"C<sub>{c}</sub>: " + " × ".join(parts) + f"; × prior {fmt(pri[c])} ⇒ {fmt(s[c], 6)}.")
    sol.append(f"P(C<sub>1</sub> | x) = {fmt(s[1], 6)}/({fmt(s[0], 6)} + {fmt(s[1], 6)}) = <b>{fmt(post, 2)}</b>.")
    muc, vc, xc = mu.copy(), var.copy(), x.copy()

    def draw(fig):
        for j in range(p):
            ax = fig.add_subplot(1, p, j + 1)
            lo = min(muc[:, j].min() - 3 * math.sqrt(vc[:, j].max()), xc[j] - 1)
            hi = max(muc[:, j].max() + 3 * math.sqrt(vc[:, j].max()), xc[j] + 1)
            t = np.linspace(lo, hi, 300)
            for c, ls in ((0, "-"), (1, "--")):
                ax.plot(t, [_gauss(v, muc[c, j], vc[c, j]) for v in t], ls=ls, color=DARK if c == 0 else MID,
                        label=f"p(x$_{j + 1}$|C$_{c}$)")
            ax.axvline(xc[j], color=LIGHT, lw=1.2)
            ax.set_xlabel(f"x$_{j + 1}$")
            ax.legend(frameon=False, fontsize=6)
            ax.set_yticks([])
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(post, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows), Figure(draw, 6.5 * p + 2, 4.5)], solution=sol)


NB_TRUE = [
    ("Naive Bayes assumes the features are conditionally independent given the class.",
     "P(x<sub>1</sub>,…,x<sub>d</sub>|c) = Π P(x<sub>j</sub>|c)."),
    ("Naive Bayes is a generative classifier: it models P(x | y) and P(y).", "Classification then uses Bayes' rule."),
    ("With d binary features and K classes, naive Bayes needs Kd + K − 1 independent parameters.",
     "Kd Bernoulli parameters + K − 1 priors."),
    ("Without smoothing, a feature value never observed with class c in training forces the posterior of c to 0 for "
     "any input containing that value.", "One zero factor makes the product zero (zero-frequency problem)."),
    ("Laplace smoothing adds a pseudo-count (typically 1) to every feature-value count within each class.",
     "Estimate becomes (n<sub>v,c</sub> + 1)/(n<sub>c</sub> + V)."),
    ("Naive Bayes can classify accurately even when the independence assumption is violated, since only the arg max "
     "of the posterior matters.", "Probability estimates may be poor while the ranking of classes is still right."),
    ("Gaussian naive Bayes corresponds to Gaussian class-conditionals with diagonal covariance matrices.",
     "Independence of Gaussian features given the class ⇔ diagonal covariance."),
    ("In practice, naive Bayes sums log-probabilities to avoid numerical underflow.",
     "Products of many small probabilities underflow."),
    ("Maximum-likelihood training of categorical naive Bayes requires only counting (closed form).",
     "Estimates are relative frequencies."),
    ("The number of naive Bayes parameters grows linearly with the number of features d.",
     "Each feature adds K(m − 1) parameters."),
    ("Gaussian naive Bayes with class-specific variances generally yields a quadratic decision boundary.",
     "Log-ratio contains x<sub>j</sub>² terms with coefficients (1/σ<sub>j0</sub>² − 1/σ<sub>j1</sub>²)/2."),
    ("If a feature is duplicated, naive Bayes counts its evidence twice.",
     "The duplicated factor appears twice in the product, overstating confidence."),
    ("Multinomial naive Bayes is a standard baseline for text classification using word counts.",
     "Words are treated as conditionally independent draws given the class."),
    ("Naive Bayes posterior probabilities are often over-confident (close to 0 or 1) when features are correlated.",
     "Correlated evidence is counted multiple times."),
]
NB_FALSE = [
    ("Naive Bayes assumes the features are marginally (unconditionally) independent.",
     "The assumption is conditional independence given the class."),
    ("Naive Bayes is a discriminative classifier that models P(y | x) directly.", "It is generative."),
    ("Laplace smoothing is used mainly to reduce the number of parameters of naive Bayes.",
     "It avoids zero probability estimates; the parameter count is unchanged."),
    ("Fitting categorical naive Bayes requires iterative gradient-based optimisation.", "MLEs are closed-form frequencies."),
    ("The number of parameters of naive Bayes grows exponentially with the number of features.",
     "That is the full joint model; naive Bayes is linear in d."),
    ("Gaussian naive Bayes estimates a full covariance matrix for each class.", "It uses diagonal covariances."),
    ("Naive Bayes cannot be applied to problems with more than two classes.", "It handles any K."),
    ("Whenever the independence assumption is violated, naive Bayes predicts the wrong class.",
     "It often still predicts correctly."),
    ("With Laplace (add-one) smoothing, a feature value with zero count in a class still gets probability 0.",
     "It gets 1/(n<sub>c</sub> + V) &gt; 0."),
    ("The Laplace-smoothed estimate (n<sub>v,c</sub> + 1)/(n<sub>c</sub> + V) does not depend on the number V of "
     "possible feature values.", "V appears in the denominator."),
    ("Duplicating a feature has no effect on naive Bayes predictions.", "The evidence is counted twice."),
    ("Naive Bayes posterior probabilities are always well calibrated.", "They are often over-confident."),
    ("Under the naive Bayes assumption, P(x<sub>1</sub>, x<sub>2</sub>) = P(x<sub>1</sub>)P(x<sub>2</sub>) for any two features.",
     "Only the class-conditional factorisation holds; marginally the features are usually dependent."),
]


@template(TOPIC, NB, marks=1, qtype="MSQ")
def nb_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, NB_TRUE, NB_FALSE)
    return Q(text="Which of the following statements about naive Bayes classifiers is/are CORRECT?", qtype="MSQ",
             marks=1, options=opts, answer=ans, solution=expl)


# =============================================================================
# LDA / QDA / FISHER
# =============================================================================
SIGS = [[[2, 1], [1, 2]], [[1, 0], [0, 2]], [[3, 1], [1, 2]], [[2, -1], [-1, 2]], [[4, 2], [2, 3]],
        [[1, 0.5], [0.5, 1]], [[2, 0], [0, 1]], [[3, -1], [-1, 2]], [[5, 2], [2, 2]], [[2, 1], [1, 3]]]


@template(TOPIC, LDA, marks=2, qtype="NAT")
def lda_1d_threshold(rng):
    while True:
        m0 = float(rng.integers(0, 6))
        m1 = m0 + float(rng.integers(2, 6))
        s2 = float(_pick(rng, [1, 2, 4, 9]))
        p1 = float(_pick(rng, [0.2, 0.25, 0.3, 0.4, 0.6, 0.7, 0.75, 0.8]))
        p0 = 1 - p1
        xs = (m0 + m1) / 2 + s2 * math.log(p0 / p1) / (m1 - m0)
        var = int(rng.integers(2))
        if var == 0:
            ans = xs
            ask = "the Bayes-optimal (minimum-error) decision threshold x*"
        else:
            xq = float(rng.integers(int(m0), int(m1) + 1))
            a = (m1 - m0) / s2
            c = -(m1 ** 2 - m0 ** 2) / (2 * s2) + math.log(p1 / p0)
            ans = _sig(a * xq + c)
            ask = f"the posterior probability P(C<sub>1</sub> | x = {fmt(xq)})"
            if not 0.03 < ans < 0.97:
                continue
        break
    text = (f"In a two-class problem with one feature, p(x | C<sub>0</sub>) = N({fmt(m0)}, {fmt(s2)}) and "
            f"p(x | C<sub>1</sub>) = N({fmt(m1)}, {fmt(s2)}) (second argument = variance), with priors "
            f"P(C<sub>0</sub>) = {fmt(p0)} and P(C<sub>1</sub>) = {fmt(p1)}. Under 0-1 loss, {ask} is ______")
    sol = ["With equal variances, ln[π<sub>1</sub>p(x|C<sub>1</sub>)/(π<sub>0</sub>p(x|C<sub>0</sub>))] = "
           "(μ<sub>1</sub>−μ<sub>0</sub>)x/σ² − (μ<sub>1</sub>²−μ<sub>0</sub>²)/(2σ²) + ln(π<sub>1</sub>/π<sub>0</sub>) "
           "— linear in x (LDA)."]
    if var == 0:
        sol += [f"Setting it to 0: x* = (μ<sub>0</sub>+μ<sub>1</sub>)/2 + σ² ln(π<sub>0</sub>/π<sub>1</sub>)/"
                f"(μ<sub>1</sub>−μ<sub>0</sub>) = {fmt((m0 + m1) / 2)} + {fmt(s2)}×ln({fmt(p0)}/{fmt(p1)})/{fmt(m1 - m0)}.",
                f"= {fmt((m0 + m1) / 2)} + ({fmt(s2 * math.log(p0 / p1) / (m1 - m0), 4)}) = <b>{fmt(xs, 2)}</b>.",
                f"The threshold moves away from the more probable class C<sub>{0 if p0 > p1 else 1}</sub>'s mean, "
                f"enlarging its decision region."]
    else:
        sol += [f"Slope a = (μ<sub>1</sub>−μ<sub>0</sub>)/σ² = {fmt(a, 4)}; intercept c = −(μ<sub>1</sub>²−μ<sub>0</sub>²)/(2σ²)"
                f" + ln(π<sub>1</sub>/π<sub>0</sub>) = {fmt(c, 4)}.",
                f"P(C<sub>1</sub>|x) = σ(a x + c) = σ({fmt(a * xq + c, 4)}) = <b>{fmt(ans, 2)}</b>."]
    M0, M1, S = m0, m1, s2

    def draw(fig):
        ax = fig.add_subplot(111)
        sd = math.sqrt(S)
        t = np.linspace(M0 - 3.2 * sd, M1 + 3.2 * sd, 300)
        ax.plot(t, [_gauss(v, M0, S) for v in t], color=DARK, label="p(x|C$_0$)")
        ax.plot(t, [_gauss(v, M1, S) for v in t], color=MID, ls="--", label="p(x|C$_1$)")
        ax.set_xlabel("x")
        ax.set_yticks([])
        ax.grid(alpha=.3)
        ax.legend(frameon=False)
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Figure(draw, 9, 4.5, caption="Class-conditional densities (not weighted by priors).")],
             solution=sol)


@template(TOPIC, LDA, marks=1, qtype="MCQ")
def lda_prior_shift(rng):
    m0 = float(rng.integers(0, 4))
    m1 = m0 + float(rng.integers(3, 6))
    j = int(rng.integers(2))
    pj = float(_pick(rng, [0.7, 0.8, 0.9]))
    mu = [m0, m1]
    other = 1 - j
    corr = f"It moves towards x = {fmt(mu[other])}, enlarging the region assigned to C<sub>{j}</sub>"
    dis = [f"It moves towards x = {fmt(mu[j])}, shrinking the region assigned to C<sub>{j}</sub>",
           f"It stays at x = {fmt((m0 + m1) / 2)} because the two variances are equal",
           f"It moves towards x = {fmt(mu[j])}, enlarging the region assigned to C<sub>{j}</sub>",
           "It splits into two thresholds, giving a quadratic boundary"]
    opts, ans = mcq(rng, corr, dis)

    def draw(fig):
        ax = fig.add_subplot(111)
        t = np.linspace(m0 - 3.5, m1 + 3.5, 300)
        ax.plot(t, [_gauss(v, m0, 1) for v in t], color=DARK, label="p(x|C$_0$)")
        ax.plot(t, [_gauss(v, m1, 1) for v in t], color=MID, ls="--", label="p(x|C$_1$)")
        ax.axvline((m0 + m1) / 2, color=LIGHT, ls=":", lw=1.2)
        ax.set_xticks(np.arange(math.floor(m0 - 3), math.ceil(m1 + 4)))
        ax.set_xlabel("x")
        ax.set_yticks([])
        ax.legend(frameon=False)
    text = (f"Two classes have unit-variance Gaussian class-conditional densities with means {fmt(m0)} (C<sub>0</sub>) "
            f"and {fmt(m1)} (C<sub>1</sub>), as plotted. With equal priors the Bayes decision threshold is the dotted "
            f"line at x = {fmt((m0 + m1) / 2)}. If the prior of C<sub>{j}</sub> is increased to {fmt(pj)}, the "
            f"threshold")
    xs = (m0 + m1) / 2 + math.log((1 - pj if j == 1 else pj) / (pj if j == 1 else 1 - pj)) / (m1 - m0)
    sol = [f"x* = (μ<sub>0</sub>+μ<sub>1</sub>)/2 + σ² ln(π<sub>0</sub>/π<sub>1</sub>)/(μ<sub>1</sub>−μ<sub>0</sub>) = "
           f"{fmt(xs, 3)}.",
           f"A larger prior for C<sub>{j}</sub> means more of the x-axis is assigned to it, so the threshold moves away "
           f"from μ<sub>{j}</sub> towards μ<sub>{other}</sub> = {fmt(mu[other])}. Answer: <b>{corr}</b>.",
           "Equal variances keep the boundary a single point (linear); priors shift it but never make it quadratic."]
    return Q(text=text, qtype="MCQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 9, 4.3)], solution=sol)


@template(TOPIC, LDA, marks=2, qtype="NAT")
def lda_discriminant_2d(rng):
    while True:
        S = np.array(SIGS[int(rng.integers(len(SIGS)))], float)
        Si = np.linalg.inv(S)
        M = rng.integers(-2, 4, (3, 2)).astype(float)
        if len({tuple(r) for r in M}) < 3:
            continue
        pri = np.array(_pick(rng, [(0.5, 0.3, 0.2), (0.2, 0.3, 0.5), (0.4, 0.4, 0.2), (1 / 3, 1 / 3, 1 / 3),
                                   (0.25, 0.25, 0.5), (0.6, 0.2, 0.2)]))
        x = rng.integers(-2, 4, 2).astype(float)
        delta = np.array([x @ Si @ M[k] - 0.5 * M[k] @ Si @ M[k] + math.log(pri[k]) for k in range(3)])
        sd = np.sort(delta)
        if sd[2] - sd[1] < 0.15:
            continue
        break
    var = int(rng.integers(2))
    if var == 0:
        k = int(rng.integers(3))
        ans, dd = delta[k], 2
        ask = f"the value of the discriminant function δ<sub>{k + 1}</sub>(<b>x</b>)"
    else:
        ans, dd = float(np.argmax(delta) + 1), 0
        ask = "the index k ∈ {1, 2, 3} of the class predicted by LDA"
    prs = ", ".join(f"π<sub>{k + 1}</sub> = {fmt(pri[k], 3) if pri[k] != 1 / 3 else '1/3'}" for k in range(3))
    mus = "; ".join(f"μ<sub>{k + 1}</sub> = ({fmt(M[k, 0])}, {fmt(M[k, 1])})ᵀ" for k in range(3))
    text = (f"An LDA classifier for 3 classes has shared covariance matrix Σ (below), class means {mus}, and priors "
            f"{prs}. The linear discriminant is δ<sub>k</sub>(<b>x</b>) = <b>x</b>ᵀΣ<super>−1</super>μ<sub>k</sub> − "
            f"½μ<sub>k</sub>ᵀΣ<super>−1</super>μ<sub>k</sub> + ln π<sub>k</sub> (natural log). For "
            f"<b>x</b> = ({fmt(x[0])}, {fmt(x[1])})ᵀ, {ask} is ______")
    sol = [Matrix("Σ⁻¹", Si, 3)]
    for k in range(3):
        a = Si @ M[k]
        sol.append(f"k = {k + 1}: Σ⁻¹μ<sub>{k + 1}</sub> = ({fmt(a[0], 4)}, {fmt(a[1], 4)}); "
                   f"<b>x</b>ᵀΣ⁻¹μ = {fmt(x @ a, 4)}; ½μᵀΣ⁻¹μ = {fmt(0.5 * M[k] @ a, 4)}; ln π = {fmt(math.log(pri[k]), 4)} "
                   f"⇒ δ<sub>{k + 1}</sub> = {fmt(delta[k], 4)}.")
    if var == 0:
        sol.append(f"Required δ<sub>{k + 1}</sub>(<b>x</b>) = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"The largest discriminant is δ<sub>{int(ans)}</sub> ⇒ predicted class <b>{int(ans)}</b>.")
    Mc, xc = M.copy(), x.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        for k, mk in enumerate(["o", "s", "^"]):
            ax.scatter([Mc[k, 0]], [Mc[k, 1]], marker=mk, s=50, facecolor="white" if k else DARK, edgecolor=DARK,
                       zorder=3, label=f"μ$_{k + 1}$")
        ax.scatter([xc[0]], [xc[1]], marker="*", s=120, color=MID, zorder=4, label="x")
        ax.set_xlim(-3, 4)
        ax.set_ylim(-3, 4)
        ax.set_aspect("equal")
        ax.grid(alpha=.3)
        ax.set_xlabel("x$_1$")
        ax.set_ylabel("x$_2$")
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    ans_r = nat_range(ans, 2) if dd else (ans, ans)
    return Q(text=text, qtype="NAT", marks=2, answer=ans_r, nat_hint=nat_hint(dd),
             blocks=[Matrix("Σ", S, 1), Figure(draw, 8, 5.5)], solution=sol)


@template(TOPIC, LDA, marks=2, qtype="NAT")
def fisher_given_sw(rng):
    while True:
        Sw = np.array(SIGS[int(rng.integers(len(SIGS)))], float) * float(_pick(rng, [1, 2, 4]))
        m0 = rng.integers(-2, 4, 2).astype(float)
        m1 = rng.integers(-2, 5, 2).astype(float)
        dm = m1 - m0
        if (dm == 0).all():
            continue
        w = np.linalg.solve(Sw, dm)
        var = int(rng.integers(3))
        if var == 0:
            if abs(w[0]) < 1e-9:
                continue
            ans = w[1] / w[0]
            ask = "the ratio w<sub>2</sub>/w<sub>1</sub> of the components of the Fisher discriminant direction <b>w</b>"
            if abs(ans) > 10:
                continue
        elif var == 1:
            ans = w @ (m0 + m1) / 2
            ask = ("the projection threshold c = <b>w</b>ᵀ(μ<sub>0</sub> + μ<sub>1</sub>)/2, where "
                   "<b>w</b> = S<sub>W</sub><super>−1</super>(μ<sub>1</sub> − μ<sub>0</sub>) (unnormalised)")
        else:
            ans = w @ dm
            ask = ("the separation of the projected class means, <b>w</b>ᵀ(μ<sub>1</sub> − μ<sub>0</sub>), with "
                   "<b>w</b> = S<sub>W</sub><super>−1</super>(μ<sub>1</sub> − μ<sub>0</sub>)")
        break
    text = (f"For a two-class problem, the class means are μ<sub>0</sub> = ({fmt(m0[0])}, {fmt(m0[1])})ᵀ and "
            f"μ<sub>1</sub> = ({fmt(m1[0])}, {fmt(m1[1])})ᵀ and the pooled within-class scatter matrix S<sub>W</sub> is "
            f"given below. Fisher's linear discriminant uses <b>w</b> ∝ S<sub>W</sub><super>−1</super>"
            f"(μ<sub>1</sub> − μ<sub>0</sub>). Then {ask} is ______")
    det = np.linalg.det(Sw)
    sol = [f"μ<sub>1</sub> − μ<sub>0</sub> = ({fmt(dm[0])}, {fmt(dm[1])})ᵀ; det S<sub>W</sub> = {fmt(det, 3)}.",
           Matrix("S<sub>W</sub>⁻¹", np.linalg.inv(Sw), 4),
           f"<b>w</b> = S<sub>W</sub><super>−1</super>(μ<sub>1</sub>−μ<sub>0</sub>) = ({fmt(w[0], 4)}, {fmt(w[1], 4)})ᵀ."]
    if var == 0:
        sol.append(f"w<sub>2</sub>/w<sub>1</sub> = {fmt(w[1], 4)}/{fmt(w[0], 4)} = <b>{fmt(ans, 2)}</b>. "
                   "(The direction, not the length, matters.)")
    elif var == 1:
        sol.append(f"(μ<sub>0</sub>+μ<sub>1</sub>)/2 = ({fmt((m0 + m1)[0] / 2)}, {fmt((m0 + m1)[1] / 2)}); "
                   f"c = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"<b>w</b>ᵀ(μ<sub>1</sub>−μ<sub>0</sub>) = (μ<sub>1</sub>−μ<sub>0</sub>)ᵀS<sub>W</sub><super>−1</super>"
                   f"(μ<sub>1</sub>−μ<sub>0</sub>) = <b>{fmt(ans, 2)}</b> (always ≥ 0 since S<sub>W</sub> is positive definite).")
    sol.append("Note: using μ<sub>1</sub> − μ<sub>0</sub> without S<sub>W</sub><super>−1</super> is correct only when "
               "S<sub>W</sub> ∝ I.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Matrix("S<sub>W</sub>", Sw, 1)], solution=sol)


@template(TOPIC, LDA, marks=2, qtype="NAT")
def fisher_from_data(rng):
    while True:
        A = rng.integers(0, 5, (3, 2)).astype(float)
        B = rng.integers(2, 8, (3, 2)).astype(float)
        if len({tuple(r) for r in np.vstack([A, B])}) < 6:
            continue
        mA, mB = A.mean(0), B.mean(0)
        S = (A - mA).T @ (A - mA) + (B - mB).T @ (B - mB)
        if abs(np.linalg.det(S)) < 2:
            continue
        dm = mB - mA
        if np.allclose(dm, 0):
            continue
        w = np.linalg.solve(S, dm)
        var = int(rng.integers(2))
        if var == 0:
            if abs(w[0]) < 1e-6 or abs(w[1] / w[0]) > 10:
                continue
            ans = w[1] / w[0]
        else:
            ans = dm @ w
        break
    rowsA = ", ".join(f"({fmt(a)}, {fmt(b)})" for a, b in A)
    rowsB = ", ".join(f"({fmt(a)}, {fmt(b)})" for a, b in B)
    ask = ("the ratio w<sub>2</sub>/w<sub>1</sub> of the Fisher direction <b>w</b> ∝ S<sub>W</sub><super>−1</super>"
           "(<b>m</b><sub>2</sub> − <b>m</b><sub>1</sub>)") if var == 0 else \
        ("(<b>m</b><sub>2</sub> − <b>m</b><sub>1</sub>)ᵀS<sub>W</sub><super>−1</super>(<b>m</b><sub>2</sub> − <b>m</b><sub>1</sub>)")
    text = (f"Class ω<sub>1</sub> has training points {rowsA} and class ω<sub>2</sub> has points {rowsB}. "
            f"Let <b>m</b><sub>1</sub>, <b>m</b><sub>2</sub> be the class means and S<sub>W</sub> = "
            f"Σ<sub>k</sub>Σ<sub>x∈ω<sub>k</sub></sub>(x − <b>m</b><sub>k</sub>)(x − <b>m</b><sub>k</sub>)ᵀ the "
            f"within-class scatter matrix (no division by n). Then {ask} is ______")
    SA = (A - mA).T @ (A - mA)
    SB = (B - mB).T @ (B - mB)
    sol = [f"<b>m</b><sub>1</sub> = ({fmt(mA[0], 3)}, {fmt(mA[1], 3)}), <b>m</b><sub>2</sub> = ({fmt(mB[0], 3)}, "
           f"{fmt(mB[1], 3)}).", Matrix("S<sub>1</sub>", SA, 3), Matrix("S<sub>2</sub>", SB, 3), Matrix("S<sub>W</sub>", S, 3),
           f"<b>m</b><sub>2</sub> − <b>m</b><sub>1</sub> = ({fmt(dm[0], 3)}, {fmt(dm[1], 3)}).",
           f"<b>w</b> = S<sub>W</sub><super>−1</super>(<b>m</b><sub>2</sub> − <b>m</b><sub>1</sub>) = "
           f"({fmt(w[0], 4)}, {fmt(w[1], 4)}).",
           (f"w<sub>2</sub>/w<sub>1</sub> = <b>{fmt(ans, 2)}</b>." if var == 0 else
            f"(<b>m</b><sub>2</sub>−<b>m</b><sub>1</sub>)ᵀ<b>w</b> = <b>{fmt(ans, 2)}</b>.")]
    Ac, Bc = A.copy(), B.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        _scatter_classes(ax, np.vstack([Ac, Bc]), np.array([0, 0, 0, 1, 1, 1]), names=("ω₁", "ω₂"))
        ax.set_xlim(-0.7, 8.7)
        ax.set_ylim(-0.7, 8.7)
        ax.set_xticks(range(9))
        ax.set_yticks(range(9))
        ax.set_aspect("equal")
        ax.grid(alpha=.3)
        ax.set_xlabel("x$_1$")
        ax.set_ylabel("x$_2$")
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False)
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Figure(draw, 8, 5.8)], solution=sol)


@template(TOPIC, LDA, marks=1, qtype="NAT")
def lda_param_count(rng):
    p = int(rng.integers(2, 11))
    K = int(rng.integers(2, 6))
    var = int(rng.integers(4))
    cov = p * (p + 1) // 2
    if var == 0:
        ans = (K - 1) + K * p + cov
        text = (f"LDA is fitted with K = {K} classes and p = {p} features. Counting class priors, class means and the "
                f"shared covariance matrix, the number of independent parameters is ______")
        sol = [f"Priors K − 1 = {K - 1}; means Kp = {K * p}; one symmetric covariance p(p+1)/2 = {cov}.",
               f"Total = <b>{ans}</b>."]
    elif var == 1:
        ans = (K - 1) + K * p + K * cov
        text = (f"QDA is fitted with K = {K} classes and p = {p} features. Counting class priors, class means and the "
                f"class-specific covariance matrices, the number of independent parameters is ______")
        sol = [f"Priors K − 1 = {K - 1}; means Kp = {K * p}; K covariances Kp(p+1)/2 = {K * cov}.",
               f"Total = <b>{ans}</b>."]
    elif var == 2:
        ans = (K - 1) * cov
        text = (f"For K = {K} classes and p = {p} features, how many MORE covariance parameters does QDA estimate than "
                f"LDA? ______")
        sol = [f"QDA: K·p(p+1)/2 = {K * cov}; LDA: p(p+1)/2 = {cov}.", f"Difference = (K − 1)p(p+1)/2 = <b>{ans}</b>.",
               "This extra variance is why LDA often beats QDA when n is small."]
    else:
        ans = min(K - 1, p)
        if rng.random() < 0.5:
            K = int(rng.integers(p + 2, p + 6)) if p <= 6 else K
            ans = min(K - 1, p)
        text = (f"Fisher's multi-class LDA is applied to data with K = {K} classes and p = {p} features. The maximum "
                f"number of discriminant directions (non-zero generalised eigenvalues of S<sub>W</sub><super>−1</super>"
                f"S<sub>B</sub>) is ______")
        sol = [f"S<sub>B</sub> is a sum of K outer products of (μ<sub>k</sub> − μ) which are linearly dependent "
               f"(weighted sum is 0), so rank(S<sub>B</sub>) ≤ K − 1 = {K - 1}; also ≤ p = {p}.",
               f"Maximum = min(K − 1, p) = <b>{ans}</b>."]
    return Q(text=text, qtype="NAT", marks=1, answer=(float(ans), float(ans)), nat_hint=nat_hint(0), solution=sol)


LDA_TRUE = [
    ("LDA models each class-conditional density as Gaussian with a covariance matrix Σ common to all classes.",
     "That is the defining assumption."),
    ("With a shared covariance matrix, the Bayes decision boundaries between Gaussian classes are linear.",
     "The quadratic terms xᵀΣ⁻¹x cancel."),
    ("QDA allows each class its own covariance matrix, giving quadratic decision boundaries in general.",
     "The xᵀΣ<sub>k</sub><super>−1</super>x terms no longer cancel."),
    ("Fisher's LDA for K classes yields at most K − 1 discriminant directions.", "rank(S<sub>B</sub>) ≤ K − 1."),
    ("For two classes, Fisher's direction w ∝ S<sub>W</sub><super>−1</super>(μ<sub>1</sub> − μ<sub>0</sub>) maximises "
     "the ratio of between-class to within-class variance of the projections.", "Solution of the Rayleigh quotient."),
    ("Both LDA and logistic regression yield log-posterior-odds that are linear in x; they differ in how the "
     "parameters are estimated.", "LDA maximises the joint likelihood, logistic regression the conditional likelihood."),
    ("Logistic regression is typically more robust than LDA when the class-conditional distributions are far from Gaussian.",
     "It makes no assumption about P(x|y)."),
    ("When the Gaussian shared-covariance assumption holds, LDA can estimate the boundary with lower variance than "
     "logistic regression.", "It uses the extra (correct) distributional information."),
    ("QDA has more parameters than LDA and may overfit when the training set is small.",
     "K covariance matrices instead of one."),
    ("Changing the class priors in LDA shifts the decision boundary but does not change its orientation.",
     "Priors only enter the constant term ln π<sub>k</sub>."),
    ("The LDA discriminant function δ<sub>k</sub>(x) = xᵀΣ<super>−1</super>μ<sub>k</sub> − "
     "½μ<sub>k</sub>ᵀΣ<super>−1</super>μ<sub>k</sub> + ln π<sub>k</sub> is linear in x.", "Only first-order terms in x."),
    ("Under the LDA model with two classes, P(y = 1 | x) has the logistic (sigmoid) form σ(wᵀx + b).",
     "Log-odds are linear in x."),
    ("Unlike unregularised logistic regression, LDA's parameter estimates remain finite when the classes are "
     "perfectly separable (if the pooled covariance is non-singular).", "LDA estimates are sample means and covariances."),
    ("Fisher's criterion J(w) is unchanged if w is multiplied by a non-zero scalar.", "Numerator and denominator scale by c²."),
    ("If the number of features exceeds the number of training points, the pooled covariance estimate is singular "
     "and LDA needs regularisation.", "Sample covariance has rank at most n − K."),
]
LDA_FALSE = [
    ("LDA estimates a separate covariance matrix for each class.", "That is QDA."),
    ("QDA always produces a linear decision boundary.", "Generally quadratic."),
    ("Fisher's LDA with K classes can always find K discriminant directions.", "At most K − 1."),
    ("Fisher's two-class direction is always w ∝ μ<sub>1</sub> − μ<sub>0</sub>, regardless of S<sub>W</sub>.",
     "Only when S<sub>W</sub> ∝ I."),
    ("Logistic regression assumes Gaussian class-conditional densities.", "It makes no assumption on P(x|y)."),
    ("LDA is a discriminative model that never models P(x | y).", "LDA is generative."),
    ("QDA has fewer parameters than LDA.", "It has (K − 1)p(p+1)/2 more."),
    ("Changing the class priors in LDA rotates the decision boundary.", "Priors only shift it."),
    ("LDA and logistic regression always produce identical coefficient estimates.", "Different estimation criteria."),
    ("Fisher's LDA chooses w to maximise the within-class scatter of the projected data.",
     "It minimises within-class scatter relative to between-class scatter."),
    ("LDA cannot be used for problems with more than two classes.", "It handles K classes."),
    ("Fisher's LDA directions coincide with the directions of maximum total variance found by PCA.",
     "PCA ignores labels; LDA uses them."),
    ("With a shared covariance matrix, unequal class priors make the LDA boundary quadratic.",
     "Priors add only a constant; the boundary stays linear."),
]


@template(TOPIC, LDA, marks=2, qtype="MSQ")
def lda_qda_lr_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, LDA_TRUE, LDA_FALSE)
    return Q(text="Which of the following statements about LDA, QDA and logistic regression is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, solution=expl)


# =============================================================================
# BAYES OPTIMAL / DECISION THEORY
# =============================================================================
@template(TOPIC, BAYES, marks=2, qtype="NAT")
def bayes_error_uniform(rng):
    while True:
        a = int(rng.integers(3, 9))
        b = int(rng.integers(1, a))
        c = int(rng.integers(a + 1, 12))
        p0 = float(_pick(rng, [0.3, 0.4, 0.5, 0.6, 0.7]))
        p1 = 1 - p0
        h0, h1 = p0 / a, p1 / (c - b)
        if abs(h0 - h1) < 1e-9:
            continue
        break
    var = int(rng.integers(2))
    ov = a - b
    if var == 0:
        ans = ov * min(h0, h1)
        ask = "the Bayes (minimum achievable) error rate"
        win = 0 if h0 > h1 else 1
        sol = [f"π<sub>0</sub>p(x|C<sub>0</sub>) = {fmt(p0)}/{a} = {fmt(h0, 4)} on [0, {a}]; "
               f"π<sub>1</sub>p(x|C<sub>1</sub>) = {fmt(p1)}/{c - b} = {fmt(h1, 4)} on [{b}, {c}].",
               f"Outside the overlap [{b}, {a}] only one class has non-zero density ⇒ no error. Inside it the Bayes rule "
               f"chooses C<sub>{win}</sub> (larger weighted density) and errs with density {fmt(min(h0, h1), 4)}.",
               f"Bayes error = (overlap length) × min = {ov} × {fmt(min(h0, h1), 4)} = <b>{fmt(ans, 3)}</b>."]
    else:
        t = float(rng.integers(b, a)) + 0.5
        ans = p0 * (a - t) / a + p1 * (t - b) / (c - b)
        ask = (f"the error rate of the rule \"predict C<sub>0</sub> if x &lt; {fmt(t)}, else C<sub>1</sub>\"")
        sol = [f"P(error) = π<sub>0</sub>P(x ≥ {fmt(t)} | C<sub>0</sub>) + π<sub>1</sub>P(x &lt; {fmt(t)} | C<sub>1</sub>).",
               f"= {fmt(p0)}×({a} − {fmt(t)})/{a} + {fmt(p1)}×({fmt(t)} − {b})/{c - b} = "
               f"{fmt(p0 * (a - t) / a, 4)} + {fmt(p1 * (t - b) / (c - b), 4)} = <b>{fmt(ans, 3)}</b>.",
               f"(For comparison, the Bayes error is {fmt(ov * min(h0, h1), 4)}: the Bayes rule assigns the whole "
               f"overlap to the class with the larger π<sub>k</sub>p(x|C<sub>k</sub>).)"]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot([0, 0, a, a], [0, 1 / a, 1 / a, 0], color=DARK, lw=1.5, label="p(x|C$_0$)")
        ax.plot([b, b, c, c], [0, 1 / (c - b), 1 / (c - b), 0], color=MID, lw=1.5, ls="--", label="p(x|C$_1$)")
        ax.set_xticks(range(0, c + 2))
        ax.set_xlim(-0.5, c + 1)
        ax.set_ylim(0, max(1 / a, 1 / (c - b)) * 1.4)
        ax.set_xlabel("x")
        ax.set_ylabel("density")
        ax.grid(alpha=.3)
        ax.legend(frameon=False)
    text = (f"For a binary problem with scalar x, p(x | C<sub>0</sub>) is uniform on [0, {a}] and p(x | C<sub>1</sub>) is "
            f"uniform on [{b}, {c}], with priors P(C<sub>0</sub>) = {fmt(p0)} and P(C<sub>1</sub>) = {fmt(p1)}. Then "
            f"{ask} is ______")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.002), nat_hint=nat_hint(3),
             blocks=[Figure(draw, 8.5, 4.5)], solution=sol)


@template(TOPIC, BAYES, marks=2, qtype="NAT")
def bayes_error_discrete(rng):
    m = int(rng.integers(4, 6))
    while True:
        P0 = rng.multinomial(10, rng.dirichlet(np.ones(m) * 1.2)) / 10
        P1 = rng.multinomial(10, rng.dirichlet(np.ones(m) * 1.2)) / 10
        pi1 = float(_pick(rng, [0.3, 0.4, 0.5, 0.6]))
        pi0 = 1 - pi1
        j0, j1 = pi0 * P0, pi1 * P1
        err = np.minimum(j0, j1).sum()
        if 0.03 < err < 0.45:
            break
    var = int(rng.integers(2))
    if var == 0:
        ans = err
        ask = "the Bayes error rate of the optimal classifier"
        sol = ["Bayes rule: choose the class with larger π<sub>k</sub>P(x|k). Bayes error = Σ<sub>x</sub> "
               "min(π<sub>0</sub>P(x|0), π<sub>1</sub>P(x|1)).",
               Table([["x", "π₀P(x|0)", "π₁P(x|1)", "decision", "min"]] +
                     [[str(i + 1), fmt(j0[i], 3), fmt(j1[i], 3), "1" if j1[i] > j0[i] else ("0" if j0[i] > j1[i] else "tie"),
                       fmt(min(j0[i], j1[i]), 3)] for i in range(m)]),
               f"Bayes error = <b>{fmt(ans, 3)}</b>."]
    else:
        while True:
            v = int(rng.integers(m))
            if j0[v] + j1[v] > 0:
                break
        ans = j1[v] / (j0[v] + j1[v])
        ask = f"the posterior probability P(y = 1 | x = {v + 1})"
        sol = [f"P(y=1|x={v + 1}) = π<sub>1</sub>P(x|1)/(π<sub>0</sub>P(x|0) + π<sub>1</sub>P(x|1)) = "
               f"{fmt(j1[v], 3)}/({fmt(j0[v], 3)} + {fmt(j1[v], 3)}) = <b>{fmt(ans, 3)}</b>."]
    rows = [["x"] + [str(i + 1) for i in range(m)], ["P(x | y=0)"] + [fmt(v_) for v_ in P0],
            ["P(x | y=1)"] + [fmt(v_) for v_ in P1]]
    text = (f"A discrete feature x ∈ {{1, …, {m}}} has the class-conditional distributions below (also plotted), with "
            f"priors P(y = 0) = {fmt(pi0)} and P(y = 1) = {fmt(pi1)}. Then {ask} is ______")
    P0c, P1c = P0.copy(), P1.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        xs = np.arange(1, m + 1)
        ax.bar(xs - 0.18, P0c, 0.36, color=DARK, label="P(x|y=0)")
        ax.bar(xs + 0.18, P1c, 0.36, color="white", edgecolor=DARK, hatch="///", label="P(x|y=1)")
        ax.set_xticks(xs)
        ax.set_xlabel("x")
        ax.set_ylabel("probability")
        ax.grid(alpha=.3, axis="y")
        ax.legend(frameon=False)
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.002), nat_hint=nat_hint(3),
             blocks=[Table(rows, header=False), Figure(draw, 8, 4.3)], solution=sol)


@template(TOPIC, BAYES, marks=2, qtype="NAT")
def bayes_loss_matrix(rng):
    want_diff = rng.random() < 0.6
    for _ in range(5000):
        p = rng.multinomial(10, [1 / 3] * 3) / 10
        if p.min() < 0.1 or len(set(p)) < 3:
            continue
        L = rng.integers(1, 11, (3, 3)).astype(float)
        np.fill_diagonal(L, 0)
        R = L @ p
        sr = np.sort(R)
        if sr[1] - sr[0] < 0.1:
            continue
        a_opt, a_map = int(np.argmin(R)), int(np.argmax(p))
        if want_diff and a_opt == a_map:
            continue
        break
    var = int(rng.integers(3))
    if var == 0:
        ans, d_, ask = R[a_opt], 2, "the minimum conditional risk (expected loss) achievable for this x"
    elif var == 1:
        ans, d_, ask = float(a_opt + 1), 0, "the index i of the Bayes-optimal (minimum-risk) action α<sub>i</sub>"
    else:
        ans, d_, ask = R[a_map], 2, ("the conditional risk of the action chosen by the MAP rule "
                                     "(i.e. choosing the class with highest posterior)")
    rows = [["loss L(α<sub>i</sub>, C<sub>j</sub>)", "true C₁", "true C₂", "true C₃"]] + \
           [[f"α<sub>{i + 1}</sub>: decide C<sub>{i + 1}</sub>"] + [fmt(L[i, j]) for j in range(3)] for i in range(3)]
    text = (f"For an input x, a classifier's posterior probabilities are P(C<sub>1</sub>|x) = {fmt(p[0])}, "
            f"P(C<sub>2</sub>|x) = {fmt(p[1])}, P(C<sub>3</sub>|x) = {fmt(p[2])}. The loss of taking action "
            f"α<sub>i</sub> (deciding C<sub>i</sub>) when the true class is C<sub>j</sub> is given below. Then {ask} is ______")
    sol = ["Conditional risk R(α<sub>i</sub>|x) = Σ<sub>j</sub> L(α<sub>i</sub>, C<sub>j</sub>)P(C<sub>j</sub>|x):"]
    for i in range(3):
        sol.append(f"R(α<sub>{i + 1}</sub>) = " + " + ".join(f"{fmt(L[i, j])}×{fmt(p[j])}" for j in range(3)) +
                   f" = {fmt(R[i], 2)}")
    sol.append(f"Minimum risk: α<sub>{a_opt + 1}</sub> with R = {fmt(R[a_opt], 2)}. The MAP rule picks "
               f"C<sub>{a_map + 1}</sub> (risk {fmt(R[a_map], 2)})" +
               (" — the same action here." if a_opt == a_map else " — different, because the losses are asymmetric."))
    sol.append(f"Answer: <b>{fmt(ans, d_)}</b>.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, d_) if d_ else (ans, ans), nat_hint=nat_hint(d_),
             blocks=[Table(rows)], solution=sol)


@template(TOPIC, BAYES, marks=1, qtype="NAT")
def bayes_cost_threshold(rng):
    cfp = int(rng.integers(1, 11))
    cfn = int(rng.integers(1, 21))
    while cfn == cfp:
        cfn = int(rng.integers(1, 21))
    ctx = _pick(rng, [("a disease screening test", "patient has the disease"),
                      ("a fraud detector", "transaction is fraudulent"),
                      ("a spam filter", "email is spam"), ("a defect detector", "part is defective")])
    var = int(rng.integers(2))
    if var == 0:
        ans = cfp / (cfp + cfn)
        text = (f"In {ctx[0]}, a false negative costs {cfn} units and a false positive costs {cfp} units (correct "
                f"decisions cost 0). The model outputs p = P(positive | x), i.e. the probability that the {ctx[1]}. "
                f"The Bayes-optimal rule predicts positive iff p exceeds the threshold ______")
        sol = [f"Expected cost of predicting positive = (1 − p)·C<sub>FP</sub>; of predicting negative = p·C<sub>FN</sub>.",
               f"Predict positive iff p·{cfn} &gt; (1 − p)·{cfp} ⇔ p &gt; C<sub>FP</sub>/(C<sub>FP</sub> + C<sub>FN</sub>) = "
               f"{cfp}/{cfp + cfn} = <b>{fmt(ans, 2)}</b>."]
    else:
        p = float(_pick(rng, [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8]))
        r_pos, r_neg = (1 - p) * cfp, p * cfn
        ans = min(r_pos, r_neg)
        text = (f"In {ctx[0]}, a false negative costs {cfn} units and a false positive costs {cfp} units (correct "
                f"decisions cost 0). For an input x the model gives P(positive | x) = {fmt(p)}. The expected cost of the "
                f"Bayes-optimal decision for this x is ______")
        sol = [f"Predict positive: (1 − {fmt(p)})×{cfp} = {fmt(r_pos, 2)}. Predict negative: {fmt(p)}×{cfn} = {fmt(r_neg, 2)}.",
               f"Optimal decision: {'positive' if r_pos < r_neg else 'negative'}; expected cost = <b>{fmt(ans, 2)}</b>."]
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)


GD_TRUE = [
    ("Under 0-1 loss, the Bayes classifier predicts arg max<sub>k</sub> P(y = k | x) and minimises the probability of "
     "misclassification.", "This is the MAP rule."),
    ("The Bayes error rate is the lowest error rate achievable by any classifier for the given joint distribution of (x, y).",
     "It is the error of the Bayes classifier."),
    ("If the class-conditional densities have non-overlapping supports, the Bayes error rate is zero.",
     "Every x can be assigned to its only possible class."),
    ("Generative classifiers model P(x | y) and P(y), and obtain P(y | x) through Bayes' rule.", "e.g. naive Bayes, LDA, QDA."),
    ("Discriminative classifiers model P(y | x) (or a decision function) directly.", "e.g. logistic regression, SVM."),
    ("A generative model can be used to sample synthetic input vectors x.", "It models the distribution of x."),
    ("With a general loss matrix, the Bayes-optimal action minimises Σ<sub>j</sub> L(α, j) P(j | x).",
     "Minimum conditional risk rule."),
    ("Naive Bayes, LDA and QDA are generative; logistic regression is discriminative.", "Standard classification."),
    ("Collecting more training data (with the same features) cannot reduce the Bayes error rate.",
     "It is a property of the true distribution."),
    ("Adding a new informative feature can reduce the Bayes error rate.", "The classes may overlap less in the larger space."),
    ("Increasing the prior of one class enlarges the region of input space assigned to that class by the Bayes rule.",
     "π<sub>k</sub> multiplies its weighted density."),
    ("Generative classifiers can handle missing input features by marginalising over them.",
     "P(x<sub>obs</sub>|y) is obtained from the joint model."),
    ("When the misclassification costs are asymmetric, the Bayes-optimal rule need not pick the most probable class.",
     "A costly error type shifts the decision threshold."),
    ("For binary classification with 0-1 loss, the Bayes error at x equals min(P(y=0|x), P(y=1|x)).",
     "The Bayes rule errs with the probability of the less probable class."),
]
GD_FALSE = [
    ("Given enough training data, any classifier can reach zero test error for every distribution.",
     "Error cannot go below the Bayes error, which can be positive."),
    ("A sufficiently flexible classifier can achieve expected test error strictly below the Bayes error.",
     "The Bayes error is a lower bound."),
    ("Logistic regression is a generative classifier.", "It is discriminative."),
    ("Under asymmetric misclassification costs, the Bayes-optimal decision is still always arg max<sub>k</sub> P(k | x).",
     "The minimum-risk decision depends on the losses."),
    ("The MAP decision rule ignores the class priors.", "MAP uses the posterior ∝ likelihood × prior; ML ignores priors."),
    ("Discriminative classifiers model the class-conditional density P(x | y).", "That is what generative models do."),
    ("The Bayes classifier can be computed knowing only the class priors.", "It needs the class-conditional densities too."),
    ("Increasing the prior of class 1 shrinks the region assigned to class 1 by the Bayes rule.", "It enlarges it."),
    ("The Bayes error rate decreases as the training set grows.", "It depends only on the true distribution."),
    ("k-NN is a generative classifier because it uses the training data at prediction time.",
     "It does not model P(x|y); it is a non-parametric discriminative method."),
    ("A generative classifier always achieves lower test error than a discriminative classifier.",
     "Neither dominates; it depends on model correctness and sample size."),
    ("For binary classification under 0-1 loss, the Bayes error at x equals max(P(y=0|x), P(y=1|x)).",
     "It is the minimum of the two posteriors."),
]


@template(TOPIC, BAYES, marks=1, qtype="MSQ")
def bayes_generative_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, GD_TRUE, GD_FALSE)
    return Q(text="Which of the following statements about Bayes-optimal classification and generative vs. "
                  "discriminative models is/are CORRECT?", qtype="MSQ", marks=1, options=opts, answer=ans,
             solution=expl)


# =============================================================================
# METRICS
# =============================================================================
def _cm_counts(rng, lo=5, hi=60):
    while True:
        tp, fp, fn, tn = (int(v) for v in rng.integers(lo, hi, 4))
        if len({tp, fp, fn, tn}) == 4:
            return tp, fp, fn, tn


def _metrics(tp, fp, fn, tn):
    P = tp / (tp + fp)
    R = tp / (tp + fn)
    S = tn / (tn + fp)
    return dict(accuracy=(tp + tn) / (tp + fp + fn + tn), precision=P, recall=R, specificity=S,
                F1=2 * P * R / (P + R), balanced=(R + S) / 2, NPV=tn / (tn + fn), FPR=fp / (fp + tn))


MET_DESC = {
    "accuracy": ("accuracy", "(TP + TN)/N"), "precision": ("precision", "TP/(TP + FP)"),
    "recall": ("recall (sensitivity, TPR)", "TP/(TP + FN)"), "specificity": ("specificity (TNR)", "TN/(TN + FP)"),
    "F1": ("F1-score", "2PR/(P + R)"), "balanced": ("balanced accuracy", "(TPR + TNR)/2"),
    "NPV": ("negative predictive value", "TN/(TN + FN)"), "FPR": ("false positive rate", "FP/(FP + TN)"),
}


def _cm_table(tp, fp, fn, tn, rows_actual=True):
    if rows_actual:
        return Table([["", "Predicted +", "Predicted −"], ["Actual +", str(tp), str(fn)], ["Actual −", str(fp), str(tn)]])
    return Table([["", "Actual +", "Actual −"], ["Predicted +", str(tp), str(fp)], ["Predicted −", str(fn), str(tn)]])


@template(TOPIC, MET, marks=1, qtype="NAT")
def metric_from_cm(rng):
    tp, fp, fn, tn = _cm_counts(rng)
    m = _metrics(tp, fp, fn, tn)
    key = _pick(rng, list(MET_DESC))
    ra = bool(rng.integers(2))
    name, formula = MET_DESC[key]
    ans = m[key]
    text = (f"The confusion matrix of a binary classifier on a test set is shown below (note which of rows/columns are "
            f"actual and predicted). The {name} of the classifier is ______")
    sol = [f"TP = {tp}, FN = {fn}, FP = {fp}, TN = {tn} (N = {tp + fp + fn + tn}).",
           f"{name[0].upper() + name[1:]} = {formula}."]
    if key == "F1":
        sol.append(f"P = {tp}/{tp + fp} = {fmt(m['precision'], 4)}, R = {tp}/{tp + fn} = {fmt(m['recall'], 4)}; "
                   f"F1 = 2TP/(2TP + FP + FN) = {2 * tp}/{2 * tp + fp + fn} = <b>{fmt(ans, 2)}</b>.")
    elif key == "balanced":
        sol.append(f"TPR = {tp}/{tp + fn} = {fmt(m['recall'], 4)}, TNR = {tn}/{tn + fp} = {fmt(m['specificity'], 4)}; "
                   f"balanced accuracy = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"Value = <b>{fmt(ans, 2)}</b>.")
    sol.append("Watch the orientation: swapping FP and FN is the most common error (it swaps precision and recall).")
    return Q(text=text, qtype="NAT", marks=1, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[_cm_table(tp, fp, fn, tn, ra)], solution=sol)


@template(TOPIC, MET, marks=2, qtype="MSQ")
def metrics_cm_msq(rng):
    while True:
        tp, fp, fn, tn = _cm_counts(rng, 4, 80)
        m = _metrics(tp, fp, fn, tn)
        if abs(m["precision"] - m["recall"]) > 0.02:
            break
    wrong = {
        "accuracy": tp / (tp + fp + fn), "precision": m["recall"], "recall": m["precision"],
        "specificity": m["NPV"], "F1": (m["precision"] + m["recall"]) / 2, "balanced": m["accuracy"],
        "NPV": m["specificity"], "FPR": fp / (fp + tp),
    }
    keys = list(rng.choice(list(MET_DESC), 3, replace=False))
    items = []
    for k in keys:
        name, formula = MET_DESC[k]
        truth = bool(rng.random() < 0.5)
        if fmt(wrong[k], 2) == fmt(m[k], 2):
            truth = True
        val = m[k] if truth else wrong[k]
        ex = f"{name} = {formula} = {fmt(m[k], 4)}" + ("." if truth else f", not {fmt(val, 2)}.")
        items.append((f"The {name} is {fmt(val, 2)}.", truth, ex))
    cmp_true = m["precision"] > m["recall"]
    if rng.random() < 0.5:
        items.append(("Precision is greater than recall.", cmp_true,
                      f"P = {fmt(m['precision'], 4)}, R = {fmt(m['recall'], 4)}."))
    else:
        items.append(("The F1-score is less than the arithmetic mean of precision and recall.",
                      True, "The harmonic mean is ≤ the arithmetic mean, with equality only if P = R (not the case here)."))
    if not any(t for _, t, _ in items):
        s, _, e = items[0]
        k = keys[0]
        name, formula = MET_DESC[k]
        items[0] = (f"The {name} is {fmt(m[k], 2)}.", True, f"{name} = {formula} = {fmt(m[k], 4)}.")
    opts, ans, expl = _msq_build(rng, items)
    ra = bool(rng.integers(2))
    text = "For the confusion matrix below, which of the following statements is/are CORRECT? (values rounded to 2 decimals)"
    sol = [f"TP = {tp}, FN = {fn}, FP = {fp}, TN = {tn}."] + expl
    return Q(text=text, qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[_cm_table(tp, fp, fn, tn, ra)],
             solution=sol)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_fbeta(rng):
    n = int(rng.integers(12, 17))
    while True:
        y = rng.integers(0, 2, n)
        yh = np.where(rng.random(n) < 0.7, y, 1 - y)
        tp = int(((y == 1) & (yh == 1)).sum())
        fp = int(((y == 0) & (yh == 1)).sum())
        fn = int(((y == 1) & (yh == 0)).sum())
        if tp >= 2 and fp >= 1 and fn >= 1 and fp != fn:
            break
    beta = float(_pick(rng, [0.5, 2.0]))
    P, R = tp / (tp + fp), tp / (tp + fn)
    b2 = beta ** 2
    ans = (1 + b2) * P * R / (b2 * P + R)
    rows = [["#"] + [str(i + 1) for i in range(n)], ["actual y"] + [str(v) for v in y],
            ["predicted ŷ"] + [str(v) for v in yh]]
    text = (f"The actual and predicted labels of a binary classifier (1 = positive) on {n} test examples are given below. "
            f"The F<sub>β</sub>-score with β = {fmt(beta)}, F<sub>β</sub> = (1 + β²)PR/(β²P + R), is ______")
    sol = [f"Counting: TP = {tp}, FP = {fp}, FN = {fn}.",
           f"P = {tp}/{tp + fp} = {fmt(P, 4)}, R = {tp}/{tp + fn} = {fmt(R, 4)}.",
           f"F<sub>{fmt(beta)}</sub> = (1 + {fmt(b2)})×{fmt(P, 4)}×{fmt(R, 4)}/({fmt(b2)}×{fmt(P, 4)} + {fmt(R, 4)}) = "
           f"<b>{fmt(ans, 2)}</b>.",
           f"β {'&gt;' if beta > 1 else '&lt;'} 1 weights {'recall' if beta > 1 else 'precision'} more heavily "
           f"(F1 here would be {fmt(2 * P * R / (P + R), 3)})."]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False)], solution=sol)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_macro_micro(rng):
    while True:
        C = rng.integers(0, 7, (3, 3))
        C[np.diag_indices(3)] = rng.integers(5, 21, 3)
        prec = np.diag(C) / C.sum(0)
        rec = np.diag(C) / C.sum(1)
        f1 = 2 * prec * rec / (prec + rec)
        if len(set(np.round(prec, 3))) == 3:
            break
    var = int(rng.integers(5))
    acc = np.trace(C) / C.sum()
    names = ["macro-averaged precision", "macro-averaged recall", "macro-averaged F1-score",
             "micro-averaged F1-score", "weighted-average (by class support) recall"]
    vals = [prec.mean(), rec.mean(), f1.mean(), acc, (rec * C.sum(1)).sum() / C.sum()]
    ans = vals[var]
    rows = [["actual \\ predicted", "A", "B", "C"]] + [[cl] + [str(v) for v in C[i]] for i, cl in enumerate("ABC")]
    text = (f"The confusion matrix of a 3-class classifier is given below (rows = actual class, columns = predicted "
            f"class). The {names[var]} is ______")
    sol = [Table([["class", "TP", "predicted total", "actual total", "precision", "recall", "F1"]] +
                 [[cl, str(C[i, i]), str(C[:, i].sum()), str(C[i].sum()), fmt(prec[i], 4), fmt(rec[i], 4), fmt(f1[i], 4)]
                  for i, cl in enumerate("ABC")]),
           "Precision of class k = C<sub>kk</sub>/(column sum); recall = C<sub>kk</sub>/(row sum)."]
    if var == 0:
        sol.append(f"Macro precision = mean of per-class precisions = <b>{fmt(ans, 2)}</b>.")
    elif var == 1:
        sol.append(f"Macro recall = mean of per-class recalls = <b>{fmt(ans, 2)}</b> (= balanced accuracy).")
    elif var == 2:
        sol.append(f"Macro F1 = mean of per-class F1 = <b>{fmt(ans, 2)}</b>.")
    elif var == 3:
        sol.append(f"Micro-averaging pools TP/FP/FN over classes; for single-label multiclass, micro-P = micro-R = "
                   f"micro-F1 = accuracy = {np.trace(C)}/{C.sum()} = <b>{fmt(ans, 2)}</b>.")
    else:
        sol.append(f"Weighted recall = Σ(support<sub>k</sub> × recall<sub>k</sub>)/N = ΣC<sub>kk</sub>/N = accuracy = "
                   f"<b>{fmt(ans, 2)}</b>.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2), blocks=[Table(rows)],
             solution=sol)


def _score_data(rng, npos, nneg, sep=3.0):
    """Distinct scores (multiples of 0.05); higher scores are more likely to be positive."""
    n = npos + nneg
    sc = np.sort(rng.choice(np.round(np.arange(0.05, 0.96, 0.05), 2), n, replace=False))[::-1]
    w = np.exp(sep * sc)
    pos_idx = rng.choice(n, npos, replace=False, p=w / w.sum())
    y = np.zeros(n, int)
    y[pos_idx] = 1
    perm = rng.permutation(n)
    return sc[perm], y[perm]


def _auc(sc, y):
    pos, neg = sc[y == 1], sc[y == 0]
    c = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return c / (len(pos) * len(neg)), c


def _score_fig(sc, y, t=None):
    def draw(fig):
        ax = fig.add_subplot(111)
        m = y == 1
        ax.scatter(sc[m], np.ones(m.sum()), marker="o", s=40, color=DARK, zorder=3)
        ax.scatter(sc[~m], np.zeros((~m).sum()), marker="s", s=36, facecolor="white", edgecolor=DARK, zorder=3)
        for cls in (0, 1):
            vals = np.sort(sc[y == cls])
            for r, s_ in enumerate(vals):
                ax.annotate(fmt(s_), (s_, cls), xytext=(0, 6 if r % 2 == 0 else 15), textcoords="offset points",
                            ha="center", fontsize=6.5)
        if t is not None:
            ax.axvline(t, ls="--", color=MID, lw=1.2)
            ax.text(t, 1.55, f" t = {fmt(t)}", fontsize=7, color=MID)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["negatives", "positives"])
        ax.set_ylim(-0.5, 1.75)
        ax.set_xlim(0, 1)
        ax.set_xlabel("classifier score")
        ax.grid(alpha=.3, axis="x")
    return Figure(draw, 10, 4)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_auc_scores(rng):
    npos = int(rng.integers(4, 6))
    nneg = int(rng.integers(4, 7))
    while True:
        sc, y = _score_data(rng, npos, nneg)
        auc, c = _auc(sc, y)
        if 0.55 <= auc < 1:
            break
    rows = [["example"] + [str(i + 1) for i in range(len(sc))], ["score"] + [fmt(v) for v in sc],
            ["label"] + [str(v) for v in y]]
    text = (f"A classifier assigns the scores below to {len(sc)} test examples ({npos} positives, label 1; {nneg} "
            f"negatives, label 0). The area under the ROC curve (AUC) is ______")
    pos = sorted(sc[y == 1], reverse=True)
    neg = sc[y == 0]
    sol = ["AUC = fraction of (positive, negative) pairs in which the positive has the higher score "
           "(Mann–Whitney statistic).",
           "For each positive, count negatives with lower score: " +
           "; ".join(f"{fmt(p)} → {int((neg < p).sum())}" for p in pos) + ".",
           f"Concordant pairs = {fmt(c, 1)} out of {npos}×{nneg} = {npos * nneg}.",
           f"AUC = {fmt(c, 1)}/{npos * nneg} = <b>{fmt(auc, 2)}</b>.",
           "(Equivalently, trace the ROC staircase by lowering the threshold and add the rectangle areas.)"]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(auc, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False), _score_fig(sc, y)], solution=sol)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_roc_figure(rng):
    P = int(rng.integers(4, 6))
    N = int(rng.integers(4, 6))
    while True:
        seq = rng.permutation([1] * P + [0] * N)
        tp = np.concatenate([[0], np.cumsum(seq)])
        fp = np.concatenate([[0], np.cumsum(1 - seq)])
        tpr, fpr = tp / P, fp / N
        auc = sum(tpr[i] for i in range(1, len(seq) + 1) if seq[i - 1] == 0) / N
        if 0.55 < auc < 0.97:
            break
    var = int(rng.integers(3))
    cands = [jf for jf in range(1, N) if tpr[fpr <= jf / N + 1e-12].max() < 1]
    if var == 2 and not cands:
        var = 0
    if var == 0:
        ans, ask = auc, "the area under this ROC curve (AUC)"
        sol = ["The ROC curve is a staircase: each vertical step is a positive and each horizontal step a negative.",
               "Area = Σ over horizontal steps of (width 1/N) × (current TPR): " +
               " + ".join(f"{fmt(tpr[i], 2)}" for i in range(1, len(seq) + 1) if seq[i - 1] == 0) + f", times 1/{N}.",
               f"AUC = <b>{fmt(ans, 2)}</b>."]
    elif var == 1:
        J = tpr - fpr
        ans = J.max()
        ask = "the maximum value of Youden's index J = TPR − FPR over the operating points on the curve"
        i = int(np.argmax(J))
        sol = ["Compute TPR − FPR at each corner point of the staircase:",
               ", ".join(f"({fmt(fpr[k], 2)}, {fmt(tpr[k], 2)})→{fmt(J[k], 2)}" for k in range(len(J))) + ".",
               f"Maximum at FPR = {fmt(fpr[i], 2)}, TPR = {fmt(tpr[i], 2)}: J = <b>{fmt(ans, 2)}</b>."]
    else:
        jf = int(_pick(rng, cands))
        f = jf / N
        ans = tpr[fpr <= f + 1e-12].max()
        ask = f"the highest TPR attainable at FPR ≤ {fmt(f, 2)}"
        sol = [f"Among the operating points with FPR ≤ {fmt(f, 2)}, take the highest point of the curve (the top of "
               f"the vertical segment at FPR = {fmt(f, 2)}).", f"TPR = <b>{fmt(ans, 2)}</b>."]
    fp_, tp_ = fpr.copy(), tpr.copy()

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(fp_, tp_, color=DARK, lw=1.6, marker="o", ms=2.5)
        ax.plot([0, 1], [0, 1], ls=":", color=MID, lw=1)
        ax.set_xticks(np.linspace(0, 1, N + 1))
        ax.set_yticks(np.linspace(0, 1, P + 1))
        ax.set_xticklabels([fmt(v, 2) for v in np.linspace(0, 1, N + 1)])
        ax.set_yticklabels([fmt(v, 2) for v in np.linspace(0, 1, P + 1)])
        ax.grid(alpha=.45)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.02)
        ax.set_aspect("equal")
        ax.set_xlabel("False positive rate")
        ax.set_ylabel("True positive rate")
    text = (f"The ROC curve below was obtained from a test set with {P} positives and {N} negatives (all scores "
            f"distinct, so the curve moves in steps of 1/{P} vertically and 1/{N} horizontally). From the figure, "
            f"{ask} is ______")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Figure(draw, 7.5, 7)], solution=sol)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_at_threshold(rng):
    n = int(rng.integers(9, 12))
    npos = int(rng.integers(3, n - 3))
    while True:
        sc, y = _score_data(rng, npos, n - npos)
        t = float(_pick(rng, sorted(sc)[2:-2]))
        yh = (sc >= t).astype(int)
        tp = int(((yh == 1) & (y == 1)).sum())
        fp = int(((yh == 1) & (y == 0)).sum())
        fn = int(((yh == 0) & (y == 1)).sum())
        tn = int(((yh == 0) & (y == 0)).sum())
        if tp >= 1 and (fp + tn) >= 1 and fp + fn >= 1:
            break
    m = _metrics(tp, fp, fn, tn) if tp + fp > 0 else None
    key = _pick(rng, ["precision", "recall", "F1", "FPR", "accuracy"])
    ans = m[key]
    name, formula = MET_DESC[key]
    rows = [["example"] + [str(i + 1) for i in range(n)], ["score"] + [fmt(v) for v in sc],
            ["label"] + [str(v) for v in y]]
    text = (f"A probabilistic classifier produces the scores below on {n} labelled examples (1 = positive). An "
            f"example is predicted positive if its score is ≥ t, with t = {fmt(t)}. The {name} at this threshold is ______")
    sol = [f"Predicted positive (score ≥ {fmt(t)}): examples " +
           ", ".join(str(i + 1) for i in range(n) if yh[i] == 1) + ".",
           f"TP = {tp}, FP = {fp}, FN = {fn}, TN = {tn}.",
           f"{name[0].upper() + name[1:]} = {formula} = <b>{fmt(ans, 2)}</b>.",
           "Raising t typically raises precision and lowers recall/FPR; lowering t does the opposite (threshold moving)."]
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False), _score_fig(sc, y, t)], solution=sol)


@template(TOPIC, MET, marks=2, qtype="NAT")
def metric_prevalence(rng):
    se = float(_pick(rng, [0.8, 0.85, 0.9, 0.95, 0.99]))
    sp = float(_pick(rng, [0.9, 0.95, 0.97, 0.98, 0.99]))
    pi = float(_pick(rng, [0.01, 0.02, 0.05, 0.1, 0.2]))
    var = int(rng.integers(4))
    TP, FN, FP, TN = se * pi, (1 - se) * pi, (1 - sp) * (1 - pi), sp * (1 - pi)
    vals = [TP / (TP + FP), TN / (TN + FN), TP + TN, 2 * TP / (2 * TP + FP + FN)]
    names = ["precision (positive predictive value)", "negative predictive value", "accuracy", "F1-score"]
    ans = vals[var]
    text = (f"A classifier for a rare condition has sensitivity (recall) {fmt(se)} and specificity {fmt(sp)}. It is "
            f"deployed on a population where the prevalence of the positive class is {fmt(pi)}. The expected "
            f"{names[var]} in this population is ______")
    sol = ["Per unit population: TP = Se·π, FN = (1 − Se)·π, FP = (1 − Sp)(1 − π), TN = Sp(1 − π).",
           f"TP = {fmt(TP, 5)}, FN = {fmt(FN, 5)}, FP = {fmt(FP, 5)}, TN = {fmt(TN, 5)}."]
    form = ["TP/(TP + FP)", "TN/(TN + FN)", "TP + TN", "2TP/(2TP + FP + FN)"][var]
    sol.append(f"{names[var][0].upper() + names[var][1:]} = {form} = <b>{fmt(ans, 3)}</b>.")
    if var == 0:
        sol.append("Even a good test has low precision when the positive class is rare: most positives predicted are "
                   "false positives from the large negative class (class-imbalance effect; ROC is unaffected).")
    elif var == 2:
        sol.append(f"Note that the trivial 'always negative' classifier would have accuracy {fmt(1 - pi, 3)} — accuracy "
                   f"is misleading under imbalance.")
    return Q(text=text, qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.002), nat_hint=nat_hint(3), solution=sol)


MET_TRUE = [
    ("If 99% of test examples are negative, a classifier that always predicts negative has 99% accuracy but zero recall.",
     "TP = 0 ⇒ recall 0."),
    ("For fixed TPR and FPR, precision decreases as the positive class becomes rarer.",
     "Precision = TPR·π/(TPR·π + FPR(1 − π))."),
    ("The ROC AUC equals the probability that a randomly chosen positive is scored higher than a randomly chosen negative.",
     "Mann–Whitney interpretation (ties count ½)."),
    ("A classifier that assigns random scores has an expected ROC AUC of 0.5.", "Its ROC curve is the diagonal."),
    ("Lowering the decision threshold can never decrease recall.", "More examples are predicted positive; TP cannot fall."),
    ("The F1-score is the harmonic mean of precision and recall.", "F1 = 2PR/(P + R)."),
    ("For single-label multiclass classification, the micro-averaged F1-score equals accuracy.",
     "Pooled FP and FN both equal the number of errors."),
    ("Macro-averaging gives every class equal weight regardless of its number of examples.", "Simple mean over classes."),
    ("Balanced accuracy for binary classification is the mean of sensitivity and specificity.", "(TPR + TNR)/2."),
    ("Specificity equals TN/(TN + FP).", "True negative rate."),
    ("Under heavy class imbalance, precision-recall curves are usually more informative than ROC curves.",
     "FPR stays small when negatives are abundant, hiding many false positives."),
    ("The F<sub>β</sub>-score with β = 2 weights recall more heavily than precision.", "β &gt; 1 favours recall."),
    ("ROC AUC is unchanged by any strictly increasing transformation of the scores.", "Only the ranking matters."),
    ("For a classifier with random scores, the expected precision at any threshold equals the prevalence of the positive class.",
     "The PR-curve baseline is horizontal at π."),
    ("If a classifier has AUC 0.3, reversing its scores (s → −s) gives AUC 0.7.", "Every pair ordering flips."),
    ("Moving the decision threshold trades precision against recall without retraining the model.",
     "Threshold moving is a common remedy for class imbalance."),
    ("The point (FPR, TPR) = (0, 1) on the ROC plane corresponds to a perfect classifier.", "No FP and no FN."),
]
MET_FALSE = [
    ("Accuracy is a reliable performance measure under heavy class imbalance.", "The trivial majority classifier scores high."),
    ("ROC AUC depends on the particular decision threshold chosen.", "It summarises all thresholds."),
    ("Lowering the decision threshold always increases precision.", "It typically lowers precision."),
    ("The F1-score is the arithmetic mean of precision and recall.", "It is the harmonic mean."),
    ("Macro-averaging weights each class by its number of examples.", "That is weighted averaging."),
    ("The precision of a random classifier is 0.5 regardless of the class prevalence.", "It equals the prevalence."),
    ("The F<sub>β</sub>-score with β = 2 weights precision more heavily than recall.", "β &gt; 1 favours recall."),
    ("Specificity equals TP/(TP + FN).", "That is recall; specificity = TN/(TN + FP)."),
    ("The ROC curve plots precision against recall.", "It plots TPR against FPR."),
    ("An AUC of 0.5 indicates a perfect classifier.", "0.5 is chance level; 1 is perfect."),
    ("At fixed TPR and FPR, precision does not depend on the class prevalence.", "It does."),
    ("Recall equals TP/(TP + FP).", "That is precision."),
    ("Applying the transformation s → s³ to the scores changes the ROC AUC.", "Monotone transforms preserve the ranking."),
    ("Micro-averaged and macro-averaged F1 are always equal for multiclass problems.",
     "They differ when classes have different sizes/performance."),
    ("Raising the decision threshold can only increase the false positive rate.", "FPR can only stay the same or fall."),
]


@template(TOPIC, MET, marks=1, qtype="MSQ")
def metrics_concepts(rng):
    opts, ans, expl = msq_from_statements(rng, MET_TRUE, MET_FALSE)
    return Q(text="Which of the following statements about classifier evaluation is/are CORRECT?", qtype="MSQ",
             marks=1, options=opts, answer=ans, solution=expl)
