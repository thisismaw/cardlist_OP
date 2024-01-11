document.addEventListener('DOMContentLoaded', () => {
    fetch('/data')
        .then(response => response.json())
        .then(cards => {
            const container = document.getElementById('cardsContainer');

            cards.forEach(card => {
                card.cardName.forEach((name, index) => {
                    if (card.backCol[index].color === "ColorBlack") {
                        const cardElement = document.createElement('div');
                        cardElement.className = 'product';
                        cardElement.innerHTML = `
                            <img src="${card.frontCol[index].imageUrl}">
                            <h3>${name}</h3>
                            <div class="info">${card.infoCol[index]}</div>
                            <div class="front">${card.frontCol[index].text}</div>
                            <div class="back">${card.backCol[index].attribute}</div>
                            <div class="color">${card.backCol[index].color}</div>
                            <button class="add-to-cart">Add to Cart</button>
                        `;
                        container.appendChild(cardElement);

                        cardElement.querySelector('.add-to-cart').addEventListener('click', function(event) {
                            event.stopPropagation();
                            showModal(card, index);
                        });
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching card data:', error));

    function showModal(card, index) {
        const modal = document.getElementById('myModal');
        const modalBody = document.getElementById('modalBody');
        const span = document.getElementsByClassName('close')[0];

        modal.style.display = 'block';
        modalBody.innerHTML = `
            <h3>${card.cardName[index]}</h3>
            <img src="${card.frontCol[index].imageUrl}" alt="Card Image">
            <div>Info: ${card.infoCol[index]}</div>
            <div>Front: ${card.frontCol[index].text}</div>
            <div>Back: ${card.backCol[index].attribute}</div>
            <div>Color: ${card.backCol[index].color}</div>
            <div>Price: ${card.backCol[index].price}</div>
        `;

        span.onclick = () => modal.style.display = 'none';
        window.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        };
    }
});
