from allennlp.predictors.predictor import Predictor
from spacy.language import Language
from spacy.tokens import Doc
from allennlp_models import pretrained
from transformers import logging
logging.set_verbosity_error()
import json


@Language.factory("srl", default_config={
    "model_path": "https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz"})
def create_srl_component(nlp: Language, name: str, model_path: str):
    return SRLComponent(nlp, model_path)


class SRLComponent:

    def __init__(self, nlp: Language, model_path: str):
        if not Doc.has_extension("srl"):
            Doc.set_extension("srl", default=None)
        #self.predictor = Predictor.from_path(model_path)
        self.predictor = pretrained.load_predictor("structured-prediction-srl-bert")


    def __call__(self, doc: Doc):
        predictions = self.predictor.predict(sentence=doc.text)
        doc._.srl = predictions
        return doc


if __name__ == '__main__':
    import spacy
    nlp = spacy.blank('en')
    nlp.add_pipe("srl")
    doc = nlp("The dog trashed the apartment in under 30 seconds.")
    print(doc._.srl)

    result = doc._.srl

    print(result.verbs[0])

