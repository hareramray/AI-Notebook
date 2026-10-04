# Set 24 — Sorting Properties (GATE-level)
SET = {
    "number": 24,
    "title": "Sorting Properties",
    "difficulty": "GATE-level",
    "focus": "stability, inversions, adaptivity, in-place, comparison lower bounds",
    "questions": [
        # ---------------------------------------------------------------- Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — stable multi-pass sorting",
            "text": "What is printed by the following Python program?",
            "code": '''recs = [("ravi", 3), ("asha", 1), ("dev", 3),
        ("mina", 2), ("om", 1), ("lata", 2)]
r = sorted(recs, key=lambda t: t[0])
r = sorted(r, key=lambda t: -t[1])
print([name for name, _ in r])''',
            "options": ["`['ravi', 'dev', 'mina', 'lata', 'asha', 'om']`",
                        "`['dev', 'ravi', 'lata', 'mina', 'asha', 'om']`",
                        "`['asha', 'om', 'lata', 'mina', 'dev', 'ravi']`",
                        "`['dev', 'ravi', 'mina', 'lata', 'om', 'asha']`"],
            "answer": "B",
            "solution": (
                "**Concept.** Python's `sorted` is **stable**: records with equal keys keep their relative "
                "order from the input. Sorting first by the *secondary* key (name) and then by the *primary* "
                "key (score, descending via `-t[1]`) therefore yields 'score descending, ties by name "
                "ascending'.\n\n"
                "**Trace.**\n"
                "- After sort by name: asha(1), dev(3), lata(2), mina(2), om(1), ravi(3).\n"
                "- Stable sort by −score: score 3 group keeps order dev, ravi; score 2 group lata, mina; "
                "score 1 group asha, om.\n"
                "- Output: `['dev', 'ravi', 'lata', 'mina', 'asha', 'om']`.\n\n"
                "**Options.**\n"
                "- (A) keeps the *original* input order within ties — that would be the result of the second "
                "sort alone.\n"
                "- (C) sorts by score ascending.\n"
                "- (D) reverses the order inside each tie group, as an unstable sort might.\n\n"
                "**Tip:** this 'sort by least significant key first' trick is exactly how LSD radix sort works, "
                "and it is correct only because each pass is stable. Equivalent one-liner: "
                "`sorted(recs, key=lambda t: (-t[1], t[0]))`."
            ),
            "verify": '''
exp = [n for n, _ in sorted(recs, key=lambda t: (-t[1], t[0]))]
assert OUTPUT.strip() == str(exp) and ANSWER == 'B'
''',
        },
        # ---------------------------------------------------------------- Q2
        {
            "type": "NAT", "marks": 1, "topic": "Bubble sort — adaptivity (rabbits and turtles)",
            "text": ("Consider bubble sort with early termination:\n\n"
                     "`for i in range(n-1):` one left-to-right pass over A[0..n−2−i] swapping adjacent "
                     "out-of-order pairs; `if no swap was made in this pass: break`.\n\n"
                     "Let p be the number of passes executed on X = [2, 3, 4, 5, 6, 1] and q the number of passes "
                     "executed on Y = [6, 1, 2, 3, 4, 5]. The value of p + q is ______."),
            "answer": "7",
            "solution": (
                "**Concept.** In one left-to-right pass a large element can travel any distance to the right "
                "(a *rabbit*), but a small element moves only **one** position to the left (a *turtle*). "
                "Bubble sort's pass count is governed by how far the worst element must move left.\n\n"
                "**X = [2, 3, 4, 5, 6, 1]** — the turtle 1 must move 5 places left, one per pass:\n"
                "- pass 1 → [2, 3, 4, 5, 1, 6], pass 2 → [2, 3, 4, 1, 5, 6], …, pass 5 → [1, 2, 3, 4, 5, 6].\n"
                "- Pass 5 still swapped, but the loop has only n − 1 = 5 iterations, so it ends. p = **5**.\n\n"
                "**Y = [6, 1, 2, 3, 4, 5]** — the rabbit 6 reaches the end in one pass:\n"
                "- pass 1 → [1, 2, 3, 4, 5, 6] (5 swaps); pass 2 makes no swap → break. q = **2**.\n\n"
                "p + q = 5 + 2 = **7**.\n\n"
                "**Trap:** both arrays have exactly 5 inversions, so they need the same number of *swaps*, "
                "yet the number of *passes* differs greatly. Passes = 1 + max over elements of how far left "
                "they must move (capped at n − 1)."
            ),
            "verify": '''
def passes(A):
    A = A[:]; n = len(A); p = 0
    for i in range(n - 1):
        p += 1; sw = False
        for j in range(n - 1 - i):
            if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]; sw = True
        if not sw: break
    return p
assert passes([2, 3, 4, 5, 6, 1]) + passes([6, 1, 2, 3, 4, 5]) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Sorting — stability of standard algorithms",
            "text": ("Each algorithm below is implemented in its standard textbook form on an array and sorts "
                     "records by key in ascending order. Which of them is/are **stable** for every input?"),
            "options": [
                "Insertion sort that shifts A[j] right while A[j] > key",
                "Selection sort that swaps the minimum of A[i..n−1] (first occurrence) with A[i]",
                "Merge sort whose merge takes from the left half when the two front keys are equal",
                "Quicksort using the Lomuto partition with the last element as pivot",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** A sort is stable if equal keys keep their input order. Algorithms that move "
                "elements only between *adjacent* positions (or merge with a left-preference on ties) are "
                "stable; algorithms that make long-distance swaps usually are not.\n\n"
                "- (A) **Stable.** The strict test `A[j] > key` stops at an equal key, so a later equal key is "
                "placed after it.\n"
                "- (B) **Not stable.** The long swap can jump an element over its equal twin. Example: "
                "[2a, 2b, 1] → swap 2a with 1 → [1, 2b, 2a].\n"
                "- (C) **Stable.** On ties the left (earlier) record is output first.\n"
                "- (D) **Not stable.** Example [1a, 1b, 0]: pivot 0; nothing ≤ 0 in the loop, final swap "
                "exchanges A[0] and A[2] → [0, 1b, 1a].\n\n"
                "**Trap:** stability is a property of the *implementation*: insertion sort with `>=` or merge "
                "sort preferring the right half on ties become unstable."
            ),
            "verify": '''
import random
def ins(A, key):
    A = A[:]
    for i in range(1, len(A)):
        x, j = A[i], i - 1
        while j >= 0 and key(A[j]) > key(x): A[j + 1] = A[j]; j -= 1
        A[j + 1] = x
    return A
def sel(A, key):
    A = A[:]
    for i in range(len(A) - 1):
        m = min(range(i, len(A)), key=lambda k: (key(A[k]), k))
        A[i], A[m] = A[m], A[i]
    return A
def ms(A, key):
    if len(A) <= 1: return A
    m = len(A) // 2; L, R = ms(A[:m], key), ms(A[m:], key); o = []
    while L and R: o.append(L.pop(0) if key(L[0]) <= key(R[0]) else R.pop(0))
    return o + L + R
def qs(A, key):
    A = A[:]
    def part(lo, hi):
        p, i = key(A[hi]), lo - 1
        for j in range(lo, hi):
            if key(A[j]) <= p: i += 1; A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]; return i + 1
    def rec(lo, hi):
        if lo < hi: q = part(lo, hi); rec(lo, q - 1); rec(q + 1, hi)
    rec(0, len(A) - 1); return A
random.seed(3)
k = lambda t: t[0]
stable = {}
for name, f in zip("ABCD", [ins, sel, ms, qs]):
    ok = True
    for _ in range(300):
        A = [(random.randint(0, 3), i) for i in range(7)]
        ok &= f(A, k) == sorted(A, key=k)
    stable[name] = ok
assert sorted(x for x in stable if stable[x]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q4
        {
            "type": "NAT", "marks": 1, "topic": "Binary search — lower bound with duplicates",
            "text": ("Consider the following Python program. It prints two integers p and q. "
                     "The value of p + q is ______."),
            "code": '''def lb(A, x):
    lo, hi, c = 0, len(A), 0
    while lo < hi:
        mid = (lo + hi) // 2
        c += 1
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo, c

A = [2, 5, 5, 5, 8, 8, 11, 14, 14, 14, 14, 20]
p, q = lb(A, 14)
print(p, q)''',
            "answer": "11",
            "solution": (
                "**Concept.** This is the half-open `lower_bound` search: it returns the first index whose "
                "value is ≥ x, and it never stops early on equality — it keeps shrinking until lo = hi.\n\n"
                "**Trace** (n = 12, x = 14):\n"
                "- lo=0, hi=12 → mid=6, A[6]=11 < 14 → lo=7. (c=1)\n"
                "- lo=7, hi=12 → mid=9, A[9]=14 ≥ 14 → hi=9. (c=2)\n"
                "- lo=7, hi=9 → mid=8, A[8]=14 → hi=8. (c=3)\n"
                "- lo=7, hi=8 → mid=7, A[7]=14 → hi=7. (c=4)\n"
                "- lo = hi = 7 → stop.\n\n"
                "p = 7 (the first 14), q = 4 iterations; p + q = **11**.\n\n"
                "**Trap:** a classic binary search would stop at the first probe that hits a 14 (index 9) "
                "and return a *non-leftmost* occurrence. Lower-bound search always runs ⌈log₂(n+1)⌉ or "
                "⌊log₂(n+1)⌋ iterations regardless of where x is found."
            ),
            "solution_diagrams": [{"type": "array", "values": [2, 5, 5, 5, 8, 8, 11, 14, 14, 14, 14, 20],
                                   "pointers": {"lo=hi": 7}, "highlight": [6, 9, 8, 7],
                                   "caption": "Probed indices 6, 9, 8, 7; answer index 7"}],
            "verify": '''
import bisect
A = [2, 5, 5, 5, 8, 8, 11, 14, 14, 14, 14, 20]
assert bisect.bisect_left(A, 14) == p and sum(map(int, OUTPUT.split())) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks — stack permutations",
            "text": ("The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack in this order; pops "
                     "may be performed at any time, and each popped value is printed. Which of the following "
                     "output sequences is **not** possible?"),
            "options": ["3 2 5 6 4 1", "4 5 3 6 1 2", "1 2 3 6 5 4", "4 3 5 2 6 1"],
            "answer": "B",
            "solution": (
                "**Concept.** A sequence is a valid stack permutation iff it never contains a pattern "
                "… c … a … b … with a < b < c (i.e. after printing c, smaller values still in the stack must "
                "come out in decreasing order).\n\n"
                "- (A) push 1,2,3 pop 3, pop 2; push 4,5 pop 5; push 6 pop 6; pop 4, pop 1. **Possible.**\n"
                "- (B) push 1..4 pop 4; push 5 pop 5; pop 3; push 6 pop 6. Now the stack holds 1, 2 with 2 on "
                "top, so the next pop must be 2 — printing 1 is impossible. **Not possible** (pattern 4…1…2).\n"
                "- (C) pop 1, 2, 3 as they arrive; push 4,5,6 and pop 6, 5, 4. **Possible.**\n"
                "- (D) push 1..4 pop 4, pop 3; push 5 pop 5; pop 2; push 6 pop 6; pop 1. **Possible.**\n\n"
                "**Tip:** simulate greedily — push until the wanted value is on top; if it is buried below "
                "the top, the sequence is impossible."
            ),
            "solution_diagrams": [{"type": "stack", "values": [1, 2], "label": "after 4 5 3 6",
                                   "caption": "Option (B): 2 is on top, so 1 cannot be popped next"}],
            "verify": '''
def possible(seq):
    st, nxt = [], 1
    for x in seq:
        while (not st or st[-1] != x) and nxt <= 6:
            st.append(nxt); nxt += 1
        if st and st[-1] == x: st.pop()
        else: return False
    return True
opts = ["3 2 5 6 4 1", "4 5 3 6 1 2", "1 2 3 6 5 4", "4 3 5 2 6 1"]
bad = [L for L, o in zip("ABCD", opts) if not possible(list(map(int, o.split())))]
assert bad == [ANSWER]
''',
        },
        # ---------------------------------------------------------------- Q6
        {
            "type": "NAT", "marks": 1, "topic": "BFS — levels and non-tree edges",
            "text": ("BFS is run from vertex A on the undirected graph below, enqueuing undiscovered neighbours "
                     "in alphabetical order. The number of graph edges whose two endpoints lie at the **same** "
                     "BFS level is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
                          "edges": [["A", "B"], ["A", "C"], ["A", "D"], ["B", "C"], ["B", "E"],
                                    ["C", "F"], ["D", "F"], ["D", "G"], ["E", "F"], ["E", "H"],
                                    ["F", "H"], ["G", "H"], ["F", "G"]],
                          "pos": {"A": [0, 2], "B": [2, 4], "C": [2, 2], "D": [2, 0], "E": [4, 4],
                                  "F": [4, 2], "G": [4, 0], "H": [6, 2]}}],
            "answer": "3",
            "solution": (
                "**Concept.** In an undirected BFS every edge joins vertices whose levels differ by 0 or 1. "
                "Tree edges and some non-tree edges go between consecutive levels; the remaining non-tree "
                "edges join two vertices of the same level (they close odd cycles).\n\n"
                "**Levels.**\n"
                "- Level 0: A.\n"
                "- Level 1: B, C, D (neighbours of A).\n"
                "- Level 2: E (from B), F (from C), G (from D).\n"
                "- Level 3: H (from E).\n\n"
                "**Classifying the 13 edges.**\n"
                "- Tree edges (7): AB, AC, AD, BE, CF, DG, EH.\n"
                "- Between consecutive levels, non-tree: DF, FH, GH (3).\n"
                "- Same level: **BC** (level 1), **EF** and **FG** (level 2) → **3**.\n\n"
                "Check: 7 + 3 + 3 = 13 edges.\n\n"
                "**Tip:** a graph is bipartite iff no BFS produces a same-level edge, so this count being "
                "non-zero proves the graph has an odd cycle (e.g. A–B–C)."
            ),
            "verify": '''
from collections import deque
E = ["AB", "AC", "AD", "BC", "BE", "CF", "DF", "DG", "EF", "EH", "FH", "GH", "FG"]
G = {}
for a, b in E:
    G.setdefault(a, set()).add(b); G.setdefault(b, set()).add(a)
lv, q = {'A': 0}, deque('A')
while q:
    u = q.popleft()
    for v in sorted(G[u]):
        if v not in lv: lv[v] = lv[u] + 1; q.append(v)
assert sum(lv[a] == lv[b] for a, b in E) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q7
        {
            "type": "NAT", "marks": 1, "topic": "Python — sort keys with negative modulo",
            "text": "What value is printed by the following Python program?",
            "code": '''L = [7, -4, 12, -9, 5, 3, -1, 10]
r = sorted(L, key=lambda x: (x % 3, -x))
print(sum(r[:4]))''',
            "answer": "16",
            "solution": (
                "**Concept.** In Python, `x % m` with m > 0 is always in [0, m − 1] (the result takes the sign "
                "of the divisor): −4 % 3 = 2, −1 % 3 = 2, −9 % 3 = 0. Tuples compare lexicographically, so "
                "the key sorts by remainder first, then by value descending.\n\n"
                "**Remainders.** 7→1, −4→2, 12→0, −9→0, 5→2, 3→0, −1→2, 10→1.\n\n"
                "**Groups (each ordered by −x, i.e. larger first).**\n"
                "- remainder 0: 12, 3, −9\n- remainder 1: 10, 7\n- remainder 2: 5, −1, −4\n\n"
                "r = [12, 3, −9, 10, 7, 5, −1, −4]; first four sum to 12 + 3 − 9 + 10 = **16**.\n\n"
                "**Trap:** using C/Java semantics (−4 % 3 = −1, −1 % 3 = −1) puts −1 and −4 in a "
                "'remainder −1' group at the very front and changes the answer completely."
            ),
            "verify": '''
r2 = sorted(L, key=lambda x: (((x % 3) + 3) % 3, -x))
assert sum(r2[:4]) == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        # ---------------------------------------------------------------- Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Sorting — auxiliary space",
            "text": "Which of the following statements about the extra space used by sorting algorithms is/are TRUE?",
            "options": [
                "Top-down merge sort on an array of n elements, with the usual merge, uses Θ(n) auxiliary space",
                "Heapsort sorts an array using O(1) auxiliary space",
                "Quicksort that recurses on the smaller part and loops on the larger part needs only "
                "O(log n) stack depth, even in the worst case",
                "Merging two sorted singly linked lists of total length n by relinking nodes requires Θ(n) "
                "auxiliary space",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "- (A) **True.** The array merge copies the two runs into a buffer (or writes into one); the "
                "top-level merge alone needs n/2 to n extra cells.\n"
                "- (B) **True.** Build-heap and the repeated swap-root-with-last + sift-down work entirely "
                "inside the array; only a few index variables are needed.\n"
                "- (C) **True.** Each recursive call is on a part of size ≤ half of the current range, so the "
                "depth is ≤ log₂ n. The larger part is handled by the loop (tail-call elimination). The "
                "*time* can still be Θ(n²) — only the stack is bounded.\n"
                "- (D) **False.** Linked-list merge only changes `next` pointers using a constant number of "
                "extra pointer variables: O(1) space. This is why merge sort is preferred for linked lists.\n\n"
                "**Trap:** confusing worst-case *time* of quicksort (Θ(n²)) with its worst-case *space*; with "
                "the smaller-side-first trick they are independent."
            ),
            "verify": '''
import math
def depth_qs(A):
    best = [0]
    def rec(lo, hi, d):
        while lo < hi:
            best[0] = max(best[0], d)
            p, i = A[hi], lo - 1
            for j in range(lo, hi):
                if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
            A[i + 1], A[hi] = A[hi], A[i + 1]; q = i + 1
            if q - lo < hi - q: rec(lo, q - 1, d + 1); lo = q + 1
            else: rec(q + 1, hi, d + 1); hi = q - 1
    rec(0, len(A) - 1, 1)
    return best[0]
n = 512
assert depth_qs(list(range(n))) <= math.log2(n) + 1
assert sorted(ANSWER) == ['A', 'B', 'C']
''',
        },
        # ---------------------------------------------------------------- Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — linear probing, unsuccessful search",
            "text": ("A hash table of size 11 uses h(k) = k mod 11 and linear probing. After inserting "
                     "22, 33, 14, 25, 47, 30, 41 (in that order) it looks as shown. Assuming the home slot of a "
                     "key that is **not** in the table is equally likely to be any of the 11 slots, the expected "
                     "number of slots probed by an unsuccessful search (counting the final empty slot) is"),
            "diagrams": [{"type": "hashtable", "size": 11,
                          "slots": {0: 22, 1: 33, 3: 14, 4: 25, 5: 47, 8: 30, 9: 41}}],
            "options": ["23/11", "12/11", "18/11", "28/11"],
            "answer": "A",
            "solution": (
                "**Concept.** An unsuccessful search starting at slot i probes every occupied slot of the run "
                "(cluster) starting at i, then the first empty slot. So cost(i) = 1 + (number of consecutive "
                "occupied slots from i).\n\n"
                "Occupied: 0, 1 | 3, 4, 5 | 8, 9. Empty: 2, 6, 7, 10.\n\n"
                "- i = 0: 0, 1, 2 → 3\n- i = 1: 1, 2 → 2\n- i = 2: 1\n"
                "- i = 3: 3, 4, 5, 6 → 4\n- i = 4: 3\n- i = 5: 2\n- i = 6: 1\n- i = 7: 1\n"
                "- i = 8: 8, 9, 10 → 3\n- i = 9: 2\n- i = 10: 1\n\n"
                "Sum = 3 + 2 + 1 + 4 + 3 + 2 + 1 + 1 + 3 + 2 + 1 = 23 → expected **23/11 ≈ 2.09**.\n\n"
                "**Options.** (B) 12/11 forgets to count the final empty slot (23 − 11 = 12); (C) 18/11 = 1 + 7/11 "
                "counts each occupied slot once, ignoring clustering; (D) 28/11 charges every slot of a cluster "
                "the *whole* cluster length instead of the part from the home slot onwards.\n\n"
                "**Insight:** a cluster of length L contributes L(L + 1)/2 extra probes — long clusters are "
                "quadratically costly, which is the essence of *primary clustering*."
            ),
            "verify": '''
from fractions import Fraction
T = [None] * 11
for k in [22, 33, 14, 25, 47, 30, 41]:
    i = k % 11
    while T[i] is not None: i = (i + 1) % 11
    T[i] = k
tot = 0
for s in range(11):
    i, c = s, 1
    while T[i] is not None: i = (i + 1) % 11; c += 1
    tot += c
opts = ["23/11", "12/11", "18/11", "28/11"]
assert Fraction(opts["ABCD".index(ANSWER)]) == Fraction(tot, 11)
''',
        },
        # ---------------------------------------------------------------- Q10
        {
            "type": "MCQ", "marks": 1, "topic": "BST counting",
            "text": ("How many structurally distinct binary search trees can be formed with the keys "
                     "1, 2, 3, 4, 5, 6 such that the root holds the key **3**?"),
            "options": ["10", "14", "5", "20"],
            "answer": "A",
            "solution": (
                "**Concept.** With root r, the left subtree is a BST on the r − 1 smaller keys and the right "
                "subtree a BST on the n − r larger keys, chosen independently. The number of BSTs on k keys is "
                "the Catalan number C_{k} (1, 1, 2, 5, 14, 42, …).\n\n"
                "- Left subtree: keys {1, 2} → C_{2} = 2 shapes.\n"
                "- Right subtree: keys {4, 5, 6} → C_{3} = 5 shapes.\n"
                "- Total = 2 × 5 = **10**.\n\n"
                "**Options.** (B) 14 = C_{4} is the count for 4 keys, (C) 5 forgets the left subtree's two "
                "shapes, (D) 20 wrongly doubles the count, as if mirror images were extra trees.\n\n"
                "**Check:** summing over all roots gives C_{0}C_{5} + C_{1}C_{4} + C_{2}C_{3} + C_{3}C_{2} + "
                "C_{4}C_{1} + C_{5}C_{0} = 42 + 14 + 10 + 10 + 14 + 42 = 132 = C_{6}."
            ),
            "solution_diagrams": [{"type": "bintree", "tree": [3, [1, None, [2]], [5, [4], [6]]],
                                   "caption": "One of the 10 trees"}],
            "verify": '''
from functools import lru_cache
@lru_cache(None)
def cnt(lo, hi):
    if lo > hi: return 1
    return sum(cnt(lo, r - 1) * cnt(r + 1, hi) for r in range(lo, hi + 1))
assert ["10", "14", "5", "20"]["ABCD".index(ANSWER)] == str(cnt(1, 2) * cnt(4, 6))
''',
        },
        # ---------------------------------------------------------------- Q11
        {
            "type": "MSQ", "marks": 2, "topic": "Inversions — insertion sort, bubble sort, reversal",
            "text": ("Let A = [4, 9, 2, 7, 5, 1, 8, 3]. An inversion is a pair of indices i < j with A[i] > A[j]. "
                     "Which of the following statements is/are TRUE?"),
            "options": [
                "A has exactly 16 inversions",
                "Insertion sort (shift while A[j] > key) performs exactly 16 element shifts on A",
                "Bubble sort with early termination (stop after a pass with no swap) executes all n − 1 = 7 passes on A",
                "The reverse of A, [3, 8, 1, 5, 7, 2, 9, 4], has exactly 12 inversions",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Counting inversions** (for each element, how many later elements are smaller):\n"
                "- 4: {2, 1, 3} → 3\n- 9: {2, 7, 5, 1, 8, 3} → 6\n- 2: {1} → 1\n- 7: {5, 1, 3} → 3\n"
                "- 5: {1, 3} → 2\n- 1: 0\n- 8: {3} → 1\n- 3: 0\n"
                "Total = 3 + 6 + 1 + 3 + 2 + 0 + 1 + 0 = **16**. (A) **True.**\n\n"
                "- (B) **True.** Every shift in insertion sort swaps one adjacent inverted pair, removing "
                "exactly one inversion, and the sort ends with 0 inversions → shifts = inversions = 16. "
                "(Bubble sort likewise performs exactly 16 swaps.)\n"
                "- (C) **False.** Each pass moves an element at most one place to the left. The element that "
                "must travel farthest left is 1 (index 5 → 0, five places) — 3 travels from index 7 to 2, also "
                "five. So 5 passes sort the array and the 6th pass makes no swap and stops: 6 passes, not 7.\n"
                "- (D) **True.** Reversing turns every inverted pair into a non-inverted one and vice versa; "
                "there are C(8, 2) = 28 pairs, so the reverse has 28 − 16 = 12 inversions.\n\n"
                "**Trap:** the number of *passes* of bubble sort depends on the maximum leftward displacement, "
                "not on the number of inversions."
            ),
            "verify": '''
A = [4, 9, 2, 7, 5, 1, 8, 3]
inv = lambda X: sum(X[i] > X[j] for i in range(len(X)) for j in range(i + 1, len(X)))
B, sh = A[:], 0
for i in range(1, len(B)):
    x, j = B[i], i - 1
    while j >= 0 and B[j] > x: B[j + 1] = B[j]; j -= 1; sh += 1
    B[j + 1] = x
C, p = A[:], 0
for i in range(7):
    p += 1; sw = False
    for j in range(7 - i):
        if C[j] > C[j + 1]: C[j], C[j + 1] = C[j + 1], C[j]; sw = True
    if not sw: break
r = {'A': inv(A) == 16, 'B': sh == 16, 'C': p == 7, 'D': inv(A[::-1]) == 12}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q12
        {
            "type": "NAT", "marks": 2, "topic": "Insertion sort — exact comparison count",
            "text": ("Insertion sort is applied to A = [13, 6, 21, 2, 17, 9, 25, 4, 11]:\n\n"
                     "`for i in 1..n−1: x = A[i]; j = i − 1; while j ≥ 0 and A[j] > x: A[j+1] = A[j]; j −= 1; "
                     "A[j+1] = x`\n\n"
                     "Count one key comparison each time `A[j] > x` is evaluated (it is not evaluated when "
                     "j < 0). The total number of key comparisons is ______."),
            "answer": "24",
            "solution": (
                "**Concept.** When inserting x, every shifted element costs one comparison that succeeds; then "
                "there is one more *failing* comparison — unless x travels all the way to index 0 (then the loop "
                "stops on j < 0 and no failing comparison is made). Hence\n\n"
                "comparisons = (inversions) + (n − 1) − (number of elements that are inserted at index 0).\n\n"
                "**Per insertion** (shifts + failing comparison):\n"
                "- 6: shifts 13, reaches index 0 → 1 + 0 = 1\n"
                "- 21: 0 shifts + 1 = 1\n"
                "- 2: shifts 21, 13, 6, reaches index 0 → 3 + 0 = 3\n"
                "- 17: shifts 21 → 1 + 1 = 2\n"
                "- 9: shifts 21, 17, 13 → 3 + 1 = 4\n"
                "- 25: 0 + 1 = 1\n"
                "- 4: shifts 25, 21, 17, 13, 9, 6 → 6 + 1 = 7\n"
                "- 11: shifts 25, 21, 17, 13 → 4 + 1 = 5\n\n"
                "Total = 1 + 1 + 3 + 2 + 4 + 1 + 7 + 5 = **24**.\n\n"
                "Formula check: inversions = 18, n − 1 = 8, elements reaching index 0: 6 and 2 → "
                "18 + 8 − 2 = 24. ✓\n\n"
                "**Trap:** answering 'inversions + n − 1' = 26, forgetting that new minima stop on the "
                "boundary check j ≥ 0 rather than on a key comparison."
            ),
            "verify": '''
A = [13, 6, 21, 2, 17, 9, 25, 4, 11]; c = 0
for i in range(1, len(A)):
    x, j = A[i], i - 1
    while j >= 0:
        c += 1
        if A[j] > x: A[j + 1] = A[j]; j -= 1
        else: break
    A[j + 1] = x
assert A == sorted(A) and c == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q13
        {
            "type": "MCQ", "marks": 2, "topic": "Selection sort — instability",
            "text": ("Records (key, tag) = [(2, a), (3, b), (2, c), (1, d), (3, e)] are sorted by key with "
                     "selection sort: in pass i (i = 0, 1, 2, 3) the record with the smallest key in positions "
                     "i..4 (the **leftmost** one in case of ties) is swapped with the record at position i. "
                     "The final order of the tags is"),
            "options": ["d, a, c, b, e", "d, c, a, b, e", "d, c, a, e, b", "d, a, c, e, b"],
            "answer": "B",
            "solution": (
                "**Concept.** Selection sort's long-distance swap can carry a record past another record with "
                "the same key, so the algorithm is not stable — even with the leftmost-minimum rule.\n\n"
                "**Trace.**\n"
                "- i = 0: minimum key 1 at position 3 → swap positions 0, 3: [1d, 3b, 2c, 2a, 3e]. "
                "(2a has jumped behind 2c!)\n"
                "- i = 1: minimum of positions 1..4 is key 2, leftmost at position 2 (2c) → swap 1, 2: "
                "[1d, 2c, 3b, 2a, 3e].\n"
                "- i = 2: minimum of positions 2..4 is 2a at position 3 → swap 2, 3: [1d, 2c, 2a, 3b, 3e].\n"
                "- i = 3: 3b vs 3e — no strictly smaller key, no change.\n\n"
                "Final tags: **d, c, a, b, e**.\n\n"
                "**Options.**\n"
                "- (A) is the stable order (what insertion sort or merge sort would give).\n"
                "- (C) also reverses b and e, but they never get swapped past each other.\n"
                "- (D) is wrong for both tie groups.\n\n"
                "**Trap:** assuming 'leftmost minimum' makes selection sort stable. It only controls which "
                "record is *chosen*; the *displaced* record A[i] can still jump over its equals."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Records after each pass",
                                   "row_labels": ["start", "i=0", "i=1", "i=2", "i=3"],
                                   "rows": [["2a", "3b", "2c", "1d", "3e"], ["1d", "3b", "2c", "2a", "3e"],
                                            ["1d", "2c", "3b", "2a", "3e"], ["1d", "2c", "2a", "3b", "3e"],
                                            ["1d", "2c", "2a", "3b", "3e"]],
                                   "highlight": [[1, 3], [4, 1], [4, 2]]}],
            "verify": '''
R = [(2, 'a'), (3, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
for i in range(len(R) - 1):
    m = i
    for j in range(i + 1, len(R)):
        if R[j][0] < R[m][0]: m = j
    R[i], R[m] = R[m], R[i]
opts = ["d, a, c, b, e", "d, c, a, b, e", "d, c, a, e, b", "d, a, c, e, b"]
assert opts["ABCD".index(ANSWER)] == ", ".join(t for _, t in R)
''',
        },
        # ---------------------------------------------------------------- Q14
        {
            "type": "NAT", "marks": 2, "topic": "Divide and conquer — counting split inversions",
            "text": ("Inversions in A = [10, 3, 15, 8, 1, 12, 6, 14] are counted with the merge-sort method: "
                     "each half is recursively sorted (counting its own inversions), and during the final merge "
                     "of the two sorted halves, whenever an element is taken from the **right** half, the number "
                     "of elements still remaining in the left half is added to the count. The amount added "
                     "during the **final (top-level) merge only** is ______."),
            "diagrams": [{"type": "array", "values": [10, 3, 15, 8, 1, 12, 6, 14], "label": "A",
                          "caption": "Left half = indices 0–3, right half = indices 4–7"}],
            "answer": "9",
            "solution": (
                "**Concept.** Every inversion is either inside the left half, inside the right half, or a "
                "*split* inversion (i in left, j in right, A[i] > A[j]). When a right-half element y is output "
                "during the merge, all elements still waiting in the left half are larger than y — each forms a "
                "split inversion with y.\n\n"
                "**Sorted halves:** L = [3, 8, 10, 15], R = [1, 6, 12, 14].\n\n"
                "**Merge trace** (elements left in L when a right element is taken):\n"
                "- take 1 (R): L has 3, 8, 10, 15 waiting → +4\n"
                "- take 3 (L)\n- take 6 (R): 8, 10, 15 waiting → +3\n"
                "- take 8, 10 (L)\n- take 12 (R): 15 waiting → +1\n"
                "- take 14 (R): 15 waiting → +1\n- take 15 (L)\n\n"
                "Split inversions = 4 + 3 + 1 + 1 = **9**.\n\n"
                "**Cross-check:** total inversions of A = 13; left-half inversions (10,3), (10,8), (15,8) = 3; "
                "right-half inversions (12,6) = 1; 13 − 3 − 1 = 9. ✓\n\n"
                "**Trap:** counting 'remaining in right' when a left element is taken counts the wrong "
                "direction, and counting during *all* merges gives the total (13), not the top-level share."
            ),
            "verify": '''
A = [10, 3, 15, 8, 1, 12, 6, 14]
L, R = sorted(A[:4]), sorted(A[4:])
i = j = add = 0
while i < 4 and j < 4:
    if L[i] <= R[j]: i += 1
    else: add += 4 - i; j += 1
brute = sum(a > b for a in A[:4] for b in A[4:])
assert add == brute == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Comparison lower bounds — merging",
            "text": ("Two sorted lists, each containing 3 elements, are to be merged into one sorted list; all 6 "
                     "elements are distinct. What is the smallest number k such that some comparison-based "
                     "algorithm always merges them using at most k comparisons?"),
            "options": ["4", "5", "6", "10"],
            "answer": "B",
            "solution": (
                "**Concept (decision-tree lower bound).** A comparison-based algorithm is a binary decision "
                "tree; it must have a distinct leaf for every possible outcome. Its worst-case number of "
                "comparisons is the tree height h, and 2^{h} ≥ #outcomes.\n\n"
                "**Outcomes.** The merged order is determined by choosing which 3 of the 6 output positions "
                "belong to the first list: C(6, 3) = 20 possibilities. So h ≥ ⌈log₂ 20⌉ = **5**.\n\n"
                "**Upper bound.** The standard merge uses at most m + n − 1 = 5 comparisons. Hence k = 5 "
                "exactly — the lower bound is tight here.\n\n"
                "**Options.**\n"
                "- (A) 4 is impossible: 2⁴ = 16 < 20 leaves.\n"
                "- (C) 6 is the total number of elements, not a comparison bound.\n"
                "- (D) 10 = ⌈log₂ 6!⌉ is the lower bound for **sorting** 6 arbitrary elements; merging gets "
                "free information from the two lists already being sorted.\n\n"
                "**Tip:** the same argument gives Ω(n log n) for sorting (log₂ n! leaves) and Ω(log n) for "
                "searching a sorted array (n + 1 outcomes)."
            ),
            "verify": '''
import math, itertools
lb = math.ceil(math.log2(math.comb(6, 3)))
worst = 0
for pos in itertools.combinations(range(6), 3):
    a = list(pos); b = [x for x in range(6) if x not in pos]
    i = j = c = 0
    while i < 3 and j < 3:
        c += 1
        if a[i] < b[j]: i += 1
        else: j += 1
    worst = max(worst, c)
assert lb == worst == int(["4", "5", "6", "10"]["ABCD".index(ANSWER)])
''',
        },
        # ---------------------------------------------------------------- Q16
        {
            "type": "MSQ", "marks": 2, "topic": "Python — sorted(), reverse and stability",
            "text": ("Consider the following Python program (it prints nothing). Which of the following "
                     "statements is/are TRUE after it runs?"),
            "code": '''data = [("p", 2), ("q", 1), ("r", 2), ("s", 1)]
a = sorted(data, key=lambda t: t[1], reverse=True)
b = sorted(data, key=lambda t: t[1])[::-1]
c = sorted(data, key=lambda t: -t[1])
d = data.sort(key=lambda t: t[1])''',
            "options": [
                "`a == c` evaluates to True",
                "`a == b` evaluates to True",
                "The names in `b`, in order, are r, p, s, q",
                "`d` is None and `data` is now [('q', 1), ('s', 1), ('p', 2), ('r', 2)]",
            ],
            "answer": ["A", "C", "D"],
            "solution": (
                "**Concept.** `sorted(..., reverse=True)` is still **stable**: it sorts as if each comparison "
                "were reversed, so records with equal keys keep their *original* order. Reversing an "
                "ascending result with `[::-1]` instead reverses the order of equal keys too. "
                "`list.sort()` sorts in place and returns None.\n\n"
                "**Values.**\n"
                "- a: key 2 first, ties in input order → p, r, q, s.\n"
                "- b: ascending is q, s, p, r; reversed → r, p, s, q.\n"
                "- c: key −2 < −1, ties in input order → p, r, q, s.\n"
                "- d: None; `data` becomes q, s, p, r (stable ascending).\n\n"
                "**Statements.**\n"
                "- (A) **True** — both are p, r, q, s.\n"
                "- (B) **False** — b has the ties reversed (r before p, s before q).\n"
                "- (C) **True.**\n"
                "- (D) **True** — note `a`, `b`, `c` were computed before the in-place sort, and `sorted` "
                "always returns a new list, so they are unaffected.\n\n"
                "**Trap:** believing `reverse=True` is the same as reversing the sorted list. It is the same "
                "only when all keys are distinct."
            ),
            "verify": '''
r = {'A': a == c, 'B': a == b, 'C': [x for x, _ in b] == list("rpsq"),
     'D': d is None and data == [('q', 1), ('s', 1), ('p', 2), ('r', 2)]}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q17
        {
            "type": "NAT", "marks": 2, "topic": "Shortest paths — tight edges",
            "text": ("For the weighted directed graph below, let d(v) be the shortest-path distance from S. "
                     "An edge (u, v) with weight w **lies on some shortest path from S** iff "
                     "d(u) + w = d(v). The number of edges of the graph that lie on some shortest path from "
                     "S is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E", "T"],
                          "edges": [["S", "A", 3], ["S", "B", 7], ["S", "C", 4], ["A", "B", 3],
                                    ["A", "D", 6], ["C", "B", 2], ["C", "E", 9], ["B", "D", 2],
                                    ["B", "E", 5], ["D", "E", 1], ["D", "T", 8], ["E", "T", 4]],
                          "pos": {"S": [0, 2], "A": [2, 4], "B": [3, 2], "C": [2, 0], "D": [5, 4],
                                  "E": [5, 0], "T": [7, 2]}}],
            "answer": "7",
            "solution": (
                "**Step 1 — distances (Dijkstra from S).**\n"
                "- Extract S (0): A = 3, B = 7, C = 4.\n"
                "- Extract A (3): B = min(7, 6) = 6, D = 9.\n"
                "- Extract C (4): B = min(6, 6) = 6 (tie), E = 13.\n"
                "- Extract B (6): D = min(9, 8) = 8, E = min(13, 11) = 11.\n"
                "- Extract D (8): E = min(11, 9) = 9, T = 16.\n"
                "- Extract E (9): T = min(16, 13) = 13.\n"
                "d: S 0, A 3, C 4, B 6, D 8, E 9, T 13.\n\n"
                "**Step 2 — test every edge for d(u) + w = d(v).**\n"
                "- S→A 0+3=3 ✓, S→B 0+7=7≠6 ✗, S→C 0+4=4 ✓\n"
                "- A→B 3+3=6 ✓, A→D 3+6=9≠8 ✗\n"
                "- C→B 4+2=6 ✓, C→E 4+9=13≠9 ✗\n"
                "- B→D 6+2=8 ✓, B→E 6+5=11≠9 ✗\n"
                "- D→E 8+1=9 ✓, D→T 8+8=16≠13 ✗\n"
                "- E→T 9+4=13 ✓\n\n"
                "Tight edges: SA, SC, AB, CB, BD, DE, ET → **7**.\n\n"
                "**Trap:** a shortest-path *tree* has only 6 edges (one parent per non-source vertex); B has "
                "two tight incoming edges (A→B and C→B), both of which lie on shortest paths — there are two "
                "shortest S–T paths: S→A→B→D→E→T and S→C→B→D→E→T, both of length 13."
            ),
            "verify": '''
W = [("S", "A", 3), ("S", "B", 7), ("S", "C", 4), ("A", "B", 3), ("A", "D", 6),
     ("C", "B", 2), ("C", "E", 9), ("B", "D", 2), ("B", "E", 5), ("D", "E", 1),
     ("D", "T", 8), ("E", "T", 4)]
V = {x for e in W for x in e[:2]}
d = {v: float('inf') for v in V}; d['S'] = 0
for _ in V:
    for a, b, w in W: d[b] = min(d[b], d[a] + w)
assert sum(d[a] + w == d[b] for a, b, w in W) == int(ANSWER) and d['T'] == 13
''',
        },
        # ---------------------------------------------------------------- Q18
        {
            "type": "MCQ", "marks": 2, "topic": "Linked lists — stable partition",
            "text": ("The function `part` rearranges a singly linked list around a value x. The list "
                     "7 → 3 → 9 → 3 → 5 → 1 → 8 is partitioned with x = 5. What is printed?"),
            "code": '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def part(head, x):
    lt = lt_t = Node(0)
    ge = ge_t = Node(0)
    while head:
        if head.val < x:
            lt_t.next = head
            lt_t = head
        else:
            ge_t.next = head
            ge_t = head
        head = head.next
    ge_t.next = None
    lt_t.next = ge.next
    return lt.next

head = None
for v in reversed([7, 3, 9, 3, 5, 1, 8]):
    head = Node(v, head)
p, out = part(head, 5), []
while p:
    out.append(p.val)
    p = p.next
print(out)''',
            "options": ["`[1, 3, 3, 5, 7, 8, 9]`", "`[3, 3, 1, 7, 9, 5, 8]`",
                        "`[1, 3, 3, 8, 5, 9, 7]`", "`[3, 3, 1, 5, 7, 8, 9]`"],
            "answer": "B",
            "solution": (
                "**Concept.** Two dummy-headed lists collect the nodes `< x` and `≥ x` by appending at their "
                "tails, so each sub-list keeps the original relative order — a **stable** partition (unlike "
                "Lomuto/Hoare array partitions). The lists are then concatenated.\n\n"
                "**Trace.**\n"
                "- 7 → ge; 3 → lt; 9 → ge; 3 → lt; 5 → ge (5 is not < 5); 1 → lt; 8 → ge.\n"
                "- lt list: 3 → 3 → 1;  ge list: 7 → 9 → 5 → 8.\n"
                "- `ge_t.next = None` terminates the ge list (node 8's old `next` was None anyway, but in "
                "general the last ≥-node may still point into the < list).\n"
                "- Concatenate: 3, 3, 1, 7, 9, 5, 8.\n\n"
                "**Options.**\n"
                "- (A) and (D) sort the values; partitioning does not sort either part.\n"
                "- (C) is what you get if nodes were inserted at the *head* of each part (reversing them).\n\n"
                "**Trap:** omitting `ge_t.next = None` can create a cycle when the last node of the original "
                "list belongs to the `<` part — the traversal would then never end."
            ),
            "diagrams": [{"type": "linkedlist", "values": [7, 3, 9, 3, 5, 1, 8], "head": "head",
                          "caption": "Input list"}],
            "solution_diagrams": [{"type": "linkedlist", "values": [3, 3, 1, 7, 9, 5, 8], "head": "result",
                                   "caption": "After part(head, 5)"}],
            "verify": '''
L = [7, 3, 9, 3, 5, 1, 8]
exp = [v for v in L if v < 5] + [v for v in L if v >= 5]
assert OUTPUT.strip() == str(exp) and ANSWER == 'B'
''',
        },
        # ---------------------------------------------------------------- Q19
        {
            "type": "MSQ", "marks": 2, "topic": "Topological sorting — DFS and Kahn's algorithm",
            "text": ("Consider the DAG below. Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                          "edges": [["A", "C"], ["A", "D"], ["B", "D"], ["B", "E"], ["C", "F"],
                                    ["D", "F"], ["D", "G"], ["E", "G"]],
                          "pos": {"A": [0, 3], "B": [0, 0], "C": [2, 4], "D": [2, 1.5], "E": [2, -1],
                                  "F": [4, 3], "G": [4, 0]}}],
            "options": [
                "DFS with the outer loop over vertices in alphabetical order and out-neighbours explored "
                "alphabetically, outputting vertices in reverse order of finishing, gives B, E, A, D, G, C, F",
                "C, A, B, D, E, F, G is a valid topological order",
                "Kahn's algorithm that always removes the alphabetically smallest current source outputs "
                "A, B, C, D, E, F, G",
                "D precedes E in every topological order",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**(A) DFS trace.** Start A: A → C → F (F finishes 1st), C finishes; A → D → F seen, D → G "
                "(G finishes), D finishes; A finishes. Start B: B → D seen, B → E → G seen, E finishes, "
                "B finishes.\n"
                "Finish order: F, C, G, D, A, E, B. Reverse: **B, E, A, D, G, C, F** → **True.**\n\n"
                "**(B)** Edge A → C requires A before C. **False.**\n\n"
                "**(C) Kahn trace** (current sources, choose smallest):\n"
                "- {A, B} → A; now C is a source (D still waits for B).\n"
                "- {B, C} → B; D and E become sources.\n"
                "- {C, D, E} → C; F waits for D.\n"
                "- {D, E} → D; F becomes a source, G waits for E.\n"
                "- {E, F} → E; G becomes a source.\n"
                "- {F, G} → F, then G.\n"
                "Output **A, B, C, D, E, F, G** → **True.**\n\n"
                "**(D)** There is no path between D and E, so they can appear in either order; e.g. the DFS "
                "order in (A) has E before D. **False.**\n\n"
                "**Trap:** the DFS order and the Kahn order are both valid but generally different — a DAG "
                "usually has many topological orders (this one has 42)."
            ),
            "verify": '''
D = {'A': 'CD', 'B': 'DE', 'C': 'F', 'D': 'FG', 'E': 'G', 'F': '', 'G': ''}
seen, fin = set(), []
def vis(u):
    seen.add(u)
    for v in D[u]:
        if v not in seen: vis(v)
    fin.append(u)
for s in sorted(D):
    if s not in seen: vis(s)
indeg = {v: 0 for v in D}
for u in D:
    for v in D[u]: indeg[v] += 1
out, avail = [], sorted(v for v in D if indeg[v] == 0)
while avail:
    u = avail.pop(0); out.append(u)
    for v in D[u]:
        indeg[v] -= 1
        if indeg[v] == 0: avail.append(v)
    avail.sort()
def valid(o):
    pos = {v: i for i, v in enumerate(o)}
    return all(pos[u] < pos[v] for u in D for v in D[u])
r = {'A': fin[::-1] == list("BEADGCF"), 'B': valid("CABDEFG"),
     'C': out == list("ABCDEFG"), 'D': fin[::-1].index('D') < fin[::-1].index('E')}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q20
        {
            "type": "MCQ", "marks": 2, "topic": "Heapsort — intermediate array state",
            "text": ("Heapsort (ascending) is applied to A = [5, 12, 9, 2, 18, 7]: first a max-heap is built "
                     "bottom-up (sift-down at i = 2, 1, 0), then repeatedly the root is swapped with the last "
                     "element of the heap, the heap size is decreased by one, and the new root is sifted down. "
                     "What is the array after the build-heap phase **and** the first **two** root extractions?"),
            "diagrams": [{"type": "heap", "values": [5, 12, 9, 2, 18, 7],
                          "caption": "Initial array as a complete binary tree"}],
            "options": ["[9, 5, 7, 2, 12, 18]", "[12, 7, 9, 2, 5, 18]",
                        "[9, 7, 5, 2, 12, 18]", "[7, 9, 5, 2, 12, 18]"],
            "answer": "C",
            "solution": (
                "**Build-heap.**\n"
                "- i = 2 (9): child 7 smaller → no change.\n"
                "- i = 1 (12): children 2, 18 → swap with 18 → [5, 18, 9, 2, 12, 7].\n"
                "- i = 0 (5): children 18, 9 → swap with 18 → [18, 5, 9, 2, 12, 7]; then at index 1, children "
                "2, 12 → swap with 12 → [18, 12, 9, 2, 5, 7].\n\n"
                "**Extraction 1.** Swap A[0] ↔ A[5]: [7, 12, 9, 2, 5, | 18]. Sift 7 in heap of size 5: "
                "children 12, 9 → swap with 12 → [12, 7, 9, 2, 5, | 18]; index 1 children 2, 5 < 7 → stop.\n\n"
                "**Extraction 2.** Swap A[0] ↔ A[4]: [5, 7, 9, 2, | 12, 18]. Sift 5 in heap of size 4: "
                "children 7, 9 → swap with 9 → [9, 7, 5, 2, | 12, 18]; index 2 has no children inside the "
                "heap → stop.\n\n"
                "Result: **[9, 7, 5, 2, 12, 18]**.\n\n"
                "**Options.**\n"
                "- (A) is a valid max-heap on the same keys, but not the one sift-down produces: 5 must move "
                "into 9's old slot (index 2), while 7 stays at index 1.\n"
                "- (B) is the state after only one extraction.\n"
                "- (D) omits the sift-down entirely.\n\n"
                "**Note:** heapsort is in-place but not stable, and its sorted suffix grows from the right."
            ),
            "solution_diagrams": [{"type": "array", "values": [9, 7, 5, 2, 12, 18], "highlight": [4, 5],
                                   "caption": "Heap part A[0..3] | sorted suffix A[4..5]"}],
            "verify": '''
H = [5, 12, 9, 2, 18, 7]; n = len(H)
def sift(i, m):
    while True:
        l, r, b = 2 * i + 1, 2 * i + 2, i
        if l < m and H[l] > H[b]: b = l
        if r < m and H[r] > H[b]: b = r
        if b == i: return
        H[i], H[b] = H[b], H[i]; i = b
for i in range(n // 2 - 1, -1, -1): sift(i, n)
for k in range(2):
    e = n - 1 - k; H[0], H[e] = H[e], H[0]; sift(0, e)
opts = ["[9, 5, 7, 2, 12, 18]", "[12, 7, 9, 2, 5, 18]",
        "[9, 7, 5, 2, 12, 18]", "[7, 9, 5, 2, 12, 18]"]
assert opts["ABCD".index(ANSWER)] == str(H)
''',
        },
    ],
}
