import requests
import json

def lookup(keyword):
    search = json.dumps({
        "queryString": "%s" % (keyword,) ,
        "resultContext" : {
            "maxResults" : "1",
            "offset" : "0",
            "aspects" : ["title","summary","location"],
            "sortOrder" : "DESC",
            "sortField" : "initialPublishDateTime"
        }
    })
    r = requests.post("http://api.ft.com/content/search/v1?apiKey=rdf6mjwhqtnz7a5wvm45t3cs", headers={"Content-Type":"application/json"}, data = search)
    content = json.loads(r.text)

    if 'results' not in content["results"][0]:
        return "No articles found"

    resp = []
    for item in content["results"][0]["results"]:
        title =  item["title"]["title"].encode("utf-8")
        if 'excerpt' in item["summary"]:
            summary = item["summary"]["excerpt"].encode("utf-8")
        else:
            summary = "No summary available"
        url = item["location"]["uri"].encode("utf-8")
        info = [title, summary, url]
        resp.append(info)

    return resp

def latest(offset):
    search = json.dumps({
        "queryString": "" ,
        "resultContext" : {
            "maxResults" : "15",
            "offset" : "%s" % (str(offset),),
            "aspects" : ["title","summary","location"],
            "sortOrder" : "DESC",
            "sortField" : "initialPublishDateTime"
        }
    })
    
    r = requests.post("http://api.ft.com/content/search/v1?apiKey=rdf6mjwhqtnz7a5wvm45t3cs", headers={"Content-Type":"application/json"}, data = search)
    if r.text.encode("UTF-8") == "Unprocessable Entity":
        return "Nothing here"
    
    content = json.loads(r.text)

    resp = []
    print content
    for item in content["results"][0]["results"]:
        title =  item["title"]["title"].encode("utf-8")
        if 'excerpt' in item["summary"]:
            summary = item["summary"]["excerpt"].encode("utf-8")
        else:
            summary = "No summary available"
        url = item["location"]["uri"].encode("utf-8")
        info = [title, summary, url]
        resp.append(info)

    return resp

for item in lookup("abdsjfadf"):
    print item

