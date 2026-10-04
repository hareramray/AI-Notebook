"""Assemble 50 GATE DA Machine-Learning mock sets into one PDF.

    python build.py                 # all 50 sets -> GATE_DA_ML_Mock_Exams_50_Sets.pdf
    python build.py --sets 2        # quick preview with 2 sets
"""
from __future__ import annotations

import argparse
import importlib
import os
import pkgutil
import random
from collections import Counter, defaultdict

import numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table as RLTable, TableStyle)

import core
from core import LETTERS, generate
import render
from render import LINE, MAROON, S, SOFT, answer_text, question_flowables, solution_flowables

HERE = os.path.dirname(os.path.abspath(__file__))

N_SETS = 50
PER_MODULE = {1: 3, 2: 4}         # per module per set -> 5 modules x 7 = 35 questions, 55 marks
DURATION_MIN = 100
MODULE_ORDER = ["regression", "classification", "svm_trees", "neural_nets", "unsupervised"]
SET_THEMES = None


# ----------------------------------------------------------------------------
# Page decoration / bookmarks
# ----------------------------------------------------------------------------
class State:
    header = ""


class SetHeader(Flowable):
    """Zero-size flowable that changes the running header and adds a PDF bookmark."""

    def __init__(self, header, bookmark=None, level=0, key=None):
        super().__init__()
        self.header, self.bookmark, self.level, self.key = header, bookmark, level, key
        self.width = self.height = 0

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        State.header = self.header
        if self.bookmark:
            key = self.key or f"bm{id(self)}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(self.bookmark, key, level=self.level, closed=self.level == 0)


def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(MAROON)
    canvas.setLineWidth(0.8)
    canvas.line(2 * cm, h - 1.35 * cm, w - 2 * cm, h - 1.35 * cm)
    canvas.setFont("Sans-Bold", 7.8)
    canvas.setFillColor(MAROON)
    canvas.drawString(2 * cm, h - 1.2 * cm, "GATE DA · Machine Learning Mock Test Series")
    canvas.setFont("Sans", 7.8)
    canvas.drawRightString(w - 2 * cm, h - 1.2 * cm, State.header)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawCentredString(w / 2, 1.0 * cm, f"— {doc.page} —")
    canvas.restoreState()


def on_cover(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(MAROON)
    canvas.rect(0, h - 9.5 * cm, w, 9.5 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Sans-Bold", 30)
    canvas.drawString(2 * cm, h - 3.4 * cm, "GATE DA")
    canvas.setFont("Sans-Bold", 21)
    canvas.drawString(2 * cm, h - 4.7 * cm, "Machine Learning")
    canvas.setFont("Sans", 15)
    canvas.drawString(2 * cm, h - 5.8 * cm, "50 Full-Length Sectional Mock Tests")
    canvas.setFont("Sans", 10.5)
    canvas.drawString(2 * cm, h - 7.0 * cm, "MCQ · MSQ · NAT  |  1-mark & 2-mark  |  Answer keys & detailed solutions")
    canvas.drawString(2 * cm, h - 7.6 * cm, "Aligned to GATE DA Section 6 (Machine Learning) syllabus")
    canvas.restoreState()


# ----------------------------------------------------------------------------
# Question selection
# ----------------------------------------------------------------------------
def load_modules():
    mods = []
    for m in MODULE_ORDER:
        importlib.import_module(f"topics.{m}")
        mods.append(m)
    return mods


def pick_templates(mods, n_sets, seed=2027):
    """Least-used-first selection so that every template is used evenly across the sets,
    while avoiding repeating a subtopic within a module in the same set when possible."""
    rnd = random.Random(seed)
    by_key = defaultdict(list)
    for t in core.REGISTRY:
        mod = t.name.split(".")[1]
        if mod in mods:
            by_key[(mod, t.marks)].append(t)
    usage = Counter()
    plan = []
    for s in range(n_sets):
        chosen = {1: [], 2: []}
        for mod in mods:
            for marks, k in PER_MODULE.items():
                pool = list(by_key[(mod, marks)])
                rnd.shuffle(pool)
                picked, subs, types = [], set(), Counter()
                for _ in range(k):
                    def score(t):
                        return (usage[t.name], t.subtopic in subs, types[t.qtype] >= 2, rnd.random())
                    cand = [t for t in pool if t not in picked]
                    best = min(cand, key=score)
                    picked.append(best)
                    subs.add(best.subtopic)
                    types[best.qtype] += 1
                    usage[best.name] += 1
                chosen[marks] += picked
        # interleave modules within each mark group so topics are mixed like a real paper
        for marks in (1, 2):
            rnd.shuffle(chosen[marks])
        plan.append(chosen[1] + chosen[2])
    return plan, usage


# ----------------------------------------------------------------------------
# Set pages
# ----------------------------------------------------------------------------
def tbl(data, widths, header=True, font=8.4, zebra=False, align="CENTER"):
    sty = S["cell"] if align == "CENTER" else S["cellL"]
    st = sty.clone("x", fontSize=font, leading=font + 2.2)
    rows = [[Paragraph(str(c), st) for c in r] for r in data]
    t = RLTable(rows, colWidths=[w * cm for w in widths], hAlign="LEFT", repeatRows=1 if header else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), SOFT))
    if zebra:
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#fbf8f3")))
    t.setStyle(TableStyle(style))
    return t


def set_intro(num, qs):
    marks = sum(q.marks for q in qs)
    types = Counter(q.qtype for q in qs)
    topics = Counter(q.topic for q in qs)
    tmarks = Counter()
    for q in qs:
        tmarks[q.topic] += q.marks
    fl = [SetHeader(f"Mock Test {num:02d}", f"Mock Test {num:02d}", 0, key=f"set{num}"),
          Paragraph(f"Mock Test {num:02d}", S["h1"]),
          Paragraph("Section 6 — Machine Learning &nbsp;|&nbsp; GATE DA pattern", S["h3"]),
          Spacer(1, 4)]
    info = [["Questions", "Total marks", "Duration", "MCQ", "MSQ", "NAT"],
            [str(len(qs)), str(marks), f"{DURATION_MIN} min", str(types["MCQ"]), str(types["MSQ"]),
             str(types["NAT"])]]
    fl += [tbl(info, [2.7] * 6), Spacer(1, 8)]
    n1 = sum(1 for q in qs if q.marks == 1)
    fl.append(Paragraph(
        f"<b>Q.1 – Q.{n1}</b> carry <b>one mark</b> each; <b>Q.{n1 + 1} – Q.{len(qs)}</b> carry <b>two marks</b> each. "
        "For a wrong MCQ answer, ⅓ mark (1-mark questions) or ⅔ mark (2-mark questions) is deducted. "
        "MSQ and NAT questions carry <b>no negative marking</b>; MSQ requires choosing <i>all and only</i> the "
        "correct options (no partial credit). NAT answers are accepted within the stated range. "
        "A calculator is allowed (as in GATE, use the on-screen virtual calculator mindset: keep work tidy).",
        S["body"]))
    fl.append(Spacer(1, 6))
    rows = [["Topic area", "Questions", "Marks"]] + [[t, str(topics[t]), str(tmarks[t])] for t in topics]
    fl += [tbl(rows, [9.5, 2.5, 2.5]), Spacer(1, 6)]
    fl.append(Paragraph("Start time: ________ &nbsp;&nbsp; End time: ________ &nbsp;&nbsp; "
                        "Score: ______ / " + str(marks), S["body"]))
    fl.append(Spacer(1, 10))
    return fl


def answer_key(num, qs):
    fl = [CondPageBreak(9 * cm), SetHeader(f"Mock Test {num:02d} · Answer Key", "Answer key", 1),
          Paragraph(f"Mock Test {num:02d} — Answer Key", S["h2"])]
    rows = [["Q", "Type", "M", "Key", "Q", "Type", "M", "Key"]]
    half = (len(qs) + 1) // 2
    for i in range(half):
        r = []
        for j in (i, i + half):
            if j < len(qs):
                q = qs[j]
                r += [str(j + 1), q.qtype, str(q.marks), answer_text(q)]
            else:
                r += ["", "", "", ""]
        rows.append(r)
    fl += [tbl(rows, [0.9, 1.3, 1.4, 4.4, 0.9, 1.3, 1.4, 4.4], zebra=True), Spacer(1, 8)]
    # self-evaluation sheet
    fl.append(Paragraph("Self-evaluation (fill after checking)", S["h3"]))
    rows = [["Topic area", "Attempted", "Correct", "Wrong (MCQ)", "Marks scored", "Max"]]
    tm = Counter()
    for q in qs:
        tm[q.topic] += q.marks
    for t in tm:
        rows.append([t, "", "", "", "", str(tm[t])])
    rows.append(["<b>Total</b>", "", "", "", "", f"<b>{sum(tm.values())}</b>"])
    fl += [tbl(rows, [6.5, 1.9, 1.8, 2.0, 2.2, 1.4]), Spacer(1, 6)]
    return fl


def build_set(num, plan_row, base_seed=100_000):
    qs = []
    for i, t in enumerate(plan_row):
        rng = np.random.default_rng(base_seed + num * 1000 + i)
        qs.append(generate(t, rng))
    story = set_intro(num, qs)
    story.append(Paragraph("Questions", S["h2"]))
    n1 = sum(1 for q in qs if q.marks == 1)
    for i, q in enumerate(qs, 1):
        if i == 1:
            story.append(Paragraph("<b>Q.1 – Q.%d : One-mark questions</b>" % n1, S["h3"]))
        if i == n1 + 1:
            story.append(CondPageBreak(6 * cm))
            story.append(Paragraph("<b>Q.%d – Q.%d : Two-mark questions</b>" % (n1 + 1, len(qs)), S["h3"]))
        story += question_flowables(i, q)
    story.append(Paragraph("<para alignment='center'><b>— END OF QUESTION PAPER —</b></para>", S["body"]))
    story += answer_key(num, qs)
    story += [PageBreak(), SetHeader(f"Mock Test {num:02d} · Solutions", "Detailed solutions", 1),
              Paragraph(f"Mock Test {num:02d} — Detailed Solutions", S["h2"])]
    for i, q in enumerate(qs, 1):
        story += solution_flowables(i, q)
    story.append(PageBreak())
    return story, qs


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", type=int, default=N_SETS)
    ap.add_argument("--out", default=os.path.join(HERE, "GATE_DA_ML_Mock_Exams_50_Sets.pdf"))
    args = ap.parse_args()

    mods = load_modules()
    plan, usage = pick_templates(mods, args.sets)

    import frontmatter
    doc = BaseDocTemplate(args.out, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.9 * cm,
                          bottomMargin=1.7 * cm, title="GATE DA – Machine Learning: 50 Mock Tests",
                          author="AI-Notebook", subject="GATE DA Machine Learning mock exams")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    cover_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, A4[1] - 11 * cm - doc.bottomMargin, id="c")
    doc.addPageTemplates([PageTemplate("cover", [cover_frame], onPage=on_cover),
                          PageTemplate("normal", [frame], onPageEnd=on_page)])

    all_sets = []
    set_stories = []
    for s in range(args.sets):
        st, qs = build_set(s + 1, plan[s])
        set_stories.append(st)
        all_sets.append(qs)
        print(f"set {s + 1:02d}: {len(qs)} questions, {sum(q.marks for q in qs)} marks", flush=True)

    story = frontmatter.cover_story(all_sets, mods)
    story += [NextPageTemplate("normal"), PageBreak()]
    story += frontmatter.intro_story(all_sets, SetHeader)
    story += frontmatter.revision_story(SetHeader)
    for st in set_stories:
        story += st
    story += frontmatter.master_key_story(all_sets, SetHeader, tbl)
    doc.build(story)
    print("usage spread: min", min(usage.values()), "max", max(usage.values()), "templates", len(usage))
    print("written", args.out)


if __name__ == "__main__":
    main()
