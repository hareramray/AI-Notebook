# Set 25 — Binary Search Variants
SET = {
    "number": 25,
    "title": "Binary Search Variants",
    "difficulty": "GATE-level",
    "focus": "lower/upper bound, rotated arrays, search on answer, off-by-one bugs",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — lower bound",
            "text": ("Consider the following Python program, run on the sorted array A shown. "
                     "The value printed is ______."),
            "code": '''def lb(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

A = [3, 7, 7, 7, 12, 15, 15, 21, 30]
print(lb(A, 15) + lb(A, 8) + lb(A, 31))''',
            "diagrams": [{"type": "array", "values": [3, 7, 7, 7, 12, 15, 15, 21, 30], "label": "A"}],
            "answer": "18",
            "solution": (
                "**Concept.** `lb` is the classic *lower bound*: it returns the smallest index i with "
                "A[i] ≥ x (or len(A) if no such index). The half-open range [lo, hi) always contains "
                "the answer, and `hi = mid` keeps mid as a candidate.\n\n"
                "- lb(A, 15): first element ≥ 15 is A[5] = 15 → 5. (Trace: [0,9) mid 4 (12<15) → "
                "lo 5; [5,9) mid 7 (21) → hi 7; [5,7) mid 6 (15) → hi 6; [5,6) mid 5 (15) → hi 5.)\n"
                "- lb(A, 8): 8 is absent; first element ≥ 8 is A[4] = 12 → 4.\n"
                "- lb(A, 31): every element is < 31 → returns len(A) = 9.\n\n"
                "Sum = 5 + 4 + 9 = **18**.\n\n"
                "**Trap:** returning the index of the *last* 15 (6) or treating the 'not found' case "
                "as −1. Lower bound never returns −1 — it returns an insertion point."
            ),
            "verify": '''
import bisect
assert sum(bisect.bisect_left(A, x) for x in (15, 8, 31)) == int(ANSWER) == int(OUTPUT)
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — off-by-one and termination",
            "text": ("Consider the function below, intended to return the index of the last element "
                     "≤ x. With A = [2, 4, 6, 8], which of the following calls **never terminates**?"),
            "code": '''def f(A, x):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo''',
            "options": ["`f(A, 5)`", "`f(A, 1)`", "`f(A, 7)`", "`f(A, 4)`"],
            "answer": "C",
            "solution": (
                "**Concept.** With `mid = (lo + hi) // 2` (floor) and the update `lo = mid`, the "
                "range does not shrink when hi = lo + 1 and A[lo] ≤ x: then mid = lo and lo stays "
                "the same forever. A 'move lo to mid' loop needs the **ceiling** mid "
                "`(lo + hi + 1) // 2`.\n\n"
                "Traces on A = [2, 4, 6, 8]:\n"
                "- f(A, 5): (0,3) mid 1, 4 ≤ 5 → lo 1; (1,3) mid 2, 6 > 5 → hi 1; stop → 1.\n"
                "- f(A, 1): (0,3) mid 1, 4 > 1 → hi 0; stop → 0.\n"
                "- f(A, 7): (0,3) mid 1 → lo 1; (1,3) mid 2, 6 ≤ 7 → lo 2; (2,3) mid 2 → lo 2 "
                "again … **infinite loop**.\n"
                "- f(A, 4): (0,3) mid 1 → lo 1; (1,3) mid 2, 6 > 4 → hi 1; stop → 1.\n\n"
                "Answer (C).\n\n"
                "**Tip:** a quick termination test: check the two-element range (lo, lo + 1). Each "
                "branch must strictly shrink it."
            ),
            "verify": '''
def g(A, x, limit=100):
    lo, hi, n = 0, len(A) - 1, 0
    while lo < hi:
        n += 1
        if n > limit: return None
        mid = (lo + hi) // 2
        if A[mid] <= x: lo = mid
        else: hi = mid - 1
    return lo
A = [2, 4, 6, 8]
res = {k: g(A, x) for k, x in zip("ABCD", (5, 1, 7, 4))}
assert [k for k in res if res[k] is None] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Python — generator exhaustion",
            "text": "Consider the following Python program. What is printed?",
            "code": '''g = (x * x for x in range(6) if x % 2)
print(sum(g), max(g, default=-1), list(g))''',
            "options": ["`35 25 [1, 9, 25]`", "`35 -1 []`", "`35 25 []`",
                        "`ValueError` is raised"],
            "answer": "B",
            "solution": (
                "**Concept.** A generator expression is a one-shot iterator. Once consumed, further "
                "iteration yields nothing. The arguments of `print` are evaluated left to right.\n\n"
                "- `x % 2` is truthy for odd x → the generator yields 1, 9, 25.\n"
                "- `sum(g)` consumes all of it → 35.\n"
                "- `max(g, default=-1)` sees an empty iterator → returns the default −1 "
                "(without `default`, it would raise ValueError).\n"
                "- `list(g)` → `[]`.\n\n"
                "Output: `35 -1 []` → (B).\n\n"
                "- (A) and (C) assume the generator restarts like a list.\n"
                "- (D) would be right only if `default` were omitted.\n\n"
                "**Trap:** a list comprehension `[x*x for …]` would give `35 25 [1, 9, 25]`; "
                "parentheses instead of brackets change everything."
            ),
            "verify": "assert OUTPUT.strip() == '35 -1 []'",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Python — the bisect module",
            "text": ("Let `A = [1, 3, 3, 3, 7, 9]` and assume `import bisect`. Which of the following "
                     "expressions evaluate to `True`?"),
            "options": ["`bisect.bisect_left(A, 3) == 1`",
                        "`bisect.bisect_right(A, 3) - bisect.bisect_left(A, 3) == 3`",
                        "`bisect.bisect(A, 8) == 4`",
                        "`bisect.bisect_right(A, 9) == 5`"],
            "answer": ["A", "B"],
            "solution": (
                "**Concept.** `bisect_left(A, x)` = first index i with A[i] ≥ x (lower bound); "
                "`bisect_right(A, x)` = first index i with A[i] > x (upper bound). `bisect` is an "
                "alias of `bisect_right`. Their difference counts occurrences of x.\n\n"
                "- (A) First element ≥ 3 is at index 1. **True.**\n"
                "- (B) bisect_right(A, 3) = 4 (first element > 3 is 7 at index 4); 4 − 1 = 3 "
                "occurrences. **True.**\n"
                "- (C) First element > 8 is 9 at index 5, so the result is 5. **False.**\n"
                "- (D) No element is > 9, so bisect_right returns len(A) = 6. **False.**\n\n"
                "**Trap:** treating `bisect` as 'index of x' — it returns an insertion point, which "
                "may equal len(A)."
            ),
            "verify": '''
import bisect
A = [1, 3, 3, 3, 7, 9]
truth = {"A": bisect.bisect_left(A, 3) == 1,
         "B": bisect.bisect_right(A, 3) - bisect.bisect_left(A, 3) == 3,
         "C": bisect.bisect(A, 8) == 4, "D": bisect.bisect_right(A, 9) == 5}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Queues — queue using two stacks",
            "text": ("A queue is implemented with two stacks IN and OUT. `enqueue(x)` pushes x on IN. "
                     "`dequeue()` pops from OUT; if OUT is empty it first pops every element of IN "
                     "and pushes it on OUT. Each individual push or pop costs 1. Starting empty, the "
                     "sequence\n\n"
                     "E1, E2, E3, D, E4, E5, D, D, D, E6, D\n\n"
                     "is executed (Ek = enqueue k, D = dequeue). The total cost is"),
            "options": ["19", "21", "23", "25"],
            "answer": "B",
            "solution": (
                "**Concept.** Each element is pushed on IN once, moved to OUT at most once (1 pop + "
                "1 push) and popped from OUT once — at most 4 operations per element, giving O(1) "
                "amortised cost.\n\n"
                "Trace:\n"
                "- E1, E2, E3: 3 pushes → cost 3. IN = [1, 2, 3].\n"
                "- D: OUT empty → move 3 elements (6) + pop 1 → cost 7. OUT = [3, 2].\n"
                "- E4, E5: cost 2. IN = [4, 5].\n"
                "- D: pop 2 → 1.  D: pop 3 → 1 (OUT now empty).\n"
                "- D: move 4, 5 (4) + pop 4 → 5. OUT = [5].\n"
                "- E6: 1.  D: pop 5 → 1.\n\n"
                "Total = 3 + 7 + 2 + 1 + 1 + 5 + 1 + 1 = **21** → (B).\n\n"
                "Check with the per-element rule: elements 1–5 each cost 4 (20); 6 is pushed only (1) → 21.\n\n"
                "**Trap:** moving IN to OUT on *every* dequeue (not only when OUT is empty) — "
                "that breaks FIFO order and inflates the cost."
            ),
            "verify": '''
IN, OUT, cost = [], [], 0
for op in "E1 E2 E3 D E4 E5 D D D E6 D".split():
    if op[0] == "E": IN.append(int(op[1:])); cost += 1
    else:
        if not OUT:
            while IN: OUT.append(IN.pop()); cost += 2
        OUT.pop(); cost += 1
assert cost == 21 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search trees — deletion",
            "text": ("The keys 40, 20, 60, 10, 30, 50, 70, 25, 35, 33 are inserted in that order into "
                     "an empty BST. Then 40 is deleted; a node with two children is replaced by its "
                     "**in-order predecessor**. What is the pre-order traversal of the resulting tree?"),
            "options": ["35, 20, 10, 30, 25, 33, 60, 50, 70",
                        "50, 20, 10, 30, 25, 35, 33, 60, 70",
                        "35, 20, 10, 30, 25, 60, 50, 70, 33",
                        "33, 20, 10, 30, 25, 35, 60, 50, 70"],
            "answer": "A",
            "solution": (
                "**Concept.** The in-order predecessor of a node with two children is the maximum "
                "of its left subtree (rightmost node there). It has no right child, so it can be "
                "unlinked by attaching its left child to its parent.\n\n"
                "Tree before deletion: 40 → (20 → 10, 30 → (25, 35 → (33, ·))), (60 → 50, 70).\n\n"
                "- Predecessor of 40 = rightmost of the left subtree: 20 → 30 → 35 → **35**.\n"
                "- Copy 35 into the root, and replace node 35 by its left child 33 (so 33 becomes "
                "30's right child).\n\n"
                "New tree: 35 → (20 → 10, 30 → (25, 33)), (60 → 50, 70). Pre-order: "
                "35, 20, 10, 30, 25, 33, 60, 50, 70 → (A).\n\n"
                "- (B) uses the in-order successor (50).\n"
                "- (C) drops 33 into the wrong subtree.\n"
                "- (D) picks 33 — the predecessor of 35, not of 40.\n\n"
                "**Trap:** forgetting to re-attach the predecessor's left child (33)."
            ),
            "diagrams": [{"type": "bintree",
                          "tree": [40, [20, [10], [30, [25], [35, [33], None]]], [60, [50], [70]]],
                          "caption": "BST before deleting 40"}],
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [35, [20, [10], [30, [25], [33]]], [60, [50], [70]]],
                                   "highlight": [35, 33], "caption": "After deleting 40"}],
            "verify": '''
def ins(t, k):
    if t is None: return [k, None, None]
    i = 1 if k < t[0] else 2; t[i] = ins(t[i], k); return t
def delete(t, k):
    if t is None: return None
    if k < t[0]: t[1] = delete(t[1], k)
    elif k > t[0]: t[2] = delete(t[2], k)
    else:
        if t[1] is None: return t[2]
        if t[2] is None: return t[1]
        p = t[1]
        while p[2]: p = p[2]
        t[0] = p[0]; t[1] = delete(t[1], p[0])
    return t
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
t = None
for k in [40, 20, 60, 10, 30, 50, 70, 25, 35, 33]: t = ins(t, k)
assert pre(delete(t, 40)) == [35, 20, 10, 30, 25, 33, 60, 50, 70] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — quadratic probing",
            "text": ("The keys 22, 34, 11, 45, 56, 23 are inserted in that order into an empty hash "
                     "table of size 11 using quadratic probing: the i-th probe (i = 0, 1, 2, …) for "
                     "key k examines slot (k mod 11 + i²) mod 11. The slot in which key 23 is stored "
                     "is ______."),
            "answer": "10",
            "solution": (
                "**Concept.** Quadratic probing jumps by offsets 0, 1, 4, 9, 16, … from the home "
                "slot, which avoids primary clustering, but keys with the same home slot still "
                "follow the same sequence (secondary clustering).\n\n"
                "Trace:\n"
                "- 22: home 0 → slot 0.\n"
                "- 34: home 1 → slot 1.\n"
                "- 11: home 0 (full) → 0 + 1 = 1 (full) → 0 + 4 = **4**.\n"
                "- 45: home 1 (full) → 1 + 1 = **2**.\n"
                "- 56: home 1 (full) → 2 (full) → 1 + 4 = **5**.\n"
                "- 23: home 1 (full) → 2 (full) → 5 (full) → 1 + 9 = **10**.\n\n"
                "Key 23 goes to slot **10**.\n\n"
                "**Trap:** using linear offsets i instead of i² gives slot 3; using the *previous* "
                "probe + i² (cumulative) also gives a different slot."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 22, 1: 34, 2: 45, 4: 11, 5: 56, 10: 23},
                                   "caption": "Final table"}],
            "verify": '''
T = [None]*11
for k in [22, 34, 11, 45, 56, 23]:
    i = 0
    while T[(k % 11 + i*i) % 11] is not None: i += 1
    T[(k % 11 + i*i) % 11] = k
assert T.index(23) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Sorting — binary insertion sort",
            "text": ("In *binary insertion sort*, insertion sort on an array is modified so that the "
                     "position of A[i] in the sorted prefix A[0..i−1] is found by binary search; the "
                     "larger elements are then shifted one place right. For an input of n distinct "
                     "keys in **decreasing** order, which statement is correct?"),
            "options": [
                "It makes Θ(n log n) comparisons and runs in Θ(n log n) time",
                "It makes Θ(n) comparisons and runs in Θ(n²) time",
                "It makes Θ(n²) comparisons and runs in Θ(n²) time",
                "It makes Θ(n log n) comparisons but runs in Θ(n²) time",
            ],
            "answer": "D",
            "solution": (
                "**Concept.** Binary search reduces the *comparisons* per insertion to O(log i), but "
                "the *data movement* in an array is unchanged: inserting at position p requires "
                "shifting i − p elements.\n\n"
                "Decreasing input: every new key is the smallest so far.\n"
                "- Comparisons: ∑ ⌈log₂(i + 1)⌉ over i = 1 … n − 1 = Θ(n log n).\n"
                "- Shifts: key i moves past all i previous keys → ∑ i = n(n − 1)/2 = Θ(n²).\n"
                "- Running time is dominated by shifts → Θ(n²).\n\n"
                "Hence (D).\n\n"
                "- (A) ignores the shifting cost.\n"
                "- (C) is ordinary insertion sort's comparison count, not binary insertion sort's.\n"
                "- (B) under-counts the binary searches.\n\n"
                "**Trap:** 'binary search makes insertion sort O(n log n)' — only the comparison "
                "count improves. On a linked list shifting is cheap, but binary search is then "
                "impossible in O(log n)."
            ),
            "verify": '''
import bisect
def bis(A):
    A = A[:]; comps = shifts = 0
    for i in range(1, len(A)):
        x, lo, hi = A[i], 0, i
        while lo < hi:
            mid = (lo + hi) // 2; comps += 1
            if A[mid] <= x: lo = mid + 1
            else: hi = mid
        shifts += i - lo; A[lo+1:i+1] = A[lo:i]; A[lo] = x
    assert A == sorted(A)
    return comps, shifts
c, s = bis(list(range(2000, 0, -1)))
import math
assert c < 2000 * 12 and s == 2000 * 1999 // 2 and ANSWER == "D"
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Graph theory — components and edge count",
            "text": ("A simple undirected graph has 12 vertices and exactly 4 connected components. "
                     "The maximum possible number of edges in such a graph is ______."),
            "answer": "36",
            "solution": (
                "**Concept.** For a fixed number of vertices and components, the edge count is "
                "maximised by making every component complete and putting as many vertices as "
                "possible into one component: C(a, 2) + C(b, 2) is larger when the sizes are "
                "unbalanced (convexity of C(x, 2)).\n\n"
                "- Use three isolated vertices and one component with 12 − 3 = 9 vertices.\n"
                "- Make that component K₉: C(9, 2) = 9 · 8 / 2 = **36** edges.\n\n"
                "General formula: C(n − k + 1, 2) for n vertices and k components.\n\n"
                "Comparison: a balanced split 3 + 3 + 3 + 3 gives only 4 · C(3, 2) = 12 edges.\n\n"
                "**Trap:** computing C(12, 2) − (something) or splitting evenly. Also, the minimum "
                "number of edges with 4 components is n − k = 8 (a forest)."
            ),
            "verify": '''
from itertools import combinations_with_replacement
best = 0
for parts in combinations_with_replacement(range(1, 13), 4):
    if sum(parts) == 12: best = max(best, sum(p*(p-1)//2 for p in parts))
assert best == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search trees — valid search sequences",
            "text": ("A BST with integer keys is searched for the key 55, and the keys of the nodes "
                     "examined are recorded in order. Which of the following sequences **cannot** "
                     "be such a record?"),
            "options": ["90, 20, 80, 30, 70, 40, 60, 55",
                        "10, 75, 64, 43, 60, 57, 55",
                        "50, 65, 52, 60, 58, 55",
                        "30, 70, 45, 62, 42, 55"],
            "answer": "D",
            "solution": (
                "**Concept.** While searching for x, each examined key narrows the open interval in "
                "which every later key must lie: after visiting k < x we need later keys > k; after "
                "k > x, later keys < k. A sequence is valid iff every key falls in the current "
                "interval.\n\n"
                "- (A) (−∞,∞) → 90: (−∞,90) → 20: (20,90) → 80: (20,80) → 30: (30,80) → 70: (30,70) "
                "→ 40: (40,70) → 60: (40,60) → 55 ✓. Valid.\n"
                "- (B) 10: (10,∞) → 75: (10,75) → 64: (10,64) → 43: (43,64) → 60: (43,60) → 57: "
                "(43,57) → 55 ✓. Valid.\n"
                "- (C) 50: (50,∞) → 65: (50,65) → 52: (52,65) → 60: (52,60) → 58: (52,58) → 55 ✓. Valid.\n"
                "- (D) 30: (30,∞) → 70: (30,70) → 45: (45,70) → 62: (45,62) → **42** is not in "
                "(45, 62). Invalid → (D).\n\n"
                "**Trap:** checking only adjacent pairs. 42 is between 30 and 62, but it violates "
                "the lower bound set earlier by 45."
            ),
            "verify": '''
def ok(seq, x):
    lo, hi = float('-inf'), float('inf')
    for k in seq[:-1]:
        if not lo < k < hi: return False
        if k < x: lo = k
        else: hi = k
    return seq[-1] == x and lo < x < hi
opts = {"A": [90,20,80,30,70,40,60,55], "B": [10,75,64,43,60,57,55],
        "C": [50,65,52,60,58,55], "D": [30,70,45,62,42,55]}
assert [k for k in opts if not ok(opts[k], 55)] == [ANSWER]
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Binary search — rotated sorted array",
            "text": ("The function below searches a rotated sorted array of distinct keys. For the "
                     "array A shown, let p₁ be the number of probes returned by `search(A, 9)` and "
                     "p₂ the number returned by `search(A, 50)`. The value of p₁ + p₂ is ______."),
            "code": '''def search(A, x):
    lo, hi, probes = 0, len(A) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        probes += 1
        if A[mid] == x:
            return mid, probes
        if A[lo] <= A[mid]:            # left half sorted
            if A[lo] <= x < A[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                          # right half sorted
            if A[mid] < x <= A[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1, probes''',
            "diagrams": [{"type": "array", "values": [41, 47, 53, 60, 4, 9, 17, 23, 30, 36],
                          "label": "A"}],
            "answer": "7",
            "solution": (
                "**Concept.** In a rotated sorted array, at least one of the halves A[lo..mid] and "
                "A[mid..hi] is sorted. Test whether x lies inside the sorted half's range; if so, "
                "search there, otherwise search the other half. Each probe still halves the range.\n\n"
                "search(A, 9):\n"
                "- lo 0, hi 9 → mid 4 (A = 4). A[0] = 41 > 4, so the right half [4 … 36] is sorted; "
                "4 < 9 ≤ 36 → lo = 5.\n"
                "- lo 5, hi 9 → mid 7 (23). A[5] = 9 ≤ 23 → left half [9 … 23] sorted; 9 ≤ 9 < 23 → hi = 6.\n"
                "- lo 5, hi 6 → mid 5 (9) → found. p₁ = 3.\n\n"
                "search(A, 50):\n"
                "- mid 4 (4): right half sorted, 50 ∉ (4, 36] → hi = 3.\n"
                "- lo 0, hi 3 → mid 1 (47): left half [41, 47] sorted, 50 ∉ [41, 47) → lo = 2.\n"
                "- lo 2, hi 3 → mid 2 (53): left half [53] sorted, 50 ∉ [53, 53) → lo = 3.\n"
                "- lo 3, hi 3 → mid 3 (60): 50 ∉ [60, 60) → lo = 4; loop ends. p₂ = 4.\n\n"
                "p₁ + p₂ = 3 + 4 = **7**.\n\n"
                "**Trap:** using `A[lo] < A[mid]` (strict) misclassifies the one-element left half "
                "when lo = mid; the `<=` test is essential."
            ),
            "verify": '''
A = [41, 47, 53, 60, 4, 9, 17, 23, 30, 36]
assert search(A, 9) == (5, 3) and search(A, 50)[0] == -1
assert search(A, 9)[1] + search(A, 50)[1] == int(ANSWER)
for x in A: assert A[search(A, x)[0]] == x
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "MSQ", "marks": 2, "topic": "Binary search — correctness of first-occurrence variants",
            "text": ("Each function below is meant to return the index of the **first** occurrence of "
                     "x in a sorted list A (possibly with duplicates, possibly empty), or −1 if x does "
                     "not occur. Which of the functions is/are correct (terminate and return the "
                     "right value) for **every** such input?"),
            "code": '''def f1(A, x):
    lo, hi, ans = 0, len(A) - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] >= x:
            if A[mid] == x:
                ans = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return ans

def f2(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] < x: lo = mid + 1
        else: hi = mid
    return lo if A[lo] == x else -1

def f3(A, x):
    lo, hi = -1, len(A)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if A[mid] < x: lo = mid
        else: hi = mid
    return hi if hi < len(A) and A[hi] == x else -1

def f4(A, x):
    lo, hi = 0, len(A) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if A[mid] <= x: lo = mid
        else: hi = mid - 1
    return lo if A and A[lo] == x else -1''',
            "options": ["`f1`", "`f2`", "`f3`", "`f4`"],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** A first-occurrence search must keep moving **left** after a match, "
                "must make progress in every branch, and must not index outside the list.\n\n"
                "- **f1** — closed interval [lo, hi]; on A[mid] ≥ x it records a match (if equal) and "
                "continues left with hi = mid − 1, else goes right. Every branch shrinks the range; "
                "the last recorded match is the leftmost. Empty list: loop skipped, returns −1. "
                "**Correct.**\n"
                "- **f2** — computes the lower bound correctly, but when x is larger than every "
                "element (or A is empty) lo = len(A) and `A[lo]` raises **IndexError**. E.g. "
                "f2([1, 2], 5). **Incorrect.**\n"
                "- **f3** — invariant A[lo] < x ≤ A[hi] with virtual sentinels A[−1] = −∞ and "
                "A[n] = +∞; the loop stops when hi = lo + 1, so hi is the lower bound. The guard "
                "`hi < len(A)` prevents out-of-range access. **Correct.**\n"
                "- **f4** — ceiling mid with `lo = mid` on A[mid] ≤ x terminates, but it finds the "
                "**last** element ≤ x, i.e. the *last* occurrence. f4([3, 3, 3], 3) returns 2, "
                "not 0. **Incorrect.**\n\n"
                "Answer: f1 and f3.\n\n"
                "**Trap:** f2 passes every test where x is present — bugs at the boundaries (x "
                "beyond the maximum, empty list) are exactly what GATE questions probe."
            ),
            "verify": '''
import bisect, itertools, random
random.seed(5)
def correct(f):
    for n in range(0, 7):
        for A in itertools.combinations_with_replacement(range(4), n):
            A = list(A)
            for x in range(-1, 5):
                exp = bisect.bisect_left(A, x)
                exp = exp if exp < len(A) and A[exp] == x else -1
                try:
                    if f(A, x) != exp: return False
                except IndexError:
                    return False
    return True
res = {"A": correct(f1), "B": correct(f2), "C": correct(f3), "D": correct(f4)}
assert sorted(k for k in res if res[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "NAT", "marks": 2, "topic": "Binary search — range counting with bisect",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''from bisect import bisect_left, bisect_right

A = sorted([12, 5, 19, 5, 8, 12, 30, 12, 26, 8, 19, 41])
Q = [(5, 12), (13, 25), (8, 8), (20, 50)]
print(sum(bisect_right(A, b) - bisect_left(A, a) for a, b in Q))''',
            "answer": "14",
            "solution": (
                "**Concept.** In a sorted list, the number of elements in the closed interval "
                "[a, b] is `bisect_right(A, b) − bisect_left(A, a)`: everything before the upper "
                "bound of b minus everything strictly before a. Each query costs O(log n).\n\n"
                "Sorted A (indices 0–11): 5, 5, 8, 8, 12, 12, 12, 19, 19, 26, 30, 41.\n\n"
                "- [5, 12]: bisect_right(12) = 7, bisect_left(5) = 0 → 7.\n"
                "- [13, 25]: bisect_right(25) = 9, bisect_left(13) = 7 → 2 (the two 19s).\n"
                "- [8, 8]: bisect_right(8) = 4, bisect_left(8) = 2 → 2.\n"
                "- [20, 50]: bisect_right(50) = 12, bisect_left(20) = 9 → 3 (26, 30, 41).\n\n"
                "Total = 7 + 2 + 2 + 3 = **14**.\n\n"
                "**Trap:** using bisect_left for the upper end excludes copies of b (would give "
                "4 + 2 + 0 + 3 = 9); using bisect_right for the lower end excludes copies of a."
            ),
            "solution_diagrams": [{"type": "array",
                                   "values": [5, 5, 8, 8, 12, 12, 12, 19, 19, 26, 30, 41],
                                   "pointers": {"lo(5)": 0, "hi(12)": 7}, "highlight": [0, 1, 2, 3, 4, 5, 6],
                                   "caption": "Query [5, 12]: indices 0 … 6 counted"}],
            "verify": '''
assert int(OUTPUT) == sum(1 for a, b in Q for v in A if a <= v <= b) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "MCQ", "marks": 2, "topic": "Complexity — recursive binary search with slicing",
            "text": ("Consider the recursive Python binary search below. In the worst case (x absent) "
                     "on a sorted list of n elements, its running time is"),
            "code": '''def bs(A, x):
    if not A:
        return False
    mid = len(A) // 2
    if A[mid] == x:
        return True
    if A[mid] < x:
        return bs(A[mid + 1:], x)
    return bs(A[:mid], x)''',
            "options": [
                "Θ(log n)",
                "Θ(n log n)",
                "Θ(n)",
                "Θ(log² n)",
            ],
            "answer": "C",
            "solution": (
                "**Concept.** A Python slice `A[i:j]` creates a **new list**, copying j − i "
                "references, so it costs Θ(j − i) time, not O(1).\n\n"
                "Recurrence: each call does O(1) comparison work plus a slice of about n/2 "
                "elements, then recurses on that slice:\n"
                "T(n) = T(n/2) + Θ(n).\n\n"
                "Unrolling: c·n + c·n/2 + c·n/4 + … ≤ 2c·n → **Θ(n)**. (Master theorem: a = 1, "
                "b = 2, f(n) = n = Ω(n^{0+ε}) and regularity holds → Θ(f(n)) = Θ(n).)\n\n"
                "- (A) would be correct if the function passed indices lo, hi instead of slicing.\n"
                "- (B) would need log n levels each costing n — but the copy sizes shrink "
                "geometrically.\n"
                "- (D) has no basis here.\n\n"
                "**Trap:** the algorithm *looks* logarithmic. Extra memory is also Θ(n) in total "
                "across the recursion. Use `bisect` or index bounds for true O(log n)."
            ),
            "verify": '''
copied = [0]
def bs2(A, x):
    if not A: return False
    mid = len(A) // 2
    if A[mid] == x: return True
    if A[mid] < x:
        copied[0] += len(A) - mid - 1; return bs2(A[mid + 1:], x)
    copied[0] += mid; return bs2(A[:mid], x)
for n in (2**12, 2**16):
    copied[0] = 0; bs2(list(range(n)), n + 5)
    assert 0.9 * n <= copied[0] <= 1.1 * n
assert bs(list(range(0, 100, 3)), 51) and not bs(list(range(0, 100, 3)), 50)
assert ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MSQ", "marks": 2, "topic": "Binary search on the answer — integer square root",
            "text": ("Consider the function below, intended to compute ⌊√n⌋ for integers n ≥ 0. "
                     "Which of the following statements is/are TRUE?"),
            "code": '''def isqrt(n):
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo''',
            "options": [
                "`isqrt(99)` returns 9",
                "For every integer n ≥ 0 the function returns ⌊√n⌋",
                "If `mid` were computed as `(lo + hi) // 2`, the call `isqrt(2)` would never terminate",
                "For n = 1000 the loop body executes exactly 10 times",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Concept.** 'Binary search on the answer': the predicate P(m) = (m² ≤ n) is true "
                "for m = 0 … ⌊√n⌋ and false afterwards. The loop keeps the invariant "
                "P(lo) is true and P(hi + 1) is false, and finds the **last** true m. Because the "
                "true branch sets lo = mid, mid must be rounded **up** to guarantee progress.\n\n"
                "- (A) 9² = 81 ≤ 99 < 100 = 10². Trace: (0,99) mid 50 → hi 49; mid 25 → hi 24; "
                "mid 12 → hi 11; mid 6 → lo 6; (6,11) mid 9 → lo 9; (9,11) mid 10 → hi 9; stop → 9. "
                "**True.**\n"
                "- (B) The invariant holds initially (P(0) true; P(n + 1) false since (n+1)² > n), "
                "each branch preserves it, and every iteration shrinks hi − lo because "
                "lo < mid ≤ hi. **True** (n = 0 and n = 1 return immediately/correctly).\n"
                "- (C) With floor mid: (0,2) mid 1, 1 ≤ 2 → lo 1; (1,2) mid 1 → lo 1 again … "
                "infinite loop. **True.**\n"
                "- (D) For n = 1000 the range shrinks 1000 → 499 → 249 → … ; tracing gives "
                "**9** iterations, not 10 (result 31). **False.**\n\n"
                "**Trap:** with the floor mid the code looks fine and works for many n (e.g. n = 0, 1), "
                "but hangs whenever the final two-element range has a true lower end."
            ),
            "verify": '''
import math
assert isqrt(99) == 9
assert all(isqrt(n) == math.isqrt(n) for n in range(3000))
def it_count(n):
    lo, hi, c = 0, n, 0
    while lo < hi:
        c += 1; mid = (lo + hi + 1) // 2
        if mid * mid <= n: lo = mid
        else: hi = mid - 1
    return c
def floor_hangs(n, limit=200):
    lo, hi, c = 0, n, 0
    while lo < hi:
        c += 1
        if c > limit: return True
        mid = (lo + hi) // 2
        if mid * mid <= n: lo = mid
        else: hi = mid - 1
    return False
truth = {"A": True, "B": True, "C": floor_hangs(2), "D": it_count(1000) == 10}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MSQ", "marks": 2, "topic": "Shortest paths — Dijkstra",
            "text": ("Dijkstra's algorithm is run from P on the weighted undirected graph shown. "
                     "Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U"],
                          "edges": [["P", "Q", 5], ["P", "R", 2], ["R", "Q", 2], ["Q", "S", 4],
                                    ["R", "S", 7], ["R", "T", 9], ["S", "T", 1], ["S", "U", 6],
                                    ["T", "U", 3]],
                          "pos": {"P": [0, 1], "Q": [2, 2.4], "R": [2, -0.4], "S": [4, 2.4],
                                  "T": [4, -0.4], "U": [6, 1]}}],
            "options": [
                "The shortest-path distance from P to U is 12",
                "Vertices are finalised in the order P, R, Q, S, T, U",
                "A shortest path from P to U passes through Q",
                "The edge R–S belongs to the shortest-path tree rooted at P",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Concept.** Dijkstra finalises vertices in increasing distance; each vertex's "
                "parent in the shortest-path tree is the vertex whose relaxation last lowered it.\n\n"
                "Trace:\n"
                "- P (0): Q = 5, R = 2.\n"
                "- R (2): Q = min(5, 4) = 4 (parent R); S = 9 (parent R); T = 11 (parent R).\n"
                "- Q (4): S = min(9, 8) = 8 (parent Q).\n"
                "- S (8): T = min(11, 9) = 9 (parent S); U = 14 (parent S).\n"
                "- T (9): U = min(14, 12) = 12 (parent T).\n"
                "- U (12).\n\n"
                "Option analysis:\n"
                "- (A) **True** — d(U) = 12 via P–R–Q–S–T–U (2 + 2 + 4 + 1 + 3).\n"
                "- (B) **True** — distances 0, 2, 4, 8, 9, 12 in that order.\n"
                "- (C) **True** — the unique shortest path uses Q.\n"
                "- (D) **False** — S's parent became Q (8 < 9), so R–S is not a tree edge.\n\n"
                "**Trap:** R–S was used *temporarily* (S = 9) but a later relaxation replaced it."
            ),
            "solution_diagrams": [{"type": "graph", "directed": False,
                                   "nodes": ["P", "Q", "R", "S", "T", "U"],
                                   "edges": [["P", "Q", 5], ["P", "R", 2], ["R", "Q", 2], ["Q", "S", 4],
                                             ["R", "S", 7], ["R", "T", 9], ["S", "T", 1], ["S", "U", 6],
                                             ["T", "U", 3]],
                                   "pos": {"P": [0, 1], "Q": [2, 2.4], "R": [2, -0.4], "S": [4, 2.4],
                                           "T": [4, -0.4], "U": [6, 1]},
                                   "highlight_edges": [["P", "R"], ["R", "Q"], ["Q", "S"], ["S", "T"],
                                                       ["T", "U"]],
                                   "caption": "Shortest-path tree (red)"}],
            "verify": '''
E = [("P","Q",5),("P","R",2),("R","Q",2),("Q","S",4),("R","S",7),("R","T",9),("S","T",1),
     ("S","U",6),("T","U",3)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: 10**9 for v in G}; d["P"] = 0; par = {}; done = []
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: d[v]); done.append(u)
    for v, w in G[u]:
        if v not in done and d[u] + w < d[v]: d[v] = d[u] + w; par[v] = u
path, n = [], "U"
while n != "P": path.append(n); n = par[n]
truth = {"A": d["U"] == 12, "B": done == list("PRQSTU"), "C": "Q" in path,
         "D": par.get("S") == "R" or par.get("R") == "S"}
assert sorted(k for k in truth if truth[k]) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MCQ", "marks": 2, "topic": "Merge sort — counting comparisons",
            "text": ("Top-down merge sort (split a list of length n into the first ⌊n/2⌋ and the "
                     "remaining elements; merge by repeatedly comparing the two front elements, and "
                     "copy the leftover without comparisons once a side is empty) is applied to "
                     "[5, 2, 8, 1, 9, 3, 7, 4]. The total number of key comparisons is"),
            "options": [
                "17",
                "16",
                "18",
                "24",
            ],
            "answer": "A",
            "solution": (
                "**Concept.** Merging lists of sizes p and q costs between min(p, q) and p + q − 1 "
                "comparisons; total = sum over all merges.\n\n"
                "Level 1 (pairs):\n"
                "- [5] + [2] → [2, 5]: 1\n- [8] + [1] → [1, 8]: 1\n"
                "- [9] + [3] → [3, 9]: 1\n- [7] + [4] → [4, 7]: 1   (subtotal 4)\n\n"
                "Level 2:\n"
                "- [2, 5] + [1, 8]: 2v1→1, 2v8→2, 5v8→5, then copy 8 → 3 comparisons.\n"
                "- [3, 9] + [4, 7]: 3v4→3, 9v4→4, 9v7→7, copy 9 → 3 comparisons.   (subtotal 6)\n\n"
                "Level 3: [1, 2, 5, 8] + [3, 4, 7, 9]:\n"
                "- 1v3→1, 2v3→2, 5v3→3, 5v4→4, 5v7→5, 8v7→7, 8v9→8, copy 9 → 7 comparisons.\n\n"
                "Total = 4 + 6 + 7 = **17** → (A).\n\n"
                "- (B) 16 and (C) 18 come from mis-counting one merge.\n"
                "- (D) 24 = n log₂ n is only an upper-bound estimate; the exact worst case for n = 8 "
                "is 17 as well — this input happens to be a worst case.\n\n"
                "**Tip:** worst case for n = 2^{k} is n·k − n + 1 = 8·3 − 8 + 1 = 17."
            ),
            "verify": '''
c = [0]
def ms(a):
    if len(a) <= 1: return a
    m = len(a) // 2; L, R = ms(a[:m]), ms(a[m:]); o = []; i = j = 0
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
ms([5, 2, 8, 1, 9, 3, 7, 4])
assert c[0] == 17 and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Linked lists — binary search on a linked list",
            "text": ("A sorted singly linked list has 16 nodes holding 10, 20, 30, …, 160 (index 0 is "
                     "the head). 'Binary search' is applied with lo = 0, hi = 15 and "
                     "mid = ⌊(lo + hi)/2⌋, exactly as on an array (go right if the key at mid is "
                     "smaller than x, left if larger, stop when found or lo > hi). Reading the key at "
                     "index i is done by starting at the head and following i `next` pointers. "
                     "The total number of `next` pointers followed while searching for x = 125 "
                     "is ______."),
            "diagrams": [{"type": "linkedlist", "values": [10, 20, 30, 40, 50, 60, 70, 80, "…", 160],
                          "caption": "Sorted list (16 nodes)"}],
            "answer": "43",
            "solution": (
                "**Concept.** On a linked list there is no random access: reaching index i costs i "
                "pointer moves. Binary search still makes only O(log n) *comparisons*, but its "
                "pointer cost is Θ(n) per search — no better (here worse) than a linear scan.\n\n"
                "Trace (key at index i is 10(i + 1)):\n"
                "- lo 0, hi 15 → mid 7 (80) < 125 → lo 8. Cost 7.\n"
                "- lo 8, hi 15 → mid 11 (120) < 125 → lo 12. Cost 11.\n"
                "- lo 12, hi 15 → mid 13 (140) > 125 → hi 12. Cost 13.\n"
                "- lo 12, hi 12 → mid 12 (130) > 125 → hi 11. Cost 12. Stop (lo > hi).\n\n"
                "Total = 7 + 11 + 13 + 12 = **43** pointer moves.\n\n"
                "A linear scan would stop at 130 (index 12) after only 12 moves.\n\n"
                "**Trap:** counting comparisons (4) instead of pointer moves, or assuming each walk "
                "can continue from the previous position (that would need a backward pointer for "
                "the left moves)."
            ),
            "verify": '''
lo, hi, cost = 0, 15, 0
while lo <= hi:
    mid = (lo + hi) // 2; cost += mid; key = 10 * (mid + 1)
    if key == 125: break
    if key < 125: lo = mid + 1
    else: hi = mid - 1
assert cost == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MSQ", "marks": 2, "topic": "Graph theory — graphical degree sequences",
            "text": ("Which of the following sequences is/are the degree sequence of some **simple** "
                     "undirected graph?"),
            "options": ["3, 3, 3, 3, 3, 3", "5, 5, 4, 3, 2, 1", "4, 4, 3, 2, 2, 1", "3, 3, 3, 1"],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** Havel–Hakimi: a non-increasing sequence d₁ ≥ d₂ ≥ … is graphical iff "
                "the sequence obtained by deleting d₁ and subtracting 1 from the next d₁ terms is "
                "graphical. (Necessary first check: the sum must be even.)\n\n"
                "- (A) 3,3,3,3,3,3 (sum 18): → 2,2,2,3,3 → sort 3,3,2,2,2 → 2,1,1,2 → sort 2,2,1,1 → "
                "1,0,1 → 1,1,0 → 0,0 ✓. **Graphical** (e.g. K₃,₃ or the triangular prism).\n"
                "- (B) 5,5,4,3,2,1 (sum 20): → 4,3,2,1,0 → 2,1,0,−1 ✗. **Not graphical**: two "
                "vertices of degree 5 among 6 vertices are adjacent to everyone, so no vertex can "
                "have degree 1.\n"
                "- (C) 4,4,3,2,2,1 (sum 16): → 3,2,1,1,1 → 1,0,0,1 → 1,1,0,0 → 0,0,0 ✓. "
                "**Graphical.**\n"
                "- (D) 3,3,3,1 (sum 10): with 4 vertices a degree-3 vertex is adjacent to all "
                "others, so three such vertices force the last vertex to degree ≥ 3. HH: → 2,2,0 → "
                "1,−1 ✗. **Not graphical.**\n\n"
                "**Trap:** an even degree sum is necessary but not sufficient — (B) and (D) both "
                "have even sums."
            ),
            "verify": '''
def hh(seq):
    s = sorted(seq, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s): return False
        for i in range(d):
            s[i] -= 1
            if s[i] < 0: return False
        s.sort(reverse=True)
    return True
opts = {"A": [3]*6, "B": [5,5,4,3,2,1], "C": [4,4,3,2,2,1], "D": [3,3,3,1]}
assert sorted(k for k in opts if hh(opts[k])) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "NAT", "marks": 2, "topic": "Binary search on the answer — minimum capacity",
            "text": ("Packages with the weights below must be shipped **in the given order**, at most "
                     "D = 3 days, each day shipping a contiguous block whose total weight does not "
                     "exceed the capacity. Consider the following Python program. The value "
                     "printed is ______."),
            "code": '''def days_needed(w, cap):
    d, load = 1, 0
    for x in w:
        if load + x > cap:
            d, load = d + 1, 0
        load += x
    return d

def min_cap(w, D):
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(w, mid) <= D:
            hi = mid
        else:
            lo = mid + 1
    return lo

print(min_cap([7, 2, 5, 10, 8, 3, 6, 4], 3))''',
            "answer": "18",
            "solution": (
                "**Concept.** days_needed(cap) is non-increasing in cap, so the predicate "
                "'days_needed(cap) ≤ D' is false … false true … true. Binary search for the first "
                "true value (lower bound) between max(w) (every package must fit) and sum(w) "
                "(one day).\n\n"
                "Search on [10, 45]:\n"
                "- mid 27: greedy days [7,2,5,10] (24; +8 > 27) [8,3,6,4] (21) → 2 days ≤ 3 → hi = 27.\n"
                "- mid 18: [7,2,5] (14; +10 > 18) [10,8] (18) [3,6,4] (13) → 3 days → hi = 18.\n"
                "- mid 14: [7,2,5] [10] [8,3] [6,4] → 4 days → lo = 15.\n"
                "- mid 16: [7,2,5] [10] [8,3] … → 4 days → lo = 17.\n"
                "- mid 17: [7,2,5] [10] [8,3,6] [4] → 4 days → lo = 18. Stop: lo = hi = **18**.\n\n"
                "Check optimality: greedy packing (fill each day as far as possible) is optimal for "
                "contiguous blocks. With capacity 17 it gives [7,2,5] [10] [8,3,6] [4] = 4 days, "
                "because 10 fits neither with the first block (24) nor with 8 (18). With 18 the "
                "pair 10 + 8 fits exactly, giving 3 days.\n\n"
                "**Trap:** starting lo at 0 or 1 still works but wastes iterations; starting hi "
                "below sum(w) can miss feasible answers. Also, days_needed must start counting "
                "at 1, not 0."
            ),
            "verify": '''
w = [7, 2, 5, 10, 8, 3, 6, 4]
best = next(c for c in range(1, 100) if c >= max(w) and days_needed(w, c) <= 3)
assert best == int(ANSWER) == int(OUTPUT)
''',
        },
    ],
}
