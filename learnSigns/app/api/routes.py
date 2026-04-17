from flask import url_for, Blueprint, render_template
import json

from app.extensions import db
from app.models import Gloss, Video, MainGloss, FlashcardSet
from app import utils
from app.home.services import search_main_glosses

from app.display import display_bp

api_bp = Blueprint("api", __name__, url_prefix="/api", template_folder="templates")

#-------------- Vocab --------------
@api_bp.route("/vocab/<int:main_gloss_id>/<int:gloss_id>")
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
            hs_img_dict[key] = url_for("display.static", filename=value)
        else:
            hs_img_dict[key] = None

    video = Video.query.filter_by(gloss_id=gloss._id).first()

    # Inserts gloss info into dict for JSON conversion
    return {
        "asl_gloss": gloss.asl_gloss,
        "display_name": gloss.display_name,
        "youtube_url": video.youtube_url if video else None,
        "credit": video.credit if video else None,
        "handshapes": {
            "dom_start": gloss.handshape.dom_start,
            "dom_end": gloss.handshape.dom_end,
            "non_dom_start": gloss.handshape.non_dom_start,
            "non_dom_end": gloss.handshape.non_dom_end
        },
        "hs_imgs": hs_img_dict
    }

#-------------- Home --------------
@api_bp.route("/search/<string:search_term>")
def get_suggestions(search_term):
    """
    Returns the list of glosses for the search bar search suggestions 
    
    search_term: str
    rtype: str - JSON string with list of main gloss names"""
    
    suggestionsList = search_main_glosses(f"{search_term}%", limit=10)
    
    return json.dumps([main_gloss.main_gloss.title() for main_gloss in suggestionsList])


@api_bp.route("/vocab_list/<string:letter>", methods=["POST", "GET"])
def get_letter_glosses(letter):

    glosses_list = []
    
    search_pattern = letter + "%"

        # Gets all glosses that start with letter
    glosses_list = (
        db.session.query(MainGloss._id, MainGloss.head_gloss_id, MainGloss.main_gloss)
        .filter(MainGloss.main_gloss.ilike(search_pattern))
        .all()
    )

    glosses_list = [list(g) for g in glosses_list]

    return json.dumps(glosses_list)

#------------ Display ----------------

@api_bp.route("/partials/flashcard")
def flashcard_partial():
    print("H")
    """ 
    Contains the HTML for flipping and going through flashcards 
    
    rtype: str - HTML string of "_flashcard.html"
    """

    return render_template("partials/_flashcard.html")

#------------ Study ----------------

@api_bp.route("/study/<int:set_id>") 
def card_data(set_id):
    """ 
    Prepares the data for studying with flashcards to be converted into JSON.

    set_id: int
    rtype: str - JSON string containing cards and set info
    """

    # Gets the flashcard set object
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    # Sorts cards by id, least to greatest
    cards = sorted(fc_set.cards, key=lambda card: card._id)
    
    # Creates a list of dicts with flashcard data inside
    cards_json = []
    for card in cards:
        gloss = Gloss.query.filter_by(_id=card.gloss_id).first()

        video = Video.query.filter_by(gloss_id=card.gloss_id).first()

        cards_json.append({
            "id": card._id,
            "front": card.front if card.front != "default" else fc_set.default_front,
            "back": card.back if card.back != "default" else fc_set.default_back,
            "term": card.term,
            "eFactor": card.e_factor,
            "visual": video.youtube_url if video else None,
            "credit": video.credit if video else None
        })

    return json.dumps({
        "set_name": fc_set.name,
        "cards": cards_json
    })

#------------ Sets ----------------

@api_bp.route("/sets/<int:set_id>")
def get_set_info(set_id):
    """
    Returns info for set object

    Used in "sets.html" to render the dialog preview

    set_id: int
    rtype: str - JSON string containing set data
    """

    

    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    fc_set_json = {
        "name": fc_set.name,
        "flashcard_ids": [card._id for card in fc_set.cards], # List of card ids
        "default_front": fc_set.default_front,
        "default_back": fc_set.default_back
    }
     
    return json.dumps(fc_set_json)


@api_bp.route("/sets/delete/<int:set_id>")
def delete_set(set_id):
    """
    Deletes the object in the database

    set_id: int
    rtype: None
    """
    # Gets all flashcards with the ids given
    fc_set = FlashcardSet.query.filter_by(_id=set_id).first()

    if fc_set:
        db.session.delete(fc_set)
        db.session.commit()

    return "Flashcards Successfully Deleted"