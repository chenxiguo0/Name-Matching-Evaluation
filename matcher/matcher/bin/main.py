import argparse
import logging
from pathlib import Path
from ..utils.parse_tsv import TsvIterator
from ..eval.eval import evaluate, plot_precision_recall_curve
from ..name_matcher import ExactMatchScorer, JaccardScorer, LevenshteinScorer, TfidfScorer

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs.txt'),
            logging.StreamHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='Name matching evaluation')
    parser.add_argument('-f', '--file', required=True, help='Path to dataset')
    parser.add_argument('-s', '--scorer', choices=['exact', 'jaccard', 'levenshtein', 'tfidf'],
                      required=True, help='Scoring algorithm to use')
    parser.add_argument('-e', '--evaluate', action='store_true', help='Evaluate results')
    parser.add_argument('-p', '--print', action='store_true', help='Print results')
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting name matching with {args.scorer} scorer")
    
    # Create appropriate scorer
    scorer_classes = {
        'exact': ExactMatchScorer,
        'jaccard': JaccardScorer,
        'levenshtein': LevenshteinScorer,
        'tfidf': TfidfScorer
    }
    
    scorer_class = scorer_classes[args.scorer]
    
    # Process data and compute scores
    results = []
    for i, comparison in enumerate(TsvIterator(args.file)):
        scorer = scorer_class(comparison.name1, comparison.name2)
        score = scorer.score(comparison.name1, comparison.name2)
        results.append((comparison.name1, comparison.name2, comparison.label, score))
        
        if i % 1000 == 0:
            logger.info(f"Processed {i} comparisons")
    
    if args.evaluate:
        metrics = ['precision', 'recall', 'f1']
        for metric in metrics:
            score = evaluate(results, metric)
            logger.info(f"{metric.capitalize()}: {score:.3f}")
    
    if args.print:
        for name1, name2, label, score in results:
            print(f"{name1}\t{name2}\t{score:.3f}\t{args.scorer}")

if __name__ == "__main__":
    main()