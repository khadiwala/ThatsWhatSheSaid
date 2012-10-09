from random import shuffle
from nltk.classify.util import apply_features
from nltk.probability import FreqDist
import re

tags = set(["twss","fml"])
filenames = ["learning/data/fmylife-parsed.txt","learning/texts-from-last-night-parsed.txt","learning//twss-stories-parsed.txt"]
stopwords = set(open("learning/english").readlines())

def is_not_stopword(w):
    return (w not in stopwords) and (w not in tags)

def get_words(sentence):
    words = re.findall(r'\w+', sentence)
    return filter(is_not_stopword, words)

def words_in_lines(lines):
    for lis in map(get_words,lines):
        for word in lis:
            yield word

def get_get_features(word_features):
    def get_features(s):
        words = get_words(s)
        instance = {}
        for w in word_features:
            instance['contains(%s)' % w] = (w in words)
        return instance
    return get_features

def get_labeled_examples(fn):
    labels = dict([(f,label) for f,label in zip(filenames,['0','0','1'])])  #fn -> label
    for f in filenames:
        print f,
        print labels[f]
    
    words = []
    for f in filenames:
        for word in words_in_lines(open(f).readlines()): #sacrifice preformance for memory
            words.append(word)
    all_words = FreqDist(w.lower() for w in words)
    word_features = all_words.keys()[:2000]        # 2000 most frequent words
    get_features = get_get_features(word_features) # create feature extractor
    
    #pair sentences and labels
    labeled_examples = []
    for f in filenames:
        labeled_examples.extend([(ex,labels[f]) for ex in open(f).readlines()])
    shuffle(labeled_examples)
    #extract features
    labeled_instances = apply_features(get_features,labeled_examples,labeled=True) #lazy map
    #dump(labeled_instances,open(fn,"w+"))
    return (labeled_instances, word_features)
