# Set 06 — Binary Search Trees (Moderate)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.

_BST_HELPERS = '''
class _N:
    def __init__(s, k): s.k, s.l, s.r = k, None, None
def _ins(t, k):
    if t is None: return _N(k)
    if k < t.k: t.l = _ins(t.l, k)
    else: t.r = _ins(t.r, k)
    return t
def _build(keys):
    r = None
    for k in keys: r = _ins(r, k)
    return r
def _ht(t): return -1 if t is None else 1 + max(_ht(t.l), _ht(t.r))
def _pre(t): return [] if t is None else [t.k] + _pre(t.l) + _pre(t.r)
def _ino(t): return [] if t is None else _ino(t.l) + [t.k] + _ino(t.r)
'''

SET = {
    'number': 6,
    'title': 'Binary Search Trees',
    'difficulty': 'Moderate',
    'focus': 'BST insert/delete/search, valid sequences, min/max, successor',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing with negative steps',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "PREORDER"
print(s[-2:0:-3], s[::-2], s[5:2:-1])''',
            'options': ['`EO RDOR DRO`', '`EOP RDOR DRO`', '`EO REDR ORD`', '`ER RDOR DROE`'],
            'answer': 'A',
            'solution': '''A slice `s[start:stop:step]` with a negative step walks **leftwards** from `start` and stops *before* reaching `stop`; omitted ends default to the far ends of the string.

Index the string: P0 R1 E2 O3 R4 D5 E6 R7.

- `s[-2:0:-3]`: start at index 6 (`E`), then 3 (`O`); the next index 0 equals `stop`, which is excluded → `EO`.
- `s[::-2]`: start at the last index 7 → 7, 5, 3, 1 → `R D O R` → `RDOR`.
- `s[5:2:-1]`: indices 5, 4, 3 → `D R O` → `DRO`.

Output: `EO RDOR DRO`.

- (A) Correct.
- (B) Includes index 0 (`P`), but `stop` is always excluded.
- (C) `REDR` would come from starting at index 7 with step −2 but reading wrong letters; `ORD` reverses the third slice incorrectly.
- (D) Treats −3 as reaching index 4 and includes the stop index in the third slice.

**Trap:** with negative steps the *stop* bound is still exclusive, and `s[::-k]` starts at the last character, not the first.''',
            'verify': '''
assert OUTPUT.split() == ['EO', 'RDOR', 'DRO']
assert ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'BST insertion — height',
            'text': 'The keys 52, 38, 71, 45, 60, 83, 41, 47, 43, 90, 65 are inserted in the given order into an initially empty binary search tree (no balancing). The height of the resulting tree, measured as the number of **edges** on the longest root-to-leaf path, is ______.',
            'answer': '4',
            'solution': '''Each key is inserted by walking from the root (left if smaller, right if larger) and attached at the first empty position.

- 52 is the root; 38 → left of 52; 71 → right of 52.
- 45 → 52 L → 38 R; 60 → 71 L; 83 → 71 R.
- 41 → 38 R → 45 L; 47 → 45 R.
- 43 → 52 L → 38 R → 45 L → 41 R (depth 4).
- 90 → 71 R → 83 R; 65 → 71 L → 60 R.

The deepest node is 43 on the path 52 → 38 → 45 → 41 → 43, which has **4 edges**. The right subtree only reaches depth 3 (52 → 71 → 83 → 90).

**Trap:** counting nodes instead of edges gives 5. Also note 41 is placed under 45 (not under 38's left) because 41 > 38.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        52,
                        [
                            38,
                            None,
                            [
                                45,
                                [
                                    41,
                                    None,
                                    [43],
                                ],
                                [47],
                            ],
                        ],
                        [
                            71,
                            [
                                60,
                                None,
                                [65],
                            ],
                            [
                                83,
                                None,
                                [90],
                            ],
                        ],
                    ],
                    'highlight': [52, 38, 45, 41, 43],
                    'caption': 'Resulting BST; the longest path is highlighted',
                },
            ],
            'verify': '''
class _N:
    def __init__(s, k): s.k, s.l, s.r = k, None, None
def _ins(t, k):
    if t is None: return _N(k)
    if k < t.k: t.l = _ins(t.l, k)
    else: t.r = _ins(t.r, k)
    return t
def _build(keys):
    r = None
    for k in keys: r = _ins(r, k)
    return r
def _ht(t): return -1 if t is None else 1 + max(_ht(t.l), _ht(t.r))
def _pre(t): return [] if t is None else [t.k] + _pre(t.l) + _pre(t.r)
def _ino(t): return [] if t is None else _ino(t.l) + [t.k] + _ino(t.r)

t = _build([52, 38, 71, 45, 60, 83, 41, 47, 43, 90, 65])
assert _ht(t) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BST search paths',
            'text': 'A binary search tree stores distinct integers from 1 to 100. A search for the key **55** examines nodes in the order listed. Which of the following sequences **cannot** be the sequence of nodes examined?',
            'options': [
                '10, 90, 20, 80, 30, 70, 55',
                '91, 12, 85, 30, 61, 40, 55',
                '70, 20, 60, 30, 65, 55',
                '5, 99, 50, 75, 60, 52, 55',
            ],
            'answer': 'C',
            'solution': '''While searching for 55, every node visited narrows an open interval (low, high) that must contain 55; each later node on the path must lie strictly inside the current interval.

- (A) 10 → (10, ∞); 90 → (10, 90); 20 → (20, 90); 80 → (20, 80); 30 → (30, 80); 70 → (30, 70); 55 inside. **Valid.**
- (B) 91 → (−∞, 91); 12 → (12, 91); 85 → (12, 85); 30 → (30, 85); 61 → (30, 61); 40 → (40, 61); 55 inside. **Valid.**
- (C) 70 → (−∞, 70); 20 → (20, 70); 60 → (20, 60); 30 → (30, 60); now **65** is not in (30, 60) — after going left at 60 every later key must be < 60. **Invalid.**
- (D) 5 → (5, ∞); 99 → (5, 99); 50 → (50, 99); 75 → (50, 75); 60 → (50, 60); 52 → (52, 60); 55 inside. **Valid.**

**Tip:** check each element only against the tightest bounds so far — a zig-zag path is perfectly fine as long as the interval keeps shrinking around the target.''',
            'verify': '''
def ok(seq, x):
    lo, hi = float('-inf'), float('inf')
    for v in seq[:-1]:
        if not (lo < v < hi): return False
        if x < v: hi = v
        else: lo = v
    return seq[-1] == x and lo < x < hi
opts = [[10,90,20,80,30,70,55],[91,12,85,30,61,40,55],
        [70,20,60,30,65,55],[5,99,50,75,60,52,55]]
bad = [L for L, s in zip('ABCD', opts) if not ok(s, 55)]
assert bad == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — permutations',
            'text': 'The integers 1, 2, 3, 4, 5 are pushed onto an initially empty stack **in this order**; pops may be interleaved with pushes at any time, and every popped value is printed. Which of the following output sequences is/are possible?',
            'options': ['2 4 1 3 5', '3 2 5 4 1', '4 5 3 2 1', '1 5 4 2 3'],
            'answer': ['B', 'C'],
            'solution': '''Simulate greedily: to output x, push everything up to x (if not yet pushed) and pop; if x is already pushed it must be on **top**, otherwise the sequence is impossible.

- (A) push 1,2 pop 2; push 3,4 pop 4; stack is [1, 3] with 3 on top but 1 is needed. **Impossible.**
- (B) push 1,2,3 pop 3; pop 2; push 4,5 pop 5; pop 4; pop 1. **Possible.**
- (C) push 1..4 pop 4; push 5 pop 5; pop 3, 2, 1. **Possible.**
- (D) push 1 pop 1; push 2..5 pop 5; pop 4; stack is [2, 3], top is 3 but 2 is needed. **Impossible.**

**Tip:** a sequence is impossible exactly when it contains a pattern a … b … c with c < a < b (the '3-1-2' pattern), e.g. 4 … 1 … 3 in (A) and 5 … 2 … 3 in (D).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [1, 3],
                    'label': '(B) after printing 2, 4',
                    'caption': 'In (B) 1 is buried under 3, so it cannot be printed next',
                },
            ],
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def possible(out):
    st, nxt = [], 1
    for x in out:
        while nxt <= x:
            st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = ["3 2 5 4 1", "2 4 1 3 5", "1 5 4 2 3", "4 5 3 2 1"]
good = [L for L, s in zip('ABCD', opts) if possible(list(map(int, s.split())))]
assert good == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'The keys 27, 14, 50, 36, 23, 41, 61, 19, 72, 8 are inserted in this order into a hash table with 9 slots (indices 0–8) using h(k) = k mod 9 and separate chaining; each new key is inserted at the **head** of its chain. Assuming every stored key is equally likely to be searched for, the average number of key comparisons in a successful search is ______ (rounded off to two decimal places).',
            'answer': ['1.89', '1.91'],
            'solution': '''In a successful search the number of comparisons equals the position of the key in its chain. For a chain of length L the positions are 1, 2, …, L whatever the insertion order, so the chain contributes L(L+1)/2 in total.

Hash values: 27→0, 14→5, 50→5, 36→0, 23→5, 41→5, 61→7, 19→1, 72→0, 8→8.

- Slot 0: 72 → 36 → 27 (length 3, total 6)
- Slot 1: 19 (1)
- Slot 5: 41 → 23 → 50 → 14 (length 4, total 10)
- Slot 7: 61 (1); Slot 8: 8 (1)

Total = 6 + 1 + 10 + 1 + 1 = 19 comparisons over 10 keys → **1.90**.

**Trap:** head-insertion changes *which* key is at which position (e.g. 14 now needs 4 comparisons) but not the multiset of positions, so the average is unaffected.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 9,
                    'slots': {
                        0: [72, 36, 27],
                        1: [19],
                        5: [41, 23, 50, 14],
                        7: [61],
                        8: [8],
                    },
                    'caption': 'Final table (chains listed head first)',
                },
            ],
            'verify': '''
T = [[] for _ in range(9)]
for k in [27, 14, 50, 36, 23, 41, 61, 19, 72, 8]:
    T[k % 9].insert(0, k)
tot = sum(ch.index(k) + 1 for ch in T for k in ch)
avg = tot / 10
assert float(ANSWER[0]) <= round(avg, 2) <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BST — in-order successor and predecessor',
            'text': 'For the binary search tree shown below, let x be the in-order **successor** of 37 and y the in-order **predecessor** of 47. The pair (x, y) is',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            25,
                            [
                                12,
                                None,
                                [18],
                            ],
                            [
                                33,
                                [29],
                                [37],
                            ],
                        ],
                        [
                            61,
                            [
                                52,
                                [47],
                                None,
                            ],
                            [78],
                        ],
                    ],
                    'caption': 'Figure: BST',
                },
            ],
            'options': ['(33, 40)', '(40, 40)', '(40, 52)', '(29, 61)'],
            'answer': 'B',
            'solution': '''If a node has **no right child**, its successor is the lowest ancestor whose *left* subtree contains the node. Symmetrically, if a node has **no left child**, its predecessor is the lowest ancestor whose *right* subtree contains the node.

- 37 is a leaf. Its path from the root is 40 (go L) → 25 (go R) → 33 (go R) → 37. The last ancestor where we turned **left** is 40, so x = 40.
- 47 is a leaf. Path: 40 (go R) → 61 (go L) → 52 (go L) → 47. The last ancestor where we turned **right** is 40, so y = 40.

Check with the in-order sequence 12, 18, 25, 29, 33, 37, **40**, 47, 52, 61, 78: the key after 37 is 40 and the key before 47 is 40.

- (A) 33 is 37's parent, but it is smaller than 37.
- (C) 52 is 47's parent, but it is larger than 47.
- (D) 29 and 61 are unrelated neighbours in the drawing.

**Trap:** the parent is the successor/predecessor only when the node is a left/right child respectively.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

class _N:
    def __init__(s, k): s.k, s.l, s.r = k, None, None
def _ins(t, k):
    if t is None: return _N(k)
    if k < t.k: t.l = _ins(t.l, k)
    else: t.r = _ins(t.r, k)
    return t
def _build(keys):
    r = None
    for k in keys: r = _ins(r, k)
    return r
def _ht(t): return -1 if t is None else 1 + max(_ht(t.l), _ht(t.r))
def _pre(t): return [] if t is None else [t.k] + _pre(t.l) + _pre(t.r)
def _ino(t): return [] if t is None else _ino(t.l) + [t.k] + _ino(t.r)

t = _build([40, 25, 61, 12, 33, 52, 78, 18, 29, 37, 47])
s = _ino(t)
x, y = s[s.index(37) + 1], s[s.index(47) - 1]
assert (x, y) == (40, 40) and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Insertion sort — number of shifts',
            'text': 'Insertion sort (ascending) is applied to the array [7, 3, 9, 1, 6, 2, 8]. A *shift* is one execution of `A[j+1] = A[j]` that moves a larger element one place to the right. The total number of shifts performed is ______.',
            'answer': '11',
            'solution': '''Each shift fixes exactly one **inversion** (a pair i < j with A[i] > A[j]), so the number of shifts equals the number of inversions.

Count, for every element, how many earlier elements are larger:

- 7: 0; 3: 1 (7); 9: 0; 1: 3 (7, 3, 9); 6: 2 (7, 9); 2: 4 (7, 3, 9, 6); 8: 1 (9).

Total = 0 + 1 + 0 + 3 + 2 + 4 + 1 = **11**.

Pass by pass the array becomes [3,7,9,1,6,2,8] → [3,7,9,…] → [1,3,7,9,6,2,8] → [1,3,6,7,9,2,8] → [1,2,3,6,7,9,8] → [1,2,3,6,7,8,9].

**Trap:** do not count comparisons — they exceed shifts by one for every pass that stops because it found a smaller element.''',
            'verify': '''
A = [7, 3, 9, 1, 6, 2, 8]; sh = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0 and A[j] > key:
        A[j + 1] = A[j]; j -= 1; sh += 1
    A[j + 1] = key
assert sh == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — list aliasing and shallow copies',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = [[0] * 2] * 3
b = [row[:] for row in a]
a[0][1] = 5
b[1][0] = 7
c = a + b
c[0][0] += 1
print(sum(map(sum, c)))''',
            'options': ['`13`', '`40`', '`23`', '`25`'],
            'answer': 'D',
            'solution': '''`[[0] * 2] * 3` creates **one** inner list referenced three times. `row[:]` makes genuine copies, and `a + b` creates a new outer list whose elements are the *same* row objects.

- After line 2: `b` has three independent rows `[0, 0]`.
- `a[0][1] = 5` changes the shared row → every row of `a` is `[0, 5]`.
- `b[1][0] = 7` → `b = [[0,0],[7,0],[0,0]]`.
- `c[0]` is the shared row of `a`; `c[0][0] += 1` → that row is `[1, 5]`.

Sum: rows from `a` contribute 3 × 6 = 18, rows from `b` contribute 7 → **25**.

- (A) 13 assumes the rows of `a` were independent (6 + 0 + 0 + 7).
- (B) 40 assumes `b` was copied *after* the `5` was written (18 + 22).
- (C) 23 assumes `a + b` copies the rows, so the `+= 1` changes only one row (16 + 7).

**Trap:** list concatenation copies references, not the inner lists.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '25' and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph traversal — BFS and DFS',
            'text': 'Consider the undirected graph below. BFS and DFS are started from **A**; whenever there is a choice, neighbours are visited in alphabetical order. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2.5],
                        'E': [3, 1],
                        'F': [3, -0.5],
                        'G': [4.5, 1],
                    },
                },
            ],
            'options': [
                'The BFS visit order is A, B, C, D, E, F, G',
                'DFS visits F before E',
                'Edge E–G is an edge of the BFS tree',
                'The BFS level (distance from A) of G is 3',
            ],
            'answer': ['A', 'D'],
            'solution': '''BFS explores level by level with a FIFO queue; DFS goes as deep as possible (recursively) before backtracking.

**BFS:** queue A → dequeue A, enqueue B, C → dequeue B, enqueue D, E → dequeue C, enqueue F (E already seen) → dequeue D, enqueue G (via D) → E, F, G. Order A, B, C, D, E, F, G; levels A0, B1, C1, D2, E2, F2, G3.

**DFS:** A → B → D → G → E (G's smallest unvisited neighbour) → back to E: C → F. Order A, B, D, G, E, C, F.

- (A) **True.**
- (B) **False** — DFS reaches E (from G) before F.
- (C) **False** — G is discovered from D, so the tree edge is D–G; E–G is a non-tree edge.
- (D) **True** — G is first reached via D at level 3.

**Trap:** in BFS a vertex's parent is the *first* vertex that discovers it, not every neighbour one level up.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2.5],
                        'E': [3, 1],
                        'F': [3, -0.5],
                        'G': [4.5, 1],
                    },
                    'caption': 'BFS tree edges highlighted',
                },
            ],
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from collections import deque
E = [("A","B"),("A","C"),("B","D"),("B","E"),("C","E"),("C","F"),("D","G"),("E","G"),("F","G")]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
for k in G: G[k].sort()
dist, par, order, q = {"A": 0}, {}, [], deque("A")
while q:
    u = q.popleft(); order.append(u)
    for v in G[u]:
        if v not in dist: dist[v] = dist[u] + 1; par[v] = u; q.append(v)
dfs = []
def go(u):
    dfs.append(u)
    for v in G[u]:
        if v not in dfs: go(v)
go("A")
truth = {'A': order == list("ABCDEFG"), 'B': dist["G"] == 3,
         'C': par["G"] == "E", 'D': dfs.index("F") < dfs.index("E")}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — counting probes',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''def bs(A, x):
    lo, hi, c = 0, len(A) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if A[mid] == x:
            return c
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return c

A = list(range(3, 60, 4))
print(bs(A, 39) + bs(A, 42))''',
            'answer': '7',
            'solution': '''`A = [3, 7, 11, …, 59]` has 15 elements (indices 0–14), `A[i] = 3 + 4i`. The counter `c` counts loop iterations (probes).

**Search 39** (index 9):
- lo=0, hi=14, mid=7, A[7]=31 < 39 → lo=8 (c=1)
- mid=11, A[11]=47 > 39 → hi=10 (c=2)
- mid=9, A[9]=39 → found, returns **3**.

**Search 42** (absent):
- mid=7 (31) → lo=8; mid=11 (47) → hi=10; mid=9 (39) → lo=10; mid=10 (43) → hi=9 → loop ends. c = **4**.

Printed value 3 + 4 = **7**.

**Tip:** with 15 = 2⁴ − 1 elements every unsuccessful search makes exactly 4 probes, while a successful one takes 1–4 depending on depth in the implicit decision tree.''',
            'verify': '''
assert int(OUTPUT.strip()) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BST deletion — successor replacement',
            'text': 'The BST shown below is modified by deleting the keys **50**, **30** and **20**, in that order. A node with two children is deleted by copying its in-order **successor** into it and then deleting the successor; a node with one child is replaced by that child. The pre-order traversal of the final tree is',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            30,
                            [
                                20,
                                None,
                                [25],
                            ],
                            [
                                40,
                                [35],
                                None,
                            ],
                        ],
                        [
                            70,
                            [
                                60,
                                None,
                                [65],
                            ],
                            [
                                85,
                                [80],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Figure: initial BST',
                },
            ],
            'options': [
                '40, 25, 35, 70, 60, 65, 85, 80',
                '60, 35, 25, 40, 70, 65, 85, 80',
                '60, 40, 25, 35, 70, 65, 85, 80',
                '60, 35, 25, 40, 70, 85, 80',
            ],
            'answer': 'B',
            'solution': '''The in-order successor of a node with two children is the **minimum of its right subtree** (go right once, then left as far as possible). That successor has no left child, so removing it is a 0- or 1-child deletion.

**Delete 50** (two children): right subtree 70 → left 60 → no left child, so successor = 60. Copy 60 into the root and delete the old 60, which has one child 65 → 65 becomes 70's left child.

**Delete 30** (two children): right subtree 40 → left 35 → successor = 35 (a leaf). Copy 35 into 30's node, remove the leaf; 40 now has no children.

**Delete 20** (one child, 25): 25 takes its place as left child of 35.

Final tree: root 60; left 35 (children 25, 40); right 70 (children 65, 85), 85 has left 80.
Pre-order: **60, 35, 25, 40, 70, 65, 85, 80**.

- (A) Result of using the in-order *predecessor* (40 replaces 50, 25 replaces 30 …).
- (B) Correct.
- (C) Takes 40 (30's right child) as the successor of 30 instead of the leftmost node 35.
- (D) Loses 65 — forgetting to re-attach the successor's right child.

**Trap:** the successor need not be a leaf — it may have a right child that must be spliced into the successor's old position.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        60,
                        [
                            35,
                            [25],
                            [40],
                        ],
                        [
                            70,
                            [65],
                            [
                                85,
                                [80],
                                None,
                            ],
                        ],
                    ],
                    'highlight': [60, 35, 25],
                    'caption': 'Final BST (changed positions highlighted)',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def dele(t, k):
    if t is None: return None
    if k < t[0]: t[1] = dele(t[1], k); return t
    if k > t[0]: t[2] = dele(t[2], k); return t
    if t[1] is None: return t[2]
    if t[2] is None: return t[1]
    m = t[2]
    while m[1]: m = m[1]
    t[0] = m[0]; t[2] = dele(t[2], m[0]); return t
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
t = None
for k in [50, 30, 70, 20, 40, 60, 85, 25, 35, 65, 80]: t = ins(t, k)
for k in [50, 30, 20]: t = dele(t, k)
opts = {'A': [60,35,25,40,70,65,85,80], 'B': [40,25,35,70,60,65,85,80],
        'C': [60,40,25,35,70,65,85,80], 'D': [60,35,25,40,70,85,80]}
assert [L for L in opts if opts[L] == pre(t)] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BST — counting insertion orders',
            'text': 'The eight keys of the BST shown below are inserted one by one, in some order, into an initially empty BST. The number of insertion orders (permutations of the eight keys) that produce **exactly** this tree is ______.',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            20,
                            [10],
                            [30],
                        ],
                        [
                            60,
                            [50],
                            [
                                70,
                                None,
                                [80],
                            ],
                        ],
                    ],
                    'caption': 'Figure: target BST',
                },
            ],
            'answer': '210',
            'solution': '''An insertion order produces the tree iff the root comes first and, recursively, the keys of each subtree appear in a valid order for that subtree; the left and right subtree sequences may be **interleaved arbitrarily**. Hence
f(T) = C(n_L + n_R, n_L) · f(L) · f(R).

- Subtree 20 (keys 10, 30): 20 first, then 10 and 30 in any order → f = C(2,1) = 2.
- Subtree 70 → 80: a chain, only one order → f = 1.
- Subtree 60 (left {50}, right {70, 80}): f = C(3,1) · 1 · 1 = 3.
- Root 40 (left 3 keys, right 4 keys): f = C(7,3) · 2 · 3 = 35 · 6 = **210**.

Out of 8! = 40320 permutations, only 210 build this particular shape.

**Trap:** multiplying only f(L)·f(R) = 6 forgets that insertions into the two subtrees can be interleaved; the binomial factor C(7,3) accounts for that.''',
            'verify': '''
from itertools import permutations
def ins(t, k):
    if t is None: return (k, None, None)
    if k < t[0]: return (t[0], ins(t[1], k), t[2])
    return (t[0], t[1], ins(t[2], k))
def build(seq):
    t = None
    for k in seq: t = ins(t, k)
    return t
target = build([40, 20, 60, 10, 30, 50, 70, 80])
keys = [10, 20, 30, 50, 60, 70, 80]
cnt = sum(1 for p in permutations(keys) if build((40,) + p) == target)
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST — valid pre-order sequences',
            'text': 'Which of the following sequences is/are valid **pre-order** traversals of some binary search tree with distinct keys?',
            'options': [
                '30, 20, 25, 10, 40, 50',
                '15, 10, 12, 11, 20, 18, 25, 17',
                '50, 30, 20, 40, 70, 60, 55, 65, 80',
                '30, 20, 10, 25, 40, 35, 50',
            ],
            'answer': ['C', 'D'],
            'solution': '''In a BST pre-order, once we move into the right subtree of a node v (i.e. see a key larger than v after v's left part), **no later key may be smaller than v**. A stack-based check keeps a running lower bound: when a key larger than the stack top arrives, pop and raise the bound to the popped key.

- (A) 30, 20, then 25 > 20 means we are in 20's right subtree (bound 20). Then 10 < 20 violates the bound. **Invalid.**
- (B) 15 → left 10 → right 12 → left 11; then 20 (bound 15), 18 left of 20, 25 right of 20 (bound now 20); then 17 < 20 would have to lie in 20's right subtree — impossible. **Invalid.**
- (C) 50 → left 30 (children 20, 40); right 70 → left 60 (children 55, 65), right 80. **Valid.**
- (D) 30 → left {20, 10, 25} = 20 with children 10, 25; right {40, 35, 50} = 40 with children 35, 50. **Valid.**

**Tip:** a sequence is a valid BST pre-order iff it avoids the pattern 'a, …, c, …, b' with b < a < c — exactly what the stack check detects.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            30,
                            [20],
                            [40],
                        ],
                        [
                            70,
                            [
                                60,
                                [55],
                                [65],
                            ],
                            [80],
                        ],
                    ],
                    'caption': 'The unique BST with pre-order (C)',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def valid(seq):
    st, low = [], float('-inf')
    for x in seq:
        if x < low: return False
        while st and st[-1] < x: low = st.pop()
        st.append(x)
    return True
opts = [[30,20,10,25,40,35,50],[30,20,25,10,40,50],
        [50,30,20,40,70,60,55,65,80],[15,10,12,11,20,18,25,17]]
good = [L for L, s in zip('ABCD', opts) if valid(s)]
assert good == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python BST — range query with pruning',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class N:
    def __init__(s, k):
        s.k, s.l, s.r = k, None, None

def ins(t, k):
    if t is None:
        return N(k)
    if k < t.k: t.l = ins(t.l, k)
    else:       t.r = ins(t.r, k)
    return t

calls = 0
def f(t, lo, hi):
    global calls
    calls += 1
    if t is None: return 0
    if t.k < lo: return f(t.r, lo, hi)
    if t.k > hi: return f(t.l, lo, hi)
    return t.k + f(t.l, lo, hi) + f(t.r, lo, hi)

root = None
for k in [45, 22, 67, 15, 31, 58, 80, 27, 36, 62]:
    root = ins(root, k)
print(f(root, 27, 62), calls)''',
            'options': ['`259 15`', '`259 10`', '`232 15`', '`259 21`'],
            'answer': 'A',
            'solution': '''`f` returns the sum of keys in [lo, hi] but **prunes**: if a key is below `lo` only the right subtree is explored, if above `hi` only the left. `calls` counts every invocation, including calls on `None`.

Tree: 45 (L 22, R 67); 22 (L 15, R 31); 31 (L 27, R 36); 67 (L 58, R 80); 58 (R 62).

Trace (✓ = key in range, added to the sum):
- f(45) ✓ → f(22), f(67)
- f(22): 22 < 27 → only f(31) ✓ → f(27) ✓ [f(None), f(None)], f(36) ✓ [f(None), f(None)]
- f(67): 67 > 62 → only f(58) ✓ → f(None), f(62) ✓ [f(None), f(None)]

Calls on real nodes: 45, 22, 31, 27, 36, 67, 58, 62 = 8; calls on `None`: 2 + 2 + 1 + 2 = 7. Total **15**. Nodes 15 and 80 are never visited.
Sum = 45 + 31 + 27 + 36 + 58 + 62 = **259**.

- (B) 10 counts each node once, ignoring pruning and `None` calls.
- (C) 232 omits 27 (treating the range as exclusive).
- (D) 21 would be the count with no pruning (10 nodes + 11 `None` calls).

**Trap:** `calls += 1` runs *before* the `None` check, so empty subtrees are counted too.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            22,
                            [15],
                            [
                                31,
                                [27],
                                [36],
                            ],
                        ],
                        [
                            67,
                            [
                                58,
                                None,
                                [62],
                            ],
                            [80],
                        ],
                    ],
                    'highlight': [45, 31, 27, 36, 58, 62],
                    'caption': 'Keys in [27, 62] highlighted; 15 and 80 are pruned',
                },
            ],
            'verify': '''
assert OUTPUT.split() == ['259', '15'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — closures and late binding',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''fs = []
for i in range(4):
    fs.append(lambda x, i=i: x * i if i % 2 else x + i)

gs = [lambda x: x * i for i in range(4)]

print(sum(f(3) for f in fs) + sum(g(3) for g in gs))''',
            'answer': '56',
            'solution': '''A default argument (`i=i`) is evaluated when the lambda is **created**, freezing the current value. A plain free variable is looked up when the lambda is **called** (late binding).

**fs** (frozen i = 0, 1, 2, 3; the body is `x*i` if i is odd else `x+i`):
- i=0: 3 + 0 = 3
- i=1: 3 × 1 = 3
- i=2: 3 + 2 = 5
- i=3: 3 × 3 = 9
Sum = 20.

**gs**: all four lambdas share the comprehension's variable `i`, whose final value is 3, so each returns 3 × 3 = 9 → sum 36.

Output 20 + 36 = **56**.

**Trap:** reading `gs` as 0 + 3 + 6 + 9 = 18 (giving 38) ignores late binding. Also note the conditional expression groups as `(x*i) if (i%2) else (x+i)`; misreading it as `x * (i if i%2 else x+i)` gives a different `fs` sum.''',
            'verify': '''
assert int(OUTPUT.strip()) == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition swaps',
            'text': 'Quicksort with the Lomuto partition below is used to sort [6, 11, 3, 9, 2, 8, 5] by calling `quicksort(A, 0, 6)`, where `quicksort(A, lo, hi)` does nothing if lo ≥ hi and otherwise calls `partition` and recurses on both sides of the returned index. Counting **every** execution of a swap statement (including swaps of an element with itself), the total number of swaps is ______.',
            'code': '''def partition(A, lo, hi):
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1
            A[i], A[j] = A[j], A[i]      # swap 1
    A[i + 1], A[hi] = A[hi], A[i + 1]    # swap 2
    return i + 1''',
            'answer': '7',
            'solution': '''Lomuto partition executes swap 1 once for every element ≤ pivot and swap 2 exactly once per call. So swaps per call = (number of elements ≤ pivot, excluding the pivot) + 1.

- partition(0, 6), pivot 5: elements ≤ 5 are 3 and 2 → 2 + 1 = 3 swaps. Array → [3, 2, **5**, 9, 11, 8, 6], pivot index 2.
- partition(0, 1) on [3, 2], pivot 2: none ≤ 2 → 1 swap → [2, 3].
- partition(3, 6) on [9, 11, 8, 6], pivot 6: none → 1 swap → [6, 11, 8, 9], pivot index 3.
- partition(4, 6) on [11, 8, 9], pivot 9: only 8 → 1 + 1 = 2 swaps → [8, 9, 11].
- Remaining ranges have size ≤ 1: no calls to partition.

Total = 3 + 1 + 1 + 2 = **7**.

**Trap:** forgetting the final pivot swap in calls where nothing is ≤ pivot (it still executes), or mis-tracking the array after the first partition — the right part becomes [9, 11, 8, 6], not the original order of those keys.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each partition call (pivot position highlighted)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', 'swaps'],
                    'row_labels': ['start', 'P(0,6)', 'P(0,1)', 'P(3,6)', 'P(4,6)'],
                    'rows': [
                        [6, 11, 3, 9, 2, 8, 5, '-'],
                        [3, 2, 5, 9, 11, 8, 6, 3],
                        [2, 3, 5, 9, 11, 8, 6, 1],
                        [2, 3, 5, 6, 11, 8, 9, 1],
                        [2, 3, 5, 6, 8, 9, 11, 2],
                    ],
                    'highlight': [
                        [1, 2],
                        [2, 0],
                        [3, 3],
                        [4, 5],
                    ],
                },
            ],
            'verify': '''
sw = 0
def part(A, lo, hi):
    global sw
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1; A[i], A[j] = A[j], A[i]; sw += 1
    A[i + 1], A[hi] = A[hi], A[i + 1]; sw += 1
    return i + 1
def qs(A, lo, hi):
    if lo < hi:
        m = part(A, lo, hi); qs(A, lo, m - 1); qs(A, m + 1, hi)
A = [6, 11, 3, 9, 2, 8, 5]; qs(A, 0, 6)
assert A == sorted(A) and sw == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array [12, 7, 25, 3, 18, 30, 9, 21, 5] (0-indexed) is converted into a **max-heap** using the bottom-up build-heap procedure (sift-down applied at indices 3, 2, 1, 0 in that order; at each step the larger child is chosen). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [12, 7, 25, 3, 18, 30, 9, 21, 5],
                    'show_index': True,
                    'caption': 'Initial array viewed as a complete binary tree',
                },
            ],
            'options': [
                'After build-heap, 3 and 5 are the children of 7',
                'After build-heap, key 12 is at index 5',
                'After build-heap, index 2 holds 25',
                'Exactly 4 swaps are performed in total',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Bottom-up build-heap sifts down every internal node from the last one (index ⌊n/2⌋ − 1 = 3) back to the root; a sifted key may sink several levels.

- i = 3 (key 3, children 21, 5): swap with 21 → [12, 7, 25, 21, 18, 30, 9, 3, 5]. (1 swap)
- i = 2 (key 25, children 30, 9): swap with 30 → [12, 7, 30, 21, 18, 25, 9, 3, 5]. (1 swap)
- i = 1 (key 7, children 21, 18): swap with 21 → index 3 now 7 with children 3, 5 → stop. [12, 21, 30, 7, 18, 25, 9, 3, 5]. (1 swap)
- i = 0 (key 12, children 21, 30): swap with 30 → at index 2, children 25, 9 → swap with 25 → index 5 is a leaf. [30, 21, 25, 7, 18, 12, 9, 3, 5]. (2 swaps)

Final heap: [30, 21, 25, 7, 18, 12, 9, 3, 5]; total swaps = 5.

- (A) index 3 = 7, its children (indices 7, 8) are 3 and 5. **True.**
- (B) 12 sank two levels to index 5. **True.**
- (C) index 2 = 25. **True.**
- (D) 5 swaps, not 4. **False** — the root's key sinks twice.

**Trap:** stopping the root's sift-down after one swap; a sift-down continues until the key is ≥ both children.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [30, 21, 25, 7, 18, 12, 9, 3, 5],
                    'highlight': [5],
                    'show_index': True,
                    'caption': 'Max-heap after build-heap (index 5 = key 12 highlighted)',
                },
            ],
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

H = [12, 7, 25, 3, 18, 30, 9, 21, 5]; sw = 0
def sift(i, n):
    global sw
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and H[l] > H[m]: m = l
        if r < n and H[r] > H[m]: m = r
        if m == i: return
        H[i], H[m] = H[m], H[i]; sw += 1; i = m
for i in range(3, -1, -1): sift(i, 9)
truth = {'A': H[2] == 25, 'B': H.index(12) == 5,
         'C': H[3] == 7 and sorted(H[7:9]) == [3, 5], 'D': sw == 4}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source **S** on the weighted directed graph shown below. The sum of the final shortest-path distances from S to all six vertices (including S itself) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['B', 'A', 3],
                        ['B', 'C', 8],
                        ['A', 'C', 2],
                        ['A', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'T', 9],
                        ['D', 'T', 3],
                        ['B', 'D', 11],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, 1],
                        'D': [5.5, -0.2],
                        'T': [6.5, 2.2],
                    },
                },
            ],
            'answer': '33',
            'solution': '''Dijkstra repeatedly extracts the unfinished vertex with the smallest tentative distance and relaxes its outgoing edges (valid because all weights are non-negative).

- Extract S (0): A = 7, B = 2.
- Extract B (2): A = min(7, 5) = 5; C = 10; D = 13.
- Extract A (5): C = min(10, 7) = 7; D = min(13, 11) = 11.
- Extract C (7): D = min(11, 8) = 8; T = 16.
- Extract D (8): T = min(16, 11) = 11.
- Extract T (11).

Final distances: S 0, B 2, A 5, C 7, D 8, T 11. Sum = 0 + 2 + 5 + 7 + 8 + 11 = **33**.

**Trap:** the direct-looking edges S→A (7), B→D (11) and C→T (9) are all beaten by longer chains of cheap edges; the shortest path to T is S→B→A→C→D→T.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, 10, 13, '∞'],
                        [0, 5, 2, 7, 11, '∞'],
                        [0, 5, 2, 7, 8, 16],
                        [0, 5, 2, 7, 8, 11],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [("S","A",7),("S","B",2),("B","A",3),("B","C",8),("A","C",2),("A","D",6),
     ("C","D",1),("C","T",9),("D","T",3),("B","D",11)]
G = {v: [] for v in "SABCDT"}
for u, v, w in E: G[u].append((v, w))
d = {v: float('inf') for v in G}; d["S"] = 0; pq = [(0, "S")]
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
            'topic': 'Linked lists — pointer manipulation in Python',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

head = None
for v in [4, 8, 15, 16, 23, 42]:
    head = Node(v, head)

p = head
while p and p.nxt:
    p.nxt = p.nxt.nxt
    p = p.nxt

out = []
while head:
    out.append(head.v)
    head = head.nxt
print(out)''',
            'options': ['`[4, 15, 23]`', '`[23, 15, 4]`', '`[42, 16, 8]`', '`[42, 16, 8, 4]`'],
            'answer': 'C',
            'solution': '''`Node(v, head)` puts each new node **in front**, so the list is built in reverse: 42 → 23 → 16 → 15 → 8 → 4.

The `while` loop unlinks every second node: it makes `p` skip its successor, then advances `p` to the new successor.

- p = 42: 42.nxt = 16 (23 removed); p = 16.
- p = 16: 16.nxt = 8 (15 removed); p = 8.
- p = 8: 8.nxt = 4.nxt = None (4 removed); p = None → loop stops (the `p and` guard prevents an AttributeError).

Remaining list: 42 → 16 → 8, so `[42, 16, 8]` is printed.

- (A) assumes the list is in insertion order 4 → 8 → … .
- (B) keeps exactly the nodes that were removed.
- (D) assumes the last node survives, i.e. that the loop stops before processing p = 8.

**Trap:** head-insertion reverses order; always draw the list before tracing pointer surgery.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [42, 23, 16, 15, 8, 4],
                    'head': 'head',
                    'caption': 'List after the first loop',
                },
                {
                    'type': 'linkedlist',
                    'values': [42, 16, 8],
                    'head': 'head',
                    'caption': 'List after removing alternate nodes',
                },
            ],
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[42, 16, 8]' and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST — reconstruction from post-order',
            'text': '''The **post-order** traversal of a binary search tree with distinct keys is
9, 17, 14, 26, 23, 35, 48, 41, 30.
Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)''',
            'options': [
                'The in-order successor of 26 is 35',
                'The tree has exactly 4 leaves',
                'The pre-order traversal is 30, 23, 14, 9, 17, 26, 41, 35, 48',
                'The height of the tree is 3',
            ],
            'answer': ['C', 'D'],
            'solution': '''In post-order the **last** key is the root; the earlier keys split into those smaller (left subtree) and larger (right subtree), each again in post-order. Since the in-order of a BST is the sorted order, the post-order alone determines the BST.

- Root 30. Left part: 9, 17, 14, 26, 23 (all < 30). Right part: 35, 48, 41.
- Left subtree root 23: smaller {9, 17, 14} → root 14 with children 9, 17; larger {26}.
- Right subtree root 41 with children 35 and 48.

Tree: 30 → (23 → (14 → 9, 17), 26), (41 → 35, 48).

- (A) 26 has no right child; it is in 30's left subtree, so its successor is **30**. **False.**
- (B) Leaves are 9, 17, 26, 35, 48 — five, not four. **False.**
- (C) Pre-order 30, 23, 14, 9, 17, 26, 41, 35, 48. **True.**
- (D) Longest path 30 → 23 → 14 → 9 has 3 edges. **True.**

**Trap:** in (A), 35 is the next key *within the right subtree*, but the root 30 lies between 26 and 35.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        30,
                        [
                            23,
                            [
                                14,
                                [9],
                                [17],
                            ],
                            [26],
                        ],
                        [
                            41,
                            [35],
                            [48],
                        ],
                    ],
                    'caption': 'BST reconstructed from the post-order',
                },
            ],
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

post = [9, 17, 14, 26, 23, 35, 48, 41, 30]
def build(p):
    if not p: return None
    r = p[-1]
    return [r, build([x for x in p[:-1] if x < r]), build([x for x in p[:-1] if x > r])]
T = build(post)
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def po(t): return [] if t is None else po(t[1]) + po(t[2]) + [t[0]]
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
def lv(t):
    if t is None: return 0
    return 1 if t[1] is None and t[2] is None else lv(t[1]) + lv(t[2])
assert po(T) == post
s = ino(T)
truth = {'A': pre(T) == [30,23,14,9,17,26,41,35,48], 'B': ht(T) == 3,
         'C': lv(T) == 4, 'D': s[s.index(26) + 1] == 35}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
    ],
}
