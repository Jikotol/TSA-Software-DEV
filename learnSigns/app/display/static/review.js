import { loadCard, nextCard, previousCard } from "./flashcard.js"
import ()

export function setupReviewActions(cards, cardState) {
    const elements = getAllReviewElements();

    setupNavigationButtons(elements, cards, cardState)

    setupFlashcard(elements, cards, cardState)

    setupFlashcardSync(elements, cards, cardState);
}

function setupFlashcardSync(elements, cards, cardState) {
    const { cardButtonsDiv, flashcardNumberDisplay } = elements;

    cardButtonsDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "BUTTON") {
            // Updates flashcard number
            flashcardNumberDisplay.innerText = cardState
            
            // Syncs changes
            loadCard(cards, cardState);
        }
    })
}

function setupNavigationButtons(elements, cards, cardState) {
    const { nextButton, backButton } = elements;

    // Goes to the next flashcard
    nextButton.addEventListener("click", () => {
        nextCard(cards, cardState);
    });
            
    // Goes to the previous flashcard
    backButton.addEventListener("click", () => {
        previousCard(cards, cardState);
    }); 
}


function getAllReviewElements() {
    const base = getCardStructureElements();
    return { 
        ...base,
        ...getReviewAButtons(base.cardButtonsDiv)
    }
}

function getReviewAButtons(cardButtonsDiv) {
    return {
        backButton: cardButtonsDiv.querySelector("#back-button"),
        flashcardNumberDisplay: cardButtonsDiv.querySelector("#flashcard-number"),
        nextButton: cardButtonsDiv.querySelector("#next-button")
    }

}