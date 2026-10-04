"""Vector diagram rendering (reportlab.graphics) for the GATE DA mock-exam book.

Every diagram is a plain dict with a "type" key. Supported types:

  bintree    {"type":"bintree", "tree":[val, left, right]}   (None = empty child)
             optional: "highlight":[vals], "null_leaves":False
  heap       {"type":"heap", "values":[...]}                  array drawn as complete binary tree
  tree       {"type":"tree", "root":"A", "children":{"A":["B","C"], ...}}  general rooted tree
  graph      {"type":"graph", "nodes":[...], "edges":[[u,v] or [u,v,w], ...], "directed":bool,
              optional "pos":{node:[x,y]}, "highlight":[nodes], "highlight_edges":[[u,v],...]}
  array      {"type":"array", "values":[...], "start":0, "show_index":True,
              optional "highlight":[idx], "pointers":{"name":idx}, "label":"A"}
  linkedlist {"type":"linkedlist", "values":[...], "doubly":False, "circular":False,
              optional "loop_to": idx  (last node points back to node at index idx — a cycle),
              optional "head":"head", "tail":None}
  hashtable  {"type":"hashtable", "size":m, "slots":{idx: value | [chain values]}}
  stack      {"type":"stack", "values":[bottom ... top], "label":"S"}
  queue      {"type":"queue", "values":[front ... rear]}
  matrix     {"type":"matrix", "rows":[[...]], "row_labels":[...], "col_labels":[...],
              optional "title":"...", "highlight":[[r,c],...]}
Common optional key: "caption".
"""
import math

from reportlab.graphics.shapes import Drawing, Circle, Line, String, Rect, Polygon, Group
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth

FONT = "DejaVuSans"
FONT_B = "DejaVuSans-Bold"
MONO = "DejaVuSansMono"

INK = colors.HexColor("#1f2937")
EDGE = colors.HexColor("#374151")
FILL = colors.HexColor("#e8f0fe")
HIL = colors.HexColor("#fde68a")
HIL_EDGE = colors.HexColor("#dc2626")
GRID = colors.HexColor("#9ca3af")
HEAD = colors.HexColor("#dbeafe")
MAXW = 440.0  # max drawing width in points


def _txt(v):
    return "" if v is None else str(v)


def _center_string(d, x, y, s, size=10, font=FONT, color=INK):
    w = stringWidth(s, font, size)
    d.add(String(x - w / 2.0, y - size * 0.35, s, fontName=font, fontSize=size, fillColor=color))


def _arrow(d, x1, y1, x2, y2, color=EDGE, width=1.0, head=6.0, shrink_end=0.0, shrink_start=0.0):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    sx, sy = x1 + ux * shrink_start, y1 + uy * shrink_start
    ex, ey = x2 - ux * shrink_end, y2 - uy * shrink_end
    d.add(Line(sx, sy, ex - ux * head * 0.6, ey - uy * head * 0.6, strokeColor=color, strokeWidth=width))
    px, py = -uy, ux
    pts = [ex, ey,
           ex - ux * head + px * head * 0.45, ey - uy * head + py * head * 0.45,
           ex - ux * head - px * head * 0.45, ey - uy * head - py * head * 0.45]
    d.add(Polygon(pts, fillColor=color, strokeColor=color, strokeWidth=0.5))


def _node(d, x, y, r, label, hl=False, size=None):
    d.add(Circle(x, y, r, fillColor=HIL if hl else FILL, strokeColor=HIL_EDGE if hl else EDGE,
                 strokeWidth=1.4 if hl else 1.0))
    s = _txt(label)
    fs = size or (10 if len(s) <= 3 else 8)
    _center_string(d, x, y, s, fs, FONT_B)


def _scale_drawing(d, w, h):
    if w > MAXW:
        f = MAXW / w
        g = Group(*d.contents)
        g.scale(f, f)
        nd = Drawing(w * f, h * f)
        nd.add(g)
        return nd
    return d


# ---------------------------------------------------------------- trees
def _layout_bintree(t):
    """In-order x positions, depth y. Returns list of (id, label, x, depth), edges, and stats."""
    nodes, edges = [], []
    counter = [0]

    def rec(node, depth, parent):
        if node is None:
            return None
        if not isinstance(node, (list, tuple)):
            node = [node, None, None]
        val = node[0]
        left = node[1] if len(node) > 1 else None
        right = node[2] if len(node) > 2 else None
        my = len(nodes)
        nodes.append([my, val, None, depth])
        lid = rec(left, depth + 1, my)
        nodes[my][2] = counter[0]
        counter[0] += 1
        rid = rec(right, depth + 1, my)
        if lid is not None:
            edges.append((my, lid))
        if rid is not None:
            edges.append((my, rid))
        return my

    rec(t, 0, None)
    return nodes, edges


def draw_bintree(spec):
    nodes, edges = _layout_bintree(spec["tree"])
    hl = set(_txt(v) for v in spec.get("highlight", []))
    if not nodes:
        return Drawing(10, 10)
    n = len(nodes)
    maxd = max(nd[3] for nd in nodes)
    r = 12
    xs = 30.0 if n > 12 else 36.0
    ys = 44.0
    w = (n - 1) * xs + 2 * r + 20
    h = maxd * ys + 2 * r + 16
    d = Drawing(w, h)
    pos = {nd[0]: (r + 10 + nd[2] * xs, h - r - 8 - nd[3] * ys) for nd in nodes}
    for a, b in edges:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        d.add(Line(x1, y1, x2, y2, strokeColor=EDGE, strokeWidth=1))
    for nd in nodes:
        x, y = pos[nd[0]]
        _node(d, x, y, r, nd[1], _txt(nd[1]) in hl)
    return _scale_drawing(d, w, h)


def heap_to_tree(values):
    def build(i):
        if i >= len(values) or values[i] is None:
            return None
        return [values[i], build(2 * i + 1), build(2 * i + 2)]
    return build(0)


def draw_heap(spec):
    vals = spec["values"]
    # Use level-based positions so the complete-tree shape is obvious
    n = len(vals)
    if n == 0:
        return Drawing(10, 10)
    depth = int(math.floor(math.log2(n)))
    r = 12
    leafgap = 30.0
    width_slots = 2 ** depth
    w = max(width_slots * leafgap, 60) + 20
    ys = 44.0
    h = depth * ys + 2 * r + 16
    d = Drawing(w, h)
    hl = set(spec.get("highlight", []))
    pos = {}
    for i in range(n):
        lvl = int(math.floor(math.log2(i + 1)))
        idx = i - (2 ** lvl - 1)
        slots = 2 ** lvl
        x = 10 + (idx + 0.5) * (w - 20) / slots
        y = h - r - 8 - lvl * ys
        pos[i] = (x, y)
    for i in range(1, n):
        p = (i - 1) // 2
        d.add(Line(pos[p][0], pos[p][1], pos[i][0], pos[i][1], strokeColor=EDGE, strokeWidth=1))
    for i in range(n):
        _node(d, pos[i][0], pos[i][1], r, vals[i], i in hl)
        if spec.get("show_index"):
            _center_string(d, pos[i][0] + r + 6, pos[i][1] + r, str(i), 7, FONT, GRID)
    return _scale_drawing(d, w, h)


def draw_tree(spec):
    root = spec["root"]
    ch = {str(k): [str(c) for c in v] for k, v in spec.get("children", {}).items()}
    labels = {str(k): str(v) for k, v in spec.get("labels", {}).items()}
    hl = set(str(v) for v in spec.get("highlight", []))
    pos_x, depth = {}, {}
    counter = [0.0]

    def rec(u, dep):
        depth[u] = dep
        kids = ch.get(u, [])
        if not kids:
            pos_x[u] = counter[0]
            counter[0] += 1
            return
        for k in kids:
            rec(k, dep + 1)
        pos_x[u] = (pos_x[kids[0]] + pos_x[kids[-1]]) / 2.0

    rec(str(root), 0)
    r = 12
    xs, ys = 34.0, 46.0
    w = (counter[0] - 1) * xs + 2 * r + 24
    h = max(depth.values()) * ys + 2 * r + 16
    d = Drawing(max(w, 40), h)
    P = {u: (r + 12 + pos_x[u] * xs, h - r - 8 - depth[u] * ys) for u in pos_x}
    for u, kids in ch.items():
        for k in kids:
            if u in P and k in P:
                d.add(Line(P[u][0], P[u][1], P[k][0], P[k][1], strokeColor=EDGE, strokeWidth=1))
    for u in P:
        _node(d, P[u][0], P[u][1], r, labels.get(u, u), u in hl)
    return _scale_drawing(d, max(w, 40), h)


# ---------------------------------------------------------------- graphs
def _auto_pos(nodes, edges, directed):
    import networkx as nx
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from([(e[0], e[1]) for e in edges])
    n = len(nodes)
    if n <= 1:
        return {nodes[0]: (0, 0)} if nodes else {}
    try:
        if nx.is_connected(G.to_undirected()) and n >= 3:
            p = nx.kamada_kawai_layout(G.to_undirected())
        else:
            p = nx.spring_layout(G, seed=7)
    except Exception:
        p = nx.circular_layout(G)
    return {k: (float(v[0]), float(v[1])) for k, v in p.items()}


def draw_graph(spec):
    nodes = [str(x) for x in spec["nodes"]]
    edges = [[str(e[0]), str(e[1])] + list(e[2:]) for e in spec.get("edges", [])]
    directed = spec.get("directed", False)
    hl = set(str(x) for x in spec.get("highlight", []))
    hle = set((str(a), str(b)) for a, b in spec.get("highlight_edges", []))
    if "pos" in spec:
        pos = {str(k): (float(v[0]), float(v[1])) for k, v in spec["pos"].items()}
        for nd in nodes:
            pos.setdefault(nd, (0.0, 0.0))
    else:
        pos = _auto_pos(nodes, edges, directed)
    xsv = [p[0] for p in pos.values()]
    ysv = [p[1] for p in pos.values()]
    minx, maxx, miny, maxy = min(xsv), max(xsv), min(ysv), max(ysv)
    spanx, spany = (maxx - minx) or 1.0, (maxy - miny) or 1.0
    r = 13
    n = len(nodes)
    target_w = min(MAXW - 40, 90 + 45 * n) if "pos" not in spec else min(MAXW - 40, 80 * spanx)
    target_w = max(target_w, 120)
    sc = target_w / spanx
    target_h = spany * sc
    if target_h > 230:
        sc = 230 / spany
        target_h = 230
    if maxy == miny:
        target_h = 0
    pad = r + 14
    w = (maxx - minx) * sc + 2 * pad
    h = target_h + 2 * pad
    d = Drawing(w, h)
    P = {k: (pad + (v[0] - minx) * sc, pad + (v[1] - miny) * sc) for k, v in pos.items()}
    pairs = set((e[0], e[1]) for e in edges)
    for e in edges:
        a, b = e[0], e[1]
        (x1, y1), (x2, y2) = P[a], P[b]
        hot = (a, b) in hle or (not directed and (b, a) in hle)
        col = HIL_EDGE if hot else EDGE
        wid = 2.0 if hot else 1.0
        offx = offy = 0.0
        if directed and (b, a) in pairs and a != b:
            L = math.hypot(x2 - x1, y2 - y1) or 1
            offx, offy = -(y2 - y1) / L * 5, (x2 - x1) / L * 5
        if a == b:
            d.add(Circle(x1, y1 + r + 6, 7, fillColor=None, strokeColor=col, strokeWidth=wid))
            mx, my = x1, y1 + r + 20
        elif directed:
            _arrow(d, x1 + offx, y1 + offy, x2 + offx, y2 + offy, col, wid, 7, shrink_end=r, shrink_start=r)
            mx, my = (x1 + x2) / 2 + offx * 1.6, (y1 + y2) / 2 + offy * 1.6
        else:
            d.add(Line(x1, y1, x2, y2, strokeColor=col, strokeWidth=wid))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if len(e) > 2 and e[2] is not None:
            s = _txt(e[2])
            tw = stringWidth(s, FONT_B, 8.5) + 4
            d.add(Rect(mx - tw / 2, my - 6, tw, 12, fillColor=colors.white, strokeColor=None))
            _center_string(d, mx, my, s, 8.5, FONT_B, colors.HexColor("#1d4ed8"))
    for k in nodes:
        _node(d, P[k][0], P[k][1], r, k, k in hl)
    return _scale_drawing(d, w, h)


# ---------------------------------------------------------------- linear structures
def _cellw(values, size=10, minw=26):
    return max([minw] + [stringWidth(_txt(v), FONT_B, size) + 12 for v in values])


def draw_array(spec):
    vals = spec["values"]
    start = spec.get("start", 0)
    show_idx = spec.get("show_index", True)
    hl = set(spec.get("highlight", []))
    pointers = spec.get("pointers", {})
    label = spec.get("label")
    cw = _cellw(vals)
    ch = 24
    lw = stringWidth(label + " =", FONT_B, 10) + 8 if label else 0
    n = len(vals)
    ptr_rows = 1 if pointers else 0
    w = lw + n * cw + 10
    h = ch + (14 if show_idx else 0) + (30 if ptr_rows else 0) + 6
    d = Drawing(w, h)
    y0 = h - ch - 3
    if label:
        _center_string(d, lw / 2, y0 + ch / 2, label + " =", 10, FONT_B)
    for i, v in enumerate(vals):
        x = lw + i * cw
        d.add(Rect(x, y0, cw, ch, fillColor=HIL if (i + start) in hl else colors.white,
                   strokeColor=EDGE, strokeWidth=1))
        _center_string(d, x + cw / 2, y0 + ch / 2, _txt(v), 10, MONO)
        if show_idx:
            _center_string(d, x + cw / 2, y0 - 8, str(i + start), 7.5, FONT, GRID)
    # pointers below
    by_idx = {}
    for name, idx in pointers.items():
        by_idx.setdefault(idx, []).append(name)
    for idx, names in by_idx.items():
        x = lw + (idx - start) * cw + cw / 2
        ytop = y0 - (16 if show_idx else 4)
        _arrow(d, x, ytop - 14, x, ytop, colors.HexColor("#1d4ed8"), 1, 5)
        _center_string(d, x, ytop - 20, ",".join(names), 8, FONT_B, colors.HexColor("#1d4ed8"))
    return _scale_drawing(d, w, h)


def draw_linkedlist(spec):
    vals = spec["values"]
    doubly = spec.get("doubly", False)
    loop_to = spec.get("loop_to")
    circular = spec.get("circular", False) or loop_to is not None
    head = spec.get("head", "head")
    tail = spec.get("tail")
    dw = _cellw(vals, 10, 28)
    pw = 12
    boxw = dw + pw * (2 if doubly else 1)
    gap = 26
    bh = 22
    n = len(vals)
    lw = (stringWidth(head, FONT_B, 9) + 18) if head else 0
    w = lw + n * (boxw + gap) + 30
    h = bh + (34 if circular else 12) + (16 if tail else 0)
    d = Drawing(w, h)
    y0 = h - bh - 6
    if head:
        _center_string(d, lw / 2 - 6, y0 + bh / 2, head, 9, FONT_B, colors.HexColor("#1d4ed8"))
        _arrow(d, lw - 14, y0 + bh / 2, lw, y0 + bh / 2, colors.HexColor("#1d4ed8"), 1, 5)
    xs = []
    for i, v in enumerate(vals):
        x = lw + i * (boxw + gap)
        xs.append(x)
        off = pw if doubly else 0
        if doubly:
            d.add(Rect(x, y0, pw, bh, fillColor=HEAD, strokeColor=EDGE))
        d.add(Rect(x + off, y0, dw, bh, fillColor=colors.white, strokeColor=EDGE))
        _center_string(d, x + off + dw / 2, y0 + bh / 2, _txt(v), 10, MONO)
        d.add(Rect(x + off + dw, y0, pw, bh, fillColor=HEAD, strokeColor=EDGE))
        if i < n - 1:
            sx = x + off + dw + pw / 2
            _arrow(d, sx, y0 + bh * 0.65, x + boxw + gap, y0 + bh * 0.65, EDGE, 1, 5)
            if doubly:
                _arrow(d, x + boxw + gap + pw / 2, y0 + bh * 0.3, x + boxw, y0 + bh * 0.3, EDGE, 1, 5)
    if n:
        lastx = xs[-1] + boxw
        if circular:
            sx = lastx - pw / 2
            d.add(Line(sx, y0, sx, y0 - 14, strokeColor=EDGE))
            d.add(Line(sx, y0 - 14, xs[loop_to if loop_to is not None else 0] + 8, y0 - 14, strokeColor=EDGE))
            tgt = xs[loop_to if loop_to is not None else 0] + 8
            d.add(Line(tgt, y0 - 14, tgt, y0 - 14, strokeColor=EDGE))
            _arrow(d, tgt, y0 - 14, tgt, y0, EDGE, 1, 5)
        else:
            _center_string(d, lastx + 14, y0 + bh / 2, "∅", 11, FONT_B)
        if tail:
            tx = xs[-1] + boxw / 2
            _arrow(d, tx, y0 - (30 if circular else 14) + 2, tx, y0, colors.HexColor("#1d4ed8"), 1, 5)
            _center_string(d, tx, y0 - (34 if circular else 18), tail, 8, FONT_B, colors.HexColor("#1d4ed8"))
    return _scale_drawing(d, w, h)


def draw_hashtable(spec):
    m = spec["size"]
    slots = {int(k): v for k, v in spec.get("slots", {}).items()}
    rowh = 18
    iw = 26
    cw = 50
    chain = any(isinstance(v, (list, tuple)) for v in slots.values())
    maxchain = max([len(v) for v in slots.values() if isinstance(v, (list, tuple))] + [0])
    w = iw + cw + (maxchain * 56 + 10 if chain else 10)
    h = m * rowh + 6
    d = Drawing(w, h)
    for i in range(m):
        y = h - 3 - (i + 1) * rowh
        _center_string(d, iw / 2, y + rowh / 2, str(i), 8.5, FONT, GRID)
        v = slots.get(i)
        d.add(Rect(iw, y, cw, rowh, fillColor=colors.white, strokeColor=EDGE))
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            if not v:
                continue
            _center_string(d, iw + cw / 2, y + rowh / 2, "•", 10, FONT_B)
            px = iw + cw / 2
            for j, item in enumerate(v):
                bx = iw + cw + 14 + j * 56
                _arrow(d, px, y + rowh / 2, bx, y + rowh / 2, EDGE, 0.8, 4)
                d.add(Rect(bx, y + 2, 38, rowh - 4, fillColor=FILL, strokeColor=EDGE))
                _center_string(d, bx + 19, y + rowh / 2, _txt(item), 8.5, MONO)
                px = bx + 38
        else:
            _center_string(d, iw + cw / 2, y + rowh / 2, _txt(v), 9, MONO)
    return _scale_drawing(d, w, h)


def draw_stack(spec):
    vals = spec["values"]
    cw = _cellw(vals, 10, 50)
    ch = 20
    n = len(vals)
    label = spec.get("label", "")
    w = cw + 90
    h = max(n, 1) * ch + 26
    d = Drawing(w, h)
    x0 = 30
    d.add(Line(x0, 6, x0, h - 6, strokeColor=EDGE, strokeWidth=1.6))
    d.add(Line(x0 + cw, 6, x0 + cw, h - 6, strokeColor=EDGE, strokeWidth=1.6))
    d.add(Line(x0, 6, x0 + cw, 6, strokeColor=EDGE, strokeWidth=1.6))
    for i, v in enumerate(vals):
        y = 6 + i * ch
        d.add(Rect(x0 + 2, y + 1, cw - 4, ch - 2, fillColor=FILL, strokeColor=EDGE, strokeWidth=0.6))
        _center_string(d, x0 + cw / 2, y + ch / 2, _txt(v), 10, MONO)
    if n:
        ty = 6 + (n - 1) * ch + ch / 2
        _arrow(d, x0 + cw + 40, ty, x0 + cw + 4, ty, colors.HexColor("#1d4ed8"), 1, 5)
        _center_string(d, x0 + cw + 58, ty, "top", 8, FONT_B, colors.HexColor("#1d4ed8"))
    if label:
        _center_string(d, x0 + cw / 2, 0, label, 8, FONT_B)
    return _scale_drawing(d, w, h)


def draw_queue(spec):
    vals = spec["values"]
    cw = _cellw(vals)
    ch = 24
    n = len(vals)
    w = n * cw + 90
    h = ch + 30
    d = Drawing(w, h)
    x0 = 45
    y0 = 18
    d.add(Line(x0 - 6, y0 - 3, x0 + n * cw + 6, y0 - 3, strokeColor=EDGE, strokeWidth=1.6))
    d.add(Line(x0 - 6, y0 + ch + 3, x0 + n * cw + 6, y0 + ch + 3, strokeColor=EDGE, strokeWidth=1.6))
    for i, v in enumerate(vals):
        d.add(Rect(x0 + i * cw, y0, cw, ch, fillColor=FILL, strokeColor=EDGE, strokeWidth=0.6))
        _center_string(d, x0 + i * cw + cw / 2, y0 + ch / 2, _txt(v), 10, MONO)
    _center_string(d, 20, y0 + ch / 2, "front", 8, FONT_B, colors.HexColor("#1d4ed8"))
    _center_string(d, x0 + n * cw + 26, y0 + ch / 2, "rear", 8, FONT_B, colors.HexColor("#1d4ed8"))
    return _scale_drawing(d, w, h)


def draw_matrix(spec):
    rows = spec["rows"]
    rl = spec.get("row_labels")
    cl = spec.get("col_labels")
    hl = set(tuple(x) for x in spec.get("highlight", []))
    title = spec.get("title")
    ncols = max(len(r) for r in rows)
    allv = [c for r in rows for c in r] + (cl or [])
    cw = _cellw(allv, 9, 26)
    rw = (max(stringWidth(_txt(x), FONT_B, 9) for x in rl) + 12) if rl else 0
    ch = 18
    th = 16 if title else 0
    w = rw + ncols * cw + 4
    h = (len(rows) + (1 if cl else 0)) * ch + 4 + th
    d = Drawing(w, h)
    top = h - 2 - th
    if title:
        _center_string(d, w / 2, h - 8, title, 9, FONT_B)
    if cl:
        for j, c in enumerate(cl):
            _center_string(d, rw + j * cw + cw / 2, top - ch / 2, _txt(c), 9, FONT_B, colors.HexColor("#1d4ed8"))
        top -= ch
    for i, r in enumerate(rows):
        y = top - (i + 1) * ch
        if rl:
            _center_string(d, rw / 2, y + ch / 2, _txt(rl[i]), 9, FONT_B, colors.HexColor("#1d4ed8"))
        for j in range(ncols):
            v = r[j] if j < len(r) else ""
            d.add(Rect(rw + j * cw, y, cw, ch, fillColor=HIL if (i, j) in hl else colors.white,
                       strokeColor=GRID, strokeWidth=0.7))
            _center_string(d, rw + j * cw + cw / 2, y + ch / 2, _txt(v), 9, MONO)
    return _scale_drawing(d, w, h)


RENDERERS = {
    "bintree": draw_bintree,
    "heap": draw_heap,
    "tree": draw_tree,
    "graph": draw_graph,
    "array": draw_array,
    "linkedlist": draw_linkedlist,
    "hashtable": draw_hashtable,
    "stack": draw_stack,
    "queue": draw_queue,
    "matrix": draw_matrix,
}


def render(spec):
    t = spec.get("type")
    if t not in RENDERERS:
        raise ValueError("unknown diagram type %r" % t)
    return RENDERERS[t](spec)
