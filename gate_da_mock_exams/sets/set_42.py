# Set 42 — Full-Syllabus Mock — Paper 12
SET = {
    "number": 42,
    "title": "Full-Syllabus Mock — Paper 12",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — list repetition and aliasing",
            "text": "Consider the following Python program. What is printed?",
            "code": '''rows = [[]] * 3
rows[1].append(4)
rows += [[]]
rows[3].append(7)
rows[0] = rows[0] + [9]
print(rows)''',
            "options": [
                "`[[9], [4], [], [7]]`",
                "`[[4, 9], [4], [4], [7]]`",
                "`[[4, 9], [4, 9], [4, 9], [7]]`",
                "`[[4, 9], [4], [4], [4, 7]]`",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** `[[]] * 3` creates a list holding **three references to one** inner list. "
                "In-place mutation through any of them is visible through all; *rebinding* a slot "
                "(`rows[0] = …`) affects only that slot.\n\n"
                "Let L be the shared inner list.\n"
                "- `rows[1].append(4)` → L = [4]; rows = [L, L, L].\n"
                "- `rows += [[]]` extends `rows` with a *new*, separate empty list M → [L, L, L, M].\n"
                "- `rows[3].append(7)` → M = [7].\n"
                "- `rows[0] = rows[0] + [9]` builds a **new** list [4, 9] (the `+` operator copies) and "
                "stores it in slot 0 only; L is still [4].\n\n"
                "Output: `[[4, 9], [4], [4], [7]]`.\n\n"
                "**Options:**\n"
                "- (A) assumes the three inner lists were independent.\n"
                "- (C) treats `rows[0] + [9]` as an in-place change of L (that would be `rows[0] += [9]`).\n"
                "- (D) assumes `+= [[]]` appended another reference to L.\n\n"
                "**Trap:** `x = x + y` and `x += y` differ for lists — the first creates a new object, the "
                "second mutates in place."
            ),
            "verify": "assert OUTPUT.strip() == '[[4, 9], [4], [4], [7]]' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Stacks and queues — interleaved operations",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''from collections import deque

s, q = [], deque()
for x in range(1, 9):
    if x % 3 == 0:
        q.append(s.pop())
    else:
        s.append(x)
        if x % 4 == 0:
            s.append(q.popleft())
print(sum(s[::2]) - len(q))''',
            "answer": "11",
            "solution": (
                "**Concept:** `s` is a stack (list: append/pop at the right end) and `q` a FIFO queue "
                "(append at the right, popleft at the left). Multiples of 3 move the stack top into the "
                "queue; multiples of 4 additionally move the queue front back onto the stack.\n\n"
                "Trace (stack bottom → top | queue front → rear):\n"
                "- x = 1: push → [1] | []\n"
                "- x = 2: push → [1, 2] | []\n"
                "- x = 3: pop 2 into q → [1] | [2]\n"
                "- x = 4: push 4, then push q.popleft() = 2 → [1, 4, 2] | []\n"
                "- x = 5: push → [1, 4, 2, 5] | []\n"
                "- x = 6: pop 5 into q → [1, 4, 2] | [5]\n"
                "- x = 7: push → [1, 4, 2, 7] | [5]\n"
                "- x = 8: push 8, then push 5 → [1, 4, 2, 7, 8, 5] | []\n\n"
                "`s[::2]` = [1, 2, 8] → sum 11; `len(q)` = 0. Printed: **11**.\n\n"
                "**Trap:** popping from the wrong end — `q.pop()` vs `q.popleft()` coincide here only "
                "because q never holds two elements, but `s.pop(0)` instead of `s.pop()` would change "
                "everything."
            ),
            "solution_diagrams": [{"type": "stack", "values": [1, 4, 2, 7, 8, 5], "label": "s",
                                   "caption": "Final stack (queue is empty)"}],
            "verify": "assert int(OUTPUT) == int(ANSWER) and s == [1, 4, 2, 7, 8, 5] and not q",
        },
        # ------------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Linked lists — operation costs",
            "text": ("A singly linked list of n nodes is maintained with both a `head` and a `tail` pointer "
                     "(each node stores only a value and a `next` pointer). Which of the following operations "
                     "can be performed in O(1) worst-case time, independent of n?"),
            "options": [
                "Insert a new node at the front",
                "Delete the last node (and update `tail`)",
                "Insert a new node at the end",
                "Concatenate a second such list (with its own head and tail) to the end of this one",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept:** an O(1) operation may only touch a constant number of nodes reachable from "
                "the stored pointers. A singly linked node cannot reach its predecessor.\n\n"
                "- (A) new.next = head; head = new. **O(1).**\n"
                "- (B) After removing the last node, `tail` must point to the *second-to-last* node, and "
                "the only way to find it is to walk from `head` — Θ(n). **Not O(1).**\n"
                "- (C) tail.next = new; tail = new. **O(1).**\n"
                "- (D) tail₁.next = head₂; tail₁ = tail₂. **O(1).** (This is why linked lists, unlike "
                "arrays, concatenate cheaply.)\n\n"
                "**Trap:** assuming the tail pointer makes *deletion* at the tail cheap. It would require a "
                "doubly linked list (a `prev` pointer) — then all four operations are O(1)."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": [12, 7, 30, 5], "head": "head",
                                   "tail": "tail",
                                   "caption": "Deleting 5 needs the node 30, reachable only from head"}],
        },
        # ------------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Binary trees — counting shapes of maximum height",
            "text": ("The number of structurally distinct binary trees with 5 nodes whose height is 4 "
                     "(height = number of edges on the longest root-to-leaf path) is ______."),
            "answer": "16",
            "solution": (
                "**Concept:** a binary tree with n nodes has height at most n − 1, attained exactly when "
                "the tree is a single path (every non-leaf node has exactly one child).\n\n"
                "With 5 nodes and height 4, all 5 nodes lie on one root-to-leaf path, so each of the 4 "
                "non-leaf nodes has exactly one child, which can be either a **left** or a **right** child. "
                "These choices are independent and each gives a different structure:\n\n"
                "2 × 2 × 2 × 2 = 2^{4} = **16**.\n\n"
                "For comparison, there are Catalan(5) = 42 binary trees with 5 nodes in total; 16 of them "
                "have height 4 (and 20 have height 3, 6 have height 2).\n\n"
                "**Trap:** answering 1 or 2 (only the all-left / all-right chains) — zig-zag paths count as "
                "different structures."
            ),
            "solution_diagrams": [{"type": "bintree", "tree": [1, [2, None, [3, [4, None, [5]], None]], None],
                                   "caption": "One of the 16 shapes (choices: L, R, L, R)"}],
            "verify": '''
def trees(n):
    if n == 0: return [None]
    out = []
    for l in range(n):
        for L in trees(l):
            for R in trees(n - 1 - l): out.append((L, R))
    return out
def h(t): return -1 if t is None else 1 + max(h(t[0]), h(t[1]))
assert sum(1 for t in trees(5) if h(t) == 4) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — reconstructing the insertion order",
            "text": ("A hash table of size 10 uses h(k) = k mod 10 and linear probing. After six insertions "
                     "into an initially empty table, the table is as shown below. Which insertion order "
                     "produces this table?"),
            "diagrams": [{"type": "hashtable", "size": 10,
                          "slots": {1: 41, 2: 52, 3: 13, 4: 31, 5: 22, 6: 64},
                          "caption": "Final table"}],
            "options": [
                "41, 52, 31, 13, 22, 64",
                "52, 41, 13, 31, 22, 64",
                "13, 52, 41, 22, 31, 64",
                "52, 13, 41, 22, 31, 64",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** a key sitting in its home slot must have been inserted while that slot was "
                "free; a displaced key must have found every slot from its home up to its final position "
                "already occupied.\n\n"
                "Home slots: 41→1, 52→2, 13→3, 31→1, 22→2, 64→4.\n"
                "- 41, 52, 13 are at home.\n"
                "- 31 is at 4, so slots 1, 2, 3 were full before 31 → 31 comes after 41, 52 **and 13**.\n"
                "- 22 is at 5, so slots 2, 3, 4 were full → 22 comes after 52, 13 **and 31**.\n"
                "- 64 is at 6, so 4 and 5 were full → 64 comes after 31 and 22.\n\n"
                "Check options:\n"
                "- (A) 31 is inserted before 13 → 31 lands in slot 3. ✗\n"
                "- (B) 52, 41, 13, 31 (→ 4), 22 (→ 5), 64 (→ 6). ✓\n"
                "- (C) 22 before 31 → 22 lands in slot 4. ✗\n"
                "- (D) same problem as (C). ✗\n\n"
                "**Trap:** checking only the home-slot keys; the order constraints come from the displaced "
                "keys."
            ),
            "verify": '''
def lp(order):
    T = [None]*10
    for k in order:
        i = k % 10
        while T[i] is not None: i = (i + 1) % 10
        T[i] = k
    return T
tgt = [None, 41, 52, 13, 31, 22, 64, None, None, None]
opts = [[41,52,31,13,22,64], [52,41,13,31,22,64], [13,52,41,22,31,64], [52,13,41,22,31,64]]
assert [c for c, o in zip("ABCD", opts) if lp(o) == tgt] == [ANSWER]
''',
        },
        # ------------------------------------------------------------------ Q6
        {
            "type": "NAT", "marks": 1, "topic": "Binary search on the answer",
            "text": ("Packages with the given weights must be shipped **in order**, using one truck trip per "
                     "day; a day's load is a contiguous group of packages whose total weight must not exceed "
                     "the truck capacity. The program finds the minimum capacity that allows shipping within "
                     "D days. The value printed is ______."),
            "code": '''W, D = [4, 9, 3, 6, 8, 2, 7], 3

def days(cap):
    d, cur = 1, 0
    for w in W:
        if cur + w > cap:
            d, cur = d + 1, 0
        cur += w
    return d

lo, hi = max(W), sum(W)
while lo < hi:
    mid = (lo + hi) // 2
    if days(mid) <= D:
        hi = mid
    else:
        lo = mid + 1
print(lo)''',
            "answer": "16",
            "solution": (
                "**Concept:** `days(cap)` is non-increasing in `cap`, so the feasible capacities form a "
                "suffix [c*, ∞). Binary search over the *answer range* [max(W), sum(W)] = [9, 39] finds the "
                "smallest feasible c*.\n\n"
                "Greedy day counts for candidate capacities:\n"
                "- cap 15: [4, 9] (13) | [3, 6] (9; adding 8 → 17) | [8, 2] (10; adding 7 → 17) | [7] → 4 days ✗\n"
                "- cap 16: [4, 9, 3] (16) | [6, 8, 2] (16) | [7] → 3 days ✓\n\n"
                "Binary search trace: (9, 39) mid 24 ✓ → hi 24; mid 16 ✓ → hi 16; mid 12 ✗ → lo 13; "
                "mid 14 ✗ → lo 15; mid 15 ✗ → lo 16 = hi. Prints **16**.\n\n"
                "Lower bound check: total 39 over 3 days needs at least ⌈39/3⌉ = 13, but contiguity forces more.\n\n"
                "**Trap:** answering 13 (ignoring that packages must stay in order) or 9 (the heaviest package "
                "only)."
            ),
            "verify": "assert int(OUTPUT) == int(ANSWER) and days(15) == 4 and days(16) == 3",
        },
        # ------------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Insertion sort — partial passes",
            "text": ("Insertion sort processes A = [8, 3, 6, 1, 9, 2] by inserting A[1], then A[2], then A[3], "
                     "… into the sorted prefix. The array immediately after A[3] has been inserted (three "
                     "insertions) is"),
            "options": [
                "[3, 6, 8, 1, 9, 2]",
                "[1, 2, 3, 8, 9, 6]",
                "[1, 3, 6, 8, 2, 9]",
                "[1, 3, 6, 8, 9, 2]",
            ],
            "answer": "D",
            "solution": (
                "**Concept:** after inserting A[i], the prefix A[0..i] is sorted and contains exactly the "
                "*original* first i + 1 elements; the suffix is untouched.\n\n"
                "- Insert 3: [3, 8, 6, 1, 9, 2]\n"
                "- Insert 6: [3, 6, 8, 1, 9, 2]\n"
                "- Insert 1: 1 shifts past 8, 6, 3 → [1, 3, 6, 8, 9, 2]\n\n"
                "Answer **[1, 3, 6, 8, 9, 2]** (D).\n\n"
                "**Options:**\n"
                "- (A) is the state after only two insertions.\n"
                "- (B) is selection sort after three passes — it places the global minima 1, 2, 3 at the "
                "front, which insertion sort does not.\n"
                "- (C) changes the suffix, which insertion sort never touches before reaching it.\n\n"
                "**Tip:** insertion sort's invariant is 'prefix sorted', selection sort's is 'prefix sorted "
                "**and** final'."
            ),
            "verify": '''
a = [8, 3, 6, 1, 9, 2]
for i in range(1, 4):
    k, j = a[i], i - 1
    while j >= 0 and a[j] > k:
        a[j+1] = a[j]; j -= 1
    a[j+1] = k
opts = [[3,6,8,1,9,2], [1,2,3,8,9,6], [1,3,6,8,2,9], [1,3,6,8,9,2]]
assert opts["ABCD".index(ANSWER)] == a
''',
        },
        # ------------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Graph representations — adjacency matrix powers",
            "text": ("A is the adjacency matrix of a simple undirected graph G on vertices 1..5, shown below. "
                     "Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "matrix", "title": "Adjacency matrix A",
                          "col_labels": ["1", "2", "3", "4", "5"], "row_labels": ["1", "2", "3", "4", "5"],
                          "rows": [[0, 1, 1, 0, 0], [1, 0, 1, 1, 0], [1, 1, 0, 1, 1], [0, 1, 1, 0, 1],
                                   [0, 0, 1, 1, 0]]}],
            "options": [
                "G has 7 edges",
                "G contains exactly 3 triangles",
                "(A²)[1][4] = 2",
                "(A³)[1][1] = 1",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Concept:** (A^{k})[i][j] counts walks of length k from i to j. In particular (A²)[i][j] "
                "(i ≠ j) counts common neighbours, and (A³)[i][i] = 2 × (number of triangles through i), "
                "since each triangle can be walked in two directions.\n\n"
                "Edges (upper triangle): 1–2, 1–3, 2–3, 2–4, 3–4, 3–5, 4–5.\n\n"
                "- (A) 7 ones above the diagonal → **7 edges**. True.\n"
                "- (B) Triangles: {1, 2, 3}, {2, 3, 4}, {3, 4, 5}. ({1, 3, 4}? 1–4 missing. {2, 4, 5}? 2–5 "
                "missing.) Exactly **3**. True.\n"
                "- (C) N(1) = {2, 3}, N(4) = {2, 3, 5}: common neighbours {2, 3} → 2. True.\n"
                "- (D) Vertex 1 lies on one triangle (1–2–3), giving the closed walks 1→2→3→1 and 1→3→2→1 → "
                "(A³)[1][1] = **2**. False.\n\n"
                "**Trap:** in (D), forgetting that each triangle yields two closed walks (one per direction). "
                "Total triangles = trace(A³)/6."
            ),
            "verify": '''
A = [[0,1,1,0,0],[1,0,1,1,0],[1,1,0,1,1],[0,1,1,0,1],[0,0,1,1,0]]
def mul(X, Y): return [[sum(X[i][k]*Y[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
A2 = mul(A, A); A3 = mul(A2, A)
edges = sum(A[i][j] for i in range(5) for j in range(i+1, 5))
tri = sum(A3[i][i] for i in range(5)) // 6
truth = [edges == 7, tri == 3, A2[0][3] == 2, A3[0][0] == 1]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Heaps — 3-ary max-heap insertion",
            "text": ("A **3-ary** max-heap is stored in an array (0-based): the children of index i are "
                     "3i + 1, 3i + 2, 3i + 3, and the parent of index i > 0 is ⌊(i − 1)/3⌋. The heap is\n\n"
                     "[90, 70, 85, 60, 50, 40, 65, 30, 20, 45, 55]\n\n"
                     "First 88 is inserted, then 95 is inserted (each by appending and sifting up). The index "
                     "at which 88 finally resides is ______."),
            "answer": "12",
            "solution": (
                "**Concept:** sift-up compares a node only with its parent ⌊(i − 1)/3⌋ and swaps while the "
                "parent is smaller. A later insertion can push an earlier key back **down** its path.\n\n"
                "**Insert 88:** appended at index 11. Parent ⌊10/3⌋ = 3 (60) < 88 → swap → 88 at index 3. "
                "Parent ⌊2/3⌋ = 0 (90) > 88 → stop. Heap: [90, 70, 85, 88, 50, 40, 65, 30, 20, 45, 55, 60].\n\n"
                "**Insert 95:** appended at index 12. Parent ⌊11/3⌋ = 3 (88) < 95 → swap → 95 at index 3, "
                "88 moves to **index 12**. Parent 0 (90) < 95 → swap → 95 at the root, 90 at index 3.\n\n"
                "Final: [95, 70, 85, 90, 50, 40, 65, 30, 20, 45, 55, 60, 88]; 88 sits at index **12**.\n\n"
                "**Trap:** using binary-heap parent formula ⌊(i − 1)/2⌋, or answering 3 by forgetting that "
                "95's sift-up path passes through 88's slot."
            ),
            "solution_diagrams": [{"type": "tree", "root": "95",
                                   "children": {"95": ["70", "85", "90"], "70": ["50", "40", "65"],
                                                "85": ["30", "20", "45"], "90": ["55", "60", "88"]},
                                   "caption": "3-ary heap after both insertions (88 is the last leaf, index 12)"}],
            "verify": '''
a = [90, 70, 85, 60, 50, 40, 65, 30, 20, 45, 55]
for x in (88, 95):
    a.append(x); i = len(a) - 1
    while i and a[(i-1)//3] < a[i]:
        a[i], a[(i-1)//3] = a[(i-1)//3], a[i]; i = (i-1)//3
assert a.index(88) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Recurrences — exact evaluation",
            "text": "Let T(1) = 1 and T(n) = 2T(n/2) + n for n a power of 2. The value of T(64) is",
            "options": ["384", "512", "448", "320"],
            "answer": "C",
            "solution": (
                "**Concept:** unrolling the merge-sort-type recurrence: there are log₂ n levels each "
                "contributing n, plus n leaves each costing T(1) = 1, so T(n) = n log₂ n + n.\n\n"
                "Direct evaluation:\n"
                "- T(2) = 2·1 + 2 = 4\n"
                "- T(4) = 2·4 + 4 = 12\n"
                "- T(8) = 2·12 + 8 = 32\n"
                "- T(16) = 2·32 + 16 = 80\n"
                "- T(32) = 2·80 + 32 = 192\n"
                "- T(64) = 2·192 + 64 = **448**\n\n"
                "Closed form: 64 · 6 + 64 = 448. ✓\n\n"
                "**Options:** (A) 384 = n log₂ n forgets the leaf level. (B) 512 = n(log₂ n + 2) "
                "over-counts a level. (D) 320 = n(log₂ n − 1) under-counts.\n\n"
                "**Tip:** the leaf contribution n · T(1) matters for exact values even though it does not "
                "change Θ(n log n)."
            ),
            "verify": '''
def T(n): return 1 if n == 1 else 2 * T(n // 2) + n
assert [384, 512, 448, 320]["ABCD".index(ANSWER)] == T(64) == 64 * 6 + 64
''',
        },
    ],
}
