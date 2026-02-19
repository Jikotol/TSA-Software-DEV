/* 
Contains functions for making the HTML
*/

// Updates new data to state when card changes and syncs changes
export function loadCard(cards, document, state) {
    let card = cards[state.index];

    clearFlashcard(state.cardContainer);
    state.side = "front";
    
    state.termEl = createTermEl(card, document);
    state.visualEl = createVisualEl(card, document);



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

function createTermEl(card, document) {
    let termEl = document.createElement("h1");
    termEl.innerText = card["term"];
    return termEl
}

function createVisualEl(card, document) {
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

export function nextCard(cards, document, state) {
    if (state.index < cards.length-1) {
        state.index += 1;
        loadCard(cards, document, state);
    }
}

export function previousCard(cards, document, state) {
    if (state.index > 0) {
        state.index -= 1;
        loadCard(cards, document, state);
    }
}

function clearFlashcard(flashcardDiv) {
    flashcardDiv.innerHTML = "";
}