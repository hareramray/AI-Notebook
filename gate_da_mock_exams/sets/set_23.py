# Set 23 — Hashing Analysis
SET = {
    'number': 23,
    'title': 'Hashing Analysis',
    'difficulty': 'GATE-level',
    'focus': 'load factor, expected probes, clustering, probability of collisions',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — dict keys that hash and compare equal',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''d = {1: 'a', True: 'b', 1.0: 'c'}
print(len(d), d[1], list(d.keys())[0])''',
            'options': ['`1 c 1`', '`3 a 1`', '`1 a 1.0`', '`1 c True`'],
            'answer': 'A',
            'solution': '''A dict locates a key by `hash(key)` and then confirms with `==`. In Python `hash(1) == hash(True) == hash(1.0)` and `1 == True == 1.0`, so all three literals denote the **same key**.

- `1: 'a'` creates the entry with key object `1`.
- `True: 'b'` finds the existing equal key; the **value** is replaced by 'b', but the original key object `1` is kept.
- `1.0: 'c'` again updates only the value → 'c'.

So `len(d)` = 1, `d[1]` = 'c', and the stored key is still the int `1`. Output: **1 c 1**.

- (B) treats the three keys as different objects — they are equal, so they collide *and* match.
- (C) assumes the first value is kept (it is the first **key** that is kept).
- (D) assumes the key object is replaced by the last one written.

**Trap:** a dict update replaces the value but never the key object. **Tip:** equal objects must have equal hashes — this is the contract every hash table relies on.''',
            'verify': '''
assert OUTPUT.strip() == "1 c 1" and ANSWER == "A"
assert type(list(d.keys())[0]) is int
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Simple uniform hashing — empty slot probability',
            'text': 'Ten keys are inserted into a hash table with 10 slots using separate chaining. Assume simple uniform hashing: each key independently hashes to each slot with probability 1/10. The probability that slot 0 is still empty after all insertions is ______ (rounded off to two decimal places).',
            'answer': ['0.34', '0.36'],
            'solution': '''Slot 0 stays empty iff **every** key misses it. Each key misses slot 0 with probability 1 − 1/10 = 0.9, independently, so

P(slot 0 empty) = 0.9^{10} ≈ 0.3487 ≈ **0.35**.

Consequences:

- The expected number of empty slots is 10 × 0.3487 ≈ 3.49 — even though n = m (load factor α = 1), about a third of the table is unused, so some chains must be longer than 1.
- For large m with n = m this tends to 1/e ≈ 0.368.

**Trap:** computing 1 − 10·(1/10) = 0 (union bound misuse), or 1/10 (the chance a *single* key hits slot 0).''',
            'verify': '''
p = 0.9 ** 10
assert float(ANSWER[0]) <= round(p, 2) <= float(ANSWER[1])
import random
random.seed(3)
emp = sum(all(random.randrange(10) != 0 for _ in range(10)) for _ in range(20000)) / 20000
assert abs(emp - p) < 0.02
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Expected number of collisions',
            'text': 'Twenty distinct keys are hashed into a table of 50 slots under simple uniform hashing. A *collision pair* is an unordered pair of distinct keys that hash to the same slot. The expected number of collision pairs is ______ (rounded off to two decimal places).',
            'answer': ['3.79', '3.81'],
            'solution': '''Use **linearity of expectation** with an indicator for every pair {x, y}:

- P(h(x) = h(y)) = 1/m = 1/50 for each pair (whatever slot x picks, y must match it).
- Number of pairs = C(20, 2) = 190.

E[collision pairs] = 190 × 1/50 = **3.80**.

Note that linearity holds even though the indicators are **not** independent. This is the birthday-paradox calculation: with n keys and m slots, collisions become likely once C(n, 2) ≈ m, i.e. n ≈ √(2m) = 10 here.

**Trap:** using n/m = 0.4 (the load factor) or n²/m = 8 (ordered pairs, counting each pair twice and including a key with itself).''',
            'verify': '''
from math import comb
e = comb(20, 2) / 50
assert float(ANSWER[0]) <= e <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Chaining — average successful search cost',
            'text': 'The hash table below (size 7, h(k) = k mod 7, separate chaining) stores 9 keys; each chain is searched from its head. Each stored key is equally likely to be searched for. The expected number of **key comparisons** in a successful search is',
            'diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: [21, 35],
                        2: [9],
                        3: [17, 31, 45, 10],
                        5: [12, 26],
                    },
                    'caption': 'Chains listed head first',
                },
            ],
            'options': ['9/7', '2', '17/9', '13/9'],
            'answer': 'C',
            'solution': '''Finding the key in position j of its chain (1-based) costs j comparisons. Average over all 9 stored keys.

- slot 0: 21 → 1, 35 → 2 (sum 3)
- slot 2: 9 → 1 (sum 1)
- slot 3: 17, 31, 45, 10 → 1 + 2 + 3 + 4 (sum 10)
- slot 5: 12 → 1, 26 → 2 (sum 3)

Total = 17 comparisons over 9 keys → **17/9 ≈ 1.89**.

- (A) 9/7 = α is the expected cost of an **unsuccessful** search (comparisons only) when the home slot is uniform over all 7 slots.
- (B) 2 is a guess from the textbook estimate 1 + α/2 ≈ 1.64 — such formulas give *expectations over random tables*, not the exact cost for this particular table.
- (D) 13/9 forgets that the 4-chain costs 10, not 6.

**Tip:** the one long chain at slot 3 contributes 10 of the 17 comparisons — uneven chains hurt more than the load factor suggests.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

T = {0: [21, 35], 2: [9], 3: [17, 31, 45, 10], 5: [12, 26]}
assert all(k % 7 == s for s, ch in T.items() for k in ch)
from fractions import Fraction
tot = sum(i + 1 for ch in T.values() for i in range(len(ch)))
n = sum(len(ch) for ch in T.values())
assert Fraction(tot, n) == Fraction(17, 9) and ANSWER == "A"
assert Fraction(sum(len(T.get(s, [])) for s in range(7)), 7) == Fraction(9, 7)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — hashability',
            'text': 'Which of the following statements about Python 3 is/are TRUE?',
            'options': [
                "After `d = {(1, 2): 'x'}`, the expression `(2, 1) in d` evaluates to `True`",
                'Evaluating `hash((1, [2]))` raises a `TypeError`',
                "`len({0, 0.0, False, ''})` evaluates to 2",
                'Evaluating `{[1, 2]: 3}` raises a `TypeError`',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Only hashable objects can be dict keys or set members. Lists are mutable and unhashable; a tuple is hashable only if **all** its elements are.

- (A) tuples are ordered: (2, 1) ≠ (1, 2). **False.**
- (B) hashing a tuple hashes its elements; the inner list fails. **True.**
- (C) 0, 0.0 and False are equal with equal hashes → one element; '' is different → size 2. **True.**
- (D) a list as a key → `TypeError: unhashable type: 'list'`. **True.**

**Trap:** (B) — a tuple *looks* immutable but is only as hashable as its contents. **Tip:** for unordered pairs use `frozenset`.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def raises(f):
    try:
        f(); return False
    except TypeError:
        return True
truth = [raises(lambda: {[1, 2]: 3}), raises(lambda: hash((1, [2]))),
         len({0, 0.0, False, ''}) == 2, (2, 1) in {(1, 2): 'x'}]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — bisect boundaries',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from bisect import bisect_left, bisect_right
a = [1, 3, 3, 3, 5, 8, 8, 10]
print(bisect_right(a, 3) - bisect_left(a, 3),
      bisect_left(a, 6), bisect_right(a, 8))''',
            'options': ['`3 5 7`', '`2 4 6`', '`3 4 7`', '`3 5 6`'],
            'answer': 'A',
            'solution': '''`bisect_left(a, x)` returns the first index i with a[i] ≥ x; `bisect_right(a, x)` returns the first index with a[i] > x. Both use binary search: Θ(log n).

- `bisect_left(a, 3)` = 1, `bisect_right(a, 3)` = 4 → difference **3** = number of 3s.
- `bisect_left(a, 6)`: 6 is absent; the first element ≥ 6 is 8 at index **5** (the insertion point).
- `bisect_right(a, 8)`: the first element > 8 is 10 at index **7**.

Output **3 5 7**.

- (B) uses last-occurrence indices (bisect_right − 1) everywhere.
- (C) gives index 4 for 6 — that is where 5 lives; 6 goes *after* 5.
- (D) confuses bisect_right(a, 8) with bisect_left(a, 8) + 1.

**Tip:** `bisect_right(a, x) − bisect_left(a, x)` counts occurrences of x in O(log n).''',
            'verify': "assert OUTPUT.strip() == '3 5 7' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation depth',
            'text': 'The postfix expression `2 3 4 * + 5 6 7 * + *` is evaluated with a stack (operands are pushed; an operator pops two operands and pushes the result). The maximum number of elements on the stack at any moment is ______.',
            'answer': '4',
            'solution': '''Track the stack size after each token (operand: +1, binary operator: −2 then +1 = −1):

- 2 → 1, 3 → 2, 4 → 3, `*` → 2 (3·4 = 12), `+` → 1 (2 + 12 = 14)
- 5 → 2, 6 → 3, 7 → **4**, `*` → 3 (42), `+` → 2 (47), `*` → 1 (14 · 47 = 658)

Maximum depth = **4**, reached with [14, 5, 6, 7] on the stack. The expression's value is 658 = (2 + 3·4)(5 + 6·7).

**Trap:** the depth is not the number of operands in a sub-expression; the earlier result 14 is still on the stack while 5, 6, 7 are pushed. **Tip:** max depth = maximum prefix sum of the ±1 sequence.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [14, 5, 6, 7],
                    'label': 'peak (depth 4)',
                },
            ],
            'verify': '''
st = []; mx = 0
for t in "2 3 4 * + 5 6 7 * + *".split():
    if t.isdigit(): st.append(int(t))
    else:
        b, a = st.pop(), st.pop(); st.append(a * b if t == "*" else a + b)
    mx = max(mx, len(st))
assert mx == int(ANSWER) and st == [658]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — linked-list pointer surgery',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class N:
    def __init__(s, v, nx=None):
        s.v, s.nx = v, nx

h = None
for v in [3, 1, 4, 1, 5]:
    h = N(v, h)
p = h
while p.nx and p.nx.nx:
    p.nx = p.nx.nx
    p = p.nx
out = []
while h:
    out.append(h.v)
    h = h.nx
print(out)''',
            'options': ['`[3, 4, 5]`', '`[5, 4, 3]`', '`[5, 1, 1]`', '`[5, 4, 1, 3]`'],
            'answer': 'B',
            'solution': '''`h = N(v, h)` inserts at the **head**, so the list is built in reverse: 5 → 1 → 4 → 1 → 3.

The loop removes every second node:

- p = 5: p.nx (1) and p.nx.nx (4) exist → 5.nx = 4; p = 4.
- p = 4: p.nx (1) and p.nx.nx (3) exist → 4.nx = 3; p = 3.
- p = 3: p.nx is None → stop.

Remaining list: 5 → 4 → 3 → output **[5, 4, 3]**.

- (A) forgets that head insertion reverses the input.
- (C) keeps the nodes at odd positions instead of deleting them.
- (D) stops after one deletion.

**Tip:** the guard `p.nx and p.nx.nx` relies on short-circuit evaluation — `p.nx.nx` is never evaluated when `p.nx` is None.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [5, 4, 3],
                    'head': 'h',
                    'caption': 'After deleting alternate nodes',
                },
            ],
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[5, 4, 3]' and ANSWER == 'A'",
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bubble sort with early termination',
            'text': 'Bubble sort with an early-exit flag (stop after the first pass that makes no swap; pass p compares adjacent pairs in A[0..n−p]) is applied to [2, 3, 9, 1, 4, 5, 8]. The number of passes executed (including the final swap-free pass) and the total number of swaps are, respectively,',
            'options': ['4 and 7', '3 and 6', '4 and 6', '6 and 6'],
            'answer': 'C',
            'solution': '''Each bubble pass moves the largest remaining element to the end, but a small element moves left by only **one** position per pass. The 1 at index 3 needs 3 passes to reach index 0.

- Pass 1: 9 bubbles to the end (swaps 9↔1, 9↔4, 9↔5, 9↔8 = 4) → [2, 3, 1, 4, 5, 8, 9]
- Pass 2: 3↔1 (1 swap) → [2, 1, 3, 4, 5, 8, 9]
- Pass 3: 2↔1 (1 swap) → [1, 2, 3, 4, 5, 8, 9]
- Pass 4: no swaps → stop

Passes = **4**, swaps = **6** (= number of inversions: 9 precedes 1, 4, 5, 8; 2 and 3 precede 1).

- (A) miscounts inversions.
- (B) forgets the verifying pass.
- (D) uses n − 1 = 6 passes, ignoring the early exit.

**Tip:** with the flag, passes = 1 + max over elements of (how far left it must move).''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

A = [2, 3, 9, 1, 4, 5, 8]; passes = sw = 0
while True:
    passes += 1; s = False
    for j in range(len(A) - passes):
        if A[j] > A[j + 1]:
            A[j], A[j + 1] = A[j + 1], A[j]; sw += 1; s = True
    if not s: break
assert (passes, sw) == (4, 6) and ANSWER == "A"
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Adjacency matrix — reading graph properties',
            'text': 'An undirected simple graph G on vertices a, b, c, d, e has the adjacency matrix A shown. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Adjacency matrix A',
                    'row_labels': ['a', 'b', 'c', 'd', 'e'],
                    'col_labels': ['a', 'b', 'c', 'd', 'e'],
                    'rows': [
                        [0, 1, 1, 0, 0],
                        [1, 0, 1, 1, 0],
                        [1, 1, 0, 0, 1],
                        [0, 1, 0, 0, 1],
                        [0, 0, 1, 1, 0],
                    ],
                },
            ],
            'options': [
                'G is bipartite',
                'The (a, d) entry of A² is 2',
                'G contains a cycle of length 5',
                'The trace (sum of diagonal entries) of A² is 12',
            ],
            'answer': ['C', 'D'],
            'solution': '''Edges: a–b, a–c, b–c, b–d, c–e, d–e (6 edges). (A²)[u][v] counts walks of length 2 from u to v, i.e. common neighbours.

- (A) a, b, c form a triangle (odd cycle). **False.**
- (B) N(a) = {b, c}, N(d) = {b, e}; common neighbour only b → entry 1. **False.**
- (C) a–b–d–e–c–a uses edges ab, bd, de, ec, ca — all present. **True.**
- (D) (A²)[v][v] = deg(v), so trace(A²) = Σ deg = 2|E| = 12. **True.**

**Tip:** trace(A³) = 6 × (number of triangles); here it is 6, confirming exactly one triangle.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A = [[0,1,1,0,0],[1,0,1,1,0],[1,1,0,0,1],[0,1,0,0,1],[0,0,1,1,0]]
n = 5
A2 = [[sum(A[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
A3 = [[sum(A2[i][k] * A[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
import itertools
def bip():
    for cols in itertools.product([0, 1], repeat=n):
        if all(cols[i] != cols[j] for i in range(n) for j in range(n) if A[i][j]): return True
    return False
c5 = any(all(A[p[i]][p[(i + 1) % 5]] for i in range(5)) for p in itertools.permutations(range(5)))
truth = [bip(), sum(A2[i][i] for i in range(n)) == 12, A2[0][3] == 2, c5]
assert sum(A3[i][i] for i in range(n)) == 6
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Linear probing — reconstructing insertion order',
            'text': 'Six distinct keys were inserted, in some unknown order, into an initially empty hash table of size 10 using h(k) = k mod 10 and linear probing (step +1). No deletions occurred. The final table is shown below. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        1: 61,
                        2: 31,
                        3: 72,
                        4: 13,
                        5: 24,
                        6: 91,
                    },
                    'caption': 'Final table',
                },
            ],
            'options': [
                '61 was inserted before 31',
                '24 could have been inserted before 72',
                '72 was inserted before 13',
                'Exactly one insertion order produces this table',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''A key stored at distance d from its home slot proves that, when it was inserted, **all** of slots home … home + d − 1 were already occupied.

Homes: 61→1, 31→1, 72→2, 13→3, 24→4, 91→1.

- 61 is at its home 1 — no constraint from itself.
- 31 (home 1) is at 2 → slot 1 (61) was full: **61 before 31**.
- 72 (home 2) is at 3 → slot 2 (31) was full: **31 before 72**.
- 13 (home 3) is at 4 → slot 3 (72) was full: **72 before 13**.
- 24 (home 4) is at 5 → slot 4 (13) was full: **13 before 24**.
- 91 (home 1) is at 6 → slots 1–5 all full: **91 last**.

The constraints form a chain 61 < 31 < 72 < 13 < 24 < 91, so the order is forced.

- (A) **True.**
- (B) 24 needs 13 already in slot 4, and 13 needs 72 → **False.**
- (C) **True.**
- (D) the chain is total → exactly **1** order. **True.**

**Trap:** assuming the 'probe-chain' constraint applies only to keys with the same home slot; with linear probing a cluster is shared by all homes inside it (primary clustering).''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
fin = {1: 61, 2: 31, 3: 72, 4: 13, 5: 24, 6: 91}
good = []
for perm in itertools.permutations(fin.values()):
    T = [None] * 10
    for k in perm:
        i = k % 10
        while T[i] is not None: i = (i + 1) % 10
        T[i] = k
    if all(T[s] == v for s, v in fin.items()): good.append(perm)
pos = lambda o, k: o.index(k)
truth = [all(pos(o, 61) < pos(o, 31) for o in good), all(pos(o, 72) < pos(o, 13) for o in good),
         any(pos(o, 24) < pos(o, 72) for o in good), len(good) == 1]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linear probing — expected unsuccessful search cost',
            'text': 'The hash table below has 10 slots and uses linear probing (step +1, wrapping from 9 to 0). A search for a key **not** in the table starts at a home slot that is equally likely to be any of the 10 slots, and probes until it reaches an empty slot; every slot inspected (including the final empty one) counts as one probe. The expected number of probes is ______ (rounded off to two decimal places).',
            'diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        0: 40,
                        1: 21,
                        2: 30,
                        3: 12,
                        5: 55,
                        6: 15,
                        9: 19,
                    },
                },
            ],
            'answer': ['2.79', '2.81'],
            'solution': '''An unsuccessful search from home h walks to the end of the cluster containing h. Occupied slots form clusters {9, 0, 1, 2, 3} (wrapping) and {5, 6}; empty slots are 4, 7, 8.

Probes by home slot:

- h = 9: 9, 0, 1, 2, 3 full, 4 empty → 6
- h = 0 → 5, h = 1 → 4, h = 2 → 3, h = 3 → 2
- h = 4 → 1 (empty immediately)
- h = 5 → 3, h = 6 → 2
- h = 7 → 1, h = 8 → 1

Sum = 6 + 5 + 4 + 3 + 2 + 1 + 3 + 2 + 1 + 1 = 28 → expected = 28/10 = **2.80**.

Shortcut: a cluster of length L contributes 2 + 3 + … + (L + 1) = L(L + 3)/2, and each empty slot contributes 1: 5·8/2 + 2·5/2 + 3 = 20 + 5 + 3 = 28.

**Trap:** forgetting the wrap-around (treating slot 9 as costing 2) gives 24/10. **Insight:** the long cluster makes the cost grow roughly with the *square* of cluster length — the essence of primary clustering. For comparison, uniform hashing at α = 0.7 predicts 1/(1 − α) ≈ 3.33.''',
            'verify': '''
occ = {0, 1, 2, 3, 5, 6, 9}; tot = 0
for h in range(10):
    i, c = h, 1
    while i in occ: i = (i + 1) % 10; c += 1
    tot += c
assert float(ANSWER[0]) <= tot / 10 <= float(ANSWER[1])
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Double hashing — probe counting',
            'text': 'Keys 27, 53, 40, 66, 14, 79, 183 are inserted in that order into an initially empty table of size 13 using double hashing: probe i (i = 0, 1, 2, …) examines slot (h₁(k) + i·h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). Each slot examined counts as one probe (including the slot finally used). The total number of probes for all seven insertions is ______.',
            'answer': '15',
            'solution': '''Every key here has h₁ = 1 (27, 53, 40, 66, 14, 79, 183 are all ≡ 1 mod 13), yet double hashing sends them along **different** probe sequences because h₂ differs — this is how double hashing avoids secondary clustering.

- 27: h₂ = 6; slot 1 empty → 1 probe
- 53: h₂ = 10; 1 full → 11 → 2 probes
- 40: h₂ = 8; 1 full → 9 → 2 probes
- 66: h₂ = 1; 1 full → 2 → 2 probes
- 14: h₂ = 4; 1 full → 5 → 2 probes
- 79: h₂ = 3; 1 full → 4 → 2 probes
- 183: h₂ = 1 + 7 = 8; 1 full → 9 full (40) → 17 mod 13 = 4 full (79) → 25 mod 13 = **12** → 4 probes

Total = 1 + 2·5 + 4 = **15**.

**Trap:** computing h₂ as k mod 11 (forgetting the +1, which guarantees h₂ ≠ 0). **Tip:** since 13 is prime, every h₂ ∈ [1, 12] generates a full permutation of the slots.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        1: 27,
                        2: 66,
                        4: 79,
                        5: 14,
                        9: 40,
                        11: 53,
                        12: 183,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 13; tot = 0
for k in [27, 53, 40, 66, 14, 79, 183]:
    h1, h2, i = k % 13, 1 + k % 11, 0
    while T[(h1 + i * h2) % 13] is not None: i += 1
    T[(h1 + i * h2) % 13] = k; tot += i + 1
assert tot == int(ANSWER) and T[12] == 183
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Probability of no collision',
            'text': 'Three distinct keys are inserted into a hash table with 7 slots. Each key independently hashes to each slot with probability 1/7. The probability that no two keys hash to the same slot is',
            'options': ['1/7', '36/49', '6/7', '30/49'],
            'answer': 'D',
            'solution': '''Count favourable hash assignments: the first key may go anywhere (7 ways), the second must avoid it (6), the third must avoid both (5).

P(no collision) = (7 · 6 · 5) / 7³ = 210/343 = **30/49 ≈ 0.612**.

Equivalently, (6/7)·(5/7) = 30/49.

- (A) 1/7 is the probability that a **particular** pair collides.
- (B) 36/49 = (6/7)² assumes the third key only has to avoid one slot.
- (C) 6/7 accounts only for the second key.

So with only 3 keys and 7 slots there is already a 19/49 ≈ 39% chance of at least one collision — the birthday paradox in miniature.

**Tip:** P(no collision) = ∏_{i=0}^{n−1} (1 − i/m) ≈ e^{−n(n−1)/(2m)} = e^{−3/7} ≈ 0.65.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

import itertools
from fractions import Fraction
good = sum(len(set(t)) == 3 for t in itertools.product(range(7), repeat=3))
assert Fraction(good, 343) == Fraction(30, 49) and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linear probing with deletion (tombstones)',
            'text': '''A hash table of size 10 uses h(k) = k mod 10 and linear probing. Deletion replaces the key by a **tombstone**: searches continue past a tombstone, while an insertion places the new key in the first tombstone or empty slot it meets. Starting from an empty table, perform:

insert 15, 25, 35, 16, 45; delete 25; delete 16; insert 55.

Then search for 45 (present) and for 65 (absent). Counting every slot inspected (including the slot where the search ends), the total number of probes made by these two searches is ______.''',
            'answer': '11',
            'solution': '''Tombstones keep probe chains intact: emptying a slot outright would make later keys of the cluster unreachable.

Build the table:

- 15 → 5; 25 → 6; 35 → 7; 16 → 6, 7 full → 8; 45 → 5, 6, 7, 8 full → 9
- delete 25 → slot 6 = tombstone; delete 16 → slot 8 = tombstone
- insert 55: home 5 full, slot 6 is a tombstone → 55 goes to **6**

Final: 5:15, 6:55, 7:35, 8:✝, 9:45, others empty.

- search 45: 5 (15), 6 (55), 7 (35), 8 (✝, keep going), 9 (found) → **5** probes
- search 65: 5, 6, 7, 8 (✝), 9, 0 (empty → stop) → **6** probes

Total = 5 + 6 = **11**.

**Trap:** stopping at the tombstone in slot 8 would wrongly report 45 as absent (4 probes) — exactly the bug tombstones exist to prevent. **Note:** tombstones lengthen unsuccessful searches until the table is rebuilt.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        5: 15,
                        6: 55,
                        7: 35,
                        8: '✝',
                        9: 45,
                    },
                    'caption': 'Table before the two searches (✝ = tombstone)',
                },
            ],
            'verify': '''
T = [None] * 10; TOMB = "T"
def ins(k):
    i = k % 10
    while T[i] is not None and T[i] != TOMB: i = (i + 1) % 10
    T[i] = k
def delete(k):
    i = k % 10
    while T[i] != k: i = (i + 1) % 10
    T[i] = TOMB
def search(k):
    i, c = k % 10, 1
    while T[i] is not None:
        if T[i] == k: return c
        i = (i + 1) % 10; c += 1
    return c
for k in (15, 25, 35, 16, 45): ins(k)
delete(25); delete(16); ins(55)
assert T[6] == 55 and search(45) == 5 and search(65) == 6
assert search(45) + search(65) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — __eq__ and __hash__ in sets',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, o):
        return self.x == o.x
    def __hash__(self):
        return hash(self.x % 3)

s = {P(1, 2), P(4, 2), P(1, 5), P(7, 0)}
t = {p.y for p in s}
print(len(s), sorted(t))''',
            'options': ['`4 [0, 2, 5]`', '`3 [0, 2]`', '`1 [2]`', '`3 [0, 2, 5]`'],
            'answer': 'B',
            'solution': '''A set first compares hashes, then uses `==` to decide whether an element is already present. Here every object has hash(x % 3) = hash(1) (x = 1, 4, 1, 7 are all ≡ 1 mod 3), so all four land in the same bucket — but `__eq__` compares only x.

- add P(1, 2): new
- add P(4, 2): same hash, 4 ≠ 1 → new
- add P(1, 5): same hash and x equal to P(1, 2) → **duplicate; not added** (the first object, with y = 2, stays)
- add P(7, 0): new

len(s) = 3, and the stored y-values are {2, 2, 0} → set {0, 2}. Output **3 [0, 2]**.

- (A) assumes objects are distinct by identity (ignores the custom `__eq__`).
- (C) assumes equal hashes imply equal elements — a hash collision is not equality.
- (D) assumes the later P(1, 5) replaces P(1, 2); a set keeps the existing element.

**Tip:** a constant-ish hash is *correct* but degrades the set to a linear scan.''',
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '3 [0, 2]' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra — single-source distances',
            'text': "Dijkstra's algorithm is run from vertex P on the weighted undirected graph below. The sum of the shortest-path distances from P to all the other five vertices is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q', 4],
                        ['P', 'R', 1],
                        ['R', 'Q', 2],
                        ['Q', 'S', 5],
                        ['R', 'S', 8],
                        ['R', 'T', 10],
                        ['S', 'T', 2],
                        ['S', 'U', 6],
                        ['T', 'U', 3],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [2, 2],
                        'R': [2, 0],
                        'S': [4, 2],
                        'T': [4, 0],
                        'U': [6, 1],
                    },
                },
            ],
            'answer': '35',
            'solution': '''Dijkstra repeatedly finalises the unvisited vertex with the smallest tentative distance.

- Extract P (0): Q = 4, R = 1
- Extract R (1): Q = min(4, 1 + 2) = 3; S = 9; T = 11
- Extract Q (3): S = min(9, 3 + 5) = 8
- Extract S (8): T = min(11, 8 + 2) = 10; U = 14
- Extract T (10): U = min(14, 10 + 3) = 13
- Extract U (13)

Distances: Q 3, R 1, S 8, T 10, U 13 → sum = **35**.

Shortest-path tree: P–R, R–Q, Q–S, S–T, T–U (a single path P–R–Q–S–T–U).

**Trap:** taking the direct edges (P–Q = 4, R–T = 10 + 1 = 11, S–U = 8 + 6 = 14) without relaxing via cheaper detours gives 4 + 1 + 8 + 11 + 14 = 38.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q', 4],
                        ['P', 'R', 1],
                        ['R', 'Q', 2],
                        ['Q', 'S', 5],
                        ['R', 'S', 8],
                        ['R', 'T', 10],
                        ['S', 'T', 2],
                        ['S', 'U', 6],
                        ['T', 'U', 3],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [2, 2],
                        'R': [2, 0],
                        'S': [4, 2],
                        'T': [4, 0],
                        'U': [6, 1],
                    },
                    'highlight_edges': [
                        ['P', 'R'],
                        ['R', 'Q'],
                        ['Q', 'S'],
                        ['S', 'T'],
                        ['T', 'U'],
                    ],
                    'caption': 'Shortest-path tree from P',
                },
            ],
            'verify': '''
import heapq
E = [("P","Q",4),("P","R",1),("R","Q",2),("Q","S",5),("R","S",8),("R","T",10),("S","T",2),("S","U",6),("T","U",3)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: float("inf") for v in G}; d["P"] = 0; pq = [(0, "P")]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d.values()) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merge sort — comparison counts',
            'text': 'Top-down merge sort (split [lo, hi) at mid = (lo + hi) // 2, sort the halves recursively, merge with the standard two-pointer merge; a comparison is one key-vs-key test) is applied to [6, 2, 9, 4, 7, 1, 8, 3]. Which of the following statements is/are TRUE?',
            'options': [
                'Just before the final merge, the two sorted halves are [2, 4, 6, 9] and [1, 3, 7, 8]',
                'The final merge makes exactly 6 comparisons',
                'No permutation of 8 distinct keys makes this algorithm perform more than 17 comparisons',
                'The total number of comparisons is 17',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Merging runs of sizes p and q costs at most p + q − 1 comparisons (the maximum is reached when the runs interleave until the very end).

- Level 1: [6]+[2], [9]+[4], [7]+[1], [8]+[3] → 1 each = 4
- Level 2: [2 6]+[4 9]: 2|4, 6|4, 6|9 → 3; [1 7]+[3 8]: 1|3, 7|3, 7|8 → 3 → 6
- Level 3: [2 4 6 9]+[1 3 7 8]: 1, 2, 3, 4, 6, 7, then 9 vs 8 → 7 comparisons

Total = 4 + 6 + 7 = **17**.

- (A) **True** — the left half [6, 2, 9, 4] sorts to [2, 4, 6, 9], the right to [1, 3, 7, 8].
- (B) the final merge makes **7**. **False.**
- (C) every merge here already hit its maximum p + q − 1, so 17 is the worst case for n = 8 (formula n⌈log₂ n⌉ − 2^{⌈log₂ n⌉} + 1 = 24 − 8 + 1 = 17). **True.**
- (D) **True.**

**Tip:** the best case for n = 8 is 12 comparisons (each merge stops after min(p, q) comparisons, e.g. on sorted input).''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def ms(a, c):
    if len(a) <= 1: return a
    m = len(a) // 2; L = ms(a[:m], c); R = ms(a[m:], c); i = j = 0; r = []; k = 0
    while i < len(L) and j < len(R):
        k += 1
        if L[i] <= R[j]: r.append(L[i]); i += 1
        else: r.append(R[j]); j += 1
    c.append(k)
    return r + L[i:] + R[j:]
c = []; ms([6, 2, 9, 4, 7, 1, 8, 3], c)
worst = 0
for p in itertools.permutations(range(8)):
    cc = []; ms(list(p), cc); worst = max(worst, sum(cc))
truth = [sum(c) == 17, c[-1] == 6, worst == 17,
         sorted([6, 2, 9, 4]) == [2, 4, 6, 9] and sorted([7, 1, 8, 3]) == [1, 3, 7, 8]]
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Heaps — counting distinct max-heaps',
            'text': 'How many distinct binary max-heaps (stored as arrays, i.e. complete binary trees) can be built using all of the keys 1, 2, 3, 4, 5, 6 exactly once?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': ['6', '?', '?', '?', '?', '?'],
                    'caption': 'Shape of every 6-node heap',
                },
            ],
            'options': ['40', '16', '32', '20'],
            'answer': 'D',
            'solution': '''The shape of a 6-node complete tree is fixed: the root's left subtree has 3 nodes (indices 1, 3, 4) and its right subtree has 2 nodes (indices 2, 5).

- The root must be the maximum, 6.
- Choose which 3 of the remaining 5 keys go to the left subtree: C(5, 3) = 10 ways.
- A 3-node heap (root + 2 children) on fixed keys: the max is the root, the other two can be swapped → H(3) = 2.
- A 2-node heap: H(2) = 1.

H(6) = C(5, 3) · H(3) · H(2) = 10 · 2 · 1 = **20**.

- (A) 40 uses C(5, 2)·2·2, wrongly giving the 2-node subtree two arrangements.
- (B) 16 = 2⁴ — a guess treating every internal node as a free left/right choice.
- (C) 32 ignores that the 2-node right subtree has only one heap arrangement.

**Tip:** the recurrence H(n) = C(n − 1, L) · H(L) · H(R) gives 1, 1, 2, 3, 8, 20, 80 for n = 1 … 7.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

import itertools
cnt = sum(all(p[(i - 1) // 2] > p[i] for i in range(1, 6)) for p in itertools.permutations(range(1, 7)))
assert cnt == 20 and ANSWER == "A"
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Open addressing — expected probe counts',
            'text': "An open-addressing hash table has load factor α = 0.75. Use the standard asymptotic estimates (uniform hashing for (A)–(B), Knuth's linear-probing estimates for (C)). Which of the following statements is/are TRUE?",
            'options': [
                'Under linear probing, the expected number of probes in an unsuccessful search is about 8.5',
                'Under uniform hashing, the expected number of probes in an unsuccessful search is at most 4',
                'Under uniform hashing, the expected number of probes in a successful search is about 1.85',
                'Separate chaining could not be used at this load factor, since chaining requires α ≤ 0.5',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Standard results for open addressing (α = n/m < 1):

- Uniform hashing, unsuccessful: ≤ 1/(1 − α) = 1/0.25 = **4**. (B) **True.**
- Uniform hashing, successful: ≤ (1/α) ln(1/(1 − α)) = (4/3) ln 4 ≈ (4/3)(1.386) ≈ **1.85**. (C) **True.**
- Linear probing (Knuth): unsuccessful ≈ ½(1 + 1/(1 − α)²) = ½(1 + 16) = **8.5**; successful ≈ ½(1 + 1/(1 − α)) = 2.5. (A) **True.**
- (D) Chaining works for **any** α (even α > 1); the expected search cost is Θ(1 + α). **False.**

Comparing (B) with (A): at the same load factor, primary clustering makes linear probing's unsuccessful search more than twice as expensive as ideal uniform hashing.

**Trap:** mixing up the successful and unsuccessful formulas — successful searches are always cheaper because they stop at the key, on average part-way along the probe sequence.''',
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import math, random
a = 0.75
uns = 1 / (1 - a); suc = (1 / a) * math.log(1 / (1 - a)); lin = 0.5 * (1 + 1 / (1 - a) ** 2)
assert uns == 4 and abs(suc - 1.85) < 0.01 and lin == 8.5
random.seed(5)
m = 2000; n = int(a * m)
T = [False] * m
for _ in range(n):
    i = random.randrange(m)
    while T[i]: i = (i + 1) % m
    T[i] = True
avg = sum(next(c for c in range(1, m + 1) if not T[(h + c - 1) % m]) for h in range(m)) / m
assert 6 < avg < 11
assert sorted(ANSWER) == ["A", "B", "C"]
''',
        },
    ],
}
