"""takes csv and combines entries

info:
combines signs with exact same hand signs and name

"""

import pandas as pd
import re

df = pd.read_csv("ASLLRP_data(OLD).csv")
df = df.sort_values(by='main_gloss')
df = df.drop_duplicates()
df.to_csv("ASLLRP_data_full.csv", index=False)
