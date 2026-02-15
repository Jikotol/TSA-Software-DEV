from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, or_
from sqlalchemy.sql.expression import func
import utils
import os
import json
import string

app = Flask(__name__)
app.secret_key = "dev"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "sqlite:///" + os.path.join(app.root_path, "data", "full.db")
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
        self.default_front = default_front # Equal to either "visual" or "term"
        self.default_back = default_back # Equal to either "visual" or "term"
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
        self.front = front # Equal to either "visual", "term", or "default"
        self.back = back # Equal to either "visual", "term", or "default"
        self.term = term # The word the flashcard is about

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
    components = db.relationship("Components", backref="components", uselist=False)

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


def get_main_head_tuples():
    """
    Randomly gets and formats main gloss objects and their head gloss objects for video browsing in home page
    """
    random_main_head_tuples = []
    used_ids = set()

    while len(random_main_head_tuples) < 6:
        main_gloss = utils.get_random_row(MainGloss)

        # Filters out duplicateds
        if main_gloss._id in used_ids:
            continue

        used_ids.add(main_gloss._id)

        head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()
        random_main_head_tuples.append((main_gloss, head_gloss))
    
    return random_main_head_tuples

@app.route("/home", methods=["POST", "GET"])
def home():
    """ Handles home.html rendering and handles redirections from the search bar """
    # Search bar results
    if request.method == "POST":
        search = request.form["search"]

        # Searches with heuristics in order to find the gloss they want
        main_gloss_list = find_main_gloss(search)

        if len(main_gloss_list) == 1:
            # Redirects user straight tothe vocab page
            main_gloss = main_gloss_list[0]
            return redirect(url_for("vocab", main_gloss_id=main_gloss._id, gloss_id=main_gloss.head_gloss_id))

        elif main_gloss_list:
            # Redirects user to search selection page
            return render_template("search_results.html", search=search, main_gloss_results=main_gloss_list)

        else:
            return render_template(
                "error.html", 
                title="Search not found", 
                msg=f"No results for \"{request.form["search"]}\""
            )

    # Gets random main glosses their head glosses for video browsing on homepage
    main_head_tuples = get_main_head_tuples()

    return render_template("home.html", main_head_tuples=main_head_tuples)

def find_main_gloss(search):
    """
    Returns all possible main_glosses that match the users search

    search: str
    rtype: list(MainGloss)
    """
    # Finds the main_gloss the user was searching for based on heuristics

    search = search.upper()

    # Gets exact matches
    main_gloss_list = MainGloss.query.filter_by(main_gloss=search).all()

    # Gets glosses with search as a substring
    main_gloss_list = main_gloss_list + search_main_glosses(search, limit=20) 
    
    # Gets glosses if they use the search as a component
    main_gloss_list = main_gloss_list + search_components(search, limit=20)

    # Returns none if search cannot be split
    if "-" not in search or " " not in search or len(main_gloss_list) > 20:
        main_gloss_list = remove_duplicates_obj_list(main_gloss_list)
        return main_gloss_list

    # Separates the user's search and checks the parts separately
    for sep in ["-", " "]:
        if sep in search:
            parts = search.split(sep)
        else:
            continue
        for part in parts:
            part = part.strip()

            # Gets glosses that start with the part
            main_gloss = search_main_glosses(f"%{part}")
            if main_gloss:
                main_gloss_list.append(main_gloss[0])

            # Gets glosses that have the part at all
            main_gloss = search_main_glosses(f"%{part}%")
            if main_gloss:
                main_gloss_list.append(main_gloss[0])
    
    main_gloss_list = remove_duplicates_obj_list(main_gloss_list)

    return main_gloss_list

def remove_duplicates_obj_list(obj_list):
    """ Removes duplicates from a list with custom db models """
    # Creates a dict list with ids as keys for unique values, removing duplicate objects
    # then retrieves the original objects with .values()
    return list({obj._id: obj for obj in obj_list}.values())

@app.route("/api/search/<string:search_term>")
def get_suggestions(search_term):
    """ 
    Returns the list of glosses for the search bar search suggestions 
    
    search_term: str
    rtype: str - JSON string with list of main gloss names
    """
    suggestionsList = search_main_glosses(f"{search_term}%", limit=10)
    
    return json.dumps([main_gloss.main_gloss.title() for main_gloss in suggestionsList])

def search_main_glosses(search_pattern, limit=20):
    """ 
    Returns a list of MainGloss objects that match the search pattern 
    
    search_pattern: str
    rtype: list() | list(MainGloss)
    """
    main_glosses = (
        db.session.query(MainGloss)
        .filter(MainGloss.main_gloss.ilike(search_pattern))
        .limit(limit)
        .all()
    )

    return main_glosses

def get_main_gloss_from_notes(search_pattern, limit=20):
    """
    Returns a list of Main Gloss object that have a search in the glosses notes

    search_pattern: str
    limit: int
    rtype: list() | list(MainGloss)
    """
    return (
        db.session.query(MainGloss)
        .distinct()
        .join(MainGloss.glosses) # Temporarily merges tables
        .filter(Gloss.notes.ilike(search_pattern)) 
        .limit(limit)
        .all()
    )

def search_components(search, limit=20):
    """ 
    Searches gloss components for the search term 
    
    search: str
    limit: int
    rtype: list() | list(MainGloss)
    """

    #
    search = fr"(^|\+){search}(\+|$)"

    return (
        db.session.query(MainGloss) # To return gloss objects
        .distinct()
        .join(MainGloss.glosses)
        .join(Gloss.components) # Combines current and components table to filter
        .filter(
            or_(
                Components.word1.op("REGEXP")(search),
                Components.word2.op("REGEXP")(search),
                Components.word3.op("REGEXP")(search)
            )   
        )
        .limit(limit)
        .all()
    )

@app.route("/vocab/<int:main_gloss_id>/<int:gloss_id>", methods=["POST", "GET"])
def vocab(main_gloss_id, gloss_id):
    """ 
    Returns and renders the base for vocab.html 
    
    main_gloss_id: int
    gloss_id: int

    rtype: str - HTML string for "vocab.html"
    """
    main_gloss = MainGloss.query.filter_by(_id=main_gloss_id).first()
    gloss = Gloss.query.filter_by(_id=gloss_id).first()

    related_glosses = get_related_glosses(main_gloss)

    return render_template("vocab.html", main_gloss=main_gloss, gloss=gloss, related_glosses=related_glosses)

def get_related_glosses(main_gloss):
    """
    Returns related glosses by matching gloss notes and compenents, used to link vocab pages

    main_gloss: MainGloss
    """

    head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()

    sim_notes_list = []

    if head_gloss.notes:
        group = head_gloss.notes
        if ";" in head_gloss.notes:
            group = head_gloss.notes.split(";")[0]

        sim_notes_list = get_main_gloss_from_notes(search_pattern=f"%{group}%", limit=6)
    
    appears_in_list = search_components(search=head_gloss.asl_gloss, limit=12)

    return {
        "same_notes_main_glosses": sim_notes_list,
        "appears_in_main_glosses": appears_in_list
    }



@app.route("/api/vocab/<int:main_gloss_id>/<int:gloss_id>")
def variant_info(main_gloss_id, gloss_id):
    """
    Returns the info of a gloss in a dict which will be turned into a JSON for frontend. Sends info to vocab page which
    shows the glosses info.

    main_gloss_id: int
    gloss_id: int
    """
    gloss = Gloss.query.filter_by(_id=gloss_id).first()
    hs_img_dict = {}

    # Adds the correct path to the image file, get_hs_imgs only returns img name with folder path, e.g images/handshapes/4_handshape_img.gif
    for key, value in utils.get_hs_imgs(gloss, add_images_path=True).items():
        if value:
            hs_img_dict[key] = url_for("static", filename=value)
        else:
            hs_img_dict[key] = None

    # Inserts gloss info into dict for JSON conversion
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
    """ 
    Renders configure HTML which allows users to create a flashcard and add it to a new or pre-existing set 
    
    rtype: str - HTML string for "configure.html" | None
    """

    # Gets info from vocab page form
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
    
    rtype: Response
    """

    if request.method == "POST":
        user = User.query.filter_by(_id=session["user_id"]).first()

        # Creates a new set 
        if "new-set" in request.form:
            fc_set = FlashcardSet(
                name=request.form["set_name"],
                default_front=request.form["set-front"],
                default_back=request.form["set-back"],
                user_id=user._id
            )

            # Adds set to session 
            db.session.add(fc_set)
        else:
            # Gets pre-existing set
            fc_set = FlashcardSet.query.filter_by(_id=int(request.form["existing-set-id"])).first()

        # Creates Flashcard object
        card = Flashcard(
            front=request.form.get("fc-front"),
            back=request.form.get("fc-back"),
            term=request.form["fc-term"]
        )

        card.gloss_id = request.form["gloss-id"]

        # Appends card to the set's cards
        fc_set.cards.append(card)

        # Commits all database changes
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/study/<int:set_id>") 
def study(set_id):
    """
    Renders the study template
    
    set_id: int
    rtype: str - HTML string for "study.html"
    """
    return render_template("study.html")

@app.route("/api/study/<int:set_id>") 
def card_data(set_id):
    """ 
    Prepares the data for studying with flashcards to be converted into JSON.

    set_id: int
    rtype: str - JSON string containing cards and set info
    """

    print("HELLO")

    # Gets the flashcard set object
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    # Sorts cards by id, least to greatest
    cards = sorted(fc_set.cards, key=lambda card: card._id)
    
    # Creates a list of dicts with flashcard data inside
    cards_json = []
    for card in cards:
        gloss = Gloss.query.filter_by(_id=card.gloss_id).first()

        cards_json.append({
            "id": card._id,
            "front": card.front if card.front != "default" else fc_set.default_front,
            "back": card.back if card.back != "default" else fc_set.default_back,
            "term": card.term,
            "visual": gloss.video.youtube_url,
            "credit": gloss.video.credit
        })

    return json.dumps({
        "set_name": fc_set.name,
        "cards": cards_json
    })

@app.route("/partials/flashcard")
def flashcard_partial():
    """ 
    Contains the HTML for flipping and going through flashcards 
    
    rtype: str - HTML string of "_flashcard.html"
    """
    return render_template("partials/_flashcard.html")

@app.route("/api/sets/<int:set_id>")
def get_set_info(set_id):
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    fc_set_json = {
        "name": fc_set.name,
        "flashcard_ids": [card._id for card in fc_set.cards], # List of card ids
        "default_front": fc_set.default_front,
        "default_back": fc_set.default_back
    }
     
    return json.dumps(fc_set_json)



@app.route("/api/sets/delete/<int:set_id>")
def delete_set(set_id):
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    if fc_set:
        db.session.delete(fc_set)
        db.session.commit()

@app.route("/sets")
def sets():
    """
    Renders the "sets" template and injects the flashcard sets the user has.

    If the user is not signed in, it redirects them to the login page.

    rtype: str - HTML string for "sets.html" | Response
    """
    if "user_id" in session:

        # Gets user object
        user = User.query.filter_by(_id=session["user_id"]).first()

        if user.flashcard_sets:
            return render_template("sets.html", fc_sets=user.flashcard_sets)
        return render_template("sets.html")
    else:
        return redirect(url_for("login"))

@app.route("/vocab-list")
def generate_vocab_list():
    """
    Creates a list of all glosses, categorizing them on the letter they start with

    rtype: str - JSON string containing main gloss and id
    """

    for letter in [""]:

@app.context_processor
def inject_user():
    """ 
    Creates global user variable containing the user object 
    
    Returns a dict, but in templates, Jinja uses it as variable "user" with a User object

    rtype: dict
    """
    return dict(user=current_user())

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Renders "login" template and handles account creation and user sign in
    """

    if request.method == "POST" and request.form["nm"]:
        # Makes the current session continue after the browser is closed, keeping users signed in
        session.permanent = True

        username = request.form["nm"]

        # Creates a new account for user under the given username if the account does not exist
        if not sign_in(username):
            add_user(username)
            sign_in(username)
        else:
            # Signs in user if account is found
            sign_in(username)

        # Brings user to home page
        return redirect(url_for("home"))

    # Makes sure session is updated correctly and redirects signed in user away from login page
    if "username" in session:
        sign_in(session["username"])
        return redirect(url_for("home"))

    # Renders "login.html" for users to sign in
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    """ 
    Logs current user out by updating session data 
    
    rtype: Response 
    """
    # Updates session variables relating to user
    if "user_id" in session:
        del session["user_id"] 
    if "username" in session:
        del session["username"]
    
    # Redirects user to "login.html" for logging in 
    return redirect(url_for("login"))

def sign_in(name):
    """
    Updates session variables to sign the user in

    rtype: None | False
    """
    # Gets user object associated with given username
    found_user = User.query.filter_by(username=name).first()

    # Signs in user by updating session variables
    if found_user:
        session["user_id"] = found_user._id
        session["username"] = found_user.username
    else:
        return False

def add_user(username):
    """ Adds new user to the database """
    user = User(username)
    db.session.add(user)
    db.session.commit()

def current_user():
    """ 
    Returns the current user's User object 
    
    rtype: User | None
    """
    if "user_id" in session:
        return User.query.filter_by(_id=session["user_id"]).first()
    return None

def clear_table(table):
    """ Clears the given table of any values """
    db.session.execute(delete(table))
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        """clear_table(Flashcard)
        clear_table(FlashcardSet)"""
        app.run(debug=True)