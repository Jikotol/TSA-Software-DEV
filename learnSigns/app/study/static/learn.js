import { loadCard, updateEasinessFactor, selectWeightedCard } from "/static/flashcard/flashcard.js";
import { getCardStructureElements, setupFlashcard } from "/static/flashcard/flashcardUtils.js";

export function setupLearnActions(cards, cardState) {
    const elements = getAllLearnElements();
    
    setupFeedbackButtons(elements, cards, cardState)

    setupFlashcard(elements, cards, cardState)

    setupFlashcardUpdate(elements, cards, cardState)

    loadCard(cards, cardState);
}

function setupFlashcardUpdate(elements, cards, cardState) {
    const { cardButtonsDiv } = elements;

    cardButtonsDiv.addEventListener("click", () => {
        if (event.target.tagName === "BUTTON") {
            selectWeightedCard(cards, cardState);
            loadCard(cards, cardState);
        }
    })
    
}

function getAllLearnElements() {
    const base = getCardStructureElements();
    return {
        ...base,
        ...getFeedbackButtons(base.cardButtonsDiv),
    }
}

function getFeedbackButtons(cardButtonsDiv) {
    return {
        easyButton: cardButtonsDiv.querySelector("#easy-button"),
        goodButton: cardButtonsDiv.querySelector("#good-button"),
        hardButton: cardButtonsDiv.querySelector("#hard-button"),
        wrongButton: cardButtonsDiv.querySelector("#wrong-button")
    }
}

function setupFeedbackButtons(elements, cards, cardState) {
    const { easyButton, goodButton, hardButton, wrongButton } = elements;

    easyButton.addEventListener("click", () => {
            updateEasinessFactor(cards[cardState.index], 3);
        });
    
    goodButton.addEventListener("click", () => {
            updateEasinessFactor(cards[cardState.index], 2);
        });

    hardButton.addEventListener("click", () => {
            updateEasinessFactor(cards[cardState.index], -2);
        });

    wrongButton.addEventListener("click", () => {
            updateEasinessFactor(cards[cardState.index], -4);
        });
    }
