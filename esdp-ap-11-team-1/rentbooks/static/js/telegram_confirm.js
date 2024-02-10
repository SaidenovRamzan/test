function getCSRFToken() {
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.indexOf('csrftoken=') === 0) {
            return cookie.substring('csrftoken='.length, cookie.length);
        }
    }
    return null;
}


$(document).ready(function () {
    // Скрыть лейбл для поля "Code" при загрузке страницы
    $('label[for="telegram-code-input"]').hide();
    // Скрыть инпут для кода при загрузке страницы
    $('#telegram-code-input').hide();
    $('#telegram-code-input1').hide();
    $('#telegram-code-input2').hide();

    $('#message-form').submit(function (event) {
        event.preventDefault();

        var formData = new FormData(this);
        var user_id = formData.get('user_id');
        var telegram_id = formData.get('telegram_id');

        var csrfToken = getCSRFToken();

        $.ajax({
            url: 'http://localhost:8000/api/telegram-confirm',
            type: 'POST',
            data: JSON.stringify({ 'user_id': user_id, 'telegram_id': telegram_id }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                console.log(data);

                // Показать лейбл и инпут для кода после успешной отправки данных
                $('label[for="telegram-code-input"]').show();
                $('#telegram-code-input').show();
                $('#telegram-code-input1').show();
                $('#telegram-code-input2').show();

                // Скрыть лейбл и инпут для Telegram ID
                $('label[for="telegram-id-input"]').hide();
                $('#telegram-id-input').hide();
                $('#telegram-id-input3').hide();
                $('#telegram-id-input4').hide();
            },
            error: function (xhr, status, error) {
                if (xhr.status == 404) {
                    console.log('Ресурс не найден (404):', error);
                    alert('ID уже занят')
                } else {
                    console.log('Произошла ошибка:', error);
                    // Дополнительные действия для обработки других ошибок
                }
            }
        });
    });

    // Обработка второй формы для отправки кода
    $('#code-form').submit(function (event) {
        event.preventDefault();
        var code = $('#telegram-code-input').val(); // Получить значение кода
        var user_id = $('#user-id-input').val(); // Получить значение user_id

        var csrfToken = getCSRFToken();

        $.ajax({
            url: 'http://localhost:8000/api/telegram-code',
            type: 'POST',
            data: JSON.stringify({ 'code': code, 'user_id': user_id }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                console.log('Отправка нового инпута:', data);
                $('#telegram-code-input1').click();
            },
        });
    });
});
