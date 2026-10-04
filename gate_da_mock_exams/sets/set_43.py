# Set 43 — Full-Syllabus Mock — Paper 13
SET = {
    "number": 43,
    "title": "Full-Syllabus Mock — Paper 13",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — shallow vs deep copy",
            "text": "Consider the following Python program. What is printed?",
            "code": '''import copy
a = [[1, 2], [3]]
b = a[:]
c = copy.deepcopy(a)
b[0].append(9)
b.append([7])
c[1].append(8)
print(a, len(b), c[1])''',
            "options": ["`[[1, 2, 9], [3]] 3 [3, 8]`", "`[[1, 2], [3]] 3 [3, 8]`",
                        "`[[1, 2, 9], [3], [7]] 3 [3, 8]`", "`[[1, 2, 9], [3, 8]] 3 [3, 8]`"],
            "answer": "A",
            "solution": (
                "`a[:]` makes a **shallow** copy: a new outer list whose elements are the *same* inner list "
                "objects. `deepcopy` copies the inner lists too.\n\n"
                "- `b[0].append(9)` mutates the inner list shared by a and b → a[0] = [1, 2, 9].\n"
                "- `b.append([7])` changes only b's outer list → len(b) = 3, a still has 2 elements.\n"
                "- `c[1].append(8)` mutates c's private copy of [3] → c[1] = [3, 8]; a[1] stays [3].\n\n"
                "Output: **[[1, 2, 9], [3]] 3 [3, 8]**.\n\n"
                "- (B) treats the slice as a deep copy.\n"
                "- (C) thinks appending to b's outer list also affects a.\n"
                "- (D) thinks deepcopy still shares inner lists with a.\n\n"
                "**Trap:** 'copy' in Python usually means one level deep. **Tip:** `list(a)`, `a.copy()` and "
                "`a[:]` are all shallow."
            ),
            "verify": "assert OUTPUT.strip() == '[[1, 2, 9], [3]] 3 [3, 8]' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — string slicing and searching",
            "text": ("Let `s = \"datascience\"`. The value of "
                     "`len(set(s[::2])) + s.find('c') + s.rfind('e')` is ______."),
            "answer": "21",
            "solution": (
                "Index the string: d0 a1 t2 a3 s4 c5 i6 e7 n8 c9 e10.\n\n"
                "- `s[::2]` takes indices 0, 2, 4, 6, 8, 10 → \"dtsine\"; all six characters are distinct → "
                "`len(set(...))` = **6**.\n"
                "- `s.find('c')` = first occurrence of 'c' = **5**.\n"
                "- `s.rfind('e')` = last occurrence of 'e' = **10**.\n\n"
                "Sum = 6 + 5 + 10 = **21**.\n\n"
                "**Traps:** taking `s[::2]` as starting from index 1, using 1-based indices (giving 6 + 6 + 11 "
                "= 23), or confusing `rfind` with 'find from the right and count from the right'. `rfind` "
                "returns an ordinary left-based index."
            ),
            "verify": '''
s = "datascience"
assert s[::2] == "dtsine" and len(set(s[::2])) + s.find('c') + s.rfind('e') == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "NAT", "marks": 1, "topic": "Stacks — counting pop sequences",
            "text": ("The integers 1, 2, 3, 4, 5 are pushed onto an initially empty stack in this order; pops may "
                     "occur at any time and every popped value is printed, until all five are printed. "
                     "The number of possible printed sequences whose **first** value is 3 is ______."),
            "answer": "9",
            "solution": (
                "To print 3 first we must push 1, 2, 3 and pop 3. The state is now: stack [1, 2] (2 on top), "
                "inputs 4, 5 still to come. Count the completions.\n\n"
                "Let N(i, s) = number of ways to finish with i inputs left and s items on the stack. "
                "N(0, s) = 1 (just pop everything); N(i, 0) = N(i − 1, 1); otherwise "
                "N(i, s) = N(i − 1, s + 1) [push] + N(i, s − 1) [pop].\n\n"
                "- N(1, 0) = 1, N(1, 1) = 2, N(1, 2) = 3, N(1, 3) = 4\n"
                "- N(2, 0) = N(1, 1) = 2\n"
                "- N(2, 1) = N(1, 2) + N(2, 0) = 3 + 2 = 5\n"
                "- N(2, 2) = N(1, 3) + N(2, 1) = 4 + 5 = **9**\n\n"
                "For instance 3 2 1 4 5, 3 2 4 1 5, 3 4 5 2 1, 3 5 4 2 1, … — in all of them 2 precedes 1.\n\n"
                "**Trap:** counting all orders of the remaining four values with 2 before 1 (12) — this also "
                "admits impossible ones such as 3 5 2 4 1 (popping 5 traps 4 above 2). Of all 42 = C₅ "
                "stack permutations of 1…5, exactly 9 start with 3."
            ),
            "verify": '''
res = []
def rec(i, st, out):
    if len(out) == 5: res.append(tuple(out)); return
    if i <= 5: rec(i + 1, st + [i], out)
    if st: rec(i, st[:-1], out + [st[-1]])
rec(1, [], [])
assert len(res) == 42 and sum(p[0] == 3 for p in res) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Queue as a circular linked list",
            "text": ("A queue is stored in a **circular** singly linked list, and only a pointer `tail` to the last "
                     "(rear) node is kept; `tail.next` is the front node. Which of the following operations can "
                     "be performed in Θ(1) worst-case time on a queue of n elements?"),
            "diagrams": [{"type": "linkedlist", "values": ["f", "x", "y", "r"], "circular": True,
                          "head": "tail.next", "caption": "front f … rear r; tail points to r"}],
            "options": [
                "Enqueue a new element at the rear",
                "Dequeue the front element",
                "Read the value of the front element",
                "Delete the rear element (the node pointed to by tail)",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "With a circular list one pointer to the rear gives access to **both** ends: rear = tail, "
                "front = tail.next.\n\n"
                "- (A) new node z: z.next = tail.next; tail.next = z; tail = z. Θ(1). **True.**\n"
                "- (B) f = tail.next; tail.next = f.next (if f is the only node, set tail = None). Θ(1). "
                "**True.**\n"
                "- (C) tail.next.val. Θ(1). **True.**\n"
                "- (D) removing tail requires its **predecessor** (to become the new tail), which can only be "
                "found by walking around the circle: Θ(n). **False.**\n\n"
                "**Trap:** keeping a pointer to the *front* instead would make enqueue Θ(n), because reaching "
                "the rear needs a full traversal. **Tip:** this is why queues built on circular lists keep "
                "the rear pointer."
            ),
            "verify": '''
class Nd:
    def __init__(s, v): s.v, s.next = v, None
tail = None; ops = 0
def enq(v):
    global tail
    z = Nd(v)
    if tail is None: z.next = z
    else: z.next = tail.next; tail.next = z
    tail = z
def deq():
    global tail
    f = tail.next
    if f is tail: tail = None
    else: tail.next = f.next
    return f.v
for v in range(1, 6): enq(v)
assert deq() == 1 and tail.next.v == 2 and deq() == 2
enq(6); out = []
while tail: out.append(deq())
assert out == [3, 4, 5, 6] and sorted(ANSWER) == ["A", "B", "C"]
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Counting BSTs with a fixed root",
            "text": ("The number of structurally distinct binary search trees that can store the keys "
                     "1, 2, 3, 4, 5 and have the key **3** at the root is ______."),
            "answer": "4",
            "solution": (
                "If 3 is the root, the left subtree is a BST on {1, 2} and the right subtree is a BST on "
                "{4, 5}, chosen independently.\n\n"
                "- Number of BSTs on 2 keys = Catalan C₂ = 2 (smaller key as root with right child, or larger "
                "key as root with left child).\n"
                "- Total = 2 × 2 = **4**.\n\n"
                "General formula: the number of BSTs on keys 1…n with root r is C_{r−1} · C_{n−r}. "
                "Summing over r gives the Catalan number C₅ = 1·14 + 1·5 + 2·2 + 5·1 + 14·1 = 42.\n\n"
                "**Trap:** answering C₅ = 42 (ignoring the root constraint) or 2 + 2 = 4 by luck with the "
                "wrong rule — the subtrees combine by **multiplication**, not addition."
            ),
            "solution_diagrams": [{"type": "bintree", "tree": [3, [1, None, [2]], [5, [4], None]],
                                   "caption": "One of the 4 trees"}],
            "verify": '''
def trees(keys):
    if not keys: return [None]
    out = []
    for i, r in enumerate(keys):
        for L in trees(keys[:i]):
            for R in trees(keys[i + 1:]): out.append((r, L, R))
    return out
T = trees([1, 2, 3, 4, 5])
assert len(T) == 42 and sum(t[0] == 3 for t in T) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Hash functions for strings",
            "text": ("Strings are hashed into a table of size 11 by h(s) = (sum of the character codes of s) mod 11. "
                     "Which of the following strings is **certain** to land in the same slot as \"listen\", "
                     "without computing any character codes?"),
            "options": ["\"tinsel\"", "\"lister\"", "\"listens\"", "\"silence\""],
            "answer": "A",
            "solution": (
                "A sum of character codes ignores **order**, so any rearrangement (anagram) of a string has the "
                "same sum and therefore the same hash value.\n\n"
                "- (A) \"tinsel\" uses exactly the letters l, i, s, t, e, n → identical sum → **same slot, "
                "guaranteed**.\n"
                "- (B) \"lister\" replaces n by r — a different sum (differs by ord('r') − ord('n') = 4), "
                "so a different slot.\n"
                "- (C) \"listens\" adds an 's' (code 115 ≡ 5 mod 11) → shifts the slot by 5.\n"
                "- (D) \"silence\" is not an anagram (extra c and e); its slot cannot be predicted without "
                "computing.\n\n"
                "(Indeed h(\"listen\") = h(\"tinsel\") = 6.)\n\n"
                "**Tip:** good string hashes are position-dependent, e.g. the polynomial hash "
                "Σ cᵢ·bⁱ mod m, which separates anagrams."
            ),
            "verify": '''
h = lambda s: sum(map(ord, s)) % 11
assert h("listen") == h("tinsel")
opts = ["tinsel", "lister", "listens", "silence"]
assert [c for c, o in zip("ABCD", opts) if sorted(o) == sorted("listen")] == [ANSWER]
assert h("lister") != h("listen") and h("listens") != h("listen")
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — average successful cost",
            "text": ("Iterative binary search (mid = ⌊(lo + hi)/2⌋, one three-way comparison per probe) is used "
                     "on a sorted array of 15 distinct elements. Each element is equally likely to be the "
                     "target, and the target is always present. The expected number of probes is"),
            "options": ["49/15", "4", "15/4", "3"],
            "answer": "A",
            "solution": (
                "The probes of binary search on 15 = 2⁴ − 1 elements form a perfectly balanced decision tree: "
                "level d (d = 1 … 4) contains 2^{d−1} elements, each found after exactly d probes.\n\n"
                "- 1 element (the middle, index 7) → 1 probe\n"
                "- 2 elements (indices 3, 11) → 2 probes\n"
                "- 4 elements → 3 probes\n"
                "- 8 elements → 4 probes\n\n"
                "Total = 1·1 + 2·2 + 4·3 + 8·4 = 1 + 4 + 12 + 32 = 49 → expected = **49/15 ≈ 3.27**.\n\n"
                "- (B) 4 is the **worst case** (and the cost of every unsuccessful search).\n"
                "- (C) 15/4 is a mis-weighted average.\n"
                "- (D) 3 = log₂ 8 is a rough guess.\n\n"
                "**Tip:** more than half of the elements sit on the deepest level, so the average is close to "
                "the worst case: about log₂ n − 1."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [7, [3, [1, [0], [2]], [5, [4], [6]]],
                                            [11, [9, [8], [10]], [13, [12], [14]]]],
                                   "caption": "Decision tree of indices probed"}],
            "verify": '''
A = list(range(15)); tot = 0
for x in A:
    lo, hi, k = 0, 14, 0
    while lo <= hi:
        m = (lo + hi) // 2; k += 1
        if A[m] == x: break
        if A[m] < x: lo = m + 1
        else: hi = m - 1
    tot += k
from fractions import Fraction
assert Fraction(tot, 15) == Fraction(49, 15) and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "NAT", "marks": 1, "topic": "Insertion sort — comparisons",
            "text": ("Insertion sort (ascending) is run on [4, 1, 3, 9, 7, 2]. For each i = 1, …, n − 1 the key A[i] "
                     "is compared with A[i−1], A[i−2], … moving left, shifting each larger element, and stopping "
                     "at the first element ≤ key or at the left end. The total number of key comparisons is "
                     "______."),
            "answer": "11",
            "solution": (
                "For each insertion: comparisons = (number of shifts) + 1, **unless** the key travels all the "
                "way to index 0 (then there is no final failing comparison).\n\n"
                "- i=1, key 1: 4 > 1 shift; reaches left end → 1 comparison → [1, 4, 3, 9, 7, 2]\n"
                "- i=2, key 3: 4 > 3 shift; 1 ≤ 3 stop → 2 → [1, 3, 4, 9, 7, 2]\n"
                "- i=3, key 9: 4 ≤ 9 stop → 1\n"
                "- i=4, key 7: 9 > 7 shift; 4 ≤ 7 stop → 2 → [1, 3, 4, 7, 9, 2]\n"
                "- i=5, key 2: 9, 7, 4, 3 shift; 1 ≤ 2 stop → 5 → [1, 2, 3, 4, 7, 9]\n\n"
                "Total = 1 + 2 + 1 + 2 + 5 = **11**.\n\n"
                "Check: shifts = inversions = 1 + 1 + 0 + 1 + 4 = 7; comparisons = 7 + (5 insertions − 1 that "
                "reached the left end) = 11.\n\n"
                "**Trap:** counting comparisons = shifts (7) or = shifts + n − 1 (12)."
            ),
            "verify": '''
A = [4, 1, 3, 9, 7, 2]; cmp = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0:
        cmp += 1
        if A[j] > key: A[j + 1] = A[j]; j -= 1
        else: break
    A[j + 1] = key
assert cmp == int(ANSWER) and A == sorted(A)
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MSQ", "marks": 1, "topic": "Degrees and Euler trails",
            "text": "Consider the undirected graph G below. Which of the following statements is/are TRUE?",
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F"],
                          "edges": [["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "E"], ["D", "E"],
                                    ["D", "F"], ["E", "F"], ["B", "E"]],
                          "pos": {"A": [0, 1], "B": [1.5, 2], "C": [1.5, 0], "D": [3.5, 2], "E": [3.5, 0],
                                  "F": [5, 1]}}],
            "options": [
                "G has an Euler trail (a walk using every edge exactly once) but no Euler circuit",
                "G has exactly two vertices of odd degree",
                "After deleting edge B–E, the resulting graph has an Euler circuit",
                "G is bipartite",
            ],
            "answer": ["A", "B"],
            "solution": (
                "Degrees: A 2, B 4 (A, C, D, E), C 3 (A, B, E), D 3 (B, E, F), E 4 (C, D, F, B), F 2. "
                "Sum = 18 = 2 × 9 edges. ✓\n\n"
                "Euler's theorem (connected graph): Euler circuit ⇔ all degrees even; Euler trail (not closed) "
                "⇔ exactly two odd-degree vertices, and the trail runs between them.\n\n"
                "- (B) odd vertices: C and D → exactly two. **True.**\n"
                "- (A) hence an Euler trail from C to D exists, but no circuit. **True.** "
                "(e.g. C-A-B-C-E-B-D-E-F-D)\n"
                "- (C) deleting B–E makes B and E odd too → four odd vertices → no Euler circuit (not even a "
                "trail). **False.**\n"
                "- (D) A–B–C is a triangle (odd cycle). **False.**\n\n"
                "**Tip:** adding the edge C–D instead would make every degree even and create an Euler circuit."
            ),
            "verify": '''
E = [("A","B"),("A","C"),("B","C"),("B","D"),("C","E"),("D","E"),("D","F"),("E","F"),("B","E")]
def degs(E):
    d = {}
    for a, b in E: d[a] = d.get(a, 0) + 1; d[b] = d.get(b, 0) + 1
    return d
odd = [v for v, k in degs(E).items() if k % 2]
E2 = [e for e in E if e != ("B", "E")]
odd2 = [v for v, k in degs(E2).items() if k % 2]
trail = "CABCEBDEFD"
used = sorted(tuple(sorted(p)) for p in zip(trail, trail[1:]))
assert used == sorted(tuple(sorted(e)) for e in E)
truth = [len(odd) == 2, len(odd) == 2, len(odd2) == 0, False]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Recurrences — master theorem",
            "text": "The solution of the recurrence T(n) = 2T(n/4) + √n, with T(1) = 1, is",
            "options": ["Θ(√n log n)", "Θ(√n)", "Θ(n)", "Θ(n^{1/4} log n)"],
            "answer": "A",
            "solution": (
                "Master theorem with a = 2, b = 4: n^{log_b a} = n^{log₄ 2} = n^{1/2} = √n. The driving term "
                "f(n) = √n is of the **same** order, so we are in case 2: T(n) = Θ(√n log n).\n\n"
                "Direct check with n = 4^{k} (√n = 2^{k}): T(4^{k}) = 2T(4^{k−1}) + 2^{k}. Dividing by 2^{k}: "
                "T(4^{k})/2^{k} = T(4^{k−1})/2^{k−1} + 1, so T(4^{k}) = 2^{k}(k + 1) = √n (log₄ n + 1).\n\n"
                "- (B) Θ(√n) would need f(n) polynomially smaller than √n (case 1).\n"
                "- (C) Θ(n) mistakes n^{log_b a} for n.\n"
                "- (D) n^{1/4} log n mistakes the critical exponent log₄ 2 = 1/2 for 1/4.\n\n"
                "**Trap:** each of the log₄ n levels of the recursion tree costs exactly √n — equal work per "
                "level is the signature of case 2."
            ),
            "verify": '''
import math
T = {1: 1}
for k in range(1, 12):
    n = 4 ** k; T[n] = 2 * T[n // 4] + int(math.isqrt(n))
    assert T[n] == 2 ** k * (k + 1)
assert ANSWER == "A"
''',
        },
    ],
}
