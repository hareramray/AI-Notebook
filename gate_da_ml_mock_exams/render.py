"""ReportLab rendering of questions, answer keys and solutions."""
from __future__ import annotations

import hashlib
import os
from typing import List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER, TA_LEFT  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (Image, KeepTogether, Paragraph, Preformatted, Spacer,  # noqa: E402
                                Table as RLTable, TableStyle)

from core import LETTERS, Code, Figure, Matrix, Q, Table, fmt  # noqa: E402

# ----------------------------------------------------------------------------
# Fonts & styles
# ----------------------------------------------------------------------------
_FONT_DIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("Serif", os.path.join(_FONT_DIR, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Bold", os.path.join(_FONT_DIR, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif-Italic", os.path.join(_FONT_DIR, "DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", os.path.join(_FONT_DIR, "DejaVuSerif-BoldItalic.ttf")))
pdfmetrics.registerFont(TTFont("Sans", os.path.join(_FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Bold", os.path.join(_FONT_DIR, "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Sans-Oblique", os.path.join(_FONT_DIR, "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("Sans-BoldOblique", os.path.join(_FONT_DIR, "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("Mono", os.path.join(_FONT_DIR, "DejaVuSansMono.ttf")))
pdfmetrics.registerFont(TTFont("Mono-Bold", os.path.join(_FONT_DIR, "DejaVuSansMono-Bold.ttf")))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic",
                              boldItalic="Serif-BoldItalic")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Oblique",
                              boldItalic="Sans-BoldOblique")
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold", italic="Mono", boldItalic="Mono-Bold")

MAROON = colors.HexColor("#6b1d1d")
INK = colors.HexColor("#1a1a1a")
SOFT = colors.HexColor("#f4ece1")
LINE = colors.HexColor("#b9a58c")
GREEN = colors.HexColor("#1d6b3a")

S = {
    "body": ParagraphStyle("body", fontName="Serif", fontSize=9.6, leading=13.2, textColor=INK),
    "opt": ParagraphStyle("opt", fontName="Serif", fontSize=9.4, leading=12.6, leftIndent=14, firstLineIndent=-14),
    "qhead": ParagraphStyle("qhead", fontName="Sans-Bold", fontSize=8.6, leading=11, textColor=MAROON),
    "sol": ParagraphStyle("sol", fontName="Serif", fontSize=9.2, leading=12.6, textColor=INK, leftIndent=6),
    "solhead": ParagraphStyle("solhead", fontName="Sans-Bold", fontSize=9, leading=12, textColor=GREEN),
    "cell": ParagraphStyle("cell", fontName="Serif", fontSize=8.6, leading=10.6, alignment=TA_CENTER),
    "cellL": ParagraphStyle("cellL", fontName="Serif", fontSize=8.6, leading=10.6, alignment=TA_LEFT),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=8.2, leading=10.4, leftIndent=8,
                           backColor=colors.HexColor("#f6f6f2"), borderPadding=4),
    "cap": ParagraphStyle("cap", fontName="Sans-Oblique", fontSize=7.8, leading=10, alignment=TA_CENTER,
                          textColor=colors.HexColor("#555555")),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=20, leading=25, textColor=MAROON, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=14, leading=18, textColor=MAROON, spaceBefore=6,
                         spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="Sans-Bold", fontSize=11, leading=14, textColor=INK, spaceBefore=6,
                         spaceAfter=3),
    "small": ParagraphStyle("small", fontName="Serif", fontSize=8.2, leading=10.5, textColor=INK),
}

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "figs")
os.makedirs(FIG_DIR, exist_ok=True)
FIG_DPI = 130

plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7, "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
})

_fig_counter = [0]


def figure_flowable(f: Figure):
    w_in, h_in = f.width_cm / 2.54, f.height_cm / 2.54
    fig = plt.figure(figsize=(w_in, h_in))
    f.draw(fig)
    _fig_counter[0] += 1
    path = os.path.join(FIG_DIR, f"fig_{os.getpid()}_{_fig_counter[0]:05d}.png")
    fig.savefig(path, dpi=FIG_DPI)
    plt.close(fig)
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        pw, ph = im.size
    width = min(f.width_cm * cm, 16 * cm)
    height = width * ph / pw
    img = Image(path, width=width, height=height)
    out = [Spacer(1, 3), img]
    if f.caption:
        out.append(Paragraph(f.caption, S["cap"]))
    out.append(Spacer(1, 3))
    return out


def table_flowable(t: Table):
    data = [[Paragraph(str(c), S["cell"]) for c in row] for row in t.rows]
    ncol = max(len(r) for r in t.rows)
    widths = [w * cm for w in t.col_widths_cm] if t.col_widths_cm else None
    if widths is None:
        maxlen = [max(len(str(r[j])) if j < len(r) else 0 for r in t.rows) for j in range(ncol)]
        raw = [max(1.1, min(5.5, 0.19 * m + 0.6)) for m in maxlen]
        tot = sum(raw)
        if tot > 16:
            raw = [r * 16 / tot for r in raw]
        widths = [r * cm for r in raw]
    tbl = RLTable(data, colWidths=widths, hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
             ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    if t.header:
        style += [("BACKGROUND", (0, 0), (-1, 0), SOFT)]
    else:
        style += [("BACKGROUND", (0, 0), (0, -1), SOFT)]
    tbl.setStyle(TableStyle(style))
    return [Spacer(1, 3), tbl, Spacer(1, 4)]


def matrix_flowable(m: Matrix):
    M = np.atleast_2d(np.asarray(m.M, dtype=float))
    if np.asarray(m.M).ndim == 1:
        M = M.T  # column vector
    r, c = M.shape
    data = []
    for i in range(r):
        row = [Paragraph(f"{m.name} =" if i == (r - 1) // 2 else "", S["cell"])]
        row += [Paragraph(fmt(M[i, j], m.digits), S["cell"]) for j in range(c)]
        data.append(row)
    namew = max(1.2, 0.22 * len(m.name) + 0.7)
    tbl = RLTable(data, colWidths=[namew * cm] + [1.25 * cm] * c, hAlign="LEFT")
    tbl.setStyle(TableStyle([
        ("LINEBEFORE", (1, 0), (1, -1), 0.9, INK), ("LINEAFTER", (-1, 0), (-1, -1), 0.9, INK),
        ("LINEABOVE", (1, 0), (1, 0), 0.9, INK), ("LINEBELOW", (1, -1), (1, -1), 0.9, INK),
        ("LINEABOVE", (-1, 0), (-1, 0), 0.9, INK), ("LINEBELOW", (-1, -1), (-1, -1), 0.9, INK),
        ("TOPPADDING", (0, 0), (-1, -1), 1), ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [Spacer(1, 2), tbl, Spacer(1, 3)]


def block_flowables(b, style="body"):
    if isinstance(b, str):
        return [Paragraph(b, S[style]), Spacer(1, 2)]
    if isinstance(b, Table):
        return table_flowable(b)
    if isinstance(b, Matrix):
        return matrix_flowable(b)
    if isinstance(b, Figure):
        return figure_flowable(b)
    if isinstance(b, Code):
        return [Preformatted(b.text, S["code"]), Spacer(1, 4)]
    raise TypeError(type(b))


def options_flowables(opts: List[str]):
    labelled = [f"<b>({LETTERS[i]})</b> {o}" for i, o in enumerate(opts)]
    plain_len = [len(o) for o in opts]
    if max(plain_len) <= 34 and not any("<br/>" in o for o in opts):
        data = [[Paragraph(labelled[0], S["opt"]), Paragraph(labelled[1], S["opt"])],
                [Paragraph(labelled[2], S["opt"]), Paragraph(labelled[3], S["opt"])]]
        t = RLTable(data, colWidths=[8 * cm, 8 * cm], hAlign="LEFT")
        t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        return [t]
    out = []
    for lo in labelled:
        p = Paragraph(lo, S["opt"])
        out.append(RLIndent(p))
    return out


def RLIndent(p):
    t = RLTable([[p]], colWidths=[16.2 * cm], hAlign="LEFT")
    t.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    return t


TYPE_NAME = {"MCQ": "MCQ", "MSQ": "MSQ (one or more correct)", "NAT": "NAT (numerical answer)"}


def question_flowables(num: int, q: Q, show_topic: bool = False):
    head = f"Q.{num}&nbsp;&nbsp;&nbsp;[{q.marks} mark{'s' if q.marks > 1 else ''} · {TYPE_NAME[q.qtype]}]"
    if show_topic:
        head += f"&nbsp;&nbsp;<font color='#777777'>{q.topic} – {q.subtopic}</font>"
    stem = q.text
    if q.qtype == "NAT" and q.nat_hint and q.nat_hint not in stem:
        stem += " " + q.nat_hint
    fl = [Paragraph(head, S["qhead"]), Paragraph(stem, S["body"]), Spacer(1, 2)]
    for b in q.blocks:
        fl += block_flowables(b)
    if q.qtype in ("MCQ", "MSQ"):
        fl += options_flowables(q.options)
    fl.append(Spacer(1, 9))
    return [KeepTogether(fl)]


def answer_text(q: Q) -> str:
    if q.qtype == "MCQ":
        return f"({LETTERS[q.answer]})"
    if q.qtype == "MSQ":
        return ", ".join(f"({LETTERS[a]})" for a in q.answer)
    lo, hi = q.answer
    if abs(lo - hi) < 1e-12:
        return fmt(lo, 4)
    return f"{fmt(lo, 4)} to {fmt(hi, 4)}"


def solution_flowables(num: int, q: Q):
    head = f"Q.{num} &nbsp;—&nbsp; Answer: {answer_text(q)} &nbsp;&nbsp;<font color='#777777' size='8'>" \
           f"[{q.qtype}, {q.marks}M · {q.topic} › {q.subtopic}]</font>"
    fl = [Paragraph(head, S["solhead"])]
    sol = q.solution if isinstance(q.solution, list) else [q.solution]
    for b in sol:
        fl += block_flowables(b, "sol")
    fl.append(Spacer(1, 7))
    return fl
