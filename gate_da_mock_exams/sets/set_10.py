# Set 10 — Elementary Sorting (selection, bubble, insertion sorts)

SET = {
    'number': 10,
    'title': 'Elementary Sorting',
    'difficulty': 'Moderate',
    'focus': 'selection, bubble, insertion sorts — passes, swaps, comparisons',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "PARTITIONS"
print(s[7:1:-2], s[::-4], s[-3:])''',
            'options': ['`OTTR SIA ONS`', '`OIT STA ONS`', '`OTT STA ONS`', '`OTT SIO NS`'],
            'answer': 'C',
            'solution': '''**Concept.** `s[start:stop:step]` with a negative step walks *leftwards* from `start` and stops *before* reaching `stop`. Omitted bounds with a negative step mean “from the last character down to the first”.

Index the string: P0 A1 R2 T3 I4 T5 I6 O7 N8 S9.

- `s[7:1:-2]` → indices 7, 5, 3 (index 1 is excluded) → O, T, T → `OTT`.
- `s[::-4]` → indices 9, 5, 1 → S, T, A → `STA`.
- `s[-3:]` → the last three characters, indices 7, 8, 9 → `ONS`.

`print` separates its arguments with one space, giving `OTT STA ONS`.

**Options.** (B) takes index 6 (I) instead of 5 — a step of −1 then −2 confusion. (A) wrongly includes the stop index 1 (R is at index 2, not 1, so it is doubly wrong). (D) starts `s[::-4]` from index 7 instead of 9.

**Trap:** the stop index is *never* included, whatever the sign of the step.''',
            'verify': "ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == 'OTT STA ONS'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Selection sort — swaps',
            'text': 'Selection sort is applied to the array below to sort it in ascending order. In pass i (i = 0, 1, …, n−2) the minimum of A[i..n−1] is located, and a swap is performed **only if** the minimum is not already at index i. The total number of swaps performed is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [34, 12, 45, 7, 23, 56, 18],
                    'label': 'A',
                    'caption': 'Input array A[0..6]',
                },
            ],
            'answer': '4',
            'solution': '''**Concept.** Selection sort always makes n−1 passes; a pass swaps only when the minimum of the unsorted suffix is not already in front.

Trace (sorted prefix grows by one each pass):

- i=0: min of whole array is 7 (index 3) → swap 34↔7 → 7 12 45 34 23 56 18 (swap 1).
- i=1: min of A[1..6] is 12, already at index 1 → no swap.
- i=2: min of A[2..6] is 18 → swap 45↔18 → 7 12 18 34 23 56 45 (swap 2).
- i=3: min is 23 → swap 34↔23 → 7 12 18 23 34 56 45 (swap 3).
- i=4: min is 34, already in place → no swap.
- i=5: min of {56, 45} is 45 → swap → 7 12 18 23 34 45 56 (swap 4).

Total swaps = **4**.

**Trap:** answering n−1 = 6 assumes every pass swaps. Selection sort performs *at most* n−1 swaps, which is why it is preferred when writes are expensive.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', 'swap?'],
                    'row_labels': ['i=0', 'i=1', 'i=2', 'i=3', 'i=4', 'i=5'],
                    'rows': [
                        [7, 12, 45, 34, 23, 56, 18, 'yes'],
                        [7, 12, 45, 34, 23, 56, 18, 'no'],
                        [7, 12, 18, 34, 23, 56, 45, 'yes'],
                        [7, 12, 18, 23, 34, 56, 45, 'yes'],
                        [7, 12, 18, 23, 34, 56, 45, 'no'],
                        [7, 12, 18, 23, 34, 45, 56, 'yes'],
                    ],
                },
            ],
            'verify': '''
a = [34, 12, 45, 7, 23, 56, 18]; sw = 0
for i in range(len(a) - 1):
    m = min(range(i, len(a)), key=lambda k: a[k])
    if m != i:
        a[i], a[m] = a[m], a[i]; sw += 1
assert a == sorted(a) and sw == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Bubble sort — early termination',
            'text': '''Bubble sort with an early-exit flag is run on the array
3, 9, 2, 11, 14, 6, 17, 20
In each pass adjacent pairs of the unsorted part are compared left to right and swapped if out of order; the algorithm stops after the first pass in which no swap occurs. How many passes are executed in total (including the final swap-free pass)?''',
            'options': ['3', '4', '5', '7'],
            'answer': 'B',
            'solution': '''**Concept.** Each bubble pass carries the largest remaining element to the end, but also moves every small element at most **one** position left. The number of passes needed equals the largest leftward distance any element must travel, plus one swap-free confirmation pass.

- Pass 1: 3 2 9 11 6 14 17 20 (swaps 9↔2 and 14↔6).
- Pass 2: 2 3 9 6 11 14 17 20 (swaps 3↔2, 11↔6).
- Pass 3: 2 3 6 9 11 14 17 20 (swap 9↔6). The array is now sorted, but the algorithm does not know that yet.
- Pass 4: no swap → stop.

Element 6 started at index 5 and must reach index 2 (3 steps left) → 3 sorting passes + 1 check = **4**.

**Options.** (A) forgets the confirming pass. (C) and (D) ignore the early exit (n−1 = 7 is the count for plain bubble sort).

**Tip:** “turtles” (small values near the end) govern bubble-sort passes; “rabbits” (large values near the front) move fast.''',
            'verify': '''
a = [3, 9, 2, 11, 14, 6, 17, 20]; n = len(a); passes = 0
for p in range(n - 1):
    passes += 1; s = False
    for j in range(n - 1 - p):
        if a[j] > a[j + 1]:
            a[j], a[j + 1] = a[j + 1], a[j]; s = True
    if not s: break
assert passes == 4 and ANSWER == 'B'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Insertion sort — shifts and inversions',
            'text': 'Standard insertion sort (shift larger elements one place right, then drop the key into the gap) sorts the array below into ascending order. The total number of element **shifts** (assignments of the form A[j+1] ← A[j]) is ______.',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [6, 2, 9, 4, 1, 7],
                    'label': 'A',
                    'caption': 'Input array',
                },
            ],
            'answer': '8',
            'solution': '''**Concept.** Every shift in insertion sort removes exactly one inversion (a pair i < j with A[i] > A[j]), and the algorithm stops when no inversions remain. So shifts = number of inversions.

Count inversions element by element (larger elements to the left of each):

- 6: none → 0
- 2: {6} → 1
- 9: none → 0
- 4: {6, 9} → 2
- 1: {6, 2, 9, 4} → 4
- 7: {9} → 1

Total = 0+1+0+2+4+1 = **8** shifts.

Cross-check by tracing: inserting 2 shifts 1; 9 shifts 0; 4 shifts 2 (9, 6); 1 shifts 4; 7 shifts 1 (9) — again 8.

**Trap:** do not confuse shifts with comparisons. Comparisons are higher (here 11) because a pass that stops on a smaller element still performs one failing comparison.''',
            'verify': '''
a = [6, 2, 9, 4, 1, 7]; sh = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0 and a[j] > key:
        a[j + 1] = a[j]; j -= 1; sh += 1
    a[j + 1] = key
assert sh == int(ANSWER) == 8
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression below is evaluated with an operand stack (all operands are single integers; `/` denotes integer division and the right operand is the one popped first).
6 2 3 + * 8 4 2 / − 3 * −
Which pair gives (value of the expression, maximum number of items on the stack at any time)?''',
            'options': ['(12, 3)', '(12, 4)', '(−12, 4)', '(18, 4)'],
            'answer': 'B',
            'solution': '''**Concept.** Push operands; on an operator pop the right operand, then the left one, and push the result.

- 6, 2, 3 → stack [6, 2, 3] (size 3)
- + → [6, 5]; * → [30]
- 8, 4, 2 → [30, 8, 4, 2] (size **4**, the maximum)
- / → 4/2 = 2 → [30, 8, 2]
- − → 8 − 2 = 6 → [30, 6]
- 3 → [30, 6, 3]; * → [30, 18]
- − → 30 − 18 = **12** → [12]

So the answer is (12, 4).

**Options.** (A) misses the moment when 8, 4, 2 sit on top of 30. (C) reverses the operand order of the last subtraction (18 − 30). (D) reports the intermediate 18 instead of the final result.

**Trap:** for non-commutative operators the *first* pop is the **right** operand.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [30, 8, 4, 2],
                    'label': 'Peak stack (size 4)',
                },
            ],
            'verify': '''ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)

S = []; mx = 0
for t in "6 2 3 + * 8 4 2 / - 3 * -".split():
    if t.isdigit(): S.append(int(t))
    else:
        b = S.pop(); a = S.pop()
        S.append({'+': a+b, '-': a-b, '*': a*b, '/': a//b}[t])
    mx = max(mx, len(S))
assert (S[0], mx) == (12, 4) and ANSWER == 'C'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search trees',
            'text': 'The keys 41, 23, 67, 15, 30, 52, 80, 27, 35, 74, 33 are inserted in this order into an initially empty binary search tree (no rebalancing). Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)',
            'options': [
                'The tree has exactly 4 leaves',
                'The post-order traversal begins 15, 27, 35',
                'The height of the tree is 4',
                'The in-order successor of 41 is 52',
            ],
            'answer': ['C', 'D'],
            'solution': '''**Concept.** Each key walks down from the root, going left if smaller and right otherwise, and is attached where it falls off.

Resulting tree: 41 has children 23 and 67; 23 → (15, 30); 30 → (27, 35); 35 → (33, –); 67 → (52, 80); 80 → (74, –).

- (A) Leaves are 15, 27, 33, 52, 74 — that is **5** leaves. **FALSE.**
- (B) Post-order = 15, 27, 33, 35, 30, 23, 52, 74, 80, 67, 41. It begins 15, 27, **33** (the child 33 is finished before its parent 35). **FALSE.**
- (C) Longest path 41→23→30→35→33 has **4 edges**. **TRUE.**
- (D) Successor of 41 = minimum of its right subtree = leftmost node under 67 = 52. **TRUE.**

**Trap:** in (B) students often list 35 before 33 because 35 was inserted first — post-order visits a node only after *both* of its subtrees.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        41,
                        [
                            23,
                            [15],
                            [
                                30,
                                [27],
                                [
                                    35,
                                    [33],
                                    None,
                                ],
                            ],
                        ],
                        [
                            67,
                            [52],
                            [
                                80,
                                [74],
                                None,
                            ],
                        ],
                    ],
                    'highlight': [41, 23, 30, 35, 33],
                    'caption': 'BST with its longest root-to-leaf path highlighted',
                },
            ],
            'verify': '''_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    i = 1 if k < t[0] else 2
    t[i] = ins(t[i], k); return t
t = None
for k in [41, 23, 67, 15, 30, 52, 80, 27, 35, 74, 33]: t = ins(t, k)
h = lambda t: -1 if t is None else 1 + max(h(t[1]), h(t[2]))
lv = lambda t: 0 if t is None else (1 if t[1] is None and t[2] is None
                                    else lv(t[1]) + lv(t[2]))
post = lambda t: [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
assert h(t) == 4 and lv(t) == 5 and post(t)[:3] == [15, 27, 33]
assert sorted(ANSWER) == ['A', 'C']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'The keys 15, 22, 9, 36, 3, 29, 44, 10 are inserted into an initially empty hash table with 7 slots (indices 0–6) using h(k) = k mod 7 and separate chaining. Which of the following correctly describes the final table?',
            'options': [
                'Longest chain has length 3; 4 slots are empty',
                'Longest chain has length 4; 3 slots are empty',
                'Longest chain has length 4; 4 slots are empty',
                'Longest chain has length 3; 3 slots are empty',
            ],
            'answer': 'C',
            'solution': '''**Concept.** With chaining every key goes to the list at slot h(k); collisions just lengthen the list.

- 15 mod 7 = 1, 22 mod 7 = 1, 36 mod 7 = 1, 29 mod 7 = 1 → slot 1 gets **4** keys.
- 9 mod 7 = 2, 44 mod 7 = 2 → slot 2 gets 2 keys.
- 3 mod 7 = 3, 10 mod 7 = 3 → slot 3 gets 2 keys.

Occupied slots: 1, 2, 3. Empty slots: 0, 4, 5, 6 → **4** empty.

So the longest chain has length 4 and 4 slots are empty → (C).

**Options.** (A)/(D) miss that 29 = 4·7 + 1 also lands in slot 1. (B) counts occupied slots instead of empty ones.

**Tip:** keys that differ by a multiple of m always collide — here 15, 22, 29, 36 form an arithmetic progression with difference 7.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        1: [15, 22, 36, 29],
                        2: [9, 44],
                        3: [3, 10],
                    },
                    'caption': 'Final chained table (new keys appended at the tail)',
                },
            ],
            'verify': '''
T = {}
for k in [15, 22, 9, 36, 3, 29, 44, 10]: T.setdefault(k % 7, []).append(k)
assert max(len(v) for v in T.values()) == 4 and 7 - len(T) == 4
assert ANSWER == 'C'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search — probe counts',
            'text': 'Binary search is performed on the sorted array A[0..14] shown below using mid = ⌊(lo + hi)/2⌋, starting with lo = 0, hi = 14. Each examination of A[mid] counts as one probe. For which of the following keys does a **successful** search take exactly 4 probes?',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [4, 9, 13, 18, 22, 27, 31, 36, 40, 45, 52, 58, 63, 70, 77],
                    'label': 'A',
                    'caption': 'Sorted array of 15 keys',
                },
            ],
            'options': ['70', '22', '36', '4'],
            'answer': ['B', 'D'],
            'solution': '''**Concept.** For n = 2^{4} − 1 = 15 elements the binary-search decision tree is perfect: one key at depth 1, two at depth 2, four at depth 3 and eight at depth 4.

- Probe 1: index 7 (36).
- Probe 2: index 3 (18) or 11 (58).
- Probe 3: index 1 (9), 5 (27), 9 (45), 13 (70).
- Probe 4: even indices 0, 2, 4, …, 14 → 4, 13, 22, 31, 40, 52, 63, 77.

Option by option:
- (A) 70 is at index 13 → 7 → 11 → 13: 3 probes. **FALSE.**
- (B) 22 is at index 4 → 7 → 3 → 5 → 4: 4 probes. **TRUE.**
- (C) 36 is found on the very first probe. **FALSE.**
- (D) 4 is at index 0 → 4 probes (7 → 3 → 1 → 0). **TRUE.**

**Tip:** with n = 2^{k} − 1, exactly half the keys (the even indices) need the maximum k probes.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A = [4, 9, 13, 18, 22, 27, 31, 36, 40, 45, 52, 58, 63, 70, 77]
def probes(x):
    lo, hi, c = 0, 14, 0
    while lo <= hi:
        m = (lo + hi) // 2; c += 1
        if A[m] == x: return c
        if A[m] < x: lo = m + 1
        else: hi = m - 1
got = [k for L, k in zip('ABCD', [4, 22, 36, 70]) if probes(k) == 4]
assert got == [4, 22] and sorted(ANSWER) == ['A', 'B']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Graph traversal — BFS',
            'text': 'Breadth-first search is run on the undirected graph below starting at vertex A. Whenever a vertex is dequeued, its unvisited neighbours are enqueued in **alphabetical order**. Which of the following is the order in which vertices are dequeued?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['D', 'E'],
                        ['D', 'G'],
                        ['E', 'F'],
                        ['C', 'F'],
                        ['G', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [4, 2],
                        'D': [0, 0],
                        'E': [2, 1],
                        'F': [4, 0],
                        'G': [2, -0.5],
                    },
                },
            ],
            'options': ['A B C F E D G', 'A D B G E C F', 'A B D E C G F', 'A B D C E G F'],
            'answer': 'D',
            'solution': '''**Concept.** BFS dequeues vertices level by level; within a level the order is the order in which they were enqueued.

- Dequeue A → enqueue B, D. Queue: B D
- Dequeue B → neighbours A, C, E; enqueue C, E. Queue: D C E
- Dequeue D → neighbours A, E, G; only G is new. Queue: C E G
- Dequeue C → neighbour F is new. Queue: E G F
- Dequeue E, then G, then F (nothing new).

Order: **A B D C E G F** → (D).

**Options.** (A) is the DFS order (alphabetical). (C) puts E before C, i.e. treats E as a neighbour of D enqueued earlier — but E was already enqueued by B *after* C. (B) starts with D, violating alphabetical order.

**Trap:** a vertex is marked when it is *enqueued*, not when dequeued; E is not re-added by D.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['D', 'E'],
                        ['D', 'G'],
                        ['E', 'F'],
                        ['C', 'F'],
                        ['G', 'F'],
                    ],
                    'highlight_edges': [
                        ['A', 'B'],
                        ['A', 'D'],
                        ['B', 'C'],
                        ['B', 'E'],
                        ['D', 'G'],
                        ['C', 'F'],
                    ],
                    'pos': {
                        'A': [0, 2],
                        'B': [2, 2],
                        'C': [4, 2],
                        'D': [0, 0],
                        'E': [2, 1],
                        'F': [4, 0],
                        'G': [2, -0.5],
                    },
                    'caption': 'BFS tree (highlighted edges)',
                },
            ],
            'verify': '''ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)

from collections import deque
G = {'A':'BD','B':'ACE','C':'BF','D':'AEG','E':'BDF','F':'CEG','G':'DF'}
seen = {'A'}; q = deque('A'); out = []
while q:
    u = q.popleft(); out.append(u)
    for v in sorted(G[u]):
        if v not in seen: seen.add(v); q.append(v)
assert ' '.join(out) == 'A B D C E G F' and ANSWER == 'B'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Python — sort vs sorted, aliasing',
            'text': 'Consider the following Python code.',
            'code': '''a = [5, 3, 8, 1]
b = a
c = a[:]
d = a.sort(reverse=True)
e = sorted(c, key=lambda x: -x)''',
            'text2': 'After it executes, which of the following expressions evaluate to `True`?',
            'options': ['`c[0] == 8`', '`b[0] == 8`', '`e == b`', '`d is None`'],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept.** `list.sort()` sorts *in place* and returns `None`; `sorted()` builds and returns a *new* list. `b = a` creates an alias, `a[:]` a shallow copy.

- After `a.sort(reverse=True)`, the list object shared by `a` and `b` is [8, 5, 3, 1].
- `c` is a separate copy taken *before* sorting, so it is still [5, 3, 8, 1].
- `d` receives the return value of `sort`, which is `None`.
- `e` sorts the copy by key −x, i.e. descending → [8, 5, 3, 1].

Option by option:
- (A) `c[0]` is 5 — the copy is untouched. **False.**
- (B) `b[0]` is 8 because `b` aliases the sorted list. **True.**
- (C) `e` = [8, 5, 3, 1] = `b` (equal contents). **True.**
- (D) `d is None`. **True.**

**Trap:** writing `x = x.sort()` is a classic bug that silently replaces the list by `None`.''',
            'verify': '''_m = {'C': 'D', 'D': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

assert b[0] == 8 and c[0] != 8 and d is None and e == b
assert sorted(ANSWER) == ['A', 'C', 'D']
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Insertion sort — intermediate state',
            'text': 'The array below is sorted in ascending order by the insertion sort shown. What is the content of A immediately after the outer loop has finished the iteration with **i = 3**?',
            'code': '''def insertion_sort(A):
    for i in range(1, len(A)):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key''',
            'run_code': False,
            'diagrams': [
                {
                    'type': 'array',
                    'values': [21, 8, 30, 14, 5, 26, 11, 17],
                    'label': 'A',
                    'caption': 'Initial array',
                },
            ],
            'options': [
                '8, 14, 21, 30, 5, 26, 11, 17',
                '8, 5, 14, 11, 17, 21, 26, 30',
                '5, 8, 14, 21, 30, 26, 11, 17',
                '5, 8, 11, 14, 21, 26, 30, 17',
            ],
            'answer': 'A',
            'solution': '''**Concept.** After the iteration with index i, insertion sort guarantees that the prefix A[0..i] is a sorted arrangement of the *original* first i+1 elements; the suffix is untouched.

Trace:

- i = 1 (key 8): 21 > 8 → shift → 8, 21, 30, 14, 5, 26, 11, 17
- i = 2 (key 30): 21 > 30 is false → no change
- i = 3 (key 14): shift 30, then 21; 8 > 14 false → 8, 14, 21, 30, 5, 26, 11, 17

So the array is **8, 14, 21, 30, 5, 26, 11, 17** → (A).

Option by option:
- (A) Correct: the prefix is a sorted version of {21, 8, 30, 14} and the tail is unchanged.
- (B) is the state after three passes of **bubble** sort (the three largest, 21, 26, 30, are parked at the end).
- (C) is one iteration too far (after i = 4, key 5 has been inserted).
- (D) is the state after three passes of **selection** sort (the three global minima 5, 8, 11 are in front). Insertion sort cannot bring 5 forward before it reaches index 4.

**Tip:** a quick fingerprint test — selection sort’s prefix contains the *global* minima, bubble sort’s suffix contains the *global* maxima, insertion sort’s prefix contains the *original* first elements in sorted order.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Insertion-sort trace',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', 'i=1', 'i=2', 'i=3'],
                    'rows': [
                        [21, 8, 30, 14, 5, 26, 11, 17],
                        [8, 21, 30, 14, 5, 26, 11, 17],
                        [8, 21, 30, 14, 5, 26, 11, 17],
                        [8, 14, 21, 30, 5, 26, 11, 17],
                    ],
                    'highlight': [
                        [1, 0],
                        [3, 1],
                    ],
                },
            ],
            'verify': '''ANSWER = {'D': 'A', 'A': 'D'}.get(ANSWER, ANSWER)

def ins(A, last):
    A = A[:]
    for i in range(1, last + 1):
        key = A[i]; j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]; j -= 1
        A[j + 1] = key
    return A
def sel(A, k):
    A = A[:]
    for i in range(k):
        m = min(range(i, len(A)), key=lambda t: A[t]); A[i], A[m] = A[m], A[i]
    return A
def bub(A, k):
    A = A[:]
    for p in range(k):
        for j in range(len(A) - 1 - p):
            if A[j] > A[j + 1]: A[j], A[j + 1] = A[j + 1], A[j]
    return A
X = [21, 8, 30, 14, 5, 26, 11, 17]
assert ins(X, 3) == [8, 14, 21, 30, 5, 26, 11, 17]
assert sel(X, 3) == [5, 8, 11, 14, 21, 26, 30, 17]
assert bub(X, 3) == [8, 5, 14, 11, 17, 21, 26, 30]
assert ins(X, 4) == [5, 8, 14, 21, 30, 26, 11, 17]
assert ANSWER == 'D'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Bubble sort — comparison count',
            'text': 'The following bubble sort (with a shrinking range and an early-exit flag) is called on `A = [2, 6, 1, 5, 9, 3, 10, 12]`. The total number of times the comparison `A[j] > A[j + 1]` is evaluated is ______.',
            'code': '''def bubble(A):
    n = len(A)
    for p in range(n - 1):
        swapped = False
        for j in range(n - 1 - p):
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swapped = True
        if not swapped:
            break''',
            'run_code': False,
            'answer': '22',
            'solution': '''**Concept.** Pass p (0-based) compares positions 0..n−2−p, i.e. n−1−p comparisons, whether or not it swaps. The total is therefore determined by *how many passes run*.

n = 8. Trace:

- Pass p=0 (7 comparisons): 2<6 keep; 6>1 swap; 6>5 swap; 6<9 keep; 9>3 swap; 9<10 keep; 10<12 keep → **2 1 5 6 3 9 10 12** (12 is in its final place).
- Pass p=1 (6 comparisons): 1 2 5 3 6 9 10 12 (swaps 2↔1, 6↔3).
- Pass p=2 (5 comparisons): 1 2 3 5 6 9 10 12 (swap 5↔3).
- Pass p=3 (4 comparisons): no swap → exit.

Total comparisons = 7 + 6 + 5 + 4 = **22**.

Why 4 passes? Element 3 starts at index 5 and must reach index 2; each pass moves a small element left by at most one place, so 3 passes are needed to sort plus one swap-free pass to detect it.

**Trap:** counting only swaps (6) or assuming the full n(n−1)/2 = 28 comparisons. The early exit saves 3 + 2 + 1 = 6 comparisons here.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', 'comps'],
                    'row_labels': ['p=0', 'p=1', 'p=2', 'p=3'],
                    'rows': [
                        [2, 1, 5, 6, 3, 9, 10, 12, 7],
                        [1, 2, 5, 3, 6, 9, 10, 12, 6],
                        [1, 2, 3, 5, 6, 9, 10, 12, 5],
                        [1, 2, 3, 5, 6, 9, 10, 12, 4],
                    ],
                },
            ],
            'verify': '''
A = [2, 6, 1, 5, 9, 3, 10, 12]; n = len(A); c = 0
for p in range(n - 1):
    s = False
    for j in range(n - 1 - p):
        c += 1
        if A[j] > A[j + 1]:
            A[j], A[j + 1] = A[j + 1], A[j]; s = True
    if p == 0: assert A == [2, 1, 5, 6, 3, 9, 10, 12]
    if not s: break
assert c == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Sorting — stability',
            'text': '''Five records (key, tag) are stored in a list in the order
(6, p), (4, q), (6, r), (2, s), (9, t)
and are sorted by **key only** (ascending). Consider these four procedures:
- Selection sort: for i = 0..n−2, find the *first* index m of the minimum key in positions i..n−1 (strict `<`) and swap positions i and m.
- Insertion sort that shifts while `A[j].key > key`.
- Bubble sort (n−1 full passes) that swaps adjacent records while `A[j].key >= A[j+1].key`.
- Python’s `sorted(R, key=lambda x: x[0])`.

Which of the following statements is/are TRUE?''',
            'options': [
                'Selection sort outputs (6, r) before (6, p)',
                'The `>=` bubble sort outputs (6, r) before (6, p)',
                'Insertion sort outputs (6, p) before (6, r)',
                '`sorted` outputs (6, r) before (6, p)',
            ],
            'answer': ['A', 'C'],
            'solution': '''**Concept.** A sort is *stable* if records with equal keys keep their input order. Swapping non-adjacent elements (selection sort) or swapping equal neighbours (a `>=` bubble sort) can break stability — but whether it *actually* happens depends on the input.

**Selection sort trace:**
- i=0: minimum key 2 at index 3 → swap (6,p) with (2,s): (2,s) (4,q) (6,r) (6,p) (9,t). The long-distance swap has jumped (6,p) **over** (6,r).
- i=1: (4,q) already minimal. i=2: first minimum key 6 is (6,r) at index 2 → no swap. i=3: no swap.
Output: (2,s) (4,q) **(6,r) (6,p)** (9,t) → (A) **TRUE**.

**Insertion sort** with strict `>` never moves a record past an equal key, so it is stable: (6,p) stays ahead of (6,r) → (C) **TRUE**.

**`>=` bubble sort:** equal neighbours are swapped every time they meet. Pass 1: (6,p)>(4,q) swap; (6,p)≥(6,r) **swap** → r ahead; (6,p)>(2,s) swap; … giving (4,q) (6,r) (2,s) (6,p) (9,t). Pass 2: (6,r)>(2,s) swap; (6,r)≥(6,p) **swap again** → p ahead: (4,q) (2,s) (6,p) (6,r) (9,t). Passes 3–4 only move (2,s) to the front. The two 6s were swapped an *even* number of times, so the final order is (6,p) (6,r) → (B) **FALSE** (the algorithm is unstable in general, but not on this input).

**`sorted`** uses Timsort, which is guaranteed stable → (6,p) first → (D) **FALSE**.

**Trap:** “unstable algorithm” does not mean “always reorders equal keys” — always trace.''',
            'verify': '''_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

import operator as op
R = [(6,'p'),(4,'q'),(6,'r'),(2,'s'),(9,'t')]
def sel(b):
    b = b[:]
    for i in range(len(b) - 1):
        m = i
        for j in range(i + 1, len(b)):
            if b[j][0] < b[m][0]: m = j
        b[i], b[m] = b[m], b[i]
    return b
def ins(b):
    b = b[:]
    for i in range(1, len(b)):
        k = b[i]; j = i - 1
        while j >= 0 and b[j][0] > k[0]: b[j + 1] = b[j]; j -= 1
        b[j + 1] = k
    return b
def bub(b):
    b = b[:]
    for p in range(len(b) - 1):
        for j in range(len(b) - 1 - p):
            if b[j][0] >= b[j + 1][0]: b[j], b[j + 1] = b[j + 1], b[j]
    return b
first6 = lambda L: [t for k, t in L if k == 6][0]
res = [first6(sel(R)) == 'r', first6(ins(R)) == 'p',
       first6(bub(R)) == 'r', first6(sorted(R, key=lambda x: x[0])) == 'r']
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — bubble passes and copying',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''def pass_k(a, k):
    a = a[:]
    for p in range(k):
        for j in range(len(a) - 1 - p):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

data = [7, 3, 9, 1, 6, 2]
r = pass_k(data, 2)
print(r, data[0])''',
            'options': [
                '`[3, 1, 6, 2, 7, 9] 7`',
                '`[3, 1, 6, 2, 7, 9] 3`',
                '`[3, 7, 1, 6, 2, 9] 7`',
                '`[1, 3, 2, 6, 7, 9] 7`',
            ],
            'answer': 'A',
            'solution': '''**Concept.** Two things are tested: (i) what k bubble passes do, and (ii) that `a = a[:]` rebinds the *local* name to a copy, so the caller’s list is untouched.

**Pass p = 0** (j = 0..4) on 7 3 9 1 6 2:
- 7>3 swap → 3 7 9 1 6 2; 7<9 keep; 9>1 swap → 3 7 1 9 6 2; 9>6 swap → 3 7 1 6 9 2; 9>2 swap → **3 7 1 6 2 9**.

**Pass p = 1** (j = 0..3) on 3 7 1 6 2 9:
- 3<7 keep; 7>1 swap → 3 1 7 6 2 9; 7>6 swap → 3 1 6 7 2 9; 7>2 swap → **3 1 6 2 7 9**.

`r` = [3, 1, 6, 2, 7, 9]. Because the function sorted a copy, `data` is still [7, 3, 9, 1, 6, 2] and `data[0]` is **7**.

Option by option:
- (A) Correct.
- (B) assumes the function mutated `data` (it would if the line `a = a[:]` were absent).
- (C) is the result after only one pass (off-by-one on `range(k)`).
- (D) is the result after three passes.

**Tip:** after k bubble passes the last k positions hold the k largest values in order — here 7, 9 — a quick sanity check on the options.''',
            'verify': "assert OUTPUT.strip() == '[3, 1, 6, 2, 7, 9] 7' and ANSWER == 'A'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition swaps',
            'text': 'The quicksort below (Lomuto partition, last element as pivot) is called as `quicksort(A, 0, 7)` on `A = [12, 5, 17, 3, 20, 9, 14, 10]`. Every execution of a swap statement is counted, **including** swaps of an element with itself. The total number of swaps executed is ______.',
            'code': '''def quicksort(A, lo, hi):
    if lo < hi:
        pivot, i = A[hi], lo - 1
        for j in range(lo, hi):
            if A[j] <= pivot:
                i += 1
                A[i], A[j] = A[j], A[i]      # swap 1
        A[i + 1], A[hi] = A[hi], A[i + 1]    # swap 2
        quicksort(A, lo, i)
        quicksort(A, i + 2, hi)''',
            'run_code': False,
            'answer': '13',
            'solution': '''**Concept.** In one Lomuto partition of A[lo..hi], swap 1 runs once for every element ≤ pivot (among A[lo..hi−1]) and swap 2 runs exactly once. So a call contributes (number of elements ≤ pivot) + 1 swaps; calls on ranges of size ≤ 1 contribute nothing.

Trace of the recursion:

- quicksort(0,7), pivot 10: elements ≤ 10 are 5, 3, 9 → 3 + 1 = **4** swaps → [5, 3, 9, **10**, 20, 17, 14, 12].
- quicksort(0,2) on [5, 3, 9], pivot 9: 5 and 3 are ≤ 9 → 2 + 1 = **3** swaps (all are self-swaps) → [5, 3, 9].
- quicksort(0,1) on [5, 3], pivot 3: none ≤ 3 → **1** swap → [3, 5].
- quicksort(4,7) on [20, 17, 14, 12], pivot 12: none ≤ 12 → **1** swap → [12, 17, 14, 20].
- quicksort(5,7) on [17, 14, 20], pivot 20: 17, 14 ≤ 20 → 2 + 1 = **3** swaps → unchanged.
- quicksort(5,6) on [17, 14], pivot 14: **1** swap → [14, 17].

Total = 4 + 3 + 1 + 1 + 3 + 1 = **13**.

**Trap:** forgetting the self-swaps (when i = j) or the final pivot swap of each call; also note that when the pivot is the maximum of its range, *every* element triggers swap 1.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Partition calls',
                    'col_labels': ['range', 'pivot', '≤ pivot', 'swaps'],
                    'rows': [
                        ['0..7', 10, 3, 4],
                        ['0..2', 9, 2, 3],
                        ['0..1', 3, 0, 1],
                        ['4..7', 12, 0, 1],
                        ['5..7', 20, 2, 3],
                        ['5..6', 14, 0, 1],
                    ],
                },
            ],
            'verify': '''
cnt = [0]
def qs(A, lo, hi):
    if lo < hi:
        p, i = A[hi], lo - 1
        for j in range(lo, hi):
            if A[j] <= p:
                i += 1; A[i], A[j] = A[j], A[i]; cnt[0] += 1
        A[i + 1], A[hi] = A[hi], A[i + 1]; cnt[0] += 1
        qs(A, lo, i); qs(A, i + 2, hi)
A = [12, 5, 17, 3, 20, 9, 14, 10]; qs(A, 0, 7)
assert A == sorted(A) and cnt[0] == int(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Merge sort — comparisons',
            'text': '''Top-down merge sort (split a list of length n into the first ⌊n/2⌋ elements and the rest) is applied to
4, 11, 2, 9, 15, 6, 1, 13
The merge step compares the front elements of the two runs, outputs the smaller, and stops comparing as soon as one run is exhausted (the rest of the other run is copied without comparisons). The total number of element comparisons over the whole sort is ______.''',
            'answer': '16',
            'solution': '''**Concept.** Merging runs of lengths p and q costs between min(p, q) and p+q−1 comparisons: fewer when one run empties early.

Level by level (bottom-up view of the recursion):

- Pairs: [4]+[11], [2]+[9], [15]+[6], [1]+[13] → 1 comparison each = **4**.
- Merge [4, 11] with [2, 9]: 2<4 → 2; 4<9 → 4; 9<11 → 9; right run empty → copy 11. **3** comparisons → [2, 4, 9, 11].
- Merge [6, 15] with [1, 13]: 1; 6; 13; then copy 15. **3** comparisons → [1, 6, 13, 15].
- Final merge [2, 4, 9, 11] with [1, 6, 13, 15]: 1, 2, 4, 6, 9, 11 are output after **6** comparisons; the left run is now empty and 13, 15 are copied.

Total = 4 + 3 + 3 + 6 = **16**.

Bounds check: the worst case for n = 8 is 1·4 + 3·2 + 7 = 17, the best case is 4 + 2·2 + 4 = 12; 16 lies between.

**Trap:** using the formula n log₂ n − n + 1 = 17 blindly — that is only the worst case.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Every merge performed',
                    'col_labels': ['left run', 'right run', 'result', 'comps'],
                    'rows': [
                        ['4', '11', '4 11', 1],
                        ['2', '9', '2 9', 1],
                        ['15', '6', '6 15', 1],
                        ['1', '13', '1 13', 1],
                        ['4 11', '2 9', '2 4 9 11', 3],
                        ['6 15', '1 13', '1 6 13 15', 3],
                        ['2 4 9 11', '1 6 13 15', '1 2 4 6 9 11 13 15', 6],
                    ],
                },
            ],
            'verify': '''
def ms(a):
    if len(a) <= 1: return a, 0
    m = len(a) // 2
    L, c1 = ms(a[:m]); R, c2 = ms(a[m:])
    out, i, j, c = [], 0, 0, 0
    while i < len(L) and j < len(R):
        c += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:], c + c1 + c2
assert ms([4, 11, 2, 9, 15, 6, 1, 13])[1] == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Heaps — bottom-up build-heap',
            'text': 'The array A = [12, 5, 19, 3, 8, 25, 14, 1, 7] (0-indexed, drawn below as a complete binary tree) is converted into a **max-heap** by the bottom-up method: sift-down is called for i = ⌊n/2⌋−1 down to 0; sift-down swaps a node with its larger child while that child is larger. Which of the following statements is/are TRUE?',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [12, 5, 19, 3, 8, 25, 14, 1, 7],
                    'caption': 'Initial array viewed as a complete binary tree',
                },
            ],
            'options': [
                'If one delete-max is then performed (move last element to the root and sift down), the array becomes 19, 8, 14, 7, 5, 12, 1, 3',
                'Exactly 5 swaps are performed during the build',
                'In the resulting heap the children of the root are 8 and 19',
                'In the resulting heap, key 3 is at index 8',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept.** Build-heap sifts down each internal node, starting from the last internal node (index ⌊9/2⌋−1 = 3).

- i=3 (3): children 1, 7 → swap with 7 (**swap 1**). A = 12 5 19 7 8 25 14 1 3
- i=2 (19): children 25, 14 → swap with 25 (**swap 2**). A = 12 5 25 7 8 19 14 1 3
- i=1 (5): children 7, 8 → swap with 8 (**swap 3**); index 4 is a leaf. A = 12 8 25 7 5 19 14 1 3
- i=0 (12): children 8, 25 → swap with 25 (**swap 4**); now at index 2, children 19, 14 → swap with 19 (**swap 5**). A = **25 8 19 7 5 12 14 1 3**

Option by option:
- (A) Delete-max: move 3 to the root → 3 8 19 7 5 12 14 1; swap with 19 → index 2; children 12, 14 → swap with 14 → 19 8 14 7 5 12 **3 1**. The option has the last two reversed (it forgets that 3 moved down to index 6 while 1 stayed at index 7). **FALSE.**
- (B) Five swaps in total. **TRUE.**
- (C) Root 25 has children A[1] = 8 and A[2] = 19. **TRUE.**
- (D) Key 3 sits at index 8 (a leaf). **TRUE.**

**Trap:** in sift-down, keep going after the first swap — 12 had to fall two levels.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [25, 8, 19, 7, 5, 12, 14, 1, 3],
                    'caption': 'Max-heap after build-heap',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

sw = [0]
def sift(a, i, n):
    while True:
        l, r, m = 2*i + 1, 2*i + 2, i
        if l < n and a[l] > a[m]: m = l
        if r < n and a[r] > a[m]: m = r
        if m == i: return
        a[i], a[m] = a[m], a[i]; sw[0] += 1; i = m
a = [12, 5, 19, 3, 8, 25, 14, 1, 7]
for i in range(len(a)//2 - 1, -1, -1): sift(a, i, len(a))
built_swaps = sw[0]
b = a[:]; b[0] = b.pop(); sift(b, 0, len(b))
res = [a[1:3] == [8, 19], built_swaps == 5, a.index(3) == 8,
       b == [19, 8, 14, 7, 5, 12, 1, 3]]
assert [L for L, ok in zip('ABCD', res) if ok] == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra relaxations',
            'text': 'Dijkstra’s algorithm is run from source S on the directed graph below. Initially d[S] = 0 and all other d-values are ∞. Count every time some d[v] is **strictly decreased** during relaxation (the first change from ∞ also counts). The total count is ______.',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['B', 'A', 3],
                        ['B', 'C', 8],
                        ['A', 'C', 2],
                        ['A', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'E', 9],
                        ['D', 'E', 3],
                        ['B', 'E', 15],
                    ],
                    'pos': {
                        'S': [0, 1.2],
                        'A': [2, 2.4],
                        'B': [2, 0],
                        'C': [3.5, 1.2],
                        'D': [5, 2.4],
                        'E': [6.5, 1.2],
                    },
                },
            ],
            'answer': '10',
            'solution': '''**Concept.** Dijkstra extracts the vertex with the smallest tentative distance and relaxes its outgoing edges; a relaxation *succeeds* when d[u] + w < d[v].

- Extract S (0): A = 7, B = 2 → **2** decreases.
- Extract B (2): A = min(7, 5) = 5 ✓, C = 10 ✓, E = 17 ✓ → **3**.
- Extract A (5): C = min(10, 7) = 7 ✓, D = 11 ✓ → **2**.
- Extract C (7): D = min(11, 8) = 8 ✓, E = min(17, 16) = 16 ✓ → **2**.
- Extract D (8): E = min(16, 11) = 11 ✓ → **1**.
- Extract E (11): no outgoing edges.

Total = 2 + 3 + 2 + 2 + 1 = **10**.

Final distances: A 5, B 2, C 7, D 8, E 11 (path S→B→A→C→D→E).

**Trap:** E is improved three times (17 → 16 → 11) and D twice (11 → 8) — students who only record final values or skip the initial ∞ → finite updates undercount.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'd-values after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, 10, '∞', 17],
                        [0, 5, 2, 7, 11, 17],
                        [0, 5, 2, 7, 8, 16],
                        [0, 5, 2, 7, 8, 11],
                    ],
                },
            ],
            'verify': '''
G = {'S': [('A',7),('B',2)], 'B': [('A',3),('C',8),('E',15)],
     'A': [('C',2),('D',6)], 'C': [('D',1),('E',9)], 'D': [('E',3)], 'E': []}
INF = float('inf'); d = {v: INF for v in G}; d['S'] = 0; done = set(); dec = 0
while len(done) < len(G):
    u = min((v for v in G if v not in done), key=lambda v: d[v]); done.add(u)
    for v, w in G[u]:
        if d[u] + w < d[v]: d[v] = d[u] + w; dec += 1
assert d == {'S':0,'A':5,'B':2,'C':7,'D':8,'E':11} and dec == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Linked lists — selection by relinking',
            'text': 'The function `f` below moves a node of a singly linked list to the front by relinking pointers. The list `6 → 3 → 8 → 2 → 5 → 1` (shown below) is processed as in the program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

def f(head):
    prev, cur = None, head
    best_prev, best = None, head
    while cur:
        if cur.v < best.v:
            best_prev, best = prev, cur
        prev, cur = cur, cur.nxt
    if best_prev:
        best_prev.nxt = best.nxt
        best.nxt = head
        head = best
    return head

h = None
for x in reversed([6, 3, 8, 2, 5, 1]):
    h = Node(x, h)
h = f(h)
h.nxt = f(h.nxt)
h.nxt.nxt = f(h.nxt.nxt)
out = []
while h:
    out.append(h.v); h = h.nxt
print(*out)''',
            'diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [6, 3, 8, 2, 5, 1],
                    'head': 'head',
                },
            ],
            'options': ['`1 2 3 5 6 8`', '`1 2 6 3 8 5`', '`1 6 3 8 2 5`', '`1 2 3 6 8 5`'],
            'answer': 'D',
            'solution': '''**Concept.** `f` finds the node with the minimum value (first occurrence) and splices it to the front of the list it is given. Calling it on successive suffixes is exactly **selection sort on a linked list** — but only three passes are made here.

- Pass 1, `f(6 3 8 2 5 1)`: minimum 1 (its predecessor is 5). Unlink 1, point it at 6 → **1** 6 3 8 2 5.
- Pass 2, `f(6 3 8 2 5)` on the suffix after 1: minimum 2 → 2 6 3 8 5; `h.nxt` is re-attached to it → 1 **2** 6 3 8 5.
- Pass 3, `f(6 3 8 5)`: minimum 3 → 3 6 8 5 → 1 2 **3** 6 8 5.

Output: `1 2 3 6 8 5` → (D).

Option by option:
- (A) assumes the list ends up fully sorted — three passes fix only the first three positions.
- (B) is after two passes.
- (C) is the list after one pass only (forgetting that the returned suffix is reattached).

**Trap:** the reassignments `h.nxt = f(h.nxt)` are essential: `f` may return a *different* node as the new head of the suffix; without reattaching, nodes would be lost.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [1, 2, 3, 6, 8, 5],
                    'head': 'head',
                    'caption': 'List after the three calls',
                },
            ],
            'verify': "ANSWER = {'B': 'D', 'D': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '1 2 3 6 8 5' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Insertion sort — comparison count',
            'text': 'Consider the insertion sort below, called on `A = [7, 4, 10, 1, 8, 3, 12]`. Because of short-circuit evaluation, the comparison `A[j] > key` is evaluated only when `j >= 0` is true. The total number of times `A[j] > key` is evaluated is ______.',
            'code': '''def isort(A):
    for i in range(1, len(A)):
        key, j = A[i], i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key''',
            'run_code': False,
            'answer': '13',
            'solution': '''**Concept.** For each key, the number of evaluations of `A[j] > key` equals the number of shifts, plus **one** extra failing comparison if the scan stops on a smaller-or-equal element (j ≥ 0). If the key travels all the way to index 0, the loop ends on `j >= 0` being false and no extra comparison happens.

- i=1, key 4: 7>4 shift; j = −1 stops → shifts 1, comparisons **1**.
- i=2, key 10: 7>10 false → shifts 0, comparisons **1**.
- i=3, key 1: 10, 7, 4 all shift; j = −1 → shifts 3, comparisons **3**.
- i=4, key 8: 10>8 shift; 7>8 false → shifts 1, comparisons **2**.
- i=5, key 3: 10, 8, 7, 4 shift; 1>3 false → shifts 4, comparisons **5**.
- i=6, key 12: 10>12 false → comparisons **1**.

Total = 1 + 1 + 3 + 2 + 5 + 1 = **13** (shifts = inversions = 9; plus 4 keys that stopped on a smaller element).

Formula: comparisons = inversions + (n − 1) − (number of keys that become the new minimum of the prefix) = 9 + 6 − 2 = 13.

**Trap:** adding one comparison per pass to the shifts gives 15 — it overcounts the two keys (4 and 1) that reached index 0.''',
            'verify': '''
A = [7, 4, 10, 1, 8, 3, 12]; c = 0
for i in range(1, len(A)):
    key, j = A[i], i - 1
    while j >= 0:
        c += 1
        if A[j] > key:
            A[j + 1] = A[j]; j -= 1
        else:
            break
    A[j + 1] = key
assert A == sorted(A) and c == int(ANSWER)
''',
        },
    ],
}
