import pandas as pd
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
        


    


class Setup():
    ...

def main():
    df = pd.read_csv("")
    dictionary = csv_to_dicts(df)
if __name__ == "__main__":
    main()
