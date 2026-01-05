import pandas as pd
import re

patterns = [r"\(.+\)", r"\([a-zA-Z]+-?.?\)", r"\\", r"\"", r"(nd-C)"]


prefixes = ["fs-", "ns-", "nat-", r"alt\.", "BCL", "PCL", "DCL", "ICL", "LCL", "SCL"]

suffixes = ["-pl", "_2", "wg", "_3", "_4"]

suffix_pattern = '|'.join(suffixes)

["fs-", ""]

prefix_pattern = '|'.join(prefixes)

def update_columns(id_num):
    gloss_label = df.loc[df["video_id"] == id_num, "main_gloss"].values[0]
    notes_label = ""
    if "(2h)" in gloss_label:
        df.loc[df["video_id"] == id_num, "handedness"] = "2"
    else:
        df.loc[df["video_id"] == id_num, "handedness"] = "1"
    gloss_label = re.sub(r"\([^)]+\)", "", gloss_label)
    if "/" in gloss_label:
        variant_tuple = re.findall(r"([a-z-]+)/([a-z-]+)", gloss_label, flags=re.IGNORECASE)[0]
        df.loc[df["video_id"] == id_num, "variant_1"], df.loc[df["video_id"] == id_num, "variant_2"] = variant_tuple[0], variant_tuple[1]
    if "+" in gloss_label:
        if df.loc[df["video_id"] == id_num, "variant_1"].iloc[0]:
            compound_word = re.findall(r"[A-Z/-]+\+([A-Z/-]+)", gloss_label)
        else:
            compound_word = re.findall(r"([A-Z/-]+\+[A-Z/-]+)", gloss_label)
        if compound_word:
            df.loc[df["video_id"] == id_num, "compounded_word"] = compound_word[0]
        notes_label = notes_label + "manually enter"
    if "-" in gloss_label:
        gloss_label = re.sub(r"-", " ", gloss_label)
    if "#" in gloss_label:
        gloss_label = re.sub(r"#", "", gloss_label)
        if notes_label:
            notes_label = notes_label + " fingerspelled"
        else:
            notes_label = notes_label + "fingerspelled"
    df.loc[df["video_id"] == id_num, "notes"] = notes_label
    df.loc[df["video_id"] == id_num, "main_gloss"] = gloss_label

""" 
+ --> 2 signs to make another sign
/ --> the signs are very similar or the same so they are glossed teh same
(2h) and (1h) --> sign is done with one or two hands

"""



def convert(text): # converts the og gloss to eng gloss(not guaranteed)
    if not isinstance(text, str):
        return text
    for pattern in patterns:
        text = re.sub(r"(LCL|SCL|ICL|DCL|PCL|BCL):?[A-Z0-9]{1}-?[A-Z]?\\{1}", "", text)
        text = re.sub(prefix_pattern, "", text)
        text = re.sub(suffix_pattern, "", text)
        text = re.sub(pattern, "", text)
        text = text.replace("#", "")
    return text
def replace_plusses(text): 
    """
    type text: str
    rtype: list
    """
    return [text.replace("+", ""), text.replace("+", " "), text.replace("+", "-")]
def replace_dashes(text):
    return [text.replace("-", " ")]
def sub_variants(row): # replace args in name with 
    ...
def get_contenders(row):
    contenders = []
    og_gloss = row.og_gloss
    clean_gloss = convert(og_gloss)
    contenders.append(clean_gloss)
    if not isinstance(clean_gloss, str):
        return contenders
    if "+" in og_gloss:
        contenders = contenders + replace_plusses(clean_gloss)
    if "/" in og_gloss:
        ...
    if "-" in og_gloss:
        contenders = contenders + replace_dashes(clean_gloss)
    return contenders

def main():
    df = pd.read_csv("ASLLRP_data_full.csv")
    """checks if my conversion function worked
    """
    counter = 0
    all_gloss_contenders = []
    for row in df.itertuples():
        all_gloss_contenders.append(get_contenders(row))
    for contender_list in all_gloss_contenders:
        equal_to_main_gloss = False
        for contender in contender_list:
            if contender in df['main_gloss'].values:
                equal_to_main_gloss = True
                continue
        if not equal_to_main_gloss:
            counter += 1
    print(counter)

if __name__ == "__main__":
    main()

"""
df["handedness"] = ""
df["notes"] = ""
df["variant_1"] = ""
df["variant_2"] = ""
df["compounded_word"] = ""
df = df.rename(columns={"Video ID number": "video_id", 
                        "Main entry gloss label": "og_gloss", 
                        "Dominant start handshape": "dominant_start_handshape", 
                        "Non-dominant start handshape": "non_dominant_start_handshape", 
                        "Dominant end handshape": "dominant_end_handshape", 
                        "Non-dominant end handshape": "non_dominant_end_handshape", 
                        "full video file": "video_file"})
df["main_gloss"] = df["og_gloss"]
df["main_gloss"] = df["main_gloss"].map(convert)
df["video_id"].map(update_columns)
new_order = [
    "video_id",
    "main_gloss",
    "og_gloss",
    "dominant_start_handshape",
    "non_dominant_start_handshape",
    "dominant_end_handshape",
    "non_dominant_end_handshape",
    "video_file",
    "handedness",
    "variant_1",
    "variant_2",
    "compounded_word",
    "notes"
]
df = df[new_order]"""