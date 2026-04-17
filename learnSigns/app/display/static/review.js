import { loadCard, nextCard, previousCard } from "/static/flashcard/flashcard.js";
import { getCardStructureElements, setupFlashcard } from "/static/flashcard/flashcardUtils.js";

export function setupReviewActions(cards, cardState) {
    const elements = getAllReviewElements();

    setupNavigationButtons(elements, cards, cardState)

    setupFlashcard(elements, cards, cardState)

    setupFlashcardSync(elements, cards, cardState);

    // Update elements with first card
    updateFlashcardNumber(elements, cardState)
    loadCard(cards, cardState);
}

function setupFlashcardSync(elements, cards, cardState) {
    const { cardButtonsDiv } = elements;

    cardButtonsDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "BUTTON") {
            // Updates flashcard number
           updateFlashcardNumber(elements, cardState)
            
            // Syncs changes
            loadCard(cards, cardState);
        }
    })
}

function updateFlashcardNumber(elements, cardState) {
    const { flashcardNumberDisplay } = elements;

    flashcardNumberDisplay.innerText = cardState.index + 1;
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