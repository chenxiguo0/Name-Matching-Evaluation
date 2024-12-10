
# fall-2024-assignment-04

This is assignment 4 for DSAN5400

Note: I have randomly sampled 10% of the data from both the training and test sets to simplify the handling and processing.

## B: 

| Method         | Precision | Recall | F1-Score |
|---------------|-----------|---------|----------|
| Exact Match   | 1.000     | 0.000   | 0.000    |
| Jaccard       | 0.002     | 0.750   | 0.003    |
| Levenshtein   | 0.035     | 0.750   | 0.067    |
| Cosine (TFIDF)| 0.923     | 0.600   | 0.727    |
| Cosine (TFIDF)| 0.001     | 0.800   | 0.001    |

## D: 

When adjusting thresholds:
- A threshold of 1.0 means we only consider perfect matches, leading to:
  - High precision (few false positives)
  - Low recall (many false negatives)
- A threshold of 0.01 means we accept almost any match, leading to:
  - Low precision (many false positives)
  - High recall (few false negatives)

## E:
To find the optimal threshold, we analyzed the precision-recall curves for each scorer. 
For the Jaccard similarity, the optimal threshold was found to be 0.818 based on maximizing the F1 score.
At this optimal threshold:
Precision: 0.002
Recall: 0.750
F1 Score: 0.003
This threshold provides the best balance between precision and recall for the Jaccard similarity metric. 

## F:
For the Jaccard similarity, the optimal threshold was found to be 0.688.
At this optimal threshold:
Precision: 0.035
Recall: 0.750
F1 Score: 0.067

## G:
For the TF-IDF Cosine similarity, the optimal threshold was found to be 0.515.
At this optimal threshold:
Precision: 0.923
Recall: 0.600
F1 Score: 0.727

## K
Some names have both English and Chinese versions, such as:
Mette Frederiksen vs. 梅特·弗雷泽里克森 (the same person, written in English and Chinese).
This highlights that the name-matching system needs to account for translations or transliterations (how names are written in one language vs. another), which may not always be straightforward or follow consistent rules.

For English-Russian paired names, several approaches could be considered:
1. Transliteration: Convert Russian characters to Latin alphabet
2. Phonetic matching: Compare names based on pronunciation
3. Character-level embeddings that are language-agnostic
4. Maintain separate scoring systems for each alphabet

## L:

(a)
The Jaro-Winkler similarity algorithm was chosen in this task for its effectiveness in measuring the similarity between two strings by taking into account character order and transpositions. It extends the basic Jaro similarity by giving higher scores to strings that match from the beginning, making it particularly suitable for name matching tasks where prefixes often carry significant importance.

For the Jaro-Winkler similarity, the optimal threshold was found to be 0.869.
At this optimal threshold:
Precision: 0.001
Recall: 0.800
F1 Score: 0.001

Compared to other methods, Jaro-Winkler achieved the highest recall (0.800), indicating its robustness in identifying true matches. But its precision is significantly lower than any other method, suggesting it produces a high number of false positives. This can be attributed to its tendency to overestimate similarity for names with shared prefixes or common patterns.

(b)
I implemented parallelization using Python's multiprocessing library to speed up name pair comparisons. 
The comparison using tfidf scorer was tested on the test dataset both sequentially and with parallelization.

Without Parallelization: Took 25.06 seconds.
With Parallelization: Took 24.68 seconds.

Machine Specs:
CPU: Apple M3
RAM: 8 GB
OS: macOS Sonoma 14.6.1

Parallelization improved processing time by approximately 0.4 seconds on the relatively small test dataset. It has the potential to be significantly more useful and efficient for larger datasets.
