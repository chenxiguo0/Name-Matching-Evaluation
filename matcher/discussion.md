[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/niDHHGwr)
# fall-2024-assignment-04

This is assignment 4 for DSAN5400

# Name Matcher Project Discussion

## Evaluation Results

| Method         | Precision | Recall | F1-Score |
|---------------|-----------|---------|----------|
| Exact Match   | 1.000     | 0.324   | 0.489    |
| Jaccard       | 0.892     | 0.763   | 0.823    |
| Levenshtein   | 0.901     | 0.812   | 0.854    |
| Cosine (TFIDF)| 0.923     | 0.847   | 0.883    |

## D: Threshold Analysis

When adjusting thresholds:
- A threshold of 1.0 means we only consider perfect matches, leading to:
  - High precision (few false positives)
  - Low recall (many false negatives)
- A threshold of 0.01 means we accept almost any match, leading to:
  - Low precision (many false positives)
  - High recall (few false negatives)

## EFG: Optimal Thresholds
- Jaccard Similarity: 0.65
- Levenshtein Distance: 0.82
- TF-IDF Cosine Similarity: 0.75

## K: Cross-Language Considerations

For English-Russian paired names, several approaches could be considered:
1. Transliteration: Convert Russian characters to Latin alphabet
2. Phonetic matching: Compare names based on pronunciation
3. Character-level embeddings that are language-agnostic
4. Maintain separate scoring systems for each alphabet
