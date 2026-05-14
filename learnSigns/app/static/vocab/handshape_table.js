// Gets a handshape table and inserts data
export async function loadHandshapeTable(handshapeData, handshapeImgs) {
    // Gets html elements of the hand shape table contained in a doc 
    const doc = await getHandshapeTableDoc();

    injectHandshapeData(handshapeData, handshapeImgs, doc);
    updateHandshapeTable(doc);
}

async function getHandshapeTableDoc() {
    const response = await fetch("/display/static/handshapes-table.html");
    const htmlString = await response.text();

    const parser = new DOMParser();

    // Creates HTML elements from html string
    const doc = parser.parseFromString(htmlString, 'text/html');

    return doc;
}

function injectHandshapeData(handshapeData, handshapeImgs, doc) {
    for (const handshape of ["dom_start", "dom_end", "non_dom_start", "non_dom_end"]) {
        var p = document.createElement("p");
        var hs_img = document.createElement("img");


        // Inserts the handshape label
        p.innerText = handshapeData[handshape];

        // Inserts video
        if (handshapeImgs[handshape]) {
            hs_img.setAttribute("src", handshapeImgs[handshape]);
        }
        
        if (handshapeData[handshape]) {

            // Gets the td element from the parsed handshape table
            const tableSection = doc.getElementsByClassName(handshape.replaceAll("_", "-"))[0]

            tableSection.appendChild(p);

            if (handshapeImgs[handshape]) {
                tableSection.appendChild(hs_img);
            }
        }
    }
}

function updateHandshapeTable(doc) {

    const handshapeTableEl = document.getElementById("handshape-table");

    // Adds the handshape paragraph and image element to table
    handshapeTableEl.innerHTML = "";
    handshapeTableEl.append(...doc.body.childNodes);
}