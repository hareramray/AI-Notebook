"""Mock Test 02 — Foundation Full-Syllabus Test II (warm-up level, whole syllabus)."""
from fractions import Fraction as Fr
from math import comb, exp, factorial, log, sqrt

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ----------------------------------------------------------------- computed answers
Q1 = comb(4, 2) * comb(48, 3)                               # 103776
Q2 = Fr(7, 8)
Q4 = Fr(comb(4, 2), comb(52, 2) - comb(48, 2))             # 1/33
R5 = np.array([4, 7, 7, 9, 13])
Q5 = R5.var(ddof=1)                                         # 11
Q8 = exp(-1.5) * (1 + 1.5)                                  # 0.5578
Q9 = log(2) / 0.25                                          # 2.7726
Q10 = stats.norm.cdf(2) - stats.norm.cdf(-1)                # 0.8186
Q11 = 3 / sqrt(2)                                           # 2.1213
Q13 = Fr(2 * factorial(4) * factorial(4), factorial(8))     # 1/35
Q14 = 1 - Fr(6 * 5 * 4 * 3, 6 ** 4)                         # 13/18
Q15 = Fr(1, 2) * Fr(3, 5) / (Fr(1, 2) * Fr(3, 5) + Fr(1, 2) * Fr(2, 6))   # 9/14
Q17 = 4 * 0.25 * 0.75 + 0.25 ** 2 * 4                       # 1.0
Q18 = Fr(1, 4)
Q19 = Fr(4, 9)
V22 = np.array([2, 4, 6, 8, 10]); F22 = np.array([3, 5, 8, 3, 1])
Q22_mean = (V22 * F22).sum() / F22.sum()
Q22_m2 = (V22 ** 2 * F22).sum() / F22.sum()
Q22 = sqrt(Q22_m2 - Q22_mean ** 2)                          # 2.107
Q23 = 2 * stats.norm.sf(1.5)                                # 0.1336
Q24 = stats.norm.sf((26 - 24) / 2)                          # 0.1587
Q25 = (92 - 2.576 * 2, 92 + 2.576 * 2)
Q26_z = (224 - 200) / 10
Q26 = 2 * stats.norm.sf(Q26_z)                              # 0.0164
O27 = np.array([[40, 10], [30, 20]])
E27 = O27.sum(1, keepdims=True) * O27.sum(0, keepdims=True) / O27.sum()
Q27 = ((O27 - E27) ** 2 / E27).sum()                        # 4.762
B28 = np.array([52, 60, 58, 45, 70, 63]); A28 = np.array([55, 65, 57, 49, 72, 68])
D28 = A28 - B28
Q28_s = D28.std(ddof=1)
Q28 = D28.mean() / (Q28_s / sqrt(len(D28)))                 # 3.22


# ----------------------------------------------------------------- figures
def fig_venn_q2():
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    ax.add_patch(plt.Rectangle((-2.9, -1.55), 6.2, 3.1, fill=False, color="0.4"))
    ax.add_patch(Circle((-0.6, 0), 1.25, color=BLUE, alpha=0.28))
    ax.add_patch(Circle((0.9, 0), 1.25, color=MAROON, alpha=0.28))
    ax.text(-1.25, 0, "HHH\nHHT\nHTH", ha="center", va="center", fontsize=9)
    ax.text(0.15, 0, "THH", ha="center", va="center", fontsize=9)
    ax.text(1.55, 0, "THT\nTTH\nTTT", ha="center", va="center", fontsize=9)
    ax.text(2.7, -1.3, "HTT", ha="center", fontsize=9)
    ax.text(-1.7, 1.2, "A: ≥ 2 heads", color=BLUE, fontsize=9)
    ax.text(1.2, 1.2, "B: 1st toss T", color=MAROON, fontsize=9)
    ax.set_xlim(-3.0, 3.4); ax.set_ylim(-1.65, 1.6); ax.set_aspect("equal"); ax.axis("off")
    return fig


def fig_exp_q9():
    t = np.linspace(0, 16, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(t, 0.25 * np.exp(-0.25 * t), color=BLUE)
    m = t <= Q9
    ax.fill_between(t[m], 0.25 * np.exp(-0.25 * t[m]), color=GOLD, alpha=0.6)
    ax.axvline(Q9, color=MAROON, lw=1.5)
    ax.axvline(4, color="0.5", ls="--", lw=1)
    ax.text(Q9 + 0.2, 0.2, f"median ≈ {Q9:.2f} h", color=MAROON, fontsize=9)
    ax.text(4.2, 0.12, "mean = 4 h", color="0.4", fontsize=9)
    ax.text(0.4, 0.04, "area 0.5", fontsize=9)
    ax.set_xlabel("waiting time t (hours)"); ax.set_yticks([])
    return fig


def fig_norm_q10():
    z = np.linspace(-3.5, 3.5, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(z, stats.norm.pdf(z), color=BLUE)
    m = (z > -1) & (z < 2)
    ax.fill_between(z[m], stats.norm.pdf(z[m]), color=BLUE, alpha=0.3)
    ax.text(0.15, 0.12, f"{Q10:.4f}", fontsize=10, ha="center")
    ax.text(-2.6, 0.06, "0.1587", color=MAROON, fontsize=9)
    ax.text(2.2, 0.06, "0.0228", color=MAROON, fontsize=9)
    ax.set_yticks([]); ax.set_xlabel("z")
    return fig


def fig_cdf_q11():
    x = np.linspace(-0.5, 3.8, 400)
    F = np.clip(x, 0, 3) ** 2 / 9
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, F, color=BLUE, lw=2)
    ax.axhline(0.5, color="0.6", ls="--", lw=1)
    ax.plot([Q11, Q11], [0, 0.5], color=MAROON, lw=1.5)
    ax.text(Q11 + 0.05, 0.08, f"m = 3/√2 ≈ {Q11:.2f}", color=MAROON, fontsize=9)
    ax.set_xlabel("rainfall x (cm)"); ax.set_ylabel("F(x)")
    return fig


def fig_tree_q15():
    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.axis("off")
    for y, lab, w, b in [(1.6, "Urn I (1/2)", "W: 3/5 → 3/10", "B: 2/5"),
                         (0.0, "Urn II (1/2)", "W: 2/6 → 1/6", "B: 4/6")]:
        ax.plot([0, 1.4], [0.8, y], color=BLUE)
        ax.text(1.45, y, lab, va="center", fontsize=9.5, color=BLUE)
        ax.plot([2.8, 4.0], [y, y + 0.35], color=MAROON)
        ax.plot([2.8, 4.0], [y, y - 0.35], color="0.6")
        ax.text(4.05, y + 0.35, w, va="center", fontsize=9, color=MAROON)
        ax.text(4.05, y - 0.35, b, va="center", fontsize=9, color="0.5")
    ax.plot(0, 0.8, "o", color="k")
    ax.set_xlim(-0.1, 6.2); ax.set_ylim(-0.6, 2.2)
    return fig


def fig_region_q18():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.fill([0, 0, 1], [0, 1, 1], color=BLUE, alpha=0.22)
    ax.plot([0, 1], [0, 1], color=BLUE)
    ax.plot([0, 0.5], [0.5, 0.5], color=MAROON, lw=3)
    ax.plot([0, 0.25], [0.5, 0.5], color=GOLD, lw=5)
    ax.text(0.02, 0.40, "slice Y = 0.5,\n0 < x < 0.5", fontsize=8.5, color=MAROON)
    ax.text(0.15, 0.8, "f = 6x", fontsize=10)
    ax.text(0.78, 0.66, "y = x", color=BLUE, fontsize=9, rotation=33)
    ax.set_xlim(0, 1.05); ax.set_ylim(0, 1.05); ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig


def fig_region_q19():
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color="0.4")
    ax.fill([0, 1, 1], [0, 0, 1], color=GOLD, alpha=0.5)
    ax.plot([0, 1], [0, 1], color=MAROON)
    ax.text(0.55, 0.2, "x > y", fontsize=10)
    ax.text(0.1, 0.8, "f = c(x + 2y)", fontsize=10, color=BLUE)
    ax.set_xlim(-0.05, 1.1); ax.set_ylim(-0.05, 1.1); ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig


def fig_hist_q22():
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.bar(V22, F22, width=1.6, color=BLUE, alpha=0.8)
    ax.axvline(Q22_mean, color=MAROON, lw=1.6)
    ax.text(Q22_mean + 1.1, 8.3, f"mean {Q22_mean:.1f}", color=MAROON, fontsize=9)
    ax.set_xticks(V22); ax.set_xlabel("score"); ax.set_ylabel("frequency")
    return fig


def fig_norm_q23():
    x = np.linspace(9.92, 10.08, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.norm.pdf(x, 10, 0.02), color=BLUE)
    for m in (x <= 9.97, x >= 10.03):
        ax.fill_between(x[m], stats.norm.pdf(x[m], 10, 0.02), color=MAROON, alpha=0.4)
    ax.axvline(9.97, color="0.5", ls="--", lw=1); ax.axvline(10.03, color="0.5", ls="--", lw=1)
    ax.text(9.925, 8, "reject\n(&lt; 9.97)".replace("&lt;", "<"), color=MAROON, fontsize=8.5)
    ax.text(10.045, 8, "reject\n(> 10.03)", color=MAROON, fontsize=8.5)
    ax.set_yticks([]); ax.set_xlabel("diameter (mm)")
    return fig


def fig_clt_q24():
    s = np.linspace(16, 32, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(s, stats.norm.pdf(s, 24, 2), color=BLUE)
    m = s >= 26
    ax.fill_between(s[m], stats.norm.pdf(s[m], 24, 2), color=MAROON, alpha=0.4)
    ax.annotate("≈ 0.1587", xy=(27, 0.03), xytext=(28.5, 0.12), color=MAROON, fontsize=9, arrowprops=dict(arrowstyle="->"))
    ax.set_yticks([]); ax.set_xlabel("total error S (mm),  S ≈ N(24, 2²)")
    return fig


def fig_ci_q25():
    fig, ax = plt.subplots(figsize=(5.4, 2.3))
    for y, z, lab, col in [(3, 1.645, "90%", GOLD), (2, 1.96, "95%", BLUE), (1, 2.576, "99%", MAROON)]:
        ax.plot([92 - 2 * z, 92 + 2 * z], [y, y], color=col, lw=4)
        ax.text(92 + 2 * z + 0.3, y, f"{lab}: 92 ± {2 * z:.2f}", va="center", fontsize=9)
    ax.axvline(92, color="0.5", ls=":")
    ax.set_yticks([]); ax.set_xlim(85, 103); ax.set_ylim(0.4, 3.6); ax.set_xlabel("mean rainfall (cm)")
    return fig


def fig_reject_q26():
    z = np.linspace(-3.8, 3.8, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(z, stats.norm.pdf(z), color=BLUE)
    for m in (z >= 2.4, z <= -2.4):
        ax.fill_between(z[m], stats.norm.pdf(z[m]), color=MAROON, alpha=0.5)
    ax.axvline(2.4, color=GOLD, lw=2)
    ax.text(2.45, 0.2, "z = 2.4", fontsize=9)
    ax.text(-3.7, 0.08, "0.0082", color=MAROON, fontsize=9)
    ax.text(2.7, 0.08, "0.0082", color=MAROON, fontsize=9)
    ax.set_yticks([]); ax.set_xlabel("z")
    return fig


def fig_chi_q27():
    x = np.linspace(0.02, 9, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.chi2.pdf(x, 1), color=BLUE)
    m = x >= 3.841
    ax.fill_between(x[m], stats.chi2.pdf(x[m], 1), color=MAROON, alpha=0.4)
    ax.axvline(Q27, color=GOLD, lw=2)
    ax.text(Q27 + 0.15, 0.4, f"χ² = {Q27:.2f}", fontsize=9)
    ax.text(5.6, 0.08, "reject: χ² ≥ 3.841", color=MAROON, fontsize=8.5)
    ax.set_ylim(0, 0.6); ax.set_yticks([]); ax.set_xlabel("χ² (1 df)")
    return fig


def fig_clt_q29():
    die = np.ones(6) / 6
    fig, axes = plt.subplots(1, 3, figsize=(6.2, 2.2), sharey=False)
    for ax, n in zip(axes, (1, 2, 10)):
        p = die.copy()
        for _ in range(n - 1):
            p = np.convolve(p, die)
        means = (np.arange(len(p)) + n) / n
        ax.bar(means, p, width=0.8 / n if n > 1 else 0.6, color=BLUE)
        ax.set_title(f"mean of {n} roll{'s' if n > 1 else ''}", fontsize=9)
        ax.set_yticks([]); ax.set_xticks([1, 3.5, 6])
    fig.tight_layout()
    return fig


# ----------------------------------------------------------------- the set
SET = {
    "title": "Foundation Full-Syllabus Test II",
    "subtitle": "A second warm-up paper over the whole syllabus — cards, coins, dice, urns, seating, factory "
                "shifts, exam scores and weather.",
    "focus": "Covers the full syllabus at warm-up difficulty: counting with cards and seating, sample spaces "
             "and axioms, mutually exclusive vs independent events, contingency tables (joint, marginal, "
             "conditional), Bayes with a two-urn tree, conditional expectation/variance (random sums), conditional "
             "and joint PDFs, sample variance and grouped standard deviation, Var of linear combinations, "
             "Bernoulli/binomial, Poisson, uniform, exponential, normal, CDF-based median, CLT for sums, z-interval, "
             "z-test (p-value), paired t-test and χ² test of independence. Concept-check MSQs probe PDF properties, "
             "expectation rules, independence implications, sampling distributions and the logic of tests and "
             "intervals.",
    "minutes": 90,
    "questions": [
        # ------------------------------------------------------------ Q1
        dict(
            qtype="MCQ", marks=1, topic="Counting: card hands", difficulty="Easy",
            text="The number of 5-card hands that can be dealt from a standard 52-card deck containing "
                 "<b>exactly</b> two aces is",
            options=["103 776", "132 600", "117 600", "622 656"],
            answer="A",
            solution=[
                "<b>Concept:</b> Multiplication principle for unordered selections: choose the aces, then choose "
                "the non-aces.",
                r"$$\binom{4}{2}\times\binom{48}{3}=6\times 17296=%d" % Q1,
                "<b>Distractors:</b> 132 600 = C(4,2)·C(52,3) lets the other three cards include aces (overcounts "
                "hands with 3 or 4 aces); 117 600 = C(4,2)·C(50,3) removes only the chosen aces from the pool; "
                "622 656 = 6·48·47·46 orders the three non-aces.",
                ("note", "'Exactly k of a type' ⇒ the remaining cards must come only from the OTHER types.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q2
        dict(
            qtype="MCQ", marks=1, topic="Sample space, union of events", difficulty="Easy",
            text="A fair coin is tossed three times. Let A = 'at least two heads' and B = 'the first toss is a "
                 "tail'. P(A ∪ B) equals",
            options=["7/8", "1/2", "3/4", "5/8"],
            answer="A",
            solution=[
                "<b>Concept:</b> List the 8 equally likely outcomes and use P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
                "A = {HHH, HHT, HTH, THH} (4 outcomes); B = {THH, THT, TTH, TTT} (4 outcomes); A ∩ B = {THH}.",
                ("fig", fig_venn_q2),
                r"$$P(A\cup B)=\dfrac{4}{8}+\dfrac{4}{8}-\dfrac{1}{8}=\dfrac{7}{8}",
                "Only HTT lies outside both events: 1 − 1/8 = 7/8. 'Adding without subtracting' gives 1 — not even "
                "an option, a useful warning sign.",
                ("note", "When the sample space is small, the complement (outcomes in neither event) is often "
                         "quickest.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q3
        dict(
            qtype="MSQ", marks=1, topic="Mutually exclusive events", difficulty="Easy",
            text="Events A and B are mutually exclusive with P(A) = 0.3 and P(B) = 0.5. Which of the following "
                 "is/are TRUE?",
            options=["P(A ∪ B) = 0.8", "P(A | B) = 0", "A and B are independent",
                     "P(A<super>c</super> ∩ B<super>c</super>) = 0.2"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> Mutually exclusive ⇒ P(A ∩ B) = 0, so probabilities of A and B simply add.",
                "<b>(A) TRUE.</b> P(A ∪ B) = 0.3 + 0.5 − 0 = 0.8.",
                "<b>(B) TRUE.</b> P(A | B) = P(A ∩ B)/P(B) = 0/0.5 = 0.",
                "<b>(C) FALSE.</b> P(A)P(B) = 0.15 ≠ 0 = P(A ∩ B).",
                "<b>(D) TRUE.</b> De Morgan: P(A<super>c</super> ∩ B<super>c</super>) = 1 − P(A ∪ B) = 0.2.",
                ("note", "P(A | B) = 0 ≠ P(A) = 0.3 shows directly that learning B changes the chance of A — the "
                         "hallmark of dependence.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q4
        dict(
            qtype="NAT", marks=1, topic="Conditional probability (cards)", difficulty="Easy",
            text="Two cards are drawn at random without replacement from a standard 52-card deck. Given that at "
                 "least one of them is a king, the probability that both are kings is ______ (round off to 3 "
                 "decimal places).",
            answer=f"{float(Q4):.3f}", range=(0.030, 0.031),
            solution=[
                "<b>Concept:</b> P(both | at least one) = P(both)/P(at least one), since 'both' ⊂ 'at least one'.",
                r"$$P(\text{both})=\dfrac{\binom{4}{2}}{\binom{52}{2}}=\dfrac{6}{1326}",
                r"$$P(\geq 1\ \text{king})=1-\dfrac{\binom{48}{2}}{\binom{52}{2}}=1-\dfrac{1128}{1326}=\dfrac{198}{1326}",
                r"$$P(\text{both}\mid\geq 1)=\dfrac{6}{198}=\dfrac{1}{33}\approx %.4f" % float(Q4),
                f"Answer ≈ <b>{float(Q4):.3f}</b>.",
                ("note", "This is NOT P(second is king | first is king) = 3/51 ≈ 0.059. 'At least one' does not "
                         "say which card is the king.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q5
        dict(
            qtype="MCQ", marks=1, topic="Sample variance", difficulty="Easy",
            text="The rainfall (in cm) recorded at a station in five consecutive months is 4, 7, 7, 9, 13. The "
                 "<b>sample variance</b> (with divisor n − 1) is",
            options=["8.8", "11", "3.32", "44"],
            answer="B",
            solution=[
                "<b>Concept:</b> s² = ∑(x<sub>i</sub> − x̄)²/(n − 1).",
                r"$$\bar{x}=\dfrac{4+7+7+9+13}{5}=\dfrac{40}{5}=8",
                ("table", [["x", "4", "7", "7", "9", "13"],
                           ["x − x̄", "−4", "−1", "−1", "1", "5"],
                           ["(x − x̄)²", "16", "1", "1", "1", "25"]]),
                r"$$s^2=\dfrac{16+1+1+1+25}{5-1}=\dfrac{44}{4}=11",
                "8.8 = 44/5 uses divisor n (population variance); 3.32 = √11 is the sample SD; 44 is the sum of "
                "squares itself.",
                ("note", "Read the divisor carefully: n − 1 (sample, unbiased) vs n (population).", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q6
        dict(
            qtype="MCQ", marks=1, topic="Binomial mean and variance", difficulty="Easy",
            text="In a series of independent free throws, the number of successes X follows a binomial "
                 "distribution with mean 6 and variance 2.4. The parameters (n, p) are",
            options=["(10, 0.6)", "(15, 0.4)", "(12, 0.5)", "(10, 0.4)"],
            answer="A",
            solution=[
                "<b>Concept:</b> X ∼ Bin(n, p) ⇒ E[X] = np, Var(X) = np(1 − p).",
                r"$$1-p=\dfrac{np(1-p)}{np}=\dfrac{2.4}{6}=0.4\ \Rightarrow\ p=0.6",
                r"$$n=\dfrac{6}{0.6}=10",
                "(15, 0.4) has mean 6 but variance 3.6; (12, 0.5) has variance 3; (10, 0.4) swaps p and 1 − p "
                "(mean 4).",
                ("note", "Dividing variance by mean gives q = 1 − p directly.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q7
        dict(
            qtype="MSQ", marks=1, topic="Properties of a PDF (concept check)", difficulty="Easy",
            text="Let f be the probability density function of a continuous random variable X. Which of the "
                 "following is/are necessarily TRUE?",
            options=["f(x) ≥ 0 for all x", "f(x) ≤ 1 for all x", "P(X = c) = 0 for every real c",
                     "∫<sub>−∞</sub><super>∞</super> f(x) dx = 1"],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> A PDF is non-negative and integrates to 1; it is a density, not a probability.",
                "<b>(A) TRUE.</b> Otherwise some interval would get negative probability.",
                "<b>(B) FALSE.</b> X ∼ U(0, 0.5) has f(x) = 2 on (0, 0.5). Only areas must be ≤ 1, not heights.",
                "<b>(C) TRUE.</b> P(X = c) = ∫<sub>c</sub><super>c</super> f(x) dx = 0.",
                "<b>(D) TRUE.</b> Total probability is 1.",
                ("note", "f(x) is probability per unit length; a narrow distribution must have a tall density.",
                 "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q8
        dict(
            qtype="NAT", marks=1, topic="Poisson distribution", difficulty="Easy",
            text="The number of bubbles (defects) in a glass sheet follows a Poisson distribution with mean 1.5. "
                 "A sheet is graded 'premium' if it has at most one bubble. The probability that a randomly chosen "
                 "sheet is premium is ______ (round off to 3 decimal places).",
            answer=f"{Q8:.3f}", range=(0.557, 0.559),
            solution=[
                "<b>Concept:</b> P(X = k) = e<super>−λ</super>λ<super>k</super>/k! with λ = 1.5.",
                r"$$P(X\leq 1)=e^{-1.5}\left(1+1.5\right)=0.2231\times 2.5=%.4f" % Q8,
                f"Answer ≈ <b>{Q8:.3f}</b>.",
                ("note", "'At most one' includes zero: P(0) = 0.2231 and P(1) = 0.3347 — forgetting P(0) is the "
                         "usual slip.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q9
        dict(
            qtype="MCQ", marks=1, topic="Exponential distribution: median", difficulty="Easy",
            text="The waiting time (in hours) until the next rain shower in a monsoon week is exponentially "
                 "distributed with rate 0.25 per hour. The <b>median</b> waiting time is closest to",
            options=["4.00 h", "2.00 h", "2.77 h", "0.17 h"],
            answer="C",
            solution=[
                "<b>Concept:</b> For Exp(λ), F(t) = 1 − e<super>−λt</super>; the median m solves F(m) = 1/2.",
                r"$$1-e^{-0.25m}=0.5\ \Rightarrow\ m=\dfrac{\ln 2}{0.25}=4\ln 2\approx %.2f\ \text{h}" % Q9,
                ("fig", fig_exp_q9),
                "4.00 h is the mean (1/λ); 2.00 h is half the mean; 0.17 h = 0.25 ln 2 multiplies instead of divides.",
                ("note", "Exponential is right-skewed, so median (0.693/λ) &lt; mean (1/λ).", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q10
        dict(
            qtype="MCQ", marks=1, topic="Standard normal probabilities", difficulty="Easy",
            text="If Z ∼ N(0, 1), then P(−1 &lt; Z &lt; 2) is closest to [Φ(1) = 0.8413, Φ(2) = 0.9772]",
            options=["0.6826", "0.8185", "0.9544", "0.1815"],
            answer="B",
            solution=[
                "<b>Concept:</b> P(a &lt; Z &lt; b) = Φ(b) − Φ(a), and Φ(−a) = 1 − Φ(a).",
                r"$$P(-1<Z<2)=\Phi(2)-\Phi(-1)=0.9772-(1-0.8413)=0.9772-0.1587=0.8185",
                ("fig", fig_norm_q10),
                "0.6826 = P(|Z| &lt; 1), 0.9544 = P(|Z| &lt; 2) (symmetric intervals); 0.1815 is the complement.",
                ("note", "Draw the curve and shade first; asymmetric intervals need two separate tail look-ups.",
                 "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q11
        dict(
            qtype="NAT", marks=1, topic="CDF and median of a continuous RV", difficulty="Easy",
            text="The rainfall X (in cm) on a stormy day has CDF F(x) = 0 for x &lt; 0, F(x) = x<super>2</super>/9 "
                 "for 0 ≤ x &lt; 3, and F(x) = 1 for x ≥ 3. The median of X is ______ cm (round off to 2 decimal "
                 "places).",
            answer=f"{Q11:.2f}", range=(2.12, 2.13),
            solution=[
                "<b>Concept:</b> The median m of a continuous RV satisfies F(m) = 0.5.",
                r"$$\dfrac{m^2}{9}=\dfrac{1}{2}\ \Rightarrow\ m^2=4.5\ \Rightarrow\ m=\dfrac{3}{\sqrt{2}}\approx %.4f" % Q11,
                ("fig", fig_cdf_q11),
                f"Answer ≈ <b>{Q11:.2f}</b> cm. (For comparison, f(x) = 2x/9 gives mean ∫ 2x²/9 dx = 2 cm &lt; median: "
                "a left-skewed density.)",
                ("note", "Work directly with the CDF — no need to differentiate to the PDF for a quantile.",
                 "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q12
        dict(
            qtype="MSQ", marks=1, topic="Expectation rules (concept check)", difficulty="Easy",
            text="Let X and Y be random variables with finite means (and X &gt; 0 where 1/X appears). Which of the "
                 "following is/are TRUE <b>in general</b>?",
            options=["E[X + Y] = E[X] + E[Y]", "E[XY] = E[X] E[Y]", "E[ E[X | Y] ] = E[X]",
                     "E[1/X] = 1/E[X]"],
            answer="A, C",
            solution=[
                "<b>Concept:</b> Linearity of expectation needs no independence; products and non-linear functions "
                "do not pass through E.",
                "<b>(A) TRUE.</b> Linearity holds for any X, Y (dependent or not).",
                "<b>(B) FALSE.</b> Needs uncorrelatedness. Take Y = X with X ∼ Bernoulli(1/2): E[X²] = 1/2 but "
                "(E[X])² = 1/4.",
                "<b>(C) TRUE.</b> Law of total expectation (tower property).",
                "<b>(D) FALSE.</b> X uniform on {1, 2}:",
                r"$$E\left[\dfrac{1}{X}\right]=\dfrac{1}{2}\left(1+\dfrac{1}{2}\right)=0.75\ \neq\ \dfrac{1}{E[X]}=\dfrac{1}{1.5}\approx 0.667",
                ("note", "Jensen: for convex g, E[g(X)] ≥ g(E[X]); 1/x is convex on x &gt; 0, so E[1/X] ≥ 1/E[X].",
                 "Key idea"),
            ],
        ),
        # ============================================================ 2-mark
        # ------------------------------------------------------------ Q13
        dict(
            qtype="NAT", marks=2, topic="Counting: seating in a row", difficulty="Medium",
            text="Four boys and four girls take seats at random in a row of 8 chairs. The probability that boys and "
                 "girls sit alternately is ______ (round off to 3 decimal places).",
            answer=f"{float(Q13):.3f}", range=(0.028, 0.029),
            solution=[
                "<b>Concept:</b> Probability = favourable arrangements / all arrangements of 8 distinct people.",
                r"$$\text{Total}=8!=40320",
                "Alternating patterns: BGBGBGBG or GBGBGBGB (2 patterns). In each, boys fill their 4 seats in 4! ways "
                "and girls in 4! ways:",
                r"$$\text{Favourable}=2\times 4!\times 4!=2\times 24\times 24=1152",
                r"$$P=\dfrac{1152}{40320}=\dfrac{1}{35}\approx %.4f" % float(Q13),
                f"Answer ≈ <b>{float(Q13):.3f}</b>.",
                "Check via genders only: choose which 4 of 8 seats get boys, C(8,4) = 70 equally likely patterns, "
                "2 alternate ⇒ 2/70 = 1/35. (verified)",
                ("note", "Forgetting the factor 2 (starting with a girl) halves the answer to 0.014.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q14
        dict(
            qtype="MCQ", marks=2, topic="Complement rule (dice)", difficulty="Medium",
            text="Four fair dice are rolled. The probability that at least two of them show the same face is",
            options=["5/18", "13/18", "671/1296", "1/216"],
            answer="B",
            solution=[
                "<b>Concept:</b> 'At least two the same' is the complement of 'all faces different'.",
                r"$$P(\text{all different})=\dfrac{6\times 5\times 4\times 3}{6^4}=\dfrac{360}{1296}=\dfrac{5}{18}",
                r"$$P(\text{at least two same})=1-\dfrac{5}{18}=\dfrac{13}{18}\approx 0.722",
                "5/18 is the complement itself; 671/1296 = 1 − (5/6)<super>4</super> is P(at least one six) — a "
                "different event; 1/216 = 6/1296 is P(all four equal).",
                ("note", "This is the birthday problem with 6 'days': with only 4 dice, a repeat is already "
                         "72% likely.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q15
        dict(
            qtype="MCQ", marks=2, topic="Bayes theorem (two urns)", difficulty="Medium",
            text="Urn I contains 3 white and 2 black balls; Urn II contains 2 white and 4 black balls. A fair coin "
                 "is tossed: heads ⇒ Urn I, tails ⇒ Urn II. One ball is drawn from the chosen urn and it is white. "
                 "The probability that Urn I was chosen is",
            options=["3/5", "1/2", "9/14", "5/14"],
            answer="C",
            solution=[
                "<b>Concept:</b> Bayes: P(I | W) = P(I)P(W | I) / [P(I)P(W | I) + P(II)P(W | II)].",
                ("fig", fig_tree_q15),
                r"$$P(W)=\dfrac{1}{2}\cdot\dfrac{3}{5}+\dfrac{1}{2}\cdot\dfrac{2}{6}=\dfrac{3}{10}+\dfrac{1}{6}=\dfrac{14}{30}=\dfrac{7}{15}",
                r"$$P(I\mid W)=\dfrac{3/10}{7/15}=\dfrac{3}{10}\cdot\dfrac{15}{7}=\dfrac{9}{14}\approx 0.643",
                "3/5 is P(W | I) (the reversed conditional); 1/2 is the prior; 5/14 is P(II | W).",
                ("note", "White is more common in Urn I (60% vs 33%), so seeing white pushes the 50:50 prior "
                         "towards Urn I — but not all the way.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q16
        dict(
            qtype="MSQ", marks=2, topic="Contingency table: joint, marginal, conditional", difficulty="Medium",
            text=["A factory's output for one week, classified by shift and quality, is:",
                  ("table", [["Shift", "Good", "Defective", "Total"],
                             ["Day", "360", "40", "400"],
                             ["Night", "180", "20", "200"],
                             ["Total", "540", "60", "600"]]),
                  "An item is chosen at random from the 600. Which of the following is/are TRUE?"],
            options=["P(Defective) = 0.1",
                     "P(Night | Defective) = 1/3",
                     "The events 'Night shift' and 'Defective' are independent",
                     "P(Day ∩ Defective) = 0.4"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> Joint = cell/total; marginal = row or column total/total; conditional = cell/"
                "row (or column) total.",
                "<b>(A) TRUE.</b> P(D) = 60/600 = 0.1.",
                "<b>(B) TRUE.</b> P(N | D) = 20/60 = 1/3.",
                "<b>(C) TRUE.</b> P(N) = 200/600 = 1/3 and",
                r"$$P(N\cap D)=\dfrac{20}{600}=\dfrac{1}{30}=\dfrac{1}{3}\times\dfrac{1}{10}=P(N)\,P(D)",
                "Equivalently P(D | Night) = 20/200 = 0.1 = P(D | Day) = 40/400 — defect rate does not depend on shift.",
                "<b>(D) FALSE.</b> P(Day ∩ D) = 40/600 ≈ 0.067. The value 0.4 is not even a probability of this "
                "event: 40/400 = 0.1 is P(D | Day), and 40/60 ≈ 0.667 is P(Day | D).",
                ("note", "Night has fewer defectives (20 vs 40) only because it makes fewer items. Compare RATES, not "
                         "counts.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q17
        dict(
            qtype="NAT", marks=2, topic="Conditional expectation and variance (random sum)", difficulty="Medium",
            text="The number of severe storms N in a season follows a Poisson distribution with mean 4. Each storm, "
                 "independently, causes a flood with probability 0.25. Let X be the number of floods in the season. "
                 "Var(X) is ______ (round off to 2 decimal places).",
            answer=f"{Q17:.2f}", range=(0.99, 1.01),
            solution=[
                "<b>Concept:</b> Given N, X ∼ Bin(N, 0.25); apply Var(X) = E[Var(X | N)] + Var(E[X | N]).",
                r"$$E[X\mid N]=0.25N,\qquad \mathrm{Var}(X\mid N)=N(0.25)(0.75)=0.1875N",
                "For N ∼ Poisson(4): E[N] = Var(N) = 4.",
                r"$$E[\mathrm{Var}(X\mid N)]=0.1875\times 4=0.75",
                r"$$\mathrm{Var}(E[X\mid N])=0.25^2\times\mathrm{Var}(N)=0.0625\times 4=0.25",
                r"$$\mathrm{Var}(X)=0.75+0.25=%.2f" % Q17,
                "Also E[X] = E[E[X | N]] = 0.25 × 4 = 1. Mean = variance = 1 is no coincidence: a Poisson count "
                "'thinned' with probability p is again Poisson, here Poisson(λp) = Poisson(1).",
                ("note", "Thinning property: Poisson(λ) arrivals, each kept independently w.p. p ⇒ Poisson(λp). "
                         "A quick check of any random-sum calculation.", "Shortcut"),
            ],
        ),
        # ------------------------------------------------------------ Q18
        dict(
            qtype="MCQ", marks=2, topic="Conditional PDF", difficulty="Medium",
            text="The joint PDF of (X, Y) is f(x, y) = 6x for 0 &lt; x &lt; y &lt; 1 and 0 otherwise. The "
                 "conditional probability P(X &lt; 0.25 | Y = 0.5) is",
            options=["0.25", "0.50", "0.125", "0.0625"],
            answer="A",
            solution=[
                "<b>Concept:</b> f<sub>X|Y</sub>(x | y) = f(x, y)/f<sub>Y</sub>(y), then integrate over the "
                "required x-range on the slice Y = y.",
                ("fig", fig_region_q18),
                r"$$f_Y(y)=\int_0^y 6x\,dx=3y^2,\qquad 0<y<1",
                r"$$f_{X\mid Y}(x\mid y)=\dfrac{6x}{3y^2}=\dfrac{2x}{y^2},\qquad 0<x<y",
                "At y = 0.5: f<sub>X|Y</sub>(x | 0.5) = 2x/0.25 = 8x on (0, 0.5). (Check: ∫<sub>0</sub><super>0.5</super> 8x dx = 1.)",
                r"$$P(X<0.25\mid Y=0.5)=\int_0^{0.25}8x\,dx=4(0.25)^2=0.25",
                "0.50 assumes X is uniform on the slice (but the density 6x is not constant); 0.0625 = ∫<sub>0</sub><super>0.25</super> 2x dx "
                "forgets the division by y² = 0.25 in the conditional density.",
                ("note", "A conditional density must integrate to 1 over the slice — use this to check "
                         "normalisation.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q19
        dict(
            qtype="NAT", marks=2, topic="Joint PDF: normalisation and region probability", difficulty="Medium",
            text="The joint PDF of (X, Y) is f(x, y) = c(x + 2y) for 0 ≤ x ≤ 1, 0 ≤ y ≤ 1, and 0 elsewhere, where "
                 "c is a constant. P(X &gt; Y) is ______ (round off to 3 decimal places).",
            answer=f"{float(Q19):.3f}", range=(0.444, 0.445),
            solution=[
                "<b>Concept:</b> First find c from total probability = 1, then integrate over the region x &gt; y.",
                r"$$\int_0^1\int_0^1 c(x+2y)\,dy\,dx=c\left(\dfrac{1}{2}+1\right)=\dfrac{3c}{2}=1\ \Rightarrow\ c=\dfrac{2}{3}",
                ("fig", fig_region_q19),
                "Region below the diagonal: 0 ≤ y ≤ x ≤ 1.",
                r"$$\int_0^1\int_0^x(x+2y)\,dy\,dx=\int_0^1\left(x^2+x^2\right)dx=\dfrac{2}{3}",
                r"$$P(X>Y)=\dfrac{2}{3}\times\dfrac{2}{3}=\dfrac{4}{9}\approx %.4f" % float(Q19),
                f"Answer ≈ <b>{float(Q19):.3f}</b>. It is below 0.5 because the density puts more weight on large y.",
                ("note", "Forgetting c gives 2/3 — always normalise before computing probabilities.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q20
        dict(
            qtype="MSQ", marks=2, topic="Implications of independence (concept check)", difficulty="Medium",
            text="Let X and Y be <b>independent</b> random variables with finite, positive variances. Which of the "
                 "following is/are necessarily TRUE?",
            options=["Cov(X, Y) = 0", "E[XY] = E[X] E[Y]", "Var(XY) = Var(X) Var(Y)",
                     "X<super>2</super> and Y<super>2</super> are independent"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> Independence factorises the joint distribution, hence expectations of products of "
                "functions: E[g(X)h(Y)] = E[g(X)]E[h(Y)].",
                "<b>(B) TRUE</b> (take g, h = identity), hence <b>(A) TRUE</b>: Cov = E[XY] − E[X]E[Y] = 0.",
                "<b>(C) FALSE.</b> Using independence,",
                r"$$\mathrm{Var}(XY)=E[X^2]E[Y^2]-(E[X]E[Y])^2",
                "which equals Var(X)Var(Y) only when means vanish. Counter-example: X, Y i.i.d. Bernoulli(1/2): "
                "XY ∼ Bernoulli(1/4), Var(XY) = 3/16, but Var(X)Var(Y) = 1/16.",
                "<b>(D) TRUE.</b> Functions of independent random variables are independent.",
                ("note", "Independence is preserved by functions; zero covariance is not (that is why uncorrelated "
                         "≠ independent).", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q21
        dict(
            qtype="MCQ", marks=2, topic="Variance of a linear combination", difficulty="Medium",
            text="Daily rainfalls X and Y (in cm) at two nearby stations have Var(X) = 4, Var(Y) = 9 and correlation "
                 "coefficient 0.5. Var(2X − Y) equals",
            options=["13", "25", "37", "19"],
            answer="A",
            solution=[
                "<b>Concept:</b> Var(aX + bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X, Y), with Cov = ρσ<sub>X</sub>σ<sub>Y</sub>.",
                r"$$\mathrm{Cov}(X,Y)=0.5\times 2\times 3=3",
                r"$$\mathrm{Var}(2X-Y)=4(4)+(-1)^2(9)+2(2)(-1)(3)=16+9-12=13",
                "25 ignores the covariance; 37 adds it with the wrong sign (+12); 19 uses 2 × 2 × 3 × ½ = 6 instead "
                "of 12 for the cross term.",
                ("note", "Positively correlated variables partly cancel in a difference, so Var(2X − Y) is smaller "
                         "than the independent case (25).", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q22
        dict(
            qtype="NAT", marks=2, topic="Grouped data: mean and standard deviation", difficulty="Medium",
            text=["The scores (out of 10) of 20 students in a weekly quiz are summarised below:",
                  ("table", [["Score", "2", "4", "6", "8", "10"],
                             ["Frequency", "3", "5", "8", "3", "1"]]),
                  "The standard deviation of the scores, using divisor n (population formula), is ______ (round off "
                  "to 2 decimal places)."],
            answer=f"{Q22:.2f}", range=(2.10, 2.11),
            solution=[
                "<b>Concept:</b> σ² = (∑f x²)/n − x̄² for frequency data.",
                ("fig", fig_hist_q22),
                r"$$\bar{x}=\dfrac{3(2)+5(4)+8(6)+3(8)+1(10)}{20}=\dfrac{108}{20}=5.4",
                r"$$\dfrac{\sum f x^2}{n}=\dfrac{3(4)+5(16)+8(36)+3(64)+1(100)}{20}=\dfrac{672}{20}=33.6",
                r"$$\sigma^2=33.6-5.4^2=33.6-29.16=4.44",
                r"$$\sigma=\sqrt{4.44}\approx %.4f" % Q22,
                f"Answer ≈ <b>{Q22:.2f}</b>. (With divisor n − 1 one would get √(88.8/19) ≈ 2.16 — not asked here.)",
                ("note", "Multiply each value (and each square) by its frequency — averaging the five distinct "
                         "scores alone gives a wrong mean of 6.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q23
        dict(
            qtype="MCQ", marks=2, topic="Normal distribution: tolerance limits", difficulty="Medium",
            text="Diameters of bolts are normally distributed with mean 10.00 mm and standard deviation 0.02 mm. "
                 "A bolt is rejected if its diameter differs from 10.00 mm by more than 0.03 mm. The proportion of "
                 "bolts rejected is closest to [Φ(1.5) = 0.9332]",
            options=["0.0668", "0.1336", "0.8664", "0.0456"],
            answer="B",
            solution=[
                "<b>Concept:</b> P(|X − μ| &gt; d) = 2[1 − Φ(d/σ)] by symmetry.",
                r"$$z=\dfrac{0.03}{0.02}=1.5",
                r"$$P(\text{reject})=P(|Z|>1.5)=2(1-0.9332)=2(0.0668)=0.1336",
                ("fig", fig_norm_q23),
                "0.0668 counts only one tail; 0.8664 is the acceptance proportion; 0.0456 = P(|Z| &gt; 2).",
                ("note", "Two-sided tolerance ⇒ two tails. Draw both rejection regions.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q24
        dict(
            qtype="NAT", marks=2, topic="CLT for a sum of uniforms", difficulty="Medium",
            text="Each of 48 rain-gauge readings is truncated (rounded down) to a whole millimetre. The truncation "
                 "errors are independent and uniformly distributed on [0, 1] mm. Using the central limit theorem "
                 "(no continuity correction), the probability that the total truncation error exceeds 26 mm is "
                 "______ (round off to 3 decimal places). [Φ(1) = 0.8413]",
            answer=f"{Q24:.3f}", range=(0.158, 0.160),
            solution=[
                "<b>Concept:</b> For S = sum of n i.i.d. variables with mean μ and variance σ², "
                "S ≈ N(nμ, nσ²) for large n.",
                r"$$U\sim U(0,1):\quad E[U]=\dfrac{1}{2},\qquad \mathrm{Var}(U)=\dfrac{(1-0)^2}{12}=\dfrac{1}{12}",
                r"$$E[S]=48\times\dfrac{1}{2}=24,\qquad \mathrm{Var}(S)=\dfrac{48}{12}=4,\qquad \mathrm{SD}(S)=2",
                r"$$P(S>26)\approx P\left(Z>\dfrac{26-24}{2}\right)=1-\Phi(1)=0.1587",
                ("fig", fig_clt_q24),
                f"Answer ≈ <b>{Q24:.3f}</b>.",
                ("note", "Variances add for a sum (n σ²); the SD grows like √n, not n. Using SD = 48/√12 ≈ 13.9 "
                         "is a common blunder.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q25
        dict(
            qtype="MCQ", marks=2, topic="Confidence interval (z, σ known)", difficulty="Medium",
            text="Annual rainfall in a region is normally distributed with known standard deviation 8 cm. Records "
                 "for 16 randomly chosen years give a mean of 92 cm. The 99% confidence interval for the mean annual "
                 "rainfall is [z<sub>0.005</sub> = 2.576, z<sub>0.025</sub> = 1.96, z<sub>0.05</sub> = 1.645]",
            options=["(88.08, 95.92)", "(86.85, 97.15)", "(88.71, 95.29)", "(71.39, 112.61)"],
            answer="B",
            solution=[
                "<b>Concept:</b> σ known ⇒ x̄ ± z<sub>α/2</sub> σ/√n; for 99%, α/2 = 0.005.",
                r"$$\dfrac{\sigma}{\sqrt{n}}=\dfrac{8}{4}=2,\qquad 2.576\times 2=5.152",
                r"$$92\pm 5.152=(86.85,\ 97.15)",
                ("fig", fig_ci_q25),
                "(A) is the 95% interval, (C) the 90% interval; (D) uses σ instead of σ/√n (92 ± 20.61).",
                ("note", "Higher confidence ⇒ wider interval (for the same data). Width = 2 z σ/√n.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q26
        dict(
            qtype="NAT", marks=2, topic="z-test for a proportion: p-value", difficulty="Medium",
            text="To test whether a coin is fair, it is tossed 400 times and shows 224 heads. Using the normal "
                 "approximation (no continuity correction) for H<sub>0</sub>: p = 0.5 versus H<sub>1</sub>: p ≠ 0.5, "
                 "the two-sided p-value is ______ (round off to 3 decimal places). [Φ(2.4) = 0.9918]",
            answer=f"{Q26:.3f}", range=(0.016, 0.017),
            solution=[
                "<b>Concept:</b> Under H<sub>0</sub>, X ∼ Bin(400, 0.5) ≈ N(np, np(1 − p)); "
                "two-sided p-value = 2P(Z ≥ |z|).",
                r"$$np=200,\qquad \sqrt{np(1-p)}=\sqrt{100}=10",
                r"$$z=\dfrac{224-200}{10}=2.4",
                r"$$p\text{-value}=2\left[1-\Phi(2.4)\right]=2(0.0082)=0.0164",
                ("fig", fig_reject_q26),
                f"Answer ≈ <b>{Q26:.3f}</b>. Since 0.016 &lt; 0.05, fairness is rejected at 5% (but not at 1%).",
                ("note", "For a two-sided test, double the one-tail area. Reporting 0.0082 is the classic "
                         "half-p-value error.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q27
        dict(
            qtype="MCQ", marks=2, topic="χ² test of independence (2 × 2)", difficulty="Medium",
            text=["Two revision methods are compared on 100 students:",
                  ("table", [["Method", "Pass", "Fail", "Total"],
                             ["A", "40", "10", "50"],
                             ["B", "30", "20", "50"],
                             ["Total", "70", "30", "100"]]),
                  "Using the χ² test of independence without continuity correction at the 5% level "
                  "(χ²<sub>0.05, 1</sub> = 3.841, χ²<sub>0.05, 3</sub> = 7.815), which is correct?"],
            options=["χ² ≈ 4.76; reject independence of method and result",
                     "χ² ≈ 4.76; do not reject, since the critical value (3 df) is 7.815",
                     "χ² ≈ 2.38; do not reject independence",
                     "χ² ≈ 0.95; do not reject independence"],
            answer="A",
            solution=[
                "<b>Concept:</b> E<sub>ij</sub> = (row total)(column total)/n; χ² = ∑(O − E)²/E with "
                "(r − 1)(c − 1) df.",
                ("table", [["Cell", "O", "E", "(O − E)²/E"],
                           ["A, Pass", "40", "50·70/100 = 35", "25/35 = 0.714"],
                           ["A, Fail", "10", "50·30/100 = 15", "25/15 = 1.667"],
                           ["B, Pass", "30", "35", "0.714"],
                           ["B, Fail", "20", "15", "1.667"]]),
                r"$$\chi^2=2(0.7143)+2(1.6667)=%.3f" % Q27,
                "df = (2 − 1)(2 − 1) = 1; critical value 3.841. Since 4.76 &gt; 3.841, reject H<sub>0</sub>: pass rate "
                "depends on the method (80% vs 60%).",
                ("fig", fig_chi_q27),
                "(B) uses rc − 1 = 3 df; (C) sums only two cells; (D) is not a valid computation of the statistic.",
                ("note", "Degrees of freedom for an r × c table are (r − 1)(c − 1), not rc − 1.", "Trap"),
            ],
        ),
        # ------------------------------------------------------------ Q28
        dict(
            qtype="MCQ", marks=2, topic="Paired t-test", difficulty="Medium",
            text=["Six students take a test before and after a revision workshop:",
                  ("table", [["Student", "1", "2", "3", "4", "5", "6"],
                             ["Before", "52", "60", "58", "45", "70", "63"],
                             ["After", "55", "65", "57", "49", "72", "68"]]),
                  "Assume the differences (After − Before) are normal. For H<sub>0</sub>: μ<sub>d</sub> = 0 vs "
                  "H<sub>1</sub>: μ<sub>d</sub> &gt; 0 at the 5% level (t<sub>0.05, 5</sub> = 2.015), which is "
                  "correct?"],
            options=["t ≈ 3.22; reject H<sub>0</sub>", "t ≈ 3.22; do not reject H<sub>0</sub>",
                     "t ≈ 1.32; do not reject H<sub>0</sub>", "t ≈ 3.53; reject H<sub>0</sub>"],
            answer="A",
            solution=[
                "<b>Concept:</b> Paired data ⇒ one-sample t-test on the differences: t = d̄/(s<sub>d</sub>/√n), "
                "n − 1 df.",
                ("table", [["d", "3", "5", "−1", "4", "2", "5"],
                           ["d − d̄", "0", "2", "−4", "1", "−1", "2"],
                           ["(d − d̄)²", "0", "4", "16", "1", "1", "4"]]),
                r"$$\bar{d}=\dfrac{18}{6}=3,\qquad s_d^2=\dfrac{26}{5}=5.2,\qquad s_d=%.4f" % Q28_s,
                r"$$t=\dfrac{3}{%.4f/\sqrt{6}}=\dfrac{3}{%.4f}\approx %.3f" % (Q28_s, Q28_s / sqrt(6), Q28),
                "With 5 df, critical value 2.015. Since 3.22 &gt; 2.015, reject H<sub>0</sub>: the workshop improves "
                "scores on average.",
                "(C) forgets √n (3/2.28); (D) uses divisor n for s<sub>d</sub> (√(26/6) = 2.08) — the conclusion "
                "agrees but the statistic is wrong.",
                ("note", "Do not run a two-sample test on paired data — pairing removes student-to-student "
                         "variation, which is exactly why it is powerful.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q29
        dict(
            qtype="MSQ", marks=2, topic="Sampling distribution of the mean, CLT (concept check)", difficulty="Medium",
            text="Let X<sub>1</sub>, …, X<sub>n</sub> be i.i.d. with mean μ and finite variance σ<super>2</super> "
                 "(population shape unknown), and let X̄ be their sample mean. Which of the following is/are TRUE?",
            options=["E[X̄] = μ for every n",
                     "Var(X̄) = σ<super>2</super>/n",
                     "For large n, the distribution of X̄ is approximately normal",
                     "For large n, each individual X<sub>i</sub> is approximately normal"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> Linearity gives the mean and variance of X̄ exactly; the CLT describes the SHAPE of "
                "X̄'s distribution for large n.",
                "<b>(A) TRUE.</b> E[X̄] = (1/n)∑E[X<sub>i</sub>] = μ — unbiased for any n.",
                "<b>(B) TRUE.</b> Independence ⇒ Var(X̄) = (1/n²)·nσ² = σ²/n.",
                "<b>(C) TRUE.</b> Central limit theorem (finite variance).",
                "<b>(D) FALSE.</b> The population does not change with n; a die roll stays discrete uniform. Only "
                "averages (or sums) become bell-shaped:",
                ("fig", fig_clt_q29),
                ("note", "(A) and (B) are exact for all n and need no normality; (C) is an approximation for "
                         "large n.", "Key idea"),
            ],
        ),
        # ------------------------------------------------------------ Q30
        dict(
            qtype="MSQ", marks=2, topic="Logic of tests and intervals (concept check)", difficulty="Medium",
            text="Which of the following statements about hypothesis tests and confidence intervals is/are TRUE?",
            options=["If the 95% two-sided z-interval for μ excludes μ<sub>0</sub>, the two-sided z-test of "
                     "H<sub>0</sub>: μ = μ<sub>0</sub> rejects H<sub>0</sub> at the 5% level.",
                     "A p-value of 0.03 means there is a 3% probability that H<sub>0</sub> is true.",
                     "For the same data, a 99% confidence interval is wider than a 95% confidence interval.",
                     "In a χ² goodness-of-fit test with k categories and no estimated parameters, the degrees of "
                     "freedom are k − 1."],
            answer="A, C, D",
            solution=[
                "<b>Concept:</b> Two-sided tests and intervals are duals: H<sub>0</sub> is rejected at level α "
                "exactly when μ<sub>0</sub> lies outside the (1 − α) interval.",
                "<b>(A) TRUE.</b> μ<sub>0</sub> outside x̄ ± 1.96σ/√n ⇔ |x̄ − μ<sub>0</sub>|/(σ/√n) &gt; 1.96 ⇔ reject.",
                "<b>(B) FALSE.</b> The p-value is P(data at least this extreme | H<sub>0</sub> true), not "
                "P(H<sub>0</sub> | data).",
                "<b>(C) TRUE.</b> 2.576 &gt; 1.96, so the margin grows.",
                "<b>(D) TRUE.</b> The k counts are constrained to sum to n, losing one df.",
                ("note", "The p-value is a probability about the DATA computed assuming H<sub>0</sub> — never the "
                         "probability that H<sub>0</sub> is true.", "Trap"),
            ],
        ),
    ],
}
