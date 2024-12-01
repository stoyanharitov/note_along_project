document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = button.getAttribute('data-post-id');
            const url = button.getAttribute('data-url');
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;

            if (!csrfToken) {
                console.error("CSRF token not found");
                return;
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                const likeCount = button.querySelector('.like-count');
                const icon = button.querySelector('.fa-heart');
                if (data.liked) {
                    icon.classList.add('liked');
                } else {
                    icon.classList.remove('liked');
                }
                likeCount.textContent = data.total_likes;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});