/*
Handles event handling and calling the functions
*/

import { loadCard, flipCard, nextCard, previousCard, updateEasinessFactor, selectWeightedCard } from "../../display/static/flashcard.js"

export async function initCardData(setId, cardContainer) {

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
        cardContainer: cardContainer
    }

    return [cards, state]
}

export function getCardStructureElements() {
    const cardButtonsDiv = document.getElementById("flashcard-actions");
    return {
        cardButtonsDiv,
        nameHeader: document.getElementById("name-header"),
        cardContainer: document.getElementById("card-div"),
    }
}



export function setupFlashcard(elements, cards, cardState) {
    const { nameHeader, cardContainer } = elements;

    nameHeader.innerText = state.setName;

    // Flips card
    cardContainer.addEventListener("click", () => {
        flipCard(cards, cardState)
    });

    document.addEventListener("DOMContentLoaded", () => {
        loadCard(cards, cardState);
    })
}



export function setupFlashcardActions(nameHeader, cards, cardContainer, cardButtonsDiv, state, reviewMode=true) {
    /* Dynamically creates the event handlers with given data and html 
    
    ADD what the variables mean!!
    */

    

    // Goes to next card if a button is clicked
    cardButtonsDiv.addEventListener("click", (event) => {
        if (event.target.tagName === "BUTTON") {
            selectWeightedCard(cards, state);
            loadCard(cards, cardState);
        }
    });

