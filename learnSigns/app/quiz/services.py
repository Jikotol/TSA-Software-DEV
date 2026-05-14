import random
from ..models import MainGloss, Gloss

import app.utils as utils 

def init_quiz_data(cards):
    """ Generates meta data for stuff, will be given to frontend as json

    this is called when user loads quiz page

    user_choices --> filled with terms

    questions_dict ={
    this in camel case actually
        {"correct_answer_data": {"gloss_id": Somenum, "flashcard_num": some_num}, "correct_answer": letter, "user_choices": choices, "type": some_string}
    }"""

    questions_num = choose_quiz_length(len(cards))

    available_cards = cards

    questions = {}
    question_index = 0

    while question_index < questions_num or len(available_cards) == 0:
        random_card = choose_random(available_cards)
        
        # Initiallizes question dict
        question_data_dict = init_question(available_cards, random_card)

        # Prevents duplicate questions
        
        if is_duplicate_question(questions, question_data_dict, question_index):
            question_data_dict["type"] = get_opposite_type(question_data_dict["type"])
            if is_duplicate_question(questions, question_data_dict, question_index):
                available_cards = [card for card in cards if card != random_card]
                continue
            
        questions[question_index] = question_data_dict
        question_index += 1

    return questions
   
def get_opposite_type(question_type):
    if question_type == "handshape":
        return "video"
    return "handshape"

def init_question(all_cards, card):
    question_data_dict = {}

    question_data_dict["correctAnswerData"] = {
        "glossId": card.gloss_id,
        "flashcardId": card._id
    }

    (choices, answer_letter) = init_choices(card, all_cards)

    question_data_dict["userChoices"] = choices
    question_data_dict["correctAnswer"] = answer_letter
    question_data_dict["type"] = choose_random(["handshape", "video"])

    return question_data_dict

def init_choices(card, cards):
    """ gives dict with answer choices, answer chioces are strings"""
    choices = {}
    letters = ["a", "b", "c", "d"]

    correct_index = choose_random(range(len(letters)))
    answer_letter = letters[correct_index]

    choices[answer_letter] = card.term

    del letters[correct_index]

    # Filters out correct answer card
    valid_cards = [c for c in cards if c != card]

    cards_used = []

    for letter in letters:
        available = [c for c in valid_cards if c not in cards_used]

        if not available:
            
            # Gets random gloss if run out of cards
            main_gloss = utils.get_random_row(MainGloss)
            head_gloss = Gloss.query.filter_by(_id=main_gloss.head_gloss_id).first() 
            choices[letter] = head_gloss.display_name if head_gloss.display_name else head_gloss.asl_gloss
            continue

        random_card = choose_random(available)
        choices[letter] = random_card.term
        cards_used.append(random_card)

    return (choices, answer_letter)

def choose_quiz_length(cardsNum):
    if cardsNum * 2 >= 30:
        return 30
    return cardsNum * 2

def choose_random(items):
    return random.choice(items)

def is_duplicate_question(all_questions, question, question_index):

    all_questions[question_index] = question

    question_tuple_list = convert_into_tuples(all_questions)

    if len(all_questions) == len(set(question_tuple_list)):
        return False
    else:
        return True
    
def convert_into_tuples(questions):
    question_tuples = []

    for _, question_dict in questions.items():
        question_tuples.append((question_dict["type"], question_dict["correctAnswerData"]["glossId"]))

    return question_tuples