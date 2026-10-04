# -*- coding: utf-8 -*-
"""GATE DA question bank: Reasoning under uncertainty
(probability for AI, conditional independence, Bayesian networks,
exact inference / variable elimination, approximate inference by sampling).

All numeric answers and d-separation claims were verified by brute-force
enumeration over the joint distribution (and networkx.is_d_separator).
"""

# ---------------------------------------------------------------------------
# Re-usable network descriptions (plain text, ReportLab-safe)
# ---------------------------------------------------------------------------
SPR = ("Consider the Bayesian network over Boolean variables Cloudy (C), Sprinkler (S), Rain (R) and "
       "WetGrass (W) with edges C → S, C → R, S → W, R → W and CPTs: P(c) = 0.5; "
       "P(s | c) = 0.1, P(s | ¬c) = 0.5; P(r | c) = 0.8, P(r | ¬c) = 0.2; "
       "P(w | s, r) = 0.99, P(w | s, ¬r) = 0.90, P(w | ¬s, r) = 0.90, P(w | ¬s, ¬r) = 0.0. ")

ALARM = ("Consider the Bayesian network over Boolean variables Burglary (B), Earthquake (E), Alarm (A), "
         "JohnCalls (J), MaryCalls (M) with edges B → A, E → A, A → J, A → M and CPTs: P(b) = 0.02, P(e) = 0.01; "
         "P(a | b, e) = 0.95, P(a | b, ¬e) = 0.90, P(a | ¬b, e) = 0.30, P(a | ¬b, ¬e) = 0.01; "
         "P(j | a) = 0.8, P(j | ¬a) = 0.05; P(m | a) = 0.7, P(m | ¬a) = 0.02. ")

XYZ = ("A full joint distribution over Boolean variables X, Y, Z is: "
       "P(x, y, z) = 0.10, P(x, y, ¬z) = 0.05, P(x, ¬y, z) = 0.15, P(x, ¬y, ¬z) = 0.10, "
       "P(¬x, y, z) = 0.05, P(¬x, y, ¬z) = 0.20, P(¬x, ¬y, z) = 0.15, P(¬x, ¬y, ¬z) = 0.20. ")

G1 = ("Consider the Bayesian network (DAG) with edges A → C, B → C, C → D, D → E, B → F. ")

G2 = ("Consider the Bayesian network (DAG) with edges A → B, A → C, B → D, C → D, E → D, D → F, C → G, H → G. ")

G3 = ("Consider the Bayesian network (DAG) with edges P → Q, P → R, Q → S, R → S, S → T, U → R. ")

CC = ("A Bayesian network has edges C → A and C → B (Boolean variables) with P(c) = 0.4, "
      "P(a | c) = 0.9, P(a | ¬c) = 0.2, P(b | c) = 0.7, P(b | ¬c) = 0.1. ")

EA = ("A Bayesian network has edges A → C and B → C (Boolean variables) with P(a) = 0.1, P(b) = 0.2, "
      "P(c | a, b) = 0.95, P(c | a, ¬b) = 0.90, P(c | ¬a, b) = 0.80, P(c | ¬a, ¬b) = 0.05. ")

BANK = [
    # =======================================================================
    # PROBABILITY FOR AI
    # =======================================================================
    {"topic": "Probability for AI", "type": "MCQ", "marks": 1,
     "q": "While answering a query P(Cavity | toothache), the unnormalized vector obtained for "
          "Cavity = ⟨true, false⟩ is ⟨0.12, 0.08⟩. Which option gives the normalization constant α and the "
          "resulting posterior distribution?",
     "options": ["α = 5, P(Cavity | toothache) = ⟨0.6, 0.4⟩",
                 "α = 0.2, P(Cavity | toothache) = ⟨0.024, 0.016⟩",
                 "α = 5, P(Cavity | toothache) = ⟨0.4, 0.6⟩",
                 "α = 2, P(Cavity | toothache) = ⟨0.24, 0.16⟩"],
     "answer": [0],
     "solution": "The entries must sum to 1 after scaling, so α = 1/(0.12 + 0.08) = 1/0.20 = 5. "
                 "Then α⟨0.12, 0.08⟩ = ⟨0.6, 0.4⟩. α = 0.2 is the sum itself (multiplying by it does not normalize), "
                 "⟨0.4, 0.6⟩ swaps the order of the values, and α = 2 gives entries summing to 0.4, not 1."},

    {"topic": "Probability for AI", "type": "NAT", "marks": 2,
     "q": "A disease D has prior P(d) = 0.01. A test has P(+ | d) = 0.9 and P(+ | ¬d) = 0.05. "
          "The test is performed twice; the two results are conditionally independent given D. "
          "Both tests come out positive. Compute P(d | +, +). (Round to 3 decimal places.)",
     "answer": {"lo": 0.765, "hi": 0.767},
     "solution": "By Bayes rule with conditional independence, P(d | +, +) = α P(+ | d)² P(d). "
                 "Unnormalized for d: 0.9² × 0.01 = 0.81 × 0.01 = 0.0081. For ¬d: 0.05² × 0.99 = 0.0025 × 0.99 = 0.002475. "
                 "Normalizing: 0.0081 / (0.0081 + 0.002475) = 0.0081 / 0.010575 ≈ 0.766. "
                 "(For comparison, a single positive test gives only 0.009/0.0585 ≈ 0.154.)"},

    {"topic": "Probability for AI", "type": "MSQ", "marks": 2,
     "q": "A hidden variable H takes values h<sub>1</sub>, h<sub>2</sub>, h<sub>3</sub> with prior probabilities 0.5, 0.3, 0.2. "
          "For an observation e, P(e | h<sub>1</sub>) = 0.1, P(e | h<sub>2</sub>) = 0.4, P(e | h<sub>3</sub>) = 0.7. "
          "Which of the following are correct?",
     "options": ["P(e) = 0.31", "P(h<sub>3</sub> | e) ≈ 0.452", "P(h<sub>1</sub> | e) ≈ 0.161",
                 "The most probable hypothesis after observing e (MAP) is h<sub>2</sub>"],
     "answer": [0, 1, 2],
     "solution": "Unnormalized posteriors P(e | h<sub>i</sub>)P(h<sub>i</sub>): 0.1 × 0.5 = 0.05, 0.4 × 0.3 = 0.12, 0.7 × 0.2 = 0.14. "
                 "Marginalizing, P(e) = 0.05 + 0.12 + 0.14 = 0.31 (A true). "
                 "P(h<sub>3</sub> | e) = 0.14/0.31 ≈ 0.452 (B true); P(h<sub>1</sub> | e) = 0.05/0.31 ≈ 0.161 (C true); P(h<sub>2</sub> | e) = 0.12/0.31 ≈ 0.387. "
                 "The MAP hypothesis is h<sub>3</sub> (largest posterior), even though it had the smallest prior, so (D) is false."},

    {"topic": "Probability for AI", "type": "NAT", "marks": 1,
     "q": "A domain has four Boolean random variables and one random variable with 3 possible values. "
          "How many independent numbers are needed to specify an arbitrary full joint distribution over these five variables?",
     "answer": {"lo": 47, "hi": 47},
     "solution": "The full joint table has 2<sup>4</sup> × 3 = 48 entries. "
                 "Because the entries must sum to 1, one of them is determined by the rest, giving 48 − 1 = 47 independent numbers. "
                 "No independence assumptions are made, so no further reduction is possible."},

    {"topic": "Probability for AI", "type": "MSQ", "marks": 1,
     "q": "Let A and B be Boolean random variables with P(b) &gt; 0 and P(¬b) &gt; 0. Which of the following identities hold for <b>every</b> such distribution?",
     "options": ["P(a ∧ b) = P(a | b) P(b)",
                 "P(a | b) = P(b | a) P(a) / P(b)",
                 "P(a | b) + P(a | ¬b) = 1",
                 "P(a) = P(a | b) P(b) + P(a | ¬b) P(¬b)"],
     "answer": [0, 1, 3],
     "solution": "(A) is the product rule. (B) is Bayes rule, derived from writing P(a ∧ b) in two ways via the product rule. "
                 "(D) is the conditioning rule (marginalization of P(a, B) with the product rule). "
                 "(C) is false: conditional distributions sum to 1 over the values of the <i>conditioned</i> variable "
                 "(P(a | b) + P(¬a | b) = 1), not over the conditioning variable; e.g. if A ⊥ B with P(a) = 0.9, "
                 "then P(a | b) + P(a | ¬b) = 0.9 + 0.9 = 1.8."},

    {"topic": "Probability for AI", "type": "MSQ", "marks": 2,
     "q": "For arbitrary random variables X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>, X<sub>4</sub> (no independence assumed), "
          "which of the following expressions are always equal to P(x<sub>1</sub>, x<sub>2</sub>, x<sub>3</sub>, x<sub>4</sub>)?",
     "options": ["P(x<sub>4</sub> | x<sub>3</sub>) P(x<sub>3</sub> | x<sub>2</sub>) P(x<sub>2</sub> | x<sub>1</sub>) P(x<sub>1</sub>)",
                 "P(x<sub>4</sub> | x<sub>1</sub>, x<sub>2</sub>, x<sub>3</sub>) P(x<sub>3</sub> | x<sub>1</sub>, x<sub>2</sub>) P(x<sub>2</sub> | x<sub>1</sub>) P(x<sub>1</sub>)",
                 "P(x<sub>1</sub> | x<sub>2</sub>, x<sub>3</sub>, x<sub>4</sub>) P(x<sub>2</sub> | x<sub>3</sub>, x<sub>4</sub>) P(x<sub>3</sub> | x<sub>4</sub>) P(x<sub>4</sub>)",
                 "P(x<sub>4</sub> | x<sub>1</sub>, x<sub>2</sub>, x<sub>3</sub>) P(x<sub>3</sub> | x<sub>2</sub>) P(x<sub>2</sub> | x<sub>1</sub>) P(x<sub>1</sub>)"],
     "answer": [1, 2],
     "solution": "The chain rule P(x<sub>1</sub>, …, x<sub>n</sub>) = ∏<sub>i</sub> P(x<sub>i</sub> | x<sub>1</sub>, …, x<sub>i−1</sub>) holds for any ordering of the variables. "
                 "(B) is the chain rule for order X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>, X<sub>4</sub>; (C) is the chain rule for the reverse order X<sub>4</sub>, X<sub>3</sub>, X<sub>2</sub>, X<sub>1</sub>. "
                 "(A) drops conditioning variables, which is valid only under Markov-chain independence assumptions. "
                 "(D) replaces P(x<sub>3</sub> | x<sub>1</sub>, x<sub>2</sub>) by P(x<sub>3</sub> | x<sub>2</sub>), which needs X<sub>3</sub> ⊥ X<sub>1</sub> | X<sub>2</sub>, not generally true."},

    {"topic": "Probability for AI", "type": "NAT", "marks": 2,
     "q": XYZ + "Compute P(x | y ∨ z). (Round to 3 decimal places.)",
     "answer": {"lo": 0.428, "hi": 0.429},
     "solution": "P(y ∨ z) = 1 − P(¬y ∧ ¬z) = 1 − [P(x, ¬y, ¬z) + P(¬x, ¬y, ¬z)] = 1 − (0.10 + 0.20) = 0.70. "
                 "P(x ∧ (y ∨ z)) = P(x, y, z) + P(x, y, ¬z) + P(x, ¬y, z) = 0.10 + 0.05 + 0.15 = 0.30. "
                 "Therefore P(x | y ∨ z) = 0.30 / 0.70 ≈ 0.4286 ≈ 0.429."},

    {"topic": "Probability for AI", "type": "MSQ", "marks": 2,
     "q": XYZ + "Which of the following statements are true?",
     "options": ["P(x) = 0.4",
                 "X ⊥ Y (X and Y are marginally independent)",
                 "X ⊥ Y | Z",
                 "P(y | ¬z) ≈ 0.455"],
     "answer": [0, 3],
     "solution": "P(x) = 0.10 + 0.05 + 0.15 + 0.10 = 0.40, so (A) is true. "
                 "P(y) = 0.10 + 0.05 + 0.05 + 0.20 = 0.40 and P(x, y) = 0.15 ≠ 0.4 × 0.4 = 0.16, so (B) is false. "
                 "Given z: P(z) = 0.45, P(x, y | z) = 0.10/0.45 ≈ 0.222, while P(x | z)P(y | z) = (0.25/0.45)(0.15/0.45) ≈ 0.556 × 0.333 ≈ 0.185, so (C) is false. "
                 "P(¬z) = 0.55 and P(y, ¬z) = 0.05 + 0.20 = 0.25, so P(y | ¬z) = 0.25/0.55 ≈ 0.4545, making (D) true."},

    {"topic": "Probability for AI", "type": "MCQ", "marks": 1,
     "q": "For random variables Y and Z, which expression is the <i>conditioning</i> rule for computing the marginal P(Y)?",
     "options": ["P(Y) = ∑<sub>z</sub> P(Y | z) P(z)",
                 "P(Y) = ∑<sub>z</sub> P(z | Y) P(Y)",
                 "P(Y) = ∏<sub>z</sub> P(Y | z)",
                 "P(Y) = ∑<sub>z</sub> P(Y | z)"],
     "answer": [0],
     "solution": "Marginalization gives P(Y) = ∑<sub>z</sub> P(Y, z), and the product rule rewrites P(Y, z) = P(Y | z)P(z); "
                 "together this is the conditioning rule (A). "
                 "(B) equals P(Y)∑<sub>z</sub>P(z | Y) = P(Y), which is circular since it needs P(Y). "
                 "(C) multiplies probabilities and is not a marginal. (D) omits the weights P(z) and need not even be ≤ 1."},

    {"topic": "Probability for AI", "type": "MCQ", "marks": 1,
     "q": "Given P(b | a) = 0.8, P(a) = 0.25 and P(b) = 0.4, what is P(a | b)?",
     "options": ["0.50", "0.32", "0.20", "0.80"],
     "answer": [0],
     "solution": "By Bayes rule, P(a | b) = P(b | a)P(a)/P(b) = 0.8 × 0.25 / 0.4 = 0.2 / 0.4 = 0.5. "
                 "0.32 = 0.8 × 0.4 multiplies by P(b) instead of dividing; 0.20 = P(a ∧ b) is the joint, not the conditional; "
                 "0.80 confuses P(a | b) with P(b | a)."},

    {"topic": "Probability for AI", "type": "MSQ", "marks": 1,
     "q": "A and B are independent Boolean variables with P(a) = 0.4 and P(b) = 0.5. Which statements are true?",
     "options": ["P(a ∨ b) = 0.7", "P(a | b) = 0.4", "P(¬a ∧ ¬b) = 0.3", "P(a ∧ ¬b) = 0.25"],
     "answer": [0, 1, 2],
     "solution": "Independence gives P(a ∧ b) = 0.4 × 0.5 = 0.2, so P(a ∨ b) = 0.4 + 0.5 − 0.2 = 0.7 (A true). "
                 "Independence means P(a | b) = P(a) = 0.4 (B true). "
                 "P(¬a ∧ ¬b) = 0.6 × 0.5 = 0.3 (C true). "
                 "P(a ∧ ¬b) = 0.4 × 0.5 = 0.2, not 0.25 (D false)."},

    {"topic": "Probability for AI", "type": "MCQ", "marks": 1,
     "q": "If n Boolean random variables are mutually (absolutely) independent, how many independent numbers suffice to specify their full joint distribution?",
     "options": ["n", "2<sup>n</sup> − 1", "2n", "n<sup>2</sup>"],
     "answer": [0],
     "solution": "Under mutual independence P(x<sub>1</sub>, …, x<sub>n</sub>) = ∏ P(x<sub>i</sub>), and each Boolean marginal needs one number P(x<sub>i</sub> = true). "
                 "Hence n numbers suffice. 2<sup>n</sup> − 1 is the count with no independence; 2n double-counts P(¬x<sub>i</sub>) = 1 − P(x<sub>i</sub>); "
                 "n<sup>2</sup> has no basis."},

    {"topic": "Probability for AI", "type": "NAT", "marks": 2,
     "q": "P(cavity) = 0.2. Toothache and Catch are conditionally independent given Cavity with "
          "P(toothache | cavity) = 0.6, P(toothache | ¬cavity) = 0.1, P(catch | cavity) = 0.9, P(catch | ¬cavity) = 0.2. "
          "Compute P(cavity | toothache, catch). (Round to 3 decimal places.)",
     "answer": {"lo": 0.870, "hi": 0.872},
     "solution": "Using conditional independence, P(Cavity | toothache, catch) = α P(toothache | Cavity) P(catch | Cavity) P(Cavity). "
                 "For cavity: 0.6 × 0.9 × 0.2 = 0.108. For ¬cavity: 0.1 × 0.2 × 0.8 = 0.016. "
                 "α = 1/(0.108 + 0.016) = 1/0.124, so P(cavity | toothache, catch) = 0.108/0.124 ≈ 0.871."},

    {"topic": "Probability for AI", "type": "MCQ", "marks": 2,
     "q": "The prior odds of hypothesis h against ¬h are 1 : 4. Evidence e has likelihood ratio P(e | h)/P(e | ¬h) = 6. "
          "What is P(h | e)?",
     "options": ["0.600", "0.857", "0.250", "0.200"],
     "answer": [0],
     "solution": "Bayes rule in odds form: posterior odds = likelihood ratio × prior odds = 6 × (1/4) = 1.5. "
                 "Then P(h | e) = 1.5/(1 + 1.5) = 0.6. "
                 "Check directly: P(h) = 0.2; with P(e | h) = 6k and P(e | ¬h) = k, P(h | e) = 1.2k/(1.2k + 0.8k) = 0.6. "
                 "0.857 = 6/7 ignores the prior, 0.250 reads the prior odds 1 : 4 as a probability, and 0.200 is the prior P(h) = 1/5, ignoring the evidence."},

    {"topic": "Probability for AI", "type": "MCQ", "marks": 1,
     "q": "In AIMA's enumeration-style inference, P(X | e) is computed as α P(X, e), where the sum over hidden variables gives P(X, e). "
          "What is the value of α?",
     "options": ["1/P(e)", "P(e)", "1/P(X)", "1/|domain(X)|"],
     "answer": [0],
     "solution": "By definition P(X | e) = P(X, e)/P(e), so α = 1/P(e). "
                 "In practice α is found by normalizing the vector P(X, e) to sum to 1, because ∑<sub>x</sub> P(x, e) = P(e). "
                 "The other options do not make the entries sum to 1 in general."},

    # =======================================================================
    # CONDITIONAL INDEPENDENCE
    # =======================================================================
    {"topic": "Conditional Independence", "type": "MCQ", "marks": 1,
     "q": "For random variables A, B, C with all conditioning events of positive probability, A ⊥ B | C holds if and only if",
     "options": ["P(A | B, C) = P(A | C)", "P(A, B) = P(A) P(B)", "P(A | C) = P(B | C)", "P(A, B, C) = P(A) P(B) P(C)"],
     "answer": [0],
     "solution": "Conditional independence of A and B given C means P(A, B | C) = P(A | C)P(B | C), equivalently P(A | B, C) = P(A | C). "
                 "(B) is marginal independence, which neither implies nor is implied by A ⊥ B | C. "
                 "(C) compares two different variables' distributions and is meaningless here. "
                 "(D) is mutual independence, a much stronger condition."},

    {"topic": "Conditional Independence", "type": "NAT", "marks": 2,
     "q": CC + "Compute P(a, b). (Round to 3 decimal places.)",
     "answer": {"lo": 0.263, "hi": 0.265},
     "solution": "A ⊥ B | C, so P(a, b) = ∑<sub>c</sub> P(c) P(a | c) P(b | c). "
                 "c: 0.4 × 0.9 × 0.7 = 0.252. ¬c: 0.6 × 0.2 × 0.1 = 0.012. Sum = 0.264. "
                 "Note P(a) = 0.36 + 0.12 = 0.48 and P(b) = 0.28 + 0.06 = 0.34, so P(a)P(b) = 0.1632 ≠ 0.264: A and B are marginally dependent."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 2,
     "q": CC + "Which of the following are true?",
     "options": ["P(a) = 0.48", "A ⊥ B (marginally)", "P(a | b, c) = 0.9", "P(a | b) ≈ 0.776"],
     "answer": [0, 2, 3],
     "solution": "P(a) = 0.4 × 0.9 + 0.6 × 0.2 = 0.36 + 0.12 = 0.48 (A true). "
                 "P(a, b) = 0.252 + 0.012 = 0.264 while P(a)P(b) = 0.48 × 0.34 = 0.1632, so A and B are dependent (B false). "
                 "In the fork C → A, C → B, A ⊥ B | C, so P(a | b, c) = P(a | c) = 0.9 (C true). "
                 "P(a | b) = 0.264/0.34 ≈ 0.7765 (D true): observing b raises belief in c and hence in a."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 2,
     "q": "X and Y are independent fair coin flips (Boolean) and Z = X XOR Y. Which statements are true?",
     "options": ["X ⊥ Z", "Y ⊥ Z", "X ⊥ Y | Z", "X ⊥ {Y, Z}"],
     "answer": [0, 1],
     "solution": "P(z) = 0.5 and P(x, z) = P(x, ¬y) = 0.25 = P(x)P(z); every entry factorizes, so X ⊥ Z (A true) and by symmetry Y ⊥ Z (B true). "
                 "Given Z, X determines Y: P(x | y, z) = 0 while P(x | z) = 0.5, so X and Y are dependent given Z (C false). "
                 "Since P(x | y, z) = 0 ≠ P(x) = 0.5, X is not independent of the pair {Y, Z} (D false). "
                 "Thus pairwise independence does not imply joint independence."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 1,
     "q": "Which of the following hold for <b>every</b> probability distribution over variables A, B, C, D?",
     "options": ["A ⊥ B | C implies B ⊥ A | C",
                 "A ⊥ {B, C} | D implies A ⊥ B | D",
                 "A ⊥ B implies A ⊥ B | C",
                 "A ⊥ B | C implies A ⊥ B"],
     "answer": [0, 1],
     "solution": "(A) Symmetry: P(A, B | C) = P(A | C)P(B | C) is symmetric in A and B. "
                 "(B) Decomposition: summing P(A, B, C | D) = P(A | D)P(B, C | D) over C gives P(A, B | D) = P(A | D)P(B | D). "
                 "(C) is false: in a v-structure A → C ← B, A ⊥ B but conditioning on C makes them dependent (explaining away). "
                 "(D) is false: in a fork A ← C → B, A ⊥ B | C but A and B are generally dependent."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 1,
     "q": "Which three-node structure is such that X and Z are d-separated by the empty set but <b>not</b> d-separated given Y?",
     "options": ["X → Y → Z", "X ← Y → Z", "X → Y ← Z", "X ← Y ← Z"],
     "answer": [2],
     "solution": "In a chain (A, D) or fork (B), the path X–Y–Z is active when Y is unobserved and blocked when Y is observed. "
                 "In the collider (v-structure) X → Y ← Z the path is blocked when neither Y nor a descendant is observed, so X and Z are d-separated by ∅, "
                 "and it becomes active when Y is observed. Hence only (C) has the stated behaviour."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 2,
     "q": G1 + "Which of the following pairs is d-separated by the given set?",
     "options": ["A and B given {E}", "A and F given {D}", "A and E given {D}", "E and F given ∅"],
     "answer": [2],
     "solution": "(C): every path from A to E goes A → C → D → E; D is a non-collider on it and is observed, so it is blocked: d-separated. "
                 "(A): the path A → C ← B has collider C whose descendant E is observed, so it is active. "
                 "(B): the path A → C ← B → F has collider C with observed descendant D, and non-collider B unobserved, so it is active. "
                 "(D): E ← D ← C ← B → F has no colliders and nothing observed, so it is active."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 2,
     "q": G1 + "Which of the following d-separation statements are true?",
     "options": ["A and B are d-separated given ∅", "A and F are d-separated given {B}",
                 "E and F are d-separated given {C}", "E and F are d-separated given ∅"],
     "answer": [0, 1, 2],
     "solution": "(A) The only path A → C ← B has collider C with no observed descendant: blocked, so true. "
                 "(B) The only path A → C ← B → F is blocked by the unobserved collider C (and also by the observed fork node B): true. "
                 "(C) The only path E ← D ← C ← B → F contains observed non-collider C: blocked, true. "
                 "(D) With nothing observed, E ← D ← C ← B → F has no colliders and is active, so false."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 2,
     "q": G3 + "Which of the following independences are guaranteed by d-separation (i.e., hold in every distribution that factorizes over this DAG)?",
     "options": ["Q ⊥ R | {P}", "Q ⊥ R | {P, T}", "U ⊥ P", "U ⊥ Q | {P, S}"],
     "answer": [0, 2],
     "solution": "Paths between Q and R: Q ← P → R (fork at P) and Q → S ← R (collider S). "
                 "(A) Given P, the fork is blocked and the collider S has no observed descendant: d-separated, true. "
                 "(B) T is a descendant of S, so observing T activates Q → S ← R: false. "
                 "(C) Paths from U to P all pass through R as a collider (U → R ← P, or U → R → S ← Q ← P with collider S); with nothing observed they are blocked: true. "
                 "(D) Given S, the path U → R → S ← Q has observed collider S and unobserved non-collider R, so it is active: false."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 2,
     "q": G3 + "Which pair of variables is <b>NOT</b> d-separated by the given set?",
     "options": ["T and P given {Q, R}", "U and Q given {P}", "U and P given {T}", "Q and R given {P}"],
     "answer": [2],
     "solution": "(C): T is a descendant of collider R on the path U → R ← P (R → S → T), so observing T activates it: not d-separated. "
                 "(A): every path from T to P goes through Q or R as non-colliders (T ← S ← Q ← P, T ← S ← R ← P), both observed: blocked. "
                 "(B): U → R ← P → Q is blocked at observed P and at unobserved collider R; U → R → S ← Q is blocked at unobserved collider S. "
                 "(D): fork P is observed and collider S is unobserved with no observed descendants: blocked."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 1,
     "q": "Burglary (B) and Earthquake (E) are independent causes of Alarm (A). Given that the alarm is ringing, learning that an earthquake occurred "
          "lowers the probability of a burglary. This phenomenon is called",
     "options": ["explaining away (intercausal reasoning)", "the local Markov property", "the naive Bayes assumption", "marginalization"],
     "answer": [0],
     "solution": "In the v-structure B → A ← E the causes are marginally independent but become dependent once the common effect is observed. "
                 "One cause 'explains away' the effect and reduces the posterior of the other cause. "
                 "The local Markov property concerns independence of a node from non-descendants given parents; naive Bayes is a class-feature model; "
                 "marginalization is summing out variables."},

    {"topic": "Conditional Independence", "type": "NAT", "marks": 2,
     "q": EA + "Compute P(a | c, b). (Round to 3 decimal places.)",
     "answer": {"lo": 0.116, "hi": 0.117},
     "solution": "Since A ⊥ B, P(A | c, b) = α P(A) P(c | A, b) (P(b) cancels). "
                 "For a: 0.1 × 0.95 = 0.095. For ¬a: 0.9 × 0.80 = 0.72. "
                 "P(a | c, b) = 0.095/(0.095 + 0.72) = 0.095/0.815 ≈ 0.1166 ≈ 0.117. "
                 "B already explains C, so A remains near its prior 0.1."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 2,
     "q": EA + "Which ordering of the three quantities P(a), P(a | c) and P(a | c, b) is correct?",
     "options": ["P(a) &lt; P(a | c, b) &lt; P(a | c)",
                 "P(a | c, b) &lt; P(a) &lt; P(a | c)",
                 "P(a) &lt; P(a | c) &lt; P(a | c, b)",
                 "P(a | c) &lt; P(a) &lt; P(a | c, b)"],
     "answer": [0],
     "solution": "P(c) = 0.1×0.2×0.95 + 0.1×0.8×0.90 + 0.9×0.2×0.80 + 0.9×0.8×0.05 = 0.019 + 0.072 + 0.144 + 0.036 = 0.271, and "
                 "P(a, c) = 0.019 + 0.072 = 0.091, so P(a | c) = 0.091/0.271 ≈ 0.336. "
                 "P(a | c, b) = 0.095/(0.095 + 0.72) ≈ 0.117. P(a) = 0.1. "
                 "Hence 0.1 &lt; 0.117 &lt; 0.336: observing c raises P(a); additionally observing b explains c away and lowers it, but not below the prior here."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 1,
     "q": "In a Bayesian network, a node is conditionally independent of all other nodes in the network given its Markov blanket. The Markov blanket consists of the node's",
     "options": ["parents, children, and children's other parents",
                 "parents and children only",
                 "parents and all ancestors",
                 "all non-descendants"],
     "answer": [0],
     "solution": "AIMA defines the Markov blanket as parents, children and children's parents. "
                 "Children's other parents are needed because of explaining away: given a child, a co-parent carries information about the node. "
                 "(B) omits the co-parents; (C) and (D) describe sets relevant to the local Markov property (independence from non-descendants given parents), not the blanket."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 1,
     "q": "Which of the following statements about d-separation in three-node structures are correct?",
     "options": ["In the chain X → Y → Z, X and Z are d-separated given Y",
                 "In the fork X ← Y → Z, X and Z are d-separated given Y",
                 "In the collider X → Y ← Z, X and Z are d-separated given Y",
                 "In the collider X → Y ← Z, X and Z are d-separated given ∅"],
     "answer": [0, 1, 3],
     "solution": "An observed non-collider blocks a path, so (A) and (B) are true. "
                 "A collider blocks the path when neither it nor any descendant is observed, so (D) is true. "
                 "Observing the collider activates the path, so (C) is false."},

    {"topic": "Conditional Independence", "type": "MCQ", "marks": 1,
     "q": "Boolean variables A, B, C satisfy A ⊥ B | C, and no other independence is known. "
          "What is the minimum number of independent parameters needed to specify P(A, B, C)?",
     "options": ["5", "7", "6", "4"],
     "answer": [0],
     "solution": "Write P(A, B, C) = P(C) P(A | C) P(B | C), using A ⊥ B | C. "
                 "P(C) needs 1 number, P(A | C) needs 2 (one per value of C), P(B | C) needs 2. Total = 5. "
                 "7 = 2<sup>3</sup> − 1 is the unconstrained full joint; 6 and 4 do not correspond to this factorization."},

    {"topic": "Conditional Independence", "type": "MSQ", "marks": 2,
     "q": "A Bayesian network over A, B, C, D encodes the factorization P(A) P(B | A) P(C | A) P(D | B, C). "
          "Which independences are guaranteed to hold in every distribution with this factorization?",
     "options": ["B ⊥ C | {A}", "B ⊥ C | {A, D}", "A ⊥ D | {B, C}", "A ⊥ D"],
     "answer": [0, 2],
     "solution": "The DAG is A → B, A → C, B → D, C → D. "
                 "(A) B–C paths: B ← A → C (fork, A observed: blocked) and B → D ← C (collider D unobserved, no descendants: blocked): d-separated, true. "
                 "(B) Observing D activates the collider path B → D ← C: false. "
                 "(C) Both A–D paths A → B → D and A → C → D pass through observed non-colliders B and C: d-separated, true. "
                 "(D) With nothing observed, A → B → D is active: false."},

    # =======================================================================
    # BAYESIAN NETWORKS
    # =======================================================================
    {"topic": "Bayesian Networks", "type": "MCQ", "marks": 1,
     "q": "A naive Bayes model with class variable C and features F<sub>1</sub>, …, F<sub>n</sub>, viewed as a Bayesian network, has which structure and assumption?",
     "options": ["Edges C → F<sub>i</sub> for each i; features are conditionally independent given C",
                 "Edges F<sub>i</sub> → C for each i; features are marginally independent",
                 "A chain C → F<sub>1</sub> → F<sub>2</sub> → … → F<sub>n</sub>",
                 "Edges C → F<sub>i</sub> for each i; features are marginally independent"],
     "answer": [0],
     "solution": "Naive Bayes uses P(C, F<sub>1</sub>, …, F<sub>n</sub>) = P(C) ∏ P(F<sub>i</sub> | C), i.e. the class is the single parent of every feature. "
                 "The DAG implies F<sub>i</sub> ⊥ F<sub>j</sub> | C. "
                 "(D) is wrong because the features are generally dependent marginally (common cause C is unobserved). "
                 "(B) reverses the edges (that would make features marginally independent but dependent given C); (C) is a different model."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 1,
     "q": "A naive Bayes classifier has a class variable with 3 values and 10 Boolean features. "
          "How many independent parameters does the Bayesian network have?",
     "answer": {"lo": 32, "hi": 32},
     "solution": "P(C) needs 3 − 1 = 2 numbers. Each feature's CPT P(F<sub>i</sub> | C) has 3 rows with 1 free number each, i.e. 3 numbers. "
                 "Total = 2 + 10 × 3 = 32 (versus 3 × 2<sup>10</sup> − 1 = 3071 for the full joint)."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 2,
     "q": "A naive Bayes spam filter has P(spam) = 0.3 and three Boolean features with "
          "P(f<sub>1</sub> | spam) = 0.8, P(f<sub>1</sub> | ham) = 0.1; P(f<sub>2</sub> | spam) = 0.6, P(f<sub>2</sub> | ham) = 0.3; "
          "P(f<sub>3</sub> | spam) = 0.2, P(f<sub>3</sub> | ham) = 0.5. "
          "An email has f<sub>1</sub> = true, f<sub>2</sub> = false, f<sub>3</sub> = true. Compute P(spam | f<sub>1</sub>, ¬f<sub>2</sub>, f<sub>3</sub>). (Round to 3 decimal places.)",
     "answer": {"lo": 0.439, "hi": 0.440},
     "solution": "Spam: 0.3 × 0.8 × (1 − 0.6) × 0.2 = 0.3 × 0.8 × 0.4 × 0.2 = 0.0192. "
                 "Ham: 0.7 × 0.1 × (1 − 0.3) × 0.5 = 0.7 × 0.1 × 0.7 × 0.5 = 0.0245. "
                 "Normalize: 0.0192/(0.0192 + 0.0245) = 0.0192/0.0437 ≈ 0.4394 ≈ 0.439. "
                 "Note P(¬f<sub>2</sub> | class) = 1 − P(f<sub>2</sub> | class) must be used for the false feature."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 1,
     "q": "A Bayesian network over Boolean variables has edges A → C, B → C, C → D, C → E. "
          "How many independent parameters do its CPTs contain?",
     "answer": {"lo": 10, "hi": 10},
     "solution": "A Boolean node with k Boolean parents needs 2<sup>k</sup> numbers. "
                 "A: 1, B: 1, C (2 parents): 4, D (1 parent): 2, E (1 parent): 2. Total = 10, compared with 2<sup>5</sup> − 1 = 31 for the full joint."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 2,
     "q": "A Bayesian network has: A with 3 values (no parents); B Boolean (no parents); C with 4 values and parents A, B; "
          "D Boolean with parent C; E with 3 values and parents C, D. How many independent parameters do the CPTs require?",
     "answer": {"lo": 41, "hi": 41},
     "solution": "Each CPT needs (number of parent configurations) × (arity − 1). "
                 "A: 1 × 2 = 2. B: 1 × 1 = 1. C: (3 × 2) × 3 = 18. D: 4 × 1 = 4. E: (4 × 2) × 2 = 16. "
                 "Total = 2 + 1 + 18 + 4 + 16 = 41, versus 3 × 2 × 4 × 2 × 3 − 1 = 143 for the full joint."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 1,
     "q": ALARM + "Compute the joint probability P(j, m, a, ¬b, ¬e). (Round to 4 decimal places.)",
     "answer": {"lo": 0.0054, "hi": 0.0055},
     "solution": "By the BN factorization, P(j, m, a, ¬b, ¬e) = P(j | a) P(m | a) P(a | ¬b, ¬e) P(¬b) P(¬e). "
                 "= 0.8 × 0.7 × 0.01 × 0.98 × 0.99 = 0.56 × 0.01 × 0.9702 = 0.005433 ≈ 0.0054."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 2,
     "q": ALARM + "Compute P(b | j, m). (Round to 3 decimal places.)",
     "answer": {"lo": 0.555, "hi": 0.557},
     "solution": "P(B | j, m) = α P(B) ∑<sub>e</sub> P(e) ∑<sub>a</sub> P(a | B, e) P(j | a) P(m | a). "
                 "Let g(a) = P(j | a)P(m | a): g(a) = 0.56, g(¬a) = 0.001. "
                 "For b: e: 0.95×0.56 + 0.05×0.001 = 0.53205; ¬e: 0.90×0.56 + 0.10×0.001 = 0.5041; weighted: 0.01×0.53205 + 0.99×0.5041 = 0.504381; times P(b) = 0.02 → 0.0100876. "
                 "For ¬b: e: 0.30×0.56 + 0.70×0.001 = 0.1687; ¬e: 0.01×0.56 + 0.99×0.001 = 0.006589; weighted: 0.01×0.1687 + 0.99×0.006589 = 0.0082101; times 0.98 → 0.0080459. "
                 "P(b | j, m) = 0.0100876/(0.0100876 + 0.0080459) ≈ 0.556."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 2,
     "q": ALARM + "Which of the following are correct (values rounded)?",
     "options": ["P(a) ≈ 0.0307", "P(b | a) ≈ 0.588", "P(b | a, e) &gt; P(b | a)", "P(j | b) ≈ 0.725"],
     "answer": [0, 1, 3],
     "solution": "P(a) = 0.02×0.01×0.95 + 0.02×0.99×0.90 + 0.98×0.01×0.30 + 0.98×0.99×0.01 = 0.00019 + 0.01782 + 0.00294 + 0.009702 = 0.030652 (A true). "
                 "P(b, a) = 0.00019 + 0.01782 = 0.01801, so P(b | a) = 0.01801/0.030652 ≈ 0.588 (B true). "
                 "P(b | a, e) = 0.019/0.313 ≈ 0.061 &lt; 0.588 (explaining away), so (C) is false. "
                 "P(a | b) = 0.01×0.95 + 0.99×0.90 = 0.9005, so P(j | b) = 0.9005×0.8 + 0.0995×0.05 = 0.7204 + 0.004975 ≈ 0.725 (D true)."},

    {"topic": "Bayesian Networks", "type": "MCQ", "marks": 1,
     "q": "Which statement is the <i>local Markov property</i> (local semantics) of a Bayesian network?",
     "options": ["Each node is conditionally independent of its non-descendants given its parents",
                 "Each node is conditionally independent of its descendants given its parents",
                 "Each node is marginally independent of all nodes that are not its parents",
                 "Each node is conditionally independent of its parents given its children"],
     "answer": [0],
     "solution": "AIMA: a node is conditionally independent of its non-descendants given its parents; this is equivalent to the global factorization semantics. "
                 "(B) is false because descendants (e.g. children) carry information about the node even given the parents. "
                 "(C) ignores dependence through common ancestors, and (D) has no basis."},

    {"topic": "Bayesian Networks", "type": "MCQ", "marks": 1,
     "q": "A Bayesian network has edges A → B, A → C, B → D, C → D. Which is the joint distribution it represents?",
     "options": ["P(A) P(B | A) P(C | A) P(D | B, C)",
                 "P(A) P(B | A) P(C | B) P(D | C)",
                 "P(A) P(B) P(C) P(D | B, C)",
                 "P(D) P(B | D) P(C | D) P(A | B, C)"],
     "answer": [0],
     "solution": "A BN represents ∏<sub>i</sub> P(X<sub>i</sub> | Parents(X<sub>i</sub>)). Parents: A: none; B: A; C: A; D: B, C. "
                 "This gives (A). (B) corresponds to a chain A → B → C → D; (C) drops edges from A; (D) reverses every edge."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 2,
     "q": G2 + "Which of the following nodes belong to the Markov blanket of C?",
     "options": ["B", "F", "H", "A"],
     "answer": [0, 2, 3],
     "solution": "Parents of C: {A}. Children of C: {D, G}. Other parents of the children: D has parents B, C, E and G has parents C, H, giving {B, E, H}. "
                 "Markov blanket of C = {A, B, D, E, G, H}. "
                 "So A (parent), B (co-parent via D) and H (co-parent via G) belong to it. "
                 "F is a child of D, i.e. a grandchild of C, and is not in the blanket: given D, F is independent of C."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 2,
     "q": ALARM + "Suppose a new network is built for the same distribution by adding nodes in the order M, J, A, B, E, "
          "choosing for each node a minimal set of parents among the previously added nodes such that the node is conditionally "
          "independent of its other predecessors given its parents. How many independent CPT parameters does this new network have "
          "(all variables Boolean)? Assume no independences beyond those implied by the original structure.",
     "answer": {"lo": 13, "hi": 13},
     "solution": "M: no predecessors → 1 parameter. J: not independent of M (both depend on A) → parent M → 2. "
                 "A: depends on both M and J and neither screens the other → parents {M, J} → 4. "
                 "B: given A, B is independent of M and J → parent {A} → 2. "
                 "E: given A alone, E still depends on B (explaining away), but given {A, B} it is independent of M, J → parents {A, B} → 4. "
                 "Total = 1 + 2 + 4 + 2 + 4 = 13, versus 10 for the causal ordering B, E, A, J, M."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 2,
     "q": "Which of the following statements about I-maps of a distribution P are correct? (G is an I-map of P if every independence implied by G by d-separation holds in P.)",
     "options": ["A complete (fully connected) DAG over the variables is an I-map of every distribution",
                 "Adding nodes in a causal order (causes before effects) usually yields a sparser minimal I-map",
                 "Adding an arc (without creating a cycle) to an I-map of P can make it fail to be an I-map of P",
                 "The minimal I-map of P is the same DAG for every variable ordering"],
     "answer": [0, 1],
     "solution": "(A) A complete DAG implies no independences, so it is trivially an I-map. "
                 "(B) AIMA shows causal orderings (e.g. B, E, A, J, M) give compact networks while diagnostic orderings (M, J, E, B, A) can be fully connected. "
                 "(C) is false: adding an arc can only remove d-separation statements, so the set of implied independences shrinks and remains true in P. "
                 "(D) is false: for the alarm example, order B, E, A, J, M gives 10 parameters, order M, J, A, B, E gives 13, and M, J, E, B, A gives 31."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 1,
     "q": "Which of the following are correct about Bayesian networks with Boolean variables?",
     "options": ["The graph must be a directed acyclic graph",
                 "The CPT of a node with k Boolean parents has 2<sup>k</sup> independent numbers",
                 "Each row of a CPT (one parent configuration) sums to 1 over the node's values",
                 "If there is no arc between X and Y, then X ⊥ Y marginally"],
     "answer": [0, 1, 2],
     "solution": "(A) BNs are DAGs by definition. (B) There are 2<sup>k</sup> rows, each needing one number P(X = true | row). "
                 "(C) Each row is a conditional distribution, so it sums to 1. "
                 "(D) is false: in A → B → C there is no arc between A and C, but they are dependent through B."},

    {"topic": "Bayesian Networks", "type": "NAT", "marks": 2,
     "q": "Fever has three possible causes Cold, Flu and Malaria, modeled with a noisy-OR CPT with no leak. "
          "The inhibition probabilities are q<sub>cold</sub> = 0.6, q<sub>flu</sub> = 0.2, q<sub>malaria</sub> = 0.1 "
          "(q<sub>i</sub> = probability that cause i, when present alone, fails to produce fever). "
          "Compute P(fever | cold, flu, ¬malaria). (Round to 2 decimal places.)",
     "answer": {"lo": 0.875, "hi": 0.885},
     "solution": "In noisy-OR, P(¬fever | causes) = product of q<sub>i</sub> over the causes that are present. "
                 "Present causes: cold and flu, so P(¬fever) = 0.6 × 0.2 = 0.12. "
                 "P(fever | cold, flu, ¬malaria) = 1 − 0.12 = 0.88. Malaria is absent and contributes no factor."},

    {"topic": "Bayesian Networks", "type": "MCQ", "marks": 1,
     "q": "A Boolean node has k Boolean parents. Its CPT is specified using a noisy-OR model (no leak). How many parameters are needed, versus a general CPT?",
     "options": ["k for noisy-OR versus 2<sup>k</sup> for a general CPT",
                 "2<sup>k</sup> for both",
                 "k<sup>2</sup> for noisy-OR versus 2<sup>k</sup> for a general CPT",
                 "2k for noisy-OR versus k<sup>2</sup> for a general CPT"],
     "answer": [0],
     "solution": "Noisy-OR needs one inhibition probability per parent, i.e. k numbers, and the full table is derived as P(¬x | parents) = ∏ q<sub>j</sub> over true parents. "
                 "A general Boolean CPT has one free number for each of the 2<sup>k</sup> parent configurations. "
                 "This linear-vs-exponential saving is why canonical distributions are used."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 2,
     "q": "A Bayesian network is the chain A → B → C over Boolean variables with P(a) = 0.6, P(b | a) = 0.7, P(b | ¬a) = 0.2, "
          "P(c | b) = 0.9, P(c | ¬b) = 0.3. Which of the following are correct?",
     "options": ["P(b) = 0.5", "P(c) = 0.6", "P(a | c) = 0.72", "P(a | c) = P(a), since A and C are not adjacent"],
     "answer": [0, 1, 2],
     "solution": "P(b) = 0.6×0.7 + 0.4×0.2 = 0.42 + 0.08 = 0.5 (A true). P(c) = 0.5×0.9 + 0.5×0.3 = 0.45 + 0.15 = 0.6 (B true). "
                 "P(a, c) = 0.6 × (0.7×0.9 + 0.3×0.3) = 0.6 × 0.72 = 0.432, so P(a | c) = 0.432/0.6 = 0.72 (C true). "
                 "(D) is false: A and C are connected by the active path A → B → C (B unobserved), so observing c raises P(a) from 0.6 to 0.72."},

    {"topic": "Bayesian Networks", "type": "MCQ", "marks": 2,
     "q": SPR + "What is P(r | w) (rounded to 3 decimal places)?",
     "options": ["0.708", "0.647", "0.430", "0.800"],
     "answer": [0],
     "solution": "Compute P(r, w) = ∑<sub>c,s</sub> P(c)P(s | c)P(r | c)P(w | s, r). With c: P(r | c) = 0.8 and P(w | r) averaged over S: 0.1×0.99 + 0.9×0.90 = 0.909 → 0.5×0.8×0.909 = 0.3636. "
                 "With ¬c: P(r | ¬c) = 0.2 and 0.5×0.99 + 0.5×0.90 = 0.945 → 0.5×0.2×0.945 = 0.0945. So P(r, w) = 0.4581. "
                 "P(¬r, w): c: 0.5×0.2×(0.1×0.9 + 0.9×0) = 0.009; ¬c: 0.5×0.8×(0.5×0.9) = 0.18; total 0.189. P(w) = 0.6471. "
                 "P(r | w) = 0.4581/0.6471 ≈ 0.708. 0.647 is P(w), 0.430 is P(s | w), 0.800 is P(r | c)."},

    {"topic": "Bayesian Networks", "type": "MSQ", "marks": 2,
     "q": SPR + "Which of the following are correct (values rounded to 3 decimal places)?",
     "options": ["P(s | w, r) ≈ 0.194", "P(s | w) ≈ 0.430", "P(s | w, r) &gt; P(s | w)", "P(w) ≈ 0.647"],
     "answer": [0, 1, 3],
     "solution": "P(s, w) = c: 0.5×0.1×(0.8×0.99 + 0.2×0.90) = 0.0486; ¬c: 0.5×0.5×(0.2×0.99 + 0.8×0.90) = 0.2295; total 0.2781. "
                 "P(¬s, w) = c: 0.5×0.9×0.8×0.90 = 0.324; ¬c: 0.5×0.5×0.2×0.90 = 0.045; total 0.369. P(w) = 0.6471 (D true) and P(s | w) = 0.2781/0.6471 ≈ 0.430 (B true). "
                 "P(s, w, r) = (0.5×0.1×0.8 + 0.5×0.5×0.2) × 0.99 = 0.0891; P(¬s, w, r) = (0.36 + 0.05) × 0.90 = 0.369; P(s | w, r) = 0.0891/0.4581 ≈ 0.194 (A true). "
                 "Rain explains away the wet grass, so P(s | w, r) &lt; P(s | w): (C) is false."},

    # =======================================================================
    # VARIABLE ELIMINATION / EXACT INFERENCE
    # =======================================================================
    {"topic": "Variable Elimination", "type": "MCQ", "marks": 1,
     "q": "In variable elimination, f<sub>1</sub>(A, B) and f<sub>2</sub>(B, C) are factors over Boolean variables. Their pointwise product f<sub>1</sub> × f<sub>2</sub> is",
     "options": ["a factor over {A, B, C} with 8 entries",
                 "a factor over {A, C} with 4 entries",
                 "a factor over {B} with 2 entries",
                 "a factor over {A, B, B, C} with 16 entries"],
     "answer": [0],
     "solution": "The pointwise product is defined on the union of the variables: f(a, b, c) = f<sub>1</sub>(a, b) × f<sub>2</sub>(b, c). "
                 "The union {A, B, C} has 2<sup>3</sup> = 8 entries. "
                 "{A, C} would result only after summing out B; shared variable B appears once, not twice."},

    {"topic": "Variable Elimination", "type": "NAT", "marks": 1,
     "q": "Factors over Boolean variables: f(A, B) with f(a, b) = 0.4, f(a, ¬b) = 0.6, f(¬a, b) = 0.8, f(¬a, ¬b) = 0.2; "
          "g(B, C) with g(b, c) = 0.3, g(b, ¬c) = 0.7, g(¬b, c) = 0.5, g(¬b, ¬c) = 0.5. "
          "Let h(A, C) = ∑<sub>B</sub> f(A, B) × g(B, C). Compute h(a, c). (Round to 2 decimal places.)",
     "answer": {"lo": 0.415, "hi": 0.425},
     "solution": "h(a, c) = f(a, b) g(b, c) + f(a, ¬b) g(¬b, c) = 0.4 × 0.3 + 0.6 × 0.5 = 0.12 + 0.30 = 0.42. "
                 "First the pointwise product over {A, B, C} is formed, then B is summed out, leaving a factor over {A, C}."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 2,
     "q": ALARM + "For the query P(J | b) (J given Burglary = true), which variables are irrelevant to the query and can be removed before running variable elimination?",
     "options": ["{M}", "{E, M}", "{E}", "No variable is irrelevant"],
     "answer": [0],
     "solution": "AIMA: every variable that is not an ancestor of a query variable or an evidence variable is irrelevant. "
                 "Ancestors of J and B: {A, B, E}. M is neither, so it is irrelevant: ∑<sub>m</sub> P(m | a) = 1. "
                 "E is an ancestor of J (E → A → J), and P(a | b) = ∑<sub>e</sub> P(e) P(a | b, e) genuinely depends on E's CPT, so E cannot be dropped."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 1,
     "q": "For a polytree (singly connected) Bayesian network, the time and space complexity of exact inference by variable elimination is",
     "options": ["linear in the size of the network (total CPT entries)",
                 "exponential in the number of variables in the worst case",
                 "quadratic in the number of variables, independent of CPT sizes",
                 "NP-hard"],
     "answer": [0],
     "solution": "AIMA: in polytrees there is at most one undirected path between any two nodes, and VE (with a suitable ordering) runs in time and space linear in the size of the network, measured by CPT entries. "
                 "Exponential/NP-hard behaviour arises for multiply connected networks. "
                 "Quadratic in variables ignores that CPT sizes grow with the number of parents."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 1,
     "q": "What is the computational complexity of exact inference in general (multiply connected) Bayesian networks?",
     "options": ["NP-hard (in fact #P-hard)", "Polynomial time", "Linear time", "Undecidable"],
     "answer": [0],
     "solution": "AIMA shows that exact inference includes propositional satisfiability as a special case (3-SAT can be encoded), so it is NP-hard; "
                 "computing the probability is #P-hard. It is linear only for polytrees and is certainly decidable (enumeration always terminates)."},

    {"topic": "Variable Elimination", "type": "NAT", "marks": 2,
     "q": "A Bayesian network over Boolean variables has edges H → X<sub>1</sub>, H → X<sub>2</sub>, H → X<sub>3</sub>, H → X<sub>4</sub>. "
          "To compute P(X<sub>1</sub>) by variable elimination, H is eliminated <b>first</b> (then X<sub>2</sub>, X<sub>3</sub>, X<sub>4</sub>). "
          "How many entries does the new factor produced by summing out H contain?",
     "answer": {"lo": 16, "hi": 16},
     "solution": "Eliminating H multiplies all factors that mention H: P(H), P(X<sub>1</sub> | H), …, P(X<sub>4</sub> | H). "
                 "Summing out H leaves a factor over {X<sub>1</sub>, X<sub>2</sub>, X<sub>3</sub>, X<sub>4</sub>}, with 2<sup>4</sup> = 16 entries. "
                 "By contrast, eliminating X<sub>2</sub>, X<sub>3</sub>, X<sub>4</sub> first gives trivial factors over H (each ∑<sub>x</sub> P(x | H) = 1) and the largest new factor has just 1 variable."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 2,
     "q": "A Bayesian network over Boolean variables has edges A → B, A → C, B → D, C → D, D → E. P(E) is computed by variable elimination with no evidence. "
          "For which elimination ordering does <b>every</b> new factor created by summing out a variable contain at most two variables?",
     "options": ["A, B, C, D", "D, C, B, A", "B, C, A, D", "C, B, A, D"],
     "answer": [0],
     "solution": "Order A, B, C, D: eliminating A combines P(A), P(B | A), P(C | A) → f(B, C); B combines f(B, C), P(D | B, C) → f(C, D); C → f(D); D with P(E | D) → f(E). Max 2 variables. "
                 "D first: P(D | B, C) and P(E | D) → f(B, C, E) (3 variables). "
                 "B first: P(B | A), P(D | B, C) → f(A, C, D) (3 variables); C first similarly gives f(A, B, D). "
                 "So only (A) keeps all factors at two variables or fewer."},

    {"topic": "Variable Elimination", "type": "MSQ", "marks": 1,
     "q": "Which of the following statements about factors in variable elimination are correct (all variables Boolean)?",
     "options": ["Summing out one variable from a factor over k variables yields a factor with 2<sup>k−1</sup> entries",
                 "The pointwise product of factors is commutative",
                 "The entries of every intermediate factor must sum to 1",
                 "Evidence variables are fixed to their observed values, so they do not appear as dimensions of factors"],
     "answer": [0, 1, 3],
     "solution": "(A) Summing out removes one Boolean dimension, from 2<sup>k</sup> to 2<sup>k−1</sup> entries. "
                 "(B) Pointwise product is entry-wise multiplication of real numbers, hence commutative (and associative). "
                 "(D) AIMA instantiates evidence, e.g. P(j | A) becomes a factor over A alone. "
                 "(C) is false: factors are generally unnormalized (e.g. P(j | A) as a function of A, or intermediate sums), normalization happens only at the end."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 2,
     "q": "For a Bayesian network with n Boolean variables, the depth-first ENUMERATION-ASK algorithm (inference by enumeration) has worst-case",
     "options": ["O(2<sup>n</sup>) time and O(n) space",
                 "O(n) time and O(2<sup>n</sup>) space",
                 "O(2<sup>n</sup>) time and O(2<sup>n</sup>) space",
                 "O(n<sup>2</sup>) time and O(n) space"],
     "answer": [0],
     "solution": "Enumeration evaluates a depth-first expression tree that branches over every hidden variable, giving O(2<sup>n</sup>) time. "
                 "Being depth-first it stores only the current path, so space is O(n). "
                 "It never builds the full joint table, so it does not need O(2<sup>n</sup>) space; polynomial time is impossible in general since inference is NP-hard. "
                 "Variable elimination improves time by caching repeated subexpressions as factors."},

    {"topic": "Variable Elimination", "type": "MSQ", "marks": 2,
     "q": "A Bayesian network has edges A → B and A → C over Boolean variables with P(a) = 0.3, P(b | a) = 0.8, P(b | ¬a) = 0.4, "
          "P(c | a) = 0.5, P(c | ¬a) = 0.1. P(A | b, c) is computed by variable elimination, multiplying the evidence-instantiated factors "
          "f<sub>1</sub>(A) = P(A), f<sub>2</sub>(A) = P(b | A), f<sub>3</sub>(A) = P(c | A) into an unnormalized factor f(A). Which are correct?",
     "options": ["f(a) = 0.12", "f(¬a) = 0.028", "P(a | b, c) ≈ 0.811", "P(b, c) = 0.12"],
     "answer": [0, 1, 2],
     "solution": "f(a) = 0.3 × 0.8 × 0.5 = 0.12 (A true). f(¬a) = 0.7 × 0.4 × 0.1 = 0.028 (B true). "
                 "Normalizing, P(a | b, c) = 0.12/(0.12 + 0.028) = 0.12/0.148 ≈ 0.811 (C true). "
                 "The normalizer is P(b, c) = f(a) + f(¬a) = 0.148, not 0.12 (which is P(a, b, c)), so (D) is false."},

    {"topic": "Variable Elimination", "type": "NAT", "marks": 2,
     "q": "A Bayesian network is the chain A → B → C → D over Boolean variables with P(a) = 0.2; P(b | a) = 0.9, P(b | ¬a) = 0.3; "
          "P(c | b) = 0.6, P(c | ¬b) = 0.1; P(d | c) = 0.7, P(d | ¬c) = 0.2. "
          "Compute P(d) by eliminating A, B, C in that order. (Round to 3 decimal places.)",
     "answer": {"lo": 0.354, "hi": 0.356},
     "solution": "Eliminate A: f<sub>A</sub>(b) = 0.2×0.9 + 0.8×0.3 = 0.18 + 0.24 = 0.42, f<sub>A</sub>(¬b) = 0.58. "
                 "Eliminate B: f<sub>B</sub>(c) = 0.42×0.6 + 0.58×0.1 = 0.252 + 0.058 = 0.31, f<sub>B</sub>(¬c) = 0.69. "
                 "Eliminate C: P(d) = 0.31×0.7 + 0.69×0.2 = 0.217 + 0.138 = 0.355. "
                 "Each step creates a factor over a single variable, so cost is linear in the chain length."},

    {"topic": "Variable Elimination", "type": "MSQ", "marks": 2,
     "q": "Which statements about variable elimination (VE) are correct?",
     "options": ["Every elimination ordering yields the same final answer",
                 "Finding an optimal elimination ordering is NP-hard in general",
                 "VE runs in time polynomial in the number of variables for every network and ordering",
                 "VE avoids the repeated computation of identical subexpressions that occurs in enumeration"],
     "answer": [0, 1, 3],
     "solution": "(A) Sums of products can be reordered (distributive law), so every ordering computes the same exact result; only cost differs. "
                 "(B) AIMA notes finding the optimal ordering is intractable (NP-hard), so heuristics such as min-fill or min-degree are used. "
                 "(D) VE stores intermediate results as factors so each is computed once. "
                 "(C) is false: the cost is exponential in the size of the largest factor, which can be large for multiply connected networks or bad orderings."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 1,
     "q": "In VE for a query with evidence J = true, the CPT P(J | A) (A and J Boolean) is converted into which factor?",
     "options": ["A factor over A with 2 entries: P(j | a), P(j | ¬a)",
                 "A factor over {A, J} with 4 entries",
                 "A factor over J with 2 entries",
                 "A scalar equal to P(j)"],
     "answer": [0],
     "solution": "Evidence variables are instantiated, so only the column J = true is kept, giving f(A) = ⟨P(j | a), P(j | ¬a)⟩. "
                 "J no longer appears as a dimension. P(j) would require summing over A weighted by P(A), which VE does only later and only if needed."},

    {"topic": "Variable Elimination", "type": "NAT", "marks": 2,
     "q": ALARM + "In computing P(B | j, m) by variable elimination, A is summed out first, producing a factor f(B, E) = ∑<sub>a</sub> P(a | B, E) P(j | a) P(m | a). "
          "Compute f(b, e). (Round to 3 decimal places.)",
     "answer": {"lo": 0.531, "hi": 0.533},
     "solution": "f(b, e) = P(a | b, e) P(j | a) P(m | a) + P(¬a | b, e) P(j | ¬a) P(m | ¬a). "
                 "= 0.95 × 0.8 × 0.7 + 0.05 × 0.05 × 0.02 = 0.532 + 0.00005 = 0.53205 ≈ 0.532. "
                 "This is not a probability distribution over B, E; it is an intermediate factor."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 2,
     "q": ALARM + "For P(B | j, m), the elimination order A then E is used. After summing out A, which factors remain to be multiplied when E is eliminated?",
     "options": ["P(E) and f<sub>A</sub>(B, E)",
                 "P(E), P(B) and f<sub>A</sub>(B, E)",
                 "P(E) and f<sub>A</sub>(B, E, J, M)",
                 "P(E), P(A | B, E) and f<sub>A</sub>(B)"],
     "answer": [0],
     "solution": "Initially the factors are P(B), P(E), P(A | B, E), f(A) = P(j | A), g(A) = P(m | A). "
                 "Summing out A multiplies the three factors containing A and yields f<sub>A</sub>(B, E). "
                 "Eliminating E then multiplies only the factors mentioning E: P(E) and f<sub>A</sub>(B, E), giving f<sub>E</sub>(B). "
                 "P(B) does not mention E so it is left aside until the end; J and M are evidence, not dimensions; P(A | B, E) was already consumed."},

    {"topic": "Variable Elimination", "type": "MCQ", "marks": 1,
     "q": "A Bayesian network is called a polytree (singly connected) if",
     "options": ["there is at most one undirected path between any two nodes",
                 "every node has at most one parent",
                 "there is at most one directed path between any two nodes",
                 "it has exactly one root node"],
     "answer": [0],
     "solution": "AIMA defines singly connected networks (polytrees) as those with at most one undirected path between any pair of nodes. "
                 "Nodes may have several parents (e.g. the alarm network is a polytree although A has two parents). "
                 "Requiring at most one directed path is weaker: A → B, A → C, B → C has two directed paths A to C, but A → B, C → B, A → D, C → D has "
                 "unique directed paths yet the undirected cycle A–B–C–D–A. A polytree may also have several roots."},

    {"topic": "Variable Elimination", "type": "MSQ", "marks": 2,
     "q": "Which of the following Bayesian networks (edges listed) are polytrees?",
     "options": ["A → C, B → C, C → D, C → E",
                 "A → B, A → C, B → D, C → D",
                 "A → B, B → C, D → C, D → E",
                 "A → B, A → C, B → C"],
     "answer": [0, 2],
     "solution": "A polytree has no undirected cycle. "
                 "(A) Underlying undirected graph A–C, B–C, C–D, C–E is a tree: polytree. "
                 "(B) A–B–D–C–A is an undirected cycle: multiply connected. "
                 "(C) A–B–C–D–E is a simple path, no cycle: polytree (C has two parents, which is allowed). "
                 "(D) A–B–C–A forms a triangle: not a polytree."},

    # =======================================================================
    # SAMPLING / APPROXIMATE INFERENCE
    # =======================================================================
    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": SPR + "Prior (direct) sampling visits variables in the order C, S, R, W and sets a variable to true if and only if the next uniform random number u satisfies "
          "u &lt; P(variable = true | sampled parents). The random numbers used are 0.42, 0.07, 0.85, 0.30 (in this order). What sample is generated?",
     "options": ["(c, s, ¬r, w)", "(c, ¬s, r, w)", "(c, s, r, w)", "(¬c, s, ¬r, ¬w)"],
     "answer": [0],
     "solution": "C: 0.42 &lt; P(c) = 0.5 → c. S: P(s | c) = 0.1, 0.07 &lt; 0.1 → s. "
                 "R: P(r | c) = 0.8, 0.85 ≥ 0.8 → ¬r. W: P(w | s, ¬r) = 0.90, 0.30 &lt; 0.90 → w. "
                 "Sample = (c, s, ¬r, w). (B) mis-samples S and R; (C) mis-samples R; (D) mis-samples C."},

    {"topic": "Sampling", "type": "NAT", "marks": 1,
     "q": SPR + "With prior sampling, what is the probability that a single generated sample is exactly (c, ¬s, r, w)? (Round to 3 decimal places.)",
     "answer": {"lo": 0.323, "hi": 0.325},
     "solution": "Prior sampling generates each event with probability equal to its joint probability: S<sub>PS</sub>(x) = ∏ P(x<sub>i</sub> | parents). "
                 "= P(c) P(¬s | c) P(r | c) P(w | ¬s, r) = 0.5 × 0.9 × 0.8 × 0.9 = 0.324."},

    {"topic": "Sampling", "type": "NAT", "marks": 1,
     "q": "To estimate P(Rain | sprinkler) by rejection sampling, 500 samples are generated by prior sampling. "
          "140 of them have Sprinkler = true, and of these 35 have Rain = true. "
          "What is the rejection-sampling estimate of P(rain | sprinkler)? (Round to 2 decimal places.)",
     "answer": {"lo": 0.245, "hi": 0.255},
     "solution": "Rejection sampling discards the 500 − 140 = 360 samples inconsistent with the evidence. "
                 "Among the 140 retained samples, the fraction with Rain = true is 35/140 = 0.25. "
                 "Dividing by 500 would be wrong because it estimates P(rain, sprinkler), not the conditional."},

    {"topic": "Sampling", "type": "NAT", "marks": 2,
     "q": SPR + "Rejection sampling is used with evidence S = true, W = true. What fraction of the prior samples is expected to be rejected? (Round to 3 decimal places.)",
     "answer": {"lo": 0.721, "hi": 0.723},
     "solution": "A sample is kept with probability P(s, w). "
                 "P(s, w) = ∑<sub>c,r</sub> P(c)P(s | c)P(r | c)P(w | s, r). c: 0.5×0.1×(0.8×0.99 + 0.2×0.90) = 0.05×0.972 = 0.0486. "
                 "¬c: 0.5×0.5×(0.2×0.99 + 0.8×0.90) = 0.25×0.918 = 0.2295. P(s, w) = 0.2781. "
                 "Expected rejected fraction = 1 − 0.2781 = 0.7219 ≈ 0.722."},

    {"topic": "Sampling", "type": "NAT", "marks": 1,
     "q": SPR + "Likelihood weighting is used with evidence S = true, W = true. A sample is generated with C = false and R = false. "
          "What is the weight of this sample? (Round to 2 decimal places.)",
     "answer": {"lo": 0.445, "hi": 0.455},
     "solution": "In likelihood weighting the weight is the product of the likelihoods of the evidence variables given their parents in the sample. "
                 "w = P(s | ¬c) × P(w | s, ¬r) = 0.5 × 0.90 = 0.45. "
                 "The probabilities of the sampled non-evidence values (P(¬c), P(¬r | ¬c)) are not part of the weight."},

    {"topic": "Sampling", "type": "NAT", "marks": 2,
     "q": SPR + "Likelihood weighting with evidence S = true, W = true produces exactly four samples of (C, R): (c, r), (¬c, r), (¬c, ¬r), (c, ¬r). "
          "Using the correct weights, compute the likelihood-weighting estimate of P(r | s, w). (Round to 3 decimal places.)",
     "answer": {"lo": 0.523, "hi": 0.524},
     "solution": "Weights w = P(s | C) × P(w | s, R): (c, r): 0.1×0.99 = 0.099; (¬c, r): 0.5×0.99 = 0.495; (¬c, ¬r): 0.5×0.90 = 0.45; (c, ¬r): 0.1×0.90 = 0.09. "
                 "Total weight = 0.099 + 0.495 + 0.45 + 0.09 = 1.134; weight with r = 0.099 + 0.495 = 0.594. "
                 "Estimate = 0.594/1.134 ≈ 0.5238 ≈ 0.524. "
                 "(The exact P(r | s, w) ≈ 0.320; with only four samples the estimate is far off, but LW is consistent as N → ∞.)"},

    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": "What is the main drawback of rejection sampling for computing P(X | e)?",
     "options": ["It rejects most samples when P(e) is small, and the fraction accepted drops exponentially with the number of evidence variables",
                 "It is not consistent: estimates do not converge even with infinitely many samples",
                 "It requires the Markov blanket of every variable",
                 "It can only be used when the evidence variables are root nodes"],
     "answer": [0],
     "solution": "Rejection sampling keeps only samples consistent with e, so about N·P(e) samples are useful; P(e) typically shrinks exponentially as evidence grows. "
                 "It is consistent (B is false). Markov blankets are used by Gibbs sampling, not rejection sampling (C false). "
                 "Evidence may be anywhere in the network (D false)."},

    {"topic": "Sampling", "type": "MSQ", "marks": 2,
     "q": "Which of the following statements about approximate inference in Bayesian networks are correct?",
     "options": ["Likelihood weighting produces consistent estimates",
                 "Likelihood weighting performs poorly when evidence variables are downstream (e.g. leaves), since samples of upstream variables ignore that evidence",
                 "Gibbs sampling resamples each non-evidence variable from its distribution conditioned on the current values of its Markov blanket",
                 "In rejection sampling, the fraction of accepted samples grows as more evidence variables are added"],
     "answer": [0, 1, 2],
     "solution": "(A) AIMA shows S<sub>WS</sub>(z, e) w(z, e) = P(z, e), so weighted estimates are consistent. "
                 "(B) Non-evidence variables are sampled from their parents only, so evidence at leaves does not influence them; many samples get tiny weights. "
                 "(C) This is exactly the Gibbs step: P(x<sub>i</sub> | mb(X<sub>i</sub>)). "
                 "(D) is false: each extra evidence variable generally reduces P(e), so fewer samples are accepted."},

    {"topic": "Sampling", "type": "NAT", "marks": 2,
     "q": SPR + "Gibbs sampling is run with evidence S = true, W = true. In the current state C = true. "
          "Compute the probability with which R is resampled to true, i.e. P(r | c, s, w). (Round to 3 decimal places.)",
     "answer": {"lo": 0.814, "hi": 0.815},
     "solution": "The Markov blanket of R is {C, S, W}. P(R | mb) = α P(R | c) P(w | s, R). "
                 "For r: 0.8 × 0.99 = 0.792. For ¬r: 0.2 × 0.90 = 0.18. "
                 "P(r | c, s, w) = 0.792/(0.792 + 0.18) = 0.792/0.972 ≈ 0.8148 ≈ 0.815."},

    {"topic": "Sampling", "type": "MCQ", "marks": 2,
     "q": SPR + "Gibbs sampling with evidence S = true, W = true is in the state where R = true. What is the probability that C is resampled to true, P(c | s, r)?",
     "options": ["0.444", "0.040", "0.500", "0.878"],
     "answer": [0],
     "solution": "MB(C) = {S, R} (its children; they have no other parents). P(C | s, r) = α P(C) P(s | C) P(r | C). "
                 "c: 0.5 × 0.1 × 0.8 = 0.04. ¬c: 0.5 × 0.5 × 0.2 = 0.05. P(c | s, r) = 0.04/0.09 ≈ 0.444. "
                 "0.040 is the unnormalized value, 0.500 is the prior, and 0.878 is P(c | ¬s, r)."},

    {"topic": "Sampling", "type": "NAT", "marks": 2,
     "q": SPR + "Gibbs sampling with evidence S = true, W = true starts in state C = true, R = false. "
          "One sweep first resamples C (given its Markov blanket), then resamples R (given its Markov blanket, using the new C). "
          "What is the probability that R = true at the end of the sweep? (Round to 3 decimal places.)",
     "answer": {"lo": 0.244, "hi": 0.245},
     "solution": "Step 1: P(c | s, ¬r) = α P(c)P(s | c)P(¬r | c): c: 0.5×0.1×0.2 = 0.01; ¬c: 0.5×0.5×0.8 = 0.2 → P(c) = 0.01/0.21 ≈ 0.04762. "
                 "Step 2: P(r | c, s, w) = 0.792/0.972 ≈ 0.81481; P(r | ¬c, s, w) = (0.2×0.99)/(0.2×0.99 + 0.8×0.90) = 0.198/0.918 ≈ 0.21569. "
                 "Total: 0.04762 × 0.81481 + 0.95238 × 0.21569 ≈ 0.03880 + 0.20542 = 0.2442 ≈ 0.244."},

    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": "A discrete variable Weather has distribution ⟨sunny: 0.2, cloudy: 0.5, rainy: 0.3⟩ (in that order). Using inverse-CDF sampling with "
          "cumulative intervals in the same order, which value is produced by the uniform random number u = 0.65?",
     "options": ["cloudy", "sunny", "rainy", "Cannot be determined from u alone"],
     "answer": [0],
     "solution": "Cumulative distribution: sunny [0, 0.2), cloudy [0.2, 0.7), rainy [0.7, 1.0). "
                 "u = 0.65 lies in [0.2, 0.7), so the sample is cloudy. "
                 "Inverse-CDF sampling is deterministic given u and the ordering, so (D) is wrong."},

    {"topic": "Sampling", "type": "NAT", "marks": 1,
     "q": "A continuous variable X has exponential density f(x) = 2e<sup>−2x</sup> for x ≥ 0. Using inverse-CDF sampling with uniform random number u = 0.75, "
          "what value of X is generated? (Round to 3 decimal places.)",
     "answer": {"lo": 0.692, "hi": 0.694},
     "solution": "The CDF is F(x) = 1 − e<sup>−2x</sup>. Solving F(x) = u gives x = −ln(1 − u)/2. "
                 "With u = 0.75: x = −ln(0.25)/2 = ln 4/2 = 1.3863/2 ≈ 0.693."},

    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": "For sampling-based estimates of a probability, the standard deviation of the estimate decreases as O(1/√N) in the number of samples N. "
          "Roughly how many samples are needed to halve the error obtained with N samples?",
     "options": ["4N", "2N", "N√2", "N<sup>2</sup>"],
     "answer": [0],
     "solution": "Error ∝ 1/√N, so halving the error requires √N' = 2√N, i.e. N' = 4N. "
                 "2N would reduce error only by a factor √2 ≈ 1.41; N√2 by 2<sup>1/4</sup>; N<sup>2</sup> is excessive and depends on N."},

    {"topic": "Sampling", "type": "MSQ", "marks": 1,
     "q": "Which statements correctly describe how sampling algorithms treat the evidence e?",
     "options": ["Likelihood weighting fixes evidence variables to their observed values and samples only non-evidence variables",
                 "Prior sampling ignores evidence while generating samples",
                 "Gibbs sampling changes the values of evidence variables during the Markov chain",
                 "Rejection sampling discards samples that are inconsistent with e"],
     "answer": [0, 1, 3],
     "solution": "(A) LW clamps evidence and weights each sample by ∏ P(e<sub>i</sub> | parents). "
                 "(B) Prior sampling generates from the prior; rejection sampling then filters these samples (D). "
                 "(C) is false: in Gibbs sampling evidence variables stay fixed at their observed values; only non-evidence variables are resampled."},

    {"topic": "Sampling", "type": "MCQ", "marks": 2,
     "q": "In likelihood weighting with evidence e and non-evidence variables z, let S<sub>WS</sub>(z, e) be the sampling probability and w(z, e) the weight. "
          "Which statement is correct?",
     "options": ["S<sub>WS</sub>(z, e) = ∏ P(z<sub>i</sub> | parents(Z<sub>i</sub>)), w(z, e) = ∏ P(e<sub>j</sub> | parents(E<sub>j</sub>)), and S<sub>WS</sub>(z, e)·w(z, e) = P(z, e)",
                 "S<sub>WS</sub>(z, e) = P(z | e), so all weights equal 1",
                 "S<sub>WS</sub>(z, e) = P(z, e) and w(z, e) = P(e)",
                 "S<sub>WS</sub>(z, e) = ∏ P(e<sub>j</sub> | parents(E<sub>j</sub>)), w(z, e) = ∏ P(z<sub>i</sub> | parents(Z<sub>i</sub>))"],
     "answer": [0],
     "solution": "Each non-evidence variable is sampled from its CPT given sampled/fixed parents, giving S<sub>WS</sub> = ∏ P(z<sub>i</sub> | parents). "
                 "The weight multiplies the evidence likelihoods. The product of these two is exactly the BN factorization of P(z, e), which proves consistency. "
                 "(B) is false: evidence at descendants is not taken into account while sampling, so S<sub>WS</sub> ≠ P(z | e) in general. "
                 "(C) and (D) misstate or swap the two products."},

    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": SPR + "When Gibbs sampling resamples Rain (R), the values of which variables must be consulted?",
     "options": ["C, S and W", "C only", "W only", "C and W only"],
     "answer": [0],
     "solution": "Gibbs samples R from P(R | mb(R)). mb(R) = parents {C} ∪ children {W} ∪ children's other parents {S} = {C, S, W}. "
                 "S is needed because P(w | S, R) depends on it (explaining away). The other options omit blanket members."},

    {"topic": "Sampling", "type": "MCQ", "marks": 1,
     "q": SPR + "Likelihood weighting is used with evidence C = true only (a root node), to estimate P(R | c). What is the weight of every sample?",
     "options": ["0.5", "1.0", "It depends on the sampled value of R", "0.8"],
     "answer": [0],
     "solution": "The weight is the product of P(e<sub>j</sub> | parents) over evidence variables; here only C, with no parents, so w = P(c) = 0.5 for every sample. "
                 "Since all weights are equal, LW reduces to sampling R from P(R | c), which is the exact posterior. "
                 "The weight does not depend on R, and 0.8 is P(r | c), a sampling probability, not a weight."},

    {"topic": "Sampling", "type": "MSQ", "marks": 2,
     "q": "Which statements about Gibbs sampling (as an MCMC method in Bayesian networks) are correct?",
     "options": ["Successive samples are generally correlated, not independent",
                 "With fixed evidence and all CPT entries strictly between 0 and 1, the chain's stationary distribution is P(X | e)",
                 "Each state of the Markov chain is a complete assignment to all variables, with evidence variables fixed",
                 "Each sample must be accepted or rejected depending on whether it agrees with the evidence"],
     "answer": [0, 1, 2],
     "solution": "(A) Each state is obtained by modifying the previous one, so samples are autocorrelated. "
                 "(B) Gibbs steps satisfy detailed balance with respect to P(x | e) and the chain is ergodic when there are no deterministic (0/1) entries, so it converges to the posterior. "
                 "(C) The state is a full assignment with evidence clamped. "
                 "(D) describes rejection sampling; Gibbs never rejects since evidence is clamped."},


]
