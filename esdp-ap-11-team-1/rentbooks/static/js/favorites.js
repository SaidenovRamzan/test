$(document).ready(function () {

    const addTo = $('.add-to-favorites');
    const remFrom = $('.remove-from-favorites');

    addTo.click(function () {
        const bookId = $("input[name='book_id']").val();
        const add = $(`#add_${bookId}`);
        const remove = $(`#remove_${bookId}`);
        const username = $("input[name='user_id']").val();
        var token = localStorage.getItem('Token');

        const data = {
            'composition_id': bookId,
            'user_id': username,
        }
        $.ajax({
            method: 'POST',
            url: '/api/add-to-favorites',
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: JSON.stringify(data),
            success: function (data) {
                add.hide();
                remove.show();
            }
        })
    })

    remFrom.click(function () {
        const bookId = $("input[name='book_id']").val();
        const add = $(`#add_${bookId}`);
        const remove = $(`#remove_${bookId}`);
        const username = $("input[name='user_id']").val();
        var token = localStorage.getItem('Token');
        var data = {
            'user_id': username,
            'composition_id': bookId
        }

        $.ajax({
            method: 'POST',
            url: '/api/remove-from-favorites',
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: JSON.stringify(data),
            success: function (data) {
                remove.hide();
                add.show();
            }
        })
    })


    function getFavorites() {
        var token = localStorage.getItem('Token');
        const bookId = $(this).attr('data-bookid');
        $.ajax({
            method: 'GET',
            url: '/api/favorites/',
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function (data) {
                console.log(data);
                console.log(bookId)
            }
        })
    }

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

})