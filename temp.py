from allennlp.predictors.predictor import Predictor
from allennlp_models import pretrained
import allennlp_models.tagging

predictor = pretrained.load_predictor("structured-prediction-srl-bert")
print (predictor.predict(
    sentence="Did Uriah honestly think he could beat the game in under three hours?."
))
