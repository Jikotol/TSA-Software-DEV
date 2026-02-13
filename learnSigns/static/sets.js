/*
Handles event handling and calling the functions
*/

import { loadCard, flipCard, nextCard, previousCard } from "./flashcard.js"

const setId = window.location.pathname.split('/').pop();
const cardContainer = document.getElementById("card-div");
// Fetches set object and list of card objects
const request = await fetch("/api/study/" + setId);
const data = await request.json();

const cards = data.cards;
const setName = data.set_name;


console.log(cards);

console.log("ehllo, worked")
console.log(document)

// Holds changing values
let state = {
    index: 0,
    side: "front",
    termEl: null,
    visualEl: null,
    cardContainer: cardContainer
}

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
    document
        .getElementById("name-header")
        .innerText = setName;
})

loadCard(cards, document, state);