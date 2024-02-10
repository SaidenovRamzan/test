$(document).ready(function() {
    $('.remove_favorite').click(function() {
        const button = $(this);
        const bookId = $("input[name='book_id']").val();
        const username = $("input[name='user_id']").val();
        const bookRow = button.closest('.col');
        const noFavText = $('#no-fav-text');
        var data = {
            'user_id': username,
            'composition_id': bookId
        };

        $.ajax({
            method: 'POST',
            url: '/api/remove-from-favorites',
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify(data),
            success: function(response) {
                bookRow.remove();
                if ($('#book-row').find('.col').length === 0) {
                    noFavText.show();
                    $('.remove_favorite').hide();
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    $('.cancel_order').click(function() {
        const button = $(this);
        const orderId = button.closest('.card').find("input[name='order_id']").val();
        const noOrdersText = $('#no-orders-text');
        $.ajax({
            method: 'POST',
            url: `/api/order/${orderId}/cancel`,
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify({
                'order_id': orderId
            }),
            success: function(response) {
                button.closest(`#card-order-${orderId}`).remove();
                if ($(`.my-orders`).find('.card').length === 0) {
                    noOrdersText.show();
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    $('.decline_order').click(function() {
        const button = $(this);
        const orderId = button.closest('.card').find("input[name='order_id']").val();
        const noOrdersText = $('#no-orders-to-me-text');
        $.ajax({
            method: 'POST',
            url: `/api/order/${orderId}/decline`,
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify({
                'order_id': orderId
            }),
            success: function(responseData) {
                button.closest(`#card-order-to-me-${orderId}`).remove();
                if ($(`.orders-to-me`).find(`.card`).length === 0) {
                    noOrdersText.show();
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    $('.accept_order').click(function() {
        const button = $(this);
        const orderId = button.closest('.card').find("input[name='order_id']").val();
        $.ajax({
            method: 'POST',
            url: `/api/order/${orderId}/approve`,
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify({
                'order_id': orderId
            }),
            success: function(response) {
                $(`#accept_order_${response.id}`).remove();
                $(`#decline_order_${response.id}`).remove();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

    function getCookie(cookieName) {
        var name = cookieName + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var cookieArray = decodedCookie.split(';');
        for (var i = 0; i < cookieArray.length; i++) {
            var cookie = cookieArray[i];
            while (cookie.charAt(0) == ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) == 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return null;
    }
});