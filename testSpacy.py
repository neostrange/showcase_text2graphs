from spacy import Language
import GPUtil
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from spacy.tokens import Doc, Token, Span
from spacy.language import Language

nlp = spacy.load("en_core_web_trf")
doc = nlp("He that would make a golden gate, must bring a nail to it daily.")

#for tok in doc:
#    print(tok.text)

for chunk in doc.noun_chunks:
    print(chunk.text)
