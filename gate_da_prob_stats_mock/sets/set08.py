"""Mock Test 08 - Topic test: descriptive statistics, covariance, correlation and mixed review."""
import math
from fractions import Fraction as Fr

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"
N = stats.norm

# ---------------------------------------------------------------- computed answers
# Q2 grouped mean
Q2_mid = [10, 30, 50, 70, 90]
Q2_f = [5, 9, 14, 8, 4]
Q2_mean = sum(m * f for m, f in zip(Q2_mid, Q2_f)) / sum(Q2_f)

# Q5
Q5 = 4 * 4 + 9 * 1 - 2 * 2 * 3 * (-0.5)

# Q6
Q6_data = [2, 4, 6, 8, 10]
Q6_s2 = float(np.var(Q6_data, ddof=1))

# Q9 combined mean
Q9 = (30 * 62.5 + 45 * 70) / 75

# Q11 binomial
Q11 = stats.binom.pmf(2, 5, 0.3)

# Q12 exponential memoryless
Q12 = math.exp(-0.4 * 3)

# Q13 combined SD
n1, m1, s1, n2, m2, s2 = 40, 50, 5, 60, 55, 4
Q13_m = (n1 * m1 + n2 * m2) / (n1 + n2)
Q13_var = (n1 * (s1 ** 2 + (m1 - Q13_m) ** 2) + n2 * (s2 ** 2 + (m2 - Q13_m) ** 2)) / (n1 + n2)
Q13_sd = math.sqrt(Q13_var)
# brute-force check: build two groups with exactly these moments
_g1 = np.array([m1 - s1, m1 + s1] * 20)
_g2 = np.array([m2 - s2, m2 + s2] * 30)
assert abs(np.concatenate([_g1, _g2]).std() - Q13_sd) < 1e-12

# Q14 grouped median and mode
Q14_f = [6, 14, 22, 12, 6]
Q14_median = 30 + (30 - 20) / 22 * 10
Q14_alt = 30 + (30.5 - 20) / 22 * 10
Q14_mode = 30 + (22 - 14) / (2 * 22 - 14 - 12) * 10
Q14_mean = sum(m * f for m, f in zip([15, 25, 35, 45, 55], Q14_f)) / 60

# Q15 correlation
Q15_x = np.array([2, 4, 5, 7, 8, 10])
Q15_y = np.array([52, 58, 63, 70, 71, 80])
Q15_Sxx = float(((Q15_x - Q15_x.mean()) ** 2).sum())
Q15_Syy = float(((Q15_y - Q15_y.mean()) ** 2).sum())
Q15_Sxy = float(((Q15_x - Q15_x.mean()) * (Q15_y - Q15_y.mean())).sum())
Q15_r = Q15_Sxy / math.sqrt(Q15_Sxx * Q15_Syy)

# Q16 regression
Q16_yhat = 50 + 12 / 8 * (24 - 20)
Q16_r = 12 / (math.sqrt(8) * 5)

# Q18 covariance matrix
Q18_S = np.array([[4, 1, -1], [1, 9, 2], [-1, 2, 1]])
assert np.all(np.linalg.eigvalsh(Q18_S) > 0)
_a = np.array([1, -2, 1])
Q18_var = int(_a @ Q18_S @ _a)
assert Q18_var == 27

# Q19
Q19_varsum = 16 + 400 + 2 * (-48)

# Q21 joint pmf
Q21_P = np.array([[0.20, 0.10], [0.15, 0.25], [0.05, 0.25]])  # rows X=0,1,2 ; cols Y=0,1
_x = np.array([0, 1, 2]); _y = np.array([0, 1])
EX = float((Q21_P.sum(1) * _x).sum()); EY = float((Q21_P.sum(0) * _y).sum())
EXY = float((Q21_P * np.outer(_x, _y)).sum())
VX = float((Q21_P.sum(1) * _x ** 2).sum() - EX ** 2); VY = float((Q21_P.sum(0) * _y ** 2).sum() - EY ** 2)
Q21_cov = EXY - EX * EY
Q21_rho = Q21_cov / math.sqrt(VX * VY)

# Q22 corrected SD
_n, _mean, _sd = 20, 30, 5
_sum = _n * _mean; _ss = _n * (_sd ** 2 + _mean ** 2)
_sum2 = _sum - 24 + 42; _ss2 = _ss - 24 ** 2 + 42 ** 2
Q22_mean = _sum2 / _n
Q22_var = _ss2 / _n - Q22_mean ** 2
Q22_sd = math.sqrt(Q22_var)

# Q23 Bayes
_pri = [0.5, 0.3, 0.2]; _def = [0.02, 0.03, 0.06]
_joint = [a * b for a, b in zip(_pri, _def)]
Q23 = _joint[2] / sum(_joint)

# Q24 conditional variance  (X~U(0,1), Y|X ~ Bin(10, X))
Q24 = 10 * (Fr(1, 2) - Fr(1, 3)) + Fr(100, 12)
assert Q24 == 10
_rng = np.random.default_rng(8)
_X = _rng.random(400000)
_Y = _rng.binomial(10, _X)
assert abs(_Y.var() - 10) < 0.15

# Q25 P(X+Y<=1) for f = x+y
Q25 = Fr(1, 3)
_U = _rng.random((400000, 2))
_w = _U.sum(1)  # importance weight = f(x,y) = x + y with uniform proposal
assert abs((_w * (_w <= 1)).mean() - 1 / 3) < 0.005

# Q27 committee
Q27 = math.comb(4, 2) * math.comb(6, 3) + math.comb(4, 3) * math.comb(6, 2) + math.comb(4, 4) * math.comb(6, 1)
assert Q27 == math.comb(10, 5) - math.comb(6, 5) - 4 * math.comb(6, 4) == 186

# Q28 percentile
Q28 = 170 + 1.2816 * 8

# Q29 Poisson
Q29 = 1 - math.exp(-1.5) * (1 + 1.5)

# Q30 regression lines
Q30_xbar, Q30_ybar = np.linalg.solve([[3, 2], [6, 1]], [26, 31])


# ---------------------------------------------------------------- figures
def _clean(ax):
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)


def fig_q2():
    fig, ax = plt.subplots(figsize=(5.2, 2.5))
    ax.bar([10, 30, 50, 70, 90], Q2_f, width=20, color=BLUE, edgecolor="white", alpha=0.85)
    for m, f in zip(Q2_mid, Q2_f):
        ax.text(m, f + 0.2, str(f), ha="center", fontsize=9)
    ax.axvline(Q2_mean, color=MAROON, ls="--")
    ax.text(Q2_mean + 1, 13.5, f"mean = {Q2_mean}", color=MAROON, fontsize=9)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xlabel("runs per innings")
    ax.set_ylabel("innings")
    return fig


def fig_q3():
    v = [18, 21, 22, 24, 25, 26, 27, 29, 31, 34, 40]
    fig, ax = plt.subplots(figsize=(5.6, 1.9))
    ax.scatter(v, [0] * 11, color=BLUE, s=40, zorder=3)
    ax.scatter([140], [0], color=MAROON, s=40, zorder=3)
    ax.annotate("", xy=(138, 0.12), xytext=(42, 0.12), arrowprops=dict(arrowstyle="->", color=MAROON))
    ax.text(90, 0.17, "largest value +100", color=MAROON, ha="center", fontsize=9)
    ax.axvline(26, color=GOLD, lw=2)
    ax.text(26, -0.3, "median stays 26", ha="center", fontsize=8)
    ax.set_ylim(-0.45, 0.4)
    ax.set_xlabel("example data (n = 11)")
    _clean(ax)
    return fig


def fig_q7():
    fig, ax = plt.subplots(figsize=(5.6, 1.9))
    st = [dict(med=26, q1=20, q3=32, whislo=8, whishi=55, fliers=[], label="")]
    ax.bxp(st, vert=False, showfliers=False, widths=0.5,
           boxprops=dict(color=BLUE), medianprops=dict(color=MAROON, lw=2),
           whiskerprops=dict(color=BLUE), capprops=dict(color=BLUE))
    for v in (8, 20, 26, 32, 55):
        ax.text(v, 1.38, str(v), ha="center", fontsize=9)
    ax.set_xlim(0, 60)
    ax.set_ylim(0.6, 1.55)
    ax.set_xlabel("delivery time (minutes); whiskers drawn to min and max")
    _clean(ax)
    return fig


def fig_q8():
    x = np.linspace(0, 140, 400)
    a = 4.0
    d = stats.gamma(a, scale=12)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, d.pdf(x), color=BLUE)
    for v, lab, c in ((d.mean(), "mean", MAROON), (d.median(), "median", GOLD), ((a - 1) * 12, "mode", "k")):
        ax.axvline(v, color=c, ls="--", lw=1.4, label=f"{lab} ≈ {v:.0f}")
    ax.legend(frameon=False, fontsize=8.5)
    ax.set_xlabel("right (positive) skew: long right tail pulls mean > median > mode")
    _clean(ax)
    return fig


def fig_q10():
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    M = np.array([[0, 1 / 3, 0], [1 / 3, 0, 1 / 3]])
    ax.imshow(M, cmap="Blues", vmin=0, vmax=0.5, origin="lower")
    for i in range(2):
        for j in range(3):
            ax.text(j, i, "1/3" if M[i, j] else "0", ha="center", va="center",
                    color="white" if M[i, j] else "k")
    ax.set_xticks([0, 1, 2]); ax.set_xticklabels(["−1", "0", "1"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["0", "1"])
    ax.set_xlabel("X"); ax.set_ylabel("Y = X²")
    ax.set_title("joint PMF: zeros where p(x)p(y) > 0", fontsize=9)
    return fig


def fig_q14():
    edges = [10, 20, 30, 40, 50, 60]
    cum = np.cumsum([0] + Q14_f)
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.plot(edges, cum, "-o", color=BLUE, ms=4)
    ax.axhline(30, color=GOLD, ls="--")
    ax.axvline(Q14_median, color=MAROON, ls="--")
    ax.text(Q14_median + 0.6, 4, f"median ≈ {Q14_median:.2f}", color=MAROON, fontsize=9)
    ax.text(11, 31.5, "n/2 = 30", fontsize=9, color="#8a6d1d")
    ax.set_xlabel("yield (kg per plot)")
    ax.set_ylabel("cumulative frequency")
    return fig


def fig_q15():
    fig, ax = plt.subplots(figsize=(5.0, 2.7))
    ax.scatter(Q15_x, Q15_y, color=BLUE, zorder=3)
    b = Q15_Sxy / Q15_Sxx
    xx = np.linspace(1, 11, 10)
    ax.plot(xx, Q15_y.mean() + b * (xx - Q15_x.mean()), color=MAROON)
    ax.axvline(Q15_x.mean(), color="grey", lw=0.7, ls=":")
    ax.axhline(Q15_y.mean(), color="grey", lw=0.7, ls=":")
    ax.text(1.2, 77, f"r = {Q15_r:.3f}", fontsize=10, color=MAROON)
    ax.set_xlabel("hours studied (x)")
    ax.set_ylabel("score (y)")
    return fig


def fig_q19():
    rng = np.random.default_rng(3)
    z = rng.multivariate_normal([0, 0], [[4, 6], [6, 25]], 150)
    X, Y = z[:, 0], z[:, 1]
    fig, axs = plt.subplots(1, 2, figsize=(6.0, 2.6))
    axs[0].scatter(X, Y, s=7, color=BLUE)
    axs[0].set_title("(X, Y): ρ = +0.6", fontsize=9)
    axs[1].scatter(3 - 2 * X, 4 * Y + 1, s=7, color=MAROON)
    axs[1].set_title("(U, V) = (3 − 2X, 4Y + 1): ρ = −0.6", fontsize=9)
    for a in axs:
        a.tick_params(labelsize=7)
    fig.tight_layout()
    return fig


def fig_q21():
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.imshow(Q21_P, cmap="Blues", vmin=0, vmax=0.35, origin="lower")
    for i in range(3):
        for j in range(2):
            ax.text(j, i, f"{Q21_P[i, j]:.2f}", ha="center", va="center",
                    color="white" if Q21_P[i, j] > 0.2 else "k")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Y = 0", "Y = 1"])
    ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["X = 0", "X = 1", "X = 2"])
    ax.set_title("mass shifts to Y = 1 as X grows → ρ > 0", fontsize=9)
    return fig


def fig_q23():
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    ax.axis("off")
    root = (0.05, 0.5)
    ys = [0.85, 0.5, 0.15]
    names = ["M1 (0.5)", "M2 (0.3)", "M3 (0.2)"]
    for y, nm, d, j in zip(ys, names, _def, _joint):
        ax.plot([root[0], 0.4], [root[1], y], color=BLUE)
        ax.text(0.41, y, nm, va="center", fontsize=9, color=BLUE)
        ax.plot([0.6, 0.85], [y, y + 0.07], color=MAROON)
        ax.plot([0.6, 0.85], [y, y - 0.07], color="grey")
        ax.text(0.86, y + 0.07, f"D ({d}) → {j:.3f}", va="center", fontsize=8.5, color=MAROON)
        ax.text(0.86, y - 0.07, f"D′ ({1-d:.2f})", va="center", fontsize=8.5, color="grey")
    ax.plot(*root, "ko", ms=4)
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 1)
    return fig


def fig_q25():
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, color=BLUE))
    ax.fill([0, 1, 0], [0, 0, 1], color=GOLD, alpha=0.6)
    ax.plot([0, 1], [1, 0], color=MAROON)
    ax.text(0.2, 0.2, "x + y ≤ 1", fontsize=9)
    ax.text(0.55, 0.62, "x + y > 1", fontsize=9)
    ax.set_xlim(-0.05, 1.1); ax.set_ylim(-0.05, 1.1)
    ax.set_aspect("equal")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig


def _F26(x):
    x = np.asarray(x, float)
    return np.where(x < 0, 0, np.where(x < 1, 0.2 + 0.3 * x, np.where(x < 2, 0.8 + 0.2 * (x - 1), 1.0)))


def fig_q26():
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    for a, b in ((-0.8, 0), (0, 1), (1, 2), (2, 2.8)):
        xx = np.linspace(a, b, 50, endpoint=False)
        ax.plot(xx, _F26(xx), color=BLUE, lw=2)
    for x0, lo, hi in ((0, 0, 0.2), (1, 0.5, 0.8)):
        ax.plot([x0], [hi], "o", color=BLUE, ms=5)
        ax.plot([x0], [lo], "o", mfc="white", color=BLUE, ms=5)
    ax.set_yticks([0, 0.2, 0.5, 0.8, 1.0])
    ax.grid(alpha=0.3)
    ax.set_xlabel("x")
    ax.set_ylabel("F(x)")
    return fig


def fig_q28():
    x = np.linspace(140, 200, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, N.pdf(x, 170, 8), color=BLUE)
    m = x <= Q28
    ax.fill_between(x[m], N.pdf(x[m], 170, 8), color=BLUE, alpha=0.2)
    m = x > Q28
    ax.fill_between(x[m], N.pdf(x[m], 170, 8), color=MAROON, alpha=0.45)
    ax.axvline(Q28, color=MAROON, ls="--")
    ax.text(Q28 + 0.8, 0.03, f"P90 ≈ {Q28:.2f} cm\n(top 10%)", color=MAROON, fontsize=8.5)
    ax.text(165, 0.015, "0.90", color=BLUE)
    ax.set_xlabel("height (cm) ~ N(170, 8²)")
    _clean(ax)
    return fig


def fig_q29():
    k = np.arange(0, 9)
    fig, ax = plt.subplots(figsize=(5.2, 2.4))
    pm = stats.poisson.pmf(k, 1.5)
    ax.bar(k, pm, color=[GOLD if kk < 2 else BLUE for kk in k], edgecolor="white")
    ax.text(3.2, 0.25, f"P(N ≥ 2) = {Q29:.4f}", color=BLUE)
    ax.text(-0.3, 0.36, "excluded: P(0)+P(1)", color="#8a6d1d", fontsize=8)
    ax.set_xlabel("calls in 5 minutes, N ~ Poisson(1.5)")
    ax.set_ylim(0, 0.4)
    return fig


def fig_q30():
    x = np.linspace(0, 7, 100)
    fig, ax = plt.subplots(figsize=(5.0, 2.8))
    ax.plot(x, (26 - 3 * x) / 2, color=BLUE, label="3x + 2y = 26  (Y on X)")
    ax.plot(x, 31 - 6 * x, color=MAROON, label="6x + y = 31  (X on Y)")
    ax.plot([Q30_xbar], [Q30_ybar], "o", color=GOLD, ms=8, mec="k")
    ax.text(Q30_xbar + 0.2, Q30_ybar + 0.6, "(x̄, ȳ) = (4, 7)", fontsize=9)
    ax.set_ylim(-2, 16)
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return fig


# ---------------------------------------------------------------- questions
Q = []

# ----- 1-mark -----
Q.append(dict(
    qtype="MCQ", marks=1, topic="Linear transformation: mean and SD", difficulty="Easy",
    text="The daily maximum temperatures in a city during May have mean 25 °C and standard deviation 4 °C. "
         "Using F = 1.8C + 32, the mean and standard deviation in °F are respectively",
    options=["77 °F and 7.2 °F", "77 °F and 39.2 °F", "45 °F and 7.2 °F", "77 °F and 51.84 °F"],
    answer="A",
    solution=[
        "<b>Concept:</b> for Y = aX + b, mean(Y) = a·mean(X) + b and SD(Y) = |a|·SD(X); the shift b does "
        "not affect spread.",
        "$$\\bar{F}=1.8(25)+32=77\\ ^{\\circ}\\mathrm{F}",
        "$$SD_F=|1.8|\\times 4=7.2\\ ^{\\circ}\\mathrm{F}",
        "(B) adds 32 to the SD. (C) forgets to add 32 to the mean. (D) gives the variance 1.8² × 16 = 51.84 "
        "(units °F²), not the SD.",
        ("note", "Location shifts move the mean, median and quartiles but leave SD, variance and IQR unchanged.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Mean of grouped data", difficulty="Easy",
    text=["The runs scored by a batter in 40 innings are grouped below.",
          ("table", [["Runs", "0–20", "20–40", "40–60", "60–80", "80–100"],
                     ["Innings", "5", "9", "14", "8", "4"]]),
          "Using class mid-points, the mean runs per innings is ______ (round off to 1 decimal place)."],
    answer=f"{Q2_mean:.1f}", range=(48.4, 48.6),
    solution=[
        "<b>Concept:</b> for grouped data, x̄ = ∑f<sub>i</sub>m<sub>i</sub> / ∑f<sub>i</sub> with m<sub>i</sub> the class mid-point.",
        ("table", [["Class", "m", "f", "f·m"]] +
         [[c, str(m), str(f), str(m * f)] for c, m, f in
          zip(["0–20", "20–40", "40–60", "60–80", "80–100"], Q2_mid, Q2_f)] +
         [["Total", "", "40", "1940"]]),
        "$$\\bar{x}=\\dfrac{1940}{40}=48.5",
        ("fig", fig_q2),
        ("note", "Coding u = (m − 50)/20 gives ∑fu = −10 − 9 + 0 + 8 + 8 = −3, so x̄ = 50 + 20(−3/40) = 48.5.",
         "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=1, topic="Robustness of summary statistics", difficulty="Medium",
    text="Eleven employees of a start-up have distinct monthly salaries. A data-entry error increases the "
         "<b>largest</b> salary by 100 (thousand rupees); all other values are unchanged. Which of the "
         "following is/are TRUE about the corrupted data compared with the original?",
    options=["The mean increases by 100/11 thousand rupees.",
             "The median is unchanged.",
             "The standard deviation is unchanged.",
             "The interquartile range is unchanged."],
    answer="A, B, D",
    solution=[
        "<b>Concept:</b> the mean and SD use every value; order statistics such as the median and quartiles "
        "depend only on ranks near the middle.",
        "<b>(A) True.</b> The total rises by 100, so the mean rises by 100/11 ≈ 9.09.",
        "<b>(B) True.</b> With n = 11 the median is the 6th ordered value; the largest (11th) value moving "
        "further right does not change any rank.",
        "<b>(C) False.</b> The largest value moves farther from the mean, so ∑(x<sub>i</sub> − x̄)² increases; "
        "the SD increases.",
        "<b>(D) True.</b> Q1 and Q3 are determined by values around the 3rd and 9th positions, which are "
        "unchanged; the max is not involved.",
        ("fig", fig_q3),
        ("note", "Median and IQR are resistant (robust) to outliers; mean and SD are not.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=1, topic="Properties of covariance and correlation", difficulty="Medium",
    text="For random variables X and Y with finite, positive variances, and constants a, b, which of the "
         "following statements is/are ALWAYS TRUE?",
    options=["Cov(X, X) = Var(X).",
             "Corr(2X + 3, −Y + 1) = −Corr(X, Y).",
             "If Cov(X, Y) = 0, then X and Y are independent.",
             "Cov(aX, bY) = |ab| Cov(X, Y)."],
    answer="A, B",
    solution=[
        "<b>Concept:</b> Cov(aX + c, bY + d) = ab Cov(X, Y); Corr(aX + c, bY + d) = sign(ab) Corr(X, Y).",
        "<b>(A) True.</b> Cov(X, X) = E[(X − μ)²] = Var(X).",
        "<b>(B) True.</b> Here a = 2, b = −1, so ab &lt; 0 and the correlation flips sign; shifts 3 and 1 are irrelevant.",
        "$$\\mathrm{Corr}(2X+3,-Y+1)=\\dfrac{(2)(-1)\\mathrm{Cov}(X,Y)}{2\\sigma_X\\cdot 1\\sigma_Y}=-\\rho_{XY}",
        "<b>(C) False.</b> Zero covariance means no LINEAR relation only (counter-example: X uniform on "
        "{−1, 0, 1}, Y = X²).",
        "<b>(D) False.</b> The correct factor is ab, not |ab|: Cov(−X, Y) = −Cov(X, Y).",
        ("note", "Absolute values appear for the SD (σ<sub>aX</sub> = |a|σ<sub>X</sub>), not for covariance.", "Trap"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Variance of a linear combination", difficulty="Easy",
    text="Var(X) = 4, Var(Y) = 1 and Cov(X, Y) = −0.5. Then Var(2X − 3Y + 5) = ______ "
         "(answer as an integer).",
    answer=f"{Q5:g}", range=(31, 31),
    solution=[
        "<b>Concept:</b> Var(aX + bY + c) = a²Var(X) + b²Var(Y) + 2ab Cov(X, Y).",
        "$$\\mathrm{Var}(2X-3Y+5)=2^2(4)+(-3)^2(1)+2(2)(-3)(-0.5)",
        "$$=16+9+6=31",
        "The constant 5 contributes nothing. Note that the negative covariance <i>increases</i> the variance "
        "here because the coefficients of X and Y have opposite signs.",
        ("note", "Sign of the cross term = sign(a) × sign(b) × sign(Cov). Track all three.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Sample vs population variance", difficulty="Easy",
    text="Five repeated measurements of a reaction time (ms) are 2, 4, 6, 8, 10 (after subtracting a baseline). "
         "The unbiased sample variance s² (divisor n − 1) is",
    options=["8", "10", "2.83", "3.16"],
    answer="B",
    solution=[
        "<b>Concept:</b> s² = ∑(x<sub>i</sub> − x̄)²/(n − 1) is unbiased for σ²; dividing by n gives the "
        "population (or MLE) variance.",
        "$$\\bar{x}=6,\\qquad \\sum(x_i-\\bar{x})^2=16+4+0+4+16=40",
        "$$s^2=\\dfrac{40}{5-1}=10\\qquad(\\text{divisor }n:\\ 40/5=8)",
        "(A) divides by n; (C) = √8 and (D) = √10 are standard deviations, not variances.",
        ("note", "E[∑(X<sub>i</sub> − X̄)²] = (n − 1)σ²: one degree of freedom is spent on X̄.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Box plot and the 1.5 × IQR rule", difficulty="Easy",
    text=["The five-number summary of food-delivery times (minutes) is: minimum 8, Q1 = 20, median 26, "
          "Q3 = 32, maximum 55.",
          ("fig", fig_q7),
          "Using the 1.5 × IQR rule, which statement is correct?"],
    options=["The IQR is 47 and there are no outliers.",
             "The maximum 55 is an outlier, but the minimum 8 is not.",
             "Both the minimum 8 and the maximum 55 are outliers.",
             "The minimum 8 is an outlier, but the maximum 55 is not."],
    answer="B",
    solution=[
        "<b>Concept:</b> fences are Q1 − 1.5·IQR and Q3 + 1.5·IQR; points beyond them are flagged as outliers.",
        "$$IQR=Q_3-Q_1=32-20=12,\\qquad 1.5\\,IQR=18",
        "$$\\text{Lower fence}=20-18=2,\\qquad \\text{Upper fence}=32+18=50",
        "8 &gt; 2, so 8 is not an outlier; 55 &gt; 50, so 55 is an outlier.",
        "(A) uses the range (55 − 8 = 47) in place of the IQR.",
        "The long upper whisker relative to the lower one also indicates right skew.",
        ("note", "IQR = Q3 − Q1, never max − min. The fences are measured from the quartiles, not from the median.",
         "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Skewness from mean, median and mode", difficulty="Easy",
    text="For the annual household incomes in a district (in ₹ thousand), mean = 52, median = 47, mode = 40 "
         "and SD = 10. Which option correctly describes the shape and Pearson's coefficient "
         "Sk = 3(mean − median)/SD?",
    options=["Positively skewed; Sk = 1.5", "Negatively skewed; Sk = −1.5",
             "Positively skewed; Sk = 1.2", "Positively skewed; Sk = 0.5"],
    answer="A",
    solution=[
        "<b>Concept:</b> mean &gt; median &gt; mode indicates a long right tail (positive skew).",
        "$$Sk=\\dfrac{3(52-47)}{10}=\\dfrac{15}{10}=1.5",
        "(C) is (mean − mode)/SD = 1.2 (Pearson's first coefficient — not the formula asked). "
        "(D) forgets the factor 3.",
        ("fig", fig_q8),
        ("note", "Empirical rule for moderate skew: mean − mode ≈ 3(mean − median). Here 12 vs 15 — close.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Combined mean of two groups", difficulty="Easy",
    text="Section A has 30 students with mean marks 62.5 and Section B has 45 students with mean marks 70. "
         "The mean marks of all 75 students together is ______ (round off to 1 decimal place).",
    answer=f"{Q9:.1f}", range=(66.9, 67.1),
    solution=[
        "<b>Concept:</b> the combined mean is the size-weighted average of group means.",
        "$$\\bar{x}=\\dfrac{30(62.5)+45(70)}{75}=\\dfrac{1875+3150}{75}=\\dfrac{5025}{75}=67.0",
        "The simple average (62.5 + 70)/2 = 66.25 is wrong because the groups have unequal sizes.",
        ("note", "The combined mean always lies between the group means, closer to the larger group.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Zero correlation vs independence", difficulty="Medium",
    text="X takes the values −1, 0, 1 with probability 1/3 each, and Y = X². Which statement is correct?",
    options=["Cov(X, Y) = 0 and X, Y are independent",
             "Cov(X, Y) = 0 but X, Y are not independent",
             "Cov(X, Y) &gt; 0 since Y increases with |X|",
             "Corr(X, Y) = 1 since Y is a function of X"],
    answer="B",
    solution=[
        "<b>Concept:</b> independence ⇒ zero covariance, but not conversely.",
        "$$E(X)=0,\\qquad E(XY)=E(X^3)=\\dfrac{(-1)+0+1}{3}=0",
        "$$\\mathrm{Cov}(X,Y)=E(XY)-E(X)E(Y)=0-0=0",
        "Dependence: P(X = 0, Y = 1) = 0 but P(X = 0)P(Y = 1) = (1/3)(2/3) = 2/9 ≠ 0.",
        ("fig", fig_q10),
        ("note", "Correlation measures LINEAR association only; a perfect quadratic relation can have ρ = 0.",
         "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Binomial PMF (review)", difficulty="Easy",
    text="Each seed in a packet germinates independently with probability 0.3. If 5 seeds are sown, the "
         "probability that exactly 2 germinate is",
    options=[f"{Q11:.4f}", f"{0.3**2*0.7**3:.4f}", f"{stats.binom.cdf(2,5,0.3):.4f}", f"{0.7**5:.4f}"],
    answer="A",
    solution=[
        "<b>Concept:</b> X ∼ Bin(n, p): P(X = k) = C(n, k) p<super>k</super>(1 − p)<super>n−k</super>.",
        "$$P(X=2)=\\binom{5}{2}(0.3)^2(0.7)^3=10\\times 0.09\\times 0.343=0.3087",
        "(B) omits C(5, 2). (C) is P(X ≤ 2). (D) is P(X = 0).",
        ("note", "The binomial coefficient counts the C(5,2) = 10 orders in which 2 successes can occur.", "Trap"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Exponential distribution: memoryless property (review)", difficulty="Easy",
    text="The time (years) until a pump fails is exponential with rate λ = 0.4 per year. Given that a pump "
         "has worked for 2 years, the probability that it works for more than 5 years in total is ______ "
         "(round off to 3 decimal places).",
    answer=f"{Q12:.3f}", range=(0.300, 0.302),
    solution=[
        "<b>Concept:</b> P(X &gt; s + t | X &gt; s) = P(X &gt; t) = e<super>−λt</super> for an exponential.",
        "$$P(X>5\\mid X>2)=\\dfrac{e^{-0.4(5)}}{e^{-0.4(2)}}=e^{-0.4(3)}=e^{-1.2}=0.3012",
        "Using e<super>−0.4×5</super> = 0.1353 ignores the conditioning information.",
        ("note", "Only the REMAINING time (3 years) matters for an exponential lifetime.", "Key idea"),
    ],
))

# ----- 2-mark -----
Q.append(dict(
    qtype="NAT", marks=2, topic="Combined variance of two groups", difficulty="Medium",
    text="In a factory, 40 workers on Shift 1 have mean output 50 units with standard deviation 5, and 60 "
         "workers on Shift 2 have mean output 55 with standard deviation 4 (both SDs computed with divisor "
         "equal to the group size). The standard deviation (divisor 100) of the outputs of all 100 workers "
         "combined is ______ (round off to 2 decimal places).",
    answer=f"{Q13_sd:.2f}", range=(5.05, 5.07),
    solution=[
        "<b>Concept:</b> total variance = mean of within-group variances + variance of group means "
        "(about the combined mean).",
        "$$\\bar{x}=\\dfrac{40(50)+60(55)}{100}=53",
        "$$d_1=50-53=-3,\\qquad d_2=55-53=2",
        "$$\\sigma^2=\\dfrac{n_1(\\sigma_1^2+d_1^2)+n_2(\\sigma_2^2+d_2^2)}{n_1+n_2}",
        "$$=\\dfrac{40(25+9)+60(16+4)}{100}=\\dfrac{1360+1200}{100}=25.6",
        f"$$\\sigma=\\sqrt{{25.6}}={Q13_sd:.4f}",
        "Checks: within part = (40·25 + 60·16)/100 = 19.6; between part = (40·9 + 60·4)/100 = 6.0; sum 25.6.",
        "A common error is to average variances only (19.6, SD 4.43), ignoring the spread between the means.",
        ("note", "This is the data version of Var(Y) = E[Var(Y|G)] + Var(E[Y|G]).", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Median of grouped data", difficulty="Medium",
    text=["Yields (kg) from 60 experimental plots are grouped as follows.",
          ("table", [["Yield", "10–20", "20–30", "30–40", "40–50", "50–60"],
                     ["Plots", "6", "14", "22", "12", "6"]]),
          "The median yield, by linear interpolation within the median class, is approximately"],
    options=[f"{Q14_median:.2f} kg", f"{Q14_alt:.2f} kg", f"{Q14_mode:.2f} kg", f"{Q14_mean:.2f} kg"],
    answer="A",
    solution=[
        "<b>Concept:</b> median = L + [(n/2 − CF)/f] × h, where L, f, h are the lower limit, frequency and "
        "width of the median class and CF the cumulative frequency before it.",
        ("table", [["Class", "f", "Cumulative"], ["10–20", "6", "6"], ["20–30", "14", "20"],
                   ["30–40", "22", "42"], ["40–50", "12", "54"], ["50–60", "6", "60"]]),
        "n/2 = 30 first falls in 30–40 (cumulative 20 → 42). So L = 30, CF = 20, f = 22, h = 10.",
        "$$\\text{Median}=30+\\dfrac{30-20}{22}\\times 10=30+4.545=34.55",
        ("fig", fig_q14),
        f"(B) uses (n + 1)/2 = 30.5 — the ungrouped-data rule. (C) is the grouped MODE "
        f"30 + 8/(44 − 14 − 12) × 10 = {Q14_mode:.2f}. (D) is the grouped MEAN.",
        ("note", f"Mean ({Q14_mean:.2f}) &gt; median ({Q14_median:.2f}) &gt; mode ({Q14_mode:.2f}): a mild positive skew.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Pearson correlation coefficient", difficulty="Medium",
    text=["Hours studied (x) and test score (y) for six students:",
          ("table", [["x", "2", "4", "5", "7", "8", "10"],
                     ["y", "52", "58", "63", "70", "71", "80"]]),
          "The Pearson correlation coefficient r between x and y is ______ (round off to 3 decimal places)."],
    answer=f"{Q15_r:.3f}", range=(round(Q15_r, 3) - 0.002, round(Q15_r, 3) + 0.002),
    solution=[
        "<b>Concept:</b> r = S<sub>xy</sub>/√(S<sub>xx</sub>S<sub>yy</sub>) with S<sub>xy</sub> = ∑(x − x̄)(y − ȳ).",
        f"$$\\bar{{x}}=\\dfrac{{36}}{{6}}=6,\\qquad \\bar{{y}}=\\dfrac{{394}}{{6}}={Q15_y.mean():.4f}",
        ("table", [["x − x̄"] + [f"{v:g}" for v in Q15_x - Q15_x.mean()],
                   ["y − ȳ"] + [f"{v:.3f}" for v in Q15_y - Q15_y.mean()]]),
        f"$$S_{{xx}}={Q15_Sxx:g},\\quad S_{{yy}}={Q15_Syy:.3f},\\quad S_{{xy}}={Q15_Sxy:g}",
        f"(Shortcut: S<sub>xy</sub> = ∑xy − n x̄ ȳ = {int((Q15_x*Q15_y).sum())} − 6 · 6 · {Q15_y.mean():.4f} = {Q15_Sxy:g}; "
        f"S<sub>xx</sub> = ∑x² − n x̄² = {int((Q15_x**2).sum())} − 216 = {Q15_Sxx:g}.)",
        f"$$r=\\dfrac{{{Q15_Sxy:g}}}{{\\sqrt{{{Q15_Sxx:g}\\times {Q15_Syy:.3f}}}}}=\\dfrac{{{Q15_Sxy:g}}}"
        f"{{{math.sqrt(Q15_Sxx*Q15_Syy):.4f}}}={Q15_r:.4f}",
        ("fig", fig_q15),
        f"The fitted slope is S<sub>xy</sub>/S<sub>xx</sub> = {Q15_Sxy/Q15_Sxx:.3f} marks per hour.",
        ("note", "r is unit-free: rescaling hours to minutes or marks to percentages leaves r unchanged.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Regression line via covariance", difficulty="Medium",
    text="For a sample of farms, X = fertiliser used (kg/acre) and Y = yield (quintal/acre) have "
         "x̄ = 20, ȳ = 50, Var(X) = 8, Var(Y) = 25 and Cov(X, Y) = 12. The least-squares prediction of Y "
         "at X = 24 from the regression of Y on X, and the correlation coefficient, are",
    options=[f"ŷ = {Q16_yhat:.2f}, r ≈ {Q16_r:.2f}", f"ŷ = {50 + 12/25*4:.2f}, r ≈ {Q16_r:.2f}",
             f"ŷ = {Q16_yhat:.2f}, r ≈ {12/(8*5):.2f}", f"ŷ = {50 + 12*4:.2f}, r ≈ {Q16_r:.2f}"],
    answer="A",
    solution=[
        "<b>Concept:</b> the Y-on-X line passes through (x̄, ȳ) with slope b<sub>YX</sub> = Cov(X, Y)/Var(X); "
        "r = Cov/(σ<sub>X</sub>σ<sub>Y</sub>).",
        "$$b_{YX}=\\dfrac{12}{8}=1.5",
        "$$\\hat{y}=\\bar{y}+b_{YX}(x-\\bar{x})=50+1.5(24-20)=56",
        "$$r=\\dfrac{12}{\\sqrt{8}\\times\\sqrt{25}}=\\dfrac{12}{14.142}=0.849",
        "(B) uses Cov/Var(Y) = 0.48 — the slope of the regression of X on Y. (C) divides Cov by "
        "Var(X)·SD(Y) instead of SD(X)·SD(Y). (D) uses the covariance itself as slope.",
        "Consistency check: b<sub>YX</sub> = r σ<sub>Y</sub>/σ<sub>X</sub> = 0.849 × 5/2.828 = 1.5. (verified)",
        ("note", "Slope of Y on X divides by Var(X) — the variance of the PREDICTOR.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Valid covariance matrices", difficulty="Medium",
    text="Which of the following 2 × 2 matrices (written row by row) can be the covariance matrix of some "
         "random vector (X, Y)?",
    options=["Rows (4, 2) and (2, 1)", "Rows (1, 2) and (2, 1)",
             "Rows (2, −1) and (−1, 2)", "Rows (3, 1) and (2, 3)"],
    answer="A, C",
    solution=[
        "<b>Concept:</b> a covariance matrix must be symmetric and positive semi-definite; for 2 × 2 this means "
        "diagonal entries ≥ 0 and determinant ≥ 0, i.e. |Cov| ≤ σ<sub>X</sub>σ<sub>Y</sub> (|ρ| ≤ 1).",
        "<b>(A) Valid.</b> det = 4 − 4 = 0 ≥ 0, ρ = 2/(2·1) = 1. Degenerate (Y = X/2 + c) but allowed.",
        "<b>(B) Invalid.</b> det = 1 − 4 = −3 &lt; 0; it would need ρ = 2/(1·1) = 2 &gt; 1.",
        "<b>(C) Valid.</b> det = 4 − 1 = 3 &gt; 0, ρ = −1/2.",
        "$$\\text{eigenvalues of (C)}: 2\\pm 1=\\{1,\\ 3\\}>0",
        "<b>(D) Invalid.</b> Not symmetric (Cov(X, Y) must equal Cov(Y, X)).",
        ("note", "PSD ⇔ Var(aX + bY) = (a, b)Σ(a, b)ᵀ ≥ 0 for all a, b — a negative determinant would allow a "
                 "negative variance.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Covariance matrix computations", difficulty="Medium",
    text=["The covariance matrix of the returns (X, Y, Z) on three stocks is",
          ("table", [["", "X", "Y", "Z"], ["X", "4", "1", "−1"], ["Y", "1", "9", "2"], ["Z", "−1", "2", "1"]]),
          "Which of the following statements is/are correct?"],
    options=["Corr(X, Y) = 1/6", "Var(X + Y) = 15", "Var(X − 2Y + Z) = 27", "Corr(Y, Z) = 2/9"],
    answer="A, B, C",
    solution=[
        "<b>Concept:</b> Var(aᵀV) = aᵀΣa = ∑a<sub>i</sub>²σ<sub>ii</sub> + 2∑<sub>i&lt;j</sub>a<sub>i</sub>a<sub>j</sub>σ<sub>ij</sub>.",
        "<b>(A) Correct.</b>",
        "$$\\rho_{XY}=\\dfrac{1}{\\sqrt{4}\\sqrt{9}}=\\dfrac{1}{6}",
        "<b>(B) Correct.</b> Var(X + Y) = 4 + 9 + 2(1) = 15.",
        "<b>(C) Correct.</b> With a = (1, −2, 1):",
        "$$1(4)+4(9)+1(1)+2[(1)(-2)(1)+(1)(1)(-1)+(-2)(1)(2)]",
        "$$=41+2(-2-1-4)=41-14=27",
        "<b>(D) Incorrect.</b> ρ<sub>YZ</sub> = 2/(√9·√1) = 2/3. (2/9 wrongly divides by Var(Y).)",
        ("note", "Divide covariances by STANDARD DEVIATIONS, not variances, to get correlations.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Correlation and variance under linear transformations", difficulty="Medium",
    text="Corr(X, Y) = 0.6, SD(X) = 2 and SD(Y) = 5. Let U = 3 − 2X and V = 4Y + 1. Then Corr(U, V) and "
         "Var(U + V) are respectively",
    options=["−0.6 and 320", "−0.6 and 512", "0.6 and 320", "−0.6 and 416"],
    answer="A",
    solution=[
        "<b>Concept:</b> Cov(aX + c, bY + d) = ab Cov(X, Y); correlation keeps its magnitude and takes sign(ab).",
        "$$\\mathrm{Cov}(X,Y)=0.6\\times 2\\times 5=6",
        "$$\\mathrm{Cov}(U,V)=(-2)(4)(6)=-48,\\qquad \\mathrm{Corr}(U,V)=-0.6",
        "$$\\mathrm{Var}(U)=4\\times 4=16,\\qquad \\mathrm{Var}(V)=16\\times 25=400",
        f"$$\\mathrm{{Var}}(U+V)=16+400+2(-48)={Q19_varsum}",
        ("fig", fig_q19),
        "(B) adds +96 (sign error). (C) ignores the sign flip. (D) ignores the covariance term.",
        ("note", "A negative scale on one variable flips the sign of ρ; scaling both negatively leaves it.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Covariance of sums and differences", difficulty="Medium",
    text="The scores X and Y of a student on two independent sections of an aptitude test satisfy "
         "Var(X) = 4 and Var(Y) = 12. Which of the following statements is/are correct?",
    options=["Corr(X, X + Y) = 0.5", "Var(X − Y) = Var(X + Y)",
             "Corr(X + Y, X − Y) = −0.5", "Cov(X + Y, X − Y) = 0"],
    answer="A, B, C",
    solution=[
        "<b>Concept:</b> covariance is bilinear: Cov(aX + bY, cX + dY) = ac Var X + bd Var Y + (ad + bc) Cov(X, Y), "
        "and Cov(X, Y) = 0 under independence.",
        "<b>(A) Correct.</b>",
        "$$\\mathrm{Cov}(X,X+Y)=\\mathrm{Var}(X)=4,\\qquad \\mathrm{Var}(X+Y)=4+12=16",
        "$$\\mathrm{Corr}(X,X+Y)=\\dfrac{4}{\\sqrt{4}\\sqrt{16}}=\\dfrac{4}{8}=0.5",
        "<b>(B) Correct.</b> With Cov(X, Y) = 0 both equal 4 + 12 = 16 (the cross term ±2Cov vanishes).",
        "<b>(C) Correct.</b>",
        "$$\\mathrm{Cov}(X+Y,X-Y)=\\mathrm{Var}(X)-\\mathrm{Var}(Y)=4-12=-8",
        "$$\\mathrm{Corr}(X+Y,X-Y)=\\dfrac{-8}{\\sqrt{16}\\sqrt{16}}=-0.5",
        "<b>(D) Incorrect.</b> It is −8; the sum and difference are uncorrelated only when Var(X) = Var(Y).",
        ("note", "Cov(X + Y, X − Y) = Var X − Var Y — a frequent one-line GATE fact.", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Correlation from a joint PMF", difficulty="Medium",
    text=["X = number of defective welds (0, 1, 2) and Y = indicator that a joint fails inspection have the "
          "joint PMF below.",
          ("table", [["", "Y = 0", "Y = 1"], ["X = 0", "0.20", "0.10"], ["X = 1", "0.15", "0.25"],
                     ["X = 2", "0.05", "0.25"]]),
          "The correlation coefficient ρ(X, Y) is closest to"],
    options=[f"{Q21_rho:.3f}", f"{Q21_cov:.3f}", f"{Q21_cov/VY:.3f}", f"{Q21_cov/VX:.3f}"],
    answer="A",
    solution=[
        "<b>Concept:</b> ρ = [E(XY) − E(X)E(Y)] / √(Var X · Var Y), using marginals from row/column sums.",
        "Marginals: P(X = 0, 1, 2) = 0.30, 0.40, 0.30; P(Y = 1) = 0.60.",
        f"$$E(X)={EX:.1f},\\quad E(X^2)=0.40+4(0.30)=1.6,\\quad \\mathrm{{Var}}(X)={VX:.2f}",
        f"$$E(Y)={EY:.1f},\\quad \\mathrm{{Var}}(Y)=0.6(0.4)={VY:.2f}",
        f"$$E(XY)=1(0.25)+2(0.25)={EXY:.2f},\\qquad \\mathrm{{Cov}}=0.75-1.0(0.6)={Q21_cov:.2f}",
        f"$$\\rho=\\dfrac{{0.15}}{{\\sqrt{{0.6\\times 0.24}}}}=\\dfrac{{0.15}}{{0.3795}}={Q21_rho:.4f}",
        ("fig", fig_q21),
        "(B) is the covariance. (C) and (D) divide by a variance instead of the product of SDs.",
        ("note", "In E(XY) only cells with x ≠ 0 and y ≠ 0 contribute — skip the zeros.", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Correcting mean and SD after a recording error", difficulty="Medium",
    text="The mean and standard deviation (divisor n) of 20 sprint times were computed as 30 and 5 seconds. "
         "It was later found that one time recorded as 24 should have been 42. The corrected standard "
         "deviation is ______ (round off to 2 decimal places).",
    answer=f"{Q22_sd:.2f}", range=(5.43, 5.45),
    solution=[
        "<b>Concept:</b> recover ∑x and ∑x² from the wrong summary, correct them, then recompute.",
        "$$\\sum x=20\\times 30=600,\\qquad \\sum x^2=n(\\sigma^2+\\bar{x}^2)=20(25+900)=18500",
        "$$\\sum x_{\\mathrm{new}}=600-24+42=618,\\qquad \\bar{x}_{\\mathrm{new}}=30.9",
        "$$\\sum x^2_{\\mathrm{new}}=18500-576+1764=19688",
        f"$$\\sigma^2_{{\\mathrm{{new}}}}=\\dfrac{{19688}}{{20}}-30.9^2=984.4-954.81={Q22_var:.2f}",
        f"$$\\sigma_{{\\mathrm{{new}}}}=\\sqrt{{{Q22_var:.2f}}}={Q22_sd:.4f}",
        ("note", "Correct BOTH ∑x and ∑x²; then remember the new mean also changes before subtracting x̄².",
         "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Bayes theorem (review)", difficulty="Medium",
    text="Machines M1, M2, M3 produce 50%, 30% and 20% of a factory's bolts, with defect rates 2%, 3% and "
         "6% respectively. A randomly chosen bolt is found defective. The probability that it came from M3 is "
         "closest to",
    options=[f"{Q23:.3f}", f"{_joint[0]/sum(_joint):.3f}", "0.200", "0.060"],
    answer="A",
    solution=[
        "<b>Concept:</b> P(M<sub>i</sub> | D) = P(M<sub>i</sub>)P(D | M<sub>i</sub>) / ∑<sub>j</sub> P(M<sub>j</sub>)P(D | M<sub>j</sub>).",
        ("fig", fig_q23),
        "$$P(D)=0.5(0.02)+0.3(0.03)+0.2(0.06)=0.010+0.009+0.012=0.031",
        f"$$P(M_3\\mid D)=\\dfrac{{0.012}}{{0.031}}={Q23:.4f}",
        f"For comparison P(M1 | D) = 0.010/0.031 = {_joint[0]/sum(_joint):.4f} and P(M2 | D) = 0.009/0.031 = {_joint[1]/sum(_joint):.4f}; the three posteriors sum to 1.",
        "(B) is P(M1 | D). (C) is the prior P(M3) — it ignores the evidence. (D) is the likelihood P(D | M3), the reverse conditional.",
        ("note", "M3 makes only 20% of bolts but, being the least reliable, accounts for nearly 39% of "
                 "the defectives.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Conditional expectation and variance (review)", difficulty="Hard",
    text="The germination probability X of a seed batch is uniformly distributed on (0, 1). Given X = x, the "
         "number Y of seeds that germinate out of 10 is Bin(10, x). Then Var(Y) = ______ "
         "(round off to 2 decimal places).",
    answer=f"{float(Q24):.2f}", range=(9.99, 10.01),
    solution=[
        "<b>Concept (law of total variance):</b> Var(Y) = E[Var(Y | X)] + Var(E[Y | X]).",
        "$$E[Y\\mid X]=10X,\\qquad \\mathrm{Var}(Y\\mid X)=10X(1-X)",
        "$$E[10X(1-X)]=10\\left(E[X]-E[X^2]\\right)=10\\left(\\dfrac{1}{2}-\\dfrac{1}{3}\\right)=\\dfrac{10}{6}",
        "$$\\mathrm{Var}(10X)=100\\times\\dfrac{1}{12}=\\dfrac{100}{12}",
        "$$\\mathrm{Var}(Y)=\\dfrac{10}{6}+\\dfrac{100}{12}=\\dfrac{20+100}{12}=10",
        "Also E(Y) = E[10X] = 5. (In fact Y is uniform on {0, 1, …, 10}, whose variance is (11² − 1)/12 = 10. (verified))",
        "A Monte Carlo simulation with 400 000 draws gives Var(Y) ≈ 10.0.",
        ("note", "Plugging in E(X) = 0.5 to get Bin(10, 0.5) variance 2.5 ignores the uncertainty in X — the "
                 "between-batch term Var(E[Y|X]) dominates.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Joint PDF: region probability (review)", difficulty="Medium",
    text="(X, Y) has joint density f(x, y) = c(x + y) for 0 &lt; x &lt; 1, 0 &lt; y &lt; 1 and 0 elsewhere. "
         "Then P(X + Y ≤ 1) equals",
    options=["1/3", "1/6", "1/2", "2/3"],
    answer="A",
    solution=[
        "<b>Concept:</b> normalise first, then integrate the density over the region.",
        "$$\\int_0^1\\int_0^1 c(x+y)\\,dy\\,dx=c\\left(\\dfrac{1}{2}+\\dfrac{1}{2}\\right)=c=1",
        ("fig", fig_q25),
        "$$P(X+Y\\leq 1)=\\int_0^1\\int_0^{1-x}(x+y)\\,dy\\,dx",
        "$$=\\int_0^1\\left[x(1-x)+\\dfrac{(1-x)^2}{2}\\right]dx=\\int_0^1\\dfrac{1-x^2}{2}\\,dx",
        "$$=\\dfrac{1}{2}\\left(1-\\dfrac{1}{3}\\right)=\\dfrac{1}{3}",
        "Alternative: S = X + Y on the triangle; the density grows with x + y, so the lower triangle "
        "(where x + y is small) gets LESS than half the mass — ruling out (C) and (D).",
        ("note", "(C) = 1/2 is the triangle's AREA — correct only for a uniform density.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Mixed-type CDF (review)", difficulty="Medium",
    text=["A random variable X (waiting time, minutes) has CDF",
          "$$F(x)=0\\ (x<0);\\quad 0.2+0.3x\\ (0\\leq x<1);\\quad 0.8+0.2(x-1)\\ (1\\leq x<2);\\quad 1\\ (x\\geq 2)",
          ("fig", fig_q26),
          "Which of the following is/are correct?"],
    options=["P(X = 0) = 0.2", "P(X = 1) = 0.3", "P(0.5 &lt; X ≤ 1.5) = 0.55", "P(X &lt; 1) = 0.8"],
    answer="A, B, C",
    solution=[
        "<b>Concept:</b> P(X = a) = F(a) − F(a<super>−</super>) (jump size); P(a &lt; X ≤ b) = F(b) − F(a); "
        "P(X &lt; a) = F(a<super>−</super>).",
        "<b>(A) Correct.</b> F(0) − F(0<super>−</super>) = 0.2 − 0 = 0.2 (customers served immediately).",
        "<b>(B) Correct.</b>",
        "$$F(1)-F(1^-)=0.8-(0.2+0.3)=0.3",
        "<b>(C) Correct.</b>",
        "$$F(1.5)-F(0.5)=[0.8+0.1]-[0.2+0.15]=0.90-0.35=0.55",
        "(This includes the jump of 0.3 at x = 1.)",
        "<b>(D) Incorrect.</b> P(X &lt; 1) = F(1<super>−</super>) = 0.5; the value 0.8 is P(X ≤ 1).",
        ("note", "For mixed distributions, &lt; versus ≤ matters exactly at the jump points.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Counting: combinations with constraints (review)", difficulty="Medium",
    text="A 5-member sports committee is to be chosen from 6 men and 4 women. The number of committees "
         "containing at least 2 women is",
    options=["186", "66", "120", "336"],
    answer="A",
    solution=[
        "<b>Concept:</b> split 'at least' into disjoint cases, or use the complement.",
        "$$\\binom{4}{2}\\binom{6}{3}+\\binom{4}{3}\\binom{6}{2}+\\binom{4}{4}\\binom{6}{1}=120+60+6=186",
        "Complement check: total minus (0 or 1 woman):",
        "$$\\binom{10}{5}-\\binom{6}{5}-\\binom{4}{1}\\binom{6}{4}=252-6-60=186",
        "(B) is the complement count (0 or 1 woman). (C) counts EXACTLY 2 women only. (D) is the over-count "
        "C(4,2)·C(8,3) = 6 × 56 = 336 from 'choose 2 women first, then any 3 of the remaining 8'.",
        ("note", "Never 'fix the required women then choose the rest from everyone' — it double-counts "
                 "committees with 3 or 4 women.", "Trap"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Normal percentile (review)", difficulty="Medium",
    text="Adult male heights in a region are N(170, 8²) cm. An army unit admits only men in the tallest 10%. "
         "The minimum admissible height is ______ cm (round off to 2 decimal places). "
         "[Use z<sub>0.10</sub> = 1.2816, i.e. Φ(1.2816) = 0.90.]",
    answer=f"{Q28:.2f}", range=(180.20, 180.30),
    solution=[
        "<b>Concept:</b> the p-th quantile of N(μ, σ²) is μ + z σ with Φ(z) = p.",
        "$$P(X>h)=0.10\\ \\Rightarrow\\ \\dfrac{h-170}{8}=1.2816",
        f"$$h=170+1.2816\\times 8=170+10.2528={Q28:.4f}",
        ("fig", fig_q28),
        "Using 1.645 (the 5% point) gives 183.16 cm — the cut-off for the top 5%, not 10%.",
        ("note", "Top 10% ⇒ upper-tail area 0.10 ⇒ z = +1.2816; bottom 10% would use −1.2816.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Poisson distribution with rescaled rate (review)", difficulty="Medium",
    text="A call centre receives calls as a Poisson process at an average rate of 3 calls per 10 minutes. "
         "The probability of receiving at least 2 calls in a 5-minute interval is",
    options=[f"{Q29:.4f}", f"{1-Q29:.4f}", f"{1-4*math.exp(-3):.4f}", f"{math.exp(-1.5):.4f}"],
    answer="A",
    solution=[
        "<b>Concept:</b> counts in an interval of length t are Poisson(λt); rescale the rate first.",
        "$$\\lambda t=3\\times\\dfrac{5}{10}=1.5",
        "$$P(N\\geq 2)=1-P(0)-P(1)=1-e^{-1.5}(1+1.5)",
        f"$$=1-2.5\\times 0.22313=1-0.55783={Q29:.4f}",
        ("fig", fig_q29),
        "(B) is P(N ≤ 1). (C) forgets to rescale (uses mean 3). (D) is P(N = 0).",
        ("note", "Always convert the rate to the interval in the question before using the PMF.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Two regression lines: means, r and variances", difficulty="Hard",
    text="For bivariate data on (X, Y), the two least-squares regression lines are 3x + 2y = 26 and "
         "6x + y = 31. Which of the following is/are correct?",
    options=["x̄ = 4 and ȳ = 7", "The correlation coefficient is r = −0.5",
             "The correlation coefficient is r = +0.5", "If Var(X) = 9, then Var(Y) = 81"],
    answer="A, B, D",
    solution=[
        "<b>Concept:</b> both regression lines pass through (x̄, ȳ); r² = b<sub>YX</sub> b<sub>XY</sub> with r "
        "having the common sign of the slopes, and b<sub>YX</sub> b<sub>XY</sub> must be ≤ 1.",
        "<b>(A) Correct.</b> Solve simultaneously: from 6x + y = 31, y = 31 − 6x; then 3x + 62 − 12x = 26 ⇒ x = 4, y = 7.",
        "Identify the lines. Try 3x + 2y = 26 as Y on X and 6x + y = 31 as X on Y:",
        "$$b_{YX}=-\\dfrac{3}{2},\\qquad b_{XY}=-\\dfrac{1}{6},\\qquad b_{YX}b_{XY}=\\dfrac{1}{4}\\leq 1\\ \\checkmark",
        "(The other assignment gives b<sub>YX</sub> = −6, b<sub>XY</sub> = −2/3, product 4 &gt; 1 — impossible.)",
        "<b>(B) Correct, (C) Incorrect.</b> r² = 1/4 and both slopes are negative, so r = −0.5.",
        "<b>(D) Correct.</b>",
        "$$b_{YX}=r\\,\\dfrac{\\sigma_Y}{\\sigma_X}\\ \\Rightarrow\\ -1.5=-0.5\\,\\dfrac{\\sigma_Y}{3}\\ \\Rightarrow\\ \\sigma_Y=9,\\ \\mathrm{Var}(Y)=81",
        ("fig", fig_q30),
        ("note", "Test both assignments of the lines: the valid one has slope product ≤ 1.", "Shortcut"),
    ],
))

assert len(Q) == 30
SET = {
    "title": "Topic Test: Descriptive Statistics, Covariance, Correlation & Mixed Review",
    "subtitle": "Summary statistics, spread, shape, covariance algebra and correlation — with a mixed review "
                "of the remaining syllabus.",
    "focus": "Mean, median, mode, variance and SD for grouped and ungrouped data; linear transformations; "
             "combining groups; sample vs population variance; quartiles, box plots and outliers; skewness; "
             "covariance and correlation (properties, Var(aX + bY), linear transforms, zero correlation vs "
             "independence, covariance matrices); regression slopes via covariance. Mixed review: binomial, "
             "exponential, Poisson, normal percentiles, Bayes theorem, conditional variance, joint PDFs, "
             "mixed CDFs and counting.",
    "minutes": 90,
    "questions": Q,
}
