let container = document.getElementById('id_music_genre_preferences');

    // Ensure the container exists before applying styles
    if (container) {
        // Set the max-height and enable scrolling
        container.style.maxHeight = '10em';  // Adjust this height as needed
        container.style.overflowY = 'auto';   // Enables vertical scrolling
        container.style.padding = '10px';     // Optional: Add padding for spacing
        container.style.border = '1px solid #ccc';  // Optional: Border for visual separation
        container.style.backgroundColor = '#606060'; // Optional: Background color
    } else {
        container = document.getElementById('id_genres');
        container.style.maxHeight = '10em';  // Adjust this height as needed
        container.style.overflowY = 'auto';   // Enables vertical scrolling
        container.style.padding = '10px';     // Optional: Add padding for spacing
        container.style.border = '1px solid #ccc';  // Optional: Border for visual separation
        container.style.backgroundColor = '#606060'; // Optional: Background color
    }