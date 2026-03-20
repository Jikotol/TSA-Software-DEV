from .extensions import db

class User(db.Model):
    __tablename__ = "users"
    _id = db.Column("user_id", db.Integer, primary_key=True) # Auto assigns id to each entry

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
    e_factor = db.Column("e_factor", db.Integer) # Easiness factor for flashcard repetition

    gloss_id = db.Column(db.Integer, db.ForeignKey("glosses.gloss_id"), nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey("flashcard_sets.set_id"))

    def __init__(self, front=None, back=None, term=None, e_factor=12):
        self.front = front # Equal to either "visual", "term", or "default"
        self.back = back # Equal to either "visual", "term", or "default"
        self.term = term # The word the flashcard is about
        self.e_factor = e_factor

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