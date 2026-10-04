# Set 14 — Graph Traversals: BFS & DFS (Moderate)
SET = {
    'number': 14,
    'title': 'Graph Traversals: BFS & DFS',
    'difficulty': 'Moderate',
    'focus': 'BFS/DFS orders, BFS levels, DFS trees, discovery/finish times',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — list aliasing in adjacency lists',
            'text': 'A student builds adjacency lists for a directed graph with 4 vertices as follows. What is printed?',
            'code': '''adj = [[]] * 4
for u, v in [(0, 1), (1, 2), (2, 3)]:
    adj[u].append(v)
print(len(adj[3]), adj[0] is adj[2])''',
            'options': ['`0 False`', '`3 True`', '`1 False`', '`3 False`'],
            'answer': 'B',
            'solution': '''**Concept.** `[[]] * 4` does **not** create four empty lists. It creates one empty list and a new outer list holding four references to that *same* object.

**Trace.**
- `adj[0].append(1)`, `adj[1].append(2)`, `adj[2].append(3)` all append to the single shared list, which becomes [1, 2, 3].
- `adj[3]` is that same list → `len(adj[3])` = 3.
- `adj[0] is adj[2]` compares identities → True.

Output: `3 True`.

**Options.**
- (A) is what the student *intended* (vertex 3 has no out-neighbours, lists distinct).
- (C) imagines each append going to a separate list but somehow reaching index 3.
- (D) gets the length right but forgets that the lists are the same object.

**Fix:** `adj = [[] for _ in range(4)]` evaluates `[]` four times. In a BFS/DFS this bug makes every vertex appear adjacent to every recorded target — a very common silent error.''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "3 True" and ANSWER == 'C'
good = [[] for _ in range(4)]
for u, v in [(0, 1), (1, 2), (2, 3)]:
    good[u].append(v)
assert len(good[3]) == 0
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'DFS — discovery and finishing times',
            'text': 'Depth-first search is run on the directed graph below starting at vertex A. Out-neighbours are explored in **alphabetical** order. A single clock starts at 0 and is incremented just before each discovery and each finish (so A is discovered at time 1). The finishing time of vertex E is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'E'],
                        ['B', 'C'],
                        ['B', 'D'],
                        ['C', 'A'],
                        ['D', 'C'],
                        ['E', 'D'],
                        ['E', 'F'],
                        ['F', 'G'],
                        ['G', 'E'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3.5],
                        'C': [2, 2],
                        'D': [4, 3.5],
                        'E': [2, 0],
                        'F': [4, 0],
                        'G': [3, -1.5],
                    },
                },
            ],
            'answer': '13',
            'solution': '''**Concept.** In DFS a vertex finishes only after every vertex reachable from it through white (undiscovered) vertices has finished, so its interval [d, f] encloses those of its descendants (parenthesis theorem).

**Trace** (d / f):
- A d=1 → B d=2 → C d=3; C→A is grey (back edge); C f=4.
- B → D d=5; D→C is black; D f=6. B f=7.
- A → E d=8; E→D black (cross edge); E → F d=9 → G d=10; G→E grey (back edge); G f=11, F f=12, **E f=13**.
- A f=14.

So f(E) = **13**.

**Trap:** exploring E before B (it is not alphabetical) gives E an earlier interval, and forgetting that every finish also ticks the clock gives values that are too small.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Discovery / finish times',
                    'col_labels': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'row_labels': ['d', 'f'],
                    'rows': [
                        [1, 2, 3, 5, 8, 9, 10],
                        [14, 7, 4, 6, 13, 12, 11],
                    ],
                    'highlight': [
                        [1, 4],
                    ],
                },
            ],
            'verify': '''
G = {'A': 'BE', 'B': 'CD', 'C': 'A', 'D': 'C', 'E': 'DF', 'F': 'G', 'G': 'E'}
d, f, t = {}, {}, [0]
def vis(u):
    t[0] += 1; d[u] = t[0]
    for v in sorted(G[u]):
        if v not in d: vis(v)
    t[0] += 1; f[u] = t[0]
vis('A')
assert f['E'] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BFS — visiting order with tie-breaking',
            'text': 'Breadth-first search is run on the undirected graph below from vertex A. When a vertex is dequeued, its undiscovered neighbours are enqueued in **alphabetical** order. The order in which vertices are dequeued is',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'C'],
                        ['A', 'F'],
                        ['C', 'B'],
                        ['C', 'G'],
                        ['F', 'G'],
                        ['F', 'H'],
                        ['B', 'D'],
                        ['G', 'E'],
                        ['H', 'E'],
                        ['D', 'E'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'C': [2, 3],
                        'F': [2, 1],
                        'B': [4, 4],
                        'G': [4, 2],
                        'H': [4, 0],
                        'D': [6, 4],
                        'E': [6, 1],
                    },
                },
            ],
            'options': [
                'A, C, F, B, G, H, D, E',
                'A, C, F, B, G, D, H, E',
                'A, C, B, G, F, H, D, E',
                'A, C, F, G, B, H, E, D',
            ],
            'answer': 'A',
            'solution': '''**Concept.** BFS dequeues vertices in non-decreasing order of distance from the source, and within a level in the order they were discovered.

**Trace** (queue after each dequeue):
- Dequeue A → enqueue C, F. Queue: C F.
- Dequeue C → neighbours A, B, G; new: B, G. Queue: F B G.
- Dequeue F → neighbours A, G, H; new: H. Queue: B G H.
- Dequeue B → new: D. Queue: G H D.
- Dequeue G → new: E. Queue: H D E.
- Dequeue H, D, E (nothing new).

Order: **A, C, F, B, G, H, D, E**. Levels: 0 {A}, 1 {C, F}, 2 {B, G, H}, 3 {D, E}.

**Options.**
- (B) puts D (level 3) before H (level 2) — impossible in BFS.
- (C) is a depth-first style order (goes from C to its neighbours before F).
- (D) places G before B although both were discovered by C, B first alphabetically; and E before D, though D was enqueued first.

**Tip:** write the queue explicitly; do not try to read levels off the picture alone.''',
            'verify': '''
from collections import deque
E = ["AC", "AF", "CB", "CG", "FG", "FH", "BD", "GE", "HE", "DE"]
G = {}
for a, b in E:
    G.setdefault(a, set()).add(b); G.setdefault(b, set()).add(a)
seen, q, out = {'A'}, deque('A'), []
while q:
    u = q.popleft(); out.append(u)
    for v in sorted(G[u]):
        if v not in seen: seen.add(v); q.append(v)
assert ", ".join(out) == "A, C, F, B, G, H, D, E" and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'BFS/DFS — complexity and edge properties',
            'text': 'Let G be a graph with n vertices and m edges. Which of the following statements is/are TRUE?',
            'options': [
                'BFS on G stored as an adjacency matrix takes Θ(n²) time',
                'DFS on G stored as adjacency lists takes Θ(n + m) time',
                'If G is undirected, every non-tree edge of a BFS tree joins two vertices whose BFS levels differ by at most 1',
                'If G is undirected, a DFS of G can produce cross edges',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''- (A) **True.** For each of the n dequeued vertices BFS scans a whole matrix row of length n to find neighbours → Θ(n²) regardless of m.
- (B) **True.** Each vertex is visited once and each adjacency list is scanned once: Θ(n + ∑ deg) = Θ(n + m).
- (C) **True.** If edge (u, v) had level(v) ≥ level(u) + 2, then when u was dequeued v was still undiscovered and would have been put at level(u) + 1 — contradiction. So every edge, tree or not, spans levels differing by 0 or 1.
- (D) **False.** In an undirected DFS every edge is a tree edge or a back edge. A would-be cross edge (u, v) with v finished before u was discovered is impossible, since v would have explored the edge to the white vertex u before finishing.

**Tip:** property (C) is why BFS gives shortest paths in unweighted graphs; property (D) is why DFS detects cycles in undirected graphs by looking for any non-tree edge to a non-parent.''',
            'verify': '''
import random
from collections import deque
random.seed(7)
okC = okD = True
for _ in range(200):
    n = random.randint(3, 9)
    G = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < 0.35: G[i].add(j); G[j].add(i)
    lv = {0: 0}; q = deque([0])
    while q:
        u = q.popleft()
        for v in G[u]:
            if v not in lv: lv[v] = lv[u] + 1; q.append(v)
    for u in lv:
        for v in G[u]:
            okC &= abs(lv[u] - lv[v]) <= 1
    st, fin, par = {}, set(), {}
    def dfs(u):
        st[u] = 1
        for v in G[u]:
            if v not in st: par[v] = u; dfs(v)
            elif v in fin and par.get(u) != v:
                # neighbour already finished and not parent: check ancestry
                a = v
                while a in par and a != u: a = par[a]
                if a != u:
                    raise AssertionError("cross edge")
        fin.add(u)
    for s in range(n):
        if s not in st: dfs(s)
assert okC and sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Queues — circular array',
            'text': '''A queue is stored in a circular array Q[0..6] of capacity 7 (all 7 slots usable; a separate counter tracks the size). Initially the queue is empty and the rear index r = 0, where r is the slot that the next enqueued element will occupy; after each enqueue, r = (r + 1) mod 7. The following operations are performed:

5 enqueues, 3 dequeues, 4 enqueues, 2 dequeues, 3 enqueues.

The index of the slot that holds the most recently enqueued element is ______.''',
            'answer': '4',
            'solution': '''**Concept.** In a circular buffer only the enqueues move r; dequeues move the front index f. Size must stay ≤ capacity, so first check no overflow occurs.

**Trace** (size, f, r):
- 5 enqueues → slots 0–4 used; size 5, f = 0, r = 5.
- 3 dequeues → size 2, f = 3.
- 4 enqueues → slots 5, 6, 0, 1; size 6, r = 2.
- 2 dequeues → size 4, f = 5.
- 3 enqueues → slots 2, 3, 4; size 7 (full, but no overflow), r = 5.

The last element went into slot **4** (= (total enqueues − 1) mod 7 = 11 mod 7).

**Trap:** answering r = 5 — r points to the *next free* slot, one past the last element. Also, the queue is exactly full at the end; with the 'one slot kept empty' convention the last enqueue would have overflowed.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': ['e8', 'e9', 'e10', 'e11', 'e12', 'e6', 'e7'],
                    'pointers': {
                        'f': 5,
                        'last': 4,
                    },
                    'highlight': [4],
                    'label': 'Q',
                    'caption': 'Final buffer (eK = K-th enqueued element)',
                },
            ],
            'verify': '''
Q, f, r, size, k = [None] * 7, 0, 0, 0, 0
for op, cnt in [('e', 5), ('d', 3), ('e', 4), ('d', 2), ('e', 3)]:
    for _ in range(cnt):
        if op == 'e':
            assert size < 7
            k += 1; Q[r] = k; last = r; r = (r + 1) % 7; size += 1
        else:
            f = (f + 1) % 7; size -= 1
assert last == int(ANSWER) and Q[f] == 6
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — quadratic probing',
            'text': 'Keys 22, 33, 44, 13, 55 are inserted in that order into an initially empty hash table of size 11 (slots 0–10) using h(k) = k mod 11 and quadratic probing: the i-th probe (i = 0, 1, 2, …) examines slot (h(k) + i²) mod 11. In which slot is key 55 stored?',
            'options': ['3', '5', '9', '6'],
            'answer': 'C',
            'solution': '''**Concept.** Quadratic probing jumps by 1, 4, 9, … from the home slot, which avoids the long primary clusters of linear probing (but keys with the same home still follow the same probe sequence — secondary clustering).

**Trace.**
- 22 → 0.
- 33 → 0 (full), 0 + 1 = **1**.
- 44 → 0, 1 full, 0 + 4 = **4**.
- 13 → 13 mod 11 = **2**.
- 55 → 0, 1, 4 all full; 0 + 9 = **9** is free.

**Options.**
- (A) 3 is what *linear* probing would give (0, 1, 2 full → 3).
- (B) 5 adds i instead of i² after the third probe.
- (D) 6 is not on 55's probe sequence 0, 1, 4, 9, 5, 3, …

**Trap:** 22, 33, 44, 55 all hash to 0, so they share one probe sequence — a textbook example of secondary clustering.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 22,
                        1: 33,
                        2: 13,
                        4: 44,
                        9: 55,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 11
for k in [22, 33, 44, 13, 55]:
    i = 0
    while T[(k % 11 + i * i) % 11] is not None: i += 1
    T[(k % 11 + i * i) % 11] = k
assert "ABCD"[["3", "5", "9", "6"].index(str(T.index(55)))] == ANSWER
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Selection sort — swap count',
            'text': 'Selection sort (ascending) is applied to [29, 10, 14, 37, 13, 5, 41]. In pass i (i = 0, 1, …, n − 2) the minimum of A[i..n−1] is found and swapped with A[i] **only if** it is not already at position i. The number of swaps performed is ______.',
            'answer': '4',
            'solution': '''**Concept.** Selection sort always makes n − 1 passes and n(n − 1)/2 comparisons; only the number of actual swaps depends on the data.

**Trace.**
- i = 0: min of whole array is 5 (index 5) → swap → [5, 10, 14, 37, 13, 29, 41]. (1)
- i = 1: min of A[1..] is 10, already at index 1 → no swap.
- i = 2: min 13 at index 4 → swap → [5, 10, 13, 37, 14, 29, 41]. (2)
- i = 3: min 14 at index 4 → swap → [5, 10, 13, 14, 37, 29, 41]. (3)
- i = 4: min 29 at index 5 → swap → [5, 10, 13, 14, 29, 37, 41]. (4)
- i = 5: min 37 already in place → no swap.

Total swaps = **4** (with 21 comparisons).

**Trap:** answering n − 1 = 6, which counts the 'swaps' of an element with itself; the question excludes those.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'row_labels': ['start', 'i=0', 'i=1', 'i=2', 'i=3', 'i=4', 'i=5'],
                    'rows': [
                        [29, 10, 14, 37, 13, 5, 41],
                        [5, 10, 14, 37, 13, 29, 41],
                        [5, 10, 14, 37, 13, 29, 41],
                        [5, 10, 13, 37, 14, 29, 41],
                        [5, 10, 13, 14, 37, 29, 41],
                        [5, 10, 13, 14, 29, 37, 41],
                        [5, 10, 13, 14, 29, 37, 41],
                    ],
                },
            ],
            'verify': '''
A = [29, 10, 14, 37, 13, 5, 41]; sw = 0
for i in range(len(A) - 1):
    m = min(range(i, len(A)), key=lambda k: A[k])
    if m != i: A[i], A[m] = A[m], A[i]; sw += 1
assert A == sorted(A) and sw == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — traversals',
            'text': 'For the binary tree shown below, the **post-order** traversal is',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'K',
                        [
                            'D',
                            [
                                'B',
                                None,
                                ['C'],
                            ],
                            [
                                'H',
                                ['F'],
                                None,
                            ],
                        ],
                        [
                            'P',
                            None,
                            [
                                'S',
                                ['R'],
                                ['U'],
                            ],
                        ],
                    ],
                    'caption': 'Binary tree',
                },
            ],
            'options': [
                'K, D, B, C, H, F, P, S, R, U',
                'B, C, D, F, H, K, P, R, S, U',
                'C, B, F, H, D, P, R, U, S, K',
                'C, B, F, H, D, R, U, S, P, K',
            ],
            'answer': 'D',
            'solution': '''**Concept.** Post-order = left subtree, right subtree, root (applied recursively). It is exactly the order in which a DFS of the tree *finishes* the vertices.

**Trace.**
- Left subtree of K (root D): post(B-subtree) = C, B; post(H-subtree) = F, H; then D → C, B, F, H, D.
- Right subtree of K (root P): P has no left child; post(S-subtree) = R, U, S; then P → R, U, S, P.
- Finally K.

Post-order: **C, B, F, H, D, R, U, S, P, K**.

**Options.**
- (A) is the pre-order traversal.
- (B) is the in-order traversal (sorted, since this happens to be a BST).
- (C) places P before its own descendants R, U, S — P must come after its right subtree.

**Tip:** the last element of post-order is always the root; the first element of pre-order is always the root. That alone eliminates (B) and (A).''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

T = ["K", ["D", ["B", None, ["C", None, None]], ["H", ["F", None, None], None]],
     ["P", None, ["S", ["R", None, None], ["U", None, None]]]]
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
opts = ["C, B, F, H, D, R, U, S, P, K", "B, C, D, F, H, K, P, R, S, U",
        "C, B, F, H, D, P, R, U, S, K", "K, D, B, C, H, F, P, S, R, U"]
assert opts["ABCD".index(ANSWER)] == ", ".join(post(T))
assert opts[1] == ", ".join(ino(T)) and opts[3] == ", ".join(pre(T))
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'DFS — possible visiting orders',
            'text': 'Depth-first search is started at vertex A of the directed graph below; out-neighbours may be explored in **any** order. Which of the following is/are possible orders in which the vertices are discovered?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 2],
                        'E': [4, 0],
                        'F': [6, 1],
                    },
                },
            ],
            'options': ['A, B, D, F, C, E', 'A, C, E, F, D, B', 'A, B, D, F, E, C', 'A, C, D, F, B, E'],
            'answer': ['A', 'B'],
            'solution': '''**Concept.** DFS always continues from the most recently discovered vertex that still has an undiscovered out-neighbour. It may backtrack only when the current vertex is exhausted.

- (A) A → B → D → F; F, D, B exhausted; back at A → C → E (D, F already seen). **Possible.**
- (B) A → C → E → F; F, E exhausted; back at C → D (F seen); back at A → B. **Possible.**
- (C) After A → B → D → F, backtracking reaches A, whose only undiscovered out-neighbour is C. E is reachable only through C, so E cannot appear before C. **Not possible.**
- (D) A → C → D → F; back at D, then C — but C still has the undiscovered neighbour E, so E must be discovered before returning to A for B. **Not possible.**

**Trap:** an order can look plausible because every vertex is adjacent to *some* earlier vertex — that is not enough; it must be adjacent to the deepest unfinished vertex.''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'A': 'BC', 'B': 'D', 'C': 'DE', 'D': 'F', 'E': 'F', 'F': ''}
def ok(s):
    s = s.replace(', ', '')
    if s[0] != 'A': return False
    seen, st = {'A'}, ['A']
    for v in s[1:]:
        while st and all(w in seen for w in G[st[-1]]): st.pop()
        if not st or v not in G[st[-1]] or v in seen: return False
        seen.add(v); st.append(v)
    return len(seen) == 6
opts = ["A, B, D, F, C, E", "A, C, E, F, D, B", "A, C, D, F, B, E", "A, B, D, F, E, C"]
assert [L for L, o in zip("ABCD", opts) if ok(o)] == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph traversal — connected components',
            'text': 'Consider the undirected graph on vertices 0–9 shown below. A program runs `for v in range(10): if not visited[v]: BFS(v)`. What is the minimum number of edges that must be added to make the graph connected? (This equals the number of BFS calls made by the loop, minus one.)',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
                    'edges': [
                        ['0', '3'],
                        ['3', '7'],
                        ['1', '4'],
                        ['2', '5'],
                        ['5', '8'],
                        ['8', '2'],
                        ['6', '9'],
                    ],
                    'pos': {
                        '0': [0, 2],
                        '3': [1, 3],
                        '7': [2, 2],
                        '1': [3.5, 3],
                        '4': [3.5, 1.5],
                        '2': [5, 3],
                        '5': [6.5, 3],
                        '8': [5.75, 1.5],
                        '6': [8, 3],
                        '9': [8, 1.5],
                    },
                },
            ],
            'options': ['2', '5', '4', '3'],
            'answer': 'D',
            'solution': '''**Concept.** Each call of BFS from an unvisited vertex discovers exactly one connected component. A graph with c components needs exactly c − 1 extra edges to become connected (join the components in a chain).

**Trace of the outer loop.**
- v = 0: BFS(0) visits {0, 3, 7}.
- v = 1: BFS(1) visits {1, 4}.
- v = 2: BFS(2) visits {2, 5, 8}.
- v = 3, 4, 5: already visited.
- v = 6: BFS(6) visits {6, 9}.
- v = 7, 8, 9: already visited.

4 BFS calls → c = 4 components → **3** edges needed.

**Options.** (C) 4 is the number of components itself; (A) and (B) miscount the components (e.g. treating the triangle 2–5–8 as two pieces).

**Tip:** the whole loop still costs Θ(n + m) — each vertex and edge is processed once across all BFS calls.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

E = [(0, 3), (3, 7), (1, 4), (2, 5), (5, 8), (8, 2), (6, 9)]
p = list(range(10))
def find(x):
    while p[x] != x: x = p[x]
    return x
for a, b in E: p[find(a)] = find(b)
c = len({find(v) for v in range(10)})
assert ["2", "3", "4", "5"]["ABCD".index(ANSWER)] == str(c - 1)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DFS — edge classification with restarts',
            'text': 'DFS is run on the directed graph below. The outer loop tries start vertices in alphabetical order (A, B, …, H), starting a new DFS tree from each vertex that is still undiscovered, and out-neighbours are always explored in alphabetical order. Every edge is classified as a tree, back, forward or cross edge with respect to the resulting DFS forest. The number of **cross** edges is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'B'],
                        ['C', 'E'],
                        ['D', 'A'],
                        ['E', 'D'],
                        ['F', 'E'],
                        ['F', 'G'],
                        ['G', 'C'],
                        ['H', 'G'],
                        ['H', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3.5],
                        'C': [2, 0.5],
                        'D': [4, 3.5],
                        'E': [4, 0.5],
                        'F': [6, 0.5],
                        'G': [3, -1.5],
                        'H': [6, -1.5],
                    },
                },
            ],
            'answer': '6',
            'solution': '''**Concept.** For edge (u, v) examined from u: v white → tree; v grey (on the recursion stack) → back; v black and d[u] < d[v] → forward; v black and d[v] < d[u] → cross.

**Trace** (d/f with a clock starting at 1):
- Tree 1 from A: A 1 → B 2 → D 3; D→A grey: **back**. D f=4, B f=5.
  A → C 6; C→B black, d[B] = 2 < 6: **cross**; C → E 7; E→D black: **cross**; E f=8, C f=9, A f=10.
- B, C, D, E already black. Tree 2 from F: F 11; F→E black: **cross**; F → G 12; G→C black: **cross**; G f=13, F f=14.
- Tree 3 from H: H 15; H→F black: **cross**; H→G black: **cross**; H f=16.

Classification: tree edges AB, BD, AC, CE, FG (5); back edge DA (1); forward edges none; cross edges CB, ED, FE, GC, HF, HG → **6**.

Check: 5 + 1 + 0 + 6 = 12 = total number of edges.

**Trap:** edges into an *earlier* DFS tree (FE, GC, HF, HG) are always cross edges — they can never be back or forward edges because the target is in a different, already finished tree.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['F', 'G'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3.5],
                        'C': [2, 0.5],
                        'D': [4, 3.5],
                        'E': [4, 0.5],
                        'F': [6, 0.5],
                        'G': [3, -1.5],
                        'H': [6, -1.5],
                    },
                    'caption': 'DFS forest (trees rooted at A, F, H)',
                },
            ],
            'verify': '''
G = {'A': 'BC', 'B': 'D', 'C': 'BE', 'D': 'A', 'E': 'D', 'F': 'EG',
     'G': 'C', 'H': 'GF'}
d, f, col, t, cnt = {}, {}, {v: 0 for v in G}, [0], {'cross': 0, 'back': 0}
def vis(u):
    t[0] += 1; d[u] = t[0]; col[u] = 1
    for v in sorted(G[u]):
        if col[v] == 0: vis(v)
        elif col[v] == 1: cnt['back'] += 1
        elif d[v] < d[u]: cnt['cross'] += 1
    col[u] = 2; t[0] += 1; f[u] = t[0]
for s in sorted(G):
    if col[s] == 0: vis(s)
assert cnt['cross'] == int(ANSWER) and cnt['back'] == 1
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BFS — buggy Python implementation',
            'text': 'The following BFS marks a vertex as seen only when it is **dequeued**. What does the program print?',
            'code': '''from collections import deque

def bfs(G, s):
    q, seen, out = deque([s]), set(), []
    while q:
        u = q.popleft()
        out.append(u)
        seen.add(u)
        for v in G[u]:
            if v not in seen:
                q.append(v)
    return out

G = {'A': 'BC', 'B': 'ACD', 'C': 'ABD', 'D': 'BC'}
print("".join(bfs(G, 'A')))''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1],
                    },
                    'caption': 'The graph G',
                },
            ],
            'options': ['`ABCD`', '`ABCCDD`', '`ABCCDDD`', '`ABCDCD`'],
            'answer': 'C',
            'solution': '''**Concept.** Correct BFS marks a vertex when it is *enqueued*. Marking on dequeue lets the same vertex be enqueued several times (once by every neighbour dequeued before it), so it is also output several times.

**Trace** (queue after processing each vertex):
- pop A → out A; seen {A}; push B, C → [B, C]
- pop B → out AB; seen {A, B}; A seen; push C, D → [C, C, D]
- pop C → out ABC; seen {A, B, C}; push D → [C, D, D]
- pop C → out ABCC; push D → [D, D, D]
- pop D → out ABCCD; seen adds D; neighbours B, C seen → [D, D]
- pop D, pop D → out ABCCDDD.

Printed: **`ABCCDDD`**.

**Options.**
- (A) is the output of a correct BFS.
- (B) misses that the *second* copy of C (dequeued before any D) pushes a third D.
- (D) interleaves the duplicates, but FIFO order keeps both Cs ahead of all Ds.

**Trap:** this bug does not cause an infinite loop (a seen vertex is never pushed again after it is dequeued), so it is easy to miss — but the queue can grow to Θ(m) and outputs repeat.''',
            'verify': '''
assert OUTPUT.strip() == "ABCCDDD" and ANSWER == 'C'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BFS — counting shortest paths',
            'text': 'In the unweighted undirected graph below, the number of distinct shortest paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['S', 'C'],
                        ['A', 'D'],
                        ['A', 'E'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['E', 'H'],
                        ['F', 'H'],
                        ['G', 'T'],
                        ['H', 'T'],
                        ['B', 'C'],
                        ['D', 'E'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'S': [0, 2],
                        'A': [2, 4],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 4],
                        'E': [4, 2],
                        'F': [4, 0],
                        'G': [6, 3],
                        'H': [6, 1],
                        'T': [8, 2],
                    },
                },
            ],
            'answer': '8',
            'solution': '''**Concept.** Run BFS from S. A shortest path to v ends with an edge (u, v) where level(u) = level(v) − 1, so ways(v) = ∑ ways(u) over such neighbours u. Edges joining two vertices of the **same** level never lie on a shortest path.

**Levels.** 0: S; 1: A, B, C; 2: D, E, F; 3: G, H; 4: T.
Same-level edges B–C, D–E, G–H are ignored.

**Counting.**
- ways(A) = ways(B) = ways(C) = 1.
- ways(D) = ways(A) = 1; ways(E) = A + B + C = 3; ways(F) = ways(C) = 1.
- ways(G) = D + E = 1 + 3 = 4; ways(H) = E + F = 3 + 1 = 4.
- ways(T) = G + H = 4 + 4 = **8**.

The shortest distance is 4 and there are **8** shortest paths.

**Trap:** counting a path such as S–B–C–E–… (which uses the same-level edge B–C) — it has length 5 to reach the next level and is not shortest.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS level and path counts',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'row_labels': ['level', 'ways'],
                    'rows': [
                        [0, 1, 1, 1, 2, 2, 2, 3, 3, 4],
                        [1, 1, 1, 1, 1, 3, 1, 4, 4, 8],
                    ],
                    'highlight': [
                        [1, 9],
                    ],
                },
            ],
            'verify': '''
from collections import deque
E = ["SA", "SB", "SC", "AD", "AE", "BE", "CE", "CF", "DG", "EG", "EH", "FH",
     "GT", "HT", "BC", "DE", "GH"]
G = {}
for a, b in E:
    G.setdefault(a, []).append(b); G.setdefault(b, []).append(a)
dist, ways, q = {'S': 0}, {'S': 1}, deque('S')
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in dist:
            dist[v] = dist[u] + 1; ways[v] = ways[u]; q.append(v)
        elif dist[v] == dist[u] + 1:
            ways[v] += ways[u]
assert ways['T'] == int(ANSWER) and dist['T'] == 4
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'DFS — parenthesis structure and edge types',
            'text': 'DFS is run on the directed graph below from vertex P, exploring out-neighbours in alphabetical order, with discovery/finish times from a clock that starts at 1 for the discovery of P. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'S'],
                        ['Q', 'R'],
                        ['R', 'T'],
                        ['S', 'R'],
                        ['S', 'T'],
                        ['T', 'U'],
                        ['U', 'Q'],
                    ],
                    'pos': {
                        'P': [0, 1.5],
                        'Q': [2, 3],
                        'R': [4, 2],
                        'S': [2, 0],
                        'T': [4, 0],
                        'U': [6, 3.5],
                    },
                },
            ],
            'options': [
                'The interval [d(S), f(S)] is nested inside the interval [d(Q), f(Q)]',
                'Edge (U, Q) is a back edge',
                'Edge (S, R) is a cross edge',
                'The graph contains a directed cycle',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Trace** (d / f):
- P 1 → Q 2 → R 3 → T 4 → U 5; U→Q: Q is grey → back edge. U f=6, T f=7, R f=8, Q f=9.
- P → S 10; S→R: R black, d(R) = 3 < 10 → cross edge; S→T: black, d(T) = 4 < 10 → cross edge. S f=11. P f=12.

Times: P 1/12, Q 2/9, R 3/8, S 10/11, T 4/7, U 5/6.

- (A) **False** — [10, 11] and [2, 9] are disjoint; S and Q are siblings under P, not ancestor/descendant. By the parenthesis theorem two intervals are either nested or disjoint.
- (B) **True** — Q is an ancestor of U still on the recursion stack.
- (C) **True** — R is finished and in a different subtree (discovered earlier).
- (D) **True** — a directed graph has a cycle iff DFS finds a back edge; here Q → R → T → U → Q.

**Trap:** S → R points 'upward' in the drawing but is not a back edge — R is not an ancestor of S in the DFS tree.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Discovery / finish times',
                    'col_labels': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'row_labels': ['d', 'f'],
                    'rows': [
                        [1, 2, 3, 10, 4, 5],
                        [12, 9, 8, 11, 7, 6],
                    ],
                },
            ],
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'P': 'QS', 'Q': 'R', 'R': 'T', 'S': 'RT', 'T': 'U', 'U': 'Q'}
d, f, col, t, kind = {}, {}, {v: 0 for v in G}, [0], {}
def vis(u):
    t[0] += 1; d[u] = t[0]; col[u] = 1
    for v in sorted(G[u]):
        if col[v] == 0: kind[u + v] = 'tree'; vis(v)
        elif col[v] == 1: kind[u + v] = 'back'
        elif d[u] < d[v]: kind[u + v] = 'fwd'
        else: kind[u + v] = 'cross'
    col[u] = 2; t[0] += 1; f[u] = t[0]
vis('P')
r = {'A': kind['UQ'] == 'back', 'B': kind['SR'] == 'cross',
     'C': d['Q'] < d['S'] and f['S'] < f['Q'],
     'D': 'back' in kind.values()}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'DFS — iterative stack implementation',
            'text': 'Consider the following iterative DFS on the directed graph shown (each adjacency string lists out-neighbours in alphabetical order). What is printed?',
            'code': '''def dfs(G, s):
    seen, st, out = set(), [s], []
    while st:
        u = st.pop()
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
        for v in G[u]:
            if v not in seen:
                st.append(v)
    return out

G = {'A': 'BCD', 'B': 'E', 'C': 'EF', 'D': 'F',
     'E': 'G', 'F': 'G', 'G': ''}
print("".join(dfs(G, 'A')))''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3.5],
                        'C': [2, 2],
                        'D': [2, 0.5],
                        'E': [4, 3],
                        'F': [4, 1],
                        'G': [6, 2],
                    },
                },
            ],
            'options': ['`ABEGCFD`', '`ADFGCEB`', '`ABCDEFG`', '`ADCBFEG`'],
            'answer': 'B',
            'solution': '''**Concept.** With an explicit stack, neighbours pushed in alphabetical order are *popped* in reverse alphabetical order, so this DFS prefers the alphabetically **last** neighbour. Marking on pop (with the `continue` check) keeps it a valid DFS order.

**Trace** (stack shown bottom → top after each step):
- pop A → out A; push B, C, D → [B, C, D]
- pop D → out AD; push F → [B, C, F]
- pop F → out ADF; push G → [B, C, G]
- pop G → out ADFG → [B, C]
- pop C → out ADFGC; E unseen → push E (F seen) → [B, E]
- pop E → out ADFGCE; G seen → [B]
- pop B → out ADFGCEB.

Printed: **`ADFGCEB`**.

**Options.**
- (A) is the recursive DFS order with alphabetical exploration.
- (C) is the BFS order.
- (D) treats the stack like a queue of reversed neighbour lists (a 'reverse BFS').

**Tip:** to make the iterative version match recursive alphabetical DFS, push neighbours in *reverse* alphabetical order.''',
            'verify': '''
assert OUTPUT.strip() == "ADFGCEB" and ANSWER == 'B'
order = []
def rec(u):
    order.append(u)
    for v in G[u]:
        if v not in order: rec(v)
rec('A')
assert "".join(order) == "ABEGCFD"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DAGs — counting topological orders',
            'text': 'The number of distinct topological orderings of the directed acyclic graph below is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['D', 'E'],
                        ['D', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [2, 3],
                        'D': [2, 1],
                        'E': [4, 2],
                        'F': [4, 0],
                    },
                },
            ],
            'answer': '12',
            'solution': '''**Concept.** Count by repeatedly choosing which current *source* (in-degree 0 vertex) comes first and recursing on the remaining DAG. (A DFS-based topological sort outputs just one of these orders: reverse finishing order.)

Constraints: A < C, A < D, B < D, C < E, D < E, D < F.

**Case 1: B first.** Then A must come next (it is the only source). The rest {C, D, E, F} with C < E, D < E, D < F:
- C next → remaining D, E, F with D first, then E, F in 2 orders → 2.
- D next → remaining C, E, F with only C < E: F can be in any of 3 slots around C, E → 3.
- Subtotal X = 5.

**Case 2: A first.** Sources now B, C.
- B next → the same sub-problem {C, D, E, F} → 5.
- C next → remaining B, D, E, F: B < D, D < E, D < F → B, D, then E/F in 2 orders → 2.
- Subtotal = 7.

Total = 5 + 7 = **12**.

**Trap:** multiplying independent-looking counts (e.g. 2 sources × …) double counts; always branch on the first vertex and recurse.''',
            'verify': '''
from functools import lru_cache
E = [("A", "C"), ("A", "D"), ("B", "D"), ("C", "E"), ("D", "E"), ("D", "F")]
V = "ABCDEF"
@lru_cache(None)
def cnt(rem):
    if not rem: return 1
    tot = 0
    for v in rem:
        if not any(b == v and a in rem for a, b in E):
            tot += cnt(rem.replace(v, ""))
    return tot
assert cnt(V) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array [14, 3, 27, 9, 31, 18, 6, 22] (indices 0–7) is converted into a **max**-heap by the standard bottom-up procedure: call sift-down on i = 3, 2, 1, 0 in that order, where sift-down swaps a node with its larger child while that child is larger. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [14, 3, 27, 9, 31, 18, 6, 22],
                    'caption': 'Initial array viewed as a complete binary tree',
                },
            ],
            'options': [
                'Exactly 4 swaps are performed in total',
                'Inserting the same keys one at a time (in array order) into an empty max-heap with sift-up produces the same final array',
                'Key 3 ends at a leaf position',
                'The resulting heap array is [31, 22, 27, 14, 3, 18, 6, 9]',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** Bottom-up heap construction sifts down every internal node from the last one (index ⌊n/2⌋ − 1 = 3) to the root. Total work is O(n).

**Trace.**
- i = 3 (9): child index 7 = 22 > 9 → swap. [14, 3, 27, 22, 31, 18, 6, 9] (1 swap)
- i = 2 (27): children 18, 6 → no swap.
- i = 1 (3): children 22, 31 → swap with 31 (index 4); index 4 has no children. [14, 31, 27, 22, 3, 18, 6, 9] (2)
- i = 0 (14): children 31, 27 → swap with 31 → index 1: children 22, 3 → swap with 22 → index 3: child 9 < 14 → stop. [31, 22, 27, 14, 3, 18, 6, 9] (4)

- (A) **True** — 1 + 0 + 1 + 2 = 4 swaps.
- (B) **False** — repeated insertion gives [31, 27, 18, 22, 9, 14, 6, 3]. The two methods generally produce different (both valid) heaps.
- (C) **True** — 3 is at index 4, whose children 9, 10 are beyond n − 1 = 7.
- (D) **True.**

**Trap:** stopping a sift-down after one swap; the key 14 must keep sinking until it is ≥ both children.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [31, 22, 27, 14, 3, 18, 6, 9],
                    'highlight': [3],
                    'caption': 'Max-heap after build-heap',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

H = [14, 3, 27, 9, 31, 18, 6, 22]; n = len(H); sw = 0
for i in range(n // 2 - 1, -1, -1):
    while True:
        l, r, b = 2 * i + 1, 2 * i + 2, i
        if l < n and H[l] > H[b]: b = l
        if r < n and H[r] > H[b]: b = r
        if b == i: break
        H[i], H[b] = H[b], H[i]; sw += 1; i = b
J = []
for x in [14, 3, 27, 9, 31, 18, 6, 22]:
    J.append(x); i = len(J) - 1
    while i and J[(i - 1) // 2] < J[i]:
        p = (i - 1) // 2; J[p], J[i] = J[i], J[p]; i = p
k = H.index(3)
r = {'A': H == [31, 22, 27, 14, 3, 18, 6, 9], 'B': sw == 4,
     'C': 2 * k + 1 >= n, 'D': J == H}
assert sorted(x for x in r if r[x]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra on an undirected graph',
            'text': "Dijkstra's algorithm is run from vertex A on the weighted undirected graph below. The sum of the final shortest-path distances from A to all six vertices (including A itself) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B', 4],
                        ['A', 'C', 1],
                        ['C', 'B', 2],
                        ['B', 'D', 5],
                        ['C', 'D', 8],
                        ['C', 'E', 10],
                        ['D', 'E', 2],
                        ['D', 'F', 6],
                        ['E', 'F', 3],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 2],
                        'E': [4, 0],
                        'F': [6, 1],
                    },
                },
            ],
            'answer': '35',
            'solution': '''**Concept.** Dijkstra finalises vertices in increasing order of distance; once extracted, a vertex's distance never changes (all weights are non-negative).

**Trace** (extracted vertex: updates):
- A (0): B = 4, C = 1.
- C (1): B = min(4, 1 + 2) = 3; D = 1 + 8 = 9; E = 1 + 10 = 11.
- B (3): D = min(9, 3 + 5) = 8.
- D (8): E = min(11, 8 + 2) = 10; F = 8 + 6 = 14.
- E (10): F = min(14, 10 + 3) = 13.
- F (13).

Distances: A 0, B 3, C 1, D 8, E 10, F 13. Sum = 0 + 3 + 1 + 8 + 10 + 13 = **35**.

**Trap:** taking the direct edges A–B = 4 or C–E = 10 at face value; both are beaten by detours (A–C–B = 3, A–C–B–D–E = 10 vs 11). Note also F is reached via E (13), not directly from D (14).''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B', 4],
                        ['A', 'C', 1],
                        ['C', 'B', 2],
                        ['B', 'D', 5],
                        ['C', 'D', 8],
                        ['C', 'E', 10],
                        ['D', 'E', 2],
                        ['D', 'F', 6],
                        ['E', 'F', 3],
                    ],
                    'highlight_edges': [
                        ['A', 'C'],
                        ['C', 'B'],
                        ['B', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 2],
                        'E': [4, 0],
                        'F': [6, 1],
                    },
                    'caption': 'Shortest-path tree from A',
                },
            ],
            'verify': '''
import heapq
E = [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 5), ("C", "D", 8),
     ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)]
G = {}
for a, b, w in E:
    G.setdefault(a, []).append((b, w)); G.setdefault(b, []).append((a, w))
d = {v: float('inf') for v in G}; d['A'] = 0; pq = [(0, 'A')]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d.values()) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — removing duplicates (buggy loop)',
            'text': 'The following program is intended to remove duplicate values from a sorted singly linked list. What does it print?',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

head = None
for v in reversed([1, 1, 1, 2, 3, 3, 3, 3, 4]):
    head = Node(v, head)
p = head
while p and p.next:
    if p.val == p.next.val:
        p.next = p.next.next
    p = p.next
out = []
while head:
    out.append(head.val)
    head = head.next
print(out)''',
            'options': ['`[1, 1, 2, 3, 3, 4]`', '`[1, 2, 3, 4]`', '`[1, 1, 2, 3, 4]`', '`[1, 2, 3, 3, 4]`'],
            'answer': 'A',
            'solution': '''**Concept.** After deleting `p.next`, the correct algorithm must **stay** on p (the new `p.next` may also equal p). This loop advances unconditionally, so in a run of equal values it deletes only every second extra copy.

**Trace** (subscripts mark copies): list 1a 1b 1c 2 3a 3b 3c 3d 4.
- p = 1a: next 1b equal → unlink 1b (1a → 1c); p = 1c.
- p = 1c: next 2 differs; p = 2.
- p = 2: next 3a differs; p = 3a.
- p = 3a: next 3b equal → unlink 3b (3a → 3c); p = 3c.
- p = 3c: next 3d equal → unlink 3d (3c → 4); p = 4.
- p = 4: p.next is None → stop.

Result: 1a, 1c, 2, 3a, 3c, 4 → **`[1, 1, 2, 3, 3, 4]`**.

**Options.**
- (B) is the intended result (needs `else: p = p.next`).
- (C) assumes the run of four 3s is fixed completely.
- (D) assumes the run of three 1s is fixed completely.

**Trap:** a run of length k keeps ⌈k/2⌉ copies with this bug: 3 ones → 2, 4 threes → 2.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 1, 2, 3, 3, 4],
                    'head': 'head',
                    'caption': 'List after the buggy loop',
                },
            ],
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "[1, 1, 2, 3, 3, 4]" and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merge sort — comparison counts',
            'text': 'Top-down merge sort (split a list of length n into the first ⌊n/2⌋ elements and the rest) sorts [21, 7, 33, 14, 2, 40, 19, 11]. Merging compares the front elements of the two halves and stops comparing as soon as one half is exhausted. Which of the following statements is/are TRUE?',
            'options': [
                'The final (top-level) merge performs 7 comparisons',
                'Merging [2, 40] with [11, 19] performs 2 comparisons',
                'No other permutation of 8 distinct keys makes this merge sort perform more comparisons',
                'The total number of element comparisons is 17',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** Merging lists of sizes p and q takes between min(p, q) and p + q − 1 comparisons. For n = 8 the worst case total is ∑ over levels = 4×1 + 2×3 + 1×7 = 17 (= n log₂ n − n + 1).

**Trace.**
- Level 1 (pairs): [21] [7] → 1; [33] [14] → 1; [2] [40] → 1; [19] [11] → 1. Subtotal 4.
- Level 2: [7, 21] + [14, 33]: 7<14, 21>14, 21<33, then left empty → 3. [2, 40] + [11, 19]: 2<11, 40>11, 40>19, right empty → 3. Subtotal 6.
- Level 3: [7, 14, 21, 33] + [2, 11, 19, 40]: outputs 2, 7, 11, 14, 19, 21, 33 each after one comparison, then 40 is copied → 7.
- Total = 4 + 6 + 7 = **17**.

**Statements.**
- (A) **True** — the halves interleave perfectly, so every merge step but the last needs a comparison.
- (B) **False** — it needs 3 comparisons, because 40 outlasts both 11 and 19.
- (C) **True** — every merge here hit its maximum p + q − 1, and 17 is the worst case for n = 8.
- (D) **True.**

**Trap:** assuming merging two lists of size 2 always takes 2 comparisons; it is 2 only when one list is entirely smaller than the other.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': 'r',
                    'children': {
                        'r': ['L', 'R'],
                        'L': ['LL', 'LR'],
                        'R': ['RL', 'RR'],
                    },
                    'labels': {
                        'r': '7 cmp',
                        'L': '3 cmp',
                        'R': '3 cmp',
                        'LL': '1',
                        'LR': '1',
                        'RL': '1',
                        'RR': '1',
                    },
                    'caption': 'Comparisons per merge in the recursion tree',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def ms(a, c):
    if len(a) <= 1: return a
    m = len(a) // 2
    L, R = ms(a[:m], c), ms(a[m:], c)
    o, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
c = [0]; ms([21, 7, 33, 14, 2, 40, 19, 11], c)
mx = 0
for p in itertools.permutations(range(8)):
    k = [0]; ms(list(p), k); mx = max(mx, k[0])
def mc(L, R):
    i = j = k = 0
    while i < len(L) and j < len(R):
        k += 1
        if L[i] <= R[j]: i += 1
        else: j += 1
    return k
r = {'A': c[0] == 17, 'B': mc([7, 14, 21, 33], [2, 11, 19, 40]) == 7,
     'C': c[0] == mx, 'D': mc([2, 40], [11, 19]) == 2}
assert c[0] == 17 and mx == 17
assert sorted(x for x in r if r[x]) == sorted(ANSWER)
''',
        },
    ],
}
