from extract_features import get_labeled_examples
from pickle import dump
import nltk

def train(fn):
    (labeled_instances,features) = get_labeled_examples()
    print "features etracted... ",
    cls = nltk.NaiveBayesClassifier.train(labeled_instances)
    print "classifier built"
    #print nltk.classify.accuracy(cls,labeled_instances[-100:])
    dump((cls,features),open(fn,"w+"))
    return cls

if __name__ == '__main__':
    cls = train("cls")
    cls.show_most_informative_features(100)

