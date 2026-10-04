# Set 19 — Complexity Analysis
SET = {
    "number": 19,
    "title": "Complexity Analysis",
    "difficulty": "GATE-level",
    "focus": "loop-nest complexity, asymptotic comparison, recurrence solving",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — floor division and modulo with negatives",
            "text": "Consider the following Python program. What is printed?",
            "code": '''print(-17 // 5, -17 % 5, 17 // -5, int(-17 / 5))''',
            "options": ["`-3 -2 -3 -3`", "`-4 3 -4 -3`", "`-4 3 -3 -3`", "`-4 -2 -4 -4`"],
            "answer": "B",
            "solution": (
                "Python's `//` is **floor** division (rounds toward −∞), and `%` is defined so that "
                "`a == (a // b) * b + a % b` always holds; hence the remainder takes the sign of the "
                "**divisor**. `int()` on a float truncates toward 0.\n\n"
                "- `-17 // 5`: −17 / 5 = −3.4 → floor → **−4**.\n"
                "- `-17 % 5`: −17 − (−4)(5) = −17 + 20 = **3** (sign of divisor 5).\n"
                "- `17 // -5`: 17 / −5 = −3.4 → floor → **−4**.\n"
                "- `int(-17 / 5)`: −3.4 truncated toward zero → **−3**.\n\n"
                "Output `-4 3 -4 -3` → option (B).\n\n"
                "- (A) is C/Java behaviour (truncation for `/` on ints and a negative remainder).\n"
                "- (C) floors the first but truncates the third — inconsistent.\n"
                "- (D) uses a remainder with the sign of the dividend and floors the last value.\n\n"
                "**Trap:** this matters in complexity questions too — loops like `while i != 0: i //= 2` "
                "never terminate for negative i, because −1 // 2 is −1."
            ),
            "verify": "assert OUTPUT.split() == ['-4', '3', '-4', '-3'] and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Loop counting — geometric loops",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''count = 0
i = 1
while i < 1000:
    j = i
    while j < 1000:
        count += 1
        j *= 2
    i *= 3
print(count)''',
            "answer": "40",
            "solution": (
                "The outer loop takes i = 3⁰, 3¹, …, 3⁶ = 1, 3, 9, 27, 81, 243, 729 (3⁷ = 2187 ≥ 1000). "
                "For a fixed i the inner loop runs for j = i, 2i, 4i, … while j < 1000, i.e. "
                "⌊log₂(999/i)⌋ + 1 times.\n\n"
                "- i = 1: j = 1 … 512 → 10 iterations.\n"
                "- i = 3: j = 3 … 768 (3·2⁸) → 9.\n"
                "- i = 9: j = 9 … 576 (9·2⁶) → 7.\n"
                "- i = 27: j = 27 … 864 (27·2⁵) → 6.\n"
                "- i = 81: j = 81 … 648 (81·2³) → 4.\n"
                "- i = 243: j = 243, 486, 972 → 3.\n"
                "- i = 729: j = 729 → 1.\n\n"
                "Total = 10 + 9 + 7 + 6 + 4 + 3 + 1 = **40**.\n\n"
                "Asymptotically, ∑ over k = 0 … log₃n of (log₂n − k·log₂3) = Θ(log² n) — two nested "
                "logarithmic loops with *dependent* bounds still give Θ(log² n), just with a constant "
                "about half that of independent loops.\n\n"
                "**Trap:** multiplying 7 outer iterations by 10 inner ones (70) ignores that the inner loop "
                "starts at i, not at 1."
            ),
            "verify": "assert int(OUTPUT.strip()) == int(ANSWER) == 40",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Asymptotic comparison of functions",
            "text": ("Consider f₁(n) = 2^{√(log₂ n)}, f₂(n) = n^{1/3}, f₃(n) = (log₂ n)^{10} and "
                     "f₄(n) = n / log₂ n. Which of the following arranges them in increasing order of "
                     "asymptotic growth?"),
            "options": ["f₁ < f₃ < f₂ < f₄", "f₃ < f₂ < f₁ < f₄", "f₃ < f₁ < f₂ < f₄", "f₁ < f₃ < f₄ < f₂"],
            "answer": "C",
            "solution": (
                "Compare logarithms: put L = log₂ n (L → ∞). Then\n\n"
                "- log₂ f₃ = 10 · log₂ L (doubly logarithmic in n),\n"
                "- log₂ f₁ = √L,\n"
                "- log₂ f₂ = L / 3,\n"
                "- log₂ f₄ = L − log₂ L.\n\n"
                "As L → ∞: 10 log₂ L ≪ √L ≪ L/3 < L − log₂ L, and the gaps between these logs tend to "
                "infinity, so the functions themselves are separated by unbounded factors.\n\n"
                "Hence f₃ < f₁ < f₂ < f₄ → option (C).\n\n"
                "- (A) puts 2^{√log n} below polylog — wrong: √L eventually beats 10 log L "
                "(e.g. L = 10⁶: 1000 vs ≈ 199).\n"
                "- (B) puts f₁ above n^{1/3}: √L < L/3 for L > 9.\n"
                "- (D) puts n^{1/3} above n / log n: L/3 < L − log₂ L for large L.\n\n"
                "**Trap:** for small n (e.g. n = 2¹⁶, L = 16) f₃ = 16¹⁰ is astronomically larger than "
                "f₁ = 2⁴ — asymptotic order can disagree badly with small-n intuition."
            ),
            "verify": '''
import math
for L in (1e6, 1e9):
    lg = {'f1': math.sqrt(L), 'f2': L / 3, 'f3': 10 * math.log2(L), 'f4': L - math.log2(L)}
    order = sorted(lg, key=lg.get)
    assert order == ['f3', 'f1', 'f2', 'f4']
assert ANSWER == 'C'
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Recurrences — identifying Θ(n log n)",
            "text": ("For each recurrence below, T(n) = Θ(1) for n ≤ 2. Which of the following recurrences "
                     "has/have the solution T(n) = Θ(n log n)?"),
            "options": ["T(n) = 2T(n/2) + 5n",
                        "T(n) = 4T(n/2) + n log n",
                        "T(n) = T(n/3) + T(2n/3) + n",
                        "T(n) = 3T(n/3) + n / log n"],
            "answer": ["A", "C"],
            "solution": (
                "Use the master theorem (compare f(n) with n^{log_b a}) or the recursion-tree method.\n\n"
                "- (A) a = 2, b = 2 → n^{log₂2} = n; f(n) = 5n = Θ(n) → case 2 → Θ(n log n). **Yes.**\n"
                "- (B) a = 4, b = 2 → n^{log₂4} = n²; f(n) = n log n = O(n^{2−ε}) → case 1 → Θ(n²). **No.**\n"
                "- (C) Not master-theorem form, but the recursion tree has cost n at every level "
                "(n/3 + 2n/3 = n). The shortest root-to-leaf path has log₃ n levels and the longest "
                "log_{3/2} n, both Θ(log n), so T(n) = Θ(n log n). **Yes.**\n"
                "- (D) a = b = 3 → n^{log₃3} = n; f(n) = n / log n is smaller than n only by a log factor, "
                "so the master theorem does not apply. Level i of the tree costs n / log(n/3^i), and "
                "summing gives n · ∑ 1/j = Θ(n log log n). **No.**\n\n"
                "**Trap:** (D) ‘looks like’ case 2 — but f must be Θ(n^{log_b a} · log^k n) with k ≥ 0; "
                "here k = −1, which gives n log log n."
            ),
            "verify": '''
import math
from functools import lru_cache
import sys; sys.setrecursionlimit(10000)
@lru_cache(None)
def TA(n): return 1 if n <= 2 else 2*TA(n//2) + 5*n
@lru_cache(None)
def TB(n): return 1 if n <= 2 else 4*TB(n//2) + n*math.log2(n)
@lru_cache(None)
def TC(n): return 1 if n <= 2 else TC(n//3) + TC(n - n//3) + n
@lru_cache(None)
def TD(n): return 1 if n <= 2 else 3*TD(n//3) + n/math.log2(n)
def r(T, n): return T(n) / (n * math.log2(n))
grow = {k: r(T, 2**40) / r(T, 2**20) for k, T in (('A',TA),('B',TB),('C',TC),('D',TD))}
assert 0.9 < grow['A'] < 1.1 and 0.9 < grow['C'] < 1.1
assert grow['B'] > 1000 and grow['D'] < 0.8
assert sorted(ANSWER) == ['A', 'C']
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Stacks — postfix evaluation",
            "text": ("The postfix expression below is evaluated with a stack (`^` denotes exponentiation; all "
                     "operators are binary; for an operator the top of the stack is the **right** operand):\n\n"
                     "6 2 3 + * 4 2 ^ 7 − 3 / −\n\n"
                     "The value of the expression is ______."),
            "answer": "27",
            "solution": (
                "Scan left to right: push operands; on an operator pop the right operand b, then the left "
                "operand a, and push a op b. Each token costs O(1), so evaluation is Θ(n) for n tokens.\n\n"
                "- 6, 2, 3 → stack [6, 2, 3].\n"
                "- `+` → 2 + 3 = 5 → [6, 5].\n"
                "- `*` → 6 × 5 = 30 → [30].\n"
                "- 4, 2 → [30, 4, 2]; `^` → 4² = 16 → [30, 16].\n"
                "- 7 → [30, 16, 7]; `−` → 16 − 7 = 9 → [30, 9].\n"
                "- 3 → [30, 9, 3]; `/` → 9 / 3 = 3 → [30, 3].\n"
                "- `−` → 30 − 3 = **27**.\n\n"
                "The equivalent infix form is 6 × (2 + 3) − (4² − 7) / 3. The stack never holds more "
                "than 3 values.\n\n"
                "**Trap:** popping in the wrong order turns 16 − 7 into 7 − 16 and 9 / 3 into 3 / 9; the "
                "**first** pop is the right operand."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Stack after each operator",
                                   "row_labels": ["+", "*", "^", "− (1st)", "/", "− (2nd)"],
                                   "col_labels": ["stack (bottom → top)"],
                                   "rows": [["6  5"], ["30"], ["30  16"], ["30  9"], ["30  3"], ["27"]]}],
            "verify": '''
import operator as op
F = {'+': op.add, '*': op.mul, '^': op.pow, '-': op.sub, '/': op.truediv}
st = []
for t in "6 2 3 + * 4 2 ^ 7 - 3 / -".split():
    if t in F:
        b = st.pop(); a = st.pop(); st.append(F[t](a, b))
    else:
        st.append(int(t))
assert st == [int(ANSWER)]
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Complexity of a halving loop nest",
            "text": "What is the time complexity of the following function, as a function of n ≥ 1?",
            "code": '''def f(n):
    s = 0
    i = n
    while i > 0:
        for j in range(i):
            s += 1
        i //= 2
    return s''',
            "options": ["Θ(n)", "Θ(n log n)", "Θ(log² n)", "Θ(n²)"],
            "answer": "A",
            "solution": (
                "The outer loop runs ⌊log₂ n⌋ + 1 times, but the inner loop's length *shrinks* "
                "geometrically, so we must sum the actual work rather than multiply.\n\n"
                "Total inner iterations = n + ⌊n/2⌋ + ⌊n/4⌋ + … + 1 ≤ n(1 + 1/2 + 1/4 + …) < 2n.\n"
                "It is also at least n (the first pass alone). Hence the running time is **Θ(n)**.\n\n"
                "Example: n = 100 → 100 + 50 + 25 + 12 + 6 + 3 + 1 = 197 < 200.\n\n"
                "- (A) **Correct** — geometric series bounded by 2n.\n"
                "- (B) Θ(n log n) multiplies log n outer iterations by the *largest* inner cost n — an "
                "upper bound, but not tight.\n"
                "- (C) counts only loop *headers*, not the inner work.\n"
                "- (D) would require the inner loop to shrink arithmetically (i −= 1), not geometrically.\n\n"
                "**Tip:** whenever inner work forms a geometric series, the total is dominated by the "
                "largest term (this is also why bottom-up build-heap is O(n))."
            ),
            "verify": '''
for n in (1, 7, 100, 1000, 4096, 9999):
    assert n <= f(n) < 2 * n
assert f(100) == 197 and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — linear probing cost",
            "text": ("The keys 42, 17, 64, 31, 75, 53, 20, 86 are inserted, in this order, into an initially "
                     "empty hash table with 11 slots using h(k) = k mod 11 and linear probing "
                     "(h(k), h(k)+1, … mod 11). Counting every slot examined (including the slot finally "
                     "used) as one probe, the total number of probes for all 8 insertions is"),
            "options": ["22", "28", "36", "29"],
            "answer": "D",
            "solution": (
                "Hash values: 42→9, 17→6, 64→9, 31→9, 75→9, 53→9, 20→9, 86→9 — seven of the eight keys "
                "collide at slot 9, the worst case for linear probing.\n\n"
                "- 42: slot 9 → 1 probe.\n"
                "- 17: slot 6 → 1 probe.\n"
                "- 64: 9, **10** → 2.\n"
                "- 31: 9, 10, **0** (wrap) → 3.\n"
                "- 75: 9, 10, 0, **1** → 4.\n"
                "- 53: 9, 10, 0, 1, **2** → 5.\n"
                "- 20: 9 … 2, **3** → 6.\n"
                "- 86: 9 … 3, **4** → 7.\n\n"
                "Total = 1 + 1 + 2 + 3 + 4 + 5 + 6 + 7 = **29** → option (D).\n\n"
                "- (A) 22 = 29 − 7 omits the final (successful) probe of the seven keys hashing to 9.\n"
                "- (B) 28 counts only the colliding keys 1 + 2 + … + 7.\n"
                "- (C) 36 = 1 + 2 + … + 8 treats 17 as a colliding key too.\n\n"
                "**Insight:** k keys with the same home slot cost 1 + 2 + … + k = Θ(k²) probes in total, "
                "which is why a bad hash function turns hashing into Θ(n²)."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 31, 1: 75, 2: 53, 3: 20, 4: 86, 6: 17, 9: 42, 10: 64},
                                   "caption": "Final table — one long cluster 9, 10, 0, 1, 2, 3, 4"}],
            "verify": '''
T = [None] * 11; tot = 0
for k in [42, 17, 64, 31, 75, 53, 20, 86]:
    i = k % 11; tot += 1
    while T[i] is not None: i = (i + 1) % 11; tot += 1
    T[i] = k
opts = {'A': 22, 'B': 28, 'C': 36, 'D': 29}
assert [x for x in opts if opts[x] == tot] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Linked lists — operation costs",
            "text": ("A singly linked list of n nodes keeps a `head` pointer and a `tail` pointer (as shown). "
                     "Each node stores only its key and a `next` pointer, and no other auxiliary information "
                     "is kept. Which of the following operations requires Θ(n) time in the worst case?"),
            "diagrams": [{"type": "linkedlist", "values": [12, 7, 33, 5, 18], "head": "head", "tail": "tail",
                          "caption": "Singly linked list with head and tail pointers"}],
            "options": ["Inserting a new node before the first node",
                        "Inserting a new node after the last node",
                        "Deleting the first node",
                        "Deleting the last node"],
            "answer": "D",
            "solution": (
                "An operation is O(1) only if every pointer it must change is reachable in O(1) steps.\n\n"
                "- (A) Insert at front: `new.next = head; head = new` → O(1).\n"
                "- (B) Insert at end: `tail.next = new; tail = new` → O(1) thanks to the tail pointer.\n"
                "- (C) Delete first: `head = head.next` → O(1).\n"
                "- (D) Delete last: we must set the **predecessor** of the tail (node 5 in the figure) to "
                "have `next = None` and make it the new tail. A singly linked list has no back pointers, "
                "so finding that predecessor requires walking from head: n − 2 steps → **Θ(n)**.\n\n"
                "Answer (D).\n\n"
                "**Consequence:** a singly linked list with head and tail pointers is an ideal *queue* "
                "(enqueue at tail, dequeue at head, both O(1)), but deleting from the tail needs a doubly "
                "linked list.\n\n"
                "**Trap:** the tail pointer gives access to the last node, not to the node *before* it."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": [12, 7, 33, 5], "head": "head",
                                   "tail": "tail",
                                   "caption": "After deleting 18: the walk to node 5 costs Θ(n)"}],
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Heaps — nodes by height",
            "text": ("A binary heap is stored in an array of n = 1000 elements (a complete binary tree). The "
                     "*height* of a node is the number of edges on the longest downward path from it to a leaf "
                     "(leaves have height 0). The number of nodes of height exactly 3 is ______."),
            "answer": "63",
            "solution": (
                "In a heap with n nodes, node i (0-based) is a leaf iff i ≥ ⌊n/2⌋. Grouping levels from "
                "the bottom, a heap has **at most** ⌈n / 2^{h+1}⌉ nodes of height h (the classic "
                "build-heap bound); we count them exactly.\n\n"
                "Direct count for n = 1000:\n\n"
                "- height 0 (leaves): indices 500 … 999 → 500 nodes.\n"
                "- height 1: parents of leaves only, indices 250 … 499 → 250 (node 499 has one child).\n"
                "- height 2: indices 125 … 249 → 125.\n"
                "- height 3: indices 62 … 124 → **63**. Node 62 lies one level above 63 … 124, but its "
                "would-be descendants on the last level (from index 1007) do not exist, so its height is "
                "also 3; node 61 reaches index 991 and has height 4.\n\n"
                "Here the bound ⌈1000 / 16⌉ = ⌈62.5⌉ = 63 is attained exactly.\n\n"
                "This count drives the O(n) bound for build-heap: a node of height h costs O(h) to sift "
                "down, and ∑ h · ⌈n/2^{h+1}⌉ = O(n).\n\n"
                "**Trap:** using depth (distance from the root) instead of height: depth 3 has exactly "
                "8 nodes."
            ),
            "verify": '''
n = 1000; h = [0] * n
for i in range(n - 1, -1, -1):
    l = 2 * i + 1
    if l < n: h[i] = 1 + max(h[l], h[l + 1] if l + 1 < n else -1)
assert h.count(3) == int(ANSWER) == -(-n // 16)
assert [i for i in range(n) if h[i] == 3][0] == 62
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MSQ", "marks": 1, "topic": "Python — cost of built-in operations",
            "text": ("Let `data` be a list of n integers, many of which may be distinct. Which of the following "
                     "fragments run(s) in **Θ(n)** expected (average-case) time for every such list?"),
            "code": '''# (A)
s = set()
for x in data:
    if x not in s:
        s.add(x)
# (B)
out = []
for x in data:
    out.insert(0, x)
# (C)
seen = []
for x in data:
    if x not in seen:
        seen.append(x)
# (D)
d = {}
for x in data:
    d[x] = d.get(x, 0) + 1''',
            "options": ["Fragment (A)", "Fragment (B)", "Fragment (C)", "Fragment (D)"],
            "answer": ["A", "D"],
            "solution": (
                "Each fragment loops n times, so the question is the cost of the operation inside.\n\n"
                "- (A) `x not in s` and `s.add(x)` on a hash set are O(1) expected → total Θ(n). **Yes.**\n"
                "- (B) `list.insert(0, x)` shifts every existing element one place right: the k-th insert "
                "costs Θ(k), total 0 + 1 + … + (n − 1) = Θ(n²). **No.** "
                "(`collections.deque.appendleft` would be O(1).)\n"
                "- (C) `x not in seen` is a **linear search** of a list. If all values are distinct, the "
                "k-th test scans k elements → Θ(n²). **No.**\n"
                "- (D) `d.get` and `d[x] = …` are O(1) expected dict operations → Θ(n). **Yes.**\n\n"
                "Answer: (A) and (D).\n\n"
                "**Trap:** the expression `x in container` looks identical for lists and sets, but costs "
                "Θ(len) for a list and O(1) on average for a set or dict. Choosing the right container "
                "changes the asymptotic complexity of the whole algorithm."
            ),
            "run_code": False,
            "verify": '''
# model the element-level work of each fragment on n distinct values
def work(n):
    A = n                                 # one O(1) hash probe per element
    B = sum(k for k in range(n))          # insert(0, x) shifts k items
    C = sum(k for k in range(n))          # 'in' scans all k earlier items
    D = n
    return A, B, C, D
w1, w2 = work(1000), work(2000)
lin = ['ABCD'[i] for i in range(4) if w2[i] / w1[i] < 2.1]
assert lin == sorted(ANSWER)
data = list(range(500))
out = []
for x in data: out.insert(0, x)
assert out == data[::-1]
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Recurrence from recursive code",
            "text": ("Consider the following Python function. Which of the following best describes its "
                     "running time T(n) for n a power of 2?"),
            "code": '''def g(n):
    if n <= 1:
        return 1
    s = 0
    for i in range(n):
        s += i
    return g(n // 2) + g(n // 2) + g(n // 2) + s''',
            "options": ["Θ(n^{log₂3})", "Θ(n log n)", "Θ(n^{1.5})", "Θ(n²)"],
            "answer": "A",
            "solution": (
                "Translate the code into a recurrence: each call does Θ(n) work in the loop and makes "
                "**three** recursive calls on n/2 (the three `g(n // 2)` calls are evaluated separately — "
                "Python does not cache them).\n\n"
                "T(n) = 3T(n/2) + Θ(n).\n\n"
                "Master theorem: a = 3, b = 2, n^{log_b a} = n^{log₂3} ≈ n^{1.585}. Since "
                "f(n) = n = O(n^{1.585 − ε}), case 1 applies → T(n) = **Θ(n^{log₂3})**.\n\n"
                "Recursion-tree check (n = 2ᵏ): level i has 3ⁱ calls each doing n/2ⁱ work → cost "
                "n(3/2)ⁱ. The series grows geometrically, so the bottom level dominates: "
                "∑ n(3/2)ⁱ for i = 0 … k−1 equals 2(3ᵏ − 2ᵏ) = Θ(3ᵏ) = Θ(n^{log₂3}).\n\n"
                "- (B) would be the answer with **two** recursive calls (merge-sort shape).\n"
                "- (C) n^{1.5} is close numerically but log₂3 ≈ 1.585 > 1.5, and exponents that differ give "
                "different Θ classes.\n"
                "- (D) n² would need four calls of size n/2 (4T(n/2) + n).\n\n"
                "**Trap:** writing `3 * g(n // 2)` instead would make it T(n) = T(n/2) + n = Θ(n). "
                "The number of *calls*, not the arithmetic, determines a."
            ),
            "verify": '''
import math
cnt = [0]
def gc(n):
    if n <= 1: return 1
    s = 0
    for i in range(n): s += i; cnt[0] += 1
    return gc(n//2) + gc(n//2) + gc(n//2) + s
for k in (8, 10, 12):
    cnt[0] = 0; gc(2**k)
    assert cnt[0] == 2 * (3**k - 2**k)
    assert gc(2**k) == g(2**k)
r = [2 * (3**k - 2**k) / (2**k) ** math.log2(3) for k in (12, 20)]
assert abs(r[1] - r[0]) < 0.02 and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Loop counting — triple nested dependent loops",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''n = 12
c = 0
for i in range(n):
    for j in range(i, n):
        for k in range(i, j):
            c += 1
print(c)''',
            "answer": "286",
            "solution": (
                "Count the triples directly. For fixed i and j (i ≤ j ≤ n − 1) the innermost loop runs "
                "j − i times. Put d = j − i, which ranges over 0 … n − 1 − i:\n\n"
                "c = ∑ over i of (0 + 1 + … + (n − 1 − i)) = ∑ over i of (n − i)(n − i − 1)/2.\n\n"
                "Substituting m = n − i (m = 1 … n): c = ∑ m(m − 1)/2 = ∑ C(m, 2) = C(n + 1, 3) "
                "(hockey-stick identity).\n\n"
                "For n = 12: C(13, 3) = 13 · 12 · 11 / 6 = **286**.\n\n"
                "Combinatorial view: each increment corresponds to a choice i ≤ k < j ≤ n − 1 — "
                "equivalently three distinct values from {0, 1, …, 12} after shifting j by 1 — hence "
                "C(13, 3).\n\n"
                "Partial sums for a check: m = 1 … 12 contribute 0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, "
                "which add up to 286.\n\n"
                "Asymptotically the fragment is Θ(n³) with constant 1/6.\n\n"
                "**Trap:** using C(n, 3) = 220 (forgetting that k ranges up to j − 1 while j can reach n − 1, "
                "which adds one value) or n³/6 = 288 (only the leading term)."
            ),
            "verify": "assert int(OUTPUT) == int(ANSWER) == 286",
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Asymptotic notation — true/false statements",
            "text": "Which of the following statements is/are TRUE?",
            "options": ["n log₂ n = O(n^{1.01})",
                        "2^{n+1} = O(2ⁿ)",
                        "(n + 1)! = O(n!)",
                        "log₂(n!) = Θ(n log₂ n)"],
            "answer": ["A", "B", "D"],
            "solution": (
                "f = O(g) iff f(n)/g(n) stays bounded as n → ∞.\n\n"
                "- (A) (n log n) / n^{1.01} = log n / n^{0.01}. Any positive power of n eventually beats "
                "any power of log n, so the ratio → 0. **True** — although the crossover is enormous "
                "(log₂ n must exceed ≈ 1000, i.e. n > 2^{1000}).\n"
                "- (B) 2^{n+1} / 2ⁿ = 2, a constant. **True.**\n"
                "- (C) (n + 1)! / n! = n + 1 → ∞, unbounded. **False.**\n"
                "- (D) log(n!) = ∑ log i ≤ n log n; and the top half of the terms are each ≥ log(n/2), "
                "so log(n!) ≥ (n/2) log(n/2) = Ω(n log n). Hence Θ(n log n) (Stirling gives "
                "n log₂ n − 1.44n + O(log n)). **True.**\n\n"
                "Answer: (A), (B), (D).\n\n"
                "**Contrast:** 2^{2n} = 4ⁿ is *not* O(2ⁿ) — a constant *factor* in the exponent changes "
                "the class, while a constant *added* to the exponent (B) does not. Similarly "
                "(n + 1)! differs from n! by a factor that grows with n.\n\n"
                "**Trap:** concluding (A) is false from small-n tables — at n = 10⁶, n log n is far bigger "
                "than n^{1.01}, but O-notation concerns the limit."
            ),
            "verify": '''
import math
def lg_ratio_A(L): return (L + math.log2(L)) - 1.01 * L      # log2 of (n log n / n^1.01)
assert lg_ratio_A(1e5) < lg_ratio_A(1e4) < 0
assert 2 ** 51 / 2 ** 50 == 2
assert math.factorial(201) / math.factorial(200) == 201
for n in (10**4, 10**6):
    r = (math.lgamma(n + 1) / math.log(2)) / (n * math.log2(n))
    assert 0.85 < r < 1
assert sorted(ANSWER) == ['A', 'B', 'D']
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Recurrences — exact solution (merge sort worst case)",
            "text": ("The worst-case number of comparisons of top-down merge sort satisfies\n\n"
                     "T(1) = 0,   T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + n − 1  for n ≥ 2.\n\n"
                     "The value of T(100) is ______."),
            "answer": "573",
            "solution": (
                "Use the recursion tree level by level; at each level a sub-problem of size s contributes "
                "s − 1, so a level costs (sum of sizes) − (number of sub-problems of size ≥ 2).\n\n"
                "- Level 0: 100 → 99.\n"
                "- Level 1: 50, 50 → 98.\n"
                "- Level 2: four 25s → 96.\n"
                "- Level 3: four 12s and four 13s → 44 + 48 = 92.\n"
                "- Level 4: 12 → 6, 6 and 13 → 6, 7 — twelve 6s, four 7s → 60 + 24 = 84.\n"
                "- Level 5: 6 → 3, 3 and 7 → 3, 4 — twenty-eight 3s, four 4s → 56 + 12 = 68.\n"
                "- Level 6: 3 → 1, 2 and 4 → 2, 2 — thirty-six 2s → 36.\n"
                "- Level 7: 2 → 1, 1 — all size 1 → 0.\n\n"
                "T(100) = 99 + 98 + 96 + 92 + 84 + 68 + 36 = **573**.\n\n"
                "Closed form check: T(n) = n⌈log₂ n⌉ − 2^{⌈log₂ n⌉} + 1 = 100 · 7 − 128 + 1 = 573.\n\n"
                "**Trap:** using n log₂ n − n + 1 (valid only for powers of two) gives "
                "100 · 6.64 − 99 ≈ 565.4 — not even an integer."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Recursion tree, level by level",
                                   "row_labels": ["0", "1", "2", "3", "4", "5", "6"],
                                   "col_labels": ["sub-problem sizes", "level cost"],
                                   "rows": [["100", 99], ["50 ×2", 98], ["25 ×4", 96],
                                            ["12 ×4, 13 ×4", 92], ["6 ×12, 7 ×4", 84],
                                            ["3 ×28, 4 ×4", 68], ["1 ×28, 2 ×36", 36]]}],
            "verify": '''
import math
def T(n): return 0 if n <= 1 else T(n // 2) + T((n + 1) // 2) + n - 1
c = math.ceil(math.log2(100))
assert T(100) == int(ANSWER) == 100 * c - 2 ** c + 1
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MSQ", "marks": 2, "topic": "Queue via two stacks — amortised cost",
            "text": ("A queue is implemented with two stacks IN and OUT. `enqueue(x)` pushes x on IN. "
                     "`dequeue()` first checks OUT; **only if OUT is empty** it pops every element of IN and "
                     "pushes it on OUT; then it pops OUT and returns that value. Each push and each pop counts "
                     "as one stack operation (emptiness checks are free).\n\n"
                     "Starting empty, the following sequence is executed:\n"
                     "enqueue 1, 2, 3, 4, 5; dequeue; dequeue; enqueue 6, 7; dequeue × 4; enqueue 8; dequeue.\n\n"
                     "Which of the following statements is/are TRUE?"),
            "options": ["The sequence performs 29 stack operations in total",
                        "The most expensive single dequeue performs 11 stack operations",
                        "The last dequeue returns 8",
                        "For **any** sequence of m queue operations starting from an empty queue, at most 4m "
                        "stack operations are performed"],
            "answer": ["A", "B", "D"],
            "solution": (
                "Every element is pushed on IN once, popped from IN at most once, pushed on OUT at most "
                "once and popped from OUT at most once → ≤ 4 stack operations per element over its life.\n\n"
                "**Trace** (cost in brackets):\n\n"
                "- enqueue 1–5 → IN = [1,2,3,4,5] (5).\n"
                "- dequeue: OUT empty → move 5 elements (10), pop 1 (1) → **11**; OUT = [5,4,3,2] (top 2).\n"
                "- dequeue → 2 (1).\n"
                "- enqueue 6, 7 → IN = [6,7] (2).\n"
                "- dequeue × 4: 3, 4, 5 (1 each = 3); the 4th finds OUT empty → move 6, 7 (4) + pop 6 (1) "
                "= 5 → total 8.\n"
                "- enqueue 8 (1); dequeue → OUT still holds 7 → returns **7** (1).\n\n"
                "Total = 5 + 11 + 1 + 2 + 8 + 1 + 1 = **29**.\n\n"
                "- (A) **True** — 29.\n"
                "- (B) **True** — the first dequeue costs 11; the transfer of 6, 7 costs only 5.\n"
                "- (C) **False** — FIFO order: 7 was enqueued before 8, so 7 comes out; 8 remains in IN.\n"
                "- (D) **True** — at most 4 operations per enqueued element and the number of enqueues "
                "is ≤ m, so the amortised cost per operation is O(1) even though a single dequeue can "
                "cost Θ(n).\n\n"
                "**Trap:** transferring IN → OUT on *every* dequeue (even when OUT is non-empty) breaks "
                "FIFO order and destroys the amortised bound."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Stack contents after each phase",
                                   "row_labels": ["enq 1–5", "deq (→1)", "deq (→2)", "enq 6,7",
                                                  "deq ×4 (→3,4,5,6)", "enq 8", "deq (→7)"],
                                   "col_labels": ["IN (bottom→top)", "OUT (bottom→top)", "cost"],
                                   "rows": [["1 2 3 4 5", "—", 5], ["—", "5 4 3 2", 11],
                                            ["—", "5 4 3", 1], ["6 7", "5 4 3", 2], ["—", "7", 8],
                                            ["8", "7", 1], ["8", "—", 1]]}],
            "verify": '''
import random
def run(ops):
    IN, OUT, c, outv, dc = [], [], 0, [], []
    for op in ops:
        if op[0] == 'e': IN.append(op[1]); c += 1
        else:
            k = 1
            if not OUT:
                while IN: OUT.append(IN.pop()); k += 2
            outv.append(OUT.pop()); c += k; dc.append(k)
    return c, outv, dc
seq = [('e', x) for x in range(1, 6)] + [('d',)] * 2 + [('e', 6), ('e', 7)] + [('d',)] * 4 \\
      + [('e', 8), ('d',)]
c, outv, dc = run(seq)
res = {'A': c == 29, 'B': max(dc) == 11, 'C': outv[-1] == 8, 'D': True}
for _ in range(300):
    ops, size = [], 0
    for _ in range(random.randint(1, 40)):
        if size and random.random() < 0.5: ops.append(('d',)); size -= 1
        else: ops.append(('e', 0)); size += 1
    res['D'] &= run(ops)[0] <= 4 * len(ops)
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "Dijkstra — counting distance updates",
            "text": ("Dijkstra's algorithm (with a priority queue supporting decrease-key) is run from source "
                     "**S** on the directed graph below. An *update* is any assignment that strictly lowers "
                     "a tentative distance d[v], including the first assignment of a finite value to a vertex "
                     "whose distance was ∞ (d[S] = 0 is the initialisation and is not counted). "
                     "The total number of updates is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E"],
                          "edges": [["S", "A", 4], ["S", "B", 9], ["A", "B", 3], ["A", "D", 12],
                                    ["B", "D", 7], ["B", "C", 4], ["C", "D", 2], ["D", "E", 1],
                                    ["C", "E", 6]],
                          "pos": {"S": [0, 1], "A": [1.5, 2], "B": [1.5, 0], "D": [3, 2], "C": [3, 0],
                                  "E": [4.5, 1]}}],
            "answer": "9",
            "solution": (
                "Each successful relaxation is one decrease-key (or insert) on the priority queue, so the "
                "number of updates measures the heap work: with a binary heap Dijkstra costs "
                "O((V + #updates) log V) ⊆ O((V + E) log V).\n\n"
                "- Extract S (0): A = 4 ✔, B = 9 ✔ → 2 updates.\n"
                "- Extract A (4): B = min(9, 4+3) = 7 ✔, D = 4+12 = 16 ✔ → 4.\n"
                "- Extract B (7): D = min(16, 7+7) = 14 ✔, C = 7+4 = 11 ✔ → 6.\n"
                "- Extract C (11): D = min(14, 11+2) = 13 ✔, E = 11+6 = 17 ✔ → 8.\n"
                "- Extract D (13): E = min(17, 13+1) = 14 ✔ → **9**.\n"
                "- Extract E (14): no outgoing edges.\n\n"
                "Final distances: A 4, B 7, C 11, D 13, E 14. D was improved three times (16 → 14 → 13) "
                "and E twice (17 → 14).\n\n"
                "Here *every* one of the 9 edges produced an update — the maximum possible, since an "
                "edge is relaxed exactly once (when its tail is extracted).\n\n"
                "**Trap:** counting only the *decrease-key* operations on vertices that already had a "
                "finite distance (B, D, D, E → 4) — the question counts first assignments as well."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Tentative distances after each extraction",
                                   "col_labels": ["A", "B", "C", "D", "E", "updates so far"],
                                   "row_labels": ["S", "A", "B", "C", "D"],
                                   "rows": [[4, 9, "∞", "∞", "∞", 2], [4, 7, "∞", 16, "∞", 4],
                                            [4, 7, 11, 14, "∞", 6], [4, 7, 11, 13, 17, 8],
                                            [4, 7, 11, 13, 14, 9]],
                                   "highlight": [[4, 4], [3, 3]]}],
            "verify": '''
import heapq
E = [("S","A",4),("S","B",9),("A","B",3),("A","D",12),("B","D",7),("B","C",4),
     ("C","D",2),("D","E",1),("C","E",6)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
INF = float('inf'); d = {v: INF for v in "SABCDE"}; d["S"] = 0
done = set(); upd = 0
while len(done) < 6:
    u = min((v for v in d if v not in done), key=lambda v: d[v]); done.add(u)
    for v, w in G.get(u, []):
        if v not in done and d[u] + w < d[v]: d[v] = d[u] + w; upd += 1
assert upd == int(ANSWER) and [d[v] for v in "ABCDE"] == [4, 7, 11, 13, 14]
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MCQ", "marks": 2, "topic": "Quicksort — comparison count on a skewed input",
            "text": ("Consider the following Python program (each call to `qs` on a list of length m ≥ 2 is "
                     "charged m − 1 comparisons, one per non-pivot element). What is printed?"),
            "code": '''comps = 0
def qs(a):
    global comps
    if len(a) <= 1:
        return a
    p = a[0]
    comps += len(a) - 1
    L = [x for x in a[1:] if x < p]
    R = [x for x in a[1:] if x >= p]
    return qs(L) + [p] + qs(R)

qs([5, 1, 2, 3, 4, 10, 9, 8, 7, 6])
print(comps)''',
            "options": ["`45`", "`21`", "`25`", "`24`"],
            "answer": "C",
            "solution": (
                "With the first element as pivot, a sorted (or reverse-sorted) sub-list produces the worst "
                "split (0 and m − 1). The first pivot 5 happens to be the median, but both halves are then "
                "already ordered, so each degenerates.\n\n"
                "- qs(10 elements), pivot 5 → 9 comparisons; L = [1, 2, 3, 4], R = [10, 9, 8, 7, 6].\n"
                "- Left: [1,2,3,4] → 3; [2,3,4] → 2; [3,4] → 1; [4] → 0. Subtotal 6.\n"
                "- Right: [10,9,8,7,6] pivot 10 → 4, L = [9,8,7,6]; then 3, 2, 1. Subtotal 10.\n\n"
                "Total = 9 + 6 + 10 = **25** → option (C).\n\n"
                "- (A) 45 = C(10, 2) is the cost if the whole list were sorted (pivot 1 first).\n"
                "- (B) 21 assumes balanced splits all the way down (≈ best case for n = 10 is 19–21).\n"
                "- (D) 24 forgets one comparison, e.g. charges m − 2 for the root call.\n\n"
                "**Insight:** a good first split is not enough — quicksort's cost depends on every level. "
                "In general a sub-list of size m that is already sorted costs m(m − 1)/2: here "
                "9 + C(4, 2) + C(5, 2) = 9 + 6 + 10.\n\n"
                "**Trap:** the `x >= p` in R keeps equal keys on the right; with all-equal input this also "
                "gives Θ(n²)."
            ),
            "solution_diagrams": [{"type": "tree", "root": "5 (9)",
                                   "children": {"5 (9)": ["1 (3)", "10 (4)"], "1 (3)": ["2 (2)"],
                                                "2 (2)": ["3 (1)"], "3 (1)": ["4"],
                                                "10 (4)": ["9 (3)"], "9 (3)": ["8 (2)"],
                                                "8 (2)": ["7 (1)"], "7 (1)": ["6"]},
                                   "caption": "Pivot tree: node = pivot (comparisons charged)"}],
            "verify": '''
assert int(OUTPUT) == 25
opts = {'A': 45, 'B': 21, 'C': 25, 'D': 24}
assert [k for k in opts if opts[k] == int(OUTPUT)] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MSQ", "marks": 2, "topic": "Heaps — complexity facts with numbers",
            "text": ("All heaps below are binary min-heaps stored in arrays (root at index 0) holding "
                     "**distinct** keys. Which of the following statements is/are TRUE?"),
            "options": [
                "Bottom-up build-heap on 1000 keys never performs more than 994 swaps",
                "The maximum key of a min-heap with n keys can always be found with O(log n) comparisons",
                "The k smallest of n keys can be output in sorted order in O(n + k log n) time using a heap",
                "In a min-heap with 1000 keys the second-smallest key is always at index 1 or index 2",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "- (A) **True.** Sifting down a node of height h costs at most h swaps. For n = 1000 the "
                "numbers of nodes of heights 1 … 9 are 250, 125, 63, 31, 16, 8, 4, 2, 1, so the worst case "
                "is 1·250 + 2·125 + 3·63 + 4·31 + 5·16 + 6·8 + 7·4 + 8·2 + 9·1 = 250 + 250 + 189 + 124 + "
                "80 + 48 + 28 + 16 + 9 = 994 < n — the concrete form of the O(n) bound.\n"
                "- (B) **False.** The maximum can be any of the ⌈n/2⌉ leaves (heap order says nothing "
                "about leaves relative to each other), so Θ(n) comparisons are needed.\n"
                "- (C) **True.** Build-heap O(n), then k extract-min operations O(k log n).\n"
                "- (D) **True.** The second-smallest key's parent must be smaller than it, so the parent is "
                "the minimum, i.e. the root; the root's children are indices 1 and 2.\n\n"
                "Answer: (A), (C), (D).\n\n"
                "**Trap for (B):** confusing ‘the max is at a leaf’ (true) with ‘the max is at the last "
                "index’ or ‘on the rightmost path’ (both false)."
            ),
            "verify": '''
import random
n = 1000; h = [0] * n
for i in range(n - 1, -1, -1):
    l = 2 * i + 1
    if l < n: h[i] = 1 + max(h[l], h[l + 1] if l + 1 < n else -1)
assert sum(h) == 994
def build(a):
    sw = 0
    for i in range(len(a) // 2 - 1, -1, -1):
        j = i
        while True:
            l, r, s = 2*j+1, 2*j+2, j
            if l < len(a) and a[l] < a[s]: s = l
            if r < len(a) and a[r] < a[s]: s = r
            if s == j: break
            a[j], a[s] = a[s], a[j]; j = s; sw += 1
    return sw
okA = okD = True; leafmax = False
for _ in range(60):
    a = random.sample(range(10**6), n)
    okA &= build(a) <= 994
    okD &= sorted(a)[1] in (a[1], a[2])
    leafmax |= a.index(max(a)) != n - 1
assert build(list(range(n, 0, -1))) <= 994
assert okA and okD and leafmax and sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "NAT", "marks": 2, "topic": "Recursion — counting calls",
            "text": "Consider the following Python program. The **second** number printed is ______.",
            "code": '''calls = 0
def f(n):
    global calls
    calls += 1
    if n < 3:
        return n
    return f(n - 1) + f(n - 3)

v = f(12)
print(v, calls)''',
            "answer": "119",
            "solution": (
                "Let C(n) be the number of calls made by f(n) (including itself). Then\n\n"
                "C(n) = 1 for n ≤ 2 and C(n) = 1 + C(n − 1) + C(n − 3) for n ≥ 3.\n\n"
                "Tabulate:\n\n"
                "- C(0) = C(1) = C(2) = 1\n"
                "- C(3) = 1 + 1 + 1 = 3; C(4) = 1 + 3 + 1 = 5; C(5) = 1 + 5 + 1 = 7\n"
                "- C(6) = 1 + 7 + 3 = 11; C(7) = 1 + 11 + 5 = 17; C(8) = 1 + 17 + 7 = 25\n"
                "- C(9) = 1 + 25 + 11 = 37; C(10) = 1 + 37 + 17 = 55; C(11) = 1 + 55 + 25 = 81\n"
                "- C(12) = 1 + 81 + 37 = **119**\n\n"
                "(The first number printed is f(12) = 69, from F(n) = F(n−1) + F(n−3) with "
                "F(0..2) = 0, 1, 2.)\n\n"
                "Growth: C(n) ≈ c·ρⁿ where ρ ≈ 1.4656 is the real root of x³ = x² + 1, so the naive "
                "recursion is exponential; memoising f reduces it to n + 1 distinct calls, i.e. Θ(n).\n\n"
                "**Trap:** using the value recurrence for the call count (69), or dropping the ‘+1’ "
                "for the call itself — that recurrence counts only the base-case (leaf) calls, 60. "
                "Since every internal call has exactly two children, calls = 2 × 60 − 1 = 119."
            ),
            "verify": "assert OUTPUT.split() == ['69', '119'] and int(ANSWER) == calls",
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MCQ", "marks": 2, "topic": "Recurrences — change of variable",
            "text": ("Let W(n) be the value of `steps` after the call `r(n)` (starting from `steps = 0`). "
                     "Which of the following is W(n) for large n?"),
            "code": '''from math import isqrt
steps = 0
def r(n):
    global steps
    if n <= 2:
        return
    i = 1
    while i < n:
        i *= 2
        steps += 1
    r(isqrt(n))
    r(isqrt(n))''',
            "options": ["Θ(log n)", "Θ(log n · log log n)", "Θ(log² n)", "Θ(√n)"],
            "answer": "B",
            "solution": (
                "The while-loop doubles i until it reaches n: ⌈log₂ n⌉ iterations. Then two recursive calls "
                "on √n. So\n\n"
                "W(n) = 2W(√n) + Θ(log n).\n\n"
                "**Change of variable:** put m = log₂ n, so √n = 2^{m/2}, and let S(m) = W(2^m):\n\n"
                "S(m) = 2S(m/2) + Θ(m).\n\n"
                "This is the merge-sort recurrence → S(m) = Θ(m log m). Returning to n: "
                "W(n) = **Θ(log n · log log n)** → option (B).\n\n"
                "Check with n = 2^{16}: level 0: 16 steps; level 1: 2 calls on 2⁸ → 2·8; level 2: 4 calls "
                "on 2⁴ → 4·4; level 3: 8 calls on 4 → 8·2; then n = 2 stops. Total "
                "16 + 16 + 16 + 16 = 64 = m log₂ m with m = 16.\n\n"
                "- (A) ignores the doubling of calls at each level (that would be W = W(√n) + log n).\n"
                "- (C) multiplies log n by the wrong depth (log n instead of log log n levels).\n"
                "- (D) confuses the argument √n with the cost.\n\n"
                "**Trap:** the recursion depth is log log n, not log n — taking square roots shrinks n far "
                "faster than halving."
            ),
            "verify": '''
import math
def W(e):
    global steps
    steps = 0; r(2 ** e); return steps
assert W(16) == 64
vals = {e: W(e) / (e * math.log2(e)) for e in (32, 64, 128)}
assert all(0.9 < v < 1.1 for v in vals.values())
assert W(128) / W(64) > 2.1 and ANSWER == 'B'
''',
        },
    ],
}
