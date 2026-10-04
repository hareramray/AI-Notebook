# Set 49 — Challenge Mock — Paper 4
SET = {
    "number": 49,
    "title": "Challenge Mock — Paper 4",
    "difficulty": "Hard",
    "focus": "hardest, multi-concept, trap-heavy 2-mark questions",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — list multiplication aliasing",
            "text": "Consider the following Python program. What is printed?",
            "code": '''grid = [[0] * 3] * 3
grid[0][1] = 5
row = grid[1][:]
row[2] = 7
print(grid[2], row, grid[0] is grid[2], row == grid[1])''',
            "options": ["`[0, 0, 0] [0, 5, 7] False False`", "`[0, 5, 0] [0, 5, 7] True True`",
                        "`[0, 5, 0] [0, 5, 7] True False`", "`[0, 5, 0] [0, 0, 7] True False`"],
            "answer": "C",
            "solution": (
                "`[[0] * 3] * 3` builds **one** inner list and an outer list holding three references to "
                "it. `[0] * 3` itself is fine, because its elements are immutable ints.\n\n"
                "- `grid[0][1] = 5` mutates the single shared row → every ‘row’ reads [0, 5, 0].\n"
                "- `grid[1][:]` is a **shallow copy** of that row → a new list [0, 5, 0]; `row[2] = 7` "
                "changes only the copy → row = [0, 5, 7].\n"
                "- `grid[0] is grid[2]` → True (same object).\n"
                "- `row == grid[1]` compares values: [0, 5, 7] vs [0, 5, 0] → False.\n\n"
                "Output `[0, 5, 0] [0, 5, 7] True False` → option (C).\n\n"
                "- (A) assumes three independent rows.\n"
                "- (B) assumes the slice is an alias (it is a copy).\n"
                "- (D) assumes the copy was taken before the assignment of 5 reached row 1.\n\n"
                "**Fix:** `grid = [[0] * 3 for _ in range(3)]` creates three separate rows — the standard "
                "way to build a DP table or an adjacency matrix."
            ),
            "verify": "assert OUTPUT.strip() == '[0, 5, 0] [0, 5, 7] True False' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — global vs nonlocal",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''x = 10
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
            "answer": "73",
            "solution": (
                "There are two different variables named x: the **global** x (10) and the **local** x of "
                "`outer` (1). `nonlocal x` in `inner` binds to outer's x; `global x` in `other` binds to "
                "the module-level x.\n\n"
                "Inside `outer`, the sum is evaluated left to right:\n\n"
                "- `inner()` → outer's x = 1 + 2 = 3 → returns 3.\n"
                "- `other()` → global x = 10 × 3 = 30 → returns 30.\n"
                "- `inner()` → outer's x = 3 + 2 = 5 → returns 5.\n"
                "- `x` (outer's local) → 5.\n"
                "- outer() returns 3 + 30 + 5 + 5 = 43.\n\n"
                "In `print(outer() + x)`, `outer()` is evaluated first (43) and **then** the global x is "
                "read — it is already 30. Result 43 + 30 = **73**.\n\n"
                "**Traps:** using the stale global 10 (→ 53), or letting `other` modify outer's x "
                "(→ different sums). Python evaluates the operands of `+` strictly left to right, so the "
                "side effect inside `outer()` is visible to the right operand."
            ),
            "verify": "assert int(OUTPUT) == int(ANSWER) == 73",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks — prefix expression evaluation",
            "text": ("The prefix (Polish) expression below is evaluated with a stack by scanning from **right to "
                     "left**. `^` is exponentiation and `/` is exact division.\n\n"
                     "− / 8 ^ 2 2 * + 4 2 3\n\n"
                     "The value of the expression is"),
            "options": ["−16", "16", "2", "17.5"],
            "answer": "A",
            "solution": (
                "Scanning a prefix expression right to left, operands are pushed; for an operator the "
                "**first** popped value is the **left** operand (the opposite of postfix evaluation).\n\n"
                "- 3, 2, 4 → stack (bottom→top) [3, 2, 4].\n"
                "- `+` → pop 4 (left), 2 (right) → 6 → [3, 6].\n"
                "- `*` → pop 6 (left), 3 (right) → 18 → [18].\n"
                "- 2, 2 → [18, 2, 2]; `^` → 2² = 4 → [18, 4].\n"
                "- 8 → [18, 4, 8]; `/` → pop 8 (left), 4 (right) → 2 → [18, 2].\n"
                "- `−` → pop 2 (left), 18 (right) → 2 − 18 = **−16**.\n\n"
                "Infix: (8 / 2²) − ((4 + 2) × 3) = 2 − 18 = −16 → option (A).\n\n"
                "- (B) 16 uses the postfix pop order for the final `−` (18 − 2).\n"
                "- (C) 2 is just the left operand 8 / 4.\n"
                "- (D) 17.5 applies the postfix pop order to *every* operator: 4 / 8 = 0.5 and 18 − 0.5.\n\n"
                "**Trap:** in prefix the operator's left operand is the one nearer to it, which ends up on "
                "**top** of the stack."
            ),
            "verify": '''
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
        # ------------------------------------------------------------ Q4
        {
            "type": "MCQ", "marks": 1, "topic": "Linked lists — reversing in groups of k",
            "text": "Consider the following Python program. What is printed?",
            "code": '''class N:
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
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7, 8], "head": "h",
                          "caption": "List built by the loop"}],
            "options": ["`[3, 2, 1, 6, 5, 4, 8, 7]`", "`[3, 2, 1, 6, 5, 4, 7, 8]`",
                        "`[8, 7, 6, 5, 4, 3, 2, 1]`", "`[1, 2, 3, 6, 5, 4, 7, 8]`"],
            "answer": "B",
            "solution": (
                "The loop builds 1 → 2 → … → 8 (each new node is put in front, from 8 down to 1).\n\n"
                "`rev_k` first checks whether k = 3 nodes remain; if not, the group is returned unchanged. "
                "Otherwise it recursively processes the rest, and then reverses the current k nodes, "
                "pointing the first one at the processed remainder (`prev` starts as that remainder).\n\n"
                "- Group 1, 2, 3 → becomes 3 → 2 → 1 → (rest).\n"
                "- Group 4, 5, 6 → 6 → 5 → 4 → (rest).\n"
                "- Remaining 7, 8: only 2 < 3 nodes → returned as is.\n\n"
                "Output `[3, 2, 1, 6, 5, 4, 7, 8]` → option (B).\n\n"
                "**The tuple assignment** `cur.nx, prev, cur = prev, cur, cur.nx` is safe: the right-hand "
                "side is evaluated completely first (old prev, old cur, old cur.nx), then the targets are "
                "assigned left to right, and `cur.nx` is assigned while `cur` still names the old node.\n\n"
                "- (A) also reverses the short final group.\n"
                "- (C) is a full reversal.\n"
                "- (D) skips the first group.\n\n"
                "**Trap:** reordering the targets as `cur, cur.nx, prev = …` would set `.nx` on the *new* "
                "cur — a classic bug."
            ),
            "verify": "assert OUTPUT.strip() == '[3, 2, 1, 6, 5, 4, 7, 8]' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MSQ", "marks": 1, "topic": "Binary trees — counting facts",
            "text": "Which of the following statements is/are TRUE?",
            "options": [
                "A full binary tree (every node has 0 or 2 children) with 20 leaves has exactly 39 nodes",
                "Every binary tree with 12 leaves has exactly 11 nodes with two children",
                "A complete binary tree with 100 nodes has height 7 (height = edges on the longest "
                "root-to-leaf path)",
                "A binary tree with n nodes has exactly n + 1 empty (None) child pointers",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Let n₀, n₁, n₂ be the numbers of nodes with 0, 1, 2 children. Counting edges two ways: "
                "n − 1 = n₁ + 2n₂ and n = n₀ + n₁ + n₂ ⇒ **n₀ = n₂ + 1**.\n\n"
                "- (A) **True.** Full ⇒ n₁ = 0, so n₂ = 20 − 1 = 19 and n = 20 + 19 = 39.\n"
                "- (B) **True.** n₂ = n₀ − 1 = 11 for *every* binary tree, regardless of n₁.\n"
                "- (C) **False.** A complete tree of height h has between 2^h and 2^{h+1} − 1 nodes; "
                "2⁶ = 64 ≤ 100 ≤ 127, so the height is ⌊log₂ 100⌋ = **6**.\n"
                "- (D) **True.** n nodes have 2n child pointers, and exactly n − 1 of them are used "
                "(one per non-root node), leaving 2n − (n − 1) = n + 1 empty.\n\n"
                "Answer: (A), (B), (D).\n\n"
                "**Trap:** (C) uses the node-count definition of height (7 levels); with edges it is 6."
            ),
            "verify": '''
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
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — probability of no collision",
            "text": ("Three distinct keys are inserted into a hash table with 8 slots. Assume each key "
                     "independently hashes to each slot with probability 1/8. The probability that **no two** "
                     "keys hash to the same slot is closest to"),
            "options": ["0.670", "0.875", "0.344", "0.656"],
            "answer": "D",
            "solution": (
                "Count favourable outcomes: the first key may go anywhere, the second must avoid one slot, "
                "the third must avoid two.\n\n"
                "P(no collision) = (8/8) × (7/8) × (6/8) = 336 / 512 = 21/32 ≈ **0.656** → option (D).\n\n"
                "- (A) 0.670 = (7/8)³ treats the three *pairs* of keys as independent events — they are not "
                "(if A≠B and B≠C, the chance that A≠C changes).\n"
                "- (B) 0.875 = 7/8 is the answer for only **two** keys.\n"
                "- (C) 0.344 = 1 − 0.656 is the probability of **at least one** collision.\n\n"
                "This is the birthday problem in miniature: with m slots, collisions become likely after "
                "only about √(πm/2) keys — the reason why hash tables must resolve collisions rather than "
                "hope to avoid them.\n\n"
                "**Tip:** the expected number of colliding pairs is C(3, 2)/8 = 0.375 — linearity works even "
                "though the pair events are dependent."
            ),
            "verify": '''
import itertools
tot = ok = 0
for s in itertools.product(range(8), repeat=3):
    tot += 1; ok += len(set(s)) == 3
p = ok / tot
opts = {'A': 0.670, 'B': 0.875, 'C': 0.344, 'D': 0.656}
assert min(opts, key=lambda k: abs(opts[k] - p)) == ANSWER and abs(p - 21 / 32) < 1e-12
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — average successful search",
            "text": ("A sorted array of n = 1023 distinct keys is searched with standard binary search "
                     "(mid = (lo + hi) // 2; one three-way comparison per iteration). Each of the 1023 keys "
                     "is equally likely to be the search key. The average number of comparisons for a "
                     "**successful** search (rounded off to two decimal places) is ______."),
            "answer": ["9.00", "9.02"],
            "solution": (
                "For n = 2¹⁰ − 1 the binary-search decision tree is **perfect** with 10 levels: level d "
                "(d = 1 … 10) holds 2^{d−1} keys, each found with exactly d comparisons.\n\n"
                "Total = ∑ d · 2^{d−1} for d = 1 … 10 = (10 − 1) · 2¹⁰ + 1 = 9 · 1024 + 1 = 9217.\n\n"
                "(Identity: ∑_{d=1}^{k} d · 2^{d−1} = (k − 1) · 2^k + 1.)\n\n"
                "Average = 9217 / 1023 ≈ **9.01**.\n\n"
                "Note how close this is to the worst case (10): half of all keys sit on the bottom level, "
                "so the average is only about one comparison below the maximum, roughly log₂ n − 1.\n\n"
                "**Trap:** answering log₂ 1023 ≈ 9.998, or (1 + 10)/2 = 5.5 by assuming every number of "
                "comparisons is equally likely."
            ),
            "verify": '''
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
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Sorting — stability of selection sort",
            "text": ("Records (key, tag) are sorted by key with selection sort: for i = 0, 1, …, the record with "
                     "the smallest key in positions i … n−1 (the **first** such record if there are ties) is "
                     "swapped into position i. The input is\n\n"
                     "(4,p) (2,q) (4,r) (1,s) (2,t) (3,u).\n\n"
                     "The sequence of tags after sorting is"),
            "options": ["s q t u p r", "s q t u r p", "s t q u r p", "s t q u p r"],
            "answer": "B",
            "solution": (
                "Trace (only swaps shown):\n\n"
                "- i = 0: smallest key 1 at (1,s), index 3 → swap with (4,p): "
                "(1,s) (2,q) (4,r) (4,p) (2,t) (3,u).\n"
                "- i = 1: smallest key 2, first occurrence (2,q) at index 1 → no change.\n"
                "- i = 2: smallest key 2 is (2,t) at index 4 → swap with (4,r): "
                "(1,s) (2,q) (2,t) (4,p) (4,r) (3,u).\n"
                "- i = 3: smallest key 3 at index 5 → swap with (4,p): "
                "(1,s) (2,q) (2,t) (3,u) (4,r) (4,p).\n"
                "- i = 4: smallest is (4,r) (first of the two 4s) → no change.\n\n"
                "Tags: **s q t u r p** → option (B).\n\n"
                "The two records with key 4 came out as r, p although the input had p before r: the "
                "long-distance swap at i = 0 threw (4,p) behind (4,r). Selection sort is **not stable**.\n\n"
                "- (A) is the stable order (what insertion or merge sort would give).\n"
                "- (C) and (D) also reorder the key-2 records, which never happens here.\n\n"
                "**Trap:** concluding stability from the 2s (q before t is preserved) — one counter-example "
                "pair is enough to make a sort unstable."
            ),
            "verify": '''
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
        # ------------------------------------------------------------ Q9
        {
            "type": "MSQ", "marks": 1, "topic": "Graphs — bipartiteness",
            "text": ("The undirected graph G below is bipartite. Each option proposes adding **one** edge to G "
                     "(the options are considered separately). After which of the following additions is the "
                     "graph still bipartite?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["E", "F"], ["F", "A"],
                                    ["G", "A"], ["H", "D"]],
                          "pos": {"A": [1, 2], "B": [2.5, 2.8], "C": [4, 2], "D": [4, 0.6], "E": [2.5, -0.2],
                                  "F": [1, 0.6], "G": [-0.5, 2.6], "H": [5.5, 0]}}],
            "options": ["Edge B–E", "Edge A–C", "Edge G–H", "Edge F–G"],
            "answer": ["A", "C"],
            "solution": (
                "A connected graph is bipartite iff a BFS/DFS 2-colouring never puts the same colour on both "
                "ends of an edge (equivalently, it has no odd cycle). Colour G from A:\n\n"
                "- A: 0; B, F, G: 1 (neighbours of A); C, E: 0; D: 1; H (neighbour of D): 0.\n\n"
                "An added edge keeps the graph bipartite iff its endpoints have **different** colours.\n\n"
                "- (A) B–E: colours 1 and 0 → **still bipartite** (it creates cycles B-C-D-E-B and "
                "B-A-F-E-B of length 4).\n"
                "- (B) A–C: both 0 → odd cycle A-B-C-A of length 3 → **not** bipartite.\n"
                "- (C) G–H: colours 1 and 0 → **still bipartite** (new cycle G-A-B-C-D-H-G has length 6).\n"
                "- (D) F–G: both 1 → triangle A-F-G → **not** bipartite.\n\n"
                "Answer: (A), (C).\n\n"
                "**Trap:** judging by the picture — B–E and A–C both look like chords of the hexagon, but "
                "B–E joins vertices at odd distance 3 (closing even cycles) while A–C joins vertices at "
                "even distance 2 (closing a triangle)."
            ),
            "verify": '''
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
        # ------------------------------------------------------------ Q10
        {
            "type": "NAT", "marks": 1, "topic": "Loop counting — harmonic sums",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''c = 0
n = 20
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        c += 1
print(c)''',
            "answer": "66",
            "solution": (
                "For a fixed i the inner loop visits j = i, 2i, 3i, … ≤ n, i.e. ⌊n/i⌋ values. So\n\n"
                "c = ∑_{i=1}^{20} ⌊20/i⌋.\n\n"
                "- i = 1 … 5: 20 + 10 + 6 + 5 + 4 = 45.\n"
                "- i = 6: 3; i = 7 … 10: 2 each → 3 + 8 = 11.\n"
                "- i = 11 … 20: 1 each → 10.\n\n"
                "Total = 45 + 11 + 10 = **66**.\n\n"
                "Equivalently, c counts pairs (i, j) with i | j, i.e. ∑_{j=1}^{20} d(j), the total number of "
                "divisors of 1 … 20.\n\n"
                "**Complexity:** ∑ n/i = n · H_n ≈ n ln n, so the fragment is **Θ(n log n)** — the same "
                "harmonic-sum pattern as the sieve of Eratosthenes (which, skipping non-primes, is even "
                "Θ(n log log n)).\n\n"
                "**Trap:** assuming two nested loops over 1 … n must be Θ(n²); the step size i makes the "
                "inner loop shrink like n/i."
            ),
            "verify": "assert int(OUTPUT) == int(ANSWER) == sum(20 // i for i in range(1, 21))",
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — sorted(): keys, case and stability",
            "text": "Consider the following Python program. What is printed?",
            "code": '''data = ["kiwi", "Fig", "apple", "date", "Banana", "fig"]
r1 = sorted(data, key=len)
r2 = sorted(data, key=str.lower)
r3 = sorted(sorted(data), key=len, reverse=True)
print(r1[:3], r2[:2], r3[2:5])''',
            "options": ["`['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']`",
                        "`['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['kiwi', 'date', 'fig']`",
                        "`['Fig', 'fig', 'date'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']`",
                        "`['Fig', 'fig', 'kiwi'] ['Banana', 'Fig'] ['date', 'kiwi', 'Fig']`"],
            "answer": "A",
            "solution": (
                "Three facts decide everything: (1) `sorted` is **stable** — records with equal keys keep "
                "their relative input order; (2) default string order compares code points, so every "
                "uppercase letter precedes every lowercase letter; (3) `reverse=True` reverses the order "
                "of *keys* but still keeps equal-key records stable (it does **not** simply reverse the "
                "output list).\n\n"
                "- r1 (by length): lengths kiwi 4, Fig 3, apple 5, date 4, Banana 6, fig 3. Length 3 in "
                "input order: Fig, fig; then length 4: kiwi, date → r1[:3] = ['Fig', 'fig', 'kiwi'].\n"
                "- r2 (case-insensitive): apple, banana, date, fig, fig, kiwi → r2[:2] = ['apple', 'Banana'].\n"
                "- r3: `sorted(data)` = ['Banana', 'Fig', 'apple', 'date', 'fig', 'kiwi'] (uppercase first). "
                "Then by length descending, ties kept in this order: Banana(6), apple(5), date(4), kiwi(4), "
                "Fig(3), fig(3) → r3[2:5] = ['date', 'kiwi', 'Fig'].\n\n"
                "Output → option (A).\n\n"
                "- (B) assumes `reverse=True` reverses tied elements too (as `sorted(...)[::-1]` would).\n"
                "- (C) sorts the length-4 words alphabetically in r1 — but `key=len` ignores the letters.\n"
                "- (D) uses case-sensitive order for r2.\n\n"
                "**Tip:** multi-key sorting by successive stable sorts (secondary key first, primary key "
                "last) relies exactly on this stability."
            ),
            "verify": '''
assert OUTPUT.strip() == "['Fig', 'fig', 'kiwi'] ['apple', 'Banana'] ['date', 'kiwi', 'Fig']"
assert sorted(sorted(data), key=len)[::-1][2:5] == ['kiwi', 'date', 'fig'] and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Python — memoisation through a mutable default",
            "text": ("Consider the following Python program. It prints four numbers; the last two are c1 and "
                     "c2. The value of c1 + c2 is ______."),
            "code": '''calls = 0
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
            "answer": "26",
            "solution": (
                "The default `memo={}` is created **once** and shared by all calls — including the second "
                "top-level call `T(10)`. Every call (even a memo hit) increments `calls`.\n\n"
                "**c1 — calls made by T(8)** (memo initially empty):\n\n"
                "- The first-child chain T(8) → T(7) → T(6) → T(5) → T(4) → T(3) → T(2): 7 calls; "
                "T(3) then calls T(1) and T(0): 2 more (all three bases get memoised) → 9.\n"
                "- Returning upward, each of T(4), T(5), T(6), T(7), T(8) makes two more calls (n−2, n−3) "
                "which are memo hits → 5 × 2 = 10.\n"
                "- c1 = 9 + 10 = **19**. (Value a = T(8) = 57: 1, 1, 1, 3, 5, 9, 17, 31, 57.)\n\n"
                "**c2 — calls made by T(10)** (memo holds 0 … 8):\n\n"
                "- T(10) (1) → T(9) (1, new) → T(8), T(7), T(6) all hits (3) → T(9) = 105.\n"
                "- Back in T(10): T(8), T(7) hits (2) → b = 193.\n"
                "- c2 = 1 + 1 + 3 + 2 = **7**.\n\n"
                "c1 + c2 = 19 + 7 = **26**.\n\n"
                "**Traps:** assuming the memo is reset between top-level calls (c2 would be 25), or counting "
                "only cache *misses* (c1 = 9, c2 = 2)."
            ),
            "verify": "assert OUTPUT.split() == ['57', '193', '19', '7'] and int(ANSWER) == c1 + c2",
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "BST — deletion with two children",
            "text": ("The BST below is built by inserting 40, 20, 60, 10, 30, 50, 70, 25, 35, 45, 55, 33. Then "
                     "**40** is deleted and afterwards **30** is deleted. A node with two children is deleted "
                     "by copying its **in-order successor**'s key into it and deleting the successor node. "
                     "Height = number of edges on the longest root-to-leaf path. Which of the following "
                     "statements is/are TRUE about the final tree?"),
            "diagrams": [{"type": "bintree",
                          "tree": [40, [20, [10], [30, [25], [35, [33], None]]],
                                   [60, [50, [45], [55]], [70]]],
                          "caption": "Initial BST"}],
            "options": [
                "Its pre-order traversal is 45, 20, 10, 33, 25, 35, 60, 50, 55, 70",
                "Its height is 4",
                "If the in-order **predecessor** had been used for deleting 40 instead, the root after that "
                "deletion would be 35",
                "It has exactly 4 leaves",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Delete 40** (two children): successor = minimum of the right subtree = 45 (leaf, left "
                "child of 50). Copy 45 into the root and remove the leaf 45 → 50 keeps only its right child "
                "55.\n\n"
                "**Delete 30** (two children 25, 35): successor = minimum of 30's right subtree = 33 (left "
                "child of 35, a leaf). Copy 33 into the node and remove leaf 33 → 35 becomes a leaf.\n\n"
                "Final tree: 45 → left 20 (10, 33 (25, 35)), right 60 (50 (–, 55), 70).\n\n"
                "- (A) **True.** Pre-order: 45, 20, 10, 33, 25, 35, 60, 50, 55, 70.\n"
                "- (B) **False.** The longest paths are 45→20→33→25/35 and 45→60→50→55: 3 edges. (The "
                "original height 4 came from 40→20→30→35→33, and 33 has been moved up.)\n"
                "- (C) **True.** The predecessor of 40 is the maximum of the left subtree: 20 → 30 → 35 "
                "(35 has no right child) → 35, so 35 would become the root (its left child 33 would move up).\n"
                "- (D) **False.** Leaves: 10, 25, 35, 55, 70 → 5.\n\n"
                "**Trap:** taking the successor of 40 to be 50 (the right child) — the successor is the "
                "*leftmost* node of the right subtree."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [45, [20, [10], [33, [25], [35]]], [60, [50, None, [55]], [70]]],
                                   "highlight": [45, 33], "caption": "After deleting 40 and then 30"}],
            "verify": '''
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
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Hashing — deletion with tombstones",
            "text": ("A hash table has 11 slots, h(k) = k mod 11, and linear probing. Deletion replaces a key by "
                     "a DELETED marker (tombstone). **Insertion** places the key in the first slot of its probe "
                     "sequence that is EMPTY or DELETED. **Search** probes until it finds the key or an EMPTY "
                     "slot (DELETED slots are probed and skipped). The operations are:\n\n"
                     "insert 22, 33, 44, 13, 24; delete 33; delete 13; insert 55; insert 46; "
                     "search 24; search 35.\n\n"
                     "Counting every slot examined as one probe, the total number of probes made by the two "
                     "searches is ______."),
            "answer": "7",
            "solution": (
                "**Inserts:** 22 → slot 0; 33 → 0 taken → 1; 44 → 0, 1 → 2; 13 (home 2) → 2 → 3; "
                "24 (home 2) → 2, 3 → 4.\n\n"
                "**Deletes:** 33 at slot 1 → DEL; 13 at slot 3 → DEL. Table: 0:22, 1:DEL, 2:44, 3:DEL, "
                "4:24.\n\n"
                "**Insert 55** (home 0): slot 0 occupied, slot 1 DEL → reuse slot 1.\n"
                "**Insert 46** (home 2): slot 2 occupied, slot 3 DEL → reuse slot 3.\n"
                "Table: 0:22, 1:55, 2:44, 3:46, 4:24, others EMPTY.\n\n"
                "**Search 24** (home 2): slots 2 (44), 3 (46), 4 (24) → found, **3** probes.\n"
                "**Search 35** (home 2, absent): slots 2, 3, 4, 5 (EMPTY) → **4** probes.\n\n"
                "Total = 3 + 4 = **7**.\n\n"
                "Why tombstones matter: had the deletions simply emptied slots 1 and 3, a search for 24 "
                "*before* the re-insertions would have stopped at the empty slot 3 and wrongly reported "
                "24 as absent.\n\n"
                "**Trap:** forgetting that 55 and 46 recycle the tombstones (then 46 would land in slot 5 "
                "and the search for 35 would cost 5 probes)."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 22, 1: "DEL", 2: 44, 3: "DEL", 4: 24},
                                   "caption": "After the two deletions"},
                                  {"type": "hashtable", "size": 11,
                                   "slots": {0: 22, 1: 55, 2: 44, 3: 46, 4: 24},
                                   "caption": "Final table (tombstones reused)"}],
            "verify": '''
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
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Quicksort — Hoare partition",
            "text": ("The Hoare partition below is called as `hoare(A, 0, 7)` on "
                     "A = [26, 41, 13, 26, 9, 37, 18, 52]. What does it return, and what is A afterwards?"),
            "code": '''def hoare(A, lo, hi):
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
            "options": ["Returns 4; A = [18, 9, 13, 26, 26, 37, 41, 52]",
                        "Returns 2; A = [18, 9, 13, 26, 41, 37, 26, 52]",
                        "Returns 3; A = [18, 9, 13, 26, 41, 37, 26, 52]",
                        "Returns 3; A = [18, 9, 13, 26, 37, 41, 26, 52]"],
            "answer": "C",
            "solution": (
                "Hoare's scheme moves i right past elements < p and j left past elements > p, then swaps; "
                "elements **equal** to the pivot stop both scans. It returns j such that "
                "A[lo..j] ≤ p ≤ A[j+1..hi] — the pivot is **not** necessarily in its final position.\n\n"
                "p = 26.\n\n"
                "- i → 0 (A[0] = 26 is not < 26). j: 52 > 26 → skip, stops at 6 (18). i < j → swap A[0], A[6] "
                "→ [18, 41, 13, 26, 9, 37, 26, 52].\n"
                "- i → 1 (41 stops). j: 37 > 26 → skip, stops at 4 (9). Swap → "
                "[18, 9, 13, 26, 41, 37, 26, 52].\n"
                "- i → 2 (13 < 26), 3 (26 stops). j → 3 (26 is not > 26). i ≥ j → **return 3**.\n\n"
                "Result: returns 3, A = [18, 9, 13, 26, 41, 37, 26, 52] → option (C). Quicksort then "
                "recurses on A[0..3] and A[4..7] (note the pivot value 26 appears on *both* sides).\n\n"
                "- (A) is what a Lomuto-style partition that places the pivot would suggest — Hoare does not.\n"
                "- (B) returns i − 1 instead of j.\n"
                "- (D) performs an extra swap of 41 and 37, which never happens.\n\n"
                "**Trap:** with Hoare partition the recursive calls must be on [lo, j] and [j + 1, hi] "
                "(not j − 1), otherwise elements can be lost or the recursion may not shrink."
            ),
            "verify": '''
A = [26, 41, 13, 26, 9, 37, 18, 52]
r = hoare(A, 0, 7)
assert r == 3 and A == [18, 9, 13, 26, 41, 37, 26, 52]
assert max(A[:r + 1]) <= 26 <= min(A[r + 1:]) and ANSWER == 'C'
''',
        },
