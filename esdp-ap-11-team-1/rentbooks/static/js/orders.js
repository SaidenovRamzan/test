$(document).ready(function () {
    $('.open-modal').click(function () {
        const button = $(this);
        const usershelfId = button.data('usershelf-id');
        const modal = $(`#exampleModal`);
        const type = button.data('operation-type');
        const select = modal.find('#operation_type');
        select.find('option').remove();
        if (type === 'rent') {
            select.append(`<option value="" disabled selected hidden>Цель</option><option value="rent">Арендовать</option>`);
        }
        if (type === 'sale') {
            select.append(`<option value="" disabled selected hidden>Цель</option><option value="buy">Купить</option>`);
        }
        if (type === 'rent and sale') {
            select.append(`<option value="" disabled selected hidden>Цель</option><option value="rent">Арендовать</option><option value="buy">Купить</option>`);
        }
        modal.find('#usershelf_id').val(usershelfId);
        modal.modal('show');
    });

    $('.create-order').click(function () {
        const button = $(this);
        const usershelfId = $('#usershelf_id').val();
        const userId = $('input[name="user_id"]').val();
        const datePlanStart = $('#date_plan_start').val();
        const datePlanEnd = $('#date_plan_end').val();
        const dateNow = new Date();
        const type = $('#operation_type').val();

        if (type === 'buy') {
            var data = {
                'user_id': userId,
                'composition_id': usershelfId,
                'date_plan_start': convertDateFormat(dateNow.toLocaleDateString()),
                'date_plan_end': null,
                'purpose': type
            };
        }
        if (type === 'rent') {
            if (!datePlanStart || !datePlanEnd) {
                alert('Пожалуйста, выберите дату начала и конца аренды');
                return;
            }
            if (datePlanStart > datePlanEnd) {
                alert('Пожалуйста, выберите дату начала меньшую даты конца аренды');
                return;
            }
            if (new Date(datePlanEnd) < dateNow) {
                alert('Пожалуйста, выберите дату конца аренды больше текущей даты');
                return;
            }
            if (new Date(datePlanStart) < dateNow.setHours(0, 0, 0, 0)) {
                alert('Пожалуйста, выберите дату начала аренды больше или равные текущей дате');
                return;
            }
            var data = {
                'user_id': userId,
                'composition_id': usershelfId,
                'date_plan_start': datePlanStart,
                'date_plan_end': datePlanEnd,
                'purpose': type
            };
        }

        $.ajax({
            method: 'POST',
            url: '/api/create_order',
            contentType: 'application/json',
            headers: {
                'Authorization': 'Token ' + localStorage.getItem('token'),
                'X-CSRFToken': getCookie('csrftoken'),
            },
            data: JSON.stringify(data),
            success: function (responseData) {
                console.log('Order Data:', data);
                console.log('Order Response:', responseData);
                $('#exampleModal').modal('hide');
                $(`.open-modal[data-usershelf-id="${usershelfId}"]`).remove();
                $(`.take-order-${usershelfId}`).append(`<a class="btn btn-success" href="/orders/${responseData.id}/detail">Перейти к заявке</a>`);
            },
            error: function (error) {
                alert(`${error.responseJSON.error}`);
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
    $('#date_plan_end').on('input', function () {
        showCreateOrder();
    });
});

function toggleDateFields() {
    var operationType = document.getElementById("operation_type").value;
    var dateFields = document.getElementById("dateFields");
    var createOrderButton = document.getElementById("create-order");

    if (operationType === "rent") {
        dateFields.style.display = "block";
    } else {
        dateFields.style.display = "none";
    }

    showCreateOrder();
}

function showCreateOrder() {
    var createOrderButton = document.getElementById("create-order");
    var dateStart = document.getElementById("date_plan_start").value;
    var dateEnd = document.getElementById("date_plan_end").value;
    var operationType = document.getElementById("operation_type").value;

    if (operationType === 'buy' || (operationType === 'rent' && dateStart && dateEnd)) {
        createOrderButton.style.display = "block";
    } else {
        createOrderButton.style.display = "none";
    }
}

function convertDateFormat(dateString) {
    var parts = dateString.split('.');
    if (parts.length === 3) {
        return parts[2] + '-' + parts[1] + '-' + parts[0];
    } else {
        return null;
    }
}