"""Mock Test 03 - Standard GATE-Level Test I (Data-Science Contexts)."""
from fractions import Fraction as Fr
from math import comb, exp, factorial, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ------------------------------------------------------------------ computed answers
# Q1 hashing, 5 keys into 8 buckets
Q1_P = 8 * 7 * 6 * 5 * 4 / 8 ** 5
# Q3 latency data
Q3_DATA = [12, 15, 15, 18, 20, 22, 95]
Q3_MEAN = sum(Q3_DATA) / len(Q3_DATA)
Q3_MED = float(np.median(Q3_DATA))
Q3_ANS = Q3_MEAN - Q3_MED
# Q6 Poisson(3), P(N<=1)
Q6_P = exp(-3) * (1 + 3)
# Q8
Q8_P = 2 * stats.norm.sf(2)
# Q10
Q10_V = 4 * 4 + 9 - 2 * 2 * 3
# Q12 uniform(2,10)
Q12_P = (10 - 7) / (10 - 4)
# Q13 spam filter precision
Q13_P = 0.2 * 0.9 / (0.2 * 0.9 + 0.8 * 0.05)
# Q14 mislabel source
Q14_P = 0.2 * 0.10 / (0.5 * 0.02 + 0.3 * 0.04 + 0.2 * 0.10)
# Q16 law of total variance
Q16_EL = 0.25 * 20 + 0.75 * 4
Q16_VL = 0.25 * 400 + 0.75 * 16 - Q16_EL ** 2
Q16_V = Q16_EL + Q16_VL
# Q17 accuracy CI
Q17_P = 340 / 400
Q17_SE = sqrt(Q17_P * (1 - Q17_P) / 400)
Q17_M = 1.96 * Q17_SE
# Q18 A/B two-proportion z
Q18_PP = 450 / 4000
Q18_SE = sqrt(Q18_PP * (1 - Q18_PP) * (1 / 2000 + 1 / 2000))
Q18_Z = (0.125 - 0.10) / Q18_SE
# Q19 one-sample t
Q19_T = (52 - 50) / (6 / 4)
# Q20 chi-square 2x2
Q20_OBS = np.array([[30, 70], [20, 80]])
Q20_EXP = Q20_OBS.sum(1, keepdims=True) * Q20_OBS.sum(0, keepdims=True) / Q20_OBS.sum()
Q20_CHI = float(((Q20_OBS - Q20_EXP) ** 2 / Q20_EXP).sum())
# Q21
Q21_P = Fr(3, 8)
# Q23
Q23_N = (1.96 * 4 / 1) ** 2
# Q25 binomial CTR
Q25_P0 = 0.95 ** 20
Q25_P1 = 20 * 0.05 * 0.95 ** 19
Q25_P = 1 - Q25_P0 - Q25_P1
# Q26 unlabeled folds
Q26_LAB = factorial(12) // factorial(4) ** 3
Q26_N = Q26_LAB // factorial(3)
# Q28 chi-square GOF
Q28_OBS = [62, 45, 48, 45]
Q28_CHI = sum((o - 50) ** 2 / 50 for o in Q28_OBS)
# Q30 t-interval
Q30_ME = 2.064 * 10 / 5


# ------------------------------------------------------------------ figures
def fig_q3():
    fig, ax = plt.subplots(figsize=(5.6, 2.2))
    ax.boxplot(Q3_DATA, vert=False, widths=0.45, patch_artist=True,
               boxprops=dict(facecolor="#eaf2f8", color=BLUE), medianprops=dict(color=MAROON, lw=2),
               flierprops=dict(marker="o", markerfacecolor=GOLD, markeredgecolor=MAROON, markersize=8))
    ax.scatter(Q3_DATA, [0.68] * 7, color=BLUE, s=18, zorder=3)
    ax.axvline(Q3_MEAN, color=GOLD, ls="--", lw=1.6)
    ax.text(Q3_MEAN + 1, 1.32, f"mean ≈ {Q3_MEAN:.2f}", color="#8a6d00", fontsize=9)
    ax.text(Q3_MED - 2, 1.32, "median = 18", color=MAROON, fontsize=9, ha="right")
    ax.set_yticks([])
    ax.set_xlabel("latency (ms)")
    ax.set_ylim(0.5, 1.5)
    return fig


def fig_q4():
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.add_patch(Circle((0.40, 0.5), 0.32, color=BLUE, alpha=0.30))
    ax.add_patch(Circle((0.72, 0.5), 0.26, color=MAROON, alpha=0.30))
    ax.add_patch(plt.Rectangle((0.0, 0.05), 1.15, 0.9, fill=False, color="#555555"))
    ax.text(0.25, 0.5, "0.24", fontsize=11, ha="center")
    ax.text(0.59, 0.5, "0.06", fontsize=11, ha="center")
    ax.text(0.85, 0.5, "0.14", fontsize=11, ha="center")
    ax.text(1.06, 0.12, "0.56", fontsize=11, ha="center")
    ax.text(0.25, 0.86, "A (rule 1)", color=BLUE, fontsize=9)
    ax.text(0.80, 0.80, "B (rule 2)", color=MAROON, fontsize=9)
    ax.set_xlim(-0.02, 1.17)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def fig_q6():
    k = np.arange(0, 11)
    p = stats.poisson.pmf(k, 3)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.bar(k, p, color=[MAROON if i <= 1 else BLUE for i in k], alpha=0.8)
    ax.set_xticks(k)
    ax.set_xlabel("requests in one minute, N")
    ax.set_ylabel("P(N = k)")
    ax.text(5.5, 0.19, "shaded: P(N ≤ 1)", color=MAROON, fontsize=9)
    return fig


def fig_q7():
    xs = [0, 1, 2, 3]
    F = [0.2, 0.5, 0.9, 1.0]
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.hlines(0, -1, 0, color=BLUE, lw=2)
    for i, x in enumerate(xs):
        right = xs[i + 1] if i + 1 < len(xs) else 4
        ax.hlines(F[i], x, right, color=BLUE, lw=2)
        ax.plot(x, F[i], "o", color=BLUE)
        prev = F[i - 1] if i else 0
        ax.plot(x, prev, "o", mfc="white", color=BLUE)
    ax.set_xlim(-1, 4)
    ax.set_ylim(-0.05, 1.08)
    ax.set_yticks([0, 0.2, 0.5, 0.9, 1.0])
    ax.set_xlabel("x (clicks per session)")
    ax.set_ylabel("F(x)")
    ax.grid(alpha=0.25)
    return fig


def fig_q8():
    x = np.linspace(-1.8, 1.8, 400)
    pdf = stats.norm.pdf(x, 0, 0.5)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, pdf, color=BLUE)
    for m in (x > 1, x < -1):
        ax.fill_between(x[m], pdf[m], color=MAROON, alpha=0.4)
    ax.axvline(1, color="#555555", lw=0.8, ls=":")
    ax.axvline(-1, color="#555555", lw=0.8, ls=":")
    ax.set_yticks([])
    ax.set_xlabel("noise ε (σ = 0.5), shaded |ε| > 1")
    return fig


def fig_q9():
    x = np.linspace(-5, 5, 500)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.norm.pdf(x), color=BLUE, label="N(0,1)")
    ax.plot(x, stats.t.pdf(x, 3), color=MAROON, ls="--", label="t, ν = 3")
    ax.plot(x, stats.t.pdf(x, 1), color="#c99a1e", ls=":", lw=2, label="t, ν = 1")
    ax.legend(frameon=False, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("x")
    return fig


def fig_q13():
    fig, ax = plt.subplots(figsize=(5.8, 2.9))
    ax.axis("off")
    r = (0.02, 0.5)
    nodes = {"S": (0.33, 0.78), "H": (0.33, 0.22)}
    leaves = {"S+": (0.72, 0.92), "S-": (0.72, 0.64), "H+": (0.72, 0.36), "H-": (0.72, 0.08)}
    for k, (x, y) in nodes.items():
        ax.plot([r[0], x], [r[1], y], color=BLUE)
    ax.text(0.12, 0.70, "0.20", color=BLUE)
    ax.text(0.12, 0.25, "0.80", color=BLUE)
    for lk, (x, y) in leaves.items():
        px, py = nodes[lk[0]]
        ax.plot([px + 0.06, x], [py, y], color=MAROON)
    ax.text(0.34, 0.80, "spam", fontsize=9, ha="left", va="bottom")
    ax.text(0.34, 0.24, "ham", fontsize=9, ha="left", va="bottom")
    ax.text(0.50, 0.88, "0.90", color=MAROON, fontsize=9)
    ax.text(0.50, 0.60, "0.10", color=MAROON, fontsize=9)
    ax.text(0.50, 0.33, "0.05", color=MAROON, fontsize=9)
    ax.text(0.50, 0.05, "0.95", color=MAROON, fontsize=9)
    labels = {"S+": "flagged: 0.20×0.90 = 0.180", "S-": "passed: 0.020",
              "H+": "flagged: 0.80×0.05 = 0.040", "H-": "passed: 0.760"}
    for lk, (x, y) in leaves.items():
        c = MAROON if lk.endswith("+") else "#555555"
        ax.text(x + 0.01, y, labels[lk], va="center", fontsize=9, color=c)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(0, 1)
    return fig


Q15_P = np.array([[0.10, 0.20, 0.20], [0.20, 0.20, 0.10]])


def fig_q15():
    fig, ax = plt.subplots(figsize=(4.8, 2.4))
    im = ax.imshow(Q15_P, cmap="Blues", vmin=0, vmax=0.3)
    for i in range(2):
        for j in range(3):
            ax.text(j, i, f"{Q15_P[i, j]:.2f}", ha="center", va="center", fontsize=11)
    ax.set_xticks([0, 1, 2], ["Y=1", "Y=2", "Y=3"])
    ax.set_yticks([0, 1], ["X=0", "X=1"])
    ax.set_title("joint PMF p(x, y)", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    return fig


def fig_q19():
    x = np.linspace(-4, 4, 400)
    pdf = stats.t.pdf(x, 15)
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.plot(x, pdf, color=BLUE)
    m = x > 1.753
    ax.fill_between(x[m], pdf[m], color=MAROON, alpha=0.4, label="reject H₀ (α = 0.05)")
    ax.axvline(Q19_T, color=GOLD, lw=2, label=f"observed t = {Q19_T:.3f}")
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_yticks([])
    ax.set_xlabel("t (15 df); critical value 1.753")
    return fig


def fig_q20():
    x = np.linspace(0.01, 9, 400)
    pdf = stats.chi2.pdf(x, 1)
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.plot(x, pdf, color=BLUE)
    m = x > 3.841
    ax.fill_between(x[m], pdf[m], color=MAROON, alpha=0.45, label="rejection region, α = 0.05")
    ax.axvline(Q20_CHI, color=GOLD, lw=2, label=f"observed χ² = {Q20_CHI:.2f}")
    ax.set_ylim(0, 0.35)
    ax.legend(frameon=False, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("χ² with 1 df (critical value 3.841)")
    return fig


def fig_q21():
    fig, ax = plt.subplots(figsize=(3.0, 2.8))
    ax.add_patch(Polygon([[0, 0], [1, 0], [1, 1]], closed=True, color=BLUE, alpha=0.18,
                         label="support 0 < y < x < 1"))
    ax.add_patch(Polygon([[0, 0], [1, 0], [0.5, 0.5]], closed=True, color=MAROON, alpha=0.45,
                         label="x + y < 1"))
    ax.plot([0, 1], [1, 0], color=MAROON, ls="--", lw=1)
    ax.plot([0, 1], [0, 1], color=BLUE, lw=1)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    return fig


Q24_C = np.array([[4, 2, 0], [2, 9, -1.5], [0, -1.5, 1]])


def fig_q24():
    d = np.sqrt(np.diag(Q24_C))
    R = Q24_C / np.outer(d, d)
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    im = ax.imshow(R, cmap="RdBu_r", vmin=-1, vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{R[i, j]:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if abs(R[i, j]) > 0.6 else "black")
    lab = ["$X_1$", "$X_2$", "$X_3$"]
    ax.set_xticks(range(3), lab)
    ax.set_yticks(range(3), lab)
    ax.set_title("correlation matrix", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    return fig


def fig_q29():
    x = np.linspace(0, 1, 200)
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.plot(x, 2 * x, color=BLUE)
    ax.fill_between(x[x <= 1 / sqrt(2)], 2 * x[x <= 1 / sqrt(2)], color=BLUE, alpha=0.15)
    for v, lab, c in [(2 / 3, "mean 0.667", GOLD), (1 / sqrt(2), "median 0.707", MAROON),
                      (1.0, "mode 1", "#555555")]:
        ax.axvline(v, color=c, lw=1.6, ls="--")
    ax.text(0.40, 1.65, "mean 0.667", color="#8a6d00", fontsize=8.5, ha="right")
    ax.text(0.72, 1.85, "median 0.707", color=MAROON, fontsize=8.5)
    ax.text(0.99, 0.2, "mode 1", color="#555555", fontsize=8.5, ha="right")
    ax.text(0.30, 0.25, "area 0.5", color=BLUE, fontsize=8.5)
    ax.set_xlabel("confidence score x")
    ax.set_ylabel("f(x) = 2x")
    return fig


# ------------------------------------------------------------------ the set
SET = {
    "title": "Standard GATE-Level Test I (Data-Science Contexts)",
    "subtitle": "Full-syllabus paper at actual GATE DA difficulty, set in spam filters, A/B tests, "
                "server logs, sensors and model evaluation.",
    "focus": "Covers the entire Probability &amp; Statistics syllabus at exam difficulty (≈30% easy, 50% medium, "
             "20% hard): counting via hashing and cross-validation folds; axioms, independence and mutual "
             "exclusivity of filter rules; Bayes theorem for classifier precision and data-source attribution; "
             "joint/marginal/conditional PMFs and PDFs; law of total variance for bursty server traffic; "
             "summary statistics and skewness; covariance matrices of features; Bernoulli dropout, binomial "
             "click-through, Poisson/exponential request logs, uniform, normal sensor noise, t and χ² "
             "distributions; CDFs; the CLT for mini-batch means; confidence intervals for model accuracy and "
             "latency; z-test for an A/B experiment, one-sample t-test, and χ² tests of independence and "
             "goodness-of-fit.",
    "minutes": 90,
    "questions": [
        # ============================================================ 1-MARK
        dict(
            qtype="MCQ", marks=1, topic="Counting (hash collisions)", difficulty="Easy",
            text="A hash function maps each of 5 distinct keys independently and uniformly at random to one of "
                 "8 buckets. The probability that no two keys land in the same bucket is closest to",
            options=["0.410", "0.795", "0.205", "0.625"],
            answer="C",
            solution=[
                "<b>Concept:</b> P(all distinct) = (ordered selections of distinct buckets) / (all assignments).",
                "Each key has 8 choices, so the sample space has 8<super>5</super> equally likely assignments.",
                "$$|S| = 8^5 = 32768",
                "For no collision the first key may use any of 8 buckets, the second any of the remaining 7, "
                "and so on (a permutation of 5 out of 8):",
                "$$|E| = {}^{8}P_{5} = 8\\cdot 7\\cdot 6\\cdot 5\\cdot 4 = 6720",
                f"$$P(\\text{{no collision}}) = \\dfrac{{6720}}{{32768}} \\approx {Q1_P:.4f}",
                "Option (B) 0.795 is the probability of <i>at least one</i> collision — the complement.",
                ("note", "This is the birthday problem: even with more buckets than keys, collisions are "
                         "likely surprisingly early. P(collision) = 1 − ∏(1 − i/m).", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Bernoulli / binomial (dropout)", difficulty="Easy",
            text="A dense layer has 10 neurons. During training, dropout removes each neuron independently with "
                 "probability 0.2. Let K be the number of neurons that are <b>kept</b>. Then (E[K], Var(K)) is",
            options=["(2, 1.6)", "(8, 1.6)", "(8, 0.16)", "(8, 2.0)"],
            answer="B",
            solution=[
                "<b>Concept:</b> a sum of n independent Bernoulli(p) indicators is Binomial(n, p) with mean np and "
                "variance np(1 − p).",
                "Each neuron is kept with probability p = 1 − 0.2 = 0.8, independently, so K ∼ Bin(10, 0.8).",
                "$$E[K] = np = 10(0.8) = 8",
                "$$\\mathrm{Var}(K) = np(1-p) = 10(0.8)(0.2) = 1.6",
                "(A) uses the dropped count's mean (2) — the variance is the same for dropped and kept counts, but "
                "the mean is not. (C) forgets the factor n. (D) reports np·(1 − p)/0.8.",
                ("note", "Var is symmetric in p and 1 − p: the number dropped, 10 − K, has the same variance 1.6.",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Mean, median (skewed data)", difficulty="Easy",
            text=["The response latencies (in ms) of 7 API calls logged by a monitoring service are "
                  "12, 15, 15, 18, 20, 22, 95. "
                  "The value of (sample mean − sample median) is ______ (round off to 2 decimal places)."],
            answer=f"{Q3_ANS:.2f}", range=(round(Q3_ANS - 0.01, 2), round(Q3_ANS + 0.01, 2)),
            solution=[
                "<b>Concept:</b> the mean uses every value (pulled by outliers); the median is the middle order "
                "statistic (robust).",
                "$$\\bar{x} = \\dfrac{12+15+15+18+20+22+95}{7} = \\dfrac{197}{7} \\approx 28.1429",
                "With n = 7 sorted values the median is the 4th value:",
                "$$\\text{median} = x_{(4)} = 18",
                f"$$\\bar{{x}} - \\text{{median}} = 28.1429 - 18 \\approx {Q3_ANS:.2f}",
                ("fig", fig_q3),
                "The single outlier 95 drags the mean far to the right of the bulk of the data (right skew), "
                "while the median stays at 18. The mode is 15.",
                ("note", "For right-skewed data (typical for latencies) mean &gt; median &gt; mode. This is why "
                         "latency SLOs are quoted as medians/percentiles, not means.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Independence vs mutual exclusivity", difficulty="Easy",
            text="An email gateway applies two spam rules. Let A = {rule 1 fires} and B = {rule 2 fires} for a "
                 "random incoming email. Logs show P(A) = 0.3, P(B) = 0.2 and P(A ∪ B) = 0.44. "
                 "Which of the following is/are TRUE?",
            options=["A and B are independent", "A and B are mutually exclusive",
                     "P(A | B) = 0.3", "The probability that neither rule fires is 0.56"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> addition rule P(A ∪ B) = P(A) + P(B) − P(A ∩ B); independence means "
                "P(A ∩ B) = P(A)P(B).",
                "$$P(A\\cap B) = 0.3 + 0.2 - 0.44 = 0.06",
                ("fig", fig_q4),
                "<b>(A) TRUE.</b> P(A)P(B) = 0.3 × 0.2 = 0.06 = P(A ∩ B).",
                "<b>(B) FALSE.</b> Mutually exclusive needs P(A ∩ B) = 0, but it is 0.06.",
                "<b>(C) TRUE.</b> P(A | B) = 0.06/0.2 = 0.3 = P(A), as expected under independence.",
                "<b>(D) TRUE.</b> P(neither) = 1 − P(A ∪ B) = 1 − 0.44 = 0.56 "
                "(= 0.7 × 0.8, again consistent with independence).",
                ("note", "Two events with positive probability cannot be both independent and mutually "
                         "exclusive: exclusivity forces P(A ∩ B) = 0 ≠ P(A)P(B).", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Exponential (memoryless)", difficulty="Easy",
            text="The time T (in seconds) between consecutive requests to a micro-service is exponentially "
                 "distributed with mean 2 s. Given that no request has arrived in the first 3 s after the last "
                 "one, the probability that none arrives in the next 2 s is",
            options=["$$e^{-1}", "$$e^{-5/2}", "$$e^{-2}", "$$1-e^{-1}"],
            answer="A",
            solution=[
                "<b>Concept:</b> the exponential distribution is memoryless: P(T &gt; s + t | T &gt; s) = P(T &gt; t).",
                "Mean 2 s ⇒ rate λ = 1/2 per second, and P(T &gt; t) = e<super>−λt</super>.",
                "$$P(T>5\\mid T>3) = \\dfrac{P(T>5)}{P(T>3)} = \\dfrac{e^{-5/2}}{e^{-3/2}} = e^{-1}",
                "$$e^{-1} \\approx 0.368",
                "(B) e<super>−5/2</super> = P(T &gt; 5) ignores the conditioning. (C) uses λ = 1 (confusing mean "
                "with rate). (D) is the probability that a request <i>does</i> arrive.",
                ("note", "Elapsed waiting time is irrelevant for exponential waits: the clock 'restarts'.",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Poisson PMF", difficulty="Easy",
            text="A web server receives requests according to a Poisson process with an average of 3 requests per "
                 "minute. The probability that it receives at most 1 request in a given minute is ______ "
                 "(round off to 3 decimal places).",
            answer=f"{Q6_P:.3f}", range=(0.198, 0.200),
            solution=[
                "<b>Concept:</b> N ∼ Poisson(λ) has P(N = k) = e<super>−λ</super>λ<super>k</super>/k!.",
                "Here λ = 3 per minute and the interval is one minute.",
                "$$P(N\\leq 1) = P(N=0) + P(N=1) = e^{-3} + 3e^{-3} = 4e^{-3}",
                f"$$4e^{{-3}} = 4(0.049787) \\approx {Q6_P:.4f}",
                ("fig", fig_q6),
                ("note", "'At most 1' includes 0. Forgetting the k = 0 term gives 0.149.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="CDF of a discrete random variable", difficulty="Easy",
            text=["The number of ad clicks X in a user session has the CDF shown below "
                  "(F(x) = 0 for x &lt; 0; jumps occur only at x = 0, 1, 2, 3). The value of E[X] is",
                  ("fig", fig_q7)],
            options=["1.0", "2.6", "1.5", "1.4"],
            answer="D",
            solution=[
                "<b>Concept:</b> for a discrete r.v., P(X = x) equals the jump of F at x.",
                ("table", [["x", "0", "1", "2", "3"],
                           ["F(x)", "0.2", "0.5", "0.9", "1.0"],
                           ["P(X = x)", "0.2", "0.3", "0.4", "0.1"]]),
                "$$E[X] = 0(0.2) + 1(0.3) + 2(0.4) + 3(0.1) = 0 + 0.3 + 0.8 + 0.3 = 1.4",
                "(B) 2.6 = 0.2 + 0.5 + 0.9 + 1.0 adds the CDF values instead of weighting x by the PMF. "
                "(C) 1.5 is the mean if all four values were equally likely.",
                ("note", "For a non-negative integer r.v., E[X] = ∑<sub>k≥0</sub> P(X &gt; k) = "
                         "0.8 + 0.5 + 0.1 = 1.4 — a quick cross-check straight from the CDF.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Normal distribution (sensor noise)", difficulty="Easy",
            text="A temperature sensor's measurement error ε is normally distributed with mean 0 and standard "
                 "deviation 0.5 °C. The probability that the absolute error exceeds 1 °C is closest to "
                 "(Φ(1) = 0.8413, Φ(2) = 0.9772)",
            options=["0.0228", "0.0455", "0.3173", "0.0500"],
            answer="B",
            solution=[
                "<b>Concept:</b> standardise, Z = (ε − μ)/σ ∼ N(0, 1), and use symmetry.",
                "$$P(|\\varepsilon|>1) = P\\left(|Z| > \\dfrac{1}{0.5}\\right) = P(|Z|>2)",
                "$$P(|Z|>2) = 2[1-\\Phi(2)] = 2(0.0228) = 0.0456",
                ("fig", fig_q8),
                "(A) is a single tail only. (C) is P(|Z| &gt; 1) — forgetting to divide by σ. "
                "(D) confuses 2σ with the 1.96σ two-sided 5% point.",
                f"Exact: 2(1 − Φ(2)) = {Q8_P:.4f}.",
                ("note", "'Absolute error exceeds' = both tails. Always ask: one tail or two?", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="t and χ² distributions", difficulty="Medium",
            text="Which of the following statements is/are TRUE?",
            options=["The t-distribution with ν degrees of freedom has heavier tails than N(0, 1)",
                     "For ν &gt; 2, the variance of a t-distribution with ν degrees of freedom is ν/(ν − 2)",
                     "A χ² random variable with k degrees of freedom has mean 2k",
                     "If Z ∼ N(0, 1), then Z<super>2</super> has a χ² distribution with 1 degree of freedom"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> T = Z/√(V/ν) with V ∼ χ²<sub>ν</sub>; a χ²<sub>k</sub> variable is a sum of k "
                "squared independent standard normals.",
                ("fig", fig_q9),
                "<b>(A) TRUE.</b> Dividing by the random √(V/ν) inflates spread; t has polynomial (not Gaussian) "
                "tails and approaches N(0, 1) as ν → ∞.",
                "<b>(B) TRUE.</b> Var(T) = ν/(ν − 2) for ν &gt; 2 (it is infinite for ν = 2 and undefined for ν = 1).",
                "<b>(C) FALSE.</b> E[χ²<sub>k</sub>] = k; it is the <i>variance</i> that equals 2k.",
                "$$E[Z^2]=1 \\Rightarrow E\\left[\\sum_{i=1}^{k} Z_i^2\\right]=k,\\quad \\mathrm{Var}(Z^2)=E[Z^4]-1=2",
                "<b>(D) TRUE.</b> By definition χ²<sub>1</sub> is the distribution of Z<super>2</super>.",
                ("note", "Mean k, variance 2k for χ²<sub>k</sub> — a favourite swap in options.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Variance of linear combination", difficulty="Easy",
            text="Two input features X and Y of a regression dataset have Var(X) = 4, Var(Y) = 9 and "
                 "Cov(X, Y) = 3. An engineered feature is defined as U = 2X − Y. The value of Var(U) is ______ "
                 "(answer as an integer).",
            answer=str(Q10_V), range=(Q10_V, Q10_V),
            solution=[
                "<b>Concept:</b> Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab·Cov(X, Y).",
                "With a = 2, b = −1:",
                "$$\\mathrm{Var}(2X-Y) = 4(4) + 1(9) + 2(2)(-1)(3)",
                f"$$= 16 + 9 - 12 = {Q10_V}",
                ("note", "The cross-term carries the sign of ab. Forgetting it gives 25; using +12 gives 37.",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="CLT / standard error (mini-batch)", difficulty="Easy",
            text="Per-example losses on a training set have mean 2.0 and standard deviation 1.2. A mini-batch of "
                 "64 examples is drawn independently (with replacement). The standard deviation of the "
                 "mini-batch average loss is",
            options=["0.0225", "1.2", "0.15", "0.019"],
            answer="C",
            solution=[
                "<b>Concept:</b> for an average of n i.i.d. values, SD(X̄) = σ/√n (the standard error).",
                "$$\\mathrm{SD}(\\bar{X}) = \\dfrac{\\sigma}{\\sqrt{n}} = \\dfrac{1.2}{\\sqrt{64}} = \\dfrac{1.2}{8} = 0.15",
                "(A) 0.0225 is the <i>variance</i> σ²/n = 1.44/64. (D) 0.019 = 1.2/64 divides by n instead of √n. "
                "(B) ignores averaging.",
                "By the CLT the batch mean is approximately N(2.0, 0.15²) — the basis of SGD noise analysis.",
                ("note", "To halve gradient noise you must quadruple the batch size (√n law).", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Continuous uniform, conditional probability", difficulty="Easy",
            text="The processing time X (in seconds) of a batch job is uniformly distributed on [2, 10]. Given that "
                 "a job has already run for more than 4 seconds, the probability that it runs for more than "
                 "7 seconds is ______ (round off to 2 decimal places).",
            answer=f"{Q12_P:.2f}", range=(0.49, 0.51),
            solution=[
                "<b>Concept:</b> P(A | B) = P(A ∩ B)/P(B); for a uniform r.v. probabilities are length ratios.",
                "$$P(X>7\\mid X>4) = \\dfrac{P(X>7)}{P(X>4)} = \\dfrac{(10-7)/8}{(10-4)/8} = \\dfrac{3}{6} = 0.5",
                "Equivalently, given X &gt; 4, X is uniform on (4, 10], and (7, 10] is half of that interval.",
                ("note", "Unlike the exponential, the uniform is <b>not</b> memoryless: the unconditional "
                         "P(X &gt; 3) = 7/8 ≠ 0.5.", "Trap"),
            ],
        ),
        # ============================================================ 2-MARK
        dict(
            qtype="NAT", marks=2, topic="Bayes theorem (classifier precision)", difficulty="Medium",
            text="In a company's inbox, 20% of emails are spam. A spam filter flags 90% of spam emails "
                 "(recall = 0.90) and wrongly flags 5% of legitimate emails (false-positive rate = 0.05). "
                 "The precision of the filter, i.e. P(spam | flagged), is ______ (round off to 3 decimal places).",
            answer=f"{Q13_P:.3f}", range=(0.817, 0.819),
            solution=[
                "<b>Concept:</b> Bayes theorem with the law of total probability in the denominator.",
                ("fig", fig_q13),
                "Total probability of a flag:",
                "$$P(F) = P(F\\mid S)P(S) + P(F\\mid H)P(H) = 0.9(0.2) + 0.05(0.8)",
                "$$P(F) = 0.18 + 0.04 = 0.22",
                "Bayes theorem:",
                f"$$P(S\\mid F) = \\dfrac{{0.18}}{{0.22}} = \\dfrac{{9}}{{11}} \\approx {Q13_P:.4f}",
                "In confusion-matrix language, per 100 emails: TP = 18, FP = 4, so precision = 18/22.",
                ("table", [["", "Flagged", "Not flagged", "Total"],
                           ["Spam", "18", "2", "20"], ["Ham", "4", "76", "80"],
                           ["Total", "22", "78", "100"]]),
                ("note", "Precision depends on the base rate; recall and FPR do not. If spam were only 2% of "
                         "mail, precision would fall to 0.018/(0.018 + 0.049) ≈ 0.27.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Bayes theorem (data provenance)", difficulty="Medium",
            text="A training corpus is assembled from three annotation vendors A, B and C, which contribute 50%, "
                 "30% and 20% of the records respectively. Their label-error rates are 2%, 4% and 10%. "
                 "A record picked at random from the corpus is found to be mislabelled. The probability that it "
                 "came from vendor C is closest to",
            options=["0.200", "0.476", "0.286", "0.238"],
            answer="B",
            solution=[
                "<b>Concept:</b> posterior ∝ prior × likelihood (Bayes theorem over a partition).",
                "Let M = {mislabelled}. Joint probabilities:",
                ("table", [["Vendor", "Prior", "P(M | vendor)", "Prior × likelihood"],
                           ["A", "0.50", "0.02", "0.010"], ["B", "0.30", "0.04", "0.012"],
                           ["C", "0.20", "0.10", "0.020"], ["Total", "1", "", "0.042"]]),
                "$$P(M) = 0.010 + 0.012 + 0.020 = 0.042",
                f"$$P(C\\mid M) = \\dfrac{{0.020}}{{0.042}} = \\dfrac{{10}}{{21}} \\approx {Q14_P:.3f}",
                "(A) 0.200 is just the prior. (C) 0.286 = 0.012/0.042 is the posterior for B. "
                "(D) 0.238 = 0.010/0.042 is the posterior for A.",
                ("note", "A small vendor with a high error rate can dominate the error pool — C supplies 20% of "
                         "data but ≈ 48% of errors.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Joint, marginal, conditional PMF; covariance", difficulty="Medium",
            text=["A recommender logs, for each impression, the ad slot Y ∈ {1, 2, 3} and whether it was clicked, "
                  "X ∈ {0, 1}. The joint PMF is:",
                  ("table", [["", "Y = 1", "Y = 2", "Y = 3"],
                             ["X = 0", "0.10", "0.20", "0.20"],
                             ["X = 1", "0.20", "0.20", "0.10"]]),
                  "Which of the following is/are TRUE?"],
            options=["X and Y are independent", "P(Y = 2 | X = 1) = 0.4", "Cov(X, Y) = −0.1",
                     "E[X | Y = 1] = 1/3"],
            answer="B, C",
            solution=[
                "<b>Concept:</b> marginals are row/column sums; conditional = joint / marginal; "
                "Cov(X, Y) = E[XY] − E[X]E[Y].",
                ("fig", fig_q15),
                "Marginals: P(X = 0) = 0.5, P(X = 1) = 0.5; P(Y = 1) = 0.3, P(Y = 2) = 0.4, P(Y = 3) = 0.3.",
                "<b>(A) FALSE.</b> P(X = 0, Y = 1) = 0.10 but P(X = 0)P(Y = 1) = 0.5 × 0.3 = 0.15. One failing "
                "cell suffices.",
                "<b>(B) TRUE.</b>",
                "$$P(Y=2\\mid X=1) = \\dfrac{0.20}{0.50} = 0.4",
                "<b>(C) TRUE.</b>",
                "$$E[X]=0.5,\\quad E[Y]=1(0.3)+2(0.4)+3(0.3)=2.0",
                "$$E[XY] = 1(1)(0.20)+1(2)(0.20)+1(3)(0.10) = 0.9",
                "$$\\mathrm{Cov}(X,Y) = 0.9 - 0.5(2.0) = -0.1",
                "<b>(D) FALSE.</b>",
                "$$E[X\\mid Y=1] = P(X=1\\mid Y=1) = \\dfrac{0.20}{0.30} = \\dfrac{2}{3}",
                ("note", "Negative covariance: clicks are more likely in the top slot (Y = 1) and less likely in "
                         "the bottom slot — position bias.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Conditional expectation & variance (law of total variance)",
            difficulty="Hard",
            text="The number of requests N hitting a cache in a one-second window is Poisson with rate Λ, where "
                 "Λ itself is random: during peak traffic (probability 0.25) Λ = 20, otherwise "
                 "(probability 0.75) Λ = 4. The variance of N is ______ (answer as an integer).",
            answer=f"{Q16_V:.0f}", range=(Q16_V, Q16_V),
            solution=[
                "<b>Concept:</b> law of total variance, Var(N) = E[Var(N | Λ)] + Var(E[N | Λ]).",
                "For a Poisson, E[N | Λ] = Λ and Var(N | Λ) = Λ.",
                "$$E[\\Lambda] = 0.25(20) + 0.75(4) = 5 + 3 = 8",
                "$$E[\\Lambda^2] = 0.25(400) + 0.75(16) = 100 + 12 = 112",
                "$$\\mathrm{Var}(\\Lambda) = 112 - 8^2 = 48",
                "Now assemble:",
                "$$E[\\mathrm{Var}(N\\mid\\Lambda)] = E[\\Lambda] = 8",
                "$$\\mathrm{Var}(E[N\\mid\\Lambda]) = \\mathrm{Var}(\\Lambda) = 48",
                f"$$\\mathrm{{Var}}(N) = 8 + 48 = {Q16_V:.0f}",
                "Also E[N] = E[Λ] = 8, so Var(N)/E[N] = 7, far above 1 — the mixture is <i>over-dispersed</i>.",
                ("note", "Treating N as Poisson(8) would give Var = 8 — a big under-estimate. Rate heterogeneity "
                         "adds Var(Λ). This is why real request counts are often modelled as negative binomial.",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Confidence interval for a proportion", difficulty="Medium",
            text="A classifier is evaluated on 400 independent test examples and classifies 340 of them correctly. "
                 "Using the normal approximation, the 95% confidence interval for its true accuracy "
                 "(z<sub>0.025</sub> = 1.96) is closest to",
            options=["(0.832, 0.868)", "(0.804, 0.896)", "(0.815, 0.885)", "(0.780, 0.920)"],
            answer="C",
            solution=[
                "<b>Concept:</b> p̂ ± z<sub>α/2</sub>√(p̂(1 − p̂)/n) (Wald interval).",
                "$$\\hat{p} = \\dfrac{340}{400} = 0.85",
                f"$$SE = \\sqrt{{\\dfrac{{0.85(0.15)}}{{400}}}} = \\sqrt{{0.00031875}} \\approx {Q17_SE:.5f}",
                f"$$\\text{{margin}} = 1.96({Q17_SE:.5f}) \\approx {Q17_M:.4f}",
                f"$$0.85 \\pm {Q17_M:.3f} \\Rightarrow ({0.85 - Q17_M:.3f},\\ {0.85 + Q17_M:.3f})",
                "(A) uses the margin 1 × SE (≈ 68% interval). (B) uses SE = √(0.85·0.15/100)·… i.e. a wrong n. "
                "(D) uses the conservative p = 0.5 with n = 100.",
                ("note", "To halve the margin (≈ 0.035 → 0.0175) you need 4× as many test examples (1600).",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="z-test for two proportions (A/B test)", difficulty="Medium",
            text="In an A/B test of a checkout page, variant A converted 200 of 2000 visitors and variant B "
                 "converted 250 of 2000 visitors. Using the pooled two-proportion z-test of "
                 "H<sub>0</sub>: p<sub>A</sub> = p<sub>B</sub>, the value of the test statistic "
                 "z = (p̂<sub>B</sub> − p̂<sub>A</sub>)/SE is ______ (round off to 2 decimal places).",
            answer=f"{Q18_Z:.2f}", range=(2.48, 2.52),
            solution=[
                "<b>Concept:</b> under H<sub>0</sub> both groups share one p, estimated by pooling; "
                "SE = √(p̂(1 − p̂)(1/n<sub>A</sub> + 1/n<sub>B</sub>)).",
                "$$\\hat{p}_A = \\dfrac{200}{2000} = 0.100,\\quad \\hat{p}_B = \\dfrac{250}{2000} = 0.125",
                "$$\\hat{p} = \\dfrac{200+250}{2000+2000} = \\dfrac{450}{4000} = 0.1125",
                "$$SE = \\sqrt{0.1125(0.8875)\\left(\\dfrac{1}{2000}+\\dfrac{1}{2000}\\right)}",
                f"$$SE = \\sqrt{{0.0998438 \\times 0.001}} \\approx {Q18_SE:.6f}",
                f"$$z = \\dfrac{{0.125-0.100}}{{{Q18_SE:.6f}}} \\approx {Q18_Z:.3f}",
                "Since |z| ≈ 2.50 &gt; 1.96, the difference is significant at the 5% level (two-sided); the "
                "two-sided p-value is about 0.012.",
                ("note", "Pooling is used for the <i>test</i> (H<sub>0</sub> says the p's are equal). For a "
                         "<i>confidence interval</i> of p<sub>B</sub> − p<sub>A</sub> use unpooled SEs.",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="One-sample t-test", difficulty="Medium",
            text="The inference latency of a model is claimed to be 50 ms on average. On 16 random requests the "
                 "sample mean is 52 ms and the sample standard deviation is 6 ms. Latencies are assumed normal. "
                 "Consider testing H<sub>0</sub>: μ = 50 against H<sub>1</sub>: μ &gt; 50. "
                 "(t<sub>0.05,15</sub> = 1.753, t<sub>0.10,15</sub> = 1.341, t<sub>0.05,35</sub> = 1.690.) "
                 "Which of the following is/are TRUE?",
            options=["The test statistic is approximately 1.33",
                     "H<sub>0</sub> is rejected at α = 0.10",
                     "With the same sample mean and standard deviation but n = 36, H<sub>0</sub> would be rejected "
                     "at α = 0.05",
                     "The p-value of the test (n = 16) exceeds 0.05"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> t = (x̄ − μ<sub>0</sub>)/(s/√n) with n − 1 df; reject for t &gt; t<sub>α,n−1</sub>.",
                "$$t = \\dfrac{52-50}{6/\\sqrt{16}} = \\dfrac{2}{1.5} \\approx 1.333",
                ("fig", fig_q19),
                "<b>(A) TRUE.</b> t ≈ 1.333.",
                "<b>(B) FALSE.</b> 1.333 &lt; 1.341 = t<sub>0.10,15</sub>; even at the 10% level we narrowly fail "
                "to reject.",
                "<b>(C) TRUE.</b> With n = 36:",
                "$$t = \\dfrac{2}{6/\\sqrt{36}} = \\dfrac{2}{1} = 2.0 > 1.690",
                "<b>(D) TRUE.</b> Since t = 1.333 &lt; 1.753, the observed t lies outside the 5% rejection region, "
                "so p &gt; 0.05 (in fact p ≈ 0.10, just above it).",
                ("note", "The same 2 ms effect becomes 'significant' with more data: significance depends on "
                         "effect size <i>and</i> n.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="χ² test of independence", difficulty="Medium",
            text=["A survey records device type and whether the user clicked a promotional banner:",
                  ("table", [["", "Clicked", "Not clicked", "Total"],
                             ["Mobile", "30", "70", "100"], ["Desktop", "20", "80", "100"]]),
                  "At α = 0.05 (χ²<sub>0.05,1</sub> = 3.841), the Pearson χ² statistic (no continuity "
                  "correction) and the decision about independence of device and clicking are"],
            options=["χ² ≈ 2.67; reject independence", "χ² ≈ 5.33; reject independence",
                     "χ² ≈ 1.33; do not reject independence", "χ² ≈ 2.67; do not reject independence"],
            answer="D",
            solution=[
                "<b>Concept:</b> E<sub>ij</sub> = (row total × column total)/grand total; "
                "χ² = ∑(O − E)²/E with (r − 1)(c − 1) df.",
                "Column totals: clicked 50, not clicked 150; grand total 200.",
                ("table", [["Cell", "O", "E", "(O − E)²/E"],
                           ["Mobile, clicked", "30", "100·50/200 = 25", "25/25 = 1.000"],
                           ["Mobile, not", "70", "75", "25/75 = 0.333"],
                           ["Desktop, clicked", "20", "25", "1.000"],
                           ["Desktop, not", "80", "75", "0.333"]]),
                f"$$\\chi^2 = 1 + 0.333 + 1 + 0.333 \\approx {Q20_CHI:.3f}",
                "$$df = (2-1)(2-1) = 1",
                ("fig", fig_q20),
                "Since 2.667 &lt; 3.841 we do not reject H<sub>0</sub>: the data are consistent with device and "
                "clicking being independent.",
                "(B) doubles the statistic; (C) uses only one row's contributions.",
                ("note", "A 30% vs 20% click rate looks large, but with only 100 users per group it is not "
                         "statistically significant at 5%.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Joint PDF, region of integration", difficulty="Hard",
            text="Two normalised anomaly scores (X, Y) have joint density f(x, y) = c·x for 0 &lt; y &lt; x &lt; 1 "
                 "and 0 elsewhere. The value of P(X + Y &lt; 1) is ______ (round off to 3 decimal places).",
            answer=f"{float(Q21_P):.3f}", range=(0.374, 0.376),
            solution=[
                "<b>Concept:</b> find c from total probability = 1, then integrate f over the event region "
                "intersected with the support.",
                "Normalisation:",
                "$$\\int_0^1\\int_0^x c\\,x\\,dy\\,dx = c\\int_0^1 x^2\\,dx = \\dfrac{c}{3} = 1 \\Rightarrow c = 3",
                ("fig", fig_q21),
                "The event {x + y &lt; 1} within {0 &lt; y &lt; x} is the triangle with vertices (0, 0), (1, 0), "
                "(½, ½). Integrate in y first on the outside: for 0 &lt; y &lt; ½, x runs from y to 1 − y.",
                "$$P = \\int_0^{1/2}\\int_y^{1-y} 3x\\,dx\\,dy = \\int_0^{1/2} \\dfrac{3}{2}\\left[(1-y)^2 - y^2\\right]dy",
                "$$= \\dfrac{3}{2}\\int_0^{1/2} (1-2y)\\,dy = \\dfrac{3}{2}\\left[y - y^2\\right]_0^{1/2}",
                "$$= \\dfrac{3}{2}\\left(\\dfrac{1}{2}-\\dfrac{1}{4}\\right) = \\dfrac{3}{8} = 0.375",
                "(Monte Carlo check with 2×10<super>6</super> samples: ≈ 0.375.)",
                ("note", "Integrating x first from 0 to 1 would need a split at x = ½; choosing y as the outer "
                         "variable avoids the split.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Conditional PDF", difficulty="Medium",
            text="Random variables X and Y have joint density f(x, y) = 3x for 0 &lt; y &lt; x &lt; 1 (0 elsewhere). "
                 "For a fixed 0 &lt; x &lt; 1, the conditional density f<sub>Y|X</sub>(y | x) and E[Y | X = x] are",
            options=["f<sub>Y|X</sub>(y | x) = 1/x on 0 &lt; y &lt; x; E[Y | X = x] = x/2",
                     "f<sub>Y|X</sub>(y | x) = 3x on 0 &lt; y &lt; x; E[Y | X = x] = 3x/2",
                     "f<sub>Y|X</sub>(y | x) = 2y/x<super>2</super> on 0 &lt; y &lt; x; E[Y | X = x] = 2x/3",
                     "f<sub>Y|X</sub>(y | x) = 1/(1 − x) on x &lt; y &lt; 1; E[Y | X = x] = (1 + x)/2"],
            answer="A",
            solution=[
                "<b>Concept:</b> f<sub>Y|X</sub>(y | x) = f(x, y)/f<sub>X</sub>(x), where f<sub>X</sub> integrates "
                "out y over the support.",
                "$$f_X(x) = \\int_0^x 3x\\,dy = 3x^2,\\quad 0<x<1",
                "$$f_{Y\\mid X}(y\\mid x) = \\dfrac{3x}{3x^2} = \\dfrac{1}{x},\\quad 0<y<x",
                "This is Uniform(0, x), so",
                "$$E[Y\\mid X=x] = \\int_0^x y\\cdot\\dfrac{1}{x}\\,dy = \\dfrac{x}{2}",
                "(B) forgets to divide by f<sub>X</sub>(x) — it does not integrate to 1 over (0, x) unless x = 1/√3. "
                "(D) uses the wrong support (y &gt; x). (C) is not proportional to the joint density in y.",
                "Bonus: Var(Y | X = x) = x²/12, so E[Var(Y | X)] = E[X²]/12 = (3/5)/12 = 1/20.",
                ("note", "If f(x, y) does not depend on y over the slice, the conditional is uniform on that "
                         "slice.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Normal / sample size via CLT", difficulty="Medium",
            text="A sensor's readings are i.i.d. N(μ, 4<super>2</super>). The device reports the average of n "
                 "readings. The smallest n for which the reported average is within ±1 unit of μ with "
                 "probability at least 0.95 is (z<sub>0.025</sub> = 1.96)",
            options=["16", "31", "61", "62"],
            answer="D",
            solution=[
                "<b>Concept:</b> X̄ ∼ N(μ, σ²/n); require z<sub>α/2</sub>·σ/√n ≤ E.",
                "$$P(|\\bar{X}-\\mu|<1) = P\\left(|Z| < \\dfrac{1}{4/\\sqrt{n}}\\right) \\geq 0.95",
                "$$\\dfrac{\\sqrt{n}}{4} \\geq 1.96 \\Rightarrow \\sqrt{n} \\geq 7.84",
                f"$$n \\geq 7.84^2 = {Q23_N:.4f}",
                "n must be an integer, so round <b>up</b>: n = 62.",
                "Check: n = 61 gives √61/4 = 1.953 &lt; 1.96 (probability ≈ 0.949, just short).",
                "(C) rounds down; (B) forgets to square 1.96 (1.96 × 4² ≈ 31); "
                "(A) = σ², ignoring the confidence level.",
                ("note", "Sample-size answers are always rounded up, never to the nearest integer.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Covariance matrix and correlation", difficulty="Medium",
            text=["Three input features X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub> have the "
                  "covariance matrix",
                  ("table", [["Σ", "X<sub>1</sub>", "X<sub>2</sub>", "X<sub>3</sub>"], ["X<sub>1</sub>", "4", "2", "0"], ["X<sub>2</sub>", "2", "9", "−1.5"],
                             ["X<sub>3</sub>", "0", "−1.5", "1"]]),
                  "Which of the following is/are TRUE?"],
            options=["Corr(X<sub>1</sub>, X<sub>2</sub>) = 1/3",
                     "Var(X<sub>1</sub> + X<sub>2</sub>) = 17",
                     "X<sub>1</sub> and X<sub>3</sub> must be independent",
                     "Var(X<sub>2</sub> − 2X<sub>3</sub>) = 19"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> ρ<sub>ij</sub> = σ<sub>ij</sub>/(σ<sub>i</sub>σ<sub>j</sub>); "
                "Var(a<super>T</super>X) = a<super>T</super>Σa.",
                ("fig", fig_q24),
                "<b>(A) TRUE.</b>",
                "$$\\rho_{12} = \\dfrac{2}{\\sqrt{4}\\sqrt{9}} = \\dfrac{2}{6} = \\dfrac{1}{3}",
                "<b>(B) TRUE.</b>",
                "$$\\mathrm{Var}(X_1+X_2) = 4 + 9 + 2(2) = 17",
                "<b>(C) FALSE.</b> Zero covariance means zero <i>linear</i> association only; independence does not "
                "follow unless (X<sub>1</sub>, X<sub>3</sub>) is jointly normal, which is not given.",
                "<b>(D) TRUE.</b>",
                "$$\\mathrm{Var}(X_2-2X_3) = 9 + 4(1) + 2(1)(-2)(-1.5) = 9 + 4 + 6 = 19",
                ("note", "Uncorrelated ⇏ independent. Classic counter-example: X ∼ N(0, 1), Y = X² has "
                         "Cov(X, Y) = E[X³] = 0 yet Y is a function of X.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Binomial (click-through rate)", difficulty="Medium",
            text="A recommended item has a click-through rate of 5%, and clicks on different impressions are "
                 "independent. If the item is shown 20 times, the probability that it receives at least 2 clicks "
                 "is closest to",
            options=["0.358", "0.264", "0.736", "0.377"],
            answer="B",
            solution=[
                "<b>Concept:</b> X ∼ Bin(n, p); use the complement for 'at least'.",
                "X ∼ Bin(20, 0.05).",
                f"$$P(X=0) = 0.95^{{20}} \\approx {Q25_P0:.4f}",
                f"$$P(X=1) = \\binom{{20}}{{1}}(0.05)(0.95)^{{19}} \\approx {Q25_P1:.4f}",
                f"$$P(X\\geq 2) = 1 - {Q25_P0:.4f} - {Q25_P1:.4f} \\approx {Q25_P:.4f}",
                "(A) 0.358 is P(X = 0); (D) 0.377 is P(X = 1); (C) 0.736 is P(X ≤ 1).",
                f"Poisson check (λ = np = 1): 1 − 2e<super>−1</super> ≈ {1 - 2 * exp(-1):.3f} — close, as n is "
                "large and p small.",
                ("note", "'At least k' with small k: compute 1 − P(0) − … − P(k − 1).", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Counting (cross-validation folds)", difficulty="Hard",
            text="Twelve distinct training examples are to be partitioned into 3 folds of 4 examples each for "
                 "cross-validation. The folds are <b>unlabelled</b> (only the grouping matters, not which fold is "
                 "called 'first'). The number of distinct partitions is",
            options=["34650", "495", "5775", "1925"],
            answer="C",
            solution=[
                "<b>Concept:</b> multinomial coefficient for labelled groups, then divide by the number of ways to "
                "permute equal-sized unlabelled groups.",
                "Labelled folds (fold 1, fold 2, fold 3):",
                "$$\\binom{12}{4}\\binom{8}{4}\\binom{4}{4} = 495\\times 70\\times 1 = 34650 = \\dfrac{12!}{4!\\,4!\\,4!}",
                "Each unlabelled partition is counted 3! = 6 times (once per labelling of the three folds):",
                f"$$\\dfrac{{34650}}{{3!}} = \\dfrac{{34650}}{{6}} = {Q26_N}",
                "(A) is the labelled count — the trap. (B) 495 = C(12, 4) only chooses one fold. "
                "(D) 1925 = 34650/18 over-divides.",
                ("note", "Divide by k! only when the k groups have the <b>same size</b> and are unlabelled. "
                         "Folds of sizes 5, 4, 3 would need no division.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Poisson process & exponential waiting times", difficulty="Medium",
            text="Login requests arrive at an authentication server as a Poisson process with rate 4 per minute. "
                 "Which of the following is/are TRUE?",
            options=["The number of requests in a 30-second interval is Poisson with mean 2",
                     "The expected waiting time until the first request is 15 seconds",
                     "The probability of no request in a 30-second interval is e<super>−2</super>",
                     "The waiting time until the second request is exponentially distributed with mean 30 seconds"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> in a Poisson process of rate λ, N(t) ∼ Poisson(λt); inter-arrival times are "
                "i.i.d. Exp(λ); the k-th arrival time is Gamma(k, λ) (Erlang).",
                "λ = 4 per minute = 1/15 per second.",
                "<b>(A) TRUE.</b> λt = 4 × 0.5 = 2.",
                "<b>(B) TRUE.</b> E[T<sub>1</sub>] = 1/λ = 1/4 min = 15 s.",
                "<b>(C) TRUE.</b>",
                "$$P(N(0.5)=0) = P(T_1>0.5) = e^{-4(0.5)} = e^{-2} \\approx 0.135",
                "<b>(D) FALSE.</b> T<sub>2</sub> = T<sub>1</sub> + (T<sub>2</sub> − T<sub>1</sub>) is a sum of two "
                "independent Exp(λ) times: its mean is 30 s, but its distribution is Gamma(2, λ) with density "
                "λ²t e<super>−λt</super>, not exponential (its density is 0 at t = 0).",
                ("note", "Mean right, distribution wrong — MSQ options often hide the error in the word "
                         "'exponentially'.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="χ² goodness-of-fit test", difficulty="Medium",
            text="To check whether a hash function spreads keys uniformly, 200 keys are hashed into 4 buckets, "
                 "giving observed counts 62, 45, 48, 45. The Pearson χ² goodness-of-fit statistic for the "
                 "hypothesis of uniform bucket probabilities is ______ (round off to 2 decimal places).",
            answer=f"{Q28_CHI:.2f}", range=(3.95, 3.97),
            solution=[
                "<b>Concept:</b> χ² = ∑(O<sub>i</sub> − E<sub>i</sub>)²/E<sub>i</sub> with k − 1 df when no "
                "parameters are estimated.",
                "Under uniformity, E<sub>i</sub> = 200/4 = 50 for every bucket.",
                ("table", [["Bucket", "O", "E", "O − E", "(O − E)²/E"],
                           ["1", "62", "50", "12", "144/50 = 2.88"], ["2", "45", "50", "−5", "0.50"],
                           ["3", "48", "50", "−2", "0.08"], ["4", "45", "50", "−5", "0.50"]]),
                f"$$\\chi^2 = 2.88 + 0.50 + 0.08 + 0.50 = {Q28_CHI:.2f}",
                "Degrees of freedom = 4 − 1 = 3; χ²<sub>0.05,3</sub> = 7.815. Since 3.96 &lt; 7.815, uniformity "
                "is not rejected.",
                ("note", "Check: ∑(O − E) must be 0 (12 − 5 − 2 − 5 = 0) — a quick guard against arithmetic "
                         "slips.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Mean, median, mode of a continuous PDF", difficulty="Medium",
            text="The confidence score X output by a well-calibrated binary classifier on positive examples has "
                 "density f(x) = 2x for 0 ≤ x ≤ 1 (0 elsewhere). Which ordering of its mean, median and mode is "
                 "correct?",
            options=["mode &lt; median &lt; mean", "mean &lt; median &lt; mode",
                     "median &lt; mean &lt; mode", "mean = median &lt; mode"],
            answer="B",
            solution=[
                "<b>Concept:</b> mean = ∫x f(x)dx; median m solves F(m) = ½; mode = argmax f.",
                "$$\\text{mean} = \\int_0^1 x\\cdot 2x\\,dx = \\dfrac{2}{3} \\approx 0.667",
                "$$F(x) = x^2 \\Rightarrow m^2 = \\dfrac{1}{2} \\Rightarrow m = \\dfrac{1}{\\sqrt{2}} \\approx 0.707",
                "f(x) = 2x is increasing on [0, 1], so the mode is at x = 1.",
                ("fig", fig_q29),
                "Hence mean (0.667) &lt; median (0.707) &lt; mode (1): the density is left-skewed.",
                ("note", "For a left-skewed distribution the long tail is on the left and pulls the mean below the "
                         "median — the mirror image of Q.3.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Confidence interval (t-based)", difficulty="Medium",
            text="The page-load times (ms) of 25 randomly chosen sessions have sample mean 80 and sample standard "
                 "deviation 10; load times are assumed normal. (t<sub>0.025,24</sub> = 2.064, "
                 "z<sub>0.025</sub> = 1.96.) Which of the following is/are TRUE?",
            options=["The 95% t-confidence interval for the mean is approximately (75.87, 84.13)",
                     "The interval computed with 1.96 in place of 2.064 is narrower than the t-interval",
                     "There is a 95% probability that the true mean lies in the computed interval (75.87, 84.13)",
                     "With n = 100 (same sample mean and s), the width of the 95% interval using z = 1.96 is 3.92"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> with σ unknown and normal data, x̄ ± t<sub>α/2,n−1</sub>·s/√n.",
                f"$$\\dfrac{{s}}{{\\sqrt{{n}}}} = \\dfrac{{10}}{{5}} = 2,\\quad \\text{{margin}} = 2.064(2) = {Q30_ME:.3f}",
                "<b>(A) TRUE.</b> 80 ± 4.128 = (75.872, 84.128).",
                "<b>(B) TRUE.</b> 1.96 &lt; 2.064, so 80 ± 3.92 = (76.08, 83.92) is narrower (and under-covers).",
                "<b>(C) FALSE.</b> μ is fixed; the computed interval either contains it or not. '95%' describes "
                "the long-run success rate of the procedure across repeated samples.",
                "<b>(D) TRUE.</b> s/√n = 10/10 = 1, width = 2 × 1.96 × 1 = 3.92.",
                ("note", "Frequentist confidence ≠ probability about the fixed parameter. This is the single most "
                         "common conceptual trap on interval questions.", "Trap"),
            ],
        ),
    ],
}
