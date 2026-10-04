# Set 28 — Connectivity & Bipartiteness (GATE-level)
SET = {
    "number": 28,
    "title": "Connectivity & Bipartiteness",
    "difficulty": "GATE-level",
    "focus": "components, bridges/cut vertices intuition, bipartite checks, cycles",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "NAT", "marks": 1, "topic": "Graph theory — connected components",
            "text": ("A simple undirected graph G has vertex set {0, 1, 2, …, 29}. Two distinct vertices "
                     "i and j are adjacent if and only if |i − j| = 12 or |i − j| = 18. The number of "
                     "connected components of G is ______."),
            "answer": "6",
            "solution": (
                "Every edge changes a vertex label by 12 or 18, both multiples of gcd(12, 18) = 6. So "
                "i mod 6 is **invariant** along any path: vertices with different residues mod 6 can "
                "never be connected → at least 6 components.\n\n"
                "Now check that each residue class is connected. Class r = {r, r+6, r+12, r+18, r+24} "
                "(r = 0..5, five vertices each):\n"
                "- r — r+12 — r+24 (steps of 12)\n"
                "- r — r+18 (step 18) and r+6 — r+18 (step 12), r+6 — r+24 (step 18)\n"
                "So r, r+6, r+12, r+18, r+24 are all linked: e.g. r → r+18 → r+6 → r+24 → r+12.\n\n"
                "Hence exactly **6** components, each with 5 vertices.\n\n"
                "**Trap:** answering gcd-based counts blindly. On a *finite path* of labels (not a "
                "cycle) a class could split if the steps overshoot the range — here 30 labels are "
                "enough for every class to stay connected, but always verify one class explicitly."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["0", "6", "12", "18", "24"],
                                   "edges": [["0", "12"], ["12", "24"], ["0", "18"], ["6", "18"],
                                             ["6", "24"]],
                                   "pos": {"0": [0, 1], "6": [1.5, 0], "12": [3, 1], "18": [1.5, 2],
                                           "24": [4.5, 0]},
                                   "caption": "Component of residue class 0 (others are identical shifts)"}],
            "verify": '''
p = list(range(30))
def f(x):
    while p[x] != x: x = p[x]
    return x
for i in range(30):
    for j in range(i+1, 30):
        if j - i in (12, 18): p[f(i)] = f(j)
assert len({f(i) for i in range(30)}) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "MCQ", "marks": 1, "topic": "Union–find with path halving",
            "text": "Consider the following Python program. What is printed?",
            "code": '''parent = list(range(8))

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

for a, b in [(0, 1), (2, 3), (1, 3), (4, 5), (6, 5), (0, 2)]:
    union(a, b)
print(parent[:4], len({find(i) for i in range(8)}))''',
            "options": ["`[1, 3, 3, 3] 3`", "`[3, 3, 3, 3] 3`", "`[3, 3, 3, 3] 4`", "`[1, 3, 3, 3] 4`"],
            "answer": "B",
            "solution": (
                "`find` uses **path halving**: each visited node is re-pointed to its grandparent, "
                "flattening the tree as a side-effect of a query.\n\n"
                "- union(0,1): roots 0, 1 → parent[0] = 1.\n"
                "- union(2,3): parent[2] = 3.\n"
                "- union(1,3): roots 1, 3 → parent[1] = 3. Now 0 → 1 → 3.\n"
                "- union(4,5): parent[4] = 5;  union(6,5): parent[6] = 5.\n"
                "- union(0,2): find(0): parent[0] ≠ 0, so parent[0] = parent[parent[0]] = parent[1] "
                "= 3, x = 3 → root 3. find(2) = 3. Same root → no link, but parent[0] has been "
                "**changed to 3** by the halving step.\n\n"
                "parent[:4] = [3, 3, 3, 3]. The sets are {0,1,2,3}, {4,5,6}, {7} → 3 components.\n"
                "Output `[3, 3, 3, 3] 3` → option **(B)**.\n\n"
                "- (A) ignores the compression done by the redundant union(0,2).\n"
                "- (C)/(D) miscount components (vertex 7 is a singleton, 4–5–6 is one set).\n\n"
                "**Trap:** a `find` call is not read-only — even a union that does nothing can modify "
                "`parent`."
            ),
            "verify": "assert OUTPUT.strip() == '[3, 3, 3, 3] 3' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Bipartite graphs — parity argument",
            "text": ("For a set D of positive integers, let G_{D} be the graph on vertices {1, 2, …, 12} in "
                     "which distinct i and j are adjacent iff |i − j| ∈ D. For which of the following "
                     "choices of D is G_{D} bipartite?"),
            "options": ["D = {1, 3}", "D = {2, 3}", "D = {2, 4}", "D = {3, 5}"],
            "answer": ["A", "D"],
            "solution": (
                "A graph is bipartite iff it has no odd cycle.\n\n"
                "- If every d ∈ D is **odd**, each edge joins an odd label to an even label, so the "
                "parity of the label is a valid 2-colouring → bipartite.\n"
                "- Otherwise look for an odd cycle: a closed walk uses steps ±d whose signed sum is 0; "
                "an odd number of steps with sum 0 gives an odd closed walk, hence an odd cycle.\n\n"
                "Options:\n"
                "- (A) {1, 3}: both odd → **bipartite**.\n"
                "- (B) {2, 3}: 2 + 2 + 2 − 3 − 3 = 0 uses 5 steps: 1 → 3 → 5 → 7 → 4 → 1 is a "
                "5-cycle → **not bipartite**.\n"
                "- (C) {2, 4}: 2 + 2 − 4 = 0 uses 3 steps: 1 → 3 → 5 → 1 is a triangle → **not "
                "bipartite** (all edges stay within one parity class, but that does not help).\n"
                "- (D) {3, 5}: both odd → **bipartite**.\n\n"
                "**Trap:** in (C) the graph splits into an 'odd' and an 'even' component, which looks "
                "bipartite-like, but each component contains triangles."
            ),
            "verify": '''
def bip(D, n=12):
    col = {}
    for s in range(1, n+1):
        if s in col: continue
        col[s] = 0; st = [s]
        while st:
            u = st.pop()
            for d in D:
                for v in (u-d, u+d):
                    if 1 <= v <= n:
                        if v not in col: col[v] = 1 - col[u]; st.append(v)
                        elif col[v] == col[u]: return False
    return True
opts = {'A': (1,3), 'B': (2,3), 'C': (2,4), 'D': (3,5)}
assert sorted(k for k, D in opts.items() if bip(D)) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Connectivity — bridges",
            "text": ("A *bridge* is an edge whose removal increases the number of connected components. "
                     "The number of bridges in the undirected graph shown is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                          "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"], ["D", "E"],
                                    ["E", "F"], ["F", "G"], ["G", "D"], ["G", "H"], ["H", "I"],
                                    ["H", "J"], ["I", "J"], ["F", "K"]],
                          "pos": {"A": [0, 2], "B": [0, 0], "C": [1.2, 1], "D": [2.6, 1],
                                  "E": [3.6, 2], "F": [4.6, 1], "G": [3.6, 0], "H": [4.8, -0.8],
                                  "I": [6, 0], "J": [6, -1.6], "K": [6, 2]}}],
            "answer": "3",
            "solution": (
                "An edge is a bridge **iff it lies on no cycle**. So identify the cycles and the edges "
                "outside them.\n\n"
                "- Triangle A–B–C: its 3 edges are on a cycle → not bridges.\n"
                "- 4-cycle D–E–F–G–D: 4 edges, not bridges.\n"
                "- Triangle H–I–J: 3 edges, not bridges.\n"
                "- Remaining edges: **C–D** (joins the triangle to the square), **G–H** (joins the "
                "square to the second triangle), **F–K** (pendant edge to the leaf K). None of these "
                "lies on a cycle.\n\n"
                "Number of bridges = **3**.\n\n"
                "Check: the graph has 11 vertices and 13 edges; contracting each of the three cycles "
                "to a single node leaves a tree on 4 nodes (the three cycles plus K), whose 3 edges "
                "are exactly the bridges.\n\n"
                "**Trap:** counting cut **vertices** (C, D, F, G, H — five of them) instead of bridges. "
                "Every bridge with a non-leaf endpoint gives cut vertices, but the counts differ."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                                   "edges": [["A", "B"], ["B", "C"], ["C", "A"], ["C", "D"], ["D", "E"],
                                             ["E", "F"], ["F", "G"], ["G", "D"], ["G", "H"], ["H", "I"],
                                             ["H", "J"], ["I", "J"], ["F", "K"]],
                                   "pos": {"A": [0, 2], "B": [0, 0], "C": [1.2, 1], "D": [2.6, 1],
                                           "E": [3.6, 2], "F": [4.6, 1], "G": [3.6, 0], "H": [4.8, -0.8],
                                           "I": [6, 0], "J": [6, -1.6], "K": [6, 2]},
                                   "highlight_edges": [["C", "D"], ["G", "H"], ["F", "K"]],
                                   "caption": "Bridges highlighted"}],
            "verify": '''
N = "ABCDEFGHIJK"
E = [('A','B'),('B','C'),('C','A'),('C','D'),('D','E'),('E','F'),('F','G'),('G','D'),
     ('G','H'),('H','I'),('H','J'),('I','J'),('F','K')]
def comps(edges):
    p = {v: v for v in N}
    def f(x):
        while p[x] != x: x = p[x]
        return x
    for u, v in edges: p[f(u)] = f(v)
    return len({f(v) for v in N})
base = comps(E)
br = [e for e in E if comps([x for x in E if x != e]) > base]
assert len(br) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks — permutations",
            "text": ("The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack in this "
                     "order; pops may be interleaved arbitrarily with the pushes and each popped value is "
                     "printed. Which of the following output sequences is **NOT** possible?"),
            "options": ["3 2 4 1 6 5", "2 4 3 6 5 1", "4 3 5 1 2 6", "1 2 3 4 5 6"],
            "answer": "C",
            "solution": (
                "Simulate greedily: to output x, push until x is on top (if x has not been pushed "
                "yet), then pop; if x was pushed earlier it must be exactly the top, otherwise the "
                "sequence is impossible.\n\n"
                "- (A) push 1,2,3 → pop 3, pop 2; push 4 → pop 4; pop 1; push 5,6 → pop 6, pop 5. "
                "Valid.\n"
                "- (B) push 1,2 → pop 2; push 3,4 → pop 4, pop 3; push 5,6 → pop 6, pop 5; pop 1. "
                "Valid.\n"
                "- (C) push 1–4 → pop 4, pop 3; stack is [1, 2] (top 2). push 5 → pop 5. Next "
                "output must be 1, but the top is **2** → impossible.\n"
                "- (D) push/pop alternately. Valid.\n\n"
                "Answer **(C)**.\n\n"
                "**Tip:** a sequence is a valid stack permutation iff it has no pattern i < j < k "
                "printed in the order k, i, j (a '312' pattern). In (C): 3 … 1 … 2 is such a "
                "pattern."
            ),
            "solution_diagrams": [{"type": "stack", "values": [1, 2], "label": "S",
                                   "caption": "Stack in (C) when 1 is required — 2 blocks it"}],
            "verify": '''
def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x: st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = {'A':[3,2,4,1,6,5],'B':[2,4,3,6,5,1],'C':[4,3,5,1,2,6],'D':[1,2,3,4,5,6]}
assert [k for k, s in opts.items() if not ok(s)] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "NAT", "marks": 1, "topic": "BST — number of insertion orders",
            "text": ("The binary search tree shown is obtained by inserting its 8 keys, one at a time, "
                     "into an empty BST. The number of different insertion orders (permutations of the "
                     "8 keys) that produce exactly this tree is ______."),
            "diagrams": [{"type": "bintree",
                          "tree": [50, [30, [20], [40]], [70, [60], [80, None, [90]]]],
                          "caption": "Figure: target BST"}],
            "answer": "210",
            "solution": (
                "A permutation builds the tree iff every node is inserted **before all its "
                "descendants**. Equivalently, count recursively:\n"
                "ways(T) = C(|L| + |R|, |L|) × ways(L) × ways(R)\n"
                "(interleave any valid order of the left subtree with any valid order of the right "
                "subtree).\n\n"
                "- Subtree 30 {20, 40}: 30 first, then 20 and 40 in any order → C(2,1) = 2.\n"
                "- Subtree 80 {90}: 80 then 90 → 1.\n"
                "- Subtree 70: left {60} (1 node), right {80, 90} (2 nodes) → C(3,1) × 1 × 1 = 3.\n"
                "- Root 50: left has 3 nodes, right has 4 nodes → C(7,3) × 2 × 3 = 35 × 6 = **210**.\n\n"
                "Sanity check: 8! = 40320 permutations in total, and only 210 of them produce this "
                "shape.\n\n"
                "**Trap:** multiplying only the subtree counts (2 × 3 = 6) and forgetting the "
                "interleavings between left and right subtrees."
            ),
            "verify": '''
from itertools import permutations
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def build(seq):
    t = None
    for k in seq: t = ins(t, k)
    return t
target = build([50,30,20,40,70,60,80,90])
cnt = sum(1 for p in permutations([20,30,40,60,70,80,90]) if build((50,) + p) == target)
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — chaining",
            "text": ("The keys 5, 14, 22, 9, 31, 40, 17, 2 are inserted into a hash table with 9 slots "
                     "(0–8) using h(k) = (2k + 3) mod 9 and separate chaining. What are the length of the "
                     "longest chain and the number of empty slots, respectively?"),
            "options": ["3 and 4", "2 and 4", "3 and 3", "3 and 5"],
            "answer": "A",
            "solution": (
                "Compute h(k) = (2k + 3) mod 9 for each key:\n\n"
                "- 5 → 13 mod 9 = 4\n"
                "- 14 → 31 mod 9 = 4\n"
                "- 22 → 47 mod 9 = 2\n"
                "- 9 → 21 mod 9 = 3\n"
                "- 31 → 65 mod 9 = 2\n"
                "- 40 → 83 mod 9 = 2\n"
                "- 17 → 37 mod 9 = 1\n"
                "- 2 → 7 mod 9 = 7\n\n"
                "Chains: slot 1: [17]; slot 2: [22, 31, 40]; slot 3: [9]; slot 4: [5, 14]; slot 7: [2].\n"
                "Occupied slots = 5 → empty slots = 9 − 5 = 4. Longest chain = 3 (slot 2).\n\n"
                "Answer **(A)** 3 and 4.\n\n"
                "- (B) misses that 40 also maps to 2 (2·40 + 3 = 83 = 9·9 + 2).\n"
                "- (C)/(D) miscount occupied slots.\n\n"
                "**Tip:** keys that differ by a multiple of 9 always collide here, since "
                "2(k + 9) + 3 ≡ 2k + 3 (mod 9): 5/14, 22/31/40."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 9,
                                   "slots": {1: [17], 2: [22, 31, 40], 3: [9], 4: [5, 14], 7: [2]},
                                   "caption": "Chained table"}],
            "verify": '''
ch = {}
for k in [5,14,22,9,31,40,17,2]: ch.setdefault((2*k+3) % 9, []).append(k)
assert max(len(v) for v in ch.values()) == 3 and 9 - len(ch) == 4 and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Bubble sort — passes",
            "text": ("Bubble sort (ascending) makes left-to-right passes; in each pass adjacent elements "
                     "a[j], a[j+1] are swapped if a[j] > a[j+1], and after pass p the last p positions "
                     "are not examined again. Starting from [26, 11, 39, 4, 18, 33, 7], what is the "
                     "array after **two** complete passes?"),
            "options": ["[11, 4, 18, 26, 7, 33, 39]", "[11, 26, 4, 18, 33, 7, 39]",
                        "[4, 7, 11, 18, 26, 33, 39]", "[11, 4, 18, 7, 26, 33, 39]"],
            "answer": "A",
            "solution": (
                "Each pass 'bubbles' the largest remaining element to the end of the unsorted part.\n\n"
                "Pass 1 on [26, 11, 39, 4, 18, 33, 7]:\n"
                "- 26>11 swap → [11, 26, 39, 4, 18, 33, 7]; 26<39; 39>4 swap; 39>18 swap; 39>33 swap; "
                "39>7 swap → [11, 26, 4, 18, 33, 7, **39**].\n\n"
                "Pass 2 on the first six:\n"
                "- 11<26; 26>4 swap → [11, 4, 26, 18, 33, 7, 39]; 26>18 swap → [11, 4, 18, 26, 33, 7, 39]; "
                "26<33; 33>7 swap → [11, 4, 18, 26, 7, **33**, 39].\n\n"
                "Answer **(A)**.\n\n"
                "- (B) is the state after only one pass.\n"
                "- (C) is the fully sorted array.\n"
                "- (D) moves 7 too far — a single pass moves a small element left by at most one "
                "position (it moved from index 6 to 5 to 4 over two passes).\n\n"
                "**Tip:** small elements ('turtles') move left only one step per pass, which is why "
                "bubble sort needs many passes when a small element sits at the end."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each pass",
                                   "col_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "row_labels": ["start", "pass 1", "pass 2"],
                                   "rows": [[26, 11, 39, 4, 18, 33, 7], [11, 26, 4, 18, 33, 7, 39],
                                            [11, 4, 18, 26, 7, 33, 39]],
                                   "highlight": [[1, 6], [2, 5]]}],
            "verify": '''
a = [26,11,39,4,18,33,7]
for p in range(2):
    for j in range(len(a)-1-p):
        if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]
assert a == [11,4,18,26,7,33,39] and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Python — aliasing in adjacency lists",
            "text": ("A student builds the adjacency lists of the path graph 0 – 1 – 2 – 3 as follows. "
                     "What is printed?"),
            "code": '''adj = [[]] * 4
for u, v in [(0, 1), (1, 2), (2, 3)]:
    adj[u].append(v)
    adj[v].append(u)
print(len(adj[0]), adj[3][:3])''',
            "options": ["`1 [2]`", "`6 [1, 0, 2]`", "`2 [2]`", "`6 [2]`"],
            "answer": "B",
            "solution": (
                "`[[]] * 4` creates a list containing **four references to the same inner list**. "
                "Every `adj[x].append(...)` mutates that one shared list.\n\n"
                "Appends in order: (0,1) → 1, 0; (1,2) → 2, 1; (2,3) → 3, 2. The shared list is "
                "[1, 0, 2, 1, 3, 2].\n\n"
                "- `len(adj[0])` = 6.\n"
                "- `adj[3][:3]` = [1, 0, 2].\n\n"
                "Output `6 [1, 0, 2]` → option **(B)**.\n\n"
                "- (A) is the intended result with independent lists (deg(0) = 1, adj[3] = [2]).\n"
                "- (C)/(D) mix the two behaviours.\n\n"
                "**Fix:** `adj = [[] for _ in range(4)]` evaluates `[]` four times. With the buggy "
                "version a BFS would see every vertex adjacent to everything in the shared list — "
                "connectivity and bipartiteness checks silently give wrong answers."
            ),
            "verify": "assert OUTPUT.strip() == '6 [1, 0, 2]' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — lower bound",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def lb(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

a = [2, 4, 4, 4, 7, 9, 9, 12, 15]
print(lb(a, 4) + lb(a, 10) + lb(a, 1))''',
            "answer": "8",
            "solution": (
                "`lb(a, x)` is the classic **lower bound**: it returns the first index i with "
                "a[i] ≥ x (or len(a) if none). The invariant is a[0..lo−1] < x ≤ a[hi..n−1].\n\n"
                "- lb(a, 4): first element ≥ 4 is the first 4 at index **1** (trace: lo,hi = 0,9 → "
                "mid 4 (7 ≥ 4) hi=4 → mid 2 (4 ≥ 4) hi=2 → mid 1 (4) hi=1 → mid 0 (2 < 4) lo=1).\n"
                "- lb(a, 10): first element ≥ 10 is 12 at index **7**.\n"
                "- lb(a, 1): every element is ≥ 1 → index **0**.\n\n"
                "Sum = 1 + 7 + 0 = **8**.\n\n"
                "**Trap:** a standard 'found / not found' binary search could return any of the "
                "indices 1, 2, 3 for x = 4; the lower-bound variant always converges to the "
                "*leftmost* one because it never stops on equality."
            ),
            "solution_diagrams": [{"type": "array", "values": [2, 4, 4, 4, 7, 9, 9, 12, 15],
                                   "pointers": {"lb(4)": 1, "lb(10)": 7, "lb(1)": 0}, "label": "a"}],
            "verify": '''
import bisect
assert bisect.bisect_left(a, 4) + bisect.bisect_left(a, 10) + bisect.bisect_left(a, 1) == int(ANSWER)
assert OUTPUT.strip() == ANSWER
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "MSQ", "marks": 2, "topic": "Connectivity — cut vertices and bridges",
            "text": ("Consider the undirected graph shown. A *cut vertex* is a vertex whose removal "
                     "(with its incident edges) increases the number of connected components; a "
                     "*bridge* is an edge whose removal does so. Which of the following statements "
                     "is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U", "V", "W", "X"],
                          "edges": [["P", "Q"], ["Q", "R"], ["R", "P"], ["R", "S"], ["S", "T"],
                                    ["T", "U"], ["U", "S"], ["U", "V"], ["V", "W"], ["W", "X"],
                                    ["X", "V"], ["T", "W"]],
                          "pos": {"P": [0, 2], "Q": [0, 0], "R": [1.2, 1], "S": [2.5, 1],
                                  "T": [3.6, 2], "U": [3.6, 0], "V": [5, 0], "W": [5, 2],
                                  "X": [6.2, 1]}}],
            "options": ["R is a cut vertex", "S is a cut vertex", "U is a cut vertex",
                        "The edge U–V is a bridge"],
            "answer": ["A", "B"],
            "solution": (
                "Group the graph into *blocks* (maximal pieces with no cut vertex). A vertex shared by "
                "two blocks is a cut vertex; a block consisting of a single edge is a bridge.\n\n"
                "Cycles present:\n"
                "- P–Q–R (triangle);\n"
                "- S–T–U (triangle), U–V–X–W–T–U and V–W–X (triangle). Because of the edge T–W, the "
                "vertices S, T, U, V, W, X all lie on common cycles → they form **one block**.\n"
                "- R–S lies on no cycle → it is a bridge (its own block).\n\n"
                "Blocks: {P, Q, R}, {R, S}, {S, T, U, V, W, X}.\n\n"
                "- (A) R joins blocks {P,Q,R} and {R,S}: removing R isolates {P, Q}. **True.**\n"
                "- (B) S joins {R,S} and the big block: removing S separates {P,Q,R} from the rest. "
                "**True.**\n"
                "- (C) Removing U: S still reaches T, T reaches W via the edge T–W, and W reaches V, X. "
                "Graph stays connected. **False.**\n"
                "- (D) U–V lies on the cycle U–V–W–T–U. Not a bridge. **False.**\n\n"
                "**Trap:** without the chord T–W, U and V *would* be cut vertices and U–V a bridge; "
                "one extra edge merges three blocks into one."
            ),
            "verify": '''
N = "PQRSTUVWX"
E = [('P','Q'),('Q','R'),('R','P'),('R','S'),('S','T'),('T','U'),('U','S'),('U','V'),
     ('V','W'),('W','X'),('X','V'),('T','W')]
def comps(nodes, edges):
    p = {v: v for v in nodes}
    def f(x):
        while p[x] != x: x = p[x]
        return x
    for u, v in edges: p[f(u)] = f(v)
    return len({f(v) for v in nodes})
def cut(x):
    nodes = [v for v in N if v != x]
    return comps(nodes, [e for e in E if x not in e]) > 1
def bridge(e):
    return comps(N, [x for x in E if x != e]) > 1
truth = {'A': cut('R'), 'B': cut('S'), 'C': cut('U'), 'D': bridge(('U','V'))}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Graph theory — edges vs components",
            "text": ("The maximum number of edges in a simple undirected graph with 12 vertices and "
                     "**exactly** 4 connected components is ______."),
            "answer": "36",
            "solution": (
                "Each component must be a complete graph to maximise edges, so the question is how to "
                "split 12 vertices into 4 non-empty parts n₁ + n₂ + n₃ + n₄ = 12 maximising "
                "∑ C(nᵢ, 2).\n\n"
                "Since C(n, 2) is convex, moving a vertex from a smaller part to a larger part never "
                "decreases the sum: C(a+1,2) + C(b−1,2) − C(a,2) − C(b,2) = a − b + 1 > 0 when "
                "a ≥ b. So the optimum is as **unbalanced** as possible: three isolated vertices and "
                "one clique on 12 − 3 = 9 vertices.\n\n"
                "Maximum = C(9, 2) = 36.\n\n"
                "Comparison with other splits:\n"
                "- 3+3+3+3 → 4 × 3 = 12 edges\n"
                "- 6+2+2+2 → 15 + 3 = 18 edges\n"
                "- 8+2+1+1 → 28 + 1 = 29 edges\n"
                "- 9+1+1+1 → **36** edges\n\n"
                "General formula: max edges with n vertices and k components = C(n − k + 1, 2).\n\n"
                "**Trap:** balancing the components (the instinct from 'fair splitting') gives the "
                "*minimum* among clique unions, not the maximum."
            ),
            "verify": '''
best = 0
n = 12
for a in range(1, n):
    for b in range(1, n):
        for c in range(1, n):
            d = n - a - b - c
            if d >= 1:
                best = max(best, sum(x*(x-1)//2 for x in (a, b, c, d)))
assert best == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Bipartiteness — BFS two-colouring",
            "text": ("The function below tries to 2-colour the graph G shown, starting at vertex 1. "
                     "Adjacency lists are sorted in increasing order, so `adj[u]` is visited in "
                     "increasing vertex order. Which of the following statements is/are TRUE?"),
            "code": '''from collections import deque

def two_colour(adj, s):
    col = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in col:
                col[v] = 1 - col[u]
                q.append(v)
            elif col[v] == col[u]:
                return None, (u, v)
    return col, None''',
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["1", "2", "3", "4", "5", "6", "7", "8"],
                          "edges": [["1", "2"], ["2", "3"], ["3", "4"], ["4", "5"], ["5", "6"],
                                    ["6", "1"], ["2", "7"], ["7", "8"], ["8", "5"], ["3", "8"],
                                    ["4", "8"]],
                          "pos": {"1": [0, 1], "2": [1, 2], "3": [2.4, 2], "4": [3.4, 1],
                                  "5": [2.4, 0], "6": [1, 0], "7": [1.6, 3.2], "8": [4.8, 1]}}],
            "options": ["`two_colour(adj, 1)` returns `None` as its first component",
                        "The conflicting edge it reports is `(4, 8)`",
                        "Deleting only the edge 3–8 makes G bipartite",
                        "Deleting only the edge 4–8 makes G bipartite"],
            "answer": ["A", "B", "D"],
            "solution": (
                "BFS colours each newly discovered vertex opposite to its parent; a non-tree edge "
                "between two vertices of the same colour proves an odd cycle.\n\n"
                "Trace (colour in brackets):\n"
                "- u=1 [0]: 2 [1], 6 [1].\n"
                "- u=2: 1 ok, 3 [0], 7 [0].\n"
                "- u=6: 1 ok, 5 [0].\n"
                "- u=3: 2 ok, 4 [1], 8 [1].\n"
                "- u=7 [0]: 2 ok, 8 [1] ok.\n"
                "- u=5 [0]: 4 [1] ok, 6 ok, 8 [1] ok.\n"
                "- u=4 [1]: 3 ok, 5 ok, **8 [1] — same colour** → return `(None, (4, 8))`.\n\n"
                "- (A) G is not bipartite and the function detects it. **True.**\n"
                "- (B) Reported pair is (4, 8). **True.**\n"
                "- (C) Removing 3–8 leaves the triangle 4–5–8. **False.**\n"
                "- (D) Every odd cycle uses 4–8 (triangles 3–4–8 and 4–5–8, etc.). Without it the "
                "colouring {1,3,5,7} vs {2,4,6,8} is proper. **True.**\n\n"
                "**Trap:** the reported edge depends on the visiting order; it is *an* edge of an odd "
                "cycle, not necessarily the unique culprit — here it happens to be unique."
            ),
            "verify": '''
E = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(2,7),(7,8),(8,5),(3,8),(4,8)]
def mk(E):
    adj = {v: [] for v in range(1, 9)}
    for u, v in E: adj[u].append(v); adj[v].append(u)
    for v in adj: adj[v].sort()
    return adj
c, bad = two_colour(mk(E), 1)
truth = {'A': c is None, 'B': bad == (4, 8),
         'C': two_colour(mk([e for e in E if e != (3,8)]), 1)[0] is not None,
         'D': two_colour(mk([e for e in E if e != (4,8)]), 1)[0] is not None}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Connected components — iterative DFS in Python",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def pairs(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    total = done = 0
    for s in range(n):
        if seen[s]:
            continue
        size, st = 0, [s]
        seen[s] = True
        while st:
            u = st.pop()
            size += 1
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    st.append(v)
        total += size * done
        done += size
    return total

E = [(0, 5), (5, 9), (1, 4), (4, 11), (11, 1),
     (2, 7), (3, 8), (8, 10), (6, 6)]
print(pairs(12, E))''',
            "answer": "56",
            "solution": (
                "The function finds each connected component (iterative DFS with an explicit stack; a "
                "vertex is marked when pushed, so it is counted exactly once) and accumulates "
                "size × (number of vertices in earlier components). That is the number of unordered "
                "pairs of vertices lying in **different** components.\n\n"
                "Components of the 12 vertices:\n"
                "- {0, 5, 9} (size 3)\n"
                "- {1, 4, 11} (size 3; edges form a triangle)\n"
                "- {2, 7} (size 2)\n"
                "- {3, 8, 10} (size 3)\n"
                "- {6} (size 1; the self-loop (6, 6) adds 6 to its own list twice but connects "
                "nothing)\n\n"
                "Accumulation in order of the smallest vertex 0, 1, 2, 3, 6:\n"
                "- 3 × 0 = 0 → done 3\n"
                "- 3 × 3 = 9 → done 6\n"
                "- 2 × 6 = 12 → done 8\n"
                "- 3 × 8 = 24 → done 11\n"
                "- 1 × 11 = 11 → done 12\n"
                "Total = 0 + 9 + 12 + 24 + 11 = **56**.\n\n"
                "Check: C(12, 2) − (3 + 3 + 1 + 3 + 0) = 66 − 10 = 56.\n\n"
                "**Trap:** forgetting the isolated vertex 6 (11 pairs) or treating the self-loop as "
                "creating an extra component."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "DFS — edge classification",
            "text": ("Depth-first search is run on the directed graph shown. The outer loop considers "
                     "start vertices in alphabetical order, and each adjacency list is explored in "
                     "alphabetical order. Let T, B, F, C be the numbers of tree, back, forward and cross "
                     "edges respectively. What is (T, B, F, C)?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                          "edges": [["A", "B"], ["A", "D"], ["A", "F"], ["B", "C"], ["B", "E"],
                                    ["C", "A"], ["C", "F"], ["D", "E"], ["E", "B"], ["E", "F"],
                                    ["G", "D"], ["G", "F"]],
                          "pos": {"A": [0, 2], "B": [2, 3], "C": [4, 2], "D": [0, 0], "E": [2, 0],
                                  "F": [4, 0], "G": [1, -1.4]}}],
            "options": ["(5, 2, 1, 4)", "(5, 2, 0, 5)", "(6, 2, 1, 3)", "(5, 3, 1, 3)"],
            "answer": "A",
            "solution": (
                "Classify edge (u, v) when it is examined: v undiscovered → **tree**; v discovered "
                "but unfinished (an ancestor) → **back**; v finished with d[u] < d[v] (a descendant) "
                "→ **forward**; v finished with d[v] < d[u] → **cross**.\n\n"
                "DFS trace with (discovery/finish) times:\n"
                "- A (1): A→B tree. B (2): B→C tree. C (3): C→A **back** (A is active); C→F tree. "
                "F (4/5). C finishes (6).\n"
                "- Back in B: B→E tree. E (7): E→B **back**; E→F **cross** (F finished, d[F]=4 < 7). "
                "E (8). B (9).\n"
                "- Back in A: A→D tree. D (10): D→E **cross**. D (11). A→F: F finished and "
                "d[A]=1 < d[F]=4 → **forward**. A (12).\n"
                "- New tree from G (13): G→D **cross**, G→F **cross**. G (14).\n\n"
                "Tree: A→B, B→C, C→F, B→E, A→D (5). Back: C→A, E→B (2). Forward: A→F (1). "
                "Cross: E→F, D→E, G→D, G→F (4). Total 12 edges ✓.\n\n"
                "Answer **(A)** (5, 2, 1, 4).\n\n"
                "- (B) classifies A→F as cross — but F is a descendant of A.\n"
                "- (C) counts A→F as a tree edge — F was already discovered via C.\n"
                "- (D) treats E→F as back.\n\n"
                "**Tip:** the graph has a cycle iff DFS finds a back edge (here A→B→C→A)."
            ),
            "solution_diagrams": [{"type": "graph", "directed": True,
                                   "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                                   "edges": [["A", "B"], ["A", "D"], ["A", "F"], ["B", "C"], ["B", "E"],
                                             ["C", "A"], ["C", "F"], ["D", "E"], ["E", "B"], ["E", "F"],
                                             ["G", "D"], ["G", "F"]],
                                   "pos": {"A": [0, 2], "B": [2, 3], "C": [4, 2], "D": [0, 0],
                                           "E": [2, 0], "F": [4, 0], "G": [1, -1.4]},
                                   "highlight_edges": [["A", "B"], ["B", "C"], ["C", "F"], ["B", "E"],
                                                       ["A", "D"]],
                                   "caption": "DFS forest (tree edges highlighted)"}],
            "verify": '''
G = {'A':'BDF','B':'CE','C':'AF','D':'E','E':'BF','F':'','G':'DF'}
t = [0]; disc = {}; fin = {}; cls = {}
def dfs(u):
    t[0] += 1; disc[u] = t[0]
    for v in G[u]:
        if v not in disc: cls[(u,v)] = 'T'; dfs(v)
        elif v not in fin: cls[(u,v)] = 'B'
        elif disc[u] < disc[v]: cls[(u,v)] = 'F'
        else: cls[(u,v)] = 'C'
    t[0] += 1; fin[u] = t[0]
for u in sorted(G):
    if u not in disc: dfs(u)
vals = list(cls.values())
res = tuple(vals.count(x) for x in 'TBFC')
assert res == (5, 2, 1, 4) and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MSQ", "marks": 2, "topic": "Sorting — properties and counts",
            "text": "Which of the following statements is/are TRUE?",
            "options": ["Quicksort with the Lomuto partition (pivot = last element, test a[j] ≤ pivot) "
                        "makes exactly 15 element comparisons on the array [7, 7, 7, 7, 7, 7]",
                        "Merge sort whose merge takes the element from the **left** run when the two "
                        "front elements are equal is a stable sort",
                        "Insertion sort makes exactly 28 element comparisons on an array of 8 distinct "
                        "elements in strictly decreasing order",
                        "Selection sort (swap a[i] with the minimum of a[i..n−1]) is stable"],
            "answer": ["A", "B", "C"],
            "solution": (
                "- (A) With all keys equal, every a[j] ≤ pivot, so the partition places the pivot at "
                "the **end** and recurses on n − 1 elements. Comparisons: 5 + 4 + 3 + 2 + 1 = 15 — the "
                "Θ(n²) worst case of Lomuto on duplicates. **True.**\n\n"
                "- (B) Taking from the left run on ties keeps equal keys in their original relative "
                "order (left-run elements were earlier in the input). **True.**\n\n"
                "- (C) In reverse-sorted input, inserting the i-th element compares it with all i "
                "earlier elements (the loop stops only at index 0, with no failing comparison). Total "
                "1 + 2 + … + 7 = 28 = n(n−1)/2. **True.**\n\n"
                "- (D) The long-distance swap can jump an element over an equal one. Example "
                "[2(a), 2(b), 1]: pass 0 swaps 2(a) with 1 → [1, 2(b), 2(a)] — the two 2s are reversed. "
                "**False.**\n\n"
                "**Trap:** in (C) one might add a final failing comparison per pass (giving 35); in a "
                "strictly decreasing array every comparison succeeds until j falls below 0, where the "
                "`j >= 0` test (an index check, not an element comparison) stops the loop."
            ),
            "verify": '''
c = [0]
def qs(a, lo, hi):
    if lo >= hi: return
    p = a[hi]; i = lo - 1
    for j in range(lo, hi):
        c[0] += 1
        if a[j] <= p:
            i += 1; a[i], a[j] = a[j], a[i]
    a[i+1], a[hi] = a[hi], a[i+1]
    qs(a, lo, i); qs(a, i+2, hi)
qs([7]*6, 0, 5)
A = c[0] == 15
def msort(a):
    if len(a) <= 1: return a
    m = len(a)//2; L, R = msort(a[:m]), msort(a[m:]); out = []; i = j = 0
    while i < len(L) and j < len(R):
        if L[i][0] <= R[j][0]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
data = [(3,'a'),(1,'b'),(3,'c'),(2,'d'),(1,'e'),(3,'f')]
B = msort(data) == sorted(data, key=lambda x: x[0])
a = list(range(8, 0, -1)); cc = 0
for i in range(1, 8):
    key = a[i]; j = i - 1
    while j >= 0:
        cc += 1
        if a[j] > key: a[j+1] = a[j]; j -= 1
        else: break
    a[j+1] = key
C = cc == 28
s = [(2,'a'),(2,'b'),(1,'c')]
for i in range(len(s)-1):
    m = min(range(i, len(s)), key=lambda k: s[k][0])
    s[i], s[m] = s[m], s[i]
D = s == sorted([(2,'a'),(2,'b'),(1,'c')], key=lambda x: x[0])
truth = {'A': A, 'B': B, 'C': C, 'D': D}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "NAT", "marks": 2, "topic": "Linked lists — Floyd's cycle detection",
            "text": ("The following program builds the singly linked list shown (node 10 points back to "
                     "node 8) and runs the meeting phase of Floyd's tortoise-and-hare algorithm. The "
                     "value printed is ______."),
            "code": '''class Node:
    def __init__(self, v):
        self.v, self.nxt = v, None

nodes = [Node(i) for i in range(1, 11)]
for a, b in zip(nodes, nodes[1:]):
    a.nxt = b
nodes[-1].nxt = nodes[7]

slow = fast = nodes[0]
steps = 0
while True:
    slow = slow.nxt
    fast = fast.nxt.nxt
    steps += 1
    if slow is fast:
        break
print(steps)''',
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                          "edges": [["1", "2"], ["2", "3"], ["3", "4"], ["4", "5"], ["5", "6"],
                                    ["6", "7"], ["7", "8"], ["8", "9"], ["9", "10"], ["10", "8"]],
                          "pos": {"1": [0, 1], "2": [1, 1], "3": [2, 1], "4": [3, 1], "5": [4, 1],
                                  "6": [5, 1], "7": [6, 1], "8": [7, 1], "9": [8, 2], "10": [8, 0]}}],
            "answer": "9",
            "solution": (
                "Let μ = number of nodes before the cycle and λ = cycle length. Here the tail is "
                "1 → … → 7, so μ = 7, and the cycle 8 → 9 → 10 → 8 has λ = 3.\n\n"
                "After k steps the tortoise is k nodes from the head and the hare 2k nodes. Both are "
                "inside the cycle once k ≥ μ, and they coincide when 2k − k = k is a multiple of λ. So "
                "the first meeting is at the smallest k ≥ μ with k ≡ 0 (mod λ): k ≥ 7, k multiple "
                "of 3 → k = **9**.\n\n"
                "Explicit check (position = node value):\n"
                "- k=7: slow 8, fast at 14 steps → 8 + (14−7) mod 3 = 8 + 1 = 9 → different.\n"
                "- k=8: slow 9, fast at 16 → 8 + 9 mod 3 = 8 → different.\n"
                "- k=9: slow 10, fast at 18 → 8 + 11 mod 3 = 10 → **meet** at node 10.\n\n"
                "Printed value: **9**.\n\n"
                "**Trap:** assuming they meet at the cycle entry (node 8) or after λ steps. The "
                "meeting point is generally *inside* the cycle; finding the entry needs the second "
                "phase (restart one pointer at the head and move both one step at a time)."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER and slow.v == 10",
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MCQ", "marks": 2, "topic": "Heaps — bottom-up build-heap",
            "text": ("The array [35, 12, 47, 8, 29, 3, 61, 17, 5] is converted into a binary **min**-heap "
                     "(0-based; children of i are 2i+1 and 2i+2) using the bottom-up method: for "
                     "i = ⌊n/2⌋ − 1 down to 0, sift a[i] down, always swapping with the smaller child "
                     "while that child is smaller. What is the resulting array?"),
            "options": ["[3, 5, 35, 8, 29, 47, 61, 17, 12]",
                        "[3, 5, 8, 12, 29, 47, 61, 35, 17]",
                        "[3, 5, 35, 12, 29, 47, 61, 17, 8]",
                        "[3, 8, 5, 12, 29, 47, 61, 17, 35]"],
            "answer": "A",
            "solution": (
                "Bottom-up heap construction sifts down every internal node, from the last one "
                "(index ⌊9/2⌋ − 1 = 3) back to the root; total cost is O(n).\n\n"
                "- i=3 (8): children 17, 5 → swap with 5 → [35, 12, 47, **5**, 29, 3, 61, 17, **8**].\n"
                "- i=2 (47): children 3, 61 → swap with 3 → [35, 12, **3**, 5, 29, **47**, 61, 17, 8].\n"
                "- i=1 (12): children 5, 29 → swap with 5 (index 3); now 12 at index 3 has children "
                "17, 8 → swap with 8 → [35, **5**, 3, **8**, 29, 47, 61, 17, **12**].\n"
                "- i=0 (35): children 5, 3 → swap with 3 (index 2); children of index 2 are 47, 61 → "
                "stop → [**3**, 5, **35**, 8, 29, 47, 61, 17, 12].\n\n"
                "Answer **(A)** (5 swaps in total).\n\n"
                "- (B) is the heap obtained by inserting the keys one by one — a different (also "
                "valid) heap.\n"
                "- (C) stops sifting 12 after one level (12 > 8 violates the heap property).\n"
                "- (D) is also a valid min-heap of the same keys, but not the one this procedure "
                "builds: 35 only sinks one level (to index 2), it never reaches the last leaf.\n\n"
                "**Trap:** build-heap and repeated insertion generally produce *different* heaps."
            ),
            "solution_diagrams": [{"type": "heap", "values": [3, 5, 35, 8, 29, 47, 61, 17, 12],
                                   "caption": "Min-heap after bottom-up construction"}],
            "verify": '''
h = [35,12,47,8,29,3,61,17,5]
def sift(a, i):
    n = len(a)
    while True:
        l, r, m = 2*i+1, 2*i+2, i
        if l < n and a[l] < a[m]: m = l
        if r < n and a[r] < a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m
for i in range(len(h)//2 - 1, -1, -1): sift(h, i)
import heapq
ins = []
for x in [35,12,47,8,29,3,61,17,5]: heapq.heappush(ins, x)
assert h == [3,5,35,8,29,47,61,17,12] and ins == [3,5,8,12,29,47,61,35,17]
assert ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Hashing — unsuccessful search with linear probing",
            "text": ("A hash table of size 10 with linear probing (h(k) = k mod 10, step +1 with "
                     "wrap-around) currently holds the keys shown. An unsuccessful search starts at the "
                     "home slot of the sought key and stops at the first empty slot; every slot "
                     "inspected, including that empty one, counts as a probe. If the home slot is "
                     "equally likely to be any of the 10 slots, the expected number of probes for an "
                     "unsuccessful search is:"),
            "diagrams": [{"type": "hashtable", "size": 10,
                          "slots": {0: 39, 1: 21, 4: 64, 5: 44, 8: 18, 9: 28},
                          "caption": "Figure: current table"}],
            "options": ["2.3", "1.7", "1.6", "2.5"],
            "answer": "A",
            "solution": (
                "Occupied slots form two clusters: {8, 9, 0, 1} (wrapping around the end) and {4, 5}. "
                "An unsuccessful search from home slot h probes the rest of h's cluster plus one empty "
                "slot.\n\n"
                "Probes per home slot:\n"
                "- h=0: 0, 1, 2 → 3\n"
                "- h=1: 1, 2 → 2\n"
                "- h=2: 1;  h=3: 1\n"
                "- h=4: 4, 5, 6 → 3;  h=5: 5, 6 → 2\n"
                "- h=6: 1;  h=7: 1\n"
                "- h=8: 8, 9, 0, 1, 2 → 5\n"
                "- h=9: 9, 0, 1, 2 → 4\n\n"
                "Sum = 3 + 2 + 1 + 1 + 3 + 2 + 1 + 1 + 5 + 4 = 23 → expected **2.3** probes → "
                "option **(A)**.\n\n"
                "- (B) 1.7 forgets the wrap-around: it stops the searches from slots 8 and 9 at the "
                "end of the array (2 and 1 probes instead of 5 and 4).\n"
                "- (C) 1.6 = 1 + load factor 0.6 — the uniform-hashing estimate, which ignores "
                "clustering.\n"
                "- (D) 2.5 is 1/(1 − α) — the open-addressing estimate under *uniform* probing, "
                "again not this concrete table.\n\n"
                "**Tip:** a cluster of length L contributes (L+1) + L + … + 2 = (L+1)(L+2)/2 − 1 "
                "probes; long clusters dominate the average (primary clustering)."
            ),
            "verify": '''
T = [None]*10
for k in [18, 28, 39, 21, 64, 44]:
    i = k % 10
    while T[i] is not None: i = (i+1) % 10
    T[i] = k
assert {i: v for i, v in enumerate(T) if v is not None} == {0:39, 1:21, 4:64, 5:44, 8:18, 9:28}
tot = 0
for h in range(10):
    i, p = h, 1
    while T[i] is not None: i = (i+1) % 10; p += 1
    tot += p
assert abs(tot/10 - 2.3) < 1e-9 and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Bipartiteness and connectivity of a grid graph",
            "text": ("G is the 3 × 4 grid graph shown (vertex labels 1–12 row by row; edges join "
                     "horizontally or vertically adjacent vertices). Which of the following statements "
                     "is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": [str(i) for i in range(1, 13)],
                          "edges": [["1", "2"], ["2", "3"], ["3", "4"], ["5", "6"], ["6", "7"],
                                    ["7", "8"], ["9", "10"], ["10", "11"], ["11", "12"], ["1", "5"],
                                    ["5", "9"], ["2", "6"], ["6", "10"], ["3", "7"], ["7", "11"],
                                    ["4", "8"], ["8", "12"]],
                          "pos": {"1": [0, 2], "2": [1.4, 2], "3": [2.8, 2], "4": [4.2, 2],
                                  "5": [0, 1], "6": [1.4, 1], "7": [2.8, 1], "8": [4.2, 1],
                                  "9": [0, 0], "10": [1.4, 0], "11": [2.8, 0], "12": [4.2, 0]}}],
            "options": ["G is bipartite and both colour classes have 6 vertices",
                        "Adding the single edge 1–6 makes G non-bipartite",
                        "G has at least one cut vertex",
                        "Deleting the two vertices 2 and 5 disconnects G"],
            "answer": ["A", "B", "D"],
            "solution": (
                "Colour vertex (r, c) by the parity of r + c — every grid edge changes r + c by 1, so "
                "this is a proper 2-colouring (a 'chessboard' colouring).\n\n"
                "- (A) Each row of 4 has 2 vertices of each colour → 6 and 6. **True.**\n"
                "- (B) Vertex 1 = (0,0) and 6 = (1,1) both have even r + c, i.e. the same colour. An "
                "edge between them closes the odd cycle 1–2–6–1 (length 3). **True.**\n"
                "- (C) Every vertex lies on a 4-cycle (unit square) and removing any one vertex leaves "
                "the rest connected around it; the grid is 2-connected. **False.**\n"
                "- (D) Vertex 1's only neighbours are 2 and 5. Removing both isolates vertex 1 → "
                "disconnected. **True.**\n\n"
                "Extra facts: |E| = 3·3 + 2·4 = 17; minimum degree 2 (corners) — so the vertex "
                "connectivity is exactly 2.\n\n"
                "**Trap:** concluding from (D) that the grid has a cut vertex — needing **two** "
                "vertices to disconnect it means it has none."
            ),
            "verify": '''
N = list(range(1, 13))
E = []
for r in range(3):
    for c in range(4):
        v = 4*r + c + 1
        if c < 3: E.append((v, v+1))
        if r < 2: E.append((v, v+4))
def connected(nodes, edges):
    nodes = list(nodes); p = {v: v for v in nodes}
    def f(x):
        while p[x] != x: x = p[x]
        return x
    for u, v in edges:
        if u in p and v in p: p[f(u)] = f(v)
    return len({f(v) for v in nodes}) == 1
def bip(edges):
    col = {}
    for s in N:
        if s in col: continue
        col[s] = 0; st = [s]
        while st:
            u = st.pop()
            for a, b in edges:
                for x, y in ((a, b), (b, a)):
                    if x == u:
                        if y not in col: col[y] = 1 - col[u]; st.append(y)
                        elif col[y] == col[u]: return None
    return col
col = bip(E)
A = col is not None and sorted(list(col.values()).count(k) for k in (0, 1)) == [6, 6]
B = bip(E + [(1, 6)]) is None
C = any(not connected([v for v in N if v != x], E) for x in N)
D = not connected([v for v in N if v not in (2, 5)], E)
truth = {'A': A, 'B': B, 'C': C, 'D': D}
assert len(E) == 17
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
    ],
}
