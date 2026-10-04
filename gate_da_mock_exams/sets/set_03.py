# Set 03 — Queues, Deques & Circular Buffers
SET = {
    "number": 3,
    "title": "Queues, Deques & Circular Buffers",
    "difficulty": "Moderate",
    "focus": "queues, circular queue arithmetic, deque, queue via stacks",
    "questions": [
        # ------------------------------------------------------------ Q1
        {
            "type": "MCQ", "marks": 1, "topic": "Python — collections.deque",
            "text": "Consider the following Python program. What is printed?",
            "code": '''from collections import deque
d = deque([3, 1, 4, 1, 5, 9])
d.rotate(2)
d.appendleft(d.pop())
d.rotate(-1)
d.extend([d.popleft(), d.pop()])
print(list(d))''',
            "options": ["`[9, 3, 1, 4, 5, 1]`", "`[9, 3, 1, 4, 1, 5]`",
                        "`[3, 1, 4, 1, 5, 9]`", "`[1, 4, 1, 5, 9, 3]`"],
            "answer": "A",
            "solution": (
                "`rotate(k)` with k > 0 moves the last k elements to the front (a right rotation); "
                "`rotate(-k)` moves the first k to the back. The arguments of `extend` are evaluated "
                "left to right **before** anything is appended.\n\n"
                "- Start: `[3, 1, 4, 1, 5, 9]`\n"
                "- `rotate(2)` → `[5, 9, 3, 1, 4, 1]`\n"
                "- `appendleft(pop())`: pop removes the rear 1 → `[1, 5, 9, 3, 1, 4]` (a right rotation by one)\n"
                "- `rotate(-1)` → `[5, 9, 3, 1, 4, 1]` (undoes the previous step)\n"
                "- `popleft()` gives 5 → `[9, 3, 1, 4, 1]`; then `pop()` gives 1 → `[9, 3, 1, 4]`; "
                "now `extend([5, 1])` → `[9, 3, 1, 4, 5, 1]`.\n\n"
                "Option-by-option:\n\n"
                "- (A) correct.\n"
                "- (B) appends the two removed values in the wrong order (pop before popleft).\n"
                "- (C) assumes the rotations cancel and extend re-adds the same ends — ignores the "
                "first `rotate(2)`.\n\n"
                "- (D) treats `rotate(2)` as a left rotation.\n\n"
                "**Trap:** the list literal `[d.popleft(), d.pop()]` is fully built before `extend` runs, "
                "so both removals happen first. **Tip:** `appendleft(pop())` ≡ `rotate(1)`."
            ),
            "verify": "assert OUTPUT.strip() == '[9, 3, 1, 4, 5, 1]'",
        },
        # ------------------------------------------------------------ Q2
        {
            "type": "NAT", "marks": 1, "topic": "Circular queue — occupancy arithmetic",
            "text": ("A circular queue is stored in an array `Q[0..9]` (size 10). `front` holds the index of the "
                     "first (oldest) element and `rear` holds the index of the last (newest) element. "
                     "The queue is non-empty and the current pointer values are shown below. "
                     "The number of elements currently in the queue is ______."),
            "diagrams": [{"type": "array", "values": ["", "", "", "", "", "", "", "", "", ""],
                          "pointers": {"rear": 3, "front": 7}, "label": "Q",
                          "caption": "front = 7, rear = 3 (contents not shown)"}],
            "answer": "7",
            "solution": (
                "With `front` and `rear` both pointing at occupied cells, a non-empty circular queue of "
                "size n holds\n\n"
                "count = ((rear − front + n) mod n) + 1.\n\n"
                "Here n = 10: count = ((3 − 7 + 10) mod 10) + 1 = 6 + 1 = **7**.\n\n"
                "Check by listing the occupied indices walking forward from front with wrap-around: "
                "7, 8, 9, 0, 1, 2, 3 — that is seven cells.\n\n"
                "**Trap:** forgetting the +1 gives 6 (that formula is for the convention where `rear` "
                "points to the next *free* slot). Computing 7 − 3 = 4 ignores the wrap-around and gives "
                "the number of **empty** cells minus one. **Tip:** always enumerate the indices once for "
                "a sanity check."
            ),
            "solution_diagrams": [{"type": "array", "values": ["x", "x", "x", "x", "", "", "", "x", "x", "x"],
                                   "highlight": [7, 8, 9, 0, 1, 2, 3],
                                   "pointers": {"rear": 3, "front": 7}, "label": "Q",
                                   "caption": "Occupied cells (x): 7, 8, 9, 0, 1, 2, 3"}],
            "verify": '''
n, front, rear = 10, 7, 3
cells = []
i = front
while True:
    cells.append(i)
    if i == rear: break
    i = (i + 1) % n
assert len(cells) == int(ANSWER) == (rear - front + n) % n + 1
''',
        },
        # ------------------------------------------------------------ Q3
        {
            "type": "NAT", "marks": 1, "topic": "Python — stack-based postfix evaluation",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''def ev(expr):
    st = []
    for t in expr.split():
        if t.isdigit():
            st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            if t == '-':
                st.append(a - b)
            elif t == '/':
                st.append(a // b)
            else:
                st.append(a * b)
    return st.pop()

print(ev("3 8 - 2 / 4 6 * -"))''',
            "answer": "-27",
            "solution": (
                "A Python list used with `append`/`pop` is a stack. For a binary operator the **first** pop "
                "is the right operand `b`, the second is the left operand `a`. `//` is floor division, "
                "which rounds toward −∞.\n\n"
                "- `3`, `8` → stack [3, 8]\n"
                "- `-` → b = 8, a = 3 → 3 − 8 = −5 → [−5]\n"
                "- `2` → [−5, 2]\n"
                "- `/` → −5 // 2 = **−3** (floor of −2.5) → [−3]\n"
                "- `4`, `6` → [−3, 4, 6]; `*` → 24 → [−3, 24]\n"
                "- `-` → −3 − 24 = **−27**\n\n"
                "**Traps:** (i) truncating toward zero gives −2 and a final answer of −26; "
                "(ii) swapping the operand order gives 8 − 3 = 5 at the first step. "
                "Note also that `'-5'.isdigit()` is False — the program only works because every input "
                "token is a non-negative literal."
            ),
            "solution_diagrams": [{"type": "stack", "values": [-3, 4, 6], "label": "stack just before `*`"}],
            "verify": "assert OUTPUT.strip() == ANSWER",
        },
        # ------------------------------------------------------------ Q4
        {
            "type": "MSQ", "marks": 1, "topic": "Python — list slicing",
            "text": ("Let `q = [10, 20, 30, 40, 50, 60]`. Which of the following statements is/are TRUE?"),
            "options": [
                "`q[::-2]` evaluates to `[60, 40, 20]`",
                "`q[4:1:-1]` evaluates to `[50, 40, 30, 20]`",
                "`q[-3:-1]` evaluates to `[40, 50]`",
                "`q[-1:-4]` evaluates to `[60, 50, 40]`",
            ],
            "answer": ["A", "C"],
            "solution": (
                "A slice `q[start:stop:step]` starts at `start`, moves by `step`, and stops **before** "
                "reaching `stop`. Negative indices count from the end (−1 is the last element). For a "
                "negative step the defaults are start = last, stop = before-the-first.\n\n"
                "- (A) step −2 from index 5: indices 5, 3, 1 → `[60, 40, 20]`. **True.**\n"
                "- (B) indices 4, 3, 2 (index 1 is the excluded stop) → `[50, 40, 30]`. **False** — "
                "the stop bound is exclusive in both directions.\n\n"
                "- (C) −3 → index 3, −1 → index 5 (excluded) → indices 3, 4 → `[40, 50]`. **True.**\n"
                "- (D) start index 5, stop index 2, step +1 (default): you cannot move forward from 5 "
                "to 2, so the result is `[]`. **False.**\n\n"
                "**Trap:** (D) looks like it should walk backwards, but without an explicit negative "
                "step Python never reverses — it silently returns an empty list."
            ),
            "verify": '''
q = [10, 20, 30, 40, 50, 60]
truth = [q[::-2] == [60, 40, 20], q[4:1:-1] == [50, 40, 30, 20],
         q[-3:-1] == [40, 50], q[-1:-4] == [60, 50, 40]]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        # ------------------------------------------------------------ Q5
        {
            "type": "MCQ", "marks": 1, "topic": "Linked-list queue",
            "text": ("A queue is implemented as a singly linked list with `head` (front) and `tail` (rear) "
                     "pointers; `enqueue` inserts after `tail`, `dequeue` removes the node at `head` and "
                     "returns its value. Starting from the queue shown, the following are executed:\n\n"
                     "`x = dequeue(); enqueue(x + 1); enqueue(dequeue()); dequeue(); enqueue(9)`\n\n"
                     "The contents of the queue from head to tail are"),
            "diagrams": [{"type": "linkedlist", "values": [12, 7, 25, 30], "head": "head", "tail": "tail"}],
            "options": ["30 → 13 → 7 → 9", "7 → 30 → 13 → 9", "25 → 30 → 13 → 9", "30 → 7 → 13 → 9"],
            "answer": "A",
            "solution": (
                "A queue is FIFO: removals come from the head, insertions go after the tail. Both are "
                "Θ(1) with a tail pointer.\n\n"
                "- `x = dequeue()` → x = 12; queue 7, 25, 30\n"
                "- `enqueue(13)` → 7, 25, 30, 13\n"
                "- `enqueue(dequeue())` removes 7 and re-inserts it at the rear → 25, 30, 13, 7\n"
                "- `dequeue()` removes 25 → 30, 13, 7\n"
                "- `enqueue(9)` → **30, 13, 7, 9**\n\n"
                "Option-by-option:\n\n"
                "- (A) correct.\n"
                "- (B) forgets that `enqueue(dequeue())` moves 7 to the back.\n"
                "- (C) skips the final `dequeue()`.\n"
                "- (D) puts 7 before 13, as if 7 had been moved before 13 was inserted.\n\n"
                "**Tip:** `enqueue(dequeue())` is a one-step rotation of the queue."
            ),
            "solution_diagrams": [{"type": "linkedlist", "values": [30, 13, 7, 9], "head": "head",
                                   "tail": "tail", "caption": "Final queue"}],
            "verify": '''
from collections import deque
q = deque([12, 7, 25, 30])
x = q.popleft(); q.append(x + 1); q.append(q.popleft()); q.popleft(); q.append(9)
assert list(q) == [30, 13, 7, 9] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q6
        {
            "type": "MCQ", "marks": 1, "topic": "Binary search — probe sequence",
            "text": ("Iterative binary search (`lo = 0`, `hi = n − 1`, `mid = (lo + hi) // 2`; if `A[mid] == x` "
                     "stop; if `A[mid] < x` then `lo = mid + 1` else `hi = mid − 1`; loop while `lo ≤ hi`) "
                     "searches for x = 37 in the sorted array below. The sequence of array values "
                     "compared with x is"),
            "diagrams": [{"type": "array", "values": [3, 8, 11, 15, 19, 22, 26, 31, 35, 40, 44, 51, 57, 62, 70],
                          "label": "A"}],
            "options": ["31, 51, 40, 35", "31, 44, 35, 40", "31, 51, 40, 35, 37", "26, 51, 40, 35"],
            "answer": "A",
            "solution": (
                "Each iteration halves the live range [lo, hi]; mid uses floor division.\n\n"
                "- lo=0, hi=14 → mid=7, A[7]=31 < 37 → lo=8\n"
                "- lo=8, hi=14 → mid=11, A[11]=51 > 37 → hi=10\n"
                "- lo=8, hi=10 → mid=9, A[9]=40 > 37 → hi=8\n"
                "- lo=8, hi=8 → mid=8, A[8]=35 < 37 → lo=9 > hi → stop (not found)\n\n"
                "Values probed: **31, 51, 40, 35** (4 probes = ⌊log₂ 15⌋ + 1).\n\n"
                "- (B) uses mid = 10 in the second step (as if hi were not 14).\n"
                "- (C) adds 37, which is not in the array at all.\n"
                "- (D) uses a wrong first midpoint (index 6).\n\n"
                "**Tip:** an unsuccessful search in an array of 2^{k} − 1 elements always makes exactly k probes."
            ),
            "verify": '''
A = [3, 8, 11, 15, 19, 22, 26, 31, 35, 40, 44, 51, 57, 62, 70]
lo, hi, seen = 0, len(A) - 1, []
while lo <= hi:
    m = (lo + hi) // 2; seen.append(A[m])
    if A[m] == 37: break
    if A[m] < 37: lo = m + 1
    else: hi = m - 1
assert seen == [31, 51, 40, 35] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q7
        {
            "type": "MCQ", "marks": 1, "topic": "Level-order traversal with a queue",
            "text": ("Level-order traversal of the binary tree below is done with a queue: enqueue the root; "
                     "repeatedly dequeue a node, visit it, then enqueue its left child and then its right "
                     "child (if present). Immediately after node **E** has been dequeued and its children "
                     "enqueued, the queue contents from front to rear are"),
            "diagrams": [{"type": "bintree",
                          "tree": ["A", ["B", ["D"], ["E", ["H"], None]], ["C", None, ["F", ["I"], ["J"]]]],
                          "caption": "Binary tree"}],
            "options": ["F, H", "H, F", "F, H, I, J", "H"],
            "answer": "A",
            "solution": (
                "The queue always holds a suffix of the current level followed by a prefix of the next "
                "level.\n\n"
                "- dequeue A → enqueue B, C → [B, C]\n"
                "- dequeue B → enqueue D, E → [C, D, E]\n"
                "- dequeue C → enqueue F (no left child) → [D, E, F]\n"
                "- dequeue D (leaf) → [E, F]\n"
                "- dequeue E → enqueue H → **[F, H]**\n\n"
                "- (B) reverses FIFO order — that would be a stack.\n"
                "- (C) adds I, J which are enqueued only when F is dequeued.\n"
                "- (D) forgets F, which was enqueued when C was processed.\n\n"
                "**Tip:** full level order is A B C D E F H I J; at any moment the queue is a contiguous "
                "window of that sequence."
            ),
            "verify": '''
from collections import deque
T = {"A": ("B", "C"), "B": ("D", "E"), "C": (None, "F"), "D": (None, None),
     "E": ("H", None), "F": ("I", "J"), "H": (None, None), "I": (None, None), "J": (None, None)}
q = deque(["A"])
while q:
    u = q.popleft()
    for c in T[u]:
        if c: q.append(c)
    if u == "E": break
assert list(q) == ["F", "H"] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q8
        {
            "type": "MCQ", "marks": 1, "topic": "Hashing — separate chaining",
            "text": ("The keys 24, 17, 40, 11, 45, 61, 9, 52 are inserted in that order into an initially empty "
                     "hash table of size 7 using h(k) = k mod 7 and separate chaining, where every new key is "
                     "inserted at the **head** of its chain. The chain at slot 3, read from head to tail, is"),
            "options": ["52 → 45 → 17 → 24", "24 → 17 → 45 → 52", "52 → 45 → 24 → 17", "45 → 52 → 17 → 24"],
            "answer": "A",
            "solution": (
                "Compute each home slot: 24→3, 17→3, 40→5, 11→4, 45→3, 61→5, 9→2, 52→3.\n\n"
                "Keys landing in slot 3, in insertion order: 24, 17, 45, 52. With head insertion each new "
                "key goes in front of the previous ones, so the chain reads in **reverse** insertion order: "
                "**52 → 45 → 17 → 24**.\n\n"
                "- (B) is tail insertion order.\n"
                "- (C) and (D) are not the reverse of any insertion order of these keys.\n\n"
                "Slot 5 similarly holds 61 → 40, slot 4 holds 11, slot 2 holds 9. Load factor α = 8/7.\n\n"
                "**Tip:** head insertion makes insertion Θ(1) without a tail pointer; the most recently "
                "inserted key is found fastest."
            ),
            "solution_diagrams": [{"type": "hashtable", "size": 7,
                                   "slots": {2: [9], 3: [52, 45, 17, 24], 4: [11], 5: [61, 40]},
                                   "caption": "Final table (chains head first)"}],
            "verify": '''
T = [[] for _ in range(7)]
for k in [24, 17, 40, 11, 45, 61, 9, 52]:
    T[k % 7].insert(0, k)
assert T[3] == [52, 45, 17, 24] and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q9
        {
            "type": "MCQ", "marks": 1, "topic": "Insertion sort — shifts",
            "text": ("Standard insertion sort (ascending) is applied to the array [5, 2, 8, 1, 9, 3, 7]. "
                     "A *shift* is one execution of `A[j+1] = A[j]` inside the inner loop. "
                     "The total number of shifts is"),
            "options": ["9", "7", "11", "6"],
            "answer": "A",
            "solution": (
                "Each shift fixes exactly one inversion (a pair i < j with A[i] > A[j]), so the number of "
                "shifts equals the number of inversions.\n\n"
                "Count, for each element, how many larger elements precede it:\n\n"
                "- 5: 0; 2: 1 (5); 8: 0; 1: 3 (5, 2, 8); 9: 0; 3: 3 (5, 8, 9); 7: 2 (8, 9)\n\n"
                "Total = 0 + 1 + 0 + 3 + 0 + 3 + 2 = **9**.\n\n"
                "- (B) 7 comes from missing that 3 has **three** larger predecessors (5, 8, 9), "
                "counting only 8 and 9.\n\n"
                "- (C) 11 over-counts — typically by counting the comparison that ends each pass as a shift.\n"
                "- (D) 6 is just the number of passes (n − 1).\n\n"
                "**Trap:** shifts ≠ comparisons. Comparisons = shifts + (number of passes in which the "
                "loop stopped because of a smaller element) — here 9 + 4 = 13."
            ),
            "solution_code": '''A = [5, 2, 8, 1, 9, 3, 7]; shifts = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0 and A[j] > key:
        A[j + 1] = A[j]; j -= 1; shifts += 1
    A[j + 1] = key
print(A, shifts)   # [1, 2, 3, 5, 7, 8, 9] 9''',
            "verify": '''
A = [5, 2, 8, 1, 9, 3, 7]; s = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0 and A[j] > key:
        A[j + 1] = A[j]; j -= 1; s += 1
    A[j + 1] = key
assert s == 9 and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q10
        {
            "type": "MSQ", "marks": 1, "topic": "BFS — valid visit orders",
            "text": ("Breadth-first search is run on the undirected graph below starting at P. Neighbours may be "
                     "enqueued in **any** order. Which of the following is/are possible BFS visit orders?"),
            "diagrams": [{"type": "graph", "directed": False,
                          "nodes": ["P", "Q", "R", "S", "T", "U"],
                          "edges": [["P", "Q"], ["P", "R"], ["Q", "S"], ["R", "S"], ["R", "T"],
                                    ["S", "U"], ["T", "U"]],
                          "pos": {"P": [0, 1], "Q": [1.5, 2], "R": [1.5, 0], "S": [3, 2], "T": [3, 0],
                                  "U": [4.5, 1]}}],
            "options": ["P, Q, R, S, T, U", "P, R, Q, T, S, U", "P, Q, R, T, S, U", "P, R, Q, S, U, T"],
            "answer": ["A", "B"],
            "solution": (
                "BFS visits vertices in non-decreasing distance from P, **and** within a level the order "
                "follows the order in which parents were dequeued (FIFO). Levels: {P}, {Q, R}, {S, T}, {U}.\n\n"
                "- (A) Q dequeued first discovers S; then R discovers T → S before T. **Valid.**\n"
                "- (B) R dequeued first discovers S and T (any order, here T then S); Q adds nothing new. "
                "**Valid.**\n\n"
                "- (C) Q is before R, so S (discovered by Q) must precede T (discovered only by R). "
                "**Invalid.**\n\n"
                "- (D) U (distance 3) appears before T (distance 2). **Invalid.**\n\n"
                "**Trap:** being level-consistent is necessary but not sufficient — (C) respects levels but "
                "violates the FIFO parent order."
            ),
            "verify": '''
from itertools import permutations
adj = {"P": "QR", "Q": "PS", "R": "PST", "S": "QRU", "T": "RU", "U": "ST"}
orders = set()
def bfs(choice):
    from collections import deque
    seen, q, out = {"P"}, deque("P"), []
    while q:
        u = q.popleft(); out.append(u)
        for v in choice[u]:
            if v not in seen: seen.add(v); q.append(v)
    return ", ".join(out)
import itertools
keys = list(adj)
for combo in itertools.product(*[list(permutations(adj[k])) for k in keys]):
    orders.add(bfs(dict(zip(keys, combo))))
opts = ["P, Q, R, S, T, U", "P, R, Q, T, S, U", "P, Q, R, T, S, U", "P, R, Q, S, U, T"]
assert sorted(ANSWER) == [c for c, o in zip("ABCD", opts) if o in orders]
''',
        },
        # ------------------------------------------------------------ Q11
        {
            "type": "NAT", "marks": 2, "topic": "Python — deque elimination simulation",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''from collections import deque
q = deque(range(1, 12))
while len(q) > 1:
    q.rotate(-(len(q) % 3))
    q.popleft()
print(q[0])''',
            "answer": "8",
            "solution": (
                "`rotate(-r)` moves the first r people to the back; `popleft()` then removes the person now "
                "at the front. The step r = len(q) mod 3 changes as the queue shrinks — so this is **not** a "
                "fixed-step Josephus problem and must be traced.\n\n"
                "- len 11, r=2: remove 3 → [4 5 6 7 8 9 10 11 1 2]\n"
                "- len 10, r=1: remove 5 → [6 7 8 9 10 11 1 2 4]\n"
                "- len 9, r=0: remove 6 → [7 8 9 10 11 1 2 4]\n"
                "- len 8, r=2: remove 9 → [10 11 1 2 4 7 8]\n"
                "- len 7, r=1: remove 11 → [1 2 4 7 8 10]\n"
                "- len 6, r=0: remove 1 → [2 4 7 8 10]\n"
                "- len 5, r=2: remove 7 → [8 10 2 4]\n"
                "- len 4, r=1: remove 10 → [2 4 8]\n"
                "- len 3, r=0: remove 2 → [4 8]\n"
                "- len 2, r=2: rotate by 2 is a full turn → remove 4 → [8]\n\n"
                "The survivor printed is **8**.\n\n"
                "**Traps:** (i) `rotate(-r)` is a *left* rotation — using a right rotation changes everything; "
                "(ii) when r = 0 the current front is removed immediately; (iii) in the last step rotating "
                "a 2-element deque by 2 leaves it unchanged."
            ),
            "verify": '''
from collections import deque
q = list(range(1, 12))
while len(q) > 1:
    r = len(q) % 3
    q = q[r:] + q[:r]
    q.pop(0)
assert OUTPUT.strip() == ANSWER == str(q[0])
''',
        },
        # ------------------------------------------------------------ Q12
        {
            "type": "NAT", "marks": 2, "topic": "Queue implemented with two stacks",
            "text": ("A queue is implemented using two stacks S1 and S2. `enqueue(x)` pushes x onto S1. "
                     "`dequeue()` first checks S2: if S2 is empty, it pops every element of S1 and pushes it onto "
                     "S2; it then pops and returns the top of S2. Each individual push or pop on S1 or S2 costs "
                     "one unit (the emptiness test is free). Starting with both stacks empty, the following "
                     "sequence is executed (E k = enqueue k, D = dequeue):\n\n"
                     "E1  E2  E3  D  E4  D  E5  E6  D  D  D  E7  D\n\n"
                     "The total cost of the whole sequence is ______."),
            "answer": "25",
            "solution": (
                "Lifetime (accounting) view: every element that is eventually dequeued costs exactly 4 units "
                "— push S1, pop S1, push S2, pop S2. An element still sitting in S1 at the end has cost only "
                "1 unit. Count the D's carefully: positions 4, 6, 9, 10, 11, 13 → **6** dequeues for "
                "7 enqueues, so element 7 is never transferred.\n\n"
                "Detailed trace (S1/S2 shown bottom→top, running cost):\n\n"
                "- E1 E2 E3: S1=[1,2,3]; cost 3\n"
                "- D: transfer 3 elements (6 units), pop 1 → S2=[3,2]; cost 10\n"
                "- E4: S1=[4]; cost 11.  D: pop 2 → cost 12\n"
                "- E5 E6: S1=[4,5,6]; cost 14.  D: pop 3 → S2 empty; cost 15\n"
                "- D: transfer 3 (6 units), pop 4 → S2=[6,5]; cost 22\n"
                "- D: pop 5 → cost 23.  E7: cost 24.  D: pop 6 → cost **25**\n\n"
                "Check with the lifetime argument: 6 dequeued elements × 4 = 24, plus 1 for element 7 "
                "left in S1 → 25.\n\n"
                "**Trap:** miscounting the dequeues, or charging a transfer on every dequeue (only when S2 "
                "is empty). **Tip:** the amortised cost per operation is O(1)."
            ),
            "solution_diagrams": [{"type": "matrix", "title": "Running state",
                                   "col_labels": ["op", "S1 (bottom→top)", "S2 (bottom→top)", "cost"],
                                   "rows": [["E1 E2 E3", "1 2 3", "—", 3], ["D → 1", "—", "3 2", 10],
                                            ["E4", "4", "3 2", 11], ["D → 2", "4", "3", 12],
                                            ["E5 E6", "4 5 6", "3", 14], ["D → 3", "4 5 6", "—", 15],
                                            ["D → 4", "—", "6 5", 22], ["D → 5", "—", "6", 23],
                                            ["E7", "7", "6", 24], ["D → 6", "7", "—", 25]]}],
            "verify": '''
ops = "E1 E2 E3 D E4 D E5 E6 D D D E7 D".split()
S1, S2, c, out = [], [], 0, []
for o in ops:
    if o[0] == "E":
        S1.append(int(o[1:])); c += 1
    else:
        if not S2:
            while S1:
                S2.append(S1.pop()); c += 2
        out.append(S2.pop()); c += 1
assert out == [1, 2, 3, 4, 5, 6] and c == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q13
        {
            "type": "MCQ", "marks": 2, "topic": "Circular queue — wasted-slot convention",
            "text": ("A circular queue uses an array of size 7 (indices 0–6). `front` is the index of the first "
                     "element and `rear` is the index of the next **free** slot. Initially front = rear = 0. "
                     "The queue is *full* when (rear + 1) mod 7 = front, and an enqueue on a full queue is "
                     "ignored. The following operations are performed:\n\n"
                     "enqueue 10, 20, 30, 40, 50; dequeue three times; enqueue 60, 70, 80, 90, 100; "
                     "dequeue twice; enqueue 110.\n\n"
                     "At the end, the values of (front, rear) and the number of elements in the queue are"),
            "options": ["front = 5, rear = 3, 5 elements", "front = 5, rear = 4, 6 elements",
                        "front = 5, rear = 2, 4 elements", "front = 4, rear = 3, 6 elements"],
            "answer": "A",
            "solution": (
                "With the wasted-slot convention an array of size 7 holds at most **6** elements; "
                "count = (rear − front + 7) mod 7.\n\n"
                "- Enqueue 10…50 into slots 0–4 → front 0, rear 5 (5 elements).\n"
                "- Three dequeues → front 3 (2 elements: 40, 50).\n"
                "- 60 → slot 5, 70 → slot 6, 80 → slot 0, 90 → slot 1 → rear 2, count (2 − 3 + 7) mod 7 = 6 "
                "→ **full**.\n\n"
                "- 100: (2 + 1) mod 7 = 3 = front → full → **ignored**.\n"
                "- Two dequeues remove 40, 50 → front 5.\n"
                "- 110 → slot 2 → rear 3.\n\n"
                "Final: front = 5, rear = 3, count = (3 − 5 + 7) mod 7 = **5** (60, 70, 80, 90, 110).\n\n"
                "- (B) assumes all 7 slots are usable, so 100 is accepted.\n"
                "- (C) forgets the final enqueue of 110.\n"
                "- (D) performs only one of the last two dequeues.\n\n"
                "**Trap:** the 'one empty slot' rule exists precisely so that front = rear can mean *empty*; "
                "it costs one cell of capacity."
            ),
            "solution_diagrams": [{"type": "array", "values": [80, 90, 110, "", "", 60, 70],
                                   "pointers": {"rear": 3, "front": 5}, "label": "Q",
                                   "caption": "Final state (slot 3, 4 free)"}],
            "verify": '''
N = 7; A = [None] * N; f = r = 0
def enq(x):
    global r
    if (r + 1) % N == f: return False
    A[r] = x; r = (r + 1) % N; return True
def deq():
    global f
    x = A[f]; A[f] = None; f = (f + 1) % N; return x
for x in (10, 20, 30, 40, 50): enq(x)
for _ in range(3): deq()
acc = [enq(x) for x in (60, 70, 80, 90, 100)]
for _ in range(2): deq()
enq(110)
assert acc == [True, True, True, True, False]
assert (f, r, (r - f) % N) == (5, 3, 5) and ANSWER == "A"
''',
        },
        # ------------------------------------------------------------ Q14
        {
            "type": "MSQ", "marks": 2, "topic": "Binary min-heap — insert & extract-min",
            "text": ("The keys 14, 9, 21, 6, 17, 3, 11 are inserted one at a time into an initially empty binary "
                     "min-heap stored in an array (0-based, children of i at 2i+1 and 2i+2; each insert "
                     "appends and sifts up). Then one `extract-min` is performed (the last element moves to "
                     "the root and sifts down, swapping with the smaller child). Which of the following "
                     "statements is/are TRUE?"),
            "options": [
                "After all seven insertions the array is [3, 9, 6, 14, 17, 21, 11]",
                "Exactly 4 swaps are performed in total during the seven insertions",
                "After the extract-min, the right child of the root is 11",
                "After the extract-min, the element at index 4 is 21",
            ],
            "answer": ["A", "C"],
            "solution": (
                "A priority queue implemented as a binary heap: insert = append + sift-up, extract-min = "
                "move last to root + sift-down.\n\n"
                "Insertions (swaps in brackets):\n\n"
                "- 14 → [14] (0)\n"
                "- 9 → swap with 14 → [9, 14] (1)\n"
                "- 21 → [9, 14, 21] (0)\n"
                "- 6 at index 3: swap with 14, then with 9 → [6, 9, 21, 14] (2)\n"
                "- 17 at index 4: parent 9 < 17 → [6, 9, 21, 14, 17] (0)\n"
                "- 3 at index 5: swap with 21, then with 6 → [3, 9, 6, 14, 17, 21] (2)\n"
                "- 11 at index 6: parent 6 < 11 → [3, 9, 6, 14, 17, 21, 11] (0)\n\n"
                "Total swaps = 5. Extract-min: remove 3, move 11 to root → [11, 9, 6, 14, 17, 21]; smaller "
                "child is 6 → swap → [6, 9, 11, 14, 17, 21]; 11's only child 21 is larger → stop.\n\n"
                "- (A) **True.**\n"
                "- (B) **False** — 5 swaps, not 4.\n"
                "- (C) index 2 holds 11. **True.**\n"
                "- (D) index 4 holds 17; 21 is at index 5. **False.**\n\n"
                "**Trap:** in sift-down always swap with the **smaller** child (9 vs 6 → choose 6); swapping "
                "with the left child by default breaks the heap property."
            ),
            "solution_diagrams": [{"type": "heap", "values": [6, 9, 11, 14, 17, 21],
                                   "caption": "Min-heap after extract-min"}],
            "verify": '''
h, sw = [], 0
for k in [14, 9, 21, 6, 17, 3, 11]:
    h.append(k); i = len(h) - 1
    while i and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2; h[p], h[i] = h[i], h[p]; i = p; sw += 1
after_ins = h[:]
h[0] = h.pop(); i = 0
while True:
    c = [j for j in (2 * i + 1, 2 * i + 2) if j < len(h)]
    if not c: break
    m = min(c, key=lambda j: h[j])
    if h[m] >= h[i]: break
    h[m], h[i] = h[i], h[m]; i = m
truth = [after_ins == [3, 9, 6, 14, 17, 21, 11], sw == 4, h[2] == 11, h[4] == 21]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
''',
        },
        # ------------------------------------------------------------ Q15
        {
            "type": "NAT", "marks": 2, "topic": "Dijkstra — counting relaxations",
            "text": ("Dijkstra's algorithm (with a min-priority queue) is run from source S on the weighted "
                     "directed graph below. Initially d[S] = 0 and every other d-value is ∞. Count every "
                     "event in which some d-value is **strictly decreased** by an edge relaxation (including a "
                     "decrease from ∞ to a finite value). The total number of such events is ______."),
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["S", "A", "B", "C", "D", "E"],
                          "edges": [["S", "A", 7], ["S", "B", 2], ["S", "C", 9], ["B", "A", 3],
                                    ["B", "D", 8], ["B", "C", 10], ["A", "C", 1], ["A", "D", 4],
                                    ["C", "E", 6], ["D", "E", 1]],
                          "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 2], "D": [4, 0],
                                  "E": [6, 1]}}],
            "answer": "9",
            "solution": (
                "Dijkstra extracts the vertex with the smallest tentative distance and relaxes its out-edges; "
                "a relaxation succeeds when d[u] + w < d[v].\n\n"
                "- Extract S (0): A ∞→7, B ∞→2, C ∞→9 — **3** decreases\n"
                "- Extract B (2): A 7→5, D ∞→10; C: 2+10 = 12 > 9 ✗ — **2**\n"
                "- Extract A (5): C 9→6, D 10→9 — **2**\n"
                "- Extract C (6): E ∞→12 — **1**\n"
                "- Extract D (9): E 12→10 — **1**\n"
                "- Extract E (10): no out-edges\n\n"
                "Total = 3 + 2 + 2 + 1 + 1 = **9**. Final distances: A 5, B 2, C 6, D 9, E 10.\n\n"
                "**Trap:** counting every edge examination (10 edges) instead of only successful ones; the "
                "relaxation of B→C fails. **Tip:** with a binary-heap PQ each successful relaxation is one "
                "decrease-key, so this count drives the O((V + E) log V) bound."
            ),
            "solution_diagrams": [{"type": "graph", "directed": True,
                                   "nodes": ["S", "A", "B", "C", "D", "E"],
                                   "edges": [["S", "A", 7], ["S", "B", 2], ["S", "C", 9], ["B", "A", 3],
                                             ["B", "D", 8], ["B", "C", 10], ["A", "C", 1], ["A", "D", 4],
                                             ["C", "E", 6], ["D", "E", 1]],
                                   "pos": {"S": [0, 1], "A": [2, 2], "B": [2, 0], "C": [4, 2], "D": [4, 0],
                                           "E": [6, 1]},
                                   "highlight_edges": [["S", "B"], ["B", "A"], ["A", "C"], ["A", "D"],
                                                       ["D", "E"]],
                                   "caption": "Shortest-path tree"}],
            "verify": '''
import heapq
G = {"S": [("A", 7), ("B", 2), ("C", 9)], "B": [("A", 3), ("D", 8), ("C", 10)],
     "A": [("C", 1), ("D", 4)], "C": [("E", 6)], "D": [("E", 1)], "E": []}
d = {v: float("inf") for v in G}; d["S"] = 0; pq = [(0, "S")]; cnt = 0; done = set()
while pq:
    du, u = heapq.heappop(pq)
    if u in done: continue
    done.add(u)
    for v, w in G[u]:
        if du + w < d[v]:
            d[v] = du + w; cnt += 1; heapq.heappush(pq, (d[v], v))
assert cnt == int(ANSWER) and d["E"] == 10
''',
        },
        # ------------------------------------------------------------ Q16
        {
            "type": "MCQ", "marks": 2, "topic": "Python — list as worklist (stack vs queue)",
            "text": ("The program below was intended to perform BFS on the directed graph shown, but it uses "
                     "`todo.pop()`. What does it print?"),
            "code": '''G = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d', 'e'],
     'd': ['f'], 'e': ['f'], 'f': []}

def walk(s):
    todo, seen, order = [s], {s}, []
    while todo:
        u = todo.pop()
        order.append(u)
        for v in G[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return ''.join(order)

print(walk('a'))''',
            "diagrams": [{"type": "graph", "directed": True,
                          "nodes": ["a", "b", "c", "d", "e", "f"],
                          "edges": [["a", "b"], ["a", "c"], ["b", "d"], ["c", "d"], ["c", "e"],
                                    ["d", "f"], ["e", "f"]],
                          "pos": {"a": [0, 1], "b": [1.5, 2], "c": [1.5, 0], "d": [3, 2], "e": [3, 0],
                                  "f": [4.5, 1]}}],
            "options": ["`acefdb`", "`abcdef`", "`abdfce`", "`acedfb`"],
            "answer": "A",
            "solution": (
                "`list.pop()` removes the **last** element, so `todo` behaves as a stack (LIFO). Vertices are "
                "marked `seen` when *pushed*, so each is pushed at most once — this is a stack-based "
                "traversal, not the recursive DFS order.\n\n"
                "- todo [a] → pop a; push b, c → [b, c]; order a\n"
                "- pop c; push d, e → [b, d, e]; order ac\n"
                "- pop e; f unseen → push f → [b, d, f]; order ace\n"
                "- pop f → [b, d]; order acef\n"
                "- pop d (f already seen) → [b]; order acefd\n"
                "- pop b (d seen) → order **acefdb**\n\n"
                "- (B) `abcdef` is the BFS order you would get with `todo.pop(0)`.\n"
                "- (C) `abdfce` is the recursive DFS order (visit neighbours in list order).\n"
                "- (D) `acedfb` would arise if d were popped before f — impossible since f was pushed last.\n\n"
                "**Trap:** marking on push (not on pop) means f is pushed by e, not d. **Tip:** use "
                "`collections.deque.popleft()` for BFS; `list.pop(0)` works but is O(n)."
            ),
            "verify": "assert OUTPUT.strip() == 'acefdb' and ANSWER == 'A'",
        },
        # ------------------------------------------------------------ Q17
        {
            "type": "NAT", "marks": 2, "topic": "Merge sort with a queue of runs",
            "text": ("A *queue-based* bottom-up merge sort works as follows. Each element of "
                     "[9, 4, 7, 1, 8, 2, 6, 3, 5] is enqueued as a one-element sorted run (in array order). "
                     "While the queue holds more than one run: dequeue run X, dequeue run Y, merge them with the "
                     "standard two-pointer merge, and enqueue the merged run. A *comparison* is one comparison "
                     "between an element of X and an element of Y; once either run is exhausted the rest is "
                     "copied without comparisons. The total number of comparisons is ______."),
            "answer": "21",
            "solution": (
                "Merging runs of sizes p and q costs between min(p, q) and p + q − 1 comparisons; the exact "
                "count is p + q − (number of elements left over when one run empties).\n\n"
                "- [9]+[4] → 1, [7]+[1] → 1, [8]+[2] → 1, [6]+[3] → 1  (queue now: [5], [4 9], [1 7], [2 8], [3 6])\n"
                "- [5]+[4 9] → 4 vs 5, 5 vs 9 → **2** → [4 5 9]\n"
                "- [1 7]+[2 8] → 1|2, 7|2, 7|8 → **3** → [1 2 7 8]\n"
                "- [3 6]+[4 5 9] → 3|4, 6|4, 6|5, 6|9 → **4** → [3 4 5 6 9]\n"
                "- [1 2 7 8]+[3 4 5 6 9] → 1|3, 2|3, 7|3, 7|4, 7|5, 7|6, 7|9, 8|9 → **8**\n\n"
                "Total = 4 + 2 + 3 + 4 + 8 = **21**.\n\n"
                "**Trap:** the odd element 5 does *not* wait for the end — FIFO order pairs it with the first "
                "merged run [4 9], so the merge tree is unbalanced compared with recursive merge sort. "
                "**Tip:** this queue scheme still makes O(n log n) comparisons overall."
            ),
            "solution_diagrams": [{"type": "queue", "values": ["[5]", "[4 9]", "[1 7]", "[2 8]", "[3 6]"],
                                   "caption": "Queue after the four singleton merges"}],
            "verify": '''
from collections import deque
Q = deque([[x] for x in [9, 4, 7, 1, 8, 2, 6, 3, 5]]); tot = 0
while len(Q) > 1:
    a, b = Q.popleft(), Q.popleft(); i = j = 0; r = []
    while i < len(a) and j < len(b):
        tot += 1
        if a[i] <= b[j]: r.append(a[i]); i += 1
        else: r.append(b[j]); j += 1
    Q.append(r + a[i:] + b[j:])
assert Q[0] == sorted(Q[0]) and tot == int(ANSWER)
''',
        },
        # ------------------------------------------------------------ Q18
        {
            "type": "MSQ", "marks": 2, "topic": "Quicksort — Lomuto partition",
            "text": ("The Lomuto partition below is applied once to A = [7, 2, 9, 4, 3, 8, 6] (pivot = last "
                     "element). Which of the following statements is/are TRUE?"),
            "code": '''def partition(A, lo, hi):
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= p:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    return i + 1''',
            "diagrams": [{"type": "array", "values": [7, 2, 9, 4, 3, 8, 6], "highlight": [6],
                          "label": "A", "caption": "pivot = A[6] = 6"}],
            "options": [
                "`partition(A, 0, 6)` returns 3",
                "After the call, A = [2, 4, 3, 6, 9, 8, 7]",
                "After the call, the part of A left of the pivot is already in sorted order",
                "If quicksort used this partition on an already ascending array of n distinct keys, it "
                "would take Θ(n²) time",
            ],
            "answer": ["A", "B", "D"],
            "solution": (
                "Lomuto keeps the invariant A[lo..i] ≤ pivot < A[i+1..j−1]; at the end the pivot is swapped "
                "into position i + 1.\n\n"
                "- j=0 (7 > 6) skip\n"
                "- j=1 (2 ≤ 6): i=0, swap A0↔A1 → [2, 7, 9, 4, 3, 8, 6]\n"
                "- j=2 (9) skip\n"
                "- j=3 (4): i=1, swap A1↔A3 → [2, 4, 9, 7, 3, 8, 6]\n"
                "- j=4 (3): i=2, swap A2↔A4 → [2, 4, 3, 7, 9, 8, 6]\n"
                "- j=5 (8) skip\n"
                "- final swap A3↔A6 → [2, 4, 3, 6, 9, 8, 7], return 3\n\n"
                "- (A) **True.**\n"
                "- (B) **True.**\n"
                "- (C) left part is [2, 4, 3] — not sorted. **False.** Partition only guarantees ≤ pivot, "
                "not order.\n\n"
                "- (D) on sorted input the last element is the maximum, every split is (n−1, 0), "
                "T(n) = T(n−1) + Θ(n) = Θ(n²). **True.**\n\n"
                "**Trap:** partitioning is not sorting, and Lomuto is not stable: the right part was "
                "7, 9, 8 in the input but ends up as 9, 8, 7 because the pivot swap moved 7 to the end."
            ),
            "solution_diagrams": [{"type": "array", "values": [2, 4, 3, 6, 9, 8, 7], "highlight": [3],
                                   "label": "A", "caption": "After partition: pivot 6 at index 3"}],
            "verify": '''
A = [7, 2, 9, 4, 3, 8, 6]
k = partition(A, 0, 6)
truth = [k == 3, A == [2, 4, 3, 6, 9, 8, 7], A[:3] == sorted(A[:3]), True]
assert sorted(ANSWER) == [c for c, t in zip("ABCD", truth) if t]
import sys
sys.setrecursionlimit(10000)
cnt = [0]
def qs(B, lo, hi, d=0):
    if lo < hi:
        cnt[0] += hi - lo
        m = partition(B, lo, hi); qs(B, lo, m - 1); qs(B, m + 1, hi)
qs(list(range(200)), 0, 199)
assert cnt[0] == 199 * 200 // 2
''',
        },
        # ------------------------------------------------------------ Q19
        {
            "type": "NAT", "marks": 2, "topic": "Monotonic deque — sliding window maximum",
            "text": "Consider the following Python program. The value printed is ______.",
            "code": '''from collections import deque

def win_max(a, k):
    dq, pops, res = deque(), 0, []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] <= x:
            dq.pop()
            pops += 1
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(a[dq[0]])
    return pops, res

p, r = win_max([4, 2, 12, 3, 8, 5, 7, 1, 9, 6], 3)
print(p + sum(r))''',
            "answer": "83",
            "solution": (
                "The deque stores **indices** whose values are strictly decreasing from front to rear. A new "
                "value pops every smaller-or-equal value from the rear (they can never be a future maximum); "
                "the front is dropped once it slides out of the window. The front is always the window max.\n\n"
                "- i0 4: dq [0]\n"
                "- i1 2: dq [0,1]\n"
                "- i2 12: pops 2 and 4 (**2 pops**) → [2]; max 12\n"
                "- i3 3: [2,3]; max 12\n"
                "- i4 8: pops 3 (**1**) → [2,4]; max 12\n"
                "- i5 5: [2,4,5]; index 2 ≤ 5−3 → popleft → [4,5]; max 8\n"
                "- i6 7: pops 5 (**1**) → [4,6]; max 8\n"
                "- i7 1: [4,6,7]; index 4 ≤ 4 → popleft → [6,7]; max 7\n"
                "- i8 9: pops 1 and 7 (**2**) → [8]; max 9\n"
                "- i9 6: [8,9]; max 9\n\n"
                "pops = 2 + 1 + 1 + 2 = 6; r = [12, 12, 12, 8, 8, 7, 9, 9], sum = 77. Printed: 6 + 77 = **83**.\n\n"
                "**Trap:** `popleft()` (window expiry) is not counted in `pops` — only rear pops are. "
                "**Tip:** each index is pushed once and popped at most once, so the algorithm is Θ(n) "
                "regardless of k."
            ),
            "solution_diagrams": [{"type": "array", "values": [4, 2, 12, 3, 8, 5, 7, 1, 9, 6],
                                   "highlight": [5, 6, 7], "pointers": {"i": 7}, "label": "a",
                                   "caption": "Window at i = 7: deque holds indices 6, 7 → max a[6] = 7"}],
            "verify": '''
a = [4, 2, 12, 3, 8, 5, 7, 1, 9, 6]
r2 = [max(a[i:i + 3]) for i in range(len(a) - 2)]
assert r == r2 and p == 6
assert OUTPUT.strip() == ANSWER == str(6 + sum(r2))
''',
        },
        # ------------------------------------------------------------ Q20
        {
            "type": "MSQ", "marks": 2, "topic": "Output-restricted deque permutations",
            "text": ("The numbers 1, 2, 3, 4 arrive in this order and each must be inserted into an initially empty "
                     "**output-restricted deque** as soon as it arrives (insertion is allowed at either end, "
                     "deletion only at the front). Deletions may be performed at any time, and each deleted "
                     "number is written to the output. Which of the following output sequences CANNOT be "
                     "produced?"),
            "options": ["4, 1, 3, 2", "4, 3, 1, 2", "3, 1, 4, 2", "4, 2, 3, 1"],
            "answer": ["A", "D"],
            "solution": (
                "If 4 is output first, then 1, 2, 3 are all inside the deque before any deletion, and the "
                "remaining output is just the deque read front-to-rear. Building the deque by inserting 1, "
                "then 2 at either end, then 3 at either end gives only:\n\n"
                "3 2 1, 2 1 3, 3 1 2, 1 2 3\n\n"
                "(the values must form a sequence where each newly inserted number is at an **end**). "
                "With 4 inserted at the front and deleted first, the possible outputs starting with 4 are "
                "4321, 4213, 4312, 4123.\n\n"
                "- (A) 4 1 3 2 → would need deque 1 3 2 with 3 in the middle. **Cannot.**\n"
                "- (B) 4 3 1 2 → deque 3 1 2 (1; 2 at rear; 3 at front). **Can.**\n"
                "- (C) insert 1, insert 2 at the rear → [1 2]; insert 3 at front → [3 1 2]; delete 3, "
                "delete 1; insert 4 at front → [4 2]; delete 4, delete 2 → 3 1 4 2. **Can.**\n\n"
                "- (D) 4 2 3 1 → deque 2 3 1 with 3 in the middle, but 3 was the last of the three inserted. "
                "**Cannot.**\n\n"
                "Of the 24 permutations exactly 22 are achievable; the only two impossible ones are (A) and (D).\n\n"
                "**Tip:** the last-inserted element of a deque must sit at one of its ends — a quick test for "
                "any 'restricted deque' question."
            ),
            "verify": '''
import itertools
res = set()
def rec(i, dq, out):
    if len(out) == 4:
        res.add(tuple(out)); return
    if dq: rec(i, dq[1:], out + [dq[0]])
    if i <= 4:
        rec(i + 1, [i] + dq, out); rec(i + 1, dq + [i], out)
rec(1, [], [])
opts = [(4, 1, 3, 2), (4, 3, 1, 2), (3, 1, 4, 2), (4, 2, 3, 1)]
assert len(res) == 22
assert sorted(ANSWER) == [c for c, o in zip("ABCD", opts) if o not in res]
''',
        },
    ],
}
