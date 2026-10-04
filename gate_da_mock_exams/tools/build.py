"""Build the GATE DA mock-test book PDF.

usage:  python3 tools/build.py [-o OUT.pdf] [--no-front] [sets/set_01.py ...]
With no set files given, every sets/set_*.py is included in order.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph, Preformatted,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DejaVuSans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansMono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansMono-Bold", FD + "DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSansMono-Oblique", FD + "DejaVuSansMono-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif", FD + "DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif-Bold", FD + "DejaVuSerif-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
LD = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans-Italic", LD + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-BoldItalic", LD + "LiberationSans-BoldItalic.ttf"))
registerFontFamily("DejaVuSans", normal="DejaVuSans", bold="DejaVuSans-Bold",
                   italic="LiberationSans-Italic", boldItalic="LiberationSans-BoldItalic")
registerFontFamily("DejaVuSansMono", normal="DejaVuSansMono", bold="DejaVuSansMono-Bold",
                   italic="DejaVuSansMono-Oblique", boldItalic="DejaVuSansMono-Bold")

import diagrams as DG
from schema import load_set, LETTERS

MAROON = colors.HexColor("#6b1d1d")
GOLD = colors.HexColor("#f2c14e")
BLUE = colors.HexColor("#1d4ed8")
DARK = colors.HexColor("#111827")
SOFT = colors.HexColor("#f3f4f6")
CODEBG = colors.HexColor("#f6f8fa")
CODEBORDER = colors.HexColor("#d0d7de")
GREEN = colors.HexColor("#166534")
GREENBG = colors.HexColor("#ecfdf5")

BASE = 9.6
ST = {
    "body": ParagraphStyle("body", fontName="DejaVuSans", fontSize=BASE, leading=BASE * 1.42,
                           textColor=DARK, alignment=TA_LEFT),
    "just": ParagraphStyle("just", fontName="DejaVuSans", fontSize=BASE, leading=BASE * 1.45,
                           textColor=DARK, alignment=TA_JUSTIFY),
    "opt": ParagraphStyle("opt", fontName="DejaVuSans", fontSize=BASE, leading=BASE * 1.38,
                          leftIndent=30, firstLineIndent=-22, textColor=DARK, spaceBefore=1.5),
    "qhead": ParagraphStyle("qhead", fontName="DejaVuSans-Bold", fontSize=10, leading=13, textColor=MAROON),
    "h1": ParagraphStyle("h1", fontName="DejaVuSerif-Bold", fontSize=22, leading=27, textColor=MAROON,
                         spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DejaVuSerif-Bold", fontSize=15, leading=19, textColor=MAROON,
                         spaceBefore=10, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="DejaVuSans-Bold", fontSize=11.5, leading=15, textColor=BLUE,
                         spaceBefore=8, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="DejaVuSans", fontSize=8, leading=10.5, textColor=DARK),
    "cell": ParagraphStyle("cell", fontName="DejaVuSans", fontSize=8.6, leading=11, textColor=DARK),
    "cellb": ParagraphStyle("cellb", fontName="DejaVuSans-Bold", fontSize=8.6, leading=11, textColor=colors.white),
    "code": ParagraphStyle("code", fontName="DejaVuSansMono", fontSize=8.3, leading=10.6, textColor=DARK),
    "caption": ParagraphStyle("caption", fontName="DejaVuSans", fontSize=8, leading=10,
                              textColor=colors.HexColor("#4b5563"), alignment=TA_CENTER),
    "toc0": ParagraphStyle("toc0", fontName="DejaVuSans-Bold", fontSize=10, leading=14, leftIndent=0),
    "toc1": ParagraphStyle("toc1", fontName="DejaVuSans", fontSize=9, leading=12, leftIndent=14),
    "ans": ParagraphStyle("ans", fontName="DejaVuSans-Bold", fontSize=10, leading=13, textColor=GREEN),
}


# ------------------------------------------------------------------ markup
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_code_re = re.compile(r"`([^`]+)`")
_bold_re = re.compile(r"\*\*(.+?)\*\*")
_it_re = re.compile(r"(?<![\w*])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![\w*])")
_ital_re = re.compile(r"(?<![\w*])_\{?__(.+?)__\}?")  # rarely used
_sup_re = re.compile(r"\^\{([^}]*)\}")
_sub_re = re.compile(r"_\{([^}]*)\}")


def md(s):
    """Tiny markup: `code`, **bold**, x^{2}, a_{i}, single newline = line break."""
    if s is None:
        return ""
    codes = []

    def keep(m):
        codes.append('<font face="DejaVuSansMono" color="#7c2d12">%s</font>' % esc(m.group(1)).replace(" ", "&nbsp;"))
        return "\x00%d\x00" % (len(codes) - 1)
    p = esc(_code_re.sub(keep, str(s)))
    p = _bold_re.sub(r"<b>\1</b>", p)
    p = _it_re.sub(r"<i>\1</i>", p)
    p = _sup_re.sub(r"<super>\1</super>", p)
    p = _sub_re.sub(r"<sub>\1</sub>", p)
    p = re.sub("\x00(\\d+)\x00", lambda m: codes[int(m.group(1))], p)
    out = [p]
    return "".join(out).replace("\n", "<br/>")


def paras(s, style="body"):
    """Split on blank lines into paragraphs; lines starting with '- ' become bullets."""
    res = []
    if not s:
        return res
    bst = ParagraphStyle("b_" + style, parent=ST[style], leftIndent=14, bulletIndent=4)
    for block in re.split(r"\n\s*\n", str(s).strip()):
        buf = []

        def flush():
            if buf:
                res.append(Paragraph(md("\n".join(buf)), ST[style]))
                buf.clear()
        for l in block.split("\n"):
            if l.lstrip().startswith(("- ", "• ")):
                flush()
                res.append(Paragraph(md(l.lstrip()[2:]), bst, bulletText="•"))
            else:
                buf.append(l)
        flush()
        res.append(Spacer(1, 3))
    return res


class CodeBlock(Flowable):
    """Shaded monospace block with line wrapping for overlong lines."""

    def __init__(self, code, label=None):
        Flowable.__init__(self)
        self.code = code.rstrip("\n").expandtabs(4)
        self.label = label

    def wrap(self, aw, ah):
        self.aw = aw
        fs = ST["code"].fontSize
        cw = pdfmetrics.stringWidth("M", "DejaVuSansMono", fs)
        maxc = max(int((aw - 34) / cw), 20)
        lines = []
        for i, ln in enumerate(self.code.split("\n"), 1):
            if len(ln) <= maxc:
                lines.append((i, ln))
            else:
                ind = len(ln) - len(ln.lstrip())
                first = True
                while ln:
                    lines.append((i if first else None, ln[:maxc]))
                    ln = ln[maxc:]
                    if ln:
                        ln = " " * min(ind + 4, 20) + ln
                    first = False
        self.lines = lines
        self.h = len(lines) * ST["code"].leading + 10 + (12 if self.label else 0)
        return aw, self.h

    def split(self, aw, ah):
        lead = ST["code"].leading
        avail = int((ah - 10 - (12 if self.label else 0)) / lead)
        if avail < 4 or avail >= len(self.lines):
            return []
        raw = self.code.split("\n")
        # split on source-line boundary
        last_src = None
        for idx in range(avail - 1, -1, -1):
            if self.lines[idx][0] is not None:
                last_src = self.lines[idx][0]
                break
        if not last_src or last_src <= 1:
            return []
        a = CodeBlock("\n".join(raw[:last_src - 1]), self.label)
        b = CodeBlock("\n".join(raw[last_src - 1:]), None)
        b.start = last_src
        return [a, b]

    def draw(self):
        c = self.canv
        lead = ST["code"].leading
        top = self.h
        if self.label:
            c.setFont("DejaVuSans-Bold", 7.5)
            c.setFillColor(colors.HexColor("#6b7280"))
            c.drawString(2, top - 9, self.label)
            top -= 12
        c.setFillColor(CODEBG)
        c.setStrokeColor(CODEBORDER)
        c.roundRect(0, 0, self.aw, top, 3, stroke=1, fill=1)
        start = getattr(self, "start", 1)
        y = top - 5 - ST["code"].fontSize
        for num, ln in self.lines:
            if num is not None:
                c.setFont("DejaVuSansMono", 6.5)
                c.setFillColor(colors.HexColor("#9ca3af"))
                c.drawRightString(18, y + 0.5, str(num + start - 1))
            c.setFont("DejaVuSansMono", ST["code"].fontSize)
            c.setFillColor(DARK)
            c.drawString(26, y, ln)
            y -= lead


def diagram_flow(specs):
    out = []
    for dg in specs or []:
        d = DG.render(dg)
        d.hAlign = "CENTER"
        item = [Spacer(1, 4), d, Spacer(1, 2)]
        if dg.get("caption"):
            item.append(Paragraph(md(dg["caption"]), ST["caption"]))
        item.append(Spacer(1, 4))
        out.extend(item)
    return out


# ------------------------------------------------------------------ answers
def fmt_answer(q):
    a = q["answer"]
    if q["type"] == "MCQ":
        return "(%s)" % a
    if q["type"] == "MSQ":
        return ", ".join("(%s)" % x for x in sorted(a))
    if isinstance(a, (list, tuple)):
        lo, hi = a
        return str(lo) if str(lo) == str(hi) else "%s to %s" % (lo, hi)
    return str(a)


# ------------------------------------------------------------------ doc template
class Book(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                                 topMargin=20 * mm, bottomMargin=17 * mm,
                                 title="GATE DA Mock Test Series - Programming, Data Structures & Algorithms",
                                 author="GATE DA Practice Series", **kw)
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        cover = Frame(0, 0, A4[0], A4[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate("cover", [cover], onPage=self._cover_bg),
                               PageTemplate("normal", [fr], onPage=self._decor)])
        self.running = ""

    def _cover_bg(self, c, doc):
        W, H = A4
        c.saveState()
        c.setFillColor(MAROON)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#7f2424"))
        for i in range(14):
            c.circle(W - 40 - (i % 4) * 38, 80 + (i // 4) * 38, 9, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.rect(0, H - 18 * mm, W, 4, fill=1, stroke=0)
        c.rect(0, 36 * mm, W, 2, fill=1, stroke=0)
        c.restoreState()

    def _decor(self, c, doc):
        W, H = A4
        c.saveState()
        c.setFillColor(MAROON)
        c.rect(0, H - 11 * mm, W, 11 * mm, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("DejaVuSans-Bold", 8.5)
        c.drawString(18 * mm, H - 7 * mm, "GATE DA  |  Programming, Data Structures & Algorithms  |  Mock Test Series")
        c.setFillColor(colors.white)
        c.setFont("DejaVuSans", 8.5)
        c.drawRightString(W - 18 * mm, H - 7 * mm, self.running)
        c.setStrokeColor(colors.HexColor("#d1d5db"))
        c.line(18 * mm, 12 * mm, W - 18 * mm, 12 * mm)
        c.setFillColor(colors.HexColor("#6b7280"))
        c.setFont("DejaVuSans", 8)
        c.drawString(18 * mm, 8 * mm, "Section 4 · Python · Stacks · Queues · Linked Lists · Trees · Hashing · "
                                      "Searching · Sorting · Graphs")
        c.drawRightString(W - 18 * mm, 8 * mm, "Page %d" % doc.page)
        c.restoreState()

    def beforeDocument(self):
        self._k = 0
        self.running = ""

    def afterFlowable(self, f):
        if isinstance(f, Paragraph):
            sn = f.style.name
            if sn == "h1":
                txt = f.getPlainText()
                self._k = getattr(self, "_k", 0) + 1
                key = "h1-%d" % self._k
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, level=0)
                self.notify("TOCEntry", (0, txt, self.page, key))
            elif sn == "h2toc":
                txt = f.getPlainText()
                self._k = getattr(self, "_k", 0) + 1
                key = "h2-%d" % self._k
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(txt, key, level=1)
                self.notify("TOCEntry", (1, txt, self.page, key))
        if isinstance(f, RunningMark):
            self.running = f.text


class RunningMark(Flowable):
    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text

    def wrap(self, aw, ah):
        return 0, 0

    def draw(self):
        pass


H2TOC = ParagraphStyle("h2toc", parent=ST["h2"])


# ------------------------------------------------------------------ set rendering
def type_badge(q):
    names = {"MCQ": "MCQ · single correct", "MSQ": "MSQ · one or more correct", "NAT": "NAT · numerical answer"}
    return names[q["type"]]


def question_flow(i, q):
    head = Paragraph('Q.%d&nbsp;&nbsp;<font color="#374151" size="8.5">[%s&nbsp;&nbsp;|&nbsp;&nbsp;%d mark%s&nbsp;&nbsp;|&nbsp;&nbsp;%s]</font>'
                     % (i, type_badge(q), q["marks"], "s" if q["marks"] > 1 else "", esc(q["topic"])), ST["qhead"])
    body = [head, Spacer(1, 3)] + paras(q["text"])
    tail = []
    if q.get("code"):
        tail.append(CodeBlock(q["code"], "Python"))
        tail.append(Spacer(1, 4))
    tail += diagram_flow(q.get("diagrams"))
    if q.get("text2"):
        tail += paras(q["text2"])
    opts = []
    if q["type"] in ("MCQ", "MSQ"):
        for L, o in zip(LETTERS, q["options"]):
            if "\n" in str(o) and str(o).lstrip().startswith("```"):
                opts.append(Paragraph("(%s)" % L, ST["opt"]))
                opts.append(CodeBlock(str(o).strip().strip("`").strip("\n")))
            else:
                opts.append(Paragraph("<b>(%s)</b>&nbsp;&nbsp;%s" % (L, md(o)), ST["opt"]))
    else:
        opts.append(Paragraph('<font color="#4b5563">Answer: ____________ (enter a numerical value)</font>',
                              ST["opt"]))
    items = body + tail + opts
    blk = [KeepTogether(items)] if _est(q) < 520 else items
    return blk + [Spacer(1, 6), HRule(), Spacer(1, 6)]


def _est(q):
    n = len(q["text"]) / 85 * 14 + 40
    if q.get("code"):
        n += q["code"].count("\n") * 10.6 + 30
    n += 120 * len(q.get("diagrams", []) or [])
    n += 4 * 18
    return n


class HRule(Flowable):
    def wrap(self, aw, ah):
        self.aw = aw
        return aw, 1

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor("#e5e7eb"))
        self.canv.setLineWidth(0.6)
        self.canv.line(0, 0, self.aw, 0)


def set_cover(S, total_sets):
    n = S["number"]
    qs = S["questions"]
    flow = [RunningMark("Mock Test %02d" % n), CondPageBreak(200)]
    flow.append(Paragraph("Mock Test %02d" % n, ST["h1"]))
    flow.append(Paragraph(esc(S["title"]), H2TOC))
    if S.get("difficulty"):
        flow.append(Paragraph("<b>Difficulty:</b> %s" % esc(S["difficulty"]), ST["body"]))
    if S.get("focus"):
        flow.append(Paragraph("<b>Focus areas:</b> %s" % md(S["focus"]), ST["body"]))
    flow.append(Spacer(1, 6))
    one = sum(1 for q in qs if q["marks"] == 1)
    two = sum(1 for q in qs if q["marks"] == 2)
    cnt = {t: sum(1 for q in qs if q["type"] == t) for t in ("MCQ", "MSQ", "NAT")}
    data = [["Questions", "Total marks", "Time", "1-mark Qs", "2-mark Qs", "MCQ / MSQ / NAT"],
            [str(len(qs)), str(one + 2 * two), "%d min" % round((one + 2 * two) * 1.8), str(one), str(two),
             "%d / %d / %d" % (cnt["MCQ"], cnt["MSQ"], cnt["NAT"])]]
    t = Table(data, colWidths=[None] * 6)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "DejaVuSans-Bold", 8.5), ("FONT", (0, 1), (-1, 1), "DejaVuSans", 9.5),
        ("BACKGROUND", (0, 0), (-1, 0), MAROON), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#fff7ed")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d1d5db")), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    flow += [t, Spacer(1, 6)]
    flow.append(Paragraph(
        "<b>Marking:</b> MCQ — +1/+2 for correct, −1/3 (1-mark) or −2/3 (2-mark) for wrong. "
        "MSQ and NAT — no negative marking; MSQ needs exactly all correct options. "
        "Programs are in Python 3 unless stated otherwise.", ST["small"]))
    flow.append(Spacer(1, 10))
    return flow


def answer_key_flow(S):
    n = S["number"]
    flow = [CondPageBreak(260), Paragraph("Answer Key — Mock Test %02d" % n, ST["h2"])]
    rows = [[Paragraph("Q", ST["cellb"]), Paragraph("Type", ST["cellb"]), Paragraph("Marks", ST["cellb"]),
             Paragraph("Key", ST["cellb"]), Paragraph("Topic", ST["cellb"])]]
    for i, q in enumerate(S["questions"], 1):
        rows.append([Paragraph(str(i), ST["cell"]), Paragraph(q["type"], ST["cell"]),
                     Paragraph(str(q["marks"]), ST["cell"]),
                     Paragraph("<b>%s</b>" % esc(fmt_answer(q)), ST["cell"]), Paragraph(md(q["topic"]), ST["cell"])])
    t = Table(rows, colWidths=[24, 40, 44, 96, None], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), MAROON), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    for r in range(1, len(rows)):
        if r % 2 == 0:
            st.append(("BACKGROUND", (0, r), (-1, r), SOFT))
    t.setStyle(TableStyle(st))
    flow += [t, Spacer(1, 8)]
    return flow


def solution_flow(i, q):
    head = Paragraph('Q.%d&nbsp;&nbsp;<font color="#374151" size="8.5">[%s · %d mark%s · %s]</font>'
                     % (i, q["type"], q["marks"], "s" if q["marks"] > 1 else "", esc(q["topic"])), ST["qhead"])
    ans = Table([[Paragraph("Answer: %s" % esc(fmt_answer(q)), ST["ans"])]], colWidths=[None])
    ans.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), GREENBG),
                             ("LINEBEFORE", (0, 0), (0, -1), 3, GREEN),
                             ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    first = [head, Spacer(1, 2), ans, Spacer(1, 4)]
    body = paras(q["solution"], "just")
    if body:
        first.append(body[0])
        body = body[1:]
    flow = [KeepTogether(first)] + body
    if q.get("solution_code"):
        flow += [CodeBlock(q["solution_code"], "Worked trace / reference code"), Spacer(1, 4)]
    flow += diagram_flow(q.get("solution_diagrams"))
    if q.get("solution_after"):
        flow += paras(q["solution_after"], "just")
    flow += [Spacer(1, 4), HRule(), Spacer(1, 6)]
    return flow


def set_flow(S, total):
    flow = [NextPageTemplate("normal"), PageBreak()]
    flow += set_cover(S, total)
    for i, q in enumerate(S["questions"], 1):
        flow += question_flow(i, q)
    flow += answer_key_flow(S)
    flow += [PageBreak(), RunningMark("Mock Test %02d — Solutions" % S["number"]),
             Paragraph("Detailed Solutions — Mock Test %02d" % S["number"], ST["h2"]), Spacer(1, 4)]
    for i, q in enumerate(S["questions"], 1):
        flow += solution_flow(i, q)
    return flow


# ------------------------------------------------------------------ build
def build(set_paths, out, front=True):
    sets = [load_set(p) for p in set_paths]
    sets.sort(key=lambda s: s["number"])
    doc = Book(out)
    story = []
    if front:
        import front as FR
        story += FR.front_matter(ST, H2TOC, sets, md, paras, CodeBlock, RunningMark, TableOfContents)
    for S in sets:
        story += set_flow(S, len(sets))
    if front:
        import front as FR
        story += FR.back_matter(ST, H2TOC, sets, RunningMark, fmt_answer)
    doc.multiBuild(story)
    return doc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("sets", nargs="*")
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "GATE_DA_PDSA_50_Mock_Tests.pdf"))
    ap.add_argument("--no-front", action="store_true")
    a = ap.parse_args()
    paths = a.sets or sorted(glob.glob(os.path.join(ROOT, "sets", "set_*.py")))
    build(paths, a.out, front=not a.no_front)
    print("wrote", a.out)
