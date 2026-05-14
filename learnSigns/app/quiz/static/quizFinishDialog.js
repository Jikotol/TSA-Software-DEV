export function setupFinishDialog(quizState, quizData) {
    const elements = getAllElements()

    // Returns score as a percentage
    const score = calculateScore(quizState, quizData);

    setupNavigationButtons(elements);
    updateMasteryLevel(quizState["setId"], score);
    updateHeaders(elements, score);
}

function getAllElements() {
    return {
        nameHeader: document.getElementById("set-name-header"),
        scoreHeader: document.getElementById("score-header"),
        returnToSetsButton: document.getElementById("return-to-sets-button"),
        goToHomeButton: document.getElementById("go-to-home-button")
    }
}

function setupNavigationButtons(elements) {
    const { goToHomeButton, returnToSetsButton } = elements;

    goToHomeButton.addEventListener("click", () => {
        window.location.href = "/sets/"
    })
    
    returnToSetsButton.addEventListener("click", () => {
        window.location.href = "/home/"
    })
}

function updateHeaders(elements, score) {
    const { nameHeader, scoreHeader } = elements;

    scoreHeader.innerText = "You got " + score + "% correct!"

    let congratsMessage = "Nice try!"

    if (score > 90) {
        congratsMessage = "You've Reached Mastery!";
    } else if (score > 75) {
        congratsMessage = "Keep up the good work!";
    } else if (score > 60) {
        congratsMessage = "Getting familiar!";
    }

    nameHeader.innerText = congratsMessage
}

function calculateScore(quizState, quizData) {
    let score = 0;

    for (const [ index, questionData ] of Object.entries(quizData)) {
        if (quizState["userAnswers"][index] == questionData["correctAnswer"]) {
            score += 1;
        }
        
    }

    const questionNum = quizState["questionNum"];

    return ((score / questionNum) * 100)
}

async function updateMasteryLevel(flashcardSetId, score) {
    fetch("/api/quiz/update-mastery/" + flashcardSetId + "/" + score);
    return
}