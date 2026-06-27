/*
Handles event handling and calling the functions
*/

import { loadCard, updateCardSide } from "./flashcard.js"

export async function initCardData(setId, frontDiv, backDiv) {

    // Fetches set object and list of card objects
    const request = await fetch("/api/study/" + setId);
    const data = await request.json();

    const cards = data.cards;
    const setName = data.set_name;

    // Holds changing values
    let state = {
        setName: setName,
        index: 0,
        side: "front",
        termEl: null,
        visualEl: null,
        frontDiv: frontDiv,
        backDiv: backDiv,
    }

    return [cards, state]
}

export function getCardStructureElements() {
    const cardButtonsDiv = document.getElementById("flashcard-actions");
    return {
        cardButtonsDiv,
        nameHeader: document.getElementById("name-header"),
        cardDiv: document.getElementById("card-div"),
    }
}

export function setupFlashcard(elements, cards, cardState) {
    const { nameHeader, cardDiv } = elements;

    nameHeader.innerText = cardState.setName;

    // Flips card
    cardDiv.addEventListener("click", () => {
        console.log(cardState.side)
        updateCardSide(cardState)
        if (cardState.side == "front") {
            cardDiv.style.transform = "rotateX(0deg)";
        } else {
            cardDiv.style.transform = "rotateX(180deg)";
        }
    });

    document.addEventListener("DOMContentLoaded", () => {
        loadCard(cards, cardState);
    })
}
