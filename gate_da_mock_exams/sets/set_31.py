# Set 31 — Full-Syllabus Mock — Paper 1

SET = {
    'number': 31,
    'title': 'Full-Syllabus Mock — Paper 1',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — split, join and reversal',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "  GATE  DA 2027 "
parts = s.split()
t = "-".join(p[::-1] for p in parts)
print(t, len(s.split(" ")))''',
            'options': ['`ETAG-AD-7202 3`', '`ETAG--AD-7202 6`', '`7202-AD-ETAG 7`', '`ETAG-AD-7202 7`'],
            'answer': 'D',
            'solution': '''`split()` with no argument splits on **runs** of whitespace and discards leading and trailing whitespace; `split(" ")` splits on **every single space**, producing empty strings between consecutive separators and at the ends.

- `s.split()` → ['GATE', 'DA', '2027'].
- Each part reversed: 'ETAG', 'AD', '7202'; joined with '-' → `ETAG-AD-7202`.
- `s.split(" ")`: s = ␣␣GATE␣␣DA␣2027␣ has 6 spaces, so it yields 7 pieces: ['', '', 'GATE', '', 'DA', '2027', ''] → length 7.

Output `ETAG-AD-7202 7` → (D).

- (A) assumes `split(" ")` behaves like `split()`.
- (B) keeps an empty word in the join and miscounts the pieces.
- (C) reverses the order of the words instead of each word.

**Tip:** `len(s.split(sep))` = (number of occurrences of sep) + 1 for any explicit separator.''',
            'verify': "ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'ETAG-AD-7202 7' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — generator exhaustion',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''g = (x * x for x in range(6) if x % 2)
print(sum(g) + sum(g) + max(g, default=-1))''',
            'answer': '34',
            'solution': '''A generator expression produces its values **once**. After it has been consumed, further iteration yields nothing.

- The generator yields squares of the odd numbers in range(6): 1, 9, 25.
- First `sum(g)` consumes them all → 35.
- Second `sum(g)` sees an exhausted generator → sum of nothing = 0.
- `max(g, default=-1)` also sees nothing → returns the default −1 (without `default` it would raise ValueError).

Total = 35 + 0 + (−1) = **34**.

If `g` were a list comprehension `[x * x for …]`, the result would be 35 + 35 + 25 = 95.

**Trap:** treating the generator like a list. Note also that the operands of `+` are evaluated left to right, so the first `sum` is the one that sees the values.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues — queue using two stacks',
            'text': '''A queue is implemented with two stacks IN and OUT. ENQUEUE(x) pushes x onto IN. DEQUEUE pops from OUT; if OUT is empty it first pops **every** element of IN and pushes it onto OUT (each such move is one *transfer*). Starting empty, the operations are:
ENQ 1, ENQ 2, ENQ 3, DEQ, ENQ 4, ENQ 5, DEQ, DEQ, ENQ 6, DEQ.
Which option gives the values returned by the four DEQs and the total number of transfers?''',
            'options': [
                '1, 2, 3, 4 and 6 transfers',
                '1, 2, 3, 4 and 5 transfers',
                '3, 2, 1, 6 and 6 transfers',
                '1, 2, 4, 5 and 4 transfers',
            ],
            'answer': 'A',
            'solution': '''Transfers reverse the order of IN, so the oldest element ends on top of OUT; the structure is a correct FIFO queue.

- ENQ 1, 2, 3 → IN = [1, 2, 3], OUT = [].
- DEQ: OUT empty → move 3, 2, 1 (3 transfers) → OUT = [3, 2, 1] (top 1); pop → **1**.
- ENQ 4, 5 → IN = [4, 5].
- DEQ → OUT non-empty, pop → **2**.
- DEQ → pop → **3**; OUT now empty.
- ENQ 6 → IN = [4, 5, 6].
- DEQ: OUT empty → move 6, 5, 4 (3 transfers) → pop → **4**.

Returned values 1, 2, 3, 4 with 3 + 3 = **6** transfers → (A).

- (B) forgets that the second refill moves 6 as well.
- (C) treats the structure as a stack.
- (D) assumes 4 and 5 jump ahead after the first refill.

**Tip:** each element is transferred at most once, so any sequence of m operations costs O(m) in total — amortised O(1) per operation.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [6, 5],
                    'label': 'OUT',
                    'caption': 'OUT after the last DEQ (top = 5)',
                },
            ],
            'verify': '''
IN, OUT, out, tr = [], [], [], 0
ops = ["E1","E2","E3","D","E4","E5","D","D","E6","D"]
for op in ops:
    if op[0] == "E": IN.append(int(op[1:]))
    else:
        if not OUT:
            while IN: OUT.append(IN.pop()); tr += 1
        out.append(OUT.pop())
assert out == [1, 2, 3, 4] and tr == 6 and OUT == [6, 5] and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Circular linked lists — repeated deletion',
            'text': 'Nine nodes labelled 1 to 9 form the circular singly linked list shown. Starting the count at node 1, the process repeatedly counts 4 nodes (the node where the count starts is counted as 1), deletes the 4th node, and restarts the count at the node following the deleted one, until one node remains. The label of the **fifth** node deleted is ______.',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    'circular': True,
                    'head': 'start',
                },
            ],
            'answer': '6',
            'solution': '''Simulate, writing the remaining circle starting from where the count begins:

- Count 1, 2, 3, 4 → delete **4**; restart at 5. Remaining: 5 6 7 8 9 1 2 3.
- Count 5, 6, 7, 8 → delete **8**; restart at 9. Remaining: 9 1 2 3 5 6 7.
- Count 9, 1, 2, 3 → delete **3**; restart at 5. Remaining: 5 6 7 9 1 2.
- Count 5, 6, 7, 9 → delete **9**; restart at 1. Remaining: 1 2 5 6 7.
- Count 1, 2, 5, 6 → delete **6**; restart at 7. Remaining: 7 1 2 5.

The fifth deletion removes node **6**. (Continuing: 5, 7, 2 are deleted and node 1 survives.)

In a circular list, deletion needs a pointer to the node **before** the victim, so an implementation walks k − 1 = 3 links from the predecessor each round; total work is O(nk).

**Trap:** restarting the count at the deleted node's predecessor, or counting the start node as 0, shifts every later deletion.''',
            'verify': '''
L = list(range(1, 10)); i = 0; order = []
while len(L) > 1:
    i = (i + 3) % len(L); order.append(L.pop(i))
assert order[4] == int(ANSWER) and L == [1]
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search trees — deletion and successors',
            'text': 'Consider the binary search tree T shown below. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            22,
                            [11],
                            [
                                34,
                                [29],
                                [39],
                            ],
                        ],
                        [
                            67,
                            [
                                56,
                                None,
                                [61],
                            ],
                            [
                                89,
                                [78],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'BST T',
                },
            ],
            'options': [
                'If 45 is deleted by replacing it with its in-order predecessor, the new root is 39',
                'The in-order successor of 61 in T is 78',
                'After that deletion, node 34 has exactly one child',
                'T has exactly 4 leaves',
            ],
            'answer': ['A', 'C'],
            'solution': '''The in-order predecessor of a node with a left subtree is the **maximum** of that left subtree (go left once, then right as far as possible). The in-order successor of a node **without** a right subtree is the nearest ancestor of which it lies in the left subtree.

- (A) Left subtree of 45 = {22, 11, 34, 29, 39}; its maximum is 39 (22 → 34 → 39). 39 replaces 45. **TRUE.**
- (B) 61 has no right child; walking up, 61 is in the right subtree of 56 and in the **left** subtree of 67 → successor 67 (in-order …, 56, 61, 67, 78, 89). **FALSE.**
- (C) 39 was the right child (a leaf) of 34, so after removing it 34 keeps only its left child 29. **TRUE.**
- (D) Leaves: 11, 29, 39, 61, 78 → 5 leaves. **FALSE.**

**Trap:** in (B), picking the smallest key in some right subtree (78) — the successor is found upward when the node has no right child.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        39,
                        [
                            22,
                            [11],
                            [
                                34,
                                [29],
                                None,
                            ],
                        ],
                        [
                            67,
                            [
                                56,
                                None,
                                [61],
                            ],
                            [
                                89,
                                [78],
                                None,
                            ],
                        ],
                    ],
                    'highlight': [39],
                    'caption': 'After deleting 45 (predecessor 39 promoted)',
                },
            ],
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

T = [45, [22, [11, None, None], [34, [29, None, None], [39, None, None]]],
     [67, [56, None, [61, None, None]], [89, [78, None, None], None]]]
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
def leaves(t):
    if t is None: return 0
    if t[1] is None and t[2] is None: return 1
    return leaves(t[1]) + leaves(t[2])
s = ino(T)
assert max(ino(T[1])) == 39 and s[s.index(61) + 1] == 67 and leaves(T) == 5
assert sorted(ANSWER) == ["A", "B"]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — probability of a collision',
            'text': 'Three keys are inserted into an initially empty hash table with 10 slots. Assume simple uniform hashing (each key independently hashes to each slot with probability 1/10). The probability that **at least one** collision occurs (i.e. some two keys hash to the same slot) is',
            'options': ['0.72', '0.28', '0.30', '0.03'],
            'answer': 'B',
            'solution': '''Compute the complement: the probability that all three keys land in **distinct** slots.

- Key 1: any slot → 10/10.
- Key 2: must avoid key 1's slot → 9/10.
- Key 3: must avoid two slots → 8/10.

P(no collision) = (10 · 9 · 8) / 10³ = 720 / 1000 = 0.72, so P(at least one collision) = 1 − 0.72 = **0.28** → (B).

Option analysis:

- (A) 0.72 is the probability of **no** collision.
- (C) 0.30 adds the three pairwise probabilities 3 × 1/10, double-counting the case where all three collide (it is only an upper bound).
- (D) 0.03 = 3/100 counts only one specific arrangement.

**Tip:** this is the birthday problem; with m slots, collisions become likely after about √m keys.''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

import itertools
tot = sum(1 for t in itertools.product(range(10), repeat=3) if len(set(t)) < 3)
assert tot == 280 and ANSWER == "C"
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — lower-bound variant',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def lb(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

a = [2, 4, 4, 4, 7, 9, 9, 12]
print(lb(a, 4), lb(a, 9) - lb(a, 8), lb(a, 13), lb(a, 4.5))''',
            'options': ['`1 2 8 4`', '`3 0 7 4`', '`1 0 8 4`', '`1 0 -1 3`'],
            'answer': 'C',
            'solution': '''`lb(a, x)` maintains a[0 … lo−1] < x ≤ a[hi … n−1] and returns the **first index whose value is ≥ x** (len(a) if none) — Python's `bisect_left`.

- lb(a, 4): first element ≥ 4 is a[1] → 1 (the leftmost of the duplicates).
- lb(a, 9) = 5 and lb(a, 8) = 5 (the first element ≥ 8 is also 9 at index 5) → difference 0.
- lb(a, 13): no element ≥ 13 → len(a) = 8.
- lb(a, 4.5): first element ≥ 4.5 is 7 at index 4 → 4.

Output `1 0 8 4` → (C).

- (A) computes the count of 9s (lb(a, 10) − lb(a, 9) = 2) instead of lb(9) − lb(8).
- (B) returns the last 4 (upper-bound − 1) and n − 1 for the missing key.
- (D) returns −1 for “not found”, which this half-open version never does.

**Tip:** the number of occurrences of x is lb(a, x + ε) − lb(a, x), e.g. lb(a, 4.5) − lb(a, 4) = 3 copies of 4.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

import bisect
assert OUTPUT.strip() == "1 0 8 4" and ANSWER == "A"
assert lb(a, 4.5) - lb(a, 4) == 3 == bisect.bisect_right(a, 4) - bisect.bisect_left(a, 4)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Elementary sorts — intermediate states',
            'text': 'The array [52, 17, 33, 8, 41, 25] is sorted into ascending order by standard **insertion sort**. What is the array after the first three iterations of the outer loop (i.e. after A[1], A[2], A[3] have been inserted)?',
            'options': [
                '[8, 17, 25, 52, 41, 33]',
                '[8, 17, 33, 52, 41, 25]',
                '[17, 33, 8, 41, 25, 52]',
                '[17, 33, 52, 8, 41, 25]',
            ],
            'answer': 'B',
            'solution': '''After iteration i of insertion sort, the **prefix** A[0 … i] holds the original first i + 1 elements in sorted order and the suffix is untouched.

- i = 1: insert 17 → [17, 52, 33, 8, 41, 25]
- i = 2: insert 33 → [17, 33, 52, 8, 41, 25]
- i = 3: insert 8 → [8, 17, 33, 52, 41, 25]

→ (B).

Option analysis:

- (A) is the state after three passes of **selection** sort (8, 17, 25 selected; the suffix is permuted by the swaps).
- (B) **Correct.**
- (C) is the state after one pass of **bubble** sort (the maximum 52 bubbles to the end).
- (D) is the state after only two iterations.

**Tip:** recognise the algorithm from the state: insertion sort → sorted prefix made of the *first* elements, untouched suffix; selection sort → prefix of the *smallest* elements; bubble sort → suffix of the *largest* elements.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Insertion sort, state after each iteration',
                    'row_labels': ['start', 'i = 1', 'i = 2', 'i = 3'],
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'rows': [
                        [52, 17, 33, 8, 41, 25],
                        [17, 52, 33, 8, 41, 25],
                        [17, 33, 52, 8, 41, 25],
                        [8, 17, 33, 52, 41, 25],
                    ],
                    'highlight': [
                        [3, 0],
                        [3, 1],
                        [3, 2],
                        [3, 3],
                    ],
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

A = [52, 17, 33, 8, 41, 25]
for i in range(1, 4):
    k = A[i]; j = i - 1
    while j >= 0 and A[j] > k: A[j + 1] = A[j]; j -= 1
    A[j + 1] = k
assert A == [8, 17, 33, 52, 41, 25]
S = [52, 17, 33, 8, 41, 25]
for i in range(3):
    m = min(range(i, 6), key=S.__getitem__); S[i], S[m] = S[m], S[i]
B = [52, 17, 33, 8, 41, 25]
for j in range(5):
    if B[j] > B[j + 1]: B[j], B[j + 1] = B[j + 1], B[j]
assert S == [8, 17, 25, 52, 41, 33] and B == [17, 33, 8, 41, 25, 52] and ANSWER == "C"
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'DAGs — topological orders and DFS',
            'text': 'Consider the directed acyclic graph G below. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['D', 'E'],
                        ['C', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1.6],
                        'E': [4.5, 1.6],
                        'F': [3, -0.2],
                    },
                },
            ],
            'options': [
                'Running DFS from A (neighbours in alphabetical order) and listing vertices in decreasing order of finishing time gives A, C, F, B, D, E',
                'G has exactly 6 topological orderings',
                'Deleting the edge C → D increases the number of topological orderings',
                'A is the only vertex with in-degree 0',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''- (A) DFS(A): A → B → D → E; E finishes, D finishes, B finishes; then A → C → (D done) → F; F, C, A finish. Finish order E, D, B, F, C, A; reversed: A, C, F, B, D, E. **TRUE.**
- (B) Count orderings: A is first. Constraints left: B, C before D; D before E; C before F. Place F relative to the chain: sequences of {B, C, D, E} with B, C before D before E are B C D E and C B D E (2). F must come after C: in B C D E, F can go after C in 3 gaps; in C B D E, F can go after C in 4 gaps. Total 3 + 4 = **7**, not 6. **FALSE.**
- (C) Without C → D the constraints are A first, B before D before E, C before F. The number of interleavings of chain B D E with chain C F is C(5, 2) = 10 > 7. **TRUE.**
- (D) In-degrees: A 0, B 1, C 1, D 2, E 1, F 1. **TRUE.**

**Tip:** reverse post-order of DFS is always a valid topological order; removing constraints can never decrease the count.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
def cnt(E):
    def ok(p):
        pos = {v: i for i, v in enumerate(p)}
        return all(pos[u] < pos[v] for u, v in E)
    return sum(ok(p) for p in itertools.permutations("ABCDEF"))
E = [("A","B"),("A","C"),("B","D"),("C","D"),("D","E"),("C","F")]
assert cnt(E) == 7 and cnt([e for e in E if e != ("C","D")]) == 10
adj = {v: sorted(w for u, w in E if u == v) for v in "ABCDEF"}
fin, vis = [], set()
def dfs(u):
    vis.add(u)
    for w in adj[u]:
        if w not in vis: dfs(w)
    fin.append(u)
dfs("A")
assert fin[::-1] == list("ACFBDE")
assert sorted(ANSWER) == ["A", "C", "D"]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Complexity — counting loop iterations',
            'text': 'Consider the following Python fragment with n = 16. The final value of `count` is ______.',
            'code': '''n = 16
count = 0
for i in range(1, n + 1):
    j = i
    while j <= n:
        count += 1
        j *= 2''',
            'answer': '31',
            'solution': '''For a fixed i, j takes the values i, 2i, 4i, … while ≤ n, so the inner loop runs ⌊log₂(n/i)⌋ + 1 times.

- i = 1: 1, 2, 4, 8, 16 → 5
- i = 2: 2, 4, 8, 16 → 4
- i = 3: 3, 6, 12 → 3
- i = 4: 4, 8, 16 → 3
- i = 5, 6, 7, 8: two values each (i, 2i ≤ 16) → 4 × 2 = 8
- i = 9 … 16: one value each → 8

count = 5 + 4 + 3 + 3 + 8 + 8 = **31**.

Asymptotically ∑_{i} (log₂(n/i) + 1) = n + log₂(n^{n}/n!) ≈ n + n log₂ e = Θ(n): most values of i contribute only one or two iterations, so the fragment is linear, not Θ(n log n).

**Trap:** multiplying n by the worst-case inner count (16 × 5 = 80).''',
            'verify': 'assert count == int(ANSWER)',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — class vs instance attributes',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Tally:
    count = 0
    items = []

    def __init__(self, x):
        self.count += 1
        self.items.append(x)

a = Tally(1)
b = Tally(2)
Tally.count += 5
print(a.count, b.count, Tally.count, len(a.items))''',
            'options': ['`2 2 7 2`', '`1 1 5 1`', '`1 1 5 2`', '`6 6 5 2`'],
            'answer': 'C',
            'solution': '''Attribute **lookup** on an instance checks the instance first, then the class. Attribute **assignment** through `self.` always creates/updates an attribute on the instance. Mutating a class-level object through `self` mutates the shared object.

- `self.count += 1` means `self.count = self.count + 1`: the read finds the class value 0, and the write creates an **instance** attribute count = 1. This happens separately for `a` and `b`, so a.count = b.count = 1, and `Tally.count` stays 0.
- `self.items.append(x)` reads the class list (no assignment) and mutates it: the single shared list becomes [1, 2].
- `Tally.count += 5` changes only the class attribute → 5. It does not affect `a` or `b`, whose own instance attributes now shadow it.

Output `1 1 5 2` → (C).

- (A) assumes `self.count += 1` increments the shared class attribute.
- (B) assumes each instance has its own `items` list.
- (D) assumes the instances still see the class attribute after the change.

**Trap:** immutable class attributes behave “per instance” after the first augmented assignment, while mutable ones (lists) stay shared.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '1 1 5 2' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — recursion with try/except/finally',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''def f(n):
    try:
        if n == 0:
            raise ValueError
        return n + f(n - 1)
    except ValueError:
        return 100
    finally:
        if n == 2:
            return -n

print(f(4))''',
            'answer': '5',
            'solution': '''Two rules matter: (1) an exception raised inside a *callee* that the callee handles never reaches the caller; (2) a `return` inside `finally` **overrides** whatever the `try`/`except` block was about to return (or raise).

Evaluate from the bottom of the recursion:

- f(0): raises ValueError inside its own try → its except returns 100; finally does nothing (n ≠ 2). f(0) = 100.
- f(1): returns 1 + 100 = 101.
- f(2): the try computes 2 + 101 = 103 and starts returning it, but `finally` executes `return -2`, which replaces it. f(2) = −2.
- f(3): 3 + (−2) = 1.
- f(4): 4 + 1 = **5**.

Without the `finally` clause the answer would be 4 + 3 + 2 + 1 + 100 = 110.

**Traps:**

- Thinking the ValueError from f(0) propagates up and is caught by every level (it is handled once, in f(0)).
- Ignoring the overriding `return` in `finally` (answer 110).''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — where can the k-th smallest be?',
            'text': 'A binary **min-heap** stores 31 distinct keys (a perfect binary tree of height 4; the root has depth 0). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [2, 5, 3, 9, 7, 4, 8],
                    'caption': 'Example: the top three levels of one such heap',
                },
            ],
            'options': [
                'The largest key is always at a leaf',
                'The 4th smallest key can be at depth 4',
                'The 3rd smallest key can be at depth 3',
                'The 3rd smallest key can be at depth 2',
            ],
            'answer': ['A', 'D'],
            'solution': '''In a min-heap every ancestor of a key is smaller than it. So the k-th smallest key has at most k − 1 ancestors, i.e. its depth is at most **k − 1**.

- (A) Every internal node has a child, which must be larger; the largest key has nothing larger, so it can have no children → it is a leaf (depth 4 here). **TRUE.**
- (B) Depth 4 needs 4 smaller ancestors; the 4th smallest has only 3 smaller keys. Its depth is at most 3. **FALSE.**
- (C) Depth 3 would require 3 smaller ancestors, but only 2 keys are smaller. **FALSE.**
- (D) The 3rd smallest may have the 2nd smallest as parent and the minimum as grandparent. In the example figure, the keys 2, 3, 4 lie on a root path: 4 (the 3rd smallest) is at depth 2. **TRUE.**

Consequence: finding the k-th smallest needs to inspect only the top k levels (and in fact only O(k) nodes with a priority-queue walk).

**Trap:** confusing “can be at depth d” with “must be at depth d”: the 3rd smallest can be at depth 1 *or* 2.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import heapq, random
random.seed(7)
deps3, deps4, leaf = set(), set(), True
dep = lambda i: (i + 1).bit_length() - 1
for _ in range(4000):
    a = random.sample(range(10 ** 4), 31); heapq.heapify(a); s = sorted(a)
    deps3.add(dep(a.index(s[2]))); deps4.add(dep(a.index(s[3])))
    leaf &= a.index(s[-1]) >= 15
ex = [2, 5, 3, 9, 7, 4, 8]
assert all(ex[i] < ex[c] for i in range(7) for c in (2*i+1, 2*i+2) if c < 7)
assert dep(ex.index(4)) == 2 and 2 in deps3 and max(deps3) <= 2 and max(deps4) <= 3 and leaf
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — counting swaps (Lomuto)',
            'text': 'Quicksort with the Lomuto partition below sorts A = [4, 8, 2, 7, 1, 5, 3, 6]. Every execution of a swap statement counts as one swap, **including** swaps of an element with itself. The total number of swaps is ______.',
            'code': '''def partition(A, lo, hi):
    p = A[hi]
    i = lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1

def quicksort(A, lo, hi):
    if lo < hi:
        q = partition(A, lo, hi)
        quicksort(A, lo, q - 1)
        quicksort(A, q + 1, hi)''',
            'answer': '12',
            'solution': '''Each partition call on k elements performs (number of non-pivot elements ≤ pivot) swaps in the loop plus 1 final pivot swap.

- partition(0, 7), pivot 6: elements ≤ 6 among 4, 8, 2, 7, 1, 5, 3 are 4, 2, 1, 5, 3 → 5 + 1 = 6 swaps. Result [4, 2, 1, 5, 3, **6**, 8, 7], q = 5.
- partition(0, 4) on [4, 2, 1, 5, 3], pivot 3: elements ≤ 3 are 2, 1 → 2 + 1 = 3 swaps. Result [2, 1, **3**, 5, 4], q = 2.
- partition(0, 1) on [2, 1], pivot 1: none ≤ 1 → 0 + 1 = 1 swap → [1, 2].
- partition(3, 4) on [5, 4], pivot 4: 0 + 1 = 1 swap → [4, 5].
- partition(6, 7) on [8, 7], pivot 7: 0 + 1 = 1 swap → [7, 8].
- Remaining calls have lo ≥ hi and do nothing.

Total = 6 + 3 + 1 + 1 + 1 = **12**.

Note the first loop swap (j = 0, element 4) swaps A[0] with itself — it is counted, as the question specifies.

**Trap:** forgetting the final pivot swap in the 2-element partitions, or skipping self-swaps (that would give 12 − 1 = 11, as only one self-swap occurs: A[0] ↔ A[0] in the first call).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each partition call',
                    'row_labels': ['start', '(0,7)', '(0,4)', '(0,1)', '(3,4)', '(6,7)'],
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'rows': [
                        [4, 8, 2, 7, 1, 5, 3, 6],
                        [4, 2, 1, 5, 3, 6, 8, 7],
                        [2, 1, 3, 5, 4, 6, 8, 7],
                        [1, 2, 3, 5, 4, 6, 8, 7],
                        [1, 2, 3, 4, 5, 6, 8, 7],
                        [1, 2, 3, 4, 5, 6, 7, 8],
                    ],
                    'highlight': [
                        [1, 5],
                        [2, 2],
                        [3, 0],
                        [4, 3],
                        [5, 6],
                    ],
                },
            ],
            'verify': '''
sw = [0]; selfs = [0]
def part(A, lo, hi):
    p = A[hi]; i = lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1; sw[0] += 1; selfs[0] += (i == j)
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]; sw[0] += 1
    return i + 1
def qs(A, lo, hi):
    if lo < hi:
        q = part(A, lo, hi); qs(A, lo, q - 1); qs(A, q + 1, hi)
A = [4, 8, 2, 7, 1, 5, 3, 6]; qs(A, 0, 7)
assert sw[0] == int(ANSWER) and A == sorted(A) and selfs[0] == 1
B = [4, 8, 2, 7, 1, 5, 3, 6]; quicksort(B, 0, 7); assert B == list(range(1, 9))
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Merging — optimal merge order',
            'text': 'Four sorted lists of lengths 10, 20, 30 and 40 must be merged into one sorted list by repeatedly merging **two** lists at a time. Merging lists of lengths p and q costs p + q − 1 comparisons in the worst case. The minimum possible total worst-case number of comparisons, over all merge orders, is',
            'options': ['190', '197', '200', '187'],
            'answer': 'D',
            'solution': '''Each merge costs (size of the result) − 1, and there are always exactly 3 merges, so total = (sum of all intermediate result sizes) − 3. Minimising the sum of result sizes is the *optimal merge pattern*: always merge the two **shortest** lists (Huffman's greedy rule).

- Merge 10 + 20 → 30, cost 29. Lists: 30, 30, 40.
- Merge 30 + 30 → 60, cost 59. Lists: 40, 60.
- Merge 40 + 60 → 100, cost 99.

Total = 29 + 59 + 99 = **187** → (D).

Other orders for comparison:

- Left to right ((10+20)+30)+40: 29 + 59 + 99 = 187 (here it happens to coincide).
- (10+20) then (30+40), then together: 29 + 69 + 99 = 197 → option (B).
- (40+30) first: 69 + 89 + 99 = 257.

- (A) 190 = 30 + 60 + 100 forgets the “− 1” per merge.
- (C) 200 = 2 × 100 is not a valid count for any order.

**Tip:** the final merge always costs n − 1 = 99; the choice only affects the earlier merges.''',
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

import itertools, heapq
def best(ls):
    h = list(ls); heapq.heapify(h); c = 0
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h); c += a + b - 1; heapq.heappush(h, a + b)
    return c
def brute(ls):
    if len(ls) == 1: return 0
    return min(ls[i] + ls[j] - 1 + brute([ls[k] for k in range(len(ls)) if k not in (i, j)]
               + [ls[i] + ls[j]]) for i, j in itertools.combinations(range(len(ls)), 2))
assert best([10, 20, 30, 40]) == brute([10, 20, 30, 40]) == 187 and ANSWER == "C"
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DFS — discovery and finishing times',
            'text': 'Depth-first search is run on the directed graph below starting from P; neighbours are explored in alphabetical order, and a single clock starting at 1 is incremented at every discovery and every finish (so d(P) = 1). The finishing time of vertex T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'S'],
                        ['Q', 'R'],
                        ['Q', 'T'],
                        ['R', 'P'],
                        ['S', 'R'],
                        ['S', 'T'],
                        ['T', 'U'],
                        ['U', 'S'],
                    ],
                    'pos': {
                        'P': [0, 0],
                        'Q': [2, 1.5],
                        'R': [2, -1.5],
                        'S': [4, -1.5],
                        'T': [4, 1.5],
                        'U': [6, 0],
                    },
                },
            ],
            'answer': '10',
            'solution': '''DFS(u): set d(u), recursively visit each undiscovered neighbour in order, then set f(u).

- P discovered (1). First neighbour Q.
- Q discovered (2). First neighbour R.
- R discovered (3). Its neighbour P is on the stack (grey) → back edge. R finishes (4).
- Back at Q, next neighbour T → T discovered (5).
- T → U discovered (6).
- U → S discovered (7).
- S: neighbour R is finished (black) → cross edge; neighbour T is grey → back edge. S finishes (8).
- U finishes (9). **T finishes (10).** Q finishes (11).
- Back at P: neighbour S already finished → forward edge (S is a descendant of P). P finishes (12).

f(T) = **10**.

Edge classification: tree P→Q, Q→R, Q→T, T→U, U→S; back R→P, S→T; cross S→R; forward P→S. Since back edges exist, the graph has cycles (P→Q→R→P and S→T→U→S).

**Trap:** visiting S from P before exploring Q's subtree completely — DFS finishes Q's entire subtree first, which is why S is discovered through U.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Discovery / finishing times',
                    'col_labels': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'row_labels': ['d', 'f'],
                    'rows': [
                        [1, 2, 3, 7, 5, 6],
                        [12, 11, 4, 8, 10, 9],
                    ],
                    'highlight': [
                        [1, 4],
                    ],
                },
            ],
            'verify': '''
G = {"P": "QS", "Q": "RT", "R": "P", "S": "RT", "T": "U", "U": "S"}
t = [0]; d = {}; f = {}
def dfs(u):
    t[0] += 1; d[u] = t[0]
    for w in sorted(G[u]):
        if w not in d: dfs(w)
    t[0] += 1; f[u] = t[0]
dfs("P")
assert f["T"] == int(ANSWER) and d == {"P": 1, "Q": 2, "R": 3, "T": 5, "U": 6, "S": 7}
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths — negative edge weights',
            'text': "Consider the weighted directed graph below with source S. Dijkstra's algorithm is run in its standard form: once a vertex is extracted from the priority queue its distance is never changed again. Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C'],
                    'edges': [
                        ['S', 'A', 5],
                        ['S', 'B', 2],
                        ['A', 'B', -4],
                        ['B', 'C', 3],
                        ['A', 'C', 6],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 1],
                    },
                },
            ],
            'options': [
                'The true shortest-path distance from S to C is 4',
                'Adding 4 to every edge weight and then running Dijkstra yields the correct shortest paths of the original graph',
                'The Bellman–Ford algorithm reports a negative-weight cycle in this graph',
                "Dijkstra's algorithm reports the distance of C as 5",
            ],
            'answer': ['A', 'D'],
            'solution': '''Dijkstra's correctness proof needs non-negative weights: it assumes no path through an unfinished vertex can later improve a finished one.

Dijkstra trace:

- Extract S (0): A = 5, B = 2.
- Extract B (2): C = 2 + 3 = 5.
- Extract A (5): A → B would give 1, but B is already finalised → ignored. A → C gives 11 > 5.
- Extract C (5).

True distances: B = min(2, 5 − 4) = 1 via S→A→B, and C = 1 + 3 = 4 via S→A→B→C.

- (A) **TRUE** — S→A→B→C costs 5 − 4 + 3 = 4.
- (B) **FALSE** — adding a constant penalises paths with more edges. New weights: S→A 9, A→B 0, B→C 7, S→B 6; S→B→C = 13 < S→A→B→C = 16, so the re-weighted shortest path to C is S→B→C, which is wrong for the original graph.
- (C) **FALSE** — the graph is acyclic, so it has no cycle at all, let alone a negative one; Bellman–Ford returns the correct distances.
- (D) **TRUE** — Dijkstra outputs 5 for C (and 2 for B).

**Trap:** (B) looks like a fix, but uniform shifting does not preserve shortest paths (Johnson's algorithm uses vertex potentials instead).''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import heapq
E = [("S","A",5),("S","B",2),("A","B",-4),("B","C",3),("A","C",6)]
def dij(E):
    G = {}
    for u, v, w in E: G.setdefault(u, []).append((v, w))
    d = {"S": 0}; done = set(); pq = [(0, "S")]
    while pq:
        du, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u)
        for v, w in G.get(u, []):
            if v not in done and du + w < d.get(v, 10 ** 9): d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d
def bf(E):
    d = {"S": 0, "A": 10 ** 9, "B": 10 ** 9, "C": 10 ** 9}
    for _ in range(3):
        for u, v, w in E: d[v] = min(d[v], d[u] + w)
    neg = any(d[u] + w < d[v] for u, v, w in E)
    return d, neg
true, neg = bf(E)
assert dij(E)["C"] == 5 and true["C"] == 4 and not neg
d2 = dij([(u, v, w + 4) for u, v, w in E])
assert d2["C"] == 13  # path S-B-C, original cost 5 != 4
assert sorted(ANSWER) == ["A", "B"]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BST — valid search paths',
            'text': 'The keys of a binary search tree are integers in the range 1 to 100. A search for the key 63 examines a sequence of nodes ending at 63. Which of the following could be the sequence of keys examined?',
            'options': [
                '90, 40, 80, 50, 70, 60, 63',
                '20, 75, 30, 60, 70, 58, 63',
                '10, 90, 85, 40, 88, 63',
                '50, 66, 55, 68, 63',
            ],
            'answer': 'A',
            'solution': '''As the search descends, each examined key narrows an open interval (low, high) that must contain 63: going left from key k sets high = k, going right sets low = k. Every later key must lie strictly inside the current interval.

- (A) 90 → (−∞, 90); 40 → (40, 90); 80 → (40, 80); 50 → (50, 80); 70 → (50, 70); 60 → (60, 70); 63 ✓. **Valid.**
- (B) … 60 → (60, ∞∩75) = (60, 75); 70 → (60, 70); then 58 is not in (60, 70). **Invalid.**
- (C) 10 → (10, ∞); 90 → (10, 90); 85 → (10, 85); 40 → (40, 85); 88 is not < 85. **Invalid.**
- (D) 50 → (50, ∞); 66 → (50, 66); 55 → (55, 66); 68 is not < 66. **Invalid.**

Answer (A).

Quick test: in a valid sequence, the keys greater than the target must appear in **decreasing** order and those smaller in **increasing** order. In (A): larger keys 90, 80, 70 decrease; smaller keys 40, 50, 60 increase ✓. In (B), smaller keys 20, 30, 60, 58 are not increasing ✗.

**Trap:** checking only that each step moves in the right direction relative to 63, while ignoring earlier bounds.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        90,
                        [
                            40,
                            None,
                            [
                                80,
                                [
                                    50,
                                    None,
                                    [
                                        70,
                                        [
                                            60,
                                            None,
                                            [63],
                                        ],
                                        None,
                                    ],
                                ],
                                None,
                            ],
                        ],
                        None,
                    ],
                    'highlight': [63],
                    'caption': 'Search path (A) drawn as a BST path',
                },
            ],
            'verify': '''
def ok(seq, x=63):
    lo, hi = float("-inf"), float("inf")
    for k in seq[:-1]:
        if not lo < k < hi: return False
        if x < k: hi = k
        else: lo = k
    return seq[-1] == x and lo < x < hi
opts = [[90,40,80,50,70,60,63],[20,75,30,60,70,58,63],[10,90,85,40,88,63],[50,66,55,68,63]]
assert [c for c, s in zip("ABCD", opts) if ok(s)] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — double hashing',
            'text': 'The keys 18, 41, 22, 44, 59, 32, 31, 73 are inserted in that order into an initially empty table with 13 slots (0 … 12) using double hashing: the i-th probe for key k is (h₁(k) + i · h₂(k)) mod 13, i = 0, 1, 2, …, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). The index of the slot in which 31 is stored is ______.',
            'answer': '12',
            'solution': '''Double hashing uses a key-dependent step h₂(k), so keys sharing a home slot usually follow different probe sequences.

- 18: h₁ = 5 → slot 5.
- 41: h₁ = 2 → slot 2.
- 22: h₁ = 9 → slot 9.
- 44: h₁ = 5 (taken), h₂ = 1 + 0 = 1 → 6 → slot 6.
- 59: h₁ = 7 → slot 7.
- 32: h₁ = 6 (taken), h₂ = 1 + 10 = 11 → 6 + 11 = 17 ≡ 4 → slot 4.
- 31: h₁ = 5 (taken), h₂ = 1 + 9 = 10 → 15 ≡ 2 (taken by 41) → 5 + 20 = 25 ≡ **12** → slot 12.
- 73: h₁ = 8 → slot 8.

Key 31 is stored in slot **12** after two collisions.

Since 13 is prime and 1 ≤ h₂ ≤ 11 < 13, every probe sequence visits all 13 slots, so insertion succeeds whenever a free slot exists.

**Trap:** using h₂(k) = k mod 11 (forgetting the “1 +”) gives step 9 for 31 and a different slot; h₂ must never be 0.''',
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
T = [None] * 13
for k in [18, 41, 22, 44, 59, 32, 31, 73]:
    i = 0
    while T[(k % 13 + i * (1 + k % 11)) % 13] is not None: i += 1
    T[(k % 13 + i * (1 + k % 11)) % 13] = k
assert T.index(31) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — mutability, tuples and closures',
            'text': 'Each statement below refers to a separate fresh Python 3 session. Which of the statements is/are TRUE?',
            'options': [
                'After `t = (1, [2])` and running `t[1] += [3]` inside `try: … except TypeError: pass`, `t == (1, [2, 3])` is True',
                '`sorted("bca") == "abc"` is True',
                'After `x = 5`, `f = lambda: x`, `x = 7`, the call `f()` returns 7',
                'After `m = [[0] * 2 for _ in range(2)]` and `m[0][0] = 1`, `m == [[1, 0], [1, 0]]` is True',
            ],
            'answer': ['A', 'C'],
            'solution': '''- (A) `t[1] += [3]` runs in two steps: `t[1].__iadd__([3])` mutates the list in place (succeeds), then Python tries `t[1] = <result>`, which raises TypeError because tuples do not support item assignment. The exception is swallowed, but the mutation has already happened: t == (1, [2, 3]). **TRUE.**
- (B) `sorted` always returns a **list**: ['a', 'b', 'c'] ≠ 'abc'. (`''.join(sorted("bca"))` would equal 'abc'.) **FALSE.**
- (C) The lambda looks up the global name `x` when it is **called**, by which time x is 7. **TRUE.**
- (D) The comprehension creates a **new** inner list on each iteration, so the rows are independent: m = [[1, 0], [0, 0]]. **FALSE.** (The aliasing trap applies to `[[0] * 2] * 2`.)

**Trap:** in (A), most people assume an operation that raises has no effect; augmented assignment on a mutable element of an immutable container is the classic counter-example. Similarly in (C), a closure captures *variables*, not values; to freeze the value write `lambda x=x: x`.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

m = [[0] * 2 for _ in range(2)]; m[0][0] = 1
A = m == [[1, 0], [1, 0]]
t = (1, [2])
try:
    t[1] += [3]
except TypeError:
    pass
B = t == (1, [2, 3])
x = 5
f = lambda: x
x = 7
C = f() == 7
D = sorted("bca") == "abc"
assert [c for c, v in zip("ABCD", [A, B, C, D]) if v] == sorted(ANSWER)
''',
        },
    ],
}
