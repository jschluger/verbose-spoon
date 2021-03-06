from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
import os
import utils
from  utils import accountManager, dbManager, api, info, ftapi
import urllib2, json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

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
        return redirect("/profile")
    else:
        return render_template("loginOrReg.html", username=True, message=False)

# Rodda testing charts, do not touch
@app.route('/chart/<string:symbol>')
@app.route('/chart')
@app.route('/chart/<string:symbol>/<int:days>')
def chart(symbol = 'AAPL', days = 365):
    data = api.get_chart(symbol, number_of_days = days)

    data_points = []

    for i in range(0, len(data['Positions'])):
        data_points.append({})
        data_points[i]['x'] = data['Dates'][i]
        data_points[i]['y'] = data['Elements'][0]['DataSeries']['close']['values'][i]

    return render_template('chart_test.html', data_points = data_points, data = data, symbol = symbol, days = days)

#handles input of the login register page
@app.route("/authOrCreate", methods=["POST"])
def authOrCreate():
    formDict = request.form
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
            return redirect( "/profile" )
        elif statusNum == 2:
            loginStatus = "wrong password"

        return render_template("loginOrReg.html",status=loginStatus, message=True)

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

        return render_template("loginOrReg.html",status=registerStatus, message=True) #status is the login/creation messate 
    else:
        return redirect(url_for("loginOrReg"))

#logout of user
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "username" in session:
        session.pop('username')
    return redirect(url_for('loginOrRegister'))

@app.route("/feed")
def feed():
    if 'username' in session:
        articles = ftapi.latest(0)
        funds = info.getFunds( session['username'] )
        return render_template("feed.html", articles = articles, funds = funds)
    else:
        return redirect( url_for('loginOrRegister') )

    
@app.route("/stock/<stocksymbol>")
@app.route("/stock/<stocksymbol>/<int:days>")
@app.route("/stock/<stocksymbol>/<int:days>/<note>")
def stock(stocksymbol=None, days = 14, note=""):
    if 'username' in session:
        message = 0 #no error

        # chart stuff
        data_points = 0
        data = 0
        try:
            data = api.get_chart(stocksymbol, number_of_days = days)

            data_points = []
        
            for i in range(0, len(data['Positions'])):
                data_points.append({})
                data_points[i]['x'] = data['Dates'][i]
                data_points[i]['y'] = data['Elements'][0]['DataSeries']['close']['values'][i]
        except:
            message = 1 # chart error
            
        #non chart stuff
        stockInfo = 0
        try:
            stockInfo = info.get_stock_info(stocksymbol, username=session['username'])
        except:
            message = 2 # info error
            
        

        funds = info.getFunds( session['username'] )

        print "MSDFSDAGFADSFSDA"
        print note

        articles = ftapi.lookup(stockInfo[1])
        return render_template("stock.html", data=stockInfo, data_points = data_points, d = data, symbol = stocksymbol, days = days, msg=message, funds = funds, note=note, articles=articles )
    else:
        return redirect("/")
            


@app.route("/myStocks", methods=["GET","POST"])
def myStocks():
    if 'username' in session:
        u = session["username"]
        tlist = info.get_user_stocks(u)
        funds = info.getFunds( u )
        return render_template("my.html",info = tlist, funds = funds)
    else:
        return redirect(url_for('loginOrRegister'))
    
@app.route("/buy", methods=["POST"])
def buy():
    if 'username' in session:
        u = session["username"]
        formDict = request.form
        sn = formDict["stockName"]
        s = formDict["shares"]
        p = float(formDict["price"])
        status = dbManager.buyStock(sn,s,p,u)
        if (status == 1):
            note = "You do not have sufficent funds to complete this transaction"
            return redirect(url_for('stock',note=note, stocksymbol=formDict["stockSymbol"], days=formDict["days"]))
        if (status == 0):
            note = "Please input a positive integer value for number of shares"
            return redirect(url_for('stock',note=note, stocksymbol=formDict["stockSymbol"], days=formDict["days"]))
        
        return redirect(url_for('myStocks'))
        
@app.route("/sell", methods=["POST"])
def sell():
    if 'username' in session:
        u = session["username"]
        formDict = request.form
        sn = formDict["stockName"]
        s = formDict["shares"]
        p = float(formDict["price"])
        status = dbManager.sellStock(sn,s,p,u)
        if (status == 1):
            print "GFDSGDSGDFSG"
            note = "You do not have sufficent shares to make this transaction"
            return redirect(url_for('stock',note=note, stocksymbol=formDict["stockSymbol"], days=formDict["days"]))
        if (status == 0):
            note = "Please input a positive integer value for number of shares"
            return redirect(url_for('stock',note=note, stocksymbol=formDict["stockSymbol"], days=formDict["days"]))
            
        return redirect(url_for('myStocks'))

@app.route("/results", methods=["POST"])
def results():
    if 'username' in session:
        flag = 0 # no error

        querry = 0
        dictOfDicts = 0
        try:
            formDict = request.form
            querry = formDict["search"]
            dictOfDicts = info.search_results(querry)
            if dictOfDicts == -1:
                flag = 2
        except:
            flag = 1 # error
        funds = info.getFunds( session['username'] )
        
        return render_template("results.html", results = dictOfDicts, search = querry, funds = funds, flag = flag)
    else:
        return redirect( "/" )

        
@app.route("/profile", methods=["POST","GET"])
def profile():
    if 'username' in session:
        u = session["username"]
        profileStuff = info.get_user_info(u)
        funds = info.getFunds( u )
        if (request.method == "POST"):
            return render_template('edit_profile.html', funds = funds)
        if (request.method == "GET"):
            return render_template("profile.html", facts = profileStuff, funds = funds)
    else:
        return redirect("/")

    
@app.route("/edit_profile", methods=["POST","GET"])
def edit_profile():
    if 'username' in session:
        u = session["username"]
        funds = info.getFunds( u )
        if (request.method == "POST"):
            formDict = request.form
            dob = formDict["dob"]
            accountManager.updateDob(u,dob)
            favStock = formDict["favStock"]
            accountManager.updateFav(u,favStock)
            print ' doing the updating'
            fullName = formDict["fullName"]
            accountManager.updateFullName(u,fullName)        
            profileStuff = info.get_user_info(u)
            return redirect(url_for('profile',facts=profileStuff, funds = funds))
        else:
            return render_template("edit_profile.html", funds = funds)
    else:
        return redirect("/")
    
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

    
if __name__ == "__main__":
    app.debug = True
    app.run()
