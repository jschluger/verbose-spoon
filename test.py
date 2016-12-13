import requests

def test():
    search = {
        "queryString": "banks"
    }
    r = requests.post("http://api.ft.com/content/search/v1?apiKey=rdf6mjwhqtnz7a5wvm45t3cs", headers={"Content-Type":"application/json"}, data = search)
    return r.content

print test()
