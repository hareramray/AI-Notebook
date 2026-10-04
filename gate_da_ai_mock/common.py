"""Shared question model, styles and small helpers."""
from dataclasses import dataclass, field
from typing import Any, List, Optional

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.fonts import addMapping

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DejaVu", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuMono", FD + "DejaVuSansMono.ttf"))
addMapping("DejaVu", 0, 0, "DejaVu")
addMapping("DejaVu", 1, 0, "DejaVu-Bold")
addMapping("DejaVu", 0, 1, "DejaVu-Oblique")
addMapping("DejaVu", 1, 1, "DejaVu-BoldOblique")

ACCENT = colors.HexColor("#7f1d1d")
BLUE = colors.HexColor("#1a56db")
GREY = colors.HexColor("#6b7280")
LIGHT = colors.HexColor("#f3f4f6")

ST = {
    "body": ParagraphStyle("body", fontName="DejaVu", fontSize=9.6, leading=13.4, alignment=TA_JUSTIFY),
    "q": ParagraphStyle("q", fontName="DejaVu", fontSize=9.8, leading=13.8, alignment=TA_LEFT),
    "opt": ParagraphStyle("opt", fontName="DejaVu", fontSize=9.4, leading=12.8, leftIndent=18,
                          firstLineIndent=-16, spaceBefore=1.5),
    "sol": ParagraphStyle("sol", fontName="DejaVu", fontSize=9.0, leading=12.6, alignment=TA_LEFT),
    "solb": ParagraphStyle("solb", fontName="DejaVu", fontSize=9.0, leading=12.6, leftIndent=12,
                           bulletIndent=2),
    "cell": ParagraphStyle("cell", fontName="DejaVu", fontSize=8.0, leading=10, alignment=TA_CENTER),
    "cellL": ParagraphStyle("cellL", fontName="DejaVu", fontSize=8.0, leading=10, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", fontName="DejaVu-Bold", fontSize=20, leading=25, textColor=ACCENT,
                         spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="DejaVu-Bold", fontSize=13.5, leading=18, textColor=ACCENT,
                         spaceBefore=6, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName="DejaVu-Bold", fontSize=11, leading=15, textColor=BLUE,
                         spaceBefore=5, spaceAfter=3),
    "small": ParagraphStyle("small", fontName="DejaVu", fontSize=8, leading=10.5, textColor=GREY),
    "center": ParagraphStyle("center", fontName="DejaVu", fontSize=10, leading=14, alignment=TA_CENTER),
    "mono": ParagraphStyle("mono", fontName="DejaVuMono", fontSize=8.2, leading=10.6),
}


@dataclass
class Q:
    topic: str
    qtype: str            # MCQ | MSQ | NAT
    marks: int
    text: str
    options: Optional[List[str]] = None
    answer: Any = None    # list of indices, or (lo, hi)
    solution: List[Any] = field(default_factory=list)   # str or flowables
    figures: List[Any] = field(default_factory=list)    # flowables shown with question
    subtopic: str = ""


def make_mcq(correct, distractors, rng):
    seen = [correct]
    for x in distractors:
        if x not in seen:
            seen.append(x)
        if len(seen) == 4:
            break
    if len(seen) < 4:
        raise ValueError("not enough distinct distractors")
    opts = seen[:]
    rng.shuffle(opts)
    return opts, [opts.index(correct)]


def make_msq(statements, rng, shuffle=True):
    """statements: list of (text, truth). Requires at least one true."""
    st = list(statements)
    if shuffle:
        rng.shuffle(st)
    return [s for s, _ in st], [i for i, (_, t) in enumerate(st) if t]


def num(x, nd=3):
    s = f"{x:.{nd}f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def tbl(rows, widths=None, header=True, font=8.0, zebra=True, align="CENTER", hl=None):
    """rows: list of lists of str (markup allowed). hl: set of (row, col) to highlight."""
    sty = ST["cell"] if align == "CENTER" else ST["cellL"]
    data = [[Paragraph(str(c), sty) for c in r] for r in rows]
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    cmds = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ca3af")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if header:
        cmds.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")))
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f9fafb")))
    for (r, c) in (hl or []):
        cmds.append(("BACKGROUND", (c, r), (c, r), colors.HexColor("#fef3c7")))
    t.setStyle(TableStyle(cmds))
    return t


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
