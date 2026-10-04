"""Reference examples showing the template API.  Not included in the mock sets
(``topics.example_template`` is skipped by build.py); copy the patterns."""
import numpy as np

from core import Q, Figure, Table, fmt, mcq, mcq_numeric, msq_from_statements, nat_hint, nat_range, template

TOPIC = "Example"


@template(TOPIC, "Simple linear regression", marks=2, qtype="NAT")
def slr_slope(rng):
    n = 5
    x = np.arange(1, n + 1, dtype=float)
    b1 = int(rng.integers(1, 4))
    b0 = int(rng.integers(-2, 3))
    y = b0 + b1 * x + rng.integers(-2, 3, size=n)
    xm, ym = x.mean(), y.mean()
    sxy = ((x - xm) * (y - ym)).sum()
    sxx = ((x - xm) ** 2).sum()
    slope = sxy / sxx

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(x, y, color="tab:blue", zorder=3)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(alpha=.3)

    return Q(
        text="Five observations (x<sub>i</sub>, y<sub>i</sub>) are shown in the table and plotted below. "
             "The least-squares estimate of the slope β<sub>1</sub> in y = β<sub>0</sub> + β<sub>1</sub>x is ______ "
             + nat_hint(2),
        qtype="NAT", marks=2, answer=nat_range(slope, 2),
        blocks=[Table([["x"] + [fmt(v) for v in x], ["y"] + [fmt(v) for v in y]], header=False),
                Figure(draw, 7, 4.5)],
        solution=[f"x̄ = {fmt(xm)}, ȳ = {fmt(ym)}.",
                  f"S<sub>xy</sub> = Σ(x<sub>i</sub>−x̄)(y<sub>i</sub>−ȳ) = {fmt(sxy)},  "
                  f"S<sub>xx</sub> = Σ(x<sub>i</sub>−x̄)² = {fmt(sxx)}.",
                  f"β̂<sub>1</sub> = S<sub>xy</sub>/S<sub>xx</sub> = <b>{fmt(slope, 2)}</b>."],
    )


@template(TOPIC, "Bias-variance", marks=1, qtype="MSQ")
def bv_statements(rng):
    T = [("Increasing model complexity typically decreases bias.", "More flexible models fit the true function better."),
         ("Bagging mainly reduces variance.", "Averaging de-correlated models reduces variance.")]
    F = [("Adding more training data increases variance.", "More data typically reduces variance."),
         ("Ridge regularisation decreases bias.", "Shrinkage introduces bias in exchange for lower variance."),
         ("Irreducible error can be reduced by a better model.", "It is noise variance σ², independent of the model.")]
    opts, ans, expl = msq_from_statements(rng, T, F)
    return Q(text="Which of the following statements is/are CORRECT?", qtype="MSQ", marks=1,
             options=opts, answer=ans, solution=expl)


@template(TOPIC, "kNN", marks=1, qtype="MCQ")
def knn_k(rng):
    opts, a = mcq(rng, "decreases", ["increases", "remains unchanged", "first increases then decreases"])
    return Q(text="As k in k-NN increases (for fixed training data), the variance of the classifier generally",
             qtype="MCQ", marks=1, options=opts, answer=a,
             solution="Larger k averages over more neighbours → smoother decision boundary → lower variance (higher bias).")
