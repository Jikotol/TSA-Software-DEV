import { setupFinishDialog } from "./quizFinishDialog.js";

export function setupSubmissionDialog(quizState, quizData) {
    const elements = getAllElements();

    setupNoSubmitButton(elements);
    setupYesSubmitButton(elements, quizState, quizData)
}

function getAllElements() {
    return {
        noSubmitButton: document.getElementById("no-submit-button"),
        yesSubmitButton: document.getElementById("yes-submit-button"),
        finishDialog: document.getElementById("quiz-finish-dialog"),
        submissionDialog: document.getElementById("confirm-submission-dialog")
    }
}

function setupNoSubmitButton(elements) {
    const { noSubmitButton, submissionDialog } = elements;

    noSubmitButton.addEventListener("click", () => {
        submissionDialog.close();
    })
}

function setupYesSubmitButton(elements, quizState, quizData) {
    const { yesSubmitButton, submissionDialog, finishDialog } = elements;

    yesSubmitButton.addEventListener("click", () => {
        submissionDialog.close()
        finishDialog.showModal();
        setupFinishDialog(quizState, quizData);
    })
}

