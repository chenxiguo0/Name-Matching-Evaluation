import abc
import csv
import collections.abc
import dataclasses
import random
from matcher.name_matcher import NameMatchScorer

@dataclasses.dataclass
class Comparison:
    """Class representing two names and their similarity"""
    name1: str
    name2: str
    score: float = 0.0

class DocIterator(abc.ABC, collections.abc.Iterator):
    def __str__(self):
        return self.__class__.__name__

class TsvIterator(DocIterator):
    """Iterator to iterate over tsv-formatted documents"""
    def __init__(self, path):
        self.path = path
        self.fp = open(self.path)
        self.reader = csv.reader(self.fp, delimiter='\t')
        next(self.reader) # skip first row

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            row = next(self.reader)
            return Comparison(row[0], row[1], float(row[2])) #NameMatchScorer(row[0], row[1]).score(row[0], row[1]))
        except StopIteration:
            self.fp.close()
            raise

def write_comparisons_to_file(comparisons, output_path):
    """Writing Comparison to a new file"""
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['name1', 'name2', 'score'])  
        for comparison in comparisons:
            writer.writerow([comparison.name1, comparison.name2, comparison.score])


def split_and_sample_data(input_file, output_train, output_test, split_ratio=0.8, sample_ratio=0.1, random_seed=5400):
    """Splits the dataset into training and testing, then samples 10% from each set"""
    random.seed(random_seed)

    # Read all data
    data = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # skip header row
        for row in reader:
            data.append(row)

    # Find unique names
    unique_names = list(set(row[0] for row in data))
    train_names = random.sample(unique_names, int(len(unique_names) * split_ratio))
    test_names = [name for name in unique_names if name not in train_names]

    # Split the data into train and test sets
    train_data = [row for row in data if row[0] in train_names]
    test_data = [row for row in data if row[0] in test_names]

    # Sample 10% of the train and test data
    train_sampled = random.sample(train_data, int(len(train_data) * sample_ratio))
    test_sampled = random.sample(test_data, int(len(test_data) * sample_ratio))

    # Write sampled train and test sets to separate files
    with open(output_train, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['name1', 'name2', 'score'])
        writer.writerows(train_sampled)

    with open(output_test, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(['name1', 'name2', 'score'])
        writer.writerows(test_sampled)