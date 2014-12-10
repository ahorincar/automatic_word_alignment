import nltk
from codecs import open
from nltk.align import AlignedSent, IBMModel1
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
from ibmmodel2 import IBMModel2

from nltk.tokenize import RegexpTokenizer

class Corpus(object):
  def __init__(self, fname):
    f = open(fname, 'r', encoding='utf-8')


    tokenizer = RegexpTokenizer(r'\w+')

    self.sents = []
    for line in f:
      if line not in ['\n', '\r\n']:
        self.sents.append(tokenizer.tokenize(line))

    for sent in self.sents:
      for i in xrange(len(sent)):
        sent[i] = sent[i].encode('unicode_escape')

    f.close()

  # def preprocessCorpus(self):
  #   return self.sents

  @classmethod
  def doStemming(self, corpus):
    stemmer = PorterStemmer()
    for sent in corpus.sents:
      for i in xrange(len(sent)):
        sent[i] = stemmer.stem(sent[i])
    return corpus

  @classmethod
  def doCapitalisation(self, corpus):
    for sent in corpus.sents:
      for i in xrange(len(sent)):
        sent[i] = sent[i].lower()

    return corpus

  @classmethod
  def doLemmatisation(self, corpus):
    lmtzr = WordNetLemmatizer()
    for sent in corpus.sents:
      for i in xrange(len(sent)):
        sent[i] = lmtzr.lemmatize(sent[i])
    return corpus

  @classmethod
  def computeAlignments(self, frst_corpus, scnd_corpus, chosen_ibm):
    i = 0
    aligned_sents = []

    while i < len(frst_corpus.sents):
      aligned_sents.append(AlignedSent(frst_corpus.sents[i], scnd_corpus.sents[i]))
      i += 1

    if chosen_ibm == "ibm1":
      ibm = IBMModel1(aligned_sents)
      return ibm.aligned()
    elif chosen_ibm == "ibm2":
      ibm = IBMModel2(aligned_sents)
      return ibm.aligned()
    else:
      ibm1 = IBMModel1(aligned_sents)
      ibm2 = IBMModel2(aligned_sents)
      return ibm1.aligned(), ibm2.aligned()

def demo():
  corpus1 = Corpus('/Users/antonia/Documents/Code/dissertation/data/corpus1.en.sgm')
  corpus2 = Corpus('/Users/antonia/Documents/Code/dissertation/data/corpus1.es.sgm')
  a_sents = Corpus.computeAlignments(corpus1, corpus2)

if __name__ == '__main__':
  demo()






