from flask import Blueprint, request, url_for, render_template, session, redirect, flash

from app.models import FlashcardSet, User
from .services import delete_cards

import json

sets_bp = Blueprint("sets", __name__, url_prefix="/sets", template_folder="templates")

@sets_bp.route("/edit/<int:set_id>", methods=["POST", "GET"])
def edit_set(set_id):
    """
    Updates the set's default settings, name, and flashcards

    set_id: int
    rtype: str - HTML string of "edit_set.html"
    """
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    if request.method == "POST":
        fc_set.default_front =  request.form.get("new-front")
        fc_set.default_back = request.form.get("new-back")
        fc_set.name = request.form.get("new-name")

        if request.form.get("flashcard-del-list"):
            delete_cards(json.loads(request.form.get("flashcard-del-list")))
        
        return redirect(url_for("sets.sets"))
        
    return render_template("sets/edit_set.html", fc_set=fc_set)


@sets_bp.route("/")
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
            return render_template("sets/sets.html", fc_sets=user.flashcard_sets)
        return render_template("sets/sets.html")
    else:
        flash("Please log in for study mode")
        return redirect(url_for("users.login"))


@sets_bp.route("/merge/<int:set_id_1>/<int:set_id_2>", methods=["POST", "GET"])
def merge_sets(set_id_1, set_id_2):

    fc_set1 = FlashcardSet.query.filter_by(_id=set_id_1).first()
    fc_set2 = FlashcardSet.query.filter_by(_id=set_id_2).first()

    return render_template("sets/merge_set.html", fc_set1=fc_set1, fc_set2=fc_set2)
