[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/niDHHGwr)
# fall-2024-assignment-04

This is assignment 4 for DSAN5400


"""
# Name Matching Evaluation Project

This project provides a set of name matching scorers and evaluates their performance using various metrics such as precision, recall, and F1 score. The project supports exact matching, Jaccard similarity, Levenshtein distance, and TF-IDF-based cosine similarity scoring. It also provides functionality to split datasets and perform evaluation with customizable parameters.

## Usage

Main Script:
The main script main.py is used to run the name matching evaluation. 
Below are the available arguments:

-f, --file (Required): Path to the dataset (e.g., queries.tsv).
-s, --scorer (Required): Scoring algorithm to use. Options: exact, jaccard, levenshtein, tfidf.
-e, --evaluate: Flag to evaluate the results after processing.
-p, --print: Flag to print the results to a file.
--split: Flag to split the dataset into training and test sets.
-o, --output: Path to save the results.


Example Usage:

python bin/main.py -f data/queries.tsv -s jaccard -e -p --split

## Data Format

The input data file (queries.tsv) should be in the following format:
name1  name2  score
"John"  "John"  1.0
"John"  "jane"  0.0

The output file (results.tsv) will contain the following columns:
Name1    Name2    True_Label    Predicted_Score    Scorer
"John"   "John"   1.0           1.0                "exact"


