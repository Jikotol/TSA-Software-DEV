import pandas as pd
import json

def csv_to_dicts(df) -> dict[str, list[dict]]: 
    """ Loads info from csv and compiles it into entries by mapping each 
    formatted term to a dict

    Returns:
        dict[str, list[dict]]: formatted term dict has term metadata and list
        of entry dictionaries (one per CSV row).
    
    """
    asl_dictionary = {}
    eng_gloss = ""
    for row in df.itertuples():
        if eng_gloss == row.main_gloss:
            continue
        eng_gloss = row.main_gloss
        if not eng_gloss in asl_dictionary.keys():
            # Creates new term dict if missing
            asl_dictionary[eng_gloss] = {
                "similar_eng_terms": eng_terms_map[eng_gloss] if eng_gloss in eng_terms_map.keys() else None,
                "main_entries": [],
                "variant_entries": []
            }
        
        # Accesses already present dict
        term_dict = asl_dictionary[eng_gloss] 
        entry = {
            "asl_gloss": row.og_gloss,
            "handshape": {
                "dom": {"start": row.dominant_start_handshape, "end": row.dominant_end_handshape},
                "non_dom": {"start": row.non_dominant_start_handshape if not pd.isna(row.non_dominant_start_handshape) else None, 
                            "end": row.non_dominant_end_handshape if not pd.isna(row.non_dominant_end_handshape) else None}
            },
            "ref_components": row.components.split("+") if not pd.isna(row.components) else None,
            "display_parts": row.display_compound_word.split("+") if not pd.isna(row.components) else None,
            "notes": row.notes if isinstance(row.notes, str) else None
        }
        term_dict["variant_entries"].append(entry)
    return asl_dictionary
def get_main_entries(variants):
    """
    variants: list[dict]
    rtype: list[dict]
    """
    if len(variants) == 1:
        return variants
    for variant in variants:
        print(variant["asl_gloss"])
def get_hand_sign_freq(dom_hs, non_dom_hs):
    ...
# variants are usually the main gloss
# compounds are usually not main gloss
# main glosses tend to have no special characters besides dashes
# main gloss should have common hand signs
# main gloss --> simplest way to sign work, no variants, no weird stuff. 
eng_terms_map = {
}
df = pd.read_csv("final_data.csv")
asl_dictionary = csv_to_dicts(df)
# get_main_entries(asl_dictionary["WHAT HAPPENED?"]["variant_entries"])
with open('data.json', 'w') as json_file:
    json.dump(asl_dictionary, json_file, indent=4)
# fill in variant gloss list, sort it, then get the last element in list(main gloss)
# check if there's more than that one element, and if there is, get the entry from variant_entries list and put it in 
# main gloss list