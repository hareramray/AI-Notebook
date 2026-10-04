"""Adversarial search generators: minimax, alpha-beta, expectimax on random game trees."""
from common import Q, make_mcq, make_msq, num, tbl
from draw import tree_drawing, legend_game

INTERNAL_NAMES = list("ABCDEFHIJKMNPQTUVWXYZ")


def random_tree(rng, depth=None, chance=False, max_leaves=16):
    while True:
        depth = depth or rng.choice([2, 3, 3])
        tree, kinds, vals, names = {}, {}, {}, {}
        counter = [0, 0]

        def build(node, lvl):
            if lvl == depth:
                tree[node] = []
                kinds[node] = "leaf"
                counter[1] += 1
                vals[node] = rng.randint(-5, 20) if not chance else rng.randint(0, 20)
                names[node] = f"L{counter[1]}"
                return
            if chance:
                kinds[node] = "max" if lvl % 2 == 0 else "chance"
            else:
                kinds[node] = "max" if lvl % 2 == 0 else "min"
            if node != "R":
                names[node] = INTERNAL_NAMES[counter[0]]
                counter[0] += 1
            else:
                names[node] = "R"
            if depth == 2:
                k = rng.choice([2, 3, 3, 4])
            else:
                k = rng.choice([2, 2, 3]) if lvl < depth - 1 else rng.choice([2, 2, 3])
            tree[node] = []
            for i in range(k):
                c = f"{node}{i}"
                tree[node].append(c)
                build(c, lvl + 1)
        build("R", 0)
        if 6 <= counter[1] <= max_leaves:
            return tree, kinds, vals, names


def minimax(tree, kinds, vals, n, memo):
    if kinds[n] == "leaf":
        memo[n] = vals[n]
    else:
        cv = [minimax(tree, kinds, vals, c, memo) for c in tree[n]]
        memo[n] = max(cv) if kinds[n] == "max" else min(cv)
    return memo[n]


def leaves_under(tree, n):
    if not tree[n]:
        return [n]
    out = []
    for c in tree[n]:
        out += leaves_under(tree, c)
    return out


def alphabeta(tree, kinds, vals, names):
    evaluated, pruned, trace = [], [], []

    def ab(n, a, b):
        if kinds[n] == "leaf":
            evaluated.append(n)
            return vals[n]
        if kinds[n] == "max":
            v = -10 ** 9
            for i, c in enumerate(tree[n]):
                v = max(v, ab(c, a, b))
                if v >= b:
                    rest = tree[n][i + 1:]
                    if rest:
                        pl = sum((leaves_under(tree, r) for r in rest), [])
                        pruned.extend(pl)
                        trace.append(f"At MAX node {names[n]}: value {v} ≥ β = {fmt(b)} ⇒ prune remaining "
                                     f"children (leaves {', '.join(names[x] for x in pl)}).")
                    return v
                a = max(a, v)
            return v
        v = 10 ** 9
        for i, c in enumerate(tree[n]):
            v = min(v, ab(c, a, b))
            if v <= a:
                rest = tree[n][i + 1:]
                if rest:
                    pl = sum((leaves_under(tree, r) for r in rest), [])
                    pruned.extend(pl)
                    trace.append(f"At MIN node {names[n]}: value {v} ≤ α = {fmt(a)} ⇒ prune remaining "
                                 f"children (leaves {', '.join(names[x] for x in pl)}).")
                return v
            b = min(b, v)
        return v
    root = ab("R", -10 ** 9, 10 ** 9)
    return root, evaluated, pruned, trace


def fmt(x):
    if x <= -10 ** 8:
        return "−∞"
    if x >= 10 ** 8:
        return "+∞"
    return str(x)


def q_minimax(rng):
    tree, kinds, vals, names = random_tree(rng)
    memo = {}
    v = minimax(tree, kinds, vals, "R", memo)
    fig = tree_drawing(tree, kinds, vals, node_names=names)
    marks = {n: f"v={memo[n]}" for n in memo if kinds[n] != "leaf"}
    solfig = tree_drawing(tree, kinds, vals, node_names=names, marks=marks)
    best = [names[c] for c in tree["R"] if memo[c] == v]
    sol = ["Back up values bottom-up: a MIN node takes the minimum of its children, a MAX node the maximum.",
           solfig,
           "Values of internal nodes: " + ", ".join(f"{names[n]} = {memo[n]}" for n in memo
                                                    if kinds[n] != "leaf" and n != "R")
           + f". Root value = <b>{v}</b>; MAX's optimal first move is towards {', '.join(best)}."]
    if rng.random() < 0.6:
        text = ("Consider the two-player zero-sum game tree below (MAX moves at the root, levels alternate). "
                "What is the minimax value of the root?")
        return Q("Adversarial Search", "NAT", 1, text, None, (v, v), sol, [fig, legend_game()], "Minimax")
    ch = [names[c] for c in tree["R"]]
    if len(best) > 1 or len(ch) < 2:
        text = "For the game tree below, what is the minimax value of the root?"
        return Q("Adversarial Search", "NAT", 1, text, None, (v, v), sol, [fig, legend_game()], "Minimax")
    correct = f"Move to {best[0]}; root value {v}"
    dis = [f"Move to {c}; root value {memo[tc]}" for c, tc in zip(ch, tree["R"]) if c != best[0]]
    dis += [f"Move to {best[0]}; root value {v + rng.choice([1, 2, 3])}",
            f"Move to {best[0]}; root value {max(vals.values())}", f"Move to {ch[-1]}; root value {v}"]
    opts, ans = make_mcq(correct, dis, rng)
    text = ("In the game tree below MAX is to move at the root. Assuming both players play optimally, which "
            "option gives MAX's best move and the minimax value of the root?")
    return Q("Adversarial Search", "MCQ", 1, text, opts, ans, sol, [fig, legend_game()], "Minimax")


def q_alphabeta(rng):
    for _ in range(200):
        tree, kinds, vals, names = random_tree(rng, depth=rng.choice([2, 3, 3]))
        root, ev, pr, trace = alphabeta(tree, kinds, vals, names)
        if len(pr) >= 2:
            break
    memo = {}
    minimax(tree, kinds, vals, "R", memo)
    fig = tree_drawing(tree, kinds, vals, node_names=names)
    marks = {l: "pruned" for l in pr}
    solfig = tree_drawing(tree, kinds, vals, node_names=names, marks=marks)
    sol = ["Run alpha–beta depth-first, left to right, passing (α, β) down. A MIN node stops as soon as its value "
           "≤ α; a MAX node stops as soon as its value ≥ β.",
           *[f"• {t}" for t in trace],
           solfig,
           f"Leaves evaluated ({len(ev)}): {', '.join(names[x] for x in ev)}. Leaves pruned ({len(pr)}): "
           f"{', '.join(names[x] for x in pr)}. Root value = {root} (same as plain minimax, "
           f"{memo['R']} — pruning never changes the root value)."]
    variant = rng.choice(["count", "msq", "evaluated"])
    head = ("Alpha–beta pruning is applied to the game tree below, exploring children strictly from "
            "<b>left to right</b> (leaves are labelled L1, L2, … under the boxes). ")
    if variant == "count":
        return Q("Adversarial Search", "NAT", 2, head + "How many leaf nodes are <b>not</b> evaluated (pruned)?",
                 None, (len(pr), len(pr)), sol, [fig, legend_game()], "Alpha-beta")
    if variant == "evaluated":
        return Q("Adversarial Search", "NAT", 2, head + "How many leaf nodes are evaluated?",
                 None, (len(ev), len(ev)), sol, [fig, legend_game()], "Alpha-beta")
    allL = leaves_under(tree, "R")
    pick_p = rng.sample(pr, min(len(pr), rng.choice([1, 2])))
    pick_e = rng.sample(ev, 4 - len(pick_p))
    st = [(f"Leaf {names[l]} is pruned.", l in pr) for l in pick_p + pick_e]
    opts, ans = make_msq(st, rng)
    opts_sorted = sorted(zip(opts, range(4)), key=lambda t: int(t[0].split()[1][1:]))
    newopts = [o for o, _ in opts_sorted]
    newans = [i for i, (o, old) in enumerate(opts_sorted) if old in ans]
    return Q("Adversarial Search", "MSQ", 2, head + "Which of the following leaves is/are pruned (never evaluated)?",
             newopts, newans, sol, [fig, legend_game()], "Alpha-beta")


def q_expectimax(rng):
    tree, kinds, vals, names = random_tree(rng, depth=2, chance=True)
    probs = {}
    elab = {}
    for n in tree:
        if kinds[n] == "chance":
            k = len(tree[n])
            choices = {2: [(0.5, 0.5), (0.4, 0.6), (0.3, 0.7), (0.2, 0.8), (0.75, 0.25)],
                       3: [(0.2, 0.3, 0.5), (0.5, 0.25, 0.25), (0.1, 0.6, 0.3), (0.4, 0.4, 0.2)],
                       4: [(0.25, 0.25, 0.25, 0.25), (0.1, 0.2, 0.3, 0.4), (0.4, 0.3, 0.2, 0.1)]}[k]
            p = list(rng.choice(choices))
            rng.shuffle(p)
            for c, pp in zip(tree[n], p):
                probs[c] = pp
                elab[(n, c)] = num(pp, 2)
    memo = {}

    def ev(n):
        if kinds[n] == "leaf":
            memo[n] = vals[n]
        elif kinds[n] == "chance":
            memo[n] = sum(probs[c] * ev(c) for c in tree[n])
        else:
            memo[n] = max(ev(c) for c in tree[n])
        return memo[n]
    v = ev("R")
    fig = tree_drawing(tree, kinds, vals, edge_labels=elab, node_names=names)
    lines = []
    for c in tree["R"]:
        terms = " + ".join(f"{num(probs[x], 2)}×{vals[x]}" for x in tree[c])
        lines.append(f"{names[c]} = {terms} = {num(memo[c], 3)}")
    sol = ["A chance node's value is the probability-weighted average of its children; MAX takes the maximum.",
           *[f"• {l}" for l in lines],
           f"Root = max({', '.join(num(memo[c], 3) for c in tree['R'])}) = <b>{num(v, 3)}</b>.",
           "Note: unlike minimax, expectimax values are sensitive to positive affine vs. non-linear transformations "
           "of the utilities — only positive linear transformations preserve the optimal decision."]
    text = ("In the expectimax tree below, the root is a MAX node and each child of the root is a CHANCE node; "
            "probabilities are written on the edges. What is the expectimax value of the root? "
            "(round off to 2 decimal places)")
    return Q("Adversarial Search", "NAT", 2, text, None, (round(v - 0.01, 2), round(v + 0.01, 2)), sol,
             [fig, legend_game(chance=True)], "Expectimax")


def q_ab_bestcase(rng):
    b = rng.choice([2, 3, 4, 5])
    d = rng.choice([2, 3, 4, 5]) if b < 5 else rng.choice([2, 3, 4])
    import math
    best = b ** math.ceil(d / 2) + b ** math.floor(d / 2) - 1
    text = (f"A uniform game tree has branching factor b = {b} and depth d = {d} (so b^d = {b ** d} leaves). "
            f"With <b>perfect move ordering</b>, what is the minimum number of leaf nodes that alpha–beta pruning "
            f"must evaluate?")
    sol = ["Knuth & Moore (1975): with perfect ordering the minimum number of leaves examined is "
           "b^⌈d/2⌉ + b^⌊d/2⌋ − 1.",
           f"= {b}^{math.ceil(d / 2)} + {b}^{math.floor(d / 2)} − 1 = {b ** math.ceil(d / 2)} + "
           f"{b ** math.floor(d / 2)} − 1 = <b>{best}</b>, versus {b ** d} for plain minimax. "
           "This is why alpha–beta can search roughly twice as deep in the same time (O(b^(d/2)))."]
    return Q("Adversarial Search", "NAT", 1, text, None, (best, best), sol, [], "Alpha-beta complexity")
