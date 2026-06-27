export function setupMasteryScoreDialog() {
    const elements = getMasteryScoreElements();

    setupScoresNavButtons(elements);
    
}

function getMasteryScoreElements() {
    return {
        showScoresButton: document.getElementById("show-mastery-scores-button"),
        scoresDialog: document.getElementById("mastery-scores-dialog"),
        escapeScoresbutton: document.getElementById("close-button")
    }
}

function setupScoresNavButtons(elements) {
    const { showScoresButton, scoresDialog, escapeScoresbutton } = elements;

    showScoresButton.addEventListener("click", () => {
        scoresDialog.showModal();
    })

    escapeScoresbutton.addEventListener("click", () => {
        scoresDialog.close();
    })
}