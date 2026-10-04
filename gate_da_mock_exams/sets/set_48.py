# Set 48 — Challenge Mock, Paper 3 (Hard)
SET = {
    "number": 48,
    "title": "Challenge Mock — Paper 3",
    "difficulty": "Hard",
    "focus": "hardest, multi-concept, trap-heavy 2-mark questions",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — chained comparisons",
            "text": "Consider the following Python program. What is printed?",
            "code": '''print(1 < 3 > 2 == 2 < 5, (1 < 3) > 2, [] == [] is not [])''',
            "options": ["`True False True`", "`True True True`", "`False False True`",
                        "`True False False`"],
            "answer": "A",
            "solution": (
                "Python **chains** comparison operators: `a op1 b op2 c` means "
                "`(a op1 b) and (b op2 c)`, with b evaluated once. `is`, `is not`, `==`, `<` … all "
                "belong to the same chaining family. Parentheses break the chain.\n\n"
                "- `1 < 3 > 2 == 2 < 5` = (1<3) and (3>2) and (2==2) and (2<5) = **True**.\n"
                "- `(1 < 3) > 2`: the parenthesised part is `True`, i.e. 1 as an int; `1 > 2` is "
                "**False**.\n"
                "- `[] == [] is not []` = ([] == []) and ([] is not []). The middle list is shared "
                "by both comparisons, but the third literal is a *new* list object, so `is not` is "
                "True; the equality is True → **True**.\n\n"
                "Output `True False True` → option **(A)**.\n\n"
                "- (B) evaluates `(1 < 3) > 2` as if it were chained.\n"
                "- (C) evaluates the first chain left-to-right as ((1<3) > 2) …, like C would.\n"
                "- (D) assumes `[] is not []` is False, i.e. that two empty-list literals are the "
                "same object — every `[]` creates a new list.\n\n"
                "**Trap:** in C/Java, `1 < 3 > 2` would compare a boolean with 2. Python's chaining "
                "is purely syntactic sugar for `and`."
            ),
            "verify": "assert OUTPUT.strip() == 'True False True' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — generators and iterator exhaustion",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''g = (x * x for x in range(6))
s1 = sum(x for x in g if x % 2)
s2 = sum(g)
it = iter(range(11))
pairs = list(zip(it, it))
rest = sum(it)
print(s1 + s2 + len(pairs) + rest)''',
            "answer": "40",
            "solution": (
                "Generators and iterators are **single-pass**; and `zip` pulls from its arguments "
                "left to right, stopping as soon as *any* argument is exhausted.\n\n"
                "- `g` yields 0, 1, 4, 9, 16, 25. The first `sum` consumes it completely, keeping odd "
                "squares 1 + 9 + 25 → s1 = **35**.\n"
                "- `sum(g)` on the exhausted generator → s2 = **0**.\n"
                "- `zip(it, it)` takes two consecutive items per tuple from the *same* iterator: "
                "(0,1), (2,3), (4,5), (6,7), (8,9) → 5 pairs. For the 6th tuple zip calls `next(it)` "
                "for the first argument and gets **10**, then the second `next` raises "
                "`StopIteration`, so the tuple is discarded — and 10 is **lost**.\n"
                "- `rest = sum(it)` → 0.\n\n"
                "Printed: 35 + 0 + 5 + 0 = **40**.\n\n"
                "**Trap:** expecting rest = 10 (answer 50), or expecting s2 = 55 (re-iterating the "
                "generator). Use `itertools.zip_longest` or slicing when leftovers matter."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Stacks — monotonic stack (next greater element)",
            "text": ("The function below is called on a = [6, 2, 5, 1, 4, 8, 3, 7] (shown). Which of the "
                     "following statements is/are TRUE?"),
            "code": '''def nge(a):
    res, st, pops = [-1] * len(a), [], 0
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
            pops += 1
        st.append(i)
    return res, pops, st''',
            "diagrams": [{"type": "array", "values": [6, 2, 5, 1, 4, 8, 3, 7], "label": "a"}],
            "options": ["`res == [8, 5, 8, 4, 8, -1, 7, -1]`",
                        "`pops == 6`",
                        "At some moment the stack holds 4 indices",
                        "When the function returns, the stack holds the indices of the values 8 and 7 "
                        "(bottom to top)"],
            "answer": ["A", "B", "D"],
            "solution": (
                "The stack keeps indices whose values are **strictly decreasing** from bottom to top; "
                "a new value pops every smaller value and becomes their next greater element. Each "
                "index is pushed once and popped at most once → O(n).\n\n"
                "Trace (stack shown as values):\n"
                "- 6 → [6]\n"
                "- 2 → [6, 2]\n"
                "- 5 pops 2 (res=5) → [6, 5]\n"
                "- 1 → [6, 5, 1]  (size 3)\n"
                "- 4 pops 1 (res=4) → [6, 5, 4]  (size 3)\n"
                "- 8 pops 4, 5, 6 (res=8 each) → [8]\n"
                "- 3 → [8, 3]\n"
                "- 7 pops 3 (res=7) → [8, 7]\n\n"
                "- (A) res = [8, 5, 8, 4, 8, −1, 7, −1]. **True.**\n"
                "- (B) pops = 1 + 1 + 3 + 1 = 6 (= 8 pushes − 2 left). **True.**\n"
                "- (C) The maximum size is 3. **False.**\n"
                "- (D) Final stack = indices 5, 7 = values 8, 7. **True.**\n\n"
                "**Trap:** in (C), 4 does not stack on top of 1 — it pops 1 first, so the size stays 3."
            ),
            "verify": '''
r, p, s = nge([6,2,5,1,4,8,3,7])
a = [6,2,5,1,4,8,3,7]
st, mx = [], 0
for i, x in enumerate(a):
    while st and a[st[-1]] < x: st.pop()
    st.append(i); mx = max(mx, len(st))
truth = {'A': r == [8,5,8,4,8,-1,7,-1], 'B': p == 6, 'C': mx >= 4,
         'D': [a[i] for i in s] == [8, 7]}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "NAT", "marks": 1, "topic": "Deques — sliding-window maximum",
            "text": ("The program computes the maximum of every window of size 3 using a deque of "
                     "indices. The value printed (the number of removals from the **back** of the "
                     "deque) is ______."),
            "code": '''from collections import deque

a = [4, 2, 12, 3, 8, 6, 1, 9, 5, 7]
k, dq, back, out = 3, deque(), 0, []
for i, x in enumerate(a):
    while dq and a[dq[-1]] <= x:
        dq.pop()
        back += 1
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        out.append(a[dq[0]])
print(back)''',
            "answer": "7",
            "solution": (
                "The deque holds indices whose values are decreasing from front to back. An incoming "
                "value removes from the back every value ≤ it (they can never be a future maximum); "
                "the front is dropped when it leaves the window.\n\n"
                "Trace (deque as values):\n"
                "- 4 → [4];  2 → [4, 2]\n"
                "- 12: pops 2, 4 (**2**) → [12]; max 12\n"
                "- 3 → [12, 3]; max 12\n"
                "- 8: pops 3 (**3**) → [12, 8]; max 12\n"
                "- 6 → [12, 8, 6]; 12 (index 2) leaves the window (front pop) → [8, 6]; max 8\n"
                "- 1 → [8, 6, 1]; max 8\n"
                "- 9: pops 1, 6, 8 (**6**) → [9]; max 9\n"
                "- 5 → [9, 5]; max 9\n"
                "- 7: pops 5 (**7**) → [9, 7]; max 9\n\n"
                "Back removals = **7**; window maxima = 12, 12, 12, 8, 8, 9, 9, 9.\n\n"
                "**Trap:** counting the single front removal (12 leaving the window) as well, which "
                "gives 8. The total of all removals is at most n, which is why the algorithm is O(n)."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER and out == [12,12,12,8,8,9,9,9]",
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Linked lists — split, reverse and interleave",
            "text": ("`reorder` is applied to the list 1 → 2 → … → 7 (shown). What does `show` print "
                     "for the result?"),
            "code": '''def reorder(h):
    slow, fast = h, h.nxt
    while fast and fast.nxt:
        slow, fast = slow.nxt, fast.nxt.nxt
    second, slow.nxt = slow.nxt, None
    prev = None
    while second:
        second.nxt, prev, second = prev, second, second.nxt
    first = h
    while prev:
        a, b = first.nxt, prev.nxt
        first.nxt, prev.nxt = prev, a
        first, prev = a, b
    return h''',
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7]}],
            "options": ["`[1, 7, 2, 6, 3, 5, 4]`", "`[1, 7, 2, 6, 3, 5]`",
                        "`[1, 5, 2, 6, 3, 7, 4]`", "`[1, 6, 2, 5, 3, 4, 7]`"],
            "answer": "A",
            "solution": (
                "Three classic phases: (1) find the middle with slow/fast pointers, (2) cut and "
                "reverse the second half, (3) interleave.\n\n"
                "- Phase 1 (fast starts at h.nxt): slow/fast = (1,2) → (2,4) → (3,6); fast.nxt = 7 → "
                "(4, None) stop. slow = **4**.\n"
                "- Cut after 4: first half 1→2→3→4, second half 5→6→7.\n"
                "- Phase 2: reverse the second half → 7→6→5 (prev = 7).\n"
                "- Phase 3: 1→7, 7→2; 2→6, 6→3; 3→5, 5→4; prev becomes None → stop. 4's next is "
                "already None.\n\n"
                "Result 1, 7, 2, 6, 3, 5, 4 → option **(A)** (pattern L₀, Lₙ, L₁, Lₙ₋₁, …).\n\n"
                "- (B) loses the middle node 4 (would happen if the cut were made *before* the "
                "middle).\n"
                "- (C) forgets to reverse the second half.\n"
                "- (D) cuts after 3 (using fast = h), leaving 4 in the second half.\n\n"
                "**Trap:** the multiple-assignment lines evaluate the entire right side first; "
                "writing them as sequential statements in the same order would lose pointers."
            ),
            "verify": '''
class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt
def build(n):
    head = None
    for v in range(n, 0, -1): head = Node(v, head)
    return head
def show(h):
    out = []
    while h: out.append(h.v); h = h.nxt
    return out
assert show(reorder(build(7))) == [1,7,2,6,3,5,4] and ANSWER == 'A'
assert show(reorder(build(6))) == [1,6,2,5,3,4]
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "NAT", "marks": 1, "topic": "Heaps — where can the k-th smallest be?",
            "text": ("A binary min-heap stores 1023 distinct keys in an array A[0..1022] (children of i at "
                     "2i+1 and 2i+2). Considering all possible such heaps, the number of different "
                     "indices at which the **4th smallest** key can appear is ______."),
            "answer": "14",
            "solution": (
                "Every ancestor of a node holds a smaller key. So if the 4th smallest key sits at "
                "depth d (root depth 0), all its d ancestors must be among the 3 smaller keys → "
                "**d ≤ 3**. It cannot be the root (d = 0) because the root holds the minimum.\n\n"
                "Conversely every node at depth 1, 2 or 3 is possible: put the 4th smallest there, "
                "place smaller keys on its ancestors (at most 3 needed) and any remaining smaller keys "
                "as other children of the root, then fill the rest with larger keys in heap order. "
                "With 1023 = 2¹⁰ − 1 keys all of depths 1–3 exist.\n\n"
                "Count = 2 + 4 + 8 = **14** indices (A[1] … A[14]).\n\n"
                "**Trap:** answering 15 (including the root) or 8 (only the deepest level 3, "
                "thinking the 4th smallest must be 'three levels down'). In general the k-th smallest "
                "(k ≥ 2) can be at any depth from 1 to k − 1, i.e. at 2^{k} − 2 indices."
            ),
            "verify": '''
import random, heapq
random.seed(3)
seen = set()
for _ in range(30000):
    a = list(range(1, 32)); random.shuffle(a); heapq.heapify(a)
    seen.add(a.index(4))
assert seen == set(range(1, 15)) and len(seen) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Python dicts — insertion order and deletion",
            "text": "Consider the following Python program. What is printed?",
            "code": '''d = {}
for k in "banana":
    d[k] = d.get(k, 0) + 1
del d['b']
d['b'] = 9
d['a'] += 1
print(list(d.items()))''',
            "options": ["`[('a', 4), ('n', 2), ('b', 9)]`", "`[('b', 9), ('a', 4), ('n', 2)]`",
                        "`[('n', 2), ('b', 9), ('a', 4)]`", "`[('a', 3), ('n', 2), ('b', 9)]`"],
            "answer": "A",
            "solution": (
                "Since Python 3.7, a dict iterates in **insertion order** of its keys. Updating the "
                "value of an existing key does **not** change its position; deleting a key and "
                "inserting it again puts it at the **end**.\n\n"
                "- Counting \"banana\": keys inserted in order b, a, n → {b: 1, a: 3, n: 2}.\n"
                "- `del d['b']` → {a: 3, n: 2}.\n"
                "- `d['b'] = 9` → re-inserted at the end → {a: 3, n: 2, b: 9}.\n"
                "- `d['a'] += 1` → value update in place → {a: 4, n: 2, b: 9}.\n\n"
                "Output `[('a', 4), ('n', 2), ('b', 9)]` → option **(A)**.\n\n"
                "- (B) assumes 'b' regains its original first position.\n"
                "- (C) assumes updating 'a' moves it to the end.\n"
                "- (D) ignores the final increment.\n\n"
                "**Tip:** underneath, CPython keeps a dense entries array plus a sparse hash index; "
                "deletion leaves a hole in the entries array, and a re-insert appends a new entry."
            ),
            "verify": "assert OUTPUT.strip() == \"[('a', 4), ('n', 2), ('b', 9)]\" and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search on the answer",
            "text": ("The program finds the smallest integer speed v such that piles of sizes P can be "
                     "finished within H hours, eating at most v units per hour from one pile (time for "
                     "a pile p is ⌈p / v⌉). What is printed?"),
            "code": '''import math
P, H = [30, 11, 23, 4, 20], 6
lo, hi, it = 1, max(P), 0
while lo < hi:
    mid = (lo + hi) // 2
    it += 1
    if sum(math.ceil(p / mid) for p in P) <= H:
        hi = mid
    else:
        lo = mid + 1
print(lo, it)''',
            "options": ["`23 5`", "`22 5`", "`23 4`", "`30 5`"],
            "answer": "A",
            "solution": (
                "The predicate 'speed v suffices' is **monotone** (if v works, every larger v works), "
                "so binary search finds the first v where it becomes true. The loop keeps the answer "
                "in [lo, hi].\n\n"
                "Hours needed: hours(v) = ∑⌈p/v⌉.\n"
                "- it 1: lo=1, hi=30, mid=15 → 2+1+2+1+2 = 8 > 6 → lo = 16\n"
                "- it 2: mid=23 → 2+1+1+1+1 = 6 ≤ 6 → hi = 23\n"
                "- it 3: mid=19 → 2+1+2+1+2 = 8 → lo = 20\n"
                "- it 4: mid=21 → 2+1+2+1+1 = 7 → lo = 22\n"
                "- it 5: mid=22 → 2+1+2+1+1 = 7 → lo = 23\n"
                "- lo = hi = 23 → stop.\n\n"
                "Output `23 5` → option **(A)**.\n\n"
                "- (B) 22 needs 7 hours (the 23-pile takes 2 hours).\n"
                "- (C) miscounts iterations (the search space 1..30 needs ⌈log₂ 30⌉ = 5 halvings).\n"
                "- (D) is a valid but not minimal speed.\n\n"
                "**Trap:** writing `hi = mid - 1` when the predicate is true would skip the answer."
            ),
            "verify": "assert OUTPUT.strip() == '23 5' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Insertion sort — exact comparison count",
            "text": ("Insertion sort (ascending) is applied to [5, 1, 4, 2, 3]. Each evaluation of "
                     "`a[j] > key` counts as one comparison; the inner loop also stops (without a "
                     "comparison) when j becomes −1. The total number of comparisons is:"),
            "options": ["9", "6", "10", "7"],
            "answer": "A",
            "solution": (
                "Comparisons = (number of shifts) + (number of passes that end with a *failing* "
                "comparison rather than at j = −1). Shifts = inversions.\n\n"
                "Inversions of [5, 1, 4, 2, 3]: (5,1), (5,4), (5,2), (5,3), (4,2), (4,3) → 6.\n\n"
                "Pass by pass:\n"
                "- insert 1: 5 > 1 shift; j = −1 stop → 1 comparison\n"
                "- insert 4: 5 > 4 shift; 1 > 4? no → 2 comparisons\n"
                "- insert 2: 5 shift, 4 shift, 1 > 2? no → 3 comparisons\n"
                "- insert 3: 5 shift, 4 shift, 2 > 3? no → 3 comparisons\n\n"
                "Total = 1 + 2 + 3 + 3 = **9** = 6 shifts + 3 failing comparisons → option **(A)**.\n\n"
                "- (B) counts only shifts.\n"
                "- (C) adds a failing comparison to every pass, including the one that ran off the "
                "front.\n"
                "- (D) undercounts the last pass.\n\n"
                "**Tip:** for n elements, comparisons = inversions + (n − 1) − (number of elements "
                "that become the new minimum of the sorted prefix)."
            ),
            "verify": '''
a = [5,1,4,2,3]; c = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0:
        c += 1
        if a[j] > key: a[j+1] = a[j]; j -= 1
        else: break
    a[j+1] = key
assert c == 9 and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MSQ", "marks": 1, "topic": "Graph theory — cycles, degrees, connectivity",
            "text": "Which of the following statements about simple undirected graphs is/are TRUE?",
            "options": ["A graph with 10 vertices, 12 edges and exactly 2 connected components "
                        "contains at least 4 distinct cycles",
                        "Every graph with n ≥ 2 vertices has two vertices of equal degree",
                        "A connected graph with n vertices and n edges contains exactly one cycle",
                        "If every vertex has degree at least 2, the graph is connected"],
            "answer": ["A", "B", "C"],
            "solution": (
                "- (A) A spanning forest of a graph with n vertices and c components has n − c edges. "
                "Each of the remaining e − (n − c) = 12 − 8 = **4** edges closes a different "
                "*fundamental cycle* with the forest (each contains its own non-forest edge, so they "
                "are distinct). **True.**\n\n"
                "- (B) Degrees lie in {0, …, n−1}, but 0 and n−1 cannot both occur (a vertex of degree "
                "n−1 is adjacent to everything). So n vertices take at most n−1 distinct values → by "
                "pigeonhole two are equal. **True.**\n\n"
                "- (C) Take a spanning tree (n − 1 edges); exactly one edge uv is left over. A tree "
                "has no cycle, so every cycle must use uv, and the rest of such a cycle is a u–v path "
                "inside the tree — which is unique. Hence exactly one cycle. **True.**\n\n"
                "- (D) Two disjoint triangles: every degree is 2, but the graph has two components. "
                "**False.**\n\n"
                "**Trap:** confusing 'minimum degree ≥ 2 ⇒ contains a cycle' (true) with "
                "'⇒ connected' (false)."
            ),
            "verify": '''
import random
from itertools import combinations
def count_cycles(n, E):
    adj = {v: set() for v in range(n)}
    for u, v in E: adj[u].add(v); adj[v].add(u)
    cyc = set()
    def dfs(start, u, path):
        for w in adj[u]:
            if w == start and len(path) >= 3:
                cyc.add(frozenset(frozenset(e) for e in zip(path, path[1:] + [start])))
            elif w > start and w not in path:
                dfs(start, w, path + [w])
    for s0 in range(n): dfs(s0, s0, [s0])
    return len(cyc)
def comps(n, E):
    p = list(range(n))
    def f(x):
        while p[x] != x: x = p[x]
        return x
    for u, v in E: p[f(u)] = f(v)
    return len({f(v) for v in range(n)})
random.seed(7)
okA = True
allE = list(combinations(range(10), 2))
tried = 0
while tried < 150:
    E = random.sample(allE, 12)
    if comps(10, E) != 2: continue
    tried += 1
    if count_cycles(10, E) < 4: okA = False
okB = True
pairs5 = list(combinations(range(5), 2))
for mask in range(1 << 10):
    deg = [0]*5
    for b, (u, v) in enumerate(pairs5):
        if mask >> b & 1: deg[u] += 1; deg[v] += 1
    if len(set(deg)) == 5: okB = False
okC = True
for mask in range(1 << 10):
    E = [pairs5[b] for b in range(10) if mask >> b & 1]
    if len(E) == 5 and comps(5, E) == 1 and count_cycles(5, E) != 1: okC = False
twoTri = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]
okD = comps(6, twoTri) == 1
truth = {'A': okA, 'B': okB, 'C': okC, 'D': okD}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
    ],
}
