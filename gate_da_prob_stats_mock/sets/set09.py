"""Mock Test 09 — Advanced Full-Syllabus Test I (hardest GATE DA level).

All numeric answers are computed below so the key cannot drift from the maths.
"""
import math
from fractions import Fraction as Fr
from math import comb, factorial

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize, stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ------------------------------------------------------------------ computed keys
# Q1 STATISTICS arrangements with the three S's not all together
_q1_total = factorial(10) // (factorial(3) * factorial(3) * factorial(2))
_q1_block = factorial(8) // (factorial(3) * factorial(2))
_q1 = _q1_total - _q1_block                                    # 47040
# Q3 series system survival
_q3 = math.exp(-0.5 * 3)                                       # 0.2231
# Q4 median of three U(0,1) <= 1/4
_q4 = Fr(3) * Fr(1, 4) ** 2 * Fr(3, 4) + Fr(1, 4) ** 3          # 5/32
# Q6 Poisson thinning
_q6 = math.exp(-12 * (20 / 60) * 0.25)                         # e^-1
# Q7 SD after removing a value equal to the mean
_q7 = math.sqrt(10 * 16 / 9)
# Q10 random number of coins
_q10 = 3.5 / 4 + (35 / 12) / 4                                 # 1.6042
# Q12
_q12 = stats.norm.sf(0.5)
# Q13 Bayes + binomial
_lb, _lf = comb(5, 4) * 0.8 ** 4 * 0.2, comb(5, 4) * 0.5 ** 5
_q13_post = (1 / 3) * _lb / ((1 / 3) * _lb + (2 / 3) * _lf)
_q13 = _q13_post * 0.8 + (1 - _q13_post) * 0.5
# Q16 meeting problem with unequal waits
_q16 = 1 - (50 ** 2 / 2 + 40 ** 2 / 2) / 3600
# Q17 sample size
_q17 = math.ceil(1.96 ** 2 * 0.2 * 0.8 / 0.03 ** 2)
# Q18 Hardy-Weinberg chi-squared
_o18 = np.array([50, 30, 20])
_p18 = (2 * 50 + 30) / 200
_e18 = 100 * np.array([_p18 ** 2, 2 * _p18 * (1 - _p18), (1 - _p18) ** 2])
_c18 = (_o18 - _e18) ** 2 / _e18
_q18 = _c18.sum()
# Q19 empty boxes
_pe = 0.8 ** 10
_q19_E = 5 * _pe
_q19 = 5 * _pe + 20 * 0.6 ** 10 - 25 * _pe ** 2
_q19_naive = 5 * _pe * (1 - _pe)
# Q20 normal mixture
_q20 = 0.6 * stats.norm.sf(2) + 0.4 * 0.5
# Q21 paired t
_d21 = np.array([3, 5, -1, 4, 6, 2])
_s21 = _d21.std(ddof=1)
_t21 = _d21.mean() / (_s21 / math.sqrt(6))
# Q22 power
_c22 = 100 + 1.645 * 2.5
_q22 = stats.norm.sf((_c22 - 106) / 2.5)
# Q23
_q23 = comb(8, 3) * (3 / 8) ** 3 * (5 / 8) ** 5
# Q25 naive Bayes
_num25 = 0.3 * 0.4 * 0.98
_den25 = _num25 + 0.7 * 0.05 * 0.80
_q25 = _num25 / _den25
# Q27 Gamma(2,1) median
_q27_med = optimize.brentq(lambda m: 1 - (1 + m) * math.exp(-m) - 0.5, 0.1, 5)
# Q28 CI width
_s28 = math.sqrt((231540 - 16 * 120 ** 2) / 15)
_q28 = 2 * 2.131 * _s28 / 4
# Q30 two pairs
_q30_fav = comb(13, 2) * comb(4, 2) ** 2 * 11 * 4
_q30 = _q30_fav / comb(52, 5)


# ------------------------------------------------------------------ figures
def _tree(ax, root, first, second):
    """first: list of (label, prob_text); second: list of lists of (label, prob_text)."""
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.text(0.3, 5, root, ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", fc="white", ec=BLUE))
    n1 = len(first)
    ys = np.linspace(8.5, 1.5, n1)
    for (lab, pr), y, kids in zip(first, ys, second):
        ax.plot([0.8, 3.6], [5, y], color=BLUE, lw=1.2)
        ax.text(2.0, (5 + y) / 2 + 0.35, pr, fontsize=8, color=MAROON, ha="center")
        ax.text(4.3, y, lab, ha="center", va="center", fontsize=8.5,
                bbox=dict(boxstyle="round", fc="#eaf2f8", ec=BLUE))
        k = len(kids)
        dy = 1.1 if k > 1 else 0
        for j, (kl, kp) in enumerate(kids):
            yy = y + dy * (1 - 2 * j / max(k - 1, 1)) if k > 1 else y
            ax.plot([5.1, 7.2], [y, yy], color=MAROON, lw=1)
            ax.text(6.1, (y + yy) / 2 + 0.3, kp, fontsize=7.5, color=MAROON, ha="center")
            ax.text(7.4, yy, kl, va="center", fontsize=8)


def fig_q4():
    x = np.linspace(0, 1, 300)
    f = 6 * x * (1 - x)
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.plot(x, f, color=BLUE, lw=2, label="pdf of median: 6x(1−x)")
    m = x <= 0.25
    ax.fill_between(x[m], f[m], color=MAROON, alpha=0.35, label="P(M ≤ 1/4) = 5/32")
    ax.axvline(0.25, color=GOLD, ls="--")
    ax.set_xlabel("m")
    ax.set_ylabel("density")
    ax.legend(fontsize=8, frameon=False)
    return fig


def fig_q8():
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.plot([-1, 0], [0, 0], color=BLUE, lw=2)
    ax.plot([0, 1], [0.25, 0.5], color=BLUE, lw=2)
    ax.plot([1, 2], [1, 1], color=BLUE, lw=2)
    ax.plot([0, 1], [0.25, 1], "o", color=BLUE)
    ax.plot([0, 1], [0, 0.5], "o", mfc="white", color=BLUE)
    ax.plot([0, 0], [0, 0.25], ":", color="gray")
    ax.plot([1, 1], [0.5, 1], ":", color="gray")
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 0.25, 0.5, 1])
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    ax.set_xlim(-1, 2)
    ax.set_ylim(-0.05, 1.1)
    return fig


def fig_q12():
    x = np.linspace(4, 20, 400)
    f = stats.norm.pdf(x, 12, 2)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, f, color=BLUE)
    for lo, hi, c in [(4, 10, MAROON), (16, 20, MAROON), (13, 20, GOLD)]:
        m = (x >= lo) & (x <= hi)
        ax.fill_between(x[m], f[m], color=c, alpha=0.35 if c == MAROON else 0.45)
    ax.annotate("0.1587", xy=(9, 0.03), xytext=(5, 0.12), arrowprops=dict(arrowstyle="->"))
    ax.annotate("0.0228", xy=(16.6, 0.006), xytext=(17, 0.1), arrowprops=dict(arrowstyle="->"))
    ax.annotate("P(X>13)", xy=(14, 0.08), xytext=(15, 0.17), arrowprops=dict(arrowstyle="->"))
    ax.set_yticks([])
    ax.set_xticks([10, 12, 13, 16])
    ax.set_xlabel("x   (μ = 12, σ = 2)")
    return fig


def fig_q13():
    fig, ax = plt.subplots(figsize=(6, 3.0))
    _tree(ax, "pick coin",
          [("Biased", "1/3"), ("Fair", "2/3")],
          [[("4 H in 5:  0.4096", "5(0.8)⁴(0.2)")], [("4 H in 5:  0.15625", "5(0.5)⁵")]])
    return fig


def fig_q15():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    ax.fill([0, 0, 1], [0, 1, 1], color=BLUE, alpha=0.18, label="support 0<x<y<1")
    ax.fill([0, 0, 0.5], [0, 1, 0.5], color=MAROON, alpha=0.35, label="x+y<1 inside support")
    ax.plot([0, 1], [0, 1], color=BLUE)
    ax.plot([0, 1], [1, 0], color=MAROON, ls="--")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=7, loc="lower right", frameon=False)
    return fig


def fig_q16():
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    ax.fill([0, 60, 60, 50, 0], [0, 60, 60, 60, 10], color=BLUE, alpha=0.25)
    ax.fill([0, 20, 60, 60], [0, 0, 40, 60], color=BLUE, alpha=0.25)
    ax.fill([0, 50, 0], [10, 60, 60], color=MAROON, alpha=0.18)
    ax.fill([20, 60, 60], [0, 0, 40], color=GOLD, alpha=0.35)
    ax.plot([0, 60], [0, 60], color="gray", lw=0.8)
    ax.text(10, 45, "B late\n(y − x > 10)", fontsize=7.5)
    ax.text(38, 8, "A late\n(x − y > 20)", fontsize=7.5)
    ax.text(26, 30, "meet", fontsize=9, color=BLUE, rotation=45)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    ax.set_aspect("equal")
    ax.set_xlabel("x = A's arrival (min)")
    ax.set_ylabel("y = B's arrival (min)")
    return fig


def fig_q18():
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    lab = ["AA", "Aa", "aa"]
    i = np.arange(3)
    ax.bar(i - 0.18, _o18, 0.36, color=BLUE, label="observed")
    ax.bar(i + 0.18, _e18, 0.36, color=GOLD, label="expected (HWE, p̂ = 0.65)")
    ax.set_xticks(i, lab)
    ax.set_ylabel("count")
    ax.legend(fontsize=8, frameon=False)
    return fig


def fig_q20():
    x = np.linspace(15, 105, 400)
    f1 = 0.6 * stats.norm.pdf(x, 50, 10)
    f2 = 0.4 * stats.norm.pdf(x, 70, 10)
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.plot(x, f1, color=BLUE, ls="--", label="0.6·N(50,10²)")
    ax.plot(x, f2, color=MAROON, ls="--", label="0.4·N(70,10²)")
    ax.plot(x, f1 + f2, color="black", lw=2, label="mixture")
    ax.plot(x, stats.norm.pdf(x, 58, 14), color=GOLD, lw=1.5, label="N(58,14²) — not equal")
    ax.set_yticks([])
    ax.set_xlabel("score")
    ax.legend(fontsize=7, frameon=False)
    return fig


def fig_q21():
    x = np.linspace(-5, 5, 400)
    f = stats.t.pdf(x, 5)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, f, color=BLUE)
    for m in (x <= -2.571, x >= 2.571):
        ax.fill_between(x[m], f[m], color=MAROON, alpha=0.35)
    ax.axvline(_t21, color=GOLD, lw=2)
    ax.text(_t21 + 0.1, 0.25, f"t = {_t21:.2f}", fontsize=8)
    ax.set_xticks([-2.571, 0, 2.571])
    ax.set_yticks([])
    ax.set_xlabel("t (5 df); shaded = rejection region, α = 0.05")
    return fig


def fig_q22():
    x = np.linspace(90, 116, 400)
    f0 = stats.norm.pdf(x, 100, 2.5)
    f1 = stats.norm.pdf(x, 106, 2.5)
    fig, ax = plt.subplots(figsize=(5.6, 2.6))
    ax.plot(x, f0, color=BLUE, label="X̄ under H₀ (μ=100)")
    ax.plot(x, f1, color=MAROON, label="X̄ under μ=106")
    m = x >= _c22
    ax.fill_between(x[m], f1[m], color=GOLD, alpha=0.55, label=f"power ≈ {_q22:.3f}")
    ax.fill_between(x[m], f0[m], color=BLUE, alpha=0.5, label="α = 0.05")
    ax.axvline(_c22, color="black", ls="--", lw=1)
    ax.text(_c22 + 0.2, 0.15, f"c = {_c22:.2f}", fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("x̄")
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    return fig


def fig_q27():
    x = np.linspace(0, 8, 400)
    f = x * np.exp(-x)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, f, color=BLUE, lw=2)
    for v, c, lab in [(1, GOLD, "mode = 1"), (_q27_med, MAROON, f"median ≈ {_q27_med:.2f}"),
                      (2, "black", "mean = 2")]:
        ax.axvline(v, color=c, ls="--", label=lab)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x) = x e⁻ˣ")
    ax.legend(fontsize=8, frameon=False)
    return fig


# ------------------------------------------------------------------ the set
SET = {
    "title": "Advanced Full-Syllabus Test I",
    "subtitle": "Hardest GATE DA level — multi-concept questions across the entire Probability & Statistics syllabus.",
    "focus": "A final-stage readiness check covering the WHOLE syllabus at the top end of GATE DA difficulty: "
             "counting with restrictions, independence subtleties, mixed CDFs, order statistics of uniforms, "
             "minima of exponentials, Poisson thinning, random sums and conditional variance, joint pdfs on "
             "triangular supports, geometric probability, normal mixtures, covariance of indicator sums, Bayes "
             "with binomial and naive-Bayes likelihoods, CLT-based sample-size design, z-test power, paired "
             "t-test, t-based CI from raw sums, and a chi-squared goodness-of-fit test whose expected counts "
             "must first be derived (Hardy–Weinberg). Almost every 2-mark question chains two or more ideas — "
             "attempt it under strict 90-minute conditions and treat any slip as a revision flag.",
    "minutes": 90,
    "questions": [
        # ============================================================ 1-mark
        dict(
            qtype="MCQ", marks=1, topic="Permutations with repetition", difficulty="Medium",
            text="The number of distinct arrangements of the letters of the word <b>STATISTICS</b> in which "
                 "the three S's do <b>not</b> all appear together (as a block SSS) is",
            options=[f"{_q1_total}", f"{_q1}", f"{_q1_total - factorial(8) // factorial(3)}", f"{_q1_block}"],
            answer="B",
            solution=[
                "<b>Concept:</b> arrangements of a multiset = n!/(product of factorials of repeat counts); "
                "use the complement 'all S together'.",
                "Letter counts: S = 3, T = 3, I = 2, A = 1, C = 1 (total 10).",
                r"$$\text{Total}=\dfrac{10!}{3!\,3!\,2!}=\dfrac{3628800}{72}=" + f"{_q1_total}",
                "Glue the three S's into one super-letter [SSS]. Now there are 8 objects: [SSS], T, T, T, I, I, A, C.",
                r"$$\text{SSS together}=\dfrac{8!}{3!\,2!}=\dfrac{40320}{12}=" + f"{_q1_block}",
                r"$$\text{Required}=" + f"{_q1_total}-{_q1_block}={_q1}",
                "Option (C) divides 8! only by 3! (forgets that the two I's are identical); (D) is the "
                "complementary count itself.",
                ("note", "When you glue identical letters into a block, the block is a single object — do not "
                         "multiply by 3! for internal order (the S's are identical), but keep dividing by the "
                         "factorials of the OTHER repeated letters.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Pairwise vs mutual independence", difficulty="Medium",
            text="Two fair coins are tossed. Let A = {first coin shows H}, B = {second coin shows H} and "
                 "C = {exactly one head}. Which of the following statements is/are TRUE?",
            options=["A, B, C are pairwise independent",
                     "A, B, C are mutually independent",
                     "P(A ∩ B ∩ C) = 0",
                     "A and C<super>c</super> are independent"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> mutual independence needs every sub-collection to factor, including the triple; "
                "pairwise independence does not imply it.",
                "Sample space {HH, HT, TH, TT}, each 1/4. A = {HH, HT}, B = {HH, TH}, C = {HT, TH}; each has probability 1/2.",
                ("table", [["Pair", "Intersection", "Probability", "Product of marginals"],
                           ["A, B", "{HH}", "1/4", "1/4"],
                           ["A, C", "{HT}", "1/4", "1/4"],
                           ["B, C", "{TH}", "1/4", "1/4"]]),
                "<b>(A) TRUE</b> — every pair factorises.",
                "<b>(C) TRUE</b> — A ∩ B = {HH} has two heads, so it cannot have exactly one head: A ∩ B ∩ C = Ø.",
                r"$$P(A\cap B\cap C)=0\neq P(A)P(B)P(C)=\dfrac{1}{8}",
                "<b>(B) FALSE</b> — the triple product fails.",
                "<b>(D) TRUE</b> — if A and C are independent then so are A and C<super>c</super>: "
                "P(A ∩ C<super>c</super>) = P(A) − P(A ∩ C) = 1/2 − 1/4 = 1/4 = P(A)P(C<super>c</super>).",
                ("note", "Knowing any two of A, B, C determines the third completely — that is why the "
                         "triple fails while every pair is fine.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Minimum of exponentials (series reliability)", difficulty="Medium",
            text="A sensor node works only if all three of its components work (series system). The component "
                 "lifetimes are independent exponential random variables with failure rates 0.1, 0.2 and 0.2 per "
                 "year. The probability that the node is still working after 3 years is ______ "
                 "(round off to 3 decimal places).",
            answer=f"{_q3:.3f}", range=(0.222, 0.224),
            solution=[
                "<b>Concept:</b> the minimum of independent exponentials is exponential with the sum of the rates.",
                "System lifetime T = min(T<sub>1</sub>, T<sub>2</sub>, T<sub>3</sub>).",
                r"$$P(T>t)=\prod_{i=1}^{3}P(T_i>t)=e^{-0.1t}e^{-0.2t}e^{-0.2t}=e^{-0.5t}",
                r"$$P(T>3)=e^{-1.5}\approx " + f"{_q3:.4f}",
                ("note", "The expected life of the series node is 1/0.5 = 2 years, and the probability that "
                         "component 1 is the first to fail is 0.1/0.5 = 0.2 — both follow from the same "
                         "'competing exponentials' fact.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Order statistics of uniforms", difficulty="Medium",
            text="X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub> are i.i.d. Uniform(0, 1) and M is their median "
                 "(the middle value). P(M ≤ 1/4) equals",
            options=["5/32", "1/64", "9/64", "1/4"],
            answer="A",
            solution=[
                "<b>Concept:</b> the k-th order statistic is ≤ m iff at least k of the n observations are ≤ m "
                "— a binomial count.",
                "Let N = number of X<sub>i</sub> ≤ 1/4. Then N ∼ Bin(3, 1/4). The median is ≤ 1/4 iff N ≥ 2.",
                r"$$P(N\geq 2)=\binom{3}{2}\left(\dfrac{1}{4}\right)^2\dfrac{3}{4}+\left(\dfrac{1}{4}\right)^3=\dfrac{9}{64}+\dfrac{1}{64}=\dfrac{5}{32}",
                "Cross-check with the pdf of the median, f<sub>M</sub>(m) = 6m(1 − m):",
                r"$$\int_0^{1/4}6m(1-m)\,dm=\left[3m^2-2m^3\right]_0^{1/4}=\dfrac{3}{16}-\dfrac{1}{32}=\dfrac{5}{32}",
                ("fig", fig_q4),
                "(B) 1/64 is P(all three ≤ 1/4), i.e. the maximum; (C) 9/64 counts exactly two only.",
                ("note", "'At least k successes' — never 'exactly k' — is what translates an order statistic "
                         "into a binomial event.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Chi-squared, t and normal relationships", difficulty="Medium",
            text="Which of the following statements is/are TRUE?",
            options=["If Z<sub>1</sub>, …, Z<sub>k</sub> are i.i.d. N(0, 1), then ∑Z<sub>i</sub><super>2</super> "
                     "has mean k and variance 2k",
                     "For every finite ν, the t<sub>ν</sub> density has heavier tails than N(0, 1)",
                     "If T ∼ t<sub>ν</sub>, then T<super>2</super> ∼ χ<super>2</super><sub>1</sub>",
                     "The χ<super>2</super><sub>k</sub> density is symmetric about its mean k"],
            answer="A, B",
            solution=[
                "<b>Concept:</b> χ<super>2</super><sub>k</sub> = sum of k squared standard normals; t<sub>ν</sub> = Z/√(V/ν) "
                "with V ∼ χ<super>2</super><sub>ν</sub> independent of Z.",
                "<b>(A) TRUE</b> — E[Z<super>2</super>] = 1 and Var(Z<super>2</super>) = E[Z<super>4</super>] − 1 = 3 − 1 = 2, so the sum has mean k, variance 2k.",
                "<b>(B) TRUE</b> — the random denominator √(V/ν) inflates the spread; P(|T| &gt; c) &gt; P(|Z| &gt; c) "
                "for large c, e.g. t<sub>0.025,10</sub> = 2.228 &gt; 1.96.",
                "<b>(C) FALSE</b> — T<super>2</super> = Z<super>2</super>/(V/ν) is a ratio of two independent χ<super>2</super>'s scaled by their df, i.e. an "
                "F(1, ν) variable, not χ<super>2</super><sub>1</sub>. Only as ν → ∞ does it approach χ<super>2</super><sub>1</sub>.",
                "<b>(D) FALSE</b> — χ<super>2</super><sub>k</sub> is supported on (0, ∞) and right-skewed; mean k exceeds its mode k − 2.",
                ("note", "Option (C) is the classic 'limit statement passed off as exact' trap.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Poisson thinning", difficulty="Medium",
            text="E-mails arrive at an inbox as a Poisson process with rate 12 per hour. Independently, each "
                 "e-mail is spam with probability 0.25. The probability that no spam arrives in a 20-minute "
                 "window is ______ (round off to 3 decimal places).",
            answer=f"{_q6:.3f}", range=(0.367, 0.369),
            solution=[
                "<b>Concept:</b> independently marking each event of a Poisson(λ) stream with probability p gives "
                "a Poisson(λp) stream (thinning).",
                "Spam stream rate = 12 × 0.25 = 3 per hour. In 20 min = 1/3 hour the spam count is Poisson with mean",
                r"$$\mu = 3\times\dfrac{1}{3}=1,\qquad P(\text{no spam})=e^{-1}\approx 0.368",
                "Long route (same answer): condition on the total N ∼ Poisson(4):",
                r"$$\sum_{n=0}^{\infty}e^{-4}\dfrac{4^n}{n!}(0.75)^n=e^{-4}e^{3}=e^{-1}",
                ("note", "Thinning lets you ignore the non-spam e-mails entirely.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Standard deviation (update)", difficulty="Medium",
            text="Ten observations have mean 20 and standard deviation 4 (computed with divisor n). One "
                 "observation whose value is exactly 20 is deleted. The standard deviation (divisor n) of the "
                 "remaining 9 observations is",
            options=["4.000", f"{_q7:.3f}", f"{4 * math.sqrt(0.9):.3f}", f"{40 / 9:.3f}"],
            answer="B",
            solution=[
                "<b>Concept:</b> SD = √(sum of squared deviations / n); removing a value at the mean leaves the "
                "mean and the sum of squared deviations unchanged but reduces n.",
                r"$$\sum_{i=1}^{10}(x_i-20)^2=n\sigma^2=10\times 16=160",
                "Removing x = 20 removes a zero deviation, and the mean of the remaining 9 values is still "
                "(200 − 20)/9 = 20. Hence",
                r"$$\sigma_{\text{new}}=\sqrt{\dfrac{160}{9}}=\dfrac{4\sqrt{10}}{3}\approx " + f"{_q7:.3f}",
                "(A) assumes SD is unchanged; (C) multiplies instead of divides by 9/10; (D) is 40/9 = 160/36, a "
                "mis-scaling.",
                ("note", "The SD INCREASES when you delete a point sitting exactly at the mean — the "
                         "remaining points are, on average, further from the centre.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Mixed CDF and expectation", difficulty="Hard",
            text=["A random variable X has CDF F(x) = 0 for x &lt; 0, F(x) = (x + 1)/4 for 0 ≤ x &lt; 1 and "
                  "F(x) = 1 for x ≥ 1 (plotted below). E[X] equals",
                  ("fig", fig_q8)],
            options=["1/8", "3/8", "1/2", "5/8"],
            answer="D",
            solution=[
                "<b>Concept:</b> jumps in a CDF are point masses; the sloped part is a density. For X ≥ 0, "
                "E[X] = ∫<sub>0</sub><super>∞</super>(1 − F(x)) dx.",
                "Jump at 0: P(X = 0) = F(0) − F(0<super>−</super>) = 1/4. Jump at 1: P(X = 1) = 1 − F(1<super>−</super>) = 1 − 2/4 = 1/2.",
                "Continuous part on (0, 1): density F′(x) = 1/4 (total mass 1/4). Check: 1/4 + 1/2 + 1/4 = 1.",
                r"$$E[X]=0\cdot\dfrac{1}{4}+\int_0^1 x\cdot\dfrac{1}{4}\,dx+1\cdot\dfrac{1}{2}=\dfrac{1}{8}+\dfrac{1}{2}=\dfrac{5}{8}",
                "Tail-integral check:",
                r"$$\int_0^1\left(1-\dfrac{x+1}{4}\right)dx=\int_0^1\dfrac{3-x}{4}\,dx=\dfrac{3-1/2}{4}=\dfrac{5}{8}",
                "(A) 1/8 uses only the continuous part and forgets the atom at 1.",
                ("note", "Always read off the jumps first — a mixed distribution's mean needs both the "
                         "atoms and the density.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Variance of a linear combination", difficulty="Medium",
            text="Var(X) = 4, Var(Y) = 9 and the correlation coefficient of X and Y is −0.5. Var(2X − 3Y + 5) equals",
            options=["61", "97", "133", "138"],
            answer="C",
            solution=[
                "<b>Concept:</b> Var(aX + bY + c) = a<super>2</super>Var X + b<super>2</super>Var Y + 2ab Cov(X, Y); constants do not matter.",
                r"$$\text{Cov}(X,Y)=\rho\,\sigma_X\sigma_Y=(-0.5)(2)(3)=-3",
                r"$$\text{Var}=4(4)+9(9)+2(2)(-3)(-3)=16+81+36=133",
                "(A) 61 = 97 − 36 uses the wrong sign for the cross term; (B) 97 ignores correlation; "
                "(D) adds the constant 5.",
                ("note", "Negative correlation combined with a minus sign in front of Y gives a POSITIVE "
                         "cross term: 2ab·Cov = 2(2)(−3)(−3) = +36.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Conditional variance (random number of trials)", difficulty="Hard",
            text="A fair die is rolled; if it shows N, then N fair coins are tossed. Let H be the number of heads "
                 "obtained. Var(H) is ______ (round off to 2 decimal places).",
            answer=f"{_q10:.2f}", range=(1.59, 1.61),
            solution=[
                "<b>Concept:</b> law of total variance Var(H) = E[Var(H | N)] + Var(E[H | N]).",
                "Given N, H ∼ Bin(N, 1/2): E[H | N] = N/2 and Var(H | N) = N/4.",
                r"$$E[N]=3.5,\qquad \text{Var}(N)=\dfrac{6^2-1}{12}=\dfrac{35}{12}",
                r"$$\text{Var}(H)=E\left[\dfrac{N}{4}\right]+\text{Var}\left(\dfrac{N}{2}\right)=\dfrac{3.5}{4}+\dfrac{35/12}{4}",
                r"$$=0.875+0.7292=1.6042\approx 1.60",
                ("note", "Forgetting the second term gives 0.875 — the variability of N itself adds 0.729.",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Hypothesis-testing concepts", difficulty="Medium",
            text="Which of the following statements is/are TRUE?",
            options=["The p-value is the probability that H<sub>0</sub> is true given the data",
                     "If the 95% two-sided z-interval for μ excludes μ<sub>0</sub>, the two-sided z-test of "
                     "H<sub>0</sub>: μ = μ<sub>0</sub> rejects at α = 0.05",
                     "For a fixed α and a fixed true μ ≠ μ<sub>0</sub>, the power of the z-test increases with n",
                     "P(Type I error) = 1 − power"],
            answer="B, C",
            solution=[
                "<b>Concept:</b> duality of CIs and tests; power = P(reject H<sub>0</sub> | H<sub>1</sub> true).",
                "<b>(A) FALSE</b> — the p-value is P(data at least this extreme | H<sub>0</sub>), computed assuming "
                "H<sub>0</sub>; it is not a posterior probability.",
                "<b>(B) TRUE</b> — μ<sub>0</sub> is outside x̄ ± 1.96σ/√n ⟺ |x̄ − μ<sub>0</sub>|/(σ/√n) &gt; 1.96.",
                "<b>(C) TRUE</b> — the standardised shift (μ − μ<sub>0</sub>)√n/σ grows with n, so the "
                "alternative distribution moves deeper into the rejection region.",
                "<b>(D) FALSE</b> — 1 − power = β = P(Type II error). α and power are computed under different "
                "hypotheses.",
                ("note", "α is fixed under H<sub>0</sub>; β and power live under H<sub>1</sub>.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Normal distribution (parameter recovery)", difficulty="Medium",
            text="X ∼ N(μ, σ<super>2</super>) with P(X &lt; 10) = 0.1587 and P(X &gt; 16) = 0.0228. Using Φ(1) = 0.8413, "
                 "Φ(2) = 0.9772 and Φ(0.5) = 0.6915, P(X &gt; 13) equals",
            options=["0.6915", "0.3085", "0.1915", "0.4013"],
            answer="B",
            solution=[
                "<b>Concept:</b> each tail probability fixes one z-score; two equations give μ and σ.",
                "P(X &lt; 10) = 0.1587 = Φ(−1) ⇒ (10 − μ)/σ = −1. P(X &gt; 16) = 0.0228 ⇒ (16 − μ)/σ = 2.",
                r"$$\mu-\sigma=10,\quad \mu+2\sigma=16\ \Rightarrow\ \sigma=2,\ \mu=12",
                r"$$P(X>13)=P\left(Z>\dfrac{13-12}{2}\right)=1-\Phi(0.5)=0.3085",
                ("fig", fig_q12),
                "(A) is P(X &lt; 13); (C) is P(12 &lt; X &lt; 13).",
                ("note", "Write both tail conditions as linear equations in μ and σ — never guess σ "
                         "from one tail only.", "Shortcut"),
            ],
        ),
        # ============================================================ 2-mark
        dict(
            qtype="NAT", marks=2, topic="Bayes theorem with binomial likelihood", difficulty="Hard",
            text="A bag has three coins: two are fair and one is biased with P(H) = 0.8. A coin is drawn at "
                 "random and tossed 5 times, giving exactly 4 heads. The same coin is tossed once more. The "
                 "probability that this sixth toss is a head is ______ (round off to 3 decimal places).",
            answer=f"{_q13:.3f}", range=(0.668, 0.672),
            solution=[
                "<b>Concept:</b> update the prior on the coin with the binomial likelihood (Bayes), then average "
                "the next-toss probability over the posterior (law of total probability).",
                ("fig", fig_q13),
                "Likelihoods of '4 heads in 5 tosses':",
                r"$$L_B=\binom{5}{4}(0.8)^4(0.2)=0.4096,\qquad L_F=\binom{5}{4}(0.5)^5=0.15625",
                r"$$P(B\mid 4H)=\dfrac{\frac{1}{3}(0.4096)}{\frac{1}{3}(0.4096)+\frac{2}{3}(0.15625)}=\dfrac{0.4096}{0.4096+0.3125}",
                r"$$P(B\mid 4H)=\dfrac{0.4096}{0.7221}\approx " + f"{_q13_post:.4f}",
                "Given the coin, the tosses are independent, so",
                r"$$P(H_6\mid 4H)=0.8\,P(B\mid 4H)+0.5\,P(F\mid 4H)",
                r"$$=0.8(" + f"{_q13_post:.4f}" + r")+0.5(" + f"{1 - _q13_post:.4f}" + r")\approx " + f"{_q13:.4f}",
                "Monte-Carlo (10<super>6</super> runs) gives ≈ 0.669–0.670, confirming the value.",
                ("note", "The tosses are NOT unconditionally independent — learning '4 heads' raises the chance "
                         "the coin is biased, so the 6th-toss probability (0.670) is neither 0.5 nor the prior "
                         "average 0.6.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Random sums (compound Poisson)", difficulty="Hard",
            text="The number of insurance claims in a month, N, is Poisson with mean 4. Claim sizes "
                 "X<sub>1</sub>, X<sub>2</sub>, … are i.i.d. exponential with mean 2 (lakh rupees), independent "
                 "of N. Let S = X<sub>1</sub> + … + X<sub>N</sub> (S = 0 if N = 0). Var(S) equals",
            options=["8", "16", "32", "64"],
            answer="C",
            solution=[
                "<b>Concept:</b> for a random sum, E[S] = E[N]E[X] and Var(S) = E[N]Var(X) + Var(N)(E[X])<super>2</super>.",
                "Conditional moments: E[S | N] = 2N and Var(S | N) = N·Var(X) = 4N (Var of Exp with mean 2 is 2<super>2</super> = 4).",
                r"$$\text{Var}(S)=E[\text{Var}(S\mid N)]+\text{Var}(E[S\mid N])=E[4N]+\text{Var}(2N)",
                r"$$=4(4)+4(4)=32",
                "Compound-Poisson shortcut: Var(S) = λE[X<super>2</super>] = 4 × (Var X + (E X)<super>2</super>) = 4 × 8 = 32.",
                "Distractors: 16 = E[N]Var(X) only (forgets randomness of N); 64 = (E N)<super>2</super>Var(X), treating S as "
                "4 copies of the same claim; 8 = E[S].",
                ("note", "For compound Poisson, Var(S) = λE[X<super>2</super>] — the SECOND RAW moment, not the variance.",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Joint pdf on a triangle; conditional expectation; covariance",
            difficulty="Hard",
            text=["(X, Y) has joint pdf f(x, y) = 2 for 0 &lt; x &lt; y &lt; 1 and 0 otherwise (support shaded "
                  "below). Which of the following is/are TRUE?",
                  ("fig", fig_q15)],
            options=["X and Y are independent",
                     "E[Y | X = x] = (1 + x)/2 for 0 &lt; x &lt; 1",
                     "P(X + Y &lt; 1) = 1/2",
                     "Cov(X, Y) = 1/36"],
            answer="B, C, D",
            solution=[
                "<b>Concept:</b> marginals by integrating out; conditional pdf = joint/marginal; a non-rectangular "
                "support rules out independence.",
                "Marginals:",
                r"$$f_X(x)=\int_x^1 2\,dy=2(1-x),\qquad f_Y(y)=\int_0^y 2\,dx=2y",
                "<b>(A) FALSE</b> — f<sub>X</sub>(x)f<sub>Y</sub>(y) = 4y(1 − x) ≠ 2, and the support is a triangle "
                "(e.g. f = 0 at (0.8, 0.2) though both marginals are positive there).",
                "<b>(B) TRUE</b> — for fixed x:",
                r"$$f_{Y\mid X}(y\mid x)=\dfrac{2}{2(1-x)}=\dfrac{1}{1-x},\ x<y<1\ \Rightarrow\ Y\mid X=x\sim U(x,1)",
                "so E[Y | X = x] = (x + 1)/2.",
                "<b>(C) TRUE</b> — inside the support, x + y &lt; 1 means x &lt; y &lt; 1 − x with x &lt; 1/2: a triangle "
                "with vertices (0,0), (0,1), (1/2,1/2) of area 1/4.",
                r"$$P(X+Y<1)=2\times\dfrac{1}{4}=\dfrac{1}{2}",
                "<b>(D) TRUE</b>:",
                r"$$E[X]=\int_0^1 2x(1-x)\,dx=\dfrac{1}{3},\qquad E[Y]=\int_0^1 2y^2\,dy=\dfrac{2}{3}",
                r"$$E[XY]=\int_0^1\int_0^y 2xy\,dx\,dy=\int_0^1 y^3\,dy=\dfrac{1}{4}",
                r"$$\text{Cov}(X,Y)=\dfrac{1}{4}-\dfrac{1}{3}\cdot\dfrac{2}{3}=\dfrac{9-8}{36}=\dfrac{1}{36}",
                ("note", "This is exactly the (min, max) of two i.i.d. U(0,1) variables — that is why "
                         "E[X] = 1/3 and E[Y] = 2/3.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Geometric probability (joint uniform)", difficulty="Hard",
            text="Two analysts A and B arrive at a meeting room independently, each at a time uniformly "
                 "distributed between 10:00 and 11:00. A waits 10 minutes for B and then leaves; B waits 20 "
                 "minutes for A and then leaves. The probability that they meet is ______ "
                 "(round off to 3 decimal places).",
            answer=f"{_q16:.3f}", range=(0.429, 0.432),
            solution=[
                "<b>Concept:</b> for independent uniforms the joint pdf is constant, so probability = favourable "
                "area / total area.",
                "Let X, Y ∈ (0, 60) be the arrival minutes of A and B. They meet iff "
                "(A first and B arrives within 10 min) or (B first and A arrives within 20 min):",
                r"$$0\leq Y-X\leq 10\quad\text{or}\quad 0\leq X-Y\leq 20",
                ("fig", fig_q16),
                "Non-meeting regions are two right triangles:",
                r"$$Y-X>10:\ \dfrac{50^2}{2}=1250,\qquad X-Y>20:\ \dfrac{40^2}{2}=800",
                r"$$P(\text{meet})=1-\dfrac{1250+800}{3600}=\dfrac{1550}{3600}\approx " + f"{_q16:.4f}",
                ("note", "Attach each waiting time to the person who arrives FIRST: A's 10-minute patience "
                         "matters only when A is early (Y − X), B's 20 minutes only when B is early (X − Y). "
                         "Swapping them gives the same number here by symmetry of the square — but the "
                         "triangles must be labelled correctly in an exam figure.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="CLT-based sample size for a proportion", difficulty="Hard",
            text="An ML team wants to estimate the misclassification rate p of a model on live traffic with a "
                 "95% confidence interval of half-width (margin of error) at most 0.03. A pilot study shows "
                 "that p is certainly no larger than 0.20. Using the normal approximation (z<sub>0.025</sub> = "
                 "1.96), the smallest sample size that guarantees the requirement is",
            options=[f"{_q17}", "1068", f"{_q17 - 1}", "601"],
            answer="A",
            solution=[
                "<b>Concept:</b> margin E = z<sub>α/2</sub>√(p(1 − p)/n) ⇒ n ≥ z<super>2</super>p(1 − p)/E<super>2</super>, using the "
                "worst-case p over the allowed range.",
                "p(1 − p) increases on [0, 0.5], so over p ≤ 0.2 its maximum is at p = 0.2: 0.2 × 0.8 = 0.16.",
                r"$$n\geq\dfrac{1.96^2(0.16)}{0.03^2}=\dfrac{3.8416\times 0.16}{0.0009}=682.95",
                "n must be an integer AND satisfy the inequality, so round UP: n = 683.",
                "(B) 1068 uses the worst case p = 0.5 — valid but not the smallest given the pilot information; "
                "(C) 682 rounds down and violates the margin.",
                ("note", "Sample-size answers are always rounded UP, and the 'worst case' p is the value in "
                         "the allowed range CLOSEST to 0.5.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Chi-squared goodness of fit with estimated parameter (genetics)",
            difficulty="Hard",
            text=["Genotypes at a locus with alleles A and a are recorded for 100 individuals:",
                  ("table", [["Genotype", "AA", "Aa", "aa", "Total"], ["Count", "50", "30", "20", "100"]]),
                  "To test Hardy–Weinberg equilibrium (expected proportions p<super>2</super>, 2p(1 − p), (1 − p)<super>2</super>), the allele "
                  "frequency p is estimated from the data by allele counting. The value of the Pearson χ<super>2</super> "
                  "statistic is ______ (round off to 2 decimal places)."],
            answer=f"{_q18:.2f}", range=(11.55, 11.66),
            solution=[
                "<b>Concept:</b> χ<super>2</super> = ∑(O − E)<super>2</super>/E with E derived from the model; each estimated parameter costs "
                "one degree of freedom.",
                "Allele counting: each AA contributes 2 A alleles, each Aa one; total alleles = 200.",
                r"$$\hat{p}=\dfrac{2(50)+30}{200}=\dfrac{130}{200}=0.65",
                r"$$E_{AA}=100(0.65)^2=42.25,\ E_{Aa}=100(2)(0.65)(0.35)=45.5,\ E_{aa}=100(0.35)^2=12.25",
                ("table", [["Genotype", "O", "E", "(O − E)<super>2</super>/E"]] +
                 [[g, f"{o}", f"{e:.2f}", f"{c:.4f}"] for g, o, e, c in zip(["AA", "Aa", "aa"], _o18, _e18, _c18)] +
                 [["Total", "100", "100", f"{_q18:.4f}"]]),
                ("fig", fig_q18),
                r"$$\chi^2=\dfrac{7.75^2}{42.25}+\dfrac{15.5^2}{45.5}+\dfrac{7.75^2}{12.25}\approx " + f"{_q18:.2f}",
                "Degrees of freedom = 3 categories − 1 − 1 (estimated p) = 1. Since 11.60 &gt; χ<super>2</super><sub>0.05,1</sub> "
                "= 3.841 (even &gt; χ<super>2</super><sub>0.001,1</sub> = 10.83), HWE is rejected — there is a heterozygote deficit.",
                ("note", "The deviations are ±7.75 for both homozygotes and −15.5 for heterozygotes: with one "
                         "estimated parameter the deviations are forced to cancel, which is the df = 1 "
                         "constraint you can see.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Covariance of indicator sums", difficulty="Hard",
            text="Ten distinguishable balls are thrown independently and uniformly into 5 boxes. Let X be the "
                 "number of empty boxes. Var(X) is closest to",
            options=[f"{_q19:.3f}", f"{_q19_E:.3f}", f"{_q19_naive:.3f}", "0.250"],
            answer="A",
            solution=[
                "<b>Concept:</b> write X = ∑I<sub>j</sub> with I<sub>j</sub> = 1 if box j is empty; then "
                "Var(X) = ∑Var(I<sub>j</sub>) + ∑<sub>j≠k</sub>Cov(I<sub>j</sub>, I<sub>k</sub>).",
                r"$$P(I_j=1)=\left(\dfrac{4}{5}\right)^{10}=" + f"{_pe:.5f}" + r",\quad P(I_jI_k=1)=\left(\dfrac{3}{5}\right)^{10}=" + f"{0.6 ** 10:.5f}",
                r"$$E[X]=5(0.8)^{10}=" + f"{_q19_E:.4f}",
                r"$$E[X^2]=\sum_j E[I_j]+\sum_{j\neq k}E[I_jI_k]=5(0.8)^{10}+20(0.6)^{10}",
                r"$$\text{Var}(X)=5(0.8)^{10}+20(0.6)^{10}-25(0.8)^{20}",
                r"$$=" + f"{_q19_E:.4f}+{20 * 0.6 ** 10:.4f}-{25 * _pe ** 2:.4f}={_q19:.4f}",
                "There are 5 × 4 = 20 ordered pairs (j, k), j ≠ k. A simulation of 2 × 10<super>5</super> throws "
                "gives Var ≈ 0.37.",
                f"(C) {_q19_naive:.3f} = 5p(1 − p) ignores the (negative) covariances between boxes; "
                f"(B) {_q19_E:.3f} is E[X].",
                ("note", "Indicators of 'box j empty' are negatively correlated: if one box is empty the balls "
                         "crowd into the others, making another empty box less likely.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Normal mixtures", difficulty="Hard",
            text="In an entrance test, 60% of candidates come from population 1 with scores N(50, 10<super>2</super>) and 40% "
                 "from population 2 with scores N(70, 10<super>2</super>). Let X be the score of a randomly chosen candidate. "
                 "Using Φ(2) = 0.9772, which of the following is/are TRUE?",
            options=["E[X] = 58",
                     "The standard deviation of X is 14",
                     "X ∼ N(58, 14<super>2</super>)",
                     "P(X &gt; 70) ≈ 0.214"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> condition on the population label G; use total expectation, total variance and "
                "total probability.",
                "<b>(A) TRUE</b>: E[X] = 0.6(50) + 0.4(70) = 58.",
                "<b>(B) TRUE</b>: Var(X) = E[Var(X | G)] + Var(E[X | G]).",
                r"$$E[\text{Var}(X\mid G)]=100,\quad \text{Var}(E[X\mid G])=0.6(0.4)(70-50)^2=96",
                r"$$\text{Var}(X)=196\ \Rightarrow\ \text{SD}=14",
                "<b>(C) FALSE</b>: a mixture of normals is not normal (it is a weighted sum of densities, not of "
                "random variables). Its density below is visibly skewed / flattened compared with N(58, 14<super>2</super>).",
                ("fig", fig_q20),
                "<b>(D) TRUE</b>:",
                r"$$P(X>70)=0.6\,P\left(Z>\dfrac{70-50}{10}\right)+0.4\,P(Z>0)=0.6(0.0228)+0.4(0.5)",
                r"$$=0.01368+0.2=" + f"{_q20:.4f}",
                "(Using N(58,14<super>2</super>) would give P(Z &gt; 0.857) ≈ 0.196 — wrong.)",
                ("note", "Sum of independent normals ⇒ normal; MIXTURE of normals ⇒ generally not normal. "
                         "The between-group term p(1 − p)(Δμ)<super>2</super> is the part students forget.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Paired t-test", difficulty="Hard",
            text=["A new caching layer is tested on 6 servers. The reduction in median latency (ms) on each "
                  "server, d = before − after, is:",
                  ("table", [["Server", "1", "2", "3", "4", "5", "6"], ["d", "3", "5", "−1", "4", "6", "2"]]),
                  "Test H<sub>0</sub>: μ<sub>d</sub> = 0 against H<sub>1</sub>: μ<sub>d</sub> ≠ 0 at α = 0.05 "
                  "(t<sub>0.025,5</sub> = 2.571). Which is correct?"],
            options=[f"t ≈ {_t21:.2f}; reject H<sub>0</sub>",
                     "t ≈ 3.42; reject H<sub>0</sub>",
                     "t ≈ 1.28; do not reject H<sub>0</sub>",
                     "t ≈ 2.85; reject H<sub>0</sub>"],
            answer="A",
            solution=[
                "<b>Concept:</b> paired data reduce to a one-sample t-test on the differences: "
                "t = d̄/(s<sub>d</sub>/√n) with n − 1 df.",
                r"$$\bar{d}=\dfrac{3+5-1+4+6+2}{6}=\dfrac{19}{6}=3.1667",
                r"$$\sum d_i^2=91,\qquad \sum(d_i-\bar{d})^2=91-6(3.1667)^2=30.833",
                r"$$s_d=\sqrt{\dfrac{30.833}{5}}=" + f"{_s21:.4f}" + r",\qquad \dfrac{s_d}{\sqrt{6}}=" + f"{_s21 / math.sqrt(6):.4f}",
                r"$$t=\dfrac{3.1667}{" + f"{_s21 / math.sqrt(6):.4f}" + r"}=" + f"{_t21:.3f}",
                "|t| = 3.12 &gt; 2.571 ⇒ reject H<sub>0</sub>: the caching layer changes latency.",
                ("fig", fig_q21),
                "(B) uses divisor n in s (3.42); (C) forgets the √n (d̄/s); (D) divides by √(n − 1) instead of √n.",
                ("note", "Treating the before/after columns as two independent samples throws away the pairing "
                         "and usually inflates the standard error.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Power of a one-sided z-test", difficulty="Hard",
            text="Daily page-load counts are normal with σ = 15. To test H<sub>0</sub>: μ = 100 against "
                 "H<sub>1</sub>: μ &gt; 100, a z-test at α = 0.05 (z<sub>0.05</sub> = 1.645) is based on n = 36 "
                 "days. If in fact μ = 106, the power of the test is ______ (round off to 2 decimal places).",
            answer=f"{_q22:.2f}", range=(0.77, 0.78),
            solution=[
                "<b>Concept:</b> find the rejection cut-off on the x̄ scale under H<sub>0</sub>, then compute the "
                "probability of exceeding it under the alternative.",
                r"$$\sigma_{\bar{X}}=\dfrac{15}{\sqrt{36}}=2.5,\qquad c=100+1.645(2.5)=104.1125",
                r"$$\text{Power}=P(\bar{X}>104.1125\mid\mu=106)=P\left(Z>\dfrac{104.1125-106}{2.5}\right)",
                r"$$=P(Z>-0.755)=\Phi(0.755)\approx " + f"{_q22:.4f}",
                ("fig", fig_q22),
                "β = P(Type II error) ≈ 0.225.",
                ("note", "Power formula in one line: Φ((μ<sub>1</sub> − μ<sub>0</sub>)√n/σ − z<sub>α</sub>) "
                         "= Φ(2.4 − 1.645) = Φ(0.755).", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Conditioning a Poisson sum", difficulty="Hard",
            text="The numbers of bug reports from Android and iOS users in a day are independent Poisson random "
                 "variables with means 3 and 5 respectively. Given that a total of 8 reports arrived, the "
                 "probability that exactly 3 came from Android users is",
            options=[f"{_q23:.4f}", f"{stats.poisson.pmf(3, 3):.4f}", "0.3750", f"{comb(8, 3) * 0.5 ** 8:.4f}"],
            answer="A",
            solution=[
                "<b>Concept:</b> if X ∼ Poi(λ<sub>1</sub>), Y ∼ Poi(λ<sub>2</sub>) independent, then "
                "X | X + Y = n ∼ Bin(n, λ<sub>1</sub>/(λ<sub>1</sub> + λ<sub>2</sub>)).",
                "Derivation:",
                r"$$P(X=3\mid X+Y=8)=\dfrac{P(X=3)P(Y=5)}{P(X+Y=8)}=\dfrac{e^{-3}\frac{3^3}{3!}\,e^{-5}\frac{5^5}{5!}}{e^{-8}\frac{8^8}{8!}}",
                r"$$=\dfrac{8!}{3!\,5!}\cdot\dfrac{3^3\,5^5}{8^8}=\binom{8}{3}\left(\dfrac{3}{8}\right)^3\left(\dfrac{5}{8}\right)^5",
                r"$$=56\times 0.052734\times 0.095367\approx " + f"{_q23:.4f}",
                "(B) is the unconditional P(X = 3); (C) is 3/8 alone; (D) uses p = 1/2.",
                ("note", "This is the reverse of Poisson thinning: conditioning a superposition on its total "
                         "gives a binomial split.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Competing exponentials; memorylessness", difficulty="Hard",
            text="T<sub>1</sub> ∼ Exp(rate 1) and T<sub>2</sub> ∼ Exp(rate 2) are independent lifetimes "
                 "(in years) of two redundant disks. Which of the following is/are TRUE?",
            options=["P(T<sub>1</sub> &lt; T<sub>2</sub>) = 1/3",
                     "min(T<sub>1</sub>, T<sub>2</sub>) is exponential with mean 1/3",
                     "E[max(T<sub>1</sub>, T<sub>2</sub>)] = 7/6",
                     "P(T<sub>1</sub> &gt; 2 | T<sub>1</sub> &gt; 1) = e<super>−2</super>"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> competing exponentials — the minimum is Exp(λ<sub>1</sub> + λ<sub>2</sub>) and the "
                "winner is i with probability λ<sub>i</sub>/(λ<sub>1</sub> + λ<sub>2</sub>).",
                "<b>(A) TRUE</b>:",
                r"$$P(T_1<T_2)=\int_0^\infty e^{-t}\,e^{-2t}\,dt=\dfrac{1}{1+2}=\dfrac{1}{3}",
                "<b>(B) TRUE</b>: P(min &gt; t) = e<super>−t</super>e<super>−2t</super> = e<super>−3t</super>, mean 1/3.",
                "<b>(C) TRUE</b>: max + min = T<sub>1</sub> + T<sub>2</sub>, so",
                r"$$E[\max]=E[T_1]+E[T_2]-E[\min]=1+\dfrac{1}{2}-\dfrac{1}{3}=\dfrac{7}{6}",
                "<b>(D) FALSE</b>: by memorylessness P(T<sub>1</sub> &gt; 2 | T<sub>1</sub> &gt; 1) = "
                "P(T<sub>1</sub> &gt; 1) = e<super>−1</super>.",
                ("note", "max + min = sum of the two — the fastest way to E[max] for any pair.", "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Naive Bayes classifier (Bayes theorem)", difficulty="Hard",
            text="A spam filter assumes word occurrences are conditionally independent given the class. Prior: "
                 "P(spam) = 0.3. The word 'free' appears in 40% of spam and 5% of ham e-mails; the word "
                 "'meeting' appears in 2% of spam and 20% of ham e-mails. An e-mail contains 'free' but does "
                 "NOT contain 'meeting'. The posterior probability that it is spam is ______ "
                 "(round off to 3 decimal places).",
            answer=f"{_q25:.3f}", range=(0.806, 0.809),
            solution=[
                "<b>Concept:</b> Bayes theorem with a likelihood that factorises over features (conditional "
                "independence); absent words contribute (1 − p).",
                r"$$P(x\mid S)=0.40\times(1-0.02)=0.392,\qquad P(x\mid H)=0.05\times(1-0.20)=0.040",
                r"$$P(S\mid x)=\dfrac{0.3(0.392)}{0.3(0.392)+0.7(0.040)}=\dfrac{0.1176}{0.1176+0.028}",
                r"$$=\dfrac{0.1176}{0.1456}\approx " + f"{_q25:.4f}",
                "If you ignored the absent word 'meeting' you would get 0.12/(0.12 + 0.035) = 0.774 — wrong.",
                ("note", "Absence of a word is evidence too: it multiplies the likelihood by (1 − p<sub>word</sub>).",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Conditional distributions; correlation", difficulty="Hard",
            text="X ∼ Uniform(0, 6) and, given X = x, Y ∼ N(x, 1). The correlation coefficient between X and Y is",
            options=["1/2", "√3/2", "3/4", "1/√3"],
            answer="B",
            solution=[
                "<b>Concept:</b> use total variance for Var(Y) and Cov(X, Y) = Cov(X, E[Y | X]).",
                r"$$\text{Var}(X)=\dfrac{6^2}{12}=3,\qquad E[Y\mid X]=X,\quad \text{Var}(Y\mid X)=1",
                r"$$\text{Var}(Y)=E[1]+\text{Var}(X)=1+3=4",
                r"$$\text{Cov}(X,Y)=E[XY]-E[X]E[Y]=E[X\,E[Y\mid X]]-E[X]^2=\text{Var}(X)=3",
                r"$$\rho=\dfrac{3}{\sqrt{3}\cdot 2}=\dfrac{\sqrt{3}}{2}\approx 0.866",
                "(C) 3/4 is ρ<super>2</super> (the fraction of Var Y explained by X) — the square root was forgotten; "
                "(A) would need Var(Y) = 12, and (D) would need Var(Y) = 9 — both come from mis-adding the conditional and between-group variances.",
                ("note", "When Y = X + noise, ρ<super>2</super> = signal variance / total variance = 3/4, so ρ = √3/2.",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Mean, median and mode of a continuous distribution", difficulty="Hard",
            text="X has pdf f(x) = x e<super>−x</super> for x &gt; 0. Which of the following correctly describes "
                 "its mode, median and mean?",
            options=[f"mode = 1 &lt; median ≈ {_q27_med:.2f} &lt; mean = 2",
                     "mode = 1 &lt; mean = 2 &lt; median ≈ 2.20",
                     "median ≈ 1.39 &lt; mode = 1.5 &lt; mean = 2",
                     "mode = median = mean = 2"],
            answer="A",
            solution=[
                "<b>Concept:</b> mode maximises f; median solves F(m) = 1/2; mean = ∫x f(x) dx.",
                "Mode: f′(x) = e<super>−x</super>(1 − x) = 0 ⇒ x = 1.",
                r"$$E[X]=\int_0^\infty x^2e^{-x}\,dx=2!=2",
                "CDF by integration by parts:",
                r"$$F(x)=\int_0^x te^{-t}\,dt=1-(1+x)e^{-x}",
                r"$$F(m)=\dfrac{1}{2}\ \Rightarrow\ (1+m)e^{-m}=\dfrac{1}{2}\ \Rightarrow\ m\approx " + f"{_q27_med:.3f}",
                "Check: (1 + 1.678)e<super>−1.678</super> = 2.678 × 0.1867 ≈ 0.500.",
                ("fig", fig_q27),
                "Right-skewed ⇒ mode &lt; median &lt; mean, as in (A).",
                ("note", "Empirical rule for moderately skewed distributions: mean − mode ≈ 3(mean − median): "
                         "here 1 vs 3(0.32) = 0.97.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="t confidence interval from raw sums", difficulty="Hard",
            text="API response times (ms) of n = 16 randomly sampled requests give ∑x<sub>i</sub> = 1920 and "
                 "∑x<sub>i</sub><super>2</super> = 231 540. Assuming normality, the WIDTH (upper minus lower "
                 "limit) of the 95% confidence interval for the mean response time is ______ ms "
                 "(round off to 2 decimal places). Use t<sub>0.025,15</sub> = 2.131.",
            answer=f"{_q28:.2f}", range=(9.25, 9.33),
            solution=[
                "<b>Concept:</b> σ unknown, normal data ⇒ x̄ ± t<sub>α/2,n−1</sub> s/√n with s computed with "
                "divisor n − 1.",
                r"$$\bar{x}=\dfrac{1920}{16}=120",
                r"$$s^2=\dfrac{\sum x_i^2-n\bar{x}^2}{n-1}=\dfrac{231540-16(14400)}{15}=\dfrac{1140}{15}=76",
                r"$$s=\sqrt{76}=" + f"{_s28:.4f}" + r",\qquad \dfrac{s}{\sqrt{n}}=\dfrac{" + f"{_s28:.4f}" + r"}{4}=" + f"{_s28 / 4:.4f}",
                r"$$\text{Width}=2(2.131)(" + f"{_s28 / 4:.4f}" + r")\approx " + f"{_q28:.2f}",
                "The interval itself is 120 ± 4.64, i.e. (115.36, 124.64).",
                "Using z = 1.96 instead of t would give 8.54 — too narrow; using divisor n would give s = √71.25.",
                ("note", "The question asks for the WIDTH (2 × margin), not the margin — a frequent "
                         "point-loser.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Sampling distributions & Chi-squared / t tests", difficulty="Hard",
            text="Which of the following statements is/are TRUE?",
            options=["For a χ<super>2</super> test of independence on a 3 × 4 contingency table, the degrees of freedom are 6",
                     "A Pearson χ<super>2</super> goodness-of-fit statistic can be negative when observed counts are below expected counts",
                     "For a random sample of size n from N(μ, σ<super>2</super>), (n − 1)S<super>2</super>/σ<super>2</super> ∼ χ<super>2</super><sub>n−1</sub>",
                     "For n = 10 the two-sided 5% critical value of the one-sample t-test exceeds 1.96"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> df for r × c independence = (r − 1)(c − 1); sample variance of normal data is "
                "scaled χ<super>2</super>; t critical values exceed z critical values.",
                "<b>(A) TRUE</b>: (3 − 1)(4 − 1) = 6.",
                "<b>(B) FALSE</b>: each term (O − E)<super>2</super>/E ≥ 0, so χ<super>2</super> ≥ 0 always.",
                "<b>(C) TRUE</b>: standard result (Cochran); one df is lost because X̄ estimates μ.",
                "<b>(D) TRUE</b>: t<sub>0.025,9</sub> = 2.262 &gt; 1.96.",
                ("note", "χ<super>2</super> tests are always right-tailed: large values signal disagreement in either "
                         "direction.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Combinatorial probability (card game)", difficulty="Hard",
            text="Five cards are dealt from a well-shuffled standard deck of 52. The probability of getting "
                 "exactly 'two pairs' (two cards of one rank, two cards of another rank, and a fifth card of a "
                 "third rank) is closest to",
            options=[f"{_q30:.4f}", f"{2 * _q30:.4f}", f"{_q30 / 2:.4f}", "0.0211"],
            answer="A",
            solution=[
                "<b>Concept:</b> count by choosing ranks first (unordered when the roles are identical), then suits.",
                "Choose the 2 pair-ranks: C(13, 2) — unordered, because both pairs play the same role.",
                "Suits for each pair: C(4, 2) each. Fifth card: any of 11 remaining ranks × 4 suits = 44.",
                r"$$N=\binom{13}{2}\binom{4}{2}^2(44)=78\times 36\times 44=" + f"{_q30_fav}",
                r"$$P=\dfrac{" + f"{_q30_fav}" + r"}{\binom{52}{5}}=\dfrac{" + f"{_q30_fav}" + r"}{2598960}\approx " + f"{_q30:.4f}",
                "(B) chooses the pair ranks as 13 × 12 (ordered), double counting; 0.0211 is three-of-a-kind.",
                ("note", "Ask: are the chosen ranks interchangeable? Two pairs — yes (combination). Full house "
                         "(triple + pair) — no (13 × 12).", "Trap"),
            ],
        ),
    ],
}
