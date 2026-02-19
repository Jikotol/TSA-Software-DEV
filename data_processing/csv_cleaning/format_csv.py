from learnSigns.backend.data_processing.csv_cleaning.clean_csv import convert, prefixes
import pandas as pd
import re

def fix_variant_columns(df):

    for row in df.itertuples():
        gloss = row.og_gloss
        if isinstance(gloss, str):
            df.loc[df["og_gloss"] == gloss, "variant_1"] = convert(row.variant_1)
            df.loc[df["og_gloss"] == gloss, "variant_2"] = convert(row.variant_2)
            if "/" in gloss and "+" not in gloss:
                df.loc[df["og_gloss"] == gloss, "variants"] = row.variant_1 + "/" + row.variant_2
            elif "/" in gloss:
                all_variants = []
                for pattern in [r"(.+\/.+)\+", r"\+(.+\/.+)"]:
                    variant_list = re.findall(pattern, gloss)
                    if variant_list:
                        for variant in variant_list:
                            variant = variant.split("/")
                            variant = map(convert, variant)
                            all_variants = all_variants + ["/".join(variant)]
                df.loc[row.Index, "variants"] = ";".join(all_variants)
"""
Fills the components column which has the main glosses of each gloss in the row
For ex. og_gloss - (1h)GOOD/THANK-YOU+ENOUGH --> GOOD/THANK-YOU+ENOUGH
"""
def check_compound_sign(og_gloss):
    if isinstance(og_gloss, str) and "+" in og_gloss:
        return True
    return False
def separate_glosses(og_gloss):
    if check_compound_sign(og_gloss):
        return og_gloss.split("+")
    return []
def check_if_sign(gloss):
    if isinstance(gloss, str):
        return False if "\\" in gloss else True
    return True
def clean_glosses(df, og_gloss):
    cleaned_glosses = []
    for gloss in separate_glosses(og_gloss):
        if check_if_sign(gloss):
            cleaned_glosses.append(convert(gloss))
        else:
            cleaned_glosses.append(map_sign_types(og_gloss))
            df.loc[df["og_gloss"] == og_gloss, "compounded_word"] = "MANUAL"
    return cleaned_glosses
def update_components_col(df):
    if "components" not in df.columns:
        df["components"] = ""
    for row in df.itertuples():
        gloss = row.og_gloss
        df.loc[df["og_gloss"] == gloss, "components"] = "+".join(clean_glosses(df, gloss))
def map_sign_types(gloss):
    for type in description_sign_type_map.keys():
        if type in gloss:
            return description_sign_type_map[type]
    return "MANUAL"
description_sign_type_map = {
"BCL": "body",
"BPCL": "body part", 
"DCL": "descriptive", 
"ICL": "instrument", 
"LCL": "locative", 
"PCL": "plural",
"SCL": "semantic"
}
"""
Fills the handedness column for each row. Takes beginning and end handsign values and puts the handedness for the whole sign

function that updates the handedness column with either one or two
function that clears a columns values
"""
def update_handedness_col(df):
    df["handedness"] = pd.NA
    df["handedness"] = df["handedness"].astype("Int64")
    for row in df.itertuples():
        # changes panda null data types to None so the length is correct
        dom_handshapes = [s for s in [row.dominant_start_handshape, row.dominant_end_handshape] if not pd.isna(s)]
        non_dom_handshapes = [s for s in [row.non_dominant_start_handshape, row.non_dominant_end_handshape] if not pd.isna(s)]
        if len(dom_handshapes) == 2 and len(non_dom_handshapes) == 0:
            df.loc[row.Index, "handedness"] = int(1)
        elif len(dom_handshapes) == len(non_dom_handshapes) == 2:
            df.loc[row.Index, "handedness"] = int(2)
        else:
            df.loc[row.Index, "handedness"] = pd.NA
"""
Fills in display_components column
Contains a string users will see with variant stuff included
"""
def update_display_components_col(df):
    for row in df.itertuples():
        og_gloss = row.og_gloss
        if not isinstance(row.compounded_word, str):
            continue
        if not "+" in og_gloss:
            continue
        if "\\" in og_gloss:
            df.loc[row.Index, "compounded_word"] = "MANUAL"
        elif re.search(r"\(.+\)", og_gloss) and "/" not in og_gloss:
            df.loc[row.Index, "compounded_word"] = og_gloss
        for prefix in prefixes:
            if prefix in og_gloss and not prefix in row.compounded_word:
                if prefix in ["ns-", "fs-"]:
                    df.loc[row.Index, "compounded_word"] = row.compounded_word + "MANUAL"
            
df = pd.read_csv("final_data.csv")
df.to_csv("test.csv", index=False)
"""
PROBLEM --> variants col uses og glosses, so to link, i need to access the glosses which is in a list in the dict

SOLUTION --> make eng_to_csv func that goes through a dict that links the og glosses to the eng
The dict only has glosses that are different than main_gloss

"""
