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
    
    while (true) {
        let cardIndex = getWeightedCardIndex(cards);

        if (cardIndex != lastCardIndex) {
            state.index = cardIndex;
            return;
        }
    }
    
}

function getWeightedCardIndex(cards) {
    // Gets card based on all cards' easiness factors
    const eFactorArray = cards.map((card) => {
        return card.eFactor;
    })

    console.log(eFactorArray)

    // Adds all the easiness factors up
    const eFactorTotal = eFactorArray.reduce(
        (acc, curr) => acc + curr
    );

    const randomNum = Math.random() * eFactorTotal;
    let upto = 0;

    for (let i=0; i<cards.length; i++) {
        upto += eFactorArray[i];
        if (upto > randomNum) {
            return i;
        }
    }

    // All of the cards have the same easiness factor
    return Math.floor(Math.random() * cards.length);
}

// Updates easiness factors based on the users response 
export function updateEasinessFactor(card, amount) {
    if (card.eFactor + amount > 20) {
        card.eFactor = 20
    } else if (card.eFactor + amount < 0) {
        card.eFactor = 0
    } else {
        card.eFactor += amount;
    }
}

function clearFlashcard(flashcardDiv) {
    flashcardDiv.innerHTML = "";
}
