let userShelfId = 0

function clearAppendImagesModal() {
    bodyModalAppendImages = document.getElementById('modal-append-images-body');
    bodyModalAppendImages.innerHTML = '<form id="image-upload-form">\n' +
        '                            <div id="image-inputs-container" class="image-inputs-container">\n' +
        '                                <div class="image-input-group mb-2">\n' +
        '                                    <input type="file" class="form-control image-input" name="images[]">\n' +
        '                                    <div class="image-buttons-container">\n' +
        '                                        <button type="button" class="btn btn-success add-image-button">+</button>\n' +
        '                                        <button type="button" class="btn btn-danger remove-image-button">-</button>\n' +
        '                                    </div>\n' +
        '                                </div>\n' +
        '                            </div>\n' +
        '                        </form>\n' +
        '                        <div id="user-id" data-user-id="{{ user.id }}"></div>'
}

const appendImagesButtond = document.querySelectorAll('.append-images-buttons');

// Добавление лисенера на нажатие кнпоку открытия модального окна
appendImagesButtond.forEach(button => button.addEventListener('click', async function () {
        userShelfId = this.getAttribute('value');

        const appendImagesTitle = document.getElementById('append-images-title');
        appendImagesTitle.innerText = `Добавление картинок в объявление ${userShelfId}`;
    }
))

// Добавление лисенера на нажатие кнопки, которая отправляет POST запрос в базу
document.getElementById('btn-append-images').addEventListener('click', function () {
    const formData = new FormData();
    const imageInputs = document.querySelectorAll('.image-input');

    // Добавляем все картинки в FormData
    imageInputs.forEach(function (input, index) {
        if (input.files[0]) {
            formData.append('image', input.files[0]);
        }
    })

    formData.append('book_shelf', userShelfId);

    // Отправка запроса на сервер
    fetch(`${baseUrl}/book_image/book/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Если CSRF token требуется
        }
    })
        .then(response => response.json())
        .then(data => {
            $('#modal-add-photo-to-usershelf').modal('hide');
            clearAppendImagesModal();
            // Здесь можно закрыть модальное окно, если нужно
        })
        .catch(error => {
            console.error('Error:', error); // Обработка ошибок
        });
})

// Функция для получения CSRF token из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function () {
    var imageUploadForm = document.getElementById('image-upload-form');
    var imageInputsContainer = document.getElementById('image-inputs-container');

    imageUploadForm.addEventListener('click', function (event) {
        if (event.target.classList.contains('add-image-button')) {
            var newImageInputGroup = document.createElement('div');
            newImageInputGroup.className = 'image-input-group mb-2';
            newImageInputGroup.innerHTML =
                '<input type="file" class="form-control image-input" name="images[]">' +
                '<div class="image-buttons-container">' +
                '<button type="button" class="btn btn-success add-image-button">+</button>' +
                '<button type="button" class="btn btn-danger remove-image-button">-</button>' +
                '</div>';

            imageInputsContainer.appendChild(newImageInputGroup);
            updateButtonsState();
        }

        if (event.target.classList.contains('remove-image-button')) {
            var groupToRemove = event.target.closest('.image-input-group');
            if (groupToRemove) {
                imageInputsContainer.removeChild(groupToRemove);
                updateButtonsState();
            }
        }
    });

    function updateButtonsState() {
        var allGroups = imageInputsContainer.getElementsByClassName('image-input-group');
        var allRemoveButtons = imageInputsContainer.getElementsByClassName('remove-image-button');
        if (allGroups.length === 1) {
            allRemoveButtons[0].style.display = 'none';
        } else {
            Array.from(allRemoveButtons).forEach(function (button) {
                button.style.display = 'block';
            });
        }
    }

    updateButtonsState();
});
