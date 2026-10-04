# Set 07 — Heaps & Priority Queues
SET = {
    'number': 7,
    'title': 'Heaps & Priority Queues',
    'difficulty': 'Moderate',
    'focus': 'binary heaps, heapify, build-heap, k-th element, heap arrays',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — slicing with negative steps',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = [3, 8, 1, 9, 4, 7, 6]
print(a[-2:0:-2], a[::-3])''',
            'options': [
                '`[7, 9] [6, 9, 3]`',
                '`[7, 9, 8, 3] [6, 9, 3]`',
                '`[7, 9, 8] [6, 9, 3]`',
                '`[7, 9, 8] [3, 9, 6]`',
            ],
            'answer': 'C',
            'solution': '''With a negative step a slice walks **right to left**, starts at `start`, and stops *before* reaching `stop` (the stop index is always excluded).

- The list has 7 elements, so index −2 is index 5, i.e. the value 7.
- `a[-2:0:-2]` visits indices 5, 3, 1 and would next visit −1… but index 0 is the stop, so it halts after 1. Values: a[5]=7, a[3]=9, a[1]=8 → `[7, 9, 8]`.
- `a[::-3]` with omitted start/stop and a negative step starts at the last index 6 and goes down to the beginning: indices 6, 3, 0 → values 6, 9, 3 → `[6, 9, 3]`.

Option analysis:

- (A) Stops one step early — index 1 is still > 0, so it is included.
- (B) Wrongly includes the stop index 0 (value 3).
- (C) Correct.
- (D) Reverses the result of `a[::-3]`, as if the slice were taken left-to-right and then reversed.

**Trap:** the stop bound is exclusive in both directions; with step −k the first element taken is the *start* index, not the stop index.''',
            'verify': "ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[7, 9, 8] [6, 9, 3]' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Max-heap insertion (sift-up)',
            'text': 'The keys 12, 25, 7, 31, 18, 40, 29 are inserted one at a time, in this order, into an initially empty binary max-heap. Each insertion places the key in the next free array slot and sifts it up, exchanging it with its parent while the parent is smaller. The total number of parent–child exchanges performed over all seven insertions is ______.',
            'answer': '5',
            'solution': '''Insertion = append at the end, then sift up. Count one exchange per swap with the parent.

- 12 → `[12]` (0 swaps)
- 25 → parent 12 < 25, swap → `[25, 12]` (1)
- 7 → parent 25 > 7 → `[25, 12, 7]` (0)
- 31 → index 3, parent 12: swap; then parent 25: swap → `[31, 25, 7, 12]` (2)
- 18 → index 4, parent 25 > 18 → no swap (0)
- 40 → index 5, parent 7: swap; then parent 31: swap → `[40, 25, 31, 12, 18, 7]` (2)
- 29 → index 6, parent 31 > 29 → no swap (0)

Total = 1 + 2 + 2 = **5**. Final heap `[40, 25, 31, 12, 18, 7, 29]`.

**Tip:** a key sifts up at most ⌊log₂ i⌋ levels when it is the i-th key (1-based), so inserting a new maximum at position 6 costs exactly 2 swaps. **Trap:** do not confuse this with bottom-up build-heap, which would give a different number of swaps and a different final array.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [40, 25, 31, 12, 18, 7, 29],
                    'caption': 'Max-heap after all seven insertions',
                },
            ],
            'verify': '''
h = []; sw = 0
for x in [12, 25, 7, 31, 18, 40, 29]:
    h.append(x); i = len(h) - 1
    while i > 0 and h[(i-1)//2] < h[i]:
        p = (i-1)//2; h[p], h[i] = h[i], h[p]; i = p; sw += 1
assert sw == int(ANSWER) and h == [40, 25, 31, 12, 18, 7, 29]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Heap property in arrays',
            'text': 'Arrays below are 0-indexed; the children of index i are 2i + 1 and 2i + 2. Which one of the following arrays represents a valid binary **max-heap**?',
            'options': [
                '`[90, 72, 85, 60, 75, 81, 30, 55]`',
                '`[90, 85, 72, 60, 81, 70, 30, 55]`',
                '`[90, 85, 72, 55, 81, 75, 30, 60]`',
                '`[90, 81, 85, 60, 72, 30, 87, 55]`',
            ],
            'answer': 'B',
            'solution': '''A max-heap needs A[parent(i)] ≥ A[i] for every i ≥ 1, where parent(i) = ⌊(i − 1)/2⌋. Check every parent against its children.

- (A) Index 1 holds 72 and its children (indices 3, 4) are 60 and **75**. 75 > 72 → **invalid**.
- (B) 90 ≥ 85, 72; 85 ≥ 60, 81; 72 ≥ 70, 30; 60 ≥ 55 → every check passes → **valid**.
- (C) Index 2 holds 72 and its child at index 5 is **75** → **invalid**. It also fails at index 3: 55 has child 60.
- (D) Index 2 holds 85 and its child at index 6 is **87** → **invalid**.

**Trap:** being sorted in descending order is sufficient but *not* necessary for a max-heap. Siblings can be in either order, and a key may be smaller than a key in a different subtree at a deeper level (in B, 70 at depth 2 is less than 81 at depth 2 in the other subtree, which is fine).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [90, 85, 72, 60, 81, 70, 30, 55],
                    'caption': 'Option (B) drawn as a complete binary tree',
                },
            ],
            'verify': '''
def ok(a): return all(a[(i-1)//2] >= a[i] for i in range(1, len(a)))
opts = [[90,72,85,60,75,81,30,55],[90,85,72,60,81,70,30,55],
        [90,85,72,55,81,75,30,60],[90,81,85,60,72,30,87,55]]
assert [ok(o) for o in opts] == [False, True, False, False] and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — permutations',
            'text': 'The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack in this order. Pops may be interleaved with pushes arbitrarily, and every popped value is written to the output immediately. Which of the following output sequences is/are possible?',
            'options': ['2 4 3 6 1 5', '1 5 2 4 3 6', '4 5 3 6 2 1', '3 2 5 4 6 1'],
            'answer': ['C', 'D'],
            'solution': '''Simulate greedily: to output x, push everything up to x (if not yet pushed), then x must be on top.

- (A) push 1,2 pop **2**; push 3,4 pop **4**; pop **3**; push 5,6 pop **6**. Stack is now [1, 5] with 5 on top, but 1 is required → **impossible**.
- (B) push 1 pop **1**; push 2..5 pop **5**; top is 4 but 2 is required → **impossible**.
- (C) push 1..4 pop **4**; push 5 pop **5**; pop **3**; push 6 pop **6**; pop **2**; pop **1**. **Possible.**
- (D) push 1,2,3 pop **3**; pop **2**; push 4,5 pop **5**; pop **4**; push 6 pop **6**; pop **1**. **Possible.**

**Tip:** an output sequence is impossible exactly when it contains three values appearing in the order high, low, middle (a, then c, then b with a > b > c) — the forbidden “3-1-2” pattern. In (A) 6, 1, 5 forms it; in (B) 5, 2, 4 forms it.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [1, 5],
                    'label': '(B) stuck: stack after 6 is popped',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def possible(seq):
    st = []; nxt = 1
    for x in seq:
        while nxt <= x: st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = [[3,2,5,4,6,1],[2,4,3,6,1,5],[4,5,3,6,2,1],[1,5,2,4,3,6]]
res = [L for L, s in zip('ABCD', opts) if possible(s)]
assert res == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — linear probing',
            'text': 'Keys 15, 26, 4, 37, 9, 20 are inserted, in this order, into an initially empty hash table with 11 slots (indices 0–10) using h(k) = (3k + 2) mod 11 and linear probing (on a collision try the next slot, wrapping around). A *probe* is one examination of a slot, including the slot where the key is finally placed. The total number of probes over all six insertions is ______.',
            'answer': '13',
            'solution': '''Compute home slots first: h(15) = 47 mod 11 = 3, h(26) = 80 mod 11 = 3, h(4) = 14 mod 11 = 3, h(37) = 113 mod 11 = 3, h(9) = 29 mod 11 = 7, h(20) = 62 mod 11 = 7.

- 15: slot 3 empty → 1 probe.
- 26: 3 full, 4 empty → 2 probes.
- 4: 3, 4 full, 5 empty → 3 probes.
- 37: 3, 4, 5 full, 6 empty → 4 probes.
- 9: slot 7 empty → 1 probe.
- 20: 7 full, 8 empty → 2 probes.

Total = 1 + 2 + 3 + 4 + 1 + 2 = **13**.

Notice how the cluster 3–6 grows and becomes adjacent to slot 7: any later key hashing to 3..8 will have to walk the whole run (primary clustering).

**Trap:** counting only *collisions* (failed probes) gives 7; the question counts every slot examined, including the successful one.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        3: 15,
                        4: 26,
                        5: 4,
                        6: 37,
                        7: 9,
                        8: 20,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None]*11; tot = 0
for k in [15, 26, 4, 37, 9, 20]:
    i = (3*k + 2) % 11; c = 1
    while T[i] is not None: i = (i+1) % 11; c += 1
    T[i] = k; tot += c
assert tot == int(ANSWER) and T[3:9] == [15, 26, 4, 37, 9, 20]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Selection sort — swaps',
            'text': 'Selection sort is applied to the array `[29, 10, 14, 37, 13, 5, 41, 22]` to sort it in ascending order. In pass i (i = 0, 1, …, n − 2) it finds the index m of the minimum of A[i..n−1] and exchanges A[i] and A[m] **only if m ≠ i**. The number of exchanges performed is ______.',
            'answer': '5',
            'solution': '''Selection sort fixes position i in pass i; an exchange is needed only when the minimum is not already in place.

- i=0: min of whole array is 5 (index 5) → swap → `[5, 10, 14, 37, 13, 29, 41, 22]` (1)
- i=1: min of A[1..] is 10, already at index 1 → no swap
- i=2: min 13 at index 4 → swap → `[5, 10, 13, 37, 14, 29, 41, 22]` (2)
- i=3: min 14 at index 4 → swap → `[5, 10, 13, 14, 37, 29, 41, 22]` (3)
- i=4: min 22 at index 7 → swap → `[5, 10, 13, 14, 22, 29, 41, 37]` (4)
- i=5: 29 in place → no swap
- i=6: min 37 at index 7 → swap → `[5, 10, 13, 14, 22, 29, 37, 41]` (5)

Total exchanges = **5**.

**Tip:** selection sort never makes more than n − 1 swaps, which is why it is preferred when writes are expensive; but the exact count needs a trace, because each swap moves an element into a new position that later passes see. **Trap:** answering 7 (= n − 1) assumes a swap in every pass.''',
            'verify': '''
a = [29, 10, 14, 37, 13, 5, 41, 22]; s = 0
for i in range(len(a) - 1):
    m = min(range(i, len(a)), key=lambda j: a[j])
    if m != i: a[i], a[m] = a[m], a[i]; s += 1
assert a == sorted(a) and s == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BST insertion and deletion',
            'text': 'The keys 48, 30, 62, 25, 35, 55, 70, 33, 37, 36 are inserted in this order into an initially empty binary search tree, giving the tree shown. Key 30 is then deleted; a node with two children is replaced by its **in-order successor**. The pre-order traversal of the resulting tree is',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        48,
                        [
                            30,
                            [25],
                            [
                                35,
                                [33],
                                [
                                    37,
                                    [36],
                                    None,
                                ],
                            ],
                        ],
                        [
                            62,
                            [55],
                            [70],
                        ],
                    ],
                    'caption': 'BST before deleting 30',
                },
            ],
            'options': [
                '48, 33, 25, 35, 36, 37, 62, 55, 70',
                '48, 35, 25, 33, 37, 36, 62, 55, 70',
                '48, 25, 35, 33, 37, 36, 62, 55, 70',
                '48, 33, 25, 35, 37, 36, 62, 55, 70',
            ],
            'answer': 'D',
            'solution': '''Node 30 has two children, so it is overwritten by its in-order successor = the minimum of its right subtree. From 35 go left as far as possible: 35 → 33, and 33 has no left child, so the successor is **33**. Copy 33 into the node and delete the leaf 33.

Resulting tree: 48 with left child 33 (children 25 and 35), 35 has only a right child 37, and 37 has left child 36; the right subtree 62 (55, 70) is unchanged.

Pre-order (root, left, right): 48, 33, 25, 35, 37, 36, 62, 55, 70.

- (A) Lists 36 before 37, but 36 is the *left child* of 37, so pre-order visits 37 first.
- (B) Puts 35 (the *right child*, not the successor) at the top of the subtree — a common slip.
- (C) Uses the in-order **predecessor** 25 instead of the successor.
- (D) Correct.

**Trap:** the successor is the leftmost node of the right subtree, not the right child.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        48,
                        [
                            33,
                            [25],
                            [
                                35,
                                None,
                                [
                                    37,
                                    [36],
                                    None,
                                ],
                            ],
                        ],
                        [
                            62,
                            [55],
                            [70],
                        ],
                    ],
                    'highlight': [33],
                    'caption': 'After deleting 30',
                },
            ],
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
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
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
t = None
for k in [48, 30, 62, 25, 35, 55, 70, 33, 37, 36]: t = ins(t, k)
t = dele(t, 30)
assert pre(t) == [48, 33, 25, 35, 37, 36, 62, 55, 70] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'BFS levels',
            'text': 'Breadth-first search is run from vertex A on the undirected graph shown. Each vertex gets a level equal to its BFS distance from A. The number of edges of the graph whose two endpoints have the **same** level is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'H'],
                        ['F', 'H'],
                        ['G', 'I'],
                        ['H', 'I'],
                        ['F', 'G'],
                        ['B', 'C'],
                        ['E', 'F'],
                    ],
                    'pos': {
                        'A': [2, 3],
                        'B': [0, 2],
                        'C': [2, 2],
                        'D': [4, 2],
                        'E': [0, 1],
                        'F': [2, 1],
                        'G': [4, 1],
                        'H': [1, 0],
                        'I': [3, 0],
                    },
                },
            ],
            'answer': '4',
            'solution': '''BFS distances do not depend on the order in which neighbours are scanned, so levels are unique.

- Level 0: A
- Level 1: B, C, D (neighbours of A)
- Level 2: E (via B or C), F (via C), G (via D)
- Level 3: H (via E or F), I (via G)

Now classify each of the 14 edges by the levels of its endpoints. Same-level edges:

- B–C (1, 1)
- E–F (2, 2)
- F–G (2, 2)
- H–I (3, 3)

All other edges join consecutive levels. Answer = **4**.

**Tip:** in an undirected graph every BFS non-tree edge joins vertices whose levels differ by at most 1; a same-level edge always closes an **odd** cycle, so the graph is not bipartite. **Trap:** do not count edges like C–E (levels 1 and 2) — they are non-tree edges but cross levels.''',
            'verify': '''
from collections import deque
E = [('A','B'),('A','C'),('A','D'),('B','E'),('C','E'),('C','F'),('D','G'),('E','H'),
     ('F','H'),('G','I'),('H','I'),('F','G'),('B','C'),('E','F')]
adj = {}
for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
d = {'A': 0}; q = deque('A')
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in d: d[v] = d[u] + 1; q.append(v)
assert sum(d[u] == d[v] for u, v in E) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Linked lists — pointer manipulation',
            'text': 'A singly linked list `head → 4 → 9 → 2 → 7 → 5` is built and the loop below is executed. Which of the following statements is/are TRUE after the loop terminates?',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

head = None
for v in [5, 7, 2, 9, 4]:
    head = Node(v, head)

p = head
while p.next and p.next.next:
    p.next = p.next.next
    p = p.next''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [4, 9, 2, 7, 5],
                    'head': 'head',
                    'caption': 'List before the loop',
                },
            ],
            'options': [
                'The node holding 9 is no longer reachable from `head`',
                'For any list of n ≥ 1 nodes, the loop leaves exactly ⌈n/2⌉ nodes reachable from `head`',
                'When the loop ends, `p` refers to the node holding 7',
                'Traversing from `head` now visits 4, 2, 5',
            ],
            'answer': ['A', 'D'],
            'solution': '''Each iteration bypasses the node after `p` and then advances `p` to the node two ahead.

- Start: p = 4. p.next (9) and p.next.next (2) exist → 4.next = 2, p = 2.
- p = 2: p.next = 7, p.next.next = 5 exist → 2.next = 5, p = 5.
- p = 5: p.next is None → loop ends.

List is now 4 → 2 → 5.

- (A) **True** — 4.next was redirected to 2, so 9 is bypassed (and 7 likewise).
- (B) **False** — for even n the last node survives too. With n = 6 (1..6): 1→3, p=3; 3→5, p=5; 5.next.next is None, so the list is 1, 3, 5, 6 — 4 nodes, not ⌈6/2⌉ = 3. In general the length is ⌊n/2⌋ + 1.
- (C) **False** — p ends at the node holding 5.
- (D) **True.**

**Trap:** the loop condition requires *two* nodes ahead; when only one remains it is kept.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [4, 2, 5],
                    'head': 'head',
                    'caption': 'Reachable list after the loop',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

out = []; q = head
while q: out.append(q.val); q = q.next
assert out == [4, 2, 5] and p.val == 5
def run(n):
    h = None
    for v in range(n, 0, -1): h = Node(v, h)
    p = h
    while p.next and p.next.next:
        p.next = p.next.next; p = p.next
    c = 0
    while h: c += 1; h = h.next
    return c
assert run(6) == 4 != 3
assert sorted(ANSWER) == ['A', 'B']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Merge — comparison count',
            'text': 'The standard merge procedure of merge sort merges the sorted lists L = [2, 9, 14, 20] and R = [5, 6, 15, 30, 31]. It compares the current heads of L and R, moves the smaller to the output, and when one list becomes empty it copies the rest of the other list without comparisons. The number of key comparisons made is',
            'options': ['6', '7', '8', '9'],
            'answer': 'B',
            'solution': '''Merging two lists of sizes m and n uses between min(m, n) and m + n − 1 comparisons; the exact number is (m + n) − (number of elements copied after one list empties).

- 2 vs 5 → 2
- 9 vs 5 → 5
- 9 vs 6 → 6
- 9 vs 15 → 9
- 14 vs 15 → 14
- 20 vs 15 → 15
- 20 vs 30 → 20 (L is now empty)

That is **7** comparisons; 30 and 31 are copied for free.

Check with the formula: 9 elements − 2 copied without comparison = 7.

- (A) 6 forgets the last comparison 20 vs 30.
- (C) 8 = m + n − 1 is the worst case, reached only if the last two output elements come from different lists.
- (D) 9 counts a comparison for every element output.

**Tip:** look at the *tail* of the merged output: the maximal run of elements from one list at the end is copied for free.''',
            'verify': '''
L = [2, 9, 14, 20]; R = [5, 6, 15, 30, 31]; i = j = c = 0
while i < len(L) and j < len(R):
    c += 1
    if L[i] <= R[j]: i += 1
    else: j += 1
assert c == 7 and ['6','7','8','9'][ord(ANSWER) - 65] == '7'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Build-heap (bottom-up heapify)',
            'text': 'The array `[14, 23, 9, 31, 7, 42, 18, 26, 50, 11]` (0-indexed) is converted into a max-heap by the bottom-up build-heap procedure: for i = ⌊n/2⌋ − 1 down to 0, `sift_down(i)` repeatedly exchanges the key with its **larger** child while that child is larger. The total number of exchanges performed is ______.',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [14, 23, 9, 31, 7, 42, 18, 26, 50, 11],
                    'caption': 'Initial array viewed as a complete binary tree',
                },
            ],
            'answer': '8',
            'solution': '''Bottom-up build-heap fixes the subtrees rooted at the internal nodes, from the last internal node (index ⌊10/2⌋ − 1 = 4) back to the root. A key may travel several levels.

- i = 4 (key 7): only child 11 → swap (1). `[14, 23, 9, 31, 11, 42, 18, 26, 50, 7]`
- i = 3 (key 31): children 26, 50 → swap with 50 (2). `[14, 23, 9, 50, 11, 42, 18, 26, 31, 7]`
- i = 2 (key 9): children 42, 18 → swap with 42 (3); 9 is now a leaf.
- i = 1 (key 23): children 50, 11 → swap with 50 (4); at index 3 its children are 26, 31 → swap with 31 (5).
- i = 0 (key 14): children 50, 42 → swap with 50 (6); at index 1 children 31, 11 → swap with 31 (7); at index 3 children 26, 23 → swap with 26 (8).

Total = **8** exchanges. Final heap: `[50, 31, 42, 26, 11, 9, 18, 14, 23, 7]`.

**Why it is Θ(n):** a node at height h can move at most h levels, and ∑ h·n/2^{h+1} = O(n). Here the internal nodes 4, 3, 2, 1, 0 have heights 1, 1, 1, 2, 3, so at most 1 + 1 + 1 + 2 + 3 = 8 exchanges are possible — this input attains the maximum.

**Trap:** stopping a sift-down after one swap (e.g. leaving 23 at index 3 or 14 at index 1) gives 5 or 6 — the key must keep sinking until both children are smaller.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [50, 31, 42, 26, 11, 9, 18, 14, 23, 7],
                    'highlight': [14, 23],
                    'caption': 'Final max-heap (keys that sank twice or more highlighted)',
                },
            ],
            'verify': '''
def sift(a, i, n, c):
    while True:
        l = 2*i + 1; r = l + 1; m = i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; c[0] += 1; i = m
a = [14, 23, 9, 31, 7, 42, 18, 26, 50, 11]; c = [0]
for i in range(len(a)//2 - 1, -1, -1): sift(a, i, len(a), c)
assert c[0] == int(ANSWER) and a == [50, 31, 42, 26, 11, 9, 18, 14, 23, 7]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Heap delete-max',
            'text': 'The max-heap shown is stored as `[95, 80, 88, 52, 76, 64, 70, 41, 30, 66]`. Two **delete-max** operations are performed. Each one moves the last array element to the root, shrinks the array by one, and sifts the root down by exchanging it with its larger child while that child is larger. The array after both deletions is',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [95, 80, 88, 52, 76, 64, 70, 41, 30, 66],
                    'caption': 'Initial max-heap',
                },
            ],
            'options': [
                '`[80, 76, 70, 52, 30, 64, 66, 41]`',
                '`[80, 76, 66, 52, 30, 64, 70, 41]`',
                '`[80, 66, 70, 52, 76, 64, 30, 41]`',
                '`[76, 80, 70, 52, 30, 64, 66, 41]`',
            ],
            'answer': 'A',
            'solution': '''**Delete-max #1** (removes 95): the last key 66 goes to the root → `[66, 80, 88, 52, 76, 64, 70, 41, 30]`.

- 66 vs children 80, 88 → swap with 88 → 66 at index 2.
- 66 vs children 64, 70 → swap with 70 → 66 at index 6 (leaf).

Heap: `[88, 80, 70, 52, 76, 64, 66, 41, 30]`.

**Delete-max #2** (removes 88): the last key 30 goes to the root → `[30, 80, 70, 52, 76, 64, 66, 41]`.

- 30 vs children 80, 70 → swap with 80 → index 1.
- 30 vs children 52, 76 → swap with 76 → index 4.
- Index 4 has children at 9, 10 — outside the array of size 8 → stop.

Heap: `[80, 76, 70, 52, 30, 64, 66, 41]`.

- (A) Correct.
- (B) Has 66 and 70 exchanged — what you get if 66 is assumed to stop at index 2 in the first deletion.
- (C) Sifts with the *smaller* child at some step; 66 at index 1 has child 76 > 66, not a heap.
- (D) Not even a heap (76 at the root with child 80).

**Trap:** always exchange with the **larger** child; exchanging with the smaller child can leave the larger child above its new parent.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [80, 76, 70, 52, 30, 64, 66, 41],
                    'caption': 'Heap after two delete-max operations',
                },
            ],
            'verify': '''
def sift(a, i):
    n = len(a)
    while True:
        l = 2*i + 1; r = l + 1; m = i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m
a = [95, 80, 88, 52, 76, 64, 70, 41, 30, 66]
for _ in range(2):
    a[0] = a[-1]; a.pop(); sift(a, 0)
opts = {'A': [80,76,70,52,30,64,66,41], 'B': [80,76,66,52,30,64,70,41],
        'C': [80,66,70,52,76,64,30,41], 'D': [76,80,70,52,30,64,66,41]}
assert [k for k, v in opts.items() if v == a] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Positions of k-th largest in a heap',
            'text': 'A binary max-heap holds 20 **distinct** keys in H[1..20] (1-indexed; the children of i are 2i and 2i + 1). Which of the following statements is/are TRUE for every such heap?',
            'options': [
                'The smallest key is stored at an index in the range 11..20',
                'The second-largest key is stored at index 2 or index 3',
                'There exists such a heap in which the third-largest key is stored at index 6',
                'There exists such a heap in which the fourth-largest key is stored at index 16',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Key fact: every ancestor of a node is larger than it. So a key that has exactly r − 1 larger keys in the heap (the r-th largest) can only sit at depth ≤ r − 1.

- (A) The smallest key cannot have a child (the child would have to be smaller). Nodes with no children are indices ⌊20/2⌋ + 1 = 11 to 20. **True.**
- (B) The second-largest key has only one larger key (the root), so its depth is ≤ 1, i.e. index 2 or 3 (it cannot be the root). **True.**
- (C) Index 6 is at depth 2; its ancestors are 3 and 1. Put the largest at 1, the second-largest at 3 and the third-largest at 6 — this can be completed to a valid heap (e.g. fill the remaining slots in decreasing order). **True** (possible).
- (D) Index 16 has depth ⌊log₂ 16⌋ = 4, so it has 4 ancestors, all larger. But the fourth-largest has only 3 larger keys. **False** — the fourth-largest is confined to depth ≤ 3, i.e. indices 2..15.

**Trap:** in (C) “third-largest must be a child of the root” is a frequent wrong belief; it can be a grandchild when the second-largest is its parent.''',
            'verify': '''
import random
random.seed(7)
def sift(a, i, n):
    while True:
        l, r, m = 2*i, 2*i + 1, i
        if l <= n and a[l] > a[m]: m = l
        if r <= n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m
seenC = False
for _ in range(3000):
    k = random.sample(range(1, 200), 20); a = [None] + k
    for i in range(10, 0, -1): sift(a, i, 20)
    s = sorted(k)
    assert 11 <= a.index(s[0]) <= 20
    assert a.index(s[-2]) in (2, 3)
    assert a.index(s[-4]) != 16
    if a.index(s[-3]) == 6: seenC = True
# explicit witness for (C): decreasing fill with 2nd at 3 and 3rd at 6
w = [None, 20, 17, 19, 16, 15, 18] + list(range(14, 0, -1))
assert all(w[i // 2] > w[i] for i in range(2, 21)) and w[6] == 18
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Counting heaps',
            'text': 'Consider all binary **min**-heaps that can be formed with the seven distinct keys 1, 2, 3, 4, 5, 6, 7 (stored as a complete binary tree of height 2). In how many of these heaps is the key 3 a **leaf**?',
            'answer': '32',
            'solution': '''A key's ancestors must all be smaller than it. If 3 is a leaf (depth 2) it has two ancestors, and the only keys smaller than 3 are 1 and 2 — so the root is 1, 3's parent is 2, and 3 sits under 2.

Count the heaps for a fixed leaf position of 3:

- The parent of 3 holds 2 and is one child of the root (fixed by the leaf choice).
- The sibling leaf of 3 can be any of the four keys {4, 5, 6, 7} → 4 ways.
- The other subtree of the root (3 nodes) gets the remaining 3 keys; its root must be the smallest of them and the two leaves can be arranged in 2 ways → 2 ways.

Per leaf position: 4 × 2 = 8. There are 4 leaf positions → 4 × 8 = **32**.

Sanity check: the total number of min-heaps on 7 keys is C(6,3) · 2 · 2 = 80. Key 3 is at depth 1 in the remaining 48 heaps (24 at each child of the root), and it is never at the root.

**Trap:** assuming the 3 must be near the top because it is “small”; only keys with few smaller keys are restricted, and 3 has exactly two, which permits depth 2.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [1, 2, 4, 3, 6, 5, 7],
                    'highlight': [3],
                    'caption': 'One of the 32 heaps (3 is a leaf under 2)',
                },
            ],
            'verify': '''
from itertools import permutations
H = [p for p in permutations(range(1, 8))
     if all(p[(i-1)//2] < p[i] for i in range(1, 7))]
assert len(H) == 80
assert sum(1 for p in H if p.index(3) >= 3) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python heapq with tuples',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''import heapq
tasks = [(3, 'e'), (1, 'b'), (4, 'a'), (1, 'a'), (5, 'c'), (2, 'd')]
h = []
for t in tasks:
    heapq.heappush(h, t)
out = []
while len(h) > 2:
    p, s = heapq.heappop(h)
    out.append(s)
    if p % 2:
        heapq.heappush(h, (p + 3, s.upper()))
print(''.join(out), h[0])''',
            'options': ["`abdeABa (5, 'c')`", "`abdeaAB (5, 'c')`", "`abdeAB (4, 'a')`", "`badeABa (5, 'c')`"],
            'answer': 'A',
            'solution': '''`heapq` is a min-heap; tuples compare lexicographically (first the number, then the string). Uppercase letters have smaller code points than lowercase ('A' = 65 < 'a' = 97).

Pops while more than two items remain:

- (1,'a') → out a; p odd → push (4,'A')
- (1,'b') → out b; push (4,'B')
- (2,'d') → out d; p even, nothing pushed
- (3,'e') → out e; push (6,'E')
- Heap now holds (4,'A'), (4,'B'), (4,'a'), (5,'c'), (6,'E').
- (4,'A') → out A (even); (4,'B') → out B; (4,'a') → out a.
- Two items (5,'c'), (6,'E') remain → loop stops. h[0] is the minimum (5,'c').

Output: `abdeABa (5, 'c')`.

- (B) Assumes (4,'a') < (4,'A') — lowercase does not sort first.
- (C) Stops one pop early (treats the condition as ≥ 3 remaining after pop).
- (D) Ignores the tie-break on the second field: (1,'a') < (1,'b').

**Trap:** p + 3 flips parity, so each task is re-pushed at most once — the loop terminates.''',
            'verify': 'assert OUTPUT.strip() == "abdeABa (5, \'c\')" and ANSWER == \'A\'',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra with a lazy priority queue',
            'text': "Dijkstra's algorithm from source S is implemented with a binary min-heap **without** decrease-key: initially (0, S) is pushed; whenever an edge relaxation strictly improves dist[v], the pair (dist[v], v) is pushed; popped pairs whose distance exceeds the current dist[v] are discarded. For the directed graph shown, the total number of push operations (including the initial push of S) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['S', 'C', 9],
                        ['B', 'A', 3],
                        ['B', 'C', 6],
                        ['A', 'D', 4],
                        ['C', 'D', 1],
                        ['B', 'E', 12],
                        ['D', 'E', 2],
                        ['C', 'E', 5],
                        ['A', 'C', 1],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [3, 2.4],
                        'B': [3, -0.4],
                        'C': [4.6, 1],
                        'D': [6.4, 2.4],
                        'E': [6.4, -0.4],
                    },
                },
            ],
            'answer': '12',
            'solution': '''Every strict improvement of a tentative distance causes one push. Trace (dist after each pop):

- push (0,S). [1]
- Pop S(0): A=7, B=2, C=9 → 3 pushes. [4]
- Pop B(2): A: 5 < 7 push; C: 8 < 9 push; E: 14 push. [7]
- Pop A(5): D = 9 push; C: 6 < 8 push. [9]
- Pop C(6): D: 7 < 9 push; E: 11 < 14 push. [11]
- Pop (7,A) — stale, discarded. Pop D(7): E: 9 < 11 push. [12]
- Remaining pops (8,C), (9,C), (9,D) are stale; E(9) relaxes nothing; (11,E), (14,E) stale.

Total pushes = **12** (1 initial + 11 improvements). Final distances: S 0, B 2, A 5, C 6, D 7, E 9.

Note the heap ends up handling 12 pops for 6 vertices: lazy deletion costs O(E log E) = O(E log V) time, the same bound as decrease-key.

**Trap:** counting one push per vertex (6) or one per edge (11) — the count is the number of strict improvements plus one.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'dist[] after each non-stale pop',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'row_labels': ['init', 'pop S', 'pop B', 'pop A', 'pop C', 'pop D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, 9, '∞', '∞'],
                        [0, 5, 2, 8, '∞', 14],
                        [0, 5, 2, 6, 9, 14],
                        [0, 5, 2, 6, 7, 11],
                        [0, 5, 2, 6, 7, 9],
                    ],
                },
            ],
            'verify': '''
import heapq
G = {'S':[('A',7),('B',2),('C',9)], 'B':[('A',3),('C',6),('E',12)],
     'A':[('D',4),('C',1)], 'C':[('D',1),('E',5)], 'D':[('E',2)], 'E':[]}
d = {v: float('inf') for v in G}; d['S'] = 0; pq = [(0, 'S')]; pushes = 1
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]:
            d[v] = du + w; heapq.heappush(pq, (d[v], v)); pushes += 1
assert pushes == int(ANSWER)
assert d == {'S':0, 'B':2, 'A':5, 'C':6, 'D':7, 'E':9}
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Valid DFS orders',
            'text': 'Depth-first search (recursive, any neighbour order allowed) is started at vertex P of the undirected graph shown. Which of the following is/are possible orders in which DFS **discovers** the vertices?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'S'],
                        ['R', 'S'],
                        ['S', 'T'],
                        ['R', 'U'],
                        ['T', 'U'],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [1.5, 2],
                        'R': [1.5, 0],
                        'S': [3, 1],
                        'T': [4.5, 2],
                        'U': [4.5, 0],
                    },
                },
            ],
            'options': ['P, R, S, U, T, Q', 'P, Q, S, T, R, U', 'P, Q, S, R, U, T', 'P, R, U, T, S, Q'],
            'answer': ['C', 'D'],
            'solution': '''Rule: each newly discovered vertex must be adjacent to the **deepest vertex on the current recursion path that still has an undiscovered neighbour** (DFS only backtracks when the current vertex is exhausted).

- (A) P→R→S→U? S and U are **not** adjacent; at that moment S still has undiscovered neighbours Q and T, so the next vertex must be one of them. **Invalid.**
- (B) P→Q→S→T. T still has the undiscovered neighbour U, so DFS must go T→U next; it cannot jump to R. **Invalid.**
- (C) P→Q→S→R (S–R edge) →U (R–U) →T (U–T). Every step goes to a neighbour of the current vertex. **Valid.**
- (D) P→R→U→T→S (T–S) →Q (S–Q). **Valid.**

**Trap:** BFS-like thinking (“visit R since it is adjacent to P”) breaks DFS order; a jump back to an ancestor's neighbour is allowed only after the current vertex has no unvisited neighbours.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'S'],
                        ['R', 'S'],
                        ['S', 'T'],
                        ['R', 'U'],
                        ['T', 'U'],
                    ],
                    'highlight_edges': [
                        ['P', 'Q'],
                        ['Q', 'S'],
                        ['S', 'R'],
                        ['R', 'U'],
                        ['U', 'T'],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [1.5, 2],
                        'R': [1.5, 0],
                        'S': [3, 1],
                        'T': [4.5, 2],
                        'U': [4.5, 0],
                    },
                    'caption': 'DFS tree for order (A)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = [('P','Q'),('P','R'),('Q','S'),('R','S'),('S','T'),('R','U'),('T','U')]
adj = {}
for u, v in E: adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
def valid(seq):
    seen = {seq[0]}; path = [seq[0]]
    for x in seq[1:]:
        while path and adj[path[-1]] <= seen: path.pop()
        if not path or x not in adj[path[-1]] or x in seen: return False
        seen.add(x); path.append(x)
    return len(seen) == len(adj)
opts = ['PQSRUT', 'PQSTRU', 'PRUTSQ', 'PRSUTQ']
assert [L for L, s in zip('ABCD', opts) if valid(s)] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': 'Consider the following quicksort with Lomuto partitioning (last element as pivot). Every execution of a swap statement is counted, even if it exchanges an element with itself. The value printed is ______.',
            'code': '''cnt = 0
def partition(a, lo, hi):
    global cnt
    p, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= p:
            i += 1
            a[i], a[j] = a[j], a[i]
            cnt += 1
    a[i + 1], a[hi] = a[hi], a[i + 1]
    cnt += 1
    return i + 1

def qsort(a, lo, hi):
    if lo < hi:
        q = partition(a, lo, hi)
        qsort(a, lo, q - 1)
        qsort(a, q + 1, hi)

a = [38, 12, 57, 24, 9, 71, 45, 30]
qsort(a, 0, len(a) - 1)
print(cnt)''',
            'answer': '9',
            'solution': '''Lomuto performs one swap for every element ≤ pivot in the scanned range plus one final swap that places the pivot. So for a call on a range: swaps = (#elements ≤ pivot, excluding pivot) + 1.

- Call [0..7], pivot 30: elements ≤ 30 are 12, 24, 9 → 3 + 1 = 4 swaps. Array `[12, 24, 9, 30, 57, 71, 45, 38]`, pivot at 3.
- Call [0..2] = [12, 24, 9], pivot 9: none ≤ 9 → 0 + 1 = 1 swap → `[9, 24, 12]`, pivot at 0.
- Call [1..2] = [24, 12], pivot 12: none → 1 swap → `[12, 24]`.
- Call [4..7] = [57, 71, 45, 38], pivot 38: none ≤ 38 → 1 swap → `[38, 71, 45, 57]`, pivot at 4.
- Call [5..7] = [71, 45, 57], pivot 57: 45 → 1 + 1 = 2 swaps → `[45, 57, 71]`.
- Remaining ranges have size ≤ 1 (no partition call).

Total = 4 + 1 + 1 + 1 + 2 = **9**.

**Trap:** forgetting the self-swaps (when i == j) or the final pivot swap; the problem counts every execution of the swap statement.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each partition call',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', '[0..7]', '[0..2]', '[1..2]', '[4..7]', '[5..7]'],
                    'rows': [
                        [38, 12, 57, 24, 9, 71, 45, 30],
                        [12, 24, 9, 30, 57, 71, 45, 38],
                        [9, 24, 12, 30, 57, 71, 45, 38],
                        [9, 12, 24, 30, 57, 71, 45, 38],
                        [9, 12, 24, 30, 38, 71, 45, 57],
                        [9, 12, 24, 30, 38, 45, 57, 71],
                    ],
                    'highlight': [
                        [1, 3],
                        [2, 0],
                        [3, 1],
                        [4, 4],
                        [5, 6],
                    ],
                },
            ],
            'verify': 'assert OUTPUT.strip() == ANSWER and a == sorted(a)',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'd-ary heaps',
            'text': 'A **3-ary** max-heap is stored in a 0-indexed array: the children of index i are 3i + 1, 3i + 2, 3i + 3 and the parent of i is ⌊(i − 1)/3⌋. The heap shown is `[90, 70, 85, 60, 40, 65, 30, 80, 20, 50, 10, 55]`. Keys 75 and then 88 are inserted (append, then sift up while the parent is smaller). The resulting array is',
            'diagrams': [
                {
                    'type': 'tree',
                    'root': '90',
                    'children': {
                        '90': ['70', '85', '60'],
                        '70': ['40', '65', '30'],
                        '85': ['80', '20', '50'],
                        '60': ['10', '55'],
                    },
                    'caption': '3-ary max-heap before the insertions',
                },
            ],
            'options': [
                '`[90, 70, 88, 75, 40, 65, 30, 80, 20, 50, 10, 55, 60, 85]`',
                '`[90, 88, 85, 75, 40, 65, 30, 80, 20, 50, 10, 55, 60, 70]`',
                '`[90, 88, 85, 75, 70, 65, 30, 80, 20, 50, 10, 55, 60, 40]`',
                '`[90, 88, 85, 60, 70, 65, 30, 80, 20, 50, 10, 55, 75, 40]`',
            ],
            'answer': 'C',
            'solution': '''In a d-ary heap the sift-up is the same as in a binary heap, only the parent formula changes: parent(i) = ⌊(i − 1)/3⌋.

**Insert 75** at index 12: parent ⌊11/3⌋ = 3 holds 60 < 75 → swap; 75 now at 3, parent 0 holds 90 → stop.
`[90, 70, 85, 75, 40, 65, 30, 80, 20, 50, 10, 55, 60]`

**Insert 88** at index 13: parent ⌊12/3⌋ = 4 holds 40 → swap; 88 at 4, parent ⌊3/3⌋ = 1 holds 70 → swap; 88 at 1, parent 0 holds 90 → stop.
`[90, 88, 85, 75, 70, 65, 30, 80, 20, 50, 10, 55, 60, 40]`

- (A) Exchanges 88 with 85, but 85 (index 2) is not an ancestor of index 13; the ancestors of 13 are 4, 1 and 0.
- (B) Moves 70 to the end instead of shifting it down one level along the path.
- (C) Correct.
- (D) Forgets to sift up 75 (left at index 12).

**Tip:** a d-ary heap has height ≈ log_d n, so insert/sift-up is O(log_d n) but delete-max costs O(d log_d n) — it must examine d children per level.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '90',
                    'children': {
                        '90': ['88', '85', '75'],
                        '88': ['70', '65', '30'],
                        '85': ['80', '20', '50'],
                        '75': ['10', '55', '60'],
                        '70': ['40'],
                    },
                    'caption': 'After inserting 75 and 88',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

a = [90, 70, 85, 60, 40, 65, 30, 80, 20, 50, 10, 55]
assert all(a[(i-1)//3] >= a[i] for i in range(1, len(a)))
for x in (75, 88):
    a.append(x); i = len(a) - 1
    while i > 0 and a[(i-1)//3] < a[i]:
        p = (i-1)//3; a[p], a[i] = a[i], a[p]; i = p
opts = {'A': [90,88,85,75,70,65,30,80,20,50,10,55,60,40],
        'B': [90,88,85,75,40,65,30,80,20,50,10,55,60,70],
        'C': [90,70,88,75,40,65,30,80,20,50,10,55,60,85],
        'D': [90,88,85,60,70,65,30,80,20,50,10,55,75,40]}
assert [k for k, v in opts.items() if v == a] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Priority-queue operation costs',
            'text': 'Let n be the number of keys in a binary heap stored in an array. Which of the following statements is/are TRUE (worst-case bounds)?',
            'options': [
                'Given the array index of a key, decrease-key in a binary min-heap takes O(log n) time',
                "Dijkstra's algorithm with a binary heap on a graph with V vertices and E edges runs in O((V + E) log V) time",
                'The maximum key of a binary **min**-heap can be found in O(log n) time',
                'Building a heap bottom-up from n arbitrary keys takes Θ(n) time',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''- (A) **True.** Decreasing a key can only violate the heap property with its parent; one sift-up of at most ⌊log₂ n⌋ levels fixes it. Knowing the index avoids an O(n) search.
- (B) **True.** At most V extract-min operations and at most E decrease-key (or lazy push) operations, each O(log V) → O((V + E) log V).
- (C) **False.** The maximum of a min-heap must be a leaf, but it can be *any* of the ⌈n/2⌉ leaves; the heap order gives no information comparing different leaves, so Θ(n) comparisons are needed.
- (D) **True.** Sift-down from a node of height h costs O(h); there are at most ⌈n/2^{h+1}⌉ nodes of height h, and ∑ h/2^{h} converges, so the total is Θ(n) — not Θ(n log n).

**Trap:** “heaps support O(log n) everything” — a heap is only partially ordered; search for an arbitrary key or the opposite extreme (max in a min-heap) is linear.

**Tip:** for dense graphs (E ≈ V²) an array-based Dijkstra in O(V²) beats the binary heap's O(V² log V).''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

# (B) the max of a min-heap can sit at any leaf: show every leaf position is achievable
import itertools
pos = set()
for p in itertools.permutations(range(1, 8)):
    if all(p[(i-1)//2] < p[i] for i in range(1, 7)): pos.add(p.index(7))
assert pos == {3, 4, 5, 6}
assert sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
    ],
}
