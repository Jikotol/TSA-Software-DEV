/*
Handles event handling and calling the functions
*/

import { loadCard, flipCard, nextCard, previousCard } from "./flashcard.js"

export async function initCardData(setId, cardContainer) {

    // Fetches set object and list of card objects
    const request = await fetch("/api/study/" + setId);
    const data = await request.json();

    const cards = data.cards;
    const setName = data.set_name;

    // Holds changing values
    let state = {
        index: 0,
        side: "front",
        termEl: null,
        visualEl: null,
        cardContainer: cardContainer
    }

    return [cards, state]
}

export function setupFlashcardActions(cards, cardContainer, document, state) {
    /* Dynamically creates the event handlers with given data and html */

    // Flips card
    cardContainer.addEventListener("click", () => {flipCard(cards, state)});

    // Goes to the next flashcard
    document.getElementById("next-btn").addEventListener("click", () => {
            nextCard(cards, document, state);
        });
                
    // Goes to the previous flashcard
    document
        .getElementById("back-btn")
        .addEventListener("click", () => {previousCard(cards, document, state)});
                
    document.addEventListener("DOMContentLoaded", () => {
        loadCard(cards, document, state);
        })
    
    loadCard(cards, document, state);
}