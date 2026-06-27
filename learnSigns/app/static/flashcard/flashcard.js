/* 
Contains functions for making the HTML
*/

import { MAX_E_FACTOR } from "../utils/constants.js";

// Updates new data to state when card changes and syncs changes
export function loadCard(cards, state) {
    let card = cards[state.index];

    clearFlashcard(state);
    
    state.termEl = createTermEl(card);
    state.visualEl = createVisualEl(card);

    // Update DOM
    syncSide(cards, state)
}

function syncSide(cards, state) {
    let card = cards[state.index];

    clearFlashcard(state);

    // Appends the correct html element based on side
    if (card["front"] == "term") {
        state.frontDiv.append(state.termEl);
    } else {
        state.frontDiv.append(state.visualEl);
    }
    if (card["back"] == "term") {
        state.backDiv.append(state.termEl);
    } else {
        state.backDiv.append(state.visualEl);
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

export function updateCardSide(state) {

    if (state.side == "front") {
        state.side = "back"
    } else {
        state.side = "front"
    }
}

export function nextCard(cards, state) {
    state.side = "front";
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

    // Convert so higher eFactor = lower chance
    const weights = eFactorArray.map(eFactor => 1 / (eFactor || 1));

    // Adds all the weights up
    const eFactorTotal = addArrayNumbers(weights);

    const randomNum = Math.random() * eFactorTotal;
    let upto = 0;

    for (let i = 0; i < cards.length; i++) {
        upto += weights[i];

        if (randomNum < upto) {
            return i;
        }
    }

    // fallback (only really needed if something is zero/invalid)
    return cards.length - 1;
}


// Updates easiness factors based on the users response 
export function updateEasinessFactor(card, amount) {
    if (card.eFactor + amount > MAX_E_FACTOR) {
        card.eFactor = MAX_E_FACTOR
    } else if (card.eFactor + amount <= 0) {
        card.eFactor = 0
    } else {
        card.eFactor += amount;
    }
}

function clearFlashcard(state) {
    state.frontDiv.innerHTML = "";
    state.backDiv.innerHTML = "";
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