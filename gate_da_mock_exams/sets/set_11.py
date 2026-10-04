# Set 11 — Merge Sort & Recurrences

SET = {
    "number": 11,
    "title": "Merge Sort & Recurrences",
    "difficulty": "Moderate",
    "focus": "merge sort traces, merge comparisons, recurrences, master theorem",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Recurrences — master theorem (extended case 2)",
            "text": ("Let T(n) = 3T(n/3) + n log₂ n for n > 1, with T(1) = 1. "
                     "Which of the following is a tight asymptotic bound for T(n)?"),
            "options": ["Θ(n log n)", "Θ(n log² n)", "Θ(n^{1.5})", "Θ(n²)"],
            "answer": "B",
            "solution": (
                "Compare f(n) = n log n with n^{log_b a} = n^{log₃ 3} = n. The two differ only by a "
                "log factor: f(n) = Θ(n^{log_b a} · log^{k} n) with k = 1. The extended case 2 of the "
                "master theorem then gives T(n) = Θ(n^{log_b a} · log^{k+1} n) = **Θ(n log² n)**.\n\n"
                "Recursion-tree check (n = 3^{m}): level i has 3^{i} subproblems of size n/3^{i}, "
                "each costing (n/3^{i}) log(n/3^{i}), so level i costs n · log(n/3^{i}) = "
                "n (m − i) log 3. Summing i = 0 … m − 1 gives n log 3 · m(m + 1)/2 = Θ(n log² n).\n\n"
                "Option analysis:\n\n"
                "- (A) Θ(n log n) would be correct for f(n) = n (plain case 2); the extra log in f "
                "adds one more log factor overall.\n"
                "- (B) **Correct.**\n"
                "- (C) and (D) would need f(n) to be polynomially larger than n, e.g. n^{1.5}.\n\n"
                "**Trap:** n log n is *not* polynomially larger than n, so case 3 does not apply."
            ),
            "verify": '''
import math
def T(m):  # T(3^m)
    t = 1
    for i in range(1, m + 1):
        n = 3 ** i
        t = 3 * t + n * math.log2(n)
    return t
r = [T(m) / (3 ** m * m * m) for m in (40, 80)]
assert abs(r[0] / r[1] - 1) < 0.05
assert T(80) / (3 ** 80 * 80) > 1.8 * T(40) / (3 ** 40 * 40)
assert ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Merge — counting comparisons",
            "text": ("The standard merge procedure is used to merge the two sorted arrays X and Y "
                     "below into one sorted array. Each step compares the current front elements of X "
                     "and Y; as soon as one array is exhausted, the remaining elements of the other "
                     "are copied without comparisons. The number of element comparisons is ______."),
            "diagrams": [{"type": "array", "values": [2, 9, 14, 20, 31], "label": "X"},
                         {"type": "array", "values": [5, 6, 15, 18, 22, 40, 41], "label": "Y"}],
            "answer": "10",
            "solution": (
                "Every comparison outputs exactly one element, so #comparisons = (number of elements "
                "output before one array runs out). Merging arrays of sizes p and q needs between "
                "min(p, q) and p + q − 1 comparisons.\n\n"
                "- 2 vs 5 → 2\n"
                "- 9 vs 5 → 5\n"
                "- 9 vs 6 → 6\n"
                "- 9 vs 15 → 9\n"
                "- 14 vs 15 → 14\n"
                "- 20 vs 15 → 15\n"
                "- 20 vs 18 → 18\n"
                "- 20 vs 22 → 20\n"
                "- 31 vs 22 → 22\n"
                "- 31 vs 40 → 31 — X is now exhausted.\n\n"
                "The remaining 40, 41 are copied directly. Comparisons = **10**.\n\n"
                "Shortcut: X runs out when its last element 31 is output. Everything ≤ 31 in Y "
                "(5, 6, 15, 18, 22 → 5 elements) is output before it, so comparisons = 5 + 5 = 10.\n\n"
                "**Trap:** answering the worst case p + q − 1 = 11; the two largest elements of Y "
                "are never compared."
            ),
            "verify": '''
X = [2, 9, 14, 20, 31]; Y = [5, 6, 15, 18, 22, 40, 41]
i = j = c = 0
while i < len(X) and j < len(Y):
    c += 1
    if X[i] <= Y[j]: i += 1
    else: j += 1
assert c == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Python — closures and late binding",
            "text": "Consider the following Python program. What is printed?",
            "code": '''fs = [lambda x: x * i for i in range(1, 4)]
print([f(2) for f in fs], sum(f(1) for f in fs))''',
            "options": ["`[2, 4, 6] 6`", "`[6, 6, 6] 9`", "`[6, 6, 6] 6`", "`[2, 4, 6] 9`"],
            "answer": "B",
            "solution": (
                "A lambda does not capture the *value* of a free variable; it captures the variable "
                "itself and looks it up **when it is called** (late binding). All three lambdas refer "
                "to the same comprehension variable `i`.\n\n"
                "- After the comprehension finishes, `i` is 3 (the last value of `range(1, 4)`).\n"
                "- `[f(2) for f in fs]` → each lambda computes 2 × 3 → `[6, 6, 6]`.\n"
                "- `sum(f(1) for f in fs)` → 3 + 3 + 3 = 9.\n\n"
                "Output: `[6, 6, 6] 9` → (B).\n\n"
                "- (A) assumes each lambda froze its own i (that requires `lambda x, i=i: x * i`); "
                "its sum would then be 1 + 2 + 3 = 6.\n"
                "- (C) mixes late binding for the list with early binding for the sum.\n"
                "- (D) mixes them the other way.\n\n"
                "**Tip:** the comprehension has its own scope in Python 3, but the closures all share "
                "that one cell for `i`."
            ),
            "verify": "assert OUTPUT.strip() == '[6, 6, 6] 9' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Stacks — feasible pop sequences",
            "text": ("The integers 1, 2, 3, 4, 5 are pushed onto an initially empty stack in this "
                     "order; pops may be interleaved arbitrarily with the pushes, and every popped "
                     "value is printed. Which of the following output sequences is/are possible?"),
            "options": ["3, 2, 5, 4, 1", "4, 2, 3, 1, 5", "1, 5, 4, 2, 3", "2, 4, 3, 5, 1"],
            "answer": ["A", "D"],
            "solution": (
                "Rule: when x is popped, every value smaller than x that is still on the stack must "
                "come out later in **decreasing** order (they are stacked in increasing order). "
                "Equivalently, a sequence is infeasible iff it contains a pattern …c…a…b… with "
                "a < b < c (a 312-pattern).\n\n"
                "- (A) 3, 2, 5, 4, 1: push 1, 2, 3, pop 3, pop 2, push 4, 5, pop 5, pop 4, pop 1. **Possible.**\n"
                "- (B) 4, 2, 3, 1, 5: when 4 is popped the stack holds 1, 2, 3 (3 on top), so 2 "
                "cannot come out before 3. **Impossible** (pattern 4, 2, 3).\n"
                "- (C) 1, 5, 4, 2, 3: after popping 5 and 4 the stack holds 2, 3 with 3 on top, so 2 "
                "cannot precede 3. **Impossible** (pattern 5, 2, 3).\n"
                "- (D) 2, 4, 3, 5, 1: push 1, 2, pop 2, push 3, 4, pop 4, pop 3, push 5, pop 5, pop 1. "
                "**Possible.**\n\n"
                "**Tip:** scan for any later pair that appears in increasing order but both smaller "
                "than an earlier element — that pair kills the sequence."
            ),
            "verify": '''
def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x: st.append(nxt); nxt += 1
        if not st or st[-1] != x: return False
        st.pop()
    return True
opts = [[3,2,5,4,1],[4,2,3,1,5],[1,5,4,2,3],[2,4,3,5,1]]
assert [c for c, s in zip("ABCD", opts) if ok(s)] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Merge sort — counting recursive calls",
            "text": ("Consider the following merge sort variant, whose base case handles lists of "
                     "length at most 2 directly. The value printed is ______."),
            "code": '''import heapq
calls = 0

def msort(a):
    global calls
    calls += 1
    if len(a) <= 2:
        return sorted(a)
    m = len(a) // 2
    return list(heapq.merge(msort(a[:m]), msort(a[m:])))

msort(list(range(13, 0, -1)))
print(calls)''',
            "answer": "15",
            "solution": (
                "The number of calls C(n) satisfies C(n) = 1 for n ≤ 2 and "
                "C(n) = 1 + C(⌊n/2⌋) + C(⌈n/2⌉) otherwise; it depends only on the length, not on the "
                "contents of the list.\n\n"
                "- C(1) = C(2) = 1\n"
                "- C(3) = 1 + C(1) + C(2) = 3\n"
                "- C(4) = 1 + C(2) + C(2) = 3\n"
                "- C(6) = 1 + C(3) + C(3) = 7\n"
                "- C(7) = 1 + C(3) + C(4) = 7\n"
                "- C(13) = 1 + C(6) + C(7) = **15**\n\n"
                "Check: the recursion tree is a full binary tree whose leaves are the base-case calls. "
                "Leaves: lengths 1, 2, 1, 2 (from the two 3s in C(6)) and 1, 2, 2, 2 (from C(7)) → 8 "
                "leaves, so the tree has 2·8 − 1 = 15 nodes.\n\n"
                "**Trap:** the classic formula 2n − 1 = 25 holds only when the base case is length ≤ 1."
            ),
            "verify": '''
def C(n): return 1 if n <= 2 else 1 + C(n // 2) + C(n - n // 2)
assert C(13) == int(ANSWER) and OUTPUT.strip() == ANSWER
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Selection sort — swaps",
            "text": ("Selection sort (in pass i, find the minimum of A[i … n−1] and swap it with A[i] "
                     "**only if** it is not already at index i) is applied to "
                     "A = [29, 10, 14, 37, 13, 5]. Which option gives the total number of swaps "
                     "performed and the array after the first two passes?"),
            "options": [
                "4 swaps; [5, 10, 14, 37, 13, 29]",
                "5 swaps; [5, 10, 14, 37, 13, 29]",
                "4 swaps; [5, 10, 13, 37, 14, 29]",
                "3 swaps; [5, 10, 29, 37, 13, 14]",
            ],
            "answer": "A",
            "solution": (
                "Selection sort makes at most n − 1 swaps; a pass whose minimum is already in place "
                "makes none.\n\n"
                "- Pass 0: min of all = 5 (index 5) → swap with 29 → [5, 10, 14, 37, 13, 29] (1).\n"
                "- Pass 1: min of A[1..5] = 10, already at index 1 → no swap.\n"
                "- Pass 2: min of A[2..5] = 13 (index 4) → [5, 10, 13, 37, 14, 29] (2).\n"
                "- Pass 3: min of A[3..5] = 14 (index 4) → [5, 10, 13, 14, 37, 29] (3).\n"
                "- Pass 4: min of A[4..5] = 29 (index 5) → [5, 10, 13, 14, 29, 37] (4).\n\n"
                "Total = **4 swaps**; after two passes the array is [5, 10, 14, 37, 13, 29] → (A).\n\n"
                "- (B) counts a swap in pass 1 (n − 1 = 5 assumes every pass swaps).\n"
                "- (C) shows the array after three passes.\n"
                "- (D) is not a state selection sort can reach.\n\n"
                "**Tip:** selection sort always does exactly n(n−1)/2 = 15 comparisons here, whatever "
                "the input; only the number of swaps depends on the data."
            ),
            "verify": '''
A = [29, 10, 14, 37, 13, 5]; sw = 0; snap = None
for i in range(len(A) - 1):
    m = min(range(i, len(A)), key=lambda k: A[k])
    if m != i: A[i], A[m] = A[m], A[i]; sw += 1
    if i == 1: snap = A[:]
assert sw == 4 and snap == [5, 10, 14, 37, 13, 29] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — separate chaining",
            "text": ("The keys 27, 45, 13, 31, 22, 40, 8, 63, 17 are inserted in that order into a hash "
                     "table with 9 slots using h(k) = k mod 9 and separate chaining; each new key is "
                     "appended at the **end** of its chain. Afterwards, every one of the nine keys is "
                     "searched for once. Counting one key comparison per chain node examined, the "
                     "total number of key comparisons over all nine successful searches is ______."),
            "answer": "19",
            "solution": (
                "With chaining, a successful search for the j-th key of a chain examines j nodes. "
                "So the total cost is ∑ over chains of 1 + 2 + … + L = L(L + 1)/2.\n\n"
                "Home slots: 27 → 0, 45 → 0, 13 → 4, 31 → 4, 22 → 4, 40 → 4, 8 → 8, 63 → 0, 17 → 8.\n\n"
                "- Slot 0: 27 → 45 → 63 (L = 3) → 1 + 2 + 3 = 6.\n"
                "- Slot 4: 13 → 31 → 22 → 40 (L = 4) → 10.\n"
                "- Slot 8: 8 → 17 (L = 2) → 3.\n\n"
                "Total = 6 + 10 + 3 = **19** (average 19/9 ≈ 2.11 comparisons per successful search, "
                "even though the load factor is only 1).\n\n"
                "**Trap:** using the textbook estimate 1 + α/2 = 1.5 per search assumes uniform "
                "hashing; these keys cluster badly because many are multiples of 9 or ≡ 4 (mod 9)."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 9,
                                   "slots": {0: [27, 45, 63], 4: [13, 31, 22, 40], 8: [8, 17]},
                                   "caption": "Chains after all insertions"}],
            "verify": '''
T = [[] for _ in range(9)]
for k in [27, 45, 13, 31, 22, 40, 8, 63, 17]: T[k % 9].append(k)
tot = sum(T[k % 9].index(k) + 1 for k in [27, 45, 13, 31, 22, 40, 8, 63, 17])
assert tot == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Binary trees — traversals",
            "text": ("Consider the binary tree shown below (G is the **left** child of E, and H, I are "
                     "the left and right children of F). Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "bintree",
                          "tree": ["A", ["B", ["D"], ["E", ["G"], None]],
                                   ["C", None, ["F", ["H"], ["I"]]]]}],
            "options": [
                "The pre-order traversal is A, B, D, E, G, C, F, H, I",
                "The in-order traversal is D, B, E, G, A, C, H, F, I",
                "The post-order traversal is D, G, E, B, H, I, F, C, A",
                "Exactly three nodes have exactly one child",
            ],
            "answer": ["A", "C"],
            "solution": (
                "Pre-order = node, left, right; in-order = left, node, right; post-order = left, right, "
                "node.\n\n"
                "- (A) Pre-order: A, then subtree B (B, D, E, G), then subtree C (C, F, H, I) → "
                "A, B, D, E, G, C, F, H, I. **TRUE.**\n"
                "- (B) In subtree E, G is the *left* child, so in-order lists G before E: "
                "D, B, G, E, A, C, H, F, I. The option puts E before G. **FALSE.**\n"
                "- (C) Post-order: D, G, E, B (left subtree), H, I, F, C (right subtree), A. **TRUE.**\n"
                "- (D) Nodes with exactly one child: E (only G) and C (only F) → two nodes. **FALSE.**\n\n"
                "**Trap:** in-order depends on whether a lone child is left or right; for pre-order and "
                "post-order the side of a lone child does not change the sequence — which is why a "
                "pre-order + post-order pair cannot always determine a binary tree uniquely."
            ),
            "verify": '''
T = ["A", ["B", ["D", None, None], ["E", ["G", None, None], None]],
     ["C", None, ["F", ["H", None, None], ["I", None, None]]]]
def pre(t): return [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
def one(t):
    if t is None: return 0
    return ((t[1] is None) != (t[2] is None)) + one(t[1]) + one(t[2])
assert pre(T) == list("ABDEGCFHI") and ino(T) != list("DBEGACHFI")
assert post(T) == list("DGEBHIFCA") and one(T) == 2
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Graph theory — handshaking lemma",
            "text": ("A simple undirected graph G is required to have 12 vertices: 5 vertices of "
                     "degree 3, 4 vertices of degree 4 and 3 vertices of degree 2. "
                     "The number of edges of G is"),
            "options": ["18", "19", "37", "No such graph exists"],
            "answer": "D",
            "solution": (
                "Handshaking lemma: ∑ deg(v) = 2|E|, so the degree sum must be **even**; equivalently, "
                "the number of odd-degree vertices must be even.\n\n"
                "Degree sum = 5·3 + 4·4 + 3·2 = 15 + 16 + 6 = 37, which is odd. Hence no graph "
                "(simple or not) can have this degree sequence → (D).\n\n"
                "- (A) 18 and (B) 19 are ⌊37/2⌋ and ⌈37/2⌉ — rounding an impossible quantity.\n"
                "- (C) 37 forgets to divide by 2 at all.\n\n"
                "Another view: there are 5 vertices of odd degree (the degree-3 ones), and every graph "
                "has an even number of odd-degree vertices.\n\n"
                "**Tip:** always check parity before computing |E| = (∑deg)/2; GATE likes to plant an "
                "infeasible degree sequence."
            ),
            "verify": '''
s = 5 * 3 + 4 * 4 + 3 * 2
assert s % 2 == 1 and ANSWER == "D"
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "NAT", "marks": 1, "topic": "Linked lists — recursive merge of sorted lists",
            "text": ("Two sorted singly linked lists (shown below) are merged by the recursive function "
                     "`merge`. The value printed is ______."),
            "diagrams": [{"type": "linkedlist", "values": [3, 8, 12, 30], "head": "a"},
                         {"type": "linkedlist", "values": [5, 9, 10, 25, 40, 41], "head": "b"}],
            "code": '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def build(xs):
    h = None
    for x in reversed(xs):
        h = Node(x, h)
    return h

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

merge(build([3, 8, 12, 30]), build([5, 9, 10, 25, 40, 41]))
print(calls)''',
            "answer": "9",
            "solution": (
                "Each non-base call fixes exactly one node of the output and recurses on the rest. "
                "The recursion stops with one extra (base-case) call as soon as one list is empty; the "
                "remainder of the other list is attached in O(1).\n\n"
                "Nodes fixed in order: 3, 5, 8, 9, 10, 12, 25, 30. After 30 is fixed, list a is empty, "
                "so the next call `merge(None, 40 → 41)` returns immediately.\n\n"
                "- Non-base calls: 8 (one per node up to and including 30).\n"
                "- Base call: 1.\n\n"
                "calls = 8 + 1 = **9**.\n\n"
                "In general, calls = (number of elements ≤ the last element of the list that runs out "
                "first, across both lists) + 1. The recursion depth is also 9, so merging long lists "
                "this way can hit Python's recursion limit (default 1000).\n\n"
                "**Trap:** answering 10 (= total nodes) — 40 and 41 are linked in without any call."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Bottom-up merge sort — pass trace",
            "text": ("Bottom-up (iterative) merge sort is applied to the array A below. In the pass "
                     "with run width w = 1, 2, 4, 8, …, adjacent runs A[i … i+w−1] and "
                     "A[i+w … i+2w−1] are merged for i = 0, 2w, 4w, …; a final run with no partner is "
                     "left unchanged. What is the array immediately **after the pass with w = 2**?"),
            "diagrams": [{"type": "array", "values": [27, 4, 19, 33, 8, 15, 2, 41, 11, 6],
                          "label": "A"}],
            "options": [
                "[4, 19, 27, 33, 2, 8, 15, 41, 11, 6]",
                "[4, 27, 19, 33, 8, 15, 2, 41, 6, 11]",
                "[2, 4, 8, 15, 19, 27, 33, 41, 6, 11]",
                "[4, 19, 27, 33, 2, 8, 15, 41, 6, 11]",
            ],
            "answer": "D",
            "solution": (
                "Bottom-up merge sort performs ⌈log₂ n⌉ passes; after the pass with width w every "
                "aligned block of 2w elements is sorted (the last block may be shorter).\n\n"
                "Pass w = 1 (merge pairs):\n\n"
                "- (27, 4) → 4, 27; (19, 33) → 19, 33; (8, 15) → 8, 15; (2, 41) → 2, 41; (11, 6) → 6, 11.\n"
                "- A = [4, 27, 19, 33, 8, 15, 2, 41, 6, 11].\n\n"
                "Pass w = 2 (merge blocks of 2 into blocks of 4):\n\n"
                "- [4, 27] + [19, 33] → [4, 19, 27, 33].\n"
                "- [8, 15] + [2, 41] → [2, 8, 15, 41].\n"
                "- [6, 11] has no partner (i = 8, i + w = 10 = n) → unchanged.\n"
                "- A = [4, 19, 27, 33, 2, 8, 15, 41, 6, 11].\n\n"
                "Later passes: w = 4 gives [2, 4, 8, 15, 19, 27, 33, 41, 6, 11] and w = 8 finishes the sort.\n\n"
                "Option analysis:\n\n"
                "- (A) forgets that the w = 1 pass already sorted the leftover pair (11, 6).\n"
                "- (B) is the state after the w = 1 pass.\n"
                "- (C) is the state after the w = 4 pass.\n"
                "- (D) **Correct.**\n\n"
                "**Trap:** unlike top-down merge sort (which splits 10 as 5 + 5), bottom-up merging "
                "uses power-of-two aligned blocks, so the intermediate states differ."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each pass",
                                   "row_labels": ["input", "w = 1", "w = 2", "w = 4", "w = 8"],
                                   "col_labels": [str(i) for i in range(10)],
                                   "rows": [[27, 4, 19, 33, 8, 15, 2, 41, 11, 6],
                                            [4, 27, 19, 33, 8, 15, 2, 41, 6, 11],
                                            [4, 19, 27, 33, 2, 8, 15, 41, 6, 11],
                                            [2, 4, 8, 15, 19, 27, 33, 41, 6, 11],
                                            [2, 4, 6, 8, 11, 15, 19, 27, 33, 41]],
                                   "highlight": [[2, c] for c in range(10)]}],
            "verify": '''
A = [27, 4, 19, 33, 8, 15, 2, 41, 11, 6]; n = len(A); w = 1; states = {}
while w < n:
    for i in range(0, n, 2 * w):
        A[i:i + 2 * w] = sorted(A[i:i + 2 * w]) if i + w < n else A[i:i + 2 * w]
    states[w] = A[:]
    w *= 2
assert states[2] == [4, 19, 27, 33, 2, 8, 15, 41, 6, 11]
assert states[1] == [4, 27, 19, 33, 8, 15, 2, 41, 6, 11]
assert states[4] == [2, 4, 8, 15, 19, 27, 33, 41, 6, 11] and ANSWER == "D"
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Merge sort — worst-case comparison recurrence",
            "text": ("For top-down merge sort that splits n elements into ⌊n/2⌋ and ⌈n/2⌉, the "
                     "worst-case number of element comparisons W(n) satisfies\n"
                     "W(1) = 0,   W(n) = W(⌊n/2⌋) + W(⌈n/2⌉) + n − 1 for n ≥ 2.\n"
                     "The value of W(13) is ______."),
            "answer": "37",
            "solution": (
                "The term n − 1 is the worst case of one merge of runs whose sizes add up to n "
                "(every element except the last is output after a comparison).\n\n"
                "Evaluate bottom-up:\n\n"
                "- W(2) = W(1) + W(1) + 1 = 1\n"
                "- W(3) = W(1) + W(2) + 2 = 3\n"
                "- W(4) = W(2) + W(2) + 3 = 5\n"
                "- W(6) = W(3) + W(3) + 5 = 11\n"
                "- W(7) = W(3) + W(4) + 6 = 14\n"
                "- W(13) = W(6) + W(7) + 12 = 11 + 14 + 12 = **37**\n\n"
                "Closed form check: W(n) = n⌈log₂ n⌉ − 2^{⌈log₂ n⌉} + 1. For n = 13, ⌈log₂ 13⌉ = 4, so "
                "W(13) = 52 − 16 + 1 = 37. ✓\n\n"
                "Compare with the information-theoretic lower bound ⌈log₂ 13!⌉ = 33: merge sort is "
                "within a few comparisons of optimal.\n\n"
                "**Traps:**\n\n"
                "- Using n log₂ n ≈ 48.1 (only an asymptotic estimate).\n"
                "- Writing W(13) = 2W(6) + 12 = 34 — the halves are 6 and **7**, not 6 and 6."
            ),
            "verify": '''
import math
def W(n): return 0 if n <= 1 else W(n // 2) + W(n - n // 2) + n - 1
assert W(13) == int(ANSWER) == 13 * 4 - 16 + 1
assert math.ceil(math.log2(math.factorial(13))) == 33
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Recurrences — which are Θ(n log n)?",
            "text": ("Which of the following recurrences has/have the solution T(n) = Θ(n log n)? "
                     "(Assume T(n) = Θ(1) for small n.)"),
            "options": [
                "T(n) = 2T(n/2) + 5n",
                "T(n) = 4T(n/2) + n log n",
                "T(n) = T(n/3) + T(2n/3) + n",
                "T(n) = 8T(n/4) + n^{1.5}",
            ],
            "answer": ["A", "C"],
            "solution": (
                "For T(n) = aT(n/b) + f(n) compare f(n) with n^{log_b a}.\n\n"
                "- (A) a = 2, b = 2 → n^{log₂ 2} = n; f = 5n = Θ(n) → case 2 → Θ(n log n). **TRUE.**\n"
                "- (B) a = 4, b = 2 → n^{2}; f = n log n = O(n^{2−ε}) → case 1 → Θ(n²). **FALSE.**\n"
                "- (C) Not in master-theorem form; use the recursion tree. Every level's subproblem "
                "sizes add up to at most n, so each full level costs n. The shortest root-to-leaf path "
                "(always n/3) has log₃ n levels and the longest (always 2n/3) has log_{3/2} n levels. "
                "So n log₃ n ≤ T(n) ≤ n log_{3/2} n, i.e. Θ(n log n). **TRUE.**\n"
                "- (D) a = 8, b = 4 → n^{log₄ 8} = n^{1.5} = f(n) → case 2 → Θ(n^{1.5} log n). "
                "**FALSE** (it has a log factor, but the polynomial part is n^{1.5}).\n\n"
                "**Trap:** in (D) the matching of f(n) with n^{log_b a} produces the “log n” factor, "
                "tempting a hasty Θ(n log n). In (C) an unbalanced split still gives n log n because "
                "the split is a constant fraction."
            ),
            "verify": '''
import math
from functools import lru_cache
@lru_cache(None)
def A(n): return 1 if n <= 1 else 2 * A(n // 2) + 5 * n
@lru_cache(None)
def B(n): return 1 if n <= 1 else 4 * B(n // 2) + n * math.log2(n)
@lru_cache(None)
def C(n): return 1 if n <= 2 else C(n // 3) + C(n - n // 3) + n
@lru_cache(None)
def D(n): return 1 if n <= 1 else 8 * D(n // 4) + n ** 1.5
r = lambda f, n: f(n) / (n * math.log2(n))
ok = lambda f: r(f, 2 ** 20) / r(f, 2 ** 10) < 1.3
assert ok(A) and ok(C) and not ok(B) and not ok(D)
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Merge sort — counting during merge (inversions)",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def sort_count(a):
    if len(a) < 2:
        return a, 0
    m = len(a) // 2
    L, x = sort_count(a[:m])
    R, y = sort_count(a[m:])
    out, i, j, c = [], 0, 0, 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
            c += len(L) - i
    return out + L[i:] + R[j:], x + y + c

print(sort_count([6, 2, 9, 4, 1, 8, 3, 7])[1])''',
            "answer": "14",
            "solution": (
                "When R[j] is output before the remaining L[i …], R[j] is smaller than all "
                "len(L) − i elements still waiting in L, each of which stood **before** it in the "
                "original array. So `c` counts exactly the inversions that cross the split, and the "
                "function returns the total number of **inversions** (pairs i < j with a[i] > a[j]).\n\n"
                "Direct count for [6, 2, 9, 4, 1, 8, 3, 7]:\n\n"
                "- 6 > 2, 4, 1, 3 → 4\n"
                "- 2 > 1 → 1\n"
                "- 9 > 4, 1, 8, 3, 7 → 5\n"
                "- 4 > 1, 3 → 2\n"
                "- 1 → 0\n"
                "- 8 > 3, 7 → 2\n"
                "- 3 → 0\n\n"
                "Total = 4 + 1 + 5 + 2 + 2 = **14**.\n\n"
                "Cross-check via the recursion: [6, 2, 9, 4] has 3 inversions ((6,2), (6,4), (9,4)), "
                "[1, 8, 3, 7] has 2 ((8,3), (8,7)), and the top-level merge of [2, 4, 6, 9] with "
                "[1, 3, 7, 8] adds 4 (when 1 is output) + 3 (for 3) + 1 (for 7) + 1 (for 8) = 9; "
                "3 + 2 + 9 = 14.\n\n"
                "**Trap:** adding 1 per out-of-order step (instead of len(L) − i) counts only the "
                "number of times a right element wins, not the inversions."
            ),
            "verify": '''
a = [6, 2, 9, 4, 1, 8, 3, 7]
inv = sum(1 for i in range(8) for j in range(i + 1, 8) if a[i] > a[j])
assert inv == int(ANSWER) and OUTPUT.strip() == ANSWER
assert sort_count([6, 2, 9, 4])[1] == 3 and sort_count([1, 8, 3, 7])[1] == 2
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Recurrences — complexity of a recursive function",
            "text": ("Consider the following Python function. Which of the following best describes "
                     "its running time as a function of n?"),
            "code": '''def work(n):
    if n <= 1:
        return 1
    t, i = 0, 1
    while i < n:
        t += 1
        i *= 2
    a = work(n // 2)
    b = work(n // 2)
    c = work(n // 2)
    return a + b + c + t''',
            "options": ["Θ(n log n)", "Θ(n^{log₂ 3})", "Θ(n^{log₂ 3} · log n)", "Θ(n²)"],
            "answer": "B",
            "solution": (
                "The while-loop doubles i, so it runs ⌈log₂ n⌉ times. Three recursive calls on n/2 "
                "follow, giving\n"
                "T(n) = 3T(n/2) + Θ(log n).\n\n"
                "Master theorem: n^{log_b a} = n^{log₂ 3} ≈ n^{1.585}. The driving function "
                "f(n) = log n is O(n^{1.585 − ε}) for, e.g., ε = 0.5, so **case 1** applies and "
                "T(n) = Θ(n^{log₂ 3}).\n\n"
                "Intuition: the recursion tree has 3^{log₂ n} = n^{log₂ 3} leaves, each Θ(1), and the "
                "internal work (a log at each node) is dominated by the leaf count since the number of "
                "nodes grows geometrically by a factor of 3 per level.\n\n"
                "Option analysis:\n\n"
                "- (A) would need 2 calls and linear work per call.\n"
                "- (B) **Correct.**\n"
                "- (C) would require f(n) = Θ(n^{log₂ 3}) (case 2).\n"
                "- (D) would need 4 calls on n/2.\n\n"
                "**Trap:** storing the three results in `a`, `b`, `c` does **not** memoise anything — "
                "each call recomputes the same subproblem. Replacing them by a single call times 3 "
                "would give T(n) = T(n/2) + log n = Θ(log² n)."
            ),
            "verify": '''
import math
cnt = [0]
def W(n):
    cnt[0] += 1
    if n <= 1: return 1
    i = 1
    while i < n: cnt[0] += 1; i *= 2
    return W(n // 2) + W(n // 2) + W(n // 2)
def cost(n): cnt[0] = 0; W(n); return cnt[0]
e = math.log2(3)
r1, r2 = cost(2 ** 8) / 2 ** (8 * e), cost(2 ** 12) / 2 ** (12 * e)
assert abs(r1 / r2 - 1) < 0.1 and work(16) > 0 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MSQ", "marks": 2, "topic": "Heaps — repeated insertion into a min-heap",
            "text": ("The keys 35, 22, 41, 18, 9, 27, 14, 30 are inserted one at a time, in that "
                     "order, into an initially empty binary **min-heap** stored in an array "
                     "(0-indexed; each insertion appends the key and sifts it up). A *swap* is one "
                     "child–parent exchange. Which of the following statements is/are TRUE?"),
            "options": [
                "The final heap array is [9, 18, 14, 30, 22, 41, 27, 35]",
                "The insertions perform 7 swaps in total",
                "Bottom-up build-heap applied to the array [35, 22, 41, 18, 9, 27, 14, 30] "
                "produces the same final array",
                "After one DELETE-MIN on the final heap, the root holds 14",
            ],
            "answer": ["A", "D"],
            "solution": (
                "Insertion = append at the end, then swap upward while the parent is larger.\n\n"
                "- 35 → [35]\n"
                "- 22 → swap with 35 → [22, 35] (1)\n"
                "- 41 → [22, 35, 41] (0)\n"
                "- 18 → swap with 35, then with 22 → [18, 22, 41, 35] (2)\n"
                "- 9 → swap with 22, then with 18 → [9, 18, 41, 35, 22] (2)\n"
                "- 27 → swap with 41 → [9, 18, 27, 35, 22, 41] (1)\n"
                "- 14 → swap with 27 → [9, 18, 14, 35, 22, 41, 27] (1)\n"
                "- 30 → swap with 35 → [9, 18, 14, 30, 22, 41, 27, 35] (1)\n\n"
                "- (A) **TRUE.**\n"
                "- (B) Swaps = 1 + 0 + 2 + 2 + 1 + 1 + 1 = 8, not 7. **FALSE.**\n"
                "- (C) Bottom-up build-heap (sift-down at i = 3, 2, 1, 0) gives "
                "[9, 18, 14, 30, 22, 27, 41, 35]: at i = 2 the key 41 is swapped with the *smaller* "
                "child 14, leaving 27 at index 5. The arrays differ at indices 5, 6. **FALSE.**\n"
                "- (D) DELETE-MIN moves 35 to the root: [35, 18, 14, 30, 22, 41, 27]; 35 swaps with "
                "the smaller child 14, then with 27 → [14, 18, 27, 30, 22, 41, 35]. Root = 14. **TRUE.**\n\n"
                "**Trap:** the heap built by n insertions need not equal the one built bottom-up — "
                "both are valid heaps on the same keys."
            ),
            "solution_diagrams": [{"type": "heap", "values": [9, 18, 14, 30, 22, 41, 27, 35],
                                   "caption": "Min-heap after the eight insertions"}],
            "verify": '''
h = []; sw = 0
for x in [35, 22, 41, 18, 9, 27, 14, 30]:
    h.append(x); i = len(h) - 1
    while i and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p; sw += 1
def down(a, i, n):
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] < a[m]: m = l
        if r < n and a[r] < a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; i = m
b = [35, 22, 41, 18, 9, 27, 14, 30]
for i in range(3, -1, -1): down(b, i, 8)
g = h[:]; g[0] = g.pop(); down(g, 0, 7)
assert h == [9, 18, 14, 30, 22, 41, 27, 35] and sw == 8 and b != h and g[0] == 14
assert sorted(ANSWER) == ["A", "D"]
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "NAT", "marks": 2, "topic": "BFS — counting shortest paths",
            "text": ("In the unweighted undirected graph below, the number of distinct shortest "
                     "paths from S to T is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["S", "A", "B", "C", "D", "E", "F", "G", "T"],
                          "edges": [["S", "A"], ["S", "B"], ["A", "C"], ["A", "D"], ["B", "D"],
                                    ["B", "E"], ["C", "D"], ["C", "F"], ["D", "F"], ["D", "G"],
                                    ["E", "G"], ["F", "T"], ["G", "T"]],
                          "pos": {"S": [0, 1], "A": [1.5, 2], "B": [1.5, 0], "C": [3, 2.4],
                                  "D": [3, 1], "E": [3, -0.4], "F": [4.5, 2], "G": [4.5, 0],
                                  "T": [6, 1]}}],
            "answer": "6",
            "solution": (
                "Run BFS from S and, for every vertex v, let σ(v) be the number of shortest paths. "
                "σ(S) = 1 and σ(v) = ∑ σ(u) over neighbours u with dist(u) = dist(v) − 1. Edges "
                "between vertices on the **same** level never lie on a shortest path.\n\n"
                "- Level 0: S (σ = 1).\n"
                "- Level 1: A (σ = 1), B (σ = 1).\n"
                "- Level 2: C (from A) σ = 1; D (from A and B) σ = 2; E (from B) σ = 1.\n"
                "- Level 3: F (from C, D) σ = 1 + 2 = 3; G (from D, E) σ = 2 + 1 = 3.\n"
                "- Level 4: T (from F, G) σ = 3 + 3 = **6**.\n\n"
                "The edge C–D joins two level-2 vertices and is ignored.\n\n"
                "Listing them: S-A-C-F-T, S-A-D-F-T, S-B-D-F-T, S-A-D-G-T, S-B-D-G-T, S-B-E-G-T.\n\n"
                "**Trap:** counting paths that use C–D (e.g. S-A-C-D-F-T) — they have length 5, "
                "not 4."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "BFS distance and path count σ",
                                   "col_labels": ["S", "A", "B", "C", "D", "E", "F", "G", "T"],
                                   "row_labels": ["dist", "σ"],
                                   "rows": [[0, 1, 1, 2, 2, 2, 3, 3, 4],
                                            [1, 1, 1, 1, 2, 1, 3, 3, 6]]}],
            "verify": '''
from collections import deque
E = [("S","A"),("S","B"),("A","C"),("A","D"),("B","D"),("B","E"),("C","D"),
     ("C","F"),("D","F"),("D","G"),("E","G"),("F","T"),("G","T")]
G = {}
for u, v in E: G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
d = {"S": 0}; s = {"S": 1}; q = deque(["S"])
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in d: d[v] = d[u] + 1; s[v] = 0; q.append(v)
        if d[v] == d[u] + 1: s[v] += s[u]
assert s["T"] == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MCQ", "marks": 2, "topic": "Dijkstra — order of finalisation",
            "text": ("Dijkstra's algorithm is run from P on the weighted undirected graph below. "
                     "Which option gives the order in which vertices are removed from the priority "
                     "queue (finalised), together with the final distance d(U)?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U"],
                          "edges": [["P", "Q", 4], ["P", "R", 1], ["R", "Q", 2], ["R", "S", 7],
                                    ["Q", "S", 5], ["Q", "T", 9], ["S", "T", 2], ["S", "U", 6],
                                    ["T", "U", 1], ["R", "U", 12]],
                          "pos": {"P": [0, 1], "Q": [2, 2], "R": [2, 0], "S": [4, 1],
                                  "T": [6, 2], "U": [6, 0]}}],
            "options": [
                "P, R, Q, S, T, U with d(U) = 11",
                "P, Q, R, S, T, U with d(U) = 11",
                "P, R, Q, S, U, T with d(U) = 13",
                "P, R, Q, T, S, U with d(U) = 12",
            ],
            "answer": "A",
            "solution": (
                "Dijkstra always finalises the vertex with the smallest tentative distance; with "
                "non-negative weights the finalisation order is the order of increasing true distance.\n\n"
                "- Extract P (0): Q = 4, R = 1.\n"
                "- Extract R (1): Q = min(4, 1 + 2) = 3, S = 8, U = 13.\n"
                "- Extract Q (3): S = min(8, 3 + 5) = 8 (tie, unchanged), T = 12.\n"
                "- Extract S (8): T = min(12, 8 + 2) = 10, U = min(13, 8 + 6) = 13.\n"
                "- Extract T (10): U = min(13, 10 + 1) = 11.\n"
                "- Extract U (11).\n\n"
                "Order: P, R, Q, S, T, U and d(U) = 11 → (A). S is reached with cost 8 along two "
                "paths, P–R–S (1 + 7) and P–R–Q–S (3 + 5); either way S–T–U adds 2 + 1 = 3, so "
                "d(U) = 11 — cheaper than the direct edges R–U (13) and S–U (14).\n\n"
                "- (B) extracts Q before R although d(R) = 1 < 3.\n"
                "- (C) keeps the direct edge R–U (13) and finalises U too early.\n"
                "- (D) finalises T (12) before S (8) — T's value 12 is only tentative at that time.\n\n"
                "**Trap:** the edge P–Q (4) is not Q's final distance; it improves to 3 through R."
            ),
            "verify": '''
import heapq
E = [("P","Q",4),("P","R",1),("R","Q",2),("R","S",7),("Q","S",5),("Q","T",9),
     ("S","T",2),("S","U",6),("T","U",1),("R","U",12)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: 10 ** 9 for v in G}; d["P"] = 0; pq = [(0, "P")]; order = []
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u] or u in order: continue
    order.append(u)
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert order == list("PRQSTU") and d["U"] == 11 and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Python — dictionaries and stable sorting",
            "text": "Consider the following Python program. What is printed?",
            "code": '''text = ("data beats models but more data beats "
        "better models and data wins")
freq = {}
for w in text.split():
    freq[w] = freq.get(w, 0) + 1
r = sorted(freq, key=lambda w: (-freq[w], len(w)))
print(r[2:6])''',
            "options": [
                "`['models', 'and', 'but', 'wins']`",
                "`['models', 'and', 'but', 'more']`",
                "`['models', 'but', 'and', 'more']`",
                "`['beats', 'models', 'but', 'and']`",
            ],
            "answer": "C",
            "solution": (
                "Since Python 3.7 a dict remembers **insertion order**, and `sorted` is **stable**: "
                "items with equal keys keep their original relative order.\n\n"
                "Frequencies (insertion order): data 3, beats 2, models 2, but 1, more 1, better 1, "
                "and 1, wins 1.\n\n"
                "Sort key = (−frequency, length):\n\n"
                "- data (−3, 4)\n"
                "- beats (−2, 5), models (−2, 6)\n"
                "- frequency-1 words by length: but (3), and (3), more (4), wins (4), better (6). "
                "Ties but/and and more/wins keep insertion order: but before and, more before wins.\n\n"
                "r = [data, beats, models, but, and, more, wins, better]; r[2:6] = "
                "['models', 'but', 'and', 'more'] → (C).\n\n"
                "- (A) breaks the but/and tie alphabetically and also mis-orders more/wins.\n"
                "- (B) breaks the but/and tie alphabetically — `sorted` never compares the words "
                "themselves here, only the key tuples.\n"
                
                "- (D) uses r[1:5] (off-by-one in the slice start).\n\n"
                "**Tip:** to break ties alphabetically you must add `w` to the key tuple explicitly, "
                "e.g. `key=lambda w: (-freq[w], len(w), w)`; then 'and' would precede 'but'."
            ),
            "verify": "assert OUTPUT.strip() == \"['models', 'but', 'and', 'more']\" and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Merge sort — stability",
            "text": ("Consider the following Python merge sort, applied to records (key, tag). "
                     "Which of the following statements is/are TRUE?"),
            "code": '''def msort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    L, R = msort(a[:m]), msort(a[m:])
    out = []
    while L and R:
        if L[0][0] < R[0][0]:
            out.append(L.pop(0))
        else:
            out.append(R.pop(0))
    return out + L + R

recs = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e')]
res = msort(recs)
print(''.join(t for _, t in res))''',
            "options": [
                "The program prints `dbeca`",
                "If `<` is replaced by `<=`, the program prints `bdace`",
                "The list `recs` is modified by the call `msort(recs)`",
                "In the output, the records with key 2 appear in the exact reverse of their input order",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Merge sort is stable only if, on equal keys, the merge takes the element from the "
                "**left** run. With `<`, ties go to the right run, so equal keys can be reordered.\n\n"
                "Trace (split 2 | 3):\n\n"
                "- Left [(2,a), (1,b)]: 2 < 1 false → b, then a → [b, a].\n"
                "- Right [(2,c)] | [(1,d), (2,e)]: inner merge gives [d, e]; then c vs d: 2 < 1 false "
                "→ d; c vs e: 2 < 2 false → e; then c → [d, e, c].\n"
                "- Top: b vs d: 1 < 1 false → d; b vs e: 1 < 2 → b; a vs e: 2 < 2 false → e; a vs c: "
                "false → c; then a. Output **dbeca**.\n\n"
                "- (A) TRUE.\n"
                "- (B) With `<=` ties go left and the sort is stable: key-1 records b, d then key-2 "
                "records a, c, e → `bdace`. TRUE.\n"
                "- (C) FALSE — `msort` only slices (`a[:m]` makes copies) and pops from those new lists; "
                "a 1-element `recs` would be returned as is, but nothing ever mutates it.\n"
                "- (D) TRUE — input order a, c, e; output order e, c, a.\n\n"
                "**Trap:** the sorted *keys* are correct either way; only the tags reveal the "
                "instability. (Also note `pop(0)` is O(len) on Python lists, so this version is "
                "slower than index-based merging.)"
            ),
            "verify": '''
import copy
r0 = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (2, 'e')]
assert OUTPUT.strip() == "dbeca" and recs == r0
def ms2(a):
    if len(a) <= 1: return a
    m = len(a) // 2; L, R = ms2(a[:m]), ms2(a[m:]); out = []
    while L and R: out.append(L.pop(0) if L[0][0] <= R[0][0] else R.pop(0))
    return out + L + R
assert "".join(t for _, t in ms2(r0)) == "bdace"
assert [t for k, t in res if k == 2] == ["e", "c", "a"]
assert sorted(ANSWER) == ["A", "B", "D"]
''',
        },
    ],
}
