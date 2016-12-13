import requests
import json

def test():
    search = json.dumps({
        "queryString": "banks",
        "resultContext" : {
            "aspects" : [ "title"]
        }
    })
    r = requests.post("http://api.ft.com/content/search/v1?apiKey=rdf6mjwhqtnz7a5wvm45t3cs", headers={"Content-Type":"application/json"}, data = search)
    content = json.loads(r.text)
    return content["results"][0]

print test()
