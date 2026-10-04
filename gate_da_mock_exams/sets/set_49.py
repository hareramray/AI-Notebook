# Set 49 — Challenge Mock — Paper 4
SET = {
    'number': 49,
    'title': 'Challenge Mock — Paper 4',
    'difficulty': 'Hard',
    'focus': 'hardest, multi-concept, trap-heavy 2-mark questions',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — list multiplication aliasing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''grid = [[0] * 3] * 3
grid[0][1] = 5
row = grid[1][:]
row[2] = 7
print(grid[2], row, grid[0] is grid[2], row == grid[1])''',
            'options': [
                '`[0, 0, 0] [0, 5, 7] False False`',
                '`[0, 5, 0] [0, 5, 7] True False`',
                '`[0, 5, 0] [0, 5, 7] True True`',
                '`[0, 5, 0] [0, 0, 7] True False`',
            ],
            'answer': 'B',
            'solution': '''`[[0] * 3] * 3` builds **one** inner list and an outer list holding three references to it. `[0] * 3` itself is fine, because its elements are immutable ints.

- `grid[0][1] = 5` mutates the single shared row → every ‘row’ reads [0, 5, 0].
- `grid[1][:]` is a **shallow copy** of that row → a new list [0, 5, 0]; `row[2] = 7` changes only the copy → row = [0, 5, 7].
- `grid[0] is grid[2]` → True (same object).
- `row == grid[1]` compares values: [0, 5, 7] vs [0, 5, 0] → False.

Output `[0, 5, 0] [0, 5, 7] True False` → option (B).

- (A) assumes three independent rows.
- (C) assumes the slice is an alias (it is a copy).
- (D) assumes the copy was taken before the assignment of 5 reached row 1.

**Fix:** `grid = [[0] * 3 for _ in range(3)]` creates three separate rows — the standard way to build a DP table or an adjacency matrix.''',
            'verify': "ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[0, 5, 0] [0, 5, 7] True False' and ANSWER == 'C'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — global vs nonlocal',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''x = 10
def outer():
    x = 1
    def inner():
        nonlocal x
        x += 2
        return x
    def other():
        global x
        x *= 3
        return x
    return inner() + other() + inner() + x

print(outer() + x)''',
            'answer': '73',
            'solution': '''There are two different variables named x: the **global** x (10) and the **local** x of `outer` (1). `nonlocal x` in `inner` binds to outer's x; `global x` in `other` binds to the module-level x.

Inside `outer`, the sum is evaluated left to right:

- `inner()` → outer's x = 1 + 2 = 3 → returns 3.
- `other()` → global x = 10 × 3 = 30 → returns 30.
- `inner()` → outer's x = 3 + 2 = 5 → returns 5.
- `x` (outer's local) → 5.
- outer() returns 3 + 30 + 5 + 5 = 43.

In `print(outer() + x)`, `outer()` is evaluated first (43) and **then** the global x is read — it is already 30. Result 43 + 30 = **73**.

**Traps:** using the stale global 10 (→ 53), or letting `other` modify outer's x (→ different sums). Python evaluates the operands of `+` strictly left to right, so the side effect inside `outer()` is visible to the right operand.''',
            'verify': 'assert int(OUTPUT) == int(ANSWER) == 73',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — prefix expression evaluation',
            'text': '''The prefix (Polish) expression below is evaluated with a stack by scanning from **right to left**. `^` is exponentiation and `/` is exact division.

− / 8 ^ 2 2 * + 4 2 3

The value of the expression is''',
            'options': ['2', '16', '−16', '17.5'],
            'answer': 'C',
            'solution': '''Scanning a prefix expression right to left, operands are pushed; for an operator the **first** popped value is the **left** operand (the opposite of postfix evaluation).

- 3, 2, 4 → stack (bottom→top) [3, 2, 4].
- `+` → pop 4 (left), 2 (right) → 6 → [3, 6].
- `*` → pop 6 (left), 3 (right) → 18 → [18].
- 2, 2 → [18, 2, 2]; `^` → 2² = 4 → [18, 4].
- 8 → [18, 4, 8]; `/` → pop 8 (left), 4 (right) → 2 → [18, 2].
- `−` → pop 2 (left), 18 (right) → 2 − 18 = **−16**.

Infix: (8 / 2²) − ((4 + 2) × 3) = 2 − 18 = −16 → option (C).

- (A) 2 is just the left operand 8 / 4.
- (B) 16 uses the postfix pop order for the final `−` (18 − 2).
- (D) 17.5 applies the postfix pop order to *every* operator: 4 / 8 = 0.5 and 18 − 0.5.

**Trap:** in prefix the operator's left operand is the one nearer to it, which ends up on **top** of the stack.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

import operator as op
F = {'+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '^': op.pow}
st = []
for t in reversed("- / 8 ^ 2 2 * + 4 2 3".split()):
    if t in F:
        a = st.pop(); b = st.pop(); st.append(F[t](a, b))
    else:
        st.append(int(t))
assert st == [-16] and ANSWER == 'A'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — reversing in groups of k',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class N:
    def __init__(self, v, nx=None):
        self.v, self.nx = v, nx

def rev_k(h, k):
    cur, cnt = h, 0
    while cur and cnt < k:
        cur, cnt = cur.nx, cnt + 1
    if cnt < k:
        return h
    prev, cur = rev_k(cur, k), h
    for _ in range(k):
        cur.nx, prev, cur = prev, cur, cur.nx
    return prev

h = None
for v in range(8, 0, -1):
    h = N(v, h)
h = rev_k(h, 3)
out = []
while h:
    out.append(h.v)
    h = h.nx
print(out)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8],
                    'head': 'h',
                    'caption': 'List built by the loop',
                },
            ],
            'options': [
                '`[3, 2, 1, 6, 5, 4, 7, 8]`',
                '`[3, 2, 1, 6, 5, 4, 8, 7]`',
                '`[8, 7, 6, 5, 4, 3, 2, 1]`',
                '`[1, 2, 3, 6, 5, 4, 7, 8]`',
            ],
            'answer': 'A',
            'solution': '''The loop builds 1 → 2 → … → 8 (each new node is put in front, from 8 down to 1).

`rev_k` first checks whether k = 3 nodes remain; if not, the group is returned unchanged. Otherwise it recursively processes the rest, and then reverses the current k nodes, pointing the first one at the processed remainder (`prev` starts as that remainder).

- Group 1, 2, 3 → becomes 3 → 2 → 1 → (rest).
- Group 4, 5, 6 → 6 → 5 → 4 → (rest).
- Remaining 7, 8: only 2 < 3 nodes → returned as is.

Output `[3, 2, 1, 6, 5, 4, 7, 8]` → option (A).

**The tuple assignment** `cur.nx, prev, cur = prev, cur, cur.nx` is safe: the right-hand side is evaluated completely first (old prev, old cur, old cur.nx), then the targets are assigned left to right, and `cur.nx` is assigned while `cur` still names the old node.

- (B) also reverses the short final group.
- (C) is a full reversal.
- (D) skips the first group.

**Trap:** reordering the targets as `cur, cur.nx, prev = …` would set `.nx` on the *new* cur — a classic bug.''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[3, 2, 1, 6, 5, 4, 7, 8]' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary trees — counting facts',
            'text': 'Which of the following statements is/are TRUE?',
            'options': [
                'A complete binary tree with 100 nodes has height 7 (height = edges on the longest root-to-leaf path)',
                'A binary tree with n nodes has exactly n + 1 empty (None) child pointers',
                'Every binary tree with 12 leaves has exactly 11 nodes with two children',
                'A full binary tree (every node has 0 or 2 children) with 20 leaves has exactly 39 nodes',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Let n₀, n₁, n₂ be the numbers of nodes with 0, 1, 2 children. Counting edges two ways: n − 1 = n₁ + 2n₂ and n = n₀ + n₁ + n₂ ⇒ **n₀ = n₂ + 1**.

- (A) **False.** A complete tree of height h has between 2^{h} and 2^{h+1} − 1 nodes; 2⁶ = 64 ≤ 100 ≤ 127, so the height is ⌊log₂ 100⌋ = **6**.
- (B) **True.** n nodes have 2n child pointers, and exactly n − 1 of them are used (one per non-root node), leaving 2n − (n − 1) = n + 1 empty.
- (C) **True.** n₂ = n₀ − 1 = 11 for *every* binary tree, regardless of n₁.
- (D) **True.** Full ⇒ n₁ = 0, so n₂ = 20 − 1 = 19 and n = 20 + 19 = 39.

Answer: (D), (C), (B).

**Trap:** (A) uses the node-count definition of height (7 levels); with edges it is 6.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import random, math
def rnd(n):
    if n == 0: return None
    k = random.randrange(n)
    return [0, rnd(k), rnd(n - 1 - k)]
def cnt(t):
    if t is None: return (0, 0, 0, 1)
    a = cnt(t[1]); b = cnt(t[2]); ch = (t[1] is not None) + (t[2] is not None)
    s = [a[i] + b[i] for i in range(4)]; s[ch] += 1
    return tuple(s)
for _ in range(300):
    n = random.randint(1, 40); c = cnt(rnd(n))
    assert c[0] == c[2] + 1 and c[3] == n + 1
assert 20 + 19 == 39 and math.floor(math.log2(100)) == 6
assert sorted(ANSWER) == ['A', 'B', 'D']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — probability of no collision',
            'text': 'Three distinct keys are inserted into a hash table with 8 slots. Assume each key independently hashes to each slot with probability 1/8. The probability that **no two** keys hash to the same slot is closest to',
            'options': ['0.670', '0.875', '0.344', '0.656'],
            'answer': 'D',
            'solution': '''Count favourable outcomes: the first key may go anywhere, the second must avoid one slot, the third must avoid two.

P(no collision) = (8/8) × (7/8) × (6/8) = 336 / 512 = 21/32 ≈ **0.656** → option (D).

- (A) 0.670 = (7/8)³ treats the three *pairs* of keys as independent events — they are not (if A≠B and B≠C, the chance that A≠C changes).
- (B) 0.875 = 7/8 is the answer for only **two** keys.
- (C) 0.344 = 1 − 0.656 is the probability of **at least one** collision.

This is the birthday problem in miniature: with m slots, collisions become likely after only about √(πm/2) keys — the reason why hash tables must resolve collisions rather than hope to avoid them.

**Tip:** the expected number of colliding pairs is C(3, 2)/8 = 0.375 — linearity works even though the pair events are dependent.''',
            'verify': '''
import itertools
tot = ok = 0
for s in itertools.product(range(8), repeat=3):
    tot += 1; ok += len(set(s)) == 3
p = ok / tot
opts = {'A': 0.670, 'B': 0.875, 'C': 0.344, 'D': 0.656}
assert min(opts, key=lambda k: abs(opts[k] - p)) == ANSWER and abs(p - 21 / 32) < 1e-12
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — average successful search',
            'text': 'A sorted array of n = 1023 distinct keys is searched with standard binary search (mid = (lo + hi) // 2; one three-way comparison per iteration). Each of the 1023 keys is equally likely to be the search key. The average number of comparisons for a **successful** search (rounded off to two decimal places) is ______.',
            'answer': ['9.00', '9.02'],
            'solution': '''For n = 2¹⁰ − 1 the binary-search decision tree is **perfect** with 10 levels: level d (d = 1 … 10) holds 2^{d−1} keys, each found with exactly d comparisons.

Total = ∑ d · 2^{d−1} for d = 1 … 10 = (10 − 1) · 2¹⁰ + 1 = 9 · 1024 + 1 = 9217.

(Identity: ∑_{d=1}^{k} d · 2^{d−1} = (k − 1) · 2^{k} + 1.)

Average = 9217 / 1023 ≈ **9.01**.

Note how close this is to the worst case (10): half of all keys sit on the bottom level, so the average is only about one comparison below the maximum, roughly log₂ n − 1.

**Trap:** answering log₂ 1023 ≈ 9.998, or (1 + 10)/2 = 5.5 by assuming every number of comparisons is equally likely.''',
            'verify': '''
A = list(range(1023)); tot = 0
for x in A:
    lo, hi, c = 0, 1022, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if A[m] == x: break
        if A[m] < x: lo = m + 1
        else: hi = m - 1
    tot += c
assert tot == 9217 and float(ANSWER[0]) <= tot / 1023 <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Sorting — stability of selection sort',
            'text': '''Records (key, tag) are sorted by key with selection sort: for i = 0, 1, …, the record with the smallest key in positions i … n−1 (the **first** such record if there are ties) is swapped into position i. The input is

(4,p) (2,q) (4,r) (1,s) (2,t) (3,u).

The sequence of tags after sorting is''',
            'options': ['s q t u p r', 's q t u r p', 's t q u r p', 's t q u p r'],
            'answer': 'B',
            'solution': '''Trace (only swaps shown):

- i = 0: smallest key 1 at (1,s), index 3 → swap with (4,p): (1,s) (2,q) (4,r) (4,p) (2,t) (3,u).
- i = 1: smallest key 2, first occurrence (2,q) at index 1 → no change.
- i = 2: smallest key 2 is (2,t) at index 4 → swap with (4,r): (1,s) (2,q) (2,t) (4,p) (4,r) (3,u).
- i = 3: smallest key 3 at index 5 → swap with (4,p): (1,s) (2,q) (2,t) (3,u) (4,r) (4,p).
- i = 4: smallest is (4,r) (first of the two 4s) → no change.

Tags: **s q t u r p** → option (B).

The two records with key 4 came out as r, p although the input had p before r: the long-distance swap at i = 0 threw (4,p) behind (4,r). Selection sort is **not stable**.

- (A) is the stable order (what insertion or merge sort would give).
- (C) and (D) also reorder the key-2 records, which never happens here.

**Trap:** concluding stability from the 2s (q before t is preserved) — one counter-example pair is enough to make a sort unstable.''',
            'verify': '''
a = [(4,'p'), (2,'q'), (4,'r'), (1,'s'), (2,'t'), (3,'u')]
for i in range(len(a)):
    m = i
    for j in range(i + 1, len(a)):
        if a[j][0] < a[m][0]: m = j
    a[i], a[m] = a[m], a[i]
opts = {'A': "s q t u p r", 'B': "s q t u r p", 'C': "s t q u r p", 'D': "s t q u p r"}
assert [k for k in opts if opts[k] == " ".join(t for _, t in a)] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graphs — bipartiteness',
            'text': 'The undirected graph G below is bipartite. Each option proposes adding **one** edge to G (the options are considered separately). After which of the following additions is the graph still bipartite?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'A'],
                        ['G', 'A'],
                        ['H', 'D'],
                    ],
                    'pos': {
                        'A': [1, 2],
                        'B': [2.5, 2.8],
                        'C': [4, 2],
                        'D': [4, 0.6],
                        'E': [2.5, -0.2],
                        'F': [1, 0.6],
                        'G': [-0.5, 2.6],
                        'H': [5.5, 0],
                    },
                },
            ],
            'options': ['Edge F–G', 'Edge A–C', 'Edge B–E', 'Edge G–H'],
            'answer': ['C', 'D'],
            'solution': '''A connected graph is bipartite iff a BFS/DFS 2-colouring never puts the same colour on both ends of an edge (equivalently, it has no odd cycle). Colour G from A:

- A: 0; B, F, G: 1 (neighbours of A); C, E: 0; D: 1; H (neighbour of D): 0.

An added edge keeps the graph bipartite iff its endpoints have **different** colours.

- (A) F–G: both 1 → triangle A-F-G → **not** bipartite.
- (B) A–C: both 0 → odd cycle A-B-C-A of length 3 → **not** bipartite.
- (C) B–E: colours 1 and 0 → **still bipartite** (it creates cycles B-C-D-E-B and B-A-F-E-B of length 4).
- (D) G–H: colours 1 and 0 → **still bipartite** (new cycle G-A-B-C-D-H-G has length 6).

Answer: (C), (D).

**Trap:** judging by the picture — B–E and A–C both look like chords of the hexagon, but B–E joins vertices at odd distance 3 (closing even cycles) while A–C joins vertices at even distance 2 (closing a triangle).''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from collections import deque
base = [("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),("F","A"),("G","A"),("H","D")]
def bip(E):
    adj = {}
    for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
    col = {}
    for s in adj:
        if s in col: continue
        col[s] = 0; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in col: col[v] = 1 - col[u]; q.append(v)
                elif col[v] == col[u]: return False
    return True
opts = {'A': ("B","E"), 'B': ("A","C"), 'C': ("G","H"), 'D': ("F","G")}
assert bip(base)
assert sorted(k for k in opts if bip(base + [opts[k]])) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Loop counting — harmonic sums',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''c = 0
n = 20
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        c += 1
print(c)''',
            'answer': '66',
            'solution': '''For a fixed i the inner loop visits j = i, 2i, 3i, … ≤ n, i.e. ⌊n/i⌋ values. So

c = ∑_{i=1}^{20} ⌊20/i⌋.

- i = 1 … 5: 20 + 10 + 6 + 5 + 4 = 45.
- i = 6: 3; i = 7 … 10: 2 each → 3 + 8 = 11.
- i = 11 … 20: 1 each → 10.

Total = 45 + 11 + 10 = **66**.

Equivalently, c counts pairs (i, j) with i | j, i.e. ∑_{j=1}^{20} d(j), the total number of divisors of 1 … 20.

**Complexity:** ∑ n/i = n · H_n ≈ n ln n, so the fragment is **Θ(n log n)** — the same harmonic-sum pattern as the sieve of Eratosthenes (which, skipping non-primes, is even Θ(n log log n)).

**Trap:** assuming two nested loops over 1 … n must be Θ(n²); the step size i makes the inner loop shrink like n/i.''',
            'verify': 'assert int(OUTPUT) == int(ANSWER) == sum(20 // i for i in range(1, 21))',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — sorted(): keys, case and stability',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''data = ["kiwi", "Fig", "apple", "date", "Banana", "fig"]
r1 = sorted(data, key=len)
r2 = sorted(data, key=str.lower)
r3 = sorted(sorted(data), key=len, reverse=True)
print(r1[:3], r2[:2], r3[2:5])''',
            'options': [
                "`['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']`",
                "`['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['kiwi', 'date', 'fig']`",
                "`['Fig', 'fig', 'date'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']`",
                "`['Fig', 'fig', 'kiwi'] ['Banana', 'Fig'] ['date', 'kiwi', 'Fig']`",
            ],
            'answer': 'A',
            'solution': '''Three facts decide everything: (1) `sorted` is **stable** — records with equal keys keep their relative input order; (2) default string order compares code points, so every uppercase letter precedes every lowercase letter; (3) `reverse=True` reverses the order of *keys* but still keeps equal-key records stable (it does **not** simply reverse the output list).

- r1 (by length): lengths kiwi 4, Fig 3, apple 5, date 4, Banana 6, fig 3. Length 3 in input order: Fig, fig; then length 4: kiwi, date → r1[:3] = ['Fig', 'fig', 'kiwi'].
- r2 (case-insensitive): apple, banana, date, fig, fig, kiwi → r2[:2] = ['apple', 'Banana'].
- r3: `sorted(data)` = ['Banana', 'Fig', 'apple', 'date', 'fig', 'kiwi'] (uppercase first). Then by length descending, ties kept in this order: Banana(6), apple(5), date(4), kiwi(4), Fig(3), fig(3) → r3[2:5] = ['date', 'kiwi', 'Fig'].

Output → option (A).

- (B) assumes `reverse=True` reverses tied elements too (as `sorted(...)[::-1]` would).
- (C) sorts the length-4 words alphabetically in r1 — but `key=len` ignores the letters.
- (D) uses case-sensitive order for r2.

**Tip:** multi-key sorting by successive stable sorts (secondary key first, primary key last) relies exactly on this stability.''',
            'verify': '''
assert OUTPUT.strip() == "['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']"
assert sorted(sorted(data), key=len)[::-1][2:5] == ['kiwi', 'date', 'fig'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — memoisation through a mutable default',
            'text': 'Consider the following Python program. It prints four numbers; the last two are c1 and c2. The value of c1 + c2 is ______.',
            'code': '''calls = 0
def T(n, memo={}):
    global calls
    calls += 1
    if n in memo:
        return memo[n]
    val = 1 if n < 3 else T(n - 1) + T(n - 2) + T(n - 3)
    memo[n] = val
    return val

a = T(8)
c1 = calls
b = T(10)
c2 = calls - c1
print(a, b, c1, c2)''',
            'answer': '26',
            'solution': '''The default `memo={}` is created **once** and shared by all calls — including the second top-level call `T(10)`. Every call (even a memo hit) increments `calls`.

**c1 — calls made by T(8)** (memo initially empty):

- The first-child chain T(8) → T(7) → T(6) → T(5) → T(4) → T(3) → T(2): 7 calls; T(3) then calls T(1) and T(0): 2 more (all three bases get memoised) → 9.
- Returning upward, each of T(4), T(5), T(6), T(7), T(8) makes two more calls (n−2, n−3) which are memo hits → 5 × 2 = 10.
- c1 = 9 + 10 = **19**. (Value a = T(8) = 57: 1, 1, 1, 3, 5, 9, 17, 31, 57.)

**c2 — calls made by T(10)** (memo holds 0 … 8):

- T(10) (1) → T(9) (1, new) → T(8), T(7), T(6) all hits (3) → T(9) = 105.
- Back in T(10): T(8), T(7) hits (2) → b = 193.
- c2 = 1 + 1 + 3 + 2 = **7**.

c1 + c2 = 19 + 7 = **26**.

**Traps:** assuming the memo is reset between top-level calls (c2 would be 25), or counting only cache *misses* (c1 = 9, c2 = 2).''',
            'verify': "assert OUTPUT.split() == ['57', '193', '19', '7'] and int(ANSWER) == c1 + c2",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST — deletion with two children',
            'text': "The BST below is built by inserting 40, 20, 60, 10, 30, 50, 70, 25, 35, 45, 55, 33. Then **40** is deleted and afterwards **30** is deleted. A node with two children is deleted by copying its **in-order successor**'s key into it and deleting the successor node. Height = number of edges on the longest root-to-leaf path. Which of the following statements is/are TRUE about the final tree?",
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            20,
                            [10],
                            [
                                30,
                                [25],
                                [
                                    35,
                                    [33],
                                    None,
                                ],
                            ],
                        ],
                        [
                            60,
                            [
                                50,
                                [45],
                                [55],
                            ],
                            [70],
                        ],
                    ],
                    'caption': 'Initial BST',
                },
            ],
            'options': [
                'It has exactly 4 leaves',
                'Its pre-order traversal is 45, 20, 10, 33, 25, 35, 60, 50, 55, 70',
                'Its height is 4',
                'If the in-order **predecessor** had been used for deleting 40 instead, the root after that deletion would be 35',
            ],
            'answer': ['B', 'D'],
            'solution': '''**Delete 40** (two children): successor = minimum of the right subtree = 45 (leaf, left child of 50). Copy 45 into the root and remove the leaf 45 → 50 keeps only its right child 55.

**Delete 30** (two children 25, 35): successor = minimum of 30's right subtree = 33 (left child of 35, a leaf). Copy 33 into the node and remove leaf 33 → 35 becomes a leaf.

Final tree: 45 → left 20 (10, 33 (25, 35)), right 60 (50 (–, 55), 70).

- (A) **False.** Leaves: 10, 25, 35, 55, 70 → 5.
- (B) **True.** Pre-order: 45, 20, 10, 33, 25, 35, 60, 50, 55, 70.
- (C) **False.** The longest paths are 45→20→33→25/35 and 45→60→50→55: 3 edges. (The original height 4 came from 40→20→30→35→33, and 33 has been moved up.)
- (D) **True.** The predecessor of 40 is the maximum of the left subtree: 20 → 30 → 35 (35 has no right child) → 35, so 35 would become the root (its left child 33 would move up).

**Trap:** taking the successor of 40 to be 50 (the right child) — the successor is the *leftmost* node of the right subtree.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            20,
                            [10],
                            [
                                33,
                                [25],
                                [35],
                            ],
                        ],
                        [
                            60,
                            [
                                50,
                                None,
                                [55],
                            ],
                            [70],
                        ],
                    ],
                    'highlight': [45, 33],
                    'caption': 'After deleting 40 and then 30',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import copy
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def ext(t, f):
    while t[f]: t = t[f]
    return t[0]
def dele(t, k, succ=True):
    if t is None: return None
    if k < t[0]: t[1] = dele(t[1], k, succ)
    elif k > t[0]: t[2] = dele(t[2], k, succ)
    else:
        if t[1] is None: return t[2]
        if t[2] is None: return t[1]
        if succ: s = ext(t[2], 1); t[0] = s; t[2] = dele(t[2], s, succ)
        else: s = ext(t[1], 2); t[0] = s; t[1] = dele(t[1], s, succ)
    return t
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
def lv(t): return 0 if t is None else (1 if not t[1] and not t[2] else lv(t[1]) + lv(t[2]))
T = None
for k in [40, 20, 60, 10, 30, 50, 70, 25, 35, 45, 55, 33]: T = ins(T, k)
F = dele(dele(copy.deepcopy(T), 40), 30)
res = {'A': pre(F) == [45, 20, 10, 33, 25, 35, 60, 50, 55, 70], 'B': ht(F) == 4,
       'C': dele(copy.deepcopy(T), 40, False)[0] == 35, 'D': lv(F) == 4}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — deletion with tombstones',
            'text': '''A hash table has 11 slots, h(k) = k mod 11, and linear probing. Deletion replaces a key by a DELETED marker (tombstone). **Insertion** places the key in the first slot of its probe sequence that is EMPTY or DELETED. **Search** probes until it finds the key or an EMPTY slot (DELETED slots are probed and skipped). The operations are:

insert 22, 33, 44, 13, 24; delete 33; delete 13; insert 55; insert 46; search 24; search 35.

Counting every slot examined as one probe, the total number of probes made by the two searches is ______.''',
            'answer': '7',
            'solution': '''**Inserts:** 22 → slot 0; 33 → 0 taken → 1; 44 → 0, 1 → 2; 13 (home 2) → 2 → 3; 24 (home 2) → 2, 3 → 4.

**Deletes:** 33 at slot 1 → DEL; 13 at slot 3 → DEL. Table: 0:22, 1:DEL, 2:44, 3:DEL, 4:24.

**Insert 55** (home 0): slot 0 occupied, slot 1 DEL → reuse slot 1.
**Insert 46** (home 2): slot 2 occupied, slot 3 DEL → reuse slot 3.
Table: 0:22, 1:55, 2:44, 3:46, 4:24, others EMPTY.

**Search 24** (home 2): slots 2 (44), 3 (46), 4 (24) → found, **3** probes.
**Search 35** (home 2, absent): slots 2, 3, 4, 5 (EMPTY) → **4** probes.

Total = 3 + 4 = **7**.

Why tombstones matter: had the deletions simply emptied slots 1 and 3, a search for 24 *before* the re-insertions would have stopped at the empty slot 3 and wrongly reported 24 as absent.

**Trap:** forgetting that 55 and 46 recycle the tombstones — they would then land in slots 5 and 6, and the two searches would cost 3 + 6 = 9 probes.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 22,
                        1: 'DEL',
                        2: 44,
                        3: 'DEL',
                        4: 24,
                    },
                    'caption': 'After the two deletions',
                },
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 22,
                        1: 55,
                        2: 44,
                        3: 46,
                        4: 24,
                    },
                    'caption': 'Final table (tombstones reused)',
                },
            ],
            'verify': '''
EMPTY, DEL = None, "DEL"
T = [EMPTY] * 11
def insert(k):
    i = k % 11
    while T[i] not in (EMPTY, DEL): i = (i + 1) % 11
    T[i] = k
def search(k):
    i = k % 11; p = 0
    while True:
        p += 1
        if T[i] == k: return p
        if T[i] is EMPTY: return p
        i = (i + 1) % 11
def delete(k):
    i = k % 11
    while T[i] != k: i = (i + 1) % 11
    T[i] = DEL
for k in [22, 33, 44, 13, 24]: insert(k)
delete(33); delete(13); insert(55); insert(46)
assert T[:6] == [22, 55, 44, 46, 24, None]
assert search(24) + search(35) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — Hoare partition',
            'text': 'The Hoare partition below is called as `hoare(A, 0, 7)` on A = [26, 41, 13, 26, 9, 37, 18, 52]. What does it return, and what is A afterwards?',
            'code': '''def hoare(A, lo, hi):
    p = A[lo]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while A[i] < p:
            i += 1
        j -= 1
        while A[j] > p:
            j -= 1
        if i >= j:
            return j
        A[i], A[j] = A[j], A[i]''',
            'options': [
                'Returns 4; A = [18, 9, 13, 26, 26, 37, 41, 52]',
                'Returns 2; A = [18, 9, 13, 26, 41, 37, 26, 52]',
                'Returns 3; A = [18, 9, 13, 26, 41, 37, 26, 52]',
                'Returns 3; A = [18, 9, 13, 26, 37, 41, 26, 52]',
            ],
            'answer': 'C',
            'solution': '''Hoare's scheme moves i right past elements < p and j left past elements > p, then swaps; elements **equal** to the pivot stop both scans. It returns j such that A[lo..j] ≤ p ≤ A[j+1..hi] — the pivot is **not** necessarily in its final position.

p = 26.

- i → 0 (A[0] = 26 is not < 26). j: 52 > 26 → skip, stops at 6 (18). i < j → swap A[0], A[6] → [18, 41, 13, 26, 9, 37, 26, 52].
- i → 1 (41 stops). j: 37 > 26 → skip, stops at 4 (9). Swap → [18, 9, 13, 26, 41, 37, 26, 52].
- i → 2 (13 < 26), 3 (26 stops). j → 3 (26 is not > 26). i ≥ j → **return 3**.

Result: returns 3, A = [18, 9, 13, 26, 41, 37, 26, 52] → option (C). Quicksort then recurses on A[0..3] and A[4..7] (note the pivot value 26 appears on *both* sides).

- (A) is what a Lomuto-style partition that places the pivot would suggest — Hoare does not.
- (B) returns i − 1 instead of j.
- (D) performs an extra swap of 41 and 37, which never happens.

**Trap:** with Hoare partition the recursive calls must be on [lo, j] and [j + 1, hi] (not j − 1), otherwise elements can be lost or the recursion may not shrink.''',
            'verify': '''
A = [26, 41, 13, 26, 9, 37, 18, 52]
r = hoare(A, 0, 7)
assert r == 3 and A == [18, 9, 13, 26, 41, 37, 26, 52]
assert max(A[:r + 1]) <= 26 <= min(A[r + 1:]) and ANSWER == 'C'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest and longest paths in a DAG',
            'text': 'Consider the weighted DAG below (note the negative edge B→C). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 3],
                        ['S', 'B', 6],
                        ['A', 'B', 2],
                        ['A', 'C', 7],
                        ['B', 'C', -4],
                        ['B', 'D', 4],
                        ['C', 'D', 1],
                        ['C', 'T', 5],
                        ['D', 'T', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2],
                        'D': [3, 0],
                        'T': [4.5, 1],
                    },
                },
            ],
            'options': [
                'The DAG has exactly 2 topological orderings',
                'Textbook Dijkstra from S (a vertex is final once extracted; edges into extracted vertices are ignored) computes the correct shortest distance for **every** vertex of this graph',
                'The longest (maximum-weight) S→T path has weight 15',
                'The shortest S→T distance is 4',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''In a DAG, shortest **and** longest paths are found by relaxing edges in topological order (negative weights are fine). Here S→A→B→C→D→T is a Hamiltonian path, so the topological order is forced: **S, A, B, C, D, T**.

Shortest distances in that order: A 3; B = min(6, 3+2) = 5; C = min(3+7, 5−4) = 1; D = min(5+4, 1+1) = 2; T = min(1+5, 2+2) = 4.
Longest distances: A 3; B = max(6, 5) = 6; C = max(10, 2) = 10; D = max(10, 11) = 11; T = max(10+5, 11+2) = 15.

- (A) **False** — exactly one topological order.
- (B) **True**, surprisingly. Dijkstra: extract S → A 3, B 6; extract A → B 5, C 10; extract B → C = 1, D 9; now the smallest label is C (1) → D 2, T 6; extract D → T 4; extract T. The negative edge B→C is relaxed **before** C is extracted, so nothing goes wrong. Negative edges *can* break Dijkstra, but they do not have to.
- (C) **True** — 15 via S→A→C→T (3 + 7 + 5).
- (D) **True** — 4 via S→A→B→C→D→T (3 + 2 − 4 + 1 + 2).

**Trap:** rejecting (B) by reflex. Dijkstra fails only when a vertex is extracted before a cheaper path through a negative edge reaches it.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
E = [("S","A",3),("S","B",6),("A","B",2),("A","C",7),("B","C",-4),("B","D",4),("C","D",1),
     ("C","T",5),("D","T",2)]
V = "SABCDT"
orders = [p for p in itertools.permutations(V)
          if all(p.index(u) < p.index(v) for u, v, _ in E)]
INF = float('inf')
sd = {v: INF for v in V}; ld = {v: -INF for v in V}; sd["S"] = ld["S"] = 0
for u in orders[0]:
    for a, b, w in E:
        if a == u: sd[b] = min(sd[b], sd[u] + w); ld[b] = max(ld[b], ld[u] + w)
G = {}
for a, b, w in E: G.setdefault(a, []).append((b, w))
dj = {v: INF for v in V}; dj["S"] = 0; done = []
while len(done) < 6:
    u = min((v for v in V if v not in done), key=lambda v: (dj[v], v)); done.append(u)
    for b, w in G.get(u, []):
        if b not in done and dj[u] + w < dj[b]: dj[b] = dj[u] + w
res = {'A': sd["T"] == 4, 'B': ld["T"] == 15, 'C': dj == sd, 'D': len(orders) == 2}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Divide and conquer — inversion counting',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''def count(a):
    if len(a) < 2:
        return a, 0
    m = len(a) // 2
    L, x = count(a[:m])
    R, y = count(a[m:])
    out, i, j, inv = [], 0, 0, x + y
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            inv += len(L) - i
    out += L[i:] + R[j:]
    return out, inv

print(count([5, 3, 5, 1, 3, 5, 2, 2])[1])''',
            'answer': '16',
            'solution': '''This is merge sort that counts **inversions** (pairs i < j with a[i] > a[j]): when R[j] is output before the remaining L[i…], it forms an inversion with each of those len(L) − i elements. Because the test is `L[i] <= R[j]`, **equal** keys are not counted — exactly as the strict definition requires.

Count by levels for [5, 3, 5, 1 | 3, 5, 2, 2]:

- Pairs: [5,3] → 1; [5,1] → 1; [3,5] → 0; [2,2] → 0 (equal). Subtotal 2.
- Merge [3,5]+[1,5]: 1 jumps over 3, 5 → 2. Merge [3,5]+[2,2]: each 2 jumps over 3, 5 → 4. Subtotal 6.
- Final merge [1,3,5,5] + [2,2,3,5]: each 2 jumps over 3, 5, 5 → 3 + 3; 3 jumps over 5, 5 → 2; the right 5 does not jump over the left 5s (equal). Subtotal 8.

Total = 2 + 6 + 8 = **16**.

Direct check: for each element count the smaller elements to its right — 5:5, 3:3, 5:4, 1:0, 3:2, 5:2, 2:0, 2:0 → 16.

Time: T(n) = 2T(n/2) + Θ(n) = Θ(n log n), versus Θ(n²) for checking all pairs.

**Trap:** counting equal pairs (using `<` instead of `<=` would also count 5-5, 3-3 and 2-2 crossings) or adding only 1 per jump instead of len(L) − i.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Inversions counted at each merge level',
                    'row_labels': ['level 1', 'level 2', 'level 3'],
                    'col_labels': ['merged runs', 'count'],
                    'rows': [
                        ['35 | 15 | 35 | 22', '1+1+0+0 = 2'],
                        ['1355 | 2235', '2+4 = 6'],
                        ['12233555', '3+3+2 = 8'],
                    ],
                },
            ],
            'verify': '''
a = [5, 3, 5, 1, 3, 5, 2, 2]
brute = sum(1 for i in range(8) for j in range(i + 1, 8) if a[i] > a[j])
assert int(OUTPUT) == brute == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Heaps — top-k of a stream',
            'text': '''To keep the 3 largest values of a stream, a binary **min**-heap of capacity 3 is used (array, root at index 0). The first three values are inserted normally (append + sift-up). For each later value x: if x > root, the root is **replaced** by x and sifted down (swap with the smaller child while larger than it); otherwise x is discarded. For the stream

15, 4, 22, 9, 31, 7, 18, 26, 3

the final heap array is''',
            'options': ['[22, 26, 31]', '[26, 31, 22]', '[18, 31, 26]', '[22, 31, 26]'],
            'answer': 'D',
            'solution': '''A min-heap of size k holds the k largest values seen so far; its root is the k-th largest, the threshold a new value must beat. Each step costs O(log k).

- 15 → [15]; 4 → append, sift up → [4, 15]; 22 → [4, 15, 22].
- 9 > 4 → root := 9 → children 15, 22 → stays → [9, 15, 22].
- 31 > 9 → root := 31 → smaller child 15 → swap → [15, 31, 22].
- 7 < 15 → discard.
- 18 > 15 → root := 18 → 18 < 31, 22 → stays → [18, 31, 22].
- 26 > 18 → root := 26 → smaller child 22 → swap → [22, 31, 26].
- 3 < 22 → discard.

Final **[22, 31, 26]** → option (D); the three largest values are 31, 26, 22 and the root 22 is the 3rd largest.

- (A) is the sorted order — a heap array need not be sorted.
- (B) forgets to sift 26 down in the last replacement.
- (C) keeps 18 — i.e. ignores that 26 beats the root.

**Trap:** using a *max*-heap for ‘k largest’ — the min-heap is what lets the smallest of the kept values be evicted in O(log k).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [22, 31, 26],
                    'caption': 'Final min-heap',
                },
            ],
            'verify': '''
def sd(h, i):
    n = len(h)
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < n and h[l] < h[m]: m = l
        if r < n and h[r] < h[m]: m = r
        if m == i: return
        h[i], h[m] = h[m], h[i]; i = m
h = []
for x in [15, 4, 22, 9, 31, 7, 18, 26, 3]:
    if len(h) < 3:
        h.append(x); i = len(h) - 1
        while i > 0 and h[(i - 1) // 2] > h[i]:
            p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p
    elif x > h[0]:
        h[0] = x; sd(h, 0)
opts = {'A': [22, 26, 31], 'B': [26, 31, 22], 'C': [18, 31, 26], 'D': [22, 31, 26]}
assert [k for k in opts if opts[k] == h] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Graph theory — maximum edges with components',
            'text': 'A simple undirected graph has 15 vertices and exactly 3 connected components, and **each component has at least 3 vertices**. The maximum possible number of edges is ______.',
            'answer': '42',
            'solution': '''Within each component the edge count is maximised by making it complete, so with component sizes a + b + c = 15 the maximum is C(a, 2) + C(b, 2) + C(c, 2). Since C(x, 2) is convex, the sum is largest when the sizes are as **unbalanced** as allowed.

- Without the size restriction: 1 + 1 + 13 → C(13, 2) = 78 (the classic answer, (n − k)(n − k + 1)/2).
- With every component ≥ 3: make two components as small as possible: 3 + 3 + 9 → 3 + 3 + C(9, 2) = 3 + 3 + 36 = **42**.

Check other splits: 3 + 4 + 8 → 3 + 6 + 28 = 37; 3 + 5 + 7 → 3 + 10 + 21 = 34; 5 + 5 + 5 → 30. Moving a vertex from a smaller to the largest component never decreases the total, so 42 is the maximum.

**Trap:** answering 78 by applying the textbook formula without the extra constraint, or choosing the balanced split (30) by intuition.''',
            'verify': '''
from math import comb
best = max(comb(a, 2) + comb(b, 2) + comb(15 - a - b, 2)
           for a in range(3, 14) for b in range(3, 14) if 15 - a - b >= 3)
assert best == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary search — counting occurrences',
            'text': 'Consider the following functions, where `a` is a list sorted in non-decreasing order. Which of the following statements is/are TRUE?',
            'code': '''def first_ge(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

def count(a, x):
    return first_ge(a, x + 1) - first_ge(a, x)''',
            'options': [
                'For a list of length 1000, the loop in `first_ge` executes at most 10 times',
                '`first_ge([], 7)` returns 0',
                '`count([1, 2, 2, 2, 5], 2)` returns 3',
                '`count(a, x)` returns the number of occurrences of x for every sorted list of **floats** a and float x',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''`first_ge` is a lower-bound search on the half-open range [lo, hi): it returns the first index whose element is ≥ x (len(a) if none).

- (A) **True.** The range size s = hi − lo shrinks to at most ⌊s/2⌋ each iteration (either [lo, mid) or [mid + 1, hi)). Starting from 1000: 1000 → 500 → 250 → 125 → 62 → 31 → 15 → 7 → 3 → 1 → 0 is the slowest possible chain — exactly 10 iterations; in general ⌊log₂ n⌋ + 1.
- (B) **True.** lo = hi = 0 → loop skipped → 0.
- (C) **True.** first_ge(a, 3) = 4 (element 5) and first_ge(a, 2) = 1 → 4 − 1 = 3.
- (D) **False.** `x + 1` is the next value only for **integers**. For a = [1.5, 2.0, 2.5] and x = 2.0: first_ge(a, 3.0) = 3 and first_ge(a, 2.0) = 1, giving 2 although 2.0 occurs once (2.5 was counted). The robust version uses an upper-bound search (first index with element > x) instead of x + 1.

Answer: (C), (B), (A).

**Trap:** (D) works on every integer test you try — the bug only appears when values can lie strictly between x and x + 1.''',
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import random
r = {}
r['A'] = count([1, 2, 2, 2, 5], 2) == 3
r['B'] = count([1.5, 2.0, 2.5], 2.0) == 1
r['C'] = first_ge([], 7) == 0
def iters(a, x):
    lo, hi, c = 0, len(a), 0
    while lo < hi:
        c += 1; mid = (lo + hi) // 2
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    return c
a = list(range(1000))
r['D'] = max(iters(a, x + d) for x in range(1000) for d in (0, 0.5)) <= 10
assert max(iters(a, x) for x in range(1001)) == 10
for _ in range(200):
    b = sorted(random.randint(0, 9) for _ in range(random.randint(0, 15)))
    assert all(count(b, x) == b.count(x) for x in range(-1, 11))
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
    ],
}
