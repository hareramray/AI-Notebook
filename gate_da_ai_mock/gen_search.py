"""Parameterised generators: uninformed and informed search on random graphs."""
import heapq
import math

from reportlab.platypus import Paragraph, Spacer
from common import Q, make_mcq, make_msq, num, tbl, ST
from draw import graph_drawing

LETTERS = list("ABCDEFHIJKLMNPR")


def _segments_cross(p1, p2, p3, p4):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if len({p1, p2, p3, p4}) < 4:
        return False
    d1, d2 = orient(p3, p4, p1), orient(p3, p4, p2)
    d3, d4 = orient(p1, p2, p3), orient(p1, p2, p4)
    return (d1 * d2 < 0) and (d3 * d4 < 0)


def random_graph(rng, n=8, min_hops=3, weighted=True):
    while True:
        cols, rows = 5, 3
        cells = [(c, r) for c in range(cols) for r in range(rows)]
        s_cell = (0, rng.randrange(rows))
        g_cell = (cols - 1, rng.randrange(rows))
        mids = [c for c in cells if c[0] not in (0, cols - 1)]
        rest = rng.sample(mids, n - 2)
        chosen = [s_cell] + rest + [g_cell]
        names = ["S"] + rng.sample(LETTERS[:n + 2], n - 2) + ["G"]
        pos = {}
        for nm, (c, r) in zip(names, chosen):
            pos[nm] = ((c + rng.uniform(-0.18, 0.18)) / (cols - 1),
                       (r + rng.uniform(-0.2, 0.2)) / (rows - 1))
        for k in pos:
            pos[k] = (min(1, max(0, pos[k][0])), min(1, max(0, pos[k][1])))
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                a, b = names[i], names[j]
                dx = (pos[a][0] - pos[b][0]) * 4
                dy = (pos[a][1] - pos[b][1]) * 2
                pairs.append((math.hypot(dx, dy), a, b))
        pairs.sort()
        edges = []
        deg = {k: 0 for k in names}
        for dist, a, b in pairs:
            if dist > 2.3 or deg[a] >= 4 or deg[b] >= 4:
                continue
            if any(_segments_cross(pos[a], pos[b], pos[u], pos[v]) for u, v in edges):
                continue
            if {a, b} == {"S", "G"}:
                continue
            if rng.random() < 0.82:
                edges.append((a, b))
                deg[a] += 1
                deg[b] += 1
        adj = {k: set() for k in names}
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        # connectivity & hop distance
        seen = {"S": 0}
        fr = ["S"]
        while fr:
            x = fr.pop(0)
            for y in adj[x]:
                if y not in seen:
                    seen[y] = seen[x] + 1
                    fr.append(y)
        if len(seen) != n or seen["G"] < min_hops:
            continue
        if any(len(adj[k]) == 0 for k in names):
            continue
        w = {}
        for a, b in edges:
            dx = (pos[a][0] - pos[b][0]) * 4
            dy = (pos[a][1] - pos[b][1]) * 2
            base = math.hypot(dx, dy) * 3
            w[frozenset((a, b))] = max(1, min(12, int(round(base + rng.randint(-1, 3)))))
        return dict(names=names, pos=pos, edges=edges, adj=adj, w=w)


def W(g, a, b):
    return g["w"][frozenset((a, b))]


def dijkstra_from(g, src):
    dist = {src: 0}
    pq = [(0, src)]
    while pq:
        d, x = heapq.heappop(pq)
        if d > dist[x]:
            continue
        for y in g["adj"][x]:
            nd = d + W(g, x, y)
            if nd < dist.get(y, 1e9):
                dist[y] = nd
                heapq.heappush(pq, (nd, y))
    return dist


def bfs(g, reverse=False):
    order, parent, fr, reached, trace = [], {"S": None}, ["S"], {"S"}, []
    while fr:
        n = fr.pop(0)
        order.append(n)
        if n == "G":
            trace.append((n, list(fr)))
            break
        for m in sorted(g["adj"][n], reverse=reverse):
            if m not in reached:
                reached.add(m)
                parent[m] = n
                fr.append(m)
        trace.append((n, list(fr)))
    return order, _path(parent, "G"), trace


def dfs(g, reverse=False):
    order, parent, visited = [], {"S": None}, set()
    found = [False]

    def visit(n):
        if found[0]:
            return
        visited.add(n)
        order.append(n)
        if n == "G":
            found[0] = True
            return
        for m in sorted(g["adj"][n], reverse=reverse):
            if m not in visited and not found[0]:
                parent[m] = n
                visit(m)
    visit("S")
    return order, _path(parent, "G")


def _path(parent, t):
    p = []
    while t is not None:
        p.append(t)
        t = parent[t]
    return p[::-1]


def best_first(g, h=None, mode="ucs"):
    """mode: ucs (g), astar (g+h), greedy (h). Graph search, goal test at expansion,
    ties broken alphabetically. Returns expansions, path, cost, trace."""
    h = h or {}

    def key(gv, n):
        if mode == "ucs":
            return gv
        if mode == "astar":
            return gv + h[n]
        return h[n]
    gbest = {"S": 0}
    parent = {"S": None}
    pq = [(key(0, "S"), "S", 0)]
    explored = set()
    order, trace = [], []
    while pq:
        k, n, gv = heapq.heappop(pq)
        if n in explored or gv != gbest.get(n):
            continue
        order.append(n)
        if n == "G":
            trace.append((n, k, gv, sorted([(kk, nn) for kk, nn, gg in pq
                                            if nn not in explored and gg == gbest.get(nn)])))
            break
        explored.add(n)
        for m in sorted(g["adj"][n]):
            ng = gv + W(g, n, m)
            if m in explored:
                continue
            if mode == "greedy":
                if m in gbest:
                    continue
            elif ng >= gbest.get(m, 1e9):
                continue
            gbest[m] = ng
            parent[m] = n
            heapq.heappush(pq, (key(ng, m), m, ng))
        trace.append((n, k, gv, sorted([(kk, nn) for kk, nn, gg in pq
                                        if nn not in explored and gg == gbest.get(nn)])))
    path = _path(parent, "G")
    cost = sum(W(g, path[i], path[i + 1]) for i in range(len(path) - 1))
    return order, path, cost, trace


def _fig(g, note=None, width=430, height=175):
    edges = [(a, b, W(g, a, b)) for a, b in g["edges"]]
    return graph_drawing(g["pos"], edges, width=width, height=height, node_note=note,
                         start="S", goal="G")


def _fig_unweighted(g):
    edges = [(a, b, None) for a, b in g["edges"]]
    return graph_drawing(g["pos"], edges, width=430, height=165, start="S", goal="G")


def other_paths(g, path, rng, k=3):
    import networkx as nx
    G = nx.Graph()
    G.add_edges_from(g["edges"])
    ps = []
    for p in nx.all_simple_paths(G, "S", "G", cutoff=7):
        if p != path:
            c = sum(W(g, p[i], p[i + 1]) for i in range(len(p) - 1))
            ps.append((c, rng.random(), p))
    ps.sort()
    return [p for _, _, p in ps[:8]]


def seq(lst):
    return ", ".join(lst)


def _perturb_orders(rng, correct, extra):
    out = list(extra)
    c = correct[:]
    for _ in range(12):
        if len(c) > 3:
            i = rng.randrange(1, len(c) - 2)
            d = c[:]
            d[i], d[i + 1] = d[i + 1], d[i]
            out.append(seq(d))
        if len(c) > 3:
            d = c[:-1]
            j = rng.randrange(1, len(d))
            d = d[:j] + d[j + 1:] + ["G"]
            out.append(seq(d))
    return [o for o in out if o != seq(correct)]


def adjacency_text(g):
    return "; ".join(f"{k}: {{{', '.join(sorted(g['adj'][k]))}}}" for k in sorted(g["adj"]))


# --------------------------------------------------------------------------- questions
def q_bfs_order(rng):
    g = random_graph(rng, n=rng.choice([7, 8, 9]), weighted=False)
    order, path, trace = bfs(g)
    o2, _ = dfs(g)
    o3, _, _ = bfs(g, reverse=True)
    opts, ans = make_mcq(seq(order), _perturb_orders(rng, order, [seq(o2), seq(o3)]), rng)
    text = ("Consider the undirected graph shown below. <b>Breadth-first search (graph-search version)</b> "
            "is run from start state <b>S</b> to find goal <b>G</b>. Successors are generated in "
            "<b>alphabetical order</b>, a state is added to the FIFO frontier only if it has not been "
            "reached before, and the goal test is applied when a state is <b>selected for expansion</b>. "
            "Which of the following is the sequence of states expanded (including S and G)?")
    rows = [["Step", "Expanded", "Frontier (FIFO) after expansion"]]
    for i, (n, fr) in enumerate(trace, 1):
        rows.append([str(i), f"<b>{n}</b>", "[" + ", ".join(fr) + "]" + ("  ← goal popped, stop" if n == "G" else "")])
    sol = [f"Adjacency lists (alphabetical): {adjacency_text(g)}.",
           "BFS trace (queue shown front → back):", tbl(rows, widths=[35, 60, 330]),
           f"Expansion order: <b>{seq(order)}</b>. The path returned is {' → '.join(path)} "
           f"with {len(path) - 1} edges, which is the path with the fewest edges (BFS is optimal for unit step costs).",
           "Distractors include the DFS order and BFS with reverse-alphabetical tie-breaking."]
    return Q("Uninformed Search", "MCQ", 1, text, opts, ans, sol, [_fig_unweighted(g)], "BFS")


def q_dfs_order(rng):
    g = random_graph(rng, n=rng.choice([7, 8, 9]), weighted=False)
    order, path = dfs(g)
    o2, _, _ = bfs(g)
    o3, _ = dfs(g, reverse=True)
    opts, ans = make_mcq(seq(order), _perturb_orders(rng, order, [seq(o2), seq(o3)]), rng)
    text = ("For the undirected graph shown, a <b>recursive depth-first search</b> is started at <b>S</b>. "
            "From every state, unvisited neighbours are explored in <b>alphabetical order</b>; a state already "
            "visited is never visited again; the search stops as soon as <b>G</b> is visited. "
            "In what order are the states visited?")
    sol = [f"Adjacency lists (alphabetical): {adjacency_text(g)}.",
           "DFS always goes deeper into the alphabetically first unvisited neighbour and backtracks only when a "
           "state has no unvisited neighbours.",
           f"Visit order: <b>{seq(order)}</b>; the path found is {' → '.join(path)} "
           f"({len(path) - 1} edges). Note that DFS need not find the shortest path."]
    return Q("Uninformed Search", "MCQ", 1, text, opts, ans, sol, [_fig_unweighted(g)], "DFS")


def _trace_table(trace, mode, h=None):
    head = {"ucs": "g", "astar": "f = g + h", "greedy": "h"}[mode]
    rows = [["Step", f"Expanded ({head})", "Frontier after expansion (sorted by priority)"]]
    for i, (n, k, gv, fr) in enumerate(trace, 1):
        frs = ", ".join(f"{nn}({num(kk)})" for kk, nn in fr)
        rows.append([str(i), f"<b>{n}</b> ({num(k)})", frs + ("  ← goal, stop" if n == "G" else "")])
    return tbl(rows, widths=[35, 95, 300])


def q_ucs(rng):
    g = random_graph(rng, n=rng.choice([7, 8]))
    order, path, cost, trace = best_first(g, mode="ucs")
    variant = rng.choice(["cost", "count", "path"])
    base = ("Uniform-cost search (graph search with an explored set, goal test when a node is "
            "<b>selected for expansion</b>, ties broken alphabetically) is run on the weighted undirected "
            "graph below from <b>S</b> to <b>G</b>. Edge labels are step costs. ")
    sol = ["UCS always expands the frontier node with the smallest path cost g(n); if a cheaper path to a "
           "frontier node is found its entry is replaced.", _trace_table(trace, "ucs"),
           f"Path returned: <b>{' → '.join(path)}</b>, cost = "
           + " + ".join(str(W(g, path[i], path[i + 1])) for i in range(len(path) - 1)) + f" = <b>{cost}</b>. "
           f"Nodes expanded (including S and G): <b>{len(order)}</b> ({seq(order)})."]
    if variant == "cost":
        return Q("Uninformed Search", "NAT", 2, base + "What is the cost of the path returned?", None,
                 (cost, cost), sol, [_fig(g)], "UCS")
    if variant == "count":
        return Q("Uninformed Search", "NAT", 2, base + "How many nodes are <b>expanded</b> "
                 "(count S and G)?", None, (len(order), len(order)), sol, [_fig(g)], "UCS")
    cands = [" → ".join(p) for p in other_paths(g, path, rng)]
    opts, ans = make_mcq(" → ".join(path), cands, rng)
    return Q("Uninformed Search", "MCQ", 2, base + "Which path is returned?", opts, ans, sol, [_fig(g)], "UCS")


def make_h(g, rng, factor=None):
    hstar = dijkstra_from(g, "G")
    c = factor if factor is not None else rng.uniform(0.6, 0.95)
    return {n: int(math.floor(c * hstar[n])) for n in g["names"]}, hstar


def q_astar(rng):
    for _ in range(50):
        g = random_graph(rng, n=rng.choice([7, 8, 9]))
        h, hstar = make_h(g, rng)
        order, path, cost, trace = best_first(g, h, mode="astar")
        o_u, _, _, _ = best_first(g, mode="ucs")
        if len(order) < len(o_u) or rng.random() < 0.3:
            break
    note = {n: f"h={h[n]}" for n in g["names"]}
    variant = rng.choice(["count", "path", "cost", "count"])
    base = ("A* search (graph search with explored set, goal test on expansion, ties broken alphabetically) "
            "is run from <b>S</b> to <b>G</b> on the graph below. Edge labels are step costs and the "
            "heuristic value h(n) is printed above each node. ")
    sol = [f"Heuristic values: " + ", ".join(f"h({n})={h[n]}" for n in sorted(h)) + ". "
           "A* expands the frontier node with the smallest f(n) = g(n) + h(n).",
           _trace_table(trace, "astar"),
           f"Path returned: <b>{' → '.join(path)}</b> with cost <b>{cost}</b>; nodes expanded = "
           f"<b>{len(order)}</b> ({seq(order)}).",
           "Check: h(n) = ⌊c·h*(n)⌋ for a constant c &lt; 1, so h is consistent (and admissible) and the path is "
           f"optimal — the true optimal cost h*(S) = {hstar['S']}. For comparison UCS (h = 0) would expand "
           f"{len(o_u)} nodes."]
    if variant == "count":
        return Q("Informed Search", "NAT", 2, base + "How many nodes are expanded, counting both S and G?",
                 None, (len(order), len(order)), sol, [_fig(g, note)], "A*")
    if variant == "cost":
        return Q("Informed Search", "NAT", 2, base + "What is the cost of the solution returned by A*?",
                 None, (cost, cost), sol, [_fig(g, note)], "A*")
    # MSQ about expansion
    st = []
    exp = set(order)
    others = [n for n in g["names"] if n not in ("S", "G")]
    rng.shuffle(others)
    for n in others[:3]:
        st.append((f"Node {n} is expanded.", n in exp))
    st.append((f"The path returned has cost {cost}.", True) if rng.random() < 0.5 else
              (f"The path returned has cost {cost + rng.choice([1, 2, -1])}.", False))
    if not any(t for _, t in st):
        st[0] = (f"Node S is expanded first.", True)
    opts, ans = make_msq(st, rng)
    return Q("Informed Search", "MSQ", 2, base + "Which of the following statements is/are TRUE?",
             opts, ans, sol, [_fig(g, note)], "A*")


def q_greedy(rng):
    for _ in range(60):
        g = random_graph(rng, n=rng.choice([7, 8]))
        h, hstar = make_h(g, rng, factor=rng.uniform(0.7, 1.0))
        order, path, cost, trace = best_first(g, h, mode="greedy")
        if cost != hstar["S"] or rng.random() < 0.25:
            break
    note = {n: f"h={h[n]}" for n in g["names"]}
    text = ("Greedy best-first search (graph search; a state is added to the frontier only if it has not "
            "been reached before; goal test on expansion; ties broken alphabetically) uses the heuristic h "
            "shown above each node to search from <b>S</b> to <b>G</b>. Edge labels are step costs. "
            "What is the cost of the path returned by greedy best-first search?")
    sol = ["Greedy best-first search orders the frontier by h(n) only, ignoring the cost already incurred.",
           _trace_table(trace, "greedy"),
           f"Path returned: <b>{' → '.join(path)}</b>, cost = "
           + " + ".join(str(W(g, path[i], path[i + 1])) for i in range(len(path) - 1)) + f" = <b>{cost}</b>.",
           f"The optimal cost is h*(S) = {hstar['S']}" + (" — greedy search is not optimal here." if cost != hstar['S']
                                                           else " — greedy happens to be optimal here, but in general it is not.")]
    return Q("Informed Search", "NAT", 1, text, None, (cost, cost), sol, [_fig(g, note)], "Greedy best-first")


def q_heuristic_props(rng):
    g = random_graph(rng, n=rng.choice([7, 8]))
    h, hstar = make_h(g, rng, factor=rng.uniform(0.75, 1.0))
    mode = rng.choice(["inadmissible", "inconsistent", "ok", "inconsistent"])
    others = [n for n in g["names"] if n not in ("S", "G")]
    if mode == "inadmissible":
        x = rng.choice(others)
        h[x] = hstar[x] + rng.randint(1, 3)
    elif mode == "inconsistent":
        # lower one node's heuristic heavily (stays admissible)
        cand = [n for n in others if hstar[n] >= 5]
        if cand:
            x = rng.choice(cand)
            h[x] = max(0, h[x] - rng.randint(4, 7))
    adm = all(h[n] <= hstar[n] for n in h)
    bad_edges = []
    for a, b in g["edges"]:
        for u, v in ((a, b), (b, a)):
            if h[u] > W(g, u, v) + h[v]:
                bad_edges.append((u, v))
    cons = not bad_edges and h["G"] == 0
    note = {n: f"h={h[n]}" for n in g["names"]}
    st = [("h is admissible.", adm), ("h is consistent (monotone).", cons)]
    over = [n for n in h if h[n] > hstar[n]]
    x = rng.choice(others)
    st.append((f"h({x}) overestimates the true cost from {x} to G.", x in over))
    if bad_edges and rng.random() < 0.7:
        u, v = rng.choice(bad_edges)
        st.append((f"The edge {u}–{v} violates the consistency condition h({u}) ≤ c({u},{v}) + h({v}).", True))
    else:
        a, b = rng.choice(g["edges"])
        viol = (a, b) in bad_edges or (b, a) in bad_edges
        st.append((f"The edge {a}–{b} violates the consistency condition (in at least one direction).", viol))
    if not any(t for _, t in st):
        st[2] = (f"h(G) = 0.", h["G"] == 0)
    opts, ans = make_msq(st, rng)
    text = ("The heuristic values h(n) for the graph below are printed above the nodes; edge labels are step "
            "costs and <b>G</b> is the only goal. Which of the following statements is/are TRUE?")
    rows = [["n"] + sorted(h), ["h(n)"] + [str(h[n]) for n in sorted(h)],
            ["h*(n)"] + [str(hstar[n]) for n in sorted(h)],
            ["h ≤ h*?"] + ["✓" if h[n] <= hstar[n] else "✗" for n in sorted(h)]]
    sol = ["First compute the true cost-to-goal h*(n) by running Dijkstra/UCS backwards from G:",
           tbl(rows, header=False),
           f"Admissible ⇔ h(n) ≤ h*(n) for every n: <b>{'yes' if adm else 'no'}</b>"
           + (f" (overestimates at {', '.join(over)})." if over else "."),
           "Consistent ⇔ h(G)=0 and h(u) ≤ c(u,v) + h(v) for every edge in both directions. Violating directed "
           "edges: " + (", ".join(f"{u}→{v} ({h[u]} &gt; {W(g, u, v)} + {h[v]})" for u, v in bad_edges)
                         if bad_edges else "none") + f". Hence consistent: <b>{'yes' if cons else 'no'}</b>.",
           "Recall: consistency ⇒ admissibility, but not conversely."]
    return Q("Informed Search", "MSQ", 2, text, opts, ans, sol, [_fig(g, note)], "Heuristics")


def q_counting(rng):
    kind = rng.choice(["bfs", "ids", "tree", "ebf", "dls"])
    b = rng.choice([2, 3, 4, 5])
    d = rng.choice([3, 4, 5]) if b > 3 else rng.choice([4, 5, 6])
    if kind == "bfs":
        ans = sum(b ** i for i in range(1, d + 1))
        text = (f"A search tree has uniform branching factor b = {b}; the shallowest goal is at depth d = {d} and "
                f"happens to be the <b>last</b> node generated at that depth. BFS applies the goal test when a node "
                f"is <b>generated</b>. How many nodes are generated in total (do <b>not</b> count the root)?")
        sol = [f"With goal test at generation, BFS generates every node at depths 1 … d before (and including) the goal "
               f"(the worst case). N = b + b² + … + b^d = " + " + ".join(str(b ** i) for i in range(1, d + 1))
               + f" = <b>{ans}</b>. This is the O(b^d) of AIMA."]
    elif kind == "ids":
        ans = sum((d + 1 - i) * b ** i for i in range(1, d + 1))
        text = (f"Iterative deepening search is applied to a tree with branching factor b = {b} whose shallowest goal "
                f"is at depth d = {d} (goal is the last node at that depth). Using the standard count "
                f"N(IDS) = d·b + (d−1)·b² + … + 1·b^d (root not counted), how many nodes are generated?")
        sol = ["Nodes at depth i are regenerated in every iteration with limit ≥ i, i.e. (d + 1 − i) times.",
               "N = " + " + ".join(f"{d + 1 - i}×{b ** i}" for i in range(1, d + 1)) + f" = <b>{ans}</b>.",
               f"Compare BFS: {sum(b ** i for i in range(1, d + 1))}; the overhead of IDS is small for b ≥ 2."]
    elif kind == "dls":
        l = d - 1
        ans = sum(b ** i for i in range(0, l + 1))
        text = (f"Depth-limited search with limit ℓ = {l} is run on a tree with branching factor b = {b}. No goal "
                f"exists within depth {l}. How many nodes (including the root) does it generate before returning "
                f"<i>cutoff</i>?")
        sol = [f"DLS explores the complete tree down to depth ℓ: 1 + b + … + b^ℓ = "
               + " + ".join(str(b ** i) for i in range(0, l + 1)) + f" = <b>{ans}</b> = (b^(ℓ+1) − 1)/(b − 1)."]
    elif kind == "tree":
        ans = (b ** (d + 1) - 1) // (b - 1)
        text = (f"How many nodes are there in a complete search tree of depth {d} (root at depth 0) with branching "
                f"factor {b}?")
        sol = [f"Σ<sub>i=0..{d}</sub> {b}^i = ({b}^{d + 1} − 1)/({b} − 1) = <b>{ans}</b>."]
    else:
        bs = rng.choice([1.5, 1.8, 2.0, 2.2, 2.5, 3.0])
        d = rng.choice([3, 4, 5])
        N = int(round(sum(bs ** i for i in range(1, d + 1))))
        lo, hi = 1.0, 10.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if sum(mid ** i for i in range(1, d + 1)) < N:
                lo = mid
            else:
                hi = mid
        val = round(lo, 2)
        text = (f"A* finds a solution at depth d = {d} after generating N = {N} nodes (root excluded). The effective "
                f"branching factor b* satisfies N = b* + (b*)² + … + (b*)^d. Find b* (round off to 2 decimal places).")
        sol = [f"Solve b + b² + … + b^{d} = {N} numerically (bisection): b* ≈ <b>{val}</b>.",
               "Check: " + " + ".join(f"{val}^{i}" for i in range(1, d + 1)) +
               f" ≈ {num(sum(val ** i for i in range(1, d + 1)), 2)} ≈ {N}."]
        return Q("Informed Search", "NAT", 1, text, None, (round(val - 0.02, 2), round(val + 0.02, 2)), sol, [],
                 "Effective branching factor")
    return Q("Uninformed Search", "NAT", 1, text, None, (ans, ans), sol, [], "Complexity")
