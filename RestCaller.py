import requests
import json


def callAllenNlpApi(apiName, string):
    URL = "https://demo.allennlp.org/api/"+apiName+"/predict"

    PARAMS = {"Content-Type": "application/json"}

    payload = {"sentence":string}
    
    # sending post request and saving response as response object
    #r = requests.post(url = URL, data = data)
    
    # extracting response text 
    #pastebin_url = r.text

    #print("The pastebin URL is:%s"%pastebin_url)

    #headers = {"content-type": "application/json; charset=UTF-8"}
    #payload = {"portalId":"1","showDate":"26/05/2014","flag":0,"size":9}
    r = requests.post(URL, headers=PARAMS, data=json.dumps(payload))

    print(r.text)

    return json.loads(r.text)

ss = "Explore the different contribution of words and images to meaning in stories and informative texts."
res_srl = callAllenNlpApi("semantic-role-labeling", ss)

print(res_srl)
