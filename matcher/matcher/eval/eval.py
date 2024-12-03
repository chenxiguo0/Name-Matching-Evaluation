from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve
import matplotlib.pyplot as plt

def evaluate(results, metric):
    """
    Evaluate the results using the specified metric
    """
    true_labels = [r[2] for r in results]  
    pred_scores = [r[3] for r in results]
    
    if metric == "precision":
        return precision_score(true_labels, [1 if s >= 0.5 else 0 for s in pred_scores])
    elif metric == "recall":
        return recall_score(true_labels, [1 if s >= 0.5 else 0 for s in pred_scores])
    elif metric == "f1":
        return f1_score(true_labels, [1 if s >= 0.5 else 0 for s in pred_scores])
    else:
        raise ValueError(f"Unknown metric: {metric}")

def plot_precision_recall_curve(y_true, scores, scorer_name):
    """Plot precision-recall curve and find optimal threshold"""
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    
    plt.figure()
    plt.plot(thresholds, precision[:-1], label='Precision')
    plt.plot(thresholds, recall[:-1], label='Recall')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.title(f'Precision-Recall Curve for {scorer_name}')
    plt.legend()
    plt.savefig(f'{scorer_name}_pr_curve.png')
    plt.close()
    
    # Find optimal threshold (F1 score)
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-9)
    optimal_threshold = thresholds[np.argmax(f1_scores[:-1])]
    
    return optimal_threshold