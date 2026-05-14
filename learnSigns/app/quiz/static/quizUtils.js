import { loadHandshapeTable } from "/static/vocab/handshape_table.js";

export async function setupQuiz(quizState, quizData, displayData) {

    const elements = getAllElements();

    setupQuizActions(elements, quizState, quizData, displayData)
    setupAnswerChoices(elements, quizState, quizData, displayData)

    syncQuiz(elements, quizState, quizData, displayData)
}

export function initQuizState(questionNum, setId) {

    const questionNums = Array.from({ length: questionNum }, (_, i) => i)

    const answers = Object.fromEntries(questionNums.map(n => [n, null]));

    return {
        questionIndex: 0, // Current question number
        userAnswers: answers, // Users answers for all questions
        questionNum: questionNum, // Number of questions in quiz
        setId: setId
    }
}

function getAllElements() {
    
    return {
        nextButton: document.getElementById("next-button"),
        backButton: document.getElementById("back-button"),
        visualDisplayDiv: document.getElementById("visual-display-div"),
        confirmSubmissionDialog: document.getElementById("confirm-submission-dialog"),
        answerForm: document.getElementById("answer-form"),

        ...getQuestionElements(),
        ...getAnswerElements(),
        ...getDisplayElements()
    }
}

function getAnswerElements() {
    return {
        answerFieldset: document.getElementById("answer-choices-fieldset"),
        answerALabel: document.getElementById("answer-a-label"),
        answerBLabel: document.getElementById("answer-b-label"),
        answerCLabel: document.getElementById("answer-c-label"),
        answerDLabel: document.getElementById("answer-d-label")
    }
}

function getDisplayElements() {
    return {
        signIFrame: document.getElementById("sign-video"),
        creditParagraph: document.getElementById("credit-paragraph"),
        handshapeTable: document.getElementById("handshape-table")
    }
}

function getQuestionElements() {
    return {
        questionHeader: document.getElementById("question-header"),
        questionLegend: document.getElementById("question-legend")
    }
}

function setupAnswerChoices(elements, quizState, quizData, displayData) {
    const {answerFieldset} = elements;

    answerFieldset.addEventListener("change", (event) => {
        const questionIndex = quizState["questionIndex"]
        quizState["userAnswers"][questionIndex] = event.target.value;
        syncQuiz(elements, quizState, quizData, displayData)
    })
}

function setupQuizActions(elements, quizState, quizData, displayData) {
    const { confirmSubmissionDialog, nextButton, backButton, answerForm } = elements;

    nextButton.addEventListener("click", () => {

        if (quizState["questionIndex"] + 1 < quizState["questionNum"]) {
            quizState["questionIndex"] += 1;
            answerForm.reset()
            syncQuiz(elements, quizState, quizData, displayData)
        } else {
            confirmSubmissionDialog.showModal();
        }
        if (quizState["questionIndex"] + 1 == quizState["questionNum"]) {
            answerForm.reset()
            nextButton.innerText = "Submit";
            nextButton.className = "special-buttons";
        }

    })

    backButton.addEventListener("click", () => {



        if (quizState["questionIndex"] != quizState["questionNum"]) {
            nextButton.innerText = "Next";
            nextButton.className = "";
        }

        if (quizState["questionIndex"] > 0) {
            quizState["questionIndex"] -= 1;
            syncQuiz(elements, quizState, quizData, displayData)
        } 
    })
}


function syncQuiz(elements, quizState, quizData, displayData) {

    const questionData = quizData[quizState["questionIndex"]];
    const questionType = questionData["type"];

    syncVisualDisplay(elements, questionType, quizState, displayData);
    syncAnswerChoices(elements, questionData);
    syncQuestionInfo(elements, quizState, quizData);

}

function syncQuestionInfo(elements, quizState, quizData) {
    const { questionHeader, questionLegend } = elements;
    const questionIndex = quizState["questionIndex"]

    questionHeader.innerText = (
        "Question " + (questionIndex + 1) + " of " + quizState["questionNum"]
    );

    if (quizData[questionIndex]["type"] == "video") {
        questionLegend.innerText = (
            "What ASL sign matches the video above?"
        );
    } else {
        questionLegend.innerText = (
            "What ASL sign matches the handshape table above?"
        );
    }

}

function loadVideo(iframe, creditParagraph, url, credit) {
    if (url) {
        iframe.src = url;
    } else {
        iframe.srcdoc = "Video Not Available"
    }
    if (credit) {
        creditParagraph.innerHTML = credit;
    } else {
        creditParagraph.innerHTML = "Unknown source";
    }

    
}


function syncVisualDisplay(elements, questionType, quizState, displayData) {
    const {signIFrame, creditParagraph, handshapeTable} = elements;

    const questionData = displayData[quizState["questionIndex"]];

    if (questionType == "handshape") {
        handshapeTable.hidden = false;
        loadHandshapeTable(questionData["handshapes"], questionData["hsImgs"]);
        creditParagraph.hidden = true;
        signIFrame.hidden = true;
    } else {
        creditParagraph.hidden = false;
        signIFrame.hidden = false;
        loadVideo(signIFrame, creditParagraph, questionData["youtubeUrl"], questionData["credit"]);
        handshapeTable.hidden = true;
        
    }
}

function syncAnswerChoices(elements, questionData) {
    const {answerALabel, answerBLabel, answerCLabel, answerDLabel} = elements;

    const answerChoices = questionData["userChoices"];

    answerALabel.innerHTML = answerChoices["a"];
    answerBLabel.innerHTML = answerChoices["b"];
    answerCLabel.innerHTML = answerChoices["c"];
    answerDLabel.innerHTML = answerChoices["d"];
}
