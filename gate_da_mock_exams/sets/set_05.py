# Set 05 — Binary Trees & Traversals
SET = {
    'number': 5,
    'title': 'Binary Trees & Traversals',
    'difficulty': 'Moderate',
    'focus': 'traversals, reconstruction from traversals, height, node counts',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — reconstruction from traversals',
            'text': '''A binary tree with distinct labels has
- pre-order traversal: K, C, A, G, E, H, T, X, V
- in-order traversal: A, C, E, G, H, K, T, V, X

Which of the following is its post-order traversal?''',
            'options': [
                'A, E, H, G, C, V, X, T, K',
                'A, E, H, G, C, X, V, T, K',
                'A, E, G, H, C, V, X, T, K',
                'E, H, G, A, C, V, X, T, K',
            ],
            'answer': 'A',
            'solution': '''**Concept.** The first pre-order symbol is the root; its position in the in-order sequence splits the remaining symbols into the left and right subtrees. Recurse.

- Root K. In-order left of K: {A, C, E, G, H}; right of K: {T, V, X}.
- Left part, pre-order C, A, G, E, H → root C; in-order A | C | E, G, H, so A is C's left child and the subtree {E, G, H} (pre-order G, E, H) has root G with children E and H.
- Right part, pre-order T, X, V → root T; in-order T, V, X has nothing left of T, so T has only a right subtree {V, X} with root X; V lies left of X in in-order, so V is X's **left** child.

Post-order (left, right, root): A, E, H, G, C, V, X, T, K → option (A).

- (B) puts X before V, i.e. treats V as a child *after* X — wrong because V is X's left child and post-order lists children before the parent.
- (C) swaps G and H: G is the parent of H, so G must follow H.
- (D) moves A after E, H, G: A is in the left subtree of C, visited first.

**Tip:** always verify by re-deriving the in-order of the reconstructed tree.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'K',
                        [
                            'C',
                            ['A'],
                            [
                                'G',
                                ['E'],
                                ['H'],
                            ],
                        ],
                        [
                            'T',
                            None,
                            [
                                'X',
                                ['V'],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Reconstructed tree',
                },
            ],
            'verify': '''ANSWER = {'C': 'A', 'A': 'C'}.get(ANSWER, ANSWER)

def build(pre, ino):
    if not pre: return None
    r = pre[0]; k = ino.index(r)
    return (r, build(pre[1:k+1], ino[:k]), build(pre[k+1:], ino[k+1:]))
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
t = build(list("KCAGEHTXV"), list("ACEGHKTVX"))
P = post(t)
opts = {"C": "AEHGCVXTK", "B": "AEHGCXVTK", "A": "AEGHCVXTK", "D": "EHGACVXTK"}
assert [k for k, v in opts.items() if list(v) == P] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary trees — node counts',
            'text': 'A binary tree has 40 nodes in total. Exactly 7 of its nodes have exactly one child. The number of leaves in the tree is ______.',
            'answer': '17',
            'solution': '''**Concept.** In any non-empty binary tree, if n₀, n₁, n₂ are the numbers of nodes with 0, 1, 2 children, then n₀ = n₂ + 1. Proof by edge counting: there are n − 1 edges, and every edge leaves a parent, so n − 1 = n₁ + 2n₂. Substituting n = n₀ + n₁ + n₂ gives n₀ = n₂ + 1.

**Computation.**
- n₀ + n₁ + n₂ = 40 with n₁ = 7 → n₀ + n₂ = 33.
- n₀ = n₂ + 1 → 2n₂ + 1 = 33 → n₂ = 16.
- Leaves n₀ = 17.

Check: edges = n₁ + 2n₂ = 7 + 32 = 39 = 40 − 1. ✓

**Trap:** the count of one-child nodes does not affect the relation n₀ = n₂ + 1; it only enters through the total. Answering 33/2 or forgetting the +1 gives 16.''',
            'verify': '''
n, n1 = 40, 7
sols = [n0 for n0 in range(n+1) for n2 in range(n+1)
        if n0 + n1 + n2 == n and n0 == n2 + 1 and n - 1 == n1 + 2*n2]
assert sols == [int(ANSWER)]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "TRAVERSAL"
print(s[::-2], s[-3:1:-1], s[1::3])''',
            'options': ['`LSEAT SREVAR RVA`', '`LSEAT SREVA REA`', '`LAEST SREVA REA`', '`LSEAT SREV REA`'],
            'answer': 'B',
            'solution': '''**Concept.** `s[start:stop:step]` includes `start`, excludes `stop`; a negative step walks right-to-left, and omitted bounds default to the appropriate end.

Indices: T0 R1 A2 V3 E4 R5 S6 A7 L8.
- `s[::-2]`: start at index 8 and step −2 → 8, 6, 4, 2, 0 → L, S, E, A, T = `LSEAT`.
- `s[-3:1:-1]`: −3 means index 6; go down while index > 1 → 6, 5, 4, 3, 2 → S, R, E, V, A = `SREVA`.
- `s[1::3]`: 1, 4, 7 → R, E, A = `REA`.

Output: `LSEAT SREVA REA` → (B).

- (A) includes index 1 (R) in the second slice and uses step 2 in the third.
- (C) reads the even-indexed characters left to right and then reverses wrongly.
- (D) stops one early, as if the stop index 1 were index 2.

**Trap:** the stop index is excluded even when stepping backwards.''',
            'verify': "ANSWER = {'D': 'B', 'B': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'LSEAT SREVA REA'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — aliasing and shallow copy',
            'text': 'Consider the following Python code. After it executes, which of the following expressions evaluate to `True`?',
            'code': '''x = [1, 2, [3, 4]]
y = x[:]
z = x
y[2].append(5)
z.append(6)
y[0] = 9''',
            'options': [
                '`x == [1, 2, [3, 4, 5], 6]`',
                '`y == [9, 2, [3, 4, 5]]`',
                '`x[2] is y[2]`',
                '`len(y) == 4`',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** `x[:]` is a *shallow* copy: a new outer list whose elements are the same objects. `z = x` creates no copy at all, only a second name.

Trace:
- `y = x[:]` → y is a new list, but `y[2]` and `x[2]` are the *same* inner list.
- `y[2].append(5)` mutates that shared inner list → both see `[3, 4, 5]`.
- `z.append(6)` mutates x (z is x) → x = `[1, 2, [3, 4, 5], 6]`; y unaffected.
- `y[0] = 9` rebinds slot 0 of y only → y = `[9, 2, [3, 4, 5]]`.

- (A) True.
- (B) True.
- (C) True — the shallow copy shares the inner list object.
- (D) False — y has 3 elements; the append went to x.

**Trap:** mutating a nested object through a shallow copy is visible in the original; rebinding a top-level slot is not.''',
            'verify': '''
assert x == [1, 2, [3, 4, 5], 6] and y == [9, 2, [3, 4, 5]]
assert x[2] is y[2] and len(y) != 4
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression below is evaluated with a stack, where every operand is a single integer token and `/` denotes integer (floor) division. The second operand popped is the left operand.

`9 4 2 - 3 * + 7 2 / -`

The value of the expression is ______.''',
            'answer': '12',
            'solution': '''**Concept.** Scan left to right: push operands; on an operator pop the right operand b, then the left operand a, push a op b.

Trace (stack shown bottom → top):
- 9, 4, 2 → [9, 4, 2]
- `-` → 4 − 2 = 2 → [9, 2]
- 3 → [9, 2, 3]; `*` → 2 × 3 = 6 → [9, 6]
- `+` → 9 + 6 = 15 → [15]
- 7, 2 → [15, 7, 2]; `/` → 7 // 2 = 3 → [15, 3]
- `-` → 15 − 3 = 12 → [12]

Value = **12** (infix: 9 + (4 − 2) × 3 − 7 / 2).

**Trap:** popping in the wrong order turns `4 2 -` into −2 and `7 2 /` into 0, giving a different result. The maximum stack depth here is only 3.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [15, 7, 2],
                    'label': 'just before /',
                    'caption': 'Stack just before the `/` is applied',
                },
            ],
            'verify': '''
st = []
for tok in "9 4 2 - 3 * + 7 2 / -".split():
    if tok.isdigit(): st.append(int(tok)); continue
    b = st.pop(); a = st.pop()
    st.append({'+': a+b, '-': a-b, '*': a*b, '/': a//b}[tok])
assert st == [int(ANSWER)]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — level-order traversal',
            'text': 'Consider the binary tree shown. Which of the following is its level-order (breadth-first, left to right within each level) traversal?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        7,
                        [
                            3,
                            [12],
                            [
                                5,
                                [1],
                                [
                                    11,
                                    None,
                                    [2],
                                ],
                            ],
                        ],
                        [
                            9,
                            None,
                            [
                                4,
                                [6],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Binary tree T',
                },
            ],
            'options': [
                '7, 9, 3, 12, 5, 4, 6, 11, 1, 2',
                '7, 3, 12, 5, 1, 11, 2, 9, 4, 6',
                '7, 3, 9, 12, 5, 4, 1, 11, 6, 2',
                '7, 3, 9, 12, 5, 4, 1, 11, 2, 6',
            ],
            'answer': 'C',
            'solution': '''**Concept.** Level-order uses a FIFO queue: dequeue a node, output it, enqueue its left then right child. Nodes therefore appear level by level, left to right.

Levels of T:
- depth 0: 7
- depth 1: 3, 9
- depth 2: 12, 5, 4
- depth 3: 1, 11 (children of 5), 6 (child of 4)
- depth 4: 2

Sequence: 7, 3, 9, 12, 5, 4, 1, 11, 6, 2 → (C).

- (A) is a zig-zag order: it reverses alternate levels.
- (B) is the pre-order traversal (depth-first).
- (D) places 2 (depth 4) before 6 (depth 3) — it treats 2 as being on 11's level.

**Tip:** 6 is at depth 3 even though it hangs from the right side; depth, not horizontal position, decides the level.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

from collections import deque
T = (7, (3, (12, None, None), (5, (1, None, None), (11, None, (2, None, None)))),
     (9, None, (4, (6, None, None), None)))
q, out = deque([T]), []
while q:
    n = q.popleft()
    if n is None: continue
    out.append(n[0]); q.append(n[1]); q.append(n[2])
assert out == [7, 3, 9, 12, 5, 4, 1, 11, 6, 2] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'The keys 44, 17, 82, 59, 31, 96, 23, 70, 38, 65 are inserted into an initially empty hash table with 7 slots (indices 0–6) using h(k) = k mod 7 and separate chaining. Let L be the length of the longest chain and E the number of empty slots after all insertions. The value of L + E is ______.',
            'answer': '7',
            'solution': '''**Concept.** With chaining every key goes into the list at its home slot; there is no probing, so just compute k mod 7 for every key.

- 44 → 2, 17 → 3, 82 → 5, 59 → 3, 31 → 3
- 96 → 5, 23 → 2, 70 → 0, 38 → 3, 65 → 2

Chains: slot 0: [70]; slot 2: [44, 23, 65]; slot 3: [17, 59, 31, 38]; slot 5: [82, 96]; slots 1, 4, 6 are empty.

L = 4 (slot 3), E = 3, so L + E = **7**.

**Trap:** 59 = 56 + 3 and 38 = 35 + 3 are easy to mis-reduce; also note that 10 keys in 7 slots must leave at least one chain of length ≥ 2 (pigeonhole), but the load factor 10/7 says nothing about the actual maximum.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: [70],
                        2: [44, 23, 65],
                        3: [17, 59, 31, 38],
                        5: [82, 96],
                    },
                    'caption': 'Final chained table',
                },
            ],
            'verify': '''
ch = {}
for k in [44, 17, 82, 59, 31, 96, 23, 70, 38, 65]:
    ch.setdefault(k % 7, []).append(k)
assert max(map(len, ch.values())) + (7 - len(ch)) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort — number of shifts',
            'text': 'Insertion sort (ascending) is applied to the array [5, 8, 2, 9, 1, 7, 3]. A *shift* is one move of an element one position to the right to make room for the key being inserted. The total number of shifts performed is',
            'options': ['11', '12', '13', '21'],
            'answer': 'B',
            'solution': '''**Concept.** Every shift in insertion sort removes exactly one inversion (a pair i < j with A[i] > A[j]), and sorting removes them all. So #shifts = #inversions.

Count inversions element by element (elements to its right that are smaller):
- 5: {2, 1, 3} → 3
- 8: {2, 1, 7, 3} → 4
- 2: {1} → 1
- 9: {1, 7, 3} → 3
- 1: none → 0
- 7: {3} → 1
- 3: → 0

Total = 3 + 4 + 1 + 3 + 0 + 1 = **12** → (B).

- (A) 11 and (C) 13 come from missing or double-counting one pair.
- (D) 21 = 7·6/2 is the worst case (reverse-sorted input), not this input.

**Tip:** the number of *comparisons* differs from the number of shifts — it is shifts plus one for each insertion that stops before reaching the front.''',
            'verify': '''
A = [5, 8, 2, 9, 1, 7, 3]; shifts = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0 and A[j] > key:
        A[j+1] = A[j]; j -= 1; shifts += 1
    A[j+1] = key
assert shifts == 12 and ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Graphs — BFS levels',
            'text': 'Breadth-first search is run from vertex A on the undirected graph shown. The number of vertices whose BFS distance (number of edges) from A is exactly 2 is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'H'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2.6],
                        'E': [3, 1],
                        'F': [3, -0.6],
                        'G': [4.5, 2],
                        'H': [4.5, 0],
                    },
                },
            ],
            'answer': '3',
            'solution': '''**Concept.** BFS discovers vertices in non-decreasing order of hop distance; the level of a vertex is its shortest-path length in an unweighted graph.

- Level 0: A
- Level 1: neighbours of A → B, C
- Level 2: new neighbours of B (D, E) and of C (F; E already found) → D, E, F
- Level 3: G (from D or E), H (from F)

Exactly **3** vertices (D, E, F) are at distance 2.

**Trap:** E is adjacent to both B and C, so it must be counted once; G is adjacent to E but is at distance 3, not 2, because no level-1 vertex touches it.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'H'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2.6],
                        'E': [3, 1],
                        'F': [3, -0.6],
                        'G': [4.5, 2],
                        'H': [4.5, 0],
                    },
                    'highlight': ['D', 'E', 'F'],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['F', 'H'],
                    ],
                    'caption': 'BFS tree (red) — level-2 vertices highlighted',
                },
            ],
            'verify': '''
from collections import deque
E = [("A","B"),("A","C"),("B","D"),("B","E"),("C","E"),("C","F"),("D","G"),("E","G"),
     ("F","H"),("G","H")]
adj = {}
for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
d = {"A": 0}; q = deque("A")
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in d: d[v] = d[u] + 1; q.append(v)
assert sum(1 for v in d if d[v] == 2) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — recursion on trees',
            'text': 'A binary tree is stored as nested tuples `(value, left, right)`. Consider the following Python program. What is printed?',
            'code': '''def f(t, d=0):
    if t is None:
        return 0
    v, l, r = t
    if l is None and r is None:
        return v if d % 2 == 0 else -v
    return f(l, d + 1) + f(r, d + 1)

T = (1, (2, (4, None, None), (5, (8, None, None), None)),
        (3, None, (6, (9, None, None), (7, None, None))))
print(f(T))''',
            'options': ['`-20`', '`20`', '`-12`', '`4`'],
            'answer': 'A',
            'solution': '''**Concept.** `f` adds the values of **leaves only**, with sign + at even depth and − at odd depth (root depth 0). Internal nodes contribute nothing; `None` children contribute 0.

Leaves and depths:
- 4: depth 2 (1→2→4) → +4
- 8: depth 3 (1→2→5→8) → −8
- 9: depth 3 (1→3→6→9) → −9
- 7: depth 3 (1→3→6→7) → −7

Sum = 4 − 8 − 9 − 7 = **−20** → (A).

- (B) 20 results from counting the root at depth 1, which flips every sign.
- (C) −12 = 4 − 9 − 7 misses leaf 8 (it hangs below the one-child node 5).
- (D) 4 counts only even-depth leaves.

**Trap:** a node with one child (5 and 3) is *not* a leaf, and the depth passed to children is `d + 1` regardless of which side they are on.''',
            'verify': "ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '-20'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary trees — reconstruction from post-order and in-order',
            'text': '''A binary tree with distinct keys has
- in-order traversal: 4, 2, 9, 5, 7, 1, 3, 8, 6
- post-order traversal: 4, 9, 2, 7, 5, 8, 6, 3, 1

Which of the following statements about this tree is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)''',
            'options': [
                'Its pre-order traversal is 1, 5, 2, 4, 9, 7, 3, 6, 8',
                'Its height is 3',
                'Node 3 has a left child',
                'It has exactly 4 leaves',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** In post-order the root is the **last** symbol. Locate it in the in-order sequence to split left/right subtrees; the post-order sequence splits at the same sizes (left block first, then right block).

Reconstruction:
- Root = 1. In-order: [4, 2, 9, 5, 7] | 1 | [3, 8, 6]. Post-order blocks: [4, 9, 2, 7, 5] and [8, 6, 3].
- Left block: root 5 (last of 4, 9, 2, 7, 5). In-order [4, 2, 9] | 5 | [7]. So 5 has right child 7 and left subtree {4, 2, 9} whose post-order 4, 9, 2 gives root 2 with children 4 (left) and 9 (right).
- Right block: root 3 (last of 8, 6, 3). In-order 3 | [8, 6] → nothing left of 3, so 3 has only a right subtree {8, 6}; post-order 8, 6 → root 6, and 8 precedes 6 in in-order, so 8 is 6's **left** child.

Option analysis:
- (A) Pre-order (root, left, right): 1, 5, 2, 4, 9, 7, 3, 6, 8. **True.**
- (B) Longest paths 1→5→2→4, 1→5→2→9 and 1→3→6→8 all have 3 edges. **True.**
- (C) 3 has only a right child (6). **False.**
- (D) Leaves are 4, 9, 7, 8 — exactly 4. **True.**

**Trap:** students often read the post-order from the front and pick 4 as the root. Another slip is attaching 8 as the right child of 6; the in-order sequence (…, 8, 6) forces it to be the left child.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        1,
                        [
                            5,
                            [
                                2,
                                [4],
                                [9],
                            ],
                            [7],
                        ],
                        [
                            3,
                            None,
                            [
                                6,
                                [8],
                                None,
                            ],
                        ],
                    ],
                    'highlight': [4, 9, 7, 8],
                    'caption': 'Reconstructed tree (leaves highlighted)',
                },
            ],
            'verify': '''
def build(post, ino):
    if not post: return None
    r = post[-1]; k = ino.index(r)
    return (r, build(post[:k], ino[:k]), build(post[k:-1], ino[k+1:]))
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def leaves(t):
    if t is None: return 0
    return 1 if t[1] is None and t[2] is None else leaves(t[1]) + leaves(t[2])
def find(t, x):
    if t is None: return None
    return t if t[0] == x else (find(t[1], x) or find(t[2], x))
t = build([4,9,2,7,5,8,6,3,1], [4,2,9,5,7,1,3,8,6])
truth = {"A": pre(t) == [1,5,2,4,9,7,3,6,8], "B": h(t) == 3,
         "C": find(t, 3)[1] is not None, "D": leaves(t) == 4}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Binary trees — counting trees with given traversals',
            'text': 'Consider binary trees on the five labelled nodes P, Q, R, S, T. The number of distinct such binary trees whose pre-order traversal is P, Q, R, S, T **and** whose post-order traversal is T, S, R, Q, P is ______.',
            'answer': '16',
            'solution': '''**Concept.** Pre-order and post-order together do **not** determine a binary tree when some node has exactly one child, because neither traversal records whether that child is a left or a right child.

Structure forced by the traversals:
- Pre-order P, Q, R, S, T says P is the root, and post-order ending with P agrees.
- Take any node X. In pre-order X precedes all its descendants; in post-order X follows them. If X had two non-empty subtrees L and R, both traversals would list all of L before all of R — but the given post-order is the exact reverse of the pre-order, so no two nodes keep their relative order. Hence **no node has two children**.
- So the tree is a **chain** P–Q–R–S–T (each of P, Q, R, S has exactly one child), and any such chain does give pre-order PQRST and post-order TSRQP.

Counting: each of the 4 one-child nodes independently chooses whether its child is a left or right child → 2⁴ = **16** trees, all with the given pre- and post-order.

**Trap:** answering 1 (assuming pre + post determine the tree) or 2 (only left-skewed and right-skewed). In-order would distinguish them; pre + post do not.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'P',
                        [
                            'Q',
                            None,
                            [
                                'R',
                                [
                                    'S',
                                    None,
                                    ['T'],
                                ],
                                None,
                            ],
                        ],
                        None,
                    ],
                    'caption': 'One of the 16 trees (zig-zag chain)',
                },
            ],
            'verify': '''
from functools import lru_cache
def shapes(n):
    if n == 0: return [None]
    out = []
    for k in range(n):
        for L in shapes(k):
            for R in shapes(n-1-k): out.append(('*', L, R))
    return out
def label(t, it):
    if t is None: return None
    v = next(it); L = label(t[1], it); R = label(t[2], it)
    return (v, L, R)
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
cnt = 0
for s in shapes(5):
    t = label(s, iter("PQRST"))
    if post(t) == list("TSRQP"): cnt += 1
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — closures and late binding',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''fs = []
for i in range(4):
    fs.append(lambda x, i=i: x * i if i % 2 else x + i)
gs = [lambda x: x * i for i in range(4)]
print(sum(f(3) for f in fs), sum(g(3) for g in gs))''',
            'options': ['`18 36`', '`20 18`', '`36 36`', '`20 36`'],
            'answer': 'D',
            'solution': '''**Concept.** A lambda's free variable is looked up **when the lambda is called** (late binding). A default argument (`i=i`) is evaluated **when the lambda is created**, freezing the current value.

First sum (`fs`, defaults freeze i = 0, 1, 2, 3); body is a conditional expression `x*i if i % 2 else x+i`:
- i = 0 (even): 3 + 0 = 3
- i = 1 (odd): 3 × 1 = 3
- i = 2 (even): 3 + 2 = 5
- i = 3 (odd): 3 × 3 = 9
- total = 20

Second sum (`gs`): all four lambdas share the comprehension's variable `i`, which is 3 once the comprehension finishes. Each call returns 3 × 3 = 9 → 4 × 9 = 36.

Output: `20 36` → (D).

- (A) mis-evaluates the conditional as always `x*i` for `fs` (0+3+6+9 = 18).
- (B) assumes `gs` captured 0, 1, 2, 3 → 0 + 3 + 6 + 9 = 18 (no late binding).
- (C) applies late binding to `fs` as well, ignoring the default argument.

**Trap:** the comprehension has its own scope, but the closures still see the *final* value of that scope's `i`.''',
            'verify': "ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '20 36'",
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary trees — iterative traversal with a stack',
            'text': 'The function `walk` below is applied to the tree shown (stored as nested tuples `(label, left, right)`). What list does `walk(T)` return?',
            'code': '''def walk(t):
    out, st = [], [t]
    while st:
        node = st.pop()
        if node is None:
            continue
        out.append(node[0])
        st.append(node[1])
        st.append(node[2])
    return out''',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'M',
                        [
                            'D',
                            ['B'],
                            [
                                'H',
                                ['F'],
                                None,
                            ],
                        ],
                        [
                            'R',
                            ['P'],
                            [
                                'W',
                                None,
                                ['Z'],
                            ],
                        ],
                    ],
                    'caption': 'Tree T',
                },
            ],
            'options': [
                'M, D, B, H, F, R, P, W, Z',
                'B, F, H, D, P, Z, W, R, M',
                'M, R, W, Z, P, D, H, F, B',
                'M, R, P, W, Z, D, B, H, F',
            ],
            'answer': 'C',
            'solution': '''**Concept.** The stack is LIFO. Pushing left **then** right means the right child is popped first, so the function visits root, right subtree, left subtree — the *mirror pre-order*, which equals the **reverse of the post-order**.

Trace (stack top on the right; `·` = None):
- pop M → out M; push D, R
- pop R → out R; push P, W
- pop W → out W; push ·, Z → pop Z → out Z; pop ·, pop · (Z's children); pop · (W's left)
- pop P → out P (children ·)
- pop D → out D; push B, H
- pop H → out H; push F, · → pop · → pop F → out F
- pop B → out B

Result: M, R, W, Z, P, D, H, F, B → (C). Post-order is B, F, H, D, P, Z, W, R, M, and (C) is exactly its reverse.

- (A) is ordinary pre-order (would need right pushed first).
- (B) is the post-order itself.
- (D) visits R's children left-first, i.e. treats the structure as a queue at one level — not what a stack does.

**Tip:** this push order is the basis of the 'two-stack post-order' trick: run it, then reverse the output.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

T = ("M", ("D", ("B", None, None), ("H", ("F", None, None), None)),
     ("R", ("P", None, None), ("W", None, ("Z", None, None))))
r = walk(T)
assert r == list("MRWZPDHFB") and ANSWER == 'B'
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
assert r == post(T)[::-1]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': 'The Lomuto partition procedure below is applied once to A = [7, 2, 9, 4, 3, 8, 5] with lo = 0 and hi = 6. Which of the following statements is/are TRUE?',
            'code': '''def partition(A, lo, hi):
    pivot, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1''',
            'options': [
                'After partition A = [2, 4, 3, 5, 9, 8, 7]',
                'The returned index is 3',
                'Exactly 3 swap statements (including the final one) are executed',
                'The sub-array to the right of the pivot is [9, 8, 7]',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** Lomuto keeps A[lo..i] ≤ pivot. Each element ≤ pivot advances i and is swapped into place; finally the pivot is swapped into position i + 1.

Pivot = 5, i = −1:
- j = 0: 7 > 5 → nothing.
- j = 1: 2 ≤ 5 → i = 0, swap A[0], A[1] → [2, 7, 9, 4, 3, 8, 5]
- j = 2: 9 > 5.
- j = 3: 4 ≤ 5 → i = 1, swap A[1], A[3] → [2, 4, 9, 7, 3, 8, 5]
- j = 4: 3 ≤ 5 → i = 2, swap A[2], A[4] → [2, 4, 3, 7, 9, 8, 5]
- j = 5: 8 > 5.
- final: swap A[3], A[6] → [2, 4, 3, 5, 9, 8, 7]; return 3.

Option analysis:
- (A) **True** — matches the final state.
- (B) **True** — pivot lands at index 3.
- (C) **False** — swaps happen at j = 1, 3, 4 plus the final one: **4** in total.
- (D) **True** — A[4..6] = [9, 8, 7].

**Trap:** forgetting the final pivot swap when counting swaps, or assuming the right part keeps its original relative order (it does not: 7 moved to the end). Lomuto is not stable.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [2, 4, 3, 5, 9, 8, 7],
                    'highlight': [3],
                    'pointers': {
                        'pivot': 3,
                    },
                    'caption': 'Array after partition',
                },
            ],
            'verify': '''
A = [7, 2, 9, 4, 3, 8, 5]; swaps = 0
pivot, i = A[6], -1
for j in range(0, 6):
    if A[j] <= pivot:
        i += 1; A[i], A[j] = A[j], A[i]; swaps += 1
A[i+1], A[6] = A[6], A[i+1]; swaps += 1
B = [7, 2, 9, 4, 3, 8, 5]; p = partition(B, 0, 6)
truth = {"A": B == [2,4,3,5,9,8,7], "B": p == 3, "C": swaps == 3, "D": B[p+1:] == [9,8,7]}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source S on the weighted directed graph shown. The sum of the final shortest-path distances of **all six** vertices (including S itself) is ______.",
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
                        ['D', 'T', 4],
                        ['B', 'D', 10],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, 2.2],
                        'D': [4, -0.2],
                        'T': [6, 1],
                    },
                },
            ],
            'answer': '34',
            'solution': '''**Concept.** Dijkstra repeatedly extracts the unfinished vertex with the smallest tentative distance and relaxes its outgoing edges; with non-negative weights the extracted value is final.

Trace (tentative distances after each extraction):
- Extract S (0): A = 7, B = 2.
- Extract B (2): A = min(7, 2+3) = 5; C = 2+8 = 10; D = 2+10 = 12.
- Extract A (5): C = min(10, 5+2) = 7; D = min(12, 5+6) = 11.
- Extract C (7): D = min(11, 7+1) = 8; T = 7+9 = 16.
- Extract D (8): T = min(16, 8+4) = 12.
- Extract T (12).

Final: S 0, A 5, B 2, C 7, D 8, T 12. Sum = 0 + 5 + 2 + 7 + 8 + 12 = **34**.

**Trap:** the direct edge S→A (7) and B→D (10) look attractive but are beaten by detours through B and C; T's distance is improved twice (16 → 12).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'row_labels': ['after S', 'after B', 'after A', 'after C', 'after D'],
                    'rows': [
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, 10, 12, '∞'],
                        [0, 5, 2, 7, 11, '∞'],
                        [0, 5, 2, 7, 8, 16],
                        [0, 5, 2, 7, 8, 12],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [("S","A",7),("S","B",2),("B","A",3),("B","C",8),("A","C",2),("A","D",6),
     ("C","D",1),("C","T",9),("D","T",4),("B","D",10)]
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
            'topic': 'Linked lists — recursive pointer manipulation',
            'text': 'Consider the following Python program operating on the singly linked list shown. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def build(vals):
    head = None
    for v in reversed(vals):
        head = Node(v, head)
    return head

def mystery(h):
    if h is None or h.nxt is None:
        return h
    second = h.nxt
    h.nxt = mystery(second.nxt)
    second.nxt = h
    return second

h = mystery(build([1, 2, 3, 4, 5, 6, 7]))
out = []
while h:
    out.append(h.v)
    h = h.nxt
print(out)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7],
                    'caption': 'Input list',
                },
            ],
            'options': [
                '`[1, 3, 2, 5, 4, 7, 6]`',
                '`[7, 6, 5, 4, 3, 2, 1]`',
                '`[2, 1, 4, 3, 6, 5]`',
                '`[2, 1, 4, 3, 6, 5, 7]`',
            ],
            'answer': 'D',
            'solution': '''**Concept.** `mystery` swaps the first two nodes and recursively processes the list starting at the third node. It therefore swaps nodes in adjacent pairs; an odd last node is returned unchanged by the base case.

Trace of the recursion:
- mystery(1): second = 2; 1.nxt = mystery(3); 2.nxt = 1; return 2.
- mystery(3): second = 4; 3.nxt = mystery(5); 4.nxt = 3; return 4.
- mystery(5): second = 6; 5.nxt = mystery(7); 6.nxt = 5; return 6.
- mystery(7): 7.nxt is None → return 7 (base case).

Unwinding: 5 → 7, 3 → 6, 1 → 4, so the list reads 2, 1, 4, 3, 6, 5, 7 → (D).

- (A) starts pairing from the second node.
- (B) is a full reversal — this function never reverses beyond a pair.
- (C) drops the unpaired 7; the base case keeps it.

**Trap:** the assignment `h.nxt = mystery(second.nxt)` must happen before `second.nxt = h`; otherwise `second.nxt` would already point back to h.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [2, 1, 4, 3, 6, 5, 7],
                    'caption': 'List after mystery',
                },
            ],
            'verify': "ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[2, 1, 4, 3, 6, 5, 7]'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Binary search — probe counting',
            'text': 'The function `bsearch` below is used on the sorted array A shown (0-based indices). Let p₁ be the value of `probes` returned when searching for x = 50, and p₂ the value returned when searching for x = 69. The value of p₁ + p₂ is ______.',
            'code': '''def bsearch(A, x):
    lo, hi, probes = 0, len(A) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        probes += 1
        if A[mid] == x:
            return mid, probes
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, probes''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [4, 9, 13, 18, 22, 27, 31, 36, 42, 47, 53, 58, 64, 69, 75],
                    'label': 'A',
                },
            ],
            'answer': '7',
            'solution': '''**Concept.** Each loop iteration inspects one middle element (one probe) and halves the range. With 15 = 2⁴ − 1 elements, at most 4 probes are ever needed.

Search x = 50:
- lo 0, hi 14 → mid 7 (36) < 50 → lo = 8
- lo 8, hi 14 → mid 11 (58) > 50 → hi = 10
- lo 8, hi 10 → mid 9 (47) < 50 → lo = 10
- lo 10, hi 10 → mid 10 (53) > 50 → hi = 9; loop ends. p₁ = 4.

Search x = 69:
- mid 7 (36) < 69 → lo = 8
- mid 11 (58) < 69 → lo = 12
- lo 12, hi 14 → mid 13 (69) found. p₂ = 3.

p₁ + p₂ = 4 + 3 = **7**.

**Trap:** an unsuccessful search on a perfectly balanced 15-element array always costs exactly 4 probes; the final `lo > hi` test is not a probe because no array element is examined.''',
            'verify': '''
A = [4, 9, 13, 18, 22, 27, 31, 36, 42, 47, 53, 58, 64, 69, 75]
assert bsearch(A, 50)[1] + bsearch(A, 69)[1] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Graphs — DFS and BFS trees',
            'text': 'Consider the undirected graph shown. Depth-first search (recursive) and breadth-first search are both started at A; whenever there is a choice, neighbours are explored in alphabetical order. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['D', 'F'],
                        ['F', 'G'],
                        ['C', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1],
                        'E': [4.5, 2],
                        'F': [4.5, 0.5],
                        'G': [3, -0.6],
                    },
                },
            ],
            'options': [
                'The DFS visit order is A, B, D, C, G, F, E',
                'In the DFS tree, the depth of E (edges from A) is 5',
                'Exactly 3 edges of the graph are not DFS-tree edges',
                'In the BFS tree, E is at level 3',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** Recursive DFS goes as deep as possible before backtracking; in an undirected graph every non-tree edge is a back edge. BFS levels equal hop distances.

DFS from A (alphabetical):
- A → B (first neighbour) → D (B's only unvisited neighbour)
- D's neighbours B, C, E, F → C first
- C's neighbours A (seen), D (seen), G → G
- G's neighbours C (seen), F → F
- F's neighbours D (seen), E → E; E has no unvisited neighbour; backtrack all the way.
- Order: A, B, D, C, G, F, E. Tree edges: AB, BD, DC, CG, GF, FE (a single path).

BFS from A: level 1 {B, C}, level 2 {D, G}, level 3 {E, F}.

Option analysis:
- (A) **True** (derived above).
- (B) **False** — the DFS tree is the path A–B–D–C–G–F–E, so E is at depth **6**.
- (C) **True** — 9 edges − 6 tree edges = 3 back edges (AC, DE, DF).
- (D) **True** — E is reached via D (level 2) → level 3.

**Trap:** E is adjacent to D, so it is tempting to place it at DFS depth 3; but DFS commits to C before ever looking at E, and E is finally reached from F.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['D', 'F'],
                        ['F', 'G'],
                        ['C', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1],
                        'E': [4.5, 2],
                        'F': [4.5, 0.5],
                        'G': [3, -0.6],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'D'],
                        ['D', 'C'],
                        ['C', 'G'],
                        ['G', 'F'],
                        ['F', 'E'],
                    ],
                    'caption': 'DFS tree edges in red',
                },
            ],
            'verify': '''
from collections import deque
E = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E"),("E","F"),("D","F"),("F","G"),("C","G")]
adj = {}
for u, v in E: adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
order, depth, tree = [], {}, 0
def dfs(u, d):
    global tree
    order.append(u); depth[u] = d
    for v in sorted(adj[u]):
        if v not in depth: tree += 1; dfs(v, d + 1)
dfs("A", 0)
lvl = {"A": 0}; q = deque("A")
while q:
    u = q.popleft()
    for v in sorted(adj[u]):
        if v not in lvl: lvl[v] = lvl[u] + 1; q.append(v)
truth = {"A": order == list("ABDCGFE"), "B": depth["E"] == 5,
         "C": len(E) - tree == 3, "D": lvl["E"] == 3}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — repeated delete-min',
            'text': 'The min-heap shown is stored in the array H = [3, 9, 5, 14, 10, 8, 7, 20, 17, 12] (0-based; children of index i are 2i + 1 and 2i + 2). Two delete-min operations are performed; each moves the last element to the root and sifts it down, swapping with the **smaller** child while that child is smaller. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 9, 5, 14, 10, 8, 7, 20, 17, 12],
                    'caption': 'Initial min-heap',
                },
            ],
            'options': [
                'After the first delete-min, H = [5, 9, 7, 14, 10, 8, 12, 20, 17]',
                'After the second delete-min, the root is 7 and its children are 9 and 8',
                'After the second delete-min, key 17 is at index 5',
                'After the second delete-min, key 14 is a leaf',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** delete-min removes H[0], moves the last element to the root, then sifts down along a path of smaller children: O(log n) work.

First delete-min (remove 3, move 12 to root): [12, 9, 5, 14, 10, 8, 7, 20, 17]
- children 9, 5 → swap with 5 → [5, 9, 12, 14, 10, 8, 7, 20, 17]
- 12 at index 2, children 8, 7 → swap with 7 → [5, 9, 7, 14, 10, 8, 12, 20, 17]
- index 6 has no children → stop.

Second delete-min (remove 5, move 17 to root): [17, 9, 7, 14, 10, 8, 12, 20]
- children 9, 7 → swap with 7 → [7, 9, 17, 14, 10, 8, 12, 20]
- 17 at index 2, children 8, 12 → swap with 8 → [7, 9, 8, 14, 10, 17, 12, 20]
- index 5 has no children (11 > 7) → stop.

Option analysis:
- (A) **True**.
- (B) **True** — H[0] = 7, H[1] = 9, H[2] = 8.
- (C) **True** — 17 ends at index 5.
- (D) **False** — with 8 elements, index 3 (key 14) has child index 7 (key 20).

**Trap:** sifting toward the *left* child by habit (9 instead of 5) breaks the heap property; always compare both children.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [7, 9, 8, 14, 10, 17, 12, 20],
                    'caption': 'Heap after two delete-min operations',
                },
            ],
            'verify': '''
def popmin(h):
    h = h[:]; h[0] = h.pop(); i, n = 0, len(h)
    while True:
        l, r, s = 2*i+1, 2*i+2, i
        if l < n and h[l] < h[s]: s = l
        if r < n and h[r] < h[s]: s = r
        if s == i: return h
        h[i], h[s] = h[s], h[i]; i = s
H1 = popmin([3, 9, 5, 14, 10, 8, 7, 20, 17, 12]); H2 = popmin(H1)
truth = {"A": H1 == [5, 9, 7, 14, 10, 8, 12, 20, 17], "B": H2[:3] == [7, 9, 8],
         "C": H2.index(17) == 5, "D": 2*H2.index(14) + 1 >= len(H2)}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
    ],
}
