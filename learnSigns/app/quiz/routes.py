from flask import Blueprint, render_template
from app.models import FlashcardSet
import json

quiz_bp = Blueprint("quiz", __name__, url_template_folder="templates", url_prefix="/quiz")

@quiz_bp.route("/int:set_id")
def quiz(set_id):
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    return render_template("quiz.html", set_id=set_id)