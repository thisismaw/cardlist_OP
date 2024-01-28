document.addEventListener('DOMContentLoaded', () => {
    fetch('/data')
        .then(response => response.json())
        .then(cards => {
            const container = document.getElementById('cardsContainer');

            cards.forEach(card => {
                card.cardName.forEach((name, index) => {
                    if (card.backCol[index].color === "ColorYellow") {
                        let imgPath = card.frontCol[index].img_src.split('../images/')[1];
                        let newImgSrc ='https://asia-en.onepiece-cardgame.com/images/' + imgPath;
                        const cardElement = document.createElement('div');
                        cardElement.className = 'product';
                        cardElement.innerHTML = `
                            <img src="${newImgSrc}" class="clickable-image" alt="Card Image">
                            <h3>${name}</h3>

                        `;
                        container.appendChild(cardElement);
    
                        const imageElement = cardElement.querySelector('.clickable-image');
                        imageElement.addEventListener('click', function() {
                            showModal(card, index, newImgSrc);
                        });
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching card data:', error));
    
    function showModal(card, index, newImgSrc) {
        const modal = document.getElementById('myModal');
        const modalBody = document.getElementById('modalBody');
    
        modal.style.display = 'block';
        modalBody.innerHTML = `
            <h3>${card.cardName[index]}</h3>
            <img src="${newImgSrc}" alt="Card Image">
            <div>Info: ${card.infoCol[index]}</div>
            <div>Front: ${card.frontCol[index].text}</div>
            <div>Back: ${card.backCol[index].attribute}</div>
            <div>Color: ${card.backCol[index].color}</div>
            `;

    const span = document.getElementsByClassName('close')[0];
    span.onclick = () => modal.style.display = 'none';
    window.onclick = (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}
});