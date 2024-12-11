document.addEventListener('DOMContentLoaded', () => {
    // Edit comment functionality
    document.querySelectorAll('.edit-btn').forEach(editButton => {
        editButton.addEventListener('click', () => {
            const commentId = editButton.getAttribute('data-comment-id');
            const commentElement = document.querySelector(`#comment-${commentId}`);
            const contentElement = commentElement.querySelector('.comment-content');
            const formElement = commentElement.querySelector('.edit-form');

            // Toggle visibility
            contentElement.style.display = 'none';
            formElement.style.display = 'block';
        });
    });

    // Save edited comment
    document.querySelectorAll('.save-btn').forEach(saveButton => {
        saveButton.addEventListener('click', () => {
            const commentId = saveButton.getAttribute('data-comment-id');
            const postId = saveButton.getAttribute('data-post-id');
            const commentElement = document.querySelector(`#comment-${commentId}`);
            const editContent = commentElement.querySelector('.edit-content').value;
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

            if (!csrfToken) {
                console.error("CSRF token not found");
                return;
            }

            fetch(`/posts/${postId}/comments/${commentId}/edit/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: editContent }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const contentElement = commentElement.querySelector('.comment-content');
                const formElement = commentElement.querySelector('.edit-form');

                // Update the content and toggle visibility
                contentElement.textContent = data.updated_content;
                contentElement.style.display = 'block';
                formElement.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Cancel edit
    document.querySelectorAll('.cancel-btn').forEach(cancelButton => {
        cancelButton.addEventListener('click', () => {
            const commentId = cancelButton.closest('.edit-form').getAttribute('data-comment-id');
            const commentElement = document.querySelector(`#comment-${commentId}`);
            const contentElement = commentElement.querySelector('.comment-content');
            const formElement = commentElement.querySelector('.edit-form');

            // Toggle visibility
            contentElement.style.display = 'block';
            formElement.style.display = 'none';
        });
    });
});
