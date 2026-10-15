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

function toggleSwitched(element) {
    const status = element.checked;

    const btnElement = document.getElementById("thebutton");
    const routePath = "/get-partial/question/" + ((status) ? "domain" : "name");
    console.log("Path: " + routePath);
    btnElement.setAttribute("hx-get", routePath);
    htmx.process(btnElement);
}

function fetchSpreadsheetData() {
    const btn = document.getElementById('load-btn');
    const container = document.getElementById('loading-container');
    const bar = document.getElementById('loading-bar');
    const displayArea = document.getElementById('data-display-area');

    // Show loading bar, hide button
    btn.style.display = 'none';
    container.style.display = 'block';
    displayArea.innerHTML = '';

    let width = 0;
    // Animate smoothly to 95% while waiting for the network
    const interval = setInterval(() => {
        if (width < 95) {
            width += (95 -width) * 0.1;
            bar.style.width = width + '%';
        }
    }, 150);

    // Call Flask API endpoint
    fetch('/fetch/data')
        .then(response =>{
            if (!response.ok) throw new Error('Network response failed');
            return response.json();
        })
        .then(result => {
            clearInterval(interval);
            bar.style.width = '100%';

            setTimeout(() => {
                container.style.display = 'none';
                btn.style.display = 'block';

                // Display the simple success message
                displayArea.innerHTML = `
                    <div style="padding: 15px; background-color: #d1fae5; border: 1px solid #10b981; color: #065f46; border-radius: 4px; font-weight: bold; width: 40%;">
                        ${result.message}
                    </div>
                    `;
            }, 300)
        })
        .catch(error => {
            clearInterval(interval);
            console.error('Error executing job:', error);
            alert('Failed to process spreadsheet data.');
            container.style.display = 'none';
            btn.style.display = 'block';
        })
}

function setUpListener(elementId) {
    document.getElementById(elementId).addEventListener('blur', function (e) {
        const fullId = e.target.id;
        const parts = fullId.split('-');
        if (parts.length < 2) return;

        console.log(`Listener triggered for element ${fullId}`);
        const listName = parts[0];
        const index = parts[1];

        const formData = new FormData();
        formData.append('_list_name', listName);
        formData.append('_index', index);

        // Find all inputs belonging to this specific FieldList and append them
        // This ensures WTForms reconstructs the entire list array correctly on the backend
        const allInputsInList = document.querySelectorAll(`[id^="${listName}-"]`);
        allInputsInList.forEach(input=> {
            if (input.tagName === 'INPUT' || input.tagName === 'TEXTAREA') {
                formData.append(input.id, input.value);
            }
        })

        fetch('/validate-field', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                const errorSpan = document.getElementById(`${data._element}-error-message`);
                if (!data._valid) {
                    errorSpan.textContent = data._error;
                } else {
                    errorSpan.textContent = '';
                }
            })
            .catch(error => console.error('Error validating field:', error));
    });
}


document.addEventListener('DOMContentLoaded', function() {
    // Need to add eventListener to the first domains field
    setUpListener('domains-0');

    const container = document.getElementById('domain-fields-container');

    if (container) {
        container.addEventListener('input', function (e) {
            const wrappers = container.getElementsByClassName('domain-input-wrapper');
            const lastInput = wrappers[wrappers.length - 1].querySelector('input');

            //I If the user typed into the very last input field, append a new empty one
            if (e.target === lastInput && lastInput.value.trim() !== '') {
                const nextIndex = wrappers.length;
                const newWrapper = document.createElement('div');
                newWrapper.className = 'domain-input-wrapper';

                let fieldname = `domains-${nextIndex}`

                // WTForms expects sequential IDs and names like domains-0, domains-1, domains-2
                newWrapper.innerHTML = `
                    <input id="${fieldname}" name="${fieldname}" type="text" value"" class="wtf-form-input">
                    <span id="${fieldname}-error-message" class="error_message"></span>
                `;

                container.appendChild(newWrapper);

                setUpListener(fieldname);
            }
        });
    }
});
