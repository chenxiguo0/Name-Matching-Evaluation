from sklearn.metrics import precision_score, recall_score, f1_score, precision_recall_curve
import matplotlib.pyplot as plt
import numpy as np

def evaluate(results, metric):
    """
    Evaluate the results using the specified metric
    """
    true_labels = np.array([float(r[2]) for r in results])
    pred_scores = np.array([float(r[3]) for r in results])
    
    true_labels_binary = (true_labels >= 0.5).astype(int)
    predictions = (pred_scores >= 0.5).astype(int)
    
    if metric == "precision":
        return precision_score(true_labels_binary, predictions, zero_division=1)  
    elif metric == "recall":
        return recall_score(true_labels_binary, predictions, zero_division=1)
    elif metric == "f1":
        return f1_score(true_labels_binary, predictions, zero_division=1)
    else:
        raise ValueError(f"Unknown metric: {metric}")

def plot_precision_recall_curve(y_true, scores, scorer_name):
    """Plot precision-recall curve and find optimal threshold"""
    
    y_true = np.array(y_true, dtype=float)
    scores = np.array(scores, dtype=float)

    y_true_binary = (y_true >= 0.5).astype(int)

    
    # Validate the data
    if not set(np.unique(y_true_binary)).issubset({0, 1}):
        raise ValueError("y_true must contain only binary values (0 or 1) after threshold")
    if not (np.all(scores >= 0) and np.all(scores <= 1)):
        raise ValueError("scores must be between 0 and 1")
        
    precision, recall, thresholds = precision_recall_curve(y_true_binary, scores)
        
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