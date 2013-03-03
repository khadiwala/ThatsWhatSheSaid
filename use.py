from pickle import load
from extract_features import get_get_features
from config import relpath

cls,fts = load(open(relpath("cls")))
gen = get_get_features(fts)

classify = lambda x : True if cls.classify(gen(x))=='1' else False
