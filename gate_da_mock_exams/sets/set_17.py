# Set 17 — Iterators, Generators & Comprehensions
SET = {
    'number': 17,
    'title': 'Iterators, Generators & Comprehensions',
    'difficulty': 'GATE-level',
    'focus': 'generators, iterator exhaustion, comprehensions, map/filter/zip',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Generator exhaustion and `in`',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''nums = [1, 2, 3, 4, 5, 6]
g = (n for n in nums if n % 2 == 0)
print(4 in g, list(g), sum(g))''',
            'options': ['`True [2, 4, 6] 12`', '`True [6] 6`', '`True [6] 0`', '`True [] 0`'],
            'answer': 'C',
            'solution': '''A generator expression is a **one-shot iterator**. The `in` operator on an iterator consumes items until it finds a match (or exhausts it), and whatever was consumed is gone.

Arguments of `print` are evaluated left to right:

- `4 in g`: the generator yields 2 (≠ 4), then 4 (match) → `True`. Items 2 and 4 are consumed.
- `list(g)`: continues from where it stopped: 5 is filtered out, 6 is yielded → `[6]`. The generator is now exhausted.
- `sum(g)`: nothing left → `sum` of an empty iterable is 0.

Output: `True [6] 0`.

- (A) treats `g` like a list that can be re-read.
- (B) assumes `sum` restarts the generator, or forgets that `list` exhausted it.
- (D) assumes `in` exhausts the whole generator even after a match.

**Trap:** membership tests stop at the first match; they do not necessarily drain the iterator.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'True [6] 0' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Nested list comprehension — counting',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''pairs = [(i, j) for i in range(6)
                for j in range(i, 6)
                if (i + j) % 3 == 0]
print(len(pairs))''',
            'answer': '7',
            'solution': '''In a comprehension with several `for` clauses, the **leftmost** loop is the outer loop and later clauses may use earlier variables (here j starts at i). The `if` filters each pair.

Enumerate i ≤ j < 6 with (i + j) divisible by 3:

- i = 0: j ∈ {0, 3} → 2 pairs
- i = 1: j ∈ {2, 5} → 2 pairs
- i = 2: j ∈ {4} → 1 pair (j = 1 is not allowed since j ≥ i)
- i = 3: j ∈ {3} → 1 pair
- i = 4: j ∈ {5} → 1 pair
- i = 5: j = 5 gives 10, not divisible → 0

Total = 2 + 2 + 1 + 1 + 1 + 0 = **7**: (0,0), (0,3), (1,2), (1,5), (2,4), (3,3), (4,5).

**Trap:** counting ordered pairs over the full 6 × 6 grid (12 pairs) or forgetting the diagonal pairs (0,0) and (3,3).''',
            'verify': '''
c = sum(1 for i in range(6) for j in range(6) if i <= j and (i + j) % 3 == 0)
assert OUTPUT.strip() == ANSWER == str(c)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': '`zip` over the same iterator',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''it = iter([10, 20, 30, 40, 50, 60, 70])
pairs = list(zip(it, it))
print(pairs, next(it, -1))''',
            'options': [
                '`[(10, 20), (30, 40), (50, 60)] -1`',
                '`[(10, 20), (30, 40), (50, 60)] 70`',
                '`[(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60), (70, 70)] -1`',
                '`[(10, 20), (30, 40), (50, 60), (70, None)] -1`',
            ],
            'answer': 'A',
            'solution': '''Both arguments of `zip` are the **same** iterator object, so each tuple takes two consecutive items: (10, 20), (30, 40), (50, 60).

For the fourth tuple, `zip` asks its first argument for an item and receives 70; it then asks the second argument, which is exhausted, so `zip` stops. The 70 already fetched is **discarded** — it is not put back. Hence `next(it, -1)` finds nothing and returns the default −1.

- (B) assumes the leftover 70 is still available.
- (C) would happen with `zip(lst, lst)` on a *list*, which creates two independent iterators.
- (D) is the behaviour of `itertools.zip_longest`, not `zip`.

**Trap:** `zip` silently drops a partially-built tuple; with a shared iterator that also silently loses an element.''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[(10, 20), (30, 40), (50, 60)] -1' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': 'The postfix expression `9 4 2 - 3 * + 6 2 / -` is evaluated with a stack: an operand is pushed; an operator pops the right operand, then the left operand, and pushes the result (`/` is exact division here). Which of the following statements is/are TRUE?',
            'options': [
                'The final result is 12',
                'The maximum number of items on the stack at any time is 3',
                'At some moment the value 6 is on top of the stack',
                'At some moment the stack holds 4 items',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Trace the stack (bottom → top) after each token:

- 9 → [9]
- 4 → [9, 4]
- 2 → [9, 4, 2]
- − → 4 − 2 = 2 → [9, 2]
- 3 → [9, 2, 3]
- * → 2 × 3 = 6 → [9, 6]
- + → 9 + 6 = 15 → [15]
- 6 → [15, 6]
- 2 → [15, 6, 2]
- / → 6 / 2 = 3 → [15, 3]
- − → 15 − 3 = 12 → [12]

- (A) **True** — result 12.
- (B) **True** — depth 3 is reached (after the first 2, after 3, after the second 2) and never exceeded.
- (C) **True** — 6 is on top after `*` and again when the operand 6 is pushed.
- (D) **False** — the depth never reaches 4.

**Trap:** operand order — for `−` and `/` the *first* pop is the right operand. Popping in the wrong order gives 2 − 4 and 2 / 6.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [15, 6, 2],
                    'label': 'Stack just before `/`',
                },
            ],
            'verify': '''
st = []; tops = []; mx = 0
for tok in "9 4 2 - 3 * + 6 2 / -".split():
    if tok in "+-*/":
        b = st.pop(); a = st.pop()
        st.append({'+': a+b, '-': a-b, '*': a*b, '/': a/b}[tok])
    else: st.append(int(tok))
    mx = max(mx, len(st)); tops.append(st[-1])
assert st == [12] and mx == 3 and 6 in tops
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Lazy `map`/`filter` pipelines',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''log = []
def f(x):
    log.append(x)
    return x % 3 == 0

m = map(lambda x: x * x, filter(f, range(1, 20)))
found = any(v > 50 for v in m)
print(len(log))''',
            'answer': '9',
            'solution': '''In Python 3 `map` and `filter` return **lazy iterators**; nothing is computed until a value is requested. `any` stops at the first true value (short-circuit), so only the prefix of `range(1, 20)` needed to find it is ever passed to `f`.

- `filter` calls f(1), f(2), f(3) → 3 passes; `map` yields 9 (not > 50).
- f(4), f(5), f(6) → 6 passes; yields 36 (not > 50).
- f(7), f(8), f(9) → 9 passes; yields 81 > 50 → `any` returns True and stops.

`f` was called for x = 1..9, so `len(log)` = **9**.

**Trap:** answering 19 assumes `filter` processes the whole range eagerly (Python 2 behaviour, or wrapping it in `list`).''',
            'verify': 'assert OUTPUT.strip() == ANSWER and found and log == list(range(1, 10))',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — `bisect` boundaries',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''import bisect
a = [2, 4, 4, 4, 7, 9, 9, 12]
x = bisect.bisect_right(a, 4) - bisect.bisect_left(a, 9)
print(x, bisect.bisect_left(a, 8))''',
            'options': ['`-1 5`', '`-2 5`', '`-1 4`', '`0 5`'],
            'answer': 'A',
            'solution': '''`bisect_left(a, x)` returns the first index i with a[i] ≥ x (the leftmost insertion point); `bisect_right(a, x)` returns the first index with a[i] > x. Both are binary searches.

- `bisect_right(a, 4)`: the 4s occupy indices 1..3, so the first element > 4 is at index **4**.
- `bisect_left(a, 9)`: the first element ≥ 9 is a[5] = 9 → **5**.
- x = 4 − 5 = −1.
- `bisect_left(a, 8)`: 8 is absent; first element ≥ 8 is a[5] = 9 → **5**.

Output: `-1 5`.

- (B) uses bisect_right(a, 4) = 3 (the index of the last 4, off by one).
- (C) returns 4 for 8, i.e. the index of the last element < 8 rather than the insertion point.
- (D) confuses bisect_left(a, 9) with bisect_left(a, 7) = 4.

**Tip:** `bisect_right(a, x) − bisect_left(a, x)` counts occurrences of x in O(log n).''',
            'verify': '''
def lb(a, x): return next((i for i, v in enumerate(a) if v >= x), len(a))
def ub(a, x): return next((i for i, v in enumerate(a) if v > x), len(a))
assert (ub(a, 4) - lb(a, 9), lb(a, 8)) == (-1, 5)
assert OUTPUT.strip() == '-1 5' and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'Keys 22, 15, 30, 44, 9, 63, 51, 36, 13 are inserted in this order into a hash table with 7 buckets using h(k) = k mod 7 and separate chaining, where each new key is inserted at the **head** of its chain. Searches are then performed for 44, 36, 58 and 70; each search scans its chain from the head until the key is found or the chain ends, and every key examined counts as one comparison. The total number of comparisons over the four searches is ______.',
            'answer': '9',
            'solution': '''Bucket of each key: 22→1, 15→1, 30→2, 44→2, 9→2, 63→0, 51→2, 36→1, 13→6. With head insertion each chain lists keys in **reverse** insertion order:

- bucket 0: 63
- bucket 1: 36 → 15 → 22
- bucket 2: 51 → 9 → 44 → 30
- bucket 6: 13

Searches:

- 44 (bucket 2): 51, 9, 44 → 3 comparisons.
- 36 (bucket 1): found at the head → 1.
- 58 (58 mod 7 = 2): 51, 9, 44, 30, end → 4 (unsuccessful, whole chain).
- 70 (70 mod 7 = 0): 63, end → 1.

Total = 3 + 1 + 4 + 1 = **9**.

**Trap:** building chains in insertion order (tail insertion) would make 44 cost 2 and 36 cost 3. Also, an unsuccessful search in an empty bucket would cost 0, but bucket 0 is not empty here.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: [63],
                        1: [36, 15, 22],
                        2: [51, 9, 44, 30],
                        6: [13],
                    },
                    'caption': 'Chains after all insertions (head first)',
                },
            ],
            'verify': '''
T = {}
for k in [22, 15, 30, 44, 9, 63, 51, 36, 13]: T.setdefault(k % 7, []).insert(0, k)
def cost(k):
    c = 0
    for x in T.get(k % 7, []):
        c += 1
        if x == k: break
    return c
assert sum(cost(k) for k in [44, 36, 58, 70]) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bubble sort with early exit',
            'text': 'Bubble sort with the early-exit flag (stop after the first pass that makes no swap; pass i compares adjacent pairs in A[0..n−1−i]) sorts `[4, 1, 2, 3, 7, 5, 6, 9, 8]` in ascending order. The total number of key comparisons is',
            'options': ['8', '15', '21', '36'],
            'answer': 'B',
            'solution': '''Bubble sort pass i scans n − 1 − i adjacent pairs and carries the largest element of the unsorted part to the end. With the flag it stops after a pass with zero swaps.

**Pass 0** (8 comparisons): 4 swaps past 1, 2, 3; 7 swaps past 5 and 6; 9 swaps past 8 → `[1, 2, 3, 4, 5, 6, 7, 8, 9]` (6 swaps).

**Pass 1** (7 comparisons): the array is sorted, no swaps → stop.

Total comparisons = 8 + 7 = **15**.

- (A) 8 forgets that one more pass is needed to *detect* that the array is sorted.
- (C) 21 = 8 + 7 + 6 adds a non-existent third pass.
- (D) 36 = n(n − 1)/2 is the cost without the early-exit flag.

**Tip:** a pass can move a large element many places right, but a small element moves only one place left per pass — here every element was at most one “left-move” from its place.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
                    'row_labels': ['start', 'pass 0', 'pass 1'],
                    'rows': [
                        [4, 1, 2, 3, 7, 5, 6, 9, 8],
                        [1, 2, 3, 4, 5, 6, 7, 8, 9],
                        [1, 2, 3, 4, 5, 6, 7, 8, 9],
                    ],
                },
            ],
            'verify': '''
a = [4, 1, 2, 3, 7, 5, 6, 9, 8]; n = len(a); comps = 0
for i in range(n - 1):
    sw = False
    for j in range(n - 1 - i):
        comps += 1
        if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]; sw = True
    if not sw: break
assert comps == 15 and ['8','15','21','36'][ord(ANSWER) - 65] == '15'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Comprehension scope',
            'text': 'Consider the following Python 3 program. Which of the following statements is/are TRUE?',
            'code': '''x = 'outer'
sq = [x * 2 for x in range(3)]
print(x)
for x in range(3):
    pass
print(x)
y = [i for i in range(3)]''',
            'options': [
                'The first `print` outputs `outer`',
                'The second `print` outputs `2`',
                '`sq` is `[0, 2, 4]`',
                'After the last line, the name `i` is defined at module level',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''In Python 3 a comprehension runs in its **own scope**: its loop variable does not leak into the enclosing scope. An ordinary `for` loop, by contrast, binds its variable in the current scope, and the variable keeps its last value after the loop.

- (A) **True** — the comprehension's `x` is local to it, so the module-level `x` is still `'outer'`.
- (B) **True** — the `for` loop rebinds the module-level `x`; after the loop it is 2.
- (C) **True** — inside the comprehension `x` is an int, so `x * 2` is 0, 2, 4 (not string repetition).
- (D) **False** — `i` exists only inside the comprehension; referring to `i` afterwards raises `NameError`.

**Trap:** Python 2 list comprehensions *did* leak their variable; Python 3 does not. Do not carry that habit over to `for` loops, which still leak.''',
            'verify': '''
assert OUTPUT.split() == ['outer', '2'] and sq == [0, 2, 4] and 'i' not in globals()
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Graph from a comprehension — degrees',
            'text': 'An undirected graph G on vertices 1, 2, …, 8 has edge set `E = [(u, v) for u in range(1, 9) for v in range(u + 1, 9) if v % u == 0]`. The number of vertices of **odd** degree in G is ______.',
            'answer': '6',
            'solution': '''An edge joins u < v exactly when u divides v. List the edges by u:

- u = 1: (1,2) … (1,8) → 7 edges
- u = 2: (2,4), (2,6), (2,8)
- u = 3: (3,6)
- u = 4: (4,8)
- u = 5, 6, 7: none (no multiple ≤ 8)

That is 12 edges. Degrees (proper divisors < v plus multiples ≤ 8):

- deg 1 = 7, deg 2 = 1 + 3 = 4, deg 3 = 1 + 1 = 2, deg 4 = 2 + 1 = 3,
- deg 5 = 1, deg 6 = 3 (1, 2, 3), deg 7 = 1, deg 8 = 3 (1, 2, 4).

Odd degrees: vertices 1, 4, 5, 6, 7, 8 → **6**.

Check with the handshake lemma: sum of degrees = 7+4+2+3+1+3+1+3 = 24 = 2 × 12 ✓, and the number of odd-degree vertices is even ✓.

**Trap:** forgetting that vertex 1 divides everything (degree 7, odd).''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': [1, 2, 3, 4, 5, 6, 7, 8],
                    'edges': [
                        [1, 2],
                        [1, 3],
                        [1, 4],
                        [1, 5],
                        [1, 6],
                        [1, 7],
                        [1, 8],
                        [2, 4],
                        [2, 6],
                        [2, 8],
                        [3, 6],
                        [4, 8],
                    ],
                    'highlight': [1, 4, 5, 6, 7, 8],
                    'pos': {
                        1: [2, 3],
                        2: [0, 1.6],
                        3: [1.4, 1.6],
                        4: [0, 0],
                        5: [2.8, 1.6],
                        6: [1.4, 0],
                        7: [4.2, 1.6],
                        8: [2.8, 0],
                    },
                    'caption': 'Divisibility graph (odd-degree vertices highlighted)',
                },
            ],
            'verify': '''
E = [(u, v) for u in range(1, 9) for v in range(u + 1, 9) if v % u == 0]
deg = {i: 0 for i in range(1, 9)}
for u, v in E: deg[u] += 1; deg[v] += 1
assert len(E) == 12 and sum(d % 2 for d in deg.values()) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Late binding: list vs generator of lambdas',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''fs = [lambda: i * 10 for i in range(3)]
gs = (lambda: i * 10 for i in range(3))
print([f() for f in fs], [g() for g in gs])''',
            'options': [
                '`[20, 20, 20] [20, 20, 20]`',
                '`[0, 10, 20] [0, 10, 20]`',
                '`[20, 20, 20] [0, 10, 20]`',
                '`[0, 10, 20] [20, 20, 20]`',
            ],
            'answer': 'C',
            'solution': '''A lambda does not store the *value* of `i`; it stores a reference to the variable `i` of the enclosing comprehension scope and looks it up **when it is called** (late binding).

**List `fs`:** the list comprehension runs to completion immediately, creating three lambdas that all close over the same `i`. When the loop finishes, `i` = 2. Calling them later gives 2 × 10 three times → `[20, 20, 20]`.

**Generator `gs`:** nothing runs until `[g() for g in gs]` pulls items. The generator creates the first lambda while i = 0 and *pauses*; the consumer calls it right away → 0. Then the generator resumes, sets i = 1, yields the second lambda, which is called at once → 10, and so on → `[0, 10, 20]`.

- (A) assumes the generator also runs to completion before the calls.
- (B) ignores late binding for the list.
- (D) swaps the two behaviours.

**Tip:** to freeze the value use a default argument: `lambda i=i: i * 10`. **Trap:** the difference here comes only from *when* each lambda is called relative to the loop.''',
            'verify': "ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[20, 20, 20] [0, 10, 20]' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Recursive generators — in-order traversal',
            'text': 'The binary tree T shown is encoded as nested lists `[value, left, right]` (None for an empty child). The value printed by the following program is ______.',
            'code': '''def inorder(t):
    if t:
        yield from inorder(t[1])
        yield t[0]
        yield from inorder(t[2])

def check(t):
    it = inorder(t)
    prev = next(it)
    for k, v in enumerate(it, 2):
        if v <= prev:
            return k * 100 + prev
        prev = v
    return 0

L = lambda v: [v, None, None]
T = [40, [25, L(10), [32, L(28), L(43)]], [60, L(45), L(70)]]
print(check(T))''',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            25,
                            [10],
                            [
                                32,
                                [28],
                                [43],
                            ],
                        ],
                        [
                            60,
                            [45],
                            [70],
                        ],
                    ],
                    'caption': 'Tree T',
                },
            ],
            'answer': '643',
            'solution': '''`inorder` is a recursive generator: `yield from` forwards every value of the sub-generator, so values come out in in-order sequence, one at a time. `check` looks for the first place where the sequence is not strictly increasing, i.e. where T fails to be a BST.

In-order sequence of T: 10, 25, 28, 32, **43**, **40**, 45, 60, 70.

- `prev = next(it)` consumes 10 (position 1).
- `enumerate(it, 2)` numbers the *remaining* values starting at 2: 25→2, 28→3, 32→4, 43→5, 40→6.
- At k = 6, v = 40 ≤ prev = 43 → return 6 × 100 + 43 = **643**.

The violation exists because 43 is in the **left** subtree of 40 yet larger than 40 — every parent–child pair is locally fine (32 < 43), which is why checking only children is not enough to validate a BST.

**Trap:** starting the count at 1 for the remaining values (giving 543) or returning v instead of prev (giving 640).''',
            'verify': '''
seq = list(inorder(T))
k = next(i for i in range(1, len(seq)) if seq[i] <= seq[i-1])
assert (k + 1) * 100 + seq[k-1] == int(ANSWER) and OUTPUT.strip() == ANSWER
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Iterator vs iterable classes',
            'text': 'Consider the following Python program. Which of the following statements about its output is/are TRUE?',
            'code': '''class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n

class Down:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        k = self.n
        while k > 0:
            k -= 1
            yield k

c, r = Countdown(3), Down(3)
print(list(c), list(c))
print(list(r), list(r))
print(list(zip(r, r)))
print(sum(c), max(r))''',
            'options': [
                'Line 1 is `[2, 1, 0] []`',
                'Line 2 is `[2, 1, 0] []`',
                'Line 3 is `[(2, 2), (1, 1), (0, 0)]`',
                'Line 4 is `0 2`',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''`Countdown` is an **iterator**: `__iter__` returns `self`, so all loops share one cursor (`self.n`) and it can be consumed only once. `Down` is an **iterable**: its `__iter__` is a generator function, so each call to `iter(r)` returns a **fresh** generator with its own `k`; `self.n` is never modified.

- Line 1: the first `list(c)` gives 2, 1, 0 and leaves n = 0; the second gets nothing → `[2, 1, 0] []`. (A) **True.**
- Line 2: each `list(r)` gets a new generator → `[2, 1, 0] [2, 1, 0]`. (B) **False.**
- Line 3: `zip(r, r)` calls `iter(r)` twice → two independent generators advancing in step → `[(2, 2), (1, 1), (0, 0)]`. (C) **True.** (Contrast with zip on a single shared iterator, which would pair consecutive items.)
- Line 4: `c` is exhausted → `sum(c)` = 0; `max(r)` uses a fresh generator → 2. (D) **True.**

**Trap:** assuming every class with `__iter__` behaves like a list. Whether re-iteration works depends on whether `__iter__` returns `self` or a new iterator.''',
            'verify': '''
lines = OUTPUT.strip().split('\\n')
assert lines[0] == '[2, 1, 0] []' and lines[1] != '[2, 1, 0] []'
assert lines[2] == '[(2, 2), (1, 1), (0, 0)]' and lines[3] == '0 2'
assert sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linked list mutated during generator traversal',
            'text': 'A singly linked list `head → 5 → 3 → 8 → 2 → 1 → 9 → 4` is processed by the program below. The value printed is ______.',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def nodes(h):
    while h:
        yield h
        h = h.next

head = None
for v in reversed([5, 3, 8, 2, 1, 9, 4]):
    head = Node(v, head)

for n in nodes(head):
    if n.next and n.val > n.next.val:
        n.next = n.next.next

print(''.join(str(n.val) for n in nodes(head)))''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [5, 3, 8, 2, 1, 9, 4],
                    'head': 'head',
                    'caption': 'Initial list',
                },
            ],
            'answer': '5819',
            'solution': '''The generator yields a node and, **when resumed**, reads `h.next` — *after* the loop body has possibly modified that pointer. So a bypassed node is never visited, and the scan continues from the new successor.

- n = 5: next is 3, 5 > 3 → 5.next = 8. Generator resumes: h = 5.next = **8**.
- n = 8: next is 2, 8 > 2 → 8.next = 1. Next h = **1**.
- n = 1: next is 9, 1 < 9 → no change. Next h = **9**.
- n = 9: next is 4, 9 > 4 → 9.next = None. Next h = None → generator ends.

Final list 5 → 8 → 1 → 9; the print joins the values → `5819`.

Note that 8 > 1 was never re-examined after 2 was removed — each node is compared only once, so the result is not “remove every element smaller than its predecessor in the final list”.

**Trap:** if the generator had saved `nxt = h.next` *before* yielding, it would visit the removed nodes 3 and 2 too, but the printed list would still be built from the live links.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [5, 8, 1, 9],
                    'head': 'head',
                    'caption': 'List after the loop',
                },
            ],
            'verify': '''
# array simulation: compare a[i] with its current successor once, then move on
a = [5, 3, 8, 2, 1, 9, 4]; i = 0
while i < len(a) - 1:
    if a[i] > a[i+1]: a.pop(i+1)
    i += 1
assert OUTPUT.strip() == ANSWER == ''.join(map(str, a))
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — comparison count',
            'text': 'Top-down merge sort (split at m = ⌊n/2⌋, left part A[0..m−1]) sorts `[7, 2, 9, 4, 3, 8, 6, 1]`. The merge step compares the heads of the two runs and stops comparing as soon as one run is exhausted. The total number of key comparisons over all merges is ______.',
            'answer': '17',
            'solution': '''Merge sort on 8 keys has three levels of merges. Count comparisons per merge (a merge of runs of sizes p and q costs p + q − (elements copied after one run empties)).

**Level 1** (pairs): [7|2], [9|4], [3|8], [6|1] → 1 comparison each → 4. Runs: [2,7] [4,9] [3,8] [1,6].

**Level 2:**

- [2,7] + [4,9]: 2<4, 7>4, 7<9 → left empty, copy 9 → **3** → [2,4,7,9]
- [3,8] + [1,6]: 3>1, 3<6, 8>6 → right empty, copy 8 → **3** → [1,3,6,8]

**Level 3:** [2,4,7,9] + [1,3,6,8]: 2>1, 2<3, 4>3, 4<6, 7>6, 7<8, 9>8 → right empty, copy 9 → **7**.

Total = 4 + 3 + 3 + 7 = **17**.

Bounds check: for n = 8 merge sort uses between 12 (= (n/2)·log₂ n) and 17 (= n log₂ n − n + 1) comparisons. This input is a worst case: in every merge the last two output elements come from different runs.

**Trap:** counting p + q comparisons per merge (giving 24) or omitting the level-1 merges.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Runs after each merge level',
                    'col_labels': ['runs', 'comparisons'],
                    'row_labels': ['start', 'level 1', 'level 2', 'level 3'],
                    'rows': [
                        ['7 2 9 4 3 8 6 1', '–'],
                        ['2 7 | 4 9 | 3 8 | 1 6', '4'],
                        ['2 4 7 9 | 1 3 6 8', '3 + 3'],
                        ['1 2 3 4 6 7 8 9', '7'],
                    ],
                },
            ],
            'verify': '''
cnt = 0
def ms(a):
    global cnt
    if len(a) <= 1: return a
    m = len(a) // 2; L = ms(a[:m]); R = ms(a[m:]); out = []; i = j = 0
    while i < len(L) and j < len(R):
        cnt += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
assert ms([7, 2, 9, 4, 3, 8, 6, 1]) == [1, 2, 3, 4, 6, 7, 8, 9] and cnt == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Frontier-based BFS with set comprehensions',
            'text': 'The program below performs a level-by-level BFS from A on the directed graph shown. Which of the following statements is/are TRUE?',
            'code': '''G = {'A': 'BC', 'B': 'D', 'C': 'DE', 'D': 'FB',
     'E': 'FA', 'F': 'G', 'G': 'C'}
seen = {'A'}
frontier = {'A'}
levels = []
while frontier:
    levels.append(''.join(sorted(frontier)))
    frontier = {v for u in frontier for v in G[u]} - seen
    seen |= frontier
print(levels)''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['C', 'D'],
                        ['C', 'E'],
                        ['D', 'F'],
                        ['D', 'B'],
                        ['E', 'F'],
                        ['E', 'A'],
                        ['F', 'G'],
                        ['G', 'C'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.6, 2.2],
                        'C': [1.6, -0.2],
                        'D': [3.2, 2.2],
                        'E': [3.2, -0.2],
                        'F': [4.8, 1],
                        'G': [3.2, 1],
                    },
                },
            ],
            'options': [
                'Exactly 5 strings are printed in the list',
                "The string at index 2 of `levels` is `'DE'`",
                '`G` appears in the string at index 3 of `levels`',
                'If the statement `seen |= frontier` were deleted, the loop would never terminate',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Each iteration replaces the frontier by all out-neighbours of the current frontier that have never been seen — exactly the next BFS level.

- Level 0: {A}
- Level 1: neighbours {B, C} − {A} → `'BC'`; seen = {A, B, C}
- Level 2: B→D; C→D, E → {D, E} → `'DE'`; seen adds D, E
- Level 3: D→F, B; E→F, A → {F, B, A} − seen = {F} → `'F'`
- Level 4: F→G → `'G'`
- Next: G→C, already seen → empty set → loop ends.

Printed: `['A', 'BC', 'DE', 'F', 'G']`.

- (A) **True** — 5 levels.
- (B) **True.**
- (C) **False** — G is at index 4 (distance 4 from A); index 3 is `'F'`.
- (D) **True** — without updating `seen`, only A is ever excluded. The cycle C → D → F → G → C never involves A, so the frontier keeps cycling (e.g. … {G} → {C} → {D, E} → {F, B} → …) and never becomes empty.

**Trap:** thinking the `- seen` alone guarantees termination; it only works if `seen` grows.''',
            'verify': '''
assert levels == ['A', 'BC', 'DE', 'F', 'G']
seen2 = {'A'}; fr = {'A'}; it = 0
while fr and it < 200:
    fr = {v for u in fr for v in G[u]} - seen2; it += 1
assert fr and it == 200
assert sorted(ANSWER) == ['A', 'B', 'D']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort with comprehensions — call count',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''calls = 0
def qs(a):
    global calls
    calls += 1
    if len(a) <= 1:
        return a
    p = a[0]
    lo = [x for x in a[1:] if x < p]
    hi = [x for x in a[1:] if x >= p]
    return qs(lo) + [p] + qs(hi)

qs([5, 3, 8, 1, 9, 2, 7])
print(calls)''',
            'answer': '9',
            'solution': '''Every call with ≥ 2 elements makes exactly two recursive calls (one possibly on an empty list); calls on lists of length 0 or 1 are leaves. So calls = 2 × (internal calls) + 1.

Recursion tree (pivot = first element):

- qs([5,3,8,1,9,2,7]) → lo = [3,1,2], hi = [8,9,7]
- qs([3,1,2]) → lo = [1,2], hi = []
- qs([1,2]) → lo = [], hi = [2]
- qs([]), qs([2]) — leaves
- qs([]) (hi of 3) — leaf
- qs([8,9,7]) → lo = [7], hi = [9]
- qs([7]), qs([9]) — leaves

Internal calls: [5,…], [3,1,2], [1,2], [8,9,7] → 4. Total calls = 2 × 4 + 1 = **9**.

**Trap:** forgetting the calls on empty lists (which still increment `calls`) gives 6. Note: this version is not in-place — each level builds new lists, using Θ(n) extra memory per level.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'All calls in the order they are made',
                    'col_labels': ['argument', 'pivot', 'lo', 'hi'],
                    'row_labels': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                    'rows': [
                        ['5 3 8 1 9 2 7', 5, '3 1 2', '8 9 7'],
                        ['3 1 2', 3, '1 2', '–'],
                        ['1 2', 1, '–', '2'],
                        ['–', '', '', ''],
                        ['2', '', '', ''],
                        ['–', '', '', ''],
                        ['8 9 7', 8, '7', '9'],
                        ['7', '', '', ''],
                        ['9', '', '', ''],
                    ],
                },
            ],
            'verify': '''
def count(a):
    if len(a) <= 1: return 1
    p = a[0]
    return 1 + count([x for x in a[1:] if x < p]) + count([x for x in a[1:] if x >= p])
assert count([5, 3, 8, 1, 9, 2, 7]) == calls == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Counting shortest paths with BFS',
            'text': 'In the unweighted undirected graph shown, the number of distinct shortest paths from S to T is',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['A', 'C'],
                        ['B', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['E', 'F'],
                        ['D', 'G'],
                        ['F', 'T'],
                        ['G', 'T'],
                        ['E', 'H'],
                        ['H', 'T'],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2],
                        'B': [1.5, 0],
                        'C': [3, 1],
                        'D': [3, 2.8],
                        'E': [3, -0.8],
                        'F': [4.5, 1],
                        'G': [5.2, 2.8],
                        'H': [5.2, -0.8],
                        'T': [6.5, 1],
                    },
                },
            ],
            'options': ['4', '6', '5', '8'],
            'answer': 'B',
            'solution': '''Run BFS from S and propagate counts: paths(v) = ∑ paths(u) over neighbours u with dist(u) = dist(v) − 1.

- dist 0: S (1 path)
- dist 1: A (1), B (1)
- dist 2: C from A and B → 2; D from A → 1; E from B → 1
- dist 3: F from C, D, E → 2 + 1 + 1 = 4; G from D → 1; H from E → 1
- dist 4: T from F, G, H → 4 + 1 + 1 = **6**

So the shortest distance is 4 and there are **6** shortest paths.

- (A) 4 counts only the paths through F.
- (C) 5 misses one of the two routes into C.
- (D) 8 adds paths of length 5 or counts edges D–F/E–F twice.

**Trap:** only predecessors **one level closer** contribute; edges inside a level or going back do not.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS distance and number of shortest paths',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'row_labels': ['dist', '#paths'],
                    'rows': [
                        [0, 1, 1, 2, 2, 2, 3, 3, 3, 4],
                        [1, 1, 1, 2, 1, 1, 4, 1, 1, 6],
                    ],
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

from collections import deque
E = [('S','A'),('S','B'),('A','C'),('B','C'),('A','D'),('B','E'),('C','F'),('D','F'),
     ('E','F'),('D','G'),('F','T'),('G','T'),('E','H'),('H','T')]
adj = {}
for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
d = {'S': 0}; c = {'S': 1}; q = deque('S')
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in d: d[v] = d[u] + 1; c[v] = 0; q.append(v)
        if d[v] == d[u] + 1: c[v] += c[u]
assert d['T'] == 4 and ['4','5','6','8'][ord(ANSWER) - 65] == str(c['T'])
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Complexity of a generator expression',
            'text': '''Consider the Python expression below, where n is a positive integer. The number of items produced by the generator (and hence the value of `count`) grows as

`count = sum(1 for i in range(n) for j in range(i, n, i + 1))`''',
            'options': ['Θ(n)', 'Θ(n²)', 'Θ(n √n)', 'Θ(n log n)'],
            'answer': 'D',
            'solution': '''For a fixed i, `range(i, n, i + 1)` has ⌈(n − i)/(i + 1)⌉ elements. Summing over i:

count = ∑_{i=0}^{n−1} ⌈(n − i)/(i + 1)⌉ ≈ ∑_{k=1}^{n} (n + 1 − k)/k = (n + 1)·H_{n} − n,

where k = i + 1 and H_{n} = 1 + 1/2 + … + 1/n ≈ ln n. Hence count = Θ(n log n).

Numerical check: n = 12 gives count = 35; n = 1000 gives 7069 ≈ 1.02 · n ln n; n = 10000 gives 93668 ≈ 1.02 · n ln n — the ratio to n ln n stays constant.

- (A) Θ(n) would hold only if the inner loop did O(1) work on average.
- (B) Θ(n²) ignores the growing step — that would be the cost with step 1.
- (C) Θ(n√n) would come from step sizes like √n, not i + 1.

**Tip:** an inner loop with step i (or i + 1) is the harmonic-series pattern, as in the sieve of Eratosthenes.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

import math
def cnt(n): return sum(1 for i in range(n) for j in range(i, n, i + 1))
assert cnt(12) == 35
r = [cnt(n) / (n * math.log(n)) for n in (1000, 4000, 16000)]
assert max(r) - min(r) < 0.05 and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Dict/set comprehensions and stable sorting',
            'text': "Let `words = ['kiwi', 'fig', 'apple', 'date', 'plum', 'pear', 'banana']`. Which of the following expressions evaluate to `True`?",
            'options': [
                "`{len(w): w for w in words}[4] == 'pear'`",
                "`sorted(words, key=len)[1] == 'kiwi'`",
                '`len({w[0] for w in words}) == 7`',
                "`sorted(words, key=lambda w: (-len(w), w))[2] == 'date'`",
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''- (A) In a dict comprehension a repeated key is **overwritten**; the last word of length 4 in the list is 'pear' (kiwi, date, plum, pear in order). **True.**
- (B) `sorted` is **stable**: equal keys keep their original relative order. By length: fig(3), then kiwi, date, plum, pear (4, original order), apple(5), banana(6). Index 1 is 'kiwi'. **True.**
- (C) First letters: k, f, a, d, p, p, b → as a set {k, f, a, d, p, b} has **6** elements. **False.**
- (D) Key (−len, word): longest first, ties alphabetical → banana, apple, date, kiwi, pear, plum, fig. Index 2 is 'date'. **True.**

**Trap:** in (A) assuming the *first* occurrence wins (it would give 'kiwi'); in (C) forgetting that sets drop duplicates; in (D) applying stability instead of the secondary key — the tuple key makes the original order irrelevant.''',
            'verify': '''
words = ['kiwi', 'fig', 'apple', 'date', 'plum', 'pear', 'banana']
vals = [{len(w): w for w in words}[4] == 'pear',
        sorted(words, key=len)[1] == 'kiwi',
        len({w[0] for w in words}) == 7,
        sorted(words, key=lambda w: (-len(w), w))[2] == 'date']
assert [L for L, v in zip('ABCD', vals) if v] == sorted(ANSWER)
''',
        },
    ],
}
