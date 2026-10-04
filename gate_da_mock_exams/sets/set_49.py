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
