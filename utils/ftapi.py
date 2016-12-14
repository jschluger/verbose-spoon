import urllib2, json


f = open( "utils/ftkey", 'r' )
KEY = f.read();
f.close


def lookup(keyword):
    search = json.dumps({
        "queryString": "%s" % (keyword,) ,
        "resultContext" : {
            "maxResults" : "10",
            "offset" : "0",
            "aspects" : ["title","summary","location"],
            "sortOrder" : "DESC",
            "sortField" : "initialPublishDateTime"
        }
    })

    request = urllib2.Request("http://api.ft.com/content/search/v1?apiKey=" + key, data = search, headers={"Content-Type":"application/json"})
    r = urllib2.urlopen(request).read()
    content = json.loads(r)

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
    
   
    request = urllib2.Request("http://api.ft.com/content/search/v1?apiKey=" + key, data = search, headers={"Content-Type":"application/json"})
    try:
        r = urllib2.urlopen(request).read()
    except:
        return "No articles here"
    
    content = json.loads(r)
    #print content
    #if r.text.encode("UTF-8") == "Unprocessable Entity":
    #    return "Nothing here"

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
