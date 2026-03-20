from flask import Blueprint, render_template

from app.models import MainGloss, Gloss
from .services import get_related_glosses

vocab_bp = Blueprint("vocab", __name__, url_prefix="/vocab", template_folder="templates")


@vocab_bp.route("/list", methods=["POST", "GET"])
def vocab_list():
    """
    Creates a list of all glosses, categorizing them on the letter they start with

    rtype: str - JSON string containing main gloss and id
    """
    
    return render_template("vocab/vocab_list.html")


@vocab_bp.route("/<int:main_gloss_id>/<int:gloss_id>", methods=["POST", "GET"])
def vocab(main_gloss_id, gloss_id):
    """ 
    Returns and organizes the needed data for "vocab.html " and renders the template
    
    main_gloss_id: int
    gloss_id: int

    rtype: str - HTML string for "vocab.html"
    """
    main_gloss = MainGloss.query.filter_by(_id=main_gloss_id).first()

    if gloss_id < 0:
        gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()
    gloss = Gloss.query.filter_by(_id=gloss_id).first()

    related_glosses = get_related_glosses(main_gloss)

    return render_template("vocab/vocab.html", main_gloss=main_gloss, gloss=gloss, related_glosses=related_glosses)
