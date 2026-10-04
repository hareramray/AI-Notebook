# Set 35 — Full-Syllabus Mock — Paper 5
SET = {
    'number': 35,
    'title': 'Full-Syllabus Mock — Paper 5',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — try / except / finally',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def f(n):
    try:
        if n < 0:
            raise ValueError
        return n * 2
    except ValueError:
        return -1
    finally:
        if n == 3:
            return 0

print(f(3), f(-2), f(5))''',
            'options': ['`6 -1 10`', '`0 -1 10`', '`0 0 10`', '`0 -1 0`'],
            'answer': 'B',
            'solution': '''**Concept.** A `finally` block always runs as the function leaves the `try` statement, even after a `return`. If `finally` itself executes a `return`, that value **replaces** the pending return value.

- f(3): `try` evaluates `return 6`, but `finally` runs; n == 3, so it returns 0. → 0
- f(−2): ValueError is raised and caught → pending `return -1`; `finally` runs, n ≠ 3, falls through → −1.
- f(5): pending `return 10`; `finally` does nothing → 10.

Output `0 -1 10` → (B).

- (A) ignores the overriding `return` in `finally`.
- (C) assumes `finally` returns 0 for every negative n as well.
- (D) applies the override to f(5) too.

**Trap:** a `return` inside `finally` also silently swallows any exception that was propagating — a classic code-review red flag.''',
            'verify': "assert OUTPUT.strip() == '0 -1 10'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — infix to postfix conversion',
            'text': '''The infix expression

`a + b * ( c - d ) / e ^ f ^ g - h`

is converted to postfix with the standard operator-stack algorithm. Precedence: `^` (highest, right-associative) > `*`, `/` (left-associative) > `+`, `-` (left-associative). '(' is pushed on the stack and popped at the matching ')'. The maximum number of symbols (operators and parentheses) on the stack at any moment is ______.''',
            'answer': '4',
            'solution': '''**Concept.** An incoming operator pops stack operators of higher precedence, or of equal precedence when it is left-associative; a right-associative `^` does not pop an equal `^`. Operands go straight to the output.

Stack after each operator/parenthesis (bottom → top):
- `+` → [+]
- `*` → [+ *]
- `(` → [+ * (]
- `-` → [+ * ( -]  (**4**)
- `)` → pops `-` and `(` → [+ *]
- `/` → pops `*` (equal, left-assoc) → [+ /]
- `^` → [+ / ^]
- `^` → right-assoc, no pop → [+ / ^ ^]  (**4**)
- `-` → pops ^, ^, /, + → [-]
- end → pop `-`.

Postfix: `a b c d - * e f g ^ ^ / + h -`. Maximum stack size = **4**.

**Trap:** treating `^` as left-associative pops the first `^` before pushing the second, so the maximum would still be reached inside the parentheses — but the postfix would wrongly become `… e f ^ g ^ …`.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['+', '/', '^', '^'],
                    'label': 'ops',
                    'caption': 'Operator stack after reading the second ^',
                },
            ],
            'verify': '''
prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
out, st, mx = [], [], 0
for t in "a+b*(c-d)/e^f^g-h":
    if t.isalpha(): out.append(t)
    elif t == '(': st.append(t)
    elif t == ')':
        while st[-1] != '(': out.append(st.pop())
        st.pop()
    else:
        while st and st[-1] != '(' and (prec[st[-1]] > prec[t] or
                                        (prec[st[-1]] == prec[t] and t != '^')):
            out.append(st.pop())
        st.append(t)
    mx = max(mx, len(st))
while st: out.append(st.pop())
assert "".join(out) == "abcd-*efg^^/+h-" and mx == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Trees — complete binary tree in an array',
            'text': 'A complete binary tree with 50 nodes is stored in an array T[1..50] in level order (the children of T[i] are T[2i] and T[2i + 1]). Height is the number of edges on the longest root-to-leaf path. Which of the following statements is/are TRUE?',
            'options': [
                'T[26] is an internal node',
                'The tree has exactly 25 leaves',
                'The parent of T[37] is T[18]',
                'The height of the tree is 5',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept.** In a 1-based array heap layout, node i has children 2i and 2i + 1 and parent ⌊i/2⌋. Node i is internal iff 2i ≤ n.

- (A) 2 × 26 = 52 > 50, so T[26] has no children — it is a leaf. **False.**
- (B) Internal nodes are i = 1 … ⌊50/2⌋ = 25, so leaves are 26 … 50 → 25 leaves. **True.**
- (C) parent(37) = ⌊37/2⌋ = 18. **True.**
- (D) Height = ⌊log₂ 50⌋ = 5 (levels hold 1, 2, 4, 8, 16 and then 19 nodes; 2⁵ = 32 ≤ 50 < 64). **True.**

Note T[25] is the only node with exactly one child (T[50]), because n is even.

**Trap:** using 0-based formulas (children 2i + 1, 2i + 2) on a 1-based array gives parent(37) = 18 by coincidence but breaks the leaf test.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

n = 50
leaves = [i for i in range(1, n+1) if 2*i > n]
height = 0
while 2**(height+1) <= n: height += 1
truth = {"A": len(leaves) == 25, "B": height == 5, "C": 37 // 2 == 18, "D": 2*26 <= n}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — double hashing',
            'text': 'The keys 18, 41, 22, 44, 59, 32, 31, 73 are inserted in that order into an empty table of size 13 using double hashing: the i-th probe (i = 0, 1, 2, …) for key k is (h₁(k) + i·h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). The index of the slot where key 31 is stored is ______.',
            'answer': '12',
            'solution': '''**Concept.** In double hashing the step size h₂(k) depends on the key, so keys sharing a home slot follow different probe sequences.

Trace (h₁, h₂ → slot):
- 18: h₁ 5 → slot 5.
- 41: h₁ 2 → slot 2.
- 22: h₁ 9 → slot 9.
- 44: h₁ 5 (full), h₂ = 1 + 0 = 1 → 6.
- 59: h₁ 7 → slot 7.
- 32: h₁ 6 (full), h₂ = 1 + 10 = 11 → (6 + 11) mod 13 = 4.
- 31: h₁ 5 (full), h₂ = 1 + 9 = 10 → (5 + 10) mod 13 = 2 (full) → (5 + 20) mod 13 = **12**.
- 73: h₁ 8 → slot 8.

Key 31 is stored in slot **12**.

**Trap:** using h₂ = k mod 11 (without the +1) would give step 9 for 31; and forgetting the mod 13 after adding 2·h₂ = 20 gives 25.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        2: 41,
                        4: 32,
                        5: 18,
                        6: 44,
                        7: 59,
                        8: 73,
                        9: 22,
                        12: 31,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None]*13
for k in [18, 41, 22, 44, 59, 32, 31, 73]:
    i = 0
    while T[(k % 13 + i*(1 + k % 11)) % 13] is not None: i += 1
    T[(k % 13 + i*(1 + k % 11)) % 13] = k
assert T.index(31) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bubble sort — passes with early exit',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def bubble(a):
    a, passes = a[:], 0
    for i in range(len(a) - 1):
        passes += 1
        swapped = False
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return passes

print(bubble([2, 3, 4, 5, 6, 1]), bubble([6, 1, 2, 3, 4, 5]))''',
            'options': ['`5 2`', '`2 5`', '`1 1`', '`5 1`'],
            'answer': 'A',
            'solution': '''**Concept.** Each bubble pass carries the largest unsorted element all the way to the right ('rabbits' move fast), but a small element moves only **one** position left per pass ('turtles' move slowly). The early-exit flag stops after the first pass with no swaps.

- [2, 3, 4, 5, 6, 1]: the 1 is a turtle at index 5; it reaches index 0 only after 5 passes. The loop allows at most n − 1 = 5 passes, so it ends after pass 5 (no extra check pass). → 5.
- [6, 1, 2, 3, 4, 5]: pass 1 carries 6 to the end → sorted; pass 2 makes no swap and breaks. → 2.

Output `5 2` → (A).

- (B) swaps the two cases.
- (D) forgets that the verifying pass (pass 2) is counted.

**Trap:** both arrays have exactly 5 inversions, so both need 5 swaps — but the number of *passes* depends on how far elements must move left.''',
            'verify': "ANSWER = {'C': 'A', 'A': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '5 2'",
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — deleting from a doubly linked list',
            'text': 'In a doubly linked list each node has fields `prev` and `next`. Node `p` is neither the first nor the last node. Which statement sequence correctly unlinks `p` so that forward and backward traversals both skip it?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': ['x', 'p', 'y'],
                    'doubly': True,
                    'caption': 'x ⇄ p ⇄ y (part of a longer list)',
                },
            ],
            'options': [
                '`p.prev.next = p.next; p.next = p.prev.next`',
                '`p.prev.next = p.next; p.next.prev = p.next`',
                '`p.next.prev = p.prev; p.prev = p.next`',
                '`p.prev.next = p.next; p.next.prev = p.prev`',
            ],
            'answer': 'D',
            'solution': '''**Concept.** To unlink p from x ⇄ p ⇄ y, two pointers outside p must change: x.next must become y and y.prev must become x. Pointers inside p may stay as they are.

- (D) x.next = y; y.prev = x. Both directions skip p. **Correct.**
- (B) sets y.prev = y (a self-loop) — backward traversal from y loops forever.
- (C) fixes y.prev = x but never changes x.next, so forward traversal still reaches p; then it rewires p's own pointer, which does not help.
- (A) fixes x.next = y but then only changes p.next (to y again); y.prev still points to p.

**Trap:** in (A) it *looks* like two pointers are updated, but only one of them belongs to a neighbour. Always check that both x.next and y.prev change.

Cost: O(1) given p — the key advantage of a doubly linked list over a singly linked one, which needs the predecessor.''',
            'verify': '''
class N:
    def __init__(s, v): s.v, s.prev, s.next = v, None, None
def make():
    ns = [N(c) for c in "wxpyz"]
    for a, b in zip(ns, ns[1:]): a.next, b.prev = b, a
    return ns
def ok(stmt):
    ns = make(); p = ns[2]
    exec(stmt, {"p": p})
    fw, n = [], ns[0]
    for _ in range(10):
        if n is None: break
        fw.append(n.v); n = n.next
    bw, n = [], ns[-1]
    for _ in range(10):
        if n is None: break
        bw.append(n.v); n = n.prev
    return fw == list("wxyz") and bw == list("zyxw")
opts = {"D": "p.prev.next = p.next; p.next.prev = p.prev",
        "B": "p.prev.next = p.next; p.next.prev = p.next",
        "C": "p.next.prev = p.prev; p.prev = p.next",
        "A": "p.prev.next = p.next; p.next = p.prev.next"}
assert [k for k in opts if ok(opts[k])] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Graphs — BFS distances',
            'text': 'The undirected graph shown is a 3 × 4 grid with one extra diagonal edge A–F. The number of vertices whose shortest-path distance (in edges) from A is exactly 2 is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['E', 'F'],
                        ['F', 'G'],
                        ['G', 'H'],
                        ['I', 'J'],
                        ['J', 'K'],
                        ['K', 'L'],
                        ['A', 'E'],
                        ['E', 'I'],
                        ['B', 'F'],
                        ['F', 'J'],
                        ['C', 'G'],
                        ['G', 'K'],
                        ['D', 'H'],
                        ['H', 'L'],
                        ['A', 'F'],
                    ],
                    'pos': {
                        'A': [0, 4],
                        'B': [2, 4],
                        'C': [4, 4],
                        'D': [6, 4],
                        'E': [0, 2],
                        'F': [2, 2],
                        'G': [4, 2],
                        'H': [6, 2],
                        'I': [0, 0],
                        'J': [2, 0],
                        'K': [4, 0],
                        'L': [6, 0],
                    },
                },
            ],
            'answer': '4',
            'solution': '''**Concept.** BFS from A labels each vertex with its hop distance. The diagonal A–F pulls F one step closer, which in turn pulls F's neighbours closer.

Level by level:
- Distance 0: A.
- Distance 1: neighbours of A → B, E, F (F via the diagonal).
- Distance 2: new neighbours of B (C), of E (I) and of F (G, J) → C, G, I, J.
- Distance 3: D (from C), H (from G), K (from G or J).
- Distance 4: L.

Exactly **4** vertices (C, G, I, J) are at distance 2. Without the diagonal, the distance-2 set would be {C, F, I} — 3 vertices — and G, J would be at distance 3.

**Trap:** K looks 'two squares away' diagonally from F, but grid moves are only along drawn edges: K's neighbours G, J, L are all at distance ≥ 2, so K is at 3.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'D'],
                        ['E', 'F'],
                        ['F', 'G'],
                        ['G', 'H'],
                        ['I', 'J'],
                        ['J', 'K'],
                        ['K', 'L'],
                        ['A', 'E'],
                        ['E', 'I'],
                        ['B', 'F'],
                        ['F', 'J'],
                        ['C', 'G'],
                        ['G', 'K'],
                        ['D', 'H'],
                        ['H', 'L'],
                        ['A', 'F'],
                    ],
                    'pos': {
                        'A': [0, 4],
                        'B': [2, 4],
                        'C': [4, 4],
                        'D': [6, 4],
                        'E': [0, 2],
                        'F': [2, 2],
                        'G': [4, 2],
                        'H': [6, 2],
                        'I': [0, 0],
                        'J': [2, 0],
                        'K': [4, 0],
                        'L': [6, 0],
                    },
                    'highlight': ['C', 'G', 'I', 'J'],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'E'],
                        ['A', 'F'],
                        ['B', 'C'],
                        ['E', 'I'],
                        ['F', 'G'],
                        ['F', 'J'],
                    ],
                    'caption': 'BFS tree edges (red) up to level 2; level-2 vertices highlighted',
                },
            ],
            'verify': '''
from collections import deque
E = [("A","B"),("B","C"),("C","D"),("E","F"),("F","G"),("G","H"),("I","J"),("J","K"),("K","L"),
     ("A","E"),("E","I"),("B","F"),("F","J"),("C","G"),("G","K"),("D","H"),("H","L"),("A","F")]
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
            'topic': 'Quicksort — worst-case comparisons',
            'text': 'Quicksort always picks the **first** element of the current sub-array as the pivot, and partitioning a sub-array of m elements makes exactly m − 1 key comparisons. Sub-arrays of size 0 or 1 are not partitioned. The total number of key comparisons made when sorting the already-sorted array [1, 2, 3, 4, 5, 6, 7, 8] is',
            'options': ['28', '36', '24', '17'],
            'answer': 'A',
            'solution': '''**Concept.** With the first element as pivot, a sorted array gives the most unbalanced split possible: the pivot is the minimum, the left part is empty and the right part has m − 1 elements. T(m) = T(m − 1) + (m − 1).

Partition sizes: 8, 7, 6, 5, 4, 3, 2 (the final size-1 sub-array is not partitioned).
Comparisons: 7 + 6 + 5 + 4 + 3 + 2 + 1 = 28 = 8·7/2 → (A).

- (B) 36 = 9·8/2 counts one extra level.
- (C) 24 ≈ n log₂ n is the balanced (best-case-like) estimate.
- (D) 17 is merge sort's worst case for n = 8, not quicksort's.

**Trap:** sorted (or reverse-sorted) input is the *worst* case for naive pivot choice; randomised or median-of-three pivots avoid it.''',
            'verify': '''ANSWER = {'C': 'A', 'A': 'C'}.get(ANSWER, ANSWER)

c = [0]
def qs(a):
    if len(a) <= 1: return a
    p = a[0]; c[0] += len(a) - 1
    return qs([x for x in a[1:] if x < p]) + [p] + qs([x for x in a[1:] if x >= p])
assert qs(list(range(1, 9))) == list(range(1, 9)) and c[0] == 28 and ANSWER == "C"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — nested comprehensions and zip',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''M = [[i * j for j in range(1, 5)] for i in range(1, 4)]
T = list(zip(*M))
print(sum(T[2]) - sum(M[1]))''',
            'answer': '-2',
            'solution': '''**Concept.** The outer comprehension variable (i) selects the row; the inner one (j) the column. `zip(*M)` transposes M: T[c] is the tuple of column c.

- M = [[1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12]] (3 rows × 4 columns).
- T = [(1, 2, 3), (2, 4, 6), (3, 6, 9), (4, 8, 12)].
- T[2] = (3, 6, 9) → sum 18.
- M[1] = [2, 4, 6, 8] → sum 20.

Printed value: 18 − 20 = **−2**.

**Trap:** reading the comprehension 'inside out' gives a 4 × 3 matrix, and then T[2] would be a row of length 4. Remember: the **leftmost** `for` in a nested comprehension of lists builds the outer list.''',
            'verify': 'assert int(OUTPUT) == int(ANSWER)',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — worst-case probes',
            'text': 'Standard binary search (each probe compares x with A[mid], mid = ⌊(lo + hi)/2⌋, and either stops or discards the half that cannot contain x) is run on a sorted array of 1000 distinct keys. The maximum number of probes over all possible search keys x (present or absent) is',
            'options': ['9', '11', '10', '500'],
            'answer': 'C',
            'solution': '''**Concept.** After a probe on a range of size m, the larger remaining part has size ⌊m/2⌋. The worst-case number of probes W(m) satisfies W(m) = 1 + W(⌊m/2⌋), W(0) = 0, giving W(m) = ⌊log₂ m⌋ + 1.

For m = 1000: sizes 1000 → 500 → 250 → 125 → 62 → 31 → 15 → 7 → 3 → 1 → 0, i.e. 10 probes. Equivalently ⌊log₂ 1000⌋ + 1 = 9 + 1 = **10** → (C).

- (A) 9 = ⌊log₂ 1000⌋ forgets the final probe on a one-element range.
- (B) 11 = ⌈log₂ 1000⌉ + 1 over-counts.
- (D) 500 is linear search's average, not binary search.

**Tip:** the decision tree of binary search on n keys has height ⌊log₂ n⌋, and an unsuccessful search needs at most ⌊log₂ n⌋ + 1 probes.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

A = list(range(0, 2000, 2)); worst = 0
for x in range(-1, 2001):
    lo, hi, p = 0, len(A) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2; p += 1
        if A[mid] == x: break
        if A[mid] < x: lo = mid + 1
        else: hi = mid - 1
    worst = max(worst, p)
assert worst == 10 and ANSWER == "B"
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — class vs instance attributes',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Counter:
    hits = []
    total = 0

    def __init__(self, name):
        self.name = name

    def hit(self, k):
        self.hits.append(k)
        self.total += k

a, b = Counter("a"), Counter("b")
a.hit(3)
b.hit(4)
a.hit(5)
print(len(a.hits), a.total, b.total, Counter.total)''',
            'options': ['`3 8 4 12`', '`2 8 4 0`', '`3 8 4 0`', '`3 12 12 12`'],
            'answer': 'C',
            'solution': '''**Concept.** Attribute *lookup* through an instance falls back to the class, but attribute *assignment* through an instance creates/updates an **instance** attribute. Mutating a class-level list through `self` mutates the one shared list.

- `self.hits.append(k)`: looks up `hits` → finds the class list (no instance attribute) → appends to the **shared** list. After three calls it holds [3, 4, 5]; `len(a.hits)` = 3.
- `self.total += k` means `self.total = self.total + k`. The right side reads the class value 0 the first time; the assignment then creates an instance attribute.
  - a.hit(3): a.total = 0 + 3 = 3.
  - b.hit(4): b.total = 0 + 4 = 4.
  - a.hit(5): a.total = 3 + 5 = 8 (now read from the instance).
- `Counter.total` was never assigned → still 0.

Output: `3 8 4 0` → (C).

- (A) assumes `+=` writes back to the class.
- (B) treats `hits` as per-instance.
- (D) treats `total` as shared like `hits`.

**Trap:** `+=` on an immutable int rebinds; `.append` on a list mutates. The same `self.x` syntax behaves differently.''',
            'verify': "ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '3 8 4 0'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — successive insertions into a max-heap',
            'text': 'The keys 15, 22, 9, 40, 31, 27, 50, 12 are inserted one at a time, in this order, into an initially empty binary max-heap stored in an array (0-based). Each insertion appends the key and sifts it up, swapping with its parent while the parent is smaller. Which of the following statements is/are TRUE?',
            'options': [
                'Inserting 50 causes exactly 2 swaps',
                'The final array is [50, 31, 40, 15, 22, 9, 27, 12]',
                'In the final heap, 40 is the left child of the root',
                'The total number of swaps over all insertions is 7',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** Insertion places the key at the next free leaf and sifts it up; the number of swaps is at most the depth of that leaf.

Trace (array after each insertion, swaps in brackets):
- 15 → [15] (0)
- 22 → [15, 22] → swap with 15 → [22, 15] (1)
- 9 → [22, 15, 9] (0)
- 40 → index 3, parent 15 → swap → index 1, parent 22 → swap → [40, 22, 9, 15] (2)
- 31 → index 4, parent 22 → swap → index 1, parent 40 stop → [40, 31, 9, 15, 22] (1)
- 27 → index 5, parent 9 → swap → index 2, parent 40 stop → [40, 31, 27, 15, 22, 9] (1)
- 50 → index 6, parent 27 → swap → index 2, parent 40 → swap → [50, 31, 40, 15, 22, 9, 27] (2)
- 12 → index 7, parent 15 → stop → [50, 31, 40, 15, 22, 9, 27, 12] (0)

Total swaps = 1 + 2 + 1 + 1 + 2 = 7.

- (A) **True.**
- (B) **True.**
- (C) **False** — 40 is at index 2, the **right** child of the root; 31 is the left child.
- (D) **True.**

**Trap:** repeated insertion and bottom-up build-heap generally produce *different* heaps from the same keys; do not mix the two procedures.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [50, 31, 40, 15, 22, 9, 27, 12],
                    'caption': 'Final max-heap',
                },
            ],
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

h, sw, per = [], 0, {}
for k in [15, 22, 9, 40, 31, 27, 50, 12]:
    h.append(k); i = len(h) - 1; c = 0
    while i > 0 and h[(i-1)//2] < h[i]:
        h[(i-1)//2], h[i] = h[i], h[(i-1)//2]; i = (i-1)//2; c += 1
    per[k] = c; sw += c
truth = {"A": h == [50,31,40,15,22,9,27,12], "B": sw == 7, "C": per[50] == 2, "D": h[1] == 40}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Graphs — DFS timestamps and edge classification',
            'text': 'DFS is run on the directed graph shown, starting at A; adjacency lists are in alphabetical order, and a single clock is incremented at every discovery and every finish (so A is discovered at time 1). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'B'],
                        ['C', 'E'],
                        ['D', 'A'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['F', 'C'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 3],
                        'C': [2, 1],
                        'D': [4, 3],
                        'E': [4, 0],
                        'F': [5, 1.6],
                    },
                },
            ],
            'options': [
                'Exactly 3 edges are back edges',
                'C is discovered at time 5 and finished at time 8',
                'A → C is a forward edge',
                'C → B is a cross edge',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** For an edge u → v met during DFS: v undiscovered → tree edge; v discovered but not finished (on the recursion stack) → back edge; v finished and d[u] < d[v] → forward edge; v finished and d[u] > d[v] → cross edge.

Trace:
- A (d 1) → B (d 2) → D (d 3). D → A: A active → **back**. D → F: F (d 4).
- F → C: C (d 5). C → B: B active → **back**. C → E: E (d 6). E → F: F active → **back**. E finishes (7). C finishes (8). F finishes (9). D finishes (10). B finishes (11).
- A → C: C already finished and d[A] = 1 < d[C] = 5 → **forward**. A finishes (12).

Tree edges: A→B, B→D, D→F, F→C, C→E. Back: D→A, C→B, E→F. Forward: A→C. No cross edges.

- (A) **True** — three back edges.
- (B) **True** — d[C] = 5, f[C] = 8.
- (C) **True.**
- (D) **False** — when C → B is examined, B is still on the stack (it finishes at 11), so it is a back edge.

**Trap:** B was discovered long before C, which tempts one to call C → B a cross edge; the deciding test is whether B is still active.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = {'A': ['B','C'], 'B': ['D'], 'C': ['B','E'], 'D': ['A','F'], 'E': ['F'], 'F': ['C']}
t = [0]; d = {}; f = {}; cls = {}
def dfs(u):
    t[0] += 1; d[u] = t[0]
    for v in E[u]:
        if v not in d: cls[(u, v)] = 'T'; dfs(v)
        elif v not in f: cls[(u, v)] = 'B'
        elif d[u] < d[v]: cls[(u, v)] = 'F'
        else: cls[(u, v)] = 'C'
    t[0] += 1; f[u] = t[0]
dfs('A')
truth = {"A": list(cls.values()).count('B') == 3, "B": cls[('C','B')] == 'C',
         "C": (d['C'], f['C']) == (5, 8), "D": cls[('A','C')] == 'F'}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recurrences — exact evaluation with floors',
            'text': 'Let T(1) = 1 and T(n) = 2·T(⌊n/2⌋) + n for n ≥ 2. The value of T(20) is ______.',
            'answer': '92',
            'solution': '''**Concept.** This is the merge-sort-style recurrence; asymptotically T(n) = Θ(n log n), but with floors the exact value must be computed by unwinding.

- T(2) = 2·T(1) + 2 = 4
- T(5) = 2·T(2) + 5 = 13
- T(10) = 2·T(5) + 10 = 36
- T(20) = 2·T(10) + 20 = **92**

Sanity check against the power-of-two closed form T(2^{k}) = 2^{k}(k + 1): T(16) = 16 × 5 = 80 and T(32) = 32 × 6 = 192, and 80 < 92 < 192 as expected for a non-decreasing function.

**Trap:** using n log₂ n + n = 20 × 4.32 + 20 ≈ 106 — the closed form holds only for powers of two. Another slip is T(5) = 2·T(2.5): floors must be applied.''',
            'verify': '''
from functools import lru_cache
@lru_cache(None)
def T(n): return 1 if n == 1 else 2 * T(n // 2) + n
assert T(20) == int(ANSWER) and T(16) == 80
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Hashing — deletion with tombstones',
            'text': 'A hash table of size 10 uses h(k) = k mod 10 with linear probing. Keys 31, 41, 51, 22, 62 are inserted in that order. Then 41 is deleted by marking its slot DELETED (a tombstone). A search probes until it finds the key or an EMPTY slot (tombstones are skipped over). An insertion places the key in the first slot of its probe sequence that is EMPTY or DELETED. Which of the following statements is/are TRUE? (A probe = one slot examined.)',
            'options': [
                'If 71 is then inserted, it is placed in slot 2',
                'Searching for 51 after the deletion examines exactly 3 slots',
                'If slot 2 had instead been simply set to EMPTY, a search for 22 would still succeed',
                'An unsuccessful search for 72 after the deletion examines exactly 5 slots',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** In open addressing, deleting by emptying a slot can break the probe chains of keys inserted after it. A tombstone keeps chains intact for searches and can be reused by insertions.

Insertions: 31 → 1; 41 → 1 full → 2; 51 → 1, 2 full → 3; 22 → 2, 3 full → 4; 62 → 2, 3, 4 full → 5. Delete 41 → slot 2 = DEL.

- (A) Insert 71: home 1 occupied, slot 2 is DELETED → 71 goes into slot 2. **True.**
- (B) Search 51: slot 1 (31), slot 2 (DEL, continue), slot 3 (51) → 3 probes. **True.**
- (C) Search 22 with slot 2 EMPTY: the home slot 2 is empty → search stops and **fails**, although 22 is in slot 4. **False.**
- (D) Search 72: home 2 (DEL), 3 (51), 4 (22), 5 (62), 6 (EMPTY) → 5 probes. **True.**

**Trap:** (C) is exactly why tombstones exist; many students assume emptying the slot is harmless.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        1: 31,
                        2: 'DEL',
                        3: 51,
                        4: 22,
                        5: 62,
                    },
                    'caption': 'Table after deleting 41 (tombstone in slot 2)',
                },
            ],
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

EMPTY, DEL = None, "DEL"
T = [EMPTY]*10
def probe(k):
    i = k % 10
    for _ in range(10): yield i; i = (i + 1) % 10
for k in [31, 41, 51, 22, 62]:
    for i in probe(k):
        if T[i] is EMPTY: T[i] = k; break
T[T.index(41)] = DEL
def search(T, k):
    n = 0
    for i in probe(k):
        n += 1
        if T[i] is EMPTY: return False, n
        if T[i] == k: return True, n
    return False, n
U = T[:]
for i in probe(71):
    if U[i] is EMPTY or U[i] == DEL: U[i] = 71; break
V = T[:]; V[2] = EMPTY
truth = {"A": search(T, 51) == (True, 3), "B": search(T, 72) == (False, 5),
         "C": U[2] == 71, "D": search(V, 22)[0]}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Graphs — counting topological orderings',
            'text': 'The number of distinct topological orderings of the directed acyclic graph shown is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'D'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['E', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [4, 2],
                        'D': [1, 1],
                        'E': [3, 1],
                        'F': [2, 0],
                        'G': [4, 0],
                    },
                },
            ],
            'answer': '42',
            'solution': '''**Concept.** Count linear extensions by splitting on structure: here F must come after D and E; G only after E; D after A, B; E after B, C.

**Step 1 — orders of A, B, C, D, E** (F comes after all of them except possibly G, so place F last among these six). Constraints: A, B before D; B, C before E. The last of the five must be D or E:
- Last = E: arrange A, B, D with D after A and B (2 ways: ABD, BAD), then insert C in any of 4 gaps → 8 orders. Here E is in position 5.
- Last = D: symmetric — arrange B, C, E with E last (2 ways), insert A in any of 4 gaps → 8 orders. In 6 of them A is inserted before E (E in position 4); in 2 of them A is inserted after E (B, C, E, A, D and C, B, E, A, D: E in position 3).
- Total 16 orders; appending F gives 16 orders of the six vertices A–F.

**Step 2 — insert G.** G's only constraint is that it follows E (it has no successors), so in a six-vertex order with E at position p it can go into any of the 7 − p gaps after E:
- E at position 5 (8 orders): 2 gaps → 16.
- E at position 4 (6 orders): 3 gaps → 18.
- E at position 3 (2 orders): 4 gaps → 8.
- Total = 16 + 18 + 8 = **42**.

**Trap:** forgetting that G is a sink with a single predecessor, so it can float anywhere after E — including after F.''',
            'verify': '''
import itertools
V = "ABCDEFG"
ED = [("A","D"),("B","D"),("B","E"),("C","E"),("D","F"),("E","F"),("E","G")]
cnt = sum(1 for p in itertools.permutations(V)
          if all(p.index(u) < p.index(v) for u, v in ED))
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Stacks — monotonic stack (next greater element)',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def nge(a):
    res, st = [-1] * len(a), []
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res

print(nge([4, 9, 2, 5, 3, 8, 1, 7]))''',
            'options': [
                '`[9, -1, 5, 8, 8, -1, 7, 7]`',
                '`[9, -1, 5, 8, 8, -1, 7, -1]`',
                '`[9, -1, 5, 9, 8, -1, 7, -1]`',
                '`[9, -1, 5, 8, 5, -1, 7, -1]`',
            ],
            'answer': 'B',
            'solution': '''**Concept.** The stack holds indices whose next greater element has not been seen; their values are non-increasing from bottom to top. A new x pops (and resolves) every smaller value on top. Each index is pushed and popped at most once → O(n).

Trace (stack shows values):
- 4: push → [4]
- 9: pops 4 (res[0] = 9) → [9]
- 2: push → [9, 2]
- 5: pops 2 (res[2] = 5) → [9, 5]
- 3: push → [9, 5, 3]
- 8: pops 3 (res[4] = 8), pops 5 (res[3] = 8) → [9, 8]
- 1: push → [9, 8, 1]
- 7: pops 1 (res[6] = 7); 8 > 7 stops → [9, 8, 7]
- End: 9, 8, 7 remain → −1.

Result `[9, -1, 5, 8, 8, -1, 7, -1]` → (B).

- (A) gives the last element a next-greater of itself.
- (C) assigns 9 to the 5 — but 8 appears first to its right.
- (D) gives 3 the value 5, which is to its **left**.

**Trap:** the answer for 5 is the *first* greater element to the right (8), not the maximum to the right (9).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [9, 8, 7],
                    'label': 'end',
                    'caption': 'Values left on the stack at the end (answer −1)',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

a = [4, 9, 2, 5, 3, 8, 1, 7]
brute = [next((y for y in a[i+1:] if y > a[i]), -1) for i in range(len(a))]
assert OUTPUT.strip() == str(brute) == '[9, -1, 5, 8, 8, -1, 7, -1]'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merge sort and quicksort — exact comparison counts',
            'text': 'Assume quicksort uses the Lomuto partition with the **last** element as pivot (partitioning m elements costs m − 1 comparisons, and elements equal to the pivot go to the left part), and merge sort splits into ⌊n/2⌋ and ⌈n/2⌉ elements and stops comparing once a side is exhausted. Which of the following statements is/are TRUE?',
            'options': [
                'Quicksort on 5 equal keys [4, 4, 4, 4, 4] makes exactly 10 comparisons',
                "If merge sort's merge takes from the right list whenever L[i] == R[j], it is still stable",
                'Merge sort on the sorted array [1, 2, …, 8] makes exactly 12 comparisons',
                'Quicksort on [3, 1, 2] makes exactly 3 comparisons',
            ],
            'answer': ['A', 'C'],
            'solution': '''**Concept.** Exact counts depend on how the splits fall. All-equal keys are a worst case for Lomuto (every key ≤ pivot), while sorted input is a best case for merge sort's merging.

- (A) Equal keys: the pivot ends up at the far right every time, leaving m − 1 keys on the left. Comparisons 4 + 3 + 2 + 1 = 10. **True.**
- (B) Taking the right element on ties puts later equal keys before earlier ones → **not stable**. **False.**
- (C) Sorted input: every merge of sizes p = q stops after p comparisons (left list empties first). Level 1: 4 merges × 1 = 4; level 2: 2 × 2 = 4; level 3: 1 × 4 = 4 → 12. **True.**
- (D) [3, 1, 2], pivot 2: 2 comparisons → [1, 2, 3], pivot index 1; the left part [1] and right part [3] have size 1 → no more comparisons. Total **2**. **False.**

**Trap:** for (D), counting one comparison for the pivot with itself. For (B), stability lives entirely in the tie-breaking rule of the merge.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

c = [0]
def qs(A, lo, hi):
    if lo >= hi: return
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        c[0] += 1
        if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
    A[i+1], A[hi] = A[hi], A[i+1]
    qs(A, lo, i); qs(A, i + 2, hi)
def qcount(A):
    c[0] = 0; A = A[:]; qs(A, 0, len(A) - 1); return c[0]
m = [0]
def ms(a, tie_right=False):
    if len(a) <= 1: return a
    k = len(a) // 2; L, R = ms(a[:k], tie_right), ms(a[k:], tie_right); o = []; i = j = 0
    while i < len(L) and j < len(R):
        m[0] += 1
        if L[i][0] < R[j][0] or (L[i][0] == R[j][0] and not tie_right): o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
m[0] = 0; ms([(v, 0) for v in range(1, 9)]); merge12 = m[0] == 12
out = ms([(1, 'a'), (1, 'b')], tie_right=True); stable = [t for _, t in out] == ['a', 'b']
truth = {"A": qcount([4]*5) == 10, "B": merge12, "C": stable, "D": qcount([3, 1, 2]) == 3}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': "Linked lists — Floyd's cycle detection",
            'text': "Consider the following Python program, which builds an 11-node list whose last node points back to node 3, and then runs Floyd's cycle-finding algorithm. The program prints two numbers. The **first** number printed is ______.",
            'code': '''class Node:
    def __init__(self, v):
        self.v, self.nxt = v, None

nodes = [Node(i) for i in range(11)]
for a, b in zip(nodes, nodes[1:]):
    a.nxt = b
nodes[-1].nxt = nodes[3]

slow = fast = nodes[0]
steps = 0
while True:
    slow, fast = slow.nxt, fast.nxt.nxt
    steps += 1
    if slow is fast:
        break
p = nodes[0]
while p is not slow:
    p, slow = p.nxt, slow.nxt
    steps += 1
print(steps, p.v)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [0, 1, 2, 3, 4, '…', 9, 10],
                    'caption': 'Nodes 0 → 1 → … → 10, and 10 → 3 (cycle of length 8)',
                },
            ],
            'answer': '11',
            'solution': '''**Concept.** Let μ be the tail length (nodes before the cycle) and λ the cycle length. Here μ = 3 (nodes 0, 1, 2) and λ = 8 (nodes 3 … 10). After k steps slow is at position k and fast at 2k; they meet at the first k ≥ μ with k ≡ 0 (mod λ). Then a pointer from the head and one from the meeting point, moving one step at a time, meet exactly at the cycle start after μ steps.

Phase 1: smallest k ≥ 3 divisible by 8 → k = 8. Check: slow at node 8; fast has moved 16 steps: 0→10 is 10 steps, then 6 more around the cycle 3, 4, …: 10 → 3 → 4 → 5 → 6 → 7 → 8. ✓ steps = 8.

Phase 2: p from node 0 and slow from node 8 advance together: (1, 9), (2, 10), (3, 3) → 3 more steps; they meet at node 3, the cycle start.

Total steps = 8 + 3 = **11**; the program prints `11 3`.

**Trap:** assuming the pointers meet at the cycle start in phase 1, or that phase 1 takes exactly λ − μ steps. In general phase 1 takes λ·⌈μ/λ⌉ steps (or λ if μ = 0).''',
            'verify': "assert OUTPUT.split() == ['11', '3'] and int(ANSWER) == 11",
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary search trees — insertion orders giving the same tree',
            'text': 'How many permutations of the keys {20, 30, 35, 40, 50, 60, 70, 80}, when inserted in that order into an initially empty BST, produce exactly the BST shown?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        50,
                        [
                            30,
                            [20],
                            [
                                40,
                                [35],
                                None,
                            ],
                        ],
                        [
                            70,
                            [60],
                            [80],
                        ],
                    ],
                    'caption': 'Target BST',
                },
            ],
            'options': ['35', '105', '420', '210'],
            'answer': 'D',
            'solution': '''**Concept.** A permutation yields the given BST iff the root comes first and, recursively, the keys of each subtree appear in an order that builds that subtree. Keys of the left and right subtrees may be **interleaved** arbitrarily. So N(T) = C(|L| + |R|, |L|) · N(L) · N(R).

- Right subtree {70, 60, 80}: 70 first, then 60 and 80 in either order → N = 2.
- Left subtree {30, 20, 40, 35}: 30 first; then interleave {20} with the sequence (40 before 35): C(3, 1) · 1 · 1 = 3 → N = 3.
- Whole tree: 50 first, then interleave 4 left keys with 3 right keys: C(7, 4) = 35.

N = 35 × 3 × 2 = **210** → (D).

- (A) 35 counts only the interleavings at the root.
- (B) 105 forgets the factor 2 for the right subtree.
- (C) 420 also lets 35 precede 40 (impossible: 35 must hang below 40).

**Trap:** the subtree root must precede all its descendants, but keys from different subtrees impose no order on each other.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

import itertools
def build(seq):
    t = None
    def ins(t, k):
        if t is None: return (k, None, None)
        if k < t[0]: return (t[0], ins(t[1], k), t[2])
        return (t[0], t[1], ins(t[2], k))
    for k in seq: t = ins(t, k)
    return t
L = lambda k: (k, None, None)
target = (50, (30, L(20), (40, L(35), None)), (70, L(60), L(80)))
cnt = sum(1 for p in itertools.permutations([20, 30, 35, 40, 50, 60, 70, 80]) if build(p) == target)
assert cnt == 210 and ANSWER == "A"
''',
        },
    ],
}
