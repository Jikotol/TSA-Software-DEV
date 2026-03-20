from sqlalchemy import or_

from app.models import Components, MainGloss, Gloss
from app.extensions import db

import app.utils as utils

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

    # Includes glosses with "+" or nothing on either side
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

def get_main_head_tuples(tuples=6):
    """
    Randomly gets and formats main gloss objects and their head gloss objects for video browsing in home page
    """
    random_main_head_tuples = []
    used_ids = set()

    while len(random_main_head_tuples) < tuples:
        main_gloss = utils.get_random_row(MainGloss)

        # Filters out duplicateds
        if main_gloss._id in used_ids:
            continue

        used_ids.add(main_gloss._id)

        head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first()
        random_main_head_tuples.append((main_gloss, head_gloss))
    
    return random_main_head_tuples