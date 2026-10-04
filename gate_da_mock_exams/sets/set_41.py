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
    ],
}
