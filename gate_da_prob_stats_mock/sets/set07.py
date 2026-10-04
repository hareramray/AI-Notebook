"""Mock Test 07 - Topic test: sampling, CLT, confidence intervals and hypothesis testing."""
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

BLUE, MAROON, GOLD = "#1f5f8b", "#6b1d1d", "#f2c14e"
N = stats.norm

# ---------------------------------------------------------------- computed answers
# Q2  CI upper limit
Q2_xbar, Q2_sig, Q2_n = 52.4, 6.0, 25
Q2_me = 1.96 * Q2_sig / math.sqrt(Q2_n)
Q2_up = Q2_xbar + Q2_me

# Q6  E[X^2] for chi2_10
Q6 = 2 * 10 + 10 ** 2

# Q7  two-sided alpha with |Z|>2.33
Q7_alpha = 2 * N.sf(2.33)

# Q9  normal approx with continuity correction
Q9_z = (59.5 - 50) / 5
Q9_p = N.sf(Q9_z)
Q9_exact = stats.binom.sf(59, 100, 0.5)

# Q10 z statistic
Q10_z = (204.5 - 200) / (15 / 6)

# Q12 sample size
Q12_raw = (1.96 * 8 / 2) ** 2
Q12 = math.ceil(Q12_raw)

# Q13 CLT for sum of 50 bags
Q13_mu, Q13_sd = 50 * 25, 0.5 * math.sqrt(50)
Q13_z = (1252 - Q13_mu) / Q13_sd
Q13_p = N.sf(Q13_z)

# Q14 CI for proportion
Q14_p = 248 / 400
Q14_se = math.sqrt(Q14_p * (1 - Q14_p) / 400)
Q14_me = 1.96 * Q14_se
Q14_lo, Q14_hi = Q14_p - Q14_me, Q14_p + Q14_me

# Q15 one-sample t
Q15_t = (10.6 - 10) / (1.2 / 4)

# Q16 paired t
Q16_before = [148, 152, 139, 160, 145, 155, 150, 142]
Q16_after = [141, 149, 140, 151, 138, 150, 146, 139]
Q16_d = np.array(Q16_before) - np.array(Q16_after)
Q16_dbar = Q16_d.mean()
Q16_ss = float(((Q16_d - Q16_dbar) ** 2).sum())
Q16_s = Q16_d.std(ddof=1)
Q16_t = Q16_dbar / (Q16_s / math.sqrt(8))

# Q17 pooled two-sample t
Q17_sp2 = (9 * 36 + 11 * 64) / 20
Q17_se = math.sqrt(Q17_sp2) * math.sqrt(1 / 10 + 1 / 12)
Q17_t = (82 - 76) / Q17_se

# Q18 GOF 9:3:3:1
Q18_O = [80, 38, 28, 14]
Q18_E = [160 * r / 16 for r in (9, 3, 3, 1)]
Q18_terms = [(o - e) ** 2 / e for o, e in zip(Q18_O, Q18_E)]
Q18_chi = sum(Q18_terms)
Q18_wrong = sum((o - e) ** 2 / o for o, e in zip(Q18_O, Q18_E))

# Q19 2x3 independence
Q19_tab = np.array([[45, 30, 25], [60, 25, 15]])
Q19_E = Q19_tab.sum(1, keepdims=True) * Q19_tab.sum(0, keepdims=True) / Q19_tab.sum()
Q19_terms = (Q19_tab - Q19_E) ** 2 / Q19_E
Q19_chi = float(Q19_terms.sum())

# Q20 2x2
a20, b20, c20, d20 = 18, 182, 42, 158
Q20_chi = 400 * (a20 * d20 - b20 * c20) ** 2 / (200 * 200 * 60 * 340)

# Q21 CI for variance
c975_9, c025_9 = stats.chi2.ppf(0.975, 9), stats.chi2.ppf(0.025, 9)   # 19.023, 2.700
Q21_lo, Q21_hi = 9 * 4.5 / 19.023, 9 * 4.5 / 2.700

# Q22 variance test
Q22_chi = 19 * 0.65 ** 2 / 0.25

# Q23 power
Q23_power = N.cdf((54 - 50) / 2 - 1.645)

# Q24 sample size for power
Q24 = math.ceil(((1.645 + 1.2816) * 10 / 4) ** 2)
Q24_two = math.ceil(((1.96 + 1.2816) * 10 / 4) ** 2)
Q24_80 = math.ceil(((1.645 + 0.8416) * 10 / 4) ** 2)

# Q27 CLT exponential
Q27_p = N.cdf((90 - 100) / (100 / 8))

# Q28 p-value
Q28_p = 2 * N.sf(2.17)

# Q29 Var(S^2)
Q29 = 2 * 81 / 10

assert abs(Q2_up - 54.752) < 1e-9 and Q6 == 120 and Q12 == 62 and Q24 == 54


# ---------------------------------------------------------------- figures
def _clean(ax):
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)


def fig_q2():
    x = np.linspace(46, 58.8, 400)
    se = Q2_sig / 5
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, N.pdf(x, Q2_xbar, se), color=BLUE)
    m = (x > Q2_xbar - Q2_me) & (x < Q2_xbar + Q2_me)
    ax.fill_between(x[m], N.pdf(x[m], Q2_xbar, se), color=BLUE, alpha=0.18)
    for v in (Q2_xbar - Q2_me, Q2_xbar + Q2_me):
        ax.axvline(v, color=MAROON, ls="--", lw=1)
    ax.annotate("", xy=(Q2_xbar + Q2_me, 0.17), xytext=(Q2_xbar, 0.17),
                arrowprops=dict(arrowstyle="<->", color=MAROON))
    ax.text(Q2_xbar + Q2_me / 2, 0.178, "ME = 2.352", ha="center", fontsize=9, color=MAROON)
    ax.text(Q2_xbar + Q2_me, 0.02, " 54.752", color=MAROON, fontsize=9)
    ax.text(Q2_xbar - Q2_me, 0.02, "50.048 ", color=MAROON, fontsize=9, ha="right")
    ax.text(Q2_xbar, 0.08, "95%", ha="center", color=BLUE)
    ax.set_xlabel("x̄ scale (centred at observed x̄ = 52.4, SE = 1.2)")
    _clean(ax)
    return fig


def fig_q4():
    x = np.linspace(-5, 5, 500)
    fig, ax = plt.subplots(figsize=(5.4, 2.6))
    ax.plot(x, N.pdf(x), color=BLUE, label="N(0,1)")
    ax.plot(x, stats.t.pdf(x, 6), color=MAROON, label="t, ν = 6")
    ax.plot(x, stats.t.pdf(x, 2), color=GOLD, label="t, ν = 2", lw=2)
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("x  (t has heavier tails, variance ν/(ν−2) > 1)")
    _clean(ax)
    return fig


def fig_q9():
    k = np.arange(35, 66)
    fig, ax = plt.subplots(figsize=(5.6, 2.7))
    pm = stats.binom.pmf(k, 100, 0.5)
    ax.bar(k, pm, width=1.0, color=["#c9d9e6" if kk < 60 else MAROON for kk in k],
           edgecolor="white", alpha=0.9)
    xx = np.linspace(35, 66, 400)
    ax.plot(xx, N.pdf(xx, 50, 5), color=BLUE)
    m = xx >= 59.5
    ax.fill_between(xx[m], N.pdf(xx[m], 50, 5), color=GOLD, alpha=0.6)
    ax.axvline(59.5, color="k", lw=0.8, ls="--")
    ax.text(59.7, 0.06, "cut at 59.5\n(continuity\ncorrection)", fontsize=8)
    ax.set_xlabel("number of heads X")
    _clean(ax)
    return fig


def fig_q13():
    x = np.linspace(1239, 1261, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, N.pdf(x, Q13_mu, Q13_sd), color=BLUE)
    m = x > 1252
    ax.fill_between(x[m], N.pdf(x[m], Q13_mu, Q13_sd), color=MAROON, alpha=0.35)
    ax.axvline(1250, color="grey", lw=0.8, ls=":")
    ax.annotate(f"P(T > 1252) ≈ {Q13_p:.3f}", xy=(1254, 0.03), xytext=(1255, 0.09),
                arrowprops=dict(arrowstyle="->"), fontsize=9)
    ax.set_xlabel("total load T (kg)  ~  N(1250, 3.536²)")
    _clean(ax)
    return fig


def fig_q15():
    x = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    ax.plot(x, stats.t.pdf(x, 15), color=BLUE)
    for c, col, lab in ((1.753, GOLD, "5% region"), (2.602, MAROON, "1% region")):
        m = x > c
        ax.fill_between(x[m], stats.t.pdf(x[m], 15), color=col, alpha=0.55)
        ax.axvline(c, color=col, lw=1)
    ax.axvline(2.0, color="k", lw=1.6)
    ax.text(2.03, 0.3, "t = 2.0", fontsize=9)
    ax.text(1.70, 0.36, "1.753", fontsize=8, ha="right", color="#8a6d1d")
    ax.text(2.65, 0.08, "2.602", fontsize=8, color=MAROON)
    ax.set_xlabel("t (15 df): t falls in the 5% region but not in the 1% region")
    _clean(ax)
    return fig


def fig_q18():
    lab = ["Round-Yellow", "Round-Green", "Wrinkled-Yellow", "Wrinkled-Green"]
    x = np.arange(4)
    fig, ax = plt.subplots(figsize=(5.6, 2.6))
    ax.bar(x - 0.2, Q18_O, 0.4, color=BLUE, label="Observed")
    ax.bar(x + 0.2, Q18_E, 0.4, color=GOLD, label="Expected (9:3:3:1)")
    ax.set_xticks(x)
    ax.set_xticklabels(lab, fontsize=8)
    ax.legend(frameon=False, fontsize=8)
    ax.set_ylabel("count")
    return fig


def fig_q19():
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    labels = ["Improved", "No change", "Worse"]
    cols = [BLUE, GOLD, MAROON]
    for i, row in enumerate(Q19_tab):
        left = 0
        for j, v in enumerate(row):
            ax.barh(i, v, left=left, color=cols[j], label=labels[j] if i == 0 else None)
            ax.text(left + v / 2, i, str(v), ha="center", va="center", color="white" if j != 1 else "k")
            left += v
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Drug A", "Drug B"])
    ax.set_xlabel("patients (100 per drug)")
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.25))
    return fig


def fig_q21():
    x = np.linspace(0, 26, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.5))
    y = stats.chi2.pdf(x, 9)
    ax.plot(x, y, color=BLUE)
    for m in (x < 2.700, x > 19.023):
        ax.fill_between(x[m], y[m], color=MAROON, alpha=0.4)
    ax.text(0.2, 0.03, "0.025", fontsize=8, color=MAROON)
    ax.text(20, 0.012, "0.025", fontsize=8, color=MAROON)
    ax.text(2.7, -0.012, "2.700", ha="center", fontsize=8)
    ax.text(19.023, -0.012, "19.023", ha="center", fontsize=8)
    ax.text(9, 0.04, "0.95", color=BLUE, ha="center")
    ax.set_xlabel("χ² with 9 df", labelpad=10)
    _clean(ax)
    return fig


def fig_q22():
    x = np.linspace(0, 50, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    y = stats.chi2.pdf(x, 19)
    ax.plot(x, y, color=BLUE)
    m = x > 30.144
    ax.fill_between(x[m], y[m], color=GOLD, alpha=0.7, label="5% region (> 30.144)")
    m = x > 36.191
    ax.fill_between(x[m], y[m], color=MAROON, alpha=0.6, label="1% region (> 36.191)")
    ax.axvline(Q22_chi, color="k", lw=1.5)
    ax.text(Q22_chi + 0.4, 0.05, f"χ² = {Q22_chi:.2f}", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    ax.set_xlabel("χ² with 19 df")
    _clean(ax)
    return fig


def fig_q23():
    x = np.linspace(43, 61, 400)
    se = 2
    c = 50 + 1.645 * se
    fig, ax = plt.subplots(figsize=(5.8, 2.7))
    ax.plot(x, N.pdf(x, 50, se), color=BLUE, label="H₀: μ = 50")
    ax.plot(x, N.pdf(x, 54, se), color=MAROON, label="true μ = 54")
    m = x > c
    ax.fill_between(x[m], N.pdf(x[m], 54, se), color=MAROON, alpha=0.25, label="power")
    ax.fill_between(x[m], N.pdf(x[m], 50, se), color=BLUE, alpha=0.5, label="α = 0.05")
    m2 = x <= c
    ax.fill_between(x[m2], N.pdf(x[m2], 54, se), color=GOLD, alpha=0.5, label="β")
    ax.axvline(c, color="k", ls="--", lw=1)
    ax.text(c + 0.1, 0.205, "x̄ = 53.29", fontsize=8)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    ax.set_xlabel("x̄  (SE = 2)")
    _clean(ax)
    return fig


def fig_q27():
    x = np.linspace(55, 145, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, N.pdf(x, 100, 12.5), color=BLUE)
    m = x < 90
    ax.fill_between(x[m], N.pdf(x[m], 100, 12.5), color=MAROON, alpha=0.35)
    ax.text(72, 0.012, f"≈ {Q27_p:.4f}", color=MAROON)
    ax.set_xlabel("X̄ (hours) ≈ N(100, 12.5²) by CLT")
    _clean(ax)
    return fig


def fig_q28():
    x = np.linspace(-4, 4, 400)
    fig, ax = plt.subplots(figsize=(5.4, 2.4))
    ax.plot(x, N.pdf(x), color=BLUE)
    for m in (x < -2.17, x > 2.17):
        ax.fill_between(x[m], N.pdf(x[m]), color=MAROON, alpha=0.45)
    ax.axvline(-2.17, color="k", lw=1)
    ax.text(-2.12, 0.25, "observed z = −2.17", fontsize=8)
    ax.text(-3.6, 0.04, "0.015", color=MAROON, fontsize=8)
    ax.text(2.9, 0.04, "0.015", color=MAROON, fontsize=8)
    ax.set_xlabel("z  (two-sided p-value = sum of both tails ≈ 0.030)")
    _clean(ax)
    return fig


# ---------------------------------------------------------------- questions
Q = []

# ----- 1-mark -----
Q.append(dict(
    qtype="MCQ", marks=1, topic="Sampling distribution of the mean", difficulty="Easy",
    text="A quality engineer samples n = 36 cartons from a filling line whose fill volume has standard "
         "deviation σ = 12 mL. To make the standard error of the sample mean exactly half of its current "
         "value, the sample size must be",
    options=["72", "144", "108", "288"],
    answer="B",
    solution=[
        "<b>Concept:</b> the standard error of X̄ is SE = σ/√n, so SE scales as 1/√n.",
        "$$SE_{\\mathrm{now}}=\\dfrac{12}{\\sqrt{36}}=2\\ \\mathrm{mL},\\qquad SE_{\\mathrm{target}}=1\\ \\mathrm{mL}",
        "$$\\dfrac{12}{\\sqrt{n}}=1\\ \\Rightarrow\\ \\sqrt{n}=12\\ \\Rightarrow\\ n=144",
        "Equivalently, halving SE requires multiplying n by 2² = 4: 36 × 4 = 144.",
        "Option (A) doubles n, which only reduces SE by a factor √2 (to 1.414 mL).",
        ("note", "Precision improves with the square root of the sample size: k-fold better precision "
                 "costs k²-fold more data.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="z confidence interval for μ", difficulty="Easy",
    text="The diastolic blood pressure of adults in a region is normally distributed with known standard "
         "deviation σ = 6 mmHg. A random sample of 25 adults has mean 52.4 mmHg (after a standardising "
         "offset). The <b>upper limit</b> of the 95% confidence interval for the population mean is ______ "
         "(round off to 2 decimal places). [Use z<sub>0.025</sub> = 1.96.]",
    answer=f"{Q2_up:.2f}", range=(54.74, 54.76),
    solution=[
        "<b>Concept:</b> with σ known, the 100(1−α)% CI for μ is x̄ ± z<sub>α/2</sub> σ/√n.",
        "$$SE=\\dfrac{\\sigma}{\\sqrt{n}}=\\dfrac{6}{\\sqrt{25}}=1.2",
        "$$ME=z_{0.025}\\times SE=1.96\\times 1.2=2.352",
        "$$\\text{Upper limit}=\\bar{x}+ME=52.4+2.352=54.752\\approx 54.75",
        "The full interval is (50.048, 54.752).",
        ("fig", fig_q2),
        ("note", "Use z (not t) because σ is known and the population is normal — the sample size "
                 "being only 25 does not matter here.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=1, topic="Interpreting a confidence interval", difficulty="Medium",
    text="From a sample of tomato plants an agronomist reports a 95% confidence interval for the mean "
         "yield per plant, μ, as (48.2, 53.8) kg, computed as x̄ ± z<sub>0.025</sub>σ/√n. "
         "Which of the following statements is/are correct?",
    options=["If the sampling and interval construction were repeated many times, about 95% of the "
             "intervals so obtained would contain μ.",
             "P(48.2 ≤ μ ≤ 53.8) = 0.95, where μ is the fixed population mean.",
             "The sample mean yield was 51.0 kg.",
             "About 95% of individual plants yield between 48.2 kg and 53.8 kg."],
    answer="A, C",
    solution=[
        "<b>Concept:</b> the confidence level is a property of the <i>procedure</i>; once computed, a "
        "specific interval either contains μ or it does not.",
        "<b>(A) Correct.</b> This is the frequentist meaning of '95% confidence': the random interval "
        "X̄ ± 1.96σ/√n covers μ with probability 0.95 before the data are seen.",
        "<b>(B) Incorrect.</b> μ is a constant and (48.2, 53.8) is a fixed interval, so the probability is "
        "either 0 or 1. The 0.95 refers to the random interval, not to this realised one.",
        "<b>(C) Correct.</b> A z-interval is symmetric about x̄:",
        "$$\\bar{x}=\\dfrac{48.2+53.8}{2}=51.0\\ \\mathrm{kg},\\qquad ME=2.8\\ \\mathrm{kg}",
        "<b>(D) Incorrect.</b> The interval describes where the <i>mean</i> lies, using SE = σ/√n. "
        "Individual plants vary with standard deviation σ, which is √n times larger, so far fewer than "
        "95% of plants fall inside this narrow interval.",
        ("note", "Confusing the CI for μ with a range for individual values (option D) is one of the most "
                 "frequently tested traps.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Properties of the t-distribution", difficulty="Easy",
    text="A random variable T follows Student's t-distribution with 6 degrees of freedom. Var(T) equals",
    options=["1", "1.2", "1.5", "3"],
    answer="C",
    solution=[
        "<b>Concept:</b> for T ∼ t<sub>ν</sub> with ν &gt; 2, E(T) = 0 and Var(T) = ν/(ν − 2).",
        "$$\\mathrm{Var}(T)=\\dfrac{6}{6-2}=\\dfrac{6}{4}=1.5",
        "Option (A) is the variance of N(0,1); the t-distribution always has a variance larger than 1 "
        "because its tails are heavier. Option (B) would be ν/(ν−1), a common misremembering.",
        ("fig", fig_q4),
        ("note", "Var(t<sub>ν</sub>) → 1 as ν → ∞; it is infinite for ν = 2 and undefined for ν = 1 (Cauchy).",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="χ² test of independence: degrees of freedom", difficulty="Easy",
    text="A survey cross-classifies 600 students by <b>study programme</b> (4 categories) and "
         "<b>preferred mode of learning</b> (online, hybrid, offline). For the χ² test of independence on this "
         "contingency table, the degrees of freedom are",
    options=["12", "11", "6", "599"],
    answer="C",
    solution=[
        "<b>Concept:</b> for an r × c contingency table, df = (r − 1)(c − 1).",
        "$$df=(4-1)(3-1)=3\\times 2=6",
        "Reason: the expected counts are fixed by the row and column totals, which impose r + c − 1 "
        "independent constraints on the rc cells:",
        "$$rc-(r+c-1)=12-6=6",
        "(B) is rc − 1, the df of a goodness-of-fit test over 12 categories with no estimated parameters.",
        ("note", "The sample size (600) never enters the degrees of freedom of a χ² contingency test.", "Trap"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Moments of the χ² distribution", difficulty="Medium",
    text="If X ∼ χ²<sub>10</sub> (chi-squared with 10 degrees of freedom), then E(X<super>2</super>) = ______ "
         "(answer as an integer).",
    answer=f"{Q6}", range=(120, 120),
    solution=[
        "<b>Concept:</b> X ∼ χ²<sub>k</sub> has E(X) = k and Var(X) = 2k.",
        "$$E(X)=10,\\qquad \\mathrm{Var}(X)=2(10)=20",
        "$$E(X^2)=\\mathrm{Var}(X)+[E(X)]^2=20+100=120",
        "Check via sum representation: X = Z<sub>1</sub><super>2</super> + … + Z<sub>10</sub><super>2</super>, and "
        "each Z<sub>i</sub><super>2</super> has mean 1 and variance E(Z⁴) − 1 = 3 − 1 = 2.",
        ("note", "Mean k, variance 2k — memorise both; they generate most χ² moment questions.", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Type I error / size of a test", difficulty="Easy",
    text="A two-sided test of H<sub>0</sub>: μ = μ<sub>0</sub> uses the standardised statistic Z, which is "
         "N(0, 1) under H<sub>0</sub>, and rejects H<sub>0</sub> when |Z| &gt; 2.33. "
         "[Φ(2.33) = 0.9901.] The probability of a Type I error is closest to",
    options=["0.0099", "0.0198", "0.9802", "0.0500"],
    answer="B",
    solution=[
        "<b>Concept:</b> P(Type I error) = α = P(reject H<sub>0</sub> | H<sub>0</sub> true).",
        "$$\\alpha=P(|Z|>2.33)=2\\,[1-\\Phi(2.33)]=2(0.0099)=0.0198",
        "(A) counts only one tail — it would be the size of the one-sided test Z &gt; 2.33. "
        "(C) is the probability of correctly retaining H<sub>0</sub>.",
        ("note", "2.33 is the one-sided 1% point; using it in a two-sided rule gives α ≈ 2%.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=1, topic="Properties of the t-distribution", difficulty="Medium",
    text="Let t<sub>α,ν</sub> denote the upper-α point of Student's t-distribution with ν degrees of freedom. "
         "Which of the following statements is/are TRUE?",
    options=["The t-distribution with ν degrees of freedom is symmetric about 0.",
             "The variance of the t-distribution with 5 degrees of freedom is 5/3.",
             "t<sub>0.025,10</sub> &lt; 1.96",
             "For fixed α, t<sub>α,ν</sub> decreases as ν increases and approaches z<sub>α</sub>."],
    answer="A, B, D",
    solution=[
        "<b>Concept:</b> T = Z/√(V/ν) with Z ∼ N(0,1), V ∼ χ²<sub>ν</sub> independent; the extra randomness "
        "in the denominator fattens the tails.",
        "<b>(A) True.</b> The density is proportional to (1 + t²/ν)<super>−(ν+1)/2</super>, an even function of t.",
        "<b>(B) True.</b>",
        "$$\\mathrm{Var}(t_5)=\\dfrac{5}{5-2}=\\dfrac{5}{3}",
        "<b>(C) False.</b> Heavier tails push critical values outward: t<sub>0.025,10</sub> = 2.228 &gt; 1.96.",
        "<b>(D) True.</b> As ν → ∞, V/ν → 1, so t<sub>ν</sub> → N(0,1) and the critical values decrease to "
        "z<sub>α</sub> (e.g. 2.228, 2.086, 2.042, … → 1.960).",
        ("note", "Every t critical value exceeds the matching z value; that is why t-intervals are wider.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Normal approximation to binomial (continuity correction)",
    difficulty="Medium",
    text="A fair coin is tossed 100 times. Using the normal approximation <b>with continuity correction</b>, "
         "P(number of heads ≥ 60) is approximately ______ (round off to 3 decimal places). "
         "[Φ(1.90) = 0.9713.]",
    answer=f"{Q9_p:.3f}", range=(0.028, 0.030),
    solution=[
        "<b>Concept:</b> X ∼ Bin(n, p) ≈ N(np, np(1−p)); for P(X ≥ k) use the cut k − 0.5.",
        "$$\\mu=np=50,\\qquad \\sigma=\\sqrt{np(1-p)}=\\sqrt{25}=5",
        "$$P(X\\geq 60)=P(X>59.5)\\approx P\\left(Z>\\dfrac{59.5-50}{5}\\right)=P(Z>1.90)",
        f"$$=1-0.9713=0.0287",
        f"The exact binomial value is {Q9_exact:.4f}, so the corrected approximation is excellent. "
        "Without the correction one gets P(Z &gt; 2) = 0.0228, a noticeably worse answer.",
        ("fig", fig_q9),
        ("note", "'≥ 60' includes the bar at 60, which spans 59.5 to 60.5 — so the cut is 59.5, not 60.5.",
         "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="z-test statistic", difficulty="Easy",
    text="The breaking strength of a cable has known σ = 15 N. To test H<sub>0</sub>: μ = 200 N, a sample "
         "of 36 cables gives x̄ = 204.5 N. The value of the z-test statistic is",
    options=["0.30", "1.80", "10.80", "1.50"],
    answer="B",
    solution=[
        "<b>Concept:</b> z = (x̄ − μ<sub>0</sub>)/(σ/√n).",
        "$$z=\\dfrac{204.5-200}{15/\\sqrt{36}}=\\dfrac{4.5}{2.5}=1.80",
        "(A) forgets √n (4.5/15). (C) multiplies by √n twice-wrongly (4.5 × 6/2.5). "
        "(D) uses √n in the wrong place (4.5/3).",
        ("note", "Always standardise with the standard error σ/√n, never with σ itself.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=1, topic="Choosing the t-test (paired)", difficulty="Easy",
    text="The resting heart rate of each of 12 athletes is measured before and after a 6-week training "
         "programme. To test whether the programme lowers the mean heart rate (population SD unknown), "
         "the appropriate test and its degrees of freedom are",
    options=["Two-sample pooled t-test with 22 df", "Paired t-test with 11 df",
             "Paired t-test with 12 df", "Two-sample pooled t-test with 23 df"],
    answer="B",
    solution=[
        "<b>Concept:</b> two measurements on the same subject are dependent; analyse the differences "
        "d<sub>i</sub> = before<sub>i</sub> − after<sub>i</sub> as one sample.",
        "$$t=\\dfrac{\\bar{d}}{s_d/\\sqrt{n}},\\qquad df=n-1=12-1=11",
        "(A) and (D) treat the 24 readings as two independent samples, ignoring the pairing (which "
        "removes athlete-to-athlete variability). (C) forgets that one df is used to estimate the mean "
        "difference.",
        ("note", "Same units measured twice → paired. Different units in two groups → two-sample.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=1, topic="Sample size determination for estimating μ", difficulty="Medium",
    text="A nutritionist wants to estimate the mean daily sugar intake (grams) of teenagers to within "
         "± 2 g with 95% confidence. A pilot study suggests σ = 8 g. The minimum sample size required is "
         "______ (answer as an integer). [Use z<sub>0.025</sub> = 1.96.]",
    answer=f"{Q12}", range=(62, 62),
    solution=[
        "<b>Concept:</b> require z<sub>α/2</sub> σ/√n ≤ E, i.e. n ≥ (z<sub>α/2</sub> σ / E)².",
        "$$n\\geq\\left(\\dfrac{1.96\\times 8}{2}\\right)^2=(7.84)^2=61.47",
        "Since n must be an integer and 61 would give a margin slightly above 2 g, round <b>up</b>: n = 62.",
        "$$\\text{Check: } 1.96\\times 8/\\sqrt{62}=1.991\\leq 2,\\quad 1.96\\times 8/\\sqrt{61}=2.008>2",
        ("note", "Sample-size answers are always rounded UP, even 61.01 → 62.", "Trap"),
    ],
))

# ----- 2-mark -----
Q.append(dict(
    qtype="NAT", marks=2, topic="CLT for a sum", difficulty="Medium",
    text="A mill fills rice bags whose weights are independent with mean 25 kg and standard deviation "
         "0.5 kg (distribution not necessarily normal). A truck is loaded with 50 such bags. Using the "
         "central limit theorem, the probability that the total load exceeds 1252 kg is ______ "
         "(round off to 3 decimal places).",
    answer=f"{Q13_p:.3f}", range=(0.282, 0.290),
    solution=[
        "<b>Concept (CLT):</b> for iid X<sub>i</sub> with mean μ and variance σ², the sum "
        "T = ∑X<sub>i</sub> is approximately N(nμ, nσ²) for large n.",
        "$$E(T)=50\\times 25=1250\\ \\mathrm{kg}",
        "$$\\mathrm{Var}(T)=50\\times 0.5^2=12.5,\\qquad SD(T)=\\sqrt{12.5}=3.536\\ \\mathrm{kg}",
        "$$P(T>1252)\\approx P\\left(Z>\\dfrac{1252-1250}{3.536}\\right)=P(Z>0.566)",
        f"$$=1-\\Phi(0.566)\\approx 1-0.7142={Q13_p:.4f}",
        "With the table value z ≈ 0.57: 1 − 0.7157 = 0.2843 (inside the accepted range).",
        ("fig", fig_q13),
        "Common errors: using SD(T) = 50 × 0.5 = 25 (adding standard deviations instead of variances) "
        "gives P ≈ 0.468; using σ/√n treats the total as if it were the mean.",
        ("note", "Variances add for independent variables: SD of a sum grows like √n, SD of a mean shrinks "
                 "like 1/√n.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Confidence interval for a proportion", difficulty="Medium",
    text="In a pre-launch survey, 248 out of 400 randomly chosen customers say they would buy a new "
         "fitness tracker. The approximate 95% confidence interval for the population proportion p is "
         "[z<sub>0.025</sub> = 1.96]",
    options=["(0.572, 0.668)", "(0.580, 0.660)", "(0.557, 0.683)", "(0.596, 0.644)"],
    answer="A",
    solution=[
        "<b>Concept:</b> for large n, p̂ ± z<sub>α/2</sub> √(p̂(1 − p̂)/n).",
        "$$\\hat{p}=\\dfrac{248}{400}=0.62",
        f"$$SE=\\sqrt{{\\dfrac{{0.62\\times 0.38}}{{400}}}}=\\sqrt{{0.000589}}={Q14_se:.5f}",
        f"$$ME=1.96\\times {Q14_se:.5f}={Q14_me:.4f}",
        f"$$\\text{{CI}}=0.62\\pm {Q14_me:.4f}=({Q14_lo:.3f},\\ {Q14_hi:.3f})",
        ("table", [["Option", "What it computes"],
                   ["(A)", "correct: 0.62 ± 1.96 SE"],
                   ["(B)", "uses 1.645 (a 90% interval)"],
                   ["(C)", "uses 2.576 (a 99% interval)"],
                   ["(D)", "0.62 ± 1 SE (forgets the z multiplier)"]]),
        "Validity check: np̂ = 248 and n(1 − p̂) = 152 are both large, so the normal approximation is fine.",
        ("note", "For a CI use p̂ in the SE; for a test of H<sub>0</sub>: p = p<sub>0</sub> use p<sub>0</sub>.",
         "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="One-sample t-test (one-sided)", difficulty="Medium",
    text="A new fertiliser is claimed to raise the mean wheat yield above 10 quintals per acre. On 16 "
         "randomly chosen plots the yields give x̄ = 10.6 and s = 1.2 (yields are normal). For "
         "H<sub>0</sub>: μ = 10 vs H<sub>1</sub>: μ &gt; 10 [t<sub>0.05,15</sub> = 1.753, t<sub>0.01,15</sub> = 2.602], "
         "the correct conclusion is",
    options=["Reject H<sub>0</sub> at both the 5% and 1% levels",
             "Reject H<sub>0</sub> at the 5% level but not at the 1% level",
             "Do not reject H<sub>0</sub> at the 5% level",
             "No conclusion is possible because σ is unknown"],
    answer="B",
    solution=[
        "<b>Concept:</b> σ unknown, normal data → t = (x̄ − μ<sub>0</sub>)/(s/√n) with n − 1 df.",
        "$$t=\\dfrac{10.6-10}{1.2/\\sqrt{16}}=\\dfrac{0.6}{0.3}=2.0,\\qquad df=15",
        "Right-tailed test: reject H<sub>0</sub> when t &gt; t<sub>α,15</sub>.",
        "$$2.0>1.753\\ \\Rightarrow\\ \\text{reject at }5\\%;\\qquad 2.0<2.602\\ \\Rightarrow\\ \\text{retain at }1\\%",
        "Equivalently the p-value lies between 0.01 and 0.05 (it is ≈ 0.032).",
        ("fig", fig_q15),
        "(D) is wrong: an unknown σ is exactly the situation the t-test is designed for.",
        ("note", "If 1.96 or 1.645 were (wrongly) used here the decision at 5% would be the same, but at "
                 "other borderline values the t vs z choice changes the verdict.", "Trap"),
    ],
))

_d_list = ", ".join(str(int(v)) for v in Q16_d)
Q.append(dict(
    qtype="NAT", marks=2, topic="Paired t-test", difficulty="Medium",
    text=["Systolic blood pressure (mmHg) of 8 patients was recorded before and after a month on a "
          "new drug:",
          ("table", [["Patient"] + [str(i) for i in range(1, 9)],
                     ["Before"] + [str(v) for v in Q16_before],
                     ["After"] + [str(v) for v in Q16_after]]),
          "For testing whether the drug reduces mean blood pressure, the value of the paired t statistic "
          "(based on d = Before − After) is ______ (round off to 2 decimal places)."],
    answer=f"{Q16_t:.2f}", range=(4.12, 4.16),
    solution=[
        "<b>Concept:</b> paired t = d̄ / (s<sub>d</sub>/√n) with n − 1 df, where d<sub>i</sub> are the "
        "within-patient differences.",
        f"Differences d<sub>i</sub>: {_d_list}.",
        f"$$\\bar{{d}}=\\dfrac{{{int(Q16_d.sum())}}}{{8}}={Q16_dbar:.3f}",
        f"$$\\sum (d_i-\\bar{{d}})^2={Q16_ss:.3f}\\quad(\\text{{or }}\\sum d_i^2-8\\bar{{d}}^2="
        f"{int((Q16_d**2).sum())}-171.125)",
        f"$$s_d^2=\\dfrac{{{Q16_ss:.3f}}}{{7}}={Q16_ss/7:.4f},\\qquad s_d={Q16_s:.4f}",
        f"$$SE=\\dfrac{{s_d}}{{\\sqrt{{8}}}}={Q16_s/math.sqrt(8):.4f}",
        f"$$t=\\dfrac{{{Q16_dbar:.3f}}}{{{Q16_s/math.sqrt(8):.4f}}}={Q16_t:.3f}",
        "With 7 df, t<sub>0.05,7</sub> = 1.895 and t<sub>0.01,7</sub> = 2.998, so the reduction is significant "
        "even at the 1% level.",
        ("note", "A two-sample t-test on these columns would give t ≈ 1.29 — the pairing removes the large "
                 "patient-to-patient variation and reveals the effect.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Two-sample pooled t-test", difficulty="Medium",
    text="Two teaching methods are compared. Method I: n<sub>1</sub> = 10 students, mean score 82, sample SD 6. "
         "Method II: n<sub>2</sub> = 12 students, mean score 76, sample SD 8. Assuming normal populations with "
         "equal variances, the pooled two-sample t statistic for H<sub>0</sub>: μ<sub>1</sub> = μ<sub>2</sub> is "
         "______ (round off to 2 decimal places).",
    answer=f"{Q17_t:.2f}", range=(1.94, 1.97),
    solution=[
        "<b>Concept:</b> pooled variance s<sub>p</sub>² = [(n<sub>1</sub>−1)s<sub>1</sub>² + (n<sub>2</sub>−1)s<sub>2</sub>²]"
        "/(n<sub>1</sub>+n<sub>2</sub>−2); t = (x̄<sub>1</sub> − x̄<sub>2</sub>)/[s<sub>p</sub>√(1/n<sub>1</sub>+1/n<sub>2</sub>)].",
        "$$s_p^2=\\dfrac{9(36)+11(64)}{10+12-2}=\\dfrac{324+704}{20}=51.4",
        f"$$s_p=\\sqrt{{51.4}}={math.sqrt(Q17_sp2):.4f}",
        f"$$\\sqrt{{\\dfrac{{1}}{{10}}+\\dfrac{{1}}{{12}}}}=\\sqrt{{0.18333}}={math.sqrt(1/10+1/12):.4f}",
        f"$$SE={math.sqrt(Q17_sp2):.4f}\\times {math.sqrt(1/10+1/12):.4f}={Q17_se:.4f}",
        f"$$t=\\dfrac{{82-76}}{{{Q17_se:.4f}}}={Q17_t:.4f}",
        "Degrees of freedom: n<sub>1</sub> + n<sub>2</sub> − 2 = 20. With t<sub>0.025,20</sub> = 2.086, a "
        "two-sided 5% test would NOT reject H<sub>0</sub> (but a one-sided test with t<sub>0.05,20</sub> = 1.725 would).",
        ("note", "Pool the variances weighted by df (9 and 11), not by n, and never average the SDs.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="χ² goodness-of-fit test", difficulty="Medium",
    text=["Mendelian theory predicts that a dihybrid pea cross produces Round-Yellow, Round-Green, "
          "Wrinkled-Yellow and Wrinkled-Green seeds in the ratio 9 : 3 : 3 : 1. Among 160 seeds the observed "
          "counts are 80, 38, 28 and 14 respectively. [χ²<sub>0.05,3</sub> = 7.815, χ²<sub>0.05,4</sub> = 9.488]. "
          "Which option correctly gives the test statistic, its df and the decision at the 5% level?"],
    options=[f"χ² ≈ {Q18_chi:.2f}, df = 3, do not reject the 9:3:3:1 hypothesis",
             f"χ² ≈ {Q18_chi:.2f}, df = 4, do not reject the 9:3:3:1 hypothesis",
             f"χ² ≈ {Q18_wrong:.2f}, df = 3, do not reject the 9:3:3:1 hypothesis",
             f"χ² ≈ {Q18_chi:.2f}, df = 3, reject the 9:3:3:1 hypothesis"],
    answer="A",
    solution=[
        "<b>Concept:</b> χ² = ∑(O − E)²/E with df = (number of categories) − 1 − (parameters estimated).",
        "Expected counts: 160 × (9, 3, 3, 1)/16 = 90, 30, 30, 10.",
        ("table", [["Class", "O", "E", "(O−E)²/E"]] +
         [[n, str(o), f"{e:g}", f"{t:.4f}"] for n, o, e, t in
          zip(["RY", "RG", "WY", "WG"], Q18_O, Q18_E, Q18_terms)] +
         [["Total", "160", "160", f"{Q18_chi:.4f}"]]),
        "$$\\chi^2=\\dfrac{100}{90}+\\dfrac{64}{30}+\\dfrac{4}{30}+\\dfrac{16}{10}" + f"={Q18_chi:.3f}",
        "No parameter is estimated (the ratio is fully specified), so df = 4 − 1 = 3.",
        f"$${Q18_chi:.2f}<7.815\\ \\Rightarrow\\ \\text{{do not reject }}H_0",
        ("fig", fig_q18),
        "(B) uses the wrong df (number of categories). (C) divides by O instead of E. (D) gets the "
        "decision backwards.",
        ("note", "Large χ² ⇒ poor fit ⇒ reject; the GOF test is always upper-tailed.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="χ² test of independence (2 × 3 table)", difficulty="Medium",
    text=["In a clinical trial, 200 patients were randomised equally to two drugs and the outcome recorded:",
          ("table", [["", "Improved", "No change", "Worse", "Total"],
                     ["Drug A", "45", "30", "25", "100"],
                     ["Drug B", "60", "25", "15", "100"],
                     ["Total", "105", "55", "40", "200"]]),
          "The value of the χ² statistic for testing independence of drug and outcome is ______ "
          "(round off to 2 decimal places)."],
    answer=f"{Q19_chi:.2f}", range=(5.08, 5.12),
    solution=[
        "<b>Concept:</b> E<sub>ij</sub> = (row total × column total)/n; χ² = ∑(O − E)²/E with (r−1)(c−1) df.",
        "Expected counts (identical for both rows because both row totals are 100):",
        "$$E_{A1}=\\dfrac{100\\times 105}{200}=52.5,\\quad E_{A2}=\\dfrac{100\\times 55}{200}=27.5,"
        "\\quad E_{A3}=\\dfrac{100\\times 40}{200}=20",
        ("table", [["Cell", "O", "E", "(O−E)²/E"]] +
         [[f"{r}, {c}", str(Q19_tab[i, j]), f"{Q19_E[i, j]:g}", f"{Q19_terms[i, j]:.4f}"]
          for i, r in enumerate(["A", "B"]) for j, c in enumerate(["Imp", "NoCh", "Worse"])]),
        f"$$\\chi^2=2\\,(1.0714+0.2273+1.25)={Q19_chi:.4f}",
        "df = (2 − 1)(3 − 1) = 2 and χ²<sub>0.05,2</sub> = 5.991, so 5.10 &lt; 5.991: independence is not "
        "rejected at 5% (p ≈ 0.078).",
        ("fig", fig_q19),
        ("note", "When row totals are equal, the deviations in the two rows are equal and opposite — compute "
                 "one row and double.", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="χ² test for a 2 × 2 table", difficulty="Medium",
    text=["In a vaccine field study, 400 children were followed for one season:",
          ("table", [["", "Infected", "Not infected", "Total"],
                     ["Vaccinated", "18", "182", "200"],
                     ["Unvaccinated", "42", "158", "200"],
                     ["Total", "60", "340", "400"]]),
          "For the χ² test of independence (without Yates' correction), which statements are correct? "
          "[χ²<sub>0.01,1</sub> = 6.635]"],
    options=["The expected count for the cell (Vaccinated, Infected) is 30.",
             "The test has 2 degrees of freedom.",
             f"The χ² statistic is approximately {Q20_chi:.2f}.",
             "Independence of vaccination status and infection is NOT rejected at the 1% level."],
    answer="A, C",
    solution=[
        "<b>Concept:</b> for a 2 × 2 table [[a, b], [c, d]], χ² = n(ad − bc)²/(r<sub>1</sub>r<sub>2</sub>c<sub>1</sub>c<sub>2</sub>), df = 1.",
        "<b>(A) Correct.</b>",
        "$$E_{11}=\\dfrac{200\\times 60}{400}=30",
        "<b>(B) Incorrect.</b> df = (2 − 1)(2 − 1) = 1.",
        "<b>(C) Correct.</b>",
        "$$ad-bc=18(158)-182(42)=2844-7644=-4800",
        f"$$\\chi^2=\\dfrac{{400\\times 4800^2}}{{200\\times 200\\times 60\\times 340}}=\\dfrac{{9.216\\times 10^9}}"
        f"{{8.16\\times 10^8}}={Q20_chi:.3f}",
        "Check by cells: every |O − E| = 12, so χ² = 144(1/30 + 1/170 + 1/30 + 1/170) = 11.29.",
        "<b>(D) Incorrect.</b> 11.29 &gt; 6.635, so independence IS rejected at 1%: infection rate "
        "9% vs 21% is a real difference.",
        ("note", "In a 2 × 2 table all four |O − E| are equal — a quick consistency check.", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Confidence interval for a variance", difficulty="Medium",
    text="A pharmaceutical plant checks the variability of tablet weight. A random sample of 10 tablets "
         "has sample variance s² = 4.5 mg². Assuming normality, the 95% confidence interval for the "
         "population variance σ² is [χ²<sub>0.025,9</sub> = 19.023, χ²<sub>0.975,9</sub> = 2.700, where "
         "χ²<sub>α,ν</sub> is the upper-α point]",
    options=["(2.13, 15.00)", "(2.37, 16.67)", "(1.46, 3.87)", "(0.24, 1.67)"],
    answer="A",
    solution=[
        "<b>Concept:</b> (n − 1)S²/σ² ∼ χ²<sub>n−1</sub>, so the CI for σ² is "
        "[(n−1)s²/χ²<sub>α/2</sub>, (n−1)s²/χ²<sub>1−α/2</sub>].",
        "$$(n-1)s^2=9\\times 4.5=40.5",
        f"$$\\text{{Lower}}=\\dfrac{{40.5}}{{19.023}}={Q21_lo:.3f},\\qquad \\text{{Upper}}=\\dfrac{{40.5}}{{2.700}}={Q21_hi:.2f}",
        "The large upper critical value gives the LOWER limit and vice versa. The interval is not "
        "symmetric about s² = 4.5 because the χ² density is skewed.",
        ("fig", fig_q21),
        "(B) uses n s² = 45 instead of (n−1)s². (C) is the CI for σ (square roots of A) — not what was "
        "asked. (D) mistakenly divides s² (not 9s²) by the critical values.",
        ("note", "Variance CIs come from the χ² pivot; they are asymmetric and the larger critical value "
                 "goes in the denominator of the lower limit.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="χ² test for a variance", difficulty="Hard",
    text="A bottling machine is acceptable only if the SD of fill volume does not exceed 0.5 mL. A sample "
         "of 20 bottles gives s = 0.65 mL. For H<sub>0</sub>: σ = 0.5 vs H<sub>1</sub>: σ &gt; 0.5 (normal fills), "
         "[χ²<sub>0.05,19</sub> = 30.144, χ²<sub>0.01,19</sub> = 36.191], which option is correct?",
    options=[f"χ² = {Q22_chi:.2f}; reject H<sub>0</sub> at 5% but not at 1%",
             f"χ² = {20*0.65**2/0.25:.2f}; reject H<sub>0</sub> at 5% but not at 1%",
             f"χ² = {19*0.65/0.5:.2f}; do not reject H<sub>0</sub> at 5%",
             f"χ² = {Q22_chi:.2f}; reject H<sub>0</sub> at both 5% and 1%"],
    answer="A",
    solution=[
        "<b>Concept:</b> under H<sub>0</sub>: σ² = σ<sub>0</sub>², the statistic (n − 1)S²/σ<sub>0</sub>² ∼ χ²<sub>n−1</sub>; "
        "for H<sub>1</sub>: σ &gt; σ<sub>0</sub> reject in the upper tail.",
        "$$\\chi^2=\\dfrac{(n-1)s^2}{\\sigma_0^2}=\\dfrac{19\\times 0.65^2}{0.5^2}=\\dfrac{19\\times 0.4225}{0.25}"
        f"={Q22_chi:.3f}",
        "$$30.144<32.11<36.191",
        "So H<sub>0</sub> is rejected at the 5% level but retained at the 1% level.",
        ("fig", fig_q22),
        "(B) uses n = 20 in place of n − 1 = 19. (C) uses s and σ instead of s² and σ². (D) misreads "
        "the 1% critical value.",
        ("note", "The χ² variance test always works with squared quantities: s² and σ<sub>0</sub>².", "Trap"),
    ],
))

Q.append(dict(
    qtype="NAT", marks=2, topic="Power of a one-sided z-test", difficulty="Hard",
    text="Battery life is normal with σ = 10 h. To test H<sub>0</sub>: μ = 50 h against H<sub>1</sub>: μ &gt; 50 h, "
         "a sample of 25 batteries is used with α = 0.05 (z<sub>0.05</sub> = 1.645). If the true mean is 54 h, "
         "the power of the test is ______ (round off to 3 decimal places).",
    answer=f"{Q23_power:.3f}", range=(0.634, 0.643),
    solution=[
        "<b>Concept:</b> power = P(reject H<sub>0</sub> | μ = μ<sub>1</sub>). Find the rejection cut-off on the "
        "x̄ scale under H<sub>0</sub>, then compute its probability under μ<sub>1</sub>.",
        "$$SE=\\dfrac{10}{\\sqrt{25}}=2",
        "Rejection region: x̄ &gt; c, where",
        "$$c=50+1.645\\times 2=53.29",
        "Under μ = 54:",
        "$$\\text{Power}=P(\\bar{X}>53.29\\mid\\mu=54)=P\\left(Z>\\dfrac{53.29-54}{2}\\right)=P(Z>-0.355)",
        f"$$=\\Phi(0.355)\\approx {Q23_power:.4f}",
        f"Hence β = P(Type II error) = 1 − power ≈ {1-Q23_power:.3f}.",
        ("fig", fig_q23),
        ("note", "Power formula for an upper-tailed z-test: Φ(√n(μ<sub>1</sub> − μ<sub>0</sub>)/σ − z<sub>α</sub>) "
                 "= Φ(2 − 1.645).", "Shortcut"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Sample size for a desired power", difficulty="Hard",
    text="For the setting H<sub>0</sub>: μ = μ<sub>0</sub> vs H<sub>1</sub>: μ &gt; μ<sub>0</sub> with σ = 10 and a "
         "one-sided z-test at α = 0.05, a researcher wants power 0.90 when the true mean is μ<sub>0</sub> + 4. "
         "[z<sub>0.05</sub> = 1.645, z<sub>0.10</sub> = 1.2816, z<sub>0.20</sub> = 0.8416, z<sub>0.025</sub> = 1.96]. "
         "The minimum sample size is",
    options=[str(Q24_80), str(Q24), str(Q24_two), "34"],
    answer="B",
    solution=[
        "<b>Concept:</b> power 1 − β requires √n δ/σ ≥ z<sub>α</sub> + z<sub>β</sub>, so "
        "n ≥ [(z<sub>α</sub> + z<sub>β</sub>)σ/δ]².",
        "Derivation: reject when x̄ &gt; μ<sub>0</sub> + z<sub>α</sub>σ/√n. Power at μ<sub>0</sub> + δ is",
        "$$\\Phi\\left(\\dfrac{\\sqrt{n}\\,\\delta}{\\sigma}-z_{\\alpha}\\right)\\geq 0.90\\ \\Leftrightarrow\\ "
        "\\dfrac{\\sqrt{n}\\,\\delta}{\\sigma}-z_{\\alpha}\\geq z_{0.10}",
        "$$n\\geq\\left(\\dfrac{(1.645+1.2816)\\times 10}{4}\\right)^2=(7.316)^2=53.53",
        f"Rounding up: n = {Q24}.",
        ("table", [["Option", "Origin"],
                   [str(Q24_80), "power 0.80 (z<sub>0.20</sub> = 0.8416)"],
                   [str(Q24), "correct"],
                   [str(Q24_two), "two-sided α (1.96 instead of 1.645)"],
                   ["34", "uses 1.645 + 0.8416 with δ/σ wrong (distractor)"]]),
        ("note", "Halving δ quadruples n; raising power from 0.80 to 0.90 costs about 40% more data.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Hypothesis-testing concepts (α, β, power, p-value)", difficulty="Medium",
    text="Consider a z-test about a population mean with known σ. Which of the following statements is/are TRUE?",
    options=["The p-value is the probability that H<sub>0</sub> is true given the observed data.",
             "For a fixed α and a fixed true alternative μ<sub>1</sub>, increasing the sample size increases the power.",
             "For a fixed sample size, reducing α (e.g. from 0.05 to 0.01) increases the Type II error "
             "probability β against a fixed alternative.",
             "If the two-sided 95% confidence interval for μ does not contain μ<sub>0</sub>, then the two-sided "
             "test of H<sub>0</sub>: μ = μ<sub>0</sub> at α = 0.05 rejects H<sub>0</sub>."],
    answer="B, C, D",
    solution=[
        "<b>Concept:</b> α, β and power are long-run error rates of the decision rule; a p-value is a tail "
        "probability computed assuming H<sub>0</sub>.",
        "<b>(A) False.</b> p-value = P(statistic at least as extreme as observed | H<sub>0</sub> true). It is "
        "conditioned ON H<sub>0</sub>, so it cannot be the probability OF H<sub>0</sub>.",
        "<b>(B) True.</b> Power = Φ(√n|μ<sub>1</sub> − μ<sub>0</sub>|/σ − z<sub>α</sub>) (one-sided) increases with n.",
        "<b>(C) True.</b> A smaller α pushes the critical value outward, enlarging the acceptance region, "
        "so β rises (power falls).",
        "<b>(D) True.</b> Duality: the 95% CI is exactly the set of μ<sub>0</sub> values NOT rejected by the "
        "two-sided 5% test.",
        "$$|\\bar{x}-\\mu_0|>1.96\\,\\sigma/\\sqrt{n}\\ \\Leftrightarrow\\ \\mu_0\\notin\\bar{x}\\pm 1.96\\,\\sigma/\\sqrt{n}",
        ("note", "α and β trade off at fixed n; only more data (or a larger effect) reduces both.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Width and margin of error of confidence intervals", difficulty="Medium",
    text="Which of the following statements about confidence intervals is/are TRUE (all other quantities "
         "held fixed)?",
    options=["Quadrupling the sample size halves the width of a z-interval for μ.",
             "From the same data, the 99% z-interval for μ is wider than the 95% z-interval.",
             "With n = 10 and the same s, the t-interval (t<sub>0.025,9</sub> = 2.262) is narrower than the "
             "interval x̄ ± 1.96 s/√n.",
             "When planning a survey for a proportion, using p = 0.5 in n = z²p(1 − p)/E² gives the "
             "smallest required sample size."],
    answer="A, B",
    solution=[
        "<b>Concept:</b> width = 2 × (critical value) × SE, with SE ∝ 1/√n.",
        "<b>(A) True.</b>",
        "$$\\dfrac{\\sigma}{\\sqrt{4n}}=\\dfrac{1}{2}\\cdot\\dfrac{\\sigma}{\\sqrt{n}}",
        "<b>(B) True.</b> 2.576 &gt; 1.96, so the 99% interval is 2.576/1.96 ≈ 1.31 times as wide.",
        "<b>(C) False.</b> 2.262 &gt; 1.96, so the t-interval is about 15% WIDER — the price of estimating σ.",
        "<b>(D) False.</b> p(1 − p) is maximised at p = 0.5 (value 0.25), so p = 0.5 gives the LARGEST "
        "(most conservative) n.",
        "$$\\dfrac{d}{dp}\\,p(1-p)=1-2p=0\\ \\Rightarrow\\ p=0.5,\\quad \\max=0.25",
        ("note", "Conservative planning uses p = 0.5 precisely because it guarantees the margin for any true p.",
         "Key idea"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="CLT for a sample mean (exponential lifetimes)", difficulty="Medium",
    text="LED bulbs have exponentially distributed lifetimes with mean 100 hours. For a random sample of "
         "64 bulbs, the approximate probability that the sample mean lifetime is less than 90 hours is "
         "[Φ(0.8) = 0.7881, Φ(0.1) = 0.5398]",
    options=[f"{Q27_p:.4f}", "0.7881", "0.4602", f"{1-math.exp(-0.9):.4f}"],
    answer="A",
    solution=[
        "<b>Concept:</b> for an exponential with mean θ, the SD is also θ; by CLT X̄ ≈ N(θ, θ²/n).",
        "$$E(\\bar{X})=100,\\qquad SD(\\bar{X})=\\dfrac{100}{\\sqrt{64}}=12.5",
        "$$P(\\bar{X}<90)\\approx \\Phi\\left(\\dfrac{90-100}{12.5}\\right)=\\Phi(-0.8)=1-0.7881=0.2119",
        ("fig", fig_q27),
        "(B) is P(X̄ &gt; 90). (C) forgets √n (z = −0.1). (D) is P(single bulb &lt; 90) = 1 − e<super>−0.9</super>, "
        "which ignores averaging.",
        ("note", "Although each lifetime is highly skewed, n = 64 is ample for the CLT on the mean.", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="p-values for a z-test", difficulty="Medium",
    text="A machine is set to cut rods of mean length μ<sub>0</sub> (σ known). For a two-sided test of "
         "H<sub>0</sub>: μ = μ<sub>0</sub>, the observed statistic is z = −2.17. [Φ(2.17) = 0.9850.] "
         "Which of the following is/are correct?",
    options=["H<sub>0</sub> is rejected at the 1% level.",
             "The two-sided p-value is approximately 0.030.",
             "For the one-sided alternative H<sub>1</sub>: μ &gt; μ<sub>0</sub>, the p-value would be approximately 0.015.",
             "H<sub>0</sub> is rejected at the 5% level."],
    answer="B, D",
    solution=[
        "<b>Concept:</b> two-sided p-value = 2P(Z ≥ |z<sub>obs</sub>|); reject iff p-value ≤ α.",
        f"$$p=2\\,[1-\\Phi(2.17)]=2(0.0150)={Q28_p:.4f}",
        "<b>(B) True.</b> p ≈ 0.030.",
        "<b>(D) True.</b> 0.030 ≤ 0.05.",
        "<b>(A) False.</b> 0.030 &gt; 0.01 (equivalently |z| = 2.17 &lt; 2.576).",
        "<b>(C) False.</b> For H<sub>1</sub>: μ &gt; μ<sub>0</sub>, the p-value is P(Z ≥ −2.17) = 0.985. The "
        "value 0.015 belongs to H<sub>1</sub>: μ &lt; μ<sub>0</sub>, the direction the data actually point.",
        ("fig", fig_q28),
        ("note", "A one-sided p-value is half the two-sided one ONLY when the data fall on the side of "
                 "the alternative.", "Trap"),
    ],
))

Q.append(dict(
    qtype="MCQ", marks=2, topic="Sampling distribution of S² (χ²)", difficulty="Hard",
    text="X<sub>1</sub>, …, X<sub>11</sub> is a random sample from N(μ, 9) and S² is the sample variance "
         "(divisor n − 1). Var(S²) equals",
    options=["16.2", "14.73", "1.62", "18.0"],
    answer="A",
    solution=[
        "<b>Concept:</b> (n − 1)S²/σ² ∼ χ²<sub>n−1</sub>, and Var(χ²<sub>k</sub>) = 2k.",
        "$$\\dfrac{10\\,S^2}{9}\\sim\\chi^2_{10}\\ \\Rightarrow\\ \\mathrm{Var}\\left(\\dfrac{10\\,S^2}{9}\\right)=20",
        "$$\\dfrac{100}{81}\\,\\mathrm{Var}(S^2)=20\\ \\Rightarrow\\ \\mathrm{Var}(S^2)=\\dfrac{20\\times 81}{100}=16.2",
        "General formula: Var(S²) = 2σ⁴/(n − 1) = 2(81)/10 = 16.2.",
        "(B) uses n instead of n − 1 (162/11). (C) forgets to square σ² (2 × 9/10 · …). (D) uses σ⁴/… "
        "with 2σ⁴/9 (df − 1).",
        ("note", "Also E(S²) = σ², so S² is unbiased; its precision improves like 1/(n − 1).", "Key idea"),
    ],
))

Q.append(dict(
    qtype="MSQ", marks=2, topic="Sampling from a normal population (t and χ² facts)", difficulty="Hard",
    text="Let X<sub>1</sub>, …, X<sub>16</sub> be a random sample from N(μ, σ²) with sample mean X̄ and sample "
         "variance S² (divisor 15). Which of the following statements is/are TRUE?",
    options=["X̄ and S² are independent random variables.",
             "(X̄ − μ)/(S/4) has exactly the standard normal distribution.",
             "15S²/σ² has a χ² distribution with 16 degrees of freedom.",
             "∑<sub>i=1</sub><super>16</super> (X<sub>i</sub> − μ)²/σ² has a χ² distribution with 16 degrees of freedom."],
    answer="A, D",
    solution=[
        "<b>Concept:</b> for normal samples, X̄ ∼ N(μ, σ²/n), (n−1)S²/σ² ∼ χ²<sub>n−1</sub>, and the two are independent.",
        "<b>(A) True.</b> Independence of X̄ and S² is a special property of the normal distribution "
        "(it characterises normality).",
        "<b>(B) False.</b> Replacing σ by S gives Student's t with 15 df, not N(0,1):",
        "$$\\dfrac{\\bar{X}-\\mu}{S/\\sqrt{16}}=\\dfrac{(\\bar{X}-\\mu)/(\\sigma/4)}{\\sqrt{\\dfrac{15S^2/\\sigma^2}{15}}}\\sim t_{15}",
        "<b>(C) False.</b> One df is lost in estimating μ by X̄: 15S²/σ² ∼ χ²<sub>15</sub>.",
        "<b>(D) True.</b> (X<sub>i</sub> − μ)/σ are 16 independent N(0,1) variables; the sum of their squares is χ²<sub>16</sub>.",
        "$$\\sum_{i=1}^{16}\\left(\\dfrac{X_i-\\mu}{\\sigma}\\right)^2=\\sum_{i=1}^{16}Z_i^2\\sim\\chi^2_{16}",
        ("note", "Known μ → n df; estimated μ (centre at X̄) → n − 1 df.", "Key idea"),
    ],
))

assert len(Q) == 30
SET = {
    "title": "Topic Test: Sampling, CLT, Confidence Intervals & Hypothesis Testing",
    "subtitle": "An inference-intensive set: sampling distributions, the CLT, z/t/χ² intervals and tests, "
                "errors and power.",
    "focus": "Sampling distribution of the mean and S²; CLT for sums and means; normal approximation to the "
             "binomial with continuity correction; z and t confidence intervals for means and proportions; "
             "sample-size planning; z-tests, one-sample/paired/pooled t-tests; χ² goodness-of-fit and "
             "independence; χ² interval and test for a variance; Type I/II errors and power; properties of "
             "the t and χ² distributions.",
    "minutes": 90,
    "questions": Q,
}
