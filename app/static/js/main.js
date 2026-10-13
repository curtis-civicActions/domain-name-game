function handleCardClick(index, answer, name) {
    console.log("Clicked card index: ", index);
    console.log("Answer index: ", answer);
    console.log("Answer index: ", name);
    let cards = document.getElementsByClassName("clickable-card");
    for (const card of cards) {
        if (card.id === ("card-" + answer)) {
            card.style.backgroundColor = "green";
        }
        else {
            card.style.backgroundColor = "red";
        }
        card.removeAttribute("onclick");
    }
    if (index === answer) {
        document.getElementById("message").innerHTML = "Congratulations!" + String.fromCodePoint(0x1F601) + " You really know your urls.";
    }
    else {
        document.getElementById("message").innerHTML = "Sorry," + String.fromCodePoint(0x1F622) + "  that is not correct. Don't worry, you'll have more chances.";
    }
    let elementId = (name === "viewone") ? "refresh_one" : "refresh_two";
    document.getElementById(elementId).visibility = "visible";
}

async function getAnotherQuestion(view) {
    try {
        const response = await fetch('/update-partial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({view_name: view})
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status ${response.status}`);
        }

        const result = await response.json();
        console.log("Success: ", result);
        return result;
    } catch (error) {
        console.log("Error: ", error);
    }
}

function toggleSwitched(element) {
    const status = element.checked;
    console.log("I made it this far");
    console.log("Status: " + status);

    const btnElement = document.getElementById("thebutton");
    const routePath = "/get-partial/question/" + ((status) ? "domain" : "name");
    console.log("Path: " + routePath);
    btnElement.setAttribute("hx-get", routePath);
    htmx.process(btnElement);
}