# -*- coding: utf-8 -*-
"""GATE DA question bank: Logic (propositional and first-order).

Every answer has been brute-force verified (truth tables / finite-domain
enumeration / a unification routine).
"""

PL = "Propositional Logic"
FOL = "Predicate Logic"

BANK = [
    # ------------------------------------------------------------------
    # PROPOSITIONAL LOGIC
    # ------------------------------------------------------------------
    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following propositional formulas is a tautology?",
     "options": ["(p → q) ∨ (q → p)", "(p → q) → (q → p)", "(p ∧ ¬q) → q", "(p ∨ q) → (p ∧ q)"],
     "answer": [0],
     "solution": "(p → q) ∨ (q → p) ≡ ¬p ∨ q ∨ ¬q ∨ p, which contains q ∨ ¬q, so it is true in all 4 rows. "
                 "(p → q) → (q → p) is false at p=F, q=T (antecedent T, consequent F). "
                 "(p ∧ ¬q) → q is false at p=T, q=F. (p ∨ q) → (p ∧ q) is false whenever exactly one of p, q is true. "
                 "Hence only the first is valid."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following is logically equivalent to p → q?",
     "options": ["¬q → ¬p", "q → p", "¬p → ¬q", "p ∧ ¬q"],
     "answer": [0],
     "solution": "The contrapositive ¬q → ¬p ≡ q ∨ ¬p ≡ p → q. The converse q → p and the inverse ¬p → ¬q are equivalent "
                 "to each other but differ from p → q at p=F, q=T (p → q is T, q → p is F). "
                 "p ∧ ¬q is the negation of p → q."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "How many of the 8 truth assignments to p, q, r are models of (p ∨ q) ∧ (¬p ∨ r)?",
     "options": [],
     "answer": {"lo": 4, "hi": 4},
     "solution": "Case p=T: the first clause is satisfied and the second requires r=T; q is free, giving 2 models. "
                 "Case p=F: the second clause is satisfied and the first requires q=T; r is free, giving 2 models. "
                 "Total = 2 + 2 = 4."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following formulas is satisfiable but NOT valid?",
     "options": ["p → (q → p)", "p ∧ ¬p", "(p ∧ q) → (p ∨ q)", "(p → q) → p"],
     "answer": [3],
     "solution": "(p → q) → p: when p=T it is true (consequent T); when p=F, p → q is T and the consequent is F, so it is false. "
                 "Hence it is satisfiable but not valid. p → (q → p) is valid (if p is T the consequent is T). "
                 "p ∧ ¬p is unsatisfiable. (p ∧ q) → (p ∨ q) is valid because p ∧ q ⊨ p ∨ q."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following entailments hold?",
     "options": ["{p → q, q → r} ⊨ p → r", "{p ∨ q, ¬p ∨ r} ⊨ q ∨ r",
                 "{p → q, q} ⊨ p", "{p → q, ¬q} ⊨ ¬p"],
     "answer": [0, 1, 3],
     "solution": "(A) Hypothetical syllogism: every model of both premises with p=T has q=T and hence r=T. "
                 "(B) This is exactly the resolution rule on p: if p=T then r must be T; if p=F then q must be T. "
                 "(C) Fails: p=F, q=T satisfies both premises but falsifies p (affirming the consequent). "
                 "(D) Modus tollens: if p were T then q would be T, contradicting ¬q. Truth tables confirm A, B, D."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "How many models over the symbols p, q, r does (p → q) ∧ (q → r) ∧ (r → p) have?",
     "options": [],
     "answer": {"lo": 2, "hi": 2},
     "solution": "The cycle of implications p → q → r → p forces p, q, r to have the same truth value: if any one is T, "
                 "all following ones are T, and the cycle returns. So the only models are all-T and all-F, i.e. 2 models."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "How many of the 32 truth assignments to x<sub>1</sub>, …, x<sub>5</sub> satisfy "
          "(x<sub>1</sub> → x<sub>2</sub>) ∧ (x<sub>2</sub> → x<sub>3</sub>) ∧ (x<sub>3</sub> → x<sub>4</sub>) ∧ (x<sub>4</sub> → x<sub>5</sub>)?",
     "options": [],
     "answer": {"lo": 6, "hi": 6},
     "solution": "The constraints say once some x<sub>i</sub> is T, every later x<sub>j</sub> (j &gt; i) must be T. "
                 "So a model is a string of F's followed by a string of T's, e.g. FFTTT. "
                 "The position where T's begin can be 1, 2, 3, 4, 5 or 'never' (all F), giving 6 models. "
                 "Brute-force over all 32 assignments confirms 6."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following clauses are Horn clauses?",
     "options": ["¬p ∨ ¬q ∨ r", "p ∨ q", "¬p ∨ ¬q", "r"],
     "answer": [0, 2, 3],
     "solution": "A Horn clause is a disjunction of literals with at most one positive literal. "
                 "¬p ∨ ¬q ∨ r has one positive literal (a definite clause, i.e. p ∧ q → r). "
                 "¬p ∨ ¬q has zero positive literals (a goal clause). r is a single positive literal (a fact). "
                 "p ∨ q has two positive literals, so it is not Horn."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following formulas is in conjunctive normal form AND is logically equivalent to p ↔ q?",
     "options": ["(¬p ∨ q) ∧ (p ∨ ¬q)", "(p ∧ q) ∨ (¬p ∧ ¬q)", "(p ∨ q) ∧ (¬p ∨ ¬q)", "(¬p ∨ q) ∧ (p ∨ ¬q) ∧ (p ∨ q)"],
     "answer": [0],
     "solution": "p ↔ q ≡ (p → q) ∧ (q → p) ≡ (¬p ∨ q) ∧ (p ∨ ¬q), which is a CNF. "
                 "(p ∧ q) ∨ (¬p ∧ ¬q) is equivalent but is in DNF, not CNF. "
                 "(p ∨ q) ∧ (¬p ∨ ¬q) is true exactly when one of p, q is true, i.e. p ⊕ q. "
                 "The last option adds the clause p ∨ q, which removes the model p=q=F, leaving only p ∧ q."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "The canonical CNF (product of maxterms, each clause containing all variables) of p ⊕ q ⊕ r has how many clauses?",
     "options": [],
     "answer": {"lo": 4, "hi": 4},
     "solution": "In the canonical CNF there is one maxterm (clause) for every falsifying assignment. "
                 "p ⊕ q ⊕ r is false exactly when an even number of variables is true: FFF, TTF, TFT, FTT. "
                 "That gives 4 falsifying rows and hence 4 clauses. It is also known that no shorter CNF exists for parity, "
                 "since every clause must contain all 3 variables."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "In how many rows of the truth table over p, q is (p → q) ↔ (¬q → p) true?",
     "options": [],
     "answer": {"lo": 2, "hi": 2},
     "solution": "p → q ≡ ¬p ∨ q and ¬q → p ≡ p ∨ q. Row TT: T, T → T. Row TF: F, T → F. Row FT: T, T → T. "
                 "Row FF: T, F → F. So the biconditional is true in 2 rows."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following formulas are valid?",
     "options": ["((p → q) ∧ (q → r)) → (p → r)", "(p → (q → r)) ↔ ((p ∧ q) → r)",
                 "((p → q) → r) ↔ (p → (q → r))", "(¬p → ⊥) → p"],
     "answer": [0, 1, 3],
     "solution": "(A) Transitivity of implication; a truth table shows no falsifying row. "
                 "(B) Exportation: both sides are equivalent to ¬p ∨ ¬q ∨ r. "
                 "(C) Not valid: at p=F, q=F, r=F the left side (p → q) → r is T → F = F, while the right side is T. "
                 "Implication is not associative. "
                 "(D) ¬p → ⊥ ≡ ¬¬p ≡ p, so the formula is p → p, which is valid (this is the basis of proof by contradiction)."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Consider the clauses C<sub>1</sub> = p ∨ q ∨ ¬r and C<sub>2</sub> = ¬p ∨ r ∨ s. Which one of the following statements is correct?",
     "options": ["q ∨ s is a valid resolvent of C<sub>1</sub> and C<sub>2</sub>",
                 "Every resolvent of C<sub>1</sub> and C<sub>2</sub> is a tautology",
                 "C<sub>1</sub> and C<sub>2</sub> have no resolvent",
                 "The empty clause can be derived from C<sub>1</sub> and C<sub>2</sub>"],
     "answer": [1],
     "solution": "C<sub>1</sub> and C<sub>2</sub> clash on two pairs, p/¬p and ¬r/r. Resolution removes exactly one complementary pair at a time. "
                 "Resolving on p gives q ∨ ¬r ∨ r ∨ s; resolving on r gives p ∨ ¬p ∨ q ∨ s. Both contain a complementary pair, "
                 "so both are tautologies. Removing both pairs at once to get q ∨ s is unsound: p=T, q=F, r=T, s=F satisfies "
                 "C<sub>1</sub> and C<sub>2</sub> but falsifies q ∨ s. The pair is satisfiable, so □ cannot be derived."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "A propositional Horn knowledge base contains the facts A and B and the definite clauses "
          "A ∧ B → C, C → D, D ∧ E → F, B → E, F ∧ G → H, H → A. "
          "Forward chaining is run to completion. How many distinct proposition symbols are inferred to be true (count the initial facts too)?",
     "options": [],
     "answer": {"lo": 6, "hi": 6},
     "solution": "Start with {A, B}. A ∧ B → C adds C; C → D adds D; B → E adds E; D ∧ E → F adds F. "
                 "F ∧ G → H never fires because G is never derived, and H → A adds nothing new. "
                 "The agenda empties with {A, B, C, D, E, F}, i.e. 6 symbols. Because forward chaining is sound and complete for Horn KBs, "
                 "these are exactly the entailed atoms."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following statements about forward and backward chaining over Horn knowledge bases is correct?",
     "options": ["Forward chaining is data-driven while backward chaining is goal-driven",
                 "Forward chaining is goal-driven while backward chaining is data-driven",
                 "Both are complete for arbitrary (non-Horn) propositional knowledge bases",
                 "Backward chaining can derive facts that forward chaining cannot"],
     "answer": [0],
     "solution": "Forward chaining starts from known facts and fires rules whose premises are satisfied (data-driven). "
                 "Backward chaining starts from the query and works back through rules whose conclusion matches (goal-driven). "
                 "Both are complete only for Horn (definite clause) KBs, not arbitrary ones. "
                 "For Horn KBs both derive exactly the entailed atoms, so neither derives anything the other cannot."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following statements are TRUE?",
     "options": ["Propositional resolution is refutation-complete",
                 "Modus ponens alone is complete for arbitrary propositional knowledge bases",
                 "Forward chaining is sound and complete for knowledge bases of definite clauses",
                 "A sound inference procedure derives only sentences that are entailed by the KB"],
     "answer": [0, 2, 3],
     "solution": "(A) True: if KB ∧ ¬α is unsatisfiable, resolution derives the empty clause. "
                 "(B) False: from p ∨ q, p → r, q → r, modus ponens cannot derive r, although r is entailed. "
                 "(C) True for definite clauses (Horn KBs with exactly one positive literal per clause). "
                 "(D) This is the definition of soundness (truth-preserving)."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "For propositional sentences α and β, α ⊨ β holds if and only if",
     "options": ["α ∧ ¬β is unsatisfiable", "α ∧ β is satisfiable", "¬α ∨ β is satisfiable", "α ∨ ¬β is valid"],
     "answer": [0],
     "solution": "α ⊨ β means every model of α is a model of β, i.e. no model makes α true and β false, i.e. α ∧ ¬β is unsatisfiable. "
                 "Equivalently α → β is valid. Satisfiability of ¬α ∨ β or α ∧ β is too weak (one model is enough). "
                 "α ∨ ¬β being valid would mean β ⊨ α, the reverse direction."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following are logically equivalent to p → (q ∨ r)?",
     "options": ["(p ∧ ¬q) → r", "(p → q) ∨ (p → r)", "¬r → (p → q)", "(p → q) ∧ (p → r)"],
     "answer": [0, 1, 2],
     "solution": "p → (q ∨ r) ≡ ¬p ∨ q ∨ r. (A) (p ∧ ¬q) → r ≡ ¬p ∨ q ∨ r. "
                 "(B) (¬p ∨ q) ∨ (¬p ∨ r) ≡ ¬p ∨ q ∨ r. (C) ¬r → (¬p ∨ q) ≡ r ∨ ¬p ∨ q. "
                 "(D) (p → q) ∧ (p → r) ≡ p → (q ∧ r), which is false at p=T, q=T, r=F whereas the original is true there."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "Of the 16 possible binary Boolean connectives ∘ (functions {T,F}<sup>2</sup> → {T,F}), how many are commutative, i.e. satisfy p ∘ q ≡ q ∘ p?",
     "options": [],
     "answer": {"lo": 8, "hi": 8},
     "solution": "A binary connective is fixed by its outputs on TT, TF, FT, FF. Commutativity requires output(TF) = output(FT). "
                 "So we may freely choose the outputs on TT, FF and the common value on TF/FT: 2<sup>3</sup> = 8. "
                 "Examples: ∧, ∨, ↔, ⊕, NAND, NOR, constant T, constant F."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following sets of connectives is NOT functionally complete?",
     "options": ["{¬, ∧}", "{NAND}", "{→, ⊥}", "{∧, ∨, ↔}"],
     "answer": [3],
     "solution": "∧, ∨ and ↔ all output T when every input is T (T ∧ T = T, T ∨ T = T, T ↔ T = T). "
                 "Hence every formula built from them is T under the all-true assignment, so ¬p cannot be expressed. "
                 "{¬, ∧} is complete by De Morgan. NAND alone is complete (¬p = p NAND p). "
                 "With → and ⊥ we get ¬p ≡ p → ⊥ and p ∨ q ≡ ¬p → q, so {→, ⊥} is complete."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "Of the 16 binary connectives ∘, for how many is the formula (p ∘ q) → p a tautology?",
     "options": [],
     "answer": {"lo": 4, "hi": 4},
     "solution": "(p ∘ q) → p can fail only in rows where p = F, and it fails there iff p ∘ q = T. "
                 "So we need F ∘ T = F and F ∘ F = F, while T ∘ T and T ∘ F are free. "
                 "That gives 2<sup>2</sup> = 4 connectives: constant F, p ∧ q, p ∧ ¬q, and the projection p."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "¬(p → q) is logically equivalent to",
     "options": ["p ∧ ¬q", "¬p ∧ q", "¬p → ¬q", "¬p ∨ q"],
     "answer": [0],
     "solution": "p → q ≡ ¬p ∨ q, so ¬(p → q) ≡ ¬(¬p ∨ q) ≡ p ∧ ¬q by De Morgan's law. "
                 "It is true only in the row p=T, q=F, which is exactly the row where p → q is false. "
                 "¬p ∧ q is true only at p=F, q=T; ¬p → ¬q is the inverse; ¬p ∨ q is p → q itself."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following formulas are in conjunctive normal form (CNF)?",
     "options": ["(p ∨ ¬q) ∧ r", "¬(p ∧ q)", "p ∨ ¬q ∨ r", "(p ∧ q) ∨ r"],
     "answer": [0, 2],
     "solution": "A CNF is a conjunction of clauses, each a disjunction of literals (negation only on atoms). "
                 "(p ∨ ¬q) ∧ r is two clauses. p ∨ ¬q ∨ r is a single clause, which is a (one-clause) CNF. "
                 "¬(p ∧ q) has negation applied to a compound formula, so it is not in CNF (its CNF is ¬p ∨ ¬q). "
                 "(p ∧ q) ∨ r has a conjunction inside a disjunction; its CNF is (p ∨ r) ∧ (q ∨ r)."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Let KB = {P → Q, Q → R, ¬R}. Which one of the following is entailed by KB?",
     "options": ["¬P ∧ ¬Q", "P ∨ Q", "¬P ∧ Q", "R"],
     "answer": [0],
     "solution": "From ¬R and Q → R, modus tollens gives ¬Q; from ¬Q and P → Q it gives ¬P. "
                 "The only model of KB (over P, Q, R) is P=F, Q=F, R=F, in which ¬P ∧ ¬Q is true. "
                 "P ∨ Q, ¬P ∧ Q and R are all false in that model, so they are not entailed."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Let α and β be propositional sentences. Which of the following statements are ALWAYS true?",
     "options": ["If α is satisfiable then ¬α is unsatisfiable", "If α is valid then ¬α is unsatisfiable",
                 "α ∨ β is satisfiable if and only if α is satisfiable or β is satisfiable",
                 "α ∧ β is satisfiable if and only if α is satisfiable and β is satisfiable"],
     "answer": [1, 2],
     "solution": "(A) False: p is satisfiable and so is ¬p. "
                 "(B) True: valid means true in all models, so ¬α is true in none. "
                 "(C) True: a model of α ∨ β is a model of α or of β, and conversely any model of α (or of β) is a model of α ∨ β. "
                 "(D) False: α = p and β = ¬p are each satisfiable but p ∧ ¬p is not (the 'if' direction fails)."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "How many truth assignments to x<sub>1</sub>, …, x<sub>5</sub> satisfy the 2-CNF "
          "(x<sub>1</sub> ∨ x<sub>2</sub>) ∧ (x<sub>2</sub> ∨ x<sub>3</sub>) ∧ (x<sub>3</sub> ∨ x<sub>4</sub>) ∧ (x<sub>4</sub> ∨ x<sub>5</sub>)?",
     "options": [],
     "answer": {"lo": 13, "hi": 13},
     "solution": "The formula says no two consecutive variables are both F. Let a<sub>n</sub> be the number of such strings of length n. "
                 "A valid string either ends in T (preceded by any valid string of length n−1) or ends in F, in which case the previous symbol must be T "
                 "(preceded by any valid string of length n−2). So a<sub>n</sub> = a<sub>n−1</sub> + a<sub>n−2</sub> with a<sub>1</sub> = 2, a<sub>2</sub> = 3. Then a<sub>3</sub> = 5, a<sub>4</sub> = 8, a<sub>5</sub> = 13. "
                 "Enumeration of all 32 assignments confirms 13."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following statements about Horn clauses and Horn-form knowledge bases are TRUE?",
     "options": ["Entailment of an atom from a Horn KB can be decided in time linear in the size of the KB",
                 "Every Horn clause has at most one positive literal",
                 "The clause ¬p ∨ q ∨ r is a Horn clause",
                 "The resolvent of two Horn clauses is again a Horn clause"],
     "answer": [0, 1, 3],
     "solution": "(A) True: forward chaining with premise counters runs in linear time. (B) True: this is the definition. "
                 "(C) False: q and r are both positive. "
                 "(D) True: if the clashing positive literal comes from C<sub>1</sub> (≤1 positive) and the negative from C<sub>2</sub>, "
                 "the resolvent contains C<sub>1</sub>'s other literals (all negative) plus C<sub>2</sub>'s remaining literals (≤1 positive), "
                 "so it has at most one positive literal."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following are tautologies?",
     "options": ["p ∨ ¬p", "¬(p ∧ ¬p)", "p → (p ∧ q)", "(p ∧ (p → q)) → q"],
     "answer": [0, 1, 3],
     "solution": "p ∨ ¬p (excluded middle) and ¬(p ∧ ¬p) (non-contradiction) are valid. "
                 "(p ∧ (p → q)) → q is the modus ponens tautology. "
                 "p → (p ∧ q) is false at p=T, q=F, so it is not valid."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "How many models over a, b, c does the CNF (a ∨ b ∨ c) ∧ (¬a ∨ ¬b) ∧ (¬b ∨ ¬c) ∧ (¬a ∨ ¬c) have?",
     "options": [],
     "answer": {"lo": 3, "hi": 3},
     "solution": "The first clause says at least one of a, b, c is true. The three binary clauses say no two are simultaneously true. "
                 "Together they encode 'exactly one of a, b, c is true', which has 3 models: (T,F,F), (F,T,F), (F,F,T)."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "To prove R from KB = {P ∨ Q, P → R, Q → R} by resolution refutation, the clause ¬R is added to the clauses of KB. "
          "What is the minimum number of resolution steps needed to derive the empty clause? (Each step resolves two clauses on one complementary pair; duplicate literals are merged.)",
     "options": [],
     "answer": {"lo": 3, "hi": 3},
     "solution": "Clauses: P ∨ Q, ¬P ∨ R, ¬Q ∨ R, ¬R. A 3-step refutation: (P ∨ Q, ¬P ∨ R) ⟹ Q ∨ R; (Q ∨ R, ¬Q ∨ R) ⟹ R; (R, ¬R) ⟹ □. "
                 "2 steps are impossible: the last step must resolve two complementary unit clauses, and the only unit initially is ¬R. "
                 "So R (a unit) must be produced in a single step, but every one-step resolvent is Q ∨ R, P ∨ R, ¬P, ¬Q or a tautology — never R. "
                 "Hence the minimum is 3 (a breadth-first search over resolution derivations confirms this)."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following sets of propositional formulas are unsatisfiable?",
     "options": ["{p ∨ q, ¬p ∨ q, p ∨ ¬q, ¬p ∨ ¬q}",
                 "{p → q, q → r, r → ¬p, p}",
                 "{p ↔ ¬q, q ↔ ¬r, r ↔ ¬p}",
                 "{p ∨ q ∨ r, ¬p ∨ ¬q, ¬q ∨ ¬r, ¬p ∨ ¬r}"],
     "answer": [0, 1, 2],
     "solution": "(A) The four clauses exclude all four (p, q) assignments, one each. "
                 "(B) From p we get q, then r, then ¬p — a contradiction. "
                 "(C) p = ¬q and q = ¬r give p = r, but r ↔ ¬p demands r = ¬p — contradiction (an odd cycle of negations). "
                 "(D) is satisfiable, e.g. p=T, q=F, r=F (exactly one true)."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "The clauses A ∨ B ∨ ¬C and ¬A ∨ B ∨ D are resolved on the symbol A. How many literals are in the resolvent (after merging duplicate literals)?",
     "options": [],
     "answer": {"lo": 3, "hi": 3},
     "solution": "Remove A and ¬A and take the union of the remaining literals: {B, ¬C} ∪ {B, D} = {B, ¬C, D}. "
                 "The duplicate B is merged (factoring), so the resolvent B ∨ ¬C ∨ D has 3 literals."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "Consider all propositional formulas over the symbols p, q, r, identified up to logical equivalence. How many of these equivalence classes φ satisfy (p ∧ q) ⊨ φ?",
     "options": [],
     "answer": {"lo": 64, "hi": 64},
     "solution": "Up to equivalence a formula is determined by its set of models, a subset of the 8 assignments. "
                 "(p ∧ q) ⊨ φ iff M(p ∧ q) ⊆ M(φ). Over p, q, r, M(p ∧ q) = {TTT, TTF} has 2 elements. "
                 "So M(φ) must contain these 2 assignments and may contain any subset of the other 6: 2<sup>6</sup> = 64."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following inference rules are sound in propositional logic?",
     "options": ["Modus ponens: from α → β and α infer β",
                 "And-elimination: from α ∧ β infer α",
                 "Abduction: from α → β and β infer α",
                 "Resolution: from α ∨ β and ¬β ∨ γ infer α ∨ γ"],
     "answer": [0, 1, 3],
     "solution": "Modus ponens, and-elimination and resolution are truth-preserving: whenever their premises are true, their conclusion is true. "
                 "For resolution, if β is true then γ must be true, else α must be true. "
                 "Abduction is unsound: α=F, β=T makes both premises true and the conclusion false."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following statements about the computational complexity of propositional reasoning is correct (assuming P ≠ NP)?",
     "options": ["Satisfiability of 3-CNF formulas can be decided in polynomial time",
                 "Deciding whether a propositional formula is valid is co-NP-complete",
                 "Satisfiability of Horn formulas is NP-complete",
                 "Satisfiability of 2-CNF formulas is NP-complete"],
     "answer": [1],
     "solution": "α is valid iff ¬α is unsatisfiable, and SAT is NP-complete, so VALIDITY (TAUT) is co-NP-complete. "
                 "3-SAT is NP-complete, so not in P under P ≠ NP. Horn-SAT is decidable in linear time (unit propagation / forward chaining). "
                 "2-SAT is decidable in linear time via the implication graph and strongly connected components."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "In the DPLL algorithm, a pure symbol is one that appears with the same sign in every clause in which it occurs. "
          "For the clause set {A ∨ ¬B, ¬B ∨ ¬C, C ∨ A}, which symbols are pure?",
     "options": ["A", "B", "C", "None of the symbols is pure"],
     "answer": [0, 1],
     "solution": "A occurs only positively (in A ∨ ¬B and C ∨ A), so it is pure; DPLL can set A = T. "
                 "B occurs only negatively (¬B twice), so it is pure; DPLL can set B = F. "
                 "C occurs negatively in ¬B ∨ ¬C and positively in C ∨ A, so it is not pure."},

    {"topic": PL, "type": "NAT", "marks": 1,
     "q": "The formula (A ∧ B) ∨ (C ∧ D) ∨ (E ∧ F) is converted to CNF by repeatedly distributing ∨ over ∧ (no simplification). How many clauses does the result have?",
     "options": [],
     "answer": {"lo": 8, "hi": 8},
     "solution": "Distribution produces one clause per way of choosing one literal from each conjunction: "
                 "{A, B} × {C, D} × {E, F}, i.e. 2 × 2 × 2 = 8 clauses such as A ∨ C ∨ E, A ∨ C ∨ F, …, B ∨ D ∨ F. "
                 "No clause is a tautology or a duplicate because all six symbols are distinct. "
                 "This illustrates the exponential blow-up of naive CNF conversion."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Let KB be a propositional knowledge base and α a sentence, and let M(·) denote the set of models. Which of the following are equivalent to KB ⊨ α?",
     "options": ["M(KB) ⊆ M(α)", "KB → α is valid", "KB ∧ ¬α is unsatisfiable", "KB ∧ α is satisfiable"],
     "answer": [0, 1, 2],
     "solution": "(A) is the definition of entailment: α is true in every model of KB. "
                 "(B) is the deduction theorem. (C) is the basis of proof by refutation (resolution). "
                 "(D) is weaker: KB = ⊤, α = p gives KB ∧ α satisfiable, but KB ⊭ α."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following formulas is in disjunctive normal form and is equivalent to (p ∨ q) ∧ ¬(p ∧ q ∧ r)?",
     "options": ["(p ∧ ¬q) ∨ (p ∧ ¬r) ∨ (q ∧ ¬p) ∨ (q ∧ ¬r)",
                 "(p ∧ ¬q) ∨ (¬p ∧ q)",
                 "(p ∧ ¬r) ∨ (q ∧ ¬r)",
                 "(p ∨ q) ∧ (¬p ∨ ¬q ∨ ¬r)"],
     "answer": [0],
     "solution": "Distribute: (p ∨ q) ∧ (¬p ∨ ¬q ∨ ¬r) = (p ∧ ¬p) ∨ (p ∧ ¬q) ∨ (p ∧ ¬r) ∨ (q ∧ ¬p) ∨ (q ∧ ¬q) ∨ (q ∧ ¬r); dropping the contradictory terms gives option A. "
                 "Option B (p ⊕ q) misses the model p=q=T, r=F. Option C misses p=T, q=F, r=T. "
                 "Option D is equivalent but is a CNF, not a DNF. Truth tables confirm A has exactly the 5 models of the original."},

    {"topic": PL, "type": "MSQ", "marks": 2,
     "q": "Which of the following formulas are contingent (satisfiable but not valid)?",
     "options": ["(p → q) ∧ (p → ¬q)", "(p → q) → (¬q → ¬p)", "(p ↔ q) ∧ (p ⊕ q)", "(p ∨ q) → (p ∧ ¬q)"],
     "answer": [0, 3],
     "solution": "(A) ≡ p → (q ∧ ¬q) ≡ ¬p: true at p=F, false at p=T, so contingent. "
                 "(B) An implication and its contrapositive are equivalent, so this is valid. "
                 "(C) p ↔ q and p ⊕ q are negations of each other, so their conjunction is unsatisfiable. "
                 "(D) True at p=q=F (antecedent false), false at p=F, q=T, so contingent."},

    {"topic": PL, "type": "NAT", "marks": 2,
     "q": "How many of the 16 truth assignments to p, q, r, s satisfy exactly two of the four clauses p ∨ q, ¬p ∨ r, ¬q ∨ s, ¬r ∨ ¬s? (Enter the number of assignments, not clauses.)",
     "options": [],
     "answer": {"lo": 2, "hi": 2},
     "solution": "Each clause, being a disjunction, is false only in specific situations: C1 false iff p=q=F; C2 iff p=T, r=F; C3 iff q=T, s=F; C4 iff r=s=T. "
                 "With 4 clauses, satisfying exactly two means falsifying exactly two. C1 is incompatible with C2 and C3 (they need p=T or q=T). "
                 "C1 &amp; C4: p=q=F, r=s=T — then C2, C3 hold → 1 assignment. C2 &amp; C3: p=T, r=F, q=T, s=F — C4 holds, C1 holds → 1 assignment. "
                 "C2 &amp; C4 needs r=F and r=T; C3 &amp; C4 needs s=F and s=T — impossible. Total = 2 (confirmed by enumeration)."},

    {"topic": PL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following statements about resolution is correct?",
     "options": ["Resolution is complete for deriving every entailed clause directly, without refutation",
                 "If a clause set is unsatisfiable, the resolution closure of the set contains the empty clause",
                 "If the resolution closure of a clause set does not contain the empty clause, the set may still be unsatisfiable",
                 "Resolution can derive the empty clause from a satisfiable set of clauses"],
     "answer": [1],
     "solution": "The ground resolution theorem: a clause set is unsatisfiable iff its resolution closure contains □. "
                 "So B is correct and C is false. D would contradict soundness. "
                 "A is false: resolution is only refutation-complete; e.g. from {p} it cannot derive the entailed clause p ∨ q directly."},

    {"topic": PL, "type": "MCQ", "marks": 1,
     "q": "Backward chaining over a propositional definite-clause KB is used to prove the query Q. Which clause is used FIRST?",
     "options": ["A clause whose head (conclusion) is Q", "A clause in which Q appears in the body",
                 "Any fact in the KB, chosen arbitrarily", "The negated query ¬Q added to the KB"],
     "answer": [0],
     "solution": "Backward chaining works from the goal: it looks for rules (or facts) whose conclusion is Q and recursively tries to prove their premises. "
                 "Using clauses with Q in the body is forward reasoning. Starting from facts is forward chaining. "
                 "Adding ¬Q is the resolution-refutation approach, not backward chaining."},

    {"topic": PL, "type": "MSQ", "marks": 1,
     "q": "Which of the following formulas are logically equivalent to p?",
     "options": ["p ∨ (p ∧ q)", "p ∧ (p ∨ q)", "(p ∨ q) ∧ (p ∨ ¬q)", "(p → q) → q"],
     "answer": [0, 1, 2],
     "solution": "(A) and (B) are the absorption laws. (C) By distribution, (p ∨ q) ∧ (p ∨ ¬q) ≡ p ∨ (q ∧ ¬q) ≡ p. "
                 "(D) (p → q) → q ≡ ¬(¬p ∨ q) ∨ q ≡ (p ∧ ¬q) ∨ q ≡ p ∨ q, which differs from p at p=F, q=T."},

    # ------------------------------------------------------------------
    # PREDICATE (FIRST-ORDER) LOGIC
    # ------------------------------------------------------------------
    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following is the correct first-order translation of 'Every student likes some course'?",
     "options": ["∀x (Student(x) → ∃y (Course(y) ∧ Likes(x, y)))",
                 "∀x (Student(x) ∧ ∃y (Course(y) ∧ Likes(x, y)))",
                 "∀x (Student(x) → ∃y (Course(y) → Likes(x, y)))",
                 "∃y ∀x (Student(x) ∧ Course(y) ∧ Likes(x, y))"],
     "answer": [0],
     "solution": "Universal quantifiers pair naturally with →, existential with ∧. "
                 "Option B claims everything in the domain is a student. "
                 "Option C is satisfied by any non-course y (making Course(y) → … vacuously true), so it does not require liking a course. "
                 "Option D says there is a single y that is a course liked by everything, and everything is a student — far too strong."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "The negation of ∀x ∃y (P(x, y) → Q(y)) is logically equivalent to",
     "options": ["∃x ∀y (P(x, y) ∧ ¬Q(y))", "∃x ∀y (¬P(x, y) → Q(y))", "∀x ∃y (P(x, y) ∧ ¬Q(y))", "∃x ∃y (P(x, y) ∧ ¬Q(y))"],
     "answer": [0],
     "solution": "Push ¬ inward: ¬∀x ∃y φ ≡ ∃x ¬∃y φ ≡ ∃x ∀y ¬φ. Then ¬(P → Q) ≡ P ∧ ¬Q, giving ∃x ∀y (P(x, y) ∧ ¬Q(y)). "
                 "Option B uses ¬P → Q ≡ P ∨ Q, which is not ¬(P → Q). Option C does not flip the quantifiers. "
                 "Option D flips only one quantifier correctly (∃y should become ∀y)."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Which of the following first-order sentences are valid?",
     "options": ["∃x ∀y P(x, y) → ∀y ∃x P(x, y)",
                 "∀y ∃x P(x, y) → ∃x ∀y P(x, y)",
                 "∀x (P(x) ∨ Q(x)) → (∀x P(x) ∨ ∀x Q(x))",
                 "∃x (P(x) ∧ Q(x)) → (∃x P(x) ∧ ∃x Q(x))"],
     "answer": [0, 3],
     "solution": "(A) If some a satisfies P(a, y) for all y, then for each y that same a is a witness — valid. "
                 "(B) Fails on domain {1, 2} with P(x, y) ⟺ x = y: each y has a witness, but no single x works for all y. "
                 "(C) Fails on domain {1, 2} with P = {1}, Q = {2}: every element is P or Q, but neither P nor Q holds everywhere. "
                 "(D) A witness a for P(a) ∧ Q(a) witnesses both ∃x P(x) and ∃x Q(x) — valid."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "In the formula ∀x (P(x, y) → ∃y Q(x, y, z)), which variables have free occurrences?",
     "options": ["y and z", "z only", "x, y and z", "x and z"],
     "answer": [0],
     "solution": "x is bound by ∀x throughout. The occurrence of y in P(x, y) is not in the scope of any ∃y/∀y, so it is free. "
                 "The y in Q(x, y, z) is bound by ∃y. z is never quantified, so it is free. "
                 "Hence the variables with free occurrences are y and z."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "What is the most general unifier (MGU) of Knows(John, x) and Knows(y, Mother(y))?",
     "options": ["{y/John, x/Mother(John)}", "{x/John, y/Mother(John)}", "{y/John, x/Mother(y)}", "The two atoms are not unifiable"],
     "answer": [0],
     "solution": "Unify arguments left to right. John vs y gives y/John. Then x vs Mother(y) becomes x vs Mother(John), giving x/Mother(John). "
                 "Applying {y/John, x/Mother(John)} to both atoms yields Knows(John, Mother(John)). "
                 "Option B binds the wrong variables. Option C leaves y in the binding of x, so it is not idempotent and does not make the atoms identical in one application."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "What is the most general unifier of P(f(x), g(y), y) and P(f(g(z)), w, z), where x, y, z, w are variables?",
     "options": ["{x/g(z), w/g(z), y/z}", "{x/g(z), w/g(y)}", "{x/g(a), w/g(a), y/a, z/a}", "The atoms are not unifiable"],
     "answer": [0],
     "solution": "f(x) vs f(g(z)) gives x/g(z). g(y) vs w gives w/g(y). y vs z gives y/z, and composing updates w/g(y) to w/g(z). "
                 "Both atoms become P(f(g(z)), g(z), z). Option B is not a unifier because y and z remain different. "
                 "Option C is a unifier but not most general (it is an instance of A with z/a). No occurs-check failure arises, so D is wrong."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Here x and y are variables, and a, b are constants. Which of the following pairs of atoms are unifiable (with the occurs check)?",
     "options": ["P(x, f(x)) and P(f(y), y)",
                 "Q(a, x, f(x)) and Q(y, b, f(b))",
                 "R(x, g(x)) and R(g(y), g(g(a)))",
                 "S(f(a), x) and S(x, f(b))"],
     "answer": [1, 2],
     "solution": "(A) x/f(y); then f(f(y)) must unify with y, which fails the occurs check. "
                 "(B) a/y gives y/a, x/b, then f(b) = f(b): MGU {y/a, x/b}. "
                 "(C) x/g(y), then g(g(y)) vs g(g(a)) gives y/a: MGU {x/g(a), y/a}. "
                 "(D) x/f(a), then f(a) must equal f(b), which fails since a ≠ b are distinct constants."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "Let the domain be D = {1, 2, 3}. How many interpretations of a binary predicate R over D satisfy ∀x ∀y (R(x, y) → R(y, x))?",
     "options": [],
     "answer": {"lo": 64, "hi": 64},
     "solution": "An interpretation of R is a subset of D × D (9 pairs). The sentence says R is symmetric. "
                 "The 3 diagonal pairs (x, x) can be chosen freely; the 3 unordered pairs {x, y} with x ≠ y must be included or excluded as a whole. "
                 "That is 2<sup>3</sup> × 2<sup>3</sup> = 64 relations."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "Let D = {1, 2, 3}. How many interpretations of a binary predicate R over D satisfy ∀x ∃y R(x, y) ∧ ∃y ∀x R(x, y)?",
     "options": [],
     "answer": {"lo": 169, "hi": 169},
     "solution": "∃y ∀x R(x, y) says some column of the 3 × 3 matrix is all T. This already implies ∀x ∃y R(x, y) (that column is a witness for every row), "
                 "so we only count relations with at least one full column. "
                 "Relations with no full column: each column has 7 non-full choices → 7<sup>3</sup> = 343. Answer = 512 − 343 = 169."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "Let D = {1, 2, 3}. How many interpretations of a binary predicate R over D satisfy ∀x ∀y (R(x, y) → ¬R(y, x))?",
     "options": [],
     "answer": {"lo": 27, "hi": 27},
     "solution": "Taking y = x gives R(x, x) → ¬R(x, x), so no diagonal pair may be in R (R is irreflexive). "
                 "For each of the 3 unordered pairs {x, y} with x ≠ y, at most one of (x, y), (y, x) is in R: 3 choices (neither, one, the other). "
                 "Total = 1 × 3<sup>3</sup> = 27 (asymmetric relations)."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "How many binary relations on the set {1, 2, 3} are transitive, i.e. satisfy ∀x ∀y ∀z (R(x, y) ∧ R(y, z) → R(x, z))?",
     "options": [],
     "answer": {"lo": 171, "hi": 171},
     "solution": "There is no simple closed formula; we enumerate all 2<sup>9</sup> = 512 relations and test the sentence for all 27 triples (x, y, z). "
                 "The count of transitive relations on a 3-element set is 171 (OEIS A006905: 1, 2, 13, 171, 3994, …). "
                 "Sanity check: on a 2-element set the same enumeration gives 13 of 16; the 3 failures contain both (1,2) and (2,1) but miss (1,1) or (2,2)."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "How many binary relations on {1, 2, 3} are both reflexive and symmetric?",
     "options": [],
     "answer": {"lo": 8, "hi": 8},
     "solution": "Reflexivity fixes all 3 diagonal pairs to be present. Symmetry ties (x, y) and (y, x) together for x ≠ y, "
                 "leaving 3 independent unordered pairs, each in or out. Total = 2<sup>3</sup> = 8."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "How many binary relations on {1, 2, 3} satisfy all three of ∀x R(x, x), ∀x ∀y (R(x, y) → R(y, x)) and ∀x ∀y ∀z (R(x, y) ∧ R(y, z) → R(x, z))?",
     "options": [],
     "answer": {"lo": 5, "hi": 5},
     "solution": "These are exactly the equivalence relations on a 3-element set, which correspond one-to-one with its partitions. "
                 "The number of partitions of a 3-set is the Bell number B<sub>3</sub> = 5: {123}, {1|23}, {2|13}, {3|12}, {1|2|3}. "
                 "Enumeration of all 512 relations confirms 5."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "Let D = {1, 2, 3} and let f be a unary function symbol. How many interpretations of f (functions D → D) satisfy ∀x f(f(x)) = f(x)?",
     "options": [],
     "answer": {"lo": 10, "hi": 10},
     "solution": "The condition says f is idempotent: f fixes every element of its image. Choose the image S (size k) — each element of S maps to itself — "
                 "and map every element outside S anywhere into S: k<sup>3−k</sup> ways. "
                 "Sum over k: k=1: 3 × 1<sup>2</sup> = 3; k=2: 3 × 2<sup>1</sup> = 6; k=3: 1 × 3<sup>0</sup> = 1. Total = 10."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "Let D = {1, 2, 3} and let f be a unary function symbol. How many interpretations of f satisfy ∀x f(f(x)) = x?",
     "options": [],
     "answer": {"lo": 4, "hi": 4},
     "solution": "f(f(x)) = x for all x means f is an involution: it is a bijection whose cycles have length 1 or 2. "
                 "On 3 elements: the identity (1 way) or exactly one transposition with one fixed point (3 ways). Total = 4."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "Skolemizing the sentence ∀x ∃y P(x, y) yields",
     "options": ["∀x P(x, F(x)), where F is a new function symbol", "∀x P(x, A), where A is a new constant",
                 "∃y P(y, y)", "∀x ∀y P(x, y)"],
     "answer": [0],
     "solution": "Since the existential ∃y lies within the scope of ∀x, the chosen y may depend on x, so it is replaced by a Skolem function F(x). "
                 "A Skolem constant would wrongly assert one y works for all x. "
                 "The result is satisfiable iff the original is (though not logically equivalent). ∀x ∀y P(x, y) is much stronger."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Skolemizing ∃x ∀y ∃z R(x, y, z) gives (A is a new constant, F, G new function symbols)",
     "options": ["∀y R(A, y, F(y))", "∀y R(A, y, F(A))", "∀y R(G(y), y, F(y))", "∀y R(A, y, B), with B a new constant"],
     "answer": [0],
     "solution": "x is existential and not inside any universal quantifier, so it becomes a constant A. "
                 "z is inside the scope of ∀y, so it becomes F(y) (arguments are the enclosing universally quantified variables). "
                 "F(A) ignores the dependence on y and is an unwarranted strengthening; G(y) for x is wrong because x precedes ∀y; "
                 "a constant for z also loses the dependence on y."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following is a prenex normal form equivalent to (∀x P(x)) → (∃y Q(y))?",
     "options": ["∃x ∃y (P(x) → Q(y))", "∀x ∃y (P(x) → Q(y))", "∀x ∀y (P(x) → Q(y))", "∃y ∀x (P(x) → Q(y))"],
     "answer": [0],
     "solution": "A quantifier pulled out of the antecedent of → flips: (∀x P(x)) → ψ ≡ ∃x (P(x) → ψ). From the consequent it does not flip: "
                 "φ → ∃y Q(y) ≡ ∃y (φ → Q(y)). So we get ∃x ∃y (P(x) → Q(y)). "
                 "Check option B on domain {1, 2} with P = {1}, Q = ∅: the original is true (∀x P(x) is false), but at x=1 no y makes P(1) → Q(y) true, so B is false. "
                 "C and D are false on the same interpretation."},

    {"topic": FOL, "type": "MSQ", "marks": 1,
     "q": "Which of the following correctly express 'Not every graph is connected'?",
     "options": ["¬∀x (Graph(x) → Connected(x))", "∃x (Graph(x) ∧ ¬Connected(x))",
                 "∀x (Graph(x) → ¬Connected(x))", "∃x (Graph(x) → ¬Connected(x))"],
     "answer": [0, 1],
     "solution": "Option A is the direct translation, and pushing the negation inward gives ∃x ¬(Graph(x) → Connected(x)) ≡ ∃x (Graph(x) ∧ ¬Connected(x)) — option B. "
                 "Option C says no graph is connected, which is stronger. "
                 "Option D is true whenever any non-graph exists (vacuous implication), so it does not express the statement."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "Which one of the following expresses 'None of my friends are perfect' (F(x): x is my friend, P(x): x is perfect)?",
     "options": ["∀x (F(x) → ¬P(x))", "∃x (F(x) ∧ ¬P(x))", "¬∀x (F(x) → P(x))", "∀x (¬F(x) → P(x))"],
     "answer": [0],
     "solution": "'None of my friends are perfect' ≡ ¬∃x (F(x) ∧ P(x)) ≡ ∀x ¬(F(x) ∧ P(x)) ≡ ∀x (F(x) → ¬P(x)). "
                 "Options B and C (which are equivalent to each other) only say some friend is not perfect. "
                 "Option D speaks about non-friends."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Consider the interpretation with domain D = {1, 2, 3} in which L(x, y) holds iff x &lt; y. Which of the following sentences are TRUE in this interpretation?",
     "options": ["∀x ∃y L(x, y)", "∃x ∀y ¬L(y, x)", "∀x ∀y (L(x, y) → ¬L(y, x))", "∀x ∀y (L(x, y) → ∃z (L(x, z) ∧ L(z, y)))"],
     "answer": [1, 2],
     "solution": "(A) False: for x = 3 no y in D is larger. (B) True: x = 1 has no y with y &lt; 1. "
                 "(C) True: &lt; is asymmetric. "
                 "(D) False: the order on {1, 2, 3} is not dense; for x = 1, y = 2 there is no z with 1 &lt; z &lt; 2. Evaluating all cases by enumeration confirms B and C."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "Interpret Div(x, y) as 'x divides y' over the domain D = {1, 2, …, 12}. For how many x ∈ D is the formula "
          "¬(x = 1) ∧ ∀y (Div(y, x) → (y = 1 ∨ y = x)) true?",
     "options": [],
     "answer": {"lo": 5, "hi": 5},
     "solution": "The formula says x ≠ 1 and the only divisors of x in D are 1 and x itself — i.e. x is prime. "
                 "(Every divisor of x ≤ 12 lies in D, so the restriction to D loses nothing.) "
                 "The primes in {1, …, 12} are 2, 3, 5, 7, 11, so the answer is 5."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Which of the following sentences (with equality) are true in exactly those interpretations where exactly one element satisfies P?",
     "options": ["∃x (P(x) ∧ ∀y (P(y) → y = x))", "∃x ∀y (P(y) ↔ y = x)",
                 "∃x ∀y ((P(x) ∧ P(y)) → x = y)", "∃x (P(x) ∧ ∀y (y = x → P(y)))"],
     "answer": [0, 1],
     "solution": "(A) Standard 'exactly one': some x is P and every P is x. (B) For some x, P(y) holds iff y = x — also exactly one; "
                 "A and B are equivalent. "
                 "(C) Is true when no element satisfies P (P(x) false makes the implication vacuous), so it expresses 'at most one'. "
                 "(D) The inner part is trivially implied by P(x), so it is just ∃x P(x) ('at least one'). "
                 "Brute force on domains of size 1–4 confirms that only A and B match 'exactly one'."},

    {"topic": FOL, "type": "MSQ", "marks": 1,
     "q": "Which of the following are sentences, i.e. formulas with no free variables (a is a constant)?",
     "options": ["(∀x P(x)) → Q(x)", "∀x (P(x) → ∃y R(x, y))", "∃x R(x, y)", "∀x ∃y (R(x, y) ∧ P(a))"],
     "answer": [1, 3],
     "solution": "(A) The scope of ∀x ends before →, so x in Q(x) is free. (B) x and y are bound everywhere. "
                 "(C) y is free. (D) x and y are bound; a is a constant, not a variable. Hence B and D are sentences."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "Resolving the first-order clauses P(x) ∨ Q(f(x)) and ¬P(g(y)) ∨ R(y) (variables already standardized apart) on P gives",
     "options": ["Q(f(g(y))) ∨ R(y)", "Q(f(x)) ∨ R(y)", "Q(g(f(y))) ∨ R(y)", "Q(f(y)) ∨ R(g(y))"],
     "answer": [0],
     "solution": "Unify P(x) with P(g(y)): MGU θ = {x/g(y)}. The resolvent is (Q(f(x)) ∨ R(y))θ = Q(f(g(y))) ∨ R(y). "
                 "Option B forgets to apply θ. Options C and D apply the substitution incorrectly."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Given the definite clauses King(x) ∧ Greedy(x) → Evil(x), King(John), and Greedy(y), Generalized Modus Ponens derives Evil(John) using which substitution?",
     "options": ["{x/John, y/John}", "{x/y}", "{x/John}", "{y/x, x/Evil}"],
     "answer": [0],
     "solution": "GMP needs one θ with King(x)θ = King(John)θ and Greedy(x)θ = Greedy(y)θ. "
                 "x/John matches the first premise; y/John then makes Greedy(y) match Greedy(John). "
                 "With only {x/John}, Greedy(John) and Greedy(y) are not syntactically identical, so the GMP side condition fails; {x/y} does not match King(John). "
                 "The conclusion is Evil(x)θ = Evil(John)."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Which of the following statements about first-order logic are TRUE?",
     "options": ["Entailment in first-order logic is semidecidable",
                 "Resolution (with factoring and unification) is refutation-complete for first-order logic",
                 "Validity of first-order sentences is decidable",
                 "Forward chaining on a Datalog KB (definite clauses without function symbols) always terminates"],
     "answer": [0, 1, 3],
     "solution": "(A) True: an algorithm can confirm every entailed sentence but may run forever on non-entailed ones (Turing/Church). "
                 "(B) True: Robinson's resolution theorem. (C) False: FOL validity is undecidable. "
                 "(D) True: with no function symbols only finitely many ground atoms exist, so a fixed point is reached in finitely many steps."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "In Existential Instantiation, the sentence ∃x Crown(x) ∧ OnHead(x, John) is replaced by Crown(C<sub>1</sub>) ∧ OnHead(C<sub>1</sub>, John). Which condition must C<sub>1</sub> satisfy?",
     "options": ["C<sub>1</sub> must be a new constant symbol not appearing anywhere else in the KB",
                 "C<sub>1</sub> must be John",
                 "C<sub>1</sub> may be any ground term already in the KB",
                 "C<sub>1</sub> must be a variable"],
     "answer": [0],
     "solution": "Existential Instantiation introduces a fresh Skolem constant naming the (unknown) witness. "
                 "Using an existing term such as John would assert, without justification, that John is the witness. "
                 "The result is inferentially equivalent (satisfiable iff the original), not logically equivalent. A variable would make it a non-ground formula."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "Let D = {1, 2, 3, 4}. How many interpretations of a unary predicate P over D make ∃x P(x) ∧ ¬∀x P(x) true?",
     "options": [],
     "answer": {"lo": 14, "hi": 14},
     "solution": "An interpretation of P is a subset of D: 2<sup>4</sup> = 16 choices. ∃x P(x) excludes the empty set, ¬∀x P(x) excludes D itself. "
                 "Hence 16 − 2 = 14."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "Let D = {1, 2, 3}. How many interpretations of two unary predicates P and Q over D (i.e. ordered pairs of subsets) satisfy ∀x (P(x) → Q(x)) ∧ ∃x (Q(x) ∧ ¬P(x))?",
     "options": [],
     "answer": {"lo": 19, "hi": 19},
     "solution": "∀x (P(x) → Q(x)) leaves each element 3 choices of (P, Q): (F,F), (F,T), (T,T); so 3<sup>3</sup> = 27 pairs. "
                 "The second conjunct requires at least one element with (F,T). Pairs with no (F,T) element: 2<sup>3</sup> = 8. "
                 "Answer = 27 − 8 = 19 (P is a proper subset of Q)."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Which of the following correctly express 'Every person who owns a dog is happy'?",
     "options": ["∀x ((Person(x) ∧ ∃y (Dog(y) ∧ Owns(x, y))) → Happy(x))",
                 "∀x ∀y ((Person(x) ∧ Dog(y) ∧ Owns(x, y)) → Happy(x))",
                 "∀x ∃y ((Person(x) ∧ Dog(y) ∧ Owns(x, y)) → Happy(x))",
                 "∀x (Person(x) → ∃y (Dog(y) ∧ Owns(x, y) ∧ Happy(x)))"],
     "answer": [0, 1],
     "solution": "(A) is the direct reading. (B) is equivalent: (∃y φ(y)) → ψ ≡ ∀y (φ(y) → ψ) when y is not free in ψ. "
                 "(C) ∃y (φ(y) → ψ) ≡ (∀y φ(y)) → ψ, which is vacuously true for x as soon as some object is not a dog owned by x, so it imposes almost no constraint. "
                 "(D) asserts every person owns a dog. Brute force on small domains confirms A ≡ B and that C, D differ."},

    {"topic": FOL, "type": "MCQ", "marks": 1,
     "q": "Over the finite domain {a, b}, the sentence ∀x ∃y R(x, y) is equivalent to which ground formula?",
     "options": ["(R(a, a) ∨ R(a, b)) ∧ (R(b, a) ∨ R(b, b))",
                 "(R(a, a) ∧ R(a, b)) ∨ (R(b, a) ∧ R(b, b))",
                 "(R(a, a) ∨ R(b, a)) ∧ (R(a, b) ∨ R(b, b))",
                 "R(a, a) ∧ R(b, b)"],
     "answer": [0],
     "solution": "Over a finite domain with every element named, ∀ becomes a conjunction over x and ∃ a disjunction over y. "
                 "For x = a: R(a, a) ∨ R(a, b); for x = b: R(b, a) ∨ R(b, b). Their conjunction is option A. "
                 "Option B is ∃x ∀y R(x, y). Option C is ∀y ∃x R(x, y) (every element has an R-predecessor). Option D is reflexivity."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Converting ∀x ((∃y P(x, y)) → (∃z Q(x, z))) to clausal form (with F a new Skolem function) gives",
     "options": ["¬P(x, y) ∨ Q(x, F(x))", "¬P(x, G(x)) ∨ Q(x, F(x))", "¬P(x, y) ∨ Q(x, C), with C a new constant", "¬P(x, y) ∧ Q(x, F(x))"],
     "answer": [0],
     "solution": "Eliminate →: ∀x (¬∃y P(x, y) ∨ ∃z Q(x, z)) ≡ ∀x (∀y ¬P(x, y) ∨ ∃z Q(x, z)). "
                 "y is now universal, so it stays a variable. z lies only within the scope of ∀x, so it becomes F(x). "
                 "Dropping universals gives the clause ¬P(x, y) ∨ Q(x, F(x)). Option B wrongly Skolemizes the universal y; "
                 "option C ignores the dependence of z on x; option D is not a clause and changes the meaning."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "Let D = {1, 2}. How many interpretations of a binary predicate R over D make the sentence ∀x ∃y R(x, y) → ∃y ∀x R(x, y) true?",
     "options": [],
     "answer": {"lo": 14, "hi": 14},
     "solution": "There are 2<sup>4</sup> = 16 relations. The sentence is false iff every row of the 2 × 2 matrix is non-empty but no column is full. "
                 "A column is full if both rows contain that column; so each row must be non-empty and the rows must have no common column, "
                 "forcing each row to be a single, different column: R = {(1,1), (2,2)} or R = {(1,2), (2,1)}. "
                 "So 2 interpretations falsify it and 16 − 2 = 14 satisfy it."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following is logically equivalent to ¬∃x (P(x) ∧ ∀y Q(x, y))?",
     "options": ["∀x (P(x) → ∃y ¬Q(x, y))", "∀x (¬P(x) ∧ ∃y ¬Q(x, y))", "∃x (¬P(x) ∨ ∃y ¬Q(x, y))", "∀x (P(x) ∧ ∃y ¬Q(x, y))"],
     "answer": [0],
     "solution": "¬∃x (…) ≡ ∀x ¬(P(x) ∧ ∀y Q(x, y)) ≡ ∀x (¬P(x) ∨ ∃y ¬Q(x, y)) ≡ ∀x (P(x) → ∃y ¬Q(x, y)). "
                 "Option B uses ∧ instead of ∨ (De Morgan applied wrongly). Option C fails to flip ∃x to ∀x. "
                 "Option D requires every element to satisfy P."},

    {"topic": FOL, "type": "MSQ", "marks": 1,
     "q": "Without standardizing variables apart, Unify(Knows(John, x), q) succeeds for which of the following atoms q?",
     "options": ["Knows(John, Jane)", "Knows(y, Bill)", "Knows(y, Mother(y))", "Knows(x, Elizabeth)"],
     "answer": [0, 1, 2],
     "solution": "(A) {x/Jane}. (B) {x/Bill, y/John}. (C) {y/John, x/Mother(John)}. "
                 "(D) fails: x would have to be both John and Elizabeth. Renaming the second x (standardizing apart) would make it succeed, "
                 "which is why AIMA insists on standardizing apart."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "A first-order language has constants a, b and one binary function symbol g. Let H<sub>0</sub> = {a, b} and H<sub>i+1</sub> = H<sub>i</sub> ∪ {g(s, t) : s, t ∈ H<sub>i</sub>}. "
          "How many ground terms are in H<sub>2</sub>?",
     "options": [],
     "answer": {"lo": 38, "hi": 38},
     "solution": "|H<sub>1</sub>| = 2 + 2<sup>2</sup> = 6: a, b, g(a,a), g(a,b), g(b,a), g(b,b). "
                 "H<sub>2</sub> = H<sub>1</sub> ∪ {g(s, t) : s, t ∈ H<sub>1</sub>}. The 36 terms g(s, t) are syntactically distinct, and they already include the 4 g-terms of H<sub>1</sub> "
                 "(since H<sub>0</sub> ⊆ H<sub>1</sub>); adding a and b gives |H<sub>2</sub>| = 2 + 6<sup>2</sup> = 38."},

    {"topic": FOL, "type": "NAT", "marks": 1,
     "q": "The KB contains the clauses ¬Man(x) ∨ Mortal(x) and Man(Socrates). To prove Mortal(Socrates) by resolution refutation, ¬Mortal(Socrates) is added. "
          "What is the minimum number of resolution steps needed to derive the empty clause?",
     "options": [],
     "answer": {"lo": 2, "hi": 2},
     "solution": "Step 1: resolve ¬Mortal(Socrates) with ¬Man(x) ∨ Mortal(x) using {x/Socrates}, giving ¬Man(Socrates). "
                 "Step 2: resolve ¬Man(Socrates) with Man(Socrates), giving □. "
                 "One step cannot suffice since no two initial clauses are complementary units. So the answer is 2."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "On the domain D = {1, 2, 3}, let R = {(1, 1), (1, 2), (1, 3), (2, 3)}. Which of the following sentences are TRUE in this interpretation?",
     "options": ["∀x ∀y ∀z (R(x, y) ∧ R(y, z) → R(x, z))", "∀x R(x, x)", "∃x ∀y R(x, y)", "∀y ∃x R(x, y)"],
     "answer": [0, 2, 3],
     "solution": "(A) The composable pairs are (1,1)(1,y) → (1,y) ∈ R, and (1,2)(2,3) → (1,3) ∈ R; so R is transitive. "
                 "(B) False: (2,2) ∉ R. (C) True with x = 1: (1,1), (1,2), (1,3) ∈ R. "
                 "(D) True: x = 1 works for every y. Enumeration over all triples confirms A, C, D."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "A KB consists of the definite clauses Nat(0) and Nat(x) → Nat(S(x)). Forward chaining is used to answer the query Nat(Foo), where Foo is a constant different from 0. Which one of the following is correct?",
     "options": ["Forward chaining never terminates, since it keeps adding Nat(S(…S(0)…))",
                 "Forward chaining terminates and answers 'not entailed'",
                 "Forward chaining derives Nat(Foo)",
                 "Forward chaining fails immediately since the KB is not in Datalog form and therefore cannot be processed"],
     "answer": [0],
     "solution": "Nat(Foo) is not entailed (there is a model where Foo is not a natural number). Forward chaining derives Nat(S(0)), Nat(S(S(0))), … forever, "
                 "because the function symbol S yields infinitely many ground terms. "
                 "This illustrates that FOL entailment with definite clauses is only semidecidable: entailed queries are eventually found, non-entailed ones may run forever. "
                 "Forward chaining still applies to non-Datalog KBs; it just lacks a termination guarantee."},

    {"topic": FOL, "type": "MCQ", "marks": 2,
     "q": "Which one of the following expresses 'No student likes every course' (S: student, C: course, L(x, y): x likes y)?",
     "options": ["∀x (S(x) → ∃y (C(y) ∧ ¬L(x, y)))",
                 "∀x (S(x) → ∃y (C(y) → ¬L(x, y)))",
                 "∀x ∀y ((S(x) ∧ C(y)) → ¬L(x, y))",
                 "∃x (S(x) ∧ ∃y (C(y) ∧ ¬L(x, y)))"],
     "answer": [0],
     "solution": "'No student likes every course' ≡ ¬∃x (S(x) ∧ ∀y (C(y) → L(x, y))) ≡ ∀x (S(x) → ∃y (C(y) ∧ ¬L(x, y))). "
                 "Option B is satisfied by any non-course y, so it is too weak. "
                 "Option C says no student likes any course — too strong. Option D only says some student fails to like some course."},

    {"topic": FOL, "type": "MSQ", "marks": 1,
     "q": "Which of the following equivalences are valid in first-order logic?",
     "options": ["∀x ∀y P(x, y) ≡ ∀y ∀x P(x, y)", "∃x ∃y P(x, y) ≡ ∃y ∃x P(x, y)",
                 "∀x ∃y P(x, y) ≡ ∃y ∀x P(x, y)", "∃x (P(x) ∨ Q(x)) ≡ ∃x P(x) ∨ ∃x Q(x)"],
     "answer": [0, 1, 3],
     "solution": "Quantifiers of the same kind commute (A, B). ∃ distributes over ∨ (D), just as ∀ distributes over ∧. "
                 "(C) Mixed quantifiers do not commute: with P(x, y) ⟺ x = y on {1, 2}, ∀x ∃y P is true but ∃y ∀x P is false."},

    {"topic": FOL, "type": "MSQ", "marks": 2,
     "q": "Let φ = ∀x ∃y (R(x, y) ∧ ¬R(y, x)). Which of the following statements are TRUE?",
     "options": ["φ has no model with a domain of size 1",
                 "φ has a model with domain {1, 2}",
                 "φ has a model with domain {1, 2, 3}",
                 "φ has a model with domain ℕ"],
     "answer": [0, 2, 3],
     "solution": "On {1}: y must be 1, and R(1, 1) ∧ ¬R(1, 1) is impossible, so no model. "
                 "On {1, 2}: element 1 needs y with R(1, y) ∧ ¬R(y, 1); y = 1 is impossible, so y = 2: R(1,2), ¬R(2,1). "
                 "Element 2 similarly needs R(2,1) ∧ ¬R(1,2) — contradiction; brute force over all 16 relations finds no model. "
                 "On {1, 2, 3} the 3-cycle R = {(1,2), (2,3), (3,1)} works, and on ℕ R(x, y) ⟺ x &lt; y works."},

    {"topic": FOL, "type": "NAT", "marks": 2,
     "q": "How many binary relations on {1, 2, 3} are partial orders, i.e. satisfy reflexivity ∀x R(x, x), antisymmetry ∀x ∀y (R(x, y) ∧ R(y, x) → x = y), and transitivity?",
     "options": [],
     "answer": {"lo": 19, "hi": 19},
     "solution": "Count labelled posets on 3 elements by shape: the antichain (1); one comparable pair plus an isolated point (3 × 2 = 6); "
                 "a chain (3! = 6); one element below two incomparable ones (3); one element above two incomparable ones (3). "
                 "Total = 1 + 6 + 6 + 3 + 3 = 19, which matches brute-force enumeration of all 512 relations."},
]
