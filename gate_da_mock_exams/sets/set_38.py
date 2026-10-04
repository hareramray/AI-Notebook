# Set 38 — Full-Syllabus Mock, Paper 8 (GATE-level)
SET = {
    'number': 38,
    'title': 'Full-Syllabus Mock — Paper 8',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing with negative steps',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "DATASCIENCE"
print(s[-2:2:-3], s[::4], s[3:-12:-1])''',
            'options': [
                '`CIA DSN` followed by an empty string',
                '`CIAT DSN ATAD`',
                '`CIA DSNE ATA`',
                '`CIA DSN ATAD`',
            ],
            'answer': 'D',
            'solution': '''Index the 11 characters: D0 A1 T2 A3 S4 C5 I6 E7 N8 C9 E10. A slice `s[a:b:k]` starts at a and moves by k, stopping **before** b; negative indices are first converted by adding len(s) = 11.

- `s[-2:2:-3]`: start −2 → 9. Indices 9, 6, 3 (next would be 0, which is past the stop index 2) → C, I, A → `CIA`.
- `s[::4]`: indices 0, 4, 8 → D, S, N → `DSN`.
- `s[3:-12:-1]`: −12 + 11 = −1, which for a negative step is clamped to 'before index 0', so the slice runs 3, 2, 1, 0 → A, T, A, D → `ATAD`.

Output `CIA DSN ATAD` → option **(D)**.

- (A) treats −12 as index −1 = 10, which would give an empty slice; but −12 is out of range on the left and is clamped, not wrapped.
- (B) includes the stop index 2 (T) — the stop is exclusive.
- (C) takes index 10 (E) in the second slice and drops D in the third.

**Trap:** `s[3:-1:-1]` really is empty (−1 means index 10), while `s[3:-12:-1]` is not — out-of-range bounds are clamped.''',
            'verify': "ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'CIA DSN ATAD' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': 'print((-7) // 2 + (-7) % 3 + 7 // -2 + int(-7 / 2) + (-9) % 4)',
            'answer': '-6',
            'solution': '''Python's `//` rounds **towards −∞** (floor), and `%` returns a result with the sign of the **divisor**, so that a == (a // b) * b + a % b always holds. `int()` of a float truncates **towards 0**.

- (−7) // 2 = floor(−3.5) = **−4**
- (−7) % 3 = −7 − 3·floor(−7/3) = −7 − 3·(−3) = **2**
- 7 // −2 = floor(−3.5) = **−4**
- int(−7 / 2) = int(−3.5) = **−3** (truncation)
- (−9) % 4 = −9 − 4·(−3) = **3**

Sum = −4 + 2 − 4 − 3 + 3 = **−6**.

**Trap:** C/Java semantics (truncate towards zero, remainder takes the sign of the dividend) would give −3 − 1 − 3 − 3 − 1 = −11.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — infix to postfix',
            'text': '''Operators have the usual precedence: `^` (highest, **right**-associative), then `*` and `/` (left-associative), then `+` and `-` (left-associative). The postfix form of

`a + b * (c - d) ^ e ^ f / g`

is:''',
            'options': [
                '`a b c d - e ^ f ^ * g / +`',
                '`a b c d - e f ^ ^ * g / +`',
                '`a b c d - e f ^ ^ g / * +`',
                '`a b c d - e f ^ ^ * + g /`',
            ],
            'answer': 'B',
            'solution': '''First fully parenthesise using precedence and associativity:
- `^` is right-associative: (c − d) ^ e ^ f = (c − d) ^ (e ^ f).
- `*` and `/` are left-associative: b * X / g = (b * X) / g.
- Then `+`: a + ((b * ((c − d) ^ (e ^ f))) / g).

Convert bottom-up:
- c − d → `c d -`
- e ^ f → `e f ^`; (c−d) ^ (e^f) → `c d - e f ^ ^`
- b * … → `b c d - e f ^ ^ *`
- … / g → `b c d - e f ^ ^ * g /`
- a + … → `a b c d - e f ^ ^ * g / +`

Answer **(B)**.

- (A) treats `^` as left-associative ((c−d)^e)^f.
- (C) groups b * (X / g) — wrong for left-associative `*`, `/`.
- (D) applies `+` before `/`.

**Tip (stack algorithm):** when an incoming operator has the same precedence as the stack top, pop first if it is left-associative, but push on top for right-associative `^`.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['+', '*', '^', '^'],
                    'label': 'ops',
                    'caption': 'Operator stack just after reading f',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

prec = {'+':1, '-':1, '*':2, '/':2, '^':3}
def to_post(tokens):
    out, st = [], []
    for t in tokens:
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
    while st: out.append(st.pop())
    return ' '.join(out)
assert to_post("a + b * ( c - d ) ^ e ^ f / g".split()) == "a b c d - e f ^ ^ * g / +"
assert ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Queues — elimination simulation',
            'text': 'People numbered 1 to 9 stand in a queue (1 at the front). Repeatedly: the person at the front is dequeued and enqueued at the rear **three** times, and then the person now at the front is dequeued and eliminated. This continues until one person remains. The number of the last remaining person is ______.',
            'diagrams': [
                {
                    'type': 'queue',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    'caption': 'Initial queue (front at left)',
                },
            ],
            'answer': '1',
            'solution': '''Each round moves 3 people to the back and eliminates the 4th — the Josephus problem with k = 4.

Queue states (front first), eliminated person in bold:
- [1..9] → rotate 1,2,3 → eliminate **4** → [5,6,7,8,9,1,2,3]
- rotate 5,6,7 → eliminate **8** → [9,1,2,3,5,6,7]
- rotate 9,1,2 → eliminate **3** → [5,6,7,9,1,2]
- rotate 5,6,7 → eliminate **9** → [1,2,5,6,7]
- rotate 1,2,5 → eliminate **6** → [7,1,2,5]
- rotate 7,1,2 → eliminate **5** → [7,1,2]
- rotate 7,1,2 → eliminate **7** → [1,2]
- rotate 1,2,1 → front is 2 → eliminate **2** → [1]

Survivor: **1**.

Check with the Josephus recurrence J(1) = 0, J(n) = (J(n−1) + 4) mod n (0-based): 0, 0, 1, 1, 0, 4, 1, 5, 0 → position 0 → person 1.

**Trap:** when fewer than 4 people remain the rotation wraps around more than once — with [1, 2], three rotations leave 2 at the front.''',
            'verify': '''
from collections import deque
q = deque(range(1, 10))
while len(q) > 1:
    for _ in range(3): q.append(q.popleft())
    q.popleft()
assert q[0] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — doubly linked list surgery',
            'text': 'The program below tries to move node 2 of a doubly linked list to the end. What is printed? (`walk` follows the named pointer for at most k nodes.)',
            'code': '''class N:
    def __init__(self, v):
        self.v, self.prev, self.next = v, None, None

nodes = [N(i) for i in range(1, 6)]
for a, b in zip(nodes, nodes[1:]):
    a.next, b.prev = b, a
head, tail = nodes[0], nodes[-1]

x = nodes[1]
x.prev.next = x.next
x.next.prev = x.prev
tail.next, x.prev = x, tail
tail = x

def walk(p, step, k):
    out = []
    while p and len(out) < k:
        out.append(p.v)
        p = getattr(p, step)
    return out

print(walk(head, 'next', 7), walk(tail, 'prev', 7))''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5],
                    'doubly': True,
                    'tail': 'tail',
                    'caption': 'List before the move',
                },
            ],
            'options': [
                '`[1, 3, 4, 5, 2, 3, 4] [2, 5, 4, 3, 1]`',
                '`[1, 3, 4, 5, 2] [2, 5, 4, 3, 1]`',
                '`[1, 3, 4, 5, 2, 3, 4] [2, 5, 4, 3, 2, 5, 4]`',
                '`[1, 2, 3, 4, 5] [5, 4, 3, 2, 1]`',
            ],
            'answer': 'A',
            'solution': '''Moving a node needs **four** pointer fields to be right: the neighbours' links around the hole, and both `prev` and `next` of the moved node.

- Unlink: 1.next = 3 and 3.prev = 1. Correct.
- Append: 5.next = 2 and 2.prev = 5; tail = 2.
- **Missing:** `x.next = None`. Node 2 still has `next` pointing to 3.

Forward walk from head: 1 → 3 → 4 → 5 → 2 → 3 → 4 … a cycle; `walk` stops after 7 values: [1, 3, 4, 5, 2, 3, 4].
Backward walk from tail: 2 → 5 → 4 → 3 → 1 → None (all `prev` links are correct): [2, 5, 4, 3, 1].

Answer **(A)**.

- (B) is what a correct move would print.
- (C) assumes the `prev` chain is also cyclic — 1.prev is still None.
- (D) assumes nothing changed.

**Trap:** stale pointers in the moved node silently create cycles; a forward traversal without the length guard would never terminate.''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[1, 3, 4, 5, 2, 3, 4] [2, 5, 4, 3, 1]' and ANSWER == 'B'",
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — node counting',
            'text': 'A binary tree has 20 leaves and 13 nodes that have exactly one child. The total number of nodes in the tree is:',
            'options': ['45', '53', '52', '33'],
            'answer': 'C',
            'solution': '''Let n₀, n₁, n₂ be the numbers of nodes with 0, 1, 2 children, and n the total.

- Every node except the root has exactly one parent, so the number of edges is n − 1.
- Counting edges from the parent side: edges = n₁ + 2n₂.
- So n₀ + n₁ + n₂ − 1 = n₁ + 2n₂ ⇒ **n₀ = n₂ + 1**.

Here n₀ = 20 ⇒ n₂ = 19. Total n = 20 + 13 + 19 = **52** → option **(C)**.

- (A) uses n₂ = n₁ − 1 (confusing the two counts).
- (B) uses n₂ = n₀ (forgetting the −1).
- (D) ignores the two-child nodes.

**Tip:** the number of one-child nodes n₁ does not affect n₂ at all — any number of single-child nodes can be inserted along edges without changing the leaf count.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

import random
random.seed(1)
def rand_tree(n):
    # random binary tree: children counts
    kids = {0: []}
    for v in range(1, n):
        cand = [u for u in kids if len(kids[u]) < 2]
        p = random.choice(cand); kids[p].append(v); kids[v] = []
    return kids
for _ in range(200):
    k = rand_tree(random.randint(1, 40))
    n0 = sum(1 for v in k if len(k[v]) == 0); n2 = sum(1 for v in k if len(k[v]) == 2)
    assert n0 == n2 + 1
assert 20 + 13 + (20 - 1) == 52 and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Heaps — recognising max-heaps',
            'text': 'Which of the following arrays (0-based; children of index i at 2i+1 and 2i+2) represent a binary **max**-heap?',
            'options': [
                '[92, 80, 90, 81, 70, 60, 30]',
                '[92, 88, 90, 50, 88, 89, 20, 49, 50]',
                '[92, 70, 85, 75, 60, 80, 50]',
                '[92, 85, 70, 60, 85, 40, 65, 10]',
            ],
            'answer': ['B', 'D'],
            'solution': '''Check a[parent] ≥ a[child] for every internal index i = 0 … ⌊n/2⌋ − 1. Equal keys are allowed.

- (A) i=1: 80 has child a[3] = 81. **Not a heap.**
- (B) i=0: 92 ≥ 88, 90 · i=1: 88 ≥ 50, 88 · i=2: 90 ≥ 89, 20 · i=3: 50 ≥ 49, 50. **Max-heap.**
- (C) i=1: 70 has child a[3] = 75 > 70. **Not a heap.**
- (D) i=0: 92 ≥ 85, 70 · i=1: 85 ≥ 60, 85 · i=2: 70 ≥ 40, 65 · i=3: 60 ≥ 10. **Max-heap.**

**Trap:** checking only that the array is 'roughly decreasing' or that each level's values are smaller than the previous level's — the heap property is only between a parent and its own children (in (B), 89 at depth 2 exceeds 88 at depth 1, which is fine).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [92, 88, 90, 50, 88, 89, 20, 49, 50],
                    'caption': 'Array (C) drawn as a tree',
                },
            ],
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def is_heap(a):
    return all(a[(i-1)//2] >= a[i] for i in range(1, len(a)))
opts = {'A':[92,85,70,60,85,40,65,10], 'B':[92,70,85,75,60,80,50],
        'C':[92,88,90,50,88,89,20,49,50], 'D':[92,80,90,81,70,60,30]}
assert sorted(k for k, v in opts.items() if is_heap(v)) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Complexity of a loop nest',
            'text': 'What is the time complexity of the following fragment as a function of n (n ≥ 2)?',
            'code': '''count = 0
for i in range(1, n + 1):
    j = i
    while j < n:
        j *= 2
        count += 1''',
            'run_code': False,
            'options': ['Θ(n log n)', 'Θ(n log log n)', 'Θ(log² n)', 'Θ(n)'],
            'answer': 'D',
            'solution': '''For a fixed i the inner loop doubles j from i until it reaches n, so it runs ⌈log₂(n/i)⌉ times — **not** log₂ n times.

Total ≈ ∑_{i=1}^{n} log₂(n/i) = n log₂ n − log₂(n!) .
By Stirling, log₂(n!) = n log₂ n − n log₂ e + O(log n), so the total is ≈ n log₂ e ≈ 1.44 n = **Θ(n)**.

Intuition: half of the i values (i > n/2) need ≤ 1 iteration, a quarter need ≤ 2, an eighth need ≤ 3, … → n(1/2 + 2/4 + 3/8 + …) = 2n.

Answer **(D)**.

- (A) bounds every inner loop by log n — a valid upper bound, but not tight.
- (C), (B) have no basis in the loop structure.

**Trap:** multiplying 'outer × worst inner' gives O(n log n); GATE asks for the tight Θ bound.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

def cnt(n):
    c = 0
    for i in range(1, n+1):
        j = i
        while j < n: j *= 2; c += 1
    return c
r = [cnt(2**k) / 2**k for k in range(8, 15)]
assert all(1.0 < x < 2.0 for x in r) and abs(r[-1] - r[-2]) < 0.05
assert ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Bubble sort — passes with early exit',
            'text': 'Bubble sort with early termination makes left-to-right passes over [12, 3, 25, 18, 30, 41, 7, 50]; pass p compares a[j], a[j+1] for j = 0 … n−1−p and swaps if a[j] > a[j+1]. The algorithm stops after the first pass in which **no swap** occurs. The total number of passes made (including that final pass) is ______.',
            'answer': '6',
            'solution': '''Large elements sink to the end quickly, but a small element moves **left by at most one position per pass**. The 7 at index 6 must reach index 1, which needs 5 passes; one more pass confirms sortedness.

- Pass 1: [3, 12, 18, 25, 30, 7, 41, 50]
- Pass 2: [3, 12, 18, 25, 7, 30, 41, 50]
- Pass 3: [3, 12, 18, 7, 25, 30, 41, 50]
- Pass 4: [3, 12, 7, 18, 25, 30, 41, 50]
- Pass 5: [3, 7, 12, 18, 25, 30, 41, 50]
- Pass 6: no swap → stop.

Total passes = **6**.

**Trap:** answering 5 (forgetting the confirming pass) or 2 (thinking 'the array is almost sorted, so bubble sort finishes fast' — bubble sort is adaptive only to elements that are out of place to the *left*).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6'],
                    'rows': [
                        [12, 3, 25, 18, 30, 41, 7, 50],
                        [3, 12, 18, 25, 30, 7, 41, 50],
                        [3, 12, 18, 25, 7, 30, 41, 50],
                        [3, 12, 18, 7, 25, 30, 41, 50],
                        [3, 12, 7, 18, 25, 30, 41, 50],
                        [3, 7, 12, 18, 25, 30, 41, 50],
                        [3, 7, 12, 18, 25, 30, 41, 50],
                    ],
                    'highlight': [
                        [1, 5],
                        [2, 4],
                        [3, 3],
                        [4, 2],
                        [5, 1],
                    ],
                },
            ],
            'verify': '''
a = [12,3,25,18,30,41,7,50]; p = 0
while True:
    p += 1; sw = False
    for j in range(len(a) - p):
        if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]; sw = True
    if not sw: break
assert p == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph theory — degree sequences',
            'text': 'Which of the following sequences is/are the degree sequence of some **simple** undirected graph?',
            'options': [
                '(3, 3, 3, 3, 3, 3, 3)',
                '(6, 1, 1, 1, 1, 1, 1)',
                '(5, 5, 4, 3, 2, 1)',
                '(4, 4, 3, 3, 2, 2)',
            ],
            'answer': ['B', 'D'],
            'solution': '''Necessary: the degree sum is even (handshaking). Sufficient test: **Havel–Hakimi** — remove the largest degree d, subtract 1 from the next d degrees, re-sort, repeat; the sequence is graphical iff this ends with all zeros and never goes negative.

- (A) seven vertices of odd degree → odd sum 21. **Not graphical.**
- (B) the star K_{1,6}. **Graphical.**
- (C) sum 20 (even), but: remove 5 → (4,3,2,1,0) → remove 4 → (2,1,0,−1) **negative** → not graphical. Intuition: two vertices of degree 5 in a 6-vertex simple graph are adjacent to *every* other vertex, so no vertex can have degree 1. **Not graphical.**
- (D) sum 18. (4,4,3,3,2,2) → remove 4: (3,2,2,1,2) → sort (3,2,2,2,1) → remove 3: (1,1,1,1) → remove 1: (0,1,1) → (1,1,0) → (0,0). **Graphical.**

**Trap:** stopping at the parity check — (C) has an even sum yet is impossible.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def hh(seq):
    s = sorted(seq, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d):
            s[i] -= 1
            if s[i] < 0: return False
        s.sort(reverse=True)
    return all(x == 0 for x in s)
opts = {'A':(4,4,3,3,2,2), 'B':(5,5,4,3,2,1), 'C':(3,)*7, 'D':(6,1,1,1,1,1,1)}
assert sorted(k for k, v in opts.items() if hh(v)) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — sort stability with reverse=True',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''words = ["kiwi", "fig", "plum", "date", "pear", "lime", "apple"]
r1 = sorted(words, key=len, reverse=True)
r2 = sorted(words, key=len)[::-1]
print(r1[:3], r2[:3])''',
            'options': [
                "`['apple', 'kiwi', 'plum'] ['apple', 'kiwi', 'plum']`",
                "`['apple', 'lime', 'pear'] ['apple', 'lime', 'pear']`",
                "`['apple', 'kiwi', 'plum'] ['apple', 'lime', 'pear']`",
                "`['apple', 'plum', 'pear'] ['apple', 'lime', 'pear']`",
            ],
            'answer': 'C',
            'solution': '''Python's `sorted` is **stable**, and `reverse=True` is implemented so that stability is preserved: elements with equal keys keep their *original* relative order. Reversing a sorted list afterwards, however, flips the order of equal keys.

Lengths: kiwi 4, fig 3, plum 4, date 4, pear 4, lime 4, apple 5.

- r1: descending by length, ties in input order → apple, kiwi, plum, date, pear, lime, fig → first three `['apple', 'kiwi', 'plum']`.
- r2: ascending sort gives fig, kiwi, plum, date, pear, lime, apple; reversing it gives apple, lime, pear, date, plum, kiwi, fig → `['apple', 'lime', 'pear']`.

Answer **(C)**.

- (A) assumes `[::-1]` preserves tie order.
- (B) assumes `reverse=True` is the same as sorting and then reversing.
- (D) mixes the two orders arbitrarily.

**Tip:** to sort descending by one key while keeping stability, use `reverse=True` (or a negated key), never `[::-1]` after an ascending sort.''',
            'verify': 'ANSWER = {\'A\': \'C\', \'C\': \'A\'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == "[\'apple\', \'kiwi\', \'plum\'] [\'apple\', \'lime\', \'pear\']" and ANSWER == \'A\'',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — counting inversions',
            'text': 'The following function counts inversions (pairs i < j with a[i] > a[j]) while merge-sorting. The value printed is ______.',
            'code': '''def sort_count(a):
    if len(a) <= 1:
        return a, 0
    m = len(a) // 2
    L, x = sort_count(a[:m])
    R, y = sort_count(a[m:])
    out, i, j, c = [], 0, 0, x + y
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            c += len(L) - i
    return out + L[i:] + R[j:], c

print(sort_count([8, 3, 9, 1, 6, 2, 7, 4])[1])''',
            'answer': '16',
            'solution': '''When R[j] is output before the remaining L[i..], it is smaller than **all** len(L) − i of them (L is sorted), so each such step adds len(L) − i inversions that cross the two halves. Inversions inside the halves are counted recursively.

Level 1 (pairs): [8,3] → 1, [9,1] → 1, [6,2] → 1, [7,4] → 1 → 4.
Level 2:
- [3,8] + [1,9]: 1 beats 3 and 8 → +2 → [1,3,8,9].
- [2,6] + [4,7]: 4 beats 6 → +1 → [2,4,6,7].
Level 3: [1,3,8,9] + [2,4,6,7]:
- 2 beats 3, 8, 9 → +3; 4 beats 8, 9 → +2; 6 → +2; 7 → +2 → +9.

Total = 4 + 3 + 9 = **16**.

Brute-force check: larger elements to the left of each element: 3:1, 9:0, 1:3, 6:2, 2:4, 7:2, 4:4 → 1+0+3+2+4+2+4 = 16.

**Trap:** adding 1 per out-of-order merge step instead of len(L) − i, or using `<` instead of `<=` (which would also count equal pairs if duplicates were present).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Cross inversions found at each merge',
                    'col_labels': ['merge', 'result', 'added'],
                    'row_labels': ['L1', 'L1', 'L1', 'L1', 'L2', 'L2', 'L3'],
                    'rows': [
                        ['8 | 3', '3 8', 1],
                        ['9 | 1', '1 9', 1],
                        ['6 | 2', '2 6', 1],
                        ['7 | 4', '4 7', 1],
                        ['3 8 | 1 9', '1 3 8 9', 2],
                        ['2 6 | 4 7', '2 4 6 7', 1],
                        ['1 3 8 9 | 2 4 6 7', '1 2 3 4 6 7 8 9', 9],
                    ],
                },
            ],
            'verify': '''
a = [8,3,9,1,6,2,7,4]
assert sum(1 for i in range(8) for j in range(i+1, 8) if a[i] > a[j]) == int(ANSWER)
assert OUTPUT.strip() == ANSWER
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort — Hoare partition',
            'text': '''The Hoare partition scheme below is applied once to A = [24, 31, 8, 47, 15, 24, 3, 52, 19] with lo = 0, hi = 8.

pivot = A[lo]; i = lo − 1; j = hi + 1
repeat forever:
- do j = j − 1 while A[j] > pivot
- do i = i + 1 while A[i] < pivot
- if i < j: swap A[i], A[j]  else: return j

Which of the following statements is/are TRUE?''',
            'options': [
                'Exactly 3 swaps are performed',
                'After the call, A[4] = 24, i.e. the pivot is in its final sorted position',
                'After the call, every element of A[0..4] is ≤ every element of A[5..8]',
                'The value returned is 4',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Hoare's scheme moves two pointers towards each other and swaps out-of-place pairs. It guarantees A[lo..j] ≤ pivot ≤ A[j+1..hi] but does **not** put the pivot in its final place. Pivot = 24.

- Round 1: j stops at 8 (19 ≤ 24); i stops at 0 (24 is not < 24). Swap → [19, 31, 8, 47, 15, 24, 3, 52, 24].
- Round 2: j: 7 (52 > 24) → 6 (3) stop; i: 1 (31) stop. Swap → [19, 3, 8, 47, 15, 24, 31, 52, 24].
- Round 3: j: 5 (24, not > 24) stop; i: 2 (8 < 24), 3 (47) stop. Swap → [19, 3, 8, 24, 15, 47, 31, 52, 24].
- Round 4: j: 4 (15) stop; i: 4 (15 < 24), 5 (47) stop. i = 5 ≥ j = 4 → return 4.

- (A) Three swaps. **True.**
- (B) A[4] = 15; the original pivot ended at index 8. **False.**
- (C) A[0..4] = {19, 3, 8, 24, 15} ≤ 24 ≤ A[5..8] = {47, 31, 52, 24}. **True.**
- (D) Returns 4. **True.**

**Trap:** applying Lomuto intuition ('the pivot lands at the returned index'). With Hoare, the next recursive calls are on [lo..j] and [j+1..hi] — the pivot is not excluded.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each swap (pivot 24)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
                    'row_labels': ['start', 'swap 1', 'swap 2', 'swap 3'],
                    'rows': [
                        [24, 31, 8, 47, 15, 24, 3, 52, 19],
                        [19, 31, 8, 47, 15, 24, 3, 52, 24],
                        [19, 3, 8, 47, 15, 24, 31, 52, 24],
                        [19, 3, 8, 24, 15, 47, 31, 52, 24],
                    ],
                    'highlight': [
                        [3, 4],
                    ],
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A = [24,31,8,47,15,24,3,52,19]
p = A[0]; i, j, sw = -1, 9, 0
while True:
    j -= 1
    while A[j] > p: j -= 1
    i += 1
    while A[i] < p: i += 1
    if i < j: A[i], A[j] = A[j], A[i]; sw += 1
    else: break
truth = {'A': j == 4, 'B': sw == 3, 'C': A[4] == 24,
         'D': max(A[:5]) <= min(A[5:])}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recurrences — exact evaluation',
            'text': 'Let T(1) = 1 and T(n) = 3T(n/3) + n for n a power of 3, n > 1. The value of T(81) is ______.',
            'answer': '405',
            'solution': '''Unroll the recurrence (recursion-tree method). With n = 3^{k}:
T(n) = 3T(n/3) + n = 9T(n/9) + n + n = … = 3^{k}·T(1) + k·n = n + n log₃ n.

Each of the k levels of the recursion tree contributes exactly n (3^{i} subproblems of size n/3^{i}), and the 3^{k} = n leaves contribute T(1) = 1 each.

For n = 81 = 3⁴: T(81) = 81 + 81 × 4 = **405**.

Step-by-step check:
- T(3) = 3·1 + 3 = 6
- T(9) = 3·6 + 9 = 27
- T(27) = 3·27 + 27 = 108
- T(81) = 3·108 + 81 = 405 ✓

Asymptotically this is case 2 of the master theorem (a = b = 3, f(n) = Θ(n)) → Θ(n log n), the same shape as merge sort's recurrence.

**Trap:** forgetting the leaf contribution n·T(1) and answering 324 = n log₃ n.''',
            'verify': '''
def T(n): return 1 if n == 1 else 3*T(n//3) + n
assert T(81) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BST — successive deletions',
            'text': 'The keys 47, 23, 71, 12, 35, 58, 84, 29, 41, 63, 90, 38 are inserted in that order into an empty BST (shown). Then 23, 71 and 47 are deleted, in that order; a node with two children is replaced by its **in-order successor**, and a node with at most one child is spliced out. What is the pre-order traversal of the final tree?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        47,
                        [
                            23,
                            [12],
                            [
                                35,
                                [29],
                                [
                                    41,
                                    [38],
                                    None,
                                ],
                            ],
                        ],
                        [
                            71,
                            [
                                58,
                                None,
                                [63],
                            ],
                            [
                                84,
                                None,
                                [90],
                            ],
                        ],
                    ],
                    'caption': 'Figure: BST before deletions',
                },
            ],
            'options': [
                '58, 29, 12, 35, 41, 38, 84, 63, 90',
                '41, 12, 35, 29, 38, 63, 58, 84, 90',
                '58, 29, 12, 35, 38, 41, 84, 63, 90',
                '58, 35, 12, 29, 41, 38, 84, 63, 90',
            ],
            'answer': 'A',
            'solution': '''In-order successor of a node with two children = minimum of its right subtree; that node has no left child, so removing it from its old place is a simple splice.

- Delete 23 (children 12, 35): successor = min of {35, 29, 41, 38} = 29. 29 replaces 23; 29 was a leaf → removed. Left subtree becomes 29 [12, 35 [–, 41 [38, –]]].
- Delete 71 (children 58, 84): successor = 84 (84 has no left child). 84 replaces 71 and 84's right child 90 moves up. Right subtree: 84 [58 [–, 63], 90].
- Delete 47 (root): successor = min of right subtree = 58. 58 replaces 47; 58's right child 63 takes its place. Right subtree: 84 [63, 90].

Final tree: 58 [29 [12, 35 [–, 41 [38, –]]], 84 [63, 90]].
Pre-order: 58, 29, 12, 35, 41, 38, 84, 63, 90 → option **(A)**.

- (B) uses the in-order **predecessor** instead.
- (C) lists 38 before 41, but 38 is 41's left child, so 41 comes first in pre-order.
- (D) puts 35 at 29's position — 35 is not the successor of 23.

**Trap:** when deleting the root last, use the tree *after* the earlier deletions — 58's right child is now 63.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        58,
                        [
                            29,
                            [12],
                            [
                                35,
                                None,
                                [
                                    41,
                                    [38],
                                    None,
                                ],
                            ],
                        ],
                        [
                            84,
                            [63],
                            [90],
                        ],
                    ],
                    'caption': 'Final BST',
                },
            ],
            'verify': '''
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
        m = t[2]
        while m[1]: m = m[1]
        t[0] = m[0]; t[2] = dele(t[2], m[0])
    return t
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
T = None
for k in [47,23,71,12,35,58,84,29,41,63,90,38]: T = ins(T, k)
for k in [23, 71, 47]: T = dele(T, k)
assert pre(T) == [58,29,12,35,41,38,84,63,90] and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Hashing — limits of quadratic probing',
            'text': 'Keys 14, 21, 28, 35 are inserted in that order into an empty table of size 7 (slots 0–6) using quadratic probing h(k, i) = (k mod 7 + i²) mod 7, i = 0, 1, 2, …  Next, key 42 is to be inserted. Which of the following statements is/are TRUE?',
            'options': [
                'If double hashing h(k, i) = (k mod 7 + i·(5 − k mod 5)) mod 7 had been used for all five keys, every key would have been placed',
                'If linear probing (step +1) had been used for all five keys, 42 would be stored in slot 3',
                'Key 42 cannot be placed by this probe sequence, even though 3 slots are empty',
                'Key 35 is stored in slot 2',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''All five keys are multiples of 7, so all have home slot 0. Quadratic probing visits 0 + i² mod 7 for i = 0, 1, 2, …: the squares mod 7 are 0, 1, 4, 2, 2, 4, 1, 0, … — only the **4** quadratic residues {0, 1, 2, 4}.

- 14 → slot 0; 21 → 0, **1**; 28 → 0, 1, **4**; 35 → 0, 1, 4, 9 mod 7 = **2**.

- (A) h₂(k) = 5 − (k mod 5) ∈ {1, …, 5} is never 0 and 7 is prime, so each probe sequence is a permutation of all 7 slots; with only 5 keys every insertion succeeds. **True.**
- (B) With linear probing: 14 → 0, 21 → 1, 28 → 2, 35 → 3, 42 → **4**, not 3. **False.**
- (C) 42 can only probe {0, 1, 2, 4}, all full; slots 3, 5, 6 are empty but unreachable. **True.** (Quadratic probing is guaranteed to succeed only when the load factor is ≤ 1/2 for prime m.)
- (D) 35 lands in slot 2. **True.**

**Trap:** assuming 'table not full ⇒ insertion succeeds' for every open-addressing scheme.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: 14,
                        1: 21,
                        2: 35,
                        4: 28,
                    },
                    'caption': 'After four insertions; 42 can only probe slots 0, 1, 4, 2',
                },
            ],
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(seq, probe, m=7):
    T = [None]*m; ok = True
    for k in seq:
        for i in range(50):
            s = probe(k, i) % m
            if T[s] is None: T[s] = k; break
        else:
            ok = False
    return T, ok
quad = lambda k, i: k % 7 + i*i
lin = lambda k, i: k % 7 + i
dbl = lambda k, i: k % 7 + i*(5 - k % 5)
T4, _ = ins([14,21,28,35], quad)
_, ok5 = ins([14,21,28,35,42], quad)
TL, _ = ins([14,21,28,35,42], lin)
_, okd = ins([14,21,28,35,42], dbl)
truth = {'A': T4.index(35) == 2, 'B': (not ok5) and T4.count(None) == 3,
         'C': TL.index(42) == 3, 'D': okd}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Dijkstra with a negative edge',
            'text': "Dijkstra's algorithm is run from S on the directed graph shown, which has one negative edge. A vertex is **finalised** when it is extracted from the priority queue, and relaxations into finalised vertices are ignored. Let d(C), d(T) be the distances it reports and δ(T) the true shortest distance from S to T. Then (d(C), d(T), δ(T)) is:",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'T'],
                    'edges': [
                        ['S', 'A', 5],
                        ['S', 'B', 2],
                        ['A', 'B', -4],
                        ['B', 'C', 4],
                        ['C', 'T', 1],
                        ['A', 'T', 6],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, -0.2],
                        'T': [4.5, 2.2],
                    },
                },
            ],
            'options': ['(5, 6, 6)', '(6, 7, 6)', '(6, 7, 7)', '(6, 11, 6)'],
            'answer': 'B',
            'solution': '''Dijkstra's correctness proof assumes that a vertex's distance can only grow along a path; a negative edge breaks this.

Trace:
- Extract S (0): A = 5, B = 2.
- Extract B (2) — **finalised at 2**: C = 2 + 4 = 6.
- Extract A (5): A→B would give 1, but B is finalised → ignored; T = 5 + 6 = 11.
- Extract C (6): T = min(11, 7) = 7.
- Extract T (7).
Reported d(C) = 6, d(T) = 7.

True distances (e.g. Bellman–Ford): B = 5 − 4 = 1, C = 1 + 4 = 5, T = 5 + 1 = **6** via S→A→B→C→T.

Answer **(B)** (6, 7, 6).

- (A) gives the true values for C and T — not what this Dijkstra reports.
- (C) assumes Dijkstra is still correct.
- (D) forgets the relaxation of C→T.

**Trap:** adding a constant to all edge weights to remove negatives does not work either — it penalises paths with more edges.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

import heapq, math
E = [('S','A',5),('S','B',2),('A','B',-4),('B','C',4),('C','T',1),('A','T',6)]
G = {v: [] for v in 'SABCT'}
for u, v, w in E: G[u].append((v, w))
d = {v: math.inf for v in G}; d['S'] = 0; fin = set(); pq = [(0, 'S')]
while pq:
    du, u = heapq.heappop(pq)
    if u in fin: continue
    fin.add(u)
    for v, w in G[u]:
        if v not in fin and du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
bf = {v: math.inf for v in G}; bf['S'] = 0
for _ in range(4):
    for u, v, w in E:
        if bf[u] + w < bf[v]: bf[v] = bf[u] + w
assert (d['C'], d['T'], bf['T']) == (6, 7, 6) and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BFS — counting shortest paths in a grid',
            'text': 'A robot moves on the 5 × 6 grid shown, one step at a time up, down, left or right, never entering a blocked cell (#). The number of distinct shortest paths from the top-left cell (row 0, column 0) to the bottom-right cell (row 4, column 5) is ______.',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Grid (# = blocked)',
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'row_labels': ['0', '1', '2', '3', '4'],
                    'rows': [
                        ['S', '', '', '', '', ''],
                        ['', '#', '', '', '#', ''],
                        ['', '', '#', '', '', ''],
                        ['', '', '', '', '#', ''],
                        ['', '', '', '', '', 'T'],
                    ],
                    'highlight': [
                        [1, 1],
                        [1, 4],
                        [2, 2],
                        [3, 4],
                    ],
                },
            ],
            'answer': '12',
            'solution': '''BFS from S gives every cell its distance; the number of shortest paths to a cell is the sum of the counts of its neighbours that are exactly one step closer. Here a monotone (right/down only) path of length 4 + 5 = 9 exists, so every shortest path is monotone and the count obeys N(r, c) = N(r−1, c) + N(r, c−1) (0 for blocked cells).

Row by row:
- row 0: 1, 1, 1, 1, 1, 1
- row 1: 1, #, 1, 2, #, 1
- row 2: 1, 1, #, 2, 2, 3
- row 3: 1, 2, 2, 4, #, 3
- row 4: 1, 3, 5, 9, 9, **12**

e.g. N(4,3) = N(3,3) + N(4,2) = 4 + 5 = 9, N(4,5) = N(3,5) + N(4,4) = 3 + 9 = 12.

Answer: **12** shortest paths, each of length 9.

**Trap:** using the unobstructed count C(9, 4) = 126, or subtracting paths through each blocked cell separately (inclusion–exclusion errors). The DP table is quicker and safer.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Number of shortest paths to each cell',
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'row_labels': ['0', '1', '2', '3', '4'],
                    'rows': [
                        [1, 1, 1, 1, 1, 1],
                        [1, '#', 1, 2, '#', 1],
                        [1, 1, '#', 2, 2, 3],
                        [1, 2, 2, 4, '#', 3],
                        [1, 3, 5, 9, 9, 12],
                    ],
                    'highlight': [
                        [4, 5],
                    ],
                },
            ],
            'verify': '''
from collections import deque
R, C = 5, 6; B = {(1,1), (1,4), (2,2), (3,4)}
d = {(0,0): 0}; n = {(0,0): 1}; q = deque([(0,0)])
while q:
    u = q.popleft()
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        v = (u[0]+dr, u[1]+dc)
        if 0 <= v[0] < R and 0 <= v[1] < C and v not in B:
            if v not in d: d[v] = d[u] + 1; n[v] = n[u]; q.append(v)
            elif d[v] == d[u] + 1: n[v] += n[u]
assert d[(4,5)] == 9 and n[(4,5)] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — shallow copy, deep copy and aliasing',
            'text': 'Consider the following Python code. Which of the following statements is/are TRUE after it runs?',
            'code': '''import copy
a = [[1, 2], [3, 4]]
b = a[:]
c = copy.deepcopy(a)
d = a
b[0].append(9)
b[1] = [7]
d.append([5])
c[0][0] = 0''',
            'options': [
                '`a == [[1, 2, 9], [3, 4], [5]]`',
                '`c[0] == [0, 2, 9]`',
                '`a[0] is b[0]`',
                '`b == [[1, 2, 9], [7]]`',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''- `b = a[:]` is a **shallow** copy: a new outer list whose elements are the *same* inner list objects.
- `c = copy.deepcopy(a)` copies the inner lists too.
- `d = a` is just another name for the same object.

Effects:
- `b[0].append(9)` mutates the shared inner list → visible through a, b, d (not c).
- `b[1] = [7]` rebinds slot 1 of **b's** outer list only.
- `d.append([5])` appends to the outer list of a (= d), not to b.
- `c[0][0] = 0` changes only c's private inner list.

Final values: a = d = [[1, 2, 9], [3, 4], [5]], b = [[1, 2, 9], [7]], c = [[0, 2], [3, 4]].

- (A) **True.**
- (B) c was copied *before* 9 was appended and does not share inner lists → c[0] = [0, 2]. **False.**
- (C) Shallow copy shares inner objects. **True.**
- (D) **True.**

**Trap:** thinking `b[1] = [7]` affects a (assignment to an index of the copy only touches the copy), or that `d.append` affects b.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

truth = {'A': a == [[1,2,9],[3,4],[5]], 'B': b == [[1,2,9],[7]],
         'C': c[0] == [0,2,9], 'D': a[0] is b[0]}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DAGs — counting topological orders',
            'text': 'The number of distinct topological orderings of the directed acyclic graph shown is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'C'],
                        ['B', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['D', 'E'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [1.8, 2],
                        'D': [1.8, 0],
                        'E': [3.6, 2],
                        'F': [3.6, 0],
                        'G': [5.4, 1],
                    },
                },
            ],
            'answer': '14',
            'solution': '''G must be last (it depends on E and F, which depend on everything else). E needs C and D; C needs A and B; D needs B; F needs D. Count orderings of the first six vertices by case analysis on where F goes.

Step 1 — orderings of {A, B, C, D, E} (ignoring F): A and B before C; B before D; C and D before E. So E is 5th; the first four are a topological order of A→C, B→C, B→D: B first then A, C, D with A before C → (B,A,C,D), (B,A,D,C), (B,D,A,C); or A first: (A,B,C,D), (A,B,D,C). That is **5** orders.

Step 2 — insert F. F must come after D (and before G); it is independent of A, C, E. For each of the 5 orders, F can go in any gap after D among the six positions:
- D in position 4 (orders B,A,C,D and A,B,C,D): gaps after D → 2 choices each (before E or after E) → 4.
- D in position 3 (B,A,D,C and A,B,D,C): 3 choices each → 6.
- D in position 2 (B,D,A,C): 4 choices → 4.
Total = 4 + 6 + 4 = **14**.

**Trap:** multiplying independent-looking counts (e.g. 5 × 3) — the number of slots for F depends on where D sits in each ordering.''',
            'verify': '''
from itertools import permutations
E = [('A','C'),('B','C'),('B','D'),('C','E'),('D','E'),('D','F'),('E','G'),('F','G')]
cnt = 0
for p in permutations('ABCDEFG'):
    pos = {v: i for i, v in enumerate(p)}
    if all(pos[u] < pos[v] for u, v in E): cnt += 1
assert cnt == int(ANSWER)
''',
        },
    ],
}
