const button = document.querySelector('.toggle-attendance-btn');

if (button) {
    button.addEventListener('click', () => {
        const concertId = button.getAttribute('concert-id');
        const url = button.getAttribute('data-concert-url');
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

        if (!csrfToken) {
            console.error("CSRF token not found");
            return;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ concert_id: concertId }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Change button text based on attendance
            if (data.attending) {
                button.textContent = "Going!";
            } else {
                button.textContent = "Join the concert";
            }

            // Update the concertgoers count
            const concertgoersCountElement = document.getElementById('concertgoers-count');
            if (concertgoersCountElement) {
                const currentCount = parseInt(concertgoersCountElement.textContent.replace('Concertgoers: ', ''));
                concertgoersCountElement.textContent = `Concertgoers: ${currentCount + (data.attending ? 1 : -1)}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

