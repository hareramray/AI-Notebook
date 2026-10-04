"""Mock Test 04 - Standard GATE-Level Test II (Data-Science Contexts)."""
from math import comb, exp, factorial, log, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ------------------------------------------------------------------ computed answers
Q1_N = factorial(6) - factorial(5)
Q3_DATA = [4, 8, 6, 5, 7]
Q3_S = float(np.std(Q3_DATA, ddof=1))
Q5_P = exp(-2)
Q8_P = 0.4 * 0.25 + 0.6 * 0.10
Q9_MED = 100 * log(2)
Q12_V = 5 + 2 * 5
# Q13 two-stage fraud detection
Q13_ONE = 0.005 * 0.98 / (0.005 * 0.98 + 0.995 * 0.03)
Q13_NUM = 0.005 * 0.98 ** 2
Q13_DEN = Q13_NUM + 0.995 * 0.03 ** 2
Q13_P = Q13_NUM / Q13_DEN
# Q14 naive Bayes
Q14_S = 0.4 * 0.5 * 0.1
Q14_H = 0.6 * 0.1 * 0.4
Q14_P = Q14_S / (Q14_S + Q14_H)
# Q16 random batch size
Q16_V = 0.5 * (32 + 64) * 0.25 * 0.75 + 0.25 ** 2 * 16 ** 2
# Q17 two-sample z
Q17_SE = sqrt(2 ** 2 / 400 + 2.4 ** 2 / 400)
Q17_Z = (5.5 - 5.2) / Q17_SE
# Q18 paired t
Q18_D = np.array([1.2, 0.8, 1.5, 0.3, 1.0, 0.6])
Q18_DBAR = float(Q18_D.mean())
Q18_S = float(Q18_D.std(ddof=1))
Q18_T = Q18_DBAR / (Q18_S / sqrt(6))
# Q19 chi-square 2x3
Q19_O = np.array([[50, 30, 20], [30, 40, 30]])
Q19_E = Q19_O.sum(1, keepdims=True) * Q19_O.sum(0, keepdims=True) / Q19_O.sum()
Q19_CHI = float(((Q19_O - Q19_E) ** 2 / Q19_E).sum())
# Q20 sample size
Q20_N = (1.96 / 0.02) ** 2 * 0.25
# Q21 Gamma(2,1)
Q21_P = 2 * exp(-1) - 3 * exp(-2)
# Q24 regression
Q24_COV = 0.6 * 2 * 5
Q24_B = Q24_COV / 4
# Q25 birthday hashing
Q25_P = 1 - float(np.prod([(100 - i) / 100 for i in range(10)]))
# Q26 hypergeometric
Q26_P = 1 - comb(16, 5) / comb(20, 5)
Q26_ONE = 4 * comb(16, 4) / comb(20, 5)
# Q28
Q28_P = float(stats.norm.cdf(0.4))
# Q30 grouped data
Q30_MID = np.array([5, 15, 25, 35])
Q30_F = np.array([5, 15, 20, 10])
Q30_MEAN = float((Q30_MID * Q30_F).sum() / Q30_F.sum())
Q30_VAR = float((Q30_MID ** 2 * Q30_F).sum() / Q30_F.sum() - Q30_MEAN ** 2)


# ------------------------------------------------------------------ figures
def fig_q6():
    x = np.linspace(2, 18, 400)
    pdf = stats.norm.pdf(x, 10, 2)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, pdf, color=BLUE)
    m = (x > 8) & (x < 12)
    ax.fill_between(x[m], pdf[m], color=GOLD, alpha=0.55, label="P(8 < X < 12) ≈ 0.683")
    ax.axvline(10, color=MAROON, ls="--", lw=1)
    ax.set_xticks([4, 6, 8, 10, 12, 14, 16])
    ax.set_yticks([])
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    ax.set_xlabel("X ~ N(10, 4): mean 10, σ = 2")
    return fig


def fig_q9():
    x = np.linspace(0, 400, 400)
    pdf = stats.expon.pdf(x, scale=100)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, pdf, color=BLUE)
    m = x <= Q9_MED
    ax.fill_between(x[m], pdf[m], color=BLUE, alpha=0.18)
    ax.axvline(Q9_MED, color=MAROON, lw=1.6, ls="--")
    ax.axvline(100, color=GOLD, lw=1.6, ls="--")
    ax.text(Q9_MED - 4, 0.0088, "median 69.3", color=MAROON, fontsize=8.5, ha="right")
    ax.text(104, 0.0072, "mean 100", color="#8a6d00", fontsize=8.5)
    ax.text(18, 0.002, "area 0.5", color=BLUE, fontsize=8.5)
    ax.set_yticks([])
    ax.set_xlabel("time to failure (hours)")
    return fig


def fig_q11():
    x = np.linspace(-3, 3, 600)
    fig, axs = plt.subplots(1, 4, figsize=(6.6, 1.9), sharey=True)
    Fa = np.where(x >= 0, 1 - np.exp(-x ** 2), 0)
    Fb = np.where(x < -1, 0, np.where(x > 1, 1, x ** 2))
    Fc = 1 / (1 + np.exp(-x))
    Fd = x / (1 + np.abs(x))
    for ax, F, t in zip(axs, [Fa, Fb, Fc, Fd], ["(A)", "(B)", "(C)", "(D)"]):
        ax.plot(x, F, color=BLUE, lw=1.6)
        ax.axhline(0, color="#999999", lw=0.6)
        ax.axhline(1, color="#999999", lw=0.6, ls=":")
        ax.set_title(t, fontsize=9)
        ax.set_xticks([-2, 0, 2])
    axs[0].set_ylim(-1.05, 1.1)
    return fig


def fig_q13():
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    ax.axis("off")
    ax.plot([0.02, 0.30], [0.5, 0.80], color=BLUE)
    ax.plot([0.02, 0.30], [0.5, 0.20], color=BLUE)
    ax.text(0.08, 0.70, "0.005", color=BLUE, fontsize=9)
    ax.text(0.08, 0.24, "0.995", color=BLUE, fontsize=9)
    ax.text(0.31, 0.80, "fraud", fontsize=9, va="center")
    ax.text(0.31, 0.20, "legit", fontsize=9, va="center")
    for y0 in (0.80, 0.20):
        ax.plot([0.42, 0.74], [y0, y0 + 0.12], color=MAROON)
        ax.plot([0.42, 0.74], [y0, y0 - 0.10], color="#bbbbbb")
    ax.text(0.50, 0.92, "0.98²", color=MAROON, fontsize=8.5)
    ax.text(0.50, 0.32, "0.03²", color=MAROON, fontsize=8.5)
    ax.text(0.76, 0.92, "both flag: 0.005 × 0.9604 = 0.004802", va="center", fontsize=8.5, color=MAROON)
    ax.text(0.76, 0.32, "both flag: 0.995 × 0.0009 = 0.000896", va="center", fontsize=8.5, color=MAROON)
    ax.text(0.76, 0.70, "(other outcomes)", va="center", fontsize=8, color="#777777")
    ax.text(0.76, 0.10, "(other outcomes)", va="center", fontsize=8, color="#777777")
    ax.set_xlim(0, 1.5)
    ax.set_ylim(0, 1)
    return fig


def fig_q15():
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    ax.add_patch(Polygon([[0, 0], [0, 3], [3, 3]], closed=True, color=MAROON, alpha=0.35,
                         label="event X < Y"))
    xx = np.linspace(0.02, 3, 60)
    X, Y = np.meshgrid(xx, xx)
    ax.contour(X, Y, 6 * np.exp(-2 * X - 3 * Y), levels=[0.05, 0.3, 1, 2.5], colors=BLUE, linewidths=0.8)
    ax.plot([0, 3], [0, 3], color=MAROON, lw=1)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(frameon=True, fontsize=8, loc="lower right")
    ax.set_title("contours of f(x, y)", fontsize=9)
    return fig


def fig_q19():
    x = np.linspace(0.01, 14, 400)
    pdf = stats.chi2.pdf(x, 2)
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.plot(x, pdf, color=BLUE)
    m = x > 5.991
    ax.fill_between(x[m], pdf[m], color=MAROON, alpha=0.45, label="reject at α = 0.05 (> 5.991)")
    ax.axvline(9.210, color="#555555", ls=":", lw=1.2, label="α = 0.01 cut-off 9.210")
    ax.axvline(Q19_CHI, color=GOLD, lw=2, label=f"observed χ² = {Q19_CHI:.2f}")
    ax.legend(frameon=False, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("χ² with 2 df")
    return fig


def fig_q21():
    x = np.linspace(0, 6, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    F = 1 - (1 + x) * np.exp(-x)
    ax.plot(x, F, color=BLUE, label=r"$F(x)=1-(1+x)e^{-x}$")
    ax.plot(x, x * np.exp(-x), color=MAROON, ls="--", label=r"$f(x)=xe^{-x}$")
    m = (x >= 1) & (x <= 2)
    ax.fill_between(x[m], x[m] * np.exp(-x[m]), color=GOLD, alpha=0.6, label="P(1 < X ≤ 2)")
    ax.legend(frameon=False, fontsize=8, loc="center right")
    ax.set_xlabel("latency x (s)")
    ax.grid(alpha=0.25)
    return fig


def fig_q24():
    rng = np.random.default_rng(4)
    z1, z2 = rng.standard_normal((2, 120))
    x = 10 + 2 * z1
    y = 50 + 5 * (0.6 * z1 + 0.8 * z2)
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    ax.scatter(x, y, s=10, color=BLUE, alpha=0.6)
    xs = np.linspace(4, 16, 10)
    ax.plot(xs, 50 + Q24_B * (xs - 10), color=MAROON, lw=2, label="best line: slope 1.5")
    ax.plot([12], [53], "o", color=GOLD, ms=9, mec=MAROON, label="prediction at x = 12")
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("x (sessions per week)")
    ax.set_ylabel("y (spend)")
    return fig


def fig_q28():
    x = np.linspace(-14, 18, 400)
    pdf = stats.norm.pdf(x, 2, 5)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, pdf, color=BLUE)
    m = x > 0
    ax.fill_between(x[m], pdf[m], color=MAROON, alpha=0.35, label="P(D > 0)")
    ax.axvline(0, color="#555555", lw=0.8)
    ax.axvline(2, color=GOLD, lw=1.5, ls="--", label="mean 2")
    ax.legend(frameon=False, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("D = X − Y ~ N(2, 25)")
    return fig


def fig_q30():
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.bar([5, 15, 25, 35], Q30_F, width=10, color=BLUE, alpha=0.75, edgecolor="white")
    ax.axvline(22.5, color=MAROON, lw=2, label="median 22.5")
    ax.axvline(Q30_MEAN, color=GOLD, lw=2, ls="--", label=f"mean {Q30_MEAN:.0f}")
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel("session length (minutes)")
    ax.set_ylabel("frequency")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    return fig


# ------------------------------------------------------------------ the set
SET = {
    "title": "Standard GATE-Level Test II (Data-Science Contexts)",
    "subtitle": "A second full-syllabus paper at actual GATE DA difficulty: fraud detection, naive Bayes, "
                "model comparison, dropout, logging pipelines and survey analytics.",
    "focus": "Covers the whole syllabus at exam difficulty (≈30% easy, 50% medium, 20% hard): permutations with "
             "restrictions, hash-collision (birthday) probabilities and hypergeometric mini-batch sampling; "
             "mutually exclusive vs independent events; total probability, two-stage Bayes for fraud alerts and "
             "a naive Bayes spam posterior; joint/conditional PDFs (exponential pair, x + y density), random-sum "
             "variance via conditional expectation; sample and grouped-data summaries, correlation invariance "
             "and the regression slope; Bernoulli/inverted dropout, discrete uniform, Poisson, exponential, "
             "Gamma-type CDFs, normal comparisons, χ² of the sample variance; CLT for dropout counts; sample "
             "size for a CTR interval; two-sample z-test for an A/B experiment, paired t-test comparing models "
             "across datasets, and a 2 × 3 χ² test of independence.",
    "minutes": 90,
    "questions": [
        # ============================================================ 1-MARK
        dict(
            qtype="MCQ", marks=1, topic="Permutations with a restriction", difficulty="Easy",
            text="Six model variants (one baseline and five candidates) are to be deployed in six consecutive "
                 "one-hour traffic slots, one variant per slot. If the baseline must <b>not</b> occupy the first "
                 "slot, the number of possible schedules is",
            options=["600", "720", "120", "480"],
            answer="A",
            solution=[
                "<b>Concept:</b> count the complement — total arrangements minus those violating the restriction.",
                "$$\\text{total} = 6! = 720",
                "Schedules with the baseline in slot 1: the remaining 5 variants fill 5 slots in 5! ways.",
                "$$\\text{bad} = 5! = 120",
                f"$$\\text{{answer}} = 720 - 120 = {Q1_N}",
                "Direct check: slot 1 can take any of the 5 candidates, then the other 5 variants (including the "
                "baseline) fill the rest in 5! ways: 5 × 120 = 600.",
                "(D) 480 = 4 × 5! would forbid the baseline from both the first and the last slot.",
                ("note", "For 'X not in position k' restrictions, (n − 1)·(n − 1)! is a fast direct count.",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Bernoulli r.v. (inverted dropout)", difficulty="Medium",
            text="In inverted dropout, an activation x is replaced by Y = x·M/q, where M ∼ Bernoulli(q) is the "
                 "keep-mask and q is the keep probability. For x = 2 and q = 0.8, the pair (E[Y], Var(Y)) is",
            options=["(2, 0.64)", "(1.6, 0.64)", "(2, 1)", "(2.5, 1)"],
            answer="C",
            solution=[
                "<b>Concept:</b> for M ∼ Bernoulli(q): E[M] = q, Var(M) = q(1 − q); and Var(cM) = c²Var(M).",
                "Here Y = (2/0.8)M = 2.5M.",
                "$$E[Y] = 2.5\\,E[M] = 2.5(0.8) = 2",
                "$$\\mathrm{Var}(Y) = 2.5^2\\,\\mathrm{Var}(M) = 6.25(0.8)(0.2) = 6.25(0.16) = 1",
                "The 1/q scaling makes E[Y] = x, so no rescaling is needed at test time — that is the point of "
                "<i>inverted</i> dropout.",
                "(A) uses Var(2M) = 0.64 (forgets the 1/q scaling in the variance). (B) has no scaling at all. "
                "(D) reports the value of Y when kept as its mean.",
                ("note", "Dropout keeps the mean but injects variance x²(1 − q)/q — here 4(0.2)/0.8 = 1.",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Sample standard deviation", difficulty="Easy",
            text="The numbers of GPU hours used by five training runs are 4, 8, 6, 5, 7. Their sample standard "
                 "deviation (with divisor n − 1) is ______ (round off to 2 decimal places).",
            answer=f"{Q3_S:.2f}", range=(1.57, 1.59),
            solution=[
                "<b>Concept:</b> s² = ∑(x<sub>i</sub> − x̄)²/(n − 1).",
                "$$\\bar{x} = \\dfrac{4+8+6+5+7}{5} = \\dfrac{30}{5} = 6",
                ("table", [["x", "4", "8", "6", "5", "7"], ["x − x̄", "−2", "2", "0", "−1", "1"],
                           ["(x − x̄)²", "4", "4", "0", "1", "1"]]),
                "$$\\sum (x_i-\\bar{x})^2 = 10,\\quad s^2 = \\dfrac{10}{5-1} = 2.5",
                f"$$s = \\sqrt{{2.5}} \\approx {Q3_S:.4f}",
                ("note", "With divisor n you would get √2 ≈ 1.41 (the population formula). Read which divisor "
                         "the question asks for.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Mutually exclusive vs independent", difficulty="Easy",
            text="For a read request, let A = {served from the in-memory cache} and B = {served from the disk "
                 "database}. A request is served from exactly one source, and P(A) = 0.7, P(B) = 0.2. Which "
                 "statement is correct?",
            options=["A and B are independent",
                     "P(A | B) = 0, so A and B are dependent",
                     "P(A ∪ B) = 0.76",
                     "P(A ∩ B) = 0.14"],
            answer="B",
            solution=[
                "<b>Concept:</b> mutually exclusive means P(A ∩ B) = 0; independent means "
                "P(A ∩ B) = P(A)P(B).",
                "'Exactly one source' ⇒ A and B cannot both occur ⇒ P(A ∩ B) = 0.",
                "$$P(A\\mid B) = \\dfrac{P(A\\cap B)}{P(B)} = \\dfrac{0}{0.2} = 0 \\neq P(A) = 0.7",
                "So knowing B changes the probability of A: they are <b>dependent</b>. (B) is correct.",
                "(A) would need P(A ∩ B) = 0.14 ≠ 0. (C) P(A ∪ B) = 0.7 + 0.2 − 0 = 0.9, not 0.76 "
                "(0.76 is what independence would give). (D) is the independence value, not the actual one.",
                ("note", "Disjoint events with non-zero probabilities are always dependent — the strongest form "
                         "of dependence: one rules the other out.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Poisson distribution", difficulty="Easy",
            text="A log-parsing job encounters malformed lines at an average rate of 0.5 per 1000 lines, "
                 "independently, so that counts follow a Poisson distribution. For a file of 4000 lines, the "
                 "probability that no malformed line is encountered is ______ (round off to 3 decimal places).",
            answer=f"{Q5_P:.3f}", range=(0.134, 0.136),
            solution=[
                "<b>Concept:</b> scale the Poisson rate to the interval length: λ = rate × length.",
                "$$\\lambda = 0.5 \\times \\dfrac{4000}{1000} = 2",
                f"$$P(N=0) = e^{{-\\lambda}} = e^{{-2}} \\approx {Q5_P:.4f}",
                ("note", "Forgetting to rescale (using λ = 0.5) gives e<super>−0.5</super> ≈ 0.607.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Normal distribution properties", difficulty="Easy",
            text="A feature X is normally distributed with mean 10 and variance 4. Which of the following is/are "
                 "TRUE?",
            options=["P(X &lt; 10) = 0.5", "(X − 10)/2 ∼ N(0, 1)", "2X ∼ N(20, 8)",
                     "P(8 &lt; X &lt; 12) ≈ 0.683"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> X ∼ N(μ, σ²) ⇒ aX + b ∼ N(aμ + b, a²σ²); σ here is √4 = 2.",
                ("fig", fig_q6),
                "<b>(A) TRUE.</b> The normal is symmetric about its mean, so half the mass lies below 10.",
                "<b>(B) TRUE.</b> Standardising with σ = 2 (not the variance 4) gives N(0, 1).",
                "<b>(C) FALSE.</b>",
                "$$\\mathrm{Var}(2X) = 2^2(4) = 16 \\Rightarrow 2X \\sim N(20,\\ 16)",
                "<b>(D) TRUE.</b> 8 and 12 are μ ∓ σ, and P(|Z| &lt; 1) = 2Φ(1) − 1 = 0.6827.",
                ("note", "Scaling multiplies the variance by a², not a. N(μ, σ²) notation uses the variance — "
                         "divide by its square root when standardising.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Discrete uniform distribution", difficulty="Medium",
            text="A data-augmentation routine picks a random crop offset X uniformly from the integers "
                 "{0, 1, 2, …, 9}. The variance of X is",
            options=["8.33", "9.17", "6.75", "8.25"],
            answer="D",
            solution=[
                "<b>Concept:</b> for X uniform on n consecutive integers, Var(X) = (n² − 1)/12.",
                "Here n = 10:",
                "$$\\mathrm{Var}(X) = \\dfrac{10^2-1}{12} = \\dfrac{99}{12} = 8.25",
                "Direct check: E[X] = 4.5 and E[X²] = (0 + 1 + 4 + … + 81)/10 = 285/10 = 28.5, so",
                "$$\\mathrm{Var}(X) = 28.5 - 4.5^2 = 28.5 - 20.25 = 8.25",
                "(A) 100/12 uses n²/12; (C) 81/12 uses the continuous formula on [0, 9]; "
                "(B) 99/12 × 10/9 applies an n − 1 correction that does not belong to a population variance.",
                ("note", "Discrete uniform: (n² − 1)/12. Continuous uniform on [a, b]: (b − a)²/12. Do not mix "
                         "them.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Total probability", difficulty="Easy",
            text="A dataset merges records from two sources: 40% come from source S and the rest from source T. "
                 "Among S-records 25% contain missing values; among T-records 10% do. The probability that a "
                 "randomly chosen record contains missing values is ______ (round off to 2 decimal places).",
            answer=f"{Q8_P:.2f}", range=(0.16, 0.16),
            solution=[
                "<b>Concept:</b> law of total probability over the partition {S, T}.",
                "$$P(M) = P(M\\mid S)P(S) + P(M\\mid T)P(T)",
                "$$P(M) = 0.25(0.4) + 0.10(0.6) = 0.10 + 0.06 = 0.16",
                "Bonus (Bayes): P(S | M) = 0.10/0.16 = 0.625 — a record with missing values is more likely from S.",
                ("note", "Averaging the two rates (0.175) ignores the unequal source sizes.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Exponential distribution (median vs mean)", difficulty="Easy",
            text="The time to failure of a GPU node is exponentially distributed with mean 100 hours. The median "
                 "time to failure is approximately",
            options=["100 hours", "69.3 hours", "50 hours", "144.3 hours"],
            answer="B",
            solution=[
                "<b>Concept:</b> the median m solves F(m) = 1 − e<super>−λm</super> = ½, so m = ln 2/λ.",
                "$$\\lambda = \\dfrac{1}{100},\\quad 1-e^{-m/100} = \\dfrac{1}{2} \\Rightarrow m = 100\\ln 2",
                f"$$m = 100(0.6931) \\approx {Q9_MED:.1f}\\text{{ hours}}",
                ("fig", fig_q9),
                "(A) is the mean; (C) assumes symmetry; (D) = 100/ln 2 inverts the factor.",
                ("note", "The exponential is right-skewed: median ≈ 0.693 × mean. Half of all nodes fail before "
                         "70 hours even though the mean is 100.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Correlation under linear transformations", difficulty="Easy",
            text="Two features have Corr(X, Y) = 0.6. New features are defined as U = 3 − 2X and V = 5Y + 1. "
                 "Then Corr(U, V) equals",
            options=["−0.6", "0.6", "−6.0", "−0.06"],
            answer="A",
            solution=[
                "<b>Concept:</b> Corr(aX + b, cY + d) = sign(ac)·Corr(X, Y): shifts and positive scalings do not "
                "change correlation; a negative factor flips its sign.",
                "$$\\mathrm{Cov}(U,V) = (-2)(5)\\,\\mathrm{Cov}(X,Y) = -10\\,\\mathrm{Cov}(X,Y)",
                "$$\\sigma_U\\sigma_V = |{-2}|\\cdot|5|\\,\\sigma_X\\sigma_Y = 10\\,\\sigma_X\\sigma_Y",
                "$$\\mathrm{Corr}(U,V) = \\dfrac{-10\\,\\mathrm{Cov}(X,Y)}{10\\,\\sigma_X\\sigma_Y} = -0.6",
                "(C) multiplies the correlation by ac as if it were a covariance; correlation always lies in [−1, 1].",
                ("note", "Standardising features (z-scores) never changes their correlations.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Valid CDFs", difficulty="Medium",
            text=["Which of the following functions is/are valid cumulative distribution functions on the real "
                  "line? (Each is plotted below on [−3, 3].)",
                  ("fig", fig_q11)],
            options=["F(x) = 1 − e<super>−x²</super> for x ≥ 0, and F(x) = 0 for x &lt; 0",
                     "F(x) = 0 for x &lt; −1, F(x) = x<super>2</super> for −1 ≤ x ≤ 1, F(x) = 1 for x &gt; 1",
                     "F(x) = 1/(1 + e<super>−x</super>) for all x",
                     "F(x) = x/(1 + |x|) for all x"],
            answer="A, C",
            solution=[
                "<b>Concept:</b> F is a CDF iff it is non-decreasing, right-continuous, F(−∞) = 0 and F(∞) = 1.",
                "<b>(A) VALID.</b> 0 for x &lt; 0, continuous at 0 (F(0) = 0), increasing for x &gt; 0, → 1 as "
                "x → ∞. (This is the Rayleigh distribution.)",
                "<b>(B) INVALID.</b> It jumps from 0 to F(−1) = 1 at x = −1 and then <i>decreases</i> to 0 at "
                "x = 0 — a CDF can never decrease.",
                "<b>(C) VALID.</b> The logistic sigmoid is continuous, strictly increasing, with limits 0 and 1.",
                "<b>(D) INVALID.</b> It is increasing, but",
                "$$\\lim_{x\\to-\\infty}\\dfrac{x}{1+|x|} = -1 \\neq 0",
                ("note", "Check all four conditions — (D) passes monotonicity and the upper limit but fails the "
                         "lower limit. A CDF takes values only in [0, 1].", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Chi-squared distribution", difficulty="Easy",
            text="Let Z<sub>1</sub>, …, Z<sub>5</sub> be independent standard normal random variables (e.g. "
                 "standardised residuals) and W = Z<sub>1</sub><super>2</super> + … + Z<sub>5</sub><super>2</super>. "
                 "The value of E[W] + Var(W) is ______ (answer as an integer).",
            answer=str(Q12_V), range=(Q12_V, Q12_V),
            solution=[
                "<b>Concept:</b> W ∼ χ²<sub>k</sub> with k = 5; a χ²<sub>k</sub> variable has mean k and "
                "variance 2k.",
                "Derivation for one term: E[Z²] = 1 and E[Z⁴] = 3, so Var(Z²) = 3 − 1 = 2. By independence:",
                "$$E[W] = 5(1) = 5,\\quad \\mathrm{Var}(W) = 5(2) = 10",
                f"$$E[W] + \\mathrm{{Var}}(W) = 5 + 10 = {Q12_V}",
                ("note", "Sum of squared residuals of standardised errors is χ² — the basis of the χ² tests and "
                         "of the sample-variance distribution.", "Key idea"),
            ],
        ),
        # ============================================================ 2-MARK
        dict(
            qtype="NAT", marks=2, topic="Bayes theorem (two-stage screening)", difficulty="Hard",
            text="0.5% of transactions are fraudulent. Two fraud models are run independently on every "
                 "transaction; conditional on the true class, their decisions are independent. Each model flags a "
                 "fraudulent transaction with probability 0.98 and a legitimate one with probability 0.03. "
                 "Given that <b>both</b> models flag a transaction, the probability that it is fraudulent is ______ "
                 "(round off to 3 decimal places).",
            answer=f"{Q13_P:.3f}", range=(0.842, 0.844),
            solution=[
                "<b>Concept:</b> Bayes theorem; conditional independence lets the likelihoods multiply.",
                ("fig", fig_q13),
                "Likelihood of 'both flag' under each class:",
                "$$P(++\\mid F) = 0.98^2 = 0.9604,\\quad P(++\\mid L) = 0.03^2 = 0.0009",
                "Joint probabilities:",
                f"$$P(F)P(++\\mid F) = 0.005(0.9604) = {Q13_NUM:.6f}",
                "$$P(L)P(++\\mid L) = 0.995(0.0009) = 0.0008955",
                f"$$P(F\\mid ++) = \\dfrac{{0.004802}}{{0.004802+0.0008955}} \\approx {Q13_P:.4f}",
                f"For comparison, a <i>single</i> flag gives only P(F | +) = 0.0049/(0.0049 + 0.02985) ≈ "
                f"{Q13_ONE:.3f}.",
                "Equivalent sequential view: the posterior after the first flag (0.141) becomes the prior for the "
                "second flag:",
                f"$$\\dfrac{{0.141(0.98)}}{{0.141(0.98) + 0.859(0.03)}} \\approx {Q13_P:.3f}",
                ("note", "With rare positives, a single good test still gives low precision; a second, "
                         "conditionally independent test multiplies the likelihood ratio (≈ 32.7 each) and boosts "
                         "precision dramatically.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Bayes theorem (naive Bayes classifier)", difficulty="Medium",
            text="A naive Bayes spam classifier uses two binary word features. Priors: P(spam) = 0.4, "
                 "P(ham) = 0.6. Likelihoods: P(\"free\" | spam) = 0.5, P(\"free\" | ham) = 0.1, "
                 "P(\"meeting\" | spam) = 0.1, P(\"meeting\" | ham) = 0.4. Assuming the words are conditionally "
                 "independent given the class, the posterior probability that an email containing both words is "
                 "spam is closest to",
            options=["0.400", "0.545", "0.455", "0.833"],
            answer="C",
            solution=[
                "<b>Concept:</b> posterior ∝ prior × ∏ likelihoods (naive conditional independence), then "
                "normalise.",
                "Unnormalised scores:",
                f"$$\\text{{spam: }} 0.4(0.5)(0.1) = {Q14_S:.3f}",
                f"$$\\text{{ham: }} 0.6(0.1)(0.4) = {Q14_H:.3f}",
                f"$$P(\\text{{spam}}\\mid \\text{{free, meeting}}) = \\dfrac{{0.020}}{{0.020+0.024}} = \\dfrac{{5}}{{11}} "
                f"\\approx {Q14_P:.3f}",
                "So the classifier labels the email ham (0.455 &lt; 0.5).",
                "(A) is the prior. (B) is the ham posterior. (D) 0.833 = 0.020/0.024 is the ratio of the two "
                "scores, not a normalised probability.",
                ("note", "The word 'free' alone gives P(spam | free) = 0.2/0.26 ≈ 0.77; the counter-evidence of "
                         "'meeting' (likelihood ratio 1/4) flips the decision.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Joint PDF, independence, P(X &lt; Y)", difficulty="Medium",
            text="The latencies X and Y (in seconds) of two independent micro-services have joint density "
                 "f(x, y) = 6e<super>−2x−3y</super> for x &gt; 0, y &gt; 0 (0 elsewhere). Which of the following "
                 "is/are TRUE?",
            options=["X and Y are independent", "X is exponential with rate 2 (mean 0.5 s)",
                     "P(X &lt; Y) = 0.6", "E[XY] = 1/6"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> if a joint density factorises as g(x)h(y) on a product support, the variables are "
                "independent.",
                "$$6e^{-2x-3y} = (2e^{-2x})(3e^{-3y}),\\quad x>0,\\ y>0",
                "<b>(A) TRUE.</b> Factorisation on the rectangle (0, ∞) × (0, ∞).",
                "<b>(B) TRUE.</b> f<sub>X</sub>(x) = 2e<super>−2x</super>: Exp(rate 2), mean 1/2.",
                "<b>(C) FALSE.</b>",
                ("fig", fig_q15),
                "$$P(X<Y) = \\int_0^\\infty 2e^{-2x}\\,P(Y>x)\\,dx = \\int_0^\\infty 2e^{-2x}e^{-3x}\\,dx",
                "$$= \\dfrac{2}{2+3} = 0.4",
                "0.6 is P(Y &lt; X) — the faster service (rate 3) usually finishes first.",
                "<b>(D) TRUE.</b> By independence:",
                "$$E[XY] = E[X]E[Y] = \\dfrac{1}{2}\\cdot\\dfrac{1}{3} = \\dfrac{1}{6}",
                ("note", "For independent exponentials, P(X &lt; Y) = λ<sub>X</sub>/(λ<sub>X</sub> + λ<sub>Y</sub>): "
                         "the one with the larger rate wins more often.", "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Conditional expectation & variance (random sum)", difficulty="Hard",
            text="A data loader produces mini-batches whose size N is 32 or 64 with equal probability. Each example "
                 "in a batch is independently a positive with probability 0.25. Let S be the number of positives "
                 "in a batch. The value of Var(S) is ______ (answer as an integer).",
            answer=f"{Q16_V:.0f}", range=(Q16_V, Q16_V),
            solution=[
                "<b>Concept:</b> law of total variance, Var(S) = E[Var(S | N)] + Var(E[S | N]).",
                "Given N, S ∼ Bin(N, 0.25):",
                "$$E[S\\mid N] = 0.25N,\\quad \\mathrm{Var}(S\\mid N) = N(0.25)(0.75) = 0.1875N",
                "Moments of N: E[N] = 48 and, since N = 48 ± 16 with equal probability, Var(N) = 16² = 256.",
                "$$E[\\mathrm{Var}(S\\mid N)] = 0.1875\\,E[N] = 0.1875(48) = 9",
                "$$\\mathrm{Var}(E[S\\mid N]) = 0.25^2\\,\\mathrm{Var}(N) = 0.0625(256) = 16",
                f"$$\\mathrm{{Var}}(S) = 9 + 16 = {Q16_V:.0f}",
                "Monte Carlo check (2×10<super>6</super> batches): ≈ 24.98.",
                ("note", "Treating S as Bin(48, 0.25) gives only 9 — it misses the variability that comes from "
                         "the random batch size.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Two-sample z-test (A/B test of means)", difficulty="Medium",
            text="An A/B test compares mean session duration (minutes). Variant A: n = 400, mean 5.2, standard "
                 "deviation 2.0. Variant B: n = 400, mean 5.5, standard deviation 2.4. Using a large-sample z-test "
                 "(z<sub>0.025</sub> = 1.96, z<sub>0.05</sub> = 1.645), which conclusion is correct?",
            options=["z ≈ 1.92; reject H<sub>0</sub>: μ<sub>A</sub> = μ<sub>B</sub> in a two-sided test at 5%",
                     "z ≈ 1.92; do not reject H<sub>0</sub> in a two-sided test at 5%, but reject it in favour of "
                     "μ<sub>B</sub> &gt; μ<sub>A</sub> in a one-sided test at 5%",
                     "z ≈ 0.10; do not reject H<sub>0</sub> in either test",
                     "z ≈ 2.50; reject H<sub>0</sub> in both tests"],
            answer="B",
            solution=[
                "<b>Concept:</b> z = (x̄<sub>B</sub> − x̄<sub>A</sub>)/√(s<sub>A</sub>²/n<sub>A</sub> + "
                "s<sub>B</sub>²/n<sub>B</sub>).",
                "$$SE = \\sqrt{\\dfrac{2.0^2}{400}+\\dfrac{2.4^2}{400}} = \\sqrt{0.01 + 0.0144} = \\sqrt{0.0244}",
                f"$$SE \\approx {Q17_SE:.4f},\\quad z = \\dfrac{{5.5-5.2}}{{{Q17_SE:.4f}}} \\approx {Q17_Z:.3f}",
                "Two-sided at 5%: |z| = 1.92 &lt; 1.96 ⇒ do not reject.",
                "One-sided (H<sub>1</sub>: μ<sub>B</sub> &gt; μ<sub>A</sub>) at 5%: 1.92 &gt; 1.645 ⇒ reject.",
                "(C) forgets to divide the variances by n: 0.3/√(4 + 5.76) ≈ 0.10. (D) uses only group B's "
                "standard error, 0.3/√(5.76/400) = 0.3/0.12 = 2.50, ignoring the uncertainty in x̄<sub>A</sub>.",
                ("note", "The choice of one- vs two-sided alternative must be fixed <b>before</b> seeing the data; "
                         "switching after the fact inflates the false-positive rate.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Paired t-test", difficulty="Medium",
            text=["Two models are evaluated on the same 6 benchmark datasets. The accuracy differences "
                  "(model 2 − model 1, in percentage points) are:",
                  ("table", [["Dataset", "1", "2", "3", "4", "5", "6"],
                             ["Difference", "1.2", "0.8", "1.5", "0.3", "1.0", "0.6"]]),
                  "The paired t-statistic for H<sub>0</sub>: mean difference = 0 is ______ "
                  "(round off to 2 decimal places)."],
            answer=f"{Q18_T:.2f}", range=(5.12, 5.16),
            solution=[
                "<b>Concept:</b> a paired test is a one-sample t-test on the differences: "
                "t = d̄/(s<sub>d</sub>/√n), df = n − 1.",
                "$$\\bar{d} = \\dfrac{1.2+0.8+1.5+0.3+1.0+0.6}{6} = \\dfrac{5.4}{6} = 0.9",
                ("table", [["d", "1.2", "0.8", "1.5", "0.3", "1.0", "0.6"],
                           ["d − d̄", "0.3", "−0.1", "0.6", "−0.6", "0.1", "−0.3"],
                           ["(d − d̄)²", "0.09", "0.01", "0.36", "0.36", "0.01", "0.09"]]),
                f"$$s_d^2 = \\dfrac{{0.92}}{{5}} = 0.184,\\quad s_d \\approx {Q18_S:.4f}",
                f"$$t = \\dfrac{{0.9}}{{{Q18_S:.4f}/\\sqrt{{6}}}} = \\dfrac{{0.9}}{{{Q18_S / sqrt(6):.4f}}} "
                f"\\approx {Q18_T:.3f}",
                "With 5 df, t<sub>0.025,5</sub> = 2.571, so model 2 is significantly better at the 5% level.",
                ("note", "Pairing removes dataset-to-dataset difficulty variation. An unpaired two-sample test on "
                         "the raw accuracies would be far less powerful.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="χ² test of independence (2 × 3)", difficulty="Medium",
            text=["A product survey cross-tabulates user plan against the most-used feature:",
                  ("table", [["", "Feature A", "Feature B", "Feature C", "Total"],
                             ["Free", "50", "30", "20", "100"], ["Paid", "30", "40", "30", "100"],
                             ["Total", "80", "70", "50", "200"]]),
                  "A χ² test of independence is performed (χ²<sub>0.05,2</sub> = 5.991, "
                  "χ²<sub>0.01,2</sub> = 9.210). Which of the following is/are TRUE?"],
            options=["The test has 2 degrees of freedom",
                     "The expected count for (Free, Feature A) is 40",
                     "The χ² statistic is about 8.43, so independence is rejected at α = 0.05",
                     "Independence is also rejected at α = 0.01"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> E<sub>ij</sub> = R<sub>i</sub>C<sub>j</sub>/N; χ² = ∑(O − E)²/E; "
                "df = (r − 1)(c − 1).",
                "<b>(A) TRUE.</b> (2 − 1)(3 − 1) = 2.",
                "<b>(B) TRUE.</b> E = 100 × 80/200 = 40. Likewise the expected counts in each row are 40, 35, 25.",
                ("table", [["Cell", "O", "E", "(O − E)²/E"],
                           ["Free, A", "50", "40", "2.500"], ["Free, B", "30", "35", "0.714"],
                           ["Free, C", "20", "25", "1.000"], ["Paid, A", "30", "40", "2.500"],
                           ["Paid, B", "40", "35", "0.714"], ["Paid, C", "30", "25", "1.000"]]),
                f"$$\\chi^2 = 2(2.5 + 0.714 + 1.0) \\approx {Q19_CHI:.3f}",
                "<b>(C) TRUE.</b> 8.43 &gt; 5.991.",
                "<b>(D) FALSE.</b> 8.43 &lt; 9.210, so not rejected at 1% (p ≈ 0.015).",
                ("fig", fig_q19),
                ("note", "Significance depends on α: report the p-value (≈ 0.015 here) rather than only a "
                         "reject/accept verdict.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Confidence interval — sample size for a proportion", difficulty="Medium",
            text="A team wants to estimate the click-through rate of a new widget to within ±0.02 with 95% "
                 "confidence, with no prior idea of its value. Using the normal approximation and the conservative "
                 "choice for p (z<sub>0.025</sub> = 1.96), the minimum number of impressions required is",
            options=["2401", "2400", "1692", "4802"],
            answer="A",
            solution=[
                "<b>Concept:</b> margin E = z√(p(1 − p)/n) ⇒ n = z²p(1 − p)/E²; with no prior information use "
                "p = 0.5, which maximises p(1 − p).",
                "$$n \\geq \\dfrac{1.96^2(0.5)(0.5)}{0.02^2} = \\dfrac{3.8416(0.25)}{0.0004}",
                f"$$n \\geq \\dfrac{{0.9604}}{{0.0004}} = {Q20_N:.0f}",
                "The bound is met exactly at 2401 (98² × 0.25), so n = 2401. 2400 would give a margin slightly "
                "above 0.02.",
                "(C) uses z = 1.645 (a 90% interval: 1691.3 → 1692). (D) doubles n, as if E were the full width "
                "0.02 divided wrongly.",
                ("note", "p(1 − p) ≤ 1/4 — the conservative choice p = 0.5 guarantees the margin whatever the true "
                         "CTR.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="CDF and PDF of a continuous r.v.", difficulty="Medium",
            text="The response time X (in seconds) of a search service has CDF "
                 "F(x) = 1 − (1 + x)e<super>−x</super> for x ≥ 0 and F(x) = 0 for x &lt; 0. "
                 "The value of P(1 &lt; X ≤ 2) is ______ (round off to 3 decimal places).",
            answer=f"{Q21_P:.3f}", range=(0.329, 0.331),
            solution=[
                "<b>Concept:</b> P(a &lt; X ≤ b) = F(b) − F(a); the PDF is F′(x).",
                "$$F(2) = 1 - 3e^{-2},\\quad F(1) = 1 - 2e^{-1}",
                "$$P(1<X\\leq 2) = (1-3e^{-2}) - (1-2e^{-1}) = 2e^{-1} - 3e^{-2}",
                f"$$= 0.735759 - 0.406006 \\approx {Q21_P:.4f}",
                "Check via the density:",
                "$$f(x) = F'(x) = -e^{-x} + (1+x)e^{-x} = x e^{-x},\\quad x\\geq 0",
                "This is a Gamma(2, 1) density — the time until the second event of a rate-1 Poisson process.",
                ("fig", fig_q21),
                ("note", "For a continuous r.v. the endpoints don't matter: P(1 &lt; X ≤ 2) = P(1 ≤ X ≤ 2).",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="CDF of the maximum (order statistics)", difficulty="Hard",
            text="A query is fanned out to 3 replicas and the response is returned only when <b>all three</b> have "
                 "replied. The replicas' latencies are independent and uniformly distributed on (0, 1) second. "
                 "The expected response time (in seconds) is",
            options=["1/2", "2/3", "1/4", "3/4"],
            answer="D",
            solution=[
                "<b>Concept:</b> for independent X<sub>i</sub>, P(max ≤ t) = ∏ P(X<sub>i</sub> ≤ t); "
                "differentiate to get the density.",
                "Let M = max(X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>).",
                "$$F_M(t) = P(X_1\\leq t)P(X_2\\leq t)P(X_3\\leq t) = t^3,\\quad 0<t<1",
                "$$f_M(t) = 3t^2",
                "$$E[M] = \\int_0^1 t\\cdot 3t^2\\,dt = \\dfrac{3}{4}",
                "Alternatively E[M] = ∫<sub>0</sub><super>1</super>(1 − t³)dt = 1 − 1/4 = 3/4.",
                "(A) is a single replica's mean. (C) 1/4 is the expected <i>minimum</i> (first reply). "
                "(B) 2/3 is E[max] for only 2 replicas.",
                ("note", "General result: max of n i.i.d. U(0, 1) has mean n/(n + 1) — tail latency grows "
                         "with fan-out.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="CLT / normal approximation (dropout count)", difficulty="Medium",
            text="A layer has 400 neurons and dropout keeps each neuron independently with probability 0.9. Let S "
                 "be the number of kept neurons. Which of the following is/are TRUE? (Φ(2) = 0.9772.)",
            options=["E[S] = 360",
                     "The standard deviation of S is 6",
                     "Using the normal approximation without continuity correction, P(S ≥ 372) ≈ 0.023",
                     "The standard deviation of the kept fraction S/400 is 0.15"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> S ∼ Bin(n, p) ≈ N(np, np(1 − p)) for large n (CLT).",
                "<b>(A) TRUE.</b> np = 400(0.9) = 360.",
                "<b>(B) TRUE.</b>",
                "$$\\mathrm{Var}(S) = 400(0.9)(0.1) = 36,\\quad \\mathrm{SD}(S) = 6",
                "<b>(C) TRUE.</b>",
                "$$P(S\\geq 372) \\approx P\\left(Z\\geq \\dfrac{372-360}{6}\\right) = P(Z\\geq 2) = 0.0228",
                "<b>(D) FALSE.</b>",
                "$$\\mathrm{SD}(S/400) = \\dfrac{6}{400} = 0.015",
                "0.15 is off by a factor of 10 (it would be √(0.09/4)).",
                "With continuity correction one would use 371.5: z = 1.917, P ≈ 0.028 — the question fixes the "
                "convention, so (C) is decidable.",
                ("note", "Proportions shrink like 1/√n: SD(S/n) = √(p(1 − p)/n).", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Covariance, correlation, regression slope", difficulty="Medium",
            text="For users of an app, weekly sessions X and weekly spend Y have E[X] = 10, E[Y] = 50, "
                 "SD(X) = 2, SD(Y) = 5 and Corr(X, Y) = 0.6. The best linear (least-squares) prediction of Y for a "
                 "user with X = 12 is",
            options=["51.2", "55.0", "53.0", "50.48"],
            answer="C",
            solution=[
                "<b>Concept:</b> the least-squares line is Ŷ = E[Y] + β(X − E[X]) with "
                "β = Cov(X, Y)/Var(X) = ρσ<sub>Y</sub>/σ<sub>X</sub>.",
                f"$$\\mathrm{{Cov}}(X,Y) = \\rho\\,\\sigma_X\\sigma_Y = 0.6(2)(5) = {Q24_COV:.0f}",
                f"$$\\beta = \\dfrac{{6}}{{2^2}} = {Q24_B}",
                "$$\\hat{Y} = 50 + 1.5(12-10) = 53",
                ("fig", fig_q24),
                "(A) uses β = ρ = 0.6. (B) uses β = σ<sub>Y</sub>/σ<sub>X</sub> = 2.5, ignoring ρ. "
                "(D) uses Cov/Var(Y) = 0.24, the slope for regressing X on Y.",
                ("note", "Regression to the mean: X is 1 SD above average, but the prediction is only ρ = 0.6 SD "
                         "of Y above average (0.6 × 5 = 3).", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Counting (birthday problem for hashing)", difficulty="Medium",
            text="Ten user IDs are hashed independently and uniformly into a table of 100 slots. The probability "
                 "that at least two IDs collide (share a slot) is closest to",
            options=["0.628", "0.372", "0.100", "0.450"],
            answer="B",
            solution=[
                "<b>Concept:</b> P(at least one collision) = 1 − P(all distinct), with "
                "P(all distinct) = <super>m</super>P<sub>k</sub>/m<super>k</super>.",
                "$$P(\\text{all distinct}) = \\dfrac{100\\cdot 99\\cdots 91}{100^{10}} = \\prod_{i=0}^{9}\\left(1-\\dfrac{i}{100}\\right)",
                f"$$= 1(0.99)(0.98)\\cdots(0.91) \\approx {1 - Q25_P:.4f}",
                f"$$P(\\text{{collision}}) \\approx 1 - {1 - Q25_P:.4f} = {Q25_P:.4f}",
                "Approximation check: 1 − exp(−k(k − 1)/(2m)) = 1 − e<super>−0.45</super> ≈ 0.362 — close.",
                "(A) is P(no collision). (D) 0.45 = C(10, 2)/100 is the union bound — an upper bound that "
                "double-counts overlapping pairs. (C) is k/m.",
                ("note", "Expected number of colliding pairs = C(k, 2)/m = 0.45, but probability ≠ expectation; "
                         "use the complement product for the exact value.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Hypergeometric sampling (mini-batches)", difficulty="Medium",
            text="A small dataset of 20 examples contains 4 mislabelled ones. A mini-batch of 5 examples is drawn "
                 "uniformly at random <b>without replacement</b>. The probability that the batch contains at least "
                 "one mislabelled example is closest to",
            options=["0.718", "0.672", "0.282", "0.470"],
            answer="A",
            solution=[
                "<b>Concept:</b> sampling without replacement ⇒ hypergeometric counts; use the complement.",
                "$$P(\\text{none}) = \\dfrac{\\binom{16}{5}}{\\binom{20}{5}} = \\dfrac{4368}{15504} \\approx 0.2817",
                f"$$P(\\text{{at least one}}) = 1 - 0.2817 \\approx {Q26_P:.4f}",
                "(B) 0.672 = 1 − 0.8<super>5</super> treats draws as with replacement (binomial). "
                "(C) is P(none). (D) is P(exactly one):",
                f"$$P(\\text{{exactly one}}) = \\dfrac{{\\binom{{4}}{{1}}\\binom{{16}}{{4}}}}{{\\binom{{20}}{{5}}}} "
                f"= \\dfrac{{7280}}{{15504}} \\approx {Q26_ONE:.3f}",
                ("note", "Without replacement, each clean draw makes the next draw slightly more likely to be "
                         "mislabelled, so P(none) is smaller than the binomial 0.328.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Sampling distribution of S² (χ²)", difficulty="Hard",
            text="Ten readings X<sub>1</sub>, …, X<sub>10</sub> are taken from a sensor whose noise is "
                 "N(μ, σ²) with σ² = 4. Let X̄ and S² be the sample mean and sample variance (divisor n − 1). "
                 "Which of the following is/are TRUE?",
            options=["9S²/4 follows a χ² distribution with 9 degrees of freedom",
                     "E[S²] = 4",
                     "Var(S²) = 3.2",
                     "X̄ and S² are dependent random variables"],
            answer="A, B",
            solution=[
                "<b>Concept:</b> for normal samples, (n − 1)S²/σ² ∼ χ²<sub>n−1</sub>, and X̄ is independent of S².",
                "<b>(A) TRUE.</b> (n − 1)S²/σ² = 9S²/4 ∼ χ²<sub>9</sub> (one df is lost by estimating μ with X̄).",
                "<b>(B) TRUE.</b> E[χ²<sub>9</sub>] = 9 ⇒ E[9S²/4] = 9 ⇒ E[S²] = 4: S² is unbiased.",
                "<b>(C) FALSE.</b> Var(χ²<sub>9</sub>) = 18, so",
                "$$\\mathrm{Var}(S^2) = \\left(\\dfrac{4}{9}\\right)^2(18) = \\dfrac{2\\sigma^4}{n-1} = \\dfrac{32}{9} \\approx 3.56",
                "3.2 = 2σ⁴/n uses n instead of n − 1.",
                "<b>(D) FALSE.</b> For normal data X̄ and S² are independent (a characterising property of the "
                "normal distribution).",
                ("note", "Remember both facts together: χ²<sub>n−1</sub> for the scaled variance and independence "
                         "of X̄ and S² — together they give the t-statistic its t<sub>n−1</sub> distribution.",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Normal distribution (difference of normals)", difficulty="Medium",
            text="Two temperature sensors give independent readings X ∼ N(20, 9) and Y ∼ N(18, 16) "
                 "(second parameter = variance). The probability that sensor X reads higher than sensor Y is "
                 "______ (round off to 3 decimal places). (Φ(0.4) = 0.6554.)",
            answer=f"{Q28_P:.3f}", range=(0.654, 0.657),
            solution=[
                "<b>Concept:</b> a difference of independent normals is normal; variances add.",
                "$$D = X - Y \\sim N(20-18,\\ 9+16) = N(2,\\ 25)",
                "$$P(X>Y) = P(D>0) = P\\left(Z > \\dfrac{0-2}{5}\\right) = P(Z>-0.4)",
                f"$$= \\Phi(0.4) \\approx {Q28_P:.4f}",
                ("fig", fig_q28),
                ("note", "Var(X − Y) = Var(X) + Var(Y) for independent variables — never subtract variances "
                         "(9 − 16 would be negative!).", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Conditional PDF and conditional expectation", difficulty="Hard",
            text="Two normalised scores (X, Y) have joint density f(x, y) = x + y on the unit square "
                 "0 &lt; x &lt; 1, 0 &lt; y &lt; 1 (0 elsewhere). The value of E[Y | X = 0.5] is",
            options=["1/2", "2/3", "5/12", "7/12"],
            answer="D",
            solution=[
                "<b>Concept:</b> f<sub>Y|X</sub>(y | x) = f(x, y)/f<sub>X</sub>(x); then integrate y against it.",
                "$$f_X(x) = \\int_0^1 (x+y)\\,dy = x + \\dfrac{1}{2}",
                "$$f_{Y\\mid X}(y\\mid x) = \\dfrac{x+y}{x+1/2},\\quad 0<y<1",
                "At x = 0.5 the denominator is 1, so f<sub>Y|X</sub>(y | 0.5) = 0.5 + y.",
                "$$E[Y\\mid X=0.5] = \\int_0^1 y(0.5+y)\\,dy = \\dfrac{0.5}{2} + \\dfrac{1}{3} = \\dfrac{1}{4}+\\dfrac{1}{3} = \\dfrac{7}{12}",
                "General formula:",
                "$$E[Y\\mid X=x] = \\dfrac{x/2 + 1/3}{x + 1/2}",
                "(A) assumes Y is uniform given X. (B) 2/3 is E[Y | X = 0] = (1/3)/(1/2). (C) is 1 − 7/12.",
                "Monte Carlo check (rejection sampling, X near 0.5): ≈ 0.582.",
                ("note", "The conditional mean decreases from 2/3 (x = 0) to 5/9 (x = 1): X and Y are slightly "
                         "negatively correlated under this density.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Grouped data: mean, median, mode, SD", difficulty="Medium",
            text=["Session lengths (minutes) of 50 users are summarised below.",
                  ("table", [["Class (min)", "0–10", "10–20", "20–30", "30–40"],
                             ["Frequency", "5", "15", "20", "10"]]),
                  "Using class mid-points for the mean and SD (divisor N) and linear interpolation within the "
                  "median class for the median, which of the following is/are TRUE?"],
            options=["The median is 22.5 minutes", "The mean is 22 minutes", "The modal class is 20–30",
                     "The standard deviation exceeds 10 minutes"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> grouped median = L + ((N/2 − CF)/f)·h; grouped mean = ∑f·m/N.",
                ("fig", fig_q30),
                "<b>(A) TRUE.</b> N/2 = 25. Cumulative frequencies: 5, 20, 40, 50 ⇒ the median class is 20–30 "
                "(L = 20, CF = 20, f = 20, h = 10).",
                "$$\\text{median} = 20 + \\dfrac{25-20}{20}(10) = 22.5",
                "<b>(B) TRUE.</b>",
                "$$\\bar{x} = \\dfrac{5(5)+15(15)+20(25)+10(35)}{50} = \\dfrac{1100}{50} = 22",
                "<b>(C) TRUE.</b> 20–30 has the highest frequency (20).",
                "<b>(D) FALSE.</b>",
                "$$\\dfrac{\\sum f m^2}{N} = \\dfrac{125+3375+12500+12250}{50} = 565",
                f"$$\\sigma^2 = 565 - 22^2 = {Q30_VAR:.0f},\\quad \\sigma = 9",
                ("note", "Here the mean (22) is slightly below the median (22.5): the long tail is on the left "
                         "(few short sessions), a mild left skew.", "Key idea"),
            ],
        ),
    ],
}
