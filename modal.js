fetch('/data')
    .then(response => response.json())
    .then(cards => {
        // ... existing code ...

        function processArray(arr) {
            // ... existing code ...

            item.cardName.forEach((name, index) => {
                // ... existing code for creating cardElement ...

                // Event listener for clicking on the card
                cardElement.addEventListener('click', function() {
                    showModal(item, index);
                });

                container.appendChild(cardElement);
            });
        }

        processArray(cards);
    })
    .catch(error => console.error('Error fetching card data:', error));

// Function to show the modal with details of the clicked card
function showModal(item, index) {
    const modal = document.getElementById("myModal");
    const modalBody = document.getElementById("modalBody");
    const span = document.getElementsByClassName("close")[0];

    modal.style.display = "block";

    // Populate modal with card details
    modalBody.innerHTML = `
        <h3>${item.cardName[index]}</h3>
        <img src="${item.frontCol[index].imageUrl}">
        <div>Info: ${item.infoCol[index]}</div>
        <div>Front: ${item.frontCol[index].text}</div>
        <div>Back: ${item.backCol[index].attribute}</div>
        <div>Color: ${item.backCol[index].color}</div>
        <div>Price: ${item.backCol[index].price}</div>
    `;

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}
