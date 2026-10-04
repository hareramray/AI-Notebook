"""Mock Test 10 — Advanced Full-Syllabus Test II (Grand Mock).

All numeric answers are computed below so the key cannot drift from the maths.
"""
import math
from fractions import Fraction as Fr
from math import comb

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"

# ------------------------------------------------------------------ computed keys
_q1 = comb(15, 3) - 4 * comb(9, 3) + 6 * comb(3, 3)                       # 125
_q3 = 6 * (1 - (5 / 6) ** 6)                                               # 3.9906
_q5 = 1 - 3 * math.exp(-2)
_q6 = math.sqrt(2 / math.pi)
_q10 = 500 + 1000 * math.log(2)
_z11 = 5 / math.sqrt(100 / 12)
_q11 = stats.norm.sf(_z11)
# Q13 reliability + Bayes
_R1 = 0.9 * (1 - 0.2 * 0.3)
_R = 1 - (1 - _R1) * (1 - 0.6)
_q13 = 0.4 * _R1 / _R
# Q14 random sum with geometric N
_EN, _VN = 1 / 0.25, 0.75 / 0.25 ** 2
_q14 = _EN * 1 + _VN * 2 ** 2
# Q15 joint pmf
_J = np.array([[0.10, 0.20, 0.10], [0.20, 0.10, 0.30]])   # rows y = 0, 1; cols x = 0, 1, 2
_px, _py = _J.sum(0), _J.sum(1)
_EX = (np.arange(3) * _px).sum()
_EY = _py[1]
_EXY = sum(x * y * _J[y, x] for x in range(3) for y in range(2))
_cov15 = _EXY - _EX * _EY
# Q16
_q16 = 5 / 24
# Q18 contingency
_T18 = np.array([[60, 25, 15], [40, 35, 25]])
_E18 = _T18.sum(1)[:, None] * _T18.sum(0)[None, :] / _T18.sum()
_C18 = (_T18 - _E18) ** 2 / _E18
_q18 = _C18.sum()
# Q19 hypergeometric
_q19 = 5 * 0.4 * 0.6 * 15 / 19
# Q21 two-proportion z
_pp = (120 + 155) / 2000
_se21 = math.sqrt(_pp * (1 - _pp) * (1 / 1000 + 1 / 1000))
_z21 = (0.155 - 0.120) / _se21
_z21_wrong = 0.035 / math.sqrt(_pp * (1 - _pp) / 1000)
# Q22
_z22 = 2 / math.sqrt(13)
_q22 = stats.norm.sf(_z22)
# Q24
_t24 = (52 - 50) / (5 / 5)
_p24 = 2 * stats.t.sf(_t24, 24)
# Q25 Poisson-Bayes
_h25 = 0.3 * math.exp(-4) * 4 ** 3 / 6
_l25 = 0.7 * math.exp(-1) * 1 ** 3 / 6
_q25 = _h25 / (_h25 + _l25)
# Q26
_q26 = (1 + math.log(2)) / 2
# Q27 combined SD
_m27 = (20 * 50 + 30 * 60) / 50
_v27 = (20 * 16 + 30 * 36) / 50 + (20 * (50 - _m27) ** 2 + 30 * (60 - _m27) ** 2) / 50
_q27 = math.sqrt(_v27)
# Q28
_n28a = math.ceil(1.96 ** 2 / 0.1 ** 2)
_n28b = math.ceil(1.96 ** 2 / 0.05 ** 2)
_n28c = math.ceil(2.576 ** 2 / 0.1 ** 2)
# Q29
_q29 = Fr(2, 3) * Fr(27, 64) / (Fr(2, 3) * Fr(27, 64) + Fr(1, 3))
# Q30 Poisson goodness of fit
_lam = 1.5
_p30 = [math.exp(-_lam) * _lam ** k / math.factorial(k) for k in range(3)]
_p30.append(1 - sum(_p30))
_E30 = 100 * np.array(_p30)
_O30 = np.array([20, 35, 25, 20])
_C30 = (_O30 - _E30) ** 2 / _E30
_q30 = _C30.sum()


# ------------------------------------------------------------------ figures
def fig_q4():
    r = np.linspace(0, 1, 300)
    f = 12 * r ** 2 * (1 - r)
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.plot(r, f, color=BLUE, lw=2, label="pdf of range R: 12r²(1−r)")
    ax.fill_between(r, f, color=BLUE, alpha=0.15)
    ax.axvline(0.6, color=MAROON, ls="--", label="E[R] = 3/5")
    ax.set_xlabel("r")
    ax.set_ylabel("density")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    return fig


def fig_q11():
    x = np.linspace(40, 60, 400)
    sd = math.sqrt(100 / 12)
    f = stats.norm.pdf(x, 50, sd)
    fig, ax = plt.subplots(figsize=(5.2, 2.4))
    ax.plot(x, f, color=BLUE)
    m = x >= 55
    ax.fill_between(x[m], f[m], color=MAROON, alpha=0.4)
    ax.annotate(f"≈ {_q11:.4f}", xy=(55.8, 0.01), xytext=(56.5, 0.07), arrowprops=dict(arrowstyle="->"))
    ax.set_yticks([])
    ax.set_xticks([50, 55])
    ax.set_xlabel("S ≈ N(50, 100/12)")
    return fig


def fig_q13():
    fig, ax = plt.subplots(figsize=(5.8, 2.6))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)

    def box(x, y, t):
        ax.add_patch(FancyBboxPatch((x - 0.6, y - 0.4), 1.2, 0.8, boxstyle="round,pad=0.05",
                                    fc="#eaf2f8", ec=BLUE))
        ax.text(x, y, t, ha="center", va="center", fontsize=8.5)

    box(3.2, 4.2, "A\n0.9")
    box(6.4, 5.1, "B\n0.8")
    box(6.4, 3.3, "C\n0.7")
    box(5.6, 1.0, "D\n0.6")
    lines = [((0.5, 2.6), (1.5, 2.6)), ((1.5, 1.0), (1.5, 4.2)), ((1.5, 4.2), (2.6, 4.2)),
             ((3.8, 4.2), (4.8, 4.2)), ((4.8, 3.3), (4.8, 5.1)), ((4.8, 5.1), (5.8, 5.1)),
             ((4.8, 3.3), (5.8, 3.3)), ((7.0, 5.1), (8.0, 5.1)), ((7.0, 3.3), (8.0, 3.3)),
             ((8.0, 3.3), (8.0, 5.1)), ((8.0, 4.2), (9.6, 4.2)), ((1.5, 1.0), (5.0, 1.0)),
             ((6.2, 1.0), (9.6, 1.0)), ((9.6, 1.0), (9.6, 4.2)), ((9.6, 2.6), (10.6, 2.6))]
    for (a, b), (c, d) in lines:
        ax.plot([a, c], [b, d], color="black", lw=1)
    ax.text(0.3, 2.6, "in", ha="right", va="center", fontsize=8)
    ax.text(10.8, 2.6, "out", va="center", fontsize=8)
    return fig


def fig_q15():
    fig, ax = plt.subplots(figsize=(4.6, 2.4))
    ax.imshow(_J, cmap="Blues", vmin=0, vmax=0.4, origin="lower")
    for y in range(2):
        for x in range(3):
            ax.text(x, y, f"{_J[y, x]:.2f}", ha="center", va="center", fontsize=10,
                    color="white" if _J[y, x] > 0.25 else "black")
    ax.set_xticks(range(3), ["x=0", "x=1", "x=2"])
    ax.set_yticks(range(2), ["y=0", "y=1"])
    ax.spines[:].set_visible(False)
    ax.set_title("joint PMF p(x, y)", fontsize=9)
    return fig


def fig_q16():
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    g = np.linspace(0, 1, 200)
    X, Y = np.meshgrid(g, g)
    ax.contourf(X, Y, X + Y, levels=12, cmap="Blues", alpha=0.55)
    ax.fill([0, 0.5, 0], [0, 1, 1], color=MAROON, alpha=0.35)
    ax.plot([0, 0.5], [0, 1], color=MAROON)
    ax.text(0.06, 0.78, "y > 2x", color=MAROON, fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("density x + y (darker = larger)", fontsize=8)
    return fig


def fig_q21():
    x = np.linspace(-4, 4, 400)
    f = stats.norm.pdf(x)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, f, color=BLUE)
    for m, c, a in [(np.abs(x) >= 1.96, GOLD, 0.6), (np.abs(x) >= 2.576, MAROON, 0.55)]:
        ax.fill_between(x[m & (x > 0)], f[m & (x > 0)], color=c, alpha=a)
        ax.fill_between(x[m & (x < 0)], f[m & (x < 0)], color=c, alpha=a)
    ax.axvline(_z21, color="black", lw=1.6)
    ax.text(_z21 + 0.08, 0.3, f"z = {_z21:.2f}", fontsize=8)
    ax.set_xticks([-2.576, -1.96, 0, 1.96, 2.576])
    ax.tick_params(labelsize=7)
    ax.set_yticks([])
    ax.set_xlabel("gold: reject at 5% (two-sided); maroon: reject at 1%")
    return fig


def fig_q24():
    x = np.linspace(-4, 4, 400)
    f = stats.t.pdf(x, 24)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, f, color=BLUE)
    m = np.abs(x) >= 2.064
    ax.fill_between(x[m & (x > 0)], f[m & (x > 0)], color=MAROON, alpha=0.4)
    ax.fill_between(x[m & (x < 0)], f[m & (x < 0)], color=MAROON, alpha=0.4)
    ax.axvline(1.711, color=GOLD, lw=2, ls="--")
    ax.axvline(2.0, color="black", lw=1.4)
    ax.text(2.08, 0.3, "t = 2.00", fontsize=8)
    ax.set_xticks([-2.064, 0, 1.711, 2.064])
    ax.tick_params(labelsize=7)
    ax.set_yticks([])
    ax.set_xlabel("t (24 df): maroon = two-sided 5% region; gold line = one-sided 5% cut-off")
    return fig


def fig_q26():
    x = np.linspace(0.5, 1, 200)
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    ax.fill_between(np.r_[0, 0.5, x], np.r_[1, 1, 0.5 / x], color=BLUE, alpha=0.3, label="xy ≤ 1/2")
    ax.plot(x, 0.5 / x, color=MAROON, lw=2, label="y = 1/(2x)")
    ax.axvline(0.5, color="gray", ls=":")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(fontsize=7, loc="lower left", frameon=True)
    return fig


def fig_q29():
    fig, ax = plt.subplots(figsize=(6, 2.8))
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.text(0.5, 5, "woman", ha="center", va="center", fontsize=9,
            bbox=dict(boxstyle="round", fc="white", ec=BLUE))
    for y, lab, pr, kid, kp in [(8, "carrier", "2/3", "3 unaffected", "(3/4)³ = 27/64"),
                                (2, "non-carrier", "1/3", "3 unaffected", "1")]:
        ax.plot([1.2, 3.6], [5, y], color=BLUE)
        ax.text(2.2, (5 + y) / 2 + 0.5, pr, color=MAROON, fontsize=9)
        ax.text(4.5, y, lab, ha="center", va="center", fontsize=8.5,
                bbox=dict(boxstyle="round", fc="#eaf2f8", ec=BLUE))
        ax.plot([5.4, 7.2], [y, y], color=MAROON)
        ax.text(6.3, y + 0.5, kp, color=MAROON, fontsize=8, ha="center")
        ax.text(7.4, y, kid, va="center", fontsize=8.5)
    return fig


def fig_q30():
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    lab = ["0", "1", "2", "≥3"]
    i = np.arange(4)
    ax.bar(i - 0.18, _O30, 0.36, color=BLUE, label="observed")
    ax.bar(i + 0.18, _E30, 0.36, color=GOLD, label="expected, Poisson(1.5)")
    ax.set_xticks(i, lab)
    ax.set_xlabel("goals per match")
    ax.set_ylabel("matches")
    ax.legend(fontsize=8, frameon=False)
    return fig


# ------------------------------------------------------------------ the set
SET = {
    "title": "Advanced Full-Syllabus Test II (Grand Mock)",
    "subtitle": "The final dress rehearsal — hardest GATE DA level, every syllabus topic, multi-step reasoning throughout.",
    "focus": "The Grand Mock: a final-stage readiness check that sweeps the ENTIRE syllabus at peak GATE DA "
             "difficulty. Counting with upper bounds (inclusion–exclusion), probability bounds, indicator "
             "expectations, range of uniform order statistics, half-normal conditional mean, memoryless "
             "lifetimes, CLT for sums, reliability block diagrams with a Bayes twist, random sums with a "
             "geometric count, joint PMF tables, non-uniform joint pdfs over sub-regions, queue waiting times "
             "via minima of exponentials, hypergeometric variance through indicator covariances, Poisson "
             "thinning, a two-proportion z-test for A/B testing, t-test/CI duality, Poisson-mixture Bayes, "
             "pooled standard deviations, CLT sample-size design, carrier-risk genetics, and χ<super>2</super> tests of "
             "independence and goodness of fit with model-derived expected counts. Score above 60% here and "
             "you are exam-ready; anything less tells you exactly which chapters to revisit.",
    "minutes": 90,
    "questions": [
        # ============================================================ 1-mark
        dict(
            qtype="MCQ", marks=1, topic="Counting with upper bounds (inclusion–exclusion)", difficulty="Hard",
            text="The number of non-negative integer solutions of x<sub>1</sub> + x<sub>2</sub> + x<sub>3</sub> + "
                 "x<sub>4</sub> = 12 with every x<sub>i</sub> ≤ 5 is",
            options=["455", "131", "125", "119"],
            answer="C",
            solution=[
                "<b>Concept:</b> stars and bars gives C(n + k − 1, k − 1); subtract solutions violating the caps "
                "by inclusion–exclusion.",
                r"$$\text{Unrestricted}=\binom{12+3}{3}=\binom{15}{3}=455",
                "If x<sub>1</sub> ≥ 6, put x<sub>1</sub> = 6 + y<sub>1</sub>: y<sub>1</sub> + x<sub>2</sub> + x<sub>3</sub> + "
                "x<sub>4</sub> = 6 ⇒ C(9, 3) = 84 solutions; 4 choices of the variable.",
                "Two variables ≥ 6 uses up all 12: remaining sum 0 ⇒ C(3, 3) = 1 solution; C(4, 2) = 6 pairs. "
                "Three variables ≥ 6 is impossible (18 &gt; 12).",
                r"$$N=455-4(84)+6(1)=455-336+6=125",
                "(D) 119 = 455 − 336 forgets to add back the double violations; (B) adds them back twice.",
                ("note", "With caps, always ask 'can two (or three) caps be broken simultaneously?' — here "
                         "exactly two can, contributing +6.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Probability axioms and bounds", difficulty="Medium",
            text="Events A and B have P(A) = 0.7 and P(B) = 0.6. Which of the following is/are necessarily TRUE "
                 "or possible as stated?",
            options=["P(A ∩ B) ≥ 0.3 necessarily",
                     "P(A ∩ B) ≤ 0.6 necessarily",
                     "A and B can be mutually exclusive",
                     "P(A ∪ B) = 0.9 is possible"],
            answer="A, B, D",
            solution=[
                "<b>Concept:</b> Bonferroni lower bound P(A ∩ B) ≥ P(A) + P(B) − 1 and P(A ∩ B) ≤ min(P(A), P(B)).",
                "<b>(A) TRUE</b>: P(A ∩ B) = P(A) + P(B) − P(A ∪ B) ≥ 0.7 + 0.6 − 1 = 0.3.",
                "<b>(B) TRUE</b>: A ∩ B ⊂ B, so P(A ∩ B) ≤ 0.6.",
                "<b>(C) FALSE</b>: mutual exclusivity needs P(A ∩ B) = 0, which violates (A); equivalently "
                "P(A ∪ B) would be 1.3 &gt; 1.",
                "<b>(D) TRUE</b>: P(A ∪ B) = 0.9 corresponds to P(A ∩ B) = 0.4 ∈ [0.3, 0.6] — admissible "
                "(e.g. a uniform sample space with suitable intervals).",
                ("note", "Feasible range: 0.3 ≤ P(A ∩ B) ≤ 0.6 ⇔ 0.7 ≤ P(A ∪ B) ≤ 1.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Expectation via indicators", difficulty="Medium",
            text="A fair die is rolled 6 times. The expected number of distinct faces that appear is ______ "
                 "(round off to 2 decimal places).",
            answer=f"{_q3:.2f}", range=(3.98, 4.00),
            solution=[
                "<b>Concept:</b> linearity of expectation over indicators — no independence needed.",
                "Let I<sub>j</sub> = 1 if face j appears at least once (j = 1, …, 6).",
                r"$$E[I_j]=1-\left(\dfrac{5}{6}\right)^6=1-0.33490=0.66510",
                r"$$E[\text{distinct}]=6\times 0.66510\approx " + f"{_q3:.4f}",
                ("note", "The indicators are dependent, but expectation is linear regardless — dependence "
                         "would matter only for the variance.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Order statistics (range of uniforms)", difficulty="Medium",
            text="X<sub>1</sub>, …, X<sub>4</sub> are i.i.d. Uniform(0, 1). The expected value of the sample range "
                 "R = max X<sub>i</sub> − min X<sub>i</sub> is",
            options=["1/2", "3/5", "4/5", "2/5"],
            answer="B",
            solution=[
                "<b>Concept:</b> for n i.i.d. U(0, 1), E[max] = n/(n + 1) and E[min] = 1/(n + 1).",
                r"$$E[\max]=\dfrac{4}{5},\qquad E[\min]=\dfrac{1}{5}",
                r"$$E[R]=\dfrac{4}{5}-\dfrac{1}{5}=\dfrac{3}{5}",
                "Check via the pdf of the range, f<sub>R</sub>(r) = n(n − 1)r<super>n−2</super>(1 − r) = 12r<super>2</super>(1 − r):",
                r"$$E[R]=\int_0^1 12r^3(1-r)\,dr=12\left(\dfrac{1}{4}-\dfrac{1}{5}\right)=\dfrac{3}{5}",
                ("fig", fig_q4),
                "(C) is E[max] alone; (A) is the mean of a single uniform.",
                ("note", "General result: E[R] = (n − 1)/(n + 1).", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Poisson distribution", difficulty="Medium",
            text="The number of defects in a 1 m length of optical fibre is Poisson. If P(X = 1) = P(X = 2), then "
                 "P(X ≥ 2) is",
            options=[f"{1 - math.exp(-2):.3f}", f"{_q5:.3f}", f"{1 - 5 * math.exp(-2):.3f}", f"{3 * math.exp(-2):.3f}"],
            answer="B",
            solution=[
                "<b>Concept:</b> equate the PMF values to find λ, then use the complement.",
                r"$$e^{-\lambda}\lambda=e^{-\lambda}\dfrac{\lambda^2}{2}\ \Rightarrow\ \lambda=2",
                r"$$P(X\geq 2)=1-P(0)-P(1)=1-e^{-2}(1+2)=1-3e^{-2}\approx " + f"{_q5:.4f}",
                "(A) is P(X ≥ 1); (C) is P(X ≥ 3); (D) is P(X ≤ 1).",
                ("note", "For Poisson, P(k)/P(k − 1) = λ/k — the ratio method finds λ instantly.", "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Conditional expectation (half-normal)", difficulty="Hard",
            text="Z ∼ N(0, 1). The value of E[Z | Z &gt; 0] is ______ (round off to 3 decimal places).",
            answer=f"{_q6:.3f}", range=(0.797, 0.799),
            solution=[
                "<b>Concept:</b> E[Z | A] = E[Z·1<sub>A</sub>]/P(A); for the normal density, φ′(z) = −zφ(z).",
                r"$$E[Z\,1_{\{Z>0\}}]=\int_0^\infty z\,\dfrac{e^{-z^2/2}}{\sqrt{2\pi}}\,dz=\dfrac{1}{\sqrt{2\pi}}\left[-e^{-z^2/2}\right]_0^\infty=\dfrac{1}{\sqrt{2\pi}}",
                r"$$E[Z\mid Z>0]=\dfrac{1/\sqrt{2\pi}}{1/2}=\sqrt{\dfrac{2}{\pi}}\approx " + f"{_q6:.4f}",
                ("note", "Equivalently E|Z| = √(2/π) ≈ 0.798 — the mean absolute deviation of a normal is "
                         "about 0.8σ.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Covariance and correlation properties", difficulty="Medium",
            text="Which of the following statements is/are TRUE?",
            options=["Cov(X, Y) = 0 implies that X and Y are independent",
                     "Corr(aX + b, cY + d) = Corr(X, Y) whenever a &gt; 0 and c &gt; 0",
                     "|Corr(X, Y)| ≤ 1 for any X, Y with finite positive variances",
                     "If X ∼ U(−1, 1) and Y = X<super>2</super>, then Corr(X, Y) = 0"],
            answer="B, C, D",
            solution=[
                "<b>Concept:</b> correlation measures LINEAR dependence only, is scale/shift invariant (up to sign) "
                "and bounded by Cauchy–Schwarz.",
                "<b>(A) FALSE</b>: zero covariance does not imply independence — (D) is a counter-example.",
                "<b>(B) TRUE</b>: Cov(aX + b, cY + d) = ac Cov(X, Y) and the SDs scale by |a|, |c|; ratio is "
                "unchanged when ac &gt; 0 (sign flips if ac &lt; 0).",
                "<b>(C) TRUE</b>: Cauchy–Schwarz |Cov(X, Y)| ≤ σ<sub>X</sub>σ<sub>Y</sub>.",
                "<b>(D) TRUE</b>: Cov(X, X<super>2</super>) = E[X<super>3</super>] − E[X]E[X<super>2</super>] = 0 − 0 = 0 by "
                "symmetry, though Y is a function of X.",
                ("note", "Y = X<super>2</super> with symmetric X is the standard 'uncorrelated but totally dependent' "
                         "example.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Binomial: parameters and mode", difficulty="Medium",
            text="X ∼ Binomial(n, p) has mean 6 and variance 2.4. The most probable value (mode) of X is",
            options=["6", "7", "5", "both 6 and 7"],
            answer="A",
            solution=[
                "<b>Concept:</b> np = mean, np(1 − p) = variance; the binomial mode is ⌊(n + 1)p⌋ (two modes "
                "only when (n + 1)p is an integer).",
                r"$$1-p=\dfrac{2.4}{6}=0.4\ \Rightarrow\ p=0.6,\quad n=\dfrac{6}{0.6}=10",
                r"$$(n+1)p=6.6\ \Rightarrow\ \text{mode}=\lfloor 6.6\rfloor=6",
                r"$$\dfrac{P(7)}{P(6)}=\dfrac{(10-6)}{7}\cdot\dfrac{0.6}{0.4}=\dfrac{6}{7}<1,\qquad \dfrac{P(6)}{P(5)}=\dfrac{5}{6}\cdot 1.5=1.25>1",
                ("note", "'Both 6 and 7' would need (n + 1)p = 7 exactly.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Chi-squared distribution (scaling)", difficulty="Medium",
            text="Z<sub>1</sub>, …, Z<sub>4</sub> are i.i.d. N(0, 4) (variance 4). Let Y = Z<sub>1</sub><super>2</super> "
                 "+ … + Z<sub>4</sub><super>2</super>. Var(Y) equals",
            options=["8", "32", "64", "128"],
            answer="D",
            solution=[
                "<b>Concept:</b> standardise first: Z<sub>i</sub> = 2W<sub>i</sub> with W<sub>i</sub> ∼ N(0, 1), so "
                "Y = 4∑W<sub>i</sub><super>2</super> = 4V with V ∼ χ<super>2</super><sub>4</sub>.",
                r"$$\text{Var}(V)=2k=8,\qquad \text{Var}(Y)=4^2\,\text{Var}(V)=16\times 8=128",
                "(A) treats Y as χ<super>2</super><sub>4</sub>; (B) and (C) apply the wrong scale factor (4 or 8) "
                "instead of 4<super>2</super> = 16.",
                ("note", "A constant multiplier c on a random variable multiplies its variance by c<super>2</super> — "
                         "here c = σ<super>2</super> = 4.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=1, topic="Exponential: memorylessness and median", difficulty="Medium",
            text="LED lifetimes are exponential with mean 1000 hours. A particular LED has already worked for "
                 "500 hours. The median of its TOTAL lifetime, given this information, is ______ hours "
                 "(round off to the nearest integer).",
            answer=f"{round(_q10)}", range=(1192, 1194),
            solution=[
                "<b>Concept:</b> memorylessness — the remaining life after survival to 500 h is again Exp(mean 1000).",
                "Median m of Exp(mean θ): e<super>−m/θ</super> = 1/2 ⇒ m = θ ln 2.",
                r"$$m_{\text{remaining}}=1000\ln 2\approx 693.1",
                r"$$m_{\text{total}}=500+693.1\approx " + f"{_q10:.1f}",
                ("note", "The median of an exponential (0.693θ) is smaller than its mean θ — right skew.",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=1, topic="Central limit theorem", difficulty="Medium",
            text="S is the sum of 100 i.i.d. Uniform(0, 1) random variables. Using the CLT (Φ(1.73) ≈ 0.9582), "
                 "P(S &gt; 55) is approximately",
            options=["0.042", "0.084", "0.023", "0.309"],
            answer="A",
            solution=[
                "<b>Concept:</b> S ≈ N(nμ, nσ<super>2</super>) with μ = 1/2 and σ<super>2</super> = 1/12 for U(0, 1).",
                r"$$E[S]=50,\qquad \text{Var}(S)=\dfrac{100}{12}=8.333,\qquad \text{SD}=2.887",
                r"$$P(S>55)\approx P\left(Z>\dfrac{5}{2.887}\right)=P(Z>1.732)\approx 0.042",
                ("fig", fig_q11),
                "(B) is the two-sided probability; (C) corresponds to z = 2, i.e. taking SD = 2.5; (D) ≈ P(Z &gt; 0.5).",
                ("note", "Variance of U(a, b) is (b − a)<super>2</super>/12 — the 12 is the most-forgotten constant "
                         "in CLT questions.", "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Confidence-interval properties", difficulty="Medium",
            text="For confidence intervals for a population mean, which of the following is/are TRUE?",
            options=["For fixed n and σ, a 99% interval is wider than a 95% interval",
                     "To halve the width of a z-interval, the sample size must be doubled",
                     "Once computed, a 95% interval (e.g. (48.1, 53.9)) contains μ with probability 0.95",
                     "With the same n and s = σ, the t-interval is wider than the z-interval"],
            answer="A, D",
            solution=[
                "<b>Concept:</b> width = 2 × critical value × σ/√n; the confidence level refers to the procedure, "
                "not a computed interval.",
                "<b>(A) TRUE</b>: 2.576 &gt; 1.96.",
                "<b>(B) FALSE</b>: width ∝ 1/√n, so halving the width needs 4 times the sample size.",
                "<b>(C) FALSE</b>: μ is fixed; a realised interval either contains it or not. '95%' is the long-run "
                "coverage of the method.",
                "<b>(D) TRUE</b>: t<sub>α/2,n−1</sub> &gt; z<sub>α/2</sub> for every finite n.",
                ("note", "Width scales like 1/√n — quadrupling n halves the width.", "Shortcut"),
            ],
        ),
        # ============================================================ 2-mark
        dict(
            qtype="NAT", marks=2, topic="System reliability with Bayes", difficulty="Hard",
            text=["In the network below, signal passes from 'in' to 'out' if there is a path of working "
                  "components. A is in series with the parallel pair (B, C), and this branch is in parallel with "
                  "D. Components fail independently; their reliabilities are shown.",
                  ("fig", fig_q13),
                  "Given that the system is working, the probability that component D has FAILED is ______ "
                  "(round off to 3 decimal places)."],
            answer=f"{_q13:.3f}", range=(0.359, 0.362),
            solution=[
                "<b>Concept:</b> series ⇒ multiply reliabilities; parallel ⇒ 1 − product of failure probabilities; "
                "then Bayes on the event 'system works'.",
                r"$$R_{BC}=1-(0.2)(0.3)=0.94,\qquad R_1=R_A R_{BC}=0.9(0.94)=0.846",
                r"$$R_{\text{sys}}=1-(1-0.846)(1-0.6)=1-0.154(0.4)=0.9384",
                "If D has failed, the system works only through the upper branch:",
                r"$$P(D^c\cap\text{works})=P(D^c)\,R_1=0.4(0.846)=0.3384",
                r"$$P(D^c\mid\text{works})=\dfrac{0.3384}{0.9384}\approx " + f"{_q13:.4f}",
                "Monte-Carlo with 10<super>6</super> runs gives 0.3610.",
                ("note", "Conditioning on success lowers the failure probability of D from 0.4 to 0.361 — but "
                         "not by much, because the upper branch is itself very reliable.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Random sum with geometric count", difficulty="Hard",
            text="A player keeps playing rounds of a game until the first loss; each round is lost with "
                 "probability 0.25, independently, and N is the total number of rounds played (including the "
                 "losing round). In each round the player earns an amount with mean 2 and variance 1, "
                 "independently of everything else. Let S be the total earnings over the N rounds. Var(S) is",
            options=["4", "48", f"{_q14:.0f}", "64"],
            answer="C",
            solution=[
                "<b>Concept:</b> Var(S) = E[N]Var(X) + Var(N)(E[X])<super>2</super> for a random sum with N independent "
                "of the X's.",
                "N is geometric on {1, 2, …} with success (loss) probability p = 0.25:",
                r"$$E[N]=\dfrac{1}{p}=4,\qquad \text{Var}(N)=\dfrac{1-p}{p^2}=\dfrac{0.75}{0.0625}=12",
                r"$$\text{Var}(S)=E[N]\cdot 1+\text{Var}(N)\cdot 2^2=4+48=" + f"{_q14:.0f}",
                "E[S] = 4 × 2 = 8 for reference.",
                "(A) keeps only the first term; (B) only the second; (D) = (E[N])<super>2</super>(E[X])<super>2</super> = "
                "E[S]<super>2</super>.",
                ("note", "The second term usually dominates: uncertainty in HOW MANY rounds matters more than "
                         "uncertainty in each round's payoff.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Joint PMF, covariance, conditional expectation", difficulty="Hard",
            text=["The joint PMF of X (number of retries) and Y (indicator of a timeout) is:",
                  ("table", [["", "X = 0", "X = 1", "X = 2"],
                             ["Y = 0", "0.10", "0.20", "0.10"],
                             ["Y = 1", "0.20", "0.10", "0.30"]]),
                  "Which of the following is/are TRUE?"],
            options=["X and Y are NOT independent",
                     "Cov(X, Y) = 0.04",
                     "E[Y | X = 2] = 0.75",
                     "P(X &gt; Y) = 0.5"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> marginals from row/column sums; independence needs EVERY cell to factor.",
                ("fig", fig_q15),
                "Marginals: P(X = 0, 1, 2) = 0.3, 0.3, 0.4 and P(Y = 0, 1) = 0.4, 0.6.",
                "<b>(A) TRUE</b>: P(X = 0, Y = 0) = 0.10 but P(X = 0)P(Y = 0) = 0.12.",
                "<b>(B) TRUE</b>:",
                r"$$E[X]=0.3+2(0.4)=1.1,\quad E[Y]=0.6,\quad E[XY]=1(0.10)+2(0.30)=0.7",
                r"$$\text{Cov}(X,Y)=0.7-1.1(0.6)=0.7-0.66=0.04",
                "<b>(C) TRUE</b>:",
                r"$$E[Y\mid X=2]=P(Y=1\mid X=2)=\dfrac{0.30}{0.40}=0.75",
                "<b>(D) FALSE</b>: X &gt; Y in cells (1,0), (2,0), (2,1):",
                r"$$P(X>Y)=0.20+0.10+0.30=0.60",
                ("note", "A single non-factoring cell is enough to rule out independence; you never need to "
                         "check all six.", "Shortcut"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Joint pdf over a sub-region", difficulty="Hard",
            text="(X, Y) has joint pdf f(x, y) = x + y for 0 &lt; x &lt; 1, 0 &lt; y &lt; 1, and 0 otherwise. "
                 "P(Y &gt; 2X) is ______ (round off to 3 decimal places).",
            answer=f"{_q16:.3f}", range=(0.207, 0.209),
            solution=[
                "<b>Concept:</b> integrate the joint pdf over the region; draw it first to set the limits.",
                ("fig", fig_q16),
                "Y &gt; 2X inside the unit square requires x &lt; 1/2 and 2x &lt; y &lt; 1.",
                r"$$P=\int_0^{1/2}\int_{2x}^{1}(x+y)\,dy\,dx",
                r"$$\int_{2x}^{1}(x+y)\,dy=x(1-2x)+\dfrac{1-4x^2}{2}=\dfrac{1}{2}+x-4x^2",
                r"$$P=\left[\dfrac{x}{2}+\dfrac{x^2}{2}-\dfrac{4x^3}{3}\right]_0^{1/2}=\dfrac{1}{4}+\dfrac{1}{8}-\dfrac{1}{6}=\dfrac{5}{24}",
                r"$$P=\dfrac{5}{24}\approx " + f"{_q16:.4f}",
                "Check: f is linear, so P = (area) × f(centroid). The triangle has area 1/4 and centroid (1/6, 2/3), "
                "where f = 5/6; hence P = (1/4)(5/6) = 5/24. The region lies where x is small, so the density "
                "there is below its average value 1.",
                ("note", "Using area alone (0.25) is valid only for UNIFORM joint pdfs.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Queues: minima of exponentials", difficulty="Hard",
            text="A help desk has 3 agents; service times are i.i.d. exponential with mean 10 minutes. You arrive "
                 "to find all 3 agents busy and nobody else waiting. Your expected total time in the system "
                 "(waiting + your own service) is",
            options=["10 min", "40/3 min", "50/3 min", "20 min"],
            answer="B",
            solution=[
                "<b>Concept:</b> by memorylessness the three ongoing services restart afresh; the first completion "
                "is the minimum of 3 i.i.d. Exp(rate 1/10), i.e. Exp(rate 3/10).",
                r"$$E[W]=\dfrac{1}{3/10}=\dfrac{10}{3}\ \text{min}",
                "Your own service then takes Exp(mean 10), independent of the wait.",
                r"$$E[\text{total}]=\dfrac{10}{3}+10=\dfrac{40}{3}\approx 13.33\ \text{min}",
                "(C) 50/3 = 10/3 + 10 + 10/3 double-counts the wait; (D) 20 treats the wait as a full service "
                "time, ignoring that 3 agents are competing to free up first; (A) ignores the wait altogether.",
                ("note", "Bonus: when you start service, the other two are still busy and memoryless, so "
                         "P(you are the last of these three to finish) = (2/3)(1/2) = 1/3.", "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Chi-squared test of independence", difficulty="Hard",
            text=["Two classifiers are evaluated on 100 hold-out samples each; errors are graded as follows:",
                  ("table", [["Model", "Correct", "Minor error", "Major error", "Total"],
                             ["A", "60", "25", "15", "100"],
                             ["B", "40", "35", "25", "100"]]),
                  "The Pearson χ<super>2</super> statistic for testing whether outcome grade is independent of model "
                  "is ______ (round off to 2 decimal places)."],
            answer=f"{_q18:.2f}", range=(8.12, 8.21),
            solution=[
                "<b>Concept:</b> expected count E<sub>ij</sub> = (row total)(column total)/n; "
                "χ<super>2</super> = ∑(O − E)<super>2</super>/E with (r − 1)(c − 1) df.",
                "Column totals: 100, 60, 40; row totals 100 each; n = 200 ⇒ expected counts 50, 30, 20 in both rows.",
                ("table", [["Cell", "O", "E", "(O − E)<super>2</super>/E"]] +
                 [[f"{m}, {g}", f"{_T18[i, j]}", f"{_E18[i, j]:.0f}", f"{_C18[i, j]:.4f}"]
                  for i, m in enumerate("AB") for j, g in enumerate(["correct", "minor", "major"])]),
                r"$$\chi^2=2\left(\dfrac{10^2}{50}+\dfrac{5^2}{30}+\dfrac{5^2}{20}\right)=2(2+0.8333+1.25)=" + f"{_q18:.4f}",
                "df = (2 − 1)(3 − 1) = 2. Since 8.17 &gt; χ<super>2</super><sub>0.05,2</sub> = 5.991 (but &lt; "
                "χ<super>2</super><sub>0.01,2</sub> = 9.210), independence is rejected at 5% but not at 1%.",
                ("note", "With equal row totals the two rows have identical expected counts and mirror-image "
                         "deviations — compute one row and double it.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Hypergeometric variance via indicator covariances", difficulty="Hard",
            text="A class has 20 students of whom 8 are women. A committee of 5 is chosen at random without "
                 "replacement. If X is the number of women on the committee, Var(X) is closest to",
            options=["1.200", f"{_q19:.3f}", "0.900", "1.520"],
            answer="B",
            solution=[
                "<b>Concept:</b> X = ∑I<sub>k</sub> over the 5 seats; the I<sub>k</sub> are exchangeable but negatively "
                "correlated because sampling is without replacement.",
                r"$$P(I_k=1)=\dfrac{8}{20}=0.4,\qquad \text{Var}(I_k)=0.4(0.6)=0.24",
                r"$$P(I_jI_k=1)=\dfrac{8}{20}\cdot\dfrac{7}{19}=\dfrac{56}{380},\qquad \text{Cov}(I_j,I_k)=\dfrac{56}{380}-0.16=-\dfrac{0.24}{19}",
                r"$$\text{Var}(X)=5(0.24)+20\left(-\dfrac{0.24}{19}\right)=1.2-0.2526=" + f"{_q19:.4f}",
                "This matches the hypergeometric formula with finite-population correction:",
                r"$$\text{Var}(X)=np(1-p)\dfrac{N-n}{N-1}=5(0.4)(0.6)\dfrac{15}{19}=" + f"{_q19:.4f}",
                "(A) is the binomial (with-replacement) variance; (C) uses (N − n)/N; (D) inverts the correction.",
                ("note", "Without replacement ⇒ negative covariances ⇒ smaller variance than binomial.", "Key idea"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="Poisson thinning and conditioning", difficulty="Hard",
            text="Requests reach a load balancer as a Poisson process with rate 6 per minute. Each request is "
                 "routed to server A with probability 1/3 and to server B with probability 2/3, independently. "
                 "Which of the following is/are TRUE?",
            options=["Arrivals at A form a Poisson process with rate 2 per minute",
                     "The number of requests reaching B in a 30-second interval has variance 4",
                     "Given that exactly 9 requests arrived in a minute, the number sent to A has mean 3 and variance 2",
                     "The mean time between consecutive arrivals at A is 1/6 minute"],
            answer="A, C",
            solution=[
                "<b>Concept:</b> thinning a Poisson(λ) process with probability p gives independent Poisson(λp) "
                "processes; conditioning on the total gives a binomial split.",
                "<b>(A) TRUE</b>: rate 6 × 1/3 = 2 per minute.",
                "<b>(B) FALSE</b>: B has rate 4 per minute; in 0.5 min the count is Poisson with mean 2, so its "
                "variance is 2, not 4.",
                "<b>(C) TRUE</b>: given N = 9, the A-count ∼ Bin(9, 1/3):",
                r"$$E=9\cdot\dfrac{1}{3}=3,\qquad \text{Var}=9\cdot\dfrac{1}{3}\cdot\dfrac{2}{3}=2",
                "<b>(D) FALSE</b>: inter-arrival times at A are Exp(rate 2), mean 1/2 minute (1/6 is for the "
                "combined stream).",
                ("note", "Poisson ⇒ variance = mean; once you condition on the total, the variance shrinks to "
                         "binomial np(1 − p).", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Two-proportion z-test (A/B testing)", difficulty="Hard",
            text="In an A/B test, the old page converts 120 of 1000 visitors and the new page 155 of 1000 visitors. "
                 "Using the pooled two-proportion z-test of H<sub>0</sub>: p<sub>A</sub> = p<sub>B</sub> vs "
                 "H<sub>1</sub>: p<sub>A</sub> ≠ p<sub>B</sub> (z<sub>0.025</sub> = 1.96, z<sub>0.005</sub> = 2.576), "
                 "which is correct?",
            options=[f"z ≈ {_z21:.2f}; reject H<sub>0</sub> at 5% but not at 1%",
                     f"z ≈ {_z21:.2f}; reject H<sub>0</sub> at both 5% and 1%",
                     f"z ≈ {_z21_wrong:.2f}; reject H<sub>0</sub> at both 5% and 1%",
                     f"z ≈ {_z21 / math.sqrt(2):.2f}; do not reject H<sub>0</sub> at 5%"],
            answer="A",
            solution=[
                "<b>Concept:</b> under H<sub>0</sub> the common p is estimated by pooling; "
                "z = (p̂<sub>B</sub> − p̂<sub>A</sub>)/√(p̂(1 − p̂)(1/n<sub>A</sub> + 1/n<sub>B</sub>)).",
                r"$$\hat{p}=\dfrac{120+155}{2000}=0.1375",
                r"$$SE=\sqrt{0.1375(0.8625)\left(\dfrac{1}{1000}+\dfrac{1}{1000}\right)}=" + f"{_se21:.5f}",
                r"$$z=\dfrac{0.155-0.120}{" + f"{_se21:.5f}" + r"}\approx " + f"{_z21:.3f}",
                "1.96 &lt; 2.27 &lt; 2.576 ⇒ reject at 5%, not at 1% (two-sided p-value ≈ 0.023).",
                ("fig", fig_q21),
                f"(C) forgets the factor (1/n<sub>A</sub> + 1/n<sub>B</sub>), using only 1/1000; (D) divides by an extra √2.",
                ("note", "The SE of a DIFFERENCE adds the two variances — it is √2 times the one-sample SE "
                         "when n<sub>A</sub> = n<sub>B</sub>.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Linear combinations of normals", difficulty="Hard",
            text="The inference latencies (ms) of two independent models are X ∼ N(10, 4) and Y ∼ N(12, 9) "
                 "(second parameter = variance). The probability that model X is SLOWER than model Y on a "
                 "request, P(X &gt; Y), is ______ (round off to 3 decimal places).",
            answer=f"{_q22:.3f}", range=(0.287, 0.292),
            solution=[
                "<b>Concept:</b> a difference of independent normals is normal with variances ADDED.",
                r"$$D=X-Y\sim N(10-12,\ 4+9)=N(-2,\ 13)",
                r"$$P(X>Y)=P(D>0)=P\left(Z>\dfrac{0-(-2)}{\sqrt{13}}\right)=P(Z>0.5547)",
                r"$$=1-\Phi(0.5547)\approx " + f"{_q22:.4f}",
                "(Table at z = 0.55 gives 0.2912, inside the accepted range.)",
                ("note", "Var(X − Y) = Var X + Var Y, never Var X − Var Y (which would be negative here!).",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Conditional pdf; covariance from conditional expectation",
            difficulty="Hard",
            text="(X, Y) has joint pdf f(x, y) = e<super>−y</super> for 0 &lt; x &lt; y &lt; ∞. The correlation "
                 "coefficient between X and Y is",
            options=["1/2", "1/√3", "1/√2", "√(2/3)"],
            answer="C",
            solution=[
                "<b>Concept:</b> find marginals, use X | Y = y to get E[XY] by iterated expectation.",
                r"$$f_X(x)=\int_x^\infty e^{-y}\,dy=e^{-x}\ \Rightarrow\ X\sim\text{Exp}(1):\ E[X]=1,\ \text{Var}(X)=1",
                r"$$f_Y(y)=\int_0^y e^{-y}\,dx=ye^{-y}:\ E[Y]=2,\ E[Y^2]=6,\ \text{Var}(Y)=2",
                "Given Y = y, f(x | y) = e<super>−y</super>/(ye<super>−y</super>) = 1/y on (0, y): X | Y = y ∼ U(0, y).",
                r"$$E[XY]=E\left[Y\,E[X\mid Y]\right]=E\left[\dfrac{Y^2}{2}\right]=3",
                r"$$\text{Cov}=3-1(2)=1,\qquad \rho=\dfrac{1}{\sqrt{1}\sqrt{2}}=\dfrac{1}{\sqrt{2}}\approx 0.707",
                "Interpretation: Y = X + W where W ∼ Exp(1) is independent of X (memorylessness), so "
                "ρ = √(Var X / Var Y) = 1/√2.",
                ("note", "Spotting Y = X + independent noise gives ρ without any integration.", "Shortcut"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="One-sample t-test and CI duality", difficulty="Hard",
            text="A sample of n = 25 battery lives gives x̄ = 52 h and s = 5 h (normal population). Consider "
                 "H<sub>0</sub>: μ = 50. Given t<sub>0.025,24</sub> = 2.064 and t<sub>0.05,24</sub> = 1.711, "
                 "which of the following is/are TRUE?",
            options=["The two-sided test rejects H<sub>0</sub> at α = 0.05",
                     "The one-sided test against H<sub>1</sub>: μ &gt; 50 rejects H<sub>0</sub> at α = 0.05",
                     "The 95% two-sided t-interval for μ contains 50",
                     "The two-sided p-value lies between 0.05 and 0.10"],
            answer="B, C, D",
            solution=[
                "<b>Concept:</b> t = (x̄ − μ<sub>0</sub>)/(s/√n) with n − 1 df; a two-sided level-α test rejects "
                "iff μ<sub>0</sub> lies outside the (1 − α) interval.",
                r"$$t=\dfrac{52-50}{5/\sqrt{25}}=\dfrac{2}{1}=2.00",
                ("fig", fig_q24),
                "<b>(A) FALSE</b>: |t| = 2.00 &lt; 2.064.",
                "<b>(B) TRUE</b>: t = 2.00 &gt; 1.711.",
                "<b>(C) TRUE</b>: 52 ± 2.064(1) = (49.936, 54.064) ∋ 50 — consistent with (A) failing.",
                "<b>(D) TRUE</b>: one-sided p ∈ (0.025, 0.05) because 1.711 &lt; 2 &lt; 2.064, so the two-sided "
                f"p ∈ (0.05, 0.10). (Exact: {_p24:.4f}.)",
                ("note", "The same data can be significant one-sided and not two-sided — the direction must "
                         "be fixed BEFORE seeing the data.", "Trap"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Bayes theorem with Poisson likelihoods", difficulty="Hard",
            text="An e-commerce site has two customer segments: 30% are 'heavy' buyers whose monthly number of "
                 "purchases is Poisson with mean 4, and 70% are 'light' buyers with Poisson mean 1. A randomly "
                 "chosen customer made exactly 3 purchases last month. The probability that the customer is a "
                 "heavy buyer is ______ (round off to 3 decimal places).",
            answer=f"{_q25:.3f}", range=(0.576, 0.579),
            solution=[
                "<b>Concept:</b> posterior ∝ prior × likelihood, with Poisson likelihoods e<super>−λ</super>λ<super>k</super>/k!.",
                r"$$P(3\mid H)=e^{-4}\dfrac{4^3}{3!}=" + f"{math.exp(-4) * 64 / 6:.5f}" + r",\qquad P(3\mid L)=e^{-1}\dfrac{1}{3!}=" + f"{math.exp(-1) / 6:.5f}",
                r"$$P(H\mid 3)=\dfrac{0.3(" + f"{math.exp(-4) * 64 / 6:.5f}" + r")}{0.3(" + f"{math.exp(-4) * 64 / 6:.5f}" + r")+0.7(" + f"{math.exp(-1) / 6:.5f}" + r")}",
                r"$$=\dfrac{" + f"{_h25:.5f}" + r"}{" + f"{_h25:.5f}+{_l25:.5f}" + r"}\approx " + f"{_q25:.4f}",
                "Ratio form (3! cancels): posterior odds = (0.3/0.7) × 64e<super>−3</super> = 0.4286 × 3.1864 = 1.3656 "
                "⇒ P = 1.3656/2.3656 ≈ 0.577.",
                ("note", "Cancel common factors (k!) before computing — fewer chances for arithmetic slips.",
                 "Shortcut"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Geometric probability (product of uniforms)", difficulty="Hard",
            text="X and Y are independent Uniform(0, 1). P(XY ≤ 1/2) equals",
            options=["ln 2", "(1 + ln 2)/2", "3/4", "1/2"],
            answer="B",
            solution=[
                "<b>Concept:</b> P = area of {(x, y) ∈ unit square: y ≤ 1/(2x)}; split where the curve meets y = 1.",
                ("fig", fig_q26),
                "For x ≤ 1/2, 1/(2x) ≥ 1 so the whole vertical strip counts (area 1/2). For x &gt; 1/2 the "
                "allowed height is 1/(2x):",
                r"$$P=\dfrac{1}{2}+\int_{1/2}^{1}\dfrac{1}{2x}\,dx=\dfrac{1}{2}+\dfrac{1}{2}\ln 2=\dfrac{1+\ln 2}{2}",
                r"$$\approx " + f"{_q26:.4f}",
                "Monte-Carlo (10<super>6</super> points) gives 0.8465.",
                "(A) ln 2 ≈ 0.693 = ∫<sub>1/2</sub><super>1</super>dx/x drops both the factor 1/2 and the full strip x ≤ 1/2; (D) wrongly assumes XY is symmetric about 1/2.",
                ("note", "Always find where the boundary curve leaves the unit square — that is where the "
                         "integral must be split.", "Trap"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Combined mean and standard deviation", difficulty="Hard",
            text="Section 1 has 20 students with mean score 50 and SD 4; section 2 has 30 students with mean 60 "
                 "and SD 6 (SDs computed with divisor n). The SD (divisor n) of all 50 scores combined is "
                 "closest to",
            options=["5.20", "5.29", f"{_q27:.2f}", "10.00"],
            answer="C",
            solution=[
                "<b>Concept:</b> total variance = average within-group variance + variance of group means "
                "(law of total variance for data).",
                r"$$\bar{x}=\dfrac{20(50)+30(60)}{50}=56",
                r"$$\text{within}=\dfrac{20(16)+30(36)}{50}=\dfrac{320+1080}{50}=28",
                r"$$\text{between}=\dfrac{20(50-56)^2+30(60-56)^2}{50}=\dfrac{720+480}{50}=24",
                r"$$\sigma=\sqrt{28+24}=\sqrt{52}\approx " + f"{_q27:.3f}",
                "(A) is the weighted average of SDs; (B) √28 ignores the between-group spread.",
                ("note", "Never average standard deviations — combine VARIANCES and add the between-means term.",
                 "Trap"),
            ],
        ),
        dict(
            qtype="MSQ", marks=2, topic="CLT sample-size design", difficulty="Hard",
            text="Job durations on a cluster are i.i.d. exponential with unknown mean θ. An engineer wants the "
                 "sample mean X̄ of n jobs to satisfy P(|X̄ − θ| ≤ 0.1θ) ≥ 0.95, using the CLT "
                 "(z<sub>0.025</sub> = 1.96, z<sub>0.005</sub> = 2.576). Which of the following is/are TRUE?",
            options=[f"The smallest such n is {_n28a}",
                     f"If the tolerance is tightened to 0.05θ (still 95%), the smallest n is {_n28b}",
                     f"For tolerance 0.1θ at 99% confidence, the smallest n is {_n28c}",
                     "The required n cannot be found without a pilot estimate of θ"],
            answer="A, B, C",
            solution=[
                "<b>Concept:</b> for Exp(mean θ), SD = θ, so SD(X̄) = θ/√n; by the CLT the condition becomes "
                "z<sub>α/2</sub>θ/√n ≤ cθ.",
                r"$$P\left(|Z|\leq\dfrac{0.1\theta}{\theta/\sqrt{n}}\right)\geq 0.95\ \Leftrightarrow\ 0.1\sqrt{n}\geq 1.96",
                r"$$\text{(A)}\ n\geq\left(\dfrac{1.96}{0.1}\right)^2=384.16\ \Rightarrow\ n=385\quad\text{TRUE}",
                r"$$\text{(B)}\ n\geq\left(\dfrac{1.96}{0.05}\right)^2=1536.64\ \Rightarrow\ n=1537\quad\text{TRUE}",
                r"$$\text{(C)}\ n\geq\left(\dfrac{2.576}{0.1}\right)^2=663.58\ \Rightarrow\ n=664\quad\text{TRUE}",
                "<b>(D) FALSE</b>: θ cancels because both the tolerance and the SD are proportional to θ — the "
                "coefficient of variation of an exponential is 1.",
                ("note", "A RELATIVE tolerance with a distribution whose SD ∝ mean (exponential) makes the "
                         "sample size parameter-free.", "Key idea"),
            ],
        ),
        dict(
            qtype="MCQ", marks=2, topic="Bayes theorem in genetics (carrier risk)", difficulty="Hard",
            text="A recessive disorder requires two copies of allele a. A woman's brother is affected, both her "
                 "parents are unaffected, and she herself is unaffected. She has three children with a man known "
                 "to be a carrier (Aa), and all three children are unaffected. The probability that she is a "
                 "carrier is",
            options=["2/3", "1/2", "27/59", "9/32"],
            answer="C",
            solution=[
                "<b>Concept:</b> prior from Mendelian segregation conditioned on her being unaffected, then update "
                "with the likelihood of three unaffected children.",
                "Affected brother ⇒ both parents are Aa. Her genotype: AA : Aa : aa = 1 : 2 : 1, but she is "
                "unaffected so aa is excluded ⇒ P(carrier) = 2/3 (prior).",
                ("fig", fig_q29),
                "If she is Aa (and he is Aa), each child is affected with probability 1/4, so P(3 unaffected) = "
                "(3/4)<super>3</super> = 27/64. If she is AA, no child can be aa, so P(3 unaffected) = 1.",
                r"$$P(\text{carrier}\mid\text{data})=\dfrac{\frac{2}{3}\cdot\frac{27}{64}}{\frac{2}{3}\cdot\frac{27}{64}+\frac{1}{3}\cdot 1}=\dfrac{54}{54+64}=\dfrac{27}{59}",
                r"$$\approx " + f"{float(_q29):.4f}",
                "(A) is the prior (ignores the children); (B) is the naive 'Aa × AA' guess; (D) 9/32 is the joint "
                "numerator (2/3)(27/64) without normalising.",
                ("note", "Unaffected children are evidence AGAINST her being a carrier, lowering 2/3 to ≈ 0.458.",
                 "Key idea"),
            ],
        ),
        dict(
            qtype="NAT", marks=2, topic="Chi-squared goodness of fit to a Poisson model", difficulty="Hard",
            text=["The number of goals per match in 100 league matches is summarised below. A pundit claims "
                  "goals per match follow a Poisson distribution with mean 1.5.",
                  ("table", [["Goals", "0", "1", "2", "3 or more", "Total"],
                             ["Matches", "20", "35", "25", "20", "100"]]),
                  "The Pearson χ<super>2</super> goodness-of-fit statistic (using the four categories shown, with "
                  "expected counts from the Poisson(1.5) model) is ______ (round off to 2 decimal places)."],
            answer=f"{_q30:.2f}", range=(0.34, 0.36),
            solution=[
                "<b>Concept:</b> derive the expected counts from the hypothesised PMF (lumping the tail into "
                "'3 or more'), then χ<super>2</super> = ∑(O − E)<super>2</super>/E with (k − 1) df (no parameter estimated).",
                r"$$p_0=e^{-1.5}=0.22313,\quad p_1=1.5e^{-1.5}=0.33470,\quad p_2=\dfrac{1.5^2}{2}e^{-1.5}=0.25102",
                r"$$p_{3+}=1-(p_0+p_1+p_2)=0.19115",
                ("table", [["Goals", "O", "E = 100p", "(O − E)<super>2</super>/E"]] +
                 [[g, f"{o}", f"{e:.3f}", f"{c:.4f}"] for g, o, e, c in zip(["0", "1", "2", "≥3"], _O30, _E30, _C30)] +
                 [["Total", "100", "100", f"{_q30:.4f}"]]),
                ("fig", fig_q30),
                r"$$\chi^2\approx " + f"{_q30:.3f}",
                "df = 4 − 1 = 3 (λ was given, not estimated); χ<super>2</super><sub>0.05,3</sub> = 7.815, so the Poisson(1.5) "
                "claim is not rejected — the fit is good.",
                ("note", "Had λ been estimated from the data, df would drop to 2. Always lump the tail so the "
                         "probabilities sum to 1.", "Trap"),
            ],
        ),
    ],
}
