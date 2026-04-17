import { MAX_E_FACTOR } from "/static/utils/constants.js";
import { floatToPercent } from "/static/utils/helpers.js"; 
import { initReturnToSetsButton, initReviewModeButton, formatElapsedTime } from "./dialogUtils.js";

export function setupPauseDialog(pauseButton, sessionState) {

    const pauseDialog = document.getElementById("pause-event-dialog");

    const pauseInfoDiv = pauseDialog.querySelector("#pause-info-div");
    setupSessionData(pauseInfoDiv, sessionState);

    const timeHeader = pauseInfoDiv.querySelector("#curr-time-elapsed-header");
    
    pauseButton.addEventListener("click", () => {
        pauseDialog.showModal();
        timeHeader.innerText = formatElapsedTime(sessionState.timeElapsed);
    })

    const pauseNavigationDiv = pauseDialog.querySelector("#pause-navigation-div");
    setupNavigationButtons(pauseDialog, pauseNavigationDiv, sessionState);

}

function setupSessionData(pauseInfoDiv, sessionState) {
    
    const pauseHeader = pauseInfoDiv.querySelector("#pause-header");
    pauseHeader.innerText = `${sessionState.setName} Paused`;

    const percentLearnedHeader = pauseInfoDiv.querySelector("#percent-learned-header");
    percentLearnedHeader.innerText = getPercentLearned(sessionState.cards)

}

function getPercentLearned(cards) {
    const totalCardsNum = cards.length
    const learnedCards = cards.filter(card => card.eFactor === MAX_E_FACTOR);

    return floatToPercent((learnedCards.length / totalCardsNum));
}

function setupNavigationButtons(pauseDialog, pauseNavigationDiv, sessionState) {
    const cancelButton = pauseNavigationDiv.querySelector("#cancel-navigation-button");
    cancelButton.addEventListener("click", () => {
        pauseDialog.close()
    })

    const reviewModeButton = pauseNavigationDiv.querySelector("#review-mode-button");
    initReviewModeButton(reviewModeButton, sessionState);

    const returnToSetsButton = pauseNavigationDiv.querySelector("#return-to-sets-button");
    initReturnToSetsButton(returnToSetsButton);
}