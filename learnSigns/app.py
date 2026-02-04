from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import utils
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
    flashcard_sets = db.relationship("FlashcardSet", backref="flashcard_sets")
    
    def __init__(self, username):
        self.username = username

class FlashcardSet(db.Model):
    __tablename__ = "flashcard_sets"
    _id = db.Column("set_id", db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cards = db.relationship("Flashcard", backref="flashcard")

class Flashcard(db.Model):
    __tablename__ = "flashcard"
    _id = db.Column("flashcard_id", db.Integer, primary_key=True)

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))
    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_sets.set_id"))

class MainGloss(db.Model):
    __tablename__ = "main_glosses"
    _id = db.Column("main_id", db.Integer, primary_key=True)

    main_gloss = db.Column("main_gloss", db.String(100), nullable=False)
    head_gloss_id = db.Column("head_gloss_id", db.String(100), nullable=False)

    glosses = db.relationship("Gloss", backref="glosses")

class Gloss(db.Model):
    __tablename__ = "glosses"
    _id = db.Column("gloss_id", db.Integer, primary_key=True)

    asl_gloss = db.Column("asl_gloss", db.String(200), nullable=False)
    display_name = db.Column("display_name", db.String(200))
    notes = db.Column("notes", db.String(200))

    main_id = db.Column(db.Integer, db.ForeignKey('main_glosses.main_id'))
    
    video = db.relationship("Video", backref="gloss", uselist=False, foreign_keys="[Video.gloss_id]")
    handshape = db.relationship("Handshape", backref="handshapes", uselist=False)
    component = db.relationship("Components", backref="components", uselist=False)

class Handshape(db.Model):
    __tablename__ = "handshapes"
    _id = db.Column("handshape_id", db.Integer, primary_key=True)

    dom_start = db.Column("dom_start", db.String(100))
    dom_end = db.Column("dom_end", db.String(100))
    non_dom_start = db.Column("non_dom_start", db.String(100))
    non_dom_end = db.Column("non_dom_end", db.String(100))

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))

class Components(db.Model):
    __tablename__ = "components"
    _id = db.Column("components_id", db.Integer, primary_key=True)

    word1 = db.Column("word1", db.String(100), nullable=False)
    word2 = db.Column("word2", db.String(100), nullable=False)
    word3 = db.Column("word3", db.String(100))

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))

class Video(db.Model):
    __tablename__ = "videos"
    _id = db.Column("video_id", db.Integer, primary_key=True)
    youtube_url = db.Column("youtube_url", db.String(300), nullable=False)
    credit = db.Column("credit", db.String(100), nullable=False)
    
    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"))

@app.route("/browse")
def browse():
    random_main_head_tuples = []
    used_ids = set()

    while len(random_main_head_tuples) < 6:
        main_gloss = utils.get_random_row(MainGloss)

        if main_gloss._id in used_ids:
            continue

        used_ids.add(main_gloss._id)

        head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()
        random_main_head_tuples.append((main_gloss, head_gloss))
    
    return render_template("browse.html", main_head_tuples=random_main_head_tuples)

@app.route("/")
@app.route("/home")
def home():
    return render_template("base.html")

@app.route("/vocab/<int:main_gloss_id>/<int:gloss_id>")
def vocab(main_gloss_id, gloss_id):
    main_gloss = MainGloss.query.filter_by(_id=main_gloss_id).first()
    # gloss = Gloss.query.filter_by(_id=gloss_id).first()
    return render_template("vocab.html", main_gloss=main_gloss)

@app.route("/api/vocab/<int:main_gloss_id>/<int:gloss_id>")
def variant_info(main_gloss_id, gloss_id):
    gloss = Gloss.query.filter_by(_id=gloss_id).first()
    hs_img_dict = utils.get_hs_imgs(gloss)
    print(utils.get_hs_imgs(gloss))
    return {
        "asl_gloss": gloss.asl_gloss,
        "display_name": gloss.display_name,
        "youtube_url": gloss.video.youtube_url,
        "credit": gloss.video.credit,
        "handshapes": {
            "dom_start": gloss.handshape.dom_start,
            "dom_end": gloss.handshape.dom_end,
            "non_dom_start": gloss.handshape.non_dom_start,
            "non_dom_end": gloss.handshape.non_dom_end
        },
        "hs_videos": utils.get_hs_imgs(gloss)
    }

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)

def make_flashcard(gloss):
    ...




"""
GET data when 
page loads or when render template

SEND data when 
user clicks/submits/interacts

youoouoasd

MainGloss.query.filter_by(_id="12").first()

"""