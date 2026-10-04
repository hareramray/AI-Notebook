# Set 40 — Full-Syllabus Mock, Paper 10

SET = {
    "number": 40,
    "title": "Full-Syllabus Mock — Paper 10",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — floor division, modulo and rounding",
            "text": "What does the following Python statement print?",
            "code": '''print(-17 // 5, -17 % 5, 17 // -5, round(-2.5), int(-2.5))''',
            "options": ["`-3 -2 -3 -3 -2`", "`-4 3 -4 -2 -2`", "`-4 3 -3 -2 -3`", "`-4 -2 -4 -3 -2`"],
            "answer": "B",
            "solution": (
                "**Concept.** Python’s `//` floors toward −∞ and `%` takes the sign of the divisor, so that "
                "`a == (a // b) * b + a % b` always holds. `round` uses banker’s rounding (ties to even); "
                "`int` truncates toward 0.\n\n"
                "- `-17 // 5` = ⌊−3.4⌋ = **−4**.\n"
                "- `-17 % 5` = −17 − (−4)(5) = **3**.\n"
                "- `17 // -5` = ⌊−3.4⌋ = **−4**.\n"
                "- `round(-2.5)`: tie between −2 and −3 → the even one, **−2**.\n"
                "- `int(-2.5)` truncates → **−2**.\n\n"
                "Output `-4 3 -4 -2 -2` → (B).\n\n"
                "**Options.** (A) is C/Java behaviour (truncating division, remainder with the sign of the "
                "dividend) plus round-half-away-from-zero. (C) truncates only the third division and floors "
                "`int`. (D) mixes a C-style remainder with half-away rounding.\n\n"
                "**Trap:** `round(2.5)` is 2 and `round(3.5)` is 4 in Python 3."
            ),
            "verify": "assert OUTPUT.strip() == '-4 3 -4 -2 -2' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — nested list comprehensions",
            "text": "What is printed by the following program?",
            "code": '''m = [[i * j for j in range(i)] for i in range(5)]
print(sum(map(sum, m)))''',
            "answer": "35",
            "solution": (
                "**Concept.** The outer comprehension creates one row per i; the inner one ranges over "
                "j = 0 … i − 1, so row i is a triangle-shaped list.\n\n"
                "- i = 0: [] → 0\n"
                "- i = 1: [0] → 0\n"
                "- i = 2: [0, 2] → 2\n"
                "- i = 3: [0, 3, 6] → 9\n"
                "- i = 4: [0, 4, 8, 12] → 24\n\n"
                "`map(sum, m)` gives the row sums 0, 0, 2, 9, 24, whose total is **35**.\n\n"
                "Closed form: row i sums to i·(0 + 1 + … + (i−1)) = i²(i−1)/2, giving 0, 0, 2, 9, 24.\n\n"
                "**Trap:** reading `range(i)` as `range(5)` (a full 5×5 multiplication table, total 100), or "
                "as 1..i inclusive (total 65)."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER == '35'",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks and queues — simulation",
            "text": "Consider the following Python program. What is printed?",
            "code": '''from collections import deque
s, q = [], deque()
for x in range(1, 9):
    s.append(x)
    if x % 3 == 0:
        q.append(s.pop()); q.append(s.pop())
    if x % 4 == 0:
        s.append(q.popleft())
print(list(q), s)''',
            "options": ["`[5, 6] [1, 4, 3, 7, 8, 2]`", "`[6, 5] [1, 4, 3, 7, 8, 2]`",
                        "`[6, 5] [1, 4, 2, 7, 8, 3]`", "`[2, 6, 5] [1, 4, 3, 7, 8]`"],
            "answer": "B",
            "solution": (
                "**Concept.** `s` is a LIFO stack (append/pop at the right) and `q` a FIFO queue "
                "(append right, popleft).\n\n"
                "- x = 1, 2, 3: s = [1, 2, 3]; at 3, pop 3 then 2 into q → q = [3, 2], s = [1].\n"
                "- x = 4: s = [1, 4]; 4 % 4 == 0 → move q’s front (3) to s → s = [1, 4, 3], q = [2].\n"
                "- x = 5: s = [1, 4, 3, 5].\n"
                "- x = 6: s = […, 5, 6]; pop 6 then 5 into q → q = [2, 6, 5], s = [1, 4, 3].\n"
                "- x = 7, 8: s = [1, 4, 3, 7, 8]; at 8 move q’s front (2) → s = [1, 4, 3, 7, 8, 2], "
                "q = [6, 5].\n\n"
                "Output `[6, 5] [1, 4, 3, 7, 8, 2]` → (B).\n\n"
                "**Options.** (A) reverses the order of the two pops. (C) dequeues from the wrong end at x = 4. "
                "(D) forgets the second transfer at x = 8.\n\n"
                "**Trap:** two consecutive pops from a stack deliver the elements in reverse order of pushing."
            ),
            "verify": "assert OUTPUT.strip() == '[6, 5] [1, 4, 3, 7, 8, 2]' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Doubly linked lists — deleting a node",
            "text": ("In a doubly linked list each node has fields `prev` and `next`. Let p point to a node that "
                     "is neither the first nor the last node. Which of the following code fragments correctly "
                     "unlink p from the list (so that a forward and a backward traversal both skip p)?"),
            "diagrams": [{"type": "linkedlist", "values": ["…", "x", "p", "y", "…"], "doubly": True,
                          "caption": "p is an interior node with neighbours x and y"}],
            "options": [
                "`p.prev.next = p.next; p.next.prev = p.prev`",
                "`p.next.prev = p.prev; p.prev.next = p.next`",
                "`p.prev.next = p.next; p.prev.next.prev = p.prev`",
                "`p.prev = p.next; p.next.prev = p.prev`",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Concept.** Unlinking p needs two updates: x.next = y and y.prev = x, where x = p.prev and "
                "y = p.next. Order does not matter as long as each right-hand side still refers to the "
                "intended node at the time it is evaluated.\n\n"
                "- (A) x.next = y; y.prev = x. **Correct.**\n"
                "- (B) The same two assignments in the other order; p’s own fields are untouched, so both "
                "still refer to x and y. **Correct.**\n"
                "- (C) After the first statement, `p.prev.next` *is* y, so `p.prev.next.prev = p.prev` sets "
                "y.prev = x. **Correct** (just an indirect way to reach y).\n"
                "- (D) The first statement overwrites p.prev with y; the second sets y.prev = p.prev = y "
                "(a self-loop) and x.next still points to p. **Wrong.**\n\n"
                "**Trap:** modifying p’s *own* pointers before using them — as in (D) — loses the reference to "
                "a neighbour."
            ),
            "verify": '''
class N:
    def __init__(s, v): s.v, s.prev, s.next = v, None, None
def make():
    ns = [N(i) for i in range(5)]
    for a, b in zip(ns, ns[1:]): a.next, b.prev = b, a
    return ns
def ok(ns):
    f, c = [], ns[0]
    while c: f.append(c.v); c = c.next
    b, c = [], ns[4]
    while c and len(b) < 10: b.append(c.v); c = c.prev
    return f == [0, 1, 3, 4] and b == [4, 3, 1, 0]
frags = ["p.prev.next = p.next; p.next.prev = p.prev",
         "p.next.prev = p.prev; p.prev.next = p.next",
         "p.prev.next = p.next; p.prev.next.prev = p.prev",
         "p.prev = p.next; p.next.prev = p.prev"]
res = []
for fr in frags:
    ns = make(); exec(fr, {'p': ns[2]}); res.append(ok(ns))
assert [L for L, r in zip('ABCD', res) if r] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Binary heaps — insertion swaps",
            "text": ("The keys 30, 20, 25, 10, 15, 5, 22 are inserted one at a time, in this order, into an "
                     "initially empty binary **min-heap** (array based; each insertion appends the key and "
                     "sifts it up, swapping with its parent while the parent is larger). The total number of "
                     "swaps performed is ______."),
            "answer": "6",
            "solution": (
                "**Concept.** Sift-up moves a new key upward past every larger ancestor; the number of swaps "
                "equals the number of levels it climbs.\n\n"
                "- 30: [30] — 0 swaps.\n"
                "- 20: child of 30 → swap → [20, 30] — 1.\n"
                "- 25: child of 20 → no swap → [20, 30, 25] — 0.\n"
                "- 10: index 3, parent 30 → swap; parent 20 → swap → [10, 20, 25, 30] — 2.\n"
                "- 15: index 4, parent 20 → swap; parent 10 → stop → [10, 15, 25, 30, 20] — 1.\n"
                "- 5: index 5, parent 25 → swap; parent 10 → swap → [5, 15, 10, 30, 20, 25] — 2.\n"
                "- 22: index 6, parent 10 → stop — 0.\n\n"
                "Total = 0 + 1 + 0 + 2 + 1 + 2 + 0 = **6**. Final heap: [5, 15, 10, 30, 20, 25, 22].\n\n"
                "**Trap:** building with bottom-up heapify instead of repeated insertion gives a *different* "
                "heap and a different swap count — read which method is used."
            ),
            "solution_diagrams": [{"type": "heap", "values": [5, 15, 10, 30, 20, 25, 22],
                                   "caption": "Final min-heap"}],
            "verify": '''
h, sw = [], 0
for x in [30, 20, 25, 10, 15, 5, 22]:
    h.append(x); i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:
        h[(i - 1) // 2], h[i] = h[i], h[(i - 1) // 2]; i = (i - 1) // 2; sw += 1
assert h == [5, 15, 10, 30, 20, 25, 22] and sw == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — minimum of a rotated array",
            "text": "Consider the following Python program. What is printed?",
            "code": '''def find_min(a):
    lo, hi, it = 0, len(a) - 1, 0
    while lo < hi:
        it += 1
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:
            lo = mid + 1
        else:
            hi = mid
    return lo, a[lo], it

print(find_min([24, 31, 2, 5, 9, 13, 17, 20]))''',
            "options": ["`(2, 2, 3)`", "`(2, 2, 4)`", "`(1, 31, 3)`", "`(2, 2, 2)`"],
            "answer": "A",
            "solution": (
                "**Concept.** In a rotated sorted array, comparing a[mid] with a[hi] tells which half holds the "
                "rotation point: a[mid] > a[hi] means the minimum is strictly right of mid; otherwise it is at "
                "mid or to its left.\n\n"
                "- (lo, hi) = (0, 7): mid 3, a[3] = 5 ≤ a[7] = 20 → hi = 3.\n"
                "- (0, 3): mid 1, a[1] = 31 > a[3] = 5 → lo = 2.\n"
                "- (2, 3): mid 2, a[2] = 2 ≤ 5 → hi = 2.\n"
                "- lo = hi = 2 → stop after **3** iterations.\n\n"
                "Returns (2, 2, 3) → (A).\n\n"
                "**Options.** (B) counts the final failed loop test as an iteration. (C) returns the "
                "*maximum* (index of the rotation’s last element). (D) undercounts the trace.\n\n"
                "**Trap:** comparing with a[lo] instead of a[hi] fails when the array is not rotated at all; "
                "the a[hi] comparison works in every case."
            ),
            "verify": "assert OUTPUT.strip() == '(2, 2, 3)' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — linear probing with deletion markers",
            "text": ("Keys 21, 31, 41, 12, 52, 3 are inserted in this order into an empty table of size 10 with "
                     "h(k) = k mod 10 and linear probing. Then 31 is deleted by placing a DELETED marker in its "
                     "slot (searches continue past DELETED and stop at an EMPTY slot). Let x be the number of "
                     "slots examined when searching for 52, and y the number examined in an (unsuccessful) "
                     "search for 72. The value of x + y is ______."),
            "answer": "10",
            "solution": (
                "**Concept.** Lazy deletion keeps probe chains intact: a DELETED slot never stops a search.\n\n"
                "Insertion:\n"
                "- 21 → 1, 31 → 2, 41 → 3.\n"
                "- 12: 2, 3 full → **4**.\n"
                "- 52: 2, 3, 4 full → **5**.\n"
                "- 3: 3, 4, 5 full → **6**.\n\n"
                "Table: 1:21, 2:31, 3:41, 4:12, 5:52, 6:3. After deleting 31, slot 2 holds DELETED.\n\n"
                "- Search 52: slots 2 (DELETED), 3, 4, 5 (found) → x = **4**.\n"
                "- Search 72: slots 2 (DELETED), 3, 4, 5, 6, 7 (EMPTY → stop) → y = **6**.\n\n"
                "x + y = **10**.\n\n"
                "**Trap:** if slot 2 were simply emptied, the search for 52 would stop immediately and "
                "wrongly report “not found” — the reason tombstones exist."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 10,
                                   "slots": {1: 21, 2: "DEL", 3: 41, 4: 12, 5: 52, 6: 3},
                                   "caption": "Table after deleting 31"}],
            "verify": '''
T = [None] * 10
for k in [21, 31, 41, 12, 52, 3]:
    i = k % 10
    while T[i] is not None: i = (i + 1) % 10
    T[i] = k
T[T.index(31)] = 'DEL'
def probes(k):
    i, p = k % 10, 0
    while True:
        p += 1
        if T[i] is None or T[i] == k: return p
        i = (i + 1) % 10
assert probes(52) + probes(72) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Elementary sorts on a reversed array",
            "text": ("The array 6, 5, 4, 3, 2, 1 is sorted into ascending order. Selection sort swaps only when "
                     "the minimum is not already in place; bubble sort and insertion sort are the standard "
                     "versions (insertion sort compares `A[j] > key` while j ≥ 0). Which of the following "
                     "statements is/are TRUE?"),
            "options": [
                "Selection sort performs exactly 3 swaps",
                "Bubble sort performs exactly 15 swaps",
                "Insertion sort performs exactly 20 key comparisons",
                "Selection sort performs exactly 15 key comparisons",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "- (A) Pass 0 swaps 6↔1 → 1 5 4 3 2 6; pass 1 swaps 5↔2 → 1 2 4 3 5 6; pass 2 swaps 4↔3 → "
                "sorted; passes 3 and 4 find the minimum already in place. **3 swaps — TRUE.**\n"
                "- (B) Every adjacent swap removes exactly one inversion; a reversed array of 6 has "
                "6·5/2 = **15** inversions. **TRUE.**\n"
                "- (C) Each key 5, 4, 3, 2, 1 travels to index 0, comparing with every element to its left and "
                "then stopping because j < 0 (no extra comparison): 1 + 2 + 3 + 4 + 5 = **15**, not 20. "
                "**FALSE.**\n"
                "- (D) Selection sort always compares n(n−1)/2 = 15 times, whatever the input. **TRUE.**\n\n"
                "**Tip:** for reversed input, selection sort does ⌊n/2⌋ swaps because each swap fixes *two* "
                "positions at once.\n\n"
                "**Trap:** in (C), adding a “failing” comparison per pass — it never happens when the key "
                "reaches index 0."
            ),
            "verify": '''
A = [6, 5, 4, 3, 2, 1]
a = A[:]; ss = sc = 0
for i in range(5):
    m = i
    for j in range(i + 1, 6):
        sc += 1
        if a[j] < a[m]: m = j
    if m != i: a[i], a[m] = a[m], a[i]; ss += 1
a = A[:]; bs = 0
for p in range(5):
    for j in range(5 - p):
        if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]; bs += 1
a = A[:]; ic = 0
for i in range(1, 6):
    key, j = a[i], i - 1
    while j >= 0:
        ic += 1
        if a[j] > key: a[j + 1] = a[j]; j -= 1
        else: break
    a[j + 1] = key
res = [ss == 3, bs == 15, ic == 20, sc == 15]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "NAT", "marks": 1, "topic": "Graph theory — handshaking lemma",
            "text": ("A simple undirected graph has 12 edges. Exactly three of its vertices have degree 4 and "
                     "every other vertex has degree 3. The number of vertices in the graph is ______."),
            "answer": "7",
            "solution": (
                "**Concept.** Handshaking lemma: the sum of all vertex degrees equals twice the number of "
                "edges, because every edge contributes 1 to the degree of each of its two endpoints.\n\n"
                "Let n be the number of vertices. Then\n"
                "3·4 + (n − 3)·3 = 2·12\n"
                "12 + 3n − 9 = 24\n"
                "3n = 21 → n = **7**.\n\n"
                "Sanity checks: degrees are at most n − 1 = 6, so a simple graph is possible; the degree sum "
                "24 is even as required (and the number of odd-degree vertices, 4, is even).\n\n"
                "**Trap:** forgetting the factor 2 (Σ deg = |E|) gives 3n + 3 = 12 → n = 3, which is "
                "impossible since three vertices of degree 4 need at least 5 vertices."
            ),
            "verify": '''
n = next(n for n in range(3, 50) if 3 * 4 + (n - 3) * 3 == 2 * 12)
assert n == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Binary trees — reconstruction from traversals",
            "text": ("A binary tree with 12 nodes has\n"
                     "pre-order: G B Q A C K F P D E R H\n"
                     "in-order:  Q B K C F A G P E D H R\n"
                     "Its post-order traversal is"),
            "options": ["Q K F C A B E H R D P G", "Q K F C A B H R E D P G",
                        "K F C Q A B E H R D P G", "Q K C F A B E H R D P G"],
            "answer": "A",
            "solution": (
                "**Concept.** The first pre-order element is the root; its position in the in-order splits the "
                "remaining nodes into left and right subtrees. Recurse.\n\n"
                "- Root G; in-order left {Q B K C F A}, right {P E D H R}.\n"
                "- Left: pre-order B Q A C K F → root B; in-order Q | B | K C F A → left Q, right {K C F A} "
                "with root A (next in pre-order); A’s left is {K C F} with root C (children K, F); A has no "
                "right child.\n"
                "- Right: pre-order P D E R H → root P; in-order P | E D H R → P has no left child; right "
                "subtree root D with left E and right {H R} rooted at R (left child H).\n\n"
                "Post-order (left, right, root): Q, K F C A, B, then E, H R, D, P, then G → "
                "**Q K F C A B E H R D P G** → (A).\n\n"
                "**Options.** (B) places H R before E (R’s subtree before D’s left child). (C) puts Q after its "
                "cousins. (D) swaps the children K and F’s order relative to C.\n\n"
                "**Tip:** the last post-order element is always the root (G), and the post-order of each "
                "subtree is contiguous — a quick way to eliminate options."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": ["G", ["B", ["Q"], ["A", ["C", ["K"], ["F"]], None]],
                                            ["P", None, ["D", ["E"], ["R", ["H"], None]]]],
                                   "caption": "Reconstructed tree"}],
            "verify": '''
pre = "G B Q A C K F P D E R H".split(); ino = "Q B K C F A G P E D H R".split()
def build(pre, ino):
    if not pre: return None
    i = ino.index(pre[0])
    return [pre[0], build(pre[1:i + 1], ino[:i]), build(pre[i + 1:], ino[i + 1:])]
post = lambda t: [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
assert ' '.join(post(build(pre, ino))) == "Q K F C A B E H R D P G" and ANSWER == 'A'
''',
        },
        # ============================================================ 2-mark
        # ------------------------------------------------------------ Q11
        {
            "type": "MCQ", "marks": 2, "topic": "Python — generators and iterator exhaustion",
            "text": "Consider the following Python program. What is printed?",
            "code": '''g = (x * x for x in range(5))
a = list(zip(g, g))
b = sum(g)
it = iter([1, 2, 3, 4])
c = [x for x in it if x % 2 == 0] + list(it)
print(a, b, c)''',
            "options": ["`[(0, 0), (1, 1), (4, 4), (9, 9), (16, 16)] 30 [2, 4, 1, 2, 3, 4]`",
                        "`[(0, 1), (4, 9)] 16 [2, 4]`",
                        "`[(0, 1), (4, 9)] 0 [2, 4]`",
                        "`[(0, 1), (4, 9)] 0 [2, 4, 1, 2, 3, 4]`"],
            "answer": "C",
            "solution": (
                "**Concept.** A generator (and any iterator) can be consumed only once; every `next()` call "
                "advances the *same* underlying object, whoever makes it.\n\n"
                "- `zip(g, g)` pulls alternately from the same generator: (0, 1), (4, 9). For the third pair "
                "it pulls 16 for the first slot, then the generator is exhausted for the second slot, so zip "
                "stops — **16 is consumed and discarded**. a = [(0, 1), (4, 9)].\n"
                "- `sum(g)`: g is already exhausted → b = **0**.\n"
                "- The comprehension iterates `it` to the end, keeping 2 and 4; then `list(it)` is empty → "
                "c = **[2, 4]**.\n\n"
                "Output `[(0, 1), (4, 9)] 0 [2, 4]` → (C).\n\n"
                "Option by option:\n"
                "- (A) treats g like a list that can be iterated twice in parallel.\n"
                "- (B) assumes zip “puts back” the unpaired 16.\n"
                "- (D) assumes `list(it)` restarts the iterator.\n\n"
                "**Trap:** `zip(it, it)` is the idiom for chunking into pairs — and an odd leftover element is "
                "silently lost."
            ),
            "verify": "assert OUTPUT.strip() == '[(0, 1), (4, 9)] 0 [2, 4]' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Python — try / except / finally with return",
            "text": "What value does the following program print?",
            "code": '''def f(x):
    try:
        return 10 // x
    except ZeroDivisionError:
        return -1
    finally:
        if x == 2:
            return 99

print(sum(f(x) for x in [0, 1, 2, 5]))''',
            "answer": "110",
            "solution": (
                "**Concept.** A `finally` block runs on every exit from the `try` statement — including a "
                "`return` from `try` or `except`. If `finally` itself executes `return`, that value **replaces** "
                "the pending return value.\n\n"
                "- f(0): `10 // 0` raises ZeroDivisionError → `except` returns −1; finally runs but x ≠ 2 → "
                "result **−1**.\n"
                "- f(1): returns 10 // 1 = **10** (finally does nothing).\n"
                "- f(2): `try` prepares to return 5, but `finally` executes `return 99` → result **99**.\n"
                "- f(5): returns 10 // 5 = **2**.\n\n"
                "Sum = −1 + 10 + 99 + 2 = **110**.\n\n"
                "**Trap:** assuming the `try` block’s `return` wins (giving 5 for f(2) and a sum of 16), or "
                "assuming the exception propagates for x = 0. A `return` inside `finally` also silently "
                "swallows any in-flight exception, which is why linters warn about it.\n\n"
                "**Order of events for f(2):** the expression `10 // 2` is evaluated and the value 5 is "
                "stashed as the pending return value; control then enters `finally`, where `return 99` "
                "discards the stashed 5. For x = 1 and x = 5 the `finally` block falls through, so the "
                "stashed value is returned unchanged."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER == '110'",
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "BST — deletion with in-order successor",
            "text": ("In the BST below, key 28 is deleted and then key 75 is deleted. A node with two children is "
                     "deleted by copying its **in-order successor** into it and then deleting the successor from "
                     "the right subtree. Which of the following statements about the final tree is/are TRUE? "
                     "(Height = number of edges on the longest root-to-leaf path.)"),
            "diagrams": [{"type": "bintree",
                          "tree": [50, [28, [14], [40, [33, None, [36]], [45]]],
                                   [75, [62, [58], [70]], [90, [80], [95]]]],
                          "caption": "Initial BST"}],
            "options": [
                "The left child of the root is 36",
                "36 is the left child of 40",
                "The height of the tree is 3",
                "The pre-order traversal is 50, 33, 14, 40, 36, 45, 80, 62, 58, 70, 90, 95",
            ],
            "answer": ["B", "C", "D"],
            "solution": (
                "**Concept.** The in-order successor of a node with two children is the leftmost node of its "
                "right subtree; it has no left child, so removing it is a one-child (or leaf) deletion.\n\n"
                "**Delete 28:** right subtree is rooted at 40; its leftmost node is **33** (33 has a right child "
                "36). Copy 33 into the node of 28, then remove the old 33 by linking its child 36 to 40’s left. "
                "Left subtree becomes 33 → (14, 40), 40 → (36, 45).\n\n"
                "**Delete 75:** successor = leftmost of the subtree at 90 = **80** (a leaf). Copy 80 up and "
                "remove the leaf. Right subtree becomes 80 → (62, 90), 62 → (58, 70), 90 → (–, 95).\n\n"
                "- (A) The root’s left child is 33, not 36 (36 would be the answer only if we had promoted the "
                "successor’s *child*). **FALSE.**\n"
                "- (B) 36 now hangs from 40 as its left child. **TRUE.**\n"
                "- (C) Longest paths, e.g. 50→33→40→36, have 3 edges (before the deletions the height was 4 "
                "via 28→40→33→36). **TRUE.**\n"
                "- (D) Pre-order: 50, 33, 14, 40, 36, 45, 80, 62, 58, 70, 90, 95. **TRUE.**\n\n"
                "**Trap:** using the in-order *predecessor* for 28 would promote 14 instead of 33, giving a "
                "different tree."
            ),
            "solution_diagrams": [{"type": "bintree",
                                   "tree": [50, [33, [14], [40, [36], [45]]],
                                            [80, [62, [58], [70]], [90, None, [95]]]],
                                   "highlight": [33, 80], "caption": "After deleting 28 and 75"}],
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
        s = t[2]
        while s[1]: s = s[1]
        t[0] = s[0]; t[2] = delete(t[2], s[0])
    return t
t = None
for k in [50, 28, 75, 14, 40, 62, 90, 33, 45, 58, 70, 80, 95, 36]: t = ins(t, k)
t = delete(delete(t, 28), 75)
h = lambda t: -1 if t is None else 1 + max(h(t[1]), h(t[2]))
pre = lambda t: [] if t is None else [t[0]] + pre(t[1]) + pre(t[2])
res = [t[1][0] == 36, t[1][2][1][0] == 36, h(t) == 3,
       pre(t) == [50, 33, 14, 40, 36, 45, 80, 62, 58, 70, 90, 95]]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Bottom-up merge sort — comparisons",
            "text": ("Bottom-up (iterative) merge sort is applied to the 11-element array below. In the pass with "
                     "run width w = 1, 2, 4, 8 it merges A[lo..lo+w−1] with A[lo+w..lo+2w−1] for lo = 0, 2w, "
                     "4w, … (a final run with no partner is left as it is). A merge stops comparing as soon as one "
                     "run is exhausted. The total number of element comparisons is ______."),
            "diagrams": [{"type": "array", "values": [12, 7, 3, 18, 9, 1, 15, 4, 11, 6, 2], "label": "A"}],
            "answer": "27",
            "solution": (
                "**Concept.** Bottom-up merge sort runs ⌈log₂ n⌉ passes; a merge of runs of length p and q "
                "costs (p + q) minus the number of elements left over when one run empties.\n\n"
                "- **w = 1:** pairs (12,7), (3,18), (9,1), (15,4), (11,6) → 5 comparisons; 2 is unpaired. "
                "A = 7 12 | 3 18 | 1 9 | 4 15 | 6 11 | 2.\n"
                "- **w = 2:** [7,12]+[3,18] → 3, 7, 12 then copy 18: **3**; [1,9]+[4,15] → 1, 4, 9 then copy "
                "15: **3**; [6,11]+[2] → 2 then copy: **1**. Pass total 7. "
                "A = 3 7 12 18 | 1 4 9 15 | 2 6 11.\n"
                "- **w = 4:** [3,7,12,18]+[1,4,9,15] → outputs 1, 3, 4, 7, 9, 12, 15 with 7 comparisons, then "
                "copy 18: **7**. [2, 6, 11] has no partner.\n"
                "- **w = 8:** [1,3,4,7,9,12,15,18]+[2,6,11] → outputs 1, 2, 3, 4, 6, 7, 9, 11 (8 comparisons), "
                "then copy 12, 15, 18: **8**.\n\n"
                "Total = 5 + 7 + 7 + 8 = **27**.\n\n"
                "**Trap:** assuming top-down and bottom-up merge sort split the same way — for n = 11 they "
                "do not (bottom-up merges 8 + 3 at the end), so their comparison counts can differ."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each pass",
                                   "col_labels": [str(i) for i in range(11)] + ["comps"],
                                   "row_labels": ["w=1", "w=2", "w=4", "w=8"],
                                   "rows": [[7, 12, 3, 18, 1, 9, 4, 15, 6, 11, 2, 5],
                                            [3, 7, 12, 18, 1, 4, 9, 15, 2, 6, 11, 7],
                                            [1, 3, 4, 7, 9, 12, 15, 18, 2, 6, 11, 7],
                                            [1, 2, 3, 4, 6, 7, 9, 11, 12, 15, 18, 8]]}],
            "verify": '''
a = [12, 7, 3, 18, 9, 1, 15, 4, 11, 6, 2]; n = len(a); w = 1; c = 0
while w < n:
    for lo in range(0, n, 2 * w):
        mid, hi = min(lo + w, n), min(lo + 2 * w, n)
        if mid >= hi: continue
        L, R, i, j, out = a[lo:mid], a[mid:hi], 0, 0, []
        while i < len(L) and j < len(R):
            c += 1
            if L[i] <= R[j]: out.append(L[i]); i += 1
            else: out.append(R[j]); j += 1
        a[lo:hi] = out + L[i:] + R[j:]
    w *= 2
assert a == sorted(a) and c == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Quicksort — Hoare partition",
            "text": ("The Hoare partition below is called as `hoare(A, 0, 8)` on "
                     "`A = [11, 4, 17, 8, 2, 19, 6, 14, 9]`. Which option gives the returned index and the "
                     "array immediately after the call?"),
            "code": '''def hoare(A, lo, hi):
    p = A[lo]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while A[i] < p:
            i += 1
        j -= 1
        while A[j] > p:
            j -= 1
        if i >= j:
            return j
        A[i], A[j] = A[j], A[i]''',
            "options": ["4 and [9, 4, 6, 8, 2, 19, 17, 14, 11]",
                        "5 and [9, 4, 6, 8, 2, 19, 17, 14, 11]",
                        "4 and [9, 4, 6, 8, 2, 11, 17, 14, 19]",
                        "5 and [2, 4, 6, 8, 9, 11, 19, 17, 14]"],
            "answer": "A",
            "solution": (
                "**Concept.** Hoare’s scheme moves i right to an element ≥ pivot and j left to an element "
                "≤ pivot, swaps them, and repeats until the pointers cross. It returns j such that every "
                "element of A[lo..j] is ≤ pivot and every element of A[j+1..hi] is ≥ pivot. The pivot is "
                "**not** necessarily in its final position.\n\n"
                "Pivot p = 11.\n"
                "- Round 1: i stops at 0 (11 ≥ 11); j stops at 8 (9 ≤ 11). Swap → [9, 4, 17, 8, 2, 19, 6, 14, "
                "11].\n"
                "- Round 2: i moves 1 (4), stops at 2 (17); j moves 7 (14 > 11), stops at 6 (6). Swap → "
                "[9, 4, 6, 8, 2, 19, 17, 14, 11].\n"
                "- Round 3: i moves 3, 4, stops at 5 (19); j moves 5 (19 > 11), stops at 4 (2). Now i = 5 ≥ "
                "j = 4 → return **4**.\n\n"
                "Result: 4 and [9, 4, 6, 8, 2, 19, 17, 14, 11] → (A). Left part {9, 4, 6, 8, 2} ≤ 11, right "
                "part {19, 17, 14, 11} ≥ 11.\n\n"
                "**Options.** (B) returns i instead of j. (C) places the pivot between the parts as Lomuto "
                "would. (D) is not produced by any single partition.\n\n"
                "**Trap:** with Hoare partition, recurse on A[lo..j] and A[j+1..hi] — *not* on j−1, because "
                "the pivot may sit inside the right part (here 11 is at index 8)."
            ),
            "verify": '''
A = [11, 4, 17, 8, 2, 19, 6, 14, 9]
r = hoare(A, 0, 8)
assert (r, A) == (4, [9, 4, 6, 8, 2, 19, 17, 14, 11]) and ANSWER == 'A'
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "Dijkstra — sum of shortest distances",
            "text": ("Dijkstra’s algorithm is run from S on the undirected weighted graph below. The sum of the "
                     "shortest-path distances from S to all seven vertices (including d(S) = 0) is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["S", "A", "B", "C", "D", "E", "T"],
                          "edges": [["S", "A", 5], ["S", "B", 2], ["A", "B", 2], ["A", "C", 4], ["B", "D", 7],
                                    ["A", "D", 6], ["C", "D", 1], ["C", "T", 8], ["D", "E", 2], ["E", "T", 3],
                                    ["B", "E", 12]],
                          "pos": {"S": [0, 1], "A": [1.5, 2.2], "B": [1.5, -0.2], "C": [3.2, 2.6],
                                  "D": [3.2, 1], "E": [4.8, -0.2], "T": [6.2, 1.6]}}],
            "answer": "48",
            "solution": (
                "**Concept.** Dijkstra finalises vertices in increasing order of distance; each extraction "
                "relaxes the edges of the extracted vertex.\n\n"
                "- Extract S (0): A = 5, B = 2.\n"
                "- Extract B (2): A = min(5, 2+2) = 4; D = 9; E = 14.\n"
                "- Extract A (4): C = 8; D = min(9, 10) = 9.\n"
                "- Extract C (8): D = min(9, 9) — tie, unchanged; T = 16.\n"
                "- Extract D (9): E = min(14, 11) = 11.\n"
                "- Extract E (11): T = min(16, 14) = 14.\n"
                "- Extract T (14).\n\n"
                "Distances: S 0, A 4, B 2, C 8, D 9, E 11, T 14 → sum = 0+4+2+8+9+11+14 = **48**.\n\n"
                "**Trap:** taking the direct edges S–A (5), B–E (12) or C–T (8 + 8 = 16) at face value — "
                "each of them is beaten by a detour (S-B-A = 4, S-B-D-E = 11, …-D-E-T = 14)."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Tentative distances after each extraction",
                                   "col_labels": ["S", "A", "B", "C", "D", "E", "T"],
                                   "row_labels": ["S", "B", "A", "C", "D", "E"],
                                   "rows": [[0, 5, 2, "∞", "∞", "∞", "∞"], [0, 4, 2, "∞", 9, 14, "∞"],
                                            [0, 4, 2, 8, 9, 14, "∞"], [0, 4, 2, 8, 9, 14, 16],
                                            [0, 4, 2, 8, 9, 11, 16], [0, 4, 2, 8, 9, 11, 14]]}],
            "verify": '''
import heapq
E = [('S','A',5),('S','B',2),('A','B',2),('A','C',4),('B','D',7),('A','D',6),
     ('C','D',1),('C','T',8),('D','E',2),('E','T',3),('B','E',12)]
G = {}
for u, v, w in E:
    G.setdefault(u, []).append((v, w)); G.setdefault(v, []).append((u, w))
d = {v: float('inf') for v in G}; d['S'] = 0; pq = [(0, 'S')]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d.values()) == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MSQ", "marks": 2, "topic": "DFS — valid traversal orders",
            "text": ("Depth-first search is started at A on the undirected graph below, with **no** fixed rule "
                     "for the order in which neighbours are tried. Which of the following are possible DFS "
                     "visiting (discovery) orders?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                          "edges": [["A", "B"], ["A", "C"], ["A", "D"], ["B", "E"], ["C", "E"], ["C", "F"],
                                    ["D", "F"], ["E", "G"], ["F", "G"]],
                          "pos": {"A": [0, 1], "B": [1.5, 2], "C": [1.5, 1], "D": [1.5, 0], "E": [3, 2],
                                  "F": [3, 0], "G": [4.5, 1]}}],
            "options": ["A B E G F C D", "A B E C D F G", "A D F G C E B", "A C E B G F D"],
            "answer": ["A", "D"],
            "solution": (
                "**Concept.** In DFS, the next discovered vertex must be an unvisited neighbour of the "
                "**deepest** vertex on the current path that still has unvisited neighbours (backtracking only "
                "when the current vertex is exhausted).\n\n"
                "- (A) A→B→E→G→F (G–F) → C (F–C) → D: at C, its neighbours A, E, F are visited, so backtrack "
                "to F, whose unvisited neighbour D is next. **Valid.**\n"
                "- (B) A→B→E→C; now C still has an unvisited neighbour F, so the next vertex must be F — D is "
                "not adjacent to C. **Invalid.**\n"
                "- (C) A→D→F→G; G’s unvisited neighbour E must come next, but C is not adjacent to G. "
                "**Invalid.**\n"
                "- (D) A→C→E→B; B is exhausted → back to E → G → F (G–F) → D (F–D). **Valid.**\n\n"
                "**Trap:** checking only that each vertex is adjacent to *some* earlier vertex — that is the "
                "condition for a valid *BFS-like or arbitrary-search* order, not for DFS. The backtracking "
                "rule is what (B) and (C) violate."
            ),
            "verify": '''
G = {'A':'BCD','B':'AE','C':'AEF','D':'AF','E':'BCG','F':'CDG','G':'EF'}
def valid(order):
    order = order.split()
    st, vis = [order[0]], {order[0]}
    for x in order[1:]:
        while st and all(v in vis for v in G[st[-1]]): st.pop()
        if not st or x not in G[st[-1]] or x in vis: return False
        vis.add(x); st.append(x)
    return len(vis) == 7
opts = ["A B E G F C D", "A B E C D F G", "A D F G C E B", "A C E B G F D"]
assert [L for L, o in zip('ABCD', opts) if valid(o)] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "NAT", "marks": 2, "topic": "Queues — round-robin scheduling simulation",
            "text": ("Five processes are scheduled with round robin using a FIFO ready queue and time quantum 3:\n"
                     "P1 (arrival 0, burst 7), P2 (1, 4), P3 (2, 9), P4 (4, 3), P5 (6, 5).\n"
                     "When a quantum ends, processes that have arrived up to and including that instant are "
                     "enqueued **before** the preempted process is put back at the rear. Context switches take "
                     "no time. The average turnaround time (completion − arrival) is ______ "
                     "(rounded off to two decimal places)."),
            "answer": ["19.39", "19.41"],
            "solution": (
                "**Concept.** Simulate the ready queue exactly; the tie rule at time 6 (P5 arrives as P2’s "
                "quantum ends) matters.\n\n"
                "- 0–3 P1 (rem 4). Arrived: P2, P3 → queue P2 P3 P1.\n"
                "- 3–6 P2 (rem 1). Arrived: P4 (4), P5 (6) → queue P3 P1 P4 P5 P2.\n"
                "- 6–9 P3 (rem 6) → P1 P4 P5 P2 P3.\n"
                "- 9–12 P1 (rem 1) → P4 P5 P2 P3 P1.\n"
                "- 12–15 P4 finishes (**15**).\n"
                "- 15–18 P5 (rem 2) → P2 P3 P1 P5.\n"
                "- 18–19 P2 finishes (**19**).\n"
                "- 19–22 P3 (rem 3) → P1 P5 P3.\n"
                "- 22–23 P1 finishes (**23**). 23–25 P5 finishes (**25**). 25–28 P3 finishes (**28**).\n\n"
                "Turnaround: P1 23 − 0 = 23, P2 19 − 1 = 18, P3 28 − 2 = 26, P4 15 − 4 = 11, P5 25 − 6 = 19. "
                "Sum = 97 → average 97/5 = **19.40**.\n\n"
                "**Trap:** re-queuing the preempted process *before* the new arrivals changes the order "
                "(e.g. P2 would precede P5 at time 6) and the answer. Also, the last completion is always the "
                "total burst time (28) when the CPU is never idle — a useful check."
            ),
            "solution_diagrams": [{"type": "queue", "values": ["P3", "P1", "P4", "P5", "P2"],
                                   "caption": "Ready queue at time 6"}],
            "verify": '''
from collections import deque
procs = [('P1', 0, 7), ('P2', 1, 4), ('P3', 2, 9), ('P4', 4, 3), ('P5', 6, 5)]
rem = {p: b for p, a, b in procs}; arr = {p: a for p, a, b in procs}
t, i, q, done = 0, 0, deque(), {}
while len(done) < 5:
    while i < 5 and procs[i][1] <= t: q.append(procs[i][0]); i += 1
    p = q.popleft(); run = min(3, rem[p]); t += run; rem[p] -= run
    while i < 5 and procs[i][1] <= t: q.append(procs[i][0]); i += 1
    if rem[p] == 0: done[p] = t
    else: q.append(p)
avg = sum(done[p] - arr[p] for p in done) / 5
assert float(ANSWER[0]) <= avg <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "MCQ", "marks": 2, "topic": "Linked lists — reversing in groups of k",
            "text": "Consider the following Python program. What is printed?",
            "code": '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def rev_k(head, k):
    cur, n = head, 0
    while cur and n < k:
        cur = cur.nxt; n += 1
    if n < k:
        return head
    prev, cur = rev_k(cur, k), head
    for _ in range(k):
        cur.nxt, prev, cur = prev, cur, cur.nxt
    return prev

h = None
for x in reversed(range(1, 9)):
    h = Node(x, h)
h = rev_k(h, 3)
out = []
while h:
    out.append(h.v); h = h.nxt
print(*out)''',
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7, 8], "head": "h"}],
            "options": ["`3 2 1 6 5 4 8 7`", "`3 2 1 6 5 4 7 8`", "`8 7 6 5 4 3 2 1`", "`1 2 3 4 5 6 7 8`"],
            "answer": "B",
            "solution": (
                "**Concept.** `rev_k` first checks that at least k nodes remain; if not, the tail is returned "
                "unchanged. Otherwise it recursively processes the rest, then reverses the first k nodes, "
                "pointing the old first node at the processed remainder.\n\n"
                "- Call on 1…8: 3 nodes exist; recurse on 4…8.\n"
                "- Call on 4…8: recurse on 7 → 8.\n"
                "- Call on 7 → 8: only 2 < 3 nodes → returned **unchanged**.\n"
                "- Back in 4…8: reverse 4, 5, 6 with prev starting at node 7 → 6 → 5 → 4 → 7 → 8.\n"
                "- Back in 1…8: reverse 1, 2, 3 with prev starting at node 6 → 3 → 2 → 1 → 6 → 5 → 4 → 7 → 8.\n\n"
                "Output `3 2 1 6 5 4 7 8` → (B).\n\n"
                "**Trap (tuple assignment).** All right-hand values (prev, cur, cur.nxt) are evaluated "
                "first; then `cur.nxt` is assigned while `cur` still names the old node, and only afterwards is "
                "`cur` advanced — so the line is correct. (Writing `cur, cur.nxt, prev = …` would assign "
                "`cur` first and corrupt the wrong node.)\n\n"
                "**Options.** (A) also reverses the incomplete last group. (C) reverses the whole list. "
                "(D) assumes nothing changes."
            ),
            "verify": "assert OUTPUT.strip() == '3 2 1 6 5 4 7 8' and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Hashing — linear probing analysis",
            "text": ("Keys 8, 19, 13, 2, 25, 30, 6 are inserted in this order into an empty hash table with 11 "
                     "slots (0–10) using h(k) = (2k + 3) mod 11 and linear probing (step +1, wrapping around). "
                     "A *probe* is one slot examination; a successful first examination counts as 1 probe. "
                     "Which of the following statements is/are TRUE?"),
            "options": [
                "Key 30 is stored in slot 1",
                "The total number of probes over all seven insertions is 16",
                "The longest run of consecutive occupied slots (with wrap-around) has length 6",
                "If key 41 is inserted next, it is stored in slot 3",
            ],
            "answer": ["A", "C"],
            "solution": (
                "**Concept.** Compute the home slot, then step +1 mod 11 until an empty slot is found.\n\n"
                "- 8: (16+3) mod 11 = 8 → slot 8 (1 probe).\n"
                "- 19: 41 mod 11 = 8 → 8 full → **9** (2 probes).\n"
                "- 13: 29 mod 11 = 7 → slot 7 (1).\n"
                "- 2: 7 mod 11 = 7 → 7, 8, 9 full → **10** (4).\n"
                "- 25: 53 mod 11 = 9 → 9, 10 full → **0** (3).\n"
                "- 30: 63 mod 11 = 8 → 8, 9, 10, 0 full → **1** (5).\n"
                "- 6: 15 mod 11 = 4 → slot 4 (1).\n\n"
                "Final table: 0:25, 1:30, 4:6, 7:13, 8:8, 9:19, 10:2.\n\n"
                "- (A) 30 is in slot 1. **TRUE.**\n"
                "- (B) Probes = 1+2+1+4+3+5+1 = **17**, not 16. **FALSE.**\n"
                "- (C) Slots 7, 8, 9, 10, 0, 1 form one wrapped cluster of length **6**. **TRUE.**\n"
                "- (D) h(41) = 85 mod 11 = 8 → 8, 9, 10, 0, 1 full → slot **2**, not 3. **FALSE.**\n\n"
                "**Trap:** forgetting wrap-around — the cluster 7..10 continues into 0..1, which is exactly why "
                "30 and 41 travel so far (primary clustering)."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11,
                                   "slots": {0: 25, 1: 30, 4: 6, 7: 13, 8: 8, 9: 19, 10: 2},
                                   "caption": "Final table"}],
            "verify": '''
T = [None] * 11; tot = 0
def put(k):
    global tot
    i = (2 * k + 3) % 11; tot += 1
    while T[i] is not None: i = (i + 1) % 11; tot += 1
    T[i] = k; return i
for k in [8, 19, 13, 2, 25, 30, 6]: put(k)
probes = tot
occ = [x is not None for x in T]; best = 0
for s in range(11):
    L = 0
    while L < 11 and occ[(s + L) % 11]: L += 1
    best = max(best, L)
slot41 = put(41)
res = [T.index(30) == 1, probes == 16, best == 6, slot41 == 3]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
    ],
}
