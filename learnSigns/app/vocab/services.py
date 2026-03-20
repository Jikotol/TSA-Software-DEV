from app.models import Gloss
from app.home.services import get_main_gloss_from_notes, search_components

def get_related_glosses(main_gloss):
    """
    Returns related glosses by matching gloss notes and compenents, used to link vocab pages

    main_gloss: MainGloss
    """

    head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()

    sim_notes_list = []

    # Finds glosses with the similar notes to head_gloss
    if head_gloss.notes:
        group = head_gloss.notes

        # Separates based on group, (e.g Possessive pronoun; singular; shows who/what owns something --> Possessive pronoun)
        if ";" in head_gloss.notes:
            group = head_gloss.notes.split(";")[0]

        sim_notes_list = get_main_gloss_from_notes(search_pattern=f"%{group}%", limit=6)
    
    # Looks through components to find glosses that use it
    appears_in_list = search_components(search=head_gloss.asl_gloss, limit=12)

    return {
        "same_notes_main_glosses": sim_notes_list,
        "appears_in_main_glosses": appears_in_list
    }