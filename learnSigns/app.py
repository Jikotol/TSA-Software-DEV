from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
from sqlalchemy.sql.expression import func
import utils
import os

app = Flask(__name__)
app.secret_key = "dev"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "sqlite:///" + os.path.join(app.root_path, "data", "sample.db")
)

app.permanent_session_lifetime = timedelta(hours=1) 

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    _id = db.Column("user_id", db.Integer, primary_key=True) # auto assigns id to each entry

    username = db.Column("username", db.String(100), nullable=False, unique=True)
    flashcard_sets = db.relationship("FlashcardSet", backref="user", cascade="all, delete-orphan")
    
    def __init__(self, username):
        self.username = username

class FlashcardSet(db.Model):
    __tablename__ = "flashcard_sets"
    _id = db.Column("set_id", db.Integer, primary_key=True)
    
    name = db.Column("set_name", db.String(100), nullable=False)
    default_front = db.Column("default_front", db.String(10), default="term", nullable=False)
    default_back = db.Column("default_back", db.String(10), default="visual", nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cards = db.relationship("Flashcard", backref="set", cascade="all, delete-orphan")

    def __init__(self, name, default_front, default_back, user_id):
        self.name = name
        self.default_front = default_front
        self.default_back = default_back
        self.user_id = user_id

class Flashcard(db.Model):
    __tablename__ = "flashcards"
    _id = db.Column("flashcard_id", db.Integer, primary_key=True)
   
    front = db.Column("front", db.String(10))
    back = db.Column("back", db.String(10))
    term = db.Column("term", db.String(200))

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_sets.set_id"))

    def __init__(self, front=None, back=None, term=None):
        self.front = front
        self.back = back
        self.term = term

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

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/vocab/<int:main_gloss_id>/<int:gloss_id>", methods=["POST", "GET"])
def vocab(main_gloss_id, gloss_id):
    main_gloss = MainGloss.query.filter_by(_id=main_gloss_id).first()
    # gloss = Gloss.query.filter_by(_id=gloss_id).first()
    return render_template("vocab.html", main_gloss=main_gloss)

@app.route("/api/vocab/<int:main_gloss_id>/<int:gloss_id>")
def variant_info(main_gloss_id, gloss_id):
    gloss = Gloss.query.filter_by(_id=gloss_id).first()
    hs_img_dict = {}

    for key, value in utils.get_hs_imgs(gloss).items():
        if value:
            hs_img_dict[key] = url_for("static", filename=value)
        else:
            hs_img_dict[key] = None

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
        "hs_videos": hs_img_dict
    }

@app.route("/create/configure/flashcards", methods=["POST", "GET"]) 
def configure():
    if request.method == "POST":
        gloss_id = request.form["gloss_id"]
        gloss = Gloss.query.filter_by(_id=gloss_id).first()
        main_gloss = request.form["main-gloss"]
        
        return render_template("configure.html", gloss=gloss, main_gloss=main_gloss)
    return "", 204
        
@app.route("/create/flashcards", methods=["POST", "GET"])        
def create():
    """
    Takes info from flashcard configure form, structures the data into objects and adds it to the database
    """
    if request.method == "POST":
        user = User.query.filter_by(_id=session["user_id"]).first()

        # Determine set
        if "new-set" in request.form:
            fc_set = FlashcardSet(
                name=request.form["set_name"],
                default_front=request.form["set-front"],
                default_back=request.form["set-back"],
                user_id=user._id
            )
            db.session.add(fc_set)  # <-- Add new set to session immediately
        else:
            fc_set = FlashcardSet.query.filter_by(_id=int(request.form["existing-set-id"])).first()

        # Create Flashcard object
        card = Flashcard(
            front=request.form.get("fc-front") if request.form["fc-front"] else fc_set.default_front,
            back=request.form.get("fc-back") if request.form["fc-back"] else fc_set.default_back,
            term=request.form["fc-term"]
        )

        card.gloss_id = request.form["gloss-id"]

        # Append card to the set's cards
        fc_set.cards.append(card)

        # Commit everything at once
        db.session.commit()

    if request.referrer != request.url:
        return redirect(url_for("browse"))
    return redirect(url_for("browse"))

@app.route("/study/<int:set_id>") 
def study(set_id):
    """
    Will have the render template thing for actually studying the flashcards
    """

    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()
    
    fc_set_json = {
        "name": fc_set.name,
        "default_front": fc_set.default_front,
        "default_back": fc_set.default_back,
    }

    # Sorts cards by id
    cards = sorted(fc_set.cards, key=lambda card: card._id)
    
    cards_json = []
    for card in cards:
        gloss = Gloss.query.filter_by(_id=card.gloss_id).first()

        cards_json.append({
            "id": card._id,
            "front": card.front,
            "back": card.back,
            "term": card.term,
            "visual": gloss.video.youtube_url,
            "credit": gloss.video.credit
        })

    return render_template("study.html", fc_set=fc_set_json, cards=cards_json)

@app.route("/sets")
def sets():
    if "user_id" in session:
        print(session)
        user = User.query.filter_by(_id=session["user_id"]).first()
        if user.flashcard_sets:
            return render_template("sets.html", fc_sets=user.flashcard_sets)
        return render_template("sets.html")
    else:
        return redirect(url_for("login"))

@app.context_processor
def inject_user():
    return dict(user=current_user())

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login(): # send info using post request
    if request.method == "POST" and request.form["nm"]:
        session.permanent = True # makes it expire w/ the time thing

        username = request.form["nm"]
        if not sign_in(username):
            add_user(username)
            sign_in(username)
        else:
            sign_in(username)

        return redirect(url_for("home"))
    if "username" in session:
        sign_in(session["username"])
        return render_template("home.html")
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"] 
    if "username" in session:
        del session["username"]
    return redirect(url_for("login"))

def sign_in(name):
    found_user = User.query.filter_by(username=name).first()
    if found_user:
        session["user_id"] = found_user._id
        session["username"] = found_user.username
    else:
        return False

def add_user(username):
    user = User(username)
    db.session.add(user)
    db.session.commit()

def current_user():
    if "user_id" in session:
        return User.query.filter_by(_id=session["user_id"]).first()
    return None

def clear_table(table):
    db.session.execute(delete(table))
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        """clear_table(Flashcard)
        clear_table(FlashcardSet)"""
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