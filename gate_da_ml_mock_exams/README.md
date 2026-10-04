# GATE DA – Machine Learning: 50 Mock Tests

`GATE_DA_ML_Mock_Exams_50_Sets.pdf` (~877 pages) contains:

- Exam guide (GATE DA pattern, marking scheme, strategy) and syllabus coverage tables
- Concept & formula revision notes for GATE DA Section 6 with diagrams
- **50 sectional mock tests**: 35 questions / 55 marks each (15 × 1-mark + 20 × 2-mark),
  MCQ / MSQ / NAT, ~700 diagram-based questions in total
- Per test: answer key, self-evaluation sheet, detailed step-by-step solutions
- Master answer key

Topics: regression (simple/multiple/ridge/lasso), bias–variance, LOO & k-fold CV, gradient descent,
logistic regression, k-NN, naive Bayes, LDA, Bayes classifier, evaluation metrics/ROC, SVM & kernels,
decision trees & ensembles, perceptron/MLP/backprop, k-means/k-medoids, hierarchical clustering,
distance measures, cluster evaluation, PCA/SVD.

## Regenerating

```bash
pip install reportlab matplotlib numpy pillow
python build.py            # all 50 sets
python build.py --sets 2   # quick preview
python selftest.py topics.regression --pdf   # stress-test one topic module
```

Each question comes from a randomized template in `topics/` whose answer is computed in code.
