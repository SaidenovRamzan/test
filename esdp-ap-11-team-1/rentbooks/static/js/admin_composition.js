$(document).ready(function () {
    $('#selected').click(function () {
        var token = localStorage.getItem('Token');
        var selectedCompositions = $('.composition:checked').map(function () {
            return $(this).val();
        }).get();

        if (selectedCompositions.length > 0) {
            var data = { selectedCompositions: selectedCompositions }
            // Here, you can send the selectedCompositions array to your API
            console.log('Selected Compositions:', selectedCompositions);
            // Example: Send data using AJAX
            $.ajax({
                method: 'POST',
                url: '/api/composition/admin/selected',
                contentType: 'application/json',
                headers: {
                    'authorization': 'Token ' + token,
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: JSON.stringify(data),
                success: function (response) {
                    for (var i = 0; i < selectedCompositions.length; i++) {
                        $(`#composition_${selectedCompositions[i]}`).remove();
                    }
                    console.log('API Response:', response);
                    console.log(data);
                },
                error: function (error) {
                    console.error('API Error:', error);
                }
            });
        } else {
            alert('Выберите композиции для выполнения действия.');
        }
    });

    // Handle the 'Сделать видимым все' button click
    $('#all').click(function () {
        var token = localStorage.getItem('Token');
        var data = {};
        // Here, you can perform an action for all compositions
        console.log('Performing action for all compositions');
        // Example: Send data using AJAX
        $.ajax({
            url: '/api/composition/admin/all',
            method: 'POST',
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': getCookie('csrftoken')
            },
            data: data,
            success: function (response) {
                $('#composition-rows').empty();
                $('#composition-rows').html('<p>Композиции не найдены</p>');
                console.log('API Response:', response);
            },
            error: function (error) {
                console.error('API Error:', error);
            }
        });
    });

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