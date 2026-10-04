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
    ],
}
