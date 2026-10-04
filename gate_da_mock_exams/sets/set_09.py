# Set 09 — Linear & Binary Search
SET = {
    'number': 9,
    'title': 'Linear & Binary Search',
    'difficulty': 'Moderate',
    'focus': 'binary search traces, comparisons, boundaries, sentinel search',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing and find/rfind',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "BINARYSEARCH"
t = s[-2:3:-3]
u = s[::4]
print(t, u, s.find("AR"), s.rfind("AR"))''',
            'options': ['`CERA BRA 3 8`', '`CER BRA 3 8`', '`HAS BRA 3 8`', '`CER BYA 3 9`'],
            'answer': 'B',
            'solution': '''Index the string once and everything follows: B0 I1 N2 A3 R4 Y5 S6 E7 A8 R9 C10 H11.

- `s[-2:3:-3]`: start at index −2 = 10 ('C'), step −3, stop *before* index 3. Indices visited: 10, 7, 4 → 'C', 'E', 'R'. The next index would be 1, which is past the stop (3) when moving left, so `t = 'CER'`.
- `s[::4]`: indices 0, 4, 8 → 'B', 'R', 'A' → `'BRA'`.
- `find` is a left-to-right linear search for the substring: first 'AR' starts at 3.
- `rfind` searches from the right: the last 'AR' starts at 8 (A8 R9).

Output: `CER BRA 3 8` → option (B).

- (A) wrongly includes index 3 — the stop index is never included.
- (C) starts at −1 ('H') instead of −2.
- (D) reads index 5 instead of 4 and gives the index of 'R' instead of where 'AR' starts.

**Trap:** with a negative step the slice runs right-to-left and stops *before* the stop index; `find`/`rfind` return the start index of the match.''',
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'CER BRA 3 8' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — comparison count',
            'text': '''The sorted array A[0..14] shown below is searched with the standard iterative binary search: `lo = 0`, `hi = 14`, `mid = (lo + hi) // 2`; if A[mid] equals the key the search stops, if A[mid] < key then `lo = mid + 1`, else `hi = mid − 1`; the loop runs while `lo ≤ hi`. One iteration (a three-way comparison of the key with A[mid]) counts as **one** comparison.

The key 44 is searched first and then the key 5. The total number of comparisons made by the two searches together is ______.''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [3, 8, 11, 15, 19, 24, 27, 31, 36, 40, 44, 52, 57, 63, 70],
                    'label': 'A',
                    'caption': 'Sorted array A (indices 0–14)',
                },
            ],
            'answer': '8',
            'solution': '''Binary search halves the live range [lo, hi] each iteration; we simply trace both searches.

**Key 44**

- lo=0, hi=14 → mid=7, A[7]=31 < 44 → lo=8.
- lo=8, hi=14 → mid=11, A[11]=52 > 44 → hi=10.
- lo=8, hi=10 → mid=9, A[9]=40 < 44 → lo=10.
- lo=10, hi=10 → mid=10, A[10]=44 → found. **4 comparisons.**

**Key 5** (absent)

- mid=7 (31) > 5 → hi=6; mid=3 (15) > 5 → hi=2; mid=1 (8) > 5 → hi=0; mid=0 (3) < 5 → lo=1 > hi → stop. **4 comparisons.**

Total = 4 + 4 = **8**.

With n = 15 = 2⁴ − 1 the decision tree is perfect with 4 levels, so *every* search (successful at the bottom level or unsuccessful) takes at most 4 comparisons.

**Trap:** do not count the final failed `lo ≤ hi` test as a key comparison — it compares indices, not the key.''',
            'verify': '''
A = [3, 8, 11, 15, 19, 24, 27, 31, 36, 40, 44, 52, 57, 63, 70]
def bs(x):
    lo, hi, c = 0, len(A) - 1, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if A[m] == x: return c
        if A[m] < x: lo = m + 1
        else: hi = m - 1
    return c
assert bs(44) + bs(5) == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Linear search — sentinel technique',
            'text': '''An array A[0..n−1] with n = 40 elements is searched for a key that is **not** present.

Version 1 (ordinary): `i = 0; while i < n and A[i] != key: i += 1`
Version 2 (sentinel, A has a spare cell A[n]): `A[n] = key; i = 0; while A[i] != key: i += 1`, followed by one final test `i < n` to decide the result.

Count every evaluation of `i < n` and every evaluation of `A[i] != key` as one comparison. (Version 1 uses short-circuit `and`.) The number of comparisons made by Version 1 minus the number made by Version 2 is ______.''',
            'answer': '39',
            'solution': '''A sentinel guarantees that the scan stops, so the bound test `i < n` can be removed from the inner loop — it is done once at the end.

**Version 1** (key absent):

- For i = 0 … 39 the test `i < n` is true and `A[i] != key` is evaluated: 40 + 40 = 80.
- At i = 40, `i < n` is false; short-circuit skips `A[40] != key`: +1.
- Total = 2n + 1 = **81**.

**Version 2**:

- `A[i] != key` is true for i = 0 … 39 (40 evaluations) and false at i = 40 (the sentinel): 41 evaluations.
- One final `i < n` (40 < 40 is false → not found): +1.
- Total = n + 2 = **42**.

Difference = 81 − 42 = **39** (in general n − 1).

**Trap:** forgetting that the sentinel cell itself is compared (n + 1 element tests), or forgetting the single bound test after the loop. Asymptotically both are Θ(n); the sentinel only halves the constant.''',
            'verify': '''
n = 40
A = list(range(100, 100 + n)); key = 7
c1 = 0; i = 0
while True:
    c1 += 1
    if not (i < n): break
    c1 += 1
    if not (A[i] != key): break
    i += 1
B = A + [key]; c2 = 0; i = 0
while True:
    c2 += 1
    if not (B[i] != key): break
    i += 1
c2 += 1
assert (c1, c2) == (81, 42) and c1 - c2 == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — permutations',
            'text': 'The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack **in this order**; pops may be interleaved with pushes arbitrarily and every popped value is printed. Which of the following output sequences is/are possible?',
            'options': ['4 5 3 6 1 2', '1 5 4 6 2 3', '3 2 5 6 4 1', '2 4 3 6 5 1'],
            'answer': ['C', 'D'],
            'solution': '''Greedy check: to output x, push everything up to x if x has not been pushed yet; if x was already pushed it must be on the **top** of the stack, otherwise the sequence is impossible.

- (A) push 1–4 pop **4**; push 5 pop **5**; pop **3**; push 6 pop **6**; now stack (bottom→top) is 1, 2 — the next output 1 is *under* 2. **Impossible.**
- (B) push 1 pop **1**; push 2–5 pop **5**, pop **4**; push 6 pop **6**; stack is 2, 3 — next output 2 is under 3. **Impossible.**
- (C) push 1,2,3 pop **3**; pop **2**; push 4,5 pop **5**; push 6 pop **6**; pop **4**; pop **1**. Possible.
- (D) push 1,2 pop **2**; push 3,4 pop **4**; pop **3**; push 5,6 pop **6**; pop **5**; pop **1**. Possible.

Answer: (C) and (D).

**Tip:** a sequence is a stack permutation iff it contains no pattern i < j < k output in the order k, i, j. In (A), 3 … 1 … 2 is exactly such a forbidden 3-1-2 pattern.''',
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x:
            st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = {'A':[3,2,5,6,4,1],'B':[4,5,3,6,1,2],'C':[2,4,3,6,5,1],'D':[1,5,4,6,2,3]}
assert sorted(k for k, v in opts.items() if ok(v)) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues — circular array',
            'text': '''A circular queue is stored in an array Q[0..7] (size 8). `front` is the index of the first element and `rear` is the index where the **next** element will be written; the queue is empty when `front == rear` and full when `(rear + 1) % 8 == front` (one cell is always left unused). Initially `front = rear = 5`.

The operations performed are: 6 enqueues, then 4 dequeues, then 5 enqueues. None of them fails. Which of the following describes the final state?''',
            'options': [
                'front = 1, rear = 7, and the queue is full',
                'front = 1, rear = 0, and the queue holds 6 elements',
                'front = 4, rear = 0, and the queue is full',
                'front = 1, rear = 0, and the queue is full',
            ],
            'answer': 'D',
            'solution': '''Each enqueue does `rear = (rear + 1) % 8`; each dequeue does `front = (front + 1) % 8`.

- 6 enqueues: rear = (5 + 6) % 8 = 3; size 6 (≤ 7, OK).
- 4 dequeues: front = (5 + 4) % 8 = 1; size 2.
- 5 enqueues: rear = (3 + 5) % 8 = 0; size 7.

Size = (rear − front + 8) % 8 = (0 − 1 + 8) % 8 = 7 = capacity 8 − 1, and indeed (rear + 1) % 8 = 1 = front, so the queue is **full**. Answer (D).

- (A) computes rear without the wrap-around ((3 + 5) = 8 → 0, not 7).
- (B) uses the correct indices but miscounts the size (7, not 6).
- (C) forgets to apply the 4 dequeues to `front` correctly (5 + 4 = 9 → 1, not 4).

**Trap:** with the “one empty cell” convention a size-8 array holds at most 7 items — a sixth enqueue in the last phase would have failed.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

N = 8; f = r = 5; size = 0
for _ in range(6): assert (r + 1) % N != f; r = (r + 1) % N; size += 1
for _ in range(4): f = (f + 1) % N; size -= 1
for _ in range(5): assert (r + 1) % N != f; r = (r + 1) % N; size += 1
assert (f, r, size) == (1, 0, 7) and (r + 1) % N == f and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'BST — unsuccessful search path',
            'text': 'The binary search tree below was built by inserting 50, 28, 71, 15, 39, 62, 88, 33, 45, 66, 30, 36 (in that order) into an empty BST. A search for the key **34** is performed. The number of nodes whose key is compared with 34 is ______.',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            28,
                            [15],
                            [
                                39,
                                [
                                    33,
                                    [30],
                                    [36],
                                ],
                                [45],
                            ],
                        ],
                        [
                            71,
                            [
                                62,
                                None,
                                [66],
                            ],
                            [88],
                        ],
                    ],
                    'caption': 'BST built from the given insertion order',
                },
            ],
            'answer': '5',
            'solution': '''A BST search follows a single root-to-leaf path: go left if key < node, right if key > node, and stop at a match or at an empty child.

- 34 vs **50** → smaller → left.
- 34 vs **28** → larger → right.
- 34 vs **39** → smaller → left.
- 34 vs **33** → larger → right.
- 34 vs **36** → smaller → left child of 36 is empty → unsuccessful.

Nodes compared: 50, 28, 39, 33, 36 → **5**.

Note that 34 would be inserted as the left child of 36 — an unsuccessful search always ends exactly where an insertion of that key would occur.

**Trap:** counting the empty child as a comparison (giving 6), or stopping at 33 because 33 < 34 < 36 'looks like' it should be between them.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            28,
                            [15],
                            [
                                39,
                                [
                                    33,
                                    [30],
                                    [36],
                                ],
                                [45],
                            ],
                        ],
                        [
                            71,
                            [
                                62,
                                None,
                                [66],
                            ],
                            [88],
                        ],
                    ],
                    'highlight': [50, 28, 39, 33, 36],
                    'caption': 'Search path for 34 (highlighted)',
                },
            ],
            'verify': '''
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in [50, 28, 71, 15, 39, 62, 88, 33, 45, 66, 30, 36]: T = ins(T, k)
c = 0; t = T
while t is not None:
    c += 1
    if 34 == t[0]: break
    t = t[1] if 34 < t[0] else t[2]
assert c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'The keys 15, 22, 8, 30, 44, 17, 50, 13, 37 are inserted in this order into a hash table with 7 slots using h(k) = k mod 7 and separate chaining (each new key is inserted at the **head** of its chain). Each of the 9 keys is equally likely to be searched for. The average number of key comparisons in a **successful** search is',
            'options': ['2.00', '1.80', '2.25', '1.50'],
            'answer': 'A',
            'solution': '''In chaining, a successful search for a key at position p of its chain costs p comparisons.

Hash values: 15→1, 22→1, 8→1, 30→2, 44→2, 17→3, 50→1, 13→6, 37→2.

- Slot 1 (head insertion): 50 → 8 → 22 → 15 — costs 1 + 2 + 3 + 4 = 10.
- Slot 2: 37 → 44 → 30 — costs 1 + 2 + 3 = 6.
- Slot 3: 17 — cost 1.  Slot 6: 13 — cost 1.

Total = 10 + 6 + 1 + 1 = 18, average = 18 / 9 = **2.00** → option (A).

- (B) 1.80 divides by 10 instead of 9.
- (C) 2.25 = 18 / 8 divides by 8 — one key forgotten when counting.
- (D) 1.50 is an underestimate, in the spirit of the textbook estimate 1 + α/2 ≈ 1.64 for *uniform* hashing; this data piles 4 keys into slot 1, so the real cost is higher.

**Tip:** head- vs tail-insertion changes *which* key is cheap, but not the multiset of costs {1, 2, …, chain length}, so the average is the same either way.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        1: [50, 8, 22, 15],
                        2: [37, 44, 30],
                        3: [17],
                        6: [13],
                    },
                    'caption': 'Final chained table (head insertion)',
                },
            ],
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

T = {i: [] for i in range(7)}
keys = [15, 22, 8, 30, 44, 17, 50, 13, 37]
for k in keys: T[k % 7].insert(0, k)
tot = sum(T[k % 7].index(k) + 1 for k in keys)
assert abs(tot / len(keys) - 2.0) < 1e-9 and ANSWER == 'B'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort with binary search',
            'text': '*Binary insertion sort* is insertion sort in which the position of A[i] inside the sorted prefix A[0..i−1] is found by binary search, after which the elements to its right in the prefix are shifted one place. For an input of n distinct keys in **strictly decreasing** order, the number of key comparisons and the number of element shifts are, respectively,',
            'options': [
                'Θ(n log n) and Θ(n log n)',
                'Θ(n log n) and Θ(n²)',
                'Θ(n²) and Θ(n²)',
                'Θ(n) and Θ(n²)',
            ],
            'answer': 'B',
            'solution': '''Binary search reduces the *search* for the insertion point, but not the *movement* of data.

- Comparisons: inserting the i-th element needs about ⌈log₂(i + 1)⌉ comparisons, so the total is ∑ log₂ i = log₂(n!) = Θ(n log n). (This holds for any input order.)
- Shifts: in a decreasing array every new element is the smallest so far and must go to index 0, so all i prefix elements shift: 0 + 1 + … + (n − 1) = n(n − 1)/2 = Θ(n²).

Therefore the answer is (B).

- (A) assumes shifts also become logarithmic — impossible in an array, each shift moves one element one slot.
- (C) is plain insertion sort's comparison count.
- (D) Θ(n) comparisons is the *best case* of ordinary insertion sort (sorted input), not binary insertion sort.

**Trap:** binary insertion sort is still Θ(n²) time in the worst case.''',
            'verify': '''
def bins(a):
    a = a[:]; comps = shifts = 0
    for i in range(1, len(a)):
        x = a[i]; lo, hi = 0, i
        while lo < hi:
            m = (lo + hi) // 2; comps += 1
            if a[m] <= x: lo = m + 1
            else: hi = m
        for j in range(i, lo, -1): a[j] = a[j - 1]; shifts += 1
        a[lo] = x
    return comps, shifts
import math
for n in (64, 256):
    c, s = bins(list(range(n, 0, -1)))
    assert s == n * (n - 1) // 2 and c <= n * math.ceil(math.log2(n))
assert ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph traversal — BFS levels',
            'text': 'Breadth-first search is run on the undirected graph below starting at **A**; whenever a vertex is processed its unvisited neighbours are enqueued in **alphabetical order**. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['E', 'G'],
                        ['F', 'H'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 2],
                        'G': [4.5, 0],
                        'H': [6, 1],
                    },
                },
            ],
            'options': [
                'Every non-tree edge joins two vertices whose BFS levels differ by at most 1',
                'The BFS visiting order is A, B, C, D, E, F, G, H',
                'Exactly three vertices are at BFS distance 2 from A',
                'Edge E–F is not an edge of the BFS tree',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''BFS processes vertices level by level using a FIFO queue.

- Dequeue A: enqueue B, C (level 1).
- Dequeue B: enqueue D (level 2, parent B).
- Dequeue C: D already seen; enqueue E (level 2, parent C).
- Dequeue D: enqueue F (level 3, parent D).
- Dequeue E: F seen; enqueue G (level 3, parent E).
- Dequeue F: enqueue H (level 4, parent F). Then G, H.

Order A B C D E F G H; levels: A0 | B1 C1 | D2 E2 | F3 G3 | H4.

- (A) **True** — in BFS of an undirected graph a non-tree edge (u, v) always has |level(u) − level(v)| ≤ 1 (here C–D: 1/2, E–F: 2/3, G–H: 3/4).
- (B) **True** — shown above.
- (C) **False** — only D and E are at distance 2.
- (D) **True** — F was discovered from D, so E–F is a non-tree (cross) edge.

**Trap:** assuming F is discovered from E because E–F is drawn horizontally; D is dequeued before E, so D claims F first.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['E', 'G'],
                        ['F', 'H'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 2],
                        'G': [4.5, 0],
                        'H': [6, 1],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'H'],
                    ],
                    'caption': 'BFS tree edges highlighted',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from collections import deque
E = [("A","B"),("A","C"),("B","D"),("C","D"),("C","E"),("D","F"),("E","F"),("E","G"),("F","H"),("G","H")]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
lev = {"A": 0}; par = {}; order = []; q = deque(["A"])
while q:
    u = q.popleft(); order.append(u)
    for v in sorted(G[u]):
        if v not in lev: lev[v] = lev[u] + 1; par[v] = u; q.append(v)
tree = {frozenset((v, p)) for v, p in par.items()}
res = {'A': order == list("ABCDEFGH"),
       'B': sum(1 for v in lev if lev[v] == 2) == 3,
       'C': frozenset(("E","F")) not in tree,
       'D': all(abs(lev[u]-lev[v]) <= 1 for u, v in E if frozenset((u,v)) not in tree)}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — bisect module boundaries',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from bisect import bisect_left, bisect_right
a = [2, 4, 4, 7, 7, 7, 9, 12]
print(bisect_left(a, 7), bisect_right(a, 7),
      bisect_left(a, 8), bisect_right(a, 1))''',
            'options': ['`4 6 7 0`', '`3 5 6 0`', '`3 6 6 0`', '`3 6 7 1`'],
            'answer': 'C',
            'solution': '''`bisect_left(a, x)` returns the first index i with a[i] ≥ x (the *lower bound*); `bisect_right(a, x)` returns the first index i with a[i] > x (the *upper bound*). Both are binary searches returning an insertion point that keeps `a` sorted.

Indices: 2₀ 4₁ 4₂ 7₃ 7₄ 7₅ 9₆ 12₇.

- `bisect_left(a, 7)` → first 7 is at **3**.
- `bisect_right(a, 7)` → one past the last 7 → **6**.
- `bisect_left(a, 8)` → 8 is absent; first element ≥ 8 is 9 at **6**.
- `bisect_right(a, 1)` → every element is > 1 → **0**.

Output `3 6 6 0` → (C). Note bisect_right(a,7) − bisect_left(a,7) = 3 = number of 7s.

- (A) is off by one on the lower bound.
- (B) returns the index of the *last* 7 (5) instead of one past it.
- (D) treats an absent key as if it were inserted after its successor.

**Tip:** for an absent key both functions return the same value.''',
            'verify': "ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.split() == ['3', '6', '6', '0'] and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Binary search — decision-tree depth',
            'text': '''A sorted array of n = 100 distinct keys A[0..99] is searched with the following function. Each execution of the loop body counts as one *iteration*.

Considering only searches for keys that **are present** in the array, the number of keys for which the search needs exactly 7 iterations is ______.''',
            'code': '''def search(A, x):
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
            'answer': '37',
            'solution': '''Binary search on n keys corresponds to a binary **decision tree**: the root is the first mid (index 49), its children are the mids of the two halves, and so on. A key at depth d (root depth 0) is found after exactly d + 1 iterations.

Because `mid` always splits the range [lo, hi] as evenly as possible (the two halves differ in size by at most 1), the decision tree is a *minimum-height* tree: every level except the last is completely full.

- Levels 0–5 are full: 1 + 2 + 4 + 8 + 16 + 32 = 63 keys (found in 1 … 6 iterations).
- The tree has height ⌊log₂ 100⌋ = 6, so the remaining 100 − 63 = **37** keys sit on level 6 and need 7 iterations.

Iteration distribution: 1 key needs 1, 2 need 2, 4 need 3, 8 need 4, 16 need 5, 32 need 6, 37 need 7 (total 100).

Consequently the average successful search costs (1·1 + 2·2 + 4·3 + 8·4 + 16·5 + 32·6 + 37·7)/100 = 580/100 = 5.80 iterations — less than one below the worst case, which is typical for binary search.

**Trap:** answering 50 (‘half the keys are leaves’) — that holds only for a perfect tree with n = 2ᵏ − 1. Here the last level is only partially filled.''',
            'verify': '''
B = list(range(100))
def iters(x):
    lo, hi, c = 0, 99, 0
    while lo <= hi:
        c += 1; mid = (lo + hi) // 2
        if B[mid] == x: return c
        if B[mid] < x: lo = mid + 1
        else: hi = mid - 1
cnt = [iters(x) for x in B]
assert cnt.count(7) == int(ANSWER) and sum(cnt) == 580
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary search — lower-bound boundaries',
            'text': 'Consider the following Python function, where `A` is a list sorted in non-decreasing order. Which of the following statements is/are TRUE?',
            'code': '''def find(A, x):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo''',
            'options': [
                '`find([], 5)` raises an `IndexError`',
                'If A is non-empty and x > max(A), `find` returns `len(A) - 1`',
                'If the line `mid = (lo + hi) // 2` is changed to `mid = (lo + hi + 1) // 2`, the call `find([10, 20], 15)` never terminates',
                'If A is non-empty and x ≤ max(A), `find` returns the index of the first element of A that is ≥ x',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Invariant: the answer (first index with A[i] ≥ x, if any) always lies in [lo, hi]. `A[mid] < x` means mid and everything left of it are too small → `lo = mid + 1`; otherwise mid itself may be the answer → `hi = mid` (not mid − 1). The loop stops when lo == hi.

- (A) **False.** lo = 0, hi = −1, the loop condition 0 < −1 is false at once, and the function returns 0 without touching the list.
- (B) **True.** Every comparison says A[mid] < x, so lo keeps moving right until lo = hi = len(A) − 1. (The caller must check A[lo] ≥ x to detect ‘not found’.)
- (C) **True.** With the upper mid: lo=0, hi=1 → mid=1, A[1]=20 ≥ 15 → hi = mid = 1. Nothing changed, so the loop repeats forever. With `hi = mid` the lower mid is *required* so that the range always shrinks.
- (D) **True.** E.g. A = [3, 5, 5, 8], x = 5: (lo,hi,mid) = (0,3,1) A[1]=5 ≥ 5 → hi=1; (0,1,0) A[0]=3 < 5 → lo=1; stop → 1, the first 5.

**Tip:** pair `lo = mid + 1 / hi = mid` with the lower mid, and `lo = mid / hi = mid − 1` with the upper mid; mixing them causes an infinite loop on two-element ranges.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import random
def lb(A, x):
    for i, v in enumerate(A):
        if v >= x: return i
for _ in range(400):
    A = sorted(random.randint(0, 20) for _ in range(random.randint(1, 12)))
    x = random.randint(-2, 24)
    if x <= max(A): assert find(A, x) == lb(A, x)
    else: assert find(A, x) == len(A) - 1
def find_up(A, x, cap=50):
    lo, hi = 0, len(A) - 1
    for _ in range(cap):
        if not lo < hi: return lo
        mid = (lo + hi + 1) // 2
        if A[mid] < x: lo = mid + 1
        else: hi = mid
    return None
assert find_up([10, 20], 15) is None
assert find([], 5) == 0
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Exponential (galloping) search',
            'text': 'The function below performs *exponential search* on the sorted array A[0..19] shown in the figure, for the key **47**. Count one *examination* each time an array element is compared with the key: the test `A[0] == key`, each evaluation of `A[b] < key` in the doubling loop, and **one** per iteration of the binary-search loop (regardless of how many relational operators that iteration evaluates). The total number of examinations is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [2, 5, 9, 12, 16, 21, 23, 28, 31, 35, 38, 42, 44, 47, 53, 58, 60, 66, 71, 75],
                    'label': 'A',
                    'caption': 'Sorted array A[0..19]',
                },
            ],
            'code': '''def exp_search(A, key):
    if A[0] == key:
        return 0
    b = 1
    while b < len(A) and A[b] < key:
        b *= 2
    lo, hi = b // 2, min(b, len(A) - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] == key:
            return mid
        elif A[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1''',
            'answer': '9',
            'solution': '''Exponential search first finds a range [b/2, b] that must contain the key by doubling b, then binary-searches inside it. Cost is O(log i) where i is the key's position — useful for unbounded or very long arrays.

**Phase 0:** `A[0] == 47`? 2 ≠ 47 → 1 examination.

**Phase 1 (doubling):**

- b=1: A[1]=5 < 47 → b=2.
- b=2: A[2]=9 < 47 → b=4.
- b=4: A[4]=16 < 47 → b=8.
- b=8: A[8]=31 < 47 → b=16.
- b=16: A[16]=60 < 47 is false → stop. 5 examinations.

Range: lo = 16 // 2 = 8, hi = min(16, 19) = 16.

**Phase 2 (binary search on A[8..16]):**

- mid=12: A[12]=44 < 47 → lo=13.
- mid=14: A[14]=53 > 47 → hi=13.
- mid=13: A[13]=47 → found. 3 examinations.

Total = 1 + 5 + 3 = **9**.

**Trap:** forgetting the initial `A[0]` test or the final, *failing* doubling test (A[16] < 47), which are both genuine examinations.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [2, 5, 9, 12, 16, 21, 23, 28, 31, 35, 38, 42, 44, 47, 53, 58, 60, 66, 71, 75],
                    'highlight': [0, 1, 2, 4, 8, 16, 12, 14, 13],
                    'pointers': {
                        'lo': 8,
                        'hi': 16,
                    },
                    'caption': 'Examined cells; binary-search range [8, 16]',
                },
            ],
            'verify': '''
A = [2, 5, 9, 12, 16, 21, 23, 28, 31, 35, 38, 42, 44, 47, 53, 58, 60, 66, 71, 75]
key = 47; c = 1
assert A[0] != key
b = 1
while True:
    if not b < len(A): break
    c += 1
    if not A[b] < key: break
    b *= 2
lo, hi = b // 2, min(b, len(A) - 1)
while lo <= hi:
    mid = (lo + hi) // 2; c += 1
    if A[mid] == key: break
    if A[mid] < key: lo = mid + 1
    else: hi = mid - 1
assert exp_search(A, key) == 13 and c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — generator-based search and exhaustion',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''data = [4, 9, 2, 9, 7, 9]
pos = (i for i, v in enumerate(data) if v == 9)
first = next(pos)
rest = list(pos)
again = list(pos)
print(first, rest, again, sum(1 for _ in pos))''',
            'options': ['`1 [3, 5] [3, 5] 2`', '`1 [1, 3, 5] [] 0`', '`1 [3, 5] [] 3`', '`1 [3, 5] [] 0`'],
            'answer': 'D',
            'solution': '''A generator expression is a **one-shot iterator**: it produces values lazily and remembers where it stopped; once exhausted it stays exhausted.

- The generator performs a linear search yielding every index i with data[i] == 9: the indices are 1, 3, 5.
- `next(pos)` runs the search until the first hit → `first = 1`. The generator is now paused just after index 1.
- `list(pos)` resumes and drains the remaining hits → `rest = [3, 5]`. The generator is now exhausted.
- `list(pos)` again → nothing left → `again = []`.
- `sum(1 for _ in pos)` iterates over the exhausted generator → 0.

Output: `1 [3, 5] [] 0` → option (D).

- (A) treats the generator like a list that can be re-iterated.
- (B) assumes `list(pos)` restarts from the beginning after `next`.
- (C) counts the original number of matches, again assuming a restart.

**Trap:** lists, tuples and ranges are re-iterable; generators, `map`, `filter`, `zip` and file objects are not. Store the results in a list if you need two passes.''',
            'verify': "ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '1 [3, 5] [] 0' and ANSWER == 'C'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — counting comparisons',
            'text': '''Top-down merge sort (split a list of length n into the first ⌊n/2⌋ and the remaining elements, sort both recursively, then merge) is applied to

[38, 12, 55, 7, 26, 49, 3, 61].

During a merge, one comparison is made each time the front elements of the two runs are compared; when one run becomes empty the rest of the other is copied without comparisons. The total number of element comparisons performed by the whole sort is ______.''',
            'answer': '17',
            'solution': '''Merging runs of sizes p and q costs between min(p, q) and p + q − 1 comparisons; the exact number is (p + q) − (number of elements left over when one run empties).

**Level 1 (pairs):** [38|12] → 1, [55|7] → 1, [26|49] → 1, [3|61] → 1. Total 4.
Runs: [12, 38], [7, 55], [26, 49], [3, 61].

**Level 2:**

- [12, 38] + [7, 55]: 12 vs 7 → 7; 12 vs 55 → 12; 38 vs 55 → 38; left run empty, copy 55. **3** comparisons → [7, 12, 38, 55].
- [26, 49] + [3, 61]: 26 vs 3 → 3; 26 vs 61 → 26; 49 vs 61 → 49; copy 61. **3** → [3, 26, 49, 61].

**Level 3:** [7, 12, 38, 55] + [3, 26, 49, 61]: 7v3→3, 7v26→7, 12v26→12, 38v26→26, 38v49→38, 55v49→49, 55v61→55, copy 61. **7** comparisons.

Total = 4 + 6 + 7 = **17**.

For n = 8 the possible range is 12 (each merge stops as early as possible) to 17 (n log₂ n − n + 1); this input happens to hit the maximum, because every merge is fully interleaved — only a single element is left over to copy.

**Trap:** counting n − 1 for every merge regardless of data, or adding a comparison for the copied tail.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each merge level',
                    'row_labels': ['input', 'level 1', 'level 2', 'level 3'],
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', 'comps'],
                    'rows': [
                        [38, 12, 55, 7, 26, 49, 3, 61, '—'],
                        [12, 38, 7, 55, 26, 49, 3, 61, 4],
                        [7, 12, 38, 55, 3, 26, 49, 61, 6],
                        [3, 7, 12, 26, 38, 49, 55, 61, 7],
                    ],
                },
            ],
            'verify': '''
def ms(a):
    if len(a) <= 1: return a, 0
    m = len(a) // 2
    L, c1 = ms(a[:m]); R, c2 = ms(a[m:])
    i = j = c = 0; out = []
    while i < len(L) and j < len(R):
        c += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:], c + c1 + c2
assert ms([38, 12, 55, 7, 26, 49, 3, 61])[1] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': '''The Lomuto partition below is applied once to

A = [23, 41, 8, 56, 17, 35, 12, 29]   (lo = 0, hi = 7).

Which of the following statements is/are TRUE? (A call `swap(i, j)` with i == j counts as a swap.)''',
            'code': '''def partition(A, lo, hi):
    pivot = A[hi]
    i = lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]      # swap(i, j)
    A[i + 1], A[hi] = A[hi], A[i + 1]    # swap(i+1, hi)
    return i + 1''',
            'options': [
                'The function returns 4',
                'The right sub-array passed to the next recursive call is [35, 56, 41]',
                'Exactly 4 swaps are performed (including the final one)',
                'After the call, A = [23, 8, 17, 12, 29, 35, 56, 41]',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Lomuto keeps A[lo..i] ≤ pivot and A[i+1..j−1] > pivot; the pivot is A[hi] = 29.

- j=0: 23 ≤ 29 → i=0, swap(0,0) → unchanged. (swap 1)
- j=1: 41 > 29 → skip.
- j=2: 8 ≤ 29 → i=1, swap(1,2) → [23, 8, 41, 56, 17, 35, 12, 29]. (swap 2)
- j=3: 56 → skip.
- j=4: 17 → i=2, swap(2,4) → [23, 8, 17, 56, 41, 35, 12, 29]. (swap 3)
- j=5: 35 → skip.
- j=6: 12 → i=3, swap(3,6) → [23, 8, 17, 12, 41, 35, 56, 29]. (swap 4)
- Final swap(4, 7) → [23, 8, 17, 12, 29, 35, 56, 41]. (swap 5) Return 4.

Verdicts:

- (A) **True** — the pivot lands at index i + 1 = 4 (four keys are ≤ 29 besides it).
- (B) **True** — quicksort next recurses on A[0..3] = [23, 8, 17, 12] and A[5..7] = [35, 56, 41].
- (C) **False** — there are 4 swaps inside the loop (one is the self-swap at j = 0) plus the final one = **5**.
- (D) **True** — exact final array above.

**Trap:** Lomuto does not preserve the relative order of the > pivot elements (41 moved from index 1 to 7) — the algorithm is not stable.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [23, 8, 17, 12, 29, 35, 56, 41],
                    'highlight': [4],
                    'pointers': {
                        'pivot': 4,
                    },
                    'caption': 'Array after partition (pivot 29 in final place)',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A = [23, 41, 8, 56, 17, 35, 12, 29]
sw = [0]
def part(A, lo, hi):
    p = A[hi]; i = lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1; A[i], A[j] = A[j], A[i]; sw[0] += 1
    A[i+1], A[hi] = A[hi], A[i+1]; sw[0] += 1
    return i + 1
B = A[:]; r = part(B, 0, 7)
res = {'A': B == [23, 8, 17, 12, 29, 35, 56, 41], 'B': r == 4,
       'C': sw[0] == 4, 'D': B[r+1:] == [35, 56, 41]}
assert partition(A, 0, 7) == r and A == B
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source **S** on the weighted directed graph below. Let d(v) be the final shortest-path distance of vertex v. The value of d(A) + d(B) + d(C) + d(D) + d(T) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['B', 'A', 3],
                        ['A', 'C', 2],
                        ['A', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'T', 7],
                        ['D', 'T', 3],
                        ['B', 'D', 11],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 2],
                        'D': [4, 0],
                        'T': [6, 1],
                    },
                },
            ],
            'answer': '33',
            'solution': '''Dijkstra repeatedly extracts the unvisited vertex with the smallest tentative distance and relaxes its outgoing edges; with non-negative weights an extracted distance is final.

- Extract S (0): A = 7, B = 2.
- Extract B (2): A = min(7, 2+3) = 5; D = 2+11 = 13.
- Extract A (5): C = 5+2 = 7; D = min(13, 5+6) = 11.
- Extract C (7): D = min(11, 7+1) = 8; T = 7+7 = 14.
- Extract D (8): T = min(14, 8+3) = 11.
- Extract T (11).

Final: d(A)=5, d(B)=2, d(C)=7, d(D)=8, d(T)=11. Sum = 5 + 2 + 7 + 8 + 11 = **33**.

Shortest-path tree: S→B→A→C→D→T is a single chain — every direct ‘shortcut’ edge (S→A, B→D, A→D, C→T) turns out to be longer than the detour.

**Trap:** finalising D at 11 via A→D (or T at 14 via C→T) because those values were seen first. A tentative distance is only final when its vertex is extracted.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, '∞', 13, '∞'],
                        [0, 5, 2, 7, 11, '∞'],
                        [0, 5, 2, 7, 8, 14],
                        [0, 5, 2, 7, 8, 11],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [("S","A",7),("S","B",2),("B","A",3),("A","C",2),("A","D",6),
     ("C","D",1),("C","T",7),("D","T",3),("B","D",11)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
d = {"S": 0}; pq = [(0, "S")]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G.get(u, []):
        if du + w < d.get(v, 1e9): d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d[v] for v in "ABCDT") == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary heaps — repeated delete-min',
            'text': 'The array below represents a binary **min-heap** (index 0 is the root; children of i are 2i+1 and 2i+2). Two `deleteMin` operations are performed. Each `deleteMin` moves the last element to the root and sifts it down, always swapping with the **smaller** child while that child is smaller than it. The resulting array is',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 9, 5, 14, 11, 8, 7, 20, 16, 13],
                    'caption': 'Min-heap [3, 9, 5, 14, 11, 8, 7, 20, 16, 13]',
                },
            ],
            'options': [
                '[7, 9, 8, 14, 11, 16, 13, 20]',
                '[7, 9, 8, 14, 11, 13, 16, 20]',
                '[7, 9, 13, 14, 11, 8, 16, 20]',
                '[7, 8, 9, 14, 11, 16, 13, 20]',
            ],
            'answer': 'A',
            'solution': '''deleteMin removes the root, moves the last leaf to the root and restores the heap order by sift-down (O(log n) swaps).

**First deleteMin** (remove 3; move 13 to the root):

- [13, 9, 5, 14, 11, 8, 7, 20, 16]: children 9, 5 → swap with 5 → index 2.
- Index 2 children are 8 (idx 5) and 7 (idx 6) → swap with 7 → index 6 (leaf).
- Result: [5, 9, 7, 14, 11, 8, 13, 20, 16].

**Second deleteMin** (remove 5; move 16 to the root):

- [16, 9, 7, 14, 11, 8, 13, 20]: children 9, 7 → swap with 7 → index 2.
- Index 2 children are 8 (idx 5) and 13 (idx 6) → swap with 8 → index 5 (leaf).
- Result: **[7, 9, 8, 14, 11, 16, 13, 20]** → option (A).
- (B) puts 13 at index 5 and 16 at index 6 — but 16 sinks into the cell vacated by 8 (index 5), while 13 never moves in the second deletion.
- (C) sifts 16 toward the *larger* child (13) at the second step, leaving 13 above its smaller child 8 — heap order is violated.
- (D) wrongly swaps 8 up to index 1 (8 is not a child of the root).

**Trap:** always compare with **both** children and pick the smaller; choosing the left child by default breaks the heap property.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [7, 9, 8, 14, 11, 16, 13, 20],
                    'highlight': [7, 8, 16],
                    'caption': 'Heap after two deleteMin operations',
                },
            ],
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

def delmin(h):
    h[0] = h[-1]; h.pop(); i = 0; n = len(h)
    while True:
        l, r, s = 2*i + 1, 2*i + 2, i
        if l < n and h[l] < h[s]: s = l
        if r < n and h[r] < h[s]: s = r
        if s == i: break
        h[i], h[s] = h[s], h[i]; i = s
h = [3, 9, 5, 14, 11, 8, 7, 20, 16, 13]
delmin(h); delmin(h)
opts = {'A': [7, 8, 9, 14, 11, 16, 13, 20], 'B': [7, 9, 8, 14, 11, 13, 16, 20],
        'C': [7, 9, 13, 14, 11, 8, 16, 20], 'D': [7, 9, 8, 14, 11, 16, 13, 20]}
assert [k for k in opts if opts[k] == h] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary search — rotated sorted array',
            'text': 'A *rotated sorted list* is a sorted list that has been cut at some point and the two pieces swapped (e.g. [5, 8, 1, 3]). Consider the following function. Which of the following statements is/are TRUE?',
            'code': '''def find_min(A):
    lo, hi = 0, len(A) - 1
    steps = 0
    while lo < hi:
        steps += 1
        mid = (lo + hi) // 2
        if A[mid] > A[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo, steps''',
            'options': [
                'For every rotation of a sorted list of distinct values, the returned index holds the minimum',
                '`find_min([2, 2, 2, 0, 2])` returns the index of the value 0',
                'If `A[mid] > A[hi]` is replaced by `A[mid] >= A[hi]`, the function still returns the index of the minimum for every rotated list of **distinct** values',
                '`find_min([41, 47, 52, 60, 3, 9, 15, 22, 30, 36])` returns `(4, 3)`',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Key idea: compare A[mid] with A[hi]. If A[mid] > A[hi], the ‘drop’ (and hence the minimum) lies strictly right of mid; otherwise A[mid..hi] is sorted and the minimum is at mid or to its left.

- (A) **True.** The invariant ‘minimum ∈ [lo, hi]’ holds after each step and the range strictly shrinks (mid < hi), so it ends on the minimum.
- (B) **False.** (0,4): mid=2, A[2]=2 > A[4]=2? no → hi=2; (0,2): mid=1 → hi=1; (0,1): mid=0 → hi=0. Returns index 0 (value 2). With duplicates, A[mid] == A[hi] gives no information about which side holds the drop.
- (C) **True.** While lo < hi we have mid < hi, so for distinct values A[mid] == A[hi] can never happen; `>=` and `>` behave identically.
- (D) **True.** (lo,hi)=(0,9): mid=4, A[4]=3 > 36? no → hi=4. (0,4): mid=2, 52 > 3 → lo=3. (3,4): mid=3, 60 > 3 → lo=4. Stop: (4, 3).

**Tip:** with duplicates the standard fix is `elif A[mid] == A[hi]: hi -= 1`, which makes the worst case Θ(n).''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

r = {}
r['A'] = find_min([41, 47, 52, 60, 3, 9, 15, 22, 30, 36]) == (4, 3)
def fm2(A):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] >= A[hi]: lo = mid + 1
        else: hi = mid
    return lo
okB = okD = True
for n in range(1, 40):
    for k in range(n):
        A = list(range(n))[k:] + list(range(n))[:k]
        okB &= A[find_min(A)[0]] == 0
        okD &= A[fm2(A)] == 0
r['B'] = okB; r['D'] = okD
r['C'] = [2, 2, 2, 0, 2][find_min([2, 2, 2, 0, 2])[0]] == 0
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — self-organising linear search',
            'text': 'A singly linked list initially holds 5 → 9 → 2 → 7 → 4 (head first). It is searched with the **move-to-front** heuristic: a search scans from the head, comparing the key with each node, and the found node is then unlinked and re-inserted at the head. The keys 7, 4, 7, 7, 2 are searched in this order (all present). What are the total number of key comparisons and the final list?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [5, 9, 2, 7, 4],
                    'head': 'head',
                    'caption': 'Initial list',
                },
            ],
            'options': [
                '20 comparisons; 5 → 9 → 2 → 7 → 4',
                '17 comparisons; 2 → 4 → 7 → 5 → 9',
                '17 comparisons; 2 → 7 → 4 → 5 → 9',
                '16 comparisons; 2 → 7 → 4 → 5 → 9',
            ],
            'answer': 'C',
            'solution': '''Linear search in a list costs (position of the key) comparisons; move-to-front makes recently used keys cheap, which pays off when accesses repeat.

- Search 7: 5, 9, 2, 7 → **4** comparisons; list becomes 7 → 5 → 9 → 2 → 4.
- Search 4: 7, 5, 9, 2, 4 → **5**; list 4 → 7 → 5 → 9 → 2.
- Search 7: 4, 7 → **2**; list 7 → 4 → 5 → 9 → 2.
- Search 7: 7 → **1**; list unchanged.
- Search 2: 7, 4, 5, 9, 2 → **5**; list 2 → 7 → 4 → 5 → 9.

Total = 4 + 5 + 2 + 1 + 5 = **17**; final list 2 → 7 → 4 → 5 → 9 → option (C).

- (A) is what a plain list (no reorganisation) would give: 4 + 5 + 4 + 4 + 3 = 20, list unchanged.
- (B) has the right count but swaps 4 and 7 — after the last access to 7, 7 is ahead of 4.
- (D) under-counts the third search (7 is at position 2 after 4 was moved in front).

**Note:** moving a node to the front of a singly linked list is O(1) once the scan has reached it, because the scan keeps the predecessor pointer.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [2, 7, 4, 5, 9],
                    'head': 'head',
                    'caption': 'Final list after the five searches',
                },
            ],
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

L = [5, 9, 2, 7, 4]; tot = 0
for k in [7, 4, 7, 7, 2]:
    i = L.index(k); tot += i + 1
    L.insert(0, L.pop(i))
assert tot == 17 and L == [2, 7, 4, 5, 9] and ANSWER == 'B'
L2 = [5, 9, 2, 7, 4]
assert sum(L2.index(k) + 1 for k in [7, 4, 7, 7, 2]) == 20
''',
        },
    ],
}
