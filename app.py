from flask import Flask, render_template
import urllib2, json

app = Flask(__name__)


@app.route("/")
def root():
    u = urllib2.urlopen("https://api.nasa.gov/planetary/apod?api_key=z5OCLcXbxVpm5pJfALskk1aCWeBKRsNiFv8N1YYp")
    response = u.read()
    data = json.loads( response )
    return render_template("index.html", pic = data['url'] )

@app.route("/testing")
def test():
    u = urllib2.urlopen("http://api.ft.com/site/v1/pages?apiKey=rdf6mjwhqtnz7a5wvm45t3cs")
    response = u.read()
    data = json.loads( response )
    return render_template("test.html", info = data )


if __name__ == "__main__":
    app.debug = True
    app.run()
    
