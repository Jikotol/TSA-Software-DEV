/* Controls the dialogs for finishing the learning session */

import { MAX_E_FACTOR } from "/static/utils/constants.js";
import { initReturnToSetsButton, initReviewModeButton, formatElapsedTime } from "./dialogUtils.js";
import { addArrayNumbers, getAllEFactors } from "/display/static/flashcard.js";

export function setupFinishDialog(document, cardButtonsDiv, sessionState) {

    const elements = getAllElements(document);

    setupSessionData(elements, sessionState);

    setupNavigationButtons(elements, sessionState);

    setupFinishDialogToggle(elements, sessionState);

    setupCardButtonsDiv(elements, cardButtonsDiv, sessionState);

}

function setupFinishDialogToggle(elements, sessionState) {
    const { timeHeader, termsLearnedDiv, document, finishDialog } = elements;

    finishDialog.addEventListener('toggle', (event) => {
        if (finishDialog.open) {
            updateTermsLearnedList(elements, sessionState);
            timeHeader.innerText = formatElapsedTime(sessionState.timeElapsed);
        }
    });
}

function setupCardButtonsDiv(elements, cardButtonsDiv, sessionState) {
    const { finishDialog } = elements;

    cardButtonsDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "BUTTON") {
            console.log(getAllEFactors(sessionState.cards));

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
        ...getTermListElements(finishDialog)
    }
}

function getNavigationElements(finishDialog) {
    const finishNavigationDiv = finishDialog.querySelector("#finish-navigation-div");
    return {
        finishNavigationDiv,
        resetLearningButton: finishNavigationDiv.querySelector("#reset-learning-button"),
        reviewModeButton: finishNavigationDiv.querySelector("#review-mode-button"),
        returnToSetsButton: finishNavigationDiv.querySelector("#return-to-sets-button")
    }
}

function getInfoElements(finishDialog) {
    const finishInfoDiv = finishDialog.querySelector("#finish-details-div");
    return {
        finishInfoDiv: finishInfoDiv,
        timeHeader: finishInfoDiv.querySelector("#final-time-elapsed-header"),
        finishHeader: finishInfoDiv.querySelector("#finish-header"),
        termsLearnedHeader: finishInfoDiv.querySelector("#total-learned-header")
    }   
}

function getTermListElements(finishDialog) {
    const termsLearnedDiv = finishDialog.querySelector("#terms-learned-list-div");
    return {
        termsLearnedDiv: termsLearnedDiv,
        termsListUl: termsLearnedDiv.querySelector("#terms-learned-ul")
    }
}

function setupSessionData(elements, sessionState) {
    const { finishHeader, termsLearnedHeader } = elements;

    finishHeader.innerText = `${sessionState.setName} Learned`;
    termsLearnedHeader.innerText = `Terms Learned: ${sessionState.cards.length}`
}


function updateTermsLearnedList(elements, sessionState) {
    const { document, termsListUl } = elements;

    termsListUl.innerHTML = "";

    sessionState.cards.forEach((card) => {
        let cardLi = document.createElement("LI");
        cardLi.innerText = card.term;
        termsListUl.appendChild(cardLi);
    })
}

function setupNavigationButtons(elements, sessionState) {
    const { reviewModeButton, returnToSetsButton } = elements;

    setupResetLearningButton(elements, sessionState);

    // From flashcard.js
    initReviewModeButton(reviewModeButton, sessionState); 
    initReturnToSetsButton(returnToSetsButton);

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
            sessionState.timeElapsed = 0;
        } else if (event.target.id === "no-reset-button") {
            resetConfirmDialog.close();
        }
    })
}
