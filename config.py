from os import path
relpath = lambda x : path.join(path.dirname(__file__),x)
filenames = ["data/fmylife-parsed.txt","data/texts-from-last-night-parsed.txt","data/twss-stories-parsed.txt"]
filenames = map(relpath, filenames)
labels = dict([(f,label) for f,label in zip(filenames,['0','0','1'])])  #fn -> label
stopwords = set(open(relpath("english")).readlines())
stopwords.add("twss")
stopwords.add("fml")
