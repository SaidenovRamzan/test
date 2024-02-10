$('.chat-item').on('click', function() {
    var chatMessages = document.querySelector('.chat-messages');
    chatMessages.innerHTML = '';

    var recipientId = $(this).data('user-id');
    var userShelfId = $(this).find('[data-user-shelf-id]').data('user-shelf-id');

    var dataToSend = {
        "id1": senderId,
        "id2": recipientId,
        "user_shelf": userShelfId
    };

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
    var bookName = $(this).find('[data-book-name]').data('book-name');
    var bookCoverphoto = $(this).find('[data-book-coverphoto]').data('book-coverphoto');

    // получение токена и запрос на получение всех сообщений 
    var csrfToken = getCSRFToken();
    $.ajax({
        url: '/api/all-chat/',
        type: 'POST',
        data: JSON.stringify(dataToSend),
        contentType: 'application/json', 
        headers: {
            'X-CSRFToken': csrfToken // Добавление CSRF-токена в заголовок
        },
        success: function (data) {
            
            var newDiv = $("<div></div>");
            newDiv.html(`<div class="avatar"><img class="img-fluid" src="data:image/;base64,${bookCoverphoto}"
            alt="{{ book.name }} Cover"></div><p>${bookName}</p>`)

            newDiv.appendTo(".chat-messages")
            for (let message of data.messages) {
                var newDiv = $("<div></div>");
                newDiv.html(`<p>${message.message}</p><span class="timestamp">${message.time.slice(11, 16)}</span>`)
                if(message.sender == senderId){
                    newDiv.addClass("message my-message");
                }
                else{
                    newDiv.addClass("message other-message");
                }
                newDiv.appendTo(".chat-messages")
              }
        },
        error: function (error) {
            console.error("Ошибка при выполнении запроса:", error);
        }
    })
});
