from utils.helper_data import hs_image_map
from sqlalchemy.sql.expression import func

def get_random_row(obj):
    # Use func.random() which SQLAlchemy compiles to the correct DB-specific function
    random_row = obj.query.order_by(func.random()).first()
    return random_row

def get_hs_img_path(hs, add_images_path=True):
    if hs in hs_image_map.keys():
        return "images/handshapes/" + hs_image_map[hs] if add_images_path else hs_image_map[hs]

def get_hs_imgs(gloss):
    """
    Maps the glosses handshapes to their image and returns the values in a dictionary.

    gloss: Gloss
    rtype: dict
    """
    hs_dict = dict(vars(gloss.handshape))

    return {
        "dom_start": get_hs_img_path(hs_dict["dom_start"]),
        "dom_end": get_hs_img_path(hs_dict["dom_end"]),
        "non_dom_start": get_hs_img_path(hs_dict["non_dom_start"]),
        "non_dom_end": get_hs_img_path(hs_dict["non_dom_end"])
    }