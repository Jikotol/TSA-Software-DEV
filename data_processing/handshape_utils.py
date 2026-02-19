import pandas as pd

def make_hs_freq_dict(df):
    """
    Makes dict of the most common handshapes by counting the appearances of each sign in the ASLLRP dataset 
    This is used to weed out rare handsigns in order to select a head gloss.

    df: pandas.Dataframe
    rtype: dict[str, int]
    """
    # Create frequency dict
    freq_dict = {}

    for row in df.itertuples():
        for col in ["dominant_start_handshape","non_dominant_start_handshape","dominant_end_handshape","non_dominant_end_handshape"]:
            handsign = getattr(row, col)
            if pd.isna(handsign):
                continue
            # handsign = handsign.replace(".png", "")
            if handsign not in freq_dict:
                freq_dict[handsign] = 0
            freq_dict[handsign] += 1
    return freq_dict
def get_handedness(row):
    """
    Uses the handsigns of each gloss to determine whether the gloss uses one, both, or a mix with
    each word in a compound gloss having different handedness.

    row: namedtuple
    rtype: int || None
    """


def main():
    df = pd.read_csv("final_data.csv")
    hs_freq_dict = make_hs_freq_dict(df)
    print(hs_freq_dict["B-L"], hs_freq_dict["B"])
if __name__ == "__main__":
    main()