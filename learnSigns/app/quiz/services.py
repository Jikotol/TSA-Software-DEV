from app.models import Gloss
import random 
# choose card from set --> make question
# internal logic --> small set, hs and video else just 

# 10 qs, 20 qs, 30 qs


# cardsNumber needs to be >= 4
def generateQuestionData(cards):
    cards = list(cards)

    questionsNumber = choose_question_number(cards.length)

    questions = []

    {"type": video, "flashcard": fc, "correct_answer": "a", "info": {"src"}, "choices": {"a": "some string", "b": "ahsheoif"}}

    # return list of dict that contain the fc obj and type

def generate_hand_shape_question(card, allCards):

    (choices, correct_answer) = init_hand_shape_choices(card, allCards)

    return {
        "type": "video",
        "flashcard": card,
        "correct_answer": correct_answer,
        "choices": choices
    }





def init_hand_shape_choices(card, allCards):
    choices = {}
    cards_used = []
    letters = ["a", "b", "c", "d"]

    correctAnswerIndex = choose_random(range(len(letters)))
    answer_letter = letters[correctAnswerIndex]

    choices[answer_letter] = card.term

    del letters[correctAnswerIndex]

    for letter in letters:
        random_card = choose_random(allCards)




def init_video_question(card, allCards):

    (choices, correct_answer) = init_term_choices(card, allCards)

    gloss = Gloss.query.filter_by(_id=card._id).first()

    return {
        "type": "video",
        "flashcard": card,
        "correct_answer": correct_answer,
        "info": {"src": gloss.video.youtube_url, "credit": gloss.video.credit},
        "choices": choices
    }

    
def init_term_choices(card, allCards):
    choices = {}
    cards_used = []
    letters = ["a", "b", "c", "d"]

    correctAnswerIndex = choose_random(range(len(letters)))
    answer_letter = letters[correctAnswerIndex]

    choices[answer_letter] = card.term

    del letters[correctAnswerIndex]

    for letter in letters:
        while True:
            choice = choose_random(allCards)

            if choice != card and choice not in cards_used:
                choices[letter] = card.term
                cards_used.append(card)

    return (choices, answer_letter)


def choose_question_number(cardsNum):
    if cardsNum * 2 >= 30:
        return 30
    return cardsNum * 2

def choose_random(cards):
    return random.choice(cards)