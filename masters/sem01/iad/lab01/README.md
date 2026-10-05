# Lab01

Лабораторна робота з порівняння моделей машинного навчання для задачі бінарної класифікації мережевого трафіку.

Використано датасет **UNSW-NB15**, де:

- `0` -- нормальний трафік;
- `1` -- атака.

У notebook виконано:

- первинний аналіз даних;
- перевірку пропущених значень;
- кодування категоріальних ознак;
- EDA: correlation heatmap, histograms, boxplots;
- підготовку train/test вибірок;
- навчання моделей kNN, Decision Tree, SVM, Random Forest та AdaBoost;
- підбір `n_neighbors` для kNN;
- підбір `C` та `gamma` для SVM через `GridSearchCV`;
- порівняння моделей за Accuracy, Precision, Recall, F1-score та confusion matrix.

## Files

- `src/main.ipynb` -- основний notebook із кодом, графіками та результатами.
- `iad-lab01.typ` -- текстовий звіт до лабораторної роботи.
- `iad-lab01.pdf` -- згенерований звіт із файлу `iad-lab01.typ`
