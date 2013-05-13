from itertools import chain
from time import time
from sklearn.linear_model import Perceptron, PassiveAggressiveClassifier, RidgeClassifier
from sklearn import cross_validation, metrics
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import NearestCentroid
from sklearn import feature_extraction as fe
import numpy as np
import pylab as pl


def tokens(s):
    return [word for word in s.rstrip().lower().split() if word not in stopwords]

def benchmark(clf, X, Y, train, test):
    clf_descr = clf[0]
    clf = clf[1]
    print(80 * '_')
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X[train], Y[train])
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X[test])
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.f1_score(Y[test], pred)
    print("f1-score:   %0.3f" % score)

    print("confusion matrix:")
    print(metrics.confusion_matrix(Y[test], pred))

    print()
    return clf_descr, score, train_time, test_time


load = lambda x  : open(x).readlines()
stopwords = set(open(load("english")))
stopwords.add("twss")
stopwords.add("fml")
pos = load("data/twss-stories-parsed.txt")
negs = ["data/fmylife-parsed.txt","data/texts-from-last-night-parsed.txt"]
neg = list(chain(*map(load,negs)))

pos_f = map(tokens, pos)
neg_f = map(tokens, neg)
all_f = chain(pos_f,neg_f)
target = np.concatenate([np.ones(len(pos)),np.zeros(len(neg))])

fh = fe.FeatureHasher(input_type='string')
all_h = fh.transform(all_f)

cv = cross_validation.KFold(all_h.shape[0], n_folds=5, shuffle=True)
train,test = next(iter(cv)) # just use one of the folds

clss = [
        ("Perceptron", Perceptron(n_iter=50,n_jobs=2)),
        ("BernoulliNB", BernoulliNB()),
        ("Ridge", RidgeClassifier(tol=1e-2, solver="lsqr")),
        ("NearestCentroid", NearestCentroid()),
        ("LinearSVC l1", LinearSVC(loss='l2', penalty="l1", dual=False, tol=1e-3)),
        ("LinearSVC l2", LinearSVC(loss='l2', penalty="l2", dual=False, tol=1e-3)),
        ("SGD l1", SGDClassifier(alpha=.0001, n_iter=50, penalty="l1")),
        ("SGD l2", SGDClassifier(alpha=.0001, n_iter=50, penalty="l2")),
        ("SGD elasticnet", SGDClassifier(alpha=.0001, n_iter=50, penalty="elasticnet"))
       ]
results = [benchmark(cls,all_h,target,train,test) for cls in clss]

### plot benchmarks ###

indices = np.arange(len(results))

collected = [[x[i] for x in results] for i in range(4)]

clf_names, score, training_time, test_time = collected
training_time = np.array(training_time) / np.max(training_time)
test_time = np.array(test_time) / np.max(test_time)

pl.title("Score")
pl.barh(indices, score, .2, label="score", color='r')
pl.barh(indices + .3, training_time, .2, label="training time", color='g')
pl.barh(indices + .6, test_time, .2, label="test time", color='b')
pl.yticks(())
pl.legend(loc='lower left', bbox_to_anchor=(1,.5))
pl.subplots_adjust(left=.25)

for i, c in zip(indices, clf_names):
    pl.text(-.3, i, c)


### Try out classifier ###

def to_sentences(document):
    text = ""
    for line in load(document):
        text += line
    return text.lower().split('.')

clf = LinearSVC(loss='l2', penalty="l1", dual=False, tol=1e-3)
clf.fit(all_h,target)

def get_twss(fn):
    sentences = to_sentences(fn)
    hashed = fh.transform(map(tokens,sentences))
    twss_pairs = filter(lambda x : x[1] == 1, zip(sentences,clf.predict(hashed)))
    return map(lambda x : x[0], twss_pairs)

for s in get_twss("data/2013-state-of-union.txt"):
    print(s.strip())

for s in get_twss("data/2002-state-of-union.txt"):
    print(s.strip())

