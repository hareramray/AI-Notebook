"""Format reference for mock-set authors (not included in the book)."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def fig_normal_shade():
    x = np.linspace(-3.5, 3.5, 400)
    fig, ax = plt.subplots(figsize=(5.2, 2.4))
    ax.plot(x, stats.norm.pdf(x), color="#1f5f8b")
    m = x > 1.96
    ax.fill_between(x[m], stats.norm.pdf(x[m]), color="#6b1d1d", alpha=0.35)
    ax.annotate("area = 0.025", xy=(2.3, 0.02), xytext=(2.2, 0.2), arrowprops=dict(arrowstyle="->"))
    ax.set_yticks([])
    ax.set_xlabel("z")
    return fig


# NAT answer computed in code so the key cannot drift from the maths
_p = 0.01 * 0.95 / (0.01 * 0.95 + 0.99 * 0.05)

SET = {
    "title": "Format Example",
    "subtitle": "Three sample questions showing every content feature.",
    "focus": "Shows MCQ, MSQ, NAT, tables, display math, figures and notes.",
    "minutes": 10,
    "questions": [
        dict(
            qtype="MCQ", marks=1, topic="Standard normal", difficulty="Easy",
            text=["Let Z ∼ N(0, 1). The value of P(Z &gt; 1.96) is closest to",
                  ("fig", fig_normal_shade)],
            options=["0.050", "0.025", "0.010", "0.975"],
            answer="B",
            solution=["By symmetry and Φ(1.96) = 0.975,",
                      "$$P(Z>1.96)=1-\\Phi(1.96)=1-0.975=0.025",
                      ("note", "1.96 is the two-sided 5% critical value; one tail holds 2.5%.", "Trap")],
        ),
        dict(
            qtype="MSQ", marks=1, topic="Independence", difficulty="Easy",
            text="Events A and B satisfy P(A) = 0.5, P(B) = 0.4, P(A ∩ B) = 0.2. Which are TRUE?",
            options=["A and B are independent", "A and B are mutually exclusive",
                     "P(A ∪ B) = 0.7", "P(A | B) = 0.5"],
            answer="A, C, D",
            solution=[("table", [["Quantity", "Value"], ["P(A)P(B)", "0.20"], ["P(A ∩ B)", "0.20"]]),
                      "Equal, so independent (A). P(A ∩ B) ≠ 0 so not mutually exclusive (B false).",
                      "$$P(A\\cup B)=0.5+0.4-0.2=0.7"],
        ),
        dict(
            qtype="NAT", marks=2, topic="Bayes theorem", difficulty="Medium",
            text="A disease has prevalence 1%. A test has sensitivity 95% and false-positive rate 5%. "
                 "Given a positive test, the probability of disease is ______ (round off to 3 decimal places).",
            answer=f"{_p:.3f}", range=(0.160, 0.162),
            solution=["$$P(D\\mid +)=\\frac{0.01(0.95)}{0.01(0.95)+0.99(0.05)}=\\frac{0.0095}{0.059}\\approx 0.161"],
        ),
    ],
}
