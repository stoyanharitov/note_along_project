document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('show-concertgoers-btn');
    const concertgoersList = document.getElementById('concertgoers-list');
    const concertgoersData = document.getElementById('concertgoers-data');

    if (!concertgoersData) {
        console.error("concertgoers-data element not found");
        return;
    }

    const concertgoers = JSON.parse(concertgoersData.textContent || '[]');
    console.log(concertgoers)

    button.addEventListener('click', function () {
        // Toggle the visibility of the list
        if (concertgoersList.style.display === 'none') {
            concertgoersList.style.display = 'block';
        } else {
            concertgoersList.style.display = 'none';
        }

        // If there are concertgoers, populate the list
        if (concertgoers.length > 0) {
            concertgoersList.innerHTML = ''; // Clear any previous content
            concertgoers.forEach(user => {
                const listItem = document.createElement('li');
                const userLink = document.createElement('a');
                userLink.href = user.profile_url;
                userLink.textContent = user.username;
                listItem.appendChild(userLink);
                concertgoersList.appendChild(listItem);
            });
        }
    });
});