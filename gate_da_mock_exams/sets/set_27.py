# Set 27 — Graph Representations
SET = {
    'number': 27,
    'title': 'Graph Representations',
    'difficulty': 'GATE-level',
    'focus': 'adjacency matrix/list, matrix powers & walks, degree sums, storage',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — aliasing when building adjacency lists',
            'text': 'A programmer builds adjacency lists for the path 0–1–2–3 as follows. What is printed?',
            'code': '''n = 4
adj = [[]] * n
for u, v in [(0, 1), (1, 2), (2, 3)]:
    adj[u].append(v)
    adj[v].append(u)
print(len(adj[0]), adj[3][:3])''',
            'options': ['`1 [2]`', '`6 [1, 0, 2]`', '`2 [2, 3]`', '`6 [2, 1, 0]`'],
            'answer': 'B',
            'solution': '''`[[]] * n` creates a list containing **n references to one and the same** empty list. So `adj[0]`, `adj[1]`, `adj[2]`, `adj[3]` are all aliases of a single list object.

Every `append` goes to that shared list, in program order:

- edge (0,1): append 1, append 0 → [1, 0]
- edge (1,2): append 2, append 1 → [1, 0, 2, 1]
- edge (2,3): append 3, append 2 → [1, 0, 2, 1, 3, 2]

`len(adj[0])` = 6 and `adj[3][:3]` = [1, 0, 2]. Output: `6 [1, 0, 2]`.

- (A) is what the *intended* adjacency lists would give (`adj[0] = [1]`, `adj[3] = [2]`).
- (C) mixes up which endpoint is appended.
- (D) reverses the order of appends.

**Fix:** `adj = [[] for _ in range(n)]` evaluates `[]` n times, giving n distinct lists.
**Trap:** `*` on a list copies references, not objects — the same trap as `[[0] * n] * n` for an adjacency *matrix*.''',
            'verify': "assert OUTPUT.strip() == '6 [1, 0, 2]' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Adjacency matrix squared — common neighbours',
            'text': 'Let A be the adjacency matrix of the simple undirected graph G shown (rows and columns in the order A, B, C, D, E, F). The entry of A² in row B, column E is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'E'],
                        ['B', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['B', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [1, 1],
                        'D': [3, 1],
                        'E': [0, 0],
                        'F': [2.5, 0],
                    },
                },
            ],
            'answer': '3',
            'solution': '''(A²)[u][v] = ∑_{w} A[u][w]·A[w][v] counts the walks of length 2 from u to v, i.e. the number of **common neighbours** of u and v (for u ≠ v in a simple graph).

- N(B) = {A, C, D, F}
- N(E) = {A, C, F}
- N(B) ∩ N(E) = {A, C, F}

So (A²)[B][E] = **3**: the walks B–A–E, B–C–E, B–F–E.

Note that B and E are *not* adjacent, yet the entry is non-zero — A² measures 2-step connectivity, not adjacency.

**Tip:** the diagonal entry (A²)[v][v] equals deg(v) — e.g. (A²)[B][B] = 4.
**Trap:** counting the edge B–E itself (it does not exist) or counting D, which is adjacent to B but not to E.''',
            'verify': '''
V = 'ABCDEF'
E = ['AB','AC','AE','BC','BD','CD','CE','DF','EF','BF']
M = [[0]*6 for _ in V]
for e in E: i, j = V.index(e[0]), V.index(e[1]); M[i][j] = M[j][i] = 1
A2 = [[sum(M[i][k]*M[k][j] for k in range(6)) for j in range(6)] for i in range(6)]
assert A2[1][4] == int(ANSWER) and A2[1][1] == 4
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graphical degree sequences',
            'text': 'Which one of the following sequences is the degree sequence of some **simple** undirected graph?',
            'options': ['5, 5, 4, 3, 2, 1', '6, 4, 3, 3, 2, 2', '4, 4, 3, 3, 2, 2', '3, 3, 3, 3, 3, 2'],
            'answer': 'C',
            'solution': '''Necessary conditions: the degree sum is even (handshake lemma) and no degree exceeds n − 1. Havel–Hakimi decides the rest: remove the largest degree d and subtract 1 from the next d largest; repeat. The sequence is graphical iff we reach all zeros.

- (A) Sum 20 (even). 5,5,4,3,2,1 → remove 5: 4,3,2,1,0 → remove 4: 2,1,0,−1 → negative → **not graphical**. (Two vertices of degree 5 among 6 vertices would both be adjacent to everyone, forcing every degree ≥ 2, but one vertex has degree 1.)
- (B) A vertex of degree 6 needs 6 distinct neighbours but only 5 other vertices exist → **not graphical**.
- (C) Sum 18. 4,4,3,3,2,2 → 3,2,2,1,2 → sort 3,2,2,2,1 → 1,1,1,1 → 0,1,1 → 0,0 → **graphical**.
- (D) Sum 17 is odd → **not graphical**.

**Trap:** checking only the parity — (A) has an even sum but still fails.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

def hh(s):
    s = sorted(s, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d): s[i] -= 1
        if min(s) < 0: return False
        s.sort(reverse=True)
    return True
opts = [[5,5,4,3,2,1],[4,4,3,3,2,2],[6,4,3,3,2,2],[3,3,3,3,3,2]]
assert [L for L, s in zip('ABCD', opts) if hh(s)] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Circular queue arithmetic',
            'text': 'A circular queue of capacity 8 is stored in an array Q[0..7] with two variables: `front` (index of the first element) and `count`. Enqueue stores at Q[(front + count) mod 8]; dequeue returns Q[front] and sets front = (front + 1) mod 8. Initially front = 6 and count = 0. The operations are: enqueue 10, 20, 30, 40, 50; dequeue twice; enqueue 60, 70, 80, 90. Which of the following statements is/are TRUE afterwards?',
            'options': [
                'front = 0',
                '90 is stored at Q[6]',
                'One more enqueue would succeed and store its value at Q[7]',
                'The next dequeue returns 40',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Position of an enqueued item = (front + count) mod 8 at the moment of insertion.

- Enqueue 10, 20, 30, 40, 50 → indices 6, 7, 0, 1, 2; count = 5.
- Dequeue twice → returns 10 then 20; front = (6 + 2) mod 8 = 0; count = 3 (30, 40, 50).
- Enqueue 60, 70, 80, 90 → indices (0 + 3) = 3, 4, 5, 6; count = 7.

- (A) **True** — front = 0.
- (B) **True** — 90 is at index 6.
- (C) **True** — count = 7 < 8, the next slot is (0 + 7) mod 8 = 7 (it still holds the stale value 20, which is simply overwritten).
- (D) **False** — Q[front] = Q[0] = 30 is returned next.

**Trap:** with a (front, count) design all 8 slots are usable; the “one slot wasted” rule applies only to the (front, rear) design that distinguishes full from empty by position.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [30, 40, 50, 60, 70, 80, 90, '–'],
                    'pointers': {
                        'front': 0,
                        'next': 7,
                    },
                    'label': 'Q',
                    'caption': 'Array after all operations (index 7 free)',
                },
            ],
            'verify': '''
Q = [None]*8; front, count = 6, 0; out = []
def enq(x):
    global count
    Q[(front + count) % 8] = x; count += 1
def deq():
    global front, count
    x = Q[front]; front = (front + 1) % 8; count -= 1; return x
for x in (10, 20, 30, 40, 50): enq(x)
out += [deq(), deq()]
for x in (60, 70, 80, 90): enq(x)
assert front == 0 and Q[6] == 90 and count == 7 and (front + count) % 8 == 7 and Q[front] == 30
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — quadratic probing',
            'text': 'Keys 25, 36, 47, 14, 58 are inserted in this order into an initially empty hash table of size 11 (indices 0–10) using quadratic probing: the i-th probe (i = 0, 1, 2, …) for key k examines slot (k mod 11 + i²) mod 11. The index of the slot in which 58 is stored is ______.',
            'answer': '8',
            'solution': '''All five keys have the same home slot: 25, 36, 47, 14, 58 all leave remainder 3 mod 11. Quadratic probing visits 3, 3+1, 3+4, 3+9, 3+16, … (mod 11) = 3, 4, 7, 1, 8, …

- 25: slot 3 (i = 0)
- 36: 3 full → slot 4 (i = 1)
- 47: 3, 4 full → slot 7 (i = 2)
- 14: 3, 4, 7 full → (3 + 9) mod 11 = slot 1 (i = 3)
- 58: 3, 4, 7, 1 full → (3 + 16) mod 11 = 19 mod 11 = slot **8** (i = 4)

Answer: **8**.

Keys with the same home slot follow the identical probe sequence — this is *secondary clustering*, which quadratic probing does not remove (double hashing does).

**Trap:** using (h + i) or adding i² to the *previous* probe position instead of to the home slot.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        1: 14,
                        3: 25,
                        4: 36,
                        7: 47,
                        8: 58,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None]*11
for k in [25, 36, 47, 14, 58]:
    for i in range(11):
        s = (k % 11 + i*i) % 11
        if T[s] is None: T[s] = k; break
assert T.index(58) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — lower-bound loop',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def search(a, x):
    lo, hi = 0, len(a) - 1
    steps = 0
    while lo < hi:
        mid = (lo + hi) // 2
        steps += 1
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo, steps

a = [3, 8, 8, 8, 15, 21, 27, 34, 40]
print(search(a, 8), search(a, 30))''',
            'options': ['`(1, 4) (7, 3)`', '`(2, 2) (7, 3)`', '`(1, 3) (6, 3)`', '`(3, 4) (7, 4)`'],
            'answer': 'A',
            'solution': '''This loop keeps the invariant “the answer lies in [lo, hi]” and returns the **first index whose value is ≥ x** (a lower bound). It always halves the range, so it never stops early on a match.

**x = 8** (lo, hi = 0, 8):

- mid 4: 15 ≥ 8 → hi = 4
- mid 2: 8 ≥ 8 → hi = 2
- mid 1: 8 ≥ 8 → hi = 1
- mid 0: 3 < 8 → lo = 1 → stop. Result (1, 4).

**x = 30**:

- mid 4: 15 < 30 → lo = 5
- mid 6: 27 < 30 → lo = 7
- mid 7: 34 ≥ 30 → hi = 7 → stop. Result (7, 3).

Output: `(1, 4) (7, 3)`.

- (B) assumes the search stops at the first mid that matches (index 2).
- (C) miscounts steps and returns the last element < 30.
- (D) returns the *last* occurrence of 8.

**Trap:** with `hi = len(a) − 1` this function can never return len(a); searching for 50 would wrongly return 8 — a classic off-by-one.''',
            'verify': "assert OUTPUT.strip() == '(1, 4) (7, 3)' and search(a, 50)[0] == 8 and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Trees — parent-array representation',
            'text': '''A rooted tree on nodes 0..10 is stored as a parent array (P[i] is the parent of node i, and −1 marks the root):

`P = [-1, 0, 0, 1, 1, 2, 4, 4, 6, 3, 8]`

The height of the tree (number of edges on the longest root-to-leaf path) is ______.''',
            'answer': '5',
            'solution': '''A parent array stores each edge once (child → parent); depth(i) = 1 + depth(P[i]) with depth(root) = 0. Compute depths in index order:

- node 0: root, depth 0
- nodes 1, 2: parent 0 → depth 1
- nodes 3, 4 (parent 1), 5 (parent 2) → depth 2
- nodes 6, 7 (parent 4), 9 (parent 3) → depth 3
- node 8 (parent 6) → depth 4
- node 10 (parent 8) → depth 5

Longest path 0 → 1 → 4 → 6 → 8 → 10 has **5** edges.

**Tip:** computing all depths naively costs O(n · height); memoising depths makes it O(n). **Trap:** counting nodes on the path (6) instead of edges.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '0',
                    'children': {
                        '0': ['1', '2'],
                        '1': ['3', '4'],
                        '2': ['5'],
                        '3': ['9'],
                        '4': ['6', '7'],
                        '6': ['8'],
                        '8': ['10'],
                    },
                    'caption': 'Tree encoded by P',
                },
            ],
            'verify': '''
P = [-1, 0, 0, 1, 1, 2, 4, 4, 6, 3, 8]
def dep(i): return 0 if P[i] < 0 else 1 + dep(P[i])
assert max(dep(i) for i in range(len(P))) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort — shifts',
            'text': 'Insertion sort sorts `[6, 2, 9, 4, 1, 8, 3]` into ascending order. A *shift* is one execution of `A[j + 1] = A[j]` (moving a larger element one place right). The total number of shifts is',
            'options': ['9', '11', '21', '12'],
            'answer': 'D',
            'solution': '''Each shift removes exactly one **inversion** (a pair i < j with A[i] > A[j]), so the number of shifts equals the number of inversions.

Count, for every element, the larger elements to its **left**:

- 6: 0
- 2: 1 (6)
- 9: 0
- 4: 2 (6, 9)
- 1: 4 (6, 2, 9, 4)
- 8: 1 (9)
- 3: 4 (6, 9, 4, 8)

Total = 0 + 1 + 0 + 2 + 4 + 1 + 4 = **12**.

These are exactly the shifts made when inserting each element (e.g. inserting 1 shifts 9, 6, 4, 2).

- (A) 9 and (B) 11 miss some inversions (typically those of 3).
- (C) 21 = n(n − 1)/2 is the worst case (reverse-sorted input).

**Tip:** comparisons = shifts + (number of insertions that stop on a comparison) — always between inversions and inversions + n − 1.''',
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

a = [6, 2, 9, 4, 1, 8, 3]; s = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0 and a[j] > key: a[j+1] = a[j]; j -= 1; s += 1
    a[j+1] = key
assert s == 12 and ['9','11','12','21'][ord(ANSWER) - 65] == '12'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Adjacency matrix identities',
            'text': 'Let A be the adjacency matrix of a simple undirected graph G with m edges and t triangles. Which of the following statements is/are TRUE for every such G?',
            'options': [
                'A is symmetric and every diagonal entry of A is 0',
                'trace(A²) = 2m',
                'trace(A³) = 6t',
                'The sum of all entries of A equals m',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''(A^{k})[i][j] counts walks of length k from i to j.

- (A) **True.** Undirected → A[i][j] = A[j][i]; simple (no self-loops) → zero diagonal.
- (B) **True.** (A²)[i][i] = number of closed walks of length 2 from i = deg(i). Summing: ∑ deg(i) = 2m (handshake lemma).
- (C) **True.** A closed walk of length 3 is a triangle traversed from one of its 3 vertices in one of 2 directions; each triangle is counted 3 × 2 = 6 times.
- (D) **False.** Each edge contributes two 1s (A[u][v] and A[v][u]), so the sum is 2m.

**Trap:** for (C) dividing by 3 only (forgetting direction) or by 2 only. For a *directed* graph the analogues differ: the sum of entries is m and trace(A²) counts 2-cycles.''',
            'verify': '''
import random, itertools
random.seed(3)
for _ in range(30):
    n = 7; A = [[0]*n for _ in range(n)]
    for i, j in itertools.combinations(range(n), 2):
        if random.random() < 0.5: A[i][j] = A[j][i] = 1
    mm = lambda X, Y: [[sum(X[i][k]*Y[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    A2 = mm(A, A); A3 = mm(A2, A)
    m = sum(map(sum, A)) // 2
    t = sum(1 for c in itertools.combinations(range(n), 3)
            if A[c[0]][c[1]] and A[c[1]][c[2]] and A[c[0]][c[2]])
    assert sum(A2[i][i] for i in range(n)) == 2*m and sum(A3[i][i] for i in range(n)) == 6*t
    assert m == 0 or sum(map(sum, A)) != m
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Directed adjacency matrix — in/out degrees',
            'text': 'The adjacency matrix M of a directed graph on vertices 1..6 is shown (M[i][j] = 1 means an edge i → j). The number of vertices whose in-degree is **different** from their out-degree is ______.',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'M (row = from, column = to)',
                    'col_labels': ['1', '2', '3', '4', '5', '6'],
                    'row_labels': ['1', '2', '3', '4', '5', '6'],
                    'rows': [
                        [0, 1, 1, 0, 0, 1],
                        [0, 0, 1, 1, 0, 0],
                        [1, 0, 0, 1, 1, 0],
                        [0, 0, 0, 0, 1, 1],
                        [0, 1, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 0],
                    ],
                },
            ],
            'answer': '3',
            'solution': '''Out-degree of i = sum of **row** i; in-degree of j = sum of **column** j.

- Row sums (out): 3, 2, 3, 2, 2, 1
- Column sums (in): 2, 2, 2, 2, 2, 3

They differ at vertex 1 (3 vs 2), vertex 3 (3 vs 2) and vertex 6 (1 vs 3) → **3** vertices.

Check: both sums total 13 = number of edges — in a directed graph ∑ in = ∑ out = m, so the surpluses (+1, +1) and the deficit (−2) must cancel.

**Trap:** reading rows as in-degrees. With an adjacency *list* representation the out-degree is the list length (O(1) if stored), but every in-degree needs a full Θ(n + m) scan.''',
            'verify': '''
M = [[0,1,1,0,0,1],[0,0,1,1,0,0],[1,0,0,1,1,0],[0,0,0,0,1,1],[0,1,0,0,0,1],[1,0,0,0,0,0]]
out = [sum(r) for r in M]; inn = [sum(M[i][j] for i in range(6)) for j in range(6)]
assert sum(o != i for o, i in zip(out, inn)) == int(ANSWER) and sum(out) == sum(inn) == 13
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Matrix powers — counting walks',
            'text': 'Let A be the adjacency matrix of the directed graph shown (order P, Q, R, S, T). The entry of A³ in row P, column T — the number of directed walks of length exactly 3 from P to T — is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['P', 'Q', 'R', 'S', 'T'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'R'],
                        ['Q', 'S'],
                        ['R', 'S'],
                        ['R', 'T'],
                        ['S', 'T'],
                        ['T', 'P'],
                        ['S', 'Q'],
                        ['T', 'S'],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [2, 2.2],
                        'R': [2, -0.2],
                        'S': [4, 2.2],
                        'T': [4, -0.2],
                    },
                },
            ],
            'answer': '3',
            'solution': '''(A³)[P][T] = ∑_{x,y} A[P][x]·A[x][y]·A[y][T] = number of walks P → x → y → T.

Out-neighbours: P: {Q, R}; Q: {R, S}; R: {S, T}; S: {T, Q}; T: {P, S}. In-neighbours of T: {R, S}.

Enumerate x ∈ out(P), y ∈ out(x) with y → T:

- x = Q: y = R (R→T ✓) → P-Q-R-T; y = S (S→T ✓) → P-Q-S-T.
- x = R: y = S (S→T ✓) → P-R-S-T; y = T (T→T? no self-loop) ✗.

Total = **3** walks.

Equivalently, row P of A² is (P:0, Q:0, R:1, S:2, T:1) and multiplying by column T of A (1 for R and S) gives 1 + 2 = 3.

**Trap:** counting *paths* vs *walks* does not matter here (all three walks have distinct vertices), but in general A^{k} counts walks, which may repeat vertices and edges.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Row P of A, A², A³',
                    'col_labels': ['P', 'Q', 'R', 'S', 'T'],
                    'row_labels': ['A', 'A²', 'A³'],
                    'rows': [
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 2, 1],
                        [1, 2, 0, 2, 3],
                    ],
                    'highlight': [
                        [2, 4],
                    ],
                },
            ],
            'verify': '''
N = 'PQRST'
E = ['PQ','PR','QR','QS','RS','RT','ST','TP','SQ','TS']
A = [[0]*5 for _ in N]
for e in E: A[N.index(e[0])][N.index(e[1])] = 1
mm = lambda X, Y: [[sum(X[i][k]*Y[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
A2 = mm(A, A); A3 = mm(A2, A)
assert A2[0] == [0, 0, 1, 2, 1] and A3[0] == [1, 2, 0, 2, 3]
assert A3[0][4] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Adjacency lists with head insertion + DFS',
            'text': 'Adjacency lists are built by inserting each new neighbour at the **front** of the list, and then a recursive DFS is run from vertex 1. What is printed?',
            'code': '''edges = [(1, 2), (1, 3), (2, 4), (3, 4),
         (1, 5), (4, 6), (5, 6), (2, 5)]
adj = {v: [] for v in range(1, 7)}
for u, v in edges:
    adj[u].insert(0, v)
    adj[v].insert(0, u)

order = []
def dfs(u):
    order.append(u)
    for w in adj[u]:
        if w not in order:
            dfs(w)

dfs(1)
print(order)''',
            'options': [
                '`[1, 2, 4, 3, 6, 5]`',
                '`[1, 5, 2, 4, 6, 3]`',
                '`[1, 5, 6, 4, 3, 2]`',
                '`[1, 3, 4, 6, 5, 2]`',
            ],
            'answer': 'B',
            'solution': '''The DFS order depends on the **representation**: with front insertion each list holds the neighbours in *reverse* order of edge insertion.

Lists: 1: [5, 3, 2]; 2: [5, 4, 1]; 3: [4, 1]; 4: [6, 3, 2]; 5: [2, 6, 1]; 6: [5, 4].

DFS trace:

- visit 1 → first neighbour 5
- visit 5 → first neighbour 2
- visit 2 → 5 seen → 4
- visit 4 → 6
- visit 6 → 5, 4 seen → return to 4 → next 3
- visit 3 → 4, 1 seen → return … all remaining neighbours seen.

Order: `[1, 5, 2, 4, 6, 3]`.

- (A) is the order with *append* (lists in insertion order: 1: [2, 3, 5], …).
- (C) goes 5 → 6 (but 2 precedes 6 in 5's list).
- (D) assumes 1's list starts with 3.

**Note:** `w not in order` is an O(n) list scan, making this DFS O(n·(n + m)); a `set` of visited vertices restores O(n + m).''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        1: [5, 3, 2],
                        2: [5, 4, 1],
                        3: [4, 1],
                        4: [6, 3, 2],
                        5: [2, 6, 1],
                        6: [5, 4],
                    },
                    'caption': 'Adjacency lists (row = vertex; row 0 unused)',
                },
            ],
            'verify': '''
assert OUTPUT.strip() == '[1, 5, 2, 4, 6, 3]' and ANSWER == 'B'
adj2 = {v: [] for v in range(1, 7)}
for u, v in edges: adj2[u].append(v); adj2[v].append(u)
o2 = []
def d2(u):
    o2.append(u)
    for w in adj2[u]:
        if w not in o2: d2(w)
d2(1)
assert o2 == [1, 2, 4, 3, 6, 5]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Matrix vs list — space and time',
            'text': 'A directed graph has n = 2000 vertices and m = 10 000 edges. Representation X is an adjacency matrix with **1 bit** per entry. Representation Y is an array of n list-head pointers (32 bits each) plus one list node per edge (32-bit vertex id + 32-bit next pointer). Which of the following statements is/are TRUE?',
            'options': [
                'Y uses fewer bits than X',
                'Testing whether the edge (u, v) exists takes O(1) time in X but may take Θ(out-deg(u)) time in Y',
                'Computing the in-degrees of all vertices takes Θ(n + m) time in Y',
                'Computing the transpose (reverse) graph takes Θ(n + m) time in X',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Space.** X: n² = 4 000 000 bits. Y: 32n + 64m = 64 000 + 640 000 = 704 000 bits. So Y is about 5.7 times smaller → (A) **True**. (The break-even is 32n + 64m = n², i.e. m ≈ 62 000 edges; denser graphs favour the bit-matrix.)

**Edge test.** X: read one bit M[u][v] → O(1). Y: scan u's list → Θ(out-deg(u)) in the worst case → (B) **True**.

**All in-degrees in Y.** One pass over all n lists and m nodes, incrementing in[v] for each node → Θ(n + m) → (C) **True**.

**Transpose in X.** Every one of the n² entries must be read/written (M^{T}[i][j] = M[j][i]) → Θ(n²), not Θ(n + m) → (D) **False**. (In Y, transposing takes Θ(n + m).)

**Trap:** assuming the matrix is always larger. With 1-bit entries and sparse lists the comparison depends on m relative to n²/64.''',
            'verify': '''
n, m = 2000, 10000
X = n * n; Y = 32 * n + 64 * m
assert Y < X and Y == 704000
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Triangles from the adjacency matrix',
            'text': 'The adjacency matrix of a simple undirected graph H on vertices 1..6 is shown. The value of trace(A³) is ______.',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Adjacency matrix A of H',
                    'col_labels': ['1', '2', '3', '4', '5', '6'],
                    'row_labels': ['1', '2', '3', '4', '5', '6'],
                    'rows': [
                        [0, 1, 1, 1, 0, 0],
                        [1, 0, 1, 0, 1, 0],
                        [1, 1, 0, 1, 1, 1],
                        [1, 0, 1, 0, 0, 1],
                        [0, 1, 1, 0, 0, 1],
                        [0, 0, 1, 1, 1, 0],
                    ],
                },
            ],
            'answer': '30',
            'solution': '''trace(A³) = ∑_{i} (A³)[i][i] counts closed walks of length 3; in a simple graph each one is a triangle, and each triangle is counted 6 times (3 starting vertices × 2 directions). So trace(A³) = 6 × (number of triangles).

Edges read from the upper triangle: 1-2, 1-3, 1-4, 2-3, 2-5, 3-4, 3-5, 3-6, 4-6, 5-6 (10 edges).

Triangles (check every pair of neighbours for adjacency):

- {1, 2, 3}: 1-2, 2-3, 1-3 ✓
- {1, 3, 4}: ✓
- {2, 3, 5}: ✓
- {3, 4, 6}: ✓
- {3, 5, 6}: ✓
- others such as {1, 2, 5} (1-5 missing) or {4, 5, 6} (4-5 missing) fail.

5 triangles → trace(A³) = 6 × 5 = **30**. Note that vertex 3 lies in all five triangles ((A³)[3][3] = 10).

**Trap:** answering 5 (the triangle count) or 15 (dividing by 2 or by 3 only).''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': [1, 2, 3, 4, 5, 6],
                    'edges': [
                        [1, 2],
                        [1, 3],
                        [1, 4],
                        [2, 3],
                        [2, 5],
                        [3, 4],
                        [3, 5],
                        [3, 6],
                        [4, 6],
                        [5, 6],
                    ],
                    'highlight': [3],
                    'pos': {
                        1: [0, 2],
                        2: [1, 3.2],
                        3: [2, 1.6],
                        4: [1, 0],
                        5: [3.4, 3.2],
                        6: [3.4, 0],
                    },
                    'caption': 'H drawn from the matrix',
                },
            ],
            'verify': '''
A = [[0,1,1,1,0,0],[1,0,1,0,1,0],[1,1,0,1,1,1],[1,0,1,0,0,1],[0,1,1,0,0,1],[0,0,1,1,1,0]]
assert all(A[i][j] == A[j][i] for i in range(6) for j in range(6))
mm = lambda X, Y: [[sum(X[i][k]*Y[k][j] for k in range(6)) for j in range(6)] for i in range(6)]
A3 = mm(mm(A, A), A)
assert sum(A3[i][i] for i in range(6)) == int(ANSWER) and A3[2][2] == 10
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Reverse graph with defaultdict',
            'text': 'Consider the following Python program, which builds the reverse of a directed graph. What is printed?',
            'code': '''from collections import defaultdict
G = {'a': ['b', 'c'], 'b': ['c'], 'c': ['a', 'd'], 'd': []}
R = defaultdict(list)
for u in G:
    for v in G[u]:
        R[v].append(u)
print(len(R), R['x'], len(R), R['c'])''',
            'options': [
                "`4 [] 4 ['a', 'b']`",
                'A `KeyError` is raised',
                "`4 [] 5 ['a', 'b']`",
                "`3 [] 4 ['b', 'a']`",
            ],
            'answer': 'C',
            'solution': '''The reverse graph has an edge v → u for every edge u → v. `defaultdict(list)` creates an empty list the **first time a missing key is accessed** — even just for reading.

Building R (in the iteration order of G, which is insertion order):

- u = a: R[b] = [a], R[c] = [a]
- u = b: R[c] = [a, b]
- u = c: R[a] = [c], R[d] = [c]
- u = d: no edges

R has keys b, c, a, d → `len(R)` = 4. (Vertex d appears as a key because it has an incoming edge.)

Arguments are evaluated left to right: `R['x']` inserts key 'x' with value [] and returns [], so the next `len(R)` is **5**. `R['c']` = ['a', 'b'].

Output: `4 [] 5 ['a', 'b']`.

- (A) assumes reading a missing key does not insert it.
- (B) is the behaviour of a plain `dict`.
- (D) forgets that d gets a key, and reverses append order.

**Trap:** probing a defaultdict silently adds vertices — use `'x' in R` or `R.get('x')` to test membership.''',
            'verify': 'ANSWER = {\'B\': \'C\', \'C\': \'B\'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == "4 [] 5 [\'a\', \'b\']" and ANSWER == \'B\'',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra on a weight matrix',
            'text': "A weighted directed graph is given by the weight matrix W shown (W[i][j] is the weight of edge i → j; ∞ means no edge). Dijkstra's algorithm is run from S. The sum of the shortest-path distances from S to all five vertices (including S itself) is ______.",
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'W (row = from, column = to)',
                    'col_labels': ['S', 'A', 'B', 'C', 'D'],
                    'row_labels': ['S', 'A', 'B', 'C', 'D'],
                    'rows': [
                        [0, 4, 1, '∞', '∞'],
                        ['∞', 0, '∞', 3, 8],
                        ['∞', 2, 0, 6, 9],
                        ['∞', '∞', '∞', 0, 2],
                        [1, '∞', '∞', '∞', 0],
                    ],
                },
            ],
            'answer': '18',
            'solution': '''With a matrix, Dijkstra scans a whole row to relax the extracted vertex's edges (Θ(V²) overall with linear-scan extraction).

- Init: S 0, others ∞.
- Extract S (0): A = 4, B = 1.
- Extract B (1): A = min(4, 1 + 2) = 3; C = 1 + 6 = 7; D = 1 + 9 = 10.
- Extract A (3): C = min(7, 3 + 3) = 6; D = min(10, 3 + 8) = 10 (unchanged).
- Extract C (6): D = min(10, 6 + 2) = 8.
- Extract D (8): edge D → S does not improve S.

Distances: S 0, A 3, B 1, C 6, D 8. Sum = 0 + 3 + 1 + 6 + 8 = **18**.

**Trap:** reading the matrix column-wise (treating W[i][j] as j → i) gives a different graph; and the back edge D → S is irrelevant for distances *from* S.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'dist[] after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞'],
                        [0, 4, 1, '∞', '∞'],
                        [0, 3, 1, 7, 10],
                        [0, 3, 1, 6, 10],
                        [0, 3, 1, 6, 8],
                        [0, 3, 1, 6, 8],
                    ],
                },
            ],
            'verify': '''
INF = float('inf')
W = [[0,4,1,INF,INF],[INF,0,INF,3,8],[INF,2,0,6,9],[INF,INF,INF,0,2],[1,INF,INF,INF,0]]
n = 5; d = [INF]*n; d[0] = 0; done = [False]*n
for _ in range(n):
    u = min((i for i in range(n) if not done[i]), key=lambda i: d[i]); done[u] = True
    for v in range(n):
        if W[u][v] != INF and d[u] + W[u][v] < d[v]: d[v] = d[u] + W[u][v]
assert d == [0, 3, 1, 6, 8] and sum(d) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Reachability and walks in a digraph',
            'text': 'Let A be the adjacency matrix of the directed graph shown (vertices 1..5 in order). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': [1, 2, 3, 4, 5],
                    'edges': [
                        [1, 2],
                        [2, 3],
                        [3, 1],
                        [3, 4],
                        [4, 5],
                        [5, 4],
                    ],
                    'pos': {
                        1: [0, 0],
                        2: [1, 1.6],
                        3: [2, 0],
                        4: [3.6, 0],
                        5: [5.2, 0],
                    },
                },
            ],
            'options': [
                'The graph is strongly connected',
                '(A³)[1][1] = 1',
                '(A²)[3][5] = 1',
                'The sum of all entries of A² equals ∑_{v} in-deg(v) · out-deg(v)',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''- (A) **False.** From 4 or 5 the only edges are 4 ↔ 5, so vertices 1, 2, 3 are unreachable from 4. The strongly connected components are {1, 2, 3} and {4, 5}.
- (B) **True.** Closed walks of length 3 from 1: 1 → 2 → 3 → 1 is the only one (1 has the single out-edge to 2, 2 only to 3, and 3 → 1 closes it).
- (C) **True.** Walks of length 2 from 3 to 5 must be 3 → x → 5 with x ∈ out(3) = {1, 4}; only x = 4 has 4 → 5. Exactly one walk.
- (D) **True.** The sum of all entries of A² counts all length-2 walks u → v → w. Grouping by the middle vertex v gives in-deg(v) choices for u and out-deg(v) choices for w. Here: v=1: 1·1, v=2: 1·1, v=3: 1·2, v=4: 2·1, v=5: 1·1 → total 7.

**Trap:** in (A), a graph can contain a cycle through every vertex of one part yet fail to be strongly connected — the edge 3 → 4 has no return path.''',
            'verify': '''
E = [(1,2),(2,3),(3,1),(3,4),(4,5),(5,4)]
A = [[0]*5 for _ in range(5)]
for u, v in E: A[u-1][v-1] = 1
mm = lambda X, Y: [[sum(X[i][k]*Y[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
A2 = mm(A, A); A3 = mm(A2, A)
ind = [sum(A[i][j] for i in range(5)) for j in range(5)]; outd = [sum(r) for r in A]
assert A3[0][0] == 1 and A2[2][4] == 1 and sum(map(sum, A2)) == sum(a*b for a, b in zip(ind, outd)) == 7
R = A; acc = [row[:] for row in A]
for _ in range(5):
    R = mm(R, A); acc = [[acc[i][j] or R[i][j] for j in range(5)] for i in range(5)]
assert acc[3][0] == 0
assert sorted(ANSWER) == ['B', 'C', 'D']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort on equal keys',
            'text': 'Quicksort with Lomuto partitioning (pivot = last element; an element goes to the left part if `a[j] <= pivot`) is run on an array of 8 **identical** keys, as in the program below. The value printed is ______.',
            'code': '''comps = 0
def partition(a, lo, hi):
    global comps
    p, i = a[hi], lo - 1
    for j in range(lo, hi):
        comps += 1
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1

def qsort(a, lo, hi):
    if lo < hi:
        q = partition(a, lo, hi)
        qsort(a, lo, q - 1)
        qsort(a, q + 1, hi)

a = [7] * 8
qsort(a, 0, 7)
print(comps)''',
            'answer': '28',
            'solution': '''With `<=`, every element equals the pivot and goes to the left part, so the pivot ends at the **last** position: the split is (n − 1, 0) — the worst case, exactly as for sorted input.

- Range size 8: 7 comparisons, pivot at index 7 → recurse on size 7 (and an empty right part)
- size 7: 6 comparisons → size 6
- … → size 2: 1 comparison → size 1 (no call work)

Total = 7 + 6 + 5 + 4 + 3 + 2 + 1 = 8·7/2 = **28** comparisons.

In general Lomuto quicksort costs Θ(n²) on all-equal input, with recurrence T(n) = T(n − 1) + (n − 1).

**Trap:** expecting equal keys to be an easy/best case. Hoare partitioning or 3-way (Dutch-flag) partitioning splits equal keys evenly or groups them, restoring O(n log n) or O(n).''',
            'verify': 'assert OUTPUT.strip() == ANSWER == str(8 * 7 // 2)',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BST reconstruction from post-order',
            'text': '''The post-order traversal of a binary search tree with distinct keys is
5, 11, 9, 17, 14, 8, 26, 23, 35, 31, 20.
Its pre-order traversal is''',
            'options': [
                '20, 8, 5, 14, 9, 11, 17, 31, 23, 26, 35',
                '20, 8, 5, 14, 11, 9, 17, 31, 23, 26, 35',
                '20, 8, 5, 9, 11, 14, 17, 31, 26, 23, 35',
                '20, 8, 14, 5, 9, 11, 17, 23, 26, 31, 35',
            ],
            'answer': 'A',
            'solution': '''In post-order the **last** key is the root; the keys smaller than the root form the left subtree's post-order and the larger ones the right subtree's. Recurse.

- Root 20. Left: 5, 11, 9, 17, 14, 8 → root 8. Right: 26, 23, 35, 31 → root 31.
- Under 8: left {5} → 5; right 11, 9, 17, 14 → root 14.
- Under 14: left 11, 9 → root 9 with right child 11; right {17}.
- Under 31: left 26, 23 → root 23 with right child 26; right {35}.

Pre-order (root, left, right): 20, 8, 5, 14, 9, 11, 17, 31, 23, 26, 35.

- (A) Correct.
- (B) Makes 11 the parent of 9 — but 9 comes *after* 11 in post-order, so 9 is the ancestor.
- (C) Lists the left subtree of 8 in sorted (in-order) order, and puts 26 above 23.
- (D) Is not even consistent with the BST: 14 precedes 5 although 5 < 8 < 14.

**Tip:** for a BST, post-order (or pre-order) alone determines the tree, because the in-order is just the sorted keys.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        20,
                        [
                            8,
                            [5],
                            [
                                14,
                                [
                                    9,
                                    None,
                                    [11],
                                ],
                                [17],
                            ],
                        ],
                        [
                            31,
                            [
                                23,
                                None,
                                [26],
                            ],
                            [35],
                        ],
                    ],
                    'caption': 'Reconstructed BST',
                },
            ],
            'verify': '''
def build(post):
    if not post: return None
    r = post[-1]
    return [r, build([x for x in post[:-1] if x < r]), build([x for x in post[:-1] if x > r])]
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
t = build([5, 11, 9, 17, 14, 8, 26, 23, 35, 31, 20])
opts = {'A': [20,8,5,14,9,11,17,31,23,26,35], 'B': [20,8,5,14,11,9,17,31,23,26,35],
        'C': [20,8,5,9,11,14,17,31,26,23,35], 'D': [20,8,14,5,9,11,17,23,26,31,35]}
assert [k for k, v in opts.items() if v == pre(t)] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Reading structure from A²',
            'text': 'G is a simple undirected graph on 7 vertices whose adjacency matrix A satisfies (A²)[i][i] = 2 for every vertex i. Which of the following statements is/are **necessarily** TRUE?',
            'options': [
                'G has exactly 7 edges',
                'G is connected',
                'G contains a cycle of odd length',
                'G is bipartite',
            ],
            'answer': ['A', 'C'],
            'solution': '''(A²)[i][i] = deg(i), so G is **2-regular**. A 2-regular graph is a disjoint union of cycles, each of length ≥ 3, whose lengths add up to 7.

Possible cycle structures: a single C₇, or C₃ ∪ C₄ (lengths ≥ 3 summing to 7).

- (A) **True.** ∑ deg = 7 × 2 = 14 = 2m → m = 7 (also: a cycle on k vertices has k edges).
- (B) **False.** C₃ ∪ C₄ is 2-regular on 7 vertices but disconnected.
- (C) **True.** The cycle lengths sum to 7 (odd), so at least one cycle has odd length (C₇ itself, or the C₃).
- (D) **False.** A graph with an odd cycle is never bipartite — in fact (C) shows G is *never* bipartite.

**Trap:** assuming “2-regular” means “a single cycle”. Only connectivity would force C₇.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                    'edges': [
                        ['a', 'b'],
                        ['b', 'c'],
                        ['c', 'a'],
                        ['d', 'e'],
                        ['e', 'f'],
                        ['f', 'g'],
                        ['g', 'd'],
                    ],
                    'pos': {
                        'a': [0, 0],
                        'b': [1, 1.5],
                        'c': [2, 0],
                        'd': [3.2, 0],
                        'e': [3.2, 1.5],
                        'f': [4.7, 1.5],
                        'g': [4.7, 0],
                    },
                    'caption': 'C₃ ∪ C₄: 2-regular on 7 vertices but disconnected',
                },
            ],
            'verify': '''
def parts(n, mn=3):
    if n == 0: yield []
    for k in range(mn, n + 1):
        for rest in parts(n - k, k): yield [k] + rest
P = list(parts(7))
assert sorted(P) == [[3, 4], [7]]
assert all(sum(p) == 7 for p in P)            # 7 edges in every case
assert any(len(p) > 1 for p in P)              # a disconnected option exists
assert all(any(k % 2 for k in p) for p in P)   # always an odd cycle
assert sorted(ANSWER) == ['A', 'C']
''',
        },
    ],
}
