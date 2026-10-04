# Set 44 — Full-Syllabus Mock — Paper 14 (GATE-level)
SET = {
    "number": 44,
    "title": "Full-Syllabus Mock — Paper 14",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ---------------------------------------------------------------- Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — `+=` versus `+` on lists",
            "text": "What is printed by the following Python program?",
            "code": '''a = [1, 2]
b = a
b += [3]
c = a
c = c + [4]
print(a, c, a is b)''',
            "options": ["`[1, 2] [1, 2, 4] False`", "`[1, 2, 3] [1, 2, 3, 4] True`",
                        "`[1, 2, 3, 4] [1, 2, 3, 4] True`", "`[1, 2, 3] [1, 2, 3, 4] False`"],
            "answer": "B",
            "solution": (
                "**Concept.** For lists, `b += [3]` calls `list.__iadd__`, which **extends the existing list in "
                "place** and rebinds b to the same object. `c = c + [4]` builds a **new** list and rebinds only "
                "c.\n\n"
                "**Trace.**\n"
                "- `b = a`: one list [1, 2], two names.\n"
                "- `b += [3]`: the shared list becomes [1, 2, 3]; a and b still refer to it.\n"
                "- `c = a`, then `c = c + [4]`: a new list [1, 2, 3, 4] is bound to c; a is unchanged.\n"
                "- `a is b` → True.\n\n"
                "Output: `[1, 2, 3] [1, 2, 3, 4] True`.\n\n"
                "**Options.**\n"
                "- (A) treats `+=` like `+` (creating a new list for b).\n"
                "- (C) treats `c = c + [4]` as an in-place change of a.\n"
                "- (D) thinks `+=` rebinds b to a different object.\n\n"
                "**Trap:** for immutable types (int, str, tuple) `x += y` always creates a new object; for "
                "lists it mutates — the same syntax, different semantics."
            ),
            "verify": "assert OUTPUT.strip() == '[1, 2, 3] [1, 2, 3, 4] True' and ANSWER == 'B'",
        },
        # ---------------------------------------------------------------- Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — dictionary keys and overwriting",
            "text": "What value is printed by the following Python program?",
            "code": '''d = {x % 4: x for x in [3, 8, 11, 14, 7, 20]}
e = {1: 'a', True: 'b', 1.0: 'c'}
print(sum(d.values()) + len(e))''',
            "answer": "42",
            "solution": (
                "**Concept.** In a dict comprehension a repeated key keeps its first insertion position but its "
                "value is overwritten by the *last* assignment. Keys are compared by hash and equality, and "
                "`1 == True == 1.0` with equal hashes, so they are the **same** key.\n\n"
                "**d.** Keys x % 4: 3→3, 8→0, 11→3, 14→2, 7→3, 20→0.\n"
                "- key 3: 3, then 11, then 7 → final 7\n"
                "- key 0: 8, then 20 → final 20\n"
                "- key 2: 14\n"
                "sum(d.values()) = 7 + 20 + 14 = 41.\n\n"
                "**e.** All three keys are equal, so e has a single entry {1: 'c'} (first key object kept, last "
                "value) → len(e) = 1.\n\n"
                "Printed: 41 + 1 = **42**.\n\n"
                "**Trap:** expecting len(e) = 3 (keys look different) or summing all six numbers (63)."
            ),
            "verify": '''
dd = {}
for x in [3, 8, 11, 14, 7, 20]: dd[x % 4] = x
assert sum(dd.values()) + 1 == int(ANSWER) == int(OUTPUT.strip()) and e == {1: 'c'}
''',
        },
        # ---------------------------------------------------------------- Q3
        {
            "type": "MCQ", "marks": 1, "topic": "Stacks — prefix expression evaluation",
            "text": ("The prefix (Polish) expression\n\n`- * + 4 3 2 / 8 ^ 2 2`\n\nis evaluated with a stack by "
                     "scanning the tokens from **right to left** (push operands; on an operator pop the top two "
                     "values x then y and push x op y). Here `/` is integer division and `^` is exponentiation. "
                     "The result is"),
            "options": ["12", "-12", "14", "2"],
            "answer": "A",
            "solution": (
                "**Concept.** Scanning a prefix expression right-to-left makes it behave like postfix, but the "
                "operand order flips: the **first** value popped is the **left** operand.\n\n"
                "**Trace** (stack bottom → top):\n"
                "- 2 → [2]; 2 → [2, 2]\n"
                "- ^ : x = 2, y = 2 → 2 ^ 2 = 4 → [4]\n"
                "- 8 → [4, 8]\n"
                "- / : x = 8, y = 4 → 8 / 4 = 2 → [2]\n"
                "- 2 → [2, 2]; 3 → [2, 2, 3]; 4 → [2, 2, 3, 4]\n"
                "- + : 4 + 3 = 7 → [2, 2, 7]\n"
                "- * : 7 × 2 = 14 → [2, 14]\n"
                "- − : x = 14, y = 2 → 14 − 2 = **12**.\n\n"
                "Infix form: ((4 + 3) × 2) − (8 / (2 ^ 2)) = 14 − 2 = 12.\n\n"
                "**Options.**\n"
                "- (B) −12 swaps the operands of − (computes y − x).\n"
                "- (C) 14 and (D) 2 are the values of the two operand sub-expressions of the outer −.\n\n"
                "**Trap:** with right-to-left scanning, popping order is the reverse of postfix evaluation."
            ),
            "verify": '''
st = []
for t in reversed("- * + 4 3 2 / 8 ^ 2 2".split()):
    if t.isdigit(): st.append(int(t))
    else:
        x, y = st.pop(), st.pop()
        st.append({'+': x + y, '-': x - y, '*': x * y, '/': x // y, '^': x ** y}[t])
assert ["12", "-12", "14", "2"]["ABCD".index(ANSWER)] == str(st[0])
''',
        },
        # ---------------------------------------------------------------- Q4
        {
            "type": "MCQ", "marks": 1, "topic": "Deques — bounded deque in Python",
            "text": "What is printed by the following Python program?",
            "code": '''from collections import deque
dq = deque(maxlen=3)
for x in range(1, 6):
    dq.append(x)
dq.appendleft(0)
dq.rotate(1)
print(list(dq))''',
            "options": ["`[0, 3, 4]`", "`[4, 0, 3]`", "`[5, 0, 3]`", "`[3, 4, 5]`"],
            "answer": "B",
            "solution": (
                "**Concept.** A deque with `maxlen` discards from the **opposite end** when full: `append` "
                "drops the leftmost item, `appendleft` drops the rightmost. `rotate(1)` moves the last element "
                "to the front.\n\n"
                "**Trace.**\n"
                "- Appending 1..5: [1] → [1, 2] → [1, 2, 3] → [2, 3, 4] → [3, 4, 5].\n"
                "- `appendleft(0)`: deque is full, so 5 is dropped from the right → [0, 3, 4].\n"
                "- `rotate(1)`: last element 4 goes to the front → [4, 0, 3].\n\n"
                "**Options.**\n"
                "- (A) forgets the rotation.\n"
                "- (C) assumes appendleft dropped from the left end (the 4) and kept 5.\n"
                "- (D) assumes appendleft is ignored on a full deque.\n\n"
                "**Tip:** a `deque(maxlen=k)` is a ready-made sliding window / circular buffer of the last k "
                "items, with O(1) operations at both ends."
            ),
            "solution_diagrams": [{"type": "queue", "values": [4, 0, 3],
                                   "caption": "Final deque (left → right)"}],
            "verify": "assert OUTPUT.strip() == '[4, 0, 3]' and ANSWER == 'B'",
        },
        # ---------------------------------------------------------------- Q5
        {
            "type": "NAT", "marks": 1, "topic": "Linked lists — middle node with slow/fast pointers",
            "text": "What value is printed by the following Python program?",
            "code": '''class Node:
    def __init__(self, val, nxt=None):
        self.val, self.next = val, nxt

def mid1(h):
    slow = fast = h
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow

def mid2(h):
    slow = fast = h
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    return slow

head = None
for v in reversed([12, 7, 30, 5, 18, 41, 9, 26]):
    head = Node(v, head)
print(mid1(head).val - mid2(head).val)''',
            "diagrams": [{"type": "linkedlist", "values": [12, 7, 30, 5, 18, 41, 9, 26], "head": "head"}],
            "answer": "13",
            "solution": (
                "**Concept.** For a list of even length n, the two loop conditions pick different middles: "
                "`while fast and fast.next` stops with slow at index n/2 (the **second** middle); "
                "`while fast.next and fast.next.next` stops with slow at index n/2 − 1 (the **first** middle).\n\n"
                "**mid1** (indices 0-based): (slow, fast) = (0, 0) → (1, 2) → (2, 4) → (3, 6) → (4, 8 = None). "
                "Loop stops; slow at index 4 → value 18.\n\n"
                "**mid2**: (0, 0) → (1, 2) → (2, 4) → (3, 6); now fast.next is index 7 but fast.next.next is "
                "None → stop. slow at index 3 → value 5.\n\n"
                "Printed: 18 − 5 = **13**.\n\n"
                "**Trap:** both functions agree on odd-length lists; only even lengths reveal the difference. "
                "Merge sort on linked lists usually wants `mid2` so that both halves are non-empty for n = 2."
            ),
            "verify": '''
L = [12, 7, 30, 5, 18, 41, 9, 26]
assert L[len(L) // 2] - L[len(L) // 2 - 1] == int(ANSWER) == int(OUTPUT.strip())
''',
        },
        # ---------------------------------------------------------------- Q6
        {
            "type": "MSQ", "marks": 1, "topic": "BST — possible search paths",
            "text": ("A binary search tree contains integer keys from 1 to 100 (not necessarily all of them), and "
                     "a search for the key **55** is performed. Which of the following could be the sequence of "
                     "keys examined by the search?"),
            "options": ["90, 20, 70, 30, 60, 50, 55", "10, 80, 40, 75, 45, 60, 55",
                        "70, 30, 65, 40, 68, 55", "25, 95, 50, 90, 52, 58, 53, 55"],
            "answer": ["A", "B", "D"],
            "solution": (
                "**Concept.** Maintain the open interval (low, high) of keys still possible. Each examined key "
                "must lie inside the current interval; if it is greater than 55 it becomes the new high, if "
                "smaller the new low.\n\n"
                "- (A) (−∞,∞): 90 → (−∞,90); 20 → (20,90); 70 → (20,70); 30 → (30,70); 60 → (30,60); "
                "50 → (50,60); 55 ✓. **Possible.**\n"
                "- (B) 10 → (10,∞); 80 → (10,80); 40 → (40,80); 75 → (40,75); 45 → (45,75); 60 → (45,60); "
                "55 ✓. **Possible.**\n"
                "- (C) 70 → (−∞,70); 30 → (30,70); 65 → (30,65); 40 → (40,65); **68 is outside (40,65)** — "
                "after going left at 65, every later key must be < 65. **Not possible.**\n"
                "- (D) 25 → (25,∞); 95 → (25,95); 50 → (50,95); 90 → (50,90); 52 → (52,90); 58 → (52,58); "
                "53 → (53,58); 55 ✓. **Possible.**\n\n"
                "**Trap:** checking only the immediate parent (68 > 40, so 'go right' looks fine) misses the "
                "constraint imposed by the earlier ancestor 65."
            ),
            "verify": '''
def ok(seq, key=55):
    lo, hi = float('-inf'), float('inf')
    for x in seq[:-1]:
        if not lo < x < hi: return False
        if x > key: hi = x
        else: lo = x
    return seq[-1] == key and lo < key < hi
opts = [[90, 20, 70, 30, 60, 50, 55], [10, 80, 40, 75, 45, 60, 55],
        [70, 30, 65, 40, 68, 55], [25, 95, 50, 90, 52, 58, 53, 55]]
assert [L for L, s in zip("ABCD", opts) if ok(s)] == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — linear probing with wrap-around",
            "text": ("Keys 4, 15, 9, 26, 20 are inserted in this order into an empty hash table with slots 0–10, "
                     "using h(k) = (2k + 3) mod 11 and linear probing (slot after 10 is 0). In which slot is "
                     "20 stored?"),
            "options": ["3", "0", "4", "2"],
            "answer": "A",
            "solution": (
                "**Concept.** Linear probing scans h, h+1, h+2, … modulo the table size, so a search that "
                "starts near the end of the table wraps around to slot 0.\n\n"
                "**Hash values.** 4 → 11 mod 11 = 0; 15 → 33 mod 11 = 0; 9 → 21 mod 11 = 10; "
                "26 → 55 mod 11 = 0; 20 → 43 mod 11 = 10.\n\n"
                "**Trace.**\n"
                "- 4 → slot 0.\n- 15 → 0 full → slot 1.\n- 9 → slot 10.\n- 26 → 0, 1 full → slot 2.\n"
                "- 20 → 10 full → 0 → 1 → 2 full → slot **3**.\n\n"
                "**Options.**\n"
                "- (B) 0 is 20's position if wrap-around were applied without checking occupancy.\n"
                "- (C) 4 skips one slot too many.\n"
                "- (D) 2 is 26's slot — it would be 20's only if 20 had been inserted before 26.\n\n"
                "**Insight:** keys with different home slots (0 and 10) merge into one cluster across the "
                "wrap-around — primary clustering does not respect the 'end' of the array."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 11, "slots": {0: 4, 1: 15, 2: 26, 3: 20, 10: 9},
                                   "caption": "Final table"}],
            "verify": '''
T = [None] * 11
for k in [4, 15, 9, 26, 20]:
    i = (2 * k + 3) % 11
    while T[i] is not None: i = (i + 1) % 11
    T[i] = k
assert ["3", "0", "4", "2"]["ABCD".index(ANSWER)] == str(T.index(20))
''',
        },
        # ---------------------------------------------------------------- Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Bubble sort — passes and swaps",
            "text": ("Bubble sort (each pass scans left to right over the unsorted prefix, swapping adjacent "
                     "out-of-order pairs) is applied to A = [62, 18, 45, 7, 53, 29, 11]. Which of the following "
                     "statements is/are TRUE?"),
            "options": [
                "After 2 passes, A = [18, 7, 45, 29, 11, 53, 62]",
                "The first 2 passes perform 9 swaps in total",
                "After any 2 passes of bubble sort on any array, the two largest elements are in their final "
                "positions",
                "Sorting A completely requires 15 swaps",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "**Pass 1:** 62 bubbles to the end, swapping with 18, 45, 7, 53, 29, 11 (6 swaps) → "
                "[18, 45, 7, 53, 29, 11, 62].\n\n"
                "**Pass 2:** 18<45 ok; 45>7 swap; 45<53 ok; 53>29 swap; 53>11 swap (3 swaps) → "
                "[18, 7, 45, 29, 11, 53, 62].\n\n"
                "- (A) **True.**\n"
                "- (B) **True** — 6 + 3 = 9.\n"
                "- (C) **True** — pass k carries the k-th largest element to position n − k; this invariant "
                "holds for every input.\n"
                "- (D) **False** — bubble sort performs exactly one swap per inversion, and A has 14 "
                "inversions (62: 6, 18: 2, 45: 3, 7: 0, 53: 2, 29: 1, 11: 0), so 14 swaps.\n\n"
                "**Trap:** counting comparisons (6 + 5 + 4 + …) instead of swaps, or mis-tallying inversions."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Array after each pass",
                                   "row_labels": ["start", "pass 1", "pass 2"],
                                   "rows": [[62, 18, 45, 7, 53, 29, 11], [18, 45, 7, 53, 29, 11, 62],
                                            [18, 7, 45, 29, 11, 53, 62]],
                                   "highlight": [[1, 6], [2, 5], [2, 6]]}],
            "verify": '''
A = [62, 18, 45, 7, 53, 29, 11]; sw = 0
for p in range(2):
    for j in range(len(A) - 1 - p):
        if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]; sw += 1
B = [62, 18, 45, 7, 53, 29, 11]
inv = sum(B[i] > B[j] for i in range(7) for j in range(i + 1, 7))
import random
random.seed(1); okC = True
for _ in range(300):
    X = random.sample(range(100), 8); Y = X[:]
    for p in range(2):
        for j in range(7 - p):
            if Y[j] > Y[j + 1]: Y[j], Y[j + 1] = Y[j + 1], Y[j]
    okC &= Y[-2:] == sorted(X)[-2:]
r = {'A': A == [18, 7, 45, 29, 11, 53, 62], 'B': sw == 9, 'C': okC, 'D': inv == 15}
assert sorted(k for k in r if r[k]) == sorted(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q9
        {
            "type": "NAT", "marks": 1, "topic": "BFS — counting possible visiting orders",
            "text": ("BFS is run on the undirected graph below starting from P. When a vertex is dequeued, its "
                     "undiscovered neighbours may be enqueued in **any** order. The number of distinct orders "
                     "in which BFS can visit (dequeue) the vertices is ______."),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U", "V", "W"],
                          "edges": [["P", "Q"], ["P", "R"], ["Q", "S"], ["Q", "T"], ["Q", "U"],
                                    ["R", "U"], ["R", "V"], ["S", "W"], ["V", "W"]],
                          "pos": {"P": [3, 4], "Q": [1.5, 2.5], "R": [4.5, 2.5], "S": [0, 1],
                                  "T": [1.5, 1], "U": [3, 1], "V": [4.5, 1], "W": [2.25, -0.5]}}],
            "answer": "10",
            "solution": (
                "**Concept.** A BFS order is fixed once we choose, for every dequeued vertex, the order in which "
                "its *newly discovered* neighbours are enqueued. Branch on these choices.\n\n"
                "**Case 1: Q before R** (level 1 = Q, R).\n"
                "- Q discovers S, T, U → 3! = 6 orders. Then R discovers only V (U already seen).\n"
                "- Level 3: W is discovered by the first of S, V to be dequeued — S (it precedes V). One "
                "way.\n- Subtotal 6.\n\n"
                "**Case 2: R before Q.**\n"
                "- R discovers U, V → 2 orders; Q then discovers S, T → 2 orders.\n"
                "- W is discovered by V (V precedes S). One way.\n- Subtotal 4.\n\n"
                "Total = 6 + 4 = **10**.\n\n"
                "**Trap:** multiplying level sizes (2! × 4! × 1 = 48) ignores that a vertex discovered by one "
                "parent cannot appear among another parent's children — U's position depends on whether Q or "
                "R is dequeued first."
            ),
            "verify": '''
import itertools
E = ["PQ", "PR", "QS", "QT", "QU", "RU", "RV", "SW", "VW"]
G = {}
for a, b in E:
    G.setdefault(a, []).append(b); G.setdefault(b, []).append(a)
res = set()
def rec(order, queue, seen):
    if not queue: res.add("".join(order)); return
    u = queue[0]; new = [v for v in G[u] if v not in seen]
    for p in itertools.permutations(new):
        rec(order + list(p), queue[1:] + list(p), seen | set(new))
rec(['P'], ['P'], {'P'})
assert len(res) == int(ANSWER)
''',
        },
        # ---------------------------------------------------------------- Q10
        {
            "type": "NAT", "marks": 1, "topic": "Recursion — counting calls",
            "text": "How many times is the function `f` called (including the initial call) when `f(8)` is evaluated?",
            "code": '''def f(n):
    if n <= 2:
        return 1
    return f(n - 1) + f(n - 3)

print(f(8))''',
            "answer": "25",
            "solution": (
                "**Concept.** Let C(n) be the number of calls made when evaluating f(n). For n ≤ 2 there is just "
                "the one call; otherwise C(n) = 1 + C(n − 1) + C(n − 3).\n\n"
                "**Table.**\n"
                "- C(0) = C(1) = C(2) = 1 (note f(0) is reached from f(3)).\n"
                "- C(3) = 1 + C(2) + C(0) = 3\n"
                "- C(4) = 1 + C(3) + C(1) = 5\n"
                "- C(5) = 1 + C(4) + C(2) = 7\n"
                "- C(6) = 1 + C(5) + C(3) = 11\n"
                "- C(7) = 1 + C(6) + C(4) = 17\n"
                "- C(8) = 1 + C(7) + C(5) = **25**\n\n"
                "(The printed value f(8) = 13 is a different quantity — it counts leaves, not calls.)\n\n"
                "**Trap:** confusing the return value with the call count, or forgetting the '+1' for the "
                "current call. Memoisation would cut the calls to O(n)."
            ),
            "verify": '''
calls = [0]
def g(n):
    calls[0] += 1
    return 1 if n <= 2 else g(n - 1) + g(n - 3)
g(8)
assert calls[0] == int(ANSWER) and OUTPUT.strip() == "13"
''',
        },
    ],
}
