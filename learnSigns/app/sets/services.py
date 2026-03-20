from app.extensions import db
from app.models import Flashcard

def delete_cards(card_id_list):
    """
    Deletes all the flashcards with the ids in the list

    card_id_list: list(int)
    rtype: None
    """
    # Gets flashcards with matching ids and deletes them
    cards = Flashcard.query.filter(Flashcard._id.in_(card_id_list)).delete()

    db.session.commit()