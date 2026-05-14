/* Controls the dialogs for finishing the learning session */

import { MAX_E_FACTOR } from "/static/utils/constants.js";
import { initReturnToSetsButton, initReviewModeButton, formatElapsedTime } from "./dialogUtils.js";
import { addArrayNumbers, getAllEFactors } from "/static/flashcard/flashcard.js";

export function setupFinishDialog(document, cardButtonsDiv, sessionState) {

    const elements = getAllElements(document);

    setupSessionData(elements, sessionState);

    setupNavigationButtons(elements, sessionState);

    setupCardButtonsDiv(elements, cardButtonsDiv, sessionState);

}

function setupCardButtonsDiv(elements, cardButtonsDiv, sessionState) {
    const { finishDialog } = elements;

    cardButtonsDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "BUTTON") {

            let averageEFactor = addArrayNumbers(getAllEFactors(sessionState.cards));

            averageEFactor = (averageEFactor/sessionState.cards.length)

            if (averageEFactor == MAX_E_FACTOR) {
                    finishDialog.showModal();
            }
        }
    })
}

function getAllElements(document) {
    const finishDialog = document.getElementById("finish-event-dialog");
    return {
        document,
        finishDialog,
        resetConfirmDialog: document.getElementById("reset-progress-dialog"),
        ...getNavigationElements(finishDialog),
        ...getInfoElements(finishDialog),
    }
}

function getNavigationElements(finishDialog) {
    const finishNavigationDiv = finishDialog.querySelector("#finish-navigation-div");
    return {
        finishNavigationDiv,
        resetLearningButton: finishNavigationDiv.querySelector("#reset-learning-button"),
        reviewModeButton: finishNavigationDiv.querySelector("#review-mode-button"),
        returnToSetsButton: finishNavigationDiv.querySelector("#return-to-sets-button"),
        quizModeButton: finishNavigationDiv.querySelector("#quiz-button")
    }
}

function getInfoElements(finishDialog) {
    const finishInfoDiv = finishDialog.querySelector("#finish-details-div");
    return {
        finishInfoDiv: finishInfoDiv,
        finishHeader: finishInfoDiv.querySelector("#finish-header"),
        termsLearnedHeader: finishInfoDiv.querySelector("#total-learned-header")
    }   
}


function setupSessionData(elements, sessionState) {
    const { finishHeader, termsLearnedHeader } = elements;

    finishHeader.innerText = `${sessionState.setName} Learned`;
    termsLearnedHeader.innerText = `Terms Learned: ${sessionState.cards.length}`
}

function setupNavigationButtons(elements, sessionState) {
    const { reviewModeButton, quizModeButton, returnToSetsButton } = elements;

    setupResetLearningButton(elements, sessionState);

    // From flashcard.js
    initReviewModeButton(reviewModeButton, sessionState); 
    initReturnToSetsButton(returnToSetsButton);

    quizModeButton.addEventListener("click", () => {

        window.location.href = `/quiz/${sessionState.setId}`;
    })

}

function setupResetLearningButton(elements, sessionState) {
    const { finishDialog, resetConfirmDialog, resetLearningButton } = elements;
    setupResetConfirmationDialog(finishDialog, resetConfirmDialog, sessionState);

    resetLearningButton.addEventListener("click", () => {
        resetConfirmDialog.showModal();
    })
}

function resetProgress(cards) {
    for (let i=0; i<cards.length; i++) {
        cards[i]["eFactor"] = 12;
    }
}

function setupResetConfirmationDialog(finishDialog, resetConfirmDialog, sessionState) {
    resetConfirmDialog.addEventListener("click", (event) => {
        if (event.target.id == "yes-reset-button") {
            resetProgress(sessionState.cards);
            finishDialog.close();
            resetConfirmDialog.close();
            sessionState.totalEFactor = 0;
        } else if (event.target.id === "no-reset-button") {
            resetConfirmDialog.close();
        }
    })
}
