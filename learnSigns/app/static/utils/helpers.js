export function floatToPercent(num) {
    if (typeof num != "number" || isNaN(num)) {
        return false;
    }

    return (num * 100) + "%";
}

export function addElementsToList(valuesList, document, listHTMLElement) {

    valuesList.forEach((value) => {
        let listItem = document.createElement("li");
        listItem.innerText = value;
        listHTMLElement.appendChild(listItem);
    })
}