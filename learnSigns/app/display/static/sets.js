/*
Handles event handling and calling the functions
*/

import { loadCard, flipCard, nextCard, previousCard, updateEasinessFactor, selectWeightedCard } from "./flashcard.js"

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

export function setupFlashcardActions(nameHeader, cards, cardContainer, document, state, reviewMode=true) {
    /* Dynamically creates the event handlers with given data and html */

    nameHeader.innerText = state.setName;

    // Flips card
    cardContainer.addEventListener("click", () => {flipCard(cards, state)});

    if (reviewMode) {
        // Sets event listeners for simple forward and backward flashcard navigation
        // Goes to the next flashcard
        document
            .getElementById("next-btn")
            .addEventListener("click", () => {nextCard(cards, document, state)});
                
        // Goes to the previous flashcard
        document
            .getElementById("back-btn")
            .addEventListener("click", () => {previousCard(cards, document, state)}); 
    } else {
        // Sets event listeners for spaced repetition based flashcard navigation


        document
            .getElementById("easy-btn")
            .addEventListener("click", () => {
                updateEasinessFactor(cards[state.index], 3);
                selectWeightedCard(cards, document, state);
            });
        
        document
            .getElementById("good-btn")
            .addEventListener("click", () => {
                updateEasinessFactor(cards[state.index], 2);
                selectWeightedCard(cards, document, state);
            });

        document
            .getElementById("hard-btn")
            .addEventListener("click", () => {
                updateEasinessFactor(cards[state.index], -2);
                selectWeightedCard(cards, document, state);
            });

        document
            .getElementById("wrong-btn")
            .addEventListener("click", () => {
                updateEasinessFactor(cards[state.index], -4);
                selectWeightedCard(cards, document, state);
            });
    }
    
                
    document.addEventListener("DOMContentLoaded", () => {
        loadCard(cards, document, state);
        })

    loadCard(cards, document, state);
}