let currentCommentData = {};

const comments_list = document.querySelector('.comments_list');
comments_list.onclick = (e) => {
    const itemId = e.target.getAttribute('id');

    if (itemId) {
        if (itemId.startsWith('edit_comment')) {
            const id = itemId.split('edit_comment_')[1];

            if (currentCommentData.id) {
                renderCommentView(currentCommentData.id);
            }

            renderEditCommentView(itemId.split('edit_comment_')[1])
        } else if (itemId.startsWith('cancel_comment')) {
            renderCommentView(itemId.split('cancel_comment_')[1])

        } else if (itemId.startsWith('delete_comment')) {
            const id = itemId.split('delete_comment_')[1]
            fetch(`/api/comments/${id}/`,
                {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.cookie.split('=')[1]
                    },
                }).then(response => response.json()).then(body => {
                const commentId = body.id;
                const commentToDelete = document.getElementById(`comment_${commentId}`);

                commentToDelete.remove();
            })
        } else if (itemId.startsWith('save_comment')) {
            const currentCommentInput = document.getElementById(`comment_input_${currentCommentData.id}`);
            currentCommentData.text = currentCommentInput.value;

            fetch(`/api/comments/${currentCommentData.id}/`,
                {
                    method: 'PUT',
                    body: JSON.stringify({text: currentCommentInput.value}),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.cookie.split('=')[1]
                    },
                }).then(response => response.json()).then(body => {
                renderCommentView(currentCommentData.id);
            })
        }
    }
}

const renderCommentView = (id) => {
    const commentDataContainer = document.getElementById(`comment_data_${currentCommentData.id}`);

    const commentText = document.createElement('div');
    const commentDate = document.createElement('div');
    commentText.innerText = currentCommentData.text;
    commentText.id = `comment_text_${id}`;
    commentText.classList.add('comment_text');
    commentDate.innerText = currentCommentData.date;
    commentDate.id = `comment_date_${id}`;
    commentDate.classList.add('comment_date')

    commentDataContainer.innerHTML = '';
    commentDataContainer.appendChild(commentText)
    commentDataContainer.appendChild(commentDate)

    if (currentCommentData.id == id) {
        currentCommentData = {};
    }

    renderViewButtons(id);
}

const renderEditCommentView = (id) => {
    currentCommentData.id = id;
    const commentDataContainer = document.getElementById(`comment_data_${id}`);
    const commentDiv = document.getElementById(`comment_text_${id}`);
    const commentDate = document.getElementById(`comment_date_${id}`);
    currentCommentData.text = commentDiv.innerText;
    currentCommentData.date = commentDate.innerText;
    commentDataContainer.innerHTML = '';
    const commentInput = document.createElement('input');
    commentInput.id = `comment_input_${id}`;
    commentInput.classList.add('comment_edit_input');
    commentInput.value = currentCommentData.text;
    commentDataContainer.appendChild(commentInput);

    renderEditButtons(id);
}

const renderEditButtons = (id) => {
    const commentEditButton = document.getElementById(`edit_comment_${id}`);
    commentEditButton.id = `save_comment_${id}`;
    commentEditButton.innerText = 'Сохранить';
    const commentDeleteButton = document.getElementById(`delete_comment_${id}`);
    commentDeleteButton.id = `cancel_comment_${id}`;
    commentDeleteButton.innerText = 'Отмена';
};

const renderViewButtons = (id) => {
    const commentSaveButton = document.getElementById(`save_comment_${id}`);
    commentSaveButton.id = `edit_comment_${id}`;
    commentSaveButton.innerText = 'Редактировать';
    const commentCancelButton = document.getElementById(`cancel_comment_${id}`);
    commentCancelButton.id = `delete_comment_${id}`;
    commentCancelButton.innerText = 'Удалить';
};