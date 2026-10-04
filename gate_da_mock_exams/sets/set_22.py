# Set 22 — DAGs & Topological Sorting
SET = {
    "number": 22,
    "title": "DAGs & Topological Sorting",
    "difficulty": "GATE-level",
    "focus": "topological orders count, DFS edge classification, cycle detection",
    "questions": [
        # ------------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — generator exhaustion",
            "text": "Consider the following Python program. What is printed?",
            "code": '''g = (x * x for x in range(6) if x % 2 == 0)
s = sum(g)
print(s, list(g), max(g, default=-1))''',
            "options": [
                "`20 [0, 4, 16] 16`",
                "`20 [] -1`",
                "`55 [] -1`",
                "A `ValueError` is raised by `max`",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** a generator expression is a one-shot iterator. Once it has been consumed, "
                "further iteration yields nothing — it does not restart.\n\n"
                "- The generator yields x² for even x in 0..5: 0, 4, 16.\n"
                "- `sum(g)` consumes all of it → 20.\n"
                "- `list(g)` → the generator is exhausted → `[]`.\n"
                "- `max(g, default=-1)` → empty iterable, so the `default` is returned → −1 "
                "(no exception because `default` is supplied).\n\n"
                "Output: `20 [] -1`.\n\n"
                "**Options:**\n"
                "- (A) treats `g` as if it were a list that can be iterated repeatedly.\n"
                "- (C) sums the squares of all of 0..5 (0 + 1 + 4 + 9 + 16 + 25 = 55), ignoring the filter.\n"
                "- (D) would be correct only without `default=` — `max()` of an empty iterable raises "
                "ValueError, but the default suppresses it.\n\n"
                "**Tip:** use a list comprehension `[...]` when the values are needed more than once."
            ),
            "verify": "assert OUTPUT.strip() == '20 [] -1' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Topological sorting — counting orders",
            "text": "The number of distinct topological orderings of the DAG shown below is ______.",
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F"],
                          "edges": [["A", "C"], ["B", "C"], ["B", "D"], ["C", "E"], ["D", "E"], ["D", "F"]],
                          "pos": {"A": [0, 2], "B": [0, 0], "C": [2, 2], "D": [2, 0], "E": [4, 2],
                                  "F": [4, 0]}}],
            "answer": "14",
            "solution": (
                "**Concept:** count linear extensions by splitting on the first vertex (a source) and "
                "counting the orders of what remains.\n\n"
                "Constraints: A < C, B < C, B < D, C < E, D < E, D < F. Sources: A and B.\n\n"
                "**Case 1 — A first.** C still needs B, and D needs B, so B must be second. Remaining "
                "{C, D, E, F} with C < E, D < E, D < F: E must follow both C and D; F follows D.\n"
                "- C D E F, C D F E, D C E F, D C F E, D F C E → **5**.\n\n"
                "**Case 2 — B first.** Remaining {A, C, D, E, F} with A < C < E, D < E, D < F.\n"
                "- Orders of {A, C, D, E} with A < C < E and D < E: D in one of 3 places → D A C E, "
                "A D C E, A C D E.\n"
                "- Insert F anywhere after D: 4, 3 and 2 places respectively → 4 + 3 + 2 = **9**.\n\n"
                "Total = 5 + 9 = **14**.\n\n"
                "**Trap:** assuming both cases are symmetric (giving 2 × 5 or 2 × 9) — after choosing A "
                "first, B is forced, but after B first, A is *not* forced."
            ),
            "verify": '''
import itertools
E = [('A','C'),('B','C'),('B','D'),('C','E'),('D','E'),('D','F')]
cnt = 0
for p in itertools.permutations("ABCDEF"):
    pos = {v: i for i, v in enumerate(p)}
    cnt += all(pos[u] < pos[v] for u, v in E)
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Topological sorting — validity of an order",
            "text": "Which of the following is **NOT** a topological ordering of the DAG shown below?",
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["P", "Q", "R", "S", "T", "U", "V"],
                          "edges": [["P", "Q"], ["P", "R"], ["Q", "S"], ["R", "S"], ["R", "T"], ["S", "U"],
                                    ["T", "U"], ["V", "T"]],
                          "pos": {"P": [0, 2], "Q": [2, 3], "R": [2, 1], "S": [4, 2], "T": [4, 0],
                                  "U": [6, 1], "V": [2, -1]}}],
            "options": [
                "P, V, R, Q, T, S, U",
                "V, P, Q, R, S, T, U",
                "P, R, V, T, Q, S, U",
                "P, Q, V, R, T, U, S",
            ],
            "answer": "D",
            "solution": (
                "**Concept:** an ordering is topological iff for every edge u → v, u appears before v. "
                "Check each edge, focusing on the sinks and on vertices with several predecessors "
                "(S needs Q, R; T needs R, V; U needs S, T).\n\n"
                "- (A) P, V, R, Q, T, S, U: P before Q, R; R before S, T; V before T; Q before S; S, T before U. "
                "**Valid.**\n"
                "- (B) V, P, Q, R, S, T, U: every edge goes forward. **Valid.**\n"
                "- (C) P, R, V, T, Q, S, U: T after R and V; S after Q and R; U last. **Valid.**\n"
                "- (D) P, Q, V, R, T, U, S: U appears **before** S although S → U is an edge. **Not valid.**\n\n"
                "**Trap:** checking only that each vertex appears after *one* of its predecessors — U comes "
                "after T, but it must also come after S. The unique sink U must always be last here."
            ),
            "verify": '''
E = [('P','Q'),('P','R'),('Q','S'),('R','S'),('R','T'),('S','U'),('T','U'),('V','T')]
def ok(o):
    pos = {v: i for i, v in enumerate(o.replace(', ', ''))}
    return all(pos[u] < pos[v] for u, v in E)
opts = ["P, V, R, Q, T, S, U", "V, P, Q, R, S, T, U", "P, R, V, T, Q, S, U", "P, Q, V, R, T, U, S"]
assert [c for c, o in zip("ABCD", opts) if not ok(o)] == [ANSWER]
''',
        },
        # ------------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "DFS — edge classification",
            "text": ("DFS is run on the directed graph below. The outer loop tries start vertices in "
                     "alphabetical order, adjacency lists are explored in alphabetical order, and a single "
                     "clock (starting at 1) is incremented at every discovery and every finish. Which of the "
                     "following statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                          "edges": [["A", "B"], ["B", "C"], ["B", "E"], ["C", "A"], ["C", "E"], ["D", "B"],
                                    ["D", "E"], ["E", "F"], ["F", "D"], ["G", "A"], ["G", "C"]],
                          "pos": {"A": [0, 2], "B": [2, 2], "C": [2, 0], "D": [4, 2], "E": [4, 0],
                                  "F": [6, 1], "G": [0, 0]}}],
            "options": [
                "(C, A) is a back edge",
                "(B, E) is a cross edge",
                "The DFS finds exactly 3 back edges",
                "D is discovered at time 6 and finished at time 7",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept:** for an edge u → v examined during DFS: v undiscovered → *tree*; v discovered "
                "but not finished (an ancestor on the stack) → *back*; v finished and d[u] < d[v] → "
                "*forward*; v finished and d[u] > d[v] → *cross*.\n\n"
                "Trace (d/f times):\n"
                "- A(1) → B(2) → C(3). C → A: A is on the stack → **back**. C → E: tree, E(4).\n"
                "- E → F: tree, F(5). F → D: tree, D(6). D → B: B on stack → **back**. D → E: E on stack → "
                "**back**. D finishes (7); F (8); E (9); C (10).\n"
                "- Back at B: B → E: E already finished, d[B] = 2 < d[E] = 4 → **forward**. B finishes (11), "
                "A (12).\n"
                "- Restart at G(13): G → A and G → C go to finished vertices discovered earlier → **cross**. "
                "G finishes (14).\n\n"
                "**Verdicts:** (A) **True**. (B) **False** — it is a forward edge (E is a descendant of B "
                "reached via C). (C) back edges C→A, D→B, D→E → exactly 3, **True**. (D) d[D] = 6, "
                "f[D] = 7, **True**.\n\n"
                "**Trap:** calling (B, E) a cross edge because E was reached 'from another branch' — what "
                "matters is that E is a descendant of B in the DFS tree."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Discovery / finish times",
                                   "col_labels": ["A", "B", "C", "D", "E", "F", "G"],
                                   "row_labels": ["d", "f"],
                                   "rows": [[1, 2, 3, 6, 4, 5, 13], [12, 11, 10, 7, 9, 8, 14]]}],
            "verify": '''
V = "ABCDEFG"
E = [('A','B'),('B','C'),('B','E'),('C','A'),('C','E'),('D','B'),('D','E'),('E','F'),
     ('F','D'),('G','A'),('G','C')]
G = {v: sorted(w for u, w in E if u == v) for v in V}
d, f, t, cls = {}, {}, [1], {}
def dfs(u):
    d[u] = t[0]; t[0] += 1
    for v in G[u]:
        if v not in d:
            cls[(u, v)] = 'tree'; dfs(v)
        elif v not in f: cls[(u, v)] = 'back'
        elif d[u] < d[v]: cls[(u, v)] = 'forward'
        else: cls[(u, v)] = 'cross'
    f[u] = t[0]; t[0] += 1
for v in V:
    if v not in d: dfs(v)
nb = sum(1 for x in cls.values() if x == 'back')
truth = [cls[('C','A')] == 'back', cls[('B','E')] == 'cross', nb == 3, (d['D'], f['D']) == (6, 7)]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Stacks — monotonic stack with Python modulo",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''st = []
for x in [7, -3, 5, -8, 2]:
    while st and st[-1] % 4 > x % 4:
        st.pop()
    st.append(x)
print(sum(st))''',
            "answer": "-6",
            "solution": (
                "**Concept:** this is a *monotonic stack*: before pushing x, it pops every element whose "
                "key (value mod 4) is larger than x's key, so keys on the stack are non-decreasing from "
                "bottom to top. In Python, `%` returns a result with the sign of the divisor, so "
                "−3 % 4 = 1 and −8 % 4 = 0.\n\n"
                "Keys: 7 → 3, −3 → 1, 5 → 1, −8 → 0, 2 → 2.\n\n"
                "Trace:\n"
                "- x = 7 (key 3): push → [7]\n"
                "- x = −3 (key 1): top key 3 > 1 → pop 7; push → [−3]\n"
                "- x = 5 (key 1): top key 1 > 1? No → push → [−3, 5]\n"
                "- x = −8 (key 0): pop 5 (1 > 0), pop −3 (1 > 0); push → [−8]\n"
                "- x = 2 (key 2): 0 > 2? No → push → [−8, 2]\n\n"
                "Sum = −8 + 2 = **−6**.\n\n"
                "**Trap:** using C-style remainders (−3 % 4 = −3, −8 % 4 = 0) changes the pops: −3 would "
                "have key −3 and pop everything, giving a different stack. Python's `%` is never "
                "negative for a positive divisor."
            ),
            "solution_diagrams": [{"type": "stack", "values": [-8, 2], "label": "st",
                                   "caption": "Final stack (keys 0, 2 — non-decreasing upwards)"}],
            "verify": "assert int(OUTPUT) == int(ANSWER) and st == [-8, 2]",
        },
        # ------------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Doubly linked lists — swapping adjacent nodes",
            "text": ("The program builds a doubly linked list P ⇄ Q ⇄ R ⇄ S ⇄ T and then rewires pointers "
                     "around nodes Q and R. What is printed?"),
            "code": '''class D:
    def __init__(s, v):
        s.v, s.prev, s.next = v, None, None

nodes = [D(v) for v in "PQRST"]
for x, y in zip(nodes, nodes[1:]):
    x.next, y.prev = y, x
p, q = nodes[1], nodes[2]
p.prev.next = q
q.next.prev = p
p.next = q.next
q.prev = p.prev
q.next = p
p.prev = q
h, fw = nodes[0], ""
while h:
    fw, h = fw + h.v, h.next
t, bw = nodes[4], ""
while t:
    bw, t = bw + t.v, t.prev
print(fw, bw)''',
            "options": ["`PRQST TSRQP`", "`PRQST TSQRP`", "`PQRST TSRQP`", "`PRST TSQRP`"],
            "answer": "B",
            "solution": (
                "**Concept:** swapping two adjacent nodes p, q (q = p.next) in a doubly linked list needs "
                "six pointer updates: the outer neighbours' links (P.next, S.prev) and both links of each "
                "of p and q. The order matters only where a pointer is read after being overwritten.\n\n"
                "Step by step (p = Q, q = R):\n"
                "- `p.prev.next = q` → P.next = R\n"
                "- `q.next.prev = p` → S.prev = Q (q.next is still S)\n"
                "- `p.next = q.next` → Q.next = S\n"
                "- `q.prev = p.prev` → R.prev = P (p.prev is still P)\n"
                "- `q.next = p` → R.next = Q\n"
                "- `p.prev = q` → Q.prev = R\n\n"
                "Forward from P: P → R → Q → S → T = `PRQST`. Backward from T: T → S → Q → R → P = "
                "`TSQRP`. The two traversals are mirror images, confirming the list is consistent.\n\n"
                "**Options:** (A) has a backward chain that was not updated; (C) assumes nothing changed; "
                "(D) loses a node.\n\n"
                "**Trap:** if `p.prev = q` were executed before `q.prev = p.prev`, R.prev would point to R "
                "itself and the backward traversal would loop forever — always read old pointers before "
                "overwriting them."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": ["P", "R", "Q", "S", "T"], "doubly": True,
                                   "head": "head", "caption": "List after the swap"}],
            "verify": "assert OUTPUT.strip() == 'PRQST TSQRP' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — double hashing",
            "text": ("Keys 18, 41, 25, 57, 70, 31 are inserted in this order into an initially empty hash "
                     "table of size 13 using double hashing: probe i (i = 0, 1, 2, …) examines slot "
                     "(h₁(k) + i · h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). "
                     "The index of the slot in which 31 is stored is ______."),
            "answer": "9",
            "solution": (
                "**Concept:** in double hashing the step size depends on the key, so keys with the same home "
                "slot follow different probe sequences (no secondary clustering).\n\n"
                "- 18: h₁ = 5 → slot 5.\n"
                "- 41: h₁ = 2 → slot 2.\n"
                "- 25: h₁ = 12 → slot 12.\n"
                "- 57: h₁ = 5 (full); h₂ = 1 + 2 = 3 → 8 → slot 8.\n"
                "- 70: h₁ = 5 (full); h₂ = 1 + 4 = 5 → 10 → slot 10.\n"
                "- 31: h₁ = 5 (full); h₂ = 1 + 9 = 10 → probes 5, (5 + 10) mod 13 = 2 (full), "
                "(5 + 20) mod 13 = 12 (full), (5 + 30) mod 13 = 9 → **slot 9**.\n\n"
                "31 needed 4 probes even though 57 and 70 (same home slot) needed only 2 each.\n\n"
                "**Trap:** using linear probing by mistake (31 would go to slot 6), or forgetting the "
                "'1 +' in h₂ (step 9 → probes 5, 1 → slot 1)."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 13,
                                   "slots": {2: 41, 5: 18, 8: 57, 9: 31, 10: 70, 12: 25},
                                   "caption": "Final table"}],
            "verify": '''
T = [None]*13
for k in [18, 41, 25, 57, 70, 31]:
    for i in range(13):
        s = (k % 13 + i * (1 + k % 11)) % 13
        if T[s] is None:
            T[s] = k; break
assert T.index(31) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Binary trees — reconstruction from traversals",
            "text": ("A binary tree with distinct labels has\n"
                     "- pre-order: M, F, B, A, D, K, H, P, S, R\n"
                     "- in-order: A, B, D, F, H, K, M, P, R, S\n\n"
                     "Which of the following statements is/are TRUE? (Height = number of edges on the "
                     "longest root-to-leaf path.)"),
            "options": [
                "The post-order traversal is A, D, B, H, K, F, R, S, P, M",
                "The height of the tree is 4",
                "The tree has exactly 4 leaves",
                "The level-order traversal is M, F, P, B, K, S, A, D, H, R",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept:** the first pre-order element is the root; its position in the in-order splits "
                "the remaining labels into the left and right subtrees. Recurse.\n\n"
                "- Root M; in-order left {A, B, D, F, H, K}, right {P, R, S}.\n"
                "- Left pre-order F, B, A, D, K, H → root F; in-order left {A, B, D}, right {H, K}.\n"
                "  - B, A, D → B with children A, D.\n"
                "  - K, H → K with left child H.\n"
                "- Right pre-order P, S, R → root P; in-order {P | R, S} → P has no left child; right "
                "subtree pre-order S, R with in-order R, S → S with left child R.\n\n"
                "**Verdicts:**\n"
                "- (A) post-order: A, D, B, H, K, F, R, S, P, M. **True.**\n"
                "- (B) longest paths M–F–B–A, M–F–K–H, M–P–S–R all have 3 edges → height 3. **False.**\n"
                "- (C) leaves A, D, H, R → 4. **True.**\n"
                "- (D) levels: M | F, P | B, K, S | A, D, H, R. **True.**\n\n"
                "**Trap:** counting nodes instead of edges for height gives 4."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": ["M", ["F", ["B", ["A"], ["D"]], ["K", ["H"], None]],
                                            ["P", None, ["S", ["R"], None]]],
                                   "caption": "Reconstructed tree"}],
            "verify": '''
def build(pre, ino):
    if not pre: return None
    r = pre[0]; k = ino.index(r)
    return [r, build(pre[1:k+1], ino[:k]), build(pre[k+1:], ino[k+1:])]
T = build(list("MFBADKHPSR"), list("ABDFHKMPRS"))
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def leaves(t): return 0 if t is None else (1 if t[1] is None and t[2] is None else leaves(t[1]) + leaves(t[2]))
lv, q = [], [T]
while q:
    n = q.pop(0); lv.append(n[0]); q += [c for c in n[1:] if c]
truth = [post(T) == list("ADBHKFRSPM"), h(T) == 4, leaves(T) == 4, lv == list("MFPBKSADHR")]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — lower bound",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def lb(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

A = [2, 4, 4, 4, 7, 9, 9, 12]
print(lb(A, 4), lb(A, 9) - lb(A, 8), lb(A, 13))''',
            "options": ["`3 1 8`", "`1 1 7`", "`1 0 8`", "`2 0 8`"],
            "answer": "C",
            "solution": (
                "**Concept:** this is the half-open `[lo, hi)` *lower-bound* search: it returns the first "
                "index i with a[i] ≥ x (or len(a) if none). With duplicates it returns the **leftmost** "
                "occurrence.\n\n"
                "- `lb(A, 4)`: first element ≥ 4 is A[1] = 4 → **1**. (Trace: lo,hi = 0,8 → mid 4 (7 ≥ 4) "
                "hi = 4 → mid 2 (4) hi = 2 → mid 1 (4) hi = 1 → mid 0 (2 < 4) lo = 1 → stop.)\n"
                "- `lb(A, 9)`: first element ≥ 9 is A[5] → 5. `lb(A, 8)`: 8 is absent; first element ≥ 8 "
                "is also A[5] → 5. Difference **0** — tells us 8 does not occur (count of 8 = "
                "lb(8 + 1) − lb(8) = 0).\n"
                "- `lb(A, 13)`: every element < 13 → returns len(A) = **8**.\n\n"
                "Output `1 0 8`.\n\n"
                "**Options:** (A) returns the *last* occurrence of 4 (upper bound − 1) and counts 9s. "
                "(B) clamps to the last index 7. (D) returns the middle 4.\n\n"
                "**Tip:** lower bound never reads a[len(a)] because mid < hi always holds."
            ),
            "verify": "assert OUTPUT.split() == ['1', '0', '8'] and ANSWER == 'C'",
        },
        # ------------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Selection sort — stability",
            "text": ("The records (3, a), (1, b), (3, c), (2, d), (1, e) are sorted by their numeric key "
                     "using swap-based selection sort: in pass i the record with the minimum key in "
                     "positions i..n−1 is found (scanning left to right and replacing the current minimum "
                     "only on a strictly smaller key) and swapped with position i. Reading only the letters, "
                     "the final order is"),
            "options": ["b e d a c", "b e d c a", "e b d c a", "e b d a c"],
            "answer": "B",
            "solution": (
                "**Concept:** swap-based selection sort is **not stable** — the long-distance swap can jump "
                "a record over another with the same key.\n\n"
                "Trace (key-letter):\n"
                "- start: 3a 1b 3c 2d 1e\n"
                "- pass 0: min key 1, first at index 1 (1b) → swap with 3a → 1b 3a 3c 2d 1e\n"
                "- pass 1: min of 3a 3c 2d 1e is 1e (index 4) → swap with 3a → 1b 1e 3c 2d 3a\n"
                "- pass 2: min of 3c 2d 3a is 2d → swap with 3c → 1b 1e 2d 3c 3a\n"
                "- pass 3: 3c vs 3a — not strictly smaller → no change.\n\n"
                "Final letters: **b e d c a**.\n\n"
                "The two 1s kept their order (b before e), but the 3s were reversed: a was originally "
                "before c, and pass 1 threw 3a to the end.\n\n"
                "**Options:** (A) is the stable result (insertion sort or merge sort would give it). "
                "(C)/(D) reverse b and e, which never happens here.\n\n"
                "**Trap:** concluding stability from the fact that *some* equal keys stayed in order."
            ),
            "verify": '''
R = [(3,'a'),(1,'b'),(3,'c'),(2,'d'),(1,'e')]
for i in range(len(R) - 1):
    m = i
    for j in range(i + 1, len(R)):
        if R[j][0] < R[m][0]: m = j
    R[i], R[m] = R[m], R[i]
assert ["b e d a c", "b e d c a", "e b d c a", "e b d a c"]["ABCD".index(ANSWER)] == " ".join(x[1] for x in R)
''',
        },
        # ------------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Topological sorting — counting orders",
            "text": "The number of distinct topological orderings of the DAG shown below is ______.",
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"], ["C", "E"], ["D", "F"],
                                    ["E", "F"], ["G", "E"], ["F", "H"], ["G", "H"]],
                          "pos": {"A": [0, 2], "B": [2, 3], "C": [2, 1], "D": [4, 3], "E": [4, 1],
                                  "F": [6, 2], "G": [2, -0.5], "H": [8, 1]}}],
            "answer": "21",
            "solution": (
                "**Concept:** first identify vertices whose position is forced, then count the linear "
                "extensions of the remaining partial order by inserting the 'loose' vertices one at a time.\n\n"
                "**Forced tail.** F needs D and E; D needs A, B, C; E needs C, G. So all of A, B, C, D, E, G "
                "precede F, and H (needing F and G) comes after F. Hence every order ends **…, F, H**.\n\n"
                "**Orders of {A, B, C, D, E} without G.** A is the only source; then B < D, C < D, C < E:\n"
                "- A B C D E, A B C E D, A C B D E, A C B E D, A C E B D → 5 orders.\n\n"
                "**Insert G** (only constraint G < E): G may go in any slot before E. If E is at "
                "position p (1-based) among the five, there are p slots.\n"
                "- A B C D E (p = 5) → 5\n"
                "- A B C E D (p = 4) → 4\n"
                "- A C B D E (p = 5) → 5\n"
                "- A C B E D (p = 4) → 4\n"
                "- A C E B D (p = 3) → 3\n\n"
                "Total = 5 + 4 + 5 + 4 + 3 = **21**.\n\n"
                "**Trap:** treating G as completely free (it is a source) and multiplying by 6 positions "
                "(giving 30) — G must still precede E."
            ),
            "verify": '''
import itertools
E = [('A','B'),('A','C'),('B','D'),('C','D'),('C','E'),('D','F'),('E','F'),('G','E'),('F','H'),('G','H')]
cnt = 0
for p in itertools.permutations("ABCDEFGH"):
    pos = {v: i for i, v in enumerate(p)}
    cnt += all(pos[u] < pos[v] for u, v in E)
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q12
        {
            "type": "MCQ", "marks": 2, "topic": "Topological sorting — Kahn's algorithm with a min-heap",
            "text": ("Kahn's algorithm is run on the DAG below, but the set of vertices with in-degree 0 is "
                     "kept in a **min-priority queue** keyed on the vertex label, so the alphabetically "
                     "smallest available vertex is always output next. The output order is"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["H", "A"], ["H", "C"], ["B", "A"], ["B", "D"], ["A", "E"], ["C", "E"],
                                    ["D", "F"], ["E", "G"], ["F", "G"], ["C", "F"]],
                          "pos": {"B": [0, 3], "H": [0, 1], "D": [2, 4], "A": [2, 2.5], "C": [2, 0.5],
                                  "F": [4, 3.5], "E": [4, 1], "G": [6, 2.2]}}],
            "options": [
                "B, H, D, A, C, E, F, G",
                "B, D, H, A, C, E, F, G",
                "B, D, H, A, C, F, E, G",
                "H, B, A, C, D, E, F, G",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** with a min-heap, Kahn's algorithm outputs the **lexicographically smallest** "
                "topological order: at each step it takes the smallest label among the current sources.\n\n"
                "In-degrees: A 2 (H, B), C 1 (H), D 1 (B), E 2 (A, C), F 2 (D, C), G 2 (E, F); B, H 0.\n\n"
                "Trace (heap contents → output):\n"
                "- {B, H} → output **B**; A → 1, D → 0. Heap {D, H}.\n"
                "- {D, H} → output **D**; F → 1. Heap {H}.\n"
                "- {H} → output **H**; A → 0, C → 0. Heap {A, C}.\n"
                "- output **A**; E → 1. Heap {C}.\n"
                "- output **C**; E → 0, F → 0. Heap {E, F}.\n"
                "- output **E**; G → 1. Then **F**; G → 0. Then **G**.\n\n"
                "Order: **B, D, H, A, C, E, F, G** → (B).\n\n"
                "**Options:**\n"
                "- (A) is what a FIFO queue gives (B, H were both initially available, so H precedes the "
                "newly freed D).\n"
                "- (C) is a valid topological order but not the smallest: after C, both E and F are "
                "available and E < F.\n"
                "- (D) is also a valid topological order, but it starts with H although B is smaller.\n\n"
                "**Trap:** confusing 'smallest available' with 'FIFO among sources'."
            ),
            "verify": '''
import heapq
V = "ABCDEFGH"
E = [('H','A'),('H','C'),('B','A'),('B','D'),('A','E'),('C','E'),('D','F'),('E','G'),('F','G'),('C','F')]
indeg = {v: 0 for v in V}
for u, v in E: indeg[v] += 1
h = [v for v in V if indeg[v] == 0]; heapq.heapify(h); out = []
while h:
    u = heapq.heappop(h); out.append(u)
    for x, v in E:
        if x == u:
            indeg[v] -= 1
            if indeg[v] == 0: heapq.heappush(h, v)
assert ", ".join(out) == "B, D, H, A, C, E, F, G" and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "DFS on a DAG — timestamps and topological order",
            "text": ("DFS is run on the DAG below with the same conventions as Q.4 (outer loop and adjacency "
                     "lists in alphabetical order; one clock starting at 1, ticking at every discovery and "
                     "finish). Let d[v] and f[v] be the discovery and finish times. Which of the following "
                     "statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                          "edges": [["A", "B"], ["A", "D"], ["B", "C"], ["B", "E"], ["D", "E"], ["E", "C"],
                                    ["F", "D"], ["F", "G"], ["G", "E"]],
                          "pos": {"A": [0, 2], "B": [2, 2], "C": [4, 2], "D": [2, 0], "E": [4, 0],
                                  "F": [0, 0], "G": [3, -1.5]}}],
            "options": [
                "d[E] = 5 and f[E] = 6",
                "(D, E) is a back edge",
                "Listing the vertices in decreasing order of finish time gives F, G, A, D, B, E, C, "
                "which is a topological order",
                "The DFS classifies exactly 3 edges as cross edges",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept:** in a DAG, DFS never finds a back edge, and for every edge u → v we have "
                "f[u] > f[v]; hence sorting by decreasing finish time is a topological order.\n\n"
                "Trace:\n"
                "- A(1) → B(2) → C(3), C finishes (4). B → E: E(5); E → C finished → cross; E finishes (6). "
                "B finishes (7).\n"
                "- A → D(8); D → E finished, d[D] = 8 > d[E] = 5 → **cross**; D finishes (9). A finishes (10).\n"
                "- Restart F(11): F → D finished → cross. F → G(12); G → E → cross; G finishes (13). "
                "F finishes (14).\n\n"
                "Times: A 1/10, B 2/7, C 3/4, D 8/9, E 5/6, F 11/14, G 12/13.\n\n"
                "**Verdicts:**\n"
                "- (A) **True.**\n"
                "- (B) **False** — E was already finished; a DAG has no back edges at all.\n"
                "- (C) decreasing f: F 14, G 13, A 10, D 9, B 7, E 6, C 4 → F, G, A, D, B, E, C. Every edge "
                "goes left to right. **True.**\n"
                "- (D) cross edges: E→C, D→E, F→D, G→E → **4**, not 3. **False.** (Tree edges: A→B, B→C, "
                "B→E, A→D, F→G.)\n\n"
                "**Trap:** in (D), forgetting that edges from a later DFS tree into an earlier one "
                "(F→D, G→E) are cross edges too."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Discovery / finish times",
                                   "col_labels": ["A", "B", "C", "D", "E", "F", "G"],
                                   "row_labels": ["d", "f"],
                                   "rows": [[1, 2, 3, 8, 5, 11, 12], [10, 7, 4, 9, 6, 14, 13]]}],
            "verify": '''
V = "ABCDEFG"
E = [('A','B'),('A','D'),('B','C'),('B','E'),('D','E'),('E','C'),('F','D'),('F','G'),('G','E')]
G = {v: sorted(w for u, w in E if u == v) for v in V}
d, f, t, cls = {}, {}, [1], {}
def dfs(u):
    d[u] = t[0]; t[0] += 1
    for v in G[u]:
        if v not in d:
            cls[(u, v)] = 'tree'; dfs(v)
        elif v not in f: cls[(u, v)] = 'back'
        elif d[u] < d[v]: cls[(u, v)] = 'forward'
        else: cls[(u, v)] = 'cross'
    f[u] = t[0]; t[0] += 1
for v in V:
    if v not in d: dfs(v)
order = sorted(V, key=lambda v: -f[v])
pos = {v: i for i, v in enumerate(order)}
truth = [(d['E'], f['E']) == (5, 6), cls[('D','E')] == 'back',
         order == list("FGADBEC") and all(pos[u] < pos[v] for u, v in E),
         sum(c == 'cross' for c in cls.values()) == 3]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "DAGs — longest (critical) path via topological order",
            "text": ("In the weighted DAG below, an edge weight is the duration of an activity; a vertex can "
                     "start only after all its incoming activities are complete. The length of the longest "
                     "path from S to T (the minimum completion time of the project) is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E", "T"],
                          "edges": [["S", "A", 3], ["S", "B", 2], ["A", "C", 4], ["A", "D", 2], ["B", "D", 6],
                                    ["D", "C", 1], ["D", "E", 4], ["B", "E", 3], ["C", "T", 3], ["E", "T", 2]],
                          "pos": {"S": [0, 1.5], "A": [2, 3], "B": [2, 0], "C": [5, 3], "D": [3.5, 1.5],
                                  "E": [5, 0], "T": [7, 1.5]}}],
            "answer": "14",
            "solution": (
                "**Concept:** longest paths are NP-hard in general graphs, but in a DAG we can process "
                "vertices in topological order with L(v) = max over edges u → v of L(u) + w(u, v).\n\n"
                "Topological order: S, A, B, D, C, E, T.\n"
                "- L(S) = 0\n"
                "- L(A) = 0 + 3 = 3\n"
                "- L(B) = 0 + 2 = 2\n"
                "- L(D) = max(L(A) + 2, L(B) + 6) = max(5, 8) = 8\n"
                "- L(C) = max(L(A) + 4, L(D) + 1) = max(7, 9) = 9\n"
                "- L(E) = max(L(D) + 4, L(B) + 3) = max(12, 5) = 12\n"
                "- L(T) = max(L(C) + 3, L(E) + 2) = max(12, 14) = **14**\n\n"
                "Critical path: S → B → D → E → T (2 + 6 + 4 + 2 = 14).\n\n"
                "**Trap:** following the locally heaviest first edge (S → A, weight 3) leads at best to 11 (S → A → D → E → T); "
                "also, running a shortest-path algorithm gives the *earliest* arrival along the cheapest "
                "route (S → A → C → T = 10), which is not the project completion time."
            ),
            "solution_diagrams": [{"type": "graph", "directed": True,
                                   "nodes": ["S", "A", "B", "C", "D", "E", "T"],
                                   "edges": [["S", "A", 3], ["S", "B", 2], ["A", "C", 4], ["A", "D", 2],
                                             ["B", "D", 6], ["D", "C", 1], ["D", "E", 4], ["B", "E", 3],
                                             ["C", "T", 3], ["E", "T", 2]],
                                   "pos": {"S": [0, 1.5], "A": [2, 3], "B": [2, 0], "C": [5, 3],
                                           "D": [3.5, 1.5], "E": [5, 0], "T": [7, 1.5]},
                                   "highlight_edges": [["S", "B"], ["B", "D"], ["D", "E"], ["E", "T"]],
                                   "caption": "Critical path S → B → D → E → T"}],
            "verify": '''
W = [('S','A',3),('S','B',2),('A','C',4),('A','D',2),('B','D',6),('D','C',1),('D','E',4),
     ('B','E',3),('C','T',3),('E','T',2)]
L = {'S': 0}
for v in "ABDCET":
    L[v] = max(L[u] + w for u, x, w in W if x == v)
assert L['T'] == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Cycle detection — Kahn's algorithm in Python",
            "text": "Consider the following Python program. What is printed?",
            "code": '''from collections import deque

G = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d', 'e'],
     'd': ['f'], 'e': ['f', 'g'], 'f': ['e'], 'g': []}
indeg = {v: 0 for v in G}
for u in G:
    for v in G[u]:
        indeg[v] += 1
q = deque(v for v in G if indeg[v] == 0)
order = []
while q:
    u = q.popleft()
    order.append(u)
    for v in G[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
print(''.join(order), sum(indeg.values()))''',
            "options": ["`abcdefg 0`", "`abcd 2`", "`acbd 3`", "`abcd 3`"],
            "answer": "D",
            "solution": (
                "**Concept:** Kahn's algorithm removes vertices of in-degree 0. If the graph has a cycle, "
                "the vertices on the cycle (and everything reachable only through it) never reach "
                "in-degree 0, so fewer than |V| vertices are output — this is how Kahn detects cycles.\n\n"
                "Initial in-degrees: a 0, b 1, c 1, d 2, e 2 (from c and f), f 2 (from d and e), g 1.\n\n"
                "Trace:\n"
                "- q = [a] → output a; b → 0, c → 0 → q = [b, c]\n"
                "- output b; d → 1\n"
                "- output c; d → 0 (enqueue), e → 1\n"
                "- output d; f → 1\n"
                "- queue empty. e and f each still have in-degree 1 (they wait on each other: e → f → e "
                "is a cycle) and g has in-degree 1 (waiting on e).\n\n"
                "`order` = abcd; remaining in-degree sum = 1 + 1 + 1 = **3**. Output `abcd 3`.\n\n"
                "**Options:** (A) ignores the cycle e ⇄ f. (B) forgets that g is blocked as well — it is not "
                "on the cycle but depends on it. (C) uses a stack-like order; the deque is FIFO.\n\n"
                "**Tip:** `len(order) < len(G)` ⇔ the directed graph contains a cycle."
            ),
            "solution_diagrams": [{"type": "graph", "directed": True,
                                   "nodes": ["a", "b", "c", "d", "e", "f", "g"],
                                   "edges": [["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"], ["c", "e"],
                                             ["d", "f"], ["e", "f"], ["f", "e"], ["e", "g"]],
                                   "pos": {"a": [0, 1], "b": [2, 2], "c": [2, 0], "d": [4, 2], "e": [4, 0],
                                           "f": [6, 1], "g": [6, -1]},
                                   "highlight": ["e", "f", "g"],
                                   "caption": "Highlighted vertices are never output (e ⇄ f is a cycle; g waits on e)"}],
            "verify": "assert OUTPUT.strip() == 'abcd 3' and ANSWER == 'D'",
        },
        # ------------------------------------------------------------------ Q16
        {
            "type": "MCQ", "marks": 2, "topic": "Merge sort — worst-case comparison recurrence",
            "text": ("The worst-case number of key comparisons made by top-down merge sort on n elements "
                     "satisfies T(1) = 0 and T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + n − 1 for n ≥ 2. The value of T(13) is"),
            "options": ["33", "49", "52", "37"],
            "answer": "D",
            "solution": (
                "**Concept:** merging lists of total length m costs at most m − 1 comparisons; the recurrence "
                "adds this over the recursion tree. Closed form: T(n) = n⌈log₂ n⌉ − 2^{⌈log₂ n⌉} + 1.\n\n"
                "Bottom-up evaluation:\n"
                "- T(2) = T(1) + T(1) + 1 = 1\n"
                "- T(3) = T(1) + T(2) + 2 = 3\n"
                "- T(4) = T(2) + T(2) + 3 = 5\n"
                "- T(6) = T(3) + T(3) + 5 = 11\n"
                "- T(7) = T(3) + T(4) + 6 = 14\n"
                "- T(13) = T(6) + T(7) + 12 = 11 + 14 + 12 = **37**\n\n"
                "Check with the closed form: ⌈log₂ 13⌉ = 4 → 13·4 − 16 + 1 = 37. ✓\n\n"
                "**Options:**\n"
                "- (A) 33 under-counts (e.g. uses ⌊n/2⌋ for both halves).\n"
                "- (B) 49 uses n instead of n − 1 per merge.\n"
                "- (C) 52 = n⌈log₂ n⌉ is only an upper bound.\n\n"
                "**Tip:** for n a power of 2, T(n) = n log₂ n − n + 1 (e.g. T(8) = 17)."
            ),
            "verify": '''
from functools import lru_cache
@lru_cache(None)
def T(n): return 0 if n <= 1 else T(n // 2) + T((n + 1) // 2) + n - 1
@lru_cache(None)
def T2(n): return 0 if n <= 1 else T2(n // 2) + T2((n + 1) // 2) + n
opts = [33, 49, 52, 37]
assert opts["ABCD".index(ANSWER)] == T(13) == 13*4 - 16 + 1 and T2(13) == 49 and T(8) == 17
''',
        },
        # ------------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Shortest paths in a DAG with a negative edge",
            "text": ("Consider the weighted DAG below (note the negative edge B → A). Which of the following "
                     "statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "T"],
                          "edges": [["S", "A", 2], ["S", "B", 5], ["B", "A", -4], ["A", "C", 4],
                                    ["C", "T", 1], ["B", "T", 6]],
                          "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 2], "T": [6, 1]}}],
            "options": [
                "Relaxing edges in topological order gives the shortest distance S → T as 6",
                "Dijkstra's algorithm, in an implementation where a vertex once extracted is never updated "
                "again, reports the distance S → T as 7",
                "Adding 4 to every edge weight (making all weights non-negative) and running Dijkstra "
                "returns a path that is also a shortest S → T path in the original graph",
                "The DAG has exactly 2 topological orderings",
            ],
            "answer": ["A", "B"],
            "solution": (
                "**Concept:** in a DAG, relaxing the out-edges of each vertex in topological order computes "
                "correct shortest paths in Θ(V + E) even with negative weights. Dijkstra's greedy choice "
                "fails with negative edges. Adding a constant to every edge penalises paths with more "
                "edges, so it does not preserve shortest paths.\n\n"
                "- (A) Topological order (unique): S, B, A, C, T. d(S) = 0; from S: A = 2, B = 5; from B: "
                "A = min(2, 5 − 4) = 1, T = 11; from A: C = 5; from C: T = min(11, 6) = **6**. **True.**\n"
                "- (B) Dijkstra: extract S → A = 2, B = 5. Extract A (2) → C = 6. Extract B (5): A is already "
                "final, so the improvement to 1 is lost; T = 11. Extract C (6) → T = 7. Extract T → **7**. "
                "**True** (and wrong — the real distance is 6).\n"
                "- (C) New weights: S→A 6, S→B 9, B→A 0, A→C 8, C→T 5, B→T 10. Path costs: S–A–C–T 19, "
                "S–B–T 19, S–B–A–C–T 22. Dijkstra returns a 3-edge path or S–B–T, both of original cost 7, "
                "but the true shortest is S–B–A–C–T (cost 6). **False.**\n"
                "- (D) S must be first; B → A forces B before A; then C, then T: only S, B, A, C, T. "
                "**False.**\n\n"
                "**Trap:** believing that 'shifting all weights to be non-negative' fixes Dijkstra."
            ),
            "verify": '''
import heapq
E = [('S','A',2),('S','B',5),('B','A',-4),('A','C',4),('C','T',1),('B','T',6)]
def dag_sp(E, order):
    d = {v: float('inf') for v in order}; d['S'] = 0
    for u in order:
        for x, v, w in E:
            if x == u and d[u] + w < d[v]: d[v] = d[u] + w
    return d
dA = dag_sp(E, "SBACT")['T']
def dijk(E):
    d = {v: float('inf') for v in "SABCT"}; d['S'] = 0; done = set(); pq = [(0, 'S')]; par = {}
    while pq:
        du, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u)
        for x, v, w in E:
            if x == u and v not in done and du + w < d[v]:
                d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
    p, v = ['T'], 'T'
    while v != 'S':
        v = par[v]; p.append(v)
    return d['T'], p[::-1]
dB, _ = dijk(E)
E4 = [(u, v, w + 4) for u, v, w in E]
_, path = dijk(E4)
orig = sum(w for i in range(len(path) - 1) for u, v, w in E if (u, v) == (path[i], path[i+1]))
import itertools
ntopo = sum(1 for p in itertools.permutations("SABCT")
            if all(p.index(u) < p.index(v) for u, v, w in E))
truth = [dA == 6, dB == 7, orig == dA, ntopo == 2]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Heaps — counting distinct max-heaps",
            "text": ("The number of distinct binary max-heaps (stored as complete binary trees / arrays) that "
                     "can be formed using all of the keys 1, 2, 3, 4, 5, 6, 7, 8 exactly once is ______."),
            "diagrams": [{"type": "heap", "values": ["8", "·", "·", "·", "·", "·", "·", "·"],
                          "caption": "Shape of every 8-node heap (root must be 8)"}],
            "answer": "210",
            "solution": (
                "**Concept:** the shape of an n-node heap is fixed. The root must hold the maximum; the "
                "remaining n − 1 keys are split between the left subtree (size L) and right subtree (size R) "
                "in C(n − 1, L) ways, and each subtree is independently a heap:\n"
                "H(n) = C(n − 1, L) · H(L) · H(R).\n\n"
                "Subtree sizes for an 8-node complete tree: levels hold 1, 2, 4, 1 nodes; the single node on "
                "the last level is under the left child. So L = 1 + 2 + 1 = 4, R = 3.\n\n"
                "- H(1) = 1, H(2) = 1 (the larger key must be the root).\n"
                "- H(3) = C(2, 1) · 1 · 1 = 2.\n"
                "- H(4): L = 2, R = 1 → C(3, 2) · H(2) · H(1) = 3.\n"
                "- H(8) = C(7, 4) · H(4) · H(3) = 35 · 3 · 2 = **210**.\n\n"
                "**Trap:** taking L = R = 3.5 (impossible) or L = 3, R = 4 — in a complete binary tree the "
                "*left* subtree is filled first. With L = 3, R = 4 the formula gives the same number here "
                "by symmetry of C(7, ·), but the sub-shapes matter in general (e.g. H(6) = 20, H(7) = 80)."
            ),
            "verify": '''
import itertools
def is_heap(a):
    return all(a[(i - 1) // 2] > a[i] for i in range(1, len(a)))
cnt = sum(1 for p in itertools.permutations(range(1, 9)) if p[0] == 8 and is_heap(p))
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q19
        {
            "type": "MSQ", "marks": 2, "topic": "Python — closures, nonlocal and late binding",
            "text": ("Consider the following Python program, which prints four integers separated by spaces. "
                     "Which of the following statements is/are TRUE?"),
            "code": '''def counter():
    n = 0
    def inc(k=1):
        nonlocal n
        n += k
        return n
    return inc

f, g = counter(), counter()
f(); f(5); g(2)
adders = [lambda x: x + i for i in range(3)]
muls = [lambda x, i=i: x * i for i in range(3)]
print(f(), g(), adders[0](10), muls[2](10))''',
            "options": [
                "The first number printed is 7",
                "The second number printed is 8",
                "The third number printed is 10",
                "The fourth number printed is 20",
            ],
            "answer": ["A", "D"],
            "solution": (
                "**Concept:** each call to `counter()` creates a fresh cell for `n`; `nonlocal` rebinds that "
                "cell. A lambda captures a *variable*, not its current value, so lambdas made in a loop see "
                "the variable's final value (late binding) — unless the value is frozen with a default "
                "argument `i=i`.\n\n"
                "- `f`: f() → 1, f(5) → 6, then `f()` in the print → **7**.\n"
                "- `g` has its own n: g(2) → 2, then `g()` → **3** (not shared with f).\n"
                "- `adders[0](10)`: the comprehension's `i` ends at 2 → 10 + 2 = **12**.\n"
                "- `muls[2](10)`: default i = 2 was stored when the lambda was created → 10 × 2 = **20**.\n\n"
                "Output: `7 3 12 20`.\n\n"
                "**Verdicts:** (A) **True**. (B) **False** — 8 would require f and g to share n. "
                "(C) **False** — 10 assumes early binding of i = 0. (D) **True.**\n\n"
                "**Trap:** the comprehension has its own scope in Python 3, but the closure still refers to "
                "that scope's single `i`, which ends at 2."
            ),
            "verify": '''
assert OUTPUT.split() == ['7', '3', '12', '20']
vals = [7, 3, 12, 20]; claims = [7, 8, 10, 20]
assert sorted(ANSWER) == [c for c, a, b in zip("ABCD", vals, claims) if a == b]
''',
        },
        # ------------------------------------------------------------------ Q20
        {
            "type": "NAT", "marks": 2, "topic": "DAGs — counting paths with memoised recursion",
            "text": ("The program below stores a DAG as a dictionary in which each value is a string of "
                     "successor labels (the DAG is drawn below). The value printed is ______."),
            "code": '''from functools import lru_cache

G = {'s': 'abc', 'a': 'bd', 'b': 'de', 'c': 'be',
     'd': 'ft', 'e': 'dft', 'f': 't', 't': ''}

@lru_cache(maxsize=None)
def paths(u):
    if u == 't':
        return 1
    return sum(paths(v) for v in G[u])

print(paths('s'))''',
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["s", "a", "b", "c", "d", "e", "f", "t"],
                          "edges": [["s", "a"], ["s", "b"], ["s", "c"], ["a", "b"], ["a", "d"], ["b", "d"],
                                    ["b", "e"], ["c", "b"], ["c", "e"], ["d", "f"], ["d", "t"], ["e", "d"],
                                    ["e", "f"], ["e", "t"], ["f", "t"]],
                          "pos": {"s": [0, 2], "a": [2, 4], "b": [2, 2], "c": [2, 0], "d": [4, 3.5],
                                  "e": [4, 0.5], "f": [6, 2], "t": [8, 2]}}],
            "answer": "24",
            "solution": (
                "**Concept:** the number of s–t paths in a DAG satisfies P(t) = 1 and "
                "P(u) = Σ P(v) over successors v; memoisation evaluates each vertex once (8 calls in all), "
                "turning an exponential enumeration into O(V + E). Iterating over a string iterates over "
                "its characters, so `G['s']` = 'abc' means successors a, b, c.\n\n"
                "Evaluate in reverse topological order:\n"
                "- P(t) = 1\n"
                "- P(f) = P(t) = 1\n"
                "- P(d) = P(f) + P(t) = 2\n"
                "- P(e) = P(d) + P(f) + P(t) = 2 + 1 + 1 = 4\n"
                "- P(b) = P(d) + P(e) = 2 + 4 = 6\n"
                "- P(a) = P(b) + P(d) = 6 + 2 = 8\n"
                "- P(c) = P(b) + P(e) = 6 + 4 = 10\n"
                "- P(s) = P(a) + P(b) + P(c) = 8 + 6 + 10 = **24**\n\n"
                "**Trap:** counting *vertices* reachable or *edges* instead of paths, or forgetting the direct "
                "edges d → t and e → t. Without `lru_cache` the answer is the same but P(b), P(d), … are "
                "recomputed many times."
            ),
            "verify": '''
assert int(OUTPUT) == int(ANSWER)
import itertools
def count(u):
    return 1 if u == 't' else sum(count(v) for v in G[u])
assert count('s') == 24
''',
        },
    ],
}
