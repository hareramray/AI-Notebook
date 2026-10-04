# Set 01 — Foundations I (Python basics, lists, strings, slicing, arrays)

SET = {
    'number': 1,
    'title': 'Foundations I',
    'difficulty': 'Moderate',
    'focus': 'Python basics, lists, strings, slicing, arrays',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing with negative steps',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "DATASCIENCE"
print(s[-2:-9:-3], s[::4])''',
            'options': ['`EIA DSN`', '`CIAT DSN`', '`CIA DSN`', '`CIA DSNE`'],
            'answer': 'C',
            'solution': '''A slice `s[start:stop:step]` begins at `start`, moves by `step`, and stops *before* reaching `stop`. Negative indices are first converted by adding `len(s)`.

Indices of `"DATASCIENCE"` (length 11): D0 A1 T2 A3 S4 C5 I6 E7 N8 C9 E10.

- `s[-2:-9:-3]`: start = 11 − 2 = 9, stop = 11 − 9 = 2 (exclusive), step −3. Visited indices 9, 6, 3 → `C`, `I`, `A`. The next index would be 0, which is past the stop (2), so the result is `CIA`.
- `s[::4]`: indices 0, 4, 8 → `D`, `S`, `N` → `DSN` (index 12 is out of range).

Output: `CIA DSN`.

- (A) starts at index 10 (`E`) — that would be `s[-1:...]`.
- (B) wrongly includes index 2 — the stop index is never included.
- (D) appends `E` as if index 12 wrapped around; slices never wrap.

**Trap:** with a negative step, the stop bound is still exclusive; convert negative indices to positive ones before tracing.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

s = "DATASCIENCE"
assert OUTPUT.strip() == 'CIA DSN'
assert ANSWER == 'A'
assert s[-2:-9:-3] + ' ' + s[::4] == 'CIA DSN'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — aliasing, += versus +',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''a = [1, 2, 3]
b = a
c = a[:]
b += [4]
c.append(5)
a = a + [6]
b.extend(c)
print(len(a) + len(b) + len(c))''',
            'answer': '17',
            'solution': '''Key idea: `b = a` creates an **alias** (two names, one list); `a[:]` creates a **shallow copy**; `b += [4]` mutates the list in place (it calls `list.__iadd__`), while `a = a + [6]` builds a **new** list and rebinds only the name `a`.

- After line 3: `a`, `b` → list L1 = [1, 2, 3]; `c` → L2 = [1, 2, 3].
- `b += [4]`: L1 becomes [1, 2, 3, 4] (seen through both `a` and `b`).
- `c.append(5)`: L2 = [1, 2, 3, 5].
- `a = a + [6]`: new list L3 = [1, 2, 3, 4, 6]; `a` now names L3, `b` still names L1.
- `b.extend(c)`: L1 = [1, 2, 3, 4, 1, 2, 3, 5] (length 8).

Lengths: len(a) = 5, len(b) = 8, len(c) = 4, sum = **17**.

**Trap:** treating `a = a + [6]` like `+=` gives len(b) = 9 and the answer 18; treating `c = a[:]` as an alias makes `c` grow too.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — operation trace',
            'text': '''The stack S below is shown bottom → top. POP() removes and returns the top, TOP() returns the top without removing it, and in an expression the operands are evaluated left to right. The following operations are executed in order:

- 1. PUSH(POP() × 3)
- 2. PUSH(POP() + POP())
- 3. PUSH(8)
- 4. t = POP(); PUSH(POP() − t)
- 5. PUSH(TOP() × TOP())

The final contents of S, bottom → top, are''',
            'diagrams': [
                {
                    'type': 'stack',
                    'values': [4, 9, 2],
                    'label': 'S',
                    'caption': 'Initial stack (top = 2)',
                },
            ],
            'options': ['4, 7, 14', '4, 7, 49', '4, −7, 49', '4, 15, 8, 49'],
            'answer': 'B',
            'solution': '''Simulate carefully, remembering that TOP() does **not** remove anything.

- Start: [4, 9, 2].
- Op 1: POP() = 2, push 6 → [4, 9, 6].
- Op 2: POP() = 6, POP() = 9, push 15 → [4, 15].
- Op 3: push 8 → [4, 15, 8].
- Op 4: t = 8; POP() = 15; push 15 − 8 = 7 → [4, 7].
- Op 5: TOP() = 7 twice (no removal), push 49 → [4, 7, 49].

Option analysis:

- (A) treats TOP() × TOP() as 7 + 7 or as 2 × TOP(); wrong.
- (B) 4, 7, 49 — matches the trace. **Correct.**
- (C) computes t − POP() = 8 − 15 = −7 in step 4 (operand order reversed).
- (D) forgets that op 4 pops two elements and pushes one.

**Tip:** for non-commutative operations (−, ÷) write down which popped value is the left operand; it is the classic source of errors in postfix evaluation too.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [4, 7, 49],
                    'label': 'S',
                    'caption': 'Final stack',
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

S = [4, 9, 2]
S.append(S.pop() * 3)
x = S.pop(); y = S.pop(); S.append(x + y)
S.append(8)
t = S.pop(); S.append(S.pop() - t)
S.append(S[-1] * S[-1])
assert S == [4, 7, 49] and ANSWER == 'C'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — pointer manipulation',
            'text': 'The singly linked list shown is built and the program below is run on it. What is printed?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 8, 1, 6, 4],
                    'head': 'head',
                },
            ],
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.next = v, nxt

head = None
for v in [4, 6, 1, 8, 3]:
    head = Node(v, head)

p = head
while p.next and p.next.next:
    p.next = p.next.next
    p = p.next

out, q = [], head
while q:
    out.append(q.v)
    q = q.next
print(out)''',
            'options': ['`[3, 1, 4]`', '`[3, 8, 1]`', '`[8, 6]`', '`[3, 1, 6, 4]`'],
            'answer': 'A',
            'solution': '''Building by inserting at the head in the order 4, 6, 1, 8, 3 yields 3 → 8 → 1 → 6 → 4 (the reverse of the insertion order), as in the figure.

The loop *bypasses* the node after `p` and then jumps to the node that follows it:

- p = 3: p.next (8) and p.next.next (1) exist → 3.next = 1; p = 1.
- p = 1: p.next (6) and p.next.next (4) exist → 1.next = 4; p = 4.
- p = 4: p.next is None → loop ends.

The list is now 3 → 1 → 4; output `[3, 1, 4]` → (A). Every node at an odd position (2nd, 4th, …) has been unlinked.

- (B) keeps the first three nodes — that is truncation, not alternate deletion.
- (C) lists the deleted nodes.
- (D) assumes only one bypass happens.

**Trap:** forgetting that head insertion reverses the order of the input loop.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 1, 4],
                    'head': 'head',
                    'caption': 'After the loop',
                },
            ],
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[3, 1, 4]' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — probe trace',
            'text': 'Iterative binary search with `lo = 0`, `hi = 12`, `mid = (lo + hi) // 2`, `lo = mid + 1` if `A[mid] < key`, `hi = mid − 1` if `A[mid] > key`, and termination when `lo > hi`, is used to search for key **47** in the sorted array A below. The sum of all array elements that are compared with the key is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [3, 8, 12, 17, 21, 26, 30, 34, 41, 45, 52, 58, 63],
                    'label': 'A',
                },
            ],
            'answer': '185',
            'solution': '''Binary search halves the live interval [lo, hi] each step; an unsuccessful search stops when the interval becomes empty.

- lo = 0, hi = 12 → mid = 6, A[6] = 30 < 47 → lo = 7.
- lo = 7, hi = 12 → mid = 9, A[9] = 45 < 47 → lo = 10.
- lo = 10, hi = 12 → mid = 11, A[11] = 58 > 47 → hi = 10.
- lo = 10, hi = 10 → mid = 10, A[10] = 52 > 47 → hi = 9.
- lo = 10 > hi = 9 → stop (not found).

Probed elements: 30, 45, 58, 52. Sum = 30 + 45 + 58 + 52 = **185**.

Note that 4 = ⌊log₂ 13⌋ + 1 probes is the maximum for n = 13, as expected for a key that falls between two array elements deep in the search tree.

**Trap:** using mid = ⌈(lo+hi)/2⌉ or stopping when lo == hi gives a different set of probes (e.g. missing the final probe of 52).''',
            'verify': '''
A = [3, 8, 12, 17, 21, 26, 30, 34, 41, 45, 52, 58, 63]
lo, hi, s = 0, 12, 0
while lo <= hi:
    m = (lo + hi) // 2
    s += A[m]
    if A[m] == 47: break
    if A[m] < 47: lo = m + 1
    else: hi = m - 1
assert s == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Insertion sort — shifts and comparisons',
            'text': 'Standard insertion sort (for i = 1 … n−1, the key A[i] is compared with A[i−1], A[i−2], … and each larger element is shifted one place right) sorts A = [5, 2, 9, 1, 7, 3] into ascending order. A *comparison* is one evaluation of `A[j] > key`. Which of the following statements is/are TRUE?',
            'options': [
                'The total number of element shifts is 8',
                'The total number of key comparisons is 11',
                'The element 9 is shifted to the right exactly twice',
                'After the iterations i = 1, 2, 3 the array is [1, 2, 5, 9, 7, 3]',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''In insertion sort each shift removes exactly one inversion, so #shifts = #inversions. Comparisons = shifts + one extra comparison for every iteration that stops on a failing test (instead of running off the left end).

- i = 1 (key 2): 5 > 2 shift; reached index 0 → 1 comparison, 1 shift → [2, 5, 9, 1, 7, 3].
- i = 2 (key 9): 5 > 9 false → 1 comparison, 0 shifts.
- i = 3 (key 1): 9, 5, 2 all shift; reached index 0 → 3 comparisons, 3 shifts → [1, 2, 5, 9, 7, 3].
- i = 4 (key 7): 9 shifts, 5 > 7 false → 2 comparisons, 1 shift → [1, 2, 5, 7, 9, 3].
- i = 5 (key 3): 9, 7, 5 shift, 2 > 3 false → 4 comparisons, 3 shifts → sorted.

Totals: shifts = 1 + 0 + 3 + 1 + 3 = 8, comparisons = 1 + 1 + 3 + 2 + 4 = 11.

- (A) TRUE — also equals the inversion count 3 + 1 + 3 + 1 = 8.
- (B) TRUE.
- (C) FALSE — 9 is shifted at i = 3, i = 4 and i = 5, i.e. three times.
- (D) TRUE — see the state after i = 3.

**Tip:** counting inversions is the fastest way to get the number of shifts.''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A = [5, 2, 9, 1, 7, 3]; sh = cmp = 0; moves9 = 0; snap = None
for i in range(1, len(A)):
    key = A[i]; j = i - 1
    while j >= 0:
        cmp += 1
        if A[j] > key:
            if A[j] == 9: moves9 += 1
            A[j + 1] = A[j]; sh += 1; j -= 1
        else: break
    A[j + 1] = key
    if i == 3: snap = A[:]
assert sh == 8 and cmp == 11 and snap == [1, 2, 5, 9, 7, 3] and moves9 == 3
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — linear probing collisions',
            'text': 'The keys 4, 15, 26, 9, 7, 20, 2 are inserted, in that order, into an initially empty hash table with 11 slots (indices 0 … 10) using h(k) = (3k + 1) mod 11 and linear probing (h(k), h(k)+1, … mod 11). A *collision* is counted each time a probed slot is found occupied. The total number of collisions is ______.',
            'answer': '5',
            'solution': '''Compute the home slots first: h(4) = 13 mod 11 = 2, h(15) = 46 mod 11 = 2, h(26) = 79 mod 11 = 2, h(9) = 28 mod 11 = 6, h(7) = 22 mod 11 = 0, h(20) = 61 mod 11 = 6, h(2) = 7.

Keys that differ by a multiple of 11 (4, 15, 26) always share a home slot here, since 3·11 ≡ 0 (mod 11).

- 4 → slot 2 (0 collisions).
- 15 → 2 occupied → slot 3 (1).
- 26 → 2, 3 occupied → slot 4 (2).
- 9 → slot 6 (0).
- 7 → slot 0 (0).
- 20 → 6 occupied → slot 7 (1).
- 2 → home 7, now occupied by 20 → slot 8 (1).

Total collisions = 1 + 2 + 1 + 1 = **5**.

**Trap:** key 2 has home slot 7, which was free originally but has been taken by 20 through probing — secondary effects of primary clustering are easy to miss.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 7,
                        2: 4,
                        3: 15,
                        4: 26,
                        6: 9,
                        7: 20,
                        8: 2,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 11; col = 0
for k in [4, 15, 26, 9, 7, 20, 2]:
    i = (3 * k + 1) % 11
    while T[i] is not None:
        col += 1; i = (i + 1) % 11
    T[i] = k
assert col == int(ANSWER) and T.index(2) == 8
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search trees — traversal',
            'text': 'The keys 40, 25, 61, 18, 33, 52, 70, 29, 36, 55 are inserted in that order into an initially empty binary search tree. The post-order traversal of the resulting tree is',
            'options': [
                '29, 36, 18, 33, 25, 52, 55, 70, 61, 40',
                '18, 25, 29, 33, 36, 40, 52, 55, 61, 70',
                '18, 36, 29, 33, 25, 55, 52, 70, 61, 40',
                '18, 29, 36, 33, 25, 55, 52, 70, 61, 40',
            ],
            'answer': 'D',
            'solution': '''Each insertion walks from the root, going left for smaller keys and right for larger ones. The resulting tree is shown in the solution figure: 40 has children 25 and 61; 25 has 18 and 33; 33 has 29 and 36; 61 has 52 and 70; 52 has right child 55.

Post-order = left subtree, right subtree, root:

- Left subtree of 40: post(18) = 18; post(33-subtree) = 29, 36, 33; then 25 → 18, 29, 36, 33, 25.
- Right subtree of 40: post(52-subtree) = 55, 52; post(70) = 70; then 61 → 55, 52, 70, 61.
- Finally 40.

Result: 18, 29, 36, 33, 25, 55, 52, 70, 61, 40 → (D).

- (A) visits 18 after the 33-subtree and puts 52 before its child 55.
- (B) is the in-order (sorted) sequence.
- (C) swaps 29 and 36 — the left child must come before the right child.
- (D) correct.

**Tip:** in a post-order listing every node appears after all its descendants; use that to eliminate options quickly.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            25,
                            [18],
                            [
                                33,
                                [29],
                                [36],
                            ],
                        ],
                        [
                            61,
                            [
                                52,
                                None,
                                [55],
                            ],
                            [70],
                        ],
                    ],
                    'caption': 'BST after all insertions',
                },
            ],
            'verify': '''
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
T = None
for k in [40, 25, 61, 18, 33, 52, 70, 29, 36, 55]: T = ins(T, k)
assert post(T) == [18, 29, 36, 33, 25, 55, 52, 70, 61, 40] and ANSWER == 'D'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'Consider the following Python program. What is printed?',
            'code': 'print(-17 // 5, -17 % 5, 17 // -5, 17 % -5, int(-17 / 5))',
            'options': ['`-3 -2 -3 2 -3`', '`-4 -2 -3 -3 -3`', '`-4 3 -4 3 -4`', '`-4 3 -4 -3 -3`'],
            'answer': 'D',
            'solution': '''Python's `//` is **floor** division (rounds toward −∞) and `%` is defined so that `a == (a // b) * b + a % b`; hence the remainder takes the sign of the **divisor**. `int()` on a float truncates toward 0.

- −17 // 5 = ⌊−3.4⌋ = −4.
- −17 % 5 = −17 − (−4)(5) = 3.
- 17 // −5 = ⌊−3.4⌋ = −4.
- 17 % −5 = 17 − (−4)(−5) = −3.
- int(−17 / 5) = int(−3.4) = −3.

Output: `-4 3 -4 -3 -3` → (D).

- (A) is what C/Java would print (truncating division).
- (B) mixes the two conventions.
- (C) gives the remainder the sign of the dividend for `17 % -5`, and floors in `int()`.

**Trap:** `int(x / y)` and `x // y` differ for negative operands.''',
            'verify': "ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '-4 3 -4 -3 -3' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graphs — degrees, BFS and DFS',
            'text': 'Consider the undirected graph G below. In every traversal, neighbours are visited in alphabetical order. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['C', 'E'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 0],
                    },
                    'caption': 'Graph G',
                },
            ],
            'options': [
                'The recursive DFS order starting from A is A, B, D, E, C, F',
                'G is bipartite',
                'In the BFS tree rooted at A, vertex F is at distance 3 from A',
                'G has exactly 4 vertices of odd degree',
            ],
            'answer': ['C', 'D'],
            'solution': '''Degrees: A 2, B 2, C 3, D 3, E 3, F 1 (sum 14 = 2 × 7 edges).

- (A) DFS: A → B (first neighbour) → D (B's only unvisited neighbour) → D's neighbours in order B, C, E: C is unvisited → C → C's unvisited neighbour E → E → F. Order A, B, D, C, E, F. The stated order skips C at D. **FALSE.**
- (B) C–D–E is a triangle (odd cycle), so G is not bipartite. **FALSE.**
- (C) BFS from A: level 1 = {B, C}, level 2 = {D, E} (D from B, E from C), level 3 = {F}. **TRUE.**
- (D) Odd-degree vertices: C, D, E, F → 4. **TRUE** (always an even number by the handshaking lemma).

**Trap:** in (A), at vertex D the alphabetically first unvisited neighbour is C, not E.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['C', 'E'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 2],
                        'E': [3, 0],
                        'F': [4.5, 0],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['E', 'F'],
                    ],
                    'caption': 'BFS tree from A (highlighted)',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from collections import deque
E = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E"),("E","F"),("C","E")]
G = {v: [] for v in "ABCDEF"}
for u, v in E: G[u].append(v); G[v].append(u)
for v in G: G[v].sort()
odd = sum(len(G[v]) % 2 for v in G)
order = []
def dfs(u):
    order.append(u)
    for w in G[u]:
        if w not in order: dfs(w)
dfs("A")
d = {"A": 0}; q = deque("A")
while q:
    u = q.popleft()
    for w in G[u]:
        if w not in d: d[w] = d[u] + 1; q.append(w)
assert odd == 4 and order != list("ABDECF") and d["F"] == 3
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — nested lists and shallow copies',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''grid = [[0] * 3] * 3
grid[0][1] = 5
rows = [row[:] for row in grid]
rows[1][2] = 7
grid[2][0] += 1
total = sum(sum(r) for r in grid)
total += sum(sum(r) for r in rows)
print(total)''',
            'answer': '40',
            'solution': '''`[[0] * 3] * 3` makes an outer list holding **three references to the same inner list**. `[0] * 3` itself is fine because integers are immutable, but replicating the outer list copies only the reference.

- `grid[0][1] = 5`: the single shared row becomes [0, 5, 0]; every `grid[i]` shows it.
- `rows = [row[:] for row in grid]`: three *independent* copies, each [0, 5, 0] (taken **now**, before later changes).
- `rows[1][2] = 7`: only the second copy changes → rows = [[0,5,0], [0,5,7], [0,5,0]].
- `grid[2][0] += 1`: the shared row becomes [1, 5, 0]; `rows` is unaffected.

Sums:

- grid: three references to [1, 5, 0] → 3 × 6 = 18.
- rows: 5 + 12 + 5 = 22.

Total = 18 + 22 = **40**.

Common wrong answers:

- 18 — treating `grid` as three independent rows (grid = [[0,5,0],[0,0,0],[1,0,0]], sum 6; rows sum 5 + 7 + 0 = 12);
- 43 — assuming the copies in `rows` also see the later `+= 1` (6 + 13 + 6 = 25 for rows).

**Trap:** list replication `*` on a list of lists aliases rows; a slice copy `row[:]` is a snapshot at the moment it is taken. The idiom `[[0] * 3 for _ in range(3)]` creates independent rows.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — strings, loops and slicing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def encode(s):
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        run = j - i
        out.append(s[i] + str(run) if run > 1 else s[i])
        i = j
    return ''.join(out)

r = encode("aaabccddddae")
print(r, len(r), r[::-2])''',
            'options': [
                '`a3bc2d4ae 9 ea4dc`',
                '`a3bc2d4ae 9 e42ba`',
                '`a3b1c2d4a1e1 12 1a1d2b3`',
                '`a3bc2d5e 8 e5c3`',
            ],
            'answer': 'B',
            'solution': '''`encode` is run-length encoding: for each maximal run of equal characters it emits the character, followed by the run length only when the run is longer than 1.

Runs in `aaabccddddae`: aaa (3), b (1), cc (2), dddd (4), a (1), e (1).
Encoded pieces: `a3`, `b`, `c2`, `d4`, `a`, `e` → r = `a3bc2d4ae`, len(r) = 9.

Indexing r: a0 3₁ b2 c3 2₄ d5 4₆ a7 e8. `r[::-2]` starts at the last index (8) and takes every second character backwards: indices 8, 6, 4, 2, 0 → `e`, `4`, `2`, `b`, `a` → `e42ba`.

Option analysis:

- (A) `ea4dc` takes indices 8, 7, 6, 5, 3 — irregular; with step −2 starting at index 8 only the even indices 8, 6, 4, 2, 0 are taken.
- (B) `a3bc2d4ae 9 e42ba` — correct.
- (C) appends counts of 1 as well; the conditional expression suppresses them.
- (D) merges the final `a` into the `d` run; a run stops at the first different character.

**Trap:** the conditional expression `X if cond else Y` binds looser than `+`, so `s[i] + str(run) if run > 1 else s[i]` means `(s[i] + str(run)) if run > 1 else s[i]`.''',
            'verify': "ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'a3bc2d4ae 9 e42ba' and ANSWER == 'C'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Queues — circular array implementation',
            'text': 'A circular queue of capacity 5 is implemented as follows. Which of the following statements about the state after the program finishes is/are TRUE?',
            'code': '''Q = [None] * 5
front = rear = size = 0

def enq(x):
    global rear, size
    Q[rear] = x
    rear = (rear + 1) % 5
    size += 1

def deq():
    global front, size
    x = Q[front]
    front = (front + 1) % 5
    size -= 1
    return x

for x in [3, 6, 9, 12]:
    enq(x)
deq(); deq()
for x in [15, 18, 21]:
    enq(x)
s = deq() + deq()
enq(s)
print(front, rear, size, Q)''',
            'options': [
                '`size` is 3',
                'The elements logically in the queue, from front to rear, are 15, 18, 21, 21',
                'The list `Q` contains 12 at index 3, and 12 is one of the elements logically in the queue',
                '`front` is 4 and `rear` is 3',
            ],
            'answer': ['B', 'D'],
            'solution': '''In a circular queue, `front` points at the oldest element and `rear` at the next free slot; both advance modulo the capacity. Dequeuing does **not** erase the slot.

- enq 3, 6, 9, 12 → Q = [3, 6, 9, 12, None], front 0, rear 4, size 4.
- deq twice (3, 6) → front 2, size 2.
- enq 15 → Q[4], rear 0; enq 18 → Q[0], rear 1; enq 21 → Q[1], rear 2; size 5 (full).
- s = deq() + deq() = Q[2] + Q[3] = 9 + 12 = 21; front 4, size 3.
- enq 21 → Q[2] = 21, rear 3, size 4.

Final: front 4, rear 3, size 4, Q = [18, 21, 21, 12, 15]. Logical contents from front: Q[4], Q[0], Q[1], Q[2] = 15, 18, 21, 21.

- (A) FALSE — size is 4.
- (B) TRUE.
- (C) FALSE — 12 is still physically present at index 3 (a stale value), but index 3 is outside the live range front … rear−1 (indices 4, 0, 1, 2).
- (D) TRUE.

**Trap:** reading the raw array instead of walking from `front` for `size` elements.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [18, 21, 21, 12, 15],
                    'pointers': {
                        'front': 4,
                        'rear': 3,
                    },
                    'highlight': [4, 0, 1, 2],
                    'label': 'Q',
                    'caption': 'Final array (live slots highlighted)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "4 3 4 [18, 21, 21, 12, 15]"
live = [Q[(front + i) % 5] for i in range(size)]
assert live == [15, 18, 21, 21] and 12 not in live and size != 3
assert sorted(ANSWER) == ["A", "B"]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Arrays — rotation by reversal',
            'text': 'Consider the following Python functions. Which of the following statements is/are TRUE? (Each statement starts from a fresh list `a = [1, 2, 3, 4, 5, 6, 7]`; a *swap* is one execution of the tuple-assignment line in `rev`.)',
            'code': '''def rev(a, i, j):
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1

def mystery(a, k):
    n = len(a)
    k %= n
    rev(a, 0, n - 1)
    rev(a, 0, k - 1)
    rev(a, k, n - 1)''',
            'options': [
                '`mystery(a, 10)` performs exactly 6 swaps',
                '`mystery(a, 7)` leaves `a` unchanged and performs no swaps',
                'After `mystery(a, -2)`, `a` is `[6, 7, 1, 2, 3, 4, 5]`',
                'After `mystery(a, 10)`, `a` is `[5, 6, 7, 1, 2, 3, 4]`',
            ],
            'answer': ['A', 'D'],
            'solution': '''Reversing the whole array, then reversing the first k and the last n − k elements, **rotates the array right by k** in place.

(D)/(A): k = 10 % 7 = 3.

- rev(0, 6): [7, 6, 5, 4, 3, 2, 1] — 3 swaps.
- rev(0, 2): [5, 6, 7, 4, 3, 2, 1] — 1 swap.
- rev(3, 6): [5, 6, 7, 1, 2, 3, 4] — 2 swaps.

Result is the right-rotation by 3 and swaps = 3 + 1 + 2 = 6. Both **TRUE**.

(C): Python's `%` with a positive modulus is non-negative: −2 % 7 = 5. So the call rotates right by 5 (= left by 2) giving [3, 4, 5, 6, 7, 1, 2]. The listed array is the right-rotation by 2. **FALSE.**

(B): k = 0. rev(0, 6) reverses (3 swaps), rev(0, −1) does nothing (i > j), and rev(0, 6) reverses back (3 swaps). The array is unchanged but **6 swaps** occur. **FALSE.**

**Trap:** assuming −2 % 7 is −2 (C/Java behaviour) or that k = 0 short-circuits.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def run(k):
    a = list(range(1, 8)); cnt = [0]
    def rv(i, j):
        while i < j:
            a[i], a[j] = a[j], a[i]; cnt[0] += 1; i += 1; j -= 1
    n = len(a); k %= n
    rv(0, n - 1); rv(0, k - 1); rv(k, n - 1)
    return a, cnt[0]
a = list(range(1, 8)); mystery(a, 10); assert a == [5, 6, 7, 1, 2, 3, 4]
assert run(10) == ([5, 6, 7, 1, 2, 3, 4], 6)
assert run(-2)[0] == [3, 4, 5, 6, 7, 1, 2]
assert run(7) == (list(range(1, 8)), 6)
assert sorted(ANSWER) == ["A", "B"]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Merge sort — counting comparisons',
            'text': '''Top-down merge sort (split a list of length n into the first ⌊n/2⌋ and the remaining elements, sort each recursively, then merge) is applied to
[38, 12, 55, 7, 41, 29, 63, 18].
The merge step compares the front elements of the two runs and stops comparing as soon as one run is exhausted (the rest is copied without comparisons). The total number of element comparisons made by all merges is''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [38, 12, 55, 7, 41, 29, 63, 18],
                    'label': 'A',
                },
            ],
            'options': ['12', '16', '17', '24'],
            'answer': 'C',
            'solution': '''Merging runs of lengths p and q needs between min(p, q) and p + q − 1 comparisons; the exact count depends on when one run is exhausted.

Level 1 (pairs), 1 comparison each: [38]+[12], [55]+[7], [41]+[29], [63]+[18] → 4 comparisons; runs [12, 38], [7, 55], [29, 41], [18, 63].

Level 2:

- [12, 38] + [7, 55]: 12 vs 7 → 7; 12 vs 55 → 12; 38 vs 55 → 38; left run exhausted, copy 55. 3 comparisons.
- [29, 41] + [18, 63]: 29 vs 18 → 18; 29 vs 63 → 29; 41 vs 63 → 41; copy 63. 3 comparisons.

Level 3: [7, 12, 38, 55] + [18, 29, 41, 63]: 7|18, 12|18, 38|18, 38|29, 38|41, 55|41, 55|63 → 7 comparisons, then 63 is copied.

Total = 4 + 3 + 3 + 7 = **17** → (C).

- (A) 12 is the best-case count (n/2 · log₂ n = 4 · 3).
- (B) 16 forgets one comparison in the final merge.
- (D) 24 = n log₂ n is only an upper-bound estimate; the worst case for n = 8 is 17 as well (each merge using p + q − 1), so this input happens to be a worst case.

**Tip:** worst-case comparisons for n = 2^k is n·k − n + 1 = 8·3 − 8 + 1 = 17.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Runs after each merge level',
                    'row_labels': ['start', 'level 1', 'level 2', 'level 3'],
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'rows': [
                        [38, 12, 55, 7, 41, 29, 63, 18],
                        [12, 38, 7, 55, 29, 41, 18, 63],
                        [7, 12, 38, 55, 18, 29, 41, 63],
                        [7, 12, 18, 29, 38, 41, 55, 63],
                    ],
                },
            ],
            'verify': '''
def ms(a, c):
    if len(a) <= 1: return a
    m = len(a) // 2; L = ms(a[:m], c); R = ms(a[m:], c); i = j = 0; out = []
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
c = [0]; ms([38, 12, 55, 7, 41, 29, 63, 18], c)
assert c[0] == 17 and ANSWER == "C"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Bubble sort — early termination',
            'text': 'The following bubble sort is applied to A = [4, 1, 6, 2, 8, 3, 9]. The total number of times the comparison `A[j] > A[j + 1]` is evaluated is ______.',
            'code': '''def bubble(A):
    n = len(A)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break''',
            'answer': '18',
            'solution': '''Each pass i compares n − 1 − i adjacent pairs; the flag stops the algorithm after the first pass that makes **no** swap (that pass's comparisons still count).

n = 7.

- Pass 0 (6 comparisons): swaps (4,1), (6,2), (8,3) → [1, 4, 2, 6, 3, 8, 9].
- Pass 1 (5 comparisons): swaps (4,2), (6,3) → [1, 2, 4, 3, 6, 8, 9].
- Pass 2 (4 comparisons): swap (4,3) → [1, 2, 3, 4, 6, 8, 9].
- Pass 3 (3 comparisons): no swap → stop.

Comparisons = 6 + 5 + 4 + 3 = **18**. (Swaps = 6, equal to the number of inversions of the input.)

Without the flag the algorithm would make 6 + 5 + 4 + 3 + 2 + 1 = 21 comparisons. The number of passes needed equals 1 + the largest distance any element must move **left** (element 3 moves from index 5 to index 2, i.e. 3 places, so 3 swapping passes + 1 verification pass).

**Trap:** forgetting to count the final, swap-free pass (answer 15).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'row_labels': ['input', 'pass 0', 'pass 1', 'pass 2', 'pass 3'],
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6'],
                    'rows': [
                        [4, 1, 6, 2, 8, 3, 9],
                        [1, 4, 2, 6, 3, 8, 9],
                        [1, 2, 4, 3, 6, 8, 9],
                        [1, 2, 3, 4, 6, 8, 9],
                        [1, 2, 3, 4, 6, 8, 9],
                    ],
                },
            ],
            'verify': '''
A = [4, 1, 6, 2, 8, 3, 9]; n = len(A); cmp = 0
for i in range(n - 1):
    sw = False
    for j in range(n - 1 - i):
        cmp += 1
        if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]; sw = True
    if not sw: break
assert cmp == int(ANSWER)
B = [4, 1, 6, 2, 8, 3, 9]; bubble(B); assert B == sorted(B)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source S on the weighted directed graph below. The sum of the shortest-path distances from S to all six vertices (including d(S) = 0) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['B', 'A', 3],
                        ['B', 'C', 8],
                        ['A', 'C', 2],
                        ['A', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'E', 9],
                        ['D', 'E', 3],
                        ['B', 'E', 15],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 1],
                        'D': [6, 2],
                        'E': [6, 0],
                    },
                },
            ],
            'answer': '33',
            'solution': '''Dijkstra repeatedly extracts the unfinished vertex with the smallest tentative distance and relaxes its out-edges; with non-negative weights each extracted distance is final.

- Init: S = 0, rest ∞.
- Extract S (0): A = 7, B = 2.
- Extract B (2): A = min(7, 2 + 3) = 5, C = 10, E = 17.
- Extract A (5): C = min(10, 5 + 2) = 7, D = 11.
- Extract C (7): D = min(11, 7 + 1) = 8, E = min(17, 16) = 16.
- Extract D (8): E = min(16, 8 + 3) = 11.
- Extract E (11).

Distances: S 0, A 5, B 2, C 7, D 8, E 11. Sum = 0 + 5 + 2 + 7 + 8 + 11 = **33**.

Shortest-path tree: S→B, B→A, A→C, C→D, D→E — a single chain, so the path to E is S→B→A→C→D→E with cost 2 + 3 + 2 + 1 + 3 = 11.

**Trap:** stopping relaxation early and keeping E = 16 (via C→E) or E = 17 (via B→E); a direct edge with few hops is not necessarily shortest.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, 10, '∞', 17],
                        [0, 5, 2, 7, 11, 17],
                        [0, 5, 2, 7, 8, 16],
                        [0, 5, 2, 7, 8, 11],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [("S","A",7),("S","B",2),("B","A",3),("B","C",8),("A","C",2),("A","D",6),
     ("C","D",1),("C","E",9),("D","E",3),("B","E",15)]
G = {v: [] for v in "SABCDE"}
for u, v, w in E: G[u].append((v, w))
d = {v: float("inf") for v in G}; d["S"] = 0; pq = [(0, "S")]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d.values()) == int(ANSWER) and d["E"] == 11
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array H = [12, 7, 25, 3, 18, 30, 9, 15] (0-indexed, children of i at 2i+1 and 2i+2) is converted into a **max-heap** using the bottom-up build-heap procedure (sift-down applied to i = 3, 2, 1, 0). A *swap* is one parent–child exchange during sift-down. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [12, 7, 25, 3, 18, 30, 9, 15],
                    'caption': 'H viewed as a complete binary tree (before build-heap)',
                },
            ],
            'options': [
                'In the built heap, 12 is stored in a leaf',
                'The resulting heap array is [30, 18, 25, 15, 7, 12, 9, 3]',
                'After one DELETE-MAX on the built heap (last element moved to the root, then sift-down), the array is [25, 18, 9, 15, 7, 12, 3]',
                'Build-heap performs exactly 5 swaps',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Bottom-up build-heap sifts down every internal node, from the last internal node (index ⌊n/2⌋ − 1 = 3) back to the root. Sift-down swaps with the **larger** child while that child is larger.

- i = 3 (3): child 15 → swap. [12, 7, 25, 15, 18, 30, 9, 3] (1 swap)
- i = 2 (25): children 30, 9 → swap with 30. [12, 7, 30, 15, 18, 25, 9, 3] (2)
- i = 1 (7): children 15, 18 → swap with 18; index 4 has no children. [12, 18, 30, 15, 7, 25, 9, 3] (3)
- i = 0 (12): children 18, 30 → swap with 30 (4); at index 2 children 25, 9 → swap with 25 (5). [30, 18, 25, 15, 7, 12, 9, 3]

- (A) TRUE — 12 is at index 5; indices 4 … 7 are leaves in an 8-element heap.
- (B) TRUE.
- (C) FALSE. Move 3 to the root: [3, 18, 25, 15, 7, 12, 9]; 3 swaps with 25 (larger child), then at index 2 children 12, 9 → swap with 12: [25, 18, 12, 15, 7, 3, 9]. The option swaps with the wrong child.
- (D) TRUE — 5 swaps.

**Trap:** sift-down must continue after the first swap (the 12 at the root sinks two levels).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [30, 18, 25, 15, 7, 12, 9, 3],
                    'caption': 'Max-heap after build-heap',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def sift(a, i, n, c):
    while True:
        l = 2 * i + 1; r = l + 1; m = i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; c[0] += 1; i = m
h = [12, 7, 25, 3, 18, 30, 9, 15]; c = [0]
for i in range(3, -1, -1): sift(h, i, 8, c)
assert h == [30, 18, 25, 15, 7, 12, 9, 3] and c[0] == 5
g = h[:]; g[0] = g.pop(); sift(g, 0, 7, [0])
assert g == [25, 18, 12, 15, 7, 3, 9] and h.index(12) >= 4
assert sorted(ANSWER) == ["A", "B", "D"]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': 'The Lomuto partition procedure below is called once on the whole array A = [14, 3, 22, 9, 17, 5, 11] (pivot = last element). The array after the call returns is',
            'code': '''def partition(A, lo, hi):
    p = A[hi]
    i = lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [14, 3, 22, 9, 17, 5, 11],
                    'label': 'A',
                    'pointers': {
                        'pivot': 6,
                    },
                },
            ],
            'options': [
                '[3, 9, 5, 11, 17, 22, 14]',
                '[3, 9, 5, 11, 14, 17, 22]',
                '[5, 3, 9, 11, 17, 22, 14]',
                '[3, 9, 5, 11, 22, 17, 14]',
            ],
            'answer': 'A',
            'solution': '''Lomuto keeps the invariant A[lo … i] ≤ pivot < A[i+1 … j−1]. Whenever A[j] ≤ pivot, i advances and A[i] ↔ A[j]. Finally the pivot is swapped into position i + 1.

Pivot p = 11, i = −1.

- j = 0 (14): > 11, nothing.
- j = 1 (3): i = 0, swap A[0] ↔ A[1] → [3, 14, 22, 9, 17, 5, 11].
- j = 2 (22): nothing.
- j = 3 (9): i = 1, swap A[1] ↔ A[3] → [3, 9, 22, 14, 17, 5, 11].
- j = 4 (17): nothing.
- j = 5 (5): i = 2, swap A[2] ↔ A[5] → [3, 9, 5, 14, 17, 22, 11].
- Final: swap A[3] ↔ A[6] → [3, 9, 5, 11, 17, 22, 14]; returns 3.

- (A) correct.
- (B) has a sorted right part — partition does not sort the sides.
- (C) moves 5 to the front; Lomuto keeps the elements ≤ pivot in the order they are discovered: 3, 9, 5.
- (D) puts 22 before 17; but only 14 (displaced by the final pivot swap) moves — to index 6 — while 17 and 22 keep their positions 4 and 5.

**Tip:** the element originally at index i + 1 is the one sent to the pivot's old slot.''',
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

A = [14, 3, 22, 9, 17, 5, 11]
k = partition(A, 0, 6)
assert A == [3, 9, 5, 11, 17, 22, 14] and k == 3 and ANSWER == "D"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linked lists — recursive pairwise swap',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def build(xs):
    head = None
    for x in reversed(xs):
        head = Node(x, head)
    return head

def f(h):
    if h is None or h.nxt is None:
        return h
    second = h.nxt
    h.nxt = f(second.nxt)
    second.nxt = h
    return second

h = f(build([2, 7, 1, 8, 2, 8, 1]))
out = 0
while h:
    out = out * 10 + h.v
    h = h.nxt
print(out)''',
            'answer': '7281821',
            'solution': '''`build` inserts at the head while iterating over the **reversed** input, so the list is 2 → 7 → 1 → 8 → 2 → 8 → 1 (same order as the Python list).

`f` swaps nodes in adjacent pairs recursively: it makes the second node of a pair the new head of that pair, points the first node to the result of processing the rest, and returns the second node. An odd node left at the end is returned unchanged.

Trace of the pairs:

- (2, 7) → 7, 2
- (1, 8) → 8, 1
- (2, 8) → 8, 2
- (1) alone → 1

Resulting list: 7 → 2 → 8 → 1 → 8 → 2 → 1.

The final loop reads the values as decimal digits: out = 7281821.

Recursion depth is ⌈n/2⌉ = 4 calls with a non-trivial body, plus the base call, so the function runs in Θ(n) time and Θ(n) stack space.

**Traps:**

- Forgetting that `reversed` in `build` cancels the head-insertion reversal (would give the list 1 → 8 → 2 → 8 → 1 → 7 → 2).
- Swapping only values rather than relinking — the result is the same here, but `second.nxt = h` must come **after** `h.nxt` is set, otherwise the rest of the list is lost.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [7, 2, 8, 1, 8, 2, 1],
                    'head': 'head',
                    'caption': 'List after f',
                },
            ],
            'verify': '''
xs = [2, 7, 1, 8, 2, 8, 1]; ys = []
for i in range(0, len(xs), 2): ys += xs[i:i + 2][::-1]
assert int("".join(map(str, ys))) == int(ANSWER)
assert OUTPUT.strip() == ANSWER
''',
        },
    ],
}
