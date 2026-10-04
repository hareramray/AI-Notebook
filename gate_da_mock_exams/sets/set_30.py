# Set 30 — Divide & Conquer Applications

SET = {
    'number': 30,
    'title': 'Divide & Conquer Applications',
    'difficulty': 'GATE-level',
    'focus': 'inversion counting, max subarray, fast power, D&C recurrences',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — recursive fast exponentiation',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''calls = 0
def power(b, e):
    global calls
    calls += 1
    if e == 0:
        return 1
    h = power(b, e // 2)
    return h * h * (b if e % 2 else 1)

print(power(3, 13) % 100, calls)''',
            'options': ['`23 4`', '`23 5`', '`23 13`', '`63 5`'],
            'answer': 'B',
            'solution': '''**Concept.** Exponentiation by squaring halves the exponent at every call: b^{e} = (b^{⌊e/2⌋})^{2} · b^{e mod 2}. The number of calls is the number of halvings to reach 0, i.e. ⌊log₂ e⌋ + 2 for e ≥ 1.

Call chain for e = 13: 13 → 6 → 3 → 1 → 0 — that is **5** calls (the call with e = 0 counts).

Values on the way back up:
- e=0: 1
- e=1: 1·1·3 = 3
- e=3: 3·3·3 = 27
- e=6: 27·27 = 729
- e=13: 729·729·3 = 1 594 323 → mod 100 = **23**.

Output `23 5` → (B).

**Options.** (A) forgets the base-case call with e = 0. (D) gets the remainder wrong (63 would come from 3^{12}·… mixing up the odd factor). (C) confuses the call count with the exponent — that is the *naive* method’s cost.

**Tip:** the recursion depth, and the number of multiplications, are Θ(log e).''',
            'verify': '''ANSWER = {'D': 'B', 'B': 'D'}.get(ANSWER, ANSWER)
assert OUTPUT.strip() == '23 5' and ANSWER == 'D' and 3**13 % 100 == 23''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Recursion — evaluating a D&C recurrence',
            'text': 'Consider the function below. The value returned by `f(20)` is ______.',
            'code': '''def f(n):
    if n <= 1:
        return 1
    return f(n // 2) + f(n // 2) + n''',
            'answer': '92',
            'solution': '''**Concept.** f satisfies f(n) = 2 f(⌊n/2⌋) + n with f(1) = 1. For powers of two this gives n log₂ n + n, but for other n the floors matter, so evaluate bottom-up along the chain 20 → 10 → 5 → 2 → 1.

- f(1) = 1
- f(2) = 2·f(1) + 2 = 4
- f(5) = 2·f(2) + 5 = 13
- f(10) = 2·f(5) + 10 = 36
- f(20) = 2·f(10) + 20 = **92**

**Trap:** plugging into the closed form n log₂ n + n with log₂ 20 ≈ 4.32 gives ≈ 106.4 — the closed form only holds exactly for powers of two. Another slip is f(5) = 2·f(2.5): integer division gives f(2).''',
            'verify': 'assert f(20) == int(ANSWER) and f(16) == 80',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Recurrences — master theorem (extended case 2)',
            'text': 'The solution of the recurrence T(n) = 4T(n/2) + n² log n, T(1) = 1, is',
            'options': ['Θ(n² log n)', 'Θ(n³)', 'Θ(n² log² n)', 'Θ(n² log log n)'],
            'answer': 'C',
            'solution': '''**Concept.** Compare f(n) with n^{log_b a}. Here a = 4, b = 2, so n^{log₂ 4} = n². f(n) = n² log n = Θ(n^{log_b a} · log^{k} n) with k = 1 — the *extended case 2* of the master theorem, giving Θ(n^{log_b a} · log^{k+1} n).

Direct check by unrolling: level i of the recursion tree has 4^{i} subproblems of size n/2^{i}, each costing (n/2^{i})² log(n/2^{i}); the level total is n² (log n − i). Summing over i = 0 … log n gives n² · Σ (log n − i) = n² · Θ(log² n).

Hence T(n) = **Θ(n² log² n)** → (C).

**Options.** (A) is what you get by ignoring the log factor in f (case 2 with k = 0). (B) would need f to be polynomially larger than n². (D) arises for f(n) = n²/log n (k = −1), not n² log n.

**Trap:** n² log n is *not* polynomially larger than n², so case 3 does not apply.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

import math
def T(n): return 1 if n <= 1 else 4 * T(n // 2) + n * n * math.log2(n)
r = [T(2**k) / (4**k * k * k) for k in (8, 12, 16)]
assert abs(r[2] - 0.5) < 0.05 and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Maximum subarray — divide and conquer',
            'text': 'The divide-and-conquer maximum-subarray algorithm splits A into the left half A[0..3] and the right half A[4..7], solves both recursively, and also computes the best subarray *crossing* the middle (best suffix of the left half + best prefix of the right half). Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [-3, 5, -2, 6, -9, 4, 3, -1],
                    'label': 'A',
                    'caption': 'Input array',
                },
            ],
            'options': [
                'The maximum subarray sum of A is 9',
                'The crossing sum computed at the top level is 9',
                'The recursive call on the left half returns 9',
                'If every element of A is negated, the maximum subarray sum becomes 9',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** answer = max(left best, right best, crossing best).

- Left half [−3, 5, −2, 6]: best is 5 − 2 + 6 = **9**.
- Right half [−9, 4, 3, −1]: best is 4 + 3 = 7.
- Crossing: suffix sums of the left half (ending at index 3) are 6, 4, 9, 6 → best 9; prefix sums of the right half (starting at index 4) are −9, −5, −2, −3 → best −2. Crossing = 9 − 2 = **7**.
- Overall = max(9, 7, 7) = 9.

Option by option:
- (A) **TRUE** (subarray 5, −2, 6).
- (B) The crossing sum is 7, not 9 — the crossing subarray *must* include A[4] = −9. **FALSE.**
- (C) The left call returns 9. **TRUE.**
- (D) Negated array: 3, −5, 2, −6, 9, −4, −3, 1. The single element 9 is best (9 − 4 < 9, and extending left adds −6). **TRUE.**

**Trap:** the crossing part must contain *at least one* element from each side, so its best prefix can be negative.''',
            'verify': '''
def best(a):
    return max(sum(a[i:j]) for i in range(len(a)) for j in range(i + 1, len(a) + 1))
A = [-3, 5, -2, 6, -9, 4, 3, -1]
cross = max(sum(A[i:4]) for i in range(4)) + max(sum(A[4:j]) for j in range(5, 9))
res = [best(A) == 9, cross == 9, best(A[:4]) == 9, best([-x for x in A]) == 9]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Inversion counting',
            'text': 'An inversion in an array A is a pair of indices (i, j) with i < j and A[i] > A[j]. The number of inversions in the array below is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [3, 8, 1, 6, 2, 7, 5, 4],
                    'label': 'A',
                },
            ],
            'answer': '14',
            'solution': '''**Concept.** Count, for each element, how many *later* elements are smaller (or, equivalently, how many earlier elements are larger). Merge-sort counting does this in Θ(n log n); for n = 8 a direct count is quick.

Smaller elements to the right of each position:
- 3: {1, 2} → 2
- 8: {1, 6, 2, 7, 5, 4} → 6
- 1: none → 0
- 6: {2, 5, 4} → 3
- 2: none → 0
- 7: {5, 4} → 2
- 5: {4} → 1
- 4: → 0

Total = 2 + 6 + 0 + 3 + 0 + 2 + 1 + 0 = **14**.

Cross-check: insertion sort on this array would perform exactly 14 shifts, and bubble sort exactly 14 swaps.

**Trap:** counting only *adjacent* out-of-order pairs (here 4) — inversions include all pairs.''',
            'verify': '''
A = [3, 8, 1, 6, 2, 7, 5, 4]
assert sum(A[i] > A[j] for i in range(8) for j in range(i + 1, 8)) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — bracket matching',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def check(s):
    st = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for i, c in enumerate(s):
        if c in '([{':
            st.append(c)
        elif not st or st.pop() != pairs[c]:
            return i
    return -1 if not st else len(s)

print(check("{[()]}"), check("([)]"), check("(()[]{"))''',
            'options': ['`-1 3 6`', '`-1 2 5`', '`-1 2 6`', '`0 2 6`'],
            'answer': 'C',
            'solution': '''**Concept.** The function returns −1 for a balanced string, the index of the first closing bracket that does not match, or len(s) if openers remain unmatched at the end.

- `{[()]}`: every closer matches the most recent opener; stack ends empty → **−1**.
- `([)]`: push `(`, `[`; at i = 2 the closer `)` pops `[` ≠ `(` → return **2**.
- `(()[]{`: pairs `()` and `[]` match, but `(` (index 0) and `{` remain on the stack at the end → return len(s) = **6**.

Output `-1 2 6` → (C).

**Options.** (A) reports the index of the *second* mismatching bracket. (B) returns the index of the last character instead of len(s). (D) treats the first string as unbalanced.

**Trap:** in `not st or st.pop() != …`, short-circuiting matters: when the stack is empty `pop()` is never called, so no IndexError occurs.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '-1 2 6' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Hashing — quadratic probing coverage',
            'text': 'A hash table of size m = 8 uses quadratic probing: probe i (i = 0, 1, 2, …) for key k examines slot (h(k) + i²) mod 8. Which of the following statements is/are TRUE?',
            'options': [
                'For a key whose home slot is 0, the slots 2, 3, 5, 6 and 7 are never examined',
                'An insertion can fail even when only 3 of the 8 slots are occupied',
                'For a key whose home slot is 3, the first four probes examine slots 3, 4, 7, 6',
                'If m were 7 instead, the probe sequence from any home slot would reach exactly 4 distinct slots',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concept.** The slots reachable from home h are h + (i² mod m). The set of squares modulo m decides how much of the table is reachable.

Squares mod 8: 0, 1, 4, 1, 0, 1, 4, 1, … → only offsets **{0, 1, 4}**.

- (A) From home 0 only slots 0, 1, 4 are ever probed; 2, 3, 5, 6, 7 never. **TRUE.**
- (B) If slots 0, 1, 4 are occupied, a key hashing to 0 can never be placed, although 5 slots are free. **TRUE.**
- (C) Offsets for i = 0, 1, 2, 3 are 0, 1, 4, 9 mod 8 = 1 → slots 3, 4, 7, **4**, not 6. **FALSE.**
- (D) Squares mod 7: 0, 1, 4, 2, 2, 4, 1 → {0, 1, 2, 4}, i.e. (7 + 1)/2 = 4 distinct offsets. **TRUE.**

**Tip:** for a prime m, quadratic probing reaches exactly ⌈m/2⌉ slots, which guarantees an insertion succeeds whenever the table is at most half full.''',
            'verify': '''
sq8 = {i * i % 8 for i in range(64)}; sq7 = {i * i % 7 for i in range(49)}
res = [sq8 == {0, 1, 4}, len(sq8) <= 3,
       [(3 + i * i) % 8 for i in range(4)] == [3, 4, 7, 6], len(sq7) == 4]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Counting BSTs (Catalan recurrence)',
            'text': 'The number of structurally distinct binary search trees on the keys 1, 2, 3, 4, 5, 6 whose **root is 3** is ______.',
            'answer': '10',
            'solution': '''**Concept.** Fixing the root splits the problem (divide and conquer): keys smaller than the root form the left subtree, larger keys the right subtree, independently. The number of BSTs on k keys is the Catalan number C_{k}: 1, 1, 2, 5, 14, …

- Left subtree: keys {1, 2} → C_{2} = 2 shapes.
- Right subtree: keys {4, 5, 6} → C_{3} = 5 shapes.

Total = 2 × 5 = **10**.

Summing C_{r−1}·C_{6−r} over all six roots r gives 42 + 14 + 10 + 10 + 14 + 42 = 132 = C_{6}, the total number of BSTs on six keys.

**Trap:** adding instead of multiplying (2 + 5 = 7); the two subtrees are chosen independently, so the counts multiply.''',
            'verify': '''
from functools import lru_cache
@lru_cache(None)
def C(n): return 1 if n <= 1 else sum(C(r) * C(n - 1 - r) for r in range(n))
assert C(2) * C(3) == int(ANSWER) and sum(C(r) * C(5 - r) for r in range(6)) == 132
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'DFS — edge classification',
            'text': 'DFS is run on the directed graph below, starting at A; whenever there is a choice, vertices are explored in alphabetical order (all vertices are reachable from A). How are the edges F→C, D→E and A→F classified (tree / back / forward / cross)?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['A', 'F'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['C', 'A'],
                        ['D', 'E'],
                        ['E', 'F'],
                        ['F', 'C'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [1.5, 2],
                        'C': [3.5, 2.4],
                        'D': [1.5, 0],
                        'E': [3, 0.6],
                        'F': [5, 1.2],
                    },
                },
            ],
            'options': [
                'back, cross, forward',
                'cross, cross, forward',
                'cross, back, tree',
                'cross, forward, forward',
            ],
            'answer': 'B',
            'solution': '''**Concept.** For an edge u→v met while scanning u: v undiscovered → tree; v discovered but unfinished (on the recursion stack) → back; v finished and discovered *after* u → forward; v finished and discovered *before* u → cross.

DFS with (discovery/finish) times:
- A 1 → B 2 → C 3: C→A is a back edge; C finishes 4.
- B → E 5 → F 6: F→C — C is already finished and was discovered (3) before F (6) → **cross**. F finishes 7, E 8, B 9.
- A → D 10: D→E — E finished (8), discovered at 5 < 10 → **cross**. D finishes 11.
- A→F: F is finished and was discovered (6) *after* A (1) → **forward**. A finishes 12.

Answer: cross, cross, forward → (B).

**Options.** (A) mislabels F→C as back, but C had already finished. (C) and (D) mislabel D→E: E is not an ancestor of D (back) nor a descendant (forward).

**Trap:** an edge into an *already finished* vertex is never a back edge; back edges exist iff the graph has a cycle (here C→A closes A→B→C).''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

G = {'A': 'BDF', 'B': 'CE', 'C': 'A', 'D': 'E', 'E': 'F', 'F': 'C'}
t = [0]; disc = {}; fin = {}; cls = {}
def dfs(u):
    t[0] += 1; disc[u] = t[0]
    for v in sorted(G[u]):
        if v not in disc: cls[(u, v)] = 'tree'; dfs(v)
        elif v not in fin: cls[(u, v)] = 'back'
        elif disc[u] < disc[v]: cls[(u, v)] = 'forward'
        else: cls[(u, v)] = 'cross'
    t[0] += 1; fin[u] = t[0]
dfs('A')
assert [cls[('F','C')], cls[('D','E')], cls[('A','F')]] == ['cross', 'cross', 'forward']
assert ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Linked lists — recursive merge',
            'text': 'The recursive function below merges two sorted singly linked lists (as in the merge step of merge sort). It is called on the lists 2 → 5 → 9 → 12 and 3 → 4 → 10 → 15 → 20. The total number of calls made to `merge` (including the first call) is ______.',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

calls = 0
def merge(a, b):
    global calls
    calls += 1
    if a is None: return b
    if b is None: return a
    if a.v <= b.v:
        a.nxt = merge(a.nxt, b)
        return a
    b.nxt = merge(a, b.nxt)
    return b

def build(xs):
    h = None
    for x in reversed(xs): h = Node(x, h)
    return h

h = merge(build([2, 5, 9, 12]), build([3, 4, 10, 15, 20]))''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [2, 5, 9, 12],
                    'head': 'a',
                },
                {
                    'type': 'linkedlist',
                    'values': [3, 4, 10, 15, 20],
                    'head': 'b',
                },
            ],
            'answer': '8',
            'solution': '''**Concept.** Each non-base call places exactly one node (the smaller front) and recurses on the rest; the recursion stops at the first call where one list is empty, and the remainder of the other list is attached in O(1).

Nodes placed, one per call: 2, 3, 4, 5, 9, 10, 12 — that is 7 calls. After 12 is placed, the next call is merge(None, 15 → 20), which returns immediately: call **8**.

Total calls = 7 + 1 = **8**. The merged list is 2 3 4 5 9 10 12 15 20.

In general, calls = (number of nodes placed before one list runs out) + 1, which is between min(p, q) + 1 and p + q.

**Trap:** answering p + q = 9 (assuming every node triggers a call) or forgetting the final base-case call (7).''',
            'verify': '''
out = []
while h: out.append(h.v); h = h.nxt
assert out == [2, 3, 4, 5, 9, 10, 12, 15, 20] and calls == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Inversion counting via merge sort — a buggy count',
            'text': 'The following function is intended to count inversions while merge-sorting, but the line marked (*) is wrong. What does the program print?',
            'code': '''def sort_count(a):
    if len(a) <= 1:
        return a, 0
    m = len(a) // 2
    L, x = sort_count(a[:m])
    R, y = sort_count(a[m:])
    out, i, j, c = [], 0, 0, x + y
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            c += 1                      # (*)
    out += L[i:] + R[j:]
    return out, c

print(sort_count([4, 1, 7, 3, 6, 2, 5])[1])''',
            'options': ['`7`', '`6`', '`10`', '`21`'],
            'answer': 'A',
            'solution': '''**Concept.** When R[j] is output before L[i], R[j] is smaller than *all* remaining left elements L[i..], so the correct update is `c += len(L) - i`. The buggy line adds only 1, i.e. it counts how many right-run elements are output while the left run is non-empty.

Recursion on [4, 1, 7, 3, 6, 2, 5] (split 3 | 4):
- [4] | [1, 7] (inner merge [1]|[7]: 0): merging [4] with [1, 7] outputs 1 before 4 → +1. Left total **1** (true inversions 1).
- [3, 6] (0) | [2, 5] (0): merge outputs 2 (+1), 3, 5 (+1), 6 → **2** (true: (3,2), (6,2), (6,5) = 3).
- Top merge [1, 4, 7] with [2, 3, 5, 6]: outputs 1, 2 (+1), 3 (+1), 4, 5 (+1), 6 (+1), then 7 → **4** (true cross inversions: 2 and 3 are each below 4 and 7, 5 and 6 below 7 → 6).

Printed value = 1 + 2 + 4 = **7** → (A). The true inversion count is 1 + 3 + 6 = 10.

Option by option:
- (A) Correct.
- (B) 6 counts only the top-level cross inversions.
- (C) 10 is what the *correct* code prints.
- (D) 21 = C(7, 2) is the total number of pairs.

**Trap:** the bug is invisible on inputs where each left run has a single remaining element when a right element jumps ahead — test on richer inputs.''',
            'verify': '''ANSWER = {'C': 'A', 'A': 'C'}.get(ANSWER, ANSWER)

a = [4, 1, 7, 3, 6, 2, 5]
assert OUTPUT.strip() == '7' and ANSWER == 'C'
assert sum(a[i] > a[j] for i in range(7) for j in range(i + 1, 7)) == 10
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — comparison count',
            'text': 'The functional quicksort below uses the first element as pivot. Assume each call on a list of length n ≥ 2 compares every one of the other n − 1 elements with the pivot exactly once (count only the `x < p` tests). For the input [6, 3, 9, 1, 8, 2, 7, 4, 5], the total number of such comparisons is ______.',
            'code': '''def qs(a):
    if len(a) <= 1:
        return a
    p = a[0]
    left = [x for x in a[1:] if x < p]
    right = [x for x in a[1:] if x >= p]
    return qs(left) + [p] + qs(right)''',
            'answer': '17',
            'solution': '''**Concept.** A call on n elements costs n − 1 comparisons; the sublists keep the *original relative order*, so each sublist’s first element is its pivot.

Recursion tree (list → cost):
- [6, 3, 9, 1, 8, 2, 7, 4, 5] → 8; left [3, 1, 2, 4, 5], right [9, 8, 7].
- [3, 1, 2, 4, 5] → 4; left [1, 2], right [4, 5].
- [1, 2] → 1 (right [2]); [4, 5] → 1 (right [5]).
- [9, 8, 7] → 2; left [8, 7] → 1 (left [7]).

Total = 8 + 4 + 1 + 1 + 2 + 1 = **17**.

For comparison: the best case for n = 9 (perfectly balanced splits 4 | 4, then 1 | 2) is 8 + 2·(3 + 1) = 16, the worst case (sorted input) is 8 + 7 + … + 1 = 36.

**Trap:** this code actually scans `a[1:]` *twice* (once per comprehension); if both tests were counted the answer would double to 34 — read what is being counted.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        6,
                        [
                            3,
                            [
                                1,
                                None,
                                [2],
                            ],
                            [
                                4,
                                None,
                                [5],
                            ],
                        ],
                        [
                            9,
                            [
                                8,
                                [7],
                                None,
                            ],
                            None,
                        ],
                    ],
                    'caption': 'Pivots form a BST: the recursion tree of quicksort',
                },
            ],
            'verify': '''
c = [0]
def qc(a):
    if len(a) <= 1: return a
    p = a[0]; c[0] += len(a) - 1
    return qc([x for x in a[1:] if x < p]) + [p] + qc([x for x in a[1:] if x >= p])
A = [6, 3, 9, 1, 8, 2, 7, 4, 5]
assert qc(A) == qs(A) == sorted(A) and c[0] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Recurrences — asymptotic solutions',
            'text': 'Which of the following recurrence/solution pairs is/are correct? (T(1) = Θ(1) in each case.)',
            'options': [
                'T(n) = T(n/2) + T(n/4) + n  ⇒  T(n) = Θ(n)',
                'T(n) = 2T(n/2) + n log n  ⇒  T(n) = Θ(n log² n)',
                'T(n) = T(√n) + 1  ⇒  T(n) = Θ(log log n)',
                'T(n) = 7T(n/2) + n²  ⇒  T(n) = Θ(n³)',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''- (A) Recursion-tree: level costs are n, (3/4)n, (3/4)^{2} n, … because the subproblem sizes sum to n/2 + n/4 = 3n/4 < n. A decreasing geometric series → Θ(n). **Correct.**
- (B) a = 2, b = 2, n^{log_b a} = n; f(n) = n log n = Θ(n · log^{1} n) → extended case 2 → Θ(n log² n). (Each of the log n levels costs n·log(n/2^{i}); the sum is n·Σ(log n − i) = Θ(n log² n).) **Correct.**
- (C) Substitute n = 2^{m}: S(m) = T(2^{m}) satisfies S(m) = S(m/2) + 1 → S(m) = Θ(log m) = Θ(log log n). **Correct.**
- (D) a = 7, b = 2: n^{log₂ 7} ≈ n^{2.807}, which dominates f(n) = n² polynomially → case 1 → Θ(n^{log₂ 7}), **not** Θ(n³). (This is Strassen’s recurrence.) **Incorrect.**

**Trap:** in (A), seeing two recursive calls and guessing Θ(n log n) — that needs the sizes to add up to n (as in T(n/2) + T(n/2)). In (D), 7 < 8 = 2³ is exactly why Strassen beats the cubic algorithm.''',
            'verify': '''
import math
from functools import lru_cache
@lru_cache(None)
def TA(n): return 1 if n <= 1 else TA(n // 2) + TA(n // 4) + n
@lru_cache(None)
def TB(n): return 1 if n <= 1 else 2 * TB(n // 2) + n * math.log2(n)
def TC(n): return 1 if n <= 2 else TC(math.isqrt(n)) + 1
@lru_cache(None)
def TD(n): return 1 if n <= 1 else 7 * TD(n // 2) + n * n
n = 2 ** 30
okA = 3.5 < TA(n) / n < 4.1
okB = 0.4 < TB(n) / (n * 30 * 30) < 0.6
okC = [TC(2 ** 16), TC(2 ** 32), TC(2 ** 64)] == [5, 6, 7]
okD = TD(n) / 8 ** 30 > 0.5          # false: ratio tends to 0
assert [L for L, ok in zip('ABCD', [okA, okB, okC, okD]) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'D&C counting — reverse pairs',
            'text': 'A *reverse pair* in an array A is a pair of indices (i, j) with i < j and A[i] > 2·A[j]. Such pairs can be counted in Θ(n log n) by a merge-sort-style divide and conquer. The number of reverse pairs in the array below is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [7, 2, 9, 3, 1, 8, 4, 6],
                    'label': 'A',
                },
            ],
            'answer': '7',
            'solution': '''**Concept (D&C).** Split into halves; count pairs inside each half recursively; count cross pairs (i in left, j in right) with two pointers over the *sorted* halves; then merge. Because the halves are sorted, the cross count takes linear time.

Top level: left [7, 2, 9, 3], right [1, 8, 4, 6].
- Inside the left half: (7, 2)? 7 > 4 ✓; (7, 3)? 7 > 6 ✓; (9, 3)? 9 > 6 ✓; (2, …), (9, …) no others → **3**.
- Inside the right half: (8, 4)? 8 > 8 ✗; (8, 6)? ✗; 1 is never on the right of a pair since nothing precedes it in this half → **0**.
- Cross pairs with sorted left [2, 3, 7, 9] and sorted right [1, 4, 6, 8]: 2·1 = 2 is exceeded by 3, 7, 9 → 3 pairs; 2·4 = 8 is exceeded by 9 → 1 pair; 2·6 = 12 and 2·8 = 16 → 0. Cross = **4**.

Total = 3 + 0 + 4 = **7**: (7,2), (7,3), (9,3), (7,1), (9,1), (3,1), (9,4).

**Trap:** counting ordinary inversions (A[i] > A[j]) instead — that gives a much larger number — or using ≥ instead of > (8 vs 2·4 is *not* a reverse pair).''',
            'verify': '''
A = [7, 2, 9, 3, 1, 8, 4, 6]
def rp(a):
    if len(a) <= 1: return a, 0
    m = len(a) // 2
    L, x = rp(a[:m]); R, y = rp(a[m:])
    c, i = 0, 0
    for r in R:
        while i < len(L) and L[i] <= 2 * r: i += 1
        c += len(L) - i
    return sorted(L + R), x + y + c
brute = sum(A[i] > 2 * A[j] for i in range(8) for j in range(i + 1, 8))
assert rp(A)[1] == brute == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Fast exponentiation — counting multiplications',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''m = 0
def pw(x, n):
    global m
    r = 1
    while n:
        if n & 1:
            r *= x; m += 1
        x *= x; m += 1
        n >>= 1
    return r

v = pw(2, 55)
print(m, v == 2 ** 55)''',
            'options': ['`54 True`', '`10 True`', '`9 True`', '`11 True`'],
            'answer': 'D',
            'solution': '''**Concept.** Right-to-left binary exponentiation squares x once per bit of n and multiplies it into r once per **1-bit**. Multiplications = (number of bits) + (number of 1-bits).

55 = 110111₂: 6 bits, 5 of them are 1.

Iteration trace (n in binary, ops):
- n=110111: bit 1 → r*=x, x*=x (2)
- n=11011: bit 1 → 2
- n=1101: bit 1 → 2
- n=110: bit 0 → only x*=x (1)
- n=11: bit 1 → 2
- n=1: bit 1 → 2, then n becomes 0.

Total = 2+2+2+1+2+2 = **11**; and the result is correct, so the program prints `11 True` → (D).

**Options.** (B) and (C) subtract the “wasted” operations (the first r *= x multiplies by 1, and the last squaring is never used) — a smarter implementation would save them, but this code counts them. (A) is the naive method’s n − 1.

**Tip:** the cost is Θ(log n) — between ⌊log₂ n⌋ + 1 and 2(⌊log₂ n⌋ + 1).''',
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)
assert OUTPUT.strip() == '11 True' and ANSWER == 'A' and bin(55).count('1') == 5''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Trees — diameter by divide and conquer',
            'text': 'The diameter of a binary tree is the number of **edges** on the longest path between any two nodes. It can be computed recursively as max(diam(L), diam(R), h(L) + h(R) + 2), where h(empty) = −1. The diameter of the tree below is ______.',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        1,
                        [
                            2,
                            [
                                4,
                                [
                                    7,
                                    [12],
                                    None,
                                ],
                                None,
                            ],
                            [
                                5,
                                [
                                    8,
                                    [10],
                                    None,
                                ],
                                [
                                    9,
                                    None,
                                    [11],
                                ],
                            ],
                        ],
                        [3, None, None],
                    ],
                    'caption': 'Binary tree',
                },
            ],
            'answer': '6',
            'solution': '''**Concept.** The longest path bends at some node v, using the deepest leaf of each subtree of v. The recursion returns the height and keeps the best h(L) + h(R) + 2 over all nodes.

Heights (edges) bottom-up:
- h(12) = 0, h(7) = 1, h(4) = 2.
- h(10) = 0, h(8) = 1; h(11) = 0, h(9) = 1; h(5) = 2.
- h(2) = 1 + max(2, 2) = 3; h(3) = 0.

Bend values h(L) + h(R) + 2:
- at 5: 1 + 1 + 2 = 4 (path 10–8–5–9–11)
- at 2: 2 + 2 + 2 = **6** (path 12–7–4–2–5–8–10)
- at 1 (root): 3 + 0 + 2 = 5
- others are smaller.

Diameter = **6**, and it does **not** pass through the root.

**Trap:** computing only h(left) + h(right) + 2 at the root (5), or counting nodes instead of edges (7).''',
            'verify': '''
T = [1, [2, [4, [7, [12, None, None], None], None],
         [5, [8, [10, None, None], None], [9, None, [11, None, None]]]], [3, None, None]]
best = [0]
def h(t):
    if t is None: return -1
    l, r = h(t[1]), h(t[2]); best[0] = max(best[0], l + r + 2)
    return 1 + max(l, r)
h(T)
assert best[0] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Quickselect — Lomuto partition',
            'text': 'The function below returns the k-th smallest element (k is 1-based) using repeated Lomuto partitioning. It is called as `select(A, 4)` with `A = [13, 4, 21, 9, 17, 2, 25, 11, 6, 15]`. Which of the following statements is/are TRUE?',
            'code': '''def select(A, k):
    lo, hi = 0, len(A) - 1
    while True:
        p, i = A[hi], lo - 1
        for j in range(lo, hi):
            if A[j] <= p:
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]
        q = i + 1
        if q == k - 1:
            return A[q]
        if q < k - 1:
            lo = q + 1
        else:
            hi = q - 1''',
            'options': [
                'The function returns 9',
                'Exactly 3 partitioning passes are performed',
                'After the first partitioning pass, 15 is at index 7',
                'When the function returns, A[0..2] is in ascending order',
            ],
            'answer': ['A', 'B'],
            'solution': '''**Concept.** Quickselect partitions once, then continues on **one** side only — the side containing index k − 1 = 3. Expected time Θ(n), worst case Θ(n²).

- Pass 1 on A[0..9], pivot 15: elements ≤ 15 are 13, 4, 9, 2, 11, 6 (6 of them) → pivot goes to index **6**. A = [13, 4, 9, 2, 11, 6, **15**, 17, 21, 25]. 6 > 3 → hi = 5.
- Pass 2 on A[0..5], pivot 6: elements ≤ 6 are 4, 2 → pivot to index 2. A[0..5] = [4, 2, **6**, 13, 11, 9]. 2 < 3 → lo = 3.
- Pass 3 on A[3..5] = [13, 11, 9], pivot 9: nothing ≤ 9 → pivot to index 3 → A[3..5] = [**9**, 11, 13]. q = 3 = k − 1 → return **9**.

Option by option:
- (A) The 4th smallest of {2, 4, 6, 9, 11, …} is 9. **TRUE.**
- (B) Three passes. **TRUE.**
- (C) 15 lands at index 6 (six smaller elements). **FALSE.**
- (D) A[0..2] = [4, 2, 6] — quickselect only guarantees that these are the elements *smaller* than A[3], not that they are sorted. **FALSE.**

**Trap:** expecting a sorted prefix — selection does strictly less work than sorting.''',
            'verify': '''
A = [13, 4, 21, 9, 17, 2, 25, 11, 6, 15]
passes = []; B = A[:]; lo, hi, k = 0, 9, 4
while True:
    p, i = B[hi], lo - 1
    for j in range(lo, hi):
        if B[j] <= p: i += 1; B[i], B[j] = B[j], B[i]
    B[i + 1], B[hi] = B[hi], B[i + 1]; q = i + 1; passes.append((p, q))
    if q == k - 1: break
    if q < k - 1: lo = q + 1
    else: hi = q - 1
C = A[:]; r = select(C, 4)
res = [r == 9, len(passes) == 3, passes[0] == (15, 7), C[:3] == sorted(C[:3])]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'BFS — counting shortest paths',
            'text': 'In the undirected, unweighted graph below, the number of distinct shortest paths from S to T is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'edges': [
                        ['S', 'A'],
                        ['S', 'B'],
                        ['S', 'C'],
                        ['A', 'D'],
                        ['A', 'E'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['E', 'H'],
                        ['F', 'H'],
                        ['G', 'T'],
                        ['H', 'T'],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [1.5, 2.2],
                        'B': [1.5, 1],
                        'C': [1.5, -0.2],
                        'D': [3, 2.2],
                        'E': [3, 1],
                        'F': [3, -0.2],
                        'G': [4.5, 1.6],
                        'H': [4.5, 0.4],
                        'T': [6, 1],
                    },
                },
            ],
            'answer': '6',
            'solution': '''**Concept.** Run BFS from S; the number of shortest paths to v is the sum of the counts of its neighbours one level closer: cnt(v) = Σ cnt(u) over edges u–v with dist(u) = dist(v) − 1.

- Level 0: S (1).
- Level 1: A, B, C — each 1.
- Level 2: D ← A: 1; E ← A, B: 1 + 1 = 2; F ← C: 1.
- Level 3: G ← D, E: 1 + 2 = 3; H ← E, F: 2 + 1 = 3.
- Level 4: T ← G, H: 3 + 3 = **6**.

So dist(S, T) = 4 and there are **6** shortest paths, e.g. S-A-D-G-T, S-A-E-G-T, S-B-E-G-T, S-A-E-H-T, S-B-E-H-T, S-C-F-H-T.

**Trap:** adding counts from *same-level* neighbours, or counting every simple path (which would include longer ones). Note E contributes to both G and H — a classic double-counting check.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'BFS levels and path counts',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T'],
                    'row_labels': ['dist', 'count'],
                    'rows': [
                        [0, 1, 1, 1, 2, 2, 2, 3, 3, 4],
                        [1, 1, 1, 1, 1, 2, 1, 3, 3, 6],
                    ],
                },
            ],
            'verify': '''
from collections import deque
E = "SA SB SC AD AE BE CF DG EG EH FH GT HT".split()
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
dist = {'S': 0}; cnt = {'S': 1}; q = deque('S')
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in dist: dist[v] = dist[u] + 1; cnt[v] = cnt[u]; q.append(v)
        elif dist[v] == dist[u] + 1: cnt[v] += cnt[u]
assert dist['T'] == 4 and cnt['T'] == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Complexity of a D&C function',
            'text': 'What is the asymptotic running time of `g(a, 0, n)` for a list `a` of length n?',
            'code': '''def g(a, lo, hi):
    if hi - lo < 4:
        return sum(a[lo:hi])
    s = 0
    for i in range(lo, hi):
        s += a[i]
    m = (lo + hi) // 2
    q = (hi - lo) // 4
    return (s + g(a, lo, m) + g(a, m, hi)
            + g(a, lo + q, hi - q))''',
            'options': ['Θ(n^{log₂ 3})', 'Θ(n log n)', 'Θ(n²)', 'Θ(n log² n)'],
            'answer': 'A',
            'solution': '''**Concept.** Write the recurrence from the code: the loop costs Θ(n); there are **three** recursive calls, each on a range of size ≈ n/2 (the third covers the middle half [lo + n/4, hi − n/4)).

T(n) = 3T(n/2) + Θ(n).

Master theorem: a = 3, b = 2, n^{log₂ 3} ≈ n^{1.585} dominates f(n) = n polynomially → case 1 → **Θ(n^{log₂ 3})** → (A).

Recursion-tree check: level i has 3^{i} calls of size n/2^{i}, costing (3/2)^{i}·n — an increasing geometric series dominated by the leaves: 3^{log₂ n} = n^{log₂ 3}.

**Options.** (B) assumes two calls (merge-sort shape). (C) over-estimates: the leaves are only n^{1.585}. (D) has no basis here.

**Trap:** the third call overlaps the other two, but overlap does not reduce cost — each call re-scans its range. (The base case `hi - lo < 4` is what guarantees that q ≥ 1, so the middle call is strictly smaller.) This is the same recurrence as Karatsuba multiplication.''',
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

cnt = [0]
def gc(lo, hi):
    if hi - lo < 4: return
    cnt[0] += hi - lo
    m = (lo + hi) // 2; q = (hi - lo) // 4
    gc(lo, m); gc(m, hi); gc(lo + q, hi - q)
r = []
for k in (10, 11):
    cnt[0] = 0; gc(0, 2 ** k); r.append(cnt[0])
assert 2.8 < r[1] / r[0] < 3.1 and ANSWER == 'B'
assert g(list(range(100)), 0, 100) > 0
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'DFS on a DAG — finish times and topological order',
            'text': 'DFS is run on the DAG below. The outer loop tries start vertices in alphabetical order, and each vertex’s out-neighbours are explored in alphabetical order. A global clock starts at 1 and is incremented at every discovery and every finish (so A is discovered at time 1). Let f(v) denote the finish time of v. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                    'edges': [
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['D', 'G'],
                        ['E', 'G'],
                        ['F', 'H'],
                        ['G', 'H'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [0, 0],
                        'C': [2, 2.6],
                        'D': [2, 1],
                        'E': [2, -0.6],
                        'F': [4, 2],
                        'G': [4, 0],
                        'H': [6, 1],
                    },
                },
            ],
            'options': [
                'Listing the vertices in decreasing order of f gives B, E, A, D, G, C, F, H',
                'f(A) = 11',
                'The edge B→D is a cross edge',
                'The edge A→D is a forward edge',
            ],
            'answer': ['A', 'C'],
            'solution': '''**Concept.** Decreasing finish time of a DFS on a DAG is a topological order. Edge types: tree (first discovery), forward (to an already-finished descendant), cross (to a finished vertex in another branch/tree).

Trace (discovery/finish):
- A 1 → C 2 → F 3 → H 4; H finishes 5, F 6, C 7.
- A → D 8: D→F (F finished) ; D → G 9: G→H (finished); G finishes 10, D 11. A finishes **12**.
- B 13: B→D (finished, discovered earlier in another tree) ; B → E 14: E→G finished; E finishes 15, B 16.

Finish times: H 5, F 6, C 7, G 10, D 11, A 12, E 15, B 16.

- (A) Decreasing f: B(16), E(15), A(12), D(11), G(10), C(7), F(6), H(5). **TRUE.**
- (B) f(A) = 12, not 11 (11 is f(D)). **FALSE.**
- (C) D was discovered (8) and finished (11) before B was discovered (13) → **cross** edge. **TRUE.**
- (D) When A scans D, D is still undiscovered (A explored C’s branch first, which never reaches D) → A→D is a **tree** edge. **FALSE.**

**Trap:** assuming that an edge reaching a vertex “late” must be forward; it is forward only if the target was already *discovered from u’s subtree* when u examines it.''',
            'verify': '''
G = {'A': 'CD', 'B': 'DE', 'C': 'F', 'D': 'FG', 'E': 'G', 'F': 'H', 'G': 'H', 'H': ''}
t = [0]; disc = {}; fin = {}; cls = {}
def dfs(u):
    t[0] += 1; disc[u] = t[0]
    for v in sorted(G[u]):
        if v not in disc: cls[(u, v)] = 'tree'; dfs(v)
        elif v not in fin: cls[(u, v)] = 'back'
        elif disc[u] < disc[v]: cls[(u, v)] = 'forward'
        else: cls[(u, v)] = 'cross'
    t[0] += 1; fin[u] = t[0]
for u in sorted(G):
    if u not in disc: dfs(u)
order = ''.join(sorted(G, key=lambda v: -fin[v]))
res = [order == 'BEADGCFH', fin['A'] == 11, cls[('B', 'D')] == 'cross',
       cls[('A', 'D')] == 'forward']
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
    ],
}
