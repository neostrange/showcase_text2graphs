from spacy import Language
import GPUtil
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

nlp = spacy.load("en_core_web_trf")
doc = nlp("Marie Curie received the Nobel Prize in Physics in 1903. She became the first woman to win the prize and the first person — man or woman — to win the award twice.")



span = doc[0:2]


print(span.text)

print(span.doc)

print(span.sent)
#for tok in doc:
    #print(tok.text, tok.ent_type_, tok.ent_iob_)

#for ent in doc.ents:
  #  print(ent.text,)

#for chunk in doc.noun_chunks:
 #   print(chunk.text)
