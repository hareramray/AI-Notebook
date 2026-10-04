"""Vector diagram helpers (ReportLab graphics) for graphs, game trees and DAGs."""
import math
from reportlab.graphics.shapes import Drawing, Circle, Line, String, Polygon, Rect
from reportlab.lib import colors

FONT = "DejaVu"
FONT_B = "DejaVu-Bold"

INK = colors.HexColor("#1f2937")
NODE_FILL = colors.HexColor("#e8f0fe")
NODE_STROKE = colors.HexColor("#1a56db")
START_FILL = colors.HexColor("#d1fae5")
GOAL_FILL = colors.HexColor("#fde68a")
EDGE = colors.HexColor("#4b5563")
LABEL_BG = colors.white
MAX_FILL = colors.HexColor("#dbeafe")
MIN_FILL = colors.HexColor("#fee2e2")
CHANCE_FILL = colors.HexColor("#ede9fe")
LEAF_FILL = colors.HexColor("#f3f4f6")
EVID_FILL = colors.HexColor("#fde68a")
QUERY_FILL = colors.HexColor("#bbf7d0")


def _arrow(d, x1, y1, x2, y2, r1, r2, color=EDGE, width=1.1, head=7):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    sx, sy = x1 + ux * r1, y1 + uy * r1
    ex, ey = x2 - ux * r2, y2 - uy * r2
    d.add(Line(sx, sy, ex - ux * head * 0.6, ey - uy * head * 0.6, strokeColor=color, strokeWidth=width))
    px, py = -uy, ux
    d.add(Polygon([ex, ey,
                   ex - ux * head + px * head * 0.45, ey - uy * head + py * head * 0.45,
                   ex - ux * head - px * head * 0.45, ey - uy * head - py * head * 0.45],
                  fillColor=color, strokeColor=color, strokeWidth=0.5))


def _label(d, x, y, text, size=8.5, color=INK, bg=True, bold=False):
    w = len(str(text)) * size * 0.58 + 4
    if bg:
        d.add(Rect(x - w / 2, y - size * 0.45, w, size * 1.25, fillColor=LABEL_BG,
                   strokeColor=None, strokeWidth=0))
    d.add(String(x, y - size * 0.1, str(text), fontName=FONT_B if bold else FONT,
                 fontSize=size, fillColor=color, textAnchor="middle"))


def graph_drawing(pos, edges, directed=False, width=420, height=200, radius=13,
                  node_note=None, start=None, goal=None, fills=None, edge_labels=True,
                  margin=28, title=None):
    """pos: {name: (x,y) in [0,1]}, edges: list of (u, v, label_or_None)."""
    top_pad = 14 if title else 0
    d = Drawing(width, height + top_pad)
    W, H = width - 2 * margin, height - 2 * margin

    def P(n):
        x, y = pos[n]
        return margin + x * W, margin + y * H

    for (u, v, lab) in edges:
        x1, y1 = P(u)
        x2, y2 = P(v)
        if directed:
            _arrow(d, x1, y1, x2, y2, radius, radius + 1)
        else:
            d.add(Line(x1, y1, x2, y2, strokeColor=EDGE, strokeWidth=1.1))
        if edge_labels and lab is not None:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            _label(d, mx, my, lab, size=8.5, color=colors.HexColor("#b91c1c"), bold=True)
    for n in pos:
        x, y = P(n)
        fill = NODE_FILL
        if fills and n in fills:
            fill = fills[n]
        elif n == start:
            fill = START_FILL
        elif n == goal:
            fill = GOAL_FILL
        d.add(Circle(x, y, radius, fillColor=fill, strokeColor=NODE_STROKE, strokeWidth=1.2))
        d.add(String(x, y - 3.5, str(n), fontName=FONT_B, fontSize=10 if len(str(n)) < 3 else 7.5,
                     fillColor=INK, textAnchor="middle"))
        if node_note and n in node_note:
            d.add(String(x, y + radius + 3, str(node_note[n]), fontName=FONT, fontSize=7.8,
                         fillColor=colors.HexColor("#065f46"), textAnchor="middle"))
    if title:
        d.add(String(width / 2, height + 2, title, fontName=FONT_B, fontSize=8.5,
                     fillColor=INK, textAnchor="middle"))
    return d


# ----------------------------------------------------------------- game trees
def tree_drawing(tree, kinds, leaf_vals, edge_labels=None, width=440, level_h=48,
                 node_names=None, show_names=True, marks=None):
    """tree: {node: [children]} with root 'R'. kinds: {node: 'max'|'min'|'chance'|'leaf'}.
    leaf_vals: {leaf: value}. edge_labels: {(p,c): text}. marks: {node: text under node}."""
    # leaf order (left to right)
    leaves = []

    def collect(n):
        if not tree.get(n):
            leaves.append(n)
        for c in tree.get(n, []):
            collect(c)
    collect("R")
    depth = {}

    def setd(n, k):
        depth[n] = k
        for c in tree.get(n, []):
            setd(c, k + 1)
    setd("R", 0)
    maxd = max(depth.values())
    nleaf = len(leaves)
    slot = (width - 30) / max(nleaf, 1)
    xs = {}
    for i, l in enumerate(leaves):
        xs[l] = 15 + slot * (i + 0.5)

    def setx(n):
        if n in xs:
            return xs[n]
        cx = [setx(c) for c in tree[n]]
        xs[n] = sum(cx) / len(cx)
        return xs[n]
    setx("R")
    height = level_h * maxd + 50
    d = Drawing(width, height)

    def Y(n):
        return height - 20 - depth[n] * level_h

    r = 11 if slot >= 24 else 9
    for n, ch in tree.items():
        for c in ch:
            d.add(Line(xs[n], Y(n) - r, xs[c], Y(c) + r, strokeColor=EDGE, strokeWidth=1))
            if edge_labels and (n, c) in edge_labels:
                mx, my = (xs[n] + xs[c]) / 2, (Y(n) + Y(c)) / 2
                _label(d, mx, my, edge_labels[(n, c)], size=7.5, color=colors.HexColor("#6d28d9"))
    for n in xs:
        x, y = xs[n], Y(n)
        k = kinds.get(n, "leaf")
        if k == "max":
            d.add(Polygon([x, y + r, x - r * 1.1, y - r * 0.8, x + r * 1.1, y - r * 0.8],
                          fillColor=MAX_FILL, strokeColor=NODE_STROKE, strokeWidth=1.1))
        elif k == "min":
            d.add(Polygon([x, y - r, x - r * 1.1, y + r * 0.8, x + r * 1.1, y + r * 0.8],
                          fillColor=MIN_FILL, strokeColor=colors.HexColor("#b91c1c"), strokeWidth=1.1))
        elif k == "chance":
            d.add(Circle(x, y, r * 0.9, fillColor=CHANCE_FILL, strokeColor=colors.HexColor("#6d28d9"),
                         strokeWidth=1.1))
        else:
            w = max(r * 1.7, slot * 0.8) if slot < 30 else r * 1.9
            w = min(w, r * 2.2)
            d.add(Rect(x - w / 2, y - r * 0.8, w, r * 1.6, fillColor=LEAF_FILL, strokeColor=INK,
                       strokeWidth=0.8))
            d.add(String(x, y - 3, str(leaf_vals[n]), fontName=FONT_B, fontSize=8.5 if r > 9 else 7.5,
                         fillColor=INK, textAnchor="middle"))
        if show_names and k != "leaf" and node_names and n in node_names:
            d.add(String(x + r * 1.25, y + 2, node_names[n], fontName=FONT, fontSize=7.5,
                         fillColor=colors.HexColor("#374151"), textAnchor="start"))
        if k == "leaf" and node_names and n in node_names:
            d.add(String(x, y - r - 9, node_names[n], fontName=FONT, fontSize=6.8,
                         fillColor=colors.HexColor("#6b7280"), textAnchor="middle"))
        if marks and n in marks:
            d.add(String(x, y - r - 18, marks[n], fontName=FONT, fontSize=7,
                         fillColor=colors.HexColor("#b91c1c"), textAnchor="middle"))
    return d


def legend_game(chance=False):
    d = Drawing(440, 18)
    x = 10
    d.add(Polygon([x + 6, 14, x, 4, x + 12, 4], fillColor=MAX_FILL, strokeColor=NODE_STROKE))
    d.add(String(x + 16, 5, "MAX node", fontName=FONT, fontSize=8, fillColor=INK))
    x = 95
    if chance:
        d.add(Circle(x + 6, 9, 6, fillColor=CHANCE_FILL, strokeColor=colors.HexColor("#6d28d9")))
        d.add(String(x + 16, 5, "CHANCE node (edge = probability)", fontName=FONT, fontSize=8, fillColor=INK))
    else:
        d.add(Polygon([x + 6, 4, x, 14, x + 12, 14], fillColor=MIN_FILL,
                      strokeColor=colors.HexColor("#b91c1c")))
        d.add(String(x + 16, 5, "MIN node", fontName=FONT, fontSize=8, fillColor=INK))
    x = 300
    d.add(Rect(x, 3, 14, 11, fillColor=LEAF_FILL, strokeColor=INK, strokeWidth=0.8))
    d.add(String(x + 18, 5, "terminal utility", fontName=FONT, fontSize=8, fillColor=INK))
    return d
