from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from  utils import accountManager, dbManager, api, info
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

# Rodda testing charts, do not touch
@app.route('/chart/<string:symbol>')
@app.route('/chart')
def chart(symbol = 'AAPL'):
    data = api.get_chart(symbol)

    data_points = []

    for i in range(0, len(data['Positions'])):
        data_points.append({})
        data_points[i]['x'] = data['Positions'][i]
        data_points[i]['y'] = data['Elements'][0]['DataSeries']['close']['values'][i]

    return render_template('chart_test.html', data_points = data_points)

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

    
@app.route("/stock/<stocksymbol>")
def stock(stocksymbol=None):
    return render_template("stock.html", data=info.get_stock_info(stocksymbol))

@app.route("/myStocks")
def myStocks():
    if 'username' in session:
        u = session["username"]
        #stuff = dbManager.get_own_stocks(u,something else)
        return render_template("my.html",info=info.get_user_info(u))
    else:
        return redirect(url_for('loginOrRegister'))
    
@app.route("/buy")
def buy():
    if 'username' in session:
        u = session["username"]
        formDict = request.form
        sn = formDict["stockName"]
        s = int(formDict["shares"])
        p = int(formDict["price"])
        message = dbManager.buyStock(sn,s,p,u)
        if (notice == "you don't got enuf money, dude"):
            return redirect(url_for('stock',note=message))
            
        return redirect(url_for('myStocks'))
        
@app.route("/sell")
def sell():
    if 'username' in session:
        u = session["username"]
        formDict = request.form
        sn = formDict["stockName"]
        s = int(formDict["shares"])
        p = int(formDict["price"])
        message = dbManager.sellStock(sn,s,p,u)
        if (notice == "you do not have enough shares of this stock to make this transaction"):
            return redirect(url_for('stock',note=message))
            
        return redirect(url_for('myStocks'))
        

    
if __name__ == "__main__":
    app.debug = True
    app.run()
