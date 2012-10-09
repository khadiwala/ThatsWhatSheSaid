from extract_features import get_labeled_examples
from random import shuffle
from pickle import dump
import nltk

def train(fn):
    (labeled_instances,get_features) = get_labeled_examples("train.txt")
    print type(labeled_instances)
    print "features etracted... ",
    cls = nltk.NaiveBayesClassifier.train(labeled_instances)
    print "classifier built"
    #print nltk.classify.accuracy(cls,labeled_instances[-100:])
    dump((cls,get_features),open(fn,"w+"))

if __name__ == '__main__':
    train("cls")
    #cls.show_most_informative_features(100)

