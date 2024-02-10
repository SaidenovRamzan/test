let sendData = {}
const appendButton = document.getElementById('btn-append-usershelf');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, начинается ли куки с нужного имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для очистки формы после ISBN
function clearISBN() {
    isbnBlock = document.getElementById('book-isbn');
    pricesBlock = document.getElementById('input-price-block');

    isbnBlock.innerHTML = '';
    pricesBlock.innerHTML = '';

    const stateDiv = document.getElementById('book-state');
    const statusDiv = document.getElementById('book-status-block');
    const purDiv = document.getElementById('book-purpose-block');
    const countDiv = document.getElementById('book-count-block');

    // Создаем радиокнопки выбора состояния и цели книги
    stateDiv.style.display = 'none';
    statusDiv.style.display = 'none';
    purDiv.style.display = 'none';
    countDiv.style.display = 'none';

    appendButton.disabled = true;
}

// Функция для очистки формы после года издания при выборе другого
function clearYears() {
    const yearsBlock = document.getElementById('book-years');
    yearsBlock.innerHTML = '';
    clearISBN();
}

function clearPublishHouses() {
    const publishBlock = document.getElementById('book-publish-houses');
    publishBlock.innerHTML = '';
    clearYears();
}


function clearAllBlocks() {
    const searchBlock = document.getElementById('searched-books-list');
    searchBlock.innerHTML = '';
    clearPublishHouses();
}

function generateBookList(books) {
    searchedBooksListDiv = document.getElementById('searched-books-list');
    for (let i = 0; i < books.length; i++) {
        // Создание самой bootstrap карточки найденной книги
        let cardMarking = document.createElement('div');
        cardMarking.classList.add('col-4');
        let card = document.createElement('div');
        card.setAttribute('data-book', `${books[i].id}`)
        card.classList.add('card');
        cardMarking.appendChild(card);

        // Добавление обложки книги
        let coverphotoBase64 = books[i].coverphoto;
        let image = document.createElement('img');

        image.src = "data:image;base64," + coverphotoBase64;
        image.setAttribute('alt', `${books[i].name}`);
        image.classList.add('card-img-top');
        card.appendChild(image);

        // Добавление контента в саму карточку (поля названия, автора и т.д.)
        let cardBody = document.createElement('div');
        cardBody.classList.add('card-body');
        card.appendChild(cardBody);
        let title = document.createElement('h6');
        title.classList.add('card-title');
        title.innerText = `${books[i].name}`
        let description = document.createElement('p');
        description.classList.add('card-text');
        let originalDescription = books[i].description; // Получаем оригинальное описание
        let truncatedDescription = originalDescription.length > 100 ? originalDescription.substring(0, 100) + '...' : originalDescription; // Ограничиваем до 100 символов (если описание длиннее)
        description.innerText = truncatedDescription;
        let choiceButton = document.createElement('button');
        choiceButton.classList.add('btn', 'btn-warning', 'choice-book-button');
        choiceButton.innerText = 'Выбрать';
        choiceButton.value = `${books[i].id}`;

        cardBody.appendChild(title);
        cardBody.appendChild(description);
        cardBody.appendChild(choiceButton);

        searchedBooksListDiv.appendChild(cardMarking);
    }
    choicePublishHouse();
}

// Функция для изменения выбора книги
function checkSelectedBooks() {
    const choiceBookButtons = document.querySelectorAll('.choice-book-button');

    choiceBookButtons.forEach(function (button) {
        const compositionId = button.getAttribute('value');
        const selectedCard = document.querySelector(`[data-book="${compositionId}"]`);
        if (selectedCard.classList.contains('selected-card')) {
            selectedCard.classList.remove("selected-card");
        }
        button.disabled = false;
    });
    clearPublishHouses();
}

// Функция для создания полей для выбора издательства определенной книги
function createChoicePublishHouse(publishHouses, compositionId) {
    // Достаем блок, где будут лежать радикнопки с выбором издательства
    const radioDiv = document.getElementById('book-publish-houses')
    radioDiv.classList.add('publish-title');

    const col12 = document.createElement('div');
    col12.classList.add('col-12');
    radioDiv.appendChild(col12);

    const title = document.createElement('h5');
    title.innerText = 'Выберете издательство';
    col12.appendChild(title);

    // Добаляем радиокнопки
    for (let i = 0; i < publishHouses.length; i++) {
        radioBox = document.createElement('div');
        radioBox.classList.add('form-check');

        input = document.createElement('input');
        input.classList.add('form-check-publish-input');
        input.classList.add('form-check-input');
        input.setAttribute('type', 'radio');
        input.setAttribute('name', 'flexRadio');
        input.setAttribute('id', `flexRadio${i}`);
        input.setAttribute('data-compositionId', `${compositionId}`)
        radioBox.appendChild(input);

        label = document.createElement('label');
        label.innerText = publishHouses[i].publish_house;
        label.classList.add('form-check-label');
        label.setAttribute('for', `flexRadio${i}`);
        radioBox.appendChild(label);
        col12.appendChild(radioBox);
    }
    choiceYear();
}

function createChoiceBookYears(bookYears, compositionId, izdatelsvo) {
// Достаем блок, где будут лежать радикнопки с выбором издательства
    const yearsDiv = document.getElementById('book-years');
    yearsDiv.classList.add('publish-title');

    const col12 = document.createElement('div');
    col12.classList.add('col-12');
    yearsDiv.appendChild(col12);

    const title = document.createElement('h5');
    title.innerText = 'Выберете год издания';
    col12.appendChild(title);

    // Добаляем года выпуска
    for (let i = 0; i < bookYears.length; i++) {
        radioBox = document.createElement('div');
        radioBox.classList.add('form-check');

        input = document.createElement('input');
        input.classList.add('form-check-year-input');
        input.classList.add('form-check-input');
        input.setAttribute('type', 'radio');
        input.setAttribute('name', 'yearRadio');
        input.setAttribute('id', `yearRadio${i}`);
        input.setAttribute('data-compositionId', `${compositionId}`)
        radioBox.appendChild(input);

        label = document.createElement('label');
        label.innerText = bookYears[i].year;
        label.classList.add('form-check-year-label');
        label.classList.add('form-check-label');
        label.setAttribute('for', `yearRadio${i}`);
        radioBox.appendChild(label);
        col12.appendChild(radioBox);
    }
    getBookISBN(izdatelsvo.innerText);
}

function createISBNBlock(isbn, compositionId, bookId, izdatelsvo) {
    const isbnDiv = document.getElementById('book-isbn');
    isbnDiv.classList.add('isbn-title');

    const col12 = document.createElement('div');
    col12.classList.add('col-12');
    isbnDiv.appendChild(col12);

    const title = document.createElement('h5');
    title.innerText = 'Сверьте с вашим ISBN';
    col12.appendChild(title);
    pISBN = document.createElement('p');
    pISBN.innerText = isbn;
    col12.appendChild(pISBN);
    createBookStatePurposeBlocks(isbn, compositionId, bookId, izdatelsvo);
}

function createBookStatePurposeBlocks(isbn, compositionId, bookId, izdatelsvo) {
    const stateDiv = document.getElementById('book-state');
    const statusDiv = document.getElementById('book-status-block');
    const purDiv = document.getElementById('book-purpose-block');
    const countDiv = document.getElementById('book-count-block');

    // Создаем радиокнопки выбора состояния и цели книги
    stateDiv.style.display = 'block';
    statusDiv.style.display = 'block';
    purDiv.style.display = 'block';
    countDiv.style.display = 'block';

    createPriceBlock(isbn, compositionId, bookId, izdatelsvo);
}

function createPriceBlock(isbn, compositionId, bookId, izdatelsvo) {
    const priceDiv = document.getElementById('input-price-block');

    const title = document.createElement('h5');
    title.innerText = 'Введите расценки';
    priceDiv.appendChild(title);

    // Делаем изначальное поле ввода для стоимости аренды, так как в радиобокс она выбрана по умолчанию
    createRentInput(priceDiv);

    const btnAppendUserShelf = document.getElementById('btn-append-usershelf');
    btnAppendUserShelf.disabled = false;

    updatePriceBlock(isbn, compositionId, bookId, izdatelsvo);
}

function createRentInput(priceDiv) {
    const rentDiv = document.createElement('div');
    const label = document.createElement('label');
    label.innerText = 'Введите стоимость аренды';
    label.setAttribute('for', `rent-coast`);

    const input = document.createElement('input');
    input.setAttribute('type', 'number');
    input.setAttribute('name', 'rent-coast');
    input.setAttribute('id', `rent-coast`);
    input.classList.add('input-numbers-width');
    input.classList.add('form-control');
    input.value = 0;
    rentDiv.appendChild(label);
    rentDiv.appendChild(input);

    priceDiv.appendChild(rentDiv);
}

function createSaleInput(priceDiv) {
    const saleDiv = document.createElement('div');
    const label = document.createElement('label');
    label.innerText = 'Введите стоимость продажи';
    label.setAttribute('for', `sale-coast`);

    const input = document.createElement('input');
    input.setAttribute('type', 'number');
    input.setAttribute('name', 'sale-coast');
    input.setAttribute('id', `sale-coast`);
    input.classList.add('input-numbers-width');
    input.classList.add('form-control');
    input.value = 0;
    saleDiv.appendChild(label);
    saleDiv.appendChild(input);

    priceDiv.appendChild(saleDiv);
}

function updatePriceBlock(isbn, compositionId, bookId, izdatelsvo) {

    const priceDiv = document.getElementById('input-price-block');

    const purposeButtons = document.querySelectorAll('.form-check-purpose-label');
    // Добавляем обработчик на событие для каждой радио-кнопки
    purposeButtons.forEach(function (purposeButton) {
        purposeButton.addEventListener('click', function () {
            priceDiv.innerHTML = '';
            const title = document.createElement('h5');
            title.innerText = 'Введите расценки';
            priceDiv.appendChild(title);

            let purpose = purposeButton.htmlFor;
            if (purpose === 'rent') {
                createRentInput(priceDiv);
            } else if (purpose === 'sale') {
                createSaleInput(priceDiv);
            } else if (purpose === 'rent-and-sale') {
                createRentInput(priceDiv);
                createSaleInput(priceDiv);
            }
        })
    })
    appendBookToShelf(isbn, compositionId, bookId, izdatelsvo);
}

// Функция для получения списка издательств по книге
function getPublishHouses(compositionId) {
    let xhr = new XMLHttpRequest();
    xhr.onload = function () {
        if (this.status === 200) {
            let data = JSON.parse(this.response);
            createChoicePublishHouse(data.publish_houses, compositionId);
        }
    }
    xhr.open('GET', `${baseUrl}/api/book/${compositionId}/get_book_publish_houses/`);
    xhr.send();
}


// Функция для отслеживания выбора книги пользователем и предоставления выбора изданий, выбранной книги
function choicePublishHouse() {
    // Достаем все кнопки для выбора книги
    const choiceBookButtons = document.querySelectorAll('.choice-book-button');

    // Функция для нового слушателя событий
    function updatedFunction() {
        checkSelectedBooks();
        const compositionId = this.getAttribute('value');
        const selectedCard = document.querySelector(`[data-book="${compositionId}"]`);
        selectedCard.classList.add('selected-card');
        this.disabled = true;

        // Очищаем также выбор издательств
        clearPublishHouses();
        getPublishHouses(compositionId);
    }

    // Перебираем все кнопки выбора книги и обновляем слушателей событий
    choiceBookButtons.forEach(button => {
        // Удаляем существующий слушатель (если он есть)
        button.removeEventListener('click', updatedFunction);
        // Добавляем новый слушатель
        button.addEventListener('click', updatedFunction);
    });
}

function choiceYear() {
    const radioButtons = document.querySelectorAll('.form-check-publish-input');

    // Добавляем обработчик на событие для каждой радио-кнопки
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            // Если радио-кнопка выбрана
            if (radioButton.checked) {
                clearYears();
                let compositionId = radioButton.getAttribute('data-compositionId');
                let izdatelstvo = document.querySelector(`label[for="${radioButton.id}"]`);
                // Отправляем запрос в базу с данными об издательстве, чтобы достать годы выпуска книги
                let xhr = new XMLHttpRequest();
                xhr.onload = function () {
                    if (this.status === 200) {
                        let data = JSON.parse(this.response);
                        createChoiceBookYears(data.years, compositionId, izdatelstvo);
                    }
                }
                xhr.open('POST', `${baseUrl}/api/book/${compositionId}/get_book_year/`);
                xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                xhr.send(JSON.stringify({'izdatelstvo': izdatelstvo.innerText}));
            }
        })
    })
}

function getBookISBN(izdatelsvo) {
    const radioYearsButtons = document.querySelectorAll('.form-check-year-input');
    // Добавляем обработчик на событие для каждой радио-кнопки
    radioYearsButtons.forEach(function (radioYearButton) {

        radioYearButton.addEventListener('change', function () {
            // Если радио-кнопка выбрана
            if (radioYearButton.checked) {
                clearISBN();
                let compositionId = radioYearButton.getAttribute('data-compositionId');
                let year = document.querySelector(`label[for="${radioYearButton.id}"]`);
                // Отправляем запрос в базу с данными об издательстве, чтобы достать годы выпуска книги
                let xhr = new XMLHttpRequest();
                xhr.onload = function () {
                    if (this.status === 200) {
                        let data = JSON.parse(this.response);
                        createISBNBlock(data.isbn, compositionId, data.bookId, izdatelsvo);
                    }
                }
                xhr.open('POST', `${baseUrl}/api/book/${compositionId}/get_book_isbn/`);
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
                xhr.send(JSON.stringify({
                    'izdatelstvo': izdatelsvo,
                    'year': year.innerText
                }));
            }
        })
    })
}


function searchBookForShelf() {
    var searchBookForShelfQuery = document.getElementById('search-book-for-shelf-query').value;
    // Проверка наличия значения в поле ввода
    if (searchBookForShelfQuery) {
        clearAllBlocks();
        let xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (this.status === 200) {
                let data = JSON.parse(this.response);
                if (data) {
                    generateBookList(data.books);
                }
            }
        }
        xhr.open('POST', `${baseUrl}/api/books/search/`);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.send(JSON.stringify({'search_request': searchBookForShelfQuery}));
    }
}

// Функция для нахождения выбранного значения состояния книги
function checkStateValue() {
    const stateRadioButtons = document.querySelectorAll('.form-check-state-input');
    let value = null;

// Итерируем по кнопкам
    stateRadioButtons.forEach(function (radioButton) {
        // Проверяем, выбрана ли текущая кнопка
        if (radioButton.checked) {
            // Если выбрана, обновляем значение book_state в объекте sendData
            value = radioButton.value;
        }
    });
    return value;
}

// Функция для нахождения выбранного значения статуса
function checkStatusValue() {
    const statusRadioButtons = document.querySelectorAll('.form-check-status-input');
    let value = null;

// Итерируем по кнопкам
    statusRadioButtons.forEach(function (radioButton) {
        // Проверяем, выбрана ли текущая кнопка
        if (radioButton.checked) {
            value = radioButton.value;
        }
    });
    return value;
}

// Функция для нахождения выбранного значения цели объявления
function checkPurposeValue() {
    const purposeRadioButtons = document.querySelectorAll('.form-check-purpose-input');
    let value = null;

// Итерируем по кнопкам
    purposeRadioButtons.forEach(function (radioButton) {
        // Проверяем, выбрана ли текущая кнопка
        if (radioButton.checked) {
            value = radioButton.value;
        }
    });
    return value;
}

// Проверка на существующие поля ввода цен и добавление их в json для POST запроса
function appendToSendDataPrices(sendData) {
    let price_for_week = document.getElementById('rent-coast');
    if (price_for_week) {
        sendData.price_for_week = price_for_week.value;
    }
    let price_for_sale = document.getElementById('sale-coast')
    if (price_for_sale) {
        sendData.price_for_sale = price_for_sale.value;
    }
    return sendData;
}

function appendBookToShelf(isbn, compositionId, bookId, izdatelstvo) {
    let count = document.getElementById('book-count-input').value;
    let userId = document.getElementById('user-id');

    sendData.user = userId.dataset.userId;
    sendData.id_book = parseInt(bookId);
    sendData.count = parseInt(count);
    sendData.book_state = checkStateValue();
    sendData.status = checkStatusValue();
    sendData.purpose = checkPurposeValue();
}

document.addEventListener('DOMContentLoaded', function () {
    var searchBookForShelfButton = document.getElementById('search-book-for-shelf-button');
    searchBookForShelfButton.addEventListener('click', function () {
        searchBookForShelf();
    });

    // Cобытие на добавление книги на полку
    appendButton.addEventListener('click', function () {
        sendData = appendToSendDataPrices(sendData);
        let xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (this.status === 200) {
                let data = JSON.parse(this.response);
                $('#modal-add-book-to-shelf').modal('hide');
                clearAllBlocks();
                let searchInput = document.getElementById('search-book-for-shelf-query');
                searchInput.value = '';
                appendButton.disabled = true;
            }
        }
        xhr.open('POST', `${baseUrl}/api/usershelf`);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.send(JSON.stringify(sendData));
    });
});


