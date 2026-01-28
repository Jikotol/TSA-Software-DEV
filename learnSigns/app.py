from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "dev"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "sqlite:///" + os.path.join(app.root_path, "data", "sample.db")
)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    _id = db.Column("user_id", db.Integer, primary_key=True) # auto assigns id to each entry

    username = db.Column("username", db.String(100), nullable=False, unique=True)
    
    def __init__(self, username):
        self.username = username

class FlashcardSet(db.Model):
    __tablename__ = "flashcard_sets"
    _id = db.Column("set_id", db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", backref="flashcard_sets")

class Flashcard(db.Model):
    __tablename__ = "flashcard"
    _id = db.Column("flashcard_id", db.Integer, primary_key=True)

    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_sets.set_id"))
    set = db.relationship("FlashcardSet", backref="flashcards")

class MainGloss(db.Model):
    __tablename__ = "main_glosses"
    _id = db.Column("main_id", db.Integer, primary_key=True)

    main_gloss = db.Column("main_gloss", db.String(100), nullable=False)
    head_gloss_id = db.Column("head_gloss_id", db.String(100), nullable=False)

class Gloss(db.Model):
    __tablename__ = "glosses"
    _id = db.Column("gloss_id", db.Integer, primary_key=True)

    main_gloss_id = db.Column(db.Integer, db.ForeignKey("main_glosses.main_id"))
    main_gloss = db.relationship("MainGloss", backref="glosses")

class Handshapes(db.Model):
    __tablename__ = "handshapes"
    _id = db.Column("handshape_id", db.Integer, primary_key=True)

    dom_start = db.Column("dom_start", db.String(100))
    dom_end = db.Column("dom_end", db.String(100))
    non_dom_start = db.Column("non_dom_start", db.String(100))
    non_dom_end = db.Column("non_dom_end", db.String(100))

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))
    gloss = db.relationship("Gloss", backref="handshapes", uselist=False)

class Components(db.Model):
    __tablename__ = "components"
    _id = db.Column("components_id", db.Integer, primary_key=True)

    word1 = db.Column("word1", db.String(100), nullable=False)
    word2 = db.Column("word2", db.String(100), nullable=False)
    word3 = db.Column("word3", db.String(100))

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))
    gloss = db.relationship("Gloss", backref="components", uselist=False)

@app.route("/study")
def study():
    return render_template("study.html")

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/vocab/<int:gloss_id>")
def vocab():
    # 
    return render_template("vocab.html")

if __name__ == "__main__":
    with app.app_context():
        db.session.add(User(username="youoouoasd"))
        db.session.commit()
    # app.run(debug=True)

"""
GET data when 
page loads or when render template

SEND data when 
user clicks/submits/interacts
"""