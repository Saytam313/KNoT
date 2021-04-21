import sys

from ufal.morphodita import *

#nacteni modelu
tagger = Tagger.load('/mnt/minerva1/nlp/projects/sentiment10/models/czech-morfflex-pdt-161115.tagger')

#prida slovni druhy a zakladni tvary slov zadanemu textu  
def parseText(text):

  if not tagger:
    sys.stderr.write("Cannot load tagger from file '%s'\n" % sys.argv[1])
    sys.exit(1)

  forms = Forms()
  lemmas = TaggedLemmas()
  tokens = TokenRanges()
  tokenizer = tagger.newTokenizer()
  if tokenizer is None:
    sys.stderr.write("No tokenizer is defined for the supplied model!")
    sys.exit(1)
  tokenizer=tokenizer.newVerticalTokenizer()
  tokenizer.setText(text)
  t = 0
  returnString=''
  while tokenizer.nextSentence(forms, tokens):
    tagger.tag(forms, lemmas)

    for i in range(len(lemmas)):
      lemma = lemmas[i]
      token = tokens[i]

      returnString+=str(text[token.start : token.start + token.length]+'\t'+lemma.tag+'\t'+lemma.lemma+'\n')

      t = token.start + token.length
    return str(returnString)