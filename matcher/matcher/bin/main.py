import argparse
import logging
from pathlib import Path
from matcher.utils.parse_tsv import TsvIterator, split_and_sample_data
from matcher.eval.eval import evaluate, plot_precision_recall_curve
from matcher.name_matcher import ExactMatchScorer, JaccardScorer, LevenshteinScorer, TfidfScorer, JaroWinklerScorer
import numpy as np
import multiprocessing
import time

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs.txt'),
            logging.StreamHandler()
        ]
    )

# Parallelizing Name Pair
def process_comparison(comparison, scorer_class):
    scorer = scorer_class(comparison.name1, comparison.name2)
    pred_score = scorer.score(comparison.name1, comparison.name2)
    true_label = float(comparison.score)  
    return (comparison.name1, comparison.name2, true_label, pred_score)

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Name matching evaluation')
    parser.add_argument('-f', '--file', required=True, help='Path to dataset')
    parser.add_argument('-s', '--scorer', choices=['exact', 'jaccard', 'levenshtein', 'tfidf', 'jarowinkler'],
                      required=True, help='Scoring algorithm to use')
    parser.add_argument('-e', '--evaluate', action='store_true', help='Evaluate results')
    parser.add_argument('-p', '--print', action='store_true', help='Print results')
    parser.add_argument('--split', action='store_true', help='Split data into train and test')
    parser.add_argument('-o', '--output', help='Path to save results', default='data/results.tsv')

    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info(f"Starting name matching with {args.scorer} scorer")
    
    if args.split:
        base_path = Path(__file__).resolve().parent.parent.parent / 'data'
        input_file = base_path / 'annotated-index.tsv'
        output_train = base_path / 'annotated-index-train.tsv'
        output_test = base_path / 'annotated-index-test.tsv'
        
        # Call the function to split and sample the data 
        split_and_sample_data(input_file, output_train, output_test)
        logger.info("Data has been split and sampled. Saved to 'annotated-index-train.tsv' and 'annotated-index-test.tsv'.")
        return  
    
    # Create appropriate scorer
    scorer_classes = {
        'exact': ExactMatchScorer,
        'jaccard': JaccardScorer,
        'levenshtein': LevenshteinScorer,
        'tfidf': TfidfScorer,
        'jarowinkler': JaroWinklerScorer
    }
    
    scorer_class = scorer_classes[args.scorer]
    

    # Process data and compute scores
    results = []
    for i, comparison in enumerate(TsvIterator(args.file)):
        scorer = scorer_class(comparison.name1, comparison.name2)
        pred_score = scorer.score(comparison.name1, comparison.name2)
        true_label = float(comparison.score)  
        results.append((comparison.name1, comparison.name2, true_label, pred_score))
        
        if i % 1000 == 0:
            logger.info(f"Processed {i} comparisons")
    
    if args.evaluate:
        valid_results = [(n1, n2, tl, ps) for n1, n2, tl, ps in results if tl is not None]
        if not valid_results:
            logger.error("No valid labeled data found for evaluation")
            return
        
        true_labels = np.array([r[2] for r in valid_results])
        scores = np.array([r[3] for r in valid_results])

        optimal_threshold = plot_precision_recall_curve(true_labels, scores, args.scorer)
        logger.info(f"Optimal threshold for {args.scorer}: {optimal_threshold:.3f}")
        
        metrics = ['precision', 'recall', 'f1']
        for metric in metrics:
            score = evaluate(results, metric)
            logger.info(f"{metric.capitalize()}: {score:.3f}")
    
    end_time = time.time() 
    execution_time = end_time - start_time  
    logger.info(f"Execution Time: {execution_time:.2f} seconds")  

    if args.print:
        output_path = Path(args.output) if args.output else Path("data/results.tsv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write("Name1\tName2\tTrue_Label\tPredicted_Score\tScorer\n")  
            for name1, name2, true_label, pred_score in results:  
                f.write(f"{name1}\t{name2}\t{true_label}\t{pred_score:.3f}\t{args.scorer}\n")
        logger.info(f"Results successfully saved to {output_path}")

    # Parallelizing Name Pair setup
    scorer_class = scorer_classes[args.scorer]
    results = []

    with multiprocessing.Pool() as pool:
        comparisons = TsvIterator(args.file)
        results = pool.starmap(process_comparison, [(comp, scorer_class) for comp in comparisons])

if __name__ == "__main__":
    main()