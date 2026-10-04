# Set 02 — Stacks & Expression Evaluation
SET = {
    'number': 2,
    'title': 'Stacks & Expression Evaluation',
    'difficulty': 'Moderate',
    'focus': 'stacks, infix/postfix/prefix, balanced brackets, stack permutations',
    'questions': [
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Python — string slicing with negative steps',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''s = "POSTFIX"
t = s[::-2] + s[1:-1:2]
print(t, len(s[5:2]))''',
            'options': ['`XFSPOSF 0`', '`XFSPOTI 0`', '`XFSPOTI 3`', '`XIFTSOP 0`'],
            'answer': 'B',
            'solution': '''**Concept:** a slice `s[start:stop:step]` walks from `start` towards `stop` in jumps of `step`; with a negative step and omitted bounds it starts at the last character. A slice whose direction cannot reach `stop` is simply empty — it never raises an error.

Indices of `"POSTFIX"`: P0 O1 S2 T3 F4 I5 X6.

- `s[::-2]` → indices 6, 4, 2, 0 → `X F S P` = `"XFSP"`.
- `s[1:-1:2]` → stop is index 6 (excluded), so indices 1, 3, 5 → `"OTI"`.
- `t = "XFSP" + "OTI" = "XFSPOTI"`.
- `s[5:2]` has the default step +1, but 5 > 2, so the slice is empty and its length is 0.

**Options:**
- (A) re-uses the reversed pattern for the second slice; wrong.
- (B) `XFSPOTI 0` — correct.
- (C) treats `s[5:2]` as if it went backwards and had 3 characters; a positive step never moves leftwards.
- (D) is the full reversal `s[::-1]` — forgets the step of 2.

**Trap:** `s[5:2]` is *not* `s[5:2:-1]`; the default step is +1.''',
            'verify': '''ANSWER = {'A': 'B', 'B': 'A'}.get(ANSWER, ANSWER)

assert OUTPUT.strip() == "XFSPOTI 0"
s = "POSTFIX"
assert s[::-1] == "XIFTSOP" and ANSWER == "A"
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Stacks — postfix evaluation',
            'text': '''The postfix expression below is evaluated using an operand stack. All operators are binary; `^` denotes exponentiation. The tokens are separated by spaces.

`5 9 3 - 2 ^ * 7 4 2 * - +`

The value of the expression is ______.''',
            'answer': '179',
            'solution': '''**Concept:** scan left to right; push operands; on an operator pop the top two values — the **first** pop is the *right* operand, the second pop is the *left* operand — and push the result.

Trace (stack shown bottom → top):
- `5 9 3` → [5, 9, 3]
- `-` → 9 − 3 = 6 → [5, 6]
- `2 ^` → 6^{2} = 36 → [5, 36]
- `*` → 5 × 36 = 180 → [180]
- `7 4 2` → [180, 7, 4, 2]
- `*` → 4 × 2 = 8 → [180, 7, 8]
- `-` → 7 − 8 = −1 → [180, −1]
- `+` → 180 + (−1) = **179**

The maximum stack depth reached is 4 (just after pushing the second 2).

**Trap:** popping in the wrong order turns `9 3 -` into −6 and `7 8 -` into +1, which gives 5 × 36 + 1 = 181 — a very common wrong answer. Always compute *second-pop op first-pop*.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [180, 7, 8],
                    'label': 'S',
                    'caption': "Operand stack just before the first '-' after 7 4 2 *",
                },
            ],
            'verify': '''
st = []
for t in "5 9 3 - 2 ^ * 7 4 2 * - +".split():
    if t.isdigit():
        st.append(int(t))
    else:
        b = st.pop(); a = st.pop()
        st.append({'+': a+b, '-': a-b, '*': a*b, '^': a**b}[t])
assert st == [int(ANSWER)]
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Stacks — infix to postfix conversion',
            'text': '''The infix expression below is converted to postfix using the standard operator-stack algorithm. Precedence: `^` (highest, **right**-associative) > `*`, `/` (left-associative) > `+`, `-` (lowest, left-associative).

`a - b / ( c + d ) * e ^ f ^ g + h`

The postfix form is''',
            'options': [
                '`a b c d + / e f ^ g ^ * - h +`',
                '`a b c d + e f g ^ ^ * / - h +`',
                '`a b c d + / e f g ^ ^ * - h +`',
                '`a b c d + / e f g ^ ^ * h + -`',
            ],
            'answer': 'C',
            'solution': '''**Concept:** an incoming operator pops every stacked operator of *higher* precedence, and also those of *equal* precedence when the incoming operator is left-associative. For a right-associative `^`, an equal `^` is **not** popped.

Grouping: `^` first: e ^ (f ^ g). Then `/` and `*` left to right: (b / (c+d)) * (e^f^g). Then `-` and `+` left to right: (a − that) + h.

Trace of key moments:
- `a` out; `-` pushed; `b` out; `/` pushed above `-`.
- `( c + d )` emits `c d +`.
- `*` arrives: pops `/` (equal precedence, left-assoc) → output so far `a b c d + /`.
- `e`, `^`, `f`, `^` (second `^` does not pop the first), `g` → stack `- * ^ ^`.
- `+` arrives: pops `^ ^ * -` → `... e f g ^ ^ * -`; then `h`, end pops `+`.

Result: `a b c d + / e f g ^ ^ * - h +`.

**Options:** (A) treats `^` as left-associative ((e^f)^g). (B) applies `*` before `/`, breaking left-to-right order. (D) evaluates `h` before the subtraction, i.e. a − (… + h). Only (C) is right.

**Tip:** check associativity of `^` first — it is the most-tested detail.''',
            'verify': '''
prec = {'+':1,'-':1,'*':2,'/':2,'^':3}
out, st = [], []
for t in "a - b / ( c + d ) * e ^ f ^ g + h".split():
    if t.isalpha(): out.append(t)
    elif t == '(': st.append(t)
    elif t == ')':
        while st[-1] != '(': out.append(st.pop())
        st.pop()
    else:
        while st and st[-1] != '(' and (prec[st[-1]] > prec[t] or
              (prec[st[-1]] == prec[t] and t != '^')):
            out.append(st.pop())
        st.append(t)
out += st[::-1]
assert ' '.join(out) == "a b c d + / e f g ^ ^ * - h +"
assert ANSWER == "C"
''',
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Stacks — stack permutations',
            'text': 'The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack **in this order**. Pops may be interleaved with the pushes arbitrarily, and every popped value is written to the output. Which of the following output sequences is/are possible?',
            'options': ['2, 4, 3, 6, 1, 5', '4, 5, 3, 6, 2, 1', '1, 5, 2, 4, 3, 6', '3, 2, 5, 6, 4, 1'],
            'answer': ['B', 'D'],
            'solution': '''**Concept:** simulate greedily — to output x, push every not-yet-pushed value up to x, then x must be on top. Equivalently, a sequence is impossible iff it contains a pattern i < j < k output in the order k … i … j (a '3-1-2' pattern).

- (A) after 2, 4, 3 the stack holds [1]; push 5, 6 and pop 6 → stack [1, 5]. Next we need 1 but 5 is on top. **Impossible** (pattern 6 … 1 … 5).
- (B) push 1–4 pop 4; push 5 pop 5; pop 3; push 6 pop 6; pop 2; pop 1. **Possible.**
- (C) pop 1 at once; push 2–5 pop 5 → stack [2, 3, 4]; we need 2 but 4 is on top. **Impossible** (pattern 5 … 2 … 4).
- (D) push 1,2,3 pop 3; pop 2; push 4,5 pop 5; push 6 pop 6; pop 4; pop 1. **Possible.**

**Trap:** do not check only the first few outputs; (A) looks fine until the last two pops.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [2, 3, 4],
                    'label': 'S',
                    'caption': '(D) after outputting 1 and 5: 2 is buried under 3, 4',
                },
            ],
            'verify': '''_m = {'C': 'B', 'B': 'C'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x:
            st.append(nxt); nxt += 1
        if st[-1] != x: return False
        st.pop()
    return True
opts = [(3,2,5,6,4,1),(2,4,3,6,1,5),(4,5,3,6,2,1),(1,5,2,4,3,6)]
got = [c for c, s in zip("ABCD", opts) if ok(s)]
assert sorted(ANSWER) == got
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Python + stacks — bracket matching',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''def check(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st, peak = [], 0
    for i, ch in enumerate(s):
        if ch in '([{':
            st.append(ch)
            peak = max(peak, len(st))
        elif not st or st.pop() != pairs[ch]:
            return -i
    return peak if not st else len(st)

print(check("{[()()]([{}])}") + check("([)]"))''',
            'answer': '2',
            'solution': '''**Concept:** a stack checks bracket balance — push every opener, and each closer must pop the matching opener. This function returns the peak stack depth for a balanced string, and −(index of the first bad closer) on a mismatch.

**First call** `{[()()]([{}])}` — depth after each character:
- `{`1 `[`2 `(`3 `)`2 `(`3 `)`2 `]`1 `(`2 `[`3 `{`4 `}`3 `]`2 `)`1 `}`0
- Every closer matches and the stack ends empty → returns peak = **4**.

**Second call** `([)]`:
- i = 0 `(` push, i = 1 `[` push.
- i = 2 `)`: pop gives `[` but `pairs[')']` is `(` → mismatch → returns −2.

Printed value: 4 + (−2) = **2**.

**Trap:** `([)]` has equal counts of each bracket type, so a counter-based check would call it balanced; only a stack catches the crossing. Note also that `-i` uses the index of the offending character (2), not the number of characters read (3).''',
            'verify': '''
assert OUTPUT.strip() == ANSWER
assert check("{[()()]([{}])}") == 4 and check("([)]") == -2
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Queues — circular array',
            'text': '''A circular queue is stored in an array `Q[0..5]` (size 6). `front` is the index of the first element and `rear` is the index of the next free slot; the queue is **full** when `(rear + 1) mod 6 == front` (one slot is always left empty). Initially `front = rear = 0`. An enqueue on a full queue is rejected and changes nothing.

The operations performed are: 5 enqueues, then 3 dequeues, then 4 enqueues. The final values of (front, rear) are''',
            'options': ['(3, 2)', '(3, 3)', '(3, 1)', '(4, 2)'],
            'answer': 'A',
            'solution': '''**Concept:** with one slot sacrificed, an array of size 6 holds at most 5 elements; both indices advance modulo 6.

Trace:
- 5 enqueues: rear goes 0 → 5; size 5. Now (5 + 1) mod 6 = 0 = front → **full**.
- 3 dequeues: front goes 0 → 3; size 2.
- Enqueue #1: slot 5 used, rear = 0 (wrap-around); size 3.
- Enqueue #2: rear = 1; size 4.
- Enqueue #3: rear = 2; size 5. Now (2 + 1) mod 6 = 3 = front → full.
- Enqueue #4: rejected.

Final: front = 3, rear = 2 → option **(A)**.

**Options:** (B) accepts the 4th enqueue, ignoring the reserved empty slot. (C) loses one enqueue at the wrap-around. (D) performs an extra dequeue.

**Tip:** with this convention, size = (rear − front + 6) mod 6 = (2 − 3 + 6) mod 6 = 5.''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': ['e7', 'e8', '', 'e4', 'e5', 'e6'],
                    'pointers': {
                        'front': 3,
                        'rear': 2,
                    },
                    'caption': 'Final state (e1..e3 dequeued; e9 rejected)',
                },
            ],
            'verify': '''ANSWER = {'B': 'A', 'A': 'B'}.get(ANSWER, ANSWER)

N = 6; front = rear = 0; size = 0
def enq():
    global rear
    if (rear + 1) % N == front: return False
    rear = (rear + 1) % N; return True
def deq():
    global front
    front = (front + 1) % N
for _ in range(5): enq()
for _ in range(3): deq()
res = [enq() for _ in range(4)]
assert res == [True, True, True, False]
assert ["(3, 3)", "(3, 2)", "(3, 1)", "(4, 2)"]["ABCD".index(ANSWER)] == "(%d, %d)" % (front, rear)
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Hashing — separate chaining',
            'text': 'The keys 23, 46, 14, 57, 35, 68, 9, 80, 19, 41 are inserted in this order into an initially empty hash table with 11 slots using h(k) = k mod 11 and separate chaining (new keys are appended at the end of their chain). Assume each key is equally likely to be searched for. The average number of key comparisons in a **successful** search, rounded off to two decimal places, is ______.',
            'answer': ['1.79', '1.81'],
            'solution': '''**Concept:** in a chain of length L, the key in position p (1-based) costs p comparisons; the chain contributes 1 + 2 + … + L = L(L + 1)/2.

Home slots (k mod 11): 23→1, 46→2, 14→3, 57→2, 35→2, 68→2, 9→9, 80→3, 19→8, 41→8.

Chains:
- slot 1: 23 (L = 1) → 1
- slot 2: 46 → 57 → 35 → 68 (L = 4) → 10
- slot 3: 14 → 80 (L = 2) → 3
- slot 8: 19 → 41 (L = 2) → 3
- slot 9: 9 (L = 1) → 1

Total = 1 + 10 + 3 + 3 + 1 = 18 comparisons over 10 keys → average = **1.80**.

**Trap:** dividing by the table size (11) or using the load factor formula 1 + α/2 = 1.45 gives the *expected* cost for random keys, not the cost for this particular key set.''',
            'solution_diagrams': [
                {
                    'type': 'hashtable',
                    'size': 11,
                    'slots': {
                        1: [23],
                        2: [46, 57, 35, 68],
                        3: [14, 80],
                        8: [19, 41],
                        9: [9],
                    },
                    'caption': 'Final chained table',
                },
            ],
            'verify': '''
ch = {}
for k in [23, 46, 14, 57, 35, 68, 9, 80, 19, 41]:
    ch.setdefault(k % 11, []).append(k)
avg = sum(len(c)*(len(c)+1)/2 for c in ch.values()) / 10
assert float(ANSWER[0]) <= avg <= float(ANSWER[1])
''',
        },
        {
            'type': 'MCQ',
            'marks': 1,
            'topic': 'Linked lists — slow/fast pointers in Python',
            'text': 'Consider the following Python program. What is printed?',
            'code': '''class N:
    def __init__(s, v, nx=None):
        s.v, s.nx = v, nx

h = None
for v in [4, 7, 1, 9, 3]:
    h = N(v, h)
p = q = h
while q and q.nx:
    p, q = p.nx, q.nx.nx
p.nx = p.nx.nx
out = []
while h:
    out.append(h.v)
    h = h.nx
print(out)''',
            'options': ['`[4, 7, 9, 3]`', '`[3, 9, 1, 4]`', '`[3, 9, 7, 4]`', '`[3, 9, 1, 7]`'],
            'answer': 'B',
            'solution': '''**Concept:** `h = N(v, h)` inserts at the **head**, so the list is built in reverse. The slow/fast pointer loop stops with `p` at the middle node; the program then unlinks the node *after* the middle.

- After the loop over `[4, 7, 1, 9, 3]`, the list is 3 → 9 → 1 → 7 → 4.
- p = q = 3. Iteration 1: p = 9, q = 1. Iteration 2: p = 1, q = 4. Now `q.nx` is None → stop.
- `p.nx = p.nx.nx` makes 1 point to 4, skipping 7.
- Traversal prints `[3, 9, 1, 4]`.

**Options:**
- (A) assumes tail insertion (list 4, 7, 1, 9, 3) and deletes 1.
- (C) deletes the middle node itself instead of its successor.
- (D) deletes the last node.

**Trap:** forgetting that prepending reverses the input order.''',
            'solution_diagrams': [
                {
                    'type': 'linkedlist',
                    'values': [3, 9, 1, 4],
                    'head': 'h',
                    'caption': 'List after node 7 is unlinked',
                },
            ],
            'verify': "ANSWER = {'C': 'B', 'B': 'C'}.get(ANSWER, ANSWER)\nassert OUTPUT.strip() == '[3, 9, 1, 4]' and ANSWER == 'C'",
        },
        {
            'type': 'MSQ',
            'marks': 1,
            'topic': 'Heaps — max-heap operations',
            'text': 'The array below (0-based) stores a binary max-heap. Which of the following statements is/are TRUE? (Each statement refers to the original heap.)',
            'diagrams': [
                {
                    'type': 'heap',
                    'values': [92, 75, 88, 40, 61, 80, 17, 12, 33, 59],
                    'caption': 'Max-heap H = [92, 75, 88, 40, 61, 80, 17, 12, 33, 59]',
                },
            ],
            'options': [
                'Inserting 65 (append, then sift-up) leaves 65 at index 1',
                'Inserting 90 (append, then sift-up) performs exactly 2 swaps',
                'The third-largest key, 80, is a child of the root',
                'After one delete-max (last element moved to the root, then sift-down), the array is [88, 75, 80, 40, 61, 59, 17, 12, 33]',
            ],
            'answer': ['B', 'D'],
            'solution': '''**Concept:** children of index i are 2i + 1 and 2i + 2; the parent is ⌊(i − 1)/2⌋.

- (A) 65 at index 10 swaps with 61 (index 4), then its parent 75 is larger → stops at **index 4**. **False.**
- (B) 90 goes to index 10; parent index 4 (61) → swap; parent index 1 (75) → swap; parent index 0 (92) is larger → stop. 2 swaps. **True.**
- (C) The root's children are 75 and 88. 80 is a child of 88, at index 5. **False.**
- (D) Move 59 to the root: [59, 75, 88, 40, 61, 80, 17, 12, 33]. Larger child 88 → swap → 59 at index 2; children 80, 17 → swap with 80 → 59 at index 5 (leaf). Result [88, 75, 80, 40, 61, 59, 17, 12, 33]. **True.**

**Trap:** the k-th largest element of a heap need not be at depth k − 1 or less in any fixed spot; for k = 3 it can be a child *or* a grandchild of the root.''',
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

H = [92, 75, 88, 40, 61, 80, 17, 12, 33, 59]
def delmax(a):
    a = a[:]; a[0] = a.pop(); i = 0
    while True:
        l, r, m = 2*i+1, 2*i+2, i
        if l < len(a) and a[l] > a[m]: m = l
        if r < len(a) and a[r] > a[m]: m = r
        if m == i: return a
        a[i], a[m] = a[m], a[i]; i = m
def ins(a, x):
    a = a[:] + [x]; i = len(a) - 1; sw = 0
    while i and a[(i-1)//2] < a[i]:
        a[i], a[(i-1)//2] = a[(i-1)//2], a[i]; i = (i-1)//2; sw += 1
    return a, sw, i
A = delmax(H) == [88, 75, 80, 40, 61, 59, 17, 12, 33]
B = ins(H, 90)[1] == 2
C = H.index(80) in (1, 2)
D = ins(H, 65)[2] == 1
assert sorted(ANSWER) == [c for c, t in zip("ABCD", [A, B, C, D]) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 1,
            'topic': 'Binary search — counting probes',
            'text': 'Consider the following Python program. The value printed is ______.',
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
    return -c

A = [3, 8, 14, 19, 23, 27, 31, 36, 42, 47, 50, 58, 63]
print(bs(A, 47) - bs(A, 30))''',
            'answer': '6',
            'solution': '''**Concept:** each loop iteration probes one middle element; `bs` returns the probe count for a hit and the *negated* probe count for a miss.

Array has 13 elements, indices 0..12.

**Search 47:**
- lo = 0, hi = 12, mid = 6 → A[6] = 31 < 47 → lo = 7 (c = 1)
- lo = 7, hi = 12, mid = 9 → A[9] = 47 → found, c = **2**

**Search 30 (absent):**
- mid = 6 → 31 > 30 → hi = 5 (c = 1)
- lo = 0, hi = 5, mid = 2 → 14 < 30 → lo = 3 (c = 2)
- lo = 3, hi = 5, mid = 4 → 23 < 30 → lo = 5 (c = 3)
- lo = 5, hi = 5, mid = 5 → 27 < 30 → lo = 6 (c = 4); loop ends → returns **−4**

Printed: 2 − (−4) = **6**.

**Trap:** missing the sign: 2 − 4 = −2 is the most common slip. Also note an unsuccessful search on 13 elements may take 3 or 4 probes (⌊log₂13⌋ + 1 = 4 at most).''',
            'solution_diagrams': [
                {
                    'type': 'array',
                    'values': [3, 8, 14, 19, 23, 27, 31, 36, 42, 47, 50, 58, 63],
                    'highlight': [6, 2, 4, 5],
                    'pointers': {
                        'lo/hi end': 5,
                    },
                    'caption': 'Probes for x = 30: indices 6, 2, 4, 5',
                },
            ],
            'verify': 'assert int(OUTPUT) == int(ANSWER) and bs(A, 47) == 2 and bs(A, 30) == -4',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Stacks — counting stack permutations',
            'text': 'The integers 1, 2, 3, 4, 5, 6 are pushed onto an initially empty stack in this order, with pops interleaved arbitrarily; popped values form the output sequence, and at the end the stack is emptied. The number of distinct output sequences whose **first** element is 4 is ______.',
            'answer': '14',
            'solution': '''**Concept:** an output sequence is fixed by the sequence of push/pop operations, and distinct valid operation sequences give distinct outputs. So we count operation sequences.

**Step 1 — forced prefix.** To output 4 first, we must push 1, 2, 3, 4 and pop 4 immediately (any earlier pop would output something other than 4). The stack is now [1, 2, 3] (3 on top) and inputs 5, 6 remain.

**Step 2 — count the rest.** We still need 2 pushes (U) and 5 pops (D), in any order such that the stack height, starting at 3, never goes below 0.
- Unrestricted arrangements: C(7, 2) = 21.
- Bad paths touch height −1. Reflecting the part before the first touch maps them to paths from −5 to 0 in 7 steps, i.e. U − D = 5, U + D = 7 → U = 6, D = 1: C(7, 1) = 7.
- Good paths: 21 − 7 = **14**.

**Cross-check by cases:** let k = number of pops before 5 is pushed (k = 0..3). The stack then holds 4 − k items, and 6 can be pushed after j = 0, 1, …, 4 − k further pops: 5 − k ways. Total 5 + 4 + 3 + 2 = 14.

**Trap:** answering Catalan(2) = 2 by thinking only about the order of 5 and 6, or answering C₆ = 132 (all stack permutations). The buried 1, 2, 3 must still come out in the order 3, 2, 1 but 5 and 6 can be interleaved among them.''',
            'verify': '''
import itertools
def ok(seq):
    st, nxt = [], 1
    for x in seq:
        while nxt <= x:
            st.append(nxt); nxt += 1
        if st[-1] != x: return False
        st.pop()
    return True
cnt = sum(1 for p in itertools.permutations(range(1, 7)) if p[0] == 4 and ok(p))
assert cnt == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Python + stacks — prefix evaluation',
            'text': 'The function below evaluates a prefix (Polish) expression by scanning it from right to left. What does the program print?',
            'code': '''def ev(tokens):
    st = []
    for t in reversed(tokens):
        if t.isdigit():
            st.append(int(t))
        else:
            a, b = st.pop(), st.pop()
            st.append({'+': a + b, '-': a - b,
                       '*': a * b, '/': a // b}[t])
    return st

print(ev("+ * 3 / - 2 9 4 - 8 5".split()))''',
            'options': ['`[0]`', '`-3`', '`[3]`', '`[-3]`'],
            'answer': 'D',
            'solution': '''**Concept:** for prefix evaluation scanned right-to-left, the **first** value popped is the *left* operand (the reverse of postfix). Here `a` = first pop = left operand — correct. Python's `//` is *floor* division, rounding towards −∞.

Trace (tokens reversed: 5 8 - 4 9 2 - / 3 * +), stack bottom → top:
- push 5, 8 → [5, 8]
- `-`: a = 8, b = 5 → 8 − 5 = 3 → [3]
- push 4, 9, 2 → [3, 4, 9, 2]
- `-`: a = 2, b = 9 → 2 − 9 = −7 → [3, 4, −7]
- `/`: a = −7, b = 4 → −7 // 4 = **−2** (floor of −1.75) → [3, −2]
- push 3 → [3, −2, 3]
- `*`: a = 3, b = −2 → −6 → [3, −6]
- `+`: a = −6, b = 3 → −3 → [−3]

`ev` returns the *list* `st`, so the output is `[-3]`.

(Note: the dict literal evaluates all four expressions each time, but no divisor is ever 0, so no exception arises.)

**Options:**
- (A) `[0]` uses truncation (−7 / 4 → −1, then −3 + 3 = 0) — C-style division, not Python.
- (B) `-3` forgets that a list is returned and printed.
- (C) `[3]` comes from a sign slip in 2 − 9.

**Trap:** `//` with a negative operand — floor, not truncate.''',
            'verify': "assert OUTPUT.strip() == '[-3]' and ANSWER == 'D'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Stacks — infix to postfix, operator-stack trace',
            'text': 'The infix expression `a * ( b + c * d ) - e / f ^ g` is converted to postfix using an operator stack (precedence `^` > `*`, `/` > `+`, `-`; `^` right-associative, others left-associative; `(` is pushed onto the same stack). Which of the following statements is/are TRUE?',
            'options': [
                'With a = 2, b = 3, c = 4, d = 5, e = 64, f = 2, g = 3 the expression evaluates to 38',
                'The postfix expression is `a b c d * + * e f g ^ / -`',
                'The maximum number of symbols (operators and `(`) on the stack at any moment is 4',
                'When `-` is scanned, exactly two operators are popped to the output',
            ],
            'answer': ['A', 'B', 'C'],
            'solution': '''**Concept:** operators wait on the stack until a lower-or-equal precedence operator (or `)` or end of input) forces them out.

Trace (stack bottom → top, output so far):
- `a` → out: a
- `*` → [*]
- `(` → [*, (]
- `b` → out: a b
- `+` → [*, (, +]
- `c` → out: a b c
- `*` → higher than `+`, push → [*, (, +, *] (**size 4**, the maximum)
- `d` → out: a b c d
- `)` → pop `*`, `+`, discard `(` → out: a b c d * + ; stack [*]
- `-` → pops `*` only (stack then empty) → push `-` → out: a b c d * + *
- `e`, `/` (push above `-`), `f`, `^` (push above `/`), `g` → stack [-, /, ^]
- end → pop `^ / -` → final `a b c d * + * e f g ^ / -`.

**Verdicts:**
- (A) 2 × (3 + 4 × 5) − 64 / 2^{3} = 2 × 23 − 64/8 = 46 − 8 = 38. **True.**
- (B) **True** (see final output).
- (C) **True** — size 4 after the inner `*`; later the stack holds at most 3.
- (D) **False** — only one operator (`*`) is on the stack when `-` arrives.

**Trap:** in (D) people forget that `)` already flushed `+` and the inner `*`.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': ['*', '(', '+', '*'],
                    'label': 'ops',
                    'caption': 'Operator stack at its peak (after the inner *)',
                },
            ],
            'verify': '''_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

prec = {'+':1,'-':1,'*':2,'/':2,'^':3}
out, st, peak, popped_at_minus = [], [], 0, None
for t in "a * ( b + c * d ) - e / f ^ g".split():
    if t.isalpha(): out.append(t)
    elif t == '(': st.append(t)
    elif t == ')':
        while st[-1] != '(': out.append(st.pop())
        st.pop()
    else:
        n0 = len(out)
        while st and st[-1] != '(' and (prec[st[-1]] > prec[t] or
              (prec[st[-1]] == prec[t] and t != '^')):
            out.append(st.pop())
        if t == '-': popped_at_minus = len(out) - n0
        st.append(t)
    peak = max(peak, len(st))
out += st[::-1]
a, b, c, d, e, f, g = 2, 3, 4, 5, 64, 2, 3
val = a * (b + c * d) - e / f ** g
truth = [' '.join(out) == "a b c d * + * e f g ^ / -", peak == 4,
         popped_at_minus == 2, val == 38]
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Python — mutable default argument in a Stack class',
            'text': 'Consider the following Python program. The value printed is ______.',
            'code': '''class Stack:
    def __init__(self, items=[]):
        self.items = items
    def push(self, x):
        self.items.append(x)
    def pop(self):
        return self.items.pop()

s1 = Stack()
s2 = Stack()
s3 = Stack([9])
for k in range(1, 5):
    (s1 if k % 2 else s2).push(k * k)
s3.push(s2.pop())
print(sum(s1.items) + len(s2.items) * 10 + s3.pop())''',
            'answer': '60',
            'solution': '''**Concept:** the default list `[]` in `__init__` is created **once** when the function is defined. `s1 = Stack()` and `s2 = Stack()` both store a reference to that same list, so they are two names for one stack. `s3` gets its own list `[9]`.

Trace:
- k = 1 (odd) → s1.push(1) → shared list [1]
- k = 2 (even) → s2.push(4) → shared list [1, 4]
- k = 3 → s1.push(9) → [1, 4, 9]
- k = 4 → s2.push(16) → [1, 4, 9, 16]
- `s2.pop()` removes 16 from the shared list → [1, 4, 9]; `s3` becomes [9, 16].

Final expression:
- `sum(s1.items)` = 1 + 4 + 9 = 14
- `len(s2.items) * 10` = 3 × 10 = 30 (same list!)
- `s3.pop()` = 16

Total = 14 + 30 + 16 = **60**.

**What a naive reading gives:** with independent lists, s1 = [1, 9] (sum 10), s2 = [4] after the pop (length 1 → 10) and s3.pop() = 16, total 36.

**Trap/Tip:** never use a mutable default; write `items=None` and `self.items = [] if items is None else items`.''',
            'solution_diagrams': [
                {
                    'type': 'stack',
                    'values': [1, 4, 9],
                    'label': 'shared',
                    'caption': 'The single list referenced by both s1.items and s2.items',
                },
            ],
            'verify': 'assert int(OUTPUT) == int(ANSWER) and s1.items is s2.items',
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Elementary sorting — selection, insertion, bubble',
            'text': '''The array A = [5, 1, 4, 2, 8, 3] is to be sorted in ascending order. Consider:
- **Selection sort**: in pass i (i = 0..n−2) the minimum of A[i..n−1] is found and swapped into position i; a swap is counted only if the minimum is not already at i.
- **Insertion sort**: a *shift* is one move of an element one position to the right.
- **Bubble sort** with early termination: a pass that makes no swap ends the algorithm (that pass is counted).

Which of the following statements is/are TRUE?''',
            'options': [
                'After 2 passes of selection sort the array is [1, 2, 4, 5, 8, 3]',
                'Bubble sort performs exactly 4 passes',
                'Selection sort performs exactly 4 swaps',
                'Insertion sort performs exactly 7 shifts',
            ],
            'answer': ['A', 'B', 'D'],
            'solution': '''**Concepts:** insertion-sort shifts = number of inversions; selection sort swaps depend on where each minimum sits; bubble sort stops after the first swap-free pass.

**Selection sort** (see table): pass 1 swaps 5↔1; pass 2 swaps 5↔2; pass 3 swaps 4↔3; pass 4 swaps 5↔4; pass 5 swaps 8↔5. Every pass swaps → **5 swaps**. (C) **False**. After 2 passes: [1, 2, 4, 5, 8, 3] → (A) **True**.

**Insertion sort:** inversions of [5, 1, 4, 2, 8, 3] are (5,1), (5,4), (5,2), (5,3), (4,2), (4,3), (8,3) = 7. Each shift removes exactly one inversion → **7 shifts**. (D) **True**.

**Bubble sort:**
- pass 1 → [1, 4, 2, 5, 3, 8]
- pass 2 → [1, 2, 4, 3, 5, 8]
- pass 3 → [1, 2, 3, 4, 5, 8]
- pass 4 → no swap → stop.
So **4 passes**; (B) **True**.

**Trap:** in (B), people stop at 3 because the array is already sorted after pass 3 — but the algorithm only *knows* that after a swap-free pass. In (C), 5 swaps happen because no element is ever already in its final selection position.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Selection sort — array after each pass',
                    'col_labels': ['0', '1', '2', '3', '4', '5'],
                    'row_labels': ['start', 'pass 1', 'pass 2', 'pass 3', 'pass 4', 'pass 5'],
                    'rows': [
                        [5, 1, 4, 2, 8, 3],
                        [1, 5, 4, 2, 8, 3],
                        [1, 2, 4, 5, 8, 3],
                        [1, 2, 3, 5, 8, 4],
                        [1, 2, 3, 4, 8, 5],
                        [1, 2, 3, 4, 5, 8],
                    ],
                    'highlight': [
                        [1, 0],
                        [2, 1],
                        [3, 2],
                        [4, 3],
                        [5, 4],
                    ],
                },
            ],
            'verify': '''_m = {'A': 'B', 'B': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'B': 'D', 'D': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'C', 'C': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

A0 = [5, 1, 4, 2, 8, 3]
a = A0[:]; sw = 0; after2 = None
for i in range(5):
    m = min(range(i, 6), key=lambda j: a[j])
    if m != i:
        a[i], a[m] = a[m], a[i]; sw += 1
    if i == 1: after2 = a[:]
inv = sum(1 for i in range(6) for j in range(i+1, 6) if A0[i] > A0[j])
b = A0[:]; passes = 0
while True:
    passes += 1; s = False
    for j in range(6 - passes):
        if b[j] > b[j+1]:
            b[j], b[j+1] = b[j+1], b[j]; s = True
    if not s: break
truth = [sw == 4, inv == 7, passes == 4, after2 == [1, 2, 4, 5, 8, 3]]
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Quicksort — recursion stack depth',
            'text': 'Consider the quicksort below (Lomuto partition, last element as pivot). It is called as `qs(a, 0, 7, 1)` on `a = [1, 2, 3, 4, 5, 6, 7, 8]`. What does the final `print` show?',
            'code': '''def part(a, lo, hi):
    x, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= x:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1

deepest = calls = 0
def qs(a, lo, hi, d):
    global deepest, calls
    calls += 1
    deepest = max(deepest, d)
    if lo < hi:
        p = part(a, lo, hi)
        qs(a, lo, p - 1, d + 1)
        qs(a, p + 1, hi, d + 1)

a = [1, 2, 3, 4, 5, 6, 7, 8]
qs(a, 0, 7, 1)
print(deepest, calls)''',
            'options': ['`7 15`', '`8 8`', '`8 15`', '`8 16`'],
            'answer': 'C',
            'solution': '''**Concept:** on already-sorted input, Lomuto with the last element as pivot always puts the pivot at `hi`, so the left part has size n − 1 and the right part is empty — the worst case, with recursion depth Θ(n) and running time Θ(n²) (T(n) = T(n − 1) + Θ(n)).

**Depth:** the subarray sizes along the left spine are 8, 7, 6, 5, 4, 3, 2, 1 at depths 1, 2, …, 8. The size-1 call (lo = hi) still executes `calls += 1` and updates `deepest` before failing the `lo < hi` test. So `deepest` = **8**.

**Calls:** every call with lo < hi (sizes 8 down to 2: 7 calls) partitions and makes exactly 2 further calls. Counting the root: calls = 1 + 2 × 7 = **15** (the 7 empty right-side calls and the one size-1 call are included).

Output: `8 15`.

**Options:**
- (A) `7 15` stops the depth at the last *partitioning* call (size 2) and forgets that the size-1 call also records its depth.
- (B) counts only the left-spine calls.
- (D) counts an extra call; a quicksort recursion tree is a full binary tree with 7 internal nodes and therefore exactly 8 leaves, 15 nodes.

**Tip:** recursing on the smaller side first (and looping on the larger) bounds the stack depth by O(log n) even in this worst case.''',
            'verify': "ANSWER = {'B': 'C', 'C': 'B'}.get(ANSWER, ANSWER)\nassert OUTPUT.split() == ['8', '15'] and ANSWER == 'B'",
        },
        {
            'type': 'MSQ',
            'marks': 2,
            'topic': 'Graph traversal — iterative DFS with an explicit stack',
            'text': '''The following iterative DFS is run on the undirected graph shown, starting at A:

Initially `stack = [A]` and `visited = []`.
Repeat while the stack is non-empty: pop u; if u is already visited, skip it; otherwise append u to `visited` and push every **unvisited** neighbour of u onto the stack in **alphabetical order** (so the alphabetically last neighbour ends on top).

Which of the following statements is/are TRUE?''',
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 1],
                        'D': [2, 0],
                        'E': [4, 2],
                        'F': [4, 0],
                        'G': [6, 1],
                    },
                    'caption': 'Undirected graph',
                },
            ],
            'options': [
                'The visiting order equals that of recursive DFS that explores neighbours alphabetically',
                'Vertex C is pushed onto the stack exactly 3 times',
                'The maximum number of entries on the stack at any moment is 5',
                'The visiting order is A, D, F, G, E, C, B',
            ],
            'answer': ['B', 'C', 'D'],
            'solution': '''**Concept:** pushing neighbours in alphabetical order makes the *last* one pop first, so the traversal goes 'reverse-alphabetical'. Because a vertex may be pushed several times (it is only checked when popped), stack entries can exceed |V| − 1 in general.

Trace (stack bottom → top after processing u):
- pop A → visit A; push B, C, D → [B, C, D]
- pop D → visit D; push F → [B, C, F]
- pop F → visit F; unvisited nbrs C, G → [B, C, C, G]
- pop G → visit G; push E → [B, C, C, E]
- pop E → visit E; unvisited nbrs B, C → [B, C, C, B, C] (**5 entries**)
- pop C → visit C; no unvisited nbrs → [B, C, C, B]
- pop B → visit B → [B, C, C]; the remaining entries are popped and skipped.

Visiting order: **A, D, F, G, E, C, B**.

**Verdicts:**
- (A) **False** — recursive alphabetical DFS gives A, B, E, C, F, D, G.
- (B) C is pushed by A, by F and by E → 3 times. **True.**
- (C) **True** — peak is 5, right after E is processed.
- (D) **True.**

**Trap:** assuming an explicit-stack DFS automatically reproduces the recursive order; to do that you must push neighbours in *reverse* order.''',
            'solution_diagrams': [
                {
                    'type': 'graph',
                    'directed': False,
                    'nodes': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                    'edges': [
                        ['A', 'B'],
                        ['A', 'C'],
                        ['A', 'D'],
                        ['B', 'E'],
                        ['C', 'E'],
                        ['C', 'F'],
                        ['D', 'F'],
                        ['E', 'G'],
                        ['F', 'G'],
                    ],
                    'pos': {
                        'A': [0, 1],
                        'B': [2, 2],
                        'C': [2, 1],
                        'D': [2, 0],
                        'E': [4, 2],
                        'F': [4, 0],
                        'G': [6, 1],
                    },
                    'highlight_edges': [
                        ['A', 'D'],
                        ['D', 'F'],
                        ['F', 'G'],
                        ['G', 'E'],
                        ['E', 'C'],
                        ['E', 'B'],
                    ],
                    'caption': 'DFS tree of the iterative traversal (vertex → the one that pushed it when it was visited)',
                },
            ],
            'verify': '''_m = {'B': 'A', 'A': 'B'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)
_m = {'A': 'D', 'D': 'A'}; ANSWER = sorted(_m.get(a, a) for a in ANSWER) if isinstance(ANSWER, list) else _m.get(ANSWER, ANSWER)

E = [('A','B'),('A','C'),('A','D'),('B','E'),('C','E'),('C','F'),('D','F'),('E','G'),('F','G')]
G = {}
for u, v in E:
    G.setdefault(u, []).append(v); G.setdefault(v, []).append(u)
for k in G: G[k].sort()
st, vis, peak, pushC = ['A'], [], 1, 0
while st:
    u = st.pop()
    if u in vis: continue
    vis.append(u)
    for v in G[u]:
        if v not in vis:
            st.append(v); pushC += (v == 'C')
    peak = max(peak, len(st))
rec = []
def dfs(u):
    rec.append(u)
    for v in G[u]:
        if v not in rec: dfs(v)
dfs('A')
truth = [vis == list("ADFGECB"), vis == rec, peak == 5, pushC == 3]
assert sorted(ANSWER) == [x for x, t in zip("ABCD", truth) if t]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Queue using two stacks — operation count',
            'text': '''A queue is implemented with two stacks S1 and S2. **Enqueue(x)** pushes x onto S1. **Dequeue()**: if S2 is empty, pop every element of S1 and push it onto S2; then pop S2. Each individual push or pop on S1 or S2 costs 1 (so moving one element costs 2).

Starting with both stacks empty, the following 12 operations are performed (E = enqueue, D = dequeue):

E  E  E  D  E  E  D  D  D  E  D  D

The total cost of the sequence is ______.''',
            'answer': '24',
            'solution': '''**Concept:** each element is pushed onto S1 once, moved to S2 at most once (cost 2) and popped from S2 once — at most 4 stack operations per element, so the amortised cost per queue operation is O(1). Here we count exactly.

Trace (sizes of S1 / S2 after each operation):
- E, E, E: 3 pushes → cost 3; S1 = 3, S2 = 0
- D: S2 empty → move 3 elements (6) + pop (1) = 7 → total 10; S1 = 0, S2 = 2
- E, E: cost 2 → total 12; S1 = 2, S2 = 2
- D: pop S2 (1) → 13; S2 = 1
- D: pop S2 (1) → 14; S2 = 0
- D: move 2 (4) + pop (1) = 5 → 19; S1 = 0, S2 = 1
- E: 1 → 20; S1 = 1
- D: pop S2 (1) → 21; S2 = 0
- D: move 1 (2) + pop (1) = 3 → **24**

Check with the per-element bound: 6 elements × (1 push + 2 move + 1 pop) = 24 — every element was transferred exactly once, so the bound is attained.

**Trap:** counting a transfer as cost 1 per element (giving 18), or moving S1 into S2 when S2 is *not* empty, which would also break FIFO order.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Stack sizes and running cost',
                    'col_labels': ['op', 'S1', 'S2', 'cost', 'total'],
                    'row_labels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
                    'rows': [
                        ['E', 1, 0, 1, 1],
                        ['E', 2, 0, 1, 2],
                        ['E', 3, 0, 1, 3],
                        ['D', 0, 2, 7, 10],
                        ['E', 1, 2, 1, 11],
                        ['E', 2, 2, 1, 12],
                        ['D', 2, 1, 1, 13],
                        ['D', 2, 0, 1, 14],
                        ['D', 0, 1, 5, 19],
                        ['E', 1, 1, 1, 20],
                        ['D', 1, 0, 1, 21],
                        ['D', 0, 0, 3, 24],
                    ],
                    'highlight': [
                        [3, 3],
                        [8, 3],
                        [11, 3],
                    ],
                },
            ],
            'verify': '''
s1, s2, ops, out, nxt = [], [], 0, [], 0
for o in "E E E D E E D D D E D D".split():
    if o == 'E':
        s1.append(nxt); nxt += 1; ops += 1
    else:
        if not s2:
            while s1:
                s2.append(s1.pop()); ops += 2
        out.append(s2.pop()); ops += 1
assert out == list(range(6)) and ops == int(ANSWER)
''',
        },
        {
            'type': 'MCQ',
            'marks': 2,
            'topic': 'Binary search trees — deletion',
            'text': 'The keys 45, 27, 63, 12, 38, 51, 80, 33, 40, 70, 56 are inserted in this order into an initially empty binary search tree (shown below). Then 45 is deleted and afterwards 27 is deleted. A node with two children is deleted by copying its **in-order successor** into it and deleting the successor. The post-order traversal of the final tree is',
            'diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        45,
                        [
                            27,
                            [12],
                            [
                                38,
                                [33],
                                [40],
                            ],
                        ],
                        [
                            63,
                            [
                                51,
                                None,
                                [56],
                            ],
                            [
                                80,
                                [70],
                                None,
                            ],
                        ],
                    ],
                    'caption': 'BST after all insertions',
                },
            ],
            'options': [
                '12, 40, 38, 33, 56, 70, 80, 63, 51',
                '40, 12, 38, 33, 56, 70, 80, 63, 51',
                '12, 33, 40, 38, 56, 70, 80, 63, 51',
                '12, 38, 40, 33, 70, 56, 80, 63, 51',
            ],
            'answer': 'A',
            'solution': '''**Concept:** the in-order successor of a node with two children is the minimum of its right subtree; it has no left child, so removing it is easy (splice in its right child).

**Delete 45:** successor = min of right subtree 63 → 51 → 51 (no left child). Copy 51 into the root; remove 51 from its old place, its right child 56 takes its place as left child of 63.

**Delete 27:** two children; successor = min of right subtree 38 → 33. Copy 33 into 27's node; delete the leaf 33. Node 38 now has only the right child 40.

Final tree: root 51; left 33 (children 12, and 38 → right 40); right 63 (children 56 and 80 → left 70).

Post-order (left, right, root):
- left subtree of 33: 12; right subtree: 40, 38; then 33 → 12, 40, 38, 33
- right subtree: 56, then 70, 80, then 63 → 56, 70, 80, 63
- root 51

Result: **12, 40, 38, 33, 56, 70, 80, 63, 51** → (A).

**Options:** (C) puts 33 before 40 — that is not a valid post-order for this tree (38's subtree contains only 40). (B) lists 40 first as if it were the leftmost leaf. (D) swaps the order inside both subtrees.

**Trap:** using the in-order *predecessor* (40 for 45, 12 for 27) produces a different tree.''',
            'solution_diagrams': [
                {
                    'type': 'bintree',
                    'tree': [
                        51,
                        [
                            33,
                            [12],
                            [
                                38,
                                None,
                                [40],
                            ],
                        ],
                        [
                            63,
                            [56],
                            [
                                80,
                                [70],
                                None,
                            ],
                        ],
                    ],
                    'highlight': [51, 33],
                    'caption': 'Final BST after deleting 45 and 27',
                },
            ],
            'verify': '''ANSWER = {'C': 'A', 'A': 'C'}.get(ANSWER, ANSWER)

def ins(t, k):
    if t is None: return [k, None, None]
    if k < t[0]: t[1] = ins(t[1], k)
    else: t[2] = ins(t[2], k)
    return t
def dele(t, k):
    if t is None: return None
    if k < t[0]: t[1] = dele(t[1], k)
    elif k > t[0]: t[2] = dele(t[2], k)
    else:
        if t[1] is None: return t[2]
        if t[2] is None: return t[1]
        s = t[2]
        while s[1]: s = s[1]
        t[0] = s[0]; t[2] = dele(t[2], s[0])
    return t
def post(t): return [] if t is None else post(t[1]) + post(t[2]) + [t[0]]
T = None
for k in [45, 27, 63, 12, 38, 51, 80, 33, 40, 70, 56]: T = ins(T, k)
T = dele(dele(T, 45), 27)
opts = ["12, 33, 40, 38, 56, 70, 80, 63, 51", "40, 12, 38, 33, 56, 70, 80, 63, 51",
        "12, 40, 38, 33, 56, 70, 80, 63, 51", "12, 38, 40, 33, 70, 56, 80, 63, 51"]
good = [c for c, o in zip("ABCD", opts) if [int(x) for x in o.split(", ")] == post(T)]
assert good == [ANSWER]
''',
        },
        {
            'type': 'NAT',
            'marks': 2,
            'topic': 'Shortest paths — Dijkstra',
            'text': "Dijkstra's algorithm is run from source S on the weighted directed graph shown. Let d(v) be the final shortest-path distance of v. The value of d(A) + d(B) + d(C) + d(D) + d(E) is ______.",
            'diagrams': [
                {
                    'type': 'graph',
                    'directed': True,
                    'nodes': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'edges': [
                        ['S', 'A', 7],
                        ['S', 'B', 2],
                        ['B', 'A', 3],
                        ['B', 'D', 8],
                        ['A', 'C', 2],
                        ['A', 'D', 6],
                        ['C', 'D', 1],
                        ['C', 'E', 9],
                        ['D', 'E', 3],
                    ],
                    'pos': {
                        'S': [0, 1],
                        'A': [2, 2],
                        'B': [2, 0],
                        'C': [4, 2],
                        'D': [4, 0],
                        'E': [6, 1],
                    },
                    'caption': 'Weighted digraph',
                },
            ],
            'answer': '33',
            'solution': '''**Concept:** Dijkstra repeatedly extracts the unfinished vertex with the smallest tentative distance and relaxes its outgoing edges; with non-negative weights each extracted distance is final.

Trace (see table):
- Extract S (0): A = 7, B = 2.
- Extract B (2): A = min(7, 2 + 3) = 5; D = 2 + 8 = 10.
- Extract A (5): C = 5 + 2 = 7; D = min(10, 5 + 6) = 10 (unchanged).
- Extract C (7): D = min(10, 7 + 1) = 8; E = 7 + 9 = 16.
- Extract D (8): E = min(16, 8 + 3) = 11.
- Extract E (11).

Final: d(A) = 5, d(B) = 2, d(C) = 7, d(D) = 8, d(E) = 11 → sum = **33**.

Shortest-path tree: S→B, B→A, A→C, C→D, D→E — a single chain, so every vertex's path goes through all earlier ones.

**Trap:** stopping at the first finite estimate (A = 7 via the direct edge, D = 10 via B) gives 7 + 2 + 9 + 10 + 13 = 41. The direct edge is not the shortest when a detour through a cheap vertex exists.''',
            'solution_diagrams': [
                {
                    'type': 'matrix',
                    'title': 'Tentative distances after each extraction',
                    'col_labels': ['S', 'A', 'B', 'C', 'D', 'E'],
                    'row_labels': ['init', 'S', 'B', 'A', 'C', 'D'],
                    'rows': [
                        [0, '∞', '∞', '∞', '∞', '∞'],
                        [0, 7, 2, '∞', '∞', '∞'],
                        [0, 5, 2, '∞', 10, '∞'],
                        [0, 5, 2, 7, 10, '∞'],
                        [0, 5, 2, 7, 8, 16],
                        [0, 5, 2, 7, 8, 11],
                    ],
                },
            ],
            'verify': '''
import heapq
W = {'S':[('A',7),('B',2)], 'B':[('A',3),('D',8)], 'A':[('C',2),('D',6)],
     'C':[('D',1),('E',9)], 'D':[('E',3)], 'E':[]}
d = {v: float('inf') for v in W}; d['S'] = 0; pq = [(0, 'S')]
while pq:
    du, u = heapq.heappop(pq)
    if du > d[u]: continue
    for v, w in W[u]:
        if du + w < d[v]:
            d[v] = du + w; heapq.heappush(pq, (d[v], v))
assert sum(d.values()) == int(ANSWER)
''',
        },
    ],
}
