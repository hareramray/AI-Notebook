# Set 47 — Challenge Mock — Paper 2
SET = {
    "number": 47,
    "title": "Challenge Mock — Paper 2",
    "difficulty": "Hard",
    "focus": "hardest, multi-concept, trap-heavy 2-mark questions",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — `+=` vs `+` on lists, identity",
            "text": "Consider the following Python program. What is printed?",
            "code": '''a = [1, 2]
b = a
a += [3]
c = a
a = a + [4]
print(b, c is b, a is c, len(a))''',
            "options": ["`[1, 2] False False 4`", "`[1, 2, 3] True False 4`",
                        "`[1, 2, 3] True True 4`", "`[1, 2, 3, 4] True True 4`"],
            "answer": "B",
            "solution": (
                "For lists, `a += x` calls `list.__iadd__`, which **extends the same object in place**; "
                "`a = a + x` builds a **new** list and rebinds `a` to it.\n\n"
                "- `b = a`: b and a name the same list [1, 2].\n"
                "- `a += [3]`: that shared list becomes [1, 2, 3] — b sees it.\n"
                "- `c = a`: c is the same object as b.\n"
                "- `a = a + [4]`: a now names a new list [1, 2, 3, 4]; b and c still name the old one.\n\n"
                "So b = [1, 2, 3], `c is b` → True, `a is c` → False, len(a) = 4.\n\n"
                "- (A) treats `+=` as creating a new list (true for tuples/strings, not lists).\n"
                "- (C) treats `a = a + [4]` as in-place.\n"
                "- (D) treats both operations as in-place.\n\n"
                "**Trap:** `x += y` and `x = x + y` are equivalent only for immutable types."
            ),
            "verify": "assert OUTPUT.strip() == '[1, 2, 3] True False 4' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — try/except/finally and return",
            "text": "The value printed by the following Python program is ______.",
            "code": '''def f(n):
    try:
        if n % 2:
            return n * 10
        raise ValueError
    except ValueError:
        return n + 1
    finally:
        if n > 5:
            return -n

print(sum(f(k) for k in range(8)))''',
            "answer": "86",
            "solution": (
                "The `finally` block runs on every exit path. If it executes its own `return`, that value "
                "**replaces** whatever the `try` or `except` block was returning.\n\n"
                "- n = 0: even → ValueError → except returns 1; finally (0 > 5 false) → **1**\n"
                "- n = 1: odd → return 10 → **10**\n"
                "- n = 2: → **3**\n- n = 3: → **30**\n- n = 4: → **5**\n- n = 5: → **50**\n"
                "- n = 6: except would return 7, but finally returns **−6**\n"
                "- n = 7: try would return 70, but finally returns **−7**\n\n"
                "Sum = 1 + 10 + 3 + 30 + 5 + 50 − 6 − 7 = **86**.\n\n"
                "**Trap:** assuming `return` ends the function immediately. With n > 5 the pending return value "
                "(7 or 70) is discarded; ignoring `finally` would give 176."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Input-restricted deque permutations",
            "text": ("An **input-restricted deque** allows insertion only at the rear but deletion at both ends. "
                     "The values 1, 2, 3, 4 are inserted in this order; deletions may be interleaved with "
                     "insertions, and each deleted value is output at once. Which of the following output "
                     "sequences is/are possible?"),
            "options": ["4, 1, 3, 2", "4, 2, 1, 3", "3, 1, 4, 2", "4, 2, 3, 1"],
            "answer": ["A", "C"],
            "solution": (
                "When the first output is 4, all of 1, 2, 3, 4 have already been inserted, in order, so the deque "
                "is [1, 2, 3, 4] and afterwards only the two **ends** can be removed.\n\n"
                "- (A) [1,2,3,4]: delete rear 4 → [1,2,3]; delete front 1 → [2,3]; delete rear 3; then 2. "
                "**Possible.**\n"
                "- (B) After 4 the deque is [1, 2, 3]; 2 is in the middle — neither end. **Impossible.**\n"
                "- (C) Insert 1, 2, 3 → [1,2,3]; delete rear 3; delete front 1 → [2]; insert 4 → [2,4]; delete "
                "rear 4; delete 2. **Possible.** (This sequence is *impossible* for a stack — the deque's "
                "extra front deletion makes it reachable.)\n"
                "- (D) Again 2 would have to leave from the middle of [1, 2, 3]. **Impossible.**\n\n"
                "In fact, of the 24 permutations of 1..4, exactly these two (4,2,1,3 and 4,2,3,1) cannot be "
                "produced by an input-restricted deque.\n\n"
                "**Trap:** applying the stack rule (forbidden 3-1-2 pattern) — it rejects (C) wrongly."
            ),
            "verify": '''
import itertools
def possible(seq):
    n = len(seq); st = [(1, (), 0)]; seen = set()
    while st:
        nx, dq, oi = st.pop()
        if oi == n: return True
        if (nx, dq, oi) in seen: continue
        seen.add((nx, dq, oi))
        if nx <= n: st.append((nx + 1, dq + (nx,), oi + 0))
        if dq and dq[0] == seq[oi]: st.append((nx, dq[1:], oi + 1))
        if dq and dq[-1] == seq[oi]: st.append((nx, dq[:-1], oi + 1))
    return False
opts = [(4,1,3,2),(4,2,1,3),(3,1,4,2),(4,2,3,1)]
assert [L for L, s in zip('ABCD', opts) if possible(s)] == sorted(ANSWER)
assert [p for p in itertools.permutations(range(1, 5)) if not possible(p)] == [(4,2,1,3),(4,2,3,1)]
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Linear probing — expected probes",
            "text": ("A hash table with 10 slots (0–9) uses linear probing. Slots 1, 2, 3, 6 and 8 are occupied "
                     "and the rest are empty, as shown. A new key is inserted whose home slot is uniformly "
                     "distributed over 0–9. Counting every slot examined (including the one where the key is "
                     "placed), the expected number of probes for this insertion is ______ (rounded off to two "
                     "decimal places)."),
            "diagrams": [{"type": "hashtable", "size": 10, "slots": {1: 31, 2: 52, 3: 13, 6: 96, 8: 78},
                          "caption": "Current table"}],
            "answer": ["1.79", "1.81"],
            "solution": (
                "With linear probing, a key whose home slot lies inside a run of occupied slots must walk to the "
                "end of the run. Probes needed for each home slot h:\n\n"
                "- h = 0: empty → 1\n"
                "- h = 1: 1, 2, 3 full, 4 empty → 4\n"
                "- h = 2: → 3\n- h = 3: → 2\n- h = 4: → 1\n- h = 5: → 1\n"
                "- h = 6: 6 full, 7 empty → 2\n- h = 7: → 1\n"
                "- h = 8: 8 full, 9 empty → 2\n- h = 9: → 1\n\n"
                "Total = 1 + 4 + 3 + 2 + 1 + 1 + 2 + 1 + 2 + 1 = 18; expected = 18/10 = **1.80**.\n\n"
                "Notice also that slot 4 receives the key with probability 4/10 (home slots 1–4) while slot 5 "
                "gets only 1/10 — long runs grow faster (primary clustering).\n\n"
                "**Trap:** using the load-factor formula ½(1 + 1/(1 − α)²) = ½(1 + 4) = 2.5 — that is an "
                "asymptotic average over *random* tables, not this specific table."
            ),
            "verify": '''
occ = {1, 2, 3, 6, 8}; tot = 0
for h in range(10):
    i, c = h, 1
    while i in occ: i = (i + 1) % 10; c += 1
    tot += c
assert float(ANSWER[0]) <= tot / 10 <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "BST — insertion orders",
            "text": ("How many permutations of the keys 1, 2, 3, 4, 5, when inserted in that order into an "
                     "initially empty BST, produce exactly the tree shown?"),
            "diagrams": [{"type": "bintree", "tree": [3, [2, [1], None], [4, None, [5]]], "caption": "Target BST"}],
            "options": ["4", "6", "8", "12"],
            "answer": "B",
            "solution": (
                "A permutation produces this tree iff every node is inserted **before all its descendants**. "
                "Here that means: 3 first; 2 before 1; 4 before 5. Keys in different subtrees of 3 can be "
                "interleaved freely.\n\n"
                "- The root 3 must come first.\n"
                "- The left subtree sequence is forced: (2, 1). The right subtree sequence is forced: (4, 5).\n"
                "- Interleavings of two fixed sequences of length 2 and 2: C(4, 2) = **6**.\n\n"
                "They are: 3 2 1 4 5, 3 2 4 1 5, 3 2 4 5 1, 3 4 2 1 5, 3 4 2 5 1, 3 4 5 2 1.\n\n"
                "General rule: ways(T) = C(|L| + |R|, |L|) · ways(L) · ways(R).\n\n"
                "- (A) 4 forgets some interleavings. (C) 8 and (D) 12 allow 1 before 2 or 5 before 4, which "
                "would change the shape.\n\n"
                "**Trap:** thinking the order must be level-order; any topological order of the tree (parents "
                "before children) works."
            ),
            "verify": '''
import itertools
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
target = [3, [2, [1, None, None], None], [4, None, [5, None, None]]]
cnt = 0
for p in itertools.permutations(range(1, 6)):
    t = None
    for k in p: t = ins(t, k)
    cnt += t == target
assert cnt == 6 and ['4','6','8','12'][ord(ANSWER) - 65] == '6'
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — worst-case iterations",
            "text": ("The standard iterative binary search (lo = 0, hi = n − 1; while lo ≤ hi: mid = ⌊(lo + hi)/2⌋; "
                     "compare; move lo or hi past mid) is run on a sorted array of n distinct keys. "
                     "The **smallest** n for which some search (successful or unsuccessful) can execute the loop "
                     "body 8 times is ______."),
            "answer": "128",
            "solution": (
                "The loop examines the nodes of an implicit, height-balanced decision tree on n keys. Its worst "
                "case equals the number of levels, ⌊log₂ n⌋ + 1, and an unsuccessful search never takes more "
                "iterations than that (it ends just below a node on the deepest level).\n\n"
                "We need ⌊log₂ n⌋ + 1 ≥ 8, i.e. ⌊log₂ n⌋ ≥ 7, i.e. n ≥ 2⁷ = **128**.\n\n"
                "Check: with n = 127 the tree is perfect with 7 levels (2⁷ − 1 nodes), so every search ends "
                "within 7 iterations. Adding one key (n = 128) creates an 8th level containing one node.\n\n"
                "**Trap:** answering 255 or 256 (confusing “at most 8” with “at least 8”), or 127 "
                "(the largest n for which 7 iterations always suffice)."
            ),
            "verify": '''
def worst(n):
    w = 0
    for x in range(-1, 2 * n + 1):            # keys are 0, 2, 4, ...; odd x are misses
        lo, hi, c = 0, n - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2; c += 1
            if 2 * mid == x: break
            if 2 * mid < x: lo = mid + 1
            else: hi = mid - 1
        w = max(w, c)
    return w
assert worst(127) == 7 and worst(128) == 8 and int(ANSWER) == 128
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Graph theory — edges forcing connectivity",
            "text": ("What is the minimum number m such that **every** simple undirected graph on 10 vertices "
                     "with m edges is connected?"),
            "options": ["9", "36", "37", "45"],
            "answer": "C",
            "solution": (
                "Find the largest number of edges a **disconnected** simple graph on 10 vertices can have; m is "
                "one more than that.\n\n"
                "A disconnected graph splits into parts of sizes k and 10 − k with no edges between them, so it "
                "has at most C(k, 2) + C(10 − k, 2) edges, maximised at the extreme split k = 1: an isolated "
                "vertex plus K₉ → C(9, 2) = 36 edges.\n\n"
                "So 36 edges do not guarantee connectivity (K₉ + isolated vertex), but any graph with **37** "
                "edges must be connected.\n\n"
                "- (A) 9 = n − 1 is the minimum number of edges in *some* connected graph (a tree), not a "
                "guarantee.\n"
                "- (B) 36 is the largest disconnected case.\n"
                "- (D) 45 = C(10, 2) is the complete graph.\n\n"
                "**Trap:** confusing “can be connected” (n − 1 edges) with “must be connected” "
                "(C(n − 1, 2) + 1 edges)."
            ),
            "verify": '''
mx = max(k*(k-1)//2 + (10-k)*(9-k)//2 for k in range(1, 10))
assert mx == 36 and ['9','36','37','45'][ord(ANSWER) - 65] == str(mx + 1)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Stability depends on the comparison",
            "text": "Which of the following sorting procedures is/are **stable**?",
            "options": ["Insertion sort that shifts A[j] right while `A[j] > key`",
                        "Bubble sort that swaps adjacent elements when `A[j] >= A[j+1]`",
                        "Merge sort whose merge takes from the left run only when `L[i] <= R[j]`",
                        "Quicksort with Lomuto partitioning (pivot = last element, `a[j] <= pivot` goes left)"],
            "answer": ["A", "C"],
            "solution": (
                "A sort is stable if records with equal keys keep their input order. Whether an "
                "implementation is stable often hinges on a single `<` versus `<=`.\n\n"
                "- (A) **Stable.** The key stops at the first element ≤ it, so it never jumps over an equal key.\n"
                "- (B) **Not stable.** With `>=`, two adjacent equal keys are swapped, reversing their order; "
                "e.g. (1,'x'), (1,'y') becomes (1,'y'), (1,'x').\n"
                "- (C) **Stable.** On ties the merge takes from the **left** run, which holds the earlier records. "
                "(With strict `<` it would take from the right on ties and be unstable.)\n"
                "- (D) **Not stable.** The final pivot swap is a long-range exchange. Input "
                "[(1,a), (1,b), (0,c)]: pivot key 0, nothing goes left, and the pivot swap exchanges positions "
                "0 and 2 → [(0,c), (1,b), (1,a)]. The recursive call on [(1,b), (1,a)] leaves it unchanged, so "
                "the 1-records come out as b, a — reversed.\n\n"
                "**Trap:** classifying algorithms as stable/unstable without looking at the exact comparison."
            ),
            "verify": '''
import itertools
def ins(a):
    a = a[:]
    for i in range(1, len(a)):
        k = a[i]; j = i - 1
        while j >= 0 and a[j][0] > k[0]: a[j+1] = a[j]; j -= 1
        a[j+1] = k
    return a
def bub(a):
    a = a[:]
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j][0] >= a[j+1][0]: a[j], a[j+1] = a[j+1], a[j]
    return a
def ms(a):
    if len(a) <= 1: return a
    m = len(a) // 2; L, R = ms(a[:m]), ms(a[m:]); o = []; i = j = 0
    while i < len(L) and j < len(R):
        if L[i][0] <= R[j][0]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
def qs(a):
    a = a[:]
    def part(lo, hi):
        p = a[hi][0]; i = lo - 1
        for j in range(lo, hi):
            if a[j][0] <= p: i += 1; a[i], a[j] = a[j], a[i]
        a[i+1], a[hi] = a[hi], a[i+1]; return i + 1
    def rec(lo, hi):
        if lo < hi: q = part(lo, hi); rec(lo, q - 1); rec(q + 1, hi)
    rec(0, len(a) - 1); return a
def stable(f):
    for n in range(1, 6):
        for keys in itertools.product(range(3), repeat=n):
            recs = [(k, i) for i, k in enumerate(keys)]
            if f(recs) != sorted(recs): return False
    return True
assert [L for L, f in zip('ABCD', (ins, bub, ms, qs)) if stable(f)] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Counting heaps",
            "text": "The number of distinct binary max-heaps that can be built with the six distinct keys 1, 2, 3, 4, 5, 6 is ______.",
            "answer": "20",
            "solution": (
                "The shape of a 6-node heap is fixed (complete binary tree): the root's left subtree has 3 nodes "
                "(a root with two children) and the right subtree has 2 nodes (a root with one left child).\n\n"
                "- The root must be 6.\n"
                "- Choose which 3 of the remaining 5 keys go to the left subtree: C(5, 3) = 10. The other 2 go right.\n"
                "- Left subtree (3 nodes): its largest key is its root; the other two can be placed in 2 ways → 2.\n"
                "- Right subtree (2 nodes): the larger is the parent, the smaller the child → 1 way.\n\n"
                "Total = 10 × 2 × 1 = **20**.\n\n"
                "Recurrence: H(n) = C(n − 1, L) · H(L) · H(R), where L, R are the subtree sizes of the complete "
                "tree. (For comparison H(7) = C(6, 3)·2·2 = 80.)\n\n"
                "**Trap:** assuming both subtrees have the same size (as for 7 nodes) or that the 2-node subtree "
                "allows 2 arrangements — the single child position is forced."
            ),
            "solution_diagrams": [{"type": "heap", "values": [6, 5, 4, 2, 3, 1],
                                   "caption": "One of the 20 heaps (left subtree {5,2,3}, right {4,1})"}],
            "verify": '''
import itertools
c = sum(1 for p in itertools.permutations(range(1, 7))
        if all(p[(i-1)//2] > p[i] for i in range(1, 6)))
assert c == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Python — multi-pass stable sorting",
            "text": "Consider the following Python program. What is printed?",
            "code": '''data = ['b2', 'a3', 'c1', 'a1', 'b3', 'c2']
data.sort(key=lambda s: s[1])
data.sort(key=lambda s: s[0], reverse=True)
print(data)''',
            "options": ["`['c1', 'c2', 'b2', 'b3', 'a1', 'a3']`",
                        "`['c2', 'c1', 'b3', 'b2', 'a3', 'a1']`",
                        "`['c1', 'c2', 'b3', 'b2', 'a1', 'a3']`",
                        "`['a1', 'a3', 'b2', 'b3', 'c1', 'c2']`"],
            "answer": "A",
            "solution": (
                "Python's sort is **stable**, and `reverse=True` keeps stability: elements with equal keys stay "
                "in their original relative order (the sort does *not* simply reverse the stable ascending result).\n\n"
                "- Pass 1 (by digit): 1s: c1, a1; 2s: b2, c2; 3s: a3, b3 → "
                "`['c1', 'a1', 'b2', 'c2', 'a3', 'b3']`\n"
                "- Pass 2 (by letter, descending): c-group in current order c1, c2; b-group b2, b3; a-group a1, a3 → "
                "`['c1', 'c2', 'b2', 'b3', 'a1', 'a3']`\n\n"
                "Net effect: letters descending, digits ascending within a letter — the classic “sort by "
                "secondary key first, then by primary key” idiom.\n\n"
                "- (B) assumes `reverse=True` reverses ties too (it would if you sorted ascending and then called `reverse()`).\n"
                "- (C) mixes the two behaviours.\n"
                "- (D) ignores `reverse=True`.\n\n"
                "**Trap:** `sorted(x, reverse=True)` ≠ `sorted(x)[::-1]` when there are ties."
            ),
            "verify": '''
assert OUTPUT.strip() == "['c1', 'c2', 'b2', 'b3', 'a1', 'a3']" and ANSWER == 'A'
d2 = sorted(sorted(['b2','a3','c1','a1','b3','c2'], key=lambda s: s[1]), key=lambda s: s[0])[::-1]
assert d2 == ['c2', 'c1', 'b3', 'b2', 'a3', 'a1']
''',
        },
    ],
}
