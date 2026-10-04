# Set 08 — Hash Tables (Moderate)
SET = {
    'number': 8,
    'title': 'Hash Tables',
    'difficulty': 'Moderate',
    'focus': 'chaining, linear/quadratic probing, double hashing, deletion',
    'questions': [
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': '''The keys 38, 15, 74, 24, 63, 50, 29, 9, 57, 44 are inserted in that order into an initially empty hash table with 7 slots (indices 0 to 6) using h(k) = k mod 7 and separate chaining. Each new key is appended at the **end** of its chain.

Every one of the 10 keys is then searched for exactly once. A search walks its chain from the front and each key examined counts as one comparison. The total number of key comparisons over all 10 successful searches is ______.''',
            'answer': '18',
            'solution': '''With chaining, a successful search for the key at position p (1-based) in its chain costs p comparisons, so the total cost of searching every key once is ∑ over chains of 1 + 2 + … + L = L(L+1)/2.

Home slots (k mod 7):
- 38→3, 15→1, 74→4, 24→3, 63→0, 50→1, 29→1, 9→2, 57→1, 44→2.

Chains (front → back):
- slot 0: 63 (L = 1) → cost 1
- slot 1: 15, 50, 29, 57 (L = 4) → cost 1+2+3+4 = 10
- slot 2: 9, 44 (L = 2) → cost 3
- slot 3: 38, 24 (L = 2) → cost 3
- slot 4: 74 (L = 1) → cost 1
- slots 5, 6 empty.

Total = 1 + 10 + 3 + 3 + 1 = **18** (average 1.8 comparisons per successful search).

**Trap:** counting only the chain lengths (10) or the longest chain (4). The cost of a successful search depends on the key's *position* inside the chain, so a long chain contributes quadratically, not linearly.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 7,
                    'slots': {
                        0: [63],
                        1: [15, 50, 29, 57],
                        2: [9, 44],
                        3: [38, 24],
                        4: [74],
                    },
                    'caption': 'Final chained table (tail insertion)',
                },
            ],
            'verify': '''
ch = [[] for _ in range(7)]
for k in [38,15,74,24,63,50,29,9,57,44]:
    ch[k % 7].append(k)
tot = sum(c.index(k) + 1 for c in ch for k in c)
assert tot == int(ANSWER)
assert max(len(c) for c in ch) == 4
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — dictionary keys and hashing',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''d = {1: 'a', True: 'b', 1.0: 'c', 2: 'd'}
print(d)''',
            'options': [
                "`{True: 'c', 2: 'd'}`",
                "`{1: 'c', 2: 'd'}`",
                "`{1: 'a', True: 'b', 1.0: 'c', 2: 'd'}`",
                "`{1.0: 'c', 2: 'd'}`",
            ],
            'answer': 'B',
            'solution': '''A Python dict treats two keys as the *same* key when they have equal hashes **and** compare equal with `==`. Here `1 == True == 1.0` and `hash(1) == hash(True) == hash(1.0) == 1`, so all three literals denote one dictionary entry.

Building the literal left to right:
- `1: 'a'` creates the entry with key object `1`.
- `True: 'b'` finds an equal existing key → only the **value** is replaced; the stored key object stays `1`.
- `1.0: 'c'` again overwrites the value → `'c'`.
- `2: 'd'` is a new key.

Result: `{1: 'c', 2: 'd'}` → option **(B)**.

- (A) and (D) assume the *latest* key object replaces the original key — it does not; only the value is updated.
- (C) assumes `int`, `bool` and `float` keys are distinct — they are not, because hash tables decide identity by hash + equality, not by type.

**Tip:** `bool` is a subclass of `int`; `True` behaves as `1` in every hash-based container (`{1, True, 1.0}` has length 1).''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)
assert OUTPUT.strip() == "{1: 'c', 2: 'd'}"''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression below is evaluated with a stack (operands are pushed; an operator pops the right operand first, then the left operand, and pushes the result). All operators are binary and `/` is exact division.

`8 6 2 - 3 * 4 / + 5 -`

What are the value of the expression and the maximum number of elements ever on the stack, respectively?''',
            'options': ['−2 and 3', '6 and 4', '11 and 3', '6 and 3'],
            'answer': 'D',
            'solution': '''Scan left to right, pushing operands and applying each operator to the top two entries:

- 8 → [8];  6 → [8, 6];  2 → [8, 6, 2]  (size 3)
- `-` → 6 − 2 = 4 → [8, 4]
- 3 → [8, 4, 3]  (size 3)
- `*` → 4 × 3 = 12 → [8, 12]
- 4 → [8, 12, 4]  (size 3)
- `/` → 12 / 4 = 3 → [8, 3]
- `+` → 8 + 3 = 11 → [11]
- 5 → [11, 5];  `-` → 11 − 5 = 6 → [6]

Value **6**, maximum stack size **3** → option **(D)**.

- (A) pops operands in the wrong order for the last operator (5 − 11 + …).
- (B) would need four operands pending at once, which never happens.
- (C) stops before the final `5 -`.

**Trap:** for non-commutative operators the *second* popped value is the left operand.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [8, 12, 4],
                    'label': 'S',
                    'caption': 'Stack just before `/` is applied (one of the size-3 peaks)',
                },
            ],
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

st = []; mx = 0
for t in "8 6 2 - 3 * 4 / + 5 -".split():
    if t in "+-*/":
        b = st.pop(); a = st.pop()
        st.append({'+':a+b,'-':a-b,'*':a*b,'/':a/b}[t])
    else:
        st.append(int(t))
    mx = max(mx, len(st))
assert st == [6] and mx == 3 and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — quadratic probing',
            'text': '''Keys 35, 20, 57, 9, 46, 31 are inserted in that order into an initially empty hash table of size 11 (indices 0–10) using quadratic probing:
h(k, i) = (k + i²) mod 11,  i = 0, 1, 2, …
The index of the slot in which key 31 is stored is ______.''',
            'answer': '7',
            'solution': '''Quadratic probing tries offsets 0, 1, 4, 9, 16, … from the home slot k mod 11, wrapping modulo 11.

- 35: home 35 mod 11 = 2 → slot **2**.
- 20: home 9 → slot **9**.
- 57: home 2 (full) → i=1: 3 → slot **3**.
- 9: home 9 (full) → i=1: 10 → slot **10**.
- 46: home 2 (full) → i=1: 3 (full) → i=2: 2+4 = 6 → slot **6**.
- 31: home 9 (full) → i=1: 10 (full) → i=2: 13 mod 11 = 2 (full) → i=3: 18 mod 11 = **7** (free).

Key 31 is stored in slot **7** after three collisions.

**Trap:** using i instead of i² (linear probing would give 9→10→0, i.e. slot 0), or forgetting to wrap 13 to 2 and finding it occupied by 35.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        2: 35,
                        3: 57,
                        6: 46,
                        7: 31,
                        9: 20,
                        10: 9,
                    },
                    'caption': 'Table after all six insertions',
                },
            ],
            'verify': '''
T = [None]*11
for k in [35,20,57,9,46,31]:
    i = 0
    while T[(k+i*i) % 11] is not None: i += 1
    T[(k+i*i) % 11] = k
assert T.index(31) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues — circular array',
            'text': '''A circular queue is stored in an array Q[0..5] with indices `front` and `rear`, both initially 0. `enqueue(x)` stores x at Q[rear] and sets rear = (rear+1) mod 6; `dequeue()` returns Q[front] and sets front = (front+1) mod 6. The queue is full when (rear+1) mod 6 = front.

Starting empty, the following operations are performed:
enqueue a, b, c, d; dequeue; dequeue; enqueue e, f, g; dequeue; enqueue h.

After these operations, the values of (front, rear) and the element at the front are:''',
            'options': ['(3, 2) and e', '(2, 1) and c', '(3, 2) and d', '(4, 2) and d'],
            'answer': 'C',
            'solution': '''Track both indices modulo 6 (capacity is 5 because one slot is kept empty to distinguish full from empty):

- enqueue a, b, c, d → slots 0–3, rear = 4, front = 0.
- dequeue, dequeue (a, b) → front = 2.
- enqueue e (slot 4), f (slot 5), g (slot 0) → rear = 7 mod 6 = 1. Now (rear+1) mod 6 = 2 = front → the queue is **full** (c, d, e, f, g).
- dequeue (c) → front = 3.
- enqueue h at slot 1 → rear = 2.

Final: front = 3, rear = 2, Q[3] = d → option **(C)**.

- (A) has the right indices but mis-reads the front element (e is at index 4).
- (B) is the state before the last dequeue/enqueue pair.
- (D) dequeues once too often.

**Tip:** with this convention the queue length is (rear − front) mod 6 = (2 − 3) mod 6 = 5, i.e. the queue is full again.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': ['g', 'h', 'c', 'd', 'e', 'f'],
                    'pointers': {
                        'front': 3,
                        'rear': 2,
                    },
                    'highlight': [3],
                    'caption': 'Array Q at the end (slot 2 still holds the dequeued c)',
                },
            ],
            'verify': '''ANSWER = {'A': 'C', 'C': 'A'}.get(ANSWER, ANSWER)

Q = [None]*6; f = r = 0
def enq(x):
    global r
    assert (r+1) % 6 != f
    Q[r] = x; r = (r+1) % 6
def deq():
    global f
    x = Q[f]; f = (f+1) % 6; return x
for x in "abcd": enq(x)
deq(); deq()
for x in "efg": enq(x)
deq(); enq('h')
assert (f, r, Q[f]) == (3, 2, 'd') and ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Binary search trees',
            'text': 'The keys 45, 22, 67, 11, 30, 56, 89, 26, 35, 60 are inserted in that order into an initially empty binary search tree, giving the tree T shown. Which of the following statements is/are TRUE? (Height = number of edges on the longest root-to-leaf path.)',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            22,
                            [11],
                            [
                                30,
                                [26],
                                [35],
                            ],
                        ],
                        [
                            67,
                            [
                                56,
                                None,
                                [60],
                            ],
                            [89],
                        ],
                    ],
                    'caption': 'Figure: BST T',
                },
            ],
            'options': [
                'T has exactly 4 leaves',
                'The height of T is 4',
                'If 22 is deleted by replacing it with its in-order successor, 26 becomes the left child of 45',
                'The in-order successor of 35 is 45',
            ],
            'answer': ['C', 'D'],
            'solution': '''In a BST the in-order successor of a node with no right child is the nearest ancestor of which the node lies in the *left* subtree.

- (A) Leaves are 11, 26, 35, 60, 89 → 5 leaves. **False.**
- (B) Longest paths: 45→22→30→26, 45→22→30→35, 45→67→56→60 — each has 3 edges. Height = 3, not 4. **False.**
- (C) 22 has two children; its successor is the minimum of its right subtree (rooted at 30) = 26. 26 replaces 22, so 26 becomes the left child of 45. **True.**
- (D) 35 has no right child. Walking up: 35 is the right child of 30, 30 is the right child of 22, 22 is the **left** child of 45 → successor = 45. **True.**

**Trap:** in (A) it is easy to miss 60, which hangs as the *right* child of 56 and makes 56 an internal node.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            26,
                            [11],
                            [
                                30,
                                None,
                                [35],
                            ],
                        ],
                        [
                            67,
                            [
                                56,
                                None,
                                [60],
                            ],
                            [89],
                        ],
                    ],
                    'highlight': [26],
                    'caption': 'T after deleting 22 (successor 26 moved up)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
T = None
for k in [45,22,67,11,30,56,89,26,35,60]: T = ins(T, k)
def h(t): return -1 if t is None else 1 + max(h(t[1]), h(t[2]))
def leaves(t):
    if t is None: return 0
    if t[1] is None and t[2] is None: return 1
    return leaves(t[1]) + leaves(t[2])
def ino(t): return [] if t is None else ino(t[1]) + [t[0]] + ino(t[2])
s = ino(T)
assert s[s.index(35)+1] == 45 and h(T) == 3 and leaves(T) == 5
assert min(ino(T[1][2])) == 26
assert sorted(ANSWER) == ['A','C']
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Binary search — iteration count',
            'text': 'Consider the following Python program operating on the sorted array shown. What is printed?',
            'code': '''def bs(a, x):
    lo, hi, c = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if a[mid] == x:
            return c
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return c

a = [3, 8, 14, 19, 25, 31, 36, 42, 47, 53, 60, 66]
print(bs(a, 50), bs(a, 31))''',
            'diagrams': [
                {
                    'type': 'array',
                    'values': [3, 8, 14, 19, 25, 31, 36, 42, 47, 53, 60, 66],
                    'label': 'a',
                },
            ],
            'options': ['`4 1`', '`3 1`', '`4 6`', '`5 1`'],
            'answer': 'A',
            'solution': '''`c` counts loop iterations (one middle-element probe each).

Search for 50 (absent), n = 12:
- lo=0, hi=11 → mid=5, a[5]=31 < 50 → lo=6  (c=1)
- lo=6, hi=11 → mid=8, a[8]=47 < 50 → lo=9  (c=2)
- lo=9, hi=11 → mid=10, a[10]=60 > 50 → hi=9  (c=3)
- lo=9, hi=9 → mid=9, a[9]=53 > 50 → hi=8  (c=4)
- lo > hi → return 4.

Search for 31: the very first mid is (0+11)//2 = 5 and a[5] = 31 → return 1.

Output `4 1` → option **(A)**.

- (B) stops one probe early (forgets the lo = hi iteration).
- (C) confuses the count with the index of 31.
- (D) adds an extra probe; ⌊log₂ 12⌋ + 1 = 4 is the maximum possible here.

**Tip:** an unsuccessful binary search on n elements uses ⌊log₂ n⌋ or ⌊log₂ n⌋ + 1 iterations.''',
            'verify': "ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '4 1' and ANSWER == 'B'",
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Insertion sort — shifts',
            'text': '''Standard insertion sort (ascending) is applied to the array
[31, 12, 47, 5, 28, 19, 40, 3].
A *shift* is one execution of `a[j+1] = a[j]` in the inner loop. The total number of shifts performed is ______.''',
            'answer': '17',
            'solution': '''Each shift moves one larger element past the key being inserted, so it removes exactly one inversion. Total shifts = number of inversions (pairs i < j with a[i] > a[j]).

Count, for each element, the larger elements to its left:
- 31: 0 · 12: 1 (31) · 47: 0 · 5: 3 (31, 12, 47)
- 28: 2 (31, 47) · 19: 3 (31, 47, 28) · 40: 1 (47)
- 3: 7 (all earlier elements)

Total = 0+1+0+3+2+3+1+7 = **17**.

Pass-by-pass the shift counts are 1, 0, 3, 2, 3, 1, 7 (see table).

**Trap:** counting *comparisons* instead of shifts — comparisons also include the final failing test of each pass that does not stop at index 0.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after inserting each key (shifts in last column)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7', 'shifts'],
                    'row_labels': ['start', '12', '47', '5', '28', '19', '40', '3'],
                    'rows': [
                        [31, 12, 47, 5, 28, 19, 40, 3, '-'],
                        [12, 31, 47, 5, 28, 19, 40, 3, 1],
                        [12, 31, 47, 5, 28, 19, 40, 3, 0],
                        [5, 12, 31, 47, 28, 19, 40, 3, 3],
                        [5, 12, 28, 31, 47, 19, 40, 3, 2],
                        [5, 12, 19, 28, 31, 47, 40, 3, 3],
                        [5, 12, 19, 28, 31, 40, 47, 3, 1],
                        [3, 5, 12, 19, 28, 31, 40, 47, 7],
                    ],
                },
            ],
            'verify': '''
a = [31,12,47,5,28,19,40,3]; s = 0
for i in range(1, len(a)):
    key = a[i]; j = i - 1
    while j >= 0 and a[j] > key:
        a[j+1] = a[j]; j -= 1; s += 1
    a[j+1] = key
assert s == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists in Python',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class Node:
    def __init__(self, v, nxt=None):
        self.v, self.nxt = v, nxt

head = None
for v in [4, 8, 15, 16, 23]:
    head = Node(v, head)

p = head
while p and p.nxt:
    p.nxt = p.nxt.nxt
    p = p.nxt

out, p = [], head
while p:
    out.append(p.v)
    p = p.nxt
print(out)''',
            'options': ['`[4, 15, 23]`', '`[23, 15, 4]`', '`[23, 16, 8]`', '`[16, 8]`'],
            'answer': 'B',
            'solution': '''`Node(v, head)` *prepends*, so the list is built in reverse: 23 → 16 → 15 → 8 → 4.

The second loop unlinks the node after `p` and then advances `p` to the new next node:
- p = 23: 23.nxt = 15 (16 removed); p = 15.
- p = 15: 15.nxt = 4 (8 removed); p = 4.
- p = 4: p.nxt is None → stop.

Final list 23 → 15 → 4, printed as `[23, 15, 4]` → option **(B)**.

- (A) forgets that insertion at the head reverses the order.
- (C) keeps the nodes that were removed (16, 8) instead of the ones kept.
- (D) assumes the head itself is deleted.

**Trap:** after `p.nxt = p.nxt.nxt`, the statement `p = p.nxt` jumps to the node that was *two* positions ahead — the loop deletes every second node.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [23, 15, 4],
                    'caption': 'List after the deletion loop',
                },
            ],
            'verify': "ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[23, 15, 4]' and ANSWER == 'A'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Graph traversal — BFS orders',
            'text': 'Breadth-first search is started at vertex P of the undirected graph shown. The neighbours of a vertex may be enqueued in **any** order. Which of the following is/are possible BFS visit orders?',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'S'],
                        ['R', 'S'],
                        ['R', 'T'],
                        ['S', 'U'],
                        ['T', 'U'],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [1.5, 2],
                        'R': [1.5, 0],
                        'S': [3, 2],
                        'T': [3, 0],
                        'U': [4.5, 1],
                    },
                },
            ],
            'options': ['P, R, S, Q, T, U', 'P, R, Q, T, S, U', 'P, Q, R, T, S, U', 'P, Q, R, S, T, U'],
            'answer': ['B', 'D'],
            'solution': '''BFS visits vertices level by level, and *within* a level the order is fixed by the order in which their parents were dequeued.

Levels from P: L1 = {Q, R}, L2 = {S, T}, L3 = {U}.

- (A) S is at level 2 but appears before Q (level 1). **Impossible.**
- (B) R first: R enqueues T then S (any order allowed); Q adds nothing new. Order P R Q T S U. **Possible.**
- (C) Q is dequeued before R, so S (discovered by Q) must precede T (discovered only by R). T before S is **impossible.**
- (D) Q first: Q enqueues S; then R enqueues T (S already seen). Order P Q R S T U. **Possible.**

**Trap:** checking only the level sets. A sequence can respect levels yet violate the FIFO parent order, as in (C).''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['P', 'Q', 'R', 'S', 'T', 'U'],
                    'edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'S'],
                        ['R', 'S'],
                        ['R', 'T'],
                        ['S', 'U'],
                        ['T', 'U'],
                    ],
                    'pos': {
                        'P': [0, 1],
                        'Q': [1.5, 2],
                        'R': [1.5, 0],
                        'S': [3, 2],
                        'T': [3, 0],
                        'U': [4.5, 1],
                    },
                    'highlight_edges': [
                        ['P', 'Q'],
                        ['P', 'R'],
                        ['Q', 'S'],
                        ['R', 'T'],
                        ['S', 'U'],
                    ],
                    'caption': 'BFS tree for order (A)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from itertools import permutations
G = {'P':'QR','Q':'PS','R':'PST','S':'QRU','T':'RU','U':'ST'}
orders = set()
def bfs(choice):
    # enumerate all BFS orders by trying all neighbour permutations
    res = set()
    def go(queue, seen, out):
        if not queue:
            res.add(''.join(out)); return
        u = queue[0]; new = [v for v in G[u] if v not in seen]
        for p in permutations(new):
            go(queue[1:] + list(p), seen | set(p), out + list(p))
    go(['P'], {'P'}, ['P'])
    return res
orders = bfs(None)
opts = {'A':'PQRSTU','B':'PRQTSU','C':'PQRTSU','D':'PRSQTU'}
assert sorted(k for k, v in opts.items() if v in orders) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — double hashing',
            'text': '''Keys 41, 58, 22, 70, 35, 96, 19, 48, 32 are inserted in that order into an initially empty table of size 13 (indices 0–12) using double hashing:
h(k, i) = (h₁(k) + i·h₂(k)) mod 13, where h₁(k) = k mod 13 and h₂(k) = 7 − (k mod 7),  i = 0, 1, 2, …
The index of the slot in which the last key, 32, is stored is ______.''',
            'answer': '12',
            'solution': '''In double hashing the probe *step* h₂(k) depends on the key, so keys that share a home slot follow different probe sequences (no secondary clustering). h₂ is never 0 here (values 1–7), and 13 is prime, so every probe sequence visits all slots.

Trace (h₁, h₂ → probes):
- 41: h₁ = 2 → slot **2**.
- 58: h₁ = 6 → slot **6**.
- 22: h₁ = 9 → slot **9**.
- 70: h₁ = 5 → slot **5**.
- 35: h₁ = 9 (full), h₂ = 7 − 0 = 7 → 16 mod 13 = **3**.
- 96: h₁ = 5 (full), h₂ = 7 − 5 = 2 → **7**.
- 19: h₁ = 6 (full), h₂ = 7 − 5 = 2 → **8**.
- 48: h₁ = 9 (full), h₂ = 7 − 6 = 1 → **10**.
- 32: h₁ = 6 (full: 58), h₂ = 7 − 4 = 3 → 9 (full: 22) → 12 → **free**.

Key 32 lands in slot **12** after 3 probes.

**Trap:** using k mod 7 itself as the step (that gives step 4 for 32 → 6, 10 (full), 14 mod 13 = 1), or forgetting that slot 9 is already occupied by 22.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 13,
                    'slots': {
                        2: 41,
                        3: 35,
                        5: 70,
                        6: 58,
                        7: 96,
                        8: 19,
                        9: 22,
                        10: 48,
                        12: 32,
                    },
                    'caption': 'Final table after nine insertions',
                },
            ],
            'verify': '''
T = [None]*13
for k in [41,58,22,70,35,96,19,48,32]:
    h1, h2, i = k % 13, 7 - k % 7, 0
    while T[(h1 + i*h2) % 13] is not None: i += 1
    T[(h1 + i*h2) % 13] = k
assert T.index(32) == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Hashing — deletion in open addressing',
            'text': '''A hash table of size 10 uses h(k) = k mod 10 with linear probing. Keys 52, 72, 13, 92, 25, 33 are inserted in that order. Then key 72 is deleted. Two deletion policies are considered:
(i) **lazy deletion** — the slot is marked DELETED (a tombstone); searches continue past tombstones and stop only at a never-used empty slot;
(ii) **naive deletion** — the slot is simply made empty.

A search for key 33 is then performed. Counting every slot inspected as one probe, what happens under policies (i) and (ii) respectively?''',
            'options': [
                '(i) 33 found after 5 probes; (ii) 33 reported absent after 1 probe',
                '(i) 33 found after 4 probes; (ii) 33 found after 4 probes',
                '(i) 33 found after 5 probes; (ii) 33 found after 4 probes',
                '(i) 33 reported absent after 1 probe; (ii) 33 reported absent after 1 probe',
            ],
            'answer': 'A',
            'solution': '''Open addressing relies on probe chains being *unbroken*: a search for k stops at the first empty slot because an insertion of k would have stopped there too.

Insertions (home = k mod 10):
- 52 → 2;  72 → 2 full → **3**;  13 → 3 full → **4**;
- 92 → 2, 3, 4 full → **5**;  25 → 5 full → **6**;
- 33 → 3, 4, 5, 6 full → **7**.

Delete 72 (slot 3).

(i) Tombstone: search 33 probes 3 (DELETED, keep going), 4 (13), 5 (92), 6 (25), 7 (33 ✓) → found after **5** probes.
(ii) Naive: slot 3 is now empty, so the search stops at its first probe and wrongly reports 33 as **absent** after **1** probe.

Option **(A)**.

- (B) and (C) assume slot 3 can be skipped for free or that the naive policy still works — the naive policy breaks the chain.
- (D) treats a tombstone as empty, which is exactly what tombstones prevent.

**Tip:** a later insert of, say, 43 may *reuse* the tombstone at slot 3 (after verifying 43 is not already present), so lazy deletion does not waste space forever.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        2: 52,
                        3: 'DEL',
                        4: 13,
                        5: 92,
                        6: 25,
                        7: 33,
                    },
                    'caption': 'Table after lazy deletion of 72',
                },
            ],
            'verify': '''
T = [None]*10
for k in [52,72,13,92,25,33]:
    i = k % 10
    while T[i] is not None: i = (i+1) % 10
    T[i] = k
T1 = T[:]; T1[T1.index(72)] = 'DEL'
T2 = T[:]; T2[T2.index(72)] = None
def search(T, k):
    i, p = k % 10, 0
    while True:
        p += 1
        if T[i] is None: return False, p
        if T[i] == k: return True, p
        i = (i+1) % 10
assert search(T1, 33) == (True, 5) and search(T2, 33) == (False, 1)
assert ANSWER == 'A'
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Hashing — reconstructing insertion order',
            'text': 'A hash table of size 10 uses h(k) = k mod 10 and linear probing. After six insertions into an initially empty table it looks as shown. Which of the following insertion sequences could have produced this table?',
            'diagrams': [
                {
                    'type': 'hashtable',
                    'size': 10,
                    'slots': {
                        2: 42,
                        3: 23,
                        4: 34,
                        5: 52,
                        6: 33,
                        7: 46,
                    },
                    'caption': 'Figure: final table',
                },
            ],
            'options': [
                '23, 34, 42, 52, 33, 46',
                '42, 23, 52, 34, 33, 46',
                '42, 34, 23, 52, 46, 33',
                '34, 42, 23, 52, 33, 46',
            ],
            'answer': ['A', 'D'],
            'solution': '''Derive *precedence constraints* from where each key sits relative to its home slot: a key displaced from home h to slot s needs slots h … s−1 to be occupied when it arrives.

- 42, 23, 34 sit at their homes (2, 3, 4) → each must arrive before any other key spills into its slot.
- 52 (home 2) is at 5 → 42, 23, 34 must all precede 52.
- 33 (home 3) is at 6 → 23, 34, 52 precede 33.
- 46 (home 6) is at 7 → 33 precedes 46.

So the valid orders are: {42, 23, 34} in any order, then 52, then 33, then 46 (3! = 6 sequences).

- (A) 23, 34, 42 | 52 | 33 | 46 — fits. **Possible.**
- (B) 52 arrives before 34, so 52 probes 2, 3 and lands in **4**; then 34 is displaced. **Not possible.**
- (C) 46 arrives before 33 and finds its home 6 empty → 46 at 6, 33 later goes to 7. **Not possible.**
- (D) 34, 42, 23 | 52 | 33 | 46 — fits. **Possible.**

**Tip:** simulate only the options that pass the constraint check — it saves time in the exam.''',
            'verify': '''_m = {'C': 'A', 'A': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

target = {2:42, 3:23, 4:34, 5:52, 6:33, 7:46}
def build(seq):
    T = [None]*10
    for k in seq:
        i = k % 10
        while T[i] is not None: i = (i+1) % 10
        T[i] = k
    return {i: v for i, v in enumerate(T) if v is not None}
opts = {'A':[34,42,23,52,33,46], 'B':[42,23,52,34,33,46],
        'C':[23,34,42,52,33,46], 'D':[42,34,23,52,46,33]}
assert sorted(k for k, s in opts.items() if build(s) == target) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — expected empty slots',
            'text': 'Fifteen keys are inserted into a hash table with 10 slots using separate chaining. Assume simple uniform hashing: each key independently hashes to each slot with probability 1/10. The expected number of slots that remain **empty** after all insertions is ______ (rounded off to two decimal places).',
            'answer': ['2.05', '2.07'],
            'solution': '''Use *linearity of expectation* with an indicator per slot.

- Let Xⱼ = 1 if slot j is empty after all insertions. A single key misses slot j with probability 1 − 1/10 = 0.9, and the 15 keys are independent, so P(Xⱼ = 1) = 0.9¹⁵.
- Expected number of empty slots E[∑Xⱼ] = 10 · 0.9¹⁵.

Compute 0.9¹⁵: 0.9² = 0.81, 0.9⁴ = 0.6561, 0.9⁸ = 0.43047, 0.9¹⁵ = 0.9⁸ · 0.9⁴ · 0.9² · 0.9 = 0.43047 × 0.6561 × 0.81 × 0.9 ≈ 0.20589.

Expected empty slots ≈ 10 × 0.20589 ≈ **2.06**.

Interpretation: even with load factor α = 1.5 about a fifth of the table is still unused, i.e. roughly m·e^{−α} ≈ 10 × 0.2231 = 2.23 for large m.

**Trap:** computing m − n (negative here) or assuming keys fill distinct slots until the table is full. Another common slip is using (1/10)¹⁵ (probability that *all* keys hit one slot) instead of 0.9¹⁵.''',
            'verify': '''
v = 10 * 0.9 ** 15
assert float(ANSWER[0]) <= round(v, 2) <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python — __hash__ and __eq__ contract',
            'text': 'Consider the following Python program, in which `__eq__` and `__hash__` are deliberately inconsistent. What is printed?',
            'code': '''class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x
    def __hash__(self):
        return hash(self.y)

s = set()
for x, y in [(1, 2), (1, 3), (2, 2), (1, 2)]:
    s.add(P(x, y))
print(len(s), P(1, 99) in s)''',
            'options': ['`2 True`', '`4 False`', '`3 False`', '`3 True`'],
            'answer': 'C',
            'solution': '''A set (a hash table) finds a candidate entry only through its **hash**; `__eq__` is consulted only among entries whose stored hash equals the probe hash. The rule `a == b ⇒ hash(a) == hash(b)` is violated here, so 'equal' objects can coexist.

Insertions (hash = hash(y)):
- P(1,2): hash 2, set empty → added (size 1).
- P(1,3): hash 3 — no stored entry has hash 3 → `__eq__` never called → added (size 2), even though its x equals P(1,2).x.
- P(2,2): hash 2 matches P(1,2); `__eq__` compares x: 2 ≠ 1 → added (size 3).
- P(1,2): hash 2; compared with P(1,2) → x equal → duplicate, not added.

`P(1, 99) in s`: hash 99 matches no stored hash → `False`, although `P(1, 99) == P(1, 2)` is `True`.

Output `3 False` → option **(C)**.

- (A) uses only `__eq__` (x values 1, 2).
- (B) ignores `__eq__` entirely (the final P(1,2) *is* rejected).
- (D) assumes membership falls back to `==` over all elements.

**Tip:** always hash exactly the fields used by `__eq__`.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '3 False' and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Merge sort — comparison counts',
            'text': 'Top-down merge sort splits an array of length n into a left half of length ⌊n/2⌋ and a right half, sorts both recursively (arrays of length ≤ 1 are returned unchanged) and merges them; the merge compares the two current front elements until one half is exhausted. Which of the following statements is/are TRUE?',
            'options': [
                'On the already sorted array [1, 2, …, 8] it makes exactly 12 comparisons',
                'The recurrence C(n) = 2C(n/2) + n − 1, C(1) = 0 gives C(8) = 24',
                'No array of 8 distinct elements needs more than 17 comparisons',
                'On [5, 9, 2, 7, 1, 8, 3, 6] the algorithm makes exactly 17 element comparisons',
            ],
            'answer': ['A', 'C', 'D'],
            'solution': '''Merging lists of sizes p and q costs between min(p, q) (one list runs out early) and p + q − 1 (they interleave to the very end) comparisons.

(D) [5, 9, 2, 7, 1, 8, 3, 6]:
- Size-1 merges: (5|9), (2|7), (1|8), (3|6) → 1 each = 4.
- Size-2 merges: [5,9]+[2,7] → 2,5,7,9 needs 3; [1,8]+[3,6] → 1,3,6,8 needs 3 → 6.
- Final: [2,5,7,9]+[1,3,6,8] fully interleaves → 7.
Total 4 + 6 + 7 = 17. **True.**

(A) Sorted input: every merge stops as soon as the left half is exhausted → 4·1 + 2·2 + 1·4 = 12. **True.**

(C) The worst case equals C(8) with C(n) = 2C(n/2) + n − 1: C(2) = 1, C(4) = 5, C(8) = 17 = n log₂ n − n + 1. The array in (D) already achieves it, and nothing can exceed it. **True.**

(B) As just computed, C(8) = 17, not 24 (24 = n log₂ n would need n comparisons per merge level). **False.**

**Trap:** using n log₂ n as the exact count — each merge of total size s needs at most s − 1 comparisons, not s.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Comparisons per merge level for (A)',
                    'col_labels': ['merges', 'result(s)', 'comparisons'],
                    'row_labels': ['level 1', 'level 2', 'level 3'],
                    'rows': [
                        ['4 × (1|1)', '59 27 18 36', 4],
                        ['2 × (2|2)', '2579 1368', 6],
                        ['1 × (4|4)', '12356789', 7],
                    ],
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

from itertools import permutations
def ms(a, c):
    if len(a) <= 1: return a
    m = len(a)//2; L = ms(a[:m], c); R = ms(a[m:], c)
    out = []; i = j = 0
    while i < len(L) and j < len(R):
        c[0] += 1
        if L[i] <= R[j]: out.append(L[i]); i += 1
        else: out.append(R[j]); j += 1
    return out + L[i:] + R[j:]
def cnt(a):
    c = [0]; ms(list(a), c); return c[0]
A = cnt([5,9,2,7,1,8,3,6]) == 17
B = cnt(range(1,9)) == 12
C = max(cnt(p) for p in permutations(range(8))) == 17
def Cr(n): return 0 if n == 1 else 2*Cr(n//2) + n - 1
D = Cr(8) == 24
truth = {'A':A, 'B':B, 'C':C, 'D':D}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — Lomuto partition',
            'text': '''The Lomuto partition scheme (pivot = last element; i starts at lo − 1; for each j from lo to hi − 1, if a[j] ≤ pivot then i is incremented and a[i], a[j] are swapped; finally a[i+1] and a[hi] are swapped) is applied once to
[42, 17, 63, 8, 55, 29, 71, 36].
What is the array after this single partition call?''',
            'options': [
                '[17, 8, 29, 36, 63, 55, 71, 42]',
                '[17, 8, 29, 36, 42, 55, 63, 71]',
                '[8, 17, 29, 36, 55, 63, 71, 42]',
                '[17, 8, 29, 36, 55, 63, 71, 42]',
            ],
            'answer': 'D',
            'solution': '''Lomuto keeps the invariant a[lo..i] ≤ pivot < a[i+1..j−1]. Pivot = 36.

- j=0: 42 > 36 → no change.
- j=1: 17 ≤ 36 → i=0, swap a[0], a[1] → [17, 42, 63, 8, 55, 29, 71, 36].
- j=2: 63 > 36.
- j=3: 8 ≤ 36 → i=1, swap a[1], a[3] → [17, 8, 63, 42, 55, 29, 71, 36].
- j=4: 55 > 36.
- j=5: 29 ≤ 36 → i=2, swap a[2], a[5] → [17, 8, 29, 42, 55, 63, 71, 36].
- j=6: 71 > 36.
- Final: swap a[3], a[7] → [17, 8, 29, **36**, 55, 63, 71, 42].

Option **(D)**; the pivot 36 is now at its final index 3.

- (A) mis-tracks the swap at j = 5 (63 moves to index 5, not 4).
- (B) sorts the right part, which partition does not do.
- (C) sorts the left part (17 and 8 keep their swapped order).

**Trap:** the final swap sends the element at i+1 (here 42) to the *end*, so the right part is not in original order.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Array after each swap (pivot 36)',
                    'col_labels': ['0', '1', '2', '3', '4', '5', '6', '7'],
                    'row_labels': ['start', 'j=1', 'j=3', 'j=5', 'final'],
                    'rows': [
                        [42, 17, 63, 8, 55, 29, 71, 36],
                        [17, 42, 63, 8, 55, 29, 71, 36],
                        [17, 8, 63, 42, 55, 29, 71, 36],
                        [17, 8, 29, 42, 55, 63, 71, 36],
                        [17, 8, 29, 36, 55, 63, 71, 42],
                    ],
                    'highlight': [
                        [4, 3],
                    ],
                },
            ],
            'verify': '''ANSWER = {'A': 'D', 'D': 'A'}.get(ANSWER, ANSWER)

a = [42,17,63,8,55,29,71,36]; p = a[-1]; i = -1
for j in range(len(a)-1):
    if a[j] <= p:
        i += 1; a[i], a[j] = a[j], a[i]
a[i+1], a[-1] = a[-1], a[i+1]
assert a == [17,8,29,36,55,63,71,42] and ANSWER == 'A'
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source A on the weighted directed graph shown. The sum of the shortest-path distances from A to the vertices B, C, D, E and F is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'edges': [
                        ['A', 'B', 7],
                        ['A', 'C', 2],
                        ['C', 'B', 3],
                        ['B', 'D', 4],
                        ['C', 'D', 9],
                        ['C', 'E', 6],
                        ['E', 'D', 1],
                        ['D', 'F', 3],
                        ['E', 'F', 8],
                        ['B', 'F', 10],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 0],
                        'D': [4, 2],
                        'E': [4, 0],
                        'F': [6, 1],
                    },
                },
            ],
            'answer': '36',
            'solution': '''Dijkstra repeatedly extracts the unsettled vertex with the smallest tentative distance and relaxes its outgoing edges (all weights are non-negative, so this is correct).

- Extract A (0): B = 7, C = 2.
- Extract C (2): B = min(7, 2+3) = 5; D = 2+9 = 11; E = 2+6 = 8.
- Extract B (5): D = min(11, 5+4) = 9; F = 5+10 = 15.
- Extract E (8): D = min(9, 8+1) = 9 (tie, no change); F = min(15, 16) = 15.
- Extract D (9): F = min(15, 9+3) = 12.
- Extract F (12).

Distances: B = 5, C = 2, D = 9, E = 8, F = 12.
Sum = 5 + 2 + 9 + 8 + 12 = **36**.

**Trap:** taking the direct edge A→B (7) or B→F (10) at face value. Both are improved through C and D respectively. Note the tie at D (A→C→B→D and A→C→E→D both cost 9) does not change any distance.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['A', 'B', 'C', 'D', 'E', 'F'],
                    'row_labels': ['A', 'C', 'B', 'E', 'D', 'F'],
                    'rows': [
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, 11, 8, '∞'],
                        [0, 5, 2, 9, 8, 15],
                        [0, 5, 2, 9, 8, 15],
                        [0, 5, 2, 9, 8, 12],
                        [0, 5, 2, 9, 8, 12],
                    ],
                },
            ],
            'verify': '''
import heapq
E = [('A','B',7),('A','C',2),('C','B',3),('B','D',4),('C','D',9),('C','E',6),
     ('E','D',1),('D','F',3),('E','F',8),('B','F',10)]
G = {v: [] for v in 'ABCDEF'}
for u, v, w in E: G[u].append((v, w))
d = {v: float('inf') for v in G}; d['A'] = 0; pq = [(0, 'A')]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in G[u]:
        if du + w < d[v]: d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d[v] for v in 'BCDEF') == int(ANSWER)
''',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Binary heaps — insertion and delete-max',
            'text': 'The keys 19, 42, 7, 33, 58, 25, 61, 12 are inserted one at a time, in that order, into an initially empty binary **max**-heap stored in an array (0-based; children of index i are 2i+1 and 2i+2). Each insertion appends the key and sifts it up by swapping with its parent while it is larger. Which of the following statements is/are TRUE?',
            'options': [
                'The level-order sequence of the final heap is 61, 58, 42, 33, 19, 25, 7, 12',
                'After one delete-max (last element moved to the root, then sift-down) the array is [58, 42, 25, 19, 33, 7, 12]',
                'A total of 7 swaps are performed during the eight insertions',
                'The root is 61 and its right child is 58',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''Heap insertion: place at the next free index, then swap upward while the parent is smaller.

- 19 → [19]
- 42 → swaps with 19 (1) → [42, 19]
- 7 → [42, 19, 7]
- 33 at idx 3, parent 19 → swap (2) → [42, 33, 7, 19]
- 58 at idx 4: swap with 33 (3), then with 42 (4) → [58, 42, 7, 19, 33]
- 25 at idx 5: swap with 7 (5) → [58, 42, 25, 19, 33, 7]
- 61 at idx 6: swap with 25 (6), with 58 (7) → [61, 42, 58, 19, 33, 7, 25]
- 12 at idx 7, parent 19 → no swap.

Final array: [61, 42, 58, 19, 33, 7, 25, 12].

- (A) The level order *is* the array order 61, 42, 58, … — the statement swaps 42 and 58 and is otherwise wrong too. **False.**
- (B) Move 12 to the root: [12, 42, 58, 19, 33, 7, 25]. 12 swaps with larger child 58 → [58, 42, 12, 19, 33, 7, 25]; then with 25 → [58, 42, 25, 19, 33, 7, 12]. **True.**
- (C) 7 swaps in total. **True.**
- (D) Root 61, right child (idx 2) 58. **True.**

**Trap:** in sift-down always swap with the *larger* child; swapping with 42 here would break the heap.''',
            'solution_diagrams': [
                {
                    'type': 'heap',
                    'values': [61, 42, 58, 19, 33, 7, 25, 12],
                    'caption': 'Max-heap after the eight insertions',
                },
                {
                    'type': 'heap',
                    'values': [58, 42, 25, 19, 33, 7, 12],
                    'caption': 'After one delete-max',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'C', 'C': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

a = []; sw = 0
for k in [19,42,7,33,58,25,61,12]:
    a.append(k); i = len(a) - 1
    while i > 0 and a[(i-1)//2] < a[i]:
        a[i], a[(i-1)//2] = a[(i-1)//2], a[i]; i = (i-1)//2; sw += 1
b = a[:]; b[0] = b.pop(); i = 0
while True:
    l, r, big = 2*i+1, 2*i+2, i
    if l < len(b) and b[l] > b[big]: big = l
    if r < len(b) and b[r] > b[big]: big = r
    if big == i: break
    b[i], b[big] = b[big], b[i]; i = big
truth = {'A': a[0] == 61 and a[2] == 58, 'B': sw == 7,
         'C': a == [61,58,42,33,19,25,7,12], 'D': b == [58,42,25,19,33,7,12]}
assert sorted(k for k, v in truth.items() if v) == sorted(ANSWER)
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Hashing — rehashing with linear probing',
            'text': 'Consider the following Python implementation of an open-addressing hash table that doubles its size whenever an insertion would push the load factor above 0.5. The value printed by the program is ______.',
            'code': '''class HT:
    def __init__(self):
        self.m, self.n = 4, 0
        self.t = [None] * 4
        self.probes = 0
    def put(self, k):
        if (self.n + 1) / self.m > 0.5:
            self.grow()
        i = k % self.m
        while self.t[i] is not None:
            i = (i + 1) % self.m
            self.probes += 1
        self.t[i] = k
        self.n += 1
    def grow(self):
        old = [k for k in self.t if k is not None]
        self.m *= 2
        self.t, self.n = [None] * self.m, 0
        for k in old:
            self.put(k)

h = HT()
for k in [10, 22, 6, 14, 30, 18, 26]:
    h.put(k)
print(h.probes)''',
            'answer': '7',
            'solution': '''`probes` counts every *extra* slot inspected (collisions), including those made while re-inserting keys during `grow`. Re-insertion happens in **table order**, not original insertion order.

- m = 4: put 10 → slot 2. put 22: load (1+1)/4 = 0.5 (not > 0.5) → home 2 full → slot 3 (**probes 1**).
- put 6: (2+1)/4 > 0.5 → grow to m = 8; old = [10, 22] → 10 → 2, 22 → 6. Then 6 → home 6 full → 7 (**2**).
- put 14: (3+1)/8 = 0.5 → no grow; home 6 full, 7 full, → 0 (**4**). Table: [14, _, 10, _, _, _, 22, 6].
- put 30: (4+1)/8 > 0.5 → grow to m = 16; old (table order) = [14, 10, 22, 6] → 14 → 14, 10 → 10, 22 → 6, 6 → home 6 full → 7 (**5**). Then 30 → home 14 full → 15 (**6**).
- put 18: 6/16 → home 2 → free.
- put 26: 7/16 → home 10 full → 11 (**7**).

Printed value: **7**.

**Trap:** forgetting that `grow` calls `put`, so collisions during rehashing are also counted, or re-inserting keys in their original order (10, 22, 6, 14), which happens to change nothing here but generally can.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 16,
                    'slots': {
                        2: 18,
                        6: 22,
                        7: 6,
                        10: 10,
                        11: 26,
                        14: 14,
                        15: 30,
                    },
                    'caption': 'Final table (m = 16)',
                },
            ],
            'verify': 'assert OUTPUT.strip() == ANSWER',
        },
    ],
}
