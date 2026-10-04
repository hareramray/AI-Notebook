"""Rendering engine for the GATE DA Probability & Statistics mock-test book.

Content grammar (used in question `text`, `solution`, and handbook sections).
A content block is either a string or a list of items; each item is one of:

  "plain paragraph with <b>ReportLab</b> markup, x<sub>i</sub>, σ<super>2</super>"
  "$$\\frac{a}{b} = \\sum_{i=1}^{n} x_i"     -> display equation (matplotlib mathtext)
  ("table", [[hdr1, hdr2], [c11, c12], ...]) -> table, first row is the header
  ("fig", callable)                          -> callable() returns a matplotlib Figure
  ("note", "text")                           -> shaded call-out box (key idea / trap)
  ("bullets", ["item 1", "item 2"])           -> bullet list

Usage:  python3 render.py sets/set01.py   -> validates + renders out/preview_set01.pdf
"""
import hashlib
import importlib.util
import io
import os
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import mathtext
from matplotlib.font_manager import FontProperties
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (CondPageBreak, Image, KeepTogether, PageBreak, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "cache")
os.makedirs(CACHE, exist_ok=True)

matplotlib.rcParams.update({
    "mathtext.fontset": "dejavuserif",
    "font.family": "DejaVu Serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 100,
})

# ---------------------------------------------------------------- fonts & styles
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Body", FD + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", FD + "DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily

registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body", boldItalic="Body-Bold")
registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans", boldItalic="Sans-Bold")

PAGE_W, PAGE_H = A4
MARGIN_X = 18 * mm
FRAME_W = PAGE_W - 2 * MARGIN_X

INK = colors.HexColor("#1d2433")
ACCENT = colors.HexColor("#6b1d1d")      # GATE-maroon
ACCENT2 = colors.HexColor("#1f5f8b")     # blue
GOLD = colors.HexColor("#f2c14e")
SOFT = colors.HexColor("#f6f1e7")
SOFT_BLUE = colors.HexColor("#eaf2f8")
RULE = colors.HexColor("#c9c2b4")
GREEN = colors.HexColor("#22663a")

S = {}
S["body"] = ParagraphStyle("body", fontName="Body", fontSize=10.2, leading=14.6, textColor=INK)
S["small"] = ParagraphStyle("small", parent=S["body"], fontSize=8.6, leading=11.5)
S["cell"] = ParagraphStyle("cell", parent=S["body"], fontSize=9.2, leading=12, alignment=TA_CENTER)
S["cellL"] = ParagraphStyle("cellL", parent=S["cell"], alignment=TA_LEFT)
S["cellH"] = ParagraphStyle("cellH", parent=S["cell"], fontName="Sans-Bold", textColor=colors.white)
S["opt"] = ParagraphStyle("opt", parent=S["body"], leftIndent=22, firstLineIndent=-22, spaceBefore=1.5)
S["qhead"] = ParagraphStyle("qhead", fontName="Sans-Bold", fontSize=10, leading=13, textColor=ACCENT)
S["shead"] = ParagraphStyle("shead", fontName="Sans-Bold", fontSize=10.5, leading=14, textColor=ACCENT2)
S["ans"] = ParagraphStyle("ans", fontName="Sans-Bold", fontSize=9.6, leading=13, textColor=GREEN)
S["h1"] = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=22, leading=28, textColor=ACCENT, spaceAfter=8)
S["h2"] = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=14.5, leading=19, textColor=ACCENT,
                         spaceBefore=10, spaceAfter=5)
S["h3"] = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=11.5, leading=15, textColor=ACCENT2,
                         spaceBefore=8, spaceAfter=3)
S["note"] = ParagraphStyle("note", parent=S["body"], fontSize=9.6, leading=13.6)
S["bullet"] = ParagraphStyle("bullet", parent=S["body"], leftIndent=14, bulletIndent=3)
S["center"] = ParagraphStyle("center", parent=S["body"], alignment=TA_CENTER)


def P(text, style="body"):
    return Paragraph(fix_text(text), S[style] if isinstance(style, str) else style)


from fontTools.ttLib import TTFont as _FT

_CMAP = set(_FT(FD + "DejaVuSerif.ttf").getBestCmap())
_SUBST = {"∅": "Ø", "⋯": "…", "∣": "|", "−": "−", " ": " ", " ": " "}
MISSING_GLYPHS = set()


def fix_text(t):
    t = str(t)
    for a, b in _SUBST.items():
        t = t.replace(a, b)
    for ch in set(t):
        if ord(ch) > 127 and ord(ch) not in _CMAP:
            MISSING_GLYPHS.add(ch)
    # escape bare '&' that is not an entity, and bare '<' that is not a tag we allow
    t = re.sub(r"&(?!(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);)", "&amp;", t)
    t = re.sub(r"<(?!/?(b|i|u|sub|super|sup|font|br|strike|a|span|para|greek|super)\b)", "&lt;", t)
    return t


# ---------------------------------------------------------------- math + figures
def _hash(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:16]


def math_image(expr, size=12.5, max_w=None):
    """Render a mathtext expression to an Image flowable (cached)."""
    max_w = max_w or FRAME_W - 20
    expr = re.sub(r"\\le(?![a-zA-Z])", r"\\leq", expr)
    expr = re.sub(r"\\ge(?![a-zA-Z])", r"\\geq", expr)
    key =_hash(f"{expr}|{size}")
    path = os.path.join(CACHE, f"m_{key}.png")
    if not os.path.exists(path):
        try:
            mathtext.math_to_image(f"${expr}$", path, prop=FontProperties(size=size), dpi=300,
                                   format="png")
        except Exception as e:  # surface which expression failed
            raise ValueError(f"mathtext failed for: {expr!r}\n{e}")
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    w_pt, h_pt = w * 72 / 300, h * 72 / 300
    if w_pt > max_w:
        h_pt *= max_w / w_pt
        w_pt = max_w
    img = Image(path, width=w_pt, height=h_pt)
    img.hAlign = "CENTER"
    return img


_fig_counter = [0]


def fig_image(fn, max_w=None, max_h=95 * mm):
    max_w = max_w or FRAME_W * 0.82
    fig = fn()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    _fig_counter[0] += 1
    data = buf.getvalue()
    path = os.path.join(CACHE, f"f_{hashlib.md5(data).hexdigest()[:16]}.png")
    with open(path, "wb") as fh:
        fh.write(data)
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    w_pt, h_pt = w * 72 / 170, h * 72 / 170
    scale = min(1.0, max_w / w_pt, max_h / h_pt)
    img = Image(path, width=w_pt * scale, height=h_pt * scale)
    img.hAlign = "CENTER"
    return img


def make_table(rows, col_widths=None, header=True, font_size=None, zebra=True, align_left_first=False):
    st_cell = S["cell"]
    if font_size:
        st_cell = ParagraphStyle("c2", parent=S["cell"], fontSize=font_size, leading=font_size * 1.3)
    st_head = ParagraphStyle("h2c", parent=st_cell, fontName="Sans-Bold", textColor=colors.white)
    st_left = ParagraphStyle("cl2", parent=st_cell, alignment=TA_LEFT)
    data = []
    for r, row in enumerate(rows):
        out = []
        for c, cell in enumerate(row):
            if r == 0 and header:
                stl = st_head
            elif c == 0 and align_left_first:
                stl = st_left
            else:
                stl = st_cell
            out.append(Paragraph(fix_text(cell), stl))
        data.append(out)
    ncol = max(len(r) for r in rows)
    if col_widths is None:
        natural = min(FRAME_W, max(ncol * 75, FRAME_W * 0.55))
        col_widths = [natural / ncol] * ncol
    t = Table(data, colWidths=col_widths, hAlign="CENTER", repeatRows=1 if header else 0)
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT2))
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if r % 2 == 0:
                style.append(("BACKGROUND", (0, r), (-1, r), SOFT_BLUE))
    t.setStyle(TableStyle(style))
    return t


class Box(Flowable):
    """Shaded call-out wrapping a list of flowables."""

    def __init__(self, flowables, bg=SOFT, border=GOLD, label=None):
        super().__init__()
        self.inner = flowables
        self.bg, self.border, self.label = bg, border, label
        self.pad = 7

    def wrap(self, aw, ah):
        self.aw = aw
        h = 0
        self._sizes = []
        for f in self.inner:
            w_, h_ = f.wrap(aw - 2 * self.pad - 4, ah)
            self._sizes.append(h_)
            h += h_ + 2
        self.h = h + 2 * self.pad
        return aw, self.h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg)
        c.setStrokeColor(self.bg)
        c.roundRect(0, 0, self.aw, self.h, 4, fill=1, stroke=0)
        c.setFillColor(self.border)
        c.rect(0, 0, 3.2, self.h, fill=1, stroke=0)
        y = self.h - self.pad
        for f, h_ in zip(self.inner, self._sizes):
            y -= h_
            f.drawOn(c, self.pad + 4, y)
            y -= 2

    def split(self, aw, ah):
        return []


def content(items, *, note_label="Key idea"):
    """Convert a content block (see module docstring) into flowables."""
    if items is None:
        return []
    if isinstance(items, (str, tuple)):
        items = [items]
    out = []
    for it in items:
        if isinstance(it, str):
            s = it.strip()
            if s.startswith("$$"):
                out.append(Spacer(1, 2))
                out.append(math_image(s[2:].strip().rstrip("$").strip()))
                out.append(Spacer(1, 3))
            else:
                out.append(P(s))
                out.append(Spacer(1, 3))
        elif isinstance(it, tuple):
            kind = it[0]
            if kind == "table":
                kw = it[2] if len(it) > 2 else {}
                out.append(Spacer(1, 2))
                out.append(make_table(it[1], **kw))
                out.append(Spacer(1, 5))
            elif kind == "fig":
                out.append(Spacer(1, 2))
                out.append(fig_image(it[1]))
                out.append(Spacer(1, 4))
            elif kind == "note":
                label = it[2] if len(it) > 2 else note_label
                inner = [P(f"<font name='Sans-Bold' color='#6b1d1d'>{label}: </font>{it[1]}", "note")]
                out.append(Spacer(1, 2))
                out.append(Box(inner))
                out.append(Spacer(1, 5))
            elif kind == "bullets":
                for b in it[1]:
                    out.append(Paragraph(fix_text(b), S["bullet"], bulletText="•"))
                out.append(Spacer(1, 3))
            else:
                raise ValueError(f"unknown content item kind {kind!r}")
        elif isinstance(it, Flowable):
            out.append(it)
        else:
            raise ValueError(f"bad content item type {type(it)}")
    return out


# ---------------------------------------------------------------- validation
QTYPES = {"MCQ", "MSQ", "NAT"}


def validate_set(SET, name="set"):
    errs = []
    for k in ("title", "subtitle", "questions"):
        if k not in SET:
            errs.append(f"{name}: missing key {k}")
    qs = SET.get("questions", [])
    for i, q in enumerate(qs, 1):
        tag = f"{name} Q{i}"
        for k in ("qtype", "marks", "topic", "text", "answer", "solution"):
            if k not in q:
                errs.append(f"{tag}: missing {k}")
        qt = q.get("qtype")
        if qt not in QTYPES:
            errs.append(f"{tag}: qtype {qt!r} invalid")
        if q.get("marks") not in (1, 2):
            errs.append(f"{tag}: marks must be 1 or 2")
        if qt in ("MCQ", "MSQ"):
            opts = q.get("options", [])
            if len(opts) != 4:
                errs.append(f"{tag}: needs exactly 4 options")
            ans = str(q.get("answer", ""))
            letters = [a.strip() for a in ans.split(",")]
            if not all(l in "ABCD" and len(l) == 1 for l in letters):
                errs.append(f"{tag}: answer {ans!r} should be letters like 'B' or 'A, C'")
            if qt == "MCQ" and len(letters) != 1:
                errs.append(f"{tag}: MCQ must have exactly one answer")
        if qt == "NAT":
            rng = q.get("range")
            if not (isinstance(rng, (tuple, list)) and len(rng) == 2 and rng[0] <= rng[1]):
                errs.append(f"{tag}: NAT needs range=(lo, hi)")
    return errs


def load_set(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SET


# ---------------------------------------------------------------- set rendering
def qtype_label(q):
    m = q["marks"]
    neg = ""
    if q["qtype"] == "MCQ":
        neg = " · −1/3" if m == 1 else " · −2/3"
    return f"{q['qtype']} · {m} mark{'s' if m > 1 else ''}{neg}"


def question_flowables(q, num):
    head = Table([[P(f"Q.{num}", "qhead"), P(f"<font size=8.5>{qtype_label(q)}</font>", "qhead")]],
                 colWidths=[40, FRAME_W - 40])
    head.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"),
                              ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    fl = [head, Spacer(1, 4)]
    fl += content(q["text"])
    if q["qtype"] in ("MCQ", "MSQ"):
        for L, o in zip("ABCD", q["options"]):
            if isinstance(o, str) and o.strip().startswith("$$"):
                row = Table([[P(f"({L})"), math_image(o.strip()[2:].strip(), size=11.5,
                                                       max_w=FRAME_W - 40)]],
                            colWidths=[24, FRAME_W - 24])
                row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                         ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                         ("ALIGN", (1, 0), (1, 0), "LEFT")]))
                row.hAlign = "LEFT"
                fl.append(row)
            else:
                fl.append(P(f"({L})&nbsp;&nbsp;{o}", "opt"))
    else:
        fl.append(Spacer(1, 3))
        fl.append(P("<font name='Sans' size=9 color='#555555'>Answer: ________________</font>"))
    fl.append(Spacer(1, 12))
    # keep short questions together; long ones may split
    return [KeepTogether(fl)] if len(fl) < 40 else fl


def answer_text(q):
    if q["qtype"] == "NAT":
        lo, hi = q["range"]
        return f"{q['answer']} (range {lo} to {hi})" if lo != hi else f"{q['answer']}"
    return q["answer"]


def solution_flowables(q, num):
    head = Table([[P(f"Q.{num}  <font color='#555555' size=8.5>[{qtype_label(q)}]</font>", "shead"),
                   P(f"<font size=8.5 color='#555555'>Topic: {q['topic']}"
                     f"{' · ' + q['difficulty'] if q.get('difficulty') else ''}</font>", "shead")]],
                 colWidths=[FRAME_W * 0.45, FRAME_W * 0.55])
    head.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"),
                              ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT2),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    fl = [CondPageBreak(70 * mm), head, Spacer(1, 4),
          P(f"Correct answer: {answer_text(q)}", "ans"), Spacer(1, 4)]
    fl += content(q["solution"])
    fl.append(Spacer(1, 12))
    return fl


def answer_key_table(qs, offset=0):
    rows = [["Q", "Type", "Marks", "Answer", "Topic"]]
    for i, q in enumerate(qs, 1):
        rows.append([str(i + offset), q["qtype"], str(q["marks"]), answer_text(q), q["topic"]])
    return make_table(rows, col_widths=[28, 44, 40, 110, FRAME_W - 222], font_size=8.6)


def set_summary(SET):
    qs = SET["questions"]
    one = [q for q in qs if q["marks"] == 1]
    two = [q for q in qs if q["marks"] == 2]
    total = sum(q["marks"] for q in qs)
    by = {t: sum(1 for q in qs if q["qtype"] == t) for t in ("MCQ", "MSQ", "NAT")}
    return one, two, total, by


def _page_break(story):
    """Drop trailing spacers (they can spill onto an otherwise blank page) and break."""
    while story and isinstance(story[-1], Spacer):
        story.pop()
    story.append(PageBreak())


def set_story(SET, set_no, register=None):
    """Story for one complete mock test: instructions, questions, key, solutions."""
    qs = SET["questions"]
    one, two, total, by = set_summary(SET)
    story = []
    anchor = f"set{set_no}"
    title = f"Mock Test {set_no:02d} — {SET['title']}"
    hp = P(f"<a name='{anchor}'/>{title}", "h1")
    if register:
        register(hp, title, 0, anchor)
    story.append(hp)
    story.append(P(SET["subtitle"], ParagraphStyle("st", parent=S["body"], textColor=ACCENT2,
                                                    fontSize=11.5, leading=15)))
    story.append(Spacer(1, 10))
    minutes = SET.get("minutes", 90)
    info = [["Item", "Details"],
            ["Questions", f"{len(qs)} ({len(one)} × 1-mark, {len(two)} × 2-mark)"],
            ["Maximum marks", f"{total}"],
            ["Question types", f"MCQ: {by['MCQ']} · MSQ: {by['MSQ']} · NAT: {by['NAT']}"],
            ["Suggested time", f"{minutes} minutes"],
            ["Negative marking", "MCQ only: −1/3 (1-mark), −2/3 (2-mark). None for MSQ & NAT."],
            ["Calculator", "Use only the GATE virtual scientific calculator"],
            ]
    story.append(make_table(info, col_widths=[120, FRAME_W - 120], align_left_first=True))
    story.append(Spacer(1, 10))
    if SET.get("focus"):
        story.append(P("<b>Topic focus of this set</b>", "h3"))
        story.append(P(SET["focus"]))
    story.append(P("<b>Instructions</b>", "h3"))
    for b in [
        "Questions 1 onwards are arranged as in GATE: all 1-mark questions first, then 2-mark questions.",
        "<b>MCQ</b> – exactly one correct option. <b>MSQ</b> – ONE OR MORE options are correct; credit only if "
        "you select all correct options and no wrong option (no partial marks, no negative marks).",
        "<b>NAT</b> – enter a numerical value using the virtual keypad. The accepted range is given in the key; "
        "round as instructed in the question.",
        "Statistical tables (Z, t, χ²) are provided in the Appendix; values in solutions use those tables.",
        "Attempt in one sitting, then check the answer key and read every solution — including those you got "
        "right — for the alternative methods and traps.",
    ]:
        story.append(Paragraph(fix_text(b), S["bullet"], bulletText="•"))
    _page_break(story)

    story.append(P(f"Mock Test {set_no:02d} · Question Paper", "h2"))
    q_sorted = list(qs)  # authors already order 1-mark first
    for i, q in enumerate(q_sorted, 1):
        if i == len(one) + 1:
            story.append(CondPageBreak(60 * mm))
            story.append(P("2-mark questions", "h3"))
        elif i == 1:
            story.append(P("1-mark questions", "h3"))
        story += question_flowables(q, i)
    _page_break(story)

    story.append(P(f"Mock Test {set_no:02d} · Answer Key", "h2"))
    story.append(answer_key_table(q_sorted))
    story.append(Spacer(1, 10))
    trk = [["", "Attempted", "Correct", "Wrong (MCQ)", "Marks"],
           ["1-mark", "", "", "", ""], ["2-mark", "", "", "", ""], ["Total", "", "", "", f"/ {total}"]]
    story.append(KeepTogether([P("<b>Score tracker</b>", "h3"),
                               make_table(trk, col_widths=[80] + [(FRAME_W - 80) / 4] * 4, zebra=False)]))
    _page_break(story)

    story.append(P(f"Mock Test {set_no:02d} · Detailed Solutions", "h2"))
    for i, q in enumerate(q_sorted, 1):
        story += solution_flowables(q, i)
    _page_break(story)
    return story


# ---------------------------------------------------------------- page decoration
def on_page(canv, doc, running="GATE DA · Probability & Statistics · Mock Test Series"):
    canv.saveState()
    canv.setStrokeColor(ACCENT)
    canv.setLineWidth(1.2)
    canv.line(MARGIN_X, PAGE_H - 14 * mm, PAGE_W - MARGIN_X, PAGE_H - 14 * mm)
    canv.setFont("Sans-Bold", 8)
    canv.setFillColor(ACCENT)
    canv.drawString(MARGIN_X, PAGE_H - 12 * mm, "GATE DA")
    canv.setFont("Sans", 8)
    canv.setFillColor(colors.HexColor("#555555"))
    canv.drawRightString(PAGE_W - MARGIN_X, PAGE_H - 12 * mm, running)
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(MARGIN_X, 13 * mm, PAGE_W - MARGIN_X, 13 * mm)
    canv.drawCentredString(PAGE_W / 2, 8.5 * mm, f"{doc.page}")
    canv.restoreState()


def preview(path):
    from reportlab.platypus import SimpleDocTemplate
    SET = load_set(path)
    name = os.path.basename(path)[:-3]
    errs = validate_set(SET, name)
    if errs:
        print("VALIDATION ERRORS:")
        print("\n".join(errs))
        sys.exit(1)
    out = os.path.join(HERE, "out", f"preview_{name}.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                            topMargin=19 * mm, bottomMargin=17 * mm)
    no = int(re.sub(r"\D", "", name) or 1)
    doc.build(set_story(SET, no), onFirstPage=on_page, onLaterPages=on_page)
    from pypdf import PdfReader
    n = len(PdfReader(out).pages)
    if MISSING_GLYPHS:
        print("WARNING: characters missing from font (render as boxes) — replace them:",
              " ".join(sorted(MISSING_GLYPHS)))
    one, two, total, by = set_summary(SET)
    print(f"OK {name}: {len(SET['questions'])} questions ({len(one)}x1, {len(two)}x2), "
          f"{total} marks, types {by}, {n} pages -> {out}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        preview(p)
