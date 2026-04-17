import { addArrayNumbers, getAllEFactors } from "/static/flashcard/flashcard.js";

function returnToSets() {
    window.location.href = "/sets/"
}

export function initReturnToSetsButton(returnButton) {
    returnButton.addEventListener("click", returnToSets);
}

// ------------- SESSION DETAILS -------------

// Time elapsed
export function formatElapsedTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `Time Elapsed: ${minutes}:${remainingSeconds}`;
}

// Review mode

function switchToReviewMode(sessionState) {
    const reviewUrl = `/study/review/${sessionState.setId}`;
    
    window.location.href = reviewUrl;
}

export function initReviewModeButton(reviewButton, sessionState) {
    reviewButton.addEventListener("click", () => {
        switchToReviewMode(sessionState);
    })
}

// Session state element

export function initSessionState(cards, setName, setId) {
    console.log(cards)
    return {
        "cards": cards,
        "setName": setName,
        "setId": setId,
        "timeElapsed": 0,
        "totalEFactor": addArrayNumbers(getAllEFactors(cards))
    }
}