"""Rebalance MCQ answer letters within a set by swapping option pairs.

For each MCQ whose key must move from X to Y, options X and Y are swapped, and every letter
reference to X/Y in text, solution, verify, etc. is swapped too. Each changed question is
re-run through its verify block; on failure the change is reverted.  Option-by-option
bullet lines ("- (B) ...") in solutions are re-sorted into A-D order afterwards.

usage: python3 tools/rebalance.py sets/set_03.py [...]   (rewrites the files in place)
"""
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from schema import load_set, run_snippet  # noqa: E402

TEXT_FIELDS = ("text", "text2", "solution", "solution_after", "solution_code")


def swap_letters_text(s, x, y):
    if not s:
        return s
    pats = [r"(?<![\w(])\(%s\)", r"(?<=[Oo]ption )%s\b", r"(?<=[Oo]ption \*\*)%s\b",
            r"(?<=[Oo]ptions )%s\b", r"(?<=[Aa]nswer: )%s\b", r"(?<=[Aa]nswer is )%s\b"]

    def sw(m):
        t = m.group(0)
        return t.replace(x, "\0").replace(y, x).replace("\0", y)
    big = "|".join("(?:%s)|(?:%s)" % (p % x, p % y) for p in pats)
    return re.sub(big, sw, s)


def swap_letters_code(s, x, y):
    if not s:
        return s

    def sw(m):
        t = m.group(0)
        return t.replace(x, "\0").replace(y, x).replace("\0", y)
    return re.sub(r"(['\"])(%s|%s)\1" % (x, y), sw, s)


def sort_option_bullets(s):
    if not s:
        return s
    lines = s.split("\n")
    out, i = [], 0
    pat = re.compile(r"^\s*- (\*\*)?\(?([A-D])\)")
    while i < len(lines):
        if pat.match(lines[i]):
            j = i
            while j < len(lines) and pat.match(lines[j]):
                j += 1
            block = lines[i:j]
            letters = [pat.match(l).group(2) for l in block]
            if len(set(letters)) == len(letters):
                block = [l for _, l in sorted(zip(letters, block))]
            out += block
            i = j
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def apply_swap(q, x, y):
    q = dict(q)
    L = "ABCD"
    opts = list(q["options"])
    ix, iy = L.index(x), L.index(y)
    opts[ix], opts[iy] = opts[iy], opts[ix]
    q["options"] = opts
    m = {x: y, y: x}
    if isinstance(q["answer"], list):
        q["answer"] = sorted(m.get(a, a) for a in q["answer"])
    else:
        q["answer"] = m.get(q["answer"], q["answer"])
    for f in ("solution", "solution_after"):
        if q.get(f):
            q[f] = sort_option_bullets(swap_letters_text(q[f], x, y))
    if q.get("verify"):
        # verify was written against the original option order: map the key back first
        q["verify"] = ("_m = {%r: %r, %r: %r}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) "
                       "if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)\n" % (x, y, y, x)) + q["verify"]
    return q


# ------------------------------------------------------------------ serialisation
def s_str(v, ind):
    if "\n" in v and "'''" not in v and not v.endswith("\\") and not v.endswith("'"):
        body = v.replace("\\", "\\\\")
        return "'''" + body + "'''"
    return repr(v)


def ser(v, ind=0):
    pad = " " * ind
    if isinstance(v, dict):
        if not v:
            return "{}"
        items = ["%s    %r: %s," % (pad, k, ser(val, ind + 4)) for k, val in v.items()]
        return "{\n" + "\n".join(items) + "\n" + pad + "}"
    if isinstance(v, (list, tuple)):
        if all(not isinstance(x, (dict, list, tuple)) and not (isinstance(x, str) and "\n" in x) for x in v):
            r = "[" + ", ".join(ser(x) for x in v) + "]"
            if len(r) + ind < 100:
                return r
        items = ["%s    %s," % (pad, ser(x, ind + 4)) for x in v]
        return "[\n" + "\n".join(items) + "\n" + pad + "]"
    if isinstance(v, str):
        return s_str(v, ind)
    return repr(v)


def rebalance(path, do_mcq=True):
    S = load_set(path)
    qs = S["questions"]
    mcq = [i for i, q in enumerate(qs) if q["type"] == "MCQ"]
    rnd = random.Random(1000 + S["number"])
    targets = ["ABCD"[k % 4] for k in range(len(mcq))]
    rnd.shuffle(targets)
    changed = 0
    for i, tgt in (zip(mcq, targets) if do_mcq else []):
        q = qs[i]
        cur = q["answer"]
        if cur == tgt:
            continue
        nq = apply_swap(q, cur, tgt)
        code = nq.get("code") if nq.get("run_code", True) else None
        if nq.get("verify"):
            err = run_snippet(code, nq["verify"], nq["answer"])
            if err:
                print("  set %02d Q%d: swap %s->%s failed verify, kept original" % (S["number"], i + 1, cur, tgt))
                continue
        qs[i] = nq
        changed += 1
    for i, q in enumerate(qs):
        if q["type"] != "MSQ":
            continue
        perm = list("ABCD")
        rnd.shuffle(perm)          # option at old position k moves to position perm[k]
        nq = q
        cur = list("ABCD")         # cur[k] = current position letter of original option k
        for k in range(4):
            tgt = perm[k]
            if cur[k] != tgt:
                a, b = cur[k], tgt
                nq = apply_swap(nq, a, b)
                cur = [b if c == a else (a if c == b else c) for c in cur]
        if nq.get("verify"):
            code = nq.get("code") if nq.get("run_code", True) else None
            if run_snippet(code, nq["verify"], nq["answer"]):
                print("  set %02d Q%d: MSQ permutation failed verify, kept original" % (S["number"], i + 1))
                continue
        qs[i] = nq
    src = open(path).read()
    header = src[:src.index("SET =")] if "SET =" in src else ""
    with open(path, "w") as f:
        f.write(header + "SET = " + ser(S) + "\n")
    load_set(path)  # sanity: still importable
    print("%s: %d MCQ keys moved -> %s" % (path, changed, "".join(q["answer"] for q in qs if q["type"] == "MCQ")))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for p in args:
        rebalance(p, do_mcq="--msq-only" not in sys.argv)
