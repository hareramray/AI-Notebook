"""Cover, introduction, revision notes (with diagrams) and master answer key."""
from __future__ import annotations

from collections import Counter

import numpy as np
from reportlab.lib.units import cm
from reportlab.platypus import CondPageBreak, KeepTogether, PageBreak, Paragraph, Spacer

from core import Figure, Table
from render import S, answer_text, block_flowables

P = lambda t, s="body": Paragraph(t, S[s])  # noqa: E731


# ----------------------------------------------------------------------------
# Cover page body (below the maroon banner)
# ----------------------------------------------------------------------------
def cover_story(all_sets, mods):
    nq = sum(len(s) for s in all_sets)
    nm = sum(q.marks for s in all_sets for q in s)
    types = Counter(q.qtype for s in all_sets for q in s)
    nfig = sum(1 for s in all_sets for q in s if any(isinstance(b, Figure) for b in q.blocks))
    out = [Spacer(1, 6),
           P("<b>What is inside</b>", "h3"),
           P(f"• <b>{len(all_sets)} mock tests</b>, each with 35 questions worth 55 marks (15 one-mark + 20 two-mark), "
             f"the same weight the subject part of a GATE DA paper carries.<br/>"
             f"• <b>{nq} questions</b> in total ({types['MCQ']} MCQ, {types['MSQ']} MSQ, {types['NAT']} NAT), "
             f"{nm} marks, with <b>{nfig} questions built around a diagram</b>: scatter plots, decision boundaries, "
             f"trees, network graphs, dendrograms, ROC curves and loss curves.<br/>"
             f"• Every test has an <b>answer key</b>, a <b>self-evaluation sheet</b> and <b>step-by-step solutions</b>. "
             f"MSQ solutions explain every option.<br/>"
             f"• A <b>concept and formula revision section</b> with diagrams, and a <b>master answer key</b> at the end."),
           Spacer(1, 10),
           P("<b>Syllabus coverage (GATE DA, Section 6: Machine Learning)</b>", "h3"),
           P("<b>Supervised learning:</b> regression and classification problems, simple linear regression, multiple "
             "linear regression, ridge regression, logistic regression, k-nearest neighbour, naive Bayes classifier, "
             "linear discriminant analysis, support vector machine, decision trees, bias-variance trade-off, "
             "cross-validation methods such as leave-one-out (LOO) cross-validation and k-fold cross-validation, "
             "multi-layer perceptron, feed-forward neural network.<br/>"
             "<b>Unsupervised learning:</b> clustering algorithms, k-means/k-medoid, hierarchical clustering, "
             "top-down, bottom-up: single-linkage, multiple-linkage, dimensionality reduction, principal component "
             "analysis."),
           Spacer(1, 10),
           P("Every question is generated from a parameterised template whose answer is <b>computed in code</b>, "
             "so the numerical keys are exact. NAT keys are given as an accepted range around the exact value.",
             "small")]
    return out


# ----------------------------------------------------------------------------
# Introduction
# ----------------------------------------------------------------------------
def intro_story(all_sets, SetHeader):
    out = [SetHeader("How to use this book", "How to use this book", 0, key="intro"),
           P("How to use this book", "h1"),
           P("The GATE DA exam", "h2"),
           P("GATE Data Science and Artificial Intelligence (DA) is a 3-hour computer-based test of 65 questions "
             "worth 100 marks: 10 General Aptitude questions (15 marks) and 55 subject questions (85 marks). "
             "Questions are of three kinds:"),
           ]
    rows = [["Type", "What you do", "Marks", "Negative marking"],
            ["MCQ: multiple choice", "Pick the one correct option out of four", "1 or 2",
             "−⅓ (1-mark), −⅔ (2-mark)"],
            ["MSQ: multiple select", "Pick ALL correct options (one or more out of four). There is no partial credit.",
             "1 or 2", "None"],
            ["NAT: numerical answer", "Type a number; it is accepted if it lies in the given range", "1 or 2", "None"]]
    out += block_flowables(Table(rows, col_widths_cm=[3.6, 7.0, 1.6, 3.8]))
    out += [P("Machine Learning is the largest single block of the DA paper, so these tests concentrate on it. "
              "Each mock test is a <b>sectional test</b> of 35 questions worth 55 marks (15 × 1 mark + 20 × 2 marks), "
              "to be done in <b>100 minutes</b>. That is the same marks-per-minute pace as the real exam."),
            P("Suggested routine", "h2"),
            P("1. Read the revision notes once and mark the formulas you are unsure of.<br/>"
              "2. Take one test at a time under exam conditions: timer on, phone away, and a basic calculator "
              "only (GATE gives you an on-screen scientific calculator).<br/>"
              "3. Mark your answers on a separate sheet. Use the answer key and the negative-marking rules to "
              "work out your score.<br/>"
              "4. Read the detailed solution for <b>every</b> question, including the ones you got right. "
              "The MSQ explanations also say why each wrong statement is wrong, which is usually the trap.<br/>"
              "5. Fill in the self-evaluation table. After every 5 tests, look across them for weak topics and "
              "re-read those parts of the notes.<br/>"
              "6. In the last few weeks, re-attempt the tests you scored lowest on."),
            P("Exam-day strategy", "h2"),
            P("• <b>NAT and MSQ have no negative marks</b>, so never leave them blank. For a NAT, an educated "
              "estimate costs nothing.<br/>"
              "• Answer an MCQ only if you can rule out at least two options. A blind guess loses marks on average "
              "(expected value ¼·1 − ¾·⅓ = 0).<br/>"
              "• For MSQ, judge each option on its own as true or false. Questions often have 2 or 3 correct "
              "options.<br/>"
              "• Watch the rounding instruction on NAT questions. Do the arithmetic at full precision and round "
              "only at the end.<br/>"
              "• In computation questions, watch these common slips: n vs n−1 (variance), log base (entropy uses "
              "log₂ unless told otherwise), squared vs non-squared distance, and whether the bias term is "
              "included in parameter counts.")]
    # Topic distribution over the whole book
    tm, tq = Counter(), Counter()
    sub = Counter()
    for s in all_sets:
        for q in s:
            tm[q.topic] += q.marks
            tq[q.topic] += 1
            sub[(q.topic, q.subtopic)] += 1
    out += [CondPageBreak(8 * cm), P("Coverage across all tests", "h2")]
    rows = [["Topic area", "Questions", "Marks"]] + [[t, str(tq[t]), str(tm[t])] for t in tq]
    out += block_flowables(Table(rows, col_widths_cm=[10, 3, 3]))
    rows = [["Topic area", "Sub-topic", "Questions"]]
    for (t, st), c in sorted(sub.items()):
        rows.append([t, st, str(c)])
    out += [P("Sub-topic frequency", "h3")]
    out += block_flowables(Table(rows, col_widths_cm=[6.5, 7.5, 2.0]))
    out.append(PageBreak())
    return out


# ----------------------------------------------------------------------------
# Revision notes with diagrams
# ----------------------------------------------------------------------------
def _fig_bias_variance(fig):
    ax = fig.add_subplot(111)
    c = np.linspace(0.5, 10, 200)
    bias2 = 4 / c
    var = 0.06 * c ** 1.6
    noise = np.full_like(c, 0.6)
    ax.plot(c, bias2, label="Bias²", lw=1.6)
    ax.plot(c, var, label="Variance", lw=1.6)
    ax.plot(c, noise, "--", label="Irreducible error σ²", lw=1)
    ax.plot(c, bias2 + var + noise, "k", label="Expected test error", lw=2)
    ax.plot(c, 3.2 * np.exp(-c / 2.2) + 0.25, ":", color="gray", label="Training error", lw=1.6)
    ax.set_ylim(0, 6)
    ax.set_xlabel("Model complexity  →")
    ax.set_ylabel("Error")
    ax.legend(frameon=False, fontsize=6.5)
    ax.set_xticks([])


def _fig_losses(fig):
    ax = fig.add_subplot(111)
    m = np.linspace(-2.5, 3, 300)
    ax.plot(m, (m < 0).astype(float), label="0–1 loss", lw=1.6)
    ax.plot(m, np.maximum(0, 1 - m), label="Hinge (SVM)", lw=1.6)
    ax.plot(m, np.log2(1 + np.exp(-m)), label="Logistic (log₂ scale)", lw=1.6)
    ax.plot(m, (1 - m) ** 2, label="Squared (1 − m)²", lw=1.2, ls="--")
    ax.set_ylim(0, 4)
    ax.set_xlabel("margin  m = y·f(x)")
    ax.set_ylabel("loss")
    ax.legend(frameon=False)
    ax.grid(alpha=.3)


def _fig_activations(fig):
    z = np.linspace(-4, 4, 300)
    ax = fig.add_subplot(111)
    ax.plot(z, 1 / (1 + np.exp(-z)), label="sigmoid σ(z)")
    ax.plot(z, np.tanh(z), label="tanh(z)")
    ax.plot(z, np.maximum(0, z), label="ReLU")
    ax.plot(z, np.where(z > 0, z, 0.1 * z), ls="--", label="leaky ReLU (0.1)")
    ax.set_ylim(-1.3, 3)
    ax.axhline(0, color="k", lw=.5)
    ax.axvline(0, color="k", lw=.5)
    ax.legend(frameon=False)
    ax.set_xlabel("z")
    ax.grid(alpha=.3)


def _fig_svm(fig):
    ax = fig.add_subplot(111)
    rng = np.random.default_rng(3)
    a = rng.normal([1, 1], .45, (14, 2))
    b = rng.normal([3.4, 3.2], .45, (14, 2))
    a = a[(a.sum(1) < 3.3)]
    b = b[(b.sum(1) > 5.3)]
    ax.scatter(*a.T, marker="o", facecolor="white", edgecolor="k", label="y = −1")
    ax.scatter(*b.T, marker="s", color="k", label="y = +1")
    xs = np.linspace(-0.5, 5, 10)
    ax.plot(xs, 4.3 - xs, "k", lw=1.5)
    ax.plot(xs, 3.3 - xs, "k--", lw=.9)
    ax.plot(xs, 5.3 - xs, "k--", lw=.9)
    ax.annotate("", xy=(2.15, 3.15), xytext=(1.65, 1.65), arrowprops=dict(arrowstyle="<->"))
    ax.text(1.0, 2.55, "margin = 2/‖w‖", fontsize=7)
    ax.text(3.3, 0.3, "wᵀx + b = 0", fontsize=7)
    ax.set_xlim(-0.3, 4.8)
    ax.set_ylim(-0.3, 4.8)
    ax.set_aspect("equal")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")


def _fig_tree(fig):
    ax = fig.add_subplot(111)
    ax.axis("off")
    box = dict(boxstyle="round,pad=0.35", fc="#f4ece1", ec="#6b1d1d")
    leaf = dict(boxstyle="round,pad=0.3", fc="white", ec="k")
    ax.text(0.5, 0.9, "Outlook?", ha="center", bbox=box)
    for x, lab in [(0.15, "Sunny"), (0.5, "Overcast"), (0.85, "Rain")]:
        ax.annotate("", xy=(x, 0.6), xytext=(0.5, 0.85), arrowprops=dict(arrowstyle="->"))
        ax.text((x + 0.5) / 2 + (0.0 if x == 0.5 else (-0.03 if x < 0.5 else 0.03)), 0.73, lab, fontsize=6.5,
                ha="center", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.text(0.15, 0.55, "Humidity?", ha="center", bbox=box)
    ax.text(0.5, 0.55, "Yes", ha="center", bbox=leaf)
    ax.text(0.85, 0.55, "Wind?", ha="center", bbox=box)
    for x0, x, lab, l in [(0.15, 0.05, "High", "No"), (0.15, 0.27, "Normal", "Yes"),
                          (0.85, 0.73, "Strong", "No"), (0.85, 0.95, "Weak", "Yes")]:
        ax.annotate("", xy=(x, 0.25), xytext=(x0, 0.5), arrowprops=dict(arrowstyle="->"))
        ax.text((x + x0) / 2 + (-0.035 if x < x0 else 0.035), 0.38, lab, fontsize=6, ha="center")
        ax.text(x, 0.2, l, ha="center", bbox=leaf)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 1)


def _fig_mlp(fig):
    ax = fig.add_subplot(111)
    ax.axis("off")
    layers = [3, 4, 2]
    names = ["Input", "Hidden\n(ReLU)", "Output\n(softmax)"]
    pos = []
    for li, n in enumerate(layers):
        ys = np.linspace(0.15, 0.85, n)
        pos.append([(0.15 + 0.35 * li, y) for y in ys])
    for li in range(len(layers) - 1):
        for p in pos[li]:
            for q in pos[li + 1]:
                ax.plot([p[0], q[0]], [p[1], q[1]], color="gray", lw=.6, zorder=1)
    for li, ps in enumerate(pos):
        for p in ps:
            ax.add_patch(__import__("matplotlib").patches.Circle(p, 0.045, fc="white", ec="k", zorder=2))
        ax.text(ps[0][0], -0.02, names[li], ha="center", va="top", fontsize=6.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.2, 1)
    ax.set_aspect("equal")


def _fig_kmeans(fig):
    ax = fig.add_subplot(111)
    rng = np.random.default_rng(7)
    cs = np.array([[1, 1], [4, 1.5], [2.5, 4]])
    mk = ["o", "s", "^"]
    for k, c in enumerate(cs):
        pts = rng.normal(c, .5, (15, 2))
        ax.scatter(*pts.T, marker=mk[k], s=16, facecolor="none" if k == 0 else None, edgecolor="k",
                   color=None if k == 0 else ["k", "gray", "gray"][k])
        ax.scatter(*c, marker="X", s=120, color="#6b1d1d")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_title("k-means: clusters and centroids (✕)")


def _fig_dendro(fig):
    ax = fig.add_subplot(111)
    # manual dendrogram for points A..E
    def link(x1, x2, h1, h2, h):
        ax.plot([x1, x1, x2, x2], [h1, h, h, h2], "k", lw=1.2)
    link(0, 1, 0, 0, 1.0)
    link(2, 3, 0, 0, 1.6)
    link(2.5, 4, 1.6, 0, 2.6)
    link(0.5, 3.25, 1.0, 2.6, 4.2)
    ax.axhline(2.0, color="#6b1d1d", ls="--", lw=1)
    ax.text(4.1, 2.05, "cut → 3 clusters", color="#6b1d1d", fontsize=7, ha="right", va="bottom")
    ax.set_xticks(range(5))
    ax.set_xticklabels(list("ABCDE"))
    ax.set_ylabel("merge distance")
    ax.set_ylim(0, 4.6)


def _fig_pca(fig):
    ax = fig.add_subplot(111)
    rng = np.random.default_rng(5)
    X = rng.multivariate_normal([0, 0], [[3, 1.6], [1.6, 1.3]], 120)
    ax.scatter(*X.T, s=6, color="gray")
    vals, vecs = np.linalg.eigh(np.cov(X.T))
    for v, l, name in zip(vecs.T[::-1], vals[::-1], ["PC1", "PC2"]):
        ax.annotate("", xy=v * 2.6 * np.sqrt(l), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=1.6, color="#6b1d1d"))
        ax.text(*(v * 2.9 * np.sqrt(l)), name, fontsize=7.5, color="#6b1d1d")
    ax.set_aspect("equal")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")


def _fig_roc(fig):
    ax = fig.add_subplot(111)
    f = np.linspace(0, 1, 100)
    ax.plot(f, f ** 0.35, label="good classifier (AUC≈0.85)")
    ax.plot(f, f ** 0.7, label="weak classifier")
    ax.plot([0, 1], [0, 1], "k--", lw=.8, label="random (AUC = 0.5)")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))


def _fig_cv(fig):
    ax = fig.add_subplot(111)
    k = 5
    for i in range(k):
        for j in range(k):
            ax.add_patch(__import__("matplotlib").patches.Rectangle((j, k - 1 - i), 0.95, 0.8,
                                                                    fc="#6b1d1d" if i == j else "#e8dccb", ec="none"))
        ax.text(-0.2, k - 1 - i + 0.4, f"Fold {i + 1}", ha="right", va="center", fontsize=7)
    ax.text(k / 2, -0.5, "dark = validation part, light = training part", ha="center", fontsize=7)
    ax.set_xlim(-1.3, k)
    ax.set_ylim(-0.8, k)
    ax.axis("off")


def section(title, items, fig=None, figw=8.5, figh=5.5, cap=""):
    out = [CondPageBreak(5 * cm), P(title, "h2")]
    for it in items:
        out.append(P(it, "body"))
        out.append(Spacer(1, 2))
    if fig is not None:
        out += block_flowables(Figure(fig, figw, figh, cap))
    return out


def revision_story(SetHeader):
    o = [SetHeader("Revision notes", "Concept & formula revision", 0, key="rev"),
         P("Concept and Formula Revision", "h1"),
         P("This is a short summary of the results the mock tests use most. Notation: n = number of samples, "
           "p = number of features, ŷ = prediction, 1[·] = indicator function.", "body")]

    o += section("1. Regression vs classification; loss functions", [
        "<b>Regression:</b> the target is continuous, and the usual loss is squared error (ŷ − y)² (or absolute "
        "error). <b>Classification:</b> the target is a discrete label; the usual losses are 0–1 loss, "
        "cross-entropy (log loss) and hinge loss.",
        "Binary cross-entropy: L = −[y ln p + (1 − y) ln(1 − p)].  Hinge loss: max(0, 1 − y·f(x)) with y ∈ {−1, +1}.",
        "Hinge, logistic and squared losses are convex surrogates for the 0–1 loss, which cannot be optimised "
        "directly. All of them are plotted against the margin m = y·f(x)."],
        _fig_losses, 8.5, 5.2, "Classification losses as functions of the margin")

    o += section("2. Simple linear regression", [
        "Model y = β₀ + β₁x + ε.  β̂₁ = S<sub>xy</sub>/S<sub>xx</sub> = r·(s<sub>y</sub>/s<sub>x</sub>),  β̂₀ = ȳ − β̂₁x̄, "
        "where S<sub>xy</sub> = Σ(x<sub>i</sub>−x̄)(y<sub>i</sub>−ȳ) and S<sub>xx</sub> = Σ(x<sub>i</sub>−x̄)².",
        "The fitted line passes through (x̄, ȳ). Residuals e<sub>i</sub> = y<sub>i</sub> − ŷ<sub>i</sub> satisfy Σe<sub>i</sub> = 0 "
        "and Σx<sub>i</sub>e<sub>i</sub> = 0.",
        "SST = Σ(y<sub>i</sub>−ȳ)² = SSR + SSE;  R² = SSR/SST = 1 − SSE/SST, and R² = r² for simple regression.",
        "Unbiased noise variance estimate: σ̂² = SSE/(n − 2) (in general SSE/(n − p − 1)). "
        "Var(β̂₁) = σ²/S<sub>xx</sub>."])

    o += section("3. Multiple linear regression", [
        "Normal equations XᵀXβ = Xᵀy ⇒ β̂ = (XᵀX)⁻¹Xᵀy (X includes a column of 1s for the intercept).",
        "Hat matrix H = X(XᵀX)⁻¹Xᵀ, ŷ = Hy. H is symmetric and idempotent (H² = H), and trace(H) = rank(H) = number "
        "of fitted parameters. I − H is also idempotent, and the residuals are e = (I − H)y.",
        "Adjusted R² = 1 − (1 − R²)(n − 1)/(n − p − 1). Adding a feature never decreases R², "
        "but adjusted R² can go down.",
        "Multicollinearity makes XᵀX close to singular, so the coefficient variances blow up. A categorical "
        "variable with K levels needs K − 1 dummy columns when an intercept is present (otherwise the "
        "dummy-variable trap makes X rank-deficient)."])

    o += section("4. Ridge, lasso and the MAP view", [
        "Ridge: minimise ‖y − Xβ‖² + λ‖β‖², with solution β̂ = (XᵀX + λI)⁻¹Xᵀy. XᵀX + λI is invertible for every λ &gt; 0. "
        "In one dimension with centred data, β̂<sub>ridge</sub> = S<sub>xy</sub>/(S<sub>xx</sub> + λ). "
        "Ridge shrinks coefficients towards 0 but never exactly to 0. Larger λ means more bias and less variance.",
        "Lasso: an L1 penalty λ‖β‖₁. Its constraint region is a diamond with corners on the axes, so the "
        "solution can set coefficients exactly to zero (feature selection). It has no closed form in general.",
        "Least squares is the MLE under Gaussian noise. MAP with a Gaussian prior on β gives ridge "
        "(λ = σ²/τ²); MAP with a Laplace prior gives lasso.",
        "The intercept is usually not penalised, and features should be standardised before regularising, "
        "because the penalty is not scale-invariant."])

    o += section("5. Bias–variance trade-off", [
        "For squared loss: E[(y − f̂(x))²] = Bias[f̂(x)]² + Var[f̂(x)] + σ² (irreducible noise).",
        "Low complexity gives high bias (underfitting): training and test errors are both high. High "
        "complexity gives high variance (overfitting): training error is low and test error is high.",
        "More training data lowers variance. Regularisation, bagging and larger k in k-NN also lower variance. "
        "Boosting and adding features mainly lower bias."],
        _fig_bias_variance, 8.5, 5.3, "U-shaped test error: the sum of bias², variance and noise")

    o += section("6. Cross-validation", [
        "<b>k-fold CV:</b> split the data into k folds; train on k − 1 folds and validate on the remaining one; "
        "repeat k times. CV error = (1/k)Σ E<sub>j</sub> (weight by fold size if folds are unequal). "
        "This takes k model fits.",
        "<b>LOOCV</b> is k = n: it needs n fits, has low bias and high variance, and involves no randomness. "
        "For least squares (and any linear smoother) there is a shortcut: "
        "CV<sub>(n)</sub> = (1/n) Σ [e<sub>i</sub>/(1 − h<sub>ii</sub>)]².",
        "Stratified k-fold keeps the class proportions in every fold. Every preprocessing step (scaling, feature "
        "selection) must be fitted inside the training folds, or information leaks from the validation data. "
        "Choosing hyper-parameters on the test set biases the error estimate; use nested CV instead."],
        _fig_cv, 7.5, 4.0, "5-fold cross-validation")

    o += section("7. Gradient descent", [
        "θ ← θ − η∇J(θ). For MSE, J = (1/n)‖Xθ − y‖² and ∇J = (2/n)Xᵀ(Xθ − y) "
        "(with the ½ convention, ∇J = (1/n)Xᵀ(Xθ − y)).",
        "A learning rate that is too large makes the loss oscillate or diverge; one that is too small makes "
        "convergence slow. For a convex quadratic, GD converges if η &lt; 2/L, where L is the largest "
        "eigenvalue of the Hessian.",
        "Updates per epoch: N/B (rounded up) for mini-batch size B. Batch GD makes 1 update per epoch; "
        "SGD makes N."])

    o += section("8. Logistic regression and softmax", [
        "P(y = 1 | x) = σ(wᵀx + b), with σ(z) = 1/(1 + e<super>−z</super>), σ(−z) = 1 − σ(z) and σ′(z) = σ(z)(1 − σ(z)) ≤ ¼.",
        "Log-odds are linear: ln[p/(1 − p)] = wᵀx + b. Increasing x<sub>j</sub> by 1 multiplies the odds by e<super>w<sub>j</sub></super>.",
        "The decision boundary at threshold 0.5 is the hyperplane wᵀx + b = 0. The gradient of the log loss is "
        "(σ(wᵀx) − y)x. There is no closed-form solution, but the loss is convex. On linearly separable data, "
        "‖w‖ → ∞ unless the model is regularised.",
        "Softmax: p<sub>k</sub> = e<super>z<sub>k</sub></super>/Σ<sub>j</sub>e<super>z<sub>j</sub></super>. Adding the "
        "same constant to all z<sub>k</sub> leaves p unchanged. The cross-entropy gradient with respect to z is p − y."])

    o += section("9. k-nearest neighbours", [
        "Predict the majority class (classification) or the mean target (regression) of the k nearest training "
        "points. The method is non-parametric and lazy: there is no training step, and prediction costs O(nd) per query.",
        "Small k gives low bias and high variance (1-NN has zero training error). Large k gives a smoother "
        "boundary, with higher bias and lower variance. Use an odd k for binary problems to avoid ties.",
        "k-NN needs feature scaling and suffers from the curse of dimensionality: in high dimensions, distances "
        "concentrate and all points look roughly equally far away.",
        "Distances: Minkowski d<sub>p</sub> = (Σ|x<sub>i</sub> − z<sub>i</sub>|<super>p</super>)<super>1/p</super>; p = 1 is "
        "Manhattan, p = 2 is Euclidean, p → ∞ is Chebyshev (max)."])

    o += section("10. Naive Bayes", [
        "ŷ = argmax<sub>c</sub> P(c) Π<sub>j</sub> P(x<sub>j</sub> | c). The model assumes the features are conditionally "
        "independent given the class.",
        "Laplace (add-α) smoothing: P(x<sub>j</sub> = v | c) = (count(v, c) + α)/(count(c) + α·|V<sub>j</sub>|). "
        "Without smoothing, a single zero count makes the whole product zero.",
        "Gaussian NB: P(x<sub>j</sub> | c) = N(x<sub>j</sub>; μ<sub>jc</sub>, σ²<sub>jc</sub>). Parameters for d binary "
        "features and K classes: (K − 1) + Kd, compared with K(2<super>d</super> − 1) + (K − 1) for the full joint distribution."])

    o += section("11. Linear discriminant analysis (LDA)", [
        "LDA models each class as a Gaussian with its own mean and a shared covariance Σ. The discriminant "
        "δ<sub>k</sub>(x) = xᵀΣ⁻¹μ<sub>k</sub> − ½μ<sub>k</sub>ᵀΣ⁻¹μ<sub>k</sub> + ln π<sub>k</sub> is linear in x, so the "
        "decision boundaries are linear.",
        "In 1-D with two classes, equal variance and equal priors, the threshold is (μ₀ + μ₁)/2. With unequal priors "
        "it is (μ₀ + μ₁)/2 + σ² ln(π₀/π₁)/(μ₁ − μ₀).",
        "QDA gives each class its own covariance Σ<sub>k</sub>, so the boundaries are quadratic. Fisher's direction is "
        "w ∝ S<sub>W</sub>⁻¹(μ₁ − μ₀). With K classes there are at most K − 1 discriminant directions."])

    o += section("12. Support vector machines", [
        "Hard margin: minimise ½‖w‖² subject to y<sub>i</sub>(wᵀx<sub>i</sub> + b) ≥ 1. The geometric margin (the "
        "width of the street) is 2/‖w‖, and the distance from a point to the hyperplane is |wᵀx + b|/‖w‖.",
        "Dual solution: w = Σα<sub>i</sub>y<sub>i</sub>x<sub>i</sub>, with Σα<sub>i</sub>y<sub>i</sub> = 0 and α<sub>i</sub> ≥ 0. "
        "Only the support vectors have α<sub>i</sub> &gt; 0.",
        "Soft margin: ½‖w‖² + CΣξ<sub>i</sub>. A large C penalises violations heavily (narrower margin, lower bias); "
        "a small C allows a wider margin (more regularisation). ξ<sub>i</sub> = 0 means outside the margin; "
        "0 &lt; ξ<sub>i</sub> ≤ 1 means inside the margin but correctly classified; ξ<sub>i</sub> &gt; 1 means misclassified.",
        "Kernels: polynomial (xᵀz + c)<super>d</super>; RBF exp(−γ‖x − z‖²). A kernel is valid exactly when every "
        "Gram matrix is positive semi-definite. Sums, products and positive multiples of valid kernels are valid."],
        _fig_svm, 9.5, 6.0, "Maximum-margin hyperplane; the dashed lines pass through the support vectors")

    o += section("13. Decision trees", [
        "Entropy H = −Σp<sub>k</sub>log₂p<sub>k</sub> (maximum log₂K). Gini = 1 − Σp<sub>k</sub>² (maximum 1 − 1/K). "
        "Misclassification error = 1 − max p<sub>k</sub>.",
        "Information gain IG = H(parent) − Σ(n<sub>v</sub>/n)H(child<sub>v</sub>). Gain ratio = IG/SplitInfo, where "
        "SplitInfo = −Σ(n<sub>v</sub>/n)log₂(n<sub>v</sub>/n); it penalises attributes with many values.",
        "For a continuous attribute, candidate thresholds are the midpoints between consecutive sorted values "
        "where the class changes. Regression trees choose splits that minimise SSE (that is, reduce variance) "
        "and predict the leaf mean.",
        "Trees are greedy, non-parametric and unaffected by monotone feature transforms. A binary tree of depth "
        "d has at most 2<super>d</super> leaves. Pre-pruning and post-pruning (cost-complexity "
        "R<sub>α</sub>(T) = R(T) + α|T|) control overfitting.",
        "Bagging and random forests reduce variance; each bootstrap sample leaves out about (1 − 1/n)<super>n</super> ≈ "
        "e<super>−1</super> ≈ 36.8% of the points (out-of-bag). AdaBoost gives a weak learner with error ε the "
        "weight α = ½ ln((1 − ε)/ε)."],
        _fig_tree, 9, 5.0, "A decision tree for the PlayTennis data")

    o += section("14. Perceptron and multi-layer perceptrons", [
        "Perceptron: ŷ = sign(wᵀx + b). Update on a mistake: w ← w + ηy<sub>i</sub>x<sub>i</sub>, b ← b + ηy<sub>i</sub>. "
        "It converges in finitely many steps if the data are linearly separable. A single perceptron cannot "
        "represent XOR.",
        "Forward pass: a<super>(l)</super> = g(W<super>(l)</super>a<super>(l−1)</super> + b<super>(l)</super>). With linear "
        "activations, any number of layers collapses to one linear map. One hidden layer with enough "
        "units is a universal approximator.",
        "Parameter count for layer sizes n₀ → n₁ → … → n<sub>L</sub>: Σ(n<sub>l−1</sub> + 1)·n<sub>l</sub> (weights plus biases).",
        "Backpropagation: δ<super>(L)</super> = ∂L/∂z<super>(L)</super>; δ<super>(l)</super> = (W<super>(l+1)</super>ᵀδ<super>(l+1)</super>) ⊙ g′(z<super>(l)</super>); "
        "∂L/∂W<super>(l)</super> = δ<super>(l)</super>a<super>(l−1)</super>ᵀ. If all weights start at the same value, "
        "symmetry is never broken, so initialise randomly.",
        "Inverted dropout with keep probability p scales the kept activations by 1/p during training. "
        "An L2 penalty gives weight decay: w ← (1 − ηλ)w − η∇L."],
        _fig_activations, 8.5, 5.2, "Common activation functions")
    o += block_flowables(Figure(_fig_mlp, 5.5, 4.0, "A 3–4–2 feed-forward network: (3+1)·4 + (4+1)·2 = 26 parameters"))

    o += section("15. Clustering: k-means and k-medoids", [
        "k-means minimises J = Σ<sub>k</sub>Σ<sub>x∈C<sub>k</sub></sub>‖x − μ<sub>k</sub>‖². Lloyd's algorithm alternates "
        "(i) assigning each point to its nearest centroid and (ii) recomputing each centroid as its cluster mean. "
        "J never increases, the algorithm converges in finitely many steps, but it may stop at a local minimum.",
        "k-means is sensitive to initialisation (k-means++ helps), to outliers and to feature scale, and it "
        "assumes convex, roughly spherical clusters. Use the elbow method or the silhouette to choose k.",
        "k-medoids (PAM): every centre must be an actual data point (the medoid minimises the total distance to "
        "the other points in its cluster). It works with any dissimilarity and is more robust to outliers.",
        "Silhouette s(i) = (b − a)/max(a, b) ∈ [−1, 1]. Here a is the mean distance to the point's own cluster and b is "
        "the smallest mean distance to another cluster."],
        _fig_kmeans, 7.5, 5.5)

    o += section("16. Hierarchical clustering", [
        "Agglomerative (bottom-up): start with n singleton clusters and repeatedly merge the closest pair, "
        "giving n − 1 merges in total. Divisive (top-down): start with one cluster and split recursively.",
        "Single linkage: min distance between members (tends to chain; equivalent to building a minimum spanning "
        "tree). Complete linkage: max distance (compact clusters). Average linkage (UPGMA): mean of all pairwise "
        "distances. Ward: the merge that least increases the total within-cluster SSE.",
        "Cutting the dendrogram at height h gives the clusters whose merge heights are below h. With "
        "single and complete linkage the merge heights never decrease (no inversions)."],
        _fig_dendro, 7.5, 5.0, "Dendrogram; cutting at height 2 gives {A,B}, {C,D}, {E}")

    o += section("17. Principal component analysis", [
        "Centre the data (and standardise it if the units differ). The covariance matrix is "
        "S = XᵀX/(n − 1). Its eigenvectors are the principal directions, and its eigenvalues λ₁ ≥ λ₂ ≥ … "
        "are the variances along them.",
        "Proportion of variance explained by PC k: λ<sub>k</sub>/Σλ<sub>j</sub>. Squared reconstruction error when "
        "keeping the top m components: the sum of the discarded eigenvalues (times n − 1 for the total squared error).",
        "SVD view: X = UΣVᵀ. The principal directions are the columns of V, the scores are UΣ = XV, and λ<sub>k</sub> = "
        "σ<sub>k</sub>²/(n − 1). PCs are orthogonal and their scores are uncorrelated.",
        "PCA is unsupervised and linear and keeps directions of maximum variance. LDA is supervised and keeps "
        "directions of maximum class separation."],
        _fig_pca, 7, 5.5, "Principal directions of a correlated 2-D cloud")

    o += section("18. Classification metrics", [
        "Precision = TP/(TP + FP). Recall (sensitivity, TPR) = TP/(TP + FN). Specificity = TN/(TN + FP). "
        "FPR = 1 − specificity.",
        "F1 = 2PR/(P + R). F<sub>β</sub> = (1 + β²)PR/(β²P + R). Accuracy = (TP + TN)/N can be misleading when "
        "the classes are imbalanced.",
        "The ROC curve plots TPR against FPR as the threshold varies. AUC is the probability that a random positive "
        "is scored higher than a random negative (ties count ½). Macro-averaging takes the unweighted mean of "
        "the per-class metric; micro-averaging pools the counts first."],
        _fig_roc, 10, 5.0)
    o.append(PageBreak())
    return o


# ----------------------------------------------------------------------------
# Master answer key
# ----------------------------------------------------------------------------
def master_key_story(all_sets, SetHeader, tbl):
    out = [SetHeader("Master answer key", "Master answer key", 0, key="master"),
           P("Master Answer Key: all tests", "h1"),
           P("NAT answers are shown as accepted ranges. For MSQ, every listed option must be chosen.", "small"),
           Spacer(1, 4)]
    for si, qs in enumerate(all_sets, 1):
        rows = [["Q"] + [str(i) for i in range(1, 13)]]
        cells = [answer_text(q).replace(" to ", "–<br/>") for q in qs]
        for start in range(0, len(qs), 12):
            chunk = cells[start:start + 12]
            idx = [str(i + 1) for i in range(start, start + len(chunk))]
            rows_c = [["Q"] + idx + [""] * (12 - len(chunk)), ["Key"] + chunk + [""] * (12 - len(chunk))]
            if start == 0:
                rows = rows_c
            else:
                rows += rows_c
        out.append(KeepTogether([P(f"<b>Mock Test {si:02d}</b>", "body"),
                                 tbl(rows, [1.0] + [1.25] * 12, header=False, font=6.6), Spacer(1, 6)]))
    return out
