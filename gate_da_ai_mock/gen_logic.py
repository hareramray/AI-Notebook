"""Propositional and predicate logic generators (answers computed by brute force)."""
import itertools

from common import Q, make_mcq, make_msq, num, tbl
from draw import graph_drawing

SYM = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}


def V(x):
    return ("var", x)


def Not(a):
    return ("not", a)


def B(op, a, b):
    return (op, a, b)


def ev(f, env):
    t = f[0]
    if t == "var":
        return env[f[1]]
    if t == "not":
        return not ev(f[1], env)
    a, b = ev(f[1], env), ev(f[2], env)
    return {"and": a and b, "or": a or b, "imp": (not a) or b, "iff": a == b, "xor": a != b}[t]


def s(f, top=True):
    t = f[0]
    if t == "var":
        return f[1]
    if t == "not":
        return "¬" + s(f[1], False)
    r = f"{s(f[1], False)} {SYM[t]} {s(f[2], False)}"
    return r if top else f"({r})"


def vars_of(f, acc=None):
    acc = set() if acc is None else acc
    if f[0] == "var":
        acc.add(f[1])
    else:
        for x in f[1:]:
            vars_of(x, acc)
    return acc


def envs(vs):
    for bits in itertools.product([True, False], repeat=len(vs)):
        yield dict(zip(vs, bits))


def models(f, vs):
    return [e for e in envs(vs) if ev(f, e)]


def rand_f(rng, vs, depth, ops=("and", "or", "imp", "iff")):
    if depth == 0 or (depth < 2 and rng.random() < 0.3):
        v = V(rng.choice(vs))
        return Not(v) if rng.random() < 0.3 else v
    if rng.random() < 0.15:
        return Not(rand_f(rng, vs, depth - 1, ops))
    return B(rng.choice(ops), rand_f(rng, vs, depth - 1, ops), rand_f(rng, vs, depth - 1, ops))


def TF(x):
    return "T" if x else "F"


def truth_table(fs, vs, labels=None):
    labels = labels or [s(f) for f in fs]
    rows = [vs + labels]
    for e in envs(vs):
        rows.append([TF(e[v]) for v in vs] + [f"<b>{TF(ev(f, e))}</b>" if i == len(fs) - 1 else TF(ev(f, e))
                                              for i, f in enumerate(fs)])
    return rows


def q_model_count(rng):
    n = rng.choice([3, 3, 4])
    vs = ["P", "Q", "R", "S"][:n]
    while True:
        f = rand_f(rng, vs, 3)
        if vars_of(f) == set(vs) and 0 < len(models(f, vs)) < 2 ** n and f[0] not in ("var", "not"):
            break
    m = len(models(f, vs))
    variant = rng.choice(["models", "models", "maxterms"])
    sub = [f[1], f[2]] if f[0] != "not" else [f[1]]
    tt = truth_table(sub + [f], vs)
    w = [26] * n + [ (430 - 26 * n) / (len(sub) + 1)] * (len(sub) + 1)
    if variant == "models":
        text = (f"How many of the {2 ** n} truth assignments to {', '.join(vs)} satisfy the formula<br/>"
                f"<b>F = {s(f)}</b> ?")
        ans = m
        tail = f"Rows where F = T: <b>{m}</b>."
    else:
        text = (f"The formula <b>F = {s(f)}</b> is written in canonical (full) conjunctive normal form, i.e. as a "
                f"conjunction of maxterms over {', '.join(vs)}. How many maxterms (clauses) does it contain?")
        ans = 2 ** n - m
        tail = (f"F has {m} models, so it is false in {2 ** n} − {m} = <b>{ans}</b> rows; each falsifying row "
                f"contributes exactly one maxterm to the canonical CNF.")
    sol = ["Build the truth table (sub-formulas shown first):", tbl(tt, widths=w), tail]
    return Q("Propositional Logic", "NAT", 1 if n == 3 else 2, text, None, (ans, ans), sol, [], "Model counting")


TAUT_TEMPLATES = [
    lambda a, b, c: B("iff", B("imp", a, b), B("imp", Not(b), Not(a))),
    lambda a, b, c: B("imp", B("and", B("imp", a, b), B("imp", b, c)), B("imp", a, c)),
    lambda a, b, c: B("imp", B("and", a, B("imp", a, b)), b),
    lambda a, b, c: B("imp", B("imp", B("imp", a, b), a), a),
    lambda a, b, c: B("imp", B("and", B("imp", a, b), Not(b)), Not(a)),
    lambda a, b, c: B("iff", Not(B("and", a, b)), B("or", Not(a), Not(b))),
    lambda a, b, c: B("imp", B("and", B("or", a, b), B("or", Not(a), c)), B("or", b, c)),
    lambda a, b, c: B("iff", B("imp", a, B("imp", b, c)), B("imp", B("and", a, b), c)),
    lambda a, b, c: B("or", B("imp", a, b), B("imp", b, a)),
    lambda a, b, c: B("imp", a, B("imp", b, a)),
]
NONTAUT_TEMPLATES = [
    lambda a, b, c: B("imp", B("imp", a, b), B("imp", b, a)),
    lambda a, b, c: B("imp", B("and", B("imp", a, b), b), a),
    lambda a, b, c: B("imp", B("and", B("imp", a, b), Not(a)), Not(b)),
    lambda a, b, c: B("iff", Not(B("and", a, b)), B("and", Not(a), Not(b))),
    lambda a, b, c: B("imp", B("imp", a, c), B("imp", B("or", a, b), c)),
    lambda a, b, c: B("iff", B("imp", B("imp", a, b), c), B("imp", a, B("imp", b, c))),
    lambda a, b, c: B("imp", B("or", a, b), B("and", a, b)),
    lambda a, b, c: B("imp", B("and", B("imp", a, c), B("imp", b, c)), B("and", a, b)),
]


def q_tautology(rng):
    vs = ["P", "Q", "R"]
    while True:
        picks = []
        nt = rng.choice([1, 2, 2, 3])
        for tpl in rng.sample(TAUT_TEMPLATES, nt):
            a, b, c = [V(x) for x in rng.sample(vs, 3)]
            if rng.random() < 0.3:
                a = Not(a)
            picks.append(tpl(a, b, c))
        for tpl in rng.sample(NONTAUT_TEMPLATES, 4 - nt):
            a, b, c = [V(x) for x in rng.sample(vs, 3)]
            picks.append(tpl(a, b, c))
        st = []
        for f in picks:
            fv = sorted(vars_of(f))
            st.append((f, all(ev(f, e) for e in envs(fv))))
        if any(t for _, t in st):
            break
    rng.shuffle(st)
    opts = [s(f) for f, _ in st]
    ans = [i for i, (_, t) in enumerate(st) if t]
    sol = []
    for i, (f, t) in enumerate(st):
        fv = sorted(vars_of(f))
        if t:
            sol.append(f"({chr(65 + i)}) {s(f)}: true in all {2 ** len(fv)} assignments ⇒ <b>valid</b>.")
        else:
            bad = next(e for e in envs(fv) if not ev(f, e))
            sol.append(f"({chr(65 + i)}) {s(f)}: <b>not valid</b> — counter-model "
                       + ", ".join(f"{k}={TF(v)}" for k, v in bad.items()) + ".")
    sol.append("Useful facts: contraposition, hypothetical syllogism, modus ponens/tollens, Peirce's law, "
               "De Morgan, resolution and exportation are tautologies; affirming the consequent, denying the "
               "antecedent and the converse are fallacies.")
    return Q("Propositional Logic", "MSQ", 2, "Which of the following formulas is/are <b>valid</b> (tautologies)?",
             opts, ans, sol, [], "Validity")


def q_entailment(rng):
    vs = ["P", "Q", "R", "S"][:rng.choice([3, 4])]
    for _ in range(500):
        kb = [rand_f(rng, vs, 2, ops=("and", "or", "imp", "iff")) for _ in range(3)]
        kbf = B("and", B("and", kb[0], kb[1]), kb[2])
        km = models(kbf, vs)
        if not (1 <= len(km) <= 3):
            continue
        cands = []
        for _ in range(60):
            c = rand_f(rng, vs, rng.choice([1, 2]))
            ent = all(ev(c, e) for e in km)
            if s(c) not in [s(x) for x, _ in cands] and len(s(c)) > 1:
                cands.append((c, ent))
        tr = [x for x in cands if x[1]]
        fa = [x for x in cands if not x[1]]
        if len(tr) >= 1 and len(fa) >= 2:
            k = rng.choice([1, 2, 2])
            k = min(k, len(tr))
            chosen = rng.sample(tr, k) + rng.sample(fa, 4 - k)
            break
    rng.shuffle(chosen)
    opts = [s(c) for c, _ in chosen]
    ans = [i for i, (_, t) in enumerate(chosen) if t]
    text = ("A knowledge base KB contains exactly the following three sentences:<br/>"
            + "<br/>".join(f"&nbsp;&nbsp;({i + 1})&nbsp; {s(k)}" for i, k in enumerate(kb))
            + "<br/>Which of the following sentences is/are entailed by KB (KB ⊨ α)?")
    rows = [vs + ["KB"]]
    for e in km:
        rows.append([TF(e[v]) for v in vs] + ["T"])
    sol = [f"KB ⊨ α iff α is true in every model of KB. Enumerating all {2 ** len(vs)} assignments, KB is true "
           f"in exactly {len(km)} of them:", tbl(rows, widths=[30] * len(vs) + [30])]
    for i, (c, t) in enumerate(chosen):
        if t:
            sol.append(f"({chr(65 + i)}) {s(c)} is true in all models of KB ⇒ <b>entailed</b>.")
        else:
            bad = next(e for e in km if not ev(c, e))
            sol.append(f"({chr(65 + i)}) {s(c)} is false in the KB-model "
                       + ", ".join(f"{k}={TF(v)}" for k, v in bad.items()) + " ⇒ not entailed.")
    return Q("Propositional Logic", "MSQ", 2, text, opts, ans, sol, [], "Entailment")


# --- rewrites for equivalence questions
def correct_rewrites(f):
    out = []
    t = f[0]
    if t == "imp":
        out += [B("or", Not(f[1]), f[2]), B("imp", Not(f[2]), Not(f[1])), Not(B("and", f[1], Not(f[2])))]
    if t == "iff":
        out += [B("and", B("imp", f[1], f[2]), B("imp", f[2], f[1])),
                B("or", B("and", f[1], f[2]), B("and", Not(f[1]), Not(f[2]))), B("iff", Not(f[1]), Not(f[2]))]
    if t in ("and", "or"):
        dual = "or" if t == "and" else "and"
        out += [Not(B(dual, Not(f[1]), Not(f[2]))), B(t, f[2], f[1])]
        if f[2][0] in ("and", "or") and f[2][0] != t:
            x, y = f[2][1], f[2][2]
            out.append(B(dual, B(t, f[1], x), B(t, f[1], y)))
    return out


def wrong_rewrites(f):
    out = []
    t = f[0]
    if t == "imp":
        out += [B("imp", f[2], f[1]), B("imp", Not(f[1]), Not(f[2])), B("or", f[1], Not(f[2])),
                B("and", Not(f[1]), f[2])]
    if t == "iff":
        out += [B("and", B("imp", f[1], f[2]), B("imp", Not(f[2]), Not(f[1]))), B("iff", f[1], Not(f[2])),
                B("or", B("and", f[1], f[2]), B("and", f[1], Not(f[2])))]
    if t in ("and", "or"):
        dual = "or" if t == "and" else "and"
        out += [Not(B(t, Not(f[1]), Not(f[2]))), B(dual, f[1], f[2]), B(t, Not(f[1]), f[2])]
    return out


def q_equivalence(rng):
    vs = ["P", "Q", "R"]
    for _ in range(300):
        op = rng.choice(["imp", "iff", "and", "or", "imp"])
        a = rand_f(rng, vs, 1)
        b = rand_f(rng, vs, 1)
        f = B(op, a, b)
        if len(vars_of(f)) < 2:
            continue
        fv = sorted(vars_of(f))
        good = [(g, True) for g in correct_rewrites(f)]
        bad = [(g, False) for g in wrong_rewrites(f)]
        allc = []
        for g, _ in good + bad:
            gv = sorted(vars_of(g) | set(fv))
            eq = all(ev(g, e) == ev(f, e) for e in envs(gv))
            if s(g) != s(f) and s(g) not in [s(x) for x, _ in allc]:
                allc.append((g, eq))
        tr = [x for x in allc if x[1]]
        fa = [x for x in allc if not x[1]]
        if len(tr) >= 1 and len(fa) >= 1 and len(allc) >= 4:
            k = min(len(tr), rng.choice([1, 2, 2, 3]), 3)
            k = max(k, 4 - len(fa))
            chosen = rng.sample(tr, k) + rng.sample(fa, 4 - k)
            break
    rng.shuffle(chosen)
    opts = [s(c) for c, _ in chosen]
    ans = [i for i, (_, t) in enumerate(chosen) if t]
    sol = [f"Compare truth tables with F = {s(f)} (or use the standard laws: implication elimination "
           "α → β ≡ ¬α ∨ β, contraposition, De Morgan, biconditional elimination, distributivity)."]
    for i, (c, t) in enumerate(chosen):
        gv = sorted(vars_of(c) | vars_of(f))
        if t:
            sol.append(f"({chr(65 + i)}) {s(c)} — agrees with F on all {2 ** len(gv)} rows ⇒ <b>equivalent</b>.")
        else:
            e = next(e for e in envs(gv) if ev(c, e) != ev(f, e))
            sol.append(f"({chr(65 + i)}) {s(c)} — differs at " + ", ".join(f"{k}={TF(v)}" for k, v in e.items())
                       + f" (F = {TF(ev(f, e))}, option = {TF(ev(c, e))}) ⇒ not equivalent.")
    return Q("Propositional Logic", "MSQ", 2,
             f"Which of the following formulas is/are logically equivalent to <b>F = {s(f)}</b> ?",
             opts, ans, sol, [], "Equivalence")


# --- resolution
def lit_s(l):
    return ("¬" if not l[1] else "") + l[0]


def cl_s(c):
    if not c:
        return "□ (empty clause)"
    return "(" + " ∨ ".join(lit_s(l) for l in sorted(c)) + ")"


def resolve(c1, c2):
    out = []
    for (v, sg) in c1:
        if (v, not sg) in c2:
            r = (c1 - {(v, sg)}) | (c2 - {(v, not sg)})
            if not any((x, not y) in r for x, y in r):
                out.append((frozenset(r), v))
    return out


def closure(clauses, limit=400):
    known = {c: None for c in clauses}
    changed = True
    while changed and len(known) < limit:
        changed = False
        ks = list(known)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                for r, v in resolve(ks[i], ks[j]):
                    if r not in known:
                        known[r] = (ks[i], ks[j], v)
                        changed = True
    return known


def derivation(known, c, out, seen):
    if c in seen or known[c] is None:
        return
    a, b, v = known[c]
    derivation(known, a, out, seen)
    derivation(known, b, out, seen)
    seen.add(c)
    out.append(f"resolve {cl_s(a)} and {cl_s(b)} on {v} ⇒ {cl_s(c)}")


def q_resolution(rng):
    vs = ["P", "Q", "R", "S"]
    for _ in range(500):
        n = rng.choice([4, 5])
        cls = set()
        while len(cls) < n:
            k = rng.choice([1, 2, 2, 3])
            vv = rng.sample(vs, k)
            cls.add(frozenset((x, rng.random() < 0.5) for x in vv))
        cls = list(cls)
        known = closure(cls)
        derived = [c for c in known if known[c] is not None]
        if len(derived) < 2 or len(known) > 120:
            continue
        cand_true = [c for c in derived if c]
        allv = []
        for _ in range(80):
            k = rng.choice([1, 2])
            vv = rng.sample(vs, k)
            c = frozenset((x, rng.random() < 0.5) for x in vv)
            if c not in known and c not in allv:
                allv.append(c)
        if len(allv) < 2 or not cand_true:
            continue
        has_empty = frozenset() in known
        st = []
        kt = min(len(cand_true), rng.choice([1, 2]))
        for c in rng.sample(cand_true, kt):
            st.append((c, True))
        for c in rng.sample(allv, 3 - kt):
            st.append((c, False))
        st.append(("EMPTY", has_empty))
        break
    rng.shuffle(st)
    opts, ans = [], []
    for i, (c, t) in enumerate(st):
        opts.append("The empty clause □ (i.e. the clause set is shown unsatisfiable)" if c == "EMPTY" else cl_s(c))
        if t:
            ans.append(i)
    text = ("Consider the clause set<br/>&nbsp;&nbsp;" + ",&nbsp; ".join(f"C{i + 1}: {cl_s(c)}" for i, c in enumerate(cls))
            + "<br/>Which of the following can be derived by repeatedly applying the propositional <b>resolution</b> "
              "rule (each step resolves exactly one complementary pair of literals; tautological resolvents are "
              "discarded; derived clauses may be reused)?")
    sol = ["Saturate the clause set under resolution (only the steps needed for the options are shown)."]
    for i, (c, t) in enumerate(st):
        lab = chr(65 + i)
        if c == "EMPTY":
            if t:
                steps = []
                derivation(known, frozenset(), steps, set())
                sol.append(f"({lab}) □ is derivable:")
                sol += [f"&nbsp;&nbsp;{k + 1}. {x}" for k, x in enumerate(steps)]
            else:
                sol.append(f"({lab}) The resolution closure contains {len(known)} clauses and no □, so the set is "
                           f"satisfiable (resolution is refutation-complete) ⇒ not derivable.")
        elif t:
            steps = []
            derivation(known, c, steps, set())
            sol.append(f"({lab}) {cl_s(c)} is derivable:")
            sol += [f"&nbsp;&nbsp;{k + 1}. {x}" for k, x in enumerate(steps)]
        else:
            sol.append(f"({lab}) {cl_s(c)} never appears in the resolution closure ⇒ not derivable "
                       "(note: a clause can be entailed yet not derivable, e.g. a weakening of a derived clause; "
                       "resolution is complete only for refutation).")
    return Q("Propositional Logic", "MSQ", 2, text, opts, ans, sol, [], "Resolution")


def q_forward_chaining(rng):
    atoms = list("ABCDEFHJK")
    for _ in range(500):
        facts = rng.sample(atoms[:5], rng.choice([2, 3]))
        rules = []
        for _ in range(rng.choice([5, 6, 7])):
            body = rng.sample(atoms, rng.choice([1, 2, 2, 3]))
            head = rng.choice([a for a in atoms if a not in body])
            rules.append((body, head))
        inferred = set(facts)
        rounds = []
        while True:
            new = []
            for body, head in rules:
                if head not in inferred and all(b in inferred for b in body):
                    new.append((body, head))
            heads = sorted({h for _, h in new})
            if not heads:
                break
            rounds.append(new)
            inferred |= set(heads)
        derived = inferred - set(facts)
        if 2 <= len(derived) and len(rounds) >= 2 and len(inferred) < len(atoms):
            break
    rtext = "<br/>".join(f"&nbsp;&nbsp;R{i + 1}: {' ∧ '.join(b)} → {h}" for i, (b, h) in enumerate(rules))
    variant = rng.choice(["nat", "msq"])
    sol = ["Forward chaining fires every rule whose premises are all known, adds the conclusion, and repeats "
           "until no new atom is added (sound and complete for Horn/definite clauses)."]
    known = set(facts)
    for k, new in enumerate(rounds, 1):
        fired = []
        for body, head in new:
            if head not in known:
                fired.append(f"{' ∧ '.join(body)} → {head}")
        heads = sorted({h for _, h in new})
        known |= set(heads)
        sol.append(f"Round {k}: fire {', '.join(fired)}; add {', '.join(heads)}.")
    sol.append(f"Fixed point: {{{', '.join(sorted(inferred))}}} — {len(inferred)} atoms are entailed "
               f"(facts: {', '.join(sorted(facts))}; newly derived: {', '.join(sorted(derived))}). Atoms never "
               f"derived: {', '.join(sorted(set(atoms) - inferred))}.")
    head = (f"A propositional definite-clause knowledge base over atoms {', '.join(atoms)} has facts "
            f"<b>{', '.join(facts)}</b> and rules:<br/>{rtext}<br/>")
    if variant == "nat":
        return Q("Propositional Logic", "NAT", 1,
                 head + "How many atoms (including the given facts) are entailed by the KB?",
                 None, (len(inferred), len(inferred)), sol, [], "Forward chaining")
    pool_t = list(derived)
    pool_f = list(set(atoms) - inferred)
    kt = min(len(pool_t), rng.choice([1, 2, 3]))
    kt = max(kt, 4 - len(pool_f))
    chosen = [(a, True) for a in rng.sample(pool_t, kt)] + [(a, False) for a in rng.sample(pool_f, 4 - kt)]
    chosen.sort()
    opts = [f"{a} is entailed" for a, _ in chosen]
    ans = [i for i, (_, t) in enumerate(chosen) if t]
    return Q("Propositional Logic", "MSQ", 2, head + "Using forward chaining, which of the following is/are TRUE?",
             opts, ans, sol, [], "Forward chaining")


# ------------------------------------------------------------------ predicate logic
def fol_statements(D, R):
    def r(x, y):
        return (x, y) in R
    out = []

    def add(txt, val, why):
        out.append((txt, val, why))
    # ∀x∃y R(x,y)
    bad = [x for x in D if not any(r(x, y) for y in D)]
    add("∀x ∃y R(x, y)", not bad,
        "every element has an outgoing edge" if not bad else f"{bad[0]} has no outgoing edge")
    good = [y for y in D if all(r(x, y) for x in D)]
    add("∃y ∀x R(x, y)", bool(good),
        f"y = {good[0]} receives an edge from every x (incl. itself)" if good else
        "no element receives edges from all elements (including a self-loop)")
    good = [x for x in D if all(r(x, y) for y in D)]
    add("∃x ∀y R(x, y)", bool(good),
        f"x = {good[0]} has edges to every y" if good else "no element has edges to all elements (incl. itself)")
    bad = [y for y in D if not any(r(x, y) for x in D)]
    add("∀y ∃x R(x, y)", not bad,
        "every element has an incoming edge" if not bad else f"{bad[0]} has no incoming edge")
    bad = [x for x in D if not r(x, x)]
    add("∀x R(x, x)", not bad, "every element has a self-loop" if not bad else f"no self-loop at {bad[0]}")
    good = [x for x in D if r(x, x)]
    add("∃x R(x, x)", bool(good), f"self-loop at {good[0]}" if good else "there are no self-loops")
    bad = [(x, y) for (x, y) in R if not r(y, x)]
    add("∀x ∀y (R(x, y) → R(y, x))", not bad,
        "every edge has its reverse" if not bad else f"R({bad[0][0]},{bad[0][1]}) holds but R({bad[0][1]},{bad[0][0]}) does not")
    bad = [(x, y, z) for (x, y) in R for z in D if r(y, z) and not r(x, z)]
    add("∀x ∀y ∀z ((R(x, y) ∧ R(y, z)) → R(x, z))", not bad,
        "all two-step paths are short-cut" if not bad else
        f"R({bad[0][0]},{bad[0][1]}) ∧ R({bad[0][1]},{bad[0][2]}) but ¬R({bad[0][0]},{bad[0][2]})")
    bad = [(x, y) for (x, y) in R if x != y and r(y, x)]
    add("∀x ∀y ((R(x, y) ∧ R(y, x)) → x = y)", not bad,
        "no pair of distinct elements is related both ways" if not bad else
        f"R({bad[0][0]},{bad[0][1]}) and R({bad[0][1]},{bad[0][0]}) with {bad[0][0]} ≠ {bad[0][1]}")
    good = [x for x in D if not any(r(y, x) for y in D)]
    add("∃x ∀y ¬R(y, x)", bool(good), f"{good[0]} has no incoming edge" if good else "every element has an incoming edge")
    good = [x for x in D if not any(r(x, y) for y in D)]
    add("∃x ∀y ¬R(x, y)", bool(good), f"{good[0]} has no outgoing edge" if good else "every element has an outgoing edge")
    bad = [x for x in D if not (any(r(x, y) and y != x for y in D))]
    add("∀x ∃y (x ≠ y ∧ R(x, y))", not bad,
        "every element has an edge to a different element" if not bad else
        f"{bad[0]} has no edge to a different element")
    bad = [(x, y) for x in D for y in D if x != y and not (r(x, y) or r(y, x))]
    add("∀x ∀y (x ≠ y → (R(x, y) ∨ R(y, x)))", not bad,
        "every two distinct elements are related in some direction" if not bad else
        f"neither R({bad[0][0]},{bad[0][1]}) nor R({bad[0][1]},{bad[0][0]})")
    return out


def q_fol_structure(rng):
    D = [1, 2, 3, 4]
    for _ in range(200):
        R = set()
        dens = rng.uniform(0.25, 0.45)
        for x in D:
            for y in D:
                if rng.random() < (dens * 0.6 if x == y else dens):
                    R.add((x, y))
        stm = fol_statements(D, R)
        tr = [x for x in stm if x[1]]
        fa = [x for x in stm if not x[1]]
        if len(tr) >= 2 and len(fa) >= 2 and len(R) >= 4:
            break
    k = rng.choice([1, 2, 2, 3])
    chosen = rng.sample(tr, k) + rng.sample(fa, 4 - k)
    rng.shuffle(chosen)
    pos = {1: (0.15, 0.85), 2: (0.85, 0.85), 3: (0.85, 0.12), 4: (0.15, 0.12)}
    loops = [x for x in D if (x, x) in R]
    edges = [(x, y, None) for (x, y) in R if x != y]
    # reverse edges drawn with slight offset: use separate curved lines by offsetting positions
    from reportlab.graphics.shapes import Drawing, Circle, String
    from draw import _arrow, NODE_FILL, NODE_STROKE, FONT_B, INK
    import math
    d = Drawing(260, 170)
    P = {k: (40 + v[0] * 180, 20 + v[1] * 130) for k, v in pos.items()}
    for (x, y, _) in edges:
        x1, y1 = P[x]
        x2, y2 = P[y]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ox, oy = -dy / L * 5, dx / L * 5
        if (y, x) not in R:
            ox = oy = 0
        _arrow(d, x1 + ox, y1 + oy, x2 + ox, y2 + oy, 14, 15)
    for v, (x, y) in P.items():
        if v in loops:
            d.add(Circle(x + (-14 if x < 130 else 14), y + (12 if y > 80 else -12), 9, fillColor=None,
                         strokeColor=colors_edge(), strokeWidth=1.1))
        d.add(Circle(x, y, 13, fillColor=NODE_FILL, strokeColor=NODE_STROKE, strokeWidth=1.2))
        d.add(String(x, y - 4, str(v), fontName=FONT_B, fontSize=11, fillColor=INK, textAnchor="middle"))
    text = ("Let the domain be D = {1, 2, 3, 4} and let the binary predicate R be interpreted as the relation "
            "drawn below (an arrow x → y means R(x, y) is true; a small loop at a node means R(x, x) is true). "
            "Which of the following sentences is/are TRUE in this interpretation?")
    opts = [c[0] for c in chosen]
    ans = [i for i, c in enumerate(chosen) if c[1]]
    sol = ["R = {" + ", ".join(f"({x},{y})" for x, y in sorted(R)) + "}."]
    for i, (t, v, why) in enumerate(chosen):
        sol.append(f"({chr(65 + i)}) {t}: <b>{'TRUE' if v else 'FALSE'}</b> — {why}.")
    sol.append("Remember: ∃y∀x R(x,y) ⇒ ∀x∃y R(x,y) but not conversely; quantifier order matters.")
    return Q("Predicate Logic", "MSQ", 2, text, opts, ans, sol, [d], "FOL semantics")


def colors_edge():
    from draw import EDGE
    return EDGE


RELPROPS = [
    ("∀x R(x, x)", lambda n: 2 ** (n * n - n), "reflexive: the n diagonal pairs are forced, the other n² − n pairs are free ⇒ 2^(n² − n)"),
    ("∀x ∀y (R(x, y) → R(y, x))", lambda n: 2 ** (n * (n + 1) // 2),
     "symmetric: choose freely the n diagonal pairs and one decision per unordered pair {x,y} ⇒ 2^(n(n+1)/2)"),
    ("∀x R(x, x) ∧ ∀x ∀y (R(x, y) → R(y, x))", lambda n: 2 ** (n * (n - 1) // 2),
     "reflexive and symmetric: only the n(n−1)/2 unordered off-diagonal pairs are free ⇒ 2^(n(n−1)/2)"),
    ("∀x ∀y ((R(x, y) ∧ R(y, x)) → x = y)", lambda n: 2 ** n * 3 ** (n * (n - 1) // 2),
     "antisymmetric: diagonal free (2^n); each unordered pair has 3 options (neither, one way, other way) ⇒ 2^n·3^(n(n−1)/2)"),
    ("∀x ∀y (R(x, y) → ¬R(y, x))", lambda n: 3 ** (n * (n - 1) // 2),
     "asymmetric: no self-loops; each unordered pair has 3 options ⇒ 3^(n(n−1)/2)"),
    ("∀x ∃y R(x, y)", lambda n: (2 ** n - 1) ** n,
     "every row of the relation matrix must be non-empty: (2^n − 1) choices per row ⇒ (2^n − 1)^n"),
    ("∃x ∀y R(x, y)", lambda n: 2 ** (n * n) - (2 ** n - 1) ** n,
     "complement of 'every row has at least one 0': 2^(n²) − (2^n − 1)^n"),
    ("∀x ¬R(x, x) ∧ ∀x ∀y (R(x, y) → R(y, x))", lambda n: 2 ** (n * (n - 1) // 2),
     "irreflexive and symmetric: diagonal forced to 0, one bit per unordered pair ⇒ 2^(n(n−1)/2)"),
]


def brute_rel(n, prop_txt):
    D = range(n)
    cells = [(x, y) for x in D for y in D]
    cnt = 0
    for bits in itertools.product([0, 1], repeat=n * n):
        R = {c for c, b in zip(cells, bits) if b}
        r = lambda x, y: (x, y) in R
        ok = {
            0: all(r(x, x) for x in D),
            1: all((not r(x, y)) or r(y, x) for x in D for y in D),
            2: all(r(x, x) for x in D) and all((not r(x, y)) or r(y, x) for x in D for y in D),
            3: all(not (r(x, y) and r(y, x)) or x == y for x in D for y in D),
            4: all((not r(x, y)) or not r(y, x) for x in D for y in D),
            5: all(any(r(x, y) for y in D) for x in D),
            6: any(all(r(x, y) for y in D) for x in D),
            7: all(not r(x, x) for x in D) and all((not r(x, y)) or r(y, x) for x in D for y in D),
        }[prop_txt]
        cnt += ok
    return cnt


def q_count_relations(rng):
    i = rng.randrange(len(RELPROPS))
    txt, f, why = RELPROPS[i]
    n = rng.choice([3, 3, 4]) if i not in (5, 6) else 3
    ans = f(n)
    if n <= 3:
        assert brute_rel(n, i) == ans, (txt, n)
    text = (f"Let D be a domain with exactly {n} elements and R a binary predicate symbol. In how many of the "
            f"2^{n * n} possible interpretations of R over D is the sentence <b>{txt}</b> true?")
    sol = [f"View R as an {n}×{n} 0/1 matrix. The sentence says R is " + why + f". With n = {n}: <b>{ans}</b>."]
    return Q("Predicate Logic", "NAT", 1, text, None, (ans, ans), sol, [], "Counting interpretations")


UNARY = [
    ("∀x (P(x) → Q(x))", lambda P, Q: all((not p) or q for p, q in zip(P, Q)),
     "each element independently has 3 allowed (P,Q) combinations (FF, FT, TT) ⇒ 3^n"),
    ("∃x (P(x) ∧ Q(x))", lambda P, Q: any(p and q for p, q in zip(P, Q)),
     "complement: no element has both, 3 combos each ⇒ 4^n − 3^n"),
    ("∀x (P(x) ↔ Q(x))", lambda P, Q: all(p == q for p, q in zip(P, Q)), "P and Q must coincide ⇒ 2^n"),
    ("∃x P(x) ∧ ∃x Q(x)", lambda P, Q: any(P) and any(Q), "each of P, Q must be non-empty ⇒ (2^n − 1)²"),
    ("∀x P(x) ∨ ∀x Q(x)", lambda P, Q: all(P) or all(Q), "inclusion–exclusion: 2^n + 2^n − 1"),
    ("∀x (P(x) ∨ Q(x)) ∧ ∃x ¬P(x)", lambda P, Q: all(p or q for p, q in zip(P, Q)) and not all(P),
     "3^n interpretations satisfy the ∀-part (each element: not both false); remove the 2^n of them with P true everywhere (Q then arbitrary) ⇒ 3^n − 2^n"),
    ("¬∃x (P(x) ∧ ¬Q(x)) ∧ ∃x P(x)", lambda P, Q: all((not p) or q for p, q in zip(P, Q)) and any(P),
     "P ⊆ Q gives 3^n; subtract the 2^n with P empty ⇒ 3^n − 2^n"),
]


def q_count_unary(rng):
    txt, f, why = rng.choice(UNARY)
    n = rng.choice([2, 3, 4])
    ans = 0
    for Pb in itertools.product([0, 1], repeat=n):
        for Qb in itertools.product([0, 1], repeat=n):
            ans += bool(f(Pb, Qb))
    text = (f"P and Q are unary predicate symbols and the domain has exactly {n} elements, so there are "
            f"4^{n} = {4 ** n} ways to interpret the pair (P, Q). For how many of them is "
            f"<b>{txt}</b> true?")
    sol = [f"Interpret P and Q as subsets of the domain; " + why + f". With n = {n} this gives <b>{ans}</b> "
           "(verified by enumerating all interpretations)."]
    return Q("Predicate Logic", "NAT", 1, text, None, (ans, ans), sol, [], "Counting interpretations")
