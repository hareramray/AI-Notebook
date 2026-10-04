# Set 15 — Shortest Paths
SET = {
    "number": 15,
    "title": "Shortest Paths",
    "difficulty": "Moderate",
    "focus": "Dijkstra traces, BFS shortest paths, path counting",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Shortest paths — Dijkstra extraction order",
            "text": ("Dijkstra's algorithm is run from S on the weighted undirected graph shown. In "
                     "which order are the vertices removed from the priority queue (finalised)?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["S", "A", "B", "C", "D", "E"],
                          "edges": [["S", "A", 4], ["S", "B", 1], ["B", "A", 2], ["B", "C", 6],
                                    ["A", "C", 3], ["A", "D", 7], ["C", "D", 1], ["C", "E", 5],
                                    ["D", "E", 2]],
                          "pos": {"S": [0, 1], "A": [2, 2.2], "B": [2, -0.2], "C": [4, -0.2],
                                  "D": [4, 2.2], "E": [6, 1]}}],
            "options": ["S, B, A, C, D, E", "S, B, A, D, C, E",
                        "S, B, C, A, D, E", "S, A, B, C, D, E"],
            "answer": "A",
            "solution": (
                "**Concept.** Dijkstra always finalises the unvisited vertex with the smallest "
                "tentative distance, so vertices are finalised in non-decreasing order of their "
                "true shortest distance.\n\n"
                "Trace:\n"
                "- S (0): A = 4, B = 1.\n"
                "- B (1): A = min(4, 1 + 2) = 3, C = 1 + 6 = 7.\n"
                "- A (3): C = min(7, 3 + 3) = 6, D = 3 + 7 = 10.\n"
                "- C (6): D = min(10, 6 + 1) = 7, E = 6 + 5 = 11.\n"
                "- D (7): E = min(11, 7 + 2) = 9.\n"
                "- E (9).\n\n"
                "Order: S, B, A, C, D, E → (A).\n\n"
                "- (B) finalises D before C — but D's distance (7) depends on C (6).\n"
                "- (C) finalises C at 7 via B, before A's improvement to 6 is seen.\n"
                "- (D) takes A before B, ignoring that B (1) is closer than A (4).\n\n"
                "**Trap:** the direct edges S–A (4) and A–D (7) are never on a shortest path."
            ),
            "verify": '''
import heapq
E = [("S","A",4),("S","B",1),("B","A",2),("B","C",6),("A","C",3),("A","D",7),
     ("C","D",1),("C","E",5),("D","E",2)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {"S": 0}; done = []; pq = [(0, "S")]
while pq:
    du, u = heapq.heappop(pq)
    if u in done: continue
    done.append(u)
    for v, w in G[u]:
        if du + w < d.get(v, 1e9): d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert ", ".join(done) == "S, B, A, C, D, E" and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — tracing mid values",
            "text": ("The function below is called as `bs(A, 60)` on the sorted array A shown "
                     "(0-based). The sum of all values taken by `mid` during the call is ______."),
            "code": '''def bs(A, x):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] == x:
            return mid
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1''',
            "diagrams": [{"type": "array", "values": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 99],
                          "label": "A"}],
            "answer": "26",
            "solution": (
                "**Concept.** Each iteration computes `mid = (lo + hi) // 2`, compares A[mid] with "
                "x and discards half of the range. 60 is absent, so the loop runs until lo > hi.\n\n"
                "Trace:\n"
                "- lo 0, hi 10 → mid 5 (23) < 60 → lo = 6\n"
                "- lo 6, hi 10 → mid 8 (72) > 60 → hi = 7\n"
                "- lo 6, hi 7 → mid 6 (38) < 60 → lo = 7\n"
                "- lo 7, hi 7 → mid 7 (56) < 60 → lo = 8; now lo > hi, return −1.\n\n"
                "Sum of mids = 5 + 8 + 6 + 7 = **26**.\n\n"
                "**Trap:** with `//` the mid of (6, 7) is 6, not 7. Note also that the final value of "
                "`lo` (8) is the insertion point of 60 — the index of the first element > 60."
            ),
            "verify": '''
A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 99]
lo, hi, s = 0, len(A) - 1, 0
while lo <= hi:
    mid = (lo + hi) // 2; s += mid
    if A[mid] == 60: break
    if A[mid] < 60: lo = mid + 1
    else: hi = mid - 1
assert s == int(ANSWER) and bs(A, 60) == -1
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Python — dictionaries and max with key",
            "text": "Consider the following Python program. What is printed?",
            "code": '''d = {}
for w in "the cat and the hat and the bat".split():
    d[w[-2:]] = d.get(w[-2:], 0) + len(w)
print(len(d), max(d, key=d.get), d["at"])''',
            "options": ["`3 he 9`", "`3 at 9`", "`4 he 9`", "`3 he 3`"],
            "answer": "A",
            "solution": (
                "**Concept.** `d.get(k, 0)` returns 0 for a missing key, so the loop accumulates "
                "word lengths grouped by the last two letters. `max(d, key=d.get)` returns the "
                "**first** key (in insertion order) attaining the maximum value.\n\n"
                "Trace (all words have length 3):\n"
                "- \"the\" ×3 → key `he`: 9\n"
                "- \"cat\", \"hat\", \"bat\" → key `at`: 9\n"
                "- \"and\" ×2 → key `nd`: 6\n\n"
                "Insertion order is `he`, `at`, `nd`. Both `he` and `at` have 9; `max` keeps the first "
                "maximum it meets, which is `he`. Output: `3 he 9` → (A).\n\n"
                "- (B) assumes ties go to the later key.\n"
                "- (C) counts four distinct words-endings, but `cat/hat/bat` share `at`.\n"
                "- (D) counts occurrences instead of summing lengths.\n\n"
                "**Tip:** `max`/`min` are stable in the sense that they return the first of equal "
                "candidates; dicts preserve insertion order since Python 3.7."
            ),
            "verify": "assert OUTPUT.strip() == '3 he 9'",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Python — floor division and modulo with negatives",
            "text": "Which of the following Python 3 expressions evaluate to `True`?",
            "options": ["`-7 // 2 == -3`", "`-7 % 3 == 2`", "`7 % -3 == -2`",
                        "`int(-7 / 2) == -7 // 2`"],
            "answer": ["B", "C"],
            "solution": (
                "**Concept.** Python's `//` floors (rounds toward −∞) and `%` is defined so that "
                "`a == (a // b) * b + a % b`; hence the remainder takes the **sign of the divisor**. "
                "`int()` truncates toward 0.\n\n"
                "- (A) −7 / 2 = −3.5, floor → −4. So `-7 // 2` is −4 ≠ −3. **False.**\n"
                "- (B) −7 // 3 = −3 (floor of −2.33), remainder −7 − (−9) = 2. **True.**\n"
                "- (C) 7 // −3 = −3 (floor of −2.33), remainder 7 − 9 = −2. **True.**\n"
                "- (D) `int(-3.5)` = −3 (truncation) but `-7 // 2` = −4. **False.**\n\n"
                "**Trap:** C and Java truncate toward zero, so −7 / 2 is −3 there and −7 % 3 is −1. "
                "Python differs whenever the operands have opposite signs."
            ),
            "verify": '''
truth = {"A": -7 // 2 == -3, "B": -7 % 3 == 2, "C": 7 % -3 == -2, "D": int(-7 / 2) == -7 // 2}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Queues — circular array arithmetic",
            "text": ("A circular queue is implemented in an array Q[0..7]. `front` is the index of the "
                     "first element and `rear` is the index of the next free slot; enqueue writes "
                     "Q[rear] then sets rear = (rear + 1) mod 8, and dequeue sets "
                     "front = (front + 1) mod 8. Initially front = rear = 5 (empty queue). The "
                     "operations performed are: 6 enqueues, then 4 dequeues, then 3 enqueues. "
                     "The index of the slot that holds the **most recently enqueued** element "
                     "is ______."),
            "answer": "5",
            "solution": (
                "**Concept.** Index arithmetic is modulo the array size. Count enqueues for `rear` "
                "and dequeues for `front`; the last element written sits at (rear − 1) mod 8.\n\n"
                "- Total enqueues = 6 + 3 = 9 → rear = (5 + 9) mod 8 = 14 mod 8 = 6.\n"
                "- Total dequeues = 4 → front = (5 + 4) mod 8 = 1.\n"
                "- Size never exceeds 6 (after the first 6 enqueues) and ends at 9 − 4 = 5, so the "
                "queue never overflows (capacity 7 with one slot kept empty).\n"
                "- Last enqueued element is at (6 − 1) mod 8 = **5**.\n\n"
                "Slot-by-slot: the 9 enqueues write slots 5, 6, 7, 0, 1, 2, 3, 4, 5 — the 9th write "
                "reuses slot 5, which was freed by the first dequeue.\n\n"
                "**Trap:** answering 6 (the value of `rear`, which is the next *free* slot)."
            ),
            "solution_diagrams": [{"type": "array", "values": ["", "e5", "e6", "e7", "e8", "e9", "", ""],
                                   "pointers": {"front": 1, "rear": 6}, "highlight": [5],
                                   "caption": "Final state (e_{i} = i-th enqueued element)"}],
            "verify": '''
front = rear = 5; size = 0; last = None
for op in ["E"]*6 + ["D"]*4 + ["E"]*3:
    if op == "E":
        assert size < 7; last = rear; rear = (rear + 1) % 8; size += 1
    else:
        front = (front + 1) % 8; size -= 1
assert last == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search trees — insertion",
            "text": ("The keys 50, 27, 73, 14, 39, 61, 88, 33, 45, 30 are inserted in that order into "
                     "an initially empty binary search tree. The sequence of keys on the path from "
                     "the root to the node containing 30 is"),
            "options": ["50, 27, 39, 33, 30", "50, 27, 14, 30",
                        "50, 27, 39, 30", "50, 27, 33, 30"],
            "answer": "A",
            "solution": (
                "**Concept.** Each key is inserted as a leaf by walking down from the root: go left "
                "if smaller, right if larger.\n\n"
                "Insertions:\n"
                "- 50 root; 27 → L of 50; 73 → R of 50.\n"
                "- 14 → L of 27; 39 → R of 27; 61 → L of 73; 88 → R of 73.\n"
                "- 33: 50 → L, 27 → R, 39 → L ⇒ left child of 39.\n"
                "- 45: 50 → L, 27 → R, 39 → R ⇒ right child of 39.\n"
                "- 30: 50 → L (30 < 50), 27 → R (30 > 27), 39 → L (30 < 39), 33 → L (30 < 33) "
                "⇒ left child of 33.\n\n"
                "Path: 50, 27, 39, 33, 30 → (A).\n\n"
                "- (B) goes left at 27; but 30 > 27.\n"
                "- (C) skips 33, which was inserted before 30 and is on the way.\n"
                "- (D) skips 39.\n\n"
                "**Tip:** the depth of 30 is 4 — later keys always hang below earlier keys on their path."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [50, [27, [14], [39, [33, [30], None], [45]]],
                                            [73, [61], [88]]],
                                   "highlight": [50, 27, 39, 33, 30],
                                   "caption": "Final BST, path to 30 highlighted"}],
            "verify": '''
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
t = None
for k in [50, 27, 73, 14, 39, 61, 88, 33, 45, 30]: t = ins(t, k)
path, n = [], t
while n[0] != 30:
    path.append(n[0]); n = n[1] if 30 < n[0] else n[2]
path.append(30)
assert path == [50, 27, 39, 33, 30] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — linear probing",
            "text": ("The keys 33, 46, 18, 57, 24, 13, 70, 35 are inserted in that order into an "
                     "initially empty hash table with 11 slots (0–10) using h(k) = k mod 11 and "
                     "linear probing (next slot = (i + 1) mod 11). A *probe* is one inspection of a "
                     "slot, including the slot where the key is finally placed. The total number of "
                     "probes over all eight insertions is ______."),
            "answer": "22",
            "solution": (
                "**Concept.** Linear probing scans consecutive slots from the home slot until an "
                "empty one is found. Runs of occupied slots (clusters) grow and lengthen later "
                "probe sequences — primary clustering.\n\n"
                "Trace (home slot → final slot, probes):\n"
                "- 33 → 0 → 0 (1)\n- 46 → 2 → 2 (1)\n- 18 → 7 → 7 (1)\n"
                "- 57 → 2 → 3 (2)\n- 24 → 2 → 4 (3)\n- 13 → 2 → 5 (4)\n"
                "- 70 → 4 → 6 (3: slots 4, 5, 6)\n"
                "- 35 → 2 → 8 (7: slots 2, 3, 4, 5, 6, 7, 8)\n\n"
                "Total = 1 + 1 + 1 + 2 + 3 + 4 + 3 + 7 = **22**.\n\n"
                "**Trap:** 70 hashes to 4, which is *not* its own collision chain, yet it collides "
                "because the cluster started at slot 2 has grown over slot 4."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 33, 2: 46, 3: 57, 4: 24, 5: 13, 6: 70, 7: 18, 8: 35},
                                   "caption": "Final table"}],
            "verify": '''
T = [None]*11; tot = 0
for k in [33, 46, 18, 57, 24, 13, 70, 35]:
    i = k % 11; tot += 1
    while T[i] is not None: i = (i + 1) % 11; tot += 1
    T[i] = k
assert tot == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Selection sort — intermediate state",
            "text": ("Selection sort (ascending) is applied to [29, 10, 14, 37, 13, 5, 41]. In pass i "
                     "(i = 0, 1, 2, …) the minimum of A[i..n−1] is found and swapped with A[i] (a swap "
                     "with itself changes nothing). What is the array after **three** passes?"),
            "options": ["[5, 10, 13, 37, 14, 29, 41]", "[5, 10, 13, 14, 29, 37, 41]",
                        "[5, 10, 14, 37, 13, 29, 41]", "[5, 10, 13, 29, 14, 37, 41]"],
            "answer": "A",
            "solution": (
                "**Concept.** After k passes of selection sort, A[0..k−1] holds the k smallest "
                "elements in order; the remainder is permuted only by the swaps performed.\n\n"
                "- Pass 0: min of whole array = 5 (index 5); swap with 29 → [5, 10, 14, 37, 13, 29, 41].\n"
                "- Pass 1: min of A[1..] = 10 at index 1 → self-swap, unchanged.\n"
                "- Pass 2: min of A[2..] = 13 (index 4); swap with 14 → [5, 10, 13, 37, 14, 29, 41].\n\n"
                "Answer (A).\n\n"
                "- (B) is the fully sorted array.\n"
                "- (C) is the state after only two passes.\n"
                "- (D) assumes the unsorted tail is also re-ordered, which selection sort never does.\n\n"
                "**Trap:** 14 moves *to the right* (to index 4) in pass 2 — selection sort is not "
                "stable and can carry elements far from their final place."
            ),
            "verify": '''
A = [29, 10, 14, 37, 13, 5, 41]
for i in range(3):
    m = min(range(i, len(A)), key=lambda j: A[j])
    A[i], A[m] = A[m], A[i]
assert A == [5, 10, 13, 37, 14, 29, 41] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Graphs — counting walks with the adjacency matrix",
            "text": ("The adjacency matrix M of a directed graph on vertices 1, 2, 3, 4 is shown "
                     "(M[i][j] = 1 iff there is an edge i → j). The number of directed walks of "
                     "length exactly 3 (three edges, vertices may repeat) from vertex 4 to vertex 1 "
                     "is ______."),
            "diagrams": [{"type": "matrix", "title": "M",
                          "row_labels": ["1", "2", "3", "4"], "col_labels": ["1", "2", "3", "4"],
                          "rows": [[0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 0]]}],
            "answer": "3",
            "solution": (
                "**Concept.** (M^{k})[i][j] counts walks of length k from i to j, because each "
                "matrix product sums over the possible intermediate vertex.\n\n"
                "Edges: 1→2, 1→3, 2→3, 2→4, 3→1, 3→4, 4→1, 4→2.\n\n"
                "Enumerate 4 → x → y → 1 directly. Vertices with an edge into 1 are 3 and 4, so "
                "y ∈ {3, 4}:\n"
                "- 4 → 1 → 3 → 1 ✓ (4→1, 1→3, 3→1)\n"
                "- 4 → 2 → 3 → 1 ✓\n"
                "- 4 → 2 → 4 → 1 ✓\n"
                "- 4 → 1 → 4? no edge 1→4; 4 → 4? no self-loop.\n\n"
                "Total **3** walks, which equals (M³)[4][1].\n\n"
                "**Trap:** walks may revisit vertices (4 → 2 → 4 → 1 is allowed). Counting only "
                "simple paths would give only 1 (4 → 2 → 3 → 1)."
            ),
            "verify": '''
M = [[0,1,1,0],[0,0,1,1],[1,0,0,1],[1,1,0,0]]
def mul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
M3 = mul(mul(M, M), M)
assert M3[3][0] == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Merge sort — comparisons in a merge",
            "text": ("The standard merge procedure combines the sorted lists L = [4, 11, 15, 32, 38] "
                     "and R = [6, 9, 12, 13]. It compares the front elements, outputs the smaller, "
                     "and when one list is exhausted copies the rest of the other **without "
                     "comparisons**. The number of key comparisons made is"),
            "options": ["6", "7", "8", "9"],
            "answer": "A",
            "solution": (
                "**Concept.** Each comparison outputs exactly one element; comparisons stop as soon "
                "as one list empties. For lists of sizes m and n the count lies between min(m, n) "
                "and m + n − 1.\n\n"
                "Trace (L front vs R front → output):\n"
                "- 4 vs 6 → 4\n- 11 vs 6 → 6\n- 11 vs 9 → 9\n- 11 vs 12 → 11\n"
                "- 15 vs 12 → 12\n- 15 vs 13 → 13 — R is now empty.\n"
                "- Copy 15, 32, 38 with no comparisons.\n\n"
                "Total = **6** → (A).\n\n"
                "- (B) 7 counts one extra comparison after R empties.\n"
                "- (D) 9 = m + n − 1 is the worst case (lists interleave until the very end).\n\n"
                "**Tip:** the number of comparisons = (m + n) − (number of elements copied after "
                "exhaustion) = 9 − 3 = 6."
            ),
            "verify": '''
L, R = [4, 11, 15, 32, 38], [6, 9, 12, 13]; i = j = c = 0
while i < len(L) and j < len(R):
    c += 1
    if L[i] <= R[j]: i += 1
    else: j += 1
assert c == 6 and ANSWER == "A"
''',
        },
    ],
}
