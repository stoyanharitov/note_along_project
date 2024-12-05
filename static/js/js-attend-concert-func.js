document.getElementById('toggle-attendance-btn')?.addEventListener('click', function() {
      const concertId = this.getAttribute('data-concert-id');
      const button = this;
      const concertUrl = this.getAttribute('data-concert-url');

      // Send AJAX request to toggle attendance
        fetch(concertUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value, // CSRF Token
          },
          body: JSON.stringify({ concert_id: concertId }),
        })
        .then(response => response.json())
        .then(data => {
                // Update the button text based on the user's attendance status
        if (data.attending) {
          button.textContent = "Going!";

          // Create a new list item and add it to the concertgoers list
          const newUserLi = document.createElement('li');
          const userLink = document.createElement('a');
          userLink.href = `/profile/${data.user.username}`;
          userLink.textContent = data.user.username;
          newUserLi.appendChild(userLink);

          document.getElementById('concertgoers-list').appendChild(newUserLi);
        } else {
          button.textContent = "Join the concert";

          // Find the user's list item and remove it
          const userLi = document.getElementById(`concertgoer-${data.user.id}`);
          if (userLi) {
            userLi.remove();
          }
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });