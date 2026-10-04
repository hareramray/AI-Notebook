# Set 50 — Challenge Mock, Paper 5

SET = {
    "number": 50,
    "title": "Challenge Mock — Paper 5",
    "difficulty": "Hard",
    "focus": "hardest, multi-concept, trap-heavy 2-mark questions",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — list replication and in-place +=",
            "text": "Consider the following Python program. What is printed?",
            "code": '''grid = [[0] * 3] * 3
grid[0][1] = 5
row = grid[1]
row += [7]
print(grid[2], len(grid[0]))''',
            "options": ["`[0, 0, 0] 3`", "`[0, 5, 0] 3`", "`[0, 5, 0, 7] 4`", "`[0, 5, 0] 4`"],
            "answer": "C",
            "solution": (
                "**Concept.** `[[0] * 3] * 3` builds an outer list holding **three references to the same inner "
                "list**. For lists, `row += [7]` is `row.extend([7])` — it mutates the object in place rather "
                "than rebinding to a new list.\n\n"
                "- `grid[0][1] = 5` changes the single shared row → every “row” shows [0, 5, 0].\n"
                "- `row = grid[1]` is yet another name for that same list.\n"
                "- `row += [7]` extends it in place → [0, 5, 0, 7], visible through grid[0], grid[1], grid[2].\n\n"
                "So `grid[2]` is [0, 5, 0, 7] and `len(grid[0])` is 4 → (C).\n\n"
                "**Options.** (A) assumes independent rows. (B) assumes `+=` creates a new list (true for tuples "
                "and strings, not lists). (D) mixes the two: aliasing for the assignment but not for `+=`.\n\n"
                "**Trap:** use `[[0] * 3 for _ in range(3)]` to obtain independent rows."
            ),
            "verify": "assert OUTPUT.strip() == '[0, 5, 0, 7] 4' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — closures with nonlocal state",
            "text": "What value does the following program print?",
            "code": '''def make():
    c = 0
    def inc(k=1):
        nonlocal c
        c += k
        return c
    return inc

a, b = make(), make()
x = a() + a(3) + b(10) + a()
print(x)''',
            "answer": "20",
            "solution": (
                "**Concept.** Each call of `make()` creates a fresh local `c` and a fresh closure bound to it; "
                "`nonlocal` lets `inc` rebind that captured variable. So `a` and `b` have *independent* "
                "counters, and the state persists between calls of the same closure.\n\n"
                "Evaluated left to right:\n"
                "- `a()` → a’s c = 1 → returns **1**\n"
                "- `a(3)` → a’s c = 4 → **4**\n"
                "- `b(10)` → b’s c = 10 → **10**\n"
                "- `a()` → a’s c = 5 → **5**\n\n"
                "x = 1 + 4 + 10 + 5 = **20**.\n\n"
                "**Trap:** assuming a and b share one counter (giving 1 + 4 + 14 + 15 = 34), or that c resets "
                "to 0 on every call (giving 1 + 3 + 10 + 1 = 15). Without `nonlocal`, `c += k` would raise "
                "UnboundLocalError."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER == '20'",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "NAT", "marks": 1, "topic": "Amortised analysis — array-backed stack",
            "text": ("A stack is stored in a dynamic array whose initial capacity is 1. When a push finds the "
                     "array full, a new array of **twice** the capacity is allocated and all current elements "
                     "are copied into it before the push proceeds. Starting from an empty stack, 100 elements "
                     "are pushed (no pops). The total number of element copies caused by resizing is ______."),
            "answer": "127",
            "solution": (
                "**Concept.** A resize happens when the stack holds exactly as many elements as the capacity; "
                "it copies all of them. Capacities go 1 → 2 → 4 → … , so resizes occur at sizes 1, 2, 4, 8, "
                "16, 32, 64.\n\n"
                "- Push #2 finds 1 element (cap 1) → copy 1, cap 2.\n"
                "- Push #3: copy 2, cap 4. Push #5: copy 4, cap 8. Push #9: copy 8, cap 16.\n"
                "- Push #17: copy 16, cap 32. Push #33: copy 32, cap 64. Push #65: copy 64, cap 128.\n"
                "- Pushes 66–100 fit in capacity 128.\n\n"
                "Total copies = 1 + 2 + 4 + 8 + 16 + 32 + 64 = **127** (< 2·100), so each push costs O(1) "
                "amortised.\n\n"
                "**Trap:** including a resize at 128 (no — only 100 elements are pushed) or counting the 100 "
                "ordinary writes as copies."
            ),
            "verify": '''
cap, size, copies = 1, 0, 0
for _ in range(100):
    if size == cap: copies += size; cap *= 2
    size += 1
assert copies == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MCQ", "marks": 1, "topic": "Heaps — where can the k-th smallest be?",
            "text": ("A binary min-heap stores 31 distinct keys in a complete binary tree (root at level 0, "
                     "leaves at level 4). At which levels can the **4th smallest** key be located (over all "
                     "possible such heaps)?"),
            "options": ["Levels 1, 2 and 3 only", "Levels 2 and 3 only", "Levels 1, 2, 3 and 4",
                        "Level 3 only"],
            "answer": "A",
            "solution": (
                "**Concept.** Every ancestor of a key in a min-heap is smaller than it. The 4th smallest has at "
                "most 3 smaller keys, so it has at most 3 ancestors → level ≤ 3. It cannot be the root (that is "
                "the minimum), so its level is ≥ 1.\n\n"
                "All three levels are achievable:\n"
                "- **Level 1:** root 1, children 2 and 4, with 3 below 2 → 4 is a child of the root.\n"
                "- **Level 2:** e.g. the chain 1 → 2 → 4 with 3 as the other child of the root.\n"
                "- **Level 3:** the chain 1 → 2 → 3 → 4 down the leftmost path.\n\n"
                "Level 4 is impossible (it would need 4 smaller ancestors). Answer → (A).\n\n"
                "**Options.** (B) wrongly excludes level 1 (see the first example). (C) includes level 4. (D) "
                "confuses “can be” with “must be”.\n\n"
                "**Tip:** the k-th smallest lies at a level between 1 and k − 1 (for k ≥ 2); hence finding it "
                "only requires inspecting the top k − 1 levels."
            ),
            "verify": '''
import random, math
def heapify(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        j = i
        while True:
            l, r, m = 2 * j + 1, 2 * j + 2, j
            if l < n and a[l] < a[m]: m = l
            if r < n and a[r] < a[m]: m = r
            if m == j: break
            a[j], a[m] = a[m], a[j]; j = m
    return a
random.seed(7); lv = set()
for _ in range(6000):
    a = list(range(31)); random.shuffle(a); heapify(a)
    lv.add(int(math.log2(a.index(3) + 1)))
assert lv == {1, 2, 3} and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MSQ", "marks": 1, "topic": "BSTs — insertion orders giving the same tree",
            "text": ("The sequence 6, 3, 9, 1, 5, 8, 4 is inserted into an empty BST (no rebalancing), giving the "
                     "tree T shown. Which of the following insertion sequences produce **exactly the same "
                     "tree** T?"),
            "diagrams": [{"type": "bintree", "tree": [6, [3, [1], [5, [4], None]], [9, [8], None]],
                          "caption": "Tree T"}],
            "options": ["6, 9, 3, 8, 1, 5, 4", "6, 3, 1, 9, 4, 5, 8", "6, 3, 5, 4, 9, 1, 8",
                        "6, 8, 9, 3, 5, 1, 4"],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** A sequence produces T iff every node is inserted **after all of its ancestors** "
                "in T. Unrelated subtrees may be interleaved freely.\n\n"
                "Ancestor constraints in T: 6 first; 3 and 9 after 6; 1 and 5 after 3; 4 after 5; 8 after 9.\n\n"
                "- (A) 6, 9, 3, 8, 1, 5, 4: all constraints hold (8 after 9, 4 after 5). **Yes.**\n"
                "- (B) 4 comes before 5 → 4 becomes the right child of 3 and 5 then goes under 4. **No.**\n"
                "- (C) 6, 3, 5, 4, 9, 1, 8: 5 after 3, 4 after 5, 1 after 3, 8 after 9. **Yes.**\n"
                "- (D) 8 is inserted before 9 → 8 becomes the right child of 6. **No.**\n\n"
                "(For the record, the number of insertion orders producing T is C(6, 2) × 3 = 45: choose the "
                "positions of the right subtree {9, 8} among the 6 non-root slots, and interleave {1} with the "
                "chain 5 → 4 after 3 in 3 ways.)\n\n"
                "**Trap:** checking only that each element lands on the correct *side* of the root — the "
                "constraint must hold at every level."
            ),
            "verify": '''
import itertools
def ins(t, k):
    if t is None: return [k, None, None]
    i = 1 if k < t[0] else 2; t[i] = ins(t[i], k); return t
def bst(seq):
    t = None
    for k in seq: t = ins(t, k)
    return t
T = bst([6, 3, 9, 1, 5, 8, 4])
opts = [[6,9,3,8,1,5,4], [6,3,1,9,4,5,8], [6,3,5,4,9,1,8], [6,8,9,3,5,1,4]]
assert [L for L, s in zip('ABCD', opts) if bst(s) == T] == sorted(ANSWER)
assert sum(bst(p) == T for p in itertools.permutations([6,3,9,1,5,8,4])) == 45
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — termination bug",
            "text": ("The following binary search contains a bug. For `a = [2, 4, 6, 8, 10]`, which of the "
                     "following calls **terminates**?"),
            "code": '''def search(a, x):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[mid] < x:
            lo = mid
        else:
            hi = mid - 1
    return -1''',
            "run_code": False,
            "options": ["`search(a, 1)`", "`search(a, 4)`", "`search(a, 7)`", "`search(a, 10)`"],
            "answer": "A",
            "solution": (
                "**Concept.** `lo = mid` (instead of `mid + 1`) makes no progress when hi = lo or hi = lo + 1, "
                "because then mid = lo. If at that moment a[mid] < x, the loop repeats forever.\n\n"
                "- (A) x = 1: mid 2 (6 > 1) → hi = 1; mid 0 (2 > 1) → hi = −1; loop ends → returns −1. "
                "**Terminates.**\n"
                "- (B) x = 4: mid 2 (6 > 4) → hi = 1; mid 0 (2 < 4) → lo = 0 → mid 0 again … **infinite**, "
                "even though 4 is present (it sits at index 1 = hi, never reached as mid).\n"
                "- (C) x = 7: lo → 2 (6 < 7); mid 3 (8 > 7) → hi = 2; mid 2 (6 < 7) → lo = 2 … **infinite**.\n"
                "- (D) x = 10: lo → 2, then lo → 3; with (lo, hi) = (3, 4), mid = 3 and 8 < 10 forever. "
                "**Infinite.**\n\n"
                "**Trap:** the bug is only triggered on the right-moving branch, so searches that keep going "
                "left (like x = 1) or hit the key at a probed mid (6, 8, 2) still work — testing a few lucky "
                "inputs does not expose it."
            ),
            "verify": '''
def capped(a, x, cap=100):
    lo, hi, it = 0, len(a) - 1, 0
    while lo <= hi:
        it += 1
        if it > cap: return None
        mid = (lo + hi) // 2
        if a[mid] == x: return mid
        if a[mid] < x: lo = mid
        else: hi = mid - 1
    return -1
a = [2, 4, 6, 8, 10]
term = [capped(a, x) is not None for x in (1, 4, 7, 10)]
assert term == [True, False, False, False] and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — expected number of empty slots",
            "text": ("Six keys are inserted into a hash table with 10 slots using separate chaining. Assume "
                     "simple uniform hashing: each key independently hashes to each slot with probability 1/10. "
                     "The expected number of slots that remain **empty** is ______ "
                     "(rounded off to two decimal places)."),
            "answer": ["5.30", "5.32"],
            "solution": (
                "**Concept.** Use linearity of expectation with an indicator per slot: I_{s} = 1 if slot s is "
                "empty after all insertions.\n\n"
                "- P(a given key avoids slot s) = 9/10.\n"
                "- Keys are independent, so P(slot s empty) = (9/10)^{6} = 0.531441.\n"
                "- E[number of empty slots] = Σ_{s} P(I_{s} = 1) = 10 × 0.531441 = **5.31441 ≈ 5.31**.\n\n"
                "(Equivalently, the expected number of *occupied* slots is 10 − 5.31 = 4.69 < 6, reflecting "
                "collisions; the expected number of colliding pairs is C(6, 2)/10 = 1.5.)\n\n"
                "**Trap:** answering 10 − 6 = 4 assumes no collisions; using (1 − 6/10) × 10 = 4 makes the "
                "same mistake. Indicators avoid any need for the (dependent) joint distribution."
            ),
            "verify": '''
from fractions import Fraction
dp = {0: Fraction(1)}
for _ in range(6):
    nd = {}
    for k, p in dp.items():
        nd[k] = nd.get(k, 0) + p * Fraction(k, 10)
        nd[k + 1] = nd.get(k + 1, 0) + p * Fraction(10 - k, 10)
    dp = nd
e = float(sum(p * (10 - k) for k, p in dp.items()))
assert float(ANSWER[0]) <= e <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Sorting — behaviour on all-equal keys",
            "text": ("An array of n keys that are **all equal** is sorted. Which of the following statements "
                     "is/are TRUE? (Insertion sort shifts while `A[j] > key`; bubble sort has an early-exit "
                     "flag; quicksort uses the stated partition scheme recursively.)"),
            "options": [
                "Insertion sort performs Θ(n) comparisons",
                "Quicksort with the Lomuto partition (last element as pivot, moving elements ≤ pivot left) "
                "performs Θ(n²) comparisons",
                "Quicksort with the Hoare partition (first element as pivot) performs Θ(n²) comparisons",
                "Bubble sort with early exit performs n(n − 1)/2 comparisons",
            ],
            "answer": ["A", "B"],
            "solution": (
                "- (A) Each key compares once with its left neighbour, finds it not greater, and stops: n − 1 "
                "comparisons. **TRUE.**\n"
                "- (B) Lomuto: every element satisfies `≤ pivot`, so the pivot ends at the right end; the "
                "recursion continues on n − 1 elements, then n − 2, … → n(n − 1)/2 = Θ(n²). **TRUE.**\n"
                "- (C) Hoare: both scans stop at *every* element equal to the pivot, so i and j advance in "
                "lock-step and meet in the middle — each partition splits the range roughly in half → "
                "Θ(n log n), not Θ(n²). **FALSE.**\n"
                "- (D) The first pass makes no swap, so the algorithm stops after n − 1 comparisons. "
                "**FALSE.**\n\n"
                "**Trap:** “quicksort is quadratic on equal keys” is true for Lomuto but *not* for Hoare — "
                "the stop-on-equal rule is precisely what balances Hoare’s splits."
            ),
            "verify": '''
import sys
sys.setrecursionlimit(10000)
def lomuto(n):
    a = [7] * n; c = [0]
    def qs(lo, hi):
        if lo < hi:
            p, i = a[hi], lo - 1
            for j in range(lo, hi):
                c[0] += 1
                if a[j] <= p: i += 1; a[i], a[j] = a[j], a[i]
            a[i + 1], a[hi] = a[hi], a[i + 1]; qs(lo, i); qs(i + 2, hi)
    qs(0, n - 1); return c[0]
def hoare(n):
    a = [7] * n; c = [0]
    def part(lo, hi):
        p, i, j = a[lo], lo - 1, hi + 1
        while True:
            i += 1; c[0] += 1
            while a[i] < p: i += 1; c[0] += 1
            j -= 1; c[0] += 1
            while a[j] > p: j -= 1; c[0] += 1
            if i >= j: return j
            a[i], a[j] = a[j], a[i]
    def qs(lo, hi):
        if lo < hi:
            q = part(lo, hi); qs(lo, q); qs(q + 1, hi)
    qs(0, n - 1); return c[0]
okB = lomuto(256) == 256 * 255 // 2
okC = hoare(512) / hoare(256) > 3.5          # quadratic would give ~4
assert okB and not okC and sorted(ANSWER) == ['A', 'B']
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Graph theory — edges vs components",
            "text": ("The maximum number of edges in a simple undirected graph with 10 vertices and exactly 3 "
                     "connected components is"),
            "options": ["36", "28", "27", "21"],
            "answer": "B",
            "solution": (
                "**Concept.** With the component sizes n₁ + n₂ + n₃ = 10 fixed, the edge count is maximised by "
                "making each component complete: Σ C(nᵢ, 2). Since C(x, 2) is convex, the sum is largest when "
                "the sizes are as **unequal** as possible: 8, 1, 1.\n\n"
                "- Sizes (8, 1, 1): C(8, 2) = **28**.\n"
                "- Sizes (7, 2, 1): 21 + 1 = 22. Sizes (4, 3, 3): 6 + 3 + 3 = 12. All smaller.\n\n"
                "General formula: (n − k)(n − k + 1)/2 = 7 · 8/2 = 28 for n = 10, k = 3 → (B).\n\n"
                "**Options.** (A) 36 = C(9, 2) is the answer for **2** components. (C) 27 subtracts one edge "
                "per extra component from 28 — no basis. (D) 21 = C(7, 2) uses n − k = 7 vertices in the big "
                "component, an off-by-one.\n\n"
                "**Trap:** balancing the components (the intuition for *minimising* edges) is exactly wrong "
                "here."
            ),
            "verify": '''
best = max(a*(a-1)//2 + b*(b-1)//2 + c*(c-1)//2
           for a in range(1, 9) for b in range(1, 9) for c in range(1, 9) if a + b + c == 10)
assert best == 28 and ANSWER == 'B'
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "NAT", "marks": 1, "topic": "Linked lists — Floyd’s cycle detection",
            "text": ("A singly linked list has nodes with values 11, 22, 33, 44, 55, 66, 77, 88, 99 in order, "
                     "and the `nxt` pointer of the last node (99) points back to the node 55. The function below "
                     "is called with the head (11). What is the value of `s1 + s2` it returns (as the first "
                     "component)?"),
            "code": '''def floyd(head):
    slow = fast = head
    s1 = 0
    while True:
        slow, fast = slow.nxt, fast.nxt.nxt
        s1 += 1
        if slow is fast:
            break
    p, s2 = head, 0
    while p is not slow:
        p, slow = p.nxt, slow.nxt
        s2 += 1
    return s1 + s2, p.v''',
            "diagrams": [{"type": "linkedlist", "values": [11, 22, 33, 44, 55, 66, 77, 88, 99], "head": "head",
                          "caption": "The last node’s nxt points back to 55 (not drawn)"}],
            "answer": "9",
            "solution": (
                "**Concept.** Tail length μ = 4 (11, 22, 33, 44 are outside the cycle) and cycle length λ = 5 "
                "(55 → 66 → 77 → 88 → 99 → 55). After the meeting, moving one pointer from the head and one "
                "from the meeting point at equal speed makes them meet at the cycle start after exactly μ "
                "steps.\n\n"
                "Phase 1 (positions as indices 0–8; index 8 → 4):\n"
                "- step 1: slow 1, fast 2; step 2: slow 2, fast 4; step 3: slow 3, fast 6;\n"
                "- step 4: slow 4, fast 8; step 5: slow 5, fast 4 → 5 (8 → 4 → 5). Meet at index 5 (66) → "
                "s1 = **5**.\n\n"
                "Phase 2: p from index 0, slow from 5 → after 4 steps p = 4 and slow = 5 → 6 → 7 → 8 → 4. "
                "Meet at 55 → s2 = **4** = μ.\n\n"
                "Return value (9, 55); s1 + s2 = **9**.\n\n"
                "Check: the first meeting occurs after s1 steps where s1 is the smallest multiple of λ that is "
                "≥ μ → s1 = 5.\n\n"
                "**Trap:** assuming the pointers meet at the cycle start in phase 1 (they meet at 66, one step "
                "past it)."
            ),
            "verify": '''
class Node:
    def __init__(s, v): s.v, s.nxt = v, None
ns = [Node(v) for v in [11, 22, 33, 44, 55, 66, 77, 88, 99]]
for a_, b_ in zip(ns, ns[1:]): a_.nxt = b_
ns[-1].nxt = ns[4]
assert floyd(ns[0]) == (int(ANSWER), 55)
''',
        },
        # ============================================================ 2-mark
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — class vs instance attributes, inheritance",
            "text": "Consider the following Python program. What is printed?",
            "code": '''class A:
    tags = []
    n = 0
    def __init__(self, t):
        self.tags.append(t)
        self.n += 1

class B(A):
    tags = []
    def __init__(self, t):
        super().__init__(t)
        self.tags = self.tags + [t * 2]

x, y, z = A(1), B(2), B(3)
print(A.tags, B.tags, z.tags, A.n + z.n)''',
            "options": ["`[1, 2, 3] [2, 3] [2, 3, 6] 3`", "`[1] [2, 3, 4, 6] [2, 3, 6] 1`",
                        "`[1] [2, 3] [2, 3, 6] 3`", "`[1] [2, 3] [2, 3, 6] 1`"],
            "answer": "D",
            "solution": (
                "**Concept.** Attribute *lookup* on an instance falls back to the class (and its bases), but "
                "attribute *assignment* on an instance always creates/overwrites an instance attribute. "
                "Mutating a found class attribute (`append`) changes the class-level object.\n\n"
                "- `A(1)`: `self.tags` finds `A.tags` → append 1 → A.tags = [1]. `self.n += 1` reads A.n (0) "
                "and **creates** x.n = 1; A.n stays 0.\n"
                "- `B(2)`: inside A.__init__, `self.tags` now finds **B.tags** (B overrides it) → B.tags = [2]; "
                "y.n = 1. Then `self.tags = self.tags + [4]` builds a *new* list [2, 4] as y’s instance "
                "attribute — B.tags is unchanged.\n"
                "- `B(3)`: `self.tags` (no instance attribute yet) finds B.tags → B.tags = [2, 3]; then "
                "z.tags = [2, 3] + [6] = [2, 3, 6]; z.n = 1.\n\n"
                "Printed: A.tags = [1], B.tags = [2, 3], z.tags = [2, 3, 6], A.n + z.n = 0 + 1 = 1 → (D).\n\n"
                "Option by option:\n"
                "- (A) assumes B shares A’s list and that n is a shared counter.\n"
                "- (B) assumes `self.tags = self.tags + …` mutates the class list (it rebinds).\n"
                "- (C) assumes `self.n += 1` increments the class attribute A.n.\n"
                "- (D) Correct.\n\n"
                "**Trap:** `self.x += 1` on an immutable class attribute silently creates an instance copy, "
                "while `self.lst.append(…)` on a mutable class attribute is shared by every instance."
            ),
            "verify": "assert OUTPUT.strip() == '[1] [2, 3] [2, 3, 6] 1' and ANSWER == 'D'",
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Monotonic deque — sliding-window maximum",
            "text": ("The function below returns the maximum of every window of k consecutive elements using a "
                     "deque of indices. For the array shown and k = 3, the sum of all the window maxima returned "
                     "is ______."),
            "code": '''from collections import deque
def win_max(a, k):
    dq, out = deque(), []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(a[dq[0]])
    return out''',
            "diagrams": [{"type": "array", "values": [4, 2, 12, 3, 8, 5, 1, 9, 6, 7], "label": "a"}],
            "answer": "79",
            "solution": (
                "**Concept.** The deque holds indices whose values are strictly decreasing from front to back; "
                "the front is the current window maximum. An index leaves from the back when a larger-or-equal "
                "value arrives and from the front when it slides out of the window. Each index enters and "
                "leaves at most once → Θ(n).\n\n"
                "Trace (deque shown as values):\n"
                "- i=0..2: 4; 2 → [4, 2]; 12 pops both → [12]. Window [4, 2, 12] → **12**.\n"
                "- i=3 (3): [12, 3] → **12**. i=4 (8): pop 3 → [12, 8] → **12** (index 2 still inside).\n"
                "- i=5 (5): [12, 8, 5]; index 2 ≤ 5 − 3 → popleft 12 → [8, 5] → **8**.\n"
                "- i=6 (1): [8, 5, 1] → **8**.\n"
                "- i=7 (9): pops 1, 5, 8 → [9] → **9**.\n"
                "- i=8 (6): [9, 6] → **9**. i=9 (7): pop 6 → [9, 7] → **9**.\n\n"
                "Maxima: 12, 12, 12, 8, 8, 9, 9, 9 → sum = **79**.\n\n"
                "**Trap:** forgetting to expire 12 at i = 5 (giving 12 instead of 8 for the window [3, 8, 5]), "
                "or counting n − k = 7 windows instead of n − k + 1 = 8."
            ),
            "verify": '''
a = [4, 2, 12, 3, 8, 5, 1, 9, 6, 7]
brute = [max(a[i:i + 3]) for i in range(len(a) - 2)]
assert win_max(a, 3) == brute and sum(brute) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Stack permutations — one stack vs two stacks in series",
            "text": ("The input 1, 2, 3, 4 (in this order) must be output as a permutation. In the **single "
                     "stack** model each input value is pushed onto S and values are popped from S to the output. "
                     "In the **two stacks in series** model the allowed moves are: push the next input onto S1; "
                     "move the top of S1 onto S2; pop the top of S2 to the output. Which of the following "
                     "statements is/are TRUE?"),
            "diagrams": [{"type": "stack", "values": [1, 2, 3], "label": "S1"},
                         {"type": "stack", "values": [], "label": "S2"}],
            "options": [
                "Every permutation of 1, 2, 3, 4 can be produced with two stacks in series",
                "Exactly 14 permutations of 1, 2, 3, 4 can be produced with a single stack",
                "The output 4 1 3 2 can be produced with a single stack",
                "The output 2 4 3 1 can be produced with a single stack",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Single stack.** The achievable outputs of 1..n are counted by the Catalan number "
                "C_{n} = (2n)!/((n+1)! n!), so for n = 4 there are **14** → (B) **TRUE**. A permutation is "
                "achievable iff it avoids the pattern “3 1 2” (some c … a … b with a < b < c).\n"
                "- (C) 4 1 3 2: when 4 is output, 1, 2, 3 are on the stack with 3 on top, so 1 cannot come "
                "next (4 1 3 is a 312-pattern). **FALSE.**\n"
                "- (D) 2 4 3 1: push 1, 2 pop 2; push 3, 4 pop 4; pop 3; pop 1. **TRUE.**\n\n"
                "**Two stacks in series.** S2 can hold a value while S1 keeps accepting input, which lets the "
                "machine undo the single-stack obstruction. For example, the 312-type output 4 1 3 2:\n"
                "- push 1, push 2; move 2 → S2 (S1 = [1], S2 = [2])\n"
                "- push 3, push 4; move 4 → S2 and output **4**\n"
                "- move 3 → S2, move 1 → S2 (S2 = [2, 3, 1], top 1)\n"
                "- output **1**, **3**, **2**.\n"
                "An exhaustive search over all move sequences (see the verify code) confirms that all 24 "
                "permutations of 1..4 are reachable → (A) **TRUE**.\n\n"
                "**Trap:** assuming two stacks behave like one bigger stack; the transfer step adds genuine "
                "reordering power."
            ),
            "verify": '''
import itertools
def single(n):
    res = set()
    def rec(nxt, s, out):
        if len(out) == n: res.add(tuple(out)); return
        if nxt <= n: rec(nxt + 1, s + [nxt], out)
        if s: rec(nxt, s[:-1], out + [s[-1]])
    rec(1, [], []); return res
def series(n):
    res = set()
    def rec(nxt, s1, s2, out):
        if len(out) == n: res.add(tuple(out)); return
        if nxt <= n: rec(nxt + 1, s1 + [nxt], s2, out)
        if s1: rec(nxt, s1[:-1], s2 + [s1[-1]], out)
        if s2: rec(nxt, s1, s2[:-1], out + [s2[-1]])
    rec(1, [], [], []); return res
S1, S2 = single(4), series(4)
res = [len(S2) == 24, len(S1) == 14, (4, 1, 3, 2) in S1, (2, 4, 3, 1) in S1]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Quicksort — counting worst-case inputs",
            "text": ("Quicksort with the Lomuto partition (last element as pivot; every element of the current "
                     "range other than the pivot is compared with the pivot exactly once) is run on each of the "
                     "120 permutations of 1, 2, 3, 4, 5. The maximum possible total number of comparisons is 10. "
                     "On how many of the 120 permutations is this maximum attained?"),
            "code": '''def quicksort(A, lo, hi):
    if lo < hi:
        p, i = A[hi], lo - 1
        for j in range(lo, hi):
            if A[j] <= p:          # one comparison
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]
        quicksort(A, lo, i)
        quicksort(A, i + 2, hi)''',
            "run_code": False,
            "answer": "16",
            "solution": (
                "**Concept.** A call on m elements costs m − 1 comparisons. The total reaches "
                "4 + 3 + 2 + 1 = 10 only if **every** partition leaves one side empty, i.e. the pivot (last "
                "element of the current range) is the minimum or maximum of that range.\n\n"
                "Count level by level:\n"
                "- Top level: A[4] must be 1 or 5 → **2** choices.\n"
                "- If the pivot is the maximum, every element is ≤ pivot, each swap is a self-swap, and the "
                "remaining 4 elements keep their order. If the pivot is the minimum, nothing is ≤ pivot and "
                "the final swap exchanges A[lo] with the pivot, so the remaining range is "
                "A[lo+1..hi−1] followed by the old A[lo]. In both cases the new range is a **fixed, "
                "invertible rearrangement** of the other 4 elements.\n"
                "- Hence, given the top-level choice, the number of good arrangements of the remaining 4 "
                "elements equals the number of worst-case permutations of size 4, and so on.\n\n"
                "W(1) = 1, W(m) = 2·W(m − 1) → W(5) = 2^{4} = **16**.\n\n"
                "Example: 2 3 4 1 5. Pivot 5 (max) → range 2 3 4 1, pivot 1 (min) → swap gives 1 | 3 4 2, "
                "pivot 2 (min) → 2 | 4 3, pivot 3 (min) → 3 | 4. Total 4 + 3 + 2 + 1 = 10 ✓.\n\n"
                "**Trap:** assuming only the sorted and reverse-sorted inputs are worst cases (2 permutations); "
                "or assuming “pivot is extreme” must hold in the *original* array positions — Lomuto’s swaps "
                "move elements, so the condition is on the rearranged subarray."
            ),
            "verify": '''
import itertools
def comps(p):
    A = list(p); c = [0]
    def qs(lo, hi):
        if lo < hi:
            pv, i = A[hi], lo - 1
            for j in range(lo, hi):
                c[0] += 1
                if A[j] <= pv: i += 1; A[i], A[j] = A[j], A[i]
            A[i + 1], A[hi] = A[hi], A[i + 1]; qs(lo, i); qs(i + 2, hi)
    qs(0, len(A) - 1); return c[0]
cs = [comps(p) for p in itertools.permutations(range(1, 6))]
assert max(cs) == 10 and cs.count(10) == int(ANSWER) and comps((2, 3, 4, 1, 5)) == 10
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Complexity — dependent logarithmic loops",
            "text": "For n a power of 2, what is the order of the value returned by `f(n)` (equivalently, its running time)?",
            "code": '''def f(n):
    c = 0
    i = n
    while i > 1:
        j = i
        while j < n:
            j *= 2
            c += 1
        i //= 2
    return c''',
            "options": ["Θ(log n)", "Θ(log² n)", "Θ(n)", "Θ(n log n)"],
            "answer": "B",
            "solution": (
                "**Concept.** Count inner iterations per outer iteration. Let n = 2^{k}. The outer loop takes "
                "i = 2^{k}, 2^{k−1}, …, 2^{1} (k iterations). For i = 2^{t}, the inner loop doubles j from 2^{t} "
                "up to 2^{k}: exactly k − t iterations.\n\n"
                "Total c = Σ_{t=1}^{k} (k − t) = 0 + 1 + … + (k − 1) = k(k − 1)/2.\n\n"
                "For n = 1024 (k = 10): c = 45; for n = 2^{20}: c = 190. With k = log₂ n, "
                "c = Θ(log² n) → (B).\n\n"
                "**Options.** (A) multiplies the *counts* incorrectly by treating the inner loop as O(1). "
                "(C)/(D) treat one of the loops as linear — but both variables move geometrically.\n\n"
                "**Trap:** the inner loop starts at the current i (not at 1), so it is short when i is large "
                "and long when i is small; the sum is an arithmetic series in k."
            ),
            "verify": '''
assert [f(2 ** k) for k in (10, 20, 30)] == [k * (k - 1) // 2 for k in (10, 20, 30)]
assert ANSWER == 'B'
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "Dijkstra with a negative edge",
            "text": ("Dijkstra’s algorithm is run from S on the directed graph below, which has one negative edge "
                     "but no negative cycle. The implementation marks a vertex *final* when it is extracted "
                     "(minimum d among non-final vertices) and relaxes an edge (u, v) only if v is not yet final. "
                     "The number of vertices whose final d-value differs from the true shortest-path distance "
                     "is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "T", "D"],
                          "edges": [["S", "A", 7], ["S", "B", 3], ["A", "C", -5], ["B", "C", 1], ["C", "T", 2],
                                    ["C", "D", 5], ["T", "D", 2]],
                          "pos": {"S": [0, 1], "A": [2, 2.2], "B": [2, -0.2], "C": [4, 1], "T": [6, 2.2],
                                  "D": [6, -0.2]}}],
            "answer": "3",
            "solution": (
                "**Dijkstra run** (extraction order with d-values):\n"
                "- S (0): A = 7, B = 3.\n"
                "- B (3): C = 4.\n"
                "- C (4): T = 6, D = 9.\n"
                "- T (6): D = min(9, 8) = 8.\n"
                "- A (7): edge A→C (−5) would give 2, but C is already final → **skipped**.\n"
                "- D (8).\n"
                "Reported: S 0, A 7, B 3, C 4, T 6, D 8.\n\n"
                "**True distances** (e.g. Bellman–Ford): C = min(3 + 1, 7 − 5) = **2**, T = 2 + 2 = **4**, "
                "D = min(2 + 5, 4 + 2) = **6**; S, A, B are unchanged (0, 7, 3).\n\n"
                "Wrong vertices: C, T and D → **3**.\n\n"
                "**Concept.** Dijkstra’s correctness relies on the fact that a path can only get longer when "
                "extended; a negative edge into an already-final vertex breaks this, and the error propagates "
                "to everything downstream of that vertex.\n\n"
                "**Trap:** counting only C (the head of the negative edge) — T and D inherit the mistake."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Reported vs true distances",
                                   "col_labels": ["S", "A", "B", "C", "T", "D"],
                                   "row_labels": ["Dijkstra", "true"],
                                   "rows": [[0, 7, 3, 4, 6, 8], [0, 7, 3, 2, 4, 6]],
                                   "highlight": [[0, 3], [0, 4], [0, 5]]}],
            "verify": '''
G = {'S': [('A', 7), ('B', 3)], 'A': [('C', -5)], 'B': [('C', 1)],
     'C': [('T', 2), ('D', 5)], 'T': [('D', 2)], 'D': []}
INF = float('inf'); d = {v: INF for v in G}; d['S'] = 0; fin = set()
while len(fin) < len(G):
    u = min((v for v in G if v not in fin), key=lambda v: d[v]); fin.add(u)
    for v, w in G[u]:
        if v not in fin and d[u] + w < d[v]: d[v] = d[u] + w
bf = {v: INF for v in G}; bf['S'] = 0
for _ in range(len(G)):
    for u in G:
        for v, w in G[u]:
            if bf[u] + w < bf[v]: bf[v] = bf[u] + w
assert sum(d[v] != bf[v] for v in G) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "Graph structure — bipartiteness, cut vertices, BFS levels",
            "text": "Consider the undirected graph below. Which of the following statements is/are TRUE?",
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["C", "E"], ["E", "F"],
                                    ["F", "G"], ["G", "H"], ["H", "E"]],
                          "pos": {"A": [0, 1], "B": [1, 2], "C": [2, 1], "D": [1, 0], "E": [3.5, 1],
                                  "F": [4.5, 2], "G": [5.5, 1], "H": [4.5, 0]}}],
            "options": [
                "The graph is bipartite",
                "The graph has exactly one cut vertex",
                "A BFS from A assigns vertices to exactly 6 distinct levels (level 0 to level 5)",
                "Every spanning tree of the graph contains the edge C–E",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "- (A) The only cycles are A-B-C-D-A and E-F-G-H-E, both of length 4 (even). A graph is "
                "bipartite iff it has no odd cycle → 2-colouring {A, C, F, H} vs {B, D, E, G}. **TRUE.**\n"
                "- (B) Removing C separates {A, B, D} from {E, F, G, H}; removing E separates {A, B, C, D} from "
                "{F, G, H}. No other vertex disconnects the graph. **Two** cut vertices → **FALSE.**\n"
                "- (C) BFS from A: level 0 {A}, 1 {B, D}, 2 {C}, 3 {E}, 4 {F, H}, 5 {G} → 6 levels. **TRUE.**\n"
                "- (D) C–E is a **bridge** (its removal disconnects the graph), and every spanning tree must "
                "contain every bridge. **TRUE.**\n\n"
                "**Concept recap.** A vertex is a cut vertex iff removing it increases the number of components; "
                "an edge lies in every spanning tree iff it is a bridge (it lies on no cycle).\n\n"
                "**Trap:** in (B), noticing only the bridge’s one endpoint — *both* endpoints of a bridge are "
                "cut vertices whenever each has degree ≥ 2."
            ),
            "verify": '''
from collections import deque
E = "AB BC CD DA CE EF FG GH HE".split()
G = {}
for u, v in E: G.setdefault(u, set()).add(v); G.setdefault(v, set()).add(u)
def ncomp(skip=None, skip_edge=None):
    seen, c = set(), 0
    for s in G:
        if s == skip or s in seen: continue
        c += 1; st = [s]; seen.add(s)
        while st:
            u = st.pop()
            for v in G[u]:
                if v == skip or v in seen or {u, v} == skip_edge: continue
                seen.add(v); st.append(v)
    return c
col = {'A': 0}; lvl = {'A': 0}; q = deque('A'); bip = True
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in col: col[v] = 1 - col[u]; lvl[v] = lvl[u] + 1; q.append(v)
        elif col[v] == col[u]: bip = False
cuts = [v for v in G if ncomp(skip=v) > 1]
res = [bip, len(cuts) == 1, len(set(lvl.values())) == 6, ncomp(skip_edge={'C', 'E'}) > 1]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Heaps — counting heaps with a constraint",
            "text": ("Consider all array-based binary **min-heaps** that store exactly the keys 1, 2, …, 7 (so "
                     "the tree is a perfect binary tree of height 2). In how many of them is key 2 the **left** "
                     "child of the root?"),
            "diagrams": [{"type": "heap", "values": [1, 2, 5, 3, 4, 6, 7],
                          "caption": "One such heap (2 is the left child of the root)"}],
            "answer": "40",
            "solution": (
                "**Concept.** Count heaps recursively: the root must be the minimum; the remaining keys are "
                "split between the two subtrees, and each subtree must itself be a heap. For a 3-node subtree "
                "with a fixed set of keys, the smallest is its root and the other two can be arranged in "
                "2 ways.\n\n"
                "- Root = 1 (forced).\n"
                "- Key 2 is the left child, so 2 is the root of the left 3-node subtree. Its two children are "
                "any 2 of the remaining keys {3, 4, 5, 6, 7}: C(5, 2) = **10** choices, arranged in **2** "
                "orders.\n"
                "- The other 3 keys form the right subtree: its minimum is the root, and the other two can be "
                "ordered in **2** ways.\n\n"
                "Total = 10 × 2 × 2 = **40**.\n\n"
                "Cross-check: the total number of min-heaps on 7 keys is C(6, 3) × 2 × 2 = 80, and by symmetry "
                "key 2 (which must be a child of the root) is the left child in exactly half of them → 40 ✓.\n\n"
                "**Trap:** forgetting that the left subtree’s children may appear in either order (giving 20), "
                "or requiring 3 to be the right child of the root (it need not be — 3 can sit under 2)."
            ),
            "verify": '''
import itertools
tot = cnt = 0
for p in itertools.permutations(range(1, 8)):
    if all(p[(i - 1) // 2] < p[i] for i in range(1, 7)):
        tot += 1; cnt += p[1] == 2
assert tot == 80 and cnt == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Python — dict ordering, update and truthiness",
            "text": "Consider the following Python program. What is printed?",
            "code": '''d = {'b': 1, 'a': 2, 'c': 3}
d['a'] = 5
del d['b']
d['b'] = 7
d.update(c=0, e=9)
k = [x for x in d if d[x]]
print(k, sorted(d, key=d.get)[0], list(d.items())[1])''',
            "options": ["`['a', 'c', 'b', 'e'] c ('c', 0)`", "`['b', 'a', 'e'] c ('a', 5)`",
                        "`['a', 'b', 'e'] c ('c', 0)`", "`['a', 'b', 'e'] c ('b', 7)`"],
            "answer": "C",
            "solution": (
                "**Concept.** Since Python 3.7, dicts preserve **insertion order**. Re-assigning an existing key "
                "keeps its position; deleting and re-inserting a key moves it to the end. `update` follows the "
                "same rules. Iterating a dict yields its keys.\n\n"
                "- Start: b:1, a:2, c:3.\n"
                "- `d['a'] = 5` → b:1, a:5, c:3 (position unchanged).\n"
                "- `del d['b']` → a:5, c:3; `d['b'] = 7` → a:5, c:3, **b:7** (now last).\n"
                "- `update(c=0, e=9)` → a:5, c:0, b:7, e:9.\n\n"
                "- `k`: keys with truthy values → c (0) is excluded → ['a', 'b', 'e'].\n"
                "- `sorted(d, key=d.get)` orders keys by value: c(0), a(5), b(7), e(9) → first is 'c'.\n"
                "- `list(d.items())[1]` → ('c', 0).\n\n"
                "Output `['a', 'b', 'e'] c ('c', 0)` → (C).\n\n"
                "**Options.** (A) forgets that 0 is falsy. (B) keeps 'b' at its original first position. (D) "
                "thinks re-inserted 'b' returns to its old slot right after 'a'.\n\n"
                "**Trap:** `d[k] = v` on an *existing* key does not move it; only deletion followed by "
                "insertion does."
            ),
            "verify": "assert OUTPUT.strip() == \"['a', 'b', 'e'] c ('c', 0)\" and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "DAGs — topological orders and Kahn’s algorithm",
            "text": "Consider the directed acyclic graph below. Which of the following statements is/are TRUE?",
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "C"], ["A", "E"], ["B", "C"], ["B", "D"], ["C", "F"], ["D", "F"],
                                    ["D", "G"], ["E", "G"], ["F", "H"], ["G", "H"]],
                          "pos": {"A": [0, 2], "B": [0, 0.4], "E": [2, 2.8], "C": [2, 1.3], "D": [2, -0.2],
                                  "G": [4, 2], "F": [4, 0.4], "H": [6, 1.2]}}],
            "options": [
                "B D A G C E F H is a valid topological order",
                "Kahn’s algorithm that always removes the alphabetically smallest vertex of in-degree 0 "
                "outputs A B C D E F G H",
                "H is the last vertex in every topological order",
                "A precedes D in every topological order",
            ],
            "answer": ["B", "C"],
            "solution": (
                "**Concept.** A sequence is a topological order iff every edge u→v has u before v. Kahn’s "
                "algorithm repeatedly outputs a vertex of in-degree 0 and deletes its out-edges.\n\n"
                "In-degrees: A 0, B 0, C 2, D 1, E 1, F 2, G 2, H 2.\n\n"
                "- (A) In B D A G C E F H, G appears before E, but E→G is an edge. **FALSE.**\n"
                "- (B) Kahn with a min-priority queue: available {A, B} → A (frees E); {B, E} → B (frees C "
                "and D); {C, D, E} → C; {D, E} → D (F freed: its predecessors C, D are done); {E, F} → E "
                "(frees G); {F, G} → F; G; H. Output **A B C D E F G H**. **TRUE.**\n"
                "- (C) H is the only sink, and every other vertex has a path to H (via F or G), so H must "
                "come after all of them. **TRUE.**\n"
                "- (D) A and D are incomparable (no path between them): e.g. B D A C E F G H is valid. "
                "**FALSE.**\n\n"
                "**Trap:** in (B), students often output D before C because D was “freed” by B at the same "
                "time as C — the tie is broken alphabetically, so C wins."
            ),
            "verify": '''
import heapq
D = {'A': 'CE', 'B': 'CD', 'C': 'F', 'D': 'FG', 'E': 'G', 'F': 'H', 'G': 'H', 'H': ''}
def valid(s):
    pos = {v: i for i, v in enumerate(s.split())}
    return all(pos[u] < pos[v] for u in D for v in D[u])
indeg = {v: 0 for v in D}
for u in D:
    for v in D[u]: indeg[v] += 1
h = [v for v in D if indeg[v] == 0]; heapq.heapify(h); out = []
while h:
    u = heapq.heappop(h); out.append(u)
    for v in D[u]:
        indeg[v] -= 1
        if indeg[v] == 0: heapq.heappush(h, v)
import itertools
orders = [p for p in itertools.permutations(D) if valid(' '.join(p))]
res = [valid("B D A G C E F H"), out == list("ABCDEFGH"),
       all(p[-1] == 'H' for p in orders), all(p.index('A') < p.index('D') for p in orders)]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
    ],
}
