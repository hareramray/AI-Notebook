# Set 15 — Shortest Paths
SET = {
    'number': 15,
    'title': 'Shortest Paths',
    'difficulty': 'Moderate',
    'focus': 'Dijkstra traces, BFS shortest paths, path counting',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Shortest paths — Dijkstra extraction order',
            'text': "Dijkstra's algorithm is run from S on the weighted undirected graph shown. In which order are the vertices removed from the priority queue (finalised)?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 1],
                        ['B', 'A', 2],
                        ['B', 'C', 6],
                        ['A', 'C', 3],
                        ['A', 'D', 7],
                        ['C', 'D', 1],
                        ['C', 'E', 5],
                        ['D', 'E', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, -0.2],
                        'D': [4, 2.2],
                        'E': [6, 1],
                    },
                },
            ],
            'options': ['S, B, A, C, D, E', 'S, B, A, D, C, E', 'S, B, C, A, D, E', 'S, A, B, C, D, E'],
            'answer': 'A',
            'solution': '''**Concept.** Dijkstra always finalises the unvisited vertex with the smallest tentative distance, so vertices are finalised in non-decreasing order of their true shortest distance.

Trace:
- S (0): A = 4, B = 1.
- B (1): A = min(4, 1 + 2) = 3, C = 1 + 6 = 7.
- A (3): C = min(7, 3 + 3) = 6, D = 3 + 7 = 10.
- C (6): D = min(10, 6 + 1) = 7, E = 6 + 5 = 11.
- D (7): E = min(11, 7 + 2) = 9.
- E (9).

Order: S, B, A, C, D, E → (A).

- (B) finalises D before C — but D's distance (7) depends on C (6).
- (C) finalises C at 7 via B, before A's improvement to 6 is seen.
- (D) takes A before B, ignoring that B (1) is closer than A (4).

**Trap:** the direct edges S–A (4) and A–D (7) are never on a shortest path.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

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
assert ", ".join(done) == "S, B, A, C, D, E" and ANSWER == "B"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — tracing mid values',
            'text': 'The function below is called as `bs(A, 60)` on the sorted array A shown (0-based). The sum of all values taken by `mid` during the call is ______.',
            'code': '''def bs(A, x):
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
            'diagrams': [
                {
                    'type': 'array',
                    'values': [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 99],
                    'label': 'A',
                },
            ],
            'answer': '26',
            'solution': '''**Concept.** Each iteration computes `mid = (lo + hi) // 2`, compares A[mid] with x and discards half of the range. 60 is absent, so the loop runs until lo > hi.

Trace:
- lo 0, hi 10 → mid 5 (23) < 60 → lo = 6
- lo 6, hi 10 → mid 8 (72) > 60 → hi = 7
- lo 6, hi 7 → mid 6 (38) < 60 → lo = 7
- lo 7, hi 7 → mid 7 (56) < 60 → lo = 8; now lo > hi, return −1.

Sum of mids = 5 + 8 + 6 + 7 = **26**.

**Trap:** with `//` the mid of (6, 7) is 6, not 7. Note also that the final value of `lo` (8) is the insertion point of 60 — the index of the first element > 60.''',
            'verify': '''
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
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — dictionaries and max with key',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''d = {}
for w in "the cat and the hat and the bat".split():
    d[w[-2:]] = d.get(w[-2:], 0) + len(w)
print(len(d), max(d, key=d.get), d["at"])''',
            'options': ['`4 he 9`', '`3 he 9`', '`3 at 9`', '`3 he 3`'],
            'answer': 'B',
            'solution': '''**Concept.** `d.get(k, 0)` returns 0 for a missing key, so the loop accumulates word lengths grouped by the last two letters. `max(d, key=d.get)` returns the **first** key (in insertion order) attaining the maximum value.

Trace (all words have length 3):
- "the" ×3 → key `he`: 9
- "cat", "hat", "bat" → key `at`: 9
- "and" ×2 → key `nd`: 6

Insertion order is `he`, `at`, `nd`. Both `he` and `at` have 9; `max` keeps the first maximum it meets, which is `he`. Output: `3 he 9` → (B).

- (A) counts four distinct words-endings, but `cat/hat/bat` share `at`.
- (C) assumes ties go to the later key.
- (D) counts occurrences instead of summing lengths.

**Tip:** `max`/`min` are stable in the sense that they return the first of equal candidates; dicts preserve insertion order since Python 3.7.''',
            'verify': "ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '3 he 9'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'Which of the following Python 3 expressions evaluate to `True`?',
            'options': ['`-7 // 2 == -3`', '`-7 % 3 == 2`', '`7 % -3 == -2`', '`int(-7 / 2) == -7 // 2`'],
            'answer': ['B', 'C'],
            'solution': '''**Concept.** Python's `//` floors (rounds toward −∞) and `%` is defined so that `a == (a // b) * b + a % b`; hence the remainder takes the **sign of the divisor**. `int()` truncates toward 0.

- (A) −7 / 2 = −3.5, floor → −4. So `-7 // 2` is −4 ≠ −3. **False.**
- (B) −7 // 3 = −3 (floor of −2.33), remainder −7 − (−9) = 2. **True.**
- (C) 7 // −3 = −3 (floor of −2.33), remainder 7 − 9 = −2. **True.**
- (D) `int(-3.5)` = −3 (truncation) but `-7 // 2` = −4. **False.**

**Trap:** C and Java truncate toward zero, so −7 / 2 is −3 there and −7 % 3 is −1. Python differs whenever the operands have opposite signs.''',
            'verify': '''
truth = {"A": -7 // 2 == -3, "B": -7 % 3 == 2, "C": 7 % -3 == -2, "D": int(-7 / 2) == -7 // 2}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Queues — circular array arithmetic',
            'text': 'A circular queue is implemented in an array Q[0..7]. `front` is the index of the first element and `rear` is the index of the next free slot; enqueue writes Q[rear] then sets rear = (rear + 1) mod 8, and dequeue sets front = (front + 1) mod 8. Initially front = rear = 5 (empty queue). The operations performed are: 6 enqueues, then 4 dequeues, then 3 enqueues. The index of the slot that holds the **most recently enqueued** element is ______.',
            'answer': '5',
            'solution': '''**Concept.** Index arithmetic is modulo the array size. Count enqueues for `rear` and dequeues for `front`; the last element written sits at (rear − 1) mod 8.

- Total enqueues = 6 + 3 = 9 → rear = (5 + 9) mod 8 = 14 mod 8 = 6.
- Total dequeues = 4 → front = (5 + 4) mod 8 = 1.
- Size never exceeds 6 (after the first 6 enqueues) and ends at 9 − 4 = 5, so the queue never overflows (capacity 7 with one slot kept empty).
- Last enqueued element is at (6 − 1) mod 8 = **5**.

Slot-by-slot: the 9 enqueues write slots 5, 6, 7, 0, 1, 2, 3, 4, 5 — the 9th write reuses slot 5, which was freed by the first dequeue.

**Trap:** answering 6 (the value of `rear`, which is the next *free* slot).''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': ['', 'e5', 'e6', 'e7', 'e8', 'e9', '', ''],
                    'pointers': {
                        'front': 1,
                        'rear': 6,
                    },
                    'highlight': [5],
                    'caption': 'Final state (e_{i} = i-th enqueued element)',
                },
            ],
            'verify': '''
front = rear = 5; size = 0; last = None
for op in ["E"]*6 + ["D"]*4 + ["E"]*3:
    if op == "E":
        assert size < 7; last = rear; rear = (rear + 1) % 8; size += 1
    else:
        front = (front + 1) % 8; size -= 1
assert last == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search trees — insertion',
            'text': 'The keys 50, 27, 73, 14, 39, 61, 88, 33, 45, 30 are inserted in that order into an initially empty binary search tree. The sequence of keys on the path from the root to the node containing 30 is',
            'options': ['50, 27, 33, 30', '50, 27, 14, 30', '50, 27, 39, 30', '50, 27, 39, 33, 30'],
            'answer': 'D',
            'solution': '''**Concept.** Each key is inserted as a leaf by walking down from the root: go left if smaller, right if larger.

Insertions:
- 50 root; 27 → L of 50; 73 → R of 50.
- 14 → L of 27; 39 → R of 27; 61 → L of 73; 88 → R of 73.
- 33: 50 → L, 27 → R, 39 → L ⇒ left child of 39.
- 45: 50 → L, 27 → R, 39 → R ⇒ right child of 39.
- 30: 50 → L (30 < 50), 27 → R (30 > 27), 39 → L (30 < 39), 33 → L (30 < 33) ⇒ left child of 33.

Path: 50, 27, 39, 33, 30 → (D).

- (B) goes left at 27; but 30 > 27.
- (C) skips 33, which was inserted before 30 and is on the way.
- (A) skips 39.

**Tip:** the depth of 30 is 4 — later keys always hang below earlier keys on their path.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            27,
                            [14],
                            [
                                39,
                                [
                                    33,
                                    [30],
                                    None,
                                ],
                                [45],
                            ],
                        ],
                        [
                            73,
                            [61],
                            [88],
                        ],
                    ],
                    'highlight': [50, 27, 39, 33, 30],
                    'caption': 'Final BST, path to 30 highlighted',
                },
            ],
            'verify': '''
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
assert path == [50, 27, 39, 33, 30] and ANSWER == "D"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — linear probing',
            'text': 'The keys 33, 46, 18, 57, 24, 13, 70, 35 are inserted in that order into an initially empty hash table with 11 slots (0–10) using h(k) = k mod 11 and linear probing (next slot = (i + 1) mod 11). A *probe* is one inspection of a slot, including the slot where the key is finally placed. The total number of probes over all eight insertions is ______.',
            'answer': '22',
            'solution': '''**Concept.** Linear probing scans consecutive slots from the home slot until an empty one is found. Runs of occupied slots (clusters) grow and lengthen later probe sequences — primary clustering.

Trace (home slot → final slot, probes):
- 33 → 0 → 0 (1)
- 46 → 2 → 2 (1)
- 18 → 7 → 7 (1)
- 57 → 2 → 3 (2)
- 24 → 2 → 4 (3)
- 13 → 2 → 5 (4)
- 70 → 4 → 6 (3: slots 4, 5, 6)
- 35 → 2 → 8 (7: slots 2, 3, 4, 5, 6, 7, 8)

Total = 1 + 1 + 1 + 2 + 3 + 4 + 3 + 7 = **22**.

**Trap:** 70 hashes to 4, which is *not* its own collision chain, yet it collides because the cluster started at slot 2 has grown over slot 4.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 33,
                        2: 46,
                        3: 57,
                        4: 24,
                        5: 13,
                        6: 70,
                        7: 18,
                        8: 35,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None]*11; tot = 0
for k in [33, 46, 18, 57, 24, 13, 70, 35]:
    i = k % 11; tot += 1
    while T[i] is not None: i = (i + 1) % 11; tot += 1
    T[i] = k
assert tot == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Selection sort — intermediate state',
            'text': 'Selection sort (ascending) is applied to [29, 10, 14, 37, 13, 5, 41]. In pass i (i = 0, 1, 2, …) the minimum of A[i..n−1] is found and swapped with A[i] (a swap with itself changes nothing). What is the array after **three** passes?',
            'options': [
                '[5, 10, 13, 37, 14, 29, 41]',
                '[5, 10, 13, 14, 29, 37, 41]',
                '[5, 10, 14, 37, 13, 29, 41]',
                '[5, 10, 13, 29, 14, 37, 41]',
            ],
            'answer': 'A',
            'solution': '''**Concept.** After k passes of selection sort, A[0..k−1] holds the k smallest elements in order; the remainder is permuted only by the swaps performed.

- Pass 0: min of whole array = 5 (index 5); swap with 29 → [5, 10, 14, 37, 13, 29, 41].
- Pass 1: min of A[1..] = 10 at index 1 → self-swap, unchanged.
- Pass 2: min of A[2..] = 13 (index 4); swap with 14 → [5, 10, 13, 37, 14, 29, 41].

Answer (A).

- (B) is the fully sorted array.
- (C) is the state after only two passes.
- (D) assumes the unsorted tail is also re-ordered, which selection sort never does.

**Trap:** 14 moves *to the right* (to index 4) in pass 2 — selection sort is not stable and can carry elements far from their final place.''',
            'verify': '''
A = [29, 10, 14, 37, 13, 5, 41]
for i in range(3):
    m = min(range(i, len(A)), key=lambda j: A[j])
    A[i], A[m] = A[m], A[i]
assert A == [5, 10, 13, 37, 14, 29, 41] and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Graphs — counting walks with the adjacency matrix',
            'text': 'The adjacency matrix M of a directed graph on vertices 1, 2, 3, 4 is shown (M[i][j] = 1 iff there is an edge i → j). The number of directed walks of length exactly 3 (three edges, vertices may repeat) from vertex 4 to vertex 1 is ______.',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'M',
                    'row_labels': ['1', '2', '3', '4'],
                    'col_labels': ['1', '2', '3', '4'],
                    'rows': [
                        [0, 1, 1, 0],
                        [0, 0, 1, 1],
                        [1, 0, 0, 1],
                        [1, 1, 0, 0],
                    ],
                },
            ],
            'answer': '3',
            'solution': '''**Concept.** (M^{k})[i][j] counts walks of length k from i to j, because each matrix product sums over the possible intermediate vertex.

Edges: 1→2, 1→3, 2→3, 2→4, 3→1, 3→4, 4→1, 4→2.

Enumerate 4 → x → y → 1 directly. Vertices with an edge into 1 are 3 and 4, so y ∈ {3, 4}:
- 4 → 1 → 3 → 1 ✓ (4→1, 1→3, 3→1)
- 4 → 2 → 3 → 1 ✓
- 4 → 2 → 4 → 1 ✓
- 4 → 1 → 4? no edge 1→4; 4 → 4? no self-loop.

Total **3** walks, which equals (M³)[4][1].

**Trap:** walks may revisit vertices (4 → 2 → 4 → 1 is allowed). Counting only simple paths would give only 1 (4 → 2 → 3 → 1).''',
            'verify': '''
M = [[0,1,1,0],[0,0,1,1],[1,0,0,1],[1,1,0,0]]
def mul(A, B): return [[sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
M3 = mul(mul(M, M), M)
assert M3[3][0] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Merge sort — comparisons in a merge',
            'text': 'The standard merge procedure combines the sorted lists L = [4, 11, 15, 32, 38] and R = [6, 9, 12, 13]. It compares the front elements, outputs the smaller, and when one list is exhausted copies the rest of the other **without comparisons**. The number of key comparisons made is',
            'options': ['8', '7', '9', '6'],
            'answer': 'D',
            'solution': '''**Concept.** Each comparison outputs exactly one element; comparisons stop as soon as one list empties. For lists of sizes m and n the count lies between min(m, n) and m + n − 1.

Trace (L front vs R front → output):
- 4 vs 6 → 4
- 11 vs 6 → 6
- 11 vs 9 → 9
- 11 vs 12 → 11
- 15 vs 12 → 12
- 15 vs 13 → 13 — R is now empty.
- Copy 15, 32, 38 with no comparisons.

Total = **6** → (D).

- (B) 7 counts one extra comparison after R empties.
- (C) 9 = m + n − 1 is the worst case (lists interleave until the very end).

**Tip:** the number of comparisons = (m + n) − (number of elements copied after exhaustion) = 9 − 3 = 6.''',
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

L, R = [4, 11, 15, 32, 38], [6, 9, 12, 13]; i = j = c = 0
while i < len(L) and j < len(R):
    c += 1
    if L[i] <= R[j]: i += 1
    else: j += 1
assert c == 6 and ANSWER == "C"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra on an undirected graph',
            'text': "Dijkstra's algorithm is run from S on the weighted undirected graph shown. The shortest-path distance from S to T is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'edges': [
                        ['S', 'A', 3],
                        ['S', 'B', 8],
                        ['A', 'B', 4],
                        ['A', 'C', 9],
                        ['B', 'C', 2],
                        ['B', 'D', 6],
                        ['C', 'D', 3],
                        ['C', 'E', 7],
                        ['D', 'E', 1],
                        ['D', 'T', 8],
                        ['E', 'T', 3],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.6, 2.4],
                        'B': [1.6, -0.4],
                        'C': [3.2, 1],
                        'D': [4.8, -0.4],
                        'E': [4.8, 2.4],
                        'T': [6.4, 1],
                    },
                },
            ],
            'answer': '16',
            'solution': '''**Concept.** With non-negative weights, the vertex extracted with the minimum tentative distance is final; relax every edge out of it.

Trace:
- Extract S (0): A = 3, B = 8.
- Extract A (3): B = min(8, 3 + 4) = 7, C = 3 + 9 = 12.
- Extract B (7): C = min(12, 7 + 2) = 9, D = 7 + 6 = 13.
- Extract C (9): D = min(13, 9 + 3) = 12, E = 9 + 7 = 16.
- Extract D (12): E = min(16, 12 + 1) = 13, T = 12 + 8 = 20.
- Extract E (13): T = min(20, 13 + 3) = 16.
- Extract T (16).

Shortest path: S → A → B → C → D → E → T, cost 3 + 4 + 2 + 3 + 1 + 3 = **16**.

**Trap:** the 'obvious' routes S–B–D–T (8 + 6 + 8 = 22) or S–A–C–E–T (3 + 9 + 7 + 3 = 22) use fewer edges but cost more. The shortest path here uses every intermediate vertex — fewest edges ≠ least weight.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'row_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'rows': [
                        [0, 3, 8, '∞', '∞', '∞', '∞'],
                        [0, 3, 7, 12, '∞', '∞', '∞'],
                        [0, 3, 7, 9, 13, '∞', '∞'],
                        [0, 3, 7, 9, 12, 16, '∞'],
                        [0, 3, 7, 9, 12, 13, 20],
                        [0, 3, 7, 9, 12, 13, 16],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [("S","A",3),("S","B",8),("A","B",4),("A","C",9),("B","C",2),("B","D",6),("C","D",3),
     ("C","E",7),("D","E",1),("D","T",8),("E","T",3)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: 1e9 for v in G}; d["S"] = 0; pq = [(0, "S")]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert d["T"] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra trace and shortest-path tree',
            'text': "Dijkstra's algorithm is run from S on the weighted directed graph shown. An *update* means a tentative distance that is already finite is decreased (the first assignment of a finite value to a vertex is **not** an update). Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 2],
                        ['A', 'C', 6],
                        ['B', 'C', 3],
                        ['B', 'D', 7],
                        ['C', 'D', 1],
                        ['C', 'E', 4],
                        ['D', 'E', 2],
                        ['A', 'D', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.4],
                        'B': [2, -0.4],
                        'C': [4, 2.4],
                        'D': [4, -0.4],
                        'E': [6, 1],
                    },
                },
            ],
            'options': [
                'The vertices are finalised in the order S, A, B, C, D, E',
                'In the shortest-path tree, the parent of D is B',
                'Exactly 4 updates occur during the run',
                'The shortest path from S to E has exactly 5 edges',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** Track tentative distances and predecessors; the predecessor recorded at the last decrease of a vertex is its parent in the shortest-path tree.

Trace (∞ → value is a first assignment; old → new is an update):
- Extract S (0): A ∞→2, B ∞→5.
- Extract A (2): B 5→4 (**update 1**), C ∞→8, D ∞→11.
- Extract B (4): C 8→7 (**update 2**); D: 4 + 7 = 11, not smaller → no change.
- Extract C (7): D 11→8 (**update 3**), E ∞→11.
- Extract D (8): E 11→10 (**update 4**).
- Extract E (10).

Final: A 2, B 4, C 7, D 8, E 10; parents A←S, B←A, C←B, D←C, E←D.

Option analysis:
- (A) **True** — order S, A, B, C, D, E.
- (B) **False** — B offers 11 (not better than A's 11); D's final parent is C.
- (C) **True** — exactly four strict decreases.
- (D) **True** — S→A→B→C→D→E has 5 edges, cost 2 + 2 + 3 + 1 + 2 = 10.

**Trap:** an equal-cost offer (B→D gives 11 = current 11) does not trigger an update with the usual strict `<` test.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 2],
                        ['A', 'C', 6],
                        ['B', 'C', 3],
                        ['B', 'D', 7],
                        ['C', 'D', 1],
                        ['C', 'E', 4],
                        ['D', 'E', 2],
                        ['A', 'D', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.4],
                        'B': [2, -0.4],
                        'C': [4, 2.4],
                        'D': [4, -0.4],
                        'E': [6, 1],
                    },
                    'highlight_edges': [
                        ['S', 'A'],
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['D', 'E'],
                    ],
                    'caption': 'Shortest-path tree (red)',
                },
            ],
            'verify': '''
E = [("S","A",2),("S","B",5),("A","B",2),("A","C",6),("B","C",3),("B","D",7),("C","D",1),
     ("C","E",4),("D","E",2),("A","D",9)]
G = {v: [] for v in "SABCDE"}
for u, v, w in E: G[u].append((v, w))
INF = 10**9; d = {v: INF for v in G}; d["S"] = 0; par = {}; done = []; ups = 0
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: (d[v], v))
    done.append(u)
    for v, w in G[u]:
        if v not in done and d[u] + w < d[v]:
            if d[v] < INF: ups += 1
            d[v] = d[u] + w; par[v] = u
n, edges = "E", 0
while n != "S": n = par[n]; edges += 1
truth = {"A": done == list("SABCDE"), "B": par["D"] == "B", "C": ups == 4, "D": edges == 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — counting shortest paths',
            'text': 'In the weighted directed graph shown, the number of distinct shortest paths (all of minimum total weight) from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 3],
                        ['A', 'C', 3],
                        ['B', 'C', 2],
                        ['A', 'D', 4],
                        ['B', 'D', 3],
                        ['C', 'T', 4],
                        ['D', 'T', 3],
                        ['C', 'E', 1],
                        ['E', 'T', 3],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, 2.2],
                        'D': [4, -0.2],
                        'E': [5.2, 1.6],
                        'T': [6.6, 1],
                    },
                },
            ],
            'answer': '6',
            'solution': '''**Concept.** Run Dijkstra while keeping cnt[v] = number of shortest paths to v. When relaxing u→v: if d[u] + w < d[v], set d[v] = d[u] + w and cnt[v] = cnt[u]; if d[u] + w = d[v], add cnt[u] to cnt[v].

Processing in order of distance:
- S: d 0, cnt 1.
- A: d 2, cnt 1 (from S).  B: d 3, cnt 1 (from S).
- C: via A 2 + 3 = 5, via B 3 + 2 = 5 → tie, cnt 1 + 1 = 2.
- D: via A 2 + 4 = 6, via B 3 + 3 = 6 → tie, cnt 2.
- E: via C 5 + 1 = 6, cnt = cnt[C] = 2.
- T: via C 5 + 4 = 9, via D 6 + 3 = 9, via E 6 + 3 = 9 → three-way tie, cnt = 2 + 2 + 2 = **6**.

The six paths of weight 9: S-A-C-T, S-B-C-T, S-A-D-T, S-B-D-T, S-A-C-E-T, S-B-C-E-T.

**Trap:** shortest paths need not have the same number of edges — the two paths through E have 4 edges and are still shortest. Plain BFS-style counting by hops would miss them.''',
            'verify': '''
E = [("S","A",2),("S","B",3),("A","C",3),("B","C",2),("A","D",4),("B","D",3),("C","T",4),
     ("D","T",3),("C","E",1),("E","T",3)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
best, cnt = [None], [0]
def go(u, cost):
    if u == "T":
        if best[0] is None or cost < best[0]: best[0], cnt[0] = cost, 1
        elif cost == best[0]: cnt[0] += 1
        return
    for v, w in G.get(u, []): go(v, cost + w)
go("S", 0)
assert best[0] == 9 and cnt[0] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra with a negative edge',
            'text': 'The standard Dijkstra algorithm (once a vertex is extracted from the priority queue its distance is never changed again) is run from S on the directed graph shown, which has one negative edge. Which pair gives the distances that the algorithm **reports** for B and C?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 3],
                        ['A', 'B', -2],
                        ['B', 'C', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 0],
                    },
                },
            ],
            'options': ['B = 3, C = 4', 'B = 2, C = 4', 'B = 3, C = 5', 'B = 2, C = 5'],
            'answer': 'C',
            'solution': '''**Concept.** Dijkstra's correctness proof assumes that a path cannot get shorter by adding edges. A negative edge breaks this, and a vertex finalised too early is never revisited.

Trace:
- Extract S (0): A = 4, B = 3.
- Extract B (3) — B is now **final**. Relax B→C: C = 5.
- Extract A (4): A→B gives 4 − 2 = 2 < 3, but B is already finalised, so it is not changed (and B→C is never relaxed again).
- Extract C (5).

Reported: B = 3, C = 5 → (C). True values: B = 2 (S→A→B), C = 4 (S→A→B→C).

- (A) mixes the two.
- (B) gives the true distances — what Bellman–Ford would produce.
- (D) is what an implementation would print if it lowered B's label without re-relaxing B's out-edges.

**Trap:** 'Dijkstra just needs no negative *cycles*' is wrong — even one negative edge without a cycle can produce wrong answers.''',
            'verify': '''ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)

G = {"S": [("A",4),("B",3)], "A": [("B",-2)], "B": [("C",2)], "C": []}
d = {v: 10**9 for v in G}; d["S"] = 0; done = set()
while len(done) < 4:
    u = min((v for v in G if v not in done), key=lambda v: d[v]); done.add(u)
    for v, w in G[u]:
        if v not in done and d[u] + w < d[v]: d[v] = d[u] + w
assert (d["B"], d["C"]) == (3, 5) and ANSWER == "D"
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — a buggy BFS (stack instead of queue)',
            'text': 'The function below was meant to compute BFS distances, but it uses a Python list as a stack. It is run on the directed graph shown. What is printed?',
            'code': '''def bfs(adj, s):
    dist = {s: 0}
    frontier = [s]
    while frontier:
        u = frontier.pop()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                frontier.append(v)
    return dist

adj = {'a': ['b', 'c'], 'b': ['e'], 'c': ['d'],
       'd': ['e', 'f'], 'e': ['f'], 'f': []}
d = bfs(adj, 'a')
print([d[k] for k in sorted(d)])''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['a', 'b', 'c', 'd', 'e', 'f'],
                    'edges': [
                        ['a', 'b'],
                        ['a', 'c'],
                        ['b', 'e'],
                        ['c', 'd'],
                        ['d', 'e'],
                        ['d', 'f'],
                        ['e', 'f'],
                    ],
                    'pos': {
                        'a': [0, 1],
                        'b': [2, 2],
                        'c': [1.4, -0.2],
                        'd': [3, -0.2],
                        'e': [4, 2],
                        'f': [5, 0.6],
                    },
                },
            ],
            'options': [
                '`[0, 1, 1, 2, 2, 3]`',
                '`[0, 1, 1, 2, 3, 4]`',
                '`[0, 1, 1, 2, 3, 3]`',
                '`[0, 1, 1, 2, 2, 4]`',
            ],
            'answer': 'C',
            'solution': '''**Concept.** `list.pop()` removes the **last** element, so the frontier behaves as a stack (DFS-like order) while distances are still fixed at first discovery. Then a vertex can be discovered first via a longer route, and its label is never corrected.

Trace (frontier shown left → right, top on the right):
- pop a: b = 1, c = 1 → [b, c]
- pop c: d = 2 → [b, d]
- pop d: e = 3, f = 3 → [b, e, f]
- pop f: no out-edges. pop e: f already seen.
- pop b: e already seen (with the wrong value 3).

Distances a..f: 0, 1, 1, 2, 3, 3 → (C).

- (A) is the correct BFS answer (e = 2 via a→b→e), which a deque with `popleft()` would print.
- (B) assumes f is reached via e (3 + 1), but f is discovered from d first.
- (D) mixes a correct e with a wrong f.

**Trap:** the code looks like BFS but the choice of `pop()` vs `popleft()` decides whether the labels are shortest-path distances.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

from collections import deque
assert OUTPUT.strip() == "[0, 1, 1, 2, 3, 3]"
dist = {'a': 0}; q = deque('a')
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist: dist[v] = dist[u] + 1; q.append(v)
assert [dist[k] for k in sorted(dist)] == [0, 1, 1, 2, 2, 3]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Stacks — permutations obtainable with a stack',
            'text': 'The integers 1, 2, 3, 4, 5 are pushed onto an initially empty stack in this order; pops may be interleaved with the pushes arbitrarily, and each popped value is appended to an output sequence. Which of the following output sequences is/are possible?',
            'options': ['3, 2, 5, 4, 1', '2, 5, 3, 4, 1', '4, 3, 5, 1, 2', '1, 4, 3, 5, 2'],
            'answer': ['A', 'D'],
            'solution': '''**Concept.** Simulate greedily: to output x, push until x is on top (if x has already been pushed it must be on top right now), then pop. A sequence is impossible exactly when it contains a pattern …c…a…b… with a < b < c (the '312' pattern).

- (A) 3, 2, 5, 4, 1: push 1, 2, 3 pop 3; pop 2; push 4, 5 pop 5; pop 4; pop 1. **Possible.**
- (B) 2, 5, 3, 4, 1: push 1, 2 pop 2; push 3, 4, 5 pop 5; top is now 4 but 3 is required → **impossible** (pattern 5, 3, 4).
- (C) 4, 3, 5, 1, 2: after 4, 3, 5 the stack holds [1, 2] with 2 on top, but 1 is required → **impossible** (pattern 4/5, 1, 2).
- (D) 1, 4, 3, 5, 2: push 1 pop 1; push 2, 3, 4 pop 4; pop 3; push 5 pop 5; pop 2. **Possible.**

**Tip:** a quick test — after any element x is output, the not-yet-output elements smaller than x must appear in *decreasing* order.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [1, 2],
                    'label': 'S',
                    'caption': 'Option (C): stack after outputting 4, 3, 5 — 1 is buried',
                },
            ],
            'verify': '''
def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x: st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = {"A": [3,2,5,4,1], "B": [2,5,3,4,1], "C": [4,3,5,1,2], "D": [1,4,3,5,2]}
assert sorted(k for k in opts if ok(opts[k])) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — memoised path counting on a grid',
            'text': 'Consider the following Python program, which counts monotone lattice paths (each step decreases r or c by 1) that avoid blocked cells. The value printed is ______.',
            'code': '''from functools import lru_cache

BLOCK = {(1, 1), (2, 3), (3, 0)}

@lru_cache(maxsize=None)
def ways(r, c):
    if (r, c) in BLOCK or r < 0 or c < 0:
        return 0
    if r == 0 and c == 0:
        return 1
    return ways(r - 1, c) + ways(r, c - 1)

print(ways(3, 4))''',
            'answer': '6',
            'solution': '''**Concept.** ways(r, c) = number of paths from (0, 0) to (r, c) moving only in +r or +c steps, avoiding blocked cells. Each cell's value is the sum of the cell above and the cell to the left; blocked cells contribute 0. Memoisation makes it O(rows × cols).

Fill the table row by row (✕ = blocked):
- r = 0: 1, 1, 1, 1, 1 (only one way along the top row)
- r = 1: 1, ✕, 0 + 1 = 1, 1 + 1 = 2, 2 + 1 = 3
- r = 2: 1, 0 + 1 = 1, 1 + 1 = 2, ✕, 3 + 0 = 3
- r = 3: ✕, 0 + 1 = 1, 2 + 1 = 3, 0 + 3 = 3, 3 + 3 = 6

ways(3, 4) = **6**.

**Trap:** forgetting that a blocked cell must return 0 *before* the base-case check, or treating the blocked (3, 0) as reachable — it kills every path that runs down column 0 to the bottom row. Without blocks the answer would be C(7, 3) = 35.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'ways(r, c)',
                    'row_labels': ['r=0', 'r=1', 'r=2', 'r=3'],
                    'col_labels': ['c=0', 'c=1', 'c=2', 'c=3', 'c=4'],
                    'rows': [
                        [1, 1, 1, 1, 1],
                        [1, '✕', 1, 2, 3],
                        [1, 1, 2, '✕', 3],
                        ['✕', 1, 3, 3, 6],
                    ],
                    'highlight': [
                        [3, 4],
                    ],
                },
            ],
            'verify': '''
B = {(1, 1), (2, 3), (3, 0)}
T = [[0]*5 for _ in range(4)]
for r in range(4):
    for c in range(5):
        if (r, c) in B: continue
        T[r][c] = 1 if r == c == 0 else (T[r-1][c] if r else 0) + (T[r][c-1] if c else 0)
assert T[3][4] == int(ANSWER) == int(OUTPUT)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Elementary sorting — bubble and insertion sort',
            'text': 'Consider the array [6, 1, 8, 3, 7, 2] to be sorted in ascending order. Bubble sort makes left-to-right passes swapping adjacent out-of-order pairs; insertion sort inserts A[1], A[2], … in turn into the sorted prefix. Which of the following statements is/are TRUE?',
            'options': [
                'After the first pass of bubble sort the array is [1, 6, 3, 7, 2, 8]',
                'The first pass of bubble sort performs exactly 5 swaps',
                'After insertion sort has inserted A[1], A[2] and A[3], the array is [1, 3, 6, 8, 7, 2]',
                'The array contains exactly 8 inversions',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** One bubble pass moves the maximum to the end; insertion sort keeps a sorted prefix. Every adjacent swap (in either algorithm) removes exactly one inversion.

Bubble pass 1 on [6, 1, 8, 3, 7, 2]:
- (6, 1) swap → [1, 6, 8, 3, 7, 2]
- (6, 8) ok
- (8, 3) swap → [1, 6, 3, 8, 7, 2]
- (8, 7) swap → [1, 6, 3, 7, 8, 2]
- (8, 2) swap → [1, 6, 3, 7, 2, 8]

Insertion sort: insert 1 → [1, 6, 8, …]; insert 8 → unchanged; insert 3 → [1, 3, 6, 8, 7, 2].

Inversions: 6 > {1, 3, 2} (3), 8 > {3, 7, 2} (3), 3 > 2 (1), 7 > 2 (1) → 8.

- (A) **True.**
- (B) **False** — 4 swaps (the pair 6, 8 is already in order).
- (C) **True.**
- (D) **True** — so bubble sort makes 8 swaps in total and insertion sort 8 shifts.

**Trap:** counting comparisons (5 in a pass) instead of swaps for (B).''',
            'verify': '''
A = [6, 1, 8, 3, 7, 2]; B = A[:]; sw = 0
for j in range(len(B) - 1):
    if B[j] > B[j+1]: B[j], B[j+1] = B[j+1], B[j]; sw += 1
C = A[:]
for i in range(1, 4):
    k, j = C[i], i - 1
    while j >= 0 and C[j] > k: C[j+1] = C[j]; j -= 1
    C[j+1] = k
inv = sum(A[i] > A[j] for i in range(6) for j in range(i+1, 6))
truth = {"A": B == [1,6,3,7,2,8], "B": sw == 5, "C": C == [1,3,6,8,7,2], "D": inv == 8}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The bottom-up build-heap procedure (sift-down at indices ⌊n/2⌋ − 1 down to 0, each time swapping with the **smaller** child while it is smaller) converts the array [9, 4, 7, 1, 8, 2, 6, 3] (0-based) into a min-heap. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [9, 4, 7, 1, 8, 2, 6, 3],
                    'caption': 'Input array viewed as a complete binary tree',
                },
            ],
            'options': [
                'The resulting heap array is [1, 3, 2, 4, 8, 7, 6, 9]',
                'Exactly 6 swaps are performed in total',
                'Key 9 ends up in a leaf',
                'The sift-down started at index 1 performs exactly one swap',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** Build-heap sifts down every internal node from the last one up to the root; total work is O(n) because most nodes are near the bottom.

n = 8, so sift-downs at i = 3, 2, 1, 0:
- i = 3 (key 1): child 3 → 1 < 3, no swap. [9, 4, 7, 1, 8, 2, 6, 3]
- i = 2 (key 7): children 2, 6 → swap with 2. [9, 4, 2, 1, 8, 7, 6, 3] (1 swap)
- i = 1 (key 4): children 1, 8 → swap with 1 → index 3; child 3 < 4 → swap. [9, 1, 2, 3, 8, 7, 6, 4] (2 swaps)
- i = 0 (key 9): children 1, 2 → swap with 1 → index 1; children 3, 8 → swap with 3 → index 3; child 4 → swap → index 7. [1, 3, 2, 4, 8, 7, 6, 9] (3 swaps)

Total swaps = 0 + 1 + 2 + 3 = 6.

- (A) **True.**
- (B) **True.**
- (C) **True** — 9 sinks to index 7, a leaf.
- (D) **False** — the sift-down from index 1 swaps twice (4 ↔ 1, then 4 ↔ 3).

**Trap:** stopping a sift-down after one level; it continues until the key is no larger than both children.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [1, 3, 2, 4, 8, 7, 6, 9],
                    'caption': 'Resulting min-heap',
                },
            ],
            'verify': '''
h = [9, 4, 7, 1, 8, 2, 6, 3]; per = {}
def sd(i):
    c, n = 0, len(h)
    while True:
        l, r, s = 2*i+1, 2*i+2, i
        if l < n and h[l] < h[s]: s = l
        if r < n and h[r] < h[s]: s = r
        if s == i: return c
        h[i], h[s] = h[s], h[i]; c += 1; i = s
for i in range(len(h)//2 - 1, -1, -1): per[i] = sd(i)
truth = {"A": h == [1,3,2,4,8,7,6,9], "B": sum(per.values()) == 6,
         "C": 2*h.index(9) + 1 >= len(h), "D": per[1] == 1}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — repeated move-last-to-front',
            'text': 'Consider the following Python program on the singly linked list shown. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

head = None
for v in [50, 40, 30, 20, 10]:
    head = Node(v, head)

steps = 0
for _ in range(7):
    prev, cur = None, head
    while cur.nxt:
        prev, cur = cur, cur.nxt
        steps += 1
    prev.nxt = None
    cur.nxt = head
    head = cur

out = []
while head:
    out.append(head.v)
    head = head.nxt
print(out, steps)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [10, 20, 30, 40, 50],
                    'caption': 'List built by the first loop',
                },
            ],
            'options': [
                '`[30, 40, 50, 10, 20] 28`',
                '`[40, 50, 10, 20, 30] 28`',
                '`[40, 50, 10, 20, 30] 35`',
                '`[20, 30, 40, 50, 10] 28`',
            ],
            'answer': 'B',
            'solution': '''**Concept.** Each iteration walks to the last node, detaches it and makes it the new head — a right rotation by one position. Seven rotations of a 5-node list equal 7 mod 5 = 2 rotations.

Building: inserting 50, 40, 30, 20, 10 at the head gives 10 → 20 → 30 → 40 → 50.

Rotations:
- 1: 50, 10, 20, 30, 40
- 2: 40, 50, 10, 20, 30
- 3: 30, 40, 50, 10, 20
- 4: 20, 30, 40, 50, 10
- 5: 10, 20, 30, 40, 50 (back to the start)
- 6: 50, 10, 20, 30, 40
- 7: 40, 50, 10, 20, 30

Step count: reaching the last of 5 nodes takes 4 advances each time, so steps = 7 × 4 = 28. Output `[40, 50, 10, 20, 30] 28` → (B).

- (A) is a rotation by 3 (or a left rotation by 2).
- (C) counts 5 advances per rotation (one per node instead of per link).
- (D) is a left rotation by 1.

**Trap:** the list length never changes, so every rotation costs exactly n − 1 = 4 pointer advances: rotating k times this way costs Θ(k·n), whereas finding k mod n first and re-linking once costs Θ(n).''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [40, 50, 10, 20, 30],
                    'caption': 'Final list',
                },
            ],
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[40, 50, 10, 20, 30] 28'",
        },
    ],
}
