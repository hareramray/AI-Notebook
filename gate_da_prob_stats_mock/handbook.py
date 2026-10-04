"""Quick-revision formula handbook for GATE DA Probability & Statistics."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from reportlab.platypus import CondPageBreak, PageBreak, Spacer
from scipy import stats

from render import FRAME_W, P, content

BLUE, MAROON, GOLD, GREY = "#1f5f8b", "#6b1d1d", "#f2c14e", "#888888"


# ------------------------------------------------------------------ figures
def fig_venn():
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.5))
    titles = ["Overlapping: P(A∪B)=P(A)+P(B)−P(A∩B)",
              "Mutually exclusive: A∩B = Ø",
              "Complement: P(Aᶜ) = 1 − P(A)"]
    for ax, t in zip(axes, titles):
        ax.add_patch(Rectangle((0, 0), 4, 3, fill=False, lw=1.2))
        ax.set_xlim(-0.2, 4.2); ax.set_ylim(-0.2, 3.4); ax.axis("off")
        ax.set_title(t, fontsize=7.6)
        ax.text(0.15, 2.7, "S", fontsize=9)
    a = axes[0]
    a.add_patch(Circle((1.6, 1.5), 1.0, color=BLUE, alpha=0.35))
    a.add_patch(Circle((2.5, 1.5), 1.0, color=MAROON, alpha=0.35))
    a.text(1.1, 1.45, "A"); a.text(2.8, 1.45, "B"); a.text(1.85, 1.45, "A∩B", fontsize=7)
    b = axes[1]
    b.add_patch(Circle((1.1, 1.5), 0.8, color=BLUE, alpha=0.35))
    b.add_patch(Circle((2.9, 1.5), 0.8, color=MAROON, alpha=0.35))
    b.text(1.0, 1.45, "A"); b.text(2.8, 1.45, "B")
    c = axes[2]
    c.add_patch(Rectangle((0, 0), 4, 3, color=GOLD, alpha=0.35))
    c.add_patch(Circle((2, 1.5), 0.9, color="white"))
    c.add_patch(Circle((2, 1.5), 0.9, color=BLUE, alpha=0.4))
    c.text(1.9, 1.45, "A"); c.text(3.2, 0.3, "Aᶜ")
    fig.tight_layout()
    return fig


def fig_tree():
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.axis("off")
    root = (0.05, 0.5)
    bs = [(0.42, 0.82, "B₁", "P(B₁)"), (0.42, 0.5, "B₂", "P(B₂)"), (0.42, 0.18, "B₃", "P(B₃)")]
    for x, y, lab, pl in bs:
        ax.plot([root[0], x], [root[1], y], color=BLUE)
        ax.text(x + 0.01, y, lab, va="center", fontsize=10, fontweight="bold")
        ax.text((root[0] + x) / 2 - 0.04, (root[1] + y) / 2 + 0.03, pl, fontsize=8, color=BLUE)
        for dy, lab2 in [(0.09, "A"), (-0.09, "Aᶜ")]:
            ax.plot([x + 0.06, 0.78], [y, y + dy], color=MAROON, lw=0.9)
            ax.text(0.79, y + dy, lab2, va="center", fontsize=8.5)
        ax.text(0.58, y + 0.075, f"P(A|{lab})", fontsize=7.5, color=MAROON)
        ax.text(0.87, y + 0.09, f"P({lab})P(A|{lab})", fontsize=7, va="center")
    ax.plot(*root, "o", color="black")
    ax.set_xlim(0, 1.12); ax.set_ylim(0.0, 1.0)
    ax.set_title("Tree diagram: P(A) = Σ P(Bᵢ)P(A|Bᵢ);  P(Bⱼ|A) = branch product / P(A)", fontsize=8.5)
    return fig


def fig_cdf():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    xs = [0, 1, 2, 3]; ps = [0.1, 0.3, 0.4, 0.2]
    ax = axes[0]
    F = np.cumsum(ps)
    edges = [-1] + xs + [4]
    vals = [0] + list(F)
    for i in range(len(vals)):
        ax.hlines(vals[i], edges[i], edges[i + 1], color=BLUE, lw=2)
    for x, f, f0 in zip(xs, F, [0] + list(F[:-1])):
        ax.plot(x, f, "o", color=BLUE)
        ax.plot(x, f0, "o", mfc="white", color=BLUE)
    ax.set_title("Discrete CDF: right-continuous step function", fontsize=8.5)
    ax.set_xlabel("x"); ax.set_ylabel("F(x)")
    ax = axes[1]
    x = np.linspace(-0.5, 4, 300)
    ax.plot(x, stats.expon.cdf(x), color=MAROON, lw=2, label="F(x)=1−e^{−x}")
    ax.plot(x, stats.expon.pdf(x), color=GOLD, lw=2, ls="--", label="f(x)=F′(x)")
    ax.legend(fontsize=7.5, frameon=False)
    ax.set_title("Continuous CDF and its density", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_skew():
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.2))
    x = np.linspace(0, 1, 300)
    for ax, (a, b, t) in zip(axes, [(2, 5, "Right (positive) skew\nmode < median < mean"),
                                    (4, 4, "Symmetric\nmean = median = mode"),
                                    (5, 2, "Left (negative) skew\nmean < median < mode")]):
        d = stats.beta(a, b)
        ax.plot(x, d.pdf(x), color=BLUE)
        ax.fill_between(x, d.pdf(x), alpha=0.15, color=BLUE)
        mode = (a - 1) / (a + b - 2)
        for v, c, l in [(d.mean(), MAROON, "mean"), (d.median(), GOLD, "median"), (mode, "k", "mode")]:
            ax.axvline(v, color=c, lw=1.2, ls="--", label=l)
        ax.set_title(t, fontsize=8)
        ax.set_yticks([])
    axes[0].legend(fontsize=6.5, frameon=False)
    fig.tight_layout()
    return fig


def fig_box():
    rng = np.random.default_rng(4)
    data = np.concatenate([rng.normal(50, 10, 120), [95, 102]])
    fig, ax = plt.subplots(figsize=(6.2, 1.9))
    ax.boxplot(data, vert=False, widths=0.5, patch_artist=True,
               boxprops=dict(facecolor="#eaf2f8", color=BLUE), medianprops=dict(color=MAROON, lw=2),
               flierprops=dict(marker="o", mfc=MAROON))
    q1, q2, q3 = np.percentile(data, [25, 50, 75])
    for v, l in [(q1, "Q₁"), (q2, "Q₂ (median)"), (q3, "Q₃")]:
        ax.text(v, 1.35, l, ha="center", fontsize=8)
    ax.text(q3 + 1.5 * (q3 - q1), 0.7, "upper fence = Q₃ + 1.5·IQR", fontsize=7.5, ha="center")
    ax.set_yticks([]); ax.set_ylim(0.5, 1.55)
    ax.set_title("Box plot: IQR = Q₃ − Q₁; points beyond 1.5·IQR fences are outliers", fontsize=8.5)
    return fig


def fig_corr():
    rng = np.random.default_rng(1)
    fig, axes = plt.subplots(1, 5, figsize=(7.6, 1.8))
    for ax, r in zip(axes, [-0.9, -0.4, 0, 0.5, 0.95]):
        cov = [[1, r], [r, 1]]
        d = rng.multivariate_normal([0, 0], cov, 150)
        ax.scatter(d[:, 0], d[:, 1], s=4, color=BLUE)
        ax.set_title(f"ρ = {r}", fontsize=8.5)
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout()
    return fig


def fig_zero_corr():
    x = np.linspace(-2, 2, 41)
    fig, ax = plt.subplots(figsize=(4.4, 2.1))
    ax.scatter(x, x ** 2, s=10, color=MAROON)
    ax.set_title("Y = X², X symmetric about 0: ρ = 0, yet Y is a function of X", fontsize=8.5)
    ax.set_xlabel("X"); ax.set_ylabel("Y")
    return fig


def fig_discrete():
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.3))
    k = np.arange(0, 11)
    axes[0].bar(np.arange(1, 7), [1 / 6] * 6, color=BLUE)
    axes[0].set_title("Discrete uniform{1..6}", fontsize=8.5)
    axes[1].bar(k, stats.binom.pmf(k, 10, 0.3), color=MAROON)
    axes[1].set_title("Binomial(n=10, p=0.3)", fontsize=8.5)
    axes[2].bar(k, stats.poisson.pmf(k, 3), color=GOLD, edgecolor="k", lw=0.4)
    axes[2].set_title("Poisson(λ=3)", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_continuous():
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.3))
    x = np.linspace(-0.5, 3.5, 400)
    axes[0].plot(x, stats.uniform(0, 2).pdf(x), color=BLUE)
    axes[0].set_title("Uniform(0, 2)", fontsize=8.5)
    x = np.linspace(0, 4, 300)
    for lam, c in [(0.5, BLUE), (1, MAROON), (2, GOLD)]:
        axes[1].plot(x, stats.expon(scale=1 / lam).pdf(x), color=c, label=f"λ={lam}")
    axes[1].legend(fontsize=7, frameon=False)
    axes[1].set_title("Exponential(λ)", fontsize=8.5)
    x = np.linspace(-5, 7, 300)
    for (m, s), c in [((0, 1), BLUE), ((0, 2), MAROON), ((2, 1), GOLD)]:
        axes[2].plot(x, stats.norm(m, s).pdf(x), color=c, label=f"N({m},{s}²)")
    axes[2].legend(fontsize=7, frameon=False)
    axes[2].set_title("Normal(μ, σ²)", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_t_chi():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.5))
    x = np.linspace(-4, 4, 400)
    axes[0].plot(x, stats.norm.pdf(x), color="k", lw=2, label="N(0,1)")
    for df, c in [(1, MAROON), (3, GOLD), (10, BLUE)]:
        axes[0].plot(x, stats.t(df).pdf(x), color=c, ls="--", label=f"t, ν={df}")
    axes[0].legend(fontsize=7, frameon=False)
    axes[0].set_title("t: heavier tails, → N(0,1) as ν → ∞", fontsize=8.5)
    x = np.linspace(0.01, 20, 400)
    for df, c in [(1, MAROON), (3, GOLD), (5, BLUE), (10, "k")]:
        axes[1].plot(x, stats.chi2(df).pdf(x), color=c, label=f"χ², k={df}")
    axes[1].set_ylim(0, 0.5)
    axes[1].legend(fontsize=7, frameon=False)
    axes[1].set_title("χ²ₖ: right-skewed, mean k, variance 2k", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_empirical():
    x = np.linspace(-4, 4, 500)
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    ax.plot(x, stats.norm.pdf(x), color="k")
    for k, c, a in [(3, GOLD, 0.25), (2, MAROON, 0.25), (1, BLUE, 0.35)]:
        m = np.abs(x) <= k
        ax.fill_between(x[m], stats.norm.pdf(x[m]), color=c, alpha=a)
    ax.annotate("68.27%", (0, 0.17), ha="center", fontsize=9)
    ax.annotate("95.45% within ±2σ", (0, 0.03), ha="center", fontsize=8)
    ax.annotate("99.73% within ±3σ", (2.9, 0.08), ha="center", fontsize=8)
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels(["μ−3σ", "μ−2σ", "μ−σ", "μ", "μ+σ", "μ+2σ", "μ+3σ"], fontsize=8)
    ax.set_yticks([])
    ax.set_title("Empirical (68–95–99.7) rule for the normal distribution", fontsize=9)
    return fig


def fig_joint_region():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8))
    ax = axes[0]
    ax.fill([0, 1, 0], [0, 1, 1], color=BLUE, alpha=0.3)
    ax.plot([0, 1], [0, 1], color=MAROON)
    ax.set_title("Support 0 < x < y < 1 (f = 2)", fontsize=8.5)
    ax.annotate("x from 0 to y", (0.1, 0.62), fontsize=8)
    ax.hlines(0.55, 0, 0.55, color="k", lw=1)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05)
    ax = axes[1]
    xx, yy = np.meshgrid(np.linspace(-3, 3, 120), np.linspace(-3, 3, 120))
    rho = 0.6
    z = np.exp(-(xx ** 2 - 2 * rho * xx * yy + yy ** 2) / (2 * (1 - rho ** 2)))
    ax.contour(xx, yy, z, levels=6, colors=BLUE, linewidths=0.8)
    ax.plot([-3, 3], [-3 * rho, 3 * rho], color=MAROON, label="E[Y|X=x] = ρx")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    ax.set_title("Bivariate normal (ρ=0.6) contours", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_clt():
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 4, figsize=(7.6, 2.0))
    for ax, n in zip(axes, [1, 2, 5, 30]):
        m = rng.exponential(1, (20000, n)).mean(axis=1)
        ax.hist(m, bins=50, density=True, color=BLUE, alpha=0.7)
        x = np.linspace(m.min(), m.max(), 200)
        if n > 1:
            ax.plot(x, stats.norm(1, 1 / np.sqrt(n)).pdf(x), color=MAROON, lw=1.4)
        ax.set_title(f"n = {n}", fontsize=8.5)
        ax.set_yticks([])
    fig.suptitle("CLT: sample means of Exponential(1) data → N(1, 1/n)", fontsize=8.5, y=1.02)
    fig.tight_layout()
    return fig


def fig_ci():
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    mu, s, n = 50, 10, 25
    miss = 0
    for i in range(40):
        x = rng.normal(mu, s, n).mean()
        h = 1.96 * s / np.sqrt(n)
        hit = x - h <= mu <= x + h
        miss += not hit
        ax.plot([i, i], [x - h, x + h], color=BLUE if hit else MAROON, lw=1.6)
        ax.plot(i, x, "o", ms=2.5, color="k")
    ax.axhline(mu, color=GOLD, lw=1.6)
    ax.set_title(f"40 independent 95% CIs for μ = 50: {miss} miss (red). μ is fixed; intervals are random.",
                 fontsize=8.2)
    ax.set_xticks([])
    return fig


def fig_rejection():
    x = np.linspace(-4, 4, 400)
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.2))
    for ax, kind in zip(axes, ["two", "right", "left"]):
        ax.plot(x, stats.norm.pdf(x), color="k")
        if kind == "two":
            regs, t = [(x <= -1.96), (x >= 1.96)], "H₁: μ ≠ μ₀  (|z| > 1.96)"
        elif kind == "right":
            regs, t = [(x >= 1.645)], "H₁: μ > μ₀  (z > 1.645)"
        else:
            regs, t = [(x <= -1.645)], "H₁: μ < μ₀  (z < −1.645)"
        for m in regs:
            ax.fill_between(x[m], stats.norm.pdf(x[m]), color=MAROON, alpha=0.45)
        ax.set_title(t, fontsize=8)
        ax.set_yticks([])
    fig.suptitle("Rejection regions at α = 0.05 (shaded)", fontsize=8.5, y=1.03)
    fig.tight_layout()
    return fig


def fig_errors():
    x = np.linspace(-4, 7, 500)
    fig, ax = plt.subplots(figsize=(6.4, 2.5))
    h0, h1 = stats.norm(0, 1), stats.norm(2.5, 1)
    c = 1.645
    ax.plot(x, h0.pdf(x), color=BLUE, label="sampling dist. under H₀")
    ax.plot(x, h1.pdf(x), color=MAROON, label="under H₁")
    ax.fill_between(x[x >= c], h0.pdf(x[x >= c]), color=BLUE, alpha=0.4, label="α (Type I)")
    ax.fill_between(x[x < c], h1.pdf(x[x < c]), color=MAROON, alpha=0.3, label="β (Type II)")
    ax.axvline(c, color="k", ls="--", lw=1)
    ax.text(c + 0.05, 0.37, "critical value", fontsize=8)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_yticks([])
    ax.set_title("Type I / Type II errors; power = 1 − β", fontsize=9)
    return fig


# ------------------------------------------------------------------ text
def section(title, items):
    return [CondPageBreak(60), P(title, "h2")] + content(items)


def handbook_story(register):
    st = []
    h = P("<a name='handbook'/>Part A · Formula Handbook & Concept Review", "h1")
    register(h, "Part A · Formula Handbook & Concept Review", 0, "handbook")
    st.append(h)
    st += content([
        "This handbook condenses every syllabus item of GATE DA Section 1 into formulas, diagrams and the "
        "traps that examiners exploit. Revise it before each mock and return to it whenever a solution "
        "refers to a result you do not remember.",
    ])

    st += section("A1. Counting: permutations and combinations", [
        ("table", [["Situation", "Count", "Example"],
                   ["Ordered, no repetition (arrange r of n)", "ⁿPᵣ = n!/(n−r)!", "Podium of 3 from 8: 336"],
                   ["Unordered, no repetition (choose r of n)", "ⁿCᵣ = n!/(r!(n−r)!)", "Committee of 3 from 8: 56"],
                   ["Ordered, with repetition", "nʳ", "4-digit PINs: 10⁴"],
                   ["Unordered, with repetition (multisets)", "ⁿ⁺ʳ⁻¹Cᵣ", "3 scoops from 5 flavours: 35"],
                   ["Arrangements with identical items", "n!/(n₁! n₂! ⋯ nₖ!)", "MISSISSIPPI: 34650"],
                   ["Circular arrangements of n distinct", "(n−1)!", "6 people at round table: 120"],
                   ["Integer solutions x₁+⋯+xₖ = n, xᵢ ≥ 0", "ⁿ⁺ᵏ⁻¹Cₖ₋₁", "x+y+z=5: 21"],
                   ["Derangements of n", "Dₙ = n! Σ (−1)ᵏ/k!", "D₄ = 9,  Dₙ/n! → 1/e"]],
         dict(col_widths=[FRAME_W * 0.42, FRAME_W * 0.24, FRAME_W * 0.34], align_left_first=True)),
        "<b>Multiplication principle:</b> a task in k stages with n₁, …, nₖ choices gives n₁n₂⋯nₖ outcomes. "
        "<b>Addition principle:</b> disjoint alternatives add.",
        "$$\\binom{n}{r}=\\binom{n}{n-r},\\qquad \\binom{n}{r}=\\binom{n-1}{r-1}+\\binom{n-1}{r},\\qquad "
        "\\sum_{r=0}^{n}\\binom{n}{r}=2^n",
        "<b>Inclusion–exclusion:</b>",
        "$$|A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|A\\cap C|-|B\\cap C|+|A\\cap B\\cap C|",
        "<b>Hypergeometric probability</b> (drawing without replacement): choosing n from N items of which "
        "K are 'successes',",
        "$$P(X=k)=\\dfrac{\\binom{K}{k}\\binom{N-K}{n-k}}{\\binom{N}{n}}",
        ("note", "Decide first whether ORDER matters and whether REPETITION is allowed. Most counting "
                 "errors come from double-counting ordered selections when the question asks for "
                 "unordered groups (divide by r!) or from forgetting identical objects.", "Trap"),
    ])

    st += section("A2. Sample space, events and the axioms of probability", [
        "A <b>sample space</b> S is the set of all outcomes; an <b>event</b> is a subset of S. Kolmogorov's axioms: "
        "(i) P(A) ≥ 0, (ii) P(S) = 1, (iii) for pairwise disjoint A₁, A₂, …, P(∪Aᵢ) = Σ P(Aᵢ).",
        ("bullets", [
            "P(Ø) = 0,  P(Aᶜ) = 1 − P(A),  A ⊂ B ⇒ P(A) ≤ P(B).",
            "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)  (addition rule).",
            "Boole: P(A ∪ B) ≤ P(A) + P(B);  Bonferroni: P(A ∩ B) ≥ P(A) + P(B) − 1.",
            "De Morgan: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ,  (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ.",
            "Equally likely outcomes: P(A) = |A| / |S|.",
        ]),
        ("fig", fig_venn),
        P("Independent vs mutually exclusive", "h3"),
        ("table", [["Property", "Independent", "Mutually exclusive"],
                   ["Definition", "P(A ∩ B) = P(A)P(B)", "A ∩ B = Ø, so P(A ∩ B) = 0"],
                   ["P(A ∪ B)", "P(A) + P(B) − P(A)P(B)", "P(A) + P(B)"],
                   ["P(A | B)", "P(A)", "0"],
                   ["Both at once?", "Only if P(A) = 0 or P(B) = 0", "—"],
                   ["Complements", "Aᶜ, B and Aᶜ, Bᶜ also independent", "Not preserved"]],
         dict(col_widths=[FRAME_W * 0.22, FRAME_W * 0.39, FRAME_W * 0.39], align_left_first=True)),
        "<b>Mutual independence</b> of A, B, C requires all pairwise product rules AND "
        "P(A ∩ B ∩ C) = P(A)P(B)P(C). Pairwise independence does not imply mutual independence "
        "(classic example: two fair coins, A = first head, B = second head, C = exactly one head).",
        ("note", "Disjoint events with positive probability are always DEPENDENT: knowing A occurred tells "
                 "you B did not.", "Trap"),
    ])

    st += section("A3. Joint, marginal and conditional probability; Bayes' theorem", [
        "$$P(A\\mid B)=\\dfrac{P(A\\cap B)}{P(B)},\\quad P(B)>0 \\qquad P(A\\cap B)=P(B)P(A\\mid B)",
        "<b>Chain rule:</b>",
        "$$P(A_1\\cap A_2\\cap\\cdots\\cap A_n)=P(A_1)P(A_2\\mid A_1)P(A_3\\mid A_1\\cap A_2)\\cdots",
        "<b>Total probability</b> (B₁, …, Bₖ partition S):",
        "$$P(A)=\\sum_{i=1}^{k}P(B_i)P(A\\mid B_i)",
        "<b>Bayes' theorem:</b>",
        "$$P(B_j\\mid A)=\\dfrac{P(B_j)P(A\\mid B_j)}{\\sum_{i}P(B_i)P(A\\mid B_i)}",
        ("fig", fig_tree),
        "<b>Joint probability table.</b> For two categorical variables, cell entries are joint probabilities; "
        "row/column totals are marginals; dividing a row by its total gives a conditional distribution.",
        ("table", [["", "B", "Bᶜ", "Total"],
                   ["A", "P(A∩B)", "P(A∩Bᶜ)", "P(A)"],
                   ["Aᶜ", "P(Aᶜ∩B)", "P(Aᶜ∩Bᶜ)", "P(Aᶜ)"],
                   ["Total", "P(B)", "P(Bᶜ)", "1"]]),
        "<b>Odds form of Bayes:</b> posterior odds = prior odds × likelihood ratio,",
        "$$\\dfrac{P(H\\mid E)}{P(H^c\\mid E)}=\\dfrac{P(H)}{P(H^c)}\\times\\dfrac{P(E\\mid H)}{P(E\\mid H^c)}",
        ("note", "Base-rate fallacy: with a rare condition, even an accurate test gives a modest P(condition | "
                 "positive). Always weigh the likelihood by the prior.", "Trap"),
    ])

    st += section("A4. Random variables, PMF, PDF and CDF", [
        "A random variable X maps outcomes to real numbers. Its <b>CDF</b> F(x) = P(X ≤ x) is "
        "non-decreasing, right-continuous, with F(−∞) = 0 and F(∞) = 1.",
        ("table", [["", "Discrete", "Continuous"],
                   ["Description", "PMF p(x) = P(X = x), Σ p(x) = 1", "PDF f(x) ≥ 0, ∫ f(x) dx = 1"],
                   ["CDF", "F(x) = Σ<sub>t≤x</sub> p(t)", "F(x) = ∫<sub>−∞</sub><super>x</super> f(t) dt"],
                   ["P(a &lt; X ≤ b)", "F(b) − F(a)", "F(b) − F(a) = ∫<sub>a</sub><super>b</super> f"],
                   ["P(X = a)", "jump of F at a", "0 for every a"],
                   ["From CDF to pmf/pdf", "p(a) = F(a) − F(a⁻)", "f(x) = F′(x)"]],
         dict(col_widths=[FRAME_W * 0.22, FRAME_W * 0.39, FRAME_W * 0.39], align_left_first=True)),
        ("fig", fig_cdf),
        "<b>Mixed distributions</b> have a CDF with both jumps and continuous increases; probabilities at jump "
        "points equal jump sizes.",
        "<b>Quantiles:</b> the p-th quantile is the smallest x with F(x) ≥ p; the median solves F(m) = 1/2. "
        "The <b>mode</b> maximises the pmf/pdf.",
        "<b>Transformations.</b> If Y = g(X) with g monotone and differentiable,",
        "$$f_Y(y)=f_X\\left(g^{-1}(y)\\right)\\left|\\dfrac{d}{dy}g^{-1}(y)\\right|",
        "In general use the CDF method: F<sub>Y</sub>(y) = P(g(X) ≤ y), then differentiate.",
        ("note", "A valid pdf may exceed 1 (e.g. Uniform(0, 0.5) has f = 2); only its integral must be 1. "
                 "A pmf can never exceed 1.", "Trap"),
    ])

    st += section("A5. Expectation, variance and their rules", [
        "$$E[X]=\\sum_x x\\,p(x)\\quad\\mathrm{or}\\quad E[X]=\\int x f(x)\\,dx,\\qquad E[g(X)]=\\sum_x g(x)p(x)",
        "$$\\mathrm{Var}(X)=E[(X-\\mu)^2]=E[X^2]-(E[X])^2,\\qquad \\sigma=\\sqrt{\\mathrm{Var}(X)}",
        ("table", [["Rule", "Statement"],
                   ["Linearity", "E[aX + bY + c] = aE[X] + bE[Y] + c (always, even if dependent)"],
                   ["Scaling", "Var(aX + b) = a² Var(X); SD(aX + b) = |a| SD(X)"],
                   ["Sum", "Var(X ± Y) = Var(X) + Var(Y) ± 2 Cov(X, Y)"],
                   ["Independent", "E[XY] = E[X]E[Y]; Var(X + Y) = Var(X) + Var(Y)"],
                   ["n i.i.d. copies", "Var(X₁+⋯+Xₙ) = nσ²;  Var(X̄) = σ²/n"],
                   ["Tail formula", "X ≥ 0 integer: E[X] = Σ<sub>k≥1</sub> P(X ≥ k); continuous: ∫₀^∞ P(X > x)dx"],
                   ["Indicators", "E[1<sub>A</sub>] = P(A); count = Σ indicators ⇒ E[count] = Σ P(Aᵢ)"]],
         dict(col_widths=[FRAME_W * 0.22, FRAME_W * 0.78], align_left_first=True)),
        P("Conditional expectation and variance", "h3"),
        "$$E[X\\mid Y=y]=\\sum_x x\\,p_{X\\mid Y}(x\\mid y)\\quad\\mathrm{or}\\quad \\int x\\,f_{X\\mid Y}(x\\mid y)\\,dx",
        "<b>Law of total expectation (tower rule):</b>",
        "$$E[X]=E\\left[E[X\\mid Y]\\right]=\\sum_y E[X\\mid Y=y]\\,P(Y=y)",
        "<b>Law of total variance (Eve's law):</b>",
        "$$\\mathrm{Var}(X)=E\\left[\\mathrm{Var}(X\\mid Y)\\right]+\\mathrm{Var}\\left(E[X\\mid Y]\\right)",
        "<b>Random sums:</b> if S = X₁ + ⋯ + X<sub>N</sub> with N independent of i.i.d. Xᵢ,",
        "$$E[S]=E[N]\\mu,\\qquad \\mathrm{Var}(S)=E[N]\\sigma^2+\\mu^2\\mathrm{Var}(N)",
        ("note", "E[X | Y] is a random variable (a function of Y); E[X | Y = y] is a number. The 'within-group' "
                 "variance E[Var(X|Y)] plus the 'between-group' variance Var(E[X|Y]) gives the total.",
         "Key idea"),
    ])

    st += section("A6. Descriptive statistics: mean, median, mode, standard deviation", [
        ("table", [["Measure", "Ungrouped data", "Notes"],
                   ["Mean", "x̄ = Σxᵢ / n", "Sensitive to outliers; Σ(xᵢ − x̄) = 0"],
                   ["Median", "middle value of sorted data", "Robust; minimises Σ|xᵢ − c|"],
                   ["Mode", "most frequent value", "May be non-unique"],
                   ["Population variance", "σ² = Σ(xᵢ − μ)² / N", "divide by N"],
                   ["Sample variance", "s² = Σ(xᵢ − x̄)² / (n − 1)", "unbiased for σ² (Bessel)"],
                   ["Shortcut", "Σ(xᵢ − x̄)² = Σxᵢ² − n x̄²", "use for hand computation"],
                   ["Range, IQR", "max − min,  Q₃ − Q₁", "IQR is robust"],
                   ["Coefficient of variation", "CV = σ / μ", "unit-free spread"]],
         dict(col_widths=[FRAME_W * 0.26, FRAME_W * 0.36, FRAME_W * 0.38], align_left_first=True)),
        "<b>Grouped data</b> with class marks mᵢ and frequencies fᵢ: x̄ = Σfᵢmᵢ / Σfᵢ. "
        "Median = L + ((N/2 − C)/f)·h and Mode = L + (f₁ − f₀)/(2f₁ − f₀ − f₂)·h, where L is the lower limit "
        "of the median/modal class, C the cumulative frequency before it and h the class width.",
        "<b>Linear transformation</b> y = ax + b: mean, median, mode transform as ax + b; SD and IQR scale by |a|; "
        "variance by a²; adding a constant does not change spread.",
        "<b>Combining two groups</b> (sizes n₁, n₂, means x̄₁, x̄₂, population-style variances σ₁², σ₂²):",
        "$$\\bar{x}=\\dfrac{n_1\\bar{x}_1+n_2\\bar{x}_2}{n_1+n_2},\\qquad "
        "\\sigma^2=\\dfrac{n_1(\\sigma_1^2+d_1^2)+n_2(\\sigma_2^2+d_2^2)}{n_1+n_2},\\ d_i=\\bar{x}_i-\\bar{x}",
        ("fig", fig_skew),
        "Empirical relation for moderately skewed data: Mode ≈ 3·Median − 2·Mean.",
        ("fig", fig_box),
    ])

    st += section("A7. Covariance and correlation", [
        "$$\\mathrm{Cov}(X,Y)=E[(X-\\mu_X)(Y-\\mu_Y)]=E[XY]-E[X]E[Y]",
        "$$\\rho_{XY}=\\dfrac{\\mathrm{Cov}(X,Y)}{\\sigma_X\\sigma_Y},\\qquad -1\\le\\rho\\le 1",
        ("bullets", [
            "Cov(X, X) = Var(X); Cov(aX + b, cY + d) = ac Cov(X, Y); covariance is bilinear.",
            "ρ(aX + b, cY + d) = sign(ac) ρ(X, Y): correlation is unit-free and shift/scale invariant.",
            "|ρ| = 1 iff Y = aX + b exactly (a ≠ 0).",
            "Independent ⇒ Cov = 0, but Cov = 0 does NOT imply independence (except for jointly normal variables).",
            "Sample: r = Sxy / √(Sxx Syy), with Sxy = Σ(xᵢ − x̄)(yᵢ − ȳ).",
            "Least-squares line of y on x: slope b = Sxy / Sxx = r·s<sub>y</sub>/s<sub>x</sub>; it passes through (x̄, ȳ). "
            "R² = r² for simple linear regression.",
            "Covariance matrix Σ is symmetric positive semi-definite; Var(aᵀX) = aᵀΣa.",
        ]),
        ("fig", fig_corr),
        ("fig", fig_zero_corr),
        ("note", "Correlation measures LINEAR association only. A perfect quadratic relation can have ρ = 0.",
         "Trap"),
    ])

    st += section("A8. Discrete distributions", [
        ("table", [["Distribution", "PMF", "Mean", "Variance"],
                   ["Discrete uniform {a,…,b}", "1/(b − a + 1)", "(a + b)/2", "((b − a + 1)² − 1)/12"],
                   ["Bernoulli(p)", "pˣ(1 − p)¹⁻ˣ, x ∈ {0, 1}", "p", "p(1 − p)"],
                   ["Binomial(n, p)", "ⁿCₓ pˣ (1 − p)ⁿ⁻ˣ", "np", "np(1 − p)"],
                   ["Poisson(λ)", "e<super>−λ</super>λˣ / x!", "λ", "λ"],
                   ["Geometric(p), trials to 1st success", "(1 − p)ˣ⁻¹ p, x ≥ 1", "1/p", "(1 − p)/p²"],
                   ["Hypergeometric(N, K, n)", "ᴷCₓ ᴺ⁻ᴷCₙ₋ₓ / ᴺCₙ", "nK/N", "n(K/N)(1 − K/N)(N − n)/(N − 1)"]],
         dict(col_widths=[FRAME_W * 0.30, FRAME_W * 0.30, FRAME_W * 0.14, FRAME_W * 0.26], font_size=8.6,
              align_left_first=True)),
        ("fig", fig_discrete),
        ("bullets", [
            "Sum of n i.i.d. Bernoulli(p) is Binomial(n, p). Sum of independent Poissons is Poisson(λ₁ + λ₂).",
            "Binomial mode: ⌊(n + 1)p⌋. Poisson mode: ⌊λ⌋ (both λ − 1 and λ if λ is an integer).",
            "Poisson approximation to binomial: n large, p small, λ = np.",
            "Poisson process with rate λ: count in time t is Poisson(λt); gaps are Exponential(λ).",
            "Poisson thinning: if each event is kept with probability p, kept events form Poisson(λp).",
            "Memoryless (discrete): geometric, P(X > m + n | X > m) = P(X > n).",
        ]),
    ])

    st += section("A9. Continuous distributions", [
        ("table", [["Distribution", "PDF", "Mean", "Variance", "CDF / notes"],
                   ["Uniform(a, b)", "1/(b − a), a &lt; x &lt; b", "(a + b)/2", "(b − a)²/12", "(x − a)/(b − a)"],
                   ["Exponential(λ)", "λe<super>−λx</super>, x &gt; 0", "1/λ", "1/λ²", "1 − e<super>−λx</super>; median ln2/λ"],
                   ["Normal(μ, σ²)", "(1/σ√(2π)) e<super>−(x−μ)²/2σ²</super>", "μ", "σ²", "Φ((x − μ)/σ)"],
                   ["Standard normal", "φ(z) = e<super>−z²/2</super>/√(2π)", "0", "1", "Φ(−z) = 1 − Φ(z)"],
                   ["t with ν d.f.", "symmetric, bell-shaped", "0 (ν &gt; 1)", "ν/(ν − 2) (ν &gt; 2)", "heavier tails"],
                   ["Chi-squared, k d.f.", "on x &gt; 0, right-skewed", "k", "2k", "Σ of k squared N(0,1)"]],
         dict(col_widths=[FRAME_W * 0.19, FRAME_W * 0.29, FRAME_W * 0.12, FRAME_W * 0.17, FRAME_W * 0.23],
              font_size=8.4, align_left_first=True)),
        ("fig", fig_continuous),
        ("bullets", [
            "<b>Memoryless:</b> X ∼ Exp(λ) ⇒ P(X > s + t | X > s) = P(X > t). Only continuous memoryless law.",
            "<b>Minimum of exponentials:</b> min(X₁, …, Xₙ) with rates λᵢ is Exp(Σλᵢ); P(Xᵢ is smallest) = λᵢ/Σλⱼ.",
            "<b>Normal closure:</b> independent normals add: aX + bY ∼ N(aμ<sub>X</sub> + bμ<sub>Y</sub>, a²σ<sub>X</sub>² + b²σ<sub>Y</sub>²).",
            "<b>Standardising:</b> Z = (X − μ)/σ ∼ N(0, 1).",
            "<b>t-distribution:</b> T = Z / √(V/ν) with Z ∼ N(0,1), V ∼ χ²<sub>ν</sub> independent.",
            "<b>Chi-squared:</b> if Z₁, …, Zₖ i.i.d. N(0,1), ΣZᵢ² ∼ χ²ₖ; independent χ² add their d.f.; "
            "(n − 1)S²/σ² ∼ χ²<sub>n−1</sub> for normal samples.",
            "<b>Uniform order statistics:</b> the k-th smallest of n i.i.d. U(0,1) has mean k/(n + 1).",
        ]),
        ("fig", fig_t_chi),
        ("fig", fig_empirical),
        ("table", [["Key z values", "Φ(z)", "Use"],
                   ["1.282", "0.90", "one-sided 10%; 80% two-sided CI"],
                   ["1.645", "0.95", "one-sided 5%; 90% two-sided CI"],
                   ["1.960", "0.975", "two-sided 5%; 95% CI"],
                   ["2.326", "0.99", "one-sided 1%; 98% CI"],
                   ["2.576", "0.995", "two-sided 1%; 99% CI"]]),
    ])

    st += section("A10. Joint, marginal and conditional distributions", [
        ("table", [["", "Discrete", "Continuous"],
                   ["Joint", "p(x, y) = P(X = x, Y = y)", "f(x, y), P((X,Y) ∈ R) = ∬<sub>R</sub> f"],
                   ["Marginal", "p<sub>X</sub>(x) = Σ<sub>y</sub> p(x, y)", "f<sub>X</sub>(x) = ∫ f(x, y) dy"],
                   ["Conditional", "p(x | y) = p(x, y)/p<sub>Y</sub>(y)", "f(x | y) = f(x, y)/f<sub>Y</sub>(y)"],
                   ["Independence", "p(x, y) = p<sub>X</sub>(x)p<sub>Y</sub>(y) ∀x,y",
                    "f(x, y) = f<sub>X</sub>(x)f<sub>Y</sub>(y) ∀x,y"]],
         dict(col_widths=[FRAME_W * 0.2, FRAME_W * 0.4, FRAME_W * 0.4], align_left_first=True)),
        "For independence of continuous X, Y the joint support must be a <b>rectangle</b> (product set) and "
        "the density must factor. A triangular support such as 0 &lt; x &lt; y &lt; 1 immediately implies dependence.",
        ("fig", fig_joint_region),
        "<b>Recipe for joint-pdf questions:</b> (1) sketch the support; (2) find the constant from ∬f = 1; "
        "(3) set integration limits from the sketch; (4) for a conditional pdf divide by the marginal "
        "and keep the conditional support.",
        "<b>Bivariate normal:</b> E[Y | X = x] = μ<sub>Y</sub> + ρ(σ<sub>Y</sub>/σ<sub>X</sub>)(x − μ<sub>X</sub>), "
        "Var(Y | X) = σ<sub>Y</sub>²(1 − ρ²).",
    ])

    st += section("A11. Sampling distributions and the Central Limit Theorem", [
        "For i.i.d. X₁, …, Xₙ with mean μ and variance σ²:",
        "$$E[\\bar{X}]=\\mu,\\qquad \\mathrm{Var}(\\bar{X})=\\dfrac{\\sigma^2}{n},\\qquad "
        "\\mathrm{SE}(\\bar{X})=\\dfrac{\\sigma}{\\sqrt{n}}",
        "<b>CLT:</b> for large n (rule of thumb n ≥ 30),",
        "$$\\dfrac{\\bar{X}-\\mu}{\\sigma/\\sqrt{n}}\\ \\approx\\ N(0,1),\\qquad "
        "\\sum_{i=1}^{n}X_i\\ \\approx\\ N(n\\mu,\\ n\\sigma^2)",
        ("fig", fig_clt),
        "<b>Normal approximation to Binomial(n, p)</b> (np ≥ 5 and n(1 − p) ≥ 5): X ≈ N(np, np(1 − p)) "
        "with <b>continuity correction</b>: P(X ≤ k) ≈ Φ((k + 0.5 − np)/√(np(1 − p))), "
        "P(X ≥ k) ≈ 1 − Φ((k − 0.5 − np)/√(np(1 − p))).",
        "<b>Sample proportion:</b> p̂ ≈ N(p, p(1 − p)/n).",
        "If the population itself is normal, X̄ is exactly normal for every n. With σ unknown and normal data, "
        "(X̄ − μ)/(S/√n) ∼ t<sub>n−1</sub> exactly.",
        ("note", "Halving the standard error needs FOUR times the sample size, because SE ∝ 1/√n.", "Shortcut"),
    ])

    st += section("A12. Confidence intervals", [
        ("table", [["Parameter", "Conditions", "100(1 − α)% interval"],
                   ["Mean μ", "σ known (or n large)", "x̄ ± z<sub>α/2</sub> σ/√n"],
                   ["Mean μ", "σ unknown, normal data", "x̄ ± t<sub>α/2, n−1</sub> s/√n"],
                   ["Proportion p", "np̂, n(1 − p̂) ≥ 5", "p̂ ± z<sub>α/2</sub> √(p̂(1 − p̂)/n)"],
                   ["μ₁ − μ₂", "σ's known", "(x̄₁ − x̄₂) ± z<sub>α/2</sub> √(σ₁²/n₁ + σ₂²/n₂)"],
                   ["μ₁ − μ₂", "equal unknown σ (pooled)", "(x̄₁ − x̄₂) ± t<sub>α/2, n₁+n₂−2</sub> s<sub>p</sub>√(1/n₁ + 1/n₂)"],
                   ["Variance σ²", "normal data",
                    "[(n − 1)s²/χ²<sub>α/2, n−1</sub>,  (n − 1)s²/χ²<sub>1−α/2, n−1</sub>]"]],
         dict(col_widths=[FRAME_W * 0.17, FRAME_W * 0.28, FRAME_W * 0.55], align_left_first=True)),
        "$$s_p^2=\\dfrac{(n_1-1)s_1^2+(n_2-1)s_2^2}{n_1+n_2-2},\\qquad "
        "n=\\left(\\dfrac{z_{\\alpha/2}\\,\\sigma}{E}\\right)^2\\ \\mathrm{for\\ margin}\\ E",
        ("fig", fig_ci),
        ("bullets", [
            "Width = 2 × margin of error. Width ↑ with confidence level and σ; ↓ with √n.",
            "Interpretation: 95% of intervals built this way contain μ. A computed interval either contains μ or not — "
            "it is NOT 'μ lies in it with probability 0.95'.",
            "A two-sided level-α test rejects H₀: μ = μ₀ exactly when μ₀ lies outside the 100(1 − α)% CI.",
            "For a proportion with no prior estimate, use p̂ = 0.5 (maximises p(1 − p)) in sample-size formulas.",
        ]),
    ])

    st += section("A13. Hypothesis testing: z-test, t-test, chi-squared test", [
        ("bullets", [
            "<b>Steps:</b> state H₀ and H₁ → choose α → compute the test statistic → find the critical value or "
            "p-value → decide (reject H₀ if statistic is in the rejection region, equivalently p-value ≤ α).",
            "<b>p-value:</b> probability, under H₀, of a statistic at least as extreme as observed. "
            "Two-sided: p = 2(1 − Φ(|z|)).",
            "<b>Type I error</b> α = P(reject H₀ | H₀ true); <b>Type II</b> β = P(fail to reject | H₁ true); "
            "<b>power</b> = 1 − β.",
        ]),
        ("fig", fig_rejection),
        ("table", [["Test", "Statistic", "Distribution under H₀"],
                   ["One-sample z", "z = (x̄ − μ₀)/(σ/√n)", "N(0, 1)"],
                   ["Proportion z", "z = (p̂ − p₀)/√(p₀(1 − p₀)/n)", "≈ N(0, 1)"],
                   ["One-sample t", "t = (x̄ − μ₀)/(s/√n)", "t<sub>n−1</sub>"],
                   ["Paired t", "t = d̄/(s<sub>d</sub>/√n) on differences", "t<sub>n−1</sub>"],
                   ["Two-sample pooled t", "t = (x̄₁ − x̄₂)/(s<sub>p</sub>√(1/n₁ + 1/n₂))", "t<sub>n₁+n₂−2</sub>"],
                   ["χ² goodness of fit", "χ² = Σ(O − E)²/E over k cells", "χ²<sub>k−1−m</sub> (m = fitted params)"],
                   ["χ² independence (r × c)", "χ² = Σ(O − E)²/E, E = row·col/N", "χ²<sub>(r−1)(c−1)</sub>"],
                   ["χ² for variance", "χ² = (n − 1)s²/σ₀²", "χ²<sub>n−1</sub>"]],
         dict(col_widths=[FRAME_W * 0.25, FRAME_W * 0.45, FRAME_W * 0.30], align_left_first=True)),
        ("fig", fig_errors),
        ("bullets", [
            "Increasing n (for fixed α) increases power; decreasing α (stricter test) decreases power.",
            "χ² tests: use counts, not percentages; each expected count should be ≥ 5 (merge cells otherwise). "
            "The χ² independence/GOF test is right-tailed.",
            "For a 2 × 2 table the χ² statistic equals z² of the two-proportion z-test.",
            "Use t (not z) when σ is unknown and n is small; as d.f. → ∞, t critical values → z critical values.",
        ]),
        ("note", "'Fail to reject H₀' is not 'accept H₀ is true'. And a p-value is NOT the probability that "
                 "H₀ is true.", "Trap"),
    ])

    st += section("A14. Twenty high-frequency exam traps", [
        ("bullets", [
            "Confusing 'mutually exclusive' with 'independent'.",
            "Using n instead of n − 1 for the sample standard deviation (or vice versa) — read the question.",
            "Forgetting continuity correction when approximating a discrete count by a normal.",
            "Using Var(X − Y) = Var(X) − Var(Y): variances of independent terms ALWAYS add.",
            "Writing SD(X + Y) = SD(X) + SD(Y) — add variances, then take the square root.",
            "Treating P(A | B) as P(B | A) (prosecutor's fallacy).",
            "Missing that 'at least one' is easiest via the complement.",
            "Using one-sided critical values for two-sided alternatives (1.645 vs 1.96).",
            "Wrong χ² degrees of freedom: (r − 1)(c − 1) for independence, k − 1 − m for goodness of fit.",
            "Integrating a joint pdf over the wrong region — always sketch the support first.",
            "Assuming zero covariance implies independence.",
            "Forgetting that P(X = a) = 0 for continuous X, so ≤ and &lt; give the same probability.",
            "For Poisson over a different time window, rescale λ (λt).",
            "Exponential parameter: rate λ (mean 1/λ) vs scale β (mean β) — check which is given.",
            "The median of an Exponential(λ) is ln 2/λ, not 1/λ.",
            "Var(aX) = a²Var(X), not aVar(X).",
            "Sampling without replacement → hypergeometric, not binomial.",
            "Normal tables give Φ(z) = P(Z ≤ z); for P(Z > z) subtract from 1.",
            "A CI for μ is about μ, not about individual observations (that would be a prediction interval).",
            "The t-statistic uses s/√n; the d.f. for a paired test is (number of pairs − 1).",
        ]),
    ])
    st.append(PageBreak())
    return st
