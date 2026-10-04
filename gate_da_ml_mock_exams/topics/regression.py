"""Regression & Model Selection — GATE DA style question templates.

Subtopics: problem framing, simple / multiple linear regression, ridge & lasso,
bias-variance trade-off, cross-validation, gradient descent, MLE / MAP view,
basis functions & feature scaling.
"""
from math import comb

import numpy as np

from core import (Figure, Matrix, Q, Table, fmt, mcq, mcq_numeric, msq_from_statements, nat_hint,
                  nat_range, template)

TOPIC = "Regression & Model Selection"
S_FRAME = "Regression vs classification"
S_SLR = "Simple linear regression"
S_MLR = "Multiple linear regression"
S_RIDGE = "Ridge & Lasso"
S_BV = "Bias-variance trade-off"
S_CV = "Cross-validation"
S_GD = "Gradient descent"
S_MLE = "MLE & MAP view"
S_POLY = "Basis functions & feature scaling"

C1, C2, C3, C4 = "#1f3b73", "#b5562b", "#2e7d32", "#7a7a7a"


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def _tol(v, base=0.01, rel=0.005):
    return max(base, rel * abs(v))


def _nat(v, d=2, base=None, rel=0.005):
    base = 10 ** (-d) if base is None else base
    return nat_range(v, d, tol=_tol(v, base, rel))


def _ols1(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    xm, ym = x.mean(), y.mean()
    sxx = ((x - xm) ** 2).sum()
    sxy = ((x - xm) * (y - ym)).sum()
    syy = ((y - ym) ** 2).sum()
    b1 = sxy / sxx
    b0 = ym - b1 * xm
    yh = b0 + b1 * x
    e = y - yh
    sse = (e ** 2).sum()
    return dict(xm=xm, ym=ym, sxx=sxx, sxy=sxy, sst=syy, b0=b0, b1=b1, yh=yh, e=e, sse=sse,
                ssr=syy - sse, r2=1 - sse / syy if syy > 0 else np.nan)


def _line(a, b, var="x", out="ŷ", d=2):
    sign = "+" if b >= 0 else "−"
    return f"{out} = {fmt(a, d)} {sign} {fmt(abs(b), d)}{var}"


def _xy_table(x, y, xl="x", yl="y", d=2):
    return Table([[xl] + [fmt(v, d) for v in x], [yl] + [fmt(v, d) for v in y]], header=False)


def _scatter(x, y, xlabel="x", ylabel="y", highlight=None, line=None, labels=None):
    x = np.asarray(x, float)
    y = np.asarray(y, float)

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(x, y, s=24, color=C1, zorder=3)
        if highlight is not None:
            ax.scatter([x[highlight]], [y[highlight]], s=110, facecolors="none", edgecolors=C2, lw=1.5, zorder=4)
        if line is not None:
            xs = np.linspace(x.min() - 0.5, x.max() + 0.5, 50)
            ax.plot(xs, line[0] + line[1] * xs, color=C2, lw=1.2)
        if labels is not None:
            for xi, yi, lab in zip(x, y, labels):
                ax.annotate(lab, (xi, yi), textcoords="offset points", xytext=(4, 4), fontsize=7)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(alpha=.3)
        pad = 0.12 * (y.max() - y.min() + 1)
        ax.set_ylim(y.min() - pad, y.max() + pad)

    return draw


def _ols_solution_lines(x, y, f):
    n = len(x)
    rows = [["i"] + [str(i + 1) for i in range(n)],
            ["x<sub>i</sub>−x̄"] + [fmt(v) for v in x - f["xm"]],
            ["y<sub>i</sub>−ȳ"] + [fmt(v) for v in y - f["ym"]],
            ["(x<sub>i</sub>−x̄)(y<sub>i</sub>−ȳ)"] + [fmt(v) for v in (x - f["xm"]) * (y - f["ym"])]]
    return [f"x̄ = {fmt(f['xm'], 3)}, ȳ = {fmt(f['ym'], 3)}.",
            Table(rows, header=False),
            f"S<sub>xx</sub> = Σ(x<sub>i</sub>−x̄)² = {fmt(f['sxx'], 3)},  S<sub>xy</sub> = {fmt(f['sxy'], 3)}.",
            f"β̂<sub>1</sub> = S<sub>xy</sub>/S<sub>xx</sub> = {fmt(f['b1'], 4)},  "
            f"β̂<sub>0</sub> = ȳ − β̂<sub>1</sub>x̄ = {fmt(f['b0'], 4)}."]


def _slr_data(rng, nmin=5, nmax=7, xmax=12, r2min=0.3):
    while True:
        n = int(rng.integers(nmin, nmax + 1))
        x = np.sort(rng.choice(np.arange(1, xmax + 1), n, replace=False)).astype(float)
        b1 = rng.choice([-3, -2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 3])
        b0 = int(rng.integers(-4, 15))
        y = np.round(b0 + b1 * x + rng.integers(-3, 4, n)).astype(float)
        f = _ols1(x, y)
        if f["sst"] > 0 and f["r2"] > r2min:
            return x, y, f


# ============================================================================
# 1-MARK TEMPLATES
# ============================================================================
REG_TASKS = [
    ("Predicting the selling price (in ₹) of a used car from its age and mileage", "price in ₹"),
    ("Forecasting tomorrow's maximum temperature (in °C) of a city", "temperature in °C"),
    ("Estimating a patient's systolic blood pressure from age and BMI", "blood pressure in mm Hg"),
    ("Predicting the number of minutes a user will spend on an app tomorrow", "time in minutes"),
    ("Estimating the remaining useful life (in hours) of a machine from sensor data", "life in hours"),
    ("Predicting crop yield (kg per hectare) from rainfall and fertiliser usage", "yield in kg/ha"),
    ("Estimating the electricity demand (MW) of a city for the next hour", "demand in MW"),
    ("Predicting the delivery time (in minutes) of a food order", "delivery time"),
    ("Estimating the age (in years) of a person from a photograph", "age in years"),
    ("Predicting the closing value of a stock index on the next trading day", "index value"),
    ("Estimating the fuel efficiency (km per litre) of a car from engine specifications", "km per litre"),
    ("Predicting the annual salary of an employee from experience and education", "salary"),
    ("Estimating the PM2.5 concentration (μg/m³) in the air for tomorrow", "concentration"),
    ("Predicting the monthly rent of a flat from its area and locality", "rent"),
    ("Estimating the time (in seconds) a runner will take to finish 400 m", "time in seconds"),
    ("Predicting the percentage of marks a student will score in an exam", "marks percentage"),
]
CLF_TASKS = [
    ("Deciding whether an incoming e-mail is spam or not spam", "spam / not spam"),
    ("Identifying the handwritten digit (0–9) shown in an image", "one of 10 digit classes"),
    ("Predicting whether a loan applicant will default (yes/no)", "yes / no"),
    ("Assigning a news article to one of: sports, politics, business", "one of 3 categories"),
    ("Diagnosing whether a tumour is benign or malignant", "benign / malignant"),
    ("Predicting the blood group (A, B, AB or O) of a person from genetic markers", "one of 4 groups"),
    ("Detecting whether a credit-card transaction is fraudulent", "fraud / genuine"),
    ("Predicting whether it will rain tomorrow (yes/no)", "rain / no rain"),
    ("Recognising the species of an iris flower from petal measurements", "species label"),
    ("Predicting the sentiment (positive / negative / neutral) of a product review", "sentiment class"),
    ("Predicting whether a customer will cancel a subscription next month", "churn / stay"),
    ("Identifying the language (Hindi, Tamil, English, ...) of a sentence", "language label"),
    ("Predicting whether a student will pass or fail a course", "pass / fail"),
    ("Recognising which of 26 letters a typed character image shows", "one of 26 letters"),
    ("Deciding whether an X-ray shows pneumonia or not", "pneumonia / normal"),
]


@template(TOPIC, S_FRAME, marks=1, qtype="MSQ")
def frame_task_type(rng):
    want_reg = rng.random() < 0.6
    R = [(t, f"The output ({o}) is a continuous real-valued quantity → regression.") for t, o in REG_TASKS]
    C = [(t, f"The output ({o}) is a discrete class label → classification.") for t, o in CLF_TASKS]
    T, F = (R, C) if want_reg else (C, R)
    opts, ans, expl = msq_from_statements(rng, T, F)
    kind = "regression" if want_reg else "classification"
    return Q(text=f"Which of the following tasks is/are most naturally formulated as <b>{kind}</b> problems?",
             qtype="MSQ", marks=1, options=opts, answer=ans,
             solution=["A supervised task is <i>regression</i> when the target y is real-valued (loss such as squared "
                       "error), and <i>classification</i> when y takes values in a finite set of labels (loss such "
                       "as cross-entropy or 0–1 loss)."] + expl)


FRAME_ITEMS = [
    ("Ordinary least squares fits a linear regression model by minimising the",
     "sum of squared residuals Σ(y<sub>i</sub> − ŷ<sub>i</sub>)²",
     ["sum of absolute residuals Σ|y<sub>i</sub> − ŷ<sub>i</sub>|", "cross-entropy loss",
      "hinge loss max(0, 1 − yŷ)", "number of misclassified points"],
     "OLS is, by definition, the minimiser of the residual sum of squares."),
    ("A model outputs p̂ = P(y = 1 | x) for a binary label y ∈ {0, 1}. The natural loss to train it is",
     "binary cross-entropy −[y log p̂ + (1−y) log(1−p̂)]",
     ["mean absolute error |y − p̂|", "the R² statistic", "the residual sum of squares of x on y",
      "the hinge loss on p̂"],
     "Cross-entropy is the negative Bernoulli log-likelihood — the standard loss for probabilistic classifiers."),
    ("Which loss function is the most robust to a few large outliers in the target of a regression problem?",
     "Absolute error |y − ŷ|",
     ["Squared error (y − ŷ)²", "Cubic error |y − ŷ|³", "Exponential error e<super>|y−ŷ|</super>",
      "Squared error divided by n"],
     "Absolute error grows linearly in the residual, so outliers have far less influence than with squared "
     "(or faster-growing) losses."),
    ("For a fitted linear regression model ŷ = wᵀx + b, the output for a new input x is",
     "a real number",
     ["a class label in {0, 1}", "a probability in [0, 1]", "a vector of class probabilities summing to 1",
      "a cluster index"],
     "Linear regression outputs an unbounded real-valued prediction."),
    ("Among all functions g, the expected squared loss E[(y − g(x))²] is minimised by",
     "the conditional mean E[y | x]",
     ["the conditional median of y given x", "the conditional mode of y given x", "the marginal mean E[y]",
      "the conditional variance Var(y | x)"],
     "E[(y−g)²|x] = Var(y|x) + (E[y|x] − g)², minimised at g = E[y|x]."),
    ("Among all functions g, the expected absolute loss E[|y − g(x)|] is minimised by",
     "the conditional median of y given x",
     ["the conditional mean E[y | x]", "the conditional mode of y given x", "the marginal mean E[y]",
      "the midrange of y given x"],
     "The minimiser of expected absolute deviation is a median."),
    ("Which of the following is NOT an appropriate evaluation metric for a regression model?",
     "F1-score",
     ["Root mean squared error", "Mean absolute error", "Coefficient of determination R²",
      "Mean squared error"],
     "F1-score combines precision and recall of class predictions; it is a classification metric."),
    ("Which of the following is an appropriate evaluation metric for a binary classifier?",
     "Area under the ROC curve",
     ["Root mean squared error of the class labels", "Coefficient of determination R²",
      "Mean absolute percentage error", "Residual sum of squares"],
     "AUC measures ranking quality of scores for two classes; the others are regression metrics."),
    ("Logistic regression, despite its name, is primarily used for",
     "classification",
     ["regression of real-valued targets", "clustering", "dimensionality reduction", "density estimation"],
     "It models P(y=1|x) = σ(wᵀx + b) and predicts a class by thresholding."),
    ("Predicting the number of goals (0, 1, 2, ...) a football team will score is most naturally a",
     "regression problem with a count-valued target (e.g. Poisson regression)",
     ["clustering problem", "dimensionality-reduction problem", "binary classification problem",
      "unsupervised density-estimation problem"],
     "The target is a numeric count, so it is a (count) regression problem."),
    ("The 0–1 loss L(y, ŷ) = 1[y ≠ ŷ] is the natural loss for",
     "classification",
     ["least-squares regression", "ridge regression", "clustering with k-means", "principal component analysis"],
     "0–1 loss counts mistakes in predicted labels."),
]


@template(TOPIC, S_FRAME, marks=1, qtype="MCQ")
def frame_loss_output(rng):
    stem, c, ds, ex = FRAME_ITEMS[int(rng.integers(len(FRAME_ITEMS)))]
    opts, a = mcq(rng, c, ds)
    return Q(text=stem + ":" if not stem.endswith("?") else stem, qtype="MCQ", marks=1, options=opts, answer=a,
             solution=[ex, f"Hence the answer is <b>{c}</b>."])


SLR_T = [
    ("For the least-squares line (with intercept), the residuals sum to zero: Σe<sub>i</sub> = 0.",
     "The normal equation for β<sub>0</sub> is exactly Σ(y<sub>i</sub> − β̂<sub>0</sub> − β̂<sub>1</sub>x<sub>i</sub>) = 0."),
    ("For the least-squares line, Σx<sub>i</sub>e<sub>i</sub> = 0.", "This is the normal equation for β<sub>1</sub>."),
    ("The least-squares line passes through the point (x̄, ȳ).", "β̂<sub>0</sub> = ȳ − β̂<sub>1</sub>x̄ ⇒ ŷ(x̄) = ȳ."),
    ("Σŷ<sub>i</sub>e<sub>i</sub> = 0 for the least-squares fit.",
     "ŷ is a linear combination of 1 and x, both orthogonal to e."),
    ("The mean of the fitted values ŷ<sub>i</sub> equals ȳ.", "Since Σe<sub>i</sub> = 0, Σŷ<sub>i</sub> = Σy<sub>i</sub>."),
    ("The least-squares slope equals r·s<sub>y</sub>/s<sub>x</sub>, where r is the sample correlation.",
     "β̂<sub>1</sub> = S<sub>xy</sub>/S<sub>xx</sub> = r·√(S<sub>yy</sub>/S<sub>xx</sub>)."),
    ("In simple linear regression with intercept, R² = r².", "SSR/SST = S<sub>xy</sub>²/(S<sub>xx</sub>S<sub>yy</sub>) = r²."),
    ("The least-squares slope has the same sign as the sample correlation r.", "β̂<sub>1</sub> = r·s<sub>y</sub>/s<sub>x</sub> with s<sub>x</sub>, s<sub>y</sub> &gt; 0."),
    ("SST = SSR + SSE for the least-squares fit with intercept.",
     "Cross term 2Σ(ŷ<sub>i</sub>−ȳ)e<sub>i</sub> vanishes by the normal equations."),
    ("If every y<sub>i</sub> is multiplied by a constant c, the least-squares slope is multiplied by c.",
     "S<sub>xy</sub> scales by c while S<sub>xx</sub> is unchanged."),
    ("Adding the same constant to every x<sub>i</sub> leaves the least-squares slope unchanged.",
     "Deviations x<sub>i</sub> − x̄ are unchanged; only the intercept changes."),
    ("The product of the slope of the y-on-x line and the slope of the x-on-y line equals r².",
     "(S<sub>xy</sub>/S<sub>xx</sub>)(S<sub>xy</sub>/S<sub>yy</sub>) = r²."),
    ("R² is unchanged if y is replaced by a + by for any constants a and b ≠ 0.",
     "r² is invariant to affine changes of either variable."),
    ("If r = 0, the least-squares line is horizontal at height ȳ.", "β̂<sub>1</sub> = 0 and β̂<sub>0</sub> = ȳ."),
]
SLR_F = [
    ("For the least-squares line, Σe<sub>i</sub>² = 0.", "Only for a perfect fit; in general SSE &gt; 0."),
    ("The slope of the x-on-y regression line is always the reciprocal of the slope of the y-on-x line.",
     "Their product is r², so they are reciprocals only when |r| = 1."),
    ("For OLS with an intercept, the training R² can be negative.", "With an intercept, 0 ≤ R² ≤ 1 on the training data."),
    ("Σy<sub>i</sub>e<sub>i</sub> = 0 for the least-squares fit.",
     "Σy<sub>i</sub>e<sub>i</sub> = Σ(ŷ<sub>i</sub>+e<sub>i</sub>)e<sub>i</sub> = SSE, which is generally positive."),
    ("The least-squares line always passes through (median of x, median of y).", "It passes through the means (x̄, ȳ)."),
    ("The least-squares slope equals r·s<sub>x</sub>/s<sub>y</sub>.", "The correct expression is r·s<sub>y</sub>/s<sub>x</sub>."),
    ("Doubling every x<sub>i</sub> doubles the least-squares slope.", "S<sub>xx</sub> becomes 4× and S<sub>xy</sub> 2×, so the slope halves."),
    ("Least squares minimises the sum of absolute residuals.", "That is least absolute deviations (LAD) regression."),
    ("Least squares minimises the sum of perpendicular distances from the points to the line.",
     "OLS minimises vertical distances; perpendicular distances give total least squares."),
    ("Residuals of a least-squares fit without an intercept always sum to zero.",
     "Without the intercept column there is no normal equation forcing Σe<sub>i</sub> = 0."),
    ("In simple linear regression, R² = r (the correlation itself).", "R² = r², which is non-negative."),
    ("SST = SSR − SSE.", "The decomposition is SST = SSR + SSE."),
    ("If r = 0 the least-squares line is ŷ = 0.", "It is ŷ = ȳ."),
    ("Converting y from metres to centimetres leaves the least-squares slope unchanged.",
     "y is multiplied by 100, so the slope is multiplied by 100."),
]


@template(TOPIC, S_SLR, marks=1, qtype="MSQ")
def slr_properties(rng):
    opts, ans, expl = msq_from_statements(rng, SLR_T, SLR_F)
    return Q(text="A simple linear regression ŷ = β̂<sub>0</sub> + β̂<sub>1</sub>x is fitted by ordinary least squares "
                  "(with intercept) to data (x<sub>i</sub>, y<sub>i</sub>), i = 1, …, n, with residuals "
                  "e<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub> and sample correlation r. "
                  "Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_SLR, marks=1, qtype="NAT")
def slr_from_summary(rng):
    while True:
        r = float(rng.choice(np.r_[np.arange(-0.9, -0.29, 0.05), np.arange(0.3, 0.91, 0.05)]).round(2))
        sx = int(rng.integers(2, 9))
        sy = int(rng.integers(2, 16))
        if sx != sy:
            break
    xm = int(rng.integers(5, 40))
    ym = int(rng.integers(20, 120))
    b1 = r * sy / sx
    b0 = ym - b1 * xm
    v = int(rng.integers(4))
    stem = (f"For a data set, x̄ = {xm}, ȳ = {ym}, s<sub>x</sub> = {sx}, s<sub>y</sub> = {sy} and the sample "
            f"correlation between x and y is r = {fmt(r)}. ")
    sol = [f"β̂<sub>1</sub> = r·s<sub>y</sub>/s<sub>x</sub> = {fmt(r)} × {sy}/{sx} = {fmt(b1, 4)}."]
    if v == 0:
        ans, q = b1, "The slope of the least-squares regression line of y on x is"
    elif v == 1:
        ans, q = b0, "The intercept of the least-squares regression line of y on x is"
        sol.append(f"β̂<sub>0</sub> = ȳ − β̂<sub>1</sub>x̄ = {ym} − ({fmt(b1, 4)})({xm}) = {fmt(b0, 4)}.")
    elif v == 2:
        k = int(rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]))
        x0 = xm + k
        ans = ym + b1 * k
        q = f"Using the least-squares regression line of y on x, the predicted value of y at x = {x0} is"
        sol.append(f"ŷ = ȳ + β̂<sub>1</sub>(x<sub>0</sub> − x̄) = {ym} + ({fmt(b1, 4)})({k}) = {fmt(ans, 4)} "
                   "(the line passes through (x̄, ȳ)).")
    else:
        ans = r * sx / sy
        q = "The slope of the least-squares regression line of <b>x on y</b> (i.e. x̂ = a + by) is"
        sol = [f"Regressing x on y swaps the roles: b = r·s<sub>x</sub>/s<sub>y</sub> = {fmt(r)} × {sx}/{sy} "
               f"= {fmt(ans, 4)}.",
               f"(A common mistake is to use r·s<sub>y</sub>/s<sub>x</sub> = {fmt(b1, 4)}, the y-on-x slope.)"]
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=stem + q + " _______ " + nat_hint(2), qtype="NAT", marks=1, answer=_nat(ans, 2),
             nat_hint=nat_hint(2), solution=sol)


RESID_OPTS = {
    "funnel": ("Non-constant error variance (heteroscedasticity)",
               "The spread of residuals grows with the fitted value (funnel shape) → the constant-variance "
               "assumption is violated; a transformation of y (e.g. log) or weighted least squares may help."),
    "curve": ("A non-linear relationship not captured by the model (e.g. a missing x² term)",
              "Residuals show a systematic U / ∩ pattern → the mean function is mis-specified; add non-linear "
              "terms or basis functions."),
    "random": ("No evident violation of the linear-model assumptions",
               "Residuals form a structureless horizontal band around 0 with constant spread → the fit is adequate."),
    "outlier": ("A single outlying observation, with the rest of the fit looking adequate",
                "All residuals lie in a narrow band except one far from 0 → an outlier that should be investigated."),
}


@template(TOPIC, S_SLR, marks=1, qtype="MCQ")
def residual_plot(rng):
    kinds = list(RESID_OPTS)
    kind = kinds[int(rng.integers(4))]
    n = 60
    f = np.sort(rng.uniform(10, 50, n))
    if kind == "funnel":
        e = rng.normal(0, 1, n) * 0.18 * (f - 7)
    elif kind == "curve":
        s = rng.choice([-1, 1])
        e = s * 0.03 * ((f - 30) ** 2 - ((f - 30) ** 2).mean()) + rng.normal(0, 0.9, n)
    elif kind == "random":
        e = rng.normal(0, 2.0, n)
    else:
        e = rng.normal(0, 1.3, n)
        j = int(rng.integers(5, n - 5))
        e[j] = rng.choice([-1, 1]) * rng.uniform(9, 11)

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(f, e, s=12, color=C1)
        ax.axhline(0, color=C4, lw=1, ls="--")
        ax.set_xlabel("fitted value ŷ")
        ax.set_ylabel("residual e = y − ŷ")
        ax.grid(alpha=.3)

    opts, a = mcq(rng, RESID_OPTS[kind][0], [RESID_OPTS[k][0] for k in kinds if k != kind])
    return Q(text="After fitting a linear regression model, the residuals are plotted against the fitted values as "
                  "shown. The plot most strongly suggests:",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 8.5, 5)],
             solution=[RESID_OPTS[kind][1], f"Answer: <b>{RESID_OPTS[kind][0]}</b>.",
                       "Other patterns: funnel → heteroscedasticity; curvature → missing non-linearity; "
                       "isolated point → outlier; random band → adequate fit."])


HAT_T = [
    ("H is symmetric (Hᵀ = H).", "Hᵀ = X((XᵀX)⁻¹)ᵀXᵀ = H since XᵀX is symmetric."),
    ("H is idempotent (H² = H).", "H² = X(XᵀX)⁻¹XᵀX(XᵀX)⁻¹Xᵀ = H."),
    ("trace(H) = p.", "trace(X(XᵀX)⁻¹Xᵀ) = trace((XᵀX)⁻¹XᵀX) = trace(I<sub>p</sub>) = p."),
    ("rank(H) = p.", "For an idempotent matrix rank = trace = p."),
    ("I − H is also symmetric and idempotent.", "(I−H)² = I − 2H + H² = I − H."),
    ("HX = X.", "X(XᵀX)⁻¹XᵀX = X — H leaves the column space of X unchanged."),
    ("Every eigenvalue of H is either 0 or 1.", "λ² = λ for an idempotent matrix."),
    ("The vector of fitted values is ŷ = Hy.", "ŷ = Xβ̂ = X(XᵀX)⁻¹Xᵀy."),
    ("The residual vector is e = (I − H)y.", "e = y − ŷ = (I − H)y."),
    ("Each diagonal element (leverage) satisfies 0 ≤ h<sub>ii</sub> ≤ 1.",
     "h<sub>ii</sub> = Σ<sub>j</sub>h<sub>ij</sub>² ≥ h<sub>ii</sub>² gives 0 ≤ h<sub>ii</sub> ≤ 1."),
    ("(I − H)X = 0, i.e. residuals are orthogonal to every column of X.", "Follows from HX = X."),
    ("The average leverage (1/n)Σh<sub>ii</sub> equals p/n.", "Σh<sub>ii</sub> = trace(H) = p."),
    ("If X contains a column of ones, each row of H sums to 1.", "H1 = 1 because 1 is in the column space of X."),
    ("Under Var(y) = σ²I, Var(e) = σ²(I − H).", "Var((I−H)y) = (I−H)σ²I(I−H)ᵀ = σ²(I−H)."),
]
HAT_F = [
    ("H is invertible.", "rank(H) = p &lt; n, so H is singular."),
    ("trace(H) = n.", "trace(H) = p."),
    ("rank(H) = n.", "rank(H) = p &lt; n."),
    ("H can have negative eigenvalues.", "Eigenvalues of a projection matrix are only 0 or 1."),
    ("H² = 2H.", "H is idempotent: H² = H."),
    ("Some leverage h<sub>ii</sub> can exceed 1.", "0 ≤ h<sub>ii</sub> ≤ 1 always."),
    ("H depends on the response vector y.", "H = X(XᵀX)⁻¹Xᵀ depends only on X."),
    ("Under Var(y) = σ²I, the residuals are uncorrelated with common variance σ².",
     "Var(e) = σ²(I − H), which is not diagonal in general."),
    ("trace(I − H) = p.", "trace(I − H) = n − p."),
    ("The residual vector is e = Hy.", "e = (I − H)y; Hy is the fitted vector."),
    ("H is an orthogonal matrix (HᵀH = I).", "HᵀH = H ≠ I since H is singular."),
    ("det(H) = 1.", "H is singular, so det(H) = 0."),
    ("ŷ = Hᵀ X y.", "ŷ = Hy; the expression HᵀXy is not even dimensionally valid in general."),
]


@template(TOPIC, S_MLR, marks=1, qtype="MSQ")
def hat_matrix_props(rng):
    opts, ans, expl = msq_from_statements(rng, HAT_T, HAT_F)
    return Q(text="Let X be an n × p design matrix of full column rank p (p &lt; n), and let "
                  "H = X(XᵀX)⁻¹Xᵀ be the hat matrix of least-squares regression of y on X. "
                  "Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


CATS = [("region", "North, South, East, West, Central, North-East"), ("season", "Winter, Summer, Monsoon, Autumn"),
        ("vehicle type", "Car, Bike, Bus, Truck, Auto"), ("education level", "School, UG, PG, PhD"),
        ("payment mode", "Cash, Card, UPI, Wallet, NetBanking"), ("day type", "Weekday, Saturday, Sunday")]


@template(TOPIC, S_MLR, marks=1, qtype="NAT")
def dummy_parameter_count(rng):
    m = int(rng.integers(1, 6))
    ci = rng.choice(len(CATS), int(rng.integers(1, 3)), replace=False)
    cats = []
    for i in ci:
        name, lv = CATS[i]
        lv = lv.split(", ")
        k = int(rng.integers(3, len(lv) + 1))
        cats.append((name, lv[:k]))
    desc = "; ".join(f"a categorical feature <i>{nm}</i> with {len(lv)} levels ({', '.join(lv)})" for nm, lv in cats)
    p = 1 + m + sum(len(lv) - 1 for _, lv in cats)
    v = int(rng.integers(3))
    stem = (f"A linear regression model with an intercept uses {m} numeric feature{'s' if m > 1 else ''} and {desc}. "
            "Each categorical feature is encoded by dummy (indicator) variables using a reference level, so that "
            "the design matrix has full column rank. ")
    sol = [f"A categorical feature with k levels needs k − 1 dummies (one level is the reference absorbed by the "
           "intercept; using all k dummies with an intercept gives perfect multicollinearity).",
           "Parameters = 1 (intercept) + " + f"{m} (numeric)" +
           "".join(f" + ({len(lv)} − 1)" for _, lv in cats) + f" = {p}."]
    if v == 0:
        ans = p
        q = "The total number of regression coefficients (including the intercept) to be estimated is"
    elif v == 1:
        nm, lv = cats[0]
        ans = p + len(lv) - 1
        q = (f"An interaction between the first numeric feature x<sub>1</sub> and <i>{nm}</i> is also added "
             f"(products of x<sub>1</sub> with each {nm} dummy). The total number of coefficients (including the "
             "intercept) is")
        sol.append(f"The interaction adds one product term per {nm} dummy: {len(lv)} − 1 = {len(lv) - 1}. "
                   f"Total = {p} + {len(lv) - 1} = {ans}.")
    else:
        n = int(rng.integers(3, 12)) * 10
        ans = n - p
        q = (f"The model is fitted to n = {n} observations. The residual degrees of freedom used in the unbiased "
             "estimate σ̂² = SSE/(degrees of freedom) is")
        sol.append(f"Residual degrees of freedom = n − (number of coefficients) = {n} − {p} = {ans}.")
    sol.append(f"Answer: <b>{ans}</b>.")
    return Q(text=stem + q + " _______ " + nat_hint(0), qtype="NAT", marks=1, answer=(ans, ans), nat_hint=nat_hint(0),
             solution=sol)


@template(TOPIC, S_MLR, marks=1, qtype="NAT")
def vif_multicollinearity(rng):
    v = int(rng.integers(4))
    sol = ["Variance inflation factor of predictor j: VIF<sub>j</sub> = 1/(1 − R<sub>j</sub>²), where "
           "R<sub>j</sub>² is the R² from regressing x<sub>j</sub> on all other predictors. It is the factor by which "
           "Var(β̂<sub>j</sub>) is inflated by collinearity; √VIF inflates the standard error."]
    if v == 0:
        r = float(rng.choice(np.arange(0.5, 0.96, 0.05)).round(2)) * rng.choice([-1, 1])
        ans = 1 / (1 - r * r)
        q = (f"In a regression with exactly two predictors x<sub>1</sub> and x<sub>2</sub>, the sample correlation "
             f"between them is {fmt(r)}. The variance inflation factor (VIF) of x<sub>1</sub> is")
        sol.append(f"With two predictors, R<sub>1</sub>² = r² = {fmt(r * r, 4)}, so VIF = 1/(1 − {fmt(r * r, 4)}) = "
                   f"{fmt(ans, 4)}.")
    elif v == 1:
        R2 = float(rng.choice(np.arange(0.55, 0.97, 0.01)).round(2))
        ans = 1 / (1 - R2)
        q = (f"Regressing predictor x<sub>3</sub> on all the other predictors gives R² = {fmt(R2)}. The VIF of "
             "x<sub>3</sub> is")
        sol.append(f"VIF = 1/(1 − {fmt(R2)}) = {fmt(ans, 4)}.")
    elif v == 2:
        R2 = float(rng.choice(np.arange(0.5, 0.97, 0.02)).round(2))
        ans = np.sqrt(1 / (1 - R2))
        q = (f"Regressing x<sub>2</sub> on the remaining predictors gives R² = {fmt(R2)}. By what factor is the "
             "standard error of β̂<sub>2</sub> inflated relative to the case of x<sub>2</sub> being uncorrelated "
             "with the other predictors?")
        sol.append(f"VIF = 1/(1 − {fmt(R2)}) = {fmt(1 / (1 - R2), 4)}; SE inflation = √VIF = {fmt(ans, 4)}.")
    else:
        vif = float(rng.choice([1.25, 2, 2.5, 4, 5, 6.25, 8, 10, 12.5, 16, 20, 25]))
        ans = 1 - 1 / vif
        q = (f"The VIF of a predictor x<sub>j</sub> is {fmt(vif)}. The R² obtained by regressing x<sub>j</sub> on "
             "the other predictors is")
        sol.append(f"R<sub>j</sub>² = 1 − 1/VIF = 1 − 1/{fmt(vif)} = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=q + " _______ " + nat_hint(2), qtype="NAT", marks=1, answer=_nat(ans, 2), nat_hint=nat_hint(2),
             solution=sol)


RIDGE_T = [
    ("Ridge regression has the closed-form solution β̂ = (XᵀX + λI)⁻¹Xᵀy.",
     "Setting the gradient of ‖y−Xβ‖² + λ‖β‖² to zero gives (XᵀX + λI)β = Xᵀy."),
    ("For λ &gt; 0, XᵀX + λI is invertible even when p &gt; n.",
     "XᵀX is PSD, so XᵀX + λI has eigenvalues ≥ λ &gt; 0."),
    ("As λ → ∞, all (penalised) ridge coefficients shrink towards 0.", "The penalty dominates the RSS."),
    ("The lasso can set some coefficients exactly to zero.",
     "The L1 ball has corners on the axes; the RSS contours often first touch it at a corner."),
    ("Increasing λ generally increases bias and decreases variance.", "Stronger shrinkage = less flexible fit."),
    ("Ridge regression with λ = 0 coincides with ordinary least squares.", "The penalty term vanishes."),
    ("The lasso constraint region Σ|β<sub>j</sub>| ≤ t in two dimensions is a diamond (square rotated by 45°).",
     "Its vertices lie on the coordinate axes."),
    ("Elastic net combines L1 and L2 penalties.", "Penalty λ<sub>1</sub>‖β‖<sub>1</sub> + λ<sub>2</sub>‖β‖²<sub>2</sub>."),
    ("Predictors are usually standardised before fitting ridge or lasso.",
     "The penalty treats all coefficients alike, so the solution depends on the scale of each predictor."),
    ("The intercept is usually not penalised in ridge regression.",
     "Penalising it would make the fit depend on the origin chosen for y."),
    ("The lasso objective ‖y − Xβ‖² + λ‖β‖<sub>1</sub> is convex in β.", "Sum of two convex functions."),
    ("With an orthonormal design (XᵀX = I), minimising ‖y − Xβ‖² + λ‖β‖² gives β̂<sub>OLS</sub>/(1 + λ).",
     "(I + λI)β = Xᵀy = β̂<sub>OLS</sub>."),
    ("With an orthonormal design, the lasso estimate is a soft-thresholded version of the OLS estimate.",
     "β̂<sub>j</sub> = sign(b<sub>j</sub>)(|b<sub>j</sub>| − c)<sub>+</sub> for a threshold c depending on λ."),
    ("The L1 penalty |β| is not differentiable at β = 0.", "Its subgradient at 0 is the interval [−1, 1]."),
    ("‖β̂<sub>ridge</sub>(λ)‖<sub>2</sub> is a non-increasing function of λ.",
     "Each component in the SVD basis is d<sub>j</sub>²/(d<sub>j</sub>²+λ) times the OLS component."),
    ("Ridge regression can be used to obtain a unique solution when predictors are perfectly collinear.",
     "XᵀX + λI is invertible for λ &gt; 0."),
]
RIDGE_F = [
    ("Ridge regression typically sets many coefficients exactly to zero.",
     "The L2 ball is smooth; ridge shrinks coefficients but rarely makes them exactly zero."),
    ("The lasso has a closed-form solution for a general design matrix X, just like ridge.",
     "In general it requires iterative methods (coordinate descent, LARS)."),
    ("Increasing λ decreases the bias of the ridge estimator.", "More shrinkage → more bias."),
    ("The ridge penalty is λΣ|β<sub>j</sub>|.", "That is the lasso (L1) penalty; ridge uses λΣβ<sub>j</sub>²."),
    ("The lasso penalty is λΣβ<sub>j</sub>².", "That is the ridge (L2) penalty."),
    ("Ridge solutions are invariant to rescaling the individual predictors.",
     "Rescaling x<sub>j</sub> changes how strongly β<sub>j</sub> is penalised."),
    ("The training error of ridge regression decreases as λ increases.",
     "λ = 0 (OLS) minimises training RSS; training error is non-decreasing in λ."),
    ("λ should be chosen to minimise the training error.", "That always picks λ = 0; use validation / CV."),
    ("The ridge constraint region Σβ<sub>j</sub>² ≤ t has sharp corners on the axes.", "It is a disc (ball)."),
    ("Ridge regression requires XᵀX to be invertible.", "XᵀX + λI is invertible for any λ &gt; 0."),
    ("As λ → ∞, the lasso coefficients grow without bound.", "They all become exactly 0 for large enough λ."),
    ("The ridge objective ‖y − Xβ‖² + λ‖β‖² (λ &gt; 0) is non-convex.", "It is strictly convex."),
    ("With an orthonormal design, the ridge estimate is β̂<sub>OLS</sub> − λ.", "It is β̂<sub>OLS</sub>/(1 + λ)."),
    ("For λ &gt; 0, ridge regression gives unbiased estimates of β.", "Shrinkage introduces bias."),
    ("Among a group of highly correlated relevant predictors, the lasso tends to keep all of them with similar "
     "coefficients.", "Lasso tends to pick one and zero the others; ridge spreads weight among them."),
]


@template(TOPIC, S_RIDGE, marks=1, qtype="MSQ")
def ridge_lasso_statements(rng):
    opts, ans, expl = msq_from_statements(rng, RIDGE_T, RIDGE_F)
    return Q(text="Consider ridge regression (minimise ‖y − Xβ‖² + λ‖β‖²<sub>2</sub>) and the lasso (minimise "
                  "‖y − Xβ‖² + λ‖β‖<sub>1</sub>) with λ ≥ 0. Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)


def _min_on_segment(A, b, P, Qp):
    d = Qp - P
    a2 = d @ A @ d
    a1 = 2 * d @ A @ (P - b)
    s = float(np.clip(-a1 / (2 * a2), 0, 1))
    pt = P + s * d
    return pt, (pt - b) @ A @ (pt - b)


@template(TOPIC, S_RIDGE, marks=1, qtype="MCQ")
def lasso_ridge_geometry(rng):
    while True:
        shape = "diamond" if rng.random() < 0.65 else "circle"
        b = rng.uniform(0.6, 2.6, 2) * rng.choice([-1, 1], 2)
        th = rng.uniform(0, np.pi)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        A = R @ np.diag([1.0, rng.uniform(1.8, 6)]) @ R.T
        if shape == "diamond":
            if np.abs(b).sum() < 1.6:
                continue
            V = [np.array(v, float) for v in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
            best = min((_min_on_segment(A, b, V[i], V[(i + 1) % 4]) for i in range(4)), key=lambda t: t[1])
            sol = best[0]
        else:
            if np.linalg.norm(b) < 1.5:
                continue
            ang = np.linspace(0, 2 * np.pi, 72001)
            pts = np.c_[np.cos(ang), np.sin(ang)]
            vals = np.einsum("ij,jk,ik->i", pts - b, A, pts - b)
            sol = pts[np.argmin(vals)]
        z = np.abs(sol) < 1e-7
        if not z.any() and np.abs(sol).min() < 0.18:
            continue
        break
    fstar = (sol - b) @ A @ (sol - b)
    if z[0] and not z[1]:
        key = 1
    elif z[1] and not z[0]:
        key = 2
    else:
        key = 0
    labels = ["β̂<sub>1</sub> ≠ 0 and β̂<sub>2</sub> ≠ 0 (both shrunk, neither exactly zero)",
              "β̂<sub>1</sub> = 0 exactly and β̂<sub>2</sub> ≠ 0",
              "β̂<sub>2</sub> = 0 exactly and β̂<sub>1</sub> ≠ 0",
              "β̂<sub>1</sub> = β̂<sub>2</sub> = 0"]
    L = max(np.abs(b).max() + 0.8, 1.6)

    def draw(fig):
        ax = fig.add_subplot(111)
        if shape == "diamond":
            ax.fill([1, 0, -1, 0], [0, 1, 0, -1], color="#cfcfcf", ec="k", lw=1)
        else:
            t = np.linspace(0, 2 * np.pi, 200)
            ax.fill(np.cos(t), np.sin(t), color="#cfcfcf", ec="k", lw=1)
        g = np.linspace(-L, L, 300)
        G1, G2 = np.meshgrid(g, g)
        D1, D2 = G1 - b[0], G2 - b[1]
        F = A[0, 0] * D1 ** 2 + 2 * A[0, 1] * D1 * D2 + A[1, 1] * D2 ** 2
        ax.contour(G1, G2, F, levels=sorted({fstar * s for s in (0.12, 0.4, 1.0, 1.9)}), colors=C1, linewidths=0.9)
        ax.plot(*b, "o", color=C2)
        ax.annotate("β̂ (OLS)", b, textcoords="offset points", xytext=(5, 5), fontsize=7)
        ax.axhline(0, color=C4, lw=0.7)
        ax.axvline(0, color=C4, lw=0.7)
        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        ax.set_aspect("equal")
        ax.set_xlabel("β₁")
        ax.set_ylabel("β₂")

    opts, a = mcq(rng, labels[key], [lab for i, lab in enumerate(labels) if i != key])
    pen = "lasso (L1: |β₁| + |β₂| ≤ t, a diamond)" if shape == "diamond" else "ridge (L2: β₁² + β₂² ≤ t², a disc)"
    sol = [f"The shaded region is the constraint set of the {pen}. The penalised estimate is the first point at which "
           "the RSS contours (ellipses centred at β̂<sub>OLS</sub>, which lies outside the region) touch the region.",
           f"From the figure the tangency point is approximately ({fmt(sol[0])}, {fmt(sol[1])})."]
    if key == 0:
        sol.append("The contour touches the boundary at a point that is not on an axis, so both coefficients are "
                   "non-zero. " + ("For the disc this is the generic case — ridge shrinks but does not zero out."
                                   if shape == "circle" else "Here the lasso tangency is on an edge of the diamond."))
    else:
        sol.append(f"The contour first touches the diamond at a corner on the β<sub>{3 - key}</sub>-axis, so "
                   f"β̂<sub>{key}</sub> = 0 exactly — this is why the lasso performs variable selection.")
    sol.append(f"Answer: <b>{labels[key]}</b>. Both coefficients cannot be zero since the OLS point lies outside the "
               "region (the constraint is active but t &gt; 0).")
    return Q(text="For a two-predictor penalised least-squares problem, the figure shows the constraint region "
                  "(shaded) of the penalty together with elliptical contours of the residual sum of squares centred "
                  "at the least-squares estimate β̂ (OLS). The penalised estimate (β̂<sub>1</sub>, β̂<sub>2</sub>) satisfies",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 7.5, 6.5)], solution=sol)


BV_T = [
    ("Expected test MSE at a point x<sub>0</sub> = Bias² + Variance + irreducible noise variance σ².",
     "Standard decomposition of E[(y<sub>0</sub> − f̂(x<sub>0</sub>))²]."),
    ("Increasing model flexibility typically decreases bias.", "Flexible models can approximate the true f better."),
    ("Increasing model flexibility typically increases variance.", "Flexible fits change more with the training sample."),
    ("The irreducible error cannot be reduced by choosing a better model.", "It is the variance of the noise ε."),
    ("For nested least-squares polynomial fits, training MSE never increases as the degree increases.",
     "A higher-degree model contains the lower-degree one as a special case."),
    ("Test error plotted against flexibility is typically U-shaped.", "Bias falls, variance rises."),
    ("High and similar training and test errors indicate underfitting (high bias).", "The model is too simple."),
    ("Very low training error with much higher test error indicates overfitting (high variance).",
     "The model fits noise in the training set."),
    ("For a fixed model class, more training data tends to reduce variance.", "Estimates stabilise as n grows."),
    ("k-NN regression with k = 1 has low bias and high variance.", "It reproduces each training point."),
    ("Averaging many (approximately) independent unbiased estimators reduces variance.", "Var of mean = σ²/B."),
    ("Regularisation trades a small increase in bias for a reduction in variance.", "Shrinkage stabilises estimates."),
    ("A predictor that outputs a fixed constant regardless of the training data has zero variance.",
     "Its prediction does not change across training sets."),
    ("The bias of f̂ at x<sub>0</sub> is E[f̂(x<sub>0</sub>)] − f(x<sub>0</sub>), the expectation being over training sets.",
     "Definition of bias."),
]
BV_F = [
    ("The irreducible error decreases as model complexity increases.", "It depends only on the noise, not the model."),
    ("Variance decreases as model complexity increases.", "Variance typically increases with complexity."),
    ("Training error is an unbiased estimate of test error.", "Training error is optimistically biased (too low)."),
    ("Overfitting models have high bias and low variance.", "Overfitting = low bias, high variance."),
    ("Expected test MSE = Bias + Variance + noise (bias not squared).", "It is the squared bias that appears."),
    ("Increasing k in k-NN regression increases its variance.", "Larger k averages more points → lower variance."),
    ("Test error always decreases as the polynomial degree increases.", "Beyond some degree it rises (overfitting)."),
    ("A model with zero training error must have zero test error.", "It may have badly overfit."),
    ("Underfitting is characterised by low training error and high test error.",
     "That describes overfitting; underfitting has high training error."),
    ("Regularisation reduces the bias of a model.", "It increases bias, reduces variance."),
    ("Ridge regression with a larger λ has higher variance.", "Larger λ → lower variance."),
    ("The squared bias term can be negative when the model overestimates f.", "A square is non-negative."),
    ("Adding more training data increases the variance of a fixed model class.", "More data reduces variance."),
    ("A 1-NN regressor has higher bias than a 50-NN regressor on the same data.",
     "1-NN is the most flexible: lower bias, higher variance."),
]


@template(TOPIC, S_BV, marks=1, qtype="MSQ")
def bias_variance_statements(rng):
    opts, ans, expl = msq_from_statements(rng, BV_T, BV_F)
    return Q(text="Regarding the bias–variance trade-off in supervised regression with squared-error loss, which of "
                  "the following statements is/are CORRECT?", qtype="MSQ", marks=1, options=opts, answer=ans,
             solution=expl)


@template(TOPIC, S_BV, marks=1, qtype="MCQ")
def bv_curve_points(rng):
    tau = rng.uniform(1.4, 2.4)
    v = rng.uniform(0.012, 0.03)
    c = np.linspace(1, 10, 400)
    train = 1.1 * np.exp(-(c - 1) / tau) + 0.04 + 0.06 * np.exp(-(c - 1) / 6)
    test = 1.15 * np.exp(-(c - 1) / tau) + v * (c - 1) ** 2 + 0.3
    cmin = float(c[np.argmin(test)])
    under = max(1.3, cmin - rng.uniform(2.0, 3.0))
    over = min(9.7, cmin + rng.uniform(2.5, 4.0))
    pos = {"under": under, "best": cmin, "over": over}
    names = ["P", "Q", "R"]
    perm = rng.permutation(3)
    assign = dict(zip(["under", "best", "over"], [names[i] for i in perm]))
    v_ = int(rng.integers(3))
    want = ["over", "under", "best"][v_]
    ask = ["overfitting (low bias, high variance)", "underfitting (high bias, low variance)",
           "the best generalisation (lowest expected test error)"][v_]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(c, train, color=C1, lw=1.5, label="training error")
        ax.plot(c, test, color=C2, lw=1.5, ls="--", label="test error")
        for k, xv in pos.items():
            ax.axvline(xv, color=C4, lw=0.8, ls=":")
            ax.text(xv, test.max() * 1.03, assign[k], ha="center", fontsize=8,
                    fontweight="bold")
        ax.set_xlabel("model complexity (flexibility)")
        ax.set_ylabel("error")
        ax.set_yticks([])
        ax.set_xticks([])
        ax.legend(loc="upper center", ncol=2, frameon=False)
        ax.set_ylim(0, test.max() * 1.32)

    correct = assign[want]
    opts, a = mcq(rng, correct, [x for x in names if x != correct] + ["None of P, Q, R"])
    expl = {"under": "both training and test errors are high (left side)",
            "best": "the test error is at its minimum",
            "over": "training error is very low but test error has risen well above its minimum (right side)"}
    return Q(text="The figure shows training and test error as a function of model complexity, with three "
                  f"complexity levels marked P, Q and R. Which marked level corresponds to {ask}?",
             qtype="MCQ", marks=1, options=opts, answer=a, blocks=[Figure(draw, 8.5, 5.2)],
             solution=[f"At {assign['under']}: {expl['under']} → underfitting.",
                       f"At {assign['best']}: {expl['best']} → best trade-off.",
                       f"At {assign['over']}: {expl['over']} → overfitting.",
                       f"Answer: <b>{correct}</b>."])


@template(TOPIC, S_CV, marks=1, qtype="NAT")
def cv_model_fits(rng):
    v = int(rng.integers(5))
    if v == 0:
        k = int(rng.choice([3, 4, 5, 10]))
        G = int(rng.integers(3, 9))
        ans = k * G + 1
        q = (f"A regularisation parameter is tuned over {G} candidate values using {k}-fold cross-validation. After "
             "selecting the best value, the model is refitted once on the full training data. The total number of "
             "times the model is fitted is")
        sol = [f"Each candidate needs k = {k} fits: {G} × {k} = {G * k}. Plus 1 final refit: <b>{ans}</b>."]
    elif v == 1:
        n = int(rng.integers(12, 61))
        G = int(rng.integers(2, 6))
        ans = n * G
        q = (f"A data set has n = {n} observations. Leave-one-out cross-validation is used to compare {G} candidate "
             "models (no final refit is counted). The total number of model fits is")
        sol = [f"LOOCV = n-fold CV: {n} fits per model × {G} models = <b>{ans}</b>."]
    elif v == 2:
        K = int(rng.choice([3, 5, 10]))
        k = int(rng.choice([3, 4, 5]))
        G = int(rng.integers(2, 7))
        ans = K * (k * G + 1)
        q = (f"Nested cross-validation is performed with an outer {K}-fold loop and an inner {k}-fold loop. In each "
             f"outer fold, the inner loop evaluates {G} hyperparameter values, after which the model with the best "
             "value is refitted once on that outer fold's training part and evaluated on its test part. The total "
             "number of model fits (no further refit at the end) is")
        sol = [f"Per outer fold: inner CV {G} × {k} = {G * k} fits + 1 refit = {G * k + 1}.",
               f"Total = {K} × {G * k + 1} = <b>{ans}</b>."]
    elif v == 3:
        r = int(rng.integers(2, 6))
        k = int(rng.choice([5, 10]))
        G = int(rng.integers(2, 6))
        ans = r * k * G
        q = (f"Repeated {k}-fold cross-validation with {r} repetitions (different random partitions) is used to "
             f"compare {G} models. Ignoring any final refit, the number of model fits is")
        sol = [f"{r} repetitions × {k} folds × {G} models = <b>{ans}</b>."]
    else:
        k = int(rng.choice([4, 5, 6, 8, 10]))
        n = k * int(rng.integers(6, 40))
        ans = n * (k - 1) // k
        q = (f"A data set of n = {n} observations is split into {k} equal folds for {k}-fold cross-validation. The "
             "number of observations used to train the model in each fold is")
        sol = [f"Each fold holds out n/k = {n // k} points, so training uses n − n/k = {n} − {n // k} = <b>{ans}</b>."]
    return Q(text=q + " _______ " + nat_hint(0), qtype="NAT", marks=1, answer=(ans, ans), nat_hint=nat_hint(0),
             solution=sol)


CV_T = [
    ("LOOCV is k-fold cross-validation with k = n.", "Each fold contains a single observation."),
    ("The LOOCV estimate involves no randomness in the choice of splits.", "There is exactly one way to leave one out."),
    ("LOOCV estimates of test error have low bias but can have relatively high variance.",
     "The n training sets overlap almost completely, so the fold errors are highly correlated."),
    ("Stratified k-fold CV keeps the class proportions in each fold close to those of the full data.",
     "That is its purpose for classification."),
    ("Standardisation parameters (mean, s.d.) should be computed only from the training folds.",
     "Using validation data to compute them leaks information."),
    ("Selecting features on the full data set and then cross-validating the selected model gives an optimistic "
     "error estimate.", "Classic data leakage — the selection already saw the validation folds."),
    ("Nested CV gives a nearly unbiased estimate of generalisation error when hyperparameters are tuned by CV.",
     "The outer loop evaluates the whole tuning procedure on untouched data."),
    ("For time-series data, validation folds should come after the training data in time.",
     "Otherwise the model is trained on the future."),
    ("In k-fold CV every observation is used for validation exactly once.", "Folds partition the data."),
    ("For least-squares linear regression, LOOCV error can be computed from a single fit using the leverages h<sub>ii</sub>.",
     "CV<sub>(n)</sub> = (1/n)Σ(e<sub>i</sub>/(1 − h<sub>ii</sub>))²."),
    ("A single train/validation split gives an error estimate that can vary substantially with the split.",
     "That is why k-fold CV averages over several splits."),
    ("k-fold CV of a single model configuration requires k model fits.", "One fit per held-out fold."),
    ("Compared with 2-fold CV, 10-fold CV uses larger training sets in each fit.", "90% vs 50% of the data."),
]
CV_F = [
    ("For any learning algorithm, LOOCV can be computed from a single model fit.",
     "The shortcut holds for linear smoothers such as least squares, not in general."),
    ("In k-fold CV each observation is used for validation k times.", "Each observation is validated exactly once."),
    ("2-fold CV gives a less (pessimistically) biased estimate of test error than LOOCV.",
     "2-fold trains on only half the data, so its estimate is more pessimistically biased."),
    ("Standardising the whole data set before splitting into folds causes no information leakage.",
     "Validation-fold statistics influence the training transformation."),
    ("The minimum CV error over many candidate models is an unbiased estimate of the chosen model's test error.",
     "Selecting the minimum makes it optimistically biased; use a separate test set or nested CV."),
    ("LOOCV on n observations requires n² model fits.", "It requires n fits."),
    ("Randomly shuffling a time series before k-fold CV is the recommended practice.", "It leaks future information."),
    ("Increasing k in k-fold CV reduces the computational cost.", "More folds → more fits, each on more data."),
    ("The test set should be used to choose the hyperparameters.", "Then test error is no longer an unbiased estimate."),
    ("In k-fold CV, the training sets of different folds are disjoint.", "They overlap heavily (for k ≥ 3)."),
    ("The k-fold CV estimate does not depend on how the data are partitioned into folds.",
     "Different random partitions give different estimates."),
    ("In nested CV, the inner loop estimates generalisation error and the outer loop tunes hyperparameters.",
     "It is the reverse: inner loop tunes, outer loop estimates performance."),
    ("Stratified CV is needed to make all folds have exactly equal size.", "Stratification is about class proportions."),
]


@template(TOPIC, S_CV, marks=1, qtype="MSQ")
def cv_statements(rng):
    opts, ans, expl = msq_from_statements(rng, CV_T, CV_F)
    return Q(text="Which of the following statements about cross-validation (CV) is/are CORRECT? "
                  "(n denotes the number of observations.)", qtype="MSQ", marks=1, options=opts, answer=ans,
             solution=expl)


ETA_SETS = [(0.02, 0.08, 0.3, 1.15), (0.01, 0.05, 0.25, 1.2), (0.03, 0.1, 0.35, 1.1), (0.02, 0.06, 0.2, 1.25),
            (0.04, 0.12, 0.4, 1.1), (0.01, 0.04, 0.15, 1.3)]


@template(TOPIC, S_GD, marks=1, qtype="MCQ")
def gd_learning_rate_curves(rng):
    etas = list(ETA_SETS[int(rng.integers(len(ETA_SETS)))])
    a = int(rng.integers(2, 6))
    w0 = float(a + rng.choice([-4, -3, 3, 4]))
    T = 25
    curves = []
    for eta in etas:
        w = w0
        Js = []
        for _ in range(T + 1):
            Js.append((w - a) ** 2)
            w = w - eta * 2 * (w - a)
        curves.append(np.array(Js))
    labs = ["A", "B", "C", "D"]
    perm = rng.permutation(4)
    lab_of = {i: labs[perm[i]] for i in range(4)}
    styles = ["-", "--", "-.", ":"]
    target = int(rng.integers(4))
    J0 = curves[0][0]

    def draw(fig):
        ax = fig.add_subplot(111)
        for i in range(4):
            ax.plot(range(T + 1), curves[i], styles[perm[i]], color=[C1, C2, C3, "k"][perm[i]], lw=1.4,
                    marker="os^d"[perm[i]], ms=2.8, markevery=3, label=f"curve {lab_of[i]}")
        ax.set_ylim(0, J0 * 1.4)
        ax.set_xlabel("iteration t")
        ax.set_ylabel("$J(w_t)$")
        handles, lbls = ax.get_legend_handles_labels()
        order = np.argsort(lbls)
        ax.legend([handles[j] for j in order], [lbls[j] for j in order], frameon=False, fontsize=7)
        ax.grid(alpha=.3)

    correct = f"Curve {lab_of[target]}"
    opts, ans = mcq(rng, correct, [f"Curve {x}" for x in labs if x != lab_of[target]])
    rates = ", ".join(fmt(e, 2) for e in etas)
    sol = [f"J(w) = (w − {a})² has J″ = 2. GD: w<sub>t+1</sub> − {a} = (1 − 2η)(w<sub>t</sub> − {a}), so "
           "J(w<sub>t</sub>) = (1 − 2η)<super>2t</super> J(w<sub>0</sub>).",
           "Ratios (1 − 2η)² per step: " + "; ".join(
               f"η = {fmt(e, 2)} → {fmt((1 - 2 * e) ** 2, 4)} (curve {lab_of[i]})" for i, e in enumerate(etas)) + ".",
           "Ratio &gt; 1 ⇒ divergence (η &gt; 1 = 2/J″); among convergent rates (all &lt; 0.5 here), a smaller η "
           "gives a ratio closer to 1, i.e. slower decrease.",
           f"Hence η = {fmt(etas[target], 2)} corresponds to <b>{correct}</b>."]
    return Q(text=f"Gradient descent w<sub>t+1</sub> = w<sub>t</sub> − η J′(w<sub>t</sub>) is run on J(w) = (w − {a})² "
                  f"from w<sub>0</sub> = {fmt(w0)} with four learning rates η ∈ {{{rates}}}. The loss curves are "
                  f"shown below (curves that leave the plotted range are cut off). Which curve corresponds to "
                  f"η = {fmt(etas[target], 2)}?",
             qtype="MCQ", marks=1, options=opts, answer=ans, blocks=[Figure(draw, 8.5, 5.2)], solution=sol)


GD_T = [
    ("The MSE loss of linear regression, J(w) = (1/n)‖Xw − y‖², is a convex function of w.",
     "Its Hessian (2/n)XᵀX is positive semidefinite."),
    ("With a sufficiently small constant learning rate, batch gradient descent on the least-squares loss converges "
     "to a global minimiser.", "Convex quadratic with Lipschitz gradient; η &lt; 2/λ<sub>max</sub>(Hessian) suffices."),
    ("Stochastic gradient descent updates the parameters using the gradient on one (or a few) randomly chosen "
     "example(s).", "Definition of SGD / mini-batch GD."),
    ("With uniform random sampling, the mini-batch gradient is an unbiased estimate of the full-batch gradient.",
     "Its expectation equals the average gradient over all examples."),
    ("Standardising features usually speeds up gradient descent for linear regression.",
     "It reduces the condition number of XᵀX, making contours rounder."),
    ("Solving the normal equations costs about O(p³) for the p × p system, which becomes expensive for very large p.",
     "Matrix factorisation/inversion is cubic in p."),
    ("If the learning rate is too large, gradient descent on the MSE loss can diverge.", "When η &gt; 2/λ<sub>max</sub>."),
    ("For J(w) = (1/n)‖Xw − y‖², the gradient descent update is w ← w − η(2/n)Xᵀ(Xw − y).", "∇J = (2/n)Xᵀ(Xw − y)."),
    ("With a constant learning rate, SGD iterates typically keep fluctuating in a neighbourhood of the minimiser.",
     "Gradient noise does not vanish; decaying step sizes are needed for exact convergence."),
    ("The Hessian of ‖Xw − y‖² is 2XᵀX.", "Differentiate 2Xᵀ(Xw − y) once more."),
    ("One epoch of SGD with batch size 1 on n examples performs n parameter updates.", "One update per example."),
    ("Batch gradient descent and the normal equations converge to the same minimiser when XᵀX is invertible.",
     "The least-squares minimiser is unique in that case."),
]
GD_F = [
    ("The MSE loss of linear regression can have local minima that are not global minima.",
     "It is convex; every local minimum is global."),
    ("Gradient descent on the MSE loss converges for every learning rate η &gt; 0.", "It diverges if η is too large."),
    ("SGD computes the exact full-data gradient at every step.", "It uses a noisy estimate from a sample."),
    ("Solving the normal equations requires choosing a learning rate.", "It is a direct (closed-form) solve."),
    ("Standardising features changes the minimum training MSE achievable by OLS with an intercept.",
     "Affine rescaling of features does not change the span of the design, hence not the fitted values."),
    ("Batch gradient descent performs one parameter update per training example in each epoch.",
     "Batch GD makes one update per pass over the data."),
    ("A larger learning rate always gives faster convergence.", "Beyond 2/λ<sub>max</sub> it diverges."),
    ("With uniform random sampling, the mini-batch gradient is a biased estimate of the full gradient.",
     "It is unbiased."),
    ("To minimise the loss, gradient descent updates w ← w + η∇J(w).", "That is gradient ascent."),
    ("For linear regression, gradient descent can reach a strictly lower training MSE than the normal-equation solution.",
     "The normal-equation solution is the global minimiser."),
    ("The gradient of ‖Xw − y‖² with respect to w is 2X(Xw − y).",
     "Dimensions do not match; the gradient is 2Xᵀ(Xw − y)."),
]


@template(TOPIC, S_GD, marks=1, qtype="MSQ")
def gd_statements(rng):
    opts, ans, expl = msq_from_statements(rng, GD_T, GD_F)
    return Q(text="Linear regression is trained by minimising the squared-error loss. Which of the following "
                  "statements about gradient-based training is/are CORRECT?", qtype="MSQ", marks=1, options=opts,
             answer=ans, solution=expl)


MLE_ITEMS = [
    ("Assume y<sub>i</sub> = wᵀx<sub>i</sub> + ε<sub>i</sub> with ε<sub>i</sub> i.i.d. N(0, σ²). The maximum-likelihood "
     "estimate of w is obtained by minimising",
     "Σ(y<sub>i</sub> − wᵀx<sub>i</sub>)²",
     ["Σ|y<sub>i</sub> − wᵀx<sub>i</sub>|", "Σ(y<sub>i</sub> − wᵀx<sub>i</sub>)² + λ‖w‖²",
      "max<sub>i</sub> |y<sub>i</sub> − wᵀx<sub>i</sub>|", "Σ(y<sub>i</sub> − wᵀx<sub>i</sub>)⁴"],
     "−log L = (n/2)log(2πσ²) + (1/2σ²)Σ(y<sub>i</sub> − wᵀx<sub>i</sub>)²; only the sum of squares depends on w."),
    ("With Gaussian noise N(0, σ²) and prior w ~ N(0, τ²I), the MAP estimate of w equals",
     "ridge regression with λ = σ²/τ²",
     ["lasso with λ = σ²/τ²", "ridge regression with λ = τ²/σ²", "ordinary least squares (the prior has no effect)",
      "ridge regression with λ = στ"],
     "−log posterior ∝ (1/2σ²)‖y − Xw‖² + (1/2τ²)‖w‖²; multiplying by 2σ² gives ‖y − Xw‖² + (σ²/τ²)‖w‖²."),
    ("With Gaussian noise and independent Laplace (double-exponential) priors on each w<sub>j</sub>, the MAP estimate "
     "corresponds to",
     "lasso (L1-penalised least squares)",
     ["ridge (L2-penalised least squares)", "ordinary least squares", "least absolute deviation regression",
      "principal component regression"],
     "−log Laplace prior ∝ Σ|w<sub>j</sub>|/b, an L1 penalty."),
    ("If the noise in y = wᵀx + ε is Laplace distributed (instead of Gaussian), the MLE of w minimises",
     "Σ|y<sub>i</sub> − wᵀx<sub>i</sub>|",
     ["Σ(y<sub>i</sub> − wᵀx<sub>i</sub>)²", "Σ log(1 + e<super>−y<sub>i</sub>wᵀx<sub>i</sub></super>)",
      "Σ max(0, 1 − y<sub>i</sub>wᵀx<sub>i</sub>)", "‖w‖<sub>1</sub>"],
     "Laplace density ∝ exp(−|ε|/b); −log-likelihood ∝ Σ|residual|."),
    ("For the Gaussian prior w ~ N(0, τ²I) and Gaussian noise, as τ² → ∞ the MAP estimate tends to",
     "the least-squares (ML) estimate",
     ["the zero vector", "the lasso estimate", "a vector with all components equal", "an undefined limit"],
     "λ = σ²/τ² → 0, so the penalty disappears."),
    ("For the Gaussian prior w ~ N(0, τ²I) and Gaussian noise, as τ² → 0 the MAP estimate tends to",
     "the zero vector",
     ["the least-squares (ML) estimate", "the lasso estimate", "a vector whose norm grows without bound",
      "Xᵀy"],
     "λ = σ²/τ² → ∞, so all weights are shrunk to the prior mean 0."),
    ("In Gaussian linear regression with n observations and p coefficients (fitted by least squares), the "
     "maximum-likelihood estimate of σ² is",
     "SSE/n",
     ["SSE/(n − p)", "SSE/(n − 1)", "√(SSE/n)", "SSE/p"],
     "Maximising over σ² gives σ̂² = (1/n)Σe<sub>i</sub>²; SSE/(n − p) is the unbiased estimate."),
    ("In Gaussian linear regression with n observations and p coefficients, an unbiased estimator of σ² is",
     "SSE/(n − p)",
     ["SSE/n", "SSE/(n + p)", "SSE/p", "√(SSE/(n − p))"],
     "E[SSE] = σ²(n − p) because the residuals live in an (n − p)-dimensional space."),
    ("For Gaussian noise variance σ² and Gaussian prior N(0, τ²I) on w, increasing σ² (with τ² fixed) makes the "
     "equivalent ridge penalty λ",
     "increase",
     ["decrease", "remain unchanged", "become negative", "equal τ²"],
     "λ = σ²/τ²: noisier data → rely more on the prior."),
]


@template(TOPIC, S_MLE, marks=1, qtype="MCQ")
def mle_map_concepts(rng):
    stem, c, ds, ex = MLE_ITEMS[int(rng.integers(len(MLE_ITEMS)))]
    opts, a = mcq(rng, c, ds)
    return Q(text=stem + ":", qtype="MCQ", marks=1, options=opts, answer=a, solution=[ex, f"Answer: <b>{c}</b>."])


@template(TOPIC, S_POLY, marks=1, qtype="NAT")
def poly_feature_count(rng):
    p = int(rng.integers(2, 6))
    d = int(rng.integers(2, 4)) if p > 3 else int(rng.integers(2, 5))
    v = int(rng.integers(3))
    tot = comb(p + d, d)
    if v == 0:
        ans = tot
        q = (f"A full polynomial regression of degree {d} in {p} input variables x<sub>1</sub>, …, x<sub>{p}</sub> "
             f"includes every monomial in these variables of total degree at most {d} (including the constant term "
             f"and all interaction terms). The number of regression coefficients is")
        sol = [f"Number of monomials of degree ≤ d in p variables = C(p + d, d) = C({p + d}, {d}) = <b>{ans}</b>."]
    elif v == 1:
        ans = tot - 1
        q = (f"Polynomial feature expansion of degree {d} is applied to {p} input variables (all monomials of total "
             f"degree 1 to {d}, including interaction terms, but excluding the constant). The number of generated "
             "features is")
        sol = [f"All monomials of degree ≤ {d}: C({p + d}, {d}) = {tot}; excluding the constant: <b>{ans}</b>."]
    else:
        ans = comb(p + d - 1, d)
        q = (f"How many distinct monomials of total degree <b>exactly</b> {d} can be formed from {p} variables "
             f"(e.g. for p = 2, d = 2: x<sub>1</sub>², x<sub>1</sub>x<sub>2</sub>, x<sub>2</sub>²)?")
        sol = [f"Multisets of size d from p variables: C(p + d − 1, d) = C({p + d - 1}, {d}) = <b>{ans}</b>."]
    return Q(text=q + " _______ " + nat_hint(0), qtype="NAT", marks=1, answer=(ans, ans), nat_hint=nat_hint(0),
             solution=sol)


SC_T = [
    ("For OLS with an intercept, rescaling a feature as x′ = ax + b (a ≠ 0) leaves the fitted values unchanged.",
     "The column space of [1, x] is unchanged; only the coefficients adjust."),
    ("Ridge and lasso solutions depend on the scales of the features.", "The penalty is not scale-invariant."),
    ("k-NN regression predictions can change if one feature is rescaled.", "Distances change."),
    ("Polynomial regression y = w<sub>0</sub> + w<sub>1</sub>x + w<sub>2</sub>x² is linear in the parameters, so it can "
     "be fitted by ordinary least squares.", "Treat 1, x, x² as columns of the design matrix."),
    ("For least-squares polynomial fits on the same data, increasing the degree never increases the training RSS.",
     "Nested models."),
    ("High-degree polynomial features can make XᵀX badly ill-conditioned; centring/scaling x helps numerically.",
     "Powers of large x differ by orders of magnitude and are highly correlated."),
    ("Gaussian radial basis functions φ<sub>j</sub>(x) = exp(−(x − μ<sub>j</sub>)²/(2s²)) can be used in a model that "
     "is linear in its weights.", "y = Σw<sub>j</sub>φ<sub>j</sub>(x) is linear in w."),
    ("z-score standardisation z = (x − x̄)/s gives the feature sample mean 0 and sample standard deviation 1.",
     "By construction."),
    ("If all features are centred to mean zero, the OLS intercept equals ȳ.", "β̂<sub>0</sub> = ȳ − Σβ̂<sub>j</sub>x̄<sub>j</sub> = ȳ."),
    ("Gradient descent for linear regression usually converges faster when features are on comparable scales.",
     "Better conditioned Hessian."),
    ("Min–max scaling maps the training values of a feature onto [0, 1].", "(x − min)/(max − min)."),
    ("With n distinct x values, a polynomial of degree n − 1 can fit the n training points exactly.",
     "Lagrange interpolation; training RSS = 0."),
]
SC_F = [
    ("Polynomial regression is non-linear in its parameters and therefore cannot be solved with the normal equations.",
     "It is linear in the parameters."),
    ("Multiplying a feature by 10 changes the OLS predictions (model with intercept).",
     "The coefficient simply becomes one-tenth; predictions are unchanged."),
    ("Ridge regression solutions are invariant to rescaling individual features.", "They are not."),
    ("Decision-tree splits are strongly affected by monotone rescaling of a feature.",
     "Trees depend only on the ordering of feature values."),
    ("With n distinct x values, a polynomial of degree n − 1 cannot in general pass through all n points.",
     "It can (interpolation)."),
    ("Standardising two features changes the correlation between them.", "Correlation is invariant to affine maps."),
    ("Min–max scaling is robust to outliers.", "A single extreme value compresses all others."),
    ("Test data should be standardised with the test set's own mean and standard deviation.",
     "Use the training statistics."),
    ("Adding x² as an extra feature makes the least-squares objective non-convex.",
     "It remains a convex quadratic in the weights."),
    ("Increasing the polynomial degree always reduces test error.", "It eventually overfits."),
    ("If a feature measured in metres is converted to centimetres, its OLS coefficient is unchanged.",
     "x is multiplied by 100, so the coefficient is divided by 100."),
]


@template(TOPIC, S_POLY, marks=1, qtype="MSQ")
def scaling_basis_statements(rng):
    opts, ans, expl = msq_from_statements(rng, SC_T, SC_F)
    return Q(text="Which of the following statements about basis-function (polynomial) regression and feature "
                  "scaling is/are CORRECT?", qtype="MSQ", marks=1, options=opts, answer=ans, solution=expl)



# ============================================================================
# 2-MARK TEMPLATES
# ============================================================================
@template(TOPIC, S_SLR, marks=2, qtype="NAT")
def slr_fit_from_data(rng):
    x, y, f = _slr_data(rng)
    n = len(x)
    v = int(rng.integers(6))
    sol = _ols_solution_lines(x, y, f)
    if v == 0:
        ans, q, d = f["b1"], "the slope β̂<sub>1</sub> of the least-squares line ŷ = β̂<sub>0</sub> + β̂<sub>1</sub>x is", 2
    elif v == 1:
        ans, q, d = f["b0"], "the intercept β̂<sub>0</sub> of the least-squares line ŷ = β̂<sub>0</sub> + β̂<sub>1</sub>x is", 2
    elif v == 2:
        cand = [c for c in range(int(x.min()), int(x.max()) + 3) if c not in x]
        x0 = int(rng.choice(cand))
        ans, d = f["b0"] + f["b1"] * x0, 2
        q = f"the value predicted by the least-squares line at x = {x0} is"
        sol.append(f"ŷ({x0}) = {fmt(f['b0'], 4)} + ({fmt(f['b1'], 4)})({x0}) = {fmt(ans, 4)}.")
    elif v == 3:
        i = int(rng.integers(n))
        ans, d = f["e"][i], 2
        q = (f"the residual e = y − ŷ of the observation (x, y) = ({fmt(x[i])}, {fmt(y[i])}) under the least-squares "
             "line is")
        sol.append(f"ŷ = {fmt(f['b0'], 4)} + ({fmt(f['b1'], 4)})({fmt(x[i])}) = {fmt(f['yh'][i], 4)}; "
                   f"e = {fmt(y[i])} − {fmt(f['yh'][i], 4)} = {fmt(ans, 4)}.")
    elif v == 4:
        ans, d = f["r2"], 3
        q = "the coefficient of determination R² of the least-squares fit is"
        sol.append(f"S<sub>yy</sub> = SST = {fmt(f['sst'], 4)}; SSR = β̂<sub>1</sub>S<sub>xy</sub> = {fmt(f['ssr'], 4)}.")
        sol.append(f"R² = SSR/SST = S<sub>xy</sub>²/(S<sub>xx</sub>S<sub>yy</sub>) = {fmt(ans, 4)}.")
    else:
        ans, d = f["sse"], 2
        q = "the residual sum of squares SSE = Σ(y<sub>i</sub> − ŷ<sub>i</sub>)² of the least-squares fit is"
        sol.append(f"SST = S<sub>yy</sub> = {fmt(f['sst'], 4)}; SSE = S<sub>yy</sub> − S<sub>xy</sub>²/S<sub>xx</sub> "
                   f"= {fmt(f['sst'], 4)} − {fmt(f['ssr'], 4)} = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, d)}</b>.")
    return Q(text=f"The {n} observations shown in the table are plotted below. For the simple linear regression of y on "
                  f"x (with intercept), {q} _______ {nat_hint(d)}",
             qtype="NAT", marks=2, answer=_nat(ans, d, base=2 * 10 ** (-d) if d == 2 else 0.003),
             nat_hint=nat_hint(d), blocks=[_xy_table(x, y), Figure(_scatter(x, y), 7.5, 4.6)], solution=sol)


@template(TOPIC, S_SLR, marks=2, qtype="MCQ")
def slr_from_sums(rng):
    while True:
        n = int(rng.integers(6, 11))
        x = rng.integers(1, 16, n).astype(float)
        y = np.round(rng.integers(-5, 10) + rng.choice([-2, -1, 1, 2, 3]) * x / 2 + rng.integers(-4, 5, n))
        Sx, Sy, Sxx_, Syy_, Sxy_ = x.sum(), y.sum(), (x * x).sum(), (y * y).sum(), (x * y).sum()
        sxx = Sxx_ - Sx ** 2 / n
        syy = Syy_ - Sy ** 2 / n
        sxy = Sxy_ - Sx * Sy / n
        if sxx <= 0 or syy <= 0:
            continue
        r = sxy / np.sqrt(sxx * syy)
        if 0.3 < abs(r) < 0.97:
            break
    xm, ym = Sx / n, Sy / n
    byx, bxy = sxy / sxx, sxy / syy
    v = int(rng.integers(3))
    stem = (f"For n = {n} paired observations: Σx = {fmt(Sx, 0)}, Σy = {fmt(Sy, 0)}, Σx² = {fmt(Sxx_, 0)}, "
            f"Σy² = {fmt(Syy_, 0)}, Σxy = {fmt(Sxy_, 0)}. ")
    sol = [f"x̄ = {fmt(xm, 4)}, ȳ = {fmt(ym, 4)}.",
           f"S<sub>xx</sub> = Σx² − (Σx)²/n = {fmt(sxx, 4)}, S<sub>yy</sub> = Σy² − (Σy)²/n = {fmt(syy, 4)}, "
           f"S<sub>xy</sub> = Σxy − ΣxΣy/n = {fmt(sxy, 4)}."]
    if v == 0:
        correct = _line(ym - byx * xm, byx)
        ds = [_line(ym - bxy * xm, bxy), _line(ym + byx * xm, byx), _line(ym - (1 / bxy) * xm, 1 / bxy),
              _line(ym - Sxy_ / Sxx_ * xm, Sxy_ / Sxx_), _line(xm - byx * ym, byx), _line(ym + byx * xm, -byx)]
        q = "The least-squares regression line of y on x is"
        sol += [f"b = S<sub>xy</sub>/S<sub>xx</sub> = {fmt(byx, 4)}; a = ȳ − b x̄ = {fmt(ym - byx * xm, 4)}.",
                f"Line: <b>{correct}</b>.",
                "Distractors: using S<sub>xy</sub>/S<sub>yy</sub> (x-on-y slope), using uncentred sums Σxy/Σx², or "
                "a sign error in the intercept."]
        opts, a = mcq(rng, correct, ds)
    elif v == 1:
        correct = _line(xm - bxy * ym, bxy, var="y", out="x̂")
        ds = [_line(xm - byx * ym, byx, var="y", out="x̂"), _line(xm + bxy * ym, bxy, var="y", out="x̂"),
              _line(xm - (1 / byx) * ym, 1 / byx, var="y", out="x̂"),
              _line(xm - Sxy_ / Syy_ * ym, Sxy_ / Syy_, var="y", out="x̂"),
              _line(ym - bxy * xm, bxy, var="y", out="x̂"), _line(xm + bxy * ym, -bxy, var="y", out="x̂")]
        q = "The least-squares regression line of <b>x on y</b> is"
        sol += [f"Regress x on y: b′ = S<sub>xy</sub>/S<sub>yy</sub> = {fmt(bxy, 4)}; a′ = x̄ − b′ȳ = "
                f"{fmt(xm - bxy * ym, 4)}.", f"Line: <b>{correct}</b>.",
                "A common error is to invert the y-on-x line (slope 1/b), which minimises the wrong (vertical) errors."]
        opts, a = mcq(rng, correct, ds)
    else:
        q = "The sample correlation coefficient r between x and y is"
        opts, a = mcq_numeric(rng, r, 3, [r * r, -r, byx, bxy, np.sign(r) * np.sqrt(abs(r))])
        sol += [f"r = S<sub>xy</sub>/√(S<sub>xx</sub>S<sub>yy</sub>) = {fmt(sxy, 4)}/√({fmt(sxx, 4)} × {fmt(syy, 4)}) = "
                f"<b>{fmt(r, 3)}</b>.", f"(r² = {fmt(r * r, 3)} would be R²; the slopes b<sub>yx</sub> = "
                f"{fmt(byx, 3)}, b<sub>xy</sub> = {fmt(bxy, 3)} satisfy b<sub>yx</sub>b<sub>xy</sub> = r².)"]
    return Q(text=stem + q + " (coefficients rounded to two decimals)" * (v < 2), qtype="MCQ", marks=2, options=opts,
             answer=a, solution=sol)


@template(TOPIC, S_SLR, marks=2, qtype="NAT")
def slr_missing_residuals(rng):
    while True:
        n = int(rng.integers(5, 7))
        x = np.sort(rng.choice(np.arange(1, 11), n, replace=False)).astype(float)
        ia, ib = sorted(rng.choice(n, 2, replace=False))
        e = np.zeros(n)
        known = [i for i in range(n) if i not in (ia, ib)]
        e[known] = rng.integers(-18, 19, len(known)) / 10
        S0, S1 = e[known].sum(), (x[known] * e[known]).sum()
        ea, eb = np.linalg.solve(np.array([[1, 1], [x[ia], x[ib]]]), [-S0, -S1])
        if max(abs(ea), abs(eb)) < 4 and min(abs(ea), abs(eb)) > 0.1:
            break
    e[ia], e[ib] = ea, eb
    c0 = float(rng.integers(-20, 41)) / 10
    c1 = float(rng.choice([-1, 1]) * rng.integers(5, 31) / 10)
    ask_b = rng.random() < 0.5
    tgt = ib if ask_b else ia
    v = int(rng.integers(2))
    rows = [["x<sub>i</sub>"] + [fmt(xi) for xi in x],
            ["e<sub>i</sub>"] + [("?" if i in (ia, ib) else fmt(e[i])) for i in range(n)]]
    stem = ("A simple linear regression with intercept is fitted by least squares. The table gives the x-values and "
            "the residuals e<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub>, but two residuals are missing. ")
    sol = ["For the least-squares fit with intercept the normal equations give Σe<sub>i</sub> = 0 and "
           "Σx<sub>i</sub>e<sub>i</sub> = 0.",
           f"Known: Σe = {fmt(S0, 3)}, Σxe = {fmt(S1, 3)}. With unknowns u = e at x = {fmt(x[ia])} and v = e at "
           f"x = {fmt(x[ib])}:",
           f"u + v = {fmt(-S0, 3)},  {fmt(x[ia])}u + {fmt(x[ib])}v = {fmt(-S1, 3)}.",
           f"Solving: u = {fmt(ea, 4)}, v = {fmt(eb, 4)}."]
    if v == 0:
        ans = e[tgt]
        q = f"The missing residual at x = {fmt(x[tgt])} is"
    else:
        ans = c0 + c1 * x[tgt] + e[tgt]
        q = (f"The fitted line is ŷ = {fmt(c0)} {'+' if c1 >= 0 else '−'} {fmt(abs(c1))}x. The observed value y at "
             f"x = {fmt(x[tgt])} is")
        sol.append(f"y = ŷ + e = ({fmt(c0)} + ({fmt(c1)})({fmt(x[tgt])})) + ({fmt(e[tgt], 4)}) = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(x[known], e[known], color=C1, s=24, zorder=3)
        for i in (ia, ib):
            ax.axvline(x[i], color=C4, ls=":", lw=1)
            ax.text(x[i], 0, "?", ha="center", va="center", fontsize=10, color=C2, fontweight="bold")
        ax.axhline(0, color=C4, lw=0.8, ls="--")
        ax.set_xlabel("x")
        ax.set_ylabel("residual e")
        ax.set_ylim(-4.2, 4.2)
        ax.grid(alpha=.3)

    return Q(text=stem + q + " _______ " + nat_hint(2), qtype="NAT", marks=2, answer=_nat(ans, 2), nat_hint=nat_hint(2),
             blocks=[Table(rows, header=False), Figure(draw, 7.5, 4.3)], solution=sol)


def _inv2(M):
    det = M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]
    return np.array([[M[1, 1], -M[0, 1]], [-M[1, 0], M[0, 0]]]) / det, det


@template(TOPIC, S_MLR, marks=2, qtype="NAT")
def mlr_normal_equations(rng):
    design = int(rng.integers(3))
    if design < 2:
        if design == 0:
            nc = int(rng.integers(0, 3))
            x1 = np.array([-1, -1, 1, 1] + [0] * nc, float)
            x2 = np.array([-1, 1, -1, 1] + [0] * nc, float)
        else:
            x1 = np.array([-2, -1, 0, 1, 2], float)
            x2 = x1 ** 2 - 2
        n = len(x1)
        X = np.c_[np.ones(n), x1, x2]
        b_true = np.array([rng.integers(2, 12), rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([-2, -1, 1, 2])], float)
        y = np.round(X @ b_true + rng.integers(-2, 3, n)).astype(float)
    else:
        while True:
            n = int(rng.integers(3, 5))
            X = rng.integers(-2, 4, (n, 2)).astype(float)
            XtX = X.T @ X
            det = np.linalg.det(XtX)
            if det >= 8 and abs(XtX[0, 1]) > 0:
                break
        y = rng.integers(-4, 9, n).astype(float)
    XtX = X.T @ X
    Xty = X.T @ y
    beta = np.linalg.solve(XtX, Xty)
    p = X.shape[1]
    names = ["β<sub>0</sub>", "β<sub>1</sub>", "β<sub>2</sub>"] if p == 3 else ["β<sub>1</sub>", "β<sub>2</sub>"]
    model = ("y = β<sub>0</sub> + β<sub>1</sub>x<sub>1</sub> + β<sub>2</sub>x<sub>2</sub> + ε (first column of X is the "
             "intercept column)" if p == 3 else "y = β<sub>1</sub>x<sub>1</sub> + β<sub>2</sub>x<sub>2</sub> + ε "
                                                 "(no intercept)")
    v = int(rng.integers(p + 1))
    sol = [Matrix("XᵀX", XtX, 2), Matrix("Xᵀy", Xty, 2)]
    if p == 3:
        sol.insert(0, "The columns of X are mutually orthogonal, so XᵀX is diagonal and each coefficient is "
                      "β̂<sub>j</sub> = (x<sub>j</sub>ᵀy)/(x<sub>j</sub>ᵀx<sub>j</sub>).")
        sol.append("β̂ = (" + ", ".join(f"{fmt(Xty[j])}/{fmt(XtX[j, j])}" for j in range(3)) + ") = (" +
                   ", ".join(fmt(b, 4) for b in beta) + ").")
    else:
        inv, det = _inv2(XtX)
        sol.append(f"det(XᵀX) = {fmt(det, 3)}; (XᵀX)⁻¹ = (1/{fmt(det, 3)})·[[{fmt(XtX[1, 1])}, {fmt(-XtX[0, 1])}], "
                   f"[{fmt(-XtX[1, 0])}, {fmt(XtX[0, 0])}]].")
        sol.append(f"β̂ = (XᵀX)⁻¹Xᵀy = ({fmt(beta[0], 4)}, {fmt(beta[1], 4)}).")
    if v < p:
        ans = beta[v]
        q = f"the least-squares estimate of {names[v]} is"
    else:
        if p == 3:
            xn = (float(rng.choice([-1.5, -0.5, 0.5, 1.5, 2])), float(rng.choice([-1, 0.5, 1, 2])))
            ans = beta[0] + beta[1] * xn[0] + beta[2] * xn[1]
            sol.append(f"ŷ = {fmt(beta[0], 4)} + ({fmt(beta[1], 4)})({fmt(xn[0])}) + ({fmt(beta[2], 4)})({fmt(xn[1])}) "
                       f"= {fmt(ans, 4)}.")
        else:
            xn = (float(rng.integers(1, 4)), float(rng.integers(-2, 4)))
            ans = beta[0] * xn[0] + beta[1] * xn[1]
            sol.append(f"ŷ = ({fmt(beta[0], 4)})({fmt(xn[0])}) + ({fmt(beta[1], 4)})({fmt(xn[1])}) = {fmt(ans, 4)}.")
        q = f"the predicted response at (x<sub>1</sub>, x<sub>2</sub>) = ({fmt(xn[0])}, {fmt(xn[1])}) is"
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"Consider the model {model}, fitted by least squares using β̂ = (XᵀX)⁻¹Xᵀy with the design "
                  f"matrix X and response y below. Then {q} _______ {nat_hint(2)}",
             qtype="NAT", marks=2, answer=_nat(ans, 2, base=0.02), nat_hint=nat_hint(2),
             blocks=[Matrix("X", X, 2), Matrix("y", y, 2)], solution=sol)


MLR_CTX = [
    dict(resp="annual salary (₹ lakh)", num="Exp", numdesc="years of experience", unit="years", bin="Female",
         bindesc="1 if the employee is female, 0 otherwise", cat="city", levels=["A", "B", "C"],
         person=lambda nv, bv, c: f"a {'female' if bv else 'male'} employee in city {c} with {nv} years of experience"),
    dict(resp="house price (₹ lakh)", num="Area", numdesc="area in hundreds of sq. ft", unit="hundred sq. ft",
         bin="Furnished", bindesc="1 if furnished, 0 otherwise", cat="zone", levels=["North", "South", "East"],
         person=lambda nv, bv, c: f"a {'furnished' if bv else 'unfurnished'} house in the {c} zone with area "
                                  f"{nv} hundred sq. ft"),
]


@template(TOPIC, S_MLR, marks=2, qtype="MSQ")
def mlr_dummy_interpretation(rng):
    ctx = MLR_CTX[int(rng.integers(len(MLR_CTX)))]
    L = ctx["levels"]
    b0 = float(rng.integers(5, 31))
    b1 = float(rng.integers(5, 31)) / 10
    b2 = float(rng.choice([-1, 1]) * rng.integers(5, 41) / 10)
    while True:
        b3, b4 = (rng.choice([-1, 1], 2) * rng.integers(5, 61, 2) / 10).astype(float)
        if abs(b3 - b4) > 0.4 and abs(b4) > 0.4 and abs(b3) > 0.4:
            break
    nm = ctx["num"]
    D2, D3 = f"{ctx['cat'].capitalize()}{L[1]}", f"{ctx['cat'].capitalize()}{L[2]}"
    eq = (f"ŷ = {fmt(b0)} + {fmt(b1)}·{nm} {'+' if b2 >= 0 else '−'} {fmt(abs(b2))}·{ctx['bin']} "
          f"{'+' if b3 >= 0 else '−'} {fmt(abs(b3))}·{D2} {'+' if b4 >= 0 else '−'} {fmt(abs(b4))}·{D3}")
    nv = int(rng.integers(2, 12))
    bv = int(rng.integers(2))
    ci = int(rng.integers(1, 3))
    pred = b0 + b1 * nv + b2 * bv + (b3 if ci == 1 else b4)
    wrong = pred - (b3 if ci == 1 else b4)
    if abs(wrong - pred) < 0.05:
        wrong = pred + 1
    k = int(rng.choice([kk for kk in range(2, 6) if abs(kk * b1 - (b1 + kk)) > 0.05]))
    pers = ctx["person"](nv, bv, L[ci])
    T = [(f"The predicted {ctx['resp'].split(' (')[0]} for {pers} is {fmt(pred)}.",
          f"ŷ = {fmt(b0)} + {fmt(b1)}×{nv} + ({fmt(b2)})×{bv} + ({fmt(b3 if ci == 1 else b4)}) = {fmt(pred)}."),
         (f"Holding other variables fixed, the predicted response for {ctx['cat']} {L[1]} minus that for "
          f"{ctx['cat']} {L[2]} is {fmt(b3 - b4)}.", f"Difference of the two dummy coefficients: {fmt(b3)} − ({fmt(b4)})."),
         (f"The coefficient of {D2} is the expected difference in response between {ctx['cat']} {L[1]} and "
          f"{ctx['cat']} {L[0]}, holding the other variables fixed.", f"{L[0]} is the reference level (all dummies 0)."),
         (f"Adding a third dummy for {ctx['cat']} {L[0]} while keeping the intercept would make XᵀX singular.",
          "The three dummies would sum to the intercept column (dummy-variable trap)."),
         (f"Increasing {nm} by {k} {ctx['unit']}, other variables fixed, changes the prediction by {fmt(k * b1)}.",
          f"{k} × {fmt(b1)} = {fmt(k * b1)}.")]
    F = [(f"The predicted {ctx['resp'].split(' (')[0]} for {pers} is {fmt(wrong)}.",
          f"This omits the {ctx['cat']} dummy; the correct value is {fmt(pred)}."),
         (f"Holding other variables fixed, the predicted response for {ctx['cat']} {L[1]} minus that for "
          f"{ctx['cat']} {L[2]} is {fmt(b3 + b4)}.", f"It is {fmt(b3)} − ({fmt(b4)}) = {fmt(b3 - b4)}, not the sum."),
         (f"The coefficient of {D2} equals the average response of all observations in {ctx['cat']} {L[1]}.",
          f"It is a difference relative to the reference level {L[0]}, adjusted for the other variables."),
         (f"The intercept {fmt(b0)} is the predicted response when {ctx['bin']} = 1, {nm} = 0, in {ctx['cat']} {L[2]}.",
          f"The intercept corresponds to {ctx['bin']} = 0, {nm} = 0 and the reference level {L[0]}."),
         (f"Increasing {nm} by {k} {ctx['unit']}, other variables fixed, changes the prediction by {fmt(b1 + k)}.",
          f"The change is {k} × {fmt(b1)} = {fmt(k * b1)}.")]
    opts, ans, expl = msq_from_statements(rng, T, F)
    return Q(text=f"A linear regression of {ctx['resp']} on {nm} ({ctx['numdesc']}), {ctx['bin']} ({ctx['bindesc']}) and "
                  f"{ctx['cat']} ∈ {{{', '.join(L)}}} encoded by dummies {D2} and {D3} (reference level {L[0]}) gives "
                  f"the fitted model<br/><font face='Mono'>{eq}</font><br/>Which of the following is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, solution=expl)


@template(TOPIC, S_MLR, marks=2, qtype="NAT")
def adjusted_r2(rng):
    v = int(rng.integers(3))
    sol = ["Adjusted R² = 1 − [SSE/(n − p − 1)]/[SST/(n − 1)] = 1 − (1 − R²)(n − 1)/(n − p − 1), where p is the number "
           "of predictors (excluding the intercept)."]
    if v == 0:
        n = int(rng.integers(15, 61))
        p = int(rng.integers(2, 7))
        sst = float(rng.integers(200, 1000))
        sse = float(np.round(sst * rng.uniform(0.15, 0.6)))
        ans = 1 - (sse / (n - p - 1)) / (sst / (n - 1))
        q = (f"A multiple regression with an intercept and p = {p} predictors is fitted to n = {n} observations, giving "
             f"SSE = {fmt(sse)} and SST = {fmt(sst)}. The adjusted R² is")
        sol.append(f"= 1 − ({fmt(sse)}/{n - p - 1})/({fmt(sst)}/{n - 1}) = 1 − {fmt(sse / (n - p - 1), 4)}/"
                   f"{fmt(sst / (n - 1), 4)} = {fmt(ans, 4)}.")
    elif v == 1:
        n = int(rng.integers(12, 41))
        pA = int(rng.integers(1, 4))
        pB = pA + int(rng.integers(1, 4))
        rA = float(rng.integers(50, 85)) / 100
        rB = min(0.97, rA + float(rng.integers(1, 9)) / 100)
        aA = 1 - (1 - rA) * (n - 1) / (n - pA - 1)
        aB = 1 - (1 - rB) * (n - 1) / (n - pB - 1)
        ans = aB - aA
        q = (f"On n = {n} observations, model A (intercept + {pA} predictor{'s' if pA > 1 else ''}) has R² = {fmt(rA)}, "
             f"and model B (intercept + {pB} predictors, containing those of A) has R² = {fmt(rB)}. The value of "
             "(adjusted R² of B) − (adjusted R² of A) is")
        sol += [f"A: 1 − (1 − {fmt(rA)})({n - 1})/({n - pA - 1}) = {fmt(aA, 4)}.",
                f"B: 1 − (1 − {fmt(rB)})({n - 1})/({n - pB - 1}) = {fmt(aB, 4)}.",
                f"Difference = {fmt(ans, 4)}" + (" (negative: the extra predictors do not justify their cost even "
                                                 "though R² increased)." if ans < 0 else ".")]
    else:
        n = int(rng.integers(10, 51))
        p = int(rng.integers(2, 6))
        r2 = float(rng.integers(40, 95)) / 100
        ans = 1 - (1 - r2) * (n - 1) / (n - p - 1)
        q = f"A regression with intercept and p = {p} predictors on n = {n} observations has R² = {fmt(r2)}. Its adjusted R² is"
        sol.append(f"= 1 − (1 − {fmt(r2)}) × {n - 1}/{n - p - 1} = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=q + " _______ " + nat_hint(3), qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.002),
             nat_hint=nat_hint(3), solution=sol)


@template(TOPIC, S_MLR, marks=2, qtype="NAT")
def leverage_slr(rng):
    while True:
        n = int(rng.integers(5, 8))
        x = np.sort(rng.choice(np.arange(0, 15), n, replace=False)).astype(float)
        if x.max() - x.min() >= 6:
            break
    y = np.round(rng.uniform(2, 9) + rng.uniform(-1, 1) * x + rng.normal(0, 1.5, n), 1)
    xm = x.mean()
    sxx = ((x - xm) ** 2).sum()
    h = 1 / n + (x - xm) ** 2 / sxx
    v = int(rng.integers(3))
    i = int(np.argmax(h)) if v == 2 else int(rng.integers(n))
    sol = ["For simple linear regression with intercept, the leverage (diagonal of the hat matrix) is "
           "h<sub>ii</sub> = 1/n + (x<sub>i</sub> − x̄)²/S<sub>xx</sub>.",
           f"x̄ = {fmt(xm, 4)}, S<sub>xx</sub> = {fmt(sxx, 4)}."]
    if v == 0:
        ans = h[i]
        q = f"the leverage h<sub>ii</sub> of the observation with x = {fmt(x[i])} (circled) is"
        sol.append(f"h = 1/{n} + ({fmt(x[i] - xm, 4)})²/{fmt(sxx, 4)} = {fmt(ans, 4)}.")
        hl = i
    elif v == 1:
        s2 = float(rng.choice([1, 2, 4, 5, 9]))
        ans = s2 * (1 - h[i])
        q = (f"if the errors have variance σ² = {fmt(s2)}, the variance of the residual e<sub>i</sub> of the observation "
             f"with x = {fmt(x[i])} (circled) is")
        sol += [f"h = {fmt(h[i], 4)}; Var(e<sub>i</sub>) = σ²(1 − h<sub>ii</sub>) = {fmt(s2)} × {fmt(1 - h[i], 4)} = "
                f"{fmt(ans, 4)}."]
        hl = i
    else:
        ans = h.max()
        q = "the largest leverage among the observations is"
        sol.append("The largest leverage is at the x farthest from x̄: x = " + fmt(x[i]) +
                   f", h = 1/{n} + ({fmt(x[i] - xm, 4)})²/{fmt(sxx, 4)} = {fmt(ans, 4)}.")
        sol.append(f"(Check: Σh<sub>ii</sub> = {fmt(h.sum(), 4)} = 2 = number of parameters.)")
        hl = None
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"A simple linear regression (with intercept) is fitted by least squares to the {n} points shown. "
                  f"With H = X(XᵀX)⁻¹Xᵀ, {q} _______ {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.002, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y, highlight=hl), 7.5, 4.4)], solution=sol)


@template(TOPIC, S_RIDGE, marks=2, qtype="NAT")
def ridge_closed_form(rng):
    while True:
        n = int(rng.integers(3, 5))
        X = rng.integers(-2, 4, (n, 2)).astype(float)
        if np.linalg.matrix_rank(X) < 2 and rng.random() < 0.6:
            continue
        XtX = X.T @ X
        if XtX[0, 1] == 0 or XtX[0, 0] == 0 or XtX[1, 1] == 0:
            continue
        break
    y = rng.integers(-3, 8, n).astype(float)
    lam = float(rng.integers(1, 6))
    A = XtX + lam * np.eye(2)
    Xty = X.T @ y
    inv, det = _inv2(A)
    beta = inv @ Xty
    v = int(rng.integers(4))
    if v < 2:
        ans, q = beta[v], f"β̂<sub>{v + 1}</sub>"
    elif v == 2:
        xn = rng.integers(-1, 4, 2).astype(float)
        while not xn.any():
            xn = rng.integers(-1, 4, 2).astype(float)
        ans = xn @ beta
        q = f"the ridge prediction at x = ({fmt(xn[0])}, {fmt(xn[1])})"
    else:
        ans = beta @ beta
        q = "‖β̂‖²<sub>2</sub>"
    sol = [f"β̂<sub>ridge</sub> = (XᵀX + λI)⁻¹Xᵀy with λ = {fmt(lam)}.", Matrix("XᵀX", XtX, 2),
           Matrix("XᵀX + λI", A, 2), Matrix("Xᵀy", Xty, 2),
           f"det = {fmt(A[0, 0])}×{fmt(A[1, 1])} − ({fmt(A[0, 1])})² = {fmt(det)}; "
           f"(XᵀX + λI)⁻¹ = (1/{fmt(det)})[[{fmt(A[1, 1])}, {fmt(-A[0, 1])}], [{fmt(-A[1, 0])}, {fmt(A[0, 0])}]].",
           f"β̂ = ({fmt(beta[0], 4)}, {fmt(beta[1], 4)})."]
    if v == 2:
        sol.append(f"ŷ = {fmt(xn[0])}×{fmt(beta[0], 4)} + {fmt(xn[1])}×{fmt(beta[1], 4)} = {fmt(ans, 4)}.")
    if v == 3:
        sol.append(f"‖β̂‖² = ({fmt(beta[0], 4)})² + ({fmt(beta[1], 4)})² = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"Ridge regression without intercept minimises ‖y − Xβ‖²<sub>2</sub> + λ‖β‖²<sub>2</sub> with "
                  f"λ = {fmt(lam)}, for the data below (β = (β<sub>1</sub>, β<sub>2</sub>)ᵀ). The value of {q} is "
                  f"_______ {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.003, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[Matrix("X", X, 2), Matrix("y", y, 2)], solution=sol)


@template(TOPIC, S_RIDGE, marks=2, qtype="NAT")
def ridge_lasso_orthonormal(rng):
    p = 5
    while True:
        b = (rng.choice([-1, 1], p) * rng.integers(2, 41, p) / 10).astype(float)
        if len(set(np.abs(b))) < p or np.min(np.diff(np.sort(np.abs(b)))) < 0.2:
            continue
        lam = float(rng.choice([0.5, 1.0, 1.5, 2.0, 2.5]))
        if np.min(np.abs(np.abs(b) - lam)) < 0.15 or (np.abs(b) > lam).sum() in (0, p):
            continue
        break
    ridge = b / (1 + lam)
    lasso = np.sign(b) * np.maximum(np.abs(b) - lam, 0)
    v = int(rng.integers(6))
    d = 2
    if v == 0:
        ans, d = int((lasso != 0).sum()), 0
        q = "the number of non-zero coefficients in the lasso solution is"
    elif v == 1:
        ans = lasso.sum()
        q = "the sum β̂<sub>1</sub> + … + β̂<sub>5</sub> of the lasso coefficients is"
    elif v == 2:
        ans = np.linalg.norm(ridge)
        q = "the Euclidean norm ‖β̂<sub>ridge</sub>‖<sub>2</sub> is"
    elif v == 3:
        j = int(rng.integers(p))
        ans = ridge[j]
        q = f"the ridge estimate of β<sub>{j + 1}</sub> is"
    elif v == 4:
        ans = np.abs(lasso).sum()
        q = "‖β̂<sub>lasso</sub>‖<sub>1</sub> is"
    else:
        m = int(rng.integers(2, 5))
        ans = np.sort(np.abs(b))[m - 1]
        q = (f"(ignoring the given λ) the smallest value of λ for which the lasso sets at least {m} coefficients "
             "exactly to zero is")
    sol = ["With XᵀX = I: β̂<sub>OLS</sub> = Xᵀy = b.",
           "Ridge: ∇[‖y−Xβ‖² + λ‖β‖²] = 0 ⇒ (1 + λ)β = b ⇒ β̂<sub>ridge</sub> = b/(1 + λ).",
           "Lasso: the problem separates per coordinate, min ½(β<sub>j</sub> − b<sub>j</sub>)² + λ|β<sub>j</sub>| ⇒ "
           "soft-thresholding β̂<sub>j</sub> = sign(b<sub>j</sub>)·max(|b<sub>j</sub>| − λ, 0).",
           Table([["j"] + [str(j + 1) for j in range(p)], ["b<sub>j</sub>"] + [fmt(t) for t in b],
                  ["ridge"] + [fmt(t, 4) for t in ridge], ["lasso"] + [fmt(t, 2) for t in lasso]], header=False)]
    if v == 5:
        sol = sol[:3] + [f"Coefficient j becomes 0 once λ ≥ |b<sub>j</sub>|. Sorted |b|: "
                         f"{', '.join(fmt(t) for t in np.sort(np.abs(b)))}; the {m}-th smallest is {fmt(ans)}."]
    sol.append(f"Answer: <b>{fmt(ans, d)}</b>.")

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.bar(range(1, p + 1), b, color=C1, width=0.55)
        for j, t in enumerate(b):
            ax.text(j + 1, t + (0.12 if t >= 0 else -0.12), fmt(t), ha="center", va="bottom" if t >= 0 else "top",
                    fontsize=7)
        ax.axhline(0, color="k", lw=0.8)
        ax.set_xticks(range(1, p + 1))
        ax.set_xticklabels([f"β{chr(0x2080 + j + 1)}" for j in range(p)])
        ax.set_ylabel("OLS estimate b_j".replace("_j", ""))
        ax.set_ylim(min(b.min(), 0) - 0.7, max(b.max(), 0) + 0.7)

    ans_rng = (ans, ans) if d == 0 else nat_range(ans, 2, max(0.01, 0.004 * abs(ans)))
    return Q(text="In a regression problem the design matrix X has orthonormal columns (XᵀX = I). The ordinary "
                  "least-squares estimates b = Xᵀy are shown below. Ridge minimises ‖y − Xβ‖² + λ‖β‖²<sub>2</sub> and "
                  "the lasso minimises ½‖y − Xβ‖² + λ‖β‖<sub>1</sub>, each with "
                  f"λ = {fmt(lam)}. Then {q} _______ {nat_hint(d)}",
             qtype="NAT", marks=2, answer=ans_rng, nat_hint=nat_hint(d), blocks=[Figure(draw, 8, 4.6)], solution=sol)


@template(TOPIC, S_RIDGE, marks=2, qtype="MSQ")
def coefficient_path(rng):
    p = 4
    while True:
        b = (rng.choice([-1, 1], p) * rng.integers(5, 41, p) / 10).astype(float)
        sa = np.sort(np.abs(b))
        if sa[0] >= 0.5 and np.min(np.diff(sa)) >= 0.4:
            break
    Lmax = float(np.ceil(np.abs(b).max()) + 1)
    kind = "lasso" if rng.random() < 0.5 else "ridge"
    cands = [l for l in np.arange(0.5, Lmax, 0.5) if np.min(np.abs(np.abs(b) - l)) >= 0.25]
    lam0 = float(rng.choice(cands))
    lg = np.linspace(0, Lmax, 300)
    if kind == "lasso":
        paths = np.sign(b)[None, :] * np.maximum(np.abs(b)[None, :] - lg[:, None], 0)
        nz = int((np.abs(b) <= lam0).sum())
    else:
        paths = b[None, :] / (1 + lg[:, None])
        nz = 0
    other = "ridge" if kind == "lasso" else "lasso"
    T = [("At λ = 0 the coefficients equal the least-squares estimates.", "Penalty vanishes at λ = 0."),
         ("As λ increases, |β̂<sub>j</sub>(λ)| is non-increasing for every j.",
          "Both b/(1+λ) and soft-thresholding shrink monotonically.")]
    F = []
    if kind == "lasso":
        T += [("The plotted paths are those of the lasso (L1 penalty).", "Coefficients hit exactly zero at finite λ."),
              ("Each coefficient path is piecewise linear in λ.", "sign(b)(|b| − λ)<sub>+</sub> is piecewise linear."),
              (f"At λ = {fmt(lam0)}, exactly {nz} coefficient(s) are zero.",
               f"Coefficients with |b<sub>j</sub>| ≤ {fmt(lam0)} are zero: count = {nz}.")]
        F += [("The plotted paths are those of ridge regression (L2 penalty).",
               "Ridge never produces exact zeros at finite λ; these paths do."),
              (f"At λ = {fmt(lam0)}, exactly {nz + 1 if nz < p else nz - 1} coefficient(s) are zero.",
               f"The correct count is {nz}."),
              ("No coefficient becomes exactly zero for any finite λ.", "Under lasso β̂<sub>j</sub> = 0 for λ ≥ |b<sub>j</sub>|.")]
    else:
        T += [("The plotted paths are those of ridge regression (L2 penalty).",
               "Smooth decay b/(1+λ), no exact zeros."),
              ("No coefficient becomes exactly zero for any finite λ.", "b/(1+λ) ≠ 0 whenever b ≠ 0."),
              (f"At λ = {fmt(lam0)}, every coefficient equals its least-squares value divided by {fmt(1 + lam0)}.",
               "β̂(λ) = b/(1 + λ).")]
        F += [("The plotted paths are those of the lasso (L1 penalty).", "No path reaches zero at a finite λ."),
              ("Each coefficient path is piecewise linear in λ.", "b/(1+λ) is a smooth hyperbola, not piecewise linear."),
              (f"At λ = {fmt(lam0)}, at least one coefficient is exactly zero.", "Ridge gives no exact zeros.")]
    F += [("At λ = 0 all coefficients equal zero.", "At λ = 0 they are the OLS estimates."),
          ("As λ increases, the training residual sum of squares decreases.",
           "Training RSS is minimised at λ = 0 and increases with λ.")]
    opts, ans, expl = msq_from_statements(rng, T, F)

    def draw(fig):
        ax = fig.add_subplot(111)
        st = ["-", "--", "-.", ":"]
        for j in range(p):
            ax.plot(lg, paths[:, j], st[j], color=[C1, C2, C3, "k"][j], lw=1.5, label=f"β{chr(0x2080 + j + 1)}")
        ax.axhline(0, color=C4, lw=0.7)
        ax.axvline(lam0, color=C4, lw=0.8, ls=":")
        ax.text(lam0, ax.get_ylim()[1], f"λ = {fmt(lam0)}", ha="center", va="bottom", fontsize=7)
        ax.set_xlabel("λ")
        ax.set_ylabel("coefficient estimate")
        ax.set_xticks(np.arange(0, Lmax + 0.01, 0.5 if Lmax <= 5 else 1))
        ax.grid(alpha=.3)
        ax.legend(frameon=False, fontsize=7, loc="upper left", bbox_to_anchor=(1.0, 1.0))

    return Q(text="For a design with orthonormal columns (XᵀX = I), the figure shows the coefficient paths "
                  "β̂<sub>j</sub>(λ) of a penalised least-squares estimator that minimises ½‖y − Xβ‖² + P<sub>λ</sub>(β), "
                  "where the penalty P<sub>λ</sub> is either the ridge penalty (λ/2)‖β‖²<sub>2</sub> or the lasso "
                  "penalty λ‖β‖<sub>1</sub>. Which of the following statements is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans, blocks=[Figure(draw, 9, 5.6)],
             solution=[f"With XᵀX = I the ridge path is b/(1 + λ) and the lasso path is sign(b)(|b| − λ)<sub>+</sub>. "
                       f"The plot shows paths reaching zero at finite λ ⇔ lasso; here it is <b>{kind}</b>."] + expl)


@template(TOPIC, S_RIDGE, marks=2, qtype="NAT")
def ridge_effective_df(rng):
    p = int(rng.integers(2, 5))
    eig = np.sort(rng.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 16, 20, 25], p, replace=False).astype(float))[::-1]
    lam = float(rng.choice([1, 2, 3, 4, 5]))
    df = (eig / (eig + lam)).sum()
    v = int(rng.integers(3))
    sol = ["Ridge fitted values ŷ = H<sub>λ</sub>y with H<sub>λ</sub> = X(XᵀX + λI)⁻¹Xᵀ. Writing XᵀX = VDVᵀ with "
           "eigenvalues d<sub>j</sub>² gives trace(H<sub>λ</sub>) = Σ d<sub>j</sub>²/(d<sub>j</sub>² + λ) "
           "(effective degrees of freedom).",
           " + ".join(f"{fmt(e)}/({fmt(e)} + {fmt(lam)})" for e in eig) + f" = {fmt(df, 4)}."]
    if v == 0:
        ans = df
        q = f"the effective degrees of freedom df(λ) = trace[X(XᵀX + λI)⁻¹Xᵀ] for λ = {fmt(lam)} is"
    elif v == 1:
        ans = p - df
        q = (f"the reduction in effective degrees of freedom relative to ordinary least squares, p − df(λ), "
             f"for λ = {fmt(lam)} is")
        sol.append(f"OLS has df = trace(H) = p = {p}; reduction = {p} − {fmt(df, 4)} = {fmt(ans, 4)}.")
    else:
        lam2 = lam * float(rng.choice([2, 3, 4]))
        df2 = (eig / (eig + lam2)).sum()
        ans = df - df2
        q = f"df({fmt(lam)}) − df({fmt(lam2)}) is"
        sol.append(" + ".join(f"{fmt(e)}/({fmt(e)} + {fmt(lam2)})" for e in eig) + f" = {fmt(df2, 4)}.")
        sol.append(f"Difference = {fmt(df, 4)} − {fmt(df2, 4)} = {fmt(ans, 4)} (df decreases as λ grows).")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"The {p} × {p} matrix XᵀX of a (centred) design matrix X has eigenvalues "
                  f"{', '.join(fmt(e) for e in eig)}. For ridge regression with penalty λ‖β‖²<sub>2</sub>, {q} "
                  f"_______ {nat_hint(2)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 2), nat_hint=nat_hint(2), solution=sol)

@template(TOPIC, S_BV, marks=2, qtype="NAT")
def bv_decomposition_numbers(rng):
    M = int(rng.integers(5, 7))
    f0 = float(rng.integers(5, 16))
    shift = float(rng.choice([-1, 1]) * rng.integers(3, 16) / 10)
    while True:
        preds = np.round(f0 + shift + rng.normal(0, rng.uniform(0.4, 1.2), M), 1)
        if np.ptp(preds) > 0.5 and abs(preds.mean() - f0) >= 0.3:
            break
    s2 = float(rng.choice([0.25, 0.5, 1.0, 1.5, 2.0]))
    mbar = preds.mean()
    bias2 = (mbar - f0) ** 2
    var = ((preds - mbar) ** 2).mean()
    tot = bias2 + var + s2
    v = int(rng.integers(3))
    q = ["the squared bias of the method at x<sub>0</sub> is", "the variance of the method's prediction at "
         "x<sub>0</sub> is", "the expected squared prediction error E[(y<sub>0</sub> − f̂(x<sub>0</sub>))²] at "
         "x<sub>0</sub> is"][v]
    ans = [bias2, var, tot][v]

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.scatter(range(1, M + 1), preds, color=C1, s=26, zorder=3, label="f̂ₘ(x₀)")
        ax.axhline(f0, color=C2, ls="--", lw=1.2, label="true f(x₀)")
        ax.set_xticks(range(1, M + 1))
        ax.set_xlabel("training set m")
        ax.set_ylabel("prediction at x₀")
        ax.legend(frameon=False, fontsize=7)
        ax.grid(alpha=.3)

    sol = [f"Mean prediction f̄ = (1/{M})Σf̂<sub>m</sub> = {fmt(mbar, 4)}.",
           f"Bias² = (f̄ − f(x<sub>0</sub>))² = ({fmt(mbar, 4)} − {fmt(f0)})² = {fmt(bias2, 4)}.",
           f"Variance = (1/{M})Σ(f̂<sub>m</sub> − f̄)² = {fmt(var, 4)}.",
           f"Expected test error = Bias² + Variance + σ² = {fmt(bias2, 4)} + {fmt(var, 4)} + {fmt(s2)} = {fmt(tot, 4)}.",
           f"Answer: <b>{fmt(ans, 3)}</b>."]
    return Q(text=f"Data are generated as y = f(x) + ε with E[ε] = 0 and Var(ε) = σ² = {fmt(s2)}. At a test point "
                  f"x<sub>0</sub> the true value is f(x<sub>0</sub>) = {fmt(f0)}. A learning method is trained on {M} "
                  "independent training sets, giving the predictions f̂<sub>m</sub>(x<sub>0</sub>) in the table "
                  "(also plotted). Treating these as the full distribution of the method's prediction (variance with "
                  f"divisor {M}), {q} _______ {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.003, 0.003 * ans)), nat_hint=nat_hint(3),
             blocks=[Table([["m"] + [str(i + 1) for i in range(M)],
                            ["f̂<sub>m</sub>(x<sub>0</sub>)"] + [fmt(t, 1) for t in preds]], header=False),
                     Figure(draw, 7.5, 4.3)], solution=sol)


@template(TOPIC, S_BV, marks=2, qtype="NAT")
def bv_shrinkage_estimator(rng):
    mu = float(rng.integers(1, 5))
    s2 = float(rng.choice([4, 9, 16, 25]))
    n = int(rng.choice([4, 5, 8, 10, 16, 20, 25]))
    c = float(rng.choice([0.5, 0.6, 0.7, 0.75, 0.8, 0.9]))
    mse = (c - 1) ** 2 * mu ** 2 + c * c * s2 / n
    v = int(rng.integers(3))
    sol = [f"E[c x̄] = cμ ⇒ Bias = (c − 1)μ; Var(c x̄) = c²σ²/n. MSE(c) = (c − 1)²μ² + c²σ²/n.",
           f"Here μ = {fmt(mu)}, σ²/n = {fmt(s2)}/{n} = {fmt(s2 / n, 4)}."]
    if v == 0:
        ans = mse
        q = f"the mean squared error of μ̂ = {fmt(c)}·x̄ is"
        sol.append(f"MSE = ({fmt(c - 1)})²({fmt(mu)})² + ({fmt(c)})²({fmt(s2 / n, 4)}) = {fmt((c - 1) ** 2 * mu ** 2, 4)} + "
                   f"{fmt(c * c * s2 / n, 4)} = {fmt(ans, 4)}.")
    elif v == 1:
        ans = s2 / n - mse
        q = f"MSE(x̄) − MSE({fmt(c)}·x̄) is (a negative value means shrinkage is worse)"
        sol.append(f"MSE(x̄) = σ²/n = {fmt(s2 / n, 4)} (unbiased). MSE({fmt(c)}x̄) = {fmt(mse, 4)}. "
                   f"Difference = {fmt(ans, 4)}.")
    else:
        ans = mu ** 2 / (mu ** 2 + s2 / n)
        q = "the value of c that minimises the MSE of μ̂ = c·x̄ is"
        sol.append("dMSE/dc = 2(c − 1)μ² + 2cσ²/n = 0 ⇒ c* = μ²/(μ² + σ²/n) = "
                   f"{fmt(mu * mu)}/({fmt(mu * mu)} + {fmt(s2 / n, 4)}) = {fmt(ans, 4)}.")
        sol.append("c* &lt; 1: accepting some bias reduces variance enough to lower MSE.")
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"X<sub>1</sub>, …, X<sub>n</sub> are i.i.d. with mean μ = {fmt(mu)} and variance σ² = {fmt(s2)}, with "
                  f"n = {n}. Consider the shrinkage estimator μ̂ = c·x̄ of μ, where x̄ is the sample mean. Using "
                  f"MSE = Bias² + Variance, {q} _______ {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, 0.003), nat_hint=nat_hint(3), solution=sol)


@template(TOPIC, S_BV, marks=2, qtype="MSQ")
def bv_degree_table(rng):
    D = 7
    ds = np.arange(1, D + 1)
    tinf = rng.uniform(0.5, 1.5)
    train = np.round(tinf + rng.uniform(6, 10) * np.exp(-0.75 * (ds - 1)) - 0.08 * (ds - 1), 2)
    dstar = int(rng.integers(2, 5))
    while True:
        val = np.empty(D)
        val[dstar - 1] = round(train[dstar - 1] + rng.uniform(0.5, 1.2), 2)
        for d in range(dstar - 1, 0, -1):
            val[d - 1] = round(max(val[d] + rng.uniform(0.8, 2.5), train[d - 1] + 0.3), 2)
        for d in range(dstar + 1, D + 1):
            val[d - 1] = round(val[d - 2] + rng.uniform(0.3, 1.6), 2)
        gap = val - train
        if np.sort(gap)[-1] - np.sort(gap)[-2] > 0.1 and np.all(np.diff(train) < 0):
            break
    g = int(np.argmax(gap)) + 1
    wrong_d = int(rng.choice([d for d in ds if d != dstar]))
    wrong_g = int(rng.choice([d for d in ds if d != g]))
    lo = int(rng.integers(1, dstar + 1))
    T = [(f"Based on the validation MSE, degree {dstar} should be selected.",
          f"Validation MSE is minimum ({fmt(val[dstar - 1])}) at degree {dstar}."),
         ("The degree-1 model underfits: its training and validation errors are both high.",
          f"Training {fmt(train[0])} and validation {fmt(val[0])} are both large — high bias."),
         (f"The degree-{D} model overfits: it has the lowest training MSE but its validation MSE exceeds the minimum.",
          f"Train {fmt(train[-1])} (lowest), validation {fmt(val[-1])} &gt; {fmt(val[dstar - 1])}."),
         (f"The generalisation gap (validation MSE − training MSE) is largest for degree {g}.",
          f"Gaps: {', '.join(fmt(t) for t in gap)}."),
         (f"The degree-{D} model has higher variance than the degree-{lo} model.",
          "Higher-degree polynomials are more flexible → higher variance.")]
    F = [(f"Based on the validation MSE, degree {wrong_d} should be selected.",
          f"The minimum validation MSE is at degree {dstar}, not {wrong_d}."),
         (f"Since training MSE keeps decreasing, the degree-{D} model generalises best.",
          "Training error always falls with degree for nested fits; it says nothing about generalisation."),
         (f"The generalisation gap (validation MSE − training MSE) is largest for degree {wrong_g}.",
          f"Gaps: {', '.join(fmt(t) for t in gap)}; the largest is at degree {g}."),
         (f"The degree-{lo} model has higher variance than the degree-{D} model.",
          "Lower-degree models are less flexible and have lower variance."),
         ("The validation MSE of the selected degree is an unbiased estimate of its test error, even though it was "
          "used for the selection.", "Choosing the minimum makes it optimistically biased; a separate test set is needed.")]
    opts, ans, expl = msq_from_statements(rng, T, F)

    def draw(fig):
        ax = fig.add_subplot(111)
        ax.plot(ds, train, "o-", color=C1, lw=1.3, ms=3.5, label="training MSE")
        ax.plot(ds, val, "s--", color=C2, lw=1.3, ms=3.5, label="validation MSE")
        ax.set_xlabel("polynomial degree")
        ax.set_ylabel("MSE")
        ax.set_xticks(ds)
        ax.grid(alpha=.3)
        ax.legend(frameon=False, fontsize=7)

    return Q(text="Polynomial regression models of degree 1 to 7 are fitted by least squares on a training set and "
                  "evaluated on a separate validation set. The resulting mean squared errors are given below. Which "
                  "of the following statements is/are CORRECT?",
             qtype="MSQ", marks=2, options=opts, answer=ans,
             blocks=[Table([["Degree"] + [str(d) for d in ds], ["Training MSE"] + [fmt(t) for t in train],
                            ["Validation MSE"] + [fmt(t) for t in val]], header=False), Figure(draw, 7.5, 4.3)],
             solution=expl)


def _fold_diagram(sizes, shade_labels=True):
    k = len(sizes)
    n = sum(sizes)

    def draw(fig):
        ax = fig.add_subplot(111)
        starts = np.cumsum([0] + list(sizes))[:-1]
        for r in range(k):
            for j in range(k):
                ax.barh(k - r, sizes[j], left=starts[j], height=0.7,
                        color=C2 if j == r else "#d9d9d9", edgecolor="white")
            ax.text(-0.5, k - r, f"split {r + 1}", ha="right", va="center", fontsize=7)
        for j in range(k):
            ax.text(starts[j] + sizes[j] / 2, k + 0.65, f"F{j + 1} ({sizes[j]})", ha="center", fontsize=6.5)
        ax.set_xlim(-n * 0.18, n)
        ax.set_ylim(0.4, k + 1.1)
        ax.axis("off")
        ax.text(n / 2, 0.45, "dark = validation fold, light = training folds", ha="center", fontsize=6.5)

    return draw


@template(TOPIC, S_CV, marks=2, qtype="NAT")
def cv_kfold_error(rng):
    v = int(rng.integers(3))
    k = int(rng.choice([4, 5]))
    if v < 2:
        while True:
            sizes = list(rng.integers(8, 21, k))
            if len(set(sizes)) > 1:
                break
        n = int(sum(sizes))
        mses = np.round(rng.uniform(1.5, 9, k), 1)
        sse = np.array(sizes) * mses
        pooled = sse.sum() / n
        if v == 0:
            ans = pooled
            rows = [["Fold"] + [f"F{j + 1}" for j in range(k)], ["size"] + [str(s) for s in sizes],
                    ["validation MSE"] + [fmt(m, 1) for m in mses]]
            q = ("The k-fold CV estimate is defined as the mean squared error over all n out-of-fold predictions "
                 "(i.e. pooled over observations). Its value is")
            sol = ["Pooled CV MSE = Σ<sub>k</sub> n<sub>k</sub>·MSE<sub>k</sub> / n (a size-weighted average, not the "
                   "plain average of fold MSEs, since folds are unequal).",
                   "Σ n<sub>k</sub>MSE<sub>k</sub> = " + " + ".join(f"{s}×{fmt(m, 1)}" for s, m in zip(sizes, mses)) +
                   f" = {fmt(sse.sum(), 3)}; n = {n}.",
                   f"CV = {fmt(sse.sum(), 3)}/{n} = {fmt(pooled, 4)}  (plain average of fold MSEs = "
                   f"{fmt(mses.mean(), 4)} — a tempting but wrong value)."]
        else:
            ans = np.sqrt(pooled)
            sse = np.round(sse, 1)
            pooled = sse.sum() / n
            ans = np.sqrt(pooled)
            rows = [["Fold"] + [f"F{j + 1}" for j in range(k)], ["size"] + [str(s) for s in sizes],
                    ["sum of squared errors"] + [fmt(m, 1) for m in sse]]
            q = "The cross-validated root mean squared error (pooled over all n out-of-fold predictions) is"
            sol = [f"Total SSE = {' + '.join(fmt(m, 1) for m in sse)} = {fmt(sse.sum(), 2)}; n = {n}.",
                   f"CV MSE = {fmt(sse.sum(), 2)}/{n} = {fmt(pooled, 4)}; RMSE = √{fmt(pooled, 4)} = {fmt(ans, 4)}."]
        stem = (f"A regression model is evaluated by {k}-fold cross-validation on n = {n} observations. The folds "
                "(F1 … F" + str(k) + ") have unequal sizes, as shown in the diagram and table. ")
        blocks = [Figure(_fold_diagram(sizes), 9, 0.9 * k + 1.2), Table(rows, header=False)]
    else:
        G = 3
        lams = sorted(rng.choice([0.01, 0.1, 0.5, 1, 2, 5, 10], G, replace=False))
        while True:
            E = np.round(rng.uniform(2, 6, (G, k)), 1)
            m = E.mean(axis=1)
            s = np.sort(m)
            if s[1] - s[0] > 0.05:
                break
        best = int(np.argmin(m))
        ans = m[best]
        sizes = [10] * k
        n = 10 * k
        rows = [["λ"] + [f"Fold {j + 1}" for j in range(k)]] + [[fmt(l)] + [fmt(e, 1) for e in E[i]]
                                                                   for i, l in enumerate(lams)]
        stem = (f"Ridge regression is tuned by {k}-fold cross-validation (equal fold sizes) over λ ∈ "
                f"{{{', '.join(fmt(l) for l in lams)}}}. The validation MSE on each fold is shown. ")
        q = "The CV estimate (mean over folds) of the λ that would be selected is"
        sol = ["CV(λ) = average of the fold MSEs: " + "; ".join(f"λ = {fmt(l)}: {fmt(mm, 4)}" for l, mm in zip(lams, m)) + ".",
               f"Smallest CV error at λ = {fmt(lams[best])}: CV = {fmt(ans, 4)}."]
        blocks = [Table(rows), Figure(_fold_diagram(sizes), 9, 0.9 * k + 1.2)]
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=stem + q + " _______ " + nat_hint(2), qtype="NAT", marks=2, answer=nat_range(ans, 2, 0.01),
             nat_hint=nat_hint(2), blocks=blocks, solution=sol)


@template(TOPIC, S_CV, marks=2, qtype="NAT")
def loocv_shortcut(rng):
    x, y, f = _slr_data(rng, 5, 6, 10, r2min=0.4)
    n = len(x)
    h = 1 / n + (x - f["xm"]) ** 2 / f["sxx"]
    loo = f["e"] / (1 - h)
    # brute-force check
    for i in range(n):
        m = np.ones(n, bool)
        m[i] = False
        g = _ols1(x[m], y[m])
        assert abs((y[i] - (g["b0"] + g["b1"] * x[i])) - loo[i]) < 1e-8
    v = int(rng.integers(3))
    i = int(rng.integers(n))
    sol = _ols_solution_lines(x, y, f) + [
        "For a linear smoother, the leave-one-out residual is e<sub>(i)</sub> = e<sub>i</sub>/(1 − h<sub>ii</sub>), "
        "with h<sub>ii</sub> = 1/n + (x<sub>i</sub> − x̄)²/S<sub>xx</sub>.",
        Table([["x<sub>i</sub>"] + [fmt(t) for t in x], ["e<sub>i</sub>"] + [fmt(t, 3) for t in f["e"]],
               ["h<sub>ii</sub>"] + [fmt(t, 3) for t in h], ["e<sub>i</sub>/(1−h<sub>ii</sub>)"] +
               [fmt(t, 3) for t in loo]], header=False)]
    if v == 0:
        ans = loo[i]
        q = (f"the leave-one-out residual y<sub>i</sub> − ŷ<sub>(−i)</sub>(x<sub>i</sub>) for the point "
             f"({fmt(x[i])}, {fmt(y[i])}) — where ŷ<sub>(−i)</sub> is the line fitted without that point — is")
    elif v == 1:
        ans = y[i] - loo[i]
        q = (f"the prediction at x = {fmt(x[i])} made by the least-squares line fitted to the other {n - 1} points "
             "(i.e. with the point at that x left out) is")
        sol.append(f"ŷ<sub>(−i)</sub> = y<sub>i</sub> − e<sub>(i)</sub> = {fmt(y[i])} − ({fmt(loo[i], 4)}) = {fmt(ans, 4)}.")
    else:
        ans = (loo ** 2).mean()
        q = "the LOOCV estimate of test MSE, (1/n)Σ(y<sub>i</sub> − ŷ<sub>(−i)</sub>(x<sub>i</sub>))², is"
        sol.append(f"CV<sub>(n)</sub> = (1/{n})Σ(e<sub>i</sub>/(1−h<sub>ii</sub>))² = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b> (verified by explicitly refitting without the point).")
    return Q(text=f"A simple linear regression (with intercept) is fitted by least squares to the {n} points below. "
                  f"Using leave-one-out cross-validation, {q} _______ {nat_hint(2)}",
             qtype="NAT", marks=2, answer=_nat(ans, 2, base=0.02, rel=0.01), nat_hint=nat_hint(2),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y), 7.5, 4.3)], solution=sol)


@template(TOPIC, S_CV, marks=2, qtype="NAT")
def cv_simple_predictors(rng):
    v = int(rng.integers(3))
    while True:
        n = int(rng.integers(5, 7))
        x = np.sort(rng.choice(np.arange(1, 16), n, replace=False)).astype(float)
        y = rng.integers(1, 13, n).astype(float)
        D = np.abs(x[:, None] - x[None, :]) + np.diag([np.inf] * n)
        ok = all(np.sum(D[i] == D[i].min()) == 1 for i in range(n))
        if v == 1 and not ok:
            continue
        if np.ptp(y) >= 3:
            break
    sol = []
    if v == 0:
        ybar = y.mean()
        loo_pred = (y.sum() - y) / (n - 1)
        err = y - loo_pred
        ans = (err ** 2).mean()
        q = ("The model always predicts the mean of the training targets (ignoring x). Its leave-one-out "
             "cross-validation MSE is")
        sol = [f"Leaving out point i, the prediction is (Σy − y<sub>i</sub>)/(n − 1) with Σy = {fmt(y.sum())}.",
               Table([["y<sub>i</sub>"] + [fmt(t) for t in y], ["prediction"] + [fmt(t, 3) for t in loo_pred],
                      ["error"] + [fmt(t, 3) for t in err]], header=False),
               f"(Shortcut: error = n(y<sub>i</sub> − ȳ)/(n − 1), ȳ = {fmt(ybar, 4)}.) LOOCV MSE = mean of squared "
               f"errors = {fmt(ans, 4)}."]
    elif v == 1:
        nn = D.argmin(axis=1)
        err = y - y[nn]
        ans = (err ** 2).mean()
        q = ("A 1-nearest-neighbour regressor (prediction = y-value of the closest training x, |·| distance) is "
             "evaluated by leave-one-out cross-validation. The LOOCV MSE is")
        sol = ["For each left-out point, the prediction is the y of its nearest remaining neighbour (no ties here).",
               Table([["x<sub>i</sub>"] + [fmt(t) for t in x], ["nearest x"] + [fmt(x[j]) for j in nn],
                      ["prediction"] + [fmt(y[j]) for j in nn], ["error"] + [fmt(t) for t in err]], header=False),
               f"LOOCV MSE = (1/{n})Σ error² = {fmt((err ** 2).sum())}/{n} = {fmt(ans, 4)}."]
    else:
        A = np.arange(n) % 2 == 0
        B = ~A
        pa, pb = y[B].mean(), y[A].mean()
        sse = ((y[A] - pa) ** 2).sum() + ((y[B] - pb) ** 2).sum()
        ans = sse / n
        q = ("Two-fold cross-validation is used with fold 1 = {points 1, 3, 5, …} and fold 2 = {points 2, 4, …} "
             "(points numbered in increasing x). The model predicts the mean of the training-fold targets. The "
             "pooled 2-fold CV MSE (over all n points) is")
        sol = [f"Fold 1 validated with mean of fold-2 targets = {fmt(pa, 4)}; fold 2 validated with mean of fold-1 "
               f"targets = {fmt(pb, 4)}.",
               f"Σ squared errors = {fmt(sse, 4)}; pooled MSE = {fmt(sse, 4)}/{n} = {fmt(ans, 4)}."]
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"Consider the {n} training points (x<sub>i</sub>, y<sub>i</sub>) shown below. " + q + " _______ " +
                  nat_hint(2), qtype="NAT", marks=2, answer=_nat(ans, 2, base=0.01), nat_hint=nat_hint(2),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y, labels=[str(i + 1) for i in range(n)]), 7.5, 4.2)],
             solution=sol)


@template(TOPIC, S_GD, marks=2, qtype="NAT")
def gd_two_steps(rng):
    while True:
        n = int(rng.integers(3, 5))
        x = np.sort(rng.choice(np.arange(0, 5), n, replace=False)).astype(float)
        y = rng.integers(-1, 9, n).astype(float)
        half = rng.random() < 0.5
        c = (1 / n) if half else (2 / n)
        X = np.c_[np.ones(n), x]
        Hm = c * X.T @ X
        eta = float(rng.choice([0.01, 0.02, 0.05, 0.1]))
        if eta * np.linalg.eigvalsh(Hm).max() < 1.6 and np.ptp(y) > 1:
            break
    while True:
        w = np.array([float(rng.integers(-1, 2)), float(rng.integers(-1, 2))])
        g1 = c * X.T @ (X @ w - y)
        if np.all(np.abs(g1) > 0.4):
            break
    hist = [w.copy()]
    grads = []
    for _ in range(2):
        r = X @ w - y
        g = c * X.T @ r
        grads.append((r.copy(), g.copy()))
        w = w - eta * g
        hist.append(w.copy())
    J = lambda ww: (0.5 if half else 1.0) / n * ((X @ ww - y) ** 2).sum()
    v = int(rng.integers(4))
    lossdef = "J(w) = (1/2n)Σ(w<sub>0</sub> + w<sub>1</sub>x<sub>i</sub> − y<sub>i</sub>)²" if half else \
        "J(w) = (1/n)Σ(w<sub>0</sub> + w<sub>1</sub>x<sub>i</sub> − y<sub>i</sub>)²"
    gdef = "(1/n)" if half else "(2/n)"
    sol = [f"∂J/∂w<sub>0</sub> = {gdef}Σr<sub>i</sub>, ∂J/∂w<sub>1</sub> = {gdef}Σr<sub>i</sub>x<sub>i</sub>, with "
           "residual r<sub>i</sub> = w<sub>0</sub> + w<sub>1</sub>x<sub>i</sub> − y<sub>i</sub>."]
    steps = 2 if v == 2 else 1
    for t in range(steps):
        r, g = grads[t]
        sol.append(f"Step {t + 1}: w = ({fmt(hist[t][0], 4)}, {fmt(hist[t][1], 4)}), r = ({', '.join(fmt(z, 4) for z in r)}), "
                   f"∇J = ({fmt(g[0], 4)}, {fmt(g[1], 4)}) ⇒ w ← w − {fmt(eta)}∇J = "
                   f"({fmt(hist[t + 1][0], 4)}, {fmt(hist[t + 1][1], 4)}).")
    if v == 0:
        ans, q = hist[1][1], "the value of w<sub>1</sub> after one iteration is"
    elif v == 1:
        ans, q = hist[1][0], "the value of w<sub>0</sub> after one iteration is"
    elif v == 2:
        ans, q = hist[2][1], "the value of w<sub>1</sub> after two iterations is"
    else:
        ans = J(hist[1])
        q = "the loss J(w) after one iteration is"
        sol.append(f"J = {fmt(ans, 4)} (initial loss {fmt(J(hist[0]), 4)}).")
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"A linear model ŷ = w<sub>0</sub> + w<sub>1</sub>x is trained on the {n} points below by batch "
                  f"gradient descent on the loss {lossdef}, starting from (w<sub>0</sub>, w<sub>1</sub>) = "
                  f"({fmt(hist[0][0])}, {fmt(hist[0][1])}) with learning rate η = {fmt(eta)}. Then {q} _______ "
                  f"{nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.002, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y), 7, 4)], solution=sol)


@template(TOPIC, S_GD, marks=2, qtype="NAT")
def sgd_updates(rng):
    while True:
        X = rng.integers(-2, 4, (2, 2)).astype(float)
        if (X != 0).any(axis=1).all():
            break
    y = rng.integers(-3, 7, 2).astype(float)
    eta = float(rng.choice([0.05, 0.1, 0.2]))
    w = rng.integers(-1, 2, 2).astype(float)
    b = float(rng.integers(-1, 2))
    w0, b0 = w.copy(), b
    lines = []
    for t in range(2):
        yh = w @ X[t] + b
        r = yh - y[t]
        gw, gb = r * X[t], r
        w = w - eta * gw
        b = b - eta * gb
        lines.append(f"Example {t + 1}: ŷ = {fmt(yh, 4)}, error ŷ − y = {fmt(r, 4)}; ∇<sub>w</sub> = ({fmt(gw[0], 4)}, "
                     f"{fmt(gw[1], 4)}), ∇<sub>b</sub> = {fmt(gb, 4)} ⇒ w = ({fmt(w[0], 4)}, {fmt(w[1], 4)}), "
                     f"b = {fmt(b, 4)}.")
    v = int(rng.integers(4))
    if v < 2:
        ans, q = w[v], f"w<sub>{v + 1}</sub>"
    elif v == 2:
        ans, q = b, "b"
    else:
        xn = rng.integers(-1, 3, 2).astype(float)
        ans = w @ xn + b
        q = f"the model's prediction for x = ({fmt(xn[0])}, {fmt(xn[1])})"
        lines.append(f"ŷ = {fmt(w[0], 4)}×{fmt(xn[0])} + {fmt(w[1], 4)}×{fmt(xn[1])} + {fmt(b, 4)} = {fmt(ans, 4)}.")
    sol = ["Per-example loss ℓ = ½(ŷ − y)² ⇒ ∂ℓ/∂w = (ŷ − y)x, ∂ℓ/∂b = (ŷ − y). Update after each example."] + lines
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    rows = [["example", "x<sub>1</sub>", "x<sub>2</sub>", "y"]] + [[str(t + 1), fmt(X[t, 0]), fmt(X[t, 1]), fmt(y[t])]
                                                                for t in range(2)]
    return Q(text=f"A linear model ŷ = w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + b is trained by "
                  f"stochastic gradient descent (batch size 1) on the per-example loss ½(ŷ − y)² with learning rate "
                  f"η = {fmt(eta)}, starting from w = ({fmt(w0[0])}, {fmt(w0[1])}), b = {fmt(b0)}. The two examples "
                  f"below are processed once, in the given order. After both updates, the value of {q} is _______ "
                  f"{nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.002, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[Table(rows)], solution=sol)


@template(TOPIC, S_GD, marks=2, qtype="NAT")
def gd_step_size_bound(rng):
    a, b = sorted(rng.choice([2, 4, 6, 8, 10, 12, 16, 20], 2, replace=False))[::-1]
    a, b = float(a), float(b)
    XtX = np.array([[(a + b) / 2, (a - b) / 2], [(a - b) / 2, (a + b) / 2]])
    n = int(rng.choice([2, 4, 5, 8, 10]))
    half = rng.random() < 0.5
    c = 1 / n if half else 2 / n
    L, mu = c * a, c * b
    v = int(rng.integers(3))
    lossdef = "J(w) = (1/2n)‖Xw − y‖²" if half else "J(w) = (1/n)‖Xw − y‖²"
    sol = [f"Hessian of J: ∇²J = {'(1/n)' if half else '(2/n)'}XᵀX. Eigenvalues of XᵀX: "
           f"{fmt((a + b) / 2)} ± {fmt((a - b) / 2)} = {fmt(a)}, {fmt(b)} (eigenvectors (1, 1), (1, −1)).",
           f"So the Hessian eigenvalues are L = {fmt(L, 4)} and μ = {fmt(mu, 4)}.",
           "GD error evolves as w<sub>t+1</sub> − w* = (I − η∇²J)(w<sub>t</sub> − w*), so it converges iff "
           "|1 − ηλ| &lt; 1 for every Hessian eigenvalue λ."]
    if v == 0:
        ans = 2 / L
        q = ("the supremum of learning rates η for which batch gradient descent converges from every starting "
             "point is")
        sol.append(f"Need η &lt; 2/L = 2/{fmt(L, 4)} = {fmt(ans, 4)}.")
    elif v == 1:
        ans = 2 / (L + mu)
        q = ("the constant learning rate η that minimises the worst-case contraction factor "
             "max<sub>i</sub>|1 − ηλ<sub>i</sub>| is")
        sol.append(f"Balance |1 − ηL| = |1 − ημ| ⇒ η* = 2/(L + μ) = 2/({fmt(L, 4)} + {fmt(mu, 4)}) = {fmt(ans, 4)}.")
    else:
        eta = round(float(rng.uniform(0.3, 1.8)) / L, 3)
        rho = max(abs(1 - eta * L), abs(1 - eta * mu))
        ans = rho
        q = (f"with η = {fmt(eta, 3)}, the contraction factor ρ = max<sub>i</sub>|1 − ηλ<sub>i</sub>| "
             "(so that ‖w<sub>t+1</sub> − w*‖ ≤ ρ‖w<sub>t</sub> − w*‖) is")
        sol.append(f"|1 − {fmt(eta, 3)}×{fmt(L, 4)}| = {fmt(abs(1 - eta * L), 4)}, |1 − {fmt(eta, 3)}×{fmt(mu, 4)}| = "
                   f"{fmt(abs(1 - eta * mu), 4)}; ρ = {fmt(rho, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"Least-squares linear regression on n = {n} observations minimises {lossdef} by batch gradient "
                  f"descent with constant learning rate η. The data give the matrix XᵀX below. Then {q} _______ "
                  f"{nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.002, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[Matrix("XᵀX", XtX, 2)], solution=sol)


@template(TOPIC, S_MLE, marks=2, qtype="NAT")
def mle_sigma_estimate(rng):
    x, y, f = _slr_data(rng, 5, 7, 10, r2min=0.3)
    while f["sse"] < 1:
        x, y, f = _slr_data(rng, 5, 7, 10, r2min=0.3)
    n = len(x)
    sse = f["sse"]
    v = int(rng.integers(4))
    sol = _ols_solution_lines(x, y, f) + [
        f"SSE = S<sub>yy</sub> − S<sub>xy</sub>²/S<sub>xx</sub> = {fmt(f['sst'], 4)} − {fmt(f['ssr'], 4)} = {fmt(sse, 4)}."]
    if v == 0:
        ans = sse / n
        q = "the maximum-likelihood estimate of σ² is"
        sol.append(f"Maximising the Gaussian likelihood over σ² gives σ̂²<sub>ML</sub> = SSE/n = {fmt(sse, 4)}/{n} = "
                   f"{fmt(ans, 4)}.")
    elif v == 1:
        ans = sse / (n - 2)
        q = "the unbiased estimate s² = SSE/(n − 2) of σ² is"
        sol.append(f"Two parameters are estimated, so s² = SSE/(n − 2) = {fmt(sse, 4)}/{n - 2} = {fmt(ans, 4)}.")
    elif v == 2:
        ans = sse / (n - 2) - sse / n
        q = "the difference between the unbiased estimate SSE/(n − 2) and the maximum-likelihood estimate of σ² is"
        sol.append(f"SSE/(n − 2) − SSE/n = {fmt(sse / (n - 2), 4)} − {fmt(sse / n, 4)} = {fmt(ans, 4)}.")
    else:
        s2 = sse / n
        ans = -n / 2 * (np.log(2 * np.pi * s2) + 1)
        q = ("the maximised log-likelihood ln L(β̂, σ̂²) (natural log, with σ̂² the maximum-likelihood estimate) is")
        sol.append("ln L = −(n/2)ln(2πσ²) − SSE/(2σ²). At σ̂² = SSE/n: ln L = −(n/2)[ln(2πσ̂²) + 1].")
        sol.append(f"σ̂² = {fmt(s2, 4)} ⇒ ln L = −({n}/2)[ln(2π×{fmt(s2, 4)}) + 1] = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"Assume y<sub>i</sub> = β<sub>0</sub> + β<sub>1</sub>x<sub>i</sub> + ε<sub>i</sub> with "
                  f"ε<sub>i</sub> i.i.d. N(0, σ²). For the {n} observations below, with β estimated by least squares "
                  f"(= maximum likelihood), {q} _______ {nat_hint(2)}",
             qtype="NAT", marks=2, answer=_nat(ans, 2, base=0.02, rel=0.006), nat_hint=nat_hint(2),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y), 7, 4.2)], solution=sol)


@template(TOPIC, S_MLE, marks=2, qtype="NAT")
def map_estimate_1d(rng):
    while True:
        n = 4
        x = rng.integers(-2, 5, n).astype(float)
        y = rng.integers(-3, 9, n).astype(float)
        Sxx, Sxy = (x * x).sum(), (x * y).sum()
        if Sxx > 0 and abs(Sxy) > 2:
            break
    s2 = float(rng.choice([1, 2, 4]))
    v = int(rng.integers(3))
    sol = []
    if v < 2:
        t2 = float(rng.choice([0.25, 0.5, 1, 2]))
        lam = s2 / t2
        wmap = Sxy / (Sxx + lam)
        wml = Sxy / Sxx
        prior = f"w ~ N(0, τ²) with τ² = {fmt(t2)}"
        sol = ["−ln p(w | data) = (1/(2σ²))Σ(y<sub>i</sub> − wx<sub>i</sub>)² + w²/(2τ²) + const.",
               f"Multiplying by 2σ²: Σ(y<sub>i</sub> − wx<sub>i</sub>)² + (σ²/τ²)w² — ridge with λ = σ²/τ² = {fmt(lam, 4)}.",
               f"Σx<sub>i</sub>² = {fmt(Sxx)}, Σx<sub>i</sub>y<sub>i</sub> = {fmt(Sxy)}; "
               f"ŵ<sub>MAP</sub> = Σxy/(Σx² + λ) = {fmt(Sxy)}/({fmt(Sxx)} + {fmt(lam, 4)}) = {fmt(wmap, 4)}."]
        if v == 0:
            ans, q = wmap, "the MAP estimate of w is"
        else:
            ans = wml - wmap
            q = "ŵ<sub>ML</sub> − ŵ<sub>MAP</sub> is"
            sol.append(f"ŵ<sub>ML</sub> = Σxy/Σx² = {fmt(wml, 4)}; difference = {fmt(ans, 4)}.")
    else:
        bb = float(rng.choice([0.25, 0.5, 1, 2]))
        thr = s2 / bb
        while abs(abs(Sxy) - thr) < 0.5:
            bb = float(rng.choice([0.25, 0.5, 1, 2]))
            thr = s2 / bb
            if abs(abs(Sxy) - thr) < 0.5:
                s2 = float(rng.choice([1, 2, 4]))
                thr = s2 / bb
        wmap = np.sign(Sxy) * max(abs(Sxy) - thr, 0) / Sxx
        ans = wmap
        prior = f"w has a Laplace prior p(w) ∝ exp(−|w|/b) with b = {fmt(bb)}"
        q = "the MAP estimate of w is"
        sol = ["−ln p(w | data) = (1/(2σ²))Σ(y<sub>i</sub> − wx<sub>i</sub>)² + |w|/b + const. Multiply by 2σ²: "
               "Σ(y<sub>i</sub> − wx<sub>i</sub>)² + (2σ²/b)|w| (lasso).",
               f"Σx<sub>i</sub>² = {fmt(Sxx)}, Σx<sub>i</sub>y<sub>i</sub> = {fmt(Sxy)}. Setting the subgradient to 0: "
               "Σx²·w = Σxy − (σ²/b)·sign(w) ⇒ ŵ = sign(Σxy)·max(|Σxy| − σ²/b, 0)/Σx².",
               f"σ²/b = {fmt(thr, 4)}; ŵ = {fmt(np.sign(Sxy), 0)}×max({fmt(abs(Sxy))} − {fmt(thr, 4)}, 0)/{fmt(Sxx)} = "
               f"{fmt(wmap, 4)}" + (" — the slope is thresholded exactly to 0." if wmap == 0 else ".")]
    sol.append(f"Answer: <b>{fmt(ans, 3)}</b>.")
    return Q(text=f"Consider the model y = wx + ε with ε ~ N(0, σ²), σ² = {fmt(s2)}, and {prior}. Given the four "
                  f"observations below, {q} _______ {nat_hint(3)}",
             qtype="NAT", marks=2, answer=nat_range(ans, 3, max(0.002, 0.003 * abs(ans))), nat_hint=nat_hint(3),
             blocks=[_xy_table(x, y)], solution=sol)


@template(TOPIC, S_POLY, marks=2, qtype="NAT")
def quadratic_fit(rng):
    n = int(rng.choice([5, 7]))
    h = (n - 1) // 2
    x = np.arange(-h, h + 1).astype(float)
    a0, b0_, c0 = float(rng.integers(-2, 6)), float(rng.integers(-2, 3)), float(rng.choice([-1.5, -1, -0.5, 0.5, 1, 1.5]))
    y = np.round(a0 + b0_ * x + c0 * x ** 2 + rng.integers(-2, 3, n)).astype(float)
    S2, S4 = (x ** 2).sum(), (x ** 4).sum()
    Sy, Sxy, Sx2y = y.sum(), (x * y).sum(), (x * x * y).sum()
    b = Sxy / S2
    M = np.array([[n, S2], [S2, S4]])
    a, c = np.linalg.solve(M, [Sy, Sx2y])
    v = int(rng.integers(4))
    if v == 0:
        ans, q = c, "the coefficient c of x²"
    elif v == 1:
        ans, q = a, "the intercept a"
    elif v == 2:
        ans, q = b, "the coefficient b of x"
    else:
        x0 = float(rng.choice([-h - 1, h + 1, 0.5, -0.5, 1.5]))
        ans = a + b * x0 + c * x0 * x0
        q = f"the fitted value ŷ at x = {fmt(x0)}"
    sol = ["Design columns 1, x, x². Because the x-values are symmetric about 0, Σx = Σx³ = 0, so the normal "
           "equations decouple:",
           f"Σx² = {fmt(S2)}, Σx⁴ = {fmt(S4)}, Σy = {fmt(Sy)}, Σxy = {fmt(Sxy)}, Σx²y = {fmt(Sx2y)}.",
           f"b = Σxy/Σx² = {fmt(Sxy)}/{fmt(S2)} = {fmt(b, 4)}.",
           f"[n, Σx²; Σx², Σx⁴][a; c] = [Σy; Σx²y] ⇒ {n}a + {fmt(S2)}c = {fmt(Sy)},  {fmt(S2)}a + {fmt(S4)}c = {fmt(Sx2y)}.",
           f"Solving: c = (nΣx²y − Σx²Σy)/(nΣx⁴ − (Σx²)²) = {fmt(c, 4)}, a = (Σy − cΣx²)/n = {fmt(a, 4)}."]
    if v == 3:
        sol.append(f"ŷ({fmt(x0)}) = {fmt(a, 4)} + ({fmt(b, 4)})({fmt(x0)}) + ({fmt(c, 4)})({fmt(x0)})² = {fmt(ans, 4)}.")
    sol.append(f"Answer: <b>{fmt(ans, 2)}</b>.")
    return Q(text=f"The quadratic model y = a + bx + cx² is fitted by least squares to the {n} points below "
                  f"(a polynomial / basis-function regression with basis 1, x, x²). Then {q} is _______ {nat_hint(2)}",
             qtype="NAT", marks=2, answer=_nat(ans, 2, base=0.02, rel=0.006), nat_hint=nat_hint(2),
             blocks=[_xy_table(x, y), Figure(_scatter(x, y), 7, 4.2)], solution=sol)


UNIT_CHANGES = [("hours", "minutes", 60), ("kilograms", "grams", 1000), ("metres", "centimetres", 100),
                ("thousands of rupees", "rupees", 1000), ("kilometres", "metres", 1000)]


@template(TOPIC, S_POLY, marks=2, qtype="NAT")
def feature_rescaling(rng):
    v = int(rng.integers(4))
    a = float(rng.integers(-50, 151)) / 10
    b = float(rng.choice([-1, 1]) * rng.integers(5, 60)) / 10
    if v == 0:
        xm = float(rng.integers(10, 60))
        sx = float(rng.integers(2, 13))
        tgt = rng.random() < 0.5
        ans = (a + b * xm) if tgt else b * sx
        q = ("After standardising x as z = (x − x̄)/s<sub>x</sub>, with x̄ = " + fmt(xm) + " and s<sub>x</sub> = " +
             fmt(sx) + ", the model is refitted as ŷ = γ<sub>0</sub> + γ<sub>1</sub>z. The value of " +
             ("γ<sub>0</sub>" if tgt else "γ<sub>1</sub>") + " is")
        sol = ["Since x = x̄ + s<sub>x</sub>z, ŷ = β<sub>0</sub> + β<sub>1</sub>x̄ + β<sub>1</sub>s<sub>x</sub>z, and OLS "
               "with intercept is equivariant under affine maps of x (same fitted values).",
               f"γ<sub>0</sub> = β<sub>0</sub> + β<sub>1</sub>x̄ = {fmt(a)} + ({fmt(b)})({fmt(xm)}) = {fmt(a + b * xm, 4)} "
               "(= ȳ, since z is centred);",
               f"γ<sub>1</sub> = β<sub>1</sub>s<sub>x</sub> = ({fmt(b)})({fmt(sx)}) = {fmt(b * sx, 4)}."]
    elif v == 1:
        big, small, k = UNIT_CHANGES[int(rng.integers(len(UNIT_CHANGES)))]
        b = float(rng.choice([-1, 1]) * rng.integers(5, 400)) / 10
        ans = b / k
        q = (f"The feature x was measured in {big}. If x is re-expressed in {small} (so x′ = {k}x) and the model is "
             "refitted, the new slope is")
        sol = [f"x = x′/{k} ⇒ ŷ = β<sub>0</sub> + (β<sub>1</sub>/{k})x′. Fitted values are unchanged; the slope becomes "
               f"{fmt(b)}/{k} = {fmt(ans, 5)}."]
    elif v == 2:
        tgt = rng.random() < 0.5
        ans = 1.8 * a + 32 if tgt else 1.8 * b
        q = ("The response y is in °C. If y is converted to °F (y′ = 1.8y + 32) and the model is refitted, the new " +
             ("intercept" if tgt else "slope") + " is")
        sol = ["The OLS coefficients transform linearly with y: β′<sub>0</sub> = 1.8β<sub>0</sub> + 32, "
               "β′<sub>1</sub> = 1.8β<sub>1</sub>.",
               f"β′<sub>0</sub> = 1.8×{fmt(a)} + 32 = {fmt(1.8 * a + 32, 4)};  β′<sub>1</sub> = 1.8×{fmt(b)} = {fmt(1.8 * b, 4)}."]
    else:
        sx = float(rng.integers(2, 15))
        sy = float(rng.integers(5, 60))
        ans = b * sx / sy
        q = (f"The sample standard deviations are s<sub>x</sub> = {fmt(sx)} and s<sub>y</sub> = {fmt(sy)}. If both x and "
             "y are z-score standardised and the regression is refitted, the new slope (the standardised coefficient) is")
        sol = [f"Standardising y divides the slope by s<sub>y</sub>; standardising x multiplies it by s<sub>x</sub>: "
               f"β* = β<sub>1</sub>s<sub>x</sub>/s<sub>y</sub> = {fmt(b)}×{fmt(sx)}/{fmt(sy)} = {fmt(ans, 4)} "
               "(this equals the correlation r in simple regression)."]
    d = 4 if (v == 1 and abs(ans) < 0.1) else (3 if abs(ans) < 1 else 2)
    sol.append(f"Answer: <b>{fmt(ans, d)}</b>.")
    return Q(text=f"A simple linear regression fitted by ordinary least squares gives ŷ = {fmt(a)} "
                  f"{'+' if b >= 0 else '−'} {fmt(abs(b))}x. {q} _______ {nat_hint(d)}",
             qtype="NAT", marks=2, answer=nat_range(ans, d, max(10 ** (-d), 0.002 * abs(ans))), nat_hint=nat_hint(d),
             solution=sol)


@template(TOPIC, S_CV, marks=2, qtype="MCQ")
def one_standard_error_rule(rng):
    while True:
        lams = [0.01, 0.1, 0.3, 1, 3, 10]
        K = len(lams)
        imin = int(rng.integers(1, 4))
        cv = np.empty(K)
        cv[imin] = round(float(rng.uniform(3, 6)), 2)
        for i in range(imin - 1, -1, -1):
            cv[i] = round(cv[i + 1] + float(rng.uniform(0.05, 0.5)), 2)
        for i in range(imin + 1, K):
            cv[i] = round(cv[i - 1] + float(rng.uniform(0.05, 0.6)) * (1 + 0.6 * (i - imin)), 2)
        se = np.round(rng.uniform(0.15, 0.5, K), 2)
        thr = cv[imin] + se[imin]
        within = [i for i in range(K) if cv[i] <= thr]
        pick = max(within)  # largest λ = simplest model
        if pick != imin and all(abs(cv[i] - thr) > 0.03 for i in range(K)):
            break
    rule = rng.random() < 0.75
    ans_i = pick if rule else imin
    labels = [f"λ = {fmt(l)}" for l in lams]
    opts, a = mcq(rng, labels[ans_i], [labels[i] for i in range(K) if i != ans_i])
    rows = [["λ"] + [fmt(l) for l in lams], ["CV MSE"] + [fmt(c) for c in cv], ["SE"] + [fmt(s) for s in se]]
    q = ("the <b>one-standard-error rule</b> (choose the most regularised model whose CV error is within one standard "
         "error of the minimum CV error)" if rule else "the rule <b>minimum CV error</b>")
    sol = [f"Minimum CV MSE = {fmt(cv[imin])} at λ = {fmt(lams[imin])}, with SE = {fmt(se[imin])}.",
           f"One-SE threshold = {fmt(cv[imin])} + {fmt(se[imin])} = {fmt(thr)}.",
           "Models within the threshold: " + ", ".join(f"λ = {fmt(lams[i])} ({fmt(cv[i])})" for i in within) + ".",
           f"The one-SE rule picks the largest such λ (simplest model): λ = {fmt(lams[pick])}; the minimum-CV rule "
           f"picks λ = {fmt(lams[imin])}.",
           f"Answer: <b>{labels[ans_i]}</b>."]
    return Q(text="Ridge regression is tuned by 10-fold cross-validation. For each λ the table gives the mean CV MSE "
                  "and its standard error (SE) across folds. (Larger λ means a simpler, more regularised model.) "
                  f"Using {q}, the selected value is",
             qtype="MCQ", marks=2, options=opts, answer=a, blocks=[Table(rows, header=False)], solution=sol)
