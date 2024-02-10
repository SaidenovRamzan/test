$(document).ready(function () {
    $('.start').click(function () {
        const numbers = $('#numbers_for_renter').val();
        const data = {
            'numbers': numbers
        }
        const div = $('.rent-div')
        const orderID = $('#order_id').val();
        const title = $('.status-title');
        const status = $('.status-list');
        $.ajax({
            method: 'POST',
            url: `/api/order/${orderID}/start_rent`,
            contentType: 'application/json',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify(data),
            success: function (data) {
                div.remove();
                title.text('Заказ №' + orderID + '  Статус обработки: Книга принята заказчиком');
                status.text(`Книга у заказчика`);
            },
            error: function (error) {
                alert(`${error.responseJSON.error}`);
            }
        })
    })

    $('.finish').click(function () {
        const numbers = $('#numbers_for_owner').val();
        const data = {
            'numbers': numbers
        };
        const div = $('.rent-div')
        const orderID = $('#order_id').val();
        const title = $('.status-title');
        const status = $('.status-list');
        $.ajax({
            method: 'POST',
            url: `/api/order/${orderID}/finish_rent`,
            contentType: 'application/json',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('Token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify(data),
            success: function (data) {
                div.remove();
                title.text('Заказ №' + orderID + ' Статус обработки: Книга принята владельцем');
                status.text(`Доступна`);
            },
            error: function (error) {
                alert(`${error.responseJSON.error}`);
            }
        })
    })

    function getCookie(cookieName) {
        const name = cookieName + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');
        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return null;
    }
});