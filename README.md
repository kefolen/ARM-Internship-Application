# ARM-Internship-Application

This repository contains a Python implementation for compressing a rule set that predicts whether a donor is "old" based on biomarkers.

## 🔍 How It Works

The script performs the following steps:

1. **Reads** a dataset and a rule file.
2. **Filters** the dataset using each rule to identify which donors are covered.
3. **Ranks** rules based on:
   - How many "old" donors they cover.
   - The probability they correctly classify as "old".
4. **Selects** a minimal subset of rules that cover as many positive examples as possible.
5. **Writes** the compressed rule set to `Data/ans.txt`.


## 💡 Heuristics Used for Compression

- **Coverage-based selection**: Prioritize rules that cover the most "old" donors not yet covered.
- **Precision scoring**: Prefer rules that have high accuracy in predicting "donor_is_old".
- **Iterative filtering**: After selecting a rule, remove already-covered rows to avoid redundancy.
- **Compactness**: Avoid overly specific or low-coverage rules unless necessary.


## 📄 Requirments
- python 3
- pandas


## 🛠️ Usage
Place your input files in the `Data/` directory:

- `dataset.tsv`: Tab-separated dataset with binary biomarker columns and a `donor_is_old` column.
- `rules.txt`: Rule file where each line represents one rule.

Then run the script:

```bash
python Implementation.py
```bash

The result will be saved in: Data/ans.txt

