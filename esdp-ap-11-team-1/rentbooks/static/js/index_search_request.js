function redirectToSearch() {
    var searchQuery = document.getElementById('search-query').value;

    // Проверка наличия значения в поле ввода
    if (searchQuery) {
        // Формируем URL с параметром запроса
        var redirectURL = '/books/?query=' + encodeURIComponent(searchQuery);

        // Выполняем редирект
        window.location.href = redirectURL;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var searchButton = document.getElementById('search-button');
    searchButton.addEventListener('click', function () {
        redirectToSearch();
    });
});

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

document.getElementById('search-query').addEventListener('input', function (e) {
    let searchQuery = e.target.value;
    let resultsContainer = document.getElementById('search-results-container');

    if (searchQuery.length > 0) {
        resultsContainer.style.display = 'block';

        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                console.log(JSON.parse(this.response));
                let books = JSON.parse(xhr.responseText).books;
                displayResults(books);
            }
        }
        xhr.open('POST', `http://localhost:8000/elastic_1`);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.send(JSON.stringify({'search_request': searchQuery}));
    } else {
        resultsContainer.style.display = 'none';
    }
})

function displayResults(books) {
    let resultsDiv = document.getElementById('search-results-container');
    resultsDiv.innerHTML = ''; // Очистить текущие результаты

    books.forEach(function (book) {
        console.log(book.id);
        let card = document.createElement('div');
        card.classList.add('search-card');
        card.innerHTML = `<a href="/composition/${book.id}/details/"><div class="card mb-3" style="max-width: 540px;">` +
                              `<div class="row g-0">` +
                                    `<div class="col-md-2">` +
                                        `<img src="data:image/;base64,${book.coverphoto}" class="img-fluid rounded-start search-card-image" alt="...">` +
                                    `</div>` +
                                    `<div class="col-md-10">` +
                                        `<div class="card-body text-into-navbar">` +
                                            `<h5 class="card-title">${book.name}</h5>` +
                                        `</div>` +
                                    `</div>` +
                              `</div>` +
                          `</div></a>`
        resultsDiv.appendChild(card);
        console.log(resultsDiv);
    });
}