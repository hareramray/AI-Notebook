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
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — try / except / finally",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def f(x):
    try:
        if x > 0:
            return 'pos'
        raise ValueError
    except ValueError:
        return 'err'
    finally:
        print('F', end=' ')

def g():
    try:
        return 1
    finally:
        return 2

print(f(1), f(0), g())''',
            "options": ["`F F pos err 2`", "`pos F err F 1`", "`F pos F err 2`", "`F F pos err 1`"],
            "answer": "A",
            "solution": (
                "Two rules: (1) a `finally` block runs on **every** exit from the `try` statement, including "
                "`return`; (2) if `finally` itself executes `return`, that value replaces the pending one.\n\n"
                "The arguments of the outer `print` are evaluated left to right **before** it prints:\n\n"
                "- `f(1)`: `return 'pos'` is pending → finally prints `F ` → returns 'pos'.\n"
                "- `f(0)`: ValueError raised → caught → `return 'err'` pending → finally prints `F ` → "
                "returns 'err'.\n"
                "- `g()`: `return 1` pending → finally's `return 2` overrides → 2.\n"
                "- Finally the outer print writes `pos err 2` after the two `F ` already on the line.\n\n"
                "Output: **F F pos err 2**.\n\n"
                "- (B) assumes the outer print emits its values interleaved with the calls.\n"
                "- (C) assumes each value is printed as soon as its call returns.\n"
                "- (D) misses that `return` in `finally` overrides the earlier `return 1`.\n\n"
                "**Trap:** `return` inside `finally` also silently swallows exceptions — avoid it in real code."
            ),
            "verify": "assert OUTPUT.strip() == 'F F pos err 2' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Monotonic stack — next greater element",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def nge(a):
    st, res = [], [-1] * len(a)
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
        st.append(i)
    return res

print(sum(nge([5, 3, 8, 2, 4, 9, 1, 6])))''',
            "answer": "42",
            "solution": (
                "The stack holds indices of elements still waiting for a larger element to their right; their "
                "values are non-increasing from bottom to top. When x arrives, every smaller waiting element "
                "gets x as its *next greater element*.\n\n"
                "- 5: stack [5]\n"
                "- 3: stack [5, 3]\n"
                "- 8: pops 3 → 8, pops 5 → 8; stack [8]\n"
                "- 2: stack [8, 2]\n"
                "- 4: pops 2 → 4; stack [8, 4]\n"
                "- 9: pops 4 → 9, pops 8 → 9; stack [9]\n"
                "- 1: stack [9, 1]\n"
                "- 6: pops 1 → 6; stack [9, 6]\n\n"
                "Never popped: 9 and 6 → keep −1.\n\n"
                "res = [8, 8, 9, 4, 9, −1, 6, −1]; sum = 8 + 8 + 9 + 4 + 9 − 1 + 6 − 1 = **42**.\n\n"
                "**Traps:** forgetting the two −1 entries (sum 44), or taking the *first popped* order as the "
                "order of res. **Tip:** each index is pushed and popped at most once → Θ(n)."
            ),
            "solution_diagrams": [{"type": "array", "values": [8, 8, 9, 4, 9, -1, 6, -1], "label": "res",
                                   "highlight": [5, 7], "caption": "−1 marks elements with no greater element"}],
            "verify": '''
a = [5, 3, 8, 2, 4, 9, 1, 6]
brute = [next((y for y in a[i + 1:] if y > a[i]), -1) for i in range(len(a))]
assert nge(a) == brute and OUTPUT.strip() == ANSWER == str(sum(brute))
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Linked lists — Floyd's cycle detection",
            "text": ("A singly linked list has nodes with values 1, 2, …, 8 in order, but the `next` pointer of node 8 "
                     "points back to node 4 (so the list ends in a cycle). Floyd's algorithm is run: `slow` and "
                     "`fast` both start at node 1; in each iteration slow moves 1 step and fast moves 2 steps, "
                     "and the loop stops as soon as they are at the same node. Which of the following "
                     "statements is/are TRUE?"),
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7, 8], "head": "head",
                          "caption": "Node 8's next pointer goes back to node 4"}],
            "options": [
                "slow and fast first meet at node 6",
                "They first meet after exactly 4 iterations",
                "The cycle contains exactly 5 nodes",
                "If one pointer is then reset to node 1 and both advance one step at a time, they next meet "
                "at node 4 after 3 steps",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "Tail length μ = 3 (nodes 1, 2, 3 before the cycle), cycle length λ = 5 (nodes 4–8).\n\n"
                "Positions after each iteration (slow / fast):\n\n"
                "- 1: 2 / 3\n"
                "- 2: 3 / 5\n"
                "- 3: 4 / 7\n"
                "- 4: 5 / 4 (7 → 8 → 4)\n"
                "- 5: **6 / 6** → meet\n"
                "- (A) **True.**\n"
                "- (B) they meet after **5** iterations. **False.**\n"
                "- (C) 4 → 5 → 6 → 7 → 8 → 4: λ = 5. **True.**\n"
                "- (D) Phase 2: from node 1 and node 6, one step each: (2, 7), (3, 8), (4, 4) → meet at the "
                "cycle entrance, node 4, after μ = 3 steps. **True.**\n\n"
                "Why phase 2 works: at the meeting point slow has walked k steps and fast 2k, so k is a "
                "multiple of λ; walking μ more steps from the meeting point lands exactly on the entrance.\n\n"
                "**Trap:** assuming the meeting point is the cycle entrance — it generally is not."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Floyd trace (phase 1)",
                                   "col_labels": ["iter", "slow", "fast"],
                                   "rows": [[0, 1, 1], [1, 2, 3], [2, 3, 5], [3, 4, 7], [4, 5, 4], [5, 6, 6]],
                                   "highlight": [[5, 1], [5, 2]]}],
            "verify": '''
nxt = {i: i + 1 for i in range(1, 8)}; nxt[8] = 4
s = f = 1; it = 0
while True:
    s = nxt[s]; f = nxt[nxt[f]]; it += 1
    if s == f: break
p, q, k = 1, s, 0
while p != q: p = nxt[p]; q = nxt[q]; k += 1
lam, x = 1, nxt[4]
while x != 4: x = nxt[x]; lam += 1
truth = [s == 6, it == 4, lam == 5, p == 4 and k == 3]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Min-heap — extract-min and insert",
            "text": ("The array below is a binary min-heap (0-based). Two `extract-min` operations are performed "
                     "(move the last element to the root, then sift down swapping with the smaller child), "
                     "followed by `insert(1)` (append, then sift up). In the resulting heap, the sum of the keys "
                     "stored in the **leaves** is ______."),
            "diagrams": [{"type": "heap", "values": [2, 5, 3, 9, 6, 4, 8, 12, 10, 7], "caption": "Initial min-heap"}],
            "answer": "45",
            "solution": (
                "- Extract-min #1 (removes 2): 7 moves to the root → [7, 5, 3, 9, 6, 4, 8, 12, 10]; 7 vs "
                "children 5, 3 → swap with 3; at index 2 children 4, 8 → swap with 4 → "
                "[3, 5, 4, 9, 6, 7, 8, 12, 10].\n\n"
                "- Extract-min #2 (removes 3): 10 moves to the root → [10, 5, 4, 9, 6, 7, 8, 12]; swap with 4; at "
                "index 2 children 7, 8 → swap with 7 → [4, 5, 7, 9, 6, 10, 8, 12].\n"
                "- Insert 1 at index 8: parent index 3 (9) → swap; parent index 1 (5) → swap; parent index 0 (4) → "
                "swap → [1, 4, 7, 5, 6, 10, 8, 12, 9].\n\n"
                "With n = 9 nodes, the leaves are indices ⌊n/2⌋ … n − 1 = 4 … 8: keys 6, 10, 8, 12, 9.\n\n"
                "Sum = 6 + 10 + 8 + 12 + 9 = **45**.\n\n"
                "**Trap:** in sift-down, swapping with the *left* child by habit (7 ↔ 5 in the first step) "
                "breaks the heap; always choose the smaller child. **Tip:** leaves of an n-node heap are "
                "exactly indices ⌊n/2⌋ to n − 1."
            ),
            "solution_diagrams": [{"type": "heap", "values": [1, 4, 7, 5, 6, 10, 8, 12, 9],
                                   "caption": "Final min-heap"}],
            "verify": '''
H = [2, 5, 3, 9, 6, 4, 8, 12, 10, 7]
def popmin(h):
    x = h[0]; h[0] = h.pop(); i = 0
    while True:
        c = [j for j in (2 * i + 1, 2 * i + 2) if j < len(h)]
        if not c: break
        m = min(c, key=lambda j: h[j])
        if h[m] >= h[i]: break
        h[m], h[i] = h[i], h[m]; i = m
    return x
def push(h, x):
    h.append(x); i = len(h) - 1
    while i and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p
assert popmin(H) == 2 and popmin(H) == 3
push(H, 1)
assert H == [1, 4, 7, 5, 6, 10, 8, 12, 9]
assert sum(H[len(H) // 2:]) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Dijkstra with a negative edge",
            "text": ("Dijkstra's algorithm is run from S on the directed graph below, which has one negative edge "
                     "(A → B with weight −3). The implementation never changes the distance of a vertex after it "
                     "has been extracted, and breaks ties alphabetically. Which set of vertices ends up with a "
                     "final distance **different** from the true shortest-path distance?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E"],
                          "edges": [["S", "A", 4], ["S", "B", 2], ["A", "B", -3], ["B", "C", 3], ["A", "D", 1],
                                    ["C", "E", 1], ["D", "E", 5]],
                          "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 0], "D": [4, 2],
                                  "E": [6, 1]}}],
            "options": ["{B, C, E}", "{B}", "{B, C}", "{B, C, D, E}"],
            "answer": "A",
            "solution": (
                "Dijkstra assumes that once a vertex is extracted no later path can be shorter — false with "
                "negative edges.\n\n"
                "**Dijkstra run:**\n\n"
                "- Extract S (0): A = 4, B = 2\n"
                "- Extract B (2): C = 5\n"
                "- Extract A (4): A→B would give 1, but B is already finalised → ignored; D = 5\n"
                "- Extract C (5, tie with D broken alphabetically): E = 6\n"
                "- Extract D (5): 5 + 5 = 10 > 6 → no change; extract E (6)\n\n"
                "Dijkstra: A 4, B 2, C 5, D 5, E 6.\n\n"
                "**True distances** (e.g. Bellman–Ford): B = 4 − 3 = 1 via S→A→B, C = 1 + 3 = 4, E = 4 + 1 = 5, "
                "A = 4, D = 5.\n\n"
                "Wrong vertices: **B, C, E** — the error at B propagates to everything reached through B.\n\n"
                "- (B) ignores propagation.\n"
                "- (C) misses that E's best path also goes through C.\n"
                "- (D) D's distance 5 (S→A→D) is correct.\n\n"
                "**Tip:** with negative edges use Bellman–Ford (V − 1 rounds of relaxing all edges)."
            ),
            "verify": '''
G = {"S": [("A", 4), ("B", 2)], "A": [("B", -3), ("D", 1)], "B": [("C", 3)], "C": [("E", 1)],
     "D": [("E", 5)], "E": []}
d = {v: float("inf") for v in G}; d["S"] = 0; done = set()
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: (d[v], v)); done.add(u)
    for v, w in G[u]:
        if v not in done and d[u] + w < d[v]: d[v] = d[u] + w
bf = {v: float("inf") for v in G}; bf["S"] = 0
for _ in range(len(G) - 1):
    for u in G:
        for v, w in G[u]:
            if bf[u] + w < bf[v]: bf[v] = bf[u] + w
wrong = {v for v in G if d[v] != bf[v]}
opts = [{"B", "C", "E"}, {"B"}, {"B", "C"}, {"B", "C", "D", "E"}]
assert [c for c, o in zip("ABCD", opts) if o == wrong] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "BFS — shortest paths in a hypercube",
            "text": ("The 4-dimensional hypercube Q₄ has the 16 binary strings of length 4 as vertices; two vertices "
                     "are adjacent iff they differ in exactly one bit. The number of distinct shortest paths from "
                     "0000 to 1111 is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["000", "001", "010", "011", "100", "101", "110", "111"],
                          "edges": [["000", "001"], ["000", "010"], ["000", "100"], ["001", "011"],
                                    ["001", "101"], ["010", "011"], ["010", "110"], ["100", "101"],
                                    ["100", "110"], ["011", "111"], ["101", "111"], ["110", "111"]],
                          "pos": {"000": [0, 0], "001": [2.4, 0], "010": [0, 2.4], "011": [2.4, 2.4],
                                  "100": [1, 0.9], "101": [3.4, 0.9], "110": [1, 3.3], "111": [3.4, 3.3]},
                          "caption": "For intuition: the 3-cube Q₃"}],
            "answer": "24",
            "solution": (
                "The distance between two vertices of a hypercube is the number of bits in which they differ "
                "(Hamming distance): d(0000, 1111) = 4. A shortest path must flip each of the 4 bits "
                "**exactly once**; flipping any bit twice wastes two steps.\n\n"
                "So a shortest path is just an order in which to flip the 4 bits: 4! = **24**.\n\n"
                "BFS path counting agrees: σ(level 1 vertex) = 1 (4 vertices), σ(level 2) = 2 (6 vertices, "
                "each reachable from 2 level-1 vertices), σ(level 3) = 3 · 2 = 6, σ(1111) = 4 · 6 = 24.\n\n"
                "**Trap:** counting vertices at distance 2 (C(4, 2) = 6) or the number of edges (32) instead of "
                "paths. **Generalisation:** in Q_{n}, two vertices at Hamming distance k are joined by k! "
                "shortest paths."
            ),
            "verify": '''
from collections import deque
V = [format(i, "04b") for i in range(16)]
adj = {v: [u for u in V if sum(a != b for a, b in zip(u, v)) == 1] for v in V}
dist = {"0000": 0}; sig = {"0000": 1}; q = deque(["0000"])
while q:
    u = q.popleft()
    for w in adj[u]:
        if w not in dist: dist[w] = dist[u] + 1; sig[w] = sig[u]; q.append(w)
        elif dist[w] == dist[u] + 1: sig[w] += sig[u]
assert sig["1111"] == int(ANSWER) and dist["1111"] == 4
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Quicksort — input sensitivity",
            "text": ("Quicksort uses the Lomuto partition with the **last** element as pivot; a partition of a "
                     "subarray of size s makes exactly s − 1 key comparisons, and subarrays of size ≤ 1 are not "
                     "partitioned. Which of the following statements about sorting 6 distinct keys is/are TRUE?"),
            "options": [
                "On [1, 2, 3, 4, 5, 6] it makes 15 comparisons",
                "On [6, 5, 4, 3, 2, 1] it makes 15 comparisons",
                "On [2, 1, 4, 3, 6, 5] it makes 8 comparisons",
                "On every permutation of 6 distinct keys it makes at least 8 comparisons",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Total comparisons = Σ (s − 1) over all partitioned subarrays; everything depends on how "
                "balanced the splits are.\n\n"
                "- (A) sorted input: the pivot is always the maximum → splits (5, 0), (4, 0), … → "
                "5 + 4 + 3 + 2 + 1 = 15. **True.**\n"
                "- (B) reverse-sorted: first pivot 1 is the minimum → [1 | 5 4 3 2 6]; the next pivot 6 is the "
                "maximum, then 2 is the minimum, … every split is still (n−1, 0) → 15. **True.**\n"
                "- (C) [2, 1, 4, 3, 6, 5]: pivot 5 → 5 comparisons, split [2 1 4 3] | [6]; pivot 3 → 3, split "
                "[2 1] | [4]; pivot 1 → 1 → total 5 + 3 + 1 = **9**, not 8. **False.**\n"
                "- (D) The first partition always costs 5. The best split of the remaining 5 elements is "
                "(2, 3) → 1 + 2 = 3 more (the 3-part costs 2 and splits 1|1), total 8; every other split "
                "costs more (e.g. (1, 4) → 0 + 3 + … ≥ 4). For example [3, 1, 2, 5, 6, 4] achieves 8. **True.**\n\n"
                "**Tip:** for n = 2^{k} − 1 a perfect pivot sequence gives the minimum; for other n the "
                "minimum is found by the best balanced split at each level."
            ),
            "verify": '''
import itertools
def qc(arr):
    A = arr[:]; c = [0]
    def part(lo, hi):
        p = A[hi]; i = lo - 1
        for j in range(lo, hi):
            c[0] += 1
            if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]; return i + 1
    def qs(lo, hi):
        if lo < hi:
            m = part(lo, hi); qs(lo, m - 1); qs(m + 1, hi)
    qs(0, len(A) - 1)
    return c[0]
mn = min(qc(list(p)) for p in itertools.permutations(range(6)))
truth = [qc([1, 2, 3, 4, 5, 6]) == 15, qc([6, 5, 4, 3, 2, 1]) == 15, qc([2, 1, 4, 3, 6, 5]) == 8, mn >= 8]
assert mn == 8 and qc([3, 1, 2, 5, 6, 4]) == 8
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MCQ", "marks": 2, "topic": "Bubble sort vs selection sort — swaps",
            "text": ("Let X be the number of swaps made by bubble sort and Y the number of swaps made by selection "
                     "sort (which swaps only when the minimum is not already in place) when sorting "
                     "[8, 3, 6, 1, 7, 2, 5, 4] in ascending order. The value of X − Y is"),
            "options": ["12", "11", "17", "13"],
            "answer": "A",
            "solution": (
                "**Bubble sort** swaps only adjacent out-of-order pairs, and each swap removes exactly one "
                "inversion, so X = number of inversions.\n\n"
                "For each element, count larger elements before it: 8: 0, 3: 1, 6: 1, 1: 3, 7: 1, 2: 4, 5: 3, "
                "4: 4 → X = **17**.\n\n"
                "**Selection sort** trace:\n\n"
                "- i=0: min 1 → swap with 8 → [1, 3, 6, 8, 7, 2, 5, 4]\n"
                "- i=1: min 2 → swap with 3 → [1, 2, 6, 8, 7, 3, 5, 4]\n"
                "- i=2: min 3 → swap with 6 → [1, 2, 3, 8, 7, 6, 5, 4]\n"
                "- i=3: min 4 → swap with 8 → [1, 2, 3, 4, 7, 6, 5, 8]\n"
                "- i=4: min 5 → swap with 7 → [1, 2, 3, 4, 5, 6, 7, 8]\n"
                "- i=5, 6: already in place\n\n"
                "Y = **5**, so X − Y = 17 − 5 = **12**.\n\n"
                "- (B) 11 uses Y = 6 (counting a swap at i=5).\n"
                "- (C) 17 is X alone.\n"
                "- (D) 13 uses Y = 4.\n\n"
                "**Tip:** selection sort does at most n − 1 swaps (Θ(n)) while bubble sort may do Θ(n²) — "
                "selection sort is preferred when writes are expensive."
            ),
            "verify": '''
A = [8, 3, 6, 1, 7, 2, 5, 4]
B = A[:]; X = 0
for p in range(len(B) - 1):
    for j in range(len(B) - 1 - p):
        if B[j] > B[j + 1]: B[j], B[j + 1] = B[j + 1], B[j]; X += 1
C = A[:]; Y = 0
for i in range(len(C) - 1):
    m = min(range(i, len(C)), key=lambda j: C[j])
    if m != i: C[i], C[m] = C[m], C[i]; Y += 1
assert (X, Y) == (17, 5) and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Double hashing — choosing h₂",
            "text": ("A table of size m = 12 uses double hashing: probe i examines (h₁(k) + i·h₂(k)) mod 12. "
                     "Which choice of h₂ guarantees that, for **every** key k ≥ 0, the probe sequence visits all "
                     "12 slots?"),
            "options": ["h₂(k) = 1 + 6·(k mod 2)", "h₂(k) = 1 + (k mod 11)",
                        "h₂(k) = 1 + 2·(k mod 6)", "h₂(k) = 1 + 4·(k mod 3)"],
            "answer": "A",
            "solution": (
                "The sequence h₁, h₁ + s, h₁ + 2s, … (mod m) visits all m slots iff gcd(s, m) = 1. For m = 12 "
                "the good step sizes are s ∈ {1, 5, 7, 11}.\n\n"
                "- (A) values {1, 7} — both coprime to 12. **Always full coverage.**\n"
                "- (B) values 1 … 11, including 2, 3, 4, 6, 8, 9, 10 → e.g. k = 1 gives s = 2, which visits only "
                "the 6 slots of one parity.\n"
                "- (C) values {1, 3, 5, 7, 9, 11} → s = 3 or 9 visits only 4 slots (gcd 3).\n"
                "- (D) values {1, 5, 9} → s = 9 has gcd(9, 12) = 3 → only 4 slots.\n\n"
                "**Tip:** this is why double hashing usually takes m **prime** (then any s in 1 … m − 1 "
                "works) or m a power of 2 with s forced odd."
            ),
            "verify": '''
from math import gcd
fs = [lambda k: 1 + 6 * (k % 2), lambda k: 1 + (k % 11), lambda k: 1 + 2 * (k % 6), lambda k: 1 + 4 * (k % 3)]
def full(f):
    return all(len({(k % 12 + i * f(k)) % 12 for i in range(12)}) == 12 for k in range(200))
assert [c for c, f in zip("ABCD", fs) if full(f)] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Python — sorted() with key functions and stability",
            "text": ("Let `words = [\"kiwi\", \"fig\", \"apple\", \"date\", \"plum\", \"pear\"]`. "
                     "Which of the following statements is/are TRUE?"),
            "options": [
                "`sorted(words, key=len)[1:5]` equals `['kiwi', 'date', 'plum', 'pear']`",
                "`sorted(words, key=lambda w: (-len(w), w))[1]` equals `'date'`",
                "`sorted(words, key=len, reverse=True)[1]` equals `'pear'`",
                "`min(words, key=lambda w: w[-1])` equals `'date'`",
            ],
            "answer": ["A", "B"],
            "solution": (
                "`sorted` is **stable**: items with equal keys keep their original relative order — and this "
                "remains true with `reverse=True` (Python reverses the comparison, not the result). "
                "`min`/`max` return the **first** item with the extreme key.\n\n"
                "- (A) key=len: fig(3); then the four 4-letter words in input order kiwi, date, plum, pear; "
                "then apple(5). Slice [1:5] → ['kiwi', 'date', 'plum', 'pear']. **True.**\n"
                "- (B) key (−len, w): longest first, ties alphabetical → apple, date, kiwi, pear, plum, fig → "
                "index 1 is 'date'. **True.**\n"
                "- (C) reverse=True by length: apple, then the 4-letter words **still in input order** "
                "kiwi, date, plum, pear, then fig → index 1 is 'kiwi'. **False.**\n"
                "- (D) last letters: i, g, e, e, m, r → smallest 'e', first achieved by 'apple'. **False.**\n\n"
                "**Trap:** (C) — many expect `reverse=True` to reverse the tie order as well (that would be "
                "`sorted(words, key=len)[::-1]`, which gives 'pear' at index 1)."
            ),
            "verify": '''
words = ["kiwi", "fig", "apple", "date", "plum", "pear"]
truth = [sorted(words, key=len)[1:5] == ['kiwi', 'date', 'plum', 'pear'],
         sorted(words, key=lambda w: (-len(w), w))[1] == 'date',
         sorted(words, key=len, reverse=True)[1] == 'pear',
         min(words, key=lambda w: w[-1]) == 'date']
assert sorted(words, key=len)[::-1][1] == 'pear'
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
    ],
}
