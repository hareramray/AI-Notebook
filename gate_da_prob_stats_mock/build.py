"""Assemble the complete GATE DA Probability & Statistics mock-test book.

    python3 build.py            -> out/GATE_DA_Probability_Statistics_Mock_Tests.pdf
"""
import glob
import math
import os
import re

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate,
                                Spacer)
from reportlab.platypus.tableofcontents import TableOfContents

from handbook import handbook_story
from render import (ACCENT, ACCENT2, FRAME_W, GOLD, HERE, MARGIN_X, PAGE_H, PAGE_W, S, P, content,
                    load_set, make_table, on_page, set_story, set_summary, validate_set)
from tables import tables_story

OUT = os.path.join(HERE, "out", "GATE_DA_Probability_Statistics_Mock_Tests.pdf")

CATEGORIES = [
    ("Counting", ["count", "permut", "combin", "arrang", "derang", "multinom", "stars", "seating",
                  "committee", "inclusion"]),
    ("Cond. expectation & variance", ["conditional expect", "conditional var", "total expect", "total var",
                                      "tower", "random sum", "e[x|", "e[y|"]),
    ("Bayes / conditional / joint prob.", ["bayes", "conditional prob", "total prob", "joint prob", "marginal",
                                           "joint pmf", "conditional"]),
    ("Axioms, events, independence", ["axiom", "sample space", "event", "independ", "exclusive", "set",
                                      "probability rules", "addition rule", "inclusion"]),
    ("Covariance & correlation", ["covar", "correl", "regression"]),
    ("Hypothesis tests (z, t, χ²)", ["z-test", "t-test", "chi-squared test", "χ² test", "hypothesis", "p-value",
                                     "goodness", "test", "type i", "power"]),
    ("Confidence intervals", ["confidence", "interval", "margin of error", "sample size"]),
    ("CLT & sampling", ["clt", "central limit", "sampling", "normal approx"]),
    ("Discrete distributions", ["binomial", "bernoulli", "discrete", "pmf", "poisson", "geometric",
                                "hypergeo", "indicator"]),
    ("Continuous distributions, PDF/CDF", ["exponential", "uniform", "pdf", "continuous", "normal", "t-dist",
                                           "chi-squared", "χ²", "cdf", "transformation", "order stat", "density",
                                           "random variable", "quantile", "memoryless"]),
    ("Descriptive statistics", ["mean", "median", "mode", "standard dev", "descriptive", "quartile", "box",
                                "variance", "grouped", "skew", "spread", "expectation"]),
]


def categorize(topic):
    t = topic.lower()
    for name, keys in CATEGORIES:
        if any(k in t for k in keys):
            return name
    return "Descriptive statistics"


class BookDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(MARGIN_X, 17 * mm, FRAME_W, PAGE_H - 36 * mm, id="f", leftPadding=0, rightPadding=0)
        cover_frame = Frame(MARGIN_X, 17 * mm, FRAME_W, PAGE_H - 36 * mm, id="c")
        self.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=draw_cover),
                               PageTemplate("normal", [frame], onPage=on_page)])

    def afterFlowable(self, f):
        toc = getattr(f, "_toc", None)
        if toc:
            level, text, key = toc
            self.notify("TOCEntry", (level, text, self.page, key))


def register(flowable, text, level, key):
    flowable._toc = (level, text, key)


def draw_cover(canv, doc):
    import numpy as np
    canv.saveState()
    canv.setFillColor(colors.HexColor("#fbf8f2"))
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canv.setFillColor(ACCENT)
    canv.rect(0, PAGE_H - 95 * mm, PAGE_W, 95 * mm, fill=1, stroke=0)
    canv.setFillColor(GOLD)
    canv.rect(0, PAGE_H - 97 * mm, PAGE_W, 2 * mm, fill=1, stroke=0)
    canv.setFont("Sans-Bold", 13)
    canv.drawString(MARGIN_X, PAGE_H - 22 * mm, "GATE  ·  DATA SCIENCE & ARTIFICIAL INTELLIGENCE (DA)")
    canv.setFillColor(colors.white)
    canv.setFont("Sans-Bold", 34)
    canv.drawString(MARGIN_X, PAGE_H - 45 * mm, "Probability &")
    canv.drawString(MARGIN_X, PAGE_H - 60 * mm, "Statistics")
    canv.setFont("Sans", 15)
    canv.drawString(MARGIN_X, PAGE_H - 75 * mm, "Mock Test Series  ·  10 Full Tests  ·  300 Questions")
    canv.setFont("Sans", 10.5)
    canv.drawString(MARGIN_X, PAGE_H - 86 * mm,
                    "MCQ · MSQ · NAT in the GATE DA pattern, with fully worked solutions")
    # bell curve illustration
    xs = np.linspace(-3.6, 3.6, 200)
    ys = np.exp(-xs ** 2 / 2)
    x0, y0, sx, sy = PAGE_W / 2, 95 * mm, 24 * mm, 70 * mm
    canv.setStrokeColor(ACCENT2)
    canv.setLineWidth(2.2)
    p = canv.beginPath()
    p.moveTo(x0 + xs[0] * sx, y0 + ys[0] * sy)
    for x, y in zip(xs[1:], ys[1:]):
        p.lineTo(x0 + x * sx, y0 + y * sy)
    canv.drawPath(p, stroke=1, fill=0)
    # shaded tails
    canv.setFillColor(colors.HexColor("#6b1d1d"))
    for side in (-1, 1):
        q = canv.beginPath()
        tail = xs[xs * side >= 1.96]
        q.moveTo(x0 + tail[0] * sx, y0)
        for x in tail:
            q.lineTo(x0 + x * sx, y0 + math.exp(-x * x / 2) * sy)
        q.lineTo(x0 + tail[-1] * sx, y0)
        q.close()
        canv.setFillAlpha(0.45)
        canv.drawPath(q, stroke=0, fill=1)
    canv.setFillAlpha(1)
    canv.setStrokeColor(colors.HexColor("#555555"))
    canv.setLineWidth(0.8)
    canv.line(x0 - 3.8 * sx, y0, x0 + 3.8 * sx, y0)
    canv.setFont("Sans", 9)
    canv.setFillColor(colors.HexColor("#555555"))
    for z, lab in [(-1.96, "−1.96"), (0, "0"), (1.96, "1.96")]:
        canv.drawCentredString(x0 + z * sx, y0 - 5 * mm, lab)
    canv.drawCentredString(x0, y0 + 30 * mm, "95%")
    # bottom panel
    canv.setFillColor(colors.HexColor("#1d2433"))
    canv.setFont("Sans-Bold", 11)
    canv.drawString(MARGIN_X, 70 * mm, "Inside this book")
    canv.setFont("Sans", 9.5)
    items = ["Part A — Formula handbook & concept review with diagrams",
             "Part B — 10 timed mock tests (30 questions, 48 marks each), answer keys & detailed solutions",
             "Part C — Standard normal, t and χ² tables  ·  performance tracker",
             "Mapped to the official GATE DA syllabus, Section 1: Probability and Statistics"]
    for i, t in enumerate(items):
        canv.drawString(MARGIN_X + 4 * mm, 62 * mm - i * 6.5 * mm, "▪  " + t)
    canv.setFillColor(ACCENT)
    canv.rect(0, 0, PAGE_W, 12 * mm, fill=1, stroke=0)
    canv.setFillColor(colors.white)
    canv.setFont("Sans", 8.5)
    canv.drawCentredString(PAGE_W / 2, 4.5 * mm, "Practice material for GATE DA aspirants · independent study resource")
    canv.restoreState()


def front_matter(sets):
    st = [NextPageTemplate("normal"), PageBreak()]
    st.append(P("Contents", "h1"))
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="Sans-Bold", fontSize=10.5, leading=15, textColor=ACCENT, spaceBefore=6),
        ParagraphStyle("t1", fontName="Body", fontSize=9.6, leading=13, leftIndent=16),
    ]
    st += [toc, PageBreak()]

    h = P("<a name='intro'/>How to Use This Book", "h1")
    register(h, "How to Use This Book", 0, "intro")
    st.append(h)
    total_q = sum(len(s["questions"]) for s in sets)
    total_m = sum(set_summary(s)[2] for s in sets)
    st += content([
        f"This book contains <b>{len(sets)} mock tests with {total_q} original questions ({total_m} marks)</b> "
        "dedicated to Section 1 of the GATE DA syllabus — Probability and Statistics — the section that also "
        "underpins much of the Machine Learning and AI sections. Every question follows the GATE question "
        "formats (MCQ, MSQ and NAT, with 1-mark and 2-mark weightage) and comes with a fully worked solution.",
        P("The GATE DA examination at a glance", "h2"),
        ("table", [["Feature", "Details"],
                   ["Duration", "3 hours, computer-based test"],
                   ["Questions / marks", "65 questions, 100 marks"],
                   ["General Aptitude (GA)", "10 questions, 15 marks (5 × 1-mark, 5 × 2-mark)"],
                   ["Subject (DA)", "55 questions, 85 marks (≈ 25 × 1-mark, 30 × 2-mark)"],
                   ["MCQ", "4 options, exactly one correct; negative marks: −1/3 (1-mark), −2/3 (2-mark)"],
                   ["MSQ", "4 options, ONE OR MORE correct; full marks only for the exact set; no negative, "
                           "no partial marking"],
                   ["NAT", "Numerical answer typed on a virtual keypad; accepted within a range; no negative"],
                   ["Calculator", "On-screen virtual scientific calculator only"]],
         dict(col_widths=[FRAME_W * 0.28, FRAME_W * 0.72], align_left_first=True)),
        "Probability & Statistics is one of the heaviest-weighted subject sections of the DA paper, and its "
        "ideas reappear in the Machine Learning (naive Bayes, LDA, bias–variance) and AI (reasoning under "
        "uncertainty) sections. A strong score here lifts the whole paper.",
        P("Structure of each mock test", "h2"),
        ("bullets", [
            "<b>30 questions, 48 marks</b>: Q1–Q12 carry 1 mark, Q13–Q30 carry 2 marks — roughly the proportion of "
            "1- and 2-mark questions in the real paper.",
            "Mixture of about 14 MCQ, 7 MSQ and 9 NAT questions per test.",
            "Suggested time: 90 minutes — the same time per mark as the real exam (≈ 1.8 min per mark).",
            "Every test is followed by an <b>answer key</b>, a <b>score tracker</b> and <b>detailed solutions</b> that "
            "state the concept, show every step, analyse each MSQ option and flag traps and shortcuts.",
        ]),
        P("Scoring rules used in this book", "h2"),
        "$$\\mathrm{Score}=\\sum_{\\mathrm{correct}}m_i-\\sum_{\\mathrm{wrong\\ MCQ}}\\dfrac{m_i}{3}",
        "MSQ answers are marked correct only when the selected set matches the key exactly. NAT answers are "
        "correct when they fall in the accepted range shown in the key.",
        P("Suggested 5-week plan", "h2"),
        ("table", [["Week", "Work", "Goal"],
                   ["1", "Part A §A1–A5; Mock 01; review every solution", "Foundations & formats"],
                   ["2", "Part A §A6–A9; Mock 02, Mock 05", "Counting, Bayes, conditional expectation"],
                   ["3", "Part A §A10–A11; Mock 03, Mock 06", "Distributions, joint pdfs, CDFs"],
                   ["4", "Part A §A12–A14; Mock 04, Mock 07, Mock 08", "Inference & descriptive stats"],
                   ["5", "Mock 09, Mock 10 under strict timing; redo wrong questions", "Exam readiness"]],
         dict(col_widths=[FRAME_W * 0.1, FRAME_W * 0.55, FRAME_W * 0.35], align_left_first=False)),
        P("Exam-day strategy for this section", "h2"),
        ("bullets", [
            "First pass: attempt all 1-mark questions and every 2-mark question you can finish in under 3 minutes.",
            "Guess on MCQs only if you can eliminate at least two options (expected value of a blind guess "
            "is zero: ¼·1 − ¾·⅓ = 0).",
            "MSQs carry no negative marking — never leave one blank, but tick only options you can justify.",
            "NAT: keep at least 4 significant figures in intermediate steps; round only at the end as instructed.",
            "Sketch: a Venn diagram, a tree, the support of a joint pdf or the rejection region costs 20 seconds "
            "and prevents most errors.",
        ]),
    ])
    st.append(PageBreak())

    # syllabus coverage
    h = P("<a name='coverage'/>Syllabus Coverage Map", "h1")
    register(h, "Syllabus Coverage Map", 0, "coverage")
    st.append(h)
    st += content(["Number of questions in each mock test by syllabus area (classified by each question's "
                   "primary topic; most questions also use ideas from neighbouring areas)."])
    cats = [c for c, _ in CATEGORIES]
    rows = [["Syllabus area"] + [f"M{i:02d}" for i in range(1, len(sets) + 1)] + ["Total"]]
    for c in cats:
        counts = [sum(1 for q in s["questions"] if categorize(q["topic"]) == c) for s in sets]
        rows.append([c] + [str(x) for x in counts] + [str(sum(counts))])
    rows.append(["Total"] + [str(len(s["questions"])) for s in sets] + [str(total_q)])
    n = len(sets)
    w0 = FRAME_W * 0.30
    wc = (FRAME_W - w0) / (n + 1)
    st.append(make_table(rows, col_widths=[w0] + [wc] * (n + 1), font_size=8, align_left_first=True))
    st.append(Spacer(1, 10))
    st.append(P("Mock test overview", "h2"))
    rows = [["Test", "Title", "Types (MCQ/MSQ/NAT)", "Marks"]]
    for i, s in enumerate(sets, 1):
        one, two, tot, by = set_summary(s)
        rows.append([f"{i:02d}", s["title"], f"{by['MCQ']} / {by['MSQ']} / {by['NAT']}", str(tot)])
    st.append(make_table(rows, col_widths=[FRAME_W * 0.08, FRAME_W * 0.62, FRAME_W * 0.2, FRAME_W * 0.1],
                         font_size=8.6))
    st.append(Spacer(1, 10))
    st.append(P("Official syllabus — Section 1: Probability and Statistics", "h2"))
    st += content([("note",
                    "Counting (permutation and combinations), probability axioms, sample space, events, independent "
                    "events, mutually exclusive events, marginal, conditional and joint probability, Bayes Theorem, "
                    "conditional expectation and variance, mean, median, mode and standard deviation, correlation, "
                    "and covariance, random variables, discrete random variables and probability mass functions, "
                    "uniform, Bernoulli, binomial distribution, continuous random variables and probability "
                    "distribution function, uniform, exponential, Poisson, normal, standard normal, t-distribution, "
                    "chi-squared distributions, cumulative distribution function, conditional PDF, central limit "
                    "theorem, confidence interval, z-test, t-test, chi-squared test.", "GATE DA 2027 syllabus")])
    st.append(PageBreak())
    return st


def tracker_story(sets):
    st = []
    h = P("<a name='tracker'/>Overall Performance Tracker", "h2")
    register(h, "Overall Performance Tracker", 1, "tracker")
    st.append(h)
    st += content(["Record each attempt. A consistent score above 70% across Tests 07–10 indicates exam "
                   "readiness for this section."])
    rows = [["Test", "Date", "Time used", "Attempted", "Correct", "Wrong", "Score", "%", "Weak topics"]]
    for i, s in enumerate(sets, 1):
        rows.append([f"{i:02d}", "", "", "", "", "", f"/{set_summary(s)[2]}", "", ""])
    w = FRAME_W
    st.append(make_table(rows, col_widths=[w * .07, w * .1, w * .1, w * .1, w * .09, w * .08, w * .09,
                                           w * .07, w * .30], font_size=8.4, zebra=False))
    st.append(Spacer(1, 12))
    st.append(P("Error log", "h3"))
    rows = [["Test · Q", "Topic", "Why I got it wrong (concept / calculation / misread / time)", "Fix"]]
    rows += [["", "", "", ""] for _ in range(14)]
    st.append(make_table(rows, col_widths=[w * .12, w * .2, w * .46, w * .22], zebra=False))
    return st


def main():
    import sys
    pattern = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sets", "set[0-9][0-9].py")
    paths = sorted(glob.glob(pattern))
    sets, errs = [], []
    for p in paths:
        s = load_set(p)
        errs += validate_set(s, os.path.basename(p))
        sets.append(s)
    if errs:
        raise SystemExit("\n".join(errs))
    doc = BookDoc(OUT, pagesize=(PAGE_W, PAGE_H), leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                  topMargin=19 * mm, bottomMargin=17 * mm,
                  title="GATE DA – Probability & Statistics Mock Test Series",
                  author="GATE DA Mock Test Series", subject="Probability and Statistics mock tests")
    story = [Spacer(1, 1)]
    story += front_matter(sets)
    story += handbook_story(register)
    h = P("<a name='partb'/>Part B · Mock Tests", "h1")
    register(h, "Part B · Mock Tests with Answer Keys and Detailed Solutions", 0, "partb")
    story.append(h)
    rows = [["Test", "Title", "Focus"]]
    for i, s in enumerate(sets, 1):
        rows.append([f"{i:02d}", s["title"], s.get("focus", s["subtitle"])])
    story.append(make_table(rows, col_widths=[FRAME_W * .08, FRAME_W * .32, FRAME_W * .60], font_size=8.4))
    story.append(PageBreak())
    reg1 = lambda f, t, l, k: register(f, t, 1, k)
    for i, s in enumerate(sets, 1):
        story += set_story(s, i, register=reg1)
    story += tables_story(register)
    story += tracker_story(sets)
    doc.multiBuild(story)
    from pypdf import PdfReader
    import render
    if render.MISSING_GLYPHS:
        print("WARNING missing glyphs:", " ".join(sorted(render.MISSING_GLYPHS)))
    print(f"Built {OUT}: {len(PdfReader(OUT).pages)} pages, {len(sets)} sets, "
          f"{sum(len(s['questions']) for s in sets)} questions")


if __name__ == "__main__":
    main()
