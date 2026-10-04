# Set 48 — Challenge Mock, Paper 3 (Hard)
SET = {
    'number': 48,
    'title': 'Challenge Mock — Paper 3',
    'difficulty': 'Hard',
    'focus': 'hardest, multi-concept, trap-heavy 2-mark questions',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — chained comparisons',
            'text': 'Consider the following Python program. What is printed?',
            'code': 'print(1 < 3 > 2 == 2 < 5, (1 < 3) > 2, [] == [] is not [])',
            'options': ['`True False False`', '`True True True`', '`False False True`', '`True False True`'],
            'answer': 'D',
            'solution': '''Python **chains** comparison operators: `a op1 b op2 c` means `(a op1 b) and (b op2 c)`, with b evaluated once. `is`, `is not`, `==`, `<` … all belong to the same chaining family. Parentheses break the chain.

- `1 < 3 > 2 == 2 < 5` = (1<3) and (3>2) and (2==2) and (2<5) = **True**.
- `(1 < 3) > 2`: the parenthesised part is `True`, i.e. 1 as an int; `1 > 2` is **False**.
- `[] == [] is not []` = ([] == []) and ([] is not []). The middle list is shared by both comparisons, but the third literal is a *new* list object, so `is not` is True; the equality is True → **True**.

Output `True False True` → option **(D)**.

- (A) assumes `[] is not []` is False, i.e. that two empty-list literals are the same object — every `[]` creates a new list.
- (B) evaluates `(1 < 3) > 2` as if it were chained.
- (C) evaluates the first chain left-to-right as ((1<3) > 2) …, like C would.

**Trap:** in C/Java, `1 < 3 > 2` would compare a boolean with 2. Python's chaining is purely syntactic sugar for `and`.''',
            'verify': "ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'True False True' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — generators and iterator exhaustion',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''g = (x * x for x in range(6))
s1 = sum(x for x in g if x % 2)
s2 = sum(g)
it = iter(range(11))
pairs = list(zip(it, it))
rest = sum(it)
print(s1 + s2 + len(pairs) + rest)''',
            'answer': '40',
            'solution': '''Generators and iterators are **single-pass**; and `zip` pulls from its arguments left to right, stopping as soon as *any* argument is exhausted.

- `g` yields 0, 1, 4, 9, 16, 25. The first `sum` consumes it completely, keeping odd squares 1 + 9 + 25 → s1 = **35**.
- `sum(g)` on the exhausted generator → s2 = **0**.
- `zip(it, it)` takes two consecutive items per tuple from the *same* iterator: (0,1), (2,3), (4,5), (6,7), (8,9) → 5 pairs. For the 6th tuple zip calls `next(it)` for the first argument and gets **10**, then the second `next` raises `StopIteration`, so the tuple is discarded — and 10 is **lost**.
- `rest = sum(it)` → 0.

Printed: 35 + 0 + 5 + 0 = **40**.

**Trap:** expecting rest = 10 (answer 50), or expecting s2 = 55 (re-iterating the generator). Use `itertools.zip_longest` or slicing when leftovers matter.''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — monotonic stack (next greater element)',
            'text': 'The function below is called on a = [6, 2, 5, 1, 4, 8, 3, 7] (shown). Which of the following statements is/are TRUE?',
            'code': '''def nge(a):
    res, st, pops = [-1] * len(a), [], 0
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
            pops += 1
        st.append(i)
    return res, pops, st''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [6, 2, 5, 1, 4, 8, 3, 7],
                    'label': 'a',
                },
            ],
            'options': [
                'At some moment the stack holds 4 indices',
                '`pops == 6`',
                'When the function returns, the stack holds the indices of the values 8 and 7 (bottom to top)',
                '`res == [8, 5, 8, 4, 8, -1, 7, -1]`',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''The stack keeps indices whose values are **strictly decreasing** from bottom to top; a new value pops every smaller value and becomes their next greater element. Each index is pushed once and popped at most once → O(n).

Trace (stack shown as values):
- 6 → [6]
- 2 → [6, 2]
- 5 pops 2 (res=5) → [6, 5]
- 1 → [6, 5, 1]  (size 3)
- 4 pops 1 (res=4) → [6, 5, 4]  (size 3)
- 8 pops 4, 5, 6 (res=8 each) → [8]
- 3 → [8, 3]
- 7 pops 3 (res=7) → [8, 7]

- (A) The maximum size is 3. **False.**
- (B) pops = 1 + 1 + 3 + 1 = 6 (= 8 pushes − 2 left). **True.**
- (C) Final stack = indices 5, 7 = values 8, 7. **True.**
- (D) res = [8, 5, 8, 4, 8, −1, 7, −1]. **True.**

**Trap:** in (A), 4 does not stack on top of 1 — it pops 1 first, so the size stays 3.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

r, p, s = nge([6,2,5,1,4,8,3,7])
a = [6,2,5,1,4,8,3,7]
st, mx = [], 0
for i, x in enumerate(a):
    while st and a[st[-1]] < x: st.pop()
    st.append(i); mx = max(mx, len(st))
truth = {'A': r == [8,5,8,4,8,-1,7,-1], 'B': p == 6, 'C': mx >= 4,
         'D': [a[i] for i in s] == [8, 7]}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Deques — sliding-window maximum',
            'text': 'The program computes the maximum of every window of size 3 using a deque of indices. The value printed (the number of removals from the **back** of the deque) is ______.',
            'code': '''from collections import deque

a = [4, 2, 12, 3, 8, 6, 1, 9, 5, 7]
k, dq, back, out = 3, deque(), 0, []
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:
        dq.pop()
        back += 1
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        out.append(a[dq[0]])
print(back)''',
            'answer': '7',
            'solution': '''The deque holds indices whose values are decreasing from front to back. An incoming value removes from the back every value ≤ it (they can never be a future maximum); the front is dropped when it leaves the window.

Trace (deque as values):
- 4 → [4];  2 → [4, 2]
- 12: pops 2, 4 (**2**) → [12]; max 12
- 3 → [12, 3]; max 12
- 8: pops 3 (**3**) → [12, 8]; max 12
- 6 → [12, 8, 6]; 12 (index 2) leaves the window (front pop) → [8, 6]; max 8
- 1 → [8, 6, 1]; max 8
- 9: pops 1, 6, 8 (**6**) → [9]; max 9
- 5 → [9, 5]; max 9
- 7: pops 5 (**7**) → [9, 7]; max 9

Back removals = **7**; window maxima = 12, 12, 12, 8, 8, 9, 9, 9.

**Trap:** counting the single front removal (12 leaving the window) as well, which gives 8. The total of all removals is at most n, which is why the algorithm is O(n).''',
            'verify': 'assert OUTPUT.strip() == ANSWER and out == [12,12,12,8,8,9,9,9]',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — split, reverse and interleave',
            'text': '`reorder` is applied to the list 1 → 2 → … → 7 (shown). Reading the returned list from its head, the sequence of values is:',
            'code': '''def reorder(h):
    slow, fast = h, h.nxt
    while fast and fast.nxt:
        slow, fast = slow.nxt, fast.nxt.nxt
    second, slow.nxt = slow.nxt, None
    prev = None
    while second:
        second.nxt, prev, second = prev, second, second.nxt
    first = h
    while prev:
        a, b = first.nxt, prev.nxt
        first.nxt, prev.nxt = prev, a
        first, prev = a, b
    return h''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7],
                },
            ],
            'options': [
                '`[1, 6, 2, 5, 3, 4, 7]`',
                '`[1, 7, 2, 6, 3, 5]`',
                '`[1, 5, 2, 6, 3, 7, 4]`',
                '`[1, 7, 2, 6, 3, 5, 4]`',
            ],
            'answer': 'D',
            'solution': '''Three classic phases: (1) find the middle with slow/fast pointers, (2) cut and reverse the second half, (3) interleave.

- Phase 1 (fast starts at h.nxt): slow/fast = (1,2) → (2,4) → (3,6); fast.nxt = 7 → (4, None) stop. slow = **4**.
- Cut after 4: first half 1→2→3→4, second half 5→6→7.
- Phase 2: reverse the second half → 7→6→5 (prev = 7).
- Phase 3: 1→7, 7→2; 2→6, 6→3; 3→5, 5→4; prev becomes None → stop. 4's next is already None.

Result 1, 7, 2, 6, 3, 5, 4 → option **(D)** (pattern L₀, Lₙ, L₁, Lₙ₋₁, …).

- (A) cuts after 3 (using fast = h), leaving 4 in the second half.
- (B) loses the middle node 4 (would happen if the cut were made *before* the middle).
- (C) forgets to reverse the second half.

**Trap:** the multiple-assignment lines evaluate the entire right side first; writing them as sequential statements in the same order would lose pointers.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def build(n):
    head = None
    for v in range(n, 0, -1): head = Node(v, head)
    return head
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out
assert show(reorder(build(7))) == [1,7,2,6,3,5,4] and ANSWER == 'A'
assert show(reorder(build(6))) == [1,6,2,5,3,4]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Heaps — where can the k-th smallest be?',
            'text': 'A binary min-heap stores 1023 distinct keys in an array A[0..1022] (children of i at 2i+1 and 2i+2). Considering all possible such heaps, the number of different indices at which the **4th smallest** key can appear is ______.',
            'answer': '14',
            'solution': '''Every ancestor of a node holds a smaller key. So if the 4th smallest key sits at depth d (root depth 0), all its d ancestors must be among the 3 smaller keys → **d ≤ 3**. It cannot be the root (d = 0) because the root holds the minimum.

Conversely every node at depth 1, 2 or 3 is possible: put the 4th smallest there, place smaller keys on its ancestors (at most 3 needed) and any remaining smaller keys as other children of the root, then fill the rest with larger keys in heap order. With 1023 = 2¹⁰ − 1 keys all of depths 1–3 exist.

Count = 2 + 4 + 8 = **14** indices (A[1] … A[14]).

**Trap:** answering 15 (including the root) or 8 (only the deepest level 3, thinking the 4th smallest must be 'three levels down'). In general the k-th smallest (k ≥ 2) can be at any depth from 1 to k − 1, i.e. at 2^{k} − 2 indices.''',
            'verify': '''
import random, heapq
random.seed(3)
seen = set()
for _ in range(30000):
    a = list(range(1, 32)); random.shuffle(a); heapq.heapify(a)
    seen.add(a.index(4))
assert seen == set(range(1, 15)) and len(seen) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python dicts — insertion order and deletion',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''d = {}
for k in "banana":
    d[k] = d.get(k, 0) + 1
del d['b']
d['b'] = 9
d['a'] += 1
print(list(d.items()))''',
            'options': [
                "`[('n', 2), ('b', 9), ('a', 4)]`",
                "`[('b', 9), ('a', 4), ('n', 2)]`",
                "`[('a', 4), ('n', 2), ('b', 9)]`",
                "`[('a', 3), ('n', 2), ('b', 9)]`",
            ],
            'answer': 'C',
            'solution': '''Since Python 3.7, a dict iterates in **insertion order** of its keys. Updating the value of an existing key does **not** change its position; deleting a key and inserting it again puts it at the **end**.

- Counting "banana": keys inserted in order b, a, n → {b: 1, a: 3, n: 2}.
- `del d['b']` → {a: 3, n: 2}.
- `d['b'] = 9` → re-inserted at the end → {a: 3, n: 2, b: 9}.
- `d['a'] += 1` → value update in place → {a: 4, n: 2, b: 9}.

Output `[('a', 4), ('n', 2), ('b', 9)]` → option **(C)**.

- (A) assumes updating 'a' moves it to the end.
- (B) assumes 'b' regains its original first position.
- (D) ignores the final increment.

**Tip:** underneath, CPython keeps a dense entries array plus a sparse hash index; deletion leaves a hole in the entries array, and a re-insert appends a new entry.''',
            'verify': 'ANSWER = {\'A\': \'C\', \'C\': \'A\'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == "[(\'a\', 4), (\'n\', 2), (\'b\', 9)]" and ANSWER == \'A\'',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search on the answer',
            'text': 'The program finds the smallest integer speed v such that piles of sizes P can be finished within H hours, eating at most v units per hour from one pile (time for a pile p is ⌈p / v⌉). What is printed?',
            'code': '''import math
P, H = [30, 11, 23, 4, 20], 6
lo, hi, it = 1, max(P), 0
while lo < hi:
    mid = (lo + hi) // 2
    it += 1
    if sum(math.ceil(p / mid) for p in P) <= H:
        hi = mid
    else:
        lo = mid + 1
print(lo, it)''',
            'options': ['`23 5`', '`22 5`', '`23 4`', '`30 5`'],
            'answer': 'A',
            'solution': '''The predicate 'speed v suffices' is **monotone** (if v works, every larger v works), so binary search finds the first v where it becomes true. The loop keeps the answer in [lo, hi].

Hours needed: hours(v) = ∑⌈p/v⌉.
- it 1: lo=1, hi=30, mid=15 → 2+1+2+1+2 = 8 > 6 → lo = 16
- it 2: mid=23 → 2+1+1+1+1 = 6 ≤ 6 → hi = 23
- it 3: mid=19 → 2+1+2+1+2 = 8 → lo = 20
- it 4: mid=21 → 2+1+2+1+1 = 7 → lo = 22
- it 5: mid=22 → 2+1+2+1+1 = 7 → lo = 23
- lo = hi = 23 → stop.

Output `23 5` → option **(A)**.

- (B) 22 needs 7 hours (the 23-pile takes 2 hours).
- (C) miscounts iterations (the search space 1..30 needs ⌈log₂ 30⌉ = 5 halvings).
- (D) is a valid but not minimal speed.

**Trap:** writing `hi = mid - 1` when the predicate is true would skip the answer.''',
            'verify': "assert OUTPUT.strip() == '23 5' and ANSWER == 'A'",
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort — exact comparison count',
            'text': 'Insertion sort (ascending) is applied to [5, 1, 4, 2, 3]. Each evaluation of `a[j] > key` counts as one comparison; the inner loop also stops (without a comparison) when j becomes −1. The total number of comparisons is:',
            'options': ['6', '9', '10', '7'],
            'answer': 'B',
            'solution': '''Comparisons = (number of shifts) + (number of passes that end with a *failing* comparison rather than at j = −1). Shifts = inversions.

Inversions of [5, 1, 4, 2, 3]: (5,1), (5,4), (5,2), (5,3), (4,2), (4,3) → 6.

Pass by pass:
- insert 1: 5 > 1 shift; j = −1 stop → 1 comparison
- insert 4: 5 > 4 shift; 1 > 4? no → 2 comparisons
- insert 2: 5 shift, 4 shift, 1 > 2? no → 3 comparisons
- insert 3: 5 shift, 4 shift, 2 > 3? no → 3 comparisons

Total = 1 + 2 + 3 + 3 = **9** = 6 shifts + 3 failing comparisons → option **(B)**.

- (A) counts only shifts.
- (C) adds a failing comparison to every pass, including the one that ran off the front.
- (D) undercounts the last pass.

**Tip:** for n elements, comparisons = inversions + (n − 1) − (number of elements that become the new minimum of the sorted prefix).''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

a = [5,1,4,2,3]; c = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0:
        c += 1
        if a[j] > key: a[j+1] = a[j]; j -= 1
        else: break
    a[j+1] = key
assert c == 9 and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph theory — cycles, degrees, connectivity',
            'text': 'Which of the following statements about simple undirected graphs is/are TRUE?',
            'options': [
                'If every vertex has degree at least 2, the graph is connected',
                'A connected graph with n vertices and n edges contains exactly one cycle',
                'Every graph with n ≥ 2 vertices has two vertices of equal degree',
                'A graph with 10 vertices, 12 edges and exactly 2 connected components contains at least 4 distinct cycles',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''- (D) A spanning forest of a graph with n vertices and c components has n − c edges. Each of the remaining e − (n − c) = 12 − 8 = **4** edges closes a different *fundamental cycle* with the forest (each contains its own non-forest edge, so they are distinct). **True.**

- (C) Degrees lie in {0, …, n−1}, but 0 and n−1 cannot both occur (a vertex of degree n−1 is adjacent to everything). So n vertices take at most n−1 distinct values → by pigeonhole two are equal. **True.**

- (B) Take a spanning tree (n − 1 edges); exactly one edge uv is left over. A tree has no cycle, so every cycle must use uv, and the rest of such a cycle is a u–v path inside the tree — which is unique. Hence exactly one cycle. **True.**

- (A) Two disjoint triangles: every degree is 2, but the graph has two components. **False.**

**Trap:** confusing 'minimum degree ≥ 2 ⇒ contains a cycle' (true) with '⇒ connected' (false).''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import random
from itertools import combinations
def count_cycles(n, E):
    adj = {v: set() for v in range(n)}
    for u, v in E: adj[u].add(v); adj[v].add(u)
    cyc = set()
    def dfs(start, u, path):
        for w in adj[u]:
            if w == start and len(path) >= 3:
                cyc.add(frozenset(frozenset(e) for e in zip(path, path[1:] + [start])))
            elif w > start and w not in path:
                dfs(start, w, path + [w])
    for s0 in range(n): dfs(s0, s0, [s0])
    return len(cyc)
def comps(n, E):
    p = list(range(n))
    def f(x):
        while p[x] != x: x = p[x]
        return x
    for u, v in E: p[f(u)] = f(v)
    return len({f(v) for v in range(n)})
random.seed(7)
okA = True
allE = list(combinations(range(10), 2))
tried = 0
while tried < 150:
    E = random.sample(allE, 12)
    if comps(10, E) != 2: continue
    tried += 1
    if count_cycles(10, E) < 4: okA = False
okB = True
pairs5 = list(combinations(range(5), 2))
for mask in range(1 << 10):
    deg = [0]*5
    for b, (u, v) in enumerate(pairs5):
        if mask >> b & 1: deg[u] += 1; deg[v] += 1
    if len(set(deg)) == 5: okB = False
okC = True
for mask in range(1 << 10):
    E = [pairs5[b] for b in range(10) if mask >> b & 1]
    if len(E) == 5 and comps(5, E) == 1 and count_cycles(5, E) != 1: okC = False
twoTri = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]
okD = comps(6, twoTri) == 1
truth = {'A': okA, 'B': okB, 'C': okC, 'D': okD}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — closures, class attributes, try/finally',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Counter:
    total = 0
    def __init__(self):
        self.fns = []
        for i in range(3):
            def f(x, i=i):
                Counter.total += x * i
                return Counter.total
            self.fns.append(f)
    def run(self, vals):
        try:
            for f, v in zip(self.fns, vals):
                if v < 0:
                    raise ValueError(v)
                f(v)
            return Counter.total
        except ValueError as e:
            return -e.args[0]
        finally:
            Counter.total += 100

c = Counter()
print(c.run([1, 2, 3]), c.run([4, -5, 6]), Counter.total)''',
            'options': ['`108 5 208`', '`8 5 208`', '`108 208 208`', '`8 -5 208`'],
            'answer': 'B',
            'solution': '''Three mechanisms interact:
- `i=i` freezes each closure's multiplier at 0, 1, 2 (no late-binding problem).
- `Counter.total` is a **class** attribute shared by all calls.
- In `return expr` inside `try`, `expr` is evaluated **before** `finally` runs; `finally` cannot change an already-computed return value (it does not itself return).

First call `run([1, 2, 3])`:
- f₀(1): total += 0 → 0;  f₁(2): += 2 → 2;  f₂(3): += 6 → 8.
- `return Counter.total` computes **8**; then `finally` makes total 108.

Second call `run([4, −5, 6])`:
- f₀(4): += 0 → 108.
- v = −5 → `ValueError(-5)`; handler returns −(−5) = **5**; `finally` → total 208.

The arguments of `print` are evaluated left to right, so `Counter.total` is read last → **208**.

Output `8 5 208` → option **(B)**.

- (A) assumes `finally` runs before the return value is computed.
- (C) additionally treats the except-branch return like the try-branch.
- (D) forgets the negation in `-e.args[0]`.

**Trap:** a `return` *inside* `finally` would override; a plain statement there only has side effects.''',
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '8 5 208' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recursion — memoisation via a mutable default',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''calls = 0

def f(n, memo={}):
    global calls
    calls += 1
    if n in memo:
        return memo[n]
    r = 1 if n < 3 else f(n - 1) + f(n - 3)
    memo[n] = r
    return r

f(10)
f(12)
print(calls)''',
            'answer': '22',
            'solution': '''The default dict `memo={}` is created once and **shared by every call**, so it acts as a persistent cache — even across the two top-level calls. Every call (hit or miss) increments `calls`.

First call f(10):
- Each n is computed (a miss) at most once. f(10) → f(9) → … → f(3) → f(2) (base) then f(0) (base); returning up, f(4) needs f(1) (base, new), and f(n−3) for n ≥ 5 is always already cached.
- Computed values: n = 0 … 10 → 11 misses. Each computed n ≥ 3 (8 values: 3 … 10) makes exactly 2 calls → 16 calls, plus the top-level call → **17**.

Second call f(12):
- f(12) miss → calls f(11) (miss) and f(9) (hit); f(11) calls f(10) (hit) and f(8) (hit).
- Calls: f(12), f(11), f(10), f(8), f(9) → **5**.

Total = 17 + 5 = **22**.

**Trap:** assuming the memo is empty again for f(12) (which would give 17 + 21 = 38), or counting only cache misses (13).''',
            'verify': '''
assert OUTPUT.strip() == ANSWER
cnt = [0]
def g(n, memo):
    cnt[0] += 1
    if n in memo: return memo[n]
    r = 1 if n < 3 else g(n-1, memo) + g(n-3, memo)
    memo[n] = r; return r
m = {}
g(10, m); g(12, m)
assert cnt[0] == 22
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST vs binary heap built from the same keys',
            'text': 'The keys 15, 9, 22, 4, 12, 19, 30, 11, 13, 2 are inserted, in that order, (i) into an empty BST T (shown) and (ii) into an empty binary **min**-heap H stored as an array (0-based), using the standard sift-up insertion. Depth of the root is 0. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        15,
                        [
                            9,
                            [
                                4,
                                [2],
                                None,
                            ],
                            [
                                12,
                                [11],
                                [13],
                            ],
                        ],
                        [
                            22,
                            [19],
                            [30],
                        ],
                    ],
                    'caption': 'Figure: BST T',
                },
            ],
            'options': [
                'Exactly two keys have the same depth in T as in H',
                'The post-order traversal of T ends with 22, 15, and the last element of the array H is 13',
                'The height of T is 3',
                'In H, the root is 2 and its two children are 4 and 19',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Build H by sift-up insertion:
- 15 → [15];  9 → swap → [9, 15];  22 → [9, 15, 22].
- 4 (index 3): swap with 15, then with 9 → [4, 9, 22, 15].
- 12 (index 4): parent 9 < 12 → [4, 9, 22, 15, 12].
- 19 (index 5): swap with 22 → [4, 9, 19, 15, 12, 22];  30 → appended.
- 11 (index 7): swap with 15; parent 9 < 11 → stop → [4, 9, 19, 11, 12, 22, 30, 15].
- 13 (index 8): parent 11 < 13 → stays.
- 2 (index 9): swap with 12, then 9, then 4 → H = [2, 4, 19, 11, 9, 22, 30, 15, 13, 12].

- (A) Depths (T, H): 15 (0, 3), 9 (1, 2), 22 (1, 2), 4 (2, 1), 12 (2, 3), 19 (2, 1), 30 (2, 2) ✓, 11 (3, 2), 13 (3, 3) ✓, 2 (3, 0). Exactly 30 and 13 match. **True.**
- (B) Post-order of T = 2, 4, 11, 13, 12, 9, 19, 30, 22, 15 — ends with 22, 15 ✓, but the last array element of H is **12**, not 13. **False.**
- (C) Longest root-to-leaf path in T: 15→9→4→2 or 15→9→12→11 → 3 edges. **True.**
- (D) H[0] = 2, H[1] = 4, H[2] = 19. **True.**

**Trap:** in H the last inserted key 2 travels all the way to the root, dragging 12 (not 13) into the last slot.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [2, 4, 19, 11, 9, 22, 30, 15, 13, 12],
                    'caption': 'Min-heap H after all insertions',
                },
            ],
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import heapq, math
keys = [15,9,22,4,12,19,30,11,13,2]
def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in keys: T = ins(T, k)
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
def depth(t, k, d=0):
    return d if t[0] == k else depth(t[1] if k < t[0] else t[2], k, d+1)
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
H = []
for k in keys:
    H.append(k); i = len(H) - 1
    while i > 0 and H[(i-1)//2] > H[i]:
        H[i], H[(i-1)//2] = H[(i-1)//2], H[i]; i = (i-1)//2
hd = {k: int(math.log2(H.index(k) + 1)) for k in keys}
same = [k for k in keys if depth(T, k) == hd[k]]
truth = {'A': ht(T) == 3, 'B': H[:3] == [2, 4, 19], 'C': len(same) == 2,
         'D': post(T)[-2:] == [22, 15] and H[-1] == 13}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Heaps — counting distinct heaps',
            'text': 'The number of distinct binary **max**-heaps (as arrays of length 9, i.e. complete binary trees filled level by level from the left) that can be formed with the 9 distinct keys 1, 2, …, 9 is ______.',
            'answer': '896',
            'solution': '''The maximum (9) must be at the root. The remaining 8 keys are split between the left and right subtrees, whose **shapes are fixed** by completeness; any choice of which keys go left works, and each side is then any heap of its own shape:
H(n) = C(n − 1, L) · H(L) · H(R), where L, R are the subtree sizes.

Shapes: a complete tree with 9 nodes has levels of 1, 2, 4 and 2 nodes. The two last-level nodes are both under the left child, so L = 1 + 2 + 2 = 5 (indices 1, 3, 4, 7, 8) and R = 3 (indices 2, 5, 6).

- H(1) = 1, H(2) = 1 (root + one child), H(3) = C(2,1)·1·1 = 2.
- H(5): L = 3, R = 1 → C(4,3)·H(3)·H(1) = 4·2 = 8.
- H(9) = C(8,5)·H(5)·H(3) = 56 · 8 · 2 = **896**.

Sanity check: 9! = 362 880 permutations, of which only 896 satisfy the heap property (the brute-force count agrees).

**Trap:** using a balanced split L = R = 4 (would give C(8,4)·3·3 = 630), or forgetting the binomial factor for choosing which keys go left.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': ['9', 'L', 'R', 'L', 'L', 'R', 'R', 'L', 'L'],
                    'caption': 'Shape: 5 positions in the left subtree (L), 3 in the right (R)',
                },
            ],
            'verify': '''
from itertools import permutations
c = 0
for p in permutations(range(9)):
    if all(p[(i-1)//2] > p[i] for i in range(1, 9)): c += 1
assert c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Merge sort — bottom-up vs top-down',
            'text': '**Bottom-up** (iterative) merge sort merges runs of width 1, 2, 4, … from left to right; at each width, a run with no partner on its right is left unchanged. A merge compares the two front elements until one run is exhausted. The number of element comparisons it makes on [5, 2, 8, 6, 1, 9, 3] is:',
            'options': ['12', '14', '13', '11'],
            'answer': 'C',
            'solution': '''Bottom-up and top-down merge sort split an odd-length array differently, so their comparison counts can differ.

Width 1 (pairs): (5|2) → 1, (8|6) → 1, (1|9) → 1, [3] has no partner → **3** comparisons; array [2, 5, 6, 8, 1, 9, 3].

Width 2: [2, 5] + [6, 8]: 2<6, 5<6, left exhausted → **2**. [1, 9] + [3]: 1<3, 9>3, right exhausted → **2**. Array [2, 5, 6, 8, 1, 3, 9].

Width 4: [2, 5, 6, 8] + [1, 3, 9]: 1, 2, 3, 5, 6, 8 are output by 6 comparisons, then 9 is copied → **6**.

Total = 3 + 4 + 6 = **13** → option **(C)**.

- (A), (D) miscount the unequal merges.
- (B) 14 is what **top-down** merge sort (split ⌊n/2⌋ = 3 | 4) makes: [5 | 2, 8] → 1 + 2, [6, 1 | 9, 3] → 1 + 1 + 3, final 3 + 4 run merge → 6; total 14.

**Trap:** assuming both versions perform identical merges — they only coincide when n is a power of two.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Bottom-up passes',
                    'col_labels': ['width', 'array after pass', 'comparisons'],
                    'row_labels': ['pass 1', 'pass 2', 'pass 3'],
                    'rows': [
                        [1, '2 5 6 8 1 9 3', 3],
                        [2, '2 5 6 8 1 3 9', 4],
                        [4, '1 2 3 5 6 8 9', 6],
                    ],
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

def bu(a):
    a = a[:]; n = len(a); w = 1; c = 0
    while w < n:
        for lo in range(0, n, 2*w):
            L = a[lo:lo+w]; R = a[lo+w:lo+2*w]; out = []; i = j = 0
            while i < len(L) and j < len(R):
                c += 1
                if L[i] <= R[j]: out.append(L[i]); i += 1
                else: out.append(R[j]); j += 1
            a[lo:lo+2*w] = out + L[i:] + R[j:]
        w *= 2
    return a, c
def td(a, c):
    if len(a) <= 1: return a
    m = len(a)//2; L = td(a[:m], c); R = td(a[m:], c); out = []; i = j = 0
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
x = [5,2,8,6,1,9,3]
s, c = bu(x); c2 = [0]; td(x, c2)
assert s == sorted(x) and c == 13 and c2[0] == 14 and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — edges on some shortest path',
            'text': 'In the weighted undirected graph shown, the number of edges that lie on **at least one** shortest path from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'edges': [
                        ['S', 'A', 3],
                        ['S', 'B', 2],
                        ['S', 'C', 6],
                        ['A', 'B', 1],
                        ['A', 'D', 3],
                        ['B', 'D', 5],
                        ['B', 'E', 3],
                        ['D', 'T', 2],
                        ['E', 'T', 3],
                        ['D', 'E', 1],
                        ['C', 'T', 3],
                        ['A', 'C', 2],
                    ],
                    'pos': {
                        'S': [0, 1.5],
                        'A': [1.8, 2.8],
                        'B': [1.8, 0.2],
                        'C': [1.8, 4.8],
                        'D': [3.8, 2.4],
                        'E': [3.8, 0.2],
                        'T': [5.6, 1.5],
                    },
                },
            ],
            'answer': '10',
            'solution': '''Run Dijkstra from S **and** from T. An edge (u, v, w) lies on some shortest S–T path iff d_{S}(u) + w + d_{T}(v) = d_{S}(T) (in either orientation).

Distances from S: S 0, A 3, B 2, C 5, D 6, E 5, T **8**.
Distances to T:   S 8, A 5, B 6, C 3, D 2, E 3, T 0.

Check each edge (best orientation):
- S–A: 0 + 3 + 5 = 8 ✓   - S–B: 0 + 2 + 6 = 8 ✓   - S–C: 0 + 6 + 3 = 9 ✗
- A–B: d_{S}(B) + 1 + d_{T}(A) = 2 + 1 + 5 = 8 ✓ (path S–B–A–D–T)
- A–D: 3 + 3 + 2 = 8 ✓   - B–D: 2 + 5 + 2 = 9 ✗   - B–E: 2 + 3 + 3 = 8 ✓
- D–T: 6 + 2 = 8 ✓   - E–T: 5 + 3 = 8 ✓
- D–E: d_{S}(E) + 1 + d_{T}(D) = 5 + 1 + 2 = 8 ✓ (path S–B–E–D–T)
- C–T: 5 + 3 = 8 ✓   - A–C: 3 + 2 + 3 = 8 ✓ (path S–A–C–T)

Edges on some shortest path: 12 − 2 = **10** (all except S–C and B–D).

**Trap:** only marking the edges of the single path Dijkstra happens to record in its predecessor tree, or testing only one orientation of each undirected edge (A–B and D–E are used 'backwards' relative to the letter order).''',
            'verify': '''
import heapq
E = [('S','A',3),('S','B',2),('S','C',6),('A','B',1),('A','D',3),('B','D',5),('B','E',3),
     ('D','T',2),('E','T',3),('D','E',1),('C','T',3),('A','C',2)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
def dij(s):
    d = {v: float('inf') for v in G}; d[s] = 0; pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]: continue
        for v, w in G[u]:
            if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
    return d
ds, dt = dij('S'), dij('T'); D = ds['T']
on = [e for e in E if ds[e[0]] + e[2] + dt[e[1]] == D or ds[e[1]] + e[2] + dt[e[0]] == D]
assert D == 8 and len(on) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Hashing — collision probabilities',
            'text': 'Three keys are inserted into a hash table with 5 slots using separate chaining. Each key independently hashes to each slot with probability 1/5. Which of the following statements is/are TRUE?',
            'options': [
                'The expected length of the longest chain is 1.6',
                'The expected number of non-empty slots is 2.44',
                'The probability that no two keys share a slot is 12/25',
                'The probability that all three keys land in the same slot is 1/25',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''There are 5³ = 125 equally likely outcomes.

- (A) Longest chain L: P(L = 1) = 60/125, P(L = 3) = 5/125, so P(L = 2) = 60/125. E[L] = (60·1 + 60·2 + 5·3)/125 = 195/125 = **1.56**, not 1.6. **False.**
- (B) Linearity of expectation: a slot stays empty with probability (4/5)³ = 64/125, so E[non-empty] = 5 · (1 − 64/125) = 5 · 61/125 = **2.44**. **True.**
- (C) All distinct: 5 · 4 · 3 = 60 outcomes → 60/125 = **12/25** = 0.48. **True.**
- (D) All in one slot: 5 outcomes → 5/125 = **1/25**. **True.**

Even with load factor α = 0.6, a collision happens with probability 0.52 — the birthday effect.

**Trap:** in (A), guessing 1 + α = 1.6 — that is the expected cost of a successful search pattern, not the expected *maximum* chain length.''',
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from fractions import Fraction as Fr
from itertools import product
outs = list(product(range(5), repeat=3))
N = len(outs)
pA = Fr(sum(1 for o in outs if len(set(o)) == 3), N)
pB = Fr(sum(1 for o in outs if len(set(o)) == 1), N)
eC = Fr(sum(len(set(o)) for o in outs), N)
eD = Fr(sum(max(o.count(s) for s in range(5)) for o in outs), N)
truth = {'A': pA == Fr(12, 25), 'B': pB == Fr(1, 25), 'C': eC == Fr(244, 100),
         'D': eD == Fr(16, 10)}
assert eD == Fr(156, 100)
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Stacks — prefix evaluation with floor division',
            'text': 'The function below evaluates a prefix (Polish) expression by scanning tokens from right to left. The value printed is ______.',
            'code': '''def ev(tokens):
    st = []
    for t in reversed(tokens):
        if t in '+-*/':
            a = st.pop()
            b = st.pop()
            st.append({'+': a + b, '-': a - b,
                       '*': a * b, '/': a // b}[t])
        else:
            st.append(int(t))
    return st[-1]

e = "* - / 7 -2 * 3 - 4 6 / - 5 * 2 6 + 1 3"
print(ev(e.split()))''',
            'answer': '-4',
            'solution': '''Scanning a prefix expression from the right, the **first** value popped is the **left** operand. Note `'-2' in '+-*/'` is False (the string "-2" is not a substring of "+-*/"), so `-2` is an operand. `/` is Python's floor division.

Structure: `* X Y` with X = `- / 7 -2 * 3 - 4 6` and Y = `/ - 5 * 2 6 + 1 3`.

- X: `/ 7 -2` = 7 // −2 = floor(−3.5) = **−4**; `* 3 - 4 6` = 3 × (4 − 6) = −6; X = −4 − (−6) = **2**.
- Y: `- 5 * 2 6` = 5 − 12 = −7; `+ 1 3` = 4; Y = −7 // 4 = floor(−1.75) = **−2**.
- Result: X × Y = 2 × (−2) = **−4**.

**Trap:** with truncating division (C/Java) X = −3 + 6 = 3 and Y = −1, giving −3; popping operands in the postfix order (right operand first) would compute −2 // 7 etc. and give a completely different value.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '*',
                    'children': {
                        '*': ['-', '/'],
                        '-': ['/₁', '×'],
                        '/₁': ['7', '-2'],
                        '×': ['3', '−'],
                        '−': ['4', '6'],
                        '/': ['-₂', '+'],
                        '-₂': ['5', '×₂'],
                        '×₂': ['2', '6₂'],
                        '+': ['1', '3₂'],
                    },
                    'labels': {
                        '/₁': '/',
                        '×': '*',
                        '−': '-',
                        '-₂': '-',
                        '×₂': '*',
                        '6₂': '6',
                        '3₂': '3',
                    },
                    'caption': 'Expression tree of e',
                },
            ],
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'DFS in Python — mutable default visited set',
            'text': 'The directed graph shown is stored as `g` (neighbours listed alphabetically). What does the program print?',
            'code': '''def dfs(g, u, seen=set(), order=None):
    if order is None:
        order = []
    seen.add(u)
    order.append(u)
    for v in g[u]:
        if v not in seen:
            dfs(g, v, seen, order)
    return order

g = {'A': 'BC', 'B': 'D', 'C': 'E', 'D': 'F',
     'E': '', 'F': '', 'G': 'AH', 'H': 'E'}
print(dfs(g, 'A'), dfs(g, 'G'))''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['G', 'A'],
                        ['G', 'H'],
                        ['H', 'E'],
                    ],
                    'pos': {
                        'A': [1.5, 2],
                        'B': [0.5, 1],
                        'C': [2.5, 1],
                        'D': [0.5, 0],
                        'E': [2.5, 0],
                        'F': [0.5, -1],
                        'G': [3.5, 3],
                        'H': [4, 1],
                    },
                },
            ],
            'options': [
                "`['A', 'B', 'D', 'F', 'C', 'E'] ['G', 'H']`",
                "`['A', 'B', 'D', 'F', 'C', 'E'] ['G', 'A', 'B', 'D', 'F', 'C', 'E', 'H']`",
                "`['A', 'B', 'D', 'F', 'C', 'E'] ['G']`",
                "`['A', 'B', 'C', 'D', 'E', 'F'] ['G', 'H']`",
            ],
            'answer': 'A',
            'solution': '''`order` is correctly reset with the `None` idiom, but `seen=set()` is a mutable default evaluated **once** — the second top-level call starts with everything the first call visited already marked.

First call dfs(g, 'A') — recursive DFS, neighbours in listed order:
- A → B → D → F (dead end) → back to A → C → E.
- order = [A, B, D, F, C, E]; seen = {A, B, C, D, E, F}.

Second call dfs(g, 'G') with the same `seen`:
- G added. Neighbour A is already in seen → skipped. H is new → visit H; its neighbour E is in seen → skipped.
- order = [G, H].

Output → option **(A)**.

- (B) is the correct DFS from G with a fresh visited set — the intended behaviour.
- (C) assumes G's neighbours are all seen — H was not reachable from A.
- (D) is a BFS order for the first call.

**Trap:** the bug is silent for the first call; only repeated calls reveal it. Always use `seen=None` and create the set inside.''',
            'verify': 'assert OUTPUT.strip() == "[\'A\', \'B\', \'D\', \'F\', \'C\', \'E\'] [\'G\', \'H\']" and ANSWER == \'A\'',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Counting BSTs by height',
            'text': 'Consider all binary search trees containing exactly the keys 1, 2, 3, 4, 5. Height is the number of edges on the longest root-to-leaf path. Which of the following statements is/are TRUE?',
            'options': [
                'Exactly 16 of them have height 4',
                'Exactly 5 of them have 3 at the root',
                'There are exactly 32 such BSTs',
                'Exactly 6 of them have the minimum possible height, 2',
            ],
            'answer': ['A', 'D'],
            'solution': '''The number of BSTs on n keys is the Catalan number Cₙ: C₀..C₅ = 1, 1, 2, 5, 14, 42. With root r there are C_{r−1} · C_{5−r} trees.

- (A) Height 4 with 5 nodes means a path: the root is 1 or 5 (otherwise both sides are non-empty and the height ≤ 3), and the same holds at every level → each of the 4 non-leaf steps chooses min or max of the remaining keys → 2⁴ = 16. **True.**
- (B) Root 3: left {1, 2} → C₂ = 2, right {4, 5} → 2 → 4 trees. **False.**
- (C) Total = C₅ = 42 (= 14 + 5 + 4 + 5 + 14 by root). **False.**
- (D) Height 2 holds at most 7 nodes; with 5 keys the root's two subtrees must both have height ≤ 1, i.e. sizes ≤ 3 and summing to 4: (1, 3), (2, 2), (3, 1). A 3-node subtree of height 1 must be perfect (1 way); a 2-node subtree has 2 shapes. Count = 1·1 + 2·2 + 1·1 = 6. **True.**

Height distribution: h=2: 6, h=3: 20, h=4: 16 (sum 42).

**Trap:** in (C), confusing 2^{n} (or 2^{n−1} chains) with the Catalan count.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        3,
                        [
                            2,
                            [1],
                            None,
                        ],
                        [
                            4,
                            None,
                            [5],
                        ],
                    ],
                    'caption': 'One of the 6 BSTs of height 2',
                },
                {
                    'type': 'bintree',
                    'tree': [
                        1,
                        None,
                        [
                            5,
                            [
                                2,
                                None,
                                [
                                    4,
                                    [3],
                                    None,
                                ],
                            ],
                            None,
                        ],
                    ],
                    'caption': 'One of the 16 BSTs of height 4 (a zig-zag path)',
                },
            ],
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from functools import lru_cache
@lru_cache(None)
def le(n, h):
    if n == 0: return 1
    if h < 0: return 0
    return sum(le(k, h-1) * le(n-1-k, h-1) for k in range(n))
exact = lambda n, h: le(n, h) - le(n, h-1)
root3 = le(2, 9) * le(2, 9)
truth = {'A': le(5, 9) == 32, 'B': exact(5, 4) == 16, 'C': exact(5, 2) == 6,
         'D': root3 == 5}
assert le(5, 9) == 42 and exact(5, 1) == 0
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
    ],
}
