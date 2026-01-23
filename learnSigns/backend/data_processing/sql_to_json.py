import json
import os

def main():
    ...
"""
{
  "set_id": "asl_basics",
  "default_front_view": "sign_video",
  "default_back_view": "english_term",
  "cards": [
    { "gloss_id": 12 },
    { "gloss_id": 15 },
    {
      "gloss_id": 18,
      "override": {
        "front_view": "sign_video_with_notes"
      }
    }
  ]
}

Based on user input(again), stored in user json
set json --> store refs to cards and defaults and overrides

LATER WHEN DOING UI CALLS
make flashcard objects(dicts) with actual info to avoid pricey sql calls which
are stored in memory and deleted after session
"""

def set_id_exists():
    ...

def generate_template_dict(set_id, cards, front="video", back="english_term"):
    valid_combinations = [("video", "english_term"), ("english_term", "video")]
    if (front, back) not in valid_combinations:
        raise ValueError("Invalid front/back combination")
    return {
        "set_id": set_id,
        "default_front_view": front,
        "default_back_view": back,
        "cards": cards
    }

def insert_set_dict(sets_file_path, set_name, set_dict):
    if os.path.exists(sets_file_path):
        with open(sets_file_path, "r") as file:
            sets = json.load(file)
    else:
        sets = {}
    sets[set_name] = set_dict
    with open(sets_file_path, "w") as file:
        json.dump(sets, file)

""" Converts data in sql data base into a usable json format. """

def create_flashcard(cur, gloss_id, set_name, display_components=False, description=False front="term", back="video"):
    """ Makes and returns correctly formatted python dict. 
    cur: sqlite3.Cursor
    rtype: dict[str, Union[str, bool]]
    """



def add_flashcard_to_json():
    """ Opens JSON file and dumps the python object inside with respect to set name """

# Make a dict obj. maybe return dict obj then have update func
# put gloss_id

# determine how its formatted(front, back, etc) in function parameters
# Sep func for one func, This not for converting all glosses
# later link to onevent func linked to btn
# later create new file for each user
"""
set = dict()
set[1]["front"]["display_components"]

"""