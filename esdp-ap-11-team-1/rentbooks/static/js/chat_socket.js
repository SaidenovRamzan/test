// Объявление переменной chatSocket в глобальной области видимости
var chatSocket;

$('.chat-item').on('click', function() {
    // Закрыть предыдущий сокет, если он существует
    if (chatSocket && chatSocket.readyState === WebSocket.OPEN) {
        chatSocket.close();
    }

    // Удалить обработчики событий
    document.querySelector('#send-button').onclick = null;

    var recipientId = $(this).data('user-id');
    var userShelfId = $(this).find('[data-user-shelf-id]').data('user-shelf-id');
    var currentHost = window.location.hostname;
    var currentPort = window.location.port;

    // Создать новый сокет, если он не существует
    if (!chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
        console.log(`ws://${currentHost}:${currentPort}/ws/chat/${senderId}/${recipientId}/${userShelfId}/`)
        chatSocket = new WebSocket(
            `ws://${currentHost}:${currentPort}/ws/chat/${senderId}/${recipientId}/${userShelfId}/`
        );

        // Установить обработчик события закрытия сокета
        chatSocket.onclose = function (e) {
            console.log('WebSocket is closed');
        };

        // Установить обработчик события прихода сообщения
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            var newDiv = $("<div></div>");
            if (data.message.sender == senderId) {
                newDiv.addClass("message my-message");
            } else {
                newDiv.addClass("message other-message");
            }
            newDiv.html(`<p>${data.message.message}</p><span class="timestamp">${data.message.time.slice(0, 5)}</span>`)
            newDiv.appendTo(".chat-messages")
        };

        // Установить обработчик события отправки сообщения
        document.querySelector('#send-button').onclick = function () {
            const messageInput = document.querySelector('#message-input');
            const message = messageInput.value;
            chatSocket.send(JSON.stringify({ message: message }));
            messageInput.value = '';
        };
    }
});
