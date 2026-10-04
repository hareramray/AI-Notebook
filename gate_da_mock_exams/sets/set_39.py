# Set 39 — Full-Syllabus Mock — Paper 9
SET = {
    'number': 39,
    'title': 'Full-Syllabus Mock — Paper 9',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — closures and late binding',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''fs = [lambda x: x * i for i in range(1, 4)]
gs = [lambda x, i=i: x * i for i in range(1, 4)]
print([f(10) for f in fs], [g(10) for g in gs])''',
            'options': [
                '`[10, 20, 30] [10, 20, 30]`',
                '`[30, 30, 30] [30, 30, 30]`',
                '`[10, 20, 30] [30, 30, 30]`',
                '`[30, 30, 30] [10, 20, 30]`',
            ],
            'answer': 'D',
            'solution': '''A lambda's body looks up free variables **when it is called**, not when it is created (late binding). A default argument, by contrast, is evaluated **once, at definition time**.

- In `fs`, all three lambdas refer to the same variable `i` of the comprehension's scope. When they are finally called, the loop has finished and i = 3, so each returns 10 × 3 = 30 → `[30, 30, 30]`.
- In `gs`, `i=i` copies the *current* value of i into each lambda's own default parameter (1, 2, 3) → `[10, 20, 30]`.

Output `[30, 30, 30] [10, 20, 30]` → option (D).

- (A) assumes the closures captured values.
- (B) assumes the default-argument trick does not help.
- (C) swaps the two behaviours.

**Trap:** the comprehension has its own scope in Python 3, but that changes nothing — the closures share that scope's single `i`. `functools.partial` is another way to freeze values.''',
            'verify': "ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[30, 30, 30] [10, 20, 30]' and ANSWER == 'C'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — infix to postfix conversion',
            'text': '''The infix expression

a − b * ( c + d ^ e ^ ( f − g ) ) / h

is converted to postfix with the standard operator-stack algorithm. Precedence: `^` (highest, **right**-associative) > `*`, `/` > `+`, `−` (left-associative). Opening parentheses are pushed on the stack and popped (not output) at the matching ‘)’. The maximum number of symbols (operators and ‘(’) on the stack at any instant is ______.''',
            'answer': '8',
            'solution': '''Rule: on an operator, pop while the top has higher precedence, or equal precedence and the incoming operator is left-associative; then push. ‘(’ is always pushed; ‘)’ pops down to the matching ‘(’.

- a → out; `−` → [−]; b → out.
- `*` (higher than −) → [− *]; `(` → [− * (]; c → out.
- `+` (top is ‘(’) → [− * ( +]; d → out.
- `^` → [− * ( + ^]; e → out.
- `^` (equal, but right-associative → no pop) → [− * ( + ^ ^] (6).
- `(` → 7 symbols; f → out; `−` (top ‘(’) → [− * ( + ^ ^ ( −] → **8**.
- g → out; `)` pops − and the ‘(’ → 6; `)` pops ^ ^ + and ‘(’ → [− *].
- `/` pops * (equal, left-assoc) → [− /]; h → out; end pops / −.

Postfix: a b c d e f g − ^ ^ + * h / −. Maximum stack size = **8**.

**Trap:** treating `^` as left-associative pops the first `^` before pushing the second, giving a maximum of 7 (and a wrong postfix: … d e ^ f g − ^ …).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['−', '*', '(', '+', '^', '^', '(', '−'],
                    'label': 'operator stack at its peak',
                    'caption': 'Stack contents just after pushing the inner −',
                },
            ],
            'verify': '''
prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
st, out, mx = [], [], 0
for t in "a - b * ( c + d ^ e ^ ( f - g ) ) / h".split():
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
assert ' '.join(out) == 'a b c d e f g - ^ ^ + * h / -' and mx == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — deque rotations',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from collections import deque
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
d.appendleft(d.pop())
d.extend([6, 7])
d.rotate(-3)
print(list(d))''',
            'options': [
                '`[3, 4, 5, 1, 2, 6, 7]`',
                '`[2, 6, 7, 3, 4, 5, 1]`',
                '`[1, 2, 6, 7, 3, 4, 5]`',
                '`[5, 1, 6, 7, 2, 3, 4]`',
            ],
            'answer': 'C',
            'solution': '''`rotate(n)` with n > 0 moves the last n elements to the front (rotate **right**); n < 0 rotates left. `pop()` removes from the right end, `appendleft` adds at the left.

- Start: [1, 2, 3, 4, 5].
- `rotate(2)` → [4, 5, 1, 2, 3].
- `appendleft(pop())`: pop 3 from the right and put it in front → [3, 4, 5, 1, 2] (this is just one more right rotation).
- `extend([6, 7])` → [3, 4, 5, 1, 2, 6, 7].
- `rotate(-3)`: move the first three to the back → [1, 2, 6, 7, 3, 4, 5].

Output → option (C).

- (A) omits the final rotation.
- (B) rotates right by 3 at the end instead of left.
- (D) treats `rotate(2)` as a left rotation.

**Tip:** each deque operation used here is O(1) except `rotate(k)`, which is O(k) — far better than slicing a list, which is O(n).''',
            'verify': "ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[1, 2, 6, 7, 3, 4, 5]' and ANSWER == 'D'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': "Linked lists — Floyd's cycle detection",
            'text': "A singly linked list has nodes 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 and node 8's `next` points back to node 4 (see figure). Floyd's algorithm starts `slow` and `fast` at node 1; in each iteration `slow` advances one node and `fast` advances two nodes, and then the two pointers are compared. The number of iterations performed until they first point to the same node is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['1', '2', '3', '4', '5', '6', '7', '8'],
                    'edges': [
                        ['1', '2'],
                        ['2', '3'],
                        ['3', '4'],
                        ['4', '5'],
                        ['5', '6'],
                        ['6', '7'],
                        ['7', '8'],
                        ['8', '4'],
                    ],
                    'pos': {
                        '1': [0, 1],
                        '2': [1.3, 1],
                        '3': [2.6, 1],
                        '4': [3.9, 1],
                        '5': [5, 2],
                        '6': [6.5, 2],
                        '7': [7.2, 0.6],
                        '8': [5.6, 0],
                    },
                },
            ],
            'answer': '5',
            'solution': '''The list has a tail of μ = 3 nodes (1, 2, 3) and a cycle of length λ = 5 (4 → 5 → 6 → 7 → 8). After t iterations slow has made t moves and fast 2t moves; once both are in the cycle they coincide when the difference t is a multiple of λ. So the first meeting is at the smallest t ≥ μ with t ≡ 0 (mod λ), i.e. t = 5.

Trace (slow / fast):

- t = 0: 1 / 1 (start, not counted)
- t = 1: 2 / 3
- t = 2: 3 / 5
- t = 3: 4 / 7
- t = 4: 5 / 4 (fast went 7 → 8 → 4)
- t = 5: 6 / 6 → **meet** after 5 iterations at node 6.

Floyd then finds the cycle start by moving one pointer back to the head and advancing both one step at a time: they meet after μ = 3 more steps at node 4.

**Trap:** counting the initial equality at node 1 (both start there) as a meeting — the comparison happens only after moving.''',
            'verify': '''
nxt = {i: i + 1 for i in range(1, 8)}; nxt[8] = 4
s = f = 1; t = 0
while True:
    s = nxt[s]; f = nxt[nxt[f]]; t += 1
    if s == f: break
p, q, mu = 1, s, 0
while p != q: p = nxt[p]; q = nxt[q]; mu += 1
assert t == int(ANSWER) and s == 6 and (p, mu) == (4, 3)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'BST — valid search sequences',
            'text': 'A binary search tree contains integer keys including 55. A search for 55 compares it with the keys of the nodes on the search path, in order. Which of the following could be such a sequence of examined keys?',
            'options': [
                '79, 14, 72, 56, 16, 53, 55',
                '10, 75, 64, 43, 60, 57, 55',
                '90, 12, 68, 34, 62, 45, 55',
                '9, 85, 47, 68, 43, 57, 55',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Maintain the open interval (low, high) the target must lie in: going right after key x sets low = x, going left sets high = x. Every later key on the path must lie inside the current interval.

- (A) 79 → (−∞, 79); 14 → (14, 79); 72 → (14, 72); 56 → left (14, 56); 16 → (16, 56); 53 → (53, 56); 55 ✓. **Valid.**
- (B) 10 → right (10, ∞); 75 → left (10, 75); 64 → left (10, 64); 43 → right (43, 64); 60 → left (43, 60); 57 → left (43, 57); 55 ✓. **Valid.**
- (C) 90 → left (−∞, 90); 12 → right (12, 90); 68 → left (12, 68); 34 → right (34, 68); 62 → left (34, 62); 45 → right (45, 62); 55 ✓. **Valid.**
- (D) 9 → (9, ∞); 85 → (9, 85); 47 → (47, 85); 68 → (47, 68); next key 43 is **outside** (47, 68) — after going right at 47, no key below 47 can appear. **Invalid.**

Answer: (B), (C), (A).

**Trap:** checking only the direction at each step (55 vs current key) without tracking the interval inherited from all ancestors.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def valid(seq, x=55):
    lo, hi = float('-inf'), float('inf')
    for k in seq[:-1]:
        if not lo < k < hi: return False
        if x > k: lo = k
        else: hi = k
    return seq[-1] == x and lo < x < hi
opts = {'A': [10, 75, 64, 43, 60, 57, 55], 'B': [90, 12, 68, 34, 62, 45, 55],
        'C': [9, 85, 47, 68, 43, 57, 55], 'D': [79, 14, 72, 56, 16, 53, 55]}
assert sorted(k for k in opts if valid(opts[k])) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Heaps — successive insertion vs build-heap',
            'text': 'The keys 15, 22, 9, 31, 40, 12, 27 are inserted **one at a time** (in this order) into an initially empty binary **max**-heap stored in an array (each insertion appends the key and sifts it up). Which of the following statements is/are TRUE?',
            'options': [
                'In the final heap, the key 9 is a leaf',
                'The final array is [40, 31, 27, 15, 22, 9, 12]',
                'A total of 7 swaps are performed',
                'Running bottom-up build-heap on the array [15, 22, 9, 31, 40, 12, 27] produces the same final array',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Insertion = append at the end, then swap with the parent while larger.

- 15 → [15].
- 22 → swap with 15 → [22, 15] (1 swap).
- 9 → [22, 15, 9].
- 31 → idx 3, swap with 15, then with 22 → [31, 22, 9, 15] (2 swaps, total 3).
- 40 → idx 4, swap with 22, then with 31 → [40, 31, 9, 15, 22] (2, total 5).
- 12 → idx 5, swap with 9 → [40, 31, 12, 15, 22, 9] (1, total 6).
- 27 → idx 6, swap with 12 → [40, 31, 27, 15, 22, 9, 12] (1, total **7**).
- (A) **True.** 9 is at index 5 ≥ ⌊7/2⌋ = 3, so it is a leaf.
- (B) **True.**  (C) **True.**
- (D) **False.** Build-heap sifts down from index 2: 9 vs children 12, 27 → swap with 27; index 1: 22 vs 31, 40 → swap with 40; index 0: 15 vs 40, 27 → 40, then 15 vs 31, 22 → 31. Result [40, 31, 27, 15, 22, 12, 9] — 12 and 9 are in the opposite places.

**Tip:** the two construction methods give valid but generally different heaps; build-heap is O(n) while n insertions are O(n log n) in the worst case.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [40, 31, 27, 15, 22, 9, 12],
                    'caption': 'Heap after the seven insertions',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

h = []; sw = 0
for k in [15, 22, 9, 31, 40, 12, 27]:
    h.append(k); i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] < h[i]:
        p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p; sw += 1
b = [15, 22, 9, 31, 40, 12, 27]
for s in range(len(b) // 2 - 1, -1, -1):
    i = s
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < 7 and b[l] > b[m]: m = l
        if r < 7 and b[r] > b[m]: m = r
        if m == i: break
        b[i], b[m] = b[m], b[i]; i = m
res = {'A': h == [40, 31, 27, 15, 22, 9, 12], 'B': sw == 7, 'C': b == h, 'D': h.index(9) >= 3}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — quadratic probing failure',
            'text': 'A hash table has 10 slots (0–9). Key k is inserted using quadratic probing: the i-th probe (i = 0, 1, 2, …) examines slot (k mod 10 + i²) mod 10. The keys 13, 23, 33, 43, 53, 63, 73 are inserted in this order into an empty table. What happens when 73 is inserted?',
            'options': [
                '73 is stored in slot 0',
                '73 is stored in slot 5',
                '73 is stored in slot 1',
                '73 cannot be inserted, although 4 slots are empty',
            ],
            'answer': 'D',
            'solution': '''All keys have home slot 3. The offsets i² mod 10 for i = 0, 1, 2, … are 0, 1, 4, 9, 6, 5, 6, 9, 4, 1, 0, … — only **six** distinct values {0, 1, 4, 5, 6, 9}. So a key with home 3 can only ever probe slots 3, 4, 7, 2, 9, 8 (= 3 + offset mod 10).

- 13 → 3; 23 → 3+1 = 4; 33 → 3+4 = 7; 43 → 3+9 = 12 → 2; 53 → 3+16 = 19 → 9; 63 → 3+25 = 28 → 8.
- 73: probes 3, 4, 7, 2, 9, 8, 8, 9, 2, 7, 3, … — all six reachable slots are full, and the sequence repeats forever. Slots 0, 1, 5, 6 are empty but **unreachable**.

Hence the insertion fails although the table is only 60 % full → option (D).

Options (A), (B), (C) name empty slots that the probe sequence for home slot 3 never visits.

**Tip:** quadratic probing is guaranteed to find an empty slot only under conditions such as m prime and load factor ≤ 1/2 (then the first ⌈m/2⌉ probes are distinct).''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        2: 43,
                        3: 13,
                        4: 23,
                        7: 33,
                        8: 63,
                        9: 53,
                    },
                    'caption': 'Table before inserting 73 (slots 0, 1, 5, 6 unreachable)',
                },
            ],
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

T = [None] * 10
placed = {}
for k in [13, 23, 33, 43, 53, 63, 73]:
    for i in range(100):
        s = (k % 10 + i * i) % 10
        if T[s] is None: T[s] = k; placed[k] = s; break
assert 73 not in placed and T.count(None) == 4 and ANSWER == 'C'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Linear search — expected comparisons',
            'text': 'An unsorted array holds n = 9 distinct keys. A key x is searched by linear search from index 0. With probability 2/3 the key is present, and if present it is equally likely to be at each of the 9 positions; with probability 1/3 it is absent. The expected number of key comparisons (rounded off to two decimal places) is ______.',
            'answer': ['6.32', '6.34'],
            'solution': '''Use the law of total expectation over the two cases.

- **Present** (probability 2/3): if x is at position i (1-based), linear search makes i comparisons. Averaging over i = 1 … 9: (1 + 2 + … + 9)/9 = 45/9 = 5 = (n + 1)/2.
- **Absent** (probability 1/3): all n = 9 elements are compared → 9.

E = (2/3)(5) + (1/3)(9) = 10/3 + 3 = 19/3 ≈ **6.33**.

General formula: E = p(n + 1)/2 + (1 − p)n. For p = 1 this is (n + 1)/2, for p = 0 it is n.

**Trap:** averaging 5 and 9 with equal weights (7) — the probabilities are 2/3 and 1/3, not 1/2 each. Another slip is using n/2 = 4.5 instead of (n + 1)/2 for the successful case.''',
            'verify': '''
from fractions import Fraction as F
E = F(2, 3) * F(sum(range(1, 10)), 9) + F(1, 3) * 9
assert E == F(19, 3) and float(ANSWER[0]) <= float(E) <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Insertion sort — intermediate state',
            'text': 'Insertion sort (increasing order) is applied to [31, 12, 47, 5, 26, 18]. One *pass* inserts the next element A[i] (i = 1, 2, …) into the sorted prefix A[0..i−1]. The array after **three** passes is',
            'options': [
                '[5, 12, 31, 47, 26, 18]',
                '[12, 31, 47, 5, 26, 18]',
                '[5, 12, 26, 31, 47, 18]',
                '[5, 12, 18, 31, 26, 47]',
            ],
            'answer': 'A',
            'solution': '''Insertion sort keeps A[0..i] sorted after pass i; the suffix is untouched.

- Pass 1 (i = 1, insert 12): 31 shifts right → [12, 31, 47, 5, 26, 18].
- Pass 2 (i = 2, insert 47): already larger than 31 → no shift.
- Pass 3 (i = 3, insert 5): 47, 31, 12 shift right → [5, 12, 31, 47, 26, 18].

Answer (A).

- (B) is the state after only two passes.
- (C) is after four passes (26 inserted).
- (D) is **selection** sort after three passes (minimums 5, 12, 18 swapped into place) — selection sort fixes final positions, insertion sort only orders the prefix.

Shifts so far: 1 + 0 + 3 = 4 = the number of inversions among the first four elements.

**Tip:** after k passes, insertion sort's prefix holds the *first* k + 1 input elements in sorted order, whereas selection sort's prefix holds the k *smallest* elements overall.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

a = [31, 12, 47, 5, 26, 18]
for i in range(1, 4):
    x = a[i]; j = i - 1
    while j >= 0 and a[j] > x: a[j + 1] = a[j]; j -= 1
    a[j + 1] = x
b = [31, 12, 47, 5, 26, 18]
for i in range(3):
    m = min(range(i, 6), key=lambda k: b[k]); b[i], b[m] = b[m], b[i]
opts = {'A': [12, 31, 47, 5, 26, 18], 'B': [5, 12, 31, 47, 26, 18],
        'C': [5, 12, 26, 31, 47, 18], 'D': [5, 12, 18, 31, 26, 47]}
assert [k for k in opts if opts[k] == a] == [ANSWER] and opts['D'] == b
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph theory — degrees and handshaking',
            'text': 'A simple undirected graph G has exactly 12 edges. Three of its vertices have degree 4 and every other vertex has degree 3. Which of the following statements is/are TRUE?',
            'options': [
                'G must be connected',
                'The complement of G has exactly 9 edges',
                'G has exactly 7 vertices',
                'G has exactly 3 vertices of odd degree',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''Handshaking lemma: the sum of degrees equals 2|E|.

- (A) **True.** In a simple graph a vertex of degree ≥ 3 needs at least 3 neighbours in its component, so every component has ≥ 4 vertices. Two components would need ≥ 8 vertices, but G has only 7 — so G is connected.
- (B) **True.** K₇ has C(7, 2) = 21 edges, so the complement has 21 − 12 = 9 edges.
- (C) **True.** 3·4 + 3(n − 3) = 24 → 3n + 3 = 24 → n = 7.
- (D) **False.** The degree-3 vertices are the odd ones: 7 − 3 = **4** of them (the number of odd-degree vertices is always even).

Answer: (C), (B), (A).

**Trap:** assuming (A) needs a specific drawing. The counting argument (minimum component size δ + 1) settles it for every such graph; the verifier also checks all 19 355 labelled graphs with this degree sequence.''',
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import itertools
pairs = list(itertools.combinations(range(7), 2))
total = conn = 0
for es in itertools.combinations(range(21), 12):
    deg = [0] * 7
    for e in es:
        u, v = pairs[e]; deg[u] += 1; deg[v] += 1
    if sorted(deg) != [3, 3, 3, 3, 4, 4, 4]: continue
    total += 1
    adj = {i: [] for i in range(7)}
    for e in es:
        u, v = pairs[e]; adj[u].append(v); adj[v].append(u)
    seen = {0}; st = [0]
    while st:
        for v in adj[st.pop()]:
            if v not in seen: seen.add(v); st.append(v)
    conn += len(seen) == 7
assert total == conn > 0 and sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — generators with try/finally',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def gen():
    try:
        for i in range(3):
            yield i
    finally:
        print("F", end=" ")

g = gen()
print(next(g), end=" ")
print(sum(g), end=" ")
print(list(g))''',
            'options': ['`0 F 3 []`', '`0 3 F []`', '`0 3 [] F`', '`0 F 3 [0, 1, 2]`'],
            'answer': 'A',
            'solution': '''A generator runs its body lazily, pausing at each `yield`. The `finally` block runs when the body actually finishes — here, when the loop ends after the last value is consumed.

- `next(g)` runs up to the first `yield` → 0. Printed: `0 `.
- `sum(g)` must evaluate completely **before** the outer `print` can print its result. It pulls 1 and 2; asking for the next value resumes the body, the loop ends, the `finally` block prints `F ` and then StopIteration ends the sum. Only now is 1 + 2 = 3 printed. Output so far: `0 F 3 `.
- `list(g)` on an exhausted generator → `[]`.

Full output: `0 F 3 []` → option (A).

- (B) assumes `finally` runs after the value 3 is printed — but arguments are evaluated before `print` executes.
- (C) delays `finally` until the program ends (it would only do that if the generator were never exhausted and was garbage-collected late).
- (D) assumes the generator restarts.

**Trap:** side effects inside generators happen at *consumption* time, interleaved with the consumer's own output.''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '0 F 3 []' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Counting BSTs by height',
            'text': 'Consider all binary search trees whose keys are exactly 1, 2, 3, 4, 5, 6 (there are 132 of them). The height of a tree is the number of **edges** on its longest root-to-leaf path. The number of these BSTs that have height exactly 4 is ______.',
            'answer': '56',
            'solution': '''Let N(n, h) = number of BSTs on n keys with height **at most** h (N(0, h) = 1 for the empty tree, N(n, −1) = 0 for n ≥ 1). Choosing root r leaves r − 1 keys on the left and n − r on the right, each of height ≤ h − 1:

N(n, h) = ∑ over r = 1 … n of N(r − 1, h − 1) · N(n − r, h − 1).

Then (height exactly 4) = N(6, 4) − N(6, 3).

- N(6, 4): left/right sizes (0,5), (1,4), (2,3), (3,2), (4,1), (5,0) with h ≤ 3: 26 + 14 + 10 + 10 + 14 + 26 = **100**.
- N(6, 3): same splits with h ≤ 2: 6 + 6 + 10 + 10 + 6 + 6 = **44**.

Answer = 100 − 44 = **56**.

Cross-check: the 132 trees split by height as 4 (height 2) + 40 (height 3) + 56 (height 4) + 32 (height 5). Height 5 means a path (‘zig-zag chain’): each of the 5 non-root levels chooses left or right → 2⁵ = 32, and 132 − 32 − 44 = 56. ✓

**Trap:** using the node-count definition of height, which shifts every value by one and would make ‘height 4’ mean edges = 3 (40 trees).''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'N(n, h) = BSTs on n keys with height ≤ h',
                    'row_labels': ['n=1', 'n=2', 'n=3', 'n=4', 'n=5', 'n=6'],
                    'col_labels': ['h=0', 'h=1', 'h=2', 'h=3', 'h=4', 'h=5'],
                    'rows': [
                        [1, 1, 1, 1, 1, 1],
                        [0, 2, 2, 2, 2, 2],
                        [0, 1, 5, 5, 5, 5],
                        [0, 0, 6, 14, 14, 14],
                        [0, 0, 6, 26, 42, 42],
                        [0, 0, 4, 44, 100, 132],
                    ],
                    'highlight': [
                        [5, 3],
                        [5, 4],
                    ],
                },
            ],
            'verify': '''
def trees(lo, hi):
    if lo > hi: return [None]
    out = []
    for r in range(lo, hi + 1):
        for L in trees(lo, r - 1):
            for R in trees(r + 1, hi): out.append((r, L, R))
    return out
def ht(t): return -1 if t is None else 1 + max(ht(t[1]), ht(t[2]))
T = trees(1, 6)
assert len(T) == 132 and sum(1 for t in T if ht(t) == 4) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quicksort and merge sort — exact comparison counts',
            'text': 'Quicksort uses Lomuto partition with the **last** element as pivot (each partition of a sub-array of length m makes m − 1 comparisons). Merge sort is top-down and stops a merge as soon as one run is exhausted. Which of the following statements is/are TRUE for n = 16 distinct keys?',
            'options': [
                'Quicksort on the decreasing array [16, 15, …, 1] makes exactly 120 comparisons',
                'Merge sort on the increasing array [1, 2, …, 16] makes exactly 32 comparisons',
                'Quicksort makes fewer comparisons on the increasing array [1, 2, …, 16] than on the decreasing array',
                'Merge sort on the decreasing array [16, 15, …, 1] makes exactly 32 comparisons',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''- (A) **True.** Decreasing input: pivot 1 is the minimum → partition gives sizes 0 and 15; the 15 remaining keys [15, …, 2, 16] — after the swaps the right part has pivot 16 (max) → sizes 14 and 0, and so on. Every partition is maximally unbalanced, so the total is 15 + 14 + … + 1 = 16·15/2 = **120**.
- (B) **True.** On sorted input, every merge of two runs of length k compares the k elements of the left run with the first element of the right run and then stops: k comparisons. Each level costs n/2 = 8, and there are log₂16 = 4 levels → **32** = (n/2) log₂ n — the best case.
- (C) **False.** With the last element as pivot, sorted input makes the pivot the maximum every time → also 120 comparisons, the same as (A).
- (D) **True.** On reversed input every right run is entirely smaller, so the right run is exhausted after k comparisons: again 8 per level → **32**.

Answer: (A), (B), (D).

**Insight:** merge sort's comparison count varies only between (n/2)log₂ n = 32 and n log₂ n − n + 1 = 49 for n = 16, whereas quicksort's count can climb all the way to n(n − 1)/2 = 120.''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def qs(a):
    c = [0]
    def part(lo, hi):
        p = a[hi]; i = lo - 1
        for j in range(lo, hi):
            c[0] += 1
            if a[j] <= p: i += 1; a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]; return i + 1
    def rec(lo, hi):
        if lo < hi:
            p = part(lo, hi); rec(lo, p - 1); rec(p + 1, hi)
    rec(0, len(a) - 1); return c[0]
def ms(a):
    if len(a) <= 1: return a, 0
    m = len(a) // 2; L, c1 = ms(a[:m]); R, c2 = ms(a[m:]); i = j = c = 0; o = []
    while i < len(L) and j < len(R):
        c += 1
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:], c + c1 + c2
inc, dec = list(range(1, 17)), list(range(16, 0, -1))
res = {'A': qs(dec[:]) == 120, 'B': ms(inc)[1] == 32, 'C': ms(dec)[1] == 32,
       'D': qs(inc[:]) < qs(dec[:])}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'DFS — timestamps and edge classification',
            'text': 'Depth-first search is run on the directed graph below starting at **A**; adjacency lists are scanned in **alphabetical order**, and a global clock starting at 1 is incremented at every discovery and every finish (d(A) = 1). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'D'],
                        ['C', 'F'],
                        ['D', 'A'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'D'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1],
                        'E': [4.5, 2],
                        'F': [4.5, 0],
                    },
                },
            ],
            'options': [
                'The vertices of the graph can be topologically sorted',
                'B→E is a cross edge',
                'd(C) = 10 and f(C) = 11',
                'Exactly two edges are back edges',
            ],
            'answer': ['C', 'D'],
            'solution': '''Classification for an edge u→v met while scanning u: v undiscovered → **tree**; v discovered but unfinished (on the recursion stack) → **back**; v finished with d(u) < d(v) → **forward**; v finished with d(u) > d(v) → **cross**.

Trace:

- A d=1 → B d=2 → (B's list: D, E) D d=3.
- D: A is on the stack → D→A **back**; E undiscovered → E d=4.
- E → F d=5. F: D is on the stack → F→D **back**. F finishes f=6; E f=7; D f=8.
- Back at B: E is finished and d(B)=2 < d(E)=4 → B→E **forward**. B f=9.
- Back at A: C d=10. C→D: D finished, d(C)=10 > 3 → **cross**; C→F → **cross**. C f=11; A f=12.

Tree edges: A→B, B→D, D→E, E→F, A→C.

- (A) **False** — a back edge means a directed cycle (A→B→D→A), so no topological order.
- (B) **False** — B→E is a forward edge (E is a descendant of B reached via D).
- (C) **True** — d(C) = 10, f(C) = 11.
- (D) **True** — D→A and F→D.

**Trap:** calling B→E a tree edge because it is drawn directly; with alphabetical order D is explored first and reaches E before B gets to scan E.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Discovery / finish times',
                    'row_labels': ['d', 'f'],
                    'col_labels': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'rows': [
                        [1, 2, 10, 3, 4, 5],
                        [12, 9, 11, 8, 7, 6],
                    ],
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

G = {'A': ['B','C'], 'B': ['D','E'], 'C': ['D','F'], 'D': ['A','E'], 'E': ['F'], 'F': ['D']}
t = [0]; d = {}; f = {}; cls = {}
def dfs(u):
    t[0] += 1; d[u] = t[0]
    for v in sorted(G[u]):
        if v not in d: cls[(u, v)] = 'tree'; dfs(v)
        elif v not in f: cls[(u, v)] = 'back'
        elif d[u] < d[v]: cls[(u, v)] = 'forward'
        else: cls[(u, v)] = 'cross'
    t[0] += 1; f[u] = t[0]
dfs('A')
res = {'A': list(cls.values()).count('back') == 2, 'B': cls[('B','E')] == 'cross',
       'C': (d['C'], f['C']) == (10, 11), 'D': 'back' not in cls.values()}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Dijkstra — extraction order',
            'text': "Dijkstra's algorithm is run from **A** on the undirected weighted graph below. When two vertices have equal tentative distance, the alphabetically smaller is extracted first. In which order are the vertices extracted from the priority queue?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B', 4],
                        ['A', 'C', 1],
                        ['C', 'B', 2],
                        ['C', 'D', 7],
                        ['B', 'D', 3],
                        ['B', 'E', 6],
                        ['D', 'E', 1],
                        ['D', 'F', 5],
                        ['E', 'G', 4],
                        ['F', 'G', 2],
                        ['C', 'F', 12],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [1.5, 0],
                        'D': [3, 1],
                        'E': [4.5, 2],
                        'F': [4.5, 0],
                        'G': [6, 1],
                    },
                },
            ],
            'options': [
                'A, B, C, D, E, F, G',
                'A, C, B, D, E, F, G',
                'A, C, B, D, E, G, F',
                'A, C, B, E, D, F, G',
            ],
            'answer': 'B',
            'solution': '''Dijkstra extracts vertices in non-decreasing order of their final distances (ties by the stated rule).

- A (0): B = 4, C = 1.
- C (1): B = min(4, 1+2) = 3; D = 1+7 = 8; F = 1+12 = 13.
- B (3): D = min(8, 3+3) = 6; E = 3+6 = 9.
- D (6): E = min(9, 6+1) = 7; F = min(13, 6+5) = 11.
- E (7): G = 7+4 = 11.
- Now F = 11 and G = 11 tie → F first (alphabetical); F: G = min(11, 11+2) stays 11.
- G (11).

Order **A, C, B, D, E, F, G** → option (B). Final distances: A0 C1 B3 D6 E7 F11 G11.

- (A) extracts B before C — B's initial label 4 is not its final distance 3, and C (1) is smaller anyway.
- (C) breaks the F/G tie the wrong way.
- (D) extracts E (tentative 9 at that time) before D (6).

**Trap:** the direct edges A–B and C–F are both ‘shortcuts’ that lose to detours; never fix a label before its vertex is extracted.''',
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

E = [("A","B",4),("A","C",1),("C","B",2),("C","D",7),("B","D",3),("B","E",6),("D","E",1),
     ("D","F",5),("E","G",4),("F","G",2),("C","F",12)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
INF = float('inf'); d = {v: INF for v in G}; d['A'] = 0; order = []
while len(order) < len(G):
    u = min((v for v in G if v not in order), key=lambda v: (d[v], v)); order.append(u)
    for v, w in G[u]:
        if v not in order and d[u] + w < d[v]: d[v] = d[u] + w
opts = {'A': "ABCDEFG", 'B': "ACBDEGF", 'C': "ACBDEFG", 'D': "ACBEDFG"}
assert [k for k in opts if opts[k] == "".join(order)] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — expected number of empty slots',
            'text': 'Ten keys are inserted into a hash table with 10 slots using separate chaining. Assume simple uniform hashing: each key independently hashes to each slot with probability 1/10. The expected number of slots that remain **empty** (rounded off to two decimal places) is ______.',
            'answer': ['3.48', '3.50'],
            'solution': '''Use **linearity of expectation** with indicator variables. Let Xⱼ = 1 if slot j is empty.

- A particular key misses slot j with probability 1 − 1/10 = 0.9.
- All 10 keys miss slot j (independently) with probability 0.9¹⁰.
- E[Xⱼ] = 0.9¹⁰ ≈ 0.348678.

E[# empty slots] = ∑ⱼ E[Xⱼ] = 10 × 0.9¹⁰ ≈ 10 × 0.348678 = **3.49**.

So even with load factor α = 1, about 35 % of the slots are empty and the 10 keys crowd into ≈ 6.5 slots — collisions are unavoidable (for large m the fraction tends to e^{−α} ≈ 0.368).

Related quantities: expected number of colliding pairs = C(10, 2)/10 = 4.5; expected chain length seen by an unsuccessful search = α = 1.

**Trap:** assuming that 10 keys in 10 slots ‘fill’ the table (0 empty), or computing (1 − 1/10)·10 = 9 by forgetting that all ten keys must miss the slot.''',
            'verify': '''
import itertools, random
exact = 10 * 0.9 ** 10
assert float(ANSWER[0]) <= exact <= float(ANSWER[1])
random.seed(7)
trials = 20000
sim = sum(10 - len({random.randrange(10) for _ in range(10)}) for _ in range(trials)) / trials
assert abs(sim - exact) < 0.05
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Heapsort — trace',
            'text': 'Heapsort is applied to [12, 45, 7, 33, 21, 50, 18]: first bottom-up build-max-heap, then repeatedly swap the root with the last element of the heap, shrink the heap by one and sift the new root down (always toward the **larger** child). What is the array after build-max-heap and **two** such extraction steps?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [12, 45, 7, 33, 21, 50, 18],
                    'caption': 'Input array viewed as a complete binary tree',
                },
            ],
            'options': [
                '[33, 21, 18, 7, 12, 45, 50]',
                '[33, 21, 18, 12, 7, 45, 50]',
                '[45, 33, 18, 12, 21, 7, 50]',
                '[33, 12, 18, 21, 7, 45, 50]',
            ],
            'answer': 'B',
            'solution': '''**Build-max-heap** (sift down indices 2, 1, 0):

- i = 2: 7 vs children 50, 18 → swap with 50 → [12, 45, 50, 33, 21, 7, 18].
- i = 1: 45 vs 33, 21 → already a heap.
- i = 0: 12 vs 45, 50 → swap with 50; at index 2, 12 vs 7, 18 → swap with 18 → [50, 45, 18, 33, 21, 7, 12].

**Extraction 1:** swap 50 ↔ 12 → [12, 45, 18, 33, 21, 7 | 50]; sift 12: children 45, 18 → 45; then children 33, 21 → 33 → [45, 33, 18, 12, 21, 7 | 50].

**Extraction 2:** swap 45 ↔ 7 → [7, 33, 18, 12, 21 | 45, 50]; sift 7: children 33, 18 → 33; then children 12, 21 → 21 → [33, 21, 18, 12, 7 | 45, 50].

Answer (B).

- (A) sifts 7 toward the *smaller* child 12 in the second extraction.
- (C) is the state after only one extraction.
- (D) stops the second sift after one level and mis-orders 12 and 21.

**Tip:** after k extractions the last k cells hold the k largest keys in sorted order — a quick sanity check (45, 50 here).''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [50, 45, 18, 33, 21, 7, 12],
                    'caption': 'After build-max-heap',
                },
                {
                    'type': 'array',
                    'values': [33, 21, 18, 12, 7, 45, 50],
                    'highlight': [5, 6],
                    'caption': 'After two extractions (sorted suffix shaded)',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

def sift(a, i, n):
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m
a = [12, 45, 7, 33, 21, 50, 18]; n = 7
for i in range(n // 2 - 1, -1, -1): sift(a, i, n)
assert a == [50, 45, 18, 33, 21, 7, 12]
for _ in range(2):
    a[0], a[n - 1] = a[n - 1], a[0]; n -= 1; sift(a, 0, n)
opts = {'A': [33, 21, 18, 12, 7, 45, 50], 'B': [33, 21, 18, 7, 12, 45, 50],
        'C': [45, 33, 18, 12, 21, 7, 50], 'D': [33, 12, 18, 21, 7, 45, 50]}
assert [k for k in opts if opts[k] == a] == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'DAGs — counting topological orders',
            'text': 'The number of distinct topological orderings of the directed acyclic graph below is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'C'],
                        ['B', 'C'],
                        ['C', 'E'],
                        ['B', 'D'],
                        ['D', 'E'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [1.5, 2],
                        'D': [1.5, 0],
                        'E': [3, 2],
                        'F': [3, 0],
                        'G': [4.5, 1],
                    },
                },
            ],
            'answer': '14',
            'solution': '''Every vertex reaches G (via E or F), so G is always **last**; count orders of A–F.

Ignore A first. B must precede C and D, so B comes first among {B, C, D, E, F}. The remaining constraints are C < E, D < E, D < F. Orders of {C, D, E, F}:

- C D E F, C D F E, D C E F, D C F E, D F C E → **5** orders.

Now insert A; its only constraint is A < C. For each order (with B in front), count the slots before C:

- B C D E F → A can go before B or between B and C: 2.
- B C D F E → 2.
- B D C E F → before B, after B, after D: 3.
- B D C F E → 3.
- B D F C E → 4.

Total = 2 + 2 + 3 + 3 + 4 = **14**.

**Trap:** treating A and B symmetrically (both are sources) — B has more successors (C and D), so it is far more constrained than A.''',
            'verify': '''
import itertools
E = [("A","C"),("B","C"),("C","E"),("B","D"),("D","E"),("D","F"),("E","G"),("F","G")]
c = 0
for p in itertools.permutations("ABCDEFG"):
    pos = {v: i for i, v in enumerate(p)}
    c += all(pos[u] < pos[v] for u, v in E)
assert c == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Monotonic stack — next greater element',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def nge(a):
    res = [-1] * len(a)
    st = []                      # stack of indices
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res

print(nge([4, 7, 3, 5, 9, 1, 6]))''',
            'options': [
                '`[7, 9, 9, 9, -1, 6, -1]`',
                '`[7, 9, 5, 9, -1, 6, 6]`',
                '`[7, 9, 5, 9, -1, 6, -1]`',
                '`[7, -1, 5, 9, -1, 6, -1]`',
            ],
            'answer': 'C',
            'solution': '''The stack holds indices whose next greater element is still unknown; their values are decreasing from bottom to top. A new x pops every smaller value — x is their answer.

- i=0 (4): push → st = [4].
- i=1 (7): pop 4 → res[0] = 7; push → [7].
- i=2 (3): push → [7, 3].
- i=3 (5): pop 3 → res[2] = 5; 7 > 5 stop; push → [7, 5].
- i=4 (9): pop 5 → res[3] = 9; pop 7 → res[1] = 9; push → [9].
- i=5 (1): push → [9, 1].
- i=6 (6): pop 1 → res[5] = 6; push → [9, 6].
- End: 9 and 6 remain → −1.

Output `[7, 9, 5, 9, -1, 6, -1]` → option (C).

- (A) gives the *maximum to the right* for index 2, not the next greater.
- (B) assigns the last element its own value.
- (D) misses that 7 is popped by 9.

**Complexity:** each index is pushed and popped at most once → Θ(n) total, even though there is a nested `while` loop (amortised analysis).''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [9, 6],
                    'label': 'st (values)',
                    'caption': 'Stack at the end — these keep −1',
                },
            ],
            'verify': "ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[7, 9, 5, 9, -1, 6, -1]' and ANSWER == 'D'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Binary search on the answer',
            'text': "Packages with weights `w` must be shipped **in the given order** within D = 3 days; each day a contiguous block of packages is loaded and its total weight may not exceed the ship's capacity c. The program below binary-searches for the minimum feasible c. The value printed is ______.",
            'code': '''w = [7, 2, 5, 10, 8, 3, 6]
D = 3

def days(c):
    d, cur = 1, 0
    for x in w:
        if cur + x > c:
            d, cur = d + 1, 0
        cur += x
    return d

lo, hi = max(w), sum(w)
while lo < hi:
    mid = (lo + hi) // 2
    if days(mid) <= D:
        hi = mid
    else:
        lo = mid + 1
print(lo)''',
            'answer': '17',
            'solution': '''`days(c)` is non-increasing in c, so feasibility is monotone and the smallest feasible c can be found by a lower-bound binary search over [max(w), sum(w)] = [10, 41].

- lo=10, hi=41: mid=25 → loads 7+2+5+10 = 24 | 8+3+6 = 17 → 2 days ≤ 3 → hi = 25.
- lo=10, hi=25: mid=17 → 7+2+5 = 14 | 10 | 8+3+6 = 17 → 3 days → hi = 17.
- lo=10, hi=17: mid=13 → 9 | 5 | 10 | 8+3 | 6 → 5 days → lo = 14.
- lo=14, hi=17: mid=15 → 14 | 10 | 11 | 6 → 4 days → lo = 16.
- lo=16, hi=17: mid=16 → 14 | 10 | 11 | 6 → 4 days → lo = 17.
- lo = hi = 17 → print **17**.

Check: c = 17 works (14 | 10 | 17) and c = 16 does not (the last block 8 + 3 + 6 = 17 must be split).

Cost: O(n log(∑w)) — 5 iterations of an O(n) check here.

**Trap:** starting with lo = 1 is still correct but slower; starting with lo = sum/D ≈ 13.7 and *rounding down* is fine too, but returning `mid` instead of `lo` can be off by one.''',
            'verify': '''
import itertools
best = min(max(sum(w[a:b]) for a, b in zip((0,) + cuts, cuts + (7,)))
           for cuts in itertools.combinations(range(1, 7), 2))
assert int(OUTPUT) == best == int(ANSWER)
''',
        },
    ],
}
