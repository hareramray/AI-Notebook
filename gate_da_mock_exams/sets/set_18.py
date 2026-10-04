# Set 18 — Scoping, Closures, OOP & Exceptions (GATE-level)
SET = {
    'number': 18,
    'title': 'Scoping, Closures, OOP & Exceptions',
    'difficulty': 'GATE-level',
    'focus': 'LEGB, global/nonlocal, closures, classes, try/except/finally',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — closures and enclosing scope',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''x = 'g'

def outer():
    x = 'e'
    def inner():
        return x
    x = 'e2'
    return inner

f = outer()
print(f(), x)''',
            'options': ['`e2 g`', '`e g`', '`g g`', '`e2 e2`'],
            'answer': 'A',
            'solution': '''Name resolution follows **LEGB** (Local, Enclosing, Global, Built-in), and a closure captures the enclosing *variable* (a cell), not the value it had when `inner` was defined.

- Inside `outer`, `x` is local because it is assigned there. `inner` does not assign `x`, so its `x` refers to `outer`'s cell.
- After `def inner`, `outer` rebinds that cell to `'e2'` and returns `inner`.
- Calling `f()` reads the cell at call time → `'e2'`.
- The module-level `x` was never touched → `'g'`.

Output `e2 g` → option **(A)**.

- (B) assumes the value is frozen at definition time (*early binding*).
- (C) assumes `inner` skips the enclosing scope and reads the global.
- (D) assumes assignments in `outer` leak into the global scope (they would only with a `global x` declaration).

**Tip:** closures bind late; to freeze a value use a default argument (`def inner(x=x)`).''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'e2 g' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — late binding in lambdas',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''fs = [lambda: i * i for i in range(4)]
gs = [lambda i=i: i * i for i in range(4)]
print(sum(f() for f in fs) + sum(g() for g in gs))''',
            'answer': '50',
            'solution': '''All lambdas in `fs` close over the **same** variable `i` of the comprehension's scope. They are called only after the comprehension has finished, when `i` = 3.

- Each `f()` returns 3 × 3 = 9; four of them sum to **36**.
- In `gs`, `i=i` is a default parameter, evaluated **when each lambda is created**, so the lambdas remember 0, 1, 2, 3 → 0 + 1 + 4 + 9 = **14**.

Printed value: 36 + 14 = **50**.

**Trap:** answering 28 (14 + 14) by assuming the loop variable is captured per iteration. In Python a closure stores a reference to the variable's cell; only default-argument values are evaluated eagerly. (Note: the comprehension variable does not leak to module scope in Python 3, but it still lives on in the closures' cell.)''',
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — try / except / finally with return',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def f():
    try:
        return 'try'
    finally:
        print('fin', end=' ')

def g():
    try:
        raise ValueError
    except ValueError:
        return 1
    finally:
        return 2

print(f(), g())''',
            'options': ['`try fin 2`', '`try 1 fin`', '`fin try 1`', '`fin try 2`'],
            'answer': 'D',
            'solution': '''A `finally` block always runs when control leaves the `try` statement — even via `return` — and a `return` inside `finally` **overrides** any pending return value or exception.

Evaluation of `print(f(), g())`:
- The arguments are evaluated first. `f()`: `return 'try'` is pending; `finally` prints `fin ` immediately; then `'try'` is returned.
- `g()`: `ValueError` is caught, `return 1` is pending; `finally` executes `return 2`, which replaces it → 2.
- Only now does the outer `print` run, writing `try 2`.

Full output: `fin try 2` → option **(D)**.

- (A) assumes `print` emits `f()`'s value before `f`'s own side effect.
- (B) gets both the order and the value wrong.
- (C) forgets that `return` in `finally` wins.

**Trap:** side effects inside argument evaluation happen *before* the enclosing call prints anything.''',
            'verify': "ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'fin try 2' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — class vs instance attributes',
            'text': 'Consider the following Python code. Which of the following statements is/are TRUE immediately after it runs (each statement is evaluated independently, starting from the state after the last line shown)?',
            'code': '''class C:
    items = []
    count = 0
    def __init__(self, v):
        self.items.append(v)
        self.count += 1

a = C(1)
b = C(2)''',
            'options': [
                '`a.items is b.items` evaluates to `True`',
                '`C.count == 0` evaluates to `True`',
                '`a.count == 2` evaluates to `True`',
                'After executing `a.items = [9]`, the expression `len(b.items) == 2` is `True`',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Attribute *lookup* searches the instance, then the class; attribute *assignment* (`self.x = …`, including augmented `self.x += …`) always writes to the instance.

- `self.items.append(v)` looks up `items` (found on the class) and **mutates** the one shared list → `C.items == [1, 2]`.
- `self.count += 1` means `self.count = self.count + 1`: it reads `C.count` (0) and **creates an instance attribute** `count = 1`. The class attribute stays 0.

Statements:
- (A) Both names resolve to the class list. **True.**
- (B) The class's `count` was never reassigned. **True.**
- (C) Each instance has its own `count == 1`. **False.**
- (D) `a.items = [9]` creates an instance attribute on `a` only; `b.items` is still the class list `[1, 2]`. **True.**

**Trap:** treating `+=` on an immutable class attribute like `append` on a mutable one — the former rebinds on the instance, the latter mutates the shared object.''',
            'verify': '''
r = {'A': a.items is b.items, 'B': C.count == 0, 'C': a.count == 2}
a.items = [9]
r['D'] = len(b.items) == 2
assert sorted(k for k, v in r.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Queues — queue using two stacks',
            'text': '''A queue is implemented with two stacks IN and OUT. `enqueue(x)` pushes x onto IN. `dequeue()` pops from OUT; if OUT is empty it first pops **every** element of IN and pushes it onto OUT (each such pop–push pair is one *transfer*).

Starting empty, the operations are:
enqueue 1, 2, 3, 4, 5; dequeue; dequeue; enqueue 6, 7; dequeue ×4.
The total number of transfers performed is ______.''',
            'answer': '7',
            'solution': '''Each element is transferred at most once (IN → OUT), which is why the two-stack queue has O(1) amortised cost per operation.

- enqueue 1–5: IN = [1, 2, 3, 4, 5] (bottom→top), OUT empty.
- dequeue #1: OUT empty → transfer 5 elements → OUT = [5, 4, 3, 2, 1]; pop 1. Transfers = **5**.
- dequeue #2: pop 2 from OUT (no transfer).
- enqueue 6, 7: IN = [6, 7].
- dequeue #3, #4, #5: pop 3, 4, 5 from OUT (OUT becomes empty).
- dequeue #6: OUT empty → transfer 7 then 6 → OUT = [7, 6]; pop 6. Transfers += **2**.

Total transfers = 5 + 2 = **7**; the dequeued sequence 1, 2, 3, 4, 5, 6 is correct FIFO order.

**Trap:** transferring on *every* dequeue (or moving elements back to IN after each dequeue) gives a much larger count and is the naive O(n)-per-operation design.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [5, 4, 3, 2, 1],
                    'label': 'OUT',
                    'caption': 'OUT just after the first transfer (top = 1)',
                },
            ],
            'verify': '''
IN, OUT, t, got = [], [], 0, []
def enq(x): IN.append(x)
def deq():
    global t
    if not OUT:
        while IN: OUT.append(IN.pop()); t += 1
    return OUT.pop()
for x in [1,2,3,4,5]: enq(x)
got += [deq(), deq()]
enq(6); enq(7)
got += [deq() for _ in range(4)]
assert got == [1,2,3,4,5,6] and t == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'BST — preorder to postorder',
            'text': '''The pre-order traversal of a binary search tree with distinct keys is
52, 31, 17, 44, 38, 49, 70, 63, 88, 91.
What is its post-order traversal?''',
            'options': [
                '17, 38, 49, 44, 31, 63, 88, 91, 70, 52',
                '17, 31, 38, 44, 49, 52, 63, 70, 88, 91',
                '17, 38, 49, 44, 31, 63, 91, 88, 70, 52',
                '17, 49, 38, 44, 31, 63, 91, 88, 70, 52',
            ],
            'answer': 'C',
            'solution': '''In a BST, the pre-order sequence determines the tree: the first key is the root, the following keys smaller than it form the left subtree's pre-order, the rest the right subtree's.

- Root 52; left part 31, 17, 44, 38, 49; right part 70, 63, 88, 91.
- Left subtree: root 31, left {17}, right 44 with children 38 and 49.
- Right subtree: root 70, left {63}, right 88 whose right child is 91.

Post-order (left, right, root):
- left subtree: 17, 38, 49, 44, 31
- right subtree: 63, 91, 88, 70
- root: 52

→ 17, 38, 49, 44, 31, 63, 91, 88, 70, 52 → option **(C)**.

- (A) visits 88 before its child 91 — 91 is the *right child* of 88, so it must come first.
- (B) is the in-order (sorted) sequence.
- (D) swaps 38 and 49, i.e. visits the right child of 44 before the left.

**Tip:** post-order always ends with the root, and every node appears after all its descendants.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        52,
                        [
                            31,
                            [17],
                            [
                                44,
                                [38],
                                [49],
                            ],
                        ],
                        [
                            70,
                            [63],
                            [
                                88,
                                None,
                                [91],
                            ],
                        ],
                    ],
                    'caption': 'BST reconstructed from the pre-order',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in [52,31,17,44,38,49,70,63,88,91]: T = ins(T, k)
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
assert post(T) == [17,38,49,44,31,63,91,88,70,52] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Selection sort — swaps',
            'text': 'Selection sort (ascending) is applied to [8, 21, 5, 34, 40, 13, 55, 47]. In pass i (i = 0, 1, …, n−2) it finds the index m of the minimum of a[i..n−1] and swaps a[i] with a[m] **only if m ≠ i**. The number of swaps performed is ______.',
            'answer': '6',
            'solution': '''Selection sort makes at most n − 1 = 7 swaps; a pass is skipped when the minimum of the unsorted suffix is already in place.

- i=0: min 5 at 2 → swap → [5, 21, 8, 34, 40, 13, 55, 47]
- i=1: min 8 at 2 → swap → [5, 8, 21, 34, 40, 13, 55, 47]
- i=2: min 13 at 5 → swap → [5, 8, 13, 34, 40, 21, 55, 47]
- i=3: min 21 at 5 → swap → [5, 8, 13, 21, 40, 34, 55, 47]
- i=4: min 34 at 5 → swap → [5, 8, 13, 21, 34, 40, 55, 47]
- i=5: min 40 at 5 → **no swap**
- i=6: min 47 at 7 → swap → sorted.

Total = **6** swaps.

**Trap:** answering n − 1 = 7 automatically. Note how 40 reached its final place as a side-effect of the i = 4 swap. The number of *comparisons*, by contrast, is always n(n−1)/2 = 28, independent of the input.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', 'swap?'],
                    'row_labels': ['start', 'i=0', 'i=1', 'i=2', 'i=3', 'i=4', 'i=5', 'i=6'],
                    'rows': [
                        [8, 21, 5, 34, 40, 13, 55, 47, '-'],
                        [5, 21, 8, 34, 40, 13, 55, 47, 'yes'],
                        [5, 8, 21, 34, 40, 13, 55, 47, 'yes'],
                        [5, 8, 13, 34, 40, 21, 55, 47, 'yes'],
                        [5, 8, 13, 21, 40, 34, 55, 47, 'yes'],
                        [5, 8, 13, 21, 34, 40, 55, 47, 'yes'],
                        [5, 8, 13, 21, 34, 40, 55, 47, 'no'],
                        [5, 8, 13, 21, 34, 40, 47, 55, 'yes'],
                    ],
                    'highlight': [
                        [6, 8],
                    ],
                },
            ],
            'verify': '''
a = [8,21,5,34,40,13,55,47]; s = 0
for i in range(len(a)-1):
    m = min(range(i, len(a)), key=lambda j: a[j])
    if m != i: a[i], a[m] = a[m], a[i]; s += 1
assert s == int(ANSWER) and a == sorted(a)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — exception hierarchy and clause order',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''log = []

def f(d, k):
    try:
        d[k] += 1
    except LookupError:
        return 'L'
    except KeyError:
        return 'K'
    else:
        return 'E'
    finally:
        log.append(k)

r = f({'a': 1}, 'a') + f({'a': 1}, 'b') + f([], 0)
print(r, len(log))''',
            'options': ['`EKL 3`', '`ELL 3`', '`ELL 2`', '`EKL 2`'],
            'answer': 'B',
            'solution': '''`except` clauses are tried **top to bottom** and the first one whose class matches (including base classes) wins. `KeyError` and `IndexError` are both subclasses of `LookupError`.

- `f({'a':1}, 'a')`: no exception → `else` returns `'E'`; `finally` logs.
- `f({'a':1}, 'b')`: `d['b']` raises `KeyError` → caught by the *first* clause `except LookupError` → `'L'`. The `except KeyError` clause is unreachable.
- `f([], 0)`: `[][0]` raises `IndexError` → also a `LookupError` → `'L'`.
- `finally` runs in every call → `log` has 3 entries.

`r = 'E' + 'L' + 'L'` → output `ELL 3` → option **(B)**.

- (A)/(D) assume the more specific `KeyError` clause is preferred — Python does not look for the best match, only the first.
- (C)/(D) assume `finally` is skipped when `return` executes in `except`/`else`.

**Tip:** always order `except` clauses from most specific to most general.''',
            'verify': "assert OUTPUT.strip() == 'ELL 3' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph traversal — DFS orders',
            'text': 'Recursive depth-first search is started at A on the directed graph shown. The out-neighbours of a vertex may be explored in **any** order. Which of the following is/are possible orders in which vertices are first visited?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'E'],
                    ],
                    'pos': {
                        'A': [2, 3],
                        'B': [1, 2],
                        'C': [3, 2],
                        'D': [0, 1],
                        'E': [2, 1],
                        'F': [4, 1],
                        'G': [1, 0],
                    },
                },
            ],
            'options': [
                'A, B, D, G, E, C, F',
                'A, C, F, E, G, B, D',
                'A, B, D, E, G, C, F',
                'A, C, E, F, G, B, D',
            ],
            'answer': ['A', 'B'],
            'solution': '''In DFS, after visiting v the search must explore **all** vertices reachable from v through unvisited vertices before backtracking. So in a valid order, the vertex after v must be an unvisited out-neighbour of v if one exists; otherwise of the nearest ancestor that still has one.

- (A) A→B→D→G (G has no out-edges; D done) → back to B → E (G already seen) → back to A → C → F (E seen). **Possible.**
- (B) A→C→F→E→G → back to C (E seen) → back to A → B → D (G seen). **Possible.**
- (C) After D, its out-neighbour G is still unvisited, so G must be next; jumping to E is **impossible.**
- (D) After E, G is an unvisited out-neighbour of E, so G must come before backtracking to C for F. **Impossible.**

**Trap:** treating DFS like 'any order that respects edges'. The rule is stricter: you can only move to a neighbour of the *current* vertex or backtrack.''',
            'verify': '''
G = {'A':'BC','B':'DE','C':'EF','D':'G','E':'G','F':'E','G':''}
def all_dfs(u, seen):
    seen = seen | {u}
    def visit(order, seen, nb):
        if not nb:
            yield order, seen; return
        for i, v in enumerate(nb):
            rest = nb[:i] + nb[i+1:]
            if v in seen:
                yield from visit(order, seen, rest)
            else:
                for o2, s2 in all_dfs(v, seen):
                    yield from visit(order + o2, s2, rest)
    yield from visit([u], seen, G[u])
valid = {''.join(o) for o, s in all_dfs('A', set())}
opts = {'A':'ABDGECF','B':'ACFEGBD','C':'ABDEGCF','D':'ACEFGBD'}
assert sorted(k for k, v in opts.items() if v in valid) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — comparison distribution',
            'text': 'Iterative binary search with mid = ⌊(lo + hi)/2⌋ is performed on a sorted array of 100 distinct keys (indices 0–99). Each iteration compares the key with a[mid] once (a three-way comparison counts as one). Among the 100 keys present in the array, the number that are found after **exactly 7** iterations is ______.',
            'answer': '37',
            'solution': '''The probes of binary search form a *decision tree*: the root is the first mid, its children are the mids of the two halves, and so on. A key at depth d (root depth 1) is found after exactly d iterations.

The decision tree for n keys is as balanced as possible (half sizes differ by at most one), so levels fill completely from the top:
- depth 1: 1 key, depth 2: 2, depth 3: 4, depth 4: 8, depth 5: 16, depth 6: 32 — that is 63 keys in total (2⁶ − 1).
- The remaining 100 − 63 = **37** keys sit at depth 7 (which could hold up to 64).

So 37 keys need exactly 7 iterations, and no key needs more (⌊log₂ 100⌋ + 1 = 7).

**Trap:** answering 64 (capacity of level 7) or 36 (miscounting the first six levels as 64 keys).''',
            'verify': '''
from collections import Counter
c = Counter()
for x in range(100):
    lo, hi, k = 0, 99, 0
    while True:
        mid = (lo + hi) // 2; k += 1
        if mid == x: break
        if mid < x: lo = mid + 1
        else: hi = mid - 1
    c[k] += 1
assert c[7] == int(ANSWER) and max(c) == 7
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — nonlocal and closure state',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def make():
    n = 0
    def inc(k=1):
        nonlocal n
        n += k
        return n
    return inc

a = make()
b = make()
a(); a(5); b(2)
c = a
c(10)
print(a(), b())''',
            'options': ['`17 3`', '`7 3`', '`17 13`', '`1 1`'],
            'answer': 'A',
            'solution': '''Each call of `make()` creates a **new** frame and hence a new cell for `n`; `inc` closes over that cell and `nonlocal n` lets it rebind it. Assigning `c = a` copies the *reference* to the same function object, not its state.

Trace of the two independent counters:
- `a()` → a's n = 1
- `a(5)` → a's n = 6
- `b(2)` → b's n = 2
- `c(10)` → c *is* a → a's n = 16
- `a()` → a's n = 17 (printed first)
- `b()` → b's n = 3 (printed second)

Output `17 3` → option **(A)**.

- (B) treats `c` as an independent copy, so `c(10)` would not affect `a`.
- (C) assumes `a` and `b` share one counter (as they would with a module-level `global n`).
- (D) assumes every call starts again from n = 0, as if `n` were a local of `inc` (in fact, without `nonlocal`, `n += k` would raise `UnboundLocalError`).

**Tip:** function objects are ordinary objects — aliasing them aliases their closure cells too.''',
            'verify': "assert OUTPUT.strip() == '17 3' and ANSWER == 'A'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — inheritance, MRO and super()',
            'text': 'Consider the following class definitions. Which of the following statements is/are TRUE?',
            'code': '''class A:
    def __init__(self):
        self.v = 1
    def f(self):
        return self.v

class B(A):
    def __init__(self):
        super().__init__()
        self.v += 10
    def f(self):
        return 2 * super().f()

class C(A):
    def f(self):
        return self.v + 100

class D(B, C):
    pass''',
            'options': [
                'The method resolution order of D is D, B, C, A, object',
                '`D().f()` returns 222',
                '`D().v` equals 1, because `C` has no `__init__` and so `A.__init__` is called last and resets v',
                '`B().f()` returns 22',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Python linearises the class hierarchy with **C3**; `super()` means 'the next class after the current one in the MRO of the *instance's* class', not 'my parent'.

- (A) D(B, C) with B(A), C(A): MRO = D, B, C, A, object. **True.**

- (B) `D()` runs `B.__init__` (first in MRO with `__init__`). Its `super()` → next after B in D's MRO is C; C has no `__init__`, so lookup continues to A → v = 1. Back in B: v += 10 → v = 11. `D().f()` → `B.f` → `2 * super().f()`; super of B in D's MRO is **C**, so `C.f` returns 11 + 100 = 111 → result 222. **True.**

- (C) As traced, `A.__init__` runs *inside* `B.__init__`, before `+= 10`; v = 11. **False.**

- (D) For a plain `B()`, the MRO is B, A, object: v = 1 + 10 = 11, `B.f` → 2 × `A.f()` = 22. **True.**

**Trap:** assuming `super().f()` inside B always calls `A.f`. In a diamond, the same line of code dispatches to `C.f` for a D instance but to `A.f` for a B instance — so `D().f()` is 222, not 22.''',
            'verify': '''
truth = {'A': [k.__name__ for k in D.__mro__] == ['D','B','C','A','object'],
         'B': D().f() == 222, 'C': D().v == 1, 'D': B().f() == 22}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — finally with break/continue and loop-else',
            'text': 'Consider the following Python function. Which of the following statements is/are TRUE?',
            'code': '''def risky(n):
    log = []
    for i in range(n):
        try:
            if i % 3 == 2:
                raise KeyError(i)
            if i == 4:
                break
            log.append(i)
        except KeyError:
            log.append(-i)
            continue
        finally:
            log.append('f')
    else:
        log.append('E')
    return log''',
            'options': [
                '`len(risky(4))` is 9',
                "`risky(6)` ends with `'E'`",
                "`risky(6).count('f')` is 5",
                '`-2` appears in both `risky(4)` and `risky(6)`',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Key rules: (1) `finally` runs whenever control leaves the `try` — normally, via `continue`, via `break`, or via an exception; (2) a loop's `else` runs only if the loop ends **without** `break`.

`risky(4)` (i = 0..3):
- i=0: append 0, finally 'f'
- i=1: append 1, 'f'
- i=2: KeyError → append −2, `continue` → finally 'f' still runs
- i=3: append 3, 'f'
- loop exhausted → else appends 'E'.
→ [0, 'f', 1, 'f', −2, 'f', 3, 'f', 'E'] — 9 items.

`risky(6)`: same for i = 0..3, then i=4: `break` → finally 'f' → loop ends by break, so **no** 'E'.
→ [0, 'f', 1, 'f', −2, 'f', 3, 'f', 'f'] — five 'f'.

- (A) 9 items. **True.**
- (B) ends with 'f', not 'E'. **False.**
- (C) five 'f' entries (i = 0..4). **True.**
- (D) −2 is logged at i = 2 in both calls. **True.**

**Trap:** thinking `break`/`continue` skip `finally`, or that loop-`else` means 'runs if the loop body never executed'.''',
            'verify': '''
r4, r6 = risky(4), risky(6)
truth = {'A': len(r4) == 9, 'B': r6[-1] == 'E', 'C': r6.count('f') == 5,
         'D': -2 in r4 and -2 in r6}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — decorators, closures and memoised recursion',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''from functools import lru_cache

def counted(f):
    def w(*a):
        w.calls += 1
        return f(*a)
    w.calls = 0
    return w

@counted
@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(7)
fib(5)
print(fib.calls)''',
            'answer': '14',
            'solution': '''Decorators apply bottom-up: `fib = counted(lru_cache(fib_original))`. The global name `fib` is bound to the **counting wrapper**, and the recursive calls inside the body look up the global `fib` at run time — so *every* call, including recursive ones and cache hits, is counted.

`fib(7)` (cache initially empty):
- each value n = 7, 6, 5, 4, 3, 2 is computed once (a cache miss) and makes exactly two calls, fib(n−1) and fib(n−2) → 6 × 2 = 12 calls;
- fib(1) and fib(0) are base cases reached via those calls (already counted);
- plus the outer call fib(7) itself → 12 + 1 = **13**.

`fib(5)`: one counted call, answered from the cache → **1**.

Total = 13 + 1 = **14**.

**Trap:** without memoisation fib(7) alone would make 41 calls; and if the decorators were in the other order (`lru_cache` outermost), cache hits would never reach the counter.''',
            'verify': '''
assert OUTPUT.strip() == ANSWER
calls = [0]
def plain(n):
    calls[0] += 1
    return n if n < 2 else plain(n-1) + plain(n-2)
plain(7)
assert calls[0] == 41
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Hashing — mutating a key after insertion',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class K:
    def __init__(self, v):
        self.v = v
    def __hash__(self):
        return hash(self.v)
    def __eq__(self, o):
        return isinstance(o, K) and self.v == o.v

k = K(1)
d = {k: 'x'}
k.v = 2
print(k in d, K(1) in d, K(2) in d, len(d))''',
            'options': [
                '`True False True 1`',
                '`False True False 1`',
                '`True False False 1`',
                '`False False False 1`',
            ],
            'answer': 'D',
            'solution': '''A dict stores each entry in the slot determined by the key's hash **at insertion time**, together with that hash value. A lookup computes the probe key's *current* hash, goes to that slot, and calls `__eq__` only on entries whose stored hash matches.

The entry was stored with hash(1). Then `k.v = 2` changes k's hash to hash(2) but the table is not updated.
- `k in d`: probes using hash(2) → no entry with stored hash 2 → **False** (even though it is the very same object).
- `K(1) in d`: hash(1) matches the stored hash; `__eq__` compares 1 with the stored key's *current* v = 2 → **False**.
- `K(2) in d`: hash(2) → no matching stored hash → **False**.
- `len(d)` is still 1 — the entry exists but is unreachable.

Output `False False False 1` → option **(D)**.

- (A)/(C) assume `in` checks object identity first without hashing.
- (B) assumes `__eq__` compares against the old value 1.

**Tip:** this is why Python's built-in mutable containers (`list`, `dict`, `set`) are unhashable — keys must not change their hash while stored.''',
            'verify': "ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'False False False 1' and ANSWER == 'B'",
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — reversal in groups',
            'text': 'The function `rev_k` below is applied to the singly linked list shown with k = 3. What list is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def rev_k(h, k):
    prev, cur, n = None, h, 0
    while cur and n < k:
        cur.nxt, prev, cur = prev, cur, cur.nxt
        n += 1
    if cur:
        h.nxt = rev_k(cur, k)
    return prev

head = None
for x in range(8, 0, -1):
    head = Node(x, head)
head = rev_k(head, 3)
out = []
while head:
    out.append(head.v)
    head = head.nxt
print(out)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 4, 5, 6, 7, 8],
                    'caption': 'Initial list',
                },
            ],
            'options': [
                '`[3, 2, 1, 6, 5, 4, 7, 8]`',
                '`[3, 2, 1, 6, 5, 4, 8, 7]`',
                '`[8, 7, 6, 5, 4, 3, 2, 1]`',
                '`[3, 2, 1]`',
            ],
            'answer': 'B',
            'solution': '''In the tuple assignment `cur.nxt, prev, cur = prev, cur, cur.nxt` the right-hand side is evaluated completely first, so it correctly reverses one link per iteration. After k steps, `prev` is the new head of the reversed group and the old head `h` is its tail.

- Group 1: 1, 2, 3 → 3 → 2 → 1; `cur` = 4 is not None, so `1.nxt = rev_k(4, 3)`.
- Group 2: 4, 5, 6 → 6 → 5 → 4; `cur` = 7 → `4.nxt = rev_k(7, 3)`.
- Group 3: 7, 8 — the loop stops when `cur` becomes None after 2 steps (n = 2 < k), so the short group is **also reversed** → 8 → 7; `cur` is None so 7.nxt stays None (it was set to None when 7 became the group tail).

Result: 3, 2, 1, 6, 5, 4, 8, 7 → option **(B)**.

- (A) assumes a final group shorter than k is left untouched — this code has no such check.
- (C) is a full reversal.
- (D) assumes the remainder is lost (it would be, without `h.nxt = …`).

**Trap:** the list is built by prepending 8, 7, …, 1, so it really starts 1 → 2 → …''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 2, 1, 6, 5, 4, 8, 7],
                    'caption': 'List after rev_k(head, 3)',
                },
            ],
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[3, 2, 1, 6, 5, 4, 8, 7]' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — comparison count',
            'text': 'The following Python quicksort uses the first element as pivot and counts one comparison for every element compared with the pivot. The value printed is ______.',
            'code': '''comps = 0

def qs(a):
    global comps
    if len(a) < 2:
        return a
    p = a[0]
    comps += len(a) - 1
    left = [x for x in a[1:] if x < p]
    right = [x for x in a[1:] if x >= p]
    return qs(left) + [p] + qs(right)

qs([50, 23, 9, 18, 61, 32, 75, 54, 41])
print(comps)''',
            'answer': '16',
            'solution': '''Each call on a sub-list of length L ≥ 2 adds L − 1 comparisons. The comprehensions keep the original relative order, so the next pivots are easy to read off.

- qs([50, 23, 9, 18, 61, 32, 75, 54, 41]): L = 9 → **8**; left = [23, 9, 18, 32, 41], right = [61, 75, 54].
- qs([23, 9, 18, 32, 41]): **4**; left = [9, 18], right = [32, 41].
- qs([9, 18]): **1**; left = [], right = [18].
- qs([32, 41]): **1**; right = [41].
- qs([61, 75, 54]): **2**; left = [54], right = [75].
- All remaining calls have length ≤ 1 → 0.

Total = 8 + 4 + 1 + 1 + 2 = **16**.

Compare: the worst case for n = 9 is 9·8/2 = 36 (already sorted input); the best is about n log₂ n − n.

**Trap:** `global comps` is required — without it, `comps += …` makes `comps` local and raises `UnboundLocalError`. Also, each partition step counts as L − 1 comparisons even though the code scans the list twice.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '50',
                    'children': {
                        '50': ['23', '61'],
                        '23': ['9', '32'],
                        '9': ['18'],
                        '32': ['41'],
                        '61': ['54', '75'],
                    },
                    'caption': "Pivot recursion tree (each pivot's call costs size − 1)",
                },
            ],
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source P on the weighted directed graph shown. Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['P', 'Q', 'R', 'S', 'U', 'V'],
                    'edges': [
                        ['P', 'Q', 6],
                        ['P', 'R', 2],
                        ['R', 'Q', 3],
                        ['R', 'S', 8],
                        ['Q', 'S', 2],
                        ['Q', 'U', 7],
                        ['S', 'U', 1],
                        ['R', 'V', 9],
                        ['U', 'V', 2],
                        ['S', 'V', 6],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [2, 2],
                        'R': [2, 0],
                        'S': [4, 2],
                        'U': [4, 0],
                        'V': [6, 1],
                    },
                },
            ],
            'options': [
                'The shortest distance from P to V is 10',
                'Vertices are extracted from the priority queue in the order P, R, Q, S, U, V',
                'In the shortest-path tree, the parent of V is R',
                'If the weight of edge P→Q were reduced from 6 to 4, the shortest distance to U would decrease by exactly 1',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''Dijkstra settles vertices in non-decreasing order of distance.

- Extract P (0): Q = 6, R = 2.
- Extract R (2): Q = min(6, 5) = 5; S = 10; V = 11.
- Extract Q (5): S = min(10, 7) = 7; U = 12.
- Extract S (7): U = min(12, 8) = 8; V = min(11, 13) = 11.
- Extract U (8): V = min(11, 10) = 10.
- Extract V (10).

- (A) d(V) = 10 via P→R→Q→S→U→V. **True.**
- (B) Extraction order P, R, Q, S, U, V. **True.**
- (C) V's final distance comes from U (8 + 2), so its parent is **U**; the edge R→V gave only the temporary value 11. **False.**
- (D) With P→Q = 4: Q = min(4, 5) = 4, S = 6, U = 7 (was 8) → decrease of exactly 1. **True.**

**Trap:** in (D) it is tempting to say 'decrease by 2' because the edge got 2 cheaper — but the old best route to Q (via R, cost 5) was already 1 cheaper than the direct edge, so the saving is only 1.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['P', 'Q', 'R', 'S', 'U', 'V'],
                    'edges': [
                        ['P', 'Q', 6],
                        ['P', 'R', 2],
                        ['R', 'Q', 3],
                        ['R', 'S', 8],
                        ['Q', 'S', 2],
                        ['Q', 'U', 7],
                        ['S', 'U', 1],
                        ['R', 'V', 9],
                        ['U', 'V', 2],
                        ['S', 'V', 6],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [2, 2],
                        'R': [2, 0],
                        'S': [4, 2],
                        'U': [4, 0],
                        'V': [6, 1],
                    },
                    'highlight_edges': [
                        ['P', 'R'],
                        ['R', 'Q'],
                        ['Q', 'S'],
                        ['S', 'U'],
                        ['U', 'V'],
                    ],
                    'caption': 'Shortest-path tree from P',
                },
            ],
            'verify': '''
import heapq
def dij(E):
    G = {}
    for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, [])
    d = {v: float('inf') for v in G}; d['P'] = 0; par = {}; order = []
    pq = [(0, 'P')]; done = set()
    while pq:
        du, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u); order.append(u)
        for v, w in G[u]:
            if du + w < d[v]: d[v] = du + w; par[v] = u; heapq.heappush(pq, (d[v], v))
    return d, par, order
E = [('P','Q',6),('P','R',2),('R','Q',3),('R','S',8),('Q','S',2),('Q','U',7),
     ('S','U',1),('R','V',9),('U','V',2),('S','V',6)]
d, par, order = dij(E)
E2 = [(u, v, 4 if (u, v) == ('P','Q') else w) for u, v, w in E]
d2, _, _ = dij(E2)
truth = {'A': d['V'] == 10, 'B': ''.join(order) == 'PRQSUV', 'C': par['V'] == 'R',
         'D': d['U'] - d2['U'] == 1}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary trees in Python — mutable default argument',
            'text': 'The following program builds the binary tree shown and collects its leaves. What is printed?',
            'code': '''class Node:
    def __init__(self, v, l=None, r=None):
        self.v, self.l, self.r = v, l, r
    def leaves(self, acc=[]):
        if self.l is None and self.r is None:
            acc.append(self.v)
        for c in (self.l, self.r):
            if c:
                c.leaves(acc)
        return acc

t = Node(1, Node(2, Node(4), Node(5, Node(8))),
         Node(3, None, Node(6, Node(7), Node(9))))
x = t.leaves()
y = t.l.leaves()
print(len(x), len(y), x is y)''',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        1,
                        [
                            2,
                            [4],
                            [
                                5,
                                [8],
                                None,
                            ],
                        ],
                        [
                            3,
                            None,
                            [
                                6,
                                [7],
                                [9],
                            ],
                        ],
                    ],
                    'caption': 'Figure: tree t',
                },
            ],
            'options': ['`4 2 False`', '`4 6 True`', '`6 6 True`', '`6 2 True`'],
            'answer': 'C',
            'solution': '''The default `acc=[]` is created **once**, when `def leaves` runs; every call that omits `acc` shares that single list. Recursive calls pass `acc` explicitly, so within one top-level call everything goes into the same list.

- `x = t.leaves()`: pre-order walk appends leaves 4, 8, 7, 9 to the shared default list → it now holds 4 items, and `x` refers to it.
- `y = t.l.leaves()`: again uses the *same* default list and appends the leaves of the subtree rooted at 2: 4, 8 → the list now holds [4, 8, 7, 9, 4, 8].
- `x` and `y` are the same object, evaluated at print time → `len(x) = len(y) = 6`, `x is y` → True.

Output `6 6 True` → option **(C)**.

- (A) is what a fresh list per call would give.
- (B) assumes `len(x)` was frozen when `x` was assigned — `x` is a reference.
- (D) mixes both errors.

**Tip:** use `acc=None` and `if acc is None: acc = []` inside the function.''',
            'verify': "assert OUTPUT.strip() == '6 6 True' and ANSWER == 'C'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — counting shortest paths',
            'text': 'In the weighted undirected graph shown, the number of distinct shortest paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 3],
                        ['S', 'C', 5],
                        ['A', 'B', 1],
                        ['A', 'D', 4],
                        ['B', 'D', 3],
                        ['B', 'E', 4],
                        ['C', 'E', 2],
                        ['D', 'F', 2],
                        ['E', 'F', 3],
                        ['D', 'T', 5],
                        ['F', 'T', 3],
                        ['E', 'T', 6],
                        ['C', 'D', 1],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.6, 2.4],
                        'B': [1.4, 1.2],
                        'C': [1.8, -0.6],
                        'D': [3.4, 2.4],
                        'E': [4.0, -0.6],
                        'F': [5.0, 1],
                        'T': [6.6, 1],
                    },
                },
            ],
            'answer': '8',
            'solution': '''Run Dijkstra and keep, for each vertex v, the number of shortest paths N(v). When an edge (u, v) gives a strictly smaller distance, set N(v) = N(u); when it gives an equal distance, add N(u).

- S: d = 0, N = 1.
- A: d = 2 (S–A), N = 1.
- B: S–B = 3 and S–A–B = 2 + 1 = 3 → d = 3, N = 1 + 1 = 2.
- C: S–C = 5 (via D would be 7) → d = 5, N = 1.
- D: via A 2 + 4 = 6, via B 3 + 3 = 6, via C 5 + 1 = 6 → d = 6, N = 1 + 2 + 1 = 4.
- E: via B 3 + 4 = 7, via C 5 + 2 = 7 → d = 7, N = 2 + 1 = 3.
- F: via D 6 + 2 = 8, via E 7 + 3 = 10 → d = 8, N = 4.
- T: via D 6 + 5 = 11, via F 8 + 3 = 11, via E 7 + 6 = 13 → d = 11, N = N(D) + N(F) = 4 + 4 = **8**.

**Trap:** stopping at the first shortest path found, or adding counts through E (whose route to T is longer). Paths through F all pass through D, but they are still distinct paths from those using D–T directly.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Distance d and path count N',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'T'],
                    'row_labels': ['d', 'N'],
                    'rows': [
                        [0, 2, 3, 5, 6, 7, 8, 11],
                        [1, 1, 2, 1, 4, 3, 4, 8],
                    ],
                    'highlight': [
                        [1, 7],
                    ],
                },
            ],
            'verify': '''
E = [('S','A',2),('S','B',3),('S','C',5),('A','B',1),('A','D',4),('B','D',3),('B','E',4),
     ('C','E',2),('D','F',2),('E','F',3),('D','T',5),('F','T',3),('E','T',6),('C','D',1)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
best = [float('inf')]; cnt = [0]
def dfs(u, seen, cost):
    if cost > 11: return
    if u == 'T':
        if cost < best[0]: best[0], cnt[0] = cost, 1
        elif cost == best[0]: cnt[0] += 1
        return
    for v, w in G[u]:
        if v not in seen: dfs(v, seen | {v}, cost + w)
dfs('S', {'S'}, 0)
assert best[0] == 11 and cnt[0] == int(ANSWER)
''',
        },
    ],
}
