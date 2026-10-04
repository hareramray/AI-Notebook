"""Mock Test 01 — Foundation Full-Syllabus Test I (warm-up level, whole syllabus)."""
from fractions import Fraction as Fr
from math import comb, exp, factorial, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ----------------------------------------------------------------- computed answers
# Q1 circular seating, 6 people, A and B not adjacent
Q1_total = factorial(5)
Q1_tog = 2 * factorial(4)
Q1_ans = Q1_total - Q1_tog                     # 72

# Q4 dice: P(sum 8 | at least one 5)
_cond = [(a, b) for a in range(1, 7) for b in range(1, 7) if 5 in (a, b)]
Q4 = Fr(sum(1 for a, b in _cond if a + b == 8), len(_cond))   # 2/11

# Q6 binomial
Q6 = 5 * 0.1 * 0.9 ** 4                         # 0.32805

# Q8 Poisson
Q8 = 1 - exp(-2)                                # 0.8647

# Q11 normal
Q11 = stats.norm.sf(1.5)                        # 0.0668

# Q13 committee
Q13_fav = comb(5, 2) * comb(6, 2) + comb(5, 3) * comb(6, 1) + comb(5, 4)
Q13 = Fr(Q13_fav, comb(11, 4))                 # 215/330

# Q14 Bayes, machines
_pri = [0.5, 0.3, 0.2]
_def = [0.02, 0.03, 0.05]
Q14_tot = sum(p * d for p, d in zip(_pri, _def))
Q14 = _pri[2] * _def[2] / Q14_tot              # 0.3448

# Q16 joint PMF covariance
J16 = np.array([[0.10, 0.20, 0.10], [0.15, 0.15, 0.30]])
_xv, _yv = np.array([0, 1]), np.array([0, 1, 2])
Q16_EX = (J16.sum(1) * _xv).sum()
Q16_EY = (J16.sum(0) * _yv).sum()
Q16_EXY = sum(J16[i, j] * _xv[i] * _yv[j] for i in range(2) for j in range(3))
Q16 = Q16_EXY - Q16_EX * Q16_EY               # 0.06

# Q17 total variance (die then coins)
_N = np.arange(1, 7)
Q17_E = Fr(7, 2) / 2
Q17 = Fr(7, 2) / 4 + Fr(35, 12) / 4          # 77/48

# Q19 P(X+Y<=1), f = x+y on unit square  -> 1/3
Q19 = Fr(1, 3)

# Q21 correlation
X21 = np.array([2, 4, 6, 8, 10]); Y21 = np.array([3, 7, 5, 10, 12])
Sxy21 = ((X21 - X21.mean()) * (Y21 - Y21.mean())).sum()
Sxx21 = ((X21 - X21.mean()) ** 2).sum(); Syy21 = ((Y21 - Y21.mean()) ** 2).sum()
Q21 = Sxy21 / sqrt(Sxx21 * Syy21)              # 0.910

# Q23 CLT
Q23 = stats.norm.sf((54 - 50) / (15 / 6))      # 0.0548
Q23_wrong = stats.norm.sf(4 / 15)

# Q24 t CI
Q24 = 50.2 + 2.064 * 0.5 / 5                   # 50.4064

# Q26 t statistic
Q26_t = (67.3 - 64) / (5.8 / sqrt(10))         # 1.799

# Q27 chi-square GOF
O27 = [15, 25, 18, 22, 16, 24]
Q27 = sum((o - 20) ** 2 / 20 for o in O27)      # 4.5

# Q29 acceptance sampling
Q29 = 0.95 ** 10 + 10 * 0.05 * 0.95 ** 9        # 0.9139


# ----------------------------------------------------------------- figures
def fig_venn_q2():
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.add_patch(plt.Rectangle((-2.6, -1.5), 5.6, 3.0, fill=False, color="0.4"))
    ax.add_patch(Circle((-0.55, 0), 1.2, color=BLUE, alpha=0.30))
    ax.add_patch(Circle((0.85, 0), 1.2, color=MAROON, alpha=0.30))
    ax.text(-1.15, 0, "0.3", ha="center", va="center", fontsize=12)
    ax.text(0.15, 0, "0.3", ha="center", va="center", fontsize=12)
    ax.text(1.45, 0, "0.2", ha="center", va="center", fontsize=12)
    ax.text(2.55, -1.2, "0.2", ha="center", fontsize=11)
    ax.text(-1.4, 1.15, "A (Sat)", color=BLUE, fontsize=10)
    ax.text(1.5, 1.15, "B (Sun)", color=MAROON, fontsize=10)
    ax.set_xlim(-2.7, 3.1); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Exactly one = 0.3 + 0.2 = 0.5", fontsize=10)
    return fig


def fig_dot_q5():
    data = [12, 15, 15, 15, 18, 20, 22, 25]
    fig, ax = plt.subplots(figsize=(5.4, 2.2))
    seen = {}
    for v in data:
        seen[v] = seen.get(v, 0) + 1
        ax.plot(v, seen[v], "o", color=BLUE, ms=9)
    for val, lab, col in [(15, "mode 15", GOLD), (16.5, "median 16.5", MAROON), (17.75, "mean 17.75", BLUE)]:
        ax.axvline(val, color=col, lw=1.6, ls="--")
        ax.text(val + 0.15, 3.4, lab, color=col, fontsize=8.5, rotation=90, va="top")
    ax.set_ylim(0, 3.6); ax.set_yticks([]); ax.set_xlabel("score")
    ax.set_title("Right tail pulls the mean up", fontsize=10)
    return fig


def fig_normal_q11():
    x = np.linspace(25, 95, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.norm.pdf(x, 60, 10), color=BLUE)
    m = x >= 75
    ax.fill_between(x[m], stats.norm.pdf(x[m], 60, 10), color=MAROON, alpha=0.4)
    ax.axvline(60, color="0.5", lw=0.8, ls=":")
    ax.annotate("P(X > 75) = ?", xy=(79, 0.006), xytext=(80, 0.025), arrowprops=dict(arrowstyle="->"))
    ax.set_yticks([]); ax.set_xlabel("score x  (μ = 60, σ = 10)")
    return fig


def fig_tree_q14():
    fig, ax = plt.subplots(figsize=(6, 3.0))
    ax.axis("off")
    ys = [2.4, 1.2, 0.0]
    names = ["M1 (0.5)", "M2 (0.3)", "M3 (0.2)"]
    leaves = ["D: 0.02 → 0.010", "D: 0.03 → 0.009", "D: 0.05 → 0.010"]
    for y, n, l in zip(ys, names, leaves):
        ax.plot([0, 1.4], [1.2, y], color=BLUE)
        ax.text(1.45, y, n, va="center", fontsize=9.5, color=BLUE)
        ax.plot([2.6, 3.8], [y, y + 0.25], color=MAROON)
        ax.plot([2.6, 3.8], [y, y - 0.25], color="0.6")
        ax.text(3.85, y + 0.25, l, va="center", fontsize=9, color=MAROON)
        ax.text(3.85, y - 0.25, "not D", va="center", fontsize=8.5, color="0.5")
    ax.plot(0, 1.2, "o", color="k")
    ax.text(3.5, -0.75, "P(D) = 0.029;  P(M3 | D) = 0.010 / 0.029", fontsize=9.5)
    ax.set_xlim(-0.1, 6.0); ax.set_ylim(-0.95, 2.8)
    return fig


def fig_heat_q16():
    fig, ax = plt.subplots(figsize=(4.8, 2.4))
    ax.imshow(J16, cmap="Blues", vmin=0, vmax=0.4)
    for i in range(2):
        for j in range(3):
            ax.text(j, i, f"{J16[i, j]:.2f}", ha="center", va="center", fontsize=11)
    ax.set_xticks(range(3)); ax.set_xticklabels(["Y=0", "Y=1", "Y=2"])
    ax.set_yticks(range(2)); ax.set_yticklabels(["X=0", "X=1"])
    ax.set_title("Cells contributing to E[XY]: X=1 row only", fontsize=9.5)
    for s in ax.spines.values():
        s.set_visible(False)
    return fig


def fig_region_q18():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.fill([0, 1, 1], [0, 0, 1], color=BLUE, alpha=0.25)
    ax.plot([0, 1], [0, 1], color=BLUE)
    ax.plot([0.6, 0.6], [0, 0.6], color=MAROON, lw=3)
    ax.text(0.62, 0.25, "given X = 0.6:\nY ~ U(0, 0.6)", color=MAROON, fontsize=9)
    ax.text(0.7, 0.05, "f = 2", fontsize=10)
    ax.text(0.25, 0.45, "y = x", color=BLUE, fontsize=9, rotation=33)
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_aspect("equal")
    return fig


def fig_region_q19():
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="0.4")
    ax.fill([0, 1, 0], [0, 0, 1], color=GOLD, alpha=0.5)
    ax.plot([0, 1], [1, 0], color=MAROON)
    ax.text(0.15, 0.2, "x + y ≤ 1", fontsize=10)
    ax.text(0.55, 0.75, "f = x + y", fontsize=10, color=BLUE)
    ax.set_xlim(-0.05, 1.1); ax.set_ylim(-0.05, 1.1); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_aspect("equal")
    return fig


def fig_sq_q20():
    rng = np.random.default_rng(1)
    x = rng.uniform(-1, 1, 150)
    fig, ax = plt.subplots(figsize=(5.0, 2.6))
    ax.scatter(x, x ** 2, s=10, color=BLUE)
    ax.set_xlabel("X ~ U(−1, 1)"); ax.set_ylabel("Y = X²")
    ax.set_title("Cov(X, Y) = 0, yet Y is a function of X", fontsize=9.5)
    return fig


def fig_scatter_q21():
    fig, ax = plt.subplots(figsize=(5.0, 2.7))
    ax.scatter(X21, Y21, color=MAROON, s=35, zorder=3)
    b = Sxy21 / Sxx21
    xx = np.linspace(1, 11, 10)
    ax.plot(xx, Y21.mean() + b * (xx - X21.mean()), color=BLUE, lw=1.4)
    ax.set_xlabel("rainfall x (cm)"); ax.set_ylabel("yield y")
    ax.set_title(f"r ≈ {Q21:.2f}: strong positive linear trend", fontsize=9.5)
    return fig


def fig_cdf_q22():
    pts = [(1, 0.2), (2, 0.5), (4, 0.9), (5, 1.0)]
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    prev_x, prev_F = -0.5, 0.0
    for x, F in pts:
        ax.plot([prev_x, x], [prev_F, prev_F], color=BLUE, lw=2)
        ax.plot(x, prev_F, "o", mfc="white", color=BLUE)
        ax.plot(x, F, "o", color=BLUE)
        prev_x, prev_F = x, F
    ax.plot([5, 6.5], [1, 1], color=BLUE, lw=2)
    ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.05, 1.1)
    ax.set_yticks([0, 0.2, 0.5, 0.9, 1.0]); ax.set_xlabel("x"); ax.set_ylabel("F(x)")
    ax.grid(alpha=0.3)
    return fig


def fig_clt_q23():
    x = np.linspace(40, 60, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.norm.pdf(x, 50, 15), color="0.55", ls="--", label="one reading (σ = 15)")
    ax.plot(x, stats.norm.pdf(x, 50, 2.5), color=BLUE, label="X̄, n = 36 (SE = 2.5)")
    m = x >= 54
    ax.fill_between(x[m], stats.norm.pdf(x[m], 50, 2.5), color=MAROON, alpha=0.4)
    ax.legend(fontsize=8, frameon=False); ax.set_yticks([]); ax.set_xlabel("mm")
    return fig


def fig_reject_q25():
    z = np.linspace(-3.6, 3.6, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(z, stats.norm.pdf(z), color=BLUE)
    m = z <= -1.645
    ax.fill_between(z[m], stats.norm.pdf(z[m]), color=MAROON, alpha=0.4)
    ax.axvline(-2.2, color=GOLD, lw=2.2)
    ax.text(-2.15, 0.30, "z = −2.20", fontsize=9)
    ax.text(-3.5, 0.12, "reject\n(α = 0.05)", color=MAROON, fontsize=8.5)
    ax.text(-1.60, 0.02, "−1.645", fontsize=8)
    ax.set_yticks([]); ax.set_xlabel("z")
    return fig


def fig_t_q26():
    t = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(t, stats.t.pdf(t, 9), color=BLUE)
    m = t >= 1.833
    ax.fill_between(t[m], stats.t.pdf(t[m], 9), color=MAROON, alpha=0.4)
    ax.axvline(Q26_t, color=GOLD, lw=2.2)
    ax.text(Q26_t - 1.6, 0.33, f"t = {Q26_t:.2f}", fontsize=9)
    ax.text(2.0, 0.08, "reject: t ≥ 1.833", color=MAROON, fontsize=8.5)
    ax.set_yticks([]); ax.set_xlabel("t (9 df)")
    return fig


def fig_chi_q27():
    x = np.linspace(0, 20, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.chi2.pdf(x, 5), color=BLUE)
    m = x >= 11.07
    ax.fill_between(x[m], stats.chi2.pdf(x[m], 5), color=MAROON, alpha=0.4)
    ax.axvline(Q27, color=GOLD, lw=2.2)
    ax.text(Q27 + 0.3, 0.13, "χ² = 4.5", fontsize=9)
    ax.text(12, 0.03, "reject: χ² ≥ 11.07", color=MAROON, fontsize=8.5)
    ax.set_yticks([]); ax.set_xlabel("χ² (5 df)")
    return fig


def fig_t_vs_z_q28():
    x = np.linspace(-4.5, 4.5, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.norm.pdf(x), color=BLUE, label="N(0,1)")
    ax.plot(x, stats.t.pdf(x, 2), color=MAROON, label="t, 2 df")
    ax.plot(x, stats.t.pdf(x, 8), color=GOLD, label="t, 8 df")
    ax.legend(fontsize=8, frameon=False); ax.set_yticks([])
    ax.set_title("Lower peak, heavier tails; t → N(0,1) as df grows", fontsize=9.5)
    return fig


# ----------------------------------------------------------------- the set
SET = {
    "title": "Foundation Full-Syllabus Test I",
    "subtitle": "Warm-up paper covering the entire GATE DA Probability & Statistics syllabus "
                "through classic contexts: dice, coins, urns, committees, quality control, exam scores "
                "and rainfall.",
    "focus": "Every syllabus head appears at least once: counting (circular seating, committees), axioms and "
             "Venn reasoning, independence vs mutual exclusivity, conditional probability with dice and urns, "
             "Bayes theorem (tree), joint/marginal/conditional PMFs and PDFs, law of total variance, "
             "mean/median/mode, covariance and correlation, Bernoulli/binomial/discrete uniform, Poisson, "
             "uniform/exponential/normal, CDF reading, CLT, t-interval, z-test, t-test and a χ² "
             "goodness-of-fit test. Five concept-check MSQs test properties of independence, CDFs, variance, "
             "correlation and the t/χ² families.",
    "minutes": 90,
    "questions": [
        # ------------------------------------------------------------ Q1
        dict(
            qtype="MCQ", marks=1, topic="Counting: circular arrangements", difficulty="Easy",
            text="Six friends, including Asha and Bimal, sit around a circular table (only relative positions "
                 "matter). The number of seating arrangements in which Asha and Bimal do <b>not</b> sit next "
                 "to each other is",
            options=["72", "48", "120", "480"],
            answer="A",
            solution=[
                "<b>Concept:</b> n distinct people can sit around a circle in (n − 1)! ways; count the complement "
                "(A and B together) by gluing them into one block.",
                "Total circular arrangements of 6 people:",
                r"$$\text{Total}=(6-1)!=5!=120",
                "Treat Asha–Bimal as one block: 5 units around a circle, and the block can be internally ordered "
                "in 2 ways:",
                r"$$\text{Together}=(5-1)!\times 2!=24\times 2=48",
                r"$$\text{Not together}=120-48=%d" % Q1_ans,
                "<b>Why not the others?</b> 48 is the 'together' count; 120 is the total; 480 = 6! − 2·5! is the "
                "answer for a straight row, not a circle.",
                ("note", "In a circle, fix one person's seat to kill rotational symmetry — that is where (n − 1)! "
                         "comes from. Always use the complement for 'not together'.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q2
        dict(
            qtype="MCQ", marks=1, topic="Probability axioms, union", difficulty="Easy",
            text="For a weekend, let A = 'it rains on Saturday' and B = 'it rains on Sunday'. Suppose "
                 "P(A) = 0.6, P(B) = 0.5 and P(A ∪ B) = 0.8. The probability that it rains on <b>exactly one</b> "
                 "of the two days is",
            options=["0.5", "0.3", "0.2", "0.8"],
            answer="A",
            solution=[
                "<b>Concept:</b> Inclusion–exclusion gives P(A ∩ B); 'exactly one' = union minus intersection.",
                r"$$P(A\cap B)=P(A)+P(B)-P(A\cup B)=0.6+0.5-0.8=0.3",
                r"$$P(\text{exactly one})=P(A\cup B)-P(A\cap B)=0.8-0.3=0.5",
                "Equivalently P(A only) + P(B only) = (0.6 − 0.3) + (0.5 − 0.3) = 0.3 + 0.2 = 0.5.",
                ("fig", fig_venn_q2),
                "Option (B) 0.3 is P(both); (C) 0.2 is P(neither) = 1 − 0.8; (D) 0.8 is P(at least one).",
                ("note", "Fill a Venn diagram from the inside out: intersection first, then the 'only' "
                         "regions, then the outside.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q3
        dict(
            qtype="MSQ", marks=1, topic="Independence vs mutual exclusivity (concept check)", difficulty="Easy",
            text="Let A and B be events in a probability space. Which of the following statements is/are "
                 "<b>always TRUE</b>?",
            options=["If P(A) &gt; 0, P(B) &gt; 0 and A, B are mutually exclusive, then A and B are NOT independent.",
                     "If A and B are independent, then A and B<super>c</super> are independent.",
                     "If P(A ∩ B) = 0, then A and B are independent.",
                     "An event A with P(A) = 1 is independent of every event B."],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> Independence means P(A ∩ B) = P(A)P(B); mutual exclusivity means A ∩ B = Ø.",
                "<b>(A) TRUE.</b> Mutually exclusive ⇒ P(A ∩ B) = 0, but P(A)P(B) &gt; 0. The product rule fails, "
                "so they are dependent (knowing A happened tells you B did not).",
                "<b>(B) TRUE.</b>",
                r"$$P(A\cap B^c)=P(A)-P(A\cap B)=P(A)-P(A)P(B)=P(A)\,P(B^c)",
                "<b>(C) FALSE.</b> Counter-example with one die: A = {1}, B = {2}. P(A ∩ B) = 0 but "
                "P(A)P(B) = 1/36 ≠ 0. (It would be true only if P(A) = 0 or P(B) = 0.)",
                "<b>(D) TRUE.</b> P(A<super>c</super> ∩ B) ≤ P(A<super>c</super>) = 0, so "
                "P(A ∩ B) = P(B) − 0 = P(B) = 1 · P(B) = P(A)P(B).",
                ("note", "Mutually exclusive events with positive probabilities are the <i>most</i> dependent "
                         "events possible — never confuse 'disjoint' with 'independent'.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q4
        dict(
            qtype="NAT", marks=1, topic="Conditional probability (dice)", difficulty="Easy",
            text="Two fair six-sided dice are rolled. Given that at least one die shows a 5, the probability "
                 "that the sum of the two faces is 8 is ______ (round off to 2 decimal places).",
            answer=f"{float(Q4):.2f}", range=(0.18, 0.19),
            solution=[
                "<b>Concept:</b> With equally likely outcomes, P(E | C) = |E ∩ C| / |C| — the condition shrinks "
                "the sample space.",
                "Outcomes with at least one 5: 6 with first die 5, 6 with second die 5, minus (5,5) counted twice:",
                r"$$|C|=6+6-1=11",
                "Among these, sum 8 needs the other die to show 3: (5,3) and (3,5).",
                r"$$P(\text{sum}=8\mid C)=\dfrac{2}{11}\approx %.4f" % float(Q4),
                f"Answer ≈ <b>{float(Q4):.2f}</b>.",
                ("note", "Unconditionally P(sum = 8) = 5/36 ≈ 0.139. Conditioning on a 5 removes (2,6), (6,2), "
                         "(4,4) and raises the chance — always rebuild the reduced sample space.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q5
        dict(
            qtype="MCQ", marks=1, topic="Mean, median, mode", difficulty="Easy",
            text="The marks (out of 30) of eight students in a quiz are: 12, 15, 15, 18, 20, 22, 15, 25. "
                 "Which ordering of the mean, median and mode is correct?",
            options=["mean &lt; median &lt; mode", "mode &lt; median &lt; mean",
                     "median &lt; mode &lt; mean", "mean = median = mode"],
            answer="B",
            solution=[
                "<b>Concept:</b> Sort the data; median = average of the two middle values for even n; mode = most "
                "frequent value.",
                "Sorted: 12, 15, 15, 15, 18, 20, 22, 25.",
                r"$$\bar{x}=\dfrac{12+15+15+15+18+20+22+25}{8}=\dfrac{142}{8}=17.75",
                r"$$\text{median}=\dfrac{x_{(4)}+x_{(5)}}{2}=\dfrac{15+18}{2}=16.5,\qquad \text{mode}=15",
                "So 15 &lt; 16.5 &lt; 17.75: mode &lt; median &lt; mean.",
                ("fig", fig_dot_q5),
                ("note", "For right-skewed data (long upper tail) the usual pattern is mode &lt; median &lt; mean; "
                         "the mean is the measure most affected by extreme values.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q6
        dict(
            qtype="MCQ", marks=1, topic="Binomial distribution", difficulty="Easy",
            text="A machine produces bolts, each defective independently with probability 0.1. In a random sample "
                 "of 5 bolts, the probability that exactly one is defective is closest to",
            options=["0.066", "0.328", "0.410", "0.590"],
            answer="B",
            solution=[
                "<b>Concept:</b> Number of defectives X ∼ Bin(n = 5, p = 0.1), "
                "P(X = k) = C(n, k) p<super>k</super>(1 − p)<super>n−k</super>.",
                r"$$P(X=1)=\binom{5}{1}(0.1)^1(0.9)^4=5\times 0.1\times 0.6561=%.5f" % Q6,
                "<b>Distractors:</b> 0.066 ≈ 0.1 × 0.9<super>4</super> forgets the factor C(5,1) = 5; 0.590 = 0.9<super>5</super> = P(X = 0); "
                "0.410 = 1 − 0.9<super>5</super> = P(X ≥ 1).",
                ("note", "Do not forget the binomial coefficient: the single defective can be any one of the "
                         "5 positions.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q7
        dict(
            qtype="MSQ", marks=1, topic="Properties of a CDF (concept check)", difficulty="Easy",
            text="Let F be the cumulative distribution function of a random variable X, i.e. F(x) = P(X ≤ x). "
                 "Which of the following is/are TRUE for <b>every</b> random variable X?",
            options=["F is non-decreasing.",
                     "F is right-continuous.",
                     "P(X = a) = F(a) − F(a<super>−</super>), where F(a<super>−</super>) is the left limit at a.",
                     "P(a &lt; X &lt; b) = F(b) − F(a) for all a &lt; b."],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> A CDF is non-decreasing, right-continuous, with limits 0 at −∞ and 1 at +∞; jumps "
                "equal point masses.",
                "<b>(A) TRUE.</b> For x &lt; y, {X ≤ x} ⊂ {X ≤ y}, so F(x) ≤ F(y).",
                "<b>(B) TRUE.</b> {X ≤ x + 1/n} decreases to {X ≤ x}; continuity of probability gives "
                "F(x + 1/n) → F(x).",
                "<b>(C) TRUE.</b> F(a) − F(a<super>−</super>) = P(X ≤ a) − P(X &lt; a) = P(X = a).",
                "<b>(D) FALSE.</b> F(b) − F(a) = P(a &lt; X ≤ b), which includes the point b. If X has a "
                "point mass at b (e.g. X = number on a die, b = 3), the two sides differ by P(X = b).",
                ("note", "For a continuous X all four interval types (a,b), [a,b], (a,b], [a,b) have the same "
                         "probability — but for discrete X the endpoints matter.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q8
        dict(
            qtype="NAT", marks=1, topic="Poisson distribution", difficulty="Easy",
            text="The number of thunderstorms in a district during July follows a Poisson distribution with mean 2. "
                 "The probability that the district experiences at least one thunderstorm in July is ______ "
                 "(round off to 2 decimal places).",
            answer=f"{Q8:.2f}", range=(0.86, 0.87),
            solution=[
                "<b>Concept:</b> For X ∼ Poisson(λ), P(X = k) = e<super>−λ</super>λ<super>k</super>/k!; use the "
                "complement for 'at least one'.",
                r"$$P(X\geq 1)=1-P(X=0)=1-e^{-2}=1-0.1353=%.4f" % Q8,
                f"Answer ≈ <b>{Q8:.2f}</b>.",
                ("note", "'At least one' ⇒ 1 − P(none). Summing P(1) + P(2) + … directly is endless for "
                         "Poisson.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q9
        dict(
            qtype="MCQ", marks=1, topic="Continuous uniform, conditional probability", difficulty="Easy",
            text="The daily rainfall X (in mm) at a hill station on a rainy day is modelled as uniform on [2, 10]. "
                 "Given that the rainfall on a day exceeds 4 mm, the probability that it exceeds 7 mm is",
            options=["0.375", "0.500", "0.625", "0.750"],
            answer="B",
            solution=[
                "<b>Concept:</b> For X ∼ U(a, b), probabilities are proportional to lengths; conditioning on an "
                "interval gives another uniform.",
                r"$$P(X>7)=\dfrac{10-7}{10-2}=\dfrac{3}{8},\qquad P(X>4)=\dfrac{10-4}{8}=\dfrac{6}{8}",
                r"$$P(X>7\mid X>4)=\dfrac{P(X>7)}{P(X>4)}=\dfrac{3/8}{6/8}=0.5",
                "Shortcut: given X &gt; 4, X ∼ U(4, 10), so P(X &gt; 7) = 3/6 = 0.5.",
                "0.375 is the unconditional P(X &gt; 7); 0.750 is P(X &gt; 4); 0.625 = P(X &lt; 7).",
                ("note", "{X &gt; 7} ⊂ {X &gt; 4}, so the intersection in the numerator is just {X &gt; 7}.",
                 "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q10
        dict(
            qtype="MCQ", marks=1, topic="Exponential distribution, memorylessness", difficulty="Easy",
            text="The lifetime of a bulb is exponentially distributed with mean 400 hours. Given that a bulb has "
                 "already worked for 200 hours, the probability that it works for at least another 400 hours is",
            options=["e<super>−1</super>", "e<super>−1.5</super>", "e<super>−0.5</super>", "1 − e<super>−1</super>"],
            answer="A",
            solution=[
                "<b>Concept:</b> X ∼ Exp(λ) with mean 1/λ has P(X &gt; t) = e<super>−λt</super> and is memoryless: "
                "P(X &gt; s + t | X &gt; s) = P(X &gt; t).",
                r"$$\lambda=\dfrac{1}{400}\ \text{per hour}",
                r"$$P(X>600\mid X>200)=\dfrac{e^{-600/400}}{e^{-200/400}}=e^{-400/400}=e^{-1}\approx 0.368",
                "e<super>−1.5</super> is the unconditional P(X &gt; 600) (ignoring the condition); 1 − e<super>−1</super> "
                "is a failure probability.",
                ("note", "Memorylessness: a working exponential component is 'as good as new' — the 200 hours "
                         "already used are irrelevant.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q11
        dict(
            qtype="NAT", marks=1, topic="Normal distribution", difficulty="Easy",
            text=["Scores in a state-level exam are normally distributed with mean 60 and standard deviation 10. "
                  "The proportion of candidates scoring above 75 is ______ (round off to 4 decimal places). "
                  "[Use Φ(1.5) = 0.9332.]",
                  ("fig", fig_normal_q11)],
            answer=f"{Q11:.4f}", range=(0.0665, 0.0670),
            solution=[
                "<b>Concept:</b> Standardise: Z = (X − μ)/σ ∼ N(0, 1).",
                r"$$z=\dfrac{75-60}{10}=1.5",
                r"$$P(X>75)=P(Z>1.5)=1-\Phi(1.5)=1-0.9332=0.0668",
                f"Answer ≈ <b>{Q11:.4f}</b>.",
                ("note", "Upper-tail area = 1 − Φ(z). Reporting Φ(1.5) itself (0.9332) is the most common "
                         "slip.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q12
        dict(
            qtype="MSQ", marks=1, topic="Variance rules (concept check)", difficulty="Easy",
            text="Let X and Y be random variables with finite variances and let a, b be constants. Which of the "
                 "following is/are TRUE?",
            options=["Var(aX + b) = a<super>2</super> Var(X)",
                     "Var(X + Y) = Var(X) + Var(Y) for all X and Y",
                     "If X and Y are independent, Var(X − Y) = Var(X) + Var(Y)",
                     "Var(X) = E[X<super>2</super>] − (E[X])<super>2</super>"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> Var(X ± Y) = Var(X) + Var(Y) ± 2Cov(X, Y); shifting does not change spread; "
                "scaling by a multiplies variance by a².",
                "<b>(A) TRUE.</b> Var(aX + b) = E[(aX + b − aμ − b)<super>2</super>] = a<super>2</super>E[(X − μ)<super>2</super>].",
                "<b>(B) FALSE.</b> It needs Cov(X, Y) = 0. E.g. Y = X gives Var(2X) = 4Var(X) ≠ 2Var(X).",
                "<b>(C) TRUE.</b> Independence ⇒ Cov = 0, and Var(−Y) = (−1)<super>2</super>Var(Y):",
                r"$$\mathrm{Var}(X-Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)-2\,\mathrm{Cov}(X,Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)",
                "<b>(D) TRUE.</b> Expand E[(X − μ)<super>2</super>] = E[X<super>2</super>] − 2μE[X] + μ<super>2</super> "
                "= E[X<super>2</super>] − μ<super>2</super>.",
                ("note", "Variances ADD for X − Y as well as X + Y (independent case). Writing "
                         "Var(X) − Var(Y) is a classic error — it can even be negative!", "Trap"),
            ],
        ),
        # ============================================================ 2-mark
        # ------------------------------------------------------------ Q13
        dict(
            qtype="NAT", marks=2, topic="Counting: committees (hypergeometric)", difficulty="Medium",
            text="A committee of 4 is chosen at random from 6 men and 5 women, all selections being equally likely. "
                 "The probability that the committee contains at least 2 women is ______ (round off to 2 decimal "
                 "places).",
            answer=f"{float(Q13):.2f}", range=(0.65, 0.66),
            solution=[
                "<b>Concept:</b> Equally likely subsets ⇒ P = favourable / total; split 'at least 2' into disjoint "
                "cases (or use the complement).",
                r"$$\text{Total}=\binom{11}{4}=330",
                "Count each case (women, men):",
                ("table", [["Women", "Men", "Count"],
                           ["2", "2", "C(5,2)·C(6,2) = 10 × 15 = 150"],
                           ["3", "1", "C(5,3)·C(6,1) = 10 × 6 = 60"],
                           ["4", "0", "C(5,4) = 5"],
                           ["Total", "", f"{Q13_fav}"]]),
                r"$$P(\geq 2\ \text{women})=\dfrac{215}{330}=\dfrac{43}{66}\approx %.4f" % float(Q13),
                "Check by complement: 0 women: C(6,4) = 15; 1 woman: 5 × C(6,3) = 100; 1 − 115/330 = 215/330. (verified)",
                f"Answer ≈ <b>{float(Q13):.2f}</b>.",
                ("note", "Do NOT count 'choose 2 women, then any 2 of the remaining 9' = C(5,2)C(9,2) = 360 — "
                         "it counts committees with 3 or 4 women several times.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q14
        dict(
            qtype="MCQ", marks=2, topic="Bayes theorem (quality control)", difficulty="Medium",
            text="Three machines M1, M2, M3 produce 50%, 30% and 20% of a factory's output, with defective rates "
                 "2%, 3% and 5% respectively. An item picked at random is found to be defective. The probability "
                 "that it was produced by M3 is closest to",
            options=["0.200", "0.310", "0.345", "0.050"],
            answer="C",
            solution=[
                "<b>Concept:</b> Bayes theorem: posterior ∝ prior × likelihood; the denominator is the total "
                "probability of a defect.",
                ("fig", fig_tree_q14),
                "Total probability of a defect:",
                r"$$P(D)=0.5(0.02)+0.3(0.03)+0.2(0.05)=0.010+0.009+0.010=%.3f" % Q14_tot,
                "Bayes theorem:",
                r"$$P(M_3\mid D)=\dfrac{P(M_3)P(D\mid M_3)}{P(D)}=\dfrac{0.010}{0.029}\approx %.4f" % Q14,
                "0.200 is the prior P(M3) (ignores the evidence); 0.310 ≈ 0.009/0.029 is P(M2 | D); "
                "0.050 is P(D | M3) — the inverse conditional.",
                ("note", "Although M3 makes only 20% of items, it contributes about 34% of defects because its "
                         "defect rate is highest. Posterior shares always add to 1: "
                         "0.345 + 0.345 + 0.310 = 1.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q15
        dict(
            qtype="MCQ", marks=2, topic="Conditional probability (urn, without replacement)", difficulty="Medium",
            text="An urn contains 4 red and 6 blue balls. Two balls are drawn one after another without "
                 "replacement. Given that the <b>second</b> ball drawn is red, the probability that the "
                 "<b>first</b> ball drawn was red is",
            options=["1/3", "2/5", "4/9", "2/15"],
            answer="A",
            solution=[
                "<b>Concept:</b> P(R<sub>1</sub> | R<sub>2</sub>) = P(R<sub>1</sub> ∩ R<sub>2</sub>)/P(R<sub>2</sub>), "
                "with P(R<sub>2</sub>) from the law of total probability.",
                r"$$P(R_1\cap R_2)=\dfrac{4}{10}\cdot\dfrac{3}{9}=\dfrac{12}{90}",
                r"$$P(R_2)=\dfrac{4}{10}\cdot\dfrac{3}{9}+\dfrac{6}{10}\cdot\dfrac{4}{9}=\dfrac{12+24}{90}=\dfrac{36}{90}=\dfrac{2}{5}",
                r"$$P(R_1\mid R_2)=\dfrac{12/90}{36/90}=\dfrac{1}{3}",
                "Symmetry check: given ball 2 is red, ball 1 is a random draw from the other 9 balls, of which "
                "3 are red ⇒ 3/9 = 1/3. (verified)",
                "2/5 is P(R<sub>2</sub>) (equal to P(R<sub>1</sub>) by exchangeability); 4/9 is "
                "P(R<sub>2</sub> | B<sub>1</sub>); 2/15 = 12/90 is the joint probability.",
                ("note", "Draws without replacement are exchangeable: the 2nd ball is just as likely to be red as "
                         "the 1st. Conditioning 'backwards in time' is perfectly legitimate.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q16
        dict(
            qtype="NAT", marks=2, topic="Joint PMF, covariance", difficulty="Medium",
            text=["In a quality audit, X = 1 if a randomly chosen item comes from the night shift (0 otherwise) and "
                  "Y = number of minor flaws on the item. The joint PMF is:",
                  ("table", [["", "Y = 0", "Y = 1", "Y = 2"],
                             ["X = 0", "0.10", "0.20", "0.10"],
                             ["X = 1", "0.15", "0.15", "0.30"]]),
                  "Cov(X, Y) is ______ (round off to 2 decimal places)."],
            answer=f"{Q16:.2f}", range=(0.06, 0.06),
            solution=[
                "<b>Concept:</b> Cov(X, Y) = E[XY] − E[X]E[Y]; marginals come from row/column sums.",
                "Marginals: P(X = 1) = 0.15 + 0.15 + 0.30 = 0.6; P(Y = 0, 1, 2) = 0.25, 0.35, 0.40.",
                r"$$E[X]=0.6,\qquad E[Y]=0(0.25)+1(0.35)+2(0.40)=1.15",
                "Only cells with X = 1 and Y ≥ 1 contribute to E[XY]:",
                ("fig", fig_heat_q16),
                r"$$E[XY]=1\cdot 1\cdot 0.15+1\cdot 2\cdot 0.30=0.75",
                r"$$\mathrm{Cov}(X,Y)=0.75-0.6\times 1.15=0.75-0.69=%.2f" % Q16,
                "Positive covariance: night-shift items tend to carry more flaws "
                "(E[Y | X = 1] = 0.75/0.6 = 1.25 vs E[Y | X = 0] = 0.40/0.4 = 1.0).",
                ("note", "For a 0/1 variable X, Cov(X, Y) = P(X = 1)·(E[Y | X = 1] − E[Y]) = "
                         "0.6 × (1.25 − 1.15) = 0.06 — a fast cross-check.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q17
        dict(
            qtype="NAT", marks=2, topic="Conditional expectation and variance", difficulty="Medium",
            text="A fair die is rolled; if it shows N, a fair coin is then tossed N times. Let Y be the total number "
                 "of heads. Var(Y) is ______ (round off to 2 decimal places).",
            answer=f"{float(Q17):.2f}", range=(1.60, 1.61),
            solution=[
                "<b>Concept:</b> Law of total variance: Var(Y) = E[Var(Y | N)] + Var(E[Y | N]).",
                "Given N = n, Y ∼ Bin(n, 1/2):",
                r"$$E[Y\mid N]=\dfrac{N}{2},\qquad \mathrm{Var}(Y\mid N)=N\cdot\dfrac{1}{2}\cdot\dfrac{1}{2}=\dfrac{N}{4}",
                "For a fair die (discrete uniform on 1–6):",
                r"$$E[N]=\dfrac{7}{2},\qquad \mathrm{Var}(N)=\dfrac{6^2-1}{12}=\dfrac{35}{12}",
                "Combine:",
                r"$$E[\mathrm{Var}(Y\mid N)]=\dfrac{E[N]}{4}=\dfrac{7}{8}=0.875",
                r"$$\mathrm{Var}(E[Y\mid N])=\dfrac{\mathrm{Var}(N)}{4}=\dfrac{35}{48}\approx 0.7292",
                r"$$\mathrm{Var}(Y)=\dfrac{7}{8}+\dfrac{35}{48}=\dfrac{77}{48}\approx %.4f" % float(Q17),
                f"(Also E[Y] = E[N]/2 = {float(Q17_E)}.) Answer ≈ <b>{float(Q17):.2f}</b>.",
                ("note", "Using only E[Var(Y | N)] = 0.875 misses the extra spread caused by the random number of "
                         "tosses. Both pieces are needed.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q18
        dict(
            qtype="MCQ", marks=2, topic="Conditional PDF, conditional expectation", difficulty="Medium",
            text="The joint PDF of (X, Y) is f(x, y) = 2 for 0 &lt; y &lt; x &lt; 1 and 0 otherwise. The value of "
                 "E[Y | X = 0.6] is",
            options=["0.30", "0.333", "0.40", "0.60"],
            answer="A",
            solution=[
                "<b>Concept:</b> f<sub>Y|X</sub>(y | x) = f(x, y)/f<sub>X</sub>(x); then integrate y against it.",
                "Marginal of X (integrate over 0 &lt; y &lt; x):",
                r"$$f_X(x)=\int_0^x 2\,dy=2x,\qquad 0<x<1",
                r"$$f_{Y\mid X}(y\mid x)=\dfrac{2}{2x}=\dfrac{1}{x},\qquad 0<y<x",
                "So given X = x, Y ∼ U(0, x).",
                ("fig", fig_region_q18),
                r"$$E[Y\mid X=0.6]=\dfrac{0+0.6}{2}=0.30",
                "0.333 is the unconditional E[Y] = ∫∫ 2y = 1/3; 0.40 = 2(0.6)/3 comes from wrongly taking the conditional density ∝ y; 0.60 is x itself.",
                ("note", "A constant joint density on a region gives uniform conditionals along each slice — draw "
                         "the region and read off the slice.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q19
        dict(
            qtype="NAT", marks=2, topic="Joint PDF, probability over a region", difficulty="Medium",
            text="The joint PDF of (X, Y) is f(x, y) = x + y for 0 ≤ x ≤ 1, 0 ≤ y ≤ 1, and 0 elsewhere. "
                 "P(X + Y ≤ 1) is ______ (round off to 2 decimal places).",
            answer=f"{float(Q19):.2f}", range=(0.33, 0.34),
            solution=[
                "<b>Concept:</b> P((X, Y) ∈ R) = ∬<sub>R</sub> f(x, y) dy dx, with limits read from a sketch.",
                ("fig", fig_region_q19),
                "Region: 0 ≤ x ≤ 1, 0 ≤ y ≤ 1 − x.",
                r"$$P=\int_0^1\int_0^{1-x}(x+y)\,dy\,dx=\int_0^1\left[x(1-x)+\dfrac{(1-x)^2}{2}\right]dx",
                r"$$=\int_0^1\dfrac{(1-x)(1+x)}{2}\,dx=\dfrac{1}{2}\int_0^1(1-x^2)\,dx=\dfrac{1}{2}\cdot\dfrac{2}{3}=\dfrac{1}{3}",
                f"Answer ≈ <b>{float(Q19):.2f}</b>.",
                "Sanity check: the triangle is half the square, but density is smaller there (x + y ≤ 1) than in the "
                "other half, so the answer should be below 0.5. (verified)",
                ("note", "Area of the region (1/2) is NOT the probability unless the density is uniform.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q20
        dict(
            qtype="MSQ", marks=2, topic="Covariance and correlation (concept check)", difficulty="Medium",
            text="Let X and Y be random variables with positive, finite variances, and let ρ(X, Y) denote their "
                 "correlation coefficient. Which of the following is/are TRUE?",
            options=["−1 ≤ ρ(X, Y) ≤ 1",
                     "If Cov(X, Y) = 0, then X and Y are independent.",
                     "ρ(2X + 3, −Y) = −ρ(X, Y)",
                     "Cov(X, X) = Var(X)"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> ρ = Cov(X, Y)/(σ<sub>X</sub>σ<sub>Y</sub>) is scale-free, bounded by Cauchy–Schwarz, "
                "and flips sign when one variable is negated.",
                "<b>(A) TRUE.</b> Cauchy–Schwarz: |Cov(X, Y)| ≤ σ<sub>X</sub>σ<sub>Y</sub>.",
                "<b>(B) FALSE.</b> Zero covariance means no <i>linear</i> relation only. Example: X ∼ U(−1, 1), "
                "Y = X<super>2</super>: Cov = E[X<super>3</super>] − E[X]E[X<super>2</super>] = 0, yet Y is completely "
                "determined by X.",
                ("fig", fig_sq_q20),
                "<b>(C) TRUE.</b> Cov(2X + 3, −Y) = −2Cov(X, Y); SDs are 2σ<sub>X</sub> and σ<sub>Y</sub>:",
                r"$$\rho(2X+3,-Y)=\dfrac{-2\,\mathrm{Cov}(X,Y)}{2\sigma_X\,\sigma_Y}=-\rho(X,Y)",
                "<b>(D) TRUE.</b> Cov(X, X) = E[X<super>2</super>] − (E[X])<super>2</super> = Var(X).",
                ("note", "Independent ⇒ uncorrelated, but NOT conversely (the converse holds for jointly normal "
                         "variables).", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q21
        dict(
            qtype="MCQ", marks=2, topic="Sample correlation coefficient", difficulty="Medium",
            text=["Seasonal rainfall x (cm) and crop yield y (quintals/acre) on five farms are:",
                  ("table", [["x", "2", "4", "6", "8", "10"], ["y", "3", "7", "5", "10", "12"]]),
                  "The Pearson correlation coefficient between x and y is closest to"],
            options=["0.83", "0.91", "1.05", "0.47"],
            answer="B",
            solution=[
                "<b>Concept:</b> r = S<sub>xy</sub>/√(S<sub>xx</sub>S<sub>yy</sub>) with S<sub>xy</sub> = ∑(x − x̄)(y − ȳ).",
                "x̄ = 30/5 = 6, ȳ = 37/5 = 7.4.",
                ("table", [["x − x̄", "−4", "−2", "0", "2", "4"],
                           ["y − ȳ", "−4.4", "−0.4", "−2.4", "2.6", "4.6"],
                           ["product", "17.6", "0.8", "0", "5.2", "18.4"]]),
                r"$$S_{xy}=42,\quad S_{xx}=16+4+0+4+16=40",
                r"$$S_{yy}=19.36+0.16+5.76+6.76+21.16=53.2",
                r"$$r=\dfrac{42}{\sqrt{40\times 53.2}}=\dfrac{42}{46.13}\approx %.3f" % Q21,
                ("fig", fig_scatter_q21),
                "0.83 ≈ r<super>2</super> (coefficient of determination); 1.05 = S<sub>xy</sub>/S<sub>xx</sub> is the "
                "regression slope, not r — and any value above 1 is impossible for r.",
                ("note", "Reject options outside [−1, 1] immediately; then check the sign from the scatter.",
                 "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q22
        dict(
            qtype="MSQ", marks=2, topic="Reading a discrete CDF", difficulty="Medium",
            text=["The CDF of a discrete random variable X (number of rainy days in a week at a station, "
                  "restricted to the values shown) is plotted below:",
                  ("fig", fig_cdf_q22),
                  "F(x) = 0 for x &lt; 1, 0.2 for 1 ≤ x &lt; 2, 0.5 for 2 ≤ x &lt; 4, 0.9 for 4 ≤ x &lt; 5 and 1 for x ≥ 5. "
                  "Which of the following is/are TRUE?"],
            options=["P(X = 2) = 0.3", "P(2 ≤ X &lt; 5) = 0.7", "P(X &gt; 4) = 0.1", "E[X] = 3"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> For a discrete X, the PMF equals the jump sizes of the CDF.",
                ("table", [["x", "1", "2", "4", "5"],
                           ["P(X = x) (jump)", "0.2", "0.3", "0.4", "0.1"]]),
                "<b>(A) TRUE.</b> Jump at 2: 0.5 − 0.2 = 0.3.",
                "<b>(B) TRUE.</b> P(2 ≤ X &lt; 5) = F(5<super>−</super>) − F(2<super>−</super>) = 0.9 − 0.2 = 0.7 "
                "(= P(X=2) + P(X=4) = 0.3 + 0.4).",
                "<b>(C) TRUE.</b> P(X &gt; 4) = 1 − F(4) = 1 − 0.9 = 0.1.",
                "<b>(D) FALSE.</b>",
                r"$$E[X]=1(0.2)+2(0.3)+4(0.4)+5(0.1)=0.2+0.6+1.6+0.5=2.9",
                ("note", "Filled dots mark F's value at a jump (right-continuity). For strict/non-strict "
                         "inequalities, decide whether the jump at the endpoint is included.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q23
        dict(
            qtype="MCQ", marks=2, topic="Central limit theorem", difficulty="Medium",
            text="Daily rainfall readings at a station during the monsoon have mean 50 mm and standard deviation 15 mm "
                 "(distribution unknown). For a random sample of 36 independent days, the probability that the sample "
                 "mean exceeds 54 mm is approximately [Φ(1.6) = 0.9452, Φ(0.27) = 0.6064]",
            options=["0.0548", "0.3936", "0.9452", "0.1096"],
            answer="A",
            solution=[
                "<b>Concept:</b> CLT: X̄ ≈ N(μ, σ²/n) for large n, whatever the population shape.",
                r"$$\mathrm{SE}=\dfrac{\sigma}{\sqrt{n}}=\dfrac{15}{\sqrt{36}}=2.5",
                r"$$P(\bar{X}>54)\approx P\left(Z>\dfrac{54-50}{2.5}\right)=P(Z>1.6)=1-0.9452=0.0548",
                ("fig", fig_clt_q23),
                f"0.3936 uses σ = 15 instead of the standard error (z ≈ 0.27); 0.9452 is Φ(1.6) itself; 0.1096 is "
                "a two-tailed area.",
                ("note", "The spread of an average shrinks by √n. Using σ instead of σ/√n is the #1 CLT "
                         "mistake.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q24
        dict(
            qtype="NAT", marks=2, topic="Confidence interval (t, σ unknown)", difficulty="Medium",
            text="A sample of 25 bolts from a production line has mean length 50.2 mm and sample standard deviation "
                 "0.5 mm. Assuming lengths are normal, the <b>upper</b> limit of the 95% confidence interval for the "
                 "mean length is ______ mm (round off to 2 decimal places). [Use t<sub>0.025, 24</sub> = 2.064.]",
            answer=f"{Q24:.2f}", range=(50.40, 50.41),
            solution=[
                "<b>Concept:</b> σ unknown, normal data ⇒ x̄ ± t<sub>α/2, n−1</sub> · s/√n.",
                r"$$\dfrac{s}{\sqrt{n}}=\dfrac{0.5}{\sqrt{25}}=0.1",
                r"$$\text{margin}=2.064\times 0.1=0.2064",
                r"$$\text{CI}=50.2\pm 0.2064=(49.9936,\ 50.4064)",
                f"Upper limit ≈ <b>{Q24:.2f}</b> mm.",
                "With z = 1.96 instead of t you would get 50.396 ≈ 50.40 — slightly narrower; GATE expects t when "
                "σ is unknown and n is small.",
                ("note", "Degrees of freedom = n − 1 = 24, and the t critical value is always larger than the "
                         "matching z value.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q25
        dict(
            qtype="MCQ", marks=2, topic="One-sample z-test (left-tailed)", difficulty="Medium",
            text="A bottling plant claims its bottles contain on average 500 ml; fill volumes have known standard "
                 "deviation 4 ml. An inspector suspects under-filling and measures 64 bottles, getting a mean of "
                 "498.9 ml. Testing H<sub>0</sub>: μ = 500 against H<sub>1</sub>: μ &lt; 500 at the 5% level "
                 "(z<sub>0.05</sub> = 1.645), which is correct?",
            options=["z = −2.20; reject H<sub>0</sub>", "z = −2.20; do not reject H<sub>0</sub>",
                     "z = −0.28; do not reject H<sub>0</sub>", "z = −17.6; reject H<sub>0</sub>"],
            answer="A",
            solution=[
                "<b>Concept:</b> z = (x̄ − μ<sub>0</sub>)/(σ/√n); left-tailed test rejects when z ≤ −z<sub>α</sub>.",
                r"$$\dfrac{\sigma}{\sqrt{n}}=\dfrac{4}{8}=0.5",
                r"$$z=\dfrac{498.9-500}{0.5}=\dfrac{-1.1}{0.5}=-2.20",
                "Rejection region: z ≤ −1.645. Since −2.20 &lt; −1.645, reject H<sub>0</sub>: evidence of under-filling.",
                ("fig", fig_reject_q25),
                "(C) divides by σ instead of σ/√n; (D) multiplies by √n twice (−1.1 × 64/4). p-value = Φ(−2.2) ≈ 0.0139 &lt; 0.05. (verified)",
                ("note", "The direction of H<sub>1</sub> fixes which tail holds the whole α. Here all 5% sits in the "
                         "left tail.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q26
        dict(
            qtype="MCQ", marks=2, topic="One-sample t-test", difficulty="Medium",
            text="Historically, students in a course scored a mean of 64 in the final exam. After a new tutoring "
                 "programme, a random sample of 10 students scored a mean of 67.3 with sample standard deviation 5.8. "
                 "Assume normality. For H<sub>0</sub>: μ = 64 vs H<sub>1</sub>: μ &gt; 64 at the 5% level "
                 "(t<sub>0.05, 9</sub> = 1.833, z<sub>0.05</sub> = 1.645), which is correct?",
            options=["t = 1.80; reject H<sub>0</sub>",
                     "t = 1.80; do not reject H<sub>0</sub>",
                     "t = 5.69; reject H<sub>0</sub>",
                     "t = 1.80; reject H<sub>0</sub> because 1.80 &gt; 1.645"],
            answer="B",
            solution=[
                "<b>Concept:</b> σ unknown ⇒ t = (x̄ − μ<sub>0</sub>)/(s/√n) with n − 1 df; reject if t ≥ t<sub>α, n−1</sub>.",
                r"$$\dfrac{s}{\sqrt{n}}=\dfrac{5.8}{\sqrt{10}}=\dfrac{5.8}{3.1623}=1.8341",
                r"$$t=\dfrac{67.3-64}{1.8341}=\dfrac{3.3}{1.8341}\approx %.3f" % Q26_t,
                "Critical value t<sub>0.05, 9</sub> = 1.833. Since 1.80 &lt; 1.833, we <b>do not reject</b> H<sub>0</sub> "
                "at 5%.",
                ("fig", fig_t_q26),
                "(C) forgets √n (3.3/0.58); (A)/(D) use the z cut-off 1.645, which is wrong when σ is estimated from "
                "only 10 observations — the heavier-tailed t requires stronger evidence.",
                ("note", "A borderline case: z-logic would reject, t-logic does not. Always use t with s and "
                         "small n.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q27
        dict(
            qtype="MCQ", marks=2, topic="χ² goodness-of-fit test", difficulty="Medium",
            text=["A die is rolled 120 times to test whether it is fair. The observed face counts are:",
                  ("table", [["Face", "1", "2", "3", "4", "5", "6"],
                             ["Observed", "15", "25", "18", "22", "16", "24"]]),
                  "Using the χ² goodness-of-fit test at the 5% level (χ²<sub>0.05, 5</sub> = 11.07, "
                  "χ²<sub>0.05, 6</sub> = 12.59), which is correct?"],
            options=["χ² = 4.5 with 5 df; do not reject fairness",
                     "χ² = 4.5 with 6 df; do not reject fairness",
                     "χ² = 90 with 5 df; reject fairness",
                     "χ² = 4.5 with 5 df; reject fairness"],
            answer="A",
            solution=[
                "<b>Concept:</b> χ² = ∑(O − E)²/E with k − 1 df (no parameters estimated).",
                "Under H<sub>0</sub> (fair die), E = 120/6 = 20 for each face.",
                ("table", [["Face", "1", "2", "3", "4", "5", "6"],
                           ["O − E", "−5", "5", "−2", "2", "−4", "4"],
                           ["(O − E)²", "25", "25", "4", "4", "16", "16"]]),
                r"$$\chi^2=\dfrac{25+25+4+4+16+16}{20}=\dfrac{90}{20}=4.5",
                "df = 6 − 1 = 5; critical value 11.07. Since 4.5 &lt; 11.07, do not reject H<sub>0</sub>.",
                ("fig", fig_chi_q27),
                "(C) forgets to divide by E; (B) uses k instead of k − 1 df (the conclusion happens to agree but the df "
                "is wrong).",
                ("note", "The counts must total n, which costs one degree of freedom: df = k − 1 − (number of "
                         "estimated parameters).", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q28
        dict(
            qtype="MSQ", marks=2, topic="t and χ² distributions (concept check)", difficulty="Medium",
            text="Which of the following statements about the t and χ² distributions is/are TRUE?",
            options=["The t distribution with ν degrees of freedom has heavier tails than N(0, 1).",
                     "As ν → ∞, the t distribution with ν degrees of freedom approaches N(0, 1).",
                     "If Z<sub>1</sub>, …, Z<sub>k</sub> are i.i.d. N(0, 1), then Z<sub>1</sub><super>2</super> + … + "
                     "Z<sub>k</sub><super>2</super> has a χ² distribution with k degrees of freedom.",
                     "A χ² random variable with k degrees of freedom has mean k and variance k."],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> t<sub>ν</sub> = Z/√(V/ν) with V ∼ χ²<sub>ν</sub>; χ²<sub>k</sub> is a sum of k squared "
                "standard normals.",
                ("fig", fig_t_vs_z_q28),
                "<b>(A) TRUE.</b> Extra randomness in the denominator (estimated σ) spreads mass into the tails.",
                "<b>(B) TRUE.</b> V/ν → 1 as ν → ∞ (law of large numbers), so t<sub>ν</sub> → Z.",
                "<b>(C) TRUE.</b> This is the definition of χ²<sub>k</sub>.",
                "<b>(D) FALSE.</b> Each Z<sub>i</sub><super>2</super> has mean 1 and variance "
                "E[Z<super>4</super>] − 1 = 3 − 1 = 2, so",
                r"$$E[\chi^2_k]=k,\qquad \mathrm{Var}(\chi^2_k)=2k",
                ("note", "Remember 'mean k, variance 2k' for χ²; and t-critical values shrink toward z-values "
                         "as the df grow.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q29
        dict(
            qtype="NAT", marks=2, topic="Binomial: acceptance sampling", difficulty="Medium",
            text="A buyer inspects a random sample of 10 items from a large lot and accepts the lot if at most one "
                 "sampled item is defective. If 5% of the items in the lot are defective (independently), the "
                 "probability that the lot is accepted is ______ (round off to 3 decimal places).",
            answer=f"{Q29:.3f}", range=(0.913, 0.915),
            solution=[
                "<b>Concept:</b> Number of defectives X ∼ Bin(10, 0.05) (large lot ⇒ independence); "
                "P(accept) = P(X ≤ 1).",
                r"$$P(X=0)=(0.95)^{10}=%.4f" % (0.95 ** 10),
                r"$$P(X=1)=\binom{10}{1}(0.05)(0.95)^9=10\times 0.05\times %.4f=%.4f" % (0.95 ** 9, 10 * 0.05 * 0.95 ** 9),
                r"$$P(\text{accept})=%.4f+%.4f=%.4f" % (0.95 ** 10, 10 * 0.05 * 0.95 ** 9, Q29),
                f"Answer ≈ <b>{Q29:.3f}</b>.",
                "Poisson check (λ = np = 0.5): e<super>−0.5</super>(1 + 0.5) = 0.9098 — close, but the exact binomial "
                "is required here.",
                ("note", "'At most one' = P(0) + P(1). Forgetting P(0) gives only 0.315.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q30
        dict(
            qtype="MSQ", marks=2, topic="Discrete uniform, Bernoulli indicators, independence", difficulty="Medium",
            text="A fair die is rolled once; let X be the face shown. Define indicator variables "
                 "I = 1 if X is even (0 otherwise), J = 1 if X ≤ 2 (0 otherwise), and K = 1 if X ≤ 3 (0 otherwise). "
                 "Which of the following is/are TRUE?",
            options=["E[X] = 3.5", "Var(X) = 35/12", "I and J are independent", "I and K are independent"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> X is discrete uniform on {1, …, 6}: mean (n + 1)/2, variance (n² − 1)/12. Indicators "
                "are Bernoulli; two indicators are independent iff P(both = 1) = product of their means.",
                "<b>(A) TRUE.</b> E[X] = (6 + 1)/2 = 3.5.",
                "<b>(B) TRUE.</b>",
                r"$$\mathrm{Var}(X)=E[X^2]-3.5^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}",
                "<b>(C) TRUE.</b> I ∼ Bernoulli(1/2), J ∼ Bernoulli(1/3). {I = 1, J = 1} = {X = 2}:",
                r"$$P(I=1,J=1)=\dfrac{1}{6}=\dfrac{1}{2}\cdot\dfrac{1}{3}=P(I=1)P(J=1)",
                "For 0/1 variables, this single equality implies the other three cells factor as well.",
                "<b>(D) FALSE.</b> {I = 1, K = 1} = {X = 2}:",
                r"$$P(I=1,K=1)=\dfrac{1}{6}\neq\dfrac{1}{2}\cdot\dfrac{1}{2}=\dfrac{1}{4}",
                ("note", "Independence is a numerical property, not a 'physical' one: events about the SAME roll "
                         "can still be independent.", "Key idea"),
            ],
        ),
    ],
}
