from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from  utils import accountManager, dbManager
import urllib2, json

app = Flask(__name__)
f = open( "utils/key", 'r' )
app.secret_key = f.read();
f.close

#root, two behaviors:
#    if logged in: redirects you to your feed
#    if not logged in: displays log in/register page
@app.route("/")
def loginOrRegister():
    if 'username' in session:
        return redirect("/feed")
    else:
        return render_template("loginOrReg.html", username=True)

#handles input of the login register page
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
    print formDict
    if formDict["logOrReg"] == "login":
        username = formDict["username"]
        password = formDict["password"]
        loginStatus = "login failed"
        statusNum = accountManager.authenticate(username,password) #returns 0,1 or 2 for login status messate
        if statusNum == 0:
            loginStatus = "user does not exist"
        elif statusNum == 1:
            session["username"]=username
            loginStatus = username + " logged in"
            return redirect( "/feed" )
        elif statusNum == 2:
            loginStatus = "wrong password"

        return render_template("loginOrReg.html",status=loginStatus)

    elif formDict["logOrReg"] == "register":  #registering
        username = formDict["username"]
        password = formDict["password"]
        pwd = formDict["pwd"]  #confirm password
        registerStatus = "register failed"
        statusNum = accountManager.register(username,password,pwd) #returns true or false
        if statusNum == 0:
            registerStatus = "username taken"
        elif statusNum == 1:
            registerStatus = "passwords do not match"
        elif statusNum == 2:
            registerStatus = username +" account created"

        return render_template("loginOrReg.html",status=registerStatus) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
        return render_template("loginOrReg.html",status="logged out") 
    else:
        return redirect(url_for('loginOrRegister'))

@app.route("/testerino")
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

@app.route("/feed")
def feed():
    return "Works"

@app.route("/profile/")
@app.route("/profile/<username>")
def profile(username=None):
    if "username" not in session:
        return redirect(url_for("login"))

    if not username:
        username = session["username"]
    me = username == session["username"]
    
    # Invalid user
    abort(404)

@app.route("/stock")
def stock():
    return "Stocks"

if __name__ == "__main__":
    app.debug = True
    app.run()
