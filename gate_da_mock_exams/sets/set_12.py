# Set 12 — Quicksort & Partitioning
SET = {
    'number': 12,
    'title': 'Quicksort & Partitioning',
    'difficulty': 'Moderate',
    'focus': 'Lomuto/Hoare partition, pivot choice, best/worst case',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — slice assignment and aliasing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''a = [3, 1, 4, 1, 5, 9, 2]
b = a
c = a[:]
b[1:3] = [7]
c[::2] = c[1::2] + [0]
print(len(a), a[2], c)''',
            'options': [
                '`6 1 [1, 1, 1, 1, 9, 9, 0]`',
                '`7 4 [1, 1, 1, 1, 9, 9, 0]`',
                '`6 1 [3, 1, 4, 1, 5, 9, 2]`',
                'A `ValueError` is raised',
            ],
            'answer': 'A',
            'solution': '''**Concept:** `b = a` makes an alias (same list); `a[:]` makes a shallow copy. Assigning to a *simple* slice may change the length; assigning to an *extended* slice (with a step) requires the right-hand side to have exactly the same number of elements.

- `b[1:3] = [7]` replaces the two elements at indices 1, 2 (values 1, 4) by one element. Since `b` is `a`, now `a = [3, 7, 1, 5, 9, 2]`: `len(a)` = 6, `a[2]` = 1.
- `c` is an independent copy `[3, 1, 4, 1, 5, 9, 2]`.
- `c[::2]` addresses indices 0, 2, 4, 6 (4 slots). The right side is `c[1::2] + [0]` = `[1, 1, 9] + [0]` = 4 values — sizes match, so no error.
- After assignment: c[0] = 1, c[2] = 1, c[4] = 9, c[6] = 0 → `[1, 1, 1, 1, 9, 9, 0]`.

**Options:**
- (B) treats `b` as a copy, so `a` would be unchanged.
- (C) assumes `c` aliases `a` (and would anyway not match).
- (D) would happen only if the extended-slice sizes differed (e.g. without `+ [0]`).

**Trap:** the length check applies only to extended slices — simple slices can shrink or grow.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "6 1 [1, 1, 1, 1, 9, 9, 0]" and ANSWER == "B"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Quicksort — Lomuto partition swaps',
            'text': 'The Lomuto partition below is applied once to A = [9, 4, 12, 7, 15, 3, 10, 8] with lo = 0 and hi = 7 (pivot = last element). The total number of times the statement marked `#S` or `#F` is executed (count every execution, even if i == j) is ______.',
            'code': '''def partition(a, lo, hi):
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]          #S
    a[i + 1], a[hi] = a[hi], a[i + 1]        #F
    return i + 1''',
            'answer': '4',
            'solution': '''**Concept:** Lomuto keeps the invariant a[lo..i] ≤ pivot < a[i+1..j−1]. A swap `#S` happens once for every element ≤ pivot; the final swap `#F` places the pivot at index i + 1.

Pivot x = 8. Trace (i starts at −1):
- j = 0: 9 > 8 → nothing.
- j = 1: 4 ≤ 8 → i = 0, swap a[0]↔a[1] → [4, 9, 12, 7, 15, 3, 10, 8] (#S 1)
- j = 2: 12 > 8.
- j = 3: 7 ≤ 8 → i = 1, swap a[1]↔a[3] → [4, 7, 12, 9, 15, 3, 10, 8] (#S 2)
- j = 4: 15 > 8.
- j = 5: 3 ≤ 8 → i = 2, swap a[2]↔a[5] → [4, 7, 3, 9, 15, 12, 10, 8] (#S 3)
- j = 6: 10 > 8.
- Final: swap a[3]↔a[7] → [4, 7, 3, 8, 15, 12, 10, 9] (#F)

Total = 3 + 1 = **4**; the pivot ends at index 3.

**Tip:** the number of `#S` executions equals the number of non-pivot elements ≤ pivot (here 4, 7, 3) — you can answer without a full trace.
**Trap:** forgetting the final pivot swap (answer 3).''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [4, 7, 3, 8, 15, 12, 10, 9],
                    'highlight': [3],
                    'pointers': {
                        'pivot': 3,
                    },
                    'caption': 'After partition: ≤ 8 | 8 | > 8',
                },
            ],
            'verify': '''
cnt = 0
def part2(a, lo, hi):
    global cnt
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1; a[i], a[j] = a[j], a[i]; cnt += 1
    a[i+1], a[hi] = a[hi], a[i+1]; cnt += 1
    return i + 1
A = [9, 4, 12, 7, 15, 3, 10, 8]
p = part2(A, 0, 7)
assert cnt == int(ANSWER) and A == [4, 7, 3, 8, 15, 12, 10, 9] and p == 3
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Quicksort — Hoare partition',
            'text': "Hoare's partition scheme (pivot p = a[lo]) is shown below. It is called once on a = [6, 11, 2, 9, 6, 1, 14, 4, 8] with lo = 0, hi = 8. What are the array and the returned index immediately after the call?",
            'code': '''def hoare(a, lo, hi):
    p, i, j = a[lo], lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < p:
            i += 1
        j -= 1
        while a[j] > p:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]''',
            'options': [
                '[4, 1, 2, 6, 9, 11, 14, 6, 8], returns 3',
                '[4, 1, 2, 6, 6, 11, 14, 9, 8], returns 4',
                '[4, 1, 2, 6, 9, 11, 14, 6, 8], returns 4',
                '[1, 4, 2, 6, 6, 9, 14, 11, 8], returns 4',
            ],
            'answer': 'A',
            'solution': '''**Concept:** Hoare's scheme moves i right past elements < p and j left past elements > p, swapping when both stop. It guarantees a[lo..j] ≤ p ≤ a[j+1..hi], but the pivot is **not** necessarily placed at its final position. Elements *equal* to p stop both scans.

Trace with p = 6:
- i stops at 0 (6 is not < 6); j moves from 8: 8 > 6 → j = 7 (4) stops. Swap → [4, 11, 2, 9, 6, 1, 14, 6, 8].
- i → 1 (11 stops); j → 6 (14 > 6) → 5 (1 stops). Swap → [4, 1, 2, 9, 6, 11, 14, 6, 8].
- i → 2 (2 < 6) → 3 (9 stops); j → 4 (6 stops, not > 6). Swap → [4, 1, 2, 6, 9, 11, 14, 6, 8].
- i → 4 (9 stops); j → 3 (6 stops). Now i ≥ j → return **3**.

Check: a[0..3] = 4, 1, 2, 6 are all ≤ 6 and a[4..8] = 9, 11, 14, 6, 8 are all ≥ 6. ✓ Note a second 6 sits in the right part — allowed by Hoare's invariant.

**Options:** (B) and (D) put both 6s next to each other as Lomuto/three-way partitioning would; (C) has the right array but returns i instead of j.

**Trap:** assuming Hoare leaves the pivot at the returned index.''',
            'verify': '''
A = [6, 11, 2, 9, 6, 1, 14, 4, 8]
r = hoare(A, 0, 8)
assert A == [4, 1, 2, 6, 9, 11, 14, 6, 8] and r == 3 and ANSWER == "A"
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Quicksort — identifying the pivot',
            'text': 'The array below shows the state of an array of distinct integers after the **first** partitioning step of some quicksort (the pivot is placed at its final sorted position; nothing else is assumed about the partition scheme). Which of the following elements could have been the pivot?',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [4, 2, 7, 5, 9, 12, 10, 15, 13, 18],
                    'caption': 'Array after the first partition',
                },
            ],
            'options': ['9', '18', '7', '12'],
            'answer': ['A', 'B'],
            'solution': '''**Concept:** after partitioning, the pivot is in its final place: every element to its left is smaller and every element to its right is larger. So x at index i is a candidate iff max(a[0..i−1]) < x < min(a[i+1..n−1]).

Prefix maxima / suffix minima check:
- (A) 9 at index 4: left {4, 2, 7, 5}, max 7 < 9; right {12, 10, 15, 13, 18}, min 10 > 9. **Possible.**
- (B) 18 at index 9 (last): everything to its left is smaller and the right side is empty. **Possible** (e.g. Lomuto with the maximum as pivot).
- (C) 7 at index 2: right part contains 5 < 7. **Not possible.**
- (D) 12 at index 5: right part contains 10 < 12. **Not possible.**

Also 4, 2, 5, 15, 10, 13 fail; only 9 and 18 qualify.

**Trap:** forgetting that a pivot can sit at an end of the array — an extreme pivot gives an empty side, which is exactly the worst case of quicksort.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

B = [4, 2, 7, 5, 9, 12, 10, 15, 13, 18]
ok = {x for i, x in enumerate(B)
      if all(y < x for y in B[:i]) and all(y > x for y in B[i+1:])}
opts = [9, 12, 18, 7]
assert sorted(ANSWER) == [c for c, v in zip("ABCD", opts) if v in ok]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — deque as a double-ended queue',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''from collections import deque

d = deque([5, 2, 8])
for k in range(1, 6):
    if k % 2:
        d.append(d.popleft() * k)
    else:
        d.appendleft(d.pop() - k)
print(d[0] - d[-1])''',
            'answer': '-23',
            'solution': '''**Concept:** a deque supports O(1) insertion/removal at both ends: `append`/`pop` work on the right, `appendleft`/`popleft` on the left. Odd k rotates the front element to the back (multiplied by k); even k rotates the back element to the front (minus k).

Trace (left → right):
- start: [5, 2, 8]
- k = 1: popleft 5, append 5 × 1 = 5 → [2, 8, 5]
- k = 2: pop 5, appendleft 5 − 2 = 3 → [3, 2, 8]
- k = 3: popleft 3, append 9 → [2, 8, 9]
- k = 4: pop 9, appendleft 5 → [5, 2, 8]
- k = 5: popleft 5, append 25 → [2, 8, 25]

`d[0] - d[-1]` = 2 − 25 = **−23**.

**Trap:** mixing up `pop()` (right end) with `popleft()`; with `pop()` on the left the answer would be completely different. Note too that the deque returns to [5, 2, 8] after k = 4 — a nice self-check.''',
            'solution_diagrams': [
                {
                    'type': 'queue',
                    'values': [2, 8, 25],
                    'caption': 'Final deque (front on the left)',
                },
            ],
            'verify': 'assert int(OUTPUT) == int(ANSWER) and list(d) == [2, 8, 25]',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Circular linked lists — elimination game',
            'text': 'Nine people numbered 1..9 are stored in a circular singly linked list. The program repeatedly skips ahead and removes a node. What does it print?',
            'code': '''class Node:
    def __init__(self, v):
        self.v, self.next = v, None

n, k = 9, 4
head = Node(1)
cur = head
for v in range(2, n + 1):
    cur.next = Node(v)
    cur = cur.next
cur.next = head            # cur is the tail
out = []
while cur.next is not cur:
    for _ in range(k - 1):
        cur = cur.next
    out.append(cur.next.v)
    cur.next = cur.next.next
print(out[4], cur.v)''',
            'options': ['`6 5`', '`9 1`', '`6 1`', '`5 1`'],
            'answer': 'C',
            'solution': '''**Concept:** to delete from a singly linked list you need the *predecessor*. `cur` starts at the tail (9), moves k − 1 = 3 steps and removes `cur.next` — i.e. every 4th person counting from the person after the last removal.

Trace (removed value, list afterwards):
- from 9 move to 3 → remove **4** → 1 2 3 5 6 7 8 9
- from 3 move to 7 → remove **8** → 1 2 3 5 6 7 9
- from 7 move to 2 → remove **3** → 1 2 5 6 7 9
- from 2 move to 7 → remove **9** → 1 2 5 6 7
- from 7 move to 5 → remove **6** → 1 2 5 7
- from 5 move to 2 → remove **5** → 1 2 7
- from 2 move to 2 → remove **7** → 1 2
- from 2 move to 1 → remove **2** → 1

`out` = [4, 8, 3, 9, 6, 5, 7, 2]; `out[4]` = 6 (5th removal) and the survivor is 1. Output `6 1`.

**Options:** (B) uses 1-based indexing for `out[4]` (that would be 9, the 4th removal). (A) and (D) report a removed person as the survivor or the wrong removal.

**Trap:** off-by-one in where counting restarts after a deletion.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    'circular': True,
                    'head': 'head',
                    'caption': 'Initial circular list; removal order 4, 8, 3, 9, 6, 5, 7, 2',
                },
            ],
            'verify': "ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.split() == ['6', '1'] and out == [4, 8, 3, 9, 6, 5, 7, 2] and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — quadratic probing',
            'text': 'Keys 25, 36, 14, 47, 58, 3 are inserted in this order into an initially empty table of size 11 using quadratic probing: probe i (i = 0, 1, 2, …) examines slot (k + i²) mod 11. Next, key 69 is to be inserted and probes i = 0, 1, …, 10 are tried. The number of **distinct** slots examined by these 11 probes for key 69 is ______.',
            'answer': '6',
            'solution': '''**Concept:** with quadratic probing and a prime table size m, i² mod m takes only (m + 1)/2 distinct values, so a key can examine only about half the table — insertion can fail although free slots exist.

Building the table:
- 25 → 3. 36 → 3 (full), 4 → slot 4.
- 14 → 3, 4, 7 → slot 7.
- 47 → 3, 4, 7, (3 + 9) mod 11 = 1 → slot 1.
- 58 → 3, 4, 7, 1, (3 + 16) mod 11 = 8 → slot 8.
- 3 → 3, 4, 7, 1, 8, (3 + 25) mod 11 = 6 → slot 6.

Key 69 (home 69 mod 11 = 3): offsets i² mod 11 for i = 0..10 are 0, 1, 4, 9, 5, 3, 3, 5, 9, 4, 1, so the slots are 3, 4, 7, 1, 8, 6, 6, 8, 1, 7, 4 — only **6** distinct slots, all occupied. The insertion fails even though slots 0, 2, 5, 9, 10 are empty.

**Trap:** assuming 11 probes visit 11 different slots (true for linear probing, false here).''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        1: 47,
                        3: 25,
                        4: 36,
                        6: 3,
                        7: 14,
                        8: 58,
                    },
                    'caption': 'Table before inserting 69: its 6 reachable slots are all full',
                },
            ],
            'verify': '''
T = [None]*11
for k in [25, 36, 14, 47, 58, 3]:
    for i in range(11):
        s = (k + i*i) % 11
        if T[s] is None:
            T[s] = k; break
probes = {(69 + i*i) % 11 for i in range(11)}
assert len(probes) == int(ANSWER) and all(T[s] is not None for s in probes)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search trees — search paths',
            'text': 'Each sequence below is claimed to be the sequence of keys compared, in order, while searching for the key 47 in some binary search tree containing distinct integers (the search ends at 47). Which sequence **cannot** occur?',
            'options': [
                '90, 25, 80, 30, 70, 40, 60, 47',
                '10, 75, 64, 43, 58, 53, 47',
                '20, 60, 30, 55, 50, 35, 47',
                '52, 15, 48, 22, 39, 50, 47',
            ],
            'answer': 'D',
            'solution': '''**Concept:** during a search every visited key narrows an open interval (low, high) that must contain the target; each subsequent key must lie inside the current interval.

- (A) 90 → (−∞, 90); 25 → (25, 90); 80 → (25, 80); 30 → (30, 80); 70 → (30, 70); 40 → (40, 70); 60 → (40, 60); 47 inside. **Valid.**
- (B) 10 → (10, ∞); 75 → (10, 75); 64 → (10, 64); 43 → (43, 64); 58 → (43, 58); 53 → (43, 53); 47 inside. **Valid.**
- (C) 20 → (20, ∞); 60 → (20, 60); 30 → (30, 60); 55 → (30, 55); 50 → (30, 50); 35 → (35, 50); 47 inside. **Valid.**
- (D) 52 → (−∞, 52); 15 → (15, 52); 48 → (15, 48); 22 → (22, 48); 39 → (39, 48); next key 50 is **not** inside (39, 48) — after going left at 48 every later key must be < 48. **Invalid.**

**Trap:** checking only that the sequence zig-zags around 47; you must check every key against *all* previous bounds, not just the immediately preceding key.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

def valid(seq, x):
    lo, hi = float('-inf'), float('inf')
    for v in seq[:-1]:
        if not lo < v < hi: return False
        if x < v: hi = v
        else: lo = v
    return seq[-1] == x
opts = [[90,25,80,30,70,40,60,47], [52,15,48,22,39,50,47],
        [20,60,30,55,50,35,47], [10,75,64,43,58,53,47]]
assert [c for c, s in zip("ABCD", opts) if not valid(s, 47)] == [ANSWER]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph traversal — BFS order',
            'text': 'Breadth-first search is run on the undirected graph below starting at A. When a vertex is dequeued, its unvisited neighbours are enqueued in **alphabetical order**. The order in which vertices are visited (enqueued) is',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'E'],
                        ['A', 'F'],
                        ['B', 'C'],
                        ['B', 'G'],
                        ['C', 'D'],
                        ['E', 'F'],
                        ['F', 'G'],
                        ['G', 'H'],
                        ['D', 'H'],
                        ['C', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [4, 2],
                        'D': [6, 2],
                        'E': [0, 0],
                        'F': [2, 0],
                        'G': [4, 0],
                        'H': [6, 0],
                    },
                },
            ],
            'options': [
                'A, B, F, E, C, G, D, H',
                'A, B, C, D, H, G, F, E',
                'A, B, E, F, G, C, H, D',
                'A, B, E, F, C, G, D, H',
            ],
            'answer': 'D',
            'solution': '''**Concept:** BFS visits vertices level by level; within a level the order is inherited from the order in which parents were dequeued, and each parent adds children alphabetically.

Trace (queue after each dequeue):
- dequeue A → enqueue B, E, F → [B, E, F]
- dequeue B → unvisited nbrs C, G → [E, F, C, G]
- dequeue E → nbrs A, F already seen → [F, C, G]
- dequeue F → nbrs A, E, G seen → [C, G]
- dequeue C → nbr D new → [G, D]
- dequeue G → nbr H new → [D, H]
- dequeue D, H → nothing new.

Order: **A, B, E, F, C, G, D, H** (levels: {A}, {B, E, F}, {C, G}, {D, H}).

**Options:** (B) is a DFS order. (C) lets F (dequeued after B and E) discover G before B does. (A) enqueues A's neighbours out of alphabetical order.

**Tip:** the level sets are fixed by distances; only the order inside a level depends on tie-breaking.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'E'],
                        ['A', 'F'],
                        ['B', 'C'],
                        ['B', 'G'],
                        ['C', 'D'],
                        ['E', 'F'],
                        ['F', 'G'],
                        ['G', 'H'],
                        ['D', 'H'],
                        ['C', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [4, 2],
                        'D': [6, 2],
                        'E': [0, 0],
                        'F': [2, 0],
                        'G': [4, 0],
                        'H': [6, 0],
                    },
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'E'],
                        ['A', 'F'],
                        ['B', 'C'],
                        ['B', 'G'],
                        ['C', 'D'],
                        ['G', 'H'],
                    ],
                    'caption': 'BFS tree (highlighted edges)',
                },
            ],
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

from collections import deque
E = [('A','B'),('A','E'),('A','F'),('B','C'),('B','G'),('C','D'),('E','F'),
     ('F','G'),('G','H'),('D','H'),('C','G')]
G = {}
for u, v in E:
    G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
q, seen = deque(['A']), ['A']
while q:
    u = q.popleft()
    for v in sorted(G[u]):
        if v not in seen:
            seen.append(v); q.append(v)
assert ", ".join(seen) == "A, B, E, F, C, G, D, H" and ANSWER == "A"
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph theory — graphical degree sequences',
            'text': 'Which of the following sequences is/are the degree sequence of some **simple** undirected graph (no self-loops, no multi-edges)?',
            'options': [
                '(5, 5, 4, 3, 2, 1)',
                '(4, 4, 3, 2, 1, 0)',
                '(6, 2, 2, 2, 2, 2, 2)',
                '(3, 3, 3, 3, 2, 2)',
            ],
            'answer': ['C', 'D'],
            'solution': '''**Concept:** the degree sum must be even (handshaking lemma), and the Havel–Hakimi test applies: remove the largest degree d and subtract 1 from the next d largest; the sequence is graphical iff this ends in all zeros.

- (A) sum 20 (even), but on 6 vertices two vertices of degree 5 are adjacent to *all* others, so every vertex has degree ≥ 2 — the 1 is impossible. **Not graphical.**
- (B) drop the isolated vertex: (4, 4, 3, 2, 1) on 5 vertices; two degree-4 vertices force every other degree ≥ 2, contradicting the 1. **Not graphical.**
- (C) sum 18. The degree-6 vertex is adjacent to all six others; each of those needs one more edge among themselves — a perfect matching on 6 vertices works. **Graphical.**
- (D) sum 16. HH: 3,3,3,3,2,2 → 2,2,2,2,2 → 1,1,2,2 → sort 2,2,1,1 → 1,0,1 → sort 1,1,0 → 0,0. **Graphical** (e.g. a 6-cycle plus two chords).

**Trap:** an even sum is necessary but not sufficient — (A) passes the parity test.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def hh(d):
    d = sorted(d, reverse=True)
    while d and d[0] > 0:
        k = d.pop(0)
        if k > len(d): return False
        for i in range(k): d[i] -= 1
        if min(d) < 0: return False
        d.sort(reverse=True)
    return True
opts = [(3,3,3,3,2,2), (5,5,4,3,2,1), (6,2,2,2,2,2,2), (4,4,3,2,1,0)]
assert sorted(ANSWER) == [c for c, s in zip("ABCD", opts) if hh(list(s))]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — list-comprehension quicksort with duplicates',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def qs(a):
    if len(a) <= 1:
        return a
    p, rest = a[0], a[1:]
    return (qs([x for x in rest if x < p]) + [p] +
            qs([x for x in rest if x > p]))

data = [4, 7, 4, 1, 7, 3, 4]
r = qs(data)
print(len(r), r[-2:], data is r)''',
            'options': ['`7 [7, 7] False`', '`5 [4, 7] False`', '`4 [4, 7] False`', '`4 [4, 7] True`'],
            'answer': 'C',
            'solution': '''**Concept:** this 'functional' quicksort partitions with strict `<` and strict `>`, so every element **equal** to the pivot (other than the pivot itself) is silently dropped. It also builds new lists, so the result is never the input object (except for inputs of length ≤ 1, which are returned as is).

Trace:
- qs([4, 7, 4, 1, 7, 3, 4]): p = 4; less = [1, 3]; greater = [7, 7]; the two other 4s vanish.
- qs([1, 3]): p = 1, less = [], greater = [3] → [1, 3].
- qs([7, 7]): p = 7, less = [], greater = [] (the second 7 is dropped) → [7].
- Result: [1, 3] + [4] + [7] = [1, 3, 4, 7].

So `len(r)` = 4, `r[-2:]` = [4, 7], `data is r` is False → `4 [4, 7] False`.

**Options:**
- (A) assumes duplicates are kept (a correct sort would give length 7 and end with [7, 7]).
- (B) keeps one duplicate too many.
- (D) claims the returned list is the input object — impossible for length > 1.

**Tip:** the fix is `<=` for one side (or a three-way split `<`, `==`, `>`). The bug only shows up with repeated keys — a classic test case to include.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '4 [4, 7] False' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — total comparisons (Lomuto)',
            'text': 'Quicksort with the Lomuto partition of Q.2 (pivot = last element of the subarray; one comparison `a[j] <= x` per loop iteration) is used to sort A = [7, 3, 9, 1, 6, 8, 2, 5]. Recursive calls on subarrays of size 0 or 1 do not partition. The total number of comparisons `a[j] <= x` made over the whole sort is ______.',
            'answer': '13',
            'solution': '''**Concept:** partitioning a subarray of size m costs exactly m − 1 comparisons; the total is the sum over all partition calls, and the call sizes depend on where each pivot lands.

Trace (see table):
- Call on [0..7], pivot 5: elements ≤ 5 are 3, 1, 2 → array [3, 1, 2, **5**, 6, 8, 9, 7], pivot at 3. Cost 7.
- Call on [0..2] = [3, 1, 2], pivot 2: → [1, **2**, 3], pivot at 1. Cost 2. Its two sides have size 1 → no further work.
- Call on [4..7] = [6, 8, 9, 7], pivot 7: 6 ≤ 7 → [6, **7**, 9, 8], pivot at 5. Cost 3.
- Left side [4..4] size 1; right side [6..7] = [9, 8], pivot 8 → [**8**, 9]. Cost 1.

Total = 7 + 2 + 3 + 1 = **13**.

For comparison, the worst case for n = 8 (e.g. already-sorted input) costs 7 + 6 + … + 1 = 28 comparisons; this input's well-placed first pivot saves more than half.

**Trap:** counting n comparisons per partition instead of n − 1, or forgetting the small size-2 partition at the end.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each partition call (pivot highlighted)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', 'cost'],
                    'row_labels': ['start', '[0..7]', '[0..2]', '[4..7]', '[6..7]'],
                    'rows': [
                        [7, 3, 9, 1, 6, 8, 2, 5, ''],
                        [3, 1, 2, 5, 6, 8, 9, 7, 7],
                        [1, 2, 3, 5, 6, 8, 9, 7, 2],
                        [1, 2, 3, 5, 6, 7, 9, 8, 3],
                        [1, 2, 3, 5, 6, 7, 8, 9, 1],
                    ],
                    'highlight': [
                        [1, 3],
                        [2, 1],
                        [3, 5],
                        [4, 6],
                    ],
                },
            ],
            'verify': '''
cmp = 0
def lom(a, lo, hi):
    global cmp
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        cmp += 1
        if a[j] <= x:
            i += 1; a[i], a[j] = a[j], a[i]
    a[i+1], a[hi] = a[hi], a[i+1]
    return i + 1
def qsort(a, lo, hi):
    if lo < hi:
        p = lom(a, lo, hi); qsort(a, lo, p-1); qsort(a, p+1, hi)
A = [7, 3, 9, 1, 6, 8, 2, 5]
qsort(A, 0, 7)
assert A == sorted(A) and cmp == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort — best/worst case and recurrences',
            'text': 'Which of the following statements is/are TRUE?',
            'options': [
                'If the pivot is always the second-smallest element of its subarray, quicksort runs in Θ(n log n) time',
                'Quicksort with the Lomuto partition (pivot = last, test `a[j] <= x`) makes exactly n(n − 1)/2 comparisons on an array of n equal keys',
                'If every partition step splits its subarray in the ratio 1 : 9, quicksort runs in Θ(n log n) time',
                'The recurrence T(n) = 2T(n/2) + c, T(1) = c, solves to Θ(n log n)',
            ],
            'answer': ['B', 'C'],
            'solution': '''**Concept:** quicksort's cost depends on the *depth* of the recursion tree. Any constant-fraction split gives O(log n) depth and Θ(n) work per level; a split that removes only a constant number of elements gives Θ(n) depth.

- (A) Each partition removes the pivot and one element to its left: T(n) = T(n − 2) + T(1) + Θ(n) → Θ(n²). **False.**
- (B) With all keys equal, `a[j] <= x` is always true, so the pivot lands at `hi` every time; subproblem sizes are n, n − 1, …, 2 with n − 1, n − 2, …, 1 comparisons — total n(n − 1)/2. **True.** (Hoare's scheme or three-way partitioning avoid this.)
- (C) T(n) = T(n/10) + T(9n/10) + Θ(n). Every level of the recursion tree does at most cn work and the depth is log_{10/9} n = Θ(log n); the first log₁₀ n levels are full, so the total is Θ(n log n). **True.**
- (D) Master theorem: a = 2, b = 2, n^{log₂2} = n dominates f(n) = c → Θ(n). Exactly, T(n) = (2n − 1)c for n a power of 2. **False.**

**Trap:** (A) 'looks' like a non-extreme pivot, but a split of (1, n − 2) is just as bad as (0, n − 1) asymptotically.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import sys
sys.setrecursionlimit(10000)
from functools import lru_cache
@lru_cache(None)
def T19(n):
    if n <= 1: return 0
    k = n // 10
    return T19(k) + T19(n - 1 - k) + n
import math
r1 = T19(10**4) / (10**4 * math.log2(10**4))
r2 = T19(10**5) / (10**5 * math.log2(10**5))
A_true = 0.5 < r2 / r1 < 1.5
def T2(n):
    t = 0
    while n > 1:
        t += n - 1; n -= 2
    return t
B_true = not (T2(4000) / T2(2000) > 3.5)
cmp = 0
def lom(a, lo, hi):
    global cmp
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        cmp += 1
        if a[j] <= x:
            i += 1; a[i], a[j] = a[j], a[i]
    a[i+1], a[hi] = a[hi], a[i+1]
    return i + 1
def qsort(a, lo, hi):
    while lo < hi:
        p = lom(a, lo, hi); qsort(a, p+1, hi); hi = p - 1
n = 300
qsort([7]*n, 0, n-1)
C_true = cmp == n*(n-1)//2
def T4(n): return 1 if n == 1 else 2*T4(n//2) + 1
D_true = not (T4(1024) == 2*1024 - 1)
assert sorted(ANSWER) == [c for c, t in zip("ABCD", [A_true, B_true, C_true, D_true]) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quickselect — partition-based selection',
            'text': 'The function below finds the k-th smallest element (k is a 0-based index) using the Lomuto partition of Q.2. It is called as `select(a, 0, 9, 3)` on a = [14, 3, 22, 9, 17, 5, 11, 26, 8, 19]. The total number of comparisons `a[j] <= x` performed inside `partition` during this call is ______.',
            'code': '''def select(a, lo, hi, k):
    if lo == hi:
        return a[lo]
    p = partition(a, lo, hi)
    if p == k:
        return a[p]
    if p < k:
        return select(a, p + 1, hi, k)
    return select(a, lo, p - 1, k)''',
            'run_code': False,
            'answer': '18',
            'solution': '''**Concept:** quickselect partitions like quicksort but recurses into **one** side only — the side containing index k. Expected time is Θ(n), worst case Θ(n²).

Target: index 3 = the 4th smallest. (Sorted: 3, 5, 8, **9**, 11, …)

- Call [0..9], pivot 19: elements ≤ 19 are 14, 3, 9, 17, 5, 11, 8 → [14, 3, 9, 17, 5, 11, 8, **19**, 22, 26], p = 7. Cost **9**. 7 > 3 → recurse left [0..6].
- Call [0..6], pivot 8: ≤ 8 are 3, 5 → [3, 5, **8**, 17, 14, 11, 9, …], p = 2. Cost **6**. 2 < 3 → recurse right [3..6].
- Call [3..6] = [17, 14, 11, 9], pivot 9: nothing ≤ 9 → pivot swapped to index 3 → [3, 5, 8, **9**, 14, 11, 17, …], p = 3. Cost **3**. p == k → return 9.

Total comparisons = 9 + 6 + 3 = **18**, and the answer returned is 9.

**Trap:** recursing into both sides (as full quicksort would) or counting n instead of n − 1 comparisons per partition (which gives 10 + 7 + 4 = 21).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Quickselect trace (pivot highlighted)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'cost'],
                    'row_labels': ['start', '[0..9]', '[0..6]', '[3..6]'],
                    'rows': [
                        [14, 3, 22, 9, 17, 5, 11, 26, 8, 19, ''],
                        [14, 3, 9, 17, 5, 11, 8, 19, 22, 26, 9],
                        [3, 5, 8, 17, 14, 11, 9, 19, 22, 26, 6],
                        [3, 5, 8, 9, 14, 11, 17, 19, 22, 26, 3],
                    ],
                    'highlight': [
                        [1, 7],
                        [2, 2],
                        [3, 3],
                    ],
                },
            ],
            'verify': '''
cmp = 0
def partition(a, lo, hi):
    global cmp
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        cmp += 1
        if a[j] <= x:
            i += 1; a[i], a[j] = a[j], a[i]
    a[i+1], a[hi] = a[hi], a[i+1]
    return i + 1
def select(a, lo, hi, k):
    if lo == hi:
        return a[lo]
    p = partition(a, lo, hi)
    if p == k:
        return a[p]
    if p < k:
        return select(a, p + 1, hi, k)
    return select(a, lo, p - 1, k)
a = [14, 3, 22, 9, 17, 5, 11, 26, 8, 19]
assert select(a, 0, 9, 3) == 9 and cmp == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — three-way (Dutch national flag) partition',
            'text': 'The three-way partition below is applied to a = [5, 8, 2, 5, 9, 1, 5, 7, 3] with pivot value p = 5. What are the final array and the values of `lt` and `gt`?',
            'code': '''def three_way(a, p):
    lt, i, gt = 0, 0, len(a) - 1
    while i <= gt:
        if a[i] < p:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > p:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt''',
            'options': [
                '[3, 2, 1, 5, 5, 5, 9, 7, 8], lt = 3, gt = 5',
                '[3, 2, 1, 5, 5, 5, 7, 9, 8], lt = 3, gt = 5',
                '[2, 1, 3, 5, 5, 5, 7, 9, 8], lt = 3, gt = 5',
                '[3, 2, 1, 5, 5, 5, 7, 9, 8], lt = 3, gt = 6',
            ],
            'answer': 'B',
            'solution': '''**Concept:** invariant a[0..lt−1] < p, a[lt..i−1] = p, a[gt+1..n−1] > p, a[i..gt] unseen. After a swap with `gt`, i is **not** advanced because the element brought in is unseen.

Trace (lt, i, gt start at 0, 0, 8):
- i=0: 5 = p → i = 1.
- i=1: 8 > p → swap with a[8] → [5, 3, 2, 5, 9, 1, 5, 7, 8], gt = 7.
- i=1: 3 < p → swap a[0]↔a[1] → [3, 5, 2, 5, 9, 1, 5, 7, 8], lt = 1, i = 2.
- i=2: 2 < p → swap a[1]↔a[2] → [3, 2, 5, 5, 9, 1, 5, 7, 8], lt = 2, i = 3.
- i=3: 5 → i = 4.
- i=4: 9 > p → swap with a[7] → [3, 2, 5, 5, 7, 1, 5, 9, 8], gt = 6.
- i=4: 7 > p → swap with a[6] → [3, 2, 5, 5, 5, 1, 7, 9, 8], gt = 5.
- i=4: 5 → i = 5.
- i=5: 1 < p → swap a[2]↔a[5] → [3, 2, 1, 5, 5, 5, 7, 9, 8], lt = 3, i = 6 > gt → stop.

Final: **[3, 2, 1, 5, 5, 5, 7, 9, 8], lt = 3, gt = 5** → (B). The equal block is a[3..5].

**Options:** (A) gets the > block order wrong (9 and 7 were swapped twice). (C) sorts the < block, which partitioning never does. (D) has gt one too large — gt must point at the last element equal to p.

**Tip:** three-way partitioning makes quicksort Θ(n) on arrays with all keys equal.''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

a = [5, 8, 2, 5, 9, 1, 5, 7, 3]
lt, gt = three_way(a, 5)
assert a == [3, 2, 1, 5, 5, 5, 7, 9, 8] and (lt, gt) == (3, 5) and ANSWER == "C"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — counting merge comparisons',
            'text': 'Top-down merge sort (split a list of length n into the first ⌊n/2⌋ and the remaining elements) sorts [6, 2, 9, 4, 1, 8, 3, 7]. During a merge, one comparison is made for each element output while both halves are non-empty; once one half is exhausted, the rest is copied without comparisons. The total number of comparisons is ______.',
            'answer': '17',
            'solution': '''**Concept:** merging lists of sizes p and q costs between min(p, q) and p + q − 1 comparisons; the exact count is p + q − (number of elements left over when one side runs out).

Recursion:
- [6, 2] → 1 comparison → [2, 6]; [9, 4] → 1 → [4, 9].
- merge [2, 6] + [4, 9]: 2 vs 4, 6 vs 4, 6 vs 9 → 3 comparisons, 9 copied → [2, 4, 6, 9].
- [1, 8] → 1 → [1, 8]; [3, 7] → 1 → [3, 7].
- merge [1, 8] + [3, 7]: 1 vs 3, 8 vs 3, 8 vs 7 → 3 comparisons, 8 copied → [1, 3, 7, 8].
- final merge [2, 4, 6, 9] + [1, 3, 7, 8]: 2–1, 2–3, 4–3, 4–7, 6–7, 9–7, 9–8 → 7 comparisons, 9 copied.

Total = 1 + 1 + 3 + 1 + 1 + 3 + 7 = **17** (the maximum possible for n = 8 is 17 as well: 4·1 + 2·3 + 7).

**Contrast:** on already-sorted input the counts are 1, 1, 2, 1, 1, 2, 4 = 12 (minimum).

**Trap:** counting a comparison for the copied tail elements (giving 8 + 4 + 4 + … = 24).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Merges and their comparison counts',
                    'col_labels': ['left', 'right', 'result', 'comps'],
                    'row_labels': ['1', '2', '3', '4', '5', '6', '7'],
                    'rows': [
                        ['[6]', '[2]', '[2,6]', 1],
                        ['[9]', '[4]', '[4,9]', 1],
                        ['[2,6]', '[4,9]', '[2,4,6,9]', 3],
                        ['[1]', '[8]', '[1,8]', 1],
                        ['[3]', '[7]', '[3,7]', 1],
                        ['[1,8]', '[3,7]', '[1,3,7,8]', 3],
                        ['[2,4,6,9]', '[1,3,7,8]', '[1..9]', 7],
                    ],
                },
            ],
            'verify': '''
c = 0
def ms(a):
    global c
    if len(a) <= 1: return a
    m = len(a) // 2
    L, R = ms(a[:m]), ms(a[m:])
    out, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        c += 1
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
assert ms([6, 2, 9, 4, 1, 8, 3, 7]) == [1, 2, 3, 4, 6, 7, 8, 9] and c == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra with ties',
            'text': "Dijkstra's algorithm is run from S on the weighted undirected graph below. A tentative distance (and the predecessor) is updated only on a **strict** improvement. Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 1],
                        ['A', 'B', 2],
                        ['A', 'C', 5],
                        ['B', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'T', 3],
                        ['D', 'T', 6],
                        ['A', 'D', 4],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 2],
                        'D': [4, 0],
                        'T': [6, 1],
                    },
                },
            ],
            'options': [
                'The shortest-path distance from S to T is 11',
                'There are exactly two distinct shortest paths from S to C',
                'The vertices are extracted (finalised) in the order S, B, A, D, C, T',
                'In the shortest-path tree produced, the parent of C is D',
            ],
            'answer': ['A', 'C'],
            'solution': '''**Concept:** Dijkstra finalises vertices in non-decreasing order of distance. Ties in path length do not change distances, but with strict updates the *first* vertex that achieves the best value stays as predecessor.

Trace:
- Extract S (0): A = 4, B = 1.
- Extract B (1): A = min(4, 1 + 2) = 3 (parent B); D = 1 + 6 = 7 (parent B).
- Extract A (3): C = 3 + 5 = 8 (parent A); D: 3 + 4 = 7, not < 7 → unchanged.
- Extract D (7): C: 7 + 1 = 8, not < 8 → parent stays A; T = 7 + 6 = 13.
- Extract C (8): T = min(13, 8 + 3) = 11 (parent C).
- Extract T (11).

**Verdicts:**
- (A) d(T) = 11 (S–B–A–C–T). **True.**
- (B) Shortest S–C paths of length 8: S–B–A–C (1 + 2 + 5), S–B–D–C (1 + 6 + 1) and S–B–A–D–C (1 + 2 + 4 + 1) — **three**, not two. **False.**
- (C) Order S, B, A, D, C, T. **True.**
- (D) C's parent is A, because D offered only an equal distance. **False.**

**Trap:** missing the path through the diagonal A–D in (B); and in (D) assuming the *last* equal offer wins.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'T'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 1],
                        ['A', 'B', 2],
                        ['A', 'C', 5],
                        ['B', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'T', 3],
                        ['D', 'T', 6],
                        ['A', 'D', 4],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 2],
                        'D': [4, 0],
                        'T': [6, 1],
                    },
                    'highlight_edges': [
                        ['S', 'B'],
                        ['B', 'A'],
                        ['B', 'D'],
                        ['A', 'C'],
                        ['C', 'T'],
                    ],
                    'caption': 'Shortest-path tree produced (strict updates)',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import heapq
E = [('S','A',4),('S','B',1),('A','B',2),('A','C',5),('B','D',6),('C','D',1),
     ('C','T',3),('D','T',6),('A','D',4)]
G = {}
for u, v, w in E:
    G.setdefault(u, {})[v] = w; G.setdefault(v, {})[u] = w
d = {v: float('inf') for v in G}; d['S'] = 0; par = {}; done = []; pq = [(0, 'S')]
while pq:
    du, u = heapq.heappop(pq)
    if u in done: continue
    done.append(u)
    for v, w in G[u].items():
        if du + w < d[v]:
            d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
def paths(u, t, seen):
    if u == t:
        yield 0; return
    for v, w in G[u].items():
        if v not in seen:
            for c in paths(v, t, seen | {v}): yield c + w
nC = sum(1 for c in paths('S', 'C', {'S'}) if c == d['C'])
truth = [done == list("SBADCT"), d['T'] == 11, nC == 2, par['C'] == 'D']
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array [3, 9, 2, 1, 4, 5, 8, 7, 10, 6] (0-based) is converted into a **max**-heap using the bottom-up build-heap procedure: sift-down is called for i = ⌊n/2⌋ − 1 down to 0, and each sift-down repeatedly swaps a node with its larger child while that child is larger. The total number of swaps performed is ______.',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 9, 2, 1, 4, 5, 8, 7, 10, 6],
                    'caption': 'Initial array viewed as a complete binary tree',
                },
            ],
            'answer': '7',
            'solution': '''**Concept:** bottom-up heapify processes internal nodes from the last one (index ⌊n/2⌋ − 1 = 4) back to the root; a node at height h causes at most h swaps, giving O(n) total.

Trace:
- i = 4 (4): only child index 9 (6) > 4 → swap (1). → [3, 9, 2, 1, 6, 5, 8, 7, 10, 4]
- i = 3 (1): children 7, 10 → swap with 10 (2). → [3, 9, 2, 10, 6, 5, 8, 7, 1, 4]
- i = 2 (2): children 5, 8 → swap with 8 (3). → [3, 9, 8, 10, 6, 5, 2, 7, 1, 4]
- i = 1 (9): children 10, 6 → swap with 10 (4); at index 3, children 7, 1 < 9 → stop. → [3, 10, 8, 9, 6, 5, 2, 7, 1, 4]
- i = 0 (3): children 10, 8 → swap (5); at index 1 children 9, 6 → swap (6); at index 3 children 7, 1 → swap with 7 (7); index 7 is a leaf.

Final heap [10, 9, 8, 7, 6, 5, 2, 3, 1, 4], total swaps = **7**.

**Trap:** inserting the elements one by one (top-down, sift-up) is a *different* algorithm and generally performs a different number of swaps and can yield a different heap.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [10, 9, 8, 7, 6, 5, 2, 3, 1, 4],
                    'caption': 'Max-heap after build-heap',
                },
            ],
            'verify': '''
a = [3, 9, 2, 1, 4, 5, 8, 7, 10, 6]; n = len(a); sw = 0
for i in range(n // 2 - 1, -1, -1):
    j = i
    while True:
        l, r, m = 2*j+1, 2*j+2, j
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == j: break
        a[j], a[m] = a[m], a[j]; sw += 1; j = m
assert sw == int(ANSWER) and a == [10, 9, 8, 7, 6, 5, 2, 3, 1, 4]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Insertion sort — comparisons and shifts',
            'text': 'Insertion sort (below) sorts a = [2, 3, 5, 1, 4, 6, 8, 7] in ascending order. A *comparison* is one evaluation of `a[j] > key` and a *shift* is one execution of `a[j + 1] = a[j]`. The pair (number of comparisons, number of shifts) is',
            'code': '''for i in range(1, len(a)):
    key, j = a[i], i - 1
    while j >= 0 and a[j] > key:
        a[j + 1] = a[j]
        j -= 1
    a[j + 1] = key''',
            'run_code': False,
            'options': ['(12, 5)', '(11, 5)', '(11, 4)', '(16, 5)'],
            'answer': 'B',
            'solution': '''**Concept:** shifts = number of inversions. Each insertion makes (shifts for that key) + 1 comparisons, **except** when the key travels all the way to index 0 — then `j >= 0` fails first and the comparison `a[j] > key` is short-circuited away.

Inversions of [2, 3, 5, 1, 4, 6, 8, 7]: (2,1), (3,1), (5,1), (5,4), (8,7) = **5 shifts**.

Per insertion (key: comparisons / shifts):
- 3: 1 / 0
- 5: 1 / 0
- 1: compares with 5, 3, 2 (all shift), then j = −1 → 3 / 3 (no 4th comparison)
- 4: 5 (shift), 3 (stop) → 2 / 1
- 6: 1 / 0
- 8: 1 / 0
- 7: 8 (shift), 6 (stop) → 2 / 1

Comparisons = 1 + 1 + 3 + 2 + 1 + 1 + 2 = **11**; shifts = **5** → (B).

**Options:** (A) adds a phantom comparison when 1 reaches the front (the formula inversions + n − 1 = 12 overcounts by the number of keys that reach index 0). (C) misses an inversion. (D) counts 2 comparisons per shift.

**Trap:** short-circuit `and` — `a[j] > key` is never evaluated once `j >= 0` is False.''',
            'verify': '''
a = [2, 3, 5, 1, 4, 6, 8, 7]; comps = shifts = 0
for i in range(1, len(a)):
    key, j = a[i], i - 1
    while j >= 0:
        comps += 1
        if a[j] > key:
            a[j+1] = a[j]; shifts += 1; j -= 1
        else:
            break
    a[j+1] = key
opts = [(12, 5), (11, 5), (11, 4), (16, 5)]
assert a == sorted(a) and opts["ABCD".index(ANSWER)] == (comps, shifts)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BFS — counting shortest paths',
            'text': 'Consider the unweighted undirected graph below. A *shortest S–T path* is one with the minimum number of edges. BFS from S enqueues neighbours in alphabetical order. Which of the following statements is/are TRUE?',
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
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['D', 'G'],
                        ['F', 'T'],
                        ['G', 'T'],
                        ['E', 'H'],
                        ['H', 'T'],
                    ],
                    'pos': {
                        'S': [0, 2],
                        'A': [2, 4],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 3],
                        'E': [4, 1],
                        'G': [6, 4],
                        'F': [6, 2],
                        'H': [6, 0],
                        'T': [8, 2],
                    },
                },
            ],
            'options': [
                'Every shortest S–T path passes through E',
                'There are exactly 8 shortest S–T paths',
                'Exactly 4 shortest S–T paths pass through D',
                'In the BFS tree, the parent of T is F',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept:** in BFS, the number of shortest paths to v is the sum of the counts of its neighbours one level closer: σ(v) = Σ σ(u) over edges u–v with dist(u) = dist(v) − 1.

Levels and counts σ:
- level 0: S (σ = 1)
- level 1: A, B, C (σ = 1 each)
- level 2: D ← A, B (σ = 2); E ← B, C (σ = 2)
- level 3: F ← D, E (σ = 4); G ← D (σ = 2); H ← E (σ = 2)
- level 4: T ← F, G, H (σ = 4 + 2 + 2 = **8**)

**Verdicts:**
- (A) **False** — paths through D (e.g. S–A–D–G–T) avoid E.
- (B) **True** — 8 shortest paths of length 4.
- (C) Paths through D = σ(D) × (shortest D→T paths) = 2 × 2 (via F or G) = 4. **True.** (D and E are on the same level, so no shortest path uses both; the other 4 go through E.)
- (D) Level-3 vertices are dequeued in the order F, G, H (F was discovered first, by D); F is the first to see T. **True.**

**Trap:** counting paths by enumerating by hand often misses the 'cross' paths S–B–D–F–T and S–B–E–F–T; the σ recurrence avoids that.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS distance and path count σ',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'row_labels': ['dist', 'σ'],
                    'rows': [
                        [0, 1, 1, 1, 2, 2, 3, 3, 3, 4],
                        [1, 1, 1, 1, 2, 2, 4, 2, 2, 8],
                    ],
                    'highlight': [
                        [1, 9],
                    ],
                },
            ],
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from collections import deque
E = [('S','A'),('S','B'),('S','C'),('A','D'),('B','D'),('B','E'),('C','E'),('D','F'),
     ('E','F'),('D','G'),('F','T'),('G','T'),('E','H'),('H','T')]
G = {}
for u, v in E:
    G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
def bfs(s, banned=()):
    dist, cnt, par, q = {s: 0}, {s: 1}, {}, deque([s])
    while q:
        u = q.popleft()
        for v in sorted(G[u]):
            if v in banned: continue
            if v not in dist:
                dist[v] = dist[u] + 1; cnt[v] = cnt[u]; par[v] = u; q.append(v)
            elif dist[v] == dist[u] + 1:
                cnt[v] += cnt[u]
    return dist, cnt, par
dist, cnt, par = bfs('S')
dE, cE, _ = bfs('S', banned=('E',))
dD, cD, _ = bfs('S', banned=('D',))
through_D = cnt['T'] - (cD['T'] if dD.get('T') == dist['T'] else 0)
all_E = dE.get('T') != dist['T']
truth = [cnt['T'] == 8, all_E, through_D == 4, par['T'] == 'F']
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
    ],
}
