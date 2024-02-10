$(document).ready(function () {
    const addTo = $("#submit_comment");
    addTo.click(function () {
        const bookId = $("input[name='composition_id']").val();
        const username = $("input[name='user_id']").val();
        const text = $("textarea[name='text']").val();
        var token = localStorage.getItem('Token');
        var csrftoken = getCookie('csrftoken');

        const data = {
            'composition_id': bookId,
            'user_id': username,
            'text': text,
        }

        $.ajax({
            method: 'POST',
            url: `/api/book/${bookId}/add-comment`,
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': csrftoken,
            },
            data: JSON.stringify(data),
            success: function (data) {
                getComments();
            },
        })
    })

    function getComments() {
        var token = localStorage.getItem('Token');
        var csrftoken = getCookie('csrftoken');
        var noComments = $(".no_comments");
        const bookId = $("input[name='composition_id']").val();
        var isStaff = $("input[name='is_staff']").val();
        $.ajax({
            method: 'GET',
            url: `/api/book/${bookId}/list-comments`,
            contentType: 'application/json',
            headers: {
                'authorization': 'Token ' + token,
                'X-CSRFToken': csrftoken,
            },
            success: function (data) {
                data.sort((b, a) => a.id - b.id);
                console.log(data.length);
                $(".comments_title").empty();
                if (data.length === 0) {
                    $(".comments_title").append(`<p>Пока нет комментариев</p>`)
                }
                if (isStaff === 'True') {
                    data.forEach(comment => {
                        const commentDate = new Date(comment.date_publish);
                        const commentTemplate = `
                        <div id="comment_${comment.id}" class="comment_item">
                            <div class="comment_field">
                                <div>Автор:</div>
                                <div>
                                <span>
                                ${comment.user}
                                </span>
                                </div>
                            </div>
                            <div id="comment_data_${comment.id}">
                                <div id="comment_text_${comment.id}" class="comment_text">${comment.text}</div>
                                <div id="comment_date_${comment.id}" class="comment_date">
                                <span>
                                ${formatDate(commentDate)}
                                </span>
                                </div>
                            </div>
                            <div id="comment_actions_${comment.id}" class="comment_actions">
                                <button id="delete_comment_${comment.id}" class="btn btn-outline-danger btn-sm">Удалить
                                </button>
                            </div>
                        </div>`;
                        $(".comments_title").append(commentTemplate);
                    });
                } if (isStaff === 'False') {
                    data.forEach(comment => {
                        const commentDate = new Date(comment.date_publish);
                        const commentTemplate = `
                        <div id="comment_${comment.id}" class="comment_item">
                            <div class="comment_field">
                                <div>Автор:</div>
                                <div>
                                <span>
                                ${comment.user}
                                </span>
                                </div>
                            </div>
                            <div id="comment_data_${comment.id}">
                                <div id="comment_text_${comment.id}" class="comment_text">${comment.text}</div>
                                <div id="comment_date_${comment.id}" class="comment_date">
                                <span>
                                ${formatDate(commentDate)}
                                </span>
                                </div>
                            </div>
                        </div>`;
                        $(".comments_title").append(commentTemplate);
                    });
                }
            }
        })
    }

    function formatDate(dateString) {
        const date = new Date(dateString);

        const options = {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'Asia/Dhaka',
        };

        const formatter = new Intl.DateTimeFormat('en-GB', options);
        return formatter.format(date);
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
    getComments();
})
