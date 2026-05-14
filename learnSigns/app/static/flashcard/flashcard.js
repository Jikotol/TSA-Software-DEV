/* 
Contains functions for making the HTML
*/

import { MAX_E_FACTOR } from "../utils/constants.js";

// Updates new data to state when card changes and syncs changes
export function loadCard(cards, state) {
    let card = cards[state.index];

    clearFlashcard(state.cardContainer);
    state.side = "front";
    
    state.termEl = createTermEl(card);
    state.visualEl = createVisualEl(card);

    // Update DOM
    syncSide(cards, state)
}


function syncSide(cards, state) {
    let card = cards[state.index];

    // Appends the correct html element based on side
    if (state.side == "front") {
        if (card["front"] == "term") {
            state.cardContainer.append(state.termEl);
        } else {
            state.cardContainer.append(state.visualEl);
        }
    } else {
        if (card["back"] == "term") {
            state.cardContainer.append(state.termEl);
        } else {
            state.cardContainer.append(state.visualEl);
        }
    }
}

function createTermEl(card) {
    let termEl = document.createElement("h1");
    termEl.innerText = card["term"];
    return termEl
}

function createVisualEl(card) {
    let visualEl = document.createElement("iframe");
    if (card["visual"]) {
        visualEl.src = card["visual"]; 
    } else {
        visualEl.srcdoc = "Video not available"
    }
    return visualEl
}

export function flipCard(cards, state) {
    clearFlashcard(state.cardContainer);

    if (state.side == "front") {
        state.side = "back"
    } else {
        state.side = "front"
    }
    syncSide(cards, state);
}

export function nextCard(cards, state) {
    if (state.index < cards.length-1) {
        state.index += 1;
    }
}

export function previousCard(cards, state) {
    if (state.index > 0) {
        state.index -= 1;
    }
}

// Update the card the user is on using the probability func
export function selectWeightedCard(cards, state) {
    let lastCardIndex = state.index;
    
    if (cards.length == 2) {
        state.index = Math.abs(state.index - 1);
        return;
    }
    while (true) {
        let cardIndex = getWeightedCardIndex(cards);

        if (cardIndex != lastCardIndex) {
            state.index = cardIndex;
            return;
        }
    }
    
}

function getWeightedCardIndex(cards) {
    // Gets card based on all cards' easiness factors and puts the values in an array
    const eFactorArray = getAllEFactors(cards);

    // Adds all the easiness factors up
    const eFactorTotal = addArrayNumbers(eFactorArray);

    const randomNum = Math.random() * eFactorTotal;
    let upto = 0;

    for (let i=0; i<cards.length; i++) {
        upto += eFactorArray[i];

        if (upto < randomNum) {
            return i;
        } else if (upto == 0 && randomNum == 0) {
            break;
        }
    }

    // All of the cards have the same easiness factor
    return Math.floor(Math.random() * cards.length);
}

// Updates easiness factors based on the users response 
export function updateEasinessFactor(card, amount) {
    if (card.eFactor + amount > MAX_E_FACTOR) {
        card.eFactor = MAX_E_FACTOR
    } else if (card.eFactor + amount < 0) {
        card.eFactor = 0
    } else {
        card.eFactor += amount;
    }
}

function clearFlashcard(flashcardDiv) {
    flashcardDiv.innerHTML = "";
}

export function addArrayNumbers(array) {
    const total = array.reduce(
        (acc, curr) => acc + curr
    );

    return total;
}

export function getAllEFactors(cards) {
    const eFactorArray = cards.map((card) => {
        return card.eFactor;
    })
    
    return eFactorArray
}