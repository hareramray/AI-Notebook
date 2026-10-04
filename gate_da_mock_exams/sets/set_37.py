# Set 37 — Full-Syllabus Mock — Paper 7
SET = {
    'number': 37,
    'title': 'Full-Syllabus Mock — Paper 7',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — floor division, modulo, rounding',
            'text': 'Consider the following Python program. What is printed?',
            'code': 'print(-17 // 5, -17 % 5, 17 // -5, round(-2.5))',
            'options': ['`-3 -2 -3 -3`', '`-4 3 -4 -2`', '`-4 -2 -4 -3`', '`-3 3 -4 -2`'],
            'answer': 'B',
            'solution': '''Python's `//` is **floor** division (rounds toward −∞), and `%` is defined so that a == (a // b) * b + a % b, which makes the remainder take the sign of the **divisor**. `round` uses round-half-to-even (banker's rounding).

- −17 / 5 = −3.4 → floor → **−4**.
- −17 % 5 = −17 − (−4)(5) = −17 + 20 = **3**.
- 17 / −5 = −3.4 → floor → **−4**.
- round(−2.5): halfway between −3 and −2 → the even one, **−2**.

Output: `-4 3 -4 -2`.

- (A) truncates toward zero (C/Java semantics) and rounds half away from zero.
- (C) gets floor right but uses a C-style negative remainder and the wrong rounding.
- (D) truncates in the first expression only — inconsistent.

**Trap:** in C, −17 / 5 = −3 and −17 % 5 = −2; Python differs on both.''',
            'verify': "assert OUTPUT.strip() == '-4 3 -4 -2' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — infix to postfix',
            'text': 'The infix expression `a - b * ( c + d / e ^ f ) * g + h` is converted to postfix with the standard operator-stack algorithm. Precedence: `^` (highest, right-associative), then `*` `/`, then `+` `-` (left-associative). Left parentheses are pushed onto the same stack. The maximum number of symbols (operators and parentheses) on the stack at any moment is ______.',
            'answer': '6',
            'solution': '''Rules: operands go straight to the output; `(` is pushed; `)` pops to the matching `(`; an operator first pops operators of higher precedence (or equal precedence if left-associative), then is pushed.

Stack after each token (bottom → top):

- `-` → [−]
- `*` → [−, *] (higher than −, no pop)
- `(` → [−, *, (]
- `+` → [−, *, (, +]
- `/` → [−, *, (, +, /]
- `^` → [−, *, (, +, /, ^] ← **6 symbols**
- `)` → pops ^, /, + and the ( → [−, *]
- `*` → pops the equal-precedence * (left-assoc), pushes * → [−, *]
- `+` → pops *, then − → [+]
- end → pop +

Maximum = **6**. Postfix: `a b c d e f ^ / + * g * - h +`.

**Trap:** forgetting to count the `(`, which occupies a stack slot (answer 5).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['−', '*', '(', '+', '/', '^'],
                    'label': 'Stack after reading ^',
                },
            ],
            'verify': '''
prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
st = []; out = []; mx = 0
for t in 'a - b * ( c + d / e ^ f ) * g + h'.split():
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
assert mx == int(ANSWER) and ' '.join(out) == 'a b c d e f ^ / + * g * - h +'
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Doubly linked lists — deletion',
            'text': 'In a doubly linked list, node p is neither the first nor the last node. Each node has fields `prev` and `next`. Which one of the following statement sequences correctly removes p from the list (so that forward and backward traversals both skip p)?',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': ['x', 'p', 'y'],
                    'doubly': True,
                    'caption': 'x ⇄ p ⇄ y (part of a longer list)',
                },
            ],
            'options': [
                '`p.next.prev = p.prev; p.prev.next = p.next.prev`',
                '`p.prev.next = p.next; p.next.prev = p.prev.next`',
                '`p.prev.next = p.next; p.next.prev = p.prev`',
                '`p.next = p.next.next; p.next.prev = p`',
            ],
            'answer': 'C',
            'solution': '''Removing p requires exactly two pointer changes: x.next must become y, and y.prev must become x (where x = p.prev and y = p.next). p's own fields can stay as they are.

- (A) After the first statement, `p.next.prev` *is* x, so the second sets x.next = x — forward traversal loops at x.
- (B) After the first statement, `p.prev.next` *is* y, so the second sets y.prev = y — a self-loop; backward traversal breaks.
- (C) x.next = y; y.prev = x. **Correct.** (The two statements are independent, so their order does not matter.)
- (D) Deletes y (the node *after* p), not p.

**Trap:** an expression like `p.prev.next` must be re-evaluated *after* earlier assignments — chained pointer expressions change meaning once a link is redirected.''',
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

class N:
    def __init__(s, v): s.v, s.prev, s.next = v, None, None
def mk():
    ns = [N(c) for c in 'wxpyz']
    for a, b in zip(ns, ns[1:]): a.next, b.prev = b, a
    return ns[0], ns[-1], ns[2]
def fwd(h):
    o = []
    while h and len(o) < 10: o.append(h.v); h = h.next
    return ''.join(o)
def bwd(t):
    o = []
    while t and len(o) < 10: o.append(t.v); t = t.prev
    return ''.join(o)
def A(p): p.prev.next = p.next; p.next.prev = p.prev
def B(p): p.prev.next = p.next; p.next.prev = p.prev.next
def C(p): p.next.prev = p.prev; p.prev.next = p.next.prev
def D(p): p.next = p.next.next; p.next.prev = p
ok = []
for L, f in zip('ABCD', (A, B, C, D)):
    h, t, p = mk(); f(p)
    ok.append(fwd(h) == 'wxyz' and bwd(t) == 'zyxw')
assert [L for L, o in zip('ABCD', ok) if o] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — double hashing',
            'text': 'Keys 18, 41, 44, 31, 57, 83 are inserted in this order into an empty table of size 13 using double hashing: the i-th probe (i = 0, 1, 2, …) for key k is (h₁(k) + i·h₂(k)) mod 13, with h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). The index of the slot in which 83 is stored is ______.',
            'answer': '0',
            'solution': '''Unlike linear/quadratic probing, keys with the same home slot get *different* step sizes h₂, so they follow different probe sequences.

- 18: h₁ = 5 → slot 5.
- 41: h₁ = 2 → slot 2.
- 44: h₁ = 5 (full), h₂ = 1 + 0 = 1 → 6 → slot 6.
- 31: h₁ = 5, h₂ = 1 + 9 = 10 → 15 mod 13 = 2 (full) → 25 mod 13 = 12 → slot 12.
- 57: h₁ = 5, h₂ = 1 + 2 = 3 → 8 → slot 8.
- 83: h₁ = 83 mod 13 = 5, h₂ = 1 + (83 mod 11) = 1 + 6 = 7. Probes: 5 (full), 12 (full, 31), 19 mod 13 = 6 (full, 44), 26 mod 13 = **0** (empty) → slot **0**.

**Trap:** computing the probe as (previous slot + i·h₂) instead of (h₁ + i·h₂), or using h₂ = k mod 11 without the +1 (which could be 0 and loop forever).''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        0: 83,
                        2: 41,
                        5: 18,
                        6: 44,
                        8: 57,
                        12: 31,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None]*13
for k in [18, 41, 44, 31, 57, 83]:
    for i in range(13):
        s = (k % 13 + i*(1 + k % 11)) % 13
        if T[s] is None: T[s] = k; break
assert T.index(83) == int(ANSWER) and T[12] == 31
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'BST search paths',
            'text': 'A binary search tree contains distinct integer keys, including 55. Which of the following could be the sequence of keys examined, in order, during a search for 55?',
            'options': [
                '90, 20, 70, 30, 60, 50, 55',
                '10, 80, 35, 75, 40, 70, 55',
                '60, 25, 58, 40, 62, 55',
                '52, 70, 54, 65, 53, 55',
            ],
            'answer': ['A', 'B'],
            'solution': '''Each examined key narrows the interval in which all later keys must lie: going left after key k sets the upper bound to k, going right sets the lower bound to k. A sequence is valid iff every key lies inside the current interval.

- (A) (−∞,∞) → 90 L (−∞,90) → 20 R (20,90) → 70 L (20,70) → 30 R (30,70) → 60 L (30,60) → 50 R (50,60) → 55 ✓. **Possible.**
- (B) 10 R (10,∞) → 80 L (10,80) → 35 R (35,80) → 75 L (35,75) → 40 R (40,75) → 70 L (40,70) → 55 ✓. **Possible.**
- (C) 60 L (−∞,60) → 25 R (25,60) → 58 L (25,58) → 40 R (40,58) → **62** ∉ (40,58). **Impossible** — 62 cannot lie in the left subtree of 60.
- (D) 52 R (52,∞) → 70 L (52,70) → 54 R (54,70) → 65 L (54,65) → **53** ∉ (54,65). **Impossible.**

**Trap:** checking only consecutive pairs (each step “moves toward 55”) is not enough — all earlier bounds still apply.''',
            'verify': '''
def ok(seq, x=55):
    lo, hi = float('-inf'), float('inf')
    for k in seq[:-1]:
        if not lo < k < hi: return False
        if x < k: hi = k
        else: lo = k
    return seq[-1] == x and lo < x < hi
opts = [[90,20,70,30,60,50,55],[10,80,35,75,40,70,55],[60,25,58,40,62,55],[52,70,54,65,53,55]]
assert [L for L, s in zip('ABCD', opts) if ok(s)] == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Selection sort is not stable',
            'text': 'Consider the following Python program, which sorts records by their numeric key. What is printed?',
            'code': '''recs = [(3, 'a'), (1, 'b'), (3, 'c'), (2, 'd'), (1, 'e')]
for i in range(len(recs) - 1):
    m = i
    for j in range(i + 1, len(recs)):
        if recs[j][0] < recs[m][0]:
            m = j
    recs[i], recs[m] = recs[m], recs[i]
print(''.join(r[1] for r in recs))''',
            'options': ['`bedca`', '`bedac`', '`ebdac`', '`ebdca`'],
            'answer': 'A',
            'solution': '''Selection sort swaps the minimum into position i; the long-distance swap can jump an element over another with an equal key, so the algorithm is **not stable**.

- i = 0: minimum key 1 first found at index 1 ('b') → swap with (3,'a') → b, a, c, d, e  (keys 1, 3, 3, 2, 1)
- i = 1: minimum key 1 at index 4 ('e') → swap with (3,'a') → b, e, c, d, a
- i = 2: minimum key 2 at index 3 ('d') → swap with (3,'c') → b, e, d, c, a
- i = 3: (3,'c') vs (3,'a') — strict `<` finds no smaller → no change

Output: `bedca`. The two key-3 records ended in the order c, a — reversed relative to the input.

- (B) `bedac` is the **stable** order (what `sorted(recs, key=lambda r: r[0])` gives).
- (C) `ebdac` is what the code would print with `<=` (choosing the *last* minimum).
- (D) `ebdca` mixes the two rules and is produced by neither version.

**Trap:** strict `<` keeps the *first* minimum, which preserves order among the minima, but the element displaced by the swap ('a') can still leap past its equal ('c').''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == 'bedca' and ANSWER == 'B'
assert ''.join(r[1] for r in sorted([(3,'a'),(1,'b'),(3,'c'),(2,'d'),(1,'e')],
                                    key=lambda r: r[0])) == 'bedac'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Recurrences — exact value',
            'text': 'Let T(1) = 1 and T(n) = 3·T(n/3) + n for n a power of 3 greater than 1. The value of T(81) is ______.',
            'answer': '405',
            'solution': '''Unroll: each level of the recursion tree does total work n (3^{i} subproblems of size n/3^{i}), and there are log₃ n levels of this kind plus the n leaves costing T(1) = 1 each.

T(n) = n·log₃ n + n·T(1) = n(log₃ n + 1).

For n = 81 = 3⁴: T(81) = 81 × (4 + 1) = **405**.

Step-by-step check:

- T(3) = 3·1 + 3 = 6
- T(9) = 3·6 + 9 = 27
- T(27) = 3·27 + 27 = 108
- T(81) = 3·108 + 81 = 405

Asymptotically T(n) = Θ(n log n) (Master theorem case 2: a = b = 3, f(n) = n = n^{log₃ 3}).

**Trap:** forgetting the leaf level — n·log₃ n alone gives 324.''',
            'verify': '''
def T(n): return 1 if n == 1 else 3 * T(n // 3) + n
assert T(81) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph theory — edges vs components',
            'text': 'The maximum number of edges in a simple undirected graph with 10 vertices and exactly 3 connected components is',
            'options': ['21', '27', '28', '36'],
            'answer': 'C',
            'solution': '''For a fixed number of components, edges are maximised by making each component complete. With component sizes n₁ + n₂ + n₃ = 10 the edge count is ∑ C(nᵢ, 2), and because C(x, 2) is convex, the sum is largest when the sizes are as **unbalanced** as possible: two isolated vertices and one K₈.

- Sizes (8, 1, 1): C(8,2) = **28**
- Sizes (7, 2, 1): 21 + 1 = 22
- Sizes (4, 3, 3): 6 + 3 + 3 = 12

General formula: C(n − k + 1, 2) = C(8, 2) = 28 for n = 10, k = 3.

- (A) 21 = C(7, 2) uses a K₇ (off by one).
- (B) 27 is not achievable by any split.
- (D) 36 = C(9, 2) is the maximum with only **2** components.

**Trap:** spreading vertices evenly *minimises* the edge count among complete components.''',
            'verify': '''
best = max(a*(a-1)//2 + b*(b-1)//2 + c*(c-1)//2
           for a in range(1, 9) for b in range(1, 9) for c in range(1, 9) if a + b + c == 10)
assert best == 28 and ['21','27','28','36'][ord(ANSWER) - 65] == '28'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — dict accumulation with enumerate',
            'text': 'The value printed by the following Python program is ______.',
            'code': '''s = "abracadabra"
d = {}
for i, c in enumerate(s):
    d[c] = d.get(c, 0) + i
print(d['a'] - d['b'])''',
            'answer': '16',
            'solution': '''`enumerate` yields (index, character) pairs starting at 0, and `d.get(c, 0)` returns 0 for a new key, so `d[c]` ends up as the **sum of the indices** at which c occurs.

Indices: a b r a c a d a b r a → 0 1 2 3 4 5 6 7 8 9 10.

- 'a' occurs at 0, 3, 5, 7, 10 → sum 25.
- 'b' occurs at 1, 8 → sum 9.

Printed value = 25 − 9 = **16**.

**Trap:** counting occurrences (5 − 2 = 3) instead of summing indices, or indexing from 1 (which would give 30 − 11 = 19).''',
            'verify': "assert OUTPUT.strip() == ANSWER and d['a'] == 25 and d['b'] == 9",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Queue using two stacks',
            'text': 'A queue is implemented with two stacks S1 and S2. Enqueue pushes onto S1. Dequeue pops from S2; if S2 is empty it first pops **every** element of S1 and pushes it onto S2. Starting empty, the operations are: enqueue 1, 2, 3, 4; dequeue; enqueue 5, 6; dequeue; enqueue 7. Which of the following statements is/are TRUE afterwards?',
            'options': [
                'S2 holds exactly 2 elements and 3 is on its top',
                'S1 holds 5, 6, 7 with 7 on top',
                'Exactly 4 element transfers from S1 to S2 have taken place so far',
                'The next dequeue will trigger a transfer from S1 to S2',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Trace (stacks written bottom → top):

- enqueue 1..4 → S1 = [1, 2, 3, 4], S2 = []
- dequeue: S2 empty → transfer 4 elements → S2 = [4, 3, 2, 1]; pop → returns 1; S2 = [4, 3, 2]
- enqueue 5, 6 → S1 = [5, 6]
- dequeue: S2 non-empty → pop → returns 2; S2 = [4, 3]
- enqueue 7 → S1 = [5, 6, 7]

- (A) **True** — S2 = [4, 3], top 3 (the next element to leave the queue).
- (B) **True.**
- (C) **True** — only the first dequeue transferred, moving 4 elements.
- (D) **False** — S2 is non-empty, so the next dequeue just pops 3.

**Tip:** each element is pushed and popped at most twice in total, so any sequence of n operations costs O(n) — amortised O(1) per operation, although one dequeue can cost Θ(n).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [5, 6, 7],
                    'label': 'S1',
                },
                {
                    'type': 'stack',
                    'values': [4, 3],
                    'label': 'S2',
                },
            ],
            'verify': '''
S1, S2 = [], []; moves = 0; out = []
def enq(x): S1.append(x)
def deq():
    global moves
    if not S2:
        while S1: S2.append(S1.pop()); moves += 1
    return S2.pop()
for x in (1, 2, 3, 4): enq(x)
out.append(deq()); enq(5); enq(6); out.append(deq()); enq(7)
assert out == [1, 2] and S2 == [4, 3] and S1 == [5, 6, 7] and moves == 4
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — closures with nonlocal',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def make():
    total = 0
    def add(x):
        nonlocal total
        total += x
        return total
    return add

a = make()
b = make()
print(a(3), a(4), b(5), a(b(1)))''',
            'options': ['`3 7 12 26`', '`3 7 5 13`', '`3 7 5 8`', '`3 4 5 7`'],
            'answer': 'B',
            'solution': '''Each call to `make()` creates a **new** local variable `total` and a new closure `add` that captures it. `nonlocal` lets `add` rebind that captured variable, so each closure keeps its own running sum.

Arguments are evaluated left to right:

- `a(3)`: a's total 0 → 3 → prints 3
- `a(4)`: a's total 3 → 7 → prints 7
- `b(5)`: b's total (separate) 0 → 5 → prints 5
- `a(b(1))`: first b(1): 5 → 6; then a(6): 7 → 13 → prints 13

Output: `3 7 5 13`.

- (A) assumes a and b share one `total` (as if it were a global).
- (C) adds only b(1) = 1 inside a (forgets b's accumulated 5).
- (D) assumes `total` resets on every call (no accumulation).

**Trap:** without `nonlocal`, `total += x` would raise `UnboundLocalError`, because the assignment makes `total` local to `add`.''',
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '3 7 5 13' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Min-heap insert and extract-min',
            'text': 'The binary min-heap shown is stored (0-indexed) as `[3, 8, 5, 12, 9, 7, 6, 15, 20, 11]`. The following operations are performed in order: insert 4; extract-min; extract-min. Insertion appends and sifts up; extract-min moves the last element to the root and sifts it down, exchanging with the smaller child. After these operations, the key at index 6 of the array is ______.',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 8, 5, 12, 9, 7, 6, 15, 20, 11],
                    'caption': 'Initial min-heap',
                },
            ],
            'answer': '11',
            'solution': '''**Insert 4** at index 10. Parent index 4 holds 9 > 4 → swap; parent index 1 holds 8 > 4 → swap; parent index 0 holds 3 < 4 → stop.
`[3, 4, 5, 12, 8, 7, 6, 15, 20, 11, 9]`

**Extract-min #1** (removes 3): last key 9 moves to the root → `[9, 4, 5, 12, 8, 7, 6, 15, 20, 11]`.

- 9 vs children 4, 5 → swap with 4 (index 1)
- 9 vs children 12, 8 → swap with 8 (index 4)
- 9 vs child 11 (index 9) → stop.

`[4, 8, 5, 12, 9, 7, 6, 15, 20, 11]`

**Extract-min #2** (removes 4): last key 11 to the root → `[11, 8, 5, 12, 9, 7, 6, 15, 20]`.

- 11 vs 8, 5 → swap with 5 (index 2)
- 11 vs 7, 6 → swap with 6 (index 6)
- index 6 has no children (13, 14 out of range) → stop.

`[5, 8, 6, 12, 9, 7, 11, 15, 20]`

Key at index 6 = **11**.

**Trap:** in the second extraction, exchanging 11 with the *left* child 8 instead of the smaller child 5 would put 8 above 5 — not a heap. Always pick the smaller child in a min-heap.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [5, 8, 6, 12, 9, 7, 11, 15, 20],
                    'highlight': [11],
                    'caption': 'Final heap',
                },
            ],
            'verify': '''
h = [3, 8, 5, 12, 9, 7, 6, 15, 20, 11]
def up(i):
    while i and h[(i-1)//2] > h[i]: p = (i-1)//2; h[p], h[i] = h[i], h[p]; i = p
def down(i):
    n = len(h)
    while True:
        l, r, m = 2*i+1, 2*i+2, i
        if l < n and h[l] < h[m]: m = l
        if r < n and h[r] < h[m]: m = r
        if m == i: return
        h[i], h[m] = h[m], h[i]; i = m
def pop():
    x = h[0]; h[0] = h[-1]; h.pop(); down(0); return x
h.append(4); up(10)
assert pop() == 3 and pop() == 4
assert h == [5, 8, 6, 12, 9, 7, 11, 15, 20] and h[6] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'DFS edge classification',
            'text': 'DFS is run on the directed graph shown, starting at A; neighbours are explored in alphabetical order, and if unvisited vertices remained a new DFS would start at the alphabetically smallest one. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'F'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['D', 'A'],
                        ['E', 'B'],
                        ['E', 'D'],
                        ['F', 'C'],
                        ['F', 'G'],
                        ['G', 'F'],
                    ],
                    'pos': {
                        'A': [2, 3],
                        'B': [0.5, 1.8],
                        'C': [2, 1.6],
                        'F': [3.6, 1.8],
                        'D': [0, 0],
                        'E': [1.6, 0],
                        'G': [3.6, 0],
                    },
                },
            ],
            'options': [
                'Exactly 3 edges are back edges',
                'F → C is a cross edge',
                'The DFS has at least one forward edge',
                'E → D is a back edge',
            ],
            'answer': ['A', 'B'],
            'solution': '''Classify edge u → v using discovery/finish times: **tree** (v first discovered via it), **back** (v is an ancestor still active), **forward** (v is a finished descendant), **cross** (v finished, not a descendant).

Trace (time: discover/finish):

- A 1 → B 2 → D 3: D → A is to an active ancestor (back). D finishes 4.
- B → E: E 5. E → B back (B active); E → D: D finished, not a descendant of E (cross). E finishes 6.
- B finishes 7. A → C: C 8; C → E: E finished in B's subtree (cross). C finishes 9.
- A → F: F 10; F → C: finished, not a descendant (cross); F → G: G 11; G → F back. G 12, F 13, A 14.

Tree: A→B, B→D, B→E, A→C, A→F, F→G (6). Back: D→A, E→B, G→F (3). Cross: E→D, C→E, F→C (3). Forward: none.

- (A) **True.**
- (B) **True.**
- (C) **False** — no edge goes from an ancestor to an already-finished descendant.
- (D) **False** — D had already finished, so E → D is a cross edge.

**Trap:** calling E → D a back edge because D was discovered earlier; a back edge requires the target to be an *active ancestor* (discovered but not finished).''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'F'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['D', 'A'],
                        ['E', 'B'],
                        ['E', 'D'],
                        ['F', 'C'],
                        ['F', 'G'],
                        ['G', 'F'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['A', 'C'],
                        ['A', 'F'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [2, 3],
                        'B': [0.5, 1.8],
                        'C': [2, 1.6],
                        'F': [3.6, 1.8],
                        'D': [0, 0],
                        'E': [1.6, 0],
                        'G': [3.6, 0],
                    },
                    'caption': 'DFS tree edges highlighted',
                },
            ],
            'verify': '''
G = {'A':'BCF','B':'DE','C':'E','D':'A','E':'BD','F':'CG','G':'F'}
t = [0]; d = {}; f = {}; par = {}
def dfs(u):
    t[0] += 1; d[u] = t[0]
    for v in G[u]:
        if v not in d: par[v] = u; dfs(v)
    t[0] += 1; f[u] = t[0]
for u in sorted(G):
    if u not in d: dfs(u)
cls = {}
for u in G:
    for v in G[u]:
        if par.get(v) == u: c = 'tree'
        elif d[v] <= d[u] and f[v] >= f[u]: c = 'back'
        elif d[v] > d[u]: c = 'fwd'
        else: c = 'cross'
        cls[u + v] = c
vals = [list(cls.values()).count('back') == 3, cls['FC'] == 'cross',
        'fwd' in cls.values(), cls['ED'] == 'back']
assert [L for L, v in zip('ABCD', vals) if v] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra — undirected weighted graph',
            'text': "Dijkstra's algorithm is run from S on the undirected weighted graph shown. The shortest-path distance from S to E is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 2],
                        ['A', 'C', 7],
                        ['B', 'D', 3],
                        ['C', 'T', 2],
                        ['D', 'C', 1],
                        ['D', 'E', 6],
                        ['E', 'T', 2],
                        ['B', 'E', 9],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.2],
                        'B': [1.5, -0.2],
                        'C': [3.5, 2.2],
                        'D': [3.5, -0.2],
                        'T': [5.2, 2.2],
                        'E': [5.2, -1.6],
                    },
                },
            ],
            'answer': '12',
            'solution': '''Extraction order with distances:

- S (0): A = 2, B = 5
- A (2): B = min(5, 4) = 4; C = 9
- B (4): D = 7; E = 4 + 9 = 13
- D (7): C = min(9, 8) = 8; E = min(13, 7 + 6) = 13
- C (8): T = 10
- T (10): E = min(13, 10 + 2) = **12**
- E (12)

Shortest path S → A → B → D → C → T → E with cost 2 + 2 + 3 + 1 + 2 + 2 = **12**.

Both “direct” routes into E (via B: 13, via D: 13) are beaten by the six-edge detour through T — the number of edges is irrelevant, only total weight counts.

**Trap:** stopping as soon as E receives a finite label (13). A label is final only when the vertex is **extracted**.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'T'],
                    'edges': [
                        ['S', 'A', 2],
                        ['S', 'B', 5],
                        ['A', 'B', 2],
                        ['A', 'C', 7],
                        ['B', 'D', 3],
                        ['C', 'T', 2],
                        ['D', 'C', 1],
                        ['D', 'E', 6],
                        ['E', 'T', 2],
                        ['B', 'E', 9],
                    ],
                    'highlight_edges': [
                        ['S', 'A'],
                        ['A', 'B'],
                        ['B', 'D'],
                        ['D', 'C'],
                        ['C', 'T'],
                        ['T', 'E'],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.2],
                        'B': [1.5, -0.2],
                        'C': [3.5, 2.2],
                        'D': [3.5, -0.2],
                        'T': [5.2, 2.2],
                        'E': [5.2, -1.6],
                    },
                    'caption': 'Shortest-path tree',
                },
            ],
            'verify': '''
import heapq
E = [('S','A',2),('S','B',5),('A','B',2),('A','C',7),('B','D',3),('C','T',2),
     ('D','C',1),('D','E',6),('E','T',2),('B','E',9)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: float('inf') for v in G}; d['S'] = 0; pq = [(0, 'S')]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert d['E'] == int(ANSWER) and d['T'] == 10
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — Hoare partition',
            'text': '''Hoare's partition (pivot p = A[lo]) is applied once to `A = [15, 22, 7, 31, 15, 4, 18, 10, 26, 3]` with lo = 0, hi = 9:

i = lo − 1, j = hi + 1; repeat { decrement j until A[j] ≤ p; increment i until A[i] ≥ p; if i < j swap A[i], A[j] else return j }.

Which option gives the array after the call, and the returned index?''',
            'options': [
                '`[3, 10, 7, 15, 4, 31, 18, 22, 26, 15]`, returns 3',
                '`[3, 10, 7, 4, 15, 31, 18, 22, 26, 15]`, returns 5',
                '`[10, 3, 7, 4, 15, 15, 18, 22, 26, 31]`, returns 4',
                '`[3, 10, 7, 4, 15, 31, 18, 22, 26, 15]`, returns 4',
            ],
            'answer': 'D',
            'solution': '''Hoare's scheme moves i right past keys < p and j left past keys > p, swapping out-of-place pairs. Keys equal to the pivot stop **both** scans. Unlike Lomuto, the pivot need not end in its final position; the call guarantees only A[lo..j] ≤ p ≤ A[j+1..hi].

p = 15.

- Round 1: j from 10 → 9 (A[9] = 3 ≤ 15); i from −1 → 0 (A[0] = 15 ≥ 15). Swap → `[3, 22, 7, 31, 15, 4, 18, 10, 26, 15]`
- Round 2: j → 8 (26), 7 (10 ≤ 15) stop; i → 1 (22 ≥ 15) stop. Swap → `[3, 10, 7, 31, 15, 4, 18, 22, 26, 15]`
- Round 3: j → 6 (18), 5 (4) stop; i → 2 (7), 3 (31) stop. Swap → `[3, 10, 7, 4, 15, 31, 18, 22, 26, 15]`
- Round 4: j → 4 (15 ≤ 15) stop; i → 4 (15 ≥ 15) stop. i = j = 4 → **return 4**.

- (A) returns 3 by stopping j at the 4 rather than at 15.
- (B) has the right array but returns i + 1 (Lomuto-style pivot index).
- (C) is not produced by any of the swaps above.
- (D) Correct: left part A[0..4] = {3, 10, 7, 4, 15} ≤ 15, right part ≥ 15.

**Trap:** expecting the pivot 15 to be at index j and the second 15 to be on the left — with Hoare, equal keys can end up on either side.''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

A = [15, 22, 7, 31, 15, 4, 18, 10, 26, 3]
p = A[0]; i, j = -1, 10
while True:
    j -= 1
    while A[j] > p: j -= 1
    i += 1
    while A[i] < p: i += 1
    if i < j: A[i], A[j] = A[j], A[i]
    else: break
assert A == [3, 10, 7, 4, 15, 31, 18, 22, 26, 15] and j == 4 and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Binary search — iterations per key',
            'text': '''The sorted array A[0..49] holds 50 distinct keys. The following search is run once for **each** of the 50 keys:

lo = 0, hi = 49; while lo ≤ hi: mid = ⌊(lo + hi)/2⌋; if A[mid] = x return; elif A[mid] < x: lo = mid + 1 else hi = mid − 1.

The number of keys for which the loop body executes exactly 6 times is ______.''',
            'answer': '19',
            'solution': '''The sequence of mids forms an implicit **decision tree** (a BST over the indices): the root is index 24, its children are the mids of [0..23] and [25..49], and so on. A key found at depth d (root depth 0) needs d + 1 iterations.

Count nodes level by level. A balanced split of n elements puts ⌊(n−1)/2⌋ on the left and ⌈(n−1)/2⌉ on the right:

- Level 0 (1 iteration): 1 node (index 24); subranges sizes 24 and 25
- Level 1 (2): 2 nodes; subranges 11, 12, 12, 12
- Level 2 (3): 4 nodes; subranges 5, 5, 5, 6, 5, 6, 5, 6
- Level 3 (4): 8 nodes; remaining 50 − 15 = 35 keys below
- Level 4 (5): 16 nodes
- Level 5 (6): the rest, 50 − (1 + 2 + 4 + 8 + 16) = **19** nodes

Since levels 0–4 are full (31 nodes) and the tree has height ⌊log₂ 50⌋ = 5, exactly 19 keys need 6 iterations. (The average successful search therefore costs (1·1 + 2·2 + 3·4 + 4·8 + 5·16 + 6·19)/50 = 243/50 = 4.86 iterations.)

**Trap:** answering 32 (a full last level) — the last level of a 50-node tree is only partly filled.''',
            'verify': '''
from collections import Counter
def iters(n, idx):
    lo, hi, c = 0, n - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2; c += 1
        if mid == idx: return c
        if mid < idx: lo = mid + 1
        else: hi = mid - 1
C = Counter(iters(50, i) for i in range(50))
assert C[6] == int(ANSWER) and sum(k * v for k, v in C.items()) == 243
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Tree reconstruction from traversals',
            'text': '''A binary tree with distinct labels has
pre-order: M D B A H F K L T W U
in-order: A B D F H K L M T U W
Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)''',
            'options': [
                'Its post-order is A B F L K H D U W T M',
                'Its height is 4',
                'It has exactly 4 leaves',
                'Exactly 3 nodes have exactly one child',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Pre-order gives the root first; its position in the in-order splits the remaining labels into left and right subtrees. Recurse.

- Root M. In-order left of M: A B D F H K L (7 nodes); right: T U W.
- Left subtree pre-order D B A H F K L → root D; in-order left {A, B}, right {F, H, K, L}.
- B with left child A. H with left child F and right child K; K has right child L.
- Right subtree pre-order T W U → root T; in-order T is first → no left child; right {U, W} with pre-order W U → W with left child U.

- (A) Post-order = A B | F L K H | D | U W T | M → **True.**
- (B) Longest path M → D → H → K → L has 4 edges → **True.**
- (C) Leaves: A, F, L, U → 4 → **True.**
- (D) One-child nodes: B (left only), K (right only), T (right only), W (left only) → **4**, not 3 → **False.**

**Check:** in a binary tree, leaves = (nodes with two children) + 1. Two-child nodes are M, D, H (3), so leaves = 4 ✓.

**Trap:** pre-order + post-order would *not* determine a tree with one-child nodes; pre-order + in-order always does.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        'M',
                        [
                            'D',
                            [
                                'B',
                                ['A'],
                                None,
                            ],
                            [
                                'H',
                                ['F'],
                                [
                                    'K',
                                    None,
                                    ['L'],
                                ],
                            ],
                        ],
                        [
                            'T',
                            None,
                            [
                                'W',
                                ['U'],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Reconstructed tree',
                },
            ],
            'verify': '''
def build(pre, ino):
    if not pre: return None
    r = pre[0]; k = ino.index(r)
    return [r, build(pre[1:k+1], ino[:k]), build(pre[k+1:], ino[k+1:])]
t = build(list('MDBAHFKLTWU'), list('ABDFHKLMTUW'))
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def nodes(t): return [] if t is None else [t] + nodes(t[1]) + nodes(t[2])
leaves = sum(1 for n in nodes(t) if n[1] is None and n[2] is None)
one = sum(1 for n in nodes(t) if (n[1] is None) != (n[2] is None))
vals = [''.join(post(t)) == 'ABFLKHDUWTM', h(t) == 4, leaves == 4, one == 3]
assert [L for L, v in zip('ABCD', vals) if v] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Insertion sort — comparisons',
            'text': 'Insertion sort (inner loop: `while j >= 0 and A[j] > key`) sorts `[5, 9, 2, 7, 3, 8, 1]` in ascending order. A *comparison* is one evaluation of `A[j] > key` (the test `j >= 0` is not counted, and when it is false `A[j] > key` is not evaluated). The total number of comparisons is ______.',
            'answer': '17',
            'solution': '''Every comparison that returns True causes a shift (removes one inversion). A comparison that returns False ends the insertion; that happens once per insertion **unless** the key travels all the way to index 0 (then the loop ends on `j >= 0`).

So comparisons = inversions + (insertions that stop early).

Insertions (i = 1..6):

- 9: compare with 5 → False. 1 comparison, 0 shifts.
- 2: shifts 9, 5 → reaches front. 2 comparisons.
- 7: shifts 9; compare with 5 → False. 2 comparisons.
- 3: shifts 9, 7, 5; compare with 2 → False. 4 comparisons.
- 8: shifts 9; compare with 7 → False. 2 comparisons.
- 1: shifts 9, 8, 7, 5, 3, 2 → reaches front. 6 comparisons.

Total = 1 + 2 + 2 + 4 + 2 + 6 = **17** (= 13 inversions + 4 early stops).

**Trap:** answering 13 (shifts only) or 21 (= n(n − 1)/2, the worst case).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each insertion',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6'],
                    'row_labels': ['start', 'i=1', 'i=2', 'i=3', 'i=4', 'i=5', 'i=6'],
                    'rows': [
                        [5, 9, 2, 7, 3, 8, 1],
                        [5, 9, 2, 7, 3, 8, 1],
                        [2, 5, 9, 7, 3, 8, 1],
                        [2, 5, 7, 9, 3, 8, 1],
                        [2, 3, 5, 7, 9, 8, 1],
                        [2, 3, 5, 7, 8, 9, 1],
                        [1, 2, 3, 5, 7, 8, 9],
                    ],
                },
            ],
            'verify': '''
a = [5, 9, 2, 7, 3, 8, 1]; c = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0:
        c += 1
        if a[j] > key: a[j+1] = a[j]; j -= 1
        else: break
    a[j+1] = key
assert c == int(ANSWER) and a == sorted(a)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': "Linked lists — Floyd's cycle detection",
            'text': "A singly linked list has nodes 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8, and node 8's `next` points back to node 4. Floyd's algorithm starts with `slow = fast = head` (node 1) and repeats `slow = slow.next; fast = fast.next.next` until `slow is fast`. Where do they first meet, and after how many iterations?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': [1, 2, 3, 4, 5, 6, 7, 8],
                    'edges': [
                        [1, 2],
                        [2, 3],
                        [3, 4],
                        [4, 5],
                        [5, 6],
                        [6, 7],
                        [7, 8],
                        [8, 4],
                    ],
                    'pos': {
                        1: [0, 1],
                        2: [1, 1],
                        3: [2, 1],
                        4: [3, 1],
                        5: [4, 2],
                        6: [5, 1],
                        7: [4.5, 0],
                        8: [3.5, 0],
                    },
                },
            ],
            'options': [
                'At node 6 after 5 iterations',
                'At node 4 after 4 iterations',
                'At node 8 after 5 iterations',
                'At node 5 after 6 iterations',
            ],
            'answer': 'A',
            'solution': '''Tail length μ = 3 (nodes 1, 2, 3 precede the cycle), cycle length λ = 5 (4 → 5 → 6 → 7 → 8 → 4).

Positions after each iteration:

- 1: slow 2, fast 3
- 2: slow 3, fast 5
- 3: slow 4, fast 7
- 4: slow 5, fast 4 (7 → 8 → 4)
- 5: slow 6, fast 6 (4 → 5 → 6) → **meet at node 6**

Check with theory: when slow enters the cycle (after μ = 3 steps, at node 4) fast is 3 steps ahead along the cycle (at node 7). The gap closes by 1 per iteration, so they meet after (λ − 3) mod λ = 2 more iterations: total 5, at 2 steps past node 4 = node 6.

- (B) Node 4 is the cycle entry, found only in phase 2 (reset one pointer to head and move both by 1: from 1 and from 6 they meet at 4 after 3 steps = μ).
- (C), (D) result from mis-stepping fast around 8 → 4.

**Trap:** assuming the meeting point is the start of the cycle.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

nxt = {i: i + 1 for i in range(1, 8)}; nxt[8] = 4
s = f = 1; k = 0
while True:
    s = nxt[s]; f = nxt[nxt[f]]; k += 1
    if s == f: break
a, b = 1, s; mu = 0
while a != b: a, b = nxt[a], nxt[b]; mu += 1
assert (s, k) == (6, 5) and (a, mu) == (4, 3) and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Solving recurrences',
            'text': 'Which of the following recurrences (with T(1) = 1) are solved correctly?',
            'options': [
                'T(n) = 2T(n/2) + n log n  ⇒  T(n) = Θ(n log² n)',
                'T(n) = T(n − 1) + n  ⇒  T(n) = Θ(n²)',
                'T(n) = 4T(n/2) + n²  ⇒  T(n) = Θ(n²)',
                'T(n) = 3T(n/2) + n  ⇒  T(n) = Θ(n^{log₂ 3})',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''- (A) **Correct.** Recursion tree: level i has 2^{i} nodes each costing (n/2^{i})·log(n/2^{i}), level total n(log n − i). Summing i = 0..log n gives n·Θ(log² n). (The basic Master theorem does not apply since n log n is not polynomially larger than n; the extended case 2 gives Θ(n log^{k+1} n) with k = 1.)
- (B) **Correct.** T(n) = 1 + 2 + … + n = n(n + 1)/2 = Θ(n²).
- (C) **Incorrect.** a = 4, b = 2 → n^{log₂ 4} = n², which matches f(n) = n² (case 2) → Θ(n² log n), not Θ(n²).
- (D) **Correct.** n^{log₂ 3} ≈ n^{1.585} dominates f(n) = n polynomially (case 1) → Θ(n^{log₂ 3}).

**Trap:** in case 2 the answer always picks up an extra log factor; equating it with f(n) is the most common error.''',
            'verify': '''
import math
from functools import lru_cache
@lru_cache(None)
def TA(n): return 1 if n == 1 else 2*TA(n//2) + n*math.log2(n)
@lru_cache(None)
def TC(n): return 1 if n == 1 else 4*TC(n//2) + n*n
@lru_cache(None)
def TD(n): return 1 if n == 1 else 3*TD(n//2) + n
def TB(n): return n*(n+1)//2
r = lambda T, g, k: T(2**k) / g(2**k)
ra = [r(TA, lambda n: n*math.log2(n)**2, k) for k in (20, 30)]
rd = [r(TD, lambda n: n**math.log2(3), k) for k in (20, 30)]
rc = [r(TC, lambda n: n*n, k) for k in (10, 20, 30)]
assert abs(ra[0] - ra[1]) < 0.05 and abs(rd[0] - rd[1]) < 0.01
assert rc[0] < rc[1] < rc[2] and rc[2] > 25          # grows like log n: not Θ(n²)
assert sorted(ANSWER) == ['A', 'B', 'D']
''',
        },
    ],
}
