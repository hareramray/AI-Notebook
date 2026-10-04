"""Reasoning under uncertainty: Bayesian networks, d-separation, variable elimination, sampling."""
import itertools

import networkx as nx
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from common import Q, make_mcq, make_msq, num, tbl
from draw import graph_drawing, QUERY_FILL, EVID_FILL

THEMES = [
    None, None,
    ["Cloudy", "Sprinkler", "Rain", "WetGrass", "Slippery"],
    ["Burglary", "Earthquake", "Alarm", "JohnCalls", "MaryCalls"],
    ["Smoker", "Pollution", "Cancer", "XRay", "Dyspnoea"],
    ["Flu", "Fever", "Cough", "Fatigue", "Doctor"],
]


def topo_layers(nodes, parents):
    depth = {}
    for n in nodes:
        depth[n] = 0 if not parents[n] else 1 + max(depth[p] for p in parents[n])
    return depth


def layout(nodes, parents, rng):
    depth = topo_layers(nodes, parents)
    maxd = max(depth.values())
    layers = {}
    for n in nodes:
        layers.setdefault(depth[n], []).append(n)
    pos = {}
    for d, ns in layers.items():
        k = len(ns)
        for i, n in enumerate(ns):
            x = (i + 0.5) / k if k > 1 else 0.5
            x += rng.uniform(-0.06, 0.06)
            pos[n] = (min(1, max(0, x)), 1 - d / max(maxd, 1))
    return pos


def random_dag(rng, k, maxpar=2, p_edge=0.55, names=None, min_edges=None):
    while True:
        nodes = names[:k] if names else [chr(65 + i) for i in range(k)]
        parents = {n: [] for n in nodes}
        for j in range(1, k):
            cands = nodes[:j]
            npar = 0
            for c in rng.sample(cands, len(cands)):
                if npar < maxpar and rng.random() < p_edge:
                    parents[nodes[j]].append(c)
                    npar += 1
            parents[nodes[j]].sort(key=nodes.index)
        G = nx.DiGraph()
        G.add_nodes_from(nodes)
        for n in nodes:
            for p in parents[n]:
                G.add_edge(p, n)
        ne = G.number_of_edges()
        if nx.is_weakly_connected(G) and (min_edges is None or ne >= min_edges):
            return nodes, parents, G


def random_bn(rng, k=None, themed=None):
    k = k or rng.choice([4, 4, 5])
    names = None
    theme = rng.choice(THEMES) if themed is None else themed
    if theme:
        names = theme[:k]
    nodes, parents, G = random_dag(rng, k, names=names)
    grid = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.05, 0.95, 0.25, 0.75]
    cpt = {}
    for n in nodes:
        cpt[n] = {}
        for vals in itertools.product([True, False], repeat=len(parents[n])):
            cpt[n][vals] = rng.choice(grid)
    pos = layout(nodes, parents, rng)
    return dict(nodes=nodes, parents=parents, cpt=cpt, pos=pos, G=G)


def p_node(bn, n, val, asg):
    pt = bn["cpt"][n][tuple(asg[p] for p in bn["parents"][n])]
    return pt if val else 1 - pt


def joint(bn, asg):
    pr = 1.0
    for n in bn["nodes"]:
        pr *= p_node(bn, n, asg[n], asg)
    return pr


def short(n):
    return n if len(n) <= 2 else n[:2]


def TF(v):
    return "T" if v else "F"


def bn_drawing(bn, query=None, evidence=None, width=250, height=165, card=None):
    edges = [(p, n, None) for n in bn["nodes"] for p in bn["parents"][n]]
    fills = {}
    if query:
        fills[query] = QUERY_FILL
    for e in (evidence or {}):
        fills[e] = EVID_FILL
    labels_pos = {}
    for n, p in bn["pos"].items():
        labels_pos[n] = p
    long = any(len(n) > 2 for n in bn["nodes"])
    if long:
        mapping = {n: n[:2] for n in bn["nodes"]}
        pos = {mapping[n]: p for n, p in labels_pos.items()}
        edges = [(mapping[a], mapping[b], None) for a, b, _ in edges]
        fills = {mapping[k]: v for k, v in fills.items()}
        note = {mapping[n]: n for n in bn["nodes"]}
        return graph_drawing(pos, edges, directed=True, width=width, height=height, fills=fills,
                             node_note=note, radius=13)
    note = {n: f"|{n}|={card[n]}" for n in bn["nodes"]} if card else None
    return graph_drawing(labels_pos, edges, directed=True, width=width, height=height, fills=fills,
                         radius=13, node_note=note)


def cpt_tables(bn, width=230):
    """Return a single Table containing all CPTs."""
    small = []
    for n in bn["nodes"]:
        pa = bn["parents"][n]
        rows = [[short(p) for p in pa] + [f"P({short(n)}=T{'|…' if pa else ''})"]]
        for vals, pt in bn["cpt"][n].items():
            rows.append([TF(v) for v in vals] + [num(pt, 2)])
        w = [22] * len(pa) + [62]
        small.append(tbl(rows, widths=w, zebra=False))
    cells, row = [], []
    for t in small:
        row.append(t)
        if len(row) == 3:
            cells.append(row)
            row = []
    if row:
        cells.append(row + [""] * (3 - len(row)))
    T = Table(cells, hAlign="LEFT")
    T.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return T


def bn_figure(bn, query=None, evidence=None):
    d = bn_drawing(bn, query, evidence)
    T = Table([[d, cpt_tables(bn)]], colWidths=[255, 230], hAlign="LEFT")
    T.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    return T


def key_legend(bn):
    if any(len(n) > 2 for n in bn["nodes"]):
        return " (Nodes are abbreviated by their first two letters: " + ", ".join(
            f"{n[:2]} = {n}" for n in bn["nodes"]) + ".)"
    return ""


def factor_formula(bn):
    parts = []
    for n in bn["nodes"]:
        pa = bn["parents"][n]
        parts.append(f"P({n}" + (f" | {', '.join(pa)})" if pa else ")"))
    return " · ".join(parts)


def enumerate_query(bn, q, ev):
    hidden = [n for n in bn["nodes"] if n != q and n not in ev]
    res = {}
    terms = {True: [], False: []}
    for qv in (True, False):
        tot = 0
        for hv in itertools.product([True, False], repeat=len(hidden)):
            asg = dict(ev)
            asg[q] = qv
            asg.update(dict(zip(hidden, hv)))
            pr = joint(bn, asg)
            tot += pr
            terms[qv].append((dict(zip(hidden, hv)), asg, pr))
        res[qv] = tot
    return res, hidden, terms


def term_str(bn, asg):
    return " × ".join(num(p_node(bn, n, asg[n], asg), 3) for n in bn["nodes"])


def q_bn_inference(rng):
    for _ in range(100):
        bn = random_bn(rng)
        nodes = bn["nodes"]
        q = rng.choice(nodes)
        others = [n for n in nodes if n != q]
        ne = rng.choice([1, 1, 2])
        evn = rng.sample(others, ne)
        ev = {e: rng.random() < 0.7 for e in evn}
        res, hidden, terms = enumerate_query(bn, q, ev)
        Z = res[True] + res[False]
        if Z > 1e-6 and len(hidden) <= 3:
            break
    post = res[True] / Z
    evs = ", ".join(f"{e} = {TF(v)}" for e, v in ev.items())
    text = (f"Consider the Bayesian network below over Boolean variables with the given CPTs (only P(X = T | parents) "
            f"is listed).{key_legend(bn)} Compute <b>P({q} = T | {evs})</b> (round off to 3 decimal places).")
    rows = [["Hidden: " + (", ".join(short(h) for h in hidden) if hidden else "—"),
             f"{short(q)}", "product of CPT entries (" + " · ".join(short(n) for n in nodes) + ")", "value"]]
    for qv in (True, False):
        for hv, asg, pr in terms[qv]:
            rows.append([", ".join(TF(v) for v in hv.values()) or "—", TF(qv), term_str(bn, asg), num(pr, 5)])
    sol = [f"Factorisation: P({', '.join(nodes)}) = {factor_formula(bn)}.",
           f"Inference by enumeration: P({q} | e) = α Σ<sub>hidden</sub> P({q}, e, hidden).",
           tbl(rows, widths=[70, 25, 270, 55]),
           f"P({q}=T, e) = {num(res[True], 5)};  P({q}=F, e) = {num(res[False], 5)};  P(e) = {num(Z, 5)}.",
           f"P({q}=T | e) = {num(res[True], 5)} / {num(Z, 5)} = <b>{num(post, 4)}</b> ≈ {post:.3f}."]
    return Q("Exact Inference", "NAT", 2, text, None, (round(post - 0.002, 3), round(post + 0.002, 3)),
             sol, [bn_figure(bn, q, ev)], "Exact inference")


def q_bn_marginal(rng):
    for _ in range(100):
        bn = random_bn(rng, k=rng.choice([3, 4]), themed=False)
        cand = [n for n in bn["nodes"] if bn["parents"][n]]
        if cand:
            break
    q = rng.choice(cand)
    res, hidden, terms = enumerate_query(bn, q, {})
    anc = nx.ancestors(bn["G"], q)
    val = res[True]
    text = (f"For the Bayesian network below (Boolean variables; CPTs list P(X = T | parents)), compute the "
            f"marginal probability <b>P({q} = T)</b> (round off to 3 decimal places).")
    sol = [f"Only the ancestors of {q} ({', '.join(sorted(anc)) or 'none'}) matter: every other variable sums out to 1.",
           f"P({q}=T) = Σ over its ancestors of P({q}=T | parents) × P(parents' configuration). Summing the joint over all "
           f"other variables gives:"]
    rows = [["Assignment to other variables", "joint P(…, " + q + "=T)"]]
    for hv, asg, pr in terms[True]:
        rows.append([", ".join(f"{k}={TF(v)}" for k, v in hv.items()), num(pr, 5)])
    sol += [tbl(rows, widths=[200, 100]), f"Sum = <b>{num(val, 4)}</b> ≈ {val:.3f}."]
    return Q("Exact Inference", "NAT", 1, text, None, (round(val - 0.002, 3), round(val + 0.002, 3)), sol,
             [bn_figure(bn, q)], "Marginal")


# ---------------------------------------------------------------- d-separation
def undirected_paths(G, x, y, cutoff=8):
    U = G.to_undirected()
    return list(nx.all_simple_paths(U, x, y, cutoff=cutoff))


def path_status(G, path, Z):
    """Return (active, reason)."""
    for i in range(1, len(path) - 1):
        a, b, c = path[i - 1], path[i], path[i + 1]
        into_b_from_a = G.has_edge(a, b)
        into_b_from_c = G.has_edge(c, b)
        if into_b_from_a and into_b_from_c:
            desc = nx.descendants(G, b) | {b}
            if not (desc & Z):
                return False, f"collider {b} with neither it nor a descendant observed"
        else:
            if b in Z:
                kind = "chain" if (into_b_from_a != into_b_from_c) else "fork"
                return False, f"observed {kind} node {b}"
    return True, "active"


def path_str(G, path):
    out = path[0]
    for i in range(1, len(path)):
        a, b = path[i - 1], path[i]
        out += (" → " if G.has_edge(a, b) else " ← ") + b
    return out


def q_dsep(rng):
    for _ in range(300):
        k = rng.choice([6, 7, 7, 8])
        nodes, parents, G = random_dag(rng, k, maxpar=2, p_edge=0.5, min_edges=k)
        stm = []
        for _ in range(40):
            x, y = rng.sample(nodes, 2)
            rest = [n for n in nodes if n not in (x, y)]
            Z = set(rng.sample(rest, rng.choice([0, 1, 1, 2])))
            ind = nx.is_d_separator(G, {x}, {y}, Z)
            txt = f"{x} ⊥ {y}" + (f" | {', '.join(sorted(Z))}" if Z else "")
            if txt not in [s for s, *_ in stm]:
                stm.append((txt, ind, x, y, Z))
        tr = [s for s in stm if s[1]]
        fa = [s for s in stm if not s[1]]
        if len(tr) >= 2 and len(fa) >= 2:
            break
    kt = min(rng.choice([1, 2, 2, 3]), len(tr))
    kt = max(kt, 4 - len(fa))
    chosen = rng.sample(tr, kt) + rng.sample(fa, 4 - kt)
    rng.shuffle(chosen)
    rp = {n: (rng.uniform(-0.04, 0.04)) for n in nodes}
    bn = dict(nodes=nodes, parents=parents, pos=layout(nodes, parents, rng), G=G)
    fig = bn_drawing(bn, width=330, height=190)
    opts = [c[0] for c in chosen]
    ans = [i for i, c in enumerate(chosen) if c[1]]
    sol = ["Rules: a chain (→ B →) or fork (← B →) is blocked iff B is observed; a collider (→ B ←) is blocked "
           "iff neither B nor any descendant of B is observed. X ⊥ Y | Z holds iff every undirected path is blocked."]
    for i, (txt, ind, x, y, Z) in enumerate(chosen):
        paths = undirected_paths(G, x, y)
        lab = chr(65 + i)
        if not ind:
            for p in paths:
                act, _ = path_status(G, p, Z)
                if act:
                    sol.append(f"({lab}) {txt}: <b>FALSE</b> — the path {path_str(G, p)} is active given "
                               f"{{{', '.join(sorted(Z))}}}.")
                    break
        else:
            reasons = []
            for p in paths[:6]:
                _, why = path_status(G, p, Z)
                reasons.append(f"{path_str(G, p)} (blocked: {why})")
            extra = f" (+{len(paths) - 6} more paths, all blocked)" if len(paths) > 6 else ""
            sol.append(f"({lab}) {txt}: <b>TRUE</b> — " + ("; ".join(reasons) if reasons else "no path at all")
                       + extra + ".")
    text = ("For the Bayesian network structure shown below, which of the following conditional independence "
            "statements is/are guaranteed by d-separation?")
    return Q("Conditional Independence", "MSQ", 2, text, opts, ans, sol, [fig], "d-separation")


def q_markov_blanket(rng):
    while True:
        k = rng.choice([7, 8])
        nodes, parents, G = random_dag(rng, k, maxpar=2, p_edge=0.5, min_edges=k)
        x = rng.choice(nodes)
        ch = list(G.successors(x))
        if ch and parents[x]:
            break
    mb = set(parents[x]) | set(ch)
    for c in ch:
        mb |= set(parents[c])
    mb.discard(x)
    bn = dict(nodes=nodes, parents=parents, pos=layout(nodes, parents, rng), G=G)
    fig = bn_drawing(bn, width=330, height=190)
    sol = [f"Markov blanket = parents ∪ children ∪ children's other parents.",
           f"Parents of {x}: {{{', '.join(parents[x])}}}; children: {{{', '.join(sorted(ch))}}}; co-parents: "
           f"{{{', '.join(sorted(mb - set(parents[x]) - set(ch))) or '∅'}}}.",
           f"MB({x}) = {{{', '.join(sorted(mb))}}} — <b>{len(mb)}</b> nodes. Given its Markov blanket, {x} is "
           f"conditionally independent of every other node in the network."]
    if rng.random() < 0.5:
        text = f"How many nodes are in the Markov blanket of <b>{x}</b> in the Bayesian network below?"
        return Q("Conditional Independence", "NAT", 1, text, None, (len(mb), len(mb)), sol, [fig], "Markov blanket")
    corr = "{" + ", ".join(sorted(mb)) + "}"
    pc = "{" + ", ".join(sorted(set(parents[x]) | set(ch))) + "}"
    nb = set(nx.all_neighbors(G, x)) | set(nx.descendants(G, x))
    alld = "{" + ", ".join(sorted(nb)) + "}"
    anc = "{" + ", ".join(sorted(set(parents[x]) | set(nx.descendants(G, x)) | (mb - set(ch)))) + "}"
    others = [n for n in nodes if n != x and n not in mb]
    plus = "{" + ", ".join(sorted(mb | set(rng.sample(others, 1)))) + "}" if others else "{}"
    opts, ans = make_mcq(corr, [pc, alld, anc, plus, "{" + ", ".join(sorted(ch)) + "}"], rng)
    text = f"Which set is the Markov blanket of <b>{x}</b> in the Bayesian network below?"
    return Q("Conditional Independence", "MCQ", 1, text, opts, ans, sol, [fig], "Markov blanket")


def q_param_count(rng):
    k = rng.choice([5, 6])
    nodes, parents, G = random_dag(rng, k, maxpar=3, p_edge=0.55, min_edges=k - 1)
    card = {n: rng.choice([2, 2, 3, 3, 4]) for n in nodes}
    terms = []
    total = 0
    for n in nodes:
        prod = 1
        for p in parents[n]:
            prod *= card[p]
        total += (card[n] - 1) * prod
        terms.append(f"({card[n]}−1)" + "".join(f"×{card[p]}" for p in parents[n]))
    full = 1
    for n in nodes:
        full *= card[n]
    bn = dict(nodes=nodes, parents=parents, pos=layout(nodes, parents, rng), G=G)
    fig = bn_drawing(bn, width=330, height=190, card=card)
    variant = rng.choice(["bn", "bn", "saving"])
    sol = ["A CPT for X with parents Pa(X) needs (|X| − 1) × Π<sub>U∈Pa(X)</sub>|U| independent parameters "
           "(the last entry of each row is 1 minus the others).",
           "Σ = " + " + ".join(f"{n}: {t}" for n, t in zip(nodes, terms)) + f" = <b>{total}</b>.",
           f"Full joint table: Π|X| − 1 = {full} − 1 = {full - 1}; saving = {full - 1 - total}."]
    if variant == "bn":
        text = ("The Bayesian network below has variables whose domain sizes are written above each node. "
                "How many independent parameters are required to specify all of its CPTs?")
        return Q("Bayesian Networks", "NAT", 1, text, None, (total, total), sol, [fig], "Parameter count")
    text = ("The domain sizes of the variables of the Bayesian network below are written above the nodes. By how many "
            "does the number of independent parameters of the full joint distribution exceed the number of "
            "independent parameters of the network's CPTs?")
    v = full - 1 - total
    return Q("Bayesian Networks", "NAT", 2, text, None, (v, v), sol, [fig], "Parameter count")


# ------------------------------------------------------------ variable elimination
def q_ve(rng):
    for _ in range(300):
        k = rng.choice([6, 7])
        nodes, parents, G = random_dag(rng, k, maxpar=2, p_edge=0.6, min_edges=k)
        q = rng.choice(nodes)
        ev = rng.sample([n for n in nodes if n != q], rng.choice([0, 1, 1]))
        hidden = [n for n in nodes if n != q and n not in ev]
        order = hidden[:]
        rng.shuffle(order)
        factors = [frozenset(([n] + parents[n])) - set(ev) for n in nodes]
        factors = [f for f in factors]
        steps = []
        cur = list(factors)
        mx = 0
        mxv = None
        for v in order:
            inv = [f for f in cur if v in f]
            rest = [f for f in cur if v not in f]
            prod = frozenset().union(*inv) if inv else frozenset()
            newf = prod - {v}
            steps.append((v, inv, prod, newf))
            cur = rest + [newf]
            if len(newf) > mx:
                mx = len(newf)
                mxv = v
        if mx >= 2 and len(order) >= 3:
            break
    bn = dict(nodes=nodes, parents=parents, pos=layout(nodes, parents, rng), G=G)
    fig = bn_drawing(bn, query=q, evidence={e: True for e in ev}, width=330, height=190)

    def fs(f):
        return "f(" + ", ".join(sorted(f)) + ")" if f else "f()"
    rows = [["Eliminate", "Factors multiplied", "Product scope", "New factor (after Σ)"]]
    for v, inv, prod, newf in steps:
        rows.append([v, ", ".join(fs(f) for f in inv), "{" + ", ".join(sorted(prod)) + "}", fs(newf)])
    init = ", ".join(fs(f) for f in factors)
    evtxt = (f"evidence {', '.join(e + ' = T' for e in ev)} is observed; ") if ev else "there is no evidence; "
    base = (f"Variable elimination is used to compute <b>P({q}" + (f" | {', '.join(e + ' = T' for e in ev)}" if ev else "")
            + f")</b> in the Bayesian network below (Boolean variables; {evtxt}the query node is green"
            + (", evidence yellow" if ev else "") + "). Every CPT becomes an initial factor (no pruning of irrelevant "
            f"variables), evidence variables are instantiated and so do not appear in any factor's scope, and the "
            f"hidden variables are eliminated in the order <b>{', '.join(order)}</b>. ")
    sol = [f"Initial factors (one per CPT, evidence removed from scopes): {init}.",
           "Eliminating Z: multiply all factors whose scope contains Z, then sum Z out.",
           tbl(rows, widths=[50, 180, 105, 95]),
           f"The largest factor produced has <b>{mx}</b> variable(s) (created when eliminating {mxv}); with Boolean "
           f"variables it has 2^{mx} = {2 ** mx} entries. Finally, multiply the remaining factors over {q} and normalise."]
    variant = rng.choice(["size", "size", "scope"])
    if variant == "size":
        text = base + "What is the number of variables in the largest factor <b>generated</b> by a summation step?"
        return Q("Exact Inference", "NAT", 2, text, None, (mx, mx), sol, [fig], "Variable elimination")
    v, inv, prod, newf = steps[rng.randrange(len(steps))]
    corr = fs(newf)
    dis = [fs(prod), fs(newf | {v}), fs(frozenset(list(newf)[:-1])) if len(newf) > 1 else "f(" + v + ")",
           fs(newf | {q}) if q not in newf else fs(newf - {q}), fs(frozenset(parents[v]))]
    if not newf:
        corr = "f() — a constant (scope ∅)"
    opts, ans = make_mcq(corr, [d for d in dis if d != corr] + ["f(" + ", ".join(sorted(set(nodes) - set(ev))) + ")"],
                         rng)
    text = base + f"What is the scope of the new factor produced when <b>{v}</b> is summed out?"
    return Q("Exact Inference", "MCQ", 2, text, opts, ans, sol, [fig], "Variable elimination")


# --------------------------------------------------------------------- sampling
def sample_prior(bn, rng):
    asg = {}
    for n in bn["nodes"]:
        asg[n] = rng.random() < bn["cpt"][n][tuple(asg[p] for p in bn["parents"][n])]
    return asg


def asg_str(bn, asg, keys=None):
    keys = keys or bn["nodes"]
    return ", ".join(f"{short(k)}={TF(asg[k])}" for k in keys)


def q_prior_prob(rng):
    bn = random_bn(rng)
    asg = sample_prior(bn, rng)
    pr = joint(bn, asg)
    text = (f"Prior (direct) sampling is run on the Bayesian network below, sampling variables in topological order "
            f"{', '.join(short(n) for n in bn['nodes'])}.{key_legend(bn)} What is the probability that a single run "
            f"produces the sample <b>⟨{asg_str(bn, asg)}⟩</b>? (round off to 4 decimal places)")
    sol = ["Prior sampling generates each complete event with exactly its joint probability "
           "S<sub>PS</sub>(x<sub>1</sub>,…,x<sub>n</sub>) = Π P(x<sub>i</sub> | parents(X<sub>i</sub>)).",
           " × ".join(f"P({short(n)}={TF(asg[n])}" + (f"|{','.join(short(p) + '=' + TF(asg[p]) for p in bn['parents'][n])})"
                                                       if bn['parents'][n] else ")") for n in bn["nodes"]),
           f"= {term_str(bn, asg)} = <b>{num(pr, 6)}</b> ≈ {pr:.4f}."]
    return Q("Sampling", "NAT", 1, text, None, (round(pr - 0.0002, 4), round(pr + 0.0002, 4)), sol,
             [bn_figure(bn)], "Prior sampling")


def q_uniform_sample(rng):
    bn = random_bn(rng, themed=False)
    us = [round(rng.uniform(0.01, 0.99), 2) for _ in bn["nodes"]]
    asg = {}
    lines = []
    for n, u in zip(bn["nodes"], us):
        p = bn["cpt"][n][tuple(asg[x] for x in bn["parents"][n])]
        asg[n] = u < p
        lines.append(f"{n}: P({n}=T | " + (", ".join(f"{x}={TF(asg[x])}" for x in bn['parents'][n]) or "—")
                     + f") = {num(p, 2)}; u = {u} {'&lt;' if asg[n] else '≥'} {num(p, 2)} ⇒ {n} = {TF(asg[n])}")
    corr = asg_str(bn, asg)
    dis = []
    for i in range(len(bn["nodes"])):
        a2 = dict(asg)
        a2[bn["nodes"][i]] = not a2[bn["nodes"][i]]
        dis.append(asg_str(bn, a2))
    # "wrong rule" distractor: True iff u > p
    a3 = {}
    for n, u in zip(bn["nodes"], us):
        p = bn["cpt"][n][tuple(a3[x] for x in bn["parents"][n])]
        a3[n] = u >= p
    dis.insert(0, asg_str(bn, a3))
    opts, ans = make_mcq(corr, dis, rng)
    text = ("Prior sampling is applied to the network below in the topological order "
            f"{', '.join(bn['nodes'])}, using the uniform random numbers <b>u = ⟨{', '.join(str(u) for u in us)}⟩</b> "
            "(one per variable, in that order). A variable X is set to T iff u &lt; P(X = T | sampled parent values). "
            "Which sample is generated?")
    sol = ["Sample each variable after its parents, using the parent values already drawn:",
           *[f"• {l}" for l in lines], f"Sample: <b>⟨{corr}⟩</b>."]
    return Q("Sampling", "MCQ", 2, text, opts, ans, sol, [bn_figure(bn)], "Prior sampling")


def q_rejection(rng):
    for _ in range(200):
        bn = random_bn(rng, themed=False)
        nodes = bn["nodes"]
        q = rng.choice(nodes)
        e = rng.choice([n for n in nodes if n != q])
        ev = rng.random() < 0.6
        N = rng.choice([15, 18, 20])
        samples = [sample_prior(bn, rng) for _ in range(N)]
        acc = [s for s in samples if s[e] == ev]
        if 4 <= len(acc) <= N - 3:
            qt = sum(1 for s in acc if s[q])
            if 0 < qt < len(acc):
                break
    est = qt / len(acc)
    rows = [["#"] + nodes]
    hl = set()
    for i, s in enumerate(samples, 1):
        rows.append([str(i)] + [TF(s[n]) for n in nodes])
    variant = rng.choice(["est", "est", "rej"])
    exact, _, _ = enumerate_query(bn, q, {e: ev})
    ex = exact[True] / (exact[True] + exact[False])
    text = (f"The following {N} samples were generated by prior sampling from a Bayesian network over Boolean variables "
            f"{', '.join(nodes)}. ")
    sol = [f"Rejection sampling keeps only samples consistent with the evidence {e} = {TF(ev)}: samples "
           + ", ".join(str(i) for i, s in enumerate(samples, 1) if s[e] == ev) + f" ({len(acc)} accepted, "
           f"{N - len(acc)} rejected).",
           f"Among the accepted samples, {q} = T in {qt}. Estimate = {qt}/{len(acc)} = <b>{num(est, 4)}</b>.",
           f"(For this network the exact value is {num(ex, 4)}; the estimate converges to it as N → ∞, but with so few "
           f"accepted samples the variance is high — the main weakness of rejection sampling when P(e) is small.)"]
    if variant == "est":
        text += (f"Using <b>rejection sampling</b>, estimate <b>P({q} = T | {e} = {TF(ev)})</b> "
                 "(round off to 2 decimal places).")
        return Q("Sampling", "NAT", 2, text, None, (round(est - 0.01, 2), round(est + 0.01, 2)), sol,
                 [tbl(rows, widths=[22] + [34] * len(nodes))], "Rejection sampling")
    text += (f"If rejection sampling is used to estimate P({q} = T | {e} = {TF(ev)}), how many of these samples are "
             f"<b>rejected</b>?")
    r = N - len(acc)
    return Q("Sampling", "NAT", 1, text, None, (r, r), sol, [tbl(rows, widths=[22] + [34] * len(nodes))],
             "Rejection sampling")


def q_likelihood_weighting(rng):
    for _ in range(200):
        bn = random_bn(rng, themed=False)
        nodes = bn["nodes"]
        q = rng.choice(nodes)
        evn = rng.sample([n for n in nodes if n != q], rng.choice([1, 2]))
        ev = {e: rng.random() < 0.65 for e in evn}
        N = rng.choice([4, 5, 6])
        samples = []
        for _ in range(N):
            asg = {}
            w = 1.0
            for n in nodes:
                p = bn["cpt"][n][tuple(asg[x] for x in bn["parents"][n])]
                if n in ev:
                    asg[n] = ev[n]
                    w *= p if ev[n] else 1 - p
                else:
                    asg[n] = rng.random() < p
            samples.append((asg, w))
        wt = sum(w for a, w in samples if a[q])
        wa = sum(w for a, w in samples)
        if wa > 0 and 0 < wt < wa:
            break
    est = wt / wa
    nonev = [n for n in nodes if n not in ev]
    rows = [["#"] + nonev]
    for i, (a, w) in enumerate(samples, 1):
        rows.append([str(i)] + [TF(a[n]) for n in nonev])
    evs = ", ".join(f"{e} = {TF(v)}" for e, v in ev.items())
    srows = [["#", "weight w = Π P(e | parents)", "w", f"{q}"]]
    for i, (a, w) in enumerate(samples, 1):
        parts = []
        for e in nodes:
            if e in ev:
                p = bn["cpt"][e][tuple(a[x] for x in bn["parents"][e])]
                parts.append(f"P({e}={TF(ev[e])}" + (f"|{','.join(x + '=' + TF(a[x]) for x in bn['parents'][e])}"
                                                    if bn['parents'][e] else "") + f")={num(p if ev[e] else 1 - p, 2)}")
        srows.append([str(i), " × ".join(parts), num(w, 4), TF(a[q])])
    variant = rng.choice(["est", "est", "w"])
    sol = ["In likelihood weighting the evidence variables are fixed and each sample is weighted by the product of the "
           "probabilities of the evidence values given their (sampled) parents.", tbl(srows, widths=[20, 300, 50, 30]),
           f"Σ w (all) = {num(wa, 4)}; Σ w ({q} = T) = {num(wt, 4)}.",
           f"Estimate P({q}=T | {evs}) = {num(wt, 4)} / {num(wa, 4)} = <b>{num(est, 4)}</b>."]
    text = (f"Likelihood weighting is used on the Bayesian network below with evidence <b>{evs}</b>. The values of the "
            f"non-evidence variables in the generated samples are listed in the table. ")
    figs = [bn_figure(bn, q, ev), tbl(rows, widths=[22] + [34] * len(nonev))]
    if variant == "est":
        text += f"Estimate <b>P({q} = T | {evs})</b> (round off to 3 decimal places)."
        return Q("Sampling", "NAT", 2, text, None, (round(est - 0.002, 3), round(est + 0.002, 3)), sol, figs,
                 "Likelihood weighting")
    i = rng.randrange(N)
    w = samples[i][1]
    text += f"What is the weight of sample #{i + 1}? (round off to 4 decimal places)"
    return Q("Sampling", "NAT", 2, text, None, (round(w - 0.0002, 4), round(w + 0.0002, 4)), sol, figs,
             "Likelihood weighting")


def q_gibbs(rng):
    for _ in range(100):
        bn = random_bn(rng, k=rng.choice([4, 5]), themed=False)
        nodes = bn["nodes"]
        x = rng.choice(nodes)
        ch = [n for n in nodes if x in bn["parents"][n]]
        if ch or bn["parents"][x]:
            break
    state = {n: rng.random() < 0.5 for n in nodes}
    ev = {e: state[e] for e in rng.sample([n for n in nodes if n != x], 1)}
    mb = set(bn["parents"][x]) | set(ch)
    for c in ch:
        mb |= set(bn["parents"][c])
    mb.discard(x)
    vals = {}
    for xv in (True, False):
        a = dict(state)
        a[x] = xv
        terms = [p_node(bn, x, xv, a)] + [p_node(bn, c, a[c], a) for c in ch]
        prod = 1
        for t in terms:
            prod *= t
        vals[xv] = (terms, prod)
    p = vals[True][1] / (vals[True][1] + vals[False][1])
    text = (f"Gibbs sampling (MCMC) is run on the Bayesian network below with evidence <b>{asg_str(bn, ev, list(ev))}</b>. "
            f"The current state of the chain is <b>⟨{asg_str(bn, state)}⟩</b>. The next step resamples <b>{x}</b>. "
            f"With what probability is {x} set to T? (round off to 3 decimal places)")

    def lab(xv):
        a = dict(state)
        a[x] = xv
        parts = [f"P({x}={TF(xv)}" + (f"|{','.join(pp + '=' + TF(a[pp]) for pp in bn['parents'][x])}"
                                      if bn['parents'][x] else "") + ")"]
        for c in ch:
            parts.append(f"P({c}={TF(a[c])}|{','.join(pp + '=' + TF(a[pp]) for pp in bn['parents'][c])})")
        return " × ".join(parts)
    sol = [f"Gibbs sampling draws {x} from P({x} | mb({x})), where mb({x}) = {{{', '.join(sorted(mb))}}}:",
           f"P({x} | mb) ∝ P({x} | parents({x})) × Π<sub>children Y</sub> P(y | parents(Y)).",
           f"{x}=T: {lab(True)} = " + " × ".join(num(t, 3) for t in vals[True][0]) + f" = {num(vals[True][1], 5)}",
           f"{x}=F: {lab(False)} = " + " × ".join(num(t, 3) for t in vals[False][0]) + f" = {num(vals[False][1], 5)}",
           f"Normalise: {num(vals[True][1], 5)} / ({num(vals[True][1], 5)} + {num(vals[False][1], 5)}) = "
           f"<b>{num(p, 4)}</b>."]
    return Q("Sampling", "NAT", 2, text, None, (round(p - 0.002, 3), round(p + 0.002, 3)), sol,
             [bn_figure(bn, x, ev)], "Gibbs sampling")
