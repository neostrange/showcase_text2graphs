
class SemanticRoleLabel1:

    def __init__(self, create = True):
        if create:
            self.child = SemanticRoleLabel1(False)
        self.result = {'verbs': [{'verb': 'trashed', 'description': 
        '[ARG0: The dog] [V: trashed] [ARG1: the apartment] [ARGM-TMP: in under 30 seconds] .', 
        'tags': ['B-ARG0', 'I-ARG0', 'B-V', 'B-ARG1', 'I-ARG1', 'B-ARGM-TMP', 'I-ARGM-TMP',
        'I-ARGM-TMP', 'I-ARGM-TMP', 'O']}],
        'words': ['The', 'dog', 'trashed', 'the', 'apartment',
        'in', 'under', '30', 'seconds', '.']}
    
    #x= result.values()
    #print(x)
    #print(result["verbs"][0])

    #verbs= result["verbs"][0]

    #print(verbs.keys())


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



srl=SemanticRoleLabel1()
frame_verb = frame_verb = srl.result["verbs"][0]
dict_args = srl.post_process_verbframe(frame_verb)
print(dict_args)

#print (srl.result["verbs"][0])


