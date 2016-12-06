from flask import Flask, render_template
import urllib2, json

app = Flask(__name__)


def validate_form(form, required_keys):
    """ Check if a dictionary contains all the required keys """
    return set(required_keys) <= set(form)

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

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # User has submitted a request to register an account
        required_keys = ["username", "pass", "passconfirm", "bday"]
        if not validate_form(request.form, required_keys):
            return render_template("register.html", message="Malformed request.", category="danger")

        username = request.form["username"]
        password = request.form["pass"]
        password_confirm = request.form["passconfirm"]
        bday = request.form["bday"]

        if not username.isalnum():
            return render_template("register.html", message="Usernames must contain only alphanumeric characters.", category="danger")

        if password != password_confirm:
            return render_template("register.html", message="Passwords do not match.", category="danger")

        if len(password) < 6:
            return render_template("register.html", message="Password must be at least 6 characters in length.", category="danger")

        if password == password.lower():
            return render_template("register.html", message="Password must contain at least one capitalized letter.", category="danger")

        if user.get_user(username=username):
            return render_template("register.html", message="Username is already in use.", category="danger")

        user.add_user(username, password)

        return render_template("register.html", message="Account created!", category="success")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # User has submitted a request to login
        required_keys = ["username", "pass"]
        if not validate_form(request.form, required_keys):
            return render_template("login.html", message="Malformed request.", category="danger")

        username = request.form["username"]
        password = hashlib.sha1(request.form["pass"]).hexdigest()

        result = user.get_user(username=username)
        if result:
            if result[2] == password:
                session["username"] = username
                return redirect(url_for("profile"))
            return render_template("login.html", message="Invalid password", category="danger")
        return render_template("login.html", message="Username does not exist...", add_mess="Register a new account?", category="danger")
    return render_template("login.html")

def logout():
    session.clear()
    return redirect(url_for("root"))

if __name__ == "__main__":
    app.debug = True
    app.run()
    
