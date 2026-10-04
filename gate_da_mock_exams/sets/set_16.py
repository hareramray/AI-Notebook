# Set 16 — Recursion & Memoization in Python (GATE-level)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.

SET = {
    'number': 16,
    'title': 'Recursion & Memoization in Python',
    'difficulty': 'GATE-level',
    'focus': 'recursion tracing, call counts, memoized recursion, recursion trees',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Recursion — tracing output order',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def f(n):
    if n <= 0:
        return
    print(n, end=' ')
    f(n - 2)
    print(n % 3, end=' ')
    f(n - 3)

f(5)''',
            'options': ['`5 3 1 2 0 1 2 2`', '`5 3 1 1 0 2 2 2`', '`5 3 1 1 0 2 2`', '`5 2 3 1 1 0 2 2`'],
            'answer': 'B',
            'solution': '''Each call prints n, recurses on n − 2, prints n mod 3, then recurses on n − 3. Calls with n ≤ 0 print nothing. Expand depth-first:

- f(5): print **5**, call f(3)
  - f(3): print **3**, call f(1)
    - f(1): print **1**; f(−1) nothing; print 1 % 3 = **1**; f(−2) nothing
  - back in f(3): print 3 % 3 = **0**; f(0) nothing
- back in f(5): print 5 % 3 = **2**; call f(2)
  - f(2): print **2**; f(0) nothing; print 2 % 3 = **2**; f(−1) nothing

Output: `5 3 1 1 0 2 2 2`.

- (A) swaps the two values printed by f(1) and f(5)'s middle print — it prints the remainders in the wrong frames.
- (C) forgets that f(2) prints twice (once before and once after its first recursive call).
- (D) runs f(n − 3) before f(n − 2).

**Tip:** for a function with code between two recursive calls, write the recursion tree and read it like an in-order walk: pre-print, left subtree, mid-print, right subtree.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': 'f5',
                    'children': {
                        'f5': ['f3', 'f2'],
                        'f3': ['f1', 'f0'],
                        'f1': ['f-1', 'f-2'],
                        'f2': ["f0'", "f-1'"],
                    },
                    'labels': {
                        'f5': '5',
                        'f3': '3',
                        'f2': '2',
                        'f1': '1',
                        'f0': '0',
                        'f-1': '-1',
                        'f-2': '-2',
                        "f0'": '0',
                        "f-1'": '-1',
                    },
                    'caption': 'Recursion tree of f(5) (node = argument)',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['5','3','1','1','0','2','2','2'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Recursion — counting calls',
            'text': 'Consider the function below. The total number of calls to `g` (including the initial call) made when `g(9)` is evaluated is ______.',
            'code': '''def g(n):
    if n < 3:
        return 1
    return g(n - 1) + g(n - 3)''',
            'answer': '37',
            'solution': '''Let C(n) be the number of calls made by g(n), counting itself. Base cases n < 3 make exactly one call; otherwise C(n) = 1 + C(n − 1) + C(n − 3).

- C(0) = C(1) = C(2) = 1
- C(3) = 1 + C(2) + C(0) = 3
- C(4) = 1 + C(3) + C(1) = 5
- C(5) = 1 + C(4) + C(2) = 7
- C(6) = 1 + C(5) + C(3) = 11
- C(7) = 1 + C(6) + C(4) = 17
- C(8) = 1 + C(7) + C(5) = 25
- C(9) = 1 + C(8) + C(6) = **37**

(The returned value g(9) is 19; it satisfies the same recurrence without the '+1'.)

**Trap:** do not confuse the *value* returned with the *number of calls*; and remember that base-case calls (n = 0, 1, 2) are calls too. Note C(n) = 2·g(n) − 1 because every internal node of the recursion tree has exactly two children.''',
            'verify': '''
cnt = 0
def h(n):
    global cnt
    cnt += 1
    return 1 if n < 3 else h(n - 1) + h(n - 3)
v = h(9)
assert cnt == int(ANSWER) and cnt == 2 * v - 1
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression below is evaluated with an operand stack (`^` is exponentiation, `/` is exact division). Let v be its value and d the maximum number of operands on the stack at any time. The pair (v, d) is

`5 9 3 2 ^ / 4 2 - * + 3 -`''',
            'options': ['(4, 4)', '(4, 5)', '(−4, 4)', '(0, 4)'],
            'answer': 'A',
            'solution': '''Scan left to right: push operands; on an operator pop the **right** operand first, then the left, and push left ∘ right.

- 5, 9, 3, 2 → [5, 9, 3, 2] (size 4)
- ^ → 3^{2} = 9 → [5, 9, 9]
- / → 9 / 9 = 1 → [5, 1]
- 4, 2 → [5, 1, 4, 2] (size 4)
- − → 4 − 2 = 2 → [5, 1, 2]
- * → 1 × 2 = 2 → [5, 2]
- + → 7 → [7]; 3 → [7, 3]; − → 7 − 3 = **4**

Maximum stack size = **4**. So (v, d) = (4, 4).

- (B) overcounts the depth (the stack never holds 5 operands).
- (C) computes the final subtraction as 3 − 7.
- (D) reverses every subtraction (2 − 4 = −2, then 5 − 2 = 3, then 3 − 3 = 0).

**Trap:** operand order matters for −, / and ^: the element popped *first* is the right operand.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [5, 1, 4, 2],
                    'label': "before '−'",
                    'caption': 'Stack at maximum depth (second time)',
                },
            ],
            'verify': '''
st, d = [], 0
for tok in "5 9 3 2 ^ / 4 2 - * + 3 -".split():
    if tok in "+-*/^":
        b, a = st.pop(), st.pop()
        st.append({'+': a + b, '-': a - b, '*': a * b, '/': a / b, '^': a ** b}[tok])
    else:
        st.append(int(tok))
    d = max(d, len(st))
assert (st[0], d) == (4, 4) and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Memoization — mutable default dictionary',
            'text': 'Consider the function below, which uses a mutable default argument as a memo table. Assume these calls are made in a fresh interpreter, in the order the statements describe. Which of the following statements is/are TRUE?',
            'code': '''def fib(n, memo={}):
    if n in memo:
        return memo[n]
    memo[n] = n if n < 2 else fib(n - 1) + fib(n - 2)
    return memo[n]''',
            'options': [
                'A later call `fib(12)` makes 12 calls to `fib` in total',
                'A second call `fib(10)` afterwards makes exactly one call to `fib`',
                'After the first call `fib(10)`, the dictionary `fib.__defaults__[0]` has 11 keys',
                'The first call `fib(10)` makes 19 calls to `fib` in total (including itself)',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''The default `{}` is created once, so the memo **persists across top-level calls**.

**First fib(10):** fib(n) calls fib(n−1) first (a new value), and when it later calls fib(n−2) that value is already memoised (a single, immediately-returning call). So each n from 10 down to 2 makes two calls, fib(1) and fib(0) make none: total = 1 + 2 × 9 = **19**.

- (A) fib(12) → fib(11) (new) → fib(10) hit, fib(9) hit; fib(12) also calls fib(10) hit. Calls: fib(12), fib(11), fib(10), fib(9), fib(10) = **5**, not 12. **False.**
- (B) 10 is in the memo, so the call returns at once — 1 call. **True.**
- (C) Keys 0, 1, …, 10 are stored → 11 keys. **True.**
- (D) **True** (19 calls).

**Trap:** a mutable default is shared state. Here that is exploited deliberately; in ordinary code it is a classic bug.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

calls = 0
def fib2(n, memo={}):
    global calls
    calls += 1
    if n in memo: return memo[n]
    memo[n] = n if n < 2 else fib2(n - 1) + fib2(n - 2)
    return memo[n]
calls = 0; fib2(10); a = calls
b = len(fib2.__defaults__[0])
calls = 0; fib2(10); c = calls
calls = 0; fib2(12); d = calls
truth = {'A': a == 19, 'B': b == 11, 'C': c == 1, 'D': d == 12}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — quadratic probing',
            'text': 'Keys 22, 33, 44, 13, 24, 35 are inserted in this order into an initially empty table of size 11 using quadratic probing: the i-th probe (i = 0, 1, 2, …) examines slot (k mod 11 + i^{2}) mod 11. Counting every slot examined (including the one where the key is finally placed), the total number of probes for all six insertions is ______.',
            'answer': '12',
            'solution': '''With quadratic probing the probe offsets are 0, 1, 4, 9, … from the home slot.

- 22: home 0, empty → slot 0 (1 probe)
- 33: home 0 full; 0+1 = 1 empty → slot 1 (2 probes)
- 44: home 0 full; 1 full; 0+4 = 4 empty → slot 4 (3 probes)
- 13: home 2, empty → slot 2 (1 probe)
- 24: home 2 full; 3 empty → slot 3 (2 probes)
- 35: home 2 full; 3 full; 2+4 = 6 empty → slot 6 (3 probes)

Total = 1 + 2 + 3 + 1 + 2 + 3 = **12**.

**Trap:** with *linear* probing 44 would go to slot 2 and push 13 and 24 further, giving a different count. Quadratic probing jumps to 0 + 4 = 4, skipping slots 2 and 3.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        0: 22,
                        1: 33,
                        2: 13,
                        3: 24,
                        4: 44,
                        6: 35,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 11; tot = 0
for k in [22, 33, 44, 13, 24, 35]:
    for i in range(11):
        tot += 1
        j = (k % 11 + i * i) % 11
        if T[j] is None:
            T[j] = k; break
assert tot == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Recursive binary search — hidden cost of slicing',
            'text': 'Consider the recursive binary search below on a sorted Python list of n elements. Its worst-case running time is',
            'code': '''def bs(A, x):
    if not A:
        return False
    m = len(A) // 2
    if A[m] == x:
        return True
    if A[m] < x:
        return bs(A[m + 1:], x)
    return bs(A[:m], x)''',
            'options': ['Θ(log n)', 'Θ(n log n)', 'Θ(n)', 'Θ(log² n)'],
            'answer': 'C',
            'solution': '''Each call does O(1) comparisons, but the **slice** `A[m+1:]` or `A[:m]` builds a new list of about n/2 elements, which costs Θ(n/2) time.

Recurrence: T(n) = T(n/2) + Θ(n).
Unrolling: n/2 + n/4 + n/8 + … ≤ n, so T(n) = **Θ(n)** (master theorem case 3: a = 1, b = 2, f(n) = n dominates n^{0} = 1).

- (A) Θ(log n) is the number of *calls*, true only if each call were O(1) (e.g. passing lo/hi indices instead of slicing).
- (B) Θ(n log n) would need Θ(n) work at each of log n levels — but the slice sizes halve.
- (D) has no basis here.

**Trap:** Python slicing copies. A 'logarithmic' algorithm written with slices is linear.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

copied = 0
def bs2(A, x):
    global copied
    if not A: return False
    m = len(A) // 2
    if A[m] == x: return True
    if A[m] < x:
        copied += len(A) - m - 1; return bs2(A[m + 1:], x)
    copied += m; return bs2(A[:m], x)
res = []
for k in (12, 16):
    n = 2 ** k; copied = 0; bs2(list(range(n)), n + 5); res.append(copied)
assert 14 <= res[1] / res[0] <= 18   # grows linearly (x16), not like log n
assert ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Recursion on binary trees',
            'text': 'The binary tree T shown below is stored as nested lists `[value, left, right]` (with `None` for an empty subtree). The value returned by `g(T)` is ______.',
            'code': '''def g(t):
    if t is None:
        return 0
    a, b = g(t[1]), g(t[2])
    return max(a, b) + (1 if t[0] % 2 else 0)''',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        7,
                        [
                            4,
                            [
                                9,
                                None,
                                [3],
                            ],
                            [2],
                        ],
                        [
                            5,
                            [
                                1,
                                [11],
                                [6],
                            ],
                            [
                                8,
                                None,
                                [13],
                            ],
                        ],
                    ],
                    'caption': 'Figure: tree T',
                },
            ],
            'answer': '4',
            'solution': '''g(t) returns the **maximum number of odd keys on any root-to-leaf path** of t: each node adds 1 if its key is odd to the best of its two subtrees.

Bottom-up values:
- Leaves: g(3) = 1, g(2) = 0, g(11) = 1, g(6) = 0, g(13) = 1.
- g(9) = max(0, 1) + 1 = 2; g(4) = max(2, 0) + 0 = 2.
- g(1) = max(1, 0) + 1 = 2; g(8) = max(0, 1) + 0 = 1; g(5) = max(2, 1) + 1 = 3.
- g(7) = max(2, 3) + 1 = **4**.

The best path is 7 → 5 → 1 → 11, all four keys odd.

**Trap:** the path 7 → 4 → 9 → 3 is the longest-looking left path but contains the even key 4, so it scores only 3.''',
            'verify': '''
T = [7, [4, [9, None, [3, None, None]], [2, None, None]],
     [5, [1, [11, None, None], [6, None, None]], [8, None, [13, None, None]]]]
assert g(T) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bubble sort with early termination',
            'text': 'Bubble sort with an early-exit flag (stop after a pass that makes no swap; pass i compares adjacent pairs in positions 0 … n−1−i) sorts [3, 1, 2, 9, 5, 4, 8, 7] in ascending order. The total number of element comparisons made is',
            'options': ['13', '28', '18', '8'],
            'answer': 'C',
            'solution': '''Each pass bubbles the largest remaining element to the end; the algorithm stops after the first pass that performs no swaps (that pass still makes its comparisons).

- Pass 1 (7 comparisons): [1, 2, 3, 5, 4, 8, 7, 9] — swaps 3↔1, 3↔2, 9↔5, 9↔4, 9↔8, 9↔7.
- Pass 2 (6 comparisons): [1, 2, 3, 4, 5, 7, 8, 9] — swaps 5↔4, 8↔7.
- Pass 3 (5 comparisons): no swaps → stop.

Comparisons = 7 + 6 + 5 = **18**. (Total swaps = 8 = number of inversions.)

- (A) 13 forgets the final swap-free pass, which is needed to *detect* sortedness.
- (B) 28 = n(n−1)/2 ignores the early exit.
- (D) 8 is the number of swaps, not comparisons.

**Tip:** the number of passes is (max number of positions any element must move **left**) + 1.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', 'pass 1', 'pass 2', 'pass 3'],
                    'rows': [
                        [3, 1, 2, 9, 5, 4, 8, 7],
                        [1, 2, 3, 5, 4, 8, 7, 9],
                        [1, 2, 3, 4, 5, 7, 8, 9],
                        [1, 2, 3, 4, 5, 7, 8, 9],
                    ],
                    'highlight': [
                        [1, 7],
                        [2, 6],
                        [2, 5],
                    ],
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

A = [3, 1, 2, 9, 5, 4, 8, 7]; n = len(A); comps = 0
for i in range(n - 1):
    sw = False
    for j in range(n - 1 - i):
        comps += 1
        if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]; sw = True
    if not sw: break
assert comps == 18 and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Recursive DFS — discovery/finish times',
            'text': 'Recursive DFS is run on the directed graph below starting from **A**, visiting out-neighbours in alphabetical order. A single clock starts at 1 and is incremented at every discovery and every finish. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['C', 'A'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'D'],
                    ],
                    'pos': {
                        'A': [0, 1.5],
                        'B': [2, 2.5],
                        'C': [2, 0.5],
                        'D': [2, -1],
                        'E': [4, 2.5],
                        'F': [4, -1],
                    },
                },
            ],
            'options': [
                'E finishes before F',
                'A → D is a back edge',
                'The finish time of D is 8',
                'The discovery order is A, B, C, E, F, D',
            ],
            'answer': ['C', 'D'],
            'solution': '''Trace (d/f = discovery/finish):

- A d1 → B d2 → C d3; C → A is to a vertex still on the stack (back edge); C f4.
- B → E d5 → F d6 → D d7; D → E: E is on the stack (back edge); D f8; F f9; E f10; B f11.
- A → D: D is already finished and was discovered after A → **forward** edge. A f12.

- (A) F (9) finishes before E (10) since F is E's descendant. **False.**
- (B) A → D goes to a *descendant* that is already finished: a forward edge, not a back edge. **False.**
- (C) D finishes at 8. **True.**
- (D) Discovery order A, B, C, E, F, D. **True.**

**Tip:** for an edge u → v to an already-discovered v: v still active ⇒ back; v finished with d[u] < d[v] ⇒ forward; otherwise cross.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['C', 'A'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'D'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['E', 'F'],
                        ['F', 'D'],
                    ],
                    'pos': {
                        'A': [0, 1.5],
                        'B': [2, 2.5],
                        'C': [2, 0.5],
                        'D': [2, -1],
                        'E': [4, 2.5],
                        'F': [4, -1],
                    },
                    'caption': 'DFS tree edges highlighted',
                },
                {
                    'type': 'matrix',
                    'title': 'Discovery / finish times',
                    'col_labels': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'row_labels': ['d', 'f'],
                    'rows': [
                        [1, 2, 3, 7, 5, 6],
                        [12, 11, 4, 8, 10, 9],
                    ],
                    'highlight': [
                        [1, 3],
                    ],
                },
            ],
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'A': ['B', 'D'], 'B': ['C', 'E'], 'C': ['A'], 'D': ['E'], 'E': ['F'], 'F': ['D']}
t = 0; d = {}; f = {}; kind = {}
def dfs(u):
    global t
    t += 1; d[u] = t
    for v in G[u]:
        if v not in d: kind[(u, v)] = 'tree'; dfs(v)
        elif v not in f: kind[(u, v)] = 'back'
        elif d[u] < d[v]: kind[(u, v)] = 'fwd'
        else: kind[(u, v)] = 'cross'
    t += 1; f[u] = t
dfs('A')
order = sorted(d, key=d.get)
truth = {'A': order == list('ABCEFD'), 'B': f['D'] == 8,
         'C': kind[('A', 'D')] == 'back', 'D': f['E'] < f['F']}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Deques — rotate semantics',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from collections import deque
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
d.appendleft(d.pop())
d.rotate(-3)
x = d.popleft() * 10 + d[-1]
print(x, len(d))''',
            'options': ['`15 4`', '`35 4`', '`45 5`', '`12 4`'],
            'answer': 'A',
            'solution': '''`rotate(k)` with k > 0 moves k elements from the right end to the left end; k < 0 rotates the other way. `pop()` removes from the right, `appendleft` adds on the left.

- start: [1, 2, 3, 4, 5]
- rotate(2): [4, 5, 1, 2, 3]
- pop() → 3, appendleft(3): [3, 4, 5, 1, 2] (this is one more right-rotation)
- rotate(−3): move 3 elements from left to right → [1, 2, 3, 4, 5]
- popleft() → 1; deque [2, 3, 4, 5]; d[−1] = 5 → x = 10 + 5 = **15**; len = 4.

Net effect: +2 +1 −3 = 0 rotations, so the deque is back to its original order.

- (B) 35 uses the deque after rotate(2) only.
- (C) 45 forgets the `pop` and treats rotate(−3) as rotating right; also the length is 4.
- (D) 12 reads d[−1] as the second element.

**Tip:** track the net rotation count rather than individual moves.''',
            'verify': '''
assert OUTPUT.split() == ['15', '4'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Memoization — lru_cache call counting',
            'text': 'Consider the following Python program. The **second** number printed (the value of `calls`) is ______.',
            'code': '''from functools import lru_cache

calls = 0

@lru_cache(maxsize=None)
def p(n, k):
    global calls
    calls += 1
    if k == 0 or k == n:
        return 1
    return p(n - 1, k - 1) + p(n - 1, k)

print(p(8, 3), calls)''',
            'answer': '23',
            'solution': '''With `lru_cache`, the function **body** runs exactly once per distinct argument pair; repeated calls are answered by the cache without executing `calls += 1`. So `calls` = number of distinct states (n, k) reachable from (8, 3).

From (n, k) we reach (n−1, k−1) and (n−1, k), stopping when k = 0 or k = n. Distinct states per level:

- n = 8: k = 3 (1)
- n = 7: k = 2, 3 (2)
- n = 6: k = 1, 2, 3 (3)
- n = 5: k = 0, 1, 2, 3 (4)
- n = 4: k = 0 (from (5,1)), 1, 2, 3 (4)
- n = 3: k = 0, 1, 2, 3 (4) — (4,0) is a base case, so (3,0) comes from (4,1)
- n = 2: k = 0, 1, 2 (3) — (3,3) and (3,0) are base cases
- n = 1: k = 0, 1 (2) — from (2,1)

Total = 1 + 2 + 3 + 4 + 4 + 4 + 3 + 2 = **23**. (The first number printed is C(8,3) = 56.)

**Trap:** without memoization the number of calls would be 2·C(8,3) − 1 = 111; with memoization it is the number of distinct subproblems, not the size of the recursion tree.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'States (n, k) whose body executes (✓)',
                    'col_labels': ['k=0', 'k=1', 'k=2', 'k=3'],
                    'row_labels': ['n=8', 'n=7', 'n=6', 'n=5', 'n=4', 'n=3', 'n=2', 'n=1'],
                    'rows': [
                        ['', '', '', '✓'],
                        ['', '', '✓', '✓'],
                        ['', '✓', '✓', '✓'],
                        ['✓', '✓', '✓', '✓'],
                        ['✓', '✓', '✓', '✓'],
                        ['✓', '✓', '✓', '✓'],
                        ['✓', '✓', '✓', ''],
                        ['✓', '✓', '', ''],
                    ],
                },
            ],
            'verify': '''
seen = set()
def walk(n, k):
    if (n, k) in seen: return
    seen.add((n, k))
    if k == 0 or k == n: return
    walk(n - 1, k - 1); walk(n - 1, k)
walk(8, 3)
assert OUTPUT.split() == ['56', ANSWER] and len(seen) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Recursion — Tower of Hanoi move sequence',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''moves = []

def hanoi(n, src, dst, via):
    if n == 0:
        return
    hanoi(n - 1, src, via, dst)
    moves.append((n, src, dst))
    hanoi(n - 1, via, dst, src)

hanoi(4, 'A', 'C', 'B')
print(moves[9])''',
            'options': ["`(3, 'B', 'C')`", "`(1, 'B', 'C')`", "`(2, 'A', 'B')`", "`(2, 'B', 'A')`"],
            'answer': 'D',
            'solution': '''hanoi(n) makes 2^{n} − 1 moves: the 2^{n−1} − 1 moves of the first sub-call, then the move of disk n (move number 2^{n−1}), then the second sub-call. `moves[9]` is the **10th** move.

- hanoi(4, A, C, B): moves 1–7 = hanoi(3, A, B, C); move 8 = disk 4 A→C; moves 9–15 = hanoi(3, B, C, A).
- Move 10 is the 2nd move of hanoi(3, B, C, A), whose moves are: hanoi(2, B, A, C) (moves 9–11), disk 3 B→C (move 12), hanoi(2, A, C, B) (13–15).
- hanoi(2, B, A, C): disk 1 B→C (move 9), **disk 2 B→A (move 10)**, disk 1 C→A (move 11).

So `moves[9] = (2, 'B', 'A')`.

- (A) `(3, 'B', 'C')` is move 12.
- (B) `(1, 'B', 'C')` is move 9 (`moves[8]`) — an off-by-one with 0-based indexing.
- (C) `(2, 'A', 'B')` is move 2 (pattern of the first half).

**Tip:** disk d moves at steps whose number has exactly d − 1 trailing zero bits in binary; 10 = 1010₂ has one trailing zero → disk 2.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "(2, 'B', 'A')" and ANSWER == 'A'
assert moves[8] == (1, 'B', 'C') and moves[11] == (3, 'B', 'C')
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Mutual recursion',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''def a(n):
    return 1 if n <= 0 else n + b(n - 1)

def b(n):
    return 0 if n <= 0 else a(n // 2) * 2

print(a(10))''',
            'answer': '22',
            'solution': '''`a` and `b` call each other; expand until a base case is reached and then substitute back.

- a(10) = 10 + b(9)
- b(9) = 2 · a(9 // 2) = 2 · a(4)
- a(4) = 4 + b(3)
- b(3) = 2 · a(1)
- a(1) = 1 + b(0) = 1 + 0 = 1 (b(0) is a base case returning 0)

Substituting back: b(3) = 2, a(4) = 6, b(9) = 12, a(10) = 10 + 12 = **22**.

Only 9 calls are made in total (a and b alternate), so the depth is small despite n = 10.

**Trap:** `b(0)` returns **0**, not 1 — the two functions have different base values. Using a(0) = 1 by mistake for b(0) gives a(1) = 2 and a final answer of 26.''',
            'verify': '''
assert int(OUTPUT.strip()) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merge sort — recursion structure',
            'text': 'Top-down merge sort is applied to an array of **13** elements. Each call on a sub-array of length L > 1 splits it into the first ⌊L/2⌋ and the remaining ⌈L/2⌉ elements, recursively sorts both halves and merges them; a call on length 1 returns immediately. Which of the following statements is/are TRUE?',
            'options': [
                'At most 5 merge-sort calls are simultaneously active on the call stack',
                'The merge-sort function is called 25 times in total (including the first call)',
                'The final (top-level) merge can perform up to 13 key comparisons',
                'Exactly 13 calls are made on sub-arrays of length 1',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''The recursion tree is a full binary tree whose leaves are the length-1 calls.

- (A) Longest chain of sizes: 13 → 7 → 4 → 2 → 1 (always following the larger half). That is **5** frames. **True.**
- (B) A full binary tree with 13 leaves has 12 internal nodes → 13 + 12 = **25 calls. True.**
- (C) Merging sorted lists of sizes 6 and 7 needs at most 6 + 7 − 1 = **12** comparisons (the last element is placed without comparing). **False.**
- (D) Every element ends up alone in exactly one leaf → **13 leaf calls. True.**

**Trap:** depth is governed by ⌈log₂ 13⌉ + 1 = 5 frames (4 edges); and the merge worst case is n − 1, not n.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '13',
                    'children': {
                        '13': ['6', '7'],
                        '6': ['3a', '3b'],
                        '7': ['3c', '4'],
                        '3a': ['1a', '2a'],
                        '3b': ['1b', '2b'],
                        '3c': ['1c', '2c'],
                        '4': ['2d', '2e'],
                    },
                    'labels': {
                        '3a': '3',
                        '3b': '3',
                        '3c': '3',
                        '1a': '1',
                        '1b': '1',
                        '1c': '1',
                        '2a': '2',
                        '2b': '2',
                        '2c': '2',
                        '2d': '2',
                        '2e': '2',
                    },
                    'caption': 'Recursion tree by sub-array length (each 2 has two leaf children, not drawn)',
                },
            ],
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

calls = 0; leaves = 0; maxd = 0
def ms(L, dep=1):
    global calls, leaves, maxd
    calls += 1; maxd = max(maxd, dep)
    if L <= 1:
        leaves += 1; return
    ms(L // 2, dep + 1); ms(L - L // 2, dep + 1)
ms(13)
top_max = (13 // 2) + (13 - 13 // 2) - 1
truth = {'A': calls == 25, 'B': maxd == 5, 'C': top_max == 13, 'D': leaves == 13}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — recursion with nonlocal state',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def make():
    count = 0
    def walk(n):
        nonlocal count
        if n <= 1:
            count += 1
            return n
        return walk(n // 2) + walk(n - n // 2)
    return walk, lambda: count

w, get = make()
print(w(7), get(), w(4), get())''',
            'options': ['`7 7 4 7`', '`7 7 4 4`', '`7 13 4 20`', '`7 7 4 11`'],
            'answer': 'D',
            'solution': '''`walk` splits n into ⌊n/2⌋ and ⌈n/2⌉ until pieces of size 1 remain, so it returns n and its recursion tree has exactly n leaves. Only leaf calls increment `count`. Because `count` lives in the enclosing scope of `make`, it is **shared and persistent** across calls of `w`, and `get` (a closure) reads its current value.

Arguments of `print` are evaluated left to right:

- `w(7)` → 7; leaves: 7 → (3, 4) → (1, 2), (2, 2) → … = 7 leaves → count = 7.
- `get()` → 7.
- `w(4)` → 4; 4 more leaves → count = 11.
- `get()` → 11.

Output: `7 7 4 11`.

- (A) assumes the lambda captured the value 7 at creation — closures see the variable, not a snapshot.
- (B) assumes `count` restarts at 0 for each call.
- (C) counts every call (2n − 1 = 13 for n = 7, then 7 more), but only leaves increment.

**Trap:** without `nonlocal`, `count += 1` would raise UnboundLocalError; with it, the state accumulates across calls.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['7', '7', '4', '11'] and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Recursive BST validation',
            'text': 'Two recursive functions are written to check whether a binary tree (nested lists `[key, left, right]`) is a BST. They are applied to the tree T shown below. Which of the following statements is/are TRUE?',
            'code': '''def local_ok(t):
    if t is None:
        return True
    k, l, r = t
    if l and l[0] > k:
        return False
    if r and r[0] < k:
        return False
    return local_ok(l) and local_ok(r)

INF = float('inf')
def range_ok(t, lo=-INF, hi=INF):
    if t is None:
        return True
    k, l, r = t
    if not lo < k < hi:
        return False
    return range_ok(l, lo, k) and range_ok(r, k, hi)''',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        30,
                        [
                            15,
                            [8],
                            [34],
                        ],
                        [
                            45,
                            [40],
                            [52],
                        ],
                    ],
                    'highlight': [34],
                    'caption': 'Figure: tree T',
                },
            ],
            'options': [
                'The in-order traversal of T is 8, 15, 34, 30, 40, 45, 52',
                '`local_ok(T)` returns True',
                '`range_ok(T)` returns False',
                'If the key 34 is changed to 31, `range_ok(T)` returns True',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''`local_ok` only compares each node with its **immediate children**, while `range_ok` passes down an interval (lo, hi) that every key in the subtree must satisfy — the correct BST definition.

- (A) In-order (left, root, right): 8, 15, 34, 30, 40, 45, 52 — not sorted, confirming T is not a BST. **True.**
- (B) Every parent–child pair is ordered correctly (15 < 30 < 45, 8 < 15 < 34, 40 < 45 < 52), so `local_ok` returns **True**. **True.**
- (C) `range_ok`: root 30 → left subtree must lie in (−∞, 30); node 15 → its right subtree must lie in (15, 30); 34 ∉ (15, 30) → **False**. **True.**
- (D) 31 is still > 30, so it still violates the bound (15, 30). **False.** (Any key in (15, 30), e.g. 29, would fix it.)

**Trap:** checking only parent–child relations is the classic wrong BST test; the constraint from the root (30) reaches all the way down to 34.''',
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

T = [30, [15, [8, None, None], [34, None, None]], [45, [40, None, None], [52, None, None]]]
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
T2 = [30, [15, [8, None, None], [31, None, None]], [45, [40, None, None], [52, None, None]]]
truth = {'A': local_ok(T) is True, 'B': range_ok(T) is False,
         'C': ino(T) == [8, 15, 34, 30, 40, 45, 52], 'D': range_ok(T2) is True}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Recurrences from recursive code',
            'text': 'Consider the four recursive Python functions below (the running time is measured as a function of n, the argument). Which of the following statements is/are TRUE?',
            'code': '''def a(n):
    if n <= 1: return 1
    s = sum(range(int(n ** 0.5)))
    return a(n // 2) + a(n // 2) + s

def b(n):
    if n == 0: return 0
    return b(n - 1) + len(list(range(n)))

def c(n):
    if n <= 1: return 1
    s = 0
    for i in range(n):
        for j in range(n):
            s += 1
    return s + c(n // 2) + c(n // 2) + c(n // 2) + c(n // 2)

def d(n):
    return 1 if n <= 0 else d(n - 1) + d(n - 1)''',
            'options': [
                'The running time of `a(n)` is Θ(n)',
                'The running time of `c(n)` is Θ(n²)',
                'The running time of `d(n)` is Θ(2ⁿ)',
                'The running time of `b(n)` is Θ(n²)',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Write the recurrence for each function from its code, then solve it.

- (A) Two calls on n/2 plus Θ(√n) work: T(n) = 2T(n/2) + √n. Here n^{log₂2} = n dominates √n (master case 1) → **Θ(n)**. **True.**
- (B) Four calls on n/2 plus Θ(n²) work: T(n) = 4T(n/2) + n². Now n^{log₂4} = n² equals f(n) (master case 2) → **Θ(n² log n)**, not Θ(n²). **False.**
- (C) Two calls on n − 1 plus O(1): T(n) = 2T(n−1) + 1 = 2^{n+1} − 1 → **Θ(2ⁿ)**. **True.**
- (D) One call on n − 1 plus building a list of n elements: T(n) = T(n−1) + Θ(n) = Θ(1 + 2 + … + n) = **Θ(n²)**. **True.**

**Trap:** in (B) each of the log₂ n levels of the recursion tree does n² total work (4^{i} calls × (n/2^{i})²), which adds the log factor. In (D) the `len(list(range(n)))` hides a linear cost.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

# c(n) returns (#inner-loop steps + #leaves): check the n^2 log n growth
r = c(512) / c(256)
assert 4.3 < r < 4.6            # n^2 would give 4.0, n^2 log n gives 4*(9/8)=4.5
cnt = 0
def d2(n):
    global cnt
    cnt += 1
    return 1 if n <= 0 else d2(n - 1) + d2(n - 1)
d2(10); x = cnt; cnt = 0; d2(11)
assert cnt == 2 * x + 1         # doubles per +1 in n
assert sorted(ANSWER) == ['A', 'B', 'D']
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Memoized recursion on a DAG — path counting',
            'text': 'The number of distinct directed paths from **S** to **T** in the DAG shown below (as computed by the memoized recursion `paths(u) = 1 if u == T else Σ paths(v)` over the out-neighbours v of u) is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['S', 'C'],
                        ['A', 'D'],
                        ['A', 'E'],
                        ['B', 'D'],
                        ['B', 'F'],
                        ['C', 'F'],
                        ['D', 'E'],
                        ['D', 'T'],
                        ['E', 'T'],
                        ['F', 'E'],
                        ['F', 'T'],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.4],
                        'B': [1.5, 1],
                        'C': [1.5, -0.4],
                        'D': [3, 2.4],
                        'F': [3, -0.4],
                        'E': [4.5, 1],
                        'T': [6, 1],
                    },
                },
            ],
            'answer': '9',
            'solution': '''In a DAG, paths(u) = Σ paths(v) over edges u → v, with paths(T) = 1. Memoization evaluates each vertex once, in reverse topological order:

- paths(T) = 1
- paths(E) = paths(T) = 1
- paths(D) = paths(E) + paths(T) = 2
- paths(F) = paths(E) + paths(T) = 2
- paths(A) = paths(D) + paths(E) = 3
- paths(B) = paths(D) + paths(F) = 4
- paths(C) = paths(F) = 2
- paths(S) = 3 + 4 + 2 = **9**

Listing them: S-A-D-E-T, S-A-D-T, S-A-E-T, S-B-D-E-T, S-B-D-T, S-B-F-E-T, S-B-F-T, S-C-F-E-T, S-C-F-T.

**Tip:** without memoization the recursion would recompute paths(D), paths(E), paths(F) repeatedly; with it the cost is Θ(V + E).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Memo table (reverse topological order)',
                    'col_labels': ['T', 'E', 'D', 'F', 'A', 'B', 'C', 'S'],
                    'row_labels': ['paths'],
                    'rows': [
                        [1, 1, 2, 2, 3, 4, 2, 9],
                    ],
                    'highlight': [
                        [0, 7],
                    ],
                },
            ],
            'verify': '''
D = {'S': 'ABC', 'A': 'DE', 'B': 'DF', 'C': 'F', 'D': 'ET', 'E': 'T', 'F': 'ET', 'T': ''}
def allp(u):
    if u == 'T': return [['T']]
    return [[u] + p for v in D[u] for p in allp(v)]
assert len(allp('S')) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Recursive linked-list surgery and aliasing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def sw(h):
    if h is None or h.nxt is None:
        return h
    nxt = h.nxt
    h.nxt = sw(nxt.nxt)
    nxt.nxt = h
    return nxt

def show(h):
    out = []
    while h:
        out.append(h.v)
        h = h.nxt
    return out

head = None
for v in range(7, 0, -1):
    head = Node(v, head)
a = head
head = sw(head)
print(show(head), show(a))''',
            'options': [
                '`[2, 1, 4, 3, 6, 5, 7] [1, 2, 3, 4, 5, 6, 7]`',
                '`[2, 1, 4, 3, 6, 5, 7] [1, 4, 3, 6, 5, 7]`',
                '`[2, 1, 4, 3, 6, 5] [1, 4, 3, 6, 5]`',
                '`[2, 1, 4, 3, 6, 5, 7] [1]`',
            ],
            'answer': 'B',
            'solution': '''The loop builds 1 → 2 → 3 → 4 → 5 → 6 → 7 (prepending 7, 6, …, 1). `sw` swaps nodes in **pairs** recursively: for the pair (h, h.nxt) it first swaps the rest of the list (starting at the third node), hangs that result after h, and puts h.nxt in front of h.

- sw(7) → 7 (single node is returned unchanged).
- sw(5): 5.nxt = sw(7) = 7; 6.nxt = 5 → returns 6 → 5 → 7.
- sw(3): 3.nxt = 6…; 4.nxt = 3 → 4 → 3 → 6 → 5 → 7.
- sw(1): 1.nxt = 4…; 2.nxt = 1 → **2 → 1 → 4 → 3 → 6 → 5 → 7**.

`a` still refers to the **node** holding 1, which is now the second node; walking from it gives 1 → 4 → 3 → 6 → 5 → 7.

- (A) assumes `a` still sees the original list — but the nodes were relinked in place.
- (C) drops the unpaired last node 7, which the base case keeps.
- (D) assumes node 1 was detached; in fact its `nxt` was set to the swapped remainder.

**Trap:** a variable that refers to a node is not a snapshot of the list.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [2, 1, 4, 3, 6, 5, 7],
                    'head': 'head',
                    'caption': 'After sw: `a` points at the node holding 1 (second node)',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "[2, 1, 4, 3, 6, 5, 7] [1, 4, 3, 6, 5, 7]" and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Memoized recursion — grid paths with obstacles',
            'text': 'A robot starts at cell (0, 0) (top-left) of the 6 × 6 grid shown below and must reach cell (5, 5) (bottom-right), moving only **right** or **down** one cell at a time and never entering a blocked cell (marked X). The program below counts such paths. The value printed is ______.',
            'diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Grid (X = blocked)',
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'row_labels': ['0', '1', '2', '3', '4', '5'],
                    'rows': [
                        ['S', '', '', '', '', ''],
                        ['', '', '', 'X', '', ''],
                        ['', 'X', '', '', '', ''],
                        ['', '', '', 'X', '', ''],
                        ['X', '', '', '', '', ''],
                        ['', '', '', '', '', 'T'],
                    ],
                    'highlight': [
                        [1, 3],
                        [2, 1],
                        [3, 3],
                        [4, 0],
                    ],
                },
            ],
            'code': '''from functools import lru_cache
N = 6
blocked = {(1, 3), (2, 1), (3, 3), (4, 0)}

@lru_cache(maxsize=None)
def P(r, c):
    if r >= N or c >= N or (r, c) in blocked:
        return 0
    if (r, c) == (N - 1, N - 1):
        return 1
    return P(r + 1, c) + P(r, c + 1)

print(P(0, 0))''',
            'answer': '39',
            'solution': '''P(r, c) = number of valid paths from (r, c) to the target = P(r+1, c) + P(r, c+1), with 0 for blocked or out-of-grid cells and 1 at the target. Fill the table from the bottom-right corner:

- Row 5 and column 5 are all 1 (only one way: straight along the edge).
- Row 4: (4,4)=2, (4,3)=3, (4,2)=4, (4,1)=5, (4,0)=X.
- Row 3: (3,4)=3, (3,3)=X, (3,2)=4, (3,1)=9, (3,0)=9.
- Row 2: (2,4)=4, (2,3)=4, (2,2)=8, (2,1)=X, (2,0)=9.
- Row 1: (1,4)=5, (1,3)=X, (1,2)=8, (1,1)=8, (1,0)=17.
- Row 0: (0,4)=6, (0,3)=6, (0,2)=14, (0,1)=22, (0,0)=**39**.

Memoization makes each of the 36 states compute once, versus an exponential number of calls for plain recursion.

**Trap:** cell (4, 0) blocks the left column, so (3, 0) = (3, 1) + 0 = 9 rather than 9 + 1; and blocked cells contribute 0, not 1.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'P(r, c) = paths from each cell',
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'row_labels': ['0', '1', '2', '3', '4', '5'],
                    'rows': [
                        [39, 22, 14, 6, 6, 1],
                        [17, 8, 8, 'X', 5, 1],
                        [9, 'X', 8, 4, 4, 1],
                        [9, 9, 4, 'X', 3, 1],
                        ['X', 5, 4, 3, 2, 1],
                        [1, 1, 1, 1, 1, 1],
                    ],
                    'highlight': [
                        [0, 0],
                    ],
                },
            ],
            'verify': '''
from itertools import combinations
cnt = 0
for downs in combinations(range(10), 5):
    r = c = 0; ok = True
    for s in range(10):
        if s in downs: r += 1
        else: c += 1
        if (r, c) in blocked: ok = False; break
    cnt += ok
assert cnt == int(ANSWER) == int(OUTPUT.strip())
''',
        },
    ],
}
