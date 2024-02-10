const detailBookButtons = document.querySelectorAll('.detail-book');
detailBookButtons.forEach(button => button.addEventListener('click', async function () {
        const bookId = this.getAttribute('value');

        let xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (this.status === 200) {
                let data = JSON.parse(this.response);

                // Получение тегов для заполнения их контентом из JSON
                modalBookName = document.getElementById('modal-detail-book-name');
                modalBookImage = document.getElementById('modal-detail-book-image');
                modalBookGenre = document.getElementById('modal-detail-book-genre');
                modalBookDescription = document.getElementById('modal-detail-book-description');
                modalBookAuthor = document.getElementById('modal-detail-book-author');
                modalBookHref = document.getElementById('modal-detail-book-href');

                // Заполнение тегов контентом из объекта JSON
                modalBookName.innerText = `${data.name}`;
                modalBookImage.setAttribute('src', `data:image/;base64,${data.coverphoto}`);
                modalBookGenre.innerText = `${data.genre}`;
                modalBookDescription.innerText = `${data.description}`;
                modalBookAuthor.innerText = `${data.author}`;
                modalBookHref.setAttribute('data-bookid', bookId);
            }
        }
        xhr.open('GET', `${baseUrl}/api/books/${bookId}/`);
        xhr.send();
    }
))
//  Редирект на детальную страницу просмотра книги с помощью кнопки "Подробнее" в модальном окне
const RedirectDetailBookButton = document.querySelectorAll('.detail-book-redirect');
RedirectDetailBookButton.forEach(button => button.addEventListener('click', function () {
    const bookId = this.getAttribute('data-bookid');

    // Далее, вы можете использовать bookId для генерации URL
    const detailBookURL = `/composition/${bookId}/details/`; // Пример URL

    // Перенаправьтесь на полученный URL
    window.location.href = detailBookURL;
}));
