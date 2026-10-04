# Set 26 — Linked-List Algorithms (GATE-level)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.
import math

# rho-shaped list for Q2: 0 -> 1 -> ... -> 11 -> 4
_RHO_POS = {str(i): [i * 1.2, 0] for i in range(5)}
for _j, _v in enumerate(range(4, 12)):
    _ang = math.pi - _j * 2 * math.pi / 8
    _RHO_POS[str(_v)] = [4 * 1.2 + 1.6 + 1.6 * math.cos(_ang), 1.6 * math.sin(_ang)]
_RHO_POS["4"] = [4 * 1.2, 0]

_LL = '''
class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out
'''

SET = {
    'number': 26,
    'title': 'Linked-List Algorithms',
    'difficulty': 'GATE-level',
    'focus': 'reversal, cycle detection, merging, middle node, list surgery',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — middle node with slow/fast pointers',
            'text': '`h` is the head of the singly linked list 10 → 20 → 30 → 40 → 50 → 60 → 70 → 80. Consider the following Python fragment. What is printed?',
            'code': '''s = f = h
while f and f.nxt:
    s, f = s.nxt, f.nxt.nxt
x = s.v

s = f = h
while f.nxt and f.nxt.nxt:
    s, f = s.nxt, f.nxt.nxt
print(x, s.v)''',
            'options': ['`50 40`', '`40 40`', '`50 50`', '`40 50`'],
            'answer': 'A',
            'solution': '''The fast pointer moves two nodes per step and the slow pointer one, so slow ends near the middle. For an **even** length, the exact stopping condition decides which of the two middle nodes is returned.

**Loop 1** (`while f and f.nxt`): positions (slow, fast) = (10, 10) → (20, 30) → (30, 50) → (40, 70) → (50, None). At (40, 70), f = 70 and f.nxt = 80, so one more step: f becomes None. x = **50** (the second middle).

**Loop 2** (`while f.nxt and f.nxt.nxt`): (10, 10) → (20, 30) → (30, 50) → (40, 70); now f.nxt = 80 but f.nxt.nxt = None, so stop. s.v = **40** (the first middle).

Output: `50 40`.

- (B), (C), (D) mix up which condition gives which middle.

**Tip:** for even n, `while f and f.nxt` returns node n/2 + 1 (1-based); `while f.nxt and f.nxt.nxt` returns node n/2 — the latter is what merge sort on lists uses to split into equal halves.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [10, 20, 30, 40, 50, 60, 70, 80],
                    'head': 'h',
                    'caption': 'The two middles: 40 (loop 2) and 50 (loop 1)',
                },
            ],
            'verify': '''
class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

h = mk([10, 20, 30, 40, 50, 60, 70, 80])
s = f = h
while f and f.nxt: s, f = s.nxt, f.nxt.nxt
x = s.v
s = f = h
while f.nxt and f.nxt.nxt: s, f = s.nxt, f.nxt.nxt
assert (x, s.v) == (50, 40) and ANSWER == 'A'
''',
            'run_code': False,
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': "Cycle detection — Floyd's algorithm",
            'text': "A singly linked list has nodes labelled 0, 1, …, 11, where node i points to node i + 1 for i < 11 and node 11 points back to node 4 (see figure). Floyd's algorithm starts with `slow = fast = node 0` and repeats `slow = slow.nxt; fast = fast.nxt.nxt` until `slow is fast`. The number of iterations of this loop is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
                    'edges': [
                        ['0', '1'],
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '4'],
                        ['4', '5'],
                        ['5', '6'],
                        ['6', '7'],
                        ['7', '8'],
                        ['8', '9'],
                        ['9', '10'],
                        ['10', '11'],
                        ['11', '4'],
                    ],
                    'pos': {
                        '0': [0.0, 0],
                        '1': [1.2, 0],
                        '2': [2.4, 0],
                        '3': [3.5999999999999996, 0],
                        '4': [4.8, 0],
                        '5': [5.268629150101525, 1.1313708498984762],
                        '6': [6.4, 1.6],
                        '7': [7.531370849898477, 1.131370849898476],
                        '8': [8.0, 0.0],
                        '9': [7.531370849898477, -1.131370849898476],
                        '10': [6.4, -1.6],
                        '11': [5.268629150101525, -1.1313708498984762],
                    },
                    'caption': 'Tail of length 4 (nodes 0–3) and a cycle of length 8 (nodes 4–11)',
                },
            ],
            'answer': '8',
            'solution': '''Let μ = 4 be the tail length and λ = 8 the cycle length. After t iterations slow is at position t and fast at 2t along the 'unrolled' path. They meet at the first t ≥ μ with 2t − t = t ≡ 0 (mod λ), i.e. the smallest multiple of λ that is ≥ μ.

Here λ = 8 ≥ μ = 4, so **t = 8**. Check by tracing (slow, fast):
(1, 2), (2, 4), (3, 6), (4, 8), (5, 10), (6, 4), (7, 6), (8, 8) → meet at node 8 after 8 iterations. (Fast at step 6: position 12 → node 4, since 12 − 4 = 8 ≡ 0.)

**Tip:** the meeting point is μ steps (mod λ) *before* the cycle start along the cycle, so restarting one pointer at the head and moving both one step at a time finds the cycle start (node 4) after μ = 4 more steps.

**Trap:** the answer is not always λ: if μ > λ, t is the first multiple of λ that is ≥ μ.''',
            'verify': '''
class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

ns = [Node(i) for i in range(12)]
for i in range(11): ns[i].nxt = ns[i + 1]
ns[11].nxt = ns[4]
s = f = ns[0]; it = 0
while True:
    s, f = s.nxt, f.nxt.nxt; it += 1
    if s is f: break
assert it == int(ANSWER) and s.v == 8
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Linked lists — cost of operations',
            'text': 'A singly linked list of n nodes is maintained with two references, `head` (first node) and `tail` (last node); nodes have only `val` and `nxt` fields. Which of the following operations can be performed in **O(1)** worst-case time (keeping `head`/`tail` correct)?',
            'options': [
                'Appending a new node after the last node',
                'Deleting the last node',
                'Deleting the node referenced by a given pointer p, where p is known not to be the last node (node identity need not be preserved)',
                'Finding the middle node',
            ],
            'answer': ['A', 'C'],
            'solution': '''O(1) is possible only when every reference that must change is reachable in constant steps.

- (A) `tail.nxt = new; tail = new` — **O(1).** True.
- (B) After deletion `tail` must point to the *second-to-last* node, which can only be found by walking from `head` (no back pointers) — Θ(n). False.
- (C) Copy the successor into p and bypass it: `p.val = p.nxt.val; p.nxt = p.nxt.nxt` (update `tail` if the bypassed node was the tail). **O(1).** True — this is why the question says node identity need not be preserved.
- (D) Needs a traversal (e.g. slow/fast pointers) — Θ(n) unless the length and middle are maintained separately. False.

**Trap:** having a `tail` pointer makes *insertion* at the end O(1) but not *deletion* at the end; that needs a doubly linked list.''',
            'verify': '''
class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

# demonstrate (C): delete node 3 from 1->2->3->4->5 using only p
h = mk([1, 2, 3, 4, 5]); p = h.nxt.nxt
p.v = p.nxt.v; p.nxt = p.nxt.nxt
assert show(h) == [1, 2, 4, 5]
assert sorted(ANSWER) == ['A', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — bracket matching',
            'text': 'The string `{[()()]([{}()])}[()]` is checked for balanced brackets using a stack: every opening bracket is pushed, and every closing bracket pops the top (which must match). The maximum number of elements on the stack at any moment is ______.',
            'answer': '4',
            'solution': '''The stack size equals the current nesting depth. Track it character by character:

- `{` 1, `[` 2, `(` 3, `)` 2, `(` 3, `)` 2, `]` 1
- `(` 2, `[` 3, `{` **4**, `}` 3, `(` **4**, `)` 3, `]` 2, `)` 1, `}` 0
- `[` 1, `(` 2, `)` 1, `]` 0

Every closing bracket matches the top, and the stack is empty at the end, so the string is balanced. Maximum depth = **4**, reached at `{` inside `([{` and again at the `(` after `}`.

**Trap:** counting the total number of pushes (10) or the number of bracket *pairs* instead of the maximum simultaneous nesting.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['{', '(', '[', '{'],
                    'label': 'depth 4',
                    'caption': 'Stack at maximum depth',
                },
            ],
            'verify': '''
st, mx = [], 0
pairs = {')': '(', ']': '[', '}': '{'}
for ch in "{[()()]([{}()])}[()]":
    if ch in "([{":
        st.append(ch); mx = max(mx, len(st))
    else:
        assert st and st.pop() == pairs[ch]
assert not st and mx == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — `+=` versus `+` on lists',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = [1, 2]
b = a
a += [3]
c = a
a = a + [4]
print(b, c is b, len(a))''',
            'options': ['`[1, 2] False 4`', '`[1, 2, 3] True 4`', '`[1, 2, 3, 4] True 4`', '`[1, 2] True 3`'],
            'answer': 'B',
            'solution': '''For lists, `a += x` calls `list.__iadd__`, which **extends the same object** in place. `a = a + x` builds a **new** list and rebinds `a`.

- `b = a` → both names refer to list L = [1, 2].
- `a += [3]` → L becomes [1, 2, 3]; `a` and `b` still refer to L.
- `c = a` → `c` refers to L.
- `a = a + [4]` → new list [1, 2, 3, 4]; only `a` is rebound.

So `b` = [1, 2, 3], `c is b` is True (both are L), `len(a)` = 4.

- (A) treats `+=` as creating a new list.
- (C) treats `a = a + [4]` as modifying L.
- (D) misses the in-place extension *and* the final concatenation.

**Trap:** for immutable types (tuples, strings, ints) `+=` does rebind; for lists it mutates.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[1, 2, 3] True 4' and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Hashing — linear probing with deletion',
            'text': 'Keys 31, 41, 51, 22, 62, 9, 19 are inserted in this order into an empty table of size 10 using h(k) = k mod 10 and linear probing. Then 41 and 22 are deleted by marking their slots with a **tombstone** (searches continue past a tombstone; an insertion of a key not present uses the first tombstone or empty slot on its probe path). Which statements is/are TRUE?',
            'options': [
                'Had the deletions simply emptied the slots (no tombstones), a search for 62 would fail',
                'Inserting 72 now places it in slot 2',
                'A search for 62 examines exactly 4 slots',
                'An unsuccessful search for 12 examines exactly 6 slots',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Build the table: 31→1, 41→2, 51→3, 22→4 (2, 3 full), 62→5 (2, 3, 4 full), 9→9, 19→0 (9 full, wraps to 0). After deletions: slot 2 = T (tombstone), slot 4 = T.

Table: 0:19, 1:31, 2:T, 3:51, 4:T, 5:62, 9:9 (slots 6, 7, 8 empty).

- (A) Without tombstones slot 2 would be empty, so the search for 62 stops at its home slot and reports 'absent' although 62 is in slot 5. **True.**
- (B) 72 (home 2): slot 2 is the first tombstone → stored in slot **2. True.**
- (C) 62: probe 2 (T, continue), 3 (51), 4 (T), 5 (62 found) → **4 slots. True.**
- (D) 12 (home 2): 2 (T), 3, 4 (T), 5, 6 (empty → stop) → **5** slots, not 6. False.

**Trap:** deletion in open addressing must not break probe chains; tombstones preserve them.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        0: 19,
                        1: 31,
                        2: 'T',
                        3: 51,
                        4: 'T',
                        5: 62,
                        9: 9,
                    },
                    'caption': 'Table after deleting 41 and 22 (T = tombstone)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

T = [None] * 10
for k in [31, 41, 51, 22, 62, 9, 19]:
    i = k % 10
    while T[i] is not None: i = (i + 1) % 10
    T[i] = k
for k in (41, 22): T[T.index(k)] = 'T'
def search(k):
    i, n = k % 10, 0
    while True:
        n += 1
        if T[i] is None: return False, n
        if T[i] == k: return True, n
        i = (i + 1) % 10
def ins_slot(k):
    i = k % 10
    while T[i] not in (None, 'T'): i = (i + 1) % 10
    return i
T2 = [None if x == 'T' else x for x in T]
truth = {'A': search(62) == (True, 4), 'B': ins_slot(72) == 2,
         'C': search(12) == (False, 6), 'D': T2[2] is None}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Heaps — insertion with sift-up',
            'text': 'The min-heap shown below is stored in an array. The keys 5 and then 3 are inserted using the standard insert (append at the end, then sift up). The resulting array is',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [4, 9, 6, 15, 12, 10, 8, 20],
                    'caption': 'Min-heap [4, 9, 6, 15, 12, 10, 8, 20]',
                },
            ],
            'options': [
                '[3, 4, 6, 9, 12, 10, 8, 20, 15, 5]',
                '[3, 5, 6, 9, 4, 10, 8, 20, 15, 12]',
                '[3, 4, 6, 5, 9, 10, 8, 20, 15, 12]',
                '[3, 4, 6, 9, 5, 10, 8, 20, 15, 12]',
            ],
            'answer': 'D',
            'solution': '''Insertion appends at index n and swaps with the parent (index (i−1)//2) while the parent is larger.

**Insert 5** at index 8: parent 3 holds 15 → swap (5 at 3); parent 1 holds 9 → swap (5 at 1); parent 0 holds 4 < 5 → stop.
Array: [4, 5, 6, 9, 12, 10, 8, 20, 15].

**Insert 3** at index 9: parent 4 holds 12 → swap (3 at 4); parent 1 holds 5 → swap (3 at 1); parent 0 holds 4 → swap (3 at 0).
Array: **[3, 4, 6, 9, 5, 10, 8, 20, 15, 12]**.

- (A) forgets to sift 3 up beyond its parent 12 and mis-places 5.
- (B) leaves 4 at index 4 — the swaps move each displaced parent *down one level only*.
- (C) places 5 under the wrong parent (index 3's child is index 7/8, not index 4).

**Tip:** the sift-up path of index i is i, (i−1)//2, …, 0 — for i = 9: 9 → 4 → 1 → 0.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 4, 6, 9, 5, 10, 8, 20, 15, 12],
                    'highlight': [0, 1, 4],
                    'caption': 'After inserting 5 and 3 (sift-up path of 3 highlighted)',
                },
            ],
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

H = [4, 9, 6, 15, 12, 10, 8, 20]
for x in (5, 3):
    H.append(x); i = len(H) - 1
    while i > 0 and H[(i - 1) // 2] > H[i]:
        H[i], H[(i - 1) // 2] = H[(i - 1) // 2], H[i]; i = (i - 1) // 2
assert H == [3, 4, 6, 9, 5, 10, 8, 20, 15, 12] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Selection sort — counting swaps',
            'text': 'Selection sort (ascending) is applied to [5, 2, 8, 1, 9, 3, 7]. In pass i (i = 0, 1, …, n−2) it finds the index m of the minimum of A[i..n−1] and swaps A[i] with A[m] **only if** m ≠ i. The number of swaps performed is ______.',
            'answer': '3',
            'solution': '''Selection sort places the i-th smallest element at position i in pass i; a swap is skipped when that element is already in place.

- i=0: min of whole array is 1 (index 3) → swap → [1, 2, 8, 5, 9, 3, 7] (1)
- i=1: min of A[1..] is 2, already at index 1 → no swap
- i=2: min is 3 (index 5) → swap → [1, 2, 3, 5, 9, 8, 7] (2)
- i=3: min is 5, already in place → no swap
- i=4: min is 7 (index 6) → swap → [1, 2, 3, 5, 7, 8, 9] (3)
- i=5: min is 8, in place → no swap

Total = **3** swaps.

**Tip:** the number of (non-trivial) swaps equals n minus the number of cycles of the permutation *as modified by earlier passes* — easiest is just to trace. Selection sort never needs more than n − 1 swaps.''',
            'verify': '''
A = [5, 2, 8, 1, 9, 3, 7]; sw = 0
for i in range(len(A) - 1):
    m = min(range(i, len(A)), key=lambda j: A[j])
    if m != i: A[i], A[m] = A[m], A[i]; sw += 1
assert sw == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BFS with adjacency lists',
            'text': '''The undirected graph shown below is stored as adjacency **linked lists**, in which the neighbours appear in exactly this order:
A: D, B   B: E, A, C   C: B, F   D: A, E   E: D, B, F   F: E, C
BFS from A visits neighbours in adjacency-list order. The BFS visit order is''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'D'],
                        ['A', 'B'],
                        ['B', 'E'],
                        ['B', 'C'],
                        ['C', 'F'],
                        ['D', 'E'],
                        ['E', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 1],
                        'C': [3, 1],
                        'D': [0, -0.5],
                        'E': [1.5, -0.5],
                        'F': [3, -0.5],
                    },
                },
            ],
            'options': ['A, B, D, C, E, F', 'A, D, B, E, C, F', 'A, D, E, B, F, C', 'A, D, B, C, E, F'],
            'answer': 'B',
            'solution': '''BFS dequeues a vertex and enqueues its unvisited neighbours **in the order of its adjacency list**, which need not be alphabetical.

- Dequeue A: enqueue D, B → queue [D, B]
- Dequeue D: neighbours A (seen), E → queue [B, E]
- Dequeue B: E (seen), A (seen), C → queue [E, C]
- Dequeue E: D, B seen; F → queue [C, F]
- Dequeue C, then F.

Order: **A, D, B, E, C, F**.

- (A) assumes alphabetical neighbour order.
- (C) is a DFS-like order (going deep through D → E).
- (D) processes B's neighbours before D's — but D was enqueued first.

**Trap:** the representation (order inside adjacency lists) determines the traversal order.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

from collections import deque
adj = {'A': 'DB', 'B': 'EAC', 'C': 'BF', 'D': 'AE', 'E': 'DBF', 'F': 'EC'}
seen, q, order = {'A'}, deque('A'), []
while q:
    u = q.popleft(); order.append(u)
    for v in adj[u]:
        if v not in seen: seen.add(v); q.append(v)
assert order == list('ADBECF') and ANSWER == 'A'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — lower bound',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def lb(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] < x:
            lo = m + 1
        else:
            hi = m
    return lo

A = [2, 4, 4, 4, 7, 9, 9, 12]
print(lb(A, 4), lb(A, 9) - lb(A, 8), lb(A, 13))''',
            'options': ['`1 2 8`', '`3 2 7`', '`1 0 8`', '`1 0 7`'],
            'answer': 'C',
            'solution': '''`lb(A, x)` returns the **first index i with A[i] ≥ x** (lower bound) — len(A) if no such index. The invariant: everything left of `lo` is < x, everything from `hi` on is ≥ x.

- lb(A, 4): first element ≥ 4 is at index **1** (the leftmost 4). Trace: (0,8) m=4 (7 ≥ 4) → hi=4; m=2 (4) → hi=2; m=1 (4) → hi=1; m=0 (2 < 4) → lo=1.
- lb(A, 9) = 5 and lb(A, 8) = 5 (8 is absent; the first element ≥ 8 is 9 at index 5) → difference **0**.
- lb(A, 13): every element is < 13 → returns len(A) = **8**.

Output `1 0 8`.

- (A) treats lb(9) − lb(8) as the count of 9s (that would be lb(A, 10) − lb(A, 9) = 2).
- (B) returns the last occurrence of 4 and counts 9s instead.
- (D) thinks an absent larger key returns the last index.

**Tip:** the count of x is lb(A, x+1) − lb(A, x) for integers.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['1', '0', '8'] and ANSWER == 'A'
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — reversal in groups of k',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

def rev_k(h, k):
    p, n = h, 0
    while p and n < k:
        p, n = p.nxt, n + 1
    if n < k:
        return h
    prev, cur = rev_k(p, k), h
    for _ in range(k):
        cur.nxt, prev, cur = prev, cur, cur.nxt
    return prev

print(show(rev_k(mk([1, 2, 3, 4, 5, 6, 7, 8]), 3)))''',
            'options': [
                '`[8, 7, 6, 5, 4, 3, 2, 1]`',
                '`[3, 2, 1, 6, 5, 4, 8, 7]`',
                '`[3, 2, 1, 6, 5, 4, 7, 8]`',
                '`[3, 2, 1, 4, 5, 6, 7, 8]`',
            ],
            'answer': 'C',
            'solution': '''`rev_k` first checks that at least k nodes remain; if not, it returns the remainder **unchanged**. Otherwise it recursively processes the list after the first k nodes (`p`), then reverses the first k nodes so that the old first node points to that processed remainder.

The tuple assignment `cur.nxt, prev, cur = prev, cur, cur.nxt` evaluates the right-hand side first (old prev, old cur, old cur.nxt) and then assigns left to right: the target `cur.nxt` still refers to the old `cur`, so this is a correct one-line pointer reversal.

- rev_k(7 → 8, 3): only 2 nodes → returned unchanged: 7 → 8.
- rev_k(4 → 5 → 6 → …): reverse 4, 5, 6 onto 7 → 8 → 6 → 5 → 4 → 7 → 8.
- rev_k(1 → …): reverse 1, 2, 3 onto that → **3 → 2 → 1 → 6 → 5 → 4 → 7 → 8**.

- (A) is a full reversal.
- (B) reverses the incomplete last group too.
- (D) reverses only the first group.

**Trap:** in a multiple assignment the right side is evaluated completely before any binding; but the *left-side targets* are assigned left to right, so `cur, cur.nxt = …` (other order) would set the `nxt` of the **new** cur — a classic bug.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 2, 1, 6, 5, 4, 7, 8],
                    'head': 'head',
                    'caption': 'Result: two full groups reversed, last group of 2 untouched',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[3, 2, 1, 6, 5, 4, 7, 8]' and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merging sorted linked lists',
            'text': 'Two sorted singly linked lists X = 3 → 8 → 12 → 20 → 31 and Y = 5 → 9 → 10 → 25 → 40 → 47 are merged into one sorted list by the standard method: repeatedly compare the heads, detach the smaller and append it to the result; when one list becomes empty the rest of the other is attached without comparisons. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 8, 12, 20, 31],
                    'head': 'X',
                },
                {
                    'type': 'linkedlist',
                    'values': [5, 9, 10, 25, 40, 47],
                    'head': 'Y',
                },
            ],
            'options': [
                'For some two sorted lists of lengths 5 and 6, this method makes 11 comparisons',
                'For some two sorted lists of lengths 5 and 6, this method makes only 5 comparisons',
                'Done by relinking the existing nodes, the merge needs only O(1) extra space',
                'Exactly 9 key comparisons are made for these two lists',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Each comparison outputs exactly one node; comparisons stop as soon as one list is exhausted.

**Trace:** 3 vs 5 → 3; 8 vs 5 → 5; 8 vs 9 → 8; 12 vs 9 → 9; 12 vs 10 → 10; 12 vs 25 → 12; 20 vs 25 → 20; 31 vs 25 → 25; 31 vs 40 → 31. X is now empty; attach 40 → 47. **9 comparisons.**

- (A) At most m + n − 1 = 10 comparisons: after 10 outputs, at least one list is empty (the last node is never compared). **False.**
- (B) If all of the 5-element list is smaller than the first element of the other, each comparison outputs a node of the shorter list: min(m, n) = 5 comparisons. **True.**
- (C) Relinking uses a constant number of pointers (a dummy head and a tail pointer). **True.**
- (D) **True.**

**Tip:** the number of comparisons is (m + n) − (number of nodes appended after one list runs out); here 11 − 2 = 9.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 5, 8, 9, 10, 12, 20, 25, 31, 40, 47],
                    'head': 'merged',
                    'caption': 'Merged list (40, 47 attached without comparisons)',
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def merge_cmp(X, Y):
    i = j = c = 0
    while i < len(X) and j < len(Y):
        c += 1
        if X[i] <= Y[j]: i += 1
        else: j += 1
    return c
from itertools import combinations
cnts = set()
for pos in combinations(range(11), 5):
    X = list(pos); Y = [v for v in range(11) if v not in pos]
    cnts.add(merge_cmp(X, Y))
truth = {'A': merge_cmp([3, 8, 12, 20, 31], [5, 9, 10, 25, 40, 47]) == 9,
         'B': 11 in cnts, 'C': 5 in cnts, 'D': True}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Circular linked list — elimination game',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

n, k = 10, 4
head = Node(1)
cur = head
for v in range(2, n + 1):
    cur.nxt = Node(v)
    cur = cur.nxt
cur.nxt = head              # close the circle; cur = node 10

while cur.nxt is not cur:
    for _ in range(k - 1):
        cur = cur.nxt
    cur.nxt = cur.nxt.nxt   # remove the node after cur
print(cur.v)''',
            'answer': '5',
            'solution': '''`cur` always sits **just before** the next person to be counted, so after k − 1 moves `cur.nxt` is the k-th person, who is unlinked. This is the Josephus process with every 4th person removed, starting the count at 1.

Circle 1 … 10, `cur` = 10.
- Count 1, 2, 3, **4** → remove 4; circle 1 2 3 5 6 7 8 9 10, cur = 3.
- 5, 6, 7, **8** → remove 8; cur = 7.
- 9, 10, 1, **2** → remove 2; cur = 1.
- 3, 5, 6, **7** → remove 7; cur = 6.
- 9, 10, 1, **3** → remove 3; cur = 1.
- 5, 6, 9, **10** → remove 10; cur = 9.
- 1, 5, 6, **9** → remove 9; cur = 6.
- 1, 5, 6, **1** → remove 1; cur = 6.
- 5, 6, 5, **6** → remove 6; only 5 remains.

Removal order: 4, 8, 2, 7, 3, 10, 9, 1, 6. Survivor **5**.

**Tip:** the Josephus recurrence J(1) = 0, J(n) = (J(n−1) + k) mod n (0-based) gives J(10) = 4, i.e. person 5. **Trap:** forgetting that counting skips removed nodes and wraps around.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                    'circular': True,
                    'head': 'head',
                    'caption': 'Initial circular list',
                },
            ],
            'verify': '''
J = 0
for m in range(2, 11): J = (J + 4) % m
assert int(OUTPUT.strip()) == int(ANSWER) == J + 1
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — rotation by k',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

def rotate(h, k):
    if h is None:
        return h
    n, tail = 1, h
    while tail.nxt:
        tail, n = tail.nxt, n + 1
    k %= n
    if k == 0:
        return h
    tail.nxt = h
    for _ in range(n - k):
        tail = tail.nxt
    h, tail.nxt = tail.nxt, None
    return h

print(show(rotate(mk([1, 2, 3, 4, 5]), 13)))''',
            'options': ['`[2, 3, 4, 5, 1]`', '`[4, 5, 1, 2, 3]`', '`[1, 2, 3, 4, 5]`', '`[3, 4, 5, 1, 2]`'],
            'answer': 'D',
            'solution': '''The function rotates the list **right** by k: it finds the length n and the tail, reduces k mod n, makes the list circular, walks n − k steps from the tail to reach the new tail, and breaks the circle after it.

- n = 5, tail = node 5; k = 13 mod 5 = 3.
- tail.nxt = head (circle 1 → 2 → 3 → 4 → 5 → 1).
- Walk n − k = 2 steps from node 5: → 1 → 2. New tail = node 2.
- `h, tail.nxt = tail.nxt, None`: RHS evaluates to (node 3, None); then h = node 3 and node 2's nxt = None.

Result: **3 → 4 → 5 → 1 → 2**.

- (A) is a left rotation by 1.
- (B) is a rotation *left* by 3 (equivalently right by 2).
- (C) assumes 13 is a multiple of 5 or that the circle is never broken.

**Tip:** rotating right by k moves the last k nodes to the front; check: the last three nodes 3, 4, 5 come first.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[3, 4, 5, 1, 2]' and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Intersection of two linked lists — two-pointer method',
            'text': 'Two singly linked lists share a common tail as shown: list A is a1 → a2 → a3 → a4 → c1 → c2 → c3 and list B is b1 → … → b6 → c1 → c2 → c3 (the c-nodes are the **same** objects). The fragment below is run with `hA` = a1 and `hB` = b1. Which of the following statements is/are TRUE?',
            'code': '''p, q, steps = hA, hB, 0
while p is not q:
    p = p.nxt if p else hB
    q = q.nxt if q else hA
    steps += 1''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'c1', 'c2', 'c3'],
                    'edges': [
                        ['a1', 'a2'],
                        ['a2', 'a3'],
                        ['a3', 'a4'],
                        ['a4', 'c1'],
                        ['b1', 'b2'],
                        ['b2', 'b3'],
                        ['b3', 'b4'],
                        ['b4', 'b5'],
                        ['b5', 'b6'],
                        ['b6', 'c1'],
                        ['c1', 'c2'],
                        ['c2', 'c3'],
                    ],
                    'pos': {
                        'a1': [2, 2],
                        'a2': [3, 2],
                        'a3': [4, 2],
                        'a4': [5, 2],
                        'b1': [0, 0],
                        'b2': [1, 0],
                        'b3': [2, 0],
                        'b4': [3, 0],
                        'b5': [4, 0],
                        'b6': [5, 0],
                        'c1': [6, 1],
                        'c2': [7, 1],
                        'c3': [8, 1],
                    },
                },
            ],
            'options': [
                'The loop body executes exactly 14 times',
                'When the loop ends, p and q both refer to c1',
                'The fragment uses O(1) extra space',
                'If the two lists had no common node (lengths 7 and 9), the loop would end after 16 iterations with p = q = None',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Each pointer walks its own list, then (after stepping onto `None` once) switches to the head of the other list. Both therefore walk (length A) + 1 + (length B before the junction) steps before arriving at the junction, which equalises the head-start difference.

- p's route: a1 … a4, c1, c2, c3 (indices 0–6), None (7), b1 … b6 (8–13), **c1 (14)**.
- q's route: b1 … b6, c1, c2, c3 (0–8), None (9), a1 … a4 (10–13), **c1 (14)**.
- They never coincide before step 14 (check: when p is at c1 (step 4), q is at b5; when q is at c1 (step 6), p is at c3).

- (A) **True** — 14 iterations.
- (B) **True** — they meet at the first common node c1.
- (C) Only two pointers and a counter. **True.**
- (D) With no common node, both reach `None` the second time after 7 + 1 + 9 = 9 + 1 + 7 = **17** iterations, not 16. **False.**

**Trap:** because the `None` itself is a step in this code, the counts are one larger per list than the plain lengths suggest.''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

c = mk(['c1', 'c2', 'c3'])
def chain(names, tailnode):
    h = None
    for v in reversed(names): h = Node(v, h if h else tailnode) if h else Node(v, tailnode)
    return h
hA = chain(['a1', 'a2', 'a3', 'a4'], c); hB = chain(['b%d' % i for i in range(1, 7)], c)
assert show(hA) == ['a1','a2','a3','a4','c1','c2','c3'] and len(show(hB)) == 9
def run(hA, hB):
    p, q, steps = hA, hB, 0
    while p is not q:
        p = p.nxt if p else hB
        q = q.nxt if q else hA
        steps += 1
    return p, steps
p, st = run(hA, hB)
p2, st2 = run(mk(list(range(7))), mk(list(range(9))))
truth = {'A': st == 14, 'B': p is c, 'C': (p2 is None and st2 == 16), 'D': True}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
            'run_code': False,
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recursion on linked lists',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def mk(vals):
    h = None
    for v in reversed(vals): h = Node(v, h)
    return h
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out

def f(h):
    if h is None:
        return 0
    r = f(h.nxt)
    return r * 2 + h.v

print(f(mk([1, 1, 0, 1, 0, 0, 1])))''',
            'answer': '75',
            'solution': '''Unfold the recursion: f(h) = h.v + 2·f(h.nxt). So for values v₀, v₁, …, v₆ (head first),
f = v₀ + 2v₁ + 4v₂ + 8v₃ + 16v₄ + 32v₅ + 64v₆ — the list is read as a binary number whose **least significant bit is at the head**.

Values 1, 1, 0, 1, 0, 0, 1 → 1 + 2 + 0 + 8 + 0 + 0 + 64 = **75**.

Trace of the return values, from the tail back to the head (f(None) = 0): 0·2 + 1 = 1 → 2·1 + 0 = 2 → 2·2 + 0 = 4 → 2·4 + 1 = 9 → 2·9 + 0 = 18 → 2·18 + 1 = 37 → 2·37 + 1 = 75.

**Trap:** reading the list head-first as binary 1101001₂ gives 105 — that would require `f` to pass an accumulator *down* (Horner's rule from the head), not combine results on the way *up*.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 1, 0, 1, 0, 0, 1],
                    'head': 'h',
                    'caption': 'Weights 1, 2, 4, …, 64 from head to tail',
                },
            ],
            'verify': '''
assert int(OUTPUT.strip()) == int(ANSWER) == int('1001011', 2)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Generators over a linked list mutated during iteration',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

class LL:
    def __init__(self, vals):
        self.head = None
        for v in reversed(vals):
            self.head = Node(v, self.head)
    def __iter__(self):
        n = self.head
        while n:
            yield n
            n = n.nxt

L = LL([3, 6, 7, 9, 10, 12, 13])
seen = []
for node in L:
    seen.append(node.v)
    if node.v % 3 == 0 and node.nxt:
        node.nxt = node.nxt.nxt
print(seen, [n.v for n in L])''',
            'options': [
                '`[3, 7, 9, 12] [3, 7, 9, 12]`',
                '`[3, 6, 7, 9, 10, 12, 13] [3, 7, 9, 12]`',
                '`[3, 6, 9, 12] [3, 7, 9, 12]`',
                '`[3, 7, 9, 12] [3, 6, 7, 9, 10, 12, 13]`',
            ],
            'answer': 'A',
            'solution': '''The generator is **lazy**: after yielding node n it pauses, and only when resumed does it read `n.nxt`. Any change the loop body makes to `node.nxt` is therefore seen by the iteration.

- Yield 3: 3 % 3 == 0 → 3.nxt = 7 (6 unlinked). Generator resumes: n = 3.nxt = **7**.
- Yield 7: not a multiple of 3. Next: 9.
- Yield 9: 9.nxt = 12 (10 unlinked). Next: 12.
- Yield 12: 12.nxt = None (13 unlinked). Next: None → stop.

`seen` = [3, 7, 9, 12]; the list itself is now 3 → 7 → 9 → 12.

- (B) assumes the generator took a snapshot of the list.
- (C) assumes the removal takes effect one step late (visiting 6).
- (D) assumes the iteration worked on a copy and the list is unchanged.

**Trap:** generators do not copy their source; mutating a structure while iterating over it changes what the iterator produces.''',
            'verify': '''
assert OUTPUT.strip() == '[3, 7, 9, 12] [3, 7, 9, 12]' and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BFS — counting shortest paths',
            'text': 'In the unweighted undirected graph shown below, the number of distinct **shortest** paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'T'],
                        ['G', 'T'],
                        ['C', 'D'],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 2.6],
                        'D': [3, 1],
                        'E': [3, -0.6],
                        'F': [4.5, 2],
                        'G': [4.5, 0],
                        'T': [6, 1],
                    },
                },
            ],
            'answer': '6',
            'solution': '''BFS assigns levels; the number of shortest paths to v is the sum of the counts of its neighbours on the **previous** level: σ(v) = Σ σ(u) over edges u–v with d(u) = d(v) − 1.

- Level 0: S (σ = 1)
- Level 1: A (1), B (1)
- Level 2: C (from A: 1), D (from A and B: 2), E (from B: 1)
- Level 3: F (from C and D: 1 + 2 = 3), G (from D and E: 2 + 1 = 3)
- Level 4: T (from F and G: 3 + 3 = **6**)

The edge C–D joins two vertices on the *same* level, so it lies on no shortest path.

**Trap:** adding paths that use C–D (e.g. S-A-C-D-G-T, length 5) or counting all simple paths instead of shortest ones.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS level d and path count σ',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'T'],
                    'row_labels': ['d', 'σ'],
                    'rows': [
                        [0, 1, 1, 2, 2, 2, 3, 3, 4],
                        [1, 1, 1, 1, 2, 1, 3, 3, 6],
                    ],
                    'highlight': [
                        [1, 8],
                    ],
                },
            ],
            'verify': '''
from collections import deque
E = [('S','A'),('S','B'),('A','C'),('A','D'),('B','D'),('B','E'),('C','F'),('D','F'),
     ('D','G'),('E','G'),('F','T'),('G','T'),('C','D')]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
def allpaths(u, path):
    if u == 'T': yield path; return
    for v in G[u]:
        if v not in path: yield from allpaths(v, path + [v])
P = list(allpaths('S', ['S']))
m = min(len(p) for p in P)
assert sum(1 for p in P if len(p) == m) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Sorted list to balanced BST',
            'text': 'A sorted linked list 1 → 2 → … → 10 is converted into a BST recursively: for the sub-list at positions lo..hi (0-based), the node at position m = ⌊(lo + hi)/2⌋ becomes the root, and positions lo..m−1 and m+1..hi build the left and right subtrees. Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)',
            'options': [
                'The BST has exactly 5 leaves',
                'The height of the BST is 4',
                'The root of the BST is 5',
                'The pre-order traversal is 5, 2, 1, 3, 4, 8, 6, 7, 9, 10',
            ],
            'answer': ['C', 'D'],
            'solution': '''Choosing the (lower) middle as root at every level gives a height-balanced BST.

- Whole list, positions 0..9: m = 4 → root **5**. Left = {1..4}, right = {6..10}.
- {1, 2, 3, 4} (0..3): m = 1 → 2; left {1}; right {3, 4} → m = 2 → 3 with right child 4.
- {6, …, 10} (5..9): m = 7 → 8; left {6, 7} → 6 with right child 7; right {9, 10} → 9 with right child 10.

Tree: 5 → (2 → 1, (3 → –, 4)), (8 → (6 → –, 7), (9 → –, 10)).

- (A) Leaves are 1, 4, 7, 10 — four. **False.**
- (B) Longest paths, e.g. 5 → 2 → 3 → 4, have 3 edges; height = 3. **False.**
- (C) **True.**
- (D) Pre-order 5, 2, 1, 3, 4, 8, 6, 7, 9, 10. **True.**

**Trap:** using the upper middle ⌈(lo+hi)/2⌉ would make 6 the root; read the rounding rule. Note the height ⌊log₂ 10⌋ = 3 is optimal for 10 keys.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        5,
                        [
                            2,
                            [1],
                            [
                                3,
                                None,
                                [4],
                            ],
                        ],
                        [
                            8,
                            [
                                6,
                                None,
                                [7],
                            ],
                            [
                                9,
                                None,
                                [10],
                            ],
                        ],
                    ],
                    'caption': 'Balanced BST built from the sorted list',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def build(lo, hi):
    if lo > hi: return None
    m = (lo + hi) // 2
    return [m + 1, build(lo, m - 1), build(m + 1, hi)]
T = build(0, 9)
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
def lv(t):
    if t is None: return 0
    return 1 if t[1] is None and t[2] is None else lv(t[1]) + lv(t[2])
truth = {'A': T[0] == 5, 'B': ht(T) == 4, 'C': pre(T) == [5,2,1,3,4,8,6,7,9,10], 'D': lv(T) == 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort on a linked list — comparisons',
            'text': 'Merge sort is applied to the linked list 21 → 7 → 33 → 14 → 2 → 40 → 19 → 11 → 28. A list of length L > 1 is split into its first ⌈L/2⌉ nodes and the remaining ⌊L/2⌋ nodes; both halves are sorted recursively and merged by the standard merge (compare heads; once one list is empty, attach the rest without comparisons). The total number of key comparisons is ______.',
            'answer': '20',
            'solution': '''Split tree: [21 7 33 14 2] + [40 19 11 28]; [21 7 33] + [14 2]; [21 7] + [33]; [40 19] + [11 28].

Merges (bottom-up) with comparison counts:
- [21] + [7] → [7, 21]: 1
- [7, 21] + [33] → 7 vs 33, 21 vs 33, then attach 33: 2
- [14] + [2] → [2, 14]: 1
- [7, 21, 33] + [2, 14] → 7 vs 2 (2), 7 vs 14 (7), 21 vs 14 (14), then attach: 3
- [40] + [19] → 1; [11] + [28] → 1
- [19, 40] + [11, 28] → 19 vs 11, 19 vs 28, 40 vs 28, then attach 40: 3
- [2, 7, 14, 21, 33] + [11, 19, 28, 40] → 2/11, 7/11, 14/11, 14/19, 21/19, 21/28, 33/28, 33/40, then attach 40: 8

Total = 1 + 2 + 1 + 3 + 1 + 1 + 3 + 8 = **20**.

**Tip:** each merge of sizes a, b costs between min(a, b) and a + b − 1 comparisons, so the total for n = 9 lies between 13 and 25 — a quick sanity check on any trace.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Merges performed',
                    'col_labels': ['left', 'right', 'result', 'comparisons'],
                    'row_labels': ['1', '2', '3', '4', '5', '6', '7', '8'],
                    'rows': [
                        ['21', '7', '7 21', 1],
                        ['7 21', '33', '7 21 33', 2],
                        ['14', '2', '2 14', 1],
                        ['7 21 33', '2 14', '2 7 14 21 33', 3],
                        ['40', '19', '19 40', 1],
                        ['11', '28', '11 28', 1],
                        ['19 40', '11 28', '11 19 28 40', 3],
                        ['2 7 14 21 33', '11 19 28 40', 'all 9 keys', 8],
                    ],
                },
            ],
            'verify': '''
cmp = 0
def ms(a):
    global cmp
    if len(a) <= 1: return a
    m = (len(a) + 1) // 2
    L, R = ms(a[:m]), ms(a[m:])
    o = []; i = j = 0
    while i < len(L) and j < len(R):
        cmp += 1
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
assert ms([21, 7, 33, 14, 2, 40, 19, 11, 28]) == sorted([21, 7, 33, 14, 2, 40, 19, 11, 28])
assert cmp == int(ANSWER)
''',
        },
    ],
}
