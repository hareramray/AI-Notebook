"""Mock Test 05 - Topic Test: Probability, Counting, Bayes & Conditional Expectation."""
import math
from fractions import Fraction as Fr
from itertools import product
from math import comb, factorial

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"


# ====================================================================== computed answers
# Q1 stars and bars, each child >= 1
A1 = comb(9, 3)
# Q3
A3 = (0.6 - (0.6 + 0.5 - 0.75)) / 0.5
# Q5 derangements of 5
D = [1, 0]
for n in range(2, 8):
    D.append((n - 1) * (D[-1] + D[-2]))
A5 = Fr(D[5], factorial(5))
# Q6
A6 = 3.5 * 0.5
# Q7
A7 = 1 - (12 * 11 * 10 * 9 * 8) / 12 ** 5
# Q8
A8 = factorial(9) // (factorial(3) ** 3 * factorial(3))
# Q10
A10 = Fr(comb(4, 2), comb(52, 2)) / (1 - Fr(comb(48, 2), comb(52, 2)))
# Q11
A11 = 0.5 * 0.01 + 0.3 * 0.02 + 0.2 * 0.03
# Q13
A13 = Fr(3, 5) * Fr(3, 7) / (Fr(3, 5) * Fr(3, 7) + Fr(2, 5) * Fr(2, 7))
# Q14
A14 = sum(1 for t in product(range(6), repeat=4) if sum(t) == 12)
# Q15
VAR15 = 4 * 10 ** 2 + 4 * 50 ** 2
A15 = math.sqrt(VAR15)
# Q16
T16 = {(1, 0): .10, (2, 0): .20, (3, 0): .10, (1, 1): .25, (2, 1): .05, (3, 1): .30}
A16 = Fr(125, 60)
# Q18
A18 = sum(1 for n in range(1, 1001) if n % 2 and n % 3 and n % 5)
# Q20
P20_pos = 0.02 * 0.9 + 0.98 * 0.05
P20_1 = 0.02 * 0.9 / P20_pos
P20_2 = 0.02 * 0.81 / (0.02 * 0.81 + 0.98 * 0.05 ** 2)
# Q21
A21 = 6 * (1 - (5 / 6) ** 10)
# Q23 joint pmf c(x+2y)
PM23 = {(x, y): Fr(x + 2 * y, 12) for x in range(3) for y in range(2)}
EX23 = sum(x * p for (x, y), p in PM23.items())
EY23 = sum(y * p for (x, y), p in PM23.items())
EXY23 = sum(x * y * p for (x, y), p in PM23.items())
A23 = EXY23 - EX23 * EY23
# Q24
A24 = Fr(1, 6) / (1 - Fr(5, 6) * Fr(2, 3))
# Q26
A26 = (1 + 0.6) / 0.6 ** 2
# Q27
A27_tot = sum(comb(5, k) * comb(6, 5 - k) for k in range(2, 6))
A27_bad = comb(9, 3) - comb(5, 3)
A27 = A27_tot - A27_bad
# Q28
A28 = 0.5 * math.log(2)
# Q29
q29 = 2 * 0.1 * 0.9
A29 = 0.7 * (1 - q29) / (0.7 * (1 - q29) + 0.3 * q29)


# ====================================================================== figures
def _tree(ax, root, branches, title=None):
    """branches: list of (label, prob_label, [(leaf_label, prob_label, highlight)])"""
    ax.axis("off")
    ax.set_xlim(-0.1, 3.3)
    n1 = len(branches)
    ys1 = np.linspace(0.85, 0.15, n1)
    ax.text(0, 0.5, root, ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", fc="white", ec=BLUE))
    for (lab, pl, leaves), y1 in zip(branches, ys1):
        ax.plot([0.15, 1.2], [0.5, y1], color=BLUE, lw=1.2)
        ax.text(0.65, (0.5 + y1) / 2 + 0.035, pl, fontsize=8.5, color=MAROON, ha="center")
        ax.text(1.35, y1, lab, ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round", fc="#eaf2f8", ec=BLUE))
        k = len(leaves)
        span = 0.32 / max(n1 - 1, 1) if n1 > 1 else 0.3
        ys2 = np.linspace(y1 + span / 2, y1 - span / 2, k) if k > 1 else [y1]
        for (ll, lp, hi), y2 in zip(leaves, ys2):
            ax.plot([1.55, 2.5], [y1, y2], color=BLUE, lw=1.0)
            ax.text(2.02, (y1 + y2) / 2 + 0.03, lp, fontsize=8, color=MAROON, ha="center")
            ax.text(2.6, y2, ll, ha="left", va="center", fontsize=8.5,
                    bbox=dict(boxstyle="round", fc=GOLD if hi else "white", ec="#888888",
                              alpha=0.9))
    if title:
        ax.set_title(title, fontsize=9)


def fig_venn_q3():
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.add_patch(Circle((0.38, 0.5), 0.3, fc=BLUE, alpha=0.25, ec=BLUE, lw=1.5))
    ax.add_patch(Circle((0.66, 0.5), 0.3, fc=MAROON, alpha=0.2, ec=MAROON, lw=1.5))
    ax.text(0.25, 0.5, "A∩B$^c$\n0.25", ha="center", va="center", fontsize=10)
    ax.text(0.52, 0.5, "A∩B\n0.35", ha="center", va="center", fontsize=10)
    ax.text(0.80, 0.5, "A$^c$∩B\n0.15", ha="center", va="center", fontsize=10)
    ax.text(0.05, 0.08, "outside: 0.25", fontsize=9)
    ax.text(0.2, 0.86, "A", color=BLUE, fontsize=12, weight="bold")
    ax.text(0.86, 0.86, "B", color=MAROON, fontsize=12, weight="bold")
    ax.add_patch(plt.Rectangle((0, 0), 1.04, 1, fill=False, ec="#555555"))
    ax.set_xlim(-0.02, 1.06)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def fig_derange_q5():
    n = np.arange(1, 9)
    Dn = [0, 1, 2, 9, 44, 265, 1854, 14833]
    ratio = [d / math.factorial(k) for d, k in zip(Dn, n)]
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.bar(n, ratio, color=[MAROON if k == 5 else BLUE for k in n], alpha=0.8, width=0.6)
    ax.axhline(1 / math.e, color=GOLD, lw=2, ls="--", label="1/e ≈ 0.3679")
    for k, r in zip(n, ratio):
        ax.text(k, r + 0.015, f"{r:.3f}", ha="center", fontsize=7.5)
    ax.set_xlabel("n (letters)")
    ax.set_ylabel("$D_n / n!$")
    ax.set_ylim(0, 0.6)
    ax.legend(fontsize=8, frameon=False)
    ax.set_title("P(no letter in its own envelope)", fontsize=9)
    return fig


def _heat(ax, M, xlabels, ylabels, xname, yname, fmt):
    ax.imshow(M, cmap="Blues", vmin=0, vmax=M.max() * 1.4)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, fmt(M[i, j]), ha="center", va="center", fontsize=10, color="#1d2433")
    ax.set_xticks(range(len(xlabels)))
    ax.set_xticklabels(xlabels)
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    for s in ax.spines.values():
        s.set_visible(False)


def fig_jpmf_q9():
    M = np.array([[0.10, 0.20, 0.10], [0.15, 0.30, 0.15]])
    fig, ax = plt.subplots(figsize=(4.6, 2.4))
    _heat(ax, M, ["y = 0", "y = 1", "y = 2"], ["x = 0", "x = 1"], "Y", "X", lambda v: f"{v:.2f}")
    ax.set_title("Joint PMF  P(X = x, Y = y)", fontsize=9)
    return fig


def fig_tree_q13():
    fig, ax = plt.subplots(figsize=(6, 3.0))
    _tree(ax, "Urn I", [
        ("White moved", "3/5", [("II: 3W,4B → draw W", "3/7", True), ("draw B", "4/7", False)]),
        ("Black moved", "2/5", [("II: 2W,5B → draw W", "2/7", True), ("draw B", "5/7", False)]),
    ])
    return fig


def fig_region_q19():
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.fill_between([0, 1], [0, 0], [0, 1], color=BLUE, alpha=0.25)
    ax.plot([0, 1], [0, 1], color=BLUE)
    ax.plot([0.6, 0.6], [0, 0.6], color=MAROON, lw=2.2)
    ax.text(0.62, 0.25, "given X = x,\nY ∼ U(0, x)", color=MAROON, fontsize=8.5)
    ax.text(0.15, 0.6, "y = x", color=BLUE, fontsize=9)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.set_title("Support of (X, Y): 0 &lt; y &lt; x &lt; 1".replace("&lt;", "<"), fontsize=9)
    return fig


def fig_tree_q20():
    fig, ax = plt.subplots(figsize=(6, 3.0))
    _tree(ax, "Person", [
        ("Diseased", "0.02", [("+ +", "0.9 × 0.9 = 0.81", True), ("other", "0.19", False)]),
        ("Healthy", "0.98", [("+ +", "0.05 × 0.05 = 0.0025", True), ("other", "0.9975", False)]),
    ])
    return fig


def fig_jpmf_q23():
    M = np.array([[float(PM23[(x, y)]) for x in range(3)] for y in range(2)])
    fig, ax = plt.subplots(figsize=(4.6, 2.4))
    _heat(ax, M, ["x = 0", "x = 1", "x = 2"], ["y = 0", "y = 1"], "X", "Y",
          lambda v: f"{round(v * 12)}/12")
    ax.set_title("p(x, y) = (x + 2y)/12", fontsize=9)
    return fig


def fig_pmf_q25():
    fig, axs = plt.subplots(1, 2, figsize=(6, 2.5))
    axs[0].bar([-2, -1, 0, 1, 2], [0.2] * 5, color=BLUE, width=0.5)
    axs[0].set_title("PMF of X", fontsize=9)
    axs[0].set_ylim(0, 0.5)
    axs[1].bar([0, 1, 4], [0.2, 0.4, 0.4], color=MAROON, width=0.5)
    axs[1].set_xticks([0, 1, 4])
    axs[1].set_title("PMF of Y = X²", fontsize=9)
    axs[1].set_ylim(0, 0.5)
    for a in axs:
        a.set_ylabel("probability")
    fig.tight_layout()
    return fig


def fig_region_q28():
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    x = np.linspace(0.5, 1, 200)
    ax.fill_between(x, 0, 1 / (4 * x), color=MAROON, alpha=0.3, label="xy < 1/4")
    ax.fill_between(x, 1 / (4 * x), 1, color=BLUE, alpha=0.12)
    ax.plot(x, 1 / (4 * x), color=MAROON)
    ax.plot([0.5, 0.5], [0, 1], color="#555555", ls="--")
    ax.text(0.73, 0.75, "xy ≥ 1/4", color=BLUE, fontsize=9)
    ax.text(0.53, 0.18, "xy < 1/4", color=MAROON, fontsize=9)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.set_title("Conditioning strip x > 1/2 (area 1/2)", fontsize=9)
    return fig


def fig_tree_q29():
    fig, ax = plt.subplots(figsize=(6, 3.0))
    _tree(ax, "Source", [
        ("Sent 1", "0.7", [("Received 1", "0.82", True), ("Received 0", "0.18", False)]),
        ("Sent 0", "0.3", [("Received 1", "0.18", True), ("Received 0", "0.82", False)]),
    ])
    return fig


def _f(x, d=4):
    return f"{x:.{d}f}"


# ====================================================================== questions
Q = []

# ---------------- Q1
Q.append(dict(
    qtype="MCQ", marks=1, topic="Counting: stars and bars", difficulty="Easy",
    text="A teacher distributes 10 identical reward stickers among 4 students so that every "
         "student receives at least one sticker. The number of possible distributions is",
    options=["286", "120", f"{A1}", "210"],
    answer="C",
    solution=[
        "<b>Concept:</b> the number of positive integer solutions of x<sub>1</sub> + … + x<sub>k</sub> = n "
        "is C(n − 1, k − 1) (stars and bars with every bin non-empty).",
        "Let x<sub>i</sub> ≥ 1 be the stickers of student i. Then",
        r"$$x_1+x_2+x_3+x_4=10,\quad x_i\geq 1",
        "Substitute y<sub>i</sub> = x<sub>i</sub> − 1 ≥ 0, giving y<sub>1</sub>+…+y<sub>4</sub> = 6 with "
        "non-negative integers:",
        r"$$\binom{6+4-1}{4-1}=\binom{9}{3}=84",
        "Why the others are wrong: 286 = C(13, 3) counts distributions where a student may get zero; "
        "120 = C(10, 3) and 210 = C(10, 4) come from mis-placing the −1.",
        ("note", "Stickers identical, students distinct → stars and bars. If the stickers were distinct the "
                 "answer would be a surjection count (inclusion–exclusion), not a binomial.", "Trap"),
    ],
))

# ---------------- Q2
Q.append(dict(
    qtype="MCQ", marks=1, topic="Mutually exclusive vs independent", difficulty="Easy",
    text="Events A and B are mutually exclusive with P(A) = 0.3 and P(B) = 0.4. Which statement is TRUE?",
    options=["A and B are independent",
             "A and B are dependent, and P(A | B) = 0",
             "P(A ∪ B) = P(A) + P(B) − P(A)P(B) = 0.58",
             "P(A | B) = P(A) = 0.3"],
    answer="B",
    solution=[
        "<b>Concept:</b> mutually exclusive means P(A ∩ B) = 0; independent means P(A ∩ B) = P(A)P(B). "
        "Both can hold only if P(A) = 0 or P(B) = 0.",
        r"$$P(A\cap B)=0\neq P(A)P(B)=0.3\times 0.4=0.12",
        "Hence A and B are <b>dependent</b>. Moreover",
        r"$$P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}=\dfrac{0}{0.4}=0",
        "(A) false (shown above). (C) false: for disjoint events P(A ∪ B) = 0.3 + 0.4 = 0.7, the "
        "product formula is for independent events. (D) false: P(A | B) = 0 ≠ 0.3.",
        ("note", "Learning that B occurred tells you A certainly did NOT occur — the strongest possible "
                 "dependence. Disjoint events with positive probabilities are never independent.", "Key idea"),
    ],
))

# ---------------- Q3
Q.append(dict(
    qtype="NAT", marks=1, topic="Conditional probability, set algebra", difficulty="Easy",
    text="For events A and B, P(A) = 0.6, P(B) = 0.5 and P(A ∪ B) = 0.75. The value of "
         "P(A | B<super>c</super>) is ______ (round off to 2 decimal places).",
    answer=f"{A3:.2f}", range=(0.50, 0.50),
    solution=[
        "<b>Concept:</b> P(A | B<super>c</super>) = P(A ∩ B<super>c</super>) / P(B<super>c</super>), with "
        "P(A ∩ B<super>c</super>) = P(A) − P(A ∩ B).",
        "Step 1 (addition rule):",
        r"$$P(A\cap B)=P(A)+P(B)-P(A\cup B)=0.6+0.5-0.75=0.35",
        "Step 2: P(A ∩ B<super>c</super>) = 0.6 − 0.35 = 0.25 and P(B<super>c</super>) = 1 − 0.5 = 0.5.",
        r"$$P(A\mid B^c)=\dfrac{0.25}{0.5}=0.50",
        ("fig", fig_venn_q3),
        ("note", "Check: P(A ∩ B) = 0.35 ≠ P(A)P(B) = 0.30, so A and B are dependent; hence "
                 "P(A | B<super>c</super>) differs from P(A) = 0.6.", "Key idea"),
    ],
))

# ---------------- Q4
Q.append(dict(
    qtype="MSQ", marks=1, topic="Probability axioms & set algebra", difficulty="Medium",
    text="For ANY two events A and B in a probability space, which of the following is/are ALWAYS TRUE? "
         "(A Δ B denotes the symmetric difference (A ∩ B<super>c</super>) ∪ (A<super>c</super> ∩ B).)",
    options=["P(A ∩ B) ≥ P(A) + P(B) − 1",
             "P(A ∪ B) ≤ P(A) + P(B)",
             "P(A ∩ B<super>c</super>) = P(A) − P(B)",
             "P(A Δ B) = P(A) + P(B) − 2P(A ∩ B)"],
    answer="A, B, D",
    solution=[
        "<b>Concept:</b> everything follows from the axioms plus the inclusion–exclusion identity "
        "P(A ∪ B) = P(A) + P(B) − P(A ∩ B).",
        "<b>(A) TRUE</b> (Bonferroni): since P(A ∪ B) ≤ 1,",
        r"$$P(A\cap B)=P(A)+P(B)-P(A\cup B)\geq P(A)+P(B)-1",
        "<b>(B) TRUE</b> (Boole): P(A ∪ B) = P(A) + P(B) − P(A ∩ B) ≤ P(A) + P(B) because P(A ∩ B) ≥ 0.",
        "<b>(C) FALSE</b>: the correct identity is P(A ∩ B<super>c</super>) = P(A) − P(A ∩ B). It equals "
        "P(A) − P(B) only when B ⊂ A. Counter-example: A, B disjoint with P(A) = 0.2, P(B) = 0.5 gives "
        "0.2 on the left but −0.3 on the right.",
        "<b>(D) TRUE</b>: A Δ B is the disjoint union of A ∩ B<super>c</super> and A<super>c</super> ∩ B:",
        r"$$[P(A)-P(A\cap B)]+[P(B)-P(A\cap B)]=P(A)+P(B)-2P(A\cap B)",
        ("note", "A probability can never be negative — any 'identity' that can produce a negative value "
                 "for some valid inputs (like option C) must be false in general.", "Shortcut"),
    ],
))

# ---------------- Q5
Q.append(dict(
    qtype="MCQ", marks=1, topic="Derangements (inclusion–exclusion)", difficulty="Medium",
    text="Five letters are written to five different people and the five addressed envelopes are filled "
         "at random, one letter per envelope. The probability that NO letter goes into its correct "
         "envelope is",
    options=[f"{A5.numerator}/{A5.denominator}", "53/144", "3/8", "1/5"],
    answer="A",
    solution=[
        "<b>Concept:</b> the number of derangements of n objects is "
        "D<sub>n</sub> = n! ∑<sub>k=0..n</sub> (−1)<super>k</super>/k!, obtained by inclusion–exclusion "
        "on the events 'letter i is correct'.",
        r"$$D_5=5!\left(1-1+\dfrac{1}{2!}-\dfrac{1}{3!}+\dfrac{1}{4!}-\dfrac{1}{5!}\right)",
        r"$$D_5=120\left(\dfrac{1}{2}-\dfrac{1}{6}+\dfrac{1}{24}-\dfrac{1}{120}\right)=60-20+5-1=44",
        r"$$P(\text{no match})=\dfrac{44}{120}=\dfrac{11}{30}\approx 0.3667",
        "Distractors: 3/8 = D<sub>4</sub>/4! and 53/144 = D<sub>6</sub>/6! (wrong n); 1/5 is the chance a "
        "particular letter is correct.",
        ("fig", fig_derange_q5),
        ("note", "D<sub>n</sub>/n! converges to 1/e ≈ 0.3679 extremely fast; for n ≥ 5 it is within 0.002. "
                 "Recursion D<sub>n</sub> = (n − 1)(D<sub>n−1</sub> + D<sub>n−2</sub>) is handy for small n.",
         "Shortcut"),
    ],
))

# ---------------- Q6
Q.append(dict(
    qtype="NAT", marks=1, topic="Law of total expectation", difficulty="Easy",
    text="A fair six-sided die is rolled once; if it shows k, a fair coin is tossed k times. Let X be the "
         "number of heads obtained. Then E[X] = ______ (round off to 2 decimal places).",
    answer=f"{A6:.2f}", range=(1.75, 1.75),
    solution=[
        "<b>Concept:</b> law of total (iterated) expectation E[X] = E[ E[X | K] ].",
        "Given K = k, X ∼ Binomial(k, 1/2), so E[X | K] = K/2.",
        r"$$E[X]=E\left[\dfrac{K}{2}\right]=\dfrac{1}{2}\cdot\dfrac{1+2+3+4+5+6}{6}=\dfrac{3.5}{2}=1.75",
        ("note", "There is no need for the PMF of X; condition on the random number of trials, then average.",
         "Key idea"),
    ],
))

# ---------------- Q7
Q.append(dict(
    qtype="MCQ", marks=1, topic="Counting: complementary probability", difficulty="Easy",
    text="Five people are selected at random. Assuming each person's birth month is equally likely to be "
         "any of the 12 months, independently of the others, the probability that at least two of them "
         "share a birth month is closest to",
    options=["0.382", "0.417", "0.583", f"{A7:.3f}"],
    answer="D",
    solution=[
        "<b>Concept:</b> P(at least one repeat) = 1 − P(all different); count ordered assignments.",
        "All-distinct assignments: 12·11·10·9·8 = 95040 out of 12<super>5</super> = 248832.",
        r"$$P(\text{all different})=\dfrac{12\cdot 11\cdot 10\cdot 9\cdot 8}{12^5}=\dfrac{95040}{248832}\approx 0.3819",
        r"$$P(\text{at least two share})=1-0.3819=0.6181",
        "0.382 is the complement (all different). 0.417 = 5/12 and 0.583 = 7/12 arise from wrongly treating "
        "the problem as a single comparison.",
        ("note", "'At least one coincidence' → always go through the complement 'all distinct'.", "Shortcut"),
    ],
))

# ---------------- Q8
Q.append(dict(
    qtype="MCQ", marks=1, topic="Multinomial counting (unlabelled groups)", difficulty="Medium",
    text="Nine students are to be split into three study circles of three students each. The circles are "
         "NOT named or distinguished in any way. The number of ways of doing this is",
    options=["1680", f"{A8}", "84", "560"],
    answer="B",
    solution=[
        "<b>Concept:</b> multinomial coefficient n!/(n<sub>1</sub>! n<sub>2</sub>! …) counts splits into "
        "LABELLED groups; divide by (number of equal-size groups)! when groups are unlabelled.",
        "Labelled circles (Circle 1, 2, 3):",
        r"$$\dfrac{9!}{3!\,3!\,3!}=\dfrac{362880}{216}=1680",
        "The 3! orderings of the same three circles give the same partition, so",
        r"$$\dfrac{1680}{3!}=280",
        "1680 forgets the over-counting; 84 = C(9, 3) chooses only one circle; 560 = 1680/3 divides by "
        "the wrong factor.",
        ("note", "Divide by k! only for groups of EQUAL size that are indistinguishable. Groups of sizes "
                 "2, 3, 4 would need no division.", "Trap"),
    ],
))

# ---------------- Q9
Q.append(dict(
    qtype="MSQ", marks=1, topic="Joint PMF, marginals, independence", difficulty="Easy",
    text=["The joint PMF of discrete random variables X and Y is shown below.",
          ("fig", fig_jpmf_q9),
          "Which of the following is/are TRUE?"],
    options=["X and Y are independent", "P(X + Y = 2) = 0.30", "E[Y] = 1", "P(X = 1 | Y = 2) = 0.4"],
    answer="A, C",
    solution=[
        "<b>Concept:</b> X, Y independent ⇔ p(x, y) = p<sub>X</sub>(x) p<sub>Y</sub>(y) for EVERY cell.",
        ("table", [["", "y = 0", "y = 1", "y = 2", "p<sub>X</sub>(x)"],
                   ["x = 0", "0.10", "0.20", "0.10", "0.40"],
                   ["x = 1", "0.15", "0.30", "0.15", "0.60"],
                   ["p<sub>Y</sub>(y)", "0.25", "0.50", "0.25", "1"]]),
        "<b>(A) TRUE</b>: 0.4×0.25 = 0.10, 0.4×0.5 = 0.20, 0.6×0.25 = 0.15, 0.6×0.5 = 0.30 — every cell "
        "factorises.",
        "<b>(B) FALSE</b>: X + Y = 2 at (0, 2) and (1, 1): 0.10 + 0.30 = 0.40.",
        "<b>(C) TRUE</b>: E[Y] = 0(0.25) + 1(0.5) + 2(0.25) = 1.",
        "<b>(D) FALSE</b>: P(X = 1 | Y = 2) = 0.15/0.25 = 0.6 (= P(X = 1), as independence demands).",
        ("note", "Rows proportional to each other (0.10 : 0.20 : 0.10 and 0.15 : 0.30 : 0.15) is a quick "
                 "visual test of independence.", "Shortcut"),
    ],
))

# ---------------- Q10
Q.append(dict(
    qtype="NAT", marks=1, topic="Conditional probability (counting)", difficulty="Medium",
    text="Two cards are drawn at random without replacement from a well-shuffled standard deck of 52 "
         "cards. Given that at least one of them is an ace, the probability that both are aces is ______ "
         "(round off to 4 decimal places).",
    answer=f"{float(A10):.4f}", range=(0.0300, 0.0306),
    solution=[
        "<b>Concept:</b> P(both | at least one) = P(both)/P(at least one), since 'both' ⊂ 'at least one'.",
        r"$$P(\text{both})=\dfrac{\binom{4}{2}}{\binom{52}{2}}=\dfrac{6}{1326}",
        r"$$P(\text{at least one})=1-\dfrac{\binom{48}{2}}{\binom{52}{2}}=1-\dfrac{1128}{1326}=\dfrac{198}{1326}",
        r"$$P(\text{both}\mid \geq 1)=\dfrac{6}{198}=\dfrac{1}{33}\approx 0.0303",
        ("note", "Compare with P(both | the FIRST card is an ace) = 3/51 ≈ 0.0588. 'At least one' is a weaker "
                 "condition and gives a smaller answer.", "Trap"),
    ],
))

# ---------------- Q11
Q.append(dict(
    qtype="MCQ", marks=1, topic="Total probability", difficulty="Easy",
    text="An annotation team has three labellers who label 50%, 30% and 20% of all images. Their error "
         "rates are 1%, 2% and 3% respectively. The probability that a randomly chosen image is mislabelled is",
    options=["0.020", "0.060", f"{A11:.3f}", "0.006"],
    answer="C",
    solution=[
        "<b>Concept:</b> law of total probability P(E) = ∑ P(E | L<sub>i</sub>) P(L<sub>i</sub>) over a "
        "partition.",
        r"$$P(E)=0.5(0.01)+0.3(0.02)+0.2(0.03)=0.005+0.006+0.006=0.017",
        "0.020 is the unweighted mean of the error rates; 0.060 is their sum.",
        ("note", "The overall rate must lie between the smallest and largest conditional rates (1% and 3%).",
         "Shortcut"),
    ],
))

# ---------------- Q12
Q.append(dict(
    qtype="MSQ", marks=1, topic="Conditional expectation properties", difficulty="Medium",
    text="Let X and Y be random variables with finite variances. Which of the following is/are ALWAYS TRUE?",
    options=["If E[X | Y] = E[X] (a constant), then X and Y are independent",
             "E[ E[X | Y] ] = E[X]",
             "E[X | Y] is a constant (non-random) number",
             "Var(X) ≥ Var( E[X | Y] )"],
    answer="B, D",
    solution=[
        "<b>Concept:</b> E[X | Y] = g(Y) is a random variable; tower property and the law of total variance "
        "Var(X) = E[Var(X | Y)] + Var(E[X | Y]).",
        "<b>(A) FALSE</b>: mean-independence is weaker than independence. Example: Y ∈ {1, 2} equally likely, "
        "X | Y=1 ∼ ±1 and X | Y=2 ∼ ±2 (equally likely signs). E[X | Y] = 0 always, but |X| = Y, so they "
        "are dependent.",
        "<b>(B) TRUE</b>: tower property (law of total expectation).",
        "<b>(C) FALSE</b>: E[X | Y] = g(Y) changes with Y; only E[X | Y = y] for a fixed y is a number.",
        "<b>(D) TRUE</b>: from the law of total variance, since E[Var(X | Y)] ≥ 0,",
        r"$$\mathrm{Var}(X)=E[\mathrm{Var}(X\mid Y)]+\mathrm{Var}(E[X\mid Y])\geq \mathrm{Var}(E[X\mid Y])",
        ("note", "Independence ⇒ E[X | Y] = E[X] ⇒ Cov(X, Y) = 0, but neither arrow reverses.", "Key idea"),
    ],
))

# ---------------- Q13
Q.append(dict(
    qtype="NAT", marks=2, topic="Bayes theorem (two-stage experiment)", difficulty="Medium",
    text="Urn I contains 3 white and 2 black balls; Urn II contains 2 white and 4 black balls. One ball "
         "is drawn at random from Urn I and placed (unseen) into Urn II. A ball is then drawn at random "
         "from Urn II and is found to be white. The probability that the transferred ball was white is "
         "______ (round off to 3 decimal places).",
    answer=f"{float(A13):.3f}", range=(0.691, 0.693),
    solution=[
        "<b>Concept:</b> Bayes' theorem over the partition {transferred W, transferred B}, with likelihoods "
        "computed from the updated composition of Urn II.",
        "Let T<sub>W</sub>, T<sub>B</sub> be the colour transferred, and W the event that the second draw "
        "is white.",
        "Step 1 — priors: P(T<sub>W</sub>) = 3/5, P(T<sub>B</sub>) = 2/5.",
        "Step 2 — likelihoods: after T<sub>W</sub>, Urn II has 3W, 4B (7 balls); after T<sub>B</sub>, it "
        "has 2W, 5B.",
        r"$$P(W\mid T_W)=\dfrac{3}{7},\qquad P(W\mid T_B)=\dfrac{2}{7}",
        ("fig", fig_tree_q13),
        "Step 3 — total probability:",
        r"$$P(W)=\dfrac{3}{5}\cdot\dfrac{3}{7}+\dfrac{2}{5}\cdot\dfrac{2}{7}=\dfrac{9+4}{35}=\dfrac{13}{35}",
        "Step 4 — Bayes:",
        r"$$P(T_W\mid W)=\dfrac{9/35}{13/35}=\dfrac{9}{13}\approx 0.692",
        ("note", "Observing white raises the probability that white was transferred from the prior 0.600 to "
                 "0.692 — evidence pushes belief toward the hypothesis that makes it more likely.",
         "Key idea"),
    ],
))

# ---------------- Q14
Q.append(dict(
    qtype="MCQ", marks=2, topic="Bounded stars and bars via inclusion–exclusion", difficulty="Hard",
    text="A server allocates 12 identical jobs to 4 distinct worker machines; each machine can hold at "
         "most 5 jobs (a machine may receive 0 jobs). The number of possible allocations is",
    options=[f"{A14}", "455", "119", "131"],
    answer="A",
    solution=[
        "<b>Concept:</b> count non-negative solutions of x<sub>1</sub>+…+x<sub>4</sub> = 12 with "
        "x<sub>i</sub> ≤ 5 by inclusion–exclusion on the 'bad' events B<sub>i</sub> = {x<sub>i</sub> ≥ 6}.",
        "Step 1 — no upper bound:",
        r"$$N_0=\binom{12+3}{3}=\binom{15}{3}=455",
        "Step 2 — one machine overloaded: set x<sub>i</sub> = 6 + z<sub>i</sub>; remaining sum 6:",
        r"$$|B_i|=\binom{6+3}{3}=84,\qquad \sum|B_i|=4\times 84=336",
        "Step 3 — two machines overloaded: remaining sum 0, exactly one way:",
        r"$$|B_i\cap B_j|=\binom{0+3}{3}=1,\qquad \sum|B_i\cap B_j|=\binom{4}{2}\times 1=6",
        "Step 4 — three overloaded needs ≥ 18 &gt; 12 jobs: impossible.",
        r"$$N=455-336+6=125",
        "455 ignores the cap; 119 = 455 − 336 forgets to add back the double overlaps; 131 adds them twice.",
        ("note", "Alternating signs: subtract singles, ADD BACK pairs, subtract triples… Forgetting the pair "
                 "term is the commonest error.", "Trap"),
    ],
))

# ---------------- Q15
Q.append(dict(
    qtype="NAT", marks=2, topic="Law of total variance (random sum)", difficulty="Medium",
    text="The number N of customers entering a shop in an hour is Poisson with mean 4. Customer i spends "
         "an amount X<sub>i</sub> (in ₹) with mean 50 and standard deviation 10; the X<sub>i</sub> are i.i.d. "
         "and independent of N. Let S = X<sub>1</sub> + … + X<sub>N</sub> (S = 0 if N = 0). The standard "
         "deviation of S is ______ (round off to 2 decimal places).",
    answer=f"{A15:.2f}", range=(101.97, 101.99),
    solution=[
        "<b>Concept:</b> for a random sum, condition on N and use "
        "Var(S) = E[Var(S | N)] + Var(E[S | N]).",
        "Given N = n, S is a sum of n i.i.d. terms:",
        r"$$E[S\mid N]=50N,\qquad \mathrm{Var}(S\mid N)=100N",
        "First term:",
        r"$$E[\mathrm{Var}(S\mid N)]=100\,E[N]=100\times 4=400",
        "Second term (for Poisson, Var(N) = E[N] = 4):",
        r"$$\mathrm{Var}(E[S\mid N])=50^2\,\mathrm{Var}(N)=2500\times 4=10000",
        r"$$\mathrm{Var}(S)=400+10000=10400,\qquad \mathrm{SD}(S)=\sqrt{10400}\approx 101.98",
        "Also E[S] = E[N]E[X] = 200.",
        ("note", "Forgetting the second term (variability in the NUMBER of customers) gives SD = 20 — a huge "
                 "underestimate. The randomness of N dominates here.", "Trap"),
    ],
))

# ---------------- Q16
Q.append(dict(
    qtype="MCQ", marks=2, topic="Conditional expectation from a joint PMF", difficulty="Medium",
    text=["The joint PMF of X ∈ {1, 2, 3} and Y ∈ {0, 1} is given below.",
          ("table", [["", "X = 1", "X = 2", "X = 3"],
                     ["Y = 0", "0.10", "0.20", "0.10"],
                     ["Y = 1", "0.25", "0.05", "0.30"]]),
          "The value of E[X | Y = 1] is"],
    options=["2.05", "2", "1.25", "25/12"],
    answer="D",
    solution=[
        "<b>Concept:</b> E[X | Y = y] = ∑<sub>x</sub> x p(x, y) / p<sub>Y</sub>(y): renormalise the row.",
        "Step 1: P(Y = 1) = 0.25 + 0.05 + 0.30 = 0.60.",
        "Step 2: conditional PMF of X given Y = 1:",
        ("table", [["x", "1", "2", "3"], ["P(X = x | Y = 1)", "0.25/0.6 = 5/12", "0.05/0.6 = 1/12",
                                            "0.30/0.6 = 6/12"]]),
        r"$$E[X\mid Y=1]=1\cdot\dfrac{5}{12}+2\cdot\dfrac{1}{12}+3\cdot\dfrac{6}{12}=\dfrac{25}{12}\approx 2.083",
        "Distractors: 1.25 is ∑ x p(x, 1) without dividing by 0.6; 2.05 is the unconditional E[X]; 2 is "
        "E[X | Y = 0] = 0.8/0.4.",
        "Check of the tower property: E[X] = 0.4(2) + 0.6(25/12) = 0.8 + 1.25 = 2.05 (verified).",
        ("note", "A conditional PMF is just a row (or column) rescaled to sum to 1.", "Key idea"),
    ],
))

# ---------------- Q17
Q.append(dict(
    qtype="MSQ", marks=2, topic="Pairwise vs mutual independence", difficulty="Hard",
    text="Two fair dice are rolled. Define A = {first die shows an odd number}, B = {second die shows an "
         "odd number}, C = {the sum of the two dice is odd}. Which of the following is/are TRUE?",
    options=["A and C are independent",
             "A, B and C are mutually independent",
             "P(A ∩ B ∩ C) = 0",
             "B and C are independent"],
    answer="A, C, D",
    solution=[
        "<b>Concept:</b> mutual independence of three events needs all three pairwise product rules AND "
        "P(A ∩ B ∩ C) = P(A)P(B)P(C).",
        "Each die is odd with probability 1/2, so P(A) = P(B) = 1/2. The sum is odd iff exactly one die is odd:",
        r"$$P(C)=\dfrac{1}{2}\cdot\dfrac{1}{2}+\dfrac{1}{2}\cdot\dfrac{1}{2}=\dfrac{1}{2}",
        "<b>(A) TRUE</b>: A ∩ C = {first odd, second even}:",
        r"$$P(A\cap C)=\dfrac{1}{4}=P(A)P(C)",
        "<b>(D) TRUE</b>: by symmetry, P(B ∩ C) = P(second odd, first even) = 1/4 = P(B)P(C). (A and B are "
        "also independent, as the dice are independent.)",
        "<b>(C) TRUE</b>: if both dice are odd, the sum is even, so A ∩ B ∩ C = Ø.",
        "<b>(B) FALSE</b>: P(A ∩ B ∩ C) = 0 ≠ P(A)P(B)P(C) = 1/8. So the events are pairwise "
        "independent but not mutually independent.",
        ("note", "Knowing A and B together determines C completely, though any single one tells nothing about "
                 "another. Pairwise independence does NOT imply mutual independence.", "Key idea"),
    ],
))

# ---------------- Q18
Q.append(dict(
    qtype="NAT", marks=2, topic="Inclusion–exclusion counting", difficulty="Medium",
    text="The number of integers in {1, 2, …, 1000} that are divisible by NONE of 2, 3 and 5 is ______.",
    answer=f"{A18}", range=(A18, A18),
    solution=[
        "<b>Concept:</b> |A<sub>2</sub>∪A<sub>3</sub>∪A<sub>5</sub>| by inclusion–exclusion, with "
        "|A<sub>d</sub>| = ⌊1000/d⌋ and A<sub>d</sub> ∩ A<sub>e</sub> = A<sub>lcm(d,e)</sub>.",
        ("table", [["Set", "Count", "Set", "Count"],
                   ["A<sub>2</sub>", "500", "A<sub>6</sub>", "166"],
                   ["A<sub>3</sub>", "333", "A<sub>10</sub>", "100"],
                   ["A<sub>5</sub>", "200", "A<sub>15</sub>", "66"],
                   ["", "", "A<sub>30</sub>", "33"]]),
        r"$$|A_2\cup A_3\cup A_5|=(500+333+200)-(166+100+66)+33",
        r"$$=1033-332+33=734",
        r"$$\text{None}=1000-734=266",
        "Sanity check: the density of such numbers is (1 − 1/2)(1 − 1/3)(1 − 1/5) = 4/15, and "
        "1000 × 4/15 ≈ 266.7.",
        ("note", "Use the floor at every step (⌊1000/3⌋ = 333, ⌊1000/15⌋ = 66); using exact fractions "
                 "gives 266.7, which is not an integer count.", "Trap"),
    ],
))

# ---------------- Q19
Q.append(dict(
    qtype="MCQ", marks=2, topic="Conditional expectation & total variance (continuous)", difficulty="Hard",
    text="Let X ∼ Uniform(0, 1). Given X = x, let Y ∼ Uniform(0, x). Then Var(Y) equals",
    options=["1/48", "7/144", "1/36", "1/12"],
    answer="B",
    solution=[
        "<b>Concept:</b> law of total variance Var(Y) = E[Var(Y | X)] + Var(E[Y | X]).",
        ("fig", fig_region_q19),
        "Given X: Y ∼ U(0, X), so",
        r"$$E[Y\mid X]=\dfrac{X}{2},\qquad \mathrm{Var}(Y\mid X)=\dfrac{X^2}{12}",
        "Term 1 (E[X<super>2</super>] = 1/3 for U(0, 1)):",
        r"$$E\left[\dfrac{X^2}{12}\right]=\dfrac{1}{12}\cdot\dfrac{1}{3}=\dfrac{1}{36}",
        "Term 2 (Var(X) = 1/12):",
        r"$$\mathrm{Var}\left(\dfrac{X}{2}\right)=\dfrac{1}{4}\cdot\dfrac{1}{12}=\dfrac{1}{48}",
        r"$$\mathrm{Var}(Y)=\dfrac{1}{36}+\dfrac{1}{48}=\dfrac{4+3}{144}=\dfrac{7}{144}",
        "Check directly: E[Y] = E[X/2] = 1/4, E[Y<super>2</super>] = E[X<super>2</super>/3] = 1/9, so "
        "Var(Y) = 1/9 − 1/16 = 7/144 (verified).",
        "1/48 and 1/36 are the two components alone; 1/12 is the variance of a U(0, 1).",
        ("note", "Both pieces are needed: within-group spread E[Var(Y | X)] plus between-group spread "
                 "Var(E[Y | X]).", "Key idea"),
    ],
))

# ---------------- Q20
Q.append(dict(
    qtype="MSQ", marks=2, topic="Bayes with repeated tests", difficulty="Hard",
    text="A disease has prevalence 2%. A screening test has sensitivity 0.90 and false-positive rate 0.05. "
         "A person takes the test twice; given the disease status, the two results are independent. "
         "Which of the following is/are TRUE?",
    options=["The probability that a single test is positive is 0.067",
             "P(disease | one positive test) lies between 0.26 and 0.28",
             "P(disease | two positive tests) is greater than 0.85",
             "The two test results are (unconditionally) independent events"],
    answer="A, B, C",
    solution=[
        "<b>Concept:</b> Bayes' theorem; conditional independence given D does not give unconditional "
        "independence.",
        ("fig", fig_tree_q20),
        f"<b>(A) TRUE</b>: P(+) = 0.02(0.90) + 0.98(0.05) = 0.018 + 0.049 = {P20_pos:.3f}.",
        f"<b>(B) TRUE</b>: P(D | +) = 0.018/0.067 = {P20_1:.4f}.",
        "<b>(C) TRUE</b>: for two positives, multiply likelihoods (conditional independence):",
        r"$$P(D\mid ++)=\dfrac{0.02(0.81)}{0.02(0.81)+0.98(0.0025)}=\dfrac{0.0162}{0.01865}",
        f"$$P(D\\mid ++)\\approx {P20_2:.4f}",
        "<b>(D) FALSE</b>: P(++) = 0.01865 but P(+)<super>2</super> = 0.067<super>2</super> ≈ 0.00449. "
        "A first positive raises the chance of disease, which raises the chance of a second positive.",
        "Equivalently, sequential updating: the posterior after test 1 (0.2687) becomes the prior for test 2: "
        "0.2687(0.9)/[0.2687(0.9) + 0.7313(0.05)] ≈ 0.8686.",
        ("note", "A single positive from a rare-disease screen is usually a false alarm (≈ 73% here); a "
                 "confirmatory second test is what makes the diagnosis convincing.", "Key idea"),
    ],
))

# ---------------- Q21
Q.append(dict(
    qtype="NAT", marks=2, topic="Expectation via indicator random variables", difficulty="Medium",
    text="A fair die is rolled 10 times. The expected number of DISTINCT faces that appear is ______ "
         "(round off to 2 decimal places).",
    answer=f"{A21:.2f}", range=(5.02, 5.04),
    solution=[
        "<b>Concept:</b> write the count as a sum of indicators and use linearity of expectation "
        "(no independence needed).",
        "Let I<sub>j</sub> = 1 if face j appears at least once, j = 1, …, 6. The number of distinct faces is "
        "D = I<sub>1</sub> + … + I<sub>6</sub>.",
        r"$$E[I_j]=P(\text{face } j \text{ appears})=1-\left(\dfrac{5}{6}\right)^{10}",
        r"$$\left(\dfrac{5}{6}\right)^{10}\approx 0.16151",
        r"$$E[D]=6\left[1-\left(\dfrac{5}{6}\right)^{10}\right]=6(0.83849)\approx 5.03",
        ("note", "The indicators are dependent (they cannot all be 0), yet linearity still holds. This trick "
                 "turns hard PMFs into one-line expectations.", "Shortcut"),
    ],
))

# ---------------- Q22
Q.append(dict(
    qtype="MCQ", marks=2, topic="Permutations with repetition & restriction", difficulty="Medium",
    text="The number of distinct arrangements of the letters of the word BALLOON in which the two L's are "
         "NOT adjacent is",
    options=["1260", "360", "900", "1080"],
    answer="C",
    solution=[
        "<b>Concept:</b> permutations of a multiset: n!/(n<sub>1</sub>! n<sub>2</sub>! …); restriction via "
        "complement (glue the L's together).",
        "BALLOON has 7 letters: B, A, L×2, O×2, N.",
        r"$$\text{Total}=\dfrac{7!}{2!\,2!}=\dfrac{5040}{4}=1260",
        "Treat 'LL' as one block: 6 objects (B, A, LL, O, O, N) with O repeated:",
        r"$$\text{L's together}=\dfrac{6!}{2!}=360",
        r"$$\text{L's apart}=1260-360=900",
        "1260 ignores the restriction; 360 is the complement; 1080 = 1260 − 180 comes from wrongly dividing "
        "6! by 2!·2! after gluing (once glued, LL is a single object and is no longer a repeated letter).",
        ("note", "Gap method check: arrange B, A, O, O, N in 5!/2! = 60 ways, choose 2 of the 6 gaps for the "
                 "L's: 60 × C(6, 2) = 900 (verified).", "Shortcut"),
    ],
))

# ---------------- Q23
Q.append(dict(
    qtype="NAT", marks=2, topic="Joint PMF: normalisation & covariance", difficulty="Medium",
    text="The joint PMF of X and Y is p(x, y) = c(x + 2y) for x ∈ {0, 1, 2} and y ∈ {0, 1}, and 0 "
         "otherwise. The covariance Cov(X, Y) is ______ (round off to 3 decimal places).",
    answer=f"{float(A23):.3f}", range=(-0.084, -0.083),
    solution=[
        "<b>Concept:</b> normalise to find c, then Cov(X, Y) = E[XY] − E[X]E[Y].",
        "Step 1 — normalisation: sum of (x + 2y) over the six cells = (0+1+2) + (2+3+4) = 12, so c = 1/12.",
        ("fig", fig_jpmf_q23),
        "Step 2 — marginals: p<sub>X</sub> = (2, 4, 6)/12 for x = 0, 1, 2; p<sub>Y</sub> = (3, 9)/12 for "
        "y = 0, 1.",
        r"$$E[X]=\dfrac{0\cdot 2+1\cdot 4+2\cdot 6}{12}=\dfrac{16}{12}=\dfrac{4}{3},\quad E[Y]=\dfrac{9}{12}=\dfrac{3}{4}",
        "Step 3 — only y = 1 cells contribute to E[XY]:",
        r"$$E[XY]=\dfrac{1\cdot 3+2\cdot 4}{12}=\dfrac{11}{12}",
        r"$$\mathrm{Cov}(X,Y)=\dfrac{11}{12}-\dfrac{4}{3}\cdot\dfrac{3}{4}=\dfrac{11}{12}-1=-\dfrac{1}{12}\approx -0.083",
        ("note", "Small negative covariance: when y = 1 the weights (2, 3, 4) are flatter across x than when "
                 "y = 0 (0, 1, 2), so E[X | Y = 1] = 11/9 &lt; E[X | Y = 0] = 5/3.", "Key idea"),
    ],
))

# ---------------- Q24
Q.append(dict(
    qtype="MCQ", marks=2, topic="Total probability by first-step conditioning", difficulty="Hard",
    text="Players A and B roll a fair die alternately, A first. A wins as soon as A rolls a 6; B wins as "
         "soon as B rolls a 5 or a 6. The game continues until someone wins. The probability that A wins is",
    options=[f"{A24.numerator}/{A24.denominator}", "6/11", "1/3", "5/8"],
    answer="A",
    solution=[
        "<b>Concept:</b> condition on the first round; if nobody wins, the game restarts in the same state "
        "(renewal argument).",
        "Let p = P(A wins). In round 1: A wins at once with probability 1/6. Otherwise (5/6), B fails with "
        "probability 4/6 = 2/3, and then the game restarts.",
        r"$$p=\dfrac{1}{6}+\dfrac{5}{6}\cdot\dfrac{2}{3}\,p",
        r"$$p\left(1-\dfrac{10}{18}\right)=\dfrac{1}{6}\;\Rightarrow\;p=\dfrac{1}{6}\cdot\dfrac{18}{8}=\dfrac{3}{8}",
        "Equivalently, a geometric series: p = (1/6)[1 + (10/18) + (10/18)<super>2</super> + …].",
        "6/11 is the answer when both need a 6; 1/3 and 5/8 = 1 − 3/8 (B's chance) are the other traps.",
        ("note", "Despite moving first, A is the underdog because B's success chance per turn (1/3) is double "
                 "A's (1/6).", "Key idea"),
    ],
))

# ---------------- Q25
Q.append(dict(
    qtype="MSQ", marks=2, topic="Functions of a random variable; uncorrelated vs independent",
    difficulty="Medium",
    text="X is uniformly distributed on {−2, −1, 0, 1, 2} and Y = X<super>2</super>. Which of the "
         "following is/are TRUE?",
    options=["X and Y are independent", "Cov(X, Y) = 0", "E[Y] = 2", "P(Y = 1) = 1/5"],
    answer="B, C",
    solution=[
        "<b>Concept:</b> zero covariance only rules out LINEAR dependence; Y = g(X) is fully dependent on X.",
        ("fig", fig_pmf_q25),
        "<b>(A) FALSE</b>: P(X = 0, Y = 4) = 0 but P(X = 0)P(Y = 4) = (1/5)(2/5) = 2/25 ≠ 0.",
        "<b>(B) TRUE</b>: E[X] = 0 and E[XY] = E[X<super>3</super>] = (−8 − 1 + 0 + 1 + 8)/5 = 0, so",
        r"$$\mathrm{Cov}(X,Y)=E[X^3]-E[X]E[X^2]=0-0=0",
        "<b>(C) TRUE</b>: E[Y] = (4 + 1 + 0 + 1 + 4)/5 = 10/5 = 2.",
        "<b>(D) FALSE</b>: Y = 1 when X = ±1, so P(Y = 1) = 2/5.",
        ("note", "Symmetric X with an even function Y = g(X) always gives Cov = 0 — the classic "
                 "'uncorrelated but dependent' example.", "Trap"),
    ],
))

# ---------------- Q26
Q.append(dict(
    qtype="NAT", marks=2, topic="Expected waiting time by conditioning", difficulty="Hard",
    text="A biased coin shows heads with probability 0.6. It is tossed repeatedly until two CONSECUTIVE "
         "heads appear. The expected number of tosses is ______ (round off to 2 decimal places).",
    answer=f"{A26:.2f}", range=(4.43, 4.46),
    solution=[
        "<b>Concept:</b> law of total expectation applied to states: let E<sub>0</sub> = expected tosses "
        "from scratch, E<sub>1</sub> = expected tosses when the last toss was H.",
        "From state 1: next toss H (0.6) finishes; T (0.4) sends us back to scratch:",
        r"$$E_1=1+0.4\,E_0",
        "From scratch: H (0.6) moves to state 1; T (0.4) leaves us at scratch:",
        r"$$E_0=1+0.6\,E_1+0.4\,E_0",
        "Substitute E<sub>1</sub>:",
        r"$$0.6E_0=1+0.6(1+0.4E_0)=1.6+0.24E_0\;\Rightarrow\;0.36E_0=1.6",
        r"$$E_0=\dfrac{1.6}{0.36}\approx 4.44",
        "General formula: E = (1 + p)/p<super>2</super>; for a fair coin it gives 6.",
        ("note", "1/p<super>2</super> = 2.78 (treating the pair as a single trial of probability p<super>2</super>) "
                 "is wrong because overlapping attempts are not independent trials.", "Trap"),
    ],
))

# ---------------- Q27
Q.append(dict(
    qtype="MCQ", marks=2, topic="Combinations with constraints", difficulty="Hard",
    text="A committee of 5 is to be chosen from 6 men and 5 women. It must contain at least 2 women, and a "
         "particular man M and a particular woman W refuse to serve together. The number of possible "
         "committees is",
    options=[f"{A27_tot}", f"{A27_bad}", "462", f"{A27}"],
    answer="D",
    solution=[
        "<b>Concept:</b> count all committees meeting the 'at least 2 women' rule, then subtract those that "
        "contain both M and W (and still meet the rule).",
        "Step 1 — at least 2 women (k women, 5 − k men):",
        r"$$\binom{5}{2}\binom{6}{3}+\binom{5}{3}\binom{6}{2}+\binom{5}{4}\binom{6}{1}+\binom{5}{5}",
        r"$$=10(20)+10(15)+5(6)+1=200+150+30+1=381",
        "Step 2 — committees with both M and W: choose 3 more from the remaining 5 men and 4 women, with at "
        "least 1 more woman (W already counts as one):",
        r"$$\binom{9}{3}-\binom{5}{3}=84-10=74",
        r"$$\text{Answer}=381-74=307",
        "381 ignores the conflict; 74 is only the subtracted set; 462 = C(11, 5) ignores both constraints.",
        ("note", "When subtracting the 'bad' committees, remember they must ALSO satisfy every other "
                 "constraint (here: ≥ 2 women in total).", "Trap"),
    ],
))

# ---------------- Q28
Q.append(dict(
    qtype="MCQ", marks=2, topic="Conditional probability on a continuous region", difficulty="Hard",
    text="A point (X, Y) is chosen uniformly at random from the unit square [0, 1] × [0, 1]. The value of "
         "P(XY &lt; 1/4 | X &gt; 1/2) is",
    options=["(ln 2)/4", "(ln 2)/2", "1/4", "1 − (ln 2)/2"],
    answer="B",
    solution=[
        "<b>Concept:</b> for a uniform point, conditional probability = (area of A ∩ B)/(area of B).",
        ("fig", fig_region_q28),
        "Conditioning event B = {X &gt; 1/2} has area 1/2. On B, the curve y = 1/(4x) lies in (1/4, 1/2], "
        "so it stays inside the square.",
        r"$$\text{Area}(A\cap B)=\int_{1/2}^{1}\dfrac{1}{4x}\,dx=\dfrac{1}{4}\ln 2",
        r"$$P(XY<1/4\mid X>1/2)=\dfrac{(\ln 2)/4}{1/2}=\dfrac{\ln 2}{2}\approx 0.3466",
        "(ln 2)/4 is the unconditional area — forgetting to divide by P(B). 1 − (ln 2)/2 is the complement.",
        "Equivalent view: given X = x ∈ (1/2, 1), X is U(1/2, 1) with density 2 and "
        "P(Y &lt; 1/(4x)) = 1/(4x), so the answer is ∫ 2·1/(4x) dx = (ln 2)/2.",
        ("note", "Always check whether the boundary curve leaves the square on the conditioning region; "
                 "if it did, the integrand would need to be capped at 1.", "Trap"),
    ],
))

# ---------------- Q29
Q.append(dict(
    qtype="MCQ", marks=2, topic="Multi-stage Bayes (cascaded channels)", difficulty="Hard",
    text="A source sends bit 1 with probability 0.7 and bit 0 with probability 0.3. The bit passes through "
         "two independent noisy relays in series; each relay flips the bit it receives with probability 0.1. "
         "Given that the final received bit is 1, the probability that a 1 was sent is closest to",
    options=["0.955", "0.820", f"{A29:.3f}", "0.574"],
    answer="C",
    solution=[
        "<b>Concept:</b> compose the stages first (total probability over the intermediate bit), then apply "
        "Bayes' theorem.",
        "Step 1 — end-to-end flip probability: the bit is wrong at the end iff exactly one relay flips:",
        r"$$q=2(0.1)(0.9)=0.18,\qquad 1-q=0.82",
        "(Two flips restore the original bit.)",
        ("fig", fig_tree_q29),
        "Step 2 — total probability of receiving 1:",
        r"$$P(R=1)=0.7(0.82)+0.3(0.18)=0.574+0.054=0.628",
        "Step 3 — Bayes:",
        r"$$P(S=1\mid R=1)=\dfrac{0.574}{0.628}\approx 0.914",
        "0.955 is the answer for a SINGLE relay (0.63/0.66); 0.82 is P(R = 1 | S = 1), the reverse "
        "conditional; 0.574 is the joint probability.",
        ("note", "Each extra noisy stage reduces how much the output tells us about the input: posterior "
                 "drops from 0.955 (one relay) to 0.914 (two relays).", "Key idea"),
    ],
))

# ---------------- Q30
Q.append(dict(
    qtype="MSQ", marks=2, topic="Conditional distribution of Poisson given the sum", difficulty="Hard",
    text="X and Y are independent Poisson random variables, each with mean λ &gt; 0. Fix a positive integer n. "
         "Which of the following is/are TRUE?",
    options=["X + Y is Poisson with mean λ",
             "Conditional on X + Y = n, X is Binomial(n, 1/2)",
             "E[X | X + Y = n] = n/2",
             "P(X = 0 | X + Y = n) = 2<super>−n</super>"],
    answer="B, C, D",
    solution=[
        "<b>Concept:</b> sums of independent Poissons are Poisson (means add); conditioning on the total "
        "splits it binomially in proportion to the means.",
        "<b>(A) FALSE</b>: X + Y ∼ Poisson(2λ).",
        "<b>(B) TRUE</b>: for 0 ≤ k ≤ n,",
        r"$$P(X=k\mid X+Y=n)=\dfrac{e^{-\lambda}\dfrac{\lambda^k}{k!}\,e^{-\lambda}\dfrac{\lambda^{n-k}}{(n-k)!}}{e^{-2\lambda}\dfrac{(2\lambda)^n}{n!}}",
        r"$$=\binom{n}{k}\left(\dfrac{1}{2}\right)^{n}",
        "which is the Binomial(n, 1/2) PMF — notice λ cancels.",
        "<b>(C) TRUE</b>: mean of Binomial(n, 1/2) is n/2 (also follows from symmetry: "
        "E[X | S] = E[Y | S] and they add to S).",
        "<b>(D) TRUE</b>: Binomial(n, 1/2) at k = 0 gives (1/2)<super>n</super> = 2<super>−n</super>.",
        "For the record, Var(X | X + Y = n) = n/4.",
        ("note", "With means λ<sub>1</sub>, λ<sub>2</sub>, X | X + Y = n ∼ Binomial(n, λ<sub>1</sub>/(λ<sub>1</sub>"
                 " + λ<sub>2</sub>)).", "Key idea"),
    ],
))


SET = {
    "title": "Topic Test: Probability, Counting, Bayes & Conditional Expectation",
    "subtitle": "A topic-intensive set on counting, axioms, independence, Bayes' theorem, joint PMFs "
                "and conditional expectation/variance.",
    "focus": "Counting (permutations, combinations, multinomial, stars and bars, derangements and "
             "inclusion–exclusion), probability axioms and set algebra, mutual exclusivity vs independence "
             "(pairwise vs mutual), joint/marginal/conditional probability, total probability and multi-stage "
             "Bayes, random variables and indicator methods, conditional expectation E[X | Y], the laws of "
             "total expectation and total variance, and joint PMF tables.",
    "minutes": 90,
    "questions": Q,
}
