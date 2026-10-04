"""Appendix: statistical tables generated with scipy (standard normal, t, chi-squared)."""
from reportlab.platypus import PageBreak, Spacer
from scipy import stats

from render import FRAME_W, P, make_table


def z_table():
    rows = [["z"] + [f".0{j}" for j in range(10)]]
    for i in range(35):
        z0 = i / 10
        rows.append([f"{z0:.1f}"] + [f"{stats.norm.cdf(z0 + j / 100):.4f}" for j in range(10)])
    w = FRAME_W / 11
    return make_table(rows, col_widths=[w] * 11, font_size=7.6)


def t_table():
    alphas = [0.10, 0.05, 0.025, 0.01, 0.005, 0.001]
    rows = [["ν \\ α (one tail)"] + [str(a) for a in alphas]]
    dfs = list(range(1, 31)) + [40, 50, 60, 80, 100, 120]
    for df in dfs:
        rows.append([str(df)] + [f"{stats.t.ppf(1 - a, df):.3f}" for a in alphas])
    rows.append(["∞ (z)"] + [f"{stats.norm.ppf(1 - a):.3f}" for a in alphas])
    w = FRAME_W / 7
    return make_table(rows, col_widths=[w] * 7, font_size=7.8)


def chi_table():
    tails = [0.995, 0.99, 0.975, 0.95, 0.90, 0.10, 0.05, 0.025, 0.01, 0.005]
    rows = [["ν \\ upper tail"] + [str(a) for a in tails]]
    dfs = list(range(1, 31)) + [40, 50, 60, 80, 100]
    for df in dfs:
        rows.append([str(df)] + [f"{stats.chi2.isf(a, df):.3f}" for a in tails])
    w = FRAME_W / 11
    return make_table(rows, col_widths=[w * 1.2] + [w * 0.98] * 10, font_size=7.2)


def tables_story(register):
    st = []
    h = P("<a name='appendix'/>Part C · Appendix: Statistical Tables", "h1")
    register(h, "Part C · Appendix: Statistical Tables", 0, "appendix")
    st.append(h)
    h = P("<a name='ztab'/>C1. Standard normal CDF Φ(z) = P(Z ≤ z)", "h2")
    register(h, "C1. Standard normal CDF", 1, "ztab")
    st += [h, P("Row gives z to one decimal; column adds the second decimal. For negative z use "
                "Φ(−z) = 1 − Φ(z). Example: Φ(1.96) = 0.9750.", "small"), Spacer(1, 6), z_table(), PageBreak()]
    h = P("<a name='ttab'/>C2. Student t critical values t<sub>α,ν</sub> (P(T &gt; t<sub>α,ν</sub>) = α)", "h2")
    register(h, "C2. Student t critical values", 1, "ttab")
    st += [h, P("For a two-sided test / CI at level α use the column α/2. Example: 95% CI with n = 10 uses "
                "t<sub>0.025, 9</sub> = 2.262.", "small"), Spacer(1, 6), t_table(), PageBreak()]
    h = P("<a name='chitab'/>C3. Chi-squared critical values χ²<sub>α,ν</sub> (P(χ² &gt; χ²<sub>α,ν</sub>) = α)", "h2")
    register(h, "C3. Chi-squared critical values", 1, "chitab")
    st += [h, P("Columns give the area to the RIGHT. Example: χ²<sub>0.05, 4</sub> = 9.488; for a variance CI with "
                "ν = 9 at 95% use 19.023 and 2.700.", "small"), Spacer(1, 6), chi_table(), PageBreak()]
    return st
