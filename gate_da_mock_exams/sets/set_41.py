# Set 41 — Full-Syllabus Mock — Paper 11

SET = {
    "number": 41,
    "title": "Full-Syllabus Mock — Paper 11",
    "difficulty": "GATE-level",
    "focus": "balanced paper across the whole Section 4 syllabus",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — identity versus equality",
            "text": "Consider the following Python program. What is printed?",
            "code": '''a = [1, 2]
b = a[:]
c = a
print(a == b, a is b, c is a, [a] * 2 == [b, c])''',
            "options": ["`True True True True`", "`True False True False`",
                        "`True False True True`", "`False False True True`"],
            "answer": "C",
            "solution": (
                "`==` compares **values** (element by element for lists); `is` compares **object "
                "identity**.\n\n"
                "- `a == b`: b is a slice copy with the same elements → True.\n"
                "- `a is b`: the slice created a new list object → False.\n"
                "- `c is a`: plain assignment binds another name to the same object → True.\n"
                "- `[a] * 2 == [b, c]`: the left side is `[a, a]`; list equality compares "
                "element-wise with `==`: a == b (True) and a == c (True) → True. It does not matter "
                "that the left list holds the same object twice.\n\n"
                "Output `True False True True` → (C).\n\n"
                "- (A) thinks a slice copy is the same object.\n"
                "- (B) thinks list equality requires identical element objects.\n"
                "- (D) thinks a copy is not equal to the original.\n\n"
                "**Tip:** use `is` only for identity checks such as `x is None`; never use it to "
                "compare values."
            ),
            "verify": "assert OUTPUT.strip() == 'True False True True' and ANSWER == 'C'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Python — dict comprehension with repeated keys",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''d = {x % 4: x for x in range(10)}
print(sum(d.values()))''',
            "answer": "30",
            "solution": (
                "A dict comprehension inserts key-value pairs in order; when a key repeats, the "
                "**later** value overwrites the earlier one (the key keeps its original position).\n\n"
                "For x = 0 … 9 the key is x % 4:\n\n"
                "- key 0: x = 0, 4, 8 → final value 8\n"
                "- key 1: x = 1, 5, 9 → final value 9\n"
                "- key 2: x = 2, 6 → final value 6\n"
                "- key 3: x = 3, 7 → final value 7\n\n"
                "d = {0: 8, 1: 9, 2: 6, 3: 7}, so sum of values = 8 + 9 + 6 + 7 = **30**.\n\n"
                "**Traps:**\n\n"
                "- Keeping the **first** value per key gives 0 + 1 + 2 + 3 = 6.\n"
                "- Summing all of range(10) (45) ignores that only 4 keys survive."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "MSQ", "marks": 1, "topic": "Stacks — infix to postfix conversion",
            "text": ("The infix expression `a + b * (c - d) / e ^ f ^ g` is converted to postfix with "
                     "the usual operator-stack algorithm. Precedence: `^` highest (right-associative), "
                     "then `*` and `/` (left-associative), then `+` and `-` (left-associative). Which "
                     "of the following statements is/are TRUE?"),
            "options": [
                "The postfix form is `a b c d - * e f g ^ ^ / +`",
                "The operator stack never holds more than 3 symbols (counting `(`)",
                "The prefix form is `+ a / * b - c d ^ e ^ f g`",
                "If `^` were left-associative, the postfix form would not change",
            ],
            "answer": ["A", "C"],
            "solution": (
                "Shunting-yard: operands go straight to the output; an incoming operator first pops "
                "operators of higher precedence (or equal precedence if it is left-associative); `(` "
                "is pushed and `)` pops back to it.\n\n"
                "- a → out. `+` → stack [+]. b → out.\n"
                "- `*` (higher than +) → [+, *]. `(` → [+, *, (]. c → out. `-` → [+, *, (, -]. d → out.\n"
                "- `)` pops `-` → out; stack [+, *].\n"
                "- `/`: equal to `*` and left-assoc → pop `*`; then push → [+, /].\n"
                "- e → out. `^` → [+, /, ^]. f → out.\n"
                "- second `^`: equal precedence but right-assoc → no pop → [+, /, ^, ^]. g → out.\n"
                "- End: pop ^, ^, /, +.\n\n"
                "Postfix: a b c d − * e f g ^ ^ / +.\n\n"
                "- (A) **TRUE.**\n"
                "- (B) The stack reaches 4 symbols twice ([+, *, (, −] and [+, /, ^, ^]). **FALSE.**\n"
                "- (C) The tree is + (a, / (* (b, − (c, d)), ^ (e, ^ (f, g)))); its pre-order is "
                "+ a / * b − c d ^ e ^ f g. **TRUE.**\n"
                "- (D) Left-associative `^` would pop the first `^` before pushing the second, "
                "giving … e f ^ g ^ …. **FALSE.**\n\n"
                "**Trap:** e ^ f ^ g means e^(f^g) — right associativity is what keeps both `^` on "
                "the stack."
            ),
            "verify": '''
P = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
def conv(expr, right=("^",)):
    out, st, mx = [], [], 0
    for t in expr.split():
        if t.isalpha(): out.append(t)
        elif t == "(": st.append(t)
        elif t == ")":
            while st[-1] != "(": out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != "(" and (P[st[-1]] > P[t] or (P[st[-1]] == P[t] and t not in right)):
                out.append(st.pop())
            st.append(t)
        mx = max(mx, len(st))
    while st: out.append(st.pop())
    return " ".join(out), mx
e = "a + b * ( c - d ) / e ^ f ^ g"
pf, mx = conv(e)
assert pf == "a b c d - * e f g ^ ^ / +" and mx == 4
assert conv(e, right=())[0] != pf
assert sorted(ANSWER) == ["A", "C"]
''',
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MCQ", "marks": 1, "topic": "Queues — circular array arithmetic",
            "text": ("A circular queue is stored in an array Q[0 … 9]. `front` is the index of the "
                     "first element and `rear` is the index of the next free slot; one slot is always "
                     "left unused so that a full queue can be told apart from an empty one. "
                     "If front = 7 and rear = 3, the number of elements in the queue is"),
            "diagrams": [{"type": "array", "values": ["x", "x", "x", "", "", "", "", "x", "x", "x"],
                          "pointers": {"rear": 3, "front": 7}, "label": "Q"}],
            "options": ["4", "5", "6", "7"],
            "answer": "C",
            "solution": (
                "With `rear` pointing at the next free slot, the occupied slots are front, front+1, "
                "…, rear−1 taken modulo the capacity n, so\n"
                "size = (rear − front + n) mod n.\n\n"
                "Here: (3 − 7 + 10) mod 10 = 6. The occupied slots are 7, 8, 9, 0, 1, 2 → **6** "
                "elements → (C).\n\n"
                "Option analysis:\n\n"
                "- (A) 4 = front − rear: the number of *free* slots (including the reserved one).\n"
                "- (B) 5 assumes rear points at the last element and subtracts the reserved slot.\n"
                "- (D) 7 counts slot 3 as occupied (rear − front + n + 1).\n\n"
                "The queue can hold at most n − 1 = 9 elements in this scheme; it is full when "
                "(rear + 1) mod n == front and empty when rear == front.\n\n"
                "**Trap:** forgetting the “+ n” and getting a negative size, or treating `rear` as "
                "the last occupied index."
            ),
            "verify": '''
n, f, r = 10, 7, 3
occ = []
i = f
while i != r: occ.append(i); i = (i + 1) % n
assert len(occ) == (r - f + n) % n == 6 and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "NAT", "marks": 1, "topic": "Linked lists — Floyd's cycle detection",
            "text": ("A singly linked list has nodes 1 → 2 → … → 9 and the `next` pointer of node 9 "
                     "points back to node 4 (see figure). Floyd's algorithm is run from the head: in "
                     "each step `slow` moves one node and `fast` moves two nodes, and the step counter "
                     "is incremented; the loop stops as soon as `slow` and `fast` are on the same "
                     "node. The number of steps executed is ______."),
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6, 7, 8, 9], "head": "head",
                          "caption": "Node 9's next pointer goes back to node 4 (not drawn)"}],
            "code": '''slow = fast = head
steps = 0
while True:
    slow = slow.nxt
    fast = fast.nxt.nxt
    steps += 1
    if slow is fast:
        break''',
            "run_code": False,
            "answer": "6",
            "solution": (
                "The tail (1, 2, 3) has length μ = 3 and the cycle 4 → 5 → … → 9 → 4 has length λ = 6. "
                "Track positions after each step (slow moves 1, fast moves 2):\n\n"
                "- Step 1: slow 2, fast 3\n"
                "- Step 2: slow 3, fast 5\n"
                "- Step 3: slow 4, fast 7\n"
                "- Step 4: slow 5, fast 9\n"
                "- Step 5: slow 6, fast 5 (9 → 4 → 5)\n"
                "- Step 6: slow 7, fast 7 → **meet**\n\n"
                "Steps = **6**.\n\n"
                "General fact: they meet after t steps where t is the smallest multiple of λ with "
                "t ≥ μ; here μ = 3, λ = 6 → t = 6. Once slow enters the cycle, the gap closes by one "
                "node per step, so the meeting happens within λ steps of slow's entry.\n\n"
                "To find the cycle's start, reset one pointer to the head and advance both one step at "
                "a time: they meet at node 4 after μ = 3 steps.\n\n"
                "**Trap:** stopping when fast first *passes* slow, or counting fast's moves (12) "
                "instead of loop iterations."
            ),
            "verify": '''
class N:
    def __init__(s, v): s.v = v; s.nxt = None
nodes = [N(i) for i in range(1, 10)]
for x, y in zip(nodes, nodes[1:]): x.nxt = y
nodes[-1].nxt = nodes[3]
head = nodes[0]
slow = fast = head; steps = 0
while True:
    slow = slow.nxt; fast = fast.nxt.nxt; steps += 1
    if slow is fast: break
assert steps == int(ANSWER) and slow.v == 7
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Expression trees — prefix form",
            "text": "The prefix (Polish) form of the expression tree shown below is",
            "diagrams": [{"type": "bintree",
                          "tree": ["−", ["*", ["+", ["a"], ["b"]], ["c"]],
                                   ["/", ["d"], ["^", ["e"], ["f"]]]],
                          "caption": "Expression tree"}],
            "options": [
                "− * + a b c / d ^ e f",
                "a b + c * d e f ^ / −",
                "− + * a b c / ^ d e f",
                "− * a + b c / d ^ e f",
            ],
            "answer": "A",
            "solution": (
                "Prefix form = **pre-order** traversal of the expression tree (operator, then left "
                "operand, then right operand). Post-order gives the postfix form; in-order (with "
                "parentheses) gives the infix form.\n\n"
                "- Root `−`.\n"
                "- Left subtree pre-order: `*`, then `+ a b`, then `c` → * + a b c.\n"
                "- Right subtree pre-order: `/`, `d`, then `^ e f` → / d ^ e f.\n\n"
                "Prefix: − * + a b c / d ^ e f → (A). Infix: (a + b) * c − d / e^{f}.\n\n"
                "- (B) is the **postfix** (post-order) form.\n"
                "- (C) swaps the order of `*` and `+` (as if + were the parent of *) and misplaces `^`.\n"
                "- (D) places `+` under the right operand of `*` — that is the tree for a * (b + c).\n\n"
                "**Tip:** a valid prefix expression scanned right to left with a stack evaluates "
                "correctly; check the number of operands: each binary operator needs exactly two."
            ),
            "verify": '''
T = ["-", ["*", ["+", ["a"], ["b"]], ["c"]], ["/", ["d"], ["^", ["e"], ["f"]]]]
def pre(t): return [t[0]] + sum((pre(c) for c in t[1:]), [])
def post(t): return sum((post(c) for c in t[1:]), []) + [t[0]]
assert " ".join(pre(T)) == "- * + a b c / d ^ e f" and ANSWER == "A"
assert " ".join(post(T)) == "a b + c * d e f ^ / -"
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "NAT", "marks": 1, "topic": "Hashing — load factor and chaining cost",
            "text": ("3000 keys are stored in a hash table with 1024 slots using separate chaining. "
                     "Under simple uniform hashing, the expected number of keys examined during an "
                     "**unsuccessful** search (not counting the cost of computing the hash) is ______ "
                     "(rounded off to two decimal places)."),
            "answer": ["2.92", "2.94"],
            "solution": (
                "In an unsuccessful search the whole chain of the probed slot is scanned. Under simple "
                "uniform hashing each of the n keys lies in that chain with probability 1/m, so by "
                "linearity of expectation the expected chain length is n/m = α (the **load factor**).\n\n"
                "- α = 3000 / 1024 = 2.9296875 ≈ **2.93**.\n\n"
                "For comparison, a *successful* search examines on average 1 + (n − 1)/(2m) "
                "= 1 + 2999/2048 ≈ 2.46 keys: the target itself plus half of the other keys that "
                "were inserted before it in the same chain (for tail insertion).\n\n"
                "With 1 + α ≈ 3.93 one would be counting the slot access as well — the question "
                "explicitly excludes it.\n\n"
                "**Trap:** applying the open-addressing formula 1/(1 − α), which is meaningless "
                "here because α > 1 — chaining allows load factors above 1."
            ),
            "verify": '''
a = 3000 / 1024
assert float(ANSWER[0]) <= round(a, 2) <= float(ANSWER[1])
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MSQ", "marks": 1, "topic": "Binary search — a buggy variant",
            "text": ("Consider the following (buggy) binary search with a = [3, 6, 9, 12, 15]. "
                     "Which of the following statements is/are TRUE?"),
            "code": '''def find(a, x):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid
        else:
            hi = mid
    return lo''',
            "options": [
                "`find(a, 3)` terminates and returns 0",
                "`find(a, 6)` terminates and returns 1",
                "`find(a, 1)` terminates and returns 0",
                "`find(a, 100)` terminates and returns 4",
            ],
            "answer": ["A", "C"],
            "solution": (
                "The bug is `lo = mid` (instead of `mid + 1`). When hi = lo + 1, mid = lo; if "
                "a[lo] < x the assignment `lo = mid` changes nothing and the loop never ends.\n\n"
                "Once `lo` moves at all, a[lo] < x holds, so eventually the interval shrinks to "
                "[lo, lo + 1] with a[lo] < x → infinite loop. The only way to terminate is for "
                "`lo` never to move *and* a[0] ≥ x, so that `hi` keeps shrinking down to 0.\n\n"
                "- (A) x = 3: mids 2, 1, 0 all have a[mid] ≥ 3 → hi = 2, 1, 0 → returns 0. **TRUE.**\n"
                "- (B) x = 6: mid 2 (9 ≥ 6) → hi 2; mid 1 (6 ≥ 6) → hi 1; mid 0 (3 < 6) → lo = 0 "
                "again with hi = 1 → loops forever. **FALSE.**\n"
                "- (C) x = 1: like (A), returns 0. **TRUE.**\n"
                "- (D) x = 100: lo moves to 2, then 3; with lo = 3, hi = 4, mid = 3 → stuck. **FALSE.**\n\n"
                "**Tip:** with `mid = (lo + hi) // 2` (rounding down) the update that keeps mid must be "
                "`hi = mid`; the other must be `lo = mid + 1`."
            ),
            "verify": '''
def term(a, x, cap=100):
    lo, hi = 0, len(a) - 1; c = 0
    while lo < hi:
        c += 1
        if c > cap: return None
        mid = (lo + hi) // 2
        if a[mid] < x: lo = mid
        else: hi = mid
    return lo
a = [3, 6, 9, 12, 15]
res = [term(a, 3) == 0, term(a, 6) == 1, term(a, 1) == 0, term(a, 100) == 4]
assert [c for c, v in zip("ABCD", res) if v] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Selection sort — counting index updates",
            "text": ("Selection sort is run on A = [7, 3, 9, 1, 6, 2]. In pass i, it sets `m = i` and "
                     "then, for j = i+1 … n−1, executes `m = j` whenever A[j] < A[m]; finally it swaps "
                     "A[i] and A[m]. Over the whole sort, how many times is the statement `m = j` "
                     "executed?"),
            "options": ["4", "7", "9", "15"],
            "answer": "B",
            "solution": (
                "The number of comparisons is fixed (n(n−1)/2 = 15), but the number of updates of `m` "
                "depends on how often a new running minimum appears in the scanned suffix.\n\n"
                "- Pass 0, scan 3, 9, 1, 6, 2 from 7: new minima 3, 1 → 2 updates; swap → "
                "[1, 3, 9, 7, 6, 2].\n"
                "- Pass 1, scan 9, 7, 6, 2 from 3: new minimum 2 → 1 update; → [1, 2, 9, 7, 6, 3].\n"
                "- Pass 2, scan 7, 6, 3 from 9: 7, 6, 3 are each new minima → 3 updates; → "
                "[1, 2, 3, 7, 6, 9].\n"
                "- Pass 3, scan 6, 9 from 7: 6 → 1 update; → [1, 2, 3, 6, 7, 9].\n"
                "- Pass 4, scan 9 from 7: none.\n\n"
                "Total = 2 + 1 + 3 + 1 + 0 = **7** → (B).\n\n"
                "- (A) 4 is the number of swaps that actually move elements.\n"
                "- (C) 9 is not obtainable from any natural count here.\n"
                "- (D) 15 is the number of comparisons.\n\n"
                "**Trap:** counting updates on the *original* array instead of the array as it is "
                "after the previous swaps (pass 2 sees 9, 7, 6, 3 only because of the earlier swaps)."
            ),
            "verify": '''
A = [7, 3, 9, 1, 6, 2]; up = 0
for i in range(len(A) - 1):
    m = i
    for j in range(i + 1, len(A)):
        if A[j] < A[m]: m = j; up += 1
    A[i], A[m] = A[m], A[i]
assert up == 7 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MCQ", "marks": 1, "topic": "Graph theory — edges in a disconnected graph",
            "text": ("The maximum number of edges in a **disconnected** simple undirected graph on "
                     "10 vertices is"),
            "options": ["45", "40", "36", "35"],
            "answer": "C",
            "solution": (
                "A disconnected graph splits its vertices into at least two parts with no edges between "
                "them. If one part has k vertices and the other 10 − k, the maximum edge count is "
                "C(k, 2) + C(10 − k, 2), which is largest when the split is as **unbalanced** as "
                "possible: k = 1.\n\n"
                "- k = 1: C(1, 2) + C(9, 2) = 0 + 36 = 36.\n"
                "- k = 2: 1 + 28 = 29.\n"
                "- k = 5: 10 + 10 = 20.\n\n"
                "So the answer is **36**: K₉ plus one isolated vertex → (C). Adding any further edge "
                "would have to touch the isolated vertex and connect the graph.\n\n"
                "- (A) 45 = C(10, 2) is the complete graph, which is connected.\n"
                "- (B) 40 and (D) 35 do not correspond to an optimal split.\n\n"
                "Corollary: any simple graph on n vertices with more than C(n − 1, 2) edges is "
                "connected.\n\n"
                "**Trap:** guessing that a balanced split maximises edges — it minimises them."
            ),
            "verify": '''
from math import comb
assert max(comb(k, 2) + comb(10 - k, 2) for k in range(1, 10)) == 36 and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Python — closures with nonlocal state",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def make():
    c = 0
    def inc(k=1):
        nonlocal c
        c += k
        return c
    return inc

f = make()
g = make()
f(); f(3); g(10)
h = f
print(f() + g() + h(2))''',
            "answer": "23",
            "solution": (
                "Each call of `make()` creates a **new** local variable `c` and a new closure that "
                "captures it; `nonlocal c` lets `inc` rebind that captured variable. `h = f` creates no "
                "new closure — `h` and `f` are the same function object sharing one `c`.\n\n"
                "- f(): f's c = 1.\n"
                "- f(3): f's c = 4.\n"
                "- g(10): g's c = 10 (independent of f).\n"
                "- In the print, operands are evaluated left to right: f() → f's c = 5, value 5; "
                "g() → g's c = 11, value 11; h(2) → same counter as f: 5 + 2 = 7, value 7.\n\n"
                "Sum = 5 + 11 + 7 = **23**.\n\n"
                "Common wrong answers:\n\n"
                "- 18 — treating `h` as a fresh counter (h(2) = 2).\n"
                "- 29 — treating f and g as sharing one counter.\n"
                "- An UnboundLocalError would occur only without `nonlocal`, because `c += k` makes "
                "`c` local to `inc`.\n\n"
                "**Tip:** default arguments (`k=1`) are evaluated once at definition time, but that "
                "is harmless here because 1 is immutable."
            ),
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "MCQ", "marks": 2, "topic": "Python — iterators and zip",
            "text": "Consider the following Python program. What is printed?",
            "code": '''a = [1, 2, 3, 4, 5, 6, 7]
it = iter(a)
p = list(zip(it, it))
q = list(it)
r = dict(zip("abc", range(5)))
print(p, q, r)''',
            "options": [
                "`[(1, 2), (3, 4), (5, 6)] [7] {'a': 0, 'b': 1, 'c': 2}`",
                "`[(1, 2), (3, 4), (5, 6)] [] {'a': 0, 'b': 1, 'c': 2}`",
                "`[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)] [] {'a': 0, 'b': 1, 'c': 2}`",
                "`[(1, 2), (3, 4), (5, 6), (7, None)] [] {'a': 0, 'b': 1, 'c': 2, 3: 4}`",
            ],
            "answer": "B",
            "solution": (
                "`zip(it, it)` pulls alternately from the **same** iterator, so it pairs consecutive "
                "elements. `zip` stops as soon as **any** input is exhausted — but it only discovers "
                "that by calling `next` on it.\n\n"
                "- Pairs (1, 2), (3, 4), (5, 6) are produced.\n"
                "- For the 4th pair, zip calls next(it) for the first slot and gets **7** (consumed!), "
                "then calls next(it) for the second slot → StopIteration → zip stops and the 7 is "
                "silently discarded.\n"
                "- So `q = list(it)` is `[]`.\n"
                "- `zip(\"abc\", range(5))` stops at the shorter input → {'a': 0, 'b': 1, 'c': 2}.\n\n"
                "Output: `[(1, 2), (3, 4), (5, 6)] [] {'a': 0, 'b': 1, 'c': 2}` → (B).\n\n"
                "Option analysis:\n\n"
                "- (A) assumes the leftover 7 is still available — it was consumed by zip.\n"
                "- (C) would be zip(a, a) on the *list*, which creates two independent iterators.\n"
                "- (D) behaves like itertools.zip_longest and invents a key 3.\n\n"
                "**Trap:** iterator exhaustion inside zip silently drops an element; "
                "`itertools.zip_longest` or slicing (a[0::2], a[1::2]) avoids it."
            ),
            "verify": "assert OUTPUT.strip() == \"[(1, 2), (3, 4), (5, 6)] [] {'a': 0, 'b': 1, 'c': 2}\" and ANSWER == 'B'",
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MSQ", "marks": 2, "topic": "Heapsort — build-heap and extraction steps",
            "text": ("Heapsort (ascending) is applied to A = [21, 35, 12, 40, 18, 27, 9, 33]. "
                     "It first builds a max-heap bottom-up (sift-down at i = 3, 2, 1, 0) and then "
                     "repeatedly swaps A[0] with the last element of the heap, shrinks the heap by "
                     "one and sifts down the new root. Which of the following statements is/are TRUE?"),
            "diagrams": [{"type": "heap", "values": [21, 35, 12, 40, 18, 27, 9, 33],
                          "caption": "A as a complete binary tree before build-heap"}],
            "options": [
                "After build-heap, A = [40, 35, 27, 33, 18, 12, 9, 21]",
                "After two extraction steps, A = [33, 21, 27, 9, 18, 12, 35, 40]",
                "Build-heap performs exactly 4 parent–child swaps",
                "After the two extraction steps, A[0 … 5] is a valid max-heap and A[6 … 7] holds the "
                "two largest keys in increasing order",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Build-heap (sift-down swaps with the larger child):\n\n"
                "- i = 3 (40): child 33 is smaller → no swap.\n"
                "- i = 2 (12): children 27, 9 → swap with 27 (1).\n"
                "- i = 1 (35): children 40, 18 → swap with 40 (2); at index 3, 35 vs child 33 → stop.\n"
                "- i = 0 (21): children 40, 27 → swap with 40 (3); at index 1, children 35, 18 → swap "
                "with 35 (4); at index 3, child 33 > 21 → swap (5).\n"
                "- Result [40, 35, 27, 33, 18, 12, 9, 21].\n\n"
                "Extraction 1: swap 40 ↔ 21 → [21, 35, 27, 33, 18, 12, 9 | 40]; sift 21: ↔35, ↔33 → "
                "[35, 33, 27, 21, 18, 12, 9 | 40].\n"
                "Extraction 2: swap 35 ↔ 9 → [9, 33, 27, 21, 18, 12 | 35, 40]; sift 9: ↔33, ↔21 → "
                "[33, 21, 27, 9, 18, 12 | 35, 40].\n\n"
                "- (A) **TRUE.**\n"
                "- (B) **TRUE.**\n"
                "- (C) Build-heap made **5** swaps (the root's 21 sank three levels). **FALSE.**\n"
                "- (D) The heap part [33, 21, 27, 9, 18, 12] satisfies the heap property, and the sorted "
                "tail is 35, 40. **TRUE.**\n\n"
                "**Trap:** stopping sift-down after one swap; 21 must keep sinking while a child is larger."
            ),
            "solution_diagrams": [{"type": "heap", "values": [40, 35, 27, 33, 18, 12, 9, 21],
                                   "caption": "Max-heap after build-heap"}],
            "verify": '''
sw = [0]
def sift(a, i, n):
    while True:
        l, r, m = 2 * i + 1, 2 * i + 2, i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; sw[0] += 1; i = m
h = [21, 35, 12, 40, 18, 27, 9, 33]
for i in range(3, -1, -1): sift(h, i, 8)
assert h == [40, 35, 27, 33, 18, 12, 9, 21] and sw[0] == 5
n = 8
for _ in range(2):
    h[0], h[n - 1] = h[n - 1], h[0]; n -= 1; sift(h, 0, n)
assert h == [33, 21, 27, 9, 18, 12, 35, 40]
assert all(h[(i - 1) // 2] >= h[i] for i in range(1, 6)) and h[6:] == [35, 40]
assert sorted(ANSWER) == ["A", "B", "D"]
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "NAT", "marks": 2, "topic": "Merge sort — comparisons on structured input",
            "text": ("Top-down merge sort (split into halves of equal size; the merge stops comparing "
                     "as soon as one run is exhausted) sorts the 16-element array\n"
                     "[2, 4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9, 11, 13, 15].\n"
                     "The total number of element comparisons is ______."),
            "answer": "39",
            "solution": (
                "Merging two runs where every element of one run is smaller than every element of the "
                "other costs only min(p, q) comparisons; a perfectly interleaved merge costs p + q − 1.\n\n"
                "Left half [2, 4, …, 16] is already sorted. At every merge inside it, the left run "
                "is entirely smaller than the right run, so each merge of two runs of length s costs s:\n\n"
                "- 4 merges of 1+1 → 4 × 1 = 4\n"
                "- 2 merges of 2+2 → 2 × 2 = 4\n"
                "- 1 merge of 4+4 → 4\n"
                "- Left half total = 12.\n\n"
                "The right half [1, 3, …, 15] is also sorted → another 12.\n\n"
                "Final merge of [2, 4, …, 16] with [1, 3, …, 15]: the outputs alternate 1, 2, 3, …; "
                "the right run is exhausted when 15 is output, i.e. after 15 elements, each needing "
                "one comparison, and 16 is copied → 15 comparisons.\n\n"
                "Total = 12 + 12 + 15 = **39**.\n\n"
                "For reference: best case for n = 16 is (n/2) log₂ n = 32 and worst case is "
                "n log₂ n − n + 1 = 49.\n\n"
                "**Trap:** assuming the final merge is also a best case (8) because both halves were "
                "sorted — interleaved values force the maximum p + q − 1."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Comparisons per merge level",
                                   "row_labels": ["left half", "right half", "final"],
                                   "col_labels": ["1+1", "2+2", "4+4", "8+8"],
                                   "rows": [[4, 4, 4, "–"], [4, 4, 4, "–"], ["–", "–", "–", 15]]}],
            "verify": '''
c = [0]
def ms(a):
    if len(a) <= 1: return a
    m = len(a) // 2; L = ms(a[:m]); R = ms(a[m:]); i = j = 0; o = []
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: o.append(L[i]); i += 1
        else: o.append(R[j]); j += 1
    return o + L[i:] + R[j:]
ms([2, 4, 6, 8, 10, 12, 14, 16, 1, 3, 5, 7, 9, 11, 13, 15])
assert c[0] == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "MCQ", "marks": 2, "topic": "Recurrences — change of variable",
            "text": ("Let T(n) = 2T(√n) + log₂ n for n > 2, with T(2) = 1. Which of the following is a "
                     "tight bound for T(n)?"),
            "options": ["Θ(log n)", "Θ(log n · log log n)", "Θ(√n)", "Θ(log² n)"],
            "answer": "B",
            "solution": (
                "Substitute m = log₂ n, i.e. n = 2^{m}, so √n = 2^{m/2}. Define S(m) = T(2^{m}). Then\n"
                "S(m) = 2S(m/2) + m.\n\n"
                "This is the merge-sort recurrence: by the master theorem (a = 2, b = 2, f(m) = m = "
                "Θ(m^{log₂ 2})) S(m) = Θ(m log m).\n\n"
                "Translating back: T(n) = S(log n) = **Θ(log n · log log n)** → (B).\n\n"
                "Recursion-tree view: the depth is log log n (taking square roots repeatedly until "
                "the argument is constant); at depth i there are 2^{i} subproblems, each of size "
                "n^{1/2^{i}}, so each costs (log n)/2^{i}; every level sums to log n.\n\n"
                "Option analysis:\n\n"
                "- (A) would hold for T(n) = T(√n) + log n (one recursive call: geometric sum).\n"
                "- (C) confuses √n in the argument with the cost.\n"
                "- (D) would need log n levels, but there are only log log n.\n\n"
                "**Tip:** recurrences on √n become ordinary divide-and-conquer recurrences after the "
                "substitution m = log n."
            ),
            "verify": '''
import math
from functools import lru_cache
@lru_cache(None)
def S(m): return 1 if m <= 1 else 2 * S(m // 2) + m
r = [S(2 ** k) / (2 ** k * k) for k in (10, 20)]
assert abs(r[0] / r[1] - 1) < 0.1
assert S(2 ** 20) / (2 ** 20) > 15 and ANSWER == "B"
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "NAT", "marks": 2, "topic": "BFS — distances in a rule-defined graph",
            "text": ("Graph G has vertex set {0, 1, …, 11}, and vertices i and j are adjacent iff "
                     "|i − j| ∈ {3, 5}. BFS is run from vertex 0. The sum of the BFS distances "
                     "(number of edges) from 0 to all 12 vertices is ______."),
            "answer": "26",
            "solution": (
                "Neighbours of i are i ± 3 and i ± 5 (within 0 … 11). BFS level by level:\n\n"
                "- Level 0: {0}.\n"
                "- Level 1: neighbours of 0 → {3, 5}.\n"
                "- Level 2: from 3 → 6, 8; from 5 → 2, 8, 10 → {2, 6, 8, 10}.\n"
                "- Level 3: from 2 → 7; from 6 → 1, 9, 11; from 8 → 11; from 10 → 7 → {1, 7, 9, 11}.\n"
                "- Level 4: from 1 → 4; (4 is not adjacent to anything earlier: 4 ± 3 = 1, 7 and "
                "4 ± 5 = 9 are all level 3) → {4}.\n\n"
                "All 12 vertices are reached (G is connected). "
                "Sum = 0·1 + 1·2 + 2·4 + 3·4 + 4·1 = 0 + 2 + 8 + 12 + 4 = **26**.\n\n"
                "Observation: every edge changes the parity of the vertex by 3 or 5 (both odd), so G is "
                "**bipartite** (even vs odd vertices) — consistent with even vertices appearing only on "
                "even levels.\n\n"
                "**Trap:** stopping at level 3 and missing vertex 4, or treating 0 + 5 + 3 = 8 as two "
                "distinct routes (BFS counts each vertex once)."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "BFS distance from 0",
                                   "col_labels": [str(i) for i in range(12)],
                                   "row_labels": ["dist"],
                                   "rows": [[0, 3, 2, 1, 4, 1, 2, 3, 2, 3, 2, 3]]}],
            "verify": '''
from collections import deque
G = {i: [j for j in range(12) if abs(i - j) in (3, 5)] for i in range(12)}
d = {0: 0}; q = deque([0])
while q:
    u = q.popleft()
    for v in G[u]:
        if v not in d: d[v] = d[u] + 1; q.append(v)
assert len(d) == 12 and sum(d.values()) == int(ANSWER)
assert [d[i] for i in range(12)] == [0, 3, 2, 1, 4, 1, 2, 3, 2, 3, 2, 3]
''',
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "MCQ", "marks": 2, "topic": "Dijkstra — counting distance updates",
            "text": ("Dijkstra's algorithm is run from S on the weighted directed graph below. "
                     "Initially d[S] = 0 and all other d values are ∞; an *update* of d[T] is an "
                     "assignment that makes d[T] **strictly smaller** (the first assignment from ∞ "
                     "counts). How many times is d[T] updated?"),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "T"],
                          "edges": [["S", "A", 1], ["S", "B", 4], ["S", "T", 15], ["A", "B", 2],
                                    ["A", "C", 6], ["B", "C", 3], ["B", "T", 10], ["C", "T", 2],
                                    ["A", "T", 12]],
                          "pos": {"S": [0, 3], "A": [1.5, 1.5], "B": [1.5, -0.5], "C": [4, 0.3],
                                  "T": [6, 3]}}],
            "options": ["2", "4", "3", "5"],
            "answer": "C",
            "solution": (
                "Dijkstra relaxes the out-edges of each vertex when it is extracted; d[T] changes only "
                "when a strictly shorter route is found.\n\n"
                "- Extract S (0): d[A] = 1, d[B] = 4, d[T] = 15 → **update 1**.\n"
                "- Extract A (1): d[B] = min(4, 3) = 3, d[C] = 7, d[T] = min(15, 1 + 12 = 13) → **update 2**.\n"
                "- Extract B (3): d[C] = min(7, 6) = 6; d[T]: 3 + 10 = 13 is **not** smaller than 13 → "
                "no update.\n"
                "- Extract C (6): d[T] = min(13, 6 + 2 = 8) → **update 3**.\n"
                "- Extract T (8).\n\n"
                "d[T] is updated **3** times (15 → 13 → 8) → (C). Final shortest path S → A → B → C → T "
                "with cost 1 + 2 + 3 + 2 = 8.\n\n"
                "Option analysis:\n\n"
                "- (A) 2 forgets the initial assignment from ∞.\n"
                "- (B) 4 counts the tie 13 = 13 at B as an update.\n"
                "- (D) 5 counts one update per incoming edge of T, plus one.\n\n"
                "**Trap:** with `<` in the relaxation test, equal-cost alternatives never trigger an "
                "update."
            ),
            "verify": '''
import heapq
E = [("S","A",1),("S","B",4),("S","T",15),("A","B",2),("A","C",6),("B","C",3),
     ("B","T",10),("C","T",2),("A","T",12)]
G = {}
for u, v, w in E: G.setdefault(u, []).append((v, w))
d = {v: float("inf") for v in "SABCT"}; d["S"] = 0; pq = [(0, "S")]; done = set(); up = 0
while pq:
    du, u = heapq.heappop(pq)
    if u in done: continue
    done.add(u)
    for v, w in G.get(u, []):
        if du + w < d[v]:
            d[v] = du + w; heapq.heappush(pq, (d[v], v)); up += (v == "T")
assert up == 3 and d["T"] == 8 and ANSWER == "C"
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MSQ", "marks": 2, "topic": "Hashing — deletion with tombstones",
            "text": ("A table with 10 slots uses h(k) = k mod 10 and linear probing. The keys 31, 41, 51, "
                     "22, 61 are inserted in that order, and then 41 is deleted by marking its slot "
                     "DELETED (a tombstone). Searches skip over DELETED slots and stop at an EMPTY "
                     "slot; an insertion places the key in the first EMPTY **or** DELETED slot on its "
                     "probe sequence. Which of the following statements is/are TRUE?"),
            "options": [
                "A search for 61 now examines exactly 5 slots",
                "If 41's slot had been made EMPTY instead of DELETED, a search for 51 would wrongly report "
                "that 51 is absent",
                "Inserting 71 now stores it in slot 2",
                "A search for 22 now examines exactly 2 slots",
            ],
            "answer": ["A", "B", "C"],
            "solution": (
                "Insertions: 31 → 1; 41 → 1 taken → 2; 51 → 1, 2 taken → 3; 22 → 2, 3 taken → 4; "
                "61 → 1, 2, 3, 4 taken → 5. Then slot 2 (41) becomes DELETED.\n\n"
                "Table: 1: 31, 2: DEL, 3: 51, 4: 22, 5: 61, rest EMPTY.\n\n"
                "- (A) Search 61: slots 1 (31), 2 (DEL, skip), 3 (51), 4 (22), 5 (61, found) → 5 slots. "
                "**TRUE.**\n"
                "- (B) Search 51 starts at slot 1 (31) and then reaches slot 2; if it were EMPTY, "
                "the search would stop and report “absent” although 51 sits in slot 3. This is exactly "
                "why tombstones are needed. **TRUE.**\n"
                "- (C) Insert 71: slot 1 occupied, slot 2 DELETED → stored in slot 2 (reusing the "
                "tombstone). **TRUE.**\n"
                "- (D) Search 22: slots 2 (DEL), 3 (51), 4 (22) → 3 slots, not 2. **FALSE.**\n\n"
                "**Trap:** in (D), forgetting that a tombstone still costs a probe. Tombstones keep "
                "searches correct but make them longer — tables with many deletions need periodic "
                "rehashing."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 10,
                                   "slots": {1: 31, 2: "DEL", 3: 51, 4: 22, 5: 61},
                                   "caption": "Table after deleting 41"}],
            "verify": '''
EMPTY, DEL = None, "DEL"
T = [EMPTY] * 10
def ins(k):
    i = k % 10
    while T[i] not in (EMPTY, DEL): i = (i + 1) % 10
    T[i] = k
def search(k, tab):
    i, c = k % 10, 0
    while True:
        c += 1
        if tab[i] is EMPTY: return None, c
        if tab[i] == k: return i, c
        i = (i + 1) % 10
for k in [31, 41, 51, 22, 61]: ins(k)
T[T.index(41)] = DEL
A = search(61, T)[1] == 5
U = T[:]; U[2] = EMPTY
B = search(51, U)[0] is None
D = search(22, T)[1] == 2
ins(71); C = T[2] == 71
assert [c for c, v in zip("ABCD", [A, B, C, D]) if v] == sorted(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "NAT", "marks": 2, "topic": "Stacks — counting output sequences",
            "text": ("The integers 1, 2, 3, 4, 5 are pushed onto an initially empty stack in this "
                     "order, with pops interleaved arbitrarily; each popped value is output, and all "
                     "five values are eventually output. The number of possible output sequences "
                     "whose **first** element is 3 is ______."),
            "answer": "9",
            "solution": (
                "For 3 to be output first, the operations must start push 1, push 2, push 3, pop. At "
                "that moment the stack holds 1, 2 (2 on top) and 4, 5 are still to be pushed.\n\n"
                "Constraint: 2 must be output before 1. The values 4 and 5 can be pushed at any time; "
                "count by when 2 and 1 are popped relative to 4 and 5:\n\n"
                "- 2 1 then 4, 5: 2 1 4 5, 2 1 5 4 → 2\n"
                "- 2 first, then 1 only after 4 and/or 5 has been output: 2 4 1 5, 2 4 5 1, 2 5 4 1 → 3\n"
                "- 4 first: 4 2 1 5, 4 2 5 1, 4 5 2 1 → 3\n"
                "- 5 first (4 must be on the stack below it): 5 4 2 1 → 1\n\n"
                "Total = 2 + 3 + 3 + 1 = **9**.\n\n"
                "Check of an excluded case: 2 5 1 4 is impossible — after 5 is popped, 4 is on top "
                "of 1, so 1 cannot precede 4.\n\n"
                "Cross-check: summing such counts over all possible first elements gives the total "
                "number of stack permutations of 5 elements, the Catalan number C₅ = 42 "
                "(first element 1: 14, 2: 14, 3: 9, 4: 4, 5: 1).\n\n"
                "**Trap:** counting 4!/2 = 12 by only enforcing “2 before 1” — the order of 4 and 5 "
                "relative to 1 and 2 is also constrained."
            ),
            "verify": '''
import itertools
def ok(seq):
    st, nx = [], 1
    for x in seq:
        while nx <= x: st.append(nx); nx += 1
        if st[-1] != x: return False
        st.pop()
    return True
good = [p for p in itertools.permutations(range(1, 6)) if ok(p)]
first3 = sorted(p[1:] for p in good if p[0] == 3)
assert len(good) == 42 and len(first3) == int(ANSWER)
assert first3 == sorted([(2,1,4,5),(2,1,5,4),(2,4,1,5),(2,4,5,1),(2,5,4,1),
                         (4,2,1,5),(4,2,5,1),(4,5,2,1),(5,4,2,1)])
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Linked lists — moving the tail to the front",
            "text": ("Consider the following Python function on a singly linked list (nodes have "
                     "fields `v` and `nxt`). Which of the following statements is/are TRUE?"),
            "code": '''def f(h, k):
    for _ in range(k):
        prev, cur = None, h
        while cur.nxt:
            prev, cur = cur, cur.nxt
        prev.nxt = None
        cur.nxt = h
        h = cur
    return h''',
            "diagrams": [{"type": "linkedlist", "values": [1, 2, 3, 4, 5, 6], "head": "h"}],
            "options": [
                "For the list shown, `f(h, 2)` returns the list 5 → 6 → 1 → 2 → 3 → 4",
                "For the list shown, `f(h, 2)` executes the statement `prev, cur = cur, cur.nxt` "
                "exactly 12 times",
                "For the list shown, `f(h, 8)` returns the list 3 → 4 → 5 → 6 → 1 → 2",
                "For a list with a single node, `f(h, 1)` raises an AttributeError",
            ],
            "answer": ["A", "D"],
            "solution": (
                "Each iteration walks to the last node (keeping its predecessor), detaches it and "
                "makes it the new head: one **right rotation** by one position. k iterations rotate "
                "right by k.\n\n"
                "- (A) Two right rotations of 1…6: 6 1 2 3 4 5 → 5 6 1 2 3 4. **TRUE.**\n"
                "- (B) In each iteration the inner loop advances from the head to the last node: "
                "n − 1 = 5 steps. Two iterations → 10, not 12. **FALSE.**\n"
                "- (C) 8 right rotations of a 6-node list = 8 mod 6 = 2 rotations → 5 6 1 2 3 4. "
                "The stated list (3 4 5 6 1 2) is the result of rotating **left** by 2. **FALSE.**\n"
                "- (D) With one node, the while-loop body never runs, so `prev` stays None and "
                "`prev.nxt = None` raises AttributeError ('NoneType' object has no attribute "
                "'nxt'). **TRUE.**\n\n"
                "Cost: Θ(nk) overall. A better approach computes k mod n, finds the new tail in one "
                "pass and re-links in O(n).\n\n"
                "**Trap:** confusing a right rotation (tail to front) with a left rotation (head to "
                "back) in (C)."
            ),
            "verify": '''
class Nd:
    def __init__(s, v, n=None): s.v, s.nxt = v, n
def mk(xs):
    h = None
    for x in reversed(xs): h = Nd(x, h)
    return h
def lst(h):
    o = []
    while h: o.append(h.v); h = h.nxt
    return o
A = lst(f(mk([1, 2, 3, 4, 5, 6]), 2)) == [5, 6, 1, 2, 3, 4]
C = lst(f(mk([1, 2, 3, 4, 5, 6]), 8)) == [3, 4, 5, 6, 1, 2]
steps = 0
h = mk([1, 2, 3, 4, 5, 6])
for _ in range(2):
    prev, cur = None, h
    while cur.nxt: prev, cur = cur, cur.nxt; steps += 1
    prev.nxt = None; cur.nxt = h; h = cur
B = steps == 12
try:
    f(mk([9]), 1); D = False
except AttributeError:
    D = True
assert [c for c, v in zip("ABCD", [A, B, C, D]) if v] == sorted(ANSWER)
''',
        },
    ],
}
