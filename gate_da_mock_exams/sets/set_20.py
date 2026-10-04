# Set 20 — Stack & Queue Applications

SET = {
    'number': 20,
    'title': 'Stack & Queue Applications',
    'difficulty': 'GATE-level',
    'focus': 'simulations, monotonic stack, two-stack queue costs, amortised ops',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — closures and late binding',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''fs = [lambda: i * i for i in range(4)]
gs = [lambda i=i: i * i for i in range(4)]
print(sum(f() for f in fs), sum(g() for g in gs))''',
            'options': ['`14 14`', '`36 14`', '`36 36`', '`0 14`'],
            'answer': 'B',
            'solution': '''**Concept.** A lambda body looks up free variables when it is *called*, not when it is created (late binding). A default argument, by contrast, is evaluated once when the lambda is *defined*.

- In `fs`, all four lambdas refer to the comprehension’s variable `i`. When they are called the comprehension has finished, so `i` = 3 for every lambda. Each returns 9 → sum = 4 × 9 = **36**.
- In `gs`, `i=i` captures the current value as a default parameter: the lambdas return 0, 1, 4, 9 → sum = **14**.

Output: `36 14` → (B).

**Options.** (A) assumes the first list also captures values. (C) assumes the default-arg trick does not help. (D) assumes `i` is 0 in the closures (or that the comprehension variable is not visible) — but each comprehension has its own scope whose `i` ends at 3.

**Tip:** `i=i` (or `functools.partial`) is the standard fix for late binding in loops.''',
            'verify': "assert OUTPUT.strip() == '36 14' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Monotonic stack — next greater element',
            'text': 'The function below computes, for every element, the next greater element to its right (−1 if none) using a stack of indices. What is the value of `s` after `s, p = nge_sum([5, 3, 8, 2, 4, 9, 1, 7])`?',
            'code': '''def nge_sum(a):
    res, st, pops = [-1] * len(a), [], 0
    for i, x in enumerate(a):
        while st and a[st[-1]] < x:
            res[st.pop()] = x
            pops += 1
        st.append(i)
    return sum(res), pops

s, p = nge_sum([5, 3, 8, 2, 4, 9, 1, 7])''',
            'answer': '43',
            'solution': '''**Concept.** The stack holds indices whose next greater element is still unknown; their values are non-increasing from bottom to top. A new value x pops every smaller value — x is their answer.

- x=5: push. Stack [5]
- x=3: 5 ≥ 3, push. [5, 3]
- x=8: pops 3 (→8) and 5 (→8). [8]
- x=2: push. [8, 2]
- x=4: pops 2 (→4). [8, 4]
- x=9: pops 4 (→9) and 8 (→9). [9]
- x=1: push. [9, 1]
- x=7: pops 1 (→7). [9, 7]
- End: 9 and 7 keep −1.

res = [8, 8, 9, 4, 9, −1, 7, −1]; s = 8+8+9+4+9−1+7−1 = **43** (and p = 6 pops).

**Trap:** forgetting the two −1 entries (giving 45), or taking the *maximum* to the right instead of the *next* greater element (e.g. 9 for 5).''',
            'verify': 'assert s == int(ANSWER) and p == 6',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues — circular array',
            'text': '''A queue is stored in a circular array Q[0..6] (capacity 7). `front` is the index of the first element and `rear` is the index where the **next** element will be written; both advance by (index + 1) mod 7. Initially front = rear = 3 and the queue is empty. The values 10, 20, 30, … are enqueued in this order, interleaved as follows:
enqueue 5 values, dequeue 3, enqueue 4 values, dequeue 2.
What are (front, rear, Q[front]) at the end?''',
            'options': ['(1, 4, 60)', '(1, 5, 60)', '(5, 1, 90)', '(1, 5, 50)'],
            'answer': 'B',
            'solution': '''**Concept.** front advances once per dequeue and rear once per enqueue, both modulo the capacity; the k-th value ever enqueued sits at index (start + k − 1) mod 7.

- 9 enqueues: rear = (3 + 9) mod 7 = **5**.
- 5 dequeues: front = (3 + 5) mod 7 = **1**.
- Queue length = 9 − 5 = 4 (never exceeds 7: the peak is 6 after the second batch).
- The values removed are 10, 20, 30, 40, 50, so the front value is the 6th one enqueued, **60**, stored at index (3 + 5) mod 7 = 1 ✓.

Remaining contents: Q[1]=60, Q[2]=70, Q[3]=80, Q[4]=90 → (1, 5, 60).

**Options.** (A) treats rear as the index of the last element. (C) swaps the roles of front and rear. (D) is off by one in the dequeued count.

**Tip:** with this convention, length = (rear − front) mod capacity whenever the queue is not full: (5 − 1) mod 7 = 4 ✓.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [None, 60, 70, 80, 90, None, None],
                    'label': 'Q',
                    'pointers': {
                        'front': 1,
                        'rear': 5,
                    },
                    'caption': 'Final circular array (slots 0, 5, 6 hold stale/no data)',
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

Q = [None] * 7; f = r = 3; vals = iter(range(10, 1000, 10))
def enq(k):
    global r
    for _ in range(k): Q[r] = next(vals); r = (r + 1) % 7
def deq(k):
    global f
    for _ in range(k): f = (f + 1) % 7
enq(5); deq(3); enq(4); deq(2)
assert (f, r, Q[f]) == (1, 5, 60) and ANSWER == 'C'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — valid stack permutations',
            'text': '''The numbers 1, 2, 3, 4, 5 are pushed onto an initially empty stack in this order; pops may be interleaved arbitrarily with the pushes and each popped value is output immediately. How many of the following six sequences can be produced as the output?
(i) 3 2 5 4 1   (ii) 4 2 3 1 5   (iii) 2 1 5 3 4
(iv) 1 5 4 3 2   (v) 5 3 4 2 1   (vi) 3 4 2 5 1''',
            'answer': '3',
            'solution': '''**Concept.** Simulate greedily: to output x, push every not-yet-pushed value up to x, then x must be on top. Equivalently, a sequence is invalid iff it contains a pattern … c … a … b … with a < b < c (a “312” pattern).

- (i) 3 2 5 4 1: push 1,2,3 pop 3; pop 2; push 4,5 pop 5; pop 4; pop 1. **Valid.**
- (ii) 4 2 3 1 5: after popping 4 the top is 3, not 2. **Invalid** (pattern 4,2,3).
- (iii) 2 1 5 3 4: after 5, stack holds 3, 4 with 4 on top; 3 is blocked. **Invalid.**
- (iv) 1 5 4 3 2: pop 1; push 2..5, pop 5, 4, 3, 2. **Valid.**
- (v) 5 3 4 2 1: after 5 the top is 4, not 3. **Invalid.**
- (vi) 3 4 2 5 1: pop 3; push 4 pop 4; pop 2; push 5 pop 5; pop 1. **Valid.**

Valid sequences: (i), (iv), (vi) → **3**.

**Trap:** once a larger value is popped, every smaller value still on the stack must come out in *decreasing* order.''',
            'verify': '''
def valid(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x: st.append(nxt); nxt += 1
        if st[-1] != x: return False
        st.pop()
    return True
C = [(3,2,5,4,1),(4,2,3,1,5),(2,1,5,3,4),(1,5,4,3,2),(5,3,4,2,1),(3,4,2,5,1)]
assert sum(valid(c) for c in C) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Deques — input-restricted deque',
            'text': 'The values 1, 2, 3, 4 arrive in this order and must be inserted at the **rear** of an input-restricted deque (insertion only at the rear, deletion at either end). Deletions may be interleaved with insertions and each deleted value is output. Which of the following output sequences are possible?',
            'options': ['2 4 1 3', '4 1 3 2', '4 2 1 3', '4 2 3 1'],
            'answer': ['A', 'B'],
            'solution': '''**Concept.** If 4 is output first, all of 1, 2, 3 are already inside, in order 1 2 3 from front to rear; afterwards only the two ends can be taken.

- (A) 2 4 1 3: insert 1, 2; delete 2 from the rear; insert 3, 4; delete 4 from the rear; deque [1, 3] → 1 from front, then 3. **Possible.**
- (B) 4 1 3 2: deque [1, 2, 3] → take 1 from the front → [2, 3] → take 3 from the rear → 2. **Possible.**
- (C) 4 2 1 3: again 2 is in the middle of [1, 2, 3] when it is needed. **Impossible.**
- (D) 4 2 3 1: after removing 4 the deque is [1, 2, 3]; 2 is in the middle and cannot be removed. **Impossible.**

In fact, of the 24 permutations of 1..4 exactly 22 are achievable; the two impossible ones are precisely 4 2 1 3 and 4 2 3 1.

**Tip:** for an input-restricted deque the hard cases are those where a *middle* element must leave before both its neighbours.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

res = set()
def rec(nxt, d, out):
    if len(out) == 4: res.add(tuple(out)); return
    if nxt <= 4: rec(nxt + 1, d + [nxt], out)
    if d:
        rec(nxt, d[1:], out + [d[0]]); rec(nxt, d[:-1], out + [d[-1]])
rec(1, [], [])
opts = [(4,2,3,1), (4,1,3,2), (2,4,1,3), (4,2,1,3)]
assert [L for L, o in zip('ABCD', opts) if o in res] == sorted(ANSWER)
assert len(res) == 22
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — collections.deque',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from collections import deque
d = deque([10, 20, 30, 40, 50])
d.rotate(2)
d.appendleft(d.pop())
d.extendleft([1, 2])
x = d.popleft() + d[-1]
d.rotate(-3)
print(x, list(d))''',
            'options': [
                '`21 [50, 10, 20, 2, 30, 40]`',
                '`22 [1, 30, 40, 50, 10, 20]`',
                '`22 [50, 10, 20, 1, 30, 40]`',
                '`12 [40, 50, 10, 1, 20, 30]`',
            ],
            'answer': 'C',
            'solution': '''**Concept.** `rotate(k)` with k > 0 moves the last k items to the front; with k < 0 it moves the first |k| items to the back. `extendleft` inserts items one by one at the left, so they appear **reversed**.

- `rotate(2)` → [40, 50, 10, 20, 30]
- `pop()` removes 30; `appendleft` → [30, 40, 50, 10, 20]
- `extendleft([1, 2])` → 1 goes left, then 2 goes left of it → [2, 1, 30, 40, 50, 10, 20]
- `popleft()` = 2, `d[-1]` = 20 → x = **22**; d = [1, 30, 40, 50, 10, 20]
- `rotate(-3)` → [50, 10, 20, 1, 30, 40]

Output `22 [50, 10, 20, 1, 30, 40]` → (C).

**Options.** (A) forgets that `extendleft` reverses (takes 1 as the leftmost). (B) omits the final rotation. (D) rotates the wrong way at the start.

**Trap:** `extendleft(iterable)` ≠ `iterable + d`; it equals `reversed(iterable) + d`.''',
            'verify': "ANSWER = {'D': 'C', 'C': 'D'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '22 [50, 10, 20, 1, 30, 40]' and ANSWER == 'D'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — double hashing',
            'text': 'Keys 27, 17, 49, 30, 71, 38 are inserted in this order into an empty table of size 11 using double hashing: probe i (i = 0, 1, 2, …) examines slot (h₁(k) + i·h₂(k)) mod 11, where h₁(k) = k mod 11 and h₂(k) = 1 + (k mod 7). The index of the slot in which 38 is stored is ______.',
            'answer': '2',
            'solution': '''**Concept.** In double hashing the step size depends on the key, so keys sharing a home slot follow *different* probe sequences.

- 27: h₁ = 5 → slot **5**.
- 17: h₁ = 6 → slot **6**.
- 49: h₁ = 5 (full), h₂ = 1 + 0 = 1 → 6 (full) → **7**.
- 30: h₁ = 8 → slot **8**.
- 71: h₁ = 5 (full), h₂ = 1 + 1 = 2 → 7 (full) → **9**.
- 38: h₁ = 5 (full), h₂ = 1 + 3 = 4 → 9 (full) → 13 mod 11 = **2** (free).

So 38 is stored at index **2** after three probes.

**Trap:** applying linear probing (step 1) would put 38 at index 10; and forgetting the “1 +” in h₂ gives step 3 for 38 → 8 (full) → 0, a wrong slot.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        2: 38,
                        5: 27,
                        6: 17,
                        7: 49,
                        8: 30,
                        9: 71,
                    },
                    'caption': 'Final table',
                },
            ],
            'verify': '''
T = [None] * 11
for k in [27, 17, 49, 30, 71, 38]:
    h1, h2, i = k % 11, 1 + k % 7, 0
    while T[(h1 + i * h2) % 11] is not None: i += 1
    T[(h1 + i * h2) % 11] = k
assert T.index(38) == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search — lower bound',
            'text': 'Consider the following Python function and list.',
            'code': '''def lb(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

a = [3, 7, 7, 7, 12, 18, 18, 25]''',
            'text2': 'Which of the following statements is/are TRUE?',
            'options': [
                '`lb(a, 7)` returns 1',
                '`lb(a, 30)` returns 7',
                'The `while` loop body executes exactly 3 times during `lb(a, 7)`',
                '`lb(a, 18) - lb(a, 12)` equals 1',
            ],
            'answer': ['A', 'D'],
            'solution': '''**Concept.** `lb` returns the first index whose value is ≥ x (len(a) if none), on the half-open interval [lo, hi).

- (A) First value ≥ 7 is at index 1. **TRUE.**
- (B) No value is ≥ 30, so the function returns len(a) = **8**, not 7. **FALSE.**
- (C) Trace for x = 7: (lo, hi) = (0, 8) → mid 4, 12 ≥ 7 → hi = 4; (0, 4) → mid 2, 7 ≥ 7 → hi = 2; (0, 2) → mid 1 → hi = 1; (0, 1) → mid 0, 3 < 7 → lo = 1. That is **4** iterations. **FALSE.**
- (D) lb(a, 18) = 5 and lb(a, 12) = 4 → difference 1 (= number of 12s). **TRUE.**

**Trap:** on a half-open interval the size goes 8 → 4 → 2 → 1 → 0, so up to ⌊log₂ n⌋ + 1 = 4 iterations are needed — not log₂ 8 = 3.''',
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def lbc(a, x):
    lo, hi, it = 0, len(a), 0
    while lo < hi:
        it += 1; mid = (lo + hi) // 2
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    return it
res = [lb(a, 7) == 1, lb(a, 18) - lb(a, 12) == 1, lb(a, 30) == 7, lbc(a, 7) == 3]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Expression trees from postfix',
            'text': '''An expression tree is built from the postfix expression
6 3 1 − / 4 2 ^ 5 * +
using a stack of subtrees (an operand is pushed as a leaf; an operator pops its right child, then its left child, and pushes the new subtree). Which of the following statements is/are TRUE? (`^` denotes exponentiation.)''',
            'options': [
                'The expression evaluates to 83',
                'The tree has exactly 5 leaves',
                'The stack never holds more than 3 subtrees during the construction',
                'The prefix form of the tree is + / 6 − 3 1 * ^ 4 2 5',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''**Concept.** Postfix → tree is a direct stack simulation; the last operator becomes the root.

Stack trace (sizes in brackets): 6 [1], 3 [2], 1 [3], − → (3−1) [2], / → 6/(3−1) [1], 4 [2], 2 [3], ^ → 4^2 [2], 5 [3], * → (4^2)*5 [2], + → root [1].

- (A) 6/(3−1) + 4^{2}·5 = 3 + 80 = 83. **TRUE.**
- (B) Leaves are the operands 6, 3, 1, 4, 2, 5 → **6** leaves. **FALSE.**
- (C) The maximum stack size is 3 (reached three times). **TRUE.**
- (D) Pre-order of the tree: + / 6 − 3 1 * ^ 4 2 5. **TRUE.**

**Trap:** the first popped subtree is the **right** child — swapping them would turn 3 − 1 into 1 − 3 and the value into −3 + 80.''',
            'solution_diagrams': [
                {
                    'type': 'tree',
                    'root': '+',
                    'children': {
                        '+': ['/', '*'],
                        '/': ['6', '−'],
                        '−': ['3', '1'],
                        '*': ['^', '5'],
                        '^': ['4', '2'],
                    },
                    'caption': 'Expression tree',
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

st = []; mx = 0
for t in "6 3 1 - / 4 2 ^ 5 * +".split():
    if t.isdigit(): st.append(t)
    else:
        r = st.pop(); l = st.pop(); st.append((t, l, r))
    mx = max(mx, len(st))
T = st[0]
pre = lambda n: [n] if isinstance(n, str) else [n[0]] + pre(n[1]) + pre(n[2])
ev = lambda n: int(n) if isinstance(n, str) else {'+': lambda a, b: a + b,
    '-': lambda a, b: a - b, '*': lambda a, b: a * b, '/': lambda a, b: a // b,
    '^': lambda a, b: a ** b}[n[0]](ev(n[1]), ev(n[2]))
leaves = sum(1 for x in pre(T) if x.isdigit())
res = [' '.join(pre(T)) == '+ / 6 - 3 1 * ^ 4 2 5', ev(T) == 83, leaves == 5, mx <= 3]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'BFS — queue occupancy',
            'text': 'BFS is run on the undirected graph below from vertex A; when a vertex is dequeued, its unvisited neighbours are enqueued in alphabetical order (a vertex is marked visited when it is enqueued). The maximum number of vertices present in the queue at any instant is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['B', 'F'],
                        ['C', 'F'],
                        ['C', 'G'],
                        ['D', 'H'],
                        ['E', 'I'],
                        ['F', 'I'],
                        ['G', 'H'],
                        ['H', 'I'],
                    ],
                    'pos': {
                        'A': [2, 3],
                        'B': [0, 2],
                        'C': [2, 2],
                        'D': [4, 2],
                        'E': [0, 1],
                        'F': [1.5, 1],
                        'G': [3, 1],
                        'H': [4, 1],
                        'I': [2, 0],
                    },
                },
            ],
            'answer': '4',
            'solution': '''**Concept.** The queue length grows when a dequeued vertex discovers several new vertices and shrinks by one per dequeue.

Queue after processing each vertex:

- A → enqueue B, C, D: [B, C, D] (3)
- B → enqueue E, F: [C, D, E, F] (**4**)
- C → F seen; enqueue G: [D, E, F, G] (**4**)
- D → enqueue H: [E, F, G, H] (**4**)
- E → enqueue I: [F, G, H, I] (**4**)
- F, G, H, I discover nothing new: 3, 2, 1, 0.

Maximum = **4**.

A vertex is removed from the queue before its neighbours are added, so the count never momentarily exceeds these values.

**Trap:** guessing the maximum degree (3) — the queue holds parts of two consecutive BFS levels at once.''',
            'verify': '''
from collections import deque
G = {'A':'BCD','B':'AEF','C':'AFG','D':'AH','E':'BI','F':'BCI','G':'CH',
     'H':'DGI','I':'EFH'}
seen = {'A'}; q = deque('A'); mx = 1
while q:
    u = q.popleft()
    for v in sorted(G[u]):
        if v not in seen: seen.add(v); q.append(v); mx = max(mx, len(q))
assert mx == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Monotonic stack — stock span',
            'text': '''The *span* of day i is the number of consecutive days ending at day i (including day i) whose price is ≤ the price on day i. Spans are computed with the stack algorithm below for the prices
30, 25, 28, 22, 26, 35, 31, 33, 40
The sum of all nine spans is ______.''',
            'code': '''def spans(p):
    st, out = [], []
    for i, x in enumerate(p):
        while st and p[st[-1]] <= x:
            st.pop()
        out.append(i + 1 if not st else i - st[-1])
        st.append(i)
    return out''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [30, 25, 28, 22, 26, 35, 31, 33, 40],
                    'label': 'p',
                    'caption': 'Prices, day 0 to day 8',
                },
            ],
            'answer': '25',
            'solution': '''**Concept.** The stack keeps indices of a strictly decreasing sequence of prices — the only days that can still block a future span. A day’s span reaches back to the nearest earlier day with a *greater* price (the stack top after popping).

- Day 0 (30): stack empty → span 1. Stack [30]
- Day 1 (25): top 30 > 25 → span 1. [30, 25]
- Day 2 (28): pop 25; top 30 (day 0) → span 2. [30, 28]
- Day 3 (22): top 28 → span 1. [30, 28, 22]
- Day 4 (26): pop 22; top 28 (day 2) → span 2. [30, 28, 26]
- Day 5 (35): pops 26, 28, 30; empty → span 6. [35]
- Day 6 (31): top 35 → span 1. [35, 31]
- Day 7 (33): pop 31; top 35 (day 5) → span 2. [35, 33]
- Day 8 (40): pops 33, 35; empty → span 9. [40]

Spans = 1, 1, 2, 1, 2, 6, 1, 2, 9 → sum = **25**.

Amortised cost: there are 8 pops in total, never more than n = 9, so the algorithm is Θ(n) despite the nested loop.

**Trap:** counting only *consecutive* smaller days via the previous day’s comparison (e.g. giving day 4 a span of 2 but day 5 a span of 3) — the span jumps over every popped run.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Span of each day',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
                    'row_labels': ['price', 'span'],
                    'rows': [
                        [30, 25, 28, 22, 26, 35, 31, 33, 40],
                        [1, 1, 2, 1, 2, 6, 1, 2, 9],
                    ],
                },
            ],
            'verify': '''
p = [30, 25, 28, 22, 26, 35, 31, 33, 40]
brute = []
for i in range(len(p)):
    j = i
    while j >= 0 and p[j] <= p[i]: j -= 1
    brute.append(i - j)
assert brute == spans(p) and sum(brute) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Stacks — infix to postfix',
            'text': '''The infix expression
a − b ^ c ^ d * e + f / (g − h) * i
is converted to postfix by the standard operator-stack algorithm. Precedence: ^ highest (right-associative), then * and / (left-associative), then + and − (left-associative). The resulting postfix expression is''',
            'options': [
                'a b c d ^ ^ e * − f g h − / i * +',
                'a b c ^ d ^ e * − f g h − / i * +',
                'a b c d ^ ^ e * f g h − / i * + −',
                'a b c d ^ ^ e * − f g h − i * / +',
            ],
            'answer': 'A',
            'solution': '''**Concept.** When an operator arrives, pop operators of *higher* precedence, and of *equal* precedence only if the incoming operator is left-associative. `(` is pushed, `)` pops back to the matching `(`.

Trace (output | stack):
- a | ;  − | −;  b | −
- ^ : top − is lower → push | − ^;  c
- ^ : equal precedence but right-assoc → **do not pop**, push | − ^ ^;  d → a b c d
- * : pop ^, ^ (higher); − is lower → push | − *;  e → a b c d ^ ^ e
- + : pop * (higher) and − (equal, left-assoc) → a b c d ^ ^ e * − ; push +
- f | + ;  / : push | + /;  ( g − h ) → f g h −
- * : / has equal precedence, left-assoc → pop / → … f g h − / ; push *
- i, end: pop *, + → **a b c d ^ ^ e * − f g h − / i * +**

Option by option:
- (A) Correct.
- (B) treats ^ as left-associative: (b^c)^d instead of b^(c^d).
- (C) fails to pop − when + arrives, i.e. computes a − (… + …).
- (D) treats * and / as right-associative: f / ((g−h)·i).

**Trap:** right-associativity of ^ only affects ties between ^ operators; it is the left-associativity of +,− and *,/ that forces the pops on equal precedence.''',
            'verify': '''
prec = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
def topost(s, right=('^',)):
    out, st = [], []
    for c in s.replace(' ', ''):
        if c.isalpha(): out.append(c)
        elif c == '(': st.append(c)
        elif c == ')':
            while st[-1] != '(': out.append(st.pop())
            st.pop()
        else:
            while st and st[-1] != '(' and (prec[st[-1]] > prec[c] or
                    (prec[st[-1]] == prec[c] and c not in right)):
                out.append(st.pop())
            st.append(c)
    return ' '.join(out + st[::-1])
r = topost("a - b ^ c ^ d * e + f / (g - h) * i")
assert r == "a b c d ^ ^ e * - f g h - / i * +" and ANSWER == 'A'
assert topost("a - b ^ c ^ d * e + f / (g - h) * i", right=()) != r
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Queue using two stacks — cost',
            'text': '''A queue is implemented with two stacks IN and OUT. `enqueue(x)` pushes x on IN. `dequeue()` first checks OUT; **only if OUT is empty**, it pops every element of IN and pushes it onto OUT; then it pops OUT. Each individual push or pop counts as one stack operation (emptiness checks are free). Starting with both stacks empty, the following 14 operations are performed (E = enqueue the next integer 1, 2, 3, …; D = dequeue):
E E E D E E D D E D E E D E
The total number of stack operations performed is ______.''',
            'answer': '26',
            'solution': '''**Concept.** Each element costs 1 push on IN, and *if it is ever transferred* 1 pop from IN + 1 push on OUT, and *if dequeued* 1 pop from OUT. Elements still on IN at the end were never transferred.

Trace (IN | OUT, top on the right):
- E E E: IN [1 2 3] — 3 ops
- D: OUT empty → transfer 3 elements (6 ops) → OUT [3 2 1]; pop 1 (1 op)
- E E: IN [4 5] — 2 ops
- D: pop 2 (1); D: pop 3 (1) — OUT now empty
- E: IN [4 5 6] — 1 op
- D: transfer 3 (6 ops) → OUT [6 5 4]; pop 4 (1)
- E E: IN [7 8] — 2 ops; D: pop 5 (1); E: IN [7 8 9] — 1 op

Totals: 9 enqueue pushes + 6 transferred × 2 + 5 dequeue pops = 9 + 12 + 5 = **26**.

Dequeue order 1, 2, 3, 4, 5 confirms FIFO behaviour. Element 6 is left on OUT and 7, 8, 9 on IN.

**Amortised view:** every element costs at most 4 stack operations over its lifetime, so any sequence of m queue operations costs O(m) even though a single dequeue can cost Θ(n).

**Trap:** transferring on *every* dequeue (or moving elements back to IN afterwards) gives much larger counts; also do not forget that the transfer is 2 operations per element.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [6],
                    'label': 'OUT at the end',
                },
                {
                    'type': 'stack',
                    'values': [7, 8, 9],
                    'label': 'IN at the end',
                },
            ],
            'verify': '''
IN, OUT, c, k, got = [], [], 0, 0, []
for o in "E E E D E E D D E D E E D E".split():
    if o == 'E':
        k += 1; IN.append(k); c += 1
    else:
        if not OUT:
            while IN: OUT.append(IN.pop()); c += 2
        got.append(OUT.pop()); c += 1
assert got == [1, 2, 3, 4, 5] and c == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Monotonic stack — largest rectangle in a histogram',
            'text': 'The largest-rectangle algorithm below is run on bar heights h = [2, 5, 4, 6, 3, 1, 4] (each bar has width 1). A sentinel bar of height 0 is appended. Which of the following statements is/are TRUE?',
            'code': '''def largest(h):
    H, st, best, pops = h + [0], [], 0, 0
    for i, x in enumerate(H):
        while st and H[st[-1]] >= x:
            t = st.pop(); pops += 1
            w = i if not st else i - st[-1] - 1
            best = max(best, H[t] * w)
        st.append(i)
    return best, pops''',
            'options': [
                'The function returns pops = 7',
                'The function returns best = 12',
                'Exactly one rectangle (one choice of height and contiguous range) attains the maximum area',
                'When the bar of height 1 (index 5) is processed, exactly 3 bars are popped',
            ],
            'answer': ['A', 'B'],
            'solution': '''**Concept.** When bar t is popped, the current index i is the first bar to its right that is lower, and the new stack top is the nearest lower bar to its left; so H[t] × w is the largest rectangle using bar t as its *shortest* bar.

Trace (pops with their areas):
- i=2 (4): pop 5 (w 1) → 5
- i=4 (3): pop 6 (w 1) → 6; pop 4 (index 2, w = 4 − 0 − 1 = 3) → **12**
- i=5 (1): pop 3 (w = 5 − 0 − 1 = 4) → **12**; pop 2 (stack empty, w 5) → 10
- i=7 (sentinel 0): pop 4 (w 1) → 4; pop 1 (w 7) → 7

Option by option:
- (A) Every one of the 7 real bars is pushed once and popped once (the sentinel is pushed but never popped) → pops = 7. **TRUE.**
- (B) best = 12. **TRUE.**
- (C) Two different rectangles reach 12: height 4 over bars 1–3 and height 3 over bars 1–4. **FALSE.**
- (D) At i = 5 the stack holds the bars of heights 2 and 3 only (5, 6, 4 were already popped earlier), so exactly **2** bars are popped. **FALSE.**

**Trap:** in (D), counting all bars taller than 1 to the left (4 of them) instead of those still on the stack.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [2, 5, 4, 6, 3, 1, 4],
                    'label': 'h',
                    'highlight': [1, 2, 3, 4],
                    'caption': 'Bars 1–4: height 3 × width 4 = 12 (also height 4 × bars 1–3 = 12)',
                },
            ],
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

b, p = largest([2, 5, 4, 6, 3, 1, 4])
h = [2, 5, 4, 6, 3, 1, 4]; cnt = 0
for i in range(7):
    for j in range(i, 7):
        if min(h[i:j+1]) * (j - i + 1) == 12: cnt += 1
H = h + [0]; st = []; at5 = None
for i, x in enumerate(H):
    k = 0
    while st and H[st[-1]] >= x: st.pop(); k += 1
    if i == 5: at5 = k
    st.append(i)
res = [b == 12, cnt == 1, p == 7, at5 == 3]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Queue simulation — elimination game',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''from collections import deque
q = deque(range(1, 9))
out = []
while len(q) > 1:
    q.rotate(-3)
    out.append(q.pop())
print(out[:3], q[0])''',
            'options': ['`[4, 8, 5] 6`', '`[3, 6, 1] 4`', '`[5, 1, 4] 3`', '`[3, 6, 1] 7`'],
            'answer': 'D',
            'solution': '''**Concept.** `rotate(-3)` moves the three leftmost items to the right end; `pop()` then removes the rightmost item — which is the **third** of the three just moved. So each round eliminates every third person in a circle (a Josephus process with k = 3).

Circle 1..8, counting from the front:
- Round 1: [4 5 6 7 8 1 2 3] → remove **3**; front is 4.
- Round 2: count 4, 5, 6 → remove **6**; front 7.
- Round 3: count 7, 8, 1 → remove **1**; front 2.
- Round 4: 2, 4, 5 → remove 5. Round 5: 7, 8, 2 → remove 2. Round 6: 4, 7, 8 → remove 8. Round 7: 4, 7, 4 → remove 4.
- Survivor: **7**.

Elimination order 3, 6, 1, 5, 2, 8, 4 → printed `[3, 6, 1] 7` → (D).

Option by option:
- (A) uses `popleft()` instead of `pop()` (removes every 4th).
- (B) reports the last *eliminated* person (4) instead of the survivor.
- (C) rotates the wrong way (`rotate(3)`), counting backwards.

**Tip:** the Josephus recurrence J(n) = (J(n−1) + k) mod n with J(1) = 0 gives J(8) = 6 (0-based) → person 7 ✓.''',
            'verify': '''ANSWER = {'C': 'D', 'D': 'C'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == '[3, 6, 1] 7' and ANSWER == 'C'
j = 0
for n in range(2, 9): j = (j + 3) % n
assert j + 1 == 7
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort with an explicit stack',
            'text': 'The non-recursive quicksort below (Lomuto partition, last element as pivot) is run on `A = [5, 1, 6, 2, 7, 3, 4]`. The maximum number of (lo, hi) pairs present on the stack at any time is ______.',
            'code': '''def qsort(A):
    st = [(0, len(A) - 1)]
    while st:
        lo, hi = st.pop()
        if lo >= hi:
            continue
        p, i = A[hi], lo - 1
        for j in range(lo, hi):
            if A[j] <= p:
                i += 1
                A[i], A[j] = A[j], A[i]
        A[i + 1], A[hi] = A[hi], A[i + 1]
        st.append((lo, i))         # left part
        st.append((i + 2, hi))     # right part''',
            'run_code': False,
            'answer': '4',
            'solution': '''**Concept.** Each processed range is replaced on the stack by two sub-ranges (even empty ones, which are popped and discarded later). Because the *right* part is pushed last, it is handled first; the stack grows while right parts keep splitting.

Trace (stack shown bottom → top after each step):
- Pop (0,6), pivot 4: A = [1, 2, 3, **4**, 7, 6, 5]; push (0,2), (4,6) → 2 pairs.
- Pop (4,6) on [7, 6, 5], pivot 5: nothing ≤ 5 → A[4..6] = [**5**, 6, 7]; push (4,3), (5,6) → stack (0,2), (4,3), (5,6): 3 pairs.
- Pop (5,6) on [6, 7], pivot 7: 6 ≤ 7 → [6, **7**]; push (5,5), (7,6) → stack (0,2), (4,3), (5,5), (7,6): **4 pairs** (maximum).
- Pop (7,6), (5,5), (4,3): all trivial → stack (0,2).
- Pop (0,2) on [1, 2, 3], pivot 3: push (0,1), (3,2) → 2 pairs; pop (3,2) trivial.
- Pop (0,1), pivot 2: push (0,0), (2,1) → 2 pairs; both trivial.

Maximum stack size = **4**.

**Tip:** pushing the *larger* part first (so the smaller part is processed next) bounds the stack size by O(log n); this code ignores sizes, so on a bad input the stack can grow to Θ(n).

**Trap:** forgetting that empty ranges like (4,3) and (7,6) are also pushed.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['(0,2)', '(4,3)', '(5,5)', '(7,6)'],
                    'label': 'Stack at its peak',
                },
            ],
            'verify': '''
A = [5, 1, 6, 2, 7, 3, 4]; st = [(0, 6)]; mx = 1
while st:
    lo, hi = st.pop()
    if lo >= hi: continue
    p, i = A[hi], lo - 1
    for j in range(lo, hi):
        if A[j] <= p: i += 1; A[i], A[j] = A[j], A[i]
    A[i + 1], A[hi] = A[hi], A[i + 1]
    st.append((lo, i)); st.append((i + 2, hi)); mx = max(mx, len(st))
assert A == sorted(A) and mx == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Trees — spiral traversal with two stacks',
            'text': 'The BST below is traversed with two stacks S1 and S2. Initially S1 = [root]. Repeat until both are empty: (i) pop every node from S1, printing it and pushing its **left then right** child (if present) onto S2; (ii) pop every node from S2, printing it and pushing its **right then left** child onto S1. What is printed?',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        44,
                        [
                            19,
                            [
                                8,
                                [4],
                                None,
                            ],
                            [
                                27,
                                [23],
                                [35],
                            ],
                        ],
                        [
                            63,
                            [
                                51,
                                None,
                                [57],
                            ],
                            [
                                90,
                                [72],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'BST',
                },
            ],
            'options': [
                '44 19 63 90 51 27 8 4 23 35 57 72',
                '44 19 63 8 27 51 90 4 23 35 57 72',
                '44 63 19 8 27 51 90 72 57 35 23 4',
                '44 63 19 8 27 51 90 4 23 35 57 72',
            ],
            'answer': 'C',
            'solution': '''**Concept.** A stack reverses the order in which a level’s children were pushed, so alternating the two stacks (and the push order) prints the levels in alternating directions — a spiral (zigzag) level order.

- Phase S1: print **44**; push 19, 63 onto S2 (63 on top).
- Phase S2: pop 63 → print, push 90, 51 onto S1; pop 19 → print, push 27, 8 onto S1. S1 (bottom→top) = 90, 51, 27, 8. Printed: **63 19**.
- Phase S1: pop 8 (push 4), 27 (push 23, 35), 51 (push 57), 90 (push 72). Printed **8 27 51 90**; S2 = 4, 23, 35, 57, 72.
- Phase S2: pop 72, 57, 35, 23, 4 → printed **72 57 35 23 4** (leaves, nothing pushed).

Output: 44 63 19 8 27 51 90 72 57 35 23 4 → (C).

Option by option:
- (A) is a spiral that starts left-to-right on level 1 (push orders swapped).
- (B) is the plain level order (a queue, not two stacks).
- (D) reverses level 1 but forgets that level 3 is reversed too.

**Trap:** level 2 is printed left-to-right because it was pushed right-then-left onto S1, and a stack reverses that.''',
            'verify': '''ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    i = 1 if k < t[0] else 2; t[i] = ins(t[i], k); return t
t = None
for k in [44, 19, 63, 8, 27, 51, 90, 23, 35, 57, 72, 4]: t = ins(t, k)
s1, s2, out = [t], [], []
while s1 or s2:
    while s1:
        n = s1.pop(); out.append(n[0])
        for c in (n[1], n[2]):
            if c: s2.append(c)
    while s2:
        n = s2.pop(); out.append(n[0])
        for c in (n[2], n[1]):
            if c: s1.append(c)
assert ' '.join(map(str, out)) == "44 63 19 8 27 51 90 72 57 35 23 4"
assert ANSWER == 'B'
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'DFS with an explicit stack',
            'text': 'The following iterative DFS is run on the undirected graph below from A. Note that a vertex is marked visited when it is **popped**, and neighbours are pushed in alphabetical order. In what order are vertices appended to `vis`?',
            'code': '''def dfs(G, s):
    st, vis = [s], []
    while st:
        u = st.pop()
        if u in vis:
            continue
        vis.append(u)
        for v in sorted(G[u]):
            if v not in vis:
                st.append(v)
    return vis''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'E'],
                        ['B', 'D'],
                        ['B', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['E', 'F'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 2],
                        'E': [2, 1],
                        'F': [4, 0],
                    },
                },
            ],
            'options': ['A E F D B C', 'A E F D C B', 'A C F E B D', 'A B D F C E'],
            'answer': 'A',
            'solution': '''**Concept.** With a stack, the neighbour pushed *last* (alphabetically largest) is explored first, so this DFS follows the reverse alphabetical choice at each vertex. Marking on pop allows duplicates on the stack; stale copies are skipped.

Stack trace (top at right):
- [A] → pop A; push B, C, E → [B, C, E]
- pop E; push B, F → [B, C, B, F]
- pop F; push C, D → [B, C, B, C, D]
- pop D; push B → [B, C, B, C, B]
- pop B (all its neighbours visited) → [B, C, B, C]
- pop C → [B, C, B]; the remaining B, C, B are already visited and skipped.

Order: **A E F D B C** → (A).

Option by option:
- (B) results if vertices are marked when *pushed* (then C is popped before B at the end).
- (C) picks C before E at A, which this stack order never does.
- (D) is the *recursive* DFS with alphabetical order.

**Trap:** an iterative DFS is not automatically the same as the recursive one; push order and marking time both matter.''',
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

G = {'A':'BCE','B':'ADE','C':'AF','D':'BF','E':'ABF','F':'CDE'}
def rdfs(u, vis):
    vis.append(u)
    for v in sorted(G[u]):
        if v not in vis: rdfs(v, vis)
    return vis
def pushmark(s):
    st, seen, order = [s], {s}, []
    while st:
        u = st.pop(); order.append(u)
        for v in sorted(G[u]):
            if v not in seen: seen.add(v); st.append(v)
    return order
got = ' '.join(dfs(G, 'A'))
assert got == 'A E F D B C' and ANSWER == 'D'
assert ' '.join(rdfs('A', [])) == 'A B D F C E' and ' '.join(pushmark('A')) == 'A E F D C B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Linked lists — circular queue with tail pointer',
            'text': 'A queue is implemented as a circular singly linked list accessed only through a `tail` pointer (`tail.nxt` is the front). Consider the following program.',
            'code': '''class Node:
    def __init__(self, v):
        self.v, self.nxt = v, None

tail = None
def enq(v):
    global tail
    n = Node(v)
    if tail is None:
        n.nxt = n
    else:
        n.nxt = tail.nxt
        tail.nxt = n
    tail = n

def deq():
    global tail
    head = tail.nxt
    if head is tail:
        tail = None
    else:
        tail.nxt = head.nxt
    return head.v

for x in [4, 8, 15]:
    enq(x)
a = deq()
enq(16); enq(23)
b = deq() + deq()
enq(a + b)''',
            'text2': 'After the program finishes, which of the following statements is/are TRUE?',
            'options': [
                'A further call `deq()` would return 23',
                '`tail.nxt.v == 16`',
                '`tail.v == 27`',
                '`tail.nxt.nxt.v == 27`',
            ],
            'answer': ['B', 'C'],
            'solution': '''**Concept.** With only a tail pointer, both enqueue (insert after tail, then advance tail) and dequeue (unlink tail.nxt) are O(1); the front is always `tail.nxt`.

- enq 4, 8, 15 → circle 4 → 8 → 15 → (back to 4); tail = 15.
- `a = deq()` removes the front 4 → a = 4; circle 8 → 15.
- enq 16, 23 → 8 → 15 → 16 → 23; tail = 23.
- `deq() + deq()` = 8 + 15 = 23 = b; circle 16 → 23.
- enq(a + b) = enq(27) → 16 → 23 → 27; tail = 27.

Option by option:
- (A) The next dequeue returns the front, 16 — not 23. **FALSE.**
- (B) The front (`tail.nxt`) is 16. **TRUE.**
- (C) tail is the last enqueued node, 27. **TRUE.**
- (D) `tail.nxt.nxt` is the second element, 23. **FALSE.**

**Trap:** thinking that `a + b` is 4 + 8 = 12 — `b` is the sum of *two* dequeues (8 and 15).''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [16, 23, 27],
                    'circular': True,
                    'head': 'tail.nxt',
                    'caption': 'Final circular list (tail = node 27)',
                },
            ],
            'verify': '''_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

res = [tail.v == 27, tail.nxt.v == 16, tail.nxt.v == 23, tail.nxt.nxt.v == 27]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Dijkstra with a binary heap (lazy deletion)',
            'text': 'Dijkstra’s algorithm is implemented with Python’s `heapq` using *lazy deletion*: whenever a distance improves, a new (distance, vertex) entry is pushed and outdated entries are skipped when popped. It is run from S on the directed graph below. Counting the initial push of (0, S), the total number of `heappush` calls is ______.',
            'code': '''import heapq
def dijkstra(G, s):
    d = {v: float('inf') for v in G}
    d[s], pq = 0, [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du > d[u]:
            continue                 # stale entry
        for v, w in G[u]:
            if du + w < d[v]:
                d[v] = du + w
                heapq.heappush(pq, (d[v], v))
    return d''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['S', 'A', 4],
                        ['S', 'B', 1],
                        ['S', 'C', 6],
                        ['A', 'D', 3],
                        ['A', 'E', 8],
                        ['B', 'A', 2],
                        ['B', 'C', 3],
                        ['B', 'D', 7],
                        ['C', 'D', 1],
                        ['C', 'F', 9],
                        ['D', 'E', 2],
                        ['D', 'F', 6],
                        ['E', 'F', 1],
                    ],
                    'pos': {
                        'S': [0, 0.6],
                        'A': [2, 2.4],
                        'B': [2, 0.6],
                        'C': [2, -1.2],
                        'D': [4, 0.6],
                        'E': [6, 2.4],
                        'F': [6, -1.2],
                    },
                },
            ],
            'answer': '14',
            'solution': '''**Concept.** One push happens for the source plus one for *every successful relaxation*; the number of pushes is therefore 1 + (number of times some d[v] decreases).

- Pop S (0): A=4, B=1, C=6 → 3 pushes.
- Pop B (1): A=3 ✓, C=4 ✓, D=8 ✓ → 3 pushes.
- Pop A (3): D = min(8, 6) = 6 ✓, E = 11 ✓ → 2 pushes.
- Pop (4, A): stale (d[A] = 3) → skipped. Pop C (4): D = min(6, 5) = 5 ✓, F = 13 ✓ → 2.
- Pop D (5): E = min(11, 7) = 7 ✓, F = min(13, 11) = 11 ✓ → 2.
- Stale (6, C), (6, D) skipped. Pop E (7): F = min(11, 8) = 8 ✓ → 1.
- Pop (8, D): stale (ties are broken by vertex name). Pop F (8); the remaining entries (11, E), (11, F), (13, F) are stale.

Pushes = 1 + 3 + 3 + 2 + 2 + 2 + 1 = **14**. (Of these, 7 are popped as stale entries.)

Final distances: A 3, B 1, C 4, D 5, E 7, F 8.

**Trap:** answering |V| = 7 (one entry per vertex, as with a decrease-key heap). Lazy deletion may push up to |E| + 1 entries, giving O(|E| log |E|) time.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Distances after each valid pop',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'pushes'],
                    'row_labels': ['S', 'B', 'A', 'C', 'D', 'E'],
                    'rows': [
                        [0, 4, 1, 6, '∞', '∞', '∞', 3],
                        [0, 3, 1, 4, 8, '∞', '∞', 3],
                        [0, 3, 1, 4, 6, 11, '∞', 2],
                        [0, 3, 1, 4, 5, 11, 13, 2],
                        [0, 3, 1, 4, 5, 7, 11, 2],
                        [0, 3, 1, 4, 5, 7, 8, 1],
                    ],
                },
            ],
            'verify': '''
import heapq
G = {'S': [('A',4),('B',1),('C',6)], 'A': [('D',3),('E',8)],
     'B': [('A',2),('C',3),('D',7)], 'C': [('D',1),('F',9)],
     'D': [('E',2),('F',6)], 'E': [('F',1)], 'F': []}
cnt = [0]
_push = heapq.heappush
def counting_push(h, x):
    cnt[0] += 1; _push(h, x)
d = {v: float('inf') for v in G}; d['S'] = 0; pq = []
counting_push(pq, (0, 'S'))
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; counting_push(pq, (d[v], v))
assert d == dijkstra(G, 'S') == {'S':0,'A':3,'B':1,'C':4,'D':5,'E':7,'F':8}
assert cnt[0] == int(ANSWER)
''',
        },
    ],
}
