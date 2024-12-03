[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/niDHHGwr)
# fall-2024-assignment-04

This is assignment 4 for DSAN5400


"""
# Name Matcher

This project implements various name matching algorithms to determine if two names refer to the same entity.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m matcher.bin.main -f data/annotated-index.tsv -s jaccard -e -p
```

Arguments:
- `-f, --file`: Path to dataset
- `-s, --scorer`: Scoring algorithm (exact/jaccard/levenshtein/tfidf)
- `-e, --evaluate`: Evaluate results
- `-p, --print`: Print results

## Running Tests

```bash
pytest
```
"""
