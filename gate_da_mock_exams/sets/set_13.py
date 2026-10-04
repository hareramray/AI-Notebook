# Set 13 — Graph Theory Fundamentals
SET = {
    'number': 13,
    'title': 'Graph Theory Fundamentals',
    'difficulty': 'Moderate',
    'focus': 'degrees, handshaking, trees, simple graphs, complete/bipartite graphs',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — dict.fromkeys aliasing in adjacency sets',
            'text': 'Consider the following Python program that builds an undirected graph. What is printed?',
            'code': '''nodes = 'abcd'
adj = dict.fromkeys(nodes, set())
for u, v in [('a', 'b'), ('b', 'c'), ('c', 'd')]:
    adj[u].add(v)
    adj[v].add(u)
print(len(adj['a']), sum(len(s) for s in adj.values()))''',
            'options': ['`1 6`', '`4 16`', '`1 3`', '`4 4`'],
            'answer': 'B',
            'solution': '''`dict.fromkeys(keys, value)` stores the **same** `value` object under every key. Here all four keys refer to one single set, so every `add` goes into that shared set.

- After the loop the shared set contains every endpoint ever added: {a, b, c, d}.
- `len(adj['a'])` = 4.
- The sum iterates over four references to the same 4-element set → 4 × 4 = 16.

Output: **4 16**.

Option-by-option:

- (A) `1 6` is what a correct adjacency structure gives (degrees 1, 2, 2, 1; sum = 2|E| = 6).
- (C) `1 3` additionally confuses the degree sum with |E|.
- (D) `4 4` realises the set is shared but forgets that `values()` yields it four times.

**Trap:** the same aliasing bug occurs with `[[]] * n`. **Fix:** `adj = {v: set() for v in nodes}` creates a fresh set per key.''',
            'verify': '''
assert OUTPUT.strip() == "4 16" and ANSWER == "B"
good = {v: set() for v in "abcd"}
for u, v in [("a", "b"), ("b", "c"), ("c", "d")]:
    good[u].add(v); good[v].add(u)
assert (len(good["a"]), sum(len(s) for s in good.values())) == (1, 6)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Handshaking lemma',
            'text': 'A simple undirected graph has 8 vertices and 15 edges. Every vertex has degree either 3 or 5. The number of vertices of degree 5 is ______.',
            'answer': '3',
            'solution': '''**Handshaking lemma:** the sum of all vertex degrees equals 2|E|, because each edge contributes one to the degree of each of its two endpoints.

Let a vertices have degree 3 and b vertices have degree 5:

- a + b = 8
- 3a + 5b = 2 × 15 = 30

Substituting a = 8 − b: 24 − 3b + 5b = 30 → 2b = 6 → **b = 3** (and a = 5).

Sanity check: the number of odd-degree vertices must be even — here all 8 vertices have odd degree, which is fine. Such a graph exists (e.g. three degree-5 hubs plus a suitable arrangement of the others).

**Trap:** using |E| = 15 instead of 2|E| = 30 gives 3a + 5b = 15, which has no solution with a + b = 8 — a clear sign of the error.''',
            'verify': '''
sols = [b for b in range(9) if 3 * (8 - b) + 5 * b == 30]
assert sols == [int(ANSWER)]
import itertools, random
random.seed(1)
# construct an explicit witness: degree sequence 5,5,5,3,3,3,3,3 is graphical
def hh(s):
    s = sorted(s, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d): s[i] -= 1
        if min(s) < 0: return False
        s.sort(reverse=True)
    return True
assert hh([5, 5, 5, 3, 3, 3, 3, 3])
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graphical degree sequences',
            'text': 'A sequence of non-negative integers is *graphical* if it is the degree sequence of some **simple** undirected graph. Which of the following sequences is/are graphical?',
            'options': ['(4, 3, 3, 2, 2, 2)', '(5, 4, 3, 2, 1, 1)', '(3, 3, 3, 3, 2, 2)', '(3, 3, 3, 1)'],
            'answer': ['A', 'C'],
            'solution': '''Use the **Havel–Hakimi** test: remove the largest degree d, subtract 1 from the next d largest entries, re-sort, repeat. The sequence is graphical iff we reach all zeros without a negative entry or a d larger than the remaining length. (An odd sum fails at once.)

- (A) 4,3,3,2,2,2 → 2,2,1,1,2 → sort 2,2,2,1,1 → 1,1,1,1 → 0,1,1 → 0,0. **Graphical.**
- (B) sum 16 is even, but 5 on 6 vertices means that vertex is adjacent to **all** others, so every other degree is ≥ 1; remove it → 3,2,1,0,0; then 3 → 1,0,−1 ✗. **Not graphical** — the two degree-1 vertices are both used up by the degree-5 vertex, so the degree-4 vertex can reach at most 3 others.
- (C) 3,3,3,3,2,2 → 2,2,2,2,2 → 1,1,2,2 → sort 2,2,1,1 → 1,0,1 → 1,1,0 → 0,0. **Graphical** (e.g. a 6-cycle with two chords).
- (D) sum 10 is even, but 3,3,3 on 4 vertices: each degree-3 vertex is adjacent to all others, so the fourth vertex would have degree 3, not 1. **Not graphical.**

**Trap:** an even degree sum is necessary but **not** sufficient — (B) and (D) both pass the parity check.''',
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def hh(s):
    s = sorted(s, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d): s[i] -= 1
        if min(s) < 0: return False
        s.sort(reverse=True)
    return True
opts = [(3, 3, 3, 3, 2, 2), (5, 4, 3, 2, 1, 1), (4, 3, 3, 2, 2, 2), (3, 3, 3, 1)]
assert all(sum(o) % 2 == 0 for o in opts)
assert sorted(ANSWER) == [c for c, o in zip("ABCD", opts) if hh(o)]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Trees — counting leaves from degrees',
            'text': 'A tree has exactly 4 vertices of degree 3, exactly 2 vertices of degree 2, and every other vertex is a leaf (degree 1). The number of leaves is ______.',
            'answer': '6',
            'solution': '''A tree on n vertices has n − 1 edges, so its degree sum is 2(n − 1).

Let L be the number of leaves. Then n = 4 + 2 + L = 6 + L and

- degree sum = 4·3 + 2·2 + L·1 = 16 + L
- 2(n − 1) = 2(5 + L) = 10 + 2L

16 + L = 10 + 2L → **L = 6**.

General shortcut: L = 2 + Σ over internal vertices of (deg − 2) = 2 + 4·1 + 2·0 = 6. Degree-2 vertices never change the leaf count.

**Trap:** forgetting the leaves in the degree sum, or using |E| = n instead of n − 1.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': 'a',
                    'children': {
                        'a': ['b', 'c', 'l1'],
                        'b': ['d', 'l2'],
                        'c': ['e', 'l3'],
                        'd': ['l4', 'l5'],
                        'e': ['f'],
                        'f': ['l6'],
                    },
                    'highlight': ['l1', 'l2', 'l3', 'l4', 'l5', 'l6'],
                    'caption': 'One such tree: a, b, c, d have degree 3; e, f degree 2',
                },
            ],
            'verify': '''
L = [x for x in range(50) if 4 * 3 + 2 * 2 + x == 2 * (6 + x - 1)]
assert L == [int(ANSWER)]
ch = {"a": ["b", "c", "l1"], "b": ["d", "l2"], "c": ["e", "l3"], "d": ["l4", "l5"], "e": ["f"], "f": ["l6"]}
deg = {}
for p, cs in ch.items():
    for c in cs:
        deg[p] = deg.get(p, 0) + 1; deg[c] = deg.get(c, 0) + 1
assert sorted(deg.values()).count(1) == 6 and sorted(deg.values()).count(3) == 4
assert sorted(deg.values()).count(2) == 2
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — feasible pop sequences',
            'text': 'The letters a, b, c, d, e are pushed onto an initially empty stack in this order. Pops may be interleaved with pushes at any time, and every popped letter is printed. Which of the following printed sequences is NOT possible?',
            'options': ['b a d c e', 'c d b e a', 'a c b e d', 'd e c a b'],
            'answer': 'D',
            'solution': '''Key rule: once x is popped, every element pushed before x that is still on the stack must come out in **reverse** push order.

- (A) push a, b; pop b, a; push c, d; pop d, c; push e; pop e. **Possible.**
- (B) push a, b, c; pop c; push d; pop d; pop b; push e; pop e; pop a. **Possible.**
- (C) push a; pop a; push b, c; pop c, b; push d, e; pop e, d. **Possible.**
- (D) push a, b, c, d; pop d; push e; pop e; pop c. The stack now holds a (bottom), b (top). The next pop must give **b**, but the sequence asks for a. **Impossible.**

**Tip:** a sequence is infeasible exactly when it contains a pattern …k…i…j… with i < j < k in push order (here d … a … b).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['a', 'b'],
                    'label': 'stack in (D) after d, e, c popped',
                },
            ],
            'verify': '''
def ok(push, pop):
    st, i = [], 0
    for x in pop:
        while (not st or st[-1] != x) and i < len(push):
            st.append(push[i]); i += 1
        if st[-1] != x: return False
        st.pop()
    return True
opts = ["badce", "cdbea", "acbed", "decab"]
assert [c for c, o in zip("ABCD", opts) if not ok("abcde", o)] == [ANSWER]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bipartite graphs and odd cycles',
            'text': 'Consider the undirected graph G below (a 6-cycle A–B–C–D–E–F–A with two chords A–C and A–D). Removing which **single** edge makes G bipartite?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'A'],
                        ['A', 'C'],
                        ['A', 'D'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1, 2],
                        'C': [2.5, 2],
                        'D': [3.5, 1],
                        'E': [2.5, 0],
                        'F': [1, 0],
                    },
                },
            ],
            'options': ['A–C', 'A–B', 'A–D', 'C–D'],
            'answer': 'A',
            'solution': '''A graph is bipartite **iff it has no odd cycle**. So we need an edge that lies on every odd cycle.

Odd cycles of G: A–B–C (length 3), A–C–D (length 3), A–C–D–E–F (length 5). The only edge common to all three is **A–C**.

After deleting A–C the remaining cycles are A–B–C–D (4), A–D–E–F (4) and the outer hexagon (6) — all even. A valid 2-colouring: {A, C, E} vs {B, D, F}.

- (B) removing A–B leaves triangle A–C–D. ✗
- (C) removing A–D leaves triangle A–B–C. ✗
- (D) removing C–D leaves triangle A–B–C. ✗

**Tip:** try a BFS 2-colouring; a conflict edge (both ends same colour) pinpoints an odd cycle.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

def bip(edges):
    col = {}
    for s in "ABCDEF":
        if s in col: continue
        col[s] = 0; st = [s]
        while st:
            u = st.pop()
            for a, b in edges:
                for x, y in ((a, b), (b, a)):
                    if x == u:
                        if y not in col: col[y] = 1 - col[u]; st.append(y)
                        elif col[y] == col[u]: return False
    return True
E = [("A","B"),("B","C"),("C","D"),("D","E"),("E","F"),("F","A"),("A","C"),("A","D")]
cands = [("A","B"), ("A","C"), ("A","D"), ("C","D")]
assert not bip(E)
assert [c for c, e in zip("ABCD", cands) if bip([x for x in E if x != e])] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — linear probing cost',
            'text': 'The keys 23, 47, 13, 35, 58, 2, 24 are inserted in that order into an initially empty hash table of size 11 with h(k) = k mod 11 and linear probing (step +1). A *probe* is one inspection of a slot, including the slot where the key is finally placed. The total number of probes for all seven insertions is ______.',
            'answer': '20',
            'solution': '''Linear probing inspects h(k), h(k)+1, … until an empty slot is found.

- 23 → home 1, empty → 1 probe
- 47 → home 3, empty → 1 probe
- 13 → home 2, empty → 1 probe
- 35 → home 2 (full), 3 (full), 4 → **3** probes
- 58 → home 3 (full), 4 (full), 5 → **3** probes
- 2 → home 2, 3, 4, 5 full, 6 → **5** probes
- 24 → home 2, 3, 4, 5, 6 full, 7 → **6** probes

Total = 1 + 1 + 1 + 3 + 3 + 5 + 6 = **20**.

**Trap:** counting only *collisions* (failed probes) gives 20 − 7 = 13. Read the definition. **Note:** the cluster 1–7 grows quickly — primary clustering makes later keys with homes 2 or 3 increasingly expensive.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        1: 23,
                        2: 13,
                        3: 47,
                        4: 35,
                        5: 58,
                        6: 2,
                        7: 24,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 11; tot = 0
for k in [23, 47, 13, 35, 58, 2, 24]:
    i = k % 11; tot += 1
    while T[i] is not None:
        i = (i + 1) % 11; tot += 1
    T[i] = k
assert tot == int(ANSWER) and T[7] == 24
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Selection sort — swaps',
            'text': 'Selection sort (ascending) is applied to [4, 9, 2, 7, 1, 8, 3]. In pass i it finds the minimum of A[i..n−1] and swaps it with A[i] **only if** it is not already at index i. The number of swaps performed is',
            'options': ['4', '5', '6', '3'],
            'answer': 'A',
            'solution': '''Selection sort always makes n(n−1)/2 = 21 comparisons, but the number of swaps depends on the data.

- i=0: min 1 at index 4 → swap → [1, 9, 2, 7, 4, 8, 3]
- i=1: min 2 at index 2 → swap → [1, 2, 9, 7, 4, 8, 3]
- i=2: min 3 at index 6 → swap → [1, 2, 3, 7, 4, 8, 9]
- i=3: min 4 at index 4 → swap → [1, 2, 3, 4, 7, 8, 9]
- i=4: 7 already in place — no swap
- i=5: 8 already in place — no swap

Total = **4** swaps.

- (B) 5 counts the pass i=4 as a swap although 7 is already in place.
- (C) 6 is the count if every one of the n − 1 passes swapped unconditionally.
- (D) 3 misses that the swap at i=2 sends 9 to the end, so i=3 still needs a swap.

**Tip:** swaps = n − (number of cycles of the permutation). Index cycles here: (0 → 3 → 4), (1 → 6 → 2) and the fixed point 5 (value 8) — 3 cycles, so 7 − 3 = 4.''',
            'verify': '''
A = [4, 9, 2, 7, 1, 8, 3]; sw = 0
for i in range(len(A) - 1):
    m = min(range(i, len(A)), key=lambda j: A[j])
    if m != i:
        A[i], A[m] = A[m], A[i]; sw += 1
assert sw == 4 and ANSWER == "A"
B = [4, 9, 2, 7, 1, 8, 3]; s = sorted(B); seen = set(); cyc = 0
for i in range(7):
    if i in seen: continue
    cyc += 1; j = i
    while j not in seen:
        seen.add(j); j = s.index(B[j])
assert 7 - cyc == 4
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — sets, tuples and frozensets for edges',
            'text': 'Which of the following Python expressions evaluate to `True`?',
            'options': [
                "`sorted({3: 'a', 1: 'b'}) == ['a', 'b']`",
                '`len({(1, 2), (2, 1)}) == 1`',
                '`len({frozenset((1, 2)), frozenset((2, 1))}) == 1`',
                '`({1, 2, 3} ^ {2, 3, 4}) == {1, 4}`',
            ],
            'answer': ['C', 'D'],
            'solution': '''These are the usual ways to store undirected edges and neighbour sets.

- (A) iterating a dict yields its **keys**; `sorted` gives `[1, 3]`. **False.**
- (B) tuples are ordered, so (1, 2) ≠ (2, 1); the set has 2 elements. **False.** This is why storing an undirected edge as a tuple can double-count it.
- (C) a frozenset is unordered and hashable, so both describe the same edge → set of size 1. **True.**
- (D) `^` is symmetric difference: elements in exactly one set → {1, 4}. **True.**

**Tip:** for undirected edges either normalise to `(min(u, v), max(u, v))` or use `frozenset({u, v})`.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

truth = [({1, 2, 3} ^ {2, 3, 4}) == {1, 4}, len({(1, 2), (2, 1)}) == 1,
         len({frozenset((1, 2)), frozenset((2, 1))}) == 1, sorted({3: 'a', 1: 'b'}) == ['a', 'b']]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Adjacency lists — counting list nodes',
            'text': 'A directed graph has vertices 1, 2, …, 20. There is an edge i → j if and only if j = i + 1 or j = 2i (with j ≤ 20). The graph is stored as adjacency lists, one singly linked list node per edge. The total number of linked-list nodes is',
            'options': ['29', '28', '56', '30'],
            'answer': 'B',
            'solution': '''In a directed graph each edge appears in exactly one adjacency list (that of its tail), so the number of nodes equals |E|.

- Edges i → i + 1 for i = 1 … 19: **19** edges.
- Edges i → 2i for i = 1 … 10 (2i ≤ 20): **10** edges.
- Overlap: i + 1 = 2i only when i = 1, i.e. the edge 1 → 2 is described twice but is one edge. Subtract 1.

|E| = 19 + 10 − 1 = **28**.

- (A) 29 forgets the overlap.
- (C) 56 doubles the count, as for an undirected graph (each edge stored twice).
- (D) 30 uses 20 and 10 edges, wrongly including 20 → 21.

**Tip:** adjacency lists use Θ(V + E) space: 20 head pointers + 28 nodes here.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

E = {(i, j) for i in range(1, 21) for j in (i + 1, 2 * i) if j <= 20}
assert len(E) == 28 and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Labelled graphs and trees — counting',
            'text': 'Consider all simple undirected graphs on the labelled vertex set {1, 2, 3, 4} that have **exactly 3 edges**. The number of these graphs that are connected is ______.',
            'answer': '16',
            'solution': '''K₄ has C(4, 2) = 6 possible edges, so there are C(6, 3) = **20** graphs with exactly 3 edges.

A graph on 4 vertices with 3 = n − 1 edges is connected **iff** it is a tree (a connected graph needs ≥ n − 1 edges, and connected with exactly n − 1 edges means acyclic). So we can count either way:

- **Disconnected** 3-edge graphs: with only 3 edges the only way to waste an edge is a cycle, and the only cycle that fits is a triangle; a triangle on 3 of the 4 vertices leaves the fourth vertex isolated. There are C(4, 3) = **4** triangles.
- Connected = 20 − 4 = **16**.

Cross-check with **Cayley's formula**: the number of labelled trees on n vertices is n^{n−2} = 4² = 16. ✓ (Shape split: 4 stars K₁,₃ + 12 paths P₄ = 16.)

**Trap:** counting unlabelled shapes (only 2: star and path) instead of labelled graphs.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['1', '2', '3', '4'],
                    'edges': [
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '1'],
                    ],
                    'pos': {
                        '1': [0, 0],
                        '2': [2, 0],
                        '3': [1, 1.6],
                        '4': [3.5, 0.8],
                    },
                    'highlight': ['4'],
                    'caption': 'One of the 4 disconnected cases: triangle + isolated vertex',
                },
            ],
            'verify': '''
import itertools
V = range(4); E = list(itertools.combinations(V, 2)); cnt = 0
for es in itertools.combinations(E, 3):
    comp = {v: v for v in V}
    def f(x):
        while comp[x] != x: x = comp[x]
        return x
    for a, b in es: comp[f(a)] = f(b)
    cnt += len({f(v) for v in V}) == 1
assert cnt == int(ANSWER) == 4 ** 2
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Complete bipartite graphs',
            'text': 'Let G be the complete bipartite graph K₃,₄ shown below (parts X = {x1, x2, x3} and Y = {y1, y2, y3, y4}). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['x1', 'x2', 'x3', 'y1', 'y2', 'y3', 'y4'],
                    'edges': [
                        ['x1', 'y1'],
                        ['x1', 'y2'],
                        ['x1', 'y3'],
                        ['x1', 'y4'],
                        ['x2', 'y1'],
                        ['x2', 'y2'],
                        ['x2', 'y3'],
                        ['x2', 'y4'],
                        ['x3', 'y1'],
                        ['x3', 'y2'],
                        ['x3', 'y3'],
                        ['x3', 'y4'],
                    ],
                    'pos': {
                        'x1': [0, 2.5],
                        'x2': [0, 1.5],
                        'x3': [0, 0.5],
                        'y1': [3, 3],
                        'y2': [3, 2],
                        'y3': [3, 1],
                        'y4': [3, 0],
                    },
                    'caption': 'K₃,₄',
                },
            ],
            'options': [
                'The complement of G (with respect to K₇ on the same 7 vertices) has exactly 9 edges',
                'G contains a cycle of length 5',
                'G has an Euler circuit',
                'G has exactly 12 edges',
            ],
            'answer': ['A', 'D'],
            'solution': '''In Kₘ,ₙ every vertex of one part is adjacent to every vertex of the other part and to none in its own part.

- (A) K₇ has C(7, 2) = 21 edges; the complement has 21 − 12 = 9 edges — exactly a K₃ on X (3 edges) plus a K₄ on Y (6 edges). **True.**
- (B) Every edge goes X ↔ Y, so any closed walk alternates sides and has **even** length. A bipartite graph has no odd cycle. **False.**
- (C) An Euler circuit needs every degree even. The x-vertices have degree 4 (even) but the y-vertices have degree 3 (odd). **False.** (Four odd vertices also rule out an Euler trail.)
- (D) |E| = m·n = 3·4 = 12. **True.** (Check by handshaking: 3·4 + 4·3 = 24 = 2·12.)

**Trap:** in (C), the even degree of the X side is irrelevant — *all* vertices must have even degree. **Tip:** the complement of Kₘ,ₙ is always Kₘ ∪ Kₙ.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
X = ["x1", "x2", "x3"]; Y = ["y1", "y2", "y3", "y4"]
E = {frozenset((x, y)) for x in X for y in Y}
V = X + Y
deg = {v: sum(v in e for e in E) for v in V}
comp = {frozenset(p) for p in itertools.combinations(V, 2)} - E
has5 = False
for cyc in itertools.permutations(V, 5):
    if all(frozenset((cyc[i], cyc[(i + 1) % 5])) in E for i in range(5)):
        has5 = True; break
truth = [len(E) == 12, has5, all(d % 2 == 0 for d in deg.values()), len(comp) == 9]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BFS — counting shortest paths',
            'text': 'The undirected unweighted graph below is a 3 × 4 grid from which the edges b–f and f–g have been removed. The number of distinct shortest paths from a to l is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
                    'edges': [
                        ['a', 'b'],
                        ['b', 'c'],
                        ['c', 'd'],
                        ['e', 'f'],
                        ['g', 'h'],
                        ['i', 'j'],
                        ['j', 'k'],
                        ['k', 'l'],
                        ['a', 'e'],
                        ['e', 'i'],
                        ['f', 'j'],
                        ['c', 'g'],
                        ['g', 'k'],
                        ['d', 'h'],
                        ['h', 'l'],
                    ],
                    'pos': {
                        'a': [0, 4],
                        'b': [1.5, 4],
                        'c': [3, 4],
                        'd': [4.5, 4],
                        'e': [0, 2],
                        'f': [1.5, 2],
                        'g': [3, 2],
                        'h': [4.5, 2],
                        'i': [0, 0],
                        'j': [1.5, 0],
                        'k': [3, 0],
                        'l': [4.5, 0],
                    },
                },
            ],
            'answer': '5',
            'solution': '''In BFS, the number of shortest paths to v is σ(v) = Σ σ(u) over neighbours u with dist(u) = dist(v) − 1. Process level by level (σ(a) = 1):

- dist 1: b (σ=1), e (σ=1)
- dist 2: c ← b (1); f ← e only, since b–f is gone (1); i ← e (1)
- dist 3: d ← c (1); g ← c only, since f–g is gone (1); j ← f, i (1 + 1 = 2)
- dist 4: h ← d, g (1 + 1 = 2); k ← g, j (1 + 2 = 3)
- dist 5: l ← h, k (2 + 3 = **5**)

The 5 paths: a-b-c-d-h-l, a-b-c-g-h-l, a-b-c-g-k-l, a-e-f-j-k-l, a-e-i-j-k-l. dist(a, l) is still 5 = 2 + 3, the Manhattan distance.

**Trap:** the complete 3 × 4 grid would give C(5, 2) = 10 paths; the two deleted edges remove exactly half of them. Do not reuse the binomial formula once edges are missing.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS distance / path count σ',
                    'row_labels': ['row 1', 'row 2', 'row 3'],
                    'col_labels': ['col 1', 'col 2', 'col 3', 'col 4'],
                    'rows': [
                        ['a: 0 / 1', 'b: 1 / 1', 'c: 2 / 1', 'd: 3 / 1'],
                        ['e: 1 / 1', 'f: 2 / 1', 'g: 3 / 1', 'h: 4 / 2'],
                        ['i: 2 / 1', 'j: 3 / 2', 'k: 4 / 3', 'l: 5 / 5'],
                    ],
                    'highlight': [
                        [2, 3],
                    ],
                },
            ],
            'verify': '''
from collections import deque
names = "abcdefghijkl"; adj = {x: set() for x in names}
for r in range(3):
    for c in range(4):
        u = names[4 * r + c]
        if c < 3: adj[u].add(names[4 * r + c + 1]); adj[names[4 * r + c + 1]].add(u)
        if r < 2: adj[u].add(names[4 * r + c + 4]); adj[names[4 * r + c + 4]].add(u)
for u, v in [("b", "f"), ("f", "g")]:
    adj[u].discard(v); adj[v].discard(u)
dist = {"a": 0}; sig = {"a": 1}; q = deque("a")
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist: dist[v] = dist[u] + 1; sig[v] = sig[u]; q.append(v)
        elif dist[v] == dist[u] + 1: sig[v] += sig[u]
assert sig["l"] == int(ANSWER) and dist["l"] == 5
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'DFS — discovery and finish times',
            'text': "Depth-first search is run on the directed graph below. The outer loop considers start vertices in alphabetical order, and each vertex's out-neighbours are explored in alphabetical order. The clock starts at 1 and is incremented at every discovery and every finish. The (discovery, finish) times of vertex **D** are",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['C', 'A'],
                        ['D', 'E'],
                        ['E', 'C'],
                        ['F', 'D'],
                        ['F', 'E'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3],
                        'C': [4, 2],
                        'D': [0, 0],
                        'E': [2.5, 1],
                        'F': [2, -1],
                    },
                },
            ],
            'options': ['(4, 9)', '(5, 6)', '(8, 9)', '(9, 10)'],
            'answer': 'C',
            'solution': '''DFS finishes a vertex only after everything newly reachable from it has finished.

- A discovered 1 → B 2 → C 3; C→A is a **back edge**; C finishes 4
- back at B: E discovered 5; E→C goes to a finished vertex (**cross edge**); E finishes 6
- B finishes 7
- back at A: D discovered **8**; D→E is a cross edge; D finishes **9**
- A finishes 10; F discovered 11 (new DFS tree), F→D, F→E cross; F finishes 12

So D = **(8, 9)**.

- (A) (4, 9) would come from exploring D right after C, ignoring that B's subtree (including E) must finish first.
- (B) (5, 6) are E's times.
- (D) (9, 10) forgets that the clock also ticks when B finishes.

**Tip:** the cycle A→B→C→A is detected by the back edge C→A (C's ancestor A is still on the recursion stack).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'DFS timestamps',
                    'col_labels': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'row_labels': ['discovery', 'finish'],
                    'rows': [
                        [1, 2, 3, 8, 5, 11],
                        [10, 7, 4, 9, 6, 12],
                    ],
                    'highlight': [
                        [0, 3],
                        [1, 3],
                    ],
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

G = {"A": "BD", "B": "CE", "C": "A", "D": "E", "E": "C", "F": "DE"}
t = [0]; d = {}; f = {}
def dfs(u):
    t[0] += 1; d[u] = t[0]
    for v in G[u]:
        if v not in d: dfs(v)
    t[0] += 1; f[u] = t[0]
for s in sorted(G):
    if s not in d: dfs(s)
assert (d["D"], f["D"]) == (8, 9) and (d["E"], f["E"]) == (5, 6) and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — connected components',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''edges = [(1, 2), (3, 4), (2, 5), (6, 6),
         (7, 8), (5, 1), (8, 9)]
n = 10
adj = {v: [] for v in range(1, n + 1)}
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)
seen, comps, sizes = set(), 0, []
for s in adj:
    if s in seen:
        continue
    comps += 1
    stack, c = [s], 0
    seen.add(s)
    while stack:
        u = stack.pop()
        c += 1
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    sizes.append(c)
print(comps * 10 + max(sizes))''',
            'answer': '53',
            'solution': '''The program counts connected components with an iterative DFS and records each component's size (number of vertices popped).

Components of the graph on vertices 1…10:

- {1, 2, 5} (edges 1–2, 2–5, 5–1 form a triangle) — size 3
- {3, 4} — size 2
- {6} — the self-loop (6, 6) appends 6 twice to `adj[6]` but adds no new vertex — size 1
- {7, 8, 9} — size 3
- {10} — isolated, still a component — size 1

comps = 5, max size = 3 → printed 5·10 + 3 = **53**.

Because vertices are marked `seen` when pushed, no vertex is counted twice even though the triangle offers two routes to 5.

**Traps:** forgetting the isolated vertex 10 (gives 43), or thinking the self-loop joins 6 to something. **Tip:** comps − 1 = 4 extra edges are needed to connect this graph.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['1', '2', '5', '3', '4', '6', '7', '8', '9', '10'],
                    'edges': [
                        ['1', '2'],
                        ['2', '5'],
                        ['5', '1'],
                        ['3', '4'],
                        ['7', '8'],
                        ['8', '9'],
                    ],
                    'pos': {
                        '1': [0, 1],
                        '2': [1, 1],
                        '5': [0.5, 0],
                        '3': [2, 1],
                        '4': [2, 0],
                        '6': [3, 0.5],
                        '7': [4, 1],
                        '8': [5, 1],
                        '9': [5, 0],
                        '10': [6, 0.5],
                    },
                    'caption': 'Five components (self-loop at 6 not drawn)',
                },
            ],
            'verify': '''
assert OUTPUT.strip() == ANSWER
p = list(range(11))
def f(x):
    while p[x] != x: x = p[x]
    return x
for u, v in edges: p[f(u)] = f(v)
roots = [f(v) for v in range(1, 11)]
assert len(set(roots)) == 5 and max(roots.count(r) for r in roots) == 3
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Edges, components and cycles',
            'text': 'G is a simple undirected graph with 10 vertices and 7 edges. Which of the following statements is/are **necessarily** TRUE?',
            'options': [
                'If G has no cycle, then G has exactly 3 connected components',
                'G has at least 3 connected components',
                'G has a vertex of degree at most 1',
                'G contains a cycle',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Key facts: a connected graph on c vertices has ≥ c − 1 edges; a forest with n vertices and k components has exactly n − k edges.

- (A) For a forest, |E| = n − k → 7 = 10 − k → k = 3. **True.**
- (B) If G has k components of sizes c₁, …, c_{k}, then 7 = |E| ≥ Σ(cᵢ − 1) = 10 − k, so k ≥ 3. **True.**
- (C) Degree sum = 14 < 2·10 = 20, so the average degree is 1.4 < 2; some vertex must have degree ≤ 1. **True.**
- (D) A forest of 3 trees, e.g. a path on 8 vertices plus 2 isolated vertices, has 7 edges and no cycle. **False** (not necessarily).

**Trap:** (D) confuses 'too few edges to be connected' with 'must have a cycle'. A cycle is forced only when |E| ≥ n, which is not the case here.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools, random
random.seed(7)
allE = list(itertools.combinations(range(10), 2))
def comps(es):
    p = list(range(10))
    def f(x):
        while p[x] != x: x = p[x]
        return x
    cyc = False
    for a, b in es:
        ra, rb = f(a), f(b)
        if ra == rb: cyc = True
        else: p[ra] = rb
    return len({f(v) for v in range(10)}), cyc
okA = okC = okD = True; foundB = False
for _ in range(4000):
    es = random.sample(allE, 7)
    k, cyc = comps(es)
    deg = [sum(v in e for e in es) for v in range(10)]
    okA &= k >= 3; okD &= min(deg) <= 1
    if not cyc: okC &= k == 3; foundB = True
assert okA and okC and okD and foundB
assert sorted(ANSWER) == ["A", "C", "D"]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — counting comparisons',
            'text': 'Quicksort with the Lomuto partition (pivot = last element of the subarray; for each j from lo to hi − 1 compare A[j] ≤ pivot; finally place the pivot) is used to sort [5, 3, 8, 1, 9, 2, 7]. Subarrays of size 0 or 1 are not partitioned. The total number of element comparisons `A[j] ≤ pivot` made over the whole sort is ______.',
            'answer': '11',
            'solution': '''A Lomuto partition of a subarray of size s makes exactly s − 1 comparisons, so we only need the sizes of all partitioned subarrays.

- [5 3 8 1 9 2 7], pivot 7: 6 comparisons → [5 3 1 2 | **7** | 8 9]
- left [5 3 1 2], pivot 2: 3 comparisons → [1 | **2** | 5 3]
- [1] size 1 — skip; [5 3], pivot 3: 1 comparison → [**3** 5]
- right [8 9], pivot 9: 1 comparison → [8 **9**]

Total = 6 + 3 + 1 + 1 = **11**.

Compare: the best possible for n = 7 is 10 (perfect 3|3 split, then 1|1 twice → 6 + 2 + 2) and the worst is 21 (sorted input, n(n−1)/2).

**Trap:** counting the final pivot swap as a comparison, or partitioning size-1 subarrays.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [5, 3, 1, 2, 7, 8, 9],
                    'highlight': [4],
                    'label': 'A',
                    'caption': 'After the first partition (pivot 7 at index 4)',
                },
            ],
            'verify': '''
c = [0]
def part(A, lo, hi):
    p = A[hi]; i = lo - 1
    for j in range(lo, hi):
        c[0] += 1
        if A[j] <= p:
            i += 1; A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1
def qs(A, lo, hi):
    if lo < hi:
        m = part(A, lo, hi); qs(A, lo, m - 1); qs(A, m + 1, hi)
A = [5, 3, 8, 1, 9, 2, 7]; qs(A, 0, 6)
assert A == sorted(A) and c[0] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Hashing — quadratic probing',
            'text': 'The keys 20, 31, 42, 9, 53 are inserted in that order into an initially empty hash table of size 11 using quadratic probing: the i-th probe (i = 0, 1, 2, …) examines slot (h(k) + i²) mod 11, where h(k) = k mod 11. The slot in which key 53 is stored is',
            'options': ['4', '1', '3', '7'],
            'answer': 'C',
            'solution': '''All five keys have home slot 9 (20, 31, 42, 9, 53 are all ≡ 9 mod 11), so each new key walks further along the same quadratic sequence 9, 10, 13≡2, 18≡7, 25≡3, …

- 20 → slot 9 (i = 0)
- 31 → 9 full; i=1: 10 → slot **10**
- 42 → 9, 10 full; i=2: 9+4 = 13 ≡ **2**
- 9 → 9, 10, 2 full; i=3: 9+9 = 18 ≡ **7**
- 53 → 9, 10, 2, 7 full; i=4: 9+16 = 25 ≡ **3**

Key 53 lands in slot **3** after 5 probes.

- (A) 4 is (9 + 5²) mod 11, i.e. one probe too many.
- (B) 1 comes from mistakenly applying linear probing *after* 9, 10 wrap (9, 10, 0, 1) — with linear probing the keys would actually occupy 9, 10, 0, 1, 2.
- (D) 7 is where key 9 went.

**Note:** this is *secondary clustering*: keys with the same home slot follow the identical probe sequence.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        2: 42,
                        3: 53,
                        7: 9,
                        9: 20,
                        10: 31,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

T = [None] * 11
for k in [20, 31, 42, 9, 53]:
    i = 0
    while T[(k % 11 + i * i) % 11] is not None: i += 1
    T[(k % 11 + i * i) % 11] = k
assert T.index(53) == 3 and ANSWER == "A"
assert (9 + 25) % 11 == 1 and (9 + 36) % 11 == 1
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary search trees — build and delete',
            'text': 'The keys 41, 17, 63, 8, 29, 55, 72, 25, 34, 60, 50 are inserted in that order into an initially empty binary search tree T. Height is the number of **edges** on the longest root-to-leaf path. Which of the following statements is/are TRUE?',
            'options': [
                'T has exactly 5 leaves',
                'If 41 is deleted by replacing it with its in-order successor, the new root is 50 and 55 then has no left child',
                'The pre-order traversal of T begins 41, 17, 8, 29, 25',
                'The height of T is 3',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Build T by standard BST insertion:

- 41 root; 17 L; 63 R; 8 under 17 (L); 29 under 17 (R); 55 under 63 (L); 72 under 63 (R)
- 25 → 41 L → 17 R → 29 L; 34 → 29 R; 60 → 63 L → 55 R; 50 → 55 L

Now the statements:

- (A) leaves: 8, 25, 34, 50, 60, 72 → **6**. **False.**
- (B) in-order successor of 41 = minimum of the right subtree = 50 (63 → 55 → 50). 50 is a leaf, so it is simply moved to the root and 55's left pointer becomes empty. **True.**
- (C) pre-order (root, left, right): 41, 17, 8, 29, 25, 34, 63, 55, 50, 60, 72. **True.**
- (D) deepest nodes 25, 34, 50, 60 are at depth 3. **True.**

**Trap:** in (B), students often pick 55 or 63 as the successor; the successor is the **leftmost** node of the right subtree.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        41,
                        [
                            17,
                            [8],
                            [
                                29,
                                [25],
                                [34],
                            ],
                        ],
                        [
                            63,
                            [
                                55,
                                [50],
                                [60],
                            ],
                            [72],
                        ],
                    ],
                    'caption': 'BST T',
                },
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            17,
                            [8],
                            [
                                29,
                                [25],
                                [34],
                            ],
                        ],
                        [
                            63,
                            [
                                55,
                                None,
                                [60],
                            ],
                            [72],
                        ],
                    ],
                    'highlight': [50],
                    'caption': 'T after deleting 41 (successor 50)',
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
t = None
for k in [41, 17, 63, 8, 29, 55, 72, 25, 34, 60, 50]: t = ins(t, k)
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def lv(t): return 0 if t is None else (1 if not t[1] and not t[2] else lv(t[1]) + lv(t[2]))
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
s = t[2]
while s[1]: s = s[1]
truth = [h(t) == 3, lv(t) == 5, s[0] == 50 and s[1] is None and s[2] is None and t[2][1][1] is s,
         pre(t)[:5] == [41, 17, 8, 29, 25]]
assert sorted(ANSWER) == [c for c, x in zip("ABCD", truth) if x]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Extremal graphs — edges vs components',
            'text': 'The maximum possible number of edges in a simple undirected graph with 10 vertices and **exactly 3** connected components is',
            'options': ['27', '36', '21', '28'],
            'answer': 'D',
            'solution': '''With components of sizes n₁ + n₂ + n₃ = 10 (each ≥ 1), the best we can do is make each component complete, giving Σ C(nᵢ, 2) edges. Because C(x, 2) is convex, the sum is maximised by making the sizes as **unequal** as possible: (8, 1, 1).

- (8, 1, 1): C(8, 2) = **28**
- (7, 2, 1): 21 + 1 + 0 = 22
- (6, 2, 2): 15 + 1 + 1 = 17; (4, 3, 3): 6 + 3 + 3 = 12 (the balanced split is the *minimum*)

General formula: C(n − k + 1, 2) for n vertices and k components → C(8, 2) = 28.

- (A) 27 is one short — the large component may be complete.
- (B) 36 = C(9, 2) is the maximum for exactly **2** components.
- (C) 21 = C(7, 2) is the maximum for 4 components.

**Tip:** the same convexity argument shows that a simple graph on n vertices with more than C(n − 1, 2) edges must be connected.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

from math import comb
best = max(comb(a, 2) + comb(b, 2) + comb(10 - a - b, 2)
           for a in range(1, 9) for b in range(1, 10 - a) if 10 - a - b >= 1)
assert best == 28 and ANSWER == "A"
''',
        },
    ],
}
