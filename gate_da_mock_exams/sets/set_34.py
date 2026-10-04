# Set 34 — Full-Syllabus Mock — Paper 4 (GATE-level)
SET = {
    'number': 34,
    'title': 'Full-Syllabus Mock — Paper 4',
    'difficulty': 'GATE-level',
    'focus': 'balanced paper across the whole Section 4 syllabus',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — closures and late binding',
            'text': 'What is printed by the following Python program?',
            'code': '''fs = [lambda: i * 2 for i in range(3)]
gs = [lambda i=i: i * 2 for i in range(3)]
print(sum(f() for f in fs), sum(g() for g in gs))''',
            'options': ['`6 6`', '`12 12`', '`12 6`', '`0 6`'],
            'answer': 'C',
            'solution': '''**Concept.** A lambda looks up a free variable when it is *called*, not when it is created (late binding). All closures created in one comprehension share the comprehension's single variable `i`, whose final value is 2. A default argument, in contrast, is evaluated once at definition time and stored with each function.

**Trace.**
- `fs`: three lambdas, each computing `i * 2` with the *final* i = 2 → 4 + 4 + 4 = 12.
- `gs`: defaults capture 0, 1, 2 respectively → 0 + 2 + 4 = 6.

Output: `12 6`.

**Options.**
- (A) assumes the plain lambdas also capture the current i.
- (B) assumes the default-argument trick does not help.
- (D) assumes the free i is 0 (its first value).

**Tip:** `i=i` (or `functools.partial`) is the idiomatic fix for late binding in loops.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '12 6' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python — floor division and modulo with negatives',
            'text': 'What value is printed by the following Python statement?',
            'code': 'print(-17 // 5 + -17 % 5 + 17 // -5)',
            'answer': '-5',
            'solution': '''**Concept.** Python's `//` is *floor* division (rounds towards −∞), and `%` is defined so that `a == (a // b) * b + a % b` always holds; hence the remainder has the sign of the divisor.

**Evaluation.**
- −17 // 5 = ⌊−3.4⌋ = **−4** (not −3).
- −17 % 5 = −17 − (−4)(5) = −17 + 20 = **3**.
- 17 // −5 = ⌊−3.4⌋ = **−4**.
- Sum = −4 + 3 − 4 = **−5**.

Note the unary minus binds tighter than `//` and `%`, so `-17 // 5` is (−17) // 5.

**Trap:** C/Java truncate towards zero, giving −3, −2 and −3 (sum −8). Python never truncates with `//`.''',
            'verify': '''
import math
v = math.floor(-17 / 5) + (-17 - 5 * math.floor(-17 / 5)) + math.floor(17 / -5)
assert v == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — infix to postfix',
            'text': '''The infix expression

`a - b * (c ^ d ^ e - f) / g + h`

is converted to postfix with the usual operator-stack algorithm, where `^` has the highest precedence and is **right-associative**, `*` and `/` come next, `+` and `-` are lowest, and all binary operators other than `^` are left-associative. The postfix expression is''',
            'options': [
                '`a b c d e ^ ^ f - * g / h + -`',
                '`a b c d ^ e ^ f - * g / - h +`',
                '`a b c d e ^ ^ f - g / * - h +`',
                '`a b c d e ^ ^ f - * g / - h +`',
            ],
            'answer': 'D',
            'solution': '''**Concept.** On reading an operator, pop operators of higher precedence, and of *equal* precedence only if the incoming operator is left-associative. For right-associative `^`, an incoming `^` does not pop a `^` already on the stack.

**Structure.** c ^ d ^ e = c ^ (d ^ e) → `c d e ^ ^`; then `− f` → `c d e ^ ^ f −`. `b * ( … ) / g` is ((b * ( … )) / g) by left associativity → `b … * g /`. Then a − (that) and finally + h, both left-associative: ((a − X) + h).

Result: `a b c d e ^ ^ f - * g / - h +`.

**Options.**
- (A) computes a − (X + h), as if `+` had higher precedence than `−`.
- (B) treats `^` as left-associative ((c ^ d) ^ e).
- (C) applies `/` before `*`, i.e. b * (… / g) — wrong for left-associative `*`/`/`.

**Tip:** check the *last* operator of the postfix — it must be the operator applied last (here the final `+`).''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

def topost(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}; out, st = [], []
    for c in s.split():
        if c.isalpha(): out.append(c)
        elif c == '(': st.append(c)
        elif c == ')':
            while st[-1] != '(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (prec[st[-1]] > prec[c] or
                    (prec[st[-1]] == prec[c] and c != '^')):
                out.append(st.pop())
            st.append(c)
    return " ".join(out + st[::-1])
r = topost("a - b * ( c ^ d ^ e - f ) / g + h")
opts = ["a b c d e ^ ^ f - * g / - h +", "a b c d ^ e ^ f - * g / - h +",
        "a b c d e ^ ^ f - g / * - h +", "a b c d e ^ ^ f - * g / h + -"]
assert opts["ABCD".index(ANSWER)] == r
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Queues — queue using two stacks',
            'text': '''A queue is implemented with two stacks S1 and S2. ENQUEUE(x) pushes x onto S1. DEQUEUE pops from S2; if S2 is empty, it first pops **every** element of S1 and pushes it onto S2. Starting with both stacks empty, the operations

E E E D E E D D D E D D

are performed (E = enqueue of a new element, D = dequeue). The total number of elements moved from S1 to S2 is ______.''',
            'answer': '6',
            'solution': '''**Concept.** Each element is moved from S1 to S2 at most once in its lifetime, so the total transfer cost is at most the number of enqueues — giving O(1) amortised cost per operation. Transfers happen only when S2 is empty at a dequeue.

**Trace** (elements numbered 1, 2, … in enqueue order; stacks shown bottom → top):
- E1 E2 E3: S1 = [1, 2, 3].
- D: S2 empty → move 3 elements (total 3): S2 = [3, 2, 1]; pop 1.
- E4 E5: S1 = [4, 5].
- D: pop 2.  D: pop 3.  S2 now empty.
- D: move 2 elements (total 5): S2 = [5, 4]; pop 4.
- E6: S1 = [6].
- D: pop 5.
- D: S2 empty → move 1 element (total 6); pop 6.

Total moves = 3 + 2 + 1 = **6** (= number of enqueues, since every element was dequeued).

**Trap:** transferring on *every* dequeue (even when S2 is non-empty) would break FIFO order as well as the cost bound.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [3, 2, 1],
                    'label': 'S2 after first transfer',
                    'caption': 'The oldest element 1 is on top of S2',
                },
            ],
            'verify': '''
S1, S2, moved, k, out = [], [], 0, 0, []
for o in "E E E D E E D D D E D D".split():
    if o == 'E': k += 1; S1.append(k)
    else:
        if not S2:
            while S1: S2.append(S1.pop()); moved += 1
        out.append(S2.pop())
assert out == [1, 2, 3, 4, 5, 6] and moved == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Recurrences — master theorem',
            'text': 'Which of the following recurrences has/have the solution T(n) = Θ(n log n)? (T(1) = 1 in each case.)',
            'options': [
                'T(n) = 2T(n/2) + n',
                'T(n) = 4T(n/2) + n',
                'T(n) = 2T(n/4) + √n',
                'T(n) = 3T(n/3) + 5n',
            ],
            'answer': ['A', 'D'],
            'solution': '''**Master theorem** for T(n) = aT(n/b) + f(n): compare f(n) with n^{log_b a}.

- (A) a = 2, b = 2: n^{log₂2} = n = f(n) → case 2 → Θ(n log n). **Yes.**
- (B) a = 4, b = 2: n^{log₂4} = n² dominates f(n) = n → case 1 → Θ(n²). **No.**
- (C) a = 2, b = 4: n^{log₄2} = n^{1/2} = √n = f(n) → case 2 → Θ(√n log n). **No** — it has a log factor but not n log n.
- (D) a = 3, b = 3: n^{log₃3} = n, f(n) = 5n = Θ(n) → case 2 → Θ(n log n). **Yes** (the constant 5 does not matter).

**Trap:** (C) looks like merge sort's 'balanced' case and indeed falls in case 2, but the critical exponent is ½, so the answer is √n log n.''',
            'verify': '''
import math
from functools import lru_cache
def mk(a, b, f):
    @lru_cache(None)
    def T(n): return 1 if n <= 1 else a * T(n // b) + f(n)
    return T
recs = {'A': (2, 2, lambda n: n), 'B': (4, 2, lambda n: n),
        'C': (2, 4, lambda n: math.sqrt(n)), 'D': (3, 3, lambda n: 5 * n)}
good = []
for k, (a, b, f) in recs.items():
    T = mk(a, b, f)
    r1 = T(b ** 8) / (b ** 8 * math.log(b ** 8))
    r2 = T(b ** 12) / (b ** 12 * math.log(b ** 12))
    if 0.5 < r2 / r1 < 2: good.append(k)
assert good == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary trees — reconstruction from traversals',
            'text': '''A binary tree with distinct keys has

pre-order: 8, 3, 5, 1, 9, 2, 6, 4, 7
in-order: 5, 1, 3, 2, 9, 8, 6, 7, 4

Its post-order traversal is''',
            'options': [
                '1, 5, 9, 2, 3, 7, 4, 6, 8',
                '1, 5, 2, 9, 3, 7, 4, 6, 8',
                '5, 1, 2, 9, 3, 4, 7, 6, 8',
                '1, 5, 2, 9, 3, 4, 7, 6, 8',
            ],
            'answer': 'B',
            'solution': '''**Concept.** The first pre-order key is the root; its position in the in-order splits the remaining keys into left and right subtrees. Recurse.

**Reconstruction.**
- Root 8. In-order left of 8: {5, 1, 3, 2, 9}; right: {6, 7, 4}.
- Left part, pre-order 3, 5, 1, 9, 2 → root 3; in-order 5, 1 | 3 | 2, 9.
  - {5, 1}: pre 5, 1 → root 5, in-order 5, 1 → 1 is 5's right child.
  - {2, 9}: pre 9, 2 → root 9, in-order 2, 9 → 2 is 9's left child.
- Right part, pre-order 6, 4, 7 → root 6; in-order 6 | 7, 4 → right subtree {7, 4}: root 4 with left child 7.

**Post-order:** 1, 5, 2, 9, 3, 7, 4, 6, 8.

**Options.**
- (A) makes 2 the *right* child of 9.
- (C) makes 1 the left child of 5 (in-order 5, 1 says 1 comes after 5, i.e. right).
- (D) makes 7 the right child of 4.

**Tip:** pre-order + in-order (or post-order + in-order) determines a binary tree uniquely; pre-order + post-order alone does not.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        8,
                        [
                            3,
                            [
                                5,
                                None,
                                [1],
                            ],
                            [
                                9,
                                [2],
                                None,
                            ],
                        ],
                        [
                            6,
                            None,
                            [
                                4,
                                [7],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'Reconstructed tree',
                },
            ],
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

def build(pre, ino):
    if not pre: return None
    r = pre[0]; k = ino.index(r)
    return [r, build(pre[1:k + 1], ino[:k]), build(pre[k + 1:], ino[k + 1:])]
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
t = build([8, 3, 5, 1, 9, 2, 6, 4, 7], [5, 1, 3, 2, 9, 8, 6, 7, 4])
opts = ["1, 5, 2, 9, 3, 7, 4, 6, 8", "1, 5, 9, 2, 3, 7, 4, 6, 8",
        "5, 1, 2, 9, 3, 4, 7, 6, 8", "1, 5, 2, 9, 3, 4, 7, 6, 8"]
assert opts["ABCD".index(ANSWER)] == ", ".join(map(str, post(t)))
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — double hashing',
            'text': 'A hash table has 13 slots (0–12) and uses double hashing: the i-th probe for key k (i = 0, 1, 2, …) is (h₁(k) + i·h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). Keys 20, 25, 30, 46, 59 are inserted in that order into an empty table. In which slot is 59 stored?',
            'options': ['9', '8', '11', '2'],
            'answer': 'A',
            'solution': '''**Concept.** In double hashing the step size depends on the key, so keys with the same home slot follow different probe sequences (no secondary clustering).

**Trace.**
- 20: h₁ = 7 → slot 7.
- 25: h₁ = 12 → slot 12.
- 30: h₁ = 4 → slot 4.
- 46: h₁ = 7 (full); h₂ = 1 + 46 mod 11 = 1 + 2 = 3 → 7 + 3 = **10**.
- 59: h₁ = 59 mod 13 = 7, h₂ = 1 + 59 mod 11 = 1 + 4 = 5. Probes: 7 (full), 12 (full), 17 mod 13 = 4 (full), 22 mod 13 = **9** (free).

59 is stored in slot **9** after 4 probes.

**Options.**
- (B) 8 is what linear probing would give (7 full → 8).
- (C) 11 uses h₂ = k mod 11 = 4 (forgetting the '1 +'): 7 → 11.
- (D) 2 uses h₂ = 1 + (k mod 13) = 8: 7 → 15 mod 13 = 2.

**Tip:** h₂ must never be 0 (hence the '1 +'), and should be coprime to the table size — with a prime size like 13 every probe sequence visits all slots.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        4: 30,
                        7: 20,
                        9: 59,
                        10: 46,
                        12: 25,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

T = [None] * 13
for k in [20, 25, 30, 46, 59]:
    i = 0
    while T[(k % 13 + i * (1 + k % 11)) % 13] is not None: i += 1
    T[(k % 13 + i * (1 + k % 11)) % 13] = k
assert ["8", "9", "11", "2"]["ABCD".index(ANSWER)] == str(T.index(59))
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Quicksort — counting comparisons',
            'text': 'Quicksort with the Lomuto partition (pivot = last element of the sub-array; one comparison `A[j] <= pivot` for each other element of the sub-array) sorts A = [3, 7, 1, 9, 5, 2]. Sub-arrays of size 0 or 1 are not partitioned. The total number of comparisons is ______.',
            'answer': '9',
            'solution': '''**Concept.** Partitioning a sub-array of size s costs s − 1 comparisons. Total cost depends on how balanced the pivots are.

**Trace.**
- Partition [3, 7, 1, 9, 5, 2], pivot 2 (5 comparisons): only 1 ≤ 2 → [1, 2, 3, 9, 5, 7], pivot at index 1. Left part [1] (size 1), right part [3, 9, 5, 7].
- Partition [3, 9, 5, 7], pivot 7 (3 comparisons): 3 and 5 ≤ 7 → [3, 5, 7, 9]. Left part [3, 5], right part [9].
- Partition [3, 5], pivot 5 (1 comparison) → [3, 5]; parts [3] and [].

Total = 5 + 3 + 1 = **9**.

**Trap:** the pivot 2 is the second smallest — a poor split — so the right part of size 4 still needs work; a perfectly balanced run on 6 keys would use fewer comparisons, a sorted input would use the maximum 5 + 4 + 3 + 2 + 1 = 15.''',
            'verify': '''
c = [0]
def qs(A, lo, hi):
    if lo >= hi: return
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        c[0] += 1
        if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    qs(A, lo, i); qs(A, i + 2, hi)
A = [3, 7, 1, 9, 5, 2]; qs(A, 0, 5)
assert A == sorted(A) and c[0] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph theory — degree sequences',
            'text': 'Which of the following sequences is/are the degree sequence of some **simple** undirected graph (no loops, no multiple edges)?',
            'options': ['3, 3, 3, 3, 2, 2', '4, 4, 3, 1, 1, 1', '5, 3, 3, 2, 2, 1', '5, 5, 4, 2, 1, 1'],
            'answer': ['A', 'C'],
            'solution': '''**Tools.** The degree sum must be even (handshaking lemma), and the Havel–Hakimi test: remove the largest degree d, subtract 1 from the next d largest, repeat; the sequence is graphical iff this ends with all zeros.

- (A) Sum 16. 3,3,3,3,2,2 → remove 3: 2,2,2,2,2 → remove 2: 1,1,2,2 → sort 2,2,1,1 → remove 2: 1,0,1 → 1,1,0 → remove 1: 0,0. **Graphical.**
- (B) Sum 14 (even), but: the two vertices of degree 4 each need 4 neighbours among the other 5 vertices. Apart from each other they each need 3 more from {3, 1, 1, 1}; the three degree-1 vertices can each serve only one of them, so at most 1 + 3 = 4 slots are available for 6 demands. Havel–Hakimi: 4,4,3,1,1,1 → 3,2,0,0,1 → sort 3,2,1,0,0 → 1,0,−1 ✗. **Not graphical.**
- (C) Sum 16. 5,3,3,2,2,1 → 2,2,1,1,0 → 1,0,1,0 → 1,1,0,0 → 0,0,0. **Graphical.**
- (D) Sum 18 (even), but two vertices of degree 5 in a 6-vertex graph are adjacent to *all* other vertices, forcing every vertex to have degree ≥ 2 — yet two vertices have degree 1. **Not graphical.**

**Trap:** an even sum is necessary but not sufficient.''',
            'verify': '''
def hh(seq):
    s = sorted(seq, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d): s[i] -= 1
        if min(s) < 0: return False
        s.sort(reverse=True)
    return True
opts = [[3, 3, 3, 3, 2, 2], [4, 4, 3, 1, 1, 1], [5, 3, 3, 2, 2, 1], [5, 5, 4, 2, 1, 1]]
assert [L for L, o in zip("ABCD", opts) if hh(o)] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — worst-case probes',
            'text': 'Standard binary search (mid = ⌊(lo + hi)/2⌋, three-way comparison at each probe, stop when found or when lo > hi) is performed on a sorted array of **200** distinct elements. The maximum number of array elements probed over all possible search keys (present or absent) is ______.',
            'answer': '8',
            'solution': '''**Concept.** Binary search follows a root-to-node path in an implicit balanced BST of n nodes. The worst case equals the height of that tree in nodes: ⌊log₂ n⌋ + 1.

**Computation.** 2⁷ = 128 ≤ 200 < 256 = 2⁸, so ⌊log₂ 200⌋ = 7 and the maximum number of probes is 7 + 1 = **8**.

**Intuition.** After k probes at most 2^{k} − 1 elements can have been 'covered'. With 7 probes only 127 < 200 elements can be distinguished, so 8 are needed; 8 probes cover up to 255.

**Trap:** answering ⌈log₂ 200⌉ = 8 happens to coincide here, but the correct general formula is ⌊log₂ n⌋ + 1 (for n = 256 it gives 9, not 8).''',
            'verify': '''
A = list(range(0, 400, 2)); worst = 0
for x in range(-1, 401):
    lo, hi, c = 0, 199, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if A[m] == x: break
        if A[m] < x: lo = m + 1
        else: hi = m - 1
    worst = max(worst, c)
assert worst == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — generator exhaustion and `in`',
            'text': 'What is printed by the following Python program?',
            'code': '''g = (x * x for x in range(6))
a = 4 in g
b = list(g)
c = 16 in g
print(a, b, c)''',
            'options': [
                '`True [0, 1, 4, 9, 16, 25] True`',
                '`True [9, 16, 25] True`',
                '`True [9, 16, 25] False`',
                '`True [16, 25] False`',
            ],
            'answer': 'C',
            'solution': '''**Concept.** A generator is an iterator: it produces each value once. The `in` operator on an iterator *consumes* values until it finds a match (or exhausts it), and `list(g)` consumes everything that is left.

**Trace.** g will yield 0, 1, 4, 9, 16, 25.
- `4 in g` consumes 0, 1, 4 and stops at the match → a = True.
- `list(g)` takes the remaining 9, 16, 25 → b = [9, 16, 25]; g is now exhausted.
- `16 in g` finds nothing left → c = False (even though 16 was produced earlier).

Output: `True [9, 16, 25] False`.

**Options.**
- (A) treats g like a list that can be re-scanned.
- (B) forgets that `list(g)` exhausted the generator.
- (D) assumes `in` also consumed the element *after* the match.

**Trap:** membership tests on generators/iterators have side effects; convert to a list or set first if you need repeated lookups.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'True [9, 16, 25] False' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Linked lists — reversing a sub-list in place',
            'text': 'The function below reverses the nodes at positions m..n (1-based) of a singly linked list by repeatedly moving the node after `cur` to the front of the sub-list. The program prints the final list as one integer. What is printed?',
            'code': '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def rev_between(head, m, n):
    dummy = Node(0, head)
    pre = dummy
    for _ in range(m - 1):
        pre = pre.next
    cur = pre.next
    for _ in range(n - m):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next

head = None
for v in reversed([4, 1, 7, 3, 9, 2, 6, 5]):
    head = Node(v, head)
p, s = rev_between(head, 3, 6), ""
while p:
    s, p = s + str(p.val), p.next
print(int(s))''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [4, 1, 7, 3, 9, 2, 6, 5],
                    'head': 'head',
                    'caption': 'Input list (positions 1–8)',
                },
            ],
            'answer': '41293765',
            'solution': '''**Concept.** `pre` stays fixed on the node just before position m, and `cur` stays on the node that was originally at position m (it drifts towards the end of the reversed block). Each iteration unlinks `cur.next` and inserts it right after `pre` — head insertion inside the block — so n − m = 3 iterations reverse positions 3..6.

**Trace.** pre = node 1 (value 1), cur = node 7.
- start: 4 1 [7 3 9 2] 6 5
- iter 1: move 3 to front of block → 4 1 [3 7 9 2] 6 5
- iter 2: move 9 → 4 1 [9 3 7 2] 6 5
- iter 3: move 2 → 4 1 [2 9 3 7] 6 5

The printed integer is **41293765**.

**Why a dummy node?** If m = 1 there is no real predecessor; the dummy makes that case identical to the others and `dummy.next` is the (possibly new) head.

**Trap:** advancing `cur` in the loop (as in ordinary reversal) would break the algorithm — here `cur` must stay put while nodes are pulled past it.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [4, 1, 2, 9, 3, 7, 6, 5],
                    'head': 'head',
                    'caption': 'After reversing positions 3–6',
                },
            ],
            'verify': '''
L = [4, 1, 7, 3, 9, 2, 6, 5]
L[2:6] = L[2:6][::-1]
assert int("".join(map(str, L))) == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'BST — reconstruction from post-order',
            'text': '''The post-order traversal of a binary search tree T with distinct keys is

12, 20, 18, 31, 27, 15, 44, 52, 48, 40

Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)''',
            'options': [
                'The pre-order traversal of T is 40, 15, 12, 27, 18, 20, 31, 48, 44, 52',
                'The height of T is 4',
                'T has exactly 5 leaves',
                'The in-order successor of 27 in T is 40',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept.** In a BST's post-order, the last key is the root; the keys before it split into a prefix of keys smaller than the root (left subtree) and the following keys larger than it (right subtree). Recurse.

**Reconstruction.**
- Root 40; left post-order 12, 20, 18, 31, 27, 15; right 44, 52, 48.
- Left: root 15; smaller {12}; larger 20, 18, 31, 27 → root 27 with left post 20, 18 (root 18, right child 20) and right 31.
- Right: root 48 with children 44 and 52.

**Statements.**
- (A) Pre-order: 40, 15, 12, 27, 18, 20, 31, 48, 44, 52. **True.**
- (B) Longest path 40 → 15 → 27 → 18 → 20 has 4 edges. **True.**
- (C) Leaves: 12, 20, 31, 44, 52 → 5. **True.**
- (D) 27 has a right subtree {31}, so its successor is the minimum there, **31**. **False.**

**Trap:** the successor of a node is an ancestor only when the node has *no* right subtree.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        40,
                        [
                            15,
                            [12],
                            [
                                27,
                                [
                                    18,
                                    None,
                                    [20],
                                ],
                                [31],
                            ],
                        ],
                        [
                            48,
                            [44],
                            [52],
                        ],
                    ],
                    'caption': 'The BST T',
                },
            ],
            'verify': '''
def build(post):
    if not post: return None
    r = post[-1]; L = [x for x in post[:-1] if x < r]; R = [x for x in post[:-1] if x > r]
    return [r, build(L), build(R)]
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def lv(t): return 0 if t is None else (1 if not t[1] and not t[2] else lv(t[1]) + lv(t[2]))
T = build([12, 20, 18, 31, 27, 15, 44, 52, 48, 40])
io = ino(T)
r = {'A': pre(T) == [40, 15, 12, 27, 18, 20, 31, 48, 44, 52], 'B': h(T) == 4,
     'C': lv(T) == 5, 'D': io[io.index(27) + 1] == 40}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary heaps — mixed operations',
            'text': 'The min-heap shown below is stored in an array. The operations DELETE-MIN, INSERT(4), DELETE-MIN are performed in this order (DELETE-MIN moves the last element to the root and sifts it down, swapping with the smaller child; INSERT appends and sifts up). The final array is',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [3, 8, 5, 12, 10, 9, 7, 15, 14],
                    'caption': 'Initial min-heap [3, 8, 5, 12, 10, 9, 7, 15, 14]',
                },
            ],
            'options': [
                '[4, 5, 7, 8, 10, 9, 14, 15]',
                '[5, 7, 8, 12, 10, 9, 14, 15]',
                '[5, 8, 7, 12, 10, 9, 15, 14]',
                '[5, 8, 7, 12, 10, 9, 14, 15]',
            ],
            'answer': 'D',
            'solution': '''**DELETE-MIN 1.** Remove 3; last element 14 goes to the root: [14, 8, 5, 12, 10, 9, 7, 15]. Sift down: children 8, 5 → swap with 5 → [5, 8, 14, 12, 10, 9, 7, 15]; children of index 2 are 9, 7 → swap with 7 → [5, 8, 7, 12, 10, 9, 14, 15].

**INSERT(4).** Append at index 8 (parent index 3 = 12): swap → index 3; parent index 1 = 8: swap → index 1; parent index 0 = 5: swap → root. Array [4, 5, 7, 8, 10, 9, 14, 15, 12].

**DELETE-MIN 2.** Remove 4; last element 12 to root: [12, 5, 7, 8, 10, 9, 14, 15]. Children 5, 7 → swap with 5 → index 1: children 8, 10 → swap with 8 → index 3: child 15 > 12 → stop. Array **[5, 8, 7, 12, 10, 9, 14, 15]**.

Interesting: the final array equals the array after the first DELETE-MIN — inserting a new minimum and deleting it retraced the same path here.

**Options.**
- (A) is the state before the second DELETE-MIN, with 12 dropped.
- (B) swaps with the left child instead of the smaller child at the first step of sift-down.
- (C) puts 15 and 14 in the wrong leaf positions (14 must sink to index 6 in the first deletion).''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

H = [3, 8, 5, 12, 10, 9, 7, 15, 14]
def down(H):
    last = H.pop()
    if not H: return
    H[0] = last; i, n = 0, len(H)
    while True:
        l, r, b = 2 * i + 1, 2 * i + 2, i
        if l < n and H[l] < H[b]: b = l
        if r < n and H[r] < H[b]: b = r
        if b == i: return
        H[i], H[b] = H[b], H[i]; i = b
def up(H, x):
    H.append(x); i = len(H) - 1
    while i and H[(i - 1) // 2] > H[i]:
        p = (i - 1) // 2; H[p], H[i] = H[i], H[p]; i = p
down(H); up(H, 4); down(H)
opts = ["[5, 8, 7, 12, 10, 9, 14, 15]", "[5, 7, 8, 12, 10, 9, 14, 15]",
        "[5, 8, 7, 12, 10, 9, 15, 14]", "[4, 5, 7, 8, 10, 9, 14, 15]"]
assert opts["ABCD".index(ANSWER)] == str(H)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Complexity — exact loop counting',
            'text': 'What value is printed by the following Python program?',
            'code': '''cnt = 0
for i in range(1, 65):
    j = i
    while j < 64:
        j *= 2
        cnt += 1
print(cnt)''',
            'answer': '120',
            'solution': '''**Concept.** For a fixed i, the inner loop doubles j until j ≥ 64, i.e. it runs ⌈log₂(64/i)⌉ times. Group the values of i by that count.

- i = 1: 1 → 2 → … → 64: 6 iterations → 6
- i = 2, 3: 5 iterations each → 10
- i = 4 … 7: 4 each → 16
- i = 8 … 15: 3 each → 24
- i = 16 … 31: 2 each → 32
- i = 32 … 63: 1 each → 32
- i = 64: 0

Total = 6 + 10 + 16 + 24 + 32 + 32 = **120**.

**Asymptotics.** For general n = 2^{k} the total is ∑_{t=1}^{k} t·2^{k−t} = 2^{k+1} − k − 2 = Θ(n) — not Θ(n log n), because most i need only a few doublings. (Check: 128 − 6 − 2 = 120.)

**Trap:** multiplying the outer count by the worst-case inner count (64 × 6 = 384) gives only an upper bound.''',
            'verify': '''
import math
s = sum(math.ceil(math.log2(64 / i)) for i in range(1, 65))
assert s == 2 ** 7 - 6 - 2 == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra with a negative edge',
            'text': "The standard Dijkstra algorithm (a vertex's distance is never changed after it is extracted from the priority queue) is run from S on the directed graph below, which has one negative edge. Which of the following statements is/are TRUE?",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 2],
                        ['A', 'B', -3],
                        ['A', 'C', 3],
                        ['B', 'C', 5],
                        ['C', 'D', 1],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2.2],
                        'B': [2, -0.2],
                        'C': [4, 1],
                        'D': [6, 1],
                    },
                },
            ],
            'options': [
                'The distance Dijkstra reports for A is the true shortest distance',
                'Dijkstra reports a distance of 7 for C',
                'The true shortest distance from S to D is 7',
                'The graph contains a negative-weight cycle',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Dijkstra trace.**
- Extract S (0): A = 4, B = 2.
- Extract B (2): C = 2 + 5 = 7.
- Extract A (4): A→B would give 1, but B is already extracted — no change. A→C gives 7, not smaller.
- Extract C (7): D = 8. Extract D (8).
Reported: A 4, B 2, C 7, D 8.

**True distances.** B: S→A→B = 4 − 3 = 1. C: min(S→A→C = 7, S→A→B→C = 1 + 5 = 6) = 6. D = 6 + 1 = 7. A = 4.

- (A) **True** — 4 is correct (no path into A other than S→A).
- (B) **True** — Dijkstra reports 7 (wrong; the true value is 6).
- (C) **True** — S→A→B→C→D = 4 − 3 + 5 + 1 = 7.
- (D) **False** — there is no cycle at all; the only negative edge A→B lies on no cycle.

**Concept/Trap.** Dijkstra's greedy choice assumes that a path can only get longer when extended. A negative edge breaks this even without negative cycles; B was finalised at 2 before the cheaper route through A was discovered, and the error propagated to C and D. Bellman–Ford handles this graph correctly.''',
            'verify': '''
E = [("S", "A", 4), ("S", "B", 2), ("A", "B", -3), ("A", "C", 3), ("B", "C", 5),
     ("C", "D", 1)]
V = "SABCD"; INF = float('inf')
d = {v: INF for v in V}; d['S'] = 0; done = set()
while len(done) < 5:
    u = min((v for v in V if v not in done), key=lambda v: d[v]); done.add(u)
    for a, b, w in E:
        if a == u and b not in done and d[u] + w < d[b]: d[b] = d[u] + w
t = {v: INF for v in V}; t['S'] = 0
for _ in range(4):
    for a, b, w in E: t[b] = min(t[b], t[a] + w)
cyc = any(t[a] + w < t[b] for a, b, w in E)
r = {'A': d['A'] == t['A'], 'B': d['C'] == 7, 'C': t['D'] == 7, 'D': cyc}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Graph theory — edges vs components',
            'text': 'A simple undirected graph has 10 vertices and exactly 3 connected components. What is the maximum possible number of edges?',
            'options': ['36', '28', '21', '33'],
            'answer': 'B',
            'solution': '''**Concept.** For fixed n and k components, the edge count is maximised by making each component complete, and among complete components by making one as large as possible: k − 1 isolated vertices and one K_{n−k+1}. (Moving a vertex from a smaller clique of size a to a larger one of size b ≥ a changes the edge count by b − (a − 1) > 0.)

**Computation.** Sizes 8, 1, 1 → C(8, 2) = 28 edges.

Compare other splits: 6 + 2 + 2 → 15 + 1 + 1 = 17; 4 + 3 + 3 → 6 + 3 + 3 = 12; 7 + 2 + 1 → 21 + 1 = 22. The maximum is **28**.

**Options.**
- (A) 36 = C(9, 2) is the maximum with 2 components.
- (C) 21 = C(7, 2) comes from wrongly using n − k = 7 as the clique size.
- (D) 33 has no valid construction.

**Related bound:** the *minimum* number of edges with k components is n − k (a forest).''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

from math import comb
best = 0
for a in range(1, 9):
    for b in range(1, 10 - a):
        c = 10 - a - b
        if c >= 1: best = max(best, comb(a, 2) + comb(b, 2) + comb(c, 2))
assert ["28", "36", "21", "33"]["ABCD".index(ANSWER)] == str(best)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — deletion with tombstones',
            'text': '''A hash table of size 10 uses h(k) = k mod 10 and linear probing. Deletion marks a slot as DELETED (a tombstone): searches continue past DELETED slots, while an insertion stores the new key in the **first** DELETED or empty slot on its probe path. Starting from an empty table:

insert 31, 41, 51, 22, 61; delete 41; insert 71.

The number of slots probed by an unsuccessful search for key 81 (counting the empty slot at which it stops) is ______.''',
            'answer': '6',
            'solution': '''**Concept.** Tombstones keep probe chains intact: an empty slot means 'the key cannot be further along', a DELETED slot does not. Insertions may recycle tombstones.

**Trace.**
- 31 → 1; 41 → 1 full → 2; 51 → 1, 2 full → 3; 22 → 2, 3 full → 4; 61 → 1, 2, 3, 4 full → 5.
- delete 41: slot 2 becomes DELETED.
- insert 71: home 1 (31), slot 2 DELETED → store 71 in slot 2.
- Table: 1:31, 2:71, 3:51, 4:22, 5:61, others empty.
- search 81: home 1 → probes 1, 2, 3, 4, 5 (all occupied, none is 81), 6 empty → stop.

Probes = **6**.

**Trap:** if deletion simply emptied slot 2, a later search for 61 would stop at slot 2 and wrongly report 'not found' — that is why tombstones exist. Note too that the cluster 1–5 still makes every search hashing to slot 1 expensive.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        1: 31,
                        2: 71,
                        3: 51,
                        4: 22,
                        5: 61,
                    },
                    'caption': 'Table before the search for 81',
                },
            ],
            'verify': '''
DEL = object(); T = [None] * 10
def ins(k):
    i = k % 10
    while T[i] is not None and T[i] is not DEL: i = (i + 1) % 10
    T[i] = k
def find(k):
    i, c = k % 10, 0
    while True:
        c += 1
        if T[i] is None: return None, c
        if T[i] == k: return i, c
        i = (i + 1) % 10
for k in [31, 41, 51, 22, 61]: ins(k)
T[find(41)[0]] = DEL
ins(71)
assert find(81) == (None, int(ANSWER)) and T[2] == 71
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Python — exceptions and try/finally',
            'text': 'Consider the following Python definitions. Which of the following statements is/are TRUE?',
            'code': '''log = []

def f(x):
    try:
        log.append("t")
        if x < 0:
            raise ValueError
        return 10 // x
    except ValueError:
        log.append("e")
        return -1
    finally:
        log.append("f")
        if x == 0:
            return 0''',
            'options': [
                '`f(4)` returns 2 and appends exactly "t", "f" to `log`',
                '`f(-3)` returns -1',
                '`f(0)` raises ZeroDivisionError',
                'If `log` is empty and `f(4)`, `f(-3)`, `f(0)` are called in this order, `len(log)` is 7 afterwards',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** A `finally` block always runs — after a `return`, after an exception is handled, and even while an unhandled exception is propagating. If the `finally` block itself executes `return`, that return value replaces whatever was pending, *including a pending exception*, which is silently discarded.

- f(4): log gets "t"; returns 10 // 4 = 2 → finally appends "f"; x ≠ 0 so the pending return 2 stands. (A) **True.**
- f(−3): "t"; ValueError raised and caught: "e", return −1 pending; finally appends "f". Returns −1. (B) **True.**
- f(0): "t"; `10 // 0` raises ZeroDivisionError, which the `except ValueError` clause does not catch; on the way out, finally appends "f" and executes `return 0`, which swallows the exception. So f(0) **returns 0**. (C) **False.**
- Log lengths: 2 + 3 + 2 = 7. (D) **True.**

**Trap:** a `return` (or `break`) inside `finally` hides errors — a notorious source of silent bugs.''',
            'verify': '''
log.clear()
a = f(4); la = list(log)
b = f(-3)
try:
    c = f(0); raised = False
except ZeroDivisionError:
    raised = True
r = {'A': a == 2 and la == ["t", "f"], 'B': b == -1, 'C': raised, 'D': len(log) == 7}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'DFS vs BFS — tree heights on a grid',
            'text': 'Consider the 3 × 3 grid graph below. DFS (recursive, neighbours explored in **alphabetical** order) is run from A, producing a DFS tree. What is the height of this DFS tree (number of edges on its longest root-to-leaf path)?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['G', 'H'],
                        ['H', 'I'],
                        ['A', 'D'],
                        ['D', 'G'],
                        ['B', 'E'],
                        ['E', 'H'],
                        ['C', 'F'],
                        ['F', 'I'],
                    ],
                    'pos': {
                        'A': [0, 4],
                        'B': [2, 4],
                        'C': [4, 4],
                        'D': [0, 2],
                        'E': [2, 2],
                        'F': [4, 2],
                        'G': [0, 0],
                        'H': [2, 0],
                        'I': [4, 0],
                    },
                },
            ],
            'options': ['8', '6', '7', '4'],
            'answer': 'A',
            'solution': '''**Concept.** DFS keeps going deeper as long as an undiscovered neighbour exists, so on a grid it tends to produce long, path-like trees; BFS produces the shallowest possible tree (height = eccentricity of the source).

**DFS trace** (alphabetical neighbours):
- A: neighbours B, D → go to B.
- B: A seen, C → go to C.
- C: B seen, F → F.
- F: C seen, E → E.
- E: B seen, D → D.
- D: A, E seen, G → G.
- G: D seen, H → H.
- H: E, G seen, I → I.
- I: all seen. Backtrack all the way; every vertex is already discovered.

The DFS tree is the Hamiltonian path A–B–C–F–E–D–G–H–I with **8** edges, so its height is **8**.

**Options.** (D) 4 is the height of the **BFS** tree from A (I is at distance 4). (B) and (C) come from backtracking too early.

**Tip:** a DFS tree of a connected graph with n vertices has height between the BFS height and n − 1; here it reaches the maximum n − 1 = 8.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                    'edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['G', 'H'],
                        ['H', 'I'],
                        ['A', 'D'],
                        ['D', 'G'],
                        ['B', 'E'],
                        ['E', 'H'],
                        ['C', 'F'],
                        ['F', 'I'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['B', 'C'],
                        ['C', 'F'],
                        ['E', 'F'],
                        ['D', 'E'],
                        ['D', 'G'],
                        ['G', 'H'],
                        ['H', 'I'],
                    ],
                    'pos': {
                        'A': [0, 4],
                        'B': [2, 4],
                        'C': [4, 4],
                        'D': [0, 2],
                        'E': [2, 2],
                        'F': [4, 2],
                        'G': [0, 0],
                        'H': [2, 0],
                        'I': [4, 0],
                    },
                    'caption': 'DFS tree edges (highlighted)',
                },
            ],
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

E = ["AB", "BC", "DE", "EF", "GH", "HI", "AD", "DG", "BE", "EH", "CF", "FI"]
G = {}
for a, b in E:
    G.setdefault(a, set()).add(b); G.setdefault(b, set()).add(a)
dep = {'A': 0}
def dfs(u):
    for v in sorted(G[u]):
        if v not in dep: dep[v] = dep[u] + 1; dfs(v)
dfs('A')
assert ["4", "6", "7", "8"]["ABCD".index(ANSWER)] == str(max(dep.values()))
''',
        },
    ],
}
