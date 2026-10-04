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
        # ------------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — lazy generator pipelines",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def gen(xs):
    for x in xs:
        print("g", x, end=" ")
        yield x * x

it = gen([1, 2, 3, 4])
ev = (y for y in it if y % 2 == 0)
print(next(ev), end=" ")
print(sum(it))''',
            "options": [
                "`g 1 g 2 g 3 g 4 4 25`",
                "`g 1 g 2 4 g 3 g 4 25`",
                "`g 1 g 2 4 g 3 g 4 29`",
                "`g 1 g 2 4 g 3 g 4 16`",
            ],
            "answer": "B",
            "solution": (
                "**Concept:** generators are lazy — code inside `gen` runs only when a value is requested. "
                "`ev` does not copy `it`; it pulls from the **same** generator, so whatever `ev` consumes "
                "is gone for later consumers.\n\n"
                "Trace:\n"
                "- Creating `it` and `ev` prints nothing.\n"
                "- `next(ev)` pulls from `it`: prints `g 1`, yields 1 (odd, rejected by the filter); pulls "
                "again: prints `g 2`, yields 4 (even) → `next(ev)` returns 4 and `print(4, end=\" \")`.\n"
                "- `sum(it)` resumes the generator **after** x = 2: prints `g 3` (yields 9), `g 4` (yields 16); "
                "the sum is 9 + 16 = 25.\n\n"
                "Output: `g 1 g 2 4 g 3 g 4 25`.\n\n"
                "**Options:**\n"
                "- (A) assumes the whole generator runs eagerly before anything is printed.\n"
                "- (C) adds the rejected value 4 again (4 + 9 + 16 = 29) — but it was already consumed.\n"
                "- (D) thinks `sum(it)` sums only the even squares (16) — `it` itself is unfiltered.\n\n"
                "**Trap:** believing that `ev` and `it` are independent iterators."
            ),
            "verify": "assert OUTPUT.strip() == 'g 1 g 2 4 g 3 g 4 25' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Quicksort — comparisons and the BST connection",
            "text": ("The quicksort below always uses the **first** element as pivot and makes exactly one "
                     "comparison per non-pivot element in each call. It is run on "
                     "[5, 8, 2, 9, 1, 7, 3, 6, 4]. The value printed is ______."),
            "code": '''comps = 0

def qs(a):
    global comps
    if len(a) <= 1:
        return a
    p, L, R = a[0], [], []
    for x in a[1:]:
        comps += 1
        (L if x < p else R).append(x)
    return qs(L) + [p] + qs(R)

qs([5, 8, 2, 9, 1, 7, 3, 6, 4])
print(comps)''',
            "answer": "16",
            "solution": (
                "**Concept:** this partition is stable, so each subarray keeps the original relative order "
                "and its first element becomes the next pivot. Hence the pivots form exactly the BST obtained "
                "by inserting the keys in the given order, and an element is compared with each of its BST "
                "**ancestors** exactly once. Total comparisons = sum of node depths (internal path length).\n\n"
                "Insert 5, 8, 2, 9, 1, 7, 3, 6, 4 into a BST:\n"
                "- depth 0: 5\n"
                "- depth 1: 2, 8\n"
                "- depth 2: 1, 3 (under 2); 7, 9 (under 8)\n"
                "- depth 3: 4 (right of 3), 6 (left of 7)\n\n"
                "Sum of depths = 2·1 + 4·2 + 2·3 = 2 + 8 + 6 = **16**.\n\n"
                "Check by calls: [5…] 8 comps; [2, 1, 3, 4] 3; [8, 9, 7, 6] 3; [3, 4] 1; [7, 6] 1 → "
                "8 + 3 + 3 + 1 + 1 = 16. ✓\n\n"
                "**Trap:** using n log₂ n ≈ 28.5 or the worst case 36 instead of tracing; or counting two "
                "comparisons per element (as a two-comprehension partition would)."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [5, [2, [1], [3, None, [4]]], [8, [7, [6], None], [9]]],
                                   "caption": "Pivot tree = BST of the input order"}],
            "verify": '''
assert int(OUTPUT) == int(ANSWER)
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in [5, 8, 2, 9, 1, 7, 3, 6, 4]: T = ins(T, k)
def ipl(t, d=0): return 0 if t is None else d + ipl(t[1], d+1) + ipl(t[2], d+1)
assert ipl(T) == 16
''',
        },
        # ------------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Shortest paths — Dijkstra relaxations",
            "text": ("Dijkstra's algorithm is run from S on the weighted directed graph below; a tentative "
                     "distance is changed only when it strictly decreases. Which of the following statements "
                     "is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E"],
                          "edges": [["S", "A", 6], ["S", "B", 2], ["B", "A", 3], ["B", "C", 7], ["B", "E", 12],
                                    ["A", "C", 1], ["A", "D", 5], ["C", "D", 2], ["C", "E", 6], ["D", "E", 1]],
                          "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 1], "D": [6, 2],
                                  "E": [6, 0]}}],
            "options": [
                "The vertices are finalised in the order S, B, A, C, D, E",
                "The shortest distance from S to E is 9",
                "Before E is finalised, its tentative distance takes exactly two distinct finite values",
                "The shortest path from S to E uses exactly 4 edges",
            ],
            "answer": ["A", "B"],
            "solution": (
                "**Concept:** each extraction finalises the closest unfinished vertex and may lower the "
                "tentative distances of its out-neighbours.\n\n"
                "Trace (changes in tentative distances):\n"
                "- Extract S (0): A = 6, B = 2.\n"
                "- Extract B (2): A = min(6, 5) = 5; C = 9; E = 14.\n"
                "- Extract A (5): C = min(9, 6) = 6; D = 10.\n"
                "- Extract C (6): D = min(10, 8) = 8; E = min(14, 12) = 12.\n"
                "- Extract D (8): E = min(12, 9) = 9.\n"
                "- Extract E (9).\n\n"
                "**Verdicts:**\n"
                "- (A) Order S, B, A, C, D, E. **True.**\n"
                "- (B) d(E) = 9. **True.**\n"
                "- (C) E's tentative value goes 14 → 12 → 9: **three** finite values. **False.**\n"
                "- (D) Path: S → B → A → C → D → E (2 + 3 + 1 + 2 + 1 = 9) has **5** edges. **False.**\n\n"
                "**Trap:** the direct-looking edges (S → A = 6, B → E = 12, C → E = 6) are all beaten by "
                "detours; shortest paths minimise weight, not the number of edges."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Tentative distances after each extraction",
                                   "col_labels": ["S", "A", "B", "C", "D", "E"],
                                   "row_labels": ["S", "B", "A", "C", "D", "E"],
                                   "rows": [[0, 6, 2, "∞", "∞", "∞"], [0, 5, 2, 9, "∞", 14],
                                            [0, 5, 2, 6, 10, 14], [0, 5, 2, 6, 8, 12],
                                            [0, 5, 2, 6, 8, 9], [0, 5, 2, 6, 8, 9]]}],
            "verify": '''
import heapq
W = {'S':[('A',6),('B',2)], 'B':[('A',3),('C',7),('E',12)], 'A':[('C',1),('D',5)],
     'C':[('D',2),('E',6)], 'D':[('E',1)], 'E':[]}
d = {v: float('inf') for v in W}; d['S'] = 0; pq = [(0, 'S')]; done = []; hist = []; par = {}
while pq:
    du, u = heapq.heappop(pq)
    if u in done: continue
    done.append(u)
    for v, w in W[u]:
        if du + w < d[v]:
            d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
            if v == 'E': hist.append(d[v])
n, v = 0, 'E'
while v != 'S': v = par[v]; n += 1
truth = [done == list("SBACDE"), d['E'] == 9, len(set(hist)) == 2, n == 4]
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", truth) if ok]
''',
        },
        # ------------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "DFS — counting possible visiting orders",
            "text": ("Depth-first search is started at vertex A of the undirected graph below. At each step "
                     "the algorithm may move to **any** unvisited neighbour of the current vertex (backtracking "
                     "when none exists). The number of distinct orders in which the six vertices can be "
                     "visited (DFS pre-orders) is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F"],
                          "edges": [["A", "B"], ["A", "C"], ["A", "D"], ["B", "E"], ["C", "E"], ["D", "E"],
                                    ["E", "F"]],
                          "pos": {"A": [0, 1], "B": [2, 2], "C": [2, 1], "D": [2, 0], "E": [4, 1],
                                  "F": [6, 1]}}],
            "answer": "18",
            "solution": (
                "**Concept:** count the choices DFS can make, being careful that after backtracking the "
                "set of unvisited neighbours may have shrunk.\n\n"
                "- From A, the first move goes to one of B, C, D: **3** choices. Call it X.\n"
                "- X's neighbours are A and E; A is visited, so DFS is forced to go to **E**.\n"
                "- At E the unvisited neighbours are F and the two vertices of {B, C, D} other than X — call "
                "them Y, Z. Each of F, Y, Z has no unvisited neighbour when reached (Y's neighbours A and E "
                "are both visited; F's only neighbour is E). So DFS visits them one after another, "
                "backtracking to E each time, in **any** order: 3! = **6** orders.\n"
                "- After E, backtracking to X and then A finds nothing new.\n\n"
                "Total = 3 × 6 = **18**.\n\n"
                "Example orders: A B E F C D, A B E C D F, A D E C F B, …\n\n"
                "**Trap:** thinking DFS from A could visit B, then go back to A and visit C directly — "
                "that would skip E, but DFS must exhaust B's branch first, and B → E is available. "
                "Another error is BFS-style counting (3! choices at A × …)."
            ),
            "verify": '''
E = [('A','B'),('A','C'),('A','D'),('B','E'),('C','E'),('D','E'),('E','F')]
G = {}
for u, v in E:
    G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
res = set()
def rec(stack, vis, order):
    if not stack:
        res.add(tuple(order)); return
    u = stack[-1]; nxt = [v for v in G[u] if v not in vis]
    if not nxt:
        rec(stack[:-1], vis, order); return
    for v in nxt: rec(stack + [v], vis | {v}, order + [v])
rec(['A'], {'A'}, ['A'])
assert len(res) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Python — dictionary keys, hashing and equality",
            "text": "Consider the following Python program. What is printed?",
            "code": '''d = {1: 'a', True: 'b', 1.0: 'c', 2: 'd'}
d[2.0] = 'e'
print(len(d), d[1], list(d)[0])''',
            "options": ["`4 c 1`", "`2 a 1`", "`2 c True`", "`2 c 1`"],
            "answer": "D",
            "solution": (
                "**Concept:** a dict (a hash table) treats two keys as the same if they have equal hashes "
                "**and** compare equal. In Python `1 == True == 1.0` and `hash(1) == hash(True) == hash(1.0)`, "
                "so they are a single key. When an existing key is assigned again, the **value** is replaced "
                "but the **original key object** is kept.\n\n"
                "Building the literal left to right:\n"
                "- `1: 'a'` → {1: 'a'}\n"
                "- `True: 'b'` → same key → {1: 'b'} (key stays the int 1)\n"
                "- `1.0: 'c'` → same key → {1: 'c'}\n"
                "- `2: 'd'` → {1: 'c', 2: 'd'}\n"
                "- `d[2.0] = 'e'` → 2.0 == 2 → {1: 'c', 2: 'e'}\n\n"
                "So `len(d)` = 2, `d[1]` = 'c', and the first key in insertion order is the int `1`. "
                "Output `2 c 1`.\n\n"
                "**Options:** (A) treats 1, True, 1.0 as distinct keys. (B) keeps the first value instead of "
                "the last. (C) assumes the key object is replaced too.\n\n"
                "**Trap:** the same rule makes `{1, True, 1.0}` a set of size 1."
            ),
            "verify": "assert OUTPUT.strip() == '2 c 1' and ANSWER == 'D'",
        },
        # ------------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "Linked lists — Floyd's cycle detection",
            "text": ("Nodes with values 1, 2, …, 10 are linked in this order, and the `next` pointer of the "
                     "node with value 10 points back to the node with value 4 (see figure). The program below "
                     "runs Floyd's tortoise-and-hare loop. The value printed is ______."),
            "code": '''slow = fast = head
while True:
    slow = slow.nx
    fast = fast.nx.nx
    if slow is fast:
        break
print(slow.v)''',
            "run_code": False,
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "head": "head",
                          "caption": "Node 10's next pointer goes back to node 4 (not drawn)"}],
            "answer": "8",
            "solution": (
                "**Concept:** let μ = number of nodes before the cycle and λ = cycle length. After k steps "
                "the tortoise is at position k and the hare at 2k (positions counted from the head, 0-based); "
                "they coincide once both are in the cycle and 2k − k = k is a multiple of λ. So k = the "
                "smallest multiple of λ that is ≥ μ.\n\n"
                "Here the cycle is 4 → 5 → … → 10 → 4: λ = 7, and μ = 3 (nodes 1, 2, 3 lead into it).\n"
                "Smallest multiple of 7 that is ≥ 3 is k = 7.\n\n"
                "After 7 steps the tortoise has moved 7 nodes from node 1 → it is at node **8**.\n\n"
                "Step check (tortoise / hare values):\n"
                "- 1: 2 / 3 · 2: 3 / 5 · 3: 4 / 7 · 4: 5 / 9 · 5: 6 / 4 · 6: 7 / 6 · 7: 8 / 8 ✓\n\n"
                "**Trap:** expecting them to meet at the cycle entrance (node 4). That needs the second "
                "phase of Floyd's algorithm: reset one pointer to the head and move both one step at a "
                "time; they meet at node 4 after μ = 3 steps."
            ),
            "verify": '''
class N:
    def __init__(s, v): s.v, s.nx = v, None
ns = [N(i) for i in range(1, 11)]
for a, b in zip(ns, ns[1:]): a.nx = b
ns[-1].nx = ns[3]
slow = fast = ns[0]
while True:
    slow = slow.nx; fast = fast.nx.nx
    if slow is fast: break
assert slow.v == int(ANSWER)
p, q = ns[0], slow
while p is not q: p, q = p.nx, q.nx
assert p.v == 4
''',
        },
        # ------------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Elementary sorts — exact comparison counts",
            "text": ("For an array of n distinct keys, consider these standard implementations: insertion sort "
                     "(inner loop `while j >= 0 and a[j] > key`), selection sort (scan the unsorted suffix for "
                     "the minimum), bubble sort with early exit (stop after a pass with no swap), and top-down "
                     "merge sort. Which of the following statements is/are TRUE?"),
            "options": [
                "Insertion sort makes exactly n − 1 key comparisons on an already-sorted array",
                "Selection sort makes exactly n(n − 1)/2 key comparisons on every input",
                "Merge sort, as usually implemented on arrays, sorts in place using O(1) extra memory",
                "Bubble sort with early exit makes exactly n(n − 1)/2 key comparisons on a reverse-sorted "
                "array",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept:** count comparisons per pass.\n\n"
                "- (A) Sorted input: each key is compared once with its left neighbour, the test fails, and "
                "the loop exits → 1 comparison for each of i = 1..n − 1 → n − 1 total. **True** (the best "
                "case, Θ(n)).\n"
                "- (B) Pass i scans n − 1 − i elements regardless of the data: (n − 1) + (n − 2) + … + 1 = "
                "n(n − 1)/2. **True** — selection sort is not adaptive.\n"
                "- (C) The standard array merge needs an auxiliary array of Θ(n). **False.**\n"
                "- (D) Reverse-sorted input: every pass swaps, so all n − 1 passes are needed, with "
                "n − 1, n − 2, …, 1 comparisons → n(n − 1)/2. Early exit never triggers. **True.**\n\n"
                "For n = 8: insertion (sorted) 7; selection 28; bubble (reversed) 28.\n\n"
                "**Trap:** in (D), thinking the early-exit flag saves a final pass — it only helps when the "
                "array becomes sorted before the last pass, which cannot happen with reversed input (the "
                "smallest element moves left only one position per pass)."
            ),
            "verify": '''
def ins_c(a):
    a = a[:]; c = 0
    for i in range(1, len(a)):
        k, j = a[i], i - 1
        while j >= 0:
            c += 1
            if a[j] > k: a[j+1] = a[j]; j -= 1
            else: break
        a[j+1] = k
    return c
def sel_c(a):
    a = a[:]; c = 0
    for i in range(len(a) - 1):
        m = i
        for j in range(i + 1, len(a)):
            c += 1
            if a[j] < a[m]: m = j
        a[i], a[m] = a[m], a[i]
    return c
def bub_c(a):
    a = a[:]; c = 0; p = 0
    while True:
        p += 1; s = False
        for j in range(len(a) - p):
            c += 1
            if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]; s = True
        if not s or p == len(a) - 1: break
    return c
import random
n = 8
A = ins_c(list(range(n))) == n - 1
B = all(sel_c(random.sample(range(50), n)) == n*(n-1)//2 for _ in range(20))
D = bub_c(list(range(n, 0, -1))) == n*(n-1)//2
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", [A, B, False, D]) if ok]
''',
        },
        # ------------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Binary search trees — insertion orders producing a tree",
            "text": ("The number of permutations of the keys {20, 30, 35, 40, 50, 70, 80} which, when inserted "
                     "in that order into an initially empty BST, produce exactly the tree shown below "
                     "is ______."),
            "diagrams": [{"type": "bintree",
                          "tree": [50, [30, [20], [40, [35], None]], [70, None, [80]]],
                          "caption": "Target BST"}],
            "answer": "45",
            "solution": (
                "**Concept:** a permutation produces the tree iff every node is inserted before all its "
                "descendants. The root must come first; the left and right subtrees' insertion sequences "
                "can be **interleaved** arbitrarily. Hence\n"
                "N(T) = C(|L| + |R|, |L|) · N(L) · N(R), equivalently n! / Π (subtree size of every node).\n\n"
                "Subtree sizes: 50 → 7, 30 → 4, 20 → 1, 40 → 2, 35 → 1, 70 → 2, 80 → 1.\n\n"
                "**Recursive count:**\n"
                "- Subtree 40 (with 35): 1 order (40, 35).\n"
                "- Subtree 30: root 30 then interleave {20} (size 1) with {40, 35} (size 2): C(3, 1) = 3.\n"
                "- Subtree 70: 1 order (70, 80).\n"
                "- Root 50: interleave left (size 4, 3 orders) with right (size 2, 1 order): "
                "C(6, 2) · 3 · 1 = 15 · 3 = **45**.\n\n"
                "**Formula check:** 7! / (7 · 4 · 1 · 2 · 1 · 2 · 1) = 5040 / 112 = 45. ✓\n\n"
                "**Trap:** multiplying only N(L) · N(R) = 3 (forgetting the interleavings) or using "
                "the number of BST *shapes* (Catalan numbers), which answers a different question."
            ),
            "verify": '''
import itertools
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
target = [50, [30, [20, None, None], [40, [35, None, None], None]], [70, None, [80, None, None]]]
cnt = 0
for p in itertools.permutations([20, 30, 35, 40, 50, 70, 80]):
    if p[0] != 50: continue
    t = None
    for k in p: t = ins(t, k)
    cnt += (t == target)
assert cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Stacks — infix to prefix conversion",
            "text": ("Operators have the usual precedence: `^` (highest, right-associative) > `*`, `/` "
                     "(left-associative) > `+`, `-` (left-associative). The prefix (Polish) form of\n\n"
                     "`( a + b ) * c - d / ( e - f ) ^ g`\n\n"
                     "is"),
            "options": [
                "`- * + a b c ^ / d - e f g`",
                "`* + a b - c / d ^ - e f g`",
                "`- * + a b c / d ^ - e f g`",
                "`- + a b * c / d ^ - e f g`",
            ],
            "answer": "C",
            "solution": (
                "**Concept:** build the expression tree from precedence and associativity, then read it in "
                "pre-order (operator before its operands). (Equivalently: reverse the infix, swap brackets, "
                "convert with a stack, reverse the result — taking care with associativity.)\n\n"
                "Parsing:\n"
                "- `^` binds tightest: (e − f) ^ g.\n"
                "- `/` next: d / ((e − f) ^ g).\n"
                "- `*`: (a + b) * c.\n"
                "- `-` at the top: [(a + b) * c] − [d / ((e − f) ^ g)].\n\n"
                "Pre-order: `-`, then left `* + a b c`, then right `/ d ^ - e f g` → "
                "`- * + a b c / d ^ - e f g`, which is option (C).\n\n"
                "**Options:**\n"
                "- (A) groups (d / (e − f)) ^ g, giving `/` lower priority than it has relative to `^`.\n"
                "- (B) makes `*` the root, i.e. (a + b) * (c − …), ignoring that `-` has lower precedence.\n"
                "- (D) reads as (a + b) − …, dropping the multiplication by c into the right operand.\n\n"
                "**Tip:** verify by evaluating with sample values, e.g. a = 1, b = 2, c = 3, d = 8, e = 5, "
                "f = 3, g = 2: infix value 9 − 8/4 = 7, and the prefix in (C) gives 7 as well."
            ),
            "solution_diagrams": [{"type": "tree", "root": "−",
                                   "children": {"−": ["*", "/"], "*": ["+", "c"], "+": ["a", "b"],
                                                "/": ["d", "^"], "^": ["−₂", "g"], "−₂": ["e", "f"]},
                                   "caption": "Expression tree (−₂ is the inner subtraction)"}],
            "verify": '''
def ev_prefix(tokens, env):
    st = []
    for t in reversed(tokens.split()):
        if t.isalpha(): st.append(env[t])
        else:
            a, b = st.pop(), st.pop()
            try:
                st.append({'+': lambda: a+b, '-': lambda: a-b, '*': lambda: a*b,
                           '/': lambda: a/b, '^': lambda: a**b}[t]())
            except (OverflowError, ZeroDivisionError):
                return None
    return st[0] if len(st) == 1 else None
import random
opts = ["- * + a b c ^ / d - e f g", "* + a b - c / d ^ - e f g",
        "- * + a b c / d ^ - e f g", "- + a b * c / d ^ - e f g"]
good = []
for c, o in zip("ABCD", opts):
    ok = True
    for _ in range(30):
        env = {k: random.randint(1, 5) for k in "abcdfg"}
        env['e'] = env['f'] + random.randint(1, 3)
        want = (env['a'] + env['b']) * env['c'] - env['d'] / (env['e'] - env['f']) ** env['g']
        got = ev_prefix(o, env)
        if got is None or abs(got - want) > 1e-9: ok = False
    if ok: good.append(c)
assert good == [ANSWER]
''',
        },
        # ------------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Graph theory — edges, components and connectivity",
            "text": "Consider simple undirected graphs (no loops, no multi-edges). Which of the following statements is/are TRUE?",
            "options": [
                "The maximum number of edges in a graph with 10 vertices and exactly 3 connected components is 28",
                "Every graph with 10 vertices and 37 edges is connected",
                "Every graph with 6 vertices in which every vertex has degree at least 2 is connected",
                "A forest (acyclic graph) with 10 vertices and 3 connected components has exactly 8 edges",
            ],
            "answer": ["A", "B"],
            "solution": (
                "**Concept:** to maximise edges with k components on n vertices, make k − 1 components single "
                "vertices and the last one a complete graph K_{n−k+1}. A forest with c components on n "
                "vertices has n − c edges.\n\n"
                "- (A) K₈ plus two isolated vertices: C(8, 2) = 28 edges. Any more balanced split has fewer "
                "edges (e.g. 6 + 2 + 2 vertices → 15 + 1 + 1). **True.**\n"
                "- (B) The maximum number of edges in a *disconnected* graph on 10 vertices is C(9, 2) = 36 "
                "(K₉ plus an isolated vertex). So 37 edges force connectivity. **True.**\n"
                "- (C) Two disjoint triangles: 6 vertices, all of degree 2, yet 2 components. **False.** "
                "(Minimum degree ≥ (n − 1)/2 = 2.5, i.e. ≥ 3, would guarantee connectivity.)\n"
                "- (D) A forest with 10 vertices and 3 trees has 10 − 3 = **7** edges. **False.**\n\n"
                "**Trap:** in (A), splitting the vertices evenly feels natural but minimises, not maximises, "
                "the edge count, because C(m, 2) is convex."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["1", "2", "3", "4", "5", "6"],
                                   "edges": [["1", "2"], ["2", "3"], ["1", "3"], ["4", "5"], ["5", "6"],
                                             ["4", "6"]],
                                   "pos": {"1": [0, 0], "2": [2, 0], "3": [1, 1.6], "4": [4, 0], "5": [6, 0],
                                           "6": [5, 1.6]},
                                   "caption": "Counterexample to (C): degree 2 everywhere, but disconnected"}],
            "verify": '''
from math import comb
from itertools import combinations_with_replacement
best = max(sum(comb(x, 2) for x in p) for p in combinations_with_replacement(range(1, 11), 3) if sum(p) == 10)
best_disc = max(comb(k, 2) + comb(10 - k, 2) for k in range(1, 10))
A = best == 28
B = best_disc == 36
C = False   # two disjoint triangles are a counterexample
D = (10 - 3) == 8
assert sorted(ANSWER) == [x for x, ok in zip("ABCD", [A, B, C, D]) if ok]
''',
        },
    ],
}
