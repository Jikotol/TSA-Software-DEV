from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(hours=1) # starts counting when session is created apparaently

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100)) # num in string the max num of chrs
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email



@app.route("/")
def home():
    return render_template("index.html", content="hello")

@app.route("/login", methods=["POST", "GET"])
def login(): # send info using post request
    if request.method == "POST":
        session.permanent = True # makes it expire w/ the time thing
        user = request.form["nm"] 
        session["user"] = user
        print(users)
        found_user = users.query.filter_by(name=user).first()  # how to grab info from db, returns a users obj
        if found_user:
            session["email"] = found_user.email
        else: # user doesn't exist, so gotta make obj
            usr = users(user, "")
            db.session.add(usr) # kinda like staging area
            db.session.commit() # ALWAYS commit when make change to database


        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST": # email form was submitted
            email = request.form["email"] # email is the name in html
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session: # user alr entered in email and now getting from session to display
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# !!!!!!! Test out closing web browser clears session data! cant tset rn