# Set 36 — Full-Syllabus Mock — Paper 6 (GATE-level)
# Q1-Q10: 1 mark, Q11-Q20: 2 marks.

SET = {
    'number': 36,
    'title': 'Full-Syllabus Mock — Paper 6',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'Consider the following Python program. What is printed?',
            'code': 'print(-17 // 5, -17 % 5, 17 // -5, int(-17 / 5))',
            'options': ['`-3 -2 -3 -3`', '`-4 3 -4 -3`', '`-4 -2 -4 -4`', '`-3 3 -4 -3`'],
            'answer': 'B',
            'solution': '''Python's `//` is **floor** division (rounds toward −∞) and `%` returns a result with the sign of the **divisor**, so that `a == (a // b) * b + a % b` always holds. `int()` of a float **truncates** toward 0.

- `-17 // 5`: −3.4 floored → **−4**.
- `-17 % 5`: −17 − (−4)(5) = −17 + 20 = **3**.
- `17 // -5`: −3.4 floored → **−4**.
- `int(-17 / 5)`: −3.4 truncated → **−3**.

Output: `-4 3 -4 -3`.

- (A) is C-style truncation for `//` and a negative remainder.
- (C) gets `//` right but uses C's remainder sign and floors in `int()`.
- (D) truncates the first division but floors the third — inconsistent.

**Trap:** `//` and `int(a / b)` differ exactly when the quotient is negative and inexact.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.split() == ['-4', '3', '-4', '-3'] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Circular queue — capacity and wrap-around',
            'text': '''A circular queue is implemented in an array of size 8 with indices `front` and `rear`, both initially 0. `enqueue(x)` stores x at `rear` and sets rear = (rear + 1) mod 8, but is **ignored** if (rear + 1) mod 8 = front (queue full). `dequeue()` returns the element at `front` and sets front = (front + 1) mod 8.
The operations performed are: enqueue 1, 2, …, 9 (in order); then 3 dequeues; then enqueue 10, 11, 12, 13. The number of enqueue operations that were ignored is ______.''',
            'answer': '3',
            'solution': '''With the 'one slot always empty' convention, an array of size 8 holds at most **7** elements; full means (rear + 1) mod 8 = front.

- Enqueue 1 … 7 into slots 0 … 6; rear = 7. Enqueue 8: (7+1) mod 8 = 0 = front → **ignored**. Enqueue 9 → **ignored**.
- 3 dequeues remove 1, 2, 3 → front = 3; size 4.
- Enqueue 10 at slot 7 (rear → 0), 11 at slot 0 (rear → 1), 12 at slot 1 (rear → 2).
- Enqueue 13: (2+1) mod 8 = 3 = front → **ignored**.

Ignored operations: 8, 9, 13 → **3**. Final state: front = 3, rear = 2, size 7.

**Trap:** assuming the capacity is 8 (then only 9 and none of the later ones would be rejected). The empty slot is what distinguishes 'full' from 'empty' (front = rear).''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [11, 12, '', 4, 5, 6, 7, 10],
                    'pointers': {
                        'rear': 2,
                        'front': 3,
                    },
                    'caption': 'Final array (slot 2 is the reserved empty slot)',
                },
            ],
            'verify': '''
N = 8; Q = [None] * N; f = r = 0; ign = 0
def enq(x):
    global r, ign
    if (r + 1) % N == f: ign += 1; return
    Q[r] = x; r = (r + 1) % N
def deq():
    global f
    x = Q[f]; f = (f + 1) % N; return x
for x in range(1, 10): enq(x)
for _ in range(3): deq()
for x in range(10, 14): enq(x)
assert ign == int(ANSWER) and (f, r) == (3, 2)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Doubly linked lists — deleting a node',
            'text': 'In a doubly linked list each node has fields `prev` and `nxt`. Node `p` is neither the first nor the last node. Which of the following two-statement fragments correctly unlinks `p` from the list (leaving all other links consistent)?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': ['x', 'p', 'y'],
                    'doubly': True,
                    'caption': 'x ⇄ p ⇄ y (part of a longer list)',
                },
            ],
            'options': [
                '`p.nxt.prev = p.prev; p.prev.nxt = p.nxt.prev`',
                '`p.prev.nxt = p.nxt; p.nxt.prev = p.prev.nxt`',
                '`p.prev.nxt = p.nxt; p.prev.nxt.prev = p.prev`',
                '`p.nxt = p.nxt.nxt; p.nxt.prev = p`',
            ],
            'answer': 'C',
            'solution': '''We need x.nxt = y and y.prev = x (with x = p.prev, y = p.nxt). The catch is that the first statement changes a link that the second statement reads.

- (A) First: y.prev = x. Second: x.nxt = p.nxt.prev = y.prev = **x** → x points to itself. Wrong.
- (B) First: x.nxt = y. Second: y.prev = p.prev.nxt = x.nxt = **y** → y points back to itself. Wrong.
- (C) First: x.nxt = y. Second: `p.prev.nxt` is now y, so y.prev = p.prev = x. **Correct.**
- (D) Sets p.nxt to y's successor and that node's prev to p — this removes **y**, not p.

**Trap:** sequential pointer updates are not simultaneous; always re-evaluate each expression after the previous assignment (or save x and y in temporaries first).''',
            'verify': '''
class N:
    def __init__(s, v): s.v, s.prev, s.nxt = v, None, None
def mk():
    ns = [N(c) for c in "wxpyz"]
    for a, b in zip(ns, ns[1:]): a.nxt, b.prev = b, a
    return ns
frags = {'A': "p.nxt.prev = p.prev; p.prev.nxt = p.nxt.prev",
         'B': "p.prev.nxt = p.nxt; p.nxt.prev = p.prev.nxt",
         'C': "p.prev.nxt = p.nxt; p.prev.nxt.prev = p.prev",
         'D': "p.nxt = p.nxt.nxt; p.nxt.prev = p"}
good = []
for L, code in frags.items():
    ns = mk(); p = ns[2]; exec(code)
    fw, h = [], ns[0]
    while h and len(fw) < 10: fw.append(h.v); h = h.nxt
    bw, t = [], ns[4]
    while t and len(bw) < 10: bw.append(t.v); t = t.prev
    if fw == list("wxyz") and bw == list("zyxw"): good.append(L)
assert good == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Heaps — possible positions of a key',
            'text': 'A max-heap with 25 **distinct** keys is stored in an array A[0..24] (children of i at 2i+1 and 2i+2). The number of distinct indices at which the **third largest** key could be located is ______.',
            'answer': '6',
            'solution': '''In a max-heap every key is smaller than all its ancestors. So a key with exactly two larger keys has **at most 2 ancestors** → depth ≤ 2 → index ∈ {1, …, 6} (it cannot be the root, which is the maximum).

All of these are achievable:
- depth 1 (index 1 or 2): e.g. largest at root, second and third largest as its two children.
- depth 2 (indices 3–6): the second largest is at index 1 (or 2) and the third largest is its child — choose either side, and either child.

Hence **6** possible indices.

**Trap:** answering 2 (only the root's children) forgets that the third largest can be a child of the second largest. In general the k-th largest can be anywhere at depth ≤ k − 1.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [100, 99, 50, 98, 40, 45, 30],
                    'highlight': [3],
                    'caption': 'Example: third largest (98) at index 3, a child of 99',
                },
            ],
            'verify': '''
import random
random.seed(7)
pos = set()
for _ in range(4000):
    keys = random.sample(range(1000), 25); H = []
    for k in keys:
        H.append(k); i = len(H) - 1
        while i and H[(i - 1) // 2] < H[i]:
            H[i], H[(i - 1) // 2] = H[(i - 1) // 2], H[i]; i = (i - 1) // 2
    pos.add(H.index(sorted(H)[-3]))
assert pos <= set(range(1, 7)) and len(pos) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Hashing — probe sequences that cover the table',
            'text': 'For a key with home slot h, an open-addressing scheme examines slots s_{i} = (h + g(i)) mod m for i = 0, 1, …, m − 1. For which of the following choices are **all m slots** guaranteed to be examined?',
            'options': [
                'm = 12, g(i) = 4i',
                'm = 11, g(i) = i^{2}',
                'm = 16, g(i) = i(i + 1)/2',
                'm = 12, g(i) = 5i',
            ],
            'answer': ['C', 'D'],
            'solution': '''A linear step c covers the whole table iff gcd(c, m) = 1. Quadratic sequences are subtler.

- (A) gcd(4, 12) = 4 → only offsets 0, 4, 8 are reached (3 slots). **False.**
- (B) i^{2} mod 11 takes only the quadratic residues {0, 1, 3, 4, 5, 9}: 6 = (m+1)/2 distinct slots. **False.** (Quadratic probing with prime m is guaranteed to find a free slot only when the table is at most half full.)
- (C) Triangular numbers i(i+1)/2 mod 2^{k} are a permutation of 0 … 2^{k} − 1; for m = 16 the offsets are 0, 1, 3, 6, 10, 15, 5, 12, 4, 13, 7, 2, 14, 11, 9, 8 — all 16. **True.**
- (D) gcd(5, 12) = 1 → 5i mod 12 runs through all 12 residues. **True.**

**Tip:** this is why practical quadratic probing often uses triangular offsets with a power-of-two table size.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def cover(m, g): return len({g(i) % m for i in range(m)})
truth = {'A': cover(12, lambda i: 5 * i) == 12, 'B': cover(12, lambda i: 4 * i) == 12,
         'C': cover(11, lambda i: i * i) == 11, 'D': cover(16, lambda i: i * (i + 1) // 2) == 16}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — worst-case probes',
            'text': 'The iterative binary search below is run on a sorted list of **100** distinct integers. The maximum possible value returned (over all search keys x, present or absent) is',
            'code': '''def bs(A, x):
    lo, hi, c = 0, len(A) - 1, 0
    while lo <= hi:
        m = (lo + hi) // 2
        c += 1
        if A[m] == x:
            return c
        if A[m] < x:
            lo = m + 1
        else:
            hi = m - 1
    return c''',
            'options': ['6', '10', '8', '7'],
            'answer': 'D',
            'solution': '''Each iteration (probe) roughly halves the range; the worst case is ⌊log₂ n⌋ + 1 probes, the height (in nodes) of the implicit decision tree.

For n = 100: ⌊log₂ 100⌋ + 1 = 6 + 1 = **7**.

Concretely, a search for a key larger than everything shrinks the range sizes 100 → 50 → 25 → 12 → 6 → 3 → 1 → 0: 7 probes. The search for the smallest elements goes 100 → 49 → 24 → 11 → 5 → 2 → 0/1 and can also need 7.

- (A) 6 = ⌊log₂ 100⌋ forgets the +1.
- (B) 10 confuses with ⌈log₂ 1000⌉.
- (C) 8 would be needed only for n ≥ 128.

**Tip:** worst case = ⌈log₂(n + 1)⌉ = 7 for 64 ≤ n ≤ 127.''',
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

A = list(range(0, 200, 2))
worst = max(bs(A, x) for x in range(-1, 201))
assert worst == 7 and ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Insertion sort — counting comparisons',
            'text': 'Insertion sort (ascending) is run on [6, 2, 9, 4, 4, 1, 8]. In each pass, the key A[i] is compared with A[i−1], A[i−2], … ; each such check `A[j] > key` counts as **one** comparison, and the pass stops at the first A[j] ≤ key or when j < 0. The total number of comparisons is ______.',
            'answer': '15',
            'solution': '''A pass for key A[i] costs (number of larger elements to its left, which get shifted) + 1, except that the +1 is missing when the key travels all the way to index 0 (the loop ends because j < 0, not because of a comparison).

- i=1, key 2: 6 > 2 shift; j < 0 → **1** comparison → [2, 6, 9, 4, 4, 1, 8]
- i=2, key 9: 6 ≤ 9 → **1** → unchanged
- i=3, key 4: 9 >, 6 >, 2 ≤ → **3** → [2, 4, 6, 9, 4, 1, 8]
- i=4, key 4: 9 >, 6 >, 4 ≤ (equal stops — keeps stability) → **3** → [2, 4, 4, 6, 9, 1, 8]
- i=5, key 1: 9, 6, 4, 4, 2 all > 1; j < 0 → **5** → [1, 2, 4, 4, 6, 9, 8]
- i=6, key 8: 9 >, 6 ≤ → **2** → [1, 2, 4, 4, 6, 8, 9]

Total = 1 + 1 + 3 + 3 + 5 + 2 = **15**.

**Trap:** adding 1 for every pass (giving 17) double-counts the two passes whose key reached the front; and treating the equal 4 as 'greater' (giving 16) breaks stability.''',
            'verify': '''
A = [6, 2, 9, 4, 4, 1, 8]; c = 0
for i in range(1, len(A)):
    k, j = A[i], i - 1
    while j >= 0:
        c += 1
        if A[j] > k: A[j + 1] = A[j]; j -= 1
        else: break
    A[j + 1] = k
assert c == int(ANSWER) and A == sorted(A)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph theory — edges versus components',
            'text': 'A simple undirected graph has 10 vertices and exactly 3 connected components. The maximum possible number of edges is',
            'options': ['28', '36', '21', '27'],
            'answer': 'A',
            'solution': '''To maximise edges with k components, make each component complete and make the sizes as **unequal** as possible: one big clique plus k − 1 isolated vertices, because C(a, 2) + C(b, 2) grows when we move a vertex from the smaller to the larger part.

Sizes 8, 1, 1 → C(8, 2) + 0 + 0 = **28** edges.
Compare with balanced sizes 4, 3, 3 → 6 + 3 + 3 = 12, or 6, 2, 2 → 15 + 1 + 1 = 17.

General formula: C(n − k + 1, 2).

- (B) 36 = C(9, 2) is the maximum for 2 components.
- (C) 21 = C(7, 2) would be for 4 components.
- (D) 27 has no justification (28 − 1).

**Trap:** spreading vertices evenly *minimises*, not maximises, the edge count.''',
            'verify': '''
best = 0
for a in range(1, 9):
    for b in range(1, 9):
        c = 10 - a - b
        if c >= 1: best = max(best, a*(a-1)//2 + b*(b-1)//2 + c*(c-1)//2)
assert best == 28 and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — dictionaries, sets and stable sorting',
            'text': 'Consider the following Python program. After it runs, which of the following expressions evaluate to `True`?',
            'code': '''d = {}
for w in "the cat sat on the mat the end".split():
    d[w] = d.get(w, 0) + 1''',
            'options': [
                "`sorted(d.items(), key=lambda kv: -kv[1])[1][0] == 'cat'`",
                "`len(set('banana') - set('ban')) > 0`",
                "`max(d, key=d.get) == 'the'`",
                "`list(d)[0] == 'the'`",
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Since Python 3.7 dictionaries preserve **insertion order**; `sorted` is **stable**.

The dictionary is {'the': 3, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1, 'end': 1} (in this order).

- (A) Sorting by −count puts 'the' first; all others tie at 1 and keep their insertion order, so the second item is ('cat', 1). **True.**
- (B) set('banana') = {'b', 'a', 'n'} = set('ban'); the difference is empty → length 0. **False.**
- (C) 'the' has the largest count, 3. **True.**
- (D) The first key inserted is 'the'. **True.**

**Trap:** for (A), one might think ties are broken alphabetically ('end') — they are not; a stable sort keeps the original order.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

truth = {'A': list(d)[0] == 'the', 'B': max(d, key=d.get) == 'the',
         'C': len(set('banana') - set('ban')) > 0,
         'D': sorted(d.items(), key=lambda kv: -kv[1])[1][0] == 'cat'}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Recurrences — master theorem',
            'text': 'The solution of the recurrence T(n) = 2T(n/4) + √n, with T(1) = 1, is',
            'options': ['Θ(√n log n)', 'Θ(√n)', 'Θ(n)', 'Θ(n^{1/2} log² n)'],
            'answer': 'A',
            'solution': '''Master theorem with a = 2, b = 4: n^{log_b a} = n^{log₄ 2} = n^{1/2}. The driving function f(n) = √n is of the **same order**, which is case 2 → T(n) = Θ(√n log n).

Recursion-tree view: level i has 2^{i} subproblems of size n/4^{i}, each costing √(n/4^{i}) = √n / 2^{i}; total per level = 2^{i} · √n / 2^{i} = √n. There are log₄ n + 1 levels, so T(n) ≈ √n (log₄ n + 1) = Θ(√n log n).

- (B) would hold if f(n) were polynomially smaller than √n (case 1).
- (C) would need f(n) = n (case 3).
- (D) would need f(n) = √n log n.

**Trap:** concluding Θ(√n) because 'the leaves and the root both cost √n' — in case 2 *every* level costs the same, so the level count multiplies in.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

import math
def T(n): return 1 if n <= 1 else 2 * T(n // 4) + math.isqrt(n)
for k in (8, 10, 12):
    n = 4 ** k
    assert T(n) == math.isqrt(n) * (k + 1)     # exactly sqrt(n) * (log4 n + 1)
assert ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Stacks — infix to postfix conversion',
            'text': '''The infix expression
`a - b * c ^ d ^ ( e + f * g ) / h`
is converted to postfix with the standard operator-stack algorithm. Precedence: `^` (highest, **right**-associative) > `*`, `/` (left-associative) > `+`, `-` (left-associative). A left parenthesis is pushed onto the same stack. The maximum number of symbols (operators and parentheses) on the stack at any time is ______.''',
            'answer': '7',
            'solution': '''Rules: operands go straight to the output; an incoming operator first pops operators of **higher** precedence, or **equal** precedence if it is left-associative; `(` is pushed; `)` pops until the matching `(`.

- a → out; `-` → stack [−]
- b; `*` (higher than −) → [−, *]
- c; `^` → [−, *, ^]
- d; `^` is right-associative, so the `^` on top is **not** popped → [−, *, ^, ^]
- `(` → [−, *, ^, ^, (] (5)
- e; `+` → [−, *, ^, ^, (, +] (6)
- f; `*` (higher than +) → [−, *, ^, ^, (, +, *] (**7**)
- g; `)` pops *, + and discards ( → [−, *, ^, ^]
- `/` pops ^, ^, * (all ≥ its precedence) → [−, /]; h; end pops / and −.

Postfix: `a b c d e f g * + ^ ^ * h / -`. Maximum stack size = **7**.

**Trap:** treating `^` as left-associative pops the first `^` when the second arrives, giving a maximum of 6 and a different (wrong) postfix.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['−', '*', '^', '^', '(', '+', '*'],
                    'label': 'after reading f, *',
                    'caption': 'Stack at its maximum size',
                },
            ],
            'verify': '''
prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
out, st, mx = [], [], 0
for t in "a - b * c ^ d ^ ( e + f * g ) / h".split():
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
    mx = max(mx, len(st))
while st: out.append(st.pop())
assert ' '.join(out) == 'a b c d e f g * + ^ ^ * h / -' and mx == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'BST — insertion orders giving the same tree',
            'text': 'The keys 46, 23, 71, 12, 35, 58, 89, 30, 64 are inserted in this order into an empty BST. Which of the following insertion orders produces **exactly the same** BST?',
            'options': [
                '46, 23, 71, 30, 12, 35, 58, 89, 64',
                '46, 71, 23, 89, 64, 58, 12, 35, 30',
                '46, 23, 12, 30, 35, 71, 58, 64, 89',
                '46, 71, 58, 64, 23, 35, 12, 89, 30',
            ],
            'answer': 'D',
            'solution': '''Two orders give the same BST iff, for every node, it is inserted **after all of its ancestors**. So list the ancestor constraints of the target tree and check each option.

Target tree: 46 → (23 → 12, (35 → 30, –)), (71 → (58 → –, 64), 89). Constraints: 46 first; 23 before 12 and 35; **35 before 30**; 71 before 58 and 89; **58 before 64**.

- (A) 30 comes before 35 → 30 becomes 23's right child and 35 hangs below 30. **Different.**
- (B) 64 precedes 58 → 64 becomes 71's left child and 58 its left child. **Different.**
- (C) 30 again precedes 35. **Different.**
- (D) 46, 71, 58, 64 (58 before 64 ✓), 23, 35, 12, 89, 30 (35 before 30 ✓). All constraints hold. **Same tree.**

**Tip:** you never need to build four trees — just check 'ancestor before descendant' for the few deep nodes.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        46,
                        [
                            23,
                            [12],
                            [
                                35,
                                [30],
                                None,
                            ],
                        ],
                        [
                            71,
                            [
                                58,
                                None,
                                [64],
                            ],
                            [89],
                        ],
                    ],
                    'caption': 'Target BST',
                },
            ],
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def bld(s):
    t = None
    for k in s: t = ins(t, k)
    return t
base = bld([46, 23, 71, 12, 35, 58, 89, 30, 64])
opts = {'A': [46,23,71,30,12,35,58,89,64], 'B': [46,71,58,64,23,35,12,89,30],
        'C': [46,23,12,30,35,71,58,64,89], 'D': [46,71,23,89,64,58,12,35,30]}
assert [L for L in opts if bld(opts[L]) == base] == [ANSWER]
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — delete-max',
            'text': 'Two delete-max operations are performed on the max-heap [90, 72, 85, 40, 68, 80, 33, 15, 27, 61] (shown below). Each delete-max moves the last element to the root and sifts it down, always swapping with the larger child. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [90, 72, 85, 40, 68, 80, 33, 15, 27, 61],
                    'caption': 'Initial max-heap',
                },
            ],
            'options': [
                'After both deletions the key 27 is at index 5',
                'After both deletions the children of the root are 72 and 61',
                'The two deletions perform 3 swaps in total',
                'After the first delete-max the array is [85, 72, 80, 40, 68, 61, 33, 15, 27]',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Delete 90:** move 61 (last) to the root → [61, 72, 85, 40, 68, 80, 33, 15, 27]. 61 vs children 72, 85 → swap with 85 (index 2). Children of index 2: 80, 33 → swap with 80 (index 5), a leaf. Result [85, 72, 80, 40, 68, 61, 33, 15, 27] (2 swaps).

**Delete 85:** move 27 to the root → [27, 72, 80, 40, 68, 61, 33, 15]. Swap with 80 (index 2); children 61, 33 → swap with 61 (index 5); leaf. Result [80, 72, 61, 40, 68, 27, 33, 15] (2 swaps).

- (A) 27 ends at index 5. **True.**
- (B) Root 80 has children 72 (index 1) and 61 (index 2). **True.**
- (C) 2 + 2 = **4** swaps. **False.**
- (D) **True.**

**Trap:** swapping with the *left* child by default (72) would violate the heap property because 85 > 72.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [80, 72, 61, 40, 68, 27, 33, 15],
                    'highlight': [0, 2, 5],
                    'caption': 'After two delete-max operations',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

H = [90, 72, 85, 40, 68, 80, 33, 15, 27, 61]; sw = 0
def delmax():
    global sw
    H[0] = H[-1]; H.pop(); i, n = 0, len(H)
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and H[l] > H[m]: m = l
        if r < n and H[r] > H[m]: m = r
        if m == i: return
        H[i], H[m] = H[m], H[i]; i = m; sw += 1
delmax(); first = H[:]
delmax()
truth = {'A': first == [85, 72, 80, 40, 68, 61, 33, 15, 27], 'B': (H[1], H[2]) == (72, 61),
         'C': sw == 3, 'D': H.index(27) == 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — counting comparisons',
            'text': 'Quicksort using the Lomuto partition (pivot = **last** element of the sub-array; every test `A[j] <= pivot` is one comparison) sorts [4, 7, 2, 6, 1, 8, 3, 5]. Sub-arrays of size 0 or 1 are not partitioned. The total number of comparisons is ______.',
            'answer': '13',
            'solution': '''A Lomuto partition of a sub-array of size s makes exactly s − 1 comparisons. So we only need the sizes of all partitioned sub-arrays.

- [4, 7, 2, 6, 1, 8, 3, 5], pivot 5: **7** comparisons → [4, 2, 1, 3, **5**, 8, 6, 7].
- Left [4, 2, 1, 3], pivot 3: **3** → [2, 1, **3**, 4].
- [2, 1], pivot 1: **1** → [**1**, 2]. ([4] and [2] are size 1.)
- Right [8, 6, 7], pivot 7: **2** → [6, **7**, 8].

Total = 7 + 3 + 1 + 2 = **13**.

**Tip:** with C(s) = s − 1 + C(left) + C(right), the minimum for n = 8 is 7 + C(3) + C(4) = 7 + 2 + 4 = 13 (perfectly balanced splits) and the maximum is n(n−1)/2 = 28 (e.g. already sorted input). Here every pivot splits evenly, so this input hits the best case.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Partition calls',
                    'col_labels': ['sub-array', 'pivot', 'result', 'comparisons'],
                    'row_labels': ['1', '2', '3', '4'],
                    'rows': [
                        ['4 7 2 6 1 8 3 5', 5, '4 2 1 3 | 5 | 8 6 7', 7],
                        ['4 2 1 3', 3, '2 1 | 3 | 4', 3],
                        ['2 1', 1, '1 | 2', 1],
                        ['8 6 7', 7, '6 | 7 | 8', 2],
                    ],
                },
            ],
            'verify': '''
c = 0
def part(A, lo, hi):
    global c
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        c += 1
        if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]; return i + 1
def qs(A, lo, hi):
    if lo < hi:
        m = part(A, lo, hi); qs(A, lo, m - 1); qs(A, m + 1, hi)
A = [4, 7, 2, 6, 1, 8, 3, 5]; qs(A, 0, 7)
assert A == sorted(A) and c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — generator exhaustion with zip',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''g = (x * x for x in range(6))
a = list(zip(g, "abc"))
b = list(g)
print(a, b, sum(g))''',
            'options': [
                "`[(0, 'a'), (1, 'b'), (4, 'c')] [9, 16, 25] 50`",
                "`[(0, 'a'), (1, 'b'), (4, 'c')] [16, 25] 0`",
                "`[(0, 'a'), (1, 'b'), (4, 'c')] [9, 16, 25] 0`",
                "`[(0, 'a'), (1, 'b'), (4, 'c')] [0, 1, 4, 9, 16, 25] 55`",
            ],
            'answer': 'B',
            'solution': '''A generator can be consumed only once. `zip` pulls from its arguments **left to right** and stops when *any* argument is exhausted.

- Rounds 1–3: zip takes 0, 1, 4 from g and 'a', 'b', 'c'.
- Round 4: zip first takes **9 from g**, then finds "abc" exhausted and stops. The 9 is discarded.
- `list(g)` gets the remaining 16, 25.
- `sum(g)`: g is exhausted → 0.

Output: `[(0, 'a'), (1, 'b'), (4, 'c')] [16, 25] 0`.

- (A) and (C) assume zip stops *before* pulling the 4th element from g (it would, only if g were the shorter, second argument).
- (D) assumes generators restart.

**Trap:** with `zip("abc", g)` (string first) no element of g would be lost — argument order matters.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "[(0, 'a'), (1, 'b'), (4, 'c')] [16, 25] 0" and ANSWER == 'A'
g2 = (x * x for x in range(6)); list(zip("abc", g2))
assert list(g2) == [9, 16, 25]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra — counting successful relaxations',
            'text': "Dijkstra's algorithm is run from **S** on the directed graph shown below. A relaxation of edge (u, v) is *successful* if it strictly decreases d[v] (including a decrease from ∞). Edges into already-extracted vertices are ignored. The total number of successful relaxations is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 1],
                        ['S', 'C', 7],
                        ['B', 'A', 2],
                        ['B', 'D', 6],
                        ['A', 'C', 2],
                        ['A', 'D', 5],
                        ['C', 'D', 1],
                        ['C', 'E', 8],
                        ['D', 'E', 3],
                        ['B', 'E', 12],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.4],
                        'B': [2, -0.4],
                        'C': [4, 2.4],
                        'D': [4, -0.4],
                        'E': [6, 1],
                    },
                },
            ],
            'answer': '9',
            'solution': '''Every vertex other than S gets exactly one 'first' successful relaxation (from ∞); the rest are improvements.

- Extract S (0): A = 4 ✓, B = 1 ✓, C = 7 ✓ (3 successful)
- Extract B (1): A = min(4, 3) = 3 ✓; D = 7 ✓; E = 13 ✓ (3)
- Extract A (3): C = min(7, 5) = 5 ✓; D: 3 + 5 = 8 > 7 ✗ (1)
- Extract C (5): D = min(7, 6) = 6 ✓; E: 5 + 8 = 13, not < 13 ✗ (1)
- Extract D (6): E = min(13, 9) = 9 ✓ (1)
- Extract E (9): no out-edges.

Total = 3 + 3 + 1 + 1 + 1 = **9**. Final distances: A 3, B 1, C 5, D 6, E 9.

**Trap:** C → E gives 13, which *equals* the current value — a tie is not a successful relaxation.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'd[·] after each extraction (✓ = changed)',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'row_labels': ['S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '4 ✓', '1 ✓', '7 ✓', '∞', '∞'],
                        [0, '3 ✓', 1, 7, '7 ✓', '13 ✓'],
                        [0, 3, 1, '5 ✓', 7, 13],
                        [0, 3, 1, 5, '6 ✓', 13],
                        [0, 3, 1, 5, 6, '9 ✓'],
                    ],
                },
            ],
            'verify': '''
E = [('S','A',4),('S','B',1),('S','C',7),('B','A',2),('B','D',6),('A','C',2),('A','D',5),
     ('C','D',1),('C','E',8),('D','E',3),('B','E',12)]
G = {v: [] for v in 'SABCDE'}
for u, v, w in E: G[u].append((v, w))
d = {v: float('inf') for v in G}; d['S'] = 0; done = set(); succ = 0
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: (d[v], v)); done.add(u)
    for v, w in G[u]:
        if v not in done and d[u] + w < d[v]: d[v] = d[u] + w; succ += 1
assert succ == int(ANSWER) and d['E'] == 9
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Topological sorting',
            'text': 'Which of the following are valid topological orderings of the DAG shown below?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [2, 2.5],
                        'D': [2, 1],
                        'E': [2, -0.5],
                        'F': [4, 2],
                        'G': [4, 0],
                    },
                },
            ],
            'options': [
                'A, B, D, C, E, G, F',
                'A, E, B, D, C, F, G',
                'B, E, A, D, C, G, F',
                'A, C, F, B, D, E, G',
            ],
            'answer': ['A', 'C'],
            'solution': '''An ordering is topological iff for **every** edge u → v, u appears before v. Check each option against the 8 edges A→C, A→D, B→D, B→E, C→F, D→F, D→G, E→G.

- (A) A, B, D, C, E, G, F: all hold (E before G, C and D before F). **Valid.**
- (B) E comes before B, violating B → E. **Invalid.**
- (C) B, E, A, D, C, G, F: B<D, B<E, A<C, A<D, C<F, D<F, D<G, E<G all hold. **Valid.**
- (D) F comes before D, violating D → F. **Invalid.**

(In total this DAG has 42 topological orderings.)

**Tip:** scan each option once, maintaining the set of already-placed vertices, and verify that all in-neighbours of the current vertex are already placed.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from itertools import permutations
DG = {'A': 'CD', 'B': 'DE', 'C': 'F', 'D': 'FG', 'E': 'G', 'F': '', 'G': ''}
def ok(p):
    pos = {v: i for i, v in enumerate(p)}
    return all(pos[u] < pos[v] for u in DG for v in DG[u])
opts = ["BEADCGF", "ABDCEGF", "AEBDCFG", "ACFBDEG"]
assert [L for L, s in zip('ABCD', opts) if ok(s)] == sorted(ANSWER)
assert sum(ok(p) for p in permutations(DG)) == 42
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — double hashing',
            'text': 'Keys 27, 40, 14, 53, 66, 79, 1 are inserted in this order into an empty hash table of size 13 using double hashing: probe i (i = 0, 1, 2, …) examines slot (h₁(k) + i · h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). Counting every slot examined, the total number of probes over all seven insertions is ______.',
            'answer': '13',
            'solution': '''Double hashing uses a key-dependent step h₂(k), so keys colliding at the same home slot follow **different** probe sequences.

- 27: h₁ = 1 → slot 1 (1 probe)
- 40: h₁ = 1 (full), h₂ = 1 + 7 = 8 → slot 9 (2 probes)
- 14: h₁ = 1 (full), h₂ = 1 + 3 = 4 → slot 5 (2)
- 53: h₁ = 1 (full), h₂ = 1 + 9 = 10 → slot 11 (2)
- 66: h₁ = 1 (full), h₂ = 1 + 0 = 1 → slot 2 (2)
- 79: h₁ = 1 (full), h₂ = 1 + 2 = 3 → slot 4 (2)
- 1: h₁ = 1 (full), h₂ = 1 + 1 = 2 → slot 3 (2)

Total = 1 + 6 × 2 = **13** probes.

**Trap:** all seven keys are ≡ 1 (mod 13). With linear probing they would form one long cluster costing 1 + 2 + … + 7 = 28 probes; double hashing spreads them out.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        1: 27,
                        2: 66,
                        3: 1,
                        4: 79,
                        5: 14,
                        9: 40,
                        11: 53,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
m = 13; T = [None] * m; tot = 0
for k in [27, 40, 14, 53, 66, 79, 1]:
    h1, h2, i = k % 13, 1 + k % 11, 0
    while True:
        tot += 1
        s = (h1 + i * h2) % m
        if T[s] is None: T[s] = k; break
        i += 1
assert tot == int(ANSWER) and T[3] == 1
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Bottom-up merge sort — intermediate state',
            'text': 'Bottom-up (iterative) merge sort is applied to [38, 16, 27, 39, 12, 27, 5, 44]. Pass 1 merges adjacent runs of length 1, pass 2 merges adjacent runs of length 2, and so on. The array after **pass 2** is',
            'options': [
                '[5, 12, 16, 27, 27, 38, 39, 44]',
                '[16, 38, 27, 39, 12, 27, 5, 44]',
                '[16, 27, 38, 39, 5, 12, 27, 44]',
                '[16, 27, 38, 39, 12, 27, 5, 44]',
            ],
            'answer': 'C',
            'solution': '''Bottom-up merge sort merges runs of width 1, 2, 4, … across the whole array in each pass.

- Pass 1 (pairs): [38,16]→[16,38]; [27,39]→[27,39]; [12,27]→[12,27]; [5,44]→[5,44]. Array: [16, 38, 27, 39, 12, 27, 5, 44].
- Pass 2 (merge runs of 2): [16,38]+[27,39] → [16, 27, 38, 39]; [12,27]+[5,44] → [5, 12, 27, 44]. Array: **[16, 27, 38, 39, 5, 12, 27, 44]**.
- Pass 3 would give the sorted array.

- (A) is after pass 3.
- (B) is the array after pass 1.
- (D) merges only the left half in pass 2 — a top-down order of work, not bottom-up.

**Tip:** after pass p, every aligned block of length 2^{p} is sorted.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', 'pass 1', 'pass 2', 'pass 3'],
                    'rows': [
                        [38, 16, 27, 39, 12, 27, 5, 44],
                        [16, 38, 27, 39, 12, 27, 5, 44],
                        [16, 27, 38, 39, 5, 12, 27, 44],
                        [5, 12, 16, 27, 27, 38, 39, 44],
                    ],
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

def merge(L, R):
    o = []; i = j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
B = [38, 16, 27, 39, 12, 27, 5, 44]
for w in (1, 2):
    B = sum([merge(B[i:i + w], B[i + w:i + 2 * w]) for i in range(0, 8, 2 * w)], [])
assert B == [16, 27, 38, 39, 5, 12, 27, 44] and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — class versus instance attributes',
            'text': 'Consider the following Python program. Which of the following statements about its output is/are TRUE?',
            'code': '''class Counter:
    total = 0
    tags = []

    def __init__(self, name):
        self.name = name
        Counter.total += 1
        self.tags.append(name)

    def bump(self):
        self.total += 1

a = Counter("x")
b = Counter("y")
a.bump(); a.bump()
b.tags = ["z"]
print(Counter.total, a.total, b.total,
      len(a.tags), len(Counter.tags), b.tags)''',
            'options': [
                'The fourth value printed is 1',
                "The last value printed is `['z']`, and `Counter.tags` is not affected by that assignment",
                'The second value printed is 4',
                'The first value printed is 2',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Attribute **lookup** on an instance falls back to the class; attribute **assignment** on an instance always creates/updates an instance attribute. Mutating a class-level list through an instance changes the shared list.

- Two constructions: `Counter.total` = 2; `self.tags.append` mutates the **shared** class list → Counter.tags = ['x', 'y'].
- `a.bump()`: `self.total += 1` reads 2 (class), then assigns a.total = 3 (new instance attribute); second bump → a.total = 4. Counter.total stays 2.
- `b.total` has no instance attribute → class value 2.
- `b.tags = ['z']` creates an instance attribute on b only.

Output: `2 4 2 2 2 ['z']`.

- (A) a.tags is the shared class list of length **2**. **False.**
- (B) **True** — rebinding `b.tags` does not touch `Counter.tags`.
- (D) **True.** (C) **True.**

**Trap:** `self.x += 1` on an immutable class attribute *shadows* it, while `self.lst.append()` on a mutable class attribute *shares* it.''',
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

vals = OUTPUT.split(maxsplit=5)
assert vals[:5] == ['2', '4', '2', '2', '2'] and vals[5].strip() == "['z']"
truth = {'A': vals[0] == '2', 'B': vals[1] == '4', 'C': vals[3] == '1',
         'D': vals[5].strip() == "['z']" and Counter.tags == ['x', 'y']}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
    ],
}
