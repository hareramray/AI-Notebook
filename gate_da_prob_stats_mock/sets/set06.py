"""Mock Test 06 - Topic Test: Random Variables, Distributions, PDFs & CDFs."""
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ====================================================================== computed answers
A2 = math.exp(-4 / 5)
A3 = stats.norm.cdf(2) - stats.norm.cdf(-1)
A10 = math.log(2) / 0.5
A13 = 1 / 6
A17 = math.exp(-1.5)
Z90, Z75 = 1.2816, 0.6745  # the table values stated in Q19
SIG19 = 12 / (Z90 + Z75)
MU19 = 60 + Z75 * SIG19
A20 = 1 - 4 * math.exp(-3)
A20_exact = 1 - stats.binom.cdf(1, 1500, 0.002)
A21 = -1 / 11
A22_sf = stats.chi2(10).sf(10)
A23 = 2 + 3 - 1 / (1 / 2 + 1 / 3)
A24 = optimize.brentq(lambda x: 4 * x ** 3 - 3 * x ** 4 - 0.5, 0, 1)
A25 = 1 - math.exp(-1)
P26 = stats.binom.cdf(2, 10, 0.2)
A26 = 5 * P26
A27 = stats.norm.cdf(0.8)
A28_med = 0.5 ** (1 / 3)
A29 = 1 - 2 / (math.e ** 2 - 1)


# ====================================================================== figures
def fig_exp_q2():
    x = np.linspace(0, 20, 400)
    f = 0.2 * np.exp(-0.2 * x)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, f, color=BLUE)
    m = x >= 7
    ax.fill_between(x[m], f[m], color=MAROON, alpha=0.3)
    m2 = x >= 3
    ax.fill_between(x[m2], f[m2], color=GOLD, alpha=0.25)
    ax.axvline(3, color="#555555", ls="--", lw=0.8)
    ax.axvline(7, color="#555555", ls="--", lw=0.8)
    ax.text(3.2, 0.17, "survived to t = 3", fontsize=8)
    ax.text(7.3, 0.08, "P(T > 7) / P(T > 3)\n= e$^{-1.4}$/e$^{-0.6}$ = e$^{-0.8}$", fontsize=8, color=MAROON)
    ax.set_xlabel("t (years)")
    ax.set_yticks([])
    ax.set_title("Exponential lifetime, mean 5", fontsize=9)
    return fig


def fig_norm_q3():
    x = np.linspace(18, 82, 400)
    f = stats.norm.pdf(x, 50, 8)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, f, color=BLUE)
    m = (x > 42) & (x < 66)
    ax.fill_between(x[m], f[m], color=MAROON, alpha=0.3)
    ax.set_xticks([34, 42, 50, 58, 66])
    ax.set_xticklabels(["34\n(z = −2)", "42\n(z = −1)", "50\n(z = 0)", "58\n(z = 1)", "66\n(z = 2)"],
                       fontsize=8)
    ax.set_yticks([])
    ax.text(51, 0.012, f"≈ {A3:.4f}", ha="center", fontsize=9)
    return fig


def fig_pois_q6():
    k = np.arange(0, 9)
    p = stats.poisson.pmf(k, 2)
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.bar(k, p, color=[MAROON if kk in (1, 2) else BLUE for kk in k], width=0.6)
    for kk, pp in zip(k, p):
        ax.text(kk, pp + 0.007, f"{pp:.3f}", ha="center", fontsize=7.5)
    ax.set_xlabel("k")
    ax.set_ylabel("P(X = k)")
    ax.set_title("Poisson(2): tied modes at k = 1 and k = 2", fontsize=9)
    ax.set_ylim(0, 0.33)
    return fig


def fig_gamma_q9():
    x = np.linspace(0, 8, 300)
    fig, axs = plt.subplots(1, 2, figsize=(6, 2.4))
    axs[0].plot(x, 1 - (1 + x) * np.exp(-x), color=BLUE)
    axs[0].set_title("CDF  F(x) = 1 − (1 + x)e$^{-x}$", fontsize=8.5)
    axs[1].plot(x, x * np.exp(-x), color=MAROON)
    axs[1].axvline(1, color=GOLD, ls="--")
    axs[1].text(1.15, 0.05, "mode x = 1", fontsize=8)
    axs[1].set_title("pdf  f(x) = F′(x) = x e$^{-x}$", fontsize=8.5)
    for a in axs:
        a.set_xlabel("x")
    fig.tight_layout()
    return fig


def fig_region_q13():
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.fill_between([0, 1], [0, 0], [0, 1], color=BLUE, alpha=0.15)
    ax.fill([0, 0.5, 1], [0, 0.5, 0], color=MAROON, alpha=0.35)
    ax.plot([0, 1], [0, 1], color=BLUE)
    ax.plot([0, 1], [1, 0], color=MAROON, ls="--")
    ax.text(0.45, 0.15, "y &lt; x and\nx + y &lt; 1".replace("&lt;", "<"), fontsize=8.5, ha="center")
    ax.text(0.78, 0.55, "support\n0 < y < x < 1", fontsize=8.5, color=BLUE)
    ax.text(0.05, 0.92, "x + y = 1", color=MAROON, fontsize=8.5)
    ax.text(0.27, 0.36, "y = x", color=BLUE, fontsize=8.5)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    return fig


def fig_transform_q16():
    fig, axs = plt.subplots(1, 2, figsize=(6, 2.6))
    x = np.linspace(-1, 2, 300)
    axs[0].plot(x, x ** 2, color=BLUE)
    axs[0].axhline(1, color="#888888", ls=":")
    axs[0].fill_between(x[x <= 1], 0, x[x <= 1] ** 2, color=GOLD, alpha=0.3)
    axs[0].fill_between(x[x >= 1], 0, x[x >= 1] ** 2, color=MAROON, alpha=0.2)
    axs[0].text(-0.9, 2.5, "y ∈ (0,1): two roots ±√y", fontsize=7.5)
    axs[0].text(-0.9, 2.0, "y ∈ (1,4): one root +√y", fontsize=7.5, color=MAROON)
    axs[0].set_xlabel("x")
    axs[0].set_ylabel("y = x²")
    y1 = np.linspace(0.02, 1, 200)
    y2 = np.linspace(1, 4, 200)
    axs[1].plot(y1, 1 / (3 * np.sqrt(y1)), color=BLUE)
    axs[1].plot(y2, 1 / (6 * np.sqrt(y2)), color=MAROON)
    axs[1].set_ylim(0, 1.5)
    axs[1].set_xlabel("y")
    axs[1].set_title("pdf of Y (jump at y = 1)", fontsize=8.5)
    fig.tight_layout()
    return fig


def fig_cdf_q18():
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.plot([-1, 0], [0, 0], color=BLUE, lw=2)
    ax.plot([0, 1], [0.25, 0.5], color=BLUE, lw=2)
    ax.plot([1, 2], [0.75, 0.75], color=BLUE, lw=2)
    ax.plot([2, 3], [1, 1], color=BLUE, lw=2)
    for xx, lo, hi in [(0, 0, 0.25), (1, 0.5, 0.75), (2, 0.75, 1)]:
        ax.plot([xx, xx], [lo, hi], color="#999999", ls=":")
        ax.plot(xx, hi, "o", color=BLUE, ms=5)
        ax.plot(xx, lo, "o", mfc="white", mec=BLUE, ms=5)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_xticks([-1, 0, 1, 2, 3])
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.set_ylim(-0.05, 1.1)
    ax.grid(alpha=0.25)
    return fig


def fig_chi2_q22():
    x = np.linspace(0.01, 30, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    for k, c in [(2, GOLD), (5, BLUE), (10, MAROON)]:
        ax.plot(x, stats.chi2.pdf(x, k), color=c, label=f"df = {k}")
    ax.axvline(10, color=MAROON, ls=":", lw=1)
    ax.axvline(stats.chi2(10).median(), color=MAROON, ls="--", lw=1)
    ax.text(10.4, 0.2, "mean 10", fontsize=8, color=MAROON)
    ax.text(9.1, 0.25, f"median {stats.chi2(10).median():.2f}", fontsize=8, color=MAROON, ha="right")
    ax.set_ylim(0, 0.32)
    ax.set_yticks([])
    ax.set_xlabel("x")
    ax.legend(fontsize=8, frameon=False)
    ax.set_title("χ² densities are right-skewed: median &lt; mean".replace("&lt;", "<"), fontsize=9)
    return fig


def fig_beta_q24():
    x = np.linspace(0, 1, 300)
    f = 12 * x ** 2 * (1 - x)
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.plot(x, f, color=BLUE)
    ax.fill_between(x[x <= A24], f[x <= A24], color=BLUE, alpha=0.15)
    for v, lab, c, dy in [(0.6, "mean 0.600", GOLD, 0.25), (A24, f"median {A24:.3f}", MAROON, 0.75),
                          (2 / 3, "mode 0.667", "#22663a", 1.25)]:
        ax.axvline(v, color=c, ls="--", lw=1.2)
        ax.text(v + 0.01, dy, lab, fontsize=8, color=c if c != GOLD else "#8a6a00")
    ax.text(0.2, 0.6, "area 0.5", fontsize=8, color=BLUE)
    ax.set_xlabel("x")
    ax.set_title("f(x) = 12x²(1 − x): left-skewed, mean < median < mode", fontsize=9)
    return fig


def fig_norm_q27():
    x = np.linspace(-12, 20, 400)
    f = stats.norm.pdf(x, 4, 5)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, f, color=BLUE)
    m = x > 0
    ax.fill_between(x[m], f[m], color=MAROON, alpha=0.3)
    ax.axvline(0, color="#555555", ls="--", lw=0.8)
    ax.text(6, 0.03, f"P(D > 0) ≈ {A27:.4f}", fontsize=9, color=MAROON)
    ax.set_xlabel("D = X − Y  ∼  N(4, 5²)")
    ax.set_yticks([])
    return fig


def fig_tri_q30():
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    z = np.array([0, 1, 2])
    ax.plot(z, [0, 1, 0], color=BLUE, lw=2)
    zz = np.linspace(1.5, 2, 50)
    ax.fill_between(zz, 2 - zz, color=MAROON, alpha=0.35)
    ax.plot([1.5, 1.5], [0, 0.5], color=MAROON, ls="--")
    ax.text(1.55, 0.55, "f(1.5) = 0.5", color=MAROON, fontsize=8.5)
    ax.text(1.72, 0.05, "0.125", fontsize=8.5)
    ax.set_xlabel("z")
    ax.set_ylabel("$f_Z(z)$")
    ax.set_title("Z = X + Y, X, Y i.i.d. U(0, 1): triangular density", fontsize=9)
    return fig


# ====================================================================== questions
Q = []

# ---------------- Q1
Q.append(dict(
    qtype="MCQ", marks=1, topic="Binomial: mean and variance", difficulty="Easy",
    text="A binomial random variable X has mean 6 and variance 4.2. The parameters (n, p) of X are",
    options=["n = 20, p = 0.3", "n = 30, p = 0.2", "n = 15, p = 0.4", "n = 20, p = 0.7"],
    answer="A",
    solution=[
        "<b>Concept:</b> for X ∼ Binomial(n, p): E[X] = np and Var(X) = np(1 − p).",
        "Divide variance by mean:",
        r"$$1-p=\dfrac{np(1-p)}{np}=\dfrac{4.2}{6}=0.7\;\Rightarrow\;p=0.3",
        r"$$n=\dfrac{6}{0.3}=20",
        "Check the distractors: (n, p) = (30, 0.2) gives variance 4.8; (15, 0.4) gives 3.6; (20, 0.7) has "
        "mean 14 — it swaps p and 1 − p.",
        ("note", "For a binomial, variance &lt; mean always (since 1 − p &lt; 1). If a problem quotes variance ≥ "
                 "mean, no binomial fits.", "Key idea"),
    ],
))

# ---------------- Q2
Q.append(dict(
    qtype="MCQ", marks=1, topic="Exponential: memorylessness", difficulty="Easy",
    text="The lifetime of an SSD is exponentially distributed with mean 5 years. A drive has already worked "
         "for 3 years. The probability that it works for at least 4 MORE years is",
    options=["e<super>−1.4</super>", "1 − e<super>−0.8</super>", "e<super>−0.8</super>",
             "e<super>−0.6</super>"],
    answer="C",
    solution=[
        "<b>Concept:</b> memoryless property P(T &gt; s + t | T &gt; s) = P(T &gt; t); for rate λ, "
        "P(T &gt; t) = e<super>−λt</super>.",
        "Rate λ = 1/mean = 0.2 per year.",
        r"$$P(T>7\mid T>3)=\dfrac{e^{-0.2(7)}}{e^{-0.2(3)}}=e^{-0.2(4)}=e^{-0.8}",
        f"Numerically e<super>−0.8</super> ≈ {A2:.4f}.",
        ("fig", fig_exp_q2),
        "e<super>−1.4</super> = P(T &gt; 7) ignores the conditioning; e<super>−0.6</super> = P(T &gt; 3); "
        "1 − e<super>−0.8</super> is the probability of failing within the next 4 years.",
        ("note", "The exponential is the only continuous distribution without memory: a used drive is as good "
                 "as new.", "Key idea"),
    ],
))

# ---------------- Q3
Q.append(dict(
    qtype="NAT", marks=1, topic="Normal: standardisation", difficulty="Easy",
    text="X ∼ N(50, 8<super>2</super>). Using Φ(1) = 0.8413 and Φ(2) = 0.9772, the value of "
         "P(42 &lt; X &lt; 66) is ______ (round off to 3 decimal places).",
    answer=f"{A3:.3f}", range=(0.817, 0.820),
    solution=[
        "<b>Concept:</b> standardise Z = (X − μ)/σ and use Φ(−a) = 1 − Φ(a).",
        r"$$z_1=\dfrac{42-50}{8}=-1,\qquad z_2=\dfrac{66-50}{8}=2",
        r"$$P(-1<Z<2)=\Phi(2)-\Phi(-1)=\Phi(2)-[1-\Phi(1)]",
        r"$$=0.9772-0.1587=0.8185\approx 0.819",
        ("fig", fig_norm_q3),
        ("note", "Asymmetric intervals must be split: 0.3413 (from −1 to 0) + 0.4772 (from 0 to 2) = 0.8185.",
         "Shortcut"),
    ],
))

# ---------------- Q4
Q.append(dict(
    qtype="MSQ", marks=1, topic="Properties of a CDF", difficulty="Medium",
    text="Which of the following functions is/are valid cumulative distribution functions?",
    options=["F(x) = 1 − e<super>−x</super> for all real x",
             "F(x) = exp(−e<super>−x</super>) for all real x",
             "F(x) = 0 for x &lt; 0;  F(x) = (x + 1)/2 for 0 ≤ x &lt; 1;  F(x) = 1 for x ≥ 1",
             "F(x) = 0 for x &lt; 0;  F(x) = sin x for 0 ≤ x &lt; π;  F(x) = 1 for x ≥ π"],
    answer="B, C",
    solution=[
        "<b>Concept:</b> F is a CDF iff it is non-decreasing, right-continuous, F(−∞) = 0 and F(+∞) = 1.",
        "<b>(A) INVALID</b>: as x → −∞, e<super>−x</super> → ∞ so F(x) → −∞; also F(−1) = 1 − e ≈ −1.72 &lt; 0.",
        "<b>(B) VALID</b> (Gumbel CDF): −e<super>−x</super> increases with x, so F is increasing and "
        "continuous; F → e<super>−∞</super> = 0 as x → −∞ and → e<super>0</super> = 1 as x → ∞.",
        "<b>(C) VALID</b> (mixed): F jumps from 0 to 1/2 at x = 0 (a point mass of 1/2, right-continuous), "
        "then rises linearly to 1 at x = 1. Non-decreasing with correct limits.",
        "<b>(D) INVALID</b>: sin x decreases on (π/2, π), e.g. F(π/2) = 1 &gt; F(3π/4) ≈ 0.707.",
        ("note", "A CDF may jump (discrete part) but may never go down. Jumps must be closed at the top "
                 "(right-continuity).", "Key idea"),
    ],
))

# ---------------- Q5
Q.append(dict(
    qtype="MCQ", marks=1, topic="Chi-squared as sum of squared normals", difficulty="Easy",
    text="Z<sub>1</sub>, …, Z<sub>5</sub> are i.i.d. N(0, 1) and W = Z<sub>1</sub><super>2</super> + … + "
         "Z<sub>5</sub><super>2</super>. The mean and variance of W are respectively",
    options=["5 and 5", "0 and 5", "5 and 25", "5 and 10"],
    answer="D",
    solution=[
        "<b>Concept:</b> a sum of k squared independent standard normals is χ²<sub>k</sub>, with mean k and "
        "variance 2k.",
        "For one term: E[Z<super>2</super>] = Var(Z) = 1 and E[Z<super>4</super>] = 3, so",
        r"$$\mathrm{Var}(Z^2)=E[Z^4]-(E[Z^2])^2=3-1=2",
        r"$$E[W]=5(1)=5,\qquad \mathrm{Var}(W)=5(2)=10",
        "'5 and 5' assumes Var(Z<super>2</super>) = 1; '0 and 5' confuses W with ∑Z<sub>i</sub>; "
        "'5 and 25' squares the mean.",
        ("note", "χ²<sub>k</sub>: mean = df, variance = 2·df. Memorise E[Z<super>4</super>] = 3.", "Shortcut"),
    ],
))

# ---------------- Q6
Q.append(dict(
    qtype="MSQ", marks=1, topic="Poisson PMF & mode", difficulty="Medium",
    text="Help-desk calls arrive as a Poisson process at 3 calls per hour. Let X be the number of calls in "
         "a 40-minute window. Which of the following is/are TRUE?",
    options=["P(X = 1) = P(X = 2)",
             "E[X] = Var(X)",
             "X has a unique mode",
             "P(X ≥ 1) = 1 − e<super>−2</super>"],
    answer="A, B, D",
    solution=[
        "<b>Concept:</b> counts in a window of length t have Poisson(λt) distribution, "
        "P(X = k) = e<super>−μ</super>μ<super>k</super>/k!.",
        r"$$\mu=\lambda t=3\times\dfrac{40}{60}=2",
        "<b>(A) TRUE</b>: P(X = 1) = 2e<super>−2</super> and P(X = 2) = 2<super>2</super>e<super>−2</super>/2 "
        "= 2e<super>−2</super>.",
        "<b>(B) TRUE</b>: for a Poisson, mean = variance = μ = 2.",
        "<b>(C) FALSE</b>: since μ = 2 is an integer, the PMF ratio P(k)/P(k − 1) = μ/k equals 1 at k = 2, "
        "so k = 1 and k = 2 are tied modes.",
        ("fig", fig_pois_q6),
        "<b>(D) TRUE</b>: P(X ≥ 1) = 1 − P(X = 0) = 1 − e<super>−2</super> ≈ 0.8647.",
        ("note", "Poisson mode = ⌊μ⌋, with a tie between μ − 1 and μ whenever μ is an integer.", "Trap"),
    ],
))

# ---------------- Q7
Q.append(dict(
    qtype="MCQ", marks=1, topic="Continuous uniform", difficulty="Easy",
    text="X is uniformly distributed on (a, b) with E[X] = 5 and Var(X) = 3. Then P(X &gt; 6) equals",
    options=["1/4", "1/3", "1/2", "1/6"],
    answer="B",
    solution=[
        "<b>Concept:</b> for U(a, b), mean = (a + b)/2, variance = (b − a)<super>2</super>/12.",
        r"$$\dfrac{(b-a)^2}{12}=3\Rightarrow b-a=6,\qquad a+b=10",
        "So a = 2, b = 8 and the density is 1/6 on (2, 8).",
        r"$$P(X>6)=\dfrac{8-6}{8-2}=\dfrac{2}{6}=\dfrac{1}{3}",
        "1/6 confuses the density height with a probability; 1/2 is P(X &gt; mean).",
        ("note", "Uniform probabilities are length ratios — find the endpoints first.", "Shortcut"),
    ],
))

# ---------------- Q8
Q.append(dict(
    qtype="MSQ", marks=1, topic="Student t-distribution properties", difficulty="Medium",
    text="Let T<sub>ν</sub> denote a random variable having Student's t-distribution with ν degrees of "
         "freedom. Which of the following is/are TRUE?",
    options=["The density of T<sub>ν</sub> is symmetric about 0 for every ν",
             "Var(T<sub>5</sub>) = 5/3",
             "T<sub>ν</sub> has heavier tails than N(0, 1), e.g. P(|T<sub>5</sub>| &gt; 2) &gt; P(|Z| &gt; 2)",
             "T<sub>1</sub> has a finite mean equal to 0"],
    answer="A, B, C",
    solution=[
        "<b>Concept:</b> T<sub>ν</sub> = Z/√(V/ν) with Z ∼ N(0,1), V ∼ χ²<sub>ν</sub> independent; "
        "E[T] = 0 for ν &gt; 1 and Var(T) = ν/(ν − 2) for ν &gt; 2.",
        "<b>(A) TRUE</b>: Z is symmetric and independent of V, so −T has the same distribution as T.",
        "<b>(B) TRUE</b>:",
        r"$$\mathrm{Var}(T_5)=\dfrac{5}{5-2}=\dfrac{5}{3}\approx 1.667",
        f"<b>(C) TRUE</b>: P(|T<sub>5</sub>| &gt; 2) = {2 * stats.t(5).sf(2):.4f} versus "
        f"P(|Z| &gt; 2) = {2 * stats.norm.sf(2):.4f}. The extra randomness in the denominator fattens tails.",
        "<b>(D) FALSE</b>: T<sub>1</sub> is the standard Cauchy distribution; ∫|t|/(π(1 + t<super>2</super>)) dt "
        "diverges, so its mean does not exist (even though the density is symmetric about 0).",
        ("note", "As ν → ∞, T<sub>ν</sub> → N(0, 1) and the variance ν/(ν − 2) → 1.", "Key idea"),
    ],
))

# ---------------- Q9
Q.append(dict(
    qtype="MCQ", marks=1, topic="PDF from CDF", difficulty="Easy",
    text="A continuous random variable has CDF F(x) = 1 − (1 + x)e<super>−x</super> for x ≥ 0 "
         "(and F(x) = 0 for x &lt; 0). Its probability density function for x &gt; 0 is",
    options=["x e<super>−x</super>", "(1 + x) e<super>−x</super>", "e<super>−x</super>",
             "(2 + x) e<super>−x</super>"],
    answer="A",
    solution=[
        "<b>Concept:</b> f(x) = F′(x) wherever F is differentiable.",
        r"$$f(x)=-\dfrac{d}{dx}\left[(1+x)e^{-x}\right]=-\left[e^{-x}-(1+x)e^{-x}\right]",
        r"$$f(x)=-e^{-x}+(1+x)e^{-x}=x\,e^{-x},\qquad x>0",
        "This is the Gamma(2, 1) density (sum of two independent Exp(1) variables), with mean 2 and mode 1.",
        ("fig", fig_gamma_q9),
        "(1 + x)e<super>−x</super> is 1 − F(x), the survival function — not the pdf.",
        ("note", "Quick check: the candidate must integrate to 1 and be ≥ 0; (1 + x)e<super>−x</super> "
                 "integrates to 2, so it cannot be a pdf.", "Shortcut"),
    ],
))

# ---------------- Q10
Q.append(dict(
    qtype="NAT", marks=1, topic="Median (quantile) of exponential", difficulty="Easy",
    text="The waiting time T (in minutes) for a ride-share has pdf f(t) = 0.5 e<super>−0.5t</super> for "
         "t ≥ 0. The median of T is ______ minutes (round off to 2 decimal places).",
    answer=f"{A10:.2f}", range=(1.38, 1.39),
    solution=[
        "<b>Concept:</b> the median m solves F(m) = 1/2; for Exp(λ), F(t) = 1 − e<super>−λt</super>.",
        r"$$1-e^{-0.5m}=\dfrac{1}{2}\;\Rightarrow\;e^{-0.5m}=\dfrac{1}{2}\;\Rightarrow\;m=\dfrac{\ln 2}{0.5}",
        r"$$m=2\ln 2\approx 1.386\approx 1.39",
        "Compare: the mean is 1/λ = 2 minutes; the mode is 0.",
        ("note", "Exponential: mode (0) &lt; median (0.693/λ) &lt; mean (1/λ), as for every right-skewed "
                 "density of this shape.", "Key idea"),
    ],
))

# ---------------- Q11
Q.append(dict(
    qtype="MCQ", marks=1, topic="Bernoulli variance", difficulty="Easy",
    text="A Bernoulli(p) random variable X has Var(X) = 0.21 and p &gt; 0.5. The value of p is",
    options=["0.3", "0.79", "0.7", "0.21"],
    answer="C",
    solution=[
        "<b>Concept:</b> Var(Bernoulli(p)) = p(1 − p), which is symmetric about p = 1/2.",
        r"$$p(1-p)=0.21\;\Rightarrow\;p^2-p+0.21=0\;\Rightarrow\;p=\dfrac{1\pm\sqrt{1-0.84}}{2}=\dfrac{1\pm 0.4}{2}",
        "So p = 0.7 or p = 0.3; the condition p &gt; 0.5 selects p = 0.7.",
        ("note", "Var(X) ≤ 1/4 for any Bernoulli; both p and 1 − p give the same variance, so an extra "
                 "condition is always needed to pin p down.", "Trap"),
    ],
))

# ---------------- Q12
Q.append(dict(
    qtype="NAT", marks=1, topic="Discrete uniform variance", difficulty="Easy",
    text="X is uniformly distributed on {1, 2, …, n}. If Var(X) = 10, then n = ______.",
    answer="11", range=(11, 11),
    solution=[
        "<b>Concept:</b> for X uniform on {1, …, n}: E[X] = (n + 1)/2 and "
        "Var(X) = (n<super>2</super> − 1)/12.",
        r"$$\dfrac{n^2-1}{12}=10\;\Rightarrow\;n^2=121\;\Rightarrow\;n=11",
        "Derivation: E[X<super>2</super>] = (n + 1)(2n + 1)/6, so",
        r"$$\mathrm{Var}(X)=\dfrac{(n+1)(2n+1)}{6}-\dfrac{(n+1)^2}{4}=\dfrac{(n+1)(n-1)}{12}",
        ("note", "Do not confuse with the continuous U(a, b) variance (b − a)<super>2</super>/12, which "
                 "would give n − 1 = √120 — not an integer.", "Trap"),
    ],
))

# ---------------- Q13
Q.append(dict(
    qtype="NAT", marks=2, topic="Joint pdf: normalisation & region probability", difficulty="Medium",
    text="The joint pdf of (X, Y) is f(x, y) = k x y for 0 &lt; y &lt; x &lt; 1, and 0 otherwise. The value of "
         "P(X + Y &lt; 1) is ______ (round off to 3 decimal places).",
    answer=f"{A13:.3f}", range=(0.166, 0.168),
    solution=[
        "<b>Concept:</b> find k from ∬f = 1, then integrate f over the intersection of the support with the "
        "event.",
        "Step 1 — normalisation:",
        r"$$\int_0^1\int_0^x kxy\,dy\,dx=k\int_0^1\dfrac{x^3}{2}\,dx=\dfrac{k}{8}=1\;\Rightarrow\;k=8",
        ("fig", fig_region_q13),
        "Step 2 — region: y &lt; x and x + y &lt; 1 means y &lt; x &lt; 1 − y, which requires y &lt; 1/2. "
        "Integrate x first:",
        r"$$P=\int_0^{1/2}\int_y^{1-y}8xy\,dx\,dy=\int_0^{1/2}4y\left[(1-y)^2-y^2\right]dy",
        r"$$=\int_0^{1/2}4y(1-2y)\,dy=4\left[\dfrac{y^2}{2}-\dfrac{2y^3}{3}\right]_0^{1/2}",
        r"$$=4\left(\dfrac{1}{8}-\dfrac{1}{12}\right)=\dfrac{4}{24}=\dfrac{1}{6}\approx 0.167",
        ("note", "Integrating y first would need a split at x = 1/2 (upper limit min(x, 1 − x)); choosing "
                 "the order with a single expression for the limits saves work.", "Shortcut"),
    ],
))

# ---------------- Q14
Q.append(dict(
    qtype="MSQ", marks=2, topic="Marginal & conditional pdfs, covariance", difficulty="Hard",
    text="(X, Y) has joint pdf f(x, y) = e<super>−x</super> for 0 &lt; y &lt; x &lt; ∞, and 0 otherwise. "
         "Which of the following is/are TRUE?",
    options=["The marginal pdf of Y is f<sub>Y</sub>(y) = e<super>−y</super>, y &gt; 0",
             "X and Y are independent",
             "Given X = x, Y is uniformly distributed on (0, x)",
             "Cov(X, Y) = 1"],
    answer="A, C, D",
    solution=[
        "<b>Concept:</b> marginals by integrating out the other variable over the support; "
        "f<sub>Y|X</sub> = f/f<sub>X</sub>.",
        "<b>(A) TRUE</b>:",
        r"$$f_Y(y)=\int_y^{\infty}e^{-x}\,dx=e^{-y},\qquad y>0",
        "<b>(B) FALSE</b>: the support 0 &lt; y &lt; x is not a rectangle, so independence is impossible. "
        "Indeed f<sub>X</sub>(x) = ∫<sub>0</sub><super>x</super> e<super>−x</super> dy = x e<super>−x</super> and "
        "f<sub>X</sub>f<sub>Y</sub> = x e<super>−x−y</super> ≠ e<super>−x</super>.",
        "<b>(C) TRUE</b>:",
        r"$$f_{Y\mid X}(y\mid x)=\dfrac{e^{-x}}{x\,e^{-x}}=\dfrac{1}{x},\qquad 0<y<x",
        "<b>(D) TRUE</b>: write W = X − Y. The joint pdf of (Y, W) is e<super>−y</super>e<super>−w</super> "
        "(Jacobian 1), so Y and W are independent Exp(1). Then X = Y + W and",
        r"$$\mathrm{Cov}(X,Y)=\mathrm{Cov}(Y+W,\,Y)=\mathrm{Var}(Y)=1",
        "Check by moments: E[X] = 2, E[Y] = 1, E[XY] = E[X·E[Y | X]] = E[X<super>2</super>/2] = 6/2 = 3, "
        "so Cov = 3 − 2 = 1.",
        ("note", "Non-rectangular support ⇒ dependent, regardless of whether the formula factorises.", "Trap"),
    ],
))

# ---------------- Q15
Q.append(dict(
    qtype="MCQ", marks=2, topic="Conditional pdf & conditional expectation", difficulty="Medium",
    text="For the joint pdf f(x, y) = 8xy on 0 &lt; y &lt; x &lt; 1 (0 elsewhere), the conditional "
         "expectation E[Y | X = x] for 0 &lt; x &lt; 1 is",
    options=["x/2", "2x/3", "x/3", "3x/4"],
    answer="B",
    solution=[
        "<b>Concept:</b> f<sub>Y|X</sub>(y | x) = f(x, y)/f<sub>X</sub>(x); then E[Y | X = x] = "
        "∫ y f<sub>Y|X</sub>(y | x) dy.",
        "Step 1 — marginal of X:",
        r"$$f_X(x)=\int_0^x 8xy\,dy=4x^3,\qquad 0<x<1",
        "Step 2 — conditional pdf:",
        r"$$f_{Y\mid X}(y\mid x)=\dfrac{8xy}{4x^3}=\dfrac{2y}{x^2},\qquad 0<y<x",
        "Step 3 — conditional mean:",
        r"$$E[Y\mid X=x]=\int_0^x y\cdot\dfrac{2y}{x^2}\,dy=\dfrac{2}{x^2}\cdot\dfrac{x^3}{3}=\dfrac{2x}{3}",
        "x/2 would be right only if Y | X were uniform on (0, x); here the conditional density 2y/x<super>2</super> "
        "leans toward larger y.",
        ("note", "Tower check: E[Y] = E[2X/3] = (2/3)(4/5) = 8/15, which matches ∫ y·4y(1 − y<super>2</super>) dy "
                 "= 8/15 computed from f<sub>Y</sub>(y) = 4y(1 − y<super>2</super>).", "Key idea"),
    ],
))

# ---------------- Q16
Q.append(dict(
    qtype="MCQ", marks=2, topic="Transformation of a random variable (non-monotone)", difficulty="Hard",
    text="X ∼ Uniform(−1, 2) and Y = X<super>2</super>. The pdf of Y is",
    options=["f<sub>Y</sub>(y) = 1/(6√y) for 0 &lt; y &lt; 4",
             "f<sub>Y</sub>(y) = 1/(3√y) for 0 &lt; y &lt; 4",
             "f<sub>Y</sub>(y) = 1/(6√y) for 0 &lt; y &lt; 1, and 1/(3√y) for 1 &lt; y &lt; 4",
             "f<sub>Y</sub>(y) = 1/(3√y) for 0 &lt; y &lt; 1, and 1/(6√y) for 1 &lt; y &lt; 4"],
    answer="D",
    solution=[
        "<b>Concept:</b> for a non-monotone g, sum over all roots: "
        "f<sub>Y</sub>(y) = ∑ f<sub>X</sub>(x<sub>i</sub>)/|g′(x<sub>i</sub>)|.",
        "f<sub>X</sub> = 1/3 on (−1, 2) and |g′(x)| = 2|x| = 2√y at x = ±√y.",
        "<b>Case 0 &lt; y &lt; 1</b>: both roots ±√y lie in (−1, 2):",
        r"$$f_Y(y)=\dfrac{1/3}{2\sqrt{y}}+\dfrac{1/3}{2\sqrt{y}}=\dfrac{1}{3\sqrt{y}}",
        "<b>Case 1 &lt; y &lt; 4</b>: only +√y ∈ (1, 2) is in the support (−√y &lt; −1):",
        r"$$f_Y(y)=\dfrac{1/3}{2\sqrt{y}}=\dfrac{1}{6\sqrt{y}}",
        ("fig", fig_transform_q16),
        "Check: ∫<sub>0</sub><super>1</super> dy/(3√y) = 2/3 and ∫<sub>1</sub><super>4</super> dy/(6√y) = 1/3; "
        "total 1 (verified). (Option B integrates to 4/3, option A to 2/3 — neither is a pdf.)",
        ("note", "CDF method as cross-check: for 0 &lt; y &lt; 1, F<sub>Y</sub>(y) = P(−√y &lt; X &lt; √y) = "
                 "2√y/3; for 1 &lt; y &lt; 4, F<sub>Y</sub>(y) = P(−1 &lt; X &lt; √y) = (√y + 1)/3.", "Shortcut"),
    ],
))

# ---------------- Q17
Q.append(dict(
    qtype="NAT", marks=2, topic="Transformation: −2 ln U and chi-squared(2)", difficulty="Medium",
    text="U ∼ Uniform(0, 1) and Y = −2 ln U. The value of P(Y &gt; 3) is ______ "
         "(round off to 3 decimal places).",
    answer=f"{A17:.3f}", range=(0.222, 0.224),
    solution=[
        "<b>Concept:</b> CDF method for a monotone transformation; −ln U ∼ Exp(1).",
        "Y &gt; y ⇔ −2 ln U &gt; y ⇔ U &lt; e<super>−y/2</super>, so",
        r"$$P(Y>y)=P(U<e^{-y/2})=e^{-y/2},\qquad y>0",
        "Hence Y ∼ Exponential with rate 1/2 (mean 2) — which is exactly the χ²<sub>2</sub> distribution.",
        r"$$f_Y(y)=\dfrac{1}{2}e^{-y/2},\qquad P(Y>3)=e^{-1.5}\approx 0.223",
        ("note", "χ²<sub>2</sub> = Exp(mean 2). This is the basis of the Box–Muller method: "
                 "Z<sub>1</sub><super>2</super> + Z<sub>2</sub><super>2</super> = −2 ln U.", "Key idea"),
    ],
))

# ---------------- Q18
Q.append(dict(
    qtype="MSQ", marks=2, topic="Mixed random variable from its CDF", difficulty="Hard",
    text=["The CDF of a random variable X is plotted below: F(x) = 0 for x &lt; 0; F(x) = (1 + x)/4 for "
          "0 ≤ x &lt; 1; F(x) = 3/4 for 1 ≤ x &lt; 2; F(x) = 1 for x ≥ 2.",
          ("fig", fig_cdf_q18),
          "Which of the following is/are TRUE?"],
    options=["P(0 ≤ X &lt; 1) = 1/4", "P(X = 1) = 1/4", "P(0 &lt; X &lt; 1) = 1/4", "E[X] = 7/8"],
    answer="B, C, D",
    solution=[
        "<b>Concept:</b> P(X = a) = F(a) − F(a<super>−</super>) (jump size); P(a &lt; X &lt; b) = "
        "F(b<super>−</super>) − F(a). E[X] = ∑ (atoms) + ∫ x f(x) dx over the continuous part.",
        ("table", [["Piece", "Probability"],
                   ["Atom at x = 0", "F(0) − F(0<super>−</super>) = 1/4 − 0 = 1/4"],
                   ["Density 1/4 on (0, 1)", "1/2 − 1/4 = 1/4"],
                   ["Atom at x = 1", "3/4 − 1/2 = 1/4"],
                   ["Atom at x = 2", "1 − 3/4 = 1/4"]]),
        "<b>(A) FALSE</b>: P(0 ≤ X &lt; 1) = F(1<super>−</super>) − F(0<super>−</super>) = 1/2 − 0 = 1/2 "
        "(it includes the atom at 0).",
        "<b>(B) TRUE</b>: jump at 1 is 3/4 − 1/2 = 1/4.",
        "<b>(C) TRUE</b>: P(0 &lt; X &lt; 1) = F(1<super>−</super>) − F(0) = 1/2 − 1/4 = 1/4.",
        "<b>(D) TRUE</b>:",
        r"$$E[X]=0\cdot\dfrac{1}{4}+1\cdot\dfrac{1}{4}+2\cdot\dfrac{1}{4}+\int_0^1 x\cdot\dfrac{1}{4}\,dx",
        r"$$=\dfrac{3}{4}+\dfrac{1}{8}=\dfrac{7}{8}",
        ("note", "Whether an endpoint is included matters ONLY at jump points; on the continuous part "
                 "P(X = a) = 0.", "Trap"),
    ],
))

# ---------------- Q19
Q.append(dict(
    qtype="NAT", marks=2, topic="Normal: solving for μ and σ from quantiles", difficulty="Medium",
    text="The response time of a web service is normally distributed. 10% of requests take longer than "
         "72 ms and 25% take less than 60 ms. Use Φ(1.2816) = 0.90 and Φ(0.6745) = 0.75. The mean "
         "response time is ______ ms (round off to 2 decimal places).",
    answer=f"{MU19:.2f}", range=(64.05, 64.25),
    solution=[
        "<b>Concept:</b> each percentile gives a linear equation x = μ + zσ.",
        "P(X &gt; 72) = 0.10 ⇒ 72 is the 90th percentile; P(X &lt; 60) = 0.25 ⇒ 60 is the 25th percentile "
        "(z = −0.6745).",
        r"$$\mu+1.2816\,\sigma=72,\qquad \mu-0.6745\,\sigma=60",
        "Subtract:",
        f"$$1.9561\\,\\sigma=12\\;\\Rightarrow\\;\\sigma={SIG19:.4f}",
        f"$$\\mu=60+0.6745({SIG19:.4f})={MU19:.4f}\\approx {MU19:.2f}",
        "Check: 72 − 1.2816σ = 72 − 7.862 = 64.138 (verified).",
        ("note", "Mind the sign: the lower quartile has z = −0.6745, not +0.6745. Using +0.6745 gives a "
                 "negative σ — a red flag.", "Trap"),
    ],
))

# ---------------- Q20
Q.append(dict(
    qtype="MCQ", marks=2, topic="Poisson approximation to binomial", difficulty="Medium",
    text="A chip has a defect with probability 0.002, independently of other chips. Using the Poisson "
         "approximation, the probability that a batch of 1500 chips contains at least 2 defective chips "
         "is approximately",
    options=[f"{A20:.3f}", f"{1 - A20:.3f}", "0.950", "0.577"],
    answer="A",
    solution=[
        "<b>Concept:</b> Binomial(n, p) ≈ Poisson(np) for large n, small p.",
        r"$$\lambda=np=1500\times 0.002=3",
        r"$$P(X\geq 2)=1-P(0)-P(1)=1-e^{-3}(1+3)=1-4e^{-3}",
        f"$$=1-4(0.049787)={A20:.4f}",
        f"The exact binomial value is {A20_exact:.4f} — the approximation is excellent.",
        f"{1 - A20:.3f} is P(X ≤ 1) (the complement); 0.950 = 1 − e<super>−3</super> is P(X ≥ 1); "
        "0.577 = 1 − e<super>−3</super>(1 + 3 + 4.5) is P(X ≥ 3) (subtracting P(2) as well).",
        ("note", "'At least 2' = 1 − P(0) − P(1): forgetting either term is the standard slip.", "Trap"),
    ],
))

# ---------------- Q21
Q.append(dict(
    qtype="NAT", marks=2, topic="Correlation from a joint pdf", difficulty="Hard",
    text="(X, Y) has joint pdf f(x, y) = x + y for 0 &lt; x &lt; 1, 0 &lt; y &lt; 1. The correlation "
         "coefficient ρ(X, Y) is ______ (round off to 3 decimal places).",
    answer=f"{A21:.3f}", range=(-0.092, -0.090),
    solution=[
        "<b>Concept:</b> ρ = Cov(X, Y)/(σ<sub>X</sub>σ<sub>Y</sub>), with all moments from the joint pdf.",
        "Marginal: f<sub>X</sub>(x) = ∫<sub>0</sub><super>1</super>(x + y) dy = x + 1/2 (same for Y by symmetry).",
        r"$$E[X]=\int_0^1 x\left(x+\dfrac{1}{2}\right)dx=\dfrac{1}{3}+\dfrac{1}{4}=\dfrac{7}{12}",
        r"$$E[X^2]=\int_0^1 x^2\left(x+\dfrac{1}{2}\right)dx=\dfrac{1}{4}+\dfrac{1}{6}=\dfrac{5}{12}",
        r"$$\mathrm{Var}(X)=\dfrac{5}{12}-\dfrac{49}{144}=\dfrac{11}{144}=\mathrm{Var}(Y)",
        r"$$E[XY]=\int_0^1\int_0^1 xy(x+y)\,dx\,dy=\dfrac{1}{3}\cdot\dfrac{1}{2}+\dfrac{1}{2}\cdot\dfrac{1}{3}=\dfrac{1}{3}",
        r"$$\mathrm{Cov}(X,Y)=\dfrac{1}{3}-\dfrac{49}{144}=-\dfrac{1}{144}",
        r"$$\rho=\dfrac{-1/144}{11/144}=-\dfrac{1}{11}\approx -0.091",
        ("note", "Because σ<sub>X</sub> = σ<sub>Y</sub>, ρ = Cov/Var. The weak negative correlation arises because "
                 "the density x + y piles mass in the corners where one variable is large.", "Key idea"),
    ],
))

# ---------------- Q22
Q.append(dict(
    qtype="MSQ", marks=2, topic="Chi-squared and t relationships", difficulty="Medium",
    text="Z ∼ N(0, 1) and V ∼ χ²<sub>n</sub> are independent. Which of the following is/are TRUE?",
    options=["Z/√(V/n) has the t-distribution with n degrees of freedom",
             "E[V] = n and Var(V) = 2n",
             "Z + V has the χ²<sub>n+1</sub> distribution",
             "For n = 10, P(V &gt; 10) = 0.5"],
    answer="A, B",
    solution=[
        "<b>Concept:</b> definitions — χ²<sub>n</sub> is a sum of n squared independent N(0,1); "
        "t<sub>n</sub> = Z/√(V/n).",
        "<b>(A) TRUE</b>: this is the definition of Student's t with n degrees of freedom.",
        "<b>(B) TRUE</b>: each squared normal has mean 1 and variance 2; add n of them.",
        "<b>(C) FALSE</b>: it is Z<super>2</super> + V that is χ²<sub>n+1</sub>. Z + V can be negative, "
        "but a chi-squared variable never is.",
        f"<b>(D) FALSE</b>: χ² is right-skewed, so its median is below its mean. For n = 10 the median is "
        f"{stats.chi2(10).median():.2f} and P(V &gt; 10) = {A22_sf:.4f} &lt; 0.5.",
        ("fig", fig_chi2_q22),
        ("note", "Useful facts: median of χ²<sub>k</sub> ≈ k(1 − 2/(9k))<super>3</super>; for large k, "
                 "χ²<sub>k</sub> ≈ N(k, 2k).", "Key idea"),
    ],
))

# ---------------- Q23
Q.append(dict(
    qtype="MCQ", marks=2, topic="Exponential: minimum and maximum", difficulty="Hard",
    text="A system has two independent servers with exponentially distributed lifetimes of mean 2 hours "
         "and 3 hours. The expected time until BOTH servers have failed is",
    options=["5 hours", "1.2 hours", f"{A23:.1f} hours", "3.0 hours"],
    answer="C",
    solution=[
        "<b>Concept:</b> min of independent exponentials is exponential with summed rates; "
        "max = X + Y − min.",
        "Rates: λ<sub>1</sub> = 1/2, λ<sub>2</sub> = 1/3. The first failure time is",
        r"$$\min(X,Y)\sim\mathrm{Exp}\left(\dfrac{1}{2}+\dfrac{1}{3}=\dfrac{5}{6}\right),\quad E[\min]=\dfrac{6}{5}=1.2",
        "Since max + min = X + Y,",
        r"$$E[\max]=E[X]+E[Y]-E[\min]=2+3-1.2=3.8",
        "Direct check: E[max] = ∫<sub>0</sub><super>∞</super> [1 − (1 − e<super>−t/2</super>)(1 − e<super>−t/3</super>)] dt "
        "= 2 + 3 − 6/5 = 3.8.",
        "5 hours = E[X + Y] (a standby/backup system, not parallel); 1.2 is the first failure; 3.0 is the larger mean.",
        ("note", "E[max] always exceeds the larger individual mean (3) but is less than the sum (5).", "Shortcut"),
    ],
))

# ---------------- Q24
Q.append(dict(
    qtype="NAT", marks=2, topic="Median, mean and mode from a pdf", difficulty="Medium",
    text="X has pdf f(x) = 12x<super>2</super>(1 − x) for 0 &lt; x &lt; 1. The median of X is ______ "
         "(round off to 3 decimal places).",
    answer=f"{A24:.3f}", range=(0.612, 0.616),
    solution=[
        "<b>Concept:</b> median m solves F(m) = 1/2; mode maximises f; mean = ∫ x f(x) dx.",
        "Step 1 — CDF:",
        r"$$F(x)=\int_0^x 12t^2(1-t)\,dt=4x^3-3x^4",
        "Step 2 — solve 4m<super>3</super> − 3m<super>4</super> = 0.5 numerically (bisection / Newton):",
        ("table", [["m", "0.60", "0.61", "0.614", "0.615", "0.62"],
                   ["F(m)", f"{4*.6**3-3*.6**4:.4f}", f"{4*.61**3-3*.61**4:.4f}",
                    f"{4*.614**3-3*.614**4:.4f}", f"{4*.615**3-3*.615**4:.4f}", f"{4*.62**3-3*.62**4:.4f}"]]),
        f"$$m\\approx {A24:.4f}",
        "For comparison:",
        r"$$E[X]=\int_0^1 12x^3(1-x)\,dx=12\left(\dfrac{1}{4}-\dfrac{1}{5}\right)=\dfrac{3}{5}",
        r"$$f'(x)=24x-36x^2=0\;\Rightarrow\;\text{mode}=\dfrac{2}{3}",
        ("fig", fig_beta_q24),
        ("note", "For a left-skewed density, mean &lt; median &lt; mode (0.600 &lt; 0.614 &lt; 0.667) — the "
                 "reverse of the right-skewed order.", "Key idea"),
    ],
))

# ---------------- Q25
Q.append(dict(
    qtype="MCQ", marks=2, topic="Hierarchical model: marginal probability", difficulty="Hard",
    text="X ∼ Uniform(0, 1). Given X = x, Y has the exponential distribution with rate x (pdf "
         "x e<super>−xy</super>, y &gt; 0). The value of P(Y &gt; 1) is",
    options=["1/e", "1 − 1/e", "1/2", "e − 2"],
    answer="B",
    solution=[
        "<b>Concept:</b> continuous law of total probability: P(A) = ∫ P(A | X = x) f<sub>X</sub>(x) dx.",
        "Given X = x, P(Y &gt; 1 | X = x) = e<super>−x</super>.",
        r"$$P(Y>1)=\int_0^1 e^{-x}\cdot 1\,dx=1-e^{-1}\approx 0.632",
        "Note that 1/e = P(Y &gt; 1 | X = 1) would be the answer only if the rate were fixed at 1.",
        "For completeness, the marginal pdf of Y is",
        r"$$f_Y(y)=\int_0^1 x\,e^{-xy}\,dx=\dfrac{1-(1+y)e^{-y}}{y^2},\qquad y>0",
        "and E[Y] = E[1/X] = ∫<sub>0</sub><super>1</super> dx/x = ∞ — small rates make Y huge.",
        ("note", "Mixing over the rate gives a heavier tail than any single exponential: P(Y &gt; 1) = 0.632 "
                 "exceeds e<super>−0.5</super> = 0.607 (the exponential with the average rate 0.5).", "Key idea"),
    ],
))

# ---------------- Q26
Q.append(dict(
    qtype="MCQ", marks=2, topic="Binomial in two stages", difficulty="Medium",
    text="A storage array has 10 disks, each failing within a year with probability 0.2 independently. The "
         "array survives the year if at most 2 disks fail. A data centre runs 5 such arrays independently. "
         "The expected number of arrays that survive the year is closest to",
    options=["1.61", "1.88", "0.68", f"{A26:.2f}"],
    answer="D",
    solution=[
        "<b>Concept:</b> stage 1 — Binomial(10, 0.2) for failures in one array; stage 2 — the number of "
        "surviving arrays is Binomial(5, p<sub>s</sub>) with mean 5p<sub>s</sub>.",
        r"$$P(X=0)=0.8^{10}\approx 0.10737",
        r"$$P(X=1)=10(0.2)(0.8)^9\approx 0.26844",
        r"$$P(X=2)=\binom{10}{2}(0.2)^2(0.8)^8=45(0.04)(0.16777)\approx 0.30199",
        f"$$p_s=P(X\\leq 2)\\approx {P26:.5f},\\qquad E[\\text{{survivors}}]=5p_s\\approx {A26:.3f}",
        "1.61 = 5 × P(X ≥ 3) counts failing arrays; 1.88 uses P(X &lt; 2) (forgets X = 2); 0.68 is p<sub>s</sub> "
        "itself.",
        ("note", "Linearity: E[∑ I<sub>j</sub>] = 5 P(array survives) — no need for the full distribution "
                 "of the number of survivors.", "Shortcut"),
    ],
))

# ---------------- Q27
Q.append(dict(
    qtype="MCQ", marks=2, topic="Linear combinations of normals", difficulty="Medium",
    text="Daily demand X ∼ N(10, 9) units at store A and Y ∼ N(6, 16) units at store B, independently "
         "(second parameter = variance). Using Φ(0.8) = 0.7881, Φ(1) = 0.8413 and Φ(0.57) = 0.7157, "
         "P(X &gt; Y) is",
    options=[f"{A27:.4f}", f"{1 - A27:.4f}", "0.8413", "0.7157"],
    answer="A",
    solution=[
        "<b>Concept:</b> independent normals: X − Y ∼ N(μ<sub>X</sub> − μ<sub>Y</sub>, σ<sub>X</sub><super>2</super> "
        "+ σ<sub>Y</sub><super>2</super>) — variances ADD even for a difference.",
        r"$$D=X-Y\sim N(10-6,\;9+16)=N(4,\;25),\qquad \sigma_D=5",
        r"$$P(X>Y)=P(D>0)=P\left(Z>\dfrac{0-4}{5}\right)=P(Z>-0.8)=\Phi(0.8)=0.7881",
        ("fig", fig_norm_q27),
        "0.2119 is P(X &lt; Y); 0.8413 = Φ(1) uses σ<sub>D</sub> = 4 (√(16)); 0.7157 = Φ(4/7) adds the SDs "
        "(3 + 4 = 7) instead of the variances.",
        ("note", "Var(X − Y) = Var(X) + Var(Y) for independent X, Y — never subtract variances.", "Trap"),
    ],
))

# ---------------- Q28
Q.append(dict(
    qtype="MSQ", marks=2, topic="Distribution of max/min of uniforms (order statistics)", difficulty="Hard",
    text="X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub> are i.i.d. Uniform(0, 1). Let M = max(X<sub>1</sub>, "
         "X<sub>2</sub>, X<sub>3</sub>) and L = min(X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>). Which of "
         "the following is/are TRUE?",
    options=["The pdf of M is 3(1 − m)<super>2</super> for 0 &lt; m &lt; 1",
             "E[M] = 3/4",
             "P(L &gt; 0.5) = 1/2",
             "The median of M is 2<super>−1/3</super> ≈ 0.794"],
    answer="B, D",
    solution=[
        "<b>Concept:</b> P(M ≤ m) = P(all ≤ m) = m<super>3</super>; P(L &gt; l) = P(all &gt; l) = "
        "(1 − l)<super>3</super>.",
        "CDF and pdf of M:",
        r"$$F_M(m)=m^3,\qquad f_M(m)=3m^2,\qquad 0<m<1",
        "<b>(A) FALSE</b>: 3(1 − m)<super>2</super> is the pdf of the minimum L, not of M.",
        "<b>(B) TRUE</b>:",
        r"$$E[M]=\int_0^1 m\cdot 3m^2\,dm=\dfrac{3}{4}",
        "<b>(C) FALSE</b>: P(L &gt; 0.5) = (0.5)<super>3</super> = 1/8.",
        "<b>(D) TRUE</b>:",
        r"$$m^3=\dfrac{1}{2}\;\Rightarrow\;m=2^{-1/3}\approx 0.7937",
        ("note", "General n: E[max] = n/(n + 1), E[min] = 1/(n + 1) for n i.i.d. U(0, 1).", "Shortcut"),
    ],
))

# ---------------- Q29
Q.append(dict(
    qtype="NAT", marks=2, topic="Conditional expectation of a truncated exponential", difficulty="Hard",
    text="X ∼ Exponential with rate 1. The value of E[X | X &lt; 2] is ______ (round off to 3 decimal places).",
    answer=f"{A29:.3f}", range=(0.685, 0.689),
    solution=[
        "<b>Concept:</b> truncated density f(x)/P(X &lt; 2) on (0, 2); memorylessness does NOT apply to "
        "conditioning on X &lt; a.",
        r"$$P(X<2)=1-e^{-2}",
        r"$$\int_0^2 x e^{-x}\,dx=\left[-(1+x)e^{-x}\right]_0^2=1-3e^{-2}",
        r"$$E[X\mid X<2]=\dfrac{1-3e^{-2}}{1-e^{-2}}=1-\dfrac{2e^{-2}}{1-e^{-2}}=1-\dfrac{2}{e^2-1}",
        f"$$=1-\\dfrac{{2}}{{6.3891}}\\approx {A29:.4f}",
        "Contrast: E[X | X &gt; 2] = 2 + 1 = 3 by memorylessness. Check with total expectation: "
        "(1 − e<super>−2</super>)(0.6870) + e<super>−2</super>(3) = 0.5940 + 0.4060 = 1 = E[X] (verified).",
        ("note", "Applying 'memorylessness' backwards (e.g. answering 1 or 2 − 1) is wrong; only "
                 "the upper tail X &gt; a is a shifted copy of the original.", "Trap"),
    ],
))

# ---------------- Q30
Q.append(dict(
    qtype="MCQ", marks=2, topic="Sum of independent uniforms (convolution)", difficulty="Medium",
    text="X and Y are i.i.d. Uniform(0, 1) and Z = X + Y. The value of the pdf f<sub>Z</sub>(1.5) and of "
         "P(Z &gt; 1.5) are respectively",
    options=["0.5 and 0.25", "1 and 0.125", "0.5 and 0.125", "0.75 and 0.125"],
    answer="C",
    solution=[
        "<b>Concept:</b> convolution f<sub>Z</sub>(z) = ∫ f<sub>X</sub>(x) f<sub>Y</sub>(z − x) dx gives the "
        "triangular density on (0, 2).",
        "For 1 ≤ z ≤ 2, the integrand is 1 when max(0, z − 1) &lt; x &lt; min(1, z), i.e. z − 1 &lt; x &lt; 1:",
        r"$$f_Z(z)=\int_{z-1}^{1}1\,dx=2-z,\qquad f_Z(1.5)=0.5",
        "Tail probability = area of the small triangle:",
        r"$$P(Z>1.5)=\int_{1.5}^{2}(2-z)\,dz=\dfrac{1}{2}(0.5)(0.5)=0.125",
        ("fig", fig_tri_q30),
        "Geometric check: Z &gt; 1.5 is the corner triangle x + y &gt; 1.5 in the unit square, area "
        "(0.5)<super>2</super>/2 = 1/8.",
        ("note", "A density value (0.5) is not a probability; the area beyond 1.5 is 0.125.", "Trap"),
    ],
))


SET = {
    "title": "Topic Test: Random Variables, Distributions, PDFs & CDFs",
    "subtitle": "A topic-intensive set on discrete and continuous distributions, CDFs, transformations, "
                "joint and conditional densities.",
    "focus": "Discrete distributions (uniform, Bernoulli, binomial, Poisson and the Poisson approximation), "
             "continuous distributions (uniform, exponential and memorylessness, normal and standardisation, "
             "t and χ² properties), CDF properties and mixed CDFs, pdf from CDF, transformations of random "
             "variables, joint/marginal/conditional pdfs, moments and covariance from densities, and "
             "quantiles, medians and modes.",
    "minutes": 90,
    "questions": Q,
}
