import json
from allennlp.predictors.predictor import Predictor
from allennlp_models import pretrained
import allennlp_models.tagging
from spacy import Language
import GPUtil
import spacy
from spacy.matcher import Matcher, DependencyMatcher
from spacy.tokens import Doc, Token, Span
from spacy.language import Language
import textwrap
from transformers import logging
logging.set_verbosity_error()

from py2neo import Graph
from py2neo import *

graph = Graph("bolt://10.1.48.224:7687", auth=("neo4j", "neo123"))

try:
    Token.set_extension("SRL", default=dict())
except:
    pass

class SemanticRoleLabel:

    list_exceptions = []

    def __init__(self, ):
       # path_cached = os.environ["TMP_SETUP_FOLDER"] + "/structured-prediction-srl-bert.2020.12.15.tar.gz"
        self.allen_srl_pred = pretrained.load_predictor("structured-prediction-srl-bert")
        try:
            GPUs = GPUtil.getGPUs()
            flag_gpu = True
        except Exception as e:
            flag_gpu = False

        if flag_gpu is True:
            #to use GPU, solution in https://github.com/allenai/allennlp/issues/1567
            self.allen_srl_pred._model = self.allen_srl_pred._model.cuda()

    def __call__(self, doc):
        res_srl = self.srl_doc(ss = doc.text)
        for tok in doc:
            if tok.pos_ in ["VERB", "AUX"]:
                ii = tok.i
                try:
                    #search for the frame that is centered on this verb
                    frame_verb = [el for el in res_srl["verbs"] if el["tags"][ii] == "B-V"][0]
                    dict_args = self.post_process_verbframe(frame_verb) 

                    #skip cases of {'V': [8]}  
                    if len(list(dict_args.keys())) > 1:
                        tok._.SRL = dict_args
                except Exception as e:
                    self.list_exceptions.append("EXCEPTION:" + doc.text + "|||" + tok.text)
        return doc

    def srl_doc(self, ss):
        res_srl = self.allen_srl_pred.predict(ss)
        print("printing the output of the SRL model")
        print(res_srl)
        return res_srl

    def post_process_verbframe(self,frame_verb):
        tags = frame_verb["tags"]
        dict_args = {}
        current_role = None

        for jj in range(len(tags)):
            if current_role is None:
                if tags[jj] == "O":
                    pass
                else:
                    #begin a tag here
                    if tags[jj][0] == "B":
                        #may have one or multiple dashes (B-ARG1, B-ARGM-DIR) 
                        key = tags[jj][ tags[jj].find("-")+1:]
                        current_role = {key: [jj]}
                    else:
                        raise Exception("cannot be {} after O".format(tags[jj])) 
            else:
                if tags[jj] == "O":
                    #a role is ended
                    dict_args.update(current_role)
                    current_role = None
                elif tags[jj][0] == "I":
                    #continue the current role
                    current_role[list(current_role.keys())[0]].append(jj)
                elif tags[jj][0] == "B":
                    #a new tag follows immediately the previous tag (without any O in-between)
                    dict_args.update(current_role)
                    key = tags[jj][ tags[jj].find("-")+1:]
                    current_role = {key: [jj]}

        return dict_args
# end of class: SemanticRoleLabel


#this is specific to spacy v3
if Language.has_factory("srl") is False:
    @Language.factory("srl", 
                      assigns=["token._.SRL"],
                      requires=["token.tag"],
                      retokenizes = False)
    def srl(nlp, name):
        return SemanticRoleLabel()

nlp = spacy.load("en_core_web_trf") 
#nlp.add_pipe("srl")


if "srl" in nlp.pipe_names:
    nlp.remove_pipe("srl")

_ = nlp.add_pipe("srl")

#doc = nlp("The dog trashed the apartment in under 30 seconds.")
#print(doc._.srl)




def apply_pipeline_1(ss, flag_display = False):

    doc = nlp(ss)

    list_pipeline = []
    for tok in  doc:
        list_pipeline.append((tok.i, tok.text, tok.tag_, tok.pos_, tok.dep_, 
                              '\n'.join(textwrap.wrap(json.dumps(tok._.SRL), width = 60))
                              ))

    #a = Node("Frame", text="verb", span="", startIndex="", endIndex="")
    #b = Node("FrameArgument", type="", text="Bob", span="", startIndex="", endIndex="")
    
    frameDict ={}

    v = ""
    sg = ""
    PARTICIPANT = Relationship.type("PARTICIPANT")

    for tok in doc:
        sg=""
        v="" 
        frameDict={} 
        for x,y in tok._.SRL.items():
            span = doc[y[0]:y[len(y)-1]+1]
            if x == "V":
                # see if the token refers to verb (predicate)
                v = Node("Frame", text=span.text, startIndex=y[0], endIndex=y[len(y)-1])
                #frameDict[x] = v;
                # save the verb node seperately 
                sg=v
            else:
                # find all the respective argument nodes and save it to dictionary
                a = Node("FrameArgument", type= x, text=span.text, startIndex=y[0], endIndex=y[len(y)-1])
                frameDict[x] = a;
        
        if not sg:
            continue
        else:
            for i in frameDict:
                if not sg:
                    break;
                r = PARTICIPANT(frameDict[i],v)
                sg = sg | r

            graph.create(sg)

          #print(x, ": ",y, span.text)
            
            

             
                

    print("list pipeline: ", list_pipeline)
    print("------------------------------------------------")
    print(tok._.SRL)



#doc = nlp("The dog trashed the apartment in under 30 seconds.")
#doc = nlp("The dog trashed the apartment in under 30 seconds.")
#doc = nlp("The dog trashed the apartment in under 30 seconds.")
#apply_pipeline_1("The dog trashed the apartment in under 30 seconds")
#apply_pipeline_1("He that would make a golden gate, must bring a nail to it daily.")
#apply_pipeline_1("Marie Curie received the Nobel Prize in Physics in 1903. She became the first woman to win the prize and the first person — man or woman — to win the award twice.")
apply_pipeline_1("John bought a new 4-wheel car. Alice became the first person in his community to have 4-wheel car.")
#apply_pipeline_1("Marie Curie received the Nobel Prize in Physics in 1903. She became the first woman to win the prize and the first person — man or woman — to win the award twice.")