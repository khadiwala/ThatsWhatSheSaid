import twitter
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from pickle import dump,load
from random import shuffle

api = twitter.Api()

def filterfun(x):
    return ('@' not in x) and (x not in stopwords.words('english')) and ('thatswhatshesaid' not in x)

def get_data(terms):
    return reduce(lambda acc,l : acc + map(lambda x : x.text,l) ,[api.GetSearch(terms,page=p) for p in range(1,100)],[])

def get_words(data):
    words = reduce(lambda y,x : y + x.split(),data,list())
    words = filter(filterfun, words)
    return words

def get_features(tweet,features):
    words = set(tweet.split())
    words = filter(filterfun, words)
    instance = {}
    for w in features:
        instance['contains(%s)' % w] = (w in words)
    return instance

#if __name__ == '__main__':
if True:
    posfile = 'posdata.txt'
    negfile = 'negdata.txt'
    try:
        with open(posfile) as f:
            posdata = load(f)
            f.close()
    except:
       posdata = get_data(["thatswhatshesaid"])
       dump(posdata,open(posfile,"w+"))

    try:
        with open(negfile) as f:
            negdata = load(f)
            f.close()
    except:
        print "need negative data"
    data = posdata + negdata
    words = get_words(data)
    all_words = FreqDist(w.lower() for w in words)
    word_features = all_words.keys()[:2000]
    data = [get_features(x,word_features) for x in data]
    labeled_data = [(data[i],1) for i in range(len(posdata))] + [(data[len(posdata)+i],0) for i in range(len(posdata))]
    shuffle(labeled_data)
    cls = nltk.NaiveBayesClassifier.train(labeled_data[:-100])
    print nltk.classify.accuracy(cls,labeled_data[-100:])
    cls.show_most_informative_features(100)

