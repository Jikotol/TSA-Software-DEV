import { loadCard, updateEasinessFactor, selectWeightedCard } from "display/static/flashcard.js"
import ()

export function setupReviewActions(cards, cardState) {
    const elements = getAllLearnElements();
    
    setupFeedbackButtons(elements, cards, cardState)

    setupFlashcard(elements, cards, cardState)

    setupFlashcardUpdate(elements, cards, cardState)
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
            updateEasinessFactor(cards[state.index], 3);
        });
    
    goodButton.addEventListener("click", () => {
            updateEasinessFactor(cards[state.index], 2);
        });

    hardButton.addEventListener("click", () => {
            updateEasinessFactor(cards[state.index], -2);
        });

    wrongButton.addEventListener("click", () => {
            updateEasinessFactor(cards[state.index], -4);
        });
    }
