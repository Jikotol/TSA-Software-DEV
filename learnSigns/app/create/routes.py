from flask import Blueprint, request, render_template, session, redirect, url_for
from app.extensions import db

from app.models import Gloss, FlashcardSet, Flashcard

create_bp = Blueprint("create", __name__, url_prefix="/create", template_folder="templates")

@create_bp.route("/configure/flashcards", methods=["POST", "GET"]) 
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
        
        return render_template("create/configure.html", gloss=gloss, main_gloss=main_gloss)
    return "", 204
        
@create_bp.route("/flashcards", methods=["POST", "GET"])        
def create():
    """ 
    Takes info from flashcard configure form, structures the data into objects and adds it to the database 
    
    rtype: Response
    """

    if request.method == "POST":
        path_list = request.referrer.split("/")

        # Creates a new set 
        if "new-set" in request.form or "merge" in path_list:
            fc_set = FlashcardSet(
                name=request.form["set_name"],
                default_front=request.form["set-front"],
                default_back=request.form["set-back"],
                user_id=session["user_id"]
            )

            # Adds set to session 
            db.session.add(fc_set)
        else:
            # Gets pre-existing set
            fc_set = FlashcardSet.query.filter_by(_id=int(request.form["existing-set-id"])).first()
    
        if "merge" in path_list:

            fc_id_list = request.form["kept-card-list"].split(",")
            fc_id_list = [int(id) for id in fc_id_list]

            merged_set_id_list = request.form["kept-card-list"].split(",")
            merged_set_id_list = [int(id) for id in merged_set_id_list]

            cards = Flashcard.query.filter(
                Flashcard._id.in_(fc_id_list)).all()
            
            for card in cards:
                card.set_id = fc_set._id
            
            merged_sets = FlashcardSet.query.filter(
                FlashcardSet._id.in_(merged_set_id_list)).all()
            
            for fc_set in merged_sets:
                db.session.delete(fc_set)

        else:

            # Creates Flashcard object
            card = Flashcard(
                front=request.form.get("fc-front"),
                back=request.form.get("fc-back"),
                term=request.form["fc-term"],
                e_factor=12
            )
    
            card.gloss_id = request.form["gloss-id"]
    
            # Appends card to the set's cards
            fc_set.cards.append(card)

        # Commits all database changes
        db.session.commit()
    
    return redirect(url_for("sets.sets"))

@create_bp.route("/sets", methods=["POST", "GET"])
def wip():
    ...