import csv

class FlashcardSet():
    def __init__(self, name="None", *args):
        self.name = name
        # cards are unordered TEMP
        self.cards = set(*args)
    def add_card(self, card):
        if card.type != Flashcard:
            raise TypeError("Must be a flashcard object to add to a flashcard set")

class Flashcard():
    def __init__(self, term, definition, video_id, gloss_lable, options=[]):
        self.term = term
        self.defintion = definition
        self.video_id = video_id
        self.gloss_lable = gloss_lable
        self.options = options
    def get_video():
        ...

class FlashcardManager():

    def __init__(self):
        pass

    def create_flashcard(term_dict, options: list) -> Flashcard:
        """ Verifies links and definition and creates flashcard with proper formatted data"""
        ...

    def get_definition(term: str) -> str:
        """ Gets definition online for a specified word and returns it """

    def format_data(data: str) -> str:
        """ Formats a single data from csv to have proper punctuation, capitalization, and gets rid of meta data """
        data = data.lower()
        


    def csv_to_dicts() -> dict[str, list[dict]]: 
        """ Loads info from csv and compiles it into entries by mapping each 
        formatted term to a dict

        Returns:
            dict[str, list[dict]]: formatted term dict has term metadata and list
            of entry dictionaries (one per CSV row).
        
        """
        card_data_dict = {}
        with open("sample_ASLLRP_data.csv") as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                formatted_term = FlashcardManager.format_data(row["main entry gloss label"])
                if not formatted_term in card_data_dict.keys():

                    # Creates new term dict if missing
                    card_data_dict[formatted_term] = {
                        "term": row["main entry gloss label"],
                        "entry": []
                    }
                
                # Accesses already present dict
                term_dict = card_data_dict[formatted_term]
                
                entry = {
                    "csv_term": formatted_term,
                    "video_id": row["Video ID number"],
                    "start_dom_handshape": row["Dominant start handshape"],
                    "end_dom_handshape": row["Dominant end handshape"],
                    "video_file": row["full video file"],
                    "num_hands": FlashcardManager.get_hand_num(row["main entry gloss label"])
                }

                # Creates term id for multiple entries. ex. 1
                entry["term_id"] = len(term_dict["entry"])

                term_dict["entry"].append(entry)

        return card_data_dict


class Setup():
    ...

def main():
    manager = FlashcardManager()
    dicts = FlashcardManager.csv_to_dicts()
    print(dicts["(1)cheat"]["entry"][0]["term_id"])
if __name__ == "__main__":
    main()
