# Set 04 — Linked Lists (Moderate)
SET = {
    'number': 4,
    'title': 'Linked Lists',
    'difficulty': 'Moderate',
    'focus': 'singly/doubly/circular lists, pointer manipulation, traversal costs',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — pointer manipulation in Python',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

head = None
for v in [7, 3, 9, 4, 6]:
    head = Node(v, head)
p = head
while p.next and p.next.next:
    p.next = p.next.next
    p = p.next
out = []
while head:
    out.append(head.val)
    head = head.next
print(out)''',
            'options': ['`[6, 4, 9, 3, 7]`', '`[7, 9, 6]`', '`[6, 9, 7]`', '`[6, 9]`'],
            'answer': 'C',
            'solution': '''**Concept.** `head = Node(v, head)` inserts every new node at the *front*, so the list is built in reverse order of the loop. The second loop then bypasses every second node.

**Trace.**
- After building: head → 6 → 4 → 9 → 3 → 7 → None.
- p = 6: p.next (4) and p.next.next (9) exist → 6.next = 9, p = 9.
- p = 9: p.next (3) and p.next.next (7) exist → 9.next = 7, p = 7.
- p = 7: p.next is None → loop stops.
- Final list: 6 → 9 → 7, printed as `[6, 9, 7]`.

**Options.**
- (A) Ignores the deletions made by the `while` loop.
- (B) Assumes the list is in insertion order 7, 3, 9, 4, 6 — but front insertion reverses it.
- (C) Correct.
- (D) Would require 7 to be skipped too; after `p = 9`, the node 7 is the new successor and the loop moves onto it instead of deleting it.

**Trap:** forgetting that prepending reverses order, and that `p = p.next` moves onto the node that was *kept*, so deletions are alternate, not consecutive.''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [6, 4, 9, 3, 7],
                    'head': 'head',
                    'caption': 'List after the building loop',
                },
            ],
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [6, 9, 7],
                    'head': 'head',
                    'caption': 'List after bypassing alternate nodes',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[6, 9, 7]'
# independent recomputation using Python lists
L = []
for v in [7, 3, 9, 4, 6]:
    L.insert(0, v)
kept = L[0::2]
assert kept == [6, 9, 7] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Doubly linked lists — unlink and move',
            'text': 'The program below builds the doubly linked list shown in the figure and then performs two pointer operations. What value does it print?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [12, 5, 8, 20, 3],
                    'doubly': True,
                    'head': 'head',
                    'tail': 'tail',
                    'caption': 'Initial doubly linked list',
                },
            ],
            'code': '''class D:
    def __init__(self, v):
        self.v, self.prev, self.next = v, None, None

nodes = [D(v) for v in [12, 5, 8, 20, 3]]
for a, b in zip(nodes, nodes[1:]):
    a.next, b.prev = b, a
head, tail = nodes[0], nodes[-1]

x = head.next.next
x.prev.next = x.next
x.next.prev = x.prev

t = tail
tail = t.prev
tail.next = None
t.next, head.prev = head, t
head = t

p, s, i = head, 0, 0
while p:
    s += i * p.v
    i, p = i + 1, p.next
print(s)''',
            'answer': '82',
            'solution': '''**Concept.** Unlinking an interior node x of a doubly linked list needs exactly two pointer writes: `x.prev.next = x.next` and `x.next.prev = x.prev`. Moving the tail to the front needs the old tail's predecessor (available in O(1) through `prev`).

**Trace.**
- `x = head.next.next` is the node 8. After the two writes, the list is 12 ⇄ 5 ⇄ 20 ⇄ 3.
- `t` = node 3; `tail` becomes 20 and `20.next = None`.
- `3.next = 12`, `12.prev = 3`, `head = 3`. The list is 3 ⇄ 12 ⇄ 5 ⇄ 20.
- The final loop computes ∑ i × value with 0-based position i:
  0×3 + 1×12 + 2×5 + 3×20 = 0 + 12 + 10 + 60 = **82**.

**Trap:** students often think the removed node 8 is still reachable (it is not — no forward pointer leads to it any more), or forget that position counting starts at 0 for the new head 3. Using 1-based weights would give 3 + 24 + 15 + 80 = 122.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 12, 5, 20],
                    'doubly': True,
                    'head': 'head',
                    'tail': 'tail',
                    'caption': 'Final list',
                },
            ],
            'verify': '''
L = [12, 5, 8, 20, 3]
L.remove(8)
L = [L[-1]] + L[:-1]
assert L == [3, 12, 5, 20]
assert sum(i * v for i, v in enumerate(L)) == int(ANSWER)
assert OUTPUT.strip() == ANSWER
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Queues using linked lists — operation costs',
            'text': 'A FIFO queue holding n elements is implemented with a singly linked list (each node has only a `next` field). Which of the following statements is/are TRUE?',
            'options': [
                'If the list is non-circular and only a head pointer is kept, enqueue at the tail takes Θ(n) time',
                'If both head and tail pointers are kept, enqueuing at the tail and dequeuing at the head both take O(1) worst-case time',
                'If the list is circular and only a pointer to the last node is kept, both enqueue and dequeue take O(1) worst-case time',
                'If both head and tail pointers are kept, enqueuing at the head and dequeuing at the tail both take O(1) worst-case time',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** In a singly linked list you can insert after any node you hold, and delete the node *after* any node you hold, in O(1). Deleting a node needs its predecessor.

- (A) **True.** Without a tail pointer, reaching the last node needs n − 1 hops.
- (B) **True.** Enqueue: `tail.next = new; tail = new`. Dequeue: `head = head.next`. Both O(1).
- (C) **True.** With a circular list and pointer `last`, the front is `last.next`. Enqueue: `new.next = last.next; last.next = new; last = new`. Dequeue: `last.next = last.next.next`. Both O(1) — one pointer suffices.
- (D) **False.** Dequeuing at the tail needs the predecessor of the tail so that its `next` can be set to None; finding it requires walking from the head — Θ(n).

**Tip:** the circular-list-with-last-pointer trick is a favourite GATE question — it gives both ends for the price of one pointer.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

class N:
    def __init__(s, v): s.v, s.next = v, None
# circular queue with only `last`: count hops, must not depend on n
def run(n):
    last, hops = None, 0
    for v in range(n):
        x = N(v)
        if last is None: x.next = x
        else: x.next, last.next = last.next, x
        last = x
    out = []
    for _ in range(n):
        f = last.next; hops += 1
        out.append(f.v)
        if f is last: last = None
        else: last.next = f.next
    return out, hops / n
o, h = run(50)
assert o == list(range(50)) and h == 1.0
assert sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing with negative steps',
            'text': 'What is printed by the following Python statements?',
            'code': '''s = "LINKEDLIST"
print(s[-2:2:-2] + s[1::4])''',
            'options': ['`ELSIDT`', '`SLEKIDT`', '`TSLEIDT`', '`SLEIDT`'],
            'answer': 'D',
            'solution': '''**Concept.** A slice `s[a:b:c]` with c < 0 starts at a, moves left by |c|, and stops *before* reaching b. Negative indices count from the end (−1 is the last character).

Indices: L0 I1 N2 K3 E4 D5 L6 I7 S8 T9.

- `s[-2:2:-2]`: start at −2 = index 8 (S), then 6 (L), 4 (E); the next index 2 is the stop bound, so it is excluded → `"SLE"`.
- `s[1::4]`: indices 1 (I), 5 (A), 9 (T) → `"IDT"`.
- Concatenation → `SLEIDT`.

**Options.**
- (A) lists the first slice in increasing index order (4, 6, 8) — but a negative step walks right-to-left.
- (B) wrongly includes index 3 (K) — but stepping by −2 from 8 never lands on 3.
- (C) starts at index 9 (T), confusing −2 with −1.

**Trap:** the stop index is exclusive in both directions, and the step decides which indices are actually visited.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

s = "LINKEDLIST"
r = "".join(s[i] for i in range(8, 2, -2)) + "".join(s[i] for i in range(1, 10, 4))
assert r == OUTPUT.strip() == "SLEIDT" and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression

`8 2 5 * + 1 3 2 * + 4 - /`

is evaluated with an operand stack in the usual way (push operands; for an operator pop two, apply, push the result). The maximum number of elements present on the stack at any instant during the evaluation is ______.''',
            'answer': '4',
            'solution': '''**Concept.** Each operand is pushed; each binary operator pops two and pushes one (net −1). The peak depth is reached just before an operator that follows a long run of operands.

**Trace** (stack shown bottom → top):
- 8 → [8]; 2 → [8, 2]; 5 → [8, 2, 5] (size 3).
- * → [8, 10]; + → [18].
- 1 → [18, 1]; 3 → [18, 1, 3]; 2 → [18, 1, 3, 2] (size **4**).
- * → [18, 1, 6]; + → [18, 7]; 4 → [18, 7, 4]; − → [18, 3]; / → [6].

Maximum size = **4** (the expression's value is 6).

**Trap:** answering 3 by looking only at the first operand run, or forgetting that the earlier partial result 18 is still sitting at the bottom of the stack.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [18, 1, 3, 2],
                    'label': 'peak (before 2nd *)',
                    'caption': 'Stack at its maximum depth',
                },
            ],
            'verify': '''
tok = "8 2 5 * + 1 3 2 * + 4 - /".split()
st, mx = [], 0
for t in tok:
    if t in "+-*/":
        b, a = st.pop(), st.pop()
        st.append({'+': a+b, '-': a-b, '*': a*b, '/': a/b}[t])
    else:
        st.append(int(t))
    mx = max(mx, len(st))
assert mx == int(ANSWER) and st == [6]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'Keys 19, 26, 13, 40, 33, 20, 6, 14 are inserted, in this order, into an initially empty hash table with 7 slots (0–6), hash function h(k) = k mod 7, and separate chaining in which every new key is inserted at the **front** of its chain. Reading the chain of slot 5 from front to back gives',
            'options': ['19, 26, 40, 33', '33, 26, 40, 19', '40, 33, 26, 19', '33, 40, 26, 19'],
            'answer': 'D',
            'solution': '''**Concept.** With front insertion, a chain lists its keys in *reverse* order of arrival.

**Hash values.** 19 → 5, 26 → 5, 13 → 6, 40 → 5, 33 → 5, 20 → 6, 6 → 6, 14 → 0.

Slot 5 receives 19, 26, 40, 33 in that order. Front insertion gives:
- after 19: [19]
- after 26: [26, 19]
- after 40: [40, 26, 19]
- after 33: [33, 40, 26, 19]

**Options.**
- (A) is the order for *tail* insertion.
- (B) is not obtainable by either policy.
- (C) swaps the last two arrivals.

**Tip:** front insertion is the default in textbook chaining because it is O(1) without a tail pointer; a successful search for 19 now costs 4 key comparisons.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: [14],
                        5: [33, 40, 26, 19],
                        6: [6, 20, 13],
                    },
                    'caption': 'Final table (chains shown front → back)',
                },
            ],
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

T = [[] for _ in range(7)]
for k in [19, 26, 13, 40, 33, 20, 6, 14]:
    T[k % 7].insert(0, k)
opts = {'A': [19, 26, 40, 33], 'B': [33, 40, 26, 19],
        'C': [40, 33, 26, 19], 'D': [33, 26, 40, 19]}
assert [o for o in opts if opts[o] == T[5]] == [ANSWER]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — probe sequence',
            'text': 'Binary search with `mid = (lo + hi) // 2` (0-based indices, initially lo = 0, hi = 11) is applied to the sorted array A below to search for the key **47**. The sequence of array **values** compared with the key is',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [4, 9, 13, 18, 22, 27, 31, 36, 40, 45, 51, 58],
                    'label': 'A',
                    'caption': 'Sorted array A[0..11]',
                },
            ],
            'options': ['31, 45, 58, 51', '27, 40, 51, 45', '27, 40, 45', '27, 40, 51, 45, 51'],
            'answer': 'B',
            'solution': '''**Concept.** Each probe halves the interval [lo, hi]; the search ends unsuccessfully when lo > hi.

**Trace.**
- lo = 0, hi = 11 → mid = 5, A[5] = 27 < 47 → lo = 6.
- lo = 6, hi = 11 → mid = 8, A[8] = 40 < 47 → lo = 9.
- lo = 9, hi = 11 → mid = 10, A[10] = 51 > 47 → hi = 9.
- lo = 9, hi = 9 → mid = 9, A[9] = 45 < 47 → lo = 10 > hi → stop (not found).

Values compared: **27, 40, 51, 45**.

**Options.**
- (A) uses the *ceiling* midpoint ⌈(lo+hi)/2⌉ (6, 9, 11, 10).
- (C) stops one probe early — after 51 the interval [9, 9] is still non-empty.
- (D) probes 51 twice, which never happens because hi moves past it.

**Trap:** always recompute mid with floor division and update lo/hi to mid ± 1.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

A = [4, 9, 13, 18, 22, 27, 31, 36, 40, 45, 51, 58]
lo, hi, seq = 0, 11, []
while lo <= hi:
    m = (lo + hi) // 2; seq.append(A[m])
    if A[m] == 47: break
    lo, hi = (m + 1, hi) if A[m] < 47 else (lo, m - 1)
assert seq == [27, 40, 51, 45] and ANSWER == 'A'
lo, hi, seq2 = 0, 11, []
while lo <= hi:
    m = (lo + hi + 1) // 2; seq2.append(A[m])
    lo, hi = (m + 1, hi) if A[m] < 47 else (lo, m - 1)
assert seq2 == [31, 45, 58, 51]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort — intermediate state',
            'text': 'Insertion sort (ascending) is applied to the array [31, 12, 47, 8, 25, 19]. In pass i (i = 1, 2, …, 5) the element at index i is inserted into the sorted prefix A[0..i−1]. What is the array immediately after pass 3 completes?',
            'options': [
                '[8, 12, 31, 47, 25, 19]',
                '[12, 31, 47, 8, 25, 19]',
                '[8, 12, 25, 31, 47, 19]',
                '[8, 12, 31, 25, 47, 19]',
            ],
            'answer': 'A',
            'solution': '''**Concept.** After pass i of insertion sort, the prefix A[0..i] is sorted and contains exactly the original first i + 1 elements; the suffix is untouched.

**Trace.**
- Pass 1 (insert 12): [12, 31, 47, 8, 25, 19].
- Pass 2 (insert 47): no shift → [12, 31, 47, 8, 25, 19].
- Pass 3 (insert 8): shift 47, 31, 12 right → [8, 12, 31, 47, 25, 19].

**Options.**
- (B) is the state after pass 2.
- (C) is the state after pass 4 — 25 has been inserted too.
- (D) mixes 25 into the prefix without fully sorting it — insertion sort never produces this.

**Contrast:** selection sort after 3 passes would instead hold the 3 *smallest overall* (8, 12, 19) at the front. Insertion sort's prefix is sorted but not final.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'row_labels': ['start', 'pass 1', 'pass 2', 'pass 3'],
                    'rows': [
                        [31, 12, 47, 8, 25, 19],
                        [12, 31, 47, 8, 25, 19],
                        [12, 31, 47, 8, 25, 19],
                        [8, 12, 31, 47, 25, 19],
                    ],
                    'highlight': [
                        [3, 0],
                        [3, 1],
                        [3, 2],
                        [3, 3],
                    ],
                },
            ],
            'verify': '''
A = [31, 12, 47, 8, 25, 19]
for i in range(1, 4):
    x, j = A[i], i - 1
    while j >= 0 and A[j] > x:
        A[j + 1] = A[j]; j -= 1
    A[j + 1] = x
assert A == [8, 12, 31, 47, 25, 19] and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph traversal — valid BFS orders',
            'text': 'Consider the undirected graph below. Breadth-first search is started at vertex A; the neighbours of a vertex may be enqueued in **any** order. Which of the following is/are possible BFS visiting orders?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
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
                        'A': [2, 4],
                        'B': [0, 2.5],
                        'C': [2, 2.5],
                        'D': [4, 2.5],
                        'E': [1, 1],
                        'F': [3, 1],
                        'G': [2, -0.5],
                    },
                },
            ],
            'options': [
                'A, B, C, D, F, E, G',
                'A, B, C, D, E, F, G',
                'A, C, B, D, F, E, G',
                'A, D, C, B, F, E, G',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept.** In BFS, when a vertex u is dequeued, all its *not-yet-discovered* neighbours are enqueued together. So the next-level vertices appear grouped by the parent that discovered them, in the order of the parents.

Level 1 = {B, C, D} in any order; level 2 = {E, F}; level 3 = {G}.

- (A) B is dequeued first and discovers E, so E must come before F. **Invalid.**
- (B) B first discovers E; C then discovers F; D nothing. Order E, F. **Valid.**
- (C) C is dequeued first and discovers both E and F (any order, here F then E); B and D add nothing. **Valid.**
- (D) D first discovers F; C then discovers E; B nothing new. Order F, E. **Valid.**

**Trap:** checking only the *levels* is not enough — (A) has correct levels but violates the FIFO order of discovery.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'A': 'BCD', 'B': 'AE', 'C': 'AEF', 'D': 'AF', 'E': 'BCG',
     'F': 'CDG', 'G': 'EF'}
def ok(seq):
    seq = seq.replace(', ', '')
    if seq[0] != 'A': return False
    seen, q, k = {'A'}, ['A'], 1
    while q:
        u = q.pop(0)
        new = {v for v in G[u] if v not in seen}
        block = seq[k:k + len(new)]
        if set(block) != new: return False
        for v in block: seen.add(v); q.append(v)
        k += len(new)
    return k == len(seq)
opts = ["A, B, C, D, E, F, G", "A, D, C, B, F, E, G",
        "A, B, C, D, F, E, G", "A, C, B, D, F, E, G"]
good = [L for L, s in zip("ABCD", opts) if ok(s)]
assert good == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary heaps — insertion swaps',
            'text': 'The keys 40, 35, 50, 20, 45, 10, 30, 15 are inserted one by one, in this order, into an initially empty binary **min**-heap (array representation, sift-up after each insertion). The total number of parent–child swaps performed over all eight insertions is ______.',
            'answer': '7',
            'solution': '''**Concept.** Insertion places the key at the next free leaf and swaps it with its parent while it is smaller than the parent. Parent of index i is (i − 1) // 2.

**Trace** (heap array after each insertion, swaps in brackets):
- 40 → [40] (0)
- 35 → [35, 40] (1)
- 50 → [35, 40, 50] (0)
- 20 → at index 3, swaps with 40, then with 35 → [20, 35, 50, 40] (2)
- 45 → parent 35 < 45 → [20, 35, 50, 40, 45] (0)
- 10 → swaps with 50, then with 20 → [10, 35, 20, 40, 45, 50] (2)
- 30 → parent 20 < 30 → [10, 35, 20, 40, 45, 50, 30] (0)
- 15 → swaps with 40, then with 35; parent 10 < 15 stops → [10, 15, 20, 35, 45, 50, 30, 40] (2)

Total = 1 + 2 + 2 + 2 = **7**.

**Trap:** do not count the final comparison that stops sift-up as a swap, and do not confuse repeated insertion with bottom-up build-heap (which would perform a different number of swaps).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [10, 15, 20, 35, 45, 50, 30, 40],
                    'caption': 'Final min-heap',
                },
            ],
            'verify': '''
h, sw = [], 0
for x in [40, 35, 50, 20, 45, 10, 30, 15]:
    h.append(x); i = len(h) - 1
    while i and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p; sw += 1
assert sw == int(ANSWER) and h == [10, 15, 20, 35, 45, 50, 30, 40]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — reversal in groups of k',
            'text': 'The singly linked list shown below holds one character per node. Consider the following Python program, which uses the function `rev_k`. What is printed?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': ['P', 'Y', 'T', 'H', 'O', 'N', 'I', 'C'],
                    'head': 'head',
                    'caption': 'Input list',
                },
            ],
            'code': '''class Node:
    def __init__(self, val):
        self.val, self.next = val, None

def rev_k(head, k):
    prev, cur, n = None, head, 0
    while cur and n < k:
        cur.next, prev, cur = prev, cur, cur.next
        n += 1
    if cur:
        head.next = rev_k(cur, k)
    return prev

head = None
for ch in reversed("PYTHONIC"):
    nd = Node(ch); nd.next = head; head = nd
head = rev_k(head, 3)
s = ""
while head:
    s, head = s + head.val, head.next
print(s)''',
            'options': ['`TYPNOHIC`', '`TYPNOHCI`', '`CINOHTYP`', '`TYPHONCI`'],
            'answer': 'B',
            'solution': '''**Concept.** `rev_k` reverses the first k nodes in place, then links the *old* head (which is now the last node of the reversed block) to the result of recursively processing the rest. A final block with fewer than k nodes is also reversed, because the `while` loop simply stops when `cur` becomes None.

**The tuple assignment.** In `cur.next, prev, cur = prev, cur, cur.next` the right side is evaluated first, giving (old prev, old cur, old cur.next); then targets are assigned left to right. `cur.next` is assigned while `cur` still refers to the old node, so the step is a correct pointer reversal.

**Trace.**
- Block 1: P Y T → T Y P; P.next ← rev_k(H…).
- Block 2: H O N → N O H; H.next ← rev_k(I…).
- Block 3: I C (only 2 nodes) → C I; `cur` is None, so no further call.
- Result: T Y P N O H C I → `TYPNOHCI`.

**Options.**
- (A) assumes an incomplete last group is left as is (that variant needs a length check first).
- (C) is a full reversal of the whole list.
- (D) reverses only the first group.

**Trap:** if the targets were written as `prev, cur, cur.next = cur, cur.next, prev`, `cur.next` would be assigned on the *new* cur and the list would be corrupted — order of targets matters.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': ['T', 'Y', 'P', 'N', 'O', 'H', 'C', 'I'],
                    'head': 'head',
                    'caption': 'Output list',
                },
            ],
            'verify': '''
s = "PYTHONIC"
exp = "".join(s[i:i + 3][::-1] for i in range(0, len(s), 3))
assert exp == OUTPUT.strip() == "TYPNOHCI" and ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': "Linked lists — Floyd's cycle detection",
            'text': '''A singly linked list has nodes 1, 2, …, 9 linked in order, and the `next` pointer of node 9 points back to node 4 (see figure). Floyd's algorithm is run:

- **Phase 1:** `slow` and `fast` both start at node 1. In each step, `slow` moves one node and `fast` moves two nodes; the step count m is the number of steps until they are first on the same node.
- **Phase 2:** `slow` is reset to node 1, `fast` stays where they met; both now move one node per step until they meet; let r be the number of steps of this phase.

The value of m + r is ______.''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                    'edges': [
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '4'],
                        ['4', '5'],
                        ['5', '6'],
                        ['6', '7'],
                        ['7', '8'],
                        ['8', '9'],
                        ['9', '4'],
                    ],
                    'pos': {
                        '1': [0, 1],
                        '2': [1.3, 1],
                        '3': [2.6, 1],
                        '4': [3.9, 1],
                        '5': [5.2, 2],
                        '6': [6.5, 2],
                        '7': [7.8, 1],
                        '8': [6.5, 0],
                        '9': [5.2, 0],
                    },
                },
            ],
            'answer': '9',
            'solution': '''**Concept.** If the tail before the cycle has μ nodes and the cycle has length λ, then phase 1 ends at a step count that is a multiple of λ and ≥ μ, and phase 2 always takes exactly μ steps, ending at the first node of the cycle.

Here μ = 3 (nodes 1, 2, 3) and λ = 6 (cycle 4 → 5 → … → 9 → 4).

**Phase 1 trace** (slow, fast after each step):
- step 1: (2, 3)
- step 2: (3, 5)
- step 3: (4, 7)
- step 4: (5, 9)
- step 5: (6, 5)  [fast: 9 → 4 → 5]
- step 6: (7, 7)  → meet. **m = 6**.

**Phase 2 trace** (slow from 1, fast from 7, one step each):
- (2, 8), (3, 9), (4, 4) → meet at node 4, the cycle entry. **r = 3**.

m + r = 6 + 3 = **9**.

**Check with the theory:** m is the smallest multiple of λ = 6 that is ≥ μ = 3, i.e. 6; r = μ = 3.

**Trap:** counting the starting position as a step, or moving `fast` only once in the step when it wraps from 9 to 4.''',
            'verify': '''
nxt = {i: i + 1 for i in range(1, 9)}; nxt[9] = 4
s = f = 1; m = 0
while True:
    s = nxt[s]; f = nxt[nxt[f]]; m += 1
    if s == f: break
s, r = 1, 0
while s != f:
    s, f, r = nxt[s], nxt[f], r + 1
assert (m, r, s) == (6, 3, 4) and m + r == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Circular linked lists — elimination game',
            'text': 'What value is printed by the following Python program?',
            'code': '''class Node:
    def __init__(self, v):
        self.v, self.next = v, None

n, k = 11, 4
first = Node(1)
p = first
for v in range(2, n + 1):
    p.next = Node(v)
    p = p.next
p.next = first          # make it circular; p = last node
while p.next is not p:
    for _ in range(k - 1):
        p = p.next
    p.next = p.next.next
print(p.v)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, '…', 10, 11],
                    'circular': True,
                    'head': 'first',
                    'caption': 'Circular list before the elimination loop',
                },
            ],
            'answer': '9',
            'solution': '''**Concept.** `p` always sits on the node *before* the one to be removed. Starting from the last node, moving k − 1 = 3 steps lands on the node preceding the 4th node, which is then unlinked. This is the Josephus problem with n = 11, k = 4 (every 4th person removed, counting resumes from the node after the removed one).

**Trace** (removed node each round, remaining circle after it):
- remove 4 → 1 2 3 5 6 7 8 9 10 11
- remove 8 → 1 2 3 5 6 7 9 10 11
- remove 1 → 2 3 5 6 7 9 10 11
- remove 6 → 2 3 5 7 9 10 11
- remove 11 → 2 3 5 7 9 10
- remove 7 → 2 3 5 9 10
- remove 3 → 2 5 9 10
- remove 2 → 5 9 10
- remove 5 → 9 10
- remove 10 → 9

Only node 9 remains, its `next` points to itself, the loop ends and **9** is printed.

**Cross-check** with the recurrence J(1) = 0, J(m) = (J(m−1) + k) mod m (0-based): J(11) = 8, i.e. person 9.

**Trap:** starting `p` at `first` instead of the last node shifts every removal by one and gives a different survivor.''',
            'verify': '''
j = 0
for m in range(2, 12):
    j = (j + 4) % m
assert j + 1 == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Doubly linked lists — deletion code',
            'text': '''A doubly linked list has nodes with fields `val`, `prev`, `next`; the first node has `prev = None` and the last node has `next = None`. The following function is meant to delete node x (which is in the list) and return the new head.

Which of the following statements is/are TRUE?''',
            'code': '''def remove(head, x):
    x.prev.next = x.next
    if x.next:
        x.next.prev = x.prev
    if x is head:
        head = x.next
    return head''',
            'run_code': False,
            'options': [
                'Called on a one-node list (x is head), it returns None without raising an error',
                'It correctly deletes any node that is neither the first nor the last node',
                'It correctly deletes the last node of a list having at least two nodes',
                'It correctly deletes the first node of a list having at least two nodes',
            ],
            'answer': ['B', 'C'],
            'solution': '''**Concept.** Deleting x needs `x.prev.next = x.next` (unless x is first) and `x.next.prev = x.prev` (unless x is last). Every dereference of `x.prev` or `x.next` must be guarded by a None check.

- (A) **False.** Same reason: the single node is also the first node, `x.prev` is None, and an `AttributeError` is raised.
- (B) **True.** Interior node: both neighbours exist; the two writes splice them together, and `x is head` is false.
- (C) **True.** Last node: `x.prev` exists, so `x.prev.next = None`; the `if x.next` guard skips the second write. The predecessor becomes the new last node.
- (D) **False.** For the first node `x.prev` is None, so the very first line evaluates `None.next = …` and raises `AttributeError` before the `x is head` check is reached.

**Fix:** write `if x.prev: x.prev.next = x.next` `else: head = x.next` — i.e. test the head case *before* dereferencing `x.prev`.

**Trap:** the head check exists in the code, so it *looks* handled — but its position after the unguarded dereference makes it unreachable for the head node.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

class N:
    def __init__(s, v): s.val, s.prev, s.next = v, None, None
def build(vals):
    ns = [N(v) for v in vals]
    for a, b in zip(ns, ns[1:]): a.next, b.prev = b, a
    return ns
def fwd(h):
    o = []
    while h: o.append(h.val); h = h.next
    return o
def remove(head, x):
    x.prev.next = x.next
    if x.next:
        x.next.prev = x.prev
    if x is head:
        head = x.next
    return head
def test(vals, idx):
    ns = build(vals)
    try:
        h = remove(ns[0], ns[idx])
    except AttributeError:
        return False
    exp = vals[:idx] + vals[idx + 1:]
    if fwd(h) != exp: return False
    if h is None: return True
    t = h
    while t.next: t = t.next
    b = []
    while t: b.append(t.val); t = t.prev
    return b == exp[::-1]
res = {'A': test([1, 2, 3, 4], 2), 'B': test([1, 2, 3, 4], 3),
       'C': test([1, 2, 3, 4], 0), 'D': test([1], 0)}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linked lists — merging sorted lists',
            'text': 'The two sorted singly linked lists L1 and L2 shown below are merged into one sorted list by the standard merge procedure: repeatedly compare the front nodes of the two lists, detach the smaller (L1 on ties) and append it to the output; as soon as one list becomes empty, the remainder of the other is attached with a single pointer assignment, without any comparisons. The number of key comparisons performed is ______.',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 8, 15, 21, 30],
                    'head': 'L1',
                },
                {
                    'type': 'linkedlist',
                    'values': [5, 6, 17, 25, 40, 42],
                    'head': 'L2',
                },
            ],
            'answer': '9',
            'solution': '''**Concept.** Each comparison moves exactly one node to the output. The process stops when one list is empty, so #comparisons = (m + n) − (number of nodes left in the other list at that moment).

**Trace** (comparison → node moved):
1. 3 vs 5 → 3
2. 8 vs 5 → 5
3. 8 vs 6 → 6
4. 8 vs 17 → 8
5. 15 vs 17 → 15
6. 21 vs 17 → 17
7. 21 vs 25 → 21
8. 30 vs 25 → 25
9. 30 vs 40 → 30 → L1 is now empty.

The remaining 40 → 42 of L2 is attached with one pointer assignment. Comparisons = 11 − 2 = **9**.

**Bounds to remember:** merging lists of sizes m and n needs at least min(m, n) = 5 and at most m + n − 1 = 10 comparisons.

**Tip:** a linked-list merge needs no extra array — it only relinks `next` pointers, which is why merge sort is the preferred sort for linked lists.

**Trap:** answering m + n − 1 = 10 (the worst case) without tracing.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 5, 6, 8, 15, 17, 21, 25, 30, 40, 42],
                    'head': 'out',
                    'caption': 'Merged list',
                },
            ],
            'verify': '''
a = [3, 8, 15, 21, 30]; b = [5, 6, 17, 25, 40, 42]
i = j = c = 0; out = []
while i < len(a) and j < len(b):
    c += 1
    if a[i] <= b[j]: out.append(a[i]); i += 1
    else: out.append(b[j]); j += 1
out += a[i:] + b[j:]
assert out == sorted(a + b) and c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Recursion on linked lists',
            'text': 'Consider the following Python program. What is its complete output?',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def g(p, d=0):
    if p is None:
        return 0
    r = g(p.next, d + 1)
    if d % 2:
        print(p.val, end=" ")
    return p.val - r

head = None
for v in [3, 9, 1, 7, 4]:
    head = Node(v, head)
print(g(head))''',
            'options': ['`9 7 -8`', '`7 9 -8`', '`9 7 8`', '`4 1 3 -8`'],
            'answer': 'A',
            'solution': '''**Concept.** The recursive call is made *before* the print, so printing happens while the recursion unwinds — i.e. from the tail back towards the head. The return value is an alternating sum computed right to left.

**Step 1 — the list.** Front insertion of 3, 9, 1, 7, 4 gives head → 4 → 7 → 1 → 9 → 3.

**Step 2 — depths.** 4 (d=0), 7 (d=1), 1 (d=2), 9 (d=3), 3 (d=4). Odd depths: 7 and 9.

**Step 3 — unwinding.**
- g(None) = 0.
- d=4, node 3: no print, returns 3 − 0 = 3.
- d=3, node 9: prints `9`, returns 9 − 3 = 6.
- d=2, node 1: no print, returns 1 − 6 = −5.
- d=1, node 7: prints `7`, returns 7 − (−5) = 12.
- d=0, node 4: no print, returns 4 − 12 = −8.

The outer `print` then writes −8 on the same line → `9 7 -8`.

**Options.**
- (B) prints in forward order — that would need the print before the recursive call.
- (C) loses the sign: 4 − (7 − (1 − (9 − 3))) = −8, not 8.
- (D) prints even-depth nodes.

**Trap:** the output of `g` appears only after all the prints *inside* g, because the argument of the outer `print` must be fully evaluated first.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "9 7 -8" and ANSWER == 'B'
L = [4, 7, 1, 9, 3]
v = 0
for x in reversed(L):
    v = x - v
assert v == -8
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — shallow vs deep copy',
            'text': 'What is printed by the following Python program?',
            'code': '''import copy
a = [[1, 2], [3, 4]]
b = a[:]
c = copy.deepcopy(a)
b[0].append(5)
b[1] = [6]
c[0][0] = 9
print(a, b[0] is a[0], c[0])''',
            'options': [
                '`[[1, 2, 5], [6]] True [9, 2]`',
                '`[[1, 2], [3, 4]] False [9, 2]`',
                '`[[1, 2, 5], [3, 4]] True [9, 2]`',
                '`[[9, 2, 5], [3, 4]] True [9, 2]`',
            ],
            'answer': 'C',
            'solution': '''**Concept.** `a[:]` makes a *shallow* copy: a new outer list whose elements are the **same** inner list objects. `copy.deepcopy` recursively copies the inner lists too. Mutating an object is visible through every reference to it; rebinding a slot of one outer list is not.

**Trace.**
- `b = a[:]` → b is a new list, but `b[0] is a[0]` and `b[1] is a[1]`.
- `c` is completely independent.
- `b[0].append(5)` mutates the shared inner list → a[0] is now [1, 2, 5].
- `b[1] = [6]` rebinds only b's slot 1; a[1] is still [3, 4].
- `c[0][0] = 9` changes only c's private copy → c[0] = [9, 2].
- `b[0] is a[0]` is still True.

Output: `[[1, 2, 5], [3, 4]] True [9, 2]`.

**Options.**
- (A) treats `b[1] = [6]` as if it changed a — rebinding a slot never affects another list.
- (B) treats `a[:]` as a deep copy.
- (D) lets the deep copy's change leak back into a.

**Trap:** distinguish *mutation* (`append`, item assignment on a shared object) from *rebinding* (assigning a new object to a name or slot).''',
            'verify': '''
assert OUTPUT.strip() == "[[1, 2, 5], [3, 4]] True [9, 2]" and ANSWER == 'C'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': "Shortest paths — Dijkstra's algorithm trace",
            'text': "Dijkstra's algorithm is run from source S on the weighted directed graph below. Initially d[S] = 0 and every other d[v] = ∞. Each time a vertex u is extracted, every edge (u, v) is relaxed. Count one **update** every time some d[v] is strictly decreased (the first change from ∞ to a finite value counts as an update). The total number of updates is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['S', 'C', 9],
                        ['B', 'A', 3],
                        ['B', 'D', 8],
                        ['A', 'C', 1],
                        ['A', 'D', 4],
                        ['C', 'T', 6],
                        ['C', 'D', 1],
                        ['D', 'T', 2],
                    ],
                    'pos': {
                        'S': [0, 1.5],
                        'A': [2, 3],
                        'B': [2, 0],
                        'C': [4.5, 3],
                        'D': [4.5, 0],
                        'T': [6.5, 1.5],
                    },
                },
            ],
            'answer': '10',
            'solution': '''**Concept.** Dijkstra repeatedly extracts the unfinished vertex with the smallest tentative distance and relaxes its outgoing edges: d[v] ← min(d[v], d[u] + w(u, v)).

**Trace** (updates in brackets):
- Extract S (0): A = 7, B = 2, C = 9 [3 updates; total 3].
- Extract B (2): A = min(7, 5) = 5 ✓, D = 10 ✓ [2; total 5].
- Extract A (5): C = min(9, 6) = 6 ✓, D = min(10, 9) = 9 ✓ [2; total 7].
- Extract C (6): T = 12 ✓, D = min(9, 7) = 7 ✓ [2; total 9].
- Extract D (7): T = min(12, 9) = 9 ✓ [1; total 10].
- Extract T (9): no outgoing edges.

Total updates = **10**. Final distances: S 0, B 2, A 5, C 6, D 7, T 9; shortest path to T is S → B → A → C → D → T.

**Trap:** D is improved three times (10 → 9 → 7) — miscounting such repeated improvements is the usual error. A relaxation that does not decrease the value is *not* an update.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, 9, '∞', '∞'],
                        [0, 5, 2, 9, 10, '∞'],
                        [0, 5, 2, 6, 9, '∞'],
                        [0, 5, 2, 6, 7, 12],
                        [0, 5, 2, 6, 7, 9],
                    ],
                },
            ],
            'verify': '''
G = {'S': [('A', 7), ('B', 2), ('C', 9)], 'B': [('A', 3), ('D', 8)],
     'A': [('C', 1), ('D', 4)], 'C': [('T', 6), ('D', 1)],
     'D': [('T', 2)], 'T': []}
INF = float('inf')
d = {v: INF for v in G}; d['S'] = 0; done = set(); upd = 0
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: d[v])
    done.add(u)
    for v, w in G[u]:
        if d[u] + w < d[v]:
            d[v] = d[u] + w; upd += 1
assert upd == int(ANSWER) and d['T'] == 9
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': 'The Lomuto partition procedure below is called as `partition(A, 0, 6)` on A = [7, 2, 9, 4, 1, 8, 5]. Which of the following statements is/are TRUE?',
            'code': '''def partition(A, lo, hi):
    pivot, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1''',
            'run_code': False,
            'options': [
                'The number of swap statements executed (including the final one) is 3',
                'If the same procedure is then called on the right part [9, 8, 7], its pivot ends at the first position of that part, so the left sub-part is empty',
                'After the call A = [2, 4, 1, 5, 9, 8, 7]',
                'The returned index (final position of the pivot) is 3',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept.** Lomuto keeps A[lo..i] ≤ pivot. Each element ≤ pivot found by j is swapped into position i + 1; at the end the pivot is swapped into i + 1.

**Trace** (pivot 5):
- j=0: 7 > 5.
- j=1: 2 ≤ 5 → i=0, swap A[0], A[1] → [2, 7, 9, 4, 1, 8, 5] (swap 1).
- j=2: 9 > 5.
- j=3: 4 ≤ 5 → i=1, swap A[1], A[3] → [2, 4, 9, 7, 1, 8, 5] (swap 2).
- j=4: 1 ≤ 5 → i=2, swap A[2], A[4] → [2, 4, 1, 7, 9, 8, 5] (swap 3).
- j=5: 8 > 5.
- Final: swap A[3], A[6] → [2, 4, 1, 5, 9, 8, 7] (swap 4); return 3.

**Statements.**
- (A) **False** — 4 swap statements execute (3 in the loop + the final one).
- (B) **True** — for [9, 8, 7] the pivot 7 is the minimum, no j satisfies A[j] ≤ 7, i stays at lo − 1, and the pivot is swapped to the first position: [7, 8, 9] with an empty left part — the classic unbalanced split.
- (C) **True** — matches the trace.
- (D) **True** — returned index is 3 (three keys are smaller than 5).

**Trap:** forgetting the final pivot swap when counting swaps.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def partition(A, lo, hi):
    global SW
    pivot, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= pivot:
            i += 1; SW += 1
            A[i], A[j] = A[j], A[i]
    SW += 1
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1
SW = 0
A = [7, 2, 9, 4, 1, 8, 5]
p = partition(A, 0, 6)
t = {'A': p == 3, 'B': A == [2, 4, 1, 5, 9, 8, 7], 'C': SW == 3}
q = partition(A, 4, 6)
t['D'] = (q == 4)
assert sorted(k for k in t if t[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary search trees — deletion',
            'text': 'The BST shown below was built by inserting 41, 19, 63, 7, 28, 52, 88, 24, 33, 57, 71, 95, 30 in that order. Now key 41 is deleted and then key 19 is deleted; a node with two children is deleted by copying its **in-order successor** into it and deleting the successor. Which of the following statements about the final tree is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        41,
                        [
                            19,
                            [7],
                            [
                                28,
                                [24],
                                [
                                    33,
                                    [30],
                                    None,
                                ],
                            ],
                        ],
                        [
                            63,
                            [
                                52,
                                None,
                                [57],
                            ],
                            [
                                88,
                                [71],
                                [95],
                            ],
                        ],
                    ],
                    'caption': 'Initial BST',
                },
            ],
            'options': [
                'The root of the final tree is 52',
                'The final tree has exactly 4 leaves',
                'The pre-order traversal of the final tree begins 52, 24, 7, 28, 33',
                'The height of the final tree is 4',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** The in-order successor of a node with two children is the minimum of its right subtree; it has no left child, so removing it is a 0- or 1-child deletion.

**Delete 41.** Successor = leftmost node of the subtree rooted at 63 → 63 → 52 (no left child). Copy 52 into the root and delete the old 52, whose right child 57 moves up to become 63's left child.

**Delete 19.** 19 has two children; successor = leftmost of subtree 28 → 24 (a leaf). Copy 24 into 19's node and delete the leaf 24. Now 28 has no left child.

**Final tree:** 52 → left 24 (children 7 and 28), 28 → right 33, 33 → left 30; 52 → right 63 (children 57 and 88), 88 → children 71 and 95.

- (A) **True.**
- (B) **False** — the leaves are 7, 30, 57, 71, 95: five leaves.
- (C) **True** — pre-order is 52, 24, 7, 28, 33, 30, 63, 57, 88, 71, 95.
- (D) **True** — path 52 → 24 → 28 → 33 → 30 has 4 edges.

**Trap:** using the in-order *predecessor* (33 for 41) gives a completely different tree; always follow the convention stated in the question.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        52,
                        [
                            24,
                            [7],
                            [
                                28,
                                None,
                                [
                                    33,
                                    [30],
                                    None,
                                ],
                            ],
                        ],
                        [
                            63,
                            [57],
                            [
                                88,
                                [71],
                                [95],
                            ],
                        ],
                    ],
                    'highlight': [52, 24],
                    'caption': 'Final BST',
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    i = 1 if k < t[0] else 2
    t[i] = ins(t[i], k); return t
def dele(t, k):
    if t is None: return None
    if k < t[0]: t[1] = dele(t[1], k)
    elif k > t[0]: t[2] = dele(t[2], k)
    else:
        if t[1] is None: return t[2]
        if t[2] is None: return t[1]
        s = t[2]
        while s[1]: s = s[1]
        t[0] = s[0]; t[2] = dele(t[2], s[0])
    return t
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def lv(t):
    if t is None: return 0
    return 1 if not t[1] and not t[2] else lv(t[1]) + lv(t[2])
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
T = None
for k in [41, 19, 63, 7, 28, 52, 88, 24, 33, 57, 71, 95, 30]:
    T = ins(T, k)
T = dele(dele(T, 41), 19)
r = {'A': T[0] == 52, 'B': h(T) == 4, 'C': lv(T) == 4,
     'D': pre(T)[:5] == [52, 24, 7, 28, 33]}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
    ],
}
