# Set 29 — Weighted Shortest Paths
SET = {
    'number': 29,
    'title': 'Weighted Shortest Paths',
    'difficulty': 'GATE-level',
    'focus': 'Dijkstra with ties, negative edges, Bellman–Ford rounds, path trees',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — heapq with tuple priorities',
            'text': 'Dijkstra implementations in Python usually store `(distance, vertex)` tuples in a `heapq`. Consider the following program. What is printed?',
            'code': '''import heapq
pq = []
for item in [(4, 'D'), (2, 'B'), (4, 'A'), (2, 'C'), (1, 'E')]:
    heapq.heappush(pq, item)
print([heapq.heappop(pq)[1] for _ in range(len(pq))])''',
            'options': [
                "`['E', 'B', 'C', 'A', 'D']`",
                "`['E', 'C', 'B', 'A', 'D']`",
                "`['E', 'B', 'C', 'D', 'A']`",
                "`['D', 'A', 'B', 'C', 'E']`",
            ],
            'answer': 'A',
            'solution': '''`heapq` is a binary **min**-heap, and tuples are compared **lexicographically**: first by distance, and only on a tie by the second component (here the vertex name, compared as strings).

Sorted order of the five tuples: (1,'E') < (2,'B') < (2,'C') < (4,'A') < (4,'D').

- `range(len(pq))` is evaluated **once**, when the comprehension starts (len = 5), so exactly five pops occur even though the heap shrinks.
- Each `heappop` returns the current minimum, so the names come out as E, B, C, A, D.

Output `['E', 'B', 'C', 'A', 'D']` → option (A).

- (B) reverses the tie between B and C.
- (C) assumes ties keep insertion order (D was pushed before A) — a heap is **not** stable, and here the tuple comparison decides anyway.
- (D) treats `heapq` as a max-heap.

**Tip:** this is why ‘ties broken alphabetically’ in Dijkstra questions matches a heap of (distance, name) tuples exactly. If the second component were not comparable (e.g. a dict), a tie would raise `TypeError` — a common bug fixed by inserting a counter.''',
            'verify': 'ANSWER = {\'C\': \'A\', \'A\': \'C\'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == "[\'E\', \'B\', \'C\', \'A\', \'D\']" and ANSWER == \'C\'',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Dijkstra — undirected graph',
            'text': "Dijkstra's algorithm is run from vertex **A** on the undirected weighted graph below. The shortest-path distance from A to F is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B', 3],
                        ['A', 'C', 8],
                        ['B', 'C', 4],
                        ['B', 'D', 9],
                        ['C', 'D', 2],
                        ['C', 'E', 7],
                        ['D', 'E', 3],
                        ['D', 'F', 8],
                        ['E', 'F', 2],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 1],
                    },
                },
            ],
            'answer': '14',
            'solution': '''Extract the closest unfinished vertex each time and relax its edges.

- A (0): B = 3, C = 8.
- B (3): C = min(8, 3+4) = 7; D = 3+9 = 12.
- C (7): D = min(12, 7+2) = 9; E = 7+7 = 14.
- D (9): E = min(14, 9+3) = 12; F = 9+8 = 17.
- E (12): F = min(17, 12+2) = 14.
- F (14).

d(F) = **14** along A → B → C → D → E → F (3 + 4 + 2 + 3 + 2).

Notice that the shortest path uses **five** edges although F is only three edges from A (e.g. A–B–D–F costs 20). Every ‘direct’ edge (A–C, B–D, C–E, D–F) is beaten by a detour.

**Trap:** stopping at the first finite value seen for a vertex (D = 12, F = 17). A label becomes final only when its vertex is extracted.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B', 3],
                        ['A', 'C', 8],
                        ['B', 'C', 4],
                        ['B', 'D', 9],
                        ['C', 'D', 2],
                        ['C', 'E', 7],
                        ['D', 'E', 3],
                        ['D', 'F', 8],
                        ['E', 'F', 2],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 1],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                    ],
                    'caption': 'Shortest-path tree from A (a single path here)',
                },
            ],
            'verify': '''
import heapq
E = [("A","B",3),("A","C",8),("B","C",4),("B","D",9),("C","D",2),("C","E",7),
     ("D","E",3),("D","F",8),("E","F",2)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {"A": 0}; pq = [(0, "A")]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d.get(v, 1e9): d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert d["F"] == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Unweighted shortest paths — counting',
            'text': 'In the unweighted undirected graph below (a 3 × 3 grid from which the edge D–E has been removed), the number of distinct shortest paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['A', 'B'],
                        ['C', 'D'],
                        ['F', 'G'],
                        ['G', 'T'],
                        ['S', 'C'],
                        ['C', 'F'],
                        ['A', 'D'],
                        ['D', 'G'],
                        ['B', 'E'],
                        ['E', 'T'],
                    ],
                    'pos': {
                        'S': [0, 2],
                        'A': [1.5, 2],
                        'B': [3, 2],
                        'C': [0, 1],
                        'D': [1.5, 1],
                        'E': [3, 1],
                        'F': [0, 0],
                        'G': [1.5, 0],
                        'T': [3, 0],
                    },
                },
            ],
            'answer': '4',
            'solution': '''BFS gives levels and the number of shortest paths: paths(v) = ∑ paths(u) over neighbours u one level closer to S.

- Level 0: S (1 path).
- Level 1: A (1), C (1).
- Level 2: B (from A: 1), D (from A and C: 2), F (from C: 1).
- Level 3: E (from B only, since D–E is missing: 1), G (from D and F: 2 + 1 = 3).
- Level 4: T (from E and G: 1 + 3 = **4**).

The four paths: S-A-B-E-T, S-A-D-G-T, S-C-D-G-T, S-C-F-G-T.

In the complete 3 × 3 grid there would be C(4, 2) = 6 monotone paths; removing D–E kills exactly the two that use it (S-A-D-E-T and S-C-D-E-T).

**Trap:** counting all simple paths (there are longer ones, e.g. S-C-D-A-B-E-T) — only paths of the minimum length 4 count.''',
            'verify': '''
from collections import deque
E = [("S","A"),("A","B"),("C","D"),("F","G"),("G","T"),("S","C"),("C","F"),("A","D"),
     ("D","G"),("B","E"),("E","T")]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
dist = {"S": 0}; cnt = {"S": 1}; q = deque(["S"])
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in dist: dist[v] = dist[u] + 1; cnt[v] = 0; q.append(v)
        if dist[v] == dist[u] + 1: cnt[v] += cnt[u]
assert dist["T"] == 4 and cnt["T"] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Shortest paths — negative edges and reweighting',
            'text': "Consider single-source shortest paths in directed graphs with real edge weights. Dijkstra's algorithm here never re-extracts a vertex. Which of the following statements is/are TRUE?",
            'options': [
                'On the graph with edges S→A (2), S→B (3), B→A (−2), Dijkstra from S reports d(A) = 2 while the true distance is 1',
                'Multiplying every edge weight by the same constant c > 0 never changes which S–T path is shortest',
                'If the graph has negative edges but no negative-weight cycle, Bellman–Ford from S computes correct distances to all vertices reachable from S',
                'Adding the same constant c > 0 to every edge weight never changes which S–T path is shortest',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''- (A) **True.** Dijkstra extracts S (0), sets A = 2, B = 3, then extracts A (2) and finalises it. When B (3) is extracted, the edge B→A would give 3 − 2 = 1, but A is already final, so the reported value stays 2. Dijkstra's greedy proof needs non-negative weights.
- (B) **True.** Every path cost is multiplied by the same c > 0, which preserves the order of path costs.
- (C) **True.** After |V| − 1 rounds, Bellman–Ford has found every shortest path with at most |V| − 1 edges, and without negative cycles shortest paths are simple.
- (D) **False.** A path with k edges gains k·c, so paths with *more* edges are penalised more. E.g. S→X→T with weights 1, 1 (total 2) vs S→T with weight 3: after adding 2 the costs become 6 and 5 — the shortest path changes.

Answer: (A), (B), (C).

**Trap:** ‘just add a constant to make all weights non-negative, then run Dijkstra’ is wrong — that is exactly statement (D). (Johnson's algorithm uses vertex potentials, which shift every S–T path by the *same* amount.)''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def dijkstra_once(G, s):
    INF = float('inf'); d = {v: INF for v in G}; d[s] = 0; done = set()
    while len(done) < len(G):
        u = min((v for v in G if v not in done), key=lambda v: (d[v], v))
        done.add(u)
        for v, w in G[u]:
            if v not in done and d[u] + w < d[v]: d[v] = d[u] + w
    return d
G = {'S': [('A', 2), ('B', 3)], 'B': [('A', -2)], 'A': []}
okA = dijkstra_once(G, 'S')['A'] == 2 and min(2, 3 - 2) == 1
paths = [[1, 1], [3]]
best = lambda c, f: min(range(2), key=lambda i: sum(f(w, c) for w in paths[i]))
okB = best(2, lambda w, c: w + c) == best(0, lambda w, c: w + c)
okC = all(best(c, lambda w, c: w * c) == best(1, lambda w, c: w * c) for c in (0.5, 2, 10))
res = {'A': okA, 'B': okB, 'C': okC, 'D': True}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues and stacks — reversing a prefix',
            'text': '''A queue holds 10, 20, 30, 40, 50, 60 (front on the left). The following is done:

1. Dequeue 4 elements, pushing each onto an empty stack.
2. Pop the stack until empty, enqueuing each popped element.
3. Twice: dequeue an element and enqueue it again.

The final queue (front to rear) is''',
            'options': [
                '60, 50, 40, 30, 20, 10',
                '50, 60, 40, 30, 20, 10',
                '10, 20, 30, 40, 50, 60',
                '40, 30, 20, 10, 50, 60',
            ],
            'answer': 'D',
            'solution': '''This is the standard ‘reverse the first k elements of a queue’ routine with k = 4.

- Step 1: stack (bottom→top) = 10, 20, 30, 40; queue = 50, 60.
- Step 2: pops come out 40, 30, 20, 10 (LIFO) and are enqueued: queue = 50, 60, 40, 30, 20, 10.
- Step 3: rotate the n − k = 2 elements that were originally behind the prefix: dequeue 50 → enqueue; dequeue 60 → enqueue. Queue = **40, 30, 20, 10, 50, 60**.

Answer (D).

- (A) would need all six elements to pass through the stack.
- (B) is the state after step 2 (forgetting step 3).
- (C) would result if a queue (FIFO) had been used instead of the stack.

Cost: k pushes, k pops and n + (n − k) queue operations → Θ(n).

**Tip:** a stack reverses order; a queue preserves it. Rotations of a queue never change the cyclic order.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

from collections import deque
q = deque([10, 20, 30, 40, 50, 60]); st = []
for _ in range(4): st.append(q.popleft())
while st: q.append(st.pop())
for _ in range(2): q.append(q.popleft())
assert list(q) == [40, 30, 20, 10, 50, 60] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Bellman–Ford — rounds depend on edge order',
            'text': '''Bellman–Ford is run from S on the directed graph below. In every round the edges are relaxed in this fixed order:

C→D, B→C, A→B, S→A, S→C.

Relaxations use the current (most recently updated) distances. Initially d(S) = 0 and all other distances are ∞. The number of the **last** round in which some distance changes is ______.''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 4],
                        ['A', 'B', -2],
                        ['B', 'C', 3],
                        ['C', 'D', 1],
                        ['S', 'C', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [3, 2],
                        'C': [3, 0],
                        'D': [4.5, 0],
                    },
                },
            ],
            'answer': '4',
            'solution': '''Bellman–Ford's guarantee is that after round i every shortest path with ≤ i edges is found; how *fast* it converges in practice depends on the edge order. Here the order is the reverse of the path S→A→B→C→D, the worst case.

- Round 1: C→D, B→C, A→B skipped (tails at ∞); S→A: A = 4; S→C: C = 9.
- Round 2: C→D: D = 10; B→C skipped (B = ∞); A→B: B = 2.
- Round 3: B→C: C = min(9, 2+3) = 5 (C→D was already processed this round).
- Round 4: C→D: D = min(10, 5+1) = 6.
- Round 5: no change → converged.

Final: A 4, B 2, C 5, D 6. The last change happens in round **4** = |V| − 1, the maximum possible.

With the order S→A, A→B, B→C, C→D, S→C, everything would be final after round 1.

**Trap:** thinking the negative edge A→B forces extra rounds — what matters is how many edges the shortest path has and whether they are relaxed in path order.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Distances at the end of each round',
                    'row_labels': ['init', 'round 1', 'round 2', 'round 3', 'round 4'],
                    'col_labels': ['S', 'A', 'B', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞'],
                        [0, 4, '∞', 9, '∞'],
                        [0, 4, 2, 9, 10],
                        [0, 4, 2, 5, 10],
                        [0, 4, 2, 5, 6],
                    ],
                    'highlight': [
                        [3, 3],
                        [4, 4],
                    ],
                },
            ],
            'verify': '''
E = [("C","D",1),("B","C",3),("A","B",-2),("S","A",4),("S","C",9)]
INF = float('inf'); d = {v: INF for v in "SABCD"}; d["S"] = 0; last = 0
for r in range(1, 10):
    ch = False
    for u, v, w in E:
        if d[u] + w < d[v]: d[v] = d[u] + w; ch = True
    if ch: last = r
assert last == int(ANSWER) and [d[v] for v in "ABCD"] == [4, 2, 5, 6]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — double hashing',
            'text': '''A hash table has 13 slots (0–12). Keys are inserted with double hashing: the i-th probe (i = 0, 1, 2, …) for key k examines slot (h₁(k) + i · h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11).

The keys 27, 40, 53, 14, 66, 92, 48 are inserted in this order into an empty table. In which slot is 48 stored?''',
            'options': ['10', '0', '3', '6'],
            'answer': 'C',
            'solution': '''Double hashing uses a key-dependent step h₂(k), so keys with the same home slot follow different probe sequences (no secondary clustering).

- 27: h₁ = 1 → slot **1**.
- 40: h₁ = 1 (taken), h₂ = 1 + 7 = 8 → 9 → slot **9**.
- 53: h₁ = 1, h₂ = 1 + 9 = 10 → 11 → slot **11**.
- 14: h₁ = 1, h₂ = 1 + 3 = 4 → 5 → slot **5**.
- 66: h₁ = 1, h₂ = 1 + 0 = 1 → 2 → slot **2**.
- 92: h₁ = 1, h₂ = 1 + 4 = 5 → 6 → slot **6**.
- 48: h₁ = 48 mod 13 = 9 (taken by 40); h₂ = 1 + (48 mod 11) = 5. Probes: 9, 14 mod 13 = 1 (27), 19 mod 13 = 6 (92), 24 mod 13 = 11 (53), 29 mod 13 = **3** → empty.

48 is stored in slot **3** after 5 probes → option (C).

- (A) 10 is what linear probing (step 1) would give from slot 9.
- (B) 0 comes from forgetting the ‘1 +’ in h₂ (step 4): 9 → 13 mod 13 = 0.
- (D) 6 overlooks that 92 already occupies slot 6.

**Tip:** since 13 is prime, every step 1 … 12 visits all slots, so double hashing always finds an empty slot when one exists.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        1: 27,
                        2: 66,
                        3: 48,
                        5: 14,
                        6: 92,
                        9: 40,
                        11: 53,
                    },
                    'caption': 'Final table (48 lands in slot 3)',
                },
            ],
            'verify': '''ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)

T = [None] * 13
for k in [27, 40, 53, 14, 66, 92, 48]:
    i = 0
    while T[(k % 13 + i * (1 + k % 11)) % 13] is not None: i += 1
    T[(k % 13 + i * (1 + k % 11)) % 13] = k
opts = {'A': 10, 'B': 0, 'C': 6, 'D': 3}
assert T.index(48) == opts[ANSWER] == 3
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — reconstruction from traversals',
            'text': '''A binary tree with distinct labels has

pre-order:  G C A B E D F K I H L
in-order:   A B C D E F G H I K L

Its post-order traversal is''',
            'options': [
                'B A D F E C I H L K G',
                'B A D F E C H I L K G',
                'A B D F E C H I L K G',
                'B A D E F C H I L K G',
            ],
            'answer': 'B',
            'solution': '''The first pre-order symbol is the root; its position in the in-order sequence splits the left and right subtrees. Recurse.

- Root G; in-order left = A B C D E F, right = H I K L.
- Left subtree: pre-order C A B E D F → root C; left {A, B}, right {D, E, F}.
  - {A, B}: pre-order A B → root A, B is its **right** child (B follows A in-order).
  - {D, E, F}: pre-order E D F → root E with children D and F.

- Right subtree: pre-order K I H L → root K; left {H, I}, right {L}.
  - {H, I}: pre-order I H → root I, H its **left** child.

Post-order (left, right, root): B A | D F E | C | H I | L | K | G → **B A D F E C H I L K G** → option (B).

- (A) swaps H and I (treats H as I's parent).
- (C) puts A before B (treats B as A's parent).
- (D) visits E before F (in-order inside E's subtree).

**Tip:** pre-order + in-order (or post-order + in-order) determine a binary tree uniquely; pre-order + post-order alone do not when a node has a single child (A and I here).''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'G',
                        [
                            'C',
                            [
                                'A',
                                None,
                                ['B'],
                            ],
                            [
                                'E',
                                ['D'],
                                ['F'],
                            ],
                        ],
                        [
                            'K',
                            [
                                'I',
                                ['H'],
                                None,
                            ],
                            ['L'],
                        ],
                    ],
                    'caption': 'Reconstructed tree',
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

def build(pre, ino):
    if not pre: return None
    r = pre[0]; k = ino.index(r)
    return [r, build(pre[1:k+1], ino[:k]), build(pre[k+1:], ino[k+1:])]
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
t = build("GCABEDFKIHL", "ABCDEFGHIKL")
opts = {'A': "BADFECIHLKG", 'B': "ABDFECHILKG", 'C': "BADFECHILKG", 'D': "BADEFCHILKG"}
assert [k for k in opts if opts[k] == "".join(post(t))] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Elementary sorts — swaps and passes',
            'text': 'The array [5, 2, 8, 1, 9, 3] is sorted into increasing order. Bubble sort compares adjacent elements left to right in each pass; selection sort swaps A[i] with the minimum of A[i..n−1] **only if** they are different positions; insertion sort shifts larger elements one place right. Which of the following statements is/are TRUE?',
            'options': [
                'After the first pass of bubble sort the array is [2, 5, 1, 8, 3, 9]',
                'Insertion sort performs exactly 7 element shifts',
                'Selection sort performs exactly 4 swaps',
                'Bubble sort performs exactly 7 swaps',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Bubble-sort swaps and insertion-sort shifts each remove exactly **one inversion**, so both equal the inversion count.

Inversions of [5, 2, 8, 1, 9, 3]: (5,2), (5,1), (5,3), (2,1), (8,1), (8,3), (9,3) → **7**.

- (A) **True** — pass 1: (5,2) swap → 2 5 8 1 9 3; (5,8) ok; (8,1) swap → 2 5 1 8 9 3; (8,9) ok; (9,3) swap → 2 5 1 8 3 9. The largest element bubbles to the end.
- (B) **True** — 7 shifts (one per inversion).
- (C) **False** — selection sort: i=0 min 1 at index 3 → swap → [1, 2, 8, 5, 9, 3]; i=1 min 2 already in place; i=2 min 3 at index 5 → swap → [1, 2, 3, 5, 9, 8]; i=3 5 in place; i=4 min 8 at index 5 → swap → [1, 2, 3, 5, 8, 9]. Only **3** swaps.
- (D) **True** — 7 swaps.

**Trap:** selection sort's swap count is at most n − 1 and is *not* related to inversions; it is the number of elements not in place minus the number of cycles in the permutation.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

a = [5, 2, 8, 1, 9, 3]
inv = sum(1 for i in range(6) for j in range(i + 1, 6) if a[i] > a[j])
b = a[:]; bs = 0; p1 = None
for i in range(6):
    for j in range(5 - i):
        if b[j] > b[j + 1]: b[j], b[j + 1] = b[j + 1], b[j]; bs += 1
    if i == 0: p1 = b[:]
c = a[:]; ss = 0
for i in range(6):
    m = min(range(i, 6), key=lambda k: c[k])
    if m != i: c[i], c[m] = c[m], c[i]; ss += 1
d = a[:]; sh = 0
for i in range(1, 6):
    x = d[i]; j = i - 1
    while j >= 0 and d[j] > x: d[j + 1] = d[j]; j -= 1; sh += 1
    d[j + 1] = x
res = {'A': bs == 7, 'B': ss == 4, 'C': sh == 7, 'D': p1 == [2, 5, 1, 8, 3, 9]}
assert inv == 7 and sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — aliasing in adjacency lists',
            'text': 'A programmer builds adjacency lists as follows. What is printed?',
            'code': '''G = dict.fromkeys("ABC", [])
G["A"].append("B")
G["B"] = G["B"] + ["C"]
G["C"] += ["A"]
print(G)''',
            'options': [
                "`{'A': ['B'], 'B': ['C'], 'C': ['A']}`",
                "`{'A': ['B', 'C', 'A'], 'B': ['B', 'C', 'A'], 'C': ['B', 'C', 'A']}`",
                "`{'A': ['B', 'A'], 'B': ['B', 'C'], 'C': ['B', 'A']}`",
                "`{'A': ['B'], 'B': ['B', 'C'], 'C': ['B', 'A']}`",
            ],
            'answer': 'C',
            'solution': '''`dict.fromkeys(keys, value)` stores the **same** object as the value of every key. Call the shared list L.

- `G["A"].append("B")` mutates L → L = ['B'], seen through A, B and C.
- `G["B"] = G["B"] + ["C"]`: `+` builds a **new** list ['B', 'C'] and rebinds only key B. L is unchanged.
- `G["C"] += ["A"]`: for lists `+=` is in-place `extend`, so L itself becomes ['B', 'A']; then G['C'] is re-assigned to the same L.

A and C still share L = ['B', 'A']; B has its own ['B', 'C']. Output → option (C).

- (A) assumes each key got its own empty list.
- (B) assumes `+` also mutates in place.
- (D) forgets that A aliases the list extended through C.

**Fix:** `G = {v: [] for v in "ABC"}` creates a fresh list per key (or use `collections.defaultdict(list)`).

**Trap:** `x = x + y` and `x += y` are *not* equivalent for mutable sequences.''',
            'verify': 'ANSWER = {\'B\': \'C\', \'C\': \'B\'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == "{\'A\': [\'B\', \'A\'], \'B\': [\'B\', \'C\'], \'C\': [\'B\', \'A\']}" and ANSWER == \'B\'',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Dijkstra — shortest-path tree with ties',
            'text': "Dijkstra's algorithm is run from S on the directed graph below. A tentative distance d[v] (and the parent of v) is changed **only on a strict improvement**, and when several vertices have the same smallest tentative distance the alphabetically smallest is extracted first. Which set of edges forms the resulting shortest-path tree?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 3],
                        ['A', 'C', 4],
                        ['B', 'C', 1],
                        ['B', 'D', 3],
                        ['C', 'D', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2],
                        'D': [3, 0],
                    },
                },
            ],
            'options': [
                '{S→A, A→B, B→C, C→D}',
                '{S→A, A→B, A→C, C→D}',
                '{S→A, S→B, A→C, C→D}',
                '{S→A, S→B, A→C, B→D}',
            ],
            'answer': 'D',
            'solution': '''Every vertex here has **two** shortest paths, so the tree is decided purely by the update rule and the extraction order.

- Extract S (0): A = 2 (parent S), B = 5 (parent S).
- Extract A (2): B via A = 2 + 3 = 5 — **not** < 5, so B keeps parent S. C = 2 + 4 = 6 (parent A).
- Extract B (5): C via B = 5 + 1 = 6 — not < 6, keeps parent A. D = 5 + 3 = 8 (parent B).
- Extract C (6): D via C = 6 + 2 = 8 — not < 8, keeps parent B.
- Extract D (8).

Tree: {S→A, S→B, A→C, B→D} → option (D). Distances: A 2, B 5, C 6, D 8.

- (A) is the tree produced by a **≤** rule, where every later equal-cost offer overwrites the parent: B←A, then C←B, then D←C.
- (B) mixes both mistakes.
- (C) assumes D is first reached from C — but B is extracted before C.

**Tip:** with ties, ‘the’ shortest-path tree is not unique; the exam must specify the update rule. With strict ‘<’ the parent is the **first** vertex extracted that offers the optimal distance.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 3],
                        ['A', 'C', 4],
                        ['B', 'C', 1],
                        ['B', 'D', 3],
                        ['C', 'D', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2],
                        'D': [3, 0],
                    },
                    'highlight_edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                    ],
                    'caption': 'Shortest-path tree (strict-improvement rule)',
                },
            ],
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

E = [("S","A",2),("S","B",5),("A","B",3),("A","C",4),("B","C",1),("B","D",3),("C","D",2)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
INF = float('inf'); d = {v: INF for v in "SABCD"}; d["S"] = 0; par = {}; done = set()
while len(done) < 5:
    u = min((v for v in d if v not in done), key=lambda v: (d[v], v)); done.add(u)
    for v, w in G.get(u, []):
        if d[u] + w < d[v]: d[v] = d[u] + w; par[v] = u
tree = {par[v] + "→" + v for v in par}
opts = {'A': "S→A, A→B, B→C, C→D", 'B': "S→A, S→B, A→C, B→D",
        'C': "S→A, S→B, A→C, C→D", 'D': "S→A, A→B, A→C, C→D"}
assert [k for k in opts if set(opts[k].split(", ")) == tree] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Bellman–Ford — round-by-round trace',
            'text': '''Bellman–Ford is run from S on the directed graph below. In every round the edges are relaxed in the order

C→D, B→D, B→C, A→C, A→B, S→B, S→A, D→A

using the current distance values. Initially d(S) = 0 and all others are ∞. Which of the following statements is/are TRUE?''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 5],
                        ['S', 'B', 8],
                        ['A', 'B', -4],
                        ['A', 'C', 7],
                        ['B', 'C', 3],
                        ['B', 'D', 6],
                        ['C', 'D', -2],
                        ['D', 'A', 4],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.5],
                        'B': [1.5, -0.5],
                        'C': [4.5, 1],
                        'D': [2.7, 1],
                    },
                },
            ],
            'options': [
                'After round 1, d(B) = 8',
                'The final value of d(D) is 2',
                'The algorithm reports a negative-weight cycle',
                'After round 2, d(D) = 7',
            ],
            'answer': ['A', 'B'],
            'solution': '''Trace (only changes are listed):

- **Round 1:** C→D, B→D, B→C, A→C, A→B skipped (tails at ∞); S→B: B = 8; S→A: A = 5; D→A skipped. End: A 5, B 8, C ∞, D ∞.
- **Round 2:** C→D skipped; B→D: D = 14; B→C: C = 11; A→C: 12 > 11; A→B: B = 5 − 4 = 1. End: A 5, B 1, C 11, D 14.
- **Round 3:** C→D: D = 9; B→D: D = 1 + 6 = 7; B→C: C = 1 + 3 = 4. End: A 5, B 1, C 4, D 7.
- **Round 4:** C→D: D = 4 − 2 = 2. End: A 5, B 1, C 4, D 2.
- **Check round:** D→A gives 2 + 4 = 6 > 5; nothing improves → no negative cycle.

Verdicts:

- (A) **True** — B is first set to 8 in round 1 (the improvement A→B comes later in the order than S→A, so it must wait for round 2).
- (B) **True** — shortest path S→A→B→C→D = 5 − 4 + 3 − 2 = 2.
- (C) **False** — the only cycles A→B→C→D→A (+1), A→C→D→A (+9) and A→B→D→A (+6) are all positive.
- (D) **False** — d(D) = 14 after round 2; 7 appears only in round 3.

**Trap:** relaxing in a ‘natural’ order (S's edges first) would converge in one or two rounds. The given order relaxes S's edges *last*, so the improvement travels only one edge of S→A→B→C→D per round — always trace with the order stated.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Distances at the end of each round',
                    'row_labels': ['init', 'round 1', 'round 2', 'round 3', 'round 4'],
                    'col_labels': ['S', 'A', 'B', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞'],
                        [0, 5, 8, '∞', '∞'],
                        [0, 5, 1, 11, 14],
                        [0, 5, 1, 4, 7],
                        [0, 5, 1, 4, 2],
                    ],
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = [("C","D",-2),("B","D",6),("B","C",3),("A","C",7),("A","B",-4),("S","B",8),("S","A",5),("D","A",4)]
INF = float('inf'); d = {v: INF for v in "SABCD"}; d["S"] = 0; snap = {}
for r in range(1, 5):
    for u, v, w in E:
        if d[u] + w < d[v]: d[v] = d[u] + w
    snap[r] = dict(d)
neg = any(d[u] + w < d[v] for u, v, w in E)
res = {'A': snap[1]['B'] == 8, 'B': snap[2]['D'] == 7, 'C': d['D'] == 2, 'D': neg}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra on a negative edge — error analysis',
            'text': 'The textbook Dijkstra algorithm is run from S on the directed graph below, which has one negative edge. Once a vertex is extracted its distance is final and is **never** changed again; among equal tentative distances the alphabetically smaller vertex is extracted first. Let r(v) be the distance reported by Dijkstra and δ(v) the true shortest distance. The value of ∑ (r(v) − δ(v)) over v ∈ {A, B, C, T} is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['B', 'A', -4],
                        ['A', 'C', 3],
                        ['C', 'T', 1],
                        ['B', 'T', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2],
                        'T': [4.5, 1],
                    },
                },
            ],
            'answer': '3',
            'solution': '''**Dijkstra's run:**

- Extract S (0): A = 2, B = 5.
- Extract A (2): C = 2 + 3 = 5.
- Tie B = C = 5 → extract B (alphabetical): B→A would give 1, but A is already final → ignored. T = 5 + 9 = 14.
- Extract C (5): T = min(14, 5 + 1) = 6.
- Extract T (6).

Reported: r(A) = 2, r(B) = 5, r(C) = 5, r(T) = 6.

**True distances** (the graph has no cycle, so just take the best path):

- δ(B) = 5; δ(A) = min(2, 5 − 4) = 1 (S→B→A);
- δ(C) = 1 + 3 = 4; δ(T) = min(4 + 1, 5 + 9) = 5.

Differences: A 1, B 0, C 1, T 1 → sum = **3**.

The single wrong label at A propagates to every vertex whose shortest path passes through A — Dijkstra never revisits A's out-edges after the improvement.

**Trap:** fixing only A (sum 1). Even an implementation that *did* lower d(A) to 1 when relaxing B→A would leave C and T wrong, because A's edges are not relaxed again.''',
            'verify': '''
E = [("S","A",2),("S","B",5),("B","A",-4),("A","C",3),("C","T",1),("B","T",9)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
INF = float('inf'); r = {v: INF for v in "SABCT"}; r["S"] = 0; done = set()
while len(done) < 5:
    u = min((v for v in r if v not in done), key=lambda v: (r[v], v)); done.add(u)
    for v, w in G.get(u, []):
        if v not in done and r[u] + w < r[v]: r[v] = r[u] + w
t = {v: INF for v in "SABCT"}; t["S"] = 0
for _ in range(4):
    for u, v, w in E:
        if t[u] + w < t[v]: t[v] = t[u] + w
assert sum(r[v] - t[v] for v in "ABCT") == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — a subtly wrong Dijkstra',
            'text': 'The following program tries to compute shortest-path distances, but marks a vertex as `seen` when it is **first pushed** instead of when it is popped. What is printed?',
            'code': '''import heapq
G = {'S': [('A', 1), ('B', 4)], 'A': [('B', 2), ('C', 6)],
     'B': [('C', 1)], 'C': []}

def sp(src):
    dist = {src: 0}
    pq = [(0, src)]
    seen = {src}
    while pq:
        d, u = heapq.heappop(pq)
        for v, w in G[u]:
            if v not in seen:
                seen.add(v)
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return dist

print(sp('S'))''',
            'options': [
                "`{'S': 0, 'A': 1, 'B': 3, 'C': 4}`",
                "`{'S': 0, 'A': 1, 'B': 4, 'C': 7}`",
                "`{'S': 0, 'A': 1, 'B': 4, 'C': 5}`",
                "`{'S': 0, 'A': 1, 'B': 3, 'C': 7}`",
            ],
            'answer': 'B',
            'solution': '''Because a vertex is frozen the first time it is *discovered*, each vertex keeps the distance of its **first discovery**, never improved — the code behaves like BFS-order labelling with weights, not like Dijkstra.

- Pop (0, S): A unseen → dist A = 1; B unseen → dist B = 4. Both pushed.
- Pop (1, A): B already seen → the better value 1 + 2 = 3 is **ignored**; C unseen → dist C = 1 + 6 = 7.
- Pop (4, B): C already seen → 4 + 1 = 5 ignored.
- Pop (7, C): no edges.

Output: `{'S': 0, 'A': 1, 'B': 4, 'C': 7}` → option (B). Dicts print in insertion order (S, A, B, C).

- (A) is the **correct** answer of real Dijkstra (S→A→B→C = 1 + 2 + 1 = 4).
- (C) assumes C is improved from B but B itself is not.
- (D) assumes B is fixed but C is not.

**Fix:** test `if d + w < dist.get(v, inf)` when relaxing, and skip stale heap entries on pop (`if d > dist[u]: continue`) — finalise on *pop*, not on push.''',
            'verify': 'assert OUTPUT.strip() == "{\'S\': 0, \'A\': 1, \'B\': 4, \'C\': 7}" and ANSWER == \'B\'',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Counting shortest paths in a weighted graph',
            'text': 'In the weighted directed graph below, the number of distinct shortest paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 3],
                        ['S', 'C', 4],
                        ['A', 'D', 3],
                        ['B', 'D', 2],
                        ['B', 'E', 4],
                        ['C', 'E', 3],
                        ['D', 'F', 3],
                        ['E', 'F', 1],
                        ['F', 'T', 2],
                        ['D', 'T', 5],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 1],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 1],
                        'T': [6, 1.6],
                    },
                },
            ],
            'answer': '6',
            'solution': '''Run Dijkstra and keep, for each vertex, the number of shortest paths: when a relaxation gives a strictly smaller distance, *replace* the count by the predecessor's count; when it gives an equal distance, *add* the predecessor's count.

- S: d 0, count 1.
- A: d 2 (1). B: d 3 (1). C: d 4 (1).
- D: via A 2 + 3 = 5, via B 3 + 2 = 5 → d 5, count 1 + 1 = **2**.
- E: via B 3 + 4 = 7, via C 4 + 3 = 7 → d 7, count **2**.
- F: via D 5 + 3 = 8, via E 7 + 1 = 8 → d 8, count 2 + 2 = **4**.
- T: via F 8 + 2 = 10, via D 5 + 5 = 10 → d 10, count 4 + 2 = **6**.

The six paths: S-A-D-F-T, S-B-D-F-T, S-B-E-F-T, S-C-E-F-T, S-A-D-T, S-B-D-T (all cost 10).

**Trap:** forgetting the direct edge D→T (answer 4) or counting B→D→F and B→E→F as one because both start with S→B. Paths are different if their edge sequences differ.''',
            'verify': '''
E = [("S","A",2),("S","B",3),("S","C",4),("A","D",3),("B","D",2),("B","E",4),("C","E",3),
     ("D","F",3),("E","F",1),("F","T",2),("D","T",5)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
paths = []
def dfs(u, c, p):
    if u == "T": paths.append((c, p)); return
    for v, w in G.get(u, []): dfs(v, c + w, p + v)
dfs("S", 0, "S")
best = min(c for c, _ in paths)
assert best == 10 and sum(1 for c, _ in paths if c == best) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths vs MST; transforming weights',
            'text': 'Consider the undirected weighted graph below. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 1],
                        ['A', 'B', 1],
                        ['B', 'T', 1],
                        ['S', 'T', 4],
                        ['S', 'C', 3],
                        ['A', 'C', 3],
                        ['B', 'C', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.6],
                        'B': [3, 2.6],
                        'T': [4.5, 1],
                        'C': [2.25, 1.7],
                    },
                },
            ],
            'options': [
                'If every edge weight is increased by 1, the shortest S–T path changes',
                'The shortest-path tree from S is a minimum spanning tree of the graph',
                'If every edge weight is squared, the shortest S–T path does not change',
                'If every edge weight is doubled, the shortest S–T path changes',
            ],
            'answer': ['A', 'C'],
            'solution': '''Original shortest S–T path: S–A–B–T with cost 1 + 1 + 1 = **3** (S–T costs 4, S–C–B–T costs 3 + 2 + 1 = 6).

- (A) **True.** +1 per edge: S–A–B–T (3 edges) → 6, S–T (1 edge) → 5, S–C–B–T → 9. The single-edge path now wins — adding a constant favours paths with fewer edges.
- (B) **False.** Distances from S: A 1, B 2, T 3, C 3 (S–C directly; S–A–C and S–A–B–C both cost 4). Shortest-path tree = {S–A, A–B, B–T, S–C}, weight 1 + 1 + 1 + 3 = 6. Kruskal picks S–A, A–B, B–T (1 each), then B–C (2) → MST weight **5**. The SPT is not an MST: it pays 3 for S–C because it optimises distance *from S*, not total weight.
- (C) **True.** Squared weights: S–A–B–T = 1 + 1 + 1 = 3, S–T = 16, S–C–B–T = 9 + 4 + 1 = 14, S–A–C–… larger → S–A–B–T remains shortest. (Squaring is not order-preserving in general — it penalises heavy edges — but here it does not change the winner.)
- (D) **False.** Doubling scales every path cost by 2 → order unchanged (6 vs 8 vs 12).

Answer: (A), (C).

**Trap:** believing the SPT and MST coincide; they share the edges incident to S only in special cases.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 1],
                        ['A', 'B', 1],
                        ['B', 'T', 1],
                        ['S', 'T', 4],
                        ['S', 'C', 3],
                        ['A', 'C', 3],
                        ['B', 'C', 2],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.6],
                        'B': [3, 2.6],
                        'T': [4.5, 1],
                        'C': [2.25, 1.7],
                    },
                    'highlight_edges': [
                        ['S', 'A'],
                        ['A', 'B'],
                        ['B', 'T'],
                        ['S', 'C'],
                    ],
                    'caption': 'Shortest-path tree from S (weight 6); MST uses B–C instead',
                },
            ],
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import heapq, itertools
E = [("S","A",1),("A","B",1),("B","T",1),("S","T",4),("S","C",3),("A","C",3),("B","C",2)]
def sp(f):
    G = {}
    for u, v, w in E:
        G.setdefault(u, []).append((v, f(w))); G.setdefault(v, []).append((u, f(w)))
    d = {"S": 0}; par = {}; pq = [(0, "S")]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]: continue
        for v, w in G[u]:
            if du + w < d.get(v, 1e9): d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
    p, x = ["T"], "T"
    while x != "S": x = par[x]; p.append(x)
    return p, par
base, par = sp(lambda w: w)
spt_w = sum(w for u, v, w in E if par.get(v) == u or par.get(u) == v)
best = 1e9
for comb in itertools.combinations(E, 4):
    comp = {v: v for v in "SABCT"}
    def f(x):
        while comp[x] != x: x = comp[x]
        return x
    ok = True
    for u, v, w in comb:
        a, b = f(u), f(v)
        if a == b: ok = False; break
        comp[a] = b
    if ok: best = min(best, sum(w for _, _, w in comb))
res = {'A': sp(lambda w: w + 1)[0] != base, 'B': spt_w == best,
       'C': sp(lambda w: 2 * w)[0] != base, 'D': sp(lambda w: w * w)[0] == base}
assert spt_w == 6 and best == 5
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Bellman–Ford — synchronous rounds = hop-bounded paths',
            'text': '''A *synchronous* Bellman–Ford is run from S on the directed graph below: in round k every vertex computes

d_k(v) = min( d_{k−1}(v),  min over edges u→v of d_{k−1}(u) + w(u, v) )

using **only the values of the previous round**; d_0(S) = 0 and d_0(v) = ∞ otherwise. The value of d_3(T) is ______.''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 1],
                        ['S', 'B', 6],
                        ['A', 'B', 2],
                        ['A', 'C', 7],
                        ['B', 'C', 1],
                        ['C', 'T', 1],
                        ['B', 'T', 5],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2],
                        'T': [4.5, 1],
                    },
                },
            ],
            'answer': '8',
            'solution': '''With synchronous updates, d_k(v) is exactly the length of the shortest S→v walk using **at most k edges** — so the answer is the best S→T path with ≤ 3 edges.

- k = 1: A 1, B 6.
- k = 2: B = min(6, 1 + 2) = 3; C = min(1 + 7, 6 + 1) = 7; T = 6 + 5 = 11.
- k = 3: C = min(7, 3 + 1, 1 + 7) = 4; T = min(11, d_2(B) + 5 = 8, d_2(C) + 1 = 8) = **8**.
- (k = 4: T = min(8, 4 + 1) = 5 — the true distance, via the 4-edge path S→A→B→C→T.)

Check by enumeration of paths with ≤ 3 edges: S-B-T 11, S-A-B-T 8, S-B-C-T 8, S-A-C-T 9 → minimum 8.

**Trap:** using freshly updated values within a round (in-place Bellman–Ford). With a favourable edge order that version could already reach 5 in round 1 or 2; the synchronous version cannot ‘skip ahead’.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'd_k(v) for synchronous rounds',
                    'row_labels': ['k = 0', 'k = 1', 'k = 2', 'k = 3', 'k = 4'],
                    'col_labels': ['S', 'A', 'B', 'C', 'T'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞'],
                        [0, 1, 6, '∞', '∞'],
                        [0, 1, 3, 7, 11],
                        [0, 1, 3, 4, 8],
                        [0, 1, 3, 4, 5],
                    ],
                    'highlight': [
                        [3, 4],
                    ],
                },
            ],
            'verify': '''
E = [("S","A",1),("S","B",6),("A","B",2),("A","C",7),("B","C",1),("C","T",1),("B","T",5)]
INF = float('inf'); d = {v: INF for v in "SABCT"}; d["S"] = 0
for k in range(3):
    nd = dict(d)
    for u, v, w in E: nd[v] = min(nd[v], d[u] + w)
    d = nd
assert d["T"] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Heaps — decrease-key (as used by Dijkstra)',
            'text': "Dijkstra's priority queue is the binary min-heap below (array, root at index 0). The key at index 8 (value 13) is **decreased to 3** and the heap property is restored by sifting it up. The resulting array is",
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [2, 7, 4, 11, 9, 6, 5, 15, 13, 10],
                    'caption': 'Min-heap before decrease-key',
                },
            ],
            'options': [
                '[2, 3, 4, 7, 9, 6, 5, 15, 11, 10]',
                '[2, 3, 4, 11, 9, 6, 5, 15, 7, 10]',
                '[3, 2, 4, 7, 9, 6, 5, 15, 11, 10]',
                '[2, 7, 4, 3, 9, 6, 5, 15, 11, 10]',
            ],
            'answer': 'A',
            'solution': '''Decrease-key lowers a key, which can only violate heap order with its **ancestors**, so the key moves up: swap with the parent ((i − 1) // 2) while it is smaller.

- Index 8 now holds 3; parent index 3 holds 11 → 3 < 11 → swap. Array: [2, 7, 4, 3, 9, 6, 5, 15, 11, 10].
- Index 3 holds 3; parent index 1 holds 7 → swap. Array: [2, 3, 4, 7, 9, 6, 5, 15, 11, 10].
- Index 1 holds 3; parent index 0 holds 2 → 3 > 2 → stop.

Result **[2, 3, 4, 7, 9, 6, 5, 15, 11, 10]** → option (A). Two swaps — O(log n) in general, which is why each relaxation in a binary-heap Dijkstra costs O(log V).

- (B) moves 7 to index 8, which is not a child of index 1 (children of 1 are 3 and 4); the elements on the path must shift down one level each.
- (C) swaps past the root although 2 < 3.
- (D) stops after the first swap.

**Tip:** the path traversed is 8 → 3 → 1 → 0; only elements on this path can move.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [2, 3, 4, 7, 9, 6, 5, 15, 11, 10],
                    'highlight': [3, 7, 11],
                    'caption': 'After decrease-key (path 8 → 3 → 1)',
                },
            ],
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

h = [2, 7, 4, 11, 9, 6, 5, 15, 13, 10]; i = 8; h[i] = 3
while i > 0 and h[(i - 1) // 2] > h[i]:
    p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p
opts = {'A': [2, 7, 4, 3, 9, 6, 5, 15, 11, 10], 'B': [2, 3, 4, 11, 9, 6, 5, 15, 7, 10],
        'C': [3, 2, 4, 7, 9, 6, 5, 15, 11, 10], 'D': [2, 3, 4, 7, 9, 6, 5, 15, 11, 10]}
assert [k for k in opts if opts[k] == h] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Linked lists — merging sorted lists (merge sort step)',
            'text': 'The two sorted singly linked lists L₁ and L₂ shown are merged into one sorted list by the standard merge (repeatedly compare the two front nodes, unlink the smaller one and append it to the result; when one list becomes empty, attach the rest of the other without comparisons). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 8, 15, 21],
                    'head': 'L₁',
                },
                {
                    'type': 'linkedlist',
                    'values': [5, 6, 17, 30, 42],
                    'head': 'L₂',
                },
            ],
            'options': [
                'Merging **any** two sorted lists of lengths 4 and 5 needs at most 8 key comparisons',
                'Merging **any** two sorted lists of lengths 4 and 5 needs at least 5 key comparisons',
                'Merging L₁ and L₂ performs exactly 7 key comparisons',
                'The 5th node of the merged list holds 8',
            ],
            'answer': ['A', 'C'],
            'solution': '''Each comparison outputs exactly one node, and comparisons stop when one list empties. So #comparisons = (m + n) − (number of nodes left in the other list at that moment).

Trace:

- 3 vs 5 → 3; 8 vs 5 → 5; 8 vs 6 → 6; 8 vs 17 → 8; 15 vs 17 → 15; 21 vs 17 → 17; 21 vs 30 → 21. L₁ is now empty → attach 30 → 42.
- Merged: 3, 5, 6, 8, 15, 17, 21, 30, 42.
- (A) **True** — the maximum is m + n − 1 = 8 (when the two lists interleave until the last element).
- (B) **False** — the minimum is min(m, n) = 4, e.g. L₁ = 1, 2, 3, 4 and L₂ = 5, …, 9: four comparisons empty L₁.
- (C) **True** — 7 comparisons (9 nodes − 2 left over).
- (D) **False** — the 5th node is 15 (8 is the 4th).

Merging linked lists needs only O(1) extra space (just pointer relinking), which is why merge sort is the method of choice for sorting linked lists: Θ(n log n) time with middle-finding by slow/fast pointers.

**Trap:** assuming every merge costs m + n − 1 comparisons.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 5, 6, 8, 15, 17, 21, 30, 42],
                    'head': 'head',
                    'caption': 'Merged list',
                },
            ],
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def merge(a, b):
    i = j = c = 0; out = []
    while i < len(a) and j < len(b):
        c += 1
        if a[i] <= b[j]: out.append(a[i]); i += 1
        else: out.append(b[j]); j += 1
    return out + a[i:] + b[j:], c
m, c = merge([3, 8, 15, 21], [5, 6, 17, 30, 42])
cs = []
for pos in itertools.combinations(range(9), 4):
    a = list(pos); b = [x for x in range(9) if x not in pos]
    cs.append(merge(a, b)[1])
res = {'A': c == 7, 'B': m[4] == 8, 'C': min(cs) >= 5, 'D': max(cs) <= 8}
assert min(cs) == 4 and max(cs) == 8
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — parametric edge weight',
            'text': 'In the undirected graph below, the edge S–B has an unknown positive integer weight w; all other weights are as shown. The **largest** value of w for which the shortest S–T path is unique and uses the edge S–B is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 4],
                        ['A', 'B', 1],
                        ['A', 'T', 6],
                        ['S', 'B', 'w'],
                        ['B', 'T', 3],
                        ['S', 'C', 2],
                        ['C', 'B', 4],
                        ['C', 'T', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.2],
                        'B': [3, 1],
                        'C': [1.5, -0.2],
                        'T': [4.5, 1],
                    },
                },
            ],
            'answer': '4',
            'solution': '''Find the best S–T path that **avoids** S–B; the path through S–B must beat it strictly.

Paths avoiding S–B:

- S–A–B–T = 4 + 1 + 3 = **8** (best)
- S–C–B–T = 2 + 4 + 3 = 9
- S–A–T = 4 + 6 = 10
- S–C–T = 2 + 9 = 11

Paths using S–B: the best is clearly S–B–T = w + 3 (S–B–A–T = w + 7 and S–B–C–T = w + 13 are longer).

Unique shortest path through S–B ⇔ w + 3 < 8 ⇔ w < 5 ⇔ w ≤ **4** (w integer).

At w = 5 the paths S–B–T and S–A–B–T tie at 8 (not unique); for w ≥ 6 the shortest path avoids S–B.

**Trap:** comparing only with the obvious two-edge alternatives S–A–T (10) or S–C–T (11), which would give w ≤ 6. The cheap edge A–B creates the real competitor S–A–B–T. (Running Dijkstra from S with w left symbolic gives the same conclusion: d(B) = min(w, 5, 6).)''',
            'verify': '''
import heapq
def sp_count(w):
    E = [("S","A",4),("A","B",1),("A","T",6),("S","B",w),("B","T",3),("S","C",2),("C","B",4),("C","T",9)]
    G = {}
    for u, v, x in E: G.setdefault(u, []).append((v, x)); G.setdefault(v, []).append((u, x))
    best = [10**9, []]
    def dfs(u, c, p):
        if u == "T":
            if c < best[0]: best[0] = c; best[1] = [p]
            elif c == best[0]: best[1].append(p)
            return
        for v, x in G[u]:
            if v not in p: dfs(v, c + x, p + [v])
    dfs("S", 0, ["S"])
    return best[1]
ok = [w for w in range(1, 20)
      if len(sp_count(w)) == 1 and sp_count(w)[0][:2] == ["S", "B"]]
assert max(ok) == int(ANSWER)
''',
        },
    ],
}
